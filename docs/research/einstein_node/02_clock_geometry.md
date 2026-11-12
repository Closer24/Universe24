# 2. What clocks can and cannot determine

Executed source: `validation/einstein_node_audit/clock_geometry.py`.
Evidence: `runs/einstein-node/clock_geometry.json`. These are exact symbolic
continuum controls and tests of the existing passive metric readout. They do
not evolve a physical clock in the Engine.

For a known chart and velocity, in c=1 units,

`Q(v)=(dτ/dt)²=-g00-2g0i vi-gij vi vj`.

With ADM lapse alpha, shift beta and spatial metric gamma, this equals
`alpha²-gamma_ij(vi+beta_i)(vj+beta_j)`, with beta components understood
contravariantly. Normal observers have `v=-beta`; grid observers have `v=0`.
Neither observer is automatically a freely falling material apparatus.

## Executed exact controls

1. Rindler `g=diag(-(1+a*x)²,1,1,1)` on `1+a*x>0`: stationary clock rate
   varies, `Gamma^x_tt=a(1+a*x)`, but all 256 Riemann components vanish.
2. Minkowski and flat-slicing de Sitter `g=diag(-1,exp(2Ht),exp(2Ht),exp(2Ht))`
   both have stationary rate one. Their Ricci scalars are respectively zero
   and `12H²`. De Sitter has `R^x_txt=-H²` and `Ric=3H²g`.
   This is an independent Einstein–Lambda reference, not an assertion that
   the current Universe24 law implements Lambda or this spacetime.
3. Ten timelike velocity readouts reconstruct every entry of an exact
   off-diagonal metric, including nonzero shift. Two held-out velocities
   reproduce their rates. Changing a spatial cross-term leaves the rest rate
   unchanged but is detected by moving samples.

For the reconstruction, use velocities `0`, `±epsilon e_i` and
`epsilon(e_i+e_j)` for `i<j`, all inside the timelike domain. Then

`g00=-Q(0)`;
`g0i=-[Q(+epsilon e_i)-Q(-epsilon e_i)]/(4epsilon)`;
`gii=-[Q(+epsilon e_i)+Q(-epsilon e_i)-2Q(0)]/(2epsilon²)`;
`gij=-[Q(epsilon(e_i+e_j))-Q(epsilon e_i)-Q(epsilon e_j)+Q(0)]/(2epsilon²)`.

This is identifiability **assuming a universal quadratic clock law**, a known
chart/velocities and calibrated units. Ten samples alone cannot prove that
law. The independent review supplies a nonquadratic impostor that agrees on
all ten samples and fails a held-out velocity. The current inputs are computed
from a metric, so success does not count as an independent measurement of it.

## Reproduced repository failure retained

Reviewer 2 ran `validation.geometry.transported_probe_clock.run(macrosteps=6,L=5)`
on main `4c494c1188f70eb8a677bf59765cc6e8571c6b88`. It internally verifies
step inverses and full rewind, allocates 26 channels and returns
`common_metric_validated=False`. Flat and central-axis controls pass, but:

| Curved preparation | Required rate squared | Control | Candidate | Geodesic residual |
| --- | ---: | ---: | ---: | --- |
| x=1,y=0 | 1/4 | 3/4 | 3 | (0,-2,0,0) |
| x=0,y=1 | 5/4 | 3/4 | No complete ticks | (0,0,2,0) |

No complete ticks means insufficient clock evidence, not a measured zero
rate. `layers/transported_probe.py` explicitly calls `k=-g_tt` a hypothesis
and its marker transport geometry-blind. Conversely, the restricted pp-wave
phase-space construction has selected geodesic arithmetic but does not
transport that particle through board nodes. These are different tests.

Reference: [David Tong, Geodesics in Spacetime](https://davidtong.org/teaching/general-relativity/grhtml/S1),
sections on accelerated coordinates, time dilation and particle action.
The exact controls and tomography above are direct calculations, not an
attribution of Universe24 results to this reference.
