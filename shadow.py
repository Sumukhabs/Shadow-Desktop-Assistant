import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
import random
from random import randrange


maildict={"antony":"sumukhabs5@gmail.com"}

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[4].id)
engine.setProperty('voice', voices[4].id)  #  voice id  (assigning a voice)


def speech(audio):
    engine.say(audio)  # it will speak out the passed audio
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)  # extracts current time
    if hour >= 0 and hour < 12:
        speech("Hello ,Good Morning!")
    elif hour >= 12 and hour < 14:
        speech("Hello ,Good Afternoon!")
    else:
        speech("Hello,good Evening!")
    speech(" I am Shadow, please tell me how may I help you?")


def takeCommand():
    '''
    It will take voice command from the user and returns it as a string
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")
    except Exception as e:
        print(e)
        speech("Sorry , can you repeat?")
        return "None"
    return query

def sendMail(mailId,message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('sumukhabs31@gmail.com', 'Gotohell7@')
    server.sendmail('sumukhabs31@gmail.com',mailId , message)
    server.close()

def givenews():
    apiKey = '49e391e7066c4158937096fb5e55fb5d'
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={apiKey}"
    r = requests.get(url)
    data = r.json()
    data = data["articles"]
    flag = True
    count = 0
    for items in data:
        count += 1
        if count > 10:
            break
        print(items["title"])
        to_speak = items["title"].split(" - ")[0]
        if flag:
            speech("Today's top ten Headline are : ")
            flag = False
        else:
            speech("Next news :")
        speech(to_speak)


def clear():
    # To clear the console after each command
    _ = os.system('cls')



if __name__ == "__main__":
    wish()
    while True:
        query=takeCommand().lower()
        #logic for excecuting tasks based on query
        if 'wikipedia' in query:
            speech("Searching wikipedia...")
            query=query.replace("wikipedia","")
            results=wikipedia.summary(query,sentences=2)
            speech("According to wikipedia")
            speech(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query or 'play songs' in query:
            music_dir='C:\\Users\\Sumukha\\Music'
            sno=len(music_dir)
            rint=randrange(0,sno-1)
            songs=os.listdir(music_dir)
            os.startfile(os.path.join(music_dir,songs[rint]))

        elif 'the time' in query:
            time= datetime.datetime.now().strftime("%H:%M:%S")
            speech(f" Sir the time is {time}")

        elif 'open atom editor' in query:
           atomPath='C:\\Users\\Sumukha\\AppData\\Local\\atom\\atom.exe'
           os.startfile(atomPath)

        elif 'send email' in query:
            try:
                speech("Whom should I send a mail?")
                to = takeCommand().lower()
                mailId=maildict[to]
                #print(mailid)
                speech(f"What Should I Say to {to}")
                message=takeCommand()
                sendMail(mailId,message)
                speech("mail has been sent boss")

            except Exception as e:
                print(e)
                speech("sorry boss, I am unable to send a mail rightnow")

        elif 'headlines' in query or 'news' in query or 'headline' in query:
            givenews()


        elif 'what' in query or 'who' in query or 'where' in query or 'can you' in query:
            webbrowser.open(f"https://www.google.com/search?&q={query}")
            speech(wikipedia.summary(query, sentences=2))

        elif 'quit' in query:
            exit(0)
