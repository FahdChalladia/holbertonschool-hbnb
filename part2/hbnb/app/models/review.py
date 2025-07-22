from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()

        if not text:
            raise ValueError("Review text is required.")
        if rating not in range(1, 6):
            raise ValueError("Rating must be between 1 and 5.")

        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
        