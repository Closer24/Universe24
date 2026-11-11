# Exact vacuum pp-wave decoding and an autonomous tidal detector

This optional experiment connects an existing prepared Rule3 travelling sector
to a full nonlinear continuum vacuum solution and tests an autonomous integer
detector against its geodesics. It is a new tensor/observation choice, not the
default ONE law or a derivation of general sourced Einstein dynamics.

## Reproduce the complete experiment

```sh
python -m pip install '.[validation]'
python experiments/geometry/pp_wave_solution.py --out runs/geometry/pp_wave
python -m unittest universe24.tests.test_pp_wave_solution -v
python -m unittest universe24.tests.test_one universe24.tests.test_migration -v
```

The full sweep has eight forward/inverse histories: flat and mixed-polarization
seeds at n=1,2,4,8. `--refinements 1 2` selects a smaller sweep. Results include
source fingerprints, tensor fingerprints, complete compressed `(a,b,r)` traces,
initial integer profiles, official detector quotients and independent reference
geodesics. The `.npz` arrays are ordinary integer/float arrays; no pickle is used.
The symbolic audit requires SymPy, already declared in the validation extra.

## The geometric solution and its exact scope

Use signature (-,+,+,+), null coordinates (u,v) and transverse coordinates (x,y):

\[
ds^2=-2\,du\,dv+dx^2+dy^2+H(u,x,y)du^2,
\qquad H=A(u)(x^2-y^2)+2B(u)xy.
\]

For arbitrary smooth profiles A and B this is a vacuum plane pp-wave. The metric
determinant is -1; its null two-by-two block has one eigenvalue of each sign,
so the metric is nondegenerate and Lorentzian without a small-amplitude
approximation. Its only potentially nonzero Ricci component is

\[
R_{uu}=-\tfrac12(H_{,xx}+H_{,yy})=0.
\]

Consequently all 16 components of the **full**, not linearized, Einstein tensor
vanish for Lambda=0. Curvature need not vanish:

\[
R_{uxux}=-A,\quad R_{uyuy}=A,\quad R_{uxuy}=-B.
\]

`pp_wave_geometry.py` computes the inverse metric, all Christoffel components,
all 256 mixed Riemann components, Ricci and Einstein tensors independently with
SymPy. It also checks the contracted Bianchi identity. Its negative control adds
`C(u)(x^2+y^2)`: the program must then return `G_uu=-2C`, not zero.

