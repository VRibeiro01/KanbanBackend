import sqlite3
from sqlite3 import OperationalError

from app.general.database import DataBase
from app.main.board.data.models.Task import Task


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
                  "PRIO INTEGER," \
                  "POSITION INTEGER" \
                  ")"
            DataBase.make_no_response_query(sql, DatabaseTask.path)
        except OperationalError:
            print("TABLE TASK EXISTS")

    @staticmethod
    def drop_db():
        try:
            sql = "DROP TABLE TASK"
            DataBase.make_no_response_query(sql, DatabaseTask.path)
        except OperationalError:
            print("Table Task dont Exists")

    @staticmethod
    def get_by_column_id(column_id):
        query = "SELECT * FROM TASK WHERE COLUMN_ID = {}".format(column_id)
        mock_column_list = DataBase.make_multi_response_query(query, DatabaseTask.path)
        board_list = []
        for task_obj in mock_column_list:
            board_list.append(Task(int(task_obj[0]), int(task_obj[1]), int(task_obj[2]), task_obj[3], int(task_obj[4]), int(task_obj[5])))
        return board_list

    @staticmethod
    def get_by_task_id(task_id):
        query = "SELECT * FROM TASK WHERE TASK_ID = {}".format(task_id)
        answer = DataBase.make_multi_response_query(query, DatabaseTask.path)
        if len(answer) == 1:
            user_obj = answer[0]
            if user_obj:
                task = Task(int(user_obj[0]), int(user_obj[1]), int(user_obj[2]), user_obj[3], int(user_obj[4]), int(user_obj[5]))
                return task
            else:
                return user_obj
        else:
            AttributeError()

    @staticmethod
    def update_task_by_task_id(task_id, user_id, title, prio, position):
        query = "UPDATE TASK SET WORKER = '{}', TITLE = '{}', PRIO = '{}', POSITION = '{}' WHERE TASK_ID = {}"\
            .format(user_id, title, prio, position, task_id)
        DataBase.make_no_response_query(query, DatabaseTask.path)
        response = DatabaseTask.get_by_task_id(task_id)
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
        query = "INSERT INTO TASK(COLUMN_ID, WORKER, TITLE, PRIO, POSITION) VALUES('{}', '{}', '{}', {}, {})" \
            .format(column_id, user_id, title, prio, position)
        cursor.execute(query)
        user_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return DatabaseTask.get_by_task_id(user_id)
