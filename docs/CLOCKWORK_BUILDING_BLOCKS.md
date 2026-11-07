# Clockwork replay and signal-started building blocks

The prepared Rule3 guide starts two local counter clocks and writes finite
internal records in a single complete trajectory. An offline replay renders
those exact counters as clock hands and the retained remainders as six-position
gears. The display reads saved states; it adds no mechanism to the automaton.

The result is deliberately narrower than physical light operating all matter.
The tested front propagates through a prepared medium. The source is a pair of
initial counter perturbations. Source-free receiver preparations are completely
stationary, but an activated receiver can keep cycling when its incoming sum is
zero. Thus these are **signal-started devices**, not evidence of continuous
optical power or an energy law.

## Open and reproduce the demonstration

The retained publication bundle is retained under
[`research/building_blocks/evidence/`](../research/building_blocks/evidence/).
Open its `clockwork.html` in a browser. Select a run, press Play, or scrub to an
integer update. Select any guide site to see both channel triples and the exact
identity `2u+r = 6ell+r_next`. The memory timelines include record reset and
later clicks. The file works offline and has no external resources.

From the repository root:

```bash
python -m research.building_blocks.run --output runs/my-clockwork
python -m research.building_blocks.verify_bundle --bundle runs/my-clockwork
python -m research.building_blocks.reproduce_studies --output runs/my-studies
python -m unittest discover -s tests -v
```

Use new output names. **The first command intentionally exits 1:** one frozen
scientific prediction failed. Its evidence and replay are still produced. The
verifier exits 0 only when the exact states, displayed values and retained
positive and negative outcomes reproduce correctly. A green reproduction check
must not be described as acceptance of that failed prediction.

An optional scientific GIF renderer uses Pillow, independently of the engine:

```bash
python -m research.clockwork.render_animation runs/my-clockwork/replay_data.json --output runs/my-animation
```

All documentation is English. No `universe24/` file, Rule3 coefficient,
per-channel state, coupling topology or arithmetic-click semantics changed.
The branch is based on the reliability PR; it does not merge that PR or main.

## Exact mapping from numbers to clocks and gears

A counter dial shows the direction of `(a,b)`; the exact signed values remain
visible because direction alone loses amplitude. At `(0,0)` the dial is marked
at rest. The six-position gear shows the exact remainder `r`, not a decorative
rotation. The UI displays the actual neighboring sum `u`, quotient `ell` and
both old/new triples for the selected completed transition.

The local identity is `2u+r=6ell+r_next`. Writing `r=2theta+epsilon` gives
`u+theta=3ell+theta_next`, with invariant parity `epsilon`. When `u=0`, the
counters obey `(a,b)->(b,-a)` and the remainder stays fixed. The clock image
therefore explains a measured projection; it is not a mechanical cause of the
update or a derivation of physical time. See [the proofs and finite
certificates](CLOCKWORK_ALGEBRA.md).

Only channels 0 and 14 along the guide appear as clocks. Every full-state
checkpoint retains all other channels and the off-guide remainder field.
Support counts refer to the complete retained state. Frame SHA-256 identifies
the full checkpoint including the update index; stationary states at different
indices therefore have different checkpoint digests. Spatially normalized
comparison hashes omit that index.
Ignoring that field would invalidate inversion and falsely localize some
oscillator motifs.

## Prepared component interface

The background is `(0,0,2)`. At guide position 0, channels 0 and 14 start as
`(0,1,2)` and `(0,-1,2)`. Receivers j=1 through N start as `(0,0,4)` and
`(0,0,0)`. All other counters start at zero. The tensor stays fixed throughout;
the visual assembly uses signs `+++`, while the separate signal and structure
studies test all eight existing sign triples. No new tensor architecture was
introduced.

| Component | Input and output | Timing and range |
|---|---|---|
| Candidate signal | Initial source disturbance, then first nonzero receiver b | First arrival at t=j in the successful prepared guides; no free-light claim |
| Clock | Arrival starts counter pair `(0,1),(1,0),(0,-1),(-1,0)` | Local projected period four within the declared first record window |
| Memory | Internal remainder predicate `M=1 iff (r0,r14)=(0,4)` | Temporary first window `[j,2(N+1)-j)` |
| Click | Passive rising edge of M | Distinct from the engine's unchanged arithmetic C0/C1/C2 classes |
| Composition | Two predefined receivers in the same guide | Both operate on N24 and fresh N28 preparations |
| Transfer control | Initially unarmed guide site or a preloaded transverse control source | Restricted state-dependent transfer observed; reliable persistent clutch not established |
| Recurrent cluster | Preloaded counter motif plus its complete remainder halo | Exact prepared periods 4,5 or7; not source-created matter or demonstrated attachment/breakup |

