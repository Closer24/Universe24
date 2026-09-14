# Euclidean pace probe: a round front and a fringe in Euclidean path difference

A configuration on the [straight-ray field](../../docs/SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1)
with `"metric": "euclidean"` ([contract](../../docs/SPATIAL_FIELDS.md#euclidean-pace-metric-euclidean),
identity `euclidean-ray-pace-v1`) and, for the fringe, the
[Kerengonen candidate](../../docs/SPATIAL_FIELDS.md#kerengonen-phased-rays-kerengonen-ray-field-v1).
Every number is a read-only world/event audit at host lattice coordinates. No
length unit or constant is identified: the pace is the integer ratio of a
heading's Euclidean and Manhattan lengths, and the phase steps and advance
are configured integers.

```sh
python examples/euclidean-pace/run_experiments.py --output artifacts/euclidean-pace
```

## Mechanism

On the links metric every ray hops one link per tick, so after `t` ticks a
lamp's front stands `t` links away in every heading: an octahedron, whose
Euclidean radius is `t` along an axis and `t / sqrt 3` along a body diagonal.
On the Euclidean metric the slowest heading (the body diagonal here, with the
smallest Euclidean length per link) hops every tick, and every other ray adds
that pace to its own wait each tick and hops only when the wait passes its
heading's pace, carrying the remainder: an axis ray hops every `sqrt 3`
ticks, a face diagonal every `sqrt 3 / sqrt 2`. A waiting ray stays resident
at its Node and its phase advances with the tick, so a ray's phase counts
ticks, and ticks count Euclidean distance.

The front probe fires one quantum on each of the 26 neighbor headings every
tick for twelve ticks and reads the farthest Node holding a ray of each
heading class. The fringe probe puts two lamps in phase four links apart, one
link below a 29-heading fan that reaches every Node of a screen line twelve
links above, and sums the coherent reading at each screen Node over the last
eight of forty ticks at 64 phase steps and advance 16. The Manhattan path
difference between the lamps is `|x + 2| - |x - 2|`, which saturates at four
links beyond the lamps, a full turn at this advance; the Euclidean one keeps
growing with `x`, and every heading in this fan moves at the pace of the
`(1, 1)` diagonal, `sqrt 2 / 2` link-lengths per tick, so the half turn is
predicted where `16 x sqrt 2 x (d_a - d_b)` is 32 steps.

## Observed outcomes on 2026-09-14

Runtime source SHA-256 in `summary.json`, Python 3.14, headless.
`tests/test_euclidean_pace.py` checks the reaches, the darkest Nodes and the
closure; `tests/test_kerengonen.py` checks the paces and the kept rays.

| Probe | Links metric | Euclidean metric |
| --- | --- | --- |
| Front, links reached (axis, face, body) | 12, 12, 12 | 6, 9, 12 |
| Front, Euclidean radius | 12, 8.49, 6.93 (spread 1.732) | 6, 6.4, 6.93 (spread 1.155) |
| Fringe, darkest Nodes | x = -1, 1 (reading 0) | x = -5, 5 (reading 0) |
| Fringe, predicted half turn | x = -1, 1 | x = -5, -4, 4, 5 |
| Fringe, readings from x = -12 | 96, 128, 96, 64, 64, 64, 64, 64, 64, 64, 64, 0, 64, 0, 64, 64, ..., 96, 128, 96 | 96, 80, 48, 64, 48, 32, 8, 0, 8, 32, 32, 64, 64, 64, 32, 32, 8, 0, 8, 32, 48, 64, 48, 80, 96 |
| Quanta closed | yes | yes |

On the links metric the line is flat beyond the lamps' separation, because
the Manhattan path difference no longer changes; the dark Nodes at `x = -1`
and `1` are the two-link difference, a half turn. On the Euclidean metric the
dark Nodes sit at `x = -5` and `5`, inside the predicted band, with the
center bright and the edges bright again where the difference passes a full
turn. The Euclidean front is round to within one link; the axis ray shows 6
links because the fraction of a link it is waiting for is not visible on the
lattice. The plain field on the Euclidean metric reads 64 to 128 rather than
a flat 64, since one or two rays of each lamp are resident at a Node on a
given tick; the summed readings above carry that modulation and the fringe
through it. The extra 32 at the edges of both lines is a third heading whose
lattice line crosses the screen there.

## Conclusion

The fringe is exactly where rays meet, and where they meet is the metric.
The links metric gives the lattice's Manhattan fringe; the Euclidean pace
gives the Euclidean one and a round front, and pays for it with rays that
wait at Nodes, slower than one link per tick and never faster. Both are
configured choices, and every quantum stays whole and counted in both.
