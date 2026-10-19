import pytest

from config.config_loader import ConfigLoader
from core.base_driver import BaseDriver
from core.driver_manager import DriverManager


def test_base_driver_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseDriver()


def test_driver_manager_implements_base_driver():
    config = ConfigLoader("local")

    driver_manager = DriverManager(config)

    assert isinstance(driver_manager, BaseDriver)