# One constrained homogeneous Einstein law

This seven-researcher round constructs and tests **one shared six-channel
candidate** for the homogeneous, isotropic, expanding Einstein system with a
neutral massive scalar and comoving dust. Its source, geometry, constraint and
matter-phase observations belong to the same tensor and complete seed.

The exact physical constraint and finite-time convergence are proved. Efficient
bit cost, spatial degrees of freedom and an operational clock detector remain
unresolved. This is not an accepted general Einstein universe or a new runtime.

Coordination: [issue40](https://github.com/Closer24/Universe24/issues/40) and
[issue41](https://github.com/Closer24/Universe24/issues/41). The source begins from
the consolidated #56 research baseline `4c2abdda08c4212d08896bd2bd933a7c8dd42c1c`;
its later workflow/documentation fix `f4f64e062f07b3ca119eccf655df746be206908b`
is retained as the publication parent.

## The single construction

The retained channels are a common denominator and five numerators for
`sa,sb,sc,se,beta`. Each keeps its complete `(a,b,r)` triple: **6 channels,
18 integers per node**. The coordinate names `sa,sb` do not denote the Engine's
old/current history banks. The passive coordinate readout is current numerator
divided by current denominator; both retained histories and every remainder
remain in the state and rewind exactly.

For four decoded real coordinates a,b,c,e define

\[
\sigma=(a^2+3b^2)/2,\quad q=c^2+3e^2,\quad
p=ac+3be,\quad y=bc-ae,
\]

\[
k=-\sigma-q/12,\qquad
\phi=2\sigma-q/6-y,\qquad d=\sigma-q/12+y.
\]

Then **for every coordinate value**, not only a constraint-prepared slice,

\[
\boxed{6k^2-p^2-\phi^2-2d^2=0.}
\]

The actual cubic coordinate vector field G satisfies the exact pushforward
identity `DP(z) G(z)=F(P(z))` for the existing full44 source restricted to

\[
\dot k=3k^2-(\phi^2+d^2)/2,\quad
\dot p=3kp-\phi,\quad \dot\phi=p,\quad
\dot d=3kd/2,\quad \dot\beta=k.
\]

All dots refer to synchronous normal proper time, with mass squared one. The
same beta defines

\[
ds^2=-dt^2+e^{-2\beta}(dx^2+dy^2+dz^2).
\]

Exponentiation is passive. The homogeneous polynomial update never needs it.
This gives a positive spatial metric at every finite decoded beta. The exact
retained-history recurrence also proves beta nonincreasing on the prepared
domain. Independent four-dimensional curvature contraction reproduces the
same scalar/dust stress in the continuum.

The coordinate force is compiled once into 58 cubic integer monomials, all
onsite and therefore within strict face support. The existing Engine advances
the ordinary full state with divisor six. Its numerator recurrence is

\[
D_+=CD^3-D_-,\qquad
P_+=C\bigl(D^2P+hD^3G(P/D)\bigr)-P_-.
\]

The apparent ratios in this identity expand to the precompiled homogeneous
polynomial; there is no runtime division except the fixed-six primitive.
The integer multiplier clears static coefficients. No projection, reset,
discarded carry, callback or second hidden history is used.

This avoids the earlier cross-history constraint defect because physical
variables are now decoded quadratically from the coordinates. A proof for
linear physical readouts of independently null histories does not prohibit
this construction. The physical interpretation has changed explicitly; it
is not an equivalence claim for the old full45 trajectories. An arbitrary
rational physical seed also need not have a rational coordinate lift.

## Actual same-state evidence

| Item | Exact default |
|---|---|
| Parameters | h=1/24, mass squared1, lapse1, zero cosmological constant |
| Coordinate seed | sa=1; sb=sc=se=beta=0; D=4; old registers0 |
| Physical seed | k=-1/2, p=0, phi=1, dust=1/2, B=1 |
| Carries | `(channel+node) mod6`, all six legal values retained |
| Tensor SHA256 | `8d5f0fad5d094908afd4e78d05e60710b96c95943bb7aa791e5b753ff33e9df9` |
| Complete seed SHA256 | `61b79e0831d775508ab04086aa4f4009d89bb6df95e2357e4ee7e5ff2777097f` |
| Allocation | 6 channels, 18 retained integers per node, 27 nodes |
| Law | 58 cubic terms, static multiplier3456, no old-a tensor reads |
| Executed common handoff | 3 steps; scalar oracle, complete inverse/rewind, ordinary bundle/runtime, saved trace and verification |
| Peak retained bits | 3 at preparation, then18,66,207 |

At fixed proper time T=1/8, three separately fingerprinted timestep laws use
the same physical and complete integer seed. The physical comparison integrates
the independent Einstein variables, not the coordinate equations used by Engine.
An independent high-precision reference was checked at two much finer resolutions.

| Steps | h | Maximum physical-field error | Scalar phase error | Dust-mass error | Peak bits |
|---:|---:|---:|---:|---:|---:|
| 3 | 1/24 | 0.00342429 | 0.00330197 | 0.0000567 | 207 |
| 4 | 1/32 | 0.00254453 | 0.00245409 | 0.0000415 | 649 |
| 6 | 1/48 | 0.00168089 | 0.00162144 | 0.0000270 | 6101 |

Every tested tick has exact decoded Hamiltonian constraint, positive metric,
retained carries and complete rewind. Observed field order is approximately1.03
and1.02. A separate analytic proof gives first-order convergence of the actual
history-dependent map for this declared seed, h=1/m<=1/16 and T<=1/8. It also
supplies uniform finite-time bounds on the coordinate norm and metric.

Dust mass `d² exp(-3 beta)` is conserved in the continuum but has a strictly
nonzero finite-step drift, bounded independently in the clock audit. Scalar
phase is monotone on the tested interval and globally in the corresponding
continuum solution, but phase/m is not universal elapsed proper time. No
autonomous tick counter, moving packet or detector has been allocated.

## Seven connected reviews

| Researcher | Report | Role in the selected law |
|---|---|---|
| 1 | [Constrained coordinates](01_coordinates.md) | Exact quadratic decoder, cubic Einstein pushforward, all33 full-source constraints, continuum future existence |
| 2 | [Hamiltonian and dust](02_hamiltonian.md) | Independent canonical equations, source/energy continuity and dust-mass obligation |
| 3 | [Native scheduler](03_native_scheduler.md) | Separate counted arithmetic bridge toward replacing the costly projective encoding; not used to certify the selected tensor |
| 4 | [Invariant map](04_invariant_map.md) | Actual-history domain theorem, first-order convergence and independent physical refinement |
| 5 | [Metric and proper time](05_spatial_metric.md) | Independent4D Einstein tensor/source, exact beta-history theorem and same-trace metric bounds |
| 6 | [Matter clock acceptance](06_clock_acceptance.md) | Predeclared phase/source/dust tests on the same three-resolution family |
| 7 | [Independent review](07_review.md) | Independent complex-pair force and recurrence oracles, exact evidence joins and wrong-dynamics controls |

The review rejects updates that preserve the decoder's constraint but violate
scalar evolution, metric evolution or dust conservation. It also caught and
fixed a warm-cache input bug that could admit a float or boolean timestep after
an equal Fraction had been cached. Exact input validation now precedes caching.

## Boundary and reproduction

The construction genuinely joins the restricted Einstein source, metric and
clock diagnostic. The remaining limits are concrete:

- The retained cubic projective denominator still has exponential bit-length
  growth in the number of updates. The three-resolution proof is not an efficient
  long-time simulation result.
- Spatial modes, anisotropy, electromagnetic fields and charged scalar phase
  are omitted. Homogeneous comoving geodesics do not establish transported
  material packets or general geodesic dynamics.
- Exact algebraic constraints coexist with time-discretization errors. Finite
  ticks are not exact continuous Einstein evolution or exact dust conservation.
- The native scheduler is separately counted and tested. Its results cannot be
  relabeled as an efficient realization of the selected cubic spinor law.

```sh
python -m validation.unified_law.run_all
python -m unittest universe24.tests.test_unified_law -v
python -m unittest discover -s universe24/tests -t . -v
python -m validation.system_smoke --out runs/unified_law/new-smoke
python -m universe24 verify --run runs/unified_law/new-smoke/run
```

Use a fresh smoke directory. Fresh evidence belongs in `runs/unified_law/`;
the published snapshot is `docs/evidence/unified_law.json`. The installed
Engine/runtime and general physical-acceptance gates remain unchanged.
