import random
from dataclasses import dataclass, field

from crossword.data import Entry

EMPTY = "."
MIN_WORDS = 6
MAX_TRIES_PER_WORD = 200


@dataclass
class Placed:
    entry: Entry
    row: int
    col: int
    across: bool
    number: int


@dataclass
class Puzzle:
    size: int
    cells: list[list[str]]
    placed: list[Placed]
    mode: str = ""
    starters: frozenset[tuple[int, int]] = field(default_factory=frozenset)


def _runs(cells: list[list[str]]) -> set[tuple[int, int, bool, str]]:
    """Every maximal run of 2+ letters as (row, col, across, word)."""
    size = len(cells)
    runs = set()
    for across in (True, False):
        for a in range(size):
            b = 0
            while b < size:
                r, c = (a, b) if across else (b, a)
                if cells[r][c] == EMPTY:
                    b += 1
                    continue
                start, letters = b, []
                while b < size:
                    rr, cc = (a, b) if across else (b, a)
                    if cells[rr][cc] == EMPTY:
                        break
                    letters.append(cells[rr][cc])
                    b += 1
                if len(letters) >= 2:
                    sr, sc = (a, start) if across else (start, a)
                    runs.add((sr, sc, across, "".join(letters)))
    return runs


def _write(cells, word, row, col, across):
    new = [line[:] for line in cells]
    for i, ch in enumerate(word):
        r, c = (row, col + i) if across else (row + i, col)
        new[r][c] = ch
    return new


def _candidates(cells, word, size):
    """Placements that cross exactly the existing letters and keep the grid clean."""
    found = []
    for across in (True, False):
        for row in range(size):
            for col in range(size):
                end_r, end_c = (row, col + len(word) - 1) if across else (row + len(word) - 1, col)
                if end_r >= size or end_c >= size:
                    continue
                crossings = 0
                ok = True
                for i, ch in enumerate(word):
                    r, c = (row, col + i) if across else (row + i, col)
                    have = cells[r][c]
                    if have == EMPTY:
                        continue
                    if have != ch:
                        ok = False
                        break
                    crossings += 1
                if ok and crossings >= 1:
                    found.append((row, col, across))
    return found


def _number(placed: list[tuple[Entry, int, int, bool]]) -> list[Placed]:
    starts = sorted({(r, c) for _, r, c, _ in placed})
    numbers = {pos: n for n, pos in enumerate(starts, 1)}
    out = [Placed(e, r, c, a, numbers[(r, c)]) for e, r, c, a in placed]
    out.sort(key=lambda p: (not p.across, p.number))
    return out


def generate(entries: list[Entry], size: int, seed: int) -> Puzzle | None:
    rng = random.Random(seed)
    pool = [e for e in entries if len(e.word) <= size]
    rng.shuffle(pool)
    pool.sort(key=lambda e: -len(e.word))
    if not pool:
        return None

    first = pool[0]
    cells = [[EMPTY] * size for _ in range(size)]
    row, col = size // 2, (size - len(first.word)) // 2
    cells = _write(cells, first.word, row, col, True)
    placed = [(first, row, col, True)]
    used = {first.word}

    progress = True
    while progress:  # new letters can open crossings for words skipped earlier
        progress = False
        for entry in pool[1:]:
            if entry.word in used:
                continue
            options = _candidates(cells, entry.word, size)
            rng.shuffle(options)
            for r, c, across in options[:MAX_TRIES_PER_WORD]:
                trial = _write(cells, entry.word, r, c, across)
                expected = {(pr, pc, pa, e.word) for e, pr, pc, pa in placed}
                expected.add((r, c, across, entry.word))
                if _runs(trial) == expected:
                    cells = trial
                    placed.append((entry, r, c, across))
                    used.add(entry.word)
                    progress = True
                    break

    if len(placed) < MIN_WORDS:
        return None
    return Puzzle(size, cells, _number(placed))


def validate(p: Puzzle) -> list[str]:
    problems: list[str] = []
    claimed = {(pl.row, pl.col, pl.across, pl.entry.word) for pl in p.placed}
    for pl in p.placed:
        for i, ch in enumerate(pl.entry.word):
            r, c = (pl.row, pl.col + i) if pl.across else (pl.row + i, pl.col)
            if not (0 <= r < p.size and 0 <= c < p.size) or p.cells[r][c] != ch:
                problems.append(f"{pl.entry.word}: letters do not match grid")
                break
    for run in sorted(_runs(p.cells) - claimed):
        problems.append(f"unclued run {run[3]} at ({run[0]},{run[1]})")
    words = [pl.entry.word for pl in p.placed]
    for w in sorted({w for w in words if words.count(w) > 1}):
        problems.append(f"duplicate word {w}")

    letters = {(r, c) for r in range(p.size) for c in range(p.size) if p.cells[r][c] != EMPTY}
    if letters:
        stack, seen = [next(iter(sorted(letters)))], set()
        while stack:
            r, c = stack.pop()
            if (r, c) in seen:
                continue
            seen.add((r, c))
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if (nr, nc) in letters:
                    stack.append((nr, nc))
        if seen != letters:
            problems.append("grid is disconnected")
    return problems
