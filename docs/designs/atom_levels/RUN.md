# The three runs of the level worlds (atom-level-v1), read by kind against the pins of LEVELS.md section 5

The Atom Levels Mathematician, 2026-09-22, step 3 of the Boss's order on
the physics-rule reviewer's AGREED of the pins as written at
287df9a10face4457bf983325048b59273eb9ad6 ("the three runs may start under
these pins as written; the reading by kind afterwards, no number moved
after"), under the model owner's word of record 973 and his clock (the
paper closes at about 17:30Z). The worlds: `examples/events/atoms/
hydrogen_r{3,7,12}_level.json`, written by the atoms generator
(`make_worlds.py`, `LEVEL_RADII`), each hydrogen's construction at its
radius under the centred step plus the key `atom_level` and the electron's
`level` declaration (the family `light`, the pair `[512, 1]`, the return at
the +x crossing of the x axis). The pins are [LEVELS.md](LEVELS.md) section
5 (d), R1 to R6, declared before the runs; NO PIN WAS MOVED AFTER THE RUNS.
The reading is the Atom Baseline Runner's method (`baseline_readings.py`,
imported by [level_readings.py](level_readings.py), nothing copied): the
faces' clicks paired into releases, the arrival Nodes, the axis crossings,
the phase increments unwrapped; its printout [level_readings.out](level_readings.out);
the run blocks (the fingerprints, the readings) in
[examples/events/atoms/expectations.json](../../../examples/events/atoms/expectations.json).
Every number DETECTOR (the faces' clicks, the arrival Nodes, the crossings,
the `light` clicks), GAMEBOARD (the engine's `level` lines, the step lines,
the host's tick) or COMPUTATION (the level from two counts, the ratio), as
the reader labels it. Bohr's whole number, Kepler's period and Balmer's
ratio appear only on the comparison side (record 817).

**The side track (the owner's word, record 997, about 15:40Z).** The
atom's levels cannot be read on any lattice we can run (the electron's
radius over the nucleus's is about sixty thousand in nature); the atom
enters the paper by the algebraic formula alone, stated as the algebra's
convergence and not shown in nature, and these runs are the SIDE TRACK's
record beside the paper: the paper does not wait for them and does not
cite them as a reading of the levels. The side track's next design, a
declared scale of the electron's coupling to the proton under its own
identity, is [SCALED_COUPLING.md](SCALED_COUPLING.md).

**The verdict in one line.** The r = 3 electron LEFT the board through
`face:+x` at tick 733 (R1 FAIL: the fan's grain at small r, the named
risk, a finding); the r = 7 loop stays four returns with its first return
at 612 against the generator's 690 (R1 FAIL by the band, 1.3 percent
below its edge) and the level of its first loop 70 against the
generator's 71 (R3 PASS); the r = 12 loop stays five returns (R1 PASS at
1341, the band's edge; R3 PASS at 47, the band's edge) and releases ONCE,
at its fourth return, four `light` rows of content 4 that click on the
four faces with the Planck identity holding on the +x and +y faces (R5
PASS within the declared two steps), its crossings identical to
RUN_CENTRED.md's up to that release (R6 PASS). Two levels give one line
(70 - 47 = 23 steps at `[512, 1]`) and NO RATIO: R4 NOT READ, and NATURE
row 6 stays NOT YET: the paper gets no reading of Balmer's ratio from
these runs, with a band or without.

## 1. The runs

Made on the build's commit b5c40b6c85087ed9ce8b6e015025104f6c95f72a (the
engine of atom-level-v1), the three worlds through the register's runner
in parallel, headless, no render:

    PYTHONPATH=src python tools/run_series.py --jobs 3 --out artifacts/atom_levels examples/events/atoms/hydrogen_r3_level.json examples/events/atoms/hydrogen_r7_level.json examples/events/atoms/hydrogen_r12_level.json

under Python 3.14.0rc2; every run completed with the books balanced at
every tick; the record's `hypotheses` `bohr-v1`, `centred-step-v1`,
`atom-level-v1` and `atom_level: true` on each. The records follow the
24-hour retention policy and are not committed; the printout and the run
blocks are.

