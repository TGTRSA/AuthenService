from tkinter import *
import tkinter.filedialog
import tkinter.messagebox 
import customtkinter as ctk
from customtkinter import CTkButton, CTkLabel, CTkEntry
import tkinter
#import clientserver
import sys
import time
import logging
import colors
import os
import json
import dbHandler
import audioParser


imagePath =  r'C:\Users\Tashriq\vs_stuff\python\loginPrac\images\Stark_Sigil.png'

# Maybe i should make it statefule and create a state update that renders 
# different frames according to the state

class State:
    def __init__(self):
        #json file data(?)
        
        pass

    def getState():
        # gets the state from the json file(?)
        # if file exists
        # check state
        # else it doesnt exist
        # then do other thing
        pass

    def updateState():
        # if the currentState isnt logged in then register
        # algorithm for state update
        # updated state 
        pass

logCredsPath = r'C:\Users\Tashriq\vs_stuff\python\loginPrac\userData\loginToken.json'
empty = " "

def makeRed(e):
    print(f"\033[91mError: {e}\033[0m")

def logError(error):
    makeRed(error)
    logging.error(str(error))  # Use logging.error for general errors

# Setup logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("Gui2.log")]
)

class BaseFrame:
    def __init__(self, title):
        self.root = ctk.CTk()
        self.root.title(title)
        self.frame = ctk.CTkFrame(master=self.root)
        self.frame.pack(fill='both', expand=True)

    def run(self):
        self.root.mainloop()

    def destroy(self):
        print("Closing...")
        self.root.destroy()

class LoginFrame(BaseFrame):
    def __init__(self):
        super().__init__('Login Window')
        self.root.geometry("1480x720")
        self.setupUI()
        
    def setupUI(self):
        
        self.userNameVar = ctk.StringVar()
        self.passwordVar = ctk.StringVar()
        
        self.loginButtons()
        self.loginLabels()
        self.loginEntries()

        self.userNameVar.trace_add("write", self.checkEntries)
        self.passwordVar.trace_add("write", self.checkEntries)

    def loginLabels(self):
        self.loginLabel = CTkLabel(self.frame, text="Don't have an account? Register instead", font=("Arial", 14))
        self.loginLabel.pack(expand=True)
        self.loginLabel.place(relx=0.49,rely=0.8, anchor="center")
        self.loginLabel.bind("<1>", self.show_register_window)
        
        self.invalidLabel = CTkLabel(self.frame, text="", font=("Arial", 20))
        self.invalidLabel.pack(pady=80)

    def loginEntries(self):
        self.userNameField = CTkEntry(self.frame, textvariable=self.userNameVar, placeholder_text="Username",width=200)
        self.userNameField.pack(expand=True)
        self.userNameField.place(relx=0.5, rely=0.4, anchor="center")

        self.passwordField = CTkEntry(self.frame, textvariable=self.passwordVar, placeholder_text="Password", show="*", width=200)
        self.passwordField.pack(expand=True)
        self.passwordField.place(relx=0.5, rely=0.5, anchor="center")

    def loginButtons(self):
        # Fix the typo and make it fit within the login window
        self.login_button = CTkButton(self.frame, text="Login", command=self.login, state=DISABLED)
        self.login_button.pack(pady=200, expand=True)
        self.login_button.place(relx=0.5, rely=0.7, anchor="center")

    def checkEntries(self, *args):
        userName = self.userNameVar.get()
        password = self.passwordVar.get()
        self.login_button.configure(state="NORMAL" if userName and password else "disabled")

    #def login(self):
     #   username = self.userNameField.get()
      #  password = self.passwordField.get()
       # if self.creditValidator(username, password):
        #    user = (f"login\a{username}\t{password}")
         #   self.clientConnection.sendall(user.encode('ascii'))
    
    def login(self):
        username = self.userNameField.get()
        password = self.passwordField.get()
        if self.creditValidator(username, password):
            user = {
                "username" : f"{username}",
                "password" : f"{password}",
                "loggedIn" : False,
            }
            datatosend = json.dumps(user, indent=4)
            print(datatosend)
            # attempt to login and receieve response from server
            if dbHandler.databaseHandler().login(datatosend) == True:
                if not os.path.exists(logCredsPath):
                    with open(logCredsPath, 'w') as file:
                        file.write(datatosend)
                with open(logCredsPath, 'w') as file:
                    file.write(datatosend)
                # Open the json file and load the information onto data
                with open(logCredsPath, 'r') as file:
                    data = json.load(file)
                # Update the login state
                data['loggedIn'] = True
                print(data)
                colors.makeGreen("Succeesfully edited userInfo")
                with open(logCredsPath, 'w') as f:
                    json.dump(data, f)
                self.destroy()
                MainWindow().run()
                time.sleep(5)
                os.remove(logCredsPath)
                #data['loggedIn'] = False
                #print(data)


    def creditValidator(self, username, password):
        if not username:
            self.invalidLabel.configure(text="Cannot submit empty username", text_color="red")
            return False
        elif not password:
            self.invalidLabel.configure(text="Cannot submit empty password", text_color="red")
            return False
        else:
            self.invalidLabel.configure(text="", text_color="green")
            return True

    def show_register_window(self, event=None):
        self.destroy()
        RegisterFrame().run()

