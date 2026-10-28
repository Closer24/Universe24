import itertools, numpy as np
from fractions import Fraction
# O: signed permutation matrices det 1
mats=[]
for perm in itertools.permutations(range(3)):
    for signs in itertools.product([1,-1],repeat=3):
        M=np.zeros((3,3),dtype=int)
        for i,(p,s) in enumerate(zip(perm,signs)): M[i,p]=s
        if round(np.linalg.det(M))==1: mats.append(M)
print("order",len(mats))
key=lambda M: tuple(M.flatten())
def inv(M): return M.T
classes=[];seen=set()
for M in mats:
    if key(M) in seen: continue
    cl={key(g@M@inv(g)) for g in mats}; seen|=cl; classes.append((M,len(cl)))
print("class sizes",[c for _,c in classes])
def order(M):
    P=np.eye(3,dtype=int);k=0
    while True:
        P=P@M;k+=1
        if (P==np.eye(3)).all(): return k
print("orders",[order(M) for M,_ in classes], "traces",[int(np.trace(M)) for M,_ in classes])
# characters of V, Sym2, Lam2, xyz
chiV=[int(np.trace(M)) for M,_ in classes]
chiV2=[int(np.trace(M@M)) for M,_ in classes]
sym2=[(int(a)*int(a)+int(b))//2 for a,b in zip(chiV,chiV2)]
lam2=[(int(a)*int(a)-int(b))//2 for a,b in zip(chiV,chiV2)]
def xyz(M):
    # image of monomial xyz under M: product of the rows' signs (each row has one entry)
    return int(np.prod([M[i].sum() for i in range(3)]))
chiA2=[xyz(M) for M,_ in classes]
sizes=[c for _,c in classes]
# irreps characters of O in class order found; build standard table by identifying classes
def ident(M):
    o=order(M); t=int(np.trace(M))
    return {(1,3):'E',(4,1):'6C4',(2,-1):'3C2' if True else '',(3,0):'8C3'}.get((o,t),'?')
lab=[]
for M,c in classes:
    o=order(M);t=int(np.trace(M))
    if o==1: lab.append('E')
    elif o==4: lab.append('6C4')
    elif o==3: lab.append('8C3')
    elif o==2 and c==3: lab.append('3C2')
    else: lab.append("6C2'")
tab={'A1':{'E':1,'8C3':1,'3C2':1,'6C4':1,"6C2'":1},'A2':{'E':1,'8C3':1,'3C2':1,'6C4':-1,"6C2'":-1},
     'E':{'E':2,'8C3':-1,'3C2':2,'6C4':0,"6C2'":0},'T1':{'E':3,'8C3':0,'3C2':-1,'6C4':1,"6C2'":-1},
     'T2':{'E':3,'8C3':0,'3C2':-1,'6C4':-1,"6C2'":1}}
def decomp(chi):
    return {k:Fraction(sum(s*x*v[l] for s,x,l in zip(sizes,chi,lab)),24) for k,v in tab.items() if sum(s*x*v[l] for s,x,l in zip(sizes,chi,lab))}
print("labels",lab)
print("V",decomp(chiV));print("Sym2",decomp(sym2));print("Lam2",decomp(lam2));print("xyz",decomp(chiA2))
# orthogonality check of table
print("table orthonormal",all(sum(s*tab[a][l]*tab[b][l] for s,l in zip(sizes,lab))==(24 if a==b else 0) for a in tab for b in tab))
# S4 isomorphism: action on 4 body diagonals (up to sign)
diags=[np.array(v) for v in [(1,1,1),(1,1,-1),(1,-1,1),(-1,1,1)]]
def perm_of(M):
    out=[]
    for d in diags:
        e=M@d
        out.append([i for i,dd in enumerate(diags) if (dd==e).all() or (dd==-e).all()][0])
    return tuple(out)
ps={perm_of(M) for M in mats}
print("distinct perms of diagonals",len(ps))
