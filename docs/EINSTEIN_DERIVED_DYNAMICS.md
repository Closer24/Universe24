# Einstein-derived dynamics, integer geometry, and the remaining general-GR gap

**Historical sector experiment.** A subsequent [full ADM + scalar implementation](INTEGER_ADM.md)
compiles nonlinear spatial evolution and all four constraint readouts into
Rule3 using staged rational arithmetic. It allows discretization error and a
finite precompiled horizon; it does not make the exact continuum claim.
This earlier experiment derives and implements one
closed homogeneous radiation sector, reconstructs general local metrics from
signed edge data, and adds a general nonlinear Einstein observer. The observer
is not an evolution law. No default ONE code or common Engine code changes.

## What is implemented

| Requirement | Implementation | Remaining limitation |
| --- | --- | --- |
| Derive the update from Einstein | Vary the Einstein–Hilbert radiation action, including the lapse; compile its homogeneous evolution into Rule3 | Flat homogeneous isotropic spatial slices, radiation, zero cosmological constant |
| Evolve geometry as retained integer state | A scale gear evolves; its square determines the metric; its value determines spatial link lengths | One geometric degree of freedom repeated over the board; arbitrary spatial geometry is not evolved |
| Let matter constrain geometry | An independent comoving-energy gear and the Einstein lapse constraint determine the allowed initial expansion/contraction speed | Perfect-fluid equation of state is assumed; no microscopic radiation model or universal matter coupling |
| Reconstruct lengths and angles | All ten signed squared edges of a nondegenerate four-simplex determine a metric by polarization | Local tangent geometry; finite curved cells are not exactly flat |
| Check the complete nonlinear Einstein tensor | General exact-rational metric jets, including off-diagonal components and spatial derivatives, produce all curvature components and all 16 entries of G | The required metric derivatives must be supplied; computing G does not evolve g |
| Integer runtime and exact reverse | Three gears, five monomials, rank two, the unchanged Engine, full (a,b,r) history | Exact reversal is not an Einstein constraint test |

The cubic board remains a computational mesh. General relativity does not
require dynamically changing its connectivity: physical distances and angles
can change on a fixed mesh. The broader implementation is documented separately
in [INTEGER_ADM.md](INTEGER_ADM.md).

## Derive before discretizing

Use c=kappa=1, where kappa=8*pi*G/c^4, and k=Lambda=0. Write

    ds^2 = a(eta)^2 [-n(eta)^2 d eta^2 + dx^2 + dy^2 + dz^2].

Matter is a comoving perfect radiation fluid, p=rho/3, with conserved
E=rho*a^4. After eliminating the fluid variables at fixed comoving energy,
the matter Routhian per unit comoving coordinate volume is -n*E. This is a
specified fluid model, not a derivation of photons from integer gears.

The symbolic audit computes the connection, all 256 mixed Riemann components,
Ricci and scalar curvature directly from the metric, retaining n. It verifies

    sqrt(-g)*R/2 = -3*a'^2/n + d/deta (3*a*a'/n).

With the boundary derivative removed, the reduced action has density

    L = -3*a'^2/n - n*E.

Varying n and a BEFORE fixing the lapse gives

    3*(a'/n)^2 = E,             (a'/n)' = 0.

Then n=1 gives a''=0 and 3*a'^2=E. Keeping only a''=0 would be wrong: any
affine trajectory would pass, even with incompatible matter energy. The
negative control exhibits exactly this failure.

