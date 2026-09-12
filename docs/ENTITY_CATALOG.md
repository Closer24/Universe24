# Executable entity catalog

Execution scope: this document describes the explicitly supplied-law reference
path (schemas 1/2). Use `ReferenceSimulation`, the `reference_api` loader and
`python -m event_universe.reference_runner` for these examples. Ordinary
initialization accepts only [schema 3 elementary fields](ELEMENTARY_FIELDS.md).
No physical name or JSON flag promotes a reference equation into that path.

An explicit `--representation quantum` now compiles each entry's
[finite quantum profile](QUANTUM_ENTITIES.md) into the native event program.
Classical profiles are unchanged. A field's quantum mode profile is not its
classical spatial-field clock; those two runtime policies are not silently mixed.


All 46 current catalog entries have explicit executable representation profiles:
11 field families and 35 particle or multiplet records. This is the scope of this
inventory, not a claim that every physical entity in nature is known or simulated.
The sourced limitations remain in [PHYSICAL_ENTITIES.md](PHYSICAL_ENTITIES.md)
and each entry's `missing_capabilities`.

`event_universe.entities` is a host-side authoring adapter. It selects profiles
by ID, combines exactly compatible field declarations, assembles seed positions,
and delegates the result to the ordinary initialization validator. It neither
executes Python supplied by data nor branches on physical names. The generated
JSON works with the existing CLI and configuration workspace without another
engine. Catalog IDs select data only.

## Run selected entities

From the checkout with the project interpreter:

```sh
python -m event_universe.entities --catalog examples/known-entities/catalog.json --entity electron --entity positron --entity electromagnetic_field --output-init artifacts/selected-entities.json
python -m event_universe --init artifacts/selected-entities.json --output artifacts/selected-entities-run --visualize
```

Use new output paths. The first command only writes configuration; the second
runs that exact configuration and uses the existing recorded HTML generator.
`compile_entities(catalog, entity_ids, shape=(9,9,9), ticks=4, link_ticks=1)` is
the corresponding Python authoring API. Original profiles stay in Git; generated
inputs and reports are experiment outputs.

## Profile data and limits

Every `executable_profile` declares its `kind`, ordinary `fields`, exact
`seed_values`, nonempty `assumptions` and `claim_level: representation_probe`.
Carrier profiles supply an ordinary `disturbance` definition. Local-field
profiles supply ordered `components`, `spatial_fields` and `field_rules` using
the existing schema. Rules are explicit data, not inferred from labels.

The supplied carrier probes copy abstract inventory, signed charge and a momentum
register under an explicit half-rate movement policy. Inventory is not mass or
energy. The rate is not inferred from species, momentum or mass. In particular,
the photon entry is a kinematic record probe, not a physical light-speed photon.
There is no numerical neutrino mass assumption or negative antimatter mass.

The supplied field probes copy each register toward +X and clear its previous
owner, preserving retained-plus-outgoing component totals. Their fixed direction,
initial values and link time are explicit experiment choices. The E/B sample
registers do not constitute a physical Maxwell wave. Strong-field registers omit
gauge evolution; spinor registers omit their transformations and statistics;
metric registers do not guarantee a valid spacetime metric. Computational and
dark-sector profiles retain their hypothesis status. The computational register
probe does not add a new coupling to the computation clock.

Limits remain 16 fields, 16 types and fixed local slot/rule capacities per world.
Each entry compiles separately. Compatible subsets compose; selecting the full
catalog in one world fails explicitly. Duplicate IDs, conflicting shared field
definitions, duplicate spatial ownership, malformed profiles and invalid integer
values fail before execution. JSON parsing rejects duplicate keys.

This adapter supports the ordinary schema's operations; it is not an independent
proof that arbitrary user-authored expressions obey the elementary-emergence
restriction. The supplied new profiles generate updates by copy/clear only.

## Conversions and evidence

The engine additionally accepts the data-defined
[bounded local conversion](LOCAL_CONVERSIONS.md) extension. Its current scope
is exactly two records to two records with full explicit output assignments and
exact declared conservation. It does not create arbitrary reaction products.
Use the standalone `examples/known-entities/conversion.json` through the same
runner. This example deliberately does not label its configured transformation
as matter annihilation.

`tests/test_entity_compiler.py` validates every profile, composed carrier/vector
and multi-scalar transport, name independence and rejection boundaries. Shared
mechanisms are exercised by representative active worlds instead of running
35 identical carrier dynamics tests. `tests/test_local_conversions.py` checks
the changed conversion contract. Physical emergence remains unestablished.
