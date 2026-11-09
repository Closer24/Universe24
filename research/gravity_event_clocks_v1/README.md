# Milestone: full-48 event-wave equation and Einstein-gravity falsification controls

**9 November 2026 · Exact mathematics and bounded simulation, not a derivation of gravity.**

This self-contained *research module* adds reproducible tests and negative controls to the existing
[gravity status](../../docs/GRAVITY_STATUS.md). It is an evidence milestone, **not** a new forward law,
a physical clock/metric construction, or proof that Einstein gravity arises from Rule3. The only
state-changing law remains `universe24/core/rule3.py`; this module imports it, does **not** vendor or edit it.
All tests use every one of the 48 channels at each modeled site, not an allocated gravity subset.

## Exact algebraic findings

Let `A_sigma` be the fixed reciprocal 6-port operator, `L_sigma=6I-A_sigma`,
`(a_n,b_n,r_n)` the original complete channel state, and
`p_n=3(b_n-a_n)+floor(r_n/2)-1`. Since `a_n=b_(n-1)` and the quotient of
`2(A_sigma b_n)+r_n` by 6 is `b_(n+1)+a_n`, **every channel** satisfies

```
6*(b_(n+1) - 2*b_n + b_(n-1)) + 2*(L_sigma*b_n) + (r_(n+1)-r_n) = 0
p_(n+1)-p_n = -L_sigma*b_n
L_sigma*mean_T(b) = -(p_T-p_0)/T
```

All are *identities*, not approximate wave equations or a discovered mass source.
If a complete trajectory is periodic, `L_sigma mean_T(b)=0`; for a positive
connected graph that mean is channel- and space-uniform. If all counter
coordinates stay uniformly bounded, the same statement holds in the infinite-time
limit. This is a restriction on the **mean counter**, not on phase correlations
or all possible emergent gravity observables.

Write `r=2*theta+epsilon`, `theta in {0,1,2}`, `epsilon in {0,1}`. The exact
`divmod` identity is

```
ell = floor((u+theta)/3)
theta' = (u+theta) mod 3
epsilon' = epsilon
```

Therefore `epsilon` is a per-address passive invariant, and changing parity
alone cannot alter *any* present or future `a,b,theta`. This excludes a gravity
source encoded **only in remainder parity** in the unmodified Rule3. It does
not exclude a physically meaningful reading of parity in a different, coupled
measurement theory.

## Clock and distance controls (not a gravitational redshift law)

On `L=19` with `+++` coupling, source `(-1,-1,0)` on all 48 channels at `(9,9,9)`,
and candidate clocks A=`(-1,-1,0)` or B=`(0,-1,4)` on all 48 channels at
distance `d` along +X, source-present versus source-absent controls:

| Distance (lattice links) | A: complete-state recurrence | A: ticks in 20 update indices | B: complete-state recurrence | B: ticks in 20 update indices |
| --- | --- | --- | --- | --- |
| 1 | 5 | 4, regular | 5 | 4, regular |
| 2 | no period of length 1–20 fits 41 sampled states | 3, irregular | 20 | **5, irregular** |
| 3–6 | 4 | 5, regular | 4 | 5, regular |

**Long recurrence period ≠ slow physical clock.** The `d=2` B preparation
returns fully after 20 updates but still yields 5 threshold-ticks per 20
indices, the same *count* as the remote reference. The source strength and
initial remainder-phase scans also fail to give a universal monotonically
decaying source–radius law. `chi=1_{a<0<=b}` is a fixed, passive toy readout,
not calibrated proper time.

## Necessary Einstein-facing checks, not positive model results

* A varying stationary clock lapse can occur in **flat Rindler spacetime**;
  clock-rate variation alone does not prove curvature.
* In exterior Schwarzschild **isotropic radius** coordinates with
  `N=(1-q)/(1+q)`, `H=(1+q)^2`, `q=GM/(2c^2*rho)`, a calibrated physical null
  signal must satisfy `v_coord/c=N*(1+N)^2/4`; inserting `N=4/5` gives
  `81/125`, as a *hypothetical comparison*, not a Universe24 measurement.
* In the PPN weak-field, isotropic-coordinate convention, Einstein's
  `gamma=1` requires `d ln(v_coord/c)/d ln(N) -> 2`, if physical clocks,
  signals and distances have first been independently calibrated.
* The zero-spatial-momentum `+++` 48×48 coupling has exact polynomial

  `lambda^8 (lambda-6) (lambda-4)^8 (lambda-2)^14 (lambda+2) (lambda^2-4lambda-2)^8`.

  The `lambda=6` mode is the unique channel-uniform scalar mode. Only the
  *frozen-remainder linear comparison* has a gap to nonuniform modes at
  zero momentum. This is not a nonlinear no-go theorem for massless spin-2
  collective excitations.
* The microscopic spatial causal support follows cubic Manhattan graph
  distance; this is not an operational physical light cone. The scalar
  spatial stencil is leading-order isotropic at small momentum with
  direction-dependent quartic corrections.
* The smooth interpolation used for the previous *auxiliary* variational
  action has vanishing derivative of its tooth map at every integer. Thus
  its infinitesimal real tangent map does not propagate linear `b` waves;
  no physical continuum graviton may be inferred from this arbitrary
  interpolation. The native finite-integer Rule3 remains unaffected.

## Reproduce and provenance

Requires Python 3.11+; workers A and B use the standard library. Worker C
uses NumPy and SymPy. From the **repository root**:

```sh
python -m research.gravity_event_clocks_v1.worker1_algebra
python -m research.gravity_event_clocks_v1.worker2_clocks
python -m research.gravity_event_clocks_v1.source_phase_scan
python -m research.gravity_event_clocks_v1.worker3_einstein
python -m unittest discover -s tests -p 'test_gravity_event_clocks_v1.py' -v
```

Fresh outputs appear under `research/gravity_event_clocks_v1/results/` and may
replace local copies there. Tracked result snapshots and their full preparation
recipes are committed for audit; `source_phase_scan` is a finite phase control,
not a search across all possible source states.

**Core provenance:** Git commit `c5a23743d96936190210dd510105ed470d4a0b23`, with
blob SHAs: `rule3.py=dd2a7cdd34200aeb73aba64d02f6cccbfb32afe5`,
`coupling.py=16d959466bd31bbcf292b6c0e1e3f4f78f748900`,
`engine.py=2493378dd0b692491bca78c0250433189c96258d`,
`group_2o.py=16c4ae73de6b8208696196bf68517de2bd8548c8`,
`state.py=3d706224eef1ec158f78623efa453bc39b0afe30`.
The original local archive used three parallel **Python processes**, not
three independently orchestrated AI agents. This is a new repository publication
of earlier bounded local evidence; it is **not** a new physics breakthrough.

**Missing:** independently measured gravitational mass and energy-momentum,
a spatially extended autonomous source, operational universal proper time,
physical light, common Lorentzian metric and Einstein's field equations.
See the [physical benchmark sheet](../clock_selection/physics_targets/gravity.md)
for G0–G5 acceptance gates.
