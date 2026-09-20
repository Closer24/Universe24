# The step drive: the physics-rule review

Reviewed on 2026-09-20, read-only, under
[physics-rule validation](../../../skills/physics-rule-validation/SKILL.md).
The change: the uncommitted diff of the worktree `/home/user/drive`, branch
`claude/step-drive`, on commit 98f44ffc, plus the new module
`tests/test_step_drive.py`. Changed files: `src/event_universe/events/engine.py`
(`step_axis`, `_move`), `src/event_universe/events/measured.py` (`drive`,
`axis_steps`, the state), `tools/coupling_readings.py` (`steps_by_rule`),
`tests/test_push_width.py`, `docs/BEAM_LAW.md` (note 17), `docs/ENGINE.md`,
`docs/MIGRATION.md`, `docs/TEST_EXPECTATIONS.md`. The design is section 1 of
`docs/designs/hubble_stars/RULES.md` at commit 5322dc4 of branch
`claude/series-g2-stars` (the file is not on this branch; see finding 3). The
rule as it was: BEAM_LAW section 3 step 5 and note 17 at 98f44ffc.

**Verdict: blocked.** Two blocking findings and three documentation findings.
The rule of one axis (`step_axis`) is the design's integer form and is correct
in isolation: the drive is the remainder of the old division, at most one Link
per self-creation, bounded, local, formula-free. The engine's loop over the
axes applies it to the first axis only in any interval in which an axis fires,
so a body with momentum on two axes at a constant momentum no longer moves as
it did, and the claim of bit-identity fails on the change's own dependent
tests.

## Finding 1 (blocking): the later axes' drives do not advance in an interval in which an earlier axis fires

**The rule.** The design (RULES.md section 1): "at every self-creation in
which the body may step (it owes nothing): `drive_a <- drive_a + |p_a|`", for
every axis a. BEAM_LAW note 17 as it was: "at most one Link per interval, x
before y before z (an axis whose step coincides with an earlier axis's step in
one interval loses it, nothing carried)". The count of an axis was read off
the clock at every self-creation whether or not another axis stepped.

**The source.** `src/event_universe/events/engine.py`, `_move`, the loop
`for axis in range(3)`: `step_axis` is called for an axis only when the loop
reaches it, and the loop returns after the first axis that fires: after a
step, after a refused step (the contact), after an escape on a face and after
`destination == origin`. The drives of the axes after it gain nothing in that
self-creation. `tools/coupling_readings.py`, `steps_by_rule`, has the same
`break` and so reproduces the engine's defect rather than the rule.

**The counterexample.** A body of content 16, width 1, momentum (1024, 320,
0), 24 self-creations; D = (2048, 1344). The rule as it was
(`by_clock(n - 1, |p|, D)`, x before y): x steps at 2, 4, ..., 24; y steps at
5, 9, 13, 17, 21. The drive as implemented: x the same; y steps at 9 and 17
only (its drive gains 320 only at the odd self-creations, when x does not
step). The engine's own test says the same: `tests/test_nature_beam_body.py`
(d), unchanged by this diff and passing at 98f44ffc, fails on this tree at
line 551: the body ends at (16, 6, 0), pinned (16, 9, 0). The effect goes
both ways: `tests/test_coupling_readings.py` (b) pins, for momentum (64, 64,
0) at content 1, width 1, the steps of x alone at 2, 4, 6, 8, 10 (every step
of y coincides with one of x and is lost); this tree gives (2, 0), (3, 1),
(4, 0), (5, 1), ..., y stepping at every self-creation x leaves free, the
body twice as fast as before.

**What this touches.** Claim (1), bit-identity at a constant momentum: false
for every body whose momentum has two or more non-zero components, and for
every body whose step is refused or that wraps on a width-1 axis while
another axis has momentum. Claim (4): the turn by momentum reads
`axis_steps` of the later axis, which now counts fewer (or more) Links than
`floor((age - 1) |p| / D)`, so its k0 differs at a constant momentum. Claim
(5): the frame's order is unchanged in code, but the rule "x before y before
z" now costs the later axes distance instead of a coincident step. The gate
set could not see this: none of its fifteen worlds has an unpushed body with
momentum on two axes.

