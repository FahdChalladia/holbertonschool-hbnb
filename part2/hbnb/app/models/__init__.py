import uuid
from datetime import datetime
from typing import Any, Dict

class BaseModel:
    """Base class with core functionality"""
    def __init__(self, *args, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key != '__class__':
                    setattr(self, key, value)
    
    def save(self):
        """Updates updated_at timestamp"""
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Converts instance to dictionary"""
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
    
    def __str__(self):
        """String representation"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"