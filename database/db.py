from pymongo import MongoClient

class Database():

    def __init__(self, dataBaseName=None, connectionString=None):
        if ((dataBaseName == None) or (connectionString == None)):
            raise Exception("Mongo DB requires Database Name and String Connection!")
        
        self.__dataBaseName = dataBaseName
        self.__connectionString = connectionString
        self.__dbConnection = None
        self.__dataBase = None

    @property
    def dataBase(self):
        return self.__dataBase

    @property
    def dbConnection(self):
        return self.__dbConnection

    def connect(self):
        try:
            self.__dbConnection =  MongoClient(self.__connectionString)
            dbName = str(self.__dataBaseName)
            self.__dataBase = self.__dbConnection[dbName]
            return True

        except Exception as err:
            print("Mongo connection error!" , err)
            return False