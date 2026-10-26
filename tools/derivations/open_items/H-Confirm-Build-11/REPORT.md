# H-Confirm-Build-11 (vf11): the cold read of PL-S1 at toys-5 99a9ee860fc213926104004fa42b449ab14d184c

**CONFIRMED 99a9ee860.** The act is the letter of the sentence approved on 2026-10-25, 22:50 UTC; every number David names is reproduced to the integer; the suite is green with every test under 15 s; every repository check exits 0 but the tests' ratchet, whose refusal is quoted below for the Boss to give the room by name. No departure found. Two remarks, neither a departure (section 2, items (c) and (e)).

Worktree: `/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf11` detached at 99a9ee860 (parent ea135ef51). The parent's `src/` and `tests/` extracted by `git archive ea135ef51` into `tools/derivations/open_items/H-Confirm-Build-11/parent/` so both shas run on the same world files, the same seeds, the same intervals. Every script, output and log under `tools/derivations/open_items/H-Confirm-Build-11/` (scripts: `probe.py`, `plasma.py`, `canon.py`, `dcheck.py`, `small.py`, `fed.py`, `compare.py`, `runs.sh`; outputs under `out/`, the comparison of every record in `out/compare_all.txt`). Nothing under `src/` or `tests/` edited, nothing committed, nothing pushed. No file above 1.5 MB was produced (the folder is 1.9 MB in all, the parent's copy included).

## 1. The suite and the repository's checks

`cd /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf11; PYTHONPATH=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/vf11/src TMPDIR=/dev/shm/tmp nice -n 19 /home/user/Universe24/venv314/bin/python -m pytest -q tests/ --durations=15` (H-Confirm-Build-11/pytest.out):
**74 passed in 109.71 s, exit 0.** No failure. The slowest test 8.22 s (`test_the_first_part_of_the_48_images_runs_alike_a_reflection_with_the_hands_exchanged`); the new test `test_the_plasma_retraces_bit_for_bit_and_returns_to_gamma_exactly_pl_s1` 2.60 s; every test under 15 s.

The checks one by one (checks.out):

| check | line | exit |
|---|---|---|
| `/home/user/Universe24/venv314/bin/python tools/engine_gates.py` | the engine gates hold against the merge base | 0 |
| `/home/user/Universe24/venv314/bin/python tools/record_code_shape.py` | the shape of the code holds against the merge base | 0 |
| `/home/user/Universe24/venv314/bin/python tools/tests_shape.py` (against origin/main, and again with `CHECK_BASE=6703dd95c`) | `tests/ grew from 1606 to 1638 lines; offset the new tests by deletions in the same pull request` | **1** |
| `/home/user/Universe24/venv314/bin/python tools/documents_gates.py` | the documents' six gates hold | 0 |
| `ruff check .` | All checks passed! | 0 |
| `ruff format --check .` | 185 files already formatted | 0 |
| `mypy src` (venv314/bin/mypy present) | Success: no issues found in 29 source files | 0 |

## 2. The act against the letter (interval.kicks, writes, unwrite, divisions, forces)

Read whole: `git show 99a9ee860`, `git diff ea135ef51 99a9ee860 -- src/event_universe/interval.py` (39 lines moved, one file of src). The sentence's clauses against the code:

- "read at the kick, before the line's division": in `kicks`, inside the loop over `self.riders`, at `r is self.potential` and before `divisions` (run: walled_act, forces, [unwrite], kicks, carrier_act, divisions, [writes]). Holds.
- "SUM over the records with a gap of N.GJ.u_in + N.GJ.u_out": `if r.gap: gj = gram.matmul(g, gram.rotation(r.shape)); charge += gram.form(gj, self.starts[k], u_in) + gram.form(gj, self.starts[k], u_out)`, N = `self.starts[k]` (the levels at the start, `self.at(line)`), u the odd velocities `paces.odd_rounded(2 p + 1, ds)` already in hand for the carrier's source. Holds.
- "one carried division at the line's write wall with the carry in the write remainder": `q, line.wr = carried_division(charge, line.wwall, line.wr, self.direction)` on `self.rows[k][0]`, the shape-4 row's time line. Holds (the write wall T = 36,000 measured on the toy).
- "the quotient landing as a momentum kick w X_now q": `p_other[0] = p_other[0] + self.direction * node.w * self.x_now * q`. Holds; backward `carried_division` at -1 returns the forward quotient and the kick comes off with `direction = -1` (measured in (d)).
- "the time line's numerator None in writes and unwrite": `[None, *self.current]` with `if n is not None` in both; the three odd lines written from `self.current` as before. Holds.
- The dead sums `w_end` (forces) and `w_after` (divisions) removed; `gram.charge` stays in gram.py for the reader (run.reading) and the tests. The former write named in kicks' docstring. Holds.

