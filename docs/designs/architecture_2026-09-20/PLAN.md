# The architecture cleanup of 2026-09-20: the plan (phase 1, read-only)

The model owner, 2026-09-20: "Can an architect run over everything, tidy up,
see what is no longer needed, and make sure there is optimization?" This is
the architect's read-only pass; nothing of the engine, the tests, the tools
or the documents was edited. Phase 2 executes it as one pull request of
small bit-exact commits after the Boss reports that the one click (stage
(vi) of `amplitude-v1`) is on `main`.

What was read: `main` at `49359cbd` (the merge of #367, `weak-v1`); the
Boss's branch `claude/universe24-new-3ytqde` at `1427af80` (the trimming,
part 1: the dated logs, the gate set, `run_series --list` and `--compare`,
the design under `docs/designs/amplitude-v1/`); the work branch
`claude/amplitude-impl` at `62369cb8` (commits (i) to (v)). Stage (vi) is
not yet visible: the brief says the record form becomes the only click and
the world key `amplitude` and the crowd-threshold `wave` reading path are
deleted; section 2 lists what dies on that assumption and section 6 the
questions it leaves. Every measurement below is of the union of the two
branches (a scratch merge of `1427af80` and `62369cb8`, no conflict), on
this machine (4 cores, 15 GB, Python 3.14.0rc2, numpy 2.5.3), with the
evidence files beside this plan: `profile.txt` (cProfile of the fifteen
gate worlds and eight amplitude worlds) and `gate_base_summary.md` (the
gate set replayed with `tools/run_series.py --list --jobs 4`: the digests
and the seconds before any change).

The documents the brief names that do not exist in any branch: none of the
three is missing, but two readers' names differ: the "F-findings of
2026-09-19/20" are records 04, 70 and 73 of `docs/LOG_2026-09-20.md`
(F1, G1 and the 23 name redundancies of Highlights 5.6), the genericity
probe is record 73 and record 90's probe of (i)-(ii).

---

## 1. Contracts and ownership

### 1.1 Every module in one line (the union tree; lines of code)

| Module | Lines | Responsibility | Verdict |
| --- | --- | --- | --- |
| `core/integer` | 83 | the work-register bound and the four integer primitives (`bounded_gcd`, `integer_root`, `by_clock`, `apportion_whole`), `reduced`, `rational_sum` | one owner, clean |
| `core/game_board` | 67 | addresses, the six Port headings, `adjacent_node`, `MAX_VALUE` | clean |
| `core/phase` | 88 | the cosine and sine tables per N, cached | clean |
| `events/world` | 2,658 | the world file: keys, bounds, refusals, the parsed records (`NatureBeamWorld`), `default_table` | one owner of the schema, but its 300-line module docstring restates the whole schema that ENGINE.md "The world" and BEAM_LAW own: a second copy (C1) |
| `events/measured` | 571 | the records beside the rows: `Measured`, `DetectorSet`, `Ledger`, `PendingRow`, `column_charges` | records only; `Measured` carries 62 fields (C5) |
| `events/nature_beam` | 3,728 | the Beam Law: the tables, the one reading, the store, `push_form`, `transform`, the amplitude lattice rules (`rotate_rows`, `apply_gate`), and the one function `nature_beam` | the one function is 1,715 lines (1953 to 3667) with five closures (`heading_port`, `collide`, `family_plan`, `admit`, `refuse`); every rule is inside it once, but the profile cannot see past its name (C2) |
| `events/meeting` | 407 | the meeting `meeting-v1`: the arc permutations, the register, `meet` | one owner |
| `events/amplitude` | 712 | the apparatus's layer: live records, offers, the rotation, the ladder, the gather | host state, per section 1.3 |
| `events/engine` | 1,023 | the frame: the clocks, the steps, the contact, the books, the snapshot, the diagnostics | `_move` re-spells the step rule beside `step_axis` (C3, record 73) |
| `events/run` | 197 | the artifacts of a run | writes `model` for `model_id` (glossary 17) |
| `runner`, `world_loading`, `configuration_validation`, `json_documents`, `snapshot_writer`, `retention`, `ui` | 88, 360, 115, 31, 57, 609, 474 | the host: loading, preflight, output, leases, the local page | untouched by this plan except the names in section 2.4 |
| `tools/*_readings.py`, `bell_chsh`, `bell_choosers`, `amplitude_path`, `run_series`, `check`, `migrate_nature_beam_worlds` | 6,900 | readers of the record, loaded by path | `coupling_readings` re-spells the step rule and the owed count (record 73); two scratch scripts of deleted laws (section 2.3) |

### 1.2 Overlapping responsibilities (C-findings)

- **C1. The schema is written twice.** `world.py`'s docstring (lines 1 to
  305) is a prose copy of the key contract that ENGINE.md "The world" and
  BEAM_LAW note 37 own; the two drift (the docstring still says a detector
  reads `"wave"` or `"beam"` and names `sum` nowhere). One owner: the
  refusals in the code and ENGINE.md's table; the docstring keeps one
  paragraph and a link.
- **C2. The one function.** `nature_beam` is one Python function of 1,715
  lines. The owner's "one generic function" is the law's identity, not a
  requirement that the source be one `def`; splitting it into the six steps
  it already names (`walk`, `collide`, `meet`, `tables`, `create`, `border`,
  `merge`), each a module-level function with the same arrays passed
  through, moves no integer and lets the profile attribute the 20 % of the
  time that today reads only "nature_beam" (section 3.2, O6). Recommended
  as its own commit at the end of the pull request, or its own pull
  request: the diff is large and behaviour-free.
