import sys, itertools, json, random, glob; sys.path.insert(0,'.')
from crossword.data import Entry
from crossword.grid import generate
used=set()
for f in glob.glob('data/puzzles/*.json'):
    for p in json.load(open(f))['placed']: used.add(p['word'])
SIZE=8
POOLS=[ # (title, need, pool)
("Instruments",4,"DRUM FLUTE HARP PIANO BELL TRUMPET GUITAR VIOLIN"),
("Tools",4,"HAMMER SAW DRILL NAIL WRENCH AXE SCREW"),
("Space",4,"MOON PLANET ROCKET COMET ORBIT ALIEN"),
("Beach",4,"SAND WAVE TOWEL BUCKET SPADE UMBRELLA"),
("Camping",4,"TENT FIRE TORCH COMPASS BACKPACK LOG"),
("Sports",5,"GOAL NET RACKET SKATE SKI TROPHY WHISTLE HELMET"),
("Reptiles",5,"TURTLE LIZARD GECKO CROC GATOR COBRA IGUANA"),
("Kitchen",5,"PAN POT KETTLE WHISK FORK KNIFE PLATE BOWL TOASTER"),
("Bathroom",5,"SOAP BRUSH TUB SINK SHOWER MIRROR TOWEL"),
("Garden",5,"SEED RAKE HOSE FLOWER WORM SHED HOE"),
("Wild animals",6,"TIGER WOLF FOX GIRAFFE ELEPHANT RHINO KANGAROO CAMEL LLAMA YAK MOOSE"),
("Sea life",6,"TURTLE OCTOPUS DOLPHIN SQUID STARFISH JELLYFISH SEAHORSE SHRIMP OYSTER"),
("Insects",6,"BEE ANT SNAIL SPIDER WORM BUTTERFLY MOTH CRICKET"),
("Birds",6,"ROBIN PENGUIN DOVE PEACOCK FLAMINGO PIGEON FINCH TOUCAN HEN CHICK"),
("Fruit",6,"LEMON PEACH CHERRY MANGO LIME KIWI BANANA ORANGE BERRY COCONUT"),
("Vegetables",6,"BEAN BEET POTATO TOMATO CABBAGE PEPPER RADISH CELERY"),
("Food",6,"BREAD PIZZA PASTA PIE BUTTER MILK NOODLE SANDWICH"),
("Sweets",6,"DONUT COOKIE CANDY MUFFIN WAFFLE POPCORN HONEY TOAST SUGAR"),
("Clothes",6,"SHIRT DRESS SKIRT BOOT CAP SCARF JACKET BELT SANDAL"),
("School",6,"RULER GLOBE PAPER PAINT CHALK MAP DESK GLUE SCISSORS"),
("Home",7,"TABLE LAMP BED CLOCK PILLOW CURTAIN SHELF STOVE"),
("Play",7,"SLIDE DICE YOYO BLOCKS PUZZLE BUBBLE CARDS TENT"),
("Transport",7,"CAR PLANE TAXI TRUCK TRACTOR SLED RAFT HELICOPTER"),
("Weather",8,"RAIN WIND STORM FOG ICE HAIL LIGHTNING THUNDER"),
("Body",8,"EYE HAND FOOT ARM TOOTH TOE KNEE HEAD CHIN NECK"),
("Farm",8,"GOAT HEN LAMB CHICK BARN FENCE HAY SCARECROW TRACTOR"),
("Pets",8,"RABBIT HAMSTER KITTEN PUPPY GOLDFISH BUNNY TURTLE"),
("Fairy tale",8,"CROWN CASTLE SWORD WAND DRAGON TOWER SHIELD THRONE"),
("Places",8,"HOUSE SCHOOL BRIDGE TOWER BARN LIGHTHOUSE WINDMILL"),
("Pirates",8,"ANCHOR MAP CHEST COIN SWORD FLAG TELESCOPE PARROT"),
("Nature",8,"MOUNTAIN VOLCANO CAVE ISLAND DESERT FOREST WATERFALL CACTUS PALM"),
]
BAN=set("EEL CLAM".split())
if __name__=="__main__":
    out=[]
    u=set(used)
    for i,(t,n,pool) in enumerate(POOLS):
        words=[w for w in dict.fromkeys(pool.split()) if w not in u]
        found=None
        combos=list(itertools.combinations(words,n)); random.Random(i).shuffle(combos)
        for combo in combos[:4000]:
            es=[Entry(w,"x","c") for w in combo]
            for s in range(1,60):
                if generate(es,SIZE,s,n): found=(list(combo),s); break
            if found: break
        print(i+1,t,n,found, "pool left",len(words))
        if not found: print("FAIL"); continue
        u|=set(found[0]); out.append([t]+list(found))
    json.dump(out,open(sys.argv[1],'w'))
