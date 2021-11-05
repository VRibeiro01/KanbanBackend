import sqlite3

from app.db.database import DataBase


class database_column:

    path = DataBase.base_path + '/dbs/database.db'

    @staticmethod
    def create_db():
        try:
            sql = "CREATE TABLE COLUMN(" \
                  "COLUMN_ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "BOARD_ID INTEGER NOT NULL," \
                  "TITLE TEXT NOT NULL," \
                  "POSITION INTEGER" \
                  ")"
            DataBase.make_no_response_query(sql, database_column.path)
        except sqlite3.OperationalError:
            print("Table Exists")

    @staticmethod
    def get_by_board_id(board_id):
        query = "SELECT * FROM COLUMN WHERE BOARD_ID = {}".format(board_id)
        return DataBase.make_multi_response_query(query, database_column.path)

    @staticmethod
    def get_by_user_id(user_id):
        query = "SELECT * FROM COLUMN WHERE USER_ID = {}".format(user_id)
        return DataBase.make_multi_response_query(query, database_column.path)

    @staticmethod
    def insert_attempt(user_id, title):
        try:
            query = "INSERT INTO COLUMN(USER_ID, TITLE) VALUES('{}','{}')".format(user_id, title)
            return DataBase.make_multi_response_query(query, database_column.path)
        except Exception:
            return "board already exist", 405