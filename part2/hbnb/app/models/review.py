import uuid
from datetime import datetime
from typing import Optional
from .user import User
from .place import Place

class Review:
    """Review model for HBnB application"""
    
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Required attributes with validation
        self.text = kwargs.get('text', '')
        self.rating = kwargs.get('rating', 0)
        self.place = kwargs.get('place')
        self.user = kwargs.get('user')
        
        # Validate fields
        if not self.text:
            raise ValueError("Review text is required")
        if not 1 <= self.rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        if not isinstance(self.place, Place):
            raise ValueError("Place must be a valid Place instance")
        if not isinstance(self.user, User):
            raise ValueError("User must be a valid User instance")

    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Convert review to dictionary"""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id,
            'user_id': self.user.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            '__class__': self.__class__.__name__
        }
