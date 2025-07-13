from flask_restx import Namespace, Resource, fields
from app.persistence.facade import hbnb_facade
from app.business_logic.user import User

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.String(readonly=True, description='User identifier'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Update date')
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """Get all users"""
        return hbnb_facade.get_all(User), 200

    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = api.payload
        user = hbnb_facade.create(User, **data)
        return user, 201

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get user by ID"""
        user = hbnb_facade.get(User, user_id)
        if not user:
            api.abort(404, "User not found")
        return user, 200

    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update user information"""
        data = api.payload
        user = hbnb_facade.update(User, user_id, **data)
        if not user:
            api.abort(404, "User not found")
        return user, 200
