from pathlib import Path


def test_claude_and_grok_skill_paths_match():
    root = Path(__file__).resolve().parents[1]
    pairs = [
        (root / ".claude/skills/category-crossword/SKILL.md", root / "skills/category-crossword/SKILL.md"),
        (root / ".cursor/skills/category-crossword/SKILL.md", root / "skills/category-crossword/SKILL.md"),
        (root / ".claude/commands/category-crossword.md", root / "skills/category-crossword/COMMAND.md"),
        (root / ".cursor/commands/category-crossword.md", root / "skills/category-crossword/COMMAND.md"),
    ]
    for link, canonical in pairs:
        assert link.resolve() == canonical.resolve()
        assert link.read_text(encoding="utf-8") == canonical.read_text(encoding="utf-8")
    text = (root / "skills/category-crossword/SKILL.md").read_text(encoding="utf-8")
    for line in [
        "A black bird",
        "no real person's face",
        "generated_content/interior.pdf",
        "pass `--approved` only after Mahjabin approves the draft in a later reply",
        "python -m crossword.category draft",
        "python -m crossword.category apply",
    ]:
        assert line in text
