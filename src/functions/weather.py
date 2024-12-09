import os
from dotenv import load_dotenv
import requests

load_dotenv()

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
        return f"An error occurred while fetching the weather data: {e}"