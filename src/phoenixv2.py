import google.generativeai as genai
import requests, json
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.box import Box, DOUBLE, ROUNDED, HEAVY, SIMPLE
from speech_to_text.stt_groq_whisper import real_time_transcription_with_threads,speak
from speech_to_text.wake_word_detection import detect_wake_word
import time
from functions.weather import get_weather
from functions.lights import turn_on_lights
from functions.food import order_food
from functions.search import internet_search
from functions.rag import knowledge_retreival
from functions.calendar import cal
from functions.docs import write_in_document
from text_to_speech.elevenlabs_stream import spk
from functions.summary import sum
import os
from dotenv import load_dotenv
import keyboard
from functions.perplex import research

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
    tools=[get_weather, turn_on_lights, order_food, internet_search, cal, write_in_document, research]
)

chat = model.start_chat(history=[],enable_automatic_function_calling=True)

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