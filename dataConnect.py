import sqlite3
from sqlite3 import Error

import functions


class SqliteDB:
    _connection = None

    def __init__(self, db_name):
        self.create_connection(db_name)

    def create_connection(self, db_name):
        try:
            self._connection = sqlite3.connect(db_name)
            return True
        except Error as e:
            functions.log(e)
            return False

    def get_connection(self):
        return self._connection

    def close_connection(self):
        if self._connection:
            self._connection.close()

    def exec_sql(self, sql, params=""):
        try:
            return self._connection.execute(sql, params)
        except Error as e:
            functions.log(e)
            return ""

    def start_transaction(self):
        self._connection.execute("""BEGIN TRANSACTION;""")

    def commit(self):
        self._connection.execute("""COMMIT;""")
