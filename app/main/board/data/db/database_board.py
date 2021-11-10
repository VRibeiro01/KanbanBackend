import sqlite3

from app.general.database import DataBase
from app.main.board.data.models.Board import Board


class database_board:

    path = DataBase.base_path + '/dbs/database.general'

    @staticmethod
    def create_db():
        try:
            sql = "CREATE TABLE BOARD(" \
                  "BOARD_ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "USER_ID INTEGER NOT NULL," \
                  "TITLE TEXT NOT NULL" \
                  ")"
            DataBase.make_no_response_query(sql, database_board.path)
        except sqlite3.OperationalError:
            print("Table Board Exists")

    @staticmethod
    def get_by_board_id(board_id):
        query = "SELECT * FROM BOARD WHERE BOARD_ID = {}".format(board_id)
        response = DataBase.make_multi_response_query(query, database_board.path)
        return Board(response[0][0], response[0][1], response[0][2])


    @staticmethod
    def get_by_user_id(user_id):
        query = "SELECT * FROM BOARD WHERE USER_ID = {}".format(user_id)
        return DataBase.make_multi_response_query(query, database_board.path)

    @staticmethod
    def insert_attempt(user_id, title):
        try:
            connection = sqlite3.connect(database_board.path)
            cursor = connection.cursor()
            query = "INSERT INTO BOARD(USER_ID, TITLE) VALUES('{}','{}')".format(user_id, title)
            cursor.execute(query)
            board_id = cursor.lastrowid
            connection.commit()
            connection.close()
            return database_board.get_by_board_id(board_id)
        except Exception:
            return "board already exist", 405