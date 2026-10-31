# Kids' Crossword Puzzle Book (Amazon KDP) - Design

Date: 2026-10-31
Owner: Mahjabin Alam

## Goal
Publish a paperback crossword puzzle book for ages 6-8 on Amazon KDP, using a repeatable
process so further volumes can follow quickly.

## Constraints
- Everything must be original or openly licensed (text, clues, art, fonts, word lists, code).
- No third-party brand or product names in the title, keywords, clues or cover.
- No invented claims about real entities (no fake reviews, awards or "bestseller" claims).
- Prefer open standards and open formats.

## Product spec (volume 1)
- Audience: ages 6-8. Large print, simple vocabulary, picture-friendly clues.
- Trim size: 8.5 x 11 in, black-and-white interior, paperback.
- About 50 puzzles, grids 7x7 to 9x9, difficulty ramping gently.
- Back matter: full solutions section. Front matter: title page, copyright page, "How to play".
- Single theme per volume (e.g. animals, space, school); final theme chosen in step 1.

## Approach (chosen: A)
Script-generated grids from an open-licensed word list, with clues written by us.

### Components
1. **Word list** - CC0/public-domain list, filtered to age-appropriate words (3-8 letters).
   Licence recorded in a THIRD_PARTY_NOTICES file.
2. **Grid generator** (Python) - builds crossword grids; validator checks connectivity,
   no orphan cells, every word has a clue, no duplicate words.
3. **Clue file** (CSV/JSON) - one original clue per word, human-reviewed.
4. **Interior renderer** - produces print-ready PDF at trim size with KDP margins and
   gutter, large-print fonts (SIL OFL licensed), page numbers, solutions section.
5. **Cover** - original artwork; spine width from KDP's cover calculator using the final
   page count; PDF cover at KDP spec.
6. **KDP listing** - title, subtitle, 7 keywords, description, categories, free KDP ISBN, price.

Each component has a clear input/output so it can be tested and reused for later volumes.

## Plan of work
1. Niche check: study existing kids' crossword books (price, page count, themes, gaps);
   pick theme and original title; quick trademark conflict check.
2. Content spec finalised (puzzle count, grid sizes, difficulty curve).
3. Build and test the grid generator + validator.
4. Write clues for all words; review for age-appropriateness and originality.
5. Build the interior renderer; check against KDP print requirements.
6. Create the cover.
7. KDP account/tax setup; create listing; upload; order proof copy.
8. Proof review (print quality, puzzle correctness) -> fix -> publish.
9. Pre-publish provenance scan: brand names, copied text, unlicensed assets, invented
   claims. Report results. Recommend trademark search before launch; I am not a lawyer.
10. Retrospective and plan for volume 2.

## Testing / verification
- Unit tests for the validator (known-good and known-bad grids).
- Every puzzle solvable and solution matches the clue set.
- PDF checked with KDP's previewer and a physical proof copy.

## Risks
- Crowded niche: mitigate with a specific theme and a good title/keywords.
- Print errors (margins, bleed): mitigate with the proof copy.
- Title/trademark conflicts: mitigate with search before launch.

## Out of scope (volume 1)
Hardcover, audiobook/ebook editions, multiple languages, ads and marketing campaigns.
