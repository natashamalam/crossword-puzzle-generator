import random
from collections import Counter

from crossword.data import Entry
from crossword.grid import MIN_WORDS, Puzzle, generate, validate

MAX_REUSE = 3
SAMPLE_SIZE = 80
CANDIDATES = 10
MAX_SEED_TRIES = 200


def _size_for(index: int, count: int) -> int:
    return 7 + min(2, index * 3 // count)


def build_puzzles(entries: list[Entry], count: int = 50, seed: int = 1) -> list[Puzzle]:
    if len(entries) * MAX_REUSE < count * MIN_WORDS:
        raise ValueError(f"not enough words: {len(entries)} for {count} puzzles")
    rng = random.Random(seed)
    uses: Counter[str] = Counter()
    puzzles: list[Puzzle] = []
    for i in range(count):
        size = _size_for(i, count)
        candidates_seen = 0
        best: Puzzle | None = None
        for _ in range(MAX_SEED_TRIES):
            pool = [e for e in entries if uses[e.word] < MAX_REUSE]
            rng.shuffle(pool)
            pool.sort(key=lambda e: uses[e.word])  # prefer fresh words
            candidate = generate(pool[:SAMPLE_SIZE], size, rng.randrange(10**9))
            if candidate and not validate(candidate):
                if best is None or len(candidate.placed) > len(best.placed):
                    best = candidate
                candidates_seen += 1
                if candidates_seen == CANDIDATES:
                    break
        if best is None:
            raise ValueError(f"not enough words to build puzzle {i + 1}")
        puzzle = best
        uses.update(pl.entry.word for pl in puzzle.placed)
        puzzles.append(puzzle)
    return puzzles
