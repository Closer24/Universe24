# Signal-triggered record and waiting protocol

The next question is whether two separately prepared incoming disturbances can
write two successive local records, with a silent interval between them, in the
unchanged Universe24 reference model. This is a stronger requirement than a
signal starting a local period-four counter motion. A signal-started oscillator
can continue after its input sum becomes zero and cannot, by that fact alone,
establish that a later record came from a second incoming signal.

The frozen protocol is
[`U24-SIGNAL-CLOCK-WAIT-v2`](../research/signal_clocks/protocol.json). It is saved
before the candidate search in this session. This provides a reviewable order
of decisions, not an externally timestamped registration. The complete search
family, its training and held-out preparations, source locations, receiver
addresses and arrival windows must also be saved before execution. Numerical
outcomes must never determine the event definition or a shorter observation
window after the fact. The earlier v1 draft is retained as
[`protocol_v1.json`](../research/signal_clocks/protocol_v1.json); no candidate
was run under it. Version 2 incorporates the user's subsequent clarification
that the full milestone needs the existing arithmetic click guard, not only a
remainder write.

## What the building block must do

Two source disturbances are present in the initial state. They may reach the
receiver at different times because their prepared routes have different
lengths. There is no insertion of a pulse during the run, no click-triggered
reset, no changing tensor, and no external choice of the next trajectory.
Only Rule3 evolves the complete board after initialization.

The detector is an ordered pair of channel addresses fixed before its run.
Its memory symbol is the exact pair of retained remainders:

\[
M(t)=(r_A(t),r_B(t)),\qquad
R(t)=\mathbf 1[M(t)\ne M(t-1)]\quad(t\ge1).
\]

Every change is counted. An observer cannot ignore an unwanted intermediate
change, wait until a convenient phase, or gate the event by an input threshold.
The initial symbol is a preparation and is not a click. The proposed device
passes only if it produces exactly two changes over the full registered
horizon, leaving three pairwise distinct symbols: the initial symbol and one
record after each arrival.

Here **remainder-record event** is a new name for a passive measurement of a
stored state. It does not replace the existing arithmetic C0/C1/C2 classifier.
Those arithmetic events additionally require a nonzero quotient and a changed
local triple. A remainder write with quotient zero is an R event under this
protocol but is not an existing arithmetic C event. Both classifications may
be reported separately without changing either update or observation semantics.

The full milestone additionally requires exactly two **C-bearing updates** in
the detector pair, coincident with the two R events. A C-bearing update means
at least one channel has an existing arithmetic C event. If both channels have
an event in that update, both individual events remain listed; grouping their
common update into one bank tick does not erase either event. The observed
index `N(t)` counts these bank ticks as an external history functional. It is
not a newly added state variable. The internal memory remains the two original
remainders.

An R-only candidate can support a narrower memory-write result but does not
pass the full signal-clock milestone. Each single-source control must also
have exactly one C-bearing update coincident with its sole R event. No extra
detector C or R event may occur anywhere in the horizon.

The two records must each persist for at least four sampled states, and the
two events must be separated by at least five updates. At least four sampled
states precede the first event, and at least four further updates remain after
the second. The training horizon is 32 updates; successful candidates face a
40-update confirmation horizon. The exact boundary conventions are retained
in the protocol and must be applied identically to every run.

Waiting means the record is unchanged and no arithmetic C event occurs. The
detector's two net input sums must additionally be zero over the specified
minimal quiet updates; zero input is not imposed on every other update in the
horizon. Before the first event at `t1`, the four sampled states
`t1-4,...,t1-1` precede the event, and zero input is checked at old-state indices
`t1-4,...,t1-2`; the arrival uses old state `t1-1` and is excluded.
The post-event zero-input ranges are `t1,...,t1+3` and `t2,...,t2+3`.
Counter phase cycling is allowed
and must be visible in The Presenter. Consequently this is **quiet record
waiting**, not a claim that the microscopic receiver is completely motionless.
Complete local rest is a separate diagnostic. For example, zero input changes
the pair of counters as `(a,b) -> (b,-a)` while preserving the remainder.

## Demonstrating an arrival rather than naming an edge

For each detector channel, retain all six signed previous-neighbor `b` terms
and their exact sum `u`. An accepted record event needs nonzero net input in
the update that produces it. That input vector must differ when the source
assigned to that arrival is removed. Arrival windows are defined from each
candidate's initial source geometry before running, not from the observed
memory edges.

Every preparation is run with four source conditions:

| Initial sources | Required record behavior over the complete horizon |
|---|---|
| Neither source | Entire board remains stationary; no record event |
| Source 1 only | Exactly one R and one coincident C-bearing update in the first window |
| Source 2 only | Exactly one R and one coincident C-bearing update in the second window |
| Both sources | Exactly two R and coincident C-bearing updates, one in each window, with quiet retained records |

