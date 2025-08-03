from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.models.review import Review
from app.services import facade
from app.models.place import Place
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', path='/api/v1/reviews', description='Review operations')

# Model for API documentation
review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='Review identifier'),
    'place_id': fields.String(required=True, description='Place ID being reviewed'),
    'user_id': fields.String(required=True, description='User ID writing the review'),
    'text': fields.String(required=True, description='Review text content'),
    'rating': fields.Integer(required=True),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Update date')
})

@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        """Get all reviews"""
        return facade.get_all_reviews(), 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review (only once per place, not on own place)"""
        user_id = get_jwt_identity()
        data = api.payload

        place_id = data.get("place_id")
        text = data.get("text")
        rating = data.get("rating")

        if not place_id or not text or not rating :
            return {"error": "Missing fields"}, 400

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if place.owner_id == user_id:
            return {"error": "You cannot review your own place"}, 400

        existing_reviews = facade.get_reviews_by_place(place_id)
        for r in existing_reviews:
            if r.user_id == user_id:
                return {"error": "You have already reviewed this place"}, 400

        try:
            new_review = facade.create_review(data)
            return  {
                "id": new_review.id,
                "place_id": new_review.place_id,
                "user_id": new_review.user_id,
                "text": new_review.text,
                "rating": new_review.rating
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400


@api.route('/<string:review_id>')
@api.response(404, 'Review not found')
class ReviewResource(Resource):
    def get(self, review_id):
        """Get review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'review not found'}, 404
        return  {
            "id": review.id,
            "place_id": review.place_id,
            "user_id": review.user_id,
            "text": review.text,
            "rating": review.rating
        }, 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin')
        user_id = current_user.get('id')

        review = facade.get_review(review_id)
        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        data = api.payload
        data["user_id"]=current_user.get("id")
        try:
            facade.update_review(review_id, data)
            return {'message': 'review updated successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 400
    
    @jwt_required()
    @api.response(403, 'Unauthorized action')
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        if not current_user.get('is_admin') and review.user_id != current_user.get("id"):
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except Exception as e:
            api.abort(400, str(e))
