<<<<<<< HEAD
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
=======
import sqlite3
from sqlite3 import Error

#
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# This function is for executing permanent changes to the DB, NOT retrieving data
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit() # THIS LINE CHANGES THE CONTENTS OF THE DB! USE WITH CAUTION
    except Error as e:
        print(f"The error '{e}' occurred")


# This function is used for retrieving data from the DB
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")



# creating the connection 
connection = create_connection("db.sqlite")
num_beds = 2
num_br = 2
list_price = 130000

q = """
SELECT * from property
WHERE (num_bedrooms = ?
AND num_bathrooms = ?
AND ABS(list_price - close_price) < (list_price * 0.2))
"""
data_points = execute_read_query(connection, q)
for data_pt in data_points:
    print(data_pt)

connection.close()
>>>>>>> a1867a4... Added videos
