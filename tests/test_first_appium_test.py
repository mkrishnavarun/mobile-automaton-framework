from pages.settings_page import SettingsPage
import pytest

@pytest.mark.mobile
def test_network_navigation(driver):
    settings_page = SettingsPage(driver)

    settings_page.open_network()

    assert settings_page.is_internet_screen_displayed()