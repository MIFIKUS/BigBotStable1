import mysql.connector


class CreateTables:
    def __init__(self):
        self.connection = mysql.connector.connect(host='192.168.3.15', user='root', password='BigBot')
        self.cursor = self.connection.cursor()

    def create_database(self):
        query = 'CREATE DATABASE Alchemy'
        try:
            self.cursor.execute(query)
        except:
            print("База данных уже создана")
        self.close_connection()
        self.connection = mysql.connector.connect(host='192.168.3.15', user='root', password='BigBot')
        self.cursor = self.connection.cursor()
    def create_gained_items_table(self):
        query = '''
            USE Alchemy;
            CREATE TABLE gained_items( 
                item_name VARCHAR(255),
                server_name VARCHAR(2)
                )'''
        self.cursor.execute(query)
        self.close_connection()
        self.connection = mysql.connector.connect(host='192.168.3.15', user='root', password='BigBot')
        self.cursor = self.connection.cursor()
    def create_less_100_items_table(self):
        query = '''
            USE Alchemy;
            CREATE TABLE less_100_items( 
                item_name VARCHAR(255),
                server_name VARCHAR(2),
                date TIMESTAMP
                )'''
        self.cursor.execute(query)
        self.close_connection()
        self.connection = mysql.connector.connect(host='192.168.3.15', user='root', password='BigBot')
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    def create(self):
        self.create_database()
        self.create_gained_items_table()
        self.create_less_100_items_table()
        self.close_connection()

create_tables = CreateTables()
create_tables.create()

