from enum import Enum


class FailureCategory(str, Enum):
    INFRASTRUCTURE = "infrastructure"
    ELEMENT_INTERACTION = "element_interaction"
    TIMEOUT = "timeout"
    ASSERTION = "assertion"
    UNKNOWN = "unknown"


def classify_failure(error_message: str) -> FailureCategory:
    """Classify a test failure using its exception message."""

    message = (error_message or "").lower()

    # Infrastructure and Appium connectivity problems
    infrastructure_patterns = (
        "connection refused",
        "failed to establish a new connection",
        "max retries exceeded",
        "could not start a new session",
        "appium server",
        "connection reset",
    )

    if any(pattern in message for pattern in infrastructure_patterns):
        return FailureCategory.INFRASTRUCTURE

    # Timeout-related failures
    timeout_patterns = (
        "timeoutexception",
        "timeout exception",
        "timed out",
        "timeout waiting",
    )

    if any(pattern in message for pattern in timeout_patterns):
        return FailureCategory.TIMEOUT

    # Element lookup and interaction failures
    element_patterns = (
        "nosuchelementexception",
        "no such element",
        "elementinteractionerror",
        "staleelementreferenceexception",
        "element not interactable",
        "elementclickinterceptedexception",
    )

    if any(pattern in message for pattern in element_patterns):
        return FailureCategory.ELEMENT_INTERACTION

    # Assertion failures
    assertion_patterns = (
        "assertionerror",
        "assert ",
        "assertion failed",
    )

    if any(pattern in message for pattern in assertion_patterns):
        return FailureCategory.ASSERTION

    return FailureCategory.UNKNOWN
