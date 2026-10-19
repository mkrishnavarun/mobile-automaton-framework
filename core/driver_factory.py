from config.config_loader import ConfigLoader
from core.driver_manager import DriverManager


class DriverFactory:
    """Factory for creating platform-specific driver managers."""

    @staticmethod
    def create_driver_manager(config: ConfigLoader):
        platform = config.platform.lower()

        if platform == "android":
            return DriverManager(config)

        raise ValueError(
            f"Unsupported platform: {platform}"
        )