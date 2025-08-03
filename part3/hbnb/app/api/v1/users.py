from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.extensions import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity ,verify_jwt_in_request

api = Namespace('users', description='User operations')

# Define the user model for input validation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password', min_length=6),
})

@api.route('/')
class UserList(Resource):
    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Retrieve list of all users"""
        users = facade.get_all_users()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users], 200

@api.route('/<user_id>')
@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User retrieved')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

 
        data = api.payload
        email = data.get('email')
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        new_user = facade.update_user(user_id, data)
        if not new_user:
            return {"error": "User not found"}, 404

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'is_admin' : new_user.is_admin
            }, 200

@api.route('/')
class AdminUserCreate(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """Register a new admin"""
        users = facade.get_all_users()
        if not users:
            new_user = api.payload
            if new_user.get('is_admin')==False:
                return {'error': 'First user must be admin'}, 400
            new_user = facade.create_user(
            first_name=new_user['first_name'],
            last_name=new_user['last_name'],
            email=new_user['email'],
            password=new_user['password'],
            is_admin=new_user["is_admin"]
            )
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'is_admin' : new_user.is_admin
            }, 201
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        
        new_user = api.payload
        email = new_user.get('email')
        password = new_user.get('password')

        if not email or not password:
            return {'error': 'Email and password are required'}, 400

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(
            first_name=new_user['first_name'],
            last_name=new_user['last_name'],
            email=new_user['email'],
            password=new_user['password'],
            is_admin=new_user["is_admin"]
            )
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'is_admin' : new_user.is_admin
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400
