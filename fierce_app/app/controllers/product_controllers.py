from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.product import Product
from app.models.admin import Admin
from app.extensions import db
from functools import wraps

product_bp = Blueprint('product_bp', __name__, url_prefix='/api/v1/products')

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = Admin.query.get(current_user_id)
        if not current_user or current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized access'}), 403
        return fn(*args, **kwargs)
    return wrapper

@product_bp.route('/', methods=['GET'])
def get_all_products():
    try:
        products = Product.query.all()
        serialized_products = [{
            'id': product.id,
            'image': product.image,
            'name': product.name,
            'price': product.price,
            'stock': product.stock,
            'created_at': product.created_at,
            'updated_at': product.updated_at
        } for product in products]
        return jsonify({'products': serialized_products}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@product_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_new_product():
    try:
        data = request.json
        required_fields = ['name', 'price', 'stock', 'image']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        product = Product(
            image=data['image'],
            name=data['name'],
            price=data['price'],
            stock=data['stock']
        )
        db.session.add(product)
        db.session.commit()

        serialized_product = {
            'id': product.id,
            'image': product.image,
            'name': product.name,
            'price': product.price,
            'stock': product.stock,
            'created_at': product.created_at,
            'updated_at': product.updated_at
        }
        return jsonify({
            'message': 'Product created successfully',
            'product': serialized_product
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_existing_product(product_id):
    try:
        data = request.json
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.stock = data.get('stock', product.stock)
        product.image = data.get('image', product.image)

        db.session.commit()

        serialized_product = {
            'id': product.id,
            'image': product.image,
            'name': product.name,
            'price': product.price,
            'stock': product.stock,
            'created_at': product.created_at,
            'updated_at': product.updated_at
        }
        return jsonify({
            'message': 'Product updated successfully',
            'product': serialized_product
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_existing_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_single_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        serialized_product = {
            'id': product.id,
            'image': product.image,
            'name': product.name,
            'price': product.price,
            'stock': product.stock,
            'created_at': product.created_at,
            'updated_at': product.updated_at
        }
        return jsonify(serialized_product), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
