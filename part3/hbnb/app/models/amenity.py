import re
from sqlalchemy.orm import validates , relationship
from app.models.base_model import BaseModel ,db 

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)
    def __init__(self, name):
        self.name = name

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) > 50:
            raise ValueError("Amenity name is required and must be <= 50 characters.")
        return name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
