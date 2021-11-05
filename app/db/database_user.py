import os
import datetime
import sqlite3

from app.db.database import DataBase


class database_user:

    path = DataBase.base_path + '/dbs/database.db'

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
            print("Table Exists")

    @staticmethod
    def get_by_user_name(user_name):
        query = "SELECT * FROM USER WHERE USERNAME = {}".format(user_name)
        return DataBase.make_multi_response_query(query, database_user.path)

    @staticmethod
    def get_by_user_id(user_id):
        query = "SELECT * FROM USER WHERE USER_ID = {}".format(user_id)
        return DataBase.make_multi_response_query(query, database_user.path)

    @staticmethod
    def insert_attempt(username, pw):
        connection = sqlite3.connect(database_user.path)
        cursor = connection.cursor()
        query = "INSERT INTO USER(USERNAME, PASSWORD) VALUES('{}','{}')".format(username, pw)
        cursor.execute(query)
        user_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return database_user.get_by_user_id(user_id)[0]

