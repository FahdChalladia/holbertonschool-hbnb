from app.models.review import Review
from app.extensions import  db
from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)