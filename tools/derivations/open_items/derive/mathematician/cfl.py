import numpy as np
L=4
def sh(a,ax,s): return np.roll(a,-s,axis=ax)
SP=[(ax,s) for ax in range(3) for s in (1,-1)]
x,y,z=np.indices((L,L,L)); cb=np.array((-1)**(x+y+z),dtype=object)
def run(W,g,ticks,am,a,r):
    amp=[]
    for t in range(ticks):
        F=sum(g*(sh(a,ax,sg)-a) for ax,sg in SP)
        p=W*(a-am)+r-W//2; pp=p+F
        am,a,r=a,a+(pp+W//2)//W,(pp+W//2)%W
        amp.append(abs(int((a*cb).sum())))
    return amp
np.random.seed(5)
for W,g,lab in [(6*10**6,2*10**6,"lambda=1/3 (light at the full rate)"),(6*10**6,2*10**6+10**4,"lambda=1/3*(1.005) (tension <0 or load <0)")]:
    am=np.array(np.random.randint(-1000,1000,(L,L,L)),dtype=object); a=am.copy(); r=np.array(np.random.randint(0,W,(L,L,L)),dtype=object)
    amp=run(W,g,2000,am,a,r)
    print(lab,": checkerboard amplitude at ticks 10,100,1000,2000:",[amp[i] for i in (9,99,999,1999)])
# exact linear Jordan block
a0,a1=0,1
seq=[a0,a1]
for t in range(10): seq.append(-2*seq[-1]-seq[-2])
print("exact checkerboard recurrence a+ = -2a - a- at lambda=1/3:",seq)
