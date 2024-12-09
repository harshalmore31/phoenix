import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
from markdown import markdown

load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("gemini_api1_key"))

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])

# NVIDIA API Client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("nvidia_api_key"),
)

while True:
    try:
        # User input and response from Google AI
        user_input = input("User_Input : ")
        response = chat_session.send_message(user_input)
        google_response = response.text
        print(google_response)

        # Send to NVIDIA model
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-reward",
            messages=[
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": google_response},
            ],
        )

        # Extract the NVIDIA response and reward
        message_content = completion.choices[0].message.content  # Message content
        reward_value = float(message_content.split(":")[1].strip())  # Parse reward value
        formatted_output = (
            f"Prompt: {user_input}\nResponse: {message_content}\nReward: {reward_value}"
        )

        # Display the formatted output
        print(formatted_output)

        # Feedback loop with Google AI
        feedback_input = f"This is Your Reward For your Generation:\n{formatted_output}"
        feedback_response = chat_session.send_message(feedback_input)
        print(feedback_response.text+"\n")

    except Exception as e:
        print(f"An error occurred: {e}")
