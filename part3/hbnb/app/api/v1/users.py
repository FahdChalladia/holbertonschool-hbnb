from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.extensions import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password'],  # EN CLAIR
            is_admin=False
        )
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

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
        current_user_id = get_jwt_identity()  # c’est une string !
        is_admin = False  # par défaut

        # Optionnel : tu peux retrouver l'objet User
        current_user = facade.get_user(current_user_id)
        if current_user and getattr(current_user, "is_admin", False):
            is_admin = True

        # Vérifie droits
        if not is_admin and current_user_id != user_id:
            return {"error": "Unauthorized action"}, 403

        data = request.get_json()

        if not is_admin and ("email" in data or "password" in data):
            return {"error": "You cannot modify email or password"}, 400

        if is_admin and "email" in data:
            existing_user = facade.get_user_by_email(data["email"])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        updated_user = facade.update_user(user_id, data)
        if not updated_user:
            return {"error": "User not found"}, 404

        return updated_user.to_dict(), 200

@api.route('/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')
        password = user_data.get('password')

        if not email or not password:
            return {'error': 'Email and password are required'}, 400

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        # Créer le nouvel utilisateur via la facade
        try:
            new_user = facade.create_user(user_data)
            return new_user, 201
        except Exception as e:
            return {'error': str(e)}, 400
