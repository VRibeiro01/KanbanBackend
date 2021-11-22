import sqlite3
from sqlite3 import OperationalError

from app.general.database import DataBase
from app.main.board.data.models.Column import Column


class DatabaseColumn:

    path = DataBase.base_path + '/dbs/database'

    @staticmethod
    def create_db():
        try:
            sql = "CREATE TABLE COLUMN(" \
                  "COLUMN_ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "BOARD_ID INTEGER NOT NULL," \
                  "TITLE TEXT NOT NULL," \
                  "POSITION INTEGER" \
                  ")"
            DataBase.make_no_response_query(sql, DatabaseColumn.path)
        except OperationalError:
            print("TABLE COLUMN EXISTS")

    @staticmethod
    def drop_db():
        try:
            sql = "DROP TABLE COLUMN"
            DataBase.make_no_response_query(sql, DatabaseColumn.path)
        except OperationalError:
            print("Table Column dont Exists")

    @staticmethod
    def get_by_board_id(board_id):
        query = "SELECT * FROM COLUMN WHERE BOARD_ID = {}".format(board_id)
        mock_column_list = DataBase.make_multi_response_query(query, DatabaseColumn.path)
        board_list = []
        for column in mock_column_list:
            board_list.append(Column(int(column[0]), int(column[1]), column[2], column[3]))
        return board_list

    @staticmethod
    def get_by_column_id(column_id):
        query = "SELECT * FROM COLUMN WHERE COLUMN_ID = {}".format(column_id)
        answer = DataBase.make_multi_response_query(query, DatabaseColumn.path)
        if len(answer) == 1:
            user_obj = answer[0]
            if user_obj:
                column = Column(int(user_obj[0]), int(user_obj[1]), user_obj[2], int(user_obj[3]))
                return column
            else:
                return user_obj
        else:
            AttributeError()

    @staticmethod
    def update_column_by_column_id(column_id, board_id, title, position):
        query = "UPDATE COLUMN SET BOARD_ID = '{}', TITLE = '{}', POSITION = '{}' WHERE COLUMN_ID = {}" \
            .format(board_id, title, position, column_id)
        DataBase.make_no_response_query(query, DatabaseColumn.path)
        response = DatabaseColumn.get_by_column_id(column_id)
        return response

    @staticmethod
    def delete_column_by_column_id(column_id):
        query = "DELETE FROM COLUMN WHERE COLUMN_ID = {}".format(column_id)
        response = DatabaseColumn.get_by_column_id(column_id)
        DataBase.make_no_response_query(query, DatabaseColumn.path)
        return response

    @staticmethod
    def insert_column(board_id, title, position):
        connection = sqlite3.connect(DatabaseColumn.path)
        cursor = connection.cursor()
        query = "INSERT INTO COLUMN(BOARD_ID, TITLE, POSITION) VALUES('{}','{}', '{}')"\
            .format(board_id, title, position)
        cursor.execute(query)
        user_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return DatabaseColumn.get_by_column_id(user_id)

