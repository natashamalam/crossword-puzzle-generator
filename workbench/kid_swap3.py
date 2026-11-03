"""Third pass: fit the remaining themed sets, allowing 1-2 extra weaker words to be swapped, on-theme words only.
kid_swap3.py <comma list of titles (use 'mixed88' for the easy mixed 7-keyword set)> <out json>"""
import sys, json, glob, random, time, itertools
sys.path.insert(0, ".")
from crossword.data import Entry
from crossword.grid import generate
BAN = set(open("workbench/not_kid_friendly.txt").read().split())
sets = json.load(open("workbench/kid_sets2.json"))
orig = [list(w) for t, w in json.load(open("workbench/hnew3.json"))] + [list(s["words"]) for s in json.load(open("workbench/mixed_sets.json"))]
POOLS = {
 "Kitchen B": "KNIFE PLATE TRAY PAN JUG MIXER BLENDER MUG",
 "Small creatures": "SPIDER BEE ANT BUG WASP TADPOLE HAMSTER MINNOW GERBIL",
 "Snacks": "COOKIE DONUT CANDY POPCORN NACHOS CRACKER RAISINS",
 "Vegetables": "SQUASH GARLIC TURNIP SPROUT EGGPLANT PARSNIP",
 "Nature": "VOLCANO RIVER POND LAKE STREAM DESERT SHORE VALLEY MOSS WATERFALL",
 "Transport": "SUBWAY SLED BUGGY CARRIAGE TUGBOAT SUBMARINE AMBULANCE",
 "Desk": "TAPE GLUE PAPER MARKER STAPLER STAMP PEN BINDER SCREEN LAPTOP PRINTER",
 "mixed88": "PUPPY KITTEN TURKEY ROOSTER PEACOCK PENGUIN MOOSE CHIMP HEAD FOOT LEG BACK BELLY LIP CHEEK COOKIE DONUT CANDY PASTA PEN BOX TOY JAR MOP ROPE BEE ANT BUG PINE TWIG",
}
book = set()
for f in glob.glob("data/puzzles/*.json"): book |= {p["word"] for p in json.load(open(f))["placed"]}
titles = sys.argv[1].split(","); out = {}
rnd = random.Random()
def idx_of(t):
    if t == "mixed88": return next(i for i, s in enumerate(sets) if s["title"] == "mixed easy" and s["n"] == 7 and "BOLT" in orig[i])
    return next(i for i, s in enumerate(sets) if s["title"] == t)
others_taken = lambda skip: book | {w for i, s in enumerate(sets) if i not in skip for w in s["words"]}
for t in titles:
    i = idx_of(t); s = sets[i]; size = s["size"]
    base = [w for w in orig[i] if w not in BAN] if len(s["words"]) < s["n"] or True else s["words"]
    taken = others_taken({i})
    maxlen = 5 if t == "mixed88" else 9
    pool = [w for w in POOLS[t].split() if w not in taken and w not in BAN and len(w) <= maxlen]
    found = None; t0 = time.time()
    for m in (0, 1, 2, 3):
        need = s["n"] - len(base) + m
        if need > len(pool) or need < 0 or m > len(base): continue
        tm = time.time()
        while time.time() - tm < 35 and not found:
            drop = set(rnd.sample(base, m)) if m else set()
            ws = [w for w in base if w not in drop] + rnd.sample(pool, need)
            nl = sum(len(w) >= 7 for w in ws)
            if s["n"] >= 7 and s["mode"] != "easy" and not 3 <= nl <= 6: continue
            es = [Entry(w, f"c{w}", "x") for w in ws]
            if any(generate(es, size, sd, len(ws), True) for sd in range(1, 50)): found = ws
        if found: break
    print(t, "->", found if found else "NOT FOUND", flush=True)
    if found: out[t] = found
json.dump(out, open(sys.argv[2], "w"))
print("DONE")
