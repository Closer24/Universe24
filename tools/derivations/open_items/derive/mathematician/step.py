import numpy as np, random
random.seed(7); np.random.seed(7)
L=4
def sh(a,ax,s): return np.roll(a,-s,axis=ax)
def lap(a,g): return sum(g*(sh(a,ax,s)-a) for ax in range(3) for s in (1,-1))
def F(a,g,D): return lap(a,g)-D*a
mid=lambda W: W//2
def S(x,W,s,g,D):
    am,a,r=x; p=W*(a-am)+r-mid(W); pp=p+s*F(a,g,D)
    return (a, a+(pp+mid(W))//W, (pp+mid(W))%W)
def Sinv(x,W,s,g,D):
    a,ap,rp=x; pp=W*(ap-a)+rp-mid(W); p=pp-s*F(a,g,D)
    return (a-(p+mid(W))//W, a, (p+mid(W))%W)
def mirror(r,W): return (2*mid(W)-r)%W
def flip(r,W): return W-1-r
def T(x,W,m): am,a,r=x; return (a,am,m(r,W))
def rnd(lo,hi): return np.array(np.random.randint(lo,hi,size=(L,L,L)),dtype=object)
def eq(x,y): return all((u==v).all() for u,v in zip(x,y))
for W,name in [(600,'even'),(601,'odd')]:
    s,g,D=1,W//3//6*0+50,7
    inv_ok=tst_mir=tst_flip=0; n=300
    for _ in range(n):
        x=(rnd(-50,50),rnd(-50,50),rnd(0,W))
        inv_ok+=eq(Sinv(S(x,W,s,g,D),W,s,g,D),x)
        tst_mir+=eq(T(S(T(x,W,mirror),W,s,g,D),W,mirror),Sinv(x,W,s,g,D))
        tst_flip+=eq(T(S(T(x,W,flip),W,s,g,D),W,flip),Sinv(x,W,s,g,D))
    print(f"W {W} ({name}): S^-1 S = id {inv_ok}/{n};  T S T = S^-1 with mirror {tst_mir}/{n}, with flip {tst_flip}/{n}")
# boundary cases: force r=0 at some sites (even W, mirror)
W,s,g,D=600,1,50,7
fails=0
for _ in range(300):
    x=(rnd(-50,50),rnd(-50,50),rnd(0,W)); x[2][0,0,0]=0
    fails+= not eq(T(S(T(x,W,mirror),W,s,g,D),W,mirror),Sinv(x,W,s,g,D))
print("even W, mirror, r=0 at one site: T S T != S^-1 in",fails,"of 300")
# single-gear example
W=4; x=(np.array([0],dtype=object),np.array([0],dtype=object),np.array([0],dtype=object))
print("free gear W=4, state (0,0,r=0): p =",W*0+0-mid(W),"; mirror(0) =",mirror(0,W),"so T leaves p at",-2,"(not +2)")
