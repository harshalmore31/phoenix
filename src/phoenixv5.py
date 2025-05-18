import os
import time
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.box import SIMPLE
from langchain_community.chat_models import ChatLiteLLM
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from speech_to_text.stt_groq_whisper import real_time_transcription_with_threads, speak
from speech_to_text.wake_word_detection import detect_wake_word
from functions.weather import get_weather
from functions.lights import turn_on_lights
from functions.food import order_food
from functions.intersearch import search
from functions.my_calendar import cal
from functions.docs import write_in_document
from functions.cms import check_my_screen
from functions.code import write_code
from functions.krya import todo

# Load environment variables
load_dotenv()

# Define paths and keys for wake word detection
custom_ppn_path = r"assests\wake_word_detect\Phoenix_en_windows_v3_0_0.ppn"
access_key = os.getenv("PICOVOICE_API_KEY")

# Initialize console for rich text output
console = Console()

# Configure the Language Model (using GPT-4o)
llm = ChatLiteLLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.2,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
)

# Load system instruction from file
with open(r"src/phoenix.txt", "r", encoding="utf-8") as f:
    instruction = f.read()

# Define tools for the agent
tools = [
    Tool(name="get_weather", func=get_weather, description="Get the current weather for a given location. Takes a location string as input."),
    Tool(name="turn_on_lights", func=turn_on_lights, description="Turn on the lights. Takes no arguments."),
    Tool(name="order_food", func=order_food, description="Order food based on the given description. Takes a string describing the order."),
    Tool(name="search", func=search, description="Perform a web search with the given query. Takes a query string."),
    Tool(name="cal", func=cal, description="Manage calendar actions. Takes a descriptive string of the action."),
    Tool(name="write_in_document", func=write_in_document, description="Write content to a document. Takes content and document name."),
    Tool(name="check_my_screen", func=check_my_screen, description="Check the status of the screen. Takes no arguments."),
    Tool(name="write_code", func=write_code, description="Generate code based on the specification. Takes a specification string."),
    Tool(name="todo", func=todo, description="Manage to-do lists. Takes a descriptive string of the action."),
]

# Set up memory for conversation history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize a simple agent - using a basic agent type instead of React
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

# Set the agent's system message using instructions
agent.agent.llm_chain.prompt.messages[0].prompt.template = instruction

# Main interaction loop
console.print(Panel("Do you want Voice OR Chat? Say 'Yes' for Voice!"))
option = input("Enter Y/N: ").strip().lower()

if option == "y":
    # Voice mode
    while True:
        if detect_wake_word(custom_ppn_path, access_key):
            user_input = real_time_transcription_with_threads()
            console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))
            ai_response = agent.invoke(user_input)
            console.print(Panel(ai_response.content, style="bold green", box=SIMPLE))
            speak(ai_response.content)
            time.sleep(1)  # Delay to allow speech to complete
else:
    # Chat mode
    while True:
        user_input = input("user_input: ").strip()
        console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))
        ai_response = agent.invoke(user_input)
        console.print(Panel(ai_response.content, style="bold green", box=SIMPLE))
        time.sleep(1)  # Optional delay for consistency