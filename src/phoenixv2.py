import google.generativeai as genai
import requests, json
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.box import Box, DOUBLE, ROUNDED, HEAVY, SIMPLE
from speech_to_text.stt_groq_whisper import real_time_transcription_with_threads,speak
from speech_to_text.wake_word_detection import detect_wake_word
import time
import webbrowser
from functions.weather import get_weather
from functions.lights import turn_on_lights
from functions.food import order_food
from functions.search import internet_search
from functions.rag import knowledge_retreival
from functions.calendar import cal
import threading
import os
from dotenv import load_dotenv

load_dotenv()

custom_ppn_path = r"assests\wake_word_detect\Phoenix_en_windows_v3_0_0.ppn"
access_key = os.getenv("picovoice_api_key")

console = Console()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) #Replace with your Google Generative AI key

generation_config = {  # You can adjust these parameters
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

with open(r"C:\Github\phoenix\phoenix\src\phoenix.txt", "r", encoding="utf-8") as f:
    instruction = f.read()

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=instruction,
    tools=[get_weather, turn_on_lights, order_food, internet_search, cal]
)


chat = model.start_chat(history=[],enable_automatic_function_calling=True)
speak("Hey Boss, How may I help you !")


def sum(fresponse):
    genai.configure(api_key=os.getenv("gemini_api2_key"))

    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-8b",
        generation_config=generation_config,
        system_instruction="Greetings, sir, I am your personal assistant. I'm here to help, chat, and provide support in a way that feels natural and engaging. I adapt to your preferences, keep our conversations relevant and friendly, and ensure you get accurate and useful information. Let's make every interaction smooth, enjoyable, and tailored just for you. Your role involves summarizing any given text in a natural, conversational manner,(You will be given text from an AI model, which you have to interpret humanly for a good natural assistant conversation) ignoring punctuation marks and avoiding special formatting and avoid markdown format too.You accept feedback give suggestions in a friendly manner, You call me Sir! ( Backend working just for the sake of your understanding -> Harshal ( Sir ) -> AI Model-1 -> AI Model-2 ( You, which summarize the text from AI Model-1), but you 2 work together for Sir, Harshal)"
    )

    chat_session = model.start_chat(history=[])
    sresponse = chat_session.send_message(fresponse)
    speak(sresponse.text)

console.print(Panel("Do you want Voice OR Chat, Say Yes for Voice !"))
option = input("Enter Y/N : ")
if option == "Y" or "y":
    while True:
        if detect_wake_word(custom_ppn_path,access_key) == True:
            user_input = real_time_transcription_with_threads()
            console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))
            response = chat.send_message(user_input)
            fresponse = response.text
            console.print(Panel(response.text, style="bold green", box=SIMPLE))
            sum(fresponse)
            # speak(response.text)
            time.sleep(1)
else:
    while True:
        user_input = input("user_input: ")
        console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))
        response = chat.send_message(user_input)
        fresponse = response.text
        console.print(Panel(response.text, style="bold green", box=SIMPLE))
        sum(fresponse)
        # speak(response.text)
        time.sleep(1)