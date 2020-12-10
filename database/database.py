from pymongo import MongoClient
from pymongo import InsertOne
from pymongo import ReturnDocument
from pymongo import (ASCENDING, DESCENDING)


class Connection:
    db_user = 'admin'
    db_pass = 'q5HX3WGYhGVNtp7d6kk3cqkGQT9Gfq'
    db_host = 'wjxpdxadgb.spotcloud.io:27017,' \
              'wsatvenyuj.spotcloud.io:27017,' \
              'trbszvyxky.spotcloud.io:27017'
    db_port = '27017'
    db_auth = 'admin'
    db_name = 'vision-occupancy-dev'

    db_uri = f'mongodb://{db_user}:{db_pass}@{db_host}/?' \
             f'replicaSet=rs0&readPreference=secondaryPreferred'

    __instance = None

    class ConnectionContainer:
        AFTER = ReturnDocument.AFTER
        BEFORE = ReturnDocument.BEFORE
        ASCENDING = ASCENDING
        DESCENDING = DESCENDING

        def __init__(self):
            self.db_client = MongoClient(
                Connection.db_uri, ssl=True,
                ssl_ca_certs='database/mongodb.pem',
                maxIdleTimeMS=5000, maxPoolSize=2
            )
            self.database = self.db_client[Connection.db_name]

            for key in self.database.list_collection_names():
                # print(key)
                setattr(self, key, self.database[key])

        @staticmethod
        def bulk_insert_one(document: dict):
            return InsertOne(document)

        def close_connection(self):
            self.db_client.close()

    @staticmethod
    def get_instance() -> ConnectionContainer:
        if Connection.__instance is None:
            Connection()
        print(Connection.__instance)
        return Connection.__instance

    def __init__(self):
        if Connection.__instance is None:
            Connection.__instance = Connection.ConnectionContainer()
        else:
            print('La conexion ya existe')