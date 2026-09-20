# The architecture cleanup, phase 2: after the one click

The architect, 2026-09-20 (the Boss's assignment after PR #382; the model
owner's standing order, record 137: advance generic things that work and
simplify). Read-only: nothing here is a change. It continues
[the phase 1 plan](PLAN.md) (its sections 2, 3 and 5) against the one
click's branch, `claude/amplitude-impl` at 02448fa6 (stage (vii) step 4 of
`amplitude-v1`: the world key `amplitude` deleted, every lamp births
records, the push by share, the birth phase `u` as the record's own field;
its gate review passed, its merge into `main` in progress). Every line
number below is of that branch. Phase 2 is one pull request opened from
`main` after the branch lands, bit-exact on the gate set; the baseline of
its replays is taken on that `main` (section 5), never on an earlier one.

## 1. What the one click changed, read from its diff

Against `main` at d768f831 (86 files, +1,706 -672): the parser drops the
key and its twelve "needs the world key" refusals (`world.py` -174 +...:
`_families`, `_lamp`, `_split`, `_label_turn`, `_rotation`, `_gate`,
`_measured`, `_detectors` without the `amplitude` argument;
`NatureBeamWorld.amplitude` replaced by the property `recorded`, "a lamp is
declared"; `_amplitude_load_checks` run on every world; a world declaring
the key refused by name at `world.py:2509`); the engine builds the layer
for every world (`engine.py:207-233`); the store gains the column `birth`
(`nature_beam.py:724`, `FIELDS`) and every rule of the GameBoard reads the
path phase, `phase - birth` (the meeting, the windows, the faces, the
border, the click's pointer); the lamp births `by_clock(age, n, d)` records
per self-creation (`nature_beam.py:3452-3527`, the crowd form's count as the
count of records); the push of a record's row is its share
(`share_of`, `nature_beam.py:811`; the books' `remainder` line,
`measured.py:514-522`); the layer admits two multiplicities of one record
whose ratio is a square (`amplitude.py:154-181`, `isqrt`,
`common_denominator`); `run.json` loses the key `amplitude` and writes
`world`, `open` and `layer` in a recorded world alone (`run.py:182`). The
pointer gate of `wave` (issue #359 step A: the threshold on the pointer's
square) is deleted at `admit` (`nature_beam.py:2520-2526`); the `wave`
reading itself stays, the crowd's pointer giving the set's phase and its
per-interval record (`nature_beam.py:3192-3230`).

What this decides of phase 1's open questions: Q1 (the 1,525 `wave`
declarations) is answered by keeping `wave` as a reading of the crowd's
record without a gate: no world is rewritten; Q2 (`beam`) stays: the
pairing reading is kept (D3 of phase 1 is not dead); Q3 (the set's phase
returned to its measured events) is kept (`nature_beam.py:3210-3214`); Q4
is the branch's own; Q5 and Q6 stand.

## 2. What the one click leaves dead or duplicated (the D2-findings)

Each with its sites on the branch and the reason it cannot move an integer.

- **D2-1. `Layer | None`.** The engine always builds the layer
  (`engine.py:207`, `self.layer: Layer | None = None` and the unconditional
  assignment at 226), so the type and every guard on it are dead:
  `rotate_rows` (`nature_beam.py:1826`, `layer: Layer | None`; its guards
  at 1870 and 1872), `nature_beam` (`2019`, `layer: Layer | None = None`;
  the guards at 2225, 3003, 3067, 3124, 3229, 3287, 3380, 3488, 3689, 3749,
  3783: eleven), `run.py:182` (`simulation.layer is not None and
  world.recorded`, the first conjunct always true). The layer is present
  in every world; on a world without a lamp it holds no record and its
  calls (`birth`, `split`, `cancel`, `gather_records`) never fire, so the
  guards' removal changes no call. Seventeen sites, about 30 lines; the
  signatures become `layer: Layer`. Check before the commit: no test
  calls `nature_beam(...)` or `rotate_rows(...)` with `layer=None` (a grep
  of `tests/` on the branch finds none today).
