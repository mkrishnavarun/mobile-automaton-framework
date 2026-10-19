import pytest

from config.config_loader import ConfigLoader
from core.driver_factory import DriverFactory
from core.driver_manager import DriverManager


def test_driver_factory_creates_android_driver_manager():
    config = ConfigLoader("local")

    driver_manager = DriverFactory.create_driver_manager(config)

    assert isinstance(driver_manager, DriverManager)


def test_driver_factory_rejects_unsupported_platform(monkeypatch):
    config = ConfigLoader("local")

    monkeypatch.setitem(
        config.config,
        "platform",
        "unsupported",
    )

    with pytest.raises(ValueError, match="Unsupported platform"):
        DriverFactory.create_driver_manager(config)
