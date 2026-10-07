import time
from functools import wraps
from utils.logger import Logger

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)


RETRYABLE_EXCEPTIONS = (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)


def retry_on_exception(
    retries: int = 2,
    delay: float = 1.0,
):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            logger = Logger.get_logger(func.__name__)

            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)

                except RETRYABLE_EXCEPTIONS as exc:
                    last_exception = exc

                    if attempt == retries:
                        raise

                    time.sleep(delay)

            raise last_exception

        return wrapper

    return decorator