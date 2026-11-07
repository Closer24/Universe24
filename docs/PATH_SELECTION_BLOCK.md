# Prepared path competition and the cooperation hypothesis

This study separates a usable finite routing interface from a proposed law
that favors higher cooperation. The latter prediction failed. All preparations
use one unchanged body-013 engine, one fixed `+++` tensor, one board, 48 channels
per node and six spatial inputs. Components assign initial triples once;
neither scores nor click readouts issue an evolution instruction.

## Registered selection study

The [frozen protocol](../research/component_studies/selection_protocol.json)
defines nine two-site patterns. Each arm has six sites. At sites 2 and 3,
letters independently select paired remainders `O=(4,0)`, `N=(2,2)` or
`R=(0,4)` on channels 0 and 14. Other arm sites use O, and apparatus counters
start at zero. A centered source is prepared with one of three counter phases.

The generic component library assembles every case. The preparation check
independently compares its complete initial triples with the declared recipe.
The library does not certify behavioral composition.

The primary score is **calibrated two-site nonadditivity**, not a general
measure of physical complexity. In isolated calibration runs, perturb either
site, both sites, or neither. For all 48 outlet b counters at steps 6 through
15, form the exact mixed vector

`D = Y_both - Y_site2 - Y_site3 + Y_none`.

`C_pair` is the number of nonzero coordinates divided by 480. All calibration
vectors and scores are saved before any joint source-present experiment.
The older binary K metric is retained only as a diagnostic. The original
54-run K failure is unchanged.

Eligibility requires both isolated paths to transmit and generate genuine
guarded arithmetic C events, unequal scores, equal arm lengths, the same
source input, and identical isolated arrival tuples: first complete-state
change, first nonzero b, and first C. This excludes the earlier O/R apparatus's
step-6 versus step-10 arrival confound.

## Results

The [complete result](../research/component_studies/selection_evidence_v1/result.json)
contains all 432 registered trajectories: 72 calibration runs, 36 additional
isolated-input controls, 81 null cases and 243 ordered joint comparisons.
All 15,930 forward steps passed exact one-step inverse checks and complete
rewinds. Every null board was stationary. Complete compressed native
checkpoints, input manifests, source snapshots and hashes are retained beside
the result. Computation used 14.66 CPU seconds.

There were **10 eligible arrival-matched comparisons, zero higher-score-only
outcomes and 10 counterexamples**. Six selected only the lower-score path;
four left both outlets quiet. This refutes the specified finite-family
prediction. It is not an impossibility proof for every complexity measure or
every admissible initial state.

A concrete counterexample is left pattern OR versus right pattern NO.
Both isolated outlets first change, transmit and click at step 10. OR has
`C_pair=0`; NO has `C_pair=1/60`. In the joint run only OR reaches its outlet,
while every retained component of the NO outlet equals its null control
through steps 6–40. Swapping the arms swaps the winning physical side. The
winner is therefore the lower-scoring pattern in this comparison.

The study nevertheless contains 16 **phase-conditioned competing-route
comparisons**: both paths transmit in isolation, but only one joint outlet
transmits and clicks. None of the pattern pairs passes the frozen requirement
across all three source phases and both swaps. Consequently the original
strong-candidate and competing-candidate selections are both empty, and its
planned holdout gate stays closed.

## Scope and follow-up

The outlet winner produces multiple arithmetic events, not a single clean
photon or a persistent internal acknowledgment. A quiet outlet does not imply
information erasure, quantum collapse or a complete-board loss of the other
history. Complete inverse recovery remains possible.

A [separate prospective follow-up](../research/component_studies/selection_followup_protocol.json)
tested the narrower OR/NO competition at new arm lengths and a fixed positive
input, then asked whether other preloaded inputs reverse the winning pattern.
It explicitly followed inspection of training data; it does not retroactively
accept the failed all-phase or higher-cooperation criteria.

## Fresh confirmation: a usable finite competing-route block

All [200 registered follow-up runs](../research/component_studies/selection_followup_evidence_v1/result.json)
completed through the generic experiment runner. The primary OR/NO prediction
passed at arm lengths 8 and 10, board sides 129 and 161, and horizons 48 and 56.
Each isolated route was functional. Their first complete-state changes, b
responses and C events agreed at step 12 for length 8 and step 14 for length
10. In each mixed joint preparation only the OR outlet transmitted and
clicked; all 48 complete NO outlet triples remained equal to the null
baseline throughout the registered window. Swapping the arms swapped the
winning physical side. The source input for this primary result was `(a,b)=(0,1)`.

