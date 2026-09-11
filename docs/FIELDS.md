# Fields and turning: generic components and model choices

## Field name

The field's user-facing English name is **Computational Field**. This name does
not assert a gravitational law. Scalar values, directional populations and named
channels retain their precise mathematical meanings. Existing Python API names,
serialized field kinds and historical model identifiers are unchanged.

## Delivered-face interface

`fields.faces.face_imbalance(incoming)` is the generic response-input calculation.
Its six integer values are ordered +x, -x, +y, -y, +z, -z and refer to the
source-facing sides of the current cell: a value on +x arrived from the +x
neighbor. They are already delivered local records. The calculation never queries
a neighbor or knows particle identities. A transport that labels travel direction
must reverse the face index exactly once when delivering its packet.

| Part | Contract |
| --- | --- |
| Law | Opposite-face differences `(I[0]-I[1], I[2]-I[3], I[4]-I[5])` |
| Inputs | Six signed 32-bit physical values, already delivered to one cell |
| Evolving state | None in the primitive; the engine owns face records |
| Parameters | No hidden coefficients or source classification |
| Outputs | Three checked 64-bit working differences |
| Response | Existing `FieldTurning` owns impulse scaling, carried residues and exact opposite field impulse |
| Equality | Equal opposite faces produce a zero vector; they do not stop inertial motion |
| Example | `(9,4,2,10,6,6)` produces `(5,-8,0)` |
| Bounds | `MAX_CORE_INT - (-MAX_CORE_INT)` is valid work; an individual input outside its physical bound is rejected |

`scalar.gradient` remains a compatibility name delegating to this one calculation.
This arithmetic refactor alone changes neither scalar transport nor the selected
response policy. A model must explicitly select full-vector response if longitudinal
acceleration is intended. Face data do not identify or subtract an individual
particle's old field.

`scalar_broadcast(value)` validates one scalar snapshot and publishes it on six
outgoing faces. It retains no value internally. The transport injects this pure
publication policy and owns delivery; this function neither reads neighbors nor
chooses when a newly calculated scalar becomes available to another cell.

## Replaceable directional transport law

`fields.streaming.OctantFieldRule` specifies
`emit(populations, sources, source_per_octant, phase) -> outgoing`. One local
eight-integer population record and a resident source count at most K are inputs.
Source strength is an immutable run parameter; phase is a supplied bounded tick.
The output is exactly six packets, each containing eight nonnegative bounded
integers. The engine owns old-snapshot delivery, face orientation and commits.
An implementation has no world access, mutable private history or source maps.

The existing `CausalOctantStream` satisfies this structural interface. It retains
the eight fixed sign sectors while splitting into six outgoing cardinal ports.
It validates old populations before source addition. Generic interface compliance
does not prove conservation, monotone propagation, self-force cancellation or
correct scheduling for a replacement law; each needs independent contract tests.
The existing rule's outward-sign argument concerns its own returning contribution
before periodic wrap. It is not a proof of the complete engine's intervention
cone, which also depends on when response and particle movement commit.

Each local emit uses eight channels and at most three directions per channel;
each destination combines at most six fixed packets. For fixed K these are
constant local bounds. Host frontier sweeps and full simulation storage still grow
with materialized cells. Six incoming response values do not imply that directional
transport must discard its eight-channel memory or that either law is isotropic.

Write each calculation once. The model selects its use, and a field or turning
policy can be replaced without editing the engine or duplicating calculations.
Start each new physical feature with the [extension procedure](PHYSICAL_FEATURES.md).

## Responsibilities

| Component | Responsibility | Current model choice |
| --- | --- | --- |
| `ScalarField` | Weight six neighbors, the local value and the supplied source, retaining division residues | Neighbor weights 1, local weight 0, source from cell occupancy |
| `gradient` | Opposite-neighbor differences on three axes | Use the scalar gradient as turning input |
| `FieldTurning` | Impulse calculation, remainder accumulation and equal-and-opposite momentum exchange | Remove the gradient component along the dominant momentum axis |
| `advance_movement` | Movement budget and one neighbor step | Speed cap from simulation configuration |
| `fields/policies.py` | Source, range and activity calculations | Uniform occupancy source, nonnegative clipping and legacy activity |
| `CurrentFieldModel` | Connect calculations to cell and particle records | Nonnegative field and the choices listed above |

Turning means a momentum response to a field. The current policy removes a
dominant-axis component; it is not a geometric angle rotation and uses no trigonometry.

## Selecting another field using the same calculation

This example creates an experimental composition without running the world.
The local value receives weight 1 alongside the six neighbors. The denominator
comes from the same Config used to audit physical-state remainders.

```python
from event_universe import Config, Simulation
from event_universe.fields import ScalarField

world = Simulation(
    Config(field_den=8),
    field=ScalarField(neighbor_weights=(1, 1, 1, 1, 1, 1), self_weight=1),
)
```

For a different field calculation, implement
`advance(sample, neighbors, *, source, denominator)` under `ScalarFieldRule`.
Inputs are the local value and remainder, six neighbor values, source strength
and denominator. Return `ScalarSample(value, remainder)`. Inheritance is not
required. Values must be bounded integers, with absolute remainder below the denominator.

The component cannot access the world, source identities or history, and retains
no private evolving state. Source calculation happens outside it; the current
model derives the source from occupancy. Zero sample, neighbors and source must
produce a zero sample. This lets the engine skip unaffected empty cells.

A field injected through `field=` stays active when only its remainder changes,
allowing small changes to accumulate across ticks. The original model explicitly
keeps its legacy activity rule for compatibility. `field_activity=` selects an
alternative predicate receiving previous sample, new sample and source count,
and returning `bool`. Available rules live in `fields/policies.py`.

## Selecting another turning policy

The direction function receives momentum and a local field vector and returns
three integers. It only selects the response vector. `FieldTurning` continues to
handle denominators, remainders, bounds and opposite field momentum in one shared implementation.

```python
from event_universe import Simulation
from event_universe.dynamics import FieldTurning
from event_universe.dynamics.turning import full_response

world = Simulation(turning=FieldTurning(select_direction=full_response))
```

This responds to the longitudinal component as well. `field=` and `turning=` can
be supplied together and selected independently. Omitting both preserves the current model.

## Verifying the separation

| Test file | Contract |
| --- | --- |
| `tests/test_scalar_field.py` | Weighted field, signed values, remainders and bounds |
| `tests/test_turning.py` | Different direction policies over shared arithmetic, small impulses and local momentum conservation |
| `tests/test_current_field.py` | Exact current-model field, occupancy source and turning policy |
| `tests/test_field_composition.py` | Replace field and turning through Simulation; reject invalid results before commit |
| `tests/test_architecture.py` | Generic components do not depend on models or worlds; physical arithmetic remains integer |

See `TEST_EXPECTATIONS.md` for movement, geometry and measurement tests and their
numerical inputs and expected results.

The replacement test combines a source-only test field with full-vector response.
It demonstrates composition, not adoption of another physical law. Full-state
comparison against the frozen version remains in place for all 278 ticks of the
three regression scenarios. Every test world run appears in `artifacts/test-runs.html`.

## Current extension limit

The adapter supports one scalar field within a fixed cell schema. The generic
calculation can return negative values, but the current adapter clips a negative
result and its remainder to zero. Vector fields, simultaneous fields or another
sign policy require a separate state contract and engine/measurement adaptation.
An experimental physical law also needs a separate model identity and documentation,
as required by `SIMULATOR_DEFINITIONS.md`.
