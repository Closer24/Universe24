import itertools, numpy as np
# binary tetrahedral group 2T (Hurwitz units) in the standard SU(2) matrices; search an integral Z[i]-basis
Q=[]
for i in range(4):
    for s in (1,-1):
        v=[0]*4; v[i]=s; Q.append(v)
for s in itertools.product((1,-1),repeat=4): Q.append([x/2 for x in s])
def mat(q):
    a,b,c,d=q
    return np.array([[a+1j*b, c+1j*d],[-c+1j*d, a-1j*b]])
G=[mat(q) for q in Q]
def gauss(M): return np.allclose(M.real,np.round(M.real)) and np.allclose(M.imag,np.round(M.imag))
vals=[ (a+1j*b)/2 for a in range(-2,3) for b in range(-2,3)]
found=None
for x in vals:
    for y in vals:
        if abs(y)<1e-9: continue
        B=np.array([[1,x],[0,y]]); Bi=np.linalg.inv(B)
        if all(gauss(Bi@g@B) for g in G): found=(x,y);break
    if found: break
print("2T integral basis B=[[1,x],[0,y]] found:",found)
if found:
    x,y=found;B=np.array([[1,x],[0,y]]);H=B.conj().T@B
    print("invariant Hermitian form in that basis (times 2):",np.round(2*H,6))
