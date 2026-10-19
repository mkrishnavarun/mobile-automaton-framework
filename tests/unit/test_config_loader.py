from pathlib import Path
from unittest.mock import patch

import pytest

from config.config_loader import ConfigLoader


def test_api_configuration_loads():
    config = ConfigLoader("local")

    assert config.api["base_url"] == "https://jsonplaceholder.typicode.com"
    assert config.api["timeout"] == 10


def test_existing_mobile_configuration_loads():
    config = ConfigLoader("local")

    assert config.appium["server_url"] == "http://127.0.0.1:4723"
    assert config.android["platform_name"] == "Android"
    assert config.app["package"] == "com.android.settings"


def test_missing_configuration_raises_error():
    with pytest.raises(FileNotFoundError):
        ConfigLoader("nonexistent_environment")


def test_appium_server_url_environment_override():
    with patch.dict(
        "os.environ",
        {"APPIUM_SERVER_URL": "http://localhost:4723"},
    ):
        config = ConfigLoader("local")

    assert config.appium["server_url"] == "http://localhost:4723"