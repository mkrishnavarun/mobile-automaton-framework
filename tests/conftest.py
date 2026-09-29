import pytest

from config.config_loader import ConfigLoader
from core.driver_manager import DriverManager
from utils.test_data_loader import TestDataLoader
from pages.settings_page import SettingsPage
from pytest_html import extras
import logging
import io


@pytest.fixture(autouse=True)
def test_log_capture():
    log_stream = io.StringIO()

    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.INFO)

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)

    yield log_stream

    root_logger.removeHandler(handler)

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="local",
        help="Environment to run tests against",
    )

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    environment = config.getoption("--env")

    environment_config = ConfigLoader(environment)

    if hasattr(config, "_metadata"):
        config._metadata["Environment"] = environment
        config._metadata["Platform"] = environment_config.android["platform_name"]
        config._metadata["Automation"] = environment_config.android["automation_name"]
        config._metadata["Device"] = environment_config.android["device_name"]
        config._metadata["Application"] = environment_config.app["package"]


@pytest.fixture
def config(request):
    environment = request.config.getoption("--env")
    return ConfigLoader(environment)


@pytest.fixture(scope="function")
def driver(config):
    driver_manager = DriverManager(config)

    mobile_driver = driver_manager.start_driver()

    try:
        yield mobile_driver
    finally:
        driver_manager.stop_driver()

@pytest.fixture
def login_data():
    return TestDataLoader.load("login_data.yaml")

@pytest.fixture
def settings_page(driver):
    return SettingsPage(driver)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        duration = f"{report.duration:.2f}s"
        report.user_properties.append(("Duration", duration))

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")

        if driver:
            import os

            screenshot_dir = "reports/html/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)

            file_name = f"{item.name}.png"
            file_path = os.path.join(screenshot_dir, file_name)

            driver.save_screenshot(file_path)

            pytest_html = item.config.pluginmanager.getplugin("html")

            if pytest_html:
                extra = getattr(report, "extras", [])

                extra.append(
                    extras.text(
                        report.longreprtext,
                        name="Failure Details"
                    )
                )

                # Add test logs
                log_capture = item.funcargs.get("test_log_capture")

                if log_capture:
                    logs = log_capture.getvalue()

                    if logs:
                        extra.append(
                            extras.text(
                                logs,
                                name="Test Logs"
                            )
                        )

                report_relative_path = os.path.join(
                    "..",
                    "screenshots",
                    file_name
                )

                extra.append(
                    extras.image(
                        report_relative_path,
                        name="Failure Screenshot"
                    )
                )

                report.extras = extra