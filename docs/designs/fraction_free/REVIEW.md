Read at ddec5166 (the branch `fraction-free` over 241fc7ac, before the merge of main 99a928e1);
read-only, 2026-09-20. The verdict: MERGEABLE AFTER five should-fix (documentation and one load
guard; no integer of the law changes), applied in the commit that carries this copy: the tight
alignment bound K + T - 1 (note 41 (vii), the Bell README), the load refusal of Lambda_c^2
(`world.column_scales`, test (g)), the two TERMINOLOGY clauses, the phase-of-the-count clause, the merge of main and the citation of record 150.

# The physics-rule review of the branch `fraction-free` at ddec5166 (read-only, 2026-09-20)

**Scope.** The worktree `/home/user/Universe24/.claude/worktrees/fraction_free`
at ddec5166 over 241fc7ac, 4b304890, 387b4120 (the merge of main e62291a8),
6cdd1dfb, e7ba13c6, a2120413; `git diff origin/main --stat`: 52 files,
+3011/-504, no world `.json` changed (the README files only under
`examples/`). What I did: read AGENTS.md, the skill, TERMINOLOGY,
ARCHITECTURE (the contract), FORM.md, REVIEW_COUNTS.md, records 133, 147,
148 (on the branch) and 150 (on main 0e7c6b43; the branch lacks 150-153),
note 41, note 17, MIGRATION, TEST_EXPECTATIONS, VALIDATION, EXPERIMENTS'
dated lines, the READMEs, the implementer's REGISTER_TABLE, GATE_TABLE,
IDENTICAL, SKIPPED and the run tree; read every src diff; ran
`tests/test_fraction_free.py` and `tests/test_integer_arithmetic.py` (42
passed, 23 s) and a `by_drive` script of my own (the lamp's alignment
threshold, the sign, the cap, the period sum). No repository file edited,
nothing committed. About 45 minutes. Every line number is against the
worktree.

## 1. The primitive and every count

- `src/event_universe/core/integer.py:77-113` (`by_drive`): `drive += rate`;
  `count = |drive| // d`, capped at `at_most` when positive, signed with the
  accumulator; the remainder `drive - count x d` kept. An unsigned rate keeps
  the accumulator in [0, d); a signed one in (-d, d) (truncation toward zero,
  symmetric: my check `by_drive(5, -9, 3) = (-1, -1)`, `by_drive(-2, -5, 3) =
  (-2, -1)`). The cap: `by_drive(0, 7, 3, at_most=1) = (1, 4)`, the
  accumulator above d until the residual fires one per following
  self-creation, the step's declared rule (note 17 as amended) and the only
  capped row (`measured.py:343`). The period sum: on 5000 signed random rates
  the counts summed to the whole part of the summed rates exactly (1514 =
  1514, the remainder 849 below 1000). The whole part of the running sum,
  the accumulator below its denominator, the cap and the sign are as note
  41 (i) states.
- The counts, each with its rate and denominator, and the stage at which it
  is advanced: the turn, `content x n` over d = K, at the frame
  (`engine.py:488`, the product bounded at `:483`); the owed count,
  `counted x n` over d of `suspension`, at `_suspend` (`engine.py:507`,
  `count_owed` `:131`); the release per family, `held x n` over d, a paid
  family's rate 0, at step 5 (`nature_beam.py:3609`, consumed at `:3627`);
  the lamp's rate, n over d, at step 5 (`:3606`, consumed at `:3864`); the
  drive, p over Q S M + |p| handed per call, the cap 1, idle at p = 0, at
  `_move` (`engine.py:580-583`); the push, X over Lambda_c^2, at the reading
  (`nature_beam.py:2268`); the flow weight, V_d,a x num_d over G Q |v_d|^2
  handed per call, at the reading (`:2174`). No count re-evaluates its age:
  the age enters no rate.
