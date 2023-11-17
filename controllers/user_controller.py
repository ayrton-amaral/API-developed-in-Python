from models.user_model import User
from database.__init__ import database
import app_config as config
import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import jsonify

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