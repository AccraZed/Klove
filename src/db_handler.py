import sqlite3
from sqlite3 import Error

# Python doesn't support function overloading(later function takes precedence)

class DatabaseHandler:
    def __init__(self, path_database):
        try:
            self.connection = sqlite3.connect(path_database)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    # Writes to DB, given the appropriate query
    def write(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            if params is not None:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # THIS CHANGES THE CONTENTS OF THE DB! USE WITH CAUTION
            self.connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred")

    def read(self, query, params=None):
        cursor = self.connection.cursor()
        result = None
        try:
            if params is not None:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            result = [dict((cursor.description[i][0], value)
                           for i, value in enumerate(row)) for row in cursor.fetchall()]
            return result

        except Error as e:
            print(f"The error '{e}' occurred")

# for speeding up alterations to the table (Justice)
# db_path = "src/db.sqlite"
# db = DatabaseHandler(db_path)
