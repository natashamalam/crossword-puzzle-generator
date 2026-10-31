import pytest

from crossword.data import Entry, load_entries


def write(tmp_path, body):
    p = tmp_path / "clues.csv"
    p.write_text("word,clue\n" + body, encoding="utf-8")
    return p


def test_load_valid_csv(tmp_path):
    p = write(tmp_path, 'cat,A pet that purrs\n"dog","A pet that barks"\n')
    assert load_entries(p) == [
        Entry("CAT", "A pet that purrs"),
        Entry("DOG", "A pet that barks"),
    ]


def test_duplicate_word_raises(tmp_path):
    p = write(tmp_path, "CAT,One\ncat,Two\n")
    with pytest.raises(ValueError, match="CAT"):
        load_entries(p)


def test_empty_clue_raises(tmp_path):
    p = write(tmp_path, "CAT,  \n")
    with pytest.raises(ValueError, match="CAT"):
        load_entries(p)


def test_non_letters_rejected(tmp_path):
    p = write(tmp_path, "CAT1,A clue\n")
    with pytest.raises(ValueError, match="CAT1"):
        load_entries(p)


@pytest.mark.parametrize("word", ["AB", "ABCDEFGHI"])
def test_length_bounds(tmp_path, word):
    p = write(tmp_path, f"{word},A clue\n")
    with pytest.raises(ValueError, match=word):
        load_entries(p)
