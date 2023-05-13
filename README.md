# API RESTful Flask

Esta API foi desenvolvida utilizando o framework Flask, com o objetivo de fornecer funcionalidades para o gerenciamento de usuários e itens em um banco de dados PostgreSQL. O código da API está dividido em três arquivos: `main.py`, `server.py` e `database.py`.

## Requisitos

Para utilizar esta API, é necessário ter instalado o Python 3 e o gerenciador de pacotes pip. Além disso, é necessário instalar as seguintes dependências:

```
Flask==2.0.0
flask-cors==3.0.10
psycopg2==2.9.6
psycopg2-binary==2.9.1
Werkzeug==2.0.0
```
Para facilitar execute a instalação automática pelo arquivo `requirements.txt`:
```
pip3 install -r requirements.txt
```

## Configuração do Banco de Dados

Antes de iniciar a utilização da API, é necessário configurar as informações do banco de dados PostgreSQL no arquivo `server.py`, preenchendo as variáveis `database_info['host']`, `database_info['database']`, `database_info['user']`, `database_info['password']` e `database_info['port']` com os valores correspondentes. Certifique-se de que o usuário configurado tenha permissão para criar tabelas e inserir dados.

## Utilização

Para iniciar a API, basta executar o arquivo `main.py`. A API estará disponível na porta 8000.
```
python3 main.py
```

### Rotas

A API possui as seguintes rotas:

#### GET /

Rota raiz, redireciona para um site específico, sendo o deste repositório no código fonte. Caso queira pode inserir qualquer outra URL ou trocar
a lógica para sua rota ter outra response como uma informação específica.

#### GET /status

Retorna informações sobre o status da API.

#### POST /api/register

Cria um novo usuário no banco de dados. É necessário enviar um objeto JSON com os campos "name", "email" e "password".

#### POST /api/login

Realiza a autenticação de um usuário com base no email e senha. É necessário enviar um objeto JSON com os campos "email" e "password".

#### GET /api/dashboard

Retorna informações do dashboard do usuário autenticado.

#### POST /api/create-item

Cria um novo item no banco de dados. É necessário enviar um objeto JSON com os campos "name" e "description".

#### GET /api/item/<item_name>

Retorna informações sobre um item específico no banco de dados.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou pull request.
