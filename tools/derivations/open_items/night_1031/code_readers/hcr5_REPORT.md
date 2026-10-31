# The fifth hostile code reader on C5 and C6 (b1a50bb33..22a12a328), 2026-10-31

(Written by the Boss from the reader's hand-back, the reader's harness having refused the write; the text is the
reader's, shortened in layout. Evidence in hcr5/: gate.log, fullcheck.log, runs/, runs_c5/, mut/ (run.py, run5.py,
run.out, run5.out) and probes/ (p1.py, p1.out, p1_m7.err). Line numbers at 22a12a328.)

VERDICT on b1a50bb33..22a12a328: NOT PASSED

One BLOCKING item: the brief's item 6 is not met. 14 of 19 mutants on shadow.py's new code pass all 20 decoder tests;
three change what the shipped click world prints, and one leaves a cone check that can never read SHOWN. (The fourth
reader rated surviving mutants MINOR, his MINOR 1; the brief said "each must fail a test".) The rest holds: the laws,
the gate (no refusal, no note), the full check (exit 0, 32 passed), the five records decoding as 13b's table says
(every line above the click world's block C5's except the D7 label), and all six of the fourth reader's items MET.

## BLOCKING

1. What the new readings print is pinned by no test. Each mutant a text edit in a copy of the tree, run on all five
   decoder test files; the control passes (mut/run.out, mut/run5.out). The worst survivors:
   - M1, shadow.py:101: the giver and the taker swapped in the meetings' count. The click world then prints "999 from
     train 3 to train 4, 1107 from train 4 to train 3", the reverse of 13b's table, and every test passes. Cause: the
     yes record at tests/test_the_tensor24_decoder_meetings.py:68-69 is symmetric, one meeting each way.
   - M4, shadow.py:240: the cone's SHOWN branch made NOT SHOWN. No test reaches the 1.3 cone's SHOWN; "stands inside
     the lay's cone" is asserted nowhere.
   - M2, shadow.py:132: each clock's count taken as all its lines (len(held)), the frame's own named mutant ("counts
     every line a meeting") in its literal form. (Writer C's version, meeting = set(places), mutants.py:31, is caught.)
     The lone-line no at meetings.py:98-100 asserts only the kind and the cause, never the clock's count.
   - M12, shadow.py:229: events[-1] for events[0]; the click world's D8 cause would name the last line's round for
     round 91.
   - M14, shadow.py:74 (C5's line): the books' trains taken as held.trains; trains 0 to 2, at 0 lines, drop out of the
     click world's books block.
   - Fix, one for one where possible: meetings.py:68-69, place 2 a give from train 2 to train 1, click(2, 0, 1, 1),
     click(2, 0, 2, -1), expecting "1 from train 0 to train 1, 1 from train 2 to train 1" (still catches the
     train-order mutant); one cone SHOWN (SEVEN with only the round-1 line at site 4, SHOWN, "... from the 2 sites
     laid: 1 of the 1 lines that could stand outside it, of 1 lines"); at :100 assert the lone clock's count is 0. The
     file then rises one or two lines past its ROOM of 158.

## MINOR

1. D8's "could" rule still allows a SHOWN that cannot fail when two or more sites are laid (the fourth reader's
   BLOCKING 1 again, narrower, on hand-built records only; the code follows the Boss's ruling exactly, so the change is
   the Boss's). shadow.py:224-226: the bound is the board's diameter; the true bound is the lay's own reach, the most
   Meshes from a site to its nearest laid site. Evidence (probes/p1.out): a ring of seven laid at sites 2 and 5; at
   round 2 no site stands outside the lay's cone, yet two lines at round 2, site 0, read SHOWN, "2 of the 2 lines that
   could stand outside it". Fix: the bound as the max over sites x of the min over laid sites y of meshes(sides, y, x)
   (whole numbers, no division; it equals the diameter when one site is laid).
2. Other survivors of all 20 tests: M3 (shadow.py:64, spread always gives the most: unequal clocks would print "78
   meetings each"); M5 (:201, the lower bound dropped, a gear at site -3 read on the board; the test at meetings.py:129
   has site 7 alone); M6 (:76, the books' gap filter removed; no test has a place with a line with q and one without);
   M7 (:95, "train" dropped from the meetings' gap fields: on a line with no train the tool raises KeyError and exits
   1, probes/p1_m7.err, though its docstring says nothing is raised; the original reads NOT READ, exit 0); M8 (:226,
   "or not lay" dropped); M9 (:140, the lines astray counted for the clocks); M10 (:207-208, a gear of no shape
   skipped); M11 (:188, RecursionError not caught); M13 (:41, the last gap named for the first). Cheapest: a site -3
   gear row at :129 and a train-less line in the row-15 test.
3. Notes, not defects: reading (b)'s verdict word always equals reading (a)'s (a line in no meeting stands at a place
   that is not a meeting), so (b)'s SHOWN is no second claim; what (b) adds is its counts, which M2 and M3 show no test
   pins. A setting with no gears reads NOT READ (as the frame asks); one whose gears are all 0 also lays nothing but
   reads NOT SHOWN on every line.

## The fourth reader's six items: all MET

- BLOCKING 1 (D8 vacuous on the click world): the click world reads NOT READ, "the lay's cone covers the board's 27
  sites from round 0, before the first click line at round 91: no line could stand outside it"; the test lays sites 2
  and 5 on a ring of seven (site 6's gear all 0), one line inside site 5's cone alone and one outside both, NOT SHOWN
  with the cause asserted whole; his three mutants caught. (MINOR 1 covers what the rule leaves.)
- MINOR 1 to 5: MET (the books' cause whole; NO CLICK and the owner's phrase as literal text; no refusal line on a
  record with click lines; train 0's tally; a header with no sides and one with no setting file; row 15's order; each
  reading's own NO CLICK check; the setting read as the runner refuses, except the lower bound's test, M5; the
  wording).

## The frame 13b and the laws

- Met as written: the meetings (one give and one take a place); each clock's line ("the order counted, no duration");
  D6 NOT READ with NO_COUNT, D7 NOT READ with AT_NODE; D8 NOT READ where no line could stand outside the lay's cone;
  light's echo NO CLICK on a record with no click line, else NOT READ with its cause; the books in row 15's order;
  shadow(record) keeps its four readings and click_board(record) gives the three new ones.
- The laws hold in shadow.py and tools/tensor24_decode.py (token scan and gate): whole numbers; no division (the one
  "/" the Path join at tool:24; each ** keyword unpacking); no float, root, search, sine or cosine; min and max only in
  spread and the diameter; no number beyond 0 and 1, no 1 + 1; no len() of a label tuple or constant; no typed verdict
  (D6, D7 and the echo through not_read()); ASCII. shadow.py:188 "except ValueError, RecursionError:" is valid on the
  pinned Python 3.14.

## What was run

Detached worktrees at 22a12a328 and 49e97c992 (removed); nothing committed or pushed. The gate (gate5 scribe_scan.py
--base origin/main --summary): no refusal, no note, exit 0. The full check: exit 0, 32 passed. The decode tool on the
five records with their ledgers: exit 0, no stderr; tensor24, -live, -well and -mesh NO CLICK on all seven with the
refusal line last; tensor24-click as 13b's table (books SHOWN 0 at 2,106 of 2,106; meetings SHOWN 1,107 and 999;
clocks' lines SHOWN 54 clocks of 78 meetings, train 3's 27 at net -4 and train 4's at net 4; D6, D7, D8 and the echo NOT
READ with causes). Mutants: 19 plus a control, 5 caught (M15 to M20), 14 survive.

## The Boss's rulings (02:0x UTC)

- BLOCKING 1: to writer C, one for one, M1, M2, M4, M12 and M14 each to fail a test, with M5 and M7; the rest where a
  line's change covers it, the others named in the commit message.
- MINOR 1: the reader's fix is taken; "could stand outside" uses the lay's own reach. The earlier ruling (the
  diameter) is withdrawn: it left a SHOWN that cannot fail on hand-built records.
