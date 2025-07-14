from flask_restx import Api

api = Api(
    title='HBnB API',
    version='1.0',
    description='HBnB Application API',
    doc='/api/v1/'
)

from app.api.v1.places import api as place_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.users import api as users_ns

api.add_namespace(place_ns, path='/api/v1/places')
api.add_namespace(reviews_ns, path='/api/v1/reviews')
api.add_namespace(users_ns, path='/api/v1/users')