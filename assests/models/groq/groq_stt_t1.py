import os
import groq
from dotenv import load_dotenv
# from realtimecopy import real_time_transcription_with_threads
from stt_groq import real_time_transcription_with_threads
load_dotenv()

client = groq.Client(api_key=os.environ["GROQ_API_KEY"])

while 1:
    user_input = real_time_transcription_with_threads()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        model="llama3-8b-8192",
    )

    print(chat_completion.choices[0].message.content)