from unittest.mock import patch

import pytest
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
)


from utils.retry_utils import retry_on_exception
from utils.retry_metrics import retry_metrics


@pytest.fixture(autouse=True)
def reset_retry_metrics():
    retry_metrics.reset()
    yield
    retry_metrics.reset()


def test_success_on_first_attempt():
    operation = lambda: "success"

    with patch("utils.retry_utils.Logger.get_logger") as mock_logger:
        result = retry_on_exception()(operation)()

    assert result == "success"
    mock_logger.return_value.info.assert_not_called()
    mock_logger.return_value.warning.assert_not_called()
    mock_logger.return_value.error.assert_not_called()


def test_recovers_after_retry():
    call_count = 0

    def flaky_operation():
        nonlocal call_count
        call_count += 1

        if call_count == 1:
            raise StaleElementReferenceException("Element became stale")

        return "success"

    with (
            patch("utils.retry_utils.time.sleep") as mock_sleep,
            patch("utils.retry_utils.Logger.get_logger") as mock_logger,
        ):
            result = retry_on_exception(retries=2, delay=0.1)(
                flaky_operation
            )()

    assert result == "success"
    assert call_count == 2
    mock_sleep.assert_called_once_with(0.1)
    mock_logger.return_value.warning.assert_called_once()
    mock_logger.return_value.info.assert_called_once()


def test_raises_exception_after_all_attempts():
    call_count = 0

    def failing_operation():
        nonlocal call_count
        call_count += 1
        raise StaleElementReferenceException("Element became stale")

    with (
        patch("utils.retry_utils.time.sleep") as mock_sleep,
        patch("utils.retry_utils.Logger.get_logger") as mock_logger,
        pytest.raises(StaleElementReferenceException),
    ):
        retry_on_exception(retries=2, delay=0.1)(failing_operation)()

    assert call_count == 3
    assert mock_sleep.call_count == 2
    mock_logger.return_value.warning.call_count == 2
    mock_logger.return_value.error.assert_called_once()


def test_non_retryable_exception_propagates_immediately():
    call_count = 0

    def failing_operation():
        nonlocal call_count
        call_count += 1
        raise ValueError("Invalid input")

    with (
        patch("utils.retry_utils.time.sleep") as mock_sleep,
        pytest.raises(ValueError, match="Invalid input"),
    ):
        retry_on_exception(retries=2)(failing_operation)()

    assert call_count == 1
    mock_sleep.assert_not_called()


def test_invalid_retry_configuration():
    with pytest.raises(ValueError, match="retries must be >= 0"):
        retry_on_exception(retries=-1)

    with pytest.raises(ValueError, match="delay must be >= 0"):
        retry_on_exception(delay=-1)


def test_intercepted_click_is_retryable():
    call_count = 0

    def operation():
        nonlocal call_count
        call_count += 1

        if call_count == 1:
            raise ElementClickInterceptedException("Click intercepted")

        return "clicked"

    with patch("utils.retry_utils.time.sleep"):
        result = retry_on_exception(retries=1)(operation)()

    assert result == "clicked"
    assert call_count == 2



def test_metrics_for_immediate_success():
    result = retry_on_exception()(lambda: "success")()

    assert result == "success"
    assert retry_metrics.get_summary() == {
        "retry_attempts": 0,
        "recovered_operations": 0,
        "exhausted_operations": 0,
    }


def test_metrics_for_recovered_operation():
    calls = 0

    def operation():
        nonlocal calls
        calls += 1

        if calls == 1:
            raise StaleElementReferenceException("Temporary failure")

        return "success"

    with patch("utils.retry_utils.time.sleep"):
        result = retry_on_exception(retries=2, delay=0)(operation)()

    assert result == "success"
    assert retry_metrics.get_summary() == {
        "retry_attempts": 1,
        "recovered_operations": 1,
        "exhausted_operations": 0,
    }


def test_metrics_for_exhausted_operation():
    def operation():
        raise StaleElementReferenceException("Persistent failure")

    with (
        patch("utils.retry_utils.time.sleep"),
        pytest.raises(StaleElementReferenceException),
    ):
        retry_on_exception(retries=2, delay=0)(operation)()

    assert retry_metrics.get_summary() == {
        "retry_attempts": 2,
        "recovered_operations": 0,
        "exhausted_operations": 1,
    }


def test_non_retryable_exception_does_not_change_metrics():
    def operation():
        raise ValueError("Invalid input")

    with pytest.raises(ValueError, match="Invalid input"):
        retry_on_exception(retries=2, delay=0)(operation)()

    assert retry_metrics.get_summary() == {
        "retry_attempts": 0,
        "recovered_operations": 0,
        "exhausted_operations": 0,
    }