import speech_recognition as sr
import pyttsx3
import requests
import webbrowser
from bs4 import BeautifulSoup

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Function to speak a given text
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to listen and convert speech to text
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not get that")
            return None
        except sr.RequestError:
            print("Sorry, my speech service is down")
            return None

# Function to search the internet
def search_internet(query):
    # For simplicity, let's use Wikipedia as an example
    url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        summary = soup.find('p').text
        return summary
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return "I couldn't find any information."

# Main function to handle voice commands
def main():
    speak("Hello, how can I assist you?")
    while True:
        command = listen()
        if command is None:
            continue

        if "search" in command:
            query = command.replace("search", "").strip()
            result = search_internet(query)
            speak(result)

        elif "exit" in command:
            speak("Goodbye!")
            break

        else:
            speak("I can search the internet for you. Just say 'search' followed by your query.")

if __name__ == "__main__":
    main()
