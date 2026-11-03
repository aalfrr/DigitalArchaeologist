
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".pdf",
}


def scan_folder(folder_path):
    """Return supported files found in a folder and its subfolders."""
    folder = Path(folder_path).expanduser().resolve()

    if not folder.is_dir():
        raise NotADirectoryError(f"Not a valid folder: {folder}")

    files = []

    for path in folder.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)

    return sorted(files)


if __name__ == "__main__":
    folder = Path(__file__).parent / "sample_documents"

    for file in scan_folder(folder):
        print(file.name)
