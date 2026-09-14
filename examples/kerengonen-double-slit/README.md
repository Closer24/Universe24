# Kerengonen double slit: two lamps in phase and a fringe in path difference

A configuration on the [Kerengonen candidate](../../docs/SPATIAL_FIELDS.md#kerengonen-phased-rays-kerengonen-ray-field-v1),
`kerengonen-ray-field-v1`; no other engine rule is involved. Every number is a
read-only world/event audit at host lattice coordinates. No wavelength,
constant or species is identified: the phase steps and the advance per link are
configured integers.

```sh
python examples/kerengonen-double-slit/run_experiments.py --output artifacts/kerengonen-double-slit
```

## Mechanism

Two funded lamps sit eight links upstream of a line of 25 absorbers, at
`y = -3` and `y = +3` in the plane of the screen. Both fire the same 59
planar headings facing the screen every tick, 16 quanta per ray, and pay every
quantum from their stock. The field has eight phase steps and advances one step
per link, so rays from the two lamps that meet at a screen Node differ in phase
by the Manhattan path difference `|y + 3| - |y - 3|` steps: zero at the
center, two at `y = +-1` (a quarter turn), four at `y = +-2` (a half turn),
six beyond (three quarters). A screen Node absorbs the rays that reach it,
scaled by the coherence of what met there; quanta that cancel continue past
the screen and leave through the open boundary. Three worlds are compared:
the phased field, the same with the second lamp offset by half a turn, and the
plain ray field without the key, where amounts simply add.

## Observed outcomes on 2026-09-14

Runtime source SHA-256 `07ecc6729b3d...` for the 16-quanta worlds and
`0682c2926013...` (probe) for the single-quantum lottery worlds (full values
in `summary.json`), Python 3.14, headless, 48 ticks. `tests/test_kerengonen.py` checks the same
coherence rule on two lamps three links from a Node and the composition of
this probe.

| Screen y | Path difference | Phased | Second lamp half a turn | Plain | Phased over plain |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 928 | 0 | 928 | 1.00 |
| +-1 | +-2 | 704 | 704 | 1376 | 0.51 |
| +-2 | +-4 | 64 | 928 | 928 | 0.07 |
| +-3 | +-6 | 512 | 512 | 928 | 0.55 |
| +-4 | +-6 | 596 | 596 | 896 | 0.67 |
| +-6 | +-6 | 464 | 464 | 832 | 0.56 |
| +-8 | +-6 | 432 | 432 | 768 | 0.56 |
| +-12 | +-6 | 436 | 436 | 640 | 0.68 |

The center is fully lit, a quarter turn halves it, a half turn darkens it to
the few quanta that arrived on ticks when only one lamp's rays were present,
and the wings sit near one half. Offsetting the second lamp by half a turn
inverts the pattern exactly where the path difference is even: the center goes
dark and `y = +-2` lights up, while the quarter-turn Nodes stay at one half.
The plain field shows no such structure; its unevenness (the peak at `y = +-1`)
is the integer heading set. Absorbed totals: 13,280 phased, 14,080 half-turn,
21,408 plain; the difference left through the open boundary. In every world
the quanta in records, in flight and escaped equal the initial stock, and both
lamps end with zero stock and the same recoil.

A separate world with eight headings, a five-Node screen and the event audit on
ran 24 ticks: the `(16, +-3)` headings of both lamps meet at the center after
19 links each and are absorbed in phase, 160 quanta; 1,280,412 Node events
closed with zero residual, energy 5,632 in the world plus 512 escaped against
6,144 initial, momentum (-2112, 0, 0) in the world against (2112, 0, 0)
escaped.

### Single quanta, whole or nothing: the fringe built click by click

The same lamps fire one quantum per ray for 96 ticks, and the field selects
`"capture": "lottery"`: a screen Node takes each whole quantum or leaves it,
by a local ticket drawn against the coherent share. Two seeds are run, and
the share rule on the same single quanta for comparison.

| Screen y | Path difference | Lottery, seed 1 | Lottery, seed 2 | Share rule |
| --- | --- | --- | --- | --- |
| 0 | 0 | 154 | 154 | 154 |
| +-1 | +-2 | 133, 127 | 135, 127 | 2 |
| +-2 | +-4 | 4 | 4 | 4 |
| +-3 | +-6 | 71, 79 | 84, 62 | 6 |
| +-5 | +-6 | 89, 93 | 106, 96 | 6 |
| +-7 | +-6 | 152 | 152 | 152 |
| +-10 | +-6 | 116, 121 | 108, 113 | 6 |

Where the coherence is one or zero the two seeds agree exactly with the share
rule: 154 at the center, 4 at the half turn, 152 at `y = +-7`, a Node that
only ever sees one lamp's rays at a time. Where the coherence is one half the
share rule truncates a lone quantum's half share to nothing and takes 2 to 6,
while the lottery takes whole quanta at that rate and the two seeds scatter
around each other. The absorbed totals are 2,354 for either seed against 578
for the share rule; every quantum is accounted for in all three worlds. This
is the fringe as single detections: each quantum lands whole at one Node, and
the pattern is in how often.

### One lamp, an absorbing wall, two slits that re-emit: the wave passes through

The falsification test. A single lamp twelve links upstream fires a forward
cone of 117 headings (within 45 degrees of +x, scale 64), 64 quanta per ray,
for 64 ticks. Eight links downstream stands a wall of absorbers across the
whole width, with two Nodes at `y = -3` and `y = +3` of a `slit` type: a slit
absorbs like the wall but re-emits its whole stock every cycle over the same
cone, at the phase it absorbed plus one advance, as
[carried](../../docs/SPATIAL_FIELDS.md#kerengonen-phased-rays-kerengonen-ray-field-v1)
emission. The screen is twelve links beyond the wall. Four worlds: both
slits, each slit alone, and both slits on the plain field.

| Screen y | Path difference | Two slits | Slit A alone | Slit B alone | Sum of the two | Plain, two slits | Two slits over the sum |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 2430 | 1110 | 1110 | 2220 | 2220 | 1.09 |
| +-1 | +-2 | 978 | 950, 1080 | 1080, 950 | 2030 | 2030 | 0.48 |
| +-2 | +-4 | 140 | 1365, 875 | 875, 1365 | 2240 | 2240 | 0.06 |
| +-3 | +-6 | 1102 | 1000, 1020 | 1020, 1000 | 2020 | 2020 | 0.55 |
| +-4 | +-6 | 1101 | 1365, 825 | 825, 1365 | 2190 | 2190 | 0.50 |
| +-8 | +-6 | 875 | 875, 580 | 725, 875 | 1600, 1455 | 1600, 1455 | 0.55, 0.60 |
| +-10 | +-6 | 987 | 825, 0 | 0, 825 | 825 | 825 | 1.20 |
| +-12 | +-6 | 465 | 465, 0 | 0, 465 | 465 | 465 | 1.00 |

Without phase, two slits give exactly the sum of the two single slits at every
Node: amounts add, nothing more. With phase the same two slits give the fringe
of the two-lamp experiment: the center above the sum, a quarter turn at one
half, a half turn at six percent, three quarters near one half, and where only
one slit's rays reach (`|y| >= 11`) exactly the single-slit value, because
there is nothing to interfere with. No second lamp exists: the two sources
are the two slits, lit by one wave, and their phases are what the wave carried
to them, 11 links from the lamp for both. The wall keeps 332,800 quanta in the
phased and the plain world alike, and every world closes on its initial stock.

### A thick screen: what a dark Node lets pass is absorbed behind it

The two-lamp world again, 16 quanta per ray, with the screen one, two, four
and eight Nodes deep. The first layer is the screen above; each layer behind
it is another line of absorbers one link on, where the path difference, and
so the phase, is different.

| Layers | Phased, total absorbed | Per layer | Plain, total absorbed | Phased over plain | First layer at y = 0 and y = 2 |
| --- | --- | --- | --- | --- | --- |
| 1 | 13,280 | 13,280 | 21,408 | 0.62 | 928, 64 |
| 2 | 17,062 | 13,280, 3,782 | 21,408 | 0.80 | 928, 64 |
| 4 | 18,752 | 13,280, 3,782, 1,244, 446 | 21,408 | 0.88 | 928, 64 |
| 8 | 19,682 | 13,280, 3,782, 1,244, 446, 148, 190, 290, 302 | 21,408 | 0.92 | 928, 64 |

The plain field absorbs everything in its first layer, and the layers behind
it stay empty. With phase, the first layer keeps its fringe unchanged, and the
quanta it let pass at its dark Nodes are absorbed in the layers behind, where
they meet a different path difference: eight layers recover 92 percent of the
plain total, the rest still in flight or escaped, and every world closes on
its initial stock. The thin-screen deficit is not lost energy but energy that
lands deeper.

## Conclusion

Rays with a phase interfere where they meet and are absorbed whole where they
land: the fringe is in the absorption, the amounts are never changed, and the
ledger closes. A single lamp behind two re-emitting slits gives the same
fringe, so the wave's phase survives absorption and re-emission at a Node and
the double slit needs no second lamp. Two limits are visible in the numbers. Interference needs rays
of both lamps at one Node on one tick, so ticks on which only one lamp's rays
are present pass ungated; and the pattern follows Manhattan path difference on
this lattice, not Euclidean. Quanta that cancel are not redistributed to the
bright fringes; they continue, and a thick screen absorbs them behind the
first layer, which keeps the rule local and the total exact but differs from
a wave that carries its energy to where it adds.
