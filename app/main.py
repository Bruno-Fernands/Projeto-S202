import sys
from app.database import Database
from app.models import User
from app.cli import LibraryCLI
from pymongo.errors import ConnectionFailure
from neo4j.exceptions import ServiceUnavailable

def main():
    try:
        # Tenta criar conexões com os bancos
        db = Database()

        # Garantir que a coleção "users" existe
        if "users" not in db.mongo.list_collection_names():
            db.mongo.create_collection("users")

        # Inicializa os modelos e a CLI
        user_model = User(db.mongo)
        cli = LibraryCLI(user_model, db.neo4j_driver)

        # Inicia o sistema
        cli.start()

    except ConnectionFailure as mongo_error:
        print(f"❌ Erro ao conectar ao MongoDB: {mongo_error}")
        sys.exit(1)

    except ServiceUnavailable as neo4j_error:
        print(f"❌ Erro ao conectar ao Neo4j: {neo4j_error}")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

    finally:
        try:
            db.close_connections()
        except Exception:
            pass  # Ignora erro de fechamento, se `db` nem foi criado

if __name__ == "__main__":
    main()
