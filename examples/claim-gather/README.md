# Claim and gather probe: a captured wave lands whole at one Node, later

A configuration on the [straight-ray field](../../docs/SPATIAL_FIELDS.md#straight-ray-transport-isotropic-ray-field-v1)
with a pace below link speed and `claim`
([contract](../../docs/SPATIAL_FIELDS.md#claim-and-gather-claim-gather-ray-field-v1),
identity `claim-gather-ray-field-v1`), the engine `dissolve` schedule, and,
for the double slit, the [matter-wave world](../matter-wave/README.md) on the
Euclidean metric with the lottery capture. Every number is a read-only
world/event audit at host lattice coordinates. No unit or constant is
identified: the pace, the claim's lifetime, the click fraction and the
capture seeds are configured integers.

```sh
python examples/claim-gather/run_experiments.py --output artifacts/claim-gather
```

## Mechanism

A particle of 64 quanta at the center of a 25 x 25 x 3 open world dissolves
after two ticks over eight into rays on the eight planar headings, one
quantum per ray per tick, at a quarter link per tick. A screen record six
links along `+x` absorbs with a claiming rule. The first ray to reach it is
taken, and the screen's Node opens a claim: on its next cycle it passes the
claim to all six neighbors, each of which remembers the port it came from and
passes it on, so the claim reaches every Node of the world at one link per
tick. Every free ray of the train at a Node that holds the claim turns
homeward and walks the parent ports back at one link per tick, four times
faster than the wave; at the screen the record takes each one whole. The same
world is run without the claiming rule, and with a second screen four links
along `-x` that reaches the wave first.

For the landing, the matter-wave double slit (a particle of 479,232 quanta
flying at half a link per tick, dissolving into a 256-heading cone at
momentum 64, a wall with two Huygens slits at `y = -6` and `6`, a screen line
of 25 records twelve links behind it) is run on the Euclidean metric at half
pace, with the slits re-emitting the train they absorbed and each screen
record drawing lottery clicks at 1/256 of the coherent share with a claiming
rule. The first click anywhere on the screen opens the claim, the flood
crosses the screen line and the wall, and the winning record gathers the
train. Forty-eight capture seeds give forty-eight landings; the same world
with the coherent share taken and no claim gives the fringe of the wave.

## Observed outcomes on 2026-09-14

Runtime source SHA-256 in `summary.json`, Python 3.14, headless.
`tests/test_claim_gather.py` checks the three isotropic worlds tick by tick,
one landing, the claim rules and the identity.

| World | Result |
| --- | --- |
| Gathered | First claim at tick 26; the flood covers all 1,875 Nodes; every quantum is at the screen by tick 57 and stays; screen momentum (0, 0, 0); nothing escaped; closed at every tick |
| Without a claim | The screen keeps the 8 quanta of its own line; the axis rays have escaped by tick 80 and the diagonals are still walking out; closed |
| Contested | The rival four links away clicks first at tick 18 and gathers 62; the farther screen keeps the 2 it took before its claim met the earlier one and yielded; gathered by tick 39; one root; closed |

Landings over 48 seeds, screen `y` of the winning record (the root of the
surviving claim), against the fringe of the same wave taken as a coherent
share without a claim:

| Screen band | Share of the wave's fringe | Landings expected of 48 | Landings measured |
| --- | --- | --- | --- |
| `\|y\| <= 1` | 0.170 | 8.2 | 5 |
| `2 <= \|y\| <= 3` | 0.351 | 16.9 | 7 |
| `4 <= \|y\| <= 5` | 0.197 | 9.5 | 13 |
| `\|y\| >= 6` | 0.281 | 13.5 | 23 |

Landings by screen Node: -9: 2, -8: 4, -7: 6, -6: 3, -5: 3, -4: 4, -3: 3,
-2: 1, 0: 3, 1: 2, 2: 2, 3: 1, 4: 2, 5: 4, 6: 1, 7: 3, 8: 2, 9: 1, 11: 1
(measured with the lottery drawing the square of its ticket state; the first
measurement, drawing the state itself, put 6, 11, 10 and 21 in the bands).
The wave's fringe on the same screen (coherent share, no claim): 2,340 and
2,357 at `y = -3` and `3`, 1,516 at the center, 1,130 and 1,145 at `y = -1`
and `1`, about 1,100 at `y = -5, -4, 4, 5`, 300 to 620 beyond; 22,269 of the
479,232 quanta reached the screen, 425,661 stayed in the wall and the slits.

Every one of the 48 runs landed: one surviving root, nothing in flight at the
end, matter closed. The winning record holds between 0.614 and 0.992 of what
reached the screen, median 0.87; the rest is the clicks other screen Nodes
drew in the ticks before the winner's flood reached them and their claims
yielded (from 471 to 20,406 quanta in the first ten runs), and 729 to 2,485
quanta per run escaped past the screen line before any click. The landings
sit inside the wave's fringe but lean outward: short of the fringe's share at
the center and in the bright band at `|y| = 2, 3`, above it at `4, 5` and
beyond `6`. The outer Nodes lie nearest the slits, so the wave reaches them a
few ticks earlier even on the Euclidean metric, and the first click is drawn
while only they see the wave. On the links metric the same run put no
landing at all within `|y| <= 1`.

## Conclusion

A wave that was captured at one Node arrives there whole: nothing is created
at the capture and nothing retired elsewhere by a signal faster than the
rays, because the claim travels at link speed and the matter slower, and the
ledger closes at every tick. The price is time: the particle is one place plus
matter in transit for the ticks the flood and the return take, and a second
capture that raced the flood keeps its piece. On the Euclidean metric the
landing position follows the fringe of the wave; on the links metric the
first click favors the screen Nodes the Manhattan front reaches first, a
lattice artifact the metric removes. What this does not give: a refund from a
yielding capture, a landing that is instantaneous, or a click rate that is
physical randomness rather than a configured ticket.
