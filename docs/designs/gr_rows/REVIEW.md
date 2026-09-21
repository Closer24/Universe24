# Physics-rule review of `optical-v1` (docs/designs/gr_rows/DESIGN.md): the rows reading the crowd

Read-only review, the physics-rule reviewer, 2026-09-21. The object: the
branch `claude/series-m-masses` at its head 676fafe8 (the assignment named
ac67fec3; the head carries one more commit, section 5b, Snell's law, and is
what was reviewed), in a detached worktree; nothing edited, nothing run
beyond `docs/designs/gr_rows/gr_rows_map.py` (re-run: its output is byte
identical to the committed `gr_rows_map.out`). Read against AGENTS.md (the
change boundaries, the three tests, record 281's measurement rule),
skills/workflow.md ("The three tests of every rule", "Notation"),
skills/physics-rule-validation/SKILL.md, SIMULATOR_DEFINITIONS.md
(LOCALITY-1), BEAM_LAW.md notes 35, 41, 47 and 48, designs/vector_form/LAW.md
(the six verbs, the roundings at load), DERIVATIONS_BEAM.md 5.1 to 5.6, 13,
15.2, 15.5, 15.6, 17.4 and 21.2, light_speed/FORM.md section 3 (form B),
records 281, 291, 294, 297, 300 and 301 (294, 297 and 300 read from
origin/main, since the branch's log ends at 292), the lensing README and
world files, and the code the design's rule would touch (`engine.py`
`count_owed` and `_suspend`, `nature_beam.py` `read_arrivals`, `Flight`,
the clock's `counted`, `measured.count_component`, `world.py`'s parsing of
`suspension`, `meeting` and the table entries, `meeting.py` `crowd_flow`).
Every symbol is named at its first use below; a scalar plain, a vector in
bold lowercase.

## VERDICT: ADMISSIBLE WITH MUST-FIXES

`optical-v1` is admissible as a hypothesis under its own identity beside the
law: each of its three parts is one primitive with declared integers, one of
the six verbs (a translation whose wall is read from the state, as the
growing wall of 15.2 and 15.6; two translations, two comparisons and a
permutation on the fan; one Euclidean division with a bilinear rate), and
local (the row's own record and the rows present at its own Node, the
reading set of note 47, fixed work per row for fixed K). No seventh verb, no
root at run time, no float. The build may start on the owner's go ONLY after
the eight must-fixes below are made in the design, because as written the
design (1) turns a row away from the mass, (2) states verb 2's integers in
two different units, (3) has no identity key, so that it would be on in the
27 registered worlds whose `suspension` pair is nonzero, (4) omits the
row's flight accumulator from the store and leaves the click's exact phase
reading a count that no longer gives the time, (5) names no step of the
interval for its reading, (6) computes the pin world's lamp with a component
its world file does not declare, (7) ignores the beam's own age moment read
by the crowd's rows, which moves its pinned numbers by tens of percent, and
(8) puts a GameBoard number in the pin table unlabelled.

The three verdicts, one line each (the whole rule, after the must-fixes):

- Generic: PASSES. One wall and one turn read off two moments of the Node,
  the same for every family and direction, the own number excluded by a
  comparison of numbers (the class `crowd_flow` uses), the factor a declared
  integer of the world (must-fix 3), no family name, no branch on a kind.
- Vector: PASSES. (T) with a state-read wall for the pace (the form of 15.6,
  admitted for the growing wall), (T)+(D)+(P) for the turn with its rate
  linear in the flow and its remainder kept, (D) with a bilinear rate for the
  second order; THETA (the fan's step angle) a rounding at load like `T_D`
  once its grain is declared (must-fix 2); no root, no float at run time.
- Local: PASSES. The row reads its own record and the moments of the rows
  present at its own Node (zero hops; the six neighbours are not even
  needed), recomputed per interval, nothing kept at a Node; the work per
  row per interval is fixed for fixed K (about 24 beyond the walk, plus the
  Node's reading), the host's segmented sum reported apart (section 1 (c)).

## 1. The three tests on each of the three parts

### 1 (a) The wall of the flight, `2 T_D (d_s + 2 n_s A)`

Symbols: `T_D` the direction's resolution (the flight's wall today is
`2 T_D`), `S_1` the direction's Manhattan length, Q the label's scale,
`[n_s, d_s]` the world's `suspension` pair, A the age moment of the rows of
other numbers at the Node (sum of amount x age), `k_a = n_s A / d_s` the
number the clock reads at the same Node, `c_0 = S_1 Q / T_D` the pace on the
line in Links per interval.

- Generic: the wall is one count with declared integers, but the factor 2
  is a constant hidden in the rule as written ("one new integer, the factor
  2, written into the wall and the turn"; section 4 then calls it "[2, 1]
  and not [1, 1]"). Under the generic test the only free numbers are the
  family table's declared integers, the width and the initial state: a
  literal 2 that the engine carries and that the Newton case would need a
  code change to alter is not a declared integer. It is a declared integer
  once the world declares it (must-fix 3); then the factor-1 world is a
  declaration and the factor is what Cassini pins. With that, passes.
- Vector: (T) on the row's position accumulator at the rate `2 S_1 Q d_s`
  with the wall `2 T_D (d_s + 2 n_s A)`; the pace `c_0 / (1 + 2 k_a)`
  follows (checked). The wall is linear in the state (A), the rate constant:
  within "at most bilinear". It is the feedback form of 15.2 and 15.6 that
  the growing wall already had admitted in principle. Two consequences the
  design does not draw: the accumulator can no longer be a function of the
  age (`Flight.accumulator` today: "both are off the age and the row
  carries no field for them"), so the row's record gains the accumulator
  with its residue (must-fix 4); and the rows leave LAW.md section 5's
  closed form ("a record is in the linear block while its rows fly: its
  state at the click a closed form of its birth"): under the identity a
  row's state at the click depends on the crowd along its path. Not a
  failure of the test; a line the design must add (should-fix 2). Passes.
- Local: A is a sum over the rows present at the row's own Node; each row's
  age is on its own record; the sum is the Node's, zero hops. Passes.

### 1 (b) The turn by the transverse flow, `w_a += 2 n_s T_D V_a` against `d_s Q^2 THETA`, seeded by the wheel

Symbols: `w_a` the turn accumulator on the row for the transverse axis a,
`V_a` the component of the crowd's flow vector **V** (the sum over the
arrivals of other numbers of amount x their unit vector at the scale Q),
THETA the angle between the row's direction and its neighbour on the fan,
u the record's birth wheel value in `Z_W`, W the wheel's width.

- Generic: one rate and one wall, no name. Two things are undefined for a
  direction off an axis: "the two axes not along the row's direction D" (for
  D = (24, 1, 0) or (1, 1, 1) every axis is along D in part) and "the fan's
  neighbour toward sign(w_a) on axis a" (the 290-direction table has no
  unique neighbour per axis). The design cites the meeting's arc
  permutation `pi_t` for the step, which is toward a TARGET vector by
  sectors, not per axis; the two mechanisms are not the same. Must-fix 2
  asks for one of them, defined in integers. With that, passes.
- Vector: (T) on `w_a` at a rate linear in the flow, (D) the comparison with
  the remainder kept, (P) the step on the fan. THETA is a rounding at load
  (a table per direction, or per direction and arc), of the same kind as
  `T_D` and `u_d`, admissible if it is listed in LAW.md section 6 with its
  grain. But the integers as written are not in one unit: the wall
  `d_s Q^2 THETA` has THETA "scaled once by the declared grain" (an integer
  `THETA_G = round(G x angle)`, G the grain), while the rate `2 n_s T_D V_a`
  is not scaled by G; the turn per interval the design derives,
  `2 (n_s / d_s)(T_D / Q^2) |V_perp|` radians (re-derived below: correct),
  needs the rate `2 n_s T_D G V_a` against that wall, or the wall in the
  rate's unit. A dimensional slip, not a physics one; must-fix 2. The seed
  `w_a = u x d_s Q^2 THETA // W` discards a remainder at run time (at
  birth); it can be made exact by carrying W into the wall and the rate
  (should-fix 6). Passes with must-fix 2.
- Local: **V** is the Node's own reading of its arrivals (the same columns
  `read_arrivals` fills for a body: the flow), zero hops. Passes.
- The SIGN, checked from 5.1: **V** = (q Q / (4 pi r^2)) r_hat points AWAY
  from the source (the stream's flux; the meeting turns "toward the crowd's
  -V"). Verb 2 as written, "w_a += 2 n_s T_D V_a ... the direction label
  steps to the fan's neighbour toward sign(w_a)", turns the row toward +V,
  away from the mass. Section 4 says "the turn is toward -V, the mass". The
  rule's text contradicts its own pin: must-fix 1.
- The turn's magnitude, re-derived: with `V = -(Q c / dwell) grad(A)` (5.1)
  and `c = Q / T_D`, `dwell = T_D / Q`, `grad_perp(A) = -(T_D^2 / Q^3)
  V_perp`; the ray equation `d theta / dl = grad_perp(2 k_a) = 2 (n_s / d_s)
  grad_perp(A)` gives per interval (c Links) `2 (n_s / d_s)(T_D / Q^2)
  |V_perp|`, the design's number; along a straight path past a mass at the
  impact distance b, `2 K_A x integral b / (b^2 + l^2)^(3/2) dl = 4 K_A / b
  = 4 k_a(b)` (K_A = k_a(b) b). The design's arithmetic holds.

### 1 (c) The clock's bilinear term, `owed = by_drive(acc_owed, 2 k n_s d_s + 3 k^2 n_s^2, 2 d_s^2)`

k here is what the clock counted (the presence or the age moment), `k' = k
n_s / d_s`, w the wait per self-creation.

- Generic: one row of the counts table (note 41: "a future count is a new
  row, not new code") with declared integers; no name. Passes. But the
  design leaves its identity open ("Under the same identity or its own"):
  keyed on the pair alone it would change series E (k = 2 to 9 at [1, 1]:
  the added wait `3 k^2 / 2` is 6 to 121 per self-creation, the registered
  rate ratios of 5.2 moved several-fold). It needs the key of must-fix 3
  (or its own), named.
- Vector: (D) with the rate `2 k n_s d_s + 3 k^2 n_s^2`, bilinear in the
  state (k x k), the remainder kept, the wall `2 d_s^2` declared. Passes.
  The bound must be stated: `3 k^2 n_s^2` with k the age moment at a dense
  Node (the nucleon's 57 rows at ages of hundreds: k of order 10^4) and
  `n_s` of the world; a refusal at load or at the frame like the meeting's
  (iv) (should-fix 4).
- Local: the body's own accumulator and its own Node's count, as today.
  Passes.
- Its arithmetic, re-derived: `1 / (1 + w)` with `w = k' + (3 / 2) k'^2` is
  `1 - k' - k'^2 / 2 + ...`, so `1 + z = 1 + k' + (3 / 2) k'^2`; at `k' =
  1 / 16`: 1.0625 + 0.005859 = 1.068359, nature's `1 / sqrt(1 - 1 / 8)` =
  1.069045, the residual 6.9 x 10^-4 against the third order 6.1 x 10^-4.
  The design's numbers.

### 1 (d) The cost against K, and the reading set

The design counts 26 per row read at every Node with a row. Two precisions.
(i) The rule reads five of the moment table's 13 columns (A: the age
outside and here; **V**: three), never the tensor's six or the second count;
computed alone the reading is about 12 per row, the 26 only where a body at
the Node reads the whole table anyway. (ii) The reading set is the SAME set
as the bodies' clock's (note 47: "everything at its Node but its own
number"; `counted` = the presence or the age moment over the rows present of
other numbers), and the same as the meeting's `crowd_flow` (the flow at the
Node less the own number's), so no new set is introduced; what is new is a
second CONSUMER of it at every free-space Node holding a row of more than
one number, which the host computes as the meeting does (two segmented
passes per interval; note 35 (vii) measured the meeting's at 4.6 ms per
interval on `mass`). Per row per interval the model's work is fixed (the
walk 16, the wall 2, the turn 4, the comparisons 2, the reading's share);
against K it is the reading at every such Node that the budget of 13.3
feels, as the design says. Fixed for fixed K: passes; the host cost to be
reported apart at the build.

## 2. LOCALITY-1, the origin of every input

| Input | Owner | Computed by whom, from what, when | Hops | Verdict |
| --- | --- | --- | --- | --- |
| A, the age moment at the row's Node | the Node's reading (no owner at the Node: recomputed per interval) | the host's keyed sum over the rows present at the Node of every number but the reader's, each row's amount and age from its own record; WHEN is not stated (must-fix 5) | 0 | local once the step is named |
| **V**, the flow at the Node | the same reading | the sum of amount x unit vector over the rows that arrived this interval (the arrivals' vectors; a row that did not step contributes the zero vector, as in `read_arrivals`) | 0 | local |
| the exclusion of the own number | the row's record (its number) | a comparison of numbers: the Node's total less the (Node, number) total, `crowd_flow`'s form; the crowd of note 47 exactly | 0 | local, generic |
| `[n_s, d_s]`, the factor, THETA, G | the world (declared), the law (at load) | at load | - | declared |
| `w_a`, the flight's accumulator | the row's record | the row | 0 | local, once the accumulator is a field (must-fix 4) |
| u, the seed | the record | the birth wheel, as the click's | 0 | local |

No estimator, no map, no search, no replay, no neighbour beyond the Node
itself; the six neighbours enter only as the arrivals' origin (LOCALITY-1's
"six causally available neighbour records"). The one open point is the
timing: the walk is step 1 of the interval, the readings step 2, the
meeting's turn after the collision in step 3 (note 35 (i)); a row's wall at
its walk in interval t needs A at its Node BEFORE its step, which is either
the reading of interval t - 1 carried on the row (one more integer) or a
fresh reading before step 1; the turn's permutation belongs where the
meeting's is, on the rows present after the walk. Until the design names
the step and the set, the skill's timing rule ("identify the model tick
being used") is not met: must-fix 5.

## 3. The measurement rule (record 281): which pins are detector readings

| Pin | Kind | Compared with what, of what kind |
| --- | --- | --- |
| the centroid's shift on series K's screen (-4.63, -9.22, -9.22 pixels) | DETECTOR: the 1681 one-Node sets' click counts per pixel, the count-weighted centroid (`tools/lensing_readings.py`, labelled DETECTOR) | with the design's own number in pixels (the same kind: `4 k_a(b) x 26 Links`); with nature by the FORM only (4 k against Newton's 2 k, the factor a ratio), never the 1.75 arcseconds (the fan's grain is 2.4 degrees; the README's own words) |
| the mean age of the arrivals (93.37, 97.30, 94.62 intervals) | DETECTOR: every click record carries the age moment of its group (`reads: "age"` on the screen's `light` entry) | with the design's delay in intervals (the same kind); with nature by the form (a logarithm of `4 r_1 r_2 / b^2`) |
| "the lamp's own rate at r = 26" (0.9898, 0.9799, 0.9899) | GAMEBOARD: the lamp's owed count on its record, a host reading; NOT a measurement | the detector's readings of it are the phase rate at the screen (7.919 ...) and the count ratio; the column must be labelled or dropped (must-fix 8) |
| the second-order term, "a lamp at k' = 1 / 16 read by a clock at k' = 0" | the phase rate read at a detector is DETECTOR; but no clock is at k' = 0 in a world with a mass | restate as the ratio of two detectors' phase rates at `k'_1` and `k'_2` (should-fix 9) |
| Snell, "a beam's centroid past a slab of denser crowd" | DETECTOR in kind; no world is named that makes a slab of crowd | should-fix 5 |

The comparisons with nature in section 1 are of FORM and of one ratio (the
factor), stated so; the absolute values (1.751 arcseconds, 131 microseconds)
are nature's numbers beside the form, not claimed: consistent with record
210 (no Link count is compared with a distance).

## 4. Bit-exactness with the identity OFF, and what changes with it ON

OFF. The arithmetic is silent at `n_s = 0` because the parser records the
pair "off" as `(0, 1)` (`world.py`: "Off: 0 and [0, d] alike, recorded as
[0, 1]"): the wall is then `2 T_D x 1` and the rate `2 S_1 Q x 1`, today's
integers; the turn's rate is 0 and the seed `u Q^2 THETA // W` never reaches
the wall `Q^2 THETA`. So "silent at suspension 0" is a property of the
rule's form GIVEN the parser's convention `d_s = 1` when off (with `(0, 0)`
the wall would be 0): the design should say so. But bit-exactness of the
registered artifacts is NOT a property of the rule: the row's record gains
fields (the two turn accumulators, the flight's accumulator), which would
appear in `state.json`, and the reading at every Node would run in every
world (the host's cost). Only a declaration gates those: the identity key,
absent by default (must-fix 3), under which the fields and the reading
exist only in worlds that declare it. The meeting's precedent is exact here
(note 35 (viii): 85 worlds byte-identical "with the module present and the
key absent").

ON by name, keyed on the pair alone as the design has it: 27 registered
worlds declare a nonzero `suspension` (listed from the checkout:
`catalog/clock_near_mass` [1, 4] and `catalog/neutron_star`;
`coupling/6.json` and `one_content.json` at 1 (ten sources of family m in
the first: each source's rows read the nine others' crowds); `hubble/*` four
worlds at [1, 4096] and [1, 2^19] with 25 sources; `hubble_stars/*` twelve
worlds with 24 lamps whose rows read one another's (light bends light, at
[1, 65536] about 0.5 percent in pace along a crossed beam: the registered z
readings with rms 0.0044 move); `redshift/scalar` and `redshift/age` (6985
events of family m ALL holding content, so "a probe's rows, if any" is to be
checked against their release, should-fix 8); `weak/j1_*`, `weak/j3_*` five
worlds at [1, 2^20] with rows of two or three numbers at one Node). Every
one of them changes unless the key gates the rule. With the key, ON by name
in the pin world: section 4's table (after must-fixes 6 and 7), plus the
consequences section 7 of the design must name (should-fix 3): under the
identity a source's rows read another source's crowd, so 5.5 (ii) "the
fields of two sources add exactly" no longer holds (a slowed row dwells
longer: the presence and the age moment rise by `1 + 2 k_a` where it is
slowed), and a beam of light reads and is read by any other number's rows
at their amounts (the clock's rule today), including another beam.

## 5. The world file: what it must declare, what the engine must refuse

Declare: (i) the identity key, absent by default, carrying the factor as a
declared integer (one integer f, `optical: 2`; or a pair if the design
wants a rational): the wall `2 T_D (d_s + f n_s A)`, the turn's rate `f n_s
T_D G V_a`; (ii) a nonzero `suspension` pair (the rule reads it); (iii) for
the second-order term, the same key or its own; (iv) nothing per world for
THETA and its grain G: constants of the law at load, listed in LAW.md
section 6 beside the fan's weights, the neighbour table built from the
direction table at load; (v) for the pin world, the lamp's entry for the
mass's family as `{"rule": "pass", "reads": "age"}` if the lamp is to count
the age moment (must-fix 6); (vi) a `wave` screen as today. Refuse: the key
with `suspension` 0 (a declared identity that does nothing is the implicit
default AGENTS.md forbids); the key together with `meeting` (two turns on
one row, unless the design states how they compose); a wall or a rate
beyond the register (`2 T_D (d_s + f n_s A_max)` and `f n_s T_D G |V|_max`
within `2^62 - 1`, `A_max` and `|V|_max` from the crowd bound as the
meeting's (iv) does, tested by division before the product); a direction
table whose neighbour table is not defined for some direction (the rest
direction is skipped: **u** = 0 has no transverse axis; state it). Nothing
about a phase circle: the turn's count is on `w_a`, not the phase, so a
phase-less family turns too (an advantage over the meeting, worth one line).

## 6. The numbers: the design's own, or a fit

Re-derived from the design's integers and the README's inputs (q = 290
rows per interval, `dwell = 110 / 64`, b = 6, `[1, 256]`): the presence at b
is `q dwell / (4 pi b^2)` = 1.102 per Node, the age at b is `b T_D / Q` =
10.3 intervals, A = 11.36 (the README's 11.4); `k_a(b) = 11.4 / 256 =
0.0445`; the deflection `4 k_a(b) = 0.178` radians; the shift `0.178 x 26 =
4.63` pixels; the delay `(2 k_a(b) b / c) ln(4 x 26 x 26 / 36)` = 0.5344 /
0.5818 x 4.319 = 3.97 intervals (the exact `2 asinh(26 / 6)` = 4.347 against
the logarithm's 4.319: 0.6 percent, the design's "a few percent" is
conservative); `heavy` 0.0887, 0.355, 9.22, 7.90; `near` 5.22 (ln 300.4 =
5.705); the second order 1.0684 at `k' = 1 / 16` (section 1 (c)); Snell at
`k_2 = 1 / 256`, 30 degrees: `asin(sin 30 / 1.0078)` = 29.744 against `30 -
(0.0078) tan 30` in degrees = 29.742. All reproduced; the script re-run in
the worktree is byte identical to the committed `.out`. The numbers are the
design's own arithmetic, no fit. Two caveats on their inputs: the README's
A at b (11.4, 22.7) is itself a formula (the shell mean), not a measured
number; series E measured `k_a r = 36.1` at [1, 2] for this source, which is
A(6) = 12.0 at [1, 1], 5 percent above 11.4 (a bracket to carry). And the
table assumes the crowd at the beam is the README's static crowd, which
under the rule it is not (must-fix 7).

## 7. The relation to form B (FORM.md section 3, record 301, in build)

Form B makes the body's drive the flight's own accumulator with the wall
`Q S M S_1 Q + |p|_1 T_D` (**p** the momentum vector, S the push's width, M
the content). The design applies "T_D grows wherever it is a wall" (15.5's
sentence for the growing wall) so that the second term becomes `|p|_1 T_D
(d_s + 2 n_s A) / d_s`. Read against the question: the body's slowing in
Nodes per interval is a CONSEQUENCE of two things already decided or under
review, form B (one flight primitive for rows and bodies, "a row the body of
no content") and verb 1 (the primitive's wall reads A), not a second
declaration; and the equivalence principle in the register's sense,
`push_m = m x push_1`, is untouched, since the push (the coupling to the
flow, 3.3) is not changed by the rule. Three things to state exactly.
(i) The Newtonian limit is untouched: at small `|p|_1` the pace is `|p|_1 /
(Q S M)`, the factor acts only through the cap term, so a slow body is
slowed at the order `v / c`, as the design says ("at the order of its
speed"); this is not the isotropic-coordinate slowing of a slow body in
the Schwarzschild metric, which is second order and enters through the
push, not the cap. (ii) Hence the claim "this is the space part acting on a
body, the post-Newtonian correction of order v^2 / c^2 that 5.3 says the law
lacks (the perihelion's three halves)" overreaches: the term is of that
order but nothing here fixes its coefficient; the design itself says "not
computed here"; soften to "a term of that order; its coefficient a run's
reading" (should-fix 7). (iii) The dependence is a build-order fact: today's
`step_axis` is per axis with the wall `Q S M + |p_a|` and carries no `T_D`,
so on main the rule would not touch bodies at all; the body's case holds
only once form B is on main (record 301: ordered, stage 1 and 2). Section 8
must list form B before the build of the body's case (should-fix 7).

## MUST-FIXES (the design, before the build)

1. Section 3, verb 2, the sentence "w_a += 2 n_s T_D V_a per interval (the
   turn accumulator ...); if abs(w_a) >= d_s Q^2 THETA: the direction label
   steps to the fan's neighbour toward sign(w_a) on axis a": as written the
   turn is toward +**V**, away from the mass (**V** is the outward flux of
   5.1; the meeting turns toward -**V**; section 4 says "the turn is toward
   -V, the mass"). Change to `w_a -= 2 n_s T_D V_a` (or the step toward
   `-sign(w_a)`), and say in "The sign and the factor from the integers"
   that the sign is the accumulator's, from **V**'s direction.

2. Section 3, verb 2, the same block and the sentence "with THETA the
   fan's step at the row's direction as a declared integer at load (the
   angle between D and its neighbour on the table, scaled once by the
   declared grain, a rounding at load like T_D and u_d)": (a) put the wall
   and the rate in one unit: `THETA_G = round(G x angle)` with G the grain
   named as a constant of the law, the wall `d_s Q^2 THETA_G`, the rate
   `2 n_s T_D G V_a` (or divide the grain out of the wall; the design's
   derived turn per interval needs one of the two); (b) define, for a
   direction off an axis, "the two transverse axes" and "the fan's
   neighbour toward sign(w_a) on axis a" as a table built at load
   (per direction, axis and sign: the neighbour and its THETA_G), or
   restate verb 2 as the meeting's arc permutation toward the target
   `-V_perp` with `V_perp` formed exactly (`Q^2 V - (V . u) u`, **u** the
   row's unit label), one accumulator against the arc's THETA_G; choose one
   and state its bound; (c) add THETA_G and G to LAW.md section 6's list of
   roundings at load when the design lands.

3. Section 3, "What the rule does not do", the sentence "it adds no new
   pair (the clock's [n_s, d_s] serves) and one integer, the factor 2,
   written into the wall and the turn as the same integer; at suspension 0
   it is silent, so every registered world with suspension 0 (series K
   included) is unchanged bit for bit": the identity needs its own world
   key, absent by default, carrying the factor as the world's declared
   integer (`optical: 2`; the rule reads f, the engine carries no 2, the
   Newton world declares 1), because keyed on the pair alone the rule is ON
   in the 27 registered worlds with a nonzero pair (section 4 of this
   review: catalog, coupling, hubble, hubble_stars, redshift, weak), and
   the second-order term of section 5 keyed on the pair alone moves series
   E several-fold. Rewrite the sentence as: the key gates the rule, the
   row's new fields and the Node's reading; every world without the key is
   byte identical in `events.jsonl` and `state.json`; `run.json` gains the
   key. Add to section 8: the parser refuses the key with `suspension` 0
   and with `meeting` (or states their composition). Section 5: name the
   term's identity (the same key or its own), not "or".

4. Section 3, verb 1's block, and section 6, the sentence "Store per row:
   two integers (the turn accumulators). Store at the Node: none.": with a
   wall read from the state the flight's accumulator is no longer a function
   of the age (`Flight.accumulator` today derives the pair (m, the residue)
   from the age and "the row carries no field for them"); the row's record
   must carry the position accumulator with its residue (the growing wall's
   form), so the store is three integers per row; and the exact phase at
   the click (LAW.md 4.1: `phi = (n / d) x made x T_D / (S_1 Q)`;
   TWO_SLITS.md section 2) must read the row's stored accumulator, since
   the Links made no longer give the time of the last Link. State both, and
   in the vector verdict name the residue's owner (the row's record).

5. Section 3, "The state read at the Node", the sentence "Nothing at the
   Node: the moments are readings of the rows present, recomputed per
   interval": name the step of the interval and the set. The walk is step 1,
   the readings step 2, the meeting's turn after the collision in step 3
   (note 35 (i)); say whether verb 1's wall at the walk of interval t reads
   A from the rows present at the end of t - 1 (then carried on the row: one
   more integer) or from a reading taken before step 1, and that verb 2's
   permutation acts at the meeting's place on the rows present after the
   walk; say which rows' arrivals **V** sums (the crossing rule's set for a
   row is the arrivals at its Node this interval). Every timing claim of the
   pin (the first click, the mean age) depends on it.

6. Section 4, the sentences "The pin world: the same four worlds with
   suspension [1, 256] (the lamp's clock then slowed too ...)" and "the
   lamp's clock at r = 26 slowed by 1 / (1 + k_a) (the phase rate 7.92 and
   7.84 against 8, series E's reading, now on), the count unchanged (no row
   taken)": the lamp's entry in the world files is `{"m": "pass"}` with no
   `reads`, so its clock counts the PRESENCE (`default_reads` gives
   `scalar`; `count_component`), which at r = 26 is `q dwell / (4 pi 26^2)`
   = 0.0587 per Node: `k = 0.0587 / 256`, the rate 0.99977, the phase rate
   7.998, INSIDE the bracket, not 0.9898 and 7.919; if the lamp is to count
   the age moment, the pin world must declare `{"rule": "pass", "reads":
   "age"}` on that entry, and then the births per interval fall with the
   self-creations (the lamp births at its self-creation, `advance("lamp")`),
   so the count ratio is 0.990, 0.980, 0.990, OUTSIDE series K's 1 percent
   bracket in `heavy`: "the count unchanged" is wrong under the design's own
   numbers. Declare the entry, correct the two columns and pin the count
   ratio; and state whether the screen's 1681 clocks, slowed by the same
   crowd at the same pair, change the click's timing (on main the readings
   and the clicks are per interval and the owed count gates only the
   self-creation's acts; to be confirmed by the implementer, not assumed).

7. Section 4, the premise "With the README's age moment at the beam's
   impact distance (11.4 per Node at (2^12, 6); 22.7 ...)": under the rule
   the mass's rows (family m, another number) read the BEAM's rows at their
   amount x age. The beam holds about 447 rows over about 260 Nodes at a
   mean age of 45 (the README's GameBoard readings), so the beam's own age
   moment is A of about 45 to 77 per Node, k = 0.18 to 0.30 at [1, 256]: the
   crowd's rows are slowed by `1 / (1 + 2 k)` = 0.6 to 0.7 inside the beam's
   Nodes, their dwell and so the crowd's presence and age moment there rise
   by that factor, and the A the beam reads is 1.4 to 1.6 times the README's,
   not "one number k_a(b)". The table's shifts and delays are therefore low
   by tens of percent and are not the rule's own numbers for that world.
   Either re-scale the pin world so the beam's own age moment is small
   against the crowd's (for example M = 2^16, sixteen rays per direction per
   interval, at [1, 4096]: the same `k_a(b)` = 0.0445 with the beam's k at
   0.01 to 0.02, a 2 to 4 percent back-reaction, inside the brackets'
   share; the host cost to be measured), or compute the back-reaction in
   the map and pin the corrected numbers; and name the consequence in
   section 7 (a beam refracts the crowd it crosses; two sources' fields no
   longer add exactly, 5.5 (ii)). Nothing in the generic rule exempts the
   crowd's rows, and nothing should; the pin must be honest about it.

8. Section 4, the table's column "the lamp's own rate at r = 26" and the
   sentence "What else the pin world changes and the run must read: the
   lamp's clock at r = 26 slowed ...": the lamp's rate is a GameBoard
   reading (the lamp's owed count, the host's view); by record 281 it may
   stand only labelled so, never as a pin; the detector readings of it are
   the phase rate at the screen and the count ratio (must-fix 6). Label
   every column of the table by kind (the centroid, the mean age, the count
   ratio and the phase rate DETECTOR; the lamp's rate GAMEBOARD or removed;
   `k_a(b)` and the deflection in radians the design's derived numbers, not
   readings). Section 5's pin "a lamp at k' = 1 / 16 read by a clock at k' =
   0": no clock is at k' = 0 in a world with a mass; restate as the ratio of
   two detectors' phase rates at two declared k' (should-fix 9 gives the
   form).

## SHOULD-FIXES

1. Section 6, the cost row "26 per row read": the rule reads five columns
   (A's two, **V**'s three), about 12 per row when computed alone; say which
   is built (the whole table shared with a body at the Node, or the five),
   and report the host's segmented reading apart from the model's count
   (the meeting's 4.6 ms per interval on `mass`, note 35 (vii), as the
   reference).
2. Section 3, the vector verdict: add that under the identity the rows
   leave LAW.md section 5's closed form (a row's state at the click is no
   longer a function of its birth alone; the rows' block gains a
   state-read wall, as the growing wall would give it): one line, so that
   LAW.md's classical-quantum boundary is amended when the design lands.
3. Section 7: add the two-source consequence (a source's rows read another
   source's crowd; 5.5 (ii) changes; Gauss's law of the stream stays exact
   in the steady state, the timing changes), the light-reads-light
   consequence (`lens_meeting`'s two lamps; hubble_stars' 24), and the
   registered worlds at a nonzero pair by group (this review's section 4),
   each "unchanged without the key".
4. Section 5: the bound of `3 k^2 n_s^2` and its refusal; the identity
   named (must-fix 3).
5. Section 5b: name the world that makes "a slab of denser crowd" (a plane
   of sources? a second mass?) or mark the Snell pin "no world yet"; state
   that the boundary in a crowd of `M / r` is never sharp, so the pin is
   the ray equation's, Snell only in the limit of a thin transition.
6. Section 3, the seed `w_a = u x d_s Q^2 THETA // W`: make it exact by
   carrying W into the wall and the rate (`W d_s Q^2 THETA_G`, `W x rate`,
   the seed `u d_s Q^2 THETA_G` whole), so that no remainder is discarded at
   run time; and say that u is the record's, so all the rows of one record
   turn together (the dither is per record, the mean exact over records),
   and that the same u decides the click's cell (a correlation between the
   turn and the click in a `sum` set world; absent in series K's `wave`
   reading; name it and test it, or seed from the wheel's next value).
7. Section 7, the series D bullet: soften "this is the space part acting on
   a body, the post-Newtonian correction ... (the perihelion's three
   halves)" to a term of that order whose coefficient a run reads; section
   8: list form B (record 301) before the body's case in the build order,
   since today's `step_axis` carries no `T_D`.
8. Section 7, the series E bullet "a probe's rows, if any": the 6985
   events of family m all hold content at `release` [1, 4096]; compute from
   their amounts whether any releases a row within the run and state the
   answer, not "if any".
9. Section 5, the pin: `1 + z = (1 + w_1) / (1 + w_2)` between two clocks at
   `k'_1` and `k'_2` read at a detector (two lamps, one screen: the ratio of
   the phase rates), with the weak-field world's integers named (a source
   whose age moment at the near lamp gives `k' = 1 / 16` and at the far one
   `k'` small), and the bracket from the ripple of the shell mean (5.2).
10. Section 4, the mass's capture: under the meeting 122 and 169 rays
    clicked on the mass in `mass` and `near` and moved the centroid by 1.2
    pixels (note 35 (ix)); under the rule the turn before x = 28 lowers a
    ray by up to about `theta b / 2`; state the expected rays taken by the
    mass per world (or 0 with the geometry) so that the centroid's bracket
    is honest.
11. Section 6 and the generic verdict: one line that the rule reads
    amounts, as the clock does, whatever the read family's column; that is
    the law's clock today, and the reviewer flags it as the owner's choice
    (the meeting weights by the column sum instead).
12. Notation: `pi_t` is named ("the arc permutation") only by reference to
    the meeting; name it at its first use in section 3; `V_perp` first
    appears in section 3 without its name ("the flow's component
    transverse to the row's direction").

## THE PINS THE BUILD MUST MEET (quoted, with the section)

To be recomputed under must-fixes 6 and 7 before the run; the FORM pins
stand as written.

- Section 3: "at suspension 0 it is silent, so every registered world with
  suspension 0 (series K included) is unchanged bit for bit" (to become:
  every world without the key, `events.jsonl` and `state.json`).
- Section 1: "Series C's field pair (the presence M / r^2 and the age
  moment M / r from the same rays, k_s r^2 = 41.5, k_a r = 36.1), the
  equivalence principle (push_m = m x push_1), Gauss's law exact, and
  every registered world with suspension 0 bit for bit."
- Section 4, the table, as stated: "`mass` | 2^12 | 6 | 0.0445 | 0.178 |
  -4.63 | 3.97 | 93.37", "`heavy` | 2^13 | 6 | 0.0887 | 0.355 | -9.22 |
  7.90 | 97.30", "`near` | 2^12 | 3 | 0.0887 | 0.355 | -9.22 | 5.22 |
  94.62" (the shift's bracket 0.5 pixel, the delay's 1 interval).
- Section 4: "Every shift and every delay is outside series K's bracket,
  toward the mass and later, and the two grow together with k_a(b) as one
  number: that is the pin's signature."
- Section 4: "with the factor 1 (Newton's index) every shift and every
  delay above is halved" (the factor-1 world as the control of the factor).
- Section 4: "the mean turn is 4.3 steps of 2.4 degrees in mass and 8.5 in
  heavy and near, so every ray turns whole steps and the wheel's dither
  sets which rays turn one more (34 and 63 of 122)".
- Section 4: "the count unchanged (no row taken), the light on the faces
  unchanged" (the count to be re-pinned per must-fix 6).
- Section 5: "at k' = 1 / 16 the law today 1.0625, with the term 1.0684,
  nature's 1.0690, the residual 6.9 x 10^-4 = the third order".
- Section 5b: "at k_2 = 1 / 256 (n_2 = 1.0078) and theta_1 = 30 degrees
  Snell gives 29.744 and the rule 29.742; at k_2 = 1 / 16 (n_2 = 1.125) and
  30 degrees, 26.388 against 25.865".
- Section 7, series D under form B: "a moving body's pace in Nodes per
  interval falls in the potential as a row's does" (a run's reading, no
  number pinned).

## What this review did not do

No run beyond the map script; no fit; no new physics; no edit to any
repository file. The verdict is on the design's form against the three
tests, LOCALITY-1 and the measurement rule; whether nature's factor 2 and
logarithm then appear on series K's screen is the run's to say, after the
owner's go and the must-fixes.
