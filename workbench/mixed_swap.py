"""Swap vague filler words in workbench/mixed_sets.json for better short words, keeping every set fitting its grid."""
import sys, json, glob, itertools, time
sys.path.insert(0, ".")
from crossword.data import Entry
from crossword.grid import generate
VAGUE = set("PEAK ISLE FAN BIB AXLE REEF WELL NEST FLAG DOME STEP ARCH".split())
# better short words (concrete, picturable), best first
BETTER = "ANVIL BADGE BRICK CORAL LASSO WHEEL PEDAL STOVE SHELF IBIS BUOY CRIB BOLT GEAR PIPE HINGE TRAY TUSK SADDLE HELMET SCISSOR PADDLE TROWEL WHEELBARROW".split()
book = set()
for f in glob.glob("data/puzzles/*.json"):
    book |= {p["word"] for p in json.load(open(f))["placed"]}
hard = {w for t, s in json.load(open("workbench/hnew3.json")) for w in s}
sets = json.load(open("workbench/mixed_sets.json"))
taken = book | hard | {w for s in sets for w in s["words"]}
cands = [w for w in BETTER if w not in taken]
def fits(ws, size):
    es = [Entry(w, f"c{w}", "x") for w in ws]
    return any(generate(es, size, s, len(ws), True) for s in range(1, 80))
for s in sets:
    bad = [w for w in s["words"] if w in VAGUE]
    if not bad: continue
    size = s["size"]; done = False; t0 = time.time()
    pool = [w for w in cands if len(w) <= size and w not in s["words"]]
    for combo in itertools.permutations(pool[:14], len(bad)):
        new = list(s["words"])
        for b, c in zip(bad, combo): new[new.index(b)] = c
        nl = sum(len(w) >= 7 for w in new)
        if s["n"] >= 7 and s["mode"] != "easy" and not 3 <= nl <= 6: continue
        if fits(new, size):
            print(s["mode"], s["n"], bad, "->", list(combo), flush=True)
            s["words"] = new; cands = [w for w in cands if w not in combo]; done = True; break
        if time.time() - t0 > 60: break
    if not done: print("NO SWAP", s["mode"], s["n"], bad, flush=True)
json.dump(sets, open("workbench/mixed_sets2.json", "w"), indent=1)
