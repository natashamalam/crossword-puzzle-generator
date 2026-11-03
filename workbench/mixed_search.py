"""Find word sets for the mixed-category puzzles: mixed_search.py <seconds per puzzle> -> workbench/mixed_sets.json"""
import sys, json, random, time
sys.path.insert(0, ".")
sys.path.insert(0, "workbench")
from crossword.data import Entry
from crossword.grid import generate
from mixed_pool import POOL

secs = float(sys.argv[1])
CONFIG = [("easy", 7, [5, 5, 6, 6, 7, 7]), ("medium", 8, [5, 6, 6, 7, 8, 8]), ("hard", 9, [5, 6, 6, 7, 8, 8])]
cat_of = {}
for cat, ws in POOL.items():
    for w in ws.split():
        cat_of[w] = w if cat == "short" else cat   # "short" words each count as their own category
rnd = random.Random(7)
taken, out = set(), []
for mode, size, counts in CONFIG:
    for n in counts:
        pool = [w for w in cat_of if w not in taken and len(w) <= min(size, 8)]
        if mode == "easy": pool = [w for w in pool if len(w) <= (5 if n >= 7 else 7)]
        t0 = time.time(); found = None
        while time.time() - t0 < secs and not found:
            ws, cats = [], set()
            for w in rnd.sample(pool, len(pool)):
                if cat_of[w] in cats: continue
                ws.append(w); cats.add(cat_of[w])
                if len(ws) == n: break
            if len(ws) < n: continue
            nl = sum(len(w) >= 7 for w in ws)
            if mode != "easy" and n >= 7 and not 3 <= nl <= 6: continue
            es = [Entry(w, f"c{w}", cat_of[w]) for w in ws]
            for s in range(1, 60):
                if generate(es, size, s, n, True): found = ws; break
        print(mode, n, found, flush=True)
        if found: taken |= set(found)
        out.append({"mode": mode, "size": size, "n": n, "words": found})
        json.dump(out, open("workbench/mixed_sets.json", "w"), indent=1)
