import pytest

from appium.options.android import UiAutomator2Options

from config.config_loader import ConfigLoader
from core.strategies.base_capabilities import BaseCapabilities
from core.strategies.android_capabilities import AndroidCapabilities


def test_android_capabilities_implements_base_interface():
    strategy = AndroidCapabilities()

    assert isinstance(strategy, BaseCapabilities)


def test_base_capabilities_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseCapabilities()


def test_android_capabilities_creates_valid_options():
    config = ConfigLoader("local")

    strategy = AndroidCapabilities()
    options = strategy.create_options(config)

    assert isinstance(options, UiAutomator2Options)
    assert options.platform_name == config.android["platform_name"]
    assert options.automation_name == config.android["automation_name"]
    assert options.device_name == config.android["device_name"]