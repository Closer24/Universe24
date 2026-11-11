# Transported node channels and a common-metric acceptance test

This implements the first executable experiment from the
[channel proposal](CHANNEL_GEODESIC_PROPOSAL.md). One fixed **order-four**
integer tensor drives 26 channels per node through unchanged fixed-six Rule3.
The packet and two autonomous clock mechanisms really move between board
nodes. The experiment succeeds on a restricted axial family and **rejects
the candidate as a general operational metric** on held-out off-axis paths.

This is an optional model, not a modification of `one_system()`, nor an
equivalent refactor of either existing 48-channel pp-wave construction.

## Run and replay

```sh
python experiments/geometry/transported_probe_clock.py --out runs/transported-probe/report.json
python experiments/geometry/transported_probe_clock.py --replay runs/transported-probe/report.json
python -m unittest universe24.tests.test_transported_probe -v
```

The report exports the actual tensor, complete initial `(a,b,r)` arrays for
each case, every state digest, official events including empty observation
slots, snapshot measurements, source hashes, and passing/failing assessments.
Replay uses the exported tensor and seeds, compares all execution evidence,
and verifies exact rewind. Observation is snapshot-based; no click-only
reconstruction is claimed. A physically rejected candidate still exits
normally after producing its report; `common_metric_validated` is the
explicit physics result and is false for the default comparison.

The committed [compact report](../runs/transported-probe/checked.json) is
replayable with `--replay runs/transported-probe/checked.json`.
[Validation details](../runs/transported-probe/validation.json) record its
hash, source provenance and the five case assessments. The full 123-test
discovery passed, including five new tests and the existing pp-wave evidence
replays; the default 20-update CLI smoke run rewound exactly.

## Channels and responsibilities

| Channels | Count | Role |
| --- | ---: | --- |
| `E00` through `E33` | 16 | Integer coframe |
| `probe.X`, `probe.Y` | 2 | Localized marker, alternating banks |
| `control.X0` through `control.Y1` | 4 | Transported period-four oscillator |
| `candidate.X0` through `candidate.Y1` | 4 | Transported metric-dependent oscillator |

Each channel retains its own `(a,b,r)`. The coframe is prepared with
`a=b`, input `u=6b`, and remains stationary. This is a prepared solution of
the same engine, not a runtime freeze. A mismatched old history can drift
without bound under the same law; a test records this limitation.

The tensor is built in `layers/transported_probe.py`; complete data are made
in `prepare/transported_probe.py`; `observe/transported_probe.py` is passive.
The runner never overwrites fields, injects signals, resets clocks or invokes
a geodesic solver to steer the dynamics. Every term uses the target node
and at most one face neighbor. All inputs use old `b`, so inverse staging is
trivial. Geometry-to-clock terms are explicitly designated one-way; matter
backreaction and reciprocity of the whole construction are not claimed.

## Exact transport encoding

Let `S f(z)=f(z-1)` denote motion in positive z. For the marker use
`R(X,Y)=(Y,SX)`. For each clock use

    R(X,Y) = (QY,SX),       Q = [[0,-1],[1,k]],
    R^-1(X,Y) = (S^-1 Y,Q^-1 X),
    Q^-1 = [[k,1],[-1,0]].

The control has `k=0`. The candidate has

    k = -g_tt = E00²-E10²-E20²-E30².

This candidate coupling is a hypothesis, not a derived clock law. Products
of two coframe components and one clock component give actual input degree
three and tensor order four. Geometry is static on the declared seed, so R
is fixed along the prepared orbit. All transported inputs are

    u = 3 (R + R^-1) b.

Prepare `a=R^-1 b`. For every allowed remainder `0<=r<6`,
`divmod(2u+r,6)=((R+R^-1)b,r)`, hence `b_next=Rb` and the retained-history
relation is preserved. This establishes the complete-state embedding and
the conserved remainder ledger, not just agreement after discarding a bank.

Initially only X has a packet. On odd steps it occupies bank Y at the next
node; on even step `2n` it occupies X at `z0+n`. A clock's phase advances once
per two microsteps. Clock channels do not read the marker or a precomputed
proper-time counter: they carry their own two-component oscillator states.

## Metric and continuum comparison

