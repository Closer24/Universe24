# Every family under one wall: the composition of optical-v1 with the massive rows (the chief physicist, 2026-09-22)

The model owner's word of 2026-09-22 ("build this with me"): the
gravitational bending enters the law generically, in six steps. This note
is step 2, the composition of `optical-v1` (on `main` at 2d5c7cf2, light's
rows only, refused at the parse together with `massive_rows`) with the
massive rows of `massive-rows-v1`, so that one wall function and one turn
verb act on every row that walks, of every family alike. Step 1 (the
label's Bresenham along the momentum with the momentum's pair, records
536 and 551) is Far 2's on branch `optical-v1-bresenham`; this note takes
its form as given. Nothing here is built; the pins are written before any
run. Every number is labelled DETECTOR (a click) or GAMEBOARD (the host's
arithmetic on the declaration or on the lattice's lines).

## The six lines

1. **The information.** Under `optical` a light row's flight wall reads
   the crowd's age moment A at its Node, one interval retarded, through
   the wall 2 T_D (d + f n A) with f = 1 + gamma (gamma the declared
   post-Newtonian parameter), and its momentum accumulator **W** takes
   the crowd's arrival flow **V** at the weight (1 + gamma) content e_D.
   A massive row walks by its family's own triple (the rate 2 |**p**_D|_1,
   the wall 2 E'_D, E'_D = isqrt(E'_0^2 + 3 **p**_D . **p**_D), E'_0 = Q S M) and
   reads no crowd. With both keys the walk read light's table for every
   family (a massive row at light's pace), so the pair is refused at the
   parse (record 510). What moves in this note: the same age moment and the
   same flow, read by every row through its own family's numbers; nothing
   kept at a Node; the label D the phase's and the books' alone.
2. **The generic solution.** One triple function on the row's momentum
   **P** with the family's rest energy, one weight function on the family's
   label, no family name and no flag: the wall's pair (2 |**P**|_1 d, 2
   isqrt((Q d a E'_0)^2 + 3 **P** . **P**) (d + f n A)) with a the row's amount,
   which at E'_0 = 0 is Far 2's photon pair (2 S_1(**P**) Q d, 2 T(**P**) (d + f n A)) and at
   **W** = 0 the family's triple times Q d a; the push **W** -= n a w **V** with
   the weight per unit w = (E'_D^2 + 3 gamma **p**_D . **p**_D) // E'_D, which at
   E'_0 = 0 and gamma = 0 is the photon's e_D exactly and at gamma = 1 the
   photon's 2 e_D within one unit (section 3); the label by Bresenham
   along **P** as built.
3. **Why it works, and what refutes it.** In the metric of the
   parametrised post-Newtonian form (g_00 = -(1 - 2 U), g_ii = 1 + 2
   gamma U, U the potential) the coordinate pace of anything that moves
   is its local pace times (1 - (1 + gamma) U), blind to its speed and
   mass: the stretch is the wall's and the local pace is the triple's
   |**p**|_1 / E'. The push on a mover is (1 + gamma v^2) times its
   Newtonian push, v^2 = 3 **p** . **p** / E'^2: a slow row falls by Newton's 2 G M /
   (b v^2), light bends by (1 + gamma) 2 G M / (b c^2), one formula. The
   deciding world (section 2): slow massive rows beside the mass at two
   gamma. The reading that shows it, DETECTOR: the delays' ratio gamma = 1
   over gamma = 0 is 2.00 (the wall stretches a massive row as it does
   light), the shifts' ratio is 1 + gamma v^2 = 1.07 (not light's 2.00).
   The reading that refutes it: a delays' ratio of 1.00 (the massive wall
   unstretched), a shifts' ratio near 2.00 (the weight blind to the speed),
   or a slow row that does not fall by 2 G M / (b v^2) at gamma = 0.
4. **Why do it.** Without it no world holds light and matter beside one
   mass under one field: the refusal at the parse stands, Newton's fall of
   a row and the bending of light are two rules in two places, and the
   Highlights line "the rows' rule at a Node for general relativity's
   formulas" stays light's alone. With it, the equivalence of the fall
   (rows of amount 1 and 4 on one path) is read after a detector on rows,
   and step 3 (the body's drive at the same coefficient) has its form.
5. **The Highlights.** Kept: 281 (the click alone is compared), 394 (the
   age word), 496 (the residue is the time of the last Link, rescaled by
   the rate's ratio at every push), 551 (the pace is the momentum's), 562,
   564, 569 and "One motion primitive for a body as for a row" (this note
   is that primitive on the rows). To widen on the owner's word after the
   deciding world reads its pins: "optical-v1, the rows' rule at a Node
   for general relativity's formulas (light's rows only today)" to "every
   row that walks, its own triple's wall at 1 + gamma, its push at the
   weight (E'^2 + 3 gamma **p** . **p**) / E'".
6. **The implementation.** The engine (`src/event_universe/events/nature_beam.py`):
   the three optical functions take the family's table (`FamilyFlight`)
   in place of the world's `Flight` (section 4), the weight from the
   family's labels, the parse refusal of the two keys lifted
   (`world.py`); the tests of section 5 written first; the deciding
   world's generator from series K's with a massive lamp (section 2); the
   six optical pin worlds re-run (the photon's weight at gamma = 1 moves by
   one unit in 221, section 3) and the massive-rows worlds re-run for
   byte identity (no `optical` key: nothing moves). Host: the build two
   to four hours with the review (the Boss's estimate of record 574), the
   runs minutes each (the deciding world 1000 intervals), the 1024
   registration's re-run once; danger high in the massive walk (the pace
   of a falling row grows with |**P**|, section 4), guarded by the byte
   identity of every world without the key and by test (c) of section 5.
   The key stays off by default until step 5.

## 1. The composition, verb by verb

On `main` the optical verbs read `frame.flight`, the world's `Flight`
(light's numbers): `optical_rate_and_wall` (the rate 2 S_1 Q d and the wall
2 T_D (d + f n A) from `flight.manhattan` and `flight.resolution`),
`optical_walk_step` (`flight.accumulator`, `flight.lines`) and
`optical_turn` (`flight.energy`, e_D per direction, and `flight.neighbours`).
Every family already carries its own table at load, `FamilyFlight`
(`family_flight`): a family without the flag `massive` takes Flight's
numbers by value (the rate 2 S_1 Q, the wall 2 T_D, the start T_D, the
labels **u**_D), a massive family its labels **p**_D at the scale p, its triple
from E'_0 = Q S M. The composition is the substitution of the family's
table for light's in the three verbs, and nothing else:

- **Verb 1, the wall.** The row's accumulator gains the family's rate
  times d against the family's wall times (d + f n A): for a family
  without the flag exactly today's optical wall, for a massive family 2
  |**p**_D|_1 d against 2 E'_D (d + f n A). Under step 1's form the pair is the
  momentum's: for a row of amount a and momentum **P** = Q d a **p**_D + **W**
  (the label's momentum at the scale Q d, as `optical_turn` forms it), the
  rate 2 |**P**|_1 d and the wall 2 isqrt((Q d a E'_0)^2 + 3 **P** . **P**) (d + f n A).
  At E'_0 = 0 this is the photon's (S_1(**P**), T(**P**)) pair, scale-free, as
  Far 2 built it; at E'_0 > 0 the rest term is scaled by the same Q d a as
  **P**, so the pace |**P**|_1 / isqrt(...) is the triple's at **W** = 0 and grows
  as the push adds to **P**: a falling row speeds up, which is the physics
  (a body's speed under the push, DERIVATIONS_BEAM 3.3), and the reason
  the massive pair must be taken at **P**'s own scale and not reduced by a
  gcd of **P** alone; the pair (rate, wall) may be reduced by their common
  divisor with the residue rescaled by the rate's ratio, record 496's
  rule, the sub-unit remainder declared.
- **Verb 2, the push.** **W** -= n a w **V** at every interval of free space,
  **V** the crowd's arrival flow at the row's Node less its own number's, w
  the weight per unit of amount, w = (E'_D^2 + 3 gamma **p**_D . **p**_D) // E'_D
  from the family's labels (for the photon **p**_D = **u**_D and E'_D = e_D =
  isqrt(3 **u**_D . **u**_D); for a massive family E'_D the triple's own). The
  physics: the push on a mover of energy E' and momentum **p** is (E'^2 +
  3 gamma **p** . **p**) / E' times the flow, (1 + gamma v^2) E' with v^2 =
  3 **p** . **p** / E'^2; a slow row (**p** small) is pushed by E'_0 = Q S M times the
  flow, Newton's push on a body of content M; light by (1 + gamma) e_D.
- **Verb 3, the label.** Unchanged from step 1: the label among D and its
  fan neighbours by Bresenham along **P** (the cross accumulator), the same
  fan for every family, the label the phase's turn (massive-rows' de
  Broglie turn |p_{D,a}| N / h at the axis Links, its own accumulator
  `acc_turn`) and the click's momentum label alone.
- **What does not change.** The crowd's two moments (`CrowdMoments`, the
  age moment before step 1, the arrival flow after the collision) are
  read as they are; the completion of a massive record at a face or a
  wall (the one quantum handed) is as `massive-rows-v1` built it; the
  inverse interval stays refused under `optical`; `meeting` stays refused
  with `optical`; the parse refusal of `optical` with `massive_rows` is
  lifted once the three verbs read the family's table.

## 2. The deciding world, pinned before the run

Series K's geometry (the open box 57 x 41 x 41, the mass at the centre
releasing one row per direction per self-creation on the 290 primitive
directions with |a| + |b| + |c| <= 6, the screen the plane x = 54 of
one-Node detectors reading `age`), the pair [1, 16384], the mass M = 2^14
(a quarter of the optical pin worlds' 2^16, so that a slow row's turn stays
below 0.3 radian), and in place of the light lamp a lamp of a massive
family `matter` (`quantum` 1, `massive`, `momentum_magnitude` p = 10 at
the world's `width` S = 1: E'_0 = Q S M = 64, E' = isqrt(64^2 + 3 x 100) =
66, v^2 = 3 p^2 / E'^2 = 0.068, the dwell per Node E' / p = 6.6 intervals
against light's 1.72) at x = 2, y = 26 (b = 6), releasing on the heading
(1, 0, 0) alone (one line, the pin's form; the beam's width of series K is
not needed for the ratio); gamma = 0 and gamma = 1, each with its control
(no mass); 1000 intervals, the window 500 to 1000 (a row takes about 343
intervals to the screen). A fifth world: gamma = 0 with the lamp's amount
4 (the equivalence: the same x(t) to the Node).

The pins, from the light-bending note's map (`docs/designs/open_problems/light_bending/light_bending_map.py`,
section E's lines at b = 6) with the massive triple's accumulator in place
of the heading's dwell and the weight above in place of (1 + gamma) e_D
(GAMEBOARD arithmetic of the lattice's lines, computed on 2026-09-22 before
any world file; the generator's expectations.json restates them from the
same map before the run):

| World | gamma | the turn, rad | the shift at the screen, pixels (DETECTOR if run; bracket 0.5) | the delay, intervals (DETECTOR if run; bracket 1) |
| --- | --- | --- | --- | --- |
| `matter_g0` | 0 | 0.276 | -7.36 | 2.65 |
| `matter_g1` | 1 | 0.295 | -7.90 | 5.30 |
| `matter_g0_x4` | 0 | 0.276 | -7.36 (the amount 4) | 2.65 |

The numbers the run reads: the delays' ratio gamma = 1 over gamma = 0,
2.00, bracket 0.83 (propagated from the two brackets of 1 interval in
quadrature; record 483's rule), the wall's factor on a massive row; the
shifts' ratio 1.07, bracket 0.10 (propagated from the two brackets of 0.5
pixel), the weight's (1 + gamma v^2) against light's 2.00; and the
equivalence, `matter_g0_x4` on `matter_g0`'s pixel to the Node. At M =
2^13 the same ratios with the delays 1.33 / 2.65 and the shifts -3.61 /
-3.86, below the brackets' reach for the ratio: 2^14 is the choice. The
gamma = 0 shift is Newton's fall of a slow row, 2 G M / (b v^2) on the
lattice's lines, the first reading of 3.3's push on a row after a
detector.

## 3. The three tests, the bounds, the one floor

- **Generic.** One triple function (`flight_triple`'s form on **P** with the
  rest energy scaled) and one weight function on the family's labels,
  declared integers, no family name; the photon is the case E'_0 = 0 by
  value, never by a branch (massive-rows' own rule).
- **Vector.** The wall is the flight's verb on the accumulator, the push
  the translation of **W**, the label's Bresenham the verb of step 1; the
  one root is `integer_root` on **P**, the law's own resolution of a direction
  (T_D, E'_D), per pushed row when **P** changes, a bounded host cost (record
  551's point for the reviewer); no float.
- **Local.** The row's own **P**, cross accumulator and residue, the crowd's
  two moments at its Node; nothing kept at a Node.
- **The bounds.** **P** carries the amount as a factor and its components
  reach Q d a |**p**_D| + |**W**|; the wall's square (Q d a E'_0)^2 + 3 **P** . **P** is
  formed in Python integers (as the fan comparison is today) and the pair
  reduced by its common divisor for the register; the existing refusal
  names the rule when a product exceeds the working bound.
- **The one floor.** w = (E'_D^2 + 3 gamma **p**_D . **p**_D) // E'_D: at gamma = 0 it
  is E'_D exactly (the photon's e_D = 110 on a heading, the massive row's
  66 in the deciding world); at gamma = 1 the photon's w is (12100 +
  12288) // 110 = 221 where the build on `main` has 2 e_D = 220, one unit
  in 221 (0.5 %), because e_D^2 = 12100 is not 3 **u**_D . **u**_D = 12288 (the
  root's floor). The generic formula is the law's; the six optical pin
  worlds at gamma = 1 are re-run under it (the pins stand, the change is
  fifty times below the 0.5-pixel bracket), the byte identity of every
  world without the key untouched. The alternative, w = (E'_0^2 + 3 (1 +
  gamma) **p**_D . **p**_D) // E'_D without the root in the numerator, moves the
  photon at gamma = 0 too (111 for 110) and is not taken.

## 4. What changes in the tree

- `src/event_universe/events/nature_beam.py`: `optical_rate_and_wall`,
  `optical_walk_step`, `optical_last_link` and `optical_turn` take the
  family's `FamilyFlight` (rate, wall, start, labels) from
  `frame.tables` in place of `frame.flight`; the momentum's pair of step
  1 gains the rest term (Q d a E'_0)^2 under the root; `flight.energy`
  is replaced by the weight from the family's labels; the fan neighbours
  stay the direction table's. The store's fields (`made`, `residue`,
  `push`, `cross`) are already per row and family-blind.
- `src/event_universe/events/world.py`: the refusal of `optical` with
  `massive_rows` lifted; the refusals of `optical` with `meeting` and of
  the inverse interval under `optical` kept.
- `examples/events/optical/`: the deciding worlds (section 2) by the
  generator beside the light pin worlds, their `expectations.json` from
  the map before the run; the six light worlds re-run.
- `docs/BEAM_LAW.md` (the architect's) and `docs/ENGINE.md`: the optical
  identity's lines say "every row that walks" once the deciding world is
  read; `docs/HYPOTHESES.md` 27 likewise; the Highlights line by the
  owner's word (line 5 of the six).

## 5. The tests, written first

- (a) The weight: on a family without the flag at gamma = 0 the weight is
  e_D on every direction (the build on `main`'s numbers, byte for byte);
  on the deciding world's `matter` family E' = 66 at gamma = 0 and (66^2
  + 300) // 66 = 70 at gamma = 1; at E'_0 = 0 and gamma = 1 the photon's 221
  on a heading (the one floor, named in the test).
- (b) The pair: a massive row of amount 1 with **W** = 0 walks at its
  triple's pace (2 |**p**_D|_1 d against 2 E'_D d, the accumulator's identity
  at A = 0, the rows' Nodes those of `massive-rows-v1` interval by
  interval); pushed to **P** = Q d **p**_D + **W** its pace is |**P**|_1 / isqrt((Q d
  E'_0)^2 + 3 **P** . **P**), larger than at **W** = 0 when **W** is along **p**_D (a
  falling row speeds up); at E'_0 = 0 the pair is step 1's exactly.
- (c) Byte identity: every registered world without the key `optical`
  (the massive-rows worlds, series K, the clock series) runs to the same
  state digest as on `main`; the six optical light worlds at gamma = 0 to
  the same digest, at gamma = 1 to the digest of the re-run named in the
  register.
- (d) The refusals: the two keys together load; `optical` with `meeting`
  refused; the inverse interval refused under `optical`.
- (e) The deciding world's readings from the clicks alone (the screen's
  click lines), the pins of section 2 restated in `expectations.json`.

## 6. The steps that follow

Step 3, the body's drive in the age wall's set at the same 1 + gamma (form
B's drive at the fraction, the same metric factor on the coordinate pace),
its pin a body beside the mass with a lamp (the Newton session's form,
record 607). Step 4, gamma's standing: a derivation of the space part from
the law, which no one has, or the owner's declaration of gamma = 1 as an
input of kind 2 with its NATURE row. Step 5, the key removed: the flight
member in the age wall's set always, every registered world with a crowd
re-run and re-pinned by the Replicator (the price named to the owner: the
0.000 of series K becomes a bending). Step 6, the Highlights line.

## 7. Links

- [The generic optical-v1](NOTE.md), [the chief physicist's re-read](PHYSICIST.md), [the mathematician's check](MATHEMATICIAN.md).
- [The light-bending note and its map](../open_problems/light_bending/NOTE.md).
- [The massive rows' design](../massive_rows/DESIGN.md) and [their register worlds](../../../examples/events/massive_rows/README.md).
- [The optical pin worlds](../../../examples/events/optical/README.md).
- [DERIVATIONS_BEAM 3.3](../../../docs/DERIVATIONS_BEAM.md#33-newtons-law-and-gs-place) and [5.4](../../../docs/DERIVATIONS_BEAM.md#54-light-no-optical-metric-on-main-the-meetings-turn-as-a-key).
