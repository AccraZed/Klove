import sqlite3
from sqlite3 import Error


#Creates connection
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# Write Functions

# This function is for executing permanent changes to the DB, NOT retrieving data
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit() # THIS LINE CHANGES THE CONTENTS OF THE DB! USE WITH CAUTION
    except Error as e:
        print(f"The error '{e}' occurred")


# This function is for executing permanent changes to the DB, NOT retrieving data
def execute_query(connection, query, params):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit() # THIS LINE CHANGES THE CONTENTS OF THE DB! USE WITH CAUTION
    except Error as e:
        print(f"The error '{e}' occurred")


# Read Functions:

# This function is used for retrieving data from the DB with simple query
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = [dict((cursor.description[i][0], value) \
            for i, value in enumerate(row)) for row in cursor.fetchall()]
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


# This function is used for retrieving data from the DB with parametrized query set
def execute_read_query(connection, query, params):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, params)
        result = [dict((cursor.description[i][0], value) \
            for i, value in enumerate(row)) for row in cursor.fetchall()]
        return result
    except Error as e:
        print(f"The error '{e}' occurred")