
from werkzeug.security import generate_password_hash, check_password_hash
from .server import database_info
from flask import session
import psycopg2.extras
import psycopg2

# Criando a Classe Database para interagir com a API em main.py
class Database():
    def __init__(self): # No método __init__ vamos criar nossa conexão com o banco de dados PostgreSQL

        # Conectando com o banco de dados
        self.conn = psycopg2.connect(
            host=database_info['host'],
            database=database_info['database'],
            user=database_info['user'],
            password=database_info['password'],
            port=database_info['port']
        )
        
    def registro(self, user): # Nesse método vamos criar novos usuários via suas informações enviada pelo cliente (POST method)
        # Definindo o cursor a partir da conexão passada no método __init__
        cur = self.conn.cursor()
        # Verificando se o usuário já não existe no banco de dados, caso contrário criando o usuário novo
        cur.execute("SELECT id, name, email, password FROM users WHERE email=%s", (user["email"],))
        account = cur.fetchall()

        if account:
            return {'conta existente': account}
        
        else:
            # Criando Hash para criptografar a senha antes de armazenar no banco de dados
            _hashed_password = generate_password_hash(user["password"])
            # Adicionando de o novo usuário
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (user["name"], user["email"], _hashed_password))
            self.conn.commit()
            return {'nova conta criada': user}
        
    def login(self, user): # Neste método vamos autenticar o usuário com suas credenciais e criar uma sessão para ele
        # Definindo o cursor a partir da conexão passada no método __init__
        cur = self.conn.cursor()
        # Verificando se o usuário existe no banco de dados
        cur.execute("SELECT id, name, email, password FROM users WHERE email=%s", (user["email"],))
        account = cur.fetchone()

        if account:
            # Validando as credencias para login
            if check_password_hash(account[3], user["password"]):
                # Criando uma sessão com cookies para o usuário ser autenticado
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                return {'login bem sucedido': session}
            
            else:
                return {'senha inválida': user["password"]}
        else:
            return {'conta inexistente': '404'}
        
    def dashboard(self): # Aqui vamos retornar dados do usuário logado na sessão, ou negar o acesso
        # Verificando se o usuário está logado
        if 'loggedin' in session:
            # Pegando informações do usuário na sessão
            name = session['username']
            itemUser_id = session['id']
            # Buscando os dados do usuário logado
            cur = self.conn.cursor()
            cur.execute("SELECT id, name, description, user_id FROM items WHERE user_id=%s", (itemUser_id,))
            items = cur.fetchall()
            # Retornando as informações do usuário para o cliente via GET
            return {'usuário logado': True, 'name': name, 'items cadastrados': items}
        else:
            return {'acesso não permitido': '401'}

    def create_item(self, item): # Aqui vamos possibilitar o usuário criar novos itens no banco de dados
        if 'loggedin' in session:
            # Verificando se o item já existe no banco de dados, caso contrário criando um novo
            cur = self.conn.cursor()
            cur.execute("SELECT name, description FROM items WHERE name=%s", (item["name"],))
            itemFetch = cur.fetchone()

            if itemFetch:
                return {'item existente': itemFetch}
        
            else:
                __user_id = session['id'] # Vamos adicionar o id de sessão para identificar quem criou o item
                cur.execute("INSERT INTO items (name, description, user_id) VALUES (%s, %s, %s)", (item["name"], item["description"], __user_id))
                self.conn.commit()
                return {'novo item criado': item}

        else:
            return {'acesso não permitido': '401'}    

    def item(self, item_name): # Aqui será feita uma busca para a requisição GET da api contendo a descrição do item solicitado
        # Buscando item no banco de dados
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, description, user_id FROM items WHERE name=%s", (item_name,))
        item = cur.fetchone()
        # Se tiver o item, retornar sua descrição
        if item:
            return {'descrição': item[2]}
        else:
            return {'item inexistente': '404'}


