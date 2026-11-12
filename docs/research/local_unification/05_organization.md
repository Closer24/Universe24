# Repeated local use, finite resources and structural controls

This audit observes the **same eight-channel conservative paired-bank tensor**
used by the native construction and balance audit. It adds no state, scheduler,
runtime chooser or external reset. Coordination and preregistration are in
[issue63](https://github.com/Closer24/Universe24/issues/63).

The protocol was posted before execution. Two pre-execution amendments followed
the shared construction from the initial three-channel proposal to paired banks,
then to the final conservative four-rail collision. Both amendments are linked
in the executable `PROTOCOL`; the earlier abandoned designs supply no evidence
for this result. The original PR54 sorter and its failed growth trials are
unchanged historical results.

## One actual repeated-use result

At each node the local collision exchanges only

\[
(r_+,r_-,c_+,c_-)=(1,0,0,1)\longleftrightarrow(0,1,1,0).
\]

All fourteen other Boolean inputs are fixed. A ready record `(1,0)` therefore
routes an incoming left-moving carrier `(0,1)` into the right-moving carrier
port `(1,0)`, with the distinction retained in the outgoing record `(0,1)`.
The reverse interaction remains part of the same invertible law.

There are two four-rail banks. `F(A,B)=(G(B),S(A))`, so one stream undergoes
successive collisions two computational updates apart. The audit reads old
bank B and new bank A at every update and keeps every outcome: corrections,
reverse corrections, unchanged split inputs, ties, absent records and double
records. It does not count only successful ready events.

The complete initial packet train in `native.repeated_fixture` gives corrections
at one predeclared receiver on updates **1,2,5,6**. Thus the same cohort succeeds
at **1 and5**, and the other at **2 and6**. Incoming records and carriers are all
present in the complete initial state. No later input is injected and no old
history or carry is reset.

The exact designed result is reproduced at side lengths7 and9, in all six face
directions, with four variants: **48 executed histories**.

| Variant | Receiver correction updates | Interpretation |
|---|---|---|
| Shared tensor and full finite supply | 1,2,5,6 | Two uses per cohort |
| Record transport disabled | 1 | The designed later tasks lose their supply |
| Collision disabled | None | Transit alone does not implement the preference |
| Later ready records removed, same shared tensor | 1,2 | The second task of each cohort is blocked |

The last control changes only the declared initial preparation under the same
law. It removes two later record packets while retaining the current carrier
pattern. The complete old histories are recalculated by the required inverse
preparation; this is **not** claimed as a complete-old-and-current-carrier-matched
intervention. The first two variants change the tensor and are explicitly
labelled mechanistic controls. Every complete history rewinds.

This establishes finite prepared repeat use, rather than an indefinitely renewed
resource, a bound material apparatus, structural growth or a cosmological burst.

## Unfiltered held-out panel

The fixed panel uses sides3 and5, seeds101/509/2027, six directions,24 updates,
three record preparations and three tensor variants: **324 trajectories and
7,776 Engine transitions**. All4,727,808 current-register comparisons agree with
the separately implemented first-order collision/transport oracle. Every step
is inverted, every run rewound, and every legal carry class retained. The
complete initial/intermediate/final `(a,b,r)` states of every panel case are
saved in `complete_panel.jsonl.gz` with a content hash.

The receiver is node0, cohort phase0, specified before the runs. A repeat means
at least two genuine inversion corrections at that same receiver/cohort; it is
a functional count, not a measure of structural complexity.

| Record preparation | Variant | Cases | Receiver repeat passes | Corrections over all sites/updates | Reverse corrections |
|---|---|---:|---:|---:|---:|
| Ready | Shared | 36 | 11 | 6,698 | 5,531 |
| Ready | Record transport off | 36 | 13 | 7,100 | 6,408 |
| Ready | Collision off | 36 | 0 | 0 | 0 |
| Depleted | Shared | 36 | 11 | 5,148 | 6,276 |
| Depleted | Record transport off | 36 | 13 | 6,111 | 6,730 |
| Depleted | Collision off | 36 | 0 | 0 | 0 |
| Mixed | Shared | 36 | 10 | 4,268 | 4,254 |
| Mixed | Record transport off | 36 | 13 | 4,239 | 4,210 |
| Mixed | Collision off | 36 | 0 | 0 | 0 |

The shared law has32 repeat passes among108 cases. Disabling record transport
has39, so this panel **does not support a universal advantage from streaming
records**. The designed packet train proves a specific supply-dependent
mechanism. Its result must not replace the unfiltered random-panel outcomes.

## Structural growth remains failed or untested

The old spatial motif formula counts distinct nonuniform axial carrier triples
that occur at multiple sites and persist at those same sites. It is applied
separately to the two carrier banks at two-update checkpoints. The inherited
requirement of at least four episodes with strict growth is retained. In this
new paired-bank protocol, episode activity is a complete-window count of actual
retained record-plus changes; it is not the old canonical-click count and is
not a calibrated physical burst.

Across the216 bank histories of the108 shared cases, strict-growth results are
**0 passed /19 failed /197 blocked by insufficient episodes**. None of the108
joint cases passes both banks. The frozen-random control still scores38; fresh
random and periodic controls are also retained. These three control sequences
are readout falsifiers, explicitly not asserted to be Engine trajectories.

Consequently persistence of this motif score does not identify useful causal
organization. Functional routing results and the motif statistic are reported
separately; a correction count is not renamed complexity. A future stronger
organization test needs an independently motivated observable and must retain
random, frozen and periodic controls.

There is also an exact structural limitation. The collision preserves
`record+ + carrier+` and `record- + carrier-` separately, so the total right/left
packet occupancy follows free streaming. This tensor changes species labels
and their correlations along crossing packet paths; it does not create new
total-density structure. This limitation coexists with real reciprocal
species-momentum exchange.

## Exact stationary-ensemble and recurrence boundary

For a finite invariant sector, a bijection `F` and an invariant distribution
`mu`, change of variables gives

\[
\mathbb E_\mu[C(F(S))-C(S)]=0.
\]

No scalar state function can increase strictly around a periodic orbit. The
eight Boolean current rails evolve by a permutation on a finite periodic
board. On the proved preparation `a=F^-1(b)` with fixed legal carries, the full
retained state also belongs to a finite invariant sector. Hence indefinite
strict growth of a state-only organization statistic is impossible **for this
candidate sector**. This is not a theorem excluding unbounded-integer Rule3
sectors or finite-window/nonstationary/subsystem organization claims.

Independent enumeration of all16 collision inputs gives:

| Exact preparation distribution | Mean change of `carrier+ - carrier-` |
|---|---:|
| Uniform carrier inputs, ready record10 | +1/2 |
| Uniform carrier inputs, depleted record01 | -1/2 |
| Uniform over all16 inputs | 0 |

This isolates a preparation-dependent routing bias. It is neither thermodynamic
entropy nor a physical-complexity law. Record transport preserves provenance;
it does not evade recurrence or provide a free source of nonstationary
preparations.

## Reproduction and acceptance

```sh
python -m validation.local_unification.organization --out runs/local-unification/organization
python -m unittest universe24.tests.test_local_unification_organization -v
```

Six focused tests pass: same-receiver same-cohort repetition, same-law late
supply depletion, disconnected collision, rejection of fabricated/off-domain
collision observations, the exact conditional ensemble means, and retained
random/frozen/periodic controls. Tests deliberately preserve the negative
claims. The report records hashes of the shared native source, this audit,
inherited metric source and full compressed histories.

Shared geometry/source and proper-time apparatus are independent obligations
on this same law. They cannot be certified by these functional or motif tests.
