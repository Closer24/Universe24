# Signal-clock building blocks: results and decisions

The current reference model now has three finite, reproducible component
results: an arrival-triggered two-symbol toggle, a phase-conditioned
three-level counter-magnitude record, and prepared open/block paths that work
both separately and together. Exact quiet preparations and a complete
period-four motion with no arithmetic clicks supply controls. The original
remainder-only three-symbol milestone and the tested higher-cooperation-score
preference failed and remain failed. These results do not yet compose into an
autonomously written-memory router or establish physical light.

All runs use unchanged Rule3, fixed body-action coupling, 48 channels per node,
six spatial neighbors, and one complete previous snapshot per update. Only
initial preparations differ. There is no runtime signal insertion, state reset,
gate, path deletion or click-controlled update.

## Open the generic Presenter

Open [Signal_Clocks.html](../research/signal_clocks/evidence/interfaces_presenter_final/Signal_Clocks.html)
locally. This self-contained file contains all 44 prospective component and
control experiments: twelve toggle runs, eight counter-memory runs and
twenty-four paired-transfer runs. It uses the existing generic Presenter;
there is no experiment-specific animation or alternative update engine.

Choose an experiment, press **Play**, or move the recorded-frame slider. Drag
the cube to rotate it and scroll to zoom. The view-options menu includes
**Focus retained state** for a readable view of the prepared apparatus.
**Look inside** opens all 48 channels at the selected node; exact values and
the six-input update remain available through the optional evidence panel.

| Example to select | Useful recorded steps | What to inspect |
|---|---|---|
| **Counter memory 20 / 28: both sources** | 19, 20, 29, 30, 48 | Detector `(110,110,110)`, channels 0 and 14; two authentic updates and retained counter levels |
| **Counter memory 20 / 28: first source only** | 20 through 48 | Same detector after only source 1; no second event |
| **Toggle 16/26: both signals** | 16, 28, 40 | Fresh changed-gap toggle at detector `(100,100,100)` |
| **Prepared transfer: open left, neutral right; source on** | 6 through 40 | Left outlet `(44,50,50)` responds; right outlet `(56,50,50)` stays equal to its no-source state |
| **Prepared transfer: neutral left, open right; source on** | 6 through 40 | The prepared open/blocked sides exchange roles |

The clock hand shows counter direction, normalized for drawing; its length
does not measure I or physical energy. The six-position gear shows the actual
remainder. Exact counter values establish I when inspected. A rotating hand
can continue between detector clicks without advancing that detector's
counted-event index.

The separate [research and negative-result replay](../research/signal_clocks/evidence/presenter_final/Signal_Clocks.html)
retains 64 earlier experiments and controls, including the complete K study.
Adjacent `experiments.json` files can also be loaded with **Open experiment**.
The two files respect the unchanged per-bundle size limits; no experiment is
silently discarded to make one file appear successful.

The current published [counter-memory closeup animation](../research/experiments/evidence/publication_v1/render/sequence-01/recorded-clocks.gif)
and [whole-cube animation](../research/experiments/evidence/publication_v1/whole_cube_render/sequence-01/recorded-clocks.gif)
show the same 49 saved states of the four-component, both-source preparation.
The toggle and paired-transfer cases remain available in the 44-case HTML
above; these two animations do not represent those other experiments.

Actual application scripts and native canvas drawing were exercised locally.
The attempted Chromium launch failed before page load with SIGTRAP. Therefore
browser CSS layout, mobile rendering and real-browser pointer interaction
remain unverified; native-canvas captures are not browser screenshots. The
scientific full-state checks and this remaining rendering limitation are
reported separately.

## What is established mathematically

Any board with all counters zero is fixed for arbitrary valid remainder
values: every net input is zero and `divmod(r,6)=(0,r)`. This supplies an exact
source-absent apparatus condition. It does not mean that arbitrary nonzero
preparations need physical light to move.

There is also a complete-board no-click motion. Put one channel at
`(a,b,r)=(0,1,2)` in a `(0,0,2)` background. The source counter rotates with
period four. Its six face-neighbor recipients retain a remainder halo while
their counters remain zero. If a recipient's input sign is `w`, its
three-position remainder follows `1,1+w,1+w,1,1`. These values never require
a carry. Thus every quotient is zero, no existing arithmetic C event occurs
anywhere, and the complete state including the halo returns after four updates.
The construction applies to each source channel and existing sign tensor on
the allowed periodic cube. It is a preloaded recurrence and a no-tick control,
not an arrival-triggered device or physical light.

For a local pair subjected to prescribed net inputs, initial remainders `(4,2)`
and two paired arrivals `(+1,-1)` can give `(4,2) -> (0,0) -> (2,4)`, with an
authentic first-channel arithmetic event on the first arrival and a
second-channel event on the second. Zero-input intervals can separate them.
This is an exact local input-response construction. Realizing those inputs in
an autonomous complete board is the additional task the searches test.

