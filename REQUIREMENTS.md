# Requirements (from Mahjabin, across sessions)

Keep this file current. Quote the user's words where the wording matters.

## The book
- KDP crossword book "Memory Boost Crosswords for Kids", ages 6-8. Built with the `category-crossword` skill (`skills/category-crossword/SKILL.md`).
- Cover subtitle: "Sharpen Your Mind, One Word at a Time" (user's choice, 2026-11-01).
- Book cap: 100 puzzles.
- Puzzle titles are just "Puzzle N". No "Easy / Medium / Hard" labels anywhere ("no need to denote with mode like Easy").

## Puzzle sets
| Mode | Grid | Count | Keywords per puzzle | Status |
|---|---|---|---|---|
| Easy | 7x7 | 20 (plus the original puzzle 001 = 21) | first 8 have 5, next 8 have 6, last 4 have 7 | applied |
| Medium | 8x8 | 31 | 5 x 4 keywords, 5 x 5, 10 x 6, 3 x 7, 8 x 8 | applied |
| Hard | 9x9 | 30 | 5 x 5 keywords, 10 x 6, 5 x 7, 10 x 8 | words locked, pictures and drafts pending |

(The user first said 25 medium puzzles; the counts add up to 31, and the user chose 31.)

## Rules
- A keyword never repeats anywhere in the book (across easy, medium and hard).
- For puzzles with 7 or more keywords, between 3 and 6 of the keywords must have 8 letters. The user later allowed **7-letter words instead of 8** when 8-letter words are hard to find: "if finding 8 letter words are difficult, use 7 letter instead."
- For some medium puzzles, use categories that were not used in the easy set.
- Hint pictures: made for 6 to 8 year olds, no letters or numbers, no real person's face or likeness. The user first asked for "realistic" pictures and said "just draw all the pictures keeping it as realistic as possible." On 2026-11-02 the user relaxed this: **simple, naive, cartoon-like pictures are fine, because the caption (the description hint) is the main clue.**
- Word choice (user, 2026-11-02): words must help 6-8 year olds build vocabulary. Use concrete, easy-to-picture everyday words. Avoid brand-like words (e.g. KAYAK, TARGET, DOMINOES were removed) and abstract or ambiguous words (e.g. SONG, PARTY, LIGHT, BOW, TOPS, STARSHIP were removed).
- Kid-friendly words only (user, 2026-11-02): words must be familiar to a 6-8 year old, concrete and easy to picture. Not obscure, technical or unusual. The user rejected these words (50 so far; later additions: GARLAND, RECORDER, PLUNGER, MAST, ARM, TUGBOAT, SLED, TADPOLE, HOSE), which must never come back (list in `workbench/not_kid_friendly.txt`): BAGUETTE, CELLO, BANJO, STREAMER, CONFETTI, BIRCH, CHISEL, WRENCH, SEESAW, ACROBAT, TRAPEZE, UNICYCLE, STILTS, ABACUS, MARACAS, SNORKEL, SAILBOAT, BEAVER, TONGS, BLUEBELL, TRELLIS, HEDGE, LYNX, PARAKEET, SUNDAE, LEEK, BOULDER, GONDOLA, MITTENS, EASEL, ANVIL, MEERKAT, SHIN, BOBCAT, BUGLE, TUXEDO, CLARINET, COYOTE, CRATER, TURBAN, LUTE.
- Captions: at most 6 words, say the category and what separates this item from others in it, never contain the answer word, and are distinct inside a category.
- Starter letters: easy shows the first letter of every word and also the middle letter for words of 5-8 letters (updated 2026-11-02 at the user's request, so every word of 5 or more letters shows at least 2 letters); medium shows the middle letter of every word; hard shows at least one letter in every word (updated 2026-11-02 after the user said the first version looked very difficult): a minimal set of letters that covers every word, using crossing letters, plus the middle letter of every 7-8 letter word. Medium still shows the middle letter of every word.
- Alternative answers (user, 2026-11-02): if a clue can be answered by another word, list it as also accepted on the Solutions pages. Alternatives live in `data/alternates.json`; the code (`crossword/alternates.py`) only lists one that has the same length and agrees with every crossing letter and every printed starter letter, so the filled grid stays valid. When choosing new words, check for look-alike synonyms.
- Workflow: draft, show the user, and apply only after the user approves in a later reply (`python -m crossword.category apply drafts/<id>.json --approved`, one at a time, in order).
- No Claude/AI attribution in commits, PRs or code. Author is Mahjabin Alam. Commit only when asked.
- Before publishing: scan for brand names, copied text and unlicensed assets; recommend a KDP/trademark search on the title and subtitle.
- Do not name a product after a third-party brand; use fictional names in samples.
- Edit skill text only in `skills/category-crossword/SKILL.md` and `COMMAND.md` (the `.claude` and `.cursor` paths are symlinks).
- Title changed 2026-11-03 to "Memory Boost Crosswords for Kids" (user: no 'Category Crosswords for Kids'; suggest memory boost). Back-cover blurb rewritten in crossword/cover.py. Search KDP/trademark on the new title.
- Brand-name words JEEP, PUMA, JAGUAR were removed (2026-11-03); avoid brand-like words.
