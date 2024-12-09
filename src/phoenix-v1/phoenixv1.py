import google.generativeai as genai
import requests, json
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.box import Box, DOUBLE, ROUNDED, HEAVY, SIMPLE
from speechcopy import transcribe_audio, speak
# from realtime import real_time_transcription_with_silence_detection
# from realtimecopy import real_time_transcription_with_threads
from sttgq import real_time_transcription_with_threads
from wake_word_detection import detect_wake_word
import time
import webbrowser
from dotenv import load_dotenv
import os

# custom_ppn_path = r"Versions\Phoenix\phoenix-v1\Phoenix_en_windows_v3_0_0.ppn"
# access_key = "49RT4geBg0wydV8MBk9dl1Iwnl1IJJBxzpuSFA+MRCqulS03cyKDWQ=="

console = Console()

def get_weather(city_name: str) -> str:
    """Gets the weather for a given city with improved error handling."""
    api_key = os.getenv("weather_api_key")  # **REPLACE!**
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city_name}&units=metric"

    try:
        response = requests.get(complete_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        x = response.json()
        # print(f"API Response: {x}") # Print the JSON response for debugging

        if x["cod"] != "404":  # Check for city not found
            main = x["main"]
            temp = main["temp"]
            feels_like = main["feels_like"] # Added feels_like temperature
            pressure = main["pressure"]
            humidity = main["humidity"]
            weather_desc = x["weather"][0]["description"]

            return (f"Temperature: {temp}°C\n"
                    f"Feels like: {feels_like}°C\n" # Output feels_like temperature
                    f"Atmospheric Pressure: {pressure} hPa\n"
                    f"Humidity: {humidity}%\n"
                    f"Description: {weather_desc}")
        elif x["cod"] == "404":
            return "City Not Found"
        else:
            return f"An unexpected error occurred: {x.get('message', 'Unknown error')}"

    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"
    
def turn_on_lights():
    console.print("💡Lights are turned on !",style="bold yellow")

# Here comes now my Chat-model can interact with various API and I can do anything using function call, like we can fucking tune a model if we make a functuion of it 

def order_food(food : str,city :str) -> str:
    print(f"Lets order {food}:")
    select = int(input("Select opt. number from Below \n 1. Zomato \n 2. Swiggy \n Opt. No : "))
    if select == 1:
        print(f"Ordering {food} from zomato")
        print(f"Click on the link below \n https://www.zomato.com/{city}/delivery/dish-{food} ")
        webbrowser.open("https://www.zomato.com/{city}/delivery/dish-{food}")
    
    else:
        print(f"Ordering {food} from swiggy")   


def internet_search(search :str) -> str:
    print("Browsing through Google Search !")
    api_key = os.getenv("google_search_api_key")
    complete_url = "https://www.googleapis.com/customsearch/v1?key="+api_key+f"&cx=017576662512468239146:omuauf_lfve&q={search}"
    response = requests.get(complete_url)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    x = response.json()
    print(x)

def knowledge_retreival():
    print("We are gonna Implement RAG here !")

import requests

def cal(eventname: str, date: str, start_time: str = None, end_time: str = None, description: str = None, location: str = None) -> str:
    """
    Sends an event creation request to a Zapier webhook to add an event to Google Calendar.
    
    Args:
        eventname (str): Name of the event (Required).
        date (str): Event date in YYYY-MM-DD format (Required).
        start_time (str): Event start time in HH:MM 24-hour format (Optional).
        end_time (str): Event end time in HH:MM 24-hour format (Optional).
        description (str): Description of the event (Required).
        location (str): Event location (Optional).
    
    Returns:
        str: A message indicating success or failure of the request.
    """

    # Check for mandatory fields
    if not eventname or not date or not description:
        return "Error: 'eventname', 'date', and 'description' are required fields."

    print("Adding the event to Google Calendar:")
    choice = input("Confirm? Enter Y/N: ").strip().lower()
    
    if choice == "y":
        # Webhook URL from Zapier
        webhook_url = "https://hooks.zapier.com/hooks/catch/10321312/2rx22ly/"  # Replace with your actual Zapier webhook URL
        
        # Build the event data payload
        event_data = {
            "summary": eventname,
            "start": {
                "dateTime": f"{date}T{start_time}:00" if start_time else None,  # Include only if start_time is provided
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": f"{date}T{end_time}:00" if end_time else None,  # Include only if end_time is provided
                "timeZone": "UTC"
            },
            "description": description,
            "location": location or "Not specified"
        }
        
        # Remove keys with None values to ensure a clean payload
        event_data = {k: v for k, v in event_data.items() if v is not None}
        if "start" in event_data:
            event_data["start"] = {k: v for k, v in event_data["start"].items() if v is not None}
        if "end" in event_data:
            event_data["end"] = {k: v for k, v in event_data["end"].items() if v is not None}

        try:
            # Send POST request to the webhook URL
            response = requests.post(webhook_url, json=event_data)

            if response.status_code == 200:
                return f"Event '{eventname}' added successfully to Google Calendar!"
            else:
                return f"Failed to add event. Status code: {response.status_code}, Response: {response.text}"
        except Exception as e:
            return f"An error occurred: {e}"
    else:
        return "Event creation canceled by user."



genai.configure(api_key=os.getenv("gemini_api1_key")) # Replace with your Google Generative AI key

generation_config = {  # You can adjust these parameters
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

# with open("phoenix.txt", "r", encoding="utf-8") as f:
#     instruction = f.read()

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # system_instruction=instruction,
    tools=[get_weather, turn_on_lights, order_food, internet_search, cal]
)


chat = model.start_chat(history=[],enable_automatic_function_calling=True)
speak("Hey Boss, How may I help you !")

while True:
    user_input =  real_time_transcription_with_threads()
    console.print(Panel(f"User said: {user_input}", style="bold blue", box=SIMPLE))
    response = chat.send_message(user_input)
    console.print(Panel(response.text, style="bold green", box=SIMPLE))
    # speak(response.text)
    time.sleep(9)