- **D2-2. The pointer gate's callers.** `POINTER_UNIT` and `pointer_units`
  (`nature_beam.py:928-944`) have no caller left in `src` (the one site,
  `admit`'s `below_wave`, is deleted); their test is
  `tests/test_nature_beam_detector.py` (e), lines 170-174 (the import) and
  780-783 (the unit, the a^2 reading, the opposite pair). Delete the two
  definitions and the test's lines; the docstring of the test module (16,
  129) names them. The tables' bound they exercised is the layer's
  (`tests/test_amplitude_layer.py` reads the pointer through `Layer.end`).
  20 lines of `src`, 15 of tests.
- **D2-3. The lamp scan at parse.** `parse_nature_beam_world` refuses `N`
  below 4 with a lamp by scanning the raw document for a `lamp` key before
  `_measured` runs (`world.py:2627-2639`, `any(isinstance(entry, dict) and
  "lamp" in entry ...)`), the knowledge `_measured` and `recorded` hold
  (`world.py:877-886`, `any(entry.lamp is not None ...)`). One place: after
  `_measured`, `if phase_steps < AMPLITUDE_LEAST_STEPS and world.recorded`,
  the same message. Bit-exact: the same worlds refused, the refusal a
  `ValueError` either way (a document whose `measured` is not a list is
  refused by `_measured` first, as today it is refused by the scan's
  `isinstance` guard falling through to `_measured`). 12 lines.
- **D2-4. `recorded` recomputed at every call.** `NatureBeamWorld.recorded`
  is a property over `measured` (`world.py:886`), read at every `books()`
  (`engine.py:751`, once per interval) and by `hypotheses` (`world.py:947`).
  A frozen field set by the parser (`recorded: bool`) is O(1) and equal by
  construction; `tests/test_amplitude_layer.py:332` asserts the equality
  on every shipped world. A world built by `dataclasses.replace(...,
  measured=...)` in a test would carry the old value: the property stays
  and caches nothing, or the field is set by `__post_init__` from
  `measured`; the second is recommended (no caller changes).
