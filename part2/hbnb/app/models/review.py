from .base import BaseModel

class Review(BaseModel):
    """Review class representing user reviews of places"""
    
    def __init__(self, *args, **kwargs):
        """Initialize Review instance"""
        super().__init__(*args, **kwargs)
        self.place_id = kwargs.get('place_id', '')
        self.user_id = kwargs.get('user_id', '')
        self.text = kwargs.get('text', '')
        
        # Validate required fields
        if not self.place_id:
            raise ValueError("place_id is required")
        if not self.user_id:
            raise ValueError("user_id is required")
        if not self.text:
            raise ValueError("text is required")
    
    def to_dict(self):
        """Return dictionary representation with extended attributes"""
        result = super().to_dict()
        # Add user details if available
        user = hbnb_facade.get(User, self.user_id)
        if user:
            result['user'] = {
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        return result
