import os
from pathlib import Path
from urllib.parse import urlparse

import yaml


class ConfigLoader:
    """Loads and validates environment-specific framework configuration."""

    def __init__(self, environment: str | None = None):
        self.environment = (
            environment or os.getenv("TEST_ENV") or "local"
        ).strip().lower()

        self.config = self._load_config()
        self._validate_config()

    def _load_config(self) -> dict:
        project_root = Path(__file__).resolve().parent.parent
        config_file = project_root / "config" / f"{self.environment}.yaml"

        if not config_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found for environment "
                f"'{self.environment}': {config_file}"
            )

        with config_file.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        if not isinstance(config, dict):
            raise ValueError(
                f"Invalid configuration in {config_file}: "
                "expected a YAML mapping."
            )

        # Apply environment-variable overrides.
        appium_server_url = os.getenv("APPIUM_SERVER_URL")
        if appium_server_url:
            config.setdefault("appium", {})["server_url"] = (
                appium_server_url
            )

        return config

    def _validate_config(self) -> None:
        """Validate required configuration fields and their values."""

        errors = []

        # Validate platform.
        platform = self.config.get("platform")
        if not isinstance(platform, str) or platform.lower() != "android":
            errors.append(
                "'platform' must be 'android'; "
                f"received {platform!r}."
            )

        # Validate Appium configuration.
        appium = self.config.get("appium")
        if not isinstance(appium, dict):
            errors.append("'appium' must be a YAML mapping.")
        else:
            server_url = appium.get("server_url")
            if not isinstance(server_url, str) or not server_url.strip():
                errors.append("'appium.server_url' is required.")
            elif not self._is_valid_url(server_url):
                errors.append(
                    "'appium.server_url' must be a valid HTTP or HTTPS URL."
                )

        # Validate Android configuration.
        android = self.config.get("android")
        if not isinstance(android, dict):
            errors.append("'android' must be a YAML mapping.")
        else:
            for key in (
                "platform_name",
                "automation_name",
                "device_name",
            ):
                if not isinstance(android.get(key), str) or not android[key].strip():
                    errors.append(f"'android.{key}' is required.")

        # Validate app configuration.
        app = self.config.get("app")
        if not isinstance(app, dict):
            errors.append("'app' must be a YAML mapping.")
        else:
            for key in ("package", "activity"):
                if not isinstance(app.get(key), str) or not app[key].strip():
                    errors.append(f"'app.{key}' is required.")

        # Validate API configuration.
        api = self.config.get("api")
        if not isinstance(api, dict):
            errors.append("'api' must be a YAML mapping.")
        else:
            base_url = api.get("base_url")
            if not isinstance(base_url, str) or not self._is_valid_url(base_url):
                errors.append(
                    "'api.base_url' must be a valid HTTP or HTTPS URL."
                )

            timeout = api.get("timeout")
            if (
                isinstance(timeout, bool)
                or not isinstance(timeout, (int, float))
                or timeout <= 0
            ):
                errors.append("'api.timeout' must be a positive number.")

        if errors:
            details = "\n".join(f"- {error}" for error in errors)
            raise ValueError(
                f"Invalid configuration for environment "
                f"'{self.environment}':\n{details}"
            )

    @staticmethod
    def _is_valid_url(value: str) -> bool:
        """Return True if the value is an HTTP(S) URL with a hostname."""
        try:
            parsed = urlparse(value)
            return (
                parsed.scheme in ("http", "https")
                and bool(parsed.netloc)
                and bool(parsed.hostname)
            )
        except ValueError:
            return False

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