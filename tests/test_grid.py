from crossword.data import Entry
from crossword.grid import Placed, Puzzle, generate, validate

WORDS = (
    "CAT DOG COW PIG HEN DUCK FROG FISH BEAR LION GOAT SHEEP HORSE MOUSE "
    "TIGER ZEBRA EAGLE OWL BEE ANT"
).split()
ENTRIES = [Entry(w, f"clue for {w.lower()}") for w in WORDS]


def hand_puzzle(size, words):
    """words: list of (word, row, col, across)."""
    cells = [["."] * size for _ in range(size)]
    placed = []
    for n, (w, r, c, across) in enumerate(words, 1):
        for i, ch in enumerate(w):
            rr, cc = (r, c + i) if across else (r + i, c)
            cells[rr][cc] = ch
        placed.append(Placed(Entry(w, "x"), r, c, across, n))
    return Puzzle(size, cells, placed)


def test_generate_is_deterministic_for_seed():
    assert generate(ENTRIES, 9, seed=3) == generate(ENTRIES, 9, seed=3)


def test_generated_puzzle_validates():
    made = [p for p in (generate(ENTRIES, 9, seed=s) for s in range(20)) if p]
    assert made, "no seed produced a puzzle"
    for p in made:
        assert validate(p) == []
        assert len(p.placed) >= 6


def test_validate_flags_disconnected():
    p = hand_puzzle(9, [("CAT", 0, 0, True), ("DOG", 8, 0, True)])
    assert any("disconnected" in m for m in validate(p))


def test_validate_flags_unclued_run():
    p = hand_puzzle(7, [("CAT", 0, 0, True)])
    p.placed.clear()
    assert any("unclued" in m for m in validate(p))


def test_unplaceable_word_is_skipped():
    entries = ENTRIES + [Entry("ELEPHANT", "big")]
    made = [p for p in (generate(entries, 7, seed=s) for s in range(20)) if p]
    assert made
    for p in made:
        assert all(pl.entry.word != "ELEPHANT" for pl in p.placed)


def test_returns_none_when_fewer_than_6_words_fit():
    assert generate(ENTRIES[:3], 9, seed=1) is None
