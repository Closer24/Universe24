import random
random.seed(1)
N=lambda z: z.real*z.real+z.imag*z.imag
def g(): return complex(random.randint(-10**6,10**6),random.randint(-10**6,10**6))
def S(p):
    p1,p2=p; c=p1.conjugate()*p2
    return (2*c.real,2*c.imag,N(p1)-N(p2))
bad=[0,0,0]
for _ in range(20000):
    psi=(g(),g()); phi=(g(),g())
    rho=N(psi[0])+N(psi[1]); rhod=N(phi[0])+N(phi[1])
    ov=phi[0].conjugate()*psi[0]+phi[1].conjugate()*psi[1]
    perp=(-phi[1].conjugate(),phi[0].conjugate())
    ovp=perp[0].conjugate()*psi[0]+perp[1].conjugate()*psi[1]
    s=S(psi);m=S(phi)
    # use Python ints to avoid float rounding: recompute with ints
    a,b=int(psi[0].real),int(psi[0].imag);c,d=int(psi[1].real),int(psi[1].imag)
    e,f=int(phi[0].real),int(phi[0].imag);gg,h=int(phi[1].real),int(phi[1].imag)
    # <phi,psi> = conj(phi1) psi1 + conj(phi2) psi2
    re=e*a+f*b+gg*c+h*d; im=e*b-f*a+gg*d-h*c
    rhoI=a*a+b*b+c*c+d*d; rhodI=e*e+f*f+gg*gg+h*h
    # S(psi)= (2Re(conj(p1)p2), 2Im(conj(p1)p2), N1-N2); conj(p1)p2=(a-ib)(c+id)=(ac+bd)+i(ad-bc)
    Sx,Sy,Sz=2*(a*c+b*d),2*(a*d-b*c),a*a+b*b-c*c-d*d
    mx,my,mz=2*(e*gg+f*h),2*(e*h-f*gg),e*e+f*f-gg*gg-h*h
    # perp overlap = -phi2 psi1 + phi1 psi2
    pre=-(gg*a-h*b)+(e*c-f*d); pim=-(gg*b+h*a)+(e*d+f*c)
    if rhoI*rhodI+Sx*mx+Sy*my+Sz*mz!=2*(re*re+im*im): bad[0]+=1
    if (re*re+im*im)+(pre*pre+pim*pim)!=rhoI*rhodI: bad[1]+=1
    if Sx*Sx+Sy*Sy+Sz*Sz!=rhoI*rhoI: bad[2]+=1
print("failures Fierz, Lagrange, S.S=rho^2:",bad)
