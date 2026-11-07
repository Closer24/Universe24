# Independent review of signal-triggered clocks

This review concerns a closed Universe24 board under the existing reference
Rule3. A signal-triggered record is not yet a physical light clock. The
presentation must retain that distinction even when it draws clocks and gears.

## Review conditions fixed before measured acceptance

The complete initial state must contain every source, receiver and memory.
Subsequent forward states must be produced solely by `Engine.advance` with
the same coupling. A source injected at a later step, a write performed by an
observer, or a changed coupling invalidates the construction.

The event predicate must be declared before the acceptance run. An initial
true predicate is not an observed event. A subsequent change in a receiver's
remainder may be a passive memory-write event, but it must not be silently
equated with the existing arithmetic C0/C1/C2 classification. That classifier
retains its nonzero-quotient and changed-triple guard.

The final frozen protocol is `U24-SIGNAL-CLOCK-WAIT-v2`, SHA-256
`24468f3f984b77340722c0f99e27e24eb6317e6c32ccddb36adc4bdd509e54ec`.
It requires exactly two distinct detector update times carrying genuine C
events, coincident with the two remainder-record changes. Every individual
channel event is retained. A successful weaker remainder-only test must not
be reported as satisfying this full milestone. Protocol v1 remains retained
as a pre-execution draft with no accepted runs.

The following controls are required for a two-arrival interpretation; each
single-source control must contain exactly one remainder change and exactly
one genuine-C-bearing detector update in its assigned arrival window:

- No source: the detector apparatus is silent throughout the declared horizon.
- First source only: the initial response occurs, followed by the declared
  silent waiting window without a second accepted event.
- Second source only: the late source has a separately measurable response.
- Both preprepared sources: the late response is causally attributable to the
  second source by comparison with the first-source-only control.
- Memory counterfactual: an identical later probe encounters preparations
  differing only in the declared memory state. A routing claim requires changed
  transmitted counter signals at fixed output ports; changing a label or hiding
  a path in the viewer is insufficient.

Exact causal attributions require care in this nonlinear automaton. Subtracting
the states of two runs does not decompose a combined run into independent
particles. Controls instead establish a specified intervention at preparation
time and its measured consequences.

## Algebraic checks that constrain the search

Write `r = 2 theta + epsilon`, where `theta` is 0, 1 or 2 and `epsilon` is 0 or 1.
Direct division of `2u+r` gives

```text
theta_next = (theta + u) mod 3
epsilon_next = epsilon
ell = floor((theta + u) / 3)
a_next = b
b_next = ell - a
```

Thus remainder parity is invariant. With zero net input, `ell=0`, the remainder
is unchanged and `(a,b)` maps to `(b,-a)`. Four applications return the pair.
Since this map is a bijection fixing the origin, a nonzero pair cannot become
the resting pair `(0,0)` during a strictly zero-input interval. Calling the
existing activated period-four guide a clock that stops until the next arrival
would therefore be incorrect.

A resting channel can instead retain a changed remainder without continuing
counter motion. For unit positive input, phases 0 and 1 advance without a carry;
phase 2 advances with a carry and activates a counter. This is a forced-input
truth table. It becomes a component demonstration only after those inputs are
realized in a complete closed-board trajectory.

The old prepared guide is also a negative control for an overly weak event
definition: one initial source produces a reset and later new memory edges.
Two observed edges alone do not prove that two independently prepared signals
have operated the receiver.

## Exact constraints on a complexity or time-arrow interpretation

Let `F` be the complete deterministic update and let `X_0,...,X_(p-1)` be a
complete-state orbit of period `p`. If a scalar state readout `K` satisfies
`K(F(X)) >= K(X)` at every point of that orbit, every inequality is equality:
summing the increments gives `K(X_p)-K(X_0)=0`. Consequently no strict increase
can occur on the cycle. The existing complete-state recurrent preparations
exclude a universal strictly increasing state function on all preparations.
This does not exclude a finite sequence of directed records in a specially
prepared experiment or a statistical statement with separately specified
conditions.

Likewise, for any finite-support probability ensemble with probabilities
`p(X)`, a bijective complete-state update merely relabels its states. Its
Shannon entropy `-sum_X p(X) log p(X)` is therefore unchanged exactly. A
many-to-one observation can hide distinctions and its observed entropy can
change. Neither observation establishes a preference for a particular
structural-complexity measure. A proposed complexity metric needs its own
definition and predictions; order, period, amplitude and entropy are not
interchangeable substitutes.

A path that becomes invisible in one output must be audited in the full
state. If two different preparations evolved to exactly the same complete
state under the same tensor, applying the inverse would make their initial
states identical, a contradiction. Apparent cancellation is compatible with
reversibility only while the distinction survives elsewhere in the complete
registers or correlations. This argument does not identify where it survives
in a particular run; that requires an explicit state comparison.

