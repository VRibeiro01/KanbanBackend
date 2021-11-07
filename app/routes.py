import sqlite3

from flask import request
from password_strength import PasswordPolicy

from app.db.database_user import database_user
from app.db.database_board import database_board
from app import app

policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1
)


database_user.create_db()
database_board.create_db()


@app.route('/user', methods=['GET'])
def get_user_by_user_name():
    username = request.args.get("username")
    if username:
        try:
            return database_user.get_by_user_name(username).to_json()
        except AttributeError:
            return "user was not found", 404
    else:
        return "no username", 400


@app.route('/user', methods=['POST'])
def add_user():
    json_payload = request.json
    username = json_payload['username']
    password = json_payload['password']
    try:
        return database_user.insert_attempt(username, password).to_json()
    except sqlite3.IntegrityError:
        return "username already exist", 300
@app.route('/user/<user_id>',methods=['DELETE'])
def delete_user(user_id):
    try:
        return database_user.delete_user_by_user_id(user_id).to_json()
    except AttributeError:
        return "user was not found", 404


@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_user_id(user_id):
    try:
        return database_user.get_by_user_id(user_id).to_json()
    except AttributeError:
        return "user was not found", 404


@app.route('/user/<user_id>', methods=['PUT'])
def update_user_by_user_id(user_id):
    json_payload = request.json
    username = json_payload['username']
    password = json_payload['password']
    return database_user.update_user_by_user_id(user_id, username, password)

@app.route('/user/<user_id>/check_pw', methods=['GET'])
def check_pw(user_id):
    password = request.args.get("password")
    try:
        user = database_user.get_by_user_id(user_id)
        if user.password == password:
            return "password is correct",200
        else:
            return "password is not correct", 404
    except AttributeError:
        return "user was not found", 404

@app.route('/user/<user_id>/boards', methods=['GET'])
def get_boards_from_user_by_user_id(user_id):
    try:
        return database_board.get_by_user_id(user_id).to_json()
    except AttributeError:
        return "user was not found", 404
