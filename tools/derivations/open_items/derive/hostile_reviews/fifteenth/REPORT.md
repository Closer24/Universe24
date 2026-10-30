# The fifteenth hostile review: stages 7b and 10 together, one reader for two stages (decision 27) (861f883e9, 20e8a8bf2, 0ef8d217d, 58962f91a)

Verdict: approve with changes (a fresh reader, 07:5x UTC 2026-10-29, at tensor24-review 20e8a8bf2). The act matches
David's table number for number and the run back is exact in every state tried; three changes are asked, in the
runner and in the tests of 7b's ruler and of stage 10's record. The probes stay in the reader's scratch (decision 26),
review_s16/probes/, each pN_*.py with its .out beside it. The engine's build is stopped on the owner's word of
07:4x UTC until the big picture closes, so each change waits for the build and is listed here as owed.

## Required changes

1. **The runner raises or hangs on files the checker passes** (its docstring promises every departure named):
   - full_rate 1 passes files.py and divides by Gamma - 1 = 0 in load.ruler_of (ZeroDivisionError, the tool exiting
     1 with a traceback; p8_gamma1_tool.out, p4_runner.out): the checker takes a full_rate of at least 2, with a
     departure test;
   - a large full_rate walks about (Gamma / 2) ln(2 Gamma) carries (610,349 counts in 1.6 s at Gamma 10^5; past 60 s
     at Gamma 10^9): named before the walk, as lay() names a board past the machine's arrays;
   - integers past 4,300 digits pass the checker and the tool dies at json.dumps on the time gear's winding: the tool
     lifts the interpreter's bound on digits, as tools/tensor24_decode.py does.
2. **The tests of 7b's ruler are too weak** (tests/test_the_tensor24_time_gear.py; the code right, p1): mutants survive
   the suite (p2_mutants.out, p6_ruler_survivors.out): Z as T Y^2 div Gamma^2, the square table as Y Gamma, last one
   count early, and four rounding mutants (the floor instead of the rounding changes 1,933 of 3,793 entries at Gamma
   1,000). The fix: the tables pinned whole, and the ruler compared bit for bit with the head's rate line, rate(Gamma,
   -c) for c below stopped_load(Gamma), over a range of Gamma.
3. **The record's fields mostly unpinned** (tests/test_the_tensor24_run.py): 8 of 24 run.py mutants survive (the
   winding from the kick, the cards' kinds and part, couplings dropped, sides reversed, the width, a kind's
   dimension, the rate line's dial). The fix: a file that tells these apart (sides [2, 3, 4], a coupling row, trains
   of part 1 and 2 and of two kinds), the whole header compared with one built from the files, the time gear's winding
   (T div 2) key, and the dial read. The stage-10 commit's "nine source mutants of run.py, each killed" overstates.

## Follow-ups

- **The example world is vacuous for the ruler:** its time gear stays at count 0 for 40 ticks (light at amplitude 1),
  so the run tests pass with ruler-read mutants (p7_vacuous.out); a runner test needs a file whose time gear moves.
- **Scale, for David and the big picture:** with the example's one gear at 10^12 the time gear's count reaches about
  10^20 within 10 ticks, against a last count of 3,792, so every reading row sits at Y(last) (p4b).
- **"At every count":** the masks test compares the first beats and the end's digest alone (the property holds: p3, 0
  mismatches); strengthen it or rename it; the plan's stage-10 row says "byte for byte", where the masked record
  differs in its rounds and its runner's name.
- **A file train named "the time gear"** gives two cards of one label; the checker should refuse the name.
- **A stale record:** a run with a departure leaves an earlier record at the path, and it still reads.
- **The checker's norm message** (c98cf9154, before these commits) is built before the comparison, so a hand with den
  near 10^2150 makes the checker raise.
- **The undo log** lives in memory (about 2 KB a round at 64 sites); the plan keeps it beside the record.
- **Equivalent survivors:** ruled passing the drive's teeth unchanged; the time gear's row alone surviving the
  untick's first ungear; L01 to L03 on the least G.
- **The Boss's log at this head:** 508 passed, exit 1 on the 30-second bound alone (a head test, 33.1 s); a quiet rerun.

## What holds

- David's table, every number (p1_table.out): G by K-S1 the head's mesh_unit_of for every Gamma from 1 to 3,000;
  T = 6 den Gamma^2 G^2 and every grip den Gamma^2 G^2; the file's trains at W = W+ = 2 T, s = 2, the spring at rest
  12 (den - pinion) G^2 Gamma^2; the time gear at W = W+ = T, s = 1, its pinion den - den div Gamma, its kick T, its
  drive's teeth (T div 2) key; one cone, 1/6, on every row; the ruler equal to the head's rate(-c) bit for bit at
  eight values of Gamma (3,793 counts at Gamma 1,000, Y(0) = 1,000, Y(last) = 44,429); the tables, the reads, the
  spring factors and J's plan as written.
- The run back (p3a): 720 single rounds and 72 ten-round rewinds home, over Gamma 2, 7 and 50, four shapes, light with
  a massive train, a T1 hand, an A2 gear and a coupling row, 122 runs crossing below 0 or past the last count.
- The masks against the synchronous run (p3b): 13,260 site-counts, 0 mismatches; the runner on five other files under
  three seeds each, every record read by the decoder, exact 1.
- The order of the reads (p2): all 28 non-equivalent step.py mutants and all 7 of sourced killed.
- The laws (p5): no // or % outside carry.py, no literal beyond 0 and 1, no float, no if, comparison or loop in the
  engine; the runner imports no engine module; ruled reads its own site's counts alone.
- The gates: refusals 0, four notes; ruff, the format, mypy, the shape and the engine gates clean; 390 Tensor24 tests.
- Decision 27 true to the owner's four answers; 7b's commit true to the code; stage 10's message overstating three
  things (every departure named, "at every count", nine mutants each killed).
