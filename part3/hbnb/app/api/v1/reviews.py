from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.models.review import Review
from app.services import facade
from app.models.place import Place
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
facade = HBnBFacade()
api = Namespace('reviews', description='Review operations')

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
    @api.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review (authenticated users only)"""
        current_user = get_jwt_identity()
        data = api.payload
        place_id = data.get('place_id')

        if not place_id:
            api.abort(400, "Place ID is required")

        place = HBnBFacade.get(Place, place_id)
        if not place:
            api.abort(400, "Place does not exist")

        # Prevent user from reviewing their own place
        if place.owner_id == current_user['id']:
            api.abort(400, "You cannot review your own place")

        # Prevent duplicate review
        existing_reviews = facade.get_reviews_by_user_and_place(current_user['id'], place_id)
        if existing_reviews:
            api.abort(400, "You have already reviewed this place")

        # Force user_id to current authenticated user
        data['user_id'] = current_user['id']

        try:
            review = facade.create_review(data)
            return review, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Get review by ID"""
        review = HBnBFacade.get(Review, review_id)
        if not review:
            api.abort(404, "Review not found")
        return review, 200

    @jwt_required()
    @api.expect(review_model)
    @api.marshal_with(review_model)
    def put(self, review_id):
        """Update review information (owner only)"""
        current_user = get_jwt_identity()
        review = HBnBFacade.get(Review, review_id)

        if not review:
            api.abort(404, "Review not found")

        if review.user_id != current_user['id']:
            api.abort(403, "Unauthorized action")

        data = api.payload

        # Optional validation
        if 'place_id' in data:
            place = HBnBFacade.get(Place, data['place_id'])
            if not place:
                api.abort(400, "Place does not exist")

        try:
            updated_review = HBnBFacade.update_review(Review, review_id, **data)
            return updated_review, 200
        except ValueError as e:
            api.abort(400, str(e))
    
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (owner only)"""
        current_user = get_jwt_identity()
        review = HBnBFacade.get(Review, review_id)

        if not review:
            api.abort(404, "Review not found")

        if review.user_id != current_user['id']:
            api.abort(403, "Unauthorized action")

        if not HBnBFacade.delete_review(Review, review_id):
            api.abort(400, "Failed to delete review")

            return {'message': 'Review deleted successfully'}, 200