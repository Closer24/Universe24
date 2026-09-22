# flow-link-v1: one arrival counts one Euclidean Link of its line, not one Node; the push's constant of gravity becomes the clock's (the Flow Weight Designer, 2026-09-22; a design, no build)

The order (the Boss, 2026-09-22, about 10:40Z, on the model owner's go of
record 886 to the Boss's recommendation (c) of record 884 of
[the log](../../LOG_2026-09-20.md)): a hypothesis under its own identity
that makes the law's two constants of gravity one, so that the light
bending's comparison has one ground; the ring world runs on it only after
the physics-rule reviewer's gate and on the owner's go. A design only:
this file, the map [flow_weight_map.py](flow_weight_map.py) with its
output [flow_weight_map.out](flow_weight_map.out) (no engine import,
nothing run on the engine; the Algebraist's step algebra reused by
import, not copied), and one index row. Base commit
`ea3609a887650a2a303d540443944f7f23d55c54` (origin/main); the step
algebra cited is [STEP_ALGEBRA.md](../light_bending/STEP_ALGEBRA.md)
sections 9 and 10 at `23ef9ce93721963098c45e0add3f846a7154a1fb` (PR #821,
merged into main at e9798aa8; the algebraic check under the rule is
[ALGEBRA.md](ALGEBRA.md) beside this file).

Every number below is GAMEBOARD, the step algebra's simulation of the
board, never a measurement, unless marked DETECTOR (the register's own
clicks). Einstein's 4 appears on the comparison side only, never as an
input (record 817); nothing here is called derived where a form was put
in: `c_f = 2` is an input (record 826 (D)), the pin `n S = d` a
declaration (II.10a of [the Einstein derivation](../einstein_outside/DERIVATION.md)),
and the weight of this hypothesis is a declaration under its own identity.

## 0. The verdict, at the top

