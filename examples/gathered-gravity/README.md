# Gathered gravity probe: does claim-and-gather focus a source's pull?

A configuration on the [signed-quanta attraction](../gravity-probe/README.md)
with [claim and gather](../../docs/SPATIAL_FIELDS.md#claim-and-gather-claim-gather-ray-field-v1)
on the gravity field. Every number is a read-only world/event audit at host
lattice coordinates; no gravitational constant or mass unit is identified.

```sh
python examples/gathered-gravity/run_experiments.py --output artifacts/gathered-gravity
```

## Question

Flat rotation curves are read as unseen mass or as a pull that falls slower
than the inverse square. The ray gravity falls as the inverse square because
a body takes only the rays whose lines cross its Node. The claim gathers a
whole train to whoever catches one ray of it: does that focus the pull on the
catcher and make it fall slower with distance?

## Mechanism

A source at the center of a 21 x 21 x 21 open world emits every tick a train
of 512 negative quanta, one per ray over 512 mirrored headings, each tick's
train with its own label. One body of a million quanta sits at distance 3, 5,
7 or 9, on the lattice axis or off it at `(r, 2, 1)`. Without a claim it
absorbs the rays that cross its Node, paying each quantum and gaining its
amount x heading, the pull of the gravity probe. With a claiming rule the
first crossing ray of a train opens a claim, the flood spreads at link speed,
and every ray of that train the flood still reaches turns homeward and is
taken whole, with its heading. At link speed the flood never overtakes the
rays running away from the body, so it gathers the half of each train headed
its way; at half pace it overtakes them all. The pull per tick is the body's
momentum gain toward the source, averaged over the last 12 of 60 ticks.

## Observed outcomes on 2026-09-14

Runtime source SHA-256 in `summary.json`, Python 3.14, headless; 60 ticks,
pull averaged over the last 12. `tests/test_gathered_gravity.py` checks a
small world: the claiming body pays more and is pulled more than four times
harder than the plain one, both closed.

| Body | Plain pull per tick | Claiming pull per tick | Paid, plain | Paid, claiming |
| --- | --- | --- | --- | --- |
| Axis, r = 3 | 148 | 2,962 | 348 | 9,548 |
| Axis, r = 5 | 24 | 2,705 | 56 | 6,858 |
| Axis, r = 7 | 26 | 2,395 | 54 | 4,994 |
| Axis, r = 9 | 26 | 2,046 | 52 | 3,636 |
| Off axis (3, 2, 1), r = 3.74 | 47.8 | 924 | 109 | 1,989 |
| Off axis (5, 2, 1), r = 5.48 | 49.9 | 745 | 106 | 1,487 |
| Off axis (7, 2, 1), r = 7.35 | 24.2 | 572 | 51 | 1,047 |
| Off axis (9, 2, 1), r = 9.27 | 0 | 0 | 0 | 0 |
| Axis, r = 5, half pace, claiming | | 243 | | 11,045 |

Log-log slopes of pull against distance: plain axis -1.57 (148 at r = 3 and
then the floor of one axis quantum, 24, at every farther Node), claiming axis
-0.32, claiming off axis -0.71 over the three Nodes a ray line crosses. The
pull is the momentum of the rays taken: with a claim it is the momentum of the
half of each train that the flood, at link speed, can still reach, which is
the half headed toward the body; the body pays for every quantum of it. At
half pace the flood overtakes the whole train, the body pays for more quanta
(11,045 against 6,858) and the pull falls eleven times, to 243, because a
whole isotropic train carries no net momentum. Off the axis at r = 9.27 no
line of the 512 headings crosses the body's Node: no ray, no claim, no pull,
in both worlds. Every world closed on its quanta.

## Conclusion

Gathering focuses the pull, but not into anything like dark matter. On the
axis a claiming body is pulled 12 to 80 times harder than a plain one and the
pull falls as about `r^-0.3`, off the axis as about `r^-0.7`; a rotation curve
from either would rise (`v^2 = a r`), not stay flat, and the exponent is set
by what part of each train the flood can catch before it escapes, not by any
mass. The moment the flood catches everything, at half pace, the gathered
momentum cancels and the pull nearly vanishes while the body pays more for
it. So the claim delivers energy to the catcher, not a force law; the plain
ray gravity stays inverse square with a granular floor, and neither gives the
flat rotation curve. What would: unseen mass, or a rule that spends a wave's
momentum, not its quanta, on the catcher, which this lattice does not have.
