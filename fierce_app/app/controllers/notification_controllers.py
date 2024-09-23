from flask import Blueprint, request, jsonify
from app.extensions import db, mail
from flask_mail import Message

notification_bp = Blueprint('notification_bp', __name__, url_prefix='/api/v1/notifications')


@notification_bp.route('/send-email', methods=['POST'])
def send_email_notification():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    # Extract client details and cart items from request data
    client_details = data.get('client')
    cart_items = data.get('cartItems')

    # Prepare email message
    msg = Message(subject="New Order Notification",
                  recipients=["anitahnansa@gmail.com"],  # Replace with admin's email address
                  body=f"New order received from {client_details['name']} at {client_details['address']}. \n\nItems:\n" +
                       '\n'.join([f"- {item['name']} - ${item['price']}" for item in cart_items]))

    # Send email
    try:
        mail.send(msg)
        return jsonify({"message": "Email notification sent successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Failed to send email notification: {str(e)}"}), 500
