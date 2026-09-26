# The atom's baseline run: hydrogen at r = 12 as the law stands, the pins before the run and the clicks after it (the owner's "go for it" of record 886 on record 884 (2))

The Atom Baseline Runner, 2026-09-22, on the Boss's bounded order of about
10:40Z: ONE run of the atoms series' hydrogen world at r = 12 as the law
stands today, no new rule, the clicks read as a baseline before the atom's
stability rule (atom-give-v1, record 881, designed elsewhere and not touched
here). Step 1 (this section, committed before any run): the world as
registered, the detectors, what a click reads, and the pins from
[the atom's algebra](https://github.com/Closer24/Universe24/blob/643b7ae7d4aeac2062518146aeb6e8b6f2998148/docs/designs/atom_algebra/ALGEBRA.md) (branch atom-algebra at 643b7ae7, PR #823; the path docs/designs/atom_algebra/ALGEBRA.md on `main` once it merges) (sections 1, 2, 3 and 7),
every number GAMEBOARD by formula until a detector clicks. Step 2 (section
4, written after the run and never editing a pin): the clicks read by kind,
PASS or FAIL against each pin. Nothing here is compared with nature;
[NATURE row 6](../../NATURE.md) stays NOT YET; Bohr's and Balmer's forms
appear only on the comparison side, never as an input (record 817). The
law as it stands: `origin/main` at the commit this branch starts from
(af39be60f5b04dd0c653172f65af8eb14b21cca0); the engine and the world file
are not changed.

**The six lines (the report's head; every number DETECTOR or GAMEBOARD).**

1. *The information.* The electron (a body of content 1836 on three Nodes,
   momentum **p** = (0, 293 783 192, 0) in label units) circles the fixed
   proton under the push of the proton's free rows read at its own Nodes
   (one row per direction of the fan every 10 intervals); at every Link it
   steps, its action row of that axis gains `abs(p_a) N` and the whole part
   over h turns its phase; every 10 of its self-creations it releases one
   unit on each in-plane heading from one Node of its set, stamped with its
   phase, which flies at one Link per interval on its digital line to a side
   face of the open cube and clicks there with its Node, its count and its
   phase; the row on -X from its middle Node, when that Node is on the +x
   axis, passes the proton's Node, where the proton's table reads it (the
   push taken, the row going on) and its `read` line is written. Nothing is
   kept at a Node; the tick is lost (GAMEBOARD).
2. *The generic solution.* None new: the law's own primitives as registered
   (the drive per axis with the wall `Q S M + abs(p_a)`, the bilinear push
   on the charge column, one action accumulator per axis divided by the
   declared h, the release on the declared pair, the click at a detector
   Node), every family alike; the run adds the one integer the algebra
   cannot give, whether the loop closes on the lattice under the declared
   integers (ALGEBRA.md section 7).
3. *Why it will work, and what refutes it.* The phase stamped on the rows
   of a closed loop repeats at the same axis every return; the faces read
   the electron's position per release as the arrival Node (the loop as a
   set of detector Nodes), the count between two same-axis crossings (the
   period) and the phase per row (the circles per return). The reading
   that shows the closure: j = 4.00 within the release grain and the
   residue per return within 3 steps of 64; the reading that refutes it: a
   residue beyond that, or a loop that does not return (the register's
   precedent at r = 12 under the drive on `main`: left through `face:+x` at
   2059, GAMEBOARD, series H).
4. *Why do this at all.* It gives the baseline the stability rule's design
   will be read against: what the detectors read of the atom as the law
   stands (the dwell, the period, the returns, the closure's residue), so
   that a run under atom-give-v1 is compared with a registered reading and
   not with a formula alone; without it the design's first run would have
   no clicks to move from.
5. *The Highlights.* Kept: the click as the one operation (P6), a detector's
   reading as the only measurement (record 281), reality is the detectors
   (record 721), the detector's own count at the click (record 754), Bohr's
   form on the comparison side only (record 817), whatever can be computed
   algebraically is computed algebraically (record 762: every pin below is
   the algebra's number); nothing here asks a line to change.
6. *The implementation.* No engine line, no world file changed, no pin moved
   after the run; one design folder (`docs/designs/atom_baseline/`: this
   file and the host reading script), one index row, the register's atoms
   README and EXPERIMENTS.md gaining the baseline's numbers by kind after
   the run; the run about 60 s and a few hundred megabytes of records
   (host, series H's cost, atoms/PINS.md section 5); nothing is dangerous:
   no identity, no key, nothing on by default.

**Notation** (skills/workflow.md, "Notation"). Q = 64 the label's scale; S
= 45 120 the width of the push; M = 1836 the electron's content; N = 64 the
steps of the phase circle; h = 5 536 242 544 the world's action; **p** the
electron's momentum vector in label units, `p_a` its component on the axis
a, `abs(p)` its length; r the radius in Links; a the semi-major axis of a
loop; j the circles the phase turns per return; T the count between two
crossings of one axis (the period); k the count between two hops of the
body on one axis (the dwell per Node); `m_i = Q S M` the drive's inertial
constant; `kappa` the push's constant of the shell mean (ALGEBRA.md section
2 (a)); pi the circle's ratio; `floor(x)` the whole part; `sqrt(x)` the root
(the limit's, never the GameBoard's); `f(L)` the flight table's least age
at which a row on a heading has made L Manhattan steps (the engine's own
`Flight.manhattan_steps`).

## 1. The world as registered (nothing changed)

The file: examples/events/atoms/hydrogen_r12.json (`examples/events/atoms/hydrogen_r12.json`, deleted 2026-09-26),
`model_id` `rays-atoms-hydrogen-r12-form-b-v1`, written by
make_worlds.py (`examples/events/atoms/make_worlds.py`, deleted 2026-09-26) on series
H's base (the atoms README (`examples/events/atoms/README.md`, deleted 2026-09-26);
[atoms/PINS.md](../atoms/PINS.md) section 1).

| The key | As declared | Kind |
| --- | --- | --- |
| `law`, `shape`, `boundary` | beam; 53^3 Nodes, the centre c = (26, 26, 26); open on every face, the six faces `wave` detectors | declared |
| `ticks` | 7500 intervals (the run's length) | declared |
| `K`, `N` | K = 2^30 = 1 073 741 824 (the clock's pair [1, K]: the electron's own clock turns 0 within the run); N = 64 | declared |
| `release`, `suspension`, `width`, `action` | the release pair [1, 18360] (one unit per 10 self-creations for a content of 1836: `by_clock(age, 1836, 18360)`); `suspension` 0 (no owed count: the push alone moves the electron, and every detector's count is one per interval, r = 1, record 754); S = 45120; h = 5 536 242 544 (h_B = 16 p_B(8), the action re-fixed under form B by series H's rule, atoms/PINS.md section 2) | declared |
| `directions` | the fan of 2616 primitive directions with 1016 <= abs(D)^2 <= 1032 | declared |
| the families (families.json (`examples/events/entities/families.json`, deleted 2026-09-26)) | `p` the proton: quantum 0 (free), `charge` [1, 1], no phase circle; `e` the electron: quantum 0 (free), `charge` -15, a phase circle | declared |
| the proton (measured event 1) | family `p`, amount 1836, `fixed`, at c, releasing on the whole fan; its table the default of the keys: a free family's rows are `read` (the push taken, the row goes on; `world.default_rule`); it declares no `rerelease` and no `measure` | declared |
| the electron (measured event 2) | family `e`, amount 1836, phase 0, at (38, 26, 26) = (c + 12, c, c), **p** = (0, 293 783 192, 0), `span` [1, 1, 3] (the Nodes z = 25, 26, 27), `phase_by_momentum` under h, `directions` the four in-plane headings +-X, +-Y; its table the default (`read`) | declared |
| `detectors` | `at_proton`: the proton's Node (26, 26, 26), `wave`, threshold 1 | declared |
| not declared | `drive_b` (form B's directional drive, `drive-b-v1`, a key off by default: the run is under the drive on `main`, the signed step drive with the wall `Q S M + abs(p_a)`); no lamp, no paid family, no `measure` entry (section 7's click is not part of the baseline); no `phase_per_link` on `e` (its rows carry the phase stamped at release and turn no further) | absent |

The momentum 293 783 192 was derived by atoms/PINS.md for the circular
orbit under form B's pace; under the drive on `main` the circular momentum
at r = 12 is 288 249 497 (series H), so the declared momentum is 1.0192 of
the circle's: the start is the loop's perihelion and the loop is slightly
eccentric (section 2, pin P2). The world is run as registered: the momentum
is a declaration of the register, not a pin, and is not changed.

## 2. The detectors, and what a click reads

**The detector set.** The world already declares the register's set, and
that set is used with no change to the world file: `at_proton` (one Node,
`wave`) and the six face detectors of the open cube (`face:+x`, `face:-x`,
`face:+y`, `face:-y`, `face:+z`, `face:-z`, `wave`, [ENGINE.md, "An open
face is a detector"](../../ENGINE.md#per-axis-gameboard-topology-2026-09-19-implementation-amendment)).
A passive detector at every Node (record 721) is not a declaration the
world file can carry today: the validator refuses "a detector on a Node
without a measured event" and "a Node in two detectors" ([ENGINE.md, the
world file's refusals](../../ENGINE.md#the-beam-law-beam-v1-the-ray-laws-record-cancelled-docscancelled_worldsmd-the-engine-has-no-laws-name-item-70)), and record 721
is the owner's idea put to him with no engine line; so the order's
"whichever the world file already declares" is the register's set, and
nothing is added. The faces are the per-Node reading this world has: every
row the electron releases ends at a face Node, and the face Node's
coordinates are the electron's own across the flight (record 839: the
arrival Node on Nodes that are detectors).

**What a click reads (the readings by type, [ENGINE.md](../../ENGINE.md#the-detectors-readings-by-type)).**

| The line | What it carries | Kind |
| --- | --- | --- |
| a `click` line on a face (family `e`) | `tick` (the detector's count, one per interval at r = 1), `node` (the arrival Node on the face), `phase` (the electron's phase at the release: the family has no `phase_per_link`), `amount` 1, `momentum` (the row's label), `content` 0 (a free row) | DETECTOR |
| the `detectors` entries of `run.json` | per detector and family: `clicks` (the units that ended at the set), `measured` (0: no family is measured), `record` (the square of the coherent pointer, accumulated), `phase` at the last click | DETECTOR |
| a `read` line of the proton (`measured` 1, `detector` `at_proton`, family `e`) | `tick`, `node`, `amount`, `push` (the push the fixed proton took, which moves nothing), `content` 0, `reading`; no phase (a free row carries no record, so no `rows` field is written); `at_proton`'s own `clicks` for `e` stay 0 under `read` (the click line is the `measure` path's, `nature_beam._apply_plans`) | DETECTOR (a measured event's own record) |
| a `read` line of the electron (`measured` 2, family `p`) | the pushes it took, the arrivals it read | DETECTOR (its own record) |
| a `click` line with `measured` 2 on a face | the electron's escape by its step (the finding, if it happens) | DETECTOR |
| a `step` line of the electron | its Node before and after, its momentum, its phase after the step, its drive rows | GAMEBOARD (the host's view of the body's record; a diagnostic, printed beside, never pinned) |
| the final `measured` state of `run.json` | its position, momentum, `pushed`, `steps`, `phase_steps`, and under `acc` the three `action` accumulators (the per-axis remainders below h at the end) | GAMEBOARD |

**The reading method, fixed here and implemented in
baseline_readings.py (`docs/designs/atom_baseline/baseline_readings.py`, deleted 2026-09-26) before the run.** (i) The
releases: each `face:+x` click (Node y) is paired with the `face:+y` click
(Node x) of the same release by the flight table's delays, `t1 - f(52 - x)
= t2 - f(52 - y)` within 3 counts, the same phase and the same z (the z was dropped
after the run: section 4's note); the
release's count is that common value and the electron's position at it is
(x, y), read at two detector Nodes. (ii) The crossings: a pass of y through
26 with x > 26 is a crossing of the +x axis (the start's), with x < 26 of
the -x axis; a pass of x through 26 with y > 26 of +y, y < 26 of -y. (iii)
The period T: the count between two successive crossings of one axis; the
returns: the +x crossings after the start. (iv) The dwell: on the face that
carries the coordinate of motion at a crossing, the count from the first
click at one Node to the first click at the next, over the hops within two
Nodes of the crossing; the grain is the release period, 10 counts, so one
hop reads 10, 20 or 30 and the mean over the hops read is the reading. (v)
The closure: the increments of the phase between successive releases,
unwrapped (below N / 2 = 32: the formula's 1.75 steps per release), summed
over one return and divided by N, the circles per return j; the residue
in steps of 64. (vi) The proton's reads per crossing. The step lines give
the same quantities as GAMEBOARD diagnostics, printed beside with "agrees"
or "differs" and never counted.

## 3. The pins by formula (GAMEBOARD by formula until a detector clicks; nothing moved after the run)

The arithmetic is the algebra's, on the drive on `main` (the wall `Q S M +
abs(p_a)`, `Q S M` = 5 301 780 480), with the world's declared integers;
the roots and pi are the limit's, on paper; every number below is a
formula's value, DETECTOR only once read.

| Pin | The formula (ALGEBRA.md) | The value | The tolerance | The detector reading that meets it |
| --- | --- | --- | --- | --- |
| P1 the dwell per Node on the loop | `k = 1 + Q S M / abs(p_a)` on the axis of motion at a crossing (section 3 (b), Theorem 3 (iii); the two-valued gaps floor(k) and floor(k) + 1) | 19.05 counts per Link at the start's crossing (`abs(p)` = 293 783 192); 20.5 at the far crossing of the limit's loop (`abs(p)` there 0.925 of the start's, the loop of P2); the order's 19 to 20 is the start's | the mean over the hops read within 2 counts of the bracket: 17 to 22.5 (the grain of one hop is 10, the release period; the mean over n hops has the spread 5 / sqrt(n)) | the faces' first-click-to-first-click counts about the crossings, method (iv) |
| P2 the period and the returns | the limit's loop from the declared momentum: `E = p^2 / (2 m_i) - kappa / r` with `p / p_c = 1.0192` gives `a = r / (2 - (p / p_c)^2) = 12.48` Links (the perihelion 12, the aphelion 12.97), `T = T_c (a / r)^(3/2)` with `T_c = 2 pi r / v_c`, `v_c = p_c / (Q S M + p_c)` = 0.05156, `T_c` = 1462 (section 2 (a), (b)) | T = 1552 counts; over 7500 counts `floor(7500 / T)` = 4 returns to the +x axis (5 if T is at or below 1500) | T within 15 percent (series H's criterion): 1319 to 1785; the returns 4 or 5, every period read inside the bracket; P2b: every return within r / 4 = 3 Links of the start (series H) | the +x crossings' counts and their differences, method (ii), (iii); the arrival Nodes at the crossings |
| P3 the closure at r = 12 | the action rows' gain over a return, `sum over the Links stepped of abs(p_axis) = j h` (section 1 (a)); in the shell mean the sum is the line integral of **p**, `2 pi p r / h` on the circle with the declared p, `2 pi sqrt(kappa m_i a) / h` on the limit's loop (section 2 (b)) | j = 4.001 on the circle, 4.004 on the limit's loop: j = 4.00; the residue per return 0.06 steps of 64 | j within 0.05 (three steps of 64: the crossing's grain is one release, 1.75 steps, and the two ends of a return give twice that); P3b: the residue per return within 3 steps of 64 | the rows' phases per release unwrapped and summed over a return, method (v) |
| P3c the per-axis closure (a GameBoard diagnostic, not counted) | on a loop symmetric in x and y the two axes' gains are each `j h / 2`, the quotients `j N / 2` = 128 each, whole; z gains nothing (section 1 (a)) | x 128.0, y 128.0, z 0 quotients of h per return; the fraction 0 on each axis | agrees within 0.05 of whole on each axis | the step lines' sums (GAMEBOARD, an approximation: the crossed Links only, the counts lost to a coincident fire not on the lines); the final `acc.action` remainders |
| P5 the proton's reads per crossing | one unit per release from one Node of the set in turn (`apportion_whole`, the leftover to the Nodes counted from age mod 3), so one release in three is from the middle Node; 1.9 releases fall in a dwell of 19 counts at the crossing Node: 0.63 reads per crossing in the mean | 0 to 2 reads per crossing, about 2.5 per return, about 12 over the run if the loop stays | every crossing read within 0 to 2 | the proton's `read` lines of family `e` within 60 counts of each crossing plus the flight (f(12) = 20), method (vi) |
| P6 the clicks per face | 7500 / 10 = 750 releases, one unit per heading each, every unit ending at the face its heading faces (the flight is blind, one Link per interval on the digital line, nothing between the electron and the face but the proton, which reads and passes) | 750 clicks of `e` on each of `face:+x`, `face:-x`, `face:+y`, `face:-y`; 0 on `face:+z`, `face:-z`; `at_proton` `clicks` 0 for `e` (read, not measured) | exact, less the rows still in flight at 7500 (at most 7 per face: the last release at 7500 arrives after it) | `run.json` `detectors`, the faces' `click` lines |

The reads of the electron (its own `read` lines of the proton's rows) and
the faces' clicks of the proton's rows (2616 per 10 intervals, about 1.96
million over the run less those in flight) are reported, not pinned. The
radius over the run is a GameBoard diagnostic (the step lines) and says
only whether the loop stays: by formula the limit's loop runs between 12
and 13 Links; the register's precedent at this radius under the drive on
`main` (series H's `r12`, the circle's momentum and the registered h) is an
escape through `face:+x` at 2059 without a closing (GAMEBOARD), so a loop
that does not stay is the finding and no pin is moved for it. The reading
the algebra named as deciding section 1 (a) on the lattice (section 7) is
P3's residue before any click.

**The fail clauses.** A run not completed or the books off at any tick (a
record check, the tool fails). A pin read outside its tolerance is FAIL in
the same font as PASS, with its number, and is never moved.

**The three tests.** No rule is added: every rule the run exercises is the
law's as registered, each already read against the three (ALGEBRA.md
section 5's table); the host script is a reader of records and no rule.

**Host.** Python 3.14 (`.python-version`), the checkout's `src`; the
register's runner `tools/run_series.py` with one job, `--out
artifacts/atom_baseline`, no render, no frames; the reading by
`baseline_readings.py` on the run folder. About 60 s and a few hundred
megabytes of records (series H's r12), within the order's half hour.

## 4. The run and the clicks (written after the run; no pin above edited)

Run on 2026-09-22 at about 09:25Z on the branch's first commit
(0ee54703, the engine and the world file those of `origin/main` af39be60):
`PYTHONPATH=src python tools/run_series.py --jobs 1 --out
artifacts/atom_baseline examples/events/atoms/hydrogen_r12.json` under
Python 3.14.0rc2 (`uv`-installed; the host offered no 3.14), headless, no
render, no frames; completed, 7500 ticks, the books balanced at every tick,
70.8 s of the runner, 124 MB peak (host), 369 MB of `events.jsonl`; the
fingerprint `state.json` sha256 7664a7129be6322e4a35bcf67aca80f2fd699f60cae421b6bd2b15ce68983c59,
the ledger e62c4d48ef87294091320b3d7cf54607924ef96bbd6e86b6c3cb6a68e558ed63,
`events.jsonl` 24e6ae816901cc365193448b9bd69834e6a08664d292f0e6d4566291981b178a.
The reading by baseline_readings.py (`docs/designs/atom_baseline/baseline_readings.py`, deleted 2026-09-26) (the method of
section 2; two reader fixes after the run, neither a pin: the `escaped`
list's shape in `run.json`, and the four units of one release landing on
different Nodes of the set by the Nodes' claims, so the pairing no longer
asks the same z); its printout is [baseline_readings.out](baseline_readings.out).
No pin above was edited.

**The verdict in one line.** The loop does not stay: as the law stands
the electron widens every quarter turn (the crossings at 13, 13, 17 and 26
Links from the proton's Node, DETECTOR) and leaves through `face:+y` at
count (the tick at r = 1) 3407 (DETECTOR), so no return, no period and no closure are read;
the dwell about the three crossings inside r = 17 reads 20.0 counts per
Link; the proton read one row per crossing; four pins FAIL, two NOT READ, one PASSES;
nothing is moved, nothing is compared with nature, NATURE row 6 stays NOT
YET.

**What the clicks read (DETECTOR unless labelled).**

| The reading | The number | Kind |
| --- | --- | --- |
| the clicks per detector, family `e` | `face:+x` 342, `face:-x` 337, `face:+y` 342, `face:-y` 339, `face:+z` 0, `face:-z` 0, `at_proton` 0 (read, not measured); the escape line of the electron on `face:+y` at count 3407, its momentum then (-172 906 816, 35 392 088, 0) | DETECTOR |
| the clicks per detector, family `p` | `face:+x` and `face:-x` 328 045 each, `face:+y` and `face:-y` 325 073 each, `face:+z` and `face:-z` 322 101 each; 1 950 438 units escaped; the electron's own reads of the proton's rows 305 (its `read` lines, its own record) | DETECTOR |
| the releases read from the faces | 334 of 340 paired (+x with +y by the flight delays; 28 clicks left unpaired at the end, the last releases' rows near the face), the release counts 11 to 3402 (1 or 2 modulo 10: the click lands one to two counts after the release plus the table's f(L)) | DETECTOR |
| the electron's position per release (the arrival Nodes) | the distance from the proton's Node least 12.00, greatest 27.86 Links; the last release read at (29, 52) | DETECTOR |
| the axis crossings | +y at 412 at (26, 39), 13 Links; -x at 851 at (13, 26), 13 Links; -y at 1302 at (26, 9), 17 Links; +x at 2191 at (52, 26), 26 Links; then no crossing before the escape | DETECTOR |
| the returns to the +x axis | 1 (at 2191, 14 Links from the start); no count between two +x crossings; no second crossing of any axis | DETECTOR |
| the dwell about the crossings (first click to first click at the next Node along the motion) | 16 hops: 19, 21, 20, 19, 20, 20, 20, 20, 21, 20, 19, 21 about the +y, -x and -y crossings (12 hops, the mean 20.0) and 29, 40, 30, 30 about the +x crossing at 26 Links (4 hops, the mean 32.3); the mean over all 16, the pin's reading, 23.06 | DETECTOR |
| the phase per release | the increments 0 to 5 steps, unwrapped; the mean 1.174 steps per release over the run (the formula's 1.75 on the circle at r = 12; the loop widened and slowed) | DETECTOR |
| the circles per return j and the residue | not read: no return | DETECTOR (none) |
| the phase stamped at the +x crossing | 53 at 2191 (the start's 0 at count 11) | DETECTOR |
| the proton's reads of the electron's rows | 5 `read` lines at counts 30, 442, 882, 1329, 2254: one per crossing (1, 1, 1, 1 within 60 of each crossing plus the flight) and the start's | DETECTOR |
| the radius over the run (the step lines) | least 12.00, greatest 27.86, at the end 26.17 at (29, 52, 26); 1.23 turns of the angle; one closing of the angle at 2181; the momentum's length at the crossings 283, 308, 273, 182 million label units (the start's 294); the loop does not stay | GAMEBOARD (a diagnostic) |
| the per-axis action over the crossed Links to the closing at 2181 | x 159.66, y 150.47, z 0 quotients of h, the sum 310.1 = 4.85 circles; the body's phase at the closing 53 (a closing of the angle at a radius that grew from 12 to 26 is not a return, so this is not a closure reading) | GAMEBOARD (a diagnostic) |
| the dwell from the step lines at the same hops | 24 gaps, the mean 22.46, the least 18, the greatest 31 | GAMEBOARD (a diagnostic; agrees with the faces' 23.06 within the release grain) |

**The verdicts against the pins of section 3 (no pin moved).**

| Pin | Declared | Read | Verdict |
| --- | --- | --- | --- |
| P1 the dwell per Node | 19.05 to 20.5 counts, the mean over the hops read within 17 to 22.5 | 23.06 over 16 hops (20.0 over the 12 hops inside r = 17, 32.3 over the 4 at r = 26) | FAIL as declared (the mean over all the hops read); the hops at the three crossings the formula's radius covers read 20.0, inside, stated as a reading and not as the pin |
| P2 the period and the returns | T = 1552 within 15 percent, 4 or 5 returns | 1 crossing of the +x axis at 2191, no period | FAIL |
| P2b the return within 3 Links of the start | 3 Links | 14 Links | FAIL |
| P3 the closure j = 4.00 within 0.05 | 4.00 | not read (no return) | NOT READ (no return; the pin unmet) |
| P3b the residue per return within 3 steps | 0.06 steps | not read | NOT READ (no return; the pin unmet) |
| P5 the proton's reads per crossing 0 to 2 | 0.63 in the mean | 1, 1, 1, 1 | PASS |
| P6 750 clicks of `e` per side face | 750 less the rows in flight | 342, 337, 342, 339 (340 releases before the escape at 3407) | FAIL |

What the run adds to the algebra (ALGEBRA.md section 7's one integer):
under the declared integers on the drive on `main`, the loop from r = 12
with the declared momentum does not close on the lattice; it widens by one
Link at the first quarter turn and by thirteen by the fourth, and the
register's precedent at this radius (series H's `r12` under the signed
drive: an escape through `face:+x` at 2059 without a closing, with the
circle's momentum and the registered h) is repeated with the atoms world's
momentum and h_B (the escape through `face:+y` at 3407, one closing of the
angle at 2181). The cause is not read here and not claimed: the fan's
grain and the whole kicks are what the register names (atoms/PINS.md
section 2, items 3 and 4), the 1.9 percent excess of the declared momentum
over the circle's is a perturbation the limit's loop absorbs at a = 12.48
and cannot widen to 26. This is the baseline the stability rule's design
reads against: what a detector reads of the atom as the law stands is a
widening loop and an escape, one row per crossing at the proton, and a
dwell of 20 counts per Link where the loop is still near r = 12.

## Links

[The atom's algebra](https://github.com/Closer24/Universe24/blob/643b7ae7d4aeac2062518146aeb6e8b6f2998148/docs/designs/atom_algebra/ALGEBRA.md) (sections 1, 2, 3, 6 and
7); [the atoms pins](../atoms/PINS.md); the atoms README (`examples/events/atoms/README.md`, deleted 2026-09-26);
[series H](../../EXPERIMENTS.md#h-bohrs-lines-behind-the-detector-2026-09-20);
[ENGINE.md, the readings by type](../../ENGINE.md#the-detectors-readings-by-type);
[NATURE row 6](../../NATURE.md); [HIGHLIGHTS 5.4](../../HIGHLIGHTS.md#54-the-detector)
(records 281, 721, 754, 762, 817, 881, 884, 886); [the day's log](../../LOG_2026-09-20.md).

> The scripts of this folder (`baseline_readings.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/atom_baseline/<script>`).

> The scripts of this folder (`baseline_readings.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/atom_baseline/<script>`).
