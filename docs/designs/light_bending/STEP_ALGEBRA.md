# The step algebra of light bending: the walk of a light row past a held mass, simulated by the law's integer steps, read at a screen of Nodes (the Bending Algebraist, 2026-09-22)

The canonical statement of this algebra is [docs/ALGEBRA.md](../../ALGEBRA.md), section 5.9; this file is kept as the record of 2026-09-22.

The owner's order (2026-09-22, translated, as the Boss relayed it at
about 07:47Z): "Try algebra, and if it does not work come back to me. An
algebra of steps can simulate a board. For these checks one scatters
detectors on Nodes." The question (records 822 and 826 of
[the log](../../LOG_2026-09-20.md)): does the law give nature's deflection
coefficient, `alpha b / (G M) = 4` (alpha the deflection angle, b the
impact distance, G Newton's constant, M the mass; Einstein's 4, Newton's
2, in units where c the pace of light is 1), and how it follows from the
Inside step, with Einstein's form on the comparison side only, never an
input (record 817).

Every number below is labelled. A number the algebra gives is GAMEBOARD
arithmetic of the declarations, called throughout **the step algebra's
simulation of the board, not a run**, never a measurement of nature; a
number the register holds from the engine's clicks is DETECTOR. The
arithmetic is in [step_algebra_map.py](step_algebra_map.py) beside this
file, its output in [step_algebra_map.out](step_algebra_map.out); no
engine was imported or run, no pin moved, no code changed.

## 0. The verdict, at the top

