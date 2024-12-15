import google.generativeai as genai
import keyboard
import cohere
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.box import Box, DOUBLE, ROUNDED, HEAVY, SIMPLE
from speech_to_text.stt_groq_whisper import real_time_transcription_with_threads,speak
import os
import groq
from dotenv import load_dotenv

load_dotenv()

console = Console()

def sum(fresponse):

    with open(r"src\functions\sum.txt", "r", encoding="utf-8") as f:
        instr = f.read()

    # client = groq.Client(api_key=os.environ["GROQ_API_KEY2"])

    # while 1:
    #     user_input = fresponse

    #     chat_completion = client.chat.completions.create(
    #         messages=[
    #             {
    #                 "role": "user",
    #                 "content": instr + user_input,
    #             }
    #         ],
    #         model="llama-3.3-70b-versatile",
    #     )

    #     print(chat_completion.choices[0].message.content)
    #     fr = chat_completion.choices[0].message.content
    api_key = os.getenv("cohere_api_key")

    co = cohere.ClientV2(api_key)
    response = co.chat(
        model="command-r-plus", 
        messages=[
            {"role": "user",
            "content": instr + fresponse}
            ]
    )
    print(response.message.content[0].text)
    fr = response.message.content[0].text

    if keyboard.is_pressed('esc'):
        console.print(Panel("Process stopped by user.", style="bold red", box=SIMPLE))
        exit
    else:
        speak(fr)