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
    def post(self):
        """Create a new review (only once per place, not on own place)"""
        user_id = get_jwt_identity()
        data = api.payload

        place_id = data.get("place_id")
        text = data.get("text")
        rating = data.get("rating")

        if not place_id or not text or rating is None:
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
            review_data = {
                "text": text,
                "rating": rating,
                "place_id": place_id,
                "user_id": user_id
            }
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 400


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Get review by ID"""
        review = HBnBFacade.get(Review, review_id)
        if not review:
            api.abort(404, "Review not found")
        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_model)
    @api.marshal_with(review_model)
    def put(self, review_id):
        """Update a review (only if user is the author)"""
        user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            api.abort(404, "Review not found")

        if review.user_id != user_id:
            api.abort(403, "Unauthorized action")

        data = api.payload

        try:
            updated_review = facade.update_review(review_id, data)
            return updated_review
        except ValueError as e:
            api.abort(400, str(e))

        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.json
        updated_review = facade.update_review(review_id, data)
        if not updated_review:
            return {'error': 'Update failed'}, 400

        return updated_review, 200
    
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (only if user is the author)"""
        user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            api.abort(404, "Review not found")

        if review.user_id != user_id:
            api.abort(403, "Unauthorized action")

        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except Exception as e:
            api.abort(400, str(e))
