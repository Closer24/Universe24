# Physics-rule review: amplitude-v1 stage (vii) step 4, "the one click" (amplitude-impl 02448fa6)

Read-only, 2026-09-20. Worktree /home/user/Universe24/.claude/worktrees/agent-ada5d79bd22bb2f56 at 02448fa6
(6fe0b9e3 merges main d768f831; origin/main is 56a258f8 with doppler-v1, not merged). Diff read:
`git diff d768f831...02448fa6` (86 files, +1706/-672). Run: 4 tests of tests/test_amplitude_click.py
(rate, multiplicities, key deleted, parse), passed in 1.5 s; no long run, no tools/check.py.
The implementer reports `check.py --full` exit 0 (805 passed, 1 xfailed); not re-run here.

## 1. The one click as built (against DESIGN 3.3, 5, 6 and the owner's order)

- NOTE (conforms). The ladder is the design's: `rungs` (src/event_universe/events/amplitude.py:185-206)
  computes b_k = (2 N C_k + T) // (2 T) over the offers scaled to the common denominator, b_K = N by
  identity; `choose` (:208-214) takes the first k with u < b_k; the cells are the offers in set order
  and arm/label order (`cells`, :583-613: sorted by `set_index`, the declared tie of records 96/105).
  The gather line (:700-735) carries chosen, node, weight, total, T, before/after: DESIGN 5's row.
- NOTE (conforms). u is the record's own field: a birth writes `u = (entry.births - 1) % modulus`
  (nature_beam.py, the birth hunk at ~:3480-3520) and every lattice rule reads the path phase
  (`read_phase = path[met]`, the coherent pointer on `path[met]`, nature_beam.py ~:2536-2545); the
  layer's offers read the running phase, u enters at `choose` alone. The lattice never reads the layer.
- NOTE (conforms). The push by share: `share_of` (nature_beam.py:811-820) is |label| x amount // m
  with the sign restored, bounded by |label| since amount^2 <= m; the recoil of a paid re-creation is
  the born rows' shares (~:3573-3590); the rest goes to the `remainder` books line.
- NOTE (design intent). Every lamp's row is a record: `for _ in range(count)` with
  `count = min(count, held // (cost x quanta))` births `rate` records per self-creation, the crowd
  branch deleted. DESIGN section 0 wrote the record form "under the key"; the owner's order
  (docs/LOG_2026-09-20.md:383) says "then the record form becomes the only click, the key and the
  crowd-threshold reading are deleted". The build is that order. The layer stays the apparatus's
  (one object per frame, reached through the apparatus events), the GameBoard computes every future,
  the click is one reading per record: the four principles named in the assignment hold.
- NOTE. A lamp's `phase_window` now gates the release by the clock's phase while the row carries u
  (MIGRATION (vii-4) names it). Consistent with u unread by the lattice; no test pins a windowed lamp
  under the record form beyond the re-pinned ones.

## 2. LOCALITY-1 end to end

- NOTE (holds on the Node). A Node holds rows only; `record`, `branch`, `multiplicity`, `birth` are
  row fields of the store; the `wave` set's pointer is this interval's arrivals with no memory
  (nature_beam.py ~:2521 "No memory between intervals"); the threshold is the amount sum. Fixed
  local work and storage for fixed K per Node is kept; the record's accumulation happens in the
  layer at apparatus events, as DESIGN 3.2 and 5 state.
