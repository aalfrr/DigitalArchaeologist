
from detectors import detect_actions


def test_deadline_detection():
    text = "The assignment is due by November 15."

    findings = detect_actions(text)

    assert any(item["category"] == "deadline" for item in findings)


def test_follow_up_detection():
    text = "Follow up with the recruiter next Friday."

    findings = detect_actions(text)

    assert any(item["category"] == "follow-up" for item in findings)


def test_no_false_findings():
    text = "The weather is sunny today."

    findings = detect_actions(text)

    assert findings == []


def test_multiple_categories():
    text = (
        "Remember to submit the application. "
        "Follow up with the recruiter."
    )

    findings = detect_actions(text)

    categories = {item["category"] for item in findings}

    assert "reminder" in categories
    assert "follow-up" in categories

def test_context_contains_complete_sentence():
    text = (
        "Remember to submit the scholarship application by November 15. "
        "Follow up with the engineering team next Friday."
    )

    findings = detect_actions(text)

    reminder = next(
        item for item in findings
        if item["category"] == "reminder"
    )

    assert reminder["context"] == (
        "Remember to submit the scholarship application by November 15."
    )