These are engineered preparations. No broad basin of simple random initial
conditions or spontaneous assembly is established. Two readouts in a shared
guide are a first composition test, not arbitrary plug-compatible components.

## What the demonstrated runs show

The registered visual protocol is
[`U24-CLOCKWORK-ASSEMBLY-v1`](../research/building_blocks/protocol.json).
It was frozen before its seven runs, within this session; this is not an
independent timestamped registration. All 400 forward updates have exact
one-step inverses and complete rewinds. The N24 traces match exactly between
L151 and L171 after spatial normalization. All retained nonbackground support
stays off the boundary in these trajectories.

| Preparation | Receiver | First click | First continuous record |
|---|---|---|---|
| N24, L151 and L171 | j6 | 6 | t6 through t43: 38 samples |
| N24, L151 and L171 | j12 | 12 | t12 through t37: 26 samples |
| N28, L181 | j8 | 8 | t8 through t49: 42 samples |
| N28, L181 | j16 | 16 | t16 through t41: 26 samples |
| No source | j6, j12 | None | Whole configuration remains exactly stationary |
| Source without guide | j6, j12 | None through t56 | No target record in the registered horizon |
| Odd remainder at j6 | j6 | None | Counter clock starts at6, but fixed memory readout fails |
| Unarmed site at j10 | j12 | 32 | Delayed records occur; the no-transfer prediction fails |

The j6 record in the N24 run resets at44 and clicks again at56. A zero record
is not a return to the entire initial state or erasure of the source history.
The full inverse recovers the initial preparation. No quantum-collapse claim
follows.

**The complete visual protocol is not accepted**, because it predicted no
activation or record beyond the gap through t56. Observed j12 clicks are
32,38,42,50. The original protocol bytes and readout are retained. The replay
labels this case as a failed criterion. The successful complete-guide result is
a narrower, separately identified observation; the failed control is not hidden.

## Bounded research and independent review

Six agents handled distinct work: algebra, propagation, component composition,
recurrent structures, visual rendering and independent review. Their findings
were inspected and the five executable study outputs were regenerated by the
project lead. Deterministic scientific fields match; only explicit interpreter,
checkout and runtime metadata are excluded from portable comparison.

| Study | Registered question / budget | Observed decision |
|---|---|---|
| [Algebra](CLOCKWORK_ALGEBRA.md) | Exact clock/gear identities and source-free stationarity; 60 CPU seconds | Proofs plus 14 finite cases; 360 updates/inverses |
| [Signal family](SIGNAL_STUDY.md) | Sign/phase/amplitude propagation and whole-state translation; 120 CPU seconds, 20,000 stored-channel cap | 24/96 guide cases meet unit-speed criterion; 24 controls; zero compact translation certificates in 40 seed cases |
| [Components](COMPONENT_STUDY.md) | Composed records, perturbations and control-source clutch; 120 CPU / 300 wall seconds | Two prepared compositions work; 1/30 strict perturbation interfaces passes; 0/24 clutch candidates meets retention criterion |
| [Structures](STRUCTURE_STUDY.md) | Full-state recurrence and finite support; each version 120 CPU seconds | 72/128 fresh halo cases pass radius-one criterion; 56 fail; source-created binding remains unresolved |
| [Independent review](BUILDING_BLOCKS_REVIEW.md) | Separate matrix-based gather, readout and artifact integrity | Complete replay agrees; corruption tests reject altered state, displayed memory/geometry and missing provenance |

A structure-v1 acceptance conjunction was impossible by construction because it
required source/guide support to stay only at the target sites from t=0. It is
retained as a protocol-design failure, not physical negative evidence. A fresh
v2 tests a defined finite halo on new sizes and phases. Short-budget failures
are inconclusive; finite searches are not impossibility proofs.

The browser workflow tests all controls and exact displayed values, captures
desktop/mobile views and records errors. Its green result concerns rendering
and replay. CI also reruns the bounded research and preserves the scientific
failure. The reliability suite continues to test the unchanged engine with
both Python 3.11 and 3.12.

## Next decisive experiment

The control-source study found a useful failed candidate: a transverse source
arms a gate before data arrives and permits a downstream click, but the first
record lasts one sample instead of the registered four. The next experiment
should search initial source/guide states that separate this priming pulse from
its later reversal. Keep the four-sample criterion, single-source null controls,
full inverse and held-out gate positions; do not relax the criterion to accept
the near miss. A bounded follow-up can use 10,000 preparations or 120 CPU seconds,
whichever comes first, with an independent confirmation budget of 120 CPU seconds.

Only after a reusable transfer interface survives new phases, preparations and
composition should the project broaden to light-like dispersion/isotropy,
conservation, scattering and physical click predictions. No structural model
change is justified by these results. Decisions on new tensor architectures,
model variants or the next research direction remain with Alon Gonen.
