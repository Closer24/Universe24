# The ring worlds of flow-link-v1: one arrival counts one Euclidean Link of its line (2026-09-22)

The worlds of the one run the model owner ordered (2026-09-22, record 915
of [the log](../../../docs/LOG_2026-09-20.md): admit `flow-link-v1` to the
ring world and run it once), written by `make_worlds.py` with their
expectations BEFORE any run (`expectations.json`, the pins by kind from the
design's map). The design is
[docs/designs/flow_weight/DESIGN.md](../../../docs/designs/flow_weight/DESIGN.md)
section 4 with [ALGEBRA.md](../../../docs/designs/flow_weight/ALGEBRA.md)
section 4 (merged in PR #839 at b463ac24; the physics-rule reviewer's
ADMISSIBLE of record 902); the construction is
[STEP_ALGEBRA.md](../../../docs/designs/light_bending/STEP_ALGEBRA.md)
section 9's; the hypothesis row is
[HYPOTHESES.md 29](../../../docs/HYPOTHESES.md#29-flow-link-v1-one-arrival-counts-one-euclidean-link-of-its-line-not-one-node-the-laws-two-constants-of-gravity-are-one-stated-so-that-it-can-fail).
A research run, made once, never a test; every expectation below was
written before the run; a reading outside its expectation is reported with
its numbers, never moved. Every number is one of the kinds of
[the register](../../../docs/EXPERIMENTS.md) ("Two kinds of readings"):
DETECTOR (the screen's clicks: the arrival Node and the age of each start's
rows), a CONVERSION of a DETECTOR reading labelled so (`C_nodes`, and
`C_ring` through the lever-arm factor the algebra stated before the run),
GAMEBOARD (the step algebra's momentum, not read by a run) or HOST (the
run's cost). Einstein's 4 appears on the comparison side only (record 817);
nothing here is pinned as nature's. The readings tool is
`tools/flow_link_readings.py`, every line labelled by its kind.

## What was built (the engine, under the world key alone)

The world key `flow_link` (`true`; absent or `false` by default; any other
type refused at load), the identity `flow-link-v1` under the record's
`hypotheses` and `flow_link: true` in `run.json` under the key alone
([ENGINE.md](../../../docs/ENGINE.md), the world file's keys;
`tests/test_flow_link.py`). Under it every direction of the world's table
carries, beside the unit label **u**_D (the integer vector nearest
`|p_D| D / |D|`, the label per Node), the flow label **f**_D, the integer
vector nearest `|p_D| D / S_1` (per component `sign(D_i) x (2 |p_D| |D_i| +
S_1) // (2 S_1)`, one Euclidean division at load, no root, no float, no
run-time division; `|p_D|` is Q = 64 for the photon and a massive family's
`momentum_magnitude`, each family's flow labels from its own labels), and
every flow sum reads it in place of the label: the rows' push by the
interval's arrivals (`nature_beam.CrowdMoments`, `optical_turn`) and a
body's push through the group moment of a free family's rays. The age
moment (the wall, the clock), the flight, the collision, the phase and the
momentum a click moves (a paid family's push, Q per unit) are untouched.
With the key absent the flow labels ARE the labels and every world reads
as it did, byte for byte (`tests/test_flow_link.py` (a): the gate world
`coupling/1b_m16` to its digests, the optical bar to main ab96e7e8's).

## The worlds

Series K's box (57 x 41 x 41, open; the one copy of the fan, the screen
and the box in [lensing/make_worlds.py](../lensing/make_worlds.py)) with
the mass of the free phase-less family `m` at the centre (28, 20, 20),
content 2^16, releasing on the fan of 290 primitive directions within
Manhattan 6 (16 units per direction per interval, q = 4640), the pair
`suspension` [1, 16384] with `width` 16384 declared (the pin n S = d,
[the Einstein derivation](../../../docs/designs/einstein_outside/DERIVATION.md)
II.10a), and in place of series K's one lamp a RING of lamps of the paid
family `light` on the plane x = 2: one at every Node (y, z) with
`|sqrt(y^2 + z^2) - b| <= 1 / 2` about the mass's line, each releasing one
unit per interval on the heading (1, 0, 0) alone; the screen x = 54 of
1681 one-Node `wave` detectors reading `age`; 400 intervals. The keys
`optical: gamma` (0 and 1) and `flow_link: true`. Every ring has its
control (no mass, the same lamps and keys) so that every start's arrival
Node and age are read against its own.

| World | b | starts | gamma | the mass |
| --- | --- | --- | --- | --- |
| `ring_b6_g0`, `ring_b6_g1` | 6 | 40 | 0, 1 | 2^16 |
| `ring_b6_control_g0`, `ring_b6_control_g1` | 6 | 40 | 0, 1 | none |
| `ring_b3_g0`, `ring_b3_g1` and their controls | 3 | 16 | 0, 1 | 2^16 / none |
| `ring_b8_g0`, `ring_b8_g1` and their controls | 8 | 48 | 0, 1 | 2^16 / none |
| `calibration_mass_g0`, `calibration_mass_g1` | 6 | series K's beam of five lines | 0, 1 | 2^16 |

The calibration copies are the registered `optical/mass_g0.json` and
`mass_g1.json` with `flow_link: true` added and nothing else changed (the
registered files are never edited); they are read by
`tools/lensing_readings.py` against the registered controls
`optical/control_g0.json` and `control_g1.json` run as they are.

## The expectations, pinned before the run (`expectations.json`)

From the design's map (`flow_weight_map.out` section 4, form `flow`: the
Bending Algebraist's integer walk of every start under the flow label; the
step algebra's simulation of the board, GAMEBOARD until the run reads the
Nodes). The per-start arrival Nodes (dy, dz) are in `expectations.json`
under `arrival_nodes`; the tolerance of the ring's mean is one Node per
start over the ring's count.

| World | the mean radial shift of the arrival Node, Links (DETECTOR) | as built | the mean delay, intervals (within 1) | starts moved by 0 / 1 / 2 / 3 Nodes | `C_nodes` (CONVERSION) | the lever-arm factor | `C_ring` (CONVERSION through the factor) against the expected `2 c_f x 0.990 x L / sqrt(L^2 + b^2)`, the grain |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ring_b6_g1` | `0.731 +- 0.025` (the deciding pin) | 0.974 | 0.78 | 15 / 20 / 2 / 3 | 2.50 | 0.68 | 3.65 against 3.86, the grain 0.085 |
| `ring_b6_g0` | `0.128 +- 0.025` (6 +- 1 of 40 starts move one Node) | 0.451 | 0.40 | 34 / 6 / 0 / 0 | 0.44 | 0.24 | 1.81 against 1.93, 0.085 |
| `ring_b3_g1` | `1.625 +- 0.0625` | 2.091 | 1.31 | 1 / 4 / 8 / 1 | 2.77 | 0.73 | 3.82 against 3.93, 0.107 |
| `ring_b3_g0` | `0.845 +- 0.0625` | 0.996 | 0.62 | 3 / 11 / 2 / 0 | 1.44 | 0.76 | 1.90 against 1.97, 0.107 |
| `ring_b8_g1` | `0.628 +- 0.021` | 0.854 | 0.98 | 22 / 21 / 2 / 3 | 2.86 | 0.73 | 3.92 against 3.79, 0.095 |
| `ring_b8_g0` | `0.107 +- 0.021` | 0.409 | 0.27 | 42 / 6 / 0 / 0 | 0.49 | 0.25 | 1.93 against 1.89, 0.095 |
| every ring | the tangential mean 0 within a Node | | | | | | |
| `calibration_mass_g0` / `_g1` | the centroid shift -1.600 / -3.000 pixels +- 0.5 (the register's -1.993 / -3.989 as built) | | the delay within the register's bracket of 1 | | | | |

`C_nodes = (the mean radial shift / 26) x b x 4 pi S / (3 q)`, `4 pi S /
(3 q) = 14.79` at this M and pin, the Nodes' own conversion (record 872
(e)); it carries the lever arm's factor `C_nodes / C_ring` the algebra
states before the run (the bend is spread from x = -26 to +26 and the part
made after the mass reaches the screen with less than 26 Links of arm), so
`C_ring` is read from the Nodes through that stated factor. The expected
`C_ring` is the declared `2 c_f` (c_f = 2, an input, record 826 (D)) times
the shells' factor 0.990 (the crowd's shell mean of the weighted flow
against the continuum's, ALGEBRA.md section 2) times the finite path's
`L / sqrt(L^2 + b^2)` at L = 26 (0.974 / 0.993 / 0.956 at b = 6 / 3 / 8);
the gamma 0 rows are `c_f` in place of `2 c_f`. The gamma 0 readings are
at the grain at M = 2^16 (six of forty starts move one Node): they pin the
count of moved starts, not a ratio.

**What refutes the hypothesis (DESIGN.md section 4):** a `C_ring` that,
after the two stated factors and through the stated lever-arm factor,
leaves `2 c_f` by more than the grain in either direction; any clock
reading that moves under the key (the controls' ages, the calibration's
delay outside the register's bracket); a world without the key that
differs from main's by a byte. A mean radial shift of 0.974 at b = 6,
gamma 1, would say the key is not in the run (the law as built).

**The verdict a run gives, by the pins:** CLOSES if every ring's `C_ring`
reads `2 c_f` bare within the grain; CLOSES WITHIN THE STATED FACTORS if it
reads the expected `2 c_f x 0.990 x L / sqrt(L^2 + b^2)` within the grain
through the lever-arm factor and the deciding pin `0.731 +- 0.025` is
inside; DOES NOT CLOSE otherwise.

## The host's cost estimate, before the run (HOST)

STEP_ALGEBRA.md section 11 and DESIGN.md section 5: the ring world is
series K's box with 40 lamps (b = 6) for 400 intervals, about the mass
world's cost times the lamps' rows. The registered mass world (one lamp of
five lines, 5 rows per interval) took 110 s at 1000 intervals on the
owner's machine (`optical/README.md`) and 11 s at 300 intervals on the
body worlds' host; on this host (4 cores, 15 GB) the first 40 intervals of
`optical/mass_g1.json` took 2.0 s. The crowd is the cost: 290 rows per
interval in flight for about 120 intervals (about 35 000 rows steady) against
the ring's 40 rows per interval for 90 intervals (3 600 rows, a tenth
more than the crowd; the beam's 450). Estimate per ring world with the
mass: 1.1 x the mass world's 400 intervals, about 60 to 120 s; a control
(no crowd) a few seconds; the 14 worlds at `--jobs 4` about 5 to 8 minutes
of wall clock, the peak memory below 1 GB per world. Measured after the
run below.

## The one run (2026-09-22): what was measured, and what the register refused

`tools/run_series.py --jobs 4`, 400 intervals, on the head of this branch
(Python 3.14.0rc2, numpy 2.5.3, headless; this host: 4 cores, 15 GB). Read
by `tools/flow_link_readings.py` (the window from interval 200, rows born
after the crowd filled the box) and, for the calibration,
`tools/lensing_readings.py --no-replay` against the registered controls
(the window [110, 400]); the run blocks (the source sha256, the digests of
the record, the readings, the verdicts) are in `expectations.json` under
`runs`, `calibration_runs` and `host_cost_measured`; no pin moved.

**The order's scope (the Boss, 2026-09-22, about 10:32Z, on the owner's
word of record 920: the algebra is done, the one run is the measurement).**
The run is b = 6, both gammas; b = 3 and 8 are declared, with the
algebra's numbers beside, and run only if b = 6 leaves the verdict
undecided at the grain. b = 6 at gamma 1 was refused by the register
(below), so the verdict at b = 6 is undecided and b = 3 and 8 were run
under that clause (the word reached this session after the runs); they
were refused alike, and their algebra stands: `C_ring` 3.82 / 3.92 against
3.93 / 3.79 at gamma 1, the mean radial shift 1.625 / 0.628 Links
(GAMEBOARD, the map's). The calibration ran at 41 s per world.

**The register's refusal (HOST).** Five of the six rings with the mass
were stopped by the engine's working bound, not by the key: `momentum_pair`
forms the pair (S_1, T) of a pushed row's whole momentum **P** = Q d
content **u**_D + **W** over the gcd of its components and refuses the
wall's square 3 |**P** / g|^2 Q^2 before the root when it leaves 2^63 - 1
(`|P / g| <= 27 397 079`). At d = 16384 the ring's rows (series K's lamp,
content 8) carry |**P**| = 2^29 on the heading, and a start off the mass's
plane is pushed in y and z at once, so the gcd of **W**'s components falls
to 16 or 2 and the primitive **P** / g is 3.3 x 10^7, over the bound; the
registered beam lies in the plane (**W**_z = 0), where the gcd stayed at
128 or more for 400 intervals. The same worlds WITHOUT the key are refused
alike (a probe of `ring_b6_g1` without `flow_link`: refused at interval
68; with the key at 80), and rows of content 1 (a lamp of turn 1) are
refused alike (the same row at interval 80, g = 2): the refusal is the ring
world's at this pin on the engine as built, a finding of the register, not
of the hypothesis. The step algebra walks integers without the bound.

| World | status (HOST) | the refusal, the primitive **P** / g at the stop |
| --- | --- | --- |
| `ring_b6_g0` | completed, 400 intervals, 64.4 s, 157 MB | |
| `ring_b6_g1` | refused at interval 79 | **P** / g = (32901461, 1149200, -1147979) |
| `ring_b3_g0` | refused at 79 | (33507403, 409525, -1064800) |
| `ring_b3_g1` | refused at 77 | (33523131, 804995, 2102152) |
| `ring_b8_g0` | refused at 135 | (33568237, 390720, -390115) |
| `ring_b8_g1` | refused at 89 | (66131823, 1205776, -1203345) |
| the six controls | completed, 400 intervals, 23 to 34 s | |
| `calibration_mass_g0`, `_g1` | completed, 400 intervals, 41 s each | |

**The ring at b = 6, gamma 0 (DETECTOR): every pin inside, the arrival
Nodes the map's, all forty.** The 40 starts' arrival Nodes agree with the
design's map start by start (40 of 40; the starts moved by 0 / 1 / 2 / 3
Nodes 34 / 6 / 0 / 0, the map's 34 / 6 / 0 / 0): `(-6, 0)` and `(6, 0)` by
one Node in y, `(0, 6)`, `(-4, 4)`, `(4, 4)`, `(4, -4)` by one Node, the
other 34 unmoved; every start's clicks land on one pixel (201 clicks per
start in the window, 185 on the four moved starts of the axes).

| Reading | Kind | Measured | The pin | Verdict |
| --- | --- | --- | --- | --- |
| the ring's mean radial shift of the arrival Node | DETECTOR | 0.128 Links (the radial shifts' sd 0.314) | 0.128 +- 0.025 (0.451 as built) | inside; the key is in the run |
| the ring's mean tangential shift | DETECTOR | 0.018 Links | 0 +- 0.025 | inside |
| the ring's mean delay | DETECTOR | 0.40 intervals | 0.40 +- 1 | inside |
| `C_nodes` | CONVERSION | 0.437 | 0.437 +- 0.085 | inside |
| `C_ring` through the lever-arm factor 0.242 | CONVERSION | 1.806 | the expected `c_f x 0.990 x L / sqrt(L^2 + b^2)` = 1.929 +- 0.085 | OUTSIDE by 0.038: 1.45 grains below, the algebra's own 1.46 |
| `C_ring` bare against 2 (gamma 0's `c_f`) | CONVERSION | 1.806 | 2 on the comparison side only | 9.7 per cent below, as the algebra |
| the controls' mean age | DETECTOR | 89.00 intervals at every ring and gamma, every start at its own (y, z) | the clock's word unchanged | inside |

**The calibration (DETECTOR, `tools/lensing_readings.py` against the
registered controls run as they are).** The registered `optical/mass_g0`
and `mass_g1` under the key read the centroid shift -1.573 / -3.180 pixels
(the design's -1.600 / -3.000 +- 0.5: inside; the register's -1.993 /
-3.989 as built), the delays 2.65 / 4.92 intervals (the register's 2.95 /
4.94, within the bracket of 1; the algebra's 2.60 / 5.00), the ratio 3.180
/ 1.573 = 2.02 (the algebra's 1.88 on the pixels, 2.17 on the momentum;
2.00 registered as built), 1344 / 1392 clicks in the window (1347 / 1395
registered), the centroid in z 20.000, no light taken by the mass. The
key moves the push and nothing else: the controls' digests are one number
at gamma 0 and 1 (no crowd), and the calibration's delays sit where the
register's do.

**The verdict, by the pins as written before the run.** At b = 6, gamma 0:
**CLOSES WITHIN THE STATED FACTORS**: the mean radial shift, the tangential
mean, the delay and `C_nodes` are inside their pins, the arrival Nodes are
the map's start by start, and `C_ring` through the stated lever-arm factor
sits 1.45 grains below `c_f x 0.990 x L / sqrt(L^2 + b^2)` (the design's
verdict sentence "to one to three grains"; the algebra itself sits 1.46
grains below there), outside the strict one-grain pin of `expectations.json`
by 0.038: the run reads what the algebra says, at the gamma 0 grain (six of
forty starts move one Node). Not CLOSES: 1.806 against 2 bare. The
deciding pin of the design, the gamma 1 ring's `0.731 +- 0.025` at b = 6,
is **NOT READ**: the world is refused by the register at interval 79, as
are b = 3 and b = 8 at both gammas. What decides it is the model owner's
and the architect's, not this run's: either the pair's bound on a pushed
row's momentum (an engine rule: the primitive **P** / g at d = 16384 with
content 8) or the ring's pin (a smaller d with S = d kept, the design's map
re-run at that pair for new pins before any run); neither is changed here.

What the run establishes: on the engine as built the key is in the run (the
b = 6, gamma 0 ring reads 0.128 against 0.451 as built, every arrival Node
where the algebra's walk under **f**_D puts it) and the calibration's shifts
move from the register's to the algebra's; the clock's word does not move.
It establishes no physical law: `c_f = 2` is an input, and the ring's
`2 c_f` at gamma 1 on the one constant stays unread until the refusal is
resolved.
