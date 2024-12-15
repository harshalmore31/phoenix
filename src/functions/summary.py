import google.generativeai as genai
import keyboard
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.box import Box, DOUBLE, ROUNDED, HEAVY, SIMPLE
from speech_to_text.stt_groq_whisper import real_time_transcription_with_threads,speak
import os
from dotenv import load_dotenv

load_dotenv()


console = Console()

def sum(fresponse):
    genai.configure(api_key=os.getenv("gemini_api2_key"))

    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    with open(r"src\functions\sum.txt", "r", encoding="utf-8") as f:
        instr = f.read()

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-8b",
        generation_config=generation_config,
        system_instruction=instr
    )

    chat_session = model.start_chat(history=[])
    sresponse = chat_session.send_message(fresponse)
    fr = sresponse.text
    if keyboard.is_pressed('esc'):
        console.print(Panel("Process stopped by user.", style="bold red", box=SIMPLE))
        exit
    else:
        speak(fr)