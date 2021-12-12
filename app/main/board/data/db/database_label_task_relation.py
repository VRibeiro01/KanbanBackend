import sqlite3
from sqlite3 import OperationalError

from app.general.database import DataBase
from app.main.board.data.db.database_label import DatabaseLabel
from app.main.board.data.models.Label import Label
from app.main.board.data.models.LabelTaskRelation import LabelTaskRelation


class DatabaseLabelTaskRelation:

    path = DataBase.base_path + '/dbs/database'

    @staticmethod
    def create_db():
        try:
            sql = "CREATE TABLE LABEL_TASK_RELATION(" \
                  "LABEL_ID INTEGER," \
                  "TASK_ID INTEGER" \
                  ")"
            DataBase.make_no_response_query(sql, DatabaseLabelTaskRelation.path)
        except OperationalError:
            print("TABLE LABEL_TASK_RELATION EXISTS")

    @staticmethod
    def drop_db():
        try:
            sql = "DROP TABLE LABEL_TASK_RELATION"
            DataBase.make_no_response_query(sql, DatabaseLabelTaskRelation.path)
        except OperationalError:
            print("Table LABEL_TASK_RELATION dont Exists")

    @staticmethod
    def get_by_label_id_and_task_id(label_id, task_id):
        query = "SELECT * FROM LABEL_TASK_RELATION WHERE LABEL_ID = {} AND TASK_ID = {}".format(label_id, task_id)
        answer = DataBase.make_multi_response_query(query, DatabaseLabelTaskRelation.path)
        if answer and len(answer) == 1:
            user_obj = answer[0]
            if user_obj:
                label = LabelTaskRelation(int(user_obj[0]), int(user_obj[1]))
                return label
        AttributeError()

    @staticmethod
    def get_labels_by_task_id(task_id):
        query = "SELECT * FROM LABEL_TASK_RELATION WHERE TASK_ID = {}".format(task_id)
        try:
            answer = DataBase.make_multi_response_query(query, DatabaseLabelTaskRelation.path)
            label_ids = []
            for obj in answer:
                if obj:
                    label_relation = LabelTaskRelation(int(obj[0]), int(obj[1]))
                    label = DatabaseLabel.get_by_label_id(label_relation.label_id)
                    label_ids.append(label)
                else:
                    AttributeError()
            return label_ids
        except OperationalError:
            return []

    @staticmethod
    def delete_task_by_task_id_and_task_id(label_id, task_id):
        query = "DELETE FROM LABEL_TASK_RELATION WHERE LABEL_ID = {} AND TASK_ID = {}".format(label_id, task_id)
        response = DatabaseLabelTaskRelation.get_by_label_id_and_task_id(label_id, task_id)
        DataBase.make_no_response_query(query, DatabaseLabelTaskRelation.path)
        return response

    @staticmethod
    def insert_task_label_relation(label_id, task_id):
        connection = sqlite3.connect(DatabaseLabelTaskRelation.path)
        cursor = connection.cursor()
        query = "INSERT INTO LABEL_TASK_RELATION(LABEL_ID, TASK_ID) VALUES('{}', '{}')" \
            .format(label_id, task_id)
        cursor.execute(query)
        connection.commit()
        connection.close()
        return DatabaseLabelTaskRelation.get_by_label_id_and_task_id(label_id, task_id)
