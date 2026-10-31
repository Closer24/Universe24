# The sixth hostile code reader (B) on the re-lays, the cut and the lean test, 22a12a328..0456fa478, 2026-10-31

(Written by the Boss from the reader's hand-back, the reader's harness having refused the write; the text is the
reader's, shortened in layout. Evidence in hcr6b/: gate.log, fullcheck.log, fullcheck_loaded.log, lay_*.out,
measure_well.out, prefixes_write.out, blocks/, mut/, probes/ (mesh_window, click_prefix, live_centre, reached) and
reach/. Read: 17f1bbf51, 6d9887945, 77a592264, 8069c3630, 0456fa478; line numbers at 0456fa478.)

VERDICT on 22a12a328..0456fa478 (the re-lays, the cut and the lean test): PASSED

## BLOCKING

None.

## MINOR

1. The held hand's quarter turn is still laid in the mesh world: mesh_lay/lay.py:71 types (1, 0) with its before
   (0, -1), aimed at an angle (90 degrees a round). The audit's N3, NAMED-OPEN, waiting for the owner's word under line
   102; not added by this range. The click world lays the same hand (not in this range). Fix: N3 to the owner before
   main is called clean.
2. The mesh 250000 is lawful (agreeing with Sofer) but sits on a cliff the lay does not show (probes/mesh_window.out,
   125 rounds): meshes 205000 to 240000 move the tied hand at 0 Node-clocks; 250000 at 122; 275000 at 126; 300000 at
   127; 350000 at 129 (at most 900 of the room's 2500). A coupling's strength picked for a qualitative outcome, not a
   root, an angle or a search in code. Fix (mesh_lay/lay.py:38): add 240000 and 350000 to SCAN so lay.txt shows the
   window.
3. The lean test takes its worlds from the written file, not from examples/ (tests/test_the_tensor24_worlds.py:14-20):
   a world added without rerunning write.py goes unguarded. Fix, one line: assert the written worlds equal the examples'
   folders minus our bang's (write.py:30's glob, less BANG).
4. The lean test's 4 rounds never reach the click world's clicks (its first click line is at round 91). Option: a
   92-round prefix for the click world in write.py (92 rounds out and back take 14.2 s, 54 click lines, exact 1), the
   no case kept at 4. The owner's trade between cost and guard.
5. The well's measure script names the ii slots by a typed role tuple, enumerate(("xx", "yy", "zz")) at
   well_lay/measure.py:108 (the tuple's length stands for the dimension; lay.py:153 and :213 read it from the shape).
   Fix: key by range(len(shape)) as lay.py:213 does, and rerun measure.txt.
6. docs/ARCHITECTURE.md still names cut things (line 159, the deleted bangs test file; lines 167-168, rows 15 and 46):
   the document's writer's.
7. Notes: examples/README.md:24 says "499 permille each at round 20" where Rule3's carry gives 498 (548654125767 of
   2^40), rounding where it should cut; its other live claims hold (967 permille at the centre at round 100,
   1063976002389; the halves meeting at z = 30 near round 50, 995 permille). derive/hostile_reviews/seventh/
   decoder_precedence.py imports the deleted books module; it names its head (823690afc) and takes a worktree argument,
   so it still reproduces as a record there.

## The items

1. The three lays: the fake is gone (no mode, Chebyshev recurrence, PERIOD, quarter-beat while loop, NUM/DEN or typed
   SLOTS; the well's slots at :153 the audit's own fix, matching load.py:217); every pulse laid at rest (well :173, mesh
   :72, live :93); each lay regenerates its files byte for byte in a scratch copy (well: setting.json, lay.txt,
   measure.txt; mesh: setting.json, lay.txt, universe.json unchanged; live: setting.json, lay.txt); the typed numbers
   left are each the lay's own named parameter, no angle and no root (well PEAK 12000, H 3, PULSE 500, HALF 4, CENTRE 9,
   TICKS 128, WINDOW 64, SPAN 16; live SCALE 2^28, REACH 8, CENTRE 10, TICKS 100, SPAN 20; mesh 250000, the room Gamma
   div 4, the run's cut-off at 10^9), agreeing with Sofer except the held hand (MINOR 1).
2. The cut: the deleted readers are unread by any run's record (run.py:185-213 writes only a header, click lines, an
   end and ledger Count lines; schema.py:9-11 the same). No kept src function loses its only test: every src function
   the suite calls in-process traced, 312 at 77a592264 (32 passed) and 262 at 0456fa478 (28 passed); only the deleted
   ones drop out (books.py, bangs.py, measure's cone_check, twins, faces, elapsed, counted, pair, outcome, settings,
   clicks, tallies, signal); measure's verdict, meshes and past still reached; records.booked keeps its test; the
   line-feed law keeps its own; shadow.click_board reached through the tool's subprocess before and after. Writer C's
   mutants 6 of 6 caught on this tree. The decode tool on the five records: exit 0, empty stderr, byte for byte
   blocks_cut's, against C6's only the four lines out. The commit's numbers hold (702 test lines out, 2,854 to 2,152;
   measure.py 262 to 36; the tool's four lines).
3. The lean test: it can fail (mutants: the mesh world's universe.json at mesh 200000; the click world's key 50811429
   to 50811431; each caught at its own world alone); no digest typed by hand (write.py rewrites
   tests/tensor24_prefixes.jsonl byte for byte, 6.3 s); no typed verdict; it guards the pruner's gap (each of the four
   worlds loads, runs 4 rounds and back exact, 1.6 to 7.5 s a case).
4. The laws in the range: whole numbers, Rule3's carry the one division, no float, root, search, sine or cosine, no
   while loop in the lays, no number beyond 0 and 1 in src or tools/tensor24_*.py, no len() of a label tuple, no
   declared train, ASCII.
5. The gate and the check at 0456fa478: gate5 --base origin/main --summary no refusal, no note, exit 0;
   CHECK_BASE=origin/main tools/check.py --full exit 0, 28 passed in 18.95 s (selftest 1285 cases; the run test the
   slowest at 13.5 s). A first full check exited 1 on the time bound alone (the run test 34.0 s against 30) while three
   lays ran beside it: machine load, not this range.
6. The judgement: the cut threw out no test that guarded a fake (every cut test pinned a reader that prints NOT READ on
   every record a run writes; keeping them would have left four readings that could drift to SHOWN unseen). Still
   guarded: the click books (shadow.books and the run test's pair world), the cone (measure.past and shadow.cone), the
   record and ledger guards, the line-feed law and the tool's ledger line. The one guard the owner may still want: the
   click world's own clicks on a real run (MINOR 4).

## The Boss's rulings (02:2x UTC)

- MINOR 1: with K = 2 W leaving code (writer D), the held hand is laid at rest like every pulse (before = now), no angle
  aimed; writer B with his re-lay on D's spring key.
- MINOR 2, 3, 4, 5 and 7: writer B, with the re-lay (the click world's prefix at its first click round on D's spring
  key, the no case at 4).
- MINOR 6: Sofer.
