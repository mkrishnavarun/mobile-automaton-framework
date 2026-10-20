import json
from collections import Counter
from pathlib import Path


def generate_insights(report_path, top_n=5):
    """Generate actionable insights from a test execution report."""
    path = Path(report_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Test report not found: {report_path}"
        )

    with path.open(encoding="utf-8") as file:
        report = json.load(file)

    results = report.get("results", [])

    total = report.get("total_tests", len(results))
    passed = report.get("passed", 0)
    failed = report.get("failed", 0)
    skipped = report.get("skipped", 0)

    executed = passed + failed
    pass_rate = round((passed / executed) * 100, 2) if executed else 0.0

    slow_tests = sorted(
        (
            test
            for test in results
            if test.get("is_slow", False)
        ),
        key=lambda test: test.get("duration_seconds", 0),
        reverse=True,
    )

    failure_categories = Counter(
        test.get("failure_category") or "unknown"
        for test in results
        if test.get("outcome") == "failed"
    )

    retry_metrics = report.get("retry_metrics", {})
    retry_attempts = retry_metrics.get("retry_attempts", 0)
    recovered = retry_metrics.get("recovered_operations", 0)
    exhausted = retry_metrics.get("exhausted_operations", 0)

    insights = []

    if failed:
        insights.append(
            f"{failed} test(s) failed. Review failure categories "
            "to prioritize investigation."
        )

    if failure_categories:
        category, count = failure_categories.most_common(1)[0]
        insights.append(
            f"Most frequent failure category: {category} "
            f"({count} test(s))."
        )

    if slow_tests:
        slowest = slow_tests[0]
        insights.append(
            f"Slowest test: {slowest.get('test_name', 'unknown')} "
            f"({slowest.get('duration_seconds', 0):.3f}s)."
        )

    if exhausted:
        insights.append(
            f"{exhausted} operation(s) exhausted their retries. "
            "Investigate persistent interaction failures."
        )

    if not insights:
        insights.append(
            "No failures or slow tests were flagged in this report."
        )

    return {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "pass_rate_percent": pass_rate,
        "failure_categories": dict(failure_categories),
        "slowest_tests": [
            {
                "test_name": test.get("test_name", "unknown"),
                "duration_seconds": test.get("duration_seconds", 0),
            }
            for test in slow_tests[:top_n]
        ],
        "retry_metrics": {
            "retry_attempts": retry_attempts,
            "recovered_operations": recovered,
            "exhausted_operations": exhausted,
        },
        "insights": insights,
    }


def save_insights(report_path, output_path=None):
    """Generate insights and save them as JSON."""
    report_path = Path(report_path)

    if output_path is None:
        output_path = (
            report_path.parent / f"{report_path.stem}-insights.json"
        )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    insights = generate_insights(report_path)

    output_path.write_text(
        json.dumps(insights, indent=2),
        encoding="utf-8",
    )

    return output_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate actionable test execution insights."
    )
    parser.add_argument(
        "report",
        help="Path to the test execution JSON report",
    )
    parser.add_argument(
        "--output",
        help="Optional output path for the insights JSON",
    )
    args = parser.parse_args()

    output_path = save_insights(args.report, args.output)
    print(f"Execution insights saved to: {output_path}")