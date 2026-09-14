# Matter-wave probe: a particle in flight becomes a wave and lands as a fringe

A configuration on the [Kerengonen candidate](../../docs/SPATIAL_FIELDS.md#kerengonen-phased-rays-kerengonen-ray-field-v1)
with the per-ray advance and the Huygens slits; no engine rule is added.
Every number is a read-only world/event audit at host lattice coordinates.
No mass, constant or wavelength unit is identified: the momentum, the advance
rule `|p| / 4` and the train length are configured integers.

```sh
python examples/matter-wave/run_experiments.py --output artifacts/matter-wave
```

## Mechanism

A particle record of 479,232 matter quanta and momentum `p` along `+x` moves
at half a link per tick. A local update counts its ticks. From tick 4 it
stands still and a funded emission pays out one sixteenth of its matter per
tick as rays over a 117-heading forward cone, each ray advancing
`wavenumber / 4` phase steps per link, where `wavenumber` is the momentum the
particle set out with; the momentum field itself takes the recoil of every
emitted ray, and the husk, empty after sixteen ticks, never moves again. The
train is longer than any path difference to the screen, so the two slits'
contributions overlap at every screen Node; a one-tick pulse meets itself only
where the paths are equal and shows no fringe, which the first version of this
probe measured. The wave meets the wall, the slits at `y = -6` and `y = +6`
and the screen of the [de Broglie probe](../de-broglie/README.md), and each
momentum is also run with one slit at a time and on the plain field.

## Observed outcomes on 2026-09-14

Runtime source SHA-256 `fa6a8e673710...` (full value in `summary.json`),
Python 3.14, headless, 84 ticks. `tests/test_matter_wave.py` checks the flight,
the stop, the pay-out and the closure on a small heading set.

| Screen y | p = 32, advance 8 | p = 64, advance 16 |
| --- | --- | --- |
| 0 | 1.24 | 1.44 |
| +-1 | 0.60 | 0.13 |
| +-2 | 0.26 | 1.29 |
| +-3 | 0.76 | 0.42 |
| +-4 | 1.12 | 1.21 |
| +-5 | 0.80 | 0.63 |
| +-6 | 0.86 | 1.30 |
| +-7, +-8 | 1.00 | 1.00 |

Each cell is the two-slit count of one particle's matter over the sum of the
two single-slit counts. The first dark fringe sits at `y = 2` for momentum 32
and at `y = 1` for momentum 64, as `16 / advance` predicts, and the faster
particle shows bright Nodes at 0, +-2, +-4 and +-6 where the slower one has
them at 0 and +-4: the same halving of the period the beam gave. Where only
one slit's rays reach, every ratio is exactly one. On the plain field the two
slits give exactly the sum of the single slits for both momenta. The husk
ends with matter 0 at `x = -14`, two links from where it started, and a recoil
of `-27,451,360` in `x` (`-27,451,328` for momentum 64): the momentum its
rays carried away. Matter in records, in flight and escaped equals the initial
479,232 in every one of the eight worlds.

## Conclusion

A moving record turned into a wave train, passed two slits, and landed on the
screen with the fringe of the momentum it flew with. Three things had to hold
for that and now do: a stock below the sweep count takes the next headings in
turn (an engine fix found by this probe), the advance is read from the
momentum of the flight rather than from the recoiling husk, and the train is
long enough to meet itself. What this is not: the matter lands spread over the
screen as one particle's wave, not at one Node. Landing whole at one place
needs a causal rule that retires the rest of the wave when one Node captures
it, which the quantum layer has and the ray field does not yet.
