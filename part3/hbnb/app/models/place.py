from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("Title is required and must be <= 100 characters.")
        if price <= 0:
            raise ValueError("Price must be positive.")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180 and 180.")

        self.title = title
        self.description = description or ""
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)
    
    def to_dict(self, include_owner=False, include_amenities=False):
        data = {
            'id': self.id,
            'name': self.title
        }

        if include_owner and self.owner_id:
            data['owner'] = self.owner_id.to_dict() if hasattr(self.owner_id, 'to_dict') else str(self.owner_id)

        if include_amenities:
            data['amenities'] = [a.to_dict() if hasattr(a, 'to_dict') else str(a) for a in self.amenities]

        return data

