import sqlite3
import os

# TODO: Fix horrible injection vulns...


class IncorrectArgs(Exception):
    pass


class DBManager:
    def __init__(self):
        self.db_name = "form_data.db"
        self.conn = None
        if not os.path.exists(self.db_name):
            # this has to go outside of create_db because decorator already creates db
            self.create_db()

    def create_connection(self):
        self.conn = sqlite3.connect(self.db_name)

    def connect(func):

        def inner_func(self, *args, **kwargs):
            try:
                self.conn.execute('SELECT name FROM sqlite_temp_master WHERE type="table";')
            except (AttributeError, sqlite3.ProgrammingError):
                self.create_connection()
            ret_val = func(self, *args, **kwargs)
            self.conn.commit()
            return ret_val

        return inner_func

    @connect
    def create_db(self):
        """Creates the database if it does not already exist"""

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
                     MacAddress text);""")
        c.execute("""CREATE TABLE TodaysMacAddresses
                     (AddressID INTEGER PRIMARY KEY AUTOINCREMENT,
                     MacAddress text);""")
        c.close()


    @connect
    def insert_record(self, table_name, *args):
        if len(*args) > 4 or len(*args) < 4:
            raise IncorrectArgs

        c = self.conn.cursor()
        c.execute(f"""INSERT INTO 
                  {table_name}(FirstName, LastName, MNumber, MacAddress)
                  VALUES(?,?,?,?);""", *args)
        c.close()


    @connect
    def update_record(self, table_name, *args):
        """Update records based on M Numbers, as that should never change"""
        sql = f"""UPDATE {table_name}
                   SET 
                   FirstName = ?,
                   LastName = ?,
                   MNumber = ?,
                   MacAddress = ?
                   WHERE MNumber = ?;"""
        c = self.conn.cursor()
        c.execute(sql, *args, args[2])
        c.close()

    @connect
    def get_form_data_to_send(self):
        """Get records for auto-form fill"""
        sql = """SELECT FirstName, LastName, MNumber, MacAddress
                     FROM FormData 
                     WHERE MacAddress IN (SELECT MacAddress FROM TodaysMacAddresses);"""
        c = self.conn.cursor()
        c.execute(sql)
        results = c.fetchall()
        c.close()

        return results

    @connect
    def clear_table(self, table_name):
        """Some tables like TodaysMacAddresses will need to be cleared out on a regular basis"""
        sql = f"""DELETE FROM {table_name};"""
        c = self.conn.cursor()
        c.execute(sql)
        c.close()

    @connect
    def insert_mac_addresses(self, mac_addresses: list):
        sql = """INSERT INTO TodaysMacAddresses(MacAddress) VALUES(?);"""
        c = self.conn.cursor()
        for mac_address in mac_addresses:
            c.execute(sql, mac_address)
        c.close()

    # joins should use mac address because that can be updated later
    # Get entries where Mac Addresses Match, for updating records.
    """SELECT fd.FirstName,fd.LastName,fd.MNumber,fd.MacAddress 
       FROM FormData AS fd 
       LEFT JOIN TempData AS td 
       ON fd.MacAddress = td.MacAddress;"""



