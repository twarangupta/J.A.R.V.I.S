import speech_recognition as sr
import pyttsx3
from datetime import datetime

# Initialize speech engine
engine = pyttsx3.init()

# Select voice (0 = Zira, 1 = Hazel)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)


def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()


recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Listening...")
    audio = recognizer.listen(source)

try:
    print("Recognizing...")
    command = recognizer.recognize_google(audio).lower()

    print("You:", command)

    if "hello" in command:
        speak("Hello Twaran. Welcome back!")

    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "your name" in command:
        speak("I am Jarvis.")

    elif "thank you" in command:
        speak("You're welcome.")

    else:
        speak("Sorry, I don't know how to respond to that yet.")

except sr.UnknownValueError:
    speak("Sorry, I couldn't understand you.")
