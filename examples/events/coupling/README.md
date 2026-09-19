# The coupling series C under the law of events, on the plane

Twenty-one worlds of one base, written by `make_worlds.py`; the register
entry is
[C, the couplings under the law of events, on the plane (2026-09-19)](../../../docs/EXPERIMENTS.md#c-the-couplings-under-the-law-of-events-on-the-plane-2026-09-19)
and the evidence is in [validation](../../../docs/VALIDATION.md). The
physics-rule reviewer pinned the design and its identities on 2026-09-19 for
an open board of 61^3; the model owner cancelled that version the same day
("cancel the runs; let it run on two-dimensional boards"), so the series runs
on the plane: the same items, the same identities, the readings of the plane
registered as the plane's. A research run, made once, never a test; a
reading outside its bound is reported with its numbers, never moved.

## The base

A board of 121 x 121 x 1 Nodes with the z axis declared periodic
(`"boundary": {"z": "periodic"}`, [the engine](../../../docs/ENGINE.md), "The
board"): with an extent of 1 the two z Ports of every Node return to the same
Node at the next interval, so the board is a true two-dimensional board and
nothing leaks on z; the x and y faces are open. The centre c = (60, 60, 0),
`"law": "events"`, K 2^22, N 64, `release` [1, 128], `suspension` 0 (1 in
world 6 only), one free family `m` of charge 0 (the family `q` in item 7,
where the measured events carry the charges), every measured event `fixed`
unless the item says otherwise, `phase` 0. The source is a measured event of
content 2^24 at c: `by_clock` gives 2^17 per Port at every self-creation on
the six Ports; the two z Ports' releases come home at the next interval as
its own number and are created again in six equal shares, so at the fixed
point the source releases 3 x 2^16 per Port and the net emission into the
plane is q = 4 x 3 x 2^16 = 6 x 2^17 = 786432 units per interval, exact
(the home amount h satisfies h = 2 (2^17 + h / 6), h = 3 x 2^17, no
remainder). A probe is a measured event of content 1 (m in item 1) with the
default table (`read` for a free family: the push taken, the units mix on as
at an empty Node), so a probe is transparent to the stream it reads. A probe
releases six lone units at age 128 / m along its six lattice lines; the tool
filters records by `number`, and the probes sit off each other's lines except
where the item allows a shared axis.

What the plane changes, beyond the count of Nodes: a Node's count and the
momentum a probe reads include what came back through its own z stub (the
two z shares of every mixing, about 2 / 9 of the units, created again at the
same Node at the next interval), while the radial flow (amount x heading
projected on the radial unit vector of the plane) does not; Gauss on a circle
gives 1 / r for the count, the flow and the carried momentum and 1 / sqrt(r)
for the size, so the far-field readings are scaled by r and 2 pi r, not r^2
and 4 pi r^2; the front of the stream along an axis is the same lone-arrival
chain as in three dimensions (the z shares only come back one interval
later), so the retardation table for the front is derived by hand from the
mixing rule below; `cube_flux` sums the four in-plane faces only (the z faces
have no outside Node), Gauss's flux through the square.

## The front derived by hand (item 4)

A lone arrival of u units at phase 0 in one slot: the amplitude is
isqrt(u x 32^2) in 32nds; the leaving amplitude of the backward heading (the
Port it came in through) is the sum less three times the arrival, -2 a, and
of every other heading a, so the weights are 4 : 1 : 1 : 1 : 1 : 1, reduced to
28 bits; the floors u x w // W per heading, the units left to the largest
remainders, ties in Port order counted from the tick (+X, -X, +Y, -Y, +Z,
-Z); a group with no whole share for any side goes whole to the heading
nearest its momentum (one unit of momentum per unit along the release
heading, exact along the front since the forward share's momentum is its
units). The source releases 2^17 per Port at tick 1; the front reaches r at
tick r + 1 and is the only thing there (every other path is longer; the z
returns arrive one interval later):

| axis | r = 1 (tick 2) | 2 (3) | 3 (4) | 4 (5) | 5 (6) | 6 (7) | after |
| --- | --- | --- | --- | --- | --- | --- | --- |
| +x | 131072 | 14563 | 1618 | 180 | 20 | 3 | exhausted: the 3 units leave 1 on -x by its floor and, of the 2 left with equal remainders, 1 on -x (rank 0 from tick 7) and 1 on +y; nothing forward |
| -x | 131072 | 14563 | 1618 | 180 | 20 | 3 | 1 unit forward from r = 7 (tick 8), then whole by its momentum: (r + 1, 1) |
| +y | 131072 | 14564 | 1618 | 179 | 20 | 2 | 2 units whole by momentum: (r + 1, 2) for r >= 6 |
| -y | 131072 | 14564 | 1619 | 180 | 20 | 2 | (r + 1, 2) for r >= 6 |

(At r = 1 the three units left go to the lowest ranks from tick 2 among the
five equal remainders, +Y, -Y, +Z, so the +x front's forward share stays at
the floor 14563 while the +y front's takes one, 14564; the chains differ by
those ties only.) The first read of a probe on +x at r = 12 (worlds 1A, 1B,
4, 7) and at r = 8, 12, 16, 20, 24, 30, 40 (5P, 6) is past the front and is
registered, not derived. The push of every first read is -amount x m along
the axis (identity).

## The worlds

| World | Item | Measured events | Intervals | What its record reads |
| --- | --- | --- | --- | --- |
| `1a_m1`, `1a_m4`, `1a_m16` | 1, equivalence | the source; a fixed probe of content m at (72, 60, 0), r = 12 on +x | 200 | the probe's `read` records of number 1: push_m(t) = m x push_1(t) at every tick and axis (identity); the first read (tick, amount) registered |
| `1b_m1`, `1b_m4`, `1b_m16` | 1, equivalence | the same probe free (`fixed` false, momentum 0) | 200 | the `step` records identical for the three m and equal to the rule off the clock on the reads' cumulative push (by_clock(t - 1, \|p\|, m + \|p\|), x before y), one x-step per interval to the merge, one `merged` record, the probe absent afterwards, the source's content 2^24 + m; the ticks registered (the 3-D prior: the first step at the first read, the merge at 2r + 1) |
| `2` | 2, the third law | A = 2^22 at (56, 60, 0), B = 2^20 at (64, 60, 0) | 200 | `pushed` and the `read` pushes per 50-interval window: toward each other; the ratio of the axial pushes in [1.0, 1.5] over the last two windows and the two within 5 %; transverse below 5 % (a reading; 1.28 on 21^3) |
| `3`, `3a`, `3b` | 3, superposition | the item-2 pair with a probe of content 1 at (60, 68, 0); A alone with the probe; B alone with the probe (A is number 1 in `3` and `3a`, B number 2 in `3` and `3b`) | 200 | the probe's records by number in `3` equal those of `3a` and `3b` exactly, its total push the sum (identity) |
| `4` | 4, retardation | the source; probes of content 1 at r = 4 on -x, 6 on +y, 8 on -y, 12 on +x | 200 | the first `read` of each probe (tick, amount, push) against the table above; with `1a_m1`, `7_00` and the +x probes of `5p` and `6` |
| `5` | 5, the far field | the source alone | 300 | replayed through the API over ticks 251-300: the ring means (the Nodes at \|d - r\| < 1/2, about 2 pi r of them) of the count, the flow, the carried radial momentum (the departures' momentum, six Ports and the four in-plane Ports) and the size at r = 4, 6, 8, 12, 16, 20, 24, 30, 40, the flux through the square at h = 4, 8, 12, 20, 40, the escape; the slopes |
| `5_long` | 5, supplementary | the source alone | 1000 | added after world 5 read an escape of 0.89 q (the fixed point not reached at 300): the same readings over ticks 951-1000 and the escape per 100-interval window, the escape's approach to q; not pinned |
| `5p` | 5, the axis pattern | the source; probes of content 1 at r = 4, 6, 8, 12, 16, 20, 24, 30, 40 on +x (all on the source's line, allowed for this item) | 200 | per probe the axis push x 2 pi r / (m q), the count and the size at its Node over ticks 151-200 (a pattern, not the law); the amount read equals the replay's count at every tick |
| `6` | 6, the clock | the probes of `5p` with `suspension` 1 | 200 | age + waited = 200; (age, waited, owed) equal to the replay of the counts read (size x 1 // 32 at each self-creation); no probe frozen (age(200) > age(60)); the lost fraction 1 - age / 200 per r against k / (k + 1) |
| `7_00`, `7_pp`, `7_pm`, `7_mp`, `7_mm` | 7, the electric reading | the source with `charge` Q in 0, +2^23, -2^23; a probe of content 1 at (72, 60, 0) with `charge` q in 0, +2, -2, the family `q` | 200 | every push (m - sign(Qq)) times the uncharged world's, `pushed` [0, 0, 0] for like signs and twice the (0, 0) world's for unlike (identity); electric / gravity = -Qq / (M m) per record |
| `7_pp_m4` | 7, the electric reading | the (+, +) pair with a probe of content 4 at the same Node | 200 | the electric part equal to the content-1 twin's at every record, the gravity part four times |

Why one replay serves worlds 5, 5P and 6: a probe reads (the push taken,
the units mix on as at an empty Node) and nothing in the transit depends on
a charge, a content or the suspension of a measured event (`suspension`
holds only a paid family's arrivals and a measured event's clock), so the
stream of the source's number is the same in the three worlds while no
probe releases (a probe of content 1 releases at age 128; in world 5P its
units are another number and in world 6 no probe's clock reaches 128). The
tool replays world 5 once, checks its books against the record's audit at
every tick, reads the count and the size at the +x axis Nodes at every tick,
and checks on the records of `5p` and `6` that the amount each probe reads
equals that count at every tick.

## Run and analyse

```bash
python examples/events/coupling/make_worlds.py   # rewrites the twenty-one worlds, unchanged
for w in 6 5p 5 4 3 1a_m1 1a_m4 1a_m16 7_00 7_pp 7_pm 7_mp 7_mm 7_pp_m4 2 3a 3b 1b_m1 1b_m4 1b_m16 5_long; do
  python -m event_universe --init examples/events/coupling/$w.json --output artifacts/coupling/$w
done   # four at a time on four cores: 168 s of wall time for the twenty, 63 s more for 5_long
PYTHONPATH=src python tools/coupling_readings.py artifacts/coupling
```

`tools/coupling_readings.py` reads each run's `run.json`,
`initialization.json` and `events.jsonl`, replays worlds 5 and 5_long
through the API (`EventSimulation`, `step`, `shell_readings`, `cube_flux`,
the departures' momentum), prints a table per item and every criterion with
its verdict, and exits nonzero on a failure. Identities are checked on
integers and `fractions.Fraction`; floats appear only in the ripple bounds,
the ring means and the slopes. A negative control (a copy of one run with
one push changed by one unit) must fail.

The preflight of shipped worlds in `tests/test_configuration_validation.py`
covers `examples/events/*.json` one level deep; these worlds are checked by
the preflight CLI (`python -m event_universe.configuration_validation
examples/events/coupling/5.json`, all twenty-one VALID) and by the runner at
every run.

## Result (2026-09-19)

Commit `ddb4470a` (the engine unchanged by this change), source fingerprint
`06a050c9d27a5ab11febe10be40865866e7f0dcbc129400e08c2d7f6b71c8560`, Python
3.14.0rc2, headless; every run completed with the books balanced at every
tick, the measured content constant and age + waited = the intervals
completed; 390 criteria passed, 15 failed, exit 1, every failure a reading
outside its bound and none an identity (the register entry has the numbers
and the verdict per item):

- Item 1, identity held: push_m = m x push_1 at all 185 records and three
  axes for m = 4, 16; the free probes' 11 steps identical and equal to the
  rule off the clock; one merge each. Registered: the first read at tick 15
  (r + 3) with amount 1, the first step at tick 16 (p / (m + p) = 1 / 2
  after one unit, by_clock 0), the merge at tick 27 = 2r + 3 (the 3-D prior
  14, 14 and 25).
- Item 2, reading within the bound: |P_A| / |P_B| 1.256 and 1.213 over the
  last two windows (3.6 % apart), 1.071 cumulative, toward each other,
  transverse / axial 0.009.
- Item 3, identity held exactly (187 records per number).
- Item 4, the front as derived at every derived Node: -x 4 (5, 180), +y 6
  (7, 2), -y 8 (9, 2), +x 4 (5, 180), +x 6 (7, 3); registered on +x past
  the front: r = 8 (11, 8), r = 12, 16, 20, 24, 30, 40 (r + 3, 1), the same
  in every world.
- Item 5, world 5 over ticks 251-300: count x r / q 0.325-0.339 (a
  constant), flow x 2 pi r / q 0.946-1.076, carried x 2 pi r / q 1.434-1.502
  over the six Ports (1.175-1.264 over the four in-plane Ports), size x
  sqrt(r) / sqrt(q) 0.874-0.975; slopes count -0.993, flow -1.048, carried
  -1.014, size -0.481 (all within their bounds); the flux through the
  square / q 0.995, 0.993, 0.988, 0.979, 0.931 at h = 4, 8, 12, 20, 40;
  the escape 0.892 q. Outside the bound: the carried momentum is 1.45 q /
  (2 pi r), not about 1 (the departures' momentum at a Node includes the
  back-scattered shares, which carry outward momentum while moving inward,
  and the stub's returns; the flow reads 1), the flux at h = 20 and 40 and
  the escape at 300 intervals: the fixed point is not reached. World
  5_long: the escape 0.889, 0.918, 0.926, 0.931, 0.940, 0.942, 0.947, 0.947
  q over the 100-interval windows ending at 300 to 1000, still below 0.95
  at 1000.
- Item 6, identity held: (age, waited, owed) equal to the replay at all
  nine radii, age + waited = 200. Outside the bound at r = 4, 6, 20:
  age(200) = age(60); the size on the axis is 100 to 400 whole units, so
  k + 1 exceeds the 200 intervals and a probe self-creates at most once
  after the field builds; the counts written are finite (222, 178, 219,
  131, 62, 43, 134, 21, 8 at the last self-creation) and being paid, no
  clock stopped by the rule.
- Item 7, identity held: like signs `pushed` [0, 0, 0], unlike twice
  (-2634004, 5855, 0), electric / gravity -1 and -1/4 exactly.
- Convergence (a): carried x 2 pi r / q flat within 3.8 % over r >= 5
  (1.454 mean; 1.197 over the in-plane Ports) but not equal to the flow's
  0.988 within 5 %; (c) 0.055, 0.031, 0.034 within their bounds; (d) exact.
