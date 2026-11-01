from crossword.starters import starter_cells, word_cells
from tests.test_grid import hand_puzzle


def test_easy_shows_first_and_middle_on_a_long_word():
    puzzle = hand_puzzle(8, [("SPARROW", 0, 0, True), ("CAT", 1, 0, True)])
    cells = starter_cells(puzzle, "easy")
    assert (0, 0) in cells and (0, 3) in cells
    assert (1, 0) in cells


def test_medium_selects_only_the_middle_letter():
    puzzle = hand_puzzle(8, [("SPARROW", 0, 0, True)])
    cells = starter_cells(puzzle, "medium")
    assert cells == {(0, 3)}


def test_hard_crossing_still_leaves_one_word_bare():
    puzzle = hand_puzzle(5, [("ABCDE", 0, 0, True), ("XYZ", 0, 2, False)])
    cells = starter_cells(puzzle, "hard")
    bare = [pl for pl in puzzle.placed if not (word_cells(pl) & cells)]
    assert bare
