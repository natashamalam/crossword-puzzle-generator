from crossword.alternates import accepted_alternates
from crossword.grid import Puzzle
from tests.test_grid import hand_puzzle


def test_alternate_must_agree_with_crossing_letters():
    puzzle = hand_puzzle(6, [("PIG", 0, 0, True), ("PEN", 0, 0, False)])
    assert accepted_alternates(puzzle, {"PIG": ["PUG"]}) == [(1, True, ["PUG"])]  # P shared
    assert accepted_alternates(puzzle, {"PIG": ["HOG"]}) == []  # H breaks the shared P


def test_alternate_must_keep_starter_letters():
    base = hand_puzzle(6, [("PIG", 0, 0, True), ("COW", 3, 0, True)])
    puzzle = Puzzle(base.size, base.cells, base.placed, "easy", frozenset({(0, 0)}))
    assert accepted_alternates(puzzle, {"PIG": ["HOG"]}) == []
    puzzle = Puzzle(base.size, base.cells, base.placed, "easy", frozenset({(0, 1)}))
    assert accepted_alternates(puzzle, {"PIG": ["PIG"]}) == []  # same word is not an alternative


def test_alternate_must_have_same_length_and_not_repeat_another_answer():
    puzzle = hand_puzzle(6, [("PIG", 0, 0, True), ("HOG", 3, 0, True)])
    assert accepted_alternates(puzzle, {"PIG": ["HOG", "PIGS"]}) == []
