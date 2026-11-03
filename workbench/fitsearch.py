"""Find an 8-word 9x9 set: fitsearch.py "keep words" "long pool" "short pool" seconds"""
import sys, random, time
sys.path.insert(0, ".")
from crossword.data import Entry
from crossword.grid import generate
keep, longs, shorts = (a.split() for a in sys.argv[1:4])
rnd = random.Random(3); t = time.time()
need = 8 - len(keep)
while time.time() - t < float(sys.argv[4]):
    nl = sum(len(w) >= 7 for w in keep)
    k = max(0, 3 - nl) + rnd.choice([0, 0, 1])
    ws = keep + rnd.sample(longs, min(k, len(longs), need)) + []
    ws += rnd.sample([w for w in shorts if w not in ws], need - (len(ws) - len(keep)))
    es = [Entry(w, f"c{w}", "x") for w in ws]
    for s in range(1, 40):
        if generate(es, 9, s, 8, True):
            print(ws, s, flush=True); sys.exit()
print("none")
