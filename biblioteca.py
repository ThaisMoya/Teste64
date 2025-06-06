import json
 
class Livros:
    def __init__ (self,titulo,autor,isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.status_emprestimo = False
        self.membro_id_emprestado = None
 
 
class Membro:
    def __init__ (self, nome, membro_id):
        self.nome = nome
        self.membro_id = membro_id
       
class Biblioteca:
    def __init__(self):
        # Tenta carregar o acervo de um arquivo, se existir
        try:
            with open("acervo.json", 'r') as arquivo:
                # Carrega os dados do arquivo
                dados = json.load(arquivo)
                print(dados)
                # Converte os dicionários de volta para objetos Livros
                self.acervo = [Livros(livro['titulo'], livro['autor'], livro['isbn'], livro['status_emprestimo'])
                              for livro in dados]
        except FileNotFoundError:
            # Se o arquivo não existir, inicia com acervo vazio
            self.acervo = []
 
        try:
            with open("membros.json", 'r') as arquivo:
                dados = json.load(arquivo)
                self.membros = [Membro(membro["nome"], membro["membro_id"]) for membro in dados]
 
        except FileNotFoundError:
            self.membros = []
   
    def salvar_membros(self):
 
        dados = [{"nome": membro.nome, "membro_id": membro.membro_id} for membro in self.membros]
   
        with open("membros.json", "w") as arquivo:
            json.dump(dados, arquivo)
 
   
    def salvar_acervo(self):
        # Converte os objetos Livros para dicionários
        dados = [{'titulo': livro.titulo, 'autor': livro.autor,
                 'isbn': livro.isbn, 'status_emprestimo': livro.status_emprestimo}
                for livro in self.acervo]
       
        # Salva os dados em um arquivo JSON
        with open('acervo.json', 'w') as arquivo:
            json.dump(dados, arquivo)
   
    def adicionar_membro(self):
        nome = input("Digite seu nome: ")
 
        #Gerar ID único para cada membro
        if not self.membros:
            membro_id = 1
        else:
            membro_id = max(membro.membro.id for membro in self.membros) + 1
 
        self.membros.append(nome, membro_id)
        self.salvar_membros()
 
        print(f"\nO membro {nome} foi adicionado com sucesso!!!")
        return
 
    def listar_membros(self):
        if not self.membros:
            print("\nNão temos membros cadastrados")
            return
        else:
            print("\n======== LISTA DE MEMBROS ========")
            for membro in self.membros:
                print(f"")
               
 
 
 
    def add_livro(self):   ####### ADM #######
        titulo = input("Digite o título do livro: ")
        autor = input("Digite o autor do livro: ")
        isbn = input("Digite o ISBN do livro: ")
       
        novo_livro = Livros(titulo, autor, isbn)
        self.acervo.append(novo_livro)
       
        # Salva o acervo após adicionar um livro
        self.salvar_acervo()
       
        print(f"Livro '{titulo}' adicionado com sucesso ao acervo!")
        return novo_livro
   
    def remove_livro(self):   ####### ADM #######
 
        remove_isbn = input("Digite o ISBN do livro que quer remover: ")
 
        # Procura o livro pelo ISBN
        livro_encontrado = None
 
        for livro in self.acervo:
            if livro.isbn == remove_isbn:
                livro_encontrado = livro
                break
       
        # Verifica se o livro foi encontrado
        if livro_encontrado is None:
            print(f"Livro com ISBN {remove_isbn} não foi encontrado no acervo.")
            return
       
        # Confirmação antes de remover
        confirmacao = input(f"Tem certeza que deseja remover o livro '{livro_encontrado.titulo}' de {livro_encontrado.autor}? (s/n): ")
       
        if confirmacao.lower() == 's':
            self.acervo.remove(livro_encontrado)
            print(f"Livro '{livro_encontrado.titulo}' removido com sucesso!")
           
            # Salva o acervo após a remoção
            self.salvar_acervo()
        else:
            print("Operação de remoção cancelada.")
           
    def listar_livros(self):   ####### MEMBRO #######   ####### ADM #######
 
        if not self.acervo:  # Verifica se o acervo está vazio
            print("O acervo está vazio. Nenhum livro cadastrado.")
            return
       
        print("\n===== LISTA DE LIVROS NO ACERVO =====")
        print(f"Total de livros: {len(self.acervo)}\n")
 
       
        for i, livro in enumerate(self.acervo, 1):
            status = "Disponível" if not livro.status_emprestimo else "Emprestado"
            print(f"{i}. Título: {livro.titulo}")
            print(f"   Autor: {livro.autor}")
            print(f"   ISBN: {livro.isbn}")
            print(f"   Status: {status}\n")
 
    def emprestar_livro(self):   ####### MEMBRO #######
        # Solicitar informações via input
        isbn = input("Digite o ISBN do livro que deseja emprestar: ")
        membro_id = input("Digite o ID do membro: ")
       
        # Encontrar o livro pelo ISBN
        for livro in self.acervo:
            if livro.isbn == isbn:
                if not livro.status_emprestimo:
                    livro.status_emprestimo = True
                    livro.membro_id_emprestado = membro_id
                    self.salvar_acervo()
                    print("Livro emprestado com sucesso!")
                    return True
                else:
                    print("Este livro já está emprestado.")
                    return False
       
        print("Livro não encontrado no acervo.")
        return False
 
    def devolver_livro(self):   ####### MEMBRO #######
        membro_id = input("Digite seu id: ")
        livros_emprestados = []
 
        for livro in self.acervo: #Verifico se há livros emprestados ao usuário e os capturo em uma lista chamada "livros_emprestados"
            if membro_id == livro.membro_id_emprestado:
                livros_emprestados.append(livro)
                if not livros_emprestados:
                    print(f"O usuário de id:{membro_id} não possui livros emprestados.")
                    return False
               
                for i, livro in enumerate(livros_emprestados, 1): #listo os livros emprestados ao usuário
                    print(f"{i}. Título: {livro.titulo}")
 
                index_devolver = int(input("Digite qual é o número do livro que deseja devolver: "))
                livro_devolvido = livros_emprestados[index_devolver - 1] #Capturo o livro que o usuário quer devolver
 
                confirmacao = input(f"Confirmar a devolução do livro '{livro_devolvido.titulo}'? (s/n): ")
 
                if confirmacao.lower() == 's':
                    livro_devolvido.status_emprestimo = False
                    livro_devolvido.membro_id_emprestado = None
                    self.salvar_acervo()
                    print(f"Livro '{livro_devolvido.titulo}' devolvido com sucesso!")
                    return True
               
                else:
                    print("Operação de devolução cancelada.")
                    return False
                 
    def consultar_emprestimo(self):
        pass
 
#############       MENUS          ###############]
 
 
def menuOpcoes():
    print(" \nMENU ")
    print("0 - Sair ")
    print("1 - Menu Membro")
    print("2 - Menu ADM ")
    return captura_input_menu()
 
def captura_input_menu():
    captura = int(input("\nDigite a opção desejada: "))
    return captura
 
def menu_membro():
    print("\n MENU MEMBRO ")
    print("0 - Sair ")
    print("1 - Emprestar Livro ")
    print("2 - Devolver Livro ")
    print("3 - Listar Livros")
    print("4 - Status do Empréstimo ")
    return captura_input_menu()
 
def menu_adm():
    print("\n MENU ADM ")
    print("0 - Sair ")
    print("1 - Adicionar Livro")
    print("2 - Remover Livro")
    print("3 - Listar Livros")
    return captura_input_menu()
 
#############      INÍCIO DO PROGRAMA         ###############
 
biblioteca = Biblioteca()
 
while True:
    opcao_digitada = menuOpcoes()
 
    if opcao_digitada == 1: ### ENTRANDO NO MENU DO MEMBRO ###
        opcao_digitada = menu_membro()
 
        if opcao_digitada == 1: ### --- OPÇÃO 1: EMPRÉSTIMO DE LIVRO --- ###
            biblioteca.emprestar_livro()
        elif opcao_digitada == 2: ### --- OPÇÃO 2: DEVOLUÇÃO DE LIVRO --- ###
            biblioteca.devolver_livro()
        elif opcao_digitada == 3: ### --- OPÇÃO 3: LISTAR LIVROS --- ###
            biblioteca.listar_livros()
        elif opcao_digitada == 4: ### --- OPÇÃO 4: CONSULTAR EMRPÉSTIMO DE LIVRO --- ###
            biblioteca.consultar_emprestimo()
       
    elif opcao_digitada  == 2: ### ENTRANDO NO MENU DO ADM ###
        opcao_digitada = menu_adm()
 
        if opcao_digitada == 1: ### --- OPÇÃO 1: ADICIONAR LIVRO --- ###
            biblioteca.add_livro()
        elif opcao_digitada == 2: ### --- OPÇÃO 2: REMOÇÃO DE LIVRO --- ###
            biblioteca.remove_livro()
        elif opcao_digitada == 3: ### --- OPÇÃO 3: LISTAR LIVROS --- ###
            biblioteca.listar_livros()
 
    elif opcao_digitada == 0:
        print("Você encerrou o programa")
        break