import os
import requests
import streamlit as st

def load_api_key():
    """
    Load API key safely:
    - Try Streamlit secrets
    - If not available (CI/testing), fall back to environment variable
    - If still missing, use TEST_KEY so tests do not crash
    """
    try:
        return st.secrets["WEATHER_API_KEY"]
    except Exception:
        return os.getenv("WEATHER_API_KEY", "TEST_KEY")

API_KEY = load_api_key()


def search_cities(query):
    url = f"https://api.weatherapi.com/v1/search.json?key={API_KEY}&q={query}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def get_current_weather(city):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        return {
            "city": data["location"]["name"],
            "region": data["location"]["region"],
            "temp_c": data["current"]["temp_c"],
            "feels_like_c": data["current"]["feelslike_c"],
            "humidity": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"],
            "condition": data["current"]["condition"]["text"],
            "icon": data["current"]["condition"]["icon"]
        }
    except Exception as e:
        return {"error": str(e)}
