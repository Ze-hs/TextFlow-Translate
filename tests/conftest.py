import pytest

from src.config import AppConfig, TranslationConfig, APIConfig, OutputConfig
from src.repository import init_database


@pytest.fixture
def test_db(tmp_path):
    database_path = str(tmp_path / "test.db")
    init_database(database_path)
    return database_path

@pytest.fixture
def test_config():
    return AppConfig(
        translation=TranslationConfig(),
        api=APIConfig(),
        output=OutputConfig()
    )
