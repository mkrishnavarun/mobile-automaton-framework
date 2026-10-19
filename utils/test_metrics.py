import json
from pathlib import Path


class TestMetrics:
    """Collect and persist pytest execution metrics."""

    def __init__(self):
        self.results = {}
        self.slow_test_threshold = 5.0

    def record(self, report):
        """Record test results, durations, and failure details."""
        test_name = report.nodeid

        result = self.results.setdefault(
            test_name,
            {
                "test_name": test_name,
                "outcome": "unknown",
                "duration_seconds": 0.0,
                "phases": {},
                "worker_id": getattr(report, "worker_id", "master"),
                "is_slow": False,
                "failure_stage": None,
                "error_message": None,
            },
        )

        result["phases"][report.when] = report.outcome

        # Record the test's call-phase duration.
        if report.when == "call":
            result["duration_seconds"] = round(report.duration, 3)
            result["is_slow"] = (
                    report.duration > self.slow_test_threshold
            )

        # Record failures and skips from any execution phase.
        if report.failed:
            result["outcome"] = "failed"
            result["failure_stage"] = report.when

            if report.longrepr:
                result["error_message"] = str(report.longrepr)

        elif report.skipped:
            result["outcome"] = "skipped"

        elif report.when == "call" and report.passed:
            result["outcome"] = "passed"

    def save(self, output_path="reports/metrics/test-results.json"):
        """Write collected metrics to a JSON file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        results = list(self.results.values())

        data = {
            "total_tests": len(results),
            "passed": sum(r["outcome"] == "passed" for r in results),
            "failed": sum(r["outcome"] == "failed" for r in results),
            "skipped": sum(r["outcome"] == "skipped" for r in results),
            "slow_tests": sum(r.get("is_slow", False) for r in results),
            "slow_test_threshold_seconds": self.slow_test_threshold,
            "results": results,
        }

        path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

        summary_path = path.parent / f"{path.stem}-summary.txt"
        summary_path.write_text(
            self.generate_summary() + "\n",
            encoding="utf-8",
        )

        return path

    def generate_summary(self):
        """Generate a human-readable test execution summary."""
        results = list(self.results.values())

        total = len(results)
        passed = sum(r["outcome"] == "passed" for r in results)
        failed = sum(r["outcome"] == "failed" for r in results)
        skipped = sum(r["outcome"] == "skipped" for r in results)

        slow_tests = [
            r for r in results if r.get("is_slow", False)
        ]

        failed_tests = [
            r for r in results if r["outcome"] == "failed"
        ]

        summary = [
            "=" * 50,
            "TEST EXECUTION SUMMARY",
            "=" * 50,
            f"Total tests : {total}",
            f"Passed      : {passed}",
            f"Failed      : {failed}",
            f"Skipped     : {skipped}",
            f"Slow tests  : {len(slow_tests)}",
            f"Slow threshold: {self.slow_test_threshold} seconds",
        ]

        if failed_tests:
            summary.append("\nFailed tests:")

            for test in failed_tests:
                summary.append(f"- {test['test_name']}")
                summary.append(
                    f"  Stage: {test.get('failure_stage')}"
                )
                summary.append(
                    f"  Error: {test.get('error_message')}"
                )

        if slow_tests:
            summary.append("\nSlow tests:")

            for test in sorted(
                    slow_tests,
                    key=lambda item: item["duration_seconds"],
                    reverse=True,
            ):
                summary.append(
                    f"- {test['test_name']} "
                    f"({test['duration_seconds']}s)"
                )

        summary.append("=" * 50)

        return "\n".join(summary)