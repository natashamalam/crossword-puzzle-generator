"""Replace the words in workbench/not_kid_friendly.txt with familiar kid words, keeping every set fitting its grid.
Reads workbench/hnew3.json (hard) and workbench/mixed_sets.json (mixed); writes workbench/kid_sets.json."""
import sys, json, glob, random, time
sys.path.insert(0, ".")
from crossword.data import Entry
from crossword.grid import generate

BAN = set(open("workbench/not_kid_friendly.txt").read().split())
THEME = {  # preferred replacements by puzzle title, best first
 "Bakery": "COOKIE DONUT BREAD CUPCAKE PIE", "Music II": "RECORDER TRIANGLE ORGAN",
 "Celebration": "GIFT PARADE COSTUME MEDAL CARD SPARKLER LANTERN", "Trees": "PINE TRUNK TWIG STUMP",
 "Tools 2": "TOOLBOX HOSE MOP ROPE", "Playground": "BENCH HOOP ROPE", "Circus": "CLOWN POPCORN CAPE HOOP COSTUME",
 "Toys": "BLOCK YOYO SPINNER BUBBLE", "Trip": "CAMERA HOTEL BOTTLE SUNHAT", "Animals B": "MOOSE PENGUIN OCTOPUS TURKEY",
 "Kitchen B": "KNIFE PLATE TRAY", "Garden B": "SCARECROW SPIDER HOSE PEBBLE BENCH", "Small creatures": "SPIDER BEE ANT BUG",
 "Snacks": "COOKIE DONUT CANDY PIE CUPCAKE", "Vegetables": "SQUASH GARLIC TURNIP SPROUT", "Nature": "VOLCANO RIVER POND LAKE STREAM PEBBLE",
 "Transport": "SUBWAY SLED BUGGY", "Winter clothes": "SCARF JACKET SKIRT PAJAMAS", "Desk": "TAPE GLUE PAPER MARKER STAPLER STAMP",
}
GENERAL = ("PUPPY KITTEN TURKEY ROOSTER PEACOCK PENGUIN OCTOPUS MOOSE SPIDER CHIMP HEAD FOOT ARM LEG BACK BELLY TOE LIP CHEEK "
           "COOKIE DONUT CANDY BREAD PIE PASTA POPCORN SCARF JACKET SKIRT PAJAMAS TABLE BATH KNIFE PLATE TAPE GLUE PAPER MARKER "
           "STAMP PEN BOX TOY JAR MOP HOSE ROPE TOOLBOX RIVER POND LAKE STREAM PEBBLE DESERT SUBWAY SLED BUGGY ORGAN RECORDER "
           "TRIANGLE GIFT PARADE MEDAL CARD CLOWN CAPE HOOP BLOCK YOYO BUBBLE CAMERA HOTEL BOTTLE SCHOOL CHURCH PALACE TRUNK TWIG "
           "PINE VOLCANO SQUASH GARLIC SCARECROW BENCH BEE ANT BUG").split()
hard = json.load(open("workbench/hnew3.json")); mixed = json.load(open("workbench/mixed_sets.json"))
sets = [{"title": t, "mode": "hard", "size": 9, "n": len(w), "words": w} for t, w in hard]
sets += [{"title": f"mixed {s['mode']}", "mode": s["mode"], "size": s["size"], "n": s["n"], "words": s["words"]} for s in mixed]
book = set()
for f in glob.glob("data/puzzles/*.json"): book |= {p["word"] for p in json.load(open(f))["placed"]}
taken = set(book) | {w for s in sets for w in s["words"] if w not in BAN}
rnd = random.Random(11)
log = open("workbench/kid_swap.log", "w")
for i, s in enumerate(sets, 53):
    bad = [w for w in s["words"] if w in BAN]
    if not bad: continue
    size = s["size"]; maxlen = 5 if (s["mode"] == "easy" and s["n"] >= 7) else 8
    theme = [w for w in THEME.get(s["title"], "").split() if w not in taken and w not in BAN and len(w) <= maxlen]
    gen = [w for w in dict.fromkeys(GENERAL) if w not in taken and w not in BAN and w not in theme and len(w) <= maxlen]
    keep = [w for w in s["words"] if w not in BAN]; found = None; t0 = time.time()
    while time.time() - t0 < 60 and not found:
        pick = []
        pool_t = theme[:]; rnd.shuffle(pool_t)
        for _ in range(len(bad)):
            src = pool_t if pool_t and rnd.random() < 0.8 else gen
            w = rnd.choice(src)
            if w in pick or w in keep: break
            pick.append(w)
        if len(pick) < len(bad): continue
        ws = keep + pick
        nl = sum(len(w) >= 7 for w in ws)
        if s["n"] >= 7 and s["mode"] != "easy" and not 3 <= nl <= 6: continue
        es = [Entry(w, f"c{w}", "x") for w in ws]
        if any(generate(es, size, sd, len(ws), True) for sd in range(1, 60)): found = ws
    msg = f"{i} {s['title']}: {bad} -> {[w for w in found if w not in keep] if found else 'NOT FOUND'}"
    print(msg, flush=True); log.write(msg + "\n"); log.flush()
    if found:
        s["words"] = found; taken |= set(found)
json.dump(sets, open("workbench/kid_sets.json", "w"), indent=1)
print("DONE")
