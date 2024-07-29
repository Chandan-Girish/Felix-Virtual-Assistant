import pyttsx3
import speech_recognition as sr
import eel
import time

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voices', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()
    

def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 4, 6)

    try:
        print('Recognizing')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language = 'en-in')
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        
    except Exception as e:
        speak("Something went wrong!")
    
    return query.lower()


@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takeCommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    try:
        
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import playYoutube
            playYoutube(query) 
        elif "wikipedia" in query:
            from engine.features import searchWikipedia
            searchWikipedia(query)
        elif "google" in query:
            from engine.features import search_google
            search_google(query)
        elif "weather" in query:
            from engine.features import get_weather_report
            get_weather_report(query)
        elif "time" in query or "current time" in query:
            from engine.features import timeFunction
            timeFunction()
        elif "date" in query or "day" in query:
            from engine.features import dateAndDay
            dateAndDay()
        elif "shut down" in query or "shutdown" in query:
            from engine.features import shutDown
            shutDown()
        else:
            from engine.features import chatGpt
            chatGpt(query)

    except:
        speak("Something went wrong!")
        eel.ReturnLanding()

    eel.ReturnLanding()



