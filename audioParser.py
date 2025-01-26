import os
import colors
import sys
import math
from textwrap import TextWrapper
import multiprocessing
#import pynput
import pyaudio
import re
import time
import json
import subprocess

NowPlaying = r'C:\Users\Tashriq\vs_stuff\python\loginPrac\audio\json\NowPlaying.json'
pathToMusicFiles = r'C:\Users\Tashriq\vs_stuff\python\loginPrac\audio'
wrapper = TextWrapper()
pathToMusicDir = r'C:\Users\Tashriq\vs_stuff\python\loginPrac\audio'

'''
class Listener:  
    def __init__(self):
        self.listener_thread = None
        self.listener_running = False
        self.log = ""

    def start_listener(self):
        if not self.listener_running:
            self.listener_thread = multiprocessing.Process(target=self.listen)
            self.listener_thread.start()
            self.listener_running = True

    def listen(self):
        with pynput.keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()
    
    def on_key_press(self, key):
        newkey = key.char if hasattr(key, 'char') else str(key)
        try:
            if key == pynput.keyboard.Key.esc:
                sys.exit(1)
            if key == pynput.keyboard.Key.space:
                print("Pause(?)")
        except AttributeError:   
            sys.exit(1) 
'''

def removeJson(path=pathToMusicDir):
    remove = input(r'Remove file(y\n): ').capitalize()
    if remove == 'Y':
            for file in os.listdir(path):
                if file.__contains__('.json'):
                    os.remove(path + f'\\{file}')
                    colors.makeGreen(f'Removed {file} successfully')
    else:
        print('Okay...')

def getMeta(mp3Path):
    command = ['ffprobe','-v', '0', '-show_format', '-show_streams', '-of', 'json', mp3Path]
    result = subprocess.check_output(
            command, text=True, shell=True
            )
    metadata = json.loads(result)
    expression = metadata['streams'][0]['duration'].strip()
    timestampIncrement(expression)

def timestampIncrement(metadata):
    with open(NowPlaying, 'r') as file:
        songInfo = json.load(file)  
    use = re.sub(r'[^\d]', '', metadata)
    seconds = math.ceil(int(use)/1000000)
    for i in range(1, seconds+1):     
        minutes, secs = divmod(i, 60)
        formattedMinutes, formattedSeconds = divmod(seconds, 60)
        formattedString = f"{'{:02}'.format(minutes)}:{'{:02}'.format(secs)}"
        sys.stdout.write('\r' + f'{formattedString} - {formattedMinutes:02d}:{formattedSeconds:02d}')
        sys.stdout.flush()
        time.sleep(1)
    #print(f"That was {songInfo['song']} by {songInfo['artist']}")

def streamSong(stream, data):
    stream.write(data)

