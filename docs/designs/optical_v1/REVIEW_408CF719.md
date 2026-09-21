# The physics-rule review of optical-v1 in its generic form at 408cf719 (Far 2's Part B), before the merge

The open-problems physicist's read-only review of 2026-09-21, on the Boss's
order under the model owner's word (record 396 of docs/LOG_2026-09-20.md):
branch `optical-v1` at its head 408cf719, which carries `clock-age-v1` at
fe987c73 (merged at 3f28b11, the Part A review's corrections included) and
`origin/main` (merged at f131f7f), read against the one-wall note as merged
([NOTE.md section 2](../one_wall/NOTE.md)), this identity's third review
([REVIEW_3.md](REVIEW_3.md), its four must-fixes and the fifth) and
BEAM_LAW's world-key text as the branch amends it. Nothing on the branch
was touched. The runs below are the reviewer's GameBoard diagnostics and
detector readings of worlds already registered, on a scratch tree that is
not pushed; the register's own numbers moved nowhere by this page.

## Verdict: ADMISSIBLE WITH CORRECTIONS

The key is one declaration of gamma with its refusals at load; the set is
the identity's with the never-list kept; verb 1 is the law's one wall
function on the flight's pair, verb 2 the law's push with the declared
weight, verb 3 a comparison of the fan's neighbours that conserves the
whole momentum; LOCALITY-1 holds in all three; with the key off the five
new accumulators are constant 0 and sixteen of sixteen gate worlds read
byte for byte as on main. One correction is a must, in the engine (M1); it
is the junction of verb 1 and verb 3, which no text declares.

**M1 (engine; `src/event_universe/events/nature_beam.py`, the walk's step
and the turn).** The row's flight accumulator is stored in the units of
its own direction's wall, `2 T_D (d + f n A)`, and verb 3 changes the
direction without rescaling the residue. The walk's own docstring asserts
what then fails: "the count gained (0 or 1: the rate never exceeds the
wall)". After a turn the carried residue is measured against the new
direction's wall, which in the pin world's fan is up to
`T(24,1,0) / T(1,0,0)` = 2662 / 110 = 24.2 times smaller, so the raw count
reaches 24. The code caps the Links walked with `np.minimum(moved, 1)` but
keeps the residue of the **uncapped** count, so the row makes one Link and
its accumulator is debited for all of them: credit the wall was paid for
is destroyed. The law's own count primitive has the cap that keeps it
(`by_drive`'s and `by_drive_rows`' `at_most`, "caps the count gained at
one self-creation and keeps the rest in the accumulator"), and the design
says "a Link when acc >= 2 T_D (d + f n A), the wall subtracted, the
residue kept on the row", which is the same contract.

It fires in the registered pin worlds. The reviewer's instrumented run
(the head's engine, the count read before the cap):

| World | intervals | row-intervals with a raw count of 2 or more | the largest count |
| --- | --- | --- | --- |
| `mass_g1` | 150 | 445 | 24 |
| `near_g1` | 150 | 319 | 23 |

A shrinking crowd cannot do this (the wall moves by 4.2 per cent at
[1, 16384] with A of order 400, so the count could reach 2 and no more);
24 is the fan's ratio above, so the turn is the cause, by arithmetic and
by the numbers.

What it costs, measured: the reviewer's counterexample tree (the cap by
`at_most=1` and the residue rescaled by `T_new / T_old` at the turn; a
scratch tree, never pushed, and not a recommendation of either form) run
over the same six worlds at 400 intervals and read by
`tools/lensing_readings.py --no-replay`, beside the head's own run, which
reproduces the register exactly:

| Reading (DETECTOR) | pinned | the head | the counterexample |
| --- | --- | --- | --- |
| `mass` shift, f = 1 / f = 2 | -1.93 / -3.86 | -1.607 / -3.812 | -1.622 / -3.806 |
| `near` shift, f = 1 / f = 2 | -2.42 / -4.83 | -2.992 / -4.654 | -3.000 / -4.408 |
| `mass` delay, f = 1 / f = 2 | 2.68 / 5.36 | 2.89 / 5.87 | 2.96 / 6.04 |
| `near` delay, f = 1 / f = 2 | 2.17 / 4.34 | 2.40 / 4.97 | 2.60 / 5.15 |
| the delays' ratio, `mass` / `near` | 2.00 +- 0.25 | 2.03 / 2.07 | 2.04 / 1.98 |
| the shifts' ratio, `mass` / `near` | 2.00 +- 0.25 | 2.37 / 1.56 | 2.35 / 1.47 |

No verdict of the register's entry turns on it: the delays' ratios stay
inside the bracket, the shifts' stay outside, `near` at f = 1 stays
outside by 0.08 and the other three shifts stay inside 0.5. The
correction is therefore not a re-reading of the physics, but the rule must
keep what its own wall paid for: the surplus kept by the count primitive's
cap, and the residue's units at a turn declared (rescaled to the new
direction's wall, or cleared). Which of the two is verb 3's form belongs
with the Bresenham question already on the model owner's list; the entry's
run is re-read after the fix, the four delays and shifts above being what
moves.

## 1. The three tests, one line each per rule

- **The set, `measured.age_wall_set(optical)` and `age_wall_coefficient`.**
  Generic: a declaration by the count's name with a coefficient, the
  law's `("owed", 1)` plus the key's `("flight", 1 + gamma)`, no family and
  no kind; the never-list refused before the set is read. Vector: no verb.
  Local: no state. PASS. REVIEW_3's should-fix 3 is met: the set is the
  identity's, the world declares gamma alone.
- **Verb 1, the flight's wall (`optical_walk_step`,
  `optical_rate_and_wall`).** Generic: `core.integer.age_wall` on the
  flight's pair with the declared coefficient, every row alike. Vector: one
  count on an accumulator, the rate bilinear in the wall and the crowd's
  moment, no root, no float. Local: the moment is the row's own Node's,
  less its own number, read before step 1; the accumulator is a field of
  the row, nothing kept at a Node. PASS, with M1 on the accumulator's
  units at a turn.