The same fixed apparatus was also tested with 12 initial source inputs,
including sign, phase and amplitude changes. Four input vectors reproduced
OR-only competition at both lengths: `(0,1)`, `(-1,0)`, `(1,1)` and `(-1,-1)`.
**No registered input reversed the winning pattern while satisfying the
isolated-functionality and both-swap requirements.** Thus this study supplies
a finite prepared competition block, not an input-controlled route switch.

All 10,400 forward transitions passed full-state inverse recording checks and
complete rewinds. The follow-up used 86.86 CPU seconds within its 90-second
budget. Every preparation used reusable `SignalSource` and `PairedArm`
components, including the arm's `length` and `gate_pairs` parameters.

For example, the confirmed length-8 preparation can be assembled from the
repository root with the current API:

```python
from research.components import (
    BoardSpec, TensorSpec, SignalSource, PairedArm, place, finalize,
)

tensor = TensorSpec.from_signs((1, 1, 1))
origin = (64, 64, 64)
prepared = finalize(BoardSpec(129, tensor=tensor), [
    place(SignalSource(a=0, b=1, tensor=tensor), at=origin, name="source"),
    place(PairedArm(direction=-1, length=8,
                    gate_pairs=((4, 0), (0, 4)), tensor=tensor),
          at=origin, name="left"),
    place(PairedArm(direction=1, length=8,
                    gate_pairs=((2, 2), (4, 0)), tensor=tensor),
          at=origin, name="right"),
])
```

`prepared.initial` is the one initial board, `prepared.engine` is the unchanged
reference executor, and `prepared.ports["left.outlet"]` contains all 48 outlet
addresses. Component names do not install behavior in the runtime. Full
experiment specifications, portable Presenter recordings and native checkpoint
traces are retained in each follow-up case directory.

## Joined route-to-receiver test: response succeeds, retention fails

The [final frozen protocol](../research/component_studies/selection_receiver_protocol.json)
placed a generic `Receiver` at each arm's eighth site, adjacent to a seven-site
`PairedArm`. Its initial remainder pair was `(4,2)`, with zero counters. This
was a **prepared waiting state**, not one written by a preceding signal. There
was only one central source; the actual route output supplied the receiver
input. Sixteen cases covered mixed arms, ties, isolated arms and source-absent
controls.

The [complete joined result](../research/component_studies/selection_receiver_evidence_v1/result.json)
shows that the winning OR route supplies `(u0,u14)=(1,-1)` at step 12, causing
an authentic first receiver C and writing the remainder pair `(0,0)`. The NO
receiver stays completely equal to its null state across all 48 channels at
every step 1–48. This holds in both spatial swaps.

The required single-click retaining component nevertheless **fails**. The
responding receiver produces 19 C-bank events, at steps `12,14,...,48`. Its
`(0,0)` remainder record first changes away at step 14. All four isolated
route-plus-receiver cases exhibit the same failure. The eight source-absent
boards remain stationary; both source-present equal-pattern cases are retained
as diagnostics.

This distinguishes an actual route-driven local response from the stronger
single-click memory requirement. First-event timing succeeds; repeated clicks
and retention fail. In the raw analysis, `event_in_declared_window` is the
combined **exactly-one-event and event-window** predicate. Its false value
does not mean the first event occurred outside the window; the recorded first
event is at step 12.

All 768 joined transitions passed exact full-state inverse capture and complete
rewinds. The final batch used 20.41 CPU seconds. The three completed studies
total 648 trajectories, 27,098 forward transitions and 121.92 CPU seconds,
within the combined 240-second ceiling. No additional search was performed
after the final bounded batch.

The next uncertainty is waveform compatibility: the route delivers repeated
inputs, while the proposed receiver requires one write followed by a quiet
retention interval. A future experiment must preregister a pulse preparation or
receiver interface that changes this behavior through initial conditions,
then retest the complete assembly. No internally computed unique-path approval,
autonomous writing of a waiting state, or higher-complexity selection law has
been established.
