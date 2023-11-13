import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

CREATE_USERS_TABLE = ("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, login VARCHAR (255) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL,  manager BOOLEAN DEFAULT True)")

INSERT_NEW_USER = ("INSERT INTO users(login, password, manager) VALUES(%s, %s, %s)")

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


@app.get("/users")
def get_users():
    return "Hello"

@app.post("/users/signup")
def add_user():
    data = request.get_json()
    login = data['login']
    password = data['password']
    manager = data['manager']

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_NEW_USER, (login, password, manager))

    return {"message": f'User {login} added.'}, 201
