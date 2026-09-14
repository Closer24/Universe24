# Particle interaction probes: charge, recoil, proton emission and radiation pressure

Four probes composed from existing rules only. Labels such as proton,
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

The fourth probe closes the energy ledger. A lamp pays every ray quantum from
its own `quanta` stock and recoils by `amount x heading`; a sail absorbs the
quanta that reach it, banking each amount and taking its momentum; the
[conservation audit](../../docs/LOCAL_CONSERVATION.md) measures rays as quanta
and checks every event. Absorption pushes the sail away from the lamp: this is
radiation pressure, not attraction. The lamp fires 252 headings every tick, 126
golden-spiral headings paired with their exact negatives, so the integer
heading set sums to zero and the recoil of one full sweep cancels exactly. The
audit re-measures every active Node and packet on every event, so this probe
stays at 12 ticks; the 512-heading, 40-tick version did not finish in hours.

The third probe uses no field. Two held records, a bound proton and a residual
core, share a Node; a local update counts ticks on the proton, and a
[two-record conversion](../../docs/LOCAL_CONVERSIONS.md) fires when the count
passes a delay. Its assignments give the free proton momentum `(+P, 0, 0)` and
the recoiling core `(-P, 0, 0)`; declared invariants keep total momentum and
total mass exact.

## Observed outcomes on 2026-09-13

21-cubed open world, one shared signed field with `self_exclusion`, runtime
source SHA-256 `2ab09f723c8a...` (full value in `summary.json`), Python 3.14,
headless. A control run with one field per body and no exclusion (source
`53710d462fd4...`) gave the same head-on and emission tables, and the run at
source `f668e71273fd...` that added funded emission, absorption and the ray
audit repeated all three tables below unchanged. `tests/test_particle_interactions.py`
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
| -3 | pulled in from tick 7, momentum -477 at tick 10, passes the heavy body and leaves at -1836 | pulled after it to +324, settling at +243 as the light body recedes |
| +3 | pushed out from tick 7, leaves with +297 | recoils to -162 |

The signs follow the charge product. Near the heavy body the flux through one
Node is a large fraction of the whole emission, so the attractive case ends with
the light body flying through and away at the speed cap with momentum far
beyond its initial state: no energy is represented, and nothing bounds a kick at
one link. The control run without self exclusion but with separate fields gave
the heavy body a larger drag (+1143); with one shared field its residual
self-field, rays returning from farther than one link, is not excluded. The
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

### Radiation pressure: a funded lamp and an absorbing sail, four links apart

Lamp of mass 4096 with a stock of 200,000 quanta, firing 252 mirrored headings
every tick at 8 quanta per ray; sail of mass 64 at rest at x = +4, absorbing;
the conservation audit checks every event. Runtime source `f668e71273fd...`,
280 s of host time for 12 ticks.

| Tick | Sail offset, momentum | Lamp momentum | Audit |
| --- | --- | --- | --- |
| 1 to 4 | 4, (0, 0, 0) | (0, 0, 0) | closed, rays in flight |
| 5 | 4, (128, 0, 16) | (0, 0, 0) | closed |
| 6 | 4, (256, 0, 32) | (0, 0, 0) | closed |
| 7 | 4, (384, 0, 48) | (0, 0, 0) | closed |
| 8 | 5, (512, 0, 64) | (0, 0, 0) | closed |
| 10 | 6, (512, 0, 64) | (0, 0, 0) | closed |
| 12 | 7, (512, 0, 64) | (0, 0, 0) | closed: world 199,976 + escaped 24 = 200,000 quanta; world momentum (128, 0, 16) + escaped (-128, 0, -16) = 0 |

The audit checked 11,249,738 Node events and every residual was zero. One
heading of the set, (16, 0, 2), passes through the sail's Node; it delivers 8
quanta and (128, 0, 16) of momentum per tick from tick 5, and the sail starts
to move at half a hop per tick once its momentum passes its mass times the
speed scale. That heading's integer path leaves the x axis after four steps, so
from x = +5 on no ray of this set crosses the sail and its momentum stays at
(512, 0, 64): 32 absorbed quanta. The lamp's momentum is zero at every tick
because the mirrored set sums to zero exactly; the momentum that pushes the
sail is carried by the rays still in flight on the opposite side of the sweep,
and leaves through the open boundary with them.

## Conclusion

Signed straight-ray fields plus an exchange coupling give the charge-sign
structure of electrostatics: repulsion, attraction, and no effect on neutral
bodies, with head-on backscatter for like charges. The charge probes carry no
energy, so close encounters are unbounded there. The radiation-pressure probe
shows the closed form: a funded emitter, an absorber and the audit keep energy
and momentum exact at every event, and the only force that closes this way is
repulsive. An attraction that pays for the kinetic energy it creates is still
open. Proton emission is a configured conversion that conserves what its
invariants declare and nothing more.
