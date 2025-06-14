from neo4j import GraphDatabase

class BibliNeo4j:
    def __init__(self, driver):
        self.driver = driver

    def close(self):
        self.driver.close()

    def registrar_livro(self, titulo, autor, ano, isbn, categoria):
        with self.driver.session() as session:
            session.run(
                """
                MERGE (c:Categoria {nome: $categoria})
                SET c.name = $categoria

                MERGE (a:Autor {nome: $autor})
                SET a.name = $autor

                MERGE (an:Ano {valor: $ano})
                SET an.name = toString($ano)

                CREATE (l:Livro {titulo: $titulo, name: $titulo, isbn: $isbn})

                MERGE (l)-[:PERTENCE_A]->(c)
                MERGE (l)-[:ESCRITO_POR]->(a)
                MERGE (l)-[:PUBLICADO_EM]->(an)
                """,
                titulo=titulo,
                autor=autor,
                ano=ano,
                isbn=isbn,
                categoria=categoria
            )


    def listar_livros(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (l:Livro)-[:PERTENCE_A]->(c:Categoria),
                    (l)-[:ESCRITO_POR]->(a:Autor),
                    (l)-[:PUBLICADO_EM]->(an:Ano)
                RETURN l.titulo AS titulo, a.nome AS autor, an.valor AS ano, l.isbn AS isbn, c.nome AS categoria
                ORDER BY l.titulo
            """)
            livros = result.data()
            if livros:
                for livro in livros:
                    print(f"{livro['titulo']} - {livro['autor']} ({livro['ano']}) - ISBN: {livro['isbn']} | Categoria: {livro['categoria']}")
            else:
                print("Nenhum livro registrado.")

    def buscar_por_titulo(self, titulo):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (l:Livro {titulo: $titulo})-[:PERTENCE_A]->(c:Categoria),
                    (l)-[:ESCRITO_POR]->(a:Autor),
                    (l)-[:PUBLICADO_EM]->(an:Ano)
                RETURN a.nome AS autor, an.valor AS ano, l.isbn AS isbn, c.nome AS categoria
            """, titulo=titulo)
            livro = result.single()
            if livro:
                print(f"{titulo} - {livro['autor']} ({livro['ano']}) - ISBN: {livro['isbn']} | Categoria: {livro['categoria']}")
            else:
                print("Livro não encontrado.")
