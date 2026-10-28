import itertools, random
from fractions import Fraction
from collections import Counter
def pick(c, sizes, room):
    t=(c*sum(sizes))//room; acc=0
    for k,s in enumerate(sizes):
        if acc<=t<acc+s: return k
        acc+=s
    return None
# 1) the multipart rule with c uniform on [0,room): exact iff sum | room; within 1/room otherwise
worst=0
for room in range(1,60):
    for sizes in itertools.product(range(0,6),repeat=3):
        S=sum(sizes)
        if S==0: continue
        cnt=Counter(pick(c,sizes,room) for c in range(room))
        for k,s in enumerate(sizes):
            err=abs(Fraction(cnt.get(k,0),room)-Fraction(s,S))
            if S and room%S==0: assert err==0
            worst=max(worst,err*room)
print("uniform c: max error in counts of room:",float(worst),"(<1 means within one count)")
print("all sizes 0 -> pick:",pick(0,[0,0],10))
# 2) the vernier: digits d_k uniform in [0,b_k), SORTED by value, Horner-composed mod M, room=min(prod b, M)
def vernier(digits,M):
    carry,room=0,1
    for d,b in sorted(digits):
        carry=(carry*b+d)%M; room=min(room*b,M)
    return carry,room
def dist(bases,M,sort=True):
    cnt=Counter();room=None
    for ds in itertools.product(*[range(b) for b in bases]):
        pairs=list(zip(ds,bases))
        if sort: c,room=vernier(pairs,M)
        else:
            carry,room=0,1
            for d,b in pairs: carry=(carry*b+d)%M; room=min(room*b,M)
            c=carry
        cnt[c]+=1
    return cnt,room
for bases,M in [((5,7,9),100),((10,10,10),1000),((6,6,6,6),1296),((8,8,8),64)]:
    for sort in (False,True):
        cnt,room=dist(bases,M,sort)
        tot=sum(cnt.values())
        up=sum(v for c,v in cnt.items() if pick(c,[1,1],room)==0)
        print(f"bases {bases} M {M} sorted={sort}: room {room}, distinct c {len(cnt)} of {room}, P(up | sizes 1,1)={up/tot:.4f} (Born 0.5), max/min count {max(cnt.values())}/{min(cnt.values()) if len(cnt)==room else 0}")
