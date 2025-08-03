import re
from app.extensions import bcrypt , db
from app.models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import validates ,relationship


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    places = relationship('Place', back_populates='owner')
    reviews = relationship("Review", back_populates="author")
    
    def __init__(self, first_name, last_name, email, password , is_admin):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required and must be <= 50 characters.")
        return first_name

    @validates('last_name')
    def validate_last_name(self, key, last_name):
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and must be <= 50 characters.")
        return last_name

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email is invalid.")
        return email