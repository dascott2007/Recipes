from flask import Flask
from flask_restx import Api
from models import Recipe, User
from exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from recipes import recipe_ns
from auth import auth_ns
from flask_cors import CORS
#from flask_vite import Vite

def create_app(config):
    app=Flask(__name__)
    app.config.from_object(config)
    CORS(app)
    #vite = Vite(app)
    db.init_app(app)
    migrate=Migrate(app, db)
    JWTManager(app) # Allows for JWTManager to be extended to work with the app

    api=Api(app, doc='/docs')
    api.add_namespace(recipe_ns)
    api.add_namespace(auth_ns)

    #Takes a request object as the argument and returns a dictionary of items. Defaults to emply list
    @app.shell_context_processor
    def make_shell_context():
        return{
            "db":db,
            "Recipe":Recipe,
            "user":User
        }    

    return app


