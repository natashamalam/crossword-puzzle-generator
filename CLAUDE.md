# Sync Claude skill and command instructions to Grok

Claude and Grok use one instruction text for the category crossword skill and command. A change made for Claude is the change Grok follows.

Edit only the canonical files:

- `skills/category-crossword/SKILL.md`
- `skills/category-crossword/COMMAND.md`

These paths are symlinks to those files, not separate copies:

- `.claude/skills/category-crossword/SKILL.md`
- `.cursor/skills/category-crossword/SKILL.md`
- `.claude/commands/category-crossword.md`
- `.cursor/commands/category-crossword.md`

When a Claude skill or command instruction changes, update the canonical file in that same change. Leave the symlinks in place so Grok reads the updated text.

```text
Bad:  edit .claude/skills/category-crossword/SKILL.md and leave a different copy under .cursor/
Good: edit skills/category-crossword/SKILL.md, which both apps link to
```

If a path above is a real file with different text, replace it with the canonical text before finishing.

# Never lose work: keep everything in the repo

These rules exist because a whole session of work (200 locked hard-mode words, the drawing kit and the build scripts) once lived only in a temporary scratchpad folder and was lost. They apply to every session.

1. **Repo, not scratchpad.** Anything that took effort to produce, or that a later session needs, is written inside this repo: word lists, captions, seeds, drawing code, build scripts, request files, decisions. Scratchpad and `/tmp` hold only throwaway output (contact sheets, logs) that can be regenerated in minutes.
2. **Save at the moment of creation.** When a word set, caption set, seed list or script is produced or changed, write it to its repo path in the same step, not at the end. Do not wait for the end of a session.
3. **One home for working files:** `workbench/` (scripts, art modules, caption files, word sets such as `hfinal.json`). Drafts stay in `drafts/`. Applied puzzles stay in `data/puzzles/`. Scripts must take repo-relative paths and must not read from a scratchpad.
4. **Memory and notes only point to repo paths that exist.** Before writing a memory note or any handoff that names a file, check that the file exists in the repo (`ls`). Never name a scratchpad path. Give paths relative to the repo root so the user can find them.
5. **Rules live in this file, state lives in `PLAN.md`.** The user's requirements and book rules are written in the "Book rules" section below; add a new rule there when the user gives one, with their wording where it matters. `PLAN.md` (local only, in `.gitignore`) holds the current state, what is done, what is next, and open decisions; update it at every milestone and before ending a session or compacting. A new session reads both first and resumes from `PLAN.md` without asking again.
6. **Checkpoint before risk.** Before a long background job, a compaction, or the end of a session, confirm this file, `PLAN.md` and `workbench/` are current. Tell the user in one line where the work lives.
7. **Suggest a commit** once a milestone is saved (for example "30 hard word sets saved"), so the work survives outside the working tree. Commit only when the user agrees, with no AI attribution.
8. **Report losses at once.** If a needed file is missing, say so first, search the session transcripts under `~/.claude/projects/` for it, and rebuild from there before asking the user to redo anything.

# Hint pictures live in `hint_images/`

All hint pictures (one `<WORD>.png` per keyword) are stored in the `hint_images/` folder at the repo root. When a new hint picture is created, write it straight to `hint_images/<WORD>.png`, never to `drafts/`, a scratchpad or any other folder, and put that path in the request's `image` field. Scripts, the draft and apply commands, the skill text and the docs all use this folder. The old `art/hints/` folder no longer exists.

# Book rules: Memory Boost Crosswords for Kids

The book is a KDP picture-clue crossword book for ages 6-8, by Mahjabin Alam. Title "Memory Boost Crosswords for Kids", subtitle "Sharpen Your Mind, One Word at a Time" (the user does not want the old title "Category Crosswords for Kids"). It has 100 puzzles (the cap) in `data/puzzles/`; `WORDS.md` lists every word.

**Words**
- A keyword never repeats anywhere in the book.
- Words are 3-8 letters (the generator rejects longer ones), kid-friendly, concrete and easy to picture. No brand names (JEEP, PUMA, JAGUAR, KAYAK, TARGET, DOMINOES were removed), nothing abstract or ambiguous, nothing obscure or technical.
- The words the user rejected must never return: the list is in `workbench/not_kid_friendly.txt` (50 words).
- Puzzles with 7 or 8 keywords in medium and hard need 3-6 words of 7-8 letters.

**Puzzles**
- Layout: easy 7x7, medium 8x8, hard 9x9. Puzzle titles are just "Puzzle N", with no Easy/Medium/Hard labels anywhere.
- Starter letters: easy shows the first letter of every word plus the middle letter of words of 5-8 letters; medium shows the middle letter of every word; hard shows a minimal covering set of letters (using crossings) plus the middle letter of 7-8 letter words, so every word has at least one letter.
- Alternative answers: if a clue has another valid word, list it in `data/alternates.json`. It prints as "Also accepted" only when the other word agrees with the crossing letters and printed starter letters.
- Workflow: draft, show the user, and apply only after the user approves in a later reply (`python -m crossword.category apply drafts/<id>.json --approved`), one puzzle at a time, in order.

**Captions and pictures**
- Captions are 6 words or fewer, name the category and what separates the item from others in it, never contain the answer, and are distinct within a category.
- Pictures are simple, naive, cartoon-like drawings (the caption is the main clue), with no letters or numbers and no real person's face. They are original, drawn in code, and stored in `hint_images/`.

**Before publishing**
- Scan for brand names, copied text and unlicensed assets, and recommend a KDP and trademark search on the title and subtitle.
- Commit only when the user asks. `PLAN.md` is local only (in `.gitignore`).
