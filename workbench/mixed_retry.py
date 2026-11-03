"""Retry one failed mixed set: mixed_retry.py <mode> <size> <n> <seconds> <outfile>"""
import sys, json, random, time
sys.path.insert(0, "."); sys.path.insert(0, "workbench")
from crossword.data import Entry
from crossword.grid import generate
from mixed_pool import POOL
mode, size, n, secs, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
cat_of = {w: (w if c == "short" else c) for c, ws in POOL.items() for w in ws.split()}
taken = {w for s in json.load(open("workbench/mixed_sets.json")) if s["words"] for w in s["words"]}
pool = [w for w in cat_of if w not in taken and len(w) <= size]
rnd = random.Random(); t0 = time.time(); found = None
while time.time() - t0 < secs and not found:
    ws, cats = [], set()
    for w in rnd.sample(pool, len(pool)):
        if cat_of[w] in cats: continue
        ws.append(w); cats.add(cat_of[w])
        if len(ws) == n: break
    nl = sum(len(w) >= 7 for w in ws)
    if len(ws) < n or not 3 <= nl <= 6: continue
    es = [Entry(w, f"c{w}", cat_of[w]) for w in ws]
    for s in range(1, 60):
        if generate(es, size, s, n, True): found = ws; break
json.dump(found, open(out, "w")); print(mode, n, found)
