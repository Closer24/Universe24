# Selected quantum method: deferred event network

The [register/channel extension](QUANTUM_ENTITIES.md) adds explicit native v2
inputs, finite multilevel registers, density states and grouped outcomes to this
same owner. The binary pure-state contract below describes the original v1 subset;
its old limitation on indistinguishable Kraus terms is removed only by that
explicit extension. The shared [native runtime](NATIVE_QUANTUM_EVENTS.md) supplies
classical feedback; the standalone backend does not own a physical engine.

## Status and scope

`deferred-event-network-v1` is the selected finite quantum-state implementation
under Q-ORACLE-1. It extends the existing `DeferredQuantum` owner. It is not a
second physical simulator, an electron/photon field law, or a universal collapse
criterion. The scalar-amplitude, Focus and terminal-trial APIs retain their old
contracts for owners that do not select this backend.

The user selected a local event lattice plus a demand-driven quantum dependency
graph. This document separates that method from the still-open physical laws.

For composition through the ordinary simulator and runner, use
[native event programs](NATIVE_QUANTUM_EVENTS.md). That contract owns the shared
causal identities, repeated local triggers and charged mechanical paths; this
document owns the finite quantum state and instrument semantics.

## Contract and ownership

| Part | Definition |
| --- | --- |
| Physical input | Immutable unwrapped 3D node addresses and a layer of disjoint one-node or cardinal nearest-neighbor operations |
| Initial state | Binary occupation per configured node; source amplitudes define the joint state, not hidden classical paths |
| Wave storage | Joint source/checkpoint state plus local matrix operations and per-node predecessor links |
| Coherent law | Explicit 2x2 or 4x4 Gaussian-integer matrix satisfying `U* U = scale I`, with positive common scale |
| Instrument | Explicit one-node family of one to four matrices satisfying `sum(K* K) = scale I`; one Kraus matrix per distinguished outcome |
| Query | Conservative backward dependency closure, including relevant earlier recorded constraints, then forward amplitude evaluation |
| Result | Local Born weights; no RNG, historical path selection, or physical-clock advance |
| Decision | First compute every branch weight, then supply one uniform integer ticket; update only the selected conditional state |
| State owner | The existing quantum owner composes one backend; no growing history is stored in ordinary physical nodes |
| Resource contract | Bounded nodes, discovered dependencies, sparse terms, decisions and existing 32/64-bit arithmetic; explicit failure, never a guessed no-event result |

`EventNetworkConfig` accepts 1–30 addresses; the 30-register cap keeps occupation
masks inside the signed register range. This does not imply full states on 30
registers are tractable. Default caps are 10,000 stored nodes, 10,000 visited nodes,
4,096 terms and 1,024 decision identities. These are computational capacities,
not physical constants. Configuration is immutable once bound.

All coefficients use the existing `Amplitude(real, imag)` bounded signed
representation. A whole-state common integer factor may be removed exactly.
Different prospective instrument branches MUST NOT be independently rescaled
before their relative probabilities have been calculated. Coefficients, products,
accumulations and weights are checked; the original arbitrary-precision research
prototype is not copied as an exception to the register contract.

## Algorithm

### Local linked histories

Each configured register has one `EventCursor` in `core/event_links.py`. The
shared event space owns its stream identity, latest event ID and last modeled
operation tick. The native physical Node holds that same handle in a fixed
local tuple; the quantum backend does not maintain a second head dictionary.
Colocated registers have distinct handles. A stream bank is sealed when the
physical engine is assembled, and contains at most thirty handles per Node.
Each handle contains three integers, independent of history length.

Every appended event stores immutable `predecessors`, one previous ID per
participating stream. A local chain can branch into separate later operations
and meet another chain in a shared event. The overall structure is a DAG, not
an independent tree per Node. The shared event store retains the old records;
changing a current head never changes a past event's data or links.

Predecessors describe local history. `parents` describe dependencies required
for evaluation, while `physical_parents` additionally require physical locality.
These are different contracts: chronological adjacency cannot authorize a
remote read or introduce an extra quantum dependency. `history(register)` walks
the local chain newest first; queries walk dependency parents and the required
record constraints. Both traversals are host work, outside ordinary local rules.

Append validates participating handles, owners, addresses, time, capacities and
parent references before publishing any event or head. Read-only public cursor
properties and immutable `NodeView.event_heads` snapshots expose IDs only. This
is an internal ownership boundary, not a sandbox against hostile Python code.

Configured sources, coherent local operations, channels and explicit result
records all use these links. Missing knowledge does not automatically create a
wave or select an outcome. Distinct registers start in a tensor-product state;
a joint operation can correlate them. Interference combines amplitudes of
coherent alternatives, never probabilities from unrelated particles.

### Deferred evaluation

1. `step` validates a whole disjoint local layer before appending its recipes.
   It advances the physical tick once. No amplitudes or random tickets are needed.
2. `query` follows the target head backwards. It includes previously committed
   constraints that overlap the dependency component, repeating to closure.
   Disconnected product histories and irrelevant unitaries may remain unevaluated.
3. The quantum owner evaluates the selected recipes forward from source or
   checkpoint states, retaining complex amplitudes and interference.
4. `prepare` does the same work for a declared instrument. It computes all
   outcome weights, including no-click/no-transfer, before any result is chosen.
5. `commit` binds a result to that prepared request. A uniform ticket in
   `[0, total_weight)` selects the cumulative weight interval. A certain result
   needs no random number. Repeated commits return the original immutable record.
