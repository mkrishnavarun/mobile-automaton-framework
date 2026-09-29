from pathlib import Path

from appium.webdriver.webdriver import WebDriver

from utils.logger import Logger


class ScreenshotUtil:
    """Utility for capturing and storing mobile screenshots."""

    logger = Logger.get_logger(__name__)

    @staticmethod
    def capture(driver: WebDriver, name: str) -> str:
        project_root = Path(__file__).resolve().parent.parent
        screenshot_directory = project_root / "screenshots"

        screenshot_directory.mkdir(exist_ok=True)

        screenshot_path = screenshot_directory / f"{name}.png"

        driver.save_screenshot(str(screenshot_path))

        ScreenshotUtil.logger.info(
            "Screenshot captured: %s",
            screenshot_path,
        )

        return str(screenshot_path)