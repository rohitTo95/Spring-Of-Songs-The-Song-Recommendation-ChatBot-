import speech_recognition as sr
import pyttsx3
import win32com.client
from config import apikey
import openai

openai.api_key = apikey
user_message_list = []
response_message_list = []


def chatBot(input_of_user):
        user_message_list.append({'role': 'system',
                                  'content': 'Your name is Spring. And User is your master, but you will talk to him/her like a best friend. Make him feel good about himself. You are a song recommendation chat bot. Song format will be: Song_Name - By Song_Artist_Name. Suggest at most 10 songs.'})
        user_message_list.append({'role': 'user', 'content': input_of_user})

        user_query = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=user_message_list
        )

        chat_response = user_query['choices'][0]['message']['content']
        response_message_list.append({'role': 'assistant', 'content': chat_response})
        return chat_response



speaker = win32com.client.Dispatch("SAPI.SpVoice")


def speak(message):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Set the index of the desired female voice
    engine.say(message)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.energy_threshold = 4000  # Adjust this value based on your microphone sensitivity
        audio = r.listen(source, phrase_time_limit=3)  # Set the maximum length of an utterance
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print("Some Error Occurred. Sorry  from Spring", e)
            return ""


if __name__ == '__main__':
    print('Welcome to ChatBot')
    speak("Hello, I am Spring. How can I help you?")  # Use the modified speak function
    while True:
        print("Listening...")
        query = takeCommand()
        response = chatBot(query)
        print(f"Spring: {response}")
        speak(response)
