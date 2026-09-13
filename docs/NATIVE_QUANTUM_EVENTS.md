# Native event programs and charged classical paths

## Contract and ownership

The primary `Simulation(initial)` and the ordinary `event-universe --init ...`
runner now compose an optional event program. It is not a second world, special
contact runner, or fixed-address fixture. Without `event_program`, existing
physical behavior and operation prices remain unchanged.

`core/event_space.py` owns one bounded namespace of immutable event identities,
time, local support, typed causal edges, owner and payload references. It contains
no quantum matrix or particle law. Carrier sources, cycle starts/commits, sends,
receipts, local requests and quantum operations/records use the same namespace.
`NetworkEvent` remains a compatibility view; its time/parents/identity come from
the shared store and its amplitudes/matrices come from the quantum payload owner.
There are not two competing authoritative copies of that metadata.

The core `EventResolver` protocol receives only a local immutable context and
the existing local planner. `integration/event_runtime.py` composes the selected
quantum owner with that protocol. Generic core and field modules do not import
quantum. Initialization resolves arbitrary type/field labels to indices. Cells,
packets and pending cycles acquire only one optional event ID each; they never
hold a growing history or a wave vector. Global counters and the bounded ledger
are host bookkeeping, not a nonlocal input to local physics.

Dependencies must refer to existing, nonfuture event IDs. Physical parent edges
additionally require the same cell or a completed nearest-neighbor link, including
configured periodic seams. Dependency-only edges confer no physical read access.
Global numbering is bookkeeping, not a preferred physical signal. Coherent quantum
operations preserve the existing disjoint local-layer contract; the native binder
also checks actual parent times against the world's fixed link transit.

## Finite quantum-register extension

The explicit [v2 register/channel contract](QUANTUM_ENTITIES.md) adds dimensions,
initial levels, colocated named registers, unobserved channels and grouped
measurement outcomes. It uses this same resolver and preserves path cost rules.

## Initialization

For the on/off choice, a copyable JSON member, UI steps, capacity and output
files, start with [event graph configuration](EVENT_GRAPH_CONFIGURATION.md).
The graph can be enabled without quantum rules.

`event_program` is a JSON object stored as one immutable bounded configuration
string in `InitialState`. Its contents are validated during initialization and
again when composed. It never stores executable code or callbacks in cells.

Choose `model: "causal-events-v1"` and a positive `capacity` for a classical-only
causal ledger. Choose `model: "local-quantum-events-v1"` to additionally supply:

- `addresses` (1-30 distinct in-domain sites), optional `occupied` site indices,
  optional quantum `bounds`, and strictly increasing `layers`. Each layer names
  a tick and disjoint one/two-site `operations` with exact integer `matrix` data.
  A complex coefficient is `[real, imag]`; a real coefficient may be one integer.
- `bindings` (at most one per address). Each names one or two local `types`, an
  owned nonconserved/nonextensive scalar `field`, one `code` per outcome via
  `codes`, and a complete one-cell `instrument`. A duplicate type selects two
  distinct records. The first matching distinct slots are used; this is not an
  all-pairs collision search. Other locally present records are unchanged.
- A simulated RNG `seed`, or a bounded `tickets` stream for reproducible tests.
  Certain outcomes consume no ticket. A nondeterministic exhausted or invalid
  ticket stream fails instead of returning a fabricated no-event result.

Examples are [native_classical.json](../examples/quantum/native_classical.json),
[native_quantum.json](../examples/quantum/native_quantum.json),
[native_reflection.json](../examples/quantum/native_reflection.json), and
[native_cost_delay.json](../examples/quantum/native_cost_delay.json).
Matrices and instruments are explicit candidate data, not derived physical laws.

## Local trigger, retained history and classical output

A binding requests a calculation when its participants are co-resident and new
records have arrived since the last local cycle, or are initially present at tick
zero. A held pair is not measured again every tick. A later encounter gets a new
request ID. Waiting preserves the proposal and the chosen result; it does not
repeat the query or resample the past.

Before sampling, all mechanical alternatives are evaluated with the existing
`DisturbanceLaw` and validated. The shared request references the local physical
cause. `prepare` reconstructs required quantum dependencies and computes all
weights; `commit` appends the selected conditional record. Only its outcome code
is supplied to the selected local mechanical proposal. A quantum-conditioned
marginal is never freely exposed as remote classical information. The engine owns
normal delay, conservation checks, commit and outgoing packets; each subsequent
receipt references the actual send. Query computation adds no world ticks.

