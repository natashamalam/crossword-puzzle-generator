import sys, json, os, subprocess; sys.path.insert(0,'.'); sys.path.insert(0,sys.argv[1])
from crossword.data import Entry
from crossword.grid import generate
import importlib
from lib import C
D={}
for name in sys.argv[3].split(','):
    D.update(importlib.import_module(name).D)       # later modules override earlier
from caps_m import CAPS_M as CAPS
from caps_h import CAPS_H
CAPS = {**CAPS, **CAPS_H}
fin=json.load(open(sys.argv[1]+'/'+sys.argv[2]))
mode=sys.argv[4]; size=int(sys.argv[5]); prefix=sys.argv[6]
allw=[]
for i,(title,words,seed0) in enumerate(fin,1):
    allw+=words
    missing=[w for w in words if w not in D or w not in CAPS]
    assert not missing,(title,missing)
    es=[Entry(w,CAPS[w][1],CAPS[w][0]) for w in words]
    pid=f"{prefix}-{i:02d}"; d=f"drafts/{pid}"; os.makedirs(d,exist_ok=True)
    seed=None
    for s in range(1,5000):
        # use the same placement generator as the CLI
        if generate(es,size,s,len(words),True): seed=s;break
    assert seed,(title,"no seed")
    items=[]
    for w in words:
        c=C(); D[w](c); c.save(f"{d}/{w}.png")
        items.append({"word":w,"category":CAPS[w][0],"caption":CAPS[w][1],"image":f"{d}/{w}.png"})
    json.dump({"mode":mode,"min_words":len(words),"free_start":True,"items":items},open(f"{d}/request.json","w"),indent=2)
    r=subprocess.run([".venv/bin/python","-m","crossword.category","draft","--input",f"{d}/request.json","--seed",str(seed),"--id",pid],capture_output=True,text=True)
    print(pid,title,len(words),seed,r.stdout.strip()[:90],r.stderr.strip()[-200:],flush=True)
assert len(allw)==len(set(allw)),"dups"
print("total",len(allw))
