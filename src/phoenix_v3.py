from langchain_community.chat_models import ChatLiteLLM
from langchain.tools import Tool
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.agents import initialize_agent, AgentType
from langchain_core.messages import SystemMessage
from langchain.memory import ConversationBufferMemory
from rich.console import Console
from rich.panel import Panel
from rich.box import SIMPLE
from speech_to_text.stt_groq_whisper import real_time_transcription_with_threads, speak
from speech_to_text.wake_word_detection import detect_wake_word
import time
from functions.weather import get_weather
from functions.lights import turn_on_lights
from functions.food import order_food
from functions.intersearch import search
from functions.my_calendar import cal
from functions.docs import write_in_document
from functions.cms import check_my_screen
from functions.code import write_code
from functions.krya import todo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define paths and keys for wake word detection
custom_ppn_path = r"assests\wake_word_detect\Phoenix_en_windows_v3_0_0.ppn"
access_key = os.getenv("picovoice_api_key")

# Initialize console for rich text output
console = Console()

# Configure the Language Model (Gemini 2.0 Flash)
llm = ChatLiteLLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.2,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
)

# Load system instruction from file
with open(r"src\phoenix.txt", "r", encoding="utf-8") as f:
    instruction = f.read()

# Set up conversation memory with system message
# system_message = SystemMessage(content=instruction)
# message_history = ChatMessageHistory(messages=[system_message])
# memory = ConversationBufferMemory(chat_memory=message_history)

# Define tools for the agent
weather_tool = Tool(
    name="get_weather",
    func=get_weather,
    description="Get the current weather for a given location. Takes a location string as input."
)

lights_tool = Tool(
    name="turn_on_lights",
    func=turn_on_lights,
    description="Turn on the lights. Takes no arguments."
)

food_tool = Tool(
    name="order_food",
    func=order_food,
    description="Order food based on the given description. Takes a string describing the order."
)

search_tool = Tool(
    name="search",
    func=search,
    description="Perform a web search with the given query. Takes a query string."
)

cal_tool = Tool(
    name="cal",
    func=cal,
    description="Manage calendar actions. Takes a descriptive string of the action."
)

document_tool = Tool(
    name="write_in_document",
    func=write_in_document,
    description="Write content to a document. Takes content and document name."
)

screen_tool = Tool(
    name="check_my_screen",
    func=check_my_screen,
    description="Check the status of the screen. Takes no arguments."
)

code_tool = Tool(
    name="write_code",
    func=write_code,
    description="Generate code based on the specification. Takes a specification string."
)

todo_tool = Tool(
    name="todo",
    func=todo,
    description="Manage to-do lists. Takes a descriptive string of the action."
)

# List of all tools for the agent
tools = [weather_tool, lights_tool, food_tool, search_tool, cal_tool, document_tool, screen_tool, code_tool, todo_tool]

# Initialize the agent with tools, LLM, and memory
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    # memory=memory,
    verbose=True
)

# Main interaction loop
console.print(Panel("Do you want Voice OR Chat, Say Yes for Voice!"))
option = input("Enter Y/N: ")

if option == "Y" or option == "y":
    # Voice mode
    while True:
        if detect_wake_word(custom_ppn_path, access_key):
            user_input = real_time_transcription_with_threads()
            console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))
            ai_response = agent.invoke(user_input)
            console.print(Panel(ai_response, style="bold green", box=SIMPLE))
            speak(ai_response)
            time.sleep(1)  # Delay to allow speech to complete
else:
    # Chat mode
    while True:
        user_input = input("user_input: ")
        console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))
        ai_response = agent.invoke(user_input)
        console.print(Panel(ai_response, style="bold green", box=SIMPLE))
        time.sleep(1)  # Optional delay for consistency