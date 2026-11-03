"""Random search for one puzzle: fitone.py "<title>" "<must>" "<pool>" <n words> <seconds> <outfile>"""
import sys, random, time, json
sys.path.insert(0, ".")
from crossword.data import Entry
from crossword.grid import generate
title, must, pool, n, secs, out = sys.argv[1], sys.argv[2].split(), sys.argv[3].split(), int(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
rnd = random.Random(hash(title) % 1000); t0 = time.time(); found = None
while time.time() - t0 < secs and not found:
    ws = must + rnd.sample([w for w in pool if w not in must], n - len(must))
    nl = sum(len(w) >= 7 for w in ws)
    if n >= 7 and not 3 <= nl <= 6: continue
    es = [Entry(w, f"c{w}", "x") for w in ws]
    for s in range(1, 60):
        if generate(es, 9, s, n, True): found = ws; break
json.dump([title, found], open(out, "w")); print(title, found)
