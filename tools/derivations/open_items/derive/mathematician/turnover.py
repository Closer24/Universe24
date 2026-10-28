# one time gear, no neighbours: w a+ + r+ = 2 w a - w a- + F(a) + r, F(a) = -D a; the act M = turnover T at the
# weak maximum (a- <= a >= a+, one strict; a+ from the step), else the step S. Is M injective without a log?
from collections import defaultdict
def run(w,D,T):
    def S(am,a,r):
        u=2*w*a-w*am-D*a+r; return (a,u//w,u%w)
    M=defaultdict(list); R=range(-25,26)
    for am in R:
        for a in R:
            for r in range(w):
                _,ap,_=S(am,a,r)
                top=(am<=a) and (ap<=a) and (am<a or ap<a)
                M[T(am,a,r) if top else S(am,a,r)].append((am,a,r,top))
    coll=[(k,v) for k,v in M.items() if len(v)>1]
    return coll
mirror=lambda w:(lambda am,a,r:(a,am,(2*(w//2)-r)%w))
flip=lambda w:(lambda am,a,r:(a,am,w-1-r))
for w in (10,11):
    for name,Tm in (("mirror",mirror),("flip",flip)):
        c=run(w,3,Tm(w))
        print(f"w {w} {name}: images hit twice: {len(c)}", ("e.g. "+str(c[0])) if c else "")
