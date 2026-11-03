import sys,json,random; sys.path.insert(0,'.'); sys.path.insert(0,sys.argv[1])
from msearch import used, BAN
from crossword.data import Entry
from crossword.grid import generate
T=[ # title, n_long, longs, shorts
("Wild animals",3,"ELEPHANT KANGAROO SQUIRREL HEDGEHOG DINOSAUR PLATYPUS","WOLF YAK CAMEL LLAMA FOX TIGER GIRAFFE RHINO MOOSE BEAR-X"),
("School",3,"BACKPACK NOTEBOOK COMPUTER SCISSORS CALENDAR KEYBOARD","RULER GLOBE PAPER GLUE DESK MAP CHALK PAINT"),
("Weather",3,"RAINCOAT SUNSHINE SNOWBALL SNOWFLAKE","RAIN WIND FOG HAIL FROST BREEZE DEW STORM ICE THUNDER"),
("Food",4,"SANDWICH PANCAKES MUSHROOM BROCCOLI SPAGHETTI","PIZZA MILK SALAD BREAD NOODLE HAM TACO PIE BEAN BEET"),
("Sports",4,"FOOTBALL BASEBALL SNOWBALL SKATEBOARD","NET SKI RACKET WHISTLE TROPHY SKATE GOAL HELMET"),
("Outdoors",4,"CAMPFIRE MOUNTAIN BACKPACK UMBRELLA TREASURE","TENT TORCH LOG HILL LAKE PALM DUNE CAVE"),
("Travel",5,"AIRPLANE MOTORBIKE ELEVATOR MOUNTAIN BACKPACK","CAR TAXI JET SLED RAFT TRUCK SUBWAY"),
("Fairy tale",5,"PRINCESS TREASURE UMBRELLA CAMPFIRE DINOSAUR","CROWN CASTLE SWORD WAND DRAGON TOWER HARP GEM RING"),
]
u=set(used)
res=[]
rnd=random.Random(3)
for t,nl,L,Sx in T:
    L=[w for w in L.split() if w not in u and len(w)==8]
    Ss=[w for w in Sx.replace("-X","").split() if w not in u and w not in BAN and 3<=len(w)<=6]
    found=None
    for it in range(60000):
        c=rnd.sample(L,min(nl,len(L)))+rnd.sample(Ss,8-min(nl,len(L)))
        es=[Entry(w,"x","c") for w in c]
        for sd in range(1,25):
            if generate(es,8,sd,8): found=(c,sd);break
        if found:break
    print(t,nl,found,flush=True)
    if found: u|=set(found[0]); res.append([t]+list(found))
json.dump(res,open(sys.argv[1]+'/m8.json','w'))
