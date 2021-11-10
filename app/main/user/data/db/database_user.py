import sqlite3

from app.main.board.data.models.Board import Board
from app.main.user.data.models.User import User
from app.general.database import DataBase


class database_user:

    path = DataBase.base_path + '/dbs/database.general'

    @staticmethod
    def create_db():
        try:
            sql = "CREATE TABLE USER(" \
                    "USER_ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                    "USERNAME TEXT UNIQUE NOT NULL, " \
                    "PASSWORD TEXT NOT NULL" \
                  ")"
            DataBase.make_no_response_query(sql, database_user.path)
        except sqlite3.OperationalError:
            print("Table User Exists")

    @staticmethod
    def get_by_user_name(user_name):
        query = "SELECT * FROM USER WHERE USERNAME = '{}'".format(user_name)
        answer = DataBase.make_multi_response_query(query, database_user.path)
        if answer and len(answer) == 1:
            user_obj = answer[0]
            if user_obj:
                user = User(int(user_obj[0]), user_obj[1], user_obj[2])
                return user
            else:
                return user_obj
        else:
            AttributeError()
    @staticmethod
    def delete_user_by_user_id(user_id):
        query = "Delete From USER WHERE USER_ID = {}".format(user_id)
        response = database_user.get_by_user_id(user_id)
        DataBase.make_no_response_query(query,database_user.path)
        return response
    @staticmethod
    def update_user_by_user_id(user_id, username, password):
        query = "UPDATE USER SET USERNAME = '{}', PASSWORD = '{}' WHERE USER_ID = {}".format(username, password, user_id)
        DataBase.make_no_response_query(query, database_user.path)
        response = database_user.get_by_user_id(user_id).to_json()
        return response

    @staticmethod
    def get_by_user_id(user_id):
        query = "SELECT * FROM USER WHERE USER_ID = {}".format(user_id)
        answer = DataBase.make_multi_response_query(query, database_user.path)
        if len(answer) == 1:
            user_obj = answer[0]
            if user_obj:
                user = User(int(user_obj[0]), user_obj[1], user_obj[2])
                return user
            else:
                return user_obj
        else:
            AttributeError()

    @staticmethod
    def insert_attempt(username, pw):
        connection = sqlite3.connect(database_user.path)
        cursor = connection.cursor()
        query = "INSERT INTO USER(USERNAME, PASSWORD) VALUES('{}','{}')".format(username, pw)
        cursor.execute(query)
        user_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return database_user.get_by_user_id(user_id)




