import psycopg2

#CRUD para biblioteca Saber & CIA

def conectar():
    print("Conectando ao banco de dados.")
    try:
        connection = psycopg2.connect(
            database='saber',                   #Nome do banco de dados
            host='localhost',                   #Porta do banco
            user='postgres',                    #Nome do usuário
            password='12345678'                 #Senha
        )
        return connection
    except psycopg2.Error as e:                 #É lançada uma excessão caso ocorra erro (e será especificada)
        print(f"Erro na conexão: {e}")

def desconectar(conexao):
    if conexao:
        print("Desconectando do banco de dados.")
        conexao.close()                         #Essa função encerra a conexão entre Python e o BD

def listar():
    conexao = conectar()
    cursor = conexao.cursor()                    #Cursor é como se fosse um ponteiro interage com os dados após ter a conexão estabelecida
    cursor.execute('SELECT * FROM autores')      #Aqui está sendo armazenado os dados da tabela correspondente
    autores = cursor.fetchall()                  #Aqui estaremos transformando os dados em uma lista de tuplas

    if len(autores) > 0:
        print("Listando os autores")
        print("-----------------------")
        for autor in autores:
            print(f"Índice: {autor[0]}")
            print(f"Nome: {autor[1]}")
            print(f"Data de nascimento: {autor[2]}")
            print(f"Nacionalidade: {autor[3]}\n")
        
        else:
            print("Não há autores a serem listados.\n")
        desconectar(conexao)
        
def inserir():
    conexao = conectar()
    cursor = conexao.cursor()

    nome = input("Informe o nome do autor: ")
    data_nascimento = input("Data de nascimento: ")
    nacionalidade = input("Nacionalidade: ")

    cursor.execute(f"INSERT INTO autores (nome, data_nasc, nacionalidade) VALUES ('{nome}', '{data_nascimento}', '{nacionalidade}')")
    #A função execute da lib psycopg2 permite que façamos instruções SQL para o banco de dados.
    conexao.commit()

    if cursor.rowcount == 1:                                        #Aqui verificamos se no cursor temos 1 linha, afinal, estávamos inserindo uma linha a mais, então deve ter 1 linha, c.c terá um erro.
        print(f"O(a) autor(a) {nome} foi inserido(a) com sucesso.")
    
    else:
        print(f"Erro ao adicionar.")
    
    desconectar(conexao)

def atualizar():
    conexao = conectar()
    cursor = conexao.cursor()

    nome = input("Insira o nome do autor que desejar alterar os dados: ")
    data_nascimento = input("Data de nascimento: ")
    nacionalidade = input("Nacionalidade: ")

    cursor.execute(f"UPDATE autores set data_nasc='{data_nascimento}', nacionalidade='{nacionalidade}' WHERE nome='{nome}'")
    conexao.commit()

    if cursor.rowcount == 1:
        print("Dados alterados com sucesso.")
    else:
        print("Erro ao alterar os dados.")
    
    desconectar(conexao)

def deletar():
    conexao = conectar()
    cursor = conexao.cursor()

    codigo = int(input(f"Digite o código do autor que desejar remover: "))

    cursor.execute(f"DELETE FROM autores WHERE id='{codigo}'")
    conexao.commit()

    if cursor.rowcount == 1:
        print(f"Autor de índice {codigo} removido.")
    else:
        print(f"Erro ao remover autor.")
    
    desconectar(conexao)


def menu():
    print("Selecione uma das opções abaixo:\n1. Inserir\n2. Remover\n3. Atualizar\n4. Listar")
    opcoes = int(input())
    
    match opcoes:
        case 1:
            inserir()
        case 2:
            deletar()
        case 3: 
            atualizar()
        case 4:
            listar()
        case _:
            print(f"Por favor, digite uma opção válida.")


