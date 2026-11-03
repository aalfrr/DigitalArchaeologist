
from pathlib import Path
from extractors import extract_text


def test_text_extraction():
    test_file = Path("sample_documents/test.txt")
    test_file.write_text(
        "Remember to submit assignment by November 15.",
        encoding="utf-8"
    )

    result = extract_text(test_file)

    assert "submit assignment" in result
    assert "November 15" in result

    test_file.unlink()
