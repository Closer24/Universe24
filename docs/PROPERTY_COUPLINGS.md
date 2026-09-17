# Couplings selected by properties

An executable rule can select a disturbance through the properties it owns.
The engine compiles this compatibility once, then uses the same selection for
scheduling, evaluation and carried fractional/budget state. Types still define
storage layouts and transport; particle labels do not choose physical behavior.

For emissions, spatial couplings and joint spatial interactions, supply exactly
one of `type` or `requires`. For pair couplings and interactions, supply exactly
one of `left_type` or `left_requires`, and exactly one of `right_type` or
`right_requires`. Requirements are unique configured property names, must match
at least one layout, and must include every carrier property read or written by
the rule. Local value predicates can then restrict the configured response.

The complete [property example](../examples/known-entities/property-coupling-probes.json)
uses `requires: ["energy", "momentum", "coupling"]`. Missing properties do not
match through internal zero placeholders. Pair selection still uses two distinct
local slots and declared rule order. When both role orientations fit the same
pair, existing slot order selects one transaction.

Existing exact-type configurations remain supported. Property selection does not
relax transport, ownership, capacity or arithmetic restrictions. The two-to-two `output_types` conversion keeps exact type selectors;
property-selected inputs are admitted by the [N-to-M conversion](LOCAL_CONVERSIONS.md#n-to-m-family-conversion),
whose outputs are always explicit families. Matching properties alone establish neither physical unit compatibility
nor an experimentally valid law.

## Entity configuration

The [physical catalog](ENTITY_CATALOG.md) remains formula-free reference data.
The original 46 representations remain in `representation-probes.json`.
The separate property profile document binds an electron, positron and neutral
control to held finite inventory probes. Coupling values are explicit experiment
data; the compiler does not derive them from catalog identities or measurements.

An optional profile-document `shared_classical` section supplies one common
`model_id`, `claim_level`, `assumptions`, `boundary`, `fields`, `spatial_fields`,
`spatial_seed_values`, `spatial_interactions` and `conservation` declaration.
The compiler copies it once after combining compatible carrier profiles. It
rejects quantum composition, conflicting field ownership and unsupported keys.
Canonical preflight validates the resulting runtime initialization.

```sh
python -m event_universe.entities --catalog examples/known-entities/catalog.json --profiles examples/known-entities/property-coupling-probes.json --entity electron --entity positron --entity electron_neutrino --output-init artifacts/property-input.json
python -m event_universe.configuration_validation artifacts/property-input.json
python -m event_universe --init artifacts/property-input.json --output artifacts/property-run
```

Use fresh output paths. Two independent local reservoirs change the same carrier
energy and momentum through shared property rules. Internal exchanges cancel in
the configured joint inventories and the neutral control remains unchanged. The
[passive local audit](LOCAL_CONSERVATION.md) checks completed owner changes.
This is finite generic exchange, not particle dispersion, Maxwell dynamics, QED,
gravity or a derivation of measured energies.

Tests: property selection (`tests/test_property_couplings.py` (deleted on 2026-09-17), deleted on 2026-09-17),
entity profiles (`tests/test_property_entity_profiles.py` (deleted on 2026-09-17), deleted on 2026-09-17), and
[local conservation](../tests/test_local_conservation.py).
