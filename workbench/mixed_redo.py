"""Re-search one whole set without the vague words: mixed_redo.py <idx in mixed_sets2.json> <seconds> <out>"""
import sys, json, glob, random, time
sys.path.insert(0, "."); sys.path.insert(0, "workbench")
from crossword.data import Entry
from crossword.grid import generate
from mixed_pool import POOL
VAGUE = set("PEAK ISLE FAN BIB AXLE REEF WELL NEST FLAG DOME STEP ARCH".split())
idx, secs, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
sets = json.load(open("workbench/mixed_sets2.json")); s = sets[idx]; n, size = s["n"], s["size"]
book = set()
for f in glob.glob("data/puzzles/*.json"): book |= {p["word"] for p in json.load(open(f))["placed"]}
hard = {w for t, sx in json.load(open("workbench/hnew3.json")) for w in sx}
taken = book | hard | {w for i, sx in enumerate(sets) if i != idx for w in sx["words"]}
EXTRA = "ANVIL BADGE BRICK CORAL LASSO WHEEL PEDAL STOVE SHELF IBIS BUOY CRIB BOLT GEAR PIPE HINGE TRAY TUSK".split()
cat_of = {w: (w if c == "short" else c) for c, ws in POOL.items() for w in ws.split()}
for w in EXTRA: cat_of.setdefault(w, w)
pool = [w for w in cat_of if w not in taken and w not in VAGUE and len(w) <= 5]
rnd = random.Random(); t0 = time.time(); found = None
while time.time() - t0 < secs and not found:
    ws, cats = [], set()
    for w in rnd.sample(pool, len(pool)):
        if cat_of[w] in cats: continue
        ws.append(w); cats.add(cat_of[w])
        if len(ws) == n: break
    if len(ws) < n: continue
    es = [Entry(w, f"c{w}", "x") for w in ws]
    if any(generate(es, size, sd, n, True) for sd in range(1, 60)): found = ws
json.dump(found, open(out, "w")); print(idx, found)
