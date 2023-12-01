from models.verb_model import Verb
from database.__init__ import database
import app_config as config
from bson.objectid import ObjectId
from helpers.external_api import get_verb_from_api, get_random_from_api

def get_verb(user_input):
    verb = user_input["verb"]
    response = get_verb_from_api(verb) 
    if response.status_code == 200:
        return {"verb": response.json()}
    else:
        return {"error": response.json()["errorMessage"]}

def get_random(user_input):
    quantity = user_input["quantity"]
    response = get_random_from_api(quantity)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json()["errorMessage"]}

def add_favorite(user_input, token_user):
    verb = user_input["verb"]
    user_id = token_user.get('uid', None)
    response = get_verb_from_api(verb)
   
    if response.status_code == 200:
        collection = database.dataBase[config.CONST_USER_COLLECTION]
        user = collection.find_one({'_id': ObjectId(user_id)})

        if user is None:
            return {'error': 'User not found.'}

        new_verb = Verb(user_id, verb)

        collection_verb = database.dataBase[config.CONST_VERB_COLLECTION]
        existing_verb = collection_verb.find_one({'owner': user_id, 'verb': verb})

        if existing_verb:
            return {'error': 'Duplicated verb'}

        favorite_verb_result = collection_verb.insert_one(new_verb.__dict__)

        return {'verb_id': str(favorite_verb_result.inserted_id)}

    elif response.status_code == 404 :
        return {"error": "verb not found"}
    else:
        return {"error": response.json()["errorMessage"]}


def get_favorite(favoriteUid, token_user):
    user_id = token_user.get('uid', None)

    collection_verb = database.dataBase[config.CONST_VERB_COLLECTION]
    selected_verb = collection_verb.find_one({'owner': user_id, '_id': ObjectId(favoriteUid)})

    if not selected_verb:
        return {'error': 'This verb is not favorited.'}

    response = get_verb_from_api(selected_verb["verb"])
    if response.status_code != 200:
        return {"error": response.json()["errorMessage"]}
    return response.json()

def get_all_favorites(token_user):
    user_id = token_user.get('uid', None)
    collection_verb = database.dataBase[config.CONST_VERB_COLLECTION]
    favorite_verbs = collection_verb.find({'owner': user_id})
    verbs = []
    for verb in favorite_verbs:
        current_verb = {}
        current_verb["_id"] = str(verb['_id'])
        current_verb["verb"] = verb['verb']
        verbs.append(current_verb)
    return verbs

def delete_favorite(favorite_uid, token_user):
    user_id = token_user.get('uid', None)
    collection_verb = database.dataBase[config.CONST_VERB_COLLECTION]
    selected_verb = collection_verb.find_one({'owner': user_id, '_id': ObjectId(favorite_uid)})
    if not selected_verb:
        return {"error": "This verb is not favorited."}
    response = collection_verb.delete_one(selected_verb)
    return {'verbs_affected': response.deleted_count}