6. A later operation uses the conditional joint state. It does not acquire sharp
   values for all unmeasured quantities, and it does not resample the past.

The links are not the wave by themselves: states and operation laws are essential.
The traversal is conservative, not an optimal tensor-network contraction solver.
No query of an uncomputed coherent branch chooses which historical route occurred.

A decision is tied to its owner, record identity, node, instrument and graph
revision. A graph change makes an uncommitted decision stale; use a fresh identity.
Prepared identities consume the decision budget even if not committed. Callers
must not accumulate unlimited abandoned requests. Past records remain available
in an immutable audit ledger; no API silently reuses their identities.

## What triggers an event?

The controller supplies a local instrument request. This can represent an
explicit measurement or a configured contact with a fresh nonreturning environment.
It is not conditional on a guessed sharp occupation, and no detector object must
be planted in every node. Both transfer and no-transfer are possible outcomes.

A coherent interaction is a local unitary recipe and does not sample. A returning
environment must remain in the joint coherent model. Choosing an outcome at every
interaction can destroy later interference. A fresh-environment trajectory is a
specified open-system model, not proof of objective collapse in the whole universe.
The original instrument form has one Kraus matrix per outcome. The explicit
[register/channel extension](QUANTUM_ENTITIES.md) now retains indistinguishable
terms as a mixed continuation rather than a fake sharp record.

The controller knows its previous records and can compute conditional marginals.
These weights are host information, not a classical signal available to a remote
node. No native Engine or generic field law consumes them in this addition. A
future native bridge must define accessible records, scheduling and physical
commits; a universal physical trigger has not been inferred from uncertainty.

## Closing the past without deleting the wave

`checkpoint(register)` resolves the full live correlated component and saves an exact
joint replacement state. Only then can old recipes be removed. The host operation
creates no measurement, advances no world tick and preserves remaining phases.
A local marginal is not a sufficient checkpoint for a correlated component.
A branch omitted by one query may become necessary at a future recombination.

The replacement is marked `checkpoint` in the shared audit. Its dependency
parents are empty because its complete state replaces that computation; its
per-stream predecessor links retain the audit history. All participating heads
redirect together, preserving their handle identities and each register's own
last modeled operation tick. A checkpoint must neither restart a Link's wait nor
make an otherwise premature Link operation admissible. Old quantum payloads may
be reclaimed; the bounded append-only causal audit is not reclaimed by this call.

Checkpoints summarize computation, whereas records fix a result. Neither proves
that all future possibilities close, that total memory is bounded for infinite
time, or that arbitrary real amplitudes have finite rational representations.
An over-budget or over-range request fails rather than changing the physics.

## Time and cost

Each successful modeled query has unit model cost and zero added world ticks.
The backend's tick is changed only by `step`. Records, checkpoint operations and
host diagnostics do not run a physical engine tick. `host_evaluated_nodes` counts
nodes in successful query/preparation evaluations, not CPU instructions or total
memory; full diagnostics/checkpoints are separate host work. Re-reading a prepared
record reuses the first computation and never causes another ticket draw.

Physical insertion uses at most two heads and fixed local matrices. A complete
host tick, graph scan, tensor-product evaluation and checkpoint are not O(1).
Zero world time is the selected oracle postulate, not zero elapsed machine time.

## Position, momentum and the classical interface

An event has a definite recorded location at its recorded time. Its continuing
quantum state need not have a definite next location or a sharp momentum.
Position and lattice-Fourier diagnostics use the same amplitudes and phases.
For a one-excitation 4x4 periodic Fourier diagnostic, one occupied register produces
16 equal momentum weights. The finite entropic bound is `H(position)+H(Fourier)>=4`.
This tests complementary bases; it does not validate a free-particle Hamiltonian.

The 3:4 beam-splitter matrix in tests and the headless demonstration is an explicit
example, not a default law selected by the engine. It does not by itself derive
free-momentum conservation, Newtonian motion or a quantum-to-classical dynamics
limit. Ordinary disturbance fields and their existing conservation laws are not
replaced by this candidate.

## Entry point and reproducible checks

```python
from event_universe.quantum import DeferredQuantum, EventNetworkConfig

owner = DeferredQuantum()
space = owner.bind_event_network(
    EventNetworkConfig(
        addresses=tuple((x, y, 0) for y in range(4) for x in range(4)),
        occupied=(5,),
    )
)
```

Supply `LocalUnitary` and `LocalInstrument` matrices explicitly. Existing legacy
nodes and a selected event network cannot coexist inside the same owner.

A complete small controller is available as:

```shell
python -m event_universe.integration.quantum_event_trial --ticket 24
python -m event_universe --init examples/quantum/linked_paths.json --output artifacts/linked-paths
python tools/check.py --base origin/main
```

The first command prints headless JSON; its ticket is deliberately supplied,
not claimed to come from a real quantum device. The integration PR records the
actual interpreter, source tree, executed checks and limitations. Required finite
expectations are listed in [TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md).

`linked_paths.json` is ordinary initialization for a four-Node, four-tick
one-excitation interferometer. Its configured mixer splits A/B on tick 1,
configured swaps move those modes to C/D on tick 2, tick 3 is idle, and a mixer
recombines at C/D on tick 4. The final occupation probabilities are C=0, D=1;
inserting a phase reversal at C on tick 3 gives C=1, D=0. A position record at C
on tick 2 gives C=D=1/2 at the output for either recorded outcome. The tests
repeat every case with and without a correlated checkpoint. Matrices are
explicit example laws; this is not spontaneous propagation into unconfigured
Nodes or a derivation of particle dynamics.
