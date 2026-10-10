import logging
import os

import requests

from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from src.config import APIConfig

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logging.getLogger("urllib3").setLevel(logging.DEBUG)


def create_session(api_config: APIConfig) -> requests.Session:
    retries = Retry(
        total=api_config.max_retries,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods={"POST"},
        respect_retry_after_header=True,
    )

    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retries))

    return session

def request_chat(prompt: str, api_config: APIConfig):
    OPEN_ROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

    if not OPEN_ROUTER_KEY:
        raise ValueError("Missing OPEN_ROUTER_KEY")
    session = create_session(api_config)

    response = session.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPEN_ROUTER_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "reasoning": {
                "effort": "low",
                "exclude": True,
            },
        },
        timeout=api_config.timeout_seconds,
    )

    response.raise_for_status()
    return response.json()