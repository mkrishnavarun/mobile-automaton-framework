import json
from pathlib import Path

from utils.logger import Logger


class DriverDiagnostics:
    """Collect diagnostic information from an Appium driver."""

    logger = Logger.get_logger(__name__)

    @staticmethod
    def capture(driver, test_name: str) -> str:
        project_root = Path(__file__).resolve().parent.parent

        diagnostics_dir = (
            project_root / "reports" / "html" / "driver_details"
        )
        diagnostics_dir.mkdir(parents=True, exist_ok=True)

        capabilities = driver.capabilities or {}

        details = {
            "test_name": test_name,
            "session_id": driver.session_id,
            "session_active": driver.session_id is not None,
            "platform_name": capabilities.get("platformName"),
            "platform_version": capabilities.get("platformVersion"),
            "device_name": capabilities.get("deviceName"),
            "automation_name": capabilities.get("automationName"),
            "app_package": capabilities.get("appPackage"),
            "app_activity": capabilities.get("appActivity"),
        }

        output_path = diagnostics_dir / f"{test_name}.json"

        output_path.write_text(
            json.dumps(details, indent=4),
            encoding="utf-8",
        )

        DriverDiagnostics.logger.info(
            "Driver diagnostics captured: %s",
            output_path,
        )

        return str(output_path)