import os
import requests

def generate_chat_reply(messages, model=None):
    body = {
        "model": model or "gpt-4o-mini-2024-07-18",
        "messages": messages,
        "temperature": 0.7
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }

    res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
    res.raise_for_status()
    return res.json()