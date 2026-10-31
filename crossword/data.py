import csv
from dataclasses import dataclass
from pathlib import Path

MIN_LEN, MAX_LEN = 3, 8


@dataclass(frozen=True)
class Entry:
    word: str
    clue: str


def load_entries(path: Path) -> list[Entry]:
    entries: list[Entry] = []
    seen: set[str] = set()
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            word = (row["word"] or "").strip().upper()
            clue = (row["clue"] or "").strip()
            if not (word.isascii() and word.isalpha()):
                raise ValueError(f"{word}: word must contain only letters A-Z")
            if not MIN_LEN <= len(word) <= MAX_LEN:
                raise ValueError(f"{word}: length must be {MIN_LEN}-{MAX_LEN}")
            if not clue:
                raise ValueError(f"{word}: clue is empty")
            if word in seen:
                raise ValueError(f"{word}: duplicate word")
            seen.add(word)
            entries.append(Entry(word, clue))
    return entries
