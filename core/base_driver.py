from abc import ABC, abstractmethod


class BaseDriver(ABC):
    """Common interface for platform-specific driver managers."""

    @abstractmethod
    def start_driver(self):
        """Start the mobile automation session."""
        pass

    @abstractmethod
    def stop_driver(self):
        """Stop the mobile automation session."""
        pass