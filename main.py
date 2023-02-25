import datetime
from unittest import result
# from itertools import count
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import pandas as pd


data=pd.read_csv(r'C:\Users\Suryansh\Downloads\stories - stories.csv')


eng = pyttsx3.init('sapi5')# To take voice
voices = eng.getProperty('voices')
eng.setProperty('voice',voices[1].id)
eng.setProperty('rate', 160)


def speaking(audio):
    eng.say(audio)
    eng.runAndWait()


def wishme():

    hour = int(datetime.datetime.now().hour)
    
    if hour>=0 and hour<12:
        speaking("Good Morning ")
    
    elif hour>=12 and hour<16:
        speaking("Good Afternoon")
    
    else:
        speaking("Good Evening")
    
    speaking("Hello I am Stacy ! Which story would you like to hear today")


def takecommand():

    #takes input from speaking
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Stacy is listening!!!!!")
        r.pause_threshold = 2
        r.energy_threshold = 700
        audio = r.listen(source)

    try:
        print("Recognising....")
        query = r.recognize_google(audio,language='en-in')
        print("You want to hear story about ",query)
    
    except Exception as e:        
        print("Do You want to hear another story")
        speaking("Do You want to hear another story")
        return "None"
    
    return query


if __name__ == "__main__":
    
    wishme()
    keys = data['keypoints']
    print(type(keys[0]))

    while True:        
        query = takecommand().lower()
        print(query)
        if 'exit' in query:
            speaking("Exiting GoodBye")
            print(("Exiting GoodBye"))
            exit()
        else:
            k = (data['keypoints'])
            key = []
            for _ in range(len(k)):
                L = (list(k[_].split(', ')))
                key.append(L)
            key_list = []
            for i in range(len(key)):
                for j in range(len(key[i])):
                    key_list.append(key[i][j])
            key_list = list(set(key_list))
            len(key_list)
            diction = {}
            n = len(key_list)
            for i in range(len(key_list)):
                diction[key_list[i]] = i

            lis = [[] for x in range(n)]
            for i in range(len(key)):
                for j in range(len(key[i])):
                    lis[diction[key[i][j]]].append(i)
            tit = data['Title']
            title = []
            for _  in range(len(tit)):
                title.append(tit[_])
            key_words = []
            str = ""
            for i in range(len(query)):
                if(query[i] == ' '):
                    key_words.append(str)
                    str = ""
                else:
                    if query[i]!=' ':
                        str = str + query[i]
            if(str!=""):
                key_words.append(str)
            print(key_words)
            res = [0]*len(tit)

            pp = []
            for i in range(len(key_words)):
                if key_words[i] in diction.keys():
                    pp = lis[diction[key_words[i]]]
                    for k in range(len(pp)):
                        res[pp[k]] += 1
            
            ind = -1
            maxi = 0
            for i in range(len(res)):
                if res[i] > maxi:
                    maxi = res[i]
                    ind = i

            if(ind == -1):
                print("No story found")
                speaking("No story found")
            
            else:
                print(data['Story'][ind])
                speaking(data['Story'][ind])