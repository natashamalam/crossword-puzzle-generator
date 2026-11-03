"""Search a 9x9 fit for puzzles that did not fit. fitpools.py <seconds each> ; writes workbench/hnew2.json"""
import sys, json, glob, itertools, time
sys.path.insert(0, ".")
from crossword.data import Entry
from crossword.grid import generate
book = set()
for f in glob.glob("data/puzzles/*.json"):
    book |= {p["word"] for p in json.load(open(f))["placed"]}
sets = json.load(open("workbench/hnew.json"))
sets = [[t, s.split()] for t, s in sets]
sets[19][1] = [w for w in sets[19][1] if w != "PEANUT"] + ["SALAD"]
# title -> (must keep, extra pool)
P = {
 "Playground": ("SEESAW SANDBOX CHALK", "FOUNTAIN HELMET BENCH LADDER SANDAL PEBBLE KNEEPAD"),
 "Circus": ("MAGICIAN ACROBAT", "JUGGLER TRAPEZE STILTS CLOWN UNICYCLE CANNON CAPE HOOP"),
 "Food": ("BROCCOLI AVOCADO PRETZEL", "WAFFLE CEREAL YOGURT NOODLE SALAD OMELET RAISIN"),
 "Animals A": ("REINDEER SHEEPDOG", "ANTELOPE BISON TAPIR BADGER SKUNK CRANE BLUEBIRD LYNX PUMA"),
 "Small creatures": ("MOSQUITO SCORPION PARAKEET", "SNAIL WALRUS SALMON TROUT WASP NEWT GNAT LYNX"),
 "Snacks": ("LOLLIPOP POPCORN", "CARAMEL PUDDING CRACKER PICKLE RAISIN PEANUT SUNDAE CASHEW NOODLE WAFFLE YOGURT CEREAL"),
 "Vegetables": ("CUCUMBER", "SPINACH LETTUCE RADISH TURNIP GARLIC OKRA LEEK PARSNIP SPROUT CHILI ZUCCHINI BEETROOT"),
 "Nature": ("DAFFODIL RAINDROP PINECONE", "BOULDER PUDDLE GLACIER CRATER MEADOW PEBBLE FERN ACORN CLIFF MOSS"),
 "House": ("DOORBELL BIRDBATH DOGHOUSE", "CHIMNEY MAILBOX SHUTTER CURTAIN CARPET WINDOW DRAWER BASKET PILLOW STOOL"),
 "Winter clothes": ("MITTENS EARMUFFS", "SLIPPERS SCARF SWEATER CARDIGAN BOOT HOOD PAJAMAS OVERALLS"),
 "Desk": ("KEYBOARD ENVELOPE", "STAPLER MARKER FOLDER EASEL CANVAS GLUE STAMP NOTEPAD SHARPENER"),
}
def ok(ws, n):
    nl = sum(len(w) >= 7 for w in ws)
    return n < 7 or 3 <= nl <= 6
def fit(ws):
    es = [Entry(w, f"c{w}", "x") for w in ws]
    for s in range(1, 40):
        if generate(es, 9, s, len(ws), True): return s
out = []; taken = set()
for t, ws in sets:
    n = len(ws)
    if t in P:
        must, pool = (x.split() for x in P[t]); pool = [w for w in pool if w not in taken and w not in book and w not in must]
        # prefer the words I listed first
        t0 = time.time(); best = None
        for combo in itertools.combinations(pool, n - len(must)):   # priority order: first fit wins
            ws2 = must + list(combo)
            if ok(ws2, n) and fit(ws2): best = ws2; break
            if time.time() - t0 > float(sys.argv[1]): break
        ws = best or ws
        print(t, "FOUND" if best else "NOT FOUND", ws, flush=True)
    taken |= set(ws); out.append([t, ws])
json.dump(out, open("workbench/hnew2.json", "w"), indent=0)
