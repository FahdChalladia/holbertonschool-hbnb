from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository
from app.models.place import Place

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
    
    def create_review(self, review_data):
        text = review_data.get('text')
        rating = review_data.get('rating')
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        if not all([text, rating, user_id, place_id]):
            raise ValueError("All fields (text, rating, user_id, place_id) are required")

        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        user = User.get(user_id)
        if not user:
            raise ValueError("User does not exist")

        place = Place.get(place_id)
        if not place:
            raise ValueError("Place does not exist")

        review = Review(text=text, rating=rating, user_id=user_id, place_id=place_id)
        review.save()
        return review

    def get_review(self, review_id):
        review = Review.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return review

    def get_all_reviews(self):
        return Review.all()

    def get_reviews_by_place(self, place_id):
        place = Place.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return [r for r in Review.all() if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = Review.get(review_id)
        if not review:
            raise ValueError("Review not found")

        text = review_data.get("text")
        rating = review_data.get("rating")

        if text:
            review.text = text
        if rating:
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5")
            review.rating = rating

        review.save()
        return review

    def delete_review(self, review_id):
        review = Review.get(review_id)
        if not review:
            raise ValueError("Review not found")
        review.delete()
        return True
