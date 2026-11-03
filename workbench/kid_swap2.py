"""Second pass: redo the themed puzzles whose swaps drifted off-theme, using only on-theme words.
Reads workbench/kid_sets.json (pass 1) and the originals; writes workbench/kid_sets2.json."""
import sys, json, glob, random, time, itertools
sys.path.insert(0, ".")
from crossword.data import Entry
from crossword.grid import generate
BAN = set(open("workbench/not_kid_friendly.txt").read().split())
sets = json.load(open("workbench/kid_sets.json"))
orig = [list(w) for t, w in json.load(open("workbench/hnew3.json"))] + [list(s["words"]) for s in json.load(open("workbench/mixed_sets.json"))]
THEME2 = {
 "Circus": "CLOWN POPCORN CAPE HOOP STAGE",
 "Trip": "CAMERA HOTEL AIRPORT LUGGAGE POSTCARD PASSPORT BOTTLE SUNHAT",
 "Kitchen B": "KNIFE PLATE TRAY",
 "Garden B": "SPIDER PEBBLE PEACOCK SCARECROW BUTTERFLY SHED POND PATH",
 "Small creatures": "SPIDER BEE ANT BUG",
 "Snacks": "COOKIE DONUT CANDY POPCORN",
 "Vegetables": "SQUASH GARLIC TURNIP SPROUT",
 "Nature": "VOLCANO RIVER POND LAKE STREAM PEBBLE DESERT",
 "Transport": "SUBWAY SLED BUGGY",
 "Winter clothes": "SCARF JACKET PAJAMAS SKIRT",
 "Desk": "TAPE GLUE PAPER MARKER STAPLER STAMP",
}
redo = [i for i, s in enumerate(sets) if s["title"] in THEME2]
redo.append(next(i for i, s in enumerate(sets) if s["title"] == "mixed easy" and s["n"] == 7 and "BOLT" in orig[i]))
book = set()
for f in glob.glob("data/puzzles/*.json"): book |= {p["word"] for p in json.load(open(f))["placed"]}
for i in redo: sets[i]["words"] = [w for w in orig[i] if w not in BAN]   # drop banned only; keep originals
taken = set(book) | {w for i, s in enumerate(sets) if i not in redo for w in s["words"]}
for i in redo:  # reserve the kept words of redone sets too
    taken |= set(sets[i]["words"])
rnd = random.Random(3)
GEN = "PUPPY KITTEN TURKEY ROOSTER PEACOCK PENGUIN OCTOPUS MOOSE CHIMP HEAD FOOT LEG BACK BELLY LIP CHEEK COOKIE DONUT CANDY PASTA TABLE BATH PEN BOX TOY JAR MOP ROPE SCHOOL HOTEL PINE TWIG BEE ANT BUG".split()
for i in redo:
    s = sets[i]; keep = s["words"]; need = s["n"] - len(keep); size = s["size"]
    cand = [w for w in THEME2.get(s["title"], " ".join(GEN)).split() if w not in taken and w not in BAN]
    if s["title"] == "mixed easy": cand = [w for w in GEN if w not in taken and len(w) <= 5]
    found = None; t0 = time.time()
    combos = list(itertools.combinations(cand, need)); rnd.shuffle(combos)
    for combo in combos:
        ws = keep + list(combo); nl = sum(len(w) >= 7 for w in ws)
        if s["n"] >= 7 and s["mode"] != "easy" and not 3 <= nl <= 6: continue
        es = [Entry(w, f"c{w}", "x") for w in ws]
        if any(generate(es, size, sd, len(ws), True) for sd in range(1, 60)): found = ws; break
        if time.time() - t0 > 80: break
    print(i + 53, s["title"], "->", [w for w in found if w not in keep] if found else "NOT FOUND", flush=True)
    if found: s["words"] = found; taken |= set(found)
json.dump(sets, open("workbench/kid_sets2.json", "w"), indent=1)
print("DONE")
