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

Current native event programs reject nonempty `spatial_fields`. A graph-only
program has the same composition limit as a quantum program. Do not remove the
fields of an intended experiment just to make validation pass; report the missing
composition instead. The directional-wait candidate in PR65 also explicitly
rejects event programs; this guide does not enable that pending integration.

See the [native event contract](NATIVE_QUANTUM_EVENTS.md) for runtime ownership,
causal links, quantum-specific configuration and failure behavior, and
[configuration validation](CONFIGURATION_VALIDATION.md) for preflight reports.
