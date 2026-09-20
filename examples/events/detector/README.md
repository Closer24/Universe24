# Detector definition examples

These worlds place reusable apparatus from the separate definitions file
`entities/detectors.json` into worlds of the law of the ray (`"law": "rays"`).
The [entity loading contract](../../../docs/ENTITY_DEFINITIONS.md) keeps
geometry, tables and detector settings in data; the world declares placement,
GameBoard shape, topology and the incoming rays. The law that runs them is
[the law of the ray](../../../docs/RAY_LAW.md): every measured event of the
apparatus measures the family `carrier`, and the detector that groups them
reads the squared coherent record of what clicked at each of its Nodes. The
`reversible-detector-v1` candidate these worlds selected until 2026-09-19 is
absorbed into the ray law and deleted
([migration](../../../docs/MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1)):
the pointer is the record, the routing is the flight table.

| World | Apparatus | Incoming rays | Intervals |
| --- | --- | --- | --- |
| `shared_3_nodes.json` | `three_node_detector`: three Nodes in a row on a 9-by-9-by-1 GameBoard, one detector `apparatus` of threshold 1 | one ray of amount 1, phase 16, on +X from `(2,4,0)` | 4 |
| `shared_100_nodes.json` | `serpentine_100_detector`: a 100-Node serpentine chain on a 12-by-12-by-1 GameBoard, one detector of threshold 1 | one ray of amount 1, phase 16, on +X from `(0,1,0)` | 101 |
| `grouped_12_nodes.json` | `grouped_12_detector`: four disjoint chains of three Nodes on a 9-by-9-by-1 GameBoard, four detectors `group_0` to `group_3` of threshold 2 | one ray of amount 2 per chain at the phases 0, 8, 16 and 24 | 4 |
| `periodic_z_node.json` | `single_node_detector`: one Node at `(4,4,0)` on a 9-by-9-by-1 GameBoard with z periodic, its entry `{"rule": "measure", "reads": "tensor"}` | one ray of amount 1, phase 16, on +Z at the Node itself (the stub of extent 1) | 3 |

All four use `N=32`, `K=1024`, fixed material content 1 and the paid family
`carrier` of `quantum` 1 (the kind follows from the quantum; the apparatus
definitions write `measure` out, the rule the keys give a paid family, as
the apparatus's own intent). Only the declared rays supply the incoming
inventory; a ray that reaches a Node of the apparatus with the threshold met
clicks there (the amount and the content enter the measured event, the
record line carries the pointer and its square) and the run's detector
report accumulates the record per detector. The ray of the periodic example
lands on its own Node at every interval the flight table moves it.

The definitions are `three_node_detector`, `serpentine_100_detector`,
`grouped_12_detector` and `single_node_detector`. Their world origins are
`(3,4,0)`, `(1,1,0)`, `(3,1,0)` and `(4,4,0)`, respectively. Each instance is
named `apparatus`; its local detector `apparatus` becomes the record label
`/apparatus/apparatus`. Labels do not select physical behavior. To reuse a body,
add an explicit placement of its definition; overlapping material is refused.

Run the read-only preflight first, using the repository's Python 3.14 environment:

```bash
python -m event_universe.configuration_validation examples/events/detector/shared_3_nodes.json --json
```

Run a prepared example into a new output directory:

```bash
python -m event_universe --init examples/events/detector/shared_3_nodes.json --output artifacts/detector_3
```

The normal runner retains `initialization.json`, `run.json`, `state.json` and
`events.jsonl`. For these external-definition inputs it also saves
`initialization_bundle.json` with the dependency closure and
`resolved_initialization.json` with the expanded physical world. Metadata records
their fingerprints and the exact definitions-file fingerprint. An existing
prepared input does not change when its original definitions file is edited.

For the workspace, choose a file-backed template or import a self-contained
bundle. Create one without running the world:

```bash
python -m event_universe.world_loading --input examples/events/detector/shared_3_nodes.json --output detector_portable.json
```

The output must be a new file. Exported bundles can move to another directory and
run without access to the original definitions path. Source-only Check, Export
and Run accept complete bundles; they do not search for a missing dependency.
These are research configurations, not tests with pinned outputs; the two
dated runs of the candidate they replaced keep their scope in
[validation](../../../docs/VALIDATION.md).
