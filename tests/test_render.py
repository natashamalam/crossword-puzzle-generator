from dataclasses import replace

import pytest

from pypdf import PdfReader
from reportlab.pdfbase.pdfmetrics import stringWidth

from crossword.data import Entry
from crossword.grid import Placed, Puzzle, generate
from crossword.render import FONT, register_fonts, render_interior, wrap_text
from crossword.starters import starter_cells
from tests.test_grid import ENTRIES

MIN_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


def two_puzzles():
    made = (generate(ENTRIES, 9, seed=s) for s in range(50))
    return [p for p in made if p][:2]


def test_page_count_even_and_at_least_24(tmp_path):
    out = tmp_path / "i.pdf"
    n = render_interior(two_puzzles(), "Test Book", out)
    assert n == len(PdfReader(out).pages)
    assert n % 2 == 0 and n >= 24


def test_page_size_is_letter(tmp_path):
    out = tmp_path / "i.pdf"
    render_interior(two_puzzles(), "Test Book", out)
    for page in PdfReader(out).pages:
        assert (float(page.mediabox.width), float(page.mediabox.height)) == (612, 792)


def test_solutions_pages_present(tmp_path):
    out = tmp_path / "i.pdf"
    render_interior(two_puzzles(), "Test Book", out)
    text = " ".join(p.extract_text() for p in PdfReader(out).pages)
    assert "Solutions" in text and "How to Play" in text


def test_wrap_text_fits_width():
    register_fonts()
    clue = "word " * 40
    lines = wrap_text(clue, FONT, 14, 200)
    assert len(lines) > 1
    assert all(stringWidth(line, FONT, 14) <= 200 for line in lines)


def test_long_clue_stays_inside_margins(tmp_path):
    p = generate(ENTRIES, 9, seed=1)
    p.placed[0] = replace(p.placed[0], entry=Entry(p.placed[0].entry.word, "very long clue " * 14))
    out = tmp_path / "i.pdf"
    render_interior([p], "Test Book", out)
    xs = []
    for page in PdfReader(out).pages:
        page.extract_text(visitor_text=lambda t, cm, tm, fd, fs: xs.append(tm[4]) if t.strip() else None)
    assert xs and min(xs) >= 36 and max(xs) <= 612 - 36


def test_clues_too_long_to_fit_raise_with_puzzle_number(tmp_path):
    p = generate(ENTRIES, 9, seed=1)
    p.placed[:] = [replace(pl, entry=Entry(pl.entry.word, "word " * 800)) for pl in p.placed]
    with pytest.raises(ValueError, match="Puzzle 1"):
        render_interior([p], "Test Book", tmp_path / "i.pdf")


def test_puzzle_page_shows_mode_caption_and_image(tmp_path):
    png = tmp_path / "CROW.png"
    png.write_bytes(MIN_PNG)
    placed = [
        Placed(Entry("CROW", "A black bird", "bird", str(png)), 0, 0, True, 1),
        Placed(Entry("CAT", "A small pet", "animal", str(png)), 1, 0, True, 2),
    ]
    cells = [["."] * 8 for _ in range(8)]
    for pl in placed:
        for i, ch in enumerate(pl.entry.word):
            cells[pl.row][pl.col + i] = ch
    puzzle = Puzzle(8, cells, placed, mode="easy")
    puzzle = replace(puzzle, starters=frozenset(starter_cells(puzzle, "easy")))
    out = tmp_path / "i.pdf"
    render_interior([puzzle], "Category Crosswords for Kids", out)
    reader = PdfReader(out)
    how = " ".join(reader.pages[2].extract_text().split())
    assert "Use the picture, the caption, and any letters already in the grid." in how
    puzzle_page = reader.pages[3]
    text = puzzle_page.extract_text()
    assert "Easy" in text and "A black bird" in text
    assert len(puzzle_page.images) >= 1
    solution = next(p for p in reader.pages if "Solutions" in (p.extract_text() or ""))
    assert len(solution.images) == 0


def test_hard_puzzle_with_six_picture_clues_prints(tmp_path):
    png = tmp_path / "a.png"
    png.write_bytes(MIN_PNG)
    words = ["CROW", "SWAN", "DOVE", "FINCH", "CRANE", "ROBIN"]
    placed = []
    cells = [["."] * 9 for _ in range(9)]
    for i, word in enumerate(words):
        placed.append(Placed(Entry(word, f"A test bird {word.lower()}", "bird", str(png)), i, 0, True, i + 1))
        for j, ch in enumerate(word):
            cells[i][j] = ch
    puzzle = Puzzle(9, cells, placed, mode="hard")
    out = tmp_path / "i.pdf"
    render_interior([puzzle], "Category Crosswords for Kids", out)
    text = " ".join((page.extract_text() or "") for page in PdfReader(out).pages)
    assert "Hard" in text and "A test bird crow" in text
