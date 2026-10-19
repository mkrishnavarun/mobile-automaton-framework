from datetime import datetime
from pathlib import Path

from appium.webdriver.webdriver import WebDriver

from utils.logger import Logger
import os


class ScreenshotUtil:
    """Utility for capturing and storing mobile screenshots."""

    logger = Logger.get_logger(__name__)

    @staticmethod
    def capture(driver: WebDriver, name: str) -> str:
        project_root = Path(__file__).resolve().parent.parent
        screenshot_directory = project_root / "screenshots"

        screenshot_directory.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        screenshot_path = (
            screenshot_directory / f"{name}_{timestamp}.png"
        )

        driver.save_screenshot(str(screenshot_path))

        ScreenshotUtil.logger.info(
            "Screenshot captured: %s",
            screenshot_path,
        )

        return str(screenshot_path)