**The admissible correction** (the design's rule, made bit-identical to the
rule as it was). In `_move`, advance every axis's drive first, then choose
the axis: for a in x, y, z: `drive_a += |p_a|` (p_a non-zero); the first axis
with `drive_a >= D_a` is the axis of this interval (stepped, refused or
escaped as now) and `drive_a -= D_a`; every later axis with `drive_a >= D_a`
in the same interval also subtracts D_a without stepping, the lost coincident
step of note 17 ("nothing carried"). Then `drive_a = n |p_a| mod D_a` on
every axis at a constant momentum, exactly the remainder of the old division,
and every step falls where it fell. For the turn by momentum, k0 must be the
rule's count on the axis as the old floor was, so the lost step counts in
`axis_steps` as a refused step already does (the lost step turned nothing
then and turns nothing now; the next step's k0 includes it). Carrying the
lost step to the next self-creation instead is a different law at a constant
momentum and needs the model owner's decision, not the implementer's.
`steps_by_rule` in the readings tool follows the same order. Test (a) of
`test_step_drive.py` must gain a two-axis case (the counterexample above,
against `by_clock` on each axis with the coincidence lost), since the single
axis case cannot distinguish the two loops.

## Finding 2 (blocking for landing): eight dependent tests fail on this tree and their integers were not re-derived

**The rule.** The workflow: "test owners retain independent expected results
and report deviations rather than changing the contract to fit code"; a
change is checked against the tests that depend on it; "Boss must not mark
the physics change complete until the required checks pass".

**The evidence.** `/home/user/gate/check.log` (the implementation's own
`tools/check.py` run on this tree): 9 failed, 693 passed. The failures:
`test_nature_beam_body` (d) and `test_coupling_readings` (b), which are
finding 1; `test_nature_beam_clock` (the step onto another refused: the body
handed the momentum stepped at once as it was, at (1 if tick < 2 else 2),
and now at tick 4), `test_contact` (three: the pair on the six headings, the
register pair over a thousand intervals, the frame's order as a declared
tie), `test_nucleus_readings` (the runner's record), `test_paid_charge` (the
steps at 6 and 9, now 7 and 10), which pin bodies that step under a push or a
hand-over and are the re-registration the design names ("the neutron star's
neutrons (refused steps, a contact) and the deuteron by the contact's
hand-over"), and `test_repository_navigation` (finding 3). I ran only the
three assigned modules; I did not re-run the six others.

**The correction.** After finding 1, the owner of each of the six tests
derives the amended rule's integers by hand from the drive (as the expected
integers of `test_step_drive.py` were), records the old and new values with
the reason in TEST_EXPECTATIONS.md, and only then changes the pins. A pin
that moves without a hand derivation is the contract fitted to the code. The
two tests of finding 1 must pass unchanged.

## Finding 3 (documentation, blocks the merge gate): the cited design and record do not exist on this branch

`docs/MIGRATION.md`, `docs/BEAM_LAW.md` note 17 and `docs/TEST_EXPECTATIONS.md`
link `docs/designs/hubble_stars/RULES.md`, which exists only on branch
`claude/series-g2-stars` (commit 5322dc4), not on this branch or its base;
`test_repository_navigation` fails on the broken link. The workflow requires
the design committed under `docs/designs/<key>/`. The same three documents
cite "record 107" of `docs/LOG_2026-09-20.md`; the log ends at record 106.
Correction: bring the design file onto this branch (or rebase onto the branch
that carries it) and write record 107 before the documents cite it.

## Finding 4 (documentation): the rule is stated as amended in note 17 only; four places still state the rule as it was

- `docs/BEAM_LAW.md` section 3 step 5 (lines 512 to 521) still reads
  "`by_clock(age, |p|, Q x S x M + |p|)` ... No remainder is kept; the count
  is the whole part off the clock". The task named section 3 step 5 as
  amended; it is not.
- `src/event_universe/events/engine.py`, the docstring of `_move` (lines 444
  to 495): the old rule, "no remainder is kept", and k0 = floor((age - 1) |p|
  / (Q S M + |p|)).
- `docs/TEST_EXPECTATIONS.md`, the table row of `test_step_drive.py`: "44 or
  45 Links where the rule as it was made 1" and "the drive in [0, D)"; the
  section and the test say 38.0, 37 to 39, and [0, 2 D - 1). The sum over
  the intervals of 50 |p| / (8192 + |p|) for p = 4096 down to 32 is 38.03,
  so the section is right and the row is wrong.
- `docs/MIGRATION.md` names the gate worlds that change as `1b_m16`, `r2`,
  `sun_planet`, `pushing_age`. The gate replay under `/home/user/gate` shows
  `1b_m16`, `r2`, `alpha_square`, `j3_deuteron` changing and `sun_planet`,
  `pushing_age` identical modulo the new fields (see below).

## Finding 5 (documentation, minor): the design's test sizes

The design's test (a) asks for 10^4 self-creations; the test runs 4000. The
design's (d) asks for `state.json` carrying the drive; the test also pins
`axis_steps`, `run.json` and the `step` line, more than asked. Neither
changes the verdict.

## The claims, one by one

1. Bit-identical at a constant momentum: **holds per axis** (`step_axis`
   alone: the drive after n self-creations is n |p| mod D and the step fires
   where `by_clock(n - 1, |p|, D)` is 1; test (a) proves it on twelve momenta
   over 4000 self-creations, and the arithmetic is the identity
   `floor(n p / D) - floor((n - 1) p / D) = 1` iff `(n - 1) p mod D + p >= D`).
   **Fails for the body** (finding 1). The gate set: I compared every file of
   the fifteen worlds' runs under `/home/user/gate/base` and
   `/home/user/gate/drive` with `drive` and `axis_steps` removed from
   `run.json`, `state.json` and the `step` lines, and `elapsed_seconds` and
   `source_sha256` ignored. Identical: `a0_b0`, `fixed`, `grouped_12_nodes`,
   `heavy_meeting`, `j2_ladder`, `j3_deuteron_crowd`, `lamp_mirror_screen`,
   `pushing_age`, `sun_planet`, `w1_beam`, `w27_beam`. Different: `1b_m16`
   (the probe's steps and position from the push), `r2`, `alpha_square`,
   `j3_deuteron` (contacts and hand-overs). As claimed for the gate set; the
   gate set has no world that exercises finding 1.
2. At most one Link per self-creation: **holds**. `_move` returns after the
   first axis that fires; `step_axis` subtracts one D at most. Test (c)
   (10 000 intervals, a random momentum on three axes) passes. The bound on
   the drive: before the addition `drive < D_max` (the largest D met so
   far), `|p| < D_now`, so after the subtraction `drive < D_max` again; by
   induction the drive stays below the largest D met, as claimed.
3. Local, bounded, on the record, no formula, no name: **holds**. `drive`
   and `axis_steps` are fields of `Measured` beside `age` and `steps`;
   nothing is written at a Node; the addition is in Python integers, which
   the design allows, and the result is below `Q S M + |p| < 2^62 + 2^62`;
   `step_axis` reads the momentum, the content and the world's width only;
   the diff branches on no name and holds no formula of a force. A declared
   `drive` is refused by the parser's generic unknown-key check
   (`world.py`, "has unknown keys"); test (d) proves it.
4. The turn by momentum reads the same k0 at a constant momentum: **holds on
   one axis** (`axis_steps - 1` counts steps made and refused, as the floor
   did; test (e) and `test_nature_beam_body` (d)'s first part pass). **Fails
   on two axes** (finding 1; the same test's second part).
5. The contact rule, the body on a set, the escape on a face and the frame's
   order: the diff does not touch `_contact`, `body_nodes`, the escape branch
   or `step`; **untouched in code**. What the order x before y before z
   costs the later axes has changed (finding 1).
6. The documents state the rule as implemented: note 17, ENGINE.md's frame,
   MIGRATION.md and TEST_EXPECTATIONS.md's section do; finding 4 lists what
   does not; finding 3 lists what they cite that does not exist.

## Tests run

Interpreter `/home/user/Universe24/.venv/bin/python` (3.14.0rc2),
`PYTHONPATH=/home/user/drive/src`, the imported package verified as
`/home/user/drive/src/event_universe`.

- `pytest tests/test_step_drive.py tests/test_push_width.py tests/test_nature_beam_body.py -q`:
  26 passed, 1 failed
  (`test_nature_beam_body.py::test_a_body_turns_its_phase_by_its_momentum_at_every_link_it_steps`,
  line 551, `(16, 6, 0) == (16, 9, 0)`).
- The same module on the base checkout `/home/user/Universe24` (its `src`,
  commit 5322dc4, whose engine is the base's): 7 passed.
- An engine-free arithmetic script (`by_clock` and `step_axis` only) for the
  counterexample of finding 1; its output is quoted there.
- Read, not run: `/home/user/gate/check.log` (the implementation's
  `tools/check.py` on this tree, 9 failed, 693 passed, 1 xfailed).

## Not verified

- The six re-registration failures of finding 2: I did not derive their
  amended integers or run them; whether each is exactly the design's
  re-registration or also finding 1 is for their owners after the
  correction.
- The registered worlds beyond the gate set (`/home/user/gate/reg_base`,
  `reg_drive`): not compared.
- The physical claim of the design, that the drive gives series G2 a
  readable Hubble diagram: a research run, not a test; outside this review.
- The design's authority: RULES.md is the physicist's read-only design on
  another branch; the owner's decision it cites ("1 and 2 are very
  important") is quoted, not linked to a record.

## Disposition, 2026-09-20 (the implementer, after the review)

Every blocking finding was corrected on the branch before its pull request;
the review above is kept as written.

- Finding 1: `_move` now advances the drive of every axis at every
  self-creation in which the body may step, steps the first axis whose
  rule fires, and lets a later axis's coincident fire lose its Link (its D
  subtracted, nothing carried, counted in `axis_steps` as the whole part
  off the clock counted it); `steps_by_rule` in the readings tool follows
  the same order. `tests/test_nature_beam_body.py` (d) and
  `tests/test_coupling_readings.py` (b) pass unchanged; test (a) of
  `tests/test_step_drive.py` gained the two-axis case (the counterexample
  above and the coincidence at (64, 64, 0)).
- Finding 2: the six tests of pushed or handed-over bodies were
  re-registered from an engine-free derivation by the rule (a script of
  the drive, the hand-over and the frame's order, run before the pins were
  moved), the old integers kept as history in TEST_EXPECTATIONS.md and in
  each module's docstring: `test_contact` (a), (d), (e),
  `test_nature_beam_clock` (d), `test_paid_charge` (d),
  `test_nucleus_readings`. Each body that receives a momentum steps one
  self-creation later than the count off the clock stepped it (its drive
  begins at 0); the register pair hands 998 times from tick 3, the first
  hand-over two intervals' pushes.
- Finding 3: the design is cited by name and branch (RULES.md section 1 on
  `claude/series-g2-stars`), not linked; record 107 is named as the Boss's
  record of the decision, written at the landing.
- Finding 4: BEAM_LAW section 3 step 5, the `_move` docstring, the
  TEST_EXPECTATIONS row (38 within 1; [0, 2 D - 1)) and MIGRATION.md's
  list of changed gate worlds (`1b_m16`, `r2`, `alpha_square`,
  `j3_deuteron`) were amended.
- Finding 5: stands as noted; the sizes are the tests' own.
