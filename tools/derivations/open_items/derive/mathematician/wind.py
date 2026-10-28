import numpy as np
np.random.seed(3); L=4
def sh(a,ax,s): return np.roll(a,-s,axis=ax)
SP=[(ax,s) for ax in range(3) for s in (1,-1)]
def step(am,a,r,W,g,D,s=1):
    F=sum(g*(sh(a,ax,sg)-a) for ax,sg in SP)-D*a
    p=W*(a-am)+r-W//2; pp=p+s*F
    return a, a+(pp+W//2)//W, (pp+W//2)%W
def wind_density(n,b,w,g,D):
    R=g; S=2*w-D-6*R
    own=w*(n*n+b*b)-S*n*b-n*sum(R*sh(b,ax,sg) for ax,sg in SP)
    shared=sum(R*(b-sh(b,ax,sg))*(n+sh(n,ax,sg)) for ax,sg in SP)
    return 2*own-shared
W,g,D=6000,600,30   # lambda = g/W = 0.1 < 1/3: stable
am=np.array(np.random.randint(-3000,3000,(L,L,L)),dtype=object); a=am+np.array(np.random.randint(-200,200,(L,L,L)),dtype=object)
r=np.array(np.random.randint(0,W,(L,L,L)),dtype=object)
E=[]
for t in range(200):
    E.append(int(wind_density(a,am,W,g,D).sum()))
    am,a,r=step(am,a,r,W,g,D)
E=np.array(E,dtype=float)
print("total wind: first",int(E[0])," min",int(E.min())," max",int(E.max()), " relative spread %.2e"%((E.max()-E.min())/E[0]), " distinct values",len(set(E.tolist())))
# local density can be negative
n=np.zeros((L,L,L),dtype=object); b=np.zeros((L,L,L),dtype=object)
for ax,sg in SP:
    idx=[0,0,0]; idx[ax]=sg%L; n[tuple(idx)]=-1; b[tuple(idx)]=1
print("local wind at a site with n=b=0, neighbours n=-1,b=+1:",int(wind_density(n,b,W,g,D)[0,0,0]))
