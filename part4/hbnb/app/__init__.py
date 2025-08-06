from flask import Flask, render_template
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth
from flask_bcrypt import Bcrypt
from app.extensions import bcrypt
from flask_jwt_extended import JWTManager
from app.extensions import db, bcrypt, jwt
from flask_cors import CORS
import os


bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__,
                static_folder=os.path.join(base_dir, '..', 'static'),
                template_folder=os.path.join(base_dir, '..', 'templates'))
    
    app.config.from_object(config_class)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth, path='/api/v1/auth')

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    CORS(app)
    

    @app.route('/login')
    def login():
        return render_template('login.html')
    @app.route('/places')
    def index():
        return render_template('index.html')
    @app.route('/place/<string:place_id>')
    def place_detail(place_id):
        return render_template('place.html')

    @app.route('/add_review/<string:place_id>')
    def add_review(place_id):
        return render_template('add_review.html')


    return app