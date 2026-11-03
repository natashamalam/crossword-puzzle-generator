import json
ex=set(json.load(open('ex_h2.json')))|{'DOORBELL','BIRDBATH','DOGHOUSE','ROOF','BASKET','STOOL','PLATE','PILLOW'}
json.dump(sorted(ex),open('ex_h3.json','w'))
T=json.load(open('ht2.json'))[1:]
add={"Transport":" TRACTOR CARAVAN AIRSHIP STEAMER TROLLEY","Winter clothes":" JACKET BOOTS TROUSER SWEATER PAJAMAS","Desk":" NOTEPAD PENCILS CRAYONS COMPASS CALCULATOR"[:0]+" NOTEPAD PENCILS CRAYONS","Animals B":" CHEETAH LEOPARD GORILLA PELICAN","Kitchen B":" CUTLERY FREEZER SPATULA","Garden B":" BEEHIVE TRELLIS","Food":" PEANUTS AVOCADO PUMPKIN CARROTS"}
for t in T: t[3]+=add.get(t[0],"")
json.dump(T,open('ht3.json','w'))
