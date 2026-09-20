# Physics-rule review: the signed step drive (record 126)

Reviewer: the physics-rule reviewer (read-only). Date: 2026-09-20.
Reviewed: branch `claude/step-drive-signed` in the worktree `/home/user/signed`,
base `d2e4c15a` (main after PR #375). The review began on the uncommitted
change (the four docs, `core/integer.py`, `events/engine.py`,
`events/measured.py`, `tests/test_step_drive.py`) and, when the change was
committed during the review as `ead9298`, was completed against that commit,
which also carries `tests/test_contact.py`, `docs/EXPERIMENTS.md` and the
orbit, Bohr, nucleus and weak READMEs (the registered re-reads).

**Verdict: the signed drive is correct, generic, local and bounded, and the
byte-identity claim for one-sign momenta holds; blocked on one line of the
law text (finding 1, BEAM_LAW section 3 step 5 still states the unsigned form
as the active rule). Everything else is not blocking.**

## The rule under review

`core.integer.by_drive(drive, rate, denominator)`: `drive += rate`; returns
(+1, drive - D) when `drive >= D`, (-1, drive + D) when `drive <= -D`,
(0, drive) otherwise. `engine.step_axis(drive, momentum, content, width)`
calls it with the signed momentum p and D = Q S M + |p| and returns the fired
sign or None. `_move` is unchanged: every axis's drive advances, the first
fire steps, a later coincident fire is lost and counted in `axis_steps`.

## Findings

### 1. BEAM_LAW section 3 step 5 states the unsigned form as the active rule (blocking)

- Rule: one source of truth for the law; an unresolved contradiction in the
  contract blocks (AGENTS.md; the review skill).
- Evidence: `docs/BEAM_LAW.md` lines 521-524 (unchanged by the commit):
  "kept on the body's record as `drive` per axis (`drive += |p|` at every
  self-creation in which it may step, one Link and `drive -= Q x S x M +
  |p|` at or beyond it)". Note 17 of the same document, ENGINE.md,
  MIGRATION.md and the code say `drive += p`, signed, with `-D` on the
  other side. A reader of section 3 (the interval's steps, the primary
  text) gets the superseded rule with no mark that it is history.
- Correction: amend the clause to the signed form (`drive += p`, a step on
  the + side and `drive -= D` at `drive >= D`, on the - side and `drive += D`
  at `drive <= -D`, D = Q x S x M + |p|; record 126) or replace it by a
  pointer to note 17 as amended. One sentence; no run needed.

### 2. `tools/coupling_readings.py` docstring states the unsigned form (not blocking)

- Evidence: `steps_by_rule`, lines 151-157: "the drive gains |p| at every
  self-creation and the body steps when it reaches Q x S x m + |p|". The
  tool calls the engine's `step_axis`, so its numbers follow the signed rule;
  only the prose is stale. `tests/test_coupling_readings.py` passes.
- Correction: "the drive gains p, signed, and the body steps when it reaches
  +(Q x S x m + |p|) or -(Q x S x m + |p|)".

### 3. TEST_EXPECTATIONS carries two unsigned phrasings without a history mark (not blocking)

- Evidence: line 1145 (the contact (a) record) "the drive gaining |p| at
  every self-creation"; line 1452 (the step drive (b)) "the drive within
  [0, D) after every interval". The integers of both records are right:
  in (a) each body keeps one sign until the three-Link case, where lines
  1169-1170 already give the signed drives -7616 and +7616; in (b) the
  momentum is positive throughout, so [0, D) is the signed drive's range
  there (the test's own comment says "one sign: never negative").
- Correction: "gaining p (signed; every body here keeps one sign until the
  three-Link case)" and "within [0, D) (the momentum of one sign)".

### 4. Test (g) discriminates the two rules only at tick 2093; its history clause is unpinned (not blocking)

