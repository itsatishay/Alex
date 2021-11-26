# all library imports
from pyautogui import *
import pyautogui
import time
import keyboard
import win32api, win32con
import logging
import speech_recognition as speech
import asyncio
from gtts import gTTS
from playsound import playsound
from pyfiglet import Figlet


# global state variables
lastLocation = []
enableLogging = True
recording = speech.Recognizer()
loop = asyncio.get_event_loop()
speechLanguage = 'en'
consoleStyleFont = Figlet(font='slant')
sleepSeconds = 0.5


# function for text to speech
def speak(sentence):
    print(sentence)
    myobj = gTTS(text=sentence, lang=speechLanguage, slow=False)
    myobj.save("speechrecord.mp3")
    audio_file = os.path.dirname(__file__) + '/speechrecord.mp3'
    playsound(audio_file)
    os.remove(audio_file)


# perform speech recognition
def speechrecog():
    with speech.Microphone() as source: recording.adjust_for_ambient_noise(source)
    speak("What can I do for you today:")
    with speech.Microphone() as source:
        audio = recording.listen(source, phrase_time_limit=5)
    try:
        recognizedText = recording.recognize_google(audio)
        print("You said: " + recognizedText)
        return recognizedText
    except Exception as e:
        print(e)


# function to handle logging
def logs(statements, stype=1):
    if enableLogging:
        if stype is 1:
            print(statements)
        else:
            logging.warning(statements)


# function create to write any sentence/word
def keywrite(sentence):
    keyboard.write(sentence)
    time.sleep(sleepSeconds)


# function created to execute any keyboard key press
def keypress(key):
    keyboard.press_and_release(key)
    time.sleep(sleepSeconds)


# function to click mouse on a given x and y axis
def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


# this function will take the image that needs to be detected , how much percentage accuracy you want for the image
# you can also provide that if you can skip the particular step if the image is not detected
# if the bot is not able to detect the image still after 8 iterations. the program will be terminated
def findimclick(imagefile, confidence=0.8, canskip=False, failedcounter=0, plusxaxis=0, plusyaxis=0, shouldwait=False):
    logs("executing step: " + imagefile)
    failedcounter = failedcounter
    if pyautogui.locateOnScreen(imagefile, confidence=confidence) is not None:
        location = pyautogui.locateOnScreen(imagefile, confidence=0.8)
        time.sleep(sleepSeconds)
        click(location[0]+plusxaxis, location[1]+plusyaxis)
        logs("execution of step: " + imagefile + " successful")
        global lastLocation
        lastLocation = location
        failedcounter = 0
        time.sleep(sleepSeconds)
        return

    elif failedcounter > 6 and canskip:
        # do nothing
        logs("skipping step : " + imagefile, 0)
        return

    elif failedcounter > 7:
        # stop the bot
        #speak("Sorry i can't process your command")
        if failedcounter < 14 and shouldwait:
            findimclick(imagefile, confidence, canskip, failedcounter+1, plusxaxis, plusyaxis, shouldwait)
        else:
            bootalex()

        # will retry the last step as because it might be possible that the last step was not successful
        # also while retrying the bot will tweak the x and y axis value by 20
    else:
        if failedcounter > 5 and not shouldwait:
            logs("retrying last step..", 0)
            click(lastLocation[0] + 20, lastLocation[1] + 20)
        logs("don't see .. trying again " + imagefile, 0)
        time.sleep(sleepSeconds)
        findimclick(imagefile, confidence, canskip, failedcounter+1, plusxaxis, plusyaxis, shouldwait)


# function to select your own custom bot and run it
def onlyrunbot():
    choicebot = int(input("Enter number of your bot: "))
    if choicebot is 1:
        # write your function name here if you just want to execute the function and not alex
    else:
        print("Your choice bot does not exist")
        choiceaction()


# give choice to user to perform any action
def choiceaction():
    stage1 = int(input("Choose Action: \n 1. Start Alex \n 2. Run Bot \n"))
    if stage1 is 1:
        bootalex()

    elif stage1 is 2:
        onlyrunbot()

    else:
        print("No option is available with this number: " + str(stage1))
        choiceaction()


# print text with style on console
def printstyletext(text):
    print(consoleStyleFont.renderText(text))


# function to start up alex
def bootalex():
    print('\n\n')
    printstyletext('A l e x')
    print('\n\n')
    print('Press A on keyboard to command Alex')
    while 1:
        if keyboard.is_pressed("A"):
            command = speechrecog()
            # if the person has not spoken any command rerun alex
            if command is None:
                bootalex()
            else:
                processvoicecommandstring(command)


# process voice command string
def processvoicecommandstring(command):
    if command.__contains__("word") and command.__contains__("word"):
        # write your function name here
        bootalex()
    else:
        speak("Sorry i don't understand your command")
        bootalex()


# mouse event to scroll action
def mousescroll(value):
    win32api.mouse_event(0x0800, 0, 0, value, 0)


# start of everything
choiceaction()





