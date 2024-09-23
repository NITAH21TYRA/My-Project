from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extensions import bcrypt, db

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    address = Column(String(200), nullable=True)
    phone_number = Column(String(20), nullable=True)
    role = Column(String(20), default='customer')  # Role can be 'customer' or 'admin'
    is_admin = Column(Boolean, default=False)  # Boolean to check if the user is an admin
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships (assuming you have other models like Order, Review, Wishlist, Notification)
    orders = relationship('Order', back_populates='user')
    reviews = relationship('Review', back_populates='user')
    wishlists = relationship('Wishlist', back_populates='user')
    notifications = relationship('Notification', back_populates='user')

    def __init__(self, name, email, password, role='customer', phone_number=None, address=None, is_admin=False):
        self.name = name
        self.email = email
        self.set_password(password)  # Use bcrypt to hash the password
        self.role = role
        self.phone_number = phone_number
        self.address = address
        self.is_admin = is_admin

    def set_password(self, password):
        """Hash the user's password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verify the user's password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_full_name(self):
        """Return the full name of the user."""
        return self.name

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, role={self.role})>"

    @staticmethod
    def create_user(name, email, password, role='customer', phone_number=None, address=None, is_admin=False):
        """Create a new user in the system."""
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"error": "Email already exists"}, 400
        
        # Create and save a new user
        new_user = User(name=name, email=email, password=password, role=role, phone_number=phone_number, address=address, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 20