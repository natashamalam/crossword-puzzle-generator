"""Fourth pass: replace newly rejected words (see not_kid_friendly.txt) in workbench/kid_sets3.json -> kid_sets4.json."""
import sys, json, glob, random, time
sys.path.insert(0, ".")
from crossword.data import Entry
from crossword.grid import generate
BAN = set(open("workbench/not_kid_friendly.txt").read().split())
sets = json.load(open("workbench/kid_sets3.json"))
POOLS = {
 "Music II": "ORGAN XYLOPHONE HARMONICA SAXOPHONE MICROPHONE",
 "Celebration": "GIFT MEDAL CARD SPARKLER BALLOONS PRESENT TROPHY CANDLE",
 "Tools 2": "ROPE FUNNEL TAPE SPONGE BRUSH BROOM",
 "Transport": "TRACTOR STROLLER SUBWAY BUGGY AMBULANCE CARRIAGE HELICOPTER MOTORBIKE",
 "Small creatures": "HAMSTER MINNOW GERBIL SPIDER BEE BUG WASP PUPPY",
}
GENERAL = ("PUPPY KITTEN TURKEY ROOSTER PENGUIN OCTOPUS CHIMP HEAD FOOT BACK BELLY TOE CHEEK COOKIE CANDY PASTA TABLE BATH "
           "BOX TOY JAR ROPE SCHOOL HOTEL PINE TWIG BEE ANT KNIFE PLATE TRAY CARD GIFT BIKE").split()
book = set()
for f in glob.glob("data/puzzles/*.json"): book |= {p["word"] for p in json.load(open(f))["placed"]}
rnd = random.Random(5)
for i, s in enumerate(sets, 53):
    bad = [w for w in s["words"] if w in BAN]
    if not bad: continue
    keep = [w for w in s["words"] if w not in BAN]
    taken = book | {w for j, x in enumerate(sets) if j != i - 53 for w in x["words"]}
    themed = s["title"] in POOLS
    maxlen = 5 if (s["mode"] == "easy" and s["n"] >= 7) else 9
    pool = [w for w in (POOLS[s["title"]].split() if themed else GENERAL) if w not in taken and w not in BAN and len(w) <= maxlen]
    found = None
    for m in (0, 1, 2):
        need = len(bad) + m; t0 = time.time()
        if need > len(pool) or m > len(keep): continue
        while time.time() - t0 < 40 and not found:
            drop = set(rnd.sample(keep, m)) if m else set()
            ws = [w for w in keep if w not in drop] + rnd.sample(pool, need)
            nl = sum(len(w) >= 7 for w in ws)
            if s["n"] >= 7 and s["mode"] != "easy" and not 3 <= nl <= 6: continue
            es = [Entry(w, f"c{w}", "x") for w in ws]
            if any(generate(es, s["size"], sd, len(ws), True) for sd in range(1, 60)): found = ws
        if found: break
    print(i, s["title"], bad, "->", found if found else "NOT FOUND", flush=True)
    if found: s["words"] = found
json.dump(sets, open("workbench/kid_sets4.json", "w"), indent=1)
print("DONE")
