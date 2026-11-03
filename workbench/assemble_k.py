"""Build drafts kid-01..kid-48 (book puzzles 53-100) from workbench/kid_sets4.json.
Run from the repo root: .venv/bin/python workbench/assemble_k.py"""
import sys, json, os, subprocess, importlib
sys.path.insert(0, '.'); sys.path.insert(0, 'workbench')
from crossword.data import Entry
from crossword.grid import generate
from lib import C
MODS = "art_a art_b art_c art_d art_e art_m1 art_m1x art_m2 art_m3 art_m4 art_fix1 art_fix2 art_h1 art_h2 art_h3 art_h4 art_h5 art_h6 art_k1 art_k2 art_k3 art_k4 art_k5 art_k6 art_k7 art_k8".split()
D = {}
for m in MODS: D.update(importlib.import_module(m).D)   # later modules override earlier
from caps_m import CAPS_M
from caps_h import CAPS_H
from caps_k import CAPS_K
CAPS = {**CAPS_M, **CAPS_H, **CAPS_K}
sets = json.load(open('workbench/kid_sets4.json'))
allw = []
for i, s in enumerate(sets, 1):
    words, size, mode = s['words'], s['size'], s['mode']
    allw += words
    miss = [w for w in words if w not in D or w not in CAPS]
    assert not miss, (i, miss)
    es = [Entry(w, CAPS[w][1], CAPS[w][0]) for w in words]
    pid = f"kid-{i:02d}"; d = f"drafts/{pid}"; os.makedirs(d, exist_ok=True)
    seed = next((x for x in range(1, 5000) if generate(es, size, x, len(words), True)), None)
    assert seed, (i, s['title'], 'no seed')
    items = []
    for w in words:
        c = C(); D[w](c); c.save(f"{d}/{w}.png")
        items.append({"word": w, "category": CAPS[w][0], "caption": CAPS[w][1], "image": f"{d}/{w}.png"})
    json.dump({"mode": mode, "min_words": len(words), "free_start": True, "items": items}, open(f"{d}/request.json", "w"), indent=2)
    r = subprocess.run([".venv/bin/python", "-m", "crossword.category", "draft", "--input", f"{d}/request.json", "--seed", str(seed), "--id", pid], capture_output=True, text=True)
    print(pid, s['title'], mode, len(words), seed, r.stdout.strip()[:80], r.stderr.strip()[-200:], flush=True)
assert len(allw) == len(set(allw)), "dups"
print("total", len(allw))