Removing a source means setting only its initially nonzero counters to zero.
The apparatus, all initial remainders, tensor, detector and observations remain
identical. Thus a second edge generated by the first source's own reflection
does not qualify as the second arrival. Nor may a source-only control be
silently discarded because it produces an inconvenient later event.

The existing prepared guide is a useful starting point but does not already
meet this stronger criterion. In its N24 run the j6 record first appears at
step 6, resets at 44 and appears again at 56 under one originally prepared
source. Those are real finite trajectory observations, not evidence for two
independent incoming signals. The earlier transverse-control example also
produced only a one-sample target record where four were required. Both
limitations remain part of the evidence; see
[the prior component study](COMPONENT_STUDY.md).

The initial search is an explicitly engineered family: a straight x guide
from -40 through 40, background remainder 2, tensor signs `+++`, receiver
channels 0 and 14 at its center, and source distances `(6,14)` or `(8,16)`.
Sources are either on opposing sides or on the same negative-x side. Each
source uses one of four unit-amplitude counter phases; the receiver uses one
of all nine even remainder pairs. This makes 576 candidates, with fixed arrival
windows `[d1,d1+1]` and `[d2,d2+1]`. The exact enumeration is in the JSON
protocol. Search may stop at the first full success or its resource limit;
unevaluated candidates are never called failures. Board side 181 leaves an
initial boundary margin of 50, greater than the 32-update search horizon.
Reserved distance pairs `(10,18)` and `(12,20)` are not training cases.

## Stored state and later routing

The two-arrival record is the first milestone. A written-memory router is a
separate, stronger claim and cannot be inferred merely because a remainder
changed or an output predicate switched value.

For a routing test, declare two disjoint output regions and a response window
before execution. For each of two memory preparations, compare the same probe
with a probe-absent control. Measure the exact difference of their output
counters `delta_a, delta_b` at every sample. Their absolute-value sum is a
counter-influence statistic, not derived physical energy. A clean routing
result requires nonzero probe influence only in output A for one memory and
only in output B for the other, under an identical fixed coupling.

A change in a readout threshold without changed transmitted counter influence
is not routing. A one-output transmission difference is a weaker transfer
result. Manually setting two different remainder preparations can test such
state dependence, but it is not yet an autonomously written-memory router.
For the latter claim, both preparations must be generated by the declared
earlier incoming source histories in the same model.

All off-output state remains retained and invertible. A quiet output therefore
does not mean that its hypothetical path history has been erased. No quantum
collapse or Born-rule conclusion follows from exclusivity in a finite prepared
trajectory.

## Cooperation is a testable hypothesis, not an instruction to the model

A separate follow-up can compare matched paths using a declared pairwise
response measure. Fix `m` distinct internal channel addresses, a calibration probe, and an exact
output vector `Y` containing all 48 `b` counters at every declared outlet node
over a fixed window. Report whether the chosen addresses belong to distinct
spatial nodes; channel non-additivity alone does not establish spatial cooperation.
Run the unperturbed preparation and parity-preserving initial remainder flips
`r -> (r+2) mod 6` at address `i`, at address `j`, and at both. Define `K` as the
fraction of pairs `i<j` for which `Yij - Yi - Yj + Y0` is nonzero.

This is a bounded measure of pairwise non-additive counter response. It is not
entropy, order, periodicity, or a general definition of physical complexity.
All flips are preparation changes before separate runs. `K` is never supplied
to Rule3 as a preference, gate or selection command.

Before a routing test, match path length, declared node count, initial counter
L1 norm, probe and output windows. Fix calibration probes, held-out probes,
monitored sites and a preference threshold before collecting their outcomes.
Include mirrored geometry and swapped branch labels. The unproved prediction
is that an independently measured higher-K branch transmits a held-out probe
while the lower-K branch is suppressed. Ties and contrary outcomes must be
reported. The first 576-case receiver search does not test or establish this
path-preference claim, and the later metric cannot retroactively accept a
failed receiver.

The executable follow-up is separately frozen as
[`U24-COOPERATION-PATH-v2`](../research/signal_clocks/complexity_protocol.json).
It uses equal six-node arms on both sides of one source, three declared
remainder variants, and two varied channel addresses per arm. Twenty-four
calibration runs measure the six direction-specific K scores using all 48
outlet counters at steps 6 through 9. Twelve joint held-out probe runs,
twelve isolated-arm runs, and six no-source controls continue through step 15.
Their selection window is steps 10 through 15, not the earlier calibration
window. The total is 54 runs and 666 forward updates before inverse audits.

