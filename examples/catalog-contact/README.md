# Catalog particles in the existing causal contact mechanism

[experiment.json](experiment.json) enables all 34 established particle/multiplet
records in the shared [catalog](../known-entities/catalog.json), including all
six quarks and their antiparticles. The hypothetical graviton is not selected.
The default world contains an electron, an up quark and a down quark.

[prepare.py](prepare.py) reads those references and reuses the complete
[causal charge template](../quantum/causal_charge.json). It writes ordinary
initialization JSON and a passive `*.bindings.json` provenance report. This is
host-side configuration preparation: no engine compilation or species-specific
runtime dispatch occurs. The engine and the template's interaction are unchanged.

## What interacts

Each occurrence has three neighboring Nodes in its own disjoint mode domain:
source contact, intermediate mode and capture contact. The existing configured
3:4 mixer and neighboring exchange govern the amplitudes. Locally retained squared
amplitudes weight the existing charge-dependent finite field source. A capture
produces one full localized record; previous field stock remains causal.

Different domains share the ordinary spatial field, but the template supplies
no reciprocal field force or cross-domain quantum gate. The default demonstration
therefore tests three particle/probe interactions, not a mutual quark/electron
collision. A held contact probe is a configured apparatus, not a new species.
The fixed ticket in the authoring file makes this a reproducible acceptance
example, not a statistical measurement of probabilities.

The [candidate contract](../../docs/CAUSAL_QUANTUM_SOURCES.md) remains binding:
source envelopes after measurements are retarded approximations, not the exact
conditional Born distribution. This experiment does not add QCD, weak decays,
spin dynamics, exchange statistics, or physical field/matter energy closure.

## Property ownership

| Data | Representation and effect |
| --- | --- |
| Electric charge | Catalog value encoded in thirds of positive elementary charge; used by the inherited emission expression |
| Mass | Catalog central value encoded in keV/c2 with a maximum half-unit rounding error; preserved inventory, not a mass-dependent propagation law |
| Mass availability | `mass_assigned=0` identifies an unassigned mass; its zero storage placeholder is not a physical zero |
| Spin | `spin_twice` stores the doubled spin quantum number as passive, nonextensive metadata; it is not a spatial spin direction |
| Momentum | The template's `momentum_known=0` remains an explicit unknown; no momentum vector or velocity is inferred from the mode gates |
| Other properties | Full catalog reference, sources, color representation, lifetimes and interaction families remain in the provenance report |

Flavor neutrinos have no single definite catalog rest mass. Their mass is marked
unassigned, whereas theoretical zero photon/gluon mass is explicitly assigned.
The gluon multiplet is one representative binding, not eight implemented color
modes. Quark mass references retain their running/direct-mass conventions and
scales; the probe does not establish isolated free quarks. A sum across those
encoded values is a **reference inventory**, not the invariant mass or energy
of a physical many-particle system. Experimental uncertainties are retained in
the report, separately from encoding error; they are not propagated by the engine.

Each distinct selected entity creates one reusable source type. Repeated placements
reuse it. All use one shared output type with explicit per-domain property values
and one probe type. At most ten occurrences use thirty modes and twelve types.
This is a schema capacity bound, not a promise of inexpensive exact joint-state
evaluation. `--all` creates one small world per record rather than one oversized
world; library coverage is independent of per-world capacity.

## Prepare and run

From the repository root with the project Python environment and `src` on
`PYTHONPATH`:

```sh
python examples/catalog-contact/prepare.py --output artifacts/catalog-inputs
python -m event_universe.configuration_validation artifacts/catalog-inputs/demo.init.json
python -m event_universe --init artifacts/catalog-inputs/demo.init.json --output artifacts/catalog-run
```

Choose particles, including repeated occurrences, without copying their numbers:

```sh
python examples/catalog-contact/prepare.py --entity up_quark --entity antiup_quark --entity photon --output artifacts/quark-inputs
python examples/catalog-contact/prepare.py --all --output artifacts/all-particle-inputs
python -m event_universe --init artifacts/all-particle-inputs/antiup_quark.init.json --output artifacts/antiup-run
```

Use new output directories. `--all` prepares and validates every input without
running worlds. Edit selections, reference scales, finite budgets, tick count and
ticket in `experiment.json`; the shared interaction stays in its original template.
The generated binding report identifies reference descriptors, encoded values,
rounding errors, placements and dependency hashes. Keep it with the initialization.

## Acceptance

[test_catalog_contact.py](../../tests/test_catalog_contact.py) runs each of the
34 bindings through the existing 16-tick contact/gate/capture path, checking
single ownership of encoded charge and mass at every tick, spatial field
accounting, one localized output, property preservation and signed/zero emission.
It also covers the three-domain demo, repeated source types, antimatter signs,
unassigned versus theoretical-zero mass, and capacity/identity rejection.
These checks are world/event audits, not measurements by a local observer.
