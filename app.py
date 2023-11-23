import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS


CREATE_USERS_TABLE = ("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, login VARCHAR (255) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL,  manager BOOLEAN DEFAULT True)")

INSERT_NEW_USER = ("INSERT INTO users(login, password, manager) VALUES(%s, %s, %s)")

GET_USER = ("SELECT * FROM users WHERE login=%s")

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

def get_user(email):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_USER, (email,))
            user = cursor.fetchone()
    
    return user


@app.post("/users/signup")
def add_user():
    data = request.get_json()
    email = data['email']
    password = data['password']
    try:
        manager = data['manager']
    except KeyError:
        manager = True

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_NEW_USER, (email, password, manager))

    return {"message": f'User {email} added.'}, 201