- Evidence (engine run, this review): the test's world under main's unsigned
  rule (the module's `step_axis` replaced by the unsigned form, everything
  else the commit's) holds for 2092 intervals exactly as under the signed
  rule and steps the neutron to (12, 10, 10) at tick 2093 (momentum +u,
  u = 310 967 280 640, the `step` line's drive 1 788 709 632 000; 225
  contacts, 117 + 109 fires by then). Under the signed rule 3000 intervals
  make no `step` (170 + 150 fires, 320 contacts, the books balanced). So the
  test does pin the change, but only because it runs 3000 intervals; the
  first 2092 are identical under both rules. The Boss's narrative of record
  126 (the neutron charged by fourteen intervals, handed +15u, stepping away
  with +u) is not this world's: here the pushes are exact mirrors (the sum
  of the x-momenta is 0 after every tick; |sum| reaches u only inside an
  interval), so a hand-over zeroes both momenta and the neutron's momentum
  is positive for at most one interval (its largest +u). The clause "under
  the first form the neutron stepped away after the contact handed it the
  proton's component" (TEST_EXPECTATIONS (g), the test docstring) is true
  at tick 2093, when the two drives have drifted apart (117 against 109
  fires) and the hand-over leaves the neutron +u.
- Is the hold the rule's consequence or a coincidence? The rule's, given the
  world's symmetry: over 3000 intervals the neutron's signed drive never
  exceeds 0 and the proton's never falls below 0 (measured); a +x step of
  the neutron needs +D_n = 31 610 959 298 560 + |p| (about 102 u) of
  positive drive, and its positive excursions are one interval of at most
  +u each, followed by tens of intervals of negative momentum. It is not a
  theorem for every pair: a body that receives a large outward component
  right after spending its own inward drive can step away under the signed
  rule too, and should (it was driven away). I tried a declared proton
  momentum of +u, +2u, +3u: under the unsigned rule the +u pair separates
  at tick 86, under the signed rule none of the three separates in 200
  intervals.
- Correction: pin tick 2093 (and the +u, the drive 1 788 709 632 000) in the
  (g) expectation and the docstring as the first form's step, and say the
  first 2092 intervals read the same under both; or keep 3000 and add the
  one-line reason above (the drive of each body never crosses 0). Not a
  code change.

### 5. The check gate did not run in the worktree (not blocking; a merge condition)

- Evidence: `python tools/check.py` in `/home/user/signed` selected the
  changed files and the affected suites (its `artifacts/check-scope.json`
  lists 30-odd test modules) and then failed before running anything:
  `RuntimeError: artifact path already has an active writer`
  (`event_universe/retention.py`, the artifacts lease held by another
  process on this worktree). I ran the relevant suites directly (below); all
  pass. The gate must be run where the lease is free before the merge
  (CONTRIBUTING.md); the language and hygiene gates and ruff are part of it.

### 6. Record 126 is cited but absent on this branch (not blocking; merge order)

- Evidence: BEAM_LAW note 17, ENGINE.md, MIGRATION.md, TEST_EXPECTATIONS.md
  and the READMEs cite "record 126 of 2026-09-20"; `docs/LOG_2026-09-20.md`
  on this branch ends at record 109. The record is on the Boss's branch.
- Correction: land the Boss's log record with or before this pull request,
  so the citations resolve on main.

### 7. The bound is tighter than the text says (not blocking; an observation)

- Under any sequence of rates with |rate_i| < D_i <= D_max, the drive obeys
  |drive| < D_max (induction: if |d| < D_max and the sum crosses +D, the
  remainder is in [0, D_max - D + ... ) < D_max; symmetric on the other
  side; otherwise |d + r| < D). Test (c)'s bound 2 x 768 - 1 is exactly
  D_max of its draw (768 + 767), so the test states the sharp bound; the
  docs' "a residual earned at a larger momentum fires at the following
  self-creations, one Link each" is right (checked: drive 1500 under D 1535,
  then rate 1 against D 200 fires once per call: 1301, 1102, 903, 704).
  No change needed.

## What was verified

1. The primitive (engine-free, `arith.py`): with a constant rate of either
   sign over 3000 self-creations for D in {3, 7, 128, 1345, 9216} and eight
   rates each, the count is `sign x by_clock(n - 1, |rate|, D)` and the
   drive is `sign x (n |rate| mod D)`; with a random signed rate in
   (-D, D) over 2000 trials x 500 calls the drive equals the signed sum of
   the rates since the last count, the count is in {-1, 0, +1} and |drive|
   < D; under varying denominators |drive| < D_max (500 x 400 calls); never
   two counts per call (by construction: one early return).
