# Fifth hostile review: 81521e0f4 (the reviews' fixes), 49c65abfa (Animate's decoder), 0970b0deb (the schema's lines)

Verdict: approve with changes (agent aadfc81ccee0cb547, returned 20:1x UTC 2026-10-28). The engine (mesh.py,
state.py, step.py) could not be broken; R1 holds; C1 to C3 done for real.

## Required

1. (the Boss) The checker's test misses the other side of several bounds and every length: 20 of 128
   moved-by-one mutants of runner/files.py pass (probes/checker_moved_by_one.py). Part, integers and sides >= 1
   can move to >= 2; a coupling's parts >= 0 to >= 1; version == 1 widen to <= 1; rim != den narrow to > den;
   the row, pair and shape lengths widen (a gear or coupling row of 7 or 5 raises at the unpack, a pair of 1
   raises IndexError: probes/checker_length_raises.py). Fix: 13 edits (probes/test_files_strengthened.py);
   0 of 128 survive with them.
2. (Animate) records.read raises: a line nested 100,000 deep (RecursionError); a whole number of 4,301 digits
   (ValueError, Python's digit limit). Fix: catch both in parsed(), name the line; lift the limit in the tool
   (sys.set_int_max_str_digits(0), as gates.py and run.py do) or name the bound in the schema
   (probes/decoder_raises.py).
3. (Animate) The tool raises where the plan says NOT READ: an absent ledger (FileNotFoundError), a blank or
   non-JSON ledger line, a list line, a line without "at", a whole click at a Node-clock with no rate line
   (zip strict), no argument (IndexError). Fix: the ledger read through guards; ticks_to answers an empty
   list; a usage line.
4. (Animate) The decoder's tests cannot fail on most readings: 15 of 16 source mutants pass
   (probes/decoder_mutants.py). Fix: the five tests of probes/test_decoder_strengthened.py (16 of 16 die,
   28 tests pass).

## Follow-ups

- Layout.meshes pairing: nothing refuses a wrong pairing; name where it is made true (runner/board.py, the
  load). "The far end conjugate" is the identity on integer grips: it waits for Gaussian grips.
- world() pins tb = tn - 1; restore a gap; give order() a second layout (three narrow stale reads die by
  order() alone at its one layout).
- N9 (the act scaled by 1 + trains // 5) still passes rename, which tries 3 and 4 trains.
- Wording: files.py:1 and the tool's line 1 still say "every reference whole" unqualified; the width
  departure names the file, not the field.
- The Boss's run2.py has one mutant that no longer matches (54 of 54 in substance).
- (Animate) records.py uses splitlines, which splits at U+0085, U+2028, U+2029: split on "\n".
- Schema wording: the Rate's and Whole's count is the count the beat reached, the first beat being 1. A Whole
  with one end is read at that end alone (Animate's guards).
- (Animate to confirm) row 15's second reading in the plan is the wind over every train; books.py reads the
  ledger's windings. Only whole clicks are counted: a split click or a turnover moving windings between the
  step and clicks lines would read NOT SHOWN on a lawful record.
- The wall's dynamic imports: open at 0970b0deb, refused at 2eec73c1d.

## What holds

The engine: 31 engine mutants killed but the equivalent control; untick exact on 1,200 random states; the tie
rule on the whole tick 40 of 40. C3's memo dies in the fresh interpreter. C4: nothing raises (P4), P5's 16
mutants killed. R1: 41 of 41; an AST sweep of ring.py, 0 of 420 non-equivalent mutants survive. The decoder
byte-identical to c94ecaa90; the wall refuses its engine, numpy and runner imports by statement; rate lines
from the real engine give the ticks on 7,500 of 7,500 beats (read by round, 4,510 wrong). The schema's lines
match the decoder. All fast checks pass; 138 Tensor24 tests in 10.6 s.
