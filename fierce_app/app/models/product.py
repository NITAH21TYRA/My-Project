# app/models/product.py

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db

class Product(db.Model):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    image = Column(String(500), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    admin_id = Column(Integer, ForeignKey('admins.id'))  # Foreign key to Admin
    admin = relationship('Admin', back_populates='products')
    
    reviews = relationship('Review', back_populates='product')
    wishlists = relationship('Wishlist', back_populates='product')
    orders = relationship('Order', back_populates='product')

    def __repr__(self):
        return f"<Product(id={self.id}, image={self.image}, name={self.name}, price={self.price}, stock={self.stock})>"
