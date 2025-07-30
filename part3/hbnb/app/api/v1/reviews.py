from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.models.review import Review
from app.services import facade
from app.models.place import Place
from app.models.user import User
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

    @api.expect(review_model)
    @api.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        data = api.payload

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

    @api.expect(review_model)
    @api.marshal_with(review_model)
    def put(self, review_id):
        """Update review information"""
        data = api.payload
        review = HBnBFacade.get(Review, review_id)
        if not review:
            api.abort(404, "Review not found")
            
        # Validate place if being updated
        if 'place_id' in data:
            place = HBnBFacade.get(Place, data['place_id'])
            if not place:
                api.abort(400, "Place does not exist")
                
        # Validate user if being updated
        if 'user_id' in data:
            user = HBnBFacade.get(User, data['user_id'])
            if not user:
                api.abort(400, "User does not exist")
        
        try:
            updated_review = HBnBFacade.update_review(Review, review_id, **data)
            return updated_review, 200
        except ValueError as e:
            api.abort(400, str(e))
    
    def delete(self, review_id):
        """Delete a review"""
        if not HBnBFacade.delete_review(Review, review_id):
            api.abort(404, "Review not found")
        return {'message': 'Review deleted successfully'}, 200
