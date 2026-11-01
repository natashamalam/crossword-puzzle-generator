from dataclasses import replace

from crossword.starters import starter_cells
from crossword.store import load_puzzle, save_puzzle
from tests.test_grid import hand_puzzle


def test_round_trip_keeps_grid_mode_and_starters(tmp_path):
    puzzle = replace(
        hand_puzzle(8, [("SPARROW", 0, 0, True), ("CAT", 1, 0, True)]),
        mode="easy",
    )
    puzzle = replace(puzzle, starters=frozenset(starter_cells(puzzle, "easy")))
    path = tmp_path / "001.json"
    save_puzzle(path, puzzle)
    assert load_puzzle(path) == puzzle
