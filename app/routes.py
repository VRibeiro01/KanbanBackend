import json
import sqlite3

from flask import request
from password_strength import PasswordPolicy

from app.Models.User import User
from app.db.database_user import database_user
from app.db.database_board import database_board
from app import app

server_adress = "http://localhost/"
base_path = "."

policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1
)


database_user.create_db()
database_board.create_db()


@app.route('/user', methods=['POST'])
def add_user():
    json_payload = request.json
    username = json_payload['username']
    password = json_payload['password']
    try:
        returning = database_user.insert_attempt(username, password)
    except sqlite3.IntegrityError:
        return "username already exist", 300
    user = User(int(returning[0]), returning[1], returning[2])
    return user.toJson()


