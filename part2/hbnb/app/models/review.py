from typing import Optional
from . import BaseModel
from .user import User
from .place import Place

class Review(BaseModel):
    """Review model with relationships"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text: str = kwargs.get('text', '')
        self.rating: int = kwargs.get('rating', 0)
        self._place: Optional[Place] = None
        self._user: Optional[User] = None
        
        if 'place' in kwargs:
            self.place = kwargs['place']
        if 'user' in kwargs:
            self.user = kwargs['user']

    # Relationship Methods
    @property
    def place(self) -> Optional[Place]:
        return self._place

    @place.setter
    def place(self, place: Place):
        if self._place is not None:
            self._place._reviews.remove(self)
        self._place = place
        place.add_review(self)
        self.save()

    @property
    def user(self) -> Optional[User]:
        return self._user

    @user.setter
    def user(self, user: User):
        if self._user is not None:
            self._user._reviews.remove(self)
        self._user = user
        user.add_review(self)
        self.save()*
