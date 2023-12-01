from models.verb_model import Verb
from database.__init__ import database
import app_config as config
from flask import jsonify
from bson.objectid import ObjectId
from helpers.external_api import getVerbFromApi, get_random_from_api

def get_verb(userInput):
    try:
        verb = userInput["verb"]

        response = getVerbFromApi(verb)

        if response.status_code == 200:
            return jsonify({"verb": response.json()})
        else:
            return jsonify({"error": response.json()["errorMessage"]})
    except Exception as err:
        print("Error on trying to get the verb. ", err)


def get_random_verbs(userInput):
    try:
        quantity = userInput["quantity"]

        response = get_random_from_api(quantity)

        if response.status_code == 200:
            return jsonify({"verbs": response.json()})
        else:
            return jsonify({"error": response.json()["errorMessage"]})
    except Exception as err:
       print("Error on trying to get the verb. ", err)


def favorite_verb(userInput, tokenUser):
    try:
        verb = userInput["verb"]
        user_id = tokenUser.get('uid', None)

        response = getVerbFromApi(verb)

        if response.status_code == 200:
            collection = database.dataBase[config.CONST_USER_COLLECTION]
            user = collection.find_one({'_id': ObjectId(user_id)})

            if user is None:
                return jsonify({'error': 'User not found.'}), 404

            new_verb = Verb()
            new_verb.owner = user_id
            new_verb.verb = verb

            collectionVerb = database.dataBase[config.CONST_VERB_COLLECTION]
            existing_verb = collectionVerb.find_one({'owner': user_id, 'verb': verb})

            if existing_verb:
                return jsonify({'error': 'Duplicated verb'}), 400

            favorite_verb_result = collectionVerb.insert_one(new_verb.__dict__)

            return jsonify({'verb_id': str(favorite_verb_result.inserted_id)})

        else:
            return jsonify({"error": response.json()["errorMessage"]})

    except Exception as err:
        print("Error on trying to save verb. ", err)


def selectFavorite(favoriteUid, tokenUser):
    user_id = tokenUser.get('uid', None)

    collectionVerb = database.dataBase[config.CONST_VERB_COLLECTION]
    selectedVerb = collectionVerb.find_one({'owner': user_id, '_id': ObjectId(favoriteUid)})

    if not selectedVerb:
        return None

    response = getVerbFromApi(selectedVerb["verb"])

    return response

def selectAllFavorites(tokenUser):
    user_id = tokenUser.get('uid', None)

    collectionVerb = database.dataBase[config.CONST_VERB_COLLECTION]
    favoriteVerbs = collectionVerb.find({'owner': user_id})

    verbs = []

    for verb in favoriteVerbs:
        current_verb = {}
        current_verb["_id"] = str(verb['_id'])
        current_verb["verb"] = verb['verb']
        verbs.append(current_verb)

    return verbs

def delete_favorite(favoriteUid, tokenUser):
    user_id = tokenUser.get('uid', None)

    collectionVerb = database.dataBase[config.CONST_VERB_COLLECTION]

    selectedVerb = collectionVerb.find_one({'owner': user_id, '_id': ObjectId(favoriteUid)})

    if not selectedVerb:
        return None

    response = collectionVerb.delete_one(selectedVerb)


    return response