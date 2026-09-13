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

Self-field exclusion is configured, not derived: a moving body reaches the next
Node together with the rays it emitted one tick earlier, and with a single shared
field it pushed itself forward regardless of the other body's sign. Separate
fields per body remove that; a general rule for excluding one's own field is
still the open hypothesis named in `POSTULATES.md`.

The third probe uses no field. Two held records, a bound proton and a residual
core, share a Node; a local update counts ticks on the proton, and a
[two-record conversion](../../docs/LOCAL_CONVERSIONS.md) fires when the count
passes a delay. Its assignments give the free proton momentum `(+P, 0, 0)` and
the recoiling core `(-P, 0, 0)`; declared invariants keep total momentum and
total mass exact.

