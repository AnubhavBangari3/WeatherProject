# app/weather.py

import re
import requests
from app.config import WEATHER_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"



def extract_city(text: str) -> str:
    """
    Extract city name from natural language queries.
    Examples:
        "How is weather in Delhi?" -> "Delhi"
        "What's the weather like today in London?" -> "London"
        "Weather Tokyo" -> "Tokyo"
    """

    # Try extracting capitalized words (Delhi, London, Mumbai, Tokyo)
    caps = re.findall(r"[A-Z][a-zA-Z]+", text)
    if caps:
        return caps[-1]  # Last capitalized word

    tokens = text.strip().split()
    return tokens[-1]


def get_weather(user_query: str) -> dict:


    if not WEATHER_KEY:
        raise ValueError("WEATHER_KEY (OpenWeather API key) not set")

    # Extract the city from user query
    city = extract_city(user_query)

    params = {
        "q": city,
        "appid": WEATHER_KEY,
        "units": "metric",
    }

    resp = requests.get(BASE_URL, params=params, timeout=10)

    # If wrong city or invalid → throw readable error
    if resp.status_code == 404:
        raise ValueError(f"City '{city}' not found. Please try another city.")

    resp.raise_for_status()

    data = resp.json()

    main = data.get("main", {})
    weather_desc = data.get("weather", [{}])[0].get("description", "")

    return {
        "city": data.get("name", city),
        "temperature": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "humidity": main.get("humidity"),
        "description": weather_desc,
    }



def format_weather_for_llm(weather: dict) -> str:
    """
    Convert weather dict into a nice natural-language summary.
    """
    return (
        f"Weather in {weather['city']}:\n"
        f"- Temperature: {weather['temperature']}°C\n"
        f"- Feels like: {weather['feels_like']}°C\n"
        f"- Humidity: {weather['humidity']}%\n"
        f"- Description: {weather['description']}"
    )
