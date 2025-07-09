from typing import List
from . import BaseModel
from .place import Place

class Amenity(BaseModel):
    """Amenity model with relationships"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name: str = kwargs.get('name', '')
        self._places: List[Place] = []

    # Relationship Methods
    @property
    def places(self) -> List[Place]:
        return self._places

    def add_place(self, place: Place):
        if place not in self._places:
            self._places.append(place)
            if self not in place.amenities:
                place.add_amenity(self)
            self.save()

    def remove_place(self, place: Place):
        if place in self._places:
            self._places.remove(place)
            if self in place.amenities:
                place.remove_amenity(self)
            self.save()
