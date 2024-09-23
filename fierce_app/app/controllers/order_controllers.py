from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_mail import Message
from app.models.order import Order
from app.models.product import Product
from app.models.notification import Notification
from app.models.admin import Admin
from app.extensions import db, mail
import logging

order_bp = Blueprint('order_bp', __name__, url_prefix='/api/v1/orders')

# Create a new order and notify the admin via email
@order_bp.route('/', methods=['POST'])
@jwt_required()  # Requires authentication
def create_order():
    try:
        current_user_id = get_jwt_identity()

        data = request.json
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not product_id or not quantity:
            return jsonify({'error': 'Product ID and quantity are required'}), 400

        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        total_price = product.price * quantity

        # Create the new order
        new_order = Order(
            user_id=current_user_id,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price
        )
        db.session.add(new_order)
        db.session.commit()

        # Send notification email to the admin
        try:
            admin_email = "admin@example.com"  # Replace with the actual admin email or fetch from the DB
            msg = Message(
                subject="New Order Created",
                recipients=[admin_email],
                html=generate_order_email_body(new_order)
            )
            mail.send(msg)
        except Exception as mail_error:
            logging.error(f"Failed to send email: {mail_error}")

        # Create a new notification
        notification = Notification(
            user_id=current_user_id,
            message=f"Your order with ID {new_order.id} has been created successfully."
        )
        db.session.add(notification)
        db.session.commit()

        return jsonify({
            'message': 'Order created successfully',
            'order': {
                'id': new_order.id,
                'user_id': new_order.user_id,
                'product_id': new_order.product_id,
                'quantity': new_order.quantity,
                'total_price': new_order.total_price,
                'status': new_order.status,
                'created_at': new_order.created_at,
                'updated_at': new_order.updated_at
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error processing order: {e}")
        return jsonify({'error': str(e)}), 500

def generate_order_email_body(order):
    return f"""
    <html>
    <body>
        <h1>New Order Created</h1>
        <p><strong>Order ID:</strong> {order.id}</p>
        <p><strong>User ID:</strong> {order.user_id}</p>
        <p><strong>Product ID:</strong> {order.product_id}</p>
        <p><strong>Quantity:</strong> {order.quantity}</p>
        <p><strong>Total Price:</strong> ${order.total_price}</p>
        <p><strong>Status:</strong> {order.status}</p>
        <p><strong>Created At:</strong> {order.created_at}</p>
        <p><strong>Updated At:</strong> {order.updated_at}</p>
    </body>
    </html>
    """
