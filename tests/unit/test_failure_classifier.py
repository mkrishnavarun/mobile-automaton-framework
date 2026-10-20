import pytest

from core.failure_classifier import (
    FailureCategory,
    classify_failure,
)


@pytest.mark.parametrize(
    "message, expected",
    [
        (
            "Connection refused: Appium server unavailable",
            FailureCategory.INFRASTRUCTURE,
        ),
        (
            "Failed to establish a new connection",
            FailureCategory.INFRASTRUCTURE,
        ),
        (
            "NoSuchElementException: element not found",
            FailureCategory.ELEMENT_INTERACTION,
        ),
        (
            "ElementInteractionError: unable to tap element",
            FailureCategory.ELEMENT_INTERACTION,
        ),
        (
            "TimeoutException: timed out waiting for element",
            FailureCategory.TIMEOUT,
        ),
        (
            "AssertionError: expected 200 but got 500",
            FailureCategory.ASSERTION,
        ),
        (
            "Unexpected framework error",
            FailureCategory.UNKNOWN,
        ),
    ],
)
def test_classify_failure(message, expected):
    assert classify_failure(message) == expected


@pytest.mark.parametrize(
    "message",
    [
        "",
        None,
    ],
)
def test_empty_or_missing_message_is_unknown(message):
    assert classify_failure(message) == FailureCategory.UNKNOWN


def test_classification_is_case_insensitive():
    assert (
        classify_failure("CONNECTION REFUSED")
        == FailureCategory.INFRASTRUCTURE
    )
