# Quantum origin cells in event spacetime

The explicit `local-quantum-events-v3` candidate adds a lifecycle for configured quantum waves
to the ordinary `Simulation`. History remains in the existing immutable event
spacetime. It adds no linked history per Node or wave and no second simulator.
The [quantum-state contract](QUANTUM_EVENTS.md) still supplies exact joint state,
phases, conditional records and bounded deferred evaluation.

## Local state and ownership

| Part | Contract |
| --- | --- |
| Origin | An immutable source-associated event ID identifying one configured wave continuation |
| Local Node | At most six distinct integer origin references, plus bounded current-event/consumption markers |
| Current register | A separate current event head and modeled operation tick; there are at most thirty configured virtual registers globally |
| History | Immutable source, operation, channel and result events with dependency edges in the shared event spacetime |
| Resolution | A write-once event-space status linking a closed origin to its successful terminal result |
| Quantum state | Joint amplitudes or density state and operation payloads owned by the existing quantum backend |

Six is an explicit capacity of this candidate. Six directional Ports do not
mathematically limit all possible fields, register degrees of freedom or arrivals
over time to six. A seventh distinct local origin fails before a partial update;
no wave is silently overwritten or discarded to fit the bank. Different virtual
registers at one physical address share the same six-origin Node bank.

An origin reference marks possible causal support. Origin count is not disturbance
count: one origin may describe a joint state with several disturbances. A claimed
collision still needs an explicit state, coupling and instrument; counting origin
names cannot establish that two physical disturbances met. A reference is not a sampled particle,
a local occupation value or a probability. A zero-amplitude branch may still
carry a reference. Knowing an origin ID does not reconstruct phase or correlation;
those remain in the shared exact quantum state and event dependencies.

## Propagation and local interactions

Initialization names origins at configured source registers and supplies the
existing one- or two-register local operations. Every v3 layer operation declares
one to six participating `origins`. It executes only while all those origins
remain active and have reached at least one of its old endpoint banks. Unarrived
support cannot execute the gate. Suppressing a resolved-origin gate additionally
requires certification that its operation would leave the complete retained
correlated density unchanged. Otherwise the layer fails before publication.
A certified skip adds an audit check but no quantum operation payload, amplitude
change or register-ready-time update. The world tick still advances. Untagged gates are rejected
in the wave profile rather than providing an escape from terminal status.

An eligible operation carries relevant causal-support references to its local outputs.
The whole simultaneous layer reads the preceding banks, so two disjoint gates
cannot relay a new origin through two Links in one tick. The native Link timing
checks still apply. Reference propagation describes causal support; the configured
matrix determines actual quantum evolution and interference.

A wave interaction explicitly names one to six distinct locally available
origins and a complete local instrument. One origin can represent a joint state;
this list is not a particle count. Initial source support is eligible on
the first native tick; afterward, a fresh configured local operation or channel
event is required.
Persistent co-residence without a new event does not repeatedly sample the same
encounter. Coherent operations alone do not request a lottery.
The finite implementation retains a one-register instrument; a general
multi-register collision instrument is outside this extension.

The instrument defines all outcomes, including no-click or no-transfer. The
configuration selects which outcomes terminate which participating origins;
outcomes not selected for termination retain the conditional continuation.
Names are labels and never select a physical species law.

## Initialization and recorded output

Select `event_program.model: "local-quantum-events-v3"`. The finite v2 register,
layer, channel and instrument definitions remain available. Additional data are:

| Member | Definition |
| --- | --- |
| `waves` | Definitions with distinct `name` and a source `register_index`; an ordinary register, including vacuum, is not automatically a wave |
| Each layer operation's `origins` | One to six participating wave names; every v3 operation requires this field, including channels |
| `wave_interactions` | At most one configured interaction per physical `address`, with its local `register_index` |
| `origins` | One to six distinct wave names required locally; these identify continuations, not a count of physical disturbances |
| `instrument` or `grouped_instrument` | Exactly one complete one-register instrument; grouped terms preserve indistinguishable alternatives |
| `terminal_outcomes` | Outcome indices that end selected origins; defaults to the empty list |
| `terminal_origins` | A subset of the required origin names; defaults to all required origins when terminal outcomes are declared, otherwise empty |
| `null_outcome` | Optional outcome index defining physical no-event; required to certify suppression of a retired-origin instrument |

The existing simulated `seed` or explicit `tickets` supply sampling. Certain
outcomes consume no ticket. A continued origin remains available for a later
fresh encounter using the updated conditional state.

V3 rejects the older carrier `bindings` interface until it has an explicit
origin-aware contract. It must not provide a route for a retired wave to sample
or control another classical cycle. V1/v2 carrier bindings retain their existing
candidate semantics. Direct wave-backend steps require an `origin_groups` tuple
matching the operations; instrument preparation and interaction require their
participating origin IDs.

The runnable input [wave_origins.json](../examples/quantum/wave_origins.json)
defines a signal and a probe on three Nodes. Configured splitting and a SWAP
bring them into a tick-2 interaction. Outcome 1 explicitly resets occupation
`|1>` to `|0>` and resolves the signal; outcome 0 is the declared null. The next
tick prunes peer references, and the probe remains active. A continuing position
instrument is a separate configuration. The explicit matrices
and source preparation are test data, not derived particle or detector laws.

