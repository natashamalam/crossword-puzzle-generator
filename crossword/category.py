from pathlib import Path

from crossword.data import Entry, check_word, validate_captions
from crossword.grid import generate
from crossword.starters import starter_cells

SIZES = {"easy": 7, "medium": 8, "hard": 9}


def mode_for_next(approved_count: int) -> str:
    number = approved_count + 1
    if number > 50:
        raise ValueError("book already has 50 puzzles")
    if number <= 20:
        return "easy"
    if number <= 35:
        return "medium"
    return "hard"


def grid_size(mode: str) -> int:
    return SIZES[mode]


def _placed_dict(pl) -> dict:
    return {
        "word": pl.entry.word,
        "clue": pl.entry.clue,
        "category": pl.entry.category,
        "image": pl.entry.image,
        "row": pl.row,
        "col": pl.col,
        "across": pl.across,
        "number": pl.number,
    }


def draft_puzzle(
    items: list[Entry],
    mode: str | None,
    approved_count: int,
    seed: int,
    art_dir: Path | None = None,
) -> dict:
    rejected: list[str] = []
    accepted: list[Entry] = []
    seen: set[str] = set()
    for raw in items:
        word = raw.word.strip().upper()
        entry = Entry(word, raw.clue, raw.category, raw.image)
        if word in seen:
            rejected.append(f"{word}: duplicate word")
            continue
        seen.add(word)
        problem = check_word(word)
        if problem:
            rejected.append(problem)
            continue
        image = entry.image
        if not image and art_dir is not None:
            stored = art_dir / f"{word}.png"
            if stored.is_file():
                image = str(stored)
        accepted.append(Entry(word, entry.clue, entry.category, image))
    validate_captions(accepted)
    if mode is None:
        mode = mode_for_next(approved_count)
    size = grid_size(mode)
    puzzle = generate(accepted, size, seed)
    if puzzle is None:
        raise ValueError("not enough words to build a puzzle")
    placed_words = {pl.entry.word for pl in puzzle.placed}
    for pl in puzzle.placed:
        path = pl.entry.image
        if not path or not Path(path).is_file():
            raise ValueError(f"{pl.entry.word}: hint image is missing")
    return {
        "mode": mode,
        "size": size,
        "cells": puzzle.cells,
        "placed": [_placed_dict(pl) for pl in puzzle.placed],
        "starters": [list(pair) for pair in sorted(starter_cells(puzzle, mode))],
        "rejected": rejected,
        "left_out": [entry.word for entry in accepted if entry.word not in placed_words],
    }
