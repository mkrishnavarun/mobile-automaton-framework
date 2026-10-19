from appium import webdriver

from config.config_loader import ConfigLoader
from core.capabilities_factory import CapabilitiesFactory
from utils.logger import Logger
from core.base_driver import BaseDriver


logger = Logger.get_logger(__name__)


class DriverManager(BaseDriver):
    """Responsible for creating and managing the Appium driver."""

    def __init__(self, config: ConfigLoader):
        self.config = config
        self.driver = None
        self.logger = logger

    def start_driver(self):
        options = CapabilitiesFactory.create_options(self.config)

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