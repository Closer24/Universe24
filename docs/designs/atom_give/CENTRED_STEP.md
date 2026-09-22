# centred-step-v1: the body's step fires when its accumulated motion reaches half the wall, under its own identity, off by default

The Atom Give Designer 2, 2026-09-22, on the model owner's word through
the Boss (record 953: the atom enters the paper only if it passes, and
speed; step 1 docs only, in parallel with the reviewer's read of PR
#867). The cause it answers is [CAUSE.md](CAUSE.md) section 2 (v) and
(iv): the count primitive fires a body's step when its accumulated
motion reaches a whole wall, so the body's Node lags its accumulated
motion by half a Link in the mean, the push read at the Node turns by
`1 / (2 r)` along the motion and pumps `pi F(r)` of the loop's constant
per turn; the kick map [cause_kicks.py](cause_kicks.py) holds the loop
at r = 12 under the step of this file. A design only: no engine line,
no world file, no run, no pin moved after this file. Every number below
is GAMEBOARD by formula from the map and the declared integers, or an
EXPECTED detector reading; nothing was run. Bohr's and Kepler's forms
appear only as the thing compared with (record 817).

**The verdict in one line.** One declaration of the drive, under the
world key `centred_step` (the identity `centred-step-v1`, absent by
default, every registered world byte identical without it): the count
of a body's step is the NEAREST whole number of its accumulator in
units of the wall, not the whole part, so a step fires when the
accumulated motion passes half a Link beyond the Node and the whole
wall is subtracted; the body's Node is then the nearest Node to its
accumulated motion and the lag is zero in the mean. Generic (one
threshold of one primitive, no family name), vector (one Euclidean
division, no root, no float), local (the body's own accumulator, as
today); a hypothesis under its own name until the owner makes it the
law. The pins for the registered `hydrogen_r12` under the key, from the
map before any run: the loop stays five turns on the board, the
crossings within 9 to 20 Links, three to four returns in 7500 intervals
with the period 1400 to 2000; an escape face click of the electron is
FAIL, a crossing outside the band is FAIL.

## 1. The one declaration, in the law's words

**Today** (BEAM_LAW note 41, record 108; `core.integer.by_drive`): a
body's accumulator on the axis a gains the signed momentum component
`p_a` at every self-creation; the count is the WHOLE PART the
accumulator then holds in units of the wall `Q S M + abs(p_a)` (`main`'s
per-axis drive, `step_divisor`; under `drive_b` the one wall of the line
drive, `by_line`), that much is subtracted, the remainder stays below
the wall, the count capped at one Link per self-creation (`at_most`).
So the accumulator runs in `[0, wall)` on an axis of one sign and the
Node is BEHIND the accumulated motion by the accumulator's fraction,
half a Link in the mean, at every reading of the push.

**Under `centred_step`** the count of the body's step is the NEAREST
whole number of the accumulator in units of the wall:

    count = (abs(drive) + wall // 2) // wall,   with the sign of drive,   capped at one Link per self-creation as today;
    the accumulator after: drive - count x wall,   in [-(wall - wall // 2), wall // 2),

that is, a step fires when the accumulated motion passes HALF the wall
beyond the Node (the first step after a birth after half a dwell, the
body born at its Node's centre), and the whole wall is subtracted, so
the accumulator runs in `[-wall / 2, wall / 2)` and the Node is the
nearest Node to the accumulated motion at every reading of the push.
On a momentum reversal the count reverses where the accumulated motion
crosses the half-Link line on the other side, as the signed count of
today does at the whole wall (a rate that reverses first cancels what it
had accumulated). Under `drive_b` the same threshold in `by_line`: an
accumulator is at or beyond the wall when `abs(drive) >= wall - wall //
2`, the furthest over it carries, the whole wall subtracted with the
sign, a coincident fire deferred as today.

**Where** (the engine's drive block, `events/engine.py` about lines
860 to 935): `main`'s branch `entry.counts.advance("drive", values=
entry.momentum, denominators=[step_divisor(...)])`, which calls
`by_drive` per axis, and form B's branch `by_line(entry.drive, rates,
wall)`; one parameter on each primitive (`centred: bool = False`, the
threshold `wall - wall // 2` in place of `wall`) passed from the world's
key by the engine at those two calls and nowhere else. NOTHING ELSE
MOVES: every other count of the law keeps the whole part (the owed
count, the release, the lamp, the turn by momentum, the push per
column, the clock: `by_drive` is called for them without the
parameter); the action rows gain `abs(p_a) N` at every Link the step
rule counts on the axis, as before (the Links per loop are the same,
their first fires half a dwell earlier); note 30 (ii)'s convention at a
Link counted but not crossed is unchanged; the lost coincident fires of
`main`'s per-axis drive are unchanged (the key does not lift them;
`drive_b` does); the push is read at the Node, as the law has it (the
key moves where the body IS, not where the push is read). With the key
absent the two calls pass `False` and every registered world replays
byte for byte (the gate set, `examples/events/gate_set.json`).

**The declaration** (kind 2 by the world key):

| The declaration | Where | What it says | Default |
| --- | --- | --- | --- |
| `centred_step: true` | the world | the identity `centred-step-v1`, listed under `hypotheses` in the record; the body's step count the nearest whole number of its accumulator in units of the wall, on both drives | absent: the whole part, as today |

## 2. The three tests (skills/workflow.md, record 202)

| The test | The rule's answer | Verdict |
| --- | --- | --- |
| Generic | one threshold of one primitive (`by_drive`, `by_line`), the same for every body of every family (the electron, a proton that moves, a planet, a cart); no family name, no kind, no branch on a name: a parameter of the count, a value of the world | PASS |
| Vector | verb 6, one Euclidean division on bounded integers: `(abs(drive) + wall // 2) // wall`, the remainder kept in the accumulator; `wall // 2` one more Euclidean division by the declared 2; no root, no float, no run-time division beyond these; the bound: `abs(drive) + wall // 2 < 2 wall`, checked where `bounded` checks the drive today | PASS |
| Local | the body's own accumulator on its own record (as today), nothing kept at a Node beyond the events there, no register, no remainder elsewhere, no draw; fixed work (one addition per axis per self-creation, as today) and fixed storage (none added) | PASS |

## 3. Why it works, and what refutes it (CAUSE.md section 2 (v), the map)

The lag's pump is `1 / (2 r)` of the push along the motion, `pi F(r)`
per turn (4.2 percent and `3.9 x 10^6` at r = 12, against 4.7 percent
and `3.5 x 10^6` read on the baseline over three quarters); the centred
step makes the mean lag zero, and the map (the Atom Algebraist's body
step under the shell mean of the push, the fan's grain absent) holds
the loop at r = 12: with the steady push alone for five turns at 12 to
13 Links (case O); with the pulse and `main`'s lost fires on top for
five turns within 10 to 19 Links (cases P and T); with the lattice's
flux `r^-1.83` within 13 to 16 (case U). What remains under the key, by
the map: the pulse's and the lost fires' wander of two to four Links
per quarter and a slow residual rise of the loop's constant (from -6.6
to -5.2 over five turns under the inverse square, -6.6 to -5.8 under
`r^-1.83`, against -7.5 to -4.0 in ONE turn on the baseline), the lost
fires' `v x p` of CAUSE.md section 2 (iv) 2, an order below the lag's
pump; `drive_b` lifts them, a separate key.

What refutes the rule: with the key on, the registered `hydrogen_r12`
leaving the board (an escape face click of the electron, DETECTOR) or a
crossing outside the band of section 4 within five turns; then the lag
is not the whole cause and the map's shell mean hides what the fan's
grain does (the register's comb, the crossed fraction 0.87 at r = 12,
PINS.md section 2). What refutes the identity's byte identity: any
registered world differing by a byte with the key absent (the gate
set's assertion, FAIL of the build).

## 4. The pins, declared before any run, for the registered `hydrogen_r12` with the key on (nothing else changed in the world)

The world: `examples/events/atoms/hydrogen_r12.json` as registered (the
baseline's world, RUN.md section 1: `main`'s drive, no `drive_b`, the
electron at (38, 26, 26) with **p** = (0, 293 783 192, 0), 7500 ticks)
plus `centred_step: true` and nothing else; the run's world file
`hydrogen_r12_centred.json` written by the build. The pins are the
map's cases T (the inverse square) and U (the lattice's flux `r^-1.83`),
the two force laws of the shell mean bracketing the fan's, with the
fan's grain (absent from the map) as the tolerance; the control is the
baseline run itself (the same world without the key: the escape through
`face:+y` at 3407, DETECTOR, RUN.md section 4).

| Pin | The map, case T (inverse square) | The map, case U (`r^-1.83`) | The pin and its tolerance | Kind | FAIL |
| --- | --- | --- | --- | --- | --- |
| C1 the loop stays | 18 quarter crossings in 7500, no escape | 15 quarter crossings, no escape | no escape face click of the electron (family `e`, `measured` 2) in 7500 ticks; at least 12 quarter crossings (three turns) | DETECTOR (the faces' click lines; the crossings from the arrival Nodes, RUN.md section 2) | an escape face click = FAIL; fewer than 12 crossings = FAIL |
| C2 the crossings' radii per quarter, five turns | 13, 13, 10, 10; 13, 13, 11, 10; 13, 14, 11, 10; 13, 17, 14, 11; 13, 19 | 13, 13, 13, 14; 14, 14, 13, 15; 15, 14, 14, 16; 16, 16, 15 | every crossing within 9 to 20 Links from the proton's Node (the map's 10 to 19 widened by one Link each side for the fan's grain); the first four within 10 to 15 | DETECTOR (the arrival Nodes at the axis crossings) | one crossing outside 9 to 20 = FAIL |
| C3 the returns to the +x axis and the period | 4 at 1412, 2842, 4384, 6201: the periods 1430, 1542, 1817 | 3 at 1648, 3440, 5404: 1792, 1964 | 3 to 4 returns in 7500; every period 1400 to 2000 (the circle's 1462 and the map's slowest 1964, the grain 5 percent each side) | DETECTOR (the `+x` crossings' counts, the faces' pairs) | a period outside 1400 to 2000 = FAIL |
| C4 the momentum's length at the crossings | 211 to 343 million | 254 to 288 million | 200 to 350 million label units at every crossing (the start's 294) | GAMEBOARD (the step lines; a diagnostic printed beside, not counted) | (not counted) |
| C5 the closure fraction at the returns | not given by the map (the phase's turn per loop is the action rows' sum over the crossed Links: a returning loop of radius 10 to 15 turns 3.4 to 5.0 circles) | | reported, not pinned: the sum of the electron's rows' phase increments over one return over N, read on the faces (ALGEBRA.md 2 (c) reading 1); the closed circle's `j = 4.001` is NOT expected of a wandering loop | DETECTOR | (not counted) |
| C6 the control | the baseline (no key): the escape at 3407 | | the same world without the key replays the baseline byte for byte (its `state.json` sha256 7664a712..., RUN.md section 4) | the build's test | a byte differing = FAIL of the build, not of the rule |

The reading of every pin is the runner's method of RUN.md section 2
(the faces' clicks paired into releases, the arrival Nodes, the
crossings; `baseline_readings.py` on the run folder, the pins C1 to C3
added to its verdict lines); the host's tick a labelled diagnostic; no
pin moved after the run. Bohr's whole number and Kepler's period appear
only afterwards on the comparison side: a loop that stays and wanders is
the pin here, not a closed circle.

## 5. What the build touches (step 2, after the reviewer's AGREED on PR #867), and the run (step 3)

| Where | What | Off by default |
| --- | --- | --- |
| `src/event_universe/core/integer.py` | `by_drive(..., centred: bool = False)`: the count `(abs(drive) + denominator // 2) // denominator` when centred, the whole part otherwise; `by_line(..., centred: bool = False)`: the threshold `wall - wall // 2` when centred | the default keeps every caller as today |
| `src/event_universe/events/measured.py` | the counts table's `advance` passing `centred` through for the `drive` rows | as today |
| `src/event_universe/events/world.py` | the world key `centred_step` (bool, false), the field, the parser, the known-keys list, `hypotheses` listing `centred-step-v1` | absent |
| `src/event_universe/events/engine.py` | the two calls of the drive block pass `self.world.centred_step` | `False` |
| `tests/test_centred_step.py` | (i) `by_drive` centred on declared integers: the first count after half the wall, the accumulator in `[-wall / 2, wall / 2)`, a reversal's count, the cap; the whole part unchanged without the flag; (ii) `by_line` the same; (iii) a body on a minimal GameBoard stepping half a dwell earlier under the key and at the same Links per loop; (iv) the parser's key and `hypotheses`; (v) the gate set byte identical with the key absent (`examples/events/gate_set.json`, the assertion of every key admitted since 2026-09-20) | |
| `examples/events/atoms/hydrogen_r12_centred.json`, the atoms README | the registered world plus the key; nothing else | the registered `hydrogen_r12.json` untouched |
| `docs/designs/atom_give/RUN_CENTRED.md`, `centred_readings.out` (step 3) | the one run, read by kind against section 4, `baseline_readings.py` reused with C1 to C3; no pin moved after the run | |

Host estimates: step 2 (the parameter on the two primitives, the key,
the two call sites, the test module, the gate set's assertion,
`check.py --base origin/main`) about one hour and a half; step 3 (one
run of 7500 ticks, about 70 s and a few hundred megabytes as the
baseline's, the reading by the runner's script, RUN_CENTRED.md) about
forty-five minutes. Dangerous: nothing with the key off (the byte
identity asserted); with it on, every body of the world steps half a
dwell earlier than today, the proton fixed, the rows untouched.

## 6. What it is not

- Not a change of the push: the push is read at the Node, from the
  rows' labels there, as the law has it; the key moves the body's Node
  to the nearest to its accumulated motion.
- Not a change of any other count: the whole part stays for the clock,
  the release, the lamp, the turn, the owed count and the push per
  column.
- Not the cure of the pulse's or the lost fires' wander (the map's
  residual, section 3); `drive_b` is the key that lifts the lost fires,
  and the two keys compose (the line drive's threshold at half the
  wall).
- Not the law: a hypothesis under its own identity, admitted per
  world, until the owner's word after the run of section 4 and the
  reviewer's read; then, if he makes it the law, every world's steps
  move and every registered pin is re-read, a separate order.
- Not the atom's stability rule: atom-give-momentum-v1
  ([DESIGN_MOMENTUM.md](DESIGN_MOMENTUM.md)) reads the closure of a loop
  that returns; the centred step is what lets a loop return on this
  lattice; the give's pins transfer to the centred step's world as
  declared there (section 6), the periods re-pinned from that world's
  own crossings (C3).

## Links

[CAUSE.md](CAUSE.md) sections 1, 2 (iv), 2 (v) and 3; [cause_kicks.py](cause_kicks.py)
and [its printout](cause_kicks.out) (cases O, P, R, T, U);
[DESIGN_MOMENTUM.md](DESIGN_MOMENTUM.md); [the baseline run](../atom_baseline/RUN.md)
and [its readings](../atom_baseline/baseline_readings.out); [PINS.md](../atoms/PINS.md)
section 2; [`core.integer.by_drive` and `by_line`](../../../src/event_universe/core/integer.py);
[BEAM_LAW notes 30 and 41](../../BEAM_LAW.md); [drive-b-v1](../drive_b/DESIGN.md)
(the key precedent, record 652); [the local integer operation contract](../../ARCHITECTURE.md#local-integer-operation-contract);
[LOCALITY-1](../../../SIMULATOR_DEFINITIONS.md); [the three tests](../../../skills/workflow.md);
records 108, 202, 652, 817, 935, 937, 952 and 953 of [the log](../../LOG_2026-09-20.md).