2. Byte-identity: `step_axis` against main's unsigned form over 3000 random
   one-sign histories (300 self-creations each, momenta including zeros, five
   contents, four widths): the fired signs are identical and the new drive is
   `sign x` the old drive at every self-creation. A momentum of 0 returns
   the drive untouched in both, so a momentum that passes through 0 and
   returns with the same sign keeps its drive. A momentum that changes sign
   is the only divergence, as claimed. The re-registered `test_contact` (a)
   and (e) integers follow the rule by hand: (a) p1's drive -7936 at tick 6,
   -7936 - 15872 = -23808 <= -16192 at tick 7, the drive -7616 (p2 +7616);
   (e) with b first, a's drive +64 - 128 = -64 at tick 2, -192 = -D at tick
   3 (the step to (1, 1, 1)), -128 at tick 4, one step (the unsigned form
   stepped at ticks 2 and 4).
3. Test (f) from the rule alone: 8 x 1024 = 8192 after eight; 8192 - 1024 k
   reaches -9216 at k = 17, the twenty-fifth self-creation, the count -1 and
   the drive 0; five more give -5120 after 30; the unsigned form fires -x at
   the ninth (8192 + 1024 = 9216). The engine test passes with those
   integers.
4. Test (g): finding 4.
5. Locality and the contract (docs/ARCHITECTURE.md): one integer per axis on
   the body's record, nothing at a Node; |drive| < D_max <= Q S M + |p|_max
   with the momentum already `bounded`; fixed work per axis; no branch on a
   physical name (`step_axis` reads content, width, momentum); no formula on
   a payload; the record's `drive` on `run.json`, `state.json` and the `step`
   line is the same integer, now signed (`measured.py` line 436 unchanged).
6. Docs: note 17, ENGINE.md, MIGRATION.md, TEST_EXPECTATIONS "The step
   drive" (a), (c), (f), (g) and the `by_drive`/`step_axis` docstrings agree
   with the code. The stale places are findings 1-3.
7. Language gate (`tests/test_repository_language.py`, 14 passed) and ruff
   (check and format) on the changed Python files: clean.

## Tests run

Interpreter `/home/user/Universe24/.venv/bin/python`, `PYTHONPATH=/home/user/signed/src`, cwd `/home/user/signed`.

- `ruff check` and `ruff format --check` on `src/event_universe/core/integer.py`,
  `src/event_universe/events/engine.py`, `src/event_universe/events/measured.py`,
  `tests/test_step_drive.py`: "All checks passed!", "4 files already formatted".
- `pytest -q tests/test_repository_language.py`: 14 passed.
- `pytest -q tests/test_step_drive.py`: 19 passed in 65 s.
- `pytest -q tests/test_contact.py tests/test_push_width.py tests/test_nucleus_readings.py tests/test_coupling_readings.py tests/test_orbit_readings.py tests/test_bohr_readings.py tests/test_nature_beam_clock.py tests/test_paid_charge.py tests/test_nature_beam_body.py tests/test_weak_readings.py tests/test_nature_beam_push.py`: 51 passed in 12 s.
- `python tools/check.py`: failed before running anything with
  `RuntimeError: artifact path already has an active writer` (finding 5).
- Scratch scripts (not in the repository): `arith.py` (items 1-3 above, all
  assertions pass); `deuteron.py`, `deuteron2.py`, `deuteron3.py` (the test
  (g) world under the signed rule for 400 and 3000 intervals and under the
  unsigned rule for 3000: first `step` at tick 2093 under the unsigned rule,
  none under the signed; the declared +u/+2u/+3u variants for 200 intervals).

## Not verified

