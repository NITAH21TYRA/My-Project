from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS
# Create SQLAlchemy instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    # Load configuration from object
    app.config.from_object('config.Config')  # Update this line

    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)

    # Initialize JWTManager
    
    #importing models
    from app.models import notification
    from app.models import order
    from app.models import product
    from app.models import user
    from app.models import review
    from app.models import wishlist


    # Import blueprints
    from app.controllers.notification_controllers import notification_bp
    from app.controllers.order_controllers import order_bp
    from app.controllers.product_controllers import product_bp
    from app.controllers.review_controllers import review_bp
    from app.controllers.user_controllers import user_bp
    from app.controllers.wishlist_controllers import wishlist_bp

    # Register blueprints
    app.register_blueprint(notification_bp, url_prefix='/api/v1/notification')
    app.register_blueprint(order_bp, url_prefix='/api/v1/order')
    app.register_blueprint(product_bp, url_prefix='/api/v1/product')
    app.register_blueprint(review_bp, url_prefix='/api/v1/review')
    app.register_blueprint(user_bp, url_prefix='/api/v1/user')
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