This is the declared measured-control candidate. A returning coherent environment
still needs joint amplitudes, not a premature classical choice. The classical
bodies in these examples are controlled by a quantum degree of freedom; they are
not yet the position eigenstates of one derived quantum matter field.

## Cost is charged for the executed path

Each begun physical cycle pays the existing local law's cost **once**, including
routing, sends, updates, interactions and its configured receive costs. The new
resolver charges one `read` price for inspecting a bound cycle; a triggered
instrument additionally costs **one oracle model operation** and one `update`
price per locally written outcome code. The chosen mechanical branch pays its
own law's cost. There is no `quantum_off` path that silently bypasses this work.

The same existing timing rule applies to the complete cost C: for budget B and
fixed link transit tau, local waiting is `(ceil(C/B)-1)*tau` when C exceeds B.
Link transit itself remains tau. Waiting ticks do not charge C again. Pending
proposals keep their original record until the normal commit. Accumulated run
cost is a diagnostic total, **not debt** that delays later cycles.

`computation.model_operations_cost` sums begun cycles, including still-pending
ones. The ledger charges that cost only on `cycle_started`, never again on
`cycle_committed` or `sent`. Quantum records carry zero additional ledger cost
because their unit charge is already included in the enclosing physical cycle.

Building/evaluating possible histories, alternative-plan validation, copying
records, full diagnostics and graph maintenance also take host computation.
They are not charged as separate physical trajectories. Report successful oracle
calls, evaluated quantum nodes, candidate plans, RNG draws and host elapsed
seconds separately. No CPU-constant or zero-memory claim follows from zero world
ticks. Scheduled coherent recipes are quantum descriptions; this candidate does
not derive a new physical cost/delay law for quantum propagation itself.

A deterministic endpoint can reproduce the ordinary mechanical trajectory when
both costs fit the budget. With a tight budget, the explicit resolver overhead
can cause an additional local delay even for a certain outcome. It must not be
hidden to manufacture a bit-for-bit timing comparison. Exact cost-matched
comparison must use the same operation profile.

## Failure and retention

Overflow, bad instruments, stale decisions, exhausted history, invalid branches
or broken causal links fail explicitly. The native engine becomes faulted and
cannot resume. A quantum record may precede a later mechanical failure: these
are sequential local events, not an invented cross-owner rollback. Never publish
a failed run as an alternative valid trajectory. The runner preserves metadata
and causal records for failures that occur during stepping.

Quantum checkpointing replaces live quantum payloads exactly but does not erase
shared causal metadata or physical descendants. Old payload references can retire;
reconstruct future state from the saved full-component checkpoint. Shared metadata
is an append-only bounded audit, not unlimited garbage collection. Existing
record, term, register, node and audit capacities continue to apply.

## Scope and independent expectations

Tests cover the five integer parameter sets and every one of their 365 tickets;
classical physical state and link timing; shared cross-owner ancestry; repeated
periodic encounters; preserved quantum reversal/checkpoint semantics; tight cost
budgets; unchanged default execution; and the canonical headless runner outputs.
For the unit-price eight-tick examples the model costs are 116 for transmission
and 135 for reflection. The budget-2 example meets at tick 15, has local contact
cost 20, commits at tick 24 and sends packets that arrive at tick 25. These are
finite expectations of the declared candidate, not a Newtonian emergence proof.

Independent spatial-field clocks and joint field/carrier proposals are not yet
bound into this shared event program: combining `event_program` with
`spatial_fields` is rejected explicitly. Existing spatial configurations without
an event program remain supported and unchanged. This avoids pretending that
unrecorded field dependencies form a complete unified graph. Infinite-time finite memory and a universal objective event trigger remain
outside the selected contract. Multiple indistinguishable Kraus terms are now
supported by the explicit v2 mixed-state extension.

## Run through the normal engine

```sh
python -m event_universe --init examples/quantum/native_classical.json --output artifacts/native-classical
python -m event_universe --init examples/quantum/native_quantum.json --output artifacts/native-quantum --visualize
python -m event_universe --init examples/quantum/native_cost_delay.json --output artifacts/native-delay --visualize
```

The normal runner writes `run.json`, `state.json`, `events.jsonl`, original
initialization and, for an event program, `causal-events.jsonl`. `run.json` retains
quantum payloads/records and separate cost statistics. Rendering stays opt-in and
uses the existing recorded-state generator; it never supplies physical inputs.
