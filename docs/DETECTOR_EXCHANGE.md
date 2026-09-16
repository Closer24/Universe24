# Detector exchange contract

## Status and authority

This definition draft records user-specified behavior and explicitly open decisions.
It is not an implemented model, a validated quantum law or authorization to implement,
run an experiment or merge. The external Detector is outside the ordinary board;
the board evolves its configured signals, phases and splits deterministically.
Detector influences enter only through its defined causal interface.

The latest action-bit decision supersedes both the earlier reflect/absorb model
and the earlier zero-draw PASS encounter. The Detector samples an **action bit**
to select PASS or GENERATE_RETURN. PASS does not sample the forwarded **content**
again; it can still follow an action draw. No 50/50 probability is implied.
Any 0/1 operation labels are encoding conventions, not physical outcome values.

Every Detector has the same capabilities and rules. Identity does not establish
an Alice/Bob priority. Other paths remain present; no Detector event restores an
earlier state, deletes global paths or changes remote state before causal delivery.

## Signal and provenance

Separate the semantic signal from its transport envelope:

```text
Signal = (payload, value_origin, bounded_provenance)
Delivery = (Signal, incoming_port, local_arrival_event)
```

`value_origin` is SPACE or DETECTOR: the origin of the value, not the last
forwarding component. PASS preserves the payload and original value provenance
exactly. Passing a SPACE signal through a Detector does not relabel it DETECTOR.
Transport metadata may change under an explicit forwarding rule.

Recipient-required provenance travels in bounded fields; generating-event,
setting and exchange identifiers require defined semantics. No global origin
lookup, remote current-state read or reconstructed trajectory supplies an input.
Payloads contain bounded data and identifiers, never formulas. Immutable laws
and distribution definitions are separate from evolving state.

## Operations and distinct draws

| Incoming origin | Selected operation | Content behavior | Local consequence |
| --- | --- | --- | --- |
| SPACE | PASS | Forward exactly the received semantic signal; no content sample | Record transmission if enabled |
| SPACE | GENERATE_RETURN | Generate a fresh value with DETECTOR provenance and emit through the incoming Port | Record generation; do not adopt the original incoming value |
| DETECTOR | PASS | Forward exactly the received signal and generation provenance; no content sample | Adopt that generated value under LOCK without resampling it |
| DETECTOR | GENERATE_RETURN | OPEN: admission after receiving or locking a generated value | Repeat-generation and exchange policy must be defined |

Action sampling is external Detector logic, not an ordinary Node/Register rule.
The action-bit distribution, dependence on causally available input/settings and
lock-dependent eligibility remain OPEN. Do not use a deterministic selector as
the accepted replacement for the user's action-bit decision.

GENERATION and action selection are different responsibilities. A return sends
a fresh generated value, not a copy, sign reversal or physical mirror transform
of the input. It can coincidentally equal the incoming value. The return-value
domain and distribution, relation to the action bit, phase and any additional
random draws remain OPEN. The action bit is not automatically the returned
payload or its phase. No default distribution may be supplied to close this gap.

A possible exact sampling interface uses bounded nonnegative integer weights,
positive bounded total weight and cumulative integer intervals. This is only
an interface proposal, not an accepted law or a selected distribution. Degenerate
distributions and random-ticket consumption require an explicit convention
consistent with the existing certain-outcome contract.

LOCK means adopting a received Detector-generated value without content
resampling. It does not establish permanent shutdown, absorption, global wave
resolution or definiteness of every observable. Duration, setting conversion,
replacement, repeat encounters and simultaneous conflicts remain OPEN.

## Spatial return and time

GENERATION returns through `outgoing_port = incoming_port`: the first hop points
backward **in space**, while model time always advances. No prior Node state or
event is restored, and there is no multi-hop return shortcut. Later encounters
with a source, Detector or previously visited location follow causal transport
and the still-open encounter policies.

The latest user intent also requires RETURN to claim/cancel the selected branch
back to the Node of its previous interaction. This is branch-local cancellation,
not deletion of unrelated branches. A proposed causal realization carries a
cancellation notice backward along that branch in space and forward in time,
one Link per allowed transit; it does not erase already committed events,
instantaneously clear a path, remove topology or permanently close Ports.
The precise endpoint, bounded branch identity/ownership, effect on future packets
and competing notices remain OPEN. This proposal is not an implemented transport
law and does not permit unbounded histories or a global branch registry in a Node.

