import sys,random,itertools; sys.path.insert(0,'.')
from crossword.data import Entry
from crossword.grid import generate
pool="HIPPO CAMEL KOALA RHINO OTTER SNAKE MOOSE LLAMA LEMUR GORILLA CHEETAH MEERKAT YAK PONY TAPIR".split()
import collections
best=collections.Counter()
rng=random.Random(5)
for _ in range(3000):
    combo=rng.sample(pool,7)
    es=[Entry(w,"x","c") for w in combo]
    for seed in range(1,15):
        pz=generate(es,7,seed,1)
        if pz: best[len(pz.placed)]+=1
print(best)
