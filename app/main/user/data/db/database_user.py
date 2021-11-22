import sqlite3
from sqlite3 import OperationalError

from app.main.user.data.models.User import User
from app.general.database import DataBase


class DatabaseUser:

    path = DataBase.base_path + '/dbs/database'

    @staticmethod
    def create_db():
        try:
            sql = "CREATE TABLE USER(" \
                    "USER_ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                    "USERNAME TEXT UNIQUE NOT NULL, " \
                    "PASSWORD TEXT NOT NULL" \
                  ")"
            DataBase.make_no_response_query(sql, DatabaseUser.path)
        except OperationalError:
            print("Table User Exists")

    @staticmethod
    def drop_db():
        try:
            sql = "DROP TABLE USER"
            DataBase.make_no_response_query(sql, DatabaseUser.path)
        except OperationalError:
            print("Table User dont Exists")

    @staticmethod
    def get_by_user_name(user_name):
        query = "SELECT * FROM USER WHERE USERNAME = '{}'".format(user_name)
        answer = DataBase.make_multi_response_query(query, DatabaseUser.path)
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
        response = DatabaseUser.get_by_user_id(user_id)
        query = "DELETE FROM USER WHERE USER_ID = {}".format(user_id)
        DataBase.make_no_response_query(query, DatabaseUser.path)
        return response

    @staticmethod
    def update_user_by_user_id(user_id, username, password):
        query = "UPDATE USER SET USERNAME = '{}', PASSWORD = '{}' WHERE USER_ID = {}".format(username, password, user_id)
        DataBase.make_no_response_query(query, DatabaseUser.path)
        return str(DatabaseUser.get_by_user_id(user_id))

    @staticmethod
    def get_by_user_id(user_id):
        query = "SELECT * FROM USER WHERE USER_ID = {}".format(user_id)
        answer = DataBase.make_multi_response_query(query, DatabaseUser.path)
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
    def insert_user(username, pw):
        connection = sqlite3.connect(DatabaseUser.path)
        cursor = connection.cursor()
        query = "INSERT INTO USER(USERNAME, PASSWORD) VALUES('{}','{}')".format(username, pw)
        cursor.execute(query)
        user_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return DatabaseUser.get_by_user_id(user_id)

