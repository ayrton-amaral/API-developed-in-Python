from flask import Blueprint, request, jsonify
from database.__init__ import database
from models.user_model import User
import json
from bson.objectid import ObjectId
from controllers.user_controller import create_user, login_user, fetch_users
from helpers.token_validation import validate_token

user = Blueprint("user", __name__)


@user.route("/v0/users/", methods=["POST"])
def create():
    try:
        data = json.loads(request.data)

        if 'email' not in data:
            return jsonify({'error': 'Email is needed in the request.'}), 400
        if 'password' not in data:
            return jsonify({'error': 'Password is needed in the request.'}), 400
        if 'name' not in data:
            return jsonify({'error': 'Name is needed in the request.'}), 400

        created_user = create_user(data)

        if created_user == "Duplicated User":
            return jsonify({'error': 'There is already an user with this email.'}), 400
        
        if not created_user.inserted_id:
            return jsonify({'error': 'Something happened when creating user.'}), 500

        return jsonify({'id': str(created_user.inserted_id)})
    except Exception:
        return jsonify({'error': 'Something happened when creating user.'}), 500


@user.route("/v0/users/login", methods=["POST"])
def login():
    try:
        data = json.loads(request.data)

        if 'email' not in data:
            return jsonify({'error': 'Email is needed in the request.'}), 400
        if 'password' not in data:
            return jsonify({'error': 'Password is needed in the request.'}), 400

        login_attempt = login_user(data)

        if login_attempt == "Invalid Email":
            return jsonify({'error': 'Email not found.'}), 400
        if login_attempt == "Invalid Password":
            return jsonify({'error': 'Invalid Password.'}), 400

        return login_attempt
    except Exception:
        return jsonify({'error': 'Something happened when trying to login.'}), 500

@user.route("/v0/users/", methods=["GET"])
def fetch():
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request.'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid token authentication.'}), 401

        return jsonify({'users': fetch_users()})
    except Exception:
        return jsonify({'error': 'Something happened when trying to fetch users.'}), 500