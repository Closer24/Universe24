<!-- Boss note, 2026-10-31 12:15 UTC: written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of Big Pic's Bell mend (bigpic-3clicks f729099e6), the hostile physicist (the HALF pair's physicist). -->

The harness refuses report files from subagents, so the whole report is below. The Boss can write it to S/bp_bell2_phys/REPORT.md.

# The hostile physicist (HALF pair) on the mend of Big Pic's Bell from the end (bigpic-3clicks f729099e6), 2026-10-31

**What I read:**
- BRIEF_PAIRS.md to its end: the 11:47 and 11:52 laws and the rulings on them, the 11:5x word, and the 12:1x and 12:2x rulings.
- The freeze: FROZEN.sha256 is 161 of 161 OK. Against 2a839f25f, three files changed: bellend.py and bellend.txt (additions only) and three_clicks/README.md. PICTURE.md, pairbell.py and pairbell.txt are unchanged.
- I did not open the other reader's folder.

**Reruns:** from a copy at S/bp_bell2_phys/rerun/, with node-all's src taken from the tar. Python 3.14 -I -B, nice 19, the load under 8. bellend.py matches the new bellend.txt byte for byte, and no .pyc was left.

**My probe:** S/bp_bell2_phys/dial2.py, run twice. dial2_run1.txt and dial2_run2.txt are identical (sha256 455adc57...). It runs bellend.py's own definitions unchanged. Whole numbers, Rule3's carry the one division.

VERDICT on the mend of Big Pic's Bell from the end: NOT PASSED

The mend adds a correct (C)-form preamble, and everything new in it is right and exact. But B1 is not met, because the law's own three parts were left as they were:
- part (i) still has a click leave the hand on the board;
- part (ii) still runs it back through the birth;
- the OPEN line still asks for that act.
So the text now states both forms, one after the other.

## Met and not met

| Item | Met? | Where |
|---|---|---|
| B1: the end law in (C)'s form | in part: the preamble states it, but parts (i) and (ii) and the OPEN line keep the refused form | bellend.py 5-9 against 14-16; README 82-83 against 96-97 and 113-114 |
| B1: "nothing picked" struck | met | bellend.py 5; README 80-81 |
| B1: the dependence a laid measure, its source the 11:52 law, its form OPEN | met, with the 08:4x pick rule cited | bellend.py 6-9; README 84-92 |
| B1: the end and the weight are not click facts | in part: the weight and the mark are named OPEN, but "no click reads the weight in this law" (11:3x Q2) is not said | README 93-94; bellend.py 20-21 unchanged |
| MINOR 1: "reading", "Read exactly" | not met (it was not ruled) | README 80 and 100; bellend.py 22 |
| MINOR 2: no signal rests on the equal split | met | bellend.py 28; README 109-110 |
| MINOR 3: Tsirelson | in part (see below) | README 111-112; README 103; bellend.txt line 63; bellend.py 18 |
| MINOR 4: the ruled control | in part (see below) | README 105; bellend.py 24 and 184 |
| The key's odd dial | met; MEASURED exactly; the weight is not said | README 109-110 |

- **MINOR 3 in detail.** README 111-112 now reads "a lattice point 41 millionths below it, a test's lay", which is met. Three places still conflict with it:
  - README 103 still reads "which is Tsirelson's 2 r2", and so does bellend.txt line 63, "(Tsirelson's 2 r2 is 2828)";
  - the comment on Z does not name it a test's lay;
  - part (iii) still says the share is "the triangle's own squares (1, 3/4, 1/4, 0)" (bellend.py 18; README 98-99), but at z the share is 147/172.
- **MINOR 4 in detail.**
  - Met: the local act at the bound is in, and reads CHSH exactly 2/1, both at the triangle's settings and at z's, with no share of exactly half (MEASURED, D2). Over all 1,296 choices of two lattice lines per place, its largest |CHSH| is 2/1 (D3).
  - Not met: the free lay is still named "the free-lay control" (README 105, bellend.py 24, the label at 184, and bellend.txt). The 11:3x Q4 rules "one name, one control".
  - Not met: the ruled member born at the middle, which that ruling also puts into bellend.py, is not there.
