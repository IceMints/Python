"""
CISP 71 Fall 2020
Create any SQLite database and table using python.
The table must have four or six columns. No foreign keys.
"""
from tkinter import *
# importing sqlite
import sqlite3


# creating a database class
class Database:
    def __init__(self, db):
       
        # create a database connection
        self.conn = sqlite3.connect(db)
        # create a cursor to send instructions to the database
        self.cur = self.conn.cursor()

        # Create table
        # Use of triple quotes to write on more than one line
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Fruit_Inventory
                        (fruitID INTEGER PRIMARY KEY,
                        fruit text,
                        description text,
                        price text,
                        supplier text)''')
        # commit to database
        self.conn.commit()

    # display all in database
    def fetch(self):
        self.cur.execute("SELECT * FROM Fruit_Inventory")
        rows = self.cur.fetchall()
        return rows
    
    # Insert a row of data
    def insert(self, fruit, description, price, supplier):
        self.cur.execute("INSERT INTO Fruit_Inventory VALUES (NULL, ?, ?, ?, ?)",
                        (fruit, description, price, supplier))
        self.conn.commit()

    # remove a row in database
    def delete(self, fruitID):
        self.cur.execute("DELETE FROM Fruit_Inventory WHERE fruitID=?", (fruitID,))
        self.conn.commit()

    # update a row in database
    def update(self, fruitID, fruit, description, price, supplier):
        self.cur.execute(
                        '''UPDATE Fruit_Inventory SET
                        fruit = ?,
                        description = ?,
                        price = ?,
                        supplier = ?
                        WHERE fruitID = ?''',
                        (fruit, description, price, supplier, fruitID))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