- **C3. The step rule is spelled twice** in the engine: `step_axis` (the
  rule) and `_move`'s `links = ((entry.age - 1) * magnitude) // (width +
  magnitude)` (the count of Links for the turn by momentum), and a third
  time in `tools/coupling_readings.py:166`. One function `links_stepped(age,
  magnitude, reach)` that both read (section 2.2, U3).
- **C4. The gate's `hold` reads the layer.** `gate_ready` (nature_beam.py
  1669) holds a `rerelease` entry's rows until every record's live units
  are all pending at this Node: `layer.records[identity].live == here`.
  That is a rule of a Node (the gate is a measured event) reading a host
  count of rows that are elsewhere on the GameBoard. The design (section
  10, "hold: true") specifies it, and the layer is the apparatus's, so the
  gate is an apparatus event; but the contract sentence "the lattice's law
  never reads the layer" (design section 5, BEAM_LAW note 37) is then
  false for this one entry. Not a defect of the integers; a sentence to
  correct in BEAM_LAW note 37 ("the gate's hold is the apparatus's
  reading of its own record") or a hold that reads only what is pending at
  the Node (the rows of `parties` records present, whatever is elsewhere).
  Physics owner's call, listed in section 6.
- **C5. Two god records.** `Measured` has 62 fields, `FamilyPlan` 41; both
  grew a field per feature. Not a cleanup item for this pull request
  (every field is read); recorded for the day the layer and the lattice
  rules of `amplitude-v1` settle.
- **Not found:** no rule branches on a physical name (families are data;
  the rule of a family follows from its `quantum`; the tables are arrays
  of codes; the only string kinds are the layer's `("set", "face",
  "border")`, host bookkeeping). No state is kept at a Node beyond its
  events: the store's `arrival` column is the interval's scratch (8 bytes
  per row, rewritten every interval), `Measured.pending` is at the
  apparatus (a re-emitter holds what came home, declared), the arc table's
  cache and the collision table are pure functions of the world.
- **Reads at a distance, all declared:** `setting_steps` (#363) reads the
  rows present at the set's own Nodes; `detector_set.phase` is returned to
  every member of a set within the interval (the declared width, record 70);
  `gather_records` marks pending rows at the chosen re-emitter for their
  rebirth (the layer writing at the apparatus, design section 6). The
  one undeclared read is C4.

### 1.3 The layer of `amplitude-v1` against the contract

Host state per live record (`LiveRecord`: 12 fields; per (set, arm) an
`Offer` with dicts keyed by (Node, label)), owned by the apparatus, never
at a Node: within principle 5 and record 74 ("what may hold state"). Its
inputs are the apparatus's Port events alone (`birth`, `split`, `cancel`,
`rotate`, `end`, `join`), its output the gather. Two costs to record as the
host's: gathered records are never freed (`Layer.records` keeps every
record born; `complete` scans them all every interval: O(births) per
interval, quadratic over a run; today under 1 % on the largest amplitude
world, section 3.4) and `cells` recomputes the set of labels present once
per cell instead of once per record. Both are bit-exact fixes (O8).

---

## 2. What is no longer needed once the one click lands

**Amendment of 13:00 UTC.** Record 101 of 2026-09-20: stage (vi) was
stopped by its rule and the key `amplitude` is kept; the one click is
stage (vii), in flight (record 103). D1, D2 and D3 below therefore wait for
stage (vii) and are not part of the cleanup pull request until it lands;
D4 to D8 and the rest of the plan stand. The gate fix of stage (v) (merged
in #370, record 109) resolved C4: the hold reads the pending rows alone.


### 2.1 Dead paths (D-findings), each with its evidence and MIGRATION line

Assumption for D1 to D3: stage (vi) as the brief states it. Where (vi)
decides otherwise the item moves to section 6.

- **D1. The world key `amplitude` and every "needs the key" branch.**
  Sites: `world.py` 64 mentions (the key's parse, `AMPLITUDE_LEAST_STEPS`,
  twelve refusals of the form "is the amplitude law's ... and needs the
  world key", `_amplitude_load_checks` gated on the key, the `amplitude`
  argument threaded through `_families`, `_lamp`, `_split`, `_label_turn`,
  `_rotation`, `_gate`, `_measured`, `_detectors`), `nature_beam.py` 52
  (30 conditionals `if world.amplitude`, the merge's `modulus if
  world.amplitude else 0`, `PendingRow.split=world.amplitude and ...`,
  `record_line(amplitude)`), `engine.py` 11 (`self.layer = None` unless
  the key; the `if layer is not None` guards, 25 sites in nature_beam),
  `measured.py` 6, `run.py` 5 (`"amplitude": world.amplitude`, the
  `hypotheses` entry). After (vi) every one is unconditional: the layer
  always exists (`Layer`, not `Layer | None`), the merge always takes the
  modulus, the three columns are always written to `state.json`, `N` below
  4 is refused for every world. `AMPLITUDE_DEFAULTS` (0, 0, 1 for a row of
  no record) stays: free families and declared rays carry no record.
  Evidence that nothing else reads the key: `grep -rn "\.amplitude\b"` over
  `src`, `tools`, `tests` finds the engine sites, `tools/amplitude_path.py`
  (reads `run.json`'s key) and the five `tests/test_amplitude_*.py`, whose
  worlds declare it. MIGRATION: the Boss's (vi) entry names the key
  deleted; the cleanup's entry names the branches removed and the
  `hypotheses` identity `amplitude-v1` kept or dropped per (vi).
  Estimated 250 lines removed.
- **D2. The crowd-threshold `wave` reading.** Sites: `pointer_units` and
  `POINTER_UNIT` (nature_beam.py 910 to 926; used at one site, `admit`'s
  `below_wave`), `st_wave`, `wave_rows`, `gated`, the set's phase read from
  the crowd's pointer for the window (`read_phase`, 2446 to 2477), the
  per-interval `record` line and `detector_set.record += X^2 + Y^2` under
  `wave` (3086 to 3130), `plan.pointer`, `plan.set_phase`,
  `DetectorSet.wave` and `DetectorSet.scope` (measured.py 174 to 194),
  `DETECTOR_READINGS = ("wave", "beam")` and the default reading of a
  measured event outside every detector (`DETECTOR_READINGS[0]`, engine.py
  246). What stays: `coherent_pointer` and `pointer_phases` (read by
  `setting_steps` for #363's window from a reading, by the faces' and the
  border's `record`, and by the set's phase returned to its measured
  events if (vi) keeps that return). The 1,525 `"reading": "wave"`
  declarations in the register (the lensing pixels, the Heisenberg
  `w*_wave` worlds, the two slits, the catalog screen) and the 273 `"sum"`
  ones: section 6, Q1. Tests that only serve the path:
  `tests/test_nature_beam_detector.py` cases (a) to (g), (i), (j) (the
  pointer gate, the set's phase, the pointer's register path: 9 of its 11
  tests), `tests/test_buildup_readings.py` with `tools/buildup_readings.py`
  (381 lines: A10 at a low rate under `wave`, the run superseded by the
  record click of record 94 and series L), `tests/test_heisenberg_readings.py`
  and `tools/heisenberg_readings.py` where they read the `wave` record
  (the `beam` reading stays, Q2). The pointer arithmetic tests ((e) the
  tables' bound, (j) the first moment) move to `test_amplitude_layer.py`
  as tests of the layer's pointer, the same integers. MIGRATION: "`wave`
  deleted on 2026-09-20 with the one click: the record of a set is the
  layer's per record; the crowd's pointer stays on the faces and the
  border, and in `setting_steps`". Estimated 150 lines of engine, 400 of
  tests and tools.
- **D3. The `beam` pairing** (`admit`, nature_beam.py 2536 to 2581: the
  O(n^2) greedy pairing by opposite phase, `plan.count`, the `beam` record
  line): dead only if (vi) makes `sum` the one reading. 649 registered
  worlds declare `beam` (the Heisenberg `w*_beam`, weak `j3_neutron_free`,
  the A2 Bell worlds through their detector definitions). Q2 in section 6;
  80 lines if deleted.
- **D4. `OLD_LAW_VALUE = "rays"` and `tools/migrate_nature_beam_worlds.py`**
  (242 lines, the rewrite of the first NatureBeam worlds to the form of
  2026-09-20). Evidence: no world in `examples/` declares `"law": "rays"`
  or a family `kind` (the grep's ten hits are `"gate": {"kind": "cnot"}`).
  The refusal message that names the tool stays as a refusal (glossary
  item 22: a refusal table names the law); the tool is deleted unless Q1
  gives it the `wave` rewrite. MIGRATION: "the migration tool deleted;
  rewrite a 2026-09-19 world with git at `62369cb8` or earlier".
- **D5. `tools/derivations_round7.py` and `derivations_round8.py`**
  (804 and 317 lines): "scratch computations ... not an engine run" for
  DERIVATIONS.md rounds 7 and 8 (the law of the shadow and "a thing
  emits", both deleted on 2026-09-19). Referenced by DERIVATIONS.md
  (4252, 5141) and MIGRATION 788; imported by nothing; the architecture
  table lists them as "numpy only". Delete with the two DERIVATIONS.md
  sentences pointing to git at the deletion commit; MIGRATION line. The
  owner's call (they are the paper trail of two rounds): recommended.
- **D6. Small dead code, each with a grep of one site or none:**
  `Layer.origin` (an identity function, one caller at nature_beam.py 1727;
  the gate's label map keys by the row's own record, so the call is
  `row.record`); the alias `Pending = PendingRow` (measured.py 82, no
  reader); `NatureBeam.record_line(amplitude)`'s flag (always true after
  (vi)); `DetectorSet.scope` (a report string of `run.json`'s record line,
  dead with `wave`). About 20 lines.
- **D7. `world.event_charges`**, "the parser's copy of the engine's
  reading of the same, `measured.column_charges`" (its own docstring;
  record 73): `_column_budget` calls `column_charges` with the same terms
  (the overflow check inside it is the run's, harmless at load; the
  reduced pairs are the same rational sums). 18 lines.
- **D8. Tests that pin an example world's numbers**, against Highlights
  5.5 ("no test pins the numbers of an example world, compares two worlds
  or reproduces a known experiment"): `tests/test_nature_beam_worlds.py`
  `test_the_two_slits_fringe_in_the_record_and_not_in_the_count` (runs
  the shipped two-slit worlds, asserts a correlation above 0.85),
  `test_the_bell_worlds_read_the_triangle_and_the_chsh_bound` (runs the
  ten A2 worlds through `bell_chsh`, asserts S = 2 and 3/2),
  `test_one_content_streams_outward_with_the_books_closed` (the flux of
  `one_content`) and `test_two_contents_is_not_refused_and_its_face_records_are_exact`.
  Each is a research run made every check; the gate set is now the replay
  (`a0_b0` covers the Bell path, and the two slits are in the amplitude
  series). The evidence each asserts is already a VALIDATION entry (the
  Bell ten at S = 2, record 71; the two slits' fringe, series A). Move the
  four to VALIDATION with their integers and delete; keep the parse tests
  and the gate-set test. About 120 lines and 10 s of every full check.
  Owner's rule; the test owner confirms.

### 2.2 Duplicated logic (U-findings), against the design's unifications

- **U1. Unification (3), "the collision, the meeting and the gate as one
  permutation component at a Node with three tables": not done.** The
  collision is `collide` (a table over 3^8 slot states, permuting
  directions of single units per (Node, number, content) class), the
  meeting is `meeting.meet` (an arc permutation of directions per target,
  k steps read off the phase register), the gate is `apply_gate` (a
  permutation of joint labels of pending rows at a re-emitter, through the
  layer's `join`). Three data models: slot codes, direction indices,
  label bits; three call sites in `nature_beam` (step 3, step 3 after the
  table, step 5). Unifying them is a change of interfaces with no integer
  moved only if each keeps its table; a `Permutation` protocol (`apply(rows)
  -> rows`, `inverse`) over the three would be a refactor of about 300
  lines with the gate's `join` still the layer's. Recommended: not in the
  cleanup pull request; a design note for the physicist, since the
  meeting's inverse and the gate's `hold` differ in kind (the collision and
  the meeting are per Node in free space, the gate at an apparatus).
  Record 86 asks each unification "done or refused with the reason": this
  is the reason.
- **U2. Unification (4), "`sum` and `wave` one reading of the one pointer,
  one scope key": half done.** `DetectorSet.scope` names the scope, but
  the pointer is formed twice: `coherent_pointer` (`read_groups` on the
  circle's unit vectors with 32 x amount, in the register or in Python
  integers) for the crowd, the faces and the border, and `Layer.end`
  (`weight * cosines[phase], weight * sines[phase]`, Python integers) for
  the record. The same integers by construction; one function
  (`pointer_of(amount, phase, cosines, sines)`, scalar, Python integers)
  called by both is bit-exact. After (vi) the crowd's site is dead (D2),
  so the duplication shrinks to the faces and the border against the
  layer. 15 lines.
- **U3. The step rule** three times (C3): `step_axis`, `_move`'s Links
  count, `coupling_readings.py:166`; and the owed count once in the engine
  (`count_owed`) and once in `coupling_readings.py:864` (the tool's own
  replay of the clock). One function each in the engine, the tool reading
  it (ARCHITECTURE's rule: "a tool calls the engine's functions, it owns no
  rule"). 30 lines.
- **U4. The moment table is formed at four sites**, all through the one
  `moment_table`: `family_plan` (once per family per interval with the
  admitted rows: the reading), `coherent_pointer` -> `read_groups` (the
  pointer on the circle), `read_arrivals` (the tests and the dense
  diagnostics) and `GameBoardDiagnostics._decompose` (on request). One
  function, four callers: this is the unification landed on 2026-09-20
  (record 64 (3)); nothing to do. The per-set pointer of `admit` under
  `wave` is a fifth call that D2 removes.
- **U5. The two ledgers** are by design (section 3.5: the GameBoard's over
  every row, the world's list over the path). Inside the first, the
  per-border tallies are three parallel structures with one shape:
  `face_*` (dicts by Port), `lifetime_*` (lists by family) and
  `cancelled_*` (lists by family), each with `amount`, `content`, `record`,
  `momentum` and a `_total` method; and `Measured.taken[family][rule]`,
  `Measured.clicks[family]` and `Ledger.held_measured[family]` count one
  click three ways (the tally by rule, the units, the content). One
  `Border` record (amount, content, record, momentum per family) held
  per face, for the border and for the cancel would delete about 60 lines
  of `Ledger` and `engine.face_detectors`; bit-exact. Recommended for the
  cleanup pull request as one commit.
- **U6. Twice-defined constants and two meanings of one name:**
  `AMPLITUDE_SCALE = 32` in `nature_beam.py:159` and `amplitude.py:85`;
  `IDENTITY` is `np.eye(3)` in nature_beam and `256^2` in amplitude;
  `amplitude.gcd`/`lcm` beside `core.integer.bounded_gcd` (the layer's are
  unbounded on purpose: rename `host_gcd`, `host_lcm`). One definition of
  the scale in `core/phase` or `nature_beam`, imported by the layer. 10
  lines.

### 2.3 Stale documents and names (S-findings)

- **S1. The trimming plan's stale-name list (Highlights 5.6).** The
  glossary's tables say "Defined in RAY_LAW n" (70 mentions of `RAY_LAW`
  in HIGHLIGHTS.md, all in 5.6's "Defined in" and "Where" columns),
  `parse_ray_world` (the world-file keys' table header and 48 rows'
  "Computed in"), `RayStore.flat`, `RayWorld.phase_steps`, `execute_ray_run`,
  `RAYS_LAW = "rays-v1"`, `LAW_VALUE` "the string `rays`". The glossary is
  a live table ("a name's row is the definition"; Highlights 5.6's own
  header), so the names are rewritten: `RAY_LAW` -> `BEAM_LAW`,
  `parse_ray_world` -> `parse_nature_beam_world`, `RayStore` ->
  `NatureBeamStore`, `RayWorld` -> `NatureBeamWorld`, `execute_ray_run` ->
  `execute_nature_beam_run`, the `law` row's value `"beam"` and
  `BEAM_LAW = "beam-v1"`. The 42 `rays-v1` mentions elsewhere are dated
  migration anchors (`MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1`
  in BEAM_LAW, ENGINE, TERMINOLOGY, TEST_EXPECTATIONS, VALIDATION,
  PROJECT_STATUS, SIMULATOR_DEFINITIONS, three READMEs) and register lines
  in EXPERIMENTS: history, untouched, as are MIGRATION (44), CHANGELOG (24)
  and the logs. Glossary items already resolved by the code and to be
  marked so: 7 (`DOCUMENT_KINDS`), 11 (`K`), 21 (`push_form` exists since
  the four unifications: BEAM_LAW, ENGINE, TERMINOLOGY and TEST_EXPECTATIONS
  now name a real function), 23 (`face:*` refused). Items still open in
  the code: 1 (`Reading.scalar` is now `Moments.presence`: done; `Readings`
  is `GameBoardDiagnostics`: done), 6 (`push` on a click line is still the
  label), 9 (`tick`/interval), 10 (`Measured.turned` done, `FlightTable.resolution`
  done), 13 (`mass` column gone: done), 15 (`Measured.clicks` done; `state()`
  still writes `events`), 16 (`position` vs `node`), 17 (`model`), 18
  (`measured`/`number` on event lines), 20 (`reading` -> `component` on
  record lines). Items 6, 15, 17, 18 and 20 change record keys: every
  reading tool and the digests move; a rename commit of its own with the
  tools' readers updated, or deferred (section 5 puts it last, optional).
- **S2. ARCHITECTURE.md's dependency table** has no row for
  `events/amplitude` (imports `core/phase`, `events/measured`) nor
  `events/meeting` (imports `core/integer`, `events/world`, numpy), and its
  `tools/` row predates `bell_choosers`, `amplitude_path`, `weak_readings`,
  `nucleus_readings`, `lensing_readings`, `hubble_readings`, `bohr_readings`,
  `buildup_readings`. `tests/test_architecture.py`'s gate checks the
  direction, not the table: the table is prose and stale. Rewrite the rows
  from the imports.
- **S3. PROJECT_STATUS.md** says the weak force, the meeting and #363 are
  "in flight" (all merged in #366 and #367) and names no `amplitude-v1`;
  HIGHLIGHTS_IMPLEMENTATION.md is "as of 2026-09-19" in its header while
  its rows are of 2026-09-20; docs/README.md's worlds row names the
  amplitude series as "the Mach-Zehnder and Elitzur-Vaidman worlds" (the
  pair, the gate and the N = 1024 and 4096 runs are in the folder); the
  "What each document owns" row of ENGINE.md still carries a "The law of
  events (`events-v1`)" section (ENGINE.md 719: a deletion notice; move
  its one sentence to MIGRATION's anchor and delete the heading).
  Part 2 of the trimming (record 98) names PROJECT_STATUS and CHANGELOG;
  this plan takes the status file and the index rows only.
- **S4. `world.py`'s docstring** (C1): the detector paragraph names
  `wave` and `beam` only; the lamp paragraph does not name `turns`,
  `branches`, `arms`; the table-entry paragraph none of `inputs`,
  `weights`, `turns`, `turn`, `rotate`, `gate`. After D1/D2 it is rewritten
  as one paragraph and a link, not extended.
- **S5. `TEST_EXPECTATIONS.md`** and the register entries name
  `tests/test_buildup_readings.py` and the `wave` cases of
  `test_nature_beam_detector.py` (D2): the rows move with the tests.

### 2.4 Worlds no series cites, scratch scripts, generated files

- Every world of the thirteen registered series is cited by its series
  README or by the register (checked by stem for the orbit, Bohr, coupling,
  nucleus, Heisenberg, weak and lensing folders) or generated by the
  folder's `make_worlds.py`; none is deletable, and record 87 says "files
  not runs, none deleted".
- The amplitude folder holds 49 worlds; its README and EXPERIMENTS L cite
  the Mach-Zehnder, Elitzur-Vaidman and the two-slit worlds (stage (iii))
  and nothing of stages (iv) and (v): the 14 `bell_*` (including the eight
  at N = 1024 and 4096), the 13 `cnot_*`, `ghz_*`, `rotations_3`, the five
  `path_*`, `slits_one` and `bell_choosers.json` have no register entry
  yet. Not dead: the entries L4 to L6 are the Boss's (record 98, part 2).
  `examples/events/amplitude/expectations.json` (917 lines) is read by
  `test_amplitude_gate.py`, `test_amplitude_pair.py` and
  `test_amplitude_layer.py` as their pinned integers (the design's numbers
  written before the run): a data file of tests living under `examples/`
  (the rule since 2026-09-17 puts a test's integers in the test or under
  `tests/`); move it to `tests/support/amplitude_expectations.json` with
  the three readers. The weak folder has the same pattern
  (`weak/expectations.json`, read by `tools/weak_readings.py`: a tool's
  file, stays).
- Scratch scripts committed: `tools/derivations_round7.py` and
  `round8.py` (D5); nothing else under `tools/`, `src/` or `examples/` is a
  one-off (every `make_worlds.py` generates a registered folder;
  `tools/generic_vector_lab/`, 4,490 lines, is the documented opt-in lab
  of ARCHITECTURE's last section, outside the engine: not touched by this
  plan, listed for the owner as the one large tree that no series and no
  test of the engine reads).
- Generated outputs: none committed (`artifacts/` ignored; the check-scope
  report is written there).

---

## 3. Optimization, measured

### 3.1 The baseline

`tools/run_series.py --list examples/events/gate_set.json --jobs 4` on the
union tree (`gate_base_summary.md` beside this plan: the digests of
`state.json`, the ledger and `events.jsonl` per world, the runner's seconds
and the peak RSS). The runner's seconds per world (no profiler):

| world | ticks | seconds | peak RSS MB | events.jsonl |
| --- | --- | --- | --- | --- |
| `heisenberg/w27_beam` | 350 | 96.4 | 224 | 51 MB |
| `hubble/pushing_age` | 400 | 51.4 | 296 | 6 MB |
| `weak/j3_deuteron_crowd` | 700 | 27.7 | 79 | 133 MB |
| `weak/j3_deuteron` | 700 | 27.3 | 80 | 134 MB |
| `bohr/r2` | 3000 | 25.0 | 108 | 140 MB |
| `lensing/heavy_meeting` | 400 | 20.0 | 90 | 20 MB |
| `nucleus/alpha_square` | 3000 | 17.1 | 202 | 146 MB |
| `weak/j2_ladder` | 1037 | 4.0 | 56 | 6 MB |
| `heisenberg/w1_beam` | 350 | 4.5 | 209 | 9 MB |
| the other six | | under 1 s each | | |
| the gate set, four jobs | | 97 s wall (the longest world), 277 s of runner time in all | | |

Record 91's "about 55 s with four jobs" was another machine; the before
and after of phase 2 are both measured here.

### 3.2 The ten hottest functions (cProfile, the fifteen gate worlds and eight amplitude worlds, 367.7 s in all; `profile.txt`)

| share | tottime s | calls | function | what it is |
| --- | --- | --- | --- | --- |
| 20.2 % | 74.3 | 12,343 | `nature_beam` (its own lines) | the per-entry Python loops of steps 4 and 5: the record dicts, `PendingRow`s, `apportion_whole`, the born lists |
| 14.6 % | 53.8 | 48,495 | `NatureBeamStore.append` | `np.concatenate` of the eleven columns once per (measured event, family) that releases: O(store) per call |
| 6.9 % | 25.4 | 216,546 | `numpy.full` | `node_event = np.full(nodes, -1)` once per interval over the whole GameBoard (301^3 = 27 M Nodes on `pushing_age`: 218 MB allocated and filled 400 times) |
| 3.9 % | 14.3 | 3,539,949 | `json.encoder.iterencode` | one `json.dumps` per record line |
| 2.7 % | 9.9 | 4,406,151 | `measured.column_charges` | the reader's charges, formed twice per measured event per interval (`_frame_all` and `books`) |
| 2.6 % | 9.6 | 2,354,311 | `numpy.ufunc.reduce` | the sums and maxima of the readings |
| 2.2 % | 7.9 | 4,406,151 | `Measured.charges` | the caller of the above (`charges(for_push=True)` in the frame, `charge` in the books) |
| 2.0 % | 7.5 | 6,763,138 | `core.integer.bounded_gcd` | the reduction of every rational pair of the charges |
| 2.0 % | 7.5 | 46,827 | `NatureBeamStore.keep` | the mask copies after the walk, the tables and the merge |
| 1.9 % | 6.9 | 662,755 | `numpy.array` | the small arrays of the born rows and the records |

Below them: `take` 1.7 %, `books` 1.4 %, `argsort` 1.4 %, `write` 1.3 %,
`_frame_all` 1.2 %, `merge_key` 1.0 %, `family_plan` 1.1 %, the record
closure of `run.py` 0.8 %. The charges' whole chain (`charges`,
`column_charges`, `rational_sum`, `reduced`, `bounded_gcd`, `checked_work`)
is 10.4 % cumulative; the record stream (`dumps`, `write`, `record`) 7 %;
the merge and sort (`keep`, `take`, `argsort`, `merge_key`) 6 %.

Per world the shares differ: `append` is 53 % of `w27_beam` (31 lamps
and 27 re-emitters, one append each per interval into a store of tens of
thousands of rows); `numpy.full` is 46 % of `pushing_age`; the charges are
39 % of `heavy_meeting` (1,683 measured events), 35 % of `j2_ladder`, 22 %
of the deuterons; the record stream is 20 % of `r2` and 25 % of
`alpha_square` (780 k lines each); `nature_beam`'s own lines are 11 to
21 % everywhere.

### 3.3 The bit-exact optimizations (O-findings), each with its expected gain and its proof

The proof of every item is the same: the gate set replayed with
`run_series --list --compare gate_base_summary.json` after the commit,
every world `identical` in `state.json`, the ledger and `events.jsonl`,
plus the amplitude worlds' `run.json` `world` lists compared by
`tools/amplitude_path.py`. The reasoning why each cannot move an integer is
given per item; the replay is the evidence.

- **O1. Batch the births: one `append` per family per interval.** Step 5
  visits the measured events in number order and appends each one's born
  rows to the store at once; the store is then merged (a sort by the
  packed key and a segmented sum). Collecting every entry's born columns
  in lists and concatenating once per family at the end of step 5 yields
  the same arrays in the same order (concatenation is associative), so the
  merge sees identical input. Everything between an entry's append and the
  end of step 5 reads only that entry's own records (its `momentum`, its
  ledger lines, the `become` record), never the store. Expected: `append`
  from 53.8 s to under 2 s over the profile; `w27_beam` from 96 s to about
  45 s; the gate set's wall from 97 s to about 52 s (the next longest world,
  `pushing_age`, after O2 about 27 s, then the deuterons at 27 s).
- **O2. Build `node_event` once.** The array over every Node that maps a
  Node to its measured event is rebuilt from `DetectorSet.nodes` every
  interval; its content changes only when a body steps (`_place`) or leaves
  (`_place(entry, ())`). Keep it on the simulation, updated in `_place`,
  passed into `nature_beam`; the same values at every read. Expected:
  `pushing_age` from 51 s to about 27 s; 25 s of the profile's 368.
  (The dense diagnostics of `GameBoardDiagnostics` are already on request.)
- **O3. Memoize the reader's charges.** `column_charges` is a pure function
  of (`family_values`, `held`) and the `for_push=False` form adds the paid
  units (`clicks + pending`); a cache on the `Measured` keyed by
  `(tuple(held), tuple(units))` returns the same pairs (the same
  `rational_sum` on the same terms). `held` changes at a click, a lamp's
  spend, a transformation and a home; most bodies of a lattice world never
  change, and the frame and the books each ask once per interval. Expected:
  9 to 10 % of the profile; `heavy_meeting` from 20 s to about 13 s, the
  deuterons from 27 s to about 22 s, `j2_ladder` from 4.0 to 2.7 s.
- **O4. `_column_budget`'s quadratic scan at load.** For every measured
  event and family it takes the maximum release over every other event:
  O(measured^2 x families) at parse (8.5 M generator steps, 2.2 s of
  `heavy_meeting`'s load; the same on every 1,681-pixel lensing world).
  The two largest releases per family, taken once, give the same maximum
  for every event. Bit-exact: the same refusal on the same worlds.
- **O5. Not planned: the merge and sort** (6 %). The walk sorts by Node
  and the merge sorts again by the packed key whose first field is the
  Node; the first sort could go, but the relative order of the rows of a
  body's several Nodes decides the order of its `pass` and `click` lines
  and of the `beam` pairing, and a stable sort by Node and a stable sort
  by the old key differ across Nodes. Measured, recorded, not changed.
- **O6. Not planned as an optimization: `nature_beam`'s own 20 %.** It
  is the Python of the records per row and the per-entry bookkeeping; the
  first step is C2 (the split into step functions), after which the
  profile says which loop. One measured item inside it: step 5 tests every
  measured event every interval with `any(free and held > 0 ...)` over
  the families (3.7 M generator steps on the deuteron, 0.5 s): a
  precomputed list of the free families makes the test two comparisons.
- **O7. The record stream** (7 %, 3.5 M lines): `json.dumps` per line is
  the bytes of `events.jsonl`; a faster encoder or fewer lines would
  change the digest. The 1 MB buffer is in place. Recorded as the floor
  of a run with a record; a run without an observer pays none of it.
- **O8. The layer** (under 1 % today): free a gathered record's offers
  after its gather is written (its identity stays in a set for the lazy
  drop and the counts), and hoist `present` out of `cells`' cell loop.
  Bit-exact: `end` on a gathered record returns before reading the offers;
  `open_records` and `report` read the counts. For the day a lamp runs for
  4,096 births (the N = 4096 Bell worlds: 4,116 intervals, `complete`
  scanning every record born each interval).

Expected in all, on this machine: the profile's 368 s to about 250 s
(O1 52, O2 25, O3 35, O4 2); the gate set's wall with four jobs from 97 s to
about 55 s; the serial runner time from 277 s to about 190 s.

### 3.4 Memory

- **The store per row:** eleven int64 columns (`FIELDS`), 88 bytes; the
  walk's transients per row (`coordinates` 24 B, `step` 24 B after the
  int8 to int64 cast, `port` 8, `arrival` 8, three masks 3 B) about 150
  bytes, freed per interval; the merge's `take` copies the eleven columns
  once (another 88). Peak about 3 x 88 bytes per row plus the record.
- **Per Node:** `node_event` 8 bytes per Node per interval (O2 makes it 8
  bytes once); the dense diagnostics only on request. The peak RSS of
  `pushing_age` (296 MB) is the 27 M-Node array; of `w27_beam` (224 MB) the
  store's rows and the 72 MB `state.json` written at the end.
- **The layer per record:** a `LiveRecord` and per (set, arm) an `Offer`
  whose dicts are keyed by (Node, label): about 1 to 2 KB for the
  Mach-Zehnder (two sets), growing as sets x labels x Nodes reached (the
  two-slit record reaches up to 121 pixel sets). Never freed today (O8).
- **The layer per record, time** (`slits_low`, 460 records, 22,302 ends):
  `end` 13 us per row ended, `cells` 3.3 ms per record (the product over
  the ends' Node tuples), `complete` 0.9 ms per record: about 4.7 ms per
  click of the run against the lattice's 28 ms per interval; on
  `bell_n1024_0_128` (1,044 records) the layer is 8 % of 3.9 s.

---

## 4. The schema

### 4.1 Every world key, its bounds and its refusal (from `world.py`; the record's spelling)

| Key | Where | Bounds | Refused | Overlap |
| --- | --- | --- | --- | --- |
| `law` | world | `"beam"` | `"events"`, `"rays"` (by name), anything else | none |
| `model_id` | world | nonempty string | | `run.json` writes it as `model` (S1 item 17) |
| `shape` | world | three extents 1 .. 4096 | | |
| `boundary` | world | `"open"` or `{x,y,z: open|periodic}` | a closed GameBoard | |
| `ticks` | world | 0 .. 2^62 - 1 | | `run.json` `tick` = `completed_ticks` on success |
| `K` | world | an integer from 1, or `[n, d]` | | one rate, two spellings (accepted since record 64) |
| `N` | world | a power of two, 2 .. 4096 (4 .. under `amplitude`) | | |
| `release`, `suspension` | world | `[n, d]` or an integer; `suspension` 0 off | | the `_ratio` convention, one function |
| `width` | world | from 1 | 0, negative | "width" also names a window's width and a set's extent (glossary 12) |
| `age_bound` | world | from 1; required on an all-periodic GameBoard; default 2 x flight bound | | |
| `action` | world | from 1 | | with `phase_by_momentum` |
| `meeting` | world | bool | with a phase-less paid family | |
| `amplitude` | world | bool | N < 4 | deleted by (vi) |
| `directions` | world | primitive vectors within +-`direction_bound`, at most 4096 entries with the eight built in | a repeat, the zero vector | |
| `direction_bound` | world | 1 .. 4096, default 64 | | derivable from `directions`: redundant |
| `families[].name`, `quantum` | family | string; 0 .. 2^30 - 1 | `kind` | |
| `families[].charge` | family | integer or `[n, d]`; a paid family whole | `columns.charge` beside it | one value, two homes |
| `families[].columns` | family | `{name: {value, sign}}`, at most 8 in all, `gravity` never | a paid family's nonzero value, two signs of one name | |
| `families[].lifetime` | family | 1 .. `age_bound`, scalar | a list | |
| `families[].phase` | family | bool | | |
| `families[].phase_per_link` | family | 0 .. N - 1, or `[n, d]` under the key | the pair without the key; on a phase-less family | two rules under one key: per Link crossed (the integer) and per interval of age (the pair); unification (1) chose it; the two agree only when every interval crosses a Link |
| `measured[].position`, `family`, `amount` | event | in the GameBoard; a family name; from 1 with `2 x content x n < d x N` | two events at a Node, a body off the GameBoard | |
| `measured[].held` | event | `{family: content >= 1}` | the own family, unknown | |
| `measured[].phase`, `momentum`, `fixed`, `span`, `phase_by_momentum` | event | 0 .. N - 1; three integers; bool; three odd extents; bool | `phase_by_momentum` without `action`, on `fixed`, phase-less | |
| `measured[].directions` | event | indices or vectors of the table, distinct | a rest direction | also `lamp.directions`, an independent default of the six headings |
| `measured[].table[family]` | entry | a rule or `{rule, phase_window, phase_width, reads, into, products, inputs, weights, turns, turn, rotate, gate}` | a window or width on `pass` or phase-less; `at`, `crowd` here | see 4.2 |
| `phase_window` | entry, lamp | 0 .. N - 1, or `{reads: family, offset}` on an entry | on `pass`; `reads` of its own family | on a `wave`/`beam` entry a gate; on a `sum` entry the rotation's setting; on a `rerelease` under the key refused unless the Node reads a `sum` set; on a lamp a release gate |
| `phase_width` | entry, lamp | 1 .. N | without a window | |
| `reads` | entry | `scalar`, `outside`, `here`, `vector`, `tensor`, `age` | | three meanings of "read": the component (this key), the reading (`detectors[].reading`), the family a window reads (`phase_window.reads`) |
| `into`, `products` | `become` entry | a family; `[[family, amount >= 1, content]]` | on any other rule; charges that do not balance | |
| `inputs`, `weights`, `turns` | `rerelease` entry | directions; integers from 0, one positive per row; 0 .. N - 1 | without the key, on another rule, on a free family | `turns` also on a lamp (per direction); `turn` on a `sum` entry; `rotate.turn` |
| `turn` | `sum` entry | 0 .. N - 1 | on `pass` | four spellings of "a phase step added": `turn`, `turns` (lamp, split), `rotate.turn`, and `phase_per_link` |
| `rotate` | `rerelease` entry | `{setting 0 .. 2N - 1, bit 0 .. 31, turn 0 .. N - 1}` | on another rule | `setting` is a second spelling of the half-angle window (`phase_window` on a `sum` entry is one) |
| `gate` | `rerelease` entry | `{kind: cnot, hold, parties 1 .. 32}` | on another rule | |
| `measured[].lamp` | event | `{rate [n, d] (= [1, 1] under the key), directions, phase_window, phase_width, turns, branches [[label, weight]], arms}` | on a free family; on a charged paid family; `headings` | |
| `measured[].become` | event | `{at >= 1, into, products, crowd >= 0}` | without `at`; unpaid products | |
| `in_transit[]` | ray | position, family, number 1 .. events, direction (rest allowed), amount >= 1, phase, age 0 .. `age_bound` | `heading`; an age at the lifetime | |
| `detectors[]` | set | name (not `face:*`, `lifetime`, `measured:*`), positions of measured events (each in one set), threshold >= 1, reading `wave` / `beam` / `sum` (`sum` under the key) | | a measured event outside every set is a set of one with threshold 1 and the default reading |

### 4.2 The one canonical spelling, recommended

- One key for "the phase step added to a row": `turn` (a scalar on an
  entry or a rotation, a list per direction on a lamp and a split);
  `rotate.turn` becomes the entry's `turn`; `turns` becomes `turn` where
  the value is a list. One key for a rotation's setting: `phase_window`
  (the half-angle setting on a `sum` entry today), so `rotate.setting`
  becomes `phase_window` of the `rerelease` entry and `rotate` keeps
  `bit` alone. This is the design's own reading ("the counter's
  `phase_window` under the key is the rotation `U_s`", section 4.1).
- `reads` (the component) -> `component`; `phase_window.reads` (the family
  whose pointer gives the centre) -> `phase_window.from`; `reading` stays
  the set's law. Three words for three things.
- `direction_bound` derived from the table (deleted as a key, kept as the
  refusal's bound).
- These are record-moving renames (a world's keys); they belong to the
  Boss's schema commit with `migrate_nature_beam_worlds.py`'s successor or
  to none; the cleanup pull request does not touch keys.

### 4.3 The run's record: redundant fields

- `run.json`: `measured_content[t]`, `transit_content[t]` and `momentum[t]`
  repeat `audit[t].families[f].measured.current`, `.transit.current` and
  `audit[t].momentum` for every tick (three arrays, one per line of the
  audit); `escaped[]` repeats the sums the face detectors carry under
  `detectors`; `model` is the world's `model_id`; `tick` equals
  `completed_ticks` on success; `hypotheses` is derived from `action`,
  `meeting`, `amplitude`, the columns and the lifetimes, all present;
  `directions` lists the two rest vectors and the six headings that every
  world has; every face's and the border's `families[f].measured` equals
  its `clicks` by construction.
- `state.json` repeats `measured`, `detectors` and `escaped` of `run.json`;
  only `nodes` is its own.
- `Measured.state()`: `content` = sum(`held`); `charge` =
  `charges["charge"]`; `home` and `home_content` are `pending` summed;
  `phase_steps` is the cumulative turn (a homonym of the world's N,
  glossary 10: `turned`); `events` is `clicks` (glossary 15); `measured`
  is the tallies (`taken`).
- `events.jsonl`: `push` on a `click` line is the row's label (glossary
  6); `measured` and `number` on a line are the reader and the emitter
  (glossary 18); a `record` line's `number` is always 0; `reading` on a
  `read`/`click` line is the component (glossary 20).
- All of these are record keys: removing one changes the digests and
  every reader (the tools, `run_series`, the pages). Listed; deferred to a
  record-format commit that the owner calls for, never mixed with the
  bit-exact commits.

---

## 5. The pull request, in bit-exact commits

Rule (the workflow, "the cost of an integration, kept short"): `python
tools/check.py` scoped per commit; the gate set replayed with `--compare`
after the first behaviour-free commit and at the end; `--full` once at the
end. Every commit `identical` on the fifteen worlds and on the amplitude
worlds' `world` lists. Order:

1. **The names and the documents** (S1 to S5, the glossary's stale names,
   ARCHITECTURE's rows, docs/README, PROJECT_STATUS, the ENGINE stub).
   Check: the language, hygiene and navigation gates. No code.
2. **The dead code of the law before (vi)** (D4 to D8, U6): the migration
   tool, the two derivations scripts, `Layer.origin`, the alias,
   `event_charges` -> `column_charges`, the four world-pinning tests moved
   to VALIDATION, the expectations file under `tests/support/`, the
   constants defined once. MIGRATION entries. Check: scoped; the gate set
   replayed (the first replay).
3. **The leftovers of the one click** (D1, D2, D3 per Q2): every key
   branch unconditional, the `wave` path deleted, the tests re-homed, the
   worlds per Q1. MIGRATION. Check: scoped tests, the amplitude tests, the
   replay against the post-(vi) baseline (taken on `main` after (vi)
   lands, replacing `gate_base_summary.json`).
4. **U2, U3, U5**: the pointer formed once, the step rule and the owed
   count once, one `Border` record for the faces, the border and the
   cancel. Check: scoped; replay.
5. **O1**: the births batched. Replay; the seconds recorded.
6. **O2**: `node_event` kept on the simulation. Replay; seconds.
7. **O3**: the charges memoized. Replay; seconds.
8. **O4, O6's list, O8**: the load's scan, the free-family test, the
   gathered records freed. Replay; seconds.
9. **Optional, last, its own review**: C2, `nature_beam` split into its
   steps, no integer moved. Replay.
10. **The evidence**: VALIDATION's entry with the fifteen digests before
    (`gate_base_summary.md`) and after, the seconds per world before and
    after, the profile's ten functions before and after; docs/README's
    index rows; `python tools/check.py --full`.

Size, estimated: about 2,700 lines removed (D1 250, D2 550 with its tests
and tool, D3 80 if Q2, D4 242, D5 1,121, D6 to D8 160, U5 60, U2/U3 45,
the docstring 250) and about 350 added (the batched births, the cache,
`Border`, the VALIDATION entry); functions unified: the pointer (2 -> 1),
the step rule (3 -> 1), the owed count (2 -> 1), the charges (2 -> 1), the
border tallies (3 -> 1); speed: the gate set's wall about 97 s -> 55 s,
the runner's sum 277 s -> about 190 s (section 3.3).

---

## 6. Questions for the Boss and the owner (what (vi) decides)

- **Q1. The 1,525 `"reading": "wave"` worlds.** Under the one click the
  key is refused or read as `sum`. Refused: the lensing, Heisenberg,
  two-slit, buildup and catalog-screen worlds stop parsing and
  `test_the_example_worlds_parse_as_nature_beam_worlds` fails for each.
  Read as `sum`: the same files run a different physics than the
  register recorded (a record's sum, not the crowd's). Recommended:
  rewrite `wave` -> `sum` in the files by the one tool (D4's last job),
  mark each register entry "under `wave`, before the one click of
  2026-09-20; re-registered as ..." (record 97 already says series K
  re-registers), and keep the old digests in VALIDATION as the record's.
- **Q2. `beam`.** Does the one click keep the pairing reading (an amount
  reading with no pointer: matter's, "a detector that reads amount does
  not see a wave", design section 0), or is `sum` the only reading of a
  set? D3 follows.
- **Q3. The set's phase returned to its measured events** (the crowd's
  pointer's nearest step, `pointer_phases`, written into every member's
  `phase` under `wave` and `sum` today): kept under the one click or not?
  If not, `pointer_phases` stays only for #363's `setting_steps`.
- **Q4. C4**: the gate's `hold` reading the layer's live count: a
  sentence in note 37, or a local hold.
- **Q5. D5 and D8**: the two derivations scripts and the four
  world-pinning tests, deleted with their evidence in VALIDATION (the
  owner's rule of 2026-09-17 says so; the test owner confirms).
- **Q6. The record-format renames** of 4.3 and the key spellings of 4.2:
  a separate commit with every reader updated, or not now.

---

## 7. The entity audit (the owner's addition through the Boss, 2026-09-20: "make sure that all the known families are in entities with what is needed to define them")

### 7.1 What the definitions layer can hold today

A definition of `event-entities-v1` (`docs/ENTITY_DEFINITIONS.md`,
`world_loading.py`) carries `measured` and `detectors` only; the families
are the world's, and a definition "names its family and carries the
family's charge with its content; it declares no charge of its own". So no
entity definition in the repository defines a family, and none can: the
keys the law needs to define a family (`quantum`, `charge`, `columns`,
`lifetime`, `phase`, `phase_per_link`) have no home in a definition file.
One definitions file exists, `examples/events/detector/entities/detectors.json`
(`three_node_detector`, `serpentine_100_detector`, of the family `carrier`),
referenced by the four detector worlds. Every other series (158 worlds)
declares its families and its apparatus inline, written by the series'
`make_worlds.py`: the canonical copy of a family is a Python literal in a
generator, and a family used by two series is two literals (the table
below). The loader's structural check already admits every key of the
amplitude law in a definition's `measured` entries (`LAMP_KEYS` and
`TABLE_ENTRY_KEYS` are imported from `world.py`: `branches`, `arms`,
`turns`, `inputs`, `weights`, `turn`, `rotate`, `gate`, and `reading:
"sum"` in `detectors`), so every apparatus of the transmission world can be
authored in v1 today; only its families cannot.

### 7.2 The families the registered series declare (every world under `examples/events`, the entity files excluded)

| Family | Defined where | Keys present | Keys the row needs and lacks | Worlds that use it |
| --- | --- | --- | --- | --- |
| `light` (the photon) | inline, seven generators; four spellings: `{quantum 1}`; with `phase_per_link` `[8, 1]`, `[16, 1]`, `[8591334592, 2^30]` (the two-slit frequency) | `quantum`; `phase_per_link` where the amplitude worlds need the phase per age | none for the row; under `amplitude-v1` a source's `lamp` carries `branches`, `arms`, `turns` (present in the amplitude worlds only) | root, bell, buildup, catalog, heisenberg, lensing, amplitude |
| `e` (the electron) | inline, `bohr/make_worlds.py` | `quantum` 0, `charge` -15, `phase` true; the body's `span [1, 1, 3]`, `phase_by_momentum`, `momentum`, the world's `action` | none: the row is complete; one copy, one series | bohr (7 worlds) |
| `p` (the proton) | inline, four generators, six spellings of `charge`: `[1, 1]` (bohr, the atom's units), `4` (nucleus, weak), `[0, 1]`, `[-2, 1]`, `[2, 1]`, `[1, 2]` (coupling: probes named `p` that are not the proton) | `quantum` 0, `charge`, `phase` false; in the nucleus `held {nuclear: 1}` | no canonical copy: the charge's scale is per series (the catalog says so); the coupling's `p` and `q` are test charges wearing the proton's name | bohr, coupling, nucleus, weak |
| `n` (the neutron) | inline, nucleus and weak | `quantum` 0, `phase` false; `held {nuclear: 1}`; `become {at, into p, products [beta, nu]}` on the free neutron | none; two identical literals | nucleus, weak |
| `nuclear` (the strong family, the gluon's place) | inline, nucleus and weak; two values of the strong column (10000, 7000) | `quantum` 0, `columns {strong: {value, sign -1}}`, `lifetime` 3, `phase` false | none; the column's value per series | nucleus, weak |
| `beta` (the weak's electron, D-1) | inline, weak | `quantum` 1, `charge` -7344 (a whole charge per unit of amount) | none; a second electron beside `e` (a paid family, since it is born by `become`); the two rows say "electron" with different keys | weak |
| `nu` (the neutrino) | inline, weak | `quantum` 0; windows on the detectors' entries (`phase_window`, `phase_width`) | one family for three flavours (the catalog's gap: no change of family in flight) | weak |
| `w` (the W) | inline, weak (`w_exchange`) | `quantum` 1, `charge` -7344, `lifetime` 1, `phase` false | none | weak |
| `d`, `detector`, `counter`, `apparatus`, `screen`, `wall`, `carrier` | inline, six generators and the one definitions file | `{quantum 1}` (`d` with `phase` false): the inert paid material a detector, a wall or a counter is made of | one row, seven names; a canonical `apparatus` family is the definition to add (the names are record keys: renaming moves the digests) | weak, hubble, bell, amplitude, catalog, root, heisenberg, lensing, buildup, detector |
| `m`, `mass`, `neutron`, `probe`, `s` | inline, seven generators | `{quantum 0, charge 0, phase false}` (coupling's `m` keeps the phase circle: a second spelling) | one row, five names: the free phase-less mass; `probe` is the catalog's probe (content 1) | coupling, lensing, orbit, redshift, root, catalog, hubble, weak |
| `q` | inline, coupling | `quantum` 0, `charge` `[0, 1]`, `[-1, 2]`, `[1, 2]` | a test charge; not a thing of physics | coupling |
| `sa`, `sb` (the choosers' families, #363) | inline, bell and amplitude | `quantum` 0 | none: a free family whose rows set a window (`phase_window {reads, offset}`) | bell, amplitude |
| `mx1` .. `pz4` (24 families) | inline, hubble | `quantum` 0 | one thing (a thrown mass) as 24 families, because the set's `record` is per family and the tool separates the sources by it; the clicks carry `number`, so one family with 24 measured events would do with the tool reading `number` | hubble |

Thirteen rows of physics (photon, electron, proton, neutron, the strong
family, the weak's electron, the neutrino, the W, the inert material, the
mass, a test charge, a chooser, a thrown source) are spread over 51 family
names in the register; none has a definition file; every one is complete
in the law's keys where it is used.

### 7.3 The catalog's rows against the worlds

| Catalog row | A world places it | The definition to add in phase 2 | The gap (a key the law lacks) |
| --- | --- | --- | --- |
| photon | yes (seven series) | `light` | none |
| electron | yes (bohr `e`; weak `beta`) | `e`, and `beta` named as the electron born by `become` | none |
| muon, tau | no world | `mu`, `tau`: `quantum` 0, `charge` `[n_e, 207 d_e]`, `[n_e, 3477 d_e]`, `become {at, into e-family, products}` (the keys exist since `weak-v1`) | none for a definition; the decay's products' content the physicist's |
| the three neutrinos | one family `nu` | `nu` (one) | oscillation (no change of family in flight): the catalog's gap |
| quarks | none | none | colour (the catalog's gap) |
| W | `weak/w_exchange` (`w`) | `w` | none |
| Z | none by the design | none | none by design |
| gluon | `nuclear`'s rays | `nuclear` | colour |
| Higgs, graviton | none / the column | none | the catalog's gap / nothing needed |
| proton, neutron, deuteron, alpha, light nuclei | nucleus, weak, bohr | `p`, `n`, `nuclear`; the composites as apparatus definitions (`deuteron`: two measured entries with `held`; `alpha`: the square) | none |
| hydrogen | bohr | `hydrogen` (the proton's fan and the electron body) | none |
| helium, a molecule | none | none until the bound nucleus | the catalog's |
| the sun, a planet, a neutron star, a lamp, a laser, a mirror, a wall, a slit, a screen, a clock, a probe | catalog and the series | each an apparatus definition in v1 (`measured` + `detectors`) | none |
| a moon, a white dwarf, a comet, dark matter, a galaxy | none / hubble | `moon`, `white_dwarf`, `dark_matter` as definitions with the catalog's numbers; a comet's tail stays the gap | the comet's tail |
| a black hole | none | none | the catalog's gap |

### 7.4 The definitions to add in phase 2 (definitions only; no law change)

1. **A home for a family in a definition.** Two forms, the Boss decides:
   (a) without a loader change, `examples/events/entities/families.json`,
   one row per physics family in the atom's units (`light`, `e`, `p`,
   `n`, `nuclear`, `nu`, `w`, `beta`, `apparatus`, `mass`, `probe`) that
   every `make_worlds.py` reads and copies into its worlds, with a hygiene
   test that a world's family block equals the file's row by name (the
   worlds keep carrying the data: the law's parser is unchanged); (b) the
   host format `event-entities-v2` with an optional `families` list per
   definition, merged into the world by name and refused on a conflicting
   key (a change of `world_loading.py` and its contract, host code, no
   physics). (b) is the real answer to "in entities with what is needed";
   (a) is the one this pull request can do alone.
2. **`examples/events/entities/apparatus.json`** (v1, works today): the
   lamp, the laser (`phase_window`), the mirror (`rerelease` on one
   direction), the wall, the slit (`rerelease` on a fan), the screen as one
   set and as pixels, the probe, the clock (a `span` body), the pair
   source (`lamp {rate [1, 1], directions [two arms], arms 2, branches
   [[0, 1], [3, 1]]}`), the GHZ source (three arms), the Mach-Zehnder
   splitter (`rerelease {inputs, weights, turns}`), the label rotation
   (`rotate {setting, bit, turn}`), the CNOT gate (`gate {kind, hold,
   parties}`), the counter pair (`+`/`-` sets reading `sum` with
   `phase_window` s and `turn` t), the chooser (a free family's source and
   the entry `phase_window {reads, offset}`): every one already declared
   inline by a registered world, moved to one copy each; the worlds of the
   catalog, the bell and the amplitude series rewritten by their
   generators to reference them (the expanded world is byte-identical to
   the inline one by the loader's contract, so the digests stand).
3. **The composites as definitions:** `deuteron`, `alpha`, `hydrogen`,
   `neutron_star`, `sun` (the mass and the lamp), each two to eight
   measured entries.
4. **The rows no world places, as definitions with the catalog's
   numbers:** `mu`, `tau` (with `become` at the clock), `moon`,
   `white_dwarf`, `dark_matter`; each gets a catalog world when the owner
   asks, not a registered run.
5. **Names:** one `apparatus` for the seven inert names and one `mass` for
   the five free phase-less names is a rename of record keys (the family
   name is on every line of `events.jsonl`): listed with 4.2, not in the
   bit-exact commits.

### 7.5 The transmission world (the owner's next experiment: a detector that generates amplitudes on the GameBoard and a detector that receives on the other side, on generic runs)

What the experimenter needs from definitions alone, every key existing in
the law today:

- **The source that births records with a declared label as its bit:** a
  measured event of the paid family `light` with `lamp {rate [1, 1],
  directions [the arm(s)], arms 1 or 2, branches [[bit, 1]]}`: `branches
  [[1, 1]]` births a record whose one joint label is 1 (the message bit),
  `[[0, 1]]` the bit 0, `[[0, 1], [3, 1]]` the entangled pair on two arms;
  `turns` per direction for a reflection's quarter turn; the birth phase u
  is the lamp's clock (`K`, `phase`), so a `phase_window` on the lamp
  selects the u range of the births. Under (vi) the record is every
  lamp's birth (no key); before it, the world declares `amplitude: true`.
- **The GameBoard:** the world's `shape`, `N` (64 or larger for finer
  rungs), `K`, `age_bound`; free space between; optionally mirrors
  (`rerelease` on one direction) and a splitter (`rerelease {inputs,
  weights, turns}`) on the path.
- **The receiving detector set reading `sum` with a rotation setting:**
  measured events of the inert family (`counter`, content 1, `fixed`) with
  the entry `light: {phase_window: s, turn: t}` (the rotation `U_s` on the
  label's bit; `turn` the phase on label 1) and `detectors [{name, positions
  [the set's Nodes], reading: "sum"}]`; two sets, `plus` and `minus`, when
  the click's channel is the reading (the bell worlds' form), one set when
  the click's label is (a `read` entry on a `sum` set is the which-path
  factor). A set of several Nodes is one cell (record 96); the gather line
  names the set, the channel, the label, u and the weight: the received
  bit is `chosen[0][2]` of the gather, the record's `u` its key.
- **The definitions file** of 7.4 (2) carries all of it as `pair_source`,
  `bit_source`, `mirror`, `splitter`, `counter_pair`, `counter_set`; the
  world that places them declares the two families (`light`, `counter`)
  until 7.4 (1) lands, and the tool `tools/amplitude_path.py` replays the
  received list from `events.jsonl`. No gap: nothing the transmission
  world needs waits on a law change.

---

## 8. Is the engine generic, and does it apply no formula? (the owner, 2026-09-20: "make sure the engine is fully generic and applies no formulas at all")

### 8.1 The dynamic proof: the rename probe (`rename_probe.py`, `rename_probe.txt`)

Twenty-two worlds of thirteen series (the gate set's kinds, the catalog,
the W world, seven amplitude worlds), every family, detector and column
renamed to keyword-like tokens (`measure`, `__proto__`, `rule`, `wave`,
`sum`, `0`, `face:+x `, `read`, `constructor`, `pass`, `rerelease`, `beam`,
`K`, `lamp`, `gate`, `mass`, `gravity`, ...), run, and compared with the
names mapped back: `events.jsonl`, `state.json` and `run.json` identical on
all twenty-two (912,000 record lines in all). A name reaches the engine
only as a key into the world's own tables; nothing reads it. This repeats
records 73, 90 and 96 (311, 70 and 100 comparisons with permutations as
well) on the union tree.

### 8.2 The static proof: what the engine compares and what it holds

- **Branches on strings** (`grep` over `events/*.py`): the rules
  (`read`, `measure`, `rerelease`, `pass`, `become`), the reading
  components (`scalar`, `outside`, `here`, `vector`, `tensor`, `age`), the
  readings (`wave`, `beam`, `sum`), the layer's kinds (`set`, `face`,
  `border`), the law value and the refused old keys. All are schema words
  of the world file, none a physical name. The two physical nouns in the
  source are the names of the two built-in columns, `gravity` and
  `charge` (`world.py` 448 and 449): names of columns, never compared
  against a family.
