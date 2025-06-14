from database import Database
from models import User
from cli import LibraryCLI

def main():
    # Configuração inicial
    db = Database()
    
    # Criar coleção se não existir
    if "users" not in db.db.list_collection_names():
        db.db.create_collection("users")
    
    # Inicializar modelos e CLI
    user_model = User(db.db)
    cli = LibraryCLI(user_model)
    
    # Iniciar aplicação
    cli.start()

if __name__ == "__main__":
    main()