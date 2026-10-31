# Kids' Crossword KDP Book Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce print-ready interior and cover PDFs for a 50-puzzle, ages 6-8 crossword paperback, plus a KDP listing sheet.

**Architecture:** A small Python package generates valid crossword grids from an original, curated word/clue file, renders them to an 8.5x11 in PDF with ReportLab, and builds a cover PDF whose spine width derives from the page count. Each stage is a pure function with file in/file out so later volumes only swap the data file.

**Tech Stack:** Python 3.11+, pytest, reportlab (BSD), Andika font (SIL OFL), pypdf (BSD, for page-count checks).

**Spec:** `docs/superpowers/specs/2026-10-31-kids-crossword-kdp-design.md`

## Global Constraints

- All words, clues, art and text are original or openly licensed; no third-party brand names anywhere.
- Trim size 8.5 x 11 in; black-and-white interior; paperback; ~50 puzzles; grids 7x7 to 9x9.
- Words 3-8 letters, uppercase A-Z only; one original clue per word.
- Fonts SIL OFL only; list every third-party item in `THIRD_PARTY_NOTICES.md`.
- No AI-tool attribution lines in commits, files or metadata; commit author `Mahjabin Alam <ts.mahjabin.alam@gmail.com>`.
- Working theme: **animals** (final title/theme confirmed in Task 0).

## Review Focus

- Word that cannot be placed in any grid: generator must skip it, not loop forever.
- Clue file with a missing, empty or duplicate word: loader raises a clear error naming the word.
- Page count odd or under 24: book builder pads blank pages to an even count of at least 24.
- Non-ASCII or lowercase characters in the data file: normalized or rejected, never rendered wrongly.
- Long clue text overflowing its column: renderer wraps and never clips.

---

### Task 0: Niche check and title (manual, with Mahjabin)

**Files:** Create `docs/listing.md`

- [ ] **Step 1:** Search Amazon for kids' crossword books (ages 6-8); record price, page count, themes, gaps in `docs/listing.md`.
- [ ] **Step 2:** Pick theme and 3 original title candidates; quick web search for conflicts with existing titles/brands; Mahjabin chooses one.
- [ ] **Step 3:** Record the chosen title, subtitle and theme in `docs/listing.md`.

### Task 1: Project scaffold and data loader

**Files:**
- Create: `crossword/__init__.py`, `crossword/data.py`, `data/clues.csv`, `tests/test_data.py`, `THIRD_PARTY_NOTICES.md`, `pyproject.toml`
- Run `git init` here, set local author to Mahjabin Alam.

**Interfaces:**
- Produces: `@dataclass Entry(word: str, clue: str)`; `load_entries(path: Path) -> list[Entry]`.

- [ ] **Step 1: Write failing tests** in `tests/test_data.py`: `test_load_valid_csv` (2 rows return 2 `Entry`, words uppercased), `test_duplicate_word_raises` (ValueError message contains the word), `test_empty_clue_raises`, `test_non_letters_rejected` (e.g. `"CAT1"`), `test_length_bounds` (2- and 9-letter words rejected).
- [ ] **Step 2:** Run `pytest tests/test_data.py -v`; expect FAIL (import error).
- [ ] **Step 3:** Implement `load_entries` in `crossword/data.py` using `csv.DictReader` (columns `word,clue`).
- [ ] **Step 4:** Run tests; expect PASS.
- [ ] **Step 5:** Add `data/clues.csv` with a 10-row starter set of original animal clues (e.g. `CAT,"A pet that purrs"`); `THIRD_PARTY_NOTICES.md` initially states "none yet". Commit: `git commit -m "feat: scaffold project and clue loader"`.

### Task 2: Grid generator and validator

**Files:** Create `crossword/grid.py`, `tests/test_grid.py`

**Interfaces:**
- Consumes: `Entry` from Task 1.
- Produces: `@dataclass Placed(entry: Entry, row: int, col: int, across: bool, number: int)`; `@dataclass Puzzle(size: int, cells: list[list[str]], placed: list[Placed])` (empty cell is `"."`); `generate(entries: list[Entry], size: int, seed: int) -> Puzzle | None`; `validate(p: Puzzle) -> list[str]` (list of problems, empty means valid).

- [ ] **Step 1: Write failing tests:** `test_generate_is_deterministic_for_seed`; `test_generated_puzzle_validates` (10 entries, size 9, `validate == []`); `test_validate_flags_disconnected` (hand-built two-island grid); `test_validate_flags_unclued_run` (letter run of length >=2 with no `Placed`); `test_unplaceable_word_is_skipped` (word longer than size, generation still returns a puzzle); `test_returns_none_when_fewer_than_6_words_fit`.
- [ ] **Step 2:** Run; expect FAIL.
- [ ] **Step 3:** Implement `generate` as seeded greedy placement: place the longest word centered, then add words crossing existing letters, rejecting placements that create adjacent-letter conflicts; cap attempts per word. Numbering: left-to-right, top-to-bottom for start cells.
- [ ] **Step 4:** Implement `validate` (connectivity via flood fill, every run of 2+ letters matches a `Placed`, no duplicate words).
- [ ] **Step 5:** Run tests; expect PASS. Commit: `feat: crossword grid generator and validator`.

