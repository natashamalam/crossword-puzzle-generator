from pathlib import Path

from crossword.cover import render_cover
from crossword.render import render_interior
from crossword.store import load_puzzles

TITLE = "Category Crosswords for Kids"  # working title: search before publication
SUBTITLE = "Easy Puzzles for Ages 6-8"
AUTHOR = "Mahjabin Alam"


def build(out_dir: Path = Path("generated_content"), puzzles_dir: Path = Path("data/puzzles")) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    puzzles = load_puzzles(puzzles_dir)
    pages = render_interior(puzzles, TITLE, out_dir / "interior.pdf", AUTHOR)
    render_cover(TITLE, SUBTITLE, AUTHOR, pages, out_dir / "cover.pdf")
    return pages


if __name__ == "__main__":
    print(f"built {build()} pages -> generated_content/interior.pdf, generated_content/cover.pdf")
