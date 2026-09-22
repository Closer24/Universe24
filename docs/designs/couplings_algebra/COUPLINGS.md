# The couplings of the atom worlds and the light worlds: every rule the engine runs for them, as one of the six verbs on the GameBoard (the Couplings Definer, 2026-09-22)

The owner's word (record 929 of [the log](../../LOG_2026-09-20.md),
2026-09-22, as the Boss relayed it): "See whether the atom test or the
light tests need new definitions that define the algebraic couplings
there, and express that in the code it is only algebraic operations on
the GameBoard, since we have no other operations on the board; then the
system is very simple." The Boss's bounded order: one table of every
coupling the atom worlds and the light worlds exercise, each row with
its name in [TERMINOLOGY.md](../../TERMINOLOGY.md) today (or MISSING),
which of the six verbs it is, its declared integers and bounds, the
function and lines in the code, the world key that turns it on, and the
design that gave it; then the three tests per row (generic / vector /
local) as the code has it. Docs only; no engine line, no key, no world,
no pin moved; every number and name below is read from the files named,
none invented.

Base: `origin/main` at `8fa9e00b` (PR #849 merged). The files read: the
physical path `src/event_universe/events/nature_beam.py`, `meeting.py`,
`engine.py`, `world.py`, `amplitude.py`, with `measured.py`,
`core/integer.py` and `core/phase.py` where a rule's primitive lives; the
atom worlds `examples/events/atoms/` (hydrogen_r12, helium_r12) with
[ALGEBRA.md](../atom_algebra/ALGEBRA.md) and the baseline run
[RUN.md](https://github.com/Closer24/Universe24/blob/01e8618379c1d54e696ce3c7d6a8f9bb2fd1fe21/docs/designs/atom_baseline/RUN.md)
(branch atom-baseline-run at 01e86183); the light worlds
`examples/events/optical/`, `lensing/`, `two_slits.json`, `one_slit.json`,
`amplitude/slits_*.json`, `massive_rows/slits_matter*.json` with
[STEP_ALGEBRA.md](../light_bending/STEP_ALGEBRA.md) and
[flow_weight/DESIGN.md](../flow_weight/DESIGN.md); the contract
[ARCHITECTURE.md, the operations of the law](../../ARCHITECTURE.md#the-operations-of-the-law);
[ENGINE.md](../../ENGINE.md); records 817, 894, 920 and 929. Every line
number is of `origin/main` at the base commit and moves with the next
edit of the file; the function's name is the durable pointer.

**The six lines (the report's head; every number here is a declared
integer of a world file or a constant of the code, GAMEBOARD; no click
is read).**

1. *The information.* Nothing moves: the table names, for the atom
   worlds and the light worlds, every rule the engine runs, what it
   reads (a body's own record; the rows at its Node or its set, less
   its own number; under `optical` the crowd at a row's Node, less its
   own number), what it writes (one accumulator or one label of its
   own record, or the row's direction), across which Link (the walk's
   one Link per interval; a body's one Link per self-creation), at what
   rate (each row's rate against its wall), what is kept (the remainder
   on the record) and what is lost (a coincident fire of a later axis
   on the per-axis drive; the count of the action row at a Link not
   crossed; the sub-unit residue at a push under `optical`).
2. *The generic solution.* One primitive per row of the table and no
   family name: every coupling these worlds run is the translation of
   an accumulator by its rate with the whole part taken and the
   remainder kept (`core.integer.by_drive`, `by_drive_rows`), the
   bilinear form with a declared matrix (the columns' signs, the
   labels' weights, the Gram matrix), the group-ring addition (the sums
   over a Node, a set or a record), the permutation (the Link, the
   collision's shift, the meeting's arc, the fan neighbour, the split's
   directions), the evaluation (the pointer, the stamp of a phase) or
   the Euclidean division (every whole part, the ladder's rungs); the
   special cases are values of the family table (the quantum 0 or not,
   the flag `massive` read into a table at load) and never a name.
3. *Why it will work, and what refutes it.* The reviewer reads each
   row's three verdicts against the lines cited; the Register
   Architect's gate `tests/test_integer_algebra.py` (being written on
   register-paper-sources; not on `main` at this base) tokenizes the
   five modules. What this table finds and says so: two integer roots
   taken at run time on these worlds' path (`meeting.meet`
   :359-361, the norm of the meeting's target, under the key `meeting`;
   `nature_beam.momentum_pair` :3549, the resolution of a pushed row's
   momentum, under the key `optical`), beside the roots formed once at
   load; and the `wave` record's square written as the product
   `X * X + Y * Y` (:4045, :5342, :6126) rather than through
   `signed_inner`. A gate that names those two functions as declared
   roots, or the owner's word moving them to a table, closes the
   sentence "six verbs and nothing else"; a float literal, a true
   division or a random draw in the path would refute it (the Boss's
   audit of record 920 found none).
4. *Why do this at all.* The vocabulary today names the push, the drive,
   the flight, the click, the meeting and the collision, and does not
   name the age wall and its set, the three verbs of `optical` on a
   row, the crowd's two moments at a row's Node, the flow label
   **f**_D, the placed fraction and the completion's quantum of the
   massive rows, or the pair form of the phase per age; the atom and
   light designs cite these by code line, and the lines move. Commit 2
   adds the missing entries to TERMINOLOGY.md and
   SIMULATOR_DEFINITIONS.md and the one sentence at the head of
   ENGINE.md.
5. *The Highlights.* Kept: the six verbs (records 181, 202), the three
   tests (record 202), the fraction-free law (record 155), the crossing
   rule (record 158), the measurement rule (record 281), the GameBoard's
   name, algebra first (record 920), the audit rule (record 817); none
   is asked to change. One option for the owner, not a proposal: the
   vector test's wording ("no root at run time beyond the ones declared
   at load") against the two run-time roots named in line 3, each
   declared in its design (the meeting's M-R, note 35; the pair of a
   pushed row, EVERY_FAMILY.md and record 496).
6. *The implementation.* Docs only: this file and its index row (commit
   1); the entries of TERMINOLOGY.md and SIMULATOR_DEFINITIONS.md and the
   sentence of ENGINE.md (commit 2); `tools/check.py --base origin/main`
   per commit under Python 3.14. Nothing runs, no identity, no key, no
   pin. What could conflict at a merge: the symbol row for **f**_D
   beside flow-link-build's own TERMINOLOGY row for `flow-link-v1` (a
   one-line textual conflict for the Boss); two status rows of
   TERMINOLOGY's identities table (optical-v1, covariant-readings-v1)
   corrected from "not built" to the code lines that run them (the
   Highlights Pruner's note in record 813).

**Notation** (skills/workflow.md, "Notation"). Q = 64 the label's scale
(`world.Q`, `LABEL_SCALE`); S the width of the push (`width`); M a
body's content; N the steps of the phase circle; h the world's `action`;
h_q a family's `quantum`; K = [n_K, d_K] the clock's pair; [n, d] the
suspension pair; [n_r, d_r] the release pair; L a family's `lifetime`;
gamma the post-Newtonian parameter (the key `optical`); f = 1 + gamma
the flight's coefficient; kappa the meeting's column sum; rho the charge
per unit of content; epsilon_c the sign of the column c; Lambda_c the
column's common denominator; tau a row's age; a_tau the age moment;
**p** a body's momentum vector, p_a its component on the axis a;
**u**_D the unit vector of the direction **D** at the scale Q; **f**_D
the flow label of flow-link-v1; **V** the label flow at a Node; **W** a
row's push accumulator; **P** = Q d content **u**_D + **W** a pushed
row's whole momentum; **c** its error accumulator; **f** a record's
phase-count vector; **G** the Gram matrix; S_1 a direction's Manhattan
length; T_D = isqrt(3 |**D**|^2 Q^2) its period constant; e_D = isqrt(3
**u**_D . **u**_D); m the multiplicity of a record's row; f_F and q_F
the placed fraction and the completion's quantum of a family; `isqrt`
the integer root; `//` the Euclidean division. The bounds: the working
bound 2^63 - 1 (`MAX_WORK_INT`, `core/integer.py:6`), the integer bound
2^62 - 1 (`MOMENTUM_BOUND`, `AMOUNT_BOUND`, `world.py:351-352`), the
meeting's `TARGET_BOUND` 2^30 (`meeting.py:85`).

## 0. The worlds and the keys they declare (what turns a coupling on)

Every key below is read from the world files; a key absent is the
law's default. K = 2^30 = 1073741824 and N = 64 in every world here
(slits_matter_small: K 2^20).

| The worlds | The keys declared | The bodies, their tables, the detectors |
| --- | --- | --- |
| `atoms/hydrogen_r12.json` (`rays-atoms-hydrogen-r12-form-b-v1`) | shape 53^3 open; ticks 7500; release [1, 18360]; suspension 0; width 45120; action 5536242544; directions the fan of 2616; families `p` (quantum 0, charge [1, 1], no phase circle), `e` (quantum 0, charge -15, a phase circle) from `entities/families.json` | the proton fixed at (26, 26, 26) releasing on the whole fan, its table the keys' default (`read`); the electron on `span` [1, 1, 3] at (38, 26, 26), momentum (0, 293783192, 0), `phase_by_momentum`, releasing on the four in-plane headings, its table the default; `at_proton` one Node, `wave`, threshold 1; the six open faces |
| `atoms/helium_r12.json` (`rays-atoms-helium-r12-form-b-v1`) | the same base; ticks 3700; families `p` (charge 4), `n`, `nuclear` (quantum 0, the column `strong` value 10000 sign -1, lifetime 3), `bond` (quantum 1, lifetime 3), `e` | four fixed nucleons about the centre holding {nuclear 1, bond 2}, releasing on the whole fan; two electrons on `span` [1, 1, 3] with opposite momenta releasing on the band fan; `at_nucleus` four Nodes, `wave`, threshold 1 |
| `optical/*_g0.json`, `*_g1.json` (`rays-lensing-*-space-v1`) | shape (57, 41, 41) open; ticks 400 (the matter worlds 1000); release [1, 4096]; suspension [1, 16384]; `optical` 0 or 1; 288 declared directions (the fan of 290 with the six headings, 296 entries with the rest slots); the matter worlds also `massive_rows` true, `action` 1024, `age_bound` 1024 and the inline family `matter` (quantum 1, or 2 in matter2, `massive`); families `light` (quantum 1), `m` (quantum 0, charge 0, no phase circle), `wall` (quantum 1) | the lamp fixed at x = 2, amount 8591334592, `lamp` rate [1, 1], wheel [1, 64], five directions, table `m: pass` (the matter lamps `momentum_magnitude` 10, 20 in matter2, 40 in the fast worlds, one direction in matter2); the mass `m` fixed at (28, 20, 20) releasing on the fan, the default table (absent in the control worlds); 1681 screen bodies `wall` at x = 54 with the table `light: {rule: measure, reads: age}, m: pass`; 1681 one-Node `wave` detectors, threshold 1 |
| `lensing/*.json` (`beam-lensing-*-v1`, series K) | the same box; suspension 0; no `optical`; the `*_meeting` worlds `meeting` true (lens_meeting: two lamps, shape (105, 41, 41), 600 ticks) | as the optical worlds without the key |
| `two_slits.json`, `one_slit.json` (`rays-two-slits-v1`) | shape (60, 121, 1), z periodic; ticks 500; release [1, 128]; suspension 0; 90 directions; `light` and `wall` from families.json | the lamp at (2, 60, 0), amount 8591334592, rate [64, 1], wheel [1, 64], five directions; a wall of `wall` bodies at x = 8 (240 or 241) with the default table (`measure`) and two openings (one in one_slit) with `light: rerelease`; 121 one-Node `wave` detectors on the screen x = 52, threshold 1 |
| `amplitude/slits_low.json`, `slits_one.json`, `slits_huygens.json` | the same base (ticks 230, 220, 4300); `light` declared inline with `phase_per_link` [8591334592, 1073741824] (the pair form); slits_huygens 1326 directions and the wheel [2531, 4096] | the lamp amount 2^30 at rate [1, 1] (slits_one: no lamp, `in_transit` rows); the openings `rerelease` (slits_huygens with `weights`); the detectors `sum` (slits_one: `wave`, with 121 `wall` bodies reading `age`) |
| `massive_rows/slits_matter.json`, `slits_matter_1024.json`, `slits_matter_small.json` | the same base; `massive_rows` true; `action` 1024; `age_bound` 2048 (256); width 1; the family `matter` (quantum 64, or 4, `massive`); 1326 directions (4) | the lamp `momentum_magnitude` 220, wheel [2531, 4096] ([633, 1024]; [5, 8]); the openings `rerelease` with `weights`; the detectors `sum` |

Not declared in any of these worlds, so not run for them: `drive_b`,
`covariant_readings`, a `become`, a `hand` or an `axis`, a
`phase_window`, a `beam` reading, a `gate` or a `rotation` on a
re-emitter, a `lamp` with `branches` or `arms` beyond one, a body that
holds paid content of another family (so the give at a contact is empty),
a moving body in a light world (every body there is `fixed`).

## 1. The table of couplings

One row per coupling; the verb is one of the six or a stated composition
of them (T the translation of an accumulator by its rate, B the bilinear
form with a declared matrix, A the group-ring addition, P the
permutation, E the evaluation, D the Euclidean division with the
remainder kept); the same verb letters are used in section 2.

| # | The coupling | Name in TERMINOLOGY.md today | The verb(s) | Declared integers and bounds | The code (function, lines on `main` at 8fa9e00b) | The world key that turns it on | The design that gave it |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | The clock's turn: a body's phase gains the count of its turn row at every self-creation | Turn; Clock; Accumulator; K = [n, d] | T then D: `by_drive(acc_turn, M x n_K, d_K)`; the count added to the phase on the circle | K = [1, 2^30] here (the turn 0 within every run, the content below K); refused at 2 x turn >= N; M x n_K tested against MOMENTUM_BOUND | `engine.NatureBeamSimulation._frame_all` :649-721 (:715 the advance, :716-720 the refusal), `step` :604-608 (the phase turned); `measured.counts_table` :421 (the row); `world.NatureBeamWorld.turn` :1250-1261 (the constant-rate identity); `core.integer.by_drive` :79-115 | none (`K` is required) | BEAM_LAW section 3 step 5, note 41 (the fraction-free law, designs/fraction_free/FORM.md); ENGINE.md "A release costs the emitter by its phase rate" |
| 2 | The owed count: the age wall on the body's clock (the crowd stretches the wall of its self-creation) | Suspension pair, owed count, a_tau; "age wall" and its set MISSING (ENGINE.md names `core.integer.age_wall` and `AGE_WALL_SET`, TERMINOLOGY does not) | T then D: `age_wall(1, 1, 1, counted, [n, d])` = (d, d + counted x n); `by_drive(acc_owed, wall - rate, d)`; the count paid one per interval | [n, d] = [1, 16384] in the optical worlds, 0 elsewhere (the count 0, :179-180); `counted` the age moment a_tau by default (`reads: age`) or the presence under `reads: presence`; the coefficient c = 1 (`AGE_WALL_SET`); the age moment bounded by the reading | `engine._suspend` :723-742, `engine.count_owed` :157-182, `_frame_all` :698-702 (the interval owed); `core.integer.age_wall` :153-187; `measured.AGE_WALL_SET` :345, `AGE_WALL_NEVER` :346, `age_wall_coefficient` :382-393, `count_component` :136-149, `counts_table` :422; `nature_beam._apply_plans` :5392-5400 (what the clock counted) | `suspension` [n, d] (0 turns it off); the entry key `reads` selects the presence | BEAM_LAW section 3 step 5, note 25; clock-age-v1 (record 394); the generic shape of records 421, 422 and 428 |
| 3 | The drive per axis: a body's step by its momentum, one Link per self-creation at most | Drive; Step; d_p (the drive's wall) | T then D with the cap: `by_drive(drive_a, p_a, Q S M + abs(p_a), at_most = 1)`, signed; then P: the Node moves one Link on the axis (`adjacent_node`), x before y before z, a later axis's coincident fire lost | Q = 64; S = 45120 (the atom worlds; 1 elsewhere); M = 1836; p_a; the cap 1; a momentum of 0 never steps (`idle_at_zero`); MOMENTUM_BOUND on every momentum (`bounded`) | `engine._move` :758-1019 (:901-905 the advance, :906-923 the fires, :926-932 the Link, :985-990 the contact or the place); `engine.step_axis` :122-154 (the one-axis rule the readings replay); `world.step_divisor` :453-464; `measured.counts_table` :432; `core.integer.by_drive` :79-115; `core.game_board.adjacent_node` | none; a body with `fixed: false` (the two atom worlds' electrons alone; :834-835 returns for a fixed body) | BEAM_LAW section 3 step 5, note 17 as amended (the step drive, records 108 and 126); designs/hubble_stars/RULES.md; `drive_b` (form B) off here |
| 4 | The turn by momentum: the action row per axis over h | Turn (the turn by momentum, `bohr-v1`); The counts table (the action rows) | T then D: the axis's `action` row gains abs(p_a) x N at every Link the step rule counts on the axis, `by_drive(acc_action_a, abs(p_a) x N, h)`; the whole part turns the phase at the Link crossed (E on the circle); at a Link not crossed the whole part is discarded, the residue kept | h = 5536242544 (the atom worlds); N = 64; the product abs(p) x N tested by `bounded` against MOMENTUM_BOUND; the parser bounds the declared momentum times ticks x N | `engine._move` :911-921 (the advance), :995-1000 (the delivery at the Link crossed), :892-898 (under `drive_b`, off here); `measured.counts_table` :438-439; `core.phase.PhaseCircle.turn` :141 | `action` (h) and the body's `phase_by_momentum` | BEAM_LAW note 30 (ii), note 41 (i) and (viii); record 155; ALGEBRA.md section 1 (a) |
| 5 | The free release: a body's rows of a free family it holds, on its declared directions | Release; Self-creation; Direction | T then D: the family's release row gains held x n_r over d_r, `by_drive(acc_release_f, held_f x n_r, d_r)` (a paid family's row has the rate 0); E: each row stamped with the body's phase, age 0, the body's number; D again for a body on a set: `place_over_nodes` places each row's units whole over the Nodes by their `place` rows | [n_r, d_r] = [1, 18360] (the atom worlds: one unit per 10 self-creations at M = 1836), [1, 4096] (the light worlds' mass, 16 units per direction per interval at M = 2^16), [1, 128] (the slits' walls, which hold no free family); AMOUNT_BOUND on the amounts; the labels bounded per row (`momentum_labels`) | `nature_beam._release` :5960-6073 (:6025-6029 the count), `_release_family` :5494-5957 (:5534-5557 the free rows, :5867-5881 the placement over a set, :5894-5913 the labels and the recoil of a paid re-creation; a free release takes none), `place_over_nodes` :1666-1692; `measured.counts_table` :424-427; `core.integer.apportion_whole` :233-249 (the pending rows, :5713) | none (`release` is required) | ENGINE.md "A release costs the emitter by its phase rate"; BEAM_LAW section 5; note 41 (viii) (the place rows, record 155) |
| 6 | The lamp's birth: a paid release of one record per count, the cost h_q x s, the wheel's u | Lamp; Wheel (the birth wheel); Record (of a quantum); Window (the lamp's) | T then D: the `lamp` row gains its declared `rate` [n, d] at every self-creation of the lamp, the count the records born now (:6019-6020); the `wheel` row advanced by r over W, u its accumulator before (`birth_coordinate`); the cost h_q x s a product of two declared integers, `held -= cost x weight`; E: the rows' phase (u + lamp_turn) mod N; D: the window `window_admits`, one floor | `quantum` h_q = 1 (`light`, `wall`), 64 (`matter`); the turn s = 8 per self-creation at the content 8 K + 1400000 (the lensing README); `rate` [1, 1] or [64, 1]; `wheel` [1, 64], [2531, 4096], [633, 1024], [5, 8]; a lamp short of `per_direction` quanta on every direction is refused (:5787-5796); the record's identity number x 2^32 + ordinal (`record_identity` :2427) | `nature_beam._release` :6019-6020 (the lamp's count), `_release_family` :5732-5847 (:5748 the cost, :5749-5760 the massive turn 1, :5772-5847 the births), `birth_coordinate` :690-706, `window_admits` :709-722; `measured.counts_table` :428-431 | the body's `lamp` (rate, wheel, directions; `momentum_magnitude` on a massive family): a lamp makes a recorded world (`amplitude-v1`, `world.NatureBeamWorld.recorded` :1236-1243) | BEAM_LAW section 5, notes 37 and 46; designs/amplitude-v1/DESIGN.md; record 180 (the wheel) |
| 7 | The flight: the walk of a row on the digital line of its direction, one Link per interval at most | Flight; Walk; Link; T_D, S_1, L_d; `m(tau)` | T then D: the position's accumulator gains 2 S_1 Q against 2 T_D from the start T_D, `by_drive_rows(residue, rate, wall)` (the count 0 or 1); P: the Link is the `made mod S_1`-th unit step of the Bresenham line; the age +1 whole; a massive family walks by its own triple (the rate 2 abs(**p**_D)_1, the wall 2 E'_D, the start E'_D) | Q = 64; S_1 = abs(a) + abs(b) + abs(c); T_D = isqrt(3 abs(**D**)^2 Q^2) formed once at load (110 on a heading); E'_D = isqrt(E'_0^2 + 3 **p**_D . **p**_D) at load with E'_0 = Q S h_q (the massive rows); the residue plus the rate within MAX_WORK_INT (:611-612) | `nature_beam.Flight.accumulator` :783-801, `walk_step` :803-821, `manhattan_steps` :775-781, `direction_flight` :847-886 (:860 T_D), `by_drive_rows` :586-618, `_walk` :3966-4179 (:4001-4003 the step, :4136-4166 the Node, the age, the sort), `_walk_rows` :1306; `FamilyFlight.walk_step` :1009-1021, `flight_triple` :1034-1055, `family_flight` :1058-1124; `world.bresenham_line` :1588 | none; `massive_rows` with the family flag `massive` for the family's own triple (the matter worlds) | BEAM_LAW section 3 step 1, note 41 (viii) (the flight as the position's accumulator, record 155; MIGRATION "no tables"); designs/massive_rows/DESIGN.md (the value form) |
| 8 | The one reading: the moments of a Node's or a set's rows (the presence, the age moment, the flow, the tensor), what a body's clock counts and its push reads | The reading (the moments); The crowd (the one reading set); Age; a_tau; **f**, **T**, **a** (**V**) | B then A: one product per row (amount x **u**_D, amount x age, amount x **u**_D **u**_D^T) in `moment_table`, summed per group (`np.add.at`, `moments_of_groups`); the age +1 per interval (T) | the amount and the age per row; the bound of the table (`reading_bound_error` :433, `first_reading_overflow` :2467); the component by the entry's `reads` (`scalar` by default, `vector` on `read`, `age` on the screens) | `nature_beam.moment_table` :441-467, `read_arrivals` :522-563, `Moments.component` :415; `_family_plan` :4692-4721 (the presence and the age moment over the present rows), :4748-4761 (the admitted rows' reading), `_walk` :4164 (the age); `measured.count_component` :136-149 | none; the entry key `reads` selects the component on the click line | BEAM_LAW section 3 step 2, notes 16 and 33 (the four unifications (3)); note 25 (the age whole, read by a body) |
| 9 | The crossing: which rows a stepping body reads and on which direction (a row and a body meet once) | Crossing | a comparison of E: the row's step this interval and the one before, `walk_step` at its age, against the body's two marks e and e'; no arithmetic on the state beyond the comparison; the swap rows gathered from the trailing Nodes | the body's `step_port` and `last_step_port` (-1 without a Link); the row's `arrival` and age | `nature_beam._family_plan` :4367-4442, `interval_frame` :3221-3258 (the marks, the entered and the trailing Nodes); `engine._move` :832-833, :992 | none; acts on a body that stepped (the atom worlds) | BEAM_LAW note 48, record 158; MIGRATION "the crossing rule" |
| 10 | The push on a body (the coupling): the signed inner product over the columns of the arriving rows' label flow | Push (the coupling); Column; Charge; **C**; The counts table (the push rows); Lambda_c | B then T then D then A: per column X = V x E_c x n_c x (Lambda_c / D_c) x (Lambda_c / d_c); the column's three push rows gain X over Lambda_c^2, `by_drive` (signed, the remainder kept); the momentum gains epsilon_c x the whole parts summed over the columns; for a paid family's rows the moment itself (kappa = 1) | the columns (name, sign): gravity (1, 1) on every family, sign -1; charge rho (`p` [1, 1], `e` -15, helium's `p` 4, `m` 0); helium's `strong` (value 10000, sign -1, on `nuclear`); the reader's charges E_c / D_c the rational sums over what it holds (`column_charges`); Lambda_c the lcm of the values' denominators (1 on every column here); each product tested by division against MOMENTUM_BOUND before it is formed (:2998-3009); the momentum `bounded` | `nature_beam.push_form` :2932-3016, `_apply_plan` :5084-5103 (the call and the momentum), `_family_plan` :4762-4807 (the flow per group `g_moment`, the shares of a record's row), `share_of` :1645-1663; `measured.Measured.charges` :704-747, `column_charges` :99-133, `counts_table` :433-437; `engine._frame_all` :671-672 (`frame_content`, `frame_charges`, read once before the law); `world.NatureBeamWorld.column_scales` :1275-1300 | none; the family keys `charge` and `columns` give the columns (`columns-v1` for a declared column) | BEAM_LAW notes 20, 28, 31 (columns-v1), 41 (the fraction-free push, designs/fraction_free/FORM.md section 2); DERIVATIONS_BEAM 3.4 |
| 11 | The table's rule per family (read, measure, rerelease, pass) and its default from the keys | Table; the rule names under Click, Re-emission | no arithmetic: the rule is a value of the entry, the default `read` for a free family (quantum 0) and `measure` for a paid one; a `pass` row is left out of the admission (:4542) and still counted in the presence and the age moment (:4703-4721) | `quantum` 0 or not; the declared entries `light: rerelease`, `light: {rule: measure, reads: age}`, `m: pass` | `world.default_rule` :941-945, `default_table` :954-963, `_table_entry` :2576; `nature_beam._family_plan` :4541-4542, :4703-4721; `_apply_plan` :4959 | the entry `table` of a body | BEAM_LAW note 15 (the table from the keys); the model owner, 2026-09-19 |
| 12 | The threshold and the window: what a set admits | Threshold; Window | A then a comparison: the amount summed over the set against the threshold; D: `window_admits`, one floor `(d + w // 2) mod N < w`; under `wave` the set's phase from the pointer (E, `coherent_pointer`, `pointer_phases`) | `threshold` 1 on every detector here; no `phase_window` declared in these worlds (the window -1: every phase admitted, :4591); the width N / 2 by default | `nature_beam._family_plan.admit` :4531-4689 (:4550-4558 the threshold, :4565-4593 the window, :4606-4607 the hand filter, 0 here), `window_admits` :709-722, `_measured_arrays` :4238-4247 | `detectors[].threshold`; the entry's `phase_window`, `phase_width` | BEAM_LAW section 5, notes 24 and 36 (i) |
| 13 | The click (measure): a paid row's units join the body's record, its label enters the momentum, its phase is read at the exact time of its last Link | Click (measurement); Detector; A detector's clock; Exact phase at the click | T: `held += content`, `clicks += units` (the group's sums); the label onto the momentum through `push_form` (:2987-2988, the moment itself for a paid family); D: the exact phase, one floor with the remainder kept (`exact_phase`); the row leaves the store | the content M and the units; MOMENTUM_BOUND (`bounded`, :5098, :5244); the exact phase's numerator n x made x T_D within MAX_WORK_INT (:678-684); the click line carries `tick` (the record's ordering), `node`, `amount`, `push` (the label), `phase`, `content`, `reading` and, with the pair form, `exact` and `remainder`; the detector's own count is its clock, `Measured.age`, advanced at :704-705 once per interval when nothing is owed, not written on the line | `nature_beam._apply_plan` :5236-5318 (:5244-5247 the content and the units, :5281-5318 the line), :5088-5103 (the label onto the momentum), `_family_plan` :4841-4863 (the exact phase), :4877-4881 (the rows leave), `exact_phase` :621-687, `optical_last_link` :3713-3727 | the entry rule `measure` (the keys' default for a paid family); the screens' `reads: age` | BEAM_LAW section 5; note 45 (record 163 (2)); the detector's own count, record 754 as ALGEBRA.md cites it |
| 14 | The face click and the border `lifetime` (the escapes) | Face, face detector; Lifetime | P: the walk's Link off the GameBoard (no Node); D: `ages_at_key`, `age mod L == 0` (`by_clock(age - 1, 1, L)` = 1); A: the amounts, the content and the labels to the escaped lines; B: the face's record `X * X + Y * Y` of the pointer of what left (:4045, :6126); D: the exact phase at the Link | `boundary` open (every axis here but the slits' z); `lifetime` 3 on helium's `nuclear` and `bond`; the world's `age_bound` refuses a row past it (:6277-6281, the same primitive) | `nature_beam._walk` :4016-4135 (:4022-4073 the faces' lines, :4078-4091 the exact phase, :4110-4135 the click line); `_border` :6076-6212; `ages_at_key` :725-738; `engine._move` :940-984 (a body's escape) | `boundary`; the family key `lifetime` | ENGINE.md "An open face is a detector", "The border lifetime"; BEAM_LAW note 31 (vii), note 33 |
| 15 | The read (a free family's rows at a body): the push taken, the row goes on | Table (a free family read) | as row 10; the row's record unchanged (a record row keeps the undelivered part of its share, :4795-4798); the `read` line with `push` and `reading` | none beyond row 10 | `nature_beam._apply_plan` :5111-5145; `default_rule` :941-945 | the entry rule `read` (the keys' default for a free family) | BEAM_LAW section 5; note 15 |
| 16 | The re-emission and the split: a `rerelease` entry's rows created again on the body's directions, a record's row split by the entry's weights | Re-emission; Split; Home | P: the rows on the declared directions; B: the split by the weights (w a_i, m x A, p + t_i), the multiplication by the apparatus's integer matrix; D: `apportion_whole` over the directions, the multiplicity m x A; T: the recoil on the emitter (`born_recoil`, `share_of`) | the entry's `weights` (slits_matter, slits_huygens: the fan's angular weights, integers; equal weights 1 where none is declared); AMOUNT_BOUND on amount x weight (:5632-5637); MOMENTUM_BOUND on m x A (:5623-5628) | `nature_beam._apply_plan` :5163-5235, `_release_family` :5558-5731 (:5585-5682 the split, :5696-5730 the apportioning), `born_recoil` :1620-1642, `share_of` :1645-1663; `world.Split` :2379-2405, `_split` :2520 | the entry rule `rerelease` (the slits' openings) | BEAM_LAW section 5, note 37 (ii); TWO_SLITS.md sections 7 and 10 (the fan's weights, N_theta) |
| 17 | The collision: the permutation of the single units of one (Node, number, content) group on the six headings at a Node of free space | Collision; The cube group (the Port order tie) | P: the cyclic shift on the 3^8 slot codes within a class (`collision.act`), the class (the crowd mask, the singles' count, their headings' sum) invariant | the alphabet: the two rest slots and the six headings (a direction index below 8, `FIXED_DIRECTIONS`); a single is a row of amount 1; the table generated once per process (:1203-1234) | `nature_beam._collide` :3360-3400, `collision_table` :1203-1234, `class_key` :1188-1194, `CollisionTable.act` :1175-1179; the call :3331-3332 | none; free space only (`occupied` False); the fan's directions (index 8 and beyond) are outside the alphabet (:3366) | BEAM_LAW section 4; record 191 (the group action) |
| 18 | The meeting: a paid unit in transit reads the free crowd and turns toward its target by its phase register | Meeting; kappa | B: kappa_AB = the signed column sum (`column_sum`), the target t = sum kappa **V** (`crowd_flow`, A); an integer root at run time: abs(t) = `integer_root(t . t)` (:359-361); D: adv = (abs(t) + Q // 2) // Q, k = (phase + adv) // N, phase' = (phase + adv) mod N (`register`); P: k steps of the arc permutation pi_t (`arcs.permutation`) | Q, N; kappa = -1 on these families (gravity alone); TARGET_BOUND 2^30 on the target (:348-355); MOMENTUM_BOUND on the flow (:263-267, :341-346) | `meeting.meet` :287-404, `column_sum` :219-231, `crowd_flow` :249-284, `register` :234-238, `arc_table` :149, `arc_shift` :187; `nature_beam.nature_beam` :3337-3338 | `meeting` (the lensing `*_meeting` worlds) | BEAM_LAW section 3 step 3, note 35 (M-R); ENGINE.md (the `turned` line) |
| 19 | The age wall on the flight (optical-v1's verb 1): the row's flight accumulator stretched by the crowd's age moment at its Node | MISSING (TERMINOLOGY's identities table lists `optical-v1` as "decided as a hypothesis, not built"; the key runs, `world._optical` :3755-3817) | T then D with the cap: the residue gains rate x d against wall x (d + f n A), `by_drive_rows(residue, rate, wall, at_most = 1)`, the surplus kept; P: the Link at `made mod S_1` of the label's line; the fresh accumulator the family's off-age pair times d | [n, d] = [1, 16384]; f = 1 + gamma (gamma = `optical` 0 or 1); A the age moment at the row's Node less its own number, one interval retarded; the largest wall times the stretch within MAX_WORK_INT (:3616-3623) | `nature_beam.optical_walk_step` :3634-3710, `optical_rate_and_wall` :3602-3631, `row_pairs` :3585-3599, `interval_frame` :3291-3295 (the crowd read before step 1), `_walk` :4004-4015; `core.integer.age_wall` :153-187; `measured.age_wall_set` :364-379, `FLIGHT_MEMBER` :350; `world.NatureBeamWorld.flight_coefficient` :1229-1233 | `optical` gamma (refused with `suspension` 0 and with `meeting`, :3788-3799) | designs/one_wall/NOTE.md sections 1 and 2; EVERY_FAMILY.md; STEP_ALGEBRA.md section 2 (the inputs table); records 421 to 428 |
| 20 | The crowd's two moments at a row's Node (optical): the age moment before step 1, the arrival flow after the walk and the collision, each less the row's own number | MISSING (The crowd names the body's reading set; the row as a reader is not named) | A: segmented sums of amount x age and amount x **u**_D (the family's own labels) per Node and per (Node, number); the own number's sums subtracted | amount x age within MOMENTUM_BOUND (:3099-3103); the rows at the fullest Node within MAX_WORK_INT (:3110-3115) | `nature_beam.CrowdMoments` :3069-3153 (:3104 the moment, :3108 the label, :3117-3119 the sums, :3136-3153 the reads), `interval_frame` :3291-3295, `optical_turn` :3800 | `optical` | one_wall/NOTE.md; the physics-rule review of 408cf719, record 494, S3 (the crowd read twice) |
| 21 | The push on a row (optical-v1's verb 2): **W** -= n x weight x **V**, the residue rescaled to the new pace | MISSING | B then T: the weight per unit (E'_D^2 + 3 gamma **p**_D . **p**_D) // E'_D formed at load, times the row's content, times n, times **V**, subtracted from **W**; D: the residue s' = s x S_1(**P**') // S_1(**P**) at every push, the sub-unit remainder dropped (the one truncation of the flight's time) | the weight 110 (e_D at gamma 0) or 221 (gamma 1) on a heading (`unit_weights`; e_D = isqrt(3 **u**_D . **u**_D) = 110 or 111 at load, `unit_energies`); n = 1; a free family's row has content 0 and never turns; n x weight x abs(**V**) and abs(**W**) + it within MAX_WORK_INT (:3825-3840); the rescaled residue within MAX_WORK_INT (:3880-3884) | `nature_beam.optical_turn` :3730-3885 (:3821-3822 the weight and the flow, :3842 the translation, :3844-3885 the rescale), `unit_weights` :3563-3582, `unit_energies` :1138-1150, `with_weights` :1127-1135, `momentum_pair` :3494-3560 (the pair of a pushed row, one `math.isqrt` per pushed row at :3549 when **P** changes) | `optical` | one_wall/NOTE.md; EVERY_FAMILY.md section 1; the reviewer's S4 (the floor a load-time rounding); record 496 (the residue) |
| 22 | The label by Bresenham along **P** (optical-v1's verb 3): the row's direction moves to the fan neighbour whose next Link keeps abs(**c** + **h** x **P**)^2 smallest among the Links that advance along **P** | MISSING | P: the direction index changed to a neighbour; the choice by comparisons of B (integer products, `error = e . e`), `h . P > 0`; T: **W** += Q d content (**u**_D - **u**_D') so **P** is conserved; T: **c** += **h** x **P** at every Link walked on a pushed row | **P** = Q d content **u**_D + **W**; the neighbours per direction at most `FAN_NEIGHBOURS` = 6 (:892); abs(**c**) + abs(**P**) within MAX_WORK_INT (:3692-3697); abs(**W**) + the shift within MAX_WORK_INT (:3951-3957); the `turned` line of the books | `nature_beam.optical_turn` :3886-3963, `optical_walk_step` :3681-3703 (the error accumulator), `fan_neighbours` :895 | `optical` | record 536 (the owner's GO on the chief physicist's recommendation of record 483); one_wall/NOTE.md section 2 |
| 23 | The momentum label of a row: the weight along the unit vector of its direction (and, when flow-link-v1 merges, the flow label **f**_D in the flow sums) | The momentum label; **u**_d; Direction; **f**_D MISSING (on `main`; flow-link-build adds `flow-link-v1` at its TERMINOLOGY :457) | D at load: **u**_D the integer vector nearest Q **D** / abs(**D**), k(abs(a)) = (isqrt((2 Q abs(a))^2 // n) + 1) // 2; B at run time: amount x content x **u**_D (a paid family) or amount x **u**_D (a free one); **f**_D[i] = sign(D[i]) x (2 Q abs(D[i]) + S_1) // (2 S_1), one D at load, read in the flow sums alone | Q = 64; every component within Q; the product weight x max abs(**u**_D) within 2^62 - 1 per row (`label_overflow_rows` :1597); a massive family's label **p**_D at the scale `momentum_magnitude` (`scaled_label`) | `nature_beam.unit_label` :824-844, `direction_flight` :872, `momentum_labels` :1714-1754, `label_weights` :1695-1711, `NatureBeamStore.labels` :2163; `world.scaled_label` :591; on flow-link-build: `direction_flight` :917-921 (`flow_label(vector, Q)`), `CrowdMoments` :3367 and :3877, `_family_plan` :4418 read `flow_labels` | none; `flow_link` (absent by default) when merged | BEAM_LAW notes 18 and 23; flow_weight/DESIGN.md section 1.2 (record 898, the reviewer's ADMISSIBLE of record 902) |
| 24 | The row's phase turn in flight: per Link crossed (`phase_per_link` over 1; a massive family abs(p_{D,a}) x N over h per axis Link) and per interval of age (the pair form n / d) | Phase (the turn per Link); Exact phase at the click (names the pair form); no entry of its own for the phase per age | T then D: `by_drive_rows(acc_turn, turn[direction, axis], turn_denominator)` at the Link crossed, the remainder on the row; D: the pair form `by_clock_rows(age, n, d)`, the first difference of a floor (no remainder on the row; the exact phase reads it at the click) | `phase_per_link` 0 on `light` of families.json (the lamp's turn 8 stamps the birth phase); the pair [8591334592, 1073741824] on the inline `light` (8 + 1400000 / 2^30 steps per interval of age); a massive family abs(**p**_D) x N over h = 1024; (age_bound + 1) x n within AMOUNT_BOUND (:1851-1855) | `nature_beam._walk` :4153-4165, `FamilyFlight.turned` :1023-1031, `family_flight` :1075 and :1106, `by_clock_rows` :569-583; `world._families` :1842-1860 | the family key `phase_per_link` (an integer or a pair); the flag `massive` | BEAM_LAW section 2; note 37 (the pair form, the owner's unification (1)); designs/massive_rows/DESIGN.md (de Broglie's turn per axis Link) |
| 25 | The exact phase at the end of a row (a click, a face, the border): phi = phase - floor(terms n / d) + floor(n made T_D / (d S_1 Q)) mod N | Exact phase at the click; phi, terms, made | D: one floor at the click with the remainder kept; under `optical` the time of the last Link is (age r - s, r) off the row's stored residue | n x made x T_D within MAX_WORK_INT (:678-684), refused naming the place; the remainder and the divisor written on the line | `nature_beam.exact_phase` :621-687; the calls :4078-4091 (a face), :4841-4863 (a body), :6149-6164 (the border); `optical_last_link` :3713-3727 | none; acts with the pair form of `phase_per_link` (a family without it reads its phase as it is, :660-661) | BEAM_LAW note 45; record 163 (2); TWO_SLITS.md section 2 |
| 26 | The merge: identical rows at one Node become one row with the amounts added; in a recorded world two rows of one record in antiphase cancel | Merge | A: the group-ring addition (the amounts added; under a record the signed sum by the half circle, the cancel) | N (the half circle N / 2); without a lamp nothing cancels | `nature_beam._merge` :6215-6281, `NatureBeamStore.merge` :2037-2120, `_merge_rows` :1377-1560 (:1393-1398 the sign of the cancel, :1445-1453 the cancel) | none; the cancel in a recorded world (a lamp) | BEAM_LAW section 3 step 6, note 37 (the normal form) |
| 27 | The detector set's record under `wave`: the pointer of what clicked, its square, the set's phase returned to its bodies | Record (of a detector); Pointer; (X, Y) | E: (X, Y) = sum 32 x amount x (C[phase], S[phase]) over the clicked rows (`coherent_pointer` through `read_groups`, a B with the tables); B: the square written as `pointer_x * pointer_x + pointer_y * pointer_y` (:5342), not through `signed_inner`; E then a comparison of products: the nearest step of the circle (`pointer_phases`), written as the phase of every body of the set | AMPLITUDE_SCALE 32 (`amplitude.py:115`); the tables at PHASE_COSINE_SCALE 256 (`core/phase.py:21`), formed once at load by fixed-point series (:30-57, :82-115); the record an exact Python integer, never refused | `nature_beam.coherent_pointer` :1765-1797, `pointer_phases` :1805, `_family_plan` :4882-4900, `_apply_plan` :5337-5370; `core.phase.phase_cosines` :97-115, `phase_sines` :82-93 | `detectors[].reading` `wave` (the default) | BEAM_LAW section 5, notes 24, 29 and 33 |
| 28 | The record's click: the gather at the ladder under `sum` (the click without amplitudes) | Click (Gather); Offer, ladder; **f**, **G**, R(f), b_k, u, W | A: the phase-count vector per label and Node (`add_counts`); B: the weight **f**^T **G** **f** through `signed_inner` (`gram_form`), no pointer formed; D: the rungs b_k = (2 W C_k + T) // (2 T), the cell of u by the comparison of products (`cell_of`), the Node within the cell (`node_choice`); E: the pointer reported (`evaluate`); the placement: the chosen end takes q_F and q_F x the label of the chosen row's direction (the massive rows; 0 for a family without the flag) | N; the wheel W (64 under [1, 64]; 4096 under [2531, 4096]); the unit 2^58 (`amplitude.UNIT` :129); the Gram matrix stored for N through GRAM_STORED_STEPS 512 (`core/phase.py:24`); the weights unbounded (the host's reports) | `amplitude.Layer.gram_form` :788-799, `gram_entry` :779-786, `evaluate` :766-777, `cells` :817, `complete` :901-1003, `rungs` :241-262, `cell_of` :275-296, `node_choice` :299-312; `core.phase.phase_gram` :61-78; `core.integer.signed_inner` :190-230; `nature_beam.gather_records` :6284-6360, `_place_completion` :6363-6455, `Layer.end` at :4096, :5115, :5193, :5266, :6169 | `detectors[].reading` `sum` in a recorded world (slits_low, slits_huygens, slits_matter) | BEAM_LAW note 37 (xii) (record 188); designs/amplitude-v1/DESIGN.md; note 46 (the wheel); designs/massive_rows/DESIGN.md section 3 |
| 29 | The completion's placement of the massive rows: the placed fraction f_F of an arrival and the quantum q_F placed at the chosen end, the rest waiting then cancelled | MISSING (`massive-rows-v1` in the identities table; "the placed quantum of a completion" and "the waiting" in ENGINE's readings by type; the pair (f_F, q_F) has no entry) | a value pair per family: (1, 0) for a family without the flag (nothing waits), (0, M) for a massive one; A: the waiting units, content and labels on the `absorbed` line; T: q_F onto the chosen end's `held`, `clicks` and momentum | f_F = `FamilyFlight.placed`, q_F = `FamilyFlight.quantum` (:979-980, :1086-1087, :1117-1118); an end with less than q_F waiting is refused (:6393-6397) | `nature_beam._walk` :4050-4073, `_apply_plan` :5242-5254, `_border` :6129-6145, `_place_completion` :6363-6455 | `massive_rows` with the flag `massive` (the matter and slits_matter worlds) | designs/massive_rows/DESIGN.md section 3 (the value form) |
| 30 | The contact (a refused step onto a body) and the give of carried paid content | Contact; Give | D: the handed component apportioned whole over the occupants (`apportion_whole`); T: the two momenta moved by it (`measure` hands it, `rerelease` returns twice it); the give: D `held // h_q`, one row born, T the recoil | `CONTACT_DEFAULT` `measure` (`world.py:332`); MOMENTUM_BOUND on both momenta | `engine._contact` :1021-1126, `_give` :1128-1203; `engine._move` :985-989 | none; runs when a moving body's destination holds a body (the atom worlds alone); the give is empty for these electrons (:1158-1162: no paid content of another family held) | ENGINE.md (the contact through the table, 2026-09-20); BEAM_LAW note 31 (ix), note 40 (`binding-v1`) |
| 31 | The books: the ledger's exact sums per interval | Books | A: exact sums (`exact_sum`, `exact_column_sums`); a report read back by no rule | none (unbounded Python integers, a GameBoard reading) | `engine.NatureBeamSimulation.books` :1276, `nature_beam.exact_sum` :1560, `exact_column_sums` :1571; the ledger's lines throughout `_walk`, `_apply_plan`, `_release_family`, `_border`, `_merge`, `meet`, `optical_turn` | none | ENGINE.md "The books" |

## 2. The three tests per row, as the code has it

Generic (one primitive with declared integers, no family name, the
engine branches on no name), vector (one of the six verbs on the state
vector, no root, no float, no run-time rounding beyond the declared
ones), local (its own record and the six neighbouring Nodes, nothing
kept at a Node). The verdicts are what the lines show; the reviewer
rules.

| # | Generic | Vector | Local |
| --- | --- | --- | --- |
| 1 | `by_drive` on the `turn` row at the world's pair for every body alike; the family enters as `phase` true or false (:706-707, a key) | T, D; the product M x n_K formed once, tested first | the body's own record (`acc_turn`); nothing at a Node |
| 2 | `age_wall` then `by_drive` on the `owed` row; the member set is a declared tuple (`AGE_WALL_SET`), the coefficient a value; `count_component` reads the entry key `reads`, no name | T, D; no root, no float | the body's own record and what its clock counted at its own Nodes less its own number (`counted`, :5396-5400); one interval retarded |
| 3 | one primitive `by_drive` with the wall `step_divisor(p_a, M, S)` per axis, every body alike; the branch at :851 is on the world key `drive_b`, off here | T, D with the cap 1, then P (one Link); no root, no float | the body's own record; the destination Node read by the step (:985) |
| 4 | one `action` row per axis, one division by the declared h; `phase_by_momentum` is the body's declaration to use it (:911, :995), not a branch on a name | T, D, then the phase's translation on Z_N; the product abs(p) x N bounded first | the body's own record; nothing at a Node |
| 5 | one `release` row per family at the world's pair; a paid family's row has the rate 0 (a value, :425); the free rows born carry content 0 and take no recoil (:5896, a branch on `free`, the quantum's value) | T, D, E; `apportion_whole` and `place_over_nodes` are D with the leftover by the largest claim | the body's own record and its own Nodes; the rows born at its Node (or its set's Nodes) |
| 6 | one `lamp` row and one `wheel` row at declared rates; the cost h_q x s a product of the family's quantum and the body's turn, every family alike; the massive turn 1 is a refusal of a value (:5749-5760) | T, D, E; the window one floor; no root | the lamp's own record; the rows born at its own Node |
| 7 | one primitive `by_drive_rows` on the row's residue with the family's triple, Flight's numbers by value for a family without the flag (:1074-1093), the triple for a massive one; the flag is read at load into a table, not at run time | T, D, P; the roots T_D and E'_D at load only (:860, :1051) | the row's own record (its direction and age; under `optical` its stored residue) and the one Link crossed |
| 8 | one moment table for every family and every reader (:441-467), the component selected by the entry key `reads`; no name | B (one product per row), A (the segmented sums); no root, no float | the rows at the reader's own Node or set (and the swap rows at the trailing Nodes one Link away, :4374-4386); nothing kept at a Node (the sums are the interval's) |
| 9 | the same comparison for every body and every family (:4425-4435); no name | E (the flight rule at the row's age) compared; no arithmetic on the state | the row's own record against the body's two marks; the trailing Node one Link away |
| 10 | one loop over the columns for every family's rows, the columns declared pairs and signs; the branch at :2987 is on `free` (the quantum 0: a paid row's push is its label), a value of the family table | B (the products), T and D (the push rows), A (the signed sum); no root, no float; the shares of a record's row D (`share_of`) | the reader's own record (`acc_push`, `frame_charges`) and the rows at its own Nodes less its own number |
| 11 | the rule a value of the entry, the default from the quantum (:941-945); no name | none | the reader's own table |
| 12 | one threshold per set, one floor per window, every family alike | A (the sum over the set), D (the window's floor), E (the set's phase) | the rows at the set's own Nodes |
| 13 | the same click for every paid family (:5236-5318); the label onto the momentum through the one `push_form` | T, D (the exact phase); the click line's `tick` is the host's ordering, no arithmetic of the rule | the body's own record and the row at its own Node |
| 14 | the same escape for every family (the faces' lines per family; `lifetime` a family key read as one comparison) | P, D (`age mod L`), A, B (the record's square as the product `X * X + Y * Y`, :4045, :6126) | the row's own record; the face it leaves through |
| 15 | as 10 | as 10 | as 10 |
| 16 | one apportioning and one split for every re-emitter, the weights a declared integer list, the norm sum a_i^2 | P, B (the weights), D (the apportioning, the multiplicity), T (the recoil) | the re-emitter's own record and its own Nodes; the rows born there |
| 17 | one table on the 3^8 codes generated from the class rule, no name, no family (per store: rows of one family, number and content) | P; no arithmetic beyond the code's digits | the single units at one Node of free space |
| 18 | one column sum per pair of families from the declared values (kappa a value); the readers are the paid families and the crowd the free ones (:312, :321, branches on `free`, the quantum's value) | B, A, then an integer root at run time (`integer_root(t . t)`, :359-361), D (the register), P (the arc) | the paid unit's own record and the free rows at its own Node less its own number; the crowd untouched |
| 19 | one wall function `age_wall` on every family's pair (the photon's by value, the massive triple by its own numbers), the coefficient a declared member (`FLIGHT_MEMBER`); no name | T, D with the cap, P; the stretch a product of declared integers; no root here | the row's own stored accumulator and the age moment at its own Node less its own number, read before step 1 |
| 20 | one segmented sum per Node for every family's rows on its own labels; no name | A (with the own number's sums subtracted) | the rows at the reader's own Node; the sums the interval's, nothing kept |
| 21 | one weight column per direction per family formed at load from the family's own energies and labels (`unit_weights`), n and **V** the same for every row; a free family's row has content 0 (a value) | B, T; D (the residue rescale, the sub-unit remainder dropped: a declared truncation, record 496 as generalised); the pair of a pushed row takes `math.isqrt` at run time (:3549), the docstring's "the law's own integer root taken per pushed row when **P** changes" | the row's own record (**W**, the residue) and the arrival flow at its own Node less its own number |
| 22 | one comparison over the direction's declared neighbours for every row that holds a push; no name | P chosen by comparisons of B (integer squares of cross products); T (**W** and **c**); no root, no float | the row's own record and the fan neighbour table (a constant of the world) |
| 23 | one rule for every direction (the nearest integer vector at the scale Q); a massive family's scale its declared `momentum_magnitude`, the same division | D at load (the isqrt inside `unit_label` :842, a declared rounding at load); B at run time | the row's own direction |
| 24 | one turn table per family over the directions and axes (`turn`, `turn_denominator`), `phase_per_link` over 1 or abs(**p**_D) N over h, a value; the pair form the same `by_clock_rows` for every family that declares it | T, D (per Link); D (the pair form, the first difference of a floor) | the row's own record and the Link it crossed |
| 25 | one floor for every row that ends, on the family's declared pair | D with the remainder kept and written | the row's own record (its phase, its age, its direction) |
| 26 | one order on the identity fields for every family; the cancel a signed sum keyed by the record (a value on the row) | A | the rows at one Node |
| 27 | one pointer per set per family from the two tables of the circle | E (a B with the tables), B written as the product (:5342), the nearest step by comparisons of products (`pointer_phases`) | the clicked rows at the set's own Nodes; the set's phase written on its own bodies |
| 28 | one Gram matrix per N, one ladder for every record (the cells from the offers, the rungs from declared integers); the placement a pair of values per family | A, B through `signed_inner`, D, E; no root | the record's offers at every Node its rows ended (:6315, the ladder over cells at several Nodes): the one step that reads beyond a Node and its six neighbours, the record's own (the click frame section 0; the Bell note) |
| 29 | a value pair per family, (1, 0) or (0, M), read at every end alike | A, T | the chosen end's own record; the waiting on the books |
| 30 | one rule through the occupant's table entry, the default `measure` a value (`CONTACT_DEFAULT`); the give per paid family by its quantum | D, T | the body's own record and the destination Node one Link away |
| 31 | exact sums per family | A | a host report |

## 3. What the table says in one line

Every rule these worlds run is one of the six verbs on bounded integers
or a stated composition of them, with two exceptions the lines show and
this file names for the reviewer and the gate: the integer root taken at
run time in the meeting's norm (`meeting.py:359-361`, under `meeting`)
and in the pair of a pushed row (`nature_beam.py:3549`, under
`optical`), each declared by its design and neither a table formed at
load; and the `wave` record's square written as a product rather than
through the bilinear primitive (:4045, :5342, :6126), a bilinear form on
integers all the same. No float, no true division, no draw (the Boss's
audit by tokens, record 920).

## 4. The definitions MISSING or stated in other terms (commit 2)

Added to [TERMINOLOGY.md](../../TERMINOLOGY.md) and
[SIMULATOR_DEFINITIONS.md](../../../SIMULATOR_DEFINITIONS.md) in the canonical
vocabulary (Node, NodeState, Link, Port, Event, LocalRule, GameBoard),
each pointing at its code lines and its design:

1. The age wall and the age wall's set (rows 2 and 19): `core.integer.age_wall`
   :153-187; `measured.AGE_WALL_SET` :345, `AGE_WALL_NEVER` :346,
   `age_wall_set` :364-379.
2. The crowd's two moments at a row's Node (row 20): `nature_beam.CrowdMoments`
   :3069-3153.
3. The three verbs of `optical` on a row (rows 19, 21, 22): the wall on the
   flight, the push on the row, the label by Bresenham along **P**; the
   pair of a pushed row and its residue rescale.
4. The flow label **f**_D of `flow-link-v1` (row 23), when merged.
5. The placed fraction f_F and the completion's quantum q_F (row 29).
6. The phase per age, the pair form of `phase_per_link` (row 24).
7. The one sentence at the head of ENGINE.md: the physical path is the
   six verbs on integers and nothing else, gated by
   `tests/test_integer_algebra.py`.
8. Two status rows of the identities table corrected from the code:
   `optical-v1` runs under its key (`world._optical` :3755-3817, the
   identity at :1387) and `covariant-readings-v1` under `covariant_readings`
   (`world.COVARIANT_READINGS_RULE` :561, `engine.covariant_frame`
   :218-273), as the Highlights Pruner noted in record 813.

## Links

- [ALGEBRA.md](../atom_algebra/ALGEBRA.md) sections 0 and 5 (the atom's
  integers and its three-tests table); [the baseline run](https://github.com/Closer24/Universe24/blob/01e8618379c1d54e696ce3c7d6a8f9bb2fd1fe21/docs/designs/atom_baseline/RUN.md)
  section 1 (the world as registered).
- [STEP_ALGEBRA.md](../light_bending/STEP_ALGEBRA.md) section 2 (the
  inputs table of the key `optical`); [flow_weight/DESIGN.md](../flow_weight/DESIGN.md)
  sections 1.1 and 1.2 (the flow label).
- [ARCHITECTURE.md, the operations of the law](../../ARCHITECTURE.md#the-operations-of-the-law);
  [ENGINE.md](../../ENGINE.md); [BEAM_LAW.md](../../BEAM_LAW.md) sections 2
  to 5 and notes 17, 23, 25, 30, 31, 33, 35, 37, 41, 45, 46, 48.
- [the log](../../LOG_2026-09-20.md) records 817, 894, 920 (and 929 on the
  Boss's records branch); [skills/workflow.md](../../../skills/workflow.md),
  "The three tests of every rule".
