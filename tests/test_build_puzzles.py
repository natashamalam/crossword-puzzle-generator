from collections import Counter

import pytest

from crossword.build_puzzles import MAX_REUSE, build_puzzles
from crossword.grid import validate
from tests.test_grid import ENTRIES


@pytest.fixture(scope="module")
def entries():
    return list(ENTRIES)


@pytest.fixture(scope="module")
def book(entries):
    return build_puzzles(entries, count=4, seed=1)


def test_returns_requested_count(book):
    assert len(book) == 4


def test_sizes_ramp_non_decreasing(book):
    sizes = [p.size for p in book]
    assert sizes == sorted(sizes)
    assert sizes[0] == 7 and sizes[-1] == 9


def test_all_puzzles_validate(book):
    for i, p in enumerate(book, 1):
        assert validate(p) == [], f"puzzle {i}"


def test_word_reuse_capped_at_3(book):
    uses = Counter(pl.entry.word for p in book for pl in p.placed)
    assert max(uses.values()) <= MAX_REUSE == 3


def test_raises_if_not_enough_words(entries):
    with pytest.raises(ValueError, match="not enough"):
        build_puzzles(entries, count=50, seed=1)


def test_puzzles_are_not_sparse(book):
    counts = [len(p.placed) for p in book]
    assert sum(counts) / len(counts) >= 8
    assert min(counts) >= 6
