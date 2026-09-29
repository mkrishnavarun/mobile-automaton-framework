from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from utils.logger import Logger
from utils.screenshot import ScreenshotUtil
from core.exceptions import ElementInteractionError


class BasePage:
    """Base class containing common mobile page actions."""

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.logger = Logger.get_logger(self.__class__.__name__)

    def find_element(self, locator):
        self.logger.info("Finding element: %s", locator)

        try:
            element = self.wait.until(
                lambda driver: driver.find_element(*locator)
            )

            self.logger.info("Element found: %s", locator)

            return element

        except Exception as exc:
            self.logger.error(
                "Failed to find element: %s",
                locator,
                exc_info=True,
            )

            try:
                ScreenshotUtil.capture(
                    self.driver,
                    "element_not_found",
                )
            except Exception:
                self.logger.exception(
                    "Failed to capture error screenshot"
                )

            raise ElementInteractionError(
                f"Unable to find element: {locator}"
            ) from exc



    def tap(self, locator):
        self.logger.info("Tapping element: %s", locator)
        element = self.find_element(locator)
        element.click()

    def enter_text(self, locator, text: str):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator) -> str:
        return self.find_element(locator).text

    def is_displayed(self, locator) -> bool:
        return self.find_element(locator).is_displayed()