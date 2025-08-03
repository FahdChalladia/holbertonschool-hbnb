from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import get_jwt

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Amenity identifier'),
    'name': fields.String(required=True, description='Amenity name'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Update date')
})


@api.route('/')
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()
        return amenities, 200
    
    @api.expect(amenity_model, validate=True)
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        amenity = api.payload
        name = amenity.get("name")
        if not name:
            return {'error': 'Amenity name is required'}, 400
        try:
            amenity = facade.create_amenity(
                name=amenity['name']
            )
            return api.marshal(amenity, amenity_model), 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity, 200
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        data = api.payload
        amenity = facade.update_amenity(amenity_id,data)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return {
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at.isoformat(),
            'updated_at': amenity.updated_at.isoformat()
            }, 201
