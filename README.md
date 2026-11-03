# Digital Archaeologist

A local-first Python automation tool that searches documents for potentially forgotten deadlines, reminders, registrations, and follow-ups.

Instead of manually revisiting old files, Digital Archaeologist extracts actionable information, assigns explainable priority scores, and generates an HTML report.

## Features

- **Document scanning:** Recursively searches selected folders for TXT, Markdown, and PDF files.
- **Text extraction:** Extracts readable text from supported documents.
- **Action detection:** Uses regular expressions to identify deadlines, reminders, follow-ups, and registration dates.
- **Date extraction:** Identifies explicit calendar dates and associates them with detected actions.
- **Priority ranking:** Scores findings based on action type, date proximity, and document age.
- **Incremental scanning:** Uses SHA-256 fingerprints to detect unchanged files and avoid unnecessary processing.
- **Persistent storage:** Uses SQLite to retain scan history, file fingerprints, and previously detected findings.
- **HTML reporting:** Generates a readable report with priority explanations and category summaries.
- **Automated testing:** Uses pytest to verify extraction, detection, ranking, database, and report functionality.

## Technologies

- Python
- SQLite
- Regular expressions
- SHA-256 hashing
- HTML/CSS
- pytest
- pypdf
- python-dateutil

## Setup

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd DigitalArchaeologist
```

Create and activate a virtual environment:

**Windows PowerShell**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install pypdf python-dateutil pytest
```

## Usage

Place documents you want to scan inside `sample_documents/`.

Run the application:

```powershell
python main.py
```

Open the generated report:

```powershell
Invoke-Item .\reports\latest_report.html
```

Run automated tests:

```powershell
python -m pytest -v
```

## How It Works

1. The scanner locates supported documents.
2. SHA-256 hashing determines whether each file has changed since its last successful scan.
3. New or modified documents are processed and their text is extracted.
4. Regular expressions identify potentially actionable phrases.
5. Explicit dates are associated with detected actions.
6. A scoring system assigns priority levels and explains its reasoning.
7. Findings, scan history, and file fingerprints are saved in SQLite.
8. The application generates an HTML report using both newly detected and previously stored findings.

## Privacy

Document processing is performed locally. Document contents are not sent to an external API. The SQLite database and generated reports remain on the local machine.

## Limitations

- Scanned PDFs containing images require OCR, which is not currently implemented.
- Detection is rule-based and may produce false positives or miss some phrasing.
- Relative dates such as "next Friday" are not currently resolved.
- Priority scores are heuristic estimates and should be reviewed rather than treated as definitive reminders.

## Future Improvements

- Configurable scan directories and excluded folders.
- Support for additional document formats.
- Improved natural-language date interpretation.
- Background or scheduled scanning.
- More advanced report filtering and search.