- **No formula of nature.** No field law, no 1 / r or 1 / r^2, no
  Coulomb constant, no mass formula, no cosine of a setting at run time
  (the tables are read), no floating point in the physical path. The
  push is one signed inner product of a moment of arrivals with the
  reader's declared columns (`push_form`); the clock, the release, the
  count, the step, the columns and the lifetime are all one primitive,
  `by_clock` (the whole part off an age); the flight and the collision
  are tables generated once from the direction set; the click's reading
  is a moment on the circle's tables; the gather is a ladder of integer
  rungs. Every physical selection (which family is matter, which is
  light, who reads whom and how, the charges, the columns, the ranges,
  the windows, the branches) is data of the world file.

### 8.3 The rules the engine does hold, each with its fixed form

"No formula at all" is not literally true and cannot be: the law itself
is arithmetic. What the engine holds is the Beam Law's own rules, each
decided by the owner and recorded, with fixed constants a world cannot
change. The honest list, with where each lives and what fixes it:

| Rule | Where | Fixed form | Fixed by | A world can |
| --- | --- | --- | --- | --- |
| the speed and the label scale | `flight_table`, `unit_label`, `Q = 64` | `T_d = isqrt(3 |v|^2 Q^2)`, u_d the nearest integer vector to `Q v / |v|` | BEAM_LAW 2 and 3 | choose the directions; not Q |
| the digital line and its period | `_bresenham`, `flight_table` | the axis furthest behind, lowest first | BEAM_LAW 3 | nothing |
| the collision | `collision_table`, `collide` | the cyclic shift within a class of the 3^8 slot states | BEAM_LAW 4, note 18 | nothing (acts at every free Node) |
| every rate off a clock | `by_clock`, `by_clock_rows`, `ages_at_key` | `((age + 1) n) // d - (age n) // d` | record 64 (2) | the pairs n / d |
| the turn and the cost of a release | `_frame_all`, step 5 | `s = by_clock(age, M n, d)`; a unit costs `h s` (E = h f) | records 10 and 64 | K, the quantum h |
| the release and the suspension | step 5, `count_owed` | `by_clock(age, M n, d)`, `by_clock(age, k n, d)` | BEAM_LAW 3 | the pairs |
| the step of a body | `step_axis`, `_move` | one Link per `(Q S M + p) / p` self-creations | D1 (record 19 of 09-19) | `width` S, the momentum |
| the push | `push_form` | `sum_c eps_c sign(V E_c n_c) by_clock(age, |V E_c n_c|, D_c d_c)`; a paid ray pushes by its label (kappa = 1) | records 27 and 35 | the columns' values and signs; not gravity's `(1, 1)`, sign -1, nor the charge column's sign +1, nor kappa = 1 for light |
| the default table | `default_rule`, `default_reads` | a free family `read`, a paid one `measure`; `vector` on `read`, `scalar` otherwise | record 18 (09-19) | override any entry |
| the contact | `_contact` | `measure` hands the axis component, `rerelease` returns twice it | record 34 and 73 | the occupant's rule |
| the window | `window_admits`, `default_width` | `(d + w // 2) mod N < w`, w = N / 2 by default | record 04 (09-19), note 36 | s and w |
| the pointer and its square | `coherent_pointer`, `pointer_units`, `AMPLITUDE_SCALE = 32`, the 1/256 tables | `X = sum 32 a C[p]`; the unit `2^26`; the nearest step | records 64 (1) and 40 | N |
| the meeting | `meeting.py` | `adv = (|t| + Q/2) // Q`, `k = (phase + adv) // N`; the arc sectors about `t = sum kappa V` | record 67, note 35 | the key `meeting`; the columns (kappa) |
| the turn by momentum | `engine._move` | `by_clock(k, |p| N, h)`, k the Links stepped | record 09-20 on Bohr (`bohr-v1`) | `action` h, `phase_by_momentum` |
| the transformation | `transform` | R = sum amount x content paid from the own family; charges balanced at load | `weak-v1`, note 36 | `become`'s keys |
| the split and its norm | step 5 | `(w a_i, m A, p + t_i)`, `A = sum a_i^2` | design 2.1 | the weights, the turns |
| the label rotation | `rotate_rows`, `Layer.rotation`, `half_angle` | `U_s = [[C', S' v(t)], [-S', C' v(t)]]` on the tables of 2N | design 2.2 | s, t, the bit |
| the gate | `apply_gate`, `Layer.join` | the CNOT permutation `(l_c, l_t) -> (l_c, l_t xor l_c)`, the only kind (`GATE_KINDS = ("cnot",)`) | design 10 | `hold`, `parties`; not the permutation |
| the merge's cancel | `NatureBeamStore.merge` | rows of one record at phases N / 2 apart subtract | design 2.3 | nothing |
| the ladder | `rungs`, `choose`, `node_choice` | `b_k = (2 N C_k + Total) // (2 Total)` | record 86 (a) | N |
| the record's identity | `record_identity` | `number x 2^32 + ordinal` | (i) | nothing |

