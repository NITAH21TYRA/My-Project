from flask import Blueprint, request, jsonify
from app.extensions import bcrypt, db


wishlist_bp = Blueprint('wishlist_bp', __name__)

@wishlist_bp.route('/wishlists', methods=['POST'])
def add_to_wishlist():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    wishlist = Wishlist(
        user_id=data['user_id'],
        product_id=data['product_id']
    )

    db.session.add(wishlist)
    db.session.commit()

    return jsonify({"message": "Product added to wishlist"}), 201

@wishlist_bp.route('/wishlists/<int:wishlist_id>', methods=['DELETE'])
def remove_from_wishlist(wishlist_id):
    wishlist = Wishlist.query.get_or_404(wishlist_id)
    db.session.delete(wishlist)
    db.session.commit()
    return jsonify({"message": "Product removed from wishlist"}), 200

@wishlist_bp.route('/users/<int:user_id>/wishlists', methods=['GET'])
def get_wishlist_for_user(user_id):
    wishlists = Wishlist.query.filter_by(user_id=user_id).all()
    wishlist_list = [{
        'id': wishlist.id,
        'user_id': wishlist.user_id,
        'product_id': wishlist.product_id,
        'created_at': wishlist.created_at
    } for wishlist in wishlists]
    return jsonify(wishlist_list), 200
