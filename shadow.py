import pyttsx3
import speech_recognition as sr
import datetime 
import wikipedia
import webbrowser
import os
os.add_dll_directory(r'C:\\Program Files\\VideoLAN\\VLC')
import smtplib
import requests
import random
from random import randrange
import email
import imaplib
import numpy as np
from youtube_search import YoutubeSearch
import json
import pafy,vlc,youtube_dl
from datetime import date
from sound import Sound



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[4].id)
engine.setProperty('voice', voices[4].id)  #  voice id  (assigning a voice)

maildict={"antony":"sumukhabs5@gmail.com"}
username = 'sumukhabs31@gmail.com'
password='gotohell77@'
imapurl="imap.gmail.com"
attachment_dir="C:\\Users\\Sumukha\\Documents\\Emails"


#def getbody(msg):
    #if msg.is_multipart():
        #msgg=getbody(msg.get_payload(0))
        #return msgg

        #for payload in msg.get_payload():
            #print(payload.get_payload())

        #msg_string=msg.decode('utf-8')
        # converts byte literal to string removing b''
        #email_message = email.message_from_string(msg_string)
        #print(email_message)
        
    #else:
        #return msg.get_payload(None,True)
        #speech(msg.get_payload())


def readmail(): 
        mail = imaplib.IMAP4_SSL(imapurl)
        mail.login(username,password)
        mail.list()
        mail.select("INBOX")
        type, data = mail.search(None, 'ALL')
        mailids=data[0]
        id_list = mailids.split()
        latest_email = (id_list[-1])
        result, data=mail.fetch(latest_email,'(RFC822)')

        msg = email.message_from_bytes(data[0][1])
        email_subject = msg['subject']
        email_from = msg['from']
        
        speech('The last Mail you receved is From : ' + email_from )
        speech('Subject is: ' + email_subject)
        
        #raw=email.message_from_bytes(data[0][1])
        raw_email=data[0][1]
        raw_email_string=raw_email.decode('utf-8')
        raw=email.message_from_string(raw_email_string)
        for part in raw.walk():
            if part.get_content_type() == "text/plain": # ignore attachments/html
                body = part.get_payload(decode=True)
                body2=body.decode('utf-8')
                speech("message is: " + body2)

            else:
                continue

        for part in msg.walk():
            if part.get_content_maintype()=='multipart':
                continue 

            if part.get('Content-Disposition') is None:
                continue

            fileName = part.get_filename()

            if bool(fileName):
                filePath = os.path.join(attachment_dir, fileName)
                with open(filePath,'wb') as f:
                    f.write(part.get_payload(decode=True))
                    speech("This Mail contains an attachment named "+ fileName)
                    speech("It is saved in emails in Document Folder")

        
        


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
        print("Say that again..")
        return "None"
    return query

def sendMail(mailId,message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(username,mailId , message)
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

def giveweather():
    return


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

        elif 'open spotify' in query:
           spotifyPath='C:\\Users\\Sumukha\\AppData\\Roaming\\Spotify\\Spotify.exe'
           os.startfile(spotifyPath)

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

       
        elif 'gmail' in query or 'mail' in query:
            webbrowser.open("https://mail.google.com/mail/u/2/#inbox")
            readmail()

        elif 'youtube' in query:
            results = YoutubeSearch(query, max_results=10).to_json()
            ress=json.loads(results)
            p=ress['videos']
            q=p[0]
            r=q['id']
            webbrowser.open("http://www.youtube.com/watch?v=" + r)
            
            #url="http://www.youtube.com/watch?v=" + r
            #video=pafy.new(url)
            #best=video.getbest()
            #media=vlc.MediaPlayer(best.url)
            #media.play()

        elif 'tell me a joke' in query:
            res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
            if res.status_code == requests.codes.ok:
                speech(str(res.json()['joke']))
            else:
                speech('oops!I ran out of jokes')

        elif "close browser" in query:
            #os.system("taskkill /im firefox.exe /f")
            os.system("taskkill /im chrome.exe /f")

        elif "weather" in query:
            giveweather()

        elif 'quit' in query:
            exit(0)

        elif 'restart pc' in query:
            os.system("shutdown /r /t 1")

        elif 'shutdown pc' in query:
            os.system("shutdown /s /t 1")


        elif 'mute' in query or 'unmute' in query:
            Sound.mute()

        elif 'increase volume' in query:
            Sound.volume_up()

        elif 'decrease volume' in query:
            Sound.volume_down()

        elif 'set maximum volume' in query:
            Sound.volume_min()

        elif 'set volume to zero' in query:
            Sound.volume_max()



