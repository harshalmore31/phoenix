import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
from markdown import markdown

load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])

while True:
    try:
        # User input and response from Google AI
        user_input = input("User_Input : ")
        response = chat_session.send_message(user_input)
        google_response = response.text
        print(google_response)

    except Exception as e:
        print(f"An error occurred: {e}")