This separation follows a causal check made before execution: a memory change
at arm index 2 cannot change a counter before its source arrival at step 2,
and then needs eight more spatial links to reach the opposite outlet. Its
earliest cross-arm effect is step 10. The corresponding index-3 bound is
step 12. An early-window comparison alone could test prepared transfer but
could not establish competition caused by these changed memory locations.
The unexecuted earlier 42-run draft remains available for provenance; it is
not counted as an experiment.

The stronger cancellation claim requires a low-K outlet that responds in its
matching isolated-arm run but is quiet in the joint run over the same late
window. In addition, an actual update must have nonzero opposing signed input
terms summing to zero, a resting old outlet counter pair, and a corresponding
isolated update with nonzero net input and nonzero next counter. This separates
input cancellation from the different arithmetic possibility `ell - a = 0`.
If these extra conditions fail, report only the measured finite-window
suppression. The arms are prepared corridors; transverse routes and the entire
off-corridor state remain in the experiment, even if the display emphasizes
the two named outlets.

## A separate endpoint preparation follow-up

The first frozen 576-case family completed with no accepted receiver. Its
retained representative exposes extra events from one source before the
second source's registered window. Unused armed guide tails behind a source
are a candidate feedback mechanism. Removing such initially prepared tails
changes the apparatus preparation, not Rule3 or the tensor.

The separately frozen
[`U24-SIGNAL-CLOCK-ENDPOINT-v1`](../research/signal_clocks/endpoint_protocol.json)
therefore places opposing sources at distances `(12,20)` or `(14,22)` and arms
only the segment between them. It searches the same nine receiver remainder
pairs and sixteen source-phase combinations: 288 candidates. It preserves
every C/R acceptance condition, source control and waiting convention from
the original protocol. It does not relax a failed criterion after seeing it.
The new search and any conditional confirmation share a 180 CPU-second budget.

For the `(12,20)` geometry, a front that goes from either source to the
opposite endpoint and returns to the receiver needs at least 52 or 44 updates.
That particular end-return mechanism cannot explain an event in the 32-update
search window. This does not exclude local reflections, transverse feedback,
or interactions of the two fronts; those remain measurable failure modes.
The reserved endpoint distance pairs are `(16,24)` and `(18,26)` for the
40-update confirmation horizon. Results from this new family will be reported
separately from the original 576 failures.

## Confirmation, budget and reporting

The search permits at most 300 CPU seconds, 600 wall seconds, 10,000 declared
preparations and 20,000 stored channels in one state. Confirmation has its own
300 CPU/600 wall-second budget. A resource stop is inconclusive and must retain
the completed cases and precise stop reason.

After a nominal training pass, test at least two source-distance pairs reserved
before search, repeat on a board with side increased by 20, and extend the
horizon to 40. Exact translated complete-state comparisons distinguish a size
effect from mere display agreement. Report four source-amplitude perturbations
separately: add +1 or -1 to the leading `b` counter of either source, without
compensating edits. Their failures constrain robustness; they do not justify
changing the registered nominal acceptance rule.

Every retained trajectory needs exact one-step inverse tests and a complete
rewind. Initial nonbackground support must be farther from the periodic
boundary than the horizon, or a separate exact causal argument must exclude
wrap influence. Observing no active boundary at sampled times alone is not
such a causal argument.

Record code and protocol hashes, complete inputs, tensor, deterministic seed
or enumeration, side, horizon, every event, unwanted events, input terms,
inverse checks and all control outcomes. Export the retained trajectories
through the unchanged generic Presenter. The clock hand still depicts the
counter pair; the gear still depicts the exact retained remainder. Displaying
these quantities creates no additional dynamics.

Until independent propagation, interaction and physical measurement tests are
met, the appropriate term is **signal-triggered clock or record**. This study
does not establish physical light, optical power, physical time calibration,
an irreversible microscopic time direction, matter or a quantum detector.
An ordered record sequence can be inspected in a forward-prepared experiment
while the full board remains reversible; that alone does not derive a universal
arrow of time.

There is a further predictive distinction. During zero-input waiting the
counter pair can rotate through four phases while `M` and the observed tick
index stay fixed. The next response contains `b_next = ell - a`, so identical
next input and remainder can produce different counter outputs at different
hidden phases. A monotone counted-event index therefore does not by itself
give a closed event-to-event law or prove that arbitrary waiting durations are
physically indistinguishable. The present held-out source-distance pairs both
retain gap eight. A later preregistered delay sweep must vary that gap while
controlling the incoming waveform before making a delay-independent clock
claim; no such result is assumed by this protocol.

Any failed criterion will be stated beside the strongest surviving narrower
result. A finite unsuccessful search is not an impossibility proof. A proposed
structural model change must be documented as a separate candidate for Alon
Gonen's decision and will not be implemented under this protocol.
