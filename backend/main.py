from flask import Flask
from flask_restx import Api
from models import Reservation, User
from exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from reservation import res_ns
from auth import auth_ns
from flask_cors import CORS

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)  #initialize db

    CORS(app) #allow cross-origin requests

    migrate = Migrate(app, db) #used to set up database migrations with the app 
    app.config['JWT_SECRET_KEY'] = 'your-secret-key' #used for JWT authentication
    JWTManager(app)

    api = Api(app, doc='/docs')

    api.add_namespace(res_ns)
    api.add_namespace(auth_ns)

    @app.route('/')
    def index():
        return 'Hello, World!'

    @app.route('/favicon.ico')
    def fav_icon():
        return "", 200


    @app.shell_context_processor
    def make_shell_context():
        return {
             "db": db,
             "User": User,
             "Reservation": Reservation
        }
    return app

