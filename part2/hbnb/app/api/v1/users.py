from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBNBFacade
from app.persistence.repository import Repository

api = Namespace('users', description='User operations')

# API Models
user_model = api.model('User', {
    'id': fields.String(readonly=True, description='User identifier'),
    'first_name': fields.String(required=True, description='First name', max_length=50),
    'last_name': fields.String(required=True, description='Last name', max_length=50),
    'email': fields.String(required=True, description='Email address'),
    'is_admin': fields.Boolean(description='Admin status', default=False),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Last update date')
})

facade = HBNBFacade(Repository())

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        users = facade.get_all_users()
        return [user for user in users], 200

    @api.doc('create_user')
    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = request.get_json()
        
        # Password would be handled here in a real implementation
        if 'password' in data:
            del data['password']  # Don't store raw password
        
        user = facade.create_user(data)
        return user, 201

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get a specific user"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user, 200

    @api.doc('update_user')
    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update a user"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        
        data = request.get_json()
        
        # Never update password via this endpoint
        if 'password' in data:
            del data['password']
        
        facade.update_user(user_id, data)
        return facade.get_user(user_id), 200