- Every remaining `by_clock` caller (grep of the branch) and its rate:
  (1) `engine.py:668`, the turn by momentum under `action`:
  `by_clock(k0, |p_a| N, h)`, the rate `|p_a| N`, NOT constant on a pushed
  body (section 2). (2) `nature_beam.py:486` `by_clock_rows`, called at
  `:2435` (the inverse walk) and `:2551` (the walk): a row's phase per
  interval of age at the family's `phase_per_age`, a constant of the row's
  family over its flight, the identity's case. (3) `world.py:1019-1030`
  `NatureBeamWorld.turn`: the constant-rate identity, called by the readings
  tools only (`tools/lensing_readings.py:281`, `buildup_readings.py:136`,
  `heisenberg_readings.py:170`, all at age 0), never by the engine.
  (4) `nature_beam.py:519-531` `ages_at_key`: the comparison
  `age % key == 0`, no rate; correct, since `by_clock(age - 1, 1, key) = 1`
  exactly when the key divides the age. (5) The tools `coupling_readings.py:86`,
  `orbit_readings.py:72` (a sum over one period), `lensing_readings.py:264`,
  `buildup_readings.py:137`: derived constant-rate readings at age 0. So
  `by_clock` is out of the law's counts except the one of section 2.

## 2. The one count left on `by_clock`: the turn under `action`

- `engine.py:663-669`: at a step on the axis a, `k0 = axis_steps[a] - 1` and
  `turn = by_clock(k0, |p_a| N, h)`. The rate `|p_a| N` is the body's
  momentum component on that axis, which the push changes at every read; in
  the seven `bohr/r*.json` worlds (the only `action` worlds on the register,
  `phase_by_momentum` on the electron) p rotates on the orbit, so |p_x| and
  |p_y| change at every interval. The turn at a Link is therefore
  `floor((k0 + 1) |p_a| N / h) - floor(k0 |p_a| N / h)` with TODAY's |p_a|
  priced over every earlier Link on that axis: the a-historical form of
  record 148, the same defect the owner retired for the step (record 108)
  and for the lamp and the crowd (record 148). Its rate is not constant along
  a pushed body's motion, so it is not lawfully different: the phase along a
  path is the action integral, the sum over the Links stepped of |p_a| N / h
  (TERMINOLOGY's own closure sentence, `docs/TERMINOLOGY.md:76`: "the turn
  per orbit is (N / h) x the sum over the Links stepped of |p_axis|"), and
  the whole part of that sum is the accumulator's count and not
  `by_clock`'s. Under the owner's "one rule" (record 150) it must join the
  table: a row (or three, one per axis) of source `momentum`, advanced at the
  step where its numerator exists (not at the frame), the denominator h. One
  row for the whole action integral (the additions commute, FORM.md section
  3) makes the per-orbit closure the exact whole part of the summed |p_a|
  with the remainder carried across orbits; three rows keep the "axes
  compose" spelling at the cost of up to two lost units per orbit. It is the
  model owner's decision under the identity `bohr-v1` (note 30, a hypothesis
  beside the law), and note 41 (i) rightly names it as left as built and not
  decided in the note.
- The integer consequence for series H if it joins: the seven bohr worlds,
  identical today (no lamp, `suspension` 0, whole charges), move in their
  PHASES only: the `step` lines' `phase`, the phases the electron's released
  rays carry, and the `wave` detectors' coherence readings behind the atom
  (the "phase turn per orbit" column of the H table, EXPERIMENTS "H, Bohr's
  lines"), by at most one phase step per Link where |p_a| changed between
  Links, exact over an orbit. The orbits' r, T, return and closing do not
  move: the turn by momentum feeds neither the step (the drive) nor the
  push, and the electron's rows are of no record, so the merge cancels
  nothing (`nature_beam.py:1174-1179`). A re-registration of seven small
  worlds with a dated line each.

## 3. The counts table

- `measured.py:205-232` (`Count`), `:233-315` (`CountTable`, the one loop
  `advance` at `:255-292`), `:317-352` (`counts_table`), on the body's
  record at `:460`. Local: the table is a field of `Measured` as its age is;
  nothing at a Node; every row gains only what the body's own record holds
  or what arrived at its Node this interval. Bounded for fixed K: one
  integer per (body, count, index, axis): turn 1, owed 1, release one per
  family, lamp 1, drive 3, push 3 per column, flow 3 per direction of the
  world's table under `doppler` (`:350`: on a fan table of a few hundred
  directions this is hundreds of integers per body, a world constant;
  FORM.md section 4 had 3, note 41 (iv) says why the denominators forbid
  one; the key leaves under records 151 and 153 in any case). The unsigned
  rows stay in [0, d), the signed ones (drive, push, flow) in (-d, d), the
  drive above D transiently under the cap when D shrinks (declared, note
  17); test (e) and my run of it.
