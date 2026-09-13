# Field-owned photon preparation and frequency

The opt-in [definition](../examples/photon/definition.json) prepares a photon
occupation in the electromagnetic field's existing finite quantum modes. The
[authoring adapter](../examples/photon/prepare.py) validates the reciprocal
catalog association and compiles the field **once**. It does not also compile a
separate photon register system or create a classical carrier.

This is an interim definition/preparation and readout. It is **not a propagating
photon, a frequency-dependent evolution law or an operational frequency detector**.
The earlier half-rate classical photon proxy in
[representation-probes.json](../examples/known-entities/representation-probes.json)
is unchanged. No simulator/schema, speed, force or delay policy is modified.

## Definition and units

| Quantity | Owner and meaning |
| --- | --- |
| `entity_id` / `field_id` | Catalog excitation and its reciprocal parent field |
| `occupations` | Initial number levels in the parent's explicitly supplied quantum registers |
| `frequency.numerator` / `denominator` | Positive integer ratio specifying the selected mode frequency |
| `frequency.reference_frame` | Named preparation reference frame; no inferred rest frame of a photon |
| `frequency.time_unit` | Declared preparation time unit, not a calibrated lattice tick or clock cycle |
| Energy per quantum | Derived readout `h*f`; not an independently editable or transported stock |
| Total excitation energy | `N*h*f` above vacuum, counted once for the occupied field modes |

The default prepares `transverse-1: 1, transverse-2: 0`, with frequency `1/8`
cycles per preparation time unit. Both polarization modes share this selected
frequency. This is illustrative input, not a measured constant or a complete
spatial wave packet. A finite-bandwidth packet needs more than one sharp frequency.

Let the named time unit be T. The frequency unit is 1/T and the energy unit is
h/T, making normalized h exactly one. The default per-quantum and total energy
are therefore both `1/8` of h/T. Doubling frequency makes them `1/4`. Two quanta
at the original frequency have per-quantum energy `1/8` and total energy `1/4`.
Vacuum occupation has zero excitation energy; the unused mode frequency remains
positive. This convention excludes zero-point energy from the excitation readout.

Ratios are reduced exactly. Numerators, denominators and intermediate products
are bounded signed-64-bit positive integers. Overflow, zero frequency, noninteger
inputs, unknown references, extra keys (including an independent `energy`),
missing modes and occupations outside the supplied finite bases are rejected.
The existing n=0,1,2 truncation is a representation limit, not a physical maximum.
The adapter requires ordered number-occupation bases; arbitrary basis labels
cannot silently be interpreted as photon counts. It uses supplied references,
not a name-specific dispatch inside the physical engine.

## Prepare without running a world

From the repository root using the project Python 3.14 environment:

```sh
PYTHONPATH=src python examples/photon/prepare.py --definition examples/photon/definition.json --catalog examples/known-entities/catalog.json --profiles examples/known-entities/representation-probes.json --output artifacts/photon-preparation
```

Choose a new output directory. Inputs are read once and validated before output
creation. The adapter writes:

- `definition.json`: exact original preparation input.
- `initialization.json`: strict ordinary input for the existing quantum backend.
- `preparation.json`: field association, occupations, rational frequency/energy,
  frame, units, limitations and SHA256 bindings to the input bytes.

The example-specific definition is consumed by this adapter, **not directly by
the ordinary runner or general preflight**. The generated initialization passes
the existing shared preflight. Its native event program has two 3-level field
registers, no interaction layers or bindings, no spatial fields and no classical
seeds. No world is advanced by preparation. The manifest is read-only metadata;
it is not loaded by the physical engine or counted as extra field inventory.

Changing only frequency changes the manifest's energy, not the generated
initialization. This intentionally exposes the present missing phase dynamics
rather than pretending that an appended frequency descriptor supplies them.
Keep all three files together; a run of the initialization alone does not load
or dynamically evolve its frequency descriptor.

## Physical interpretation and remaining work

For a definite-frequency photon, E=h*f in the same reference frame; see
[NIST's Planck relation](https://www.nist.gov/si-redefinition/kilogram/kilogram-mass-and-plancks-constant).
The excitation belongs to the electromagnetic quantum field, with two physical
polarizations; see [Tong, QED section 6.2](https://www.damtp.cam.ac.uk/user/tong/qft/qfthtml/S6.html).
Here these are selected representation/readout assumptions, not laws derived by
Universe24. Photon number and photon frequency are separate quantities. Neither
is identified with a freely chosen classical field amplitude.

The register preparation does not implement emission, absorption, spectral phase,
propagation, Maxwell constraints or a local detector. Its address identifies
preparation support only. Frequency measured by another observer cannot be
obtained by relabeling this preparation frequency; signal transfer and clock
calibration must be implemented and tested separately. No photon rest frame is
introduced. General native quantum/spatial-field composition remains unsupported,
so no automatic coupling to the separate directional-delay branch is claimed.

[Tests](../tests/test_photon_configuration.py) cover single ownership, number
levels, exact frequency/energy scaling, unchanged historical proxies, invalid
references and bases, 64-bit bounds, immutable inputs, reproducible output,
no-overwrite behavior and CLI/shared-preflight composition. These are software
acceptance checks of preparation, not experimental photon or relativity evidence.
