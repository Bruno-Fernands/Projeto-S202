from app.modelsneo4j import BibliNeo4j

class LibraryCLI:
    def __init__(self, user_model, neo4j_driver):
        self.biblioteca = BibliNeo4j(neo4j_driver)
        self.user_model = user_model
        self.current_user = None

    def start(self):
        while True:
            if not self.current_user:
                self.show_main_menu()
            else:
                if self.current_user["is_employee"]:
                    self.show_employee_menu()
                else:
                    self.show_user_menu()

    def show_main_menu(self):
        print("\n=== Biblioteca Digital ===")
        print("1. Login")
        print("2. Registrar")
        print("3. Sair")
    
        choice = input("Escolha: ")
    
        if choice == "1":
            self.login()
        elif choice == "2":
            self.register()
        elif choice == "3":
            self.exit_program()  # Aqui!
        else:
            print("Opção inválida!")


    def show_user_menu(self):
        print(f"\nBem-vindo, {self.current_user['name']}!")
        print("1. Meus dados")
        print("2. Meus livros")
        print("3. Atualizar dados")
        print("4. Logout")
        
        choice = input("Escolha: ")
        
        if choice == "1":
            self.show_user_data()
        elif choice == "2":
            self.show_borrowed_books()
        elif choice == "3":
            self.update_user_data()
        elif choice == "4":
            self.current_user = None
        else:
            print("Opção inválida!")

    def show_employee_menu(self):
        print(f"\nPainel Funcionário - {self.current_user['name']}")
        print("1. Gerenciar usuários")
        print("2. Gerenciar livros")
        print("3. Logout")
        
        choice = input("Escolha: ")
        
        if choice == "1":
            self.manage_users()
        elif choice == "2":
            self.manage_books()
        elif choice == "3":
            self.current_user = None
        else:
            print("Opção inválida!")

    def login(self):
        email = input("Email: ")
        password = input("Senha: ")
        user = self.user_model.authenticate(email, password)
        if user:
            self.current_user = user
            print("Login bem-sucedido!")
        else:
            print("Credenciais inválidas!")

    def register(self):
        name = input("Nome: ")
        email = input("Email: ")
        password = input("Senha: ")
        
        # Verifica se é cadastro de funcionário
        is_employee = input("Código de funcionário (deixe em branco para usuário): ")
        
        user_id = self.user_model.create(
            name, 
            email, 
            password,
            is_employee=bool(is_employee)
        )
        
        if user_id:
            print("Registro bem-sucedido!")
        else:
            print("Email já cadastrado!")

    def show_user_data(self):
        print(f"\nNome: {self.current_user['name']}")
        print(f"Email: {self.current_user['email']}")
        print(f"Tipo: {'Funcionário' if self.current_user['is_employee'] else 'Usuário'}")

    def show_borrowed_books(self):
        books = self.current_user.get('borrowed_books', [])
        if books:
            print("\nLivros emprestados:")
            for book in books:
                print(f"- {book.get('title', 'Sem título')}")
        else:
            print("\nNenhum livro emprestado.")

    def update_user_data(self):
        print("\nAtualizar dados (deixe em branco para manter)")
        name = input(f"Nome [{self.current_user['name']}]: ") or self.current_user['name']
        new_email = input(f"Email [{self.current_user['email']}]: ") or self.current_user['email']
        password = input("Nova senha (deixe em branco para manter): ") or self.current_user['password']
        
        updates = {
            "name": name,
            "email": new_email,
            "password": password
        }
        
        self.user_model.update(str(self.current_user['_id']), updates)
        print("Dados atualizados!")

    def manage_users(self):
        while True:
            print("\nGerenciar Usuários")
            print("1. Listar todos")
            print("2. Buscar por email")
            print("3. Voltar")
            
            choice = input("Escolha: ")
            
            if choice == "1":
                users = self.user_model.list_all()
                for user in users:
                    print(f"\nID: {user['_id']}")
                    print(f"Nome: {user['name']}")
                    print(f"Email: {user['email']}")
                    print(f"Tipo: {'Funcionário' if user['is_employee'] else 'Usuário'}")
            elif choice == "2":
                email = input("Digite o email: ")
                user = self.user_model.find_by_email(email)
                if user:
                    print(f"\nNome: {user['name']}")
                    print(f"Email: {user['email']}")
                    print(f"Tipo: {'Funcionário' if user['is_employee'] else 'Usuário'}")
                else:
                    print("Usuário não encontrado!")
            elif choice == "3":
                break
            else:
                print("Opção inválida!")

    def manage_books(self):
        while True:
            print("\nGerenciar Livros")
            print("1. Registrar Livro")
            print("2. Listar Livros")
            print("3. Buscar por Título")
            print("4. Voltar")

            choice = input("Escolha: ")

            if choice == "1":
                titulo = input("Título: ")
                autor = input("Autor: ")
                ano = input("Ano de Publicação: ")
                isbn = input("ISBN: ")
                categoria = input("Categoria: ")
                self.biblioteca.registrar_livro(titulo, autor, ano, isbn, categoria)
                print("Livro registrado e salvo no banco com sucesso.")
            elif choice == "2":
                self.biblioteca.listar_livros()
            elif choice == "3":
                titulo = input("Título do livro: ")
                self.biblioteca.buscar_por_titulo(titulo)
            elif choice == "4":
                break
            else:
                print("Opção inválida!")
    
    def exit_program(self):
        self.biblioteca.close()
        print("Conexão com a biblioteca encerrada.")
        exit()

            