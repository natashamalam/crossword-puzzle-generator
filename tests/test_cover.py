from pypdf import PdfReader

from crossword.cover import render_cover, spine_width_in


def test_spine_width_100_pages():
    assert abs(spine_width_in(100) - 0.2252) < 1e-6


def test_cover_dimensions(tmp_path):
    out = tmp_path / "c.pdf"
    w_in, h_in = render_cover("Zoo", "Sub", "Author Name", 100, out)
    page = PdfReader(out).pages[0]
    assert abs(float(page.mediabox.width) - w_in * 72) < 0.01
    assert abs(float(page.mediabox.height) - h_in * 72) < 0.01
    assert abs(w_in - (2 * 8.5 + 0.2252 + 0.25)) < 1e-6
    assert abs(h_in - 11.25) < 1e-6


def count_title(path):
    text = PdfReader(path).pages[0].extract_text()
    return text.count("Zoo")


def test_spine_text_skipped_under_79_pages(tmp_path):
    thin, thick = tmp_path / "thin.pdf", tmp_path / "thick.pdf"
    render_cover("Zoo", "Sub", "Author Name", 60, thin)
    render_cover("Zoo", "Sub", "Author Name", 100, thick)
    assert count_title(thick) == count_title(thin) + 1
