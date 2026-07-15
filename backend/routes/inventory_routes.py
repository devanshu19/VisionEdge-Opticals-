from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Product

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/', methods=['GET'])
@jwt_required()
def get_products():
    category = request.args.get('category')
    query = Product.query
    
    if category and category != 'all':
        query = query.filter_by(category=category)
        
    products = query.all()
    return jsonify([p.to_dict() for p in products]), 200

@inventory_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict()), 200

@inventory_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    
    required_fields = ['item_code', 'name', 'category', 'price']
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required field: {field}"}), 400
            
    if Product.query.filter_by(item_code=data['item_code']).first():
        return jsonify({"message": "Item code already exists"}), 400
        
    new_product = Product(
        item_code=data['item_code'],
        name=data['name'],
        category=data['category'],
        brand=data.get('brand'),
        stock=data.get('stock', 0),
        price=float(data['price'])
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({"message": "Product created successfully", "product": new_product.to_dict()}), 201

@inventory_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data: product.name = data['name']
    if 'category' in data: product.category = data['category']
    if 'brand' in data: product.brand = data['brand']
    if 'stock' in data: product.stock = int(data['stock'])
    if 'price' in data: product.price = float(data['price'])
    
    db.session.commit()
    return jsonify({"message": "Product updated successfully", "product": product.to_dict()}), 200

@inventory_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200
