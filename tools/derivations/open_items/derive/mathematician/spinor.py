import itertools, numpy as np
r2=np.sqrt(2)
# binary octahedral group as unit quaternions
Q=[]
for i in range(4):
    for s in (1,-1):
        v=[0]*4; v[i]=s; Q.append(v)
for s in itertools.product((1,-1),repeat=4): Q.append([x/2 for x in s])
for i,j in itertools.combinations(range(4),2):
    for s1 in (1,-1):
        for s2 in (1,-1):
            v=[0]*4; v[i]=s1/r2; v[j]=s2/r2; Q.append(v)
print("|2O| =",len(Q))
def mat(q):
    a,b,c,d=q
    return np.array([[a+1j*b, c+1j*d],[-c+1j*d, a-1j*b]])
def rot(q):
    # SO(3) image
    U=mat(q); sig=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.array([[1,0],[0,-1]])]
    return np.real(np.array([[0.5*np.trace(sig[i]@U@sig[j]@U.conj().T) for j in range(3)] for i in range(3)])).round(6)
def is_gauss(M): return np.allclose(M.real,np.round(M.real)) and np.allclose(M.imag,np.round(M.imag))
def kmin(U):
    for k in range(5):
        if is_gauss(U*r2**k): return k
from collections import defaultdict
bycls=defaultdict(set)
for q in Q:
    U=mat(q); R=rot(q)
    tr=np.trace(R); ang=np.degrees(np.arccos(np.clip((tr-1)/2,-1,1)))
    # axis type
    if abs(ang)<1e-6: typ='identity'
    else:
        w,v=np.linalg.eig(R); ax=np.real(v[:,np.argmin(abs(w-1))]); ax=np.round(abs(ax)/max(abs(ax)),3)
        nz=int((ax>1e-3).sum()); typ={1:'face',2:'edge',3:'body'}[nz]+f' {ang:.0f}deg'
    bycls[typ].add((kmin(U), round(np.trace(U).real,4)))
for k,v in sorted(bycls.items()): print(f"{k:16s} scale exponent k and SU(2) trace: {sorted(v)}")