Distinguish model time in integer multiples of `delta_t_min`, Detector time with
an explicitly defined mapping, and host recording time used only for diagnostics.
The Detector clock and bounded processing/transport delays remain OPEN. Follow
[minimum model time](REFERENCE_UNITS.md#minimum-model-time-and-output-delay):
waiting is distinct from Link transit, and whether generic k includes transit
remains unresolved. Do not add a tick unconditionally. An emitted signal cannot
cross a Link before its allowed transit or cascade across several Links in one
elementary step because of host callback order.

## State, ownership and readout

Detector state is fixed-capacity local data: configuration identifiers, bounded
lock/transaction information and owned inputs/outputs. Exact layouts and capacities
are architecture decisions; no growing per-ray history becomes physical state.
External placement grants no instantaneous access to the board or another Detector.

Receipt, action selection, generation, LOCK and committed transmission are distinct
events. A Recorder preserves passive evidence; a Renderer presents it. Neither
supplies the physical rule. Which event constitutes the reported measurement,
and how an output value maps to a physical observable, remain OPEN.

Use the [stored-code contract](ARCHITECTURE.md#stored-codes-and-mathematical-values)
and [remainder ownership](ARCHITECTURE.md#lossless-remainder-ownership). Signed
values, phases and ratios require explicit exact encodings. Bounds, pending output
ownership and failure behavior must be defined before publication; capacity
exhaustion is an error, not a different physical outcome. Whether all intermediate
values must also be nonnegative remains OPEN. Do not truncate, clamp or drop a
remainder. Sampling/commit retry semantics must prevent accidental extra draws.

Generating a value does not establish physical energy, momentum or charge of the
emitted signal. Any such claim needs explicit local or external source accounting.

## Open decisions before execution

| Decision | Required closure |
| --- | --- |
| Action bit | Distribution, causal inputs/settings, eligible encounters and random-ticket semantics |
| Return content | Value domain/distribution, relation to action bit, phase and number of content draws |
| Forwarding | Deterministic outgoing-Port mapping for PASS |
| LOCK | Meaning across settings, duration, replacement and repeat-generation eligibility |
| Exchange | Bounded identity/lifetime, replay and periodic-return rules |
| Branch cancellation | Exact prior-interaction endpoint, bounded branch identity, causal notice semantics and treatment of future packets/conflicts |
| Competing generations | Collision/simultaneous handling without privileged Detector identity |
| Readout and output | Reported-result trigger, destination behavior, payload/phase ownership and source accounting |
| Time and transactions | Detector/model clock mapping, processing/Link delays, capacities and retry/commit behavior |

## Prospective acceptance checks

Fix the missing parameters and independent expected results before execution:

- Action sampling occurs only in the external Detector under the declared law.
- A PASS result preserves payload/provenance and draws no additional content;
  its preceding action draw is separately recorded.
- Admitted GENERATE_RETURN follows its declared content law, does not adopt the
  original value and returns through the incoming Port with forward causal timing.
- Passing a Detector-generated value adopts it without content resampling.
- Swapping Detector identities preserves the common rule.
- Other paths remain, with no remote state change before causal arrival.
- Branch cancellation affects only its declared branch and endpoint under the
  agreed causal notice rule; committed history and spatial topology remain intact.
- Duplicate calls, simultaneous choices and periodic re-encounters follow the
  declared transaction/exchange policy without accidental extra generation.
- All pending outputs, bounds and remainders retain valid ownership.

Quantum acceptance also requires a specified quantum-state transformation and
independent interference/correlation predictions. Matching an inserted probability
table establishes that configured mechanism, not emergence of the table. A value
communicated between Detectors before their results are fixed is communication-
assisted coordination; two Detectors alone do not establish entanglement or a
solution to a Bell experiment with causally separated outcomes.

## Existing implementation boundary

The physics reviewer inspected main
`e5b5911ab13373e08345cf971a6ae8d7e9cb462e`. Existing null/absorption and
continue/localized/new_wave profiles do not implement this exchange contract.
Do not run or relabel them as a PASS/GENERATE_RETURN demonstration. This draft
does not alter those named profiles, their evidence or executable behavior.
Implementation readiness remains blocked by the open decisions above.