- **The key's odd dial (D1).** MEASURED exactly on D = 50,811,429, with HALF = (D - 1)/2 and a far share of floor(n D / d) of D seeds:
  - the largest signal at 1:0 and at 0:1 is 63,514,286 / 2,581,801,317,022,041, which equals (5D - 1)/(4D^2);
  - at 1:1 it is half of that.
  - The README should say that the figure holds with one end alone.

## Lines that still let a click write the board (11:47)

- **bellend.py 14-16 and README 96-97:** "(i) one wing's click fixes the hand: clicking +1 it leaves the hand along its setting" and "(ii) the board runs that end back to the birth: ... the hand that end left". The 11:47 ruling: "A click that writes the board's state, directly or through a birth, is refused." The 11:3x Q1: "A click that leaves the hand on the board would amend the law of the path, and that is not asked."
- **README 113-114, the OPEN line:** "the law on the board's own act, that is, the end click leaving the hand along its setting, the run back to the birth". This OPEN asks for a refused act. It should ask for the seeds' law that lays the hand with the start and the end, with each click only reading.
- **A pointer, outside stage 4c:** the README's new spread section has "a click that lands one quantum, split between an outlet along the setting and one across it". The 12:2x Q3 already rules that the outlets may not depend on the setting.

## Lines that connect the two places within the run (11:52)

- **bellend.py 11:** "born once at the source and carried, unchanged, to its two wings". **README 95:** "the pair's one hand runs from the birth to both wings".
- **Part (ii):** the fixing wing's click is carried through the birth to the far wing.
- **The free lay and the local act:** "the hand born free at the source" (bellend.py 24, 26, 104, 128 and 184; README 106).
- **Stage 4b's timelike case (T):** "wing A's setting and landing carried on to wing B" (twoends.py 21; PICTURE.md 154; README 78). That is a click's landing reaching the far place within the run.
- **The lawful twins write the same joint law.** For each, the twin is each wing's own copy, laid with the start and the end. My first Bell probe showed the start twin equals the end law at 16 of 16 cells, and the free lay and the local act are the same counts under this restatement.

## New items

1. **One form, not two.** Restate parts (i) and (ii) in the preamble's form:
   - (i): the hand and the fixing wing's setting and outcome are fixed together by the start and the end, the hand along the setting where that outcome is +1 and across it where it is -1, one count each way;
   - (ii): each wing's copy is laid with them, and no click and no passing carries it;
   - (iii) stays as it is.
2. **The 12:2x Q4 premise does not hold.** It says "as bellend.py already does". But bellend.py's part (i) is the same sentence the THIRD physicist flagged in the README.
3. **The dial's signal:** name the weight it holds at.
4. **Stage 4b's timelike case:** under 11:52 it should be named refused, kept only as a control of what the law forbids.

## Questions for the Boss

1. Are parts (i) and (ii) restated in place, with the OPEN line naming the seeds' law rather than an act in which the end click leaves the hand?
2. Is "one hand born at the source and carried to both wings" restated as each wing's copy laid with the start and the end, for the end law, the free lay and the local act alike?
3. Is stage 4b's timelike case named refused under 11:47 and 11:52?
4. Under the 11:3x Q4, does the free lay drop the name "control", and does the ruled member born at the middle go in beside the local act?

## Solution24 (the reader's line)

The mend adds what is sound and exact:
- (C)'s form;
- the laid measure's source, the owner's law of 11:52;
- the ruled local act at exactly 2;
- the equal split's role in no signal.
But the old law still stands beneath it. One restatement of the three parts and the OPEN line, in the form the preamble already gives, would meet B1.
