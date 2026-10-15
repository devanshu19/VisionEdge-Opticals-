import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, current_app
from auth_utils import roles_required
from flask_jwt_extended import get_jwt_identity
from models import db, Brand, Category, Supplier, Frame, Lens, InventoryTransaction
from sqlalchemy import or_

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/upload-image', methods=['POST'])
@roles_required('admin')
def upload_product_image():
    if 'file' not in request.files:
        return jsonify({"message": "No file uploaded"}), 400
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({"message": "No file selected"}), 400
        
    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg']:
        return jsonify({"message": "Invalid file extension. Please upload an image."}), 400
        
    new_filename = f"prod_{uuid.uuid4().hex[:10]}{ext}"
    upload_dir = os.path.join(current_app.root_path, 'media', 'products')
    os.makedirs(upload_dir, exist_ok=True)
    
    filepath = os.path.join(upload_dir, new_filename)
    file.save(filepath)
    
    relative_url = f"/media/products/{new_filename}"
    return jsonify({"image_url": relative_url, "filename": new_filename}), 200

# --- DASHBOARD STATS ---
@inventory_bp.route('/stats', methods=['GET'])
@roles_required('admin', 'staff')
def get_inventory_stats():
    frames = Frame.query.count()
    lenses = Lens.query.count()
    
    low_frames = Frame.query.filter(Frame.stock <= Frame.min_stock).count()
    low_lenses = Lens.query.filter(Lens.stock <= Lens.min_stock).count()
    
    out_of_stock = Frame.query.filter(Frame.stock == 0).count() + Lens.query.filter(Lens.stock == 0).count()
    
    # Calculate Total Inventory Value (Stock * Price)
    total_value = sum((f.stock * (f.price or 0)) for f in Frame.query.all()) + \
                  sum((l.stock * (l.price or 0)) for l in Lens.query.all())
                  
    return jsonify({
        "total_frames": frames,
        "total_lenses": lenses,
        "low_stock_items": low_frames + low_lenses,
        "out_of_stock": out_of_stock,
        "total_value": total_value
    }), 200

# --- BRANDS ---
@inventory_bp.route('/brands', methods=['GET'])
def get_brands():
    return jsonify([b.to_dict() for b in Brand.query.all()]), 200

@inventory_bp.route('/brands', methods=['POST'])
@roles_required('admin')
def add_brand():
    data = request.get_json()
    if not data.get('name'): return jsonify({"message": "Brand name required"}), 400
    brand = Brand(name=data['name'], status=data.get('status', 'Active'), logo=data.get('logo'))
    db.session.add(brand)
    db.session.commit()
    return jsonify(brand.to_dict()), 201

# --- CATEGORIES ---
@inventory_bp.route('/categories', methods=['GET'])
def get_categories():
    type_filter = request.args.get('type')
    query = Category.query
    if type_filter:
        query = query.filter_by(type=type_filter)
    return jsonify([c.to_dict() for c in query.all()]), 200

@inventory_bp.route('/categories', methods=['POST'])
@roles_required('admin')
def add_category():
    data = request.get_json()
    if not data.get('name') or not data.get('type'): return jsonify({"message": "Name and Type required"}), 400
    category = Category(name=data['name'], type=data['type'], description=data.get('description'))
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201

# --- SUPPLIERS ---
@inventory_bp.route('/suppliers', methods=['GET'])
@roles_required('admin', 'staff')
def get_suppliers():
    return jsonify([s.to_dict() for s in Supplier.query.all()]), 200

@inventory_bp.route('/suppliers', methods=['POST'])
@roles_required('admin')
def add_supplier():
    data = request.get_json()
    if not data.get('name'): return jsonify({"message": "Name required"}), 400
    sup = Supplier(**{k: v for k, v in data.items() if hasattr(Supplier, k)})
    db.session.add(sup)
    db.session.commit()
    return jsonify(sup.to_dict()), 201

# --- FRAMES ---
@inventory_bp.route('/frames', methods=['GET'])
def get_frames():
    query = Frame.query
    search = request.args.get('search')
    if search:
        st = f"%{search}%"
        query = query.filter(or_(Frame.frame_code.ilike(st), Frame.name.ilike(st)))
    return jsonify([f.to_dict() for f in query.all()]), 200

@inventory_bp.route('/frames/<int:id>', methods=['GET'])
def get_frame(id):
    return jsonify(Frame.query.get_or_404(id).to_dict()), 200

