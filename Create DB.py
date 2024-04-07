import mysql.connector


class CreateTables:
    def __init__(self):
        self.connection = mysql.connector.connect(host='192.168.1.71', user='root', password='root')
        self.cursor = self.connection.cursor()

    def create_database(self):
        query = 'CREATE DATABASE Autosell'
        try:
            self.cursor.execute(query)
        except:
            print("База данных уже создана")
        self.close_connection()
        self.connection = mysql.connector.connect(host='192.168.1.71', user='root', password='root')
        self.cursor = self.connection.cursor()
    def create_gained_items_table(self):
        query = '''
            USE Autosell;
            CREATE TABLE items( 
                item_name VARCHAR(255),
                price INT
                )'''
        self.cursor.execute(query)
        self.close_connection()
        self.connection = mysql.connector.connect(host='192.168.1.71', user='root', password='root')
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    def create(self):
        self.create_database()
        self.create_gained_items_table()
        self.close_connection()

create_tables = CreateTables()
create_tables.create()