- The order of the law unchanged: the turn at the frame before
  `nature_beam` (`engine.py:488`), the push and the flow inside the reading
  (`nature_beam.py:2174`, `:2268`), the lamp and the release at step 5
  (`:3606-3609`), the owed count at `_suspend` after the reading
  (`engine.py:507`), the drive at `_move` (`:580`). Record 150's "a consumer
  that needs its whole part before the others keeps its delivery in place
  and is reported" did not arise: every row is advanced where its consumer
  reads it. One change of evaluation, not of order: the lamp row advances at
  every self-creation of the lamp (`:3606`) where `by_clock` was read only
  inside the release condition; the same semantics (the old count was a
  function of the age, unread at a self-creation that could not birth), the
  discard declared in note 41 (iii).
- The state keys: `acc` at `measured.py:704` beside `drive` (new on this
  branch since stage 1); the table changed no key: the seventeen gate
  digests of GATE_TABLE.md are those of stage (D). No runner resume path
  exists (TEST_EXPECTATIONS (c) says so; test (c) resumes at test level), and
  `state.json` carries the phase of every count as FORM.md 1 (i) requires; a
  declared `acc` is refused as an unknown key. `Measured.drive`, `acc_push`,
  `acc_flow` return copies (`measured.py:637-655`); no writer in `src`
  indexes into them (grep), the setters go through `CountTable.set`.

## 4. The push and the flow accumulators

- `nature_beam.py:2180-2271` (`push_form`): per column, X = V x E_c n_c x
  (Lambda_c / D_c) x (Lambda_c / d_c) over Lambda_c^2 on one accumulator per
  (column, axis), taking the group's whole flow V (already summed over the
  directions by the reading), so for the push the split over the directions
  equals the whole (FORM.md section 3). Lambda_c = lcm over the families
  (`world.py:1044-1061`); the reader's reduced charge denominator D_c and
  every arriving d_c divide it. Lambda = 1 on gravity and on whole charges,
  where the count is X itself with the remainder 0: every registered pushed
  world with whole charges is identical (IDENTICAL.md: bohr, orbit, coupling
  1a/1b and 2-6, lensing, nucleus, catalog; the fractional series 7 pair
  identical too, fixed probes on a constant flow, the identity). No
  registered push moved on gravity and whole charges.
