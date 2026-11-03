
from detectors import extract_dates


def test_month_day_year():
    results = extract_dates("Deadline: November 15, 2026.")

    assert results[0]["date"] == "2026-11-15"


def test_iso_date():
    results = extract_dates("Submit by 2026-12-01.")

    assert results[0]["date"] == "2026-12-01"


def test_multiple_dates():
    results = extract_dates(
        "Applications close November 15, 2026. "
        "Interviews begin December 3, 2026."
    )

    assert len(results) == 2


def test_no_dates():
    results = extract_dates("Remember to contact the recruiter.")

    assert results == []
