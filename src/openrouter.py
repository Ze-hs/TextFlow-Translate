import os

import requests
import json
from dotenv import load_dotenv

load_dotenv()

def request_chat(prompt: str):
    OPEN_ROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

    if not OPEN_ROUTER_KEY:
        raise ValueError("Missing OPEN_ROUTER_KEY")

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
        "Authorization": f"Bearer {OPEN_ROUTER_KEY}",
        },
        data=json.dumps({
        "model": "openrouter/free",
        "messages": [
          {
            "role": "user",
            "content": f"{prompt}"
          },
        ],
        "reasoning": {
              "effort": "low",
              "exclude": True
          },
        "timeout": 60
      }),
    )

    response.raise_for_status()
    return response.json()
