import json
from pathlib import Path
from threading import Lock


class RetryMetrics:
    """Thread-safe collector for retry operation metrics."""

    def __init__(self):
        self._lock = Lock()
        self._metrics = {
            "retry_attempts": 0,
            "recovered_operations": 0,
            "exhausted_operations": 0,
        }

    def record_retry_attempt(self):
        with self._lock:
            self._metrics["retry_attempts"] += 1

    def record_recovery(self):
        with self._lock:
            self._metrics["recovered_operations"] += 1

    def record_exhaustion(self):
        with self._lock:
            self._metrics["exhausted_operations"] += 1

    def get_summary(self):
        with self._lock:
            return self._metrics.copy()

    def reset(self):
        with self._lock:
            for key in self._metrics:
                self._metrics[key] = 0

    def save(self, output_path):
        """Save this process's retry metrics to a JSON file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.get_summary(), indent=2),
            encoding="utf-8",
        )
        return path

    def merge(self, metrics_data):
        """Add retry metrics from another process."""
        with self._lock:
            for key in self._metrics:
                self._metrics[key] += int(metrics_data.get(key, 0))


retry_metrics = RetryMetrics()