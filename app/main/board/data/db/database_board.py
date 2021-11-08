import sqlite3

from app.general.database import DataBase


class database_board:

    path = DataBase.base_path + '/dbs/database.general'

    @staticmethod
    def create_db():
        try:
            sql = "CREATE TABLE BOARD(" \
                  "BOARD_ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "USER_ID INTEGER NOT NULL" \
                  "TITLE TEXT NOT NULL" \
                  ")"
            DataBase.make_no_response_query(sql, database_board.path)
        except sqlite3.OperationalError:
            print("Table Exists")

    @staticmethod
    def get_by_board_id(board_id):
        query = "SELECT * FROM BOARD WHERE BOARD_ID = {}".format(board_id)
        return DataBase.make_multi_response_query(query, database_board.path)

    @staticmethod
    def get_by_user_id(user_id):
        query = "SELECT * FROM BOARD WHERE USER_ID = {}".format(user_id)
        return DataBase.make_multi_response_query(query, database_board.path)

    @staticmethod
    def insert_attempt(user_id, title):
        try:
            query = "INSERT INTO BOARD(USER_ID, TITLE) VALUES('{}','{}')".format(user_id, title)
            return DataBase.make_multi_response_query(query, database_board.path)
        except Exception:
            return "board already exist", 405