class RegisterFrame(BaseFrame):
    def __init__(self):
        super().__init__('Register window')
        self.root.geometry("1480x720")
        ctk.set_appearance_mode("dark")
        self.setup_ui()

    def setup_ui(self):
        self.userNameVar = ctk.StringVar()
        self.passwordVar = ctk.StringVar()
        
        # Register UI components
        self.UserEntries()
        self.RegisterLabels()
        self.UserInfoButtons()
        
        self.userNameVar.trace_add("write", self.checkEntries)
        self.passwordVar.trace_add("write", self.checkEntries)

    def UserEntries(self):
        self.userNameField = CTkEntry(self.frame, textvariable=self.userNameVar, placeholder_text="Username", width=200)
        self.userNameField.pack(expand=True)
        self.userNameField.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        self.passwordField = CTkEntry(self.frame, textvariable=self.passwordVar, placeholder_text="Password", show="*", width=200)
        self.passwordField.pack(expand=True)
        self.passwordField.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def RegisterLabels(self):
        self.loginLabel = CTkLabel(self.frame, text="Login", font=("Arial", 10))
        self.loginLabel.pack(expand=True)
        self.loginLabel.place(relx=0.58, rely=0.7, anchor="center")
        self.loginLabel.bind("<1>", self.loginFrame)
        
        self.invalidLabel = CTkLabel(self.frame, text="", font=("Arial", 20))
        self.invalidLabel.pack(pady=80)

    def loginFrame(self, event=None):
        self.destroy()
        LoginFrame().run()

    def UserInfoButtons(self):
        self.registerButton = CTkButton(self.frame, text="Register", command=self.register, state=DISABLED)
        self.registerButton.pack(pady=200, expand=True)
        self.registerButton.place(relx=0.5, rely=0.7, anchor="center")
        
    def checkEntries(self, *args):
        userName = self.userNameVar.get()
        password = self.passwordVar.get()
        self.registerButton.configure(state="NORMAL" if userName and password else "disabled")

    def register(self):
        username = self.userNameVar.get()
        password = self.passwordVar.get()
        user = {
            "method": "register",
            "username" : f"{username}",
            "password" : f"{password}",
            "loggedIn" : False
        }
        parsedJsonUser = json.dumps(user)
        # # Use logging in production
        # if client.sendall(user) == True:
        if dbHandler.databaseHandler().dbRegister(parsedJsonUser) == True:
            with open(logCredsPath, 'w') as file:
                file.write(parsedJsonUser)

            colors.makeGreen("User information successfully created and registered")
            #time.sleep(5)
            #os.remove(logCredsPath)
            #colors.makeGreen('Removed token successfully')

    def creditValidator(self, username, password):
        if not username:
            self.invalidLabel.configure(text="Cannot submit empty username", text_color="red")
            return False
        elif not password:
            self.invalidLabel.configure(text="Cannot submit empty password", text_color="red")
            return False
        else:
            self.invalidLabel.configure(text="", text_color="green")
            return True
        

