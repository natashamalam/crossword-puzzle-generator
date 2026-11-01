from crossword.grid import Placed, Puzzle


def word_cells(pl: Placed) -> set[tuple[int, int]]:
    cells = set()
    for i in range(len(pl.entry.word)):
        if pl.across:
            cells.add((pl.row, pl.col + i))
        else:
            cells.add((pl.row + i, pl.col))
    return cells


def _at(pl: Placed, index: int) -> tuple[int, int]:
    if pl.across:
        return pl.row, pl.col + index
    return pl.row + index, pl.col


def _covered(puzzle: Puzzle, cells: set[tuple[int, int]]) -> bool:
    return all(word_cells(pl) & cells for pl in puzzle.placed)


def _trim_hard(puzzle: Puzzle, cells: set[tuple[int, int]]) -> set[tuple[int, int]]:
    cells = set(cells)
    while cells and _covered(puzzle, cells):
        removable = []
        for cell in sorted(cells):
            users = [pl for pl in puzzle.placed if cell in word_cells(pl)]
            if users and all(len(word_cells(pl) & cells) > 1 for pl in users):
                removable.append(cell)
        victim = removable[0] if removable else sorted(cells)[0]
        cells.remove(victim)
    return cells


def starter_cells(puzzle: Puzzle, mode: str) -> set[tuple[int, int]]:
    if mode == "easy":
        cells = set()
        for pl in puzzle.placed:
            cells.add(_at(pl, 0))
            if len(pl.entry.word) >= 6:
                cells.add(_at(pl, len(pl.entry.word) // 2))
        return cells
    if mode == "medium":
        return {_at(pl, len(pl.entry.word) // 2) for pl in puzzle.placed}
    if mode == "hard":
        ordered = sorted(puzzle.placed, key=lambda pl: (pl.number, 0 if pl.across else 1))
        cells = {_at(pl, len(pl.entry.word) // 2) for pl in ordered[::2]}
        return _trim_hard(puzzle, cells)
    raise ValueError(f"unknown mode {mode}")