**ADMISSIBLE, in my own judgement before the reviewer's**, as a hypothesis
under its own identity `flow-link-v1`, off by default. The rule is one
line: the arrival flow a reader sums counts each arriving row of
direction **D** with the flow label **f**_D, the integer vector nearest
`Q` **D** `/ S_1` (the label per Euclidean Link of the line, `|`**D**`| /
S_1` Links per Node), in place of the unit label **u**_D, the integer
vector nearest `Q` **D** `/ |`**D**`|` (the label per Node). It removes
from the push exactly what the reviewer found the push carries (record
872): a digital line has `S_1 / |`**D**`|` Nodes per Euclidean Link, the
push counts one arrival per Node per interval on each line, so its shell
mean carries the fan's mean of `S_1 / |`**D**`|`, `F_L1 = 1.4355` on the
290 directions (1.421 by the shells) and `3 / 2` in the isotropic limit;
the clock's presence per Node, the dwell `T_D / (S_1 Q)` intervals, is
the inverse of that incidence up to the pace, so the clock's word carries
none. Under the rule the fan's mean of incidence times weight is `1.0000`
by identity (`1.0003` with the rounding of **f**_D at load), and the same
crowd's shell mean of the flow over r = 4 .. 14 is `22.85` against the
continuum's `q / (4 pi) = 23.08` (`0.990`; the law as built `32.79`,
`1.421`), beside the clock's `A r = 68.72` against `69.23` (`0.993`): the
two constants of gravity, the push's and the clock's, are one to three
parts in a thousand on series K's fan, both `q / (4 pi S)` at the pin
`n S = d`. The three tests pass (section 2): one table column per
direction, formed once at load by one Euclidean division with the nearest
whole (as **u**_D itself is), read by every family's flow alike; verb 3's
sum unchanged; no root, no float, no run-time division, nothing kept at a
Node, the same six reads. What moves (section 3): every push on the law,
under the key, by the fan's L1 factor; the wall's delay not at all. The
ring of starts (section 4) under the rule reads `C_ring = 3.65 / 3.82 /
3.92` at b = 6 / 3 / 8 at gamma 1 against 4 on the clock's `G M` (`1.81 /
1.90 / 1.93` against 2 at gamma 0; the ratio `2.02`, the declared `c_f`
read back), the residual `0.08 to 0.35` the finite path's `L / sqrt(L^2 +
b^2)` (0.97 to 0.96) and the shells' `0.990`, one to three grains of the
ring (`0.085 to 0.107`): **the ring reads `2 c_f` within the finite
path's factor `L / sqrt(L^2 + b^2)` and the shells' `0.990`, to one to
three grains (`3.65 / 3.82 / 3.92` against the expected `3.86 / 3.93 /
3.79`), where it read 5.1 to 5.9 as built**. The alternative not chosen, `c_f` absorbing the factor (`1 +
gamma = 4 / 3` in the limit), leaves the wall's delay off by the same
`3 / 2` and is named in section 3 (e).

What this does not do: it does not make 4 a derivation. The ring under
the rule reads the declared `2 c_f` against the clock's constant, both on
one ground now; the 2 of `c_f` stays an input of kind 2. And it is a
change of the flow's rule for every reader, not a patch on light: Newton's
rows move by the same factor (section 3 (c)), which is why it is a
hypothesis under its own identity and not a line of the law until the
owner admits it.

## 1. The rule under its own identity

### 1.1 The integers the engine already holds for a row's line

Per direction **D** = (a, b, c) of the world's table, formed once at load
and read as constants (BEAM_LAW note 41 (viii)), in
[nature_beam.py](../../../src/event_universe/events/nature_beam.py):

| Integer | Where | What |
| --- | --- | --- |
| **D** itself, `Flight.vectors` | `:745-760`, `direction_flight :847-880` | the direction as integers |
| `S_1 = |a| + |b| + |c|`, `Flight.manhattan` | `:855` (`s1 = sum(abs(c) ...)`) | the L1 length, the Nodes per period of the digital line |
| `T_D = isqrt(3 (a^2 + b^2 + c^2) Q^2)`, `Flight.resolution` | `:861` | the flight's wall per period, the one root of the table, taken at load |
| the line, `Flight.lines` | `:863-868`, `world.bresenham_line :1491` | the `S_1` unit steps of one period |
| **u**_D, `Flight.labels` | `:874`, `unit_label :824` | the integer vector nearest `Q` **D** `/ |`**D**`|`, the label of one unit per Node |
| `e_D = isqrt(3` **u**_D `.` **u**_D`)`, `Flight.energy` | `:876` | the photon's energy per unit |
| the rate `2 S_1 Q` and the wall `2 T_D`, `FamilyFlight.rate`, `.wall` | `:954, :971-972` | the flight accumulator's pair per direction |

**The dwell as the engine computes it for the age moment.** The engine
holds no integer named the dwell; the dwell is what the flight's pair
makes. A row of direction **D** at age tau has made `m(tau) = (2 tau S_1
Q + T_D) // (2 T_D)` Links (`Flight.manhattan_steps :775`, the
accumulator `:783`, `core.integer.by_drive :79`); the rows of one line
present at a Node reached at the Link `made` are the ages with `m(tau) =
made`, one arriving per interval and each staying `T_D / (S_1 Q)`
intervals in the mean (the whole part or the whole part plus one of that
ratio at every Node: `2 T_D / (2 S_1 Q)`, the wall over the rate). The
age moment `A` a reader takes (`CrowdMoments :3069`, `moment = amount x
age :3104`, summed per Node `:3117`, read less the reader's own number by
`age_moment :3136`) sums amount times age over the rows present, so each
line enters it with its presence, the dwell. The arrival flow **V**
(`label[arrived] = amount x unit_rows :3108`, summed `:3119`, read by
`arrival_flow :3145`) sums amount times **u**_D over the rows that
arrived this interval, so each line enters it with one label per Node
per interval, whatever its dwell. The push translates the row's
accumulator by it, **W** `-= n x weight x` **V** (`optical_turn :3730`,
the read `:3822`, the translation `:3842`; the weight per unit
`unit_weights :3563`); a body's push reads the same labels through the
group moment (`plan.g_moment :4800-4803`, `push_form :2932`).

### 1.2 The weight, a ratio of those integers, no root

A digital line of direction **D** advances `|`**D**`|` Euclidean Links in
`S_1` Nodes, so it has `S_1 / |`**D**`|` Nodes per Euclidean Link. The
weight that counts one arrival as one Euclidean Link of its line instead
of one Node is the inverse,

    w_D = |D| / S_1          (Links per Node of the line D)

and the label one unit carries into the flow becomes

    u_D x w_D = (Q D / |D|) x (|D| / S_1) = Q D / S_1,

