import json
from dataclasses import replace

import pytest

from crossword.category import apply_draft, draft_puzzle, mode_for_next
from crossword.data import Entry
from crossword.store import load_puzzle, save_puzzle
from tests.test_grid import hand_puzzle

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
    assert mode_for_next(99) == "hard"
    with pytest.raises(ValueError, match="100"):
        mode_for_next(100)


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


def test_apply_without_approved_changes_nothing(tmp_path):
    draft = tmp_path / "draft.json"
    draft.write_text("{}", encoding="utf-8")
    puzzles, art, out = tmp_path / "puzzles", tmp_path / "art", tmp_path / "out"
    with pytest.raises(SystemExit):
        apply_draft(draft, puzzles, art, out, approved=False)
    assert not puzzles.exists() and not art.exists() and not out.exists()


def test_apply_stops_when_caption_differs(tmp_path):
    puzzles, art, out = tmp_path / "puzzles", tmp_path / "art", tmp_path / "out"
    puzzles.mkdir()
    stored = hand_puzzle(8, [("CAT", 0, 0, True)])
    stored.placed[0] = replace(stored.placed[0], entry=Entry("CAT", "A small pet", "animal", ""))
    save_puzzle(puzzles / "001.json", stored)
    png = tmp_path / "CAT.png"
    png.write_bytes(MIN_PNG)
    draft = tmp_path / "draft.json"
    draft.write_text(json.dumps({
        "mode": "easy",
        "size": 8,
        "cells": [["."] * 8 for _ in range(8)],
        "starters": [],
        "placed": [{
            "word": "CAT",
            "clue": "A barn pet",
            "category": "animal",
            "image": str(png),
            "row": 0,
            "col": 0,
            "across": True,
            "number": 1,
        }],
    }), encoding="utf-8")
    with pytest.raises(ValueError, match="which version to keep"):
        apply_draft(draft, puzzles, art, out, approved=True)
    assert load_puzzle(puzzles / "001.json").placed[0].entry.clue == "A small pet"


def test_apply_copies_puzzle_art_and_pdfs(tmp_path):
    png = tmp_path / "h.png"
    png.write_bytes(MIN_PNG)
    items = [Entry(w, f"A test clue for {w.lower()}", "bird", str(png)) for w in WORDS]
    body = draft_puzzle(items, "easy", 0, seed=1)
    draft = tmp_path / "draft.json"
    draft.write_text(json.dumps(body), encoding="utf-8")
    puzzles, art, out = tmp_path / "puzzles", tmp_path / "art", tmp_path / "out"
    pages = apply_draft(draft, puzzles, art, out, approved=True)
    assert (puzzles / "001.json").exists()
    assert (art / "DOG.png").read_bytes() == MIN_PNG
    assert (out / "interior.pdf").exists() and (out / "cover.pdf").exists()
    assert pages >= 24


def test_named_mode_refuses_puzzle_51(tmp_path):
    png = tmp_path / "h.png"
    png.write_bytes(MIN_PNG)
    items = [Entry(w, f"A test clue for {w.lower()}", "bird", str(png)) for w in WORDS]
    with pytest.raises(ValueError, match="100"):
        draft_puzzle(items, "easy", 100, seed=1)


def test_apply_refuses_puzzle_51(tmp_path):
    puzzles = tmp_path / "puzzles"
    puzzles.mkdir()
    stored = hand_puzzle(8, [("CAT", 0, 0, True)])
    for n in range(1, 101):
        save_puzzle(puzzles / f"{n:03d}.json", stored)
    png = tmp_path / "h.png"
    png.write_bytes(MIN_PNG)
    body = draft_puzzle([Entry(w, f"A test clue for {w.lower()}", "bird", str(png)) for w in WORDS], "easy", 0, seed=1)
    draft = tmp_path / "draft.json"
    draft.write_text(json.dumps(body), encoding="utf-8")
    with pytest.raises(ValueError, match="100"):
        apply_draft(draft, puzzles, tmp_path / "art", tmp_path / "out", approved=True)
    assert not (puzzles / "101.json").exists()


def test_apply_leaves_no_puzzle_when_render_fails(tmp_path, monkeypatch):
    png = tmp_path / "h.png"
    png.write_bytes(MIN_PNG)
    items = [Entry(w, f"A test clue for {w.lower()}", "bird", str(png)) for w in WORDS]
    draft = tmp_path / "draft.json"
    draft.write_text(json.dumps(draft_puzzle(items, "easy", 0, seed=1)), encoding="utf-8")
    puzzles = tmp_path / "puzzles"

    def boom(*_args, **_kwargs):
        raise ValueError("Puzzle 1: clues do not fit on the page, shorten them")

    monkeypatch.setattr("build.render_interior", boom)
    with pytest.raises(ValueError, match="do not fit"):
        apply_draft(draft, puzzles, tmp_path / "art", tmp_path / "out", approved=True)
    assert not puzzles.exists() or not list(puzzles.glob("*.json"))
