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