the root cancelling exactly: **the flow label is** `Q` **D** `/ S_1`, a
ratio of the direction's own integers and its L1 length, no root, no
float. Its relation to the dwell: the dwell per Node is `T_D / (S_1 Q) =
(|`**D**`| / S_1) x (T_D / (Q |`**D**`|))`, the Euclidean length per Node
times the intervals per Euclidean Link `T_D / (Q |`**D**`|)`, which is
`sqrt 3` on every line to the isqrt's grain (`T_h / Q = 110 / 64` on the
heading, `1.0078` under `sqrt 3`). So `w_D` is the line's dwell in units
of the heading's dwell, `T_D / (S_1 T_h)`, and the exact form `|`**D**`| /
S_1` is that ratio with the two floors of the isqrt removed: the fan's
mean of incidence times weight is `1.0060` on the isqrt form (the
heading's floor, common to every line) and `1.0000` on the exact form
(the map's section 1). The design takes the exact form; the isqrt form
would be the same rule with a constant `0.6` per cent bias on the push's
constant.

**The one division, at load, the nearest whole (the vector verb).** `Q`
**D** `/ S_1` is not an integer vector (the heading's `(64, 0, 0)` and
the lines `(1, 1, 0)`, `(1, 1, 1)` apart). The rule declares its flow
label as the engine declares **u**_D: one Euclidean division per
component, the nearest whole,

    f_D[i] = sign(D[i]) x (2 Q |D[i]| + S_1) // (2 S_1),

formed once at load in `direction_flight` beside `labels`, one column
`flow_labels` of the same shape (directions, 3), and read by the flow as
a constant. That formula is the photon's, whose label per unit is **u**_D
of magnitude `Q`. A massive family's rows carry their own label **p**_D
of magnitude `|`**p**_D`|` (the lamp's `momentum_magnitude`,
`FamilyFlight.labels :944, :959`, `scaled_label`), and the same weight
`|`**D**`| / S_1` on it gives the flow label nearest `|`**p**_D`|` **D** `/
S_1`, not `Q` **D** `/ S_1`: so `FamilyFlight` forms its `flow_labels`
from its own labels by the same division with `|`**p**_D`|` in `Q`'s
place, `f_D[i] = sign(D[i]) x (2 |`**p**_D`| |D[i]| + S_1) // (2 S_1)`,
the photon the case `|`**p**_D`| = Q` (the reviewer's line, record 902);
else the generic test would be passed by the photon alone and the massive
rows' flow would keep the L1 factor. The map's numbers use the right
magnitude: series K's crowd is the photon family at `Q = 64` (the mass's
free rays, `u_D` at the scale `Q`), and D3's plane fan is the free
family's rays at the scale `Q` too (`|u_d| / Q = 1.0000`, the orbit
register), where only the ratio `F_plane` enters, magnitude-free. The
remainder is dropped at load as **u**_D's is the remainder is dropped at load as **u**_D's is
(`unit_label :824`, "the integer vector nearest"), a declared rounding at
load and none at run time. Per line the rounding is at most `1 / (2 Q
|`**D**`| / S_1)` on a component: the largest relative error of `|`**f**_D`|`
over the 290 directions is `0.0156` (the line `(-2, -2, -1)`, **f** =
`(-26, -26, -13)` for `(-25.6, -25.6, -12.8)`), the mean `0.0045`, the
same order as **u**_D's own `1.35` per cent (DERIVATIONS_BEAM 3.2); in the
fan's mean the roundings cancel to `1.0003`. The beam's own lines:
`(24, 1, 0)`: **f** = `(61, 3, 0)` for **u** = `(64, 3, 0)`; `(12, 1, 0)`:
`(59, 5, 0)` for `(64, 5, 0)`; the heading unchanged, `(64, 0, 0)`.

