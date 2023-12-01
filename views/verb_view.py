from flask import Blueprint, request, jsonify
import json
from controllers.verb_controller import get_verb as controller_get_verb, get_random as controller_get_random, add_favorite as controller_add_favorite, get_favorite as controller_get_favorite, get_all_favorites as controller_get_all_favorites, delete_favorite as controller_delete_favorite
from helpers.token_validation import validate_token
from helpers.error_message import *
from bson.objectid import ObjectId

verb = Blueprint("verb", __name__)

@verb.route("/v0/verbs/", methods=["GET"])
def get_verb():
    try:
        token = validate_token()

        if token == 400:
            return jsonify(CONST_MISSING_TOKEN_ERROR), 400
        if token == 401:
            return jsonify(CONST_INVALID_TOKEN_ERROR), 401
            
        data = json.loads(request.data)
        if 'verb' not in data:
            return jsonify(CONST_VERB_NEEDED_ERROR), 400

        response = controller_get_verb(data)
        return jsonify(response)
    except Exception:
        return jsonify({'error': 'Something happened when trying to get the verb.'}), 500

@verb.route("/v0/verbs/random/", methods=["GET"])
def get_random():
    try:
        token = validate_token()
        if token == 400:
            return jsonify(CONST_MISSING_TOKEN_ERROR), 400
        if token == 401:
            return jsonify(CONST_INVALID_TOKEN_ERROR), 401
            
        data = json.loads(request.data)

        if 'quantity' not in data:
            return jsonify(CONST_QUANTITY_NEEDED_ERROR), 400
    
        response = controller_get_random(data)
        return jsonify(response)        
    except Exception:
        return jsonify({'error': 'Something happened when trying to get random verbs.'}), 500

@verb.route("/v0/verbs/favorites", methods=["POST"])
def add_favorite():
    try:
        token = validate_token()
        if token == 400:
            return jsonify(CONST_MISSING_TOKEN_ERROR), token
        if token == 401:
            return jsonify(CONST_INVALID_TOKEN_ERROR), token
            
        data = json.loads(request.data)

        if 'verb' not in data:
            return jsonify(CONST_VERB_NEEDED_ERROR), 400

        favorite_verb_result = controller_add_favorite(data, token)
        
        if 'error' in favorite_verb_result:
            return jsonify(favorite_verb_result), 400
        
        return jsonify(favorite_verb_result)
    except Exception as error:
        print(error)
        return jsonify({'error': 'Something happened when trying to favorite the verb.'}), 500


@verb.route("/v0/verbs/favorites/<favorite_uid>/", methods=["GET"])
def get_favorite(favorite_uid):
    try:
        token = validate_token()
        if token == 400:
            return jsonify(CONST_MISSING_TOKEN_ERROR), token
        if token == 401:
            return jsonify(CONST_INVALID_TOKEN_ERROR), token
        
        try:
            ObjectId(favorite_uid)
        except Exception:
            return jsonify({'error': 'This ObjectId format is not valid.'}), 400

        favorite_verb = controller_get_favorite(favorite_uid, token)
        
        if 'error' in favorite_verb:
            return jsonify(favorite_verb), 400

        return jsonify({"verb": favorite_verb})
    except Exception as error:
        print(error)
        return jsonify({'error': 'Something happened when trying to find favorite verb.'}), 500
    
@verb.route("/v0/verbs/favorites/", methods=["GET"])
def get_all_favorites():
    try:
        token = validate_token()
        if token == 400:
            return jsonify(CONST_MISSING_TOKEN_ERROR), token
        if token == 401:
            return jsonify(CONST_INVALID_TOKEN_ERROR), token

        favoriteVerbs = controller_get_all_favorites(token)
        return jsonify({"verbs": favoriteVerbs})
    except Exception as error:
        print(error)
        return jsonify({'error': 'Something happened when trying to list all favorites verb.'}), 500
    
@verb.route("/v0/verbs/favorites/<favorite_uid>/", methods=["DELETE"])
def delete_favorite_verb(favorite_uid):
    try:
        token = validate_token()
        if token == 400:
            return jsonify(CONST_MISSING_TOKEN_ERROR), token
        if token == 401:
            return jsonify(CONST_INVALID_TOKEN_ERROR), token
        
        try:
            ObjectId(favorite_uid)
        except Exception:
            return jsonify({'error': 'This ObjectId format is not valid.'}), 400

        deleted_favorite = controller_delete_favorite(favorite_uid, token)
 
        if 'error' in deleted_favorite:
            return jsonify(deleted_favorite), 400

        return jsonify(deleted_favorite)
    
    except Exception as error:
        print(error)
        return jsonify({'error': 'Something happened when trying to find favorite verb.'}), 500
    