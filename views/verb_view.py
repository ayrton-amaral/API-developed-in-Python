from flask import Blueprint, request, jsonify
import json
from controllers.verb_controller import get_verb, favorite_verb
from helpers.token_validation import validate_token

verb = Blueprint("verb", __name__)

@verb.route("/v0/verbs/", methods=["GET"])
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

@verb.route("/v0/verbs/favorites/", methods=["POST"])
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

    except Exception as error:
        print(error)
        return jsonify({'error': 'Something happened when trying to favorite the verb.'}), 500
