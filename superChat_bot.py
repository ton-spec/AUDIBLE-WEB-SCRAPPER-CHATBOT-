import os
import random
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
from playsound import playsound
import re
import sys

def speak(text):
    # Initialize the gTTS object with the text to be spoken
    tts = gTTS(text=text, lang='en', tld='com')

    # Save the spoken text as an MP3 file
    tts.save('response.mp3')

    # Use the 'playsound' module to play the MP3 file
    playsound('response.mp3')

# Sample chatbot code
while True:
    user = input("User:")

    # Create a dictionary of possible responses with corresponding keywords
    possible_responses = {
        "hello": ["Hello there, how can I help you?", "Nice to meet you! What can I do for you?"],
        "help": ["Hi, how can I be of assistance?", "Greetings! What can I help you with?", "Howdy! What can I do for you today?"]
    }

    # Find a response that matches at least one user input word
    response_text = ""
    for keyword in possible_responses.keys():
        if any(word in user.lower() for word in keyword.split()):
            response_text = random.choice(possible_responses[keyword])
            break

    # If no matching keyword is found, check if the user input is in a web page
    if not response_text:
        # Scrape a web page
        url = 'https://en.wikipedia.org/wiki/' + user
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        web_text = soup.get_text().lower()
        if any(word in web_text for word in user.lower().split()):
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                paragraph_text = paragraph.get_text().strip()
                if paragraph_text and not paragraph_text.startswith("[") and not paragraph_text.endswith("]") and not paragraph_text.endswith(".") and not paragraph_text.endswith(",") and not paragraph_text.endswith(":") and not paragraph_text.endswith(";") and not paragraph_text.endswith("?") and not paragraph_text.endswith("!") and not paragraph_text.endswith("'") and not paragraph_text.endswith('"'):
                    response_text = paragraph_text
                    break

    # If still no matching response is found, use a default response
    if not response_text:
        response_text = "I'm sorry, I don't understand. Can you please rephrase your question?"

   
    
    print("Chatbot:", response_text)

   

 

    if response_text.strip() != "":
        # Use the 'speak' function to generate and play the spoken response
        speak(response_text)
    else:
        print("Chatbot: I'm sorry, I don't understand. Can you please rephrase your question?")

    # Remove the temporary MP3 file
    if os.path.exists('response.mp3'):
        os.remove('response.mp3')
