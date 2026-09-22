# The algebraic check of flow-link-v1: the step algebra of light beside a mass, the ring of starts and Newton's rows under the weighted flow (the Flow Weight Designer, 2026-09-22)

The owner's word (record 888, translated, as the Boss relayed it):
"(c): try to solve it algebraically too. It is an important law." This
file is the algebra of [DESIGN.md](DESIGN.md)'s rule in the manner of the
Bending Algebraist's [STEP_ALGEBRA.md](../light_bending/STEP_ALGEBRA.md)
(record 839: an algebra of steps can simulate a board): the law's integer
steps applied exactly, under the rule, to one row of light on each line,
read at a screen of Nodes. The arithmetic is
[flow_weight_map.py](flow_weight_map.py) beside this file, its output
[flow_weight_map.out](flow_weight_map.out); the map IMPORTS the
Algebraist's [step_algebra_map.py](../light_bending/step_algebra_map.py)
(one canonical copy) and reuses its `walk` (the three rules of the key
`optical` interval by interval, integer for integer as `nature_beam.py`
computes them), its `Table`, `Crowd`, `primitive_fan`, `unit_label`,
`bresenham_line`, `in_box`, `ring_starts` and constants; what it adds is
the flow label `f_D` and a crowd whose flow is summed on it
(`WeightedCrowd`), so the Algebraist's walk reads the rule's flow
unchanged, and beside it the exact form (`ExactTable`, the labels and the
flow in units of `1 / L`). No engine was imported or run, no pin moved,
no code changed. Base commit `ea3609a887650a2a303d540443944f7f23d55c54`,
main merged forward at `67cee093` (PR #821 in).

Every number is GAMEBOARD, **the step algebra's simulation of the board,
not a run**, never a measurement of nature; a number the register holds
from the engine's clicks is DETECTOR. Einstein's 4 appears on the
comparison side only, never as an input (record 817); `c_f = 2` is an
input (record 826 (D)), the pin `n S = d` a declaration (II.10a), the
weight a declaration under its own identity (DESIGN.md section 1).

## 0. The verdict, at the top

**CLOSES TO `2 c_f` within the finite path's factor and the shells'
`0.990`, to one to three grains, on the one constant.** Under
the rule (the flow label `f_D`, the integer vector nearest `Q D / S_1`,
per arriving row in place of `u_D`; the photon's magnitude `Q`, a massive
family's its own `|p_D|` in `Q`'s place, record 902; every crowd walked
here is the photon family at `Q = 64`) the push's constant of gravity is the
clock's: the same crowd's shell mean of the weighted flow is `22.85`
against the continuum's `q / (4 pi) = 23.08` (`0.990 +- 0.018`, the
shells' error of the mean) beside the clock's `A r = 68.72` against
`69.23` (`0.993 +- 0.020`), the law as built `32.79` (`1.421`). The ring
of starts on that one constant reads `C_ring = 3.65 / 3.82 / 3.92` at
b = 6 / 3 / 8 at gamma 1 against 4 (`1.81 / 1.90 / 1.93` against 2 at
gamma 0; the ratio `2.02`, the declared `c_f` read back), the residual
below `2 c_f` the finite path's `L / sqrt(L^2 + b^2)` (0.974 at b = 6)
and the shells' `0.990`, one to three grains of the ring (`0.085 to
0.107`). Not CLOSES: the ring does not read 4 within the grain without
the two stated factors, and the number is `2 c_f` with `c_f` an input,
not a derivation of 4. Not CANNOT CLOSE: the ground of the comparison is
one, and the reading sits where the algebra puts it. The calibration
(section 1): the control unchanged (`89.40`), the mass world's shifts
`-2.000 / -4.000` (the register's `-1.993 / -3.989`, DETECTOR) become
`-1.600 / -3.000` under the rule, the delays within the bracket; the
in-plane coefficient at b = 6 `14.71` becomes `11.69`, still the plane's
comb (record 862), not a constant. Newton's rows (section 5): the fall's
`g` and the push per interval divided by the plane fan's `F_plane =
1.2871`, D3's periods `343 / 687` to `384 / 768` by the balance, `T(24) /
T(12) = 2.00` unchanged.

## 1. The calibration first (a): what the weighted flow does to the registered clicks

**By formula.** The control world has no crowd: the rule reads nothing,
and the control's clicks are byte for byte the register's. On a mass
world the push per interval of dwell at a Node is `n x weight x V`, and
the rule changes `V` alone: each arriving row of direction `D` enters
with `f_D` (magnitude `Q |D| / S_1` within the rounding) in place of
`u_D` (magnitude `Q`). The wall reads the age moment, untouched, so the
row's pace and its delay are the flight's under the same stretch; the
click's age moves only through the bent path's Links, second order in
the angle. So: the control unchanged; every shift smaller by the
in-plane lines' own `|D| / S_1` weighted along the row's path (a
per-line factor between `1 / sqrt 3` and 1, not the shell mean's `1 /
1.42`: the beam in the plane sums the 48 in-plane lines, each once); the
delay within its bracket.

**By the map** (`flow_weight_map.out` section 3; the Algebraist's walk
reused, the crowd's flow on `f_D`):

| World | gamma | shifts per line, pixels: as built (the Algebraist's, calibrated to the register) | under the rule | the mean: as built / under the rule / registered (DETECTOR) | delays: as built / under the rule / registered |
| --- | --- | --- | --- | --- | --- |
| the control | 0 | ages 89, 90, 90, 89, 89 | the same | `89.40 / 89.40 / 89.40` | |
| `mass` (b = 6) | 0 | -2, -2, -2, -2, -2 | -1, -1, -2, -2, -2 | `-2.000 / -1.600 / -1.993` | `3.00 / 2.60 / 2.95` |
| `mass` (b = 6) | 1 | -4, -4, -4, -4, -4 | -3, -3, -3, -3, -3 | `-4.000 / -3.000 / -3.989` | `5.00 / 5.00 / 4.94` |
| `far` (b = 8) | 0 | -2, -1, -2, -2, -2 | -1, -1, -2, -1, -1 | `-1.800 / -1.200 / -1.773` | `2.40 / 2.40 / 2.56` |
| `far` (b = 8) | 1 | -4, -3, -4, -3, -3 | -3, -2, -3, -2, -3 | `-3.400 / -2.600 / -3.403` | `4.40 / 5.00 / 4.33` |
| `near` (b = 3) | 0 | -2, -2, -3, -1, -5 | -2, -2, -3, -1, -4 | `-2.600 / -2.400 / -2.608` | `2.80 / 3.20 / 2.99` |
| `near` (b = 3) | 1 | -6, -5, -6, -3, -12 | -4, -4, -5, -2, -9 | `-6.400 / -4.800 / -6.412` | `6.00 / 5.00 / 6.20` |

The exact form (the labels and the flow in units of `1 / L`, `L = 3900`)
lands the same Nodes on every line but one (`near`, gamma 1, the heading:
`-3` for `-4`) and the same delays within one interval. The ratio gamma
1 / gamma 0 of the shifts under the rule is `1.88 / 2.17 / 2.00` at
b = 6 / 8 / 3 on the pixels and `2.17 / 2.06 / 1.99` on the momentum
(`2.114 / 2.077 / 2.112` as built): the declared `c_f` read back with the
dwell's `1 + c_f k`, RECOVERED, not derived. What the rule does to the
registered clicks, then: the control nothing; the mass world's shift
`-1.993 / -3.989` (DETECTOR) would read about `-1.6 / -3.0` under the key
(the algebra's `-1.600 / -3.000`, the grain 0.2 pixel on the five-line
mean); the delays stay within the register's bracket of one interval
(the largest move `0.6` at b = 8, gamma 1, and `-1.0` at b = 3, gamma 1,
the near world's one line landing 9 Nodes off instead of 12).

## 2. The shell mean (b): the L1 factor cancels, the residual with its grain

From the same stationary crowd (M = `2^16`, `q = 4640`), the shell means
over r = 4 .. 14 (`flow_weight_map.out` section 2), the grain the
standard error of the mean over the eleven shells:

| Reading | the mean | the continuum | the factor | the shells' spread (sd) | the mean's error |
| --- | --- | --- | --- | --- | --- |
| `|V| r^2 / Q` on `u_D`, the law as built | `32.79` | `23.08` | `1.421` | `2.08` | `0.63` (`0.027`) |
| `|V_f| r^2 / Q` on `f_D`, the rule | `22.85` | `23.08` | `0.990` | `1.40` | `0.42` (`0.018`) |
| `|V_L| r^2 / (Q L)`, the exact form | `22.84` | `23.08` | `0.990` | `1.39` | `0.42` (`0.018`) |
| `A r`, the clock's word (unchanged) | `68.72` | `69.23` | `0.993` | `4.54` | `1.37` (`0.020`) |

The cancellation shown: on the fan the mean of `(S_1 / |D|) x (|D| / S_1)`
is `1.0000` by identity and `1.0003` with the rounded `f_D` (the largest
per-line rounding `1.56` per cent, the mean `0.45`), where the mean of
`S_1 / |D|` alone is `1.4355` (section 1 of the .out). On the lattice the
push's factor `0.990 +- 0.018` and the clock's `0.993 +- 0.020` are one
within the grain; the residual `0.010` of both is the shells' count of
Nodes (DERIVATIONS_BEAM 3.2's Gauss ripple; `21.8` to `24.7` shell by
shell under the rule, `61.1` to `77.4` on the clock's word), not the
rule's. The push's constant is the clock's, `q / (4 pi S)` at the pin.

## 3. The ring of starts (c): the coefficient on the one constant

Section 9's construction unchanged (the same fan and M, one row on the
heading from every Node of the lamp's plane at `|sqrt(y^2 + z^2) - b| <=
1 / 2`, the whole screen read), every start walked by the Algebraist's
`walk` with the crowd's flow on `f_D` (`flow_weight_map.out` section 4):

| b | starts | gamma | `C_ring` as built (the Algebraist's) | `C_ring` under the rule, on the one constant | the exact form | the expected `2 c_f x 0.990 x L / sqrt(L^2 + b^2)` | the residual, in grains (`0.107 / 0.085 / 0.095`) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 16 | 0 | 2.605 | **1.901** | 1.891 | 1.966 | 0.6 |
| 3 | 16 | 1 | 5.442 | **3.821** | 3.822 | 3.932 | 1.0 |
| 6 | 40 | 0 | 2.599 | **1.805** | 1.795 | 1.929 | 1.5 |
| 6 | 40 | 1 | 5.116 | **3.652** | 3.644 | 3.857 | 2.4 |
| 8 | 48 | 0 | 2.905 | **1.932** | 1.929 | 1.893 | 0.4 |
| 8 | 48 | 1 | 5.859 | **3.918** | 3.914 | 3.786 | 1.4 |

The tangential mean is `0.00000` at every ring; the ratio gamma 1 /
gamma 0 `2.01 / 2.02 / 2.03` at b = 3 / 6 / 8. The expected column is
the declared `2 c_f` times the two factors the algebra states: the
shells' `0.990` (section 2) and the finite path's `L / sqrt(L^2 + b^2)`
with `L = 26` (`0.993 / 0.974 / 0.956`: the continuum's transverse
impulse summed from x = -26 to +26 instead of over the whole line). The
dwell's `1 + c_f k` (`k = 0.02 to 0.05`) is upward and inside the same
grain. So the ring reads `2 c_f` on the one constant within one to three
grains at every b and both gammas: **`4 x 0.99 x (0.96 to 0.99)`, that is
3.8 to 3.9 expected against 3.65 to 3.92 read, at `c_f = 2`.**

**The in-plane coefficient at b = 6, for the record.** The heading's row
in the mass's plane reads `C = 11.69` at gamma 1 under the rule (`14.71`
as built), `5.38` at gamma 0 (`6.96`); at b = 3 and 8, `8.52` and `13.45`
(`11.27` and `16.95`): smaller by the in-plane lines' own weights, still
growing with b, the plane's comb of record 862 (the b-exponent 0 of the
two-dimensional fan) and no constant of the law. The ring takes the plane
out, as before; the rule takes the L1 factor out.

## 4. The pins of the ring world under the rule (d), before any run

The world: STEP_ALGEBRA.md section 9's (the registered box, fan of 290,
mass `2^16`, `suspension [1, 16384]`, `width 16384`, the ring of lamps on
the heading at every start listed in the .out, the screen of `wave`
pixels reading `age`), with the key `flow_link: true` beside `optical: 1`
and `optical: 0`. The pins, the step algebra's simulation of the board,
DETECTOR when run; the reading the screen's clicks (the arrival Node's
radial shift toward the mass's line, `-(dy y + dz z) / r` in Links, and
the click's age less the control's), the momentum's `tan alpha` GAMEBOARD
and not compared:

| b | starts | gamma | the ring's mean radial shift of the arrival Node, Links (as built) | tolerance | the starts moved by 0 / 1 / 2 / 3 Nodes | the mean delay, intervals (within 1) | `C` from the Nodes (the Nodes' own conversion) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 16 | 0 | `0.845` (0.996) | `+- 0.0625` | 3 / 11 / 2 / 0 | `0.62` | `1.44` |
| 3 | 16 | 1 | `1.625` (2.091) | `+- 0.0625` | 1 / 4 / 8 / 1 | `1.31` | `2.77` |
| 6 | 40 | 0 | `0.128` (0.451) | `+- 0.025` | 34 / 6 / 0 / 0 | `0.40` | `0.44` |
| 6 | 40 | 1 | `0.731` (0.974) | `+- 0.025` | 15 / 20 / 2 / 3 | `0.78` | `2.50` |
| 8 | 48 | 0 | `0.107` (0.409) | `+- 0.021` | 42 / 6 / 0 / 0 | `0.27` | `0.49` |
| 8 | 48 | 1 | `0.628` (0.854) | `+- 0.021` | 22 / 21 / 2 / 3 | `0.98` | `2.86` |

The tolerance is one Node per start over the ring's count (the
Algebraist's grain, section 9); the per-start arrival Nodes `(dy, dz)`
are listed in the .out's section 4 under `form flow` (at b = 6, gamma 1:
`(-6, 0)`, `(6, 0)` and `(0, 6)` by 3 Nodes, `(-4, 4)` and `(4, 4)` by one
on each axis, 20 starts by 1, 15 by 0); the tangential mean 0 within a
Node. **The comparison a run makes, on the Nodes' own conversion (record
872 (e)):** `C_nodes = (mean radial shift / 26) x b x 4 pi S / (3 q)`,
`4 pi S / (3 q) = 14.79` at this M and pin, reads `2.50` at b = 6, gamma
1, and carries the lever arm's factor the algebra states before the run,
`C_nodes / C_ring = 0.68` (`0.73 / 0.73` at b = 3 / 8; `0.65` as built),
because the bend is spread along the path and the part made after the
mass reaches the screen with less than 26 Links of arm; through that
stated factor the Nodes' reading is compared with `2 c_f` on the one
constant within the ring's grain and the finite path's factor. The
deciding pin is gamma 1's at b = 6, `0.731 +- 0.025` Links over 40
starts: `0.974` refutes the rule's presence in the run (the law as
built). The gamma 0 reading is at the grain at M = `2^16` (6 starts of 40
move one Node), so it pins the count of moved starts (`6 +- 1` of 40),
not a ratio.

## 5. Newton's rows, by formula (e continued)

The push a body reads is linear in the flow, so under the rule every
push is divided by its fan's mean of `S_1 / |D|`, and nothing of the
body enters (the equivalence exact as before, `push_m = m x push_1`).
On series D's plane (the 120 primitive in-plane directions within radius
8) `F_plane = 1.2871` (`4 / pi = 1.2732` in the isotropic limit;
`flow_weight_map.out` section 1). **The fall's `g`** (`g = v^2 / r`, the
second difference of the clicks' x in D3, `omega^2 = (2 pi / T)^2`): `g`
divided by `1.2871` at every radius, GAMEBOARD by formula. **The orbit's
periods** (D3, S = 32, the pinned n = 9, the circular balance `n^2 / (S +
n)` proportional to the push): the balance divided by `1.2871` solves to
`n = 7.818` (the nearest whole 8), so `T = 2 pi r (S + n) / n = 343 / 687`
becomes `384 / 768` (`377 / 754` at n = 8) at r = 12 / 24, to be
re-derived by the generator before any run. **The ratio** `T(24) / T(12)
= 2.00` is unchanged: the fan is the same at both radii and the weight
per line is a constant of the line, not of r, so the same factor divides
the push at r = 12 and r = 24 and cancels in the ratio (the arithmetic:
`768 / 384 = 2.000`, `754 / 377 = 2.000`, as `687 / 343 = 2.003`). Series
C's `flow x 2 pi r / q = 1.00` per Node on that fan becomes `0.78`. Every
clock reading unchanged (the age moment untouched).

## 6. The verdict (e)

**CLOSES TO `2 c_f` ON THE ONE CONSTANT within the finite path's factor
`L / sqrt(L^2 + b^2)` and the shells' `0.990`, to one to three grains:
`3.65 / 3.82 / 3.92` against the expected `3.86 / 3.93 / 3.79` at b = 6 /
3 / 8 at `c_f = 2` (bare against 4: 8.7, 4.5 and 2.0 per cent below); not CLOSES (4 is not read within the grain bare), not CANNOT
CLOSE (the ground is one).** What is declared: `c_f = 2` (the key),
`[1, 16384]` and the fan (the world), `n S = d` (the pin), `f_D` (the
hypothesis). What follows: the push's constant equal to the clock's
(`0.990` against `0.993`), the ring's `2 c_f` on it, the ratio gamma 1 /
gamma 0 of `2.02`, the delay the wall's alone, unchanged. Nothing is
derived: 4 is `2 x (1 + gamma)` with gamma an input of kind 2, read back
on one ground. What a run adds (the ring world under the key, on the
owner's go after the reviewer's gate): the clicks of section 4 against
their pins, the control byte identical, the delay within its bracket; a
mean radial shift of `0.974` at b = 6, gamma 1, would say the key is not
in the run, one outside `0.731 +- 0.025` by more than the lever arm's
stated factor would refute the algebra's walk of the rule.

## 7. Links

- [DESIGN.md](DESIGN.md): the rule, the three tests, what moves, the key.
- [flow_weight_map.py](flow_weight_map.py), [flow_weight_map.out](flow_weight_map.out): the arithmetic (the Algebraist's map imported).
- [STEP_ALGEBRA.md](../light_bending/STEP_ALGEBRA.md), [step_algebra_map.py](../light_bending/step_algebra_map.py): the step algebra reused, sections 5, 9 and 10.
- [examples/events/optical/README.md](../../../examples/events/optical/README.md): the registered worlds (DETECTOR).
- [docs/EXPERIMENTS.md](../../EXPERIMENTS.md), D3: Newton after a detector, the pins that would move.
- [the log](../../LOG_2026-09-20.md) records 817, 862, 872, 878, 880, 884, 888.
