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


def test_hard_shows_a_letter_in_every_word():
    puzzle = hand_puzzle(5, [("ABCDE", 0, 0, True), ("XYZ", 0, 2, False)])
    cells = starter_cells(puzzle, "hard")
    assert all(word_cells(pl) & cells for pl in puzzle.placed)


def test_hard_uses_a_crossing_letter_for_two_words():
    puzzle = hand_puzzle(5, [("ABCDE", 0, 0, True), ("XYZ", 0, 2, False)])
    assert len(starter_cells(puzzle, "hard")) == 1


def test_hard_adds_the_middle_of_a_long_word():
    puzzle = hand_puzzle(8, [("SPARROW", 0, 0, True), ("CAT", 2, 0, True)])
    cells = starter_cells(puzzle, "hard")
    assert (0, 3) in cells
    assert all(word_cells(pl) & cells for pl in puzzle.placed)


def test_easy_shows_two_letters_on_a_five_letter_word():
    puzzle = hand_puzzle(8, [("EAGLE", 0, 0, True), ("CAT", 2, 0, True)])
    cells = starter_cells(puzzle, "easy")
    assert (0, 0) in cells and (0, 2) in cells
    assert len([c for c in cells if c[0] == 2]) == 1  # 3-letter word keeps only its first letter
