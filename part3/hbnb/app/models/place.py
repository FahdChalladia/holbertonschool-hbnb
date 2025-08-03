import re
from app.models.base_model import BaseModel , db , Base
from sqlalchemy.orm import validates ,relationship

class Place(BaseModel):
    __tablename__ = 'places'

    

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    owner = relationship('User', back_populates='places')
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        self.title = title
        self.description = description or ""
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

    @validates('title')
    def validate_title(self, key, title):
        if not title or len(title) > 100:
            raise ValueError("Title is required and must be <= 100 characters.")
        return title

    @validates('price')
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError("Price must be positive.")
        return price

    @validates('latitude')
    def validate_latitude(self, key, latitude):
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90 and 90.")
        return latitude

    @validates('longitude')
    def validate_longitude(self, key, longitude):
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180 and 180.")
        return longitude

    def to_dict(self, include_owner=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

        if include_owner:
            data['owner'] = self.owner_id

        return data
