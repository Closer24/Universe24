# H-Confirm-Build-15: the interval's fold, d9d7914ff (toys-5)

CONFIRMED d9d7914ff. No departure. Every record equal to the parent's in every key but the milliseconds; the fold's acts two kinds alone; every check exit 0; no test grown by the fold.

Worktree /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf15 at d9d7914ff (detached); the parent engine from git archive a796f299c src under tools/derivations/open_items/H-Confirm-Build-15/parent/src. Python 3.14 (venv314), every run at nice 19 with TMPDIR=/dev/shm/tmp. Read 00:46 to 00:53 UTC. No run cut short.

Ancestry, read first: the commit's own parent is 4180d66c2 (Build CS5-S2, the cycle lay `wave`), not a796f299c; a796f299c is the grandparent. git show d9d7914ff --stat: 2 files, src/event_universe/interval.py (+41 -71 of its 112 changed lines) and tests/test_the_node.py (1 line, walled_act renamed readings). The diff of src against a796f299c carries CS5-S2's lines besides (node.py 2, rows.py 4, seed.py 11, wave.py 89 new); of tests/ and tools/ against a796f299c, CS5-S2's test (39 lines in test_the_board.py), its two world files and its ROOM entry of 45 in tools/tests_shape.py. The fold itself moves no line of tests but the one rename.

## 1. The records (the build's runs written to /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/records/d9d7914ff/; the parent's read from /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/records/a796f299c/)

Runs: python -m event_universe.run tests/worlds/world_<w>.json <out> back N for the hole, the chiral, the bodies, the pair_3 and the universe (the world files' own intervals 60, 60, 300, 400, 400); the plasma_3 through run_record.py at intervals 170 (its world file says 400; the parent's record stands at 170) back 10. Compared with compare.py: every top-level key (G, T, counts, cube, den, gamma, gapped, intervals, log, nodes, planes, rows, run_back, turns, universe, world), the rows' milliseconds alone stripped; the files parsed with a float refused (none met).

| world | intervals | back | build against parent | log entries | counts (births / body_clicks / turns / laid_back) | run back |
|---|---|---|---|---|---|---|
| world_hole | 60 | 20 | equal in every key | 21050 | 24 / 1124 / 570 / 0 | 20 of 20 |
| world_chiral | 60 | 20 | equal in every key | 26140 | 19 / 3052 / 659 / 0 | 20 of 20 |
| world_bodies | 300 | 20 | equal in every key | 15782 | 0 / 1973 / 4229 / 0 | 20 of 20 |
| world_pair_3 | 400 | 10 | equal in every key | 3646 | 0 / 297 / 54 / 297 | 10 of 10 |
| world_universe | 400 | 10 | equal in every key | 19752 | 0 / 1875 / 250 / 1875 | 10 of 10 |
| world_plasma_3 | 170 | 10 | equal in every key | 13205 | 0 / 162 / 27 / 162 | 10 of 10 |

No apart interval, no apart field. The three committed records (examples/records/hole.json, chiral.json, bodies.json) against the build's own runs: equal in every key but the milliseconds (compare_committed.txt). Since the parent records are a796f299c's engine's and the build carries CS5-S2's src besides the fold, CS5-S2 moved no number on these six either.

A first run of the plasma_3 went at the file's 400 intervals (the CLI reads the file's count); kept as logs/world_plasma_3_400_misrun.json, body_clicks 405, run back 10 of 10; replaced by the 170 run.

## 2. The fold

interval.py: 305 lines to 277; "def " 17 to 13; docstring lines (ast, module, class and functions) 18 to 14. Imports unchanged.

The acts after the fold, in run's order: Interval.__init__ (backward: close.click at -1 and the swap's exchange undone), readings, [direction -1: lays], kick, division, [direction -1: interval counted down, return], swap, close. The methods of Interval: __init__, at, lines, ends, mean_wall(line), readings, kick, division, lays, swap, close; the module's laid_on and run. node.py's one caller is interval.run (node.py line 334); run.py calls none directly.

