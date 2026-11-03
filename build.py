from pathlib import Path

from crossword.alternates import load_alternates
from crossword.cover import render_cover
from crossword.render import render_interior
from crossword.store import load_puzzles

TITLE = "Memory Boost Crosswords for Kids"  # working title: search before publication
SUBTITLE = "Sharpen Your Mind, One Word at a Time"
AUTHOR = "Mahjabin Alam"


def build(
    out_dir: Path = Path("generated_content"),
    puzzles_dir: Path = Path("data/puzzles"),
    alternates_file: Path = Path("data/alternates.json"),
) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    puzzles = load_puzzles(puzzles_dir)
    pages = render_interior(puzzles, TITLE, out_dir / "interior.pdf", AUTHOR, load_alternates(alternates_file))
    render_cover(TITLE, SUBTITLE, AUTHOR, pages, out_dir / "cover.pdf")
    return pages


if __name__ == "__main__":
    print(f"built {build()} pages -> generated_content/interior.pdf, generated_content/cover.pdf")
