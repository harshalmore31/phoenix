from openai import OpenAI
from dotenv import load_dotenv
import os
from speech_to_text.stt_groq_whisper import real_time_transcription_with_threads,speak
from speech_to_text.wake_word_detection import detect_wake_word
import time

load_dotenv()

client = OpenAI()


custom_ppn_path = r"assests\wake_word_detect\Phoenix_en_windows_v3_0_0.ppn"
access_key = os.getenv("picovoice_api_key")

with open(r"C:\Github\phoenix\phoenix\src\phoenix.txt", "r", encoding="utf-8") as f:
    instruction = f.read()

print("Do you want Voice OR Chat? Say Yes for Voice!")
option = input("Enter Y/N: ")

if option == "Y":
    user_input = real_time_transcription_with_threads()
    while True:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": instruction},
                      {"role": "user", "content": user_input}],
            stream=True,
        )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
elif option == "N":
    user_input = input("user_input : ")
    stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": instruction},
                      {"role": "user", "content": user_input}],
            stream=True,
        )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
else:
    print("Invalid input. Please enter 'Y' or 'N'.")
