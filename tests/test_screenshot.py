from pathlib import Path

from utils.screenshot import ScreenshotUtil
import pytest

@pytest.mark.mobile
def test_capture_screenshot(driver):
    screenshot_path = ScreenshotUtil.capture(
        driver,
        "settings_page",
    )

    assert Path(screenshot_path).exists()