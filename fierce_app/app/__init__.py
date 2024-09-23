from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS
from app.extensions import db, bcrypt

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load configuration from object
    app.config.from_object('config.Config')

    # Set up the JWT secret key
    app.config['JWT_SECRET_KEY'] = '12345'

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)  # Initialize JWTManager here

    # Import and register models
    from app.models.user import User
    from app.models.product import Product
    from app.models.order import Order
    from app.models.wishlist import Wishlist
    from app.models.review import Review
    from app.models.notification import Notification
    from app.models.admin import Admin  # Ensure this import is here to register the model

    # Import and register blueprints
    from app.controllers.notification_controllers import notification_bp
    from app.controllers.order_controllers import order_bp
    from app.controllers.product_controllers import product_bp
    from app.controllers.review_controllers import review_bp
    from app.controllers.user_controllers import user  # Ensure consistent naming
    from app.controllers.wishlist_controllers import wishlist_bp
    from app.controllers.admin_controller import admin_bp

    # Register blueprints with url_prefix
    app.register_blueprint(notification_bp, url_prefix='/api/v1/notifications')
    app.register_blueprint(order_bp, url_prefix='/api/v1/orders')
    app.register_blueprint(product_bp, url_prefix='/api/v1/products')
    app.register_blueprint(review_bp, url_prefix='/api/v1/reviews')
    app.register_blueprint(user, url_prefix='/api/v1/user')  # Corrected url_prefix to 'users'
    app.register_blueprint(wishlist_bp, url_prefix='/api/v1/wishlist')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

    @app.route('/')
    def home():
        return "WELCOME TO FIERCE JEWELLERY & ACCESSORIES"

    # Routes for protected resources
    @app.route('/protected')
    @jwt_required()
    def protected():
        current_user_id = get_jwt_identity()
        return jsonify(logged_in_as=current_user_id), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
