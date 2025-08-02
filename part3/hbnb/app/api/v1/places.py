from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
api = Namespace('places', description='Place operations')

# Models
user_model = api.model('User', {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
})

amenity_model = api.model('Amenity', {
    'id': fields.String,
    'name': fields.String,
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place (Authenticated users only)"""
        data = api.payload
        user_id = get_jwt_identity()

        try:
            data["owner_id"] = user_id
            place = facade.create_place(place_data=data)
            return {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner_id": place.owner_id
            }, 201
        except ValueError as e:
            return {'message': str(e)}, 400 

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{
            "id":place.id,
            "title": place.title ,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id
        }for place in places], 200



@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404
        return place.to_dict(include_owner=True, include_amenities=True), 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information (owner only)"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {'message': 'Place not found'}, 404

        current_user_id = get_jwt_identity()
        if place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            updated_place = facade.update_place(place_id, api.payload)
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 400

        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.json
        updated_place = facade.update_place(place_id, data)
        if not updated_place:
            return {'error': 'Update failed'}, 400

        return updated_place, 200

@api.response(204, 'Place deleted')
@api.response(404, 'Place not found')
def delete(self, place_id):
    """Delete a place by ID"""
    success = facade.delete_place(place_id)
    if not success:
        return {'message': 'Place not found'}, 404
    return '', 204
