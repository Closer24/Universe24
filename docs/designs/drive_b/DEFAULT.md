# The line drive as the law's default: form B moves from the key `drive_b` to `beam-v1`'s drive, the per-axis drive kept for history under the key `per_axis_drive`

The Drive Default Builder's design note, 2026-09-22, on the model owner's
decision of the same day (record 972 of
[docs/LOG_2026-09-20.md](../../LOG_2026-09-20.md), once merged; the
owner's words: "definitely type B should be the default for now because
that is the most common"), through the Boss. Step 1, documents only: no
engine line, no world file, no run, no pin moved. The rule it makes the
default is form B in the integer form (c) as built under the key
`drive_b` ([DESIGN.md](DESIGN.md); BEAM_LAW note 49; HYPOTHESES 28;
[light_speed/FORM.md 3.1](../light_speed/FORM.md#31-amended-after-the-physics-rule-review-of-the-build-m1-the-residue-across-lines-and-the-correction)),
which the owner asked about (record 970) and asked to be tested as the
generic rule it is (record 971). The owner's earlier word of record 955
(the centred step and form B as the default decided together after the
paper, one re-pin campaign) is the frame this note fills: this is the one
design that reads both (section (e)); the centred step's default is not
decided here. Every number below is a HOST computation from the
register's world files through the engine's own loader
(`event_universe.world_loading.load_world`, `world.drive_wall`,
`world.step_divisor`; the two scans are described in section (b)) or a
derived pin, labelled; nothing was run.

## The six lines

1. **The information.** Unchanged from the key's build: a body's step
   moves its own record from its Node to the neighbour through the Port
   of one axis, at most one Link per interval, three signed accumulators
   `drive_a` on the record gaining `p_a Q` per self-creation against ONE
   wall `W = Q^2 S M + |p|_1 T_h` (`T_h = isqrt(3 Q^2) = 110`; `Q^2 S M`
   under `covariant_readings`), the axis furthest over the wall stepping.
   What moves is WHO reads it: today a world that declares `drive_b`;
   after the flip every world that declares nothing, that is the law.
   Kept: the three rows of the counts table, the record's fields. Lost:
   nothing; the per-axis drive (BEAM_LAW note 17, `step_axis`, the
   coincident fire dropped) stays in the engine under the explicit key
   `per_axis_drive`, for the history's controls and replays.
2. **The generic solution.** One motion primitive for a body as for a
   row (record 183) becomes the law's text: `core.integer.by_line` on the
   body's momentum is the rows' own argmax carry (note 41 (viii)), one
   primitive for every family, the engine branching on no name. The flip
   is one boolean's polarity in `engine._move` and `world.py`: the line
   rule is the branch taken with nothing declared, the per-axis rule the
   branch taken under a declared identity; no second primitive, no
   default written into the parser's silence (Highlights head item 10:
   every key absent by default is a hypothesis, and the law's own default
   is stated in the law's file, BEAM_LAW note 17 rewritten).
3. **Why it works.** On the GameBoard nothing new happens: the six
   deciding worlds of series X read the line drive at their pins (ticks
   51, 101, 152 on face:+x from (40, 20, 20), (40, 40, 20), (40, 40, 40),
   DETECTOR, 19 of 19 readings inside) and the per-axis controls at 36,
   50, 65. The reading that shows the flip: `drive_b/plane_b` run with no
   key clicks at 101 from (40, 40, 20) (DETECTOR, the pin as registered);
   `drive_b/plane_main` run under `per_axis_drive` clicks at 50 from (40,
   20, 20), byte for byte its registered record. The reading that refutes
   it: a keyless world clicking at 50, or a control under the history key
   clicking at 101; a registered world outside the moving-body list of
   section (b) whose digests move.
4. **Why do it.** The owner's word (record 972: the most common case is a
   body off the headings, which the per-axis drive walks along one axis
   with the other axis's fires lost, DERIVATIONS_BEAM 1.3 item 7) and
   three defects the default carries today: (i) a body outruns its own
   family's rows above `|p| = 1.39 Q S M` (record 301; `orbit/s1_r12` at
   0.75 Links per interval per axis, HOST, above the rows' 0.5818); (ii)
   the covariant readings refuse every off-axis body (record 647); (iii)
   the atoms series (`atoms/hydrogen_r12`, `helium_r12`) and the first D3
   run were designed for form B's pace and are read today under the
   per-axis drive, so their register carries a drive their pins were not
   derived for (section (b)). Not done: the paper's rows on moving
   bodies stay read under a drive the owner has replaced, and every new
   world off a heading needs a key to move straight.
5. **The Highlights kept.** Records 183 and 301 (one motion primitive;
   form B on the conditional yes) are realised as the law by this flip;
   202 (the three tests) holds, the verdicts in section (f); 281 (only a
   detector's reading is a measurement) holds, every re-pin a click; 10
   (no implicit default) holds, the law's default in the law's file and
   the history's drive under a declared identity; 894 (no unnecessary
   checks) holds, the gate set replayed once per push and `--full` once
   at the end. Two lines change on the owner's word, as new lines naming
   the ones they supersede: the line of record 652 ("form B ... under its
   own identity, off by default") and the line of record 955 ("form B as
   the law's default ... after the paper") are superseded by record 972
   (form B the default now); the centred step's half of the 955 line
   stands (its default decided at the paper's close, section (e)).
6. **The implementation.** The tree (section (a)): `engine._move`'s
   branch inverted on `world.per_axis_drive`; `world.py`'s key `drive_b`
   deleted (an unknown key refuses at load naming the change), the key
   `per_axis_drive` parsed beside `centred_step`, `hypotheses` listing
   `per-axis-drive-v1`, `run.json` carrying `drive: "line"` or `"per_axis"`
   on every record; `_covariant`'s and `covariant_frame`'s one-axis
   refusals kept under the history key alone. The register (section
   (b)): 103 registered worlds carry a moving body (82 with a declared
   momentum, 21 whose free bodies at rest the rows push; HOST scan); 74
   of them are re-pinned and re-run, 24 keep every DETECTOR pin (the 21
   already under `drive_b`, the 3 covariant worlds), 3 are refused by the
   wall's bound and need the owner's word, 2 are deleted by PR #860. The
   documents: BEAM_LAW note 17 rewritten as the law's drive with note 49
   marked superseded and kept, ENGINE.md, TERMINOLOGY's identities table,
   HYPOTHESES 28's status, MIGRATION, TEST_EXPECTATIONS, EXPERIMENTS and
   VALIDATION rows per re-pinned series. Time, a HOST estimate (section
   (g)): the code flip with its tests and the gate set's digests 3 hours;
   the re-pin runs about 55 minutes of engine time in all (about 20 at
   four jobs), the generators' pins, the readings by kind and the
   register's rows 6 to 8 hours over the 13 series; the review 2 hours;
   end to end about two working days. Danger: medium. What can break:
   every registered moving-body reading (guarded by the pins declared by
   each generator before its run and the readings by kind), the three
   refused worlds (guarded by the load refusal naming the rule), a
   paper row read under the old drive cited as the new (guarded by the
   rule of section (d): every row names its drive). After the flip no
   key stays off: the law has one drive, and `per_axis_drive` is the
   history's, off by default.

## (a) How the default flips, with no implicit default

**The rule of Highlights head item 10.** Every key absent by default is a
hypothesis, named under `hypotheses` when declared; the law's own default
is stated in the law's file. So the flip is not "the key's default becomes
true": the key `drive_b` ceases to exist, the line drive is written into
BEAM_LAW note 17 as the drive of `beam-v1`, and the drive the law had
until this day becomes a declared identity.

**The law's drive.** BEAM_LAW note 17 ("the step by the momentum") is
rewritten: a free body at a self-creation steps by the line rule of note
49 (the three accumulators, the one wall, the argmax carry, `by_line`),
with note 49's text folded into it; note 49 stays in the file marked
"superseded on <date>: the rule of this note is the law's drive since
record 972, note 17" (Highlights 5.4's rule: marked, never deleted, record
941 (4)). The identity `drive-b-v1` leaves the identities table of
TERMINOLOGY.md as a hypothesis and is written in its "retired" list with
the date; HYPOTHESES 28 keeps its statement with the status "entered the
law on <date> (record 972)". `world.py` loses `DRIVE_B_RULE`,
`NatureBeamWorld.drive_b` and the parser's `drive_b` branch; `drive_wall`,
`T_HEADING` and `by_line` stay where they are, now the law's.

**The history's drive, declared.** The per-axis drive of note 17 as it ran
on main until the flip (`step_axis`, `step_divisor` with the cap
`|p_a|`, `by_drive` per axis, the coincident fire lost) is kept in the
engine under the world key `per_axis_drive` (a boolean, false by default,
any other type refused at load naming the key) and the identity
`per-axis-drive-v1`, listed under `hypotheses` after `optical-v1` and
before `centred-step-v1`, with the status in TERMINOLOGY's identities
table "history: the law's drive from 2026-09-19 (note 17) to <date>
(record 972); declared by the register's controls and by a replay of a
reading registered under it". It is a declaration of history, not a new
hypothesis: nothing is claimed for it, and nothing new is derived under
it.

**What every world reads.** A world that declares nothing reads the line
drive. A world that declares `per_axis_drive: true` reads the per-axis
drive byte for byte as main runs it today (the gate set's digests of the
controls prove it, section (f)). A world that declares `drive_b` is
refused at load by the parser's known-key set, with the message naming
the change ("`drive_b` is the law's drive since <date> (record 972);
declare nothing, or `per_axis_drive` for the drive of history"), so that
no registered or hand-written world carries a stale key in silence. The
21 worlds that declare `drive_b` today (the six of series X, the fifteen
body worlds of `optical/`) are rewritten by their generators without the
key; the three controls `axis_main`, `plane_main`, `cube_main` are
rewritten with `per_axis_drive: true`.

**The record names its drive.** `run.json` gains one field on every
record, `"drive": "line"` under the law and `"drive": "per_axis"` under
the history key, beside `law` and `hypotheses`; every `expectations.json`
entry of a series with a moving body gains a `drive` field in its
`derivations` map naming the drive its pin is derived under. A record or a
pin without the field is one from before the flip and was read under the
per-axis drive: the rule of section (d) for the paper.

**The engine.** `_move`'s head keeps one branch and inverts its
polarity: `if self.world.per_axis_drive:` the code of today's `else`
(the `counts.advance("drive", ...)` per axis with `step_divisor` and the
lost fire), `else:` the code of today's `if self.world.drive_b:` (the
wall, the rates, the bound before every addition, `by_line` with the
centred flag, the `action` row of the stepped axis). The one-axis
refusals of `_covariant` (at load) and `covariant_frame` (at the frame)
are raised only under `per_axis_drive`, their text unchanged but for the
key's name; a moving body under `optical` at gamma above 0 is refused
only under `per_axis_drive` (PR #855's refusal, section (e)). The body's
membership of the age wall's set at the coefficient gamma
(`DRIVE_MEMBER`, `measured.age_wall_set`) holds for every world under the
law and for none under the history key. No line of `nature_beam.py`, the
collision, the meeting, the push, the click or the books moves.

**The three verdicts of the flip itself** are in section (f).

## (b) Every registered world with a moving body, by series

**How the list was made (HOST, no run).** Two scans of every world file
under `examples/events/` (306 files parse as worlds through the engine's
loader on main at e5a980da; the entity, gate-set and expectations files
excluded): (1) every measured event with `fixed` false and a non-zero
`momentum` (82 worlds, "declared movers"); (2) every measured event with
`fixed` false, content above 0, `momentum` 0, in a world where rows exist
within the run (a lamp, a declared transit row, or a free family
releasing at the world's `release` rate within `ticks`), which the rows'
push can set in motion (21 more worlds, "pushed"; the register's READMEs
record their steps: alpha_square's p4 steps +y at tick 57, q4's rectangle
disperses at about 160, the coupling probes make 11 steps, the deuteron's
nucleons attempt 33 and 29 steps at contacts). Together 103 worlds in 20
folders (17 hold a declared mover; `binding/`, `weak/` and `coupling/`
hold pushed bodies alone). Since the merge of main on 2026-09-22 the moving
detector's six worlds (`moving_detector/`, PR #834's series, six declared
movers whose momenta are the per-axis pace 1/k exactly) are in the
register too, under the transient key `per_axis_drive` until their own
re-pin. A body's content M is `sum(held)` as the parser's load check
takes it; S the world's `width`; the pace per axis under the per-axis
drive `|p_a| / (Q S M + |p_a|)` (`step_divisor`, the cap on), under the
line drive `|p_a| Q / W` per axis and `|p|_1 Q / W` Manhattan
(`drive_wall`); their ratio on a heading is `1 / (1 + 0.72 v)` with `v`
the per-axis pace (FORM.md 3.1 (c)), the same on every heading; off the
headings the line of **p** replaces the axis staircase with its lost
fires (the ratio in the table is Euclidean pace over Euclidean pace).
The wall `W` is tested against the law's bound `2^62 - 1`
(`world.MOMENTUM_BOUND`, `drive_wall`), the products by division before
they are formed.

**Which pins move.** Every declared mover of the register moves on a
heading (82 of 82 have `|p|` on one axis, the six of series X apart:
three off the headings under the key already). So the rule is one line:
on a heading a pin's pace becomes `1 / (1 + 0.72 v)` of today's, the
cap `64 / 110` never reached by a registered body (the largest per-axis
pace of the register, `orbit/s1_r12` at 0.75, becomes 0.487); off the
headings (a pushed body, an orbit's turn) the path becomes the digital
line of **p** with no fire lost, the pace `|p|_1 Q / W` Manhattan. What
does not move: a pin under `covariant_readings` (the cap term keyed off:
`by_line` with the wall `Q^2 S M` fires at the same self-creations as
`by_drive` against `Q S M`, integer for integer, the accumulator's unit
alone scaled by Q, so every DETECTOR reading of series S stands and only
the GameBoard's `drive` values and the digests move); a pin already under
`drive_b`; a fixed body; a body of no content.

The table, grouped by series (the register's letter, the folder). Ratio
is the line drive's pace over today's per-axis pace at the world's
declared momentum, HOST; "T" the run time per world the register records
for the series (host seconds, from the series' README or its EXPERIMENTS
entry); "pins" what the generator re-declares (section (c)).

| Series, folder | Worlds with a moving body | Their bodies (HOST: per-axis pace, line pace, ratio) | What moves | T per world |
| --- | --- | --- | --- | --- |
| H, `bohr/` | 7: `r2`, `r4`, `r6`, `r8`, `r12`, `r15`, `r16` | the electron (M 1836, S 45120) on a heading at 0.1077, 0.0854, 0.0684, 0.0600, 0.0516, 0.0466, 0.0493 becomes 0.1000, 0.0805, 0.0652, 0.0575, 0.0497, 0.0451, 0.0476 (ratios 0.928 to 0.968) | the orbit's period, the closure `4 p r = j h` (j = 2.000 at r = 8 with `h = 16 p(8)` re-fixed under the line pace), the lines' clicks | 19 to 87 s |
| H (the atoms), `atoms/` | 3: `hydrogen_r12`, `hydrogen_r12_centred`, `helium_r12` | the electron at 0.0525 (0.0506, ratio 0.964), the two electrons of helium at 0.1175 (0.1084, 0.922); their momenta were derived for form B's circle (README, PINS.md) and registered under the per-axis drive | the pins of PINS.md become the ones the drive matches; the centred world reads both keys' interaction (section (e)) | 71 to 77 s (RUN_CENTRED.md) |
| D, `orbit/` | 8: `s1_r12`, `s1_r24`, `s8_r12`, `s8_r24`, `s32_r12`, `s32_r24`, `s32_r12_lamp`, `s32_r24_lamp` | the probe at S = 1: 0.7500 becomes 0.4873 (0.650, the registered defect of record 301 closed); S = 8: 0.3846 to 0.3013 (0.783); S = 32: 0.2195 to 0.1896 (0.864); the lamp worlds 0.2381 to 0.2033 (0.854) | the circle's n (the root of `n x pace(n) = q L C / (2 pi)` under the line pace), T, the mean radius, C; every reading GAMEBOARD (records 562, 564) | 3.9 to 6.5 s |
| D3, `orbit_lamp/` | 5: `r12`, `r24`, `r24_4m`, `r12_control`, `r24_control` | the probe at n = 9: 0.2195 becomes 0.1896 (0.864); the generator's circle under the line drive is n = 10 at 0.2033 (`pace(n, S, DIRECTIONAL_DRIVE)`, already written) | T(12) 343 becomes 371, T(24) 687 becomes 742 (the first run's pins, kept in the README as history), the ratio 2.00 +- 0.18 unchanged, the controls' escape tick 278 +- 6 becomes the 61st Link at 0.2033 (about 300), the equivalence pin unchanged in form; the paper's D3 row (section (d)) | 14 s |
| G, `hubble/` | 4: `coasting_age`, `coasting_scalar`, `pushing_age`, `pushing_scalar` | four thrown bodies (M 64 or 1024, S 2^20) at 0.0499, 0.1496, 0.2494, 0.3491 become 0.0481, 0.1351, 0.2115, 0.2791 (0.965, 0.903, 0.848, 0.799) | every star's z and the diagram's slope (DETECTOR, the pointer's clicks) | about 40 s |
| G2, `hubble_stars/` and `hubble_stars/record/` | 18: `coasting_none`, `coasting_age`, `coasting_scalar`, `double_none`, `double_age`, `double_scalar`, `gravity_none`, `gravity_age`, `gravity_scalar`, and the nine `record/` worlds | 24 stars per world (M 4198400 or 8392704, S 2^20) at 0.0333 to 0.0667 become 0.0326 to 0.0636 (0.977 to 0.954) | the redshift per star (about 2 to 5 percent slower), the deceleration q read from the diagram (the paper's rows 3 and 4b, section (d)) | 36 to 41 s |
| S, `covariant/` | 3: `j4_muon_3640`, `j4_muon_12856`, `coasting_none_covariant` | the muon at 0.2748 and the stars at 0.0345 to 0.0588: ratio 1.0000 exactly (the cap keyed off) | no DETECTOR pin (the 64th self-creation at 70 and 124, the clicks at 369 and 345, z = 0.3674 stand); the `drive` accumulators x64 on the `step` lines and in `state.json`: the bit-exact replays of `test_covariant_readings.py` re-pinned | 0.3 s, 0.3 s, 43 s |
| the clocks, `crowd_clock/`, `cluster_clock/`, `reader_clock/` | 5: `moving_08`, `moving_1`, `moving_3`, `cluster_moving`, `alike_receding` | the source at 0.1164 becomes 0.1074 (0.923); the masses at 0.0618 to 0.1058 become 0.0591 to 0.0983 (0.93 to 0.96); **three worlds REFUSED at load under the line drive**: `moving_1`, `cluster_moving` and `alike_receding` carry a mass of content M = 2^30 at S = 2^20, whose `Q^2 S M = 2^62` passes the bound `2^62 - 1` by one (HOST; `drive_wall` refuses naming the rule) | the readings of the two admitted worlds move a few percent; the three refused need the owner's word: the mass's content or the width lowered by one bit (M 2^29 at the same momentum per unit) and re-pinned, or the three left as history under `per_axis_drive` | 1.4 to 3.3 s |
| the two stars, `two_stars/` | 3: `rest_frame`, `symmetric`, `symmetric_pass` | the star at 0.2327 becomes 0.1994 (0.857); the pair at 0.1164 becomes 0.1074 (0.923); `rest_frame` holds one free body at rest beside two sources | the arrival ticks and the frames' ratios (2 / 3, the README) | seconds (the README records no time; 201 x 3 x 3, 500 intervals) |
| I, `nucleus/` | 8: `deuteron_1_kick`, `deuteron_3` (declared, 10^12 on a heading at 0.0307 becomes 0.0300, 0.978); `alpha_line`, `alpha_square`, `deuteron_1`, `pp_1`, `pp_1_weak`, `pp_3` (pushed) | the pushed bodies at paces of order 0.03 (ratio about 0.98); the dispersal's first steps (15, 33, 57, 68 in the README) shift by a few intervals and the pushed path becomes the line of the push's resultant | the steps' ticks and the separations (GAMEBOARD), the border's clicks (DETECTOR) | 4 to 87 s |
| R, `quarks/` | 7: `q6_proton_kick` (declared: the kicked u at 0.1853 becomes 0.1635, 0.882: a Link every 6.1 intervals in place of 5.4); `q1` to `q5`, `q7` (pushed) | q3's dispersal by 25 to 60, q4's at about 160, the lines' "no step in 3000" expected to stand (the per-axis count fires at the same |p_a| threshold scaled) | the face clicks' ticks, the read mass unchanged | 10 min 37 s for the seven at two jobs |
| N, `binding/` | 3: `alpha_square_bond`, `deuteron_bond`, `proton_bond_lamp` (pushed) | B3's dispersal (p4 +y at 81, n2 at 89, p1 -y at 95, n3 -x at 111) shifts with the pace | the give at the contact (the tick of the first contact), the border's clicks; the paper's rows 7a and 7b rest on these (section (d)) | 13 to 53 s |
| J3, `weak/` | 3: `j3_deuteron`, `j3_deuteron_crowd`, `j3_neutron_free` (pushed) | the nucleons attempt 33 and 29 steps at contacts (0 Links either way); the count of attempts and the `drive` accumulators move | the `become` blocks by the clock unchanged in form; the digests of the gate world `weak/j3_deuteron` move (section (f)) | about 1.5 min for the three |
| C, `coupling/` | 3: `1b_m1`, `1b_m4`, `1b_m16` (pushed free probe) | the probe's 11 steps in 200 intervals (a pace about 0.055, ratio about 0.96): 10 or 11 steps | the front and the push readings unchanged (rows); the probe's steps (GAMEBOARD); the gate world `coupling/1b_m16`'s digests | 19 to 102 s |
| X (Y after PR #863), `drive_b/` | 6: `axis_b`, `plane_b`, `cube_b` (under the key today), `axis_main`, `plane_main`, `cube_main` (the controls) | the three `_b` worlds rewritten without the key read the same integers (51, 101, 152); the three `_main` rewritten with `per_axis_drive: true` read 36, 50, 65 byte for byte | no pin moves; the generator's `key` argument becomes the history key on the controls | 0.10 s |
| the optical bodies (PR #813), `optical/` | 15: `body_b{10..18}_g{0,1}`, `body_control_b{10..18}` (under `optical` and `drive_b` today; the pace 0.3678 on a heading, the control's click at 150 from (56, 20 + b, 20)) | rewritten without `drive_b`; every pin of BODY_DRIVE.md section 4 stands (already the line drive's) | no pin moves; a byte-identity replay at the flip proves it | 11 s |
| the thin worlds, `catalog/`, `gallery/` | 2: `catalog/sun_planet` (0.1869 becomes 0.1648, 0.882), `gallery/proton_electron` (0.6945 becomes 0.4633, 0.667; three bodies pushed) | deleted by PR #860 (the owner's strike, record 894) | not re-pinned; if PR #860 has not merged when the flip lands, they are re-run once under `per_axis_drive` for their pages, never re-pinned | seconds |

The count: 103 worlds with a moving body; 74 re-pinned and re-run (H 7,
the atoms 3, D 8, D3 5, G 4, G2 18, the clocks 2, the two stars 3, I 8,
R 7, N 3, J3 3, C 3); 24 whose DETECTOR pins stand (X 6, the optical
bodies 15, S 3, of which S's digests move); 3 refused at load until the
owner's word (the clocks' heavy masses); 2 deleted by PR #860. Beside the
register, PR #879's four D3 worlds under `flow_link` (`r12_flow`,
`r24_flow` and their controls, pinned at the whole n = 8, the per-axis
pace 8 / 40 = 0.2, the momentum 538968064 = 8 x 64 x (2^12 + 2^20),
`expectations_flow.json`) join
series D3's re-pin if PR #879 lands before the flip (section (e)). Every
other registered world (amplitude, bell, buildup, c_measured, clock_word,
detector, hand, heisenberg, lensing, masses, massive_rows, redshift,
shell_clock, weak's J1 and J2, the crowd and reader clocks' rest worlds,
optical's light worlds, the root's four) carries no free body with
content and momentum, or no rows that could push one, and reads byte for
byte as today: the gate set's digests of those worlds are the proof
(section (f)).

## (c) The pins re-declared by each generator before any run

The rule of record 281 and of the register's head: the pins declared,
then the run, the reading by kind, nothing moved after. For every series
of the 74 the order is one commit of the generator's pins, then one run,
then one commit of the readings.

- **The generator.** Each `make_worlds.py` of the 13 folders of the 74
  (the clocks' one admitted folder `crowd_clock/` among them; the other
  two clock folders hold only the refused worlds) gains the
  line drive's pace as its `pace()` (the orbit_lamp generator already
  carries both, `AXIS_DRIVE` and `DIRECTIONAL_DRIVE`; the others compute
  `n / (S + n)` or read the engine's `step_divisor`) and derives its pins
  from it: the circle's n where a circle is declared (H, the atoms, D,
  D3), the period `2 pi r / v`, the escape tick at the 61st Link, the
  arrival ticks of thrown bodies (G, G2, the clocks, the two stars), the
  dispersal's first step where a push's resultant is known from the
  design (I, R, N, C, J3: the pace at the design's push, the tick of the
  first Link `ceil(W / (|p_a| Q))` after the push). Every pin is written
  into `expectations.json` (the series that lack one, H, D, G, I, N, J3
  and C, get one in the register's format of `orbit_lamp/`, with a
  `derivations` map naming the formula and the drive) with the field
  `drive: "line"`, before any run. The generator keeps the per-axis
  derivation as a function (`pace(n, S, "per_axis")`) so that the
  history's pin is reproducible from the same file, and the README's
  table keeps the registered reading under the per-axis drive as a row
  marked "history (per-axis drive, <fingerprint>)": the old integers are
  kept (record 301's WHAT MOVES; record 894's rule for the tests).
- **The reading by kind.** Each series' readings tool
  (`tools/click_readings/` after PR #860; today `tools/<series>_readings.py`)
  reads the run against the new pins; every line DETECTOR or GAMEBOARD;
  the drive's accumulators, `fast_steps` and `axis_steps` are GAMEBOARD
  and never pinned; the escape click's tick is GAMEBOARD where PR #863
  names it so and DETECTOR (the face and the Node) otherwise. A reading
  outside its pin is reported with its numbers and its cause and moves no
  number: the register's row says PASS, FAIL or OUTSIDE by kind, as the
  D3 row does today (the circle's period outside its pin, kept).
- **The controls.** Where a series carries a control that must stay the
  history's (the three `_main` of X), the control declares
  `per_axis_drive: true` and keeps its pin; no other series needs a
  history control, since the history's reading is the register's row as
  it stands, with its fingerprint.
- **The centred column.** Because the owner decided the centred step and
  form B together (record 955, section (e)), every generator's
  `expectations()` takes `(drive, centred)` and writes the line drive's
  pins with `centred: false` now, and the same function gives the pins
  with `centred: true` when the owner's word comes, without a second
  design: the centred start moves the first fire of every body by half a
  wall (the deciding world's click 35 against 36 under the per-axis
  drive, `test_centred_step.py`; under `by_line` the 21st fire at 50
  against 51).

## (d) The paper's rows that read under the drive

The paper on PR #802 (`paper/general_formula/main.tex`, NUMBERS.md) was
read under the per-axis drive at the fingerprints its tables carry. The
rule this design asks for: every row that rests on a moving body names
the drive it was read under, in the cell that names its series and
fingerprint ("series D3 at `<fingerprint>`, the per-axis drive"), so that
the paper as it stands stays true, and the re-read under the line drive
is a new reading beside it, as row 4b already carries series S beside
series G2. Appendix C's dated transitions (record 812) gain one line, "the
line drive the law's drive (<date>, <SHA>)". The rows, from the tree
(HOST, the lines of `main.tex` at 6f953920):

| Where | The row | Rests on | What the flip does |
| --- | --- | --- | --- |
| Table `tab:checks` | the equivalence principle after a detector; the 1 / r force's scale symmetry (series D3: the same x on 138 of 139 birth ticks, T(24) / T(12) = 1.997, the controls at x = 60 + r, the escape 278 +- 6; the circle's period, amplitude and omega^2 outside their pins) | `orbit_lamp/` (per-axis, n = 9) | re-read at n = 10 under the line drive (T 371 and 742, the generator's own): a second row beside the first; the "outside" verdict of the circle's period re-read |
| Table `tab:checks` | the covariant readings (series S: the clicks 392, 369, 345; z = 0.3674) | `covariant/` | stands: no DETECTOR reading moves (the cap keyed off); the row names the drive as "either drive, the same integers" |
| Table `tab:nature` row 3 | the deceleration q_0: -0.108 coasting (series G2, the pointer's z) | `hubble_stars/` | re-read: every star 2 to 5 percent slower under the line drive; the FAIL's number moves, its verdict is read again |
| Table `tab:nature` row 4b | a moving lamp's redshift z = 0.2636 at beta = 0.2674 (series G2); under covariant-readings-v1 0.3674 (series S) | `hubble_stars/`, `covariant/` | the G2 half re-read (the star's pace 0.0667 becomes 0.0636, HOST); the S half stands |
| Table `tab:nature` rows 7a, 7b | the deuteron's binding fraction 0.109 percent; the alpha's binding over the deuteron's 2.0 (series N, the border's clicks; the give once per body) | `binding/` (pushed bodies) | re-read: the first contact's tick moves with the pace, so the give's tick and the border's clicks may move; the rows' verdicts (BOUND, FAIL) read again |
| Table `tab:nature`, the rows "by a pin without its run" (4a the muon in flight, 6 Bohr's ratio) | pins, no run | the pace per axis | the pins re-derived under the line drive before any run of theirs; the rows' status unchanged |
| The ledger row (line 346) | "A body's dispersion, its momentum's fraction; the moving clock's rate 1 ... the drive per axis, the owed count ... exact ... 4.3, 4.4" | the law's text | the row names the line drive (`|p|_1 Q / W`, exact) and cites note 17 as rewritten; the per-axis fraction stays in DERIVATIONS 4.3 and 4.4 as the history's |
| The law's statement (lines 162 to 163, 185, 192, 242, 265) | the drive per axis, the rate `|p_a|`, the wall `N_l N_w M + |p_a|`, one Link per interval | the law's text | rewritten to the line drive: three accumulators, one wall `N_l^2 N_w M + |p|_1 T_h`, the argmax carry; the paper's symbols table gains `T_h` |
| The discussion (line 589) | "a body can outrun its own field's rows on the drive as built on main" | the defect of record 301 | true of the per-axis drive, dated; under the line drive no body outruns its rows (the cap `64 / 110`) |
| The open table (lines 1299 to 1300) | "a closed orbit's period at two radii under the directional drive (form B, not built)"; "the off-axis runs pending" | the tree's state | "form B built (PR #813) and the law's drive since <date>"; the off-axis covariant runs no longer refused at load |
| The appendix's derivation record (NUMBERS rows 100, 115, 118) | Table 1's cells from series D and H; series H's closure at r = 8, j = 2; series H's 2.041 to 2.000 | `orbit/`, `bohr/` | re-read under the line drive as second rows; the first rows stand with their drive named |
| The optical bodies (PR #813, BODY_DRIVE.md; the paper's one sentence on form B, records 952 and 953) | the body worlds' clicks (159 to 168 at gamma 0 and 1; the fall in pixels) | `optical/body_*` | stand: read under `drive_b`, that is the line drive; the sentence names the drive as the law's |
| NUMBERS row 91 | the Lorentz dispersion under form B in the map (design) | the map | stands |

The paper's writer takes the rows on the merge SHA of the re-pin
campaign, never before (the rule of record 955 (2) and the paper's
merge rule of record 941 (6)); until then the paper cites the per-axis
rows as they are, each with its drive named.

## (e) The interaction with the centred step, PR #855, PR #854 and PR #879

- **The centred step (`centred_step`, `centred-step-v1`; record 941
  (4)'s rule on 5.4, record 954's reading, record 955's decision).** The
  key stays a key. Its threshold is already a parameter of `by_line`
  (`wall - wall // 2` under the key, the whole wall without it), so the
  flip changes nothing of it: a keyless world reads the line drive
  started at the whole wall, `centred_step: true` reads the line drive
  started at the half (`atoms/hydrogen_r12_centred` today reads the
  per-axis drive centred; after the flip the line drive centred, its
  registered run kept as history and its pins of CENTRED_STEP.md section
  4 re-derived, the loop's lag pump smaller by `(|p| / S_1)^2` off the
  axes, the reviewer's line of record 955). Its default is decided at the
  paper's close, not here; the generators' `(drive, centred)` argument
  (section (c)) makes that decision one more column of the same
  campaign, and the engine's `_move` gains no branch for it.
- **PR #855 (generic-bending): the flight in the age wall's set at 1 +
  gamma for every world; `drive_b` beside the law's flight.** On that
  branch the `optical is not None` gate in `_move` is removed and the
  body's drive is a member of the age wall's set at the coefficient
  gamma under `drive_b`, a moving body at gamma above 0 without `drive_b`
  refused at load. After the flip the same lines read: the drive a
  member at gamma for every world under the law (gamma 0 by default, the
  coefficient 0, the member declared unstretched, no wall function
  called); under `per_axis_drive` no member, and a moving body at gamma
  above 0 refused at load naming the history key. PR #863's
  `stretched_drive` bound (the stretched wall and rates against the
  working bound) applies to every world at gamma above 0. The flip's
  branch merges main after PR #855 lands and resolves `_move`'s block by
  hand once (the Boss's order: the code flip starts only after #855,
  #854 and #879 are on main).
- **PR #854 (flow-link-v1): the flow label per Euclidean Link under
  `flow_link`.** A key on the rows' flow sums (`nature_beam.py`), which
  enter a body's push and so its momentum; the drive reads the momentum
  and nothing of the flow. No shared line; the two compose by
  declaration. The ring worlds carry no moving body.
- **PR #879 (Newton under the one constant): series D3's four worlds
  under `flow_link`.** Four more worlds with a moving body (the probe at
  the whole n = 8, the per-axis pace 8 / 40 = 0.2; their pins in
  `expectations_flow.json`, derived under the per-axis drive as the file
  says: T(12) in 343 .. 411, T(24) in 686 .. 822, the controls' escape
  299 .. 311). They are read under the per-axis drive on that PR; when
  it lands they enter D3's re-pin under the line drive with the pin the
  generator's own derivation gives, not the registered worlds' n = 10:
  under `flow_link` the circle's balance is divided by the plane's flow
  constant, so the line drive's root is `n^2 / (S + 1.71875 n) = 1.4838`,
  n = 8.28, the whole 8, the pace `8 x 64 / (64 x 32 + 8 x 110) = 8 /
  45.75 = 0.1749`, T(12) = 431 and T(24) = 862 (the reviewer's
  arithmetic, HOST; the generator decides the pin), as a second reading
  beside the first, and their FAIL (the ratio 1.677) is re-read under
  the law's drive.

## (f) The three tests on the switch; the byte-identity tests that change

**The three tests of the flip** (record 202; the rule itself passed them
in DESIGN.md section 3 and BEAM_LAW note 49):

1. **Generic: PASS.** The law's drive is one primitive with the declared
   integers `p_a`, M, S and the constants Q, `T_h`, for every family; the
   engine branches on a declared identity (`per_axis_drive`), never on a
   name; the default is written in the law's file, not in the parser's
   silence.
2. **Vector: PASS.** Unchanged: the translation of three accumulators by
   their rates, one comparison, one Euclidean division with the
   remainder kept; no root at run time (`T_h` at load), no float. The
   flip adds no verb.
3. **Local: PASS.** Unchanged: the body's own record and the world's
   constants; fixed work and storage; nothing at a Node; every host
   reading labelled GAMEBOARD.

**The byte-identity register that changes** (`examples/events/gate_set.json`,
read by `tests/test_amplitude_click.py` (d), `tests/test_drive_b.py`
(a), `tests/test_covariant_readings.py`, `tests/test_centred_step.py`
(a), `tests/test_nature_beam_worlds.py`; record 894's rule: the former
values kept, none deleted). Of the 17 gate worlds, by the scan of
section (b):

| Gate world (cap) | Under the flip | The digests |
| --- | --- | --- |
| `bohr/r2` (689) | a declared mover | move; the former kept |
| `nucleus/alpha_square` (180) | pushed bodies (p4 steps by 57) | move; the former kept |
| `hubble/pushing_age` (1) | four declared movers; at the first self-creation the accumulators hold `p_a Q` in place of `p_a` | `state.json` moves; the former kept |
| `coupling/1b_m16` (25) | the pushed probe | expected to move (its first steps within 25 intervals); the former kept |
| `weak/j3_deuteron` (700) | the nucleons' attempted steps and accumulators | move; the former kept (they moved once under clock-age-v1 already, the entry says so) |
| `weak/j3_deuteron_crowd` (1) | pushed, but no push before tick 2 | expected unchanged; the replay decides |
| `drive_b/plane_b` (200) | under the key today; declares nothing after | expected unchanged (the record's `hypotheses` and `drive` lie outside the three digests); the replay decides |
| `detector/grouped_12_nodes`, `weak/j2_ladder`, `hand/wu` | no moving body | unchanged: the byte-identity proof of the flip for a world without a moving body |
| the seven lamp worlds without digests | no moving body | unchanged |

Each moved entry keeps its former digests beside the new ones under the
key `former` with the cause and the date (`{"digests": {...}, "drive":
"per_axis", "moved": "<date>, record 972"}`), as JSON has no comments;
the tests keep the former integers in comments (record 894). Beside the
gate set: the bit-exact replays of series S
(`test_covariant_readings.py`, the J4 runs and the coasting run at its
cap) are re-pinned for the accumulator's unit alone, with the DETECTOR
assertions of those tests unchanged, the former digests in comments;
`test_drive_b.py` (a) inverts (every world outside the three controls
parses with `per_axis_drive` false and the identity absent; the controls
with it; the gate world's digests as before; `run.json` with `drive:
"line"`), (c) and (d) unchanged, (f) gains the refusal of `drive_b` by
name, (g) reads the admission without a key; `test_optical_body.py`'s
"a moving body under optical needs the directional drive" becomes "is
refused under `per_axis_drive` at gamma above 0"; `test_step_drive.py`
and `test_push_width.py` keep their per-axis integers on worlds that
declare `per_axis_drive` (the primitives `step_axis` and `by_drive` are
tested as they are) and each gains one case under the law (the width-8
body at n = 1 stepping once per 9.72 self-creations, HOST, in place of
once per 9; the box body's 21st fire at 51); `test_centred_step.py`'s
deciding world reads `by_line` centred (the click at 50 against 51);
`test_crossing.py`'s `fast_steps` cases, `test_coupling_readings.py`'s
step replay and `test_binding.py`'s contact ticks are re-derived from
`by_line` before the run, every expected integer written first. New:
one test that a world declaring `drive_b` is refused naming the change,
one that `run.json` names its drive under both, one that the three
controls replay their registered digests under `per_axis_drive`.

## (g) The order of the build after the design; the estimate

The build starts on the Boss's word, after the physics-rule reviewer's
ADMISSIBLE on this note and after PRs #855, #854 and #879 are on main
(PR #860's deletions before it if the Boss orders so, since they remove
two moving-body worlds and move the readings tools). One writer on the
branch `drive-default`; one push per step; `python tools/check.py --base
origin/main` per commit, `--full` once at the end (record 894).

1. **The code flip, tests first** (one commit of the failing tests, one
   of the code, one of the documents and the gate set): `world.py`,
   `engine.py`, `measured.py` where `age_wall_set` reads the key;
   BEAM_LAW note 17 rewritten and note 49 marked; ENGINE.md,
   TERMINOLOGY (the identities, the retired list), HYPOTHESES 28,
   MIGRATION's entry, TEST_EXPECTATIONS, CHANGELOG, docs/README.md; the
   21 worlds rewritten by their generators (X and the optical bodies);
   the gate set replayed once (`tools/run_series.py --list
   examples/events/gate_set.json --fast`, about a minute) and its moved
   digests re-pinned with the former kept. HOST estimate: 3 hours
   including the merge of main over #855's `_move` block.
2. **The re-pin runs, series by series**, in the order of the paper's
   dependence, each series one commit of pins and one of readings: D3
   (14 s x 5, plus PR #879's four), H and the atoms (19 to 87 s x 10), D
   (6 s x 8), G2 (40 s x 18) and G (40 s x 4), S (the digests alone, 44
   s), I (4 to 87 s x 8), R (the seven at two jobs, 11 min), N (13 to 53
   s x 3), J3 (about 1.5 min), C (19 to 102 s x 3), the two stars and
   the two admitted clocks (seconds), then the byte-identity replays of
   the optical bodies (11 s x 15) and X (0.1 s x 6). Engine time from
   the register's recorded run times (HOST): about 55 minutes in all
   serial, about 20 minutes at four jobs; the host work around the runs
   (the generators' pins, the readings tools by kind, the READMEs'
   history rows, EXPERIMENTS and VALIDATION rows) 6 to 8 hours over the
   13 series. The three refused clock worlds wait for the owner's word
   and cost nothing until it comes.
3. **The CI as the gate**: green on every push; the reviewer reads the
   head again before the merge, since registered integers move (the
   rule of record 309 (4)); the Boss opens the pull request. The paper's
   writer takes the rows of section (d) on the merge SHA.

End to end, a HOST estimate: the code flip 3 hours, the runs and their
register 7 to 9 hours, the review 2 hours; about two working days with
one builder, the runs in parallel with the documents where the split of
files allows (record 894's rule: pages and runs apart).

**What this note needs from the Boss and the owner before step 2**: (1)
the reviewer's verdict on this note; (2) the owner's word on the three
refused worlds (`crowd_clock/moving_1`, `cluster_clock/cluster_moving`,
`reader_clock/alike_receding`: a mass of content 2^30 at width 2^20 whose
wall passes the law's bound by one; lower the content by one bit and
re-pin, or keep the three as history under `per_axis_drive`); (3) whether
the name `per_axis_drive` / `per-axis-drive-v1` stands; (4) whether the
centred step flips in the same campaign now or at the paper's close
(record 955: one decision; this note's generators carry both columns
either way); (5) PRs #855, #854 and #879 on main, and PR #860's
deletions if they go first.
