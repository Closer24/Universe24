# Local unit-excitation coupling probe

`unit-local-excitation-field-transducer-v1` connects independently owned internal
and spatial states through
existing [local field/carrier transactions](LOCAL_FIELD_RULES.md#joint-fieldcarrier-transactions).
It is a finite candidate, not electron dynamics or a quantum photon model.
The [catalog](ENTITY_CATALOG.md) remains a descriptive reference: its field
membership and interaction labels do not choose this law.

## Contract and owners

| Part | Declared contract |
| --- | --- |
| Internal excitation | One held carrier owns transverse vector `internal`, vector `recoil` and selector `coupling` |
| Spatial excitation | One local spatial field owns transverse vector `amplitude`; free stock travels through +X links |
| Internal states | Each amplitude is empty or one of +Y, -Y, +Z, -Z; this finite occupation is an assumption |
| Coupling selector | -1, 0 or +1; it changes the exchange rule, not field membership |
| Receiver | A local scalar `gate`: 0 forwards, 1 holds awaiting nonzero input, 2 explicitly initiates release from internal stock |
| Inputs | Owned local state and information that has completed its link transit |
| Commit | Joint internal, field, recoil and gate changes pass together or fail before that transaction changes any owner |
| World | At most one held receiver, at most one initial nonzero spatial packet, zero baselines, no sources, periodic 3D domain |
| Lifetime | One configured capture/release; inspect the first encounter before a returned packet overlaps other same-mode stock |

The same configured rules execute at every node. The receiver's gate is physical
local control state; it is not a global clock or a detector outside the model.
An emission trigger (gate 2) admits no nonzero initial spatial packet, even at
the receiver, so a delayed emission cannot overlap an independently seeded pulse.
A gate without a carrier holds incoming stock. A zero coupling at an occupied
receiver releases the incoming packet unchanged after the local commit.

## Elementary change and independent expectations

Positive coupling copies the incoming field vector into the carrier and reverses
the previous internal vector into the field. Negative coupling reverses those
sign choices; zero coupling preserves both vectors. Absorption transfers one +X
recoil unit to the carrier; emission transfers one -X unit; exchanging two occupied
states transfers no recoil. The assignments use elementary copies, sign changes
and fixed integer transfers. Squared norms are used for activation and checks,
not to calculate a force or a replacement recoil from a continuum equation.

| Case, initially zero recoil | Internal after | Field after | Recoil after |
| --- | --- | --- | --- |
| Positive absorption: internal 0, field Y | Y | 0 | +X |
| Negative absorption: internal 0, field Y | -Y | 0 | +X |
| Zero coupling: internal 0, field Y | 0 | Y | 0 |
| Positive emission: internal Y, field 0 | 0 | -Y | -X |
| Positive occupied exchange: internal Y, field Z | Z | -Y | 0 |

For the admitted unit states, the candidate defines normalized total occupation
`U = |internal|^2 + sum(|amplitude_owner|^2)` and recoil/flux balance
`P = recoil + X * sum(|amplitude_owner|^2)`.
These are explicit acceptance definitions, not measured particle energies.
Every resident or in-flight field owner is counted once. Received samples,
frozen proposals and observer archives are views, not additional inventory.
The opposite signed local exchange restores the amplitude/recoil state when
explicitly supplied the previous outgoing field and rearmed gate. Rearming is a
separate initial-condition experiment, not autonomous repeated absorption.

## Event order and capture

The current engine samples local field input before that phase's field rules.
Unconditional streaming can therefore move the sampled stock away before the
carrier transaction commits. A nonlinear guard must reject such a stale change.
This example retains stock while the gate is positive. The joint commit clears
the gate, and a following field phase releases any remaining amplitude.

A longer computation delay leaves original internal and field values owned and
unchanged until commit. Link transit and computation delay are distinct modeled
times. Evidence is a world/event audit of source, arrival and commit events;
it is not an observer image or a claim about proper time.

An additional same-mode arrival during the hold is outside the single-packet
input envelope. The engine combines those amplitudes before the joint guard;
squared-norm totals can already change at that invalid arrival. A later rejection
shows that the stale joint transaction cannot partially commit, not that all
interference or arbitrary packet overlap conserves this candidate's U/P.

## Prepare, validate and run

The [saved law](../examples/coupled-excitations/law.json),
[case data](../examples/coupled-excitations/experiments.json) and
[definition](../examples/coupled-excitations/definition.json) have separate owners.
The [adapter](../examples/coupled-excitations/prepare.py) assembles ordinary JSON
and checks the candidate's input envelope. The standard preflight checks the
resulting initialization schema; these are different validation scopes.

```sh
python examples/coupled-excitations/prepare.py --case incoming_positive --output artifacts/coupling-input.json
python -m event_universe.configuration_validation artifacts/coupling-input.json
python -m event_universe --init artifacts/coupling-input.json --output artifacts/coupling-run
```

Use new output paths. No simulator rebuild or visualization is required.
Acceptance tests (`tests/test_coupled_excitations.py` (deleted on 2026-09-17), deleted on 2026-09-17) exercise the configured
rules with independent expected states; the test-selection gate tracks changes
to the saved law and all authoring resources.

## Physical scope

The held carrier is a receiver with an internal state and a recoil inventory.
Its recoil does not determine a trajectory or satisfy a massive dispersion law.
The selected direction, discrete occupation, capture gate and exchange rule are
supplied hypotheses. Spinors, fermion statistics, a quantum electromagnetic field,
charge/current continuity, Maxwell dynamics, transition probabilities and QED
remain unimplemented by this probe. A passing finite experiment establishes its
local exchange mechanism only; it does not derive electron or photon properties.
