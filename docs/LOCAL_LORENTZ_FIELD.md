# Local field impulse and formula-free NodeState

The active `Simulation` can run
[the local pulse configuration](../examples/local_lorentz_field.json) without a
new physical engine or compilation. It uses the existing
[local field framework](LOCAL_FIELD_RULES.md), not the standalone instantaneous
Fourier reference. This candidate is named `configured-local-lorentz-pulse-v1`.
Canonical names follow [the terminology contract](TERMINOLOGY.md).

## Ownership and physical contract

The electric and magnetic Vectors are independently owned spatial stock. A
configured LocalRule forwards each pulse through one +X Link per field interval,
with the configured Link transit time. Initial pulses are explicit initial
conditions, not fields reconstructed from distant particles. They continue to
propagate with no carriers present. Periodic return is real transport.

Each configured carrier samples only fields retained or delivered at its Node.
Its shared initialization law applies the impulse
`delta_p = charge * (electric + cross(momentum / mass, magnetic))`.
The field amplitudes use impulse-per-unit-charge conventions for one configured
interaction interval; the expression does not omit an implicit variable dt.
The same transaction transfers `-delta_p` to a local momentum reservoir. The
combined momentum invariant is exact, including delayed commit. The engine does
not contain a branch for an electron, proton, electric field or Lorentz formula.

Carrier archetypes define properties once; seeds refer to their type. Masses
use 100000 integer units per electron mass: 100000, 183615267 and 183868366.
These approximate the previously used measured ratios to five decimal places;
they are not an exact universal integer mass quantum. The initial momentum is
`[mass, 0, 0]`, giving an exactly representable initial velocity `[1, 0, 0]`.

At the three target Nodes, E is `[0,200000,0]` and B is `[0,0,300000]`. The
independent expected impulses are `[0,+100000,0]` for charge -1,
`[0,-100000,0]` for charge +1, and zero for charge 0. A pulse starts at X=1,
crosses four Links, and the normal-budget run responds at tick 5 at X=5.
There is no response at ticks 1 through 4. Tests isolate E and B independently,
rename fields/types, check autonomy, and reject overflow and nonexact division.

This is a one-shot held-probe experiment. The explicit `armed` property disables
later response before evaluating another division, including after periodic
return. It is an experiment control, not a universal interaction law or a
self-field exclusion solution. Carrier positions are held to isolate the local
impulse; changing momentum does not move a held probe. No claim of physical
Maxwell propagation, radiation, magnetic moments, energy conservation, or
emergent Lorentz behavior is made. The opposite reservoir is an accounting
candidate, not a derived electromagnetic field-momentum density.

## NodeState rule and daily audit

NodeState, disturbance records, field records, pending transactions and Link
packets contain bounded values, fixed records, remainders, indices and scheduling
data. They must not own expression trees, formula strings, arbitrary mappings,
callable laws or initialization definitions. Rule/type indices may refer to the
shared immutable definitions; frozen pending before/after values and deltas are
state, not executable formulas. There is no ban on mathematics in shared generic
field/dynamics components or configured entity laws.

[The canonical read-only guard](../src/event_universe/diagnostics/node_contract.py)
walks the full reachable NodeState graph. [Its tests](../tests/test_node_state_contract.py)
inspect declared state fields as well as live Nodes, pending transactions and
packets, and inject forbidden objects to verify rejection. The old
`diagnostics/node_contract.py` path remains only as an explicit compatibility
shim. New state owner types require review rather than being accepted
automatically. This finite structural guard supplements the existing architecture
and locality audits; it cannot prove arbitrary code behavior.

The daily genericity audit runs the compatibility-selected guard suite and
the local response suite (`tests/test_local_lorentz_field.py` (deleted on 2026-09-17), deleted on 2026-09-17). It also reviews
new dynamic consumers for global source reconstruction and formula duplication.

```text
python -m pytest tests/test_node_state_contract.py tests/test_local_lorentz_field.py
python -m event_universe --init examples/local_lorentz_field.json --output artifacts/local-field
```
