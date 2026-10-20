import pytest
from unittest.mock import Mock, patch
import conftest

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


def test_driver_reference_cleared_when_quit_fails():
    config = ConfigLoader("local")
    driver_manager = DriverManager(config)

    mock_driver = Mock()
    mock_driver.quit.side_effect = RuntimeError("Simulated quit failure")

    driver_manager.driver = mock_driver

    with pytest.raises(RuntimeError, match="Simulated quit failure"):
        driver_manager.stop_driver()

    assert driver_manager.driver is None
    mock_driver.quit.assert_called_once()

def test_driver_fixture_cleans_up_when_startup_fails():
    config = ConfigLoader("local")
    mock_manager = Mock()
    mock_manager.start_driver.side_effect = RuntimeError(
        "Simulated startup failure"
    )

    fixture_function = conftest.driver.__wrapped__
    generator = fixture_function(config)

    with patch(
        "conftest.DriverFactory.create_driver_manager",
        return_value=mock_manager,
    ):
        with pytest.raises(RuntimeError, match="Simulated startup failure"):
            next(generator)

    mock_manager.stop_driver.assert_called_once()
