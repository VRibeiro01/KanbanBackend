import sqlite3
from sqlite3 import OperationalError

from app.general.database import DataBase
from app.main.board.data.db.database_label_task_relation import DatabaseLabelTaskRelation
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
            label_list = DatabaseLabelTaskRelation.get_labels_by_task_id(int(task_obj[0]))
            board_list.append(Task(int(task_obj[0]), int(task_obj[1]), int(task_obj[2]), task_obj[3], int(task_obj[4]), int(task_obj[5]), label_list))
        return board_list

    @staticmethod
    def get_by_task_id(task_id):
        query = "SELECT * FROM TASK WHERE TASK_ID = {}".format(task_id)
        answer = DataBase.make_multi_response_query(query, DatabaseTask.path)
        if len(answer) == 1:
            task_obj = answer[0]
            if task_obj:
                label_list = DatabaseLabelTaskRelation.get_labels_by_task_id(task_id)
                task = Task(int(task_obj[0]), int(task_obj[1]), int(task_obj[2]), task_obj[3], int(task_obj[4]), int(task_obj[5]), label_list)
                return task
        AttributeError()

    @staticmethod
    def update_task_by_task_id(task_id, user_id, title, prio, position, label_id_list):
        old_response = DatabaseTask.get_by_task_id(task_id)
        # manage labels
        for label_saved in old_response.labels:
            if label_saved.label_id not in label_id_list:
                DatabaseLabelTaskRelation.delete_task_by_task_id_and_task_id(label_saved.label_id, task_id)
        for label_id in label_id_list:
            try:
                returning = DatabaseLabelTaskRelation.get_by_label_id_and_task_id(label_id, task_id)
                if not returning:
                    DatabaseLabelTaskRelation.insert_task_label_relation(label_id, task_id)
            except AssertionError:
                DatabaseLabelTaskRelation.insert_task_label_relation(label_id, task_id)

        query = "UPDATE TASK SET WORKER = '{}', TITLE = '{}', PRIO = '{}', POSITION = '{}' WHERE TASK_ID = {}"\
            .format(user_id, title, prio, position, task_id)
        DataBase.make_no_response_query(query, DatabaseTask.path)
        for label_id in label_id_list:
            try:
                returning = DatabaseLabelTaskRelation.get_by_label_id_and_task_id(label_id, task_id)
                if not returning:
                    DatabaseLabelTaskRelation.insert_task_label_relation(label_id, task_id)
            except AttributeError:
                DatabaseLabelTaskRelation.insert_task_label_relation(label_id, task_id)

        response = DatabaseTask.get_by_task_id(task_id)
        return response

    @staticmethod
    def delete_task_by_task_id(task_id):
        query = "DELETE FROM TASK WHERE TASK_ID = {}".format(task_id)
        response = DatabaseTask.get_by_task_id(task_id)
        DataBase.make_no_response_query(query, DatabaseTask.path)
        label_relation_list = DatabaseLabelTaskRelation.get_labels_by_task_id(task_id)
        for label_relation in label_relation_list:
            DatabaseLabelTaskRelation.delete_task_by_task_id_and_task_id(label_relation.label_id, label_relation.task_id)
        return response

    @staticmethod
    def insert_task(column_id, user_id, title, prio, position, label_id_list):
        connection = sqlite3.connect(DatabaseTask.path)
        cursor = connection.cursor()
        query = "INSERT INTO TASK(COLUMN_ID, WORKER, TITLE, PRIO, POSITION) VALUES('{}', '{}', '{}', {}, {})" \
            .format(column_id, user_id, title, prio, position)
        cursor.execute(query)
        task_id = cursor.lastrowid
        connection.commit()
        connection.close()
        print(label_id_list)
        for label_id in label_id_list:
            try:
                returning = DatabaseLabelTaskRelation.get_by_label_id_and_task_id(label_id, task_id)
                if not returning:
                    DatabaseLabelTaskRelation.insert_task_label_relation(label_id, task_id)
            except AssertionError:
                DatabaseLabelTaskRelation.insert_task_label_relation(label_id, task_id)
        return DatabaseTask.get_by_task_id(task_id)
