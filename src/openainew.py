import openai
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.box import SIMPLE
from speech_to_text.stt_groq_whisper import real_time_transcription_with_threads
from speech_to_text.wake_word_detection import detect_wake_word
import time

load_dotenv(dotenv_path=r"C:\Github\phoenix\phoenix\.env")
api_key = os.getenv("OPENAI_API_KEY")
print(f"Loaded API key: {api_key}")

custom_ppn_path = r"assests\wake_word_detect\Phoenix_en_windows_v3_0_0.ppn"
access_key = os.getenv("picovoice_api_key")

# Read system instruction from a file
with open(r"C:\Github\phoenix\phoenix\src\phoenix.txt", "r", encoding="utf-8") as f:
    instruction = f.read()

console = Console()

openai.api_key = api_key  # Set the API key globally

# Voice or Chat mode selection
console.print(Panel("Do you want Voice OR Chat? Say Yes for Voice!"))
option = input("Enter Y/N: ")

if option.lower() == "y":
    while True:
        # Wake word detection
        if detect_wake_word(custom_ppn_path, access_key):
            user_input = real_time_transcription_with_threads()
            console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))

            # OpenAI API request
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": instruction},
                        {"role": "user", "content": user_input},
                    ],
                    stream=True,  # Enable streaming response
                )

                # Process streaming response
                for chunk in response:
                    if "choices" in chunk and chunk["choices"][0]["delta"].get("content"):
                        content = chunk["choices"][0]["delta"]["content"]
                        print(content, end="")
                        # Optional: Text-to-speech integration
                        # speak(content)

            except Exception as e:
                console.print(Panel(f"Error: {e}", style="bold red"))
            time.sleep(1)
else:
    while True:
        user_input = input("user_input: ")
        console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))

        # OpenAI API request
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": user_input},
                ],
                stream=True,  # Enable streaming response
            )

            # Process streaming response
            for chunk in response:
                if "choices" in chunk and chunk["choices"][0]["delta"].get("content"):
                    content = chunk["choices"][0]["delta"]["content"]
                    print(content, end="")
                    # Optional: Text-to-speech integration
                    # speak(content)

        except Exception as e:
            console.print(Panel(f"Error: {e}", style="bold red"))
        time.sleep(1)
