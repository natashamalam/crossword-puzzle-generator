import sys,json,itertools,random; sys.path.insert(0,'.'); sys.path.insert(0,sys.argv[1])
from msearch import used
from crossword.data import Entry
from crossword.grid import generate
ch=json.load(open(sys.argv[1]+'/mchosen.json'))
u=set(used)
for t,ws,s in ch: u|=set(ws)
P={"Pets":"PUPPY KITTEN BUNNY BONE LEASH COLLAR CAGE TOY BED BOWL HAMSTER RABBIT FISH CAT DOG PAW TAIL",
"Fairy tale":"KING QUEEN CROWN CASTLE SWORD WAND DRAGON TOWER HARP ELF RING GIANT MAGIC SHIELD GEM OGRE",
"Places":"HOUSE SCHOOL BRIDGE TOWER BARN ZOO PARK SHOP CABIN HUT MILL FARM STORE CAFE ROAD PIER INN"}
new={}
for t,pool in P.items():
    words=[w for w in dict.fromkeys(pool.split()) if w not in u]
    combos=list(itertools.combinations(words,8)); random.Random(5).shuffle(combos)
    found=None
    for c in combos[:20000]:
        es=[Entry(w,"x","c") for w in c]
        for sd in range(1,60):
            if generate(es,8,sd,8): found=(list(c),sd);break
        if found:break
    print(t,found,len(words))
    if found: u|=set(found[0]); new[t]=[t]+list(found)
order=["Instruments","Tools","Space","Beach","Camping","Sports","Reptiles","Kitchen","Bathroom","Garden","Wild animals","Sea life","Insects","Birds","Fruit","Vegetables","Food","Sweets","Clothes","School","Home","Play","Transport","Weather","Body","Farm","Pets","Fairy tale","Places","Pirates","Nature"]
allp={c[0]:c for c in ch}; allp.update(new)
final=[allp[k] for k in order]
json.dump(final,open(sys.argv[1]+'/mfinal.json','w'))
print(len(final))
