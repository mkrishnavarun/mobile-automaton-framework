from config.config_loader import ConfigLoader
from core.strategies.base_capabilities import BaseCapabilities
from core.strategies.android_options_builder import AndroidOptionsBuilder


class AndroidCapabilities(BaseCapabilities):
    """Creates Appium options for Android devices."""

    def create_options(self, config: ConfigLoader):
        return (
            AndroidOptionsBuilder()
            .with_platform(config.android["platform_name"])
            .with_automation(config.android["automation_name"])
            .with_device(config.android["device_name"])
            .with_app(
                config.app["package"],
                config.app["activity"],
            )
            .build()
        )