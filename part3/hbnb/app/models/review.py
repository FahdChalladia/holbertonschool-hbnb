import re
from app.extensions import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)

    def __init__(self, text, rating, place_id, user_id):
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
    def save(self):
        from app import db
        self.db = db
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @validates('text')
    def validate_text(self, key, text):
        if not text or len(text.strip()) == 0:
            raise ValueError("Review text is required.")
        if len(text) > 500:
            raise ValueError("Review text must be less than 500 characters.")
        return text

    @validates('rating')
    def validate_rating(self, key, rating):
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5.")
        return rating

    @validates('place_id')
    def validate_place_id(self, key, place_id):
        if not place_id or len(place_id) != 36:
            raise ValueError("place_id is required and must be a valid UUID.")
        return place_id

    @validates('user_id')
    def validate_user_id(self, key, user_id):
        if not user_id or len(user_id) != 36:
            raise ValueError("user_id is required and must be a valid UUID.")
        return user_id

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
