class MobileFrameworkError(Exception):
    """Base exception for the mobile automation framework."""


class DriverInitializationError(MobileFrameworkError):
    """Raised when the Appium driver cannot be initialized."""

class ElementInteractionError(MobileFrameworkError):
    """Raised when an element interaction fails."""