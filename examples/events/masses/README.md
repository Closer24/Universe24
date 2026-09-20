# The cavity: two lamps exchanging light (the masses design, 2026-09-20)

Two worlds written by hand for
[the masses design](../../../docs/designs/masses/DESIGN.md), section 3: the
one dynamics of a measured event's content the Beam Law has is the exchange
of paid units (a lamp's release costs `quantum` x turn per unit, a click
joins what the unit carries, E = h f), and the question is whether that
dynamics selects a content. Not a registered series: nothing here is
entered in the experiments register until the model owner says so.

## The base

A bar of 12 x 1 x 1 Nodes, `"law": "beam"`, y and z periodic, x open, K
4096, N 64, `suspension` 0, one paid family `light` (`quantum` 1). Two
fixed lamps of that family at x = 2 and x = 9 (seven Links apart, twelve
intervals of flight on a heading), each with `rate` [1, 1] on the one
direction toward the other and no window: at every self-creation whose
turn s = `by_clock(age, M, 4096)` is above 0 it releases one unit of
content s toward the other, and the other measures it by the keys' rule
(a paid arrival is measured: the content joins).

| World | The two contents | What it reads |
| --- | --- | --- |
| `cavity_unequal.json` | 32768 and 8192 (turns 8 and 2), 6000 intervals | whether the contents move, and toward what |
| `cavity_equal.json` | 20480 and 20480 (turns 5 and 5), 600 intervals | whether an equal split is a fixed point |

## The expectation, written before the runs (the mathematician's integers)

The map is linear in the contents: A loses s_A = M_A / K per interval and
gains s_B twelve intervals later, so the sum is conserved (the books) and
the difference relaxes as (1 - 2 / K) per interval, the time constant
K / 2 = 2048 intervals. Expected: `cavity_unequal` at 6000 intervals near
(20806, 20035) (the standalone map of `ladder.py` section C, which
reproduces the engine integer by integer at 600 intervals: (29634, 11209));
`cavity_equal` at (20420, 20420) at every interval past the flight time,
sixty units of content in transit (twelve intervals x five each way);
every total has such a fixed point, so no content is selected.

## Run and read

```bash
PYTHONPATH=src python -m event_universe --init examples/events/masses/cavity_unequal.json --output runs/masses/cavity_unequal
PYTHONPATH=src python -m event_universe --init examples/events/masses/cavity_equal.json --output runs/masses/cavity_equal
PYTHONPATH=src python docs/designs/masses/cavity_read.py runs/masses
```

Each run takes seconds. The readings of 2026-09-20 are in
`docs/designs/masses/cavity.out` (every line labelled DETECTOR or
GAMEBOARD): `cavity_unequal` (20806, 20035) at 6000, `cavity_equal`
(20420, 20420) at 600, the books balanced at every tick, the content per
click (the partner's turn, E = h f read at the receiver) 8 and 2 at the
start of the unequal world and 5 at its end on both sides.
