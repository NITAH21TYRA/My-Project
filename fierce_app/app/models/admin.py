# app/models/admin.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.extensions import db, bcrypt

class Admin(db.Model):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=db.func.current_timestamp())
    updated_at = Column(DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    products = relationship('Product', back_populates='admin')
    orders = relationship('Order', back_populates='admin')
    

    def __repr__(self):
        return f"<Admin(id={self.id}, email={self.email})>"

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
