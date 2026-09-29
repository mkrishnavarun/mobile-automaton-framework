def test_configuration(config):
    assert config.appium["server_url"] == "http://127.0.0.1:4723"
    assert config.android["platform_name"] == "Android"
    assert config.android["automation_name"] == "UiAutomator2"