from appium import webdriver
from appium.options.android import UiAutomator2Options

from config.config_loader import ConfigLoader
from utils.logger import Logger


logger = Logger.get_logger(__name__)

class DriverManager:
    """
    Responsible for creating and managing the Appium driver.
    """

    def __init__(self, config: ConfigLoader):
        self.config = config
        self.driver = None
        self.logger=logger

    def start_driver(self):
        options = UiAutomator2Options()

        options.platform_name = self.config.android["platform_name"]
        options.automation_name = self.config.android["automation_name"]
        options.device_name = self.config.android["device_name"]

        options.app_package = self.config.app["package"]
        options.app_activity = self.config.app["activity"]

        self.logger.info(
            "Launching application: %s",
            self.config.app["package"],
        )

        self.driver = webdriver.Remote(
            command_executor=self.config.appium["server_url"],
            options=options,
        )

        self.logger.info("Appium driver started successfully")
        return self.driver

    def stop_driver(self):
        if self.driver:
            self.logger.info("Stopping Appium driver")
            self.driver.quit()
            self.driver = None
            self.logger.info("Appium driver stopped")