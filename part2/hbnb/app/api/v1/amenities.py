from flask_restx import Namespace, Resource, fields
from app.persistence.facade import hbnb_facade
from app.business_logic.amenity import Amenity

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
        return hbnb_facade.get_all(Amenity), 200

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = api.payload
        amenity = hbnb_facade.create(Amenity, **data)
        return amenity, 201

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get amenity by ID"""
        amenity = hbnb_facade.get(Amenity, amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity, 200

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update amenity information"""
        data = api.payload
        amenity = hbnb_facade.update(Amenity, amenity_id, **data)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity, 200
