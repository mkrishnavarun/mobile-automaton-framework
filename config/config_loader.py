import os
from pathlib import Path

import yaml


class ConfigLoader:
    """Loads environment-specific framework configuration."""

    def __init__(self, environment: str = "local"):
        self.environment = environment
        self.config = self._load_config()

    def _load_config(self) -> dict:
        project_root = Path(__file__).resolve().parent.parent
        config_file = project_root / "config" / f"{self.environment}.yaml"

        if not config_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_file}"
            )

        with config_file.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        appium_server_url = os.getenv("APPIUM_SERVER_URL")

        if appium_server_url:
            config["appium"]["server_url"] = appium_server_url

        return config

    @property
    def appium(self) -> dict:
        return self.config["appium"]

    @property
    def android(self) -> dict:
        return self.config["android"]

    @property
    def app(self) -> dict:
        return self.config["app"]

    @property
    def platform(self) -> str:
        return self.config["platform"]

    @property
    def api(self) -> dict:
        return self.config["api"]