**CANNOT CLOSE on the registered geometry.** The step algebra reproduces
the registered runs of the key `optical` exactly to the grain (section 5:
the mass world's `-2.000 / -4.000` pixels against the register's
`-1.993 / -3.989`, DETECTOR), so the simulation is trusted. Under the pin
`n S = d` at `c_f = 2` it gives the coefficient
`C = alpha b c^2 / (G M) = 14.71` at b = 6 (11.27 at b = 3, 16.95 at 8,
22.07 at 10, 26.09 at 14, 30.18 at 16), not 4 and growing with b (section
7). The number is the fan's in-plane comb, not a constant of the law: on
series K's fan (290 directions, the beam in the mass's plane) the
transverse flow a row sums along its path is 2.1 to 8.3 times the
continuum's (section 8), and one Node off the plane the same row reads
`C = 3.0` at b = 6 and `1.0` at b = 8. The input beyond the pin is the
continuum's `G M` itself: on this GameBoard no reading of one row equals
the shell mean the formula `alpha = 2 c_f (n S / d) G M / (c^2 b)` was
taken in, so the comparison with 4 has no ground here. What does close,
exactly: the ratio of the gamma-1 to the gamma-0 deflection is
`2.06 to 2.17` on the row's momentum (2.00 on the pixels at b = 6), the
declared `c_f = 2` read back with the dwell's second-order term, never
derived; the bending is the push's alone and the delay the wall's alone
(section 6). **The ring of starts (section 9, the reviewer's third
option on the owner's "one scatters detectors on Nodes")** takes the
plane out: the orientation average over every Node at the impact
distance b, on the same fan and the same M, reads `C_ring = 5.12` at
b = 6 (5.44 at b = 3, 5.86 at b = 8) at gamma 1, flat in b within 15
per cent (the `M / b` form recovered) but not 4 within the ring's grain
(0.09 to 0.11); the factor left, 1.28 to 1.46, is the fan's L1 factor of
the flow (the same crowd's shell mean `|V| r^2 / Q = 32.79` against the
continuum's 23.08, `F_L1 = 1.421`, `3 / 2` in the isotropic limit), and
against the push's own constant the ring reads `3.60 / 3.83 / 4.12` at
b = 6 / 3 / 8, the declared `2 c_f` read back, no test of 4. So the
registered geometry's failure is the plane's, what remains is the gap
between the law's two constants of gravity (the clock's, which the pin
makes nature's, and the push's), and the world that decides is the
registered box with a ring of lamps, its arrival Nodes pinned in section
9. The one-line question for the owner is in section 10.

## 1. The order

1. Read the law's lines on main for the key's three rules and the flight
   (section 2), and the registered worlds' numbers from the world files
   under examples/events/optical/ (`examples/events/optical/README.md`, deleted 2026-09-26).
2. Declare the pins before any arithmetic (section 3): `n S = d`,
   `c_f = 2`, the comparison and its tolerance, the calibration.
3. Transcribe the steps as integers (section 4): the flight table, the hop
   rule with the half-wall start, the wall per Link under the key, the
   push, the label's Bresenham, the pair of a pushed row; the stationary
   crowd of the mass from the same flight rule.
4. Calibrate: the algebra must land the registered worlds at their own
   numbers within the grain, else it is not trusted (section 5).
5. Simulate per b, read the arrival Node on the screen of Nodes and the
   click's age, compute `alpha b / (G M)` and the delay at the pin
   (sections 6 and 7), show the reason where it does not close (section 8).
6. Take the plane out: the ring of starts at the impact distance b, the
   orientation average of the comb on the same fan and the same M, with
   its arrival Nodes as the pins of the world that decides (section 9).
7. The verdict (section 10); what a run would add (section 11).

## 2. The inputs table (every input with its kind and its source line, as record 817's table)

The kinds: **law** (the six verbs as the engine runs them on main, with or
without the key); **key** (a declaration of the identity `optical-v1`,
off by default, records 421 to 428); **world** (a declared number of the
world file); **pin** (a condition declared in section 3 of this file);
**comparison** (nature's form, on the comparison side only). No row of
kind law, key, world or pin carries Einstein's, Newton's or Shapiro's
form; they appear in the comparison rows alone.

| Input | Kind | Where it lives on main (file:line) | Its value here |
| --- | --- | --- | --- |
| the flight table: `S_1 = a + b + c` in absolute value, `T_D = isqrt(3 (a^2 + b^2 + c^2) Q^2)`, Q = 64 | law | `nature_beam.py:847-880` (`direction_flight`); BEAM_LAW.md :359-402 | the heading's `T_D = 110`; the beam's `(24, 1, 0)`: 2662; `(12, 1, 0)`: 1334 |
| the hop rule with the half-wall start, `m(tau) = floor((2 tau S_1 Q + T_D) / (2 T_D))`; the accumulator (the count made, the residue) from the start `T_D` at the rate `2 S_1 Q` against the wall `2 T_D` | law | `nature_beam.py:775-818` (`Flight.manhattan_steps`, `accumulator`, `walk_step`); `core/integer.py:79` (`by_drive`) | the fresh row's pair `(0, T_D)` at age 0 |
| the digital line: the axis furthest behind first, the lowest axis first | law | `world.py:1491` (`bresenham_line`) | per direction |
| the unit label `u_D`, the integer vector nearest `Q D / |D|` | law | `nature_beam.py:824` (`unit_label`) | the heading `(64, 0, 0)`; `(24, 1, 0)`: `(64, 3, 0)`; `(12, 1, 0)`: `(64, 5, 0)` |
| the one wall function of the crowd: the rate times d against the wall times `(d + c a_tau n)`, `[n, d]` the suspension pair, `a_tau` the age moment at the Node | law (the clock's member, coefficient 1) | `core/integer.py:118-153` (`age_wall`); `measured.py:344` (`AGE_WALL_SET = (("owed", 1),)`) | the same function on the flight under the key |
| the flight a member of the wall's set at the coefficient `c_f = 1 + gamma` (gamma the world's post-Newtonian parameter) | key (a declaration, P9 of the paper) | `measured.py:349-362` (`FLIGHT_MEMBER`, `age_wall_set`); `world.py:1140-1144` (`flight_coefficient`); `nature_beam.py:3602-3631` (`optical_rate_and_wall`) | `c_f = 1` at gamma 0, `2` at gamma 1 |
| the row's walk under the key: the accumulator gains `rate x d`, a Link when it reaches `wall x (d + c_f n A)`, one Link at most, the surplus kept; the fresh accumulator the family's `(0, T_D)` at the row's age, times d; the Link the label's line step at `made mod S_1`; the error accumulator `c += h x P` on a pushed row | key | `nature_beam.py:3634-3710` (`optical_walk_step`) | transcribed |
| the crowd read twice: the age moment `A` before step 1 from the rows present at the end of the interval before, and the arrival flow `V` after the walk from the interval's own arrivals, each less the reader's own number | key | `nature_beam.py:3069-3160` (`CrowdMoments`, `age_moment`, `arrival_flow`) | the stationary crowd of section 4 (c) |
| the push, `W -= n x weight x V` per interval of dwell at a free Node, the weight per unit `(e_D^2 + 3 gamma u_D . u_D) // e_D` with `e_D = isqrt(3 u_D . u_D)`; the residue rescaled by `S_1(P') / S_1(P)` at every push | key | `nature_beam.py:3807-3885` (`optical_turn`, verb 2); `nature_beam.py:3563` (`unit_weights`) | the heading's weight 110 at gamma 0, 221 at gamma 1; `(12, 1, 0)`: 111 and 222 |
| the label by Bresenham along `P = Q d content u_D + W`: among D and its fan neighbours the Link that keeps `|c + h x P|^2` smallest among those with `h . P > 0`, ties to D then the fan's order; `W += Q d content (u_D - u_D')` so P is conserved | key | `nature_beam.py:3886-3970` (`optical_turn`, verb 3); `nature_beam.py:895` (`fan_neighbours`) | transcribed |
| the pair of a pushed row, `(S_1(P), T(P))` of P over its gcd, `T = isqrt(3 |P|^2 Q^2)` (the photon's rest term 0) | key | `nature_beam.py:3494-3560` (`momentum_pair`); `:3585` (`row_pairs`) | transcribed |
| no push and no turn at an occupied Node | key | `nature_beam.py:3807` (`~occupied[store.node]`) | the lamp's own Node |
| the rule at the mass's Node: the arriving row takes the mass's table entry for its family, and the registered mass declares none (`mass_g0.json`), so the family's default rule, `measure` for a paid family (the row is measured by the mass, the click; the engine has no other rule there) | law (the default table) | `world.py:855` (`default_rule`), `:868` (`default_table`); ENGINE.md :671-672 | matched in the map; no beam line reaches the mass's Node on the registered fan at b >= 3, so sections 5 to 7 never invoke it; section 8's dense-fan rows do |
| the suspension pair `[n, d]` | world | `examples/events/optical/mass_g0.json` (`"suspension": [1, 16384]`); `optical/make_worlds.py:42` | `[1, 16384]` |
| the width S | world | none declared in `examples/events/optical/*.json`: the default 1 (`world.py:29-34`) | S = 1 in the register; `S = 16384` under the pin |
| gamma | world (a declared input of kind 2, record 826 (D)) | `optical/*_g0.json` `"optical": 0`, `*_g1.json` `"optical": 1` | 0 and 1 |
| the mass M and its release: `by_clock(age, M, 4096)` units per direction per interval on the fan of 290 primitive directions with `|a| + |b| + |c| <= 6` | world | `lensing/make_worlds.py:87-88` (`SOURCE = 1 << 12`, `FAN_MANHATTAN = 6`); `optical/make_worlds.py:44` (`MASS_FACTOR = 16`) | 16 units per direction per interval at `M = 2^16`, 1 at `2^12`; `q = 290 M / 4096` units per interval |
| the box, the lamp, the screen: shape (57, 41, 41), the mass at (28, 20, 20), the lamp at x = 2 and y = 20 + b, the screen the plane x = 54 of 1681 one-Node `wave` detectors reading `age` | world | `lensing/make_worlds.py:77-80, 93` | the lamp 26 Links before the mass, the screen 26 after |
| the beam: the heading and four in-plane directions | world | `lensing/make_worlds.py:93` (`BEAM`) | `(1, 0, 0)`, `(24, +-1, 0)`, `(12, +-1, 0)` |
| the world's direction table: two rest slots, the six headings, then the declared list | law | `world.py:1449` | 296 entries |
| K, N, the ticks, the window | world | `lensing/make_worlds.py:81-82, 89`; `tools/lensing_readings.py:135` (`WINDOW_START = 110`) | `K = 2^30`, `N = 64`, 400 ticks, the window [110, 400] |
| the content of a light row | world (the lamp's rows are of amount 1, content the family's quantum 1) | `nature_beam.py:5748-5770` | 1; the push and P both scale with it, so the turn is content-free |
| `G M = q / (4 pi S)`, the law's Newton constant from the push in the continuum | law's continuum (a shell-mean identity) | [one_wall/NOTE.md](../one_wall/NOTE.md) section 5 ("the one constant"); [einstein_outside/DERIVATION.md](../einstein_outside/DERIVATION.md) II.11 :1318 | `q / (4 pi S)` |
| `c = 1 / sqrt 3` Links per interval | law | BEAM_LAW.md :359-402 | `c^2 = 1 / 3` |
| `alpha = 4 G M / (c^2 b)` (Einstein), `2 G M / (c^2 b)` (Newton); Shapiro's `(1 + gamma_PPN) (G M / c^3) ln(4 r_1 r_2 / b^2)` | comparison only | [NATURE.md](../../NATURE.md) row 13; II.11 | never an input |

## 3. The pins, declared before any arithmetic

- **P1, the pin of the constant: `n S = d` and `c_f = 2`.** The
  suspension pair's `n / d` is the inverse of the width S (II.10a: the
  clock's suspension and the push's width one declared number), and the
  flight's coefficient is nature's `1 + gamma_PPN = 2` (the time part 1
  and the space part 1). With the register's `[1, 16384]` the pin means
  `S = 16384`. The width enters no rule of a light row (the photon's
  tables are Flight's by value, `nature_beam.py:1074-1095`; the push's
  scale is `Q d`, not `Q S`; the lamp's owed count is `n A / d`): under
  the pin the light's clicks are the registered worlds' byte for byte,
  and the pin acts on the conversion alone, through `G M = q / (4 pi S)`.
- **P2, the comparison and its tolerance.** The quantity compared is
  `C = alpha b c^2 / (G M)` with `c^2 = 1 / 3` and `G M = q / (4 pi S)`,
  against Einstein's 4 (Newton's 2). Beside it the lattice-internal form
  `C' = tan alpha / k(b)`, `k(b) = n A(0, b, 0) / d` the clock's own k at
  the beam's Node nearest the mass, the same 4 in the continuum at the
  pin (`alpha = 2 c_f k(b)`), an exact rational on the GameBoard. The
  tolerance is the grain of one Node over the screen distance: one Node
  of the screen over the 26 Links from the mass to the screen,
  `1 / 26 = 0.03846` radian per line; on C at the pin
  `(1 / 26) / (G M / (c^2 b)) = 0.5689 b` per line (3.41 at b = 6, 4.55
  at b = 8), a fifth of it on the five-line mean (0.68 at b = 6); on C'
  `(1 / 26) / k(b)` = 1.88 per line at b = 6 (0.38 on the mean). The
  row's momentum P gives `tan alpha` with no such grain (GAMEBOARD); the
  arrival Node (the detector's reading) has it.
- **P3, the calibration.** Before any number at the pin, the step
  algebra must land the registered worlds (M = 2^16, `[1, 16384]`,
  S = 1) at their own DETECTOR numbers: the mass world's centroid shift
  `-1.993 / -3.989` pixels at gamma 0 / 1 and its delays `2.95 / 4.94`
  intervals within the grain, the grain being one Node on one of the five
  lines, `0.2` pixel on the five-line mean, and 1 interval on the mean
  age (the register's own bracket); the far world (`-1.773 / -3.403`,
  `2.56 / 4.33`) and the near world (`-2.608 / -6.412`, `2.99 / 6.20`)
  beside it; and the control's mean age `89.40` exactly. Else the
  simulation is not trusted and this file says so.
- **P4, what would refute the reading of the two verbs.** The wall
  unstretched (coefficient 0) must leave the landing Node unchanged if
  the bending is the push's alone; the push off (V = 0) must leave the
  delay unchanged if the delay is the wall's alone.
- **P5, the b form.** `C` constant in b within the grain reads the
  `M / b` form; `C` growing with b reads the comb (the note's section 4:
  the in-plane lines cross the row's line once whatever b).

## 4. The step algebra (what is declared, what follows)

**(a) The state of one row of light**, five integers and three vectors,
nothing else: its Node, its direction label D (an index into the world's
table), the count `made` of Links since birth, the residue s of the
flight's accumulator (in units of `1 / d`), the age tau; the push
accumulator **W** (three integers), the error accumulator **c** (three
integers); `content = 1`. The declared constants of the table: per
direction `S_1`, `T_D`, the line, `u_D`, `e_D`, the weight, the six
neighbours.

**(b) One interval**, in the engine's order, all integers:

    verb 1 (the walk): A = the crowd's age moment at the row's Node (the interval before)
                       (r0, w0) = (2 S_1 Q, 2 T_D) on a row never pushed, else (2 S_1(P) Q, 2 T(P))
                       s += r0 d;  if s >= w0 (d + c_f n A): s -= w0 (d + c_f n A), the Link h = line_D[made mod S_1],
                       c += h x P (a pushed row), made += 1, the Node moves by h
    verb 2 (the push): at a free Node, V = the arrival flow there (this interval's arrivals);
                       W -= n x weight_D x V;  s = s x S_1(P') // S_1(P)  (the rate's ratio, floor)
    verb 3 (the label): P = Q d u_D + W; among D and its neighbours the h = line_D'[made mod S_1(D')] with h . P > 0
                       that keeps |c + h x P|^2 smallest; if D' differs, W += Q d (u_D - u_D'), D = D'
    the click: the Node with x = 26 is the screen's; the row's age there is the click's reading (`reads: age`)

Declared (the key): the flight in the wall's set at `c_f`; the push's
weight `(1 + gamma) e_D` within one unit; the label by Bresenham on P;
the pair of a pushed row on P. The law's: the flight table, the hop rule,
the one wall function, the one count primitive. Nothing here is Einstein's
form; `c_f = 2` is a number put in.

**(c) The crowd**, from the same flight rule, exactly: the mass at the
origin releases `scale = M / 4096` units on each of the 290 directions
every interval; the row of direction D at age tau sits at the
`m(tau)`-th Node of D's line, so at a Node reached at the Link `made` of
D's line the rows present at the end of an interval have the ages
`{tau : m(tau) = made}` = `[age_of(made), age_of(made + 1))`, and one row
of D arrives there per interval. Hence, for every Node inside the box,

    A(r) = scale x sum over the lines D through r of the sum of those ages     (the age moment)
    V(r) = scale x sum over the lines D through r of u_D                        (the arrival flow)

constant in time once the oldest row that reaches r has been born (the
ages at the beam's Nodes are below 60; the register's window begins at
110). This is what the engine's `CrowdMoments` sums, less the reader's
own number (the beam's rows are of the lamp's number and never enter it);
the light-bending map computed the same lines
([light_bending_map.py](../open_problems/light_bending/light_bending_map.py)).
At the beam's Node nearest the mass, `A(0, 6, 0) = 21 x scale` (the ages
10 and 11 of the line `(0, 1, 0)` at its Link 6), `A(0, 3, 0) = 29 x
scale`, `A(0, 8, 0) = 27 x scale`.

**(d) The reading.** Every Node of the screen is a detector (the 1681
`wave` pixels of series K's world file; the passive detector at every
Node of record 721 is here the declared screen). The reading of one line
is its arrival Node `(26, y, z)` and the row's age there; the beam's
reading is the mean over its five lines against the control's (the
count-weighted centroid the readings tool forms, each line landing every
one of its rows at one Node once the crowd is stationary); the delay the
mean click age less the control's. The shift's sign is negative toward
the mass.

**(e) The two exact deflection numbers.** From the arrival Node, the
shift in pixels (the detector's grain, one Node per line); from the row's
momentum at the screen, `tan alpha = -(P0 x P)_z / (P0 . P)` with P0 the
momentum at birth, an exact rational (GAMEBOARD, the host's view of the
row), positive toward the mass.

## 5. The calibration (P3): the registered worlds landed by the step algebra

M = 2^16, the pair `[1, 16384]`, S = 1 as the world files declare it (so
`n S / d = 2^-14` in these worlds; record 826 (E)'s 16 is the width
`2^20` of the 35 crowd worlds, which the optical worlds do not declare).
The control: the five lines land at `y_lamp + (0, +2, -2, +4, -4)`, the
click ages 89, 90, 90, 89, 89, the mean `89.40`, the register's `89.40`
exactly (DETECTOR, series K and the optical controls). The step algebra's
simulation of the board, not a run:

| World | gamma | the five lines' shifts, pixels (the arrival Node less the control's) | the mean shift | registered (DETECTOR) | the five lines' delays, intervals | the mean delay | registered (DETECTOR) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `mass` (b = 6) | 0 | -2, -2, -2, -2, -2 | `-2.000` | `-1.993` | 4, 3, 2, 3, 3 | `3.00` | `2.95` |
| `mass` (b = 6) | 1 | -4, -4, -4, -4, -4 | `-4.000` | `-3.989` | 5, 6, 4, 4, 6 | `5.00` | `4.94` |
| `far` (b = 8) | 0 | -2, -1, -2, -2, -2 | `-1.800` | `-1.773` | 3, 1, 2, 2, 4 | `2.40` | `2.56` |
| `far` (b = 8) | 1 | -4, -3, -4, -3, -3 | `-3.400` | `-3.403` | 6, 5, 4, 2, 5 | `4.40` | `4.33` |
| `near` (b = 3) | 0 | -2, -2, -3, -1, -5 | `-2.600` | `-2.608` | 2, 2, 1, 5, 4 | `2.80` | `2.99` |
| `near` (b = 3) | 1 | -6, -5, -6, -3, -12 | `-6.400` | `-6.412` | 5, 2, 5, 6, 12 | `6.00` | `6.20` |

Every shift within 0.03 pixel of the register (the grain 0.2), every
delay within 0.2 interval (the bracket 1). The residuals are the early
window's transient: the rows born before tick 48 walk their first Links
through a crowd not yet stationary, about 30 births of 291 per line, and
the register's `-1.993` is `-2.000` with 9 rows of 1347 landed one Node
less. The register's ratio `2.00` of the mass shifts is here `-4 / -2`
exactly. One transcription decided the far world: the engine pushes no
row at an occupied Node, and at the mass world the lamp's own Node holds
an age moment `A = 1456`, `1456 n / d = 0.0889` that keeps the row from its first Link for
one interval (the lamp's clock rate 0.918 of the register, GAMEBOARD);
without that line the far world at gamma 1 landed one line one Node
further. **The calibration pin is MET; the simulation is trusted.**

## 6. The simulation per b: the arrival Node and the shift, the click's age and the delay

M = 2^16 unless marked, the crowd's `q = 4640` units per interval, the
pair `[1, 16384]`; every line's landing Node in
[step_algebra_map.out](step_algebra_map.out) section 3. The step
algebra's simulation of the board, not a run:

| b | gamma | the shifts per line, pixels | the mean shift | the mean delay, intervals | `tan alpha` (the momentum, exact in the .out) | the ratio gamma 1 / gamma 0 of `tan alpha` |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 0 | -2, -2, -3, -1, -5 | -2.600 | 2.80 | 0.12022 | |
| 3 | 1 | -6, -5, -6, -3, -12 | -6.400 | 6.00 | 0.25391 | 2.112 |
| 6 | 0 | -2, -2, -2, -2, -2 | -2.000 | 3.00 | 0.07840 | |
| 6 | 1 | -4, -4, -4, -4, -4 | -4.000 | 5.00 | 0.16577 | 2.114 |
| 8 | 0 | -2, -1, -2, -2, -2 | -1.800 | 2.40 | 0.06900 | |
| 8 | 1 | -4, -3, -4, -3, -3 | -3.400 | 4.40 | 0.14328 | 2.077 |
| 10 | 0 | -2, -1, -2, -2, -1 | -1.600 | 2.00 | 0.06870 | |
| 10 | 1 | -4, -4, -4, -3, -4 | -3.800 | 4.00 | 0.14919 | 2.172 |
| 14 | 0 | -2, -1, -2, -2, -2 | -1.800 | 2.20 | 0.06126 | |
| 14 | 1 | -3, -3, -3, -3, -3 | -3.000 | 3.20 | 0.12601 | 2.057 |
| 16 | 0 | -1, -1, -2, -2, -2 | -1.600 | 2.20 | 0.06067 | |
| 16 | 1 | -3, -3, -3, -3, -3 | -3.000 | 3.80 | 0.12751 | 2.102 |
| 18 (four lines: `(12, 1, 0)` leaves the box at (4, 21, 0)) | 0 | -1, -1, -1, -, -1 | -1.000 | 1.25 | 0.05166 | |
| 18 | 1 | -3, -2, -3, -, -3 | -2.750 | 3.25 | 0.11348 | 2.133 |
| 6, M = 2^12 | 0 | 0, 0, 0, 0, 0 | 0.000 | 0.20 | 0.00485 | |
| 6, M = 2^12 | 1 | 0, 0, -1, 0, 0 | -0.200 | 1.00 | 0.00978 | 2.017 |
| 8, M = 2^12 | 0 | 0, 0, 0, 0, 0 | 0.000 | 0.20 | 0.00444 | |
| 8, M = 2^12 | 1 | 0, 0, -1, 0, 0 | -0.200 | 1.00 | 0.00885 | 1.994 |

The body worlds at b = 14, 16 and 18 named in the order are not on main
(record 826 (C): the fifteen body worlds of step 3 on the branch
`optical-body-drive`); the light row is walked at those b on the
registered box, where the box's width (y up to 20 from the mass) cuts one
beam line at b = 18. At M = 2^12 the deflection is a hundredth of a
radian, under the screen's grain: the arrival Node moves on one line in
ten, the momentum's `tan alpha` is a sixteenth of the 2^16 value, as the
push's linearity in the crowd says.

**The two verbs apart (P4).** At b = 6, gamma 1, the wall unstretched
(coefficient 0 on the flight, a reading the engine refuses and the
algebra can make) lands the five lines at `-4, -4, -4, -4, -4`, the
rule's own landing, with the delays `1, 1, 0, 0, 2` (the bent path's
extra Links, second order in the angle); the push off (V = 0) lands them
at `0, 0, 0, 0, 0` with the delays `5, 4, 5, 4, 5`. At b = 8 the same,
with one line one Node apart between the rule and the unstretched wall
(`-4` against `-3`: the wall's slowing lengthens the dwell, and the push
is per interval of dwell). So: **the bending is the push's alone, the
delay the wall's alone plus the bent path's Links; the wall bends
nothing by itself** (the one-wall note's section 5 (a), now shown on the
rule as built), and the coupling of the two is the dwell: the deflection
carries the factor `(1 + c_f k)` of the stretched dwell, which is why the
ratio gamma 1 / gamma 0 of `tan alpha` is `2.06 to 2.17` and not 2.00
(`2 (1 + 2 k) / (1 + k)` at `k = 0.02 to 0.05`), while the pixels at
b = 6 read `2.00`. The ratio is the declared `c_f` read back, in the
weight and in the wall, RECOVERED and not derived.

## 7. The coefficient `alpha b / (G M)` and the Shapiro delay at the pin

Under P1 (`S = 16384`, `c_f = 2`): `G M = q / (4 pi S)`,
`G M / c^2 = 3 q / (4 pi S) = 0.067610` Links at M = 2^16 (`0.004226` at
2^12), the same light numbers as section 6. C from the momentum's
`tan alpha` (its lattice part an exact rational, the `4 pi` beside it);
C' the exact rational `tan alpha / k(b)`; C from the arrival Nodes takes
`-shift / 26` in place of `tan alpha`. The step algebra's simulation of
the board, not a run:

| b | `A(0, b, 0)` | `k(b) = n A / d` | gamma | `C = alpha b c^2 / (G M)` | C from the arrival Nodes | `C' = tan alpha / k(b)` (exact in the .out) | the delay, intervals (the mean click age less the control's) | Shapiro's `c_f (n S / d) (G M / c^3) ln(4 L^2 / b^2)`, L = 26 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 464 | 0.028320 | 0 | 5.33 | 4.44 | 4.24 | 2.80 | 0.67 |
| 3 | 464 | 0.028320 | 1 | **11.27** | 10.92 | 8.97 | 6.00 | 1.34 |
| 6 | 336 | 0.020508 | 0 | 6.96 | 6.83 | 3.82 | 3.00 | 0.51 |
| 6 | 336 | 0.020508 | 1 | **14.71** | 13.65 | 8.08 | 5.00 | 1.01 |
| 8 | 432 | 0.026367 | 0 | 8.16 | 8.19 | 2.62 | 2.40 | 0.44 |
| 8 | 432 | 0.026367 | 1 | **16.95** | 15.47 | 5.43 | 4.40 | 0.88 |
| 10 | 560 | 0.034180 | 0 | 10.16 | 9.10 | 2.01 | 2.00 | 0.39 |
| 10 | 560 | 0.034180 | 1 | **22.07** | 21.62 | 4.36 | 4.00 | 0.77 |
| 14 | 384 | 0.023438 | 0 | 12.68 | 14.34 | 2.61 | 2.20 | 0.31 |
| 14 | 384 | 0.023438 | 1 | **26.09** | 23.89 | 5.38 | 3.20 | 0.62 |
| 16 | 880 | 0.053711 | 0 | 14.36 | 14.56 | 1.13 | 2.20 | 0.28 |
| 16 | 880 | 0.053711 | 1 | **30.18** | 27.31 | 2.37 | 3.80 | 0.55 |
| 18 (four lines) | 496 | 0.030273 | 0 | 13.75 | 10.24 | 1.71 | 1.25 | 0.25 |
| 18 (four lines) | 496 | 0.030273 | 1 | **30.21** | 28.16 | 3.75 | 3.25 | 0.50 |
| 6, M = 2^12 | 21 | 0.001282 | 0 | 6.89 | 0.00 | 3.78 | 0.20 | 0.03 |
| 6, M = 2^12 | 21 | 0.001282 | 1 | 13.89 | 10.92 | 7.63 | 1.00 | 0.06 |
| 8, M = 2^12 | 27 | 0.001648 | 0 | 8.40 | 0.00 | 2.69 | 0.20 | 0.03 |
| 8, M = 2^12 | 27 | 0.001648 | 1 | 16.76 | 14.56 | 5.37 | 1.00 | 0.06 |

The exact rational at the calibration world, b = 6, gamma 1:
`C' = 12893848856972110694686063399872767165696 / 1595121552073993109668023640256512470369 = 8.0833`,
from `tan alpha = 50366597097547307401117435155752996741 / 303832676585522497079623550525049994356 = 0.16577`
and `k(6) = 336 / 16384`.

Read against the pins: **C is not 4 at any b, and it grows with b** (P5:
the comb, not the `M / b` form); the tolerance of P2 (0.68 on the
five-line mean at b = 6) does not reach it. C' is 8.08 at b = 6 and
wanders from 2.4 to 9.0 with b: the clock's word at the one Node nearest
the mass and the push's word summed along the path are not one constant
on these lines. The delay is 4.6 to 5.0 times Shapiro's at b = 6 and
grows with b relative to it, the same comb in the wall's sum (the
light-bending note's 5.4 at b = 6 in the shell-mean form). Under the pin
the register's own DETECTOR numbers (-1.993 / -3.989 pixels) convert to
`C = 13.65` from the arrival Nodes at gamma 1: NATURE row 13 stays NOT
COMPARED, and would read 13.65 against 4 if compared on this geometry.

## 8. The reason, shown: the fan's in-plane comb

The heading's path from x = -26 to +25 at y = b sums the transverse flow
`V_y` at its Nodes times its dwell there (the push's integrand); the
continuum's value for the same crowd is
`2 q Q b / (4 pi) x L / (b sqrt(L^2 + b^2)) x sqrt 3` (label units times
intervals). GAMEBOARD arithmetic of the lines:

| b | the lattice's path sum | the continuum's | the ratio |
| --- | --- | --- | --- |
| 3 | 56416 | 27107 | 2.08 |
| 6 | 44432 | 13294 | 3.34 |
| 8 | 39968 | 9780 | 4.09 |
| 10 | 44512 | 7641 | 5.83 |
| 14 | 37328 | 5148 | 7.25 |
| 16 | 35952 | 4357 | 8.25 |
| 18 | 27760 | 3739 | 7.42 |

The lattice's sum is nearly flat in b (the 48 in-plane lines of the fan
each cross the row's line once whatever b, the note's section 4) while
the continuum's falls as `1 / b`: the row on this geometry reads the
b-exponent 0, not 1, and C grows as b. The reason in one sentence: the
beam lies in the fan's symmetry plane z = 0, where the 48 in-plane lines
are a two-dimensional fan of line density `1 / r`, so the transverse
impulse summed along a straight path is independent of b (the exponent 0
of a two-dimensional inverse-first-power field), and one Node off the
plane the crossings are isolated Nodes (the table below, C 1.0 to 3.0).
This is the whole of the gap to 4
at gamma 1 (`14.71 / 4 = 3.68` against the flow ratio 3.34 at b = 6, the
rest the dwell's `1 + c_f k` and the pixel's rounding).

The same rows off the plane and at denser fans (not registered worlds,
no pin moved; the reason tested, not a new world proposed):

| The change | b | the shifts per line | `tan alpha` | C against 4 |
| --- | --- | --- | --- | --- |
| the beam one Node off the plane (z = 1) | 6 | -1, 0, -2, 0, -2 | 0.03342 | 3.01 |
| the beam one Node off the plane (z = 1) | 8 | 0, 0, -1, 0, 0 | 0.00835 | 0.99 |
| the beam two Nodes off the plane (z = 2) | 6 | -1, -1, -2, -1, -2 | 0.06115 | 5.72 |
| the beam two Nodes off the plane (z = 2) | 8 | -1, -1, -2, 0, -1 | 0.04037 | 4.92 |
| the fan at P = 8 (674 directions, q = 10784) | 6 | -7, -7, -9, -3, -13 | 0.34909 | 13.33 |
| the fan at P = 10 (1250 directions, q = 20000) | 6 | -13, -2, -17, -3 (one line measured by the mass or out of the box) | 0.52666 | 10.84 |
| the fan at P = 12 (2114 directions, q = 33824) | 6 | -2, -3 (three lines measured by the mass or out of the box) | 0.60412 | 7.36 |

One Node off the plane the row reads a third to a tenth of the in-plane
sum and C falls to 1 to 3; a denser fan at the same M puts the row in the
strong field (turns of 0.35 to 0.6 radian; rows that reach the mass's
Node) and does not give a limit. The dense-fan rows follow the map's
rule at the mass's Node, which is the engine's default for a paid family
arriving at a measured event without a table entry, `measure` (the
inputs table): the row is measured by the mass and ends there; at the
registered fan no beam line reaches that Node. The reading of one row at
P = 6 is the lines, not a field: the formula's `G M` is a shell mean that
no Node of this box carries.

## 9. The ring of starts: the orientation average of the comb (the reviewer's third option; the owner's "one scatters detectors on Nodes")

**The construction, on the same fan and the same M, no scaling.** One
row of light on the heading `(1, 0, 0)` from every start on the ring of
impact distance b: every Node `(y, z)` of the lamp's plane x = 2 with
`|sqrt(y^2 + z^2) - b| <= 1 / 2` about the mass's line (16 starts at
b = 3, 40 at b = 6, 48 at b = 8; the list in the .out, section 9), the
whole screen read, every Node of it a detector. Per start the radial
deflection toward the mass's line, from the momentum at the screen
`tan alpha_r = -(P_y y + P_z z) / (P_x r)` with `r = sqrt(y^2 + z^2)`
(GAMEBOARD, exact up to the root in r) and from the arrival Node its
radial shift `-(dy y + dz z) / r` in Links (the detector's reading); the
tangential component beside it as a check of the symmetry. The ring's
mean is the orientation average of the comb, which is what the shell
mean is, with no denser fan and no scaling of M. The coefficient
`C_ring = mean(tan alpha_r x r) x 4 pi S / (3 q)` against 4 under the
pin, and beside it the same against the lattice's own push constant:
from the same crowd the shell mean of `|V| r^2 / Q` over r = 4 .. 14 is
32.79 against the continuum's `q / (4 pi) = 23.08`, the fan's L1 factor
`F_L1 = 1.421` (the one-wall note's section 5 found the same 32.79
against 23.08). **Where F_L1 comes from and where it goes** (the
physics-rule reviewer's line, the numbers computed here): the arrival
flow counts one arrival per Node per interval on each line, and a
digital line has `S_1 / |D|` Nodes per Euclidean Link, so the flow's
shell mean carries the fan's mean of `S_1 / |D|`: 1.436 over the 290
directions (computed in the map, the .out's section 9 line) and 1.421
weighted by the shells; while the clock's presence per Node on a line,
the dwell `sqrt 3 |D| / S_1` intervals, cancels that incidence, so the
age moment's shell mean is the continuum's with no L1 factor (computed
here from the same crowd: `A r = 68.72` over r = 4 .. 14 against the
continuum's `3 q / (4 pi) = 69.23`), which is why the one-wall note
found 32.79 against 23.08 between the two words. And the factor is not
the finite fan's: in the isotropic limit the mean of `|x| + |y| + |z|`
over the unit sphere is exactly `3 / 2` (the mean of `|x|` is `1 / 2`;
computed here by quadrature, 1.5000), so a denser fan raises F_L1 toward
1.5, and the ring's C against the clock's `G M` tends to `2 c_f x 3 / 2
= 6` at `c_f = 2`, not to 4. So the push a body reads on this fan is
`1.421 x q / (4 pi S r^2)`, `3 / 2 x q / (4 pi S r^2)` in the limit, and
`C_ring / F_L1` is the input read back: `2 c_f` by construction, 4 at
`c_f = 2`, the residual 3.6 to 4.1 the grain and the dwell's `1 + c_f k`;
it is no test of 4. The grain: one Node per start
over the 26 Links, `1 / 26` radian per start, `0.5689 b` on C per start,
divided by the ring's count on its mean. The step algebra's simulation
of the board, not a run:

| b | starts | gamma | the ring's mean `tan alpha_r` | `C_ring` against 4 (the continuum's `G M`) | `C_ring / F_L1` (the lattice's own push constant) | the mean radial shift of the arrival Node, Links | C from the arrival Nodes | the mean delay, intervals | the grain on `C_ring` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 16 | 0 | 0.05826 | 2.605 | 1.834 | 0.996 | 1.700 | 0.19 | 0.107 |
| 3 | 16 | 1 | 0.12143 | **5.442** | **3.830** | 2.091 | 3.568 | 0.12 | 0.107 |
| 6 | 40 | 0 | 0.02915 | 2.599 | 1.829 | 0.451 | 1.541 | 0.55 | 0.085 |
| 6 | 40 | 1 | 0.05719 | **5.116** | **3.600** | 0.974 | 3.323 | 0.25 | 0.085 |
| 8 | 48 | 0 | 0.02449 | 2.905 | 2.045 | 0.409 | 1.864 | 0.35 | 0.095 |
| 8 | 48 | 1 | 0.04949 | **5.859** | **4.123** | 0.854 | 3.889 | 0.60 | 0.095 |

The tangential component averages to 0.00000 at every ring (the ring is
symmetric under the fan's 48 signed axis permutations, and so is the
crowd). The ratio gamma 1 / gamma 0 of the ring's mean is 2.09, 1.97
and 2.02 at b = 3, 6, 8.

**Read against the pins.** (i) The `M / b` form returns: `C_ring` is
5.44, 5.12, 5.86 at b = 3, 6, 8, flat within 15 per cent where the
in-plane row read 11.3, 14.7, 17.0 growing with b (section 7); the
plane was the b-exponent's failure. (ii) Against the continuum's
`G M = q / (4 pi S)` the ring does not read 4 within its grain: the
number is 5.1 to 5.9 at gamma 1, 2.6 to 2.9 at gamma 0, above Einstein's
4 and Newton's 2 by the factor 1.28 to 1.46. (iii) That factor is the
fan's L1 factor of the flow, 1.421, a constant of the fan's Manhattan
lines and not of b, `3 / 2` in the isotropic limit: the column
`C_ring / F_L1` (3.60, 3.83 and 4.12 at b = 6, 3 and 8 at gamma 1; 1.83,
1.83, 2.05 at gamma 0) is the declared `2 c_f` read back through the
push's own constant, 4 at `c_f = 2` by construction, its residual the
grain and the dwell's `1 + c_f k`; it tests nothing about 4. (iv) The
screen's own reading, the arrival
Node's radial shift, gives a smaller C (3.3 to 3.9 against the
continuum's `G M`) than the momentum does, because the bend is spread
along the whole path (the fan's lines cross the row from x = -26 to
+26) and the lever arm to the screen is shorter than 26 Links for the
part of the bend made after the mass; a run reads the Nodes, so the pin
of the ring world is the Nodes and their mean, not the momentum.

**The verdict of this section.** The registered geometry's failure is
the plane's, not the fan's: the orientation average removes the growth
with b and brings the coefficient from 11 to 30 down to 5.1 to 5.9, and
what remains is the fan's L1 factor of the flow, 1.42 on this fan and
`3 / 2` in the limit, the same constant the one-wall note found between
the clock's word and the push's word. Against the clock's `G M`, which
the pin `n S = d` makes nature's, the ring does not read 4: the number is
5.12 at b = 6 and tends to 6 with a denser fan; against the push's own
constant it reads the declared `2 c_f` back, no test. The law has two
constants of gravity on this GameBoard, the clock's and the push's,
F_L1 apart; which one the coefficient stands on is the owner's question
of section 10, now with the plane out of it. **The world that decides**, one world, on the owner's
word only: the registered box, fan, mass `2^16` and pair `[1, 16384]`
with the width 16384 declared (the pin), the lamp replaced by a ring of
lamps on the heading at every start listed in the .out (40 at b = 6),
the screen as it is; its pins, from this section before any run
(DETECTOR when run): per start the arrival Node of the .out (section 9,
each `dy, dz`), the ring's mean radial shift `0.974 +- 0.025` Links at
gamma 1 and `0.451 +- 0.025` at gamma 0 at b = 6 (one Node per start
over 40 starts), the ring's mean delay `0.25` and `0.55` intervals
within 1, the tangential mean 0 within a Node, the ratio of the two
radial means 2.16 within the propagated grain; at b = 8 `0.854` and
`0.409` Links over 48 starts. A world whose ring is a lamp emitting on
many directions from one Node reads the same crowd but not the same
starts, and needs its own pins.

## 10. The verdict

**CANNOT CLOSE.** The step algebra simulates the board exactly (P3 met)
and gives, under the pin `n S = d` at `c_f = 2`, the coefficient
`C = alpha b c^2 / (G M) = 14.71` at b = 6 (11.27 at b = 3, 16.95 at 8,
22.07 at 10, 26.09 at 14, 30.18 at 16; 6.96 at b = 6 at gamma 0), not 4
and not constant in b, with the exact rationals in the .out. The number
is the geometry's: the transverse flow a row sums along series K's beam,
in the mass's plane at the fan of 290, is 2.1 to 8.3 times the continuum
value that `alpha = 2 c_f (n S / d) G M / (c^2 b)` was taken in, so the
missing thing is not a declaration of the law but the ground of the
comparison, the continuum's `G M`, which no reading of one row equals on
the registered box. What is declared: `c_f = 2` (the key), `[1, 16384]`
and the fan (the world), `n S = d` (the pin). What follows: the ratio
gamma 1 / gamma 0 `2.06 to 2.17` on the momentum and `2.00` on the pixels
at b = 6 (the declared `c_f` read back, with the dwell's second-order
term); the bending the push's alone and the delay the wall's alone; the
delay's sum and the bending's sum both the comb's. Nothing is derived:
the 2 of `c_f` is an input (record 826 (D)), the pin a declaration
(II.10a), and 4 is not reached. The one-line question for the owner:
**shall the coefficient be read against the law's own Newton on the same
lines, where it is `2 c_f n S / d = 4` at the pin by construction (the
input read back, the space part still an input), or against the
continuum's `G M`, which needs one new world where a row reads the shell
mean (the beam off the mass's plane at a denser fan with M scaled down
by the fan's count, a new pin from this algebra before it runs)?** With
the plane taken out by the ring of section 9 the question is the
choice between the law's two constants of gravity: **the clock's, `q /
(4 pi S)` from the age moment (the pin `n S = d` makes it nature's `G
M`), against which the ring reads 5.1 to 5.9 and tends to 6 with a
denser fan; or the push's, `F_L1` times larger on the registered fan
(1.421) and `3 / 2` times in the isotropic limit, against which the ring
reads the declared `2 c_f` back.** Two ways to make the two one, named
and not proposed: a rule change under its own identity, the flow
weighted per line by `|D| / S_1` (the label per Euclidean Link in place
of per Node), which would remove F_L1 from the push and leave the wall's
delay as it is; or `c_f` absorbing the factor, `1 + gamma = 4 / 3` in
the limit, which the wall's delay would then miss by the same `3 / 2`.
The ring world of section 9 reads the coefficient on either ground.

## 11. What a run would add

One world at the pin on the registered geometry (`width 16384` beside
`suspension [1, 16384]`, the same lamp, mass, fan and screen) would read
the light's clicks byte for byte as the registered worlds do (the width
enters no rule of a light row, section 3 P1): it adds nothing to the
light; it re-pins the lamp's clock and any body's fall in that world to
`n S / d = 1` (II.10a), a re-read of the lamp's rate 0.918. The run that
would decide the coefficient is the ring world of section 9, on the
owner's word only: the registered box with a ring of lamps at the impact
distance b on the same fan and the same M, its pins the arrival Nodes
this algebra computes before the run (section 9), the reading the
screen's clicks and ages (DETECTOR), the comparison C_ring against 4
within the ring's grain, once on the continuum's `G M` and once on the
lattice's own push constant, both stated before the run. The denser fan
off the plane with M scaled down (section 8) is the second world, not
needed for the plane's question. No world file is written here.

## 12. Links

- [step_algebra_map.py](step_algebra_map.py), [step_algebra_map.out](step_algebra_map.out): the arithmetic of this file.
- examples/events/optical/README.md (`examples/events/optical/README.md`, deleted 2026-09-26): the registered worlds and their runs (DETECTOR).
- [docs/designs/one_wall/NOTE.md](../one_wall/NOTE.md), [EVERY_FAMILY.md](../one_wall/EVERY_FAMILY.md): the key's rules as designed.
- [docs/designs/open_problems/light_bending/NOTE.md](../open_problems/light_bending/NOTE.md): the lattice's lines and the comb (section 4), the pins of the register.
- [docs/designs/einstein_outside/DERIVATION.md](../einstein_outside/DERIVATION.md) II.10a and II.11: the pin `n S = d` and the closed form under the key.
- [docs/NATURE.md](../../NATURE.md) row 13: NOT COMPARED, unchanged by this file.
- [docs/LOG_2026-09-20.md](../../LOG_2026-09-20.md) records 721, 762, 817, 822, 826.
