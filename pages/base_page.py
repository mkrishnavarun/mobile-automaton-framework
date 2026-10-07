from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)

from utils.logger import Logger
from utils.screenshot import ScreenshotUtil
from core.exceptions import ElementInteractionError
from utils.wait_utils import WaitUtils
from utils.retry_utils import retry_on_exception


class BasePage:
    """Base class containing common mobile page actions."""

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait_utils = WaitUtils(driver, timeout)
        self.logger = Logger.get_logger(self.__class__.__name__)

    def find_element(self, locator):
        self.logger.info("Finding element: %s", locator)

        try:
            element = self.wait_utils.wait_for_present(locator)

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

    @retry_on_exception(retries=2, delay=1)
    def tap(self, locator):
        self.logger.info("Tapping element: %s", locator)

        try:
            element = self.find_element(locator)
            element.click()

        except (
                ElementClickInterceptedException,
                ElementNotInteractableException,
                StaleElementReferenceException,
        ):
            raise

        except Exception as exc:
            self.logger.error(
                "Failed to tap element: %s",
                locator,
                exc_info=True,
            )

            try:
                ScreenshotUtil.capture(
                    self.driver,
                    "tap_failed",
                )
            except Exception:
                self.logger.exception(
                    "Failed to capture tap failure screenshot"
                )

            raise ElementInteractionError(
                f"Unable to tap element: {locator}"
            ) from exc

    def enter_text(self, locator, text: str):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator) -> str:
        return self.find_element(locator).text

    def is_displayed(self, locator) -> bool:
        return self.find_element(locator).is_displayed()