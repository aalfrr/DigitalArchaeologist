
from datetime import date, datetime
from pathlib import Path


CATEGORY_SCORES = {
    "deadline": 30,
    "registration": 25,
    "follow-up": 20,
    "reminder": 10
}


def rank_finding(finding, file_path):
    """Calculate an explainable priority score for an action."""

    score = 0
    reasons = []

    # 1. Action category
    category = finding["category"]
    category_score = CATEGORY_SCORES.get(category, 0)

    score += category_score

    if category_score:
        reasons.append(f"{category}: +{category_score}")

    # 2. Date proximity
    today = date.today()

    for item in finding.get("dates", []):
        deadline = date.fromisoformat(item["date"])
        days_remaining = (deadline - today).days

        if days_remaining < 0:
            score += 15
            reasons.append("Date has passed: +15")

        elif days_remaining <= 7:
            score += 30
            reasons.append("Date within 7 days: +30")

        elif days_remaining <= 30:
            score += 20
            reasons.append("Date within 30 days: +20")

        break  # Only use the first date associated with this action.

    # 3. File age
    path = Path(file_path)

    modified_date = datetime.fromtimestamp(
        path.stat().st_mtime
    ).date()

    age_days = (today - modified_date).days

    if age_days >= 90:
        score += 10
        reasons.append("File is at least 90 days old: +10")

    return {
        "score": score,
        "reasons": reasons
    }
