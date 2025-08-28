import gradio as gr
from chatbot import Chat, register_call
import wikipedia
import pyjokes
import requests
import json
import os

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

# === Wikipedia ===
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

# === Memory (Name) ===
@register_call("rememberName")
def remember_name(session, name):
    memory["user_name"] = name
    save_memory()
    return f"Got it, I’ll remember your name {name}!"

@register_call("getName")
def get_name(session):
    return memory.get("user_name", "I don’t know your name yet.")

# === Jokes ===
@register_call("joke")
def tell_joke(session):
    return pyjokes.get_joke()

# === Weather ===
API_KEY = "YOUR_OPENWEATHER_API_KEY"  # Replace with your free API key
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

# === Chatbot Core ===
chat = Chat("smartbot.template")

def chatbot_fn(message, history):
    reply = chat.respond(message)
    history.append((message, reply))  # add to conversation
    return history, history

with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Intelligent Chatbot\nAsk me about Wikipedia, jokes, memory, or weather!")

    chatbot_ui = gr.Chatbot()
    msg = gr.Textbox(placeholder="Type your message here...")
    clear = gr.Button("Clear Chat")

    def respond(message, history):
        reply = chat.respond(message)
        history.append((message, reply))
        return history, ""

    msg.submit(respond, [msg, chatbot_ui], [chatbot_ui, msg])
    clear.click(lambda: [], None, chatbot_ui)

if __name__ == "__main__":
    demo.launch()
