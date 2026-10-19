import pytest

@pytest.mark.mobile
def test_settings_app_opens(settings_page, test_log_capture):
    assert settings_page.is_settings_displayed()