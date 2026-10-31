import re
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
BANNED_FILE = ROOT / "data" / "banned_terms.txt"
TEXT_SUFFIXES = {".py", ".md", ".csv", ".txt"}


def _read(path: Path) -> str:
    if path.suffix == ".pdf":
        return " ".join(page.extract_text() for page in PdfReader(path).pages)
    return path.read_text(encoding="utf-8")


def scan_text(paths: list[Path], banned: list[str]) -> list[str]:
    """Return "path: term" for every banned term (whole words, any case) found."""
    hits = []
    for path in paths:
        text = _read(path)
        for term in banned:
            if re.search(rf"\b{re.escape(term)}\b", text, re.IGNORECASE):
                hits.append(f"{path}: {term}")
    return hits


def main(argv: list[str]) -> int:
    banned = [t.strip() for t in BANNED_FILE.read_text(encoding="utf-8").splitlines()
              if t.strip() and not t.startswith("#")]
    targets = [Path(a) for a in argv] or [ROOT / "data", ROOT / "docs", ROOT / "crossword", ROOT / "out"]
    files = []
    for t in targets:
        found = [t] if t.is_file() else sorted(t.rglob("*")) if t.exists() else []
        files += [f for f in found if f.is_file() and f != BANNED_FILE
                  and f.suffix in TEXT_SUFFIXES | {".pdf"}]
    hits = scan_text(files, banned)
    print(f"scanned {len(files)} files for {len(banned)} terms")
    for hit in hits:
        print("HIT", hit)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
