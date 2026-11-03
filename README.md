# Crossword KDP

Builds a kids' crossword puzzle book (interior PDF and cover PDF) for Amazon KDP.

## Build the book

```bash
.venv/bin/python build.py
```

Output goes to `generated_content/` (`interior.pdf`, `cover.pdf`). Run the tests with `.venv/bin/python -m pytest`.

## The `category-crossword` skill and command

One instruction text drives both Claude Code and Cursor (Grok). The text lives in two canonical files:

| File | Role |
| --- | --- |
| `skills/category-crossword/SKILL.md` | The skill: what to do and how |
| `skills/category-crossword/COMMAND.md` | The slash command: the entry point |

The tool folders contain symlinks to those files, not copies:

| Tool | Skill path | Command path |
| --- | --- | --- |
| Claude Code | `.claude/skills/category-crossword/SKILL.md` | `.claude/commands/category-crossword.md` |
| Cursor | `.cursor/skills/category-crossword/SKILL.md` | `.cursor/commands/category-crossword.md` |

**Edit only the files under `skills/`.** Both tools then pick up the change. See `CLAUDE.md` and `.cursor/rules/sync-claude-skill-to-grok.mdc`.

### What it does

Each run makes **one** puzzle from the categories and items you give it, for example `bird: sparrow, crow, swan`. It works in two steps:

1. **Draft.** The agent writes a short caption for each item, draws an original black-and-white cartoon, and runs `python -m crossword.category draft`. It then shows you the mode, every placed word with its caption and picture, any words left out, and the grid. It stops there.
2. **Apply.** Only after you approve in a later message does it run `python -m crossword.category apply drafts/<id>.json --approved`. That saves the puzzle, copies new pictures into `art/hints/`, and rebuilds `generated_content/interior.pdf` and `cover.pdf`.

The mode (easy, medium or hard) follows the puzzle's position in the book: 1-20 easy, 21-35 medium, 36-50 hard. The book stops at 100 puzzles. You can name a mode to override this.

### Invoke in Claude Code

Open Claude Code in this directory, then either:

- Type the slash command with your categories and items: `/category-crossword bird: sparrow, crow, swan`.
- Or ask in plain words, such as "make a category crossword with bird: sparrow, crow, swan". Claude loads the skill when the request matches its description.

After adding or changing a skill or command, start a new session so Claude Code reloads it.

### Invoke in Cursor

Open this folder in Cursor and use Agent chat:

- Type `/category-crossword bird: sparrow, crow, swan` and pick the command from the list.
- Or ask in plain words. Cursor's agent can apply the skill on its own when the request matches.

### Approve or change a draft

Reply to the draft in the same chat. Say "approved" to apply it, or ask for changes (a different caption, a swapped word, another mode) and the agent drafts again. Nothing is added to the book until you approve.

### Check the setup

```bash
ls -l .claude/skills/category-crossword/SKILL.md .cursor/skills/category-crossword/SKILL.md \
      .claude/commands/category-crossword.md .cursor/commands/category-crossword.md
```

Each line should show `->` pointing at a file under `skills/category-crossword/`. A plain file instead of a symlink means it has drifted. Replace it with the canonical text.

## Before selling

Run a trademark search on the final title and review your KDP listing sheet (`docs/listing.md`, kept locally and not tracked in git). The title in `build.py` is a working title.