The former acts mapped: readings + walled_act + forces -> readings (the walled row's carried division kept among the readings, as the commit says); unwrite -> lays at -1 (called before kick, the same place); kicks -> kick; carrier_act + divisions -> division (w_div computed inside division from out[k][0] where carrier_act set self.w_div); writes -> lays at +1 (called inside division after node.set_rows); set_rows (formerly in run) -> inside division; rest -> the restore at the end of division; close -> swap (node.swap, formerly the first line of effect inside close) + close. mean_wall took no argument and read the carrier's lines as the rows hold them; it takes the line it reads, called with self.carrier.lines[0] in kick (the rows' own), self.out[k][0] in division (the act's end) and node.row(CARRIER).lines[0] in lays (after set_rows, the same out line forward; backward the rows as held). The one rearrangement: the former order was divisions, writes on self.out's lines, set_rows, rest; the fold's is set_rows, lays on node.emitter().lines[0] and node.row(POTENTIAL).lines, restore; after set_rows those are the same Line objects, and the six records confirm it moves no integer.

Two kinds of act: every site in interval.py that writes a level or a remainder is a carried division or a lay: line 109 node.act (the walled row, Rule3), line 176 carried_division (the charge at the kick), line 200 node.carried (the carrier), line 213 division_forward with Line(...) at 215/217 (the riding lines), lines 239 and 244 node.write (the lays, one carried division each at the write wall, node.py 208-209). node.restore (lines 220, 231) copies held lines back at the still Nodes, no arithmetic. No other site writes a level: grep of ".now = / .before = / .rem = / .wr = / Line(" over src lists interval.py lines 176, 215, 217 alone, the rest in node.py (act, write, restore, exchange), rows.py, gram.py, seed.py and wave.py (the lays' making), all unchanged by the fold.

The reach: the Node method calls are the same set as the parent's (act, all_lines, arrivals, carried, click, emitter, exchange, link_factors, records, restore, row, rows, rule_of, set_rows, swap, write), node.write 4 to 2 (the one lays method in both directions), node.row 2 to 4 and node.emitter 1 to 2 (lays reads the rows through the Node after set_rows). Nothing new reads beyond the Node and its six Links. Integer literals beyond 0, 1, -1 (ast, literals.py, parent src against build src): interval.py 5 to 5, no file up (wave.py is CS5-S2's, 6, new against a796f299c, absent in the parent). Floats: 0 in every file; no "/" division outside docstrings in interval.py. No family's name in interval.py (grep electron, photon, quark, neutrino, proton, muon, boson, lepton, hadron, gluon: 0). No branch on a row's kind: no isinstance, no "shape ==" test; the row-role tests (r is self.potential, r in self.records, r.wall is None, r is not self.carrier, r.pair) number 9 in both files, unchanged.

## 3. The checks (exit codes; logs under tools/derivations/open_items/H-Confirm-Build-15/logs/)

ruff check .: "All checks passed!", exit 0. ruff format --check .: "186 files already formatted", exit 0. mypy: "Success: no issues found in 30 source files", exit 0. tools/record_code_shape.py: "the shape of the code holds against the merge base", exit 0. tools/engine_gates.py: "the engine gates hold against the merge base", exit 0. tools/tests_shape.py with CHECK_BASE=a796f299c: "the shape of tests/ holds against the merge base", exit 0 (the 39-line growth is CS5-S2's test under its ROOM entry of 45, not the fold's); with CHECK_BASE=4180d66c2 (the commit's own parent): the same line, exit 0. tools/documents_gates.py: "the documents' six gates hold", exit 0.

## 4. The tests

git diff a796f299c d9d7914ff --stat -- tests/ tools/: tests/test_the_board.py +39, tests/test_the_node.py +3 -2, tests/worlds/universe_ga2.json +1, tests/worlds/world_ga2.json +1, tools/tests_shape.py +4; 48 insertions, 2 deletions, all of CS5-S2 (4180d66c2) but one: the fold's own diff against 4180d66c2 is tests/test_the_node.py 1 line, interval.walled_act() to interval.readings() in test_the_unit_the_emitter_and_the_identity_turn_are_values_of_the_pair_un, the assertion after it unchanged (links_at sorted [0, 1], a -1 among the frames). No count moved, no assertion loosened by the fold.

## 5. Missing

Nothing missing of what the commit names. Not measured: the suite (not asked); the pair, the universe and the plasma_3 "at 60 and after 10 back with the same state hashes" as the commit phrases it, measured instead at the cache's counts 400, 400 and 170 with 10 back, exact 10 of 10 each.

Files: /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf15/tools/derivations/open_items/H-Confirm-Build-15/ (run_record.py, compare.py, compare_six.txt, compare_committed.txt, literals.py, literals.txt, src_diff.txt, logs/, parent/src); the records at /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/records/d9d7914ff/ (six files).
