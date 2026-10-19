from unittest.mock import MagicMock, patch

import pytest

from core.exceptions import ElementInteractionError
from pages.base_page import BasePage


@pytest.fixture
def base_page():
    driver = MagicMock()
    page = BasePage(driver)
    return page


def test_find_element_returns_element(base_page):
    expected_element = MagicMock()

    with patch.object(
        base_page.wait_utils,
        "wait_for_present",
        return_value=expected_element,
    ):
        element = base_page.find_element(("id", "test_element"))

    assert element is expected_element


def test_find_element_raises_custom_exception(base_page):
    with patch.object(
        base_page.wait_utils,
        "wait_for_present",
        side_effect=Exception("Element not found"),
    ), patch(
        "pages.base_page.ScreenshotUtil.capture"
    ):
        with pytest.raises(ElementInteractionError):
            base_page.find_element(("id", "missing_element"))


def test_tap_clicks_element(base_page):
    element = MagicMock()

    with patch.object(
        base_page,
        "find_element",
        return_value=element,
    ):
        base_page.tap(("id", "test_button"))

    element.click.assert_called_once()


def test_enter_text_clears_and_enters_text(base_page):
    element = MagicMock()

    with patch.object(
        base_page,
        "find_element",
        return_value=element,
    ):
        base_page.enter_text(("id", "username"), "test_user")

    element.clear.assert_called_once()
    element.send_keys.assert_called_once_with("test_user")


def test_get_text_returns_element_text(base_page):
    element = MagicMock()
    element.text = "Settings"

    with patch.object(
        base_page,
        "find_element",
        return_value=element,
    ):
        result = base_page.get_text(("id", "title"))

    assert result == "Settings"


def test_is_displayed_returns_true(base_page):
    element = MagicMock()
    element.is_displayed.return_value = True

    with patch.object(
        base_page,
        "find_element",
        return_value=element,
    ):
        result = base_page.is_displayed(("id", "title"))

    assert result is True