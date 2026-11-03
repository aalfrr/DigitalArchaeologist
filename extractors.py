
from pathlib import Path
from pypdf import PdfReader


def extract_text(file_path):
    """Extract text from a supported document."""

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="replace")

    elif extension == ".pdf":
        reader = PdfReader(path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)

        return "\n".join(pages)

    else:
        raise ValueError(f"Unsupported file type: {extension}")
