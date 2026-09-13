# Configure the causal event graph

The causal event graph records which local actions caused later actions. Quantum
programs can use this shared graph, but a graph-only run does not enable quantum
rules. The ordinary action log and the causal graph are separate outputs.

## Choose a mode

| Configuration | Causal graph | Quantum program |
| --- | --- | --- |
| Omit `event_program` entirely | Off | Off in the native event-program path |
| `model: "causal-events-v1"` | On | Off |
| `model: "local-quantum-events-v1"` or `"local-quantum-events-v2"` | On | On; requires the full quantum configuration |

There is no separate graph-recording switch for a running quantum program.
Removing its `event_program` also removes its configured quantum dynamics; this
is not an equivalent faster quantum run. A display setting does not enable or
disable the graph.

## Enable a graph without quantum rules

In the UI, open **Experiment controls** on a phone, then **Names & configuration**
and the **JSON** tab. Add this member to the outermost initialization object,
beside `model_id`, `fields` and `seeds`:

```json
"event_program": {
  "model": "causal-events-v1",
  "capacity": 100000
}
```

This is a member fragment, not a complete run configuration. Separate it from
adjacent members with a comma. Keep one `event_program` key; do not nest it inside
`fields`, `operation_costs`, `observer` or a disturbance type. Strict JSON does
not allow comments or trailing commas. Press **Check configuration** before
running. Configuration edits do not require a simulator rebuild.

For a complete compatible input, use the existing
[classical graph example](../examples/quantum/native_classical.json). Its folder
name does not enable quantum behavior: its `event_program.model` selects the
classical causal ledger. Import that file into the UI, or validate it with:

```sh
python -m event_universe.configuration_validation examples/quantum/native_classical.json --json
```

That command only checks the configuration. To execute the example when a run is
wanted, choose a fresh output directory:

```sh
python -m event_universe --init examples/quantum/native_classical.json --output artifacts/event-graph-demo
```

## Disable the graph

Delete the entire `event_program` member and fix its adjacent comma. Omission is
the default. Do not replace it with `null`, `false`, `{}`, `enabled: false` or a
made-up `model: "off"`; those are not supported configuration forms. Validate the
edited document again. Removing a quantum program changes the chosen experiment.

## Capacity and saved evidence

`capacity` is the positive integer limit on retained causal event records for the
whole run. It is not a tick count, particle count, frame stride or physical memory
per cell. One tick can create several records. Preflight checks deterministic
startup needs; a run can still exhaust capacity later. Exhaustion reports an
error rather than silently dropping history. The value above is an example, not
a guarantee for every world or duration.

| Runner output | Meaning |
| --- | --- |
| `events.jsonl` | Ordinary action trace, also written without a causal graph |
| `causal-events.jsonl` | Causal records when `event_program` is enabled; records contain IDs and parent references |
| `run.json` | Run status and statistics; event programs expose causal-event statistics |

Check the run status before interpreting saved records. The causal file is data,
not an automatically drawn graph. The existing particle movie is a separate view;
turning on the graph does not automatically visualize causal geometry.

## Supported combinations

`causal-events-v1` supports spatial fields, configured emissions, local field
rules, spatial responses and existing computation-dependent carrier waits.
It selects no quantum resolver and does not change their physical results,
operation prices or link times. Both native quantum models still reject spatial
fields: their independent clocks have not been composed. The separate
directional-wait candidate in PR65 still requires its own integration; this
extension does not activate that candidate or a checkpoint format.

The separate `conservation` local energy/momentum audit currently rejects every
native event program, including `causal-events-v1`. This boundary applies both
to JSON and typed `InitialState` input, before allocating event runtime state.
Existing component accounting and local transaction guards remain available
with the graph; they are distinct from this optional audit.

## Spatial provenance and resource bounds

