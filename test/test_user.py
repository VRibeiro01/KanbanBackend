import json
from json import JSONDecodeError

from app import app
import unittest

from app.main.board.data.db.database_board import DatabaseBoard
from app.main.board.data.db.database_column import DatabaseColumn
from app.main.board.data.db.database_task import DatabaseTask
from app.main.user.data.db.database_user import DatabaseUser


class UserTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        DatabaseUser.path = '../dbs/database_test'
        DatabaseUser.create_db()
        DatabaseBoard.path = '../dbs/database_test'
        DatabaseBoard.create_db()
        DatabaseColumn.path = '../dbs/database_test'
        DatabaseColumn.create_db()
        DatabaseTask.path = '../dbs/database_test'
        DatabaseTask.create_db()

    def tearDown(self):
        DatabaseUser.drop_db()
        DatabaseBoard.drop_db()
        DatabaseColumn.drop_db()
        DatabaseTask.drop_db()

    def compare_returns(self, function, url, key, value, name=None):
        if key == value:
            print("\t" + function + ": " + url + " -> " + (name + ": " if name else ": ") + str(key) + " == " + str(value) + " ✔️")
        else:
            print("\t" + function + ": " + url + " -> " + (name + ": " if name else ": ") + str(key) + " != " + str(value) + " ❌")
        self.assertEqual(key, value)

    def expectGetStatus(self, c, url, status, expected=None):
        if expected is None:
            expected = []
        response = c.get(url)
        self.compare_returns("GET", url, response.status_code, status, name="status")
        try:
            response_json = json.loads(response.data)
            for expected_item in expected:
                self.compare_returns("GET", url, response_json[expected_item[0]], expected_item[1], name=expected_item[0])
            return response_json
        except JSONDecodeError:
            return None

    def expectPostStatus(self, c, url, form, status, expected=None):
        if expected is None:
            expected = []
        response = c.post(url, json=form, follow_redirects=True)
        self.compare_returns("POST", url, response.status_code, status, name="status")
        response_json = json.loads(response.data)
        for expected_item in expected:
            self.compare_returns("POST", url, response_json[expected_item[0]], expected_item[1], name=expected_item[0])
        return response_json

    def expectPutStatus(self, c, url, form, status, expected=None):
        if expected is None:
            expected = []
        response = c.put(url, json=form)
        self.compare_returns("PUT", url, response.status_code, status, name="status")
        response_json = json.loads(response.data)
        for expected_item in expected:
            self.compare_returns("PUT", url, response_json[expected_item[0]], expected_item[1], name=expected_item[0])
        return response_json

    def expectDeleteStatus(self, c, url, status, expected=None):
        if expected is None:
            expected = []
        response = c.delete(url)
        self.compare_returns("DELETE", url, response.status_code, status, name="status")
        response_json = json.loads(response.data)
        for expected_item in expected:
            self.compare_returns("DELETE", url, response_json[expected_item[0]], expected_item[1], name=expected_item[0])
        return response_json

    def test_user(self):
        with self.client as c:
            print("TEST THE USER")
            response = self.expectPostStatus(c, "/user",
                                             dict(username="ferdi",password="123456789"),
                                             200,
                                             expected=[["username", "ferdi"],["password", "123456789"]])

            self.expectGetStatus(c, "/user/{}".format(response["user_id"]), 200)

            self.expectPutStatus(c, "/user/{}".format(response["user_id"]),
                                 dict(username="ferdinando", password="123456789"),
                                 200,
                                 expected=[["username", "ferdinando"], ["password", "123456789"]]
                                 )

            self.expectDeleteStatus(c, "/user/{}".format(response["user_id"]),
                                    200,
                                    expected=[["username", "ferdinando"], ["password", "123456789"]])

            self.expectGetStatus(c, "/user/{}".format(response["user_id"]), 404)

    def test_board(self):
        with self.client as c:
            print("TEST THE BOARD")
            response = self.expectPostStatus(c, "/user",
                                             dict(username="ferdi",password="123456789"),
                                             200,
                                             expected=[["username", "ferdi"],["password", "123456789"]])

            response_board = self.expectPostStatus(c, "/board",
                                                   dict(owner_id=response["user_id"],title="NEUES BOARD"),
                                                   200,
                                                   expected=[["owner_id", response["user_id"]],["title", "NEUES BOARD"]])

            self.expectGetStatus(c, "/board/{}".format(response_board["board_id"]), 200)

            self.expectPutStatus(c, "/board/{}".format(response_board["board_id"]),
                                 dict(owner_id=response["user_id"], title="2. NEUER TITEL"),
                                 200,
                                 expected=[["owner_id", response["user_id"]], ["title", "2. NEUER TITEL"]])

            response_boards = self.expectGetStatus(c, "/user/{}/boards".format(response_board["board_id"]), 200)
            self.assertEqual(len(response_boards), 1)

            self.expectDeleteStatus(c, "/board/{}".format(response_board["board_id"]), 200,
                                    expected=[["owner_id", response["user_id"]], ["title", "2. NEUER TITEL"]])

            self.expectGetStatus(c, "/board/{}".format(response_board["board_id"]), 404)

    def test_column(self):
        with self.client as c:
            print("TEST THE COLUMN")
            response = self.expectPostStatus(c, "/user", dict(username="ferdi", password="123456789"), 200,
                                             expected=[["username", "ferdi"], ["password", "123456789"]])
            response_board = self.expectPostStatus(c, "/board", dict(owner_id=response["user_id"], title="NEUES BOARD"),
                                                   200, expected=[["owner_id", response["user_id"]], ["title", "NEUES BOARD"]])

            response_column = self.expectPostStatus(c, "/column", dict(board_id=response_board["board_id"], title="NEUE REIHE", position=1),
                                                    200, expected=[["board_id", response_board["board_id"]],
                                                                   ["title", "NEUE REIHE"],
                                                                   ["position", 1]])

            self.expectGetStatus(c, "/column/{}".format(response_column["column_id"]), 200)

            self.expectPutStatus(c, "/column/{}".format(response_column["column_id"]),
                                 dict(board_id=response_board["board_id"], title="2. NEUE REIHE", position=1), 200,
                                 expected=[["board_id", response_board["board_id"]], ["title", "2. NEUE REIHE"], ["position", 1]])

            response_boards = self.expectGetStatus(c, "/board/{}/columns".format(response_column["board_id"]), 200)
            self.assertEqual(len(response_boards), 1)

            self.expectDeleteStatus(c, "/column/{}".format(response_column["column_id"]), 200,
                                    expected=[["board_id", response_board["board_id"]], ["title", "2. NEUE REIHE"], ["position", 1]])

            self.expectGetStatus(c, "/column/{}".format(response_column["column_id"]), 404)

    def test_task(self):
        with self.client as c:
            print("TEST THE TASK")
            response = self.expectPostStatus(c, "/user", dict(username="ferdi", password="123456789"), 200,
                                             expected=[["username", "ferdi"], ["password", "123456789"]])
            response_board = self.expectPostStatus(c, "/board", dict(owner_id=response["user_id"], title="NEUES BOARD"),
                                                   200, expected=[["owner_id", response["user_id"]], ["title", "NEUES BOARD"]])

            response_column = self.expectPostStatus(c, "/column", dict(board_id=response_board["board_id"], title="NEUE REIHE", position=1),
                                                    200, expected=[["board_id", response_board["board_id"]],
                                                                   ["title", "NEUE REIHE"],
                                                                   ["position", 1]])

            response_task = self.expectPostStatus(c, "/task",
                                                    dict(column_id=response_column["column_id"],
                                                         worker=response["user_id"],
                                                         title="NEUE TASK",
                                                         prio=2,
                                                         position=1),
                                                    200,
                                                    expected=[
                                                        ["column_id", response_column["column_id"]],
                                                        ["worker", response["user_id"]],
                                                        ["title", "NEUE TASK"],
                                                        ["prio", 2],
                                                        ["position", 1]

                                                    ])

            self.expectGetStatus(c, "/task/{}".format(response_task["task_id"]), 200)

            self.expectPutStatus(c, "/task/{}".format(response_task["task_id"]),
                                 dict(column_id=response_column["column_id"],
                                      worker=response["user_id"],
                                      title="2. NEUE TASK",
                                      prio=2,
                                      position=1),
                                 200,
                                 expected=[
                                     ["column_id", response_column["column_id"]],
                                     ["worker", response["user_id"]],
                                     ["title", "2. NEUE TASK"],
                                     ["prio", 2],
                                     ["position", 1]

                                 ])

            response_boards = self.expectGetStatus(c, "/column/{}/tasks".format(response_column["column_id"]), 200)
            self.assertEqual(len(response_boards), 1)

            self.expectDeleteStatus(c, "/task/{}".format(response_task["task_id"]), 200,
                                    expected=[
                                        ["column_id", response_column["column_id"]],
                                        ["worker", response["user_id"]],
                                        ["title", "2. NEUE TASK"],
                                        ["prio", 2],
                                        ["position", 1]

                                    ])

            self.expectGetStatus(c, "/task/{}".format(response_task["task_id"]), 404)


