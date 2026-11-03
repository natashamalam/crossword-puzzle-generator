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
5. **Two living files, updated at every milestone and before ending a session or compacting:**
   - `REQUIREMENTS.md`: the user's requirements, their exact wording where it matters, and the rules that came out of them.
   - `PLAN.md`: current state (counts of puzzles applied and drafted), what is done, what is next, and open decisions.
   A new session reads both first and resumes from `PLAN.md` without asking again.
6. **Checkpoint before risk.** Before a long background job, a compaction, or the end of a session, confirm the files in rule 5 and `workbench/` are current. Tell the user in one line where the work lives.
7. **Suggest a commit** once a milestone is saved (for example "30 hard word sets saved"), so the work survives outside the working tree. Commit only when the user agrees, with no AI attribution.
8. **Report losses at once.** If a needed file is missing, say so first, search the session transcripts under `~/.claude/projects/` for it, and rebuild from there before asking the user to redo anything.
