from flask_restx import Namespace, Resource, fields
from app.persistence.facade import hbnb_facade
from app.business_logic.place import Place
from app.business_logic.user import User
from app.business_logic.amenity import Amenity

api = Namespace('places', description='Place operations')

# Model for API documentation
place_model = api.model('Place', {
    'id': fields.String(readonly=True, description='Place identifier'),
    'owner_id': fields.String(required=True, description='Owner user ID'),
    'name': fields.String(required=True, description='Place name'),
    'description': fields.String(description='Place description'),
    'latitude': fields.Float(description='Geographic latitude'),
    'longitude': fields.Float(description='Geographic longitude'),
    'amenity_ids': fields.List(fields.String, description='List of amenity IDs'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Update date')
})

@api.route('/')
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        """Get all places"""
        return hbnb_facade.get_all(Place), 200

    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        data = api.payload
        
        # Validate owner exists
        owner = hbnb_facade.get(User, data['owner_id'])
        if not owner:
            api.abort(400, "Owner user does not exist")
            
        # Validate amenities exist
        for amenity_id in data.get('amenity_ids', []):
            if not hbnb_facade.get(Amenity, amenity_id):
                api.abort(400, f"Amenity with ID {amenity_id} does not exist")
        
        try:
            place = hbnb_facade.create(Place, **data)
            return place, 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Get place by ID"""
        place = hbnb_facade.get(Place, place_id)
        if not place:
            api.abort(404, "Place not found")
        return place, 200

    @api.expect(place_model)
    @api.marshal_with(place_model)
    def put(self, place_id):
        """Update place information"""
        data = api.payload
        place = hbnb_facade.get(Place, place_id)
        if not place:
            api.abort(404, "Place not found")
            
        # Validate owner if being updated
        if 'owner_id' in data:
            owner = hbnb_facade.get(User, data['owner_id'])
            if not owner:
                api.abort(400, "Owner user does not exist")
                
        # Validate amenities if being updated
        if 'amenity_ids' in data:
            for amenity_id in data['amenity_ids']:
                if not hbnb_facade.get(Amenity, amenity_id):
                    api.abort(400, f"Amenity with ID {amenity_id} does not exist")
        
        try:
            updated_place = hbnb_facade.update(Place, place_id, **data)
            return updated_place, 200
        except ValueError as e:
            api.abort(400, str(e))
