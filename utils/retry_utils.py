import time
from functools import wraps

from utils.logger import Logger
from utils.retry_metrics import retry_metrics

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
    """Retry an operation on selected Selenium interaction exceptions.

    Args:
        retries: Number of retries after the initial attempt.
        delay: Seconds to wait between attempts.
    """
    if retries < 0:
        raise ValueError("retries must be >= 0")

    if delay < 0:
        raise ValueError("delay must be >= 0")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = Logger.get_logger(func.__module__)
            total_attempts = retries + 1

            for attempt in range(1, total_attempts + 1):
                try:
                    result = func(*args, **kwargs)

                    if attempt > 1:
                        retry_metrics.record_recovery()
                        logger.info(
                            "Retry recovered: %s succeeded on attempt %d/%d",
                            func.__qualname__,
                            attempt,
                            total_attempts,
                        )

                    return result

                except RETRYABLE_EXCEPTIONS as exc:
                    if attempt == total_attempts:
                        retry_metrics.record_exhaustion()
                        logger.error(
                            "Retry exhausted: %s failed after %d attempts. "
                            "Last error: %s: %s",
                            func.__qualname__,
                            total_attempts,
                            type(exc).__name__,
                            exc,
                        )
                        raise

                    retry_metrics.record_retry_attempt()

                    logger.warning(
                        "Retry attempt %d/%d failed for %s: %s: %s. "
                        "Retrying in %s seconds.",
                        attempt,
                        total_attempts,
                        func.__qualname__,
                        type(exc).__name__,
                        exc,
                        delay,
                    )

                    time.sleep(delay)

        return wrapper

    return decorator