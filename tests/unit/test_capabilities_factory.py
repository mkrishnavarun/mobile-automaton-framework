import pytest

from appium.options.android import UiAutomator2Options

from config.config_loader import ConfigLoader
from core.capabilities_factory import CapabilitiesFactory


def test_capabilities_factory_creates_android_options():
    config = ConfigLoader("local")

    options = CapabilitiesFactory.create_options(config)

    assert isinstance(options, UiAutomator2Options)
    assert options.platform_name == config.android["platform_name"]
    assert options.automation_name == config.android["automation_name"]
    assert options.device_name == config.android["device_name"]


def test_capabilities_factory_rejects_unsupported_platform(monkeypatch):
    config = ConfigLoader("local")

    monkeypatch.setitem(
        config.config,
        "platform",
        "unsupported",
    )

    with pytest.raises(ValueError, match="Unsupported platform"):
        CapabilitiesFactory.create_options(config)