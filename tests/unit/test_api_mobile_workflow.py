import logging

logger = logging.getLogger(__name__)

import pytest

@pytest.mark.mobile
def test_api_and_mobile_workflow(api_client, driver):
    """Validate API and mobile UI in one workflow."""

    # Step 1: API validation
    logger.info("STEP 1: Starting API validation")

    response = api_client.get("/posts/1")

    logger.info("API response status: %s", response.status_code)

    assert response.status_code == 200, (
        f"API validation failed: expected HTTP 200, "
        f"received HTTP {response.status_code}"
    )

    post = response.json()

    assert post["id"] == 1, "API returned an unexpected post ID"
    assert "title" in post, "API response is missing the title"
    assert "body" in post, "API response is missing the body"

    logger.info("STEP 1 PASSED: API validation successful")

    # Step 2: Mobile UI validation
    logger.info("STEP 2: Starting mobile UI validation")

    current_package = driver.current_package

    logger.info("Current Android package: %s", current_package)

    assert current_package == "com.android.settings", (
        f"Mobile UI validation failed: expected "
        f"com.android.settings, received {current_package}"
    )

    logger.info("STEP 2 PASSED: Mobile UI validation successful")

    logger.info("WORKFLOW PASSED: API and mobile validations completed")

from unittest.mock import MagicMock, patch


from api.api_client import APIClient


def test_api_failure_returns_error_status():
    client = APIClient("https://example.com")

    try:
        with patch.object(client.session, "get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=500,
                json=lambda: {"error": "Internal Server Error"},
            )

            response = client.get("/posts/1")

            assert response.status_code == 500
            assert response.json() == {
                "error": "Internal Server Error"
            }
    finally:
        client.close()