See [the algebra and finite checks](SIGNAL_CLOCK_ALGEBRA.md). Reversibility
retains all microscopic information; a zero visible output or a returned local
bit does not erase the source history.

## Registered receiver searches

The fixed readout is the exact detector remainder pair `M=(r0,r14)`. Every
change is an R event. Authentic arithmetic C events retain their existing
nonzero-quotient and changed-triple guard. A C-bearing update groups the two
detector channels by their common update index while retaining every
individual channel event.

The full milestone requires exactly two coincident R/C-bearing updates, three
distinct retained memory symbols, fixed arrival windows, silent waiting,
source-absent and single-source controls, and exact complete-state inversion.
These criteria were fixed before either search. The second family changes
initial geometry and does not weaken the criterion.

| Frozen family | Candidates completed | Accepted full devices | R-only passes | Audited trajectories | Forward updates |
|---|---:|---:|---:|---:|---:|
| Long armed guide, sources inside the guide | 576 | 0 | 0 | 900 | 28,800 |
| Guide only between endpoint sources | 288 | 0 | 0 | 450 | 14,400 |

The first search used approximately 65.12 CPU seconds; the endpoint follow-up
used 18.30. Both completed their entire declared enumeration. All sampled
forward steps passed their exact inverse checks and complete rewinds. These
finite negative results are not an impossibility proof for all preparations.
Conditional held-out tests for the original three-symbol milestone were not
triggered; none may be described as passed.

The first retained long-guide case makes the failure concrete. With source 1
alone, its detector R events already occur at 6, 8, 10 and 12 before source 2's
registered window 14–15. Genuine C-bearing updates occur at 6, 10 and 12.
Thus the later events cannot all be attributed to the absent second source.
Unused armed tails are one possible feedback source, but removing them is not
a general cure: endpoint preparations still show local remainder feedback.

Evidence: [long-guide results](../research/signal_clocks/evidence/training/search_results.json),
[endpoint results](../research/signal_clocks/evidence/endpoints/search_results.json),
and [frozen criteria and interpretations](SIGNAL_CLOCK_PROTOCOL.md).

## A narrower two-symbol toggle candidate

The endpoint search contains a useful bounded observation that remains a
failure of its original acceptance rule. Case `endpoint-064` has source offsets
`(-12,+20)`, unit source phases `(0,1)`, target remainders `(4,0)`, and a
32-update horizon.

| Sources present | Detector R/C-bearing update times | Internal memory |
|---|---|---|
| Neither | None | `(4,0)` throughout; complete board stationary |
| Source 1 only | 12 | `(4,0) -> (0,4)` |
| Source 2 only | 20 | `(4,0) -> (0,4)` |
| Both | 12, 22 | `(4,0) -> (0,4) -> (4,0)` |

There are no other detector R/C events through step 32. The registered quiet
input intervals, full inverses and source-counterfactual input comparisons
pass. However, the final bit equals its initial value, and the second event is
outside the registered 20–21 window. It therefore supplies neither the required
three distinct local records nor a passed original milestone.

The timing is not evidence that the second signal arrived locally at 20 and
waited inside the detector for two updates. The both-source detector and its
six input terms still agree with source-1-only through old step 20. Their first
local input difference is at old step 21, immediately before the event at 22.
The source-2-only run would produce its event at 20. The interaction therefore
changes the observed arrival history; a separate detector latency has not been
derived from these traces.

The fresh [toggle confirmation protocol](../research/signal_clocks/toggle_protocol.json)
tests a genuinely different interface: an alternating memory bit, not a local
history counter. It uses fresh distance pairs `(16,24)`, `(16,28)` and
`(16,26)`, four source controls for each, a 40-update horizon and a larger board.
The first two cases vary the waiting gap by four; the third tests a different
counter phase. Their exact predicted times `d1,d2+2` are explicitly a
preregistered empirical hypothesis, not a timing theorem.

All twelve runs and all three case groups passed their fixed predictions.
There were 480 forward updates, each with exact inverse verification and a
complete rewind, within approximately 1.04 CPU seconds.

| Fresh source distances | Both-source C/R-bearing times | Source-1-only | Source-2-only | First second-source local input difference |
|---|---|---|---|---|
| 16, 24 | 16, 26 | 16 | 24 | Old state 25 |
| 16, 28 | 16, 30 | 16 | 28 | Old state 29 |
| 16, 26 | 16, 28 | 16 | 26 | Old state 27 |

In every group the no-source board stayed exactly stationary, the two-source
memory followed `(4,0) -> (0,4) -> (4,0)`, and no further detector C/R event
occurred through step 40. All declared waiting and source-counterfactual checks
passed, including the prospectively chosen gap-10 phase challenge. The second
event follows the first locally detectable second-source input difference by
one update. The earlier source-2-only arrival time is a counterfactual, not an
observed early local arrival in the combined run.

