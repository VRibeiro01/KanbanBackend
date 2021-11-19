import sqlite3
from sqlite3 import OperationalError

from app.general.database import DataBase


class DatabaseTask:

    path = DataBase.base_path + '/dbs/database'

    @staticmethod
    def create_db():
        try:
            sql = "CREATE TABLE TASK(" \
                  "TASK_ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                  "COLUMN_ID INTEGER NOT NULL," \
                  "WORKER INTEGER," \
                  "TITLE TEXT NOT NULL," \
                  "PRIO INTEGER" \
                  "POSITION INTEGER" \
                  ")"
            DataBase.make_no_response_query(sql, DatabaseTask.path)
        except OperationalError:
            print("TABLE TASK EXISTS")

    @staticmethod
    def get_by_column_id(column_id):
        query = "SELECT * FROM TASK WHERE COLUMN_ID = {}".format(column_id)
        return DataBase.make_multi_response_query(query, DatabaseTask.path)

    @staticmethod
    def get_by_task_id(task_id):
        query = "SELECT * FROM TASK WHERE TASK_ID = {}".format(task_id)
        return DataBase.make_multi_response_query(query, DatabaseTask.path)

    @staticmethod
    def update_task_by_task_id(task_id, user_id, title, prio, position):
        query = "UPDATE TASK SET WORKER = '{}', TITLE = '{}', PRIO = '{}', POSITION = '{}' WHERE TASK_ID = {}"\
            .format(user_id, title, prio, position, task_id)
        DataBase.make_no_response_query(query, DatabaseTask.path)
        response = DatabaseTask.get_by_task_id(task_id).to_json()
        return response

    @staticmethod
    def delete_task_by_task_id(task_id):
        query = "DELETE FROM TASK WHERE TASK_ID = {}".format(task_id)
        response = DatabaseTask.get_by_task_id(task_id)
        DataBase.make_no_response_query(query, DatabaseTask.path)
        return response

    @staticmethod
    def insert_task(column_id, user_id, title, prio, position):
        connection = sqlite3.connect(DatabaseTask.path)
        cursor = connection.cursor()
        query = "INSERT INTO TASK(COLUMN_ID, WORKER, TITLE, PRIO, POSITION) VALUES('{}', '{}', '{}', '{}','{}')" \
            .format(column_id, user_id, title, prio, position)
        cursor.execute(query)
        user_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return DatabaseTask.get_by_column_id(user_id)
