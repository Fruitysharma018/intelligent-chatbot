import json
import os
from chatbot import Chat, register_call
import wikipedia
import pyjokes
import requests

# === Memory Handling ===
MEMORY_FILE = "memory.json"

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {}

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

# === Wikipedia search ===
@register_call("whoIs")
def who_is(session, query):
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception:
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query, sentences=2)
            except Exception:
                pass
    return "Sorry, I couldn't find anything about " + query

# === Remember & recall name ===
@register_call("rememberName")
def remember_name(session, name):
    memory["user_name"] = name
    save_memory()
    return f"Got it, I’ll remember your name {name}!"

@register_call("getName")
def get_name(session):
    return memory.get("user_name", "I don’t know your name yet.")

# === Tell jokes ===
@register_call("joke")
def tell_joke(session):
    return pyjokes.get_joke()

# === Weather ===
API_KEY = "YOUR_OPENWEATHER_API_KEY"  # Replace with your API key
@register_call("weather")
def get_weather(session, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"The weather in {city} is {desc} with {temp}°C."
    else:
        return "Sorry, I couldn't fetch the weather for that location."

# === Start chatbot ===
first_question = "Hi, I’m your smart bot! Ask me something..."
Chat("smartbot.template").converse(first_question)
