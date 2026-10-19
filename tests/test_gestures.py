from pages.settings_page import SettingsPage
from utils.gesture_utils import GestureUtils
import pytest

@pytest.mark.mobile
def test_scroll_down_and_up(driver):
    gestures = GestureUtils(driver)

    initial_size = driver.get_window_size()

    gestures.scroll_down()
    gestures.scroll_up()

    assert driver.get_window_size() == initial_size

@pytest.mark.mobile
def test_long_press_element(driver):
    settings_page = SettingsPage(driver)
    gestures = GestureUtils(driver)

    element = settings_page.find_element(
        settings_page.NETWORK_OPTION
    )

    gestures.long_press_element(element, duration=1000)


    # Verify the Android app session is still active.
    assert driver.session_id is not None
    assert driver.current_package == "com.android.settings"

@pytest.mark.mobile
def test_tap_gesture(driver):
    settings_page = SettingsPage(driver)
    gestures = GestureUtils(driver)

    element = settings_page.find_element(settings_page.NETWORK_OPTION)
    rect = element.rect

    x = rect["x"] + rect["width"] // 2
    y = rect["y"] + rect["height"] // 2

    gestures.tap(x, y)

    assert settings_page.is_internet_screen_displayed()

@pytest.mark.mobile
def test_double_tap_gesture(driver):
    gestures = GestureUtils(driver)

    size = driver.get_window_size()
    x = size["width"] // 2
    y = size["height"] // 2

@pytest.mark.mobile
def test_tap_element(driver):
    settings_page = SettingsPage(driver)
    gestures = GestureUtils(driver)

    element = settings_page.find_element(settings_page.NETWORK_OPTION)
    gestures.tap_element(element)

    assert settings_page.is_internet_screen_displayed()

@pytest.mark.mobile
def test_double_tap_element(driver):
    settings_page = SettingsPage(driver)
    gestures = GestureUtils(driver)

    element = settings_page.find_element(settings_page.NETWORK_OPTION)
    gestures.double_tap_element(element)

    assert driver.session_id is not None