class MainWindow(BaseFrame):
    def __init__(self):
        with open(logCredsPath, 'r') as file:
            jsonData = json.load(file)
        self.username = jsonData['username']
        string = f"Welcome to {self.username}'s spot"
        super().__init__(string)
        self.root.geometry('1920x1080')
        self.dirFrame = ctk.CTkFrame(self.root)
        self.dirFrame.pack(fill="both",expand=True, padx=10, pady=10)
        try:
            self.setupUI()
        except Exception as e:
            print(e)
        
    def setupUI(self):
        self.directory = r'C:\Users\Tashriq\vs_stuff\python\loginPrac\audio'
        self.scrollable_frame = ctk.CTkScrollableFrame(self.dirFrame, width=500, height=300)
        self.scrollable_frame.pack(padx=20,pady=20, fill='both',expand=True)

        #self.buttons()
        #self.Textfield()
        #self.imageStuff()
        #widget = ctk.CTKW
        self.displayItems()
    
    def displayItems(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        try: 
            for file in sorted(os.listdir(self.directory)):
                if file.__contains__('.mp3'):
                    fullPath = os.path.join(self.directory, file)
                    self.audioLabels(file, fullPath)      
        except Exception as e:
            print(e)
            sys.exit(1)

    def audioLabels(self, item, fullPath):
        self.directoryLabel = ctk.CTkLabel(self.scrollable_frame, text=item, cursor='hand2' if fullPath else 'arrow')
        self.directoryLabel.pack(anchor='w', padx=10, pady=2)
        self.directoryLabel.bind("<Button-1>",lambda event,path=fullPath:self.openFile(path))

    @staticmethod
    def openFile(filePath):
        if os.path.isdir(filePath):
            print("Dir")
        elif os.path.isfile(filePath):
            audioParser.songChoice(filePath)
            #os.startfile(filePath)
        

    def imageStuff(self):
        #self.Image = PIL.Image.open(imagePath)
        self.Image = tkinter.PhotoImage(file=imagePath)
        self.ImageLabel =CTkLabel(self.frame, image=self.Image)
        self.ImageLabel.pack()
        pass

    def buttons(self):
        self.mainbutt = CTkButton(self.frame, text="Push", command=self.do)
        self.mainbutt.pack(pady=200, expand=True)
        self.mainbutt.place(relx=0.5, rely=0.7, anchor="center")
    
    def Textfield(self):
        self.entryWidget = ctk.CTkEntry(self.root, width =300, placeholder_text='Type message...')
        self.entryWidget.pack(pady=10)
        self.textWidget = ctk.CTkTextbox(self.root, width = 350, height=450)
        self.textWidget.pack(pady=20)
        pass

    def do(self):
        message = self.entryWidget.get()
        self.textWidget.insert(ctk.END, message + '\n')
        self.entryWidget.delete(0, ctk.END)

class App(BaseFrame):
    def __init__(self, loggedIn=False):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        if self.loggedIn():
            MainWindow().run()
        else:
            RegisterFrame().run()

    def loggedIn(self):
        if os.path.exists(logCredsPath):
            with open(logCredsPath, 'r') as file:
                userData = json.load(file)

                return userData['loggedIn']
        else:
            return False
            

    def on_closing(self):
        if hasattr(self, 'clientConnection'):
            try:
                self.clientConnection.close()
                print("Closing server")
            except Exception as e:
                print(e)
            finally:
                self.closeApp()
        else:
            self.closeApp()

    def closeApp(self):
        print("Closing app...")
        self.root.destroy()
        sys.exit(1)

if __name__ == "__main__":
    try:
        App()
    except KeyboardInterrupt:
        pass
