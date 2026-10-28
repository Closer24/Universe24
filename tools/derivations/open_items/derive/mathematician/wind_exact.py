import numpy as np
from fractions import Fraction
np.random.seed(3); L=4
def sh(a,ax,s): return np.roll(a,-s,axis=ax)
SP=[(ax,s) for ax in range(3) for s in (1,-1)]
def wind_density(n,b,w,g,D):
    R=g; S=2*w-D-6*R
    own=w*(n*n+b*b)-S*n*b-n*sum(R*sh(b,ax,sg) for ax,sg in SP)
    shared=sum(R*(b-sh(b,ax,sg))*(n+sh(n,ax,sg)) for ax,sg in SP)
    return 2*own-shared
W,g,D=6000,600,30
am=np.array(np.random.randint(-3000,3000,(L,L,L)),dtype=object); a=am+np.array(np.random.randint(-200,200,(L,L,L)),dtype=object)
am=am+Fraction(0); a=a+Fraction(0)
E=set()
for t in range(30):
    E.add(wind_density(a,am,W,g,D).sum())
    F=sum(g*(sh(a,ax,sg)-a) for ax,sg in SP)-D*a
    am,a=a,2*a-am+F/W
print("exact (rational) leapfrog: distinct total-wind values over 30 ticks:",len(E))
