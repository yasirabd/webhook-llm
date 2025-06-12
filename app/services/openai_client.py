import os
import requests
from app.utils.config_loader import load_yaml_config


# Load model config
model_config = load_yaml_config("config/model.yaml")
BASE_MODEL = model_config["openai"]["base_model"]
FINETUNED_MODEL = model_config["openai"]["finetuned_model"]

def generate_chat_reply(messages, model=None, use_finetuned=True):
    selected_model = model or (FINETUNED_MODEL if use_finetuned else BASE_MODEL)
    
    body = {
        "model": selected_model,
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