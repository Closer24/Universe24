# Opt-in coherent units

The optional top-level `unit_system` enables exact calibration and dimensional
validation during preparation. Omitted metadata preserves the existing free-text
unit labels and numeric behavior. Strict validation never rewrites an expression,
converts a physical register during stepping, or supplies a force from a name.

The implementation is [units.py](../src/event_universe/units.py), with immutable
metadata in [unit_state.py](../src/event_universe/core/unit_state.py). The
[JSON Schema](../src/event_universe/schemas/unit-system.schema.json) describes
its structure; the canonical initialization validator additionally enforces
unique names, coherent scales and expression dimensions.

## Registry and calibration

```json
{
  "model_id": "si-rational-v1",
  "base_scales": [[1,1000],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1]],
  "units": [
    {"name":"metre", "dimensions":[1,0,0,0,0,0,0], "si_scale":[1,1]},
    {"name":"millimetre", "dimensions":[1,0,0,0,0,0,0], "si_scale":[1,1000]},
    {"name":"count", "dimensions":[0,0,0,0,0,0,0], "si_scale":[1,1]}
  ]
}
```

All seven entries use the order **length, mass, time, electric current,
temperature, amount of substance, luminous intensity**. The corresponding SI
base units are metre, kilogram, second, ampere, kelvin, mole and candela.
Every `base_scales` entry specifies one model base unit in the corresponding
SI unit. `si_scale` specifies one named registry unit in SI base-unit products.
Names are references, not built-in physical interpretations: the registry can
declare arbitrary names with the same dimensions and exact scale.

There are 1 through 64 unique unit names, each at most 128 characters. Every
dimension has exactly seven integer exponents from -16 through 16. Ratios are
positive integer numerator/denominator pairs of at most 256 bits per input
integer, reduced exactly on parsing. Zero denominators, booleans, floats,
unknown keys and unknown field-unit labels are rejected. Negative quantities
belong in field values; calibration scales are positive. Offset units such as
degrees Celsius are unsupported; convert them explicitly during authoring.

`fields[].units` selects a registry name. The existing positive `field.scale`
remains the denominator of the stored value. To keep the unchanged integer
arithmetic numerically consistent, every field must satisfy:

```text
SI amount represented by one raw integer
  = unit.si_scale / field.scale
  = product(base_scales[i] raised to dimensions[i])
```

Thus the example accepts a field declared in metres with `scale: 1000`, or a
field declared in millimetres with `scale: 1`. Both store the same millimetre
quantum. A metre field with `scale: 1` is rejected under this calibration.
Different quanta for the same dimension cannot be mixed merely because their
labels or exponents look compatible. Unused registry entries may describe
other unit scales for authoring conversions.

Length and time calibration also describe coordinate increments and ticks.
They do not change graph neighbors, transit scheduling, model operation costs,
or the Euclidean lengths of diagonal links. Equal link tick counts still need
not mean equal Euclidean speeds on a mixed-length topology. A declared time
field is a local quantity, not an automatic read of scheduler time.

## Dimensional expressions

Plain nonzero scalar/vector literals and matrix coefficients are dimensionless.
Initial defaults, seeds, baselines and finite budgets take the units of their
declared fields. A dimensional constant used inside an expression therefore
needs a declared field with a supplied default; the checker never infers its
units from the assignment target. Literal zero, and expressions proven zero by
simple zero propagation, can be used at any dimension. A comparison against
zero is consequently meaningful for a dimensional quantity.

| Operation | Dimensional contract |
| --- | --- |
| `field`, `received`, `outgoing` | Referenced field dimension |
| `flux` | Referenced scalar field dimension; this is a delivered-amount projection, not amount per second |
| `add`, `sub`, `min`, `max` | Matching dimensions, with compatible zero |
| `eq`, `gt` | Matching input dimensions; dimensionless result |
| `mul`, `dot`, `cross` | Add operand exponents |
| `exact_div`, `ratio` | Subtract denominator exponents; an identically zero denominator is rejected |
| `neg`, `abs`, `sum`, `component`, `transform` | Preserve input dimension |
| `vector` | All nonzero components have the same dimension |
| `rational_whole`, `rational_remainder`, `rational_numerator`, `rational_floor` | Preserve the projected quantity's dimension |
| `rational_denominator`, `rational_direction` | Dimensionless integer bookkeeping or direction |
| `rational_key` | Check its input; allowed only at an invariant root, as an exact comparison representation |

Squared norms use `dot(v,v)`; integer powers use the supported multiplications.
This feature adds no square root, arbitrary power or new physical evaluator
operation. Unknown operations and unsupported syntax are rejected. Syntax
walks keep the existing bounded expression depth and node limits.

All assignments must match the target field, including updates, atomic pair
assignments, retained/outgoing local fields and joint field/carrier transactions.
Exchange and emission amounts match their target quantity. Conditions and
local checks are dimensionless; invariants can compare any consistently formed
quantity before and after a transaction. Specialized rotation requests are
dimensionless turn counts; their target vectors retain their own units. Cost
reporting fields are dimensionless modeled counts.

A movement rate must be a dimensionless ratio: its numerator and dynamic divisor
have matching dimensions, or its numerator is dimensionless when the divisor is
a plain configured integer. A direction expression may have any consistently
formed vector dimension; it supplies routing affinity, not a derived SI
velocity. The checker does not infer a relation between stored momentum and
the realized path.

Native quantum/event programs keep their existing validated dimensionless
coefficients, instrument outcomes and integer control codes. Any mechanical
field receiving an outcome code must be dimensionless. Ordinary mechanical
expressions selected by that code still receive the same dimensional checks.
Unit metadata does not add a Hamiltonian, energy interpretation or new quantum
evolution rule.

## Exact authoring conversions

`parse_unit_system(raw)` returns immutable `UnitSystem` metadata.
`validate_units(initial)` checks parsed JSON inputs and typed API/checkpoint
initial states; it returns immediately for legacy inputs without unit metadata.

`convert_value(value, from_unit, to_unit, system)` accepts an integer or Python
`Fraction` and returns an exact `Fraction`. It checks equal dimensions and uses
the explicitly registered SI scales. It does not round. For the registry above,
converting 3/2 metres to millimetres gives exactly 1500.

`encode_field_value(value, from_unit, field, system)` additionally applies the
field's denominator and returns one external JSON integer component. It rejects
fractional quanta, forbidden negative values and values outside the existing
physical register bound. Call it separately for each vector component. Host
conversion fractions never become physical cell or packet state.

[Focused tests](../tests/test_units.py) check nonzero impulse and kinetic-energy
reference calculations, wrong formulas in every law context, exact conversion,
unit bounds and unchanged calibrated-versus-legacy traces. Those reference
formulas are supplied examples. Dimensional validity alone proves neither
energy conservation nor a physical law: a dimensionally valid equation may
still have the wrong coefficient, locality, dynamics or conservation behavior.
