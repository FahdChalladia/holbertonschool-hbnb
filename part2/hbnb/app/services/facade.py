from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.repositories import storage

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.all()

    def update_user(self, user_id, update_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        return user
    
    def create_amenity(self, amenity_data):
        if not amenity_data.get("name"):
            raise ValueError("Amenity name is required")
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        return amenity

    def create_place(self, place_data):
        try:
            place = Place(**place_data)
            storage.new(place)
            storage.save()
            return place
        except ValueError as e:
            raise ValueError(str(e))

    def get_place(self, place_id):
        place = storage.get(Place, place_id)
        if not place:
            return None
        return place

    def get_all_places(self):
        return storage.all(Place).values()

    def update_place(self, place_id, place_data):
        place = storage.get(Place, place_id)
        if not place:
            return None
        for key, value in place_data.items():
            if hasattr(place, key):
                setattr(place, key, value)
        storage.save()
        return place