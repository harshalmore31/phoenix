import os
from dotenv import load_dotenv
from litellm import completion

# Load environment variables from .env file
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

# Define the get_weather function
def get_weather(city_name: str) -> str:
    """Gets the weather for a given city with improved error handling."""
    api_key = os.getenv("weather_api_key")
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city_name}&units=metric"

    try:
        response = requests.get(complete_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        x = response.json()

        if x["cod"] != "404":
            main = x["main"]
            temp = main["temp"]
            feels_like = main["feels_like"]  # Added feels_like temperature
            pressure = main["pressure"]
            humidity = main["humidity"]
            weather_desc = x["weather"][0]["description"]

            return (f"Temperature: {temp}°C\n"
                    f"Feels like: {feels_like}°C\n"
                    f"Atmospheric Pressure: {pressure} hPa\n"
                    f"Humidity: {humidity}%\n"
                    f"Description: {weather_desc}")
        elif x["cod"] == "404":
            return "City Not Found"
        else:
            return f"An unexpected error occurred: {x.get('message', 'Unknown error')}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching the weather data: {e}"

# Define tools for function calling
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Gets the weather for a given city with improved error handling.",
            "strict": True,
            "parameters": {
                "type": "object",
                "required": ["city_name"],
                "properties": {
                    "city_name": {
                        "type": "string",
                        "description": "Name of the city for which to retrieve the weather"
                    }
                },
                "additionalProperties": False
            }
        }
    }
]

# Example usage of the function
if __name__ == "__main__":
    try:
        completion_result = completion(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "What is the weather like in Paris today?"}],
            tools=tools
        )

        tool_calls = completion_result.choices[0].message.tool_calls
        print(f"Tool Calls: {tool_calls}")

        # Template for adding more functions
        # 1. Define the function logic (e.g., def get_time_zone(...)).
        # 2. Add function metadata to the tools list.
        # 3. Test the function with appropriate inputs.

    except Exception as e:
        print(f"An unexpected error occurred: {e}")