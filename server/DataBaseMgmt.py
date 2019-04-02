import sqlite3
import os


class IncorrectArgs(Exception):
    pass


class DBManager:
    def __init__(self):
        self.db_name = "form_data.db"
        self.conn = None
        self.create_db()

    def create_connection(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def connect(self, func):
        try:
            self.conn.execute('SELECT name FROM sqlite_temp_master WHERE type="table";')
        except (AttributeError, sqlite3.ProgrammingError):
            self.conn = sqlite3.connect(self.db_name)

        def inner_func(*args, **kwargs):
            return func(*args, **kwargs)
        ret_val = inner_func
        self.conn.commit()
        return ret_val

    @connect
    def create_db(self):
        """Creates the database if it does not already exist"""
        if os.path.exists(self.db_name):
            return

        c = self.conn.cursor()
        c.execute("""CREATE TABLE FormData
                     (recordID INTEGER PRIMARY KEY AUTOINCREMENT,
                     FirstName text, 
                     LastName text,
                     MNumber text,
                     MacAddress text)""")
        c.execute("""CREATE TABLE TempData
                     (recordID INTEGER PRIMARY KEY AUTOINCREMENT,
                     FirstName text, 
                     LastName text,
                     MNumber text,
                     MacAddress text)""")

    @connect
    def insert_record(self, table_name, *args):
        if len(args) > 4 or len(args) < 4:
            raise IncorrectArgs

        c = self.conn.cursor()
        c.execute(f"""INSERT INTO 
                  {table_name}(FirstName, LastName, MNumber, MacAddress)
                  VALUES(?,?,?,?)""", *args)


