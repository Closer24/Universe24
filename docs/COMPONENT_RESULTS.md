# Component research: results, limits and decisions

The component work separates three questions: whether initial preparations can
be assembled without contradiction, whether an assembled apparatus performs a
declared finite function, and whether that function supports a physical claim.
Only the first two questions are addressed by these studies.

The current evidence includes an exact guided mobile packet, earlier finite
signal/record components, and prepared route competition. The registered
higher-cooperation-score selection prediction failed. The strict waiting
receiver also failed in both completed search families. A generic assembly
interface must preserve these distinctions rather than treating every recipe
as a verified device.

## Fixed model and version identity

All component runs use one global board, 48 channels per node, six spatial
inputs per channel, integer triples `(a,b,r)` with `r` in `0..5`, reference body
actions `(0,1,3)`, and preselected signs `(+,+,+)`. Rule3 with `num=den=1` is the
sole forward operation. Every update reads one complete previous snapshot.

Preparations and source counterfactuals are fixed before execution. No runtime
injection, switch, score-based selector, click veto, path deletion or coupling
change is present in the experiment definition. All readouts inspect completed
states. A signal here means a prepared disturbance with a demonstrated causal
effect; it has not been identified as physical light.

The original evidence was captured in a local, uncommitted working tree. Run source snapshots and hashes,
complete preparations, fixed tensor fingerprints and frozen protocols identify
the executed artifacts more precisely than HEAD alone. Historical evidence is
preserved; later APIs and documents do not retrospectively change its status.

## Claim ledger

| Claim | Classification and scope | Evidence |
| --- | --- | --- |
| Generic assembly reproduces the historical component preparations and trajectories | Software regression: all 44 experiments, 1,868 complete states and 1,824 inverse transitions match; independent oracle replay also passes | [Migration report](../research/experiments/evidence/assembly_v1/compatibility/report.json), [independent baseline audit](../research/component_review/baseline_trace_audit.json) |
| A declared guided packet translates by one X site per update, including its remainder halo; its first full return is exactly L | Mathematical proof for this fixed periodic guide and preparation, every L>=5 and every nonnegative update index; finite checks at L=5,17,31 | [Proof and limitations](CONFIRMATION_BLOCK.md), [all-state independent audit](../research/component_review/packet_review.json) |
| A receiver bit toggles on two source arrivals and stays fixed between its declared events | Earlier finite computational result: 12 runs, horizon 40, three fresh distance pairs | [Signal-clock results](SIGNAL_CLOCK_RESULTS.md), [record](../research/signal_clocks/evidence/toggle_confirmation/result.json) |
| Existing receiver counters retain levels I=0,1,4 under two arrivals | Earlier phase-conditioned finite result: 8 runs, horizon 48; not an unlimited counter or physical energy | [Record](../research/signal_clocks/evidence/counter_memory/result.json) |
| Prepared O/N paths transmit/block separately and in one shared apparatus | Earlier finite result: 24 runs, all 48 outlet triples compared over steps 6..40; the controlling state is initially prepared | [Record](../research/signal_clocks/evidence/paired_blocker/result.json) |
| One arrival writes a silent pending record and a second independent arrival creates the only receiver-node click | Not established: 0 accepted cases out of 145 candidates and 580 source-control runs in two frozen families | [Waiting results and concrete counterexample](CONFIRMATION_BLOCK.md) |
| The larger calibrated C_pair score predicts the unique surviving route when isolated arrivals match | Refuted in the registered family: 10 eligible comparisons, 10 counterexamples, 0 higher-score-only successes | [Selection record](../research/component_studies/selection_evidence_v1/result.json), [independent review](../research/component_review/selection_review.json) |
| OR/NO prepared competition survives fresh lengths at source phase (0,1) | Finite prospective result: arm lengths 8 and 10, both spatial swaps, matching isolated and null controls; OR wins, the pattern with lower training C_pair | [Fresh follow-up record](../research/component_studies/selection_followup_evidence_v1/result.json), [independent review](../research/component_review/selection_followup_review.json) |
| Changing only source input reverses the unique route winner | Not observed among the 12 registered input vectors in the 200-run follow-up; no phase-only or amplitude-changing winner-flip claim | [Fresh follow-up record](../research/component_studies/selection_followup_evidence_v1/result.json) |
| An actual competing-route output activates an attached receiver | Finite joined observation: OR supplies input (+1,-1), producing a guarded receiver event and M=(0,0) at step 12; the other complete outlet stays quiet through step 48 in both swaps | [Joined result](../research/component_studies/selection_receiver_evidence_v1/result.json), [independent review](../research/component_review/joined_receiver_review.json) |
| The joined apparatus produces exactly one click and retains that confirmation record | Failed: 19 C-bearing receiver updates at 12,14,...,48; the record first changes again at step 14 | [Joined result](../research/component_studies/selection_receiver_evidence_v1/result.json) |

