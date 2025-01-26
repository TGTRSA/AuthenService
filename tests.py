import os
empty = ""
import threading
import sys
import pickle
from typing import List
import clientserver
import pprint
import dbHandler
import time
import math
import json
import re
import subprocess
import wave
import pyaudio
from pydub import AudioSegment

wfcon = AudioSegment.from_file(r"C:\Users\Tashriq\vs_stuff\python\loginPrac\audio\01 Ruin.mp3")

audio = pyaudio.PyAudio()

wf = wave

#stream = audio.open(format=audio.get_format_from_width(wfcon.gets))


def getMeta(mp3Path=r"C:\Users\Tashriq\vs_stuff\python\loginPrac\audio\01 Ruin.mp3"):
    outputPath = r"C:\Users\Tashriq\vs_stuff\python\loginPrac\audio\extraJson" + r"\json.json"
    #command = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', '-show_entries', mp3Path]
    command = ['ffprobe', '-show_format', '-show_streams', '-of', 'json', mp3Path]
    result = subprocess.check_output(
            command, text=True, shell=True
            )
    metadata = json.loads(result)
    expression = metadata['streams'][0]['duration'].strip()
    timestamp(expression)

def timestamp(metadata):
    use = re.sub(r'[^\d]', '', metadata)
    seconds = math.ceil( int(use)/1000000)
    for i in range(1, seconds+1):
        minutes, secs = divmod(i, 60)
        formattedMinutes, formattedSeconds = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(minutes,secs)
        sys.stdout.write('\r' + f"{formattedMinutes:02d}:{formattedSeconds:02d}")
        #formattedString = f"{format(minutes)}:{format(secs)}"
        #sys.stdout.write('\r' + formattedString)
        #sys.stdout.flush()
        #sys.stdout.write('\r' + f"{'{:02}:{:02}'.format(seconds)}")
        time.sleep(1)
def format(x):
    formatted = '{:02}'.format(x)
    return formatted

def mainFunciton():
    event1 = threading.Event()
    event2 = threading.Event()
    user = putInParser('bigga','nacks')
    time.sleep(2)
    event1.set()
    #clientserver.ClientServer().sendToServer(user)
    event1.wait()
    clientserver.ClientServer().sendToServer(user)
    time.sleep(3)
    event2.set()

def putInParser(username,password):
    user ={
                "method" : "login",
                "username" : f"{username}",
                "password" : f"{password}",
                "loggedIn" : False,
            }
    return user

def loginTest():
    #user = putInParser("Watch", "YourBack")
    users = [
             json.dumps(putInParser('winnie','pooh')),
            json.dumps(putInParser('yahoo', 'back')),
             json.dumps(putInParser('bruce', 'wayne')),
             json.dumps(putInParser('holy', 'moly')),
             json.dumps(putInParser('hokey', 'pokey'))
    ]
    
    for i in range(len(users)):
        dbHandler.databaseHandler().dbRegister(users[i])
        #dbHandler.databaseHandler().login(users[i])
        #print(users[i])

def tuples():            
   # sendToServer                                                                          
    user = putInParser('bigga','nacks')
    serialised = json.dumps(user)
    #clientserver.ClientServer().sendToServer(user)
    #clientserver.ClientServer().startClient()
    clientserver.ClientServer().sendToServer(serialised)
            
def sendToServer(info:List[str]):
    bytesData = pickle.dumps(info)
    #print(f"Natural bytes {bytesData}")
    serialised_data =  pickle.loads(bytesData)
    parser(serialised_data)

def parser(*args: List[str]):    
    print(f"Parser function with data:{args[0]}")
    print(range(len(args)))
    try:
        
        lines = args[0].split('\t')
        parsed = ','.join(lines)
        print(f"Using join: {parsed}")
        print(f"Using .split: {lines}")
        print(f"method: {lines[0]}")
        reg(lines[1])
    except Exception as e:
        print(e)


def reg(args:List[str]):
    splitString = args.split('\a')
    print(f"Using join: {', '.join(map(str, splitString))}")
    print(f"Split string {splitString}")
    print(f"Username: {splitString[0]}")
    print(f"Password: {splitString[1]}")

if __name__ == "__main__":
    #runCMD()
    #checker()
    #checkerThread = threading.Thread(target=check)
    #checkerThread.start()
    #makeRed("Something new")
    #integerCheck()
    #
    # client = clientserver.ClientServer().startClient()
    #clientserver.ClientServer().startClient()
    #tuples()
    #mainFunciton()
    #loginTest()
    getMeta()
    #dbHandler.databaseHandler().OrderDB()