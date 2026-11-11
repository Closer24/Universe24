"""Passive full nonlinear Brinkmann geometry audit, independent of Rule3.

Signature (-,+,+,+), coordinates (u,v,x,y), R^a_bcd = d_c Gamma^a_db
- d_d Gamma^a_cb + Gamma^a_cs Gamma^s_db - Gamma^a_ds Gamma^s_cb.
SymPy is used only in validation, never in the forward engine.
"""
from fractions import Fraction


def audit():
    import sympy as s
    u, v, x, y = coords = s.symbols('u v x y', real=True)
    A, B, C = [s.Function(n)(u) for n in ('A', 'B', 'C')]
    H = A*(x*x-y*y)+2*B*x*y+C*(x*x+y*y)
    g = s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
    inv = g.inv()
    gamma = [[[s.simplify(sum(inv[a,k]*(s.diff(g[k,c],coords[b])+
                 s.diff(g[k,b],coords[c])-s.diff(g[b,c],coords[k]))
                 for k in range(4))/2) for c in range(4)] for b in range(4)] for a in range(4)]
    R = [[[[s.simplify(s.diff(gamma[a][d][b],coords[c])-s.diff(gamma[a][c][b],coords[d])+
          sum(gamma[a][c][k]*gamma[k][d][b]-gamma[a][d][k]*gamma[k][c][b] for k in range(4)))
          for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    ricci = s.Matrix(4,4,lambda b,d: s.simplify(sum(R[a][b][a][d] for a in range(4))))
    scalar = s.simplify(sum(inv[a,b]*ricci[a,b] for a in range(4) for b in range(4)))
    einstein = s.simplify(ricci-g*scalar/2)
    assert g.det()==-1 and scalar==0
    assert einstein==s.diag(-2*C,0,0,0)
    lower = lambda a,b,c,d: s.simplify(sum(g[a,k]*R[k][b][c][d] for k in range(4)))
    assert lower(0,2,0,2)==-A-C
    assert lower(0,3,0,3)==A-C
    assert lower(0,2,0,3)==-B
    up = inv*einstein*inv
    divergence = [s.simplify(sum(s.diff(up[m,n],coords[m])+
                  sum(gamma[m][m][k]*up[k,n]+gamma[n][m][k]*up[m,k] for k in range(4))
                  for m in range(4))) for n in range(4)]
    assert divergence==[0]*4
    # u is affine. The complete longitudinal geodesic follows from normalization:
    # v'=(1+x'^2+y'^2+H)/2, x''=H_x/2, y''=H_y/2.
    vx, vy = s.symbols('vx vy')
    ax, ay = s.diff(H,x)/2,s.diff(H,y)/2
    vprime=(1+vx*vx+vy*vy+H)/2
    vsecond=s.diff(vprime,u)+s.diff(vprime,x)*vx+s.diff(vprime,y)*vy+s.diff(vprime,vx)*ax+s.diff(vprime,vy)*ay
    tangent=[1,vprime,vx,vy]
    for index, acceleration in ((0,0),(2,ax),(3,ay)):
        assert s.simplify(acceleration+sum(gamma[index][i][j]*tangent[i]*tangent[j]
                         for i in range(4) for j in range(4)))==0
    assert s.simplify(vsecond+sum(gamma[1][i][j]*tangent[i]*tangent[j] for i in range(4) for j in range(4)))==0
    assert s.simplify((s.Matrix(tangent).T*g*s.Matrix(tangent))[0])==-1
    vacuum=einstein.subs(C,0)
    assert vacuum==s.zeros(4)
    return dict(metric='ds^2=-2 du dv+dx^2+dy^2+[A(u)(x^2-y^2)+2B(u)xy]du^2',
                method='All Christoffel, 256 mixed Riemann, 16 Ricci and 16 Einstein components computed from the metric',
                determinant=-1,lorentzian_signature='one negative, three positive; null block determinant -1',
                all_16_full_nonlinear_vacuum_Einstein_components_zero=True,
                tidal_components={'Ruxux':'-A','Ruyuy':'A','Ruxuy':'-B'},
                nonzero_curvature_allowed=True,contracted_Bianchi_all_four_zero=True,
                negative_trace_control={'added_H':'C(u)(x^2+y^2)','Guu':'-2*C(u)','C_1_over_100_Guu':'-1/50'},
                transverse_geodesic='x_second=A*x+B*y; y_second=B*x-A*y',
                longitudinal_geodesic_and_timelike_normalization_verified=True,
                scope='Exact continuum identity for arbitrary smooth A,B, Lambda=0 and vacuum; not a discrete Einstein evolution theorem')


def boundary_audit():
    """Exact interior stencil and a deliberately invalid torus gluing."""
    L=7; grid=list(range(-3,4)); A=Fraction(1,50); B=Fraction(1,75)
    h=[[A*(x*x-y*y)+2*B*x*y for y in grid] for x in grid]
    lap=lambda i,j: h[(i+1)%L][j]+h[(i-1)%L][j]+h[i][(j+1)%L]+h[i][(j-1)%L]-4*h[i][j]
    assert all(lap(i,j)==0 for i in range(1,L-1) for j in range(1,L-1))
    bad=[(i,j,lap(i,j)) for i in range(L) for j in range(L) if lap(i,j)!=0]
    assert bad
    return dict(interior_quadratic_Laplacian_exactly_zero=True,wrapped_torus_rejected=True,
                nonzero_seam_cells=len(bad),example={'index':list(bad[0][:2]),'Laplacian':str(bad[0][2])},
                domain='Local transverse patch only. The periodic carrier lattice is not a global physical transverse torus.')
