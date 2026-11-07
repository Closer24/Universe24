# Component research: prospective acceptance contract

This protocol separates a valid software assembly from demonstrated component
behavior. The frozen machine-readable contract is
[U24-COMPONENT-CONTRACT-v1](../research/component_studies/protocols/component_contract_v1.json).
Each study must freeze its complete ordered case manifest and source identity
before computing new outcomes. A fresh confirmation protocol must precede its
own runs. Failed earlier studies remain failed.

## Fixed model and observations

All studies use one board, 48 channels per node, six spatial inputs, the
reference body actions `(0,1,3)`, fixed signs `(+,+,+)`, and unchanged Rule3.
Sources are initial counter values. Every later state comes from the same
generic engine. No source injection, coupling change, click veto, external
selection, path deletion or state reset is allowed. The proposed broader tensor
family is not implemented or used here.

A **signal** is a declared initial disturbance with a later causal effect
against its matched source-absent run. A **C event** uses the existing guarded
arithmetic classifier. A **node tick** groups simultaneous C events across all
48 channels, while retaining each individual event. A change of the receiver
remainder pair `M=(r0,r14)` is an **R event** and need not be a C event.

Waiting means that a declared local record persists without a receiver-node
tick over a fixed interval. Other nodes can continue evolving and clicking.
Record the first differing six-term input vector, first net-input difference,
and record/tick time separately: source distance does not establish arrival.

## Study 1: a waiting record followed by confirmation

**Question:** can one arrival write a waiting record without a receiver tick,
and a second independently preloaded arrival then cause the only receiver tick?

The exploratory family has 64 candidates and four source masks per candidate:
two source geometries, two guide modes, four distance pairs and four source-phase
pairs. It uses side 201, horizon 40 and initial receiver remainder pair `(2,4)`.
The exact choices and windows are in the frozen contract.

The source-absent board must remain stationary. Either source alone must change
`M` once to `(4,2)`, retain it, and produce no C event in **any of the receiver's
48 channels** through the horizon. With both sources, the required sequence is
`(2,4) -> (4,2) -> (0,0)`: the pending record persists for at least four complete
updates, followed by exactly one receiver C-bearing update at the second record
change. No extra R or receiver C events are accepted. Input and source-removal
controls must establish both causal contributions.

This would be a two-arrival confirmation or coincidence component. The second
signal is not an externally issued approval. It also does not establish that a
path apparatus computed which route was unique; that requires another closed
composition experiment.

**Budget:** at most 180 CPU seconds, 300 wall seconds, 1,000 initial preparations
including confirmation, 64 steps per preparation and 20,000 retained channels.
If the search passes, select the first passing candidate in the frozen order
and prospectively confirm at least three fresh distance pairs with all four
source masks. If none passes, report the finite counterexamples and limits.

The first family completed with no accepted candidate. A concrete one-source
control writes the pending record at step 8 but has net input `(-2,+2)` at old
step 9 and a receiver C event at step 10. The absent second source therefore
does not prevent confirmation in that preparation. The separately registered
[buffer amendment](../research/component_studies/protocols/confirmation_buffer_amendment_v1.json)
tests 81 initial remainder buffers around the same receiver, with all four
source masks and unchanged acceptance criteria. It uses the remaining shared
computation budget. The first negative result is not reclassified.

## Study 2: competition and a declared cooperation score

**Question:** does a calibrated two-site nonadditivity score predict which
individually transmitting route produces the unique joint outlet response?

Use equal six-site arms and the nine two-site patterns formed from remainder
pairs `O=(4,0)`, `N=(2,2)` and `R=(0,4)`. Calibrate each isolated arm before joint
comparisons. The fixed calibration vector contains all 48 outlet `b` values at
steps 6 through 15. Four prescribed preparations give

`D = Y_both - Y_site2 - Y_site3 + Y_base`,

and the primary score is the exact fraction

`C_pair = number of nonzero coordinates of D / 480`.

The two perturbations and their locations are fixed in the contract. This score
measures the extent of two-site nonadditivity; it is neither entropy, order,
periodicity nor a general physical complexity measure. The engine never reads
it. The earlier 54-run binary-K prediction remains failed.

Every proposed competing route must transmit and produce a guarded outlet tick
in isolation. Joint tests retain all 81 ordered pattern pairs, matching nulls,
isolated controls, ties and left/right swaps. The fixed joint window is steps
6 through 40. A unique winner must have an outlet C event; the losing outlet
must equal its matching no-source baseline in **all 48 complete triples at
every sample** in that window. Counter-only silence is insufficient.

Arrival timing is a competing explanation. Record each isolated outlet's first
complete-state difference, first `b` response and first C-bearing update. The
primary score prediction applies only to unequal-score pairs with matched
arrival triples and the same initial source phase, amplitude and arm length.
Unmatched pairs remain visible as prepared competition, not evidence that
complexity caused selection. No eligible comparisons means an inconclusive
test, not a pass. Any eligible counterexample rejects the stated finite-family
prediction, even if some useful individual competitive component succeeds.

**Budget:** at most 240 CPU seconds, 600 wall seconds, 1,000 initial preparations
including confirmation, 64 steps and 20,000 retained channels. A selected
competitive component needs a separately frozen fresh-geometry/phase test.
Calibrations, score order and readout windows must not be changed after viewing
joint outcomes.

The registered 432-run search completed. All ten matched-arrival, unequal-score
eligible comparisons contradicted the higher-score-only prediction. The
prediction is refuted in this family. No candidate passed across all three
registered phases, so the original fresh-confirmation gate remains closed.

The separately registered
[phase-conditioned follow-up](../research/component_studies/protocols/selection_phase_amendment_v1.json)
selects the `OR/NO` competitive apparatus. Its isolated arrival times match,
yet `OR` wins with score `0` against `NO` with score `1/60`. This remains a
counterexample. Fresh lengths and twelve specified source vectors test whether
the narrower competitive component persists or changes its output with the
input. A phase-only claim requires equal source `a²+b²`; a change across
amplitudes is described as input-controlled. No broader score law is restored.

## Ancillary guided-packet check

A separate registered packet construction tests exact whole-state translation
along a fully prepared periodic guide, with all transverse remainder state
retained. It compares source-present and source-absent preparations at sides
5, 17 and 31, each for one complete circuit. This deliberately uses periodic
wrapping, so the no-wrap condition for the receiver and route studies does not
apply to this different question. It cannot supply their causal-isolation
evidence. The [packet protocol](../research/component_studies/confirmation_packet_protocol.json)
uses at most ten additional CPU seconds within the shared confirmation budget.
Its scope is a prepared guided mobile packet, not free-vacuum light or an
already assembled waiting-confirmation device.

## Verification, evidence and decisions

Retain complete preparations, source and protocol hashes, fixed coupling,
board size, step horizon, all outcomes and stop reasons. Check exact one-step
inverses and a complete rewind, including off-axis effects and every remainder.
Archive the full-state trajectory of every completed registered run, including
failed candidates and calibration controls; do not filter evidence by result.
Require an initial nonbackground boundary margin greater than the horizon.
Resource exhaustion is inconclusive. The generic Presenter must display the
recorded states and unchanged readouts; it supplies no scientific acceptance.

The preparation-library migration has a separate regression gate: reproduce all
44 historical component trajectories and their 1,868 complete states exactly.
Tensor compatibility and nonconflicting initial assignments make an assembly
valid; they do not make its intended behavior true.

Positive results apply only to the stated finite preparations and observation
windows. A silent outlet does not erase the full reversible history. Neither
study alone establishes physical light, an irreversible microscopic clock,
quantum collapse or a universal preference for complex paths.
