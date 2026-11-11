# An exact sourced Einstein-Maxwell decoder and integer test particles

This optional experiment extends the vacuum result in
[PP_WAVE_SOLUTION.md](PP_WAVE_SOLUTION.md) to a nonzero, independently computed
electromagnetic stress tensor. The source is a plane radiation field; no massive
matter distribution or general reciprocal matter-gravity solver is claimed.
The default ONE tensor and common Engine are unchanged.

The [tensor-board observer](TENSOR_BOARD.md) reads these stored histories and
exposes the full metric, Riemann, Ricci, Einstein, Maxwell stress and Weyl tensors.

## Reproduction

```sh
python -m pip install '.[validation]'
python experiments/geometry/electrovac_solution.py --out runs/geometry/electrovac
python -m unittest universe24.tests.test_electrovac_solution universe24.tests.test_pp_wave_solution universe24.tests.test_one universe24.tests.test_migration -v
```

The main sweep contains flat, linearly polarized and circularly polarized
electromagnetic seeds at n=1,2,4,8. Two additional n=2 histories reverse the
field sign and double its amplitude. Each history includes a complete integer
state trace, the initial profile, official quotients and an independent
continuum reference. `--refinements 1 2` gives a smaller sweep. All generated
data go under `runs/`; NPZ files require no pickle.

## The independently sourced continuum equations

Fix signature (-,+,+,+), coordinates (u,v,x,y), Lambda=0 and units
`kappa=8*pi*G/c^4=1`. Define a Maxwell two-form independently of the metric:

\[
F=E_1(u)\,du\wedge dx+E_2(u)\,du\wedge dy,
\qquad \rho=E_1^2+E_2^2.
\]

Use the Brinkmann metric

\[
ds^2=-2du\,dv+dx^2+dy^2+C(u)(x^2+y^2)du^2,
\qquad C=-\rho/2.
\]

The program computes the stress tensor directly from the Maxwell field:

\[
T_{\mu\nu}=F_{\mu\alpha}g^{\alpha\beta}F_{\nu\beta}
-\tfrac14g_{\mu\nu}F_{\alpha\beta}F^{\alpha\beta}.
\]

It independently differentiates the metric to obtain Christoffel symbols,
Ricci and the Einstein tensor. The results are

\[
T_{uu}=\rho,\qquad G_{uu}=-2C=\rho,
\qquad G_{\mu\nu}-T_{\mu\nu}=0
\]

for all 16 components. Thus T is **not defined by setting it equal to G**.
All exterior Maxwell equations, all four source-free Maxwell divergences and
all four stress divergences vanish symbolically. The stress is null radiation
with `T(k,k)=rho*(k^u)^2 >= 0`. A deliberately flat metric with the same nonzero
F has residual `G_uu-T_uu=-rho` and is rejected.

