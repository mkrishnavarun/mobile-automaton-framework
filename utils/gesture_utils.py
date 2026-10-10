from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from utils.logger import Logger


class GestureUtils:
    """Reusable mobile gesture operations."""

    logger = Logger.get_logger(__name__)

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def swipe(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration: int = 500,
    ) -> None:
        """Swipe from one screen coordinate to another."""

        self.logger.info(
            "Swiping from (%s, %s) to (%s, %s)",
            start_x,
            start_y,
            end_x,
            end_y,
        )

        touch = PointerInput(
            interaction.POINTER_TOUCH,
            "touch",
        )

        actions = ActionBuilder(
            self.driver,
            mouse=touch,
        )

        pointer = actions.pointer_action

        pointer.move_to_location(start_x, start_y)
        pointer.pointer_down()
        pointer.pause(0.1)

        # Configure the duration on the pointer input,
        # rather than passing it to move_to_location().
        touch.create_pause(0)
        pointer.move_to_location(end_x, end_y)

        pointer.release()
        actions.perform()

    def scroll_down(self) -> None:
        """Scroll toward the bottom of the screen."""

        size = self.driver.get_window_size()

        center_x = size["width"] // 2
        start_y = int(size["height"] * 0.75)
        end_y = int(size["height"] * 0.25)

        self.swipe(center_x, start_y, center_x, end_y)

    def scroll_up(self) -> None:
        """Scroll toward the top of the screen."""

        size = self.driver.get_window_size()

        center_x = size["width"] // 2
        start_y = int(size["height"] * 0.25)
        end_y = int(size["height"] * 0.75)

        self.swipe(center_x, start_y, center_x, end_y)


    def long_press(
        self,
        x: int,
        y: int,
        duration: int = 1000,
    ) -> None:
        """Press and hold at screen coordinates for a specified duration."""

        self.logger.info(
            "Long pressing at (%s, %s) for %s ms",
            x,
            y,
            duration,
        )

        touch = PointerInput(
            interaction.POINTER_TOUCH,
            "touch",
        )

        actions = ActionBuilder(
            self.driver,
            mouse=touch,
        )

        pointer = actions.pointer_action

        pointer.move_to_location(x, y)
        pointer.pointer_down()
        pointer.pause(duration / 1000)
        pointer.release()

        actions.perform()

    def long_press_element(
        self,
        element,
        duration: int = 1000,
    ) -> None:
        """Long-press the center of a web element."""

        rect = element.rect

        x = rect["x"] + rect["width"] // 2
        y = rect["y"] + rect["height"] // 2

        self.logger.info(
            "Long pressing element at (%s, %s) for %s ms",
            x,
            y,
            duration,
        )

        self.long_press(x, y, duration)

    def tap(self, x: int, y: int) -> None:
        """Tap at the specified screen coordinates."""
        self.logger.info("Tapping at (%s, %s)", x, y)

        touch = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionBuilder(self.driver, mouse=touch)
        pointer = actions.pointer_action

        pointer.move_to_location(x, y)
        pointer.pointer_down()
        pointer.pointer_up()

        actions.perform()

    def double_tap(self, x: int, y: int) -> None:
        """Double-tap at the specified screen coordinates."""
        self.logger.info("Double-tapping at (%s, %s)", x, y)

        touch = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionBuilder(self.driver, mouse=touch)
        pointer = actions.pointer_action

        pointer.move_to_location(x, y)
        pointer.pointer_down()
        pointer.pointer_up()
        pointer.pause(0.1)
        pointer.pointer_down()
        pointer.pointer_up()

        actions.perform()


    def tap_element(self, element) -> None:
        """Tap the center of an element."""
        rect = element.rect

        x = rect["x"] + rect["width"] // 2
        y = rect["y"] + rect["height"] // 2

        self.logger.info("Tapping element at (%s, %s)", x, y)
        self.tap(x, y)

    def double_tap_element(self, element) -> None:
        """Double-tap the center of an element."""
        rect = element.rect

        x = rect["x"] + rect["width"] // 2
        y = rect["y"] + rect["height"] // 2

        self.logger.info("Double-tapping element at (%s, %s)", x, y)
        self.double_tap(x, y)