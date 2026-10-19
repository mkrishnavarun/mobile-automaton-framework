from config.config_loader import ConfigLoader
from core.strategies.android_capabilities import AndroidCapabilities


class CapabilitiesFactory:
    """Creates platform-specific Appium options."""

    @staticmethod
    def create_options(config: ConfigLoader):
        platform = config.platform.lower()

        if platform == "android":
            strategy = AndroidCapabilities()
            return strategy.create_options(config)

        raise ValueError(
            f"Unsupported platform: {platform}"
        )