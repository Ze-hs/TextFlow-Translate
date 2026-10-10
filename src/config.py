
import json
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class TranslationConfig:
    source_language: str = "Japanese"
    target_language: str = "English"
    default_model: str = "openrouter/free"
    style: str = "natural"
    max_chunk_chars: int = 3000


@dataclass(frozen=True)
class APIConfig:
    timeout_seconds: int = 60
    max_retries: int = 3


@dataclass(frozen=True)
class OutputConfig:
    directory: str = "translations"
    format: str = "txt"


@dataclass(frozen=True)
class AppConfig:
    translation: TranslationConfig
    api: APIConfig
    output: OutputConfig


def load_config(path: str) -> AppConfig:
    path = Path(path)

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file not found: {path}"
        ) from None
    except json.JSONDecodeError as exception:
        raise ValueError(
            f"Invalid JSON in configuration file: {path}"
        ) from exception

    try:
        config = AppConfig(
            translation=TranslationConfig(**data.get("translation", {})),
            api=APIConfig(**data.get("api", {})),
            output=OutputConfig(**data.get("output", {})),
        )
    except TypeError as exception:
        raise ValueError(
            f"Invalid configuration fields: {exception}"
        ) from exception

    return config