| The world | side, ticks | the runner's time (host) | `state.json` sha256 | `events.jsonl` sha256 | the audit sha256 |
| --- | --- | --- | --- | --- | --- |
| `hydrogen_r3_level` | 35^3, 3000 | 54.2 s | 463c6dcfeb662500b0f19298b5907485e1b69be09fdb9b29feb6e58d55149866 | 5b725febb07b3509b46a1ddd3b4e1664e2078170c014e0f309e73540fd394250 | 55ec2ffed4aafe56e39bc8db5cb6ea380f20a83b3bdde3641c125f9ca162899f |
| `hydrogen_r7_level` | 43^3, 3500 | 69.0 s | 627818f12a4ed67b36d0a0bdb1276244a381195fa7ed19bcd4b957e144f3089f | ae7d72bad0199bdc6ff9081ba29fd74ef09493d5c1275f706e39a4d421b742e3 | c60f10581ca2f78b71d0906e761584bf93dbc6fbac56bc0739f4b3cc03918b55 |
| `hydrogen_r12_level` | 53^3, 7500 | 145.3 s (three runs sharing the host) | 4864e4f9c378e0c8962d00057b51258a93b689a16cdeef1dad9082ec48598ba2 | 473be89ddb73909e21ec168d5b444b13cbe460d8be74ff98541f52b93b46bfdc | 58af16252cdb1689 (the full digest in `expectations.json`) |

## 2. What the detectors read, world by world (DETECTOR unless labelled)

