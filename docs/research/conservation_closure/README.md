# Conservation, clocks and one native anisotropic Einstein sector

This six-researcher continuation constructs **one eight-channel exact native
diagonal Bianchi I solution family**, with massless scalar and comoving dust.
The same complete Engine state supplies the source, anisotropic metric,
conserved charges and source-based proper-time diagnostic. Its integers have
logarithmic bit growth. It extends the known homogeneous massless solution
from [PR59](https://github.com/Closer24/Universe24/pull/59); it does not replace
the genuinely massive spinor dynamics in [PR60](https://github.com/Closer24/Universe24/pull/60).

Coordination and independent handoffs are in [issue40](https://github.com/Closer24/Universe24/issues/40)
and [issue41](https://github.com/Closer24/Universe24/issues/41). The Engine,
installed runtime, canonical decoder and physical acceptance gates are unchanged.

## What conservation gives the actual integer board

Every fixed-six update, including nonzero carries, obeys

\[
\pi=6(b-a)+r,\qquad \pi_+-\pi=2(u-6b).
\]

Consequently, a reciprocal shift-invariant face interaction can give an exact
local current and a conserved global charge. The carry belongs to that charge.
The executed two-channel spatial control keeps its full charge at69, while
omitting carries gives6,0,6,6,0. This is a separate arithmetic tensor; its
metric/source are not the Bianchi metric/source. Its bit growth is not bounded
by the theorem for the selected native candidate.

Conservation also simplifies the physical homogeneous equations. Put

\[
V=a_1a_2a_3,\quad U=\dot V,\quad
P=V\dot\phi,\quad D=V\rho_d,\quad
H_i=\frac{U}{3V}+\frac{S_i}{V},\quad\sum_i S_i=0.
\]

Here the S_i are diagonal components of the conserved mixed shear density
V sigma^i_j in the chosen homogeneous basis. They are not spatial covectors.
With c=8piG=1, lapse1, zero cosmological constant and zero scalar potential,

\[
Q=U^2-3DV-\frac32\left(P^2+\sum_iS_i^2\right)=0,
\qquad \dot U=\frac32D,
\qquad \dot P=\dot D=\dot S_i=0.
\]

If one additionally fixes proper-time midpoint kinematics
DeltaV=h(U_++U)/2 and the positive branch U_++U>0, then conservation factors as

\[
0=Q_+-Q=(U_++U)\left(U_+-U-\frac32Dh\right).
\]

It uniquely selects the exact map **within those assumptions**:

\[
U_+=U+\frac32Dh,\qquad
V_+=V+hU+\frac34Dh^2.
\]

The midpoint relation and branch are additional conditions. Conservation
alone leaves wrong time calibrations and other dynamics possible.

## Complete-state realization and metric

For h=1/N retain W=4N^2V and read J=b_W-a_W+3D=4NU. The unchanged Engine uses
u_W=6b_W+18D, giving

\[
W_+=W+J+3D,\qquad J_+=J+6D,
\]

\[
\mathcal I=J^2-12DW-24N^2(P^2+\sum_iS_i^2)
\quad\text{exactly invariant}.
\]

Every other channel uses u=6b. Their prepared histories keep charges and
anchors constant, while the time marker has unit slope. All carries remain
retained and rewind. There are **8 channels,24 retained integers/node,9 linear
monomials**, no scheduler and no workspace. The same tensor is used at every N;
only the complete seed and static units change.

The passive full-state interpretation is

\[
I=\int_{U_{\rm ref}}^U\frac{2\,dv}{v^2-K},\quad
K=U^2-3DV,\quad
a_i=V^{1/3}e^{S_iI},\quad
\phi=\phi_{\rm ref}+PI.
\]

The anchors are retained. No external tick, trajectory solver or reference
integration supplies evolution. Roots, logarithms and exponentials occur only
in this declared diagnostic. Its stable log1p evaluation also covers the
independently discovered extreme backward-anchor cancellation regression.
Off-constraint inputs remain off constraint and cannot create an accepted bundle.

An independent derivation from this metric computes all Christoffel/Riemann
components and obtains

\[
G_{\mu\nu}-T_{\mu\nu}
=\frac{Q}{3V^2}\operatorname{diag}(1,a_1^2,a_2^2,a_3^2).
\]

The default seed D=1,P=2,S=(1,-1,0),U=4,V=7/3 has nonzero Weyl square
2736/2401. Erasing shear from the metric while retaining Q=0 fails the
Einstein/source comparison. The expansion is genuinely anisotropic.

## Clock and covector distinctions

The new integer clock invariant is J-Jref-6DT. The source clock

\[
\tau_{\rm source}=\frac{J-J_{\rm ref}}{6DN}
=\frac{2(U-U_{\rm ref})}{3D}
\]

advances by1/N using the actual volume history and dust charge. It never reads
the time marker or a saved run. Its agreement with the marker is checked,
not assumed. Changing the marker origin changes canonical click counts
without changing geometry or source; clicks are not automatically proper time.

A moving test body's conserved spatial covector p_i is distinct from mixed
shear density. The same metric gives

\[
E^2=m^2+\sum_i p_i^2/a_i^2,\quad
\frac{dx^i}{dt}=\frac{p_i}{a_i^2E},\quad
\frac{d\tau}{dt}=\frac mE.
\]

The four geodesic equations and index transformations are proved. These are
passive probe diagnostics: no probe trajectory, transported signal or detector
has been added to the retained state. The massless scalar is monotone in this
chart and is not a periodic material clock. A separate scoped quasipolynomial
proof prevents treating an unrestricted threshold as a free bounded-time
fixed-six instruction; it is not a no-go theorem for all physical clocks.

## Executed evidence

| Resolution N | Actual steps | Proper endpoint | Volume | Velocity | Peak retained bits |
|---:|---:|---:|---:|---:|---:|
|24|3|1/8|2185/768|67/16|13|
|48|6|1/8|2185/768|67/16|15|
|96|12|1/8|2185/768|67/16|17|

The exact native source endpoints coincide; no discretization-error estimate
is needed for this solvable source family. Numerical metric evaluation and
passive trajectory quadrature have their own precision/error controls.
Three saved runs through the ordinary runtime join exact tensor/seed identities,
scalar oracles, canonical clicks, every inverse and complete rewind.

An actual4096-step run reaches proper time512/3 with26-bit maximum integers
and2,654,208 independent scalar-register comparisons. The exact formula
W_n=W_0+nJ_0+3Dn^2 proves retained bit growth O(log N+log(1+n)) for fixed
physical preparation. This statement does not count passive transcendental
readout as exact integer arithmetic or solve the massive candidate's cost.

| Lane | Report | Contribution |
|---|---|---|
|1|[Native conserved state](01_native.md)|Exact source flow, full history, ordinary runtime, long-run bit theorem|
|2|[Tensor and metric](02_tensor_metric.md)|Independent all-component Einstein source, Weyl, basis and domain checks|
|3|[Covectors and geodesics](03_covectors.md)|Same-metric geodesics and bounded passive proper-time diagnostics|
|4|[Clocks and records](04_clocks.md)|Source-time invariant, click interventions and scoped threshold obstruction|
|5|[Noether and space](05_noether.md)|Carry-aware local continuity and explicit missing momentum constraint|
|6|[Independent review](06_review.md)|Independent recurrence, physical negatives, exact joins and restricted uniqueness|

## What remains unsolved

The same Bianchi tensor can preserve every pointwise Q while a nonhomogeneous
shear preparation violates the independent momentum constraint. A smooth
counterexample gives residual -3/7. The physical reader correctly rejects the
nonhomogeneous state. General gravity needs one face-coupled source/geometry
law with spatial curvature and momentum constraints, and either exact
propagation or proved convergent error bounds on its actual complete histories.

The massive potential destroys the specific constant-charge reduction used
here. PR60's massive construction and its exponential bit growth remain
separate. Operational material clock/detector records, general spatial
Einstein dynamics and a uniqueness theorem for the project's full physical
law remain unestablished. No quantum acceptance is inferred.

The primary literature read by the team is cited in each report. In particular,
[Caceres et al.](https://arxiv.org/html/1003.3491v1), section2.1, explains the
shear-index distinction; [Capozziello et al.](https://arxiv.org/pdf/gr-qc/9606050)
derives Noether reductions of known Bianchi equations. These known continuum
results motivate the chart. The fixed-six embedding, complete-state evidence,
counterexamples and software checks are derived here.

```sh
python -m validation.conservation_closure.run_all
python -m unittest universe24.tests.test_conservation_closure -v
python -m unittest discover -s universe24/tests -t . -v
python -m validation.system_smoke --out runs/conservation_closure/fresh-smoke
python -m universe24 verify --run runs/conservation_closure/fresh-smoke/run
```

Fresh evidence is in `runs/conservation_closure/`. The published compact
snapshot is `docs/evidence/conservation_closure.json`. The original PR59
source and evidence are preserved unchanged alongside PR60 in this branch.
