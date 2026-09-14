# Kerengonen mirror probe: a lamp facing a mirror holds a standing wave

A configuration on the [Kerengonen candidate](../../docs/SPATIAL_FIELDS.md#kerengonen-phased-rays-kerengonen-ray-field-v1)
with the mirror emission; no other engine rule is involved. Every number is a
read-only world/event audit at host lattice coordinates. No wavelength unit or
constant is identified: the phase steps and the advance per link are
configured integers.

```sh
python examples/kerengonen-mirror/run_experiments.py --output artifacts/kerengonen-mirror
```

## Mechanism

A held lamp at `x = -16` fires 8 quanta each way along the axis every tick on
a 64-step field; the `-x` rays leave the open world at once. A mirror record
at `x = +16` absorbs every ray that reaches it and, next cycle, re-emits its
whole stock as one ray back along `-x`, the mirror image of the heading it
absorbed, at the phase it absorbed plus one advance. The mirror keeps the
momentum it reverses through its `recoil_field`. Between lamp and mirror the
incident and reflected rays meet at every Node with equal amounts, and the
sampled value is their coherent sum: `16 cos^2` of half the phase difference,
which changes by `2 x advance` per link. The standing wave's period is
therefore `64 / (2 x advance)` links. Each advance is also run without the
mirror.

## Observed outcomes on 2026-09-14

Runtime source SHA-256 `bf409119b7ca...` (full value in `summary.json`),
Python 3.14, headless, 96 ticks; the line is read from `x = -15` to `x = 15`.
`tests/test_kerengonen_mirror.py` checks the periods at advances 4 and 8 on a
shorter run, and `tests/test_kerengonen.py` checks the reflected rays, the
carried phase, the mirror's stock and momentum and the closure.

| Advance | Period predicted | Period measured | Readings from x = -15 | Without the mirror |
| --- | --- | --- | --- | --- |
| 2 | 16 | 16 | 15, 14, 12, 9, 6, 3, 1, 0, 0, 1, 3, 6, 9, 12, 14, 15, then again | 8 everywhere |
| 4 | 8 | 8 | 15, 11, 4, 0, 0, 4, 11, 15, then again | 8 everywhere |
| 8 | 4 | 4 | 13, 2, 2, 13, then again | 8 everywhere |

The nodes of the standing wave sit where the reading is 0 and the antinodes
where it is 15 (the integer cosine table rounds the full 16 down by one at a
half step); doubling the advance halves the period, twice. Without the mirror
the line reads a flat 8: the incident ray alone, with nothing to interfere
with. The mirror ends every run with momentum `+1016` along `x`, the momentum
of the rays it turned around, and the quanta in records, in flight and escaped
equal the lamp's initial stock in every world.

## Conclusion

Reflection is absorption followed by re-emission along the mirrored heading
with the phase carried, and that suffices for a standing wave with the
half-wavelength period the phase advance dictates. With the Huygens slit this
gives the field two ways to turn a wave around a corner, both local and both
closed on the ledger. What it does not give: a mirror that reflects at an
angle other than across a lattice axis, or a partial mirror; both would need a
heading map beyond one sign flip.
