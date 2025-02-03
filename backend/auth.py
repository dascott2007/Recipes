from flask import Flask, request, jsonify, make_response
from flask_restx import Resource, Namespace, fields
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import(
JWTManager, create_access_token, create_refresh_token, get_jwt_identity, jwt_required
) 

auth_ns=Namespace('auth', description='A namespace for our authentication')

signup_model=auth_ns.model(
    'SignUp',
    {
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String()
    }
)

login_model=auth_ns.model(
    'Login',
    {
        "username": fields.String(),
        "password": fields.String()
    }
)

@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data=request.get_json()

        username=data.get('username')
        # Check if user exists, if so, the return an exception

        db_user=User.query.filter_by(username=username).first()
        if db_user is not None:
            return jsonify({"message":f"User with username {username} aready exists."})

        new_user=User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password'))
        )

        new_user.save()

        return make_response(jsonify({"message": "User created successfully"}),201)
    
@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data=request.get_json()

        username=data.get('username')
        password=data.get('password')

        db_user=User.query.filter_by(username=username).first() # If the user exists, retrun the 1st user that matches
        
        if db_user and check_password_hash(db_user.password, password): # db_user.password is the hashed pw
            access_token=create_access_token(identity=db_user.username)
            refresh_token=create_refresh_token(identity=db_user.username)

            return jsonify(
                {"access_token":access_token, "refresh_token":refresh_token}
            )

# The below will allow us to get a fresh access_token when the front end sends us the refresh token
# This way we use the refresh token so the user can get authenticated with a new access token
@auth_ns.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh=True) # Protect the route so it requires a refresh token
    def post(self):

        current_user=get_jwt_identity()

        new_access_token=create_access_token(identity=current_user)

        return make_response(jsonify({"access_token":new_access_token}),200)