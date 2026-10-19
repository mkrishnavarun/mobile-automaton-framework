from abc import ABC, abstractmethod


class BaseCapabilities(ABC):
    """Interface for platform-specific Appium capabilities."""

    @abstractmethod
    def create_options(self, config):
        """Create Appium options for a platform."""
        pass