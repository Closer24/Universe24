# H-Confirm-Build-12: the cold read of David's build of CS4-S2 at toys-5 e1209f752 (parent 99a9ee860, PL-S1)

**CONFIRMED e1209f752.** No departure in the act. One ratchet's line (section 6) and three remarks (section 7).

Worktree $S/hands/vf12 (S = /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad), detached at e1209f752; nothing edited under src/ or tests/ (`git status --short`: the hand's folder alone, untracked). Every file of this hand under $S/hands/vf12/tools/derivations/open_items/H-Confirm-Build-12/ (the parent's engine unpacked by `git archive 99a9ee860 src tests` under parent/; the records above 1.5 MB removed after their reading, the logs and the readers' texts kept). Python /home/user/Universe24/venv314/bin/python, TMPDIR=/dev/shm/tmp, nice 19 on every run. Integers only; the barred words none in this text and none in the diff's added lines (grep 0).

## 1. The suite and the checks (checks/*.log, pytest.log)

| check | command | result | exit |
|---|---|---|---|
| the suite | `nice -n 19 $PY -m pytest -q tests/ --durations=0` | **75 passed** in 115.80 s; the longest test 8.54 s (the fourth part of the 48), every test under 15 s; David's test 3.81 s, the re-pinned SL-S2 test 3.08 s; failures none | 0 |
| engine gates | `$PY tools/engine_gates.py` | "the engine gates hold against the merge base" | 0 |
| the code's shape | `$PY tools/record_code_shape.py` | "the shape of the code holds against the merge base" | 0 |
| the tests' shape | `$PY tools/tests_shape.py` | **"tests/ grew from 1606 to 1696 lines; offset the new tests by deletions in the same pull request"** (section 6) | 1 |
| the documents | `$PY tools/documents_gates.py` | "the documents' six gates hold" | 0 |
| ruff | `ruff check .` | "All checks passed!" | 0 |
| ruff format | `ruff format --check .` | "185 files already formatted" | 0 |
| mypy | `$PY -m mypy` | "Success: no issues found in 29 source files" | 0 |

## 2. The act is the letter (the diff of src against 99a9ee860: take.py, close.py, bodies.py, read whole)

(a) **One rule, one function.** `take.fall_of(node, at, walls, r, row)` takes the row, computes `gaps = [now^2 - before^2 for line in row.lines]`, `k = gaps.index(max(gaps))` (the first line where equal) and reads the fall on `row.lines[k]`, returning `(levels, fall, k)`; `take.take_at` reads `k` from fall_of, lays `toward * levels` by `lay(node, taken, at, toward * levels, line=k)` and returns `(levels, fall, now, before, k)`; the birth (close.births through take_at), the merger's two ends (close.merger_take: fall_of at both ends, then take_at at each) and the body's click (bodies.bodies through take_at) go through this one function. `grep -n "lines\[0\]" src/event_universe/*.py`: 20 hits, none a take: bodies.py:39 the plane's re line read for the beat's zero crossing (CK-S1's reading), bodies.py:157 the sign row's level logged on the credit, board.py:85 a count of lines, interval.py 79 / 90 / 92 / 93 / 158, node.py 112 / 116 / 307, readings.py 33, seed.py 203 / 317 the carrier's, the walled row's or the potential row's own time line, run.py 58 / 60 / 85 / 101 / 106 the reader's rows (the gap-0 velocity and current read from outside). `lay` with `line` named builds `tuple(levels if j == 2 * line else 0 for j in range(2 * len(lines)))`: one count on that line's now alone, over any count of lines.

(b) **Locality.** The choice reads `line.now[at]` and `line.before[at]` of the taken row's own lines at the Node alone; the fall's pull reads the neighbours' `before` through the rule's reaches as before (the one-Link reach unchanged); the take writes `now` at the Node alone.

(c) **Genericity.** `row.lines` of any length (the plane's two, the quartet's, the spinor's eight), no family's name, no typed number in the added lines (grep: no float, no `/`); the only numerals are the exponent 2 and the index arithmetic 2 k.

(d) **The run back.** unclick reads `take["taken_line"]` per take (`entry.get("takes", [entry])`) and lays `taken_now_was - now` on that line with `line=k`; measured exact on every record: hole 20 of 20, chiral 20 of 20, bodies 20 of 20, world_pair_3 10 of 10, world_universe 10 of 10, the cycle board 10 of 10 (736 takes on the second line), the quarter-turned image 10 of 10 and 20 of 20 (81 takes on the second line), the merger board 10 of 10 and 20 of 20 (66 takes on the second line) (replay/*.txt, records/compare_records.txt, cycle/out/read_course_vf12.txt).

(e) **The merger.** merger_take's first loop calls fall_of at minus and at plus (both pre-reads, `refused(node, where, "stop", fall=fall, walls=wall, row=rec)` on the first that stops, the count `refused_stop` by 1 and the log entry with the parent's keys: the records' refusal counts and masked logs equal); the second loop takes at each end. Measured in the call order (replay_takes.py wraps close.fall_of and close.take_at by name): on the merger board 2 mergers, the two reads before both takes at each (call indices 0, 1 before 2, 3 at i 1; 110, 111 before 112, 113 at i 19).

## 3. The numbers (records/compare_records.txt, records/read_records.txt, replay/*.txt, cycle/out/*)

**The three records against the parent** (`$PY -m event_universe.run world_<x>.json <x>_david.json back 20` under $W/src and under parent/src; `compare_records.py`): hole 60: births 16, credits 777, laid back 0, turns 546, refused_stop 434; chiral 60: 17 / 2,943 / 3 / 639 / 2,221; bodies 300: 0 / 1,973 / 0 / 4,229 / 825. On all three: the Node lines equal (60 / 60 / 300 lines), the rows equal apart from milliseconds, the counts equal, the turns equal, the run back 20 of 20 under both. The logs apart in two fields alone: `taken_line` present on every take under David (hole 16 births + 777 credits = 793, chiral 17 + 2,943 = 2,960, bodies 1,973), every one 0; the stop refusals' `fall` 0 under David where the parent carried the negative full fall of the re line (hole 405 of 434 stops, chiral 2,121 of 2,221, bodies 731 of 825: the im line at 0 chosen where the re line's gap is negative, now == before there, the stop with the fall 0). With `taken_line` and the stops' `fall` masked and milliseconds dropped the hashes are equal: hole 91aae3edda7df465, chiral 1a67db943ac367d8, bodies 83b5ecfb490a0954 under both engines. The committed examples/records/{hole,chiral,bodies}.json equal David's re-run bit for bit (milliseconds dropped): ce78886c24b060c3, 03333ae102d29862, 463d17e550345797. Integers per row 98 / 98 / 89, max bits 115 / 115 / 92 (transient 99 / 99 / 78), equal to the parent (the rows equal).

**world_pair_3 and world_universe at 400** (`back 10`): the Node lines equal at 400 of 400 under both, the rows equal apart from milliseconds, the counts equal (pair_3: 297 credits every one laid back, 27 stops, 54 turns; universe: 1,875 credits every one laid back, 250 stops, 250 turns), the run back 10 of 10; the logs apart in `taken_line` (every take 0) and the stops' fall alone; masked hashes 136a1beb39695b93 and 2a6d202b1e9f7b8d under both.

**David's two tests re-derived** (replay/replay_takes.py: this hand's own `my_line` reads the taken row's levels at the Node before the engine's take_at runs, the first line of the largest now^2 - before^2, and compares with the line the engine returns and logs): the pair beside its quarter-turned image at 20: X equal at every Node at 20 of 20, 81 credits on each, equal take for take in (i, node, taken, levels, taker), the board's takes on line 0 (81) and the image's on line 1 (81), the image's re line 0 at every credited Node, 0 mismatches of the line, run back 10 of 10 and 20 of 20. The merger board at 20: the first birth at i 1, the heavy row taken, taken_line [1, 1], 0 heavy-row refusals at or before it, 11 births, 87 takes with 66 on line 1 and 21 on line 0, the one birth's take on the first line at (19, 0), 74 credits, 102 stops, 0 mismatches of the line at 87 of 87 (the takes traced and logged equal as multisets), run back 10 of 10 and 20 of 20.

**The recurring bang with births** (cycle/run_vf12.sh: `cs6_run.py worlds/empty4_ga2_450.json out/ga2_vf12_450.json worlds/cycle_m5_m0.json back 10` under $W/src with NO flag, the hand's scripts and worlds copied beside this hand's; `read_course.py`, `read_stops.py`, `replay_takes.py cycle`, `$PY -m event_universe.gates`, `gates_summary.py`). The world file empty4_ga2_450.json carries no lay (the fifth form `wave` is CS5-S2's, not built); the cycle pattern (p1 [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2], cz 1, 5 quanta, mirror 0, sense 1) is laid by cs5_run.lay_pattern through the engine's one lay act (`node.lay(rec, Ellipsis, levels)`, the amplitude 300 fitted, share_min 8,187,942,649,920,690,060,000, phase_counts 16 x 4), so this is the test of the act, not of the seed from the file. Every number of the prediction (run B under CS4_TAKE_FARTHEST=1) measured under David's build with no flag:

| predicted | measured |
|---|---|
| 64 births at interval 2 at 64 of 64 Nodes | 64 births, all at i 2, at 64 Nodes, classes [0, 1, 2, 3], child rows 0 and 1, taken at or above booked 64 of 64 |
| taken lines 0 at 32 Nodes and 1 at 32 | by line {0: 32, 1: 32}; by (class, line) (0, 0) 16, (1, 1) 16, (2, 0) 16, (3, 1) 16; re-derived from the levels at every take with 0 mismatches (1,472 takes traced and logged, equal as multisets) |
| 0 stops | stops 0 at i 1, 2 and 3 (the first at i 4: 128 at the fall 321 thousandths of the walls, the second gapped row's click after the first took the light); refused_stop 1,408 over 450 as the hand's run B |
| 1,408 credits every one laid back | body_clicks 1,408, laid_back 1,408: 128 at each of 8, 10, 219, 221, 223, 231, 439, 441, 443, 445, 447 |
| tops 109 and 330 with 64 turning | tops (109, 21,888) and (330, 22,321), 64 turning at 110 and 331, turns 128, no turn in parts |
| X = Gamma exactly at every Node at 218 and 442 | bottoms (218, 1,000, 1,000, 1,000) and (442, 1,000, 1,000, 1,000); X one value at 450 of 450, e_max 0; the retrace X(top + k) = X(top - k) at every k about both tops |
| run back 10 of 10 | {"intervals": 10, "exact": 10}; and 10 of 10 from the seed through the births |
| 89 integers, 115 bits | integers 89, max bits 115, transient 99 |
| gates 1 and 46 SHOWN | gate 1 "SHOWN: 2 exact returns to Gamma at every Node, the whole board turning at once at 2 tops, 3 bangs" (births and credits between the bangs [64, 256], [0, 768], [0, 384]); gate 46 "SHOWN: body credits in the later cycle, no birth" (1,152 after 218); 21 SHOWN in all (1, 2, 3, 4, 6, 7, 8, 8b, 9, 15, 16, 17, 18, 21, 25, 26, 27, 43, 45, 46, the constants), 10 NOT SHOWN, 20 NOT READ |

The counts equal the hand's run B to the integer (taken 215,649,578,622,176,003,919,808, booked 215,312,393,244,131,723,991,552, refused_lay 17,088, refused_orientation 33,280, refused_twist 17,152, met 67,584). The charge at every birth: W_children [-18,000, 18,000] at 64 of 64. The same board under the parent 99a9ee860 (cycle/out/read_course_parent.txt, for contrast): 36 births (32 at i 2 at the classes 0 and 2, 4 at 216), 248 credits with 172 laid back, the board parted from i 3 (e 8, X 1,095 / 1,104), no interval with 64 turning, no exact return (bottoms 1,049 at 211 and 987 at 423).

## 4. The laws, each with a number

The run back exact on every record: 20 / 20 / 20 (hole, chiral, bodies), 10 / 10 (pair_3, universe, the cycle board), 10 and 20 on David's two boards. The one-Link reach: the choice at the Node's own levels, the pull through the rule's reaches as before. Integers only: the added lines carry no float and no division. Within 128 bits: 115 on the records and the cycle board, 92 on the bodies. The fixed count unchanged: 98 integers per row on the hole, the chiral, pair_3 and universe, 89 on the bodies and ga2, equal to the parent. No family's name in the diff. The 48 green: the four parts of the 48 images pass in the suite (8.54, 8.51, 7.82, 7.65 s). The charge 0 at every birth: 16 of 16 on the hole, 64 of 64 on the cycle board, 13 of 17 on the chiral where the 4 others (i 7, 7, 8, 10, sums 1,872 / 2,016 / 125 / -864) are the parent's bit for bit (the masked logs equal); on David's merger board 9 of 11 (section 7).

## 5. The tests

The moved count: one assertion re-pinned in the SL-S2 test, `assert refusals and all(cause == "stop" ...)` to `assert merger["i"] == 1 and refusals == [] and merger["taken_line"] == [1, 1]`: a board where the takes land on the second line (the heavy row's 3 B against 0), measured: the merger at i 1, 0 heavy-row refusals before it, [1, 1]; the docstring names the former act's stops. Not a loosening: the former asserted stops before a merger at i 2, the new asserts their absence and the merger's line by name. The other assertions of that test unchanged (the diff touches one line). No count moved on the three records (every take on the first line there, the counts equal). The new test asserts 81 credits equal take for take, {0} on the board and {1} on the image, 11 births, on_first [(19, 0)], (87, 66, 74), the run back 20 of 20, each re-derived here by this hand's own reader (section 3). The new test 3.81 s, the re-pinned 3.08 s.

## 6. The ratchet's line

`tools/tests_shape.py` refuses: "tests/ grew from 1606 to 1696 lines; offset the new tests by deletions in the same pull request" (exit 1). Measured with the tool's own functions (checks/tests_shape_counts.txt): the merge base 6703dd95c (tools/check_base.txt) 1,022 lines plus the rooms named 584 = 1,606; the parent 99a9ee860 1,638 (32 over at toys-5: PL-S1's room of 37 lines is named on engine-5.0-test at 6a482bffb, not on toys-5); the head 1,696, grown by 58 (the new test 56 lines, the def through its last line, plus 2 blank lines). David's push carries NO ROOM entry for `tests/test_the_node.py::test_the_take_moves_the_line_farthest_from_its_before_and_logs_it_per_take_cs4_s2`; the Boss named 40 lines in 6404974647 and the test is 56: with PL-S1's 37 and a 40-line room the gate would read 1,696 against 1,683, 13 over; the room that holds is 56 (or the test cut by 16 lines). For the Boss at the merge, as PL-S1's room was given.

## 7. Remarks (no departure of the act)

1. take.py's module docstring names "the refusal by name (`refused`)" among the module's functions; `refused` is defined in close.py (used by merger_take), take.py does not import it, and take_at's own refusal log is still written inline (the same keys). A docstring's word, 0 effect on the act.
2. On David's merger board the light birth at i 17 at (2, 3, 0) carries W_children [-19,152, 18,000] (sum -1,152) and the merger at i 19 at (1, 4, 3) / (2, 4, 3) books a negative wall (-516,463,374,611,297,597,904) with W_children [-18,430, -12,508] (sum -30,938): the merger act's own reading on a board where light already stands above a quantum at an end (the parent's engine reaches 1 birth on this board, so no parent number stands beside it); the chiral's 4 births off 0 are the parent's alike. For the owner of the merger act (SL-S2), not CS4-S2's.
3. The cycle board's refused_stop 1,408 equals its credits: the second gapped row's click at a Node after the first row's click took the light stops by name every time (the fall 321 thousandths of the walls at i 4), as in the hand's run B.

## Missing by name

The owner's word on the fifth form (`wave` in the world file: the cycle pattern is laid here by the hand's script through the engine's lay act); the ROOM entry for David's test (section 6); the clicks' 48 on the cycle board (not run here); the beat's reading at the laid-back credits (the hand's item 4).

Runs cut short: none.