**The exact form beside it, with the remainder kept** (for the reviewer's
choice, not the design's): the push accumulator **W** and the label scale
taken in units of `1 / L`, `L` the least common multiple of `S_1` over
the world's table (`3900` on series K's table: the fan's `1 .. 6`, the
beam's `25` and `13`), so that one unit carries `Q` **D** `L / S_1`, an
integer vector, and the momentum is **P** `= L Q d content` **u**_D `+`
**W**_L; verb 3 is homogeneous in **P** (the argmin of `|`**c** `+`
**h** `x` **P**`|^2` with **c** scaled alike), `momentum_pair` takes
**P** over its gcd, and the turn's conservation `W_L += L Q d content
(u_D - u_D')` holds: the same walk, no remainder ever formed (`S_1`
divides `L`). Its price is the working bound: every product of the push
and the pair grows by `L` (`2 T(`**P**`) d` at content 1 on series K
about `1.5 x 10^16`, six hundred times under `2^63`, but `L` grows as
the fan's lcm: `27720` at Manhattan 12). The map runs both forms
(section 4): they differ by at most one Node on one line of thirty and
by `0.01` on `C_ring`. The design takes the rounded label, the exact
form is stated so that the reviewer can prefer it.

### 1.3 The cancellation in the shell mean, the arithmetic

On the fan of 290 directions (`|a| + |b| + |c| <= 6`, primitive), each
line crossing a shell of unit thickness at `S_1 / |`**D**`|` Nodes and
carrying `scale x |label|` per Node per interval, the shell mean of the
flow's magnitude over `N(r) -> 4 pi r^2` Nodes is

    <|V|> r^2 / Q = (q / (4 pi)) x mean over the fan of (S_1 / |D|) x (|label| / Q),

so the factor beside the continuum's `q / (4 pi)` is the fan's mean of
incidence times weight (the map's section 1):

| The label per arrival | mean of `(S_1 / |D|) x (|label| / Q)` over the 290 |
| --- | --- |
| **u**_D (the law as built) | `1.4355` (`F_L1`) |
| `Q` **D** `/ S_1` (the exact weight) | `1.0000` (an identity, line by line) |
| **f**_D (the flow label, rounded at load) | `1.0003` |
| **u**_D `x T_D / (S_1 T_h)` (the dwell in the heading's units) | `1.0060` |

And on the lattice itself, from the same stationary crowd of series K's
mass (M = `2^16`, 16 units per direction per interval, `q = 4640`) that
STEP_ALGEBRA.md section 9 summed, the shell means over r = 4 .. 14 (the
map's section 2; the clock's word beside them, unchanged):

| Reading | the law as built | under flow-link-v1 (**f**_D) | exact form | the continuum |
| --- | --- | --- | --- | --- |
| `|`**V**`| r^2 / Q` | `32.79` (`1.421`) | `22.85` (`0.990`) | `22.84` (`0.990`) | `q / (4 pi) = 23.08` |
| `A r` (the age moment) | `68.72` (`0.993`) | `68.72` (`0.993`) | `68.72` | `3 q / (4 pi) = 69.23` |

The `1.421` of the shells against the fan's `1.4355` is the shells'
weighting of the lines (the reviewer's two numbers, record 880); under
the rule the residual `0.990` is the shells' own ripple at r = 4 .. 14
(`21.8` to `24.7` shell by shell, the lattice's count of Nodes on a shell,
DERIVATIONS_BEAM 3.2), the same ripple the clock's word shows (`61.1` to
`77.4`). **The grain stated: the two constants agree to `0.3` per cent
on the fan's mean (`1.0003` against `1`) and to `0.3` per cent on the
lattice's shells (`0.990` against `0.993`).** In the isotropic limit the
fan's mean of `S_1 / |`**D**`|` tends to `3 / 2` and the mean of the
product to 1 exactly: the cancellation is not the fan's, it is line by
line.

### 1.4 Why this weight and not another

The reviewer named two ways to make the constants one (record 872): the
flow weighted per line by `|`**D**`| / S_1`, or `c_f` absorbing the
factor. The first is this design; the name flow-dwell-v1 the Boss offered
is kept as the physical reading (each arrival counts by its line's dwell
in the heading's units), and the identity is called flow-link-v1 because
the integer the rule writes down is the Euclidean Link per Node, `Q`
**D** `/ S_1`, with no root, and not the isqrt ratio. A third form,
weighting by the dwell `T_D / (S_1 Q)` itself, would multiply every push
by `sqrt 3` beside the cancellation (the pace's factor, `1 / c`), which
is a change of the push's constant by a known number and not what is
asked. A per-Node weight (a table by Node) fails the local test's
"nothing kept at a Node" and is refused.

## 2. The three tests, written out

1. **Generic: PASS.** One primitive, a table column per direction of the
   world's table, `flow_labels`, formed at load from the declared integers
   **D** and `S_1` by one Euclidean division, and read by every family's
   flow alike (the photon's rows at `Q`, a massive family's rows on its
   own labels `FamilyFlight.labels :944` at `|`**p**_D`|`, each family's
   `flow_labels` formed from its own labels by the one division, the free family's rays a body reads
   through `g_moment`); no family name, no kind, no branch: the engine
   reads `flow_labels` where it read `labels` in the flow's sum, and the
   rest direction's label is `(0, 0, 0)` as before. A world without the
   key has `flow_labels` equal to `labels`, byte for byte.
2. **Vector: PASS.** The flow is verb 3, the group-ring addition of
   labels over the interval's arrivals (`np.add.at :3119`), unchanged; the
   only division is verb 6 at load, `(2 |`**p**_D`| |D[i]| + S_1) // (2
   S_1)` on each family's own label magnitude (`Q` for the photon), the
   nearest whole declared at load as **u**_D's is; no root (the root of
   `|`**D**`|` cancels against **u**_D's, section 1.2), no float, no
   rounding at run time. The push's rate `n x weight x` **V** stays
   bilinear in the state (the weight a constant per direction, **V** a
   sum of constants over the arrivals).
3. **Local: PASS.** The reader reads what it reads today: its own record
   and the interval's arrivals at its own Node (LOCALITY-1; the crowd's
   moments are the Node's own sums less the reader's own number,
   `:3136-3153`), nothing at a distance and nothing kept at a Node; the
   work per row per interval is the same sum with the same count of
   terms; the storage per row is unchanged (**W**'s three integers), the
   host's table one column of three integers per direction more.

No test fails; the hypothesis needs no seventh verb and no root at a
declared grain. It is still a hypothesis under its own identity because
it changes what every push reads, which moves registered pins (section
3), and the law admits such a change on the owner's word only.

## 3. What changes and what does not

**(a) The push's constant becomes the clock's.** In the shell mean the
push a body of content M reads is `n x weight x <|`**V**`|>` with
`<|`**V**`|> = q Q / (4 pi r^2)` under the rule (no L1 factor), so
Newton's `G` from the push is `G = K (n / d) / (4 pi S)` of DERIVATIONS_BEAM
3.3 with the fan's `K / 4 pi` now the true `q / (4 pi)` and not `F_L1
q / (4 pi)`; at the pin `n S = d` it is `q / (4 pi S)`, the clock's
constant of II.10a (the age moment's `k = n A / d` with `A r = 3 q / (4
pi)`), one number. The 3.2 identity "the K beams cross a shell at K of
its Nodes" was the continuum's; on the lattice each line crosses a unit
shell at `S_1 / |`**D**`|` Nodes, and the rule is what makes 3.2's
sentence true for the flow a reader sums.

**(b) The wall's delay unchanged.** The wall reads the age moment `A`
(`optical_rate_and_wall :3602`, `age_wall integer.py:153`), which the rule
does not touch: the presence per Node, the dwell, is the flight's and
stays. The Shapiro delay `c_f (n S / d) (G M / c^3) ln(4 r_1 r_2 / b^2)`
stands as II.11 has it. On the registered in-plane worlds the click's
mean age moves only through the bent path's Links (second order): the
map's section 3 reads the delays `2.60 / 5.00` at b = 6 (registered
`2.95 / 4.94` DETECTOR, the algebra's `3.00 / 5.00` as built), `2.40 /
5.00` at b = 8 (`2.40 / 4.40`), `3.20 / 5.00` at b = 3 (`2.80 / 6.00`),
every one within the register's bracket of one interval.

**(c) The pins that would move (GAMEBOARD, by formula and by the map;
nothing moved in any register by this file).** The rule changes the push
of every reader, so every registered number that rests on the push
moves by the fan's L1 factor of its world, and every number that rests
on the wall, the clock or the flight alone does not.

| Registered pin | Where | How it moves under the key |
| --- | --- | --- |
| Series K / optical, the mass world's centroid shift `-1.993 / -3.989` pixels at gamma 0 / 1 (DETECTOR), the algebra's `-2.000 / -4.000` | `examples/events/optical/README.md :281-284`; STEP_ALGEBRA.md section 5 | the map's section 3: `-1.600 / -3.000` (the far `-1.800 / -3.400` to `-1.200 / -2.600`; the near `-2.600 / -6.400` to `-2.400 / -4.800`); the ratio gamma 1 / gamma 0 `1.88 to 2.17` on the pixels, `1.99 to 2.17` on the momentum; the in-plane comb stays (C = `11.69` at b = 6, `8.52` at 3, `13.45` at 8: the plane's failure of record 862, not the constant's) |
| The bending's coefficient, NATURE row 13 (NOT COMPARED) | `docs/NATURE.md :115` | the ring's `C_ring` against the clock's `G M`: `5.12` to `3.65` at b = 6 (section 4); the in-plane worlds' `14.71` to `11.69`, still the comb; the row stays NOT COMPARED until the ring world runs |
| Series D3, Newton after a detector: `T(12) = 343`, `T(24) = 687` within 9 per cent at n = 9 on the plane at S = 32 | `docs/EXPERIMENTS.md :7493`; `examples/events/orbit_lamp/README.md` | the plane fan's factor `F_plane = 1.2871` (120 directions, `4 / pi = 1.2732` in the limit): the circular balance `n^2 / (S + n)` divided by `F_plane` gives `n = 7.818` (the nearest whole 8), `T = 2 pi r (S + n) / n = 384 / 768` (`377 / 754` at n = 8); to be re-derived by the generator before any run |
| The same series' `T(24) / T(12) = 2.00 +- 0.18` | as above | unchanged: the ratio carries no constant |
| The same series' `omega^2 = (2 pi / T)^2` and the equivalence world | as above | `omega^2` and the fall's `g = v^2 / r` divided by `F_plane = 1.2871` (the push linear in the flow, the equivalence exact: `push_m = m x push_1` as before) |
| Series C (the plane's `1 / r`, GAMEBOARD diagnostics of the probe's register) | DERIVATIONS_BEAM 3.2 to 3.3 | `flow x 2 pi r / q = 1.00` becomes `1 / F_plane = 0.78` per Node on a fan of 120 (the Node count `N(r)` unchanged) |
| Every clock pin: the redshift ratio `2.00` (NATURE row 12), the crowd clock's `k`, the lamp's rate `0.918` at the mass world, the shell worlds' inside `1.000` and outside `1 / r` | the age moment | unchanged: the clock's word reads presence, not arrivals |
| Every pin of the flight, the collision, the amplitude, the phase | no flow read | unchanged, byte for byte |

**(d) The pins that would not move at all** are every world without the
key (the key absent, `flow_labels` equal to `labels`), and every reading
of the clock's word with or without the key.

**(e) The alternative not chosen: `c_f` absorbing the factor.** The
push's weight `(1 + gamma) e_D` could be declared `(1 + gamma) e_D /
F_L1`, `1 + gamma = 4 / 3` in the isotropic limit for nature's 2. Then
the ring's `C` against the clock's `G M` reads 4 on that fan, but the
wall carries the same `c_f` on the flight (`age_wall_set`, the flight a
member at `1 + gamma`) and its delay would read `2 / (3 / 2) = 4 / 3` of
Shapiro's coefficient, off by `3 / 2` (record 872, record 878 (4)); and
the factor is the fan's, `1.4355` at Manhattan 6 and `3 / 2` in the
limit, so `c_f` would be a number per fan, not a constant of the world.
Refused here for that reason; named as the reviewer asked.

## 4. The ring world on this rule

**The construction** is STEP_ALGEBRA.md section 9's, unchanged: the
registered box, fan of 290, mass `2^16`, pair `[1, 16384]` with the width
`16384` declared (the pin), one row of light on the heading from every
Node of the lamp's plane x = 2 at `|sqrt(y^2 + z^2) - b| <= 1 / 2` about
the mass's line (16 starts at b = 3, 40 at 6, 48 at 8), the screen x = 54
of one-Node `wave` detectors reading `age`, every Node of it a detector.
Under the key `flow_link` (section 6) the push reads **f**_D. The map's
section 4 walks every start under the three forms (the law as built, the
flow label, the exact form). The step algebra's simulation of the board,
not a run:

| b | starts | gamma | `C_ring` as built (record 878) | `C_ring` under flow-link-v1, against 4 | exact form | the mean radial shift of the arrival Node, Links (the pin) | the mean delay | the grain on `C_ring` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 16 | 0 | 2.605 | **1.901** (against 2) | 1.891 | `0.845` (as built 0.996) | 0.62 | 0.107 |
| 3 | 16 | 1 | 5.442 | **3.821** | 3.822 | `1.625` (2.091) | 1.31 | 0.107 |
| 6 | 40 | 0 | 2.599 | **1.805** (against 2) | 1.795 | `0.128` (0.451) | 0.40 | 0.085 |
| 6 | 40 | 1 | 5.116 | **3.652** | 3.644 | `0.731` (0.974) | 0.78 | 0.085 |
| 8 | 48 | 0 | 2.905 | **1.932** (against 2) | 1.929 | `0.107` (0.409) | 0.27 | 0.095 |
| 8 | 48 | 1 | 5.859 | **3.918** | 3.914 | `0.628` (0.854) | 0.98 | 0.095 |

The tangential mean is `0.00000` at every ring (the fan's symmetry, as
before). The ratio gamma 1 / gamma 0 of the ring's mean is `2.01 / 2.02 /
2.03` at b = 3 / 6 / 8: the declared `c_f = 2` read back, RECOVERED, not
derived.

**Read against the pins.** (i) On the clock's `G M = q / (4 pi S)`, the
one constant now, the ring reads `2 c_f` within the finite path's factor
`L / sqrt(L^2 + b^2)` and the shells' `0.990`, to one to three grains:
`3.65 / 3.82 / 3.92` against the expected `3.86 / 3.93 / 3.79` at b = 6 /
3 / 8 at gamma 1 (bare against 4: 8.7, 4.5 and 2.0 per cent below),
`1.81 / 1.90 / 1.93` against `1.93 / 1.97 / 1.89` at gamma 0, where it
read `5.1 to 5.9` and `2.6 to 2.9` as built. (ii) The residual below 4 is
accounted for and not free: the finite path from x = -26 to +26 sums
`L / sqrt(L^2 + b^2)` of the continuum's transverse impulse (`0.993 /
0.974 / 0.956` at b = 3 / 6 / 8) and the shells' `0.990`, so the expected
`4 x 0.990 x (0.993, 0.974, 0.956) = 3.93 / 3.86 / 3.79` against the read
`3.82 / 3.65 / 3.92`: within `0.11 / 0.21 / 0.13`, one to three grains
(`0.107 / 0.085 / 0.095`), and the dwell's `1 + c_f k` (upward, `k =
0.02 to 0.05`) inside the same margin. (iii) If the cancellation were
exact and the path infinite the number would be `2 c_f = 4` by
construction: the ring on this rule tests that the two constants are one
(the reading the law as built refutes at `5.12`), not that 4 is derived.

**What a detector at the screen clicks, and the comparison on the Nodes'
own conversion (record 872 (e)).** A `wave` pixel clicks a row's arrival
Node and its age (DETECTOR). Per start the reading is the arrival Node's
radial shift toward the mass's line, `-(dy y + dz z) / r` in Links, and
the click's age less the control's; the ring's mean over its starts is
the measurement. The momentum's `tan alpha` is GAMEBOARD and is not what
a run compares. The Nodes' own conversion is `C_nodes = (mean radial
shift / 26) x b x 4 pi S / (3 q)`, `4 pi S / (3 q) = 14.79` at this M
and pin, which carries the lever arm's factor the algebra states before
the run: the bend is spread from x = -26 to +26 and the part made after
the mass reaches the screen with less than 26 Links of arm, so
`C_nodes / C_ring = 0.65 to 0.73` on every form (as built `3.32 / 5.12`
at b = 6, record 878). Under the rule, from the table: `C_nodes = 2.50 /
2.77 / 2.86` at b = 6 / 3 / 8 at gamma 1, the expected click readings.
So the pins of the ring world under the key, DETECTOR when run, from this
section before any run: at b = 6 the ring's mean radial shift `0.731 +-
0.025` Links at gamma 1 (one Node per start over 40 starts) and `0.128 +-
0.025` at gamma 0; the per-start arrival Nodes `(dy, dz)` listed in the
.out's section 4 (at b = 6, gamma 1: `(-6, 0)`, `(6, 0)` and `(0, 6)` shift by 3
Nodes, `(-4, 4)` and `(4, 4)` by one Node on each axis, 20 starts by 1,
15 by 0); the mean delay `0.78`
and `0.40` intervals within 1; the tangential mean 0 within a Node; the
ratio of the two radial means `5.7` on the Nodes (the gamma 0 reading at
the grain: 5 starts of 40 move one Node, so the Nodes' ratio is not a
pin, the momentum's `2.02` is GAMEBOARD); at b = 8 `0.628` and `0.107`
over 48 starts; at b = 3 `1.625` and `0.845` over 16. **The comparison a
run makes**: the mean radial shift against `0.731 +- 0.025` (the rule
in the run; `0.974` refutes it as the law as built); `C_nodes` against
the algebra's `2.50`, and through the stated lever-arm factor `C_ring`
against 4 within the ring's grain and the finite path's factor; the
control worlds byte identical to the register; the delay within its
bracket. What refutes the hypothesis: a ring reading whose `C_ring`,
corrected by the stated factors, leaves `2 c_f` by more than the grain
in either direction; or any clock reading (the lamp's rate, the redshift
ratio) that moves under the key. The gamma 0 Nodes are at the grain at
M = `2^16`; a run that wants the gamma 0 pin off the grain doubles M
(`2^17`, the shifts doubling, the algebra to re-pin it first), which is
not proposed here.

## 5. The cost

**Local, per Node, for fixed K: unchanged.** The push's read is the same
sum over the interval's arrivals at the row's Node with the same count
of terms (one label per arriving row), the same translation of **W**,
the same label and pair; the age moment's read unchanged. Storage per
row unchanged: **W**'s three integers, **c**'s three, the residue, as
today; nothing kept at a Node. Under the exact form (section 1.2) the
storage is the same three integers, the working bound's headroom on
them divided by `L`.

**The host's, separately.** One column of three integers per direction
of the world's table (`flow_labels`, 296 rows on series K), computed once
at load by one integer division per component; the readings tools'
conversions unchanged. The ring world's run is series K's box with 40
lamps (b = 6) for 400 intervals, about the mass world's cost times the
lamps' rows (STEP_ALGEBRA.md section 11), the host's estimate to be
made by the runner before the run.

## 6. The key, the world files, and the row for the hypothesis list

**The key.** The world key `flow_link` (a boolean; absent by default;
`world.py`'s key list `:406-416`, parsed as `optical` is `:3978`), the
identity `flow-link-v1` beside `OPTICAL_RULE` (`world.py :646`). With the
key `true`, `direction_flight` fills `flow_labels` with **f**_D and the
flow's sums (`CrowdMoments :3108`, `g_moment :4800`) read it; absent,
`flow_labels` is `labels` and every world reads as it did, byte for byte
(the test of every identity). Refused at load with a table whose `S_1`
is 0 on a moving direction (none exists) and, under the exact form only,
with `L` such that `2 T(`**P**`) d` at the largest content leaves the
working bound (tested by division before the product, as the pair is).
It stands alone: a world may declare it without `optical` (a body's push
under the law's own coupling then reads **f**_D), and with `optical:
gamma` for light.

**The world files that would declare it** (none written here): the ring
world of section 4, series K's box with the ring of lamps under `optical:
1` and `optical: 0`, `flow_link: true`, `width: 16384`, `suspension: [1,
16384]`, generated beside `examples/events/lensing/make_worlds.py` with
its pins from this file's section 4 and the .out; the registered
`optical/mass_g0.json` and `mass_g1.json` under the key as the calibration
of the build (the map's section 3: `-1.600 / -3.000` on the algebra); and,
if the owner wants Newton's rows on the one constant, series D3's
`orbit_lamp` worlds with the key and re-derived pins (`384 / 768`).
The registered worlds themselves are not changed.

**One row for [the hypothesis list](../../HYPOTHESES.md)** (proposed, not
added; it enters when the design is gated):

> **29. flow-link-v1: one arrival counts one Euclidean Link of its line,
> not one Node; the law's two constants of gravity are one, stated so
> that it can fail.** Under the world key `flow_link` (absent by default)
> the arrival flow every reader sums carries per arriving row the flow
> label **f**_D, the integer vector nearest `Q` **D** `/ S_1`, in place of
> the unit label **u**_D; the push's shell mean then carries no L1 factor
> (the fan's mean of `S_1 / |`**D**`|`, 1.4355 on 290 directions, 3 / 2 in
> the limit) and the push's Newton constant equals the clock's, `q / (4 pi
> S)` at the pin `n S = d`, to three parts in a thousand on series K's fan
> ([the design](DESIGN.md) (from HYPOTHESES.md: `designs/flow_weight/DESIGN.md`)). The expectation, before any
> run: the ring of starts at b = 6 under `optical: 1` reads the mean radial
> shift of the arrival Node `0.731 +- 0.025` Links over 40 starts (`0.974`
> as built) and `C_ring = 3.65` against 4 on the clock's constant within
> the ring's grain and the finite path's factor. What would refute it: a
> ring reading that leaves `2 c_f` by more than the grain after the
> stated factors, in either direction; any reading of a clock that moves
> under the key; a world without the key that differs from main's by a
> byte. Status: a design of 2026-09-22, no build, no run, the key off.

## 7. Links

- [flow_weight_map.py](flow_weight_map.py), [flow_weight_map.out](flow_weight_map.out): the arithmetic of this file (no engine import; the Algebraist's [step_algebra_map.py](../light_bending/step_algebra_map.py) imported, its `walk`, `Table`, `Crowd` and `ring_starts` reused).
- [ALGEBRA.md](ALGEBRA.md): the algebraic check under the rule, in the Algebraist's manner (the owner's word of record 888).
- [STEP_ALGEBRA.md](../light_bending/STEP_ALGEBRA.md) sections 9 and 10 at `23ef9ce9` (PR #821): the ring, `F_L1`, the two constants, the question.
- [one_wall/NOTE.md](../one_wall/NOTE.md) section 5: the one constant, `32.79` against `23.08`.
- [einstein_outside/DERIVATION.md](../einstein_outside/DERIVATION.md) II.10a and II.11: the pin `n S = d`, the bending and the delay under the key.
- [DERIVATIONS_BEAM.md](../../DERIVATIONS_BEAM.md) 3.2 and 3.3: the shell mean and G's place.
- [BEAM_LAW.md](../../BEAM_LAW.md), [ENGINE.md](../../ENGINE.md): the flight, the wall, the push.
- [the log](../../LOG_2026-09-20.md) records 817, 855, 862, 872, 878, 880, 884.
- [HIGHLIGHTS.md](../../HIGHLIGHTS.md) 5.4: the three tests (2026-09-21), the measurement rule, gamma an input of kind 2, the algebra first, record 817's line; kept, none asked to change.
