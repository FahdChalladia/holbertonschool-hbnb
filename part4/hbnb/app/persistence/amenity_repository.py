from app.models.amenity import Amenity
from app.extensions import  db
from app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)