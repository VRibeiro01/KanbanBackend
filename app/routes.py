import datetime
import json
import sqlite3

from flask import request
from password_strength import PasswordPolicy

from app.main.board.data.db.database_label import DatabaseLabel
from app.main.board.data.db.database_label_task_relation import DatabaseLabelTaskRelation
from app.main.user.data.db.database_user import DatabaseUser
from app.main.board.data.db.database_board import DatabaseBoard
from app.main.board.data.db.database_column import DatabaseColumn
from app.main.board.data.db.database_task import DatabaseTask
from app import app
import test.testdaten as test_daten

policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1
)


DatabaseUser.create_db()
DatabaseBoard.create_db()
DatabaseColumn.create_db()
DatabaseTask.create_db()
DatabaseLabel.create_db()
DatabaseLabelTaskRelation.create_db()


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


@app.route('/user/login', methods=['PUT'])
def login_user():
    json_payload = request.json
    username = json_payload['username']
    password = json_payload['password']
    try:
        user = DatabaseUser.get_by_user_name(username)
        DatabaseUser.check_pw(user.user_id, password)
        session_id = DatabaseUser.get_new_session_token(user.user_id)
        return str(session_id), 200
    except AttributeError:
        return "user was not found", 404


@app.route('/user/<user_id>/logout', methods=['PUT'])
def logout_user(user_id):
    try:
        DatabaseUser.delete_session_token(user_id)
        return "User logged out"
    except AttributeError:
        return "user was not found", 404


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        session_token = request.args.get("session_token")
        user = DatabaseUser.get_by_user_id(user_id)
        if session_token == user.session_token and user.vali_date_from_token and user.vali_date_from_token > datetime.datetime.now().timestamp():
            user = DatabaseUser.delete_user_by_user_id(user_id)
            if user:
                return str(user)
            else:
                return "user was not found", 404
        else:
            return "user was not logged in", 400
    except AttributeError:
        return "user was not found", 404


@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_user_id(user_id):
    try:
        user = DatabaseUser.get_by_user_id(user_id)
        if user:
            session_token = request.args.get("session_token")
            user = DatabaseUser.get_by_user_id(user_id)
            if session_token == user.session_token and user.vali_date_from_token and user.vali_date_from_token > datetime.datetime.now().timestamp():
                return str(user)
            else:
                return "user was not logged in", 400
        else:
            return "user was not found", 404
    except AttributeError:
        return "user was not found", 404


@app.route('/user/<user_id>', methods=['PUT'])
def update_user_by_user_id(user_id):
    json_payload = request.json
    username = json_payload['username']
    password = json_payload['password']
    try:
        session_token = request.args.get("session_token")
        user = DatabaseUser.get_by_user_id(user_id)
        if session_token == user.session_token and user.vali_date_from_token and user.vali_date_from_token > datetime.datetime.now().timestamp():
                return str(DatabaseUser.update_user_by_user_id(user_id, username, password))
        else:
            return "user was not logged in", 400
    except AttributeError:
        return "user was not found", 404


@app.route('/user/<user_id>/boards', methods=['GET'])
def get_boards_from_user_by_user_id(user_id):
    return str(DatabaseBoard.get_by_user_id(user_id))


# --------------------------BOARD------------------------------------------

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
        board = DatabaseBoard.get_by_board_id(board_id)
        if board:
            return str(board)
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
    try:
        board = DatabaseBoard.delete_board_by_board_id(board_id)
        if board:
            return str(board)
        else:
            return "board was not found", 404
    except AttributeError:
        return "board was not found", 404


@app.route('/board/<board_id>/columns', methods=['GET'])
def get_columns_from_board_by_board_id(board_id):
    try:
        return str(DatabaseColumn.get_by_board_id(board_id))
    except AttributeError:
        return "user was not found", 404

# --------------------------COLUMNS-------------------------------------------

# @app.after_request
# def apply_caching(response):
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     response.headers["Access-Control-Allow-Headers"] = "*"
#     return response


@app.route('/column', methods=['POST'])
def add_column():
    json_payload = request.json
    board_id = int(json_payload['board_id'])
    title = json_payload['title']
    position = int(json_payload['position'])
    try:
        return str(DatabaseColumn.insert_column(board_id, title, position))
    except sqlite3.IntegrityError:
        return "column already exist", 300