## What the moving packet establishes

The packet is a complete prepared state on a translation-invariant periodic
guide. Its counters and all transverse remainder patterns move together.
The proof gives `W^t(S)=T_x^t(S)` for the exact preparation. The finite check
contains six source-present/source-absent runs, 112 retained states, 106
updates and 212 individual guarded arithmetic events. The independent audit
reconstructs every preparation and checks every state, transition and event.

This is a useful mobile pattern in board coordinates. It is not a free-vacuum
wave, a perturbation-stability result or a physical speed calibration. The
periodic circuit deliberately uses wraparound; it cannot be used as no-wrap
evidence for the receiver or route studies.

A fixed unmodified guide site sees zero integrated signed input over a full
packet passage. Rule3 gives

`r_T-r_0 = 2 sum(u_t) - 6 sum(ell_t)`.

When `sum(u_t)=0`, the endpoint remainders are equal. If the endpoint counters
also return, the entire local triple is unchanged. Thus this bare packet is
not itself a quiet remainder latch. An interacting detector may alter the
actual waveform or store information in counters and other sites; no general
impossibility result for memory follows.

## Why the waiting searches failed

The first family tested 64 apparatus candidates under all four initial source
masks. The second tested 81 additional remainder-buffer preparations under the
same four masks. Both completed their frozen enumeration and full inverse
checks, with 0 accepted cases. The tested board side was 201 and horizon 40;
initial support was farther from the periodic boundary than the horizon.

In the first retained example, source 1 alone writes `M=(4,2)` at step 8 without
a receiver C event. At old step 9 its actual incoming net input is `(-2,+2)`;
step 10 therefore already produces a guarded event in receiver channel 14.
The second source is absent. This directly defeats the registered requirement
that a single source leave a quiet waiting record through the whole horizon.

All 48 receiver channels were checked. Activity at other nodes is permitted
and is not a failed local waiting condition. These negative results concern
the stated families, not every possible preparation of the model.

## Why the score prediction failed

The new primary score was fixed before calibration and joint runs:

`C_pair = support(Y_both - Y_site2 - Y_site3 + Y_base) / 480`.

The vectors contain all 48 outlet b values at steps 6..15. The score measures
two-site nonadditivity. It is not entropy, order, periodicity or a general
physical complexity measure, and it never controls an update.

The 432 recorded trajectories produce 243 joint comparisons across three
source phases. Both routes must work in isolation; unequal-score comparisons
are eligible only when their isolated first state-change, b-response and
C-bearing times match. All ten eligible comparisons contradict the stated
higher-score-only prediction. Unmatched arrival times are not used to claim
complexity preference. The independent reviewer recomputes every recorded
observation and classification and separately replays 20 complete trajectories.

The original six-site OR/NO case is concrete: both isolated arrival triples are `(10,10,10)`,
but OR, with score 0, wins over NO, with score 1/60, in both spatial swaps under
the initial phase `(0,1)`. This is useful prepared competition and a direct
counterexample to the score prediction. No candidate passed across all three
phases, so the originally gated 28-run confirmation was not executed.

The narrower fresh-length/input follow-up has its own prospective protocol.
It cannot repair the failed score prediction or reopen the earlier acceptance
gate. The earlier, separate 54-run binary-K prediction also remains failed.

## Fresh competition and input controls

The separately registered follow-up completed all 200 trajectories. It tests
the OR/NO apparatus at arm lengths 8 and 10, board sides 129 and 161, and
horizons 48 and 56. For the declared source vector `(a,b)=(0,1)`, both routes
remain functional in isolation, OR alone produces the joint output in both
spatial swaps, and the NO outlet remains equal to its full 48-channel null
baseline throughout the registered window. The finite primary prediction
passes and every full rewind succeeds.

