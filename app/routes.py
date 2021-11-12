import sqlite3

from flask import request
from password_strength import PasswordPolicy

from app.main.user.data.db.database_user import DatabaseUser
from app.main.board.data.db.database_board import DatabaseBoard
from app.main.board.data.db.database_column import DatabaseColumn
from app.main.board.data.db.database_task import DatabaseTask
from app import app

policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1
)


DatabaseUser.create_db()
DatabaseBoard.create_db()
DatabaseColumn.create_db()
DatabaseTask.create_db()


@app.route('/user', methods=['GET'])
def get_user_by_user_name():
    username = request.args.get("username")
    if username:
        try:
            return DatabaseUser.get_by_user_name(username).__repr__()
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
        return str(DatabaseUser.insert_user(username, password))
    except sqlite3.IntegrityError:
        return "username already exist", 300


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        return str(DatabaseUser.delete_user_by_user_id(user_id))
    except AttributeError:
        return "user was not found", 404


@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_user_id(user_id):
    try:
        return str(DatabaseUser.get_by_user_id(user_id))
    except AttributeError:
        return "user was not found", 404


@app.route('/user/<user_id>', methods=['PUT'])
def update_user_by_user_id(user_id):
    json_payload = request.json
    username = json_payload['username']
    password = json_payload['password']
    return str(DatabaseUser.update_user_by_user_id(user_id, username, password))


@app.route('/user/<user_id>/check_pw', methods=['GET'])
def check_pw(user_id):
    password = request.args.get("password")
    try:
        user = DatabaseUser.get_by_user_id(user_id)
        if user.password == password:
            return "password is correct",200
        else:
            return "password is not correct", 404
    except AttributeError:
        return "user was not found", 404


@app.route('/user/<user_id>/boards', methods=['GET'])
def get_boards_from_user_by_user_id(user_id):
    return str(DatabaseBoard.get_by_user_id(user_id))


# --------------------------BOARD-------------------------------------------

@app.route('/board', methods=['POST'])
def add_board():
    json_payload = request.json
    owner_id = json_payload['owner_id']
    title = json_payload['title']
    try:
        return str(DatabaseBoard.insert_board(owner_id, title))
    except sqlite3.IntegrityError:
        return "board already exist", 300


@app.route('/board/<board_id>', methods=['GET'])
def get_board_by_board_id(board_id):
    return str(DatabaseBoard.get_by_board_id(board_id))


@app.route('/board/<board_id>', methods=['PUT'])
def update_board_by_board_id(board_id):
    json_payload = request.json
    owner_id = json_payload['owner_id']
    title = json_payload['title']
    return DatabaseBoard.update_board_by_board_id(board_id, owner_id, title)


@app.route('/board/<board_id>', methods=['DELETE'])
def delete_board(board_id):
    return str(DatabaseBoard.delete_board_by_board_id(board_id))


@app.route('/board/<board_id>/columns', methods=['GET'])
def get_columns_from_board_by_board_id(board_id):
    try:
        return DatabaseColumn.get_by_board_id(board_id).to_json()
    except AttributeError:
        return "user was not found", 404
