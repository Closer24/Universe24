# Local work readout and configured directional response

> **History (2026-09-19).** The engine this document describes was deleted on
> 2026-09-19 with the old engine ([migration](MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted));
> the one engine is the field-only engine of the law of the shadow
> ([SPATIAL_FIELDS.md](SPATIAL_FIELDS.md#the-law-of-the-shadow-field-only-v1)).
> The text below is kept as the record of what was built and measured; its
> links to code, worlds and tests name files that no longer exist.

The generic emission expression accepts `{"node": "committed_cost"}`. It reads
one bounded nonnegative scalar owned by the colocated carrier Node: the cost of
its most recent successfully committed cycle, including that cycle's local field
processing. It is initially zero. Pending work is excluded. It remains at the
Node after a carrier leaves and is not part of a transferred record.

The readout is available only in emission expressions. It cannot read a neighbor,
global work ledger, replay graph, pending plan or arbitrary Node attribute. The
field law receives the integer value, not the Node or world. Other expression
contexts reject the leaf. Scalar/vector arithmetic and overflow rules are unchanged.
Snapshots and the immutable Node view expose `committed_cost` separately from the
existing most recently planned `cost` / `last_cost` diagnostic.

Existing `cost_field` behavior is preserved, including its hold-only restriction:
that property is a carried reporter, not this Node-owned readout. Moving emitters
can use the new leaf without owning or transporting a cost property. An emission
still occurs for each eligible resident emitter at the configured interval and
uses its existing residue/budget. This extension does not add autonomous sources
to empty or field-only Nodes, and a cost readout is a level from the last completed
cycle, not a new quantity consumed exactly once. Several eligible records can
each use that same local level, as explicitly configured.

## Candidate contract

The moving-pair initialization (`examples/computational-response/moving-pair.json`, deleted on 2026-09-17)
defines one reusable body and two seeds. This is an explicit candidate, not a
derived gravitational law or a realistic particle model.

| Part | Definition |
| --- | --- |
| Source input | Previous committed local work minus the body's ordinary-work threshold |
| Emission | Clamp the excess to 0..64, multiply by a configured three-component vector |
| Eligibility | Existing property selector requires momentum and response properties |
| Directional input | Nonzero vector payload actually received on each last-hop travel port |
| Reaction | Add the configured opposite-port impulse times the body's signed response property |
| Opposite reaction | Subtract the same impulse from the locally owned spatial momentum register |
| Invariant | Carrier plus local-field momentum is unchanged by every joint proposal |
| Timing | Existing schema-1 cost-budget scheduling; link transit and h are unchanged |
| Bounds | Existing field, slot, expression, operation and integer limits; six configured rules |

Ports identify the direction of packet travel on the last link. For example,
positive-X travel arrived from the negative-X neighbor; the example's impulse is
negative X. No remote source position is inferred or looked up. Equal opposite
inputs cancel. A zero response property disables the impulse; reversing its sign
reverses the reaction. Names have no behavioral role.

The three-component source payload is not asserted to be a radial gravitational
vector. This candidate uses its received magnitude as a trigger and the last-hop
port as the direction. Its impulse law is expressly supplied in JSON. Arrival of
an old signal can continue after a source stops, and a moving source can encounter
its earlier field; no nonlocal self-field subtraction is performed.

The spatial momentum register retains reaction stock locally. It is an explicitly
defined component ledger; physical field energy, inertia and source recoil are
not derived here. No claim of kinetic-energy conservation or Newton's law follows
from its exact momentum invariant. Future physical candidates must supply and
test the corresponding energy/readout definitions and constitutive rules.

## Validation and memory

`tests/test_node_work_emission.py` (deleted on 2026-09-17) checks zero startup, pending versus committed
cost, a moving emitter entering a fresh Node, invalid/missing/out-of-scope reads,
integer arithmetic and legacy emission behavior. `tests/test_computational_response.py` (deleted on 2026-09-17)
checks causal input/output for each of six ports, opposite reactions, transient
trigger consumption, cancellation, disabled coupling and name independence.

The production state addition is one integer register per allocated carrier Node;
the public view and optional snapshot copy it for observation. There is no history,
per-source map, extra world scan or growing physical buffer. The spatial planner
interface gains one scalar argument, with no extra physical ownership access.
Ordinary headless execution remains the default.

Run the example with the ordinary runner:

```text
python -m event_universe --init examples/computational-response/moving-pair.json --output artifacts/node-work-pair
```

Use a new output directory for every run. Initialization is runtime JSON; it does
not require a simulator rebuild. Rendering remains separately opt-in.

With `spatial_computation_delay`, emission reads the previous completed shared
cycle cost. Its source debit commits with the frozen field/carrier proposal.
The Node register updates only after that commit; moving carriers cannot carry
it to the next Node. The indexed `node_execution` clock remains a separate mode.
