"""Alternative answers: other words that also fit a clue and keep the filled grid valid."""
import json
from pathlib import Path

from crossword.grid import Puzzle
from crossword.starters import word_cells


def load_alternates(path: Path) -> dict[str, list[str]]:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {word.upper(): [alt.upper() for alt in alts] for word, alts in data.items()}


def accepted_alternates(puzzle: Puzzle, alternates: dict[str, list[str]]) -> list[tuple[int, bool, list[str]]]:
    """(number, across, [alternatives]) for every clue that has an alternative the grid allows.

    An alternative must have the same length, differ from every answer in the puzzle, and agree with
    each letter that is shared with a crossing word or printed as a starter letter.
    """
    answers = {pl.entry.word for pl in puzzle.placed}
    cell_users: dict[tuple[int, int], int] = {}
    for pl in puzzle.placed:
        for cell in word_cells(pl):
            cell_users[cell] = cell_users.get(cell, 0) + 1
    out = []
    for pl in puzzle.placed:
        word = pl.entry.word
        cells = sorted(word_cells(pl), key=lambda rc: (rc[0], rc[1]))
        good = []
        for alt in alternates.get(word, []):
            if len(alt) != len(word) or alt == word or alt in answers:
                continue
            fixed = [i for i, rc in enumerate(cells) if cell_users[rc] > 1 or rc in puzzle.starters]
            if all(alt[i] == word[i] for i in fixed):
                good.append(alt)
        if good:
            out.append((pl.number, pl.across, good))
    return sorted(out)
