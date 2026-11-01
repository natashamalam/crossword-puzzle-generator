import pytest

from crossword.category import draft_puzzle, mode_for_next
from crossword.data import Entry

MIN_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)

WORDS = (
    "CAT DOG COW PIG HEN DUCK FROG FISH BEAR LION GOAT SHEEP HORSE "
    "MOUSE TIGER ZEBRA EAGLE OWL BEE ANT"
).split()


def test_mode_follows_approved_count():
    assert mode_for_next(0) == "easy"
    assert mode_for_next(19) == "easy"
    assert mode_for_next(20) == "medium"
    assert mode_for_next(34) == "medium"
    assert mode_for_next(35) == "hard"
    assert mode_for_next(49) == "hard"
    with pytest.raises(ValueError, match="50"):
        mode_for_next(50)


def test_easy_draft_leaves_out_a_word_longer_than_the_grid(tmp_path):
    png = tmp_path / "h.png"
    png.write_bytes(MIN_PNG)
    items = [Entry(w, f"A test clue for {w.lower()}", "bird", str(png)) for w in WORDS]
    items.append(Entry("SEAHORSE", "A horse that lives at sea", "nature", str(png)))
    draft = draft_puzzle(items, "easy", 0, seed=1)
    assert draft["mode"] == "easy" and draft["size"] == 7
    assert "SEAHORSE" in draft["left_out"]
    assert len(draft["placed"]) >= 6


def test_missing_image_on_a_placed_word_raises():
    items = [Entry(w, f"A test clue for {w.lower()}", "bird", "") for w in WORDS]
    with pytest.raises(ValueError, match="hint image is missing"):
        draft_puzzle(items, "easy", 0, seed=1)


def test_empty_image_reuses_approved_art(tmp_path):
    art = tmp_path / "hints"
    art.mkdir()
    for w in WORDS:
        (art / f"{w}.png").write_bytes(MIN_PNG)
    items = [Entry(w, f"A test clue for {w.lower()}", "bird", "") for w in WORDS]
    draft = draft_puzzle(items, "easy", 0, seed=1, art_dir=art)
    assert draft["placed"]
    assert all(item["image"] == str(art / f"{item['word']}.png") for item in draft["placed"])