## Evidence requirements and limits

Independent review must recompute full sparse states, including off-axis and
remainder-only changes, with a separate gather construction from exact matrix
couplings. Full inverse checks cannot be restricted to visible clock channels.
Source hashes, preparation, fixed tensor, board side, horizon, protocol bytes,
resource budget and negative outcomes must be retained.

The detector's complete sampled interval must cover every claimed retention or
waiting endpoint. A short run cannot certify an unsampled interval. Boundary
independence requires a declared causal margin or a larger-board comparison;
absence of a visible crossing in a selected channel is insufficient.

Finite searches and finite perturbation tests do not establish universal
impossibility or a broad basin of spontaneous formation. Counterfactual routing,
if found, would be state-dependent classical information processing in this
model; it would not alone establish quantum path selection or collapse. The
inverse retains the complete microscopic information even when a chosen
readout is silent.

## Current verification state

The initial review found an off-by-one first-arrival condition and a boundary
test based only on observed support. The code owner corrected both before
search acceptance: four initial sampled states permit a first event at step
4, and the initial support must have margin strictly greater than the declared
horizon. A third regression rejects an incomplete trace whose declared horizon
extends beyond its final sample.

Nine independent review tests currently pass. They include 48 full-state
forward comparisons from all four source masks against a separate exact-matrix
gather oracle, one-step inverse checks and complete rewinds, as well as the
initial-source-only intervention check and observer-contract regressions.
Synthetic observer traces used by those regression tests are explicitly not
closed-board constructions.

The single-unit-source control additionally has an independent routing
certificate over all 48 channels, all eight sign triples and sides 3 and 5:
768 preparations and 3,072 full-state steps agree with the exact-matrix port
construction, each inverse succeeds and no guarded arithmetic event occurs
anywhere. This finite certificate supports the separately proved all-side
period-four identity. It does not supply the missing arrival-triggered device
by calling internal rotation a click.

Math 1's phase/parity, zero-input exact-period-four, immediate-rest obstruction,
fixed-point obstruction, finite-invariant-set complexity, central-channel
pairing and counter-magnitude balance proofs were independently checked and
have the stated scope. Their prescribed scalar arrivals remain truth tables,
not a spatial experiment. The actual closed-board results below are separately
audited.

## Audited results

The original waiting protocol failed for all 576 full-segment preparations
and all 288 separately registered endpoint preparations. Recomputing every
saved detector recurrence and every criterion decision agrees with those
negative classifications. The search's complete unique trajectories were
engine-audited; only the selected full traces were retained. Independent
matrix-based replay of retained states must not be described as a second
full-state simulation of every unstored search trajectory.

The endpoint search contained a narrower, useful exploratory observation:
endpoint-064 has actual detector R/C bank events at 12 and 22, with remainder
memory `(4,0) -> (0,4) -> (4,0)`. Its no-source control is stationary; either
source alone produces one event, at 12 or 20 respectively. All four complete
traces pass independent replay and inversion. The original test still fails:
the second event is outside its fixed window and the final remainder symbol
does not distinguish the two-event history from the initial symbol.

A new, prospectively specified two-symbol protocol then succeeds on all
12 fresh control runs. The both-source events are 16/26, 16/30 and 16/28 for
source distances 16/24, 16/28 and 16/26. Every record change and guarded event
through step 40 is retained. All 480 full-state transitions agree with the
independent matrix gather, including every detector input term, and rewind
exactly. The second source first changes local input terms at old steps
25, 29 and 27, with the corresponding clicks at 26, 30 and 28. The terms at
the naive geometric arrival are identical to the first-source-only control.
Consequently this is not evidence of a two-step local detector latency after
an already observed arrival.

The exact observable `I=a*a+b*b` supplies another distinction. Its identity
`I_next-I=ell*ell-2*a*ell` follows by expansion of Rule3, and makes it invariant
during zero-input waiting. The exploratory endpoint trajectory has levels
0, 1 and 4; this observation did not retroactively satisfy the old criterion.
The fresh gap-10 toggle instead has levels 0, 1 and 0, exposing phase dependence.
A separate prospective magnitude-memory protocol subsequently passes all
eight fresh controls at distances 20/28 and 20/32: the registered local levels
0, 1 and 4 persist through step 48, with events 20/30 and 20/34. All 384
transitions are independently verified. This is a finite phase-conditioned
memory component, not an arbitrary-phase or indefinitely reusable counter.

The original cooperation hypothesis fails in its declared family: independent
replay of all 54 cases (666 transitions) reproduces every calibration vector
and score. In both orientations, K is 0 for variant 0 and 1 for variants 2
and 4. All eight unequal-score held-out comparisons transmit at both outlets;
four are score ties. There is no strict high-K-only selection and no qualifying
signed-input cancellation witness. This refutes the fixed finite prediction,
not every conceivable complexity metric or state-dependent router.

