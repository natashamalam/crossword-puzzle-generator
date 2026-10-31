from datetime import date
from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from crossword.grid import EMPTY, Puzzle

FONT = "Andika"
FONT_FILE = Path(__file__).resolve().parent.parent / "fonts" / "Andika-Regular.ttf"
W, H = 612, 792
OUTER, GUTTER, TOP, BOTTOM = 36, 54, 36, 48
MIN_PAGES = 24
# (clue font size, grid cell size): the first combination whose clues fit is used.
LAYOUTS = [(14, 36), (14, 32), (13, 30), (12, 28)]
PUZZLES_PER_SOLUTION_PAGE = 4

HOW_TO_PLAY = [
    "1. Each number in the grid matches a clue below it.",
    "2. Across clues go from left to right. Down clues go from top to bottom.",
    "3. Read the clue, think of the word and write one letter in each box.",
    "4. Words cross each other, so a letter you write can help with another clue.",
    "5. Stuck? Skip it and come back later. The answers are at the back of the book.",
]


def register_fonts() -> None:
    if FONT not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(FONT, str(FONT_FILE)))


def wrap_text(text: str, font: str, size: float, max_width: float) -> list[str]:
    lines: list[str] = []
    line = ""
    for word in text.split():
        while stringWidth(word, font, size) > max_width:  # break a word wider than the column
            cut = len(word) - 1
            while cut > 1 and stringWidth(word[:cut], font, size) > max_width:
                cut -= 1
            if line:
                lines.append(line)
                line = ""
            lines.append(word[:cut])
            word = word[cut:]
        trial = f"{line} {word}".strip()
        if stringWidth(trial, font, size) <= max_width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def _margins(page_no: int) -> tuple[float, float]:
    """(left, right): the gutter sits on the inside edge of every page."""
    return (GUTTER, OUTER) if page_no % 2 else (OUTER, GUTTER)


def _footer(c: Canvas) -> None:
    c.setFont(FONT, 10)
    c.drawCentredString(W / 2, 24, str(c.getPageNumber()))


def _draw_grid(c: Canvas, p: Puzzle, x: float, top: float, cell: float, letters: bool) -> None:
    numbers = {(pl.row, pl.col): pl.number for pl in p.placed}
    c.setLineWidth(1.2)
    c.setStrokeColorRGB(0, 0, 0)
    for r in range(p.size):
        for col in range(p.size):
            ch = p.cells[r][col]
            if ch == EMPTY:
                continue
            cx, cy = x + col * cell, top - (r + 1) * cell
            c.rect(cx, cy, cell, cell)
            if (r, col) in numbers:
                c.setFont(FONT, max(7, cell * 0.28))
                c.drawString(cx + 2, cy + cell - cell * 0.28 - 1, str(numbers[(r, col)]))
            if letters:
                c.setFont(FONT, cell * 0.6)
                c.drawCentredString(cx + cell / 2, cy + cell * 0.22, ch)


def _clue_columns(p: Puzzle, size: int, width: float):
    cols = []
    for title, across in (("Across", True), ("Down", False)):
        items = []
        for pl in sorted((q for q in p.placed if q.across == across), key=lambda q: q.number):
            items.append((str(pl.number), wrap_text(pl.entry.clue, FONT, size, width - 22)))
        cols.append((title, items))
    return cols


def _puzzle_page(c: Canvas, p: Puzzle, number: int) -> None:
    left, right = _margins(c.getPageNumber())
    content = W - left - right
    col_w = (content - 20) / 2
    c.setFont(FONT, 26)
    c.drawCentredString(left + content / 2, H - TOP - 26, f"Puzzle {number}")
    grid_top = H - TOP - 50
    for size, cell in LAYOUTS:
        leading = size * 1.3
        cols = _clue_columns(p, size, col_w)
        need = max(1 + sum(len(lines) for _, lines in items) for _, items in cols) * leading + 8 * max(len(i) for _, i in cols)
        clues_top = grid_top - p.size * cell - 28
        if need <= clues_top - BOTTOM:
            break
    else:
        raise ValueError(f"Puzzle {number}: clues do not fit on the page, shorten them")
    _draw_grid(c, p, left + (content - p.size * cell) / 2, grid_top, cell, letters=False)
    for i, (title, items) in enumerate(cols):
        x = left + i * (col_w + 20)
        y = clues_top
        c.setFont(FONT, size + 2)
        c.drawString(x, y, title)
        y -= leading + 4
        c.setFont(FONT, size)
        for num, lines in items:
            c.drawString(x, y, num)
            for line in lines:
                c.drawString(x + 22, y, line)
                y -= leading
            y -= 4
    _footer(c)


def _solution_pages(c: Canvas, puzzles: list[Puzzle]) -> None:
    for start in range(0, len(puzzles), PUZZLES_PER_SOLUTION_PAGE):
        left, right = _margins(c.getPageNumber())
        content = W - left - right
        c.setFont(FONT, 26)
        c.drawCentredString(left + content / 2, H - TOP - 26, "Solutions")
        half = content / 2
        for i, p in enumerate(puzzles[start:start + PUZZLES_PER_SOLUTION_PAGE]):
            qx = left + (i % 2) * half
            qy = H - TOP - 70 - (i // 2) * 320
            cell = min(24, (half - 20) / p.size)
            c.setFont(FONT, 14)
            c.drawString(qx, qy, f"Puzzle {start + i + 1}")
            _draw_grid(c, p, qx, qy - 12, cell, letters=True)
        _footer(c)
        c.showPage()


def _centered_lines(c: Canvas, lines: list[str], size: float, y: float, leading: float) -> float:
    c.setFont(FONT, size)
    for line in lines:
        c.drawCentredString(W / 2, y, line)
        y -= leading
    return y


def render_interior(puzzles: list[Puzzle], title: str, out: Path, author: str = "Mahjabin Alam") -> int:
    register_fonts()
    c = Canvas(str(out), pagesize=(W, H))
    c.setTitle(title)
    c.setAuthor(author)

    # title page
    y = _centered_lines(c, wrap_text(title, FONT, 38, W - 144), 38, H - 250, 46)
    _centered_lines(c, ["A crossword puzzle book for ages 6-8"], 18, y - 10, 24)
    _centered_lines(c, [author], 20, 140, 24)
    c.showPage()

    # copyright page
    year = date.today().year
    c.setFont(FONT, 12)
    y = 300
    for line in [f"Copyright © {year} {author}. All rights reserved.", "",
                 "No part of this book may be reproduced without written permission",
                 "from the author, except for short quotations in reviews.", "",
                 "All puzzles and clues are original."]:
        c.drawCentredString(W / 2, y, line)
        y -= 18
    c.showPage()

    # how to play
    left, right = _margins(c.getPageNumber())
    c.setFont(FONT, 28)
    c.drawCentredString(W / 2, H - 120, "How to Play")
    y = H - 190
    c.setFont(FONT, 18)
    for step in HOW_TO_PLAY:
        for line in wrap_text(step, FONT, 18, W - left - right):
            c.drawString(left, y, line)
            y -= 26
        y -= 14
    _footer(c)
    c.showPage()

    for n, p in enumerate(puzzles, 1):
        _puzzle_page(c, p, n)
        c.showPage()
    _solution_pages(c, puzzles)

    pages = c.getPageNumber() - 1
    target = max(MIN_PAGES, pages + pages % 2)
    for _ in range(target - pages):
        c.showPage()
    c.save()
    return target
