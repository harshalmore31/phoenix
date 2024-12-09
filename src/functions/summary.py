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

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-8b",
        generation_config=generation_config,
        system_instruction="Greetings, sir, I am your personal assistant. I'm here to help, chat, and provide support in a way that feels natural and engaging. I adapt to your preferences, keep our conversations relevant and friendly, and ensure you get accurate and useful information. Let's make every interaction smooth, enjoyable, and tailored just for you. Your role involves summarizing any given text in a natural, conversational manner,(You will be given text from an AI model, which you have to interpret humanly for a good natural assistant conversation) ignoring punctuation marks and avoiding special formatting and avoid markdown format too.You accept feedback give suggestions in a friendly manner, You call me Sir! ( Backend working just for the sake of your understanding -> Harshal ( Sir ) -> AI Model-1 -> AI Model-2 ( You, which summarize the text from AI Model-1), but you 2 work together for Sir, Harshal)"
    )

    chat_session = model.start_chat(history=[])
    sresponse = chat_session.send_message(fresponse)
    fr = sresponse.text
    if keyboard.is_pressed('esc'):
        console.print(Panel("Process stopped by user.", style="bold red", box=SIMPLE))
        exit
    else:
        speak(fr)