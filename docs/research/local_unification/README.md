# One local carrier–record interaction and its spatial source chart

This package follows [issue63](https://github.com/Closer24/Universe24/issues/63)
and the [eight-agent synthesis](https://github.com/Closer24/Universe24/issues/61).
It constructs one conservative reversible scattering mechanism and a
twelve-channel, source-coupled finite-chart extension. The ordinary sealed
bundle, fixed-six Engine, passive decoder and saved-run verifier remain the
only execution path.

The scope is explicit: repeated record-bearing scattering and a spatial
two-null-stream Einstein sector on a declared causal interior. It is not a
global periodic Einstein universe, a bound massive object, a material
proper-time clock, a Born rule or sustained complexity growth.

## The local collision

The four Boolean rails are record+, record−, carrier+, carrier−. The collision
exchanges 1001 and 0110 and fixes the other fourteen states. Write

```text
delta = ad(1-b-c) - bc(1-a-d)
G(a,b,c,d) = (a-delta, b+delta, c+delta, d-delta)
```

The fourth-degree terms cancel. G is an involution on all sixteen Boolean
states. It preserves a+c and b+d, as well as the separate record/carrier
counts. In lattice-ray units its positive energy is E=a+b+c+d, its signed
momentum is P=a+c-b-d, and E>=|P|. Carrier momentum changes by2delta and
record momentum by−2delta. A record is a moving part of the same account,
not an uncounted recoil register.

Two complete four-rail banks retain collision and streaming phases:

```text
F(A,B) = (G(B), S(A))
F^-1(A,B) = (S^-1(B), G(A))
u = 3(F(b)+F^-1(b))
a_initial = F^-1(b_initial)
```

All eight channels keep their full (a,b,r). Because0<=r<6,
divmod(6(F+F^-1)+r,6) leaves r unchanged and the ordinary Rule3 update gives
b_next=F(b) on this prepared sector. Induction proves the sector and inverse
for all time. Nonlinear terms are onsite cubic; each streaming term is linear
across one face. No additional scheduler or discarded history is used.

A cohort collides and moves once per two Engine ticks. The two banks are
staggered populations: consecutive collisions at ticks1 and2 are different
cohorts. Repeated use of one cohort is tested at1 and5, and2 and6.

## Repeated records and finite supply

A complete finite packet train produces selected encounters at one receiver
at ticks1,2,5,6. Used records move away and remain recoverable. Removing the
later ready-record supply under the same tensor prevents the second pair.
Collision-off and record-transport-off controls are separate laws with
explicit fingerprints, not substitute explanations of the positive run.

The dual rails distinguish absent, ready, used and double records. The
retained event record is not inferred from total arithmetic click count:
connected and disconnected controls can have equal click counts and
different carrier outcomes. All outcomes and complete histories are retained.

The preregistered random panel tests functional reuse and structural motifs
separately. Neither prepared routing success nor accumulated used-record
count is called complexity growth. Frozen texture, periodic recurrence,
exhausted supply and failed trials remain in the evidence.

## The twelve-channel source-dependent extension

Four additional complete channels carry plus/minus characteristic profile
coefficients for both banks. The packet prefix is exactly the same eight
channels and tensor rows. Geometry rows read the actual packet populations.

Let n+ and n− be the sums of the corresponding record/carrier rails.
Initial integer profiles satisfy the interior constraints

```text
F[j+1]-2F[j]+F[j-1] = -n_plus[j]
G[j+1]-2G[j]+G[j-1] = -n_minus[j].
```

The characteristic shift can therefore be written with a source term:
F[j-1]=2F[j]-F[j+1]-n_plus[j]. The native geometry rows use this identity
inside the same fixed-six tensor, rather than calculating geometry externally
after each step. Initial profile preparation is complete before evolution.

The full periodic integer state always rewinds. Its physical characteristic
interpretation requires the proved finite causal chart; source defects at
the periodic seam are exposed, not removed.

## Exact continuum geometry on the chart

Reconstruct f and g from the retained coefficients with centered cubic
cardinal B-splines. Their independently verified derivative identity is

```text
B3''(x) = B1(x+1)-2B1(x)+B1(x-1).
```

Consequently the discrete source constraint implies
f''=−sum(n_plus[j] B1) and g''=−sum(n_minus[j] B1). This is an exact
reconstruction identity, not an assertion that a finite difference equals
a derivative of arbitrary samples. The hat profiles are nonnegative.

Use u=t−x, v=t+x, R=f(u)+g(v)>0 and

```text
ds² = -2 R^(-1/2) du dv + R(dy²+dz²).
G_uu = -f''/R, G_vv = -g''/R; all other G components are zero.
```

The metric-to-Christoffel-to-Ricci calculation, covariant stress balance and
affine null-ray equations are independently checked. In units8piG=c=1,
the same ray profiles supply the source. Orthonormal energy density is
(n_plus+n_minus)/(2sqrt(R)), not the unweighted packet-count ledger.

At even Engine microticks both bank profiles have advanced one cell per
macrotime. The common readout recovers metric and source from those actual
retained profiles. Odd microticks are circuit stages. Source-neutral
record/carrier exchanges can change the labeled trajectories while leaving
total stress and geometry identical. Null coordinate speeds remain±1;
the metric changes affine parameter and locally measured energy.

This is a restricted physical interpretation with its units and chart
declared. It does not derive those choices uniquely from Rule3.

## Domain and explicit negative controls

On a periodic board, summing a discrete Laplacian gives zero. Hence a
globally periodic profile cannot satisfy Delta²F=−n with nonzero n>=0.
The construction therefore certifies a finite causal interior only, before
seam defects reach it. The complete outside state remains in the run and
in the inverse. No global physical acceptance is assigned.

The default plane-symmetric preparation uses L19 and six native ticks.
A coefficient comparison margin, inverse preparation and spline support
determine the allowed spacetime diamond. Positivity throughout that diamond
follows from nonnegative B-splines, partition of unity and positive initial
coefficient bounds. The reader must reject unsafe locations/horizons,
nonplanar or malformed states, source defects and R<=0.

Removing geometry's source terms leaves an invertible tensor but violates
its Einstein source constraint. Joining a different seed, tensor, horizon,
source revision or saved trace also fails acceptance. A shared Engine and
a matching channel count alone are insufficient.

## Reproduction and evidence

```sh
python -m unittest discover -s universe24/tests -t . -p 'test_local_unification*.py' -v
python -m validation.local_unification.run_all --out runs/local-unification
python -m universe24 verify --run runs/local-unification/geometry/runtime
python -m unittest discover -s universe24/tests -t . -v
python -m validation.system_smoke --out runs/local-unification-smoke
python -m universe24 verify --run runs/local-unification-smoke/run
```

Use fresh output directories. The collector binds the same twelve-channel
runtime to record, balance, source and independent acceptance evidence.
Separate eight-channel controls and random panels keep their own identities.
Source hashes, exact inputs, complete traces, canonical clicks, all trial
outcomes and integer bit costs are preserved in the output and CI artifacts.

| Report | Responsibility |
|---|---|
| [01_native](01_native.md) | Cubic conservative collision, complete-history sector and interventions |
| [02_balance](02_balance.md) | Positive kinetic accounts, record recoil and local/regional flux |
| [03_geometry](03_geometry.md) | Source-dependent native profiles and spatial Einstein chart |
| [04_records](04_records.md) | Retained provenance, repeated encounters and lifetime |
| [05_organization](05_organization.md) | Registered functional/structural tests and failures |
| [06_contracts](06_contracts.md) | Allocation, orientation and exact source/run joins |
| [07_geometry_review](07_geometry_review.md) | Independent spline, geometry and causal-domain proofs |
| [08_collection](08_collection.md) | One joined execution/evidence pipeline |
| [09_acceptance](09_acceptance.md) | Independent full-state scalar replay and adversarial acceptance |
| [10_limits](10_limits.md) | Exact boundaries for clocks, massive localization and growth |

The recovered implementation passed all 65 focused tests in the independent
combined-source review. The published source `fb4a09b2925a876d6c92493b2784fe30c16ed2e1`
also passed all five workflows in Python 3.11/3.12. Current combined-source
verification is recorded by the central acceptance command and its source
hashes. Historical results do not certify changed bytes; no software test
changes the remaining physical boundaries above.