This construction belongs to the established Einstein-Maxwell plane-wave
family; see [J. W. van Holten, The Gravity of Light-Waves (2018)](https://doi.org/10.3390/universe4100110).
The normalization of v and curvature conventions are fixed here and checked
directly, rather than copied between incompatible conventions.

In this special aligned sector the Maxwell equation is independent of C.
Consequently the field can propagate unchanged while its stress determines
nonzero geometry. This is a consistent coupled continuum solution; it does
not demonstrate generic two-way scattering or autonomous metric evolution.

## Exact integer source transport and a local conservation law

The four source gears reuse `retimed_tensor_wave.build(Q, axis=2)` unchanged.
Let R(X,Y)=(Y,SX), where S shifts one site along z. Prepared data have
`a=R^-1 b`, so the ordinary Rule3 update gives `b'=R b` and constant source
remainders exactly. There is no source injection during evolution.

At refinement n choose

\[
L=3n,\quad P=128n^2,\quad Q=2P^2n^2,\quad D=6Q,
\quad du=1/n,\quad s=2^{13}n^4.
\]

The two integer profiles f,h have 2L samples. Set p.X=f(2z), p.Y=f(2z+1)
and similarly for q and h. Decode `E1=p.X/P`, `E2=q.X/P` at
`u=(2z+tick)/n`. A real trigonometric interpolant of the complete initial
profiles specifies the smooth continuum decoder. Density is the **square of
the interpolated fields**, not an independent interpolation of squared samples.
Floating point selects seed integers and evaluates passive references only.

The circular preparation rounds `(P*cos(2*pi*u/6)/8, P*sin(2*pi*u/6)/8)`
once. Linear polarization sets its second component to zero. Flat sets both
to zero. Exported seed integers are authoritative. A constant-field control
uses `(P/8,0)` exactly and admits a closed-form trajectory.

Define integer source-bank densities `rhoX=p.X^2+q.X^2` and
`rhoY=p.Y^2+q.Y^2`. Exact transport proves the pointwise identity

\[
(\rho_X+\rho_Y)'-(\rho_X+\rho_Y)=S\rho_X-\rho_X.
\]

The right side telescopes on the periodic carrier ring. The implementation
checks this local ledger at every site and step and conserves the total
integer carrier energy exactly. This is a transport invariant, not a claim
of finite total gravitational energy for an infinite plane wave. The physical
transverse chart is a local patch, not a periodic physical torus.

## Neutral and charged particles use the same geometry

There are two neutral basis probes starting at (1,0), (0,1), and one charged
probe at (1,0), all with initial radial velocity 1/16. Charge-to-mass ratio is
0 for the first two and 1 for the third. Positions are stored as integers X,Y
with physical decoder x=X/s,y=Y/s. They obey fixed inputs

\[
u_X=DX-3(p.X^2+q.X^2)X-6qPs\,p.X,
\quad
u_Y=DY-3(p.X^2+q.X^2)Y-6qPs\,q.X.
\]

The complete tensor has 10 gears and 28 monomials, with input degree three
(tensor order four). Every nonlinear term is on-site. The carrier terms use
only one face neighbor. Fourteen couplings to test particles are explicitly
designated one-way; their stress and electric current are neglected.

Rule3 implies the **exact**, remainder-inclusive identity

\[
D(X_{t+1}-2X_t+X_{t-1})
=-6(p.X_t^2+q.X_t^2)X_t-12qPs\,p.X_t+r_t-r_{t+1}.
\]

After division by `D*s*du^2` this is a central-difference approximation to

\[
x''=-\rho x/2-qE_1,\qquad y''=-\rho y/2-qE_2.
\]

The retained remainder acceleration is bounded by `n^2/s=1/(8192*n^2)`.
The integer ledger is checked with Python integers to avoid diagnostic
overflow. The common Engine chooses its validated int64 or Python-int path;
no alternate floating point evolution is inserted.

An independent RK4 reference integrates these equations with 64 and 128
substeps per Rule3 update, and reconstructs

\[
v'=\tfrac12(1+x'^2+y'^2+H).
\]

The symbolic audit verifies all four Lorentz-force equations and timelike
normalization. u is affine proper time in this chosen family; v is a passive
reference coordinate, not a runtime gear. For a constant E1=1/8, E2=0,
`omega=1/sqrt(128)` and the exact x trajectories are

\[
x_0=\cos(\omega u)+\sin(\omega u)/(16\omega),\qquad
x_q=x_0-16q[1-\cos(\omega u)].
\]

These analytic trajectories separately validate the reference solver and
the normalization of the force. Integer detector positions are reconstructed
from official quotients and the declared starting pair, with an independent
check that no nonzero raw quotient was omitted. All complete states rewind.

## Controls distinguish gravity, electromagnetism and reciprocity

- Reversing both electromagnetic fields leaves rho, geometry and the entire
  neutral trajectory unchanged, while reversing the direct Lorentz force.
- Doubling the integer field amplitudes quadruples Tuu exactly, with stronger
  neutral focusing. This uses the same tensor and changes only the seed.
- Removing the field restores exact flat affine motion.
- Perturbing the source preparation breaks exact travelling transport even
  though inverse evolution still works.
- A fully reciprocal completion adds every missing derivative of the
  interaction potential below. It passes the algebraic reciprocity checker
  and exact inverse check but fails this prepared transport/continuity sector.

The naive reciprocal potential is

\[
\Phi_{int}=-\tfrac32(p.X^2+q.X^2)\sum_j(X_j^2+Y_j^2)
-6Ps\sum_j q_j(p.X X_j+q.X Y_j).
\]

Its extra source inputs are cubic and local. The negative test gives one
neutral gear unit amplitude and no charged probe. Even this small initial
change destroys the source shift and energy ledger. Algebraic reciprocity
therefore cannot simply be attached to the successful decoder and called
general relativity. This control does not rule out other constrained
reciprocal constructions.

## Scope of the advance

The 14 full histories passed exact transport, local source continuity,
force ledgers, official decoding and complete rewind. Thirty scoped and
quick regression tests passed, including the earlier vacuum experiment.
At the finest declared step du=1/8, maximum componentwise position errors
in initial unit-length coordinates were:

| Source preparation | Neutral probe | Charged probe |
| --- | --- | --- |
| Linear polarization | 0.00000940570 | 0.000323778 |
| Circular polarization | 0.00000496377 | 0.000964513 |
| Flat | 0 exactly | 0 exactly |

The last measured convergence orders range from 1.7569 to 2.0450; these are
finite-resolution observations, not an exact assertion of order two for
every preparation. The n=8 histories exercise both the Engine's int64 and
arbitrary-precision paths and rewind exactly through both. The direct
reciprocal control produces two source mismatches and local continuity
residual 15 on its first update, while passing the inverse check.

The new result is a nonzero source computed independently from F, full
continuum Einstein-Maxwell compatibility, an exact discrete source continuity
identity, and autonomous charged/neutral test-particle responses with measured
refinement. It is stronger than checking the vacuum identity G=0 alone.

It still uses a declared metric decoder and prepared aligned radiation.
Metric gears are not independently solved, the probes do not source gravity
or electromagnetism, longitudinal particle motion is not stored, and the
metric has not been inferred from clocks and signals. No universal coupling
to existing ONE species, massive-matter dynamics, arbitrary-data stability,
finite transverse beam, general Einstein constraints or physical global
periodic spacetime has been established. A general feedback construction must
supply conserved sources and preserve its geometric constraints together.
