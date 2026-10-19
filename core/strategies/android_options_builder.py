from appium.options.android import UiAutomator2Options


class AndroidOptionsBuilder:
    """Builds Appium options for an Android session."""

    def __init__(self):
        self._options = UiAutomator2Options()

    def with_platform(self, platform_name: str):
        self._options.platform_name = platform_name
        return self

    def with_automation(self, automation_name: str):
        self._options.automation_name = automation_name
        return self

    def with_device(self, device_name: str):
        self._options.device_name = device_name
        return self

    def with_app(self, package: str, activity: str):
        self._options.app_package = package
        self._options.app_activity = activity
        return self

    def build(self) -> UiAutomator2Options:
        """Return the configured Appium options."""
        return self._options