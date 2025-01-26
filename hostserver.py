import socket
import threading
from datetime import datetime
from pynput import keyboard
import sys
import logging
import json
import colors
import os
import dbHandler
import colors
from typing import List

sequence = ['c','l','o','s','e']

# laptop host = 127.0.0.1
data_payload = 1024
port = 1835
backlog = 5
#host = '192.168.1.67' # Public ip for laptop
host =  '192.168.8.115'


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
    logging.exception("\nError")

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
            #Listener(self.serverSocket).start_listener()
        except Exception as e:
            print(f"Error: {e}")
            logging.exception("\n")
            colors.makeRed("Closing program")
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
    # Closed
    def handleClient(self):
            try:
                # Get data from client
                data = self.clientSocket.recv(data_payload)
                if not self.clientSocket:
                    print(f"Client {self.clientAddress} disconnected")
                    self.clientSocket.shutdown(socket.SHUT_RDWR)
                    print(f"\033[32mClosed {self.clientAddress} successfully\033[0m")
                    sys.exit(1)
                # Parse the serialised data here
                serialisedData = data.decode('ascii')
                print(f"sent:{serialisedData} {self.clientAddress}")
                
                
                self.handleReq(serialisedData)
                #self.debug(data.decode('ascii'))
                
                #print(f"Received keystrokes: {data.decode('utf-8')}")
            except KeyboardInterrupt:
                self.closeServer()
            except Exception as e:
                self.closeServer()
                logError(e)
                return False
            finally:
                colors.makeGreen('YAHOOOOYYYY')
                self.serverSocket.close()
                sys.exit(1)
    

    def debug(self, data:List[str]):
        print(data)
        jsonData = json.loads(data.decode())
        print(jsonData)

    def disconnectClient(self):
        colors.makeRed("Disconnecting clients")
        self.clientSocket.shutdown(socket.SHUT_RDWR)
        sys.exit(1)

    def handleReq(self, args: List[str]):
        jsonData = json.loads(args)
        print(jsonData)
        print("Handling request")
        print(f"Method: {jsonData['method']}")
        try:
            if jsonData['method'] == 'register':
                #self.register(jsonData[1])
                # jsonData[1] is the user information itself
                #dbHandler.databaseHandler().dbRegister(jsonData[1])
                print('register')
            elif jsonData['method'] == 'login':
                print('login')
                #dbHandler.databaseHanlder().login(jsonData[1])
        except Exception as e:
            logError(e)
            sys.exit(1)
        except KeyboardInterrupt:
            self.closeServer()
            sys.exit(1)

    def closeServer(self):
        closeMsg = f"Attempting to close server... {self.timestamp}"
        try:
            colors.makeRed(closeMsg)
            self.clientSocket.shutdown(socket.SHUT_RDWR)
            self.serverSocket.close()
            sys.exit(1)
        except Exception as e:
            logError()
            sys.exit(1)
class Listener:  
    def __init__(self, server: HostServer):
        self.listener_thread = None
        self.listener_running = False
        self.server = server
        self.log = ""

    def start_listener(self):
        if not self.listener_running:
            self.listener_thread = threading.Thread(target=self.listen)
            self.listener_thread.start()
            self.listener_running = True

    def listen(self):
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()

    def check(self):
        check = input("Close server(y/n)?")
        match check.capitalize():
            case "Y":
                try:
                    self.server.closeServer()
                except Exception as e:
                    logError(e)
                #print(input)
            case "N":
                try:
                    self.server.closeServer()
                    HostServer.startServer()
                except Exception as e:
                    logError(e)
    
    def on_key_press(self, key):
        newkey = key.char if hasattr(key, 'char') else str(key)
        try:
            if key == keyboard.Key.esc:
                self.checkerThread = threading.Thread(target=self.check)
                self.checkerThread.start()
                #self.check()
                #self.server.closeServer()
                return False  # Stop listener
        except AttributeError:
            if key == keyboard.Key.space:
                self.log += " "  

                print(f"log with space: {self.log}")    

if __name__ == "__main__":
    # Start server
    server = HostServer(port)
    server.startServer()