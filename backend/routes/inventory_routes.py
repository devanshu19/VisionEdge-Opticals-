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

# --- ALL INVENTORY (UNIFIED REALTIME QUERY) ---
@inventory_bp.route('/items', methods=['GET'])
def get_all_items():
    frames = [f.to_dict() for f in Frame.query.order_by(Frame.id.desc()).all()]
    lenses = [l.to_dict() for l in Lens.query.order_by(Lens.id.desc()).all()]
    return jsonify({
        "frames": frames,
        "lenses": lenses,
        "all": frames + lenses,
        "total": len(frames) + len(lenses)
    }), 200

# --- FRAMES ---
@inventory_bp.route('/frames', methods=['GET'])
def get_frames():
    query = Frame.query
    search = request.args.get('search')
    category = request.args.get('category')
    if search:
        st = f"%{search}%"
        query = query.filter(or_(Frame.frame_code.ilike(st), Frame.name.ilike(st), Frame.brand.ilike(st)))
    if category and category.lower() != 'all':
        query = query.filter(Frame.category.ilike(f"%{category}%"))
    return jsonify([f.to_dict() for f in query.order_by(Frame.id.desc()).all()]), 200

@inventory_bp.route('/frames/<int:id>', methods=['GET'])
def get_frame(id):
    return jsonify(Frame.query.get_or_404(id).to_dict()), 200

@inventory_bp.route('/frames', methods=['POST'])
@roles_required('admin', 'staff')
def add_frame():
    data = request.get_json() or {}
    
    # Resolve Brand name
    brand = data.get('brand') or data.get('brand_name')
    if not brand and data.get('brand_id'):
        b = Brand.query.get(data['brand_id'])
        if b: brand = b.name
    brand = brand or "VisionEdge"

    # Resolve Category name
    category = data.get('category') or data.get('category_name')
    if not category and data.get('category_id'):
        c = Category.query.get(data['category_id'])
        if c: category = c.name
    category = category or "Eyeglasses"

    # Frame Code (auto-generate if blank)
    code = (data.get('frame_code') or '').strip()
    if not code:
        code = f"FRM-{uuid.uuid4().hex[:6].upper()}"
    elif Frame.query.filter_by(frame_code=code).first():
        code = f"{code}-{uuid.uuid4().hex[:4].upper()}"

    name = (data.get('name') or data.get('model') or f"{brand} {category}").strip()
    model = (data.get('model') or name).strip()
    
    selling_price = float(data.get('selling_price') or data.get('price') or 999.0)
    price = float(data.get('price') or selling_price)
    stock = int(data.get('stock') or 0)
    min_stock = int(data.get('min_stock') or 5)

    frame = Frame(
        frame_code=code,
        name=name,
        model=model,
        brand=brand,
        category=category,
        shape=data.get('shape') or 'Rectangle',
        material=data.get('material') or 'Acetate',
        color=data.get('color') or 'Black',
        size=data.get('size') or 'Medium',
        gender=data.get('gender') or 'Unisex',
        price=price,
        selling_price=selling_price,
        stock=stock,
        min_stock=min_stock,
        image=data.get('image') or '',
        vto_image=data.get('vto_image') or '',
        status=data.get('status') or 'Available'
    )
    db.session.add(frame)
    db.session.commit()
    
    # Log initial stock if > 0
    if frame.stock > 0:
        try:
            tx = InventoryTransaction(
                item_type='Frame', item_id=frame.id, transaction_type='Stock In',
                quantity=frame.stock, reason='Initial Stock', user_id=get_jwt_identity()
            )
            db.session.add(tx)
            db.session.commit()
        except Exception:
            db.session.rollback()
        
    return jsonify({"message": "Frame created successfully", "frame": frame.to_dict()}), 201

@inventory_bp.route('/frames/<int:id>', methods=['PUT'])
@roles_required('admin', 'staff')
def update_frame(id):
    frame = Frame.query.get_or_404(id)
    data = request.get_json() or {}
    
    # Brand & Category resolution
    if 'brand' in data and data['brand']:
        frame.brand = data['brand']
    elif 'brand_id' in data and data['brand_id']:
        b = Brand.query.get(data['brand_id'])
        if b: frame.brand = b.name

    if 'category' in data and data['category']:
        frame.category = data['category']
    elif 'category_id' in data and data['category_id']:
        c = Category.query.get(data['category_id'])
        if c: frame.category = c.name

    if 'name' in data and data['name']:
        frame.name = data['name'].strip()
    if 'model' in data and data['model']:
        frame.model = data['model'].strip()
    if 'shape' in data: frame.shape = data['shape']
    if 'material' in data: frame.material = data['material']
    if 'color' in data: frame.color = data['color']
    if 'size' in data: frame.size = data['size']
    if 'gender' in data: frame.gender = data['gender']
    if 'status' in data: frame.status = data['status']
    if 'image' in data: frame.image = data['image']
    if 'vto_image' in data: frame.vto_image = data['vto_image']
    if 'min_stock' in data and data['min_stock'] is not None:
        frame.min_stock = int(data['min_stock'])
    if 'stock' in data and data['stock'] is not None:
        frame.stock = int(data['stock'])
        
    if 'selling_price' in data and data['selling_price'] is not None:
        frame.selling_price = float(data['selling_price'])
        if 'price' not in data or not data['price']:
            frame.price = frame.selling_price
    if 'price' in data and data['price'] is not None:
        frame.price = float(data['price'])
        if 'selling_price' not in data or not data['selling_price']:
            frame.selling_price = frame.price
            
    db.session.commit()
    return jsonify({"message": "Frame updated successfully", "frame": frame.to_dict()}), 200

