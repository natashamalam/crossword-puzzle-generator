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


def _hard_cells(puzzle: Puzzle) -> set[tuple[int, int]]:
    """Fewest letters that still show one letter in every word, using crossings where
    possible, plus the middle letter of every long (7-8 letter) word."""
    bare = list(puzzle.placed)
    cells: set[tuple[int, int]] = set()
    while bare:
        users: dict[tuple[int, int], int] = {}
        for pl in bare:
            for cell in word_cells(pl):
                users[cell] = users.get(cell, 0) + 1
        best = max(sorted(users), key=lambda cell: users[cell])
        cells.add(best)
        bare = [pl for pl in bare if best not in word_cells(pl)]
    for pl in puzzle.placed:
        if len(pl.entry.word) >= 7:
            cells.add(_at(pl, len(pl.entry.word) // 2))
    return cells


def starter_cells(puzzle: Puzzle, mode: str) -> set[tuple[int, int]]:
    if mode == "easy":
        cells = set()
        for pl in puzzle.placed:
            cells.add(_at(pl, 0))
            if len(pl.entry.word) >= 5:
                cells.add(_at(pl, len(pl.entry.word) // 2))
        return cells
    if mode == "medium":
        return {_at(pl, len(pl.entry.word) // 2) for pl in puzzle.placed}
    if mode == "hard":
        return _hard_cells(puzzle)
    raise ValueError(f"unknown mode {mode}")
