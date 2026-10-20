import json

import pytest

from core.execution_insights import generate_insights, save_insights


@pytest.fixture
def report_file(tmp_path):
    """Create a sample test execution report."""
    report = {
        "total_tests": 4,
        "passed": 2,
        "failed": 2,
        "skipped": 0,
        "retry_metrics": {
            "retry_attempts": 3,
            "recovered_operations": 1,
            "exhausted_operations": 1,
        },
        "results": [
            {
                "test_name": "test_fast",
                "outcome": "passed",
                "duration_seconds": 1.0,
                "is_slow": False,
                "failure_category": None,
            },
            {
                "test_name": "test_slow",
                "outcome": "passed",
                "duration_seconds": 8.0,
                "is_slow": True,
                "failure_category": None,
            },
            {
                "test_name": "test_timeout",
                "outcome": "failed",
                "duration_seconds": 3.0,
                "is_slow": False,
                "failure_category": "timeout",
            },
            {
                "test_name": "test_assertion",
                "outcome": "failed",
                "duration_seconds": 2.0,
                "is_slow": False,
                "failure_category": "assertion",
            },
        ],
    }

    path = tmp_path / "report.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    return path


def test_calculates_pass_rate(report_file):
    insights = generate_insights(report_file)

    assert insights["total_tests"] == 4
    assert insights["passed"] == 2
    assert insights["failed"] == 2
    assert insights["pass_rate_percent"] == 50.0


def test_identifies_failure_categories(report_file):
    insights = generate_insights(report_file)

    assert insights["failure_categories"] == {
        "timeout": 1,
        "assertion": 1,
    }


def test_identifies_slowest_tests(report_file):
    insights = generate_insights(report_file)

    assert insights["slowest_tests"][0]["test_name"] == "test_slow"
    assert insights["slowest_tests"][0]["duration_seconds"] == 8.0


def test_includes_retry_metrics(report_file):
    insights = generate_insights(report_file)

    assert insights["retry_metrics"]["retry_attempts"] == 3
    assert insights["retry_metrics"]["recovered_operations"] == 1
    assert insights["retry_metrics"]["exhausted_operations"] == 1


def test_generates_failure_insights(report_file):
    insights = generate_insights(report_file)

    assert any("2 test(s) failed" in item for item in insights["insights"])
    assert any("timeout" in item for item in insights["insights"])
    assert any("Slowest test" in item for item in insights["insights"])


def test_rejects_missing_report(tmp_path):
    missing_file = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        generate_insights(missing_file)


def test_saves_insights_as_json(report_file, tmp_path):
    output_file = tmp_path / "insights.json"

    returned_path = save_insights(report_file, output_file)

    assert returned_path == output_file
    assert output_file.exists()

    saved_data = json.loads(output_file.read_text(encoding="utf-8"))
    assert saved_data["pass_rate_percent"] == 50.0


def test_handles_report_without_results(tmp_path):
    path = tmp_path / "empty.json"
    path.write_text(
        json.dumps({
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "results": [],
        }),
        encoding="utf-8",
    )

    insights = generate_insights(path)

    assert insights["pass_rate_percent"] == 0.0
    assert insights["failure_categories"] == {}
    assert insights["slowest_tests"] == []