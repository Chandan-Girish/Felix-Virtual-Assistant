import sqlite3
import struct
import time, datetime
import webbrowser
from urllib.parse import quote
import eel
import os
import pyaudio
import pvporcupine
import pyautogui
import wikipedia
import requests

from playsound import playsound
from engine.command import speak
from engine.config import ASSISTANT_NAME, PICOVOICE_API
import pywhatkit as kit
from hugchat import hugchat

from engine.helper import extract_yt_term

# Database
conn = sqlite3.connect("felix.db")
cursor = conn.cursor()


# Assistant Sound
@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)


# Open Function
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0:
                cursor.execute(
                    'SELECT url FROM  web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak('Requested resource not found!')
        
        except:
            speak("Something went wrong!")


# YouTube Automation
def playYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


# HotWord Detection 
def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
        access_key = PICOVOICE_API
        keyword_path = r'www\\assets\\felix\\felix_en_windows_v3_0_0.ppn'
        porcupine=pvporcupine.create(access_key=access_key,keyword_paths=[keyword_path]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        while True:
            try:
                keyword=audio_stream.read(porcupine.frame_length)
                keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

                keyword_index=porcupine.process(keyword)

                if keyword_index>=0:
                    print("hotword detected")

                    # pressing shorcut key win+j
                    import pyautogui as autogui
                    autogui.keyDown("win")
                    autogui.press("j")
                    time.sleep(2)
                    autogui.keyUp("win")
                    
            except Exception as e:
                print(f"Error processing audio: {e}")
    
    except Exception as e:
        print(f"An error occured: {e}")
         
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


# Wikipedia 
def searchWikipedia(query):
    speak("Searching wikipedia...")
    query = query.replace("wikipedia", "")
    query = query.replace("search wikipedia for", "")
    query = query.replace(ASSISTANT_NAME, "")
    results = wikipedia.summary(query, sentences = 4)
    speak("According to wikipedia "+ results)
    print(results)

# Greeting 
def greeting():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        res = "Good Morning!"
    
    elif hour>=12 and hour<17:
        res = "Good Afternoon!"

    else:
        res = "Good Evening!"
    
    speak(res + " How may I help you?")

# Google Search
def search_google(query):
    query = query.replace("google","")
    query = query.replace("search","")
    query = query.replace("for","")
    query = query.replace("from","")
    speak(f"Searching google for {query}")
    search_url = f"https://www.google.com/search?q={quote(query)}"
    webbrowser.open(search_url)


# Weather Information
from engine.config import WEATHER_API
def get_weather_report(query):
    query = query.replace("what's the weather", "")
    query = query.replace("weather", "")
    query = query.replace("in","")
    api_key = WEATHER_API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            temp = round(temperature)
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            wind = round(wind_speed * 3.6)
            report = f"Weather in {query}: {weather_description}\tTemperature: {temp}°C\tHumidity: {humidity}%\tWind Speed: {wind} kilometers per hour"
            speak(report)
            return report
        else:
            speak("Error: City not found")
    except Exception as e:
        return f"An error occurred: {str(e)}"



# Chat-GPT
def chatGpt(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

#Time
def timeFunction():
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"Current time is {time}")

#date and day
def dateAndDay():
    day = datetime.datetime.now().strftime("%A")
    date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"It's {day}, {date}")


# Close Function
def shutDown():
    speak("Goodbye! System shutting down")
    pyautogui.hotkey("ctrl","w")
        






