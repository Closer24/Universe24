# One wall for every accumulator, and the push on a row with its energy as the weight: the generic rule for light beside a mass, `one-wall-v1` (the physicist, read-only, 2026-09-21)

The Boss's order of 2026-09-21 (about 15:24Z) on the owner's word ("close
one wall"): the design note for issue #605, the previous physicist's
statement of the owner's question "why is the light not coupled to the
clock; when a clock slows it should bend the light" and of the law's
structure "it does not ask; the clock simply slows". Read against `main`
at a29709d (PRs #602, #603, #606 and #608 merged: the clock's word the
age word, record 394; `optical-v1` designed and given the go, not built;
the light-bending and the Lorentz notes of the open problems). Every
number is from [one_wall_map.py](one_wall_map.py) beside this note
(integers; the flight rule, the unit label and the Bresenham order
transcribed from BEAM_LAW section 3 as the light-bending map transcribed
them; the push transcribed from step 4; no engine import) and its output
[one_wall_map.out](one_wall_map.out). No run, nothing registered, nothing
decided. Notation as the workflow's rule: a scalar plain, a vector in
bold lowercase, every symbol named at its first use.

## 0. The verdict, stated at the top

**ADMISSIBLE WITH CORRECTIONS** as a hypothesis under its own identity,
`one-wall-v1`, a world key off by default. It passes the three tests
(section 3). The corrections (section 8): the two halves of issue #605 do
not add. The wall's half and the push's half are one deflection, Newton's
`2 G M / (b c^2)` (Soldner 1801, Einstein 1911), read twice: the push
bends the row and the wall tilts its wavefront by the same angle, so that
the row rides its own front; the sum `4 G M / (b c^2)` is a double count
(section 5). The rule is the TIME PART of the weak-field metric on the
GameBoard, complete and generic: the redshift, the delay at half
Shapiro's coefficient, Newton's deflection for rows, the drive of a body
slowed in the potential; its post-Newtonian gamma (the space part over
the time part) is 0 in the deflection and 0 in the delay, consistently,
where nature reads 1 to `10^-4` (VLBI) and `10^-5` (Cassini). The space
part is no verb's (the light-bending note's finding stands: no rule of
the six lengthens a Link); it enters only as a declared integer on the
wall (`optical-v1`'s f = 2, an input) and this rule declares none. What
the rule adds beyond `optical-v1` at f = 1 is the ONE constant: the
clock's k and Newton's G tied by the world's pair (section 4), and a turn
that is the body's own push, no second constant.

## 1. The rule in its generic vector form (the workflow's ask, record 177)

The state at a Node is a multiset of records; every rule of the law is
one of the six verbs on it. The crowd of a record is the one reading set
of BEAM_LAW note 47: the rows present at its Node of every number but
its own, read as the moments of their labels and ages (a body's clock and
push read it today; a row reads nothing).

- **Verb 1, one wall.** Every count of the law is the translation of an
  accumulator by a rate against a wall with the remainder kept,
  `by_drive(acc, rate, wall)`. The crowd at a Node stretches the wall of
  EVERY accumulator there by one factor, the same for a body's
  self-creation clock (today's owed count), a body's drive, a lamp's rate
  and a row's flight: `wall x (d + a_tau n)` against `rate x d`, with
  a_tau (the age moment) the crowd's `sum amount x age` and `[n, d]` the
  world's suspension pair. A row is a body of no content: one line of
  the walk serves both. The invariance kept: the bijection of the
  interval (a stretched wall is a wall; the residue stays on the
  record).
- **Verb 2, the push with the energy as the weight.** The push is the
  bilinear form of step 4, `kappa(A, B) x weight_A x` **V**`_B`, **V**
  the crowd's label flow at the Node, kappa the declared column sum
  (gravity `-1`). Today the weight is the reader's content M. Under the
  rule the weight is the reader's energy in the law's value form, `E' =
  isqrt(E'_0^2 + 3` **p** `.` **p**`)` (the massive rows' wall,
  DERIVATIONS_BEAM 23; covariant readings 17.6 M3), over the scale
  `Q S`: for a body at rest `E'_0 = Q S M` and the weight is M, today's
  integer; for a row of light `E'_0 = 0` and **p** its label per unit,
  `content x` **u**`_D`, so `E' = content x e_D` with `e_D = isqrt(3`
  **u**`_D .` **u**`_D)` a table of the direction (110 on a heading, the
  flight's `T_D` by value: the photon's energy is `T_D` per unit of
  content). So a ray is pushed toward a mass as a body is, in the same
  form, and rays of every content bend alike (the weight and the
  momentum both scale with the content).
- **Verb 3, the row's turn.** The push accumulates on the row in a
  vector accumulator **w** (three integers, the meeting's phase register
  made a vector). The row's whole momentum is **P** `= Q S content`
  **u**`_D +` **w**; when the fan direction nearest **P** is not D, the
  direction label moves to it (the permutation on the declared fan, the
  meeting's own verb, the nearest chosen by comparisons of integer
  products `(`**P**` . D)^2 |D'|^2` against `(`**P**` . D')^2 |D|^2`,
  `|D|^2` whole) and **w** keeps the remainder `Q S content (`**u**`_D -`
  **u**`_D')`, so that **P** is conserved across the turn. The invariance
  kept: the row's momentum, on its label and its accumulator together.

No root and no float at run time (`e_D` at load, as `T_D`), no branch on
a family (the special case, a row, is the value `E'_0 = 0`), nothing kept
at a Node, fixed work per row. The push on a row's own direction (the
longitudinal part of **V**) moves **w** along **u**`_D` and back: a row
falling in and climbing out returns it, the redshift of light in the
record's phase being the wall's (the time in flight), not the label's.

## 2. The integer form, per dimension and per world

With Q = 64 the label's scale, S the world's `width`, `S_1` the
direction's Manhattan length, `T_D = isqrt(3 |D|^2 Q^2)` its resolution,
A the age moment of the other numbers' rows at the Node (whole), **V**
their arrival flow (`sum amount x` **u**`_d` over the crossing rule's
set), `[n, d]` the suspension pair:

    the row's flight:   acc += 2 S_1 Q d;  a Link when acc >= 2 T_D (d + n A), the wall subtracted, the residue kept
                        (the pace c_h / (1 + n A / d); the accumulator a field of the row with its residue)
    the body's clock:   by_drive(acc_owed, A n, d)                    (today's integers, record 394)
    the body's drive:   the same factor on the drive's wall Q S M + |p| under form B (optical-v1 section 7)
    the push on a row:  w -= content x e_D x V             per interval (gravity's kappa = -1; the columns' signs as step 4 has them)
    the row's turn:     P = Q S content u_D + w;  D' = the fan's nearest to P;  if D' != D: label -> D',  w += Q S content (u_D - u_D')
    the exact phase:    phi = floor(n (age r - s) / (d r)) mod N        (optical-v1's must-fix 4: the click reads the stored accumulator)

The bounds, tested by division before the product and refused naming the
Node, as the meeting's (note 35 (iv)): `2 T_D (d + n A)` and `2 S_1 Q d`
within the register (A at the fullest Node of the register is of order
`10^4` at `d = 1`); `content x e_D x |V|` per interval (the pin world's
`|V|` at b of order `10^3` label units, `e_D` 110, the content `2^9`:
`6 x 10^7` per interval, `10^10` over a path); `Q S content |u|` within
`2^62 - 1` (S up to `2^40` at content `2^9`). The nearest of the fan:
the fan's neighbours of D (4 to 6 per direction on the sphere, the
Farey neighbours on a plane, the neighbour table `optical-v1` lists at
load), stepped while a neighbour is nearer: fixed work, at most the
fan's diameter in steps, one in practice.