Use the previously studied stationary pp-wave family with fixed scale P=1,

    F = c(x²-y²),       c in {0,1},
    E^a_mu = delta^a_mu + eta^aa l_a l_mu F,
    l = (1,0,0,-1),    eta = diag(-1,1,1,1),
    g = E^T eta E = eta + 2F l l^T.

The exact inverse certificate is `E(2I-E)=I`, so the coframe remains
nondegenerate on the prepared orbit. The continuum profile is harmonic;
for c=1 its transverse Hessian is `(2,-2)` and its curvature is nonzero,
including at the central axis where F itself vanishes. This is a chosen
vacuum metric, not a solution derived from generic initial data.

Only even microsteps are assigned continuum samples `t=2n,z=z0+n`, with
fixed transverse x,y. The longitudinal coordinate uses the covering space
when the packet wraps around the periodic z direction. The smooth interpolant
therefore has tangent `v=(2,0,0,1)` per macrostep. The odd staggered samples
are not asserted to lie on that uniform-speed interpolation.

Direct calculation from the metric gives

    g(v,v) = -3+2c(x²-y²),
    Gamma(v,v) = (0,-2cx,2cy,0).

The straight transported path is thus an affinely parametrized geodesic on
the central axis, and throughout the flat case. Off-axis in the curved case
it fails the transverse equation. Tests independently construct the metric
inverse and Christoffel symbols with SymPy; the trajectory oracle is not
`Engine.step`.

Each clock tick is a return of its measured phase to the initial phase at an
even sample. One flat calibration is declared per clock species: control
ticks represent `4 sqrt(3)` proper units; candidate ticks `6 sqrt(3)` units.
Neither calibration changes by location or curvature. This is calibration
against the chosen flat orbit, not a derivation of universal clock units.
The observer compares exact **squared rates** over complete cycles, so no
floating arithmetic or square-root approximation enters the acceptance test.
No completed cycle means insufficient clock evidence, never success.

## Recorded default result

Five cases use L=5 and 24 macrosteps (48 Rule3 updates), all under the same
tensor. Its fingerprint is
`8560ba937fd3b75f10b4e999a5febe0990cfcd85f443e64f73961f8ac7ed80ac`.
All five transport their localized marker and both clock states and rewind
exactly. The squared proper-time rates below are relative to coordinate t.

| c | x,y | Geodesic | Metric rate² | Control rate² | Candidate rate² | Joint result |
| ---: | --- | --- | ---: | ---: | --- | --- |
| 0 | 0,0 | Pass | 3/4 | 3/4 | 3/4 | Pass |
| 0 | 1,0 | Pass | 3/4 | 3/4 | 3/4 | Pass |
| 1 | 0,0 | Pass | 3/4 | 3/4 | 3/4 | Restricted pass |
| 1 | 1,0 | Fail | 1/4 | 3/4 | 3 | Fail |
| 1 | 0,1 | Fail | 5/4 | 3/4 | No returned cycle | Fail |

At x=1,y=0 the candidate period changes from six macrosteps to three. This
is a genuine geometric response, but it is the wrong proper-time response.
Changing only geometry while retaining identical complete non-geometric
initial data changes candidate-clock updates; the control and marker remain
unchanged. This separate test avoids confusing a seed change with feedback.

For the curved preparation, 60 seam nodes have nonzero transverse discrete
Laplacian; all interior values are zero. These seam failures are reported,
not reclassified as vacuum. The probe preparations leave room for the
interior derivative stencil. Nondegeneracy does not make arbitrary board
coordinates timelike or repair the global chart.

## What has and has not been implemented

Compared with the earlier single-carrier geodesic example, this experiment
adds actual board transport, independently evolving clock mechanisms, a
genuine rank-four metric-to-clock coupling, and a joint acceptance gate.
The restricted axial agreement and the failed held-out cases are separate
results. Passing tests that verify the failures do not turn them into
physical successes.

Geometry-responsive spatial motion, a clock law that passes the held-out
proper-time checks, null probes, backreaction, generic dynamical geometry,
constraint evolution and a continuum-limit study remain unresolved. The
global physics gate deliberately remains false. In particular, neither
integer reversibility nor the presence of a tensor of order four establishes
Einstein dynamics.
