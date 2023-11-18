from flask import Blueprint, request, jsonify
from database.__init__ import database
from models.user_model import User
from models.verb_model import Verb
import json
from bson.objectid import ObjectId
from controllers.user_controller import create_user, login_user, fetch_users, get_verb, favorite_verb
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

@user.route("/v0/verbs/", methods=["GET"])
def getVerb():
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid token authentication, please login again'}), 401
            
        data = json.loads(request.data)
        if 'verb' not in data:
            return jsonify({'error': 'Verb is needed in the request.'}), 400

        response_data = get_verb(data).json

        return jsonify(response_data)
    except Exception:
        return jsonify({'error': 'Something happened when trying to get the verb.'}), 500

@user.route("/v0/verbs/favorites/", methods=["POST"])
def favoriteVerb():
    try:
        token = validate_token()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request, please try again'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid token authentication, please login again'}), 401
            
        data = json.loads(request.data)

        if 'verb' not in data:
            return jsonify({'error': 'Verb is needed in the request.'}), 400

        favorite_verb_result = favorite_verb(data, token)

        return favorite_verb_result

    except Exception:
        return jsonify({'error': 'Something happened when trying to favorite the verb.'}), 500
