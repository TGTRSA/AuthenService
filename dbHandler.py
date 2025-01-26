from database_module import DatabaseMaker 
import logging
from typing import List
import sys
import colors
import sqlite3 as sq
import json
import os
from datetime import datetime
import hashlib
import time

user = []
pathToHanlderError = r'C:\Users\Tashriq\vs_stuff\python\loginPrac\userData\dbHandler.log'
userDbPath = r'C:\Users\Tashriq\vs_stuff\python\loginPrac\userData\users'
orderedDbPath = r'C:\Users\Tashriq\vs_stuff\python\loginPrac\userData\orderedDb'

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
            logging.FileHandler(pathToHanlderError) #Log to a file
            #logging.StreamHandler(),    # Log to console
    ]
)

def logError(e):
    print(f"\033[91mError: {e}\033[0m")
    logging.exception("\nError\n")
    print("Closing script...")
    sys.exit(1)


class databaseHandler:
    def __init__(self, databasename=userDbPath):
        self.databasename = f"{databasename}.db"
        orderedDbName = f"{orderedDbPath}.db"
        try:
            self.dbConn = sq.connect(self.databasename)
            self.orderConn = sq.connect(orderedDbName)
            print("Connection to database being created")
            self.cursor = self.dbConn.cursor()
            self.orderedDbcursor = self.orderConn.cursor()
        except Exception as err:
            logError(err)
        except KeyboardInterrupt:
            print('Canceling connection')         

    # similar to login will always be triggered by register request
    def dbRegister(self, args:List[str]):
        #tableName = 'users'
        print("Registering...")
        try:
            tableName = '"user"("UID","userName","password")'
            
            jsonData = json.loads(args)
            userInfo = self.JsonParser(jsonData)
            UID = self.hashUserName(jsonData["username"])
            #print(jsonData['username'])
            #print(UID)
            #print(tableInsert)
            sql_command = f"INSERT INTO {tableName} VALUES (\"{UID}\",{userInfo});"
            #print(f"SQL COMMAND: {sql_command}")

            # Should execute on the unordered db
            self.cursor.execute(sql_command)
            time.sleep(10)
            self.OrderDB()
            self.dbConn.commit()

            colors.makeGreen("Database test successful")
            return True
        except sq.Error as e:
            print(f"\033[91m An Error occured:{e}\033[0m")
        except Exception as e:
            logError(e)
            sys.exit(1)

    def hashUserName(self, username) -> int:
        hashobj = hashlib.sha256()
        hashobj.update(username.encode('utf-8'))
        hexV = int(hashobj.hexdigest()[:11], 16)
        return hexV

    def JsonParser(self, args:List[str]):
        print(args)
        userInfo = f'"{args["username"]}", "{args["password"]}"'
        print(f"{userInfo}")
        return userInfo

    # initlialised by the server so will always be triggered by login request
    def login(self, *args:List[list]):
        print("Checking user data...")
        try:
            print(args)
            jsonData = json.loads(args[0])
            #print(jsonData['username'])
            userInfo = f'"{jsonData["username"]}", "{jsonData["password"]}"'
            print(userInfo)
            
            self.cursor.execute(f'SELECT * FROM user WHERE userName = (\'{jsonData["username"]}\') AND password = (\'{jsonData["password"]}\');')
            results = self.cursor.fetchall()

            # where json data(login_token) is created on the server-side
            #if results:
            #    print("Creating login information")
             #   for row in results:
              #      userInfo = { 
               #         "userName": row[0],
                #        "password" : row[1], 
                 #       "dateOfLogin": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                  #  }
                   # user.append(userInfo)
                #with open('loginToken.json', 'w') as f: 
                 #   jsonData = json.dumps(userInfo)
                  #  json.dump(user, f, indent=4)
                #print(jsonData ,'\tlogin')
                #clientserver.sendall(jsonData.encode('ascii')) 
            #else:
             #   colors.makeRed("User does not exist")
            
            if results:
                colors.makeGreen("Database test successful")
                return True
            else:
                colors.makeRed('User does not exist')
            
        except sq.Error as e:
            print(f"\033[91m An Error occured:{e}\033[0m")
        except Exception as e:
            logError(e)
            sys.exit(1)

    def removeUser(self, args:List[str]):
        userInfo = self.JsonParser(args)
        self.cursor.execute(f"DELETE FROM user WHERE userName =(?) AND password=(?);", userInfo)  
        pass

    def addPicture(self):
        pass

    def removePicture(self):
        pass

