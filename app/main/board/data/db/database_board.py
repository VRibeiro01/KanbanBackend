import sqlite3
from sqlite3 import OperationalError

from app.general.database import DataBase
from app.main.board.data.models.Board import Board


class DatabaseBoard:

    path = DataBase.base_path + '/dbs/database'

    @staticmethod
    def create_db():
        try:
            sql = "CREATE TABLE BOARD(" \
                  "BOARD_ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "USER_ID INTEGER NOT NULL," \
                  "TITLE TEXT NOT NULL" \
                  ")"
            DataBase.make_no_response_query(sql, DatabaseBoard.path)
        except sqlite3.OperationalError:
            print("Table Board Exists")

    @staticmethod
    def get_by_board_id(board_id):
        query = "SELECT * FROM BOARD WHERE BOARD_ID = {}".format(board_id)
        answer = DataBase.make_multi_response_query(query, DatabaseBoard.path)
        if len(answer) == 1:
            user_obj = answer[0]
            if user_obj:
                board = Board(int(user_obj[0]), int(user_obj[1]), user_obj[2])
                return board
            else:
                return user_obj
        else:
            AttributeError()

    @staticmethod
    def get_by_user_id(user_id):
        query = "SELECT * FROM BOARD WHERE USER_ID = {}".format(user_id)
        moack_board_list = DataBase.make_multi_response_query(query, DatabaseBoard.path)
        board_list = []
        for board in moack_board_list:
            board_list.append(Board(int(board[0]), int(board[1]), board[2]))
        return board_list

    @staticmethod
    def update_board_by_board_id(board_id, user_id, title):
        query = "UPDATE BOARD SET USER_ID = '{}', TITLE = '{}' WHERE BOARD_ID = {}" \
            .format(user_id, title, board_id)
        DataBase.make_no_response_query(query, DatabaseBoard.path)
        response = str(DatabaseBoard.get_by_board_id(board_id))
        return response

    @staticmethod
    def delete_board_by_board_id(board_id):
        query = "DELETE FROM BOARD WHERE BOARD_ID = {}".format(board_id)
        response = DatabaseBoard.get_by_board_id(board_id)
        DataBase.make_no_response_query(query, DatabaseBoard.path)
        return response

    @staticmethod
    def insert_board(user_id, title):
        connection = sqlite3.connect(DatabaseBoard.path)
        cursor = connection.cursor()
        query = "INSERT INTO BOARD(USER_ID, TITLE) VALUES('{}','{}')".format(user_id, title)
        cursor.execute(query)
        user_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return DatabaseBoard.get_by_board_id(user_id)
