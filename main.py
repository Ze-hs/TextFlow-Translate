import os

import requests
import json
from dotenv import load_dotenv

load_dotenv()

OPEN_ROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

def main():
    print("Hello World")


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
        "content": "What is the meaning of life?"
      },
    ],
      "reasoning": {
          "effort": "low",
          "exclude": True
      }
  })
)

print(response.ok)
print(json.dumps(response.json(), indent=4))
print()
