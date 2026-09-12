# Universe24 configuration guide

## File map

| File | Owns | Consumer |
| --- | --- | --- |
| Physical reference catalog | Descriptive properties, identities and possible interactions; no formulas | Catalog validator and explicit profile adapter |
| Representation profiles or law JSON | Declared normalization, initial values and explicit experiment rules | Existing entity adapter or example preparation script |
| Experiment authoring JSON | Selected definitions, placements and parameter choices | That example's preparation script, if one exists |
| Versioned experiment manifest and parts | Environment, definitions, initial conditions and run controls, with bounded local includes | `python -m event_universe --experiment ...` |
| Final initialization JSON | Complete validated world and initial state | `python -m event_universe --init ...` |
| Display JSON | Supported camera, arrows, dimensions and playback controls | The selected renderer, not the simulator |
| Run output directory | Copied input, metadata, states, events and optional recorded HTML | Inspection and rendering tools |

The [experiment package contract](../../../docs/EXPERIMENTS.md) defines the manifest
and reusable parts, with a complete runnable example. A simple run still needs
only one initialization JSON. There is no generic `include`, `entities_file`, `camera`
or `display` member in that runtime file. Reusable authoring files must be assembled
by a supported adapter. Optional passive probe placement belongs in the `observer` member. Do not put Python expressions or callbacks into JSON.

For reusable files, start with `examples/experiment-package/experiment.json`.
Run `python -m event_universe --experiment examples/experiment-package/experiment.json --validate`,
then replace `--validate` with `--output artifacts/package-run`. Export the offline
editor contract using `python -m event_universe --schema runtime`. Run controls
in the manifest's run part can be overridden by explicit CLI flags.
See [checkpoint continuation](../../../docs/CHECKPOINTS.md) for saving complete
state instead of reconstructing it from a movie or final snapshot.

## 1. Start with a complete working configuration

From the repository root, copy
[two-streams.json](../assets/two-streams.json) to a new input path such as
`artifacts/inputs/my-world.json`. It defines one reusable moving type and places two
instances in a periodic 9 x 9 x 9 domain. They approach, share a node, pass through
and return. It deliberately defines no encounter rule: co-location alone does not
imply a collision. The declared conserved inventory is 2 throughout.

PowerShell, using an existing project Python environment:

```powershell
New-Item -ItemType Directory -Force artifacts/inputs | Out-Null
Copy-Item -LiteralPath skills/simulation-configuration/assets/two-streams.json -Destination artifacts/inputs/my-world.json
$env:PYTHONPATH = (Resolve-Path src).Path
python -m event_universe.configuration_validation artifacts/inputs/my-world.json
python -m event_universe --init artifacts/inputs/my-world.json --output artifacts/my-world-run
```

The validation command is read-only. Run the following simulation command only
when execution or behavioral acceptance is requested. See the
[validation contract](../../../docs/CONFIGURATION_VALIDATION.md) for supported file
kinds, explicit profile/catalog and observer/world dependencies, structured errors
and unsupported authoring formats. A passing preflight does not prove future run
completion or the physical law.

Choose a new input destination before copying and a new run directory on each run.
Use the verified project interpreter instead of `python` if PATH resolves another
installation. An editable package install is an alternative to `PYTHONPATH`.
No environment reinstall is needed for each configuration edit.

## 2. Space, capacity, clocks and duration