### 8.4 The verdict, and the three places where a fixed rule could be data

The engine is generic in the sense the owner asked for on 2026-09-19 and
2026-09-20 ("no scenario-name conditions in a general law", "the engine
does not know which family is which"): no physical name is read, no law
of nature is written in it, every physical choice is a key. It is not
formula-free: it is the Beam Law's twenty-one rules of integer arithmetic
above, every one recorded as the owner's decision or the design's, with
the constants Q = 64, 32, 1/256 and N.

Three of the fixed forms are choices that could become keys of the world
without any other change of the law, and are the ones to decide on:

1. **Gravity is built in.** Every family carries the column `(1, 1)` with
   the sign minus and cannot decline it (`built_in_columns`); the charge
   column's sign +1 is fixed too, and a paid ray's push is its label with
   no column. A world cannot place a family that gravitates otherwise or
   not at all. The owner's decision of record 27 ("gravity the column
   every family has") is the reason; if the owner wants it as data,
   `gravity` becomes a declarable column with a default, one commit, and
   every registered world byte-identical by the default.
2. **The gate is one permutation.** `cnot` is the one `kind`; a declared
   permutation table of joint labels (`{"kind": "table", "map": [[from,
   to], ...]}`) would make the gate data as the split's weights are.
3. **The turn by momentum is a formula in the frame.** `floor(k |p| N /
   h)` lives in `engine._move`, selected by `action`; it is a hypothesis
   (`bohr-v1`) beside the law, and the one rule not spelled through a
   table or the push. It stays a formula unless the owner moves it to a
   table entry of the body.

Everything else that is fixed is the law's identity (the speed, the
line, the collision, the clock, the window, the pointer, the ladder), and
making it data would be a change of the law, not of the engine.
