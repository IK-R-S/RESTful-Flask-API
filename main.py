from flask import Flask, request, redirect
from database.database import Database
from flask_cors import CORS
import secrets

app = Flask(__name__) # Iniciando a aplicação Flask

# Crie sua API secreta caso queira restringir acessos, configure mais tarde.
app.secret_key = 'segredo'
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32) # 32 é o tamanho da chave em bytes

CORS(app) # Evitando problemas de conexão via CORS

@app.route('/', methods=['GET']) # Rota raiz redirecionando para uma URL, em aplicações redirecione para a página do site da sua empresa ou projeto
def index():
    return redirect('https://github.com/IK-R-S/RESTful-Flask-API')

@app.route('/status', methods=['GET'])
def status():
    return {
        'framework': 'flask',
        'server': 'online',
        'status code': 200
    }

@app.route('/api/register', methods=['POST']) # Rota para registrar novos usuários
def register():
    # Pegando os dados enviados no Body da requisição
    data = request.json
    user = {
    "name": data['name'],
    "email": data['email'],
    "password": data['password'],
    }
    # Chamando a classe do banco de dados e executando seu método de Registro para usuários
    db = Database()
    response = db.registro(user)
    return response
        
@app.route('/api/login', methods=['POST']) # Rota para logar usuários
def login():
    # Pegando as credenciais enviadas no Body
    data = request.json
    user = {
        "email": data['email'],
        "password": data['password'],
    }
    # Chamando a classe do banco de dados e executando seu método de Login
    db = Database()
    response = db.login(user)
    return response

@app.route('/api/dashboard', methods=['GET']) # Rota para a dashboard do usuário
def dashboard():
    # Chamando a classe do banco de dados e executando seu método de Dashboard para usuários
    db = Database()
    response = db.dashboard()
    return response

@app.route('/api/create-item', methods=['POST']) # Rota para usuários criarem itens no banco de dados
def create_item():
    # Pegando os dados do novo item enviados no Body da requisição
    data = request.json
    item = {
    "name": data['name'],
    "description": data['description']
    }
    # Chamando a classe do banco de dados e executando seu método para  usuários criarem novos itens
    db = Database()
    response = db.create_item(item)
    return response

@app.route('/api/item/<item_name>', methods=['GET']) # Rota para pegar informações dos itens
def item(item_name):
    # Chamando a classe do banco de dados e executando seu método para retornar a descriçao de um item
    db = Database()
    response = db.item(item_name)
    return response
    
app.run(port=8000, debug=True) # Rodando sua aplicação em "localhost:8000"
