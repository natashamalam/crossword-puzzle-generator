from pypdf import PdfReader

from build import build
from crossword.cover import spine_width_in
from crossword.scan import scan_text


def test_build_creates_both_pdfs(tmp_path):
    pages = build(tmp_path, count=10)
    interior, cover = tmp_path / "interior.pdf", tmp_path / "cover.pdf"
    assert interior.exists() and cover.exists()
    assert len(PdfReader(interior).pages) == pages
    width_pt = float(PdfReader(cover).pages[0].mediabox.width)
    assert abs(width_pt / 72 - (2 * 8.5 + 0.25 + spine_width_in(pages))) < 0.001


def test_scan_flags_banned_term(tmp_path):
    f = tmp_path / "a.md"
    f.write_text("A fun Acme Toys puzzle book", encoding="utf-8")
    assert scan_text([f], ["acme toys"]) == [f"{f}: acme toys"]


def test_scan_clean_returns_empty(tmp_path):
    f = tmp_path / "a.md"
    f.write_text("A fun puzzle book about cats", encoding="utf-8")
    assert scan_text([f], ["acme toys"]) == []
