from flask import Blueprint, request, jsonify
from app.extensions import db, bcrypt
from app.models.admin import Admin
from app.models.product import Product
from app.models.order import Order
import jwt
import datetime
from dateutil import parser  # Import dateutil parser
from functools import wraps  # Import wraps for decorator
from flask_cors import CORS

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/api/v1/admin')

# Define your secret key here or use an environment variable
SECRET_KEY = 'your_secret_key'

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        # Get the token from the Authorization header
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing"}), 403
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[len('Bearer '):]
        
        try:
            # Decode the token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = Admin.query.get(data['sub'])
            if not current_user:
                return jsonify({"message": "Invalid token"}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 403
        
        return f(current_user, *args, **kwargs)
    return decorator

@admin_bp.route('/register', methods=['POST'], endpoint='register_admin')
def register_admin():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    existing_admin = Admin.query.filter_by(email=email).first()
    if existing_admin:
        return jsonify({"message": "Admin already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_admin = Admin(email=email, password_hash=hashed_password)
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({"message": "Admin registered successfully"}), 201

@admin_bp.route('/login', methods=['POST'], endpoint='login_admin')
def login_admin():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    admin = Admin.query.filter_by(email=email).first()
    if not admin or not admin.check_password(password):
        return jsonify({"message": "Invalid email or password"}), 401

    # Generate JWT token
    token = jwt.encode({
        'sub': admin.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({"token": token}), 200

@admin_bp.route('/products', methods=['GET'], endpoint='get_products')
@token_required
def get_products(current_user):
    products = Product.query.all()
    products_list = []
    for product in products:
        created_at = product.created_at
        updated_at = product.updated_at

        # Handle conversion if created_at and updated_at are strings
        if isinstance(created_at, str):
            try:
                created_at = parser.isoparse(created_at)
            except ValueError:
                created_at = None
        
        if isinstance(updated_at, str):
            try:
                updated_at = parser.isoparse(updated_at)
            except ValueError:
                updated_at = None

        product_data = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'stock': product.stock,
            'image': product.image,
            'created_at': created_at.isoformat() if created_at else None,
            'updated_at': updated_at.isoformat() if updated_at else None
        }
        products_list.append(product_data)
    return jsonify(products=products_list), 200

@admin_bp.route('/product', methods=['POST'], endpoint='add_product')
@token_required
def add_product(current_user):
    data = request.json
    new_product = Product(
        name=data['name'],
        price=data['price'],
        stock=data['stock'],
        image=data['image'],
        admin_id=current_user.id
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully"}), 201

@admin_bp.route('/product/<int:product_id>', methods=['PUT'], endpoint='update_product')
@token_required
def update_product(current_user, product_id):
    data = request.json
    product = Product.query.get_or_404(product_id)
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    product.image = data.get('image', product.image)
    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200

@admin_bp.route('/product/<int:product_id>', methods=['DELETE'], endpoint='delete_product')
@token_required
def delete_product(current_user, product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200

@admin_bp.route('/orders', methods=['GET'], endpoint='get_orders')
@token_required
def get_orders(current_user):
    orders = Order.query.all()
    orders_list = []
    for order in orders:
        created_at = order.created_at
        updated_at = order.updated_at

        # Handle conversion if created_at and updated_at are strings
        if isinstance(created_at, str):
            try:
                created_at = parser.isoparse(created_at)
            except ValueError:
                created_at = None
        
        if isinstance(updated_at, str):
            try:
                updated_at = parser.isoparse(updated_at)
            except ValueError:
                updated_at = None

        order_data = {
            'id': order.id,
            'status': order.status,
            'created_at': created_at.isoformat() if created_at else None,
            'updated_at': updated_at.isoformat() if updated_at else None
        }
        orders_list.append(order_data)
    return jsonify(orders=orders_list), 200

@admin_bp.route('/order/<int:order_id>', methods=['PUT'], endpoint='update_order')
@token_required
def update_order(current_user, order_id):
    data = request.json
    order = Order.query.get_or_404(order_id)
    order.status = data.get('status', order.status)
    db.session.commit()
    return jsonify({"message": "Order updated successfully"}), 200

@admin_bp.route('/order/<int:order_id>', methods=['DELETE'], endpoint='delete_order')
@token_required
def delete_order(current_user, order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted successfully"}), 200
