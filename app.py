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

def get_user_id(email):
    user_id = get_user(email)
    if (user_id):
        return user_id[0]
    return False
    

@app.post("/users/signup")
def add_user():
    data = request.get_json()
    email = data['email']
    password = data['password']
    # The try block is implemented to safeguard against the absence of a value for 'manager,' just as it is currently (only email and password can be passed to the database). However, if in the future we wish to pass a value for 'manager' as well, it is already implemented.
    try:
        manager = data['manager']
    except KeyError:
        manager = True

    user_id = get_user_id(email)
    if user_id:
        return {"message": f'User {email} already exists.'}, 409
    else:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_USERS_TABLE)
                cursor.execute(INSERT_NEW_USER, (email, password, manager))

        return {"message": f'User {email} added.'}, 201
     


@app.post("/users/login")
def login():
    data =  request.get_json()
    email = data['email']
    password = data['password']

    with connection:
        with connection.cursor() as cursor:
            pass

    return {"message": "You are logged in." }, 200