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
            return str(DatabaseUser.get_by_user_name(username))
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
        if DatabaseUser.get_by_user_id(user_id):
            return str(DatabaseUser.delete_user_by_user_id(user_id))
        else:
            return "user was not found", 404
    except AttributeError:
        return "user was not found", 404


@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_user_id(user_id):
    try:
        if DatabaseUser.get_by_user_id(user_id):
            return str(DatabaseUser.get_by_user_id(user_id))
        else:
            return "user was not found", 404
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
            return "password is correct", 200
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
    try:
        if DatabaseBoard.get_by_board_id(board_id):
            return str(DatabaseBoard.get_by_board_id(board_id))
        else:
            return "board was not found", 404
    except AttributeError:
        return "board was not found", 404


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
        return str(DatabaseColumn.get_by_board_id(board_id))
    except AttributeError:
        return "user was not found", 404

# --------------------------COLUMNS-------------------------------------------


@app.route('/column', methods=['POST'])
def add_column():
    json_payload = request.json
    board_id = int(json_payload['board_id'])
    title = json_payload['title']
    position = int(json_payload['position'])
    try:
        return str(DatabaseColumn.insert_column(board_id, title, position))
    except sqlite3.IntegrityError:
        return "board already exist", 300


@app.route('/column/<column_id>', methods=['GET'])
def get_column_by_column_id(column_id):
    try:
        if DatabaseColumn.get_by_column_id(column_id):
            return str(DatabaseColumn.get_by_column_id(column_id))
        else:
            return "board was not found", 404
    except AttributeError:
        return "board was not found", 404


@app.route('/column/<column_id>', methods=['PUT'])
def update_column_by_column_id(column_id):
    json_payload = request.json
    board_id = int(json_payload['board_id'])
    title = json_payload['title']
    position = int(json_payload['position'])
    return str(DatabaseColumn.update_column_by_column_id(column_id, board_id, title, position))


@app.route('/column/<column_id>', methods=['DELETE'])
def delete_column(column_id):
    return str(DatabaseColumn.delete_column_by_column_id(column_id))


@app.route('/column/<column_id>/tasks', methods=['GET'])
def get_tasks_from_column_by_column_id(column_id):
    try:
        return str(DatabaseTask.get_by_column_id(column_id))
    except AttributeError:
        return "user was not found", 404


# --------------------------TASKS-------------------------------------------

@app.route('/task', methods=['POST'])
def add_task():
    json_payload = request.json
    column_id = int(json_payload['column_id'])
    worker = int(json_payload['worker'])
    title = json_payload['title']
    prio = int(json_payload['prio'])
    position = int(json_payload['position'])
    try:
        return str(DatabaseTask.insert_task(column_id, worker, title, prio, position))
    except sqlite3.IntegrityError:
        return "board already exist", 300


@app.route('/task/<task_id>', methods=['GET'])
def get_task_by_task_id(task_id):
    try:
        if DatabaseTask.get_by_task_id(task_id):
            return str(DatabaseTask.get_by_task_id(task_id))
        else:
            return "board was not found", 404
    except AttributeError:
        return "board was not found", 404

@app.route('/board/<board_id>/columns', methods=['GET'])
def get_columns_by_board_id(board_id):
    columns = database_column.get_by_board_id(board_id)
    print(json.dumps(columns))
    return json.dumps(columns)


@app.route('/task/<task_id>', methods=['PUT'])
def update_task_by_task_id(task_id):
    json_payload = request.json
    worker = int(json_payload['worker'])
    title = json_payload['title']
    prio = int(json_payload['prio'])
    position = int(json_payload['position'])
    return str(DatabaseTask.update_task_by_task_id(task_id, worker, title, prio, position))


@app.route('/task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    return str(DatabaseTask.delete_task_by_task_id(task_id))