- **Verb 2, the push (`optical_turn`, the first half).** Generic: every
  row of content in free space, the weight `(1 + gamma) content e_D` with
  the content the row's own column (a row of a free family carries content
  0 and never turns: a column, not a kind). Vector: **W** -= n weight
  **V**, bilinear, the law's own push form with gravity's sign. Local: the
  flow is the interval's own arrivals at the row's Node less its own
  number, the crossing rule's set, as a body's push reads it in step 4.
  PASS.
- **Verb 3, the turn (`optical_turn`, the second half).** Generic: the
  label moves to the fan's nearest neighbour of the row's whole momentum,
  no family name. Vector: comparisons of integers only (the cosines cross-
  multiplied), the permutation on the direction index, and **W** takes
  `Q d content (u_D - u_D')` so **P** is conserved. Local: at most
  `FAN_NEIGHBOURS` = 6 neighbours from a table built at load, one step per
  interval, fixed work. PASS.

## 2. LOCALITY-1

Two readings of the crowd, both at the row's own Node and both less the
reader's own number (`CrowdMoments`, segmented sums, no family name): the
wall's age moment A read once before step 1 from the state of the interval
before, one interval retarded, and the turn's flow **V** read after the
walk and the collision from the interval's own arrivals, which is the
crossing rule's set and what a body's push already reads. Nothing is kept
at a Node between intervals; the five new fields live on the row; the fan's
neighbour table and e_D are constants of the direction table at load, as
T_D and **u**_D are. No path relays a reading across two Links in one
interval. The bounds are tested by division before the products are formed
(the wall, the push per interval, the age moment).

## 3. The measurement rule on the register's entry

The pins are in `examples/events/optical/expectations.json` with their
derivation, written before the run; the entry and the worlds' README label
every line DETECTOR (the screen's centroid, the delay, the clicks) or
GAMEBOARD (the crowd at b, the lamp's clock rate, `tools/optical_readings.py`'s
angles of **P**), and the diagnostic's own text says it reads verb 2's
arithmetic back to itself and says nothing about where the light arrives.
The `near` shift at f = 1 stays outside its bracket and the shifts' ratio
stays refuted at 0.25, both recorded as they are, with the bracket's own
inconsistency named as a fact of the pin rather than a new pin: the rule
of record 281 and of the derivation before the numbers is kept. The
reviewer reran the six worlds on the head: the readings are the register's,
integer for integer in the columns above.

## 4. Bit-exactness with the key off

The five accumulators (`made`, `residue`, `push_x`, `push_y`, `push_z`)
are constant 0 without the key, and `test_optical.py` (e) pins that and
that no `flight` or `push` line reaches `state.json`. The reviewer's own
check: the nine gate worlds pinned by digests pass
`tests/test_amplitude_click.py` (d) on the head, and the seven gate worlds
without digests were run at their caps on main's engine and on 408cf719,
the three digests (state, books, events) equal on both. Sixteen of
sixteen, the Boss's `--list --fast` replay confirmed by hand.

## 5. The declarations against the merged one-wall note

One key, `optical: gamma`, parsed once with f = 1 + gamma derived once
(`NatureBeamWorld.flight_coefficient`) and written into the wall and the
weight as the same number; the refusals listed once at load and tested in
(d): `suspension` 0, `meeting` (one turn verb per row), gamma not a
non-negative integer, a moving direction with no neighbour within a right
angle; the inverse interval refused under the key, with its reason (the
wall reads the crowd of the interval before). The weight is `content x e_D`
with e_D = 110 or 111, never the direction's T_D of 2662 (REVIEW_3's
must-fix 1). The phase per age is not a member and cannot be declared one.
The body's side of the identity is not built, as must-fix 2 and 3 asked:
the body's drive is not a member, the energy weight
`(E^2 + 3 gamma p . p) / E` waits on form B, and the key changes rows
alone. The run's record carries `optical` {gamma, flight_coefficient} and
the identity under `hypotheses`, under the key only.

## 6. The generic check and the price

`push_x/y/z` are the row's momentum accumulator of this identity and are
distinct in name and in meaning from massive-rows' `acc_turn`, the phase's
turn count; both may exist in one store without meeting. A row of amount
a behaves as a rows of amount 1: the weight and the label term of **P**
both scale with the row's whole content, so the turn's decision is the
same and the merge changes no physics. The price, named rather than
charged: `optical_rate_and_wall` calls `age_wall` in a Python loop per row
per interval, and the five fields are identity fields, so rows carrying
different pushes no longer merge (the pin worlds show no growth from it:
457 light rows at the end of `mass_g1` against the control's 447).

## Should-fixes (not blocking)

- **S1.** The push accumulator's own growth is not bounded-checked: the
  per-interval product n x weight x |**V**| is tested by division with one
  doubling of headroom, but **W** + that product is not, so a long path in
  a dense crowd would wrap the int64 field silently. The largest |**W**|
  component in the pin worlds is 2^28, far from the register, so this is
  the missing check and not a present overflow; `checked_work`'s
  convention is to test the sum before forming it.
- **S2.** The walk's docstring states the invariant "0 or 1: the rate never
  exceeds the wall", which holds for a row on its own direction and not
  after a turn; whatever M1's form, the sentence is corrected with it.
- **S3.** The entry and BEAM_LAW name the wall's reading as one interval
  retarded but leave the turn's flow to the code's docstring; one clause
  saying the flow is the interval's own arrivals, the crossing rule's set,
  puts both reads in the law's text.
