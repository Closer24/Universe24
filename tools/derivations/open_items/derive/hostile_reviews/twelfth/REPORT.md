# The twelfth hostile review: Animate's decoder after the seventh review (ac2f5689f, 69eb983f9, 06c823ca2)

Verdict: approve with changes (a fresh reader, 02:5x UTC 2026-10-29). 06c823ca2 and 69eb983f9 stand. ac2f5689f mends
every case the seventh review found, and needs six changes, all in the decoder, which is Animate's; the Boss asked them
of her on #2187 with the two probes they need. Each claim stands on a probe the reader ran; the probes stay in the
reader's scratch (decision 26), named below, and their case labels (A1, C1 and so on) are row15_and_guards.py's.

## Required, all Animate's

1. **The tool raises on an unnamed `ends` or `children` field** (decoder/records.py:134-141, `off()`, which walks
   them on every line where the schema names them on Whole alone). A rate, split, turnover, books, header or end line
   holding `"ends": [1]`, `"children": "x"` or `"ends": -1` raises AttributeError or TypeError, and the tool exits 1
   with a traceback (C1 to C5, D1; 132 of 80,000 fuzzed records, 1 of 1,500 tool runs). The fix reads the sites and
   Spokes of `ends` and `children` on whole clicks alone, and the count rule on the kinds whose record has a count;
   it ends two false refusals with them (C6, a rate line's unnamed `ends` off the board; C7, a books line's unnamed
   count 0).
2. **The tool raises on a field's name that is no printable label** (records.py:233 puts it raw into the cause, the
   tool's line 55 prints it): a key `"\ud800"` holding a float raises UnicodeEncodeError (D2), and a key holding a
   line feed forges a second "not read" line (D3). The fix names the field as `ascii(name)[1:-1]`; a plain name reads
   as before.
3. **Row 15's first reading closes on a click whose own holdings make windings** (books.py:46-58, `closes()`, summing
   holding by holding): train 1's one holding (7 to 4) listed twice in a take pays for 6 windings laid where train 1
   gave 3 (A1), and one train taken 7 to 4 and laid 100 to 103 in one part closes (A2). The fix reads each part's
   books per train, each train once in the taken and once in the laid (or chained), and reads any other click not
   read, named.
4. **The verdict's order against its own docstring** (books.py:141-142 against :16-18): a click whose books open
   beside a ledger read at no round with a click reads not read, where the docstring says not shown (B1, B2). The fix
   reads the gap after the failing part, or rewords the docstring, and pins either.
5. **A whole click with no train of its own reads shown** (books.py:56 skips the own-train check, where books.py:6-7
   states it outright and records.py:12-13 reads a reading that needs an absent field as not read; A5). The fix makes
   `legible()` ask the click's train, or names the train optional as q is, and pins it.
6. **The tests miss all 25 of the reader's mutants** (mutants_s13.py), each survivor shown reading a witness
   otherwise than the head:
   - the value rules' lower sides (a site and a Spoke below 0), a child's site, a line's own round, site and count on
     every kind but rate;
   - absent fields a mutant turns into raises (an end without its rounds, an end or a child without its site, an end
     without its Spoke, a train card without its index);
   - a kind that is no label, an unnamed mapping not walked, a lawful unnamed row refused;
   - the books' bounds one side each (a taken holding that keeps its windings, a laid one that gains nothing, q below
     the windings that left), the click without its train, q summed over a pair's ends, the verdict's order;
   - clicks lines holding a train the header lacks (the seventh's own mutant, ported faithfully);
   - the ticks at count 0 (clocks.py:48);
   - the tool over more than one click (every click read against the first Node-clock, counts matched backward, the
     last read printed first, a click of 0 ticks not counted, the last unread click named first).

   The fix: rows in the tests' broken, open and lacking lists, one list read with no raise, and one tool run of three
   clicks at two Node-clocks. The decoder's test file stands at 588 lines under the cap of 600 for a new file; a second
   file of its tests takes its own budget (decision 26) on Animate's word.

## Follow-ups

- **Animate's item 3, each reading held against 0:** acceptable as the schema stands, and stricter than part C's "the
  change equals the booked", differing only where a click books integers out of the trains. Owed from the plan: a word
  that a Books line moves no wind out of the trains, or row 15 reads Books lines into the booked (A8). Unsettled with
  it: whether q counts the windings that left or the quanta laid (A6), and whether a pair's q is per end or for both
  (A7).
- **The library past the digits' limit** raises naming an off-board site of a board whose sides multiply past 4,300
  digits (records.py:139, C8; the tool lifts the limit and does not raise): name the board by its sides.
- **Values unchecked:** holdings and q below 0 read shown (A3, A4); the sides [2, -1, -1] read as a board of two
  sites (C9); a train card without its index is left out of every train of the header (C10); a holding that does not
  change reads open, lawful or not.
- **69eb983f9's wording** became the file's budget under decision 26, and ENGINE.md's sentence went with it.

## What holds

- 06c823ca2's three gate files blob for blob scribe-5 6199bb040; ac2f5689f's five files those of reader-5 4072b42b6
  (gate_blobs.out).
- The seventh's probes on the new text: decoder_readings.py reads every case as the plan and the schema say, the empty
  digest aside, which the plan allows; decoder_precedence.py and decoder_tests_s8_run.py broke on their fixtures and
  their old anchors, and, adapted, read as the plan says, 17 of 18 ported mutants dying by the 75 tests
  (s7_decoder_readings_rerun.out, s7_precedence_adapted.py, s7_tests_rerun.py).
- Animate's 114 mutants on the head: 0 survive (animate_mutants_rerun.out).
- Across 80,000 fuzzed records and ledgers and 1,500 tool runs, every raise is change 1 or 2, none above 0.5 s; an
  empty file, a lone line feed, a header alone, an end alone, carriage returns, bytes that are no UTF-8, a NUL in a
  path and a folder are each named (fuzz_guards.py, fuzz_tool.out).
- 4,000 clicks at one Node-clock at half the full rate in 0.39 s for the whole tool, four times as many in 1.50 s, the
  ticks matching the count (speed.py).
- The gate with amendment 4: refusals 0, notes 2, none in the decoder or the tool; one-change copies with a 2, a
  float or a true division in the tool, or the engine's step, the runner, numpy, a table, a clamp or a module's state
  in the decoder are refused (gate_laws.py). No byte that is not ASCII and no run of three capitals (text_rules.py).
- The six tests of 69eb983f9's room held exactly its lines, each the first to fail on one of Animate's mutants
  (room.py). The fast checks and the 298 Tensor24 tests pass (fast_checks.out, pytest_tensor24.out).
