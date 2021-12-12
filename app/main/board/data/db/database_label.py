import sqlite3
from sqlite3 import OperationalError

from app.general.database import DataBase
from app.main.board.data.models.Label import Label


class DatabaseLabel:

    path = DataBase.base_path + '/dbs/database'

    @staticmethod
    def create_db():
        try:
            sql = "CREATE TABLE LABEL(" \
                  "LABEL_ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "TITLE TEXT NOT NULL" \
                  ")"
            DataBase.make_no_response_query(sql, DatabaseLabel.path)
        except OperationalError:
            print("TABLE LABEL EXISTS")

    @staticmethod
    def drop_db():
        try:
            sql = "DROP TABLE LABEL"
            DataBase.make_no_response_query(sql, DatabaseLabel.path)
        except OperationalError:
            print("Table LABEL dont Exists")

    @staticmethod
    def get_by_label_id(label_id):
        query = "SELECT * FROM LABEL WHERE LABEL_ID = {}".format(label_id)
        answer = DataBase.make_multi_response_query(query, DatabaseLabel.path)
        if len(answer) == 1:
            user_obj = answer[0]
            if user_obj:
                label = Label(int(user_obj[0]), int(user_obj[1]), user_obj[2])
                return label
            else:
                return user_obj
        else:
            AttributeError()

    @staticmethod
    def get_by_board_id(board_id):
        query = "SELECT * FROM LABEL WHERE BOARD_ID = {}".format(board_id)
        answer = DataBase.make_multi_response_query(query, DatabaseLabel.path)
        list_labels = []
        for user_obj in answer:
            if user_obj:
                list_labels.append(Label(int(user_obj[0]), int(user_obj[1]), user_obj[2]))
        else:
            AttributeError()
        return list_labels

    @staticmethod
    def update_label_by_label_id(label_id, board_id, title):
        query = "UPDATE LABEL SET TITLE = '{}' SET BOARD_ID = '{}' WHERE LABEL_ID = {}"\
            .format(title, board_id, label_id)
        DataBase.make_no_response_query(query, DatabaseLabel.path)
        response = DatabaseLabel.get_by_label_id(label_id)
        return response

    @staticmethod
    def delete_label_by_task_id(label_id):
        query = "DELETE FROM LABEL WHERE LABEL_ID = {}".format(label_id)
        response = DatabaseLabel.get_by_label_id(label_id)
        DataBase.make_no_response_query(query, DatabaseLabel.path)
        return response

    @staticmethod
    def insert_task(board_id, title):
        connection = sqlite3.connect(DatabaseLabel.path)
        cursor = connection.cursor()
        query = "INSERT INTO LABEL(BOARD_ID, TITLE) VALUES('{}', '{}', '{}')" \
            .format(board_id, title)
        cursor.execute(query)
        label_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return DatabaseLabel.get_by_label_id(label_id)
