from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db

class Wishlist(db.Model):
    __tablename__ = 'wishlists'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    product = relationship('Product', back_populates='wishlists')
    user = relationship('User', back_populates='wishlists')

    def __repr__(self):
        return f"<Wishlist(id={self.id}, product_id={self.product_id}, user_id={self.user_id})>"

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id
        }
