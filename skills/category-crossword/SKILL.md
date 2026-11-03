---
name: category-crossword
description: Draft a category crossword for Memory Boost Crosswords for Kids, show it for approval, and add it to the book only after approval. Use when the user gives categories and items, such as bird and sparrow, or asks for a category crossword.
---

# Category crossword

Build one puzzle for Memory Boost Crosswords for Kids from the categories and items the user gives. Easy, medium, and hard all use this same command.

## Draft

1. Turn the user's list into `request.json`. Each item has `word`, `category`, `caption`, and `image`.
2. Write a caption of at most 6 words. Name the category and the fact that separates this item from the others in that category. CROW is `A black bird`. SWAN is `A white bird with a long neck`. SPARROW is `A small brown bird`.
3. Draw one original still black-and-white cartoon for each new word. Use bold outlines, flat shapes, and a white background. Put no letters or numbers in the picture. The picture contains no real person's face, likeness, photograph, child, name, address, or school.
4. Save the cartoon as `drafts/<id>/<WORD>.png` and put that path in `image`. If `art/hints/<WORD>.png` already exists, reuse it and leave `image` empty.
5. Run:

```text
python -m crossword.category draft --input request.json --seed 1 --id <id>
```

6. Show Mahjabin the mode, each placed word with its category, caption, and picture, the words rejected or left out, and the grid with starter letters visible.
7. Stop. Do not apply the draft in this turn.

## Apply

pass `--approved` only after Mahjabin approves the draft in a later reply. Then run:

```text
python -m crossword.category apply drafts/<id>.json --approved
```

That writes the puzzle, copies new pictures into `art/hints/`, and rebuilds `generated_content/interior.pdf` and `generated_content/cover.pdf`.

## Modes

If the user names a mode, use it. Otherwise the book assigns puzzles 1–20 easy, 21–35 medium, and 36–50 hard. The book stops at 100 puzzles.

Easy shows the first letter of every word and, for a word of 5–8 letters, the middle letter. Medium shows the middle letter of every word. Hard shows the fewest letters that put at least one letter in every word, using crossing letters where it can, and also shows the middle letter of every 7–8 letter word. No word is left with no letter.

## One instruction text

Edit only `skills/category-crossword/SKILL.md` and `skills/category-crossword/COMMAND.md`. The Claude and Grok paths are symlinks to those files.