These are established continuum identities for Brinkmann plane waves; see
[Alvarez, Anero and Sanchez-Ruiz (2024), equations 4-7](https://doi.org/10.1140/epjc/s10052-024-12986-1).
The paper uses a different signature/normalization; this experiment fixes its
own convention above and derives the components directly from that metric.

The construction is a **new decoder**. It does not assert that the previous TT
metric readout in `PHASE_METRIC_EXPERIMENT.md` was already an exact nonlinear
solution. Its Einstein tensor is not inferred from the rank of the update tensor.

## Exact transport from the existing repository construction

The four source gears are the unchanged two-bank construction from
`retimed_tensor_wave.build(Q, axis=2)`. Write S for a forward z shift and

\[
\mathcal R(X,Y)=(Y,SX),\qquad
\mathcal R^{-1}(X,Y)=(S^{-1}Y,X).
\]

The fixed input is `(D/2)(R+R^-1)b`. With `a=R^-1 b`, Rule3 gives `b'=R b`.
Since twice the input is divisible by D, every source remainder stays fixed.
Induction proves the prepared transport identity in both time directions.
There is no phase callback and no coefficient change during a run.

At refinement n, let L=3n, dt=1/n, P=4096 n^2, Q=2P n^2 and D=6Q. Choose
two integer fine-ring profiles f and h of length 2L. Initialize

\[
b_{p.X}(z)=f(2z),\quad b_{p.Y}(z)=f(2z+1),
\]

and similarly for q.X/q.Y and h. At update t, `p.X=f(2z+t)` exactly. The local
sample decoder is `A=p.X/P, B=q.X/P`, with `u=(2z+t)/n`. The physical carrier
spacing in this convention is 2/n; one complete fine-ring period is six units
of u at every n. All three lattice dimensions increase, but only one prepared
propagation direction is tested. This is not a generic three-dimensional limit.

For a definite smooth continuum decoder, use the real periodic trigonometric
interpolant of the complete **initial** integer profiles. It reproduces their
samples and evolves by translation. This interpolation is a declared analysis
map, not a computation fed back into Rule3. Any smooth profiles satisfy the
continuum vacuum identity; this freedom alone is not evidence for emergent GR.

The mixed seed samples `sin(2*pi*u/6)/50` and `cos(2*pi*u/6)/75`, rounded once
to integer multiples of 1/P. Initial preparation uses floating point; all
subsequent state evolution is exact integer arithmetic. Exported integer seeds
are authoritative. Flat and wave cases at the same n have identical tensors.

## Autonomous detector and full geodesic reference

For a central geodesic at x=y=0 and u an affine parameter, transverse separation
obeys the exact plane-wave equation

\[
x''=A x+B y,\qquad y''=B x-A y.
\]

Two basis arms start at (1,0) and (0,1), with radial affine velocity 1/16.
Four additional ordinary gears encode their transverse positions with integer
scale `s=2^20 n^4`. The fixed inputs for each arm are

\[
u_x=D x+6(p.X\,x+q.X\,y),\qquad
u_y=D y+6(q.X\,x-p.X\,y).
\]

Every product is on-site and quadratic. The complete tensor has eight gears,
20 monomials and order three, below the allowed order four. The source reads
only its nearest face neighbors. All terms pass strict physical support.
The eight source-to-detector terms are explicitly designated **one-way test
body couplings**; the remaining terms pass the repository reciprocity check.

The exact integer identity checked at every site and update is

\[
D(x_{t+1}-2x_t+x_{t-1})
=12(p.X_t x_t+q.X_t y_t)+r_t-r_{t+1},
\]

and its y counterpart. After division by `D*s*dt^2`, the main term is precisely
the transverse geodesic force; the remainder acceleration has bound
`n^2/s=1/(2^20 n^2)`. The remainder is retained, not dropped in the audit.
Initial a uses the second-order Taylor value at -dt, rounded by exact rational
arithmetic. The observed second-order convergence is a finite four-level test;
it is not an all-seed or infinite-time stability proof.

For comparison, an independent RK4 solver uses the smooth decoded profiles,
with 64 and 128 substeps per Rule3 update. It integrates both transverse motion
and the longitudinal coordinate

\[
v'=\tfrac12[1+x'^2+y'^2+H(u,x,y)].
\]

This enforces timelike normalization -1 when u is proper time. The symbolic
audit verifies that its derivative satisfies the longitudinal geodesic
equation. **v is a reference reconstruction, not a runtime gear.** The runtime
detector represents transverse tidal motion, not a complete freely travelling
particle implementation or an emergent clock calibration.

The detector is read from signed official quotients at node zero. Given its two
declared starting positions, `x_next=ell-x_previous` reconstructs its position.
Missing event slots are zero; a separate check detects any missing nonzero raw
quotient instead of silently replacing the event stream. That audit passes for
the declared histories. This decoder is not asserted for arbitrary seeds.

## Boundaries, controls and criteria

The physical transverse chart is a local patch |x|,|y|<3; all measured arm
positions must remain inside. The expressions x^2-y^2 and xy are **not** glued
periodically across the board. A rational finite-difference test verifies zero
transverse Laplacian in the patch interior and detects nonzero seam residuals
if the same polynomial is incorrectly wrapped onto a torus. Periodic source
transport therefore does not establish a globally periodic physical metric.

Controls cover a flat seed, a plus-only seed, a traceful non-vacuum metric,
changing detector data without changing source histories, and violating the
prepared source relation. The last control still rewinds but fails the exact
travelling identity, distinguishing invertibility from the geometric claim.

The complete sweep reports maximum position error in units of initial arm
length, not relative error of a component that can cross zero. The finest
declared target is error <0.005 and last observed convergence order >1.5.
Reference substep-halving difference must be below 1e-8. Flat trajectories,
source shifts, official reconstruction, carry ledgers and full rewind are exact
checks. Fresh numbers and all complete traces are written under `runs/`.

## Recorded validation

The declared eight-case sweep gave these maximum componentwise transverse
position errors, normalized to the initial unit arm length:

| Refinement n | Step du | Mixed-polarization error | Flat error |
| --- | --- | --- | --- |
| 1 | 1 | 0.0111621646 | 0 |
| 2 | 1/2 | 0.00275014885 | 0 |
| 4 | 1/4 | 0.000684057366 | 0 |
| 8 | 1/8 | 0.000170742627 | 0 |

Observed orders were 2.0210, 2.0073 and 2.0023. Each refinement uses its own
rounded initial profile and its corresponding continuum reference. Thus the
table measures detector error for those decoded profiles, not an independent
proof of a continuum limit for arbitrary states. All eight histories passed
exact carrier transport, zero integer ledger residual, official-event decoding
and full-state rewind. The eight scoped tests and 13 existing quick tests passed.

## What this completes and what remains open

The follow-up [Einstein-Maxwell experiment](EINSTEIN_MAXWELL_EXPERIMENT.md)
adds an independently computed nonzero electromagnetic source and charged
test particles, with a separate negative test for naive reciprocal completion.

This completes a restricted chain: exact prepared integer transport, a declared
full nonlinear vacuum metric, symbolic Einstein/Riemann verification, and an
autonomous tidal detector with measured convergence to its geodesics.

It does **not** implement the general Einstein equations for arbitrary initial
data, a matter stress source and reciprocal backreaction, preservation of all
Einstein constraints in a general interacting state, universal propagation for
all existing ONE species, or a global physical interpretation of the periodic
cube. A two-way matter coupling would change this candidate and needs its own
constraint and convergence argument. These are separate research problems,
not consequences of exact rewind or a vacuum tensor with G=0.
