"""Analyze historical pytest metrics reports for inconsistent test outcomes."""

import argparse
import json
from collections import defaultdict
from pathlib import Path


def analyze_reports(report_paths):
    """Identify tests with both passing and failing outcomes across reports."""
    outcomes_by_test = defaultdict(lambda: {"passed": 0, "failed": 0})
    reports_read = 0

    for report_path in report_paths:
        path = Path(report_path)

        if not path.is_file():
            raise FileNotFoundError(f"Metrics report not found: {path}")

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in metrics report: {path}") from exc

        if not isinstance(data, dict) or not isinstance(data.get("results"), list):
            raise ValueError(
                f"Invalid metrics structure in {path}: expected a "
                "JSON object containing a results list"
            )

        for index, result in enumerate(data["results"]):
            if not isinstance(result, dict):
                raise ValueError(
                    f"Invalid result at index {index} in {path}"
                )

            test_name = result.get("test_name")
            outcome = str(result.get("outcome", "")).strip().lower()

            if not test_name:
                raise ValueError(
                    f"Missing test_name at index {index} in {path}"
                )

            if outcome in {"passed", "pass"}:
                outcomes_by_test[test_name]["passed"] += 1
            elif outcome in {"failed", "fail"}:
                outcomes_by_test[test_name]["failed"] += 1
            # Skipped and other outcomes are not included in the failure rate.

        reports_read += 1

    flaky_tests = []

    for test_name, counts in sorted(outcomes_by_test.items()):
        passed = counts["passed"]
        failed = counts["failed"]
        executions = passed + failed

        if passed > 0 and failed > 0:
            flaky_tests.append(
                {
                    "test_name": test_name,
                    "passed": passed,
                    "failed": failed,
                    "executions": executions,
                    "failure_rate_percent": round(
                        failed / executions * 100, 2
                    ),
                }
            )

    return {
        "reports_read": reports_read,
        "total_unique_tests": len(outcomes_by_test),
        "flaky_test_count": len(flaky_tests),
        "flaky_tests": flaky_tests,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Detect inconsistent test outcomes across metrics reports."
    )
    parser.add_argument(
        "reports",
        nargs="+",
        help="Paths to existing pytest metrics JSON reports",
    )
    args = parser.parse_args()

    try:
        summary = analyze_reports(args.reports)
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
