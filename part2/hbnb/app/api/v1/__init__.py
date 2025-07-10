from flask_restx import Api
from .users import api as users_ns

api = Api(
    title='HBnB API',
    version='1.0',
    description='API for HBnB clone application',
    doc='/docs'
)

api.add_namespace(users_ns, path='/users')
