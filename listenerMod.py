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
        try:
            if key == sequence:
                self.checkerThread = threading.Thread(target=self.check)
                self.checkerThread.start()
                #self.check()
                #self.server.closeServer()
                return False  # Stop listener
        except AttributeError:
            if key == keyboard.Key.space:
                self.log += " "  

                print(f"log with space: {self.log}")  