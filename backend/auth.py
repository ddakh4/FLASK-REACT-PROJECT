from flask import make_response
from flask_restx import Resource, Namespace, fields
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (JWTManager,
                               create_access_token,
                               create_refresh_token,
                               get_jwt_identity,
                               jwt_required)
from flask import Flask, request, jsonify, make_response

auth_ns = Namespace('auth', description = "A namespace for our Authentication")

#models used to validate the data in the requests
signup_model = auth_ns.model(
    'SignUp',
    {
    "fullname": fields.String(),
    "username": fields.String(),
    "phone": fields.String(),
    "password": fields.String()
    }
)

login_model = auth_ns.model(
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
        data = request.get_json()

        username = data.get('username')
        db_user = User.query.filter_by(username = username).first()
        if db_user is not None:
            return jsonify({"message": "User with username {} already exists".format(username)})

        phone = data.get('phone')
        db_phone = User.query.filter_by(phone=phone).first()
        if db_phone is not None:
            return jsonify({"message": "User with phone number {} already exists".format(phone)})

        new_user = User(
            fullname = data.get('fullname'),
            username = data.get('username'),
            phone = data.get('phone'),
            password = generate_password_hash(data.get('password'))
        )

        new_user.save()
        response =  make_response(jsonify({"message": "User created succesfully"}), 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        db_user = User.query.filter_by(username = username).first()

        if db_user is None or not check_password_hash(db_user.password, password):
            return jsonify({"message": "Invalid username or password"})

        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity = db_user.id)
            refresh_token = create_refresh_token(identity = db_user.id)

            response =  make_response(jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user_id": db_user.id,
                "user_name": db_user.username}
            ), 201)
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response

@auth_ns.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh = True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity = current_user)
        return make_response(jsonify({"access_token": new_access_token}), 200)