- The bound of the lifted product: tested by division before it is formed
  (`:2251-2264`), refused by `column_bound_error` naming the body, its Node
  and the column. LOUD, but AT RUN (the first read whose factor is not 0),
  not at load: `column_scales` forms Lambda_c and `counts_table` forms
  Lambda_c^2 (`measured.py:345`) with no register check, so a world with
  coprime 30-bit denominators loads, carries Lambda^2 of about 2^120 as a
  row's denominator, and is refused only when a push forms; a world whose
  fractional-charge families never meet is never refused.
  `tests/test_columns.py:272-279` pins the run refusal. SHOULD-FIX: a
  parse-time refusal where Lambda_c^2 leaves the register (at
  `column_scales` or the world's load checks), the contract's "check
  intermediates before ... assignment" (`docs/ARCHITECTURE.md:73-75`). No
  registered world reaches it (every Lambda is 1 or a few tens).
- `nature_beam.py:2104-2178` (`weighted_flow`): one accumulator per
  (direction, axis) at G Q |v_d|^2, the numerator `v x num_d` signed (the
  drive's rule, a reversal cancels first). The directions' denominators have
  no common multiple in the register, so the split over the directions
  remains a sum of per-direction whole parts, each exact over a period; the
  per-interval loss of up to (directions - 1) units that FORM.md section 3
  promised to remove is removed for the push, not for the doppler weight, and
  note 41 (iv) says so honestly. At rest the numerator equals the
  denominator, the count is V_d exactly and the accumulator is untouched:
  bit-identical to the unweighted push (test_doppler (f)). Exact over a
  period: test_doppler (b), 396672 = the whole part of the summed fluxes
  (396673 off the clock).

## 5. The readers by record

- The pass line now carries `record` and `u` (`nature_beam.py:3235-3241`,
  from the store's record and birth of the passing row), the click line
  already did. `tools/bell_chsh.py:173-183` and `tools/bell_choosers.py:241-261`
  pair Alice's and Bob's lines by `record - base - 1`, the birth ordinal,
  and report the tick offsets without using them. The record's identity
  (the lamp's number x 2^32 + the ordinal) is stamped on the row at its
  birth on the GameBoard and carried through the flight: the law's own
  field, not a tool's memory; the reader only reads it off the line. The
  phase rule is checked as `phase == age mod N == u` (`bell_chsh.py:206`).
- S = 176/64: `tests/test_amplitude_pair.py` (the cells 27, 5, 5, 27 and
  5, 27, 27, 5) passes under `--full` (960 passed, `ff_full.log`), the
  reviewer's `pair_by_ordinal.py` gave the same on both trees (record 148),
  the choosers' fifteen E and S = 156/64, the MZ ports and the GHZ triples
  unchanged (EXPERIMENTS' L line). Unchanged, as the law says: a click is a
  function of the record's u and the settings.
- The K + 2 (T - 1) statement: SUFFICIENT, NOT TIGHT. The frame reads the
  content before the birth pays, so the k-th self-creation adds
  M0 - c (k - 1) to the turn's accumulator; after j self-creations it holds
  j M0 - c j (j - 1) / 2 - (births) K, and one birth per self-creation over
  T intervals needs M0 >= K + c (T - 1) / 2, that is K + T - 1 at c = 2. My
  `by_drive` replay: K + 2 gives 159 births with the stall at tick 4 (as
  registered); K + 159 gives 160 of 160; K + 318 gives 160. So "K + 318
  here" in `examples/events/bell/README.md:32` is twice the least content,
  and note 41 (vii) (`docs/BEAM_LAW.md:3273-3275`) "K + c (T - 1) or more
  keeps one birth per interval over T intervals" is true as a bound but is
  presented as the rule the exact clock needs; the reviewer's own check in
  REVIEW_COUNTS section 2 (b) (K + 160 gives the first stall at tick 162)
  agrees with the tight bound. SHOULD-FIX (a sentence in note 41 (vii) and
  the Bell README): the least content is K + c (T - 1) / 2 rounded up,
  K + T - 1 on these lamps (K + 159 for 160 births); K + c (T - 1) suffices.

## 6. The re-registration

Sampled from REGISTER_TABLE.md (all "events, books"). No world file changed
(`git diff origin/main --stat` lists no `.json` under `examples/`): nothing
tuned. The old integers are kept as history in the dated lines of
EXPERIMENTS (A2, G, G2, J, L, N: "the numbers above are kept as history")
and in the READMEs (bell, amplitude, weak, hubble, hubble_stars, binding,
masses).

- `weak/j3_deuteron`: the waits 1110 -> 1149 over the 764 bodies (the two
  nucleons 80 -> 69 each, the shell's counters up; ages by -2 to 11), the
  steps 62 -> 64 (every attempt a refused contact), the neutron 577 -> 568,
  the beta 590 -> 581 with the same content at the same Node: the owed count
  at a crowd that changes every interval (the fan's rows dwell 1 or 2
  intervals), the reviewer's 200-interval replay having shown the
  accumulator equal to the whole part of the summed k n / d exactly.
  BOUND stands; the readings 34 inside and 2 outside as before.
- `amplitude/bell_0_8`: births 80 -> 79 (the pair lamp of 15 x 2^20 pays
  and stalls once, at tick 3), clicks 286 -> 282: the turn at a falling
  content, at most one unit; the cells and S unchanged by ordinal.
- `hubble_stars/record/gravity_scalar`: births 9512 -> 9504 (each star's
  lamp stalls once; 9600 -> 9576 in the `none` worlds), waits 107 -> 90,
  steps 1311 -> 1312, 22 of 25 ages by -1 to 4: the turn of paid lamps and
  the owed count of the scalar clock on a changing crowd; q +0.749 ->
  +0.380 and H 0.854 -> 0.896 (the clocked worlds' q is the reading most
  sensitive to the waits; the three clock-free worlds to the digit).
- `binding/proton_bond_lamp`: 3000 births as before (the content 2^23
  stays above K), 35 gathers of content 7 for 32 (the turn 7 at three more
  self-creations, the whole part of a falling rate, at most one per
  self-creation), no contact, no bond: the verdict stands.
- `hubble/pushing_scalar`: waits 639 -> 617, steps 1408 -> 1411, 24 of 31
  ages by -4 to 8: the owed count on a varying crowd (the push itself at
  Lambda = 1 unchanged, the coasting worlds identical); q = -0.55 the
  nearest in 9 of 12 windows (8 under the drive, 10 registered).

Identical (IDENTICAL.md; the gate digests "state.json alone", for the new
`acc` key): `bohr/r8` (a pushed body, whole charges, no lamp, `suspension`
0), `coupling/1b_m16` (a probe on a constant flow, Lambda = 1),
`lensing/heavy_meeting`, `weak/j2_ladder`, `redshift/age`: each a
constant-rate count, the identity where FORM.md section 1 said it holds.
Skipped, seven, named with reasons (VALIDATION, MIGRATION, SKIPPED.md):
`heisenberg/w27_beam` (as ordered); `heisenberg/w27_wave`,
`buildup/w27_rate1`, `w27_rate47`, `w27_rate8` (beyond the 1200 s wall on
the base, not run on the head); `heisenberg/w9_beam`, `w9_wave` (beyond the
4096 MB guard on both trees). Those five lamp worlds will move when run (a
paid lamp); their dated lines are absent and said to be.

## 7. The documents

- Note 41 (`docs/BEAM_LAW.md:3158-3287`): English, consistent with the code
  as built (the primitive, the table and its loop, the discard (iii), the
  lift and the per-direction flow (iv), the cell as a comparison (v), `acc`
  (vi), the alignment (vii)). Note 17 (`:1121-1131`): the exemption quoted
  and retired with its reason; consistent. TERMINOLOGY "Accumulator (of a
  count)" (`docs/TERMINOLOGY.md:77`): consistent. ARCHITECTURE (`:83-88`):
  the remainder owner named; consistent. ENGINE (`docs/ENGINE.md:185-196,
  206-208`): consistent. MIGRATION: complete, the seven not compared named.
  All English.
- Two TERMINOLOGY entries still describe the retired forms: "Turn by
  momentum" (`:76`, "derived from the age as the owed count is read off the
  clock: no register, no remainder": the owed count is no longer read off
  the clock) and "Width (of the push)" (`:78`, "`by_clock(age, |p|, S x M +
  |p|)`, no remainder kept": contradicts note 17 as amended and note 41).
  SHOULD-FIX, two clauses.
- The "phase of the count" reading of the accumulator (record 150 (3): the
  residue below the denominator is the phase within the cycle; record 151:
  "how much is left until the next click") is NOT stated in note 41,
  TERMINOLOGY or ENGINE; it appears in FORM.md:53 ("the phase of every count
  at that age") and in test (c)'s docstring only. SHOULD-FIX, one clause in
  note 41 (i) or the TERMINOLOGY entry: the accumulator is the phase of the
  count within its cycle, which is why `state.json` must carry it.
- The branch lacks records 150-153 (main 0e7c6b43); the merge of main
  before the pull request brings them (the log appends only), and note 41
  and `measured.py:206` ("the model owner's table of 2026-09-20") can then
  cite record 150.
- `engine.py:121` (`step_axis`, "the one place the step rule lives") is no
  longer literally true: `_move` advances the table's drive rows
  (`engine.py:580-583`) and `step_axis` is a second composition of the same
  `by_drive(at_most=1)` with `step_divisor`, kept for the readings tools and
  tests. The same integers (test_step_drive); a wording and duplication nit
  for the architect, not a physics defect.

## 8. LOCALITY-1, the integer contract, reversibility

- LOCALITY-1: every accumulator is on the body's own record and gains only
  the body's own content, its counted crowd at its Node, its held content,
  its rate, its momentum, or the flow of the rows that arrived at its Node
  this interval; Lambda_c is a parse-time constant of the declared families,
  not a read of remote state; nothing at a Node; fixed work and storage for
  fixed K (one addition and one comparison per row per interval). No
  violation found.
- The integer contract: every product tested by division before it is
  formed (`engine.py:483`, `nature_beam.py:2251-2264`, the flux at `:2170`);
  the remainder owned and declared (ARCHITECTURE `:83-88`); no float. The
  one gap is Lambda_c^2 formed unchecked at load (section 4).
- Reversibility: `by_drive` is invertible given the count and the rate
  (`acc_before = acc_after + count x d - rate`; the cap changes nothing);
  the engine's inverse pass (`engine.py:427`) runs on a GameBoard without
  measured events and inverts no body count, so nothing new is irreversible.
  The one count not recoverable from the record is the lamp's count at a
  self-creation of turn 0 or outside the window (note 41 (iii)), discarded
  as the unread `by_clock` count was; declared, and the only place a count
  leaves the accumulator without a birth.

## Verdict

**MERGEABLE AFTER** the following SHOULD-FIX (documentation and one load
guard; no integer of the law changes; none is blocking):

1. Note 41 (vii) and `examples/events/bell/README.md:32`: the least content
   for one birth per interval over T intervals is K + c (T - 1) / 2 rounded
   up (K + T - 1 at c = 2, K + 159 on the Bell lamps); K + c (T - 1)
   suffices and is not the rule.
2. A parse-time refusal where Lambda_c^2 leaves the register
   (`world.column_scales` or the world's load checks), so the coprime
   30-bit case is refused at load and not at the first push; test_columns
   (a) keeps the run refusal beside it.
3. TERMINOLOGY `:76` and `:78`: the retired "no remainder kept" clauses of
   "Turn by momentum" and "Width (of the push)" replaced by the drive
   (width) and "left as built, note 41 (i)" (the turn by momentum).
4. One clause stating the accumulator as the phase of the count within its
   cycle (note 41 (i) or the TERMINOLOGY entry), the owner's reading of
   record 150.
5. Merge main (records 150-153) before the pull request and cite record 150
   for the table. (Optional: the `step_axis` docstring.)

**The recommendation on the `action` turn for the owner:** the turn by
momentum (`engine.py:668`, `by_clock(k0, |p_a| N, h)`) is the one count
whose rate the push changes and that still re-prices its history, so under
"one rule" it should join the table as a row advanced at the step with the
rate |p_a| N over h (one row for the action integral, or three per axis to
keep the composition), which moves only the phase readings of series H (the
step lines' phase, the electron's rays, the wave detectors' clicks) and none
of its orbits: the model owner's decision under `bohr-v1`, as a separate
keyed change with the seven bohr worlds re-registered.
