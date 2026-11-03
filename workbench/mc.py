import sys,json,random,time; sys.path.insert(0,'.'); sys.path.insert(0,sys.argv[1])
from msearch import used, BAN
from gen2 import gen2
SIZE=int(sys.argv[3]) if len(sys.argv)>3 else 8
T=json.load(open(sys.argv[2]))   # [title,n_total,nlong_min,longs,shorts]
u=set(used); res=[]; rnd=random.Random(11)
for t,n,nl,L,Sx in T:
    L=[w for w in L.split() if w not in u]; Ss=[w for w in Sx.split() if w not in u and w not in BAN]
    found=None; t0=time.time(); it=0
    while time.time()-t0<float(sys.argv[4]) and not found:
        it+=1
        k=min(len(L),nl+ (1 if rnd.random()<0.3 else 0))
        c=rnd.sample(L,k)+rnd.sample(Ss,n-k)
        for sd in range(1,30):
            p=gen2(c,SIZE,sd,n)
            if p: found=(c,sd,len([w for w in c if len(w)==8])); break
    print(t,n,found,it,flush=True)
    if found: u|=set(found[0]); res.append([t]+list(found))
json.dump(res,open(sys.argv[2]+'.out','w'))
