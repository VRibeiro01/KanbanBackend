import sqlite3
from sqlite3 import OperationalError

from app.general.database import DataBase


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
    def get_by_board_id(board_id):
        query = "SELECT * FROM COLUMN WHERE BOARD_ID = {}".format(board_id)
        return DataBase.make_multi_response_query(query, DatabaseColumn.path)

    @staticmethod
    def get_by_column_id(column_id):
        query = "SELECT * FROM COLUMN WHERE COLUMN_ID = {}".format(column_id)
        return DataBase.make_multi_response_query(query, DatabaseColumn.path)

    @staticmethod
    def update_column_by_column_id(column_id, board_id, title, position):
        query = "UPDATE COLUMN SET BOARD_ID = '{}', TITLE = '{}', POSITION = '{}' WHERE COLUMN_ID = {}" \
            .format(board_id, title, position, column_id)
        DataBase.make_no_response_query(query, DatabaseColumn.path)
        response = DatabaseColumn.get_by_column_id(column_id).to_json()
        return response

    @staticmethod
    def delete_column_by_column_id(column_id):
        query = "DELETE FROM TASK WHERE COLUMN_ID = {}".format(column_id)
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

