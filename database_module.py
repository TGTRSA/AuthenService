import sqlite3 as sq
from typing import List
import logging
import sys
import colors

# Logging for file error config
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
            logging.FileHandler("dbErros.log") #Log to a file
            #logging.StreamHandler(),    # Log to console
    ]
)

def logError(e):
    print(f"\033[91mError: {e}\033[0m")
    logging.exception("\nError\n")
    sys.exit(1)

class DatabaseMaker:
    def __init__(self, databasename:str):
        #self.databasename = str(f"{databasename}.db"
        self.databasename = databasename + ".db"
        print(f'Connection to {str(self.databasename)} established')  
        try:
            self.dbConn = sq.connect(self.databasename)
            print("Connection to database being created")
            self.cursor = self.dbConn.cursor()
        except Exception as err:
            logError(err)
        except KeyboardInterrupt:
            print('Canceling connection')         

    def end_connection(self):
        # Close our connection
        self.dbConn.commit()
        self.dbConn.close()

    def createTable(self,tableName, *args: List[str]):
        tableValues = ",".join(map(str, args))  # Join column definitions with commas
        sql_command = f"CREATE TABLE IF NOT EXISTS {tableName}{tableValues};"
        try:
           # print(f"Attempting to insert {args}")
           # print(f"INSERT INTO {tableName} VALUES {args}")
            self.cursor.execute(sql_command)
            print(f"Inserted ({args}) inserted into\ntable ({tableName}) ")
            self.end_connection()
        except Exception as err:
            logError(err)
        
    def insert_into_table(self, tableName: str, *args: List[str]):
        #cursor = self.db_connection.cursor()
        #splitString = args.split('\a')
        tableContent = ",".join(map(str, args))
        #tableContent = ','.join(args)
        sql_command = f"INSERT INTO {tableName} {tableContent};"
        print(sql_command)
        try:
            #print(f"Attempting to insert {tableContent}")
            #print(f"INSERT INTO {tableName} VALUES {tableContent}")
            self.cursor.execute(sql_command)
            colors.makeGreen(f"Inserted ({args}) inserted into\ntable ({tableName}) ")
            self.conn.commit()
        except Exception as e:
            logError(e)

    def view_contents(self):
        self.cursor = self.conn_db()
        value = int(input("1. View one value from table\n2. Particular row with particular value\n"))
        tableName1 = str(input("Table name:"))
        if value == 1:
            # Code to view one value from one table
            try:
                self.cursor.execute(f"SELECT * FROM {tableName1}")
                rows = self.c.fetchall()
                for row in rows:
                    print(row)
            except sq.Error as e:
                print(f"An error occured: {e}")
        if value == 2:
            # Code to view all values from one table
            try:
                row = input("Row:")
                search_value = input("Search: ")
                self.c.execute(f"SELECT * FROM {tableName1} WHERE {row}=:n", {"n": f"{search_value}"})
                rows = self.c.fetchall()
                for row in rows:
                    print(row)
            except Exception as err:
                logError(err)
                
if __name__ == "__main__":
    userDbPath = r'C:\Users\Tashriq\vs_stuff\python\loginPrac\userData\test'
    db = DatabaseMaker(userDbPath)