- The registered re-reads committed during the review (`docs/EXPERIMENTS.md`,
  the orbit, Bohr, nucleus and weak READMEs: the orbit numbers T 701, 821,
  880, 878, the returns, the radii, "no orbit closes by the criterion", the
  Bohr, nucleus and weak lines): not re-run (4000-interval worlds and the
  readings tools, beyond this review's budget). Their tests pass, which
  checks the tools' arithmetic on the recorded events, not the numbers
  quoted in the prose.
- Whether the claim "every world whose momenta keep one sign on every axis
  steps as before" was checked against the whole example set (the gate
  set's compare); proven here for the rule and its record, not run over the
  33 worlds.
- The Boss's W1 world of record 126 itself (its narrative differs from the
  test's world; finding 4); the record is not on this branch.
- Whether Q x S x M is guarded against the integer bound at parse time (a
  pre-existing question, unchanged by this commit: D is the same integer as
  before).

## Disposition, 2026-09-20 (the implementer, after the review)

- Finding 1 (blocking): BEAM_LAW section 3 step 5 now states the signed
  form, the `|p|` form named as history.
- Findings 2 and 3: the readings tool's docstring and the two
  TEST_EXPECTATIONS phrasings amended (signed; one sign where the case is
  one).
- Finding 4: test (g)'s docstring and its TEST_EXPECTATIONS item carry
  the reviewer's measurement (the first form holds for 2092 intervals and
  steps the neutron at tick 2093) and the reason the hold is the rule's
  consequence for this pair and not a theorem; the pin stays on the run's
  3000 intervals with no `step` record.
- Finding 5: `tools/check.py` run where the lease was free: exit 0.
- Finding 6: record 126 is the Boss's, on the Boss's branch; the pull
  request names it and lands after it.
- Finding 7: noted; no change.

# Physics-rule review, second pass: rule (a) of the suspension (record 128)

