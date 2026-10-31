from pathlib import Path

from reportlab.pdfgen.canvas import Canvas

from crossword.render import FONT, register_fonts, wrap_text

TRIM_W, TRIM_H = 8.5, 11.0
BLEED = 0.125
SPINE_PER_PAGE = 0.002252  # black-and-white interior, white paper
MIN_SPINE_TEXT_PAGES = 79
PT = 72

BACKGROUND = (0.99, 0.96, 0.86)
INK = (0.12, 0.16, 0.30)
CELL_COLORS = [(0.96, 0.62, 0.20), (0.30, 0.65, 0.55), (0.35, 0.55, 0.85), (0.90, 0.45, 0.55)]
BLURB = ("Fun animal crossword puzzles for young puzzle solvers. "
         "Big, easy-to-read letters and clues. Answers are included at the back.")


def spine_width_in(page_count: int) -> float:
    return page_count * SPINE_PER_PAGE


def _cell(c: Canvas, x: float, y: float, size: float, letter: str, color) -> None:
    c.setFillColorRGB(*color)
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(3)
    c.roundRect(x, y, size, size, 8, fill=1, stroke=1)
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT, size * 0.62)
    c.drawCentredString(x + size / 2, y + size * 0.2, letter)


def _crossword_motif(c: Canvas, left: float, top: float, size: float) -> None:
    """Original decoration: PUZZLE across with ZOO going down from the first Z."""
    for i, ch in enumerate("PUZZLE"):
        _cell(c, left + i * size, top - size, size, ch, CELL_COLORS[i % 4])
    for j, ch in enumerate("OO", 1):
        _cell(c, left + 2 * size, top - size - j * size, size, ch, CELL_COLORS[(j + 1) % 4])


def render_cover(title: str, subtitle: str, author: str, page_count: int, out: Path) -> tuple[float, float]:
    register_fonts()
    spine = spine_width_in(page_count)
    width_in = 2 * TRIM_W + spine + 2 * BLEED
    height_in = TRIM_H + 2 * BLEED
    w, h = width_in * PT, height_in * PT
    c = Canvas(str(out), pagesize=(w, h))
    c.setTitle(title)
    c.setAuthor(author)
    c.setFillColorRGB(*BACKGROUND)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    page_w = TRIM_W * PT
    back_x = BLEED * PT
    spine_x = back_x + page_w
    front_x = spine_x + spine * PT
    safe = 0.5 * PT
    top = h - BLEED * PT - safe

    # front cover
    fw = page_w - 2 * safe
    c.setFillColorRGB(*INK)
    y = top - 40
    for line in wrap_text(title, FONT, 54, fw):
        c.setFont(FONT, 54)
        c.drawCentredString(front_x + page_w / 2, y, line)
        y -= 64
    c.setFont(FONT, 24)
    for line in wrap_text(subtitle, FONT, 24, fw):
        c.drawCentredString(front_x + page_w / 2, y - 10, line)
        y -= 32
    size = fw / 6
    _crossword_motif(c, front_x + safe, y - 40, size)
    c.setFillColorRGB(*INK)
    c.setFont(FONT, 26)
    c.drawCentredString(front_x + page_w / 2, BLEED * PT + safe, author)

    # back cover (bottom-right stays empty for the barcode KDP adds)
    c.setFont(FONT, 18)
    y = top - 60
    for line in wrap_text(BLURB, FONT, 18, fw):
        c.drawString(back_x + safe, y, line)
        y -= 26

    # spine text only when the book is thick enough for KDP to allow it
    if page_count >= MIN_SPINE_TEXT_PAGES:
        c.saveState()
        c.translate(spine_x + spine * PT / 2, h / 2)
        c.rotate(-90)
        c.setFillColorRGB(*INK)
        c.setFont(FONT, min(20, spine * PT * 0.5))
        c.drawCentredString(0, -4, f"{title}   -   {author}")
        c.restoreState()

    c.showPage()
    c.save()
    return width_in, height_in
