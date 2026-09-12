# Reusable experiment packages

A package separates reusable definitions, the environment, initial placements and
run controls. Loading it produces one ordinary initialization JSON and validates
that input with the [canonical parser](DISTURBANCES.md). Editing a package requires
no code compilation, package rebuild or new physical engine.

The complete example starts at
[experiment.json](../examples/experiment-package/experiment.json). It defines one
moving type and places two instances with opposite headings. They share a node
after two ticks and pass through each other; no collision law is selected. The
declared quantity stays two. Labels do not select physical laws.

## Manifest and ownership

```json
{
  "experiment_version": 1,
  "schema_version": 1,
  "model_id": "reusable-two-streams-v1",
  "environment": "environment.json",
  "definitions": ["definitions/entities.json"],
  "initial_conditions": "initial.json",
  "run": "run.json"
}
```

`experiment_version` versions this authoring format. `schema_version` selects the
existing runtime contract, currently 1 or 2. The manifest owns both version
numbers and `model_id`; parts cannot override them. The destination output
directory is selected at execution, so the package has no host-specific path.

| Part kind | Members of `data` |
| --- | --- |
| `environment` | `shape`, `boundary`, `topology`, `slots_per_cell`, `link_ticks`, `normal_budget`, `operation_costs`, optional `unit_system` |
| `definitions` | `fields`, `disturbance_types`, `couplings`, `interactions`, `spatial_fields`, `emissions`, `spatial_couplings`, `field_groups`, `field_rules`, `spatial_interactions`, `event_program` |
| `initial_conditions` | `seeds`, `spatial_seeds` |
| `run` | `ticks`, optional `visualize` and `frame_stride` |

Each part uses this envelope:

```json
{
  "part_version": 1,
  "part_kind": "definitions",
  "includes": ["fields.json"],
  "data": {
    "disturbance_types": [
      {
        "name": "traveler",
        "fields": ["quantity", "heading"],
        "defaults": {"quantity": 1, "heading": [1, 0, 0]},
        "transport": {"mode": "move", "direction_field": "heading"}
      }
    ]
  }
}
```

An included part must have the same kind. Paths are relative to the file that
contains the reference, use `/`, and end in `.json`. Absolute paths, URLs,
backslashes, `.`/`..` segments and paths resolving outside the package directory
are rejected. Referenced files and directories cannot be symbolic links or
junctions: the captured package must remain reproducible using ordinary files.
Keep shared definitions inside the directory containing the
manifest. Files outside that root require an explicit copy into the package.

Includes are processed before the containing file, in declared order. Each
resolved file contributes once, including in a shared dependency diamond.
Cycles, duplicate reference entries and unknown keys fail. Limits are 64 unique
source files, include depth 16 and 16 MiB of total source bytes, including the
manifest. These bound host-side loading, independently of local physical costs.

## Reuse and placement

`fields` and `disturbance_types` have the same structure as runtime definitions.
Declare a type once, including its defaults and generic rules. Every seed then
selects that type and optionally supplies different values:

```json
{
  "part_version": 1,
  "part_kind": "initial_conditions",
  "data": {
    "seeds": [
      {"position": [2, 4, 4], "type": "traveler"},
      {"position": [6, 4, 4], "type": "traveler", "values": {"heading": [-1, 0, 0]}}
    ]
  }
}
```

Repeated seeds are distinct instances, including identical entries, subject to
the configured cell capacity. Their order is preserved. The loader never changes
positions, overrides values by species name or infers interactions.

Different files can share exactly equal field or type declarations. Conflicting
declarations with the same name fail; there is no implicit last-file-wins rule.
Repeated names inside one part fail. Other named rules must have unique names,
and emissions must have unique type/field pairs. Scalar environment and run
members can repeat only with equal values. Explicit rule ordering is preserved.

The existing [catalog adapter](ENTITY_CATALOG.md) remains available for catalog
representation profiles. Its output and these packages both target ordinary
runtime definitions. Packages do not interpret catalog IDs or add a second
entity representation or species lookup.

## Load, validate and run

```sh
python -m event_universe --experiment examples/experiment-package/experiment.json --validate
python -m event_universe --experiment examples/experiment-package/experiment.json --output artifacts/two-streams
```

The run part requires `ticks`; `visualize` defaults to false and `frame_stride`
defaults to one. Output placement and the existing optional reception observer
remain runner options. The complete runtime input contains `ticks`, but never
authoring references, `includes`, `visualize` or `frame_stride`.

The host API is `event_universe.experiment.load_experiment(Path(...))`. Its frozen
`ExperimentPackage` contains `initial`, exact `runtime_json` bytes, and ordered
`sources` with relative path, original bytes and SHA-256. `run_controls` and
`provenance` return independent dictionaries; modifying those dictionaries cannot
alter the captured run. Each source is read once. Later file edits affect the next
load, not an already prepared experiment.

Provenance records the manifest name, each captured source hash, the hash of the
merged runtime JSON, and the hash of resolved run controls. The merged JSON uses
UTF-8, sorted object keys, two-space indentation and a terminal newline; array
order is retained. Source hashes cover original bytes, including whitespace.

## Formal JSON Schema

Project schemas use JSON Schema Draft 2020-12 and are installed as resources in
`event_universe.schemas`. `schema_document("runtime")` returns the runtime schema;
other names are `experiment`, `environment`, `definitions`, `initial_conditions`,
`run`, `native-events` and `unit-system`. External references use the canonical
repository schema IDs. Consumers can register the packaged resources for fully
offline resolution. The simulator itself needs no JSON Schema library.

```sh
python -m event_universe --schema runtime
python -m event_universe --schema experiment
```

Schemas cover supported object members, recursive expression shapes, transport
variants, version-specific spatial fields, native events and units. They do not
replace semantic validation: names and owned fields must resolve, vector sizes
must match references, topology must close, expression work must stay bounded,
and incompatible capabilities must fail. JSON Schema also treats `1.0` as an
integer value, whereas the runtime requires actual integer JSON tokens. Run the
canonical validator before execution. Do not add `$schema` to a strict runtime
input; select its schema through the editor or validator configuration.

The schemas describe this project's interchange format. They do not make the
model an openPMD, HDF5 or VTK implementation, and do not establish physical laws
from the names of configured quantities.
