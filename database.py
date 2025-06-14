import pymongo
from pymongo.errors import ConnectionFailure

class Database:
    def __init__(self, database_name="biblioteca"):
        try:
            self.client = pymongo.MongoClient("localhost:27017")
            self.db = self.client[database_name]
            print("Conectado ao MongoDB com sucesso!")
        except ConnectionFailure as e:
            print(f"Falha na conexão: {e}")
            raise