Independently form T=(rho+p)u_cov*u_cov^T+p*g, with u=(1/(a*n),0,0,0).
In conformal gauge the independently differentiated Einstein tensor is

    G_00 = 3*a'^2/a^2,
    G_ii = (a'^2 - 2*a*a'')/a^2,
    T_00 = E/a^2,
    T_ii = E/(3*a^2).

All 16 entries of G-T vanish under both derived equations. All four stress
conservation equations also vanish. Radiation has scalar R=0 but, for a'!=0,
nonzero Kretschmann invariant 24*a'^4/a^8: this spacetime is curved.

## Discrete action and exact integer compilation

At conformal step h and edge lapse n_j, use the reduced discrete action

    S_d = sum_j [-3*(a_{j+1}-a_j)^2/(h*n_j) - h*n_j*E].

Independent variations of the interior a_j and the n_j, followed by n_j=1,
give

    a_{j+1}-2*a_j+a_{j-1}=0,
    3*((a_{j+1}-a_j)/h)^2=E.

The audit differentiates this action explicitly. In this affine sector the
discrete and continuum equations agree exactly, not just to truncation order.
That special property is not asserted for a general Regge discretization.

Let n be a refinement factor, h=1/n, S=64*n. Retain integer gears A, E_int, C:

    a = A/S,     E = E_int/S^2,     tau = C/(2*S*n).

With the repository's common D=6Q, construct fixed inputs

    u_A = D*b_A,
    u_E = D*b_E,
    u_C = D*b_C + D*(b_A-a_A).

For every remainder 0<=r<D, Rule3 therefore gives exactly

    A_next = 2*A-A_previous,
    E_next = 2*E-E_previous,
    C_next = 2*C-C_previous+2*(A-A_previous),
    r_next = r.

Prepare A_0=2S, A_previous=A_0-B, E_previous=E_0=3*n^2*B^2,
C_0=0, C_previous=-2*A_0+B. The independent source can also be supplied
explicitly; inconsistent initial pairs are rejected at preparation, never
repaired during a run. The invariant solution is

    A_j=A_0+B*j,     E_j=E_0,     C_j=2*A_0*j+B*j^2.

Hence a=2+v*eta, tau=2*eta+v*eta^2/2, v=n*B/S, and

    a(tau)^2 = 4+2*v*tau,       rho*a^4=E.

The apparent zero conformal acceleration does not mean zero gravitational
effect: proper-time expansion follows the radiation Friedmann law, with
d^2a/dtau^2=-v^2/a^3. The geometry equation does not contain a runtime source
force in this gauge and sector; matter enters through the initial constraint.
This is not a general backreaction mechanism.

The clock counter is a passive comoving proper-time integral, with a documented
one-way designation. It has no stress or feedback. Its old-a dependency is
acyclic. Every term is on-site and degree one. No callback, projection, runtime
injection, floating-point update, or alternative time-stepper is used.
Observers reject a<=0, where this physical chart is singular; the bare Engine
itself has no such veto. Nonuniform initial data are outside the FLRW claim.

## What lengths and angles actually determine

For simplex vertices 0,...,4, let s_ij be signed squared intervals. In the basis
of the four edges leaving vertex 0,

    g_ab = (s_0a+s_0b-s_ab)/2.

The implementation requires all ten entries, exact rational arithmetic, and
signature (-,+,+,+). It also handles a null basis using exact 2x2 congruence
pivots. Off-diagonal terms recover angles and time-space mixing. Tests show
two distinct metrics with the same axis lengths but different diagonals:
axis links alone do not determine a general metric.

In the evolving sector, signed tangent intervals are calculated from the
retained A and a fixed coordinate basis; reconstruction recovers the metric
exactly. They are derived observables, not ten independent evolved edge gears.
Integer numerators with declared common scales represent these rational data.
The comoving timelike edge is also a geodesic, and its proper length follows
exactly from the retained clock increment. A separate finite-cell control
integrates coordinate-straight paths; these are generally NOT geodesics. Its
reconstructed constant metric approaches the base-point metric under
refinement but differs at every finite tested resolution.

## General nonlinear observer and explicit barriers

`full_gr_audit.py` computes g inverse, its derivatives, the connection,
all Riemann components, Ricci, R and G from a general rational metric jet.
The linear Gram reconstruction also acts on edge derivatives, so the same
calculation accepts ten signed edge values and their first/second derivatives.
One snapshot of lengths alone does not determine curvature or Einstein dynamics.

Independent validations include curved Schwarzschild vacuum (all G entries
zero, 24 nonzero Riemann components), a shifted radiation chart with nonzero
G_01=1/256, and a spatially varying off-diagonal polynomial metric compared
against independent analytic differentiation. These are observer tests, not
Schwarzschild evolution on the board.

The audit records three obstacles to a DIRECT replacement of the current
tensor entries with general Einstein equations:

1. A generic inverse-metric component 1/(1+x) has a nonzero fourth derivative,
   so it is not a cubic polynomial in the existing x field.
2. A direct cross-axis stress product reading both +x and +y is rejected by
   the existing one-face support validator.
3. Ordinary central differences do not obey the continuum product rule. For
   integer samples (1,2,4), D(f^2)-2*f*D(f)=3/2. Consequently replacing all
   derivatives in continuum identities by that difference is not an exact
   discrete Bianchi/conservation proof.

These are narrowly stated barriers, not a theorem excluding every integer
encoding of gravity. Auxiliary fields, first-order variables, microsteps,
constraint-preserving discretizations and consistent discrete actions can
change the problem. They must be designed and validated; adding more gears or
calling an arbitrary recurrent rule “Einstein” does not do that automatically.
The existing `layers/einstein.py` and `observe/einstein.py` already document
related limitations of the linearized ten-component layer.

## How others obtain geometry-driven evolution

These primary sources inform the research direction; this code does not claim
to implement their unrestricted algorithms:

- [Regge, General relativity without coordinates (1961)](https://doi.org/10.1007/BF02733251): replace smooth geometry with piecewise-flat simplices and curvature at hinges.
- [Borissova and Dittrich (2023), especially the Lorentzian-geometry appendix](https://arxiv.org/abs/2303.07367): signed squared edge lengths, causal types, volumes, angles and Lorentzian Regge action.
- [Barrett et al., A Parallelizable Implicit Evolution Scheme for Regge Calculus](https://arxiv.org/abs/gr-qc/9411008): advance vertices by solving local implicit equations for new edge lengths. This is not the same operation as evaluating a fixed cubic Rule3 polynomial.
- [Jercher and Steinhaus (2024)](https://arxiv.org/abs/2312.11639): Lorentzian cosmological frusta with a massless scalar source, causal restrictions, expanding/contracting edge lengths, and a relational Friedmann continuum limit in a small-deficit expansion. Their matter model is not the radiation fluid used here.
- [Tong, General Relativity, sections 4.6.1–4.6.2](https://www.damtp.cam.ac.uk/user/tong/gr/grhtml/S4.html): full Einstein derivation of FLRW equations, radiation continuity and proper-time square-root expansion.

A general construction should start from a chosen covariant or constrained
discrete action, derive its geometry AND matter equations, and show how the
integer Rule3 state enforces or approximates those equations. It must specify
gauge, constraints, boundary conditions and the continuum limit. Full local
metric evolution and scalar feedback are now implemented in the staged ADM
experiment; its constraint errors are measured. Regge is a researched
route to that goal, not a completed component of this patch.

## Reproduction and measured results

Requires the repository's optional validation dependency SymPy; plotting is
not required by the experiment.

```bash
python experiments/geometry/einstein_friedmann.py --out runs/geometry/friedmann
python -m unittest universe24.tests.test_einstein_friedmann -v
python -m unittest universe24.tests.test_one universe24.tests.test_migration -v
```

The run records all retained triples for 16 histories: four time refinements
and flat, expanding, faster-expanding and contracting preparations on L=6.
The tangent probe basis is also scaled by 1/n. With fixed L, this is not a
spatial-grid convergence study on a fixed physical domain.
There are 107,136 node-snapshots; spatially identical geometric data are
checked over the whole board, while remainders may differ. All 16 G-T entries
vanish exactly in the declared homogeneous decoder. Every single-step inverse
and complete rewind succeeds. The strongest integer fallback test exceeds
int64 without changing the recurrence.

At eta=8 the base expanding run has a=3, tau=20, rho=1/1728. Fourfold initial
energy requires twice the conformal velocity and gives a=4. The contracting
branch gives a=1, tau=12. An independent source mismatch gives Einstein
residual 1/16384, and an added integer forcing term gives 1/32; both erroneous
models still reverse exactly. Generated reports, exact arrays, sources'
SHA256 hashes and test logs live under `runs/geometry/friedmann/`.

Validation: 16 new physics/geometry tests and 34 existing quick/wave/tensor-board
regression tests pass (50 total). No structural Engine change is involved.
