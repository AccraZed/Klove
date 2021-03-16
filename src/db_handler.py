import sqlite3
from sqlite3 import Error

class DatabaseHandler:
    def __init__(self, path_database):
        try:
            self.connection = sqlite3.connect(path_database)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    # Writes to DB, given the appropriate query

    def write(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            # THIS CHANGES THE CONTENTS OF THE DB! USE WITH CAUTION
            connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred")

    def write(self, query, params):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            # THIS CHANGES THE CONTENTS OF THE DB! USE WITH CAUTION
            connection.commit() 
        except Error as e:
            print(f"The error '{e}' occurred")

    # Reads from the DB, returning a dict of the query results

    def read(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def read(self, query, params):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query, params)
            result = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
            return result
        except Error as e:
            print(f"The error '{e}' occurred")