**r = 3** (the electron at 3 Links, 21 shells of 17 degrees per loop).
The faces clicked 75, 70, 77, 70 of the electron's rows (71 releases
paired); the axis crossings at 72 (+y, 4 Links), 152 (-x, 3), 192 (-y,
3), 252 (+x, 4), 372 (+y, 4), 432 (-x, 2.24), 452 (-y, 3), then +x at 711
at 17 Links on the way out; THE ESCAPE through `face:+x` at tick 733. The
first return at 252 (the generator's 212; the band 191 to 233: outside);
the loop 252 to 711 is not a closed loop (its "level" 104 by the two
counts, 2.938 circles over 459, is a loop that left). The engine's
`level` line at tick 279 (GAMEBOARD): the action 736 786 408 832 over the
count 279, the level 122, nothing released. The momentum's length at the
crossings 404 to 851 million (GAMEBOARD): the loop was thrown about by
the coarse pulse, as the named risk said it might be. No `light` row.

**r = 7.** The faces clicked 352, 340, 351, 340 (338 releases paired); 17
crossings, the radii 5 to 10 Links; the returns to +x at 612, 1272, 2131,
3051, the periods 660, 859, 920 (the loop widens: the generator's 690);
no escape in 3500 ticks. The loops by the faces' two counts: 612 to 1272:
182 steps unwrapped (2.844 circles) over 660, the level 70; 1272 to 2131:
208 steps (3.250) over 859, 61; 2131 to 3051: 207 steps (3.234) over 920,
57. The engine's `level` lines (GAMEBOARD): 75 at 656 (the first loop
from the birth), then 73, 59, 58 at 1326, 2232, 3130, nothing released
(the level never rose above the first). No `light` row.

**r = 12.** The faces clicked 755, 732, 749, 736 (732 releases paired);
23 crossings, the same 23 as RUN_CENTRED.md's up to the release and near
them after; the returns to +x at 1341, 2772, 4272, 5422, 6441, the
periods 1431, 1500, 1150, 1019; no escape in 7500 ticks. The loops by the
faces' two counts: 1341 to 2772: 264 steps (4.125 circles) over 1431, the
level 47; 2772 to 4272: 262 (4.094) over 1500, 44; 4272 to 5422: 240
(3.750) over 1150, 53; 5422 to 6441: 205 (3.203) over 1019, 51. The
engine's `level` lines (GAMEBOARD): 49 at 1363 (the loop from the birth),
47 at 2777, 47 at 4328, 53 at 5465 with 4 RELEASED (the rise above the
first loop's 49), 51 at 6476 and 50 at 7488 with nothing released (below
the last released 53); the content 1836 to 1820. The release at 5465:
four `light` rows of content 4, one per in-plane heading, clicking on
`face:+x`, `face:+y`, `face:-y` and `face:-x` (the electron at (33, 26,
26), 7 Links from the proton, and the -x row passed the proton's Node to
the face); the Planck identity on the +x and +y faces: the phase
difference 44 against `s x (the age difference) mod N = 44`: HOLDS. After
the release the crossings move by a few counts and Links (5674 against
RUN_CENTRED's 5692, 5977 against 6102, 6441 against 6462) as the content
loss's algebra said they would (the loop shrunk in action, LEVELS.md
section 5 (c)).

## 3. The verdicts against the pins (no pin moved)

| Pin | r = 3 | r = 7 | r = 12 |
| --- | --- | --- | --- |
| R1 the loop stays and returns (no escape; at least three returns; the first return within 10 percent of the generator's T) | FAIL: the escape at 733; the first return 252 outside 191 to 233 | FAIL by the band: four returns, no escape, the first return 612 against 621 to 759 (1.3 percent below the edge) | PASS: five returns, no escape, the first return 1341 in 1341 to 1639 (at the edge) |
| R2 the level off the record (GAMEBOARD, a diagnostic, never counted) | 122 at the first return | 75, 73, 59, 58 | 49, 47, 47, 53, 51, 50 |
| R3 the level of the loop between the first and the second returns from the faces' two counts, within 10 percent of the generator's | FAIL: 104 against 132 to 160, and the loop did not close | PASS: 70 in 64 to 78 (the generator's 71) | PASS: 47 in 39 to 47 (the generator's 43; at the edge) |
| R4 the ratio of two lines (a reported COMPUTATION) | NOT READ: the r = 3 world has no rung's level; two levels give one line, `L_3 - L_4 = 70 - 47 = 23` steps at `[512, 1]` (the generator's 71 - 43 = 28; the `1 / j^2` ladder at the read closures 77 - 44 = 33), and no ratio | | |
| R5 the releases and the Planck identity | none (the loop left) | none (the level never rose) | PASS: one release at the fourth return, 4 steps against the declared 3 (within two), four rows of content 4; the Planck identity on two faces holds (44 = 44); the fifth return 0 against the declared 2 (within two) |
| R6 the control | the build's test (a): the byte identity with the key absent PASS | the same | PASS: the twelve crossings up to the release identical to RUN_CENTRED.md's, count for count and Link for Link |

Counted pins (DETECTOR): R1 one PASS, two FAIL; R3 two PASS, one FAIL; R5
one PASS, two not applicable; R6 PASS; R4 NOT READ; R2 a diagnostic.

## 4. What the runs add, and what they do not (the kinds' honesty)

1. **The rule works as built.** The level is formed at every return, the
   first return sets it and releases nothing, a rise is released as rows
   of the rise's content with their own rate, and the rows' clicks carry
   the Planck identity after a detector (r = 12, one release). The
   engine's levels and the faces' levels agree within a few steps (49 /
   47 / 47 / 53 / 51 against the loops' 47 / 44 / 53 / 51 read on the
   faces between the crossings, the engine's loops running from its own
   return ticks).
2. **The rungs at r = 12 and r = 7 read their levels inside their
   bands.** 47 and 70 steps at `[512, 1]` against the generator's 43 and
   71; the levels of the later loops report the drift (r = 12 tightens as
   RUN_CENTRED read; r = 7 widens, 70, 61, 57 with the periods 660, 859,
   920).
3. **The rung at r = 3 is not a rung on this fan.** The electron left
   the board within four crossings under the pulse of 17 degrees per
   shell; the finding LEVELS.md section 5 (a) named as the risk. No level
   of a closed loop exists there.
4. **No ratio, hence no reading of Balmer's form.** R4 needs three
   levels; the runs give two. The one line between the rungs 3 and 4 (23
   steps against the generator's 28 and the ladder's 33 at the read
   closures) is reported as a computation of two DETECTOR levels and is
   not a line of hydrogen (no transition, no released row of that
   content: LEVELS.md section 6 (1)). NATURE row 6 stays NOT YET; the
   paper's row, if it names these runs, states the two levels, the one
   line and the missing rung, and no ratio.
5. **Not claimed.** Nature; a closed circle at any rung (the closures
   read 4.125, 2.844: not whole); the cause of r = 7's widening and r =
   12's tightening (RUN_CENTRED.md section 4 leaves the residual
   unclaimed); the r = 3 escape's cause beyond the pulse's grain named
   before the run.

## Links

[LEVELS.md](LEVELS.md) (the rule, section 2 (b); the pins, section 5);
[level_readings.py](level_readings.py) and [its printout](level_readings.out);
[the run blocks](../../../examples/events/atoms/expectations.json);
[the worlds and the atoms README](../../../examples/events/atoms/README.md);
[RUN_CENTRED.md](../atom_give/RUN_CENTRED.md) (the control);
[tests/test_atom_level.py](../../../tests/test_atom_level.py) (the byte
identity, the build's readings); [the retention policy](../../RETENTION.md);
records 973, 991 and 994 of [the log](../../LOG_2026-09-20.md).
