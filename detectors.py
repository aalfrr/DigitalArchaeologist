from datetime import date
from dateutil import parser
import re


ACTION_PATTERNS = {
    "deadline": [
        r"\bdue\s+(?:by|on)\b",
        r"\bdeadline\b",
        r"\bsubmit\s+by\b",
        r"\bexpires?\s+on\b",
    ],

    "follow-up": [
        r"\bfollow\s+up\b",
        r"\bget\s+back\s+to\b",
        r"\bcontact\s+again\b",
        r"\bcheck\s+in\b",
    ],

    "reminder": [
        r"\bdon't\s+forget\b",
        r"\bremember\s+to\b",
        r"\bmake\s+sure\s+to\b",
        r"\bneed\s+to\b",
    ],

    "registration": [
        r"\bregistration\s+closes?\b",
        r"\bapplications?\s+close\b",
        r"\bsign\s+up\s+by\b",
    ],
}



def detect_actions(text):
    """Find actionable phrases and extract their containing sentences."""

    findings = []

    # Split text into sentences while retaining their positions.
    sentence_pattern = re.compile(r"[^.!?\n]+(?:[.!?]+|$)")

    sentences = list(sentence_pattern.finditer(text))

    for category, patterns in ACTION_PATTERNS.items():
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):

                # Find the sentence containing this match.
                for sentence in sentences:
                    if sentence.start() <= match.start() < sentence.end():

                        context = sentence.group().strip()

                        findings.append({
                            "category": category,
                            "phrase": match.group(),
                            "context": context,
                            "position": match.start()
                        })

                        break

    # Sort findings in the order they appear in the document.
    return sorted(findings, key=lambda item: item["position"])


def extract_dates(text):
    """Find explicit calendar dates in text."""

    date_pattern = re.compile(
        r"\b(?:"
        r"\d{4}-\d{1,2}-\d{1,2}"
        r"|"
        r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|"
        r"Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|"
        r"Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
        r"\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?"
        r")\b",
        re.IGNORECASE
    )

    dates = []

    for match in date_pattern.finditer(text):
        raw_date = match.group()

        try:
            parsed = parser.parse(
                raw_date,
                default=date.today().replace(month=1, day=1)
            )

            dates.append({
                "original": raw_date,
                "date": parsed.isoformat(),
                "position": match.start()
            })

        except (ValueError, OverflowError):
            continue

    return dates

def associate_dates(findings):
    """Attach dates from each finding's sentence to that finding."""

    for finding in findings:
        finding["dates"] = extract_dates(finding["context"])

    return findings
