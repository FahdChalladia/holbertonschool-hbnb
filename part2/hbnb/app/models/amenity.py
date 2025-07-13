from uuid import uuid4

class Amenity:
    def __init__(self, name, id=None):
        self.id = id or str(uuid4())
        self.name = name
