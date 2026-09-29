import logging
from pathlib import Path


class Logger:
    """Centralized logger for the mobile automation framework."""

    @staticmethod
    def get_logger(name: str = "mobile-framework") -> logging.Logger:
        logger = logging.getLogger(name)

        if logger.handlers:
            return logger

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # File handler
        project_root = Path(__file__).resolve().parent.parent
        log_directory = project_root / "logs"
        log_directory.mkdir(exist_ok=True)

        file_handler = logging.FileHandler(
            log_directory / "framework.log",
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger