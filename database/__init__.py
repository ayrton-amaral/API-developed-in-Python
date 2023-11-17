from .db import Database
import app_config as config

database = Database(connectionString=config.CONST_MONGO_URL, dataBaseName=config.CONST_DATABASE_NAME)
database.connect()