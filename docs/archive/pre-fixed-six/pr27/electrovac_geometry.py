"""Independent continuum Einstein-Maxwell audit; never updates Rule3 state."""
from functools import lru_cache


@lru_cache(maxsize=1)
def audit():
    import sympy as s
    u, v, x, y = coords = s.symbols('u v x y', real=True)
    e, f, C = [s.Function(n)(u) for n in ('E1', 'E2', 'C')]
    H = C*(x*x+y*y)
    g = s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
    inv = g.inv()
    gamma = [[[s.simplify(sum(inv[a,k]*(s.diff(g[k,c],coords[b])+
        s.diff(g[k,b],coords[c])-s.diff(g[b,c],coords[k])) for k in range(4))/2)
        for c in range(4)] for b in range(4)] for a in range(4)]
    ricci = s.Matrix(4,4,lambda b,d: s.simplify(sum(
        s.diff(gamma[a][b][d],coords[a])-s.diff(gamma[a][b][a],coords[d])+
        sum(gamma[a][a][k]*gamma[k][b][d]-gamma[a][d][k]*gamma[k][b][a]
            for k in range(4)) for a in range(4))))
    scalar = s.simplify(sum(inv[a,b]*ricci[a,b] for a in range(4) for b in range(4)))
    G = s.simplify(ricci-g*scalar/2)
    F = s.Matrix([[0,0,e,f],[0,0,0,0],[-e,0,0,0],[-f,0,0,0]])
    Fup = inv*F*inv
    invariant = s.simplify(sum(F[a,b]*Fup[a,b] for a in range(4) for b in range(4)))
    T = s.simplify(F*inv*F.T-g*invariant/4)
    rho = e*e+f*f
    assert g.det()==-1 and scalar==0 and invariant==0
    assert T==s.diag(rho,0,0,0) and G==s.diag(-2*C,0,0,0)
    assert all(s.simplify(sum(s.diff(Fup[a,b],coords[a]) for a in range(4)))==0
               for b in range(4))  # sqrt(-det g)=1
    assert all(s.simplify(s.diff(F[a,b],coords[c])+s.diff(F[b,c],coords[a])+
                          s.diff(F[c,a],coords[b]))==0
               for a in range(4) for b in range(4) for c in range(4))
    Tup = inv*T*inv
    for b in range(4):
        div = sum(s.diff(Tup[a,b],coords[a])+sum(gamma[a][a][k]*Tup[k,b]+
              gamma[b][a][k]*Tup[a,k] for k in range(4)) for a in range(4))
        assert s.simplify(div)==0
    # Units kappa=8*pi*G/c^4=1. T was obtained from F, not defined from G.
    assert s.simplify((G-T).subs(C,-rho/2))==s.zeros(4)
    assert s.simplify((G-T).subs(C,0))==s.diag(-rho,0,0,0)
    # Full charged worldline including longitudinal v and normalization.
    vx, vy, charge = s.symbols('vx vy charge', real=True)
    ax, ay = C*x-charge*e, C*y-charge*f
    vp = (1+vx*vx+vy*vy+H)/2
    vpp = s.diff(vp,u)+s.diff(vp,x)*vx+s.diff(vp,y)*vy+s.diff(vp,vx)*ax+s.diff(vp,vy)*ay
    velocity = s.Matrix([1,vp,vx,vy])
    lorentz = charge*inv*F*velocity
    for a,acc in enumerate((0,vpp,ax,ay)):
        residual = acc+sum(gamma[a][b][c]*velocity[b]*velocity[c]
                            for b in range(4) for c in range(4))-lorentz[a]
        assert s.simplify(residual)==0
    assert s.simplify((velocity.T*g*velocity)[0])==-1
    return dict(convention='(-,+,+,+), coordinates (u,v,x,y), kappa=1, Lambda=0',
        metric='ds^2=-2du dv+dx^2+dy^2-(E1(u)^2+E2(u)^2)(x^2+y^2)du^2/2',
        independently_computed_Tuu='E1(u)^2+E2(u)^2',
        independently_computed_Guu='-2*C(u)', C='-(E1(u)^2+E2(u)^2)/2',
        all_16_Einstein_Maxwell_residuals_zero=True,
        all_Maxwell_divergences_zero=True, all_exterior_derivatives_zero=True,
        all_stress_divergences_zero=True, null_energy_condition='T(k,k)=rho*(k^u)^2 >= 0',
        flat_metric_with_nonzero_field_rejected=True,
        flat_metric_residual_Guu_minus_Tuu='-(E1(u)^2+E2(u)^2)',
        charged_and_neutral_worldline_equations_verified=True,
        transverse_equation="x''=-rho*x/2-charge*E1; y''=-rho*y/2-charge*E2",
        source_is_not_defined_from_Einstein_tensor=True,
        limitation='Exact aligned plane-wave continuum sector; no general matter backreaction or metric reconstruction from clocks.')
