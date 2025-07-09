from typing import List, Optional
from . import BaseModel

class User(BaseModel):
    """User model with relationships"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first_name: str = kwargs.get('first_name', '')
        self.last_name: str = kwargs.get('last_name', '')
        self.email: str = kwargs.get('email', '')
        self.is_admin: bool = kwargs.get('is_admin', False)
        self._places: List['Place'] = []
        self._reviews: List['Review'] = []

    # Relationship Methods
    @property
    def places(self) -> List['Place']:
        return self._places

    @property
    def reviews(self) -> List['Review']:
        return self._reviews

    def add_place(self, place: 'Place'):
        if place not in self._places:
            if place.owner and place.owner != self:
                raise ValueError("Place already owned by another user")
            self._places.append(place)
            place.owner = self
            self.save()

    def add_review(self, review: 'Review'):
        if review not in self._reviews:
            self._reviews.append(review)
            if review.user != self:
                review.user = self
            self.save()