@inventory_bp.route('/frames', methods=['POST'])
@roles_required('admin')
def add_frame():
    data = request.get_json()
    if Frame.query.filter_by(frame_code=data.get('frame_code')).first():
        return jsonify({"message": "Frame code already exists"}), 409
        
    if not data.get('price'):
        data['price'] = data.get('selling_price') or 0.0
    frame = Frame(**{k: v for k, v in data.items() if hasattr(Frame, k) and k != 'id'})
    db.session.add(frame)
    db.session.commit()
    
    # Log initial stock if > 0
    if frame.stock > 0:
        tx = InventoryTransaction(
            item_type='Frame', item_id=frame.id, transaction_type='Stock In',
            quantity=frame.stock, reason='Initial Stock', user_id=get_jwt_identity()
        )
        db.session.add(tx)
        db.session.commit()
        
    return jsonify(frame.to_dict()), 201

@inventory_bp.route('/frames/<int:id>', methods=['PUT'])
@roles_required('admin')
def update_frame(id):
    frame = Frame.query.get_or_404(id)
    data = request.get_json()
    
    # Disallow stock manual updates from here to enforce ledger (but fallback logic added)
    for k, v in data.items():
        if hasattr(Frame, k) and k not in ['id', 'stock']:
            setattr(frame, k, v)
            
    db.session.commit()
    return jsonify(frame.to_dict()), 200

@inventory_bp.route('/frames/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_frame(id):
    frame = Frame.query.get_or_404(id)
    db.session.delete(frame)
    db.session.commit()
    return jsonify({"message": "Frame deleted"}), 200

# --- LENSES ---
@inventory_bp.route('/lenses', methods=['GET'])
def get_lenses():
    query = Lens.query
    search = request.args.get('search')
    if search:
        st = f"%{search}%"
        query = query.filter(or_(Lens.lens_code.ilike(st), Lens.name.ilike(st)))
    return jsonify([l.to_dict() for l in query.all()]), 200

@inventory_bp.route('/lenses/<int:id>', methods=['GET'])
def get_lens(id):
    return jsonify(Lens.query.get_or_404(id).to_dict()), 200

@inventory_bp.route('/lenses', methods=['POST'])
@roles_required('admin')
def add_lens():
    data = request.get_json()
    if Lens.query.filter_by(lens_code=data.get('lens_code')).first():
        return jsonify({"message": "Lens code already exists"}), 409
        
    if not data.get('price'):
        data['price'] = data.get('selling_price') or 0.0
    lens = Lens(**{k: v for k, v in data.items() if hasattr(Lens, k) and k != 'id'})
    db.session.add(lens)
    db.session.commit()
    
    if lens.stock > 0:
        tx = InventoryTransaction(
            item_type='Lens', item_id=lens.id, transaction_type='Stock In',
            quantity=lens.stock, reason='Initial Stock', user_id=get_jwt_identity()
        )
        db.session.add(tx)
        db.session.commit()
        
    return jsonify(lens.to_dict()), 201

@inventory_bp.route('/lenses/<int:id>', methods=['PUT'])
@roles_required('admin')
def update_lens(id):
    lens = Lens.query.get_or_404(id)
    data = request.get_json()
    for k, v in data.items():
        if hasattr(Lens, k) and k not in ['id', 'stock']:
            setattr(lens, k, v)
    db.session.commit()
    return jsonify(lens.to_dict()), 200

@inventory_bp.route('/lenses/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_lens(id):
    lens = Lens.query.get_or_404(id)
    db.session.delete(lens)
    db.session.commit()
    return jsonify({"message": "Lens deleted"}), 200

# --- TRANSACTIONS ---
@inventory_bp.route('/transactions', methods=['POST'])
@roles_required('admin')
def adjust_stock():
    data = request.get_json()
    item_type = data.get('item_type') # Frame / Lens
    item_id = data.get('item_id')
    qty = int(data.get('quantity', 0))
    tx_type = data.get('transaction_type') # Stock In, Stock Out
    
    if item_type == 'Frame':
        item = Frame.query.get_or_404(item_id)
    elif item_type == 'Lens':
        item = Lens.query.get_or_404(item_id)
    else:
        return jsonify({"message": "Invalid item type"}), 400
        
    if tx_type == 'Stock Out' and item.stock < qty:
        return jsonify({"message": "Insufficient stock"}), 400
        
    if tx_type == 'Stock In':
        item.stock += qty
    else:
        item.stock -= qty
        
    tx = InventoryTransaction(
        item_type=item_type,
        item_id=item_id,
        transaction_type=tx_type,
        quantity=qty,
        reason=data.get('reason'),
        reference_number=data.get('reference_number'),
        user_id=get_jwt_identity()
    )
    db.session.add(tx)
    db.session.commit()
    
    return jsonify({"message": "Stock updated", "new_stock": item.stock}), 200

@inventory_bp.route('/transactions/<item_type>/<int:item_id>', methods=['GET'])
@roles_required('admin', 'staff')
def get_transactions(item_type, item_id):
    txs = InventoryTransaction.query.filter_by(item_type=item_type.capitalize(), item_id=item_id).order_by(InventoryTransaction.date.desc()).all()
    return jsonify([t.to_dict() for t in txs]), 200
