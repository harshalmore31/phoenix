import os
import time
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.box import SIMPLE
from langchain_community.chat_models import ChatLiteLLM
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
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

# Configure the Language Model (Gemini 2.0 Flash)
llm = ChatLiteLLM(
    model="gpt-4o",
    temperature=0.2,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
)

# Load system instruction from file
with open(r"src/phoenix.txt", "r", encoding="utf-8") as f:
    instruction = f.read()

# Define the corrected ReAct prompt template
react_prompt = PromptTemplate.from_template(
    instruction + """

Use the following tools to answer the user's question:

{tools}

Use the following format:

Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}

{agent_scratchpad}
"""
)

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

# Create the ReAct agent using the latest LangChain approach
# Create the ReAct agent with the prompt
agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)
# Set up the agent executor with memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Set up the agent executor with memory
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

# Main interaction loop
console.print(Panel("Do you want Voice OR Chat? Say 'Yes' for Voice!"))
option = input("Enter Y/N: ").strip().lower()

if option == "y":
    # Voice mode
    while True:
        if detect_wake_word(custom_ppn_path, access_key):
            user_input = real_time_transcription_with_threads()
            console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))
            ai_response = executor.invoke({"input": user_input})
            console.print(Panel(ai_response["output"], style="bold green", box=SIMPLE))
            speak(ai_response["output"])
            time.sleep(1)  # Delay to allow speech to complete
else:
    # Chat mode
    while True:
        user_input = input("user_input: ").strip()
        console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))
        ai_response = executor.invoke({"input": user_input})
        console.print(Panel(ai_response["output"], style="bold green", box=SIMPLE))
        time.sleep(1)  # Optional delay for consistency