Reviewer: the physics-rule reviewer (read-only). Date: 2026-09-20.
Reviewed: the commit of rule (a) (`2dfb91a` on `claude/step-drive-signed`,
the same change as `2451e89` on `claude/suspension-rule-a`, PR #383):
`nature_beam` step 4's rule matrix reading `pass` for every family of an
entry that waits this interval; the re-registered tests; the law text.

**Verdict: the rule as decided ("a measured event whose clock owes an
interval neither releases nor reads in it") is implemented faithfully,
generically and locally: one condition on the rule matrix, no family named,
the pass-through exact, nothing held at a Node, byte-identical under
`suspension` 0 by construction. The three re-registered expectations are
correct derivations (checked from the code and by trace). Not blocking on
the code. Two things are for the model owner before or at merge: the
record's own acceptance criterion ("the pair's momenta balanced to the
integer over 3000 intervals") is not met (the sum ends at -P), which the
commit reports honestly but calls a "coincidence" when for a mirror pair it
is the arithmetic of near-equal counts; and a pre-existing gap in the same
spirit: a body steps (and hands over) in the last interval of its wait.**

## Findings

### 1. "Coincidence" understates the third-law remainder (not blocking; wording)

- Rule: a physical hypothesis's expectation must be independent and stated
  as measured (AGENTS.md; the review skill).
- Evidence: trace of test (g)'s world: the proton's count 128 800 and the
  neutron's 128 590 against 2^27 give first waits at ages 1042 and 1043
  (2^27 / 128 800 = 1042.06, 2^27 / 128 590 = 1043.8), i.e. ticks 1044 and
  1045, adjacent by arithmetic; the sum reads -P at 1044 (the proton's read
  missing), 0 at 1045 (the neutron's read of rows the proton never
  released), -P from 1046 (the neutron's release missing at the proton),
  -2P at 2087 (the proton's second wait), -P from 2088 to 3000. For any
  bound pair of near-equal content the two clocks fire within a few
  intervals of each other, so the remainder is generic for pairs, not a
  coincidence; `j3_deuteron`'s 7-Link drift in the weak re-read is the same
  effect. The -P is the rule's consequence, not an implementation defect: a
  wait deletes one read (of the partner's rows released one flight earlier)
  and one release (read by the partner one flight later); when the
  partner's wait falls on the interval that missing release would have
  arrived, its own deletion of a read removes nothing, so only one of the
  two deletions is compensated. Momentum is conserved globally (the un-read
  rows leave through the face; books balanced at every tick).
- Correction: in BEAM_LAW note 17, TEST_EXPECTATIONS (g) and the test
  docstring replace "narrowed to that coincidence" by "narrowed to the case
  of adjacent waits, which for a pair of near-equal content is the ordinary
  case, so a bound pair gains one push net per pair of adjacent waits, in
  the sign of the body that waits first"; and state explicitly that record
  128's stated test ("balanced to the integer over 3000 intervals") is not
  met, for the owner's decision.

### 2. A body steps and hands over in the last interval of its wait (not blocking; for the owner; pre-existing)

- Rule: the owner's reason for rule (a), "to wait is not to communicate in
  either direction"; BEAM_LAW note 17 "at every self-creation in which it
  may step drive_a += p_a".
- Evidence: `engine.py` `_frame_all` decrements `owed` to 0 and sets
  `creating = False`; `_move` guards on `entry.owed > 0`, which is already
  0, so with `owed` 1 every waiting interval is a stepping interval: in the
  (g) run at tick 2087 the proton waits (creating False) and makes a
  `contact` (a hand-over to the neutron) in the same interval. Not
  introduced by this commit (the guard predates it) and the (g) integers
  include it (contacts == steps holds).
- Correction: an owner's decision whether `_move` should be guarded by
  `creating` (a physical change, its own record and re-reads); not this
  PR's.

### 3. The test's reason for -2P is wrong (not blocking; docs)

- Evidence: `tests/test_step_drive.py` (g) comment "-2 P within a
  hand-over's interval"; a hand-over never changes the pair's sum
  (`_contact` moves a component from one body to the other). The -2P at
  tick 2087 is the proton's second wait (its read missing for one
  interval; the neutron misses the proton's release at 2088 and the sum
  returns to -P).
- Correction: "-2P in the interval of the proton's second wait (tick
  2087), -P again at 2088"; pin 2087 in TEST_EXPECTATIONS (g) beside 1044.

### 4. The clock counts rows the body did not read (not blocking; for the owner)

- Evidence: `nature_beam.py` adds every row of another number at the Node
  (arrived or resting) to `presence`; `met` excludes non-arrived rows and
  PASS entries, so passed rows that rest at the Node by their flight
  rhythm (a heading ray moves at age 0 -> 1, rests 1 -> 2: trace of the
  k = 8 probe, rows (node 1, age 1) and (node 1, age 2) both present at
  tick 5) are counted once, never read. This is a reading of state only
  (no consumption, no register: the rows are the store's, unchanged) and
  matches what a `pass` body always counted. Its physical reading is a
  feedback: a waiting body counts more and waits more (the k = 8 probe
  owes 4 instead of 2; Hubble `pushing_scalar`'s detector reads 0.21
  self-creations per interval instead of 0.29 and sees one interval in
  five). Record 128 decides only "neither releases nor reads"; the count is
  the implementer's reading, registered.
- Correction: none in code; the owner should confirm that the owed count is
  of the presence including unread rows, and that a detector under a
  suspension exposes at its own clock's rate.

### 5. Two step-4 phrasings without the rule (not blocking; docs)

- Evidence: `nature_beam.py` module docstring ("a measured event meets the
  rays that arrived this interval at its Node") and `engine.py`
  `_frame_all` docstring ("no self-creation, no release, no turn"; add "no
  read"). ENGINE.md does not restate step 4 and needs no change; the law
  text (BEAM_LAW step 4 and note 17), MIGRATION and TEST_EXPECTATIONS agree
  with the code; no contradiction of the kind of the first review's
  finding 1.

### 6. Home rows are still taken while waiting (not blocking; observation)

- Evidence: `home = own & arrived` has no rule, so a waiting body's own
  returning rays join `pending` and are re-created at its next
  self-creation. Consistent with the rule's letter ("reads" are of other
  numbers) and with note 4 (home keeps phase and content); no world in the
  change exercises it.
- Correction: one clause in note 17.

## Verified

- Locality and books (item 1): PASS rows are neither in `met` nor `taken`,
  `keep` stays True, no ledger line moves; the row's flight is untouched
  (the walk in step 1 precedes the tables and reads nothing of the
  entries), so the bijection holds and nothing is kept at the Node; the (g)
  run's books balanced at every 250th tick and at 3000, the probe world's
  at every tick.
- Byte-identity under `suspension` 0 (item 2): `_suspend` returns before
  writing when `suspension[0]` is 0; `owed` defaults to 0 and is not a
  parseable key; `_frame_all` then sets `creating = True` for every entry
  at every interval, so `ev_rule` equals the declared matrix; `nature_beam`
  is called only after the frame (`step`) or without measured events
  (`inverse_step`). Exact from the code; `test_nature_beam_worlds.py`
  passes unchanged.
- The re-registered tests (item 3) are derivations, not descriptions: clock
  (e) k = 8: counted 8 at tick 2 -> owed by_clock(1, 8, 4) = 2; waits at 3,
  4; at tick 5 the arrival of 8 plus the 8 passed at tick 4 resting by the
  heading's rhythm = 16 -> owed by_clock(2, 16, 4) = 4; ages 1, 2, 2, 2, 3,
  3, 3, 3, 3, 4, waited 6, owed 4 (trace matches tick by tick); k = 1:
  presence 2 at tick 6, by_clock(4, 2, 4) = 0, ages unchanged. Age (c):
  self-creations at ticks 1-6, 8, 12, 16, 19, 23; the arrival first reaches
  the reader at tick 6, so reads at 6, 8, 12, 16, 19, 23 = six (nineteen
  were the ticks 6-24), ages and counts unchanged because `read` consumes
  nothing. Step drive (g): waited (2, 1); sums 0 to tick 1043, -P at 1044,
  0 at 1045, -P from 1046, -2P at 2087 only, -P at the end; no `step`,
  contacts == steps (the trace above).
- Item 4: the right reading, with the qualification of finding 1; not an
  implementation defect.
- Item 5: no contradiction between law text and code found.

## Tests run

Interpreter `/home/user/Universe24/.venv/bin/python`, `PYTHONPATH` the
branch's `src`: `test_nature_beam_clock`, `test_nature_beam_age`,
`test_step_drive`, `test_nature_beam_worlds`, `test_contact`,
`test_hubble_readings`, `test_weak_readings`, `test_coupling_readings`: 55
passed in 74 s; `test_repository_language` 14 passed; ruff check and format
clean on `nature_beam.py` and the three test files. Scratch traces (not in
the repository): the (g) world for 3000 intervals with creating, owed,
counted, waited, the momentum sum and the read/contact records per tick;
the k = 1 and k = 8 probe worlds for 10 intervals with the store's rows
(node, age, arrival) per tick.

Not verified: the re-read numbers in EXPERIMENTS.md and the READMEs (the
Hubble clock rates and mx1 counts, j3_deuteron's 7 steps and fire at 572,
coupling item 6's 131 072) were not re-run; `tools/check.py` was not run
for this commit by the reviewer (the log records 737 passed for the
branch); record 128 is cited from the LOG on this branch.

## Disposition, 2026-09-20 (the implementer, after the second review)

- Finding 1: BEAM_LAW note 17, TEST_EXPECTATIONS (g) and the test's
  comment now say "adjacent waits, the ordinary case for a pair of
  near-equal content, one push net per pair of adjacent waits in the sign
  of the body that waits first", and state that record 128's criterion
  ("balanced to the integer over 3000 intervals") is not met on this pair,
  for the owner. The pull request's body says the same.
- Finding 2: not this PR's; carried to the owner in the report (a step in
  the last interval of a wait: whether `_move` should be guarded by
  `creating`).
- Finding 3: the comment corrected (the -2P is the proton's second wait at
  tick 2087, -P again at 2088); tick 2087 pinned in the test (the one
  interval reading -2P) and in TEST_EXPECTATIONS (g).
- Finding 4: no code change; the reading (the owed count of the presence
  including unread rows; a detector under a suspension exposing at its
  clock's rate) is stated in note 17 and carried to the owner for
  confirmation.
- Finding 5: both docstrings amended (the module's step 4; `_frame_all`'s
  "no read").
- Finding 6: one clause in note 17 (home rows taken while waiting).
- `python tools/check.py` on the branch after these edits: see the pull
  request.
