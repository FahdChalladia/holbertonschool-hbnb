from flask_restx import Namespace, Resource, fields
from app.persistence.facade import hbnb_facade
from app.business_logic.review import Review
from app.business_logic.place import Place
from app.business_logic.user import User

api = Namespace('reviews', description='Review operations')

# Model for API documentation
review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='Review identifier'),
    'place_id': fields.String(required=True, description='Place ID being reviewed'),
    'user_id': fields.String(required=True, description='User ID writing the review'),
    'text': fields.String(required=True, description='Review text content'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Update date')
})

@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        """Get all reviews"""
        return hbnb_facade.get_all(Review), 200

    @api.expect(review_model)
    @api.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        data = api.payload
        
        # Validate place exists
        place = hbnb_facade.get(Place, data['place_id'])
        if not place:
            api.abort(400, "Place does not exist")
            
        # Validate user exists
        user = hbnb_facade.get(User, data['user_id'])
        if not user:
            api.abort(400, "User does not exist")
        
        try:
            review = hbnb_facade.create(Review, **data)
            return review, 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Get review by ID"""
        review = hbnb_facade.get(Review, review_id)
        if not review:
            api.abort(404, "Review not found")
        return review, 200

    @api.expect(review_model)
    @api.marshal_with(review_model)
    def put(self, review_id):
        """Update review information"""
        data = api.payload
        review = hbnb_facade.get(Review, review_id)
        if not review:
            api.abort(404, "Review not found")
            
        # Validate place if being updated
        if 'place_id' in data:
            place = hbnb_facade.get(Place, data['place_id'])
            if not place:
                api.abort(400, "Place does not exist")
                
        # Validate user if being updated
        if 'user_id' in data:
            user = hbnb_facade.get(User, data['user_id'])
            if not user:
                api.abort(400, "User does not exist")
        
        try:
            updated_review = hbnb_facade.update(Review, review_id, **data)
            return updated_review, 200
        except ValueError as e:
            api.abort(400, str(e))
    
    def delete(self, review_id):
        """Delete a review"""
        if not hbnb_facade.delete(Review, review_id):
            api.abort(404, "Review not found")
        return {'message': 'Review deleted successfully'}, 200
