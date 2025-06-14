import pymongo
from pymongo.errors import ConnectionFailure
from neo4j import GraphDatabase

class Database:
    def __init__(self, mongo_uri="mongodb://localhost:27017", neo4j_uri="bolt://localhost:7687",
                 neo4j_user="neo4j", neo4j_password="senha123", database_name="biblioteca"):

        # MongoDB
        try:
            self.mongo_client = pymongo.MongoClient("mongodb://root:senha123@localhost:27017/")
            self.mongo = self.mongo_client[database_name]
            print("Conectado ao MongoDB com sucesso!")
        except ConnectionFailure as e:
            print(f"Falha na conexão com MongoDB: {e}")
            raise

        # Neo4j
        try:
            self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
            print("Conectado ao Neo4j com sucesso!")
        except Exception as e:
            print(f"Falha na conexão com Neo4j: {e}")
            raise

    def get_mongo_collection(self, collection_name):
        return self.mongo[collection_name]

    def get_neo4j_session(self):
        return self.neo4j_driver.session()

    def close_connections(self):
        self.mongo_client.close()
        self.neo4j_driver.close()
        print("Conexões encerradas.")
