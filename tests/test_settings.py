# def test_settings_app_opens(driver):
#     assert driver.current_package == "com.android.settings"

def test_settings_app_opens(settings_page, test_log_capture):
    # print(test_log_capture.getvalue())
    assert settings_page.is_settings_displayed()
    # assert False