@inventory_bp.route('/frames/<int:id>', methods=['DELETE'])
@roles_required('admin', 'staff')
def delete_frame(id):
    frame = Frame.query.get_or_404(id)
    try:
        InventoryTransaction.query.filter_by(item_type='Frame', item_id=frame.id).delete()
    except Exception:
        pass
    db.session.delete(frame)
    db.session.commit()
    return jsonify({"message": "Frame deleted successfully", "id": id}), 200

# --- LENSES ---
@inventory_bp.route('/lenses', methods=['GET'])
def get_lenses():
    query = Lens.query
    search = request.args.get('search')
    if search:
        st = f"%{search}%"
        query = query.filter(or_(Lens.lens_code.ilike(st), Lens.name.ilike(st), Lens.brand.ilike(st)))
    return jsonify([l.to_dict() for l in query.order_by(Lens.id.desc()).all()]), 200

@inventory_bp.route('/lenses/<int:id>', methods=['GET'])
def get_lens(id):
    return jsonify(Lens.query.get_or_404(id).to_dict()), 200

@inventory_bp.route('/lenses', methods=['POST'])
@roles_required('admin', 'staff')
def add_lens():
    data = request.get_json() or {}
    
    brand = data.get('brand') or data.get('brand_name')
    if not brand and data.get('brand_id'):
        b = Brand.query.get(data['brand_id'])
        if b: brand = b.name
    brand = brand or "VisionEdge"

    code = (data.get('lens_code') or '').strip()
    if not code:
        code = f"LNS-{uuid.uuid4().hex[:6].upper()}"
    elif Lens.query.filter_by(lens_code=code).first():
        code = f"{code}-{uuid.uuid4().hex[:4].upper()}"

    lens_type = data.get('lens_type') or data.get('type') or 'Single Vision'
    name = (data.get('name') or f"{brand} {lens_type}").strip()
    
    selling_price = float(data.get('selling_price') or data.get('price') or 899.0)
    price = float(data.get('price') or selling_price)
    stock = int(data.get('stock') or 0)
    min_stock = int(data.get('min_stock') or 10)

    lens = Lens(
        lens_code=code,
        name=name,
        brand=brand,
        category=data.get('category') or 'Contact & Optical Lenses',
        type=lens_type,
        lens_type=lens_type,
        coating=data.get('coating') or 'Anti-Reflective',
        price=price,
        selling_price=selling_price,
        stock=stock,
        min_stock=min_stock,
        image=data.get('image') or '',
        status=data.get('status') or 'Available'
    )
    db.session.add(lens)
    db.session.commit()
    
    if lens.stock > 0:
        try:
            tx = InventoryTransaction(
                item_type='Lens', item_id=lens.id, transaction_type='Stock In',
                quantity=lens.stock, reason='Initial Stock', user_id=get_jwt_identity()
            )
            db.session.add(tx)
            db.session.commit()
        except Exception:
            db.session.rollback()
        
    return jsonify({"message": "Lens created successfully", "lens": lens.to_dict()}), 201

@inventory_bp.route('/lenses/<int:id>', methods=['PUT'])
@roles_required('admin', 'staff')
def update_lens(id):
    lens = Lens.query.get_or_404(id)
    data = request.get_json() or {}
    
    if 'brand' in data and data['brand']:
        lens.brand = data['brand']
    elif 'brand_id' in data and data['brand_id']:
        b = Brand.query.get(data['brand_id'])
        if b: lens.brand = b.name

    if 'name' in data and data['name']: lens.name = data['name'].strip()
    if 'type' in data and data['type']:
        lens.type = data['type']
        lens.lens_type = data['type']
    if 'lens_type' in data and data['lens_type']:
        lens.lens_type = data['lens_type']
        lens.type = data['lens_type']
    if 'category' in data and data['category']: lens.category = data['category']
    if 'coating' in data: lens.coating = data['coating']
    if 'status' in data: lens.status = data['status']
    if 'image' in data: lens.image = data['image']
    if 'min_stock' in data and data['min_stock'] is not None:
        lens.min_stock = int(data['min_stock'])
    if 'stock' in data and data['stock'] is not None:
        lens.stock = int(data['stock'])
        
    if 'selling_price' in data and data['selling_price'] is not None:
        lens.selling_price = float(data['selling_price'])
        if 'price' not in data or not data['price']:
            lens.price = lens.selling_price
    if 'price' in data and data['price'] is not None:
        lens.price = float(data['price'])
        if 'selling_price' not in data or not data['selling_price']:
            lens.selling_price = lens.price

    db.session.commit()
    return jsonify({"message": "Lens updated successfully", "lens": lens.to_dict()}), 200

@inventory_bp.route('/lenses/<int:id>', methods=['DELETE'])
@roles_required('admin', 'staff')
def delete_lens(id):
    lens = Lens.query.get_or_404(id)
    try:
        InventoryTransaction.query.filter_by(item_type='Lens', item_id=lens.id).delete()
    except Exception:
        pass
    db.session.delete(lens)
    db.session.commit()
    return jsonify({"message": "Lens deleted successfully", "id": id}), 200

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
