import json

import pytest

from core.flaky_test_analyzer import analyze_reports


def write_report(tmp_path, filename, results):
    path = tmp_path / filename
    path.write_text(
        json.dumps({"results": results}),
        encoding="utf-8",
    )
    return path


def test_detects_test_with_inconsistent_outcomes(tmp_path):
    report_one = write_report(
        tmp_path,
        "run1.json",
        [
            {"test_name": "test_login", "outcome": "passed"},
            {"test_name": "test_search", "outcome": "passed"},
        ],
    )
    report_two = write_report(
        tmp_path,
        "run2.json",
        [
            {"test_name": "test_login", "outcome": "failed"},
            {"test_name": "test_search", "outcome": "passed"},
        ],
    )

    summary = analyze_reports([report_one, report_two])

    assert summary["reports_read"] == 2
    assert summary["total_unique_tests"] == 2
    assert summary["flaky_test_count"] == 1

    flaky_test = summary["flaky_tests"][0]
    assert flaky_test["test_name"] == "test_login"
    assert flaky_test["passed"] == 1
    assert flaky_test["failed"] == 1
    assert flaky_test["executions"] == 2
    assert flaky_test["failure_rate_percent"] == 50.0


def test_consistently_passing_test_is_not_flaky(tmp_path):
    report = write_report(
        tmp_path,
        "run.json",
        [
            {"test_name": "test_settings", "outcome": "passed"},
            {"test_name": "test_settings", "outcome": "passed"},
        ],
    )

    summary = analyze_reports([report])

    assert summary["flaky_test_count"] == 0
    assert summary["flaky_tests"] == []


def test_consistently_failing_test_is_not_classified_as_flaky(tmp_path):
    report = write_report(
        tmp_path,
        "run.json",
        [
            {"test_name": "test_checkout", "outcome": "failed"},
            {"test_name": "test_checkout", "outcome": "failed"},
        ],
    )

    summary = analyze_reports([report])

    assert summary["flaky_test_count"] == 0


def test_skipped_results_do_not_affect_failure_rate(tmp_path):
    report = write_report(
        tmp_path,
        "run.json",
        [
            {"test_name": "test_api", "outcome": "passed"},
            {"test_name": "test_api", "outcome": "skipped"},
            {"test_name": "test_api", "outcome": "failed"},
        ],
    )

    summary = analyze_reports([report])

    assert summary["flaky_test_count"] == 1
    assert summary["flaky_tests"][0]["executions"] == 2
    assert summary["flaky_tests"][0]["failure_rate_percent"] == 50.0


def test_missing_report_raises_clear_error(tmp_path):
    with pytest.raises(FileNotFoundError, match="Metrics report not found"):
        analyze_reports([tmp_path / "missing.json"])


def test_malformed_json_raises_clear_error(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        analyze_reports([path])


def test_invalid_metrics_structure_raises_clear_error(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps({"total_tests": 2}), encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid metrics structure"):
        analyze_reports([path])