`NodeView.event_origins` exposes an immutable local ID snapshot. The resolver's
`wave_origins` report pairs each `origin_event` with its `resolution_event`, and
`node_wave_origins` reports each Node's `address`, `origins`, `event_id` and
`consumed_id`. These are audit data, never a source of ordinary physical inputs.

## One result and local invalidation

The quantum owner serializes relevance validation, probability preparation,
ticket selection, conditional record commit and terminal origin marking in one
event-space transaction. The first successful terminal result closes its selected
origins exactly once. A later contender checks that status before sampling and
cannot commit a second terminal result for the same origin. A nonterminal result
updates the conditional joint state; the next contender must use that updated
state rather than weights computed before it.

The origin's historical address, tick, parents and source data remain immutable.
The resolution points to a later result event at its actual occurrence time and
location. Closing a source-associated continuation does not rewrite the past.

Committing a result does not traverse or update the other Nodes' banks. Each
participating Node checks its own at-most-six references on every native tick and
discards resolved ones locally. A status recheck at interaction prevents another
result in the same tick before that local pruning happens. Retired references
are not subsequently propagated as live continuations. Later gates requiring
them are suppressed only after the full-density invariance check above.

An instrument for a retired origin may be suppressed only when its declared
`null_outcome` is the sole possible outcome and that branch preserves the complete
retained correlated density. Missing null definitions, any other possible outcome
or a state-changing null branch reject the request. Returning `None` means that
declared physical no-event result; it is not an arbitrary erased measurement.
An origin flag alone cannot authorize removing an operation or instrument that
would change observable quantum behavior.

The native resolver caches this certificate for the immutable binding/address
and current target register head. It rechecks after that head changes, even when
the Node's arrival marker has not changed. Certification evaluates existing joint
state under Q-ORACLE-1; it does not add a second history or mutate the physical past.

Gate and result ledger events reference their participating origin IDs. These
are event-spacetime provenance; they are not added to quantum recipe parents as
if an origin bookkeeping record were another amplitude source.

The shared status is internal quantum-owner bookkeeping under Q-ORACLE-1. It is
not a freely readable classical signal for a distant Node, field rule or observer.
Finite checks of this implementation do not establish a general no-signalling
theorem. Ordinary physical inputs still require their configured causal delivery.

## Continuation, uncertainty and conservation

A position record does not assign a simultaneous sharp momentum. This extension
adds no physical momentum observable or propagation law. A continuing outcome
keeps the selected joint quantum state. Terminal status ends eligibility of that
named origin; it does not create an invented classical momentum or remove the
exact record needed to condition other degrees of freedom. Ending its future
gates does not by itself model particle absorption: actual removal needs an
instrument that supplies the corresponding state reset and any declared
exchanges. A later physical preparation needs explicit model rules; arbitrary
dynamic creation of origin generations is not supplied.

Interference still depends on complex phase and coherent joint alternatives.
A returning environment must remain in the joint coherent model. Independent
unconditioned lotteries followed by a first-writer flag generally produce the
wrong outcome statistics; atomicity alone cannot repair them.

The origin lifecycle adds no force, momentum, energy or universal collapse law.
Any claimed conserved quantity requires its declared local operator or mechanical
balance and an independent test. Passing a status or probability test alone does
not establish conservation for unspecified interactions or a classical limit.

## Cost, limits and migration

Direct event-ID/status access and checking a six-entry local bank require bounded
local work independent of the number of stored past events. The whole tick over
many Nodes, lock contention, dependency evaluation and joint-state storage remain
separate host costs. Q-ORACLE-1 assigns one model operation to a successful query;
it does not claim that Python tensor evaluation is O(1).

The native `wave_control_cost` reports priced origin-bank inspections and
successful oracle requests, including cancellation certification. Audit events
`wave-skip-check` and `wave-null-check` each carry one model operation; the
`host_cancellation_checks` counter and successful-query totals report their host
evaluation separately. Certification is not O(1), and its bounded state/term
budgets still apply. Only the direct origin-status lookup has the local O(1) claim.

With an event ledger selected, `computation_report.model_operations_cost` equals
the complete ledger cost. `carrier_model_operations_cost` retains the ordinary
carrier-cycle subtotal; `wave_control_cost` is already included in the total and
must not be added again. V3 audit checks and their costs do not provide physical
observer signals or new carrier delays. This profile rejects carrier bindings
and parallel Node planning; it does not derive a propagation-delay or momentum
law. Host evaluation and RNG statistics remain separate.

This is the existing finite register candidate with explicitly configured gates
and instruments. Native event programs still reject parallel Node planning and
independent spatial-field clocks. The event and quantum budgets remain finite
and fail explicitly; an unlimited universe in bounded total memory is not claimed.
Origin resolution does not garbage-collect the immutable spacetime audit.

The separate `EventPredecessor` records and `history(register)` API have been
removed. Read immutable events directly or use diagnostic dependency traversal;
current register cursors remain for state and Link readiness. Exact checkpoints
preserve the complete live correlated state, origin identity and each register's
modeled time while retiring only replaceable quantum payloads.

`examples/quantum/event_paths.json` replaces `linked_paths.json`, and
`tests/test_quantum_node_events.py` replaces `test_quantum_linked_nodes.py`.
The same four-Node interference, intermediate record, correlated checkpoint and
physical timing cases are retained. Origin-specific expectations are listed in
[TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md), with native integration in
`tests/test_native_wave_origins.py` and guarded cancellation checks in
`tests/test_native_wave_cancellation.py`. Runs remain headless by default.
