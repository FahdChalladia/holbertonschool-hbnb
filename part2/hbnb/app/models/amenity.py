import uuid
from datetime import datetime

class Amenity:
    """Amenity model for HBnB application"""
    
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Required attribute with validation
        self.name = kwargs.get('name', '')
        
        if not self.name or len(self.name) > 50:
            raise ValueError("Name is required and must be 50 characters or less")

    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Convert amenity to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            '__class__': self.__class__.__name__
        }
