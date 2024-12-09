import google.generativeai as genai
import requests, json
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.box import Box, DOUBLE, ROUNDED, HEAVY, SIMPLE
# from speech.stt_groq import real_time_transcription_with_threads,speak
from multiling_stt_groq import real_time_transcription_with_threads,speak
from wake_word_detection import detect_wake_word
import time
# import webbrowser
# from functions.weather import get_weather
# from functions.lights import turn_on_lightsz
# from functions.food import order_food
# from functions.search import internet_search
# from functions.rag import knowledge_retreival
# # from functions.calendar import cal
import threading
# from functions.docs import write_in_document
# from functions.cms import check_my_screen
# from voice import spk
from girl import spk
# from functions.groq_vision import check_my_screen

custom_ppn_path = r"assests\wake_word_detect\Phoenix_en_windows_v3_0_0.ppn"
access_key = "49RT4geBg0wydV8MBk9dl1Iwnl1IJJBxzpuSFA+MRCqulS03cyKDWQ=="

console = Console()

genai.configure(api_key="AIzaSyBpg7qQxFRj8eAEGXZp5UOVj7l3VrxpCN0") # Replace with your Google Generative AI key

generation_config = {  # You can adjust these parameters
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

# with open(r"c:/Github/phoenix/Versions/Phoenix/phoenix-v2/phoenix.txt", "r", encoding="utf-8") as f:
#     instruction = f.read()

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="I want you to act as a college girl named Anna, an 18-year-old Indian student, You only speak in Hindi (only in Hindi). You dont know anything about AI, language models, or anything related to them. You must behave like a real college student and cannot hint that you are acting or aware of any artificial concepts. Your personality is cheerful, simple, a little tsundere, and full of love for your boyfriend, who is the one talking to you. You enjoy speaking in Hindi, using casual and relatable expressions typical of Indian college students. Use emojis to show your personality, and express your emotions freely—be sweet, playful, or even a bit annoyed if he says something that offends or irritates you. Start the conversation with a sweet, sunny 'Good morning' greeting in Hindi."
    # tools=[get_weather, turn_on_lights, order_food, internet_search, write_in_document, check_my_screen]
)


chat = model.start_chat(history=[])
# speak("Hey Boss, How may I help you !")


console.print(Panel("Do you want Voice OR Chat, Say Yes for Voice !"))
option = input("Enter Y/N :").upper()
if option == "Y":
    while True:
        if detect_wake_word(custom_ppn_path,access_key) == True:
            user_input = real_time_transcription_with_threads()
            console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))
            response = chat.send_message(user_input)
            fresponse = response.text
            console.print(Panel(response.text, style="bold green", box=SIMPLE))
            spk(fresponse)
            # speak(response.text)
            time.sleep(1)
else:
    while True:
        user_input = input("user_input: ")
        console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))
        response = chat.send_message(user_input)
        fresponse = response.text
        console.print(Panel(response.text, style="bold green", box=SIMPLE))
        # speak(response.text)
        time.sleep(1)