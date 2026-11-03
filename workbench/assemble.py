import sys, json, os, shutil, subprocess; sys.path.insert(0,'.'); sys.path.insert(0,sys.argv[1])
from crossword.data import Entry
from crossword.grid import generate
from caps import CAPS
from lib import C
import art_a, art_b, art_c, art_d, art_e
D={}
for m in (art_a,art_b,art_c,art_d,art_e): D.update(m.D)
ch=json.load(open(sys.argv[1]+'/chosen.json'))
allw=[]
for i in range(1,21):
    words=ch[str(i)][0]; allw+=words
    missing=[w for w in words if w not in D or w not in CAPS]
    assert not missing,(i,missing)
    es=[Entry(w,CAPS[w][1],CAPS[w][0]) for w in words]
    seed=next(s for s in range(1,2000) if generate(es,7,s,len(words)))
    pid=f"easy-{i:02d}"; d=f"drafts/{pid}"; os.makedirs(d,exist_ok=True)
    items=[]
    for w in words:
        c=C(); D[w](c); os.makedirs("hint_images", exist_ok=True); c.save(f"hint_images/{w}.png")
        items.append({"word":w,"category":CAPS[w][0],"caption":CAPS[w][1],"image":f"hint_images/{w}.png"})
    json.dump({"mode":"easy","min_words":len(words),"items":items},open(f"{d}/request.json","w"),indent=2)
    r=subprocess.run([".venv/bin/python","-m","crossword.category","draft","--input",f"{d}/request.json","--seed",str(seed),"--id",pid],capture_output=True,text=True)
    print(pid,len(words),seed,r.stdout.strip(),r.stderr.strip()[-200:])
assert len(allw)==len(set(allw))==116,(len(allw),len(set(allw)))
print("unique words:",len(set(allw)))
