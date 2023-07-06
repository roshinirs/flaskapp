import pymongo


class ServerSession:
    def __init__(self):

        try:
            mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=1000)
            self.dbconnect = mongo.projectdb
            mongo.server_info()

        except Exception as error:
            print(f"ERROR - cannot connect to db {error}")