(a) **Locality.** The charge reads `self.starts[k]` (the Node's own levels), `u_in` from `p_side` (the Node's own lines' levels and remainders at the mean wall) and `u_out` from `p_side + X_now F` with `self.force[k]` the arrivals over one Link already read for the kick. Nothing new is read from a neighbour; the diff names no `across`, `links`, `arrivals`, `frames` or `phases` (grep of the added lines: none). Holds.

(b) **Genericity.** One bilinear for every shape: `gram.form(gj, N, u)` with `gj = gram.matmul(gram.gram(r.shape), gram.rotation(r.shape))`, the quartet's derived G and J included (shape 8 has `gap`, so it enters the sum). No family's name (`grep -rniE "electron|proton|neutron|photon|quark" src`: none), no number typed in the diff (the indices `[0]` name the row's time line as every other act does; `r is self.potential` names the shape-4 row by its shape constant as before). Holds.

(c) **The order of the rows.** The charge is accumulated inside the loop over `self.riders` and spent at `r is self.potential`, so the act rests on every gapped record standing before the shape-4 row in `node.rows_`. That order is not the file's: `rows.rows_of` sorts the file's rows by `order_of` (the walled row 0, the records with a gap 1, the gap-0 plane 2, the shape-4 row 3, the carrier 4; stable), so no file can place a gapped record after the potential row. Measured as asked (`canon.py make` and `canon.py run`, 170 intervals, the same world, the same seed with the rows' indices remapped): three universe files for tests/worlds/world_plasma_3.json, the original order [2, 2, 2, 2, 10, 4, 1], `gapped_after` [2, 2, 10, 4, 2, 2, 1] (two gapped records listed after the shape-4 row) and `gapped_before` [2, 2, 2, 2, 4, 10, 1] (the gapped records reversed). The acts' order printed by the engine is the same in all three ([walled, gapped, gapped, gapped, gap-0, shape-4, carrier], the gapped records' relative order following the file). A canonical per-interval hash (the rows keyed by shape, pair and wall; every line's now, before, rem and wr) is **equal bit for bit at 170 of 170 intervals** in both permutations against the original, the time line's write remainder equal at 170 of 170, X min equal, the top (84, 27), the counts equal (162 credits, 162 laid back). PL-S1 as built does not depend on the file's order of rows. Remark, not a departure: the correctness rests on `order_of`'s sort, which the kick does not state; a reader of `kicks` alone cannot see it.

(d) **The write remainder.** `dcheck.py` on world_plasma_3.json for 100 intervals through the top at 84, each interval stepped forward, back and forward again with `Interval.kicks`, `interval.carried_division` and `Node.write` wrapped: the time line's write remainder after the step equals the one the kick's carried division left at **99 of 100** intervals, the one exception the top 84 where the close's swap mirrors every write remainder once (node.exchange, the law's); `node.write` touched the time line at **0 of 100** intervals (identified by the line object); exactly **one** carried division at the kick per forward interval (direction +1) and **one** per backward interval (direction -1); one step back returns the write remainder bit for bit at **100 of 100**. The write remainder moved at 100 of 100 intervals (the charge is never 0 on the plasma). No second division on that line, the run back inverting it on the same wall.

(e) Remark: the three odd lines' write at the time line's wall T is unchanged; the gap-0 line's and the shape-4 row's four write walls are all T = 36,000 on the toy (write_walls), so a check by the wall's value cannot tell the lines apart; my first count did that and was corrected to the line object before the numbers above were read.

## 3. The numbers David names, measured

Every record run at both shas by `probe.py` (run.record with 20 back, the gates read by `event_universe.gates.gates` on the record as tests/test_the_record.py reads them) and compared by `compare.py` (out/compare_all.txt); the plasma by `plasma.py` (the test's method to 400: the tops, X = Gamma where, the credits, the run back 10 through the top, the retrace at every top).

**Nature's plasma, 3-cube (world_plasma_3.json to 400)**, build: tops (84, 27) and (252, 27); X = Gamma at every Node at **166, 167, 335, 336** and nowhere else; **405 credits, 405 laid back**, 135 in the rise; births 0, laid 0; the run back through the top **10 of 10** (the window 80 to 89); the retrace at the top 84 **83 of 83** and at the top 252 **148 of 148** (the state at top + k equal to the exchange of the state at top - 1 - k in every level and remainder, `node.exchange` the exchange); 98 integers, the state's bits 115, the transient bits 97. Parent on the same world: X = Gamma at 337 alone (the bottom 939 at 167 as David names), 135 credits, the second top at 251, the retrace **0 of 83** (parted from k = 1).

**Nature's plasma, 5-cube (world_plasma.json to 400)**, build (3 minutes): tops (84, 125) and (252, 125); X = Gamma at **166, 167, 335, 336**; **1,875 credits, 1,875 laid back**, 625 in the rise; the run back through the top 10 of 10; the retrace **83 of 83** at 84 and **148 of 148** at 252; 98 integers, bits 115 / 97.

**The pair (world_pair_3.json to 400)**: build against parent **bit for bit** at 400 of 400 intervals (Node lines, log of 3,646 events, the rows at every mark); tops (85, 27), (252, 27); X = Gamma at 168, 169, 333, 334; 297 credits all laid back; the run back 20 of 20.

**The heavy pair (world_universe.json, the 5-cube to 400)**: build against parent **bit for bit** at 400 of 400 intervals (log 19,752 events); tops (101, 125), (301, 125); X = Gamma at 200, 201, 399, 400; 1,875 credits all laid back; the run back 20 of 20. Under the build the retrace at the top 101 is **100 of 100**, the run back through the top 10 of 10 (the one-line parting at k = 1 David names gone; the parent not retraced here).

**The uniform boards**: world_sea_3.json (240) **bit for bit** at 240 of 240 (no record with a gap, no charge; tops (58, 27), (173, 27); X = Gamma at 114, 115, 229, 230); world_universe.json as above, bit for bit.

**The bodies (world_bodies.json, 7-cube to 300)**: **bit for bit** at 300 of 300 intervals, the log of 15,782 events, 1,973 credits, 0 laid back, births 0, the run back 20 of 20, 89 integers, 92 bits; the SHOWN set {2, 3, 5, 6, 7, 9, 10, 18, 30, 37, 43, 45} at both shas; the committed examples/records/bodies.json counts equal (1,973).

**The hole 60 (world_hole.json)**: build **credits 777** (parent 233), **births 16** (16), **turns 546** (546), laid back 0 (0), 98 integers, 115 bits, the run back 20 of 20; the first birth at interval 9 at both shas, the records first apart at interval 18 in the log and 20 in the Node lines (bit for bit before). The committed examples/records/hole.json carries these counts (the suite's bit-for-bit test of the record passed). The SHOWN set before: {2, 4, 5, 7, 8, 9, 10, 15, 16, 17, 18, 19, 21, 22, 25, 26, 27, 30, 37, 43, 45}; after: the same less **9 and 22**. Gate 9 (collisions) from SHOWN to NOT SHOWN, the parent's verdict "SHOWN: two bodies' credited Nodes approached and stood one Link apart", the build's "NOT SHOWN: the credited Nodes receding". Gate 22 (Coulomb's sign) from SHOWN in part to NOT SHOWN, the parent's "SHOWN in part: unlike senses approach", the build's "NOT SHOWN: unlike senses do not approach, like senses do not part". Both named in David's test (VERDICTS and SHOWN_ROWS) with the cause.

**The chiral 60 (world_chiral.json)**: build **credits 2,943** (parent 2,914), **births 17** (17), **turns 639** (641), **laid back 3** (1), the run back 20 of 20; the first birth at 3 at both shas, the records first apart at interval 6. The SHOWN set **unchanged** ({2, 4, 5, 7, 8, 9, 10, 15, 16, 17, 18, 19, 21, 22, 25, 26, 27, 30, 37, 43, 45} at both). The committed chiral.json carries 2,943 / 17 / 639 / 3.

**The gates' SHOWN sets elsewhere**: plasma_3 at 400 before {2, 3, 5, 6, 7, 8, 9, 10, 16, 18, 30, 49}, after {1, 2, 3, 5, 6, 7, 8, 9, 16, 18, 45, 46}: gained 1 (the exact return: "2 exact returns to Gamma at every Node, the whole board turning at once at 2 tops"), 45 (a body stands in its own well), 46 (body credits in the later cycle); lost 10 and 30 (the parent's "SHOWN in the reader's view; NOT READ in the one-place view", the clocks compared through the gap-0 plane) and 49 (the spacings geometric), a charged board whose course PL-S1 moves by the law. pair_3: unchanged {1, 2, 3, 5, 6, 7, 8, 9, 16, 18, 45, 46, 49}. universe: unchanged {1, 2, 3, 6, 7, 8, 9, 16, 18, 19, 26, 46}. No gate turns from SHOWN to NOT SHOWN on a board whose record is bit for bit.

## 4. The laws

- The run back exact: 20 of 20 on every record above (plasma_3, pair_3, universe, sea_3, bodies, hole, chiral, node) at both shas; 10 of 10 through the top on the plasma (3-cube and 5-cube) and the heavy pair; the suite's run-back assertions green.
- One-Link reach: nothing in the diff reads beyond the Node and the arrivals already read over its six Links (section 2 (a)).
- Integers only: `grep -n "float\|/ " src/event_universe/interval.py` none; no true division in src; no float but the gates' "floats used": 0 string.
- Within 128 bits: the plasma's state bits 115 and transient bits 97 (3-cube and 5-cube), the heavy pair's 115 / 98, every record's max bits 115 (toy) and 92 (middle).
- The fixed count of integers per Node unchanged: 98 on every toy record, 89 on the bodies, equal at both shas.
- No family's name in src: none.
- The 48: the four parts of the 48 images green in the suite (8.1 to 8.2 s each).

## 5. The counts re-pinned in the tests

`git diff ea135ef51 99a9ee860 -- tests/`: 32 lines net (the new plasma test 37 lines; docstrings re-cut). Every moved number sits on a board charged when it parts, measured per interval at both shas (`small.py`, `probe.py`):

| test | moved | board | first birth (gapped levels first not 0) | first interval apart | by the law |
|---|---|---|---|---|---|
| the horizon (test_the_node, world_node.json fed at the centre, 20) | the credits' senses `[(0,0)]*9 + [(-1,0),(1,0),(1,0)]` to `[(0,0)]*4 + [(1,0),(0,0),(-1,0),(-1,0)] + [(1,0)]*4` (twelve credits, five at W 0) | uncharged at the lay (the carrier's axis and the light fed) | 2 | 3 | yes |
| SL-S1 births 5 to 4 (the chiral on the 3-cube, 30) | births | uncharged at the lay | 6 | 8 | yes |
| WS sites 2,160 to 2,156, nonzero 695 to 625 (chiral 5-cube, 20) | sites, W not 0 | uncharged at the lay | 3 | 6 | yes |
| PM-S1 body clicks 1,996 to 1,999 (chiral 5-cube, 40) | credits | as above | 3 | 6 | yes |
| CK-S1 credits 819 to 825, upward 642 to 697 (chiral 5-cube, 20) | credits | as above | 3 | 6 | yes |
| EQ-S1 hole births 12 to 16 at 20; the 48's births 12 to 16 (hole 5-cube, 20) | births | uncharged at the lay | 9 | 18 | yes |
| test_the_record: hole credits 233 to 777, chiral 2,914 to 2,943, laid back 1 to 3, SHOWN_ROWS of the hole less 9 and 22, VERDICTS 9 and 22 | the records | as above | 9 / 3 | 18 / 6 | yes |

No count moved on a board with no charge: the pair, the heavy pair, the bare sea, the bodies and world_node.json unfed are bit for bit at both shas. No assertion loosened: every equality stays an equality (`== (16, 0)`, `== 1999`, `== 4`, `== [296, 2156]`, `== (825, 697)`, the credits list), no check removed; the hole's VERDICTS gained an entry for gate 9 (asserted NOT SHOWN by name), gate 22's entry re-pinned to NOT SHOWN, SHOWN_ROWS of the hole re-pinned with the two gates named in a comment. ENGINE.md's one sentence re-cut (the acts' list, (3) and (5)).

## 6. The ratchet's line

`tools/tests_shape.py` (against origin/main and with `CHECK_BASE=6703dd95c` alike): `tests/ grew from 1606 to 1638 lines; offset the new tests by deletions in the same pull request` (exit 1). The room asked by name in David's line; for the Boss to give.

## 7. Missing by name

- David's "148 of 148" is the retrace at the second top (252) on the 3-cube to 400 (400 - 252 = 148 k's), not a 5-cube figure; measured 148 of 148 on the 3-cube and on the 5-cube alike (both top at 84 and 252).
- The heavy pair's parent-side "one-line parting at k = 1" was not retraced here (its build-side retrace is 100 of 100; the parent's records are bit for bit with the build's in every Node line and log entry, so the parting David names lived in the write remainder alone).
- `kicks` does not state that its sum rests on `rows.order_of` placing every gapped record before the shape-4 row (section 2 (c)); measured harmless, named for the Scribe.
- The comparison document named in the brief as The-Plasma-Charge-At-The-Kick_COMPARISON.md stands in the worktree as tools/derivations/open_items/PL_COMPARISON.md with the hands' folders pl1 and pl2.
