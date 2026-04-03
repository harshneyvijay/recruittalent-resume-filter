from pypdf import PdfReader
from pathlib import Path


def extract_text(file):
    suffix = Path(file.filename).suffix.lower()

    if suffix == ".txt":
        return file.read().decode("utf-8", errors="ignore").strip()

    if suffix == ".pdf":
        try:
            reader = PdfReader(file)
            return "".join(page.extract_text() or "" for page in reader.pages).strip()
        except Exception:
            return ""

    return ""