**The key and the refusals.** `one_wall: true`, absent by default; every
world without the key byte identical in `events.jsonl` and `state.json`
(the meeting's precedent, note 35 (viii); the gate set of
`examples/events/gate_set.json` read at its caps, the three digests of
`test_massive_rows` (a)). Refused: the key with `suspension` 0 (the push
would act on the rows while the wall did nothing: two constants where
the rule has one, section 4); the key with `meeting` or with `optical`
(two turns on one row); a wall, a push or a momentum beyond the register.

## 3. The three tests, one line each; LOCALITY-1; the measurement rule

- **Generic:** three primitives already in the law (a wall read from a
  count, the bilinear push, the permutation on the fan) with declared
  integers (`[n, d]`, S, `e_D` and the neighbour table at load), one
  path for a body and a row, the row the value `E'_0 = 0`. Pass.
- **Vector:** verb 1 a translation with a state-read wall (the growing
  wall's form, 15.6); verb 2 a translation of a vector accumulator at a
  rate bilinear in the state (the flow times the energy); verb 3 a
  comparison and a permutation with the remainder kept; no root, no
  float, no rounding at run time beyond `e_D` at load. Pass.
- **Local:** a row reads its own record and the moments of its own Node
  (the rows present there, the arrivals of LOCALITY-1's six neighbours),
  zero hops; nothing kept at a Node; fixed work per row for fixed K
  (section 7). Pass.

**LOCALITY-1** holds as for the clock: the reading set is the Node's own
rows less the reader's number. **The measurement rule** (record 281):
every number below is labelled DETECTOR (a click's pixel or age, a
record's phase) or GAMEBOARD (a row's state, a shell mean, a count of
operations); only DETECTOR numbers are pinned or compared with nature.

## 4. The one constant: the clock's k and Newton's G (the map's section A)

The push gives a body the acceleration `|`**V**`| / (Q S)` Links per
interval squared (`p += -M V`, the drive one Link per `(Q S M + |p|) /
|p|` self-creations), and the continuum's flow of one source is `|`**V**`|
= q Q / (4 pi r^2)` (q the rows released per interval), so Newton's `G M`
on the GameBoard is `q / (4 pi S)` and `G M / (r c^2) = 3 q / (4 pi S r)`
with `c^2 = 1 / 3`. The clock's count is `k_a = (n / d) A` with `A = 3 q /
(4 pi r)` (DERIVATIONS 5.1, the dwell `1 / c`). So

    k_a / (G M / (r c^2)) = n S / d :

the clock's constant and Newton's are ONE number exactly when the world
declares `n S = d`, the pair `[1, S]`. Series E's `scalar` world at `[1,
1]` and `S = 1` is that world; its `age` world at `[1, 2]` declares the
clock's G half of Newton's. This is the condition nature's one G puts on
the declaration, and it is not free: under this rule a world whose pair
is not `[1, S]` has a ray whose front tilts by one angle and whose path
bends by another (section 5), two deflections for two detectors.

**The lattice constant** (GAMEBOARD, the shell means of the map over `r =
4 .. 14`): the age moment is isotropic, `A r = 68.72` against the
continuum's `3 q / (4 pi) = 69.23` (a line dwells `T_D / (|D| Q) = 1 / c`
per Euclidean Link on every direction), while the flow a Node reads
counts one arrival per line per interval at `S_1 / |D|` Nodes per
Euclidean Link, the fan's L1 factor: `|`**V**`| r^2 / Q = 32.79` against
`23.08`, 1.42. So at `[1, S]` the clock's constant is 0.70 of the push's
on the lattice at this fan (1.00 in the continuum; the factor is the
fan's, the orbit note's Manhattan factor again), and the pin of section
6 carries it.

## 5. The pins before the numbers: whether the two halves add (the map's sections B and C)

**The claim to test** (issue #605): the wall alone gives `2 G M / (b
c^2)`, the push on the row's energy gives `2 G M / (b c^2)`, the sum `4 G
M / (b c^2)`.

**The derivation.** A row of light beside a mass under the rule does two
things. Its pace falls to `c / (1 + k_a)` where the crowd is dense, so it
arrives late by `(1 / c) integral of k_a dl` along its line: with `k_a =
G M / (r c^2)` at `n S = d`, `(G M / c^3) ln(4 r_1 r_2 / b^2)`, half of
Shapiro's coefficient (Shapiro's is `(1 + gamma) G M / c^3`, gamma = 1).
And its direction turns by the push, per interval `e_D |`**V**`_perp| /
(Q^2 S)` radians (**w** gains `e_D` **V**, **P**'s base is `Q S` **u**
with `|`**u**`| = Q`), which in the continuum is `|`**V**`_perp| / (Q S
c)` per interval (`e_D / Q = sqrt 3 = 1 / c`): the particle at c in
Newton's field, `theta = 2 G M / (b c^2)` toward the mass.

Now the front. Rows arriving at the screen at neighbouring pixels differ
in phase by the difference of their travel times; the geometric length of
a path bent by theta at the mass exceeds the straight one by `theta^2 L /
4`, second order, so the phase gradient across the screen is the wall's
delay gradient alone: `d / db` of `(G M / c^3) ln(4 L^2 / b^2)` is `-2 G
M / (c^3 b)`, and the front's tilt is `2 G M / (b c^2)` toward the mass,
whatever the push did. At `n S = d` that is the push's angle: the rows
ride their own wavefront, as Fermat's rays do in a medium of index `1 +
k_a`. The push is the mechanism OF the wall's turn (a row on a digital
line does not turn by its wall; the light-bending note's section 2), not
a second turn. **The two halves do not add: they are one deflection,
Newton's, read by a pixel detector as the click's centroid (the push) and
by a phase detector as the front's tilt (the wall); at a pair other than
`[1, S]` the two readings are two numbers, never their sum.**

**The pins** (DETECTOR if run; the crowd of one unit per direction per
interval on series K's fan of 290, the beam on the heading in the mass's
plane, the lamp 26 Links before the mass and the screen 26 after; the
control the same world without the key; every number the lattice's own
from the map's offline flight, interval by interval under the rule):

| S | pair | b | the click's pixel, control (DETECTOR) | the pixel under the rule | the age at the click, control | under the rule | the continuum's bend, tilt, delay | refutes if |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [1, 1] | 6 | 6 | captured (the push turns it 10 times; the wall alone stalls it beyond 400 intervals) | 89 | no arrival | 600 Links, 585, 521 intervals | series K's own words: nature would capture the beam |
| 256 | [1, 256] | 6 | 6 | 0 (the bend 6 Links toward the mass; the push alone 8) | 89 | 99 (the delay 10) | 2.34, 2.28, 2.04 | the pixel outside 0 +- 2, the age outside 99 +- 2 |
| 256 | [1, 256] | 3 | 3 | -4 (the bend 7; the push alone 6) | 89 | 97 (the delay 8) | 4.69, 4.66, 2.68 | the pixel outside -4 +- 2, the age outside 97 +- 2 |
| 1024 | [1, 1024] | 6 | 6 | 6 (no turn: below one fan step) | 89 | 92 | 0.59, 0.57, 0.51 | a turn |
| 256 | [1, 4096] | 6 | 6 | -1 (the push's bend; the wall's tilt 0.14) | 89 | 92 | 2.34, 0.14, 0.13 | the pair not [1, S]: two numbers, a control of section 4 |

What the lattice does that the continuum does not (the light-bending
note's section 4, confirmed here): in the mass's plane the row reads the
comb of the 48 in-plane lines, its bend 3 to 4 times the isotropic sum
(6 to 8 Links against 2.3 at b = 6) and its delay 5 times (10 intervals
against 2.0), nearly the same at b = 3 as at 6 where the continuum
doubles; and the delay's difference between the rows at b and b + 1 is
not a gradient at this fan (10 against 7 intervals at b = 6, 9 against
12 at b = 3: the sign flips), so the front's tilt cannot be read by
neighbouring rows at P = 6 and needs the dense fan (`P >> r`) or a shell
mean. The pin for a run is the two DETECTOR readings above, the click's
pixel and the click's age, with the brackets of two pixels and two
intervals (one fan step of 2.4 degrees is one Link at 26; the wall moves
the timing of the turns and the path by a pixel: the map's push-alone
against both). The `1 / b` form and the equality of the two halves are
not readable at this fan; a fan of P = 12 or a beam one Node off the
plane would read them, a second pin.

**The Shapiro delay's form.** Under the rule the delay is the wall's
alone, `(1 / c) integral of k_a dl = (G M / c^3) ln(4 r_1 r_2 / b^2)`: the
logarithm of the potential, Shapiro's form, at half his coefficient
(gamma = 0). The push adds nothing to it (the bent path's length is second
order). On the lattice the delay is `(n / d) sum of A` over the intervals
the row dwells, 10 intervals at `[1, 256]`, b = 6 (2834 per unit of n /
d at b = 6, 2202 at b = 3: the plane's comb, the map's section B), and
the ratio of the delays at b = 3 and 6 is 0.8 where the logarithm gives
1.3: the comb, not the form. The form is the continuum's, the lattice
reads the lines.

**The Sun** (the map's section D): `k = G M / (R c^2) = 2.12 x 10^-6`; the
rule's bending `2 k = 0.876` arcsec against nature's `4 k = 1.751`
(Dyson, Eddington and Davidson 1920: 1.98 +- 0.16 and 1.61 +- 0.40; VLBI
gamma = 0.99992 +- 0.00012); the rule's delay half Shapiro's (Cassini
2003: gamma - 1 = (2.1 +- 2.3) x 10^-5). Both FAIL by the factor 2,
consistently: PPN gamma = 0.

## 6. What moves in the register if the key is on (a named list, no run)

- **With the key off, nothing**: every registered world byte identical in
  `events.jsonl` and `state.json`; the gate set's three digests at its
  caps unchanged (the gate test, `test_massive_rows` (a)); `run.json`
  gains the key.
- **The clocks unchanged**: verb 1 on a body's clock is today's owed
  count, `by_drive(acc_owed, A n, d)`, integer for integer (record 394,
  `clock-age-v1`); series E's pair (`k_s r^2 = 41.5`, `k_a r = 36.1`),
  series T, U and V read as they do, key or no key, because their lamps
  and probes hold no rows that another number's crowd would slow; series
  E's 6985 sources DO release rows that read one another's crowds, so
  series E under the key would move (its rows' pace `1 / (1 + k)` at k =
  2 to 9, the timing and the local density; Gauss's law exact in the
  steady state), unchanged without it.
- **Series C's beam beside a mass**: series C is one source and its
  probes; the source's rows read no crowd of another number (the probes
  release nothing), so its field pair and "a beam does not dilute" stand
  with or without the key. What the key changes is a beam of ANOTHER
  number beside a mass: it slows and turns (series K's case), and a beam
  no longer keeps series C's "no dilution" where it crosses another
  number's crowd, which is the rule's point.
- **Series K**: its four worlds declare `suspension` 0, so the key is
  refused there (section 2); the re-run is the pin world of section 5
  (`width` 256, the pair `[1, 256]`, the mass `2^12`, b = 6 and 3, the
  screen's `age` reading as today), four worlds with their controls,
  seconds each. K under the meeting is unchanged (its key is another).
- **A body in motion** (form B's drive, `optical-v1` section 7): its pace
  in Nodes per interval falls by `1 / (1 + k_a)` in the potential, a
  post-Newtonian term; the orbit series would move by it under the key
  only.
- **Two lamps' beams read each other** (`lens_meeting`, `hubble_stars`
  if the key were declared there, as `optical-v1` section 7 lists);
  nothing on `main` declares it.

## 7. The host price, as a count per interval (the map's section D)

On series K's `mass` world (13618 crowd rows and 447 beam rows per
interval, BEAM_LAW note 35 (vii)): the reading of A and **V** at every
Node with a row, five columns of the moment table, about 12 operations
per row read, `168 780` per interval, shared by every row and body at the
Node (a second consumer of the reading the bodies take today); per row
the wall 2, the push 6, the nearest of the fan's neighbours 2 x 6, a turn
3, about 23 per row, `323 495`; against today's walk of 16 per row,
`225 040`: about 3.2 times the walk's count, linear in the rows, nothing
that grows with the GameBoard or the families. Store per row: the
position accumulator with its residue and the three of **w**, four
integers; at the Node nothing. The host's segmented sums are reported
apart from the count (the meeting's 4.6 ms per interval on `mass`, note
35 (vii), the reference).

## 8. The corrections, and what must be added if the hypothesis is built

1. **The sum is withdrawn.** The two halves are one deflection, Newton's
   `2 G M / (b c^2)`, gamma = 0 (section 5); the paper's bending row
   states the rule's 0.876 arcsec and the delay's half coefficient as
   FAIL by the factor 2, both.
2. **The energy is `E'`, not the label's magnitude.** Issue #605's
   "content x Q per unit" is `E' / sqrt 3`; the weight that gives Newton's
   half exactly is `E' = isqrt(3 p . p) = content x e_D` with `e_D` at
   load (the law's `c^2 = [1, 3]`, the massive rows' own wall at `E'_0 =
   0`), and for a body `E'_0 / (Q S) = M`, today's push.
3. **The one constant.** The clock's k and Newton's G are one number at
   the pair `[1, S]` only (section 4); the world's pair is the
   declaration of nature's one G, and a pin world declares it so; the
   lattice reads 0.70 of it at this fan (the L1 factor).
4. **The pins from the lattice's lines** (section 5's table), not the
   continuum; the front's tilt and the `1 / b` form are not readable at
   P = 6.
5. **The refusals** of section 2, the key with `suspension` 0 first.
6. **What the build adds**: the key's parser; `e_D` and the neighbour
   table at load (listed with `T_D` and `u_d` in LAW.md section 6); the
   row's four fields; the Node's reading before step 1 at every Node with
   a row (`optical-v1`'s step of the interval, one interval retarded as a
   body's push is); the wall in `Flight.walk_step` and `FamilyFlight`
   alike (one line for both); the push and the turn at the meeting's
   call site; the click's exact phase reading the stored accumulator; the
   `turned` line of the books; the gate test on the 85-world set and the
   gate set's digests; `tests/test_one_wall.py` (a) the wall on a lone
   row against `by_drive` by hand, (b) the push and the turn of one row
   at one Node against the map's flight, (c) `P` conserved across a turn,
   (d) the refusals, (e) byte identity without the key.
7. **What it is, named honestly**: the time part of the weak-field
   metric as the law's own statement, with nature's rows 12 (the clock,
   PASS at first order), 13 (the bending, FAIL by 2) and the delay (FAIL
   by 2) under one identity; the space part remains an input
   (`optical-v1`'s f) or a verb nobody has.

## 9. Questions for the owner, through the Boss, stated on the GameBoard first

1. **On the GameBoard**: under this rule the crowd enters a row twice, as
   its wall (the pace) and as its push (the direction), and the two are
   one turn at the pair `[1, S]`. Is the owner's intent the rule as one
   wall with the push as its turn (gamma = 0, the law's own number, the
   bending row a FAIL by the factor 2), or the wall read twice by a row
   (`optical-v1`'s declared f = 2, an input, the bending row a PASS by
   declaration)? The physics does not decide; nature reads the second.
2. **On the pair**: the rule makes the world's suspension pair the
   declaration of one G (`n S = d`). Does the register's convention move
   to `[1, S]` for every world with a crowd (series E's `scalar` is
   there; its `age` world, U and V are not), or does the pair stay free
   with two constants named in each world?
3. **The run**: the pin world of section 5 (four worlds of series K's
   size, seconds each) once the build lands; not needed for this note's
   verdict, needed for the register's row.

## 10. Links

[BEAM_LAW section 3](../../BEAM_LAW.md#3-the-nodes-interval-nature_beam)
(the flight rule, step 4's push, the meeting) and
[note 47](../../BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
[DERIVATIONS_BEAM 5.1 to 5.4](../../DERIVATIONS_BEAM.md#5-general-relativity-the-equation-of-the-delay-field),
[21.4 row E13](../../DERIVATIONS_BEAM.md#214-the-einstein-map-every-result-of-the-special-and-the-general-theory-its-status-today-what-the-six-give-what-must-be-added-the-pin)
and 23 (the massive rows' `E'`);
[the optical-v1 design](../gr_rows/DESIGN.md) and its
[second review](../gr_rows/REVIEW_ROUND2.md);
[the clock's word](../clock_age/NOTE.md);
[the light-bending note](../open_problems/light_bending/NOTE.md) and
[the Lorentz note](../open_problems/lorentz/NOTE.md);
[EXPERIMENTS K](../../EXPERIMENTS.md#k-light-beside-a-mass-2026-09-20)
and [K under the meeting](../../EXPERIMENTS.md#k-under-the-meeting-2026-09-20);
[issue #605](https://github.com/Closer24/Universe24/issues/605);
[the three tests](../../../skills/workflow.md#the-three-tests-of-every-rule-generic-vector-local-the-model-owner-2026-09-21-record-202).
