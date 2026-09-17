# Physical entity catalog and explicit representation probes

Optional [property coupling profiles](PROPERTY_COUPLINGS.md) add one explicit
`shared_classical` law and local energy/momentum measurements to compatible
carrier representations. Physical reference metadata remains formula-free.

[catalog.json](../examples/known-entities/catalog.json) is a version 2 physical
reference. It contains identities, sourced properties and possible interaction
families, with no executable profiles, update formulas, rates or Hamiltonians.
Measured properties are external comparison targets; the engine does not load
them as laws or convert them into lattice parameters.

The catalog covers 11 field families, 35 particle or multiplet records, and 14
composite, collective and gravitational disturbance families. The established
Standard Model species include antiparticles. Gravity, unresolved dark-sector
identity and project hypotheses retain distinct evidence statuses. Composite
spectra and material excitations have no finite exhaustive list: family entries
state their scope and point to specialist catalogs. This is neither a complete
list of nature nor a claim that these entities have emerged in the simulator.
See [physical support and limitations](PHYSICAL_ENTITIES.md).

## Reference data contract

The numerical snapshot uses PDG 2026 summary tables. Individually cited reviews
retain their own edition; electron magnetic moment uses CODATA 2022 explicitly.
Shared constants and units are owned by [reference units](REFERENCE_UNITS.md),
including bounded Scalar/Vector authoring and the distinction between model
timing h and Planck's constant of action.

Every entity declares sourced `physical_properties` and `interaction_ids`.
Fields link to `excitation_ids`; elementary particles link back with `field_ids`.
Bound states describe their constituents separately. Particle/antiparticle
relations are reciprocal, with conjugate electric charge and equal spin and
mass status. Neutrino flavor records do not invent absolute masses or settle
the Dirac/Majorana question.

A physical property has a `status`, `sources` and a value or explicit context.
Measurements use decimal strings, a unit and measurement context. Uncertainty,
precision, bounds and confidence levels are recorded when supplied by the source;
unknown values are not zero. Quark mass conventions and medium-dependent
collective properties must retain their context. Decimal parsing is confined to
host-side reference validation, outside physical state and integer operations.

Intrinsic charge and doubled spin use `metadata_key` to reference their one
canonical integer value. A property with `status: reference` and `entity_id`
refers to the same property on another entity, such as an antiparticle's mass.
Reference cycles and unresolved identities are rejected.

Signed references may add `reference_sign: -1`, for example conjugate magnetic
moments using the same spin-axis convention. Mass/lifetime/width cannot acquire
a negative sign. `resolve_property` returns the resolved value with an explicit
reference chain and original target status; an antiparticle inference is not
reclassified as an independent measurement. Its resolved report is not itself a
catalog property descriptor. Asymmetric uncertainties require both
`uncertainty_plus_decimal` and `uncertainty_minus_decimal`. Width-based entries
use lifetime `not_supplied`, rather than claiming lifetime is inapplicable.

The 17 `interaction_families` specify participants, mediators, conditions and
evidence status. The 33 `representative_channels` list incoming and outgoing
entities; repeated IDs encode multiplicity. They are descriptive possibilities,
not an exhaustive reaction table or a request to perform a conversion. Kinematic
availability, environment and selection rules still matter. No cross section,
branching probability or dynamical law is inferred from a listed channel.

Validate the reference without creating a simulation:

```sh
python -m event_universe.entity_catalog examples/known-entities/catalog.json
```

`validate_catalog(catalog)` checks the schema, citations, measurements, aliases,
reciprocal links, channel membership and electric-charge balance where all
participants carry a definite catalog charge. It rejects executable content.
These structural checks do not prove scientific completeness or measured values;
independent inventory and physical-property tests supplement them.

## Run a selected representation experiment

The catalog contact experiment (`examples/catalog-contact`), which bound the 34
established particle/multiplet records to the causal quantum source and contact
mechanism, was deleted on 2026-09-17 with the shared quantum resource. No engine
law is added by selecting an entity.

The original 46 classical probes live in
[representation-probes.json](../examples/known-entities/representation-probes.json).
Its `profiles` array identifies each row by `entity_id`, separately from the
physical reference. There is no automatic profile lookup or species dispatch.

```sh
python -m event_universe.entities --catalog examples/known-entities/catalog.json --profiles examples/known-entities/representation-probes.json --entity electron --entity positron --entity electromagnetic_field --output-init artifacts/selected-entities.json
python -m event_universe --init artifacts/selected-entities.json --output artifacts/selected-entities-run
```

Use new output paths. Add `--visualize` to the
runner only when visual output is wanted. The Python API is
`compile_entities(catalog, entity_ids, profiles=profiles, shape=(9,9,9), ticks=4, link_ticks=1)`.
Both documents must be passed explicitly. Legacy version 1 catalogs retain their
embedded-profile API; mixing embedded and separate profiles is rejected.

`event_universe.entities` only selects profiles, combines compatible field
declarations, places seeds and delegates to ordinary initialization validation.
It does not use reference masses, spins or possible interactions to derive any
runtime operation. A family without a supplied experiment profile cannot compile;
absence of a profile never creates an implicit physical model.

Each classical profile declares `kind`, `fields`, `seed_values`, nonempty
`assumptions` and `claim_level: representation_probe`. Carrier profiles add a
`disturbance`; field probes declare their components and explicit local rules.
Duplicate or orphan profile IDs, incompatible
declarations, malformed profiles and exceeded runtime capacities fail explicitly.
Subset profile documents are allowed when every selected entity is covered.

For whole-library checks, `entities.validate_profiles(catalog, profiles)` validates
every supplied profile independently and returns profile/classical
counts. Use the [common preflight CLI](CONFIGURATION_VALIDATION.md) for file reports
and explicit dependencies. It checks unselected rows as well; validate a compiled
multi-entity initialization separately for its combined capacity and compatibility.

The carrier probes copy inventory, charge and momentum registers with an explicit
half-rate movement policy. Inventory is not physical mass or energy. The photon
probe is not a physical light-speed photon. Field probes copy registers toward
+X and clear the previous owner. They do not establish Maxwell waves, gauge
dynamics, spinor transformations or a valid spacetime metric. Their supplied
updates remain elementary copy/clear operations. Limits remain 16 fields and
16 types per world; compatible subsets compose, not the full catalog at once.

## Evidence and conversion limits

`tests/test_entity_catalog.py` checks reference coverage, sourced physical
properties and invalid metadata. `tests/test_entity_compiler.py` checks explicit
profile selection, legacy compatibility, rejection cases and active representative
worlds. Small-space consumers use the same separated profiles.
Changing reference metadata must not change compiled laws or resulting physics.

The separate [bounded local conversion](LOCAL_CONVERSIONS.md) interface supports
explicit two-record to two-record assignments and declared conservation. The
standalone `examples/known-entities/conversion.json` is an abstract conversion
probe, not a realization of the catalog's particle reactions. Physical emergence
remains unestablished.
