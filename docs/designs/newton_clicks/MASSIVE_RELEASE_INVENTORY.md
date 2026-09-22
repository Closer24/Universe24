# What the law as built already has for a released row with mass past a held mass, read by a click (the chief physicist, an inventory, no run)

The model owner's words of 2026-09-22 (records 1044 and 1046 of
[docs/LOG_2026-09-20.md](../../LOG_2026-09-20.md): no cart; a moving
detector as it should be, with mass, "otherwise there is no matter to
transfer"; Newton out of the algebra of the clicks, Einstein the step
between) and the Boss's bounded order: one page on what `main` at
5c7e69a9 already holds for such a world, each item with its file, its
section, its key, the kind of its reading, and one line saying whether it
applies to a massive released row unchanged, with a declaration, or not
at all. The pins are the mathematician's
(`NEWTON_FROM_CLICKS.md`, to come beside this file); no number is chosen
here, nothing is built and nothing is run.

## The world the owner names, in the law's words

A measured event at rest (the emitter) releases a row of a paid family
in one declared direction; the row walks Node by Node past a measured
event holding a free mass (the held mass, whose released rows are the
crowd the walking row reads); its arrival at a second measured event at
rest (the receiver) is a click on the receiver's record: the Node, the
row's ordinal (`record` mod 2^32, the emitter's birth count) and, under
the key `clock_stamp` (PR #834, on `main` since ee3d34f6; the reviewer's
read Q ADMISSIBLE), the receiver's own count. Mass on the row is the identity `massive-rows-v1`: a paid family
declared `massive` births rows of content M with a momentum label at the
scale p; a free family's rows carry no content (`world.py`, `families`:
"whose rays carry no content"), and a paid family without the flag
carries the content quantum x turn and the label at the scale Q.

## The inventory

