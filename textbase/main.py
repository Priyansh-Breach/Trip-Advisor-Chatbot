import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List
import requests

# Load environment variables from the .env file
# load_dotenv()

# Get the API keys from the environment variables
weather_api_key = os.getenv("WEATHER_API_KEY")

# Load your OpenAI API key from the environment variable:
models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with a trip advisor AI. Feel free to ask any questions or discuss your travel plans. The AI will respond in a natural, conversational manner. Let's plan your perfect trip!
"""

MAX_CONTEXT_LENGTH = 4096  # Max context length of the GPT-3.5 Turbo model

@textbase.chatbot("trip_advisor_bot")
def on_message(message_history: List[Message], state: dict = None):
    """
    Main chatbot logic.

    Args:
        message_history (List[Message]): List of user messages
        state (dict, optional): A dictionary to store any stateful information. Defaults to None.

    Returns:
        tuple: A tuple containing the bot's response (str) and updated state (dict).
    """
    if state is None or "key_points" not in state:
        state = {"key_points": []}

    user_input = message_history[-1].content.lower()

    # Check if the user wants to start planning a new trip
    if "start" in user_input and "trip" in user_input:
        state["trip_preferences"] = {}  # Reset previous trip preferences
        state["key_points"] = []  # Reset key points for new conversation

    # Extract user preferences for the current trip
    preferences_mapping = {
        "destination": "destination",
        "budget": "budget",
        "duration": "duration",
    }

    for key, value in preferences_mapping.items():
        if value in user_input:
            state["trip_preferences"][key] = user_input.replace(value, "").strip()

    # Store key points of the conversation for context length management
    state["key_points"].append(user_input)

    # Check if the user wants weather forecast for a specific city
    if user_input.startswith("weather "):
        city_name = user_input[len("weather "):].strip()
        weather_data = get_weather_data(city_name)
        if weather_data:
            forecast = format_weather_forecast(weather_data)
            bot_response = f"The weather forecast for {city_name} for the next 10 days:\n{forecast}"
        else:
            bot_response = f"Failed to retrieve weather data for {city_name}."
        return bot_response, state

    # Keep the context length within the model's limit
    truncated_message_history = truncate_context_length(message_history, state["key_points"])

    # Generate GPT-3.5 Turbo response
    bot_response = models.OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=truncated_message_history,
        model="gpt-3.5-turbo",
    )

    return bot_response, state

def format_weather_forecast(weather_data):
    """
    Format the weather forecast data into a readable string.

    Args:
        weather_data (dict): Weather data for a specific city.

    Returns:
        str: Formatted weather forecast string.
    """
    forecast = ""
    for day in weather_data["forecast"]["forecastday"]:
        date = day["date"]
        condition = day["day"]["condition"]["text"]
        forecast += f"{date}: Condition: {condition}\n\n"
    return forecast

def truncate_context_length(message_history: List[Message], key_points: List[str]) -> List[Message]:
    """
    Truncate the message history to keep the context length within the model's limit.

    Args:
        message_history (List[Message]): List of user messages.
        key_points (List[str]): List of key points in the conversation.

    Returns:
        List[Message]: Truncated message history.
    """
    context_length = sum(len(msg.content) for msg in message_history) + len(key_points)
    while context_length > MAX_CONTEXT_LENGTH:
        context_length -= len(message_history[0].content)
        message_history.pop(0)
    return message_history

def get_weather_data(city, days=10):
    """
    Get weather data for a specific city from the Weather API.

    Args:
        city (str): Name of the city for weather forecast.
        days (int, optional): Number of days for the forecast. Defaults to 10.

    Returns:
        dict: Weather data for the specified city.
    """
    api_key = weather_api_key
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": api_key,
        "q": city,
        "days": days,
        "aqi": "no",
        "alerts": "no"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Check for any request errors
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return None

def get_user_input():
    state = None  # Initialize state
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        else:
            bot_response, state = on_message(message_history=[Message(user_input)], state=state)
            print("Bot:", bot_response)

if __name__ == "__main__":
    get_user_input()
