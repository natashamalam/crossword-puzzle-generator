import json
from pathlib import Path

from crossword.data import Entry
from crossword.grid import Placed, Puzzle


def save_puzzle(path: Path, puzzle: Puzzle) -> None:
    data = {
        "mode": puzzle.mode,
        "size": puzzle.size,
        "cells": puzzle.cells,
        "starters": [list(pair) for pair in sorted(puzzle.starters)],
        "placed": [
            {
                "word": pl.entry.word,
                "clue": pl.entry.clue,
                "category": pl.entry.category,
                "image": pl.entry.image,
                "row": pl.row,
                "col": pl.col,
                "across": pl.across,
                "number": pl.number,
            }
            for pl in puzzle.placed
        ],
    }
    path.write_text(json.dumps(data), encoding="utf-8")


def load_puzzle(path: Path) -> Puzzle:
    data = json.loads(path.read_text(encoding="utf-8"))
    placed = [
        Placed(
            Entry(item["word"], item["clue"], item.get("category", ""), item.get("image", "")),
            item["row"],
            item["col"],
            item["across"],
            item["number"],
        )
        for item in data["placed"]
    ]
    return Puzzle(
        data["size"],
        data["cells"],
        placed,
        data.get("mode", ""),
        frozenset(tuple(pair) for pair in data.get("starters", [])),
    )


def load_puzzles(directory: Path) -> list[Puzzle]:
    if not directory.is_dir():
        return []
    return [load_puzzle(path) for path in sorted(directory.glob("*.json"))]
