import sqlite3


class DataBase:
    base_path = "."

    @staticmethod
    def make_no_response_query(sql, database_url):
        connection = sqlite3.connect(database_url)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()

    @staticmethod
    def make_multi_response_query(query, database_url):

        connection = sqlite3.connect(database_url)
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            msg = cursor.fetchall()
            connection.close()
            response = []
            for answer in msg:
                response.append(list(answer))
            return response
        except sqlite3.OperationalError:
            print("Invalid query: " + query)
            return None
