import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import speech_recognition as sr
import pyaudio
import os

# Load pre-trained model and tokenizer
model_name = "t5-base"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Set up speech recognition
r = sr.Recognizer()

def listen():
    """Listen to user input through microphone"""
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-US")
            print(f"User: {query}")
            return query
        except sr.UnknownValueError:
            print("JARVIS: Sorry, I didn't understand that.")
            return ""

def respond(query):
    """Generate response using T5 model"""
    inputs = tokenizer(query, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"JARVIS: {response}")
    return response

def main():
    while True:
        query = listen()
        if query:
            respond(query)

if __name__ == "__main__":
    main()