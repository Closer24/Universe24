# Particle interaction probes: charge, recoil and proton emission

Three probes composed from existing rules only. Labels such as proton,
electron and charge are configuration data: the engine dispatches no law by
name, and no physical constant, unit or species is identified. Every number is
a read-only world/event audit at host lattice coordinates.

```sh
python examples/particle-interactions/run_experiments.py --output artifacts/particle-interactions
```

## Mechanism

Each charged body emits a signed [straight-ray field](../../docs/SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1)
of its own, `charge x 512` units per tick over 512 golden-spiral headings, and
responds to the other bodies' fields through an `exchange` coupling whose
amount is `-(charge x flux)`. The delivered flux points away from the emitter,
so like charges push apart and unlike charges pull together. A body moves along
its momentum at `min(1, |p| / (16 x mass))` hops per tick.

A moving body reaches the next Node together with the rays it emitted one tick
earlier, and without any exclusion it pushed itself forward regardless of the
other body's sign. The field is shared by all charges and uses the local
[`self_exclusion`](../../docs/SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1)
rule: a departing emitter subtracts the rays of its own departure cycle from
the flux it samples on arrival, from its own registers only, in work bounded by
`rays_per_tick`. Self-field returning from any other distance is not excluded;
a general self-field law is still the open hypothesis named in `POSTULATES.md`.

The third probe uses no field. Two held records, a bound proton and a residual
core, share a Node; a local update counts ticks on the proton, and a
[two-record conversion](../../docs/LOCAL_CONVERSIONS.md) fires when the count
passes a delay. Its assignments give the free proton momentum `(+P, 0, 0)` and
the recoiling core `(-P, 0, 0)`; declared invariants keep total momentum and
total mass exact.

## Observed outcomes on 2026-09-13

21-cubed open world, runtime source SHA-256 `53710d462fd4...` (full value in
`summary.json`), Python 3.14, headless. `tests/test_particle_interactions.py`
checks the same statements with six axis rays per body on a 15-cubed world.

### Head-on encounter of two equal bodies, mass 16, momentum +-128, from x = -+7

| Pair | Closest approach | What followed |
| --- | --- | --- |
| like charges +3, +3 | distance 2 at tick 13 | both reverse: left back at -7 by tick 21, right at +6, then they leave through the boundary |
| opposite charges +3, -3 | distance 0 at tick 14 | they meet at the same Node and continue through each other |
| neutral 0, 0 | distance 0 at tick 14 | unchanged momenta, half a hop per tick throughout |

Like charges never share a Node: the head-on backscatter of a repulsive
inverse-square kick. The opposite pair reaches the Node together two ticks
earlier than by inertia alone, then keeps going; there is no binding, because
the kicks near the meeting point are as large inward as outward and the rule
carries no energy.

### Light body (mass 1) beside a heavy one (mass 256, charge +3), five links apart

| Light charge | Light body | Heavy body |
| --- | --- | --- |
| -3 | pulled in from tick 7, momentum -180 at tick 10, passes the heavy body and leaves at -999 | pulled after it with +1143 |
| +3 | pushed out from tick 7, leaves with +45 | recoils to -162 |

The signs follow the charge product. Near the heavy body the flux through one
Node is a large fraction of the whole emission, so the attractive case ends with
both bodies flying apart at the speed cap with momenta far beyond their initial
state: no energy is represented, and nothing bounds a kick at one link. The
momentum kicks are exchanged with each body's local momentum field, not between
the bodies, so equal and opposite recoil holds only while both bodies stay in
each other's field.

### Timed proton emission from a bound pair

| Tick | Free proton (mass 1) offset, momentum | Recoiling core (mass 3) offset, momentum |
| --- | --- | --- |
| 9 | still bound | 0, -24 |
| 10 | 1, +24 | 0, -24 |
| 14 | 5, +24 | -2, -24 |
| 18 | 9, +24 | -4, -24 |

The conversion fires on the cycle after the counter passes 8. The proton leaves
at one hop per tick, the triple-mass core at one third, momentum sums to zero
and mass to 4 until both leave the open boundary. This is a declared output
law with exact invariants, not a decay rate or a nuclear model.

## Conclusion

Signed straight-ray fields plus an exchange coupling give the charge-sign
structure of electrostatics: repulsion, attraction, and no effect on neutral
bodies, with head-on backscatter for like charges. Two things are missing for
more than that: a representation of energy, without which close encounters are
unbounded, and a local rule that keeps a body from responding to its own field
without a separate field per body. Proton emission is a configured conversion
that conserves what its invariants declare and nothing more.

