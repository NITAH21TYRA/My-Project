# Import necessary modules
from flask import Blueprint, request, jsonify
from app.models.review import Review
from app.extensions import db,bcrypt

review_bp = Blueprint('review_bp', __name__, url_prefix='/api/v1/reviews')

@review_bp.route('/reviews', methods=['POST'])
def add_review():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        required_fields = ['user_id', 'product_id', 'rating']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        review = Review(
            user_id=data['user_id'],
            product_id=data['product_id'],
            rating=data['rating'],
            comment=data.get('comment', '')
        )

        db.session.add(review)
        db.session.commit()

        return jsonify({"message": "Review added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@review_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        review = Review.query.get_or_404(review_id)
        if 'rating' in data:
            review.rating = data['rating']
        if 'comment' in data:
            review.comment = data['comment']

        db.session.commit()

        return jsonify({"message": "Review updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@review_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    try:
        review = Review.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()

        return jsonify({"message": "Review deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@review_bp.route('/products/<int:product_id>/reviews', methods=['GET'])
def get_reviews_for_product(product_id):
    try:
        reviews = Review.query.filter_by(product_id=product_id).all()
        reviews_list = [{
            'id': review.id,
            'user_id': review.user_id,
            'product_id': review.product_id,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at,
            'updated_at': review.updated_at
        } for review in reviews]
        return jsonify(reviews_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