Spatial events use the same ID namespace as carrier events. The graph records
dependencies at local transaction and packet-bundle granularity. A parent names
a supplied local owner input or retained provenance dependency; it does not establish minimal
dependence of each output component on each source. The graph is an analyst's
audit. Its global IDs and ancestors are not inputs to field laws or information
automatically available to a local observer.

| Record | Causal inputs |
| --- | --- |
| `spatial_source` | One root per spatially seeded cell, independently of colocated carrier roots |
| `spatial_cycle` | Previous local field state and the local carrier owner supplied to emission processing; source and rule deltas remain in the action trace |
| `spatial_sent` | The field cycle that prepared this port's actual packet; sibling sends are independent |
| `spatial_received` | Every actual arriving packet and existing local stock, even when signed amounts cancel |
| `spatial_decayed` | The corresponding reception; these two records describe one atomic arrival/attenuation transaction, with no extra clock advance |
| `spatial_escaped` | The terminal packet after its full link time; no exterior cell is created |
| `cycle_started` | The frozen pre-emission field sample when a response reads it, and the field-work event used in the carrier's cost |
| `spatial_coupled` | Through the joint commit: its frozen carrier proposal, current field state and any departure packets it amends |

Emission bookkeeping changes update the carrier's causal head. A delayed carrier
cycle retains its original sample dependency while later field events continue.
At a joint reaction, same-tick field departures may be amended, created or
cancelled under the existing physical rule. Surviving packets then reference
the `spatial_coupled` event. Its `spatial_departures` action-log member, when
present, replaces the complete same-tick departure list; an empty list means
all those field departures were cancelled. Later receipts use the final owner.

Each field cell adds three optional integer references: current state, frozen
sample and field-work event. Each spatial packet adds one. No cell or packet
holds source lists, recursive ancestry or copied event payloads. Appending checks
only bounded direct parents. History traversal is an explicit read-only analysis
operation; normal stepping never traverses ancestors or queries quantum state.
Implicit baselines create no volume-sized collection of root events. Idle field
cells do not create an event on every tick.

Startup capacity counts carrier-seeded cells plus spatially seeded cells.
Before a local field departure, reception or joint commit changes ownership, the
engine checks space for its entire event batch. Exact capacity is allowed; a
batch that cannot fit faults the run before that local transaction changes stock
or consumes packets. Earlier independent completed transactions remain valid.
The world cannot resume after a fault. The runner saves its failed status and
bounded graph rather than silently omitting causal records.

Host storage is linear in retained events, with at most `capacity` records, plus
fixed references per allocated owner. Capacity is an event count, not a byte or
wall-time guarantee. Enabling the graph adds host work; it adds no model work.
Spatial records have zero `model_cost` because spatial work is already included
where the carrier cost contract charges it. The existing `event_ledger_cost`
counter therefore remains the recorded carrier-cycle work, not total field-only
work. `run.json` reports `causal_events` and `causal_event_capacity` separately.

## Reproduce a field encounter without quantum

The complete [signed-field example](../examples/spatial_causal_events.json)
routes +64 and -64 toward each other through configured local operations. Both
arrive at `(4, 2, 2)` on tick 6, where their signed field amount cancels. The
reception keeps both histories. By tick 12 the world is idle and the graph holds
20 events within its capacity of 64. Signed accounting is preserved; this is not
a claim of energy conservation, particle annihilation or a quantum interaction.

```sh
python -m event_universe.configuration_validation examples/spatial_causal_events.json --json
python -m event_universe --init examples/spatial_causal_events.json --output artifacts/spatial-event-demo
```

Join the two JSONL files using action `event_id` and causal record `id`. Physical
values and source/reaction/dissipation details live in `events.jsonl`; parent IDs
and event owners live in `causal-events.jsonl`. Request `--visualize` only when a
recorded physical-state movie is wanted. It does not draw or change the graph.

See the [native event contract](NATIVE_QUANTUM_EVENTS.md) for runtime ownership,
causal links, quantum-specific configuration and failure behavior, and
[configuration validation](CONFIGURATION_VALIDATION.md) for preflight reports.