### Task 3: Content build (50 puzzles) and quality gate

**Files:** Create `crossword/build_puzzles.py`, `tests/test_build_puzzles.py`; expand `data/clues.csv` to ~400 words.

**Interfaces:**
- Consumes: `load_entries`, `generate`, `validate`.
- Produces: `build_puzzles(entries: list[Entry], count: int = 50, seed: int = 1) -> list[Puzzle]` (sizes ramp 7 -> 8 -> 9 across the book; every puzzle validates; words reused across puzzles at most 3 times).

- [ ] **Step 1: Write failing tests:** `test_returns_requested_count`; `test_sizes_ramp_non_decreasing`; `test_all_puzzles_validate`; `test_word_reuse_capped_at_3`; `test_raises_if_not_enough_words`.
- [ ] **Step 2:** Run; expect FAIL.
- [ ] **Step 3:** Implement `build_puzzles`, retrying seeds until a valid puzzle is made.
- [ ] **Step 4:** Write the ~400 original animal words and clues in `data/clues.csv` (simple language for age 6-8; no trademarks, no copied clue text). Mahjabin reviews the file.
- [ ] **Step 5:** Run tests; expect PASS. Commit: `feat: puzzle set builder and animal clue data`.

### Task 4: Interior PDF renderer

**Files:** Create `crossword/render.py`, `fonts/Andika-Regular.ttf` (+ `fonts/OFL.txt`), `tests/test_render.py`

**Interfaces:**
- Consumes: `Puzzle`.
- Produces: `render_interior(puzzles: list[Puzzle], title: str, out: Path) -> int` (returns final page count; page size 612x792 pt; margins >= 0.5 in outer, 0.75 in gutter; order: title page, copyright page, "How to play", puzzles, solutions; pads blank pages so count is even and >= 24).

- [ ] **Step 1: Write failing tests:** `test_page_count_even_and_at_least_24`; `test_page_size_is_letter` (use pypdf); `test_long_clue_wraps` (clue of 200 chars renders without raising and stays inside the margin box); `test_solutions_pages_present` (extracted text contains "Solutions").
- [ ] **Step 2:** Run; expect FAIL.
- [ ] **Step 3:** Implement with ReportLab canvas: one puzzle per page (grid on top, numbered Across/Down clues below at >= 14 pt); solutions 4 per page; register Andika.
- [ ] **Step 4:** Run tests; expect PASS. Add font OFL entry to `THIRD_PARTY_NOTICES.md`. Commit: `feat: interior PDF renderer`.

### Task 5: Cover PDF

**Files:** Create `crossword/cover.py`, `tests/test_cover.py`

**Interfaces:**
- Produces: `spine_width_in(page_count: int) -> float` (= `page_count * 0.002252`, white paper B&W); `render_cover(title: str, subtitle: str, author: str, page_count: int, out: Path) -> tuple[float, float]` returning (width_in, height_in), where width = 2*8.5 + spine + 0.25 and height = 11 + 0.25. Art is generated from original vector shapes in code (no external images).

- [ ] **Step 1: Write failing tests:** `test_spine_width_100_pages` (== 0.2252 within 1e-6); `test_cover_dimensions` (page size matches returned inches at 72 pt/in); `test_spine_text_skipped_under_79_pages` (KDP minimum for spine text).
- [ ] **Step 2:** Run; expect FAIL.
- [ ] **Step 3:** Implement the two functions; spine text only if page count >= 79.
- [ ] **Step 4:** Run tests; expect PASS. Before upload, confirm the numbers against KDP's cover calculator and fix constants if they differ. Commit: `feat: cover renderer`.

### Task 6: One-command build, provenance scan, listing, proof

**Files:** Create `build.py`, `tests/test_build.py`, `crossword/scan.py`, `docs/listing.md` (extend)

**Interfaces:**
- Produces: `python build.py` writes `out/interior.pdf` and `out/cover.pdf`; `scan_text(paths: list[Path], banned: list[str]) -> list[str]` returns `"path: term"` hits.

- [ ] **Step 1: Write failing tests:** `test_build_creates_both_pdfs` (tmp out dir); `test_scan_flags_banned_term`; `test_scan_clean_returns_empty`.
- [ ] **Step 2:** Run; expect FAIL.
- [ ] **Step 3:** Implement `build.py` (load -> build_puzzles -> render_interior -> render_cover with real page count) and `scan_text`.
- [ ] **Step 4:** Run full `pytest -v`; expect all PASS. Run `python build.py`; open both PDFs and inspect visually.
- [ ] **Step 5:** Run the scan over `data/`, `docs/`, `crossword/` with a banned list of known brand names (Mahjabin supplies/approves the list); report results.
- [ ] **Step 6 (manual with Mahjabin):** Complete `docs/listing.md` (description, 7 keywords, categories, price, free KDP ISBN). Create the KDP account and tax info, upload PDFs, order a proof copy, review it for print quality and puzzle errors, fix, then publish.
- [ ] **Step 7:** Recommend a trademark search on the final title before launch (not legal advice). Commit: `feat: build pipeline, scan and listing`.