@app.route('/column/<column_id>', methods=['GET'])
def get_column_by_column_id(column_id):
    try:
        column = DatabaseColumn.get_by_column_id(column_id)
        if column:
            return str(column)
        else:
            return "column was not found", 404
    except AttributeError:
        return "column was not found", 404


@app.route('/column/<column_id>', methods=['PUT'])
def update_column_by_column_id(column_id):
    json_payload = request.json
    board_id = int(json_payload['board_id'])
    title = json_payload['title']
    position = int(json_payload['position'])
    return str(DatabaseColumn.update_column_by_column_id(column_id, board_id, title, position))


@app.route('/column/<column_id>', methods=['DELETE'])
def delete_column(column_id):
    try:
        column = DatabaseColumn.delete_column_by_column_id(column_id)
        if column:
            return str(column)
        else:
            return "column was not found", 404
    except AttributeError:
        return "column was not found", 404


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
    deadline = float(json_payload['deadline'])
    labels = list(json_payload['labels'])
    try:
        return str(DatabaseTask.insert_task(column_id, worker, title, prio, position, deadline, labels))
    except sqlite3.IntegrityError:
        return "task already exist", 300


@app.route('/task/<task_id>', methods=['GET'])
def get_task_by_task_id(task_id):
    try:
        task = DatabaseTask.get_by_task_id(task_id)
        if task:
            return str(task)
        else:
            return "task was not found", 404
    except AttributeError:
        return "task was not found", 404


@app.route('/task/worker/<worker_id>', methods=['GET'])
def get_columns_by_board_id(worker_id):
    try:
        return str(DatabaseTask.get_by_worker_id(worker_id))
    except AttributeError:
        return "user was not found", 404


@app.route('/task/<task_id>', methods=['PUT'])
def update_task_by_task_id(task_id):
    json_payload = request.json
    worker = None
    if "worker" in json_payload:
        worker = int(json_payload['worker'])
    title = None
    if "title" in json_payload:
        title = json_payload['title']
    prio = None
    if "prio" in json_payload:
        prio = int(json_payload['prio'])
    position = None
    if "position" in json_payload:
        position = int(json_payload['position'])
    deadline = None
    if "deadline" in json_payload:
        deadline = float(json_payload['deadline'])
    labels = None
    if "labels" in json_payload:
        labels = list(json_payload['labels'])
    column_id = None
    if "column_id" in json_payload:
        column_id = int(json_payload['column_id'])
    return str(DatabaseTask.update_task_by_task_id(task_id, column_id, worker, title, prio, position, deadline, labels))


@app.route('/task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = DatabaseTask.delete_task_by_task_id(task_id)
        if task:
            return str(task)
        else:
            return "task was not found", 404
    except AttributeError:
        return "task was not found", 404

# --------------------------LABEL-------------------------------------------


@app.route('/label', methods=['POST'])
def add_label():
    json_payload = request.json
    title = json_payload['title']
    board_id = int(json_payload['board_id'])
    try:
        return str(DatabaseLabel.insert_label(board_id, title))
    except sqlite3.IntegrityError:
        return "board already exist", 300


@app.route('/label/<label_id>', methods=['GET'])
def get_label_by_label_id(label_id):
    try:
        task = DatabaseLabel.get_by_label_id(label_id)
        if task:
            return str(task)
        else:
            return "label was not found", 404
    except AttributeError:
        return "label was not found", 404


@app.route('/label/<label_id>', methods=['PUT'])
def update_label_by_label_id(label_id):
    json_payload = request.json
    board_id = int(json_payload['board_id'])
    title = json_payload['title']
    return str(DatabaseLabel.update_label_by_label_id(label_id, board_id, title))


@app.route('/label/<label_id>', methods=['DELETE'])
def delete_label(label_id):
    try:
        label = DatabaseLabel.delete_label_by_task_id(label_id)
        if label:
            return str(label)
        else:
            return "label was not found", 404
    except AttributeError:
        return "label was not found", 404


@app.route('/fill_data', methods=['GET'])
def fill_test_data():
    test_daten.run()
    return "inserted"