A separately prepared paired-channel blocker has a positive bounded result.
All 24 complete traces (960 transitions) pass independent matrix replay.
The O arm transmits in isolation; the N arm's full 48-channel outlet state
matches its source-absent control at every sampled step 6 through 40. Joint
O/N and N/O preparations retain that open/blocked behavior in both orientations.
All comparisons include both counters and the remainder, not only the visible
channel. Six R-arm comparisons are active in isolation but quiet jointly;
none has the registered simultaneous signed-input cancellation witness.
They are finite suppression observations, not established interference
cancellation. These are preloaded memory states, not yet a router whose
memory is autonomously written by an earlier signal.

The source history remains explicitly visible outside the blocked outlet.
At step 40, each O/N and N/O source-present board differs from its source-absent
control at 40 complete channel addresses. The origin's channel 0 is
`(0,-1,2)` rather than `(0,0,2)` and channel 14 is `(0,1,2)` rather than
`(0,0,2)`, although all 48 triples at the blocked outlet agree. These are
read-only comparisons of already audited traces; they locate surviving
information and do not add a new acceptance criterion. The exact witnesses
and trace hashes are retained in
[the information-retention audit](../research/signal_clocks/independent_information_retention.json).

The independent machine-readable audits retain the exact native-trace hashes:

- [Primary traces](../research/signal_clocks/independent_trace_audit.json)
- [All primary detector criteria](../research/signal_clocks/independent_training_criteria.json)
- [Endpoint negatives](../research/signal_clocks/independent_endpoint_negative_audit.json)
- [Cooperation and endpoint criteria](../research/signal_clocks/independent_followup_audit.json)
- [Exploratory toggle](../research/signal_clocks/independent_toggle_audit.json)
- [Fresh toggle confirmation](../research/signal_clocks/independent_toggle_confirmation_audit.json)
- [Counter memory and paired blockers](../research/signal_clocks/independent_components_audit.json)
- [Displayed period controls](../research/signal_clocks/independent_period_audit.json)

These results establish finite, prepared computational building blocks under
unchanged Rule3. Physical light, a quantum path-selection law, an autonomous
irreversible time direction, general robustness and arbitrary composition
remain unproved. Final integration verification separately binds the
source and protocol identities, test results, standalone Presenter files and
their actual rendering evidence.

## Final integration verification

The final Python suite completed once after the scientific implementation and
tests were frozen: **94 tests passed**, exit code 0, in 111.454 reported seconds
(111.667 wall seconds), within its 600-second ceiling. No second full-suite run
was needed. The independent trace audits cover **112 complete trajectories,
3,018 states and 2,906 transitions**, including all retained counterfactual
controls. Their exact trace bytes still match their audit records.

All 13 reference engine files match the audited `ed1556e...` source manifest
and the local checkout's HEAD. The upstream commit tree itself is unavailable
locally, so this is a comparison with the retained audited pin, not a new remote
fetch or upstream-blob verification. The model, tensor semantics and existing
C classifier were not changed. Work remains local on
`research/signal-clocks-2026-11-07`; no commit, push, pull request or merge was
performed for this work.

The [current 44-case Presenter](../research/signal_clocks/evidence/interfaces_presenter_final/Signal_Clocks.html)
contains all 1,868 recorded states for the fresh component confirmations.
The [64-case evidence Presenter](../research/signal_clocks/evidence/presenter_final/Signal_Clocks.html)
retains the exploratory toggle, negative controls, cooperation study and
period-four controls. Every final experiment identifies both the originally
registered protocol bytes and its serialized copy; the two representations
were independently checked for equal JSON content. All embedded state data,
input hashes and unchanged generic UI sources match their manifests.

Actual-app rendering was checked with jsdom and native Canvas2D. The 64-case
run passed. The first 44-case run completed every case and readout check, then
failed its aggregate GIF encoding wall budget; that failed report is retained.
A subsequent animation capture supplied valid frame images, but independent
review found a zero-byte GIF at one original output path despite its recorded
hash. That output is excluded. Four replacement, content-addressed delivery
files were independently hashed, decoded frame by frame and hashed again
after all encoding writers exited: 41, 49, 41 and 41 frames, all 800 by 450
pixels with 250 ms frame durations. The incident and recovery are retained in
the verification evidence. Presentation-only text corrections were checked
to leave all states, coupling, readouts, view settings and UI code unchanged.

Chromium failed before page load. Consequently real-browser layout,
responsive behavior, accessibility and native pointer interactions remain
unvalidated; Canvas checks are not a substitute for that scope. The exact
test logs, source and artifact hashes, scoped rendering evidence, preserved
failures and decoded GIF paths are recorded in
[verification.json](../research/signal_clocks/verification.json).
