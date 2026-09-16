# Physical reference units and integer authoring

The project-wide [lossless remainder requirement](ARCHITECTURE.md#lossless-remainder-ownership)
is binding for the intended model. The existing behaviors documented below are
not automatically compliant: preserve their evidence and report the mapped gaps,
without silently changing runtime semantics through documentation.

The canonical shared registry is
[physical-units.json](../examples/known-entities/physical-units.json).
It defines SI base dimensions, named unit scales and sourced constants once.
[reference_units.py](../src/event_universe/reference_units.py) resolves those
definitions and prepares bounded Scalar/Vector values. It is a host authoring
tool, outside physical stepping, costs, delays and state. It is not an automatic
unit conversion inside the engine or a new physical law.

## Constants, units and model timing

### Minimum model time and output delay

Use `delta_t_min` (Delta t_min) for the minimum model time interval; no SI value
is assigned. Physical h and hbar are action constants, not time intervals.
In the Node design, the locally received computation field sets
each output delay through a defined local rule in integer multiples of this
interval, not through host load or an inferred hbar/energy law.

For additional waiting before dispatch, define
`tau_wait(n,p) = k_wait(n,p) * delta_t_min`, with a nonnegative integer count.
Waiting and Link transit are distinct. **Open convention:** does a generic `k`
already include transit? Only if transit is one tick and `k` counts additional
waiting is total elapsed time `(k + 1) * delta_t_min`. Do not add one
unconditionally or count transit twice. Zero waiting never permits same-tick
Link traversal; preserve current/future queues and causal readiness.

Speed `c` has dimensions length/time. A calibrated Link speed needs its length
and transit duration; neither a numerical tick scale nor a new physical law
is inferred here. This is the canonical timing clarification for the target
design; existing executable profile timing below remains unchanged.

### Mass encoding, rest phase and Node delay

These are three distinct quantities. The approved documentation separation does
not choose a mass-dependent latency law or establish universal mass quantization.

| Quantity | Meaning and required record |
| --- | --- |
| Reference rest mass | Published value, unit, experimental uncertainty, context and source; preserve them independently of encoding |
| Encoded mass | `m_encoded = N * mass_unit`, with bounded nonnegative integer N, chosen unit, explicit storage bounds and representation error against the selected reference central value |
| Rest phase | A physical phase reference, separate from local transaction completion or transport retention |
| Node delay | `tau_node = k * delta_t_min`, with bounded nonnegative k and a specified local policy; its functional form remains OPEN |

For a definite rest energy, the standard phase rate magnitude is
`omega_0 = m*c^2/hbar`; its full phase period is `T_0 = h/(m*c^2)`.
Increasing mass increases this rate and shortens the period; neither expression
defines processing latency. Motion also depends on momentum, not mass alone.
A completed Node-cycle count is not an established proper-time mapping.
See [Feynman III, sections 7-1 and 7-2](https://www.feynmanlectures.caltech.edu/III_07.html).
These are physical comparison relations, not implemented phase operators.

Writing `m = N * mass_unit` selects a bounded numerical representation. It does
not assert that all physical masses are exact integer multiples of one universal
mass quantum. Measurement uncertainty, representation error and model error are
different records. Changing the chosen mass unit must not change claimed physical
behavior; convert parameters consistently or reject an unsupported conversion.
Nonexact encoding requires an explicit bounded remainder/scale owner or rejection,
not an unreported rounding step under the target lossless contract.

The [mass/phase/delay JSON design](examples/mass-phase-delay.design.json) is a
non-executable proposal: every key is prospective, not an implemented catalog or
initialization schema. It references the existing electron mass record without
copying its numerical value. Choosing that central value as one unit makes N=1
and representation error zero by definition; its experimental uncertainty is
still retained. This example does not establish a shared exact unit for all
other masses. Null storage bounds, code mapping, phase mapping and delay fields
are unresolved decisions, not runtime defaults.

The delay's functional form, massless behavior and whether it represents holding
transport output or completing a joint transaction remain OPEN. The existing
k/Link-transit ambiguity above is unchanged. No illustrative linear mass-delay
formula is selected here. Delay changes must preserve causal arrivals, complete
joint ownership, exact arithmetic and all remainders. This proposal neither
changes current profiles nor blocks independent property-transport or finite
wave benchmarks whose own contracts are already specified.

### Existing profiles and physical constants

The registry distinguishes exact SI defining constants (`speed_of_light`,
`planck_h`, `elementary_charge`, `boltzmann_k`) from measured constants
(`newton_G`, `fine_structure_alpha`, magnetic moment units). All cite
[NIST CODATA 2022](https://physics.nist.gov/cuu/Constants/Table/allascii.txt).
The unit dependency graph derives eV, MeV/c2, charge thirds and other units from
these definitions without repeating the defining numerical constants.

`planck_h` is an action, with units J s. The model's timing interval h is
not this constant. The opt-in [Node processor](NODE_VECTOR_PROCESSOR.md) uses
`link_ticks: 1`, with k local h steps followed by one further hop. Existing
profiles retain configured `link_ticks` and their [cost-budget delay](SPATIAL_COMPUTATION_DELAY.md).
No SI time per tick or SI length per Link is assumed by the registry.
Physical link speed would require both scales and division by `link_ticks`.
Even after calibration, a candidate wave need not travel at the link speed.

A constant may be a chosen unit: one value in `planck_h` is one Planck constant
of action; one value in `speed_of_light` is one physical vacuum light speed.
Their different dimensions prohibit converting action to time or speed to mass.
No known universal rest-mass quantum makes every particle mass an integer
multiple. A chosen field scale is a representation convention, not evidence of
such a law. A finite decimal approximation to hbar is not declared exact.

The seven dimension exponents follow length, mass, time, current, temperature,
amount and luminous intensity. This ordering is compatible with the proposed
`si-rational-v1` convention in open PR56; that unmerged runtime interface is not
activated or duplicated here. The central constants registry can later supply
its explicit calibration inputs.

## Author a Scalar or a Vector

Field declarations retain the existing `units`, `scale`, `components` and
`signed` settings. The encoded integer divided by `scale` is the value in the
declared unit. Scale and payload must fit the existing runtime bounds.

```sh
python -m event_universe.reference_units --registry examples/known-entities/physical-units.json --catalog examples/known-entities/catalog.json --entity electron --field-unit keV/c2 --unsigned --max-error 0.0005
python -m event_universe.reference_units --registry examples/known-entities/physical-units.json --catalog examples/known-entities/catalog.json --entity electron --property electric_charge --field-unit "elementary charge" --scale 3
python -m event_universe.reference_units --registry examples/known-entities/physical-units.json --value 1.25 -2.5 0 --from-unit MeV/c --field-unit keV/c
python -m event_universe.reference_units --registry examples/known-entities/physical-units.json --value 1 --from-unit planck_h --field-unit planck_h
```

The mass command emits 511, with its signed encoding error in the source
unit MeV/c2. The charge command emits -3. The vector command emits `[1250, -2500, 0]` exactly. The final command emits one
unit of action. Commands print JSON; they neither overwrite configurations nor
run a simulation. Copy only `value` into the matching field's initialization,
retain its declared unit/scale and save the report as experiment evidence.

The Python API `encode_components(registry, values, source_unit, field,
max_error=None)` accepts decimal strings and a full existing field declaration.
This physical-quantity encoder supports one or three components. The opt-in Node
processor also supports wider generic registers; their preparation is outside
this encoder's spatial Scalar/Vector scope. Unknown units, incompatible dimensions,
negative unsigned inputs, overflow and shape errors fail before returning a value.
No implicit rounding occurs. An explicit `max_error` permits nearest rounding,
with ties away from zero, only within that per-component error budget expressed
in source units. Runtime intermediate arithmetic still requires its ordinary
bounds checks; fitting an initial payload does not certify a future calculation.

Reports retain exact rational encoding errors and an SI component quantum.
These describe selected decimal central values. `measured_scale_dependencies`
identifies measured constants involved in calibration;
`experimental_uncertainty_propagated: false` makes clear that experimental
uncertainty and correlations were not propagated. Encoding error, measurement
uncertainty and model error are distinct. Tiny SI values may round to zero only
when an explicit error budget permits it; inspect the report.

## Match the vector meaning

| Quantity | Stored shape and interpretation |
| --- | --- |
| Rest mass, electric charge, energy | Scalar; electric charge sign is not a spatial direction |
| Momentum, velocity, electric field | Three-component polar Vector with an explicit basis |
| Magnetic field, magnetic moment, classical angular momentum | Three-component axial Vector; reflections require its axial transformation convention |
| `twice_spin` | Intrinsic identity metadata, not a classical spin orientation |
| Directional wave amplitudes | One three-component Vector per configured propagation Port |
| Spinor, color gauge state, spacetime metric | Not implemented merely by placing numbers into one three-vector |

All components share one unit and scale. The converter preserves component order
and signs; it does not rotate a vector or choose a Port. Preparation must supply
orientation and the model must implement appropriate transformations. A signed
magnetic moment in the catalog is its value for maximal spin projection along
the quantization axis; it does not prescribe a three-vector quantum state.

Six Ports are six transfer directions, not a six-component vector. In the
[directional-wave candidate](DIRECTIONAL_WAVE.md), different modes can cancel the
aggregate E/B readout while retaining nonzero owned energy. Do not replace its
mode-based accounting with a sum-vector norm, or label its normalized readouts
as SI fields without an independently justified calibration. A unit name or
constant does not enable a Lorentz force or gravitational momentum change.

## Validation and boundaries

`tests/test_reference_units.py` checks dimensions, defining constants, conjugate
magnetic conversion, vector signs, exact rejection, explicit error budgets and
runtime bounds. A 40-tick periodic transport probe carries encoded electron,
proton and neutron reference masses and a signed three-vector through the
existing generic profiles with two-tick Links. Mass inventory, charge and vector
components remain conserved. Its configured motion is a transport test, not a
mass-dependent physical trajectory.

Reference parsing uses bounded-size exact rationals only during authoring.
The registry and rational reports are never inserted into physical state. The
engine continues to receive integers and use its existing local arithmetic.
Catalog changes also retain the existing tests that metadata cannot change
compiled laws. Electromagnetic, weak, strong and gravitational dynamics still
need their own explicit laws and independent physical validation.
