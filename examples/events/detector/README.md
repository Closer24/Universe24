# Physical detector examples

These data-only worlds select `dynamics: "reversible-detector-v1"` in the
ordinary events engine. The candidate's
[published contract](../../../docs/DETECTOR_REQUIREMENTS.md#implementation-contract-reversible-detector-v1)
defines its assumed local law, physical state, inverse and limits. Default
`events-v1` worlds keep their existing measurement and mixing rules.

An incoming Event physically traverses a chain of ordinary measured Events.
Each contact preserves the carrier's amount, identity and phase, routes it by a
port permutation, and changes the local material phase and recoil. One declared
output Event supplies a group result from its phase relative to its own clock.
The observer does not sum the covered Nodes or recover a result from the log.

| World | Coverage and output | Trigger | Declared duration |
| --- | --- | --- | --- |
| `shared_3_nodes.json` | Three Nodes on a 9-by-9-by-1 board; one output at `(5,4,0)` | One unit arriving from any covered position can produce the common result | 4 ticks for the supplied carrier starting at `(2,4,0)` |
| `shared_100_nodes.json` | A 100-Node serpentine chain on a 12-by-12-by-1 board; one output at `(1,10,0)` | One unit; 100 covered Nodes do not require 100 quanta | 101 ticks for the supplied carrier starting at `(0,1,0)` |
| `grouped_12_nodes.json` | Four disjoint chains of three Nodes on a 9-by-9-by-1 board; four distinguishable output groups | Two units per group; supplied as one amount-2 bundle per chain | 4 ticks |

The three examples use `N=32`, `K=1024`, fixed material content 1,
output capacity 31 and reference phase 0. The shared-output carriers have phase
16; the four separate groups use phases 0, 8, 16 and 24. Only declared initial Events supply the incoming inventory; no new signal
is created during a contact. A port permutation at a corner routes the actual
carrier and takes its balancing recoil. The last tick leaves the carriers on
the board; increasing the duration can hit the unsupported escape boundary.

Run the read-only preflight first, using the repository's Python 3.14 environment:

```bash
python -m event_universe.configuration_validation examples/events/detector/shared_3_nodes.json --json
```

Run a prepared example into a new output directory:

```bash
python -m event_universe --init examples/events/detector/shared_3_nodes.json --output artifacts/detector_3
```

The normal runner retains `initialization.json`, `run.json`, `state.json` and
`events.jsonl`. Candidate snapshots identify `dynamics` and contain
`detector_readouts`: each detector has `name`, `positions` and `groups`, and
each group has `name`, `value` and `triggered`. `value` counts units transduced
at the physical output, and `triggered` compares it with that group's threshold.
Old `detectors` summaries and transduction logs are diagnostics, not missing
physical memory. The user-requested demonstration additionally retains a
standalone HTML with its dated source and initialization fingerprints.

Coverage, grouping and threshold are independent configuration choices. To
change an entry position, preserve the declared actual route and allow its
travel time. Group membership alone does not deliver a signal. Different path
lengths can reveal position through timing; these examples do not promise
complete spatial anonymity. Repeated passage through the output counts again,
so these trial paths cross it once.

This is nondestructive transduction, not matter absorption or a thermal model.
Full output capacity, a forbidden slot state, integer overflow or an attempted
escape refuses the interval before committing it; refusal is not a physical
reset or saturation mechanism. The candidate preserves amount and total
material-plus-carrier momentum on its domain. It supplies no energy law for the
fixed support and no derivation of Heisenberg, Born statistics or Bell violation.
The owner's sensitivity-and-information hypothesis remains a separate research
question. Composite absorbers and reduced coarse cells are separate designs.
