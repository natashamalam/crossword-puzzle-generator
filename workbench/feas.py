import sys; sys.path.insert(0,'.'); sys.path.insert(0,sys.argv[1])
from words import P
from crossword.data import Entry
from crossword.grid import generate
allw=[w for p in P for w,_,_ in p]
print(len(allw),len(set(allw)),[w for w in set(allw) if allw.count(w)>1])
for i,p in enumerate(P,1):
    es=[Entry(w,c,cat) for w,cat,c in [(w,cat,cap) for w,cat,cap in p]]
    best=None
    for seed in range(1,400):
        pz=generate(es,7,seed,1)
        if pz and (best is None or len(pz.placed)>len(best[1].placed)): best=(seed,pz)
        if best and len(best[1].placed)==len(p): break
    print(i,len(p),best[0] if best else None,len(best[1].placed) if best else 0)
