# De Broglie probe: a beam's fringe spacing shrinks as its momentum grows

A configuration on the [Kerengonen candidate](../../docs/SPATIAL_FIELDS.md#kerengonen-phased-rays-kerengonen-ray-field-v1)
with the per-ray advance: a held beam source of momentum `p` emits matter
rays whose phase advances `|p| / 4` steps per link, its own de Broglie rule,
on a field of 64 phase steps. Every number is a read-only world/event audit at
host lattice coordinates. No mass, constant or wavelength unit is identified:
the momentum and the advance are configured integers, and the rule between
them is the one under test.

```sh
python examples/de-broglie/run_experiments.py --output artifacts/de-broglie
```

## Mechanism

The beam sits thirteen links upstream of an absorbing wall with two Huygens
slits at `y = -6` and `y = +6`, which absorb what reaches them and re-emit
their stock every cycle at the phase and advance they absorbed, one advance
on. The screen of 25 absorbers is twelve links beyond the wall. On this
lattice the path difference between the slits and a screen Node at offset `y`
is `2 y` links for `|y| <= 6` and 12 beyond, so the phase difference is
`2 y x advance` steps: the first dark fringe sits at `y = 16 / advance` and the
fringe period in `y` is `32 / advance`. For momenta 16, 32 and 64 the advance
is 4, 8 and 16, the first dark 4, 2 and 1, the period 8, 4 and 2. Each
momentum is also run with one slit at a time and on the plain field, and the
fringe is read as the two-slit profile over the sum of the two single slits.

## Observed outcomes on 2026-09-14

Runtime source SHA-256 `40c741bed3d9...` (full value in `summary.json`),
Python 3.14, headless, 117 headings in a forward cone at scale 64, 64 quanta
per ray, 64 ticks. `tests/test_de_broglie.py` checks the composition; the
carried advance and the momentum rule are checked in `tests/test_kerengonen.py`.

| Screen y | Phase steps per unit y | p = 16, advance 4 | p = 32, advance 8 | p = 64, advance 16 |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1.12 | 1.24 | 1.45 |
| +-1 | 2 x advance | 0.77, 0.80 | 0.55, 0.59 | 0.07 |
| +-2 | | 0.55, 0.63 | 0.08, 0.09 | 1.33, 1.34 |
| +-3 | | 0.32, 0.15 | 0.57, 0.64 | 0.17, 0.16 |
| +-4 | | 0.18, 0.16 | 1.17, 1.15 | 1.34, 1.35 |
| +-5 | | 0.22, 0.21 | 0.54, 0.58 | 0.24, 0.22 |
| +-6 | | 0.80, 0.93 | 0.33 | 1.38, 1.51 |
| +-7, +-8 | one slit only | 1.00 | 1.00 | 1.00 |

Each cell is the two-slit count over the sum of the single-slit counts.

| Momentum | Advance | First dark predicted | First dark measured | Period predicted | Bright Nodes seen |
| --- | --- | --- | --- | --- | --- |
| 16 | 4 | 4 | 4 | 8 | 0 |
| 32 | 8 | 2 | 2 | 4 | 0, +-4 |
| 64 | 16 | 1 | 1 | 2 | 0, +-2, +-4, +-6 |

Doubling the momentum halves the fringe period, three times in a row: the
first dark moves from 4 to 2 to 1, and the beam of momentum 64 shows four
bright and three dark pairs where the beam of momentum 16 shows one dark pair.
Where only one slit's rays reach, `|y| >= 7`, every ratio is exactly one. On
the plain field two slits give exactly the sum of the two single slits for
every momentum: the momentum does nothing there. All twelve worlds close on
their initial stock of matter. The single-slit profiles are the same for all
three momenta, because the advance changes nothing about where a ray goes.

## Conclusion

The de Broglie rule holds on matter rays as configured: wavelength inverse to
momentum, read off a double slit, with the plain field as the null. What the
probe does not do is derive the rule; `|p| / 4` is the configured law, and the
measurement shows that the lattice, the Huygens slits and the coherence gate
carry it faithfully from the source to the screen. A moving particle is not
yet a matter ray: the beam here is a held source, and turning a record in
flight into rays and back is the next step.
