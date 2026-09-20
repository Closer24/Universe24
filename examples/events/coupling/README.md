# The coupling series C under the Beam Law, on the plane

Twenty-one worlds of one base, written by `make_worlds.py`; the register
entry is
[C, the couplings under the Beam Law, on the plane (2026-09-19)](../../../docs/EXPERIMENTS.md#c-the-couplings-under-the-beam-law-on-the-plane-2026-09-19)
and the evidence is in [validation](../../../docs/VALIDATION.md). The
physics-rule reviewer pinned the design and its identities on 2026-09-19 for
the law of events; the model owner moved the series to two-dimensional
GameBoards the same day; the Beam Law of the same night re-registers it
with the expectations of [BEAM_LAW section 8](../../../docs/BEAM_LAW.md#8-independent-expectations-for-the-re-registered-readings)
(count x r constant, flow x 2 pi r = 1, the clock's slowing ~ 1 / r on the
plane, the third law exact on lone beams, the front from the flight table,
the 1b merge criteria become the refusal). A research run, made once, never
a test; a reading outside its expectation is reported with its numbers,
never moved. The registered readings of the law of events keep their scope
in the register.

## The base

A GameBoard of 121 x 121 x 1 Nodes with the z axis declared periodic
(`"boundary": {"z": "periodic"}`, [the engine](../../../docs/ENGINE.md)): a
true two-dimensional GameBoard, nothing leaks on z; the x and y faces are open.
The centre c = (60, 60, 0), `"law": "beam"`, K 2^22, N 64, `release`
[1, 128], `suspension` 0 (1 in world 6 only), one free family `m`
(`quantum` 0, the kind following from the quantum) of charge 0 (item 7
declares two free families, `q` for the source and `p` for the probe, each
with its charge per unit of content as a pair `[n, d]`: since 2026-09-20 a
charge is per unit of content of a family and a measured event's charge is
that times its content, so the source's charge 2^23 on 2^24 is the family
charge [1, 2] and the probe's 2 on content 1 is [2, 1]),
every measured event `fixed` unless the item says otherwise, `phase` 0. The
source is a measured event of content 2^24 at c releasing on the six
headings: `by_clock` gives 2^17 per heading at every self-creation; the two
z rays land on the source's own Node at their first walk (the stub of
extent 1) and are home, created again in six equal shares at the next
self-creation, so at the fixed point the net emission into the plane is
q = 6 x 2^17 = 786432 units per interval, exact, in four beams of 3 x 2^16
per interval on the in-plane headings. Under the Beam Law a beam does not
spread: the ring's Nodes off the four in-plane axes are empty, a ring mean
is the axial Nodes' reading over the ring's Node count, and the count on an
axis is constant with r. A probe is a measured event of content 1 (m in
item 1) with the table the keys give (`read` for a free family: the push
taken, the rays go on; no table declared), so a probe is transparent to the
beam it reads. A probe
releases six lone rays at age 128 / m along its six GameBoard lines; the tool
filters records by `number`.

## The front from the flight table (item 4)

A ray released at tick t first walks at t + 1; the flight table of the
heading (1, 0, 0) (T 110, L 55) reaches m Links at the walks 1, 3, 5, 7, 8,
10, 12, 13, 15, 17, 19, ... (`tests/test_nature_beam_flight.py` (a)), so the front
of a beam reaches r at tick 1 + (the first arrival at r Links), whole:
2^17 at every r (a ray does not spread; no chain). r = 4: tick 8; 6: 11;
8: 14; 12: 21; 16: 28; 20: 35; 24: 42; 30: 52; 40: 69. Two rays of the beam
sit at a Node at the ages where the table waits (the mean stay 1 / c =
1.73 intervals per Link), so the presence at an axial Node is one or two
rays of 2^17.

## The worlds

| World | Item | Measured events | Intervals | What its record reads |
| --- | --- | --- | --- | --- |
| `1a_m1`, `1a_m4`, `1a_m16` | 1, equivalence | the source; a fixed probe of content m at (72, 60, 0), r = 12 on +x | 200 | the probe's `read` records of number 1: push_m(t) = m x push_1(t) at every tick and axis (identity); the first read at tick 21 with amount 2^17 (the front) |
| `1b_m1`, `1b_m4`, `1b_m16` | 1, equivalence | the same probe free (`fixed` false, momentum 0) | 200 | the `step` records identical for the three m and equal to the rule off the clock on the reads' cumulative push (by_clock(t - 1, \|p\|, m + \|p\|), x before y), one x-step per interval from the first read (tick 21) to the Node beside the source (x = 61 at tick 31), every further step refused (no merge since 2026-09-19), no `merged` record, the probe present at the end |
| `2` | 2, the third law | A = 2^22 at (56, 60, 0), B = 2^20 at (64, 60, 0) | 200 | `pushed` and the `read` pushes per 50-interval window: toward each other; the same reading ticks; per tick \|push_A + push_B\| / \|push_A\| below 1 % (the grain of the whole apportioning of 2^15 and 2^13 over six headings); cumulative \|P_A + P_B\| / \|P_A\| below 1e-4; zero over the first window |
| `3`, `3a`, `3b` | 3, superposition | the item-2 pair with a probe of content 1 at (60, 68, 0); A alone with the probe; B alone with the probe | 200 | the probe's records by number in `3` equal those of `3a` and `3b` exactly, its total push the sum (identity); off both axes the probe reads nothing (the beams do not spread) |
| `4` | 4, retardation | the source; probes of content 1 at r = 4 on -x, 6 on +y, 8 on -y, 12 on +x | 200 | the first `read` of each probe (tick, amount, push) against the flight table above; with `1a_m1`, `7_00` and the +x probes of `5p` and `6` |
| `5` | 5, the far field | the source alone | 300 | replayed through the API over ticks 251-300: the ring means (the Nodes at \|d - r\| < 1/2) of the count, the presence and the flow at r = 4, 6, 8, 12, 16, 20, 24, 30, 40, the flux through the square at h = 4, 8, 12, 20, 40, the escape; the slopes; the readings against BEAM_LAW section 8 |
| `5_long` | 5, supplementary | the source alone | 1000 | the same readings over ticks 951-1000; not pinned |
| `5p` | 5, the axis pattern | the source; probes of content 1 at r = 4, 6, 8, 12, 16, 20, 24, 30, 40 on +x | 200 | per probe the axis push x 2 pi r / (m q), the count and the presence at its Node over ticks 151-200 (the beam's Nodes); the amount read equals the replay's count at every tick |
| `6` | 6, the clock | the probes of `5p` with `suspension` 1 | 200 | age + waited = 200; (age, waited, owed) equal to the replay of the presence read (`by_clock(age, k, 1)` at each self-creation); the clock counts until the front's arrival and is then owed the beam's presence (2^17 or 2^18) for the rest of the run: the accepted price on the axis, registered |
| `7_00`, `7_pp`, `7_pm`, `7_mp`, `7_mm` | 7, the electric reading | the source (the family `q`, `charge` [0, 1], [1, 2], [-1, 2] per unit of content: Q = 0, +2^23, -2^23 on its content 2^24); a probe of content 1 at (72, 60, 0) (the family `p`, `charge` [0, 1], [2, 1], [-2, 1]: q = 0, +2, -2) | 200 | every push (m - sign(Qq)) times the uncharged world's, `pushed` [0, 0, 0] for like signs and twice the (0, 0) world's for unlike (identity); electric / gravity = -Qq / (M m) per record |
| `7_pp_m4` | 7, the electric reading | the (+, +) pair with a probe of content 4 at the same Node (the family `p` of `charge` [1, 2]: q = 2 on content 4) | 200 | the electric part equal to the content-1 twin's at every record, the gravity part four times |

Why one replay serves worlds 5, 5P and 6: a probe reads (the push taken,
the rays go on) and nothing in the flight or the collision depends on a
charge, a content or the suspension of a measured event, so the stream of
the source's number is the same in the three worlds while no probe releases
(a probe of content 1 releases at age 128; in world 5P its rays are another
number and in world 6 no probe's clock reaches 128). The tool replays world
5 once, checks its books against the record's audit at every tick, reads the
count, the presence and the flow at the +x axis Nodes at every tick, and
checks on the records of `5p` and `6` that the amount each probe reads
equals that count at every tick.

## Run and analyse

```bash
python examples/events/coupling/make_worlds.py   # rewrites the twenty-one worlds, unchanged
python tools/run_series.py --jobs 4 --out artifacts/coupling examples/events/coupling/*.json
PYTHONPATH=src python tools/coupling_readings.py artifacts/coupling
```

`tools/coupling_readings.py` reads each run's `run.json`,
`initialization.json` and `events.jsonl`, replays worlds 5 and 5_long
through the API (`NatureBeamSimulation`, `step`, the count, presence and flow
arrays, the flux through the square), prints a table per item, every
criterion with its verdict (an identity, a book, a timing off the flight
table: a failure exits nonzero) and every reading against the expectations
of BEAM_LAW section 8 with its verdict (inside or outside; registered, never
a failure). Identities are checked on integers and `fractions.Fraction`;
floats appear only in the ring means, the slopes and the readings' bounds.

## Result under the Beam Law (2026-09-19)

Branch `claude/universe24-new-3ytqde`, the Beam Law's commits on the base
`ce0b22af`, source fingerprint `703f9427d9f70e6c619218e457edca0b7647381a8cc7a20d140e4a3d9dd3f671`, Python 3.14, headless;
every run completed with the books balanced at every tick, the measured
content constant and age + waited = the intervals completed, 0.5 to 3.3 s
per run (21 runs in about 20 s, four at a time); 392 criteria passed, 0
failed, exit 0; 19 readings inside the expectation, 9 outside, registered:

- Item 1, identity held: push_m = m x push_1 at all 180 records and three
  axes for m = 4, 16; the first read at tick 21 with amount 131072 (the
  front of the flight table at 12 Links); the free probes' 11 steps
  (ticks 21 to 31, x from 72 to 61) identical and equal to the rule off the
  clock; the steps onto the source refused, no `merged` record.
- Item 2, the third law: the cumulative pushes 9612145197056 and
  -9612088573952 on x, the ratio 1.0000 at four decimals, the sum 5.9e-6
  of the push; per tick the difference at most 0.05 % (the grain of the
  whole apportioning); zero over the first window.
- Item 3, identity held exactly (0 records: the probe at (60, 68, 0) sits
  off both beams' axes, so under the Beam Law it reads nothing; the identity
  holds trivially and is registered as such).
- Item 4, the front at every probe as the flight table gives it: r = 4
  tick 8, 6 tick 11, 8 tick 14, 12 tick 21, 16 tick 28, 20 tick 35, 24 tick
  42, 30 tick 52, 40 tick 69, amount 131072 whole in every world.
- Item 5, world 5 over ticks 251-300 (q = 786432): count x r / q 0.125,
  0.150, 0.167, 0.176, 0.143, 0.179, 0.167, 0.150, 0.152 at r = 4 to 40
  (the ring's Node count: r / Nodes; 0.1592 = 1 / (2 pi) in the mean),
  presence / count 2.000 at every r >= 6 (1.000 at r = 4), flow x 2 pi r /
  q 0.785, 0.942, 1.047, 1.109, 0.898, 1.122, 1.047, 0.942, 0.952; the
  slopes count -0.944, flow -0.944, presence -0.760; the flux through the
  square / q 1.0000 at h = 4, 8, 12, 20, 40 and the escape 1.0000 q (Gauss
  exact, a ballistic stream). Outside the expectation: the ripple of
  count x r / q over r >= 8 is 0.25 (bound 0.10) and count x r / q at
  r = 16 is 0.143 (bound 0.15 to 0.19): the rings at r = 16 and r = 20 both
  have 112 Nodes, so the six-beam ring mean follows the GameBoard ring's
  Node count and not r; flow x 2 pi r / q at r = 12, 16, 20 (1.109, 0.898,
  1.122) outside 0.90 to 1.10 for the same reason; the presence slope
  -0.760 outside -1.00 +- 0.10 (the presence at r = 4 is one ray, at
  r >= 6 two). World 5_long over ticks 951-1000: the same numbers.
- Item 5P, the axis pattern: -push_x x 2 pi r / (m q) = 2 pi r / 4 exactly
  (a beam of q / 4 per interval at every r: 6.28, 9.42, 12.57, 18.85, 25.13,
  31.42, 37.70, 47.12, 62.83 at r = 4 to 40), count x r / q = r / 4, the
  presence 196609 at r = 4 and 393216 to 393217 at r >= 6; the amount read
  equal to the replay's count at every tick at every probe.
- Item 6, the clock: identity held, (age, waited, owed) equal to the replay
  at all nine radii, age + waited = 200; the clock counts until the front's
  arrival (age(200) = 8, 11, 14, 21, 28, 35, 42, 52, 69 at r = 4 to 40,
  the front's ticks) and is then owed 130880 to 130941 intervals (the
  beam's presence 2^17 or 2^18 read at one self-creation): the accepted
  price of the design (section 8, item 6: on the axis the presence does not
  fall with r; off the axis a Node reads nothing). The reading "the count's
  share lost against k / (k + 1) with k = q / (6 r)" is inside the
  expectation at every r (0.96 to 0.66 against 0.9999 to 0.9997), which
  says only that the clock is not frozen from the start.
- Item 7, identity held: like signs `pushed` [0, 0, 0], unlike twice
  (-70582384, 0, 0), the content-4 probe 3 times; electric / gravity -1
  and -1/4 exactly.
- Convergence: (a) flow x 2 pi r / q mean 1.0075 over r >= 5, the ripple
  0.25 outside 0.10 (the ring count); the mean stay presence / count 2.00
  against 1 / c = 1.73 (the table's waits fall on whole intervals);
  (c) |slope_count - slope_flow| 0.000, |slope_presence - slope_count|
  0.18 outside 0.10; (d) exact.

Under the contact through the table (2026-09-20) the free probes of
`1b_m1`, `1b_m4` and `1b_m16` step as registered and, from tick 32,
hand the x component of their momentum to the fixed source at every
refused step (169 `contact` records; the probe's momentum 0 at the end
where it grew without bound); the other worlds are byte-identical
([validation](../../../docs/VALIDATION.md#the-columns-the-lifetime-the-held-content-and-the-contact-through-the-table-the-66-example-worlds-compared---2026-09-20)).

## Result under the label along the unit vector (2026-09-19)

The label of a unit along a heading is 64 e_d since the model owner's
decision of 2026-09-19 (the label along the unit vector u_d of the
direction at the flight table's scale Q = 64,
[BEAM_LAW section 2](../../../docs/BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file)
and note 23), so every push, momentum and momentum book line of these
worlds' records is the registered one times 64 exactly (the series 7
electric part included), while the counts, the presences, the clock and
Gauss's flux off the Port crossings are unchanged; the tool divides the
labels by Q where it compares with q or an amount and reads the step
rule as `by_clock(t - 1, |p|, 64 m + |p|)`. The twenty-one worlds
(unchanged files) run on the source fingerprint
`0eaa589ab51cdc0a12a863cd23e535e1e8ac052e8b4f3f8facf30ef05a323c5a`, Python 3.14, headless, 0.3 to 2.5 s per run: 392
criteria passed, 0 failed, exit 0; 19 readings inside the expectation, 9
outside, every reading equal to the result above. In label units: item
1's first read (21, 131072, (-8388608, 0, 0)), `pushed` (-2258636288, 0,
0) for m = 1; item 2 P_A = (615177292611584, 0, 0), P_B =
(-615173668732928, 0, 0), the ratio 1.0000 and the sum 5.89e-6 of the
push; item 7 unlike signs (-4517272576, 0, 0), the content-4 probe
(-6775908864, 0, 0). The register entry records it.

## Result under the law of events (2026-09-19, history)

Commit `ddb4470a`, source fingerprint
`06a050c9d27a5ab11febe10be40865866e7f0dcbc129400e08c2d7f6b71c8560`, Python
3.14.0rc2: 390 criteria passed, 15 failed, every failure a reading outside
its bound (the register entry has the numbers): the equivalence and the
superposition identities held, the third law 1.21 to 1.26, the front the
lone-arrival chain 131072, 14563, ..., count x r / q 0.33 constant, flow x
2 pi r / q 0.95 to 1.08, the carried momentum 1.45 q / (2 pi r), the clock
frozen at r = 4, 6, 20. The engine of that run is deleted
([migration](../../../docs/MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1));
the readings keep their scope.

## Re-read under the step drive (2026-09-20)

The free probes of `1b_m1`, `1b_m4` and `1b_m16` make the same 11 steps
to the Node beside the source one interval later than registered (the
ticks 22 to 32 in place of 21 to 31) and hand their x component over from
tick 33 (168 `contact` records in place of 169 from tick 32); the reads
are the same; the eighteen other worlds have no free body and read the same (the
record's new fields aside). The register entry has the momenta ([migration](../../../docs/MIGRATION.md#the-step-drive-on-2026-09-20-the-count-of-links-as-the-whole-part-of-the-driven-distance)).

## Re-read under rule (a) (2026-09-20)

Under rule (a) of the suspension (record 128: a waiting body neither
releases nor reads) item 6 alone changes, in what is not registered: the
probes' clocks count as registered (age 8 to 69 at r = 4 to 40 after 200
intervals), and each probe reads the beam's presence once (`read` total
131 072) instead of at every waiting interval; the other worlds declare no
suspension ([migration](../../../docs/MIGRATION.md#the-step-drive-on-2026-09-20-the-count-of-links-as-the-whole-part-of-the-driven-distance)).