The result field `phase_independent_extension_passed` refers only to that one
registered gap-10 extension of the two nominal gaps. It does not establish
independence from all source phases or all waiting gaps, and it makes no claim
about phase-independent counter-magnitude memory.

This establishes a prepared finite two-arrival toggle interface on these three
fresh cases. It does not establish arbitrary delay invariance, indefinite
reuse, or a local count of past events. The original three-symbol milestone
remains failed. Evidence is retained in the
[fresh confirmation result](../research/signal_clocks/evidence/toggle_confirmation/result.json)
and all twelve complete trajectories.

The quiet intervals concern this detector pair's observed clock. Other nodes
can have arithmetic events while a signal propagates. The separate period-four
control above is the result with no arithmetic clicks anywhere on the board;
these two scopes must not be confused.

## A fresh three-level record in the existing counters

After the exploratory toggle was inspected, its counter magnitude
`I=a*a+b*b` suggested a different local record. This observation was not used
to retroactively accept any earlier remainder-only experiment. The new
[counter-memory protocol](../research/signal_clocks/counter_memory_protocol.json)
was frozen before eight new runs at distance pairs `(20,28)` and `(20,32)`.
They use side 221, horizon 48, four source controls per geometry, the same
endpoint guide, and unit source phases `(0,1)`.

All eight runs passed. Each detector channel independently keeps the following
exact magnitude levels:

| Sources | Distance pair | C/R-bearing updates | Retained I sequence in each channel |
|---|---|---|---|
| Neither | Both geometries | None | `0` through 48 |
| Source 1 only | Both geometries | 20 | `0 -> 1` |
| Source 2 only | 20, 28 | 28 | `0 -> 1` |
| Source 2 only | 20, 32 | 32 | `0 -> 1` |
| Both | 20, 28 | 20, 30 | `0 -> 1 -> 4` |
| Both | 20, 32 | 20, 34 | `0 -> 1 -> 4` |

Each level is constant over its complete registered interval, with no extra
detector R, C or magnitude changes through step 48. Both-source records retain
their final level for 19 or 15 sampled states, respectively, including the
event state. All 384 forward updates pass exact full-state inverses and
complete rewinds. The first second-source local input differences are old
steps 29 and 33, immediately before the corresponding records.

The identity `I_next - I = ell*ell - 2*a*ell` explains both the quiet retention
and its limits. Zero input preserves I while the counters can rotate. At an
arrival, the old phase matters: the same input can increase or decrease I.
Thus I is not physical energy, a general conserved quantity, or an unlimited
monotone click counter. The result is restricted to the declared even-gap
preparations and two arrivals. The internal record is the existing tuple
`(r0,r14,I0,I14)`; no new state variable was added.

Evidence: [counter-memory result](../research/signal_clocks/evidence/counter_memory/result.json)
and all eight complete trajectories. The older remainder-only milestone stays
failed: this is a separately defined and prospectively confirmed observable.

## The tested cooperation preference failed

The separately frozen path study defines K as pairwise non-additivity of the
exact all-channel outlet response to two initial remainder perturbations.
Here there is only one pair of perturbed addresses, so K is either zero or
one. It is neither entropy nor a general measure of physical complexity.
The score never enters the update rule.

All 54 registered runs completed, with 666 audited forward updates, stationary
no-source controls and complete inverse checks. Calibration gives the same
scores in the two tested directions:

| Initial channel-0 remainder at the two selected sites | K |
|---|---:|
| 0 | 0 |
| 2 | 1 |
| 4 | 1 |

Of twelve held-out comparisons, eight have unequal scores and four are ties.
**All eight unequal-score comparisons transmit to both outlets.** None meets
the higher-K-only prediction, none suppresses the lower-K outlet relative to
its isolated-arm control, and none has the registered strong cancellation
witness. The four ties make no directional prediction and are not counted as
successes or directional failures.

A direct counterexample is `joint-0-2-P1`: the left branch has K=0 and the right
has K=1, yet both outlets have the same nonzero channel-14 samples, `b=-2` at
step 10 and `b=1` at step 12. Their late-window absolute counter sums are both
3, exactly as in their isolated-arm controls. The statistic is not physical
energy. The fixed all-48-channel readout matters: the study varied channel-0
memory while the channel-14 signal partner continued through both outlets.
Looking only at a convenient channel would hide that retained transmission.

These observations refute the precise finite preference prediction for this
K, these preparations and these held-out probes. They do not prove that every
possible cooperative measure or state-dependent router is impossible.
Evidence: [complete path results](../research/signal_clocks/evidence/cooperation/result.json)
and [the fixed path protocol](../research/signal_clocks/complexity_protocol.json).

## Prepared open and blocked paths

The next transfer experiment addresses the observed partner-channel leakage
by preparing both channel remainders, without modifying the failed K metric or
its results. Its [paired-transfer protocol](../research/signal_clocks/paired_blocker_protocol.json)
was frozen before the runs.

The board has side 101, background `(0,0,2)`, a centered unit source pair,
and two six-node x-directed arms. Ordinary arm sites have remainder pair
`(4,0)`. At indices 2 and 3 in each arm, set both remainders to one of the
declared pairs: open O=`(4,0)`, neutral N=`(2,2)`, or reverse control R=`(0,4)`.
All apparatus counters start at zero. Each outlet is the entire node at arm
index 6, including all 48 complete channel triples.

All 24 runs completed: nine ordered joint preparations with a source, nine
matching no-source controls, and six isolated-arm cases. The observation
window is every sampled state from step 6 through step 40. All 960 forward
updates pass their full-state inverse and rewind audits. Initial support is
44 links from the boundary, exceeding the 40-update horizon.

| Prepared interface | Required observation | Result in the fixed window |
|---|---|---|
| Isolated O, either direction | At least one nonzero outlet b response | Pass |
| Isolated N, either direction | All 48 outlet `(a,b,r)` triples equal the no-source baseline | Pass; no leak |
| O left, N right | Left transmits; right remains completely equal to its no-source baseline | Pass |
| N left, O right | Right transmits; left remains completely equal to its no-source baseline | Pass |
| Every joint no-source control | Complete board stationary | Pass |

This is stronger than showing a zero selected counter: the blocked outlet's
remainders and other channels also remain unchanged throughout the entire
registered window. It is nevertheless finite-window blocking, not proof that
the outlet will remain quiet forever or under arbitrary probes.

Six reverse-control comparisons have an outlet active in isolation but quiet
in a joint preparation. None supplies the additional registered signed-input
cancellation witness. Report those as counterfactual suppression, not proven
input cancellation, deletion of a path, or quantum collapse. The nominal
neutral blocker is already quiet in isolation and is not cancellation by a
competing signal.

The O/N state is prepared initially. No previous signal has yet been shown to
write this path choice and then route the next independent signal in the same
closed run. Therefore the result is a **prepared state-dependent transfer
interface**, not an autonomously written-memory router. Full off-axis state
is retained and invertible. Evidence is in the
[paired-transfer result](../research/signal_clocks/evidence/paired_blocker/result.json)
and all 24 complete trajectories.

The retained history has explicit locations. At step 40 in both O/N and N/O,
the blocked outlet's 48 triples equal its no-source control, yet **40 channel
addresses elsewhere in the full state differ**. At the source `(50,50,50)`,
channel 0 is `(0,-1,2)` and channel 14 is `(0,1,2)`, versus `(0,0,2)` in the
controls. At the first site toward the blocked arm, channel 0 is `(-1,0,0)`
instead of `(0,0,4)`: position `(51,50,50)` for O/N and `(49,50,50)` for N/O.
These exact witnesses and trace hashes are retained in the
[independent information-retention check](../research/signal_clocks/independent_information_retention.json).
The quiet outlet therefore does not identify the complete histories or erase
their distinguishing information.

## Interpretation and next decisive questions

The observations support a useful separation. A board can evolve through many
updates with no arithmetic clicks. A local record can be started by a prepared
signal. A bit toggles twice on fresh controlled preparations, and existing
counters retain three exact magnitude levels in a separate confirmation.
Prepared open/block paths also compose in one shared two-arm apparatus.
These are concrete finite interfaces, but none establishes physical light,
quantum selection, or an irreversible microscopic time.

The fresh toggle preparations reproduced their fixed timing and waiting
interface, including the deliberately changed phase gap. An alternating bit
still needs a third independently prepared input and a composition test before
claiming an indefinitely reusable clock. Counter phase is part of the full
state and may matter for other gaps and later clicks.

The decisive next composition test is to use a first, entirely preloaded
incoming source to write a neutral path's controlling remainder pair, then let
a second independently preloaded probe encounter that changed apparatus.
Compare neither source, writer only, probe only and both, keeping exact
all-channel outlet windows and an unchanged observer. The written state must
persist during a declared quiet interval, and the later probe must produce
different transmitted influence because of that stored state. Simultaneous
residual waves from the writer must be distinguished from retained-memory
control. No such joined write-then-route result is claimed here.

Before general reuse, the positive transfer interface also needs new arm
lengths, longer observation horizons, declared perturbations and an actual
clock-memory connection. The confirmed I record needs a third independent
input and a composition test. These next tests can use initial-condition
searches within the same model; no runtime selector or structural change has
been justified.

No structural model change is established as necessary by these finite results.
If a future exact obstruction requires one, it must be proposed as a separate
candidate rather than silently inserted into the reference model.
