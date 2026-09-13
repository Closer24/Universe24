# Historical scalar fields and turning components

The active API defines fields and disturbance types through initialization data.
See [DISTURBANCES.md](DISTURBANCES.md) for the schema, safe expression language,
transport modes, paired coupling and conservation requirements. This supports
bounded scalar and vector fields without adding physical names to the engine.

The component guide below is retained for the explicitly named historical
ScalarSimulation API. It does not define the active generic payload schema.

Write each calculation once. The model selects its use, and a field or turning
policy can be replaced without editing the engine or duplicating calculations.
Start each new physical feature with the [extension procedure](PHYSICAL_FEATURES.md).

## Responsibilities

| Component | Responsibility | Historical scalar choice |
| --- | --- | --- |
| `ScalarField` | Weight six neighbors, the local value and the supplied source, retaining division residues | Neighbor weights 1, local weight 0, source from node occupancy |
| `gradient` | Opposite-neighbor differences on three axes | Use the scalar gradient as turning input |
| `FieldTurning` | Impulse calculation, remainder accumulation and equal-and-opposite momentum exchange | Remove the gradient component along the dominant momentum axis |
| `advance_movement` | Movement budget and one neighbor step | Speed cap from simulation configuration |
| `fields/policies.py` | Source, range and activity calculations | Uniform occupancy source, nonnegative clipping and legacy activity |
| `ScalarFieldModel` | Connect calculations to node and particle records | Nonnegative field and the choices listed above |

Turning means a momentum response to a field. The historical scalar policy removes a
dominant-axis component; it is not a geometric angle rotation and uses no trigonometry.

## Selecting another field using the same calculation

This example creates an experimental composition without running the world.
The local value receives weight 1 alongside the six neighbors. The denominator
comes from the same Config used to audit physical-state remainders.

```python
from event_universe import Config, ScalarSimulation
from event_universe.fields import ScalarField

world = ScalarSimulation(
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
no private evolving state. Source calculation happens outside it; the historical scalar
model derives the source from occupancy. Zero sample, neighbors and source must
produce a zero sample. This lets the engine skip unaffected empty nodes.

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
from event_universe import ScalarSimulation
from event_universe.dynamics import FieldTurning
from event_universe.dynamics.turning import full_response

world = ScalarSimulation(turning=FieldTurning(select_direction=full_response))
```

This responds to the longitudinal component as well. `field=` and `turning=` can
be supplied together and selected independently. Omitting both preserves the current model.

## Verifying the separation

| Test file | Contract |
| --- | --- |
| `tests/test_scalar_field.py` | Weighted field, signed values, remainders and bounds |
| `tests/test_turning.py` | Different direction policies over shared arithmetic, small impulses and local momentum conservation |
| `tests/test_scalar_field_model.py` | Exact current-model field, occupancy source and turning policy |
| `tests/test_field_composition.py` | Replace field and turning through ScalarSimulation; reject invalid results before commit |
| `tests/test_architecture.py` | Generic components do not depend on models or worlds; physical arithmetic remains integer |

See `TEST_EXPECTATIONS.md` for movement, geometry and measurement tests and their
numerical inputs and expected results.

The replacement test combines a source-only test field with full-vector response.
It demonstrates composition, not adoption of another physical law. Full-state
comparisons against the frozen version are historical evidence; the archived
reference is not an active compatibility gate. Current regression assertions
remain. Test worlds are headless unless `--visualize-runs` is requested.

## Scalar extension limit

The adapter supports one scalar field within a fixed node schema. The generic
calculation can return negative values, but the current adapter clips a negative
result and its remainder to zero. This limit is specific to the historical scalar adapter. Vector and simultaneous
fields use the active disturbance contract instead; a different sign policy is
specified by the field definition.
An experimental physical law also needs a separate model identity and documentation,
as required by `SIMULATOR_DEFINITIONS.md`.
