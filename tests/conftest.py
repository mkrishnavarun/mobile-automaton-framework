import pytest

from config.config_loader import ConfigLoader
from utils.test_data_loader import TestDataLoader
from pages.settings_page import SettingsPage
from pytest_html import extras
import logging
import io
from core.driver_factory import DriverFactory
from api.api_client import APIClient
from utils.screenshot import ScreenshotUtil
import os
from utils.driver_diagnostics import DriverDiagnostics


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

    if report.when != "call" or not report.failed:
        return

    from pathlib import Path

    driver = item.funcargs.get("driver")

    project_root = Path(__file__).resolve().parent.parent
    report_dir = project_root / "reports" / "html"

    screenshot_dir = report_dir / "screenshots"
    source_dir = report_dir / "page_source"
    diagnostics_dir = report_dir / "driver_details"

    screenshot_dir.mkdir(parents=True, exist_ok=True)
    source_dir.mkdir(parents=True, exist_ok=True)
    diagnostics_dir.mkdir(parents=True, exist_ok=True)

    screenshot_path = None
    page_source_path = None
    diagnostics_path = None

    if driver:
        # Capture driver and device details
        try:
            diagnostics_path = Path(
                DriverDiagnostics.capture(driver, item.name)
            )

            logging.info(
                "Driver diagnostics captured: %s",
                diagnostics_path,
            )

        except Exception:
            logging.exception(
                "Failed to capture driver diagnostics for test: %s",
                item.name,
            )

        # Capture screenshot
        try:
            screenshot_path = screenshot_dir / f"{item.name}.png"

            driver.save_screenshot(str(screenshot_path))

            logging.info(
                "Failure screenshot captured: %s",
                screenshot_path,
            )

        except Exception:
            logging.exception(
                "Failed to capture screenshot for test: %s",
                item.name,
            )
            screenshot_path = None

        # Capture UI page source
        try:
            page_source_path = source_dir / f"{item.name}.xml"

            page_source_path.write_text(
                driver.page_source,
                encoding="utf-8",
            )

            logging.info(
                "Page source captured: %s",
                page_source_path,
            )

        except Exception:
            logging.exception(
                "Failed to capture page source for test: %s",
                item.name,
            )
            page_source_path = None

    # Add diagnostics to the HTML report
    if item.config.pluginmanager.getplugin("html"):
        extra = list(getattr(report, "extras", []))

        extra.append(
            extras.text(
                report.longreprtext,
                name="Failure Details",
            )
        )

        # Attach test logs
        log_capture = item.funcargs.get("test_log_capture")

        if log_capture:
            logs = log_capture.getvalue()

            if logs:
                extra.append(
                    extras.text(
                        logs,
                        name="Test Logs",
                    )
                )

        # Embed screenshot
        if screenshot_path and screenshot_path.exists():
            extra.append(
                extras.image(
                    os.path.relpath(
                        screenshot_path,
                        report_dir,
                    ),
                    name="Failure Screenshot",
                )
            )

        # Link page source
        if page_source_path and page_source_path.exists():
            extra.append(
                extras.url(
                    os.path.relpath(
                        page_source_path,
                        report_dir,
                    ),
                    name="Failure Page Source",
                )
            )

        # Link driver diagnostics
        if diagnostics_path and diagnostics_path.exists():
            extra.append(
                extras.url(
                    os.path.relpath(
                        diagnostics_path,
                        report_dir,
                    ),
                    name="Driver Diagnostics",
                )
            )

        report.extras = extra


@pytest.fixture
def driver(config):
    driver_manager = DriverFactory.create_driver_manager(config)

    mobile_driver = driver_manager.start_driver()

    try:
        yield mobile_driver
    finally:
        driver_manager.stop_driver()


@pytest.fixture
def api_client(config):
    client = APIClient(
        base_url=config.api["base_url"],
        timeout=config.api["timeout"],
    )

    try:
        yield client
    finally:
        client.close()