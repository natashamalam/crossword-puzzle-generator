from dataclasses import replace

from pypdf import PdfReader
from reportlab.pdfbase.pdfmetrics import stringWidth

from crossword.data import Entry
from crossword.grid import generate
from crossword.render import FONT, register_fonts, render_interior, wrap_text
from tests.test_grid import ENTRIES


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