The authoritative top-level table is in
[DISTURBANCES.md](../../../docs/DISTURBANCES.md#json-schema-versions-1-and-2).

| Key | How to choose it |
| --- | --- |
| `schema_version` | `1` for conservative outward or configured local fields; `2` for finite dissipative outward fields |
| `model_id` | A descriptive identity for the selected rules; use a new identity for a new hypothesis |
| `shape` | Three integer node counts, such as `[9,9,9]` or `[64,64,64]`; the latter is 64 cubed, not a 2D plane |
| `boundary` | `periodic` connects opposite faces; `open` records escaping stock |
| `topology` | Omit for six cardinal links, or select [configured offsets and sites](../../../docs/CONFIGURED_TOPOLOGY.md); number alone is insufficient |
| `slots_per_cell` | Maximum co-resident carried records, 1 through 32; this is not the number of spatial modes |
| `link_ticks` | Positive travel time for each nearest-neighbor link |
| `normal_budget` | Positive local computation budget; lowering it can delay carrier commits |
| `operation_costs` | Explicit positive prices for all nine operations, as in the template |
| `unit_system` | Optional [coherent rational SI calibration](../../../docs/UNITS.md); validates dimensional operations before running |
| `ticks` | Requested physical duration; CLI `--ticks` is an explicit override |

Coordinates start at zero. For shape `[9,9,9]`, every seed component is 0 through 8.
A +X step from `[8,4,4]` returns at `[0,4,4]` with unchanged signs under periodic
boundaries. `link_ticks`, transport rate and computation delay can affect motion;
GIF `frame_ms` cannot. A larger domain does not add resolution to a fixed node.
Begin with a bounded case before allocating a 64-cubed recorded state.

For eight BCC links and a configured vector encounter, start from
[bcc_vectors.json](../../../examples/topology/bcc_vectors.json). Its accompanying
[example explanation](../../../examples/topology/README.md) defines the rotation,
measured invariants and limits. Use `transport: "local"` for spatial fields in a
configured topology; the default outward/rotation/native-event paths have separate
six-port contracts. Port weights and `received`/`outgoing` indices follow the saved
offset order. A direction provider on this topology explicitly selects
`direction_policy: "positive-dot"`. Editing these values requires no compilation.

## 3. Define quantities and reusable entities

`fields` declares each scalar (`components: 1`) or vector (`components: 3`) once:

```json
{"name":"momentum","components":3,"units":"momentum unit","signed":true,"conserved":true,"scale":1,"extensive":true}
```

Payloads use bounded integers, not floats. `scale` describes a denominator; the
engine does not convert physical units automatically. `conserved` declares an
additive amount, and requires an extensive field (`extensive: true` is the default).
A direction can be intensive and
nonconserved. Energy derived from several registers needs its own expression and
acceptance check. Declaring a field named energy does not calculate it.

With `unit_system`, each field's `units` must resolve to a declared dimension and
exact rational SI scale. The coherent raw quantum is shared across all fields of
the same dimension. Use the host conversion helpers for authoring values; they
reject unrepresentable integers. The runtime gains no automatic conversions or
hidden mass, energy or momentum formulas. Without `unit_system`, existing labels
and numerical behavior remain unchanged.

`disturbance_types` owns the fields carried by a reusable type, `defaults`, local
updates and its `transport`. `seeds` creates occurrences:

```json
{"position":[6,4,4],"type":"stream","values":{"direction":[-1,0,0]}}
```

This reuses the template's type and changes only one initial value. Supported seed
members are `position`, `type`, `values`. Do not add an instance `name` key. Type and
field names are reusable labels; per-instance presentation labels belong outside
the runtime file unless the selected display schema supports them.

For existing particle definitions, use the
[entity catalog](../../../docs/ENTITY_CATALOG.md):

```sh
python -m event_universe.entities --catalog examples/known-entities/catalog.json --profiles examples/known-entities/representation-probes.json --entity electron --entity proton --entity neutron --ticks 36 --output-init artifacts/inputs/three-entities.json
```

Edit the generated file's `shape`, `boundary`, `seeds` and explicitly supported
transport parameters, then validate again. The adapter selects each entity ID
once; create additional occurrences by adding seeds of its generated type.
For programmatic authoring, pass `profiles` explicitly to `compile_entities`,
which also supports `shape`, `ticks` and
`link_ticks`; the CLI currently exposes `--ticks`, not all of those options.

The version 2 physical catalog contains no executable expressions. Physical
properties and possible interactions stay in that reference; experiment profiles
are supplied through a separate file. Never infer update laws, reaction rates or
lattice parameters from catalog measurements. Validate reference changes with
`python -m event_universe.configuration_validation examples/known-entities/catalog.json`.
Check every supplied representation, including unselected entities, with
`python -m event_universe.configuration_validation examples/known-entities/representation-probes.json --catalog examples/known-entities/catalog.json`.
The supplied profiles are representation probes, not a mass-calibrated particle
theory. Do not assume that selecting electron adds Coulomb force, or that its
inventory register is its SI mass. Reuse or author explicit executable profiles,
declare a consistent integer normalization, and retain their physical limitations.

## 4. Choose propagation and field ownership

| Requested behavior | Configuration owner | Working reference |
| --- | --- | --- |
| Hold or move a whole carried record | Type `transport` with `hold` or `move` | [Basic input](../../../examples/basic.json) |
| Split extensive payload by local weights | Type `transport` with `split` | [Disturbance contract](../../../docs/DISTURBANCES.md) |
| Persistent spatial value and explicit local propagation | `spatial_fields` with `transport: local`, then `field_rules` | [Directional law](../../../examples/directional-wave/law.json) |
| Outward spatial propagation and baseline | `spatial_fields` with `transport: outward` | [Spatial fields](../../../docs/SPATIAL_FIELDS.md) |
| Source injection | `emissions` | [Spatial fields](../../../docs/SPATIAL_FIELDS.md) |
| Field acts on a carried record | `spatial_couplings` or schema 1 `spatial_interactions` | [Spatial response](../../../docs/SPATIAL_COUPLINGS.md), [local rules](../../../docs/LOCAL_FIELD_RULES.md) |

The [local Lorentz pulse](../../../docs/LOCAL_LORENTZ_FIELD.md) is also a complete
schema 1 field/carrier example with normalized masses and exact paired momentum
reaction. Its held, one-shot probes are explicit experiment controls. It does not
establish Maxwell evolution or energy conservation; preserve that scope when reused.

The six transport ports are `[+X,-X,+Y,-Y,+Z,-Z]`. Payload vectors have three
components. A negative amplitude is not automatically a negative travel port.
`spatial_seeds` uses the engine's eight population bins: scalar populations are
eight integers; vector populations are eight three-vectors. These bins are not
the six neighbor ports. Copy a validated seed or use the selected preparation
script; do not reshape six mode amplitudes into eight bins by guessing.

`field_groups` labels existing components; grouping does not create energy, a
force or extra state. A `received` view is already-owned local stock. Count real
resident and in-flight owners once in conservation measurements. A baseline is
immutable background, not automatically a finite source reservoir.

Schema 2 requires `decay` for each spatial field and finite `budget` for each
emission/spatial coupling. It rejects `field_rules` and `spatial_interactions`,
including empty lists. Removing a key without specifying an alternative law is
not a valid way to preserve a requested physical experiment.

## 5. Declare encounters and conservation explicitly

Carried `couplings` perform configured exchanges. `interactions` defines atomic
pair transactions: eligible left/right types, an optional `when`, simultaneous
assignments and invariant expressions. The current conversion extension is
two records to two records, not arbitrary particle creation. See
[LOCAL_CONVERSIONS.md](../../../docs/LOCAL_CONVERSIONS.md).

Field-only encounters use `field_rules`; a rule can jointly assign several
retained/outgoing scalar or vector fields. `spatial_interactions` supplies the
separate field/carrier transaction. Copy syntax from
[LOCAL_FIELD_RULES.md](../../../docs/LOCAL_FIELD_RULES.md) and validate every
reference, assignment target, integer intermediate and unchanged-quantity guard.
Do not insert unsupported participant-count or contact-normal keys.

For the reusable directional candidate, these files have distinct roles:

| File | Edit for |
| --- | --- |
| [law.json](../../../examples/directional-wave/law.json) | Six modes, transverse/bound guards, polarization encounters and streaming |
| [definition.json](../../../examples/directional-wave/definition.json) | Declared energy/momentum, channel directions, assumptions and readouts |
| [experiments.json](../../../examples/directional-wave/experiments.json) | Shape, tick count, link time, seed positions/amplitudes and encounter toggle |
| [display.json](../../../examples/directional-wave/display.json) | Camera and visual options |

The experiment's `values` maps mode names to three-vectors. It is an authoring
format; `prepare.py` expands it into valid `spatial_seeds`. For each mode the
amplitude must be transverse to its direction and every component at most
536870911 in absolute value. A +X amplitude may be `[0,3,0]`, not `[3,0,0]`.
The example defines U as the sum of mode squared magnitudes and P as their
direction-weighted sum, including in-flight modes. The 3Y/2Y opposite pair has
U=13 and P=5X. Its encounter rotates polarization, not trajectories.
See the complete [candidate contract](../../../docs/DIRECTIONAL_WAVE.md).

Native causal/quantum experiments use the separate optional `event_program` in
[NATIVE_QUANTUM_EVENTS.md](../../../docs/NATIVE_QUANTUM_EVENTS.md). Start from its
supplied examples. Their composition with spatial fields is currently rejected.

## 6. Execute, record and display

Headless runs write `initialization.json`, `run.json`, `state.json` and
`events.jsonl`. Read `run.json`: status, completed ticks, source/input identity,
conservation and failure details. An exit code alone is insufficient. The optional
native computation counter measures disturbance cycles; zero is not proof of
zero spatial-field computation. Use the relevant accounting owner.

```sh
python -m event_universe --init artifacts/inputs/my-world.json --output artifacts/my-world-movie --visualize --frame-stride 1
```

`--visualize` records the canonical HTML. `--frame-stride` samples recorded frames
only; every physical tick still executes. To change dynamics, edit initialization
and rerun. To change the camera or playback, render the same saved frames again.
Keep stride 1 when a one-tick encounter matters. No universal GIF exporter is
implied: use the renderer that understands the chosen model and recording.

For the directional-wave comparison, follow the complete
[prepare/run/verify/render commands](../../../docs/DIRECTIONAL_WAVE.md#configure-once-and-reuse).
The renderer accepts `--display path/to/display.json`. Its options are:

| Option | Effect |
| --- | --- |
| `width`, `height` | GIF pixel size; the saved portrait preset is 720 x 980 |
| `frame_ms`, `encounter_ms` | Playback duration per ordinary/encounter frame |
| `show_nodes`, `show_axes` | Lattice nodes and coordinate axes |
| `show_electric`, `show_magnetic` | Derived E/B arrows |
| `show_modes`, `show_travel` | Individual amplitudes and travel-direction arrows |
| `vector_scale` | Display arrow length only |
| `camera_yaw`, `camera_wobble` | Camera angle and oscillation in radians |

Modes remain essential when aggregate E/B cancels. In-flight glyphs are explicitly
distinguished from resident nodes. The current renderer needs two verified cubic
recordings with the same initial state: a free reference and the saved interaction
law. It is not a generic particle movie renderer. Reverify changed recordings.

For phone delivery, decode every GIF frame, inspect overlap/post-encounter/wrap
frames, and provide an accessible file link through the user's requested storage.
A local `127.0.0.1` address belongs to the phone when opened there; it does not point
to the simulation computer. Do not change file-sharing permissions implicitly.

## 7. Common corrections

| Observation | Check |
| --- | --- |
| Unknown key/type/field | Use the strict schema; resolve all references inside final JSON |
| No visible motion | Completed ticks, `hold` versus `move`, rate/denominator, link time, cost delay, frame stride |
| Records meet but pass through | An eligible interaction and its predicate must be configured |
| Charge does not create a force | Add an explicit supported emission/evolution/response law |
| Energy appears to vanish | Include actual transit owners, escaped/decayed amounts where applicable, and keep modes separate |
| Changing speed in a GIF does not change trajectories | Playback and simulated timing are independent settings |
| Nonempty output error | Use a new directory; preserve earlier evidence |
| Local-field/native-event composition fails | Current clocks/ownership contract does not support that combination |

Generated outputs expire under the repository's
[24-hour retention policy](../../../docs/RETENTION.md); active writes are leased.
Original input, reusable definitions and templates stay outside disposable run
directories. Save requested evidence before expiry. A successful experiment proves
only its stated candidate checks, not every real-world law suggested by its names.
