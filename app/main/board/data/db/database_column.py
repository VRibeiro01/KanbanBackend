import sqlite3

from app.general.database import DataBase
from app.main.board.data.models.Column import Column


class database_column:

    path = DataBase.base_path + '/dbs/database.general'

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
        answer = DataBase.make_multi_response_query(query, database_column.path)
        column_count = len(answer)
        column_list = []
        x = 0
        while x < column_count:
            c_id = answer[x][0]
            b_id = answer[x][1]
            title = answer[x][2]
            position = answer[x][3]
            column_element = Column(c_id, b_id, title, position).to_json()
            column_list.append(column_element)
            x += 1
        return column_list


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