| What the law has | File, section | Key | Kind of its reading | On a massive released row |
| --- | --- | --- | --- | --- |
| **massive-rows-v1**, the row's content as its mass: a paid family declared `massive` births records of rows carrying the content M (its `quantum`) and the label **p**_D = `unit_label` of D at the scale p; the primitive is the flight's one accumulator, the rate 2 abs(**p**_D)_1 against the wall 2 E'_D with E'_D = isqrt((Q S M)^2 + 3 **p**_D . **p**_D) formed at load (integers: Q = 64, S the width, M, p, E'_D; the turn abs(p_a) N / h per axis Link over `action` h); the completion hands ONE quantum (M and the one label) to the chosen set (f_F = 0, q_F = M) | [docs/designs/massive_rows/DESIGN.md](../massive_rows/DESIGN.md) section 1 (the keys), 3 (the completion); [docs/ENGINE.md](../../ENGINE.md) "the massive rows" (`nature_beam.FamilyFlight`, `NatureBeamTables.family_flights`); [BEAM_LAW section 2](../../BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file); the register [W](../../EXPERIMENTS.md#w-the-massive-rows-2026-09-21), `examples/events/massive_rows/` | the world key `massive_rows` (false by default; `age_bound` declared with it; `action` h required), the family key `massive` (a paid family with a phase circle, no `phase_per_link`), the lamp key `momentum_magnitude` p (required on a massive family's lamp, refused elsewhere) | DETECTOR: the `click` line (what arrived, `content` and `push`) and the `gather` line (the placed quantum M and q_F x the label; ENGINE.md's row "the placed quantum of a completion"); GAMEBOARD: the `waiting` lines of the books, a completion at a face | **With a declaration**: the three keys above. This is the only way the law gives a released row mass; without them the row's content is quantum x turn at the scale Q, a photon's. |
| **Series K, light past a mass**: an open 57 x 41 x 41 box, a lamp of the paid family `light` at (2, 20 + b, 20) releasing one unit per interval on five directions within 5 degrees of +x, a fixed mass of the free phase-less family `m` at the centre releasing series E's fan of 290 every interval, a screen of 1681 one-Node `wave` pixels at x = 54 reading `age` for `light` and `pass` for `m`, `suspension` 0; four worlds (control, mass, heavy, near) | [docs/EXPERIMENTS.md, K](../../EXPERIMENTS.md#k-light-beside-a-mass-2026-09-20); `examples/events/lensing/` (`make_worlds.py`, `tools/lensing_readings.py`) | no key of a hypothesis; `reads: "age"` on the screen's table entry; `suspension` [0, d] | DETECTOR: the centroid's deflection 0.000 pixel in y and z, the mean age's delta 0.00 interval, the count ratio 1.0000, the phase rate 8.000; the verdict a plain disagreement with nature (FAIL: nature's 46 to 91 radians, hundreds of intervals), registered on 2026-09-20 under the law before the generic entry | **With a declaration, and not as it stands**: the geometry (a lamp, a held mass releasing, a far reader) is the owner's world's; the row is a photon (content 1) and the pair [0, d], at which the generic entry stretches and pushes nothing (below), so K's numbers say nothing about a massive row. A massive family in K's lamp needs the three keys of the row above and a pair with n > 0. |
| **The flight wall** (the age word's one wall function on a row): the row's flight is a member of the age wall's declared set, the rate 2 S_1 Q d against the wall 2 T_D (d + f n A), A the crowd's age moment at the row's Node read one interval retarded, f = 1 + gamma; under `massive_rows` the row walks by its own family's pair with the rest term (`row_pairs`, `momentum_pair`), the wall's square refused before it is formed above the working bound | [docs/ENGINE.md](../../ENGINE.md) "the age wall's set" (`measured.AGE_WALL_SET`, `core.integer.age_wall`) and the `optical` paragraph (`nature_beam.optical_walk_step`); [docs/designs/one_wall/EVERY_FAMILY.md](../one_wall/EVERY_FAMILY.md) | the world's `suspension` [n, d] (the stretch is n / d times A: at [0, d] or with no crowd the walk is integer for integer as before, byte for byte); `optical` gamma (0 by default) | GAMEBOARD: the row's flight accumulator in the snapshot where a crowd moved it; DETECTOR: the click's exact time, ONE form for every row, (age r - s + T d) / r (`optical_last_link`) | **Unchanged**, once the row exists under `massive_rows` and the pair has n > 0: every family walks under the one wall since 2026-09-22 (EVERY_FAMILY.md), the massive row by its own pair. The bound: the primitive of **P** with the rest term under about 2^24.7 per component, else refused naming the rule (the price note's line (i)). |
| **The flow label** (flow-link-v1): the arrival flow every reader sums counts each arriving row of direction D with the flow label **f**_D, the integer vector nearest abs(p_D) D / S_1 (the label per Euclidean Link), in place of the unit label; abs(p_D) is Q for the photon and a massive family's `momentum_magnitude` (`FamilyFlight.flow_labels`); read by the flow's sums alone (the rows' push, a body's push through the group moment); the age moment, the wall, the flight, the collision, the phase and the momentum a click moves untouched | [docs/ENGINE.md](../../ENGINE.md) "`flow_link`" (`nature_beam.flow_label`); [docs/designs/flow_weight/DESIGN.md](../flow_weight/DESIGN.md) section 3 (c), [ALGEBRA.md](../flow_weight/ALGEBRA.md) section 5 | the world key `flow_link` (false by default; the identity `flow-link-v1` under `hypotheses` when true) | GAMEBOARD: the push a row or a body takes (the flow); no reading of its own | **Unchanged, on or off by the world's choice**: the massive family's flow labels are formed from its own p at load; it changes what the held mass's crowd pushes the row by (the L1 factor of the fan, 1.44 on K's 290 directions, removed under the key), not the row's mass or its flight. |
| **The age word** (clock-age-v1): a body's owed count is the count of its accumulator at the rate k x n over d, k the age moment sum amount x age of the other numbers' rows at its Node (or the presence on a table entry that reads `presence`); on a table entry that reads `age` a click carries the arriving row's age (note 25); series T read the age word at two distances (the ratio 42 / 22 = 1.909 against the continuum's 2.000) | [docs/ENGINE.md](../../ENGINE.md) "the owed count" (`_suspend`, `count_owed`, `measured.count_component`); [docs/EXPERIMENTS.md, T](../../EXPERIMENTS.md#t-the-clocks-word-2026-09-21); [docs/designs/clock_age/NOTE.md](../clock_age/NOTE.md) | `suspension` [n, d] on the world; `reads: "age"` or `"presence"` on a table entry; no key of a hypothesis (the age moment the default since 2026-09-21) | the birth ordinal DETECTOR against the click's tick, a GAMEBOARD count (a fixed detector's own age at `suspension` 0, record 569; the receiver's own count DETECTOR under `clock_stamp`); 1 + z the inverse slope, COMPUTATION from the two (T's pins 2.650 and 4.150); GAMEBOARD: the moments and k | **Unchanged on the receiver and the emitter** (bodies at rest owe by the crowd at their Nodes as any); **not at all on the row itself**: a row owes no count, it is stretched by the flight wall above, the same A and the same one wall function. A massive row's `age` on the click is read as a photon's, by `reads: "age"`. |
| **The generic entry of the bending** (2026-09-22): the row's flight in the age wall's set at 1 + gamma for every world (no key, no hypothesis; `optical` names none since 2026-09-22), and after the collision every row of content in free space is pushed by the interval's arrival flow at its Node, **W** -= n (1 + gamma) content e_D **V**, its label following the line of its whole momentum **P** = Q d content **u**_D + **W** by Bresenham (the label chosen among D and its fan neighbours), its pace its momentum's, the residue rescaled at every push; under `massive_rows` the push at the weight per unit (E'_D^2 + 3 gamma **p**_D . **p**_D) // E'_D on the family's labels (`unit_weights`) and the pair of **P** with the rest term (`row_pairs`); at `suspension` 0 nothing is stretched and nothing pushed; the price: the registered crowd worlds at n > 0 refuse or freeze | [docs/ENGINE.md](../../ENGINE.md) the `optical` paragraph (`optical_walk_step`, `optical_turn`, `momentum_pair`, `unit_weights`, `row_pairs`); [docs/designs/one_wall/GENERIC_BENDING_PRICE.md](../one_wall/GENERIC_BENDING_PRICE.md); [EVERY_FAMILY.md](../one_wall/EVERY_FAMILY.md) | `optical` gamma, a non-negative integer, 0 by default (nature's 1 a declaration per world, never a default, record 817); `suspension` [n, d] with n > 0 for anything to act; the record's block `optical` {gamma, flight_coefficient} for every world | DETECTOR: the click's Node (the bending, a displaced arrival), its exact time (the delay) and its `push` (the label after the turns); GAMEBOARD: the row's `cross` accumulator and its **W** in the snapshot | **Unchanged**: the law's own for every row of content since 2026-09-22, the massive row included by EVERY_FAMILY.md (the rest term in its pair and its weight; the pushed row's pace its momentum's, below the flight's). What it does to a massive row past a held mass at a pair with n > 0 is exactly the reading the owner asks for, and no registered world has read it: the 32 crowd worlds at n > 0 are light rows at d = 65536 and refuse (the price note); a massive row's **P** carries its own p and M and meets the bound on its own terms, to be checked at the declared numbers before any run. |

Beside these, three things the click carries that the reading would use,
all built: the row's ordinal on the click line (`record` mod 2^32, the
emitter's birth count; the amplitude law's record form), the emitter's
birth wheel (`wheel` [r, W], required on every lamp) and the row's `age`
on a table entry that reads it; and the receiver's own count on every
line it writes, `clock`, under the key `clock_stamp` (PR #834, on `main`). The push of a paid row on the reader it clicks is the label itself
(note 18): a massive row's click moves the receiver's momentum by
**p**_D and hands it M at the completion, the matter transferred.

## The shortest list of declarations such a world would need

No number is chosen here; each line names the key and what fixes it.

1. The world keys `massive_rows: true`, `age_bound` (at least the longest
   flight), `action` h and `width` S (the rest energy Q S M and de
   Broglie's turn); `suspension` [n, d] with n > 0 (the wall and the push
   act on nothing at [0, d]); `optical` gamma, 0 or a declared 1;
   `flow_link` on or off, stated either way.
2. The family of the row: a paid family declared `massive` with its
   `quantum` M, a phase circle (`phase` true) and no `phase_per_link`;
   the held mass's free family `m` (quantum 0, `phase` false, `charge` 0).
3. The emitter: a measured event at rest of the massive family with a
   `lamp` (`rate`, `wheel`, one declared direction under `directions`,
   `momentum_magnitude` p) and the content K at the turn rate [1, K], so
   that its turn is exactly 1 at the birth (the refusal at the birth in
   nature_beam.py's `_release_family`, not at load); each unit born costs
   the lamp M, so the turn falls to 0 on one self-creation in about
   K / (births x M) and never to 2: the births' rate is read as the ordinal
   against the receiver's count, not as one per interval.
4. The held mass: a fixed measured event of `m` with the amount and the
   `directions` of its release (the crowd is its released rows; a mass that
   releases nothing is read by nothing) and the world's `release` [n, d].
5. The receiver: a measured event at rest (or a declared detector) whose
   table measures the massive family (`measure`, `reads: "age"` for the
   row's age on the click), with `pass` for `m` on the emitter and the
   receiver; the faces open.
6. The click instrument: `clock_stamp: true` (PR #834, on `main`: the
   receiver's own count on the click line; without it the tick, a
   GAMEBOARD count, is what the line carries).
7. The pair's bound checked before the run: the primitive of the pushed
   row's **P** with the rest term under the working bound at the declared
   p, M, d and crowd (the price note's line (i)), or the world refuses.

What the law does NOT have: a rule by which a row in transit transfers
its content to anything but a measured event at its completion (the
click, the gather), and any reading of a row's own count (a row has an
age, not a clock). Everything else the owner's world needs is on `main`
under the declarations above, and its pins are the mathematician's.