- SHOULD-FIX (host cost, a defect, not the design's cost). `Layer.complete`
  (amplitude.py:650-737) marks `found.gathered = True` and KEEPS the LiveRecord with all its offers
  (each Offer's `residuals`, `content` and `momentum` dicts per Node) in `self.records` for the whole
  run; the only deletion in the module is the gate's join (:481). It also iterates
  `for identity in sorted(self.records)` on every call, so the host's work per interval grows with
  every record ever born and the memory with every record's offers. DESIGN 12 costs the layer's table
  "live until completion". w27_beam's 7.09 GB at interval 211 and "seconds per interval" are this
  retention, not the law. Fix: at completion drop the offers (keep the identity in a `gathered` set
  for the lazy deletion of rows at their next set; the gather is already in `self.gathers`), and
  visit only records whose `live` reached 0; `open_records`/`report` (:739-779) then count from the
  gathered set. Until then the three build-up worlds and w27_beam cannot be re-read (finding 5).
- NOTE. The host cost is reported separately (EXPERIMENTS.md:1703 and MIGRATION (vii-4)), as
  required; the per-Node cost is unchanged.

## 3. Integer discipline

- NOTE (holds). The share is bounded by the label; the rungs use host integers exactly; two
  multiplicities at one offer add only at a square ratio, refused by name otherwise ((vii-1),
  `common_denominator`, amplitude.py:167). The `remainder` line closes by recount on the small world
  of test (g): 48 x 32 = 1536 (mass), 55 x 32 = 1760 (splitter, both axes), remainder
  x = 1536 - 1760 = -224, y = -1760: every integer equal to the pinned expectation.
- NOTE (a bound moved from load to run). The load-time ceiling (world.py:2240-2258) no longer
  multiplies a plain `rerelease`'s factor; the split's own check refuses the multiplicity when formed
  (nature_beam.py:3315 "bounded before it is formed and refused naming the Node"). Correct in law
  (a path's count of re-emissions is not known at load), but a world may now run long before it is
  refused. Acceptable; say it in ENGINE if not already.
- NOTE. A lamp is refused with N below 4 (world.py:2567-2571, the quarter turn of a reflection);
  a world that declares the deleted key is refused by name (world.py, `DELETED_AMPLITUDE_KEY`).

## 4. The stop rule (records 96 at LOG:383, 101 at LOG:407, 114 at LOG:457, 116 at LOG:465, 119 at LOG:477)

- BLOCKING BY THE RULE AS WRITTEN (an owner's decision, not a code defect). The order at LOG:383:
  "only the worlds whose digest changes (expected the crowd-threshold series) are re-run and
  re-pinned ... if any world outside those series changes, the stage stops and the key stays,
  reported." Five lamp worlds outside those series changed (catalog/lamp_mirror_screen,
  catalog/sun_planet, lensing/heavy_meeting, lensing/mass_meeting, two_slits). Under the letter the
  key stays and the stage stops; the implementer's reading "every lamp world" is the intent's, not
  the letter's, and record 116 (LOG:465) sent step 4 "under the stop rule of stage (vi)" unchanged.
- Under the intent: the same rule stopped stage (vi) once (record 101, LOG:407) on these same
  worlds; the owner then ordered (vii-1) to (vii-3) precisely so that they could run under the
  record form, and record 114 (LOG:457) reported that series K re-registers under the one click
  "as record 97 said", leaving it "for the physicist, not decided". The changed set is exactly the
  lamp worlds (7 of 15, 7 of 17), no lamp-free world moved (8 of 8, 10 of 10 byte-identical), and
  the cause is the record form itself (u the ordinal, the path phase read by the lattice, the
  crowd's pointer gate deleted), not a leak. The evidence supports the intent; it does not replace
  the owner's word.
- The key-kept alternative costs: two click forms in one engine (the `world.amplitude` branches
  deleted here, ~170 lines of world.py and ~50 of nature_beam.py), the crowd's pointer gate kept
  beside the ladder, series K carrying two lattices (record 114), and the identity `amplitude-v1`
  a key and not a law; it buys byte-identity of the seven lamp worlds' crowd readings that the
  design's section 0 already rejects as a reading of the world.
- Recommendation for the owner (three lines):
  1. Say in one line whether "every lamp is a record" is the law; the letter of LOG:383 stops here.
  2. If yes, the deletion is admissible: the seven lamp worlds re-register by their dated lines and
     Highlights 5.4 gets that one line; if no, the key returns and steps 1 to 3 stay as built.
  3. Either way, land the layer's release of gathered offers (finding 2) before w27 is re-read.

## 5. The re-run series (EXPERIMENTS.md dated lines)

- A1 two_slits (EXPERIMENTS.md:408): SHOULD-FIX the reading, the change itself expected. The line
  reads the rows' counts per pixel (91 per record: the GameBoard's absorptions), not the world's
  list of gathers; under the record form the fringe is the ladder's over each record's offers at
  the pixels its two paths reach (series L2, slits_low). The crowd form's 0.85 at the period 8 was
  interference BETWEEN records through the pointer gate, the reading DESIGN section 0 rejects; its
  fall to 0.80/0.12/0.35 at 16/8/4 is the per-Link path phase without the clock's emission lag, not
  a lost interference of the law. The verdict must be re-read from two_slits's gathers (not
  computed in the line): say so, or compute it.
- The old A2 phase form (EXPERIMENTS.md:1018): expected. The pair lamp's rows carry the path phase
  0 and the counters' windows read the path phase, so every pair lands in one cell (E = +-1, S = 2).
  The crowd's phase form was an apparatus reading the clock phase on the row, which step 2 took off
  the lattice by design. It is not a second apparatus of the same law; it reads nothing now. The
  pair is L3/L5 (S = 176/64, 2896/1024, 11584/4096, unchanged). The crowd numbers are history; the
  verdict to re-read is only whether the ten `bell/` worlds stay registered.
- A10 build-up (EXPERIMENTS.md:1832): expected. 1.9985 / 0.9994 = 2 / 1 times the tables' norm error
  (C^2 + S^2 = 65536 +- 237, 0.36 %) on rows one u-step apart. The three w27 worlds are not re-run
  (finding 2): the verdict cannot be re-read until the cost is fixed.
- K (EXPERIMENTS.md:2767): stands. The table is the step-2 table (25.871 / 24.301 / 21.854 / 19.101),
  unchanged at steps 3 and 4; heavy_meeting and mass_meeting are now record worlds, so record 114's
  "two lattices" resolves to one: the physicist re-reads K's registered verdict on this table.
- A2 with the choosers (EXPERIMENTS.md:2841): as the old A2; L3's bell_choosers (156/64) stands.
- Must be re-read by the physicist: A1 (from the gathers), A10 and the w-series widths (after the
  cost fix), K's registered verdict on the step-2 table. Stand: L1 to L6, the K table, the pair's S.

## 6. Deletions, history, marks, language

- NOTE (holds). MIGRATION (vii-4) lists every deleted path: the key and its parsing, the "needs the
  key" refusals, the crowd form of a lamp, the `wave` pointer gate (note 32), the ceiling's
  rerelease factor, the layer on every world, the 46 worlds regenerated (each diff is the one key
  line; expectations unchanged by the implementer's report, consistent with the 2-line diffs).
  The old numbers are kept as dated history (six dated lines; no record rewritten). Marks
  "re-run under the one click (stage (vii) step 4); the verdict to be re-read" in the re-pinned tests
  (tests diff lines 840-1336) and in TEST_EXPECTATIONS.md:723, :823, :1830, :1839, :2091;
  BEAM_LAW note 37 (x) and HYPOTHESES 22 consistent with MIGRATION. No HIGHLIGHTS edit. No
  non-Latin script in the additions; English throughout. No board/grid/lattice/Site noun in the
  added lines of src, docs and tests (grep of the additions: 0).

## 7. Verdict and merge order

MERGEABLE AFTER: (a) the owner's one-line decision on the stop rule (finding 4; blocking by the
rule's letter, the evidence for the intent complete), (b) the layer's release of gathered records'
offers and the per-interval visit of live-zero records only (finding 2), (c) the A1 line reading
the gathers or saying it does not (finding 5). Merge origin/main 56a258f8 (doppler-v1) into the
branch first: `git merge-tree` reports content conflicts in docs/BEAM_LAW.md (note 38 beside note
37 (x)), docs/ENGINE.md, src/event_universe/events/run.py (run.json keys: doppler's beside the
deleted `amplitude`) and src/event_universe/events/world.py (WORLD_KEYS and the parser);
nature_beam.py, engine.py, measured.py, MIGRATION and TEST_EXPECTATIONS auto-merge, which does not
prove the semantics: after the merge, check that doppler's weighted flow on the arrivals reads a
record row's share (finding 1) and not its whole label, re-run test (g) and doppler's fixed-body
bit-identity, then tools/check.py --full on the merged head.
