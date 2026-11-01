from dataclasses import replace

from pypdf import PdfReader

from build import build
from crossword.cover import spine_width_in
from crossword.scan import scan_text
from crossword.store import save_puzzle
from tests.test_grid import hand_puzzle


def test_build_creates_both_pdfs(tmp_path):
    puzzles = tmp_path / "puzzles"
    puzzles.mkdir()
    puzzle = replace(hand_puzzle(8, [("CROW", 0, 0, True), ("CAT", 1, 0, True)]), mode="easy")
    save_puzzle(puzzles / "001.json", puzzle)
    out = tmp_path / "out"
    pages = build(out, puzzles)
    interior, cover = out / "interior.pdf", out / "cover.pdf"
    assert interior.exists() and cover.exists()
    assert len(PdfReader(interior).pages) == pages
    width_pt = float(PdfReader(cover).pages[0].mediabox.width)
    assert abs(width_pt / 72 - (2 * 8.5 + 0.25 + spine_width_in(pages))) < 0.001


def test_empty_book_still_builds_front_matter(tmp_path):
    pages = build(tmp_path / "out", tmp_path / "puzzles")
    assert pages >= 24 and pages % 2 == 0
    assert (tmp_path / "out" / "interior.pdf").exists()


def test_scan_flags_banned_term(tmp_path):
    f = tmp_path / "a.md"
    f.write_text("A fun Acme Toys puzzle book", encoding="utf-8")
    assert scan_text([f], ["acme toys"]) == [f"{f}: acme toys"]


def test_scan_clean_returns_empty(tmp_path):
    f = tmp_path / "a.md"
    f.write_text("A fun puzzle book about cats", encoding="utf-8")
    assert scan_text([f], ["acme toys"]) == []
