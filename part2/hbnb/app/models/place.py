from typing import List, Optional
from . import BaseModel
from .user import User
from .review import Review
from .amenity import Amenity

class Place(BaseModel):
    """Place model with relationships"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title: str = kwargs.get('title', '')
        self.description: str = kwargs.get('description', '')
        self.price: float = kwargs.get('price', 0.0)
        self.latitude: float = kwargs.get('latitude', 0.0)
        self.longitude: float = kwargs.get('longitude', 0.0)
        self._owner: Optional[User] = None
        self._reviews: List[Review] = []
        self._amenities: List[Amenity] = []
        
        if 'owner' in kwargs:
            self.owner = kwargs['owner']

    # Relationship Methods
    @property
    def owner(self) -> Optional[User]:
        return self._owner

    @owner.setter
    def owner(self, user: User):
        if self._owner is not None:
            self._owner._places.remove(self)
        self._owner = user
        user.add_place(self)
        self.save()

    @property
    def reviews(self) -> List[Review]:
        return self._reviews

    def add_review(self, review: Review):
        if review not in self._reviews:
            self._reviews.append(review)
            if review.place != self:
                review.place = self
            self.save()

    @property
    def amenities(self) -> List[Amenity]:
        return self._amenities

    def add_amenity(self, amenity: Amenity):
        if amenity not in self._amenities:
            self._amenities.append(amenity)
            amenity.add_place(self)
            self.save()

    def remove_amenity(self, amenity: Amenity):
        if amenity in self._amenities:
            self._amenities.remove(amenity)
            amenity.remove_place(self)
            self.save()
