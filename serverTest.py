import socket
import threading
from datetime import datetime
#import csv
from pynput import keyboard
import sys
import logging

import pickle
import os
#import database_module as dbMod
from typing import List
import dbHandler

def makeRed(string):
    print(f"\033[91m{string}\033[0m")

# laptop host = 127.0.0.1
data_payload = 1024
port = 1835
backlog = 5
#host = '192.168.1.67' # Public ip for wifi at parents place
host =  '192.168.8.115'
#host = socket.gethostbyname('localhost')
#print(host)

# Logging for file error config
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
            logging.FileHandler("serverErrors.log") #Log to a file
            #logging.StreamHandler(),    # Log to console
    ]
)

def logError(e):
    print(f"\033[91mError: {e}\033[0m")
    logging.exception("Error")

class HostServer:
    def __init__(self, port):
        self.port = port

    def startServer(self):
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            # Create socket
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set socket opt
            self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            # address to be used to bind and lisyen for connections on
            server_address = (host, self.port)
            print(f"Starting server on port: {server_address} at {self.timestamp}")
            # Binding and listening for connections
            self.serverSocket.bind(server_address)
            self.serverSocket.listen(backlog)
        except Exception as e:
            print(f"Error: {e}")
            logging.exception("\n")
            print("Error logged")
            print("Closing program")
            sys.exit(1)
        while True:
            # Accept connections on socket
            try:
                self.clientSocket, self.clientAddress = self.serverSocket.accept()
                print(f"Connected to {self.clientAddress} at {self.timestamp}")
                # Fork your client
                self.handleClient()
            except KeyboardInterrupt:
                self.serverSocket.close()
                sys.exit(1)
            
    # To handle the incoming data and connections
    def handleClient(self):
            try:
                # Get data from client
                data = self.clientSocket.recv(data_payload)
                if not data:
                    print(f"Client {self.clientAddress} disconnected")
                    #self.clientSocket.shutdown(socket.SHUT_RDWR)
                    #sys.exit(1)
                # serialised_data =  pickle.loads(data)
                serialised_data = data.decode('ascii')
                print(data.decode('asciii'))
                # Parse the serialised data here
                #print(f"Client sent: {serialised_data, self.clientAddress}")
                self.parse(serialised_data)
            except KeyboardInterrupt:
                self.closeServer()
            except Exception as e:
                self.closeServer()
                logError(e)
                return False

    def parse(self, *args: List[list]):
        print("Starting parser")
        try:
            lines = args[0].split('\a')
            self.handleReq(lines[0])
            #reg(lines[1])
        except Exception as e:
            logError(e)
            sys.exit(1)

    def handleReq(self, args: List[str]):
        print("Handling request")
        print(f"Method: {args[0]}")
        try:
            if args[0] == 'register':
                #self.register(args[1])
                # args[1] is the user information itself
                dbHandler.databaseHandler().dbRegister(args[1])
            elif args[0] == 'login':
                dbHandler.databaseHanlder().login(args[1])
        except Exception as e:
            logError(e)
            sys.exit(1)
        except KeyboardInterrupt:
            self.closeServer()
            sys.exit(1)
    
    def register(self, args:List[str]):
        print("Registering...")
        try:
            pass
        except Exception as e:
            logError(e)
            #self.closeServer()
            sys.exit(1)
        except KeyboardInterrupt:
            self.closeServer()

    def closeServer(self):
        closeMsg = f"Attempting to close server... {self.timestamp}"
        makeRed(closeMsg)
        self.serverSocket.close()
        try:
            #self.serverSocket.shutdown(socket.SHUT_WR)?
            sys.exit(1)
        #self.serverSocket = None
        except Exception as e:
            logError()
            sys.exit(1)    

if __name__ == "__main__":
    # Start server
    server = HostServer(port)
    server.startServer()
    