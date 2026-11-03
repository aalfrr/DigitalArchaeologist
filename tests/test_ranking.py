
from datetime import date, timedelta

from ranking import rank_finding


def test_deadline_scores_higher_than_reminder(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Sample document")

    deadline = {"category": "deadline", "dates": []}
    reminder = {"category": "reminder", "dates": []}

    deadline_result = rank_finding(deadline, file_path)
    reminder_result = rank_finding(reminder, file_path)

    assert deadline_result["score"] > reminder_result["score"]


def test_approaching_date_increases_score(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Sample document")

    finding_without_date = {
        "category": "deadline",
        "dates": []
    }

    finding_with_date = {
        "category": "deadline",
        "dates": [{
            "date": (date.today() + timedelta(days=3)).isoformat()
        }]
    }

    without_date = rank_finding(finding_without_date, file_path)
    with_date = rank_finding(finding_with_date, file_path)

    assert with_date["score"] > without_date["score"]


def test_ranking_has_explanation(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Sample document")

    finding = {
        "category": "deadline",
        "dates": []
    }

    result = rank_finding(finding, file_path)

    assert result["score"] > 0
    assert len(result["reasons"]) > 0
