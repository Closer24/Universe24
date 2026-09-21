# Physics-rule review of `optical-v1`, second round: does the amendment close the eight must-fixes

Read-only review, the physics-rule reviewer, 2026-09-21. The object: the
branch `claude/series-m-masses` at its head 267d1df9 (one commit over main
at 6f2f2a34: `docs/designs/gr_rows/DESIGN.md` amended, `gr_rows_map.py`
re-run, `gr_rows_map.out`), read in a detached worktree; nothing edited,
nothing run beyond the map script (re-run in the worktree with the
repository's venv: byte identical to the committed `.out`, sha256
`03b29962...412743` on both). Read first: the first round
(`optical_review_REVIEW.md`, ADMISSIBLE WITH MUST-FIXES, eight must-fixes
and twelve should-fixes), then the amended design section by section with
its "amended per the review" notes, against BEAM_LAW.md section 3 (the
interval's order), notes 47 and 48 (the reading set, the crossing rule's
marks), note 45 read from `origin/click` (the exact phase at the click; it
is on neither main nor this branch), designs/vector_form/LAW.md 4.1, 4.2 and
6, DERIVATIONS_BEAM.md 5.1 and 5.2, records 156, 163, 299, 301, 302 and 303,
the lensing README and `mass.json`, and the code the build would touch
(`Flight.accumulator` and `walk_step`, the store's FIELDS with `arrival`,
`read_arrivals`, `crowd_flow`, `meet`'s call site, `count_component`, the
clock's `counted`, `engine._frame_all`, `_suspend`, `count_owed`, the
click's `admit()` in step 4 and the `creating` gate of step 5). Every symbol
is named at its first use; a scalar plain, a vector in bold lowercase.

## VERDICT: BUILDABLE (the build may start after form B lands, under the owner's go of record 303)

All eight must-fixes are CLOSED: 8 CLOSED, 0 PARTLY, 0 OPEN. The amended
rule passes the three tests (one paragraph each below), its every input is
local by LOCALITY-1 with the step of the interval now named, its pins are
labelled by kind, and its numbers are its own arithmetic (the map reproduced
byte for byte, the key numbers re-derived below by hand). What remains is a
short list of precisions for the build (should-fixes, none a physics gap):
two build-order names missing from section 8 (the click branch, record
299's array primitive), the exact-phase formula the build must write, the
wheel's width as the law's, the back-reaction range labelled as the
first-order estimate it is, and one distance.

## The eight must-fixes, one by one

### 1. The sign: CLOSED

The closing sentence (section 3, verb 2): "per interval: w -= f n_s T_D G
(Q^2 V - (V . u) u) (the turn accumulator w, three integers; the minus is
V's direction: the flux points away from the source, the turn is toward
it)", and section 4: "the sign is the accumulator's, w -= ... V, from V's
direction (the flux points away from the source, 3.4 and 5.1), so the step
is toward the mass, negative in y on the screen".

Derived in two lines. Symbols: **V** the crowd's flow at the row's Node (the
sum of amount times the unit vector at the scale Q over the arrivals),
**u** the row's unit label (|**u**| = Q), **w** the turn accumulator, f the
world's factor, `[n_s, d_s]` the suspension pair, `T_D` the direction's
resolution, G the angle's grain, **t**(D, D') the transverse unit from the
direction D toward its fan neighbour D' at the scale Q.
(i) By 5.1 the flux is **V** = (q Q / (4 pi r^2)) **r_hat** with **r_hat**
from the source to the Node, so at a row on the beam's line (the lamp at y =
26, the mass at y = 20 in `mass.json`: the row 6 above the mass) the
transverse part `Q^2 V - (V . u) u` = Q^2 **V**_perp has a positive y
component: it points away from the mass.
(ii) `w -= f n_s T_D G (Q^2 V - (V . u) u)` makes `w_y` grow negative; the
neighbour D' whose **t**(D, D') has a negative y component gives `p = w .
t(D, D') > 0` and reaches the wall first, and the label steps to D', which
lies lower in y: toward the mass. On the screen (the README: "a deflection
toward the mass is negative in y") the centroid's shift is negative: the
map's -4.63, -9.22, -9.22. The script writes the minus by that convention
in its format string (`-{shift:.2f}`), so the sign in the `.out` is the
text's derivation, not the script's arithmetic; acceptable for a map, and
the run's centroid is the number that carries it.

### 2. The units, one unit: CLOSED

The closing sentences (section 3, verb 2): "G the grain of the angle, a
constant of the law at load (2^16); THETA_G(D, D') = round(G x angle(D,
D'))" and "The units are one: |w| grows by G d_s Q^4 times the angle turned
per interval, f (n_s / d_s)(T_D / Q^2) |V_perp| radians ..., and the wall
along t is G d_s Q^4 times the neighbour's angle; the wall's division by W
is exact because Q^5 = 2^30 is a multiple of W = 2^12".

Verified. With |**u**| = Q, `|Q^2 V - (V . u) u| = Q^2 |V_perp|`, so per
interval `|delta w| = f n_s T_D G Q^2 |V_perp| = G d_s Q^4 x [f (n_s / d_s)
(T_D / Q^2) |V_perp|]`, the bracket the angle per interval of the first
round's re-derivation (from **V** = -(Q c / dwell) grad A, c = Q / T_D,
dwell = T_D / Q). The wall: `p = w . t >= d_s Q^5 THETA_G` with |**t**| = Q
is `|w along t| >= d_s Q^4 THETA_G = G d_s Q^4 x angle(D, D')` up to the
rounding: the rate and the wall are in the one unit `G d_s Q^4 x radians`.
The remainder subtracted at a step, `|t d_s Q^3 THETA_G| = d_s Q^4
THETA_G`, is the same unit and the full step's worth, so the dithered wall
`(W - u) / W` decides only WHEN the step falls, not how much is removed:
the mean over records exact, as the click's rung. The divisibility: `Q^5 =
64^5 = 2^30`, `W = 2^12`, `Q^5 / W = 2^18`, so the row's wall `(W - u) d_s
2^18 THETA_G` is whole for every u in `Z_W`: no remainder at birth.
`THETA_G` at the light's step: `round(2^16 x atan(1 / 24)) = 2729`
(checked). The register: `f n_s T_D G Q^2 |V| <= 2^62` gives `|V| <= 7.8 x
10^7` at `n_s = 1` (checked: `2^62 / (2 x 110 x 2^16 x 2^12)`); `d_s Q^5
THETA_G = 4096 x 2^30 x 2729 = 1.2 x 10^16`, inside.
Is `round(G x angle)` a declared rounding or a float in the rule? A
declared rounding at load, of the same kind as the C and S tables of N
(cos and sin at load, `core/phase.py`) and the fan's weights at G (LAW.md
section 6): it is formed once from the direction table's integer vectors,
never at run time, and the design says it is to be listed in LAW.md section
6 when it lands. The rule itself carries no float. Record 156 is the wheel's
and the exact phase's record; the standard the design cites for the
rounding is LAW.md section 6 (record 168's inventory), the right one.
One precision (should-fix A): the wheel on main is `u = (births - 1) mod
N` (nature_beam.py:3936), N = 64 = 2^6 in series K; `W = 2^12` at the
golden rate is note 46 on the click branch (PR #457). The claim holds for
any power-of-two wheel up to 2^30; the design should say "W the law's wheel,
a power of two", so the build is right on whichever wheel main carries.

### 3. The key `optical: f`: CLOSED

The closing sentences (section 3): "The identity is declared by one world
key, `optical: f`, absent by default: f the factor, a declared integer of
the world (the pin world declares 2, the Newton world 1); the engine
carries no 2. The key gates the rule, the row's new fields and the Node's
reading: a world without the key is byte identical in `events.jsonl` and
`state.json` (the meeting's precedent, note 35 (viii)); `run.json` gains the
key. Under the key the second-order term of section 5 is on as well."
Section 5: "under the same key `optical`". Section 7: "Without the key
nothing changes: every registered world is byte identical ..., including
the 27 worlds with a nonzero `suspension` pair (by group: ...)".

Is byte-identity a property of the design or a claim the build must test?
Both, and the design states both: a property (with the key absent no field
is added to the store, no reading is taken before step 1, `Flight`'s wall
is today's `2 T_D`, `count_owed` is today's row; the parser's `(0, 1)`
convention when off is no longer needed for silence, since the key gates
the code path, not the arithmetic) and a test, stated in section 8 (3):
"`state.json` and `events.jsonl` byte identical without the key on the
85-world set" (the meeting's gate, note 35 (viii)). The refusals, all five
stated (section 3 "What the engine refuses" and section 8 (3)): the key
with `suspension` 0; the key with `meeting`; f not a positive integer; a
wall or a rate beyond the register (the bounds of must-fix 2, tested by
division before the product, refused naming the Node); a direction table
whose neighbour table is not defined for some direction. Section 5 names
the term's identity as the same key, not "or".

### 4. The position accumulator a row field, the click's exact phase reading it: CLOSED

The closing sentences (section 3, verb 1): "The accumulator is a field of
the row's record with its residue (today `Flight.accumulator` is a function
of the age and the row carries no field for it; with a wall read from the
state it cannot be), the residue's owner the row's record; and the exact
phase at the click (LAW.md 4.1 ...) reads the row's stored accumulator for
the fraction of the last Link, since the Links made no longer give the
time: one read at the click, no extra cost per interval." Section 6: "Store
per row: four integers (the position accumulator with its residue, the
three of w)."

Consistent with note 45 (read from `origin/click`): note 45's click takes
three Euclidean divisions, of which (1) and (2) re-read `made` and the
walk's whole part off the age "never held on the row", and (3) is the one
division of the click with its remainder kept. Under the key (1) is no
longer off the age; it is the stored count m, and the time of the last
Link is no longer `made T_D / (S_1 Q)`. What replaces it, which the build
must write and the design states only as "reads the row's stored
accumulator" (should-fix B, one formula): with the accumulator (m, s) on
the row after this interval's carry (s the residue, r = `2 S_1 Q d_s` the
rate), the last Link was crossed at the fraction `1 - s / r` of the
interval, so the time of the last Link is `age - s / r` and the exact phase
is `phi = floor(n (age r - s) / (d r)) mod N`: still ONE division at the
click with its remainder kept, the numerator `n (age r - s)` within the
register (`r <= 2 x 6 x 64 x 4096` on series K's fans, age within
`age_bound`), and the wall of the interval is not needed after the carry.
Note 45's form is preserved. Consistent with note 48's marks: the row's
`arrival` is a store column (nature_beam.py FIELDS, written at the walk's
end, line 2549), the one-interval fact of the row's own record that the
flow **V** reads (must-fix 5). The carry stays 0 or 1 per interval: `2 S_1
Q d_s <= 2 T_D (d_s + f n_s A)` since `S_1 Q <= T_D` and A >= 0.
Section 8 (3) lists the row's four fields and the click's read. One
build-order fact for section 8 (should-fix C): note 45's `exact_phase` is
on PR #457, not on main at 6f2f2a34; form B's build merges main "when the
click (PR #457) and the architect's array-form primitive (record 299)
land", so "after form B lands" covers it transitively, but the design
should name it.

### 5. The step of the interval and the set: CLOSED

The closing paragraph (section 3, "The step of the interval"): "the Node's
moments A and V are read once at the start of the interval, before step 1,
from the rows present at the end of the interval before (their ages and
amounts on their own records, their arrivals of that interval); verb 1's
wall at the walk of step 1 reads that A; verb 2's turn acts at the
meeting's place, after the collision in step 3, on the rows present after
the walk, reading the same V; nothing is carried on the row between
intervals but its own accumulators. So a row's wall in interval t is the
crowd of t - 1 at its Node, one interval retarded, as a body's push is."

Consistent with BEAM_LAW section 3's order (the walk 1, the readings 2,
the collision then the meeting 3, the detectors 4, the self-creations 5,
the border 6) and with note 48's engine order (the frame, `_move`, the law,
the clocks' turn and the count owed). LOCALITY-1: A is read from the ages
and amounts on the rows' own records, **V** from their `arrival` columns
(the walk of t - 1 wrote them; the walk of t overwrites them at its end,
line 2549, so before step 1 they are t - 1's), both at the row's own Node,
zero hops; the Node holds nothing between intervals; the interval's host
arrays (the keyed sums, as the meeting's) are the interval's frame,
recomputed. The turn at the meeting's call site (nature_beam.py:2573, after
the collision) reads the same per-Node **V** of that frame for the rows
present after the walk. One precision, immaterial to the numbers
(should-fix D): between "the end of the interval before" and nature_beam's
step 1 the engine's `_move` may add rows (a release at a body's step, a
contact's give), each at age 0 without an arrival, so each contributes 0 to
A and the zero vector to **V**; the two readings coincide, and the design
may say so in one line so the build has no choice to make.

### 6. The lamp's reads declared, the count ratio pinned, the 1681 clocks: CLOSED

The closing sentences (section 4): "the lamp's entry for the mass's family
declared `{"rule": "pass", "reads": "age"}` so that its clock counts the
age moment (today `{"m": "pass"}` counts the presence)"; "the lamp's
self-creations slowed by 1 / (1 + k_lamp) ... and with them its births, so
the count ratio at the screen is 0.990, 0.980, 0.990 (DETECTOR), outside
series K's 1 percent bracket in `heavy` by the pin world's own declaration
(series E's clock slowing, on by `reads: age`) and not by the rows' rule";
"whether the screen's 1681 clocks, slowed by the same crowd at the same
pair, change the click's timing (...) is the implementer's to confirm, not
assumed here."

Checked against the world file and the code: `mass.json`'s lamp has
`"table": {"m": "pass"}` and `count_component` gives the presence for any
entry not reading `age`, so the declaration is needed and is the right key.
The distinction is sound: the count ratio's cause is the clock's rule of
5.2 (the owed count, `_suspend` with `count_owed` at the pair), which the
world switches on by declaring the pair `[1, 4096]` and `reads: age`; the
rows' rule changes no birth. Series E's slowing at `[1, 4096]`: `k_lamp` =
0.010 to 0.020, the weak field where the first-order line `1 / (1 + k)`
holds without the shell ripple that series E met at k = 2 to 9, so the
0.990 and 0.980 are the clock's own numbers. The rows' rule does not touch
the count in the window either: the README reads the count "in the window
[110, 400]", and the delayed first click (tick 90 plus 4 to 8) falls before
110, so the window is in the steady state where the arrival rate equals the
release rate (a static crowd stretches no stream). The pinned kind:
DETECTOR (the screen's clicks in the window against the control's). The
1681 clocks: an OPEN ITEM by the design's own words, stated as the
implementer's, which is what the first round asked ("to be confirmed by the
implementer, not assumed"). My reading of main, for the build's test and
not in place of it: the click's admission (`admitted = admit()`,
nature_beam.py:3002, step 4) is outside the `creating` gate, which covers
only step 5's self-creations (line 3631: the lamp, the releases, `become`)
and the frame's turn and owed count in the engine; the `wave` reading's
pointer and phase are the rows', not the detector's own phase. So on main a
screen clock's owed count gates none of its clicks, and the count ratio and
the mean age stand. It matters: a beam pixel counts about 90 per interval
(one row at age 89 to 90, `reads: age` on `light`) over 4096, so it would
owe one interval in 46, a 2.2 percent hole in the count if the click were
gated; the build's test should pin a slowed one-Node detector's clicks
equal to an unslowed one's. One distance (should-fix E): the lamp at [2,
26, 20] and the mass at [28, 20, 20] are 26.7 Links apart, not 26; `k_lamp`
by `A ~ 1 / r` is 0.0100 and 0.0199 (0.0102 in `near`), the rates 0.9901,
0.9805, 0.9899: the same at the three decimals pinned, so the pin stands;
the map's `r = 26` should be `sqrt(26^2 + b^2)`.

### 7. The pin world re-scaled, the back-reaction as a range: CLOSED

The closing sentences (section 4): "The pin world: the same four worlds
with the key `optical: 2`, the pair `[1, 4096]`, the mass sixteen times the
registered (M = 2^16 and 2^17 ...)"; "the mass's rows (another number) read
the beam's rows at their amount times age, A of about 45 to 77 per Node
(the README's GameBoard readings of the beam), `k_beam` = 0.011 to 0.019 at
`[1, 4096]`, so the crowd's rows inside the beam are slowed by `1 / (1 + 2
k_beam)` = 0.978 to 0.964 and the A the beam reads there is 1.022 to 1.038
times the static crowd's: a back-reaction of 2 to 4 percent, carried below
as a range".

Re-derived from the design's integers: the mass scaled by 16 scales the
crowd's age moment at b by 16 (the same rows at sixteen times the amount,
or sixteen rows, `amount x age` either way): `A(6) = 16 x 11.4 = 182.4`,
`k_a(b) = 182.4 / 4096 = 0.0445`; `A = 16 x 22.7 = 363.2`, `k_a(b) = 363.2
/ 4096 = 0.0887`: the values first pinned. The lamp is NOT scaled, so the
beam's own age moment stays the README's GameBoard reading, 45 to 77 per
Node (447 rows over about 260 Nodes at the mean age 45, the age at the
mass's plane `26 x 1.72 = 44.7`), `k_beam = 45 / 4096 = 0.0110` to `77 /
4096 = 0.0188`; the crowd's pace inside the beam `1 / (1 + 2 k_beam)` =
0.9785 to 0.9638; the dwell up by the inverse, 1.0220 to 1.0376: the 2 to 4
percent. The map re-run reproduces all of it byte for byte. Is the range a
derived bound or an estimate? A first-order ESTIMATE from a GameBoard
reading, not a derived bound: it takes the crowd's flux through the beam as
unchanged (Gauss exact in the steady state, true) and scales the crowd's
presence and age moment at the beam's Nodes by the dwell's rise (true to
first order); it omits the crowd's age gained through the slowed segment
(about five Nodes at `2 k_beam` slower, 0.1 to 0.2 intervals on ages near
10: one to two percent more on A, the same order as the range) and the
crowd's turn by the beam's transverse flow (|**V**_beam| of order Q per Node
per interval gives `8 x 10^-4` radians per interval, negligible). Both
numbers are labelled (the static one and the range) and the range sits
inside the brackets (0.10 to 0.35 pixel against 0.5; 0.08 to 0.30 intervals
against 1), so the pin holds whether or not the estimate is exact. What the
design should say in one line (should-fix F): the range is a first-order
estimate; the run's GameBoard reading of the beam's age moment at the
mass's plane (a diagnostic, labelled) replaces it, and the detector pin is
the static number with the range as the bracket's share. The consequence is
named in section 7 (a beam refracts the crowd it crosses; two sources'
fields no longer add exactly).

### 8. Every column by kind, the second-order pin as two detectors: CLOSED

The closing sentences: section 4's table header, "`k_a(b)` (derived) | the
deflection, radians (derived) | the centroid's shift, pixels, DETECTOR (the
bracket 0.5) | ... | the lamp's clock rate at r = 26, GAMEBOARD | the count
ratio, DETECTOR (the bracket 1 percent) | the phase rate, DETECTOR (8
registered)"; section 5: "The pin, as a detector reading: two lamps at
`k'_1` and `k'_2` beside one source, read at one screen, the ratio of their
phase rates `(1 + w_1) / (1 + w_2)` (... at `k'_1 = 1 / 16` and `k'_2 = 1 /
256` the ratio today 1.0584, with the term 1.0642, nature's ... 1.0649, the
residual `6.8 x 10^-4`, the third order ...)".

Checked: the lamp's rate stands labelled GAMEBOARD and is not a pin; the
detector readings of it (the count ratio, the phase rate) are the pins.
The second-order pin: the screen's own clock is in the same potential and
cancels in the ratio of two lamps' phase rates read at one screen, so the
pin is a DETECTOR reading and needs no clock at `k' = 0`. The numbers by
hand: today `(1 + 1 / 16) / (1 + 1 / 256) = 1.05837`; with the term `w_1 =
0.0625 + 1.5 x 0.00390625 = 0.068359`, `w_2 = 0.00390625 + 1.5 x 1.526 x
10^-5 = 0.0039291`, the ratio 1.064178; nature `sqrt((1 - 2 / 256) / (1 - 2
/ 16)) = sqrt(1.133929) = 1.064861`; the residual `-6.8 x 10^-4` against the
third order `(5 / 2)(1 / 16)^3 = 6.1 x 10^-4`: named and of the right size.
The map's rows at 1 / 64 and 1 / 1000 show the residual falling as `k'^3`
(`-9.8 x 10^-6`, `-2.5 x 10^-9`): the term is second order exactly.

## The three tests on the amended rule

**Generic: PASSES.** One primitive at every Node and every direction: a
wall and a turn read off two moments (A the age moment, **V** the flow) of
the one reading set of note 47 (the rows present at the row's Node less its
own number, by a comparison of numbers as `crowd_flow` makes it). Its
declared integers are the world's `[n_s, d_s]` and f, and the law's
`THETA_G` and **t** at load from the direction table; no family name, no
branch on a kind, no constant hidden in the engine (the 2 of the first draft
is now the world's f, and the Newton world declares 1). A body under form B
is the case with content, served by the same wall; a phase-less family
turns, since the count is on **w**. The rule reads amounts whatever the
column, the clock's rule today and the owner's choice, stated so.

**Vector: PASSES.** Verb 1 is (T) on the row's position accumulator at the
constant rate `2 S_1 Q d_s` against the wall `2 T_D (d_s + f n_s A)`, a
count read from the state, the growing wall's form of 15.6 with the residue
owned by the row's record; verb 2 is (T) on **w** at a rate linear in
**V** (the projection `Q^2 V - (V . u) u` exact in integers), (D) one
comparison per fan neighbour with the remainder kept, and (P) the arc step
to D', the wall and the rate in one unit and the birth's dither whole
(`Q^5 / W` an integer); the second-order term is (D) with a rate bilinear
in the state, `2 k n_s d_s + 3 k^2 n_s^2` over `2 d_s^2`. No root, no float
at run time; the one rounding, `THETA_G` and **t**, is at load and named for
LAW.md section 6. One small leak, not a failure: after a step **w** keeps a
component along the new **u** (the old transverse direction is 2.4 degrees
off the new one), never read and bounded by the steps made times `sin 2.4
degrees` of a step; the build may note it.

**Local: PASSES.** The row reads its own record (its accumulators, its
label, its number, its `arrival`) and the moments of the rows present at
its own Node, formed from their own records (ages, amounts, `arrival`),
zero hops; the six neighbours enter only as the origin of the arrivals
(LOCALITY-1's causally available records); the reading is taken once per
interval before step 1 and held in the interval's frame, and the Node keeps
nothing between intervals. The work per row per interval is fixed for fixed
K (the walk 16, the wall 2, the turn 10, two per neighbour over four to six,
3 at a step) and the reading's share is the same segmented pass the meeting
makes, its host cost reported apart (section 6).

## Section 8, the build's places in order, and what each must not touch

The design names the places (section 8 (3)) and the one dependency (form B,
(1)); it does not say what each place must not touch. Stated here for the
build, in the design's order:

1. Form B on main first (record 301; it merges main after PR #457 and record
   299's primitive land, so both are on main by then).
2. The owner's go (record 303, given for the amended design) and this
   re-read: given by this verdict.
3. The build, each place with its boundary:
   - the key's parser (`world.py`): adds `optical` and its five refusals;
     must not change the parsing of `suspension`, `meeting` or the tables;
   - the neighbour table with `THETA_G` and **t** at load: beside the fan's
     weights; must not touch the flight table (`T_D`, `u_d`, the lines) nor
     the collision table;
   - the row's four fields: added to the store under the key only; must
     not change the meaning of any existing column (`arrival`, `age`,
     `phase`) and must leave `state.json` the same bytes without the key;
   - the reading before step 1: a keyed `read_arrivals` over the store's
     rows for A and **V** per (Node, number); must not touch
     `read_arrivals` itself nor step 2's readings for the bodies;
   - the wall in `Flight`: through the architect's `by_drive_rows` (record
     299, the array form of the one count primitive) with the wall a
     per-row array; must not touch the primitive nor `Flight`'s form
     without the key (bit-exact on the gate set);
   - the turn at the meeting's call site (nature_beam.py:2573, after the
     collision): its own function beside `meet`; must not touch `meet` or
     `crowd_flow` (the key with `meeting` is refused, so the two never run
     together);
   - the click's exact phase reading the stored accumulator: in note 45's
     `exact_phase` (PR #457) with the formula of must-fix 4 above; must not
     touch the click's other divisions, the ladder or the wheel;
   - the second-order term as a row of the counts table (`count_owed`,
     `_suspend`): under the key only; must not touch the owed count's form
     without the key, and must not touch form B's drive (`step_axis` today,
     the body's Manhattan accumulator under form B): the body's case of
     verb 1 enters through form B's wall `|p|_1 T_D` by the same factor at
     the cap term and nothing else in the drive changes.
   - the gate: `state.json` and `events.jsonl` byte identical without the
     key on the 85-world set, as stated.
4. The runs as stated: series K's four worlds re-scaled at `[1, 4096]` with
   `optical: 2` and with `optical: 1` as the factor's control; a weak-field
   world with two lamps for section 5's ratio; the host cost apart.

## Snell

Stated as asked: "No world yet makes a slab of crowd: a crowd of `M / r`
has no sharp boundary, so the pin as it stands is the ray equation's, and
Snell's form holds in the limit of a thin transition" (section 5b), with
the first-order form derived, the exact `1 / n` named and left out, and the
numbers the map's. No world is claimed; the pin is the ray equation's.

## Should-fixes (precisions for the build; none a must-fix)

A. Section 3, verb 2: "W the wheel" should read "W the law's wheel, a power
   of two (N on main today, 2^12 under note 46)"; the divisibility holds
   for either.
B. Section 3, verb 1: write the click's formula, `phi = floor(n (age r - s)
   / (d r)) mod N` with (m, s) the stored accumulator and `r = 2 S_1 Q
   d_s`, one division at the click with the remainder kept (note 45's
   form); today's `made T_D / (S_1 Q)` no longer gives the time.
C. Section 8: name PR #457 (note 45's `exact_phase`, note 46's wheel) and
   record 299's `by_drive_rows` as places the build stands on, covered by
   "after form B lands" but not said.
D. Section 3, the step: one line that rows born in `_move` of the same
   interval (age 0, no arrival) contribute 0 to A and **V**, so the reading
   before step 1 equals the reading of the rows present at the end of the
   interval before.
E. Section 4 and the map: the lamp's distance from the mass is `sqrt(26^2 +
   b^2)` = 26.7 and 26.2, not 26; the rates 0.9901, 0.9805, 0.9899, the pins
   unchanged at three decimals.
F. Section 4: label the back-reaction range a first-order estimate from a
   GameBoard reading, replaced by the run's own reading of the beam's age
   moment at the mass's plane (a diagnostic); the detector pin the static
   number with the range as the bracket's share.
G. Section 3, verb 2: one line on the along-**u** component **w** keeps
   after a step (never read, bounded, second order in the step's angle).
H. Section 4: the host cost "about sixteen times series K's" is an upper
   bound; sixteen rays per direction born in one interval with one phase
   merge into one row of amount 16, so the rows may be near series K's;
   "to be measured" stands.

## What this review did not do

No run beyond the map script; no fit; no new physics; no edit to any
repository file. The verdict is on the amended design's form against the
three tests, LOCALITY-1 and the measurement rule, and on whether each
must-fix of the first round is closed by a sentence of the text. Whether
nature's factor 2 and logarithm appear on the re-scaled series K screen is
the run's to say.
