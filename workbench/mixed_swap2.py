"""Retry vague-word swaps for one set: mixed_swap2.py <index in mixed_sets2.json> <seconds> <out>"""
import sys, json, glob, random, time
sys.path.insert(0, "."); sys.path.insert(0, "workbench")
from crossword.data import Entry
from crossword.grid import generate
from mixed_pool import POOL
VAGUE = set("PEAK ISLE FAN BIB AXLE REEF WELL NEST FLAG DOME STEP ARCH".split())
idx, secs, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
if len(sys.argv) > 4: VAGUE = set(sys.argv[4].split(","))
sets = json.load(open("workbench/mixed_sets2.json"))
book = set()
for f in glob.glob("data/puzzles/*.json"): book |= {p["word"] for p in json.load(open(f))["placed"]}
hard = {w for t, s in json.load(open("workbench/hnew3.json")) for w in s}
taken = book | hard | {w for s in sets for w in s["words"]}
EXTRA = "ANVIL BADGE BRICK CORAL LASSO WHEEL PEDAL STOVE SHELF IBIS BUOY CRIB BOLT GEAR PIPE HINGE TRAY TUSK SADDLE PADDLE TROWEL STIRRUP BEACON ANTLER MITTEN LOCKET RIBBON BEETLE DAGGER KETTLE PEBBLE".split()
pool = [w for w in dict.fromkeys(EXTRA + [w for ws in POOL.values() for w in ws.split()]) if w not in taken and w not in VAGUE]
s = sets[idx]; size = s["size"]; bad = [w for w in s["words"] if w in VAGUE]
pool = [w for w in pool if len(w) <= (5 if s["mode"] == "easy" and s["n"] >= 7 else size)]
rnd = random.Random(); t0 = time.time(); found = None
while time.time() - t0 < secs and not found:
    combo = rnd.sample(pool, len(bad)); new = list(s["words"])
    for b, c in zip(bad, combo): new[new.index(b)] = c
    nl = sum(len(w) >= 7 for w in new)
    if s["n"] >= 7 and s["mode"] != "easy" and not 3 <= nl <= 6: continue
    es = [Entry(w, f"c{w}", "x") for w in new]
    if any(generate(es, size, sd, len(new), True) for sd in range(1, 60)): found = new
json.dump(found, open(out, "w")); print(idx, bad, "->", found)
