import os
import time
import keyboard
from google import genai
from google.genai import types
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.box import Box, DOUBLE, ROUNDED, HEAVY, SIMPLE
from speech_to_text.stt_groq_whisper import real_time_transcription_with_threads, speak
from speech_to_text.wake_word_detection import detect_wake_word
from functions.weather import get_weather
from functions.lights import turn_on_lights
from functions.food import order_food
from functions.intersearch import search
# from functions.tsearch import search
from functions.rag import knowledge_retreival
from functions.my_calendar import cal
from functions.docs import write_in_document
# from text_to_speech.elevenlabs_stream import spk
from functions.summary import sum
from functions.cms import check_my_screen
from functions.code import write_code
from functions.krya import todo
from dotenv import load_dotenv

load_dotenv()

custom_ppn_path = r"assests\wake_word_detect\Phoenix_en_windows_v3_0_0.ppn"
access_key = os.getenv("picovoice_api_key")

console = Console()

# Initialize the Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Read the instructions
# with open(r"C:\Github\phoenix\phoenix\src\phoenix.txt", "r", encoding="utf-8") as f:
#     instruction = f.read()

# Convert the function tools to the new format
def convert_to_function_declarations(tools_list):
    function_declarations = []
    for tool in tools_list:
        function_declaration = types.FunctionDeclaration(
            name=tool["name"],
            description=tool["description"],
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    param["name"]: types.Schema(
                        type=types.Type.STRING if param["type"] == "string" else types.Type.NUMBER,
                        description=param.get("description", "")
                    ) for param in tool.get("parameters", {}).get("properties", [])
                },
                required=[param["name"] for param in tool.get("parameters", {}).get("required", [])]
            )
        )
        function_declarations.append(function_declaration)
    return function_declarations

# List of tools to be converted
tools_list = [get_weather, turn_on_lights, order_food, search, cal, write_in_document, check_my_screen, write_code, todo]

# Create the Tool object with function declarations
tools = [types.Tool(function_declarations=convert_to_function_declarations(tools_list))]

# Generation config
generate_content_config = types.GenerateContentConfig(
    temperature=0.2,
    top_p=0.95,
    top_k=40,
    max_output_tokens=1024,
    tools=tools,
)

# Model configuration
model = "gemini-exp-1206"  # Use the model name from your old code

# Initialize chat history
chat_history = []

# Function to process response
def process_response(response):
    if hasattr(response, 'function_calls') and response.function_calls:
        # Handle function calls here
        function_call = response.function_calls[0]
        function_name = function_call.name
        function_args = function_call.args
        
        # Call the appropriate function based on the function name
        # This is a placeholder - you'll need to implement the actual function calling logic
        console.print(f"Function called: {function_name} with args: {function_args}")
        
        # Execute the function and get the result
        # result = execute_function(function_name, function_args)
        
        # Add the function call and result to the chat history
        # chat_history.append(...)
        
        return "Function response placeholder"  # Replace with actual function response
    else:
        return response.text

# Function to send a message and get a response
def send_message(user_input):
    # Add user message to history
    chat_history.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)],
        )
    )
    
    # Generate response
    response = client.models.generate_content(
        model=model,
        contents=chat_history,
        config=generate_content_config,
    )
    
    # Process the response
    processed_response = process_response(response)
    
    # Add model response to history
    chat_history.append(
        types.Content(
            role="model",
            parts=[types.Part.from_text(text=processed_response)],
        )
    )
    
    return processed_response

# Main execution
console.print(Panel("Do you want Voice OR Chat, Say Yes for Voice !"))
option = input("Enter Y/N : ")

if option == "Y" or option == "y":
    while True:
        if detect_wake_word(custom_ppn_path, access_key) == True:
            user_input = real_time_transcription_with_threads()
            console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))
            response_text = send_message(user_input)
            console.print(Panel(response_text, style="bold green", box=SIMPLE))
            # sum(response_text)
            speak(response_text)
            time.sleep(1)
else:
    while True:
        user_input = input("user_input: ")
        console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))
        response_text = send_message(user_input)
        console.print(Panel(response_text, style="bold green", box=SIMPLE))
        # sum(response_text)
        # speak(response_text)
        time.sleep(1)