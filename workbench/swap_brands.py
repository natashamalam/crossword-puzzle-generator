"""Brand-safe swaps in applied puzzles (run from the repo root): 007 JEEP->CAR (re-laid out), 073 PUMA->ORCA, 100 JAGUAR->FARMER."""
import sys, json, importlib, os
sys.path.insert(0, '.'); sys.path.insert(0, 'workbench')
from pathlib import Path
from lib import C
from crossword.data import Entry
from crossword.category import draft_puzzle
from caps_k import CAPS_K
from caps_h import CAPS_H
CAPS = {**CAPS_H, **CAPS_K}
D = {}
for m in ("art_h1", "art_h2", "art_h3", "art_h4", "art_h5", "art_h6", "art_k9"): D.update(importlib.import_module(m).D)
def png(w):
    p = f"hint_images/{w}.png"; c = C(); D[w](c); c.save(p); return p

def inplace(num, old, new):
    f = f"data/puzzles/{num}.json"; d = json.load(open(f))
    p = next(x for x in d['placed'] if x['word'] == old)
    assert len(old) == len(new)
    for i, ch in enumerate(new):
        r, c = (p['row'], p['col'] + i) if p['across'] else (p['row'] + i, p['col'])
        assert d['cells'][r][c] in (old[i], ch) and (d['cells'][r][c] == old[i]), (num, i)
        d['cells'][r][c] = ch
    p.update(word=new, category=CAPS[new][0], clue=CAPS[new][1], image=png(new))
    json.dump(d, open(f, "w")); os.remove(f"hint_images/{old}.png")

inplace("073", "PUMA", "ORCA")
inplace("100", "JAGUAR", "FARMER")
# puzzle 7: rebuild with CAR instead of JEEP
old = json.load(open("data/puzzles/007.json"))
es = [Entry(x['word'] if x['word'] != 'JEEP' else 'CAR', x['clue'] if x['word'] != 'JEEP' else "A small vehicle with four wheels", 'vehicle', x['image'] if x['word'] != 'JEEP' else png('CAR')) for x in old['placed']]
for seed in range(1, 400):
    try:
        d = draft_puzzle(es, 'easy', 6, seed, None, 5, True)
    except ValueError:
        continue
    if not d['left_out']: break
out = {k: d[k] for k in ("mode", "size", "cells", "starters", "placed")}
json.dump(out, open("data/puzzles/007.json", "w")); os.remove("hint_images/JEEP.png")
print("seed", seed, [p['word'] for p in d['placed']])
