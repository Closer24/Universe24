# Generic field definitions and positive records

The user-directed [Highlights document](https://docs.google.com/document/d/1IkhSyqZZMBSgbJV-PMMwcXG0D_Rlfg4FrLy2jXBMUSs/edit),
including section 3.3.1, requires fields to share a local definition contract,
conserve discrete flux and retain integer directional ratios. The experimental
`GenericFaceSimulation` runs every configured definition through one `FieldBank`.
Its current identity is `generic-conserved-flux-bank-v2-experimental`.
Conservation is not proof of moving self-force cancellation or complete causality.

## Conservation and directional ratios

Every definition declares fixed conserved channels and independent measurements
of its state and packets. It also declares source and sink budgets from local
inputs and immutable parameters. A publication callback cannot invent a budget
to explain its own residual. The bank checks, for every channel:

- Old inventory plus the declared source equals outgoing packet inventory,
  retained inventory and the declared sink.
- Retained inventory plus completed incoming packets equals new inventory.

Both checks use bounded working arithmetic. All packets, states and response
faces are validated before the atomic bank commit. A mismatch faults the update;
there is no rounding sink, saturation, optional accounting bypass or field-name
branch. The correctness of an injected inventory measurement is still a reviewed
law contract; arithmetic checks cannot prove an intentionally dishonest callback.
Neutral state and packet records must measure zero, because the sparse scheduler
omits neutral packets and unvisited zero cells.

The shared `split_ratio` primitive emits whole weighted bundles. With available
amount A and fixed integer weights whose sum is W, the bundle count is A divided
by W, rounded down. Each outgoing portion is its weight times that count. The
remainder stays in local state and joins later input. Consequently every nonzero
bundle has exactly the declared directional ratios; rotating leftover units among
faces would provide only a time average and is not this law.

`scalar_definition()` is a new conservative scalar redistribution law, not the
historical scalar potential stencil. It explicitly changes direction through
local isotropic redistribution into six equal portions. Its state stores received
flux and a remainder below six. It accepts only denominator 6; a denominator-seven
potential request fails instead of silently changing meaning.

`octant_definition()` retains eight fixed sign sectors. Each sector redistributes
into its three sign-compatible directions in equal bundles, retaining a remainder
below three. Sector inventories are checked separately, so loss in one cannot
cancel creation in another. It never rotates rounding leftovers or changes an
octant's signs. Local redistribution and its directional weights are explicit
policies, not a hidden change of direction in free propagation.

Both supplied definitions add the persistent occupancy source once on every
publication tick and have zero sinks. Apparent dilution comes from local spreading,
not a distance or radius formula. Total inventory on a periodic lattice therefore
persists after sources stop; a stranded remainder waits for later input. General
absorption/decay capability is not implemented by these zero-sink definitions.
No claim of field extinction or physical gravity follows from this behavior.

## Stored representation and local bounds

Each signed field value uses two strictly positive integers `(magnitude, code)`.
Code 1 represents zero with magnitude 1; codes 2 and 3 represent positive and
negative values. The previous signed physical range is unchanged. Booleans,
invalid bounds and noncanonical zero encodings are rejected. Supplied conserved
flux definitions additionally reject negative decoded inventory.

| Definition | Positive state registers | Positive packet registers | Conserved channels | State plus six response pairs |
| --- | ---: | ---: | ---: | ---: |
| Scalar redistribution | 4 | 2 | 1 | 16 |
| Octant redistribution | 32 | 16 | 8 | 44 |

A cell containing both fields stores 60 positive field integers. Incoming packets
are transient routing buffers, not retained history. Six response pairs represent
last delivered values and are used by the next local response; they are not added
again when measuring conserved inventory. Old/new state proposals, six packets
per definition, a three-component response snapshot and inherited six-value/K-slot
working snapshots have separate bounded local costs. Total host cost grows with
materialized cells; this is not a constant-time world simulation.

Definitions, widths and field count are fixed at construction. Sparse operation
requires zero-source neutral state to remain quiescent at every phase. Construction
checks phase zero; purity and all-phase quiescence remain definition obligations.
No source identities, trajectory history or growing packet queue are used.

Positive coding covers new field state and messages. Historical particles, clocks,
momentum ledgers and sentinels remain outside this representation migration. The
whole simulator is not positive-coded on this evidence alone.

## Definition and runtime interface

| Operation or property | Responsibility |
| --- | --- |
| `publish(old_state, source_count, phase)` | Six outgoing packets and the retained state |
| `absorb(retained_state, incoming, source_count, phase)` | New state and six encoded source-facing response values |
| `inventory_state`, `inventory_packet` | Independent per-channel inventory measurements |
| `source_amount`, `sink_amount` | Explicit publication budgets; never inferred from imbalance |
| `conserved_width` | Fixed number of independently checked channels |
| `response(faces)` | Local bounded working response vector |
| `allowed_faces`, `allowed_directions` | Fixed incoming-face and outgoing-direction codes 1 through 6 |
| `direction_change_rule` | Explicit local redistribution or absence of direction-changing interaction |
| `response_unit` | Compatibility identifier required before summing responses |

Face order is +x,-x,+y,-y,+z,-z. Incoming faces point toward the supplying neighbor;
outgoing codes indicate travel. An exclusively +x publisher needs incoming -x
permitted as well. Forbidden nonzero packets and response faces are rejected.

The bank publishes only old state, routes one edge, then absorbs into retained
state. Every field uses this same runtime. Independent tests supply a third
policy without editing the engine. Definition responses are summed in bounded
working arithmetic before the shared full-vector particle update and equal/opposite
local momentum exchange; the sum is not narrowed into a fake six-face record.
The common response-unit identifier is an experimental computational scale, not a
calibration showing that different fields have equal physical strength.

`GenericFaceSimulation(config, definitions=(scalar_definition(), octant_definition()))`
selects both fields. Optional `collisions=True` reuses the existing local pair law.
Only unit links are supported: larger positive lengths fail explicitly. Publishing
once per long-link cycle would change source behavior and is not an allowed
shortcut. Generic variable-length field and matter transit remains unfinished.

## Motion, display and unresolved acceptance

The shared movement adapter keeps the discrete momentum component ratios during
free motion, retains fractional speed credit and schedules at most one cardinal
hop per tick. Individual hops cannot represent all components simultaneously;
exact signed hop counts reproduce the ratio over a complete axis cycle. Existing
movement tests and an actual generic zero-source run check this behavior. Local
interactions may change momentum and therefore the subsequent direction ratio.

Particles use the previous local delivered response. This removes the tested
fresh-field-to-moving-particle two-edge relay, but does not establish the complete
causal cone. Moving self-emission and competing arrivals remain mandatory failing
acceptance cases. Conservation and new model names do not waive those gates.
Historical APIs and their frozen reference remain unchanged compatibility evidence,
not accepted implementations of Highlights 3.3.1. No new default is promoted.

For diagnostics, `field_faces`/`face_at` expose the first field's last delivered
flux, identified by `display_field_name`; `field_faces_by_name` exposes every field
separately. `field_inventory_by_name` includes retained remainders in each field's
conserved channels. A cloud of delivered face magnitudes is not total inventory,
and different field magnitudes are never summed for display.
