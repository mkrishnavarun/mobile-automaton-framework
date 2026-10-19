from appium.options.android import UiAutomator2Options

from config.config_loader import ConfigLoader


class CapabilitiesFactory:
    """Creates platform-specific Appium options."""

    @staticmethod
    def create_options(config: ConfigLoader):
        platform = config.platform.lower()

        if platform == "android":
            options = UiAutomator2Options()

            options.platform_name = config.android["platform_name"]
            options.automation_name = config.android["automation_name"]
            options.device_name = config.android["device_name"]

            options.app_package = config.app["package"]
            options.app_activity = config.app["activity"]

            return options

        raise ValueError(
            f"Unsupported platform: {platform}"
        )