The [independent follow-up review](../research/component_review/selection_followup_review.json)
checks all 200 recorded runs and 10,600 native/portable states, recomputes the
96 joint classifications, and separately replays 16 complete trajectories.
The training score order was kept fixed from the six-site calibration; no new
score was measured at lengths 8 and 10 or fitted to their outcomes.

Twelve source vectors were fixed before these fresh runs. They change only the
initial source counters while keeping the apparatus fixed. No qualifying
input-controlled winner reversal was found; in particular, no equal-amplitude
phase-only reversal was found. Thus this is a confirmed prepared competitive
interface within its stated domain, not a demonstrated input-controlled
switch or a restored preference for larger C_pair.

## Actual route-to-receiver trial

The final bounded trial uses one central source and attaches a receiver at
each route outlet. The receiver begins in a prepared waiting state
`M=(4,2)`, with zero counters. The actual route output must supply the input
that creates its C event; there is no additional source labeled as an
approval signal.

The frozen test has 16 source-present/source-absent, isolated, mixed and tie
preparations, length 8, side 129 and horizon 48. Each required receiver must
have exactly one C-bearing update across all 48 channels, at steps 12..15,
then retain `M=(0,0)` through step 48. The other mixed-apparatus outlet must
remain completely equal to its null control. These criteria are fixed before
the joined runs.

All 16 runs completed. The actual OR-route input is `(+1,-1)` at the receiver
on the update to step 12; it produces a genuine C event and `M=(0,0)`. The NO
receiver remains equal to its complete 48-channel source-absent state at every
step 1..48, in both spatial swaps. This establishes a finite causal connection
from the source through competing routes to a receiver.

The single-click retaining criterion nevertheless fails. Each selected OR
receiver has 19 C-bearing updates at `12,14,...,48`, with 29 individual channel
events retained. Its remainder record is already `(2,4)` at step 14 instead
of the required `(0,0)`. All four source-present isolated route/receiver cases
also have repeated ticks. All eight source-absent cases pass stationarity;
the six required source-present cases fail the complete criterion. The two
source-present tie cases remain diagnostic. Every full rewind passes.

The [independent joined audit](../research/component_review/joined_receiver_review.json)
checks all 16 trajectories, 784 complete states and 768 forward/inverse
transitions, including native/portable equality, every receiver-channel event
and the six signed input terms. The failed behavioral criterion therefore
survives independent replay; it is not merely a presentation error.

The first arrival is inside the registered timing window. An evidence field
named `event_in_declared_window` also requires there to be exactly one event;
its false value in these cases must not be read as an incorrect first-arrival
time. The failures are extra clicks and failed record retention. No window
was shortened and no later event was discarded to create a success.

## Assembly and the next decisive connection

One shared compatible tensor and consistent initial triples establish a valid
preparation. They do not prove that connected components preserve their
isolated functions. The assembly migration passes exact comparison of all 44
historical component runs and their 1,868 complete states, including C/R
readouts and recorded inputs. The independent matrix-based oracle separately
replays all 44 trajectories and 1,824 forward/inverse transitions. This
preserves those bounded historical results; it does not certify every future
composition.

The decisive remaining question is whether an **initially prepared conversion
region** can shape a moving packet or route output into a receiver input that
writes and retains a record, while preventing further receiver ticks until a
later actual apparatus signal arrives. Only initial counter/remainder data
may change; the tensor and Rule3 stay fixed. The next protocol must distinguish
one retained event from a continuing input train and track where the other
signal information remains in the full reversible state.

That test should retain the same four source controls, declared quiet interval,
all-channel receiver observation and full inverses. The balanced bare packet
does not automatically provide a remainder latch, and the successful bare
competition does not automatically provide an exclusive retaining detector.
No additional search is included in the present bounded iteration.

A separately prepared second source can test coincidence but cannot establish
that the apparatus computed route uniqueness. The completed route-to-receiver
trial starts with a prepared waiting state; it does not show an earlier signal
writing that state. Highest-complexity selection, internally computed
unique-path approval and the complete two-stage confirmation mechanism remain
unestablished.

Keep all isolated, null, tie and swapped controls; check every receiver and
outlet channel; retain the complete reversible history. A quiet outlet is not
information deletion, quantum collapse or proof of a physical time arrow.