def play_mp3(mp3Path, fileName):
    timestampProcess = multiprocessing.Process(target=getMeta, args=(mp3Path,))
    if os.path.exists(mp3Path):
        #audio = AudioSegment.from_mp3(mp3Path)
        #length = len(audio)/1000
        #seconds = math.ceil(length/60)
        command = ['ffmpeg','-v', '0' ,'-i', mp3Path, "-f","wav", "-"]
        #command = ['ffmpeg','-i', mp3Path, "-vf","showinfo", "-f", 'null', '-']
        #command = ['ffmpeg','-i', mp3Path, "-f","wav", "-"]
        #process = subprocess.check_output(command, shell=True)
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=2,
                        rate=44100,
                        output=True)
        timestampProcess.start()
        while True:
            data = process.stdout.read(1024)
            if not data:
                break
            # Start threads
            stream.write(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()


def playAudioFile(relativePath, fileName):
    fullPath = relativePath + f'\\{fileName}.mp3'
    try:
        # Open the audio file
        #wf = convertTowav(fullPath, relativePath, fileName)
        play_mp3(fullPath, fileName)
        #print(fullPath, '\n', songName)
        # Read the audio data
        #audioData = wf.readframes(wf.getnframes())
        # Play the audio data using os
        #if os.name == 'nt':
         #   winsound.PlaySound(wf, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as e:
        print(e)

def createMp3Metadata(pathToMusicFiles, mp3file, fileName):
    path = pathToMusicFiles + f'\\{mp3file}'
    outputPath = pathToMusicFiles+ f'\\{fileName}' + '.txt'
    try:
        #print(outputPath)
        # Running the metadata extraction alongside some json parsing
        #command = ["ffprobe", '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', path]
        if not os.path.exists(outputPath):
            command = ['ffmpeg', '-v', path, '-f', 'ffmetadata',outputPath]
        # Returned output is json in itself
            result =subprocess.check_output(
            command,text=True,shell=True
            )
        jsonify(outputPath, fileName)
    except Exception as e:
        print(e)
        #if pathToJson:
         #   removeJson()
        sys.exit(1)
        return None
    
def jsonify(meta, filename, path=pathToMusicDir):
    metadata = {}
    print(meta)
    with open(meta, 'r' ) as f:
        for line in f:
            #key, value = line.strip().split('=')
            strippedLines = line.strip().split('=')
            if len(strippedLines) > 1:
                key, value = strippedLines
                metadata[key] = value

            else:
                print("Doing nothing")
        print(path+f'\\{filename}'+'.json')
        #print(metadata)
        write = json.dumps(metadata, indent=4)
        print(write)
        with open(path+f'\\{filename}'+'.json', 'w') as file:
            json.dump(metadata, file, indent=4)
            time.sleep(2)
        
            
def countFiles(path=pathToMusicDir):
    for file in os.listdir(path):
        # Checks if file is mp3
        if file.__contains__('.mp3'):
            #filePath = pathToMusicDir + f"\\{file}"
            # Takes only the file name
            fileName = file.split('.mp3') 
            # Creates the json path
            pathToJson = pathToMusicDir + f'\\{fileName[0]}' + '.json'
            print(fileName[0])
            createMp3Metadata(pathToMusicDir, f'{file}', fileName[0])

def getInfo():
    array = 0
    songNumber = 0
    songdict = {}
    for file in os.listdir(pathToMusicDir):
        if file.__contains__('.json'):
            songNumber = songNumber + 1
            pathToJson = pathToMusicDir + f'\\{file}'
            with open(pathToJson, 'r') as file:
                musicdata = json.load(file)
                #print(musicdata)
            title = musicdata.get('title')
            #artist = musicdata['artist']
            artist = musicdata.get('artist')
            songdict[songNumber, 'artist'] = title, artist
    
    return songdict


def chooseSong(path=pathToMusicDir):
    #Listener().start_listener()
    # List titles of songs 
    songdict = getInfo()
    print(songdict)
    for key, value in songdict.items():
        print(f"{key[0]}: {value[0]}")
    # Choose song
    choice = int(input("Choose a song: "))
    # play song
    songName = songdict[choice, 'artist'][0]
    #nowPlaying(songdict[choice, 'artist'][0],songdict[choice, 'artist'][1])
    print(f"Now playing: {songdict[choice, 'artist'][0]} by {songdict[choice, 'artist'][1]} ")
    newdict = nameFileMatcher()
    # newdict[songName] is essentially the fileName
    playAudioFile(path, newdict[songName])
    #segmenter(path, parsedSongName)

def nowPlaying(artist, songName):
    data = {
        'artist':artist,
        'song' : songName,
    }
    if not os.path.exists:
        with open(NowPlaying, 'w') as file:
            pass
    else:
        with open(NowPlaying, 'w') as file:
            json.dump(data, file, indent=4)

def nameFileMatcher(path=pathToMusicDir):
    songdict = {}
    for file in os.listdir(path):
        if file.__contains__('.json'):

            pathToJson = path + f'\\{file}'
            with open(pathToJson, 'r') as file:
                musicdata = json.load(file)
            title = musicdata.get('title')
            with open(pathToJson, 'r') as new:
                #data = new.read()
                filename = new.name
                decode = filename.split('.')[0]
                songName = decode.split('\\')[7]
            songdict[title] = songName
    return songdict

if __name__ == "__main__":
    chooseSong()
    #getTimstampThread.start()
    #mp3Play.join()
    #getTimstampThread.start()
    #playwithtimestamp()


