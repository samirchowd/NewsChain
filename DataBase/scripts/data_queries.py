import psycopg2
from psycopg2 import DatabaseError as Error
import pandas as pd
import articledb_connection

host = 'localhost'
user = 'postgres'
passwd = 'Mar.Kar0298'

try:
    connection = articledb_connection.create_server_connection(host, user, passwd)
except Error as err:
    print(f"Error: '{err}'")


def query(conn, type_of_query):
    result = []
    if type_of_query == 'title':
        try:
            curs = conn.cursor()
            curs.execute("SET SEARCH_PATH TO articledb")
            curs.execute("SELECT title FROM Article")
            while True:
                row = curs.fetchone()
                if row is None:
                    break
                result.append(row[0])
        except Error as err:
            print(f"Error: '{err}'")
    elif type_of_query == 'abstract':
        try:
            curs = conn.cursor()
            curs.execute("SET SEARCH_PATH TO articledb")
            curs.execute("SELECT abstract FROM Article")
            while True:
                row = curs.fetchone()
                if row is None:
                    break
                result.append(row[0])
        except Error as err:
            print(f"Error: '{err}'")
    elif type_of_query == 'timestamp':
        try:
            curs = conn.cursor()
            curs.execute("SET SEARCH_PATH TO articledb")
            curs.execute("SELECT time_stamp FROM Article")
            while True:
                row = curs.fetchone()
                if row is None:
                    break
                result.append(row[0])
        except Error as err:
            print(f"Error: '{err}'")
    return result


titles = query(connection, 'title')
