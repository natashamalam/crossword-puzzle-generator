from pathlib import Path

from crossword.build_puzzles import build_puzzles
from crossword.cover import render_cover
from crossword.data import load_entries
from crossword.render import render_interior

TITLE = "Animal Crosswords for Kids"  # placeholder: confirm title and run a trademark search first
SUBTITLE = "Easy Puzzles for Ages 6-8"
AUTHOR = "Mahjabin Alam"
CLUES = Path(__file__).resolve().parent / "data" / "clues.csv"


def build(out_dir: Path = Path("generated_content"), count: int = 50) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    puzzles = build_puzzles(load_entries(CLUES), count=count)
    pages = render_interior(puzzles, TITLE, out_dir / "interior.pdf", AUTHOR)
    render_cover(TITLE, SUBTITLE, AUTHOR, pages, out_dir / "cover.pdf")
    return pages


if __name__ == "__main__":
    print(f"built {build()} pages -> generated_content/interior.pdf, generated_content/cover.pdf")
