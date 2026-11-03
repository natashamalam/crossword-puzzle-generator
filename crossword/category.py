import argparse
import json
import shutil
import tempfile
from pathlib import Path

from crossword.data import Entry, check_word, validate_captions
from crossword.grid import MIN_WORDS, Placed, Puzzle, generate
from crossword.starters import starter_cells
from crossword.store import load_puzzles, save_puzzle

SIZES = {"easy": 7, "medium": 8, "hard": 9}
MAX_PUZZLES = 100


def mode_for_next(approved_count: int) -> str:
    number = approved_count + 1
    if number > MAX_PUZZLES:
        raise ValueError(f"book already has {MAX_PUZZLES} puzzles")
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
    min_words: int | None = None,
    free_start: bool = False,
) -> dict:
    if approved_count >= MAX_PUZZLES:
        raise ValueError(f"book already has {MAX_PUZZLES} puzzles")
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
    puzzle = generate(accepted, size, seed, min_words or MIN_WORDS, free_start)
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


def _puzzle_from_draft(draft: dict, images: dict[str, str]) -> Puzzle:
    placed = []
    for item in draft["placed"]:
        image = images.get(item["word"], item.get("image", ""))
        placed.append(
            Placed(
                Entry(item["word"], item["clue"], item.get("category", ""), image),
                item["row"],
                item["col"],
                item["across"],
                item["number"],
            )
        )
    return Puzzle(
        draft["size"],
        draft["cells"],
        placed,
        draft.get("mode", ""),
        frozenset(tuple(pair) for pair in draft.get("starters", [])),
    )


def apply_draft(
    draft_path: Path,
    puzzles_dir: Path,
    art_dir: Path,
    out_dir: Path,
    approved: bool,
) -> int:
    if not approved:
        raise SystemExit(2)
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    existing = load_puzzles(puzzles_dir)
    if len(existing) >= MAX_PUZZLES:
        raise ValueError(f"book already has {MAX_PUZZLES} puzzles")
    stored = {pl.entry.word: pl.entry for puzzle in existing for pl in puzzle.placed}
    for item in draft["placed"]:
        word = item["word"]
        previous = stored.get(word)
        if previous is not None and previous.clue != item["clue"]:
            raise ValueError(f"{word}: which version to keep")
        approved_png = art_dir / f"{word}.png"
        source = Path(item.get("image", ""))
        if (
            previous is not None
            and approved_png.is_file()
            and source.is_file()
            and approved_png.read_bytes() != source.read_bytes()
        ):
            raise ValueError(f"{word}: which version to keep")
    from build import build

    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        tmp_puzzles = tmp_root / "puzzles"
        tmp_art = tmp_root / "art"
        tmp_out = tmp_root / "out"
        tmp_puzzles.mkdir()
        tmp_art.mkdir()
        if puzzles_dir.is_dir():
            for path in sorted(puzzles_dir.glob("*.json")):
                shutil.copy(path, tmp_puzzles / path.name)
        images = {}
        for item in draft["placed"]:
            word = item["word"]
            source = Path(item.get("image", ""))
            dest = tmp_art / f"{word}.png"
            if source.is_file():
                dest.write_bytes(source.read_bytes())
            images[word] = str(dest)
        save_puzzle(tmp_puzzles / f"{len(existing) + 1:03d}.json", _puzzle_from_draft(draft, images))
        pages = build(tmp_out, tmp_puzzles)
        art_dir.mkdir(parents=True, exist_ok=True)
        final_images = {}
        for word, src in images.items():
            final = art_dir / f"{word}.png"
            source = Path(src)
            if source.is_file() and source.resolve() != final.resolve():
                final.write_bytes(source.read_bytes())
            final_images[word] = str(final)
        puzzles_dir.mkdir(parents=True, exist_ok=True)
        save_puzzle(
            puzzles_dir / f"{len(existing) + 1:03d}.json",
            _puzzle_from_draft(draft, final_images),
        )
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(tmp_out / "interior.pdf", out_dir / "interior.pdf")
        shutil.copy(tmp_out / "cover.pdf", out_dir / "cover.pdf")
    return pages


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m crossword.category")
    sub = parser.add_subparsers(dest="cmd", required=True)
    draft_cmd = sub.add_parser("draft")
    draft_cmd.add_argument("--input", type=Path, required=True)
    draft_cmd.add_argument("--seed", type=int, default=1)
    draft_cmd.add_argument("--id", required=True)
    apply_cmd = sub.add_parser("apply")
    apply_cmd.add_argument("draft", type=Path)
    apply_cmd.add_argument("--approved", action="store_true")
    args = parser.parse_args(argv)
    if args.cmd == "draft":
        request = json.loads(args.input.read_text(encoding="utf-8"))
        items = [
            Entry(item["word"], item["caption"], item["category"], item.get("image", ""))
            for item in request["items"]
        ]
        result = draft_puzzle(
            items,
            request.get("mode"),
            len(load_puzzles(Path("data/puzzles"))),
            args.seed,
            Path("art/hints"),
            request.get("min_words"),
            bool(request.get("free_start")),
        )
        out = Path("drafts") / f"{args.id}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result), encoding="utf-8")
        print(out)
        return 0
    pages = apply_draft(
        args.draft,
        Path("data/puzzles"),
        Path("art/hints"),
        Path("generated_content"),
        args.approved,
    )
    print(pages)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
