<!-- Boss note, 2026-10-31 12:14 UTC: written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of Big Pic's Bell mend (bigpic-3clicks f729099e6; 739bffbd2, f729099e6), the hostile mathematician (the HALF pair's mathematician). -->

Reader of Big Pic's mended Bell from the end (bigpic-3clicks f729099e6; commits 739bffbd2 and f729099e6), the hostile mathematician (the HALF pair's mathematician). My harness does not let me write report files, so the whole report is below. Please file it as S/bp_bell2_math/REPORT.md.

My probe is p_bell2.py, with its output p_bell2.txt, in S/bp_bell2_math/. The rerun copy is rerun/ in the same folder.

# The hostile mathematician (HALF pair) on the Bell mends, 2026-10-31

**Read:**
- BRIEF_PAIRS.md to its end (line 1699), including the 12:1x and 12:2x rulings.
- The two commits' diffs against the 2a839f25f freeze: three_clicks/README.md stage 4c, bellend.py and bellend.txt.

**Checks:**
- FROZEN.sha256: 161 of 161 OK.
- 160 bench files are f729099e6's, blob for blob. The 161st, tests/frame.py, is 9d75a4904's addendum, as the 11:2x ruling has it.
- The tar is unchanged.

**Reruns:** from the copy, under the live venv's Python 3.14.6 -I -B, nice 19, with the load below 8 for every run.
- bellend.py reproduces bellend.txt byte for byte.
- No bytecode appeared.

I touched no repository or worktree, did not open the other reader's folder, and posted nothing.

VERDICT on the mend: NOT MET IN FULL

The counted law is unchanged and stays PASSED. Of my seven MINOR items, two are met, four are met in part and one is not. There is one new item.

## My MINOR 1 to 7

1. **Tsirelson's line: in part.**
   - Met: README line 111 reads "Tsirelson's 2 r2 is its supremum, and z = 13 + 5 w is a lattice point 41 millionths below it, a test's lay."
   - Not met, still in place:
     - README line 103: "2,828 per mille ... which is Tsirelson's 2 r2";
     - bellend.py line 223 and its printout: "(Tsirelson's 2 r2 is 2828)".
   - The fraction is unchanged: 449,753 / 159,014 (p_bell2).
2. **"From the end" named untested: in part.**
   - Met in lines 84-95:
     - "the dependence is laid by statement, and its start twin writes the same joint law";
     - the weight and the mark in the clicks are named OPEN.
   - Not met: the three parts below them still state the old form (see the new item).
3. **No signal on the counting, not on a fixed dial: met.**
   - README lines 109-110 carry the equal split and (5 D - 1) / (4 D^2).
   - bellend.py's header line 28 carries it too.
4. **"Every seed is counted": in part.**
   - Met: "Nothing picked" is struck, and no signal is said to rest on the equal split.
   - Not met:
     - the comment at line 80 still says "36, 12 or 4" and omits 108;
     - no assert checks that the scales' carries leave 0.
5. **The free lay against the ruled control: in part.**
   - The local act at the bound is in. MEASURED exactly (p_bell2):
     - CHSH is exactly 2 at the triangle's settings and at z's, where every one of the 12 hands gives +2;
     - its largest CHSH over all 12^4 setting choices is 2;
     - its +1 shares are exactly 1/2 on all 144 pairs;
     - no share of exactly half occurs.
   - Not met:
     - The free lay is still named "control" in README line 105, in bellend.py lines 24 and 184, and in bellend.txt line 41. The 11:3x Q4 ruling says "named a reading (half the curve), not the control".
     - The ruling's "ruled member born at the middle" is not in bellend.
6. **R4 and the records: met as named.** "The order reading both ways, and the pair's reading" stay OPEN, and DECODE3j and DECODE3k carry the rest.
7. **pairbell.py: not met.** It is unchanged and still uses random, float, Fraction, divmod, % and //.

## The restated (C) form

- **It keeps the counted law exact, with the same joint law.**
  - MEASURED (p_bell2): I counted (C)'s form apart. Per fixing end, the hand is laid in advance along or across that end's setting, one count each. The end's outcome is read from the hand, and the far click chooses by its own seeds.
  - On all 144 ordered pairs, at the weights 1:0, 0:1, 1:1, 1:2 and 3:7, it equals end_law_on count for count: 0 off.
  - The end law itself is still (1 + oA oB cos 2 theta) / 4, with shares of 1/2: 0 off.
  - DERIVED: it is the same products relabelled.
- **It holds checks that cannot fail.** Each reads the laid measure back, so it is a check by construction. Name them so, as the rulings name such identities elsewhere.
  - E = cos 2 theta, the shares of 1/2, CHSH 5/2, and the readings being the same at every weight are identities of the laid measure.
  - The local act's count of shares of exactly half is 0 by structure. Every angle between hexagonal lattice vectors has tan equal to sqrt 3 times a rational, so none is 45 degrees.
  - Its shares of 1/2 are structural too. Any window of 90 degrees not ending on a hand holds 3 of the 6 lines spaced 30 degrees apart.

## New item

**N1. Parts (i) and (ii) still state the refused form.**
- Where:
  - README lines 96-97: "(i) one wing's click fixes the hand: clicking +1 it leaves the hand along its setting"; "(ii) the board runs that end back to the birth";
  - bellend.py lines 14-16 and line 20;
  - README's OPEN line 113, which lists "the end click leaving the hand along its setting, the run back to the birth" as an open act.
- Why it is refused: under the 11:47 ruling, a click that writes the board's state, directly or through a birth, is refused. So the act in the OPEN line is refused, not open.
- These lines contradict the (C)-form paragraph above them in the same file.
- The 12:2x Q4 ruling says README part (i) takes the restatement "as bellend.py already does", but bellend.py's own (i) and (ii) have not taken it.
- Fix:
  - (i) reads: the hand and the fixing end are laid in advance, along or across that end's setting, one count each, and the fixing end's outcome is its reading of the hand;
  - (ii) is struck;
  - the OPEN line reads: road (C)'s seeds' law, its form from the structure.

## Questions for the Boss

1. Is N1 carried by Big Pic now, with the free lay renamed and the Tsirelson residues mended in the same commit?
2. Should the end law's readings be named checks by construction, alongside the local act's tie count?

## Solution24 (the reader's line)

The mend keeps the counted law exact, and its restated form changes no count. But the old click-writes-the-hand words still stand beside the new ones, and the owner's 11:47 law refuses them.