- **D2-5. The books' `amplitude` flag.** `engine.py:751`, `amplitude =
  self.world.recorded`, gates the `cancelled` and `remainder` lines under
  a name that no longer exists in the world file; it is `recorded`. A
  rename, no behaviour.
- **D2-6. `DetectorSet.wave`.** `measured.py:177-180`: `wave` is true for
  `wave` and for `sum` ("the pointer's reading, at either scope"), read at
  `nature_beam.py:2345` (`st_wave`), 3196 and 3223; `sum` is the
  narrower property. The name says one reading and means two: `pointer`
  (the set reads the crowd's pointer for its phase). A rename with its
  three readers and `st_wave` -> `st_pointer`. `DetectorSet.scope` stays:
  it is the `scope` key of the `sum` record line (`nature_beam.py:3824`,
  read by `tests/test_amplitude_layer.py:433-437`), not dead.
- **D2-7. Comments that name the deleted key as live.** `nature_beam.py`
  203, 222 ("every row without the key"), 728, 746 ("the merge under the
  key"), 1121, 1151, 1155, 1157, 1649; `measured.py` 64-65, 508-510;
  `engine.py` 800; `world.py` 402-411 (the `AMPLITUDE_RULE` block, "under
  the world key `amplitude`"), 417-418 ("under the key" on
  `AMPLITUDE_LEAST_STEPS`), 530-534 (`SUM_READING`: "under the amplitude
  key alone ... the crowd's pointer threshold is its gate as under
  `wave`": the gate is deleted). Sixteen sites; each sentence says what it
  now means: a row of no record, a recorded world, the ladder's click.
  `world.py:237-242` (`wave`'s docstring) is right again after the branch
  (the threshold "the smallest amount ... summed over the whole set").
- **D2-8. `isqrt` on the host's integers.** `amplitude.py:154-165` is
  Newton's integer square root; `math.isqrt` is the standard library's
  exact one (Python 3.8). The same integers (both exact by definition);
  12 lines. The layer's `gcd`/`lcm` beside it are phase 1's U6.
- **D2-9. `run.json`'s removed keys.** The branch removed `amplitude`
  and writes `world`, `open` and `layer` for a recorded world; the one
  reader of the key, `tools/amplitude_path.py`, is updated on the branch
  (-2 lines). Nothing of the record is dead; the documents that still
  present the key as a world key are S2-1 below.
- **Phase 1's D-findings, unchanged in status:** D1 is done by the branch
  (the key and its branches); D2 is narrowed to D2-2 above (the gate's
  callers; the `wave` record and the set's phase stay by Q1/Q3); D3
  (`beam`) is not dead (Q2 kept); D4 to D8 stand as written (the migration
  tool, the two derivations scripts, `Layer.origin` at `amplitude.py:346`
  with its one caller `nature_beam.py:1778`, the alias `Pending` at
  `measured.py:86`, `event_charges` at `world.py:2265`, the four
  world-pinning tests). Phase 1's U2 shrinks as it said (the crowd's site
  of the pointer is the set's phase only); U3, U5 and U6 stand.

## 3. The stale names (the S2-findings)

- **S2-1. Documents presenting `amplitude` as a world key** after the
  branch's own document edits (MIGRATION, TERMINOLOGY, HYPOTHESES,
  TEST_EXPECTATIONS, EXPERIMENTS and the catalog are edited on the branch):
  `docs/ENGINE.md`, `docs/BEAM_LAW.md` (note 37's "under the world key"),
  `docs/TERMINOLOGY.md` and `docs/HYPOTHESES.md` where a sentence still
  says "under the key", `docs/TEST_EXPECTATIONS.md`'s rows of the five
  amplitude test files, `examples/events/amplitude/README.md` and
  `examples/events/README.md` (the two-slit row's "under the world key
  `amplitude`"), and phase 1's `PLAN.md` (D1 to D3 and section 6, amended
  by a dated line, not rewritten). `docs/VALIDATION.md` and
  `docs/designs/amplitude-v1/DESIGN.md` keep the key as history (the
  digests recorded under it; the design's stages). The rule of the
  sentence: "in a recorded world (a lamp declared)" for "under the key".
- **S2-2. Names in the code:** `AMPLITUDE_DEFAULTS` (`nature_beam.py:745`,
  the columns of a row of no record) -> `NO_RECORD_COLUMNS`;
  `_amplitude_load_checks` (`world.py:2205`, run on every world) ->
  `_record_load_checks`; the local `amplitude` of `books` (D2-5);
  `DetectorSet.wave` (D2-6); `AMPLITUDE_LEAST_STEPS` stays (the circle a
  record needs); `AMPLITUDE_RULE = "amplitude-v1"` stays (the identity
  under `hypotheses` of a recorded world, `world.py:947`); `AMPLITUDE_SCALE`
  once (phase 1's U6).
- **S2-3. Phase 1's S1 to S5 stand**, with S4 (`world.py`'s docstring)
  now also naming `u` on a record's row and the share on a click line.

## 4. The order of the commits for the phase 2 pull request

The rule of every commit (phase 1, section 5): `python tools/check.py`
scoped; the gate set replayed with `tools/run_series.py --list
examples/events/gate_set.json --compare BASE` after each commit that
touches `src`, every world `identical` in `state.json`, the ledger and
`events.jsonl`; the amplitude worlds' `run.json` `world` lists compared by
`tools/amplitude_path.py`; `--full` once at the end.

0. **The baseline.** On `main` after the one click merges (its lamp-free
   gate worlds' digests were re-pinned on the branch at 02448fa6 from main
   d768f831, and `main` has since taken the signed drive and `doppler-v1`):
   `run_series` on the fifteen gate worlds and on the amplitude series,
   the summary kept beside this plan as `gate_base_phase2.json`. The
   baseline of phase 1 (`gate_base_summary.json`, taken at 63a9fb0c) is
   stale: today's replay of #382 showed four gate worlds "changed" against
   it and identical against a fresh replay of d2e4c15a (the step drive
   moved them); a stale baseline masks or fakes a change.
1. **The names and the documents** (S2-1, S2-2, S2-3, D2-7): no behaviour;
   the language, hygiene and navigation gates.
2. **The dead code of the law before the one click** (phase 1's D4 to D8,
   U6; D2-8): the migration tool, the two derivations scripts,
   `Layer.origin`, the alias, `event_charges` -> `column_charges`, the four
   world-pinning tests moved to VALIDATION, `amplitude/expectations.json`
   under `tests/support/`, the scale and the identity defined once,
   `math.isqrt`. MIGRATION entries. Replay 1.
3. **The one click's leftovers** (D2-1 to D2-6): `Layer` not `Layer |
   None` with its seventeen sites, `pointer_units` and `POINTER_UNIT`
   deleted with test (e)'s lines, the lamp scan after `_measured`,
   `recorded` a field, the books' flag and the set's property renamed.
   Replay 2 (the largest commit of the phase in sites, the smallest in
   risk: every site is a guard that is always true or a name).
4. **U2, U3, U5** (phase 1): the pointer formed once (the faces and the
   border against the layer's `end`), the step rule and the owed count
   once, one `Border` record. Replay 3.
5. **O1**, the births batched: one `append` per family per interval. The
   one click changed the lamp's loop (`nature_beam.py:3495-3527`: `count`
   records per self-creation, `layer.birth` and the `birth` record line
   per record, then the born rows): the batching collects the store's
   rows only; the layer's `birth` and `split` calls and the record lines
   stay in their order inside the loop, so the layer sees the same
   sequence. Replay; the seconds.
6. **O2**, `node_event` kept on the simulation. Replay; seconds.
7. **O3**, the reader's charges memoized. Replay; seconds.
8. **O4, O6's free-family list, O8**. Replay; seconds. O8's premise holds
   on the branch: a gathered record's offers are read by nothing after its
   gather (`amplitude.py`, `Layer.end` on a gathered identity returns
   before the offers).
9. **Optional, its own review**: C2, `nature_beam` split into its six
   steps.
10. **The evidence**: VALIDATION's entry with the fifteen digests before
    and after, the seconds per world, the profile's ten functions before
    and after (phase 1's `profile.txt` predates the one click, whose
    records and shares add Python per row: the profile is taken again at
    commit 0 and read at commit 8); docs/README's rows; `check.py --full`.

Size, estimated: about 2,300 lines removed (phase 1's D4 to D8 1,500;
D2-1 30, D2-2 35, D2-3 12, D2-7 the sentences, U5 60, U2/U3 45, the
docstring 250, `isqrt` 12) and about 350 added; functions unified as
phase 1 said (the pointer, the step rule, the owed count, the charges,
the border tallies) plus the lamp scan; speed as phase 1's section 3.3
estimates, re-measured at commit 0 under the one click.

## 5. The risk

- **The baseline** (commit 0): the one risk that has bitten today. Every
  replay of phase 2 compares against a summary taken on the `main` the
  pull request starts from, after the one click; a difference on a world
  the commit does not touch means the baseline, not the commit.
- **D2-1**: a caller passing `layer=None` (none in `src`; none in `tests`
  on the branch; a tool constructing `nature_beam` directly: none) would
  fail at type check, not at run; `mypy` is in `check.py`.
- **D2-3 and D2-4**: the refusal's order and the field's value are checked
  by `tests/test_amplitude_record.py` (89-109: `recorded`, `hypotheses`,
  `N` 2 without a lamp admitted) and by `tests/test_amplitude_layer.py:332`
  over every shipped world; both are on the branch.
- **O1 under the one click**: the store's rows and the layer's calls are
  produced in one loop; the batching must not reorder the layer's calls
  against the record lines (the `birth` line precedes the rows' `append`
  today; it will precede the batch). The amplitude worlds' `world` lists
  and `events.jsonl` digests are the check.
- **Not in phase 2**: D3 (`beam`), Q2's decision being the owner's; the
  record-format renames of phase 1's 4.3 (Q6); the unification (3) of the
  three permutations (phase 1's U1, a design note for the physicist).
