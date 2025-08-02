from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()

        if not text:
            raise ValueError("Review text is required.")
        if rating not in range(1, 6):
            raise ValueError("Rating must be between 1 and 5.")
        if not place_id:
            raise ValueError("place_id is required.")
        if not user_id:
            raise ValueError("user_id is required.")

        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def to_dict(self):
            return {
                "id": self.id,
                "text": self.text,
                "rating": self.rating,
                "place_id": self.place_id,
                "user_id": self.user_id,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()
            }
