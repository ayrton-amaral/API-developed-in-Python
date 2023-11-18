from models.user_model import User
from models.verb_model import Verb
from database.__init__ import database
import app_config as config
import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import jsonify
import requests
from bson.objectid import ObjectId


#pip install bcrypt
#pip install pyjwt

def generate_hashed_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def create_user(userInformation):
    try:
        new_user  = User()
        new_user.name = userInformation["name"]
        new_user.email = userInformation["email"]
        new_user.password = generate_hashed_password(userInformation["password"])

        collection = database.dataBase[config.CONST_USER_COLLECTION]

        if collection.find_one({'email': new_user.email}):
            return "Duplicated User"

        created_user = collection.insert_one(new_user.__dict__)

        return created_user


    except Exception as err:
        print("Error on creating user: ", err)

def login_user(userInformation):
    try:
        email = userInformation["email"]
        password = userInformation["password"].encode('utf-8')

        collection = database.dataBase[config.CONST_USER_COLLECTION]

        current_user = collection.find_one({'email': email})

        if not current_user:
            return "Invalid Email"

        if not bcrypt.checkpw(password, current_user["password"]):
            return "Invalid Password"

        logged_user = {}
        logged_user["uid"] = str(current_user['_id'])
        logged_user["email"] = current_user['email']
        logged_user["name"] = current_user['name']

        expiration = datetime.utcnow() + timedelta(seconds=config.JWT_EXPIRATION)

        jwt_data = {'email': logged_user["email"], 'uid': logged_user["uid"], 'exp': expiration}

        token_to_return = jwt.encode(payload=jwt_data, key=config.TOKEN_SECRET)

        return jsonify({'token': token_to_return, 'expiration': config.JWT_EXPIRATION, 'logged_user': logged_user})

    except Exception as err:
        print("Error on trying to login. ", err)

def fetch_users():
    try:
        collection = database.dataBase[config.CONST_USER_COLLECTION]
        users = []

        for user in collection.find():
            current_user = {}
            current_user["uid"] = str(user['_id'])
            current_user["email"] = user['email']
            current_user["name"] = user['name']
            users.append(current_user)

        return users
    except Exception as err:
        print("Error on trying to fetch users. ", err)


def get_verb(userInput):
    try:
        verb = userInput["verb"]
        external_api_url = 'https://lasalle-frenchverb-api-afpnl.ondigitalocean.app/v1/api/verb'
        response = requests.get(external_api_url, headers={'token':
        '278ef2169b144e879aec4f48383dce28e654a009cacf46f8b6c03bbc9a4b9d11'}, json={'verb':
        verb})

        if response.status_code == 200:
            return jsonify({"verb": response.json()})
        else:
            return jsonify({"error": response.json()["errorMessage"]})
    except Exception as err:
        print("Error on trying to get the verb. ", err)

def favorite_verb(userInput, tokenUser):
    try:
        verb = userInput["verb"]
        user_id = tokenUser.get('uid', None)

        external_api_url = 'https://lasalle-frenchverb-api-afpnl.ondigitalocean.app/v1/api/verb'
        response = requests.get(external_api_url, headers={'token': '278ef2169b144e879aec4f48383dce28e654a009cacf46f8b6c03bbc9a4b9d11'}, json={'verb': verb})

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
