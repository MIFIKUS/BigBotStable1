from database.access_data import *
import mysql.connector


def get_cursor():
    connection = mysql.connector.connect(host=IP, user=USER, password=PASSWORD)
    connection.autocommit = True
    return connection.cursor()
