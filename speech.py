# speech.py
import speech_recognition as sr
import pyttsx3
import random

recognizer = sr.Recognizer()

def recognize_speech():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            response = recognizer.recognize_google(audio)
            return response.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            print("Could not request results. Check your internet connection.")

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 0.9)
    engine.say(text)
    engine.runAndWait()

def generate_user_id():
    return random.randint(100000, 999999)

