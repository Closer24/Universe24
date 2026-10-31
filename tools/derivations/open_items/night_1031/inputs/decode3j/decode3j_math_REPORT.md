<!-- Boss note, 2026-10-31 12:06 UTC: written by the Boss from the reader's hand-back (the harness refuses report files from readers); the text below is the reader's, whole. Reader of DECODE3j (frozen b343bdec, S/decode3j_frozen), the hostile mathematician (the HALF pair's mathematician). -->

Reader of DECODE3j (frozen b343bdec...), the hostile mathematician (the HALF pair's mathematician). My harness does not let me write report files, so the whole report is below. Please file it as S/decode3j_math/REPORT.md.

My probes are in S/decode3j_math/, each p_*.py with its .txt: p_cuts3j, p_gates3j, p_d4j, p_e4j, p_parse3j, p_parse3j_b and p_sizes3j. The copy I reran from is rerun/ in the same folder.

# The hostile mathematician (HALF pair) on DECODE3j, 2026-10-31

**Read:**
- BRIEF_PAIRS.md to its end, including the owner's laws of 11:47 and 11:52 and their rulings.
- DECODE3j.md, all 371 lines. Its sha256 begins b343bdecf338fa0f, as named.
- decode3j.py, far3j.py, cuts3j.py, readings3j.json, rulings_verbatim.md and the run outputs.

**Checks:**
- FROZEN.sha256: 88 of 88 OK.
- nl_sources.sha256: 35 of 35, before and after my runs.
- bellend.py is Big Pic's frozen copy, byte for byte.
- Section 0's 4 quoted blocks are verbatim in the brief, and its 4 headings are the brief's.

**Reruns:** from the copy, under the live venv's Python 3.14.6 -I -B, nice 19.
- cuts3j.py, decode3j.py (10 min 2 s) and far3j.py each reproduce their outputs byte for byte. No bytecode appeared.
- One conduct slip of mine: far3j's rerun started at load 8.87, because my chained command did not wait. Every later run waited for the load to fall below 8.

I touched no repository or worktree, did not open the other reader's folder, and posted nothing.

VERDICT on DECODE3j: NOT PASSED

(one BLOCKING)

## BLOCKING

**B1. The pair parse at any round joins by order and cannot refuse. A both-form pair's tie becomes the next pair's bearing** (section 3).

- **The rule:**
  - an outcome is joined by the meeting next before it, if one stands since its last outcome;
  - otherwise it is joined by the meeting next after it;
  - a tie that joins a waiting outcome is spent.
- **What follows from it:**
  - A tie that joins nothing stands as the next outcome's bearing. A both-form pair's tie is such a tie, since the pair's bearing already joined its outcome.
  - A tie with two outcomes waiting at one place keeps the last. That is a pick by order, which MIN1's rule refuses.
  - An outcome that no meeting joins vanishes without a word.
- **MEASURED.** The probes are p_parse3j and p_parse3j_b. They run decode3j's own from_lines_joined, mates and r4j on the toy's third click, written per pair event:

| record | pairs read back | sources read back | N_T | click parts |
|---|---|---|---|---|
| P1: after, with 400 pair events given no meeting | 39,600 of 40,000 | one | 66 | SHOWN; nothing refuses |
| P2: two sources, both at every pair event | 40,000 | 20,000 and 20,000 | 90 | SHOWN |
| P3: two sources, both at even t and after at odd t | 40,000, of which 20,000 are joined by the previous pair event's tie | 40,000 at one source | 66 | SHOWN |

  - mates read on every row.
  - Right pair records of the pattern (decode3h's right_pairs): two sources, 3,000 a half, 20 draws.
    - Written both at every event, they read NOT READ 20 of 20, refusing only on 20, because each source holds 1,500 a half.
    - The same draws written alternating both and after read SHOWN 20 of 20, refusing only on 0, at N_T 66.
    - So the writing alone changes the verdict.
- **Why it blocks:**
  - The 10:42 ruling's scope is "before, after or both, at any round", so a record that mixes start-form and end-form pairs is in it.
  - Under the owner's 11:52 law, a pair's connection comes from its start and its end. Read by order, the parse presumes that the joining meeting stands next to the outcomes within the run, and it joins pair t+1 by pair t's end.
- **Fix:**
  - the record names each join: the meeting names its outcomes' round or pair, or the outcome line names its meeting;
  - the parse reads those names, never the order;
  - a meeting that joins no outcome, an outcome joined by none, or two outcomes of one place joined by one meeting is refused by name;
  - then re-measure P3 and the right records.

## MINOR

1. **D4's whitelist refuses honest conversions in the codebase's own style.**
   - MEASURED with decode3j's own d4_whitelist (p_d4j):
     - C-a with a docstring is refused ("a Expr node");
     - C-a with annotations is refused ("the name list outside own()");
     - C-a with a return annotation is refused ("int");
     - C-a doubled, `2 * (...)`, is refused ("a Mult node").
   - My four evasions are refused, and so is own shadowed by a nested def. The keyword C-a is allowed.
   - Fix: allow the leading docstring, skip annotation subtrees, and say where Mult stands.
2. **E4's fall to (e) at B is chance; the curve is its reading.**
   - DERIVED: the late hand gives B a lag-1 correlation of (9/100)(5/32) = 45/3,200. Its z at 20,000 a half is about 3,955, under CUT_FW 11,343.
   - MEASURED (p_e4j, the pair born at 3 to 7):
     - (e) at B refuses only at birth 3, at 11,471, which is 128 over the cut;
     - births 4 to 7 read 3,487 to 7,411 and pass;
     - the curve refuses all five, with 232 to 278 pairs a half landing alike at A 0, B 90, where the pattern's E is -1 exactly.
3. **Under 11:52, the far outcome's reach is no longer a corner.**
   - A start-and-end law is where a cross-event coupling through the outcomes would be laid, and no order part reads it on that path. E3 passes every order part.
   - The candidate sum refuses E3 (329,134 and 281,287, against 40,082) and passes E4.
   - Fix: promote the candidate (one sum per half on 16 degrees, N_T + 2), or name the reach for Big Pic.
4. **The test writers connect the two places by a click within the run.**
   - The toy's second click and right_pairs' draw read both settings (SAME[|b - a|]).
   - rec_end's far click reads the hand the end click left, and the late hand reads the previous event's.
   - Each is unlawful as an act under 11:47 and 11:52, though lawful as a test record.
   - Fix: name this, and write E1 and E2 in the restated (C) form. That form gives the same joint law (DERIVED in my Bell report).
5. **"Refusing only" flags only the ladders' gates.** (a)'s reach and (e)'s lag-1 cells also bar SHOWN without setting it. Name the flag for what it reads, or fold the other two in.
6. **The size rows do not add.**
   - MEASURED (p_sizes3j): 9, 6, 30, 76, 247 (236 + 4 + 7) and 39, the text's own figures.
   - ladder_gate, exp_neg_up and ambiguous (41 lines) stand in both R2's row and R4's, and worst (6) in both the precedence's and R4's. So 47 lines are counted twice.
7. **Two checks whose no no row shows.**
   - "The limit" is dominated by the curve wherever R4 can read SHOWN. At 2,500 a half, fair, a record that passes the curve keeps S under about 2.85, while the limit refuses only past about 3.03 (DERIVED from the cuts). Yet it costs a test in N_T.
   - R2's reversed reading counts the same four pairs at L = 1 as the forward one (DERIVED), and every measured row reads the same both ways.

## SOUND, with numbers

- **The cuts.** p_cuts3j checks them with my own series, written apart from cuts3j and cuts3h:
  - LAGSUM at 66 is 40,082 and 26,827, and at 90 it is 40,999 and 27,605;
  - CUT_FW at 66 is 11,343, and at 90 it is 11,920;
  - each is the least whole thousandth: 0 off.
- **Why 40,082 and not 39,697.** The level fell from 1/1,160 (N_T 58) to 1/1,320 (N_T 66). The least thousandth on 16 degrees is 39,697 at the first level and 40,082 at the second (MEASURED). My E sums are unchanged, and every verdict is the same under both cuts.
- **My DECODE3i B1: met.**
  - Rows 1 to 4 are refused by the new ladders alone ([0, 0, 0] and [0, 0]; [32, 512, 0]; [128, 0]; [0, 0]). So are the physicist's two-sided rows and the parity of the next two.
  - The toy passes, and the flipped form passes as the named reach.
- **The gates' counting.**
  - qexp 6L + 3 and 4L + 2 are DERIVED from the counts per symbol.
  - The product form holds under the null: the settings are free, the outcomes fair, and there is no signal.
- **N_T** = 2 (21 + 12 S), 66 or 90. I counted it part by part against r4j.
- **The rate at 3,000 a half:** SHOWN 974, NOT SHOWN 26, refusing only on 0, reproduced.
- **The gates, re-measured (p_gates3j).** First openings in pair events a half, for (e), the joint past and future, the two-sided joint and the joint of both places:
  - one source, fair, N_T 66: 200, 2,500, 2,500 and 900;
  - two sources, N_T 90: 400, 5,000, 5,000 and 1,800;
  - settings 700/300: 200, 1,300, 1,300 and 500;
  - settings 900/100: 200, 400, 400 and 200.
  - The text's cases hold.
- **The law of the path.** Under 11:47, the refusal by the joint of both places stands: rows 3 and 4 are signals.
- **R2's failing rows** and **D4's refusals** are reproduced.
- **E1 to E4** match the text's table to the count.

## DERIVED / MEASURED / OVERCLAIMED

- **DERIVED, sound:**
  - the qexps;
  - N_T;
  - the reach beyond the windows;
  - the far outcome's reach;
  - the law-of-the-path refusal of signalling laws.
- **MEASURED:** the text's tables, reproduced. Mine are:
  - the parse rows and the right records;
  - D4's honest forms;
  - E4 over five births;
  - the gates, the cuts and the sizes.
- **OVERCLAIMED:**
  - the parse "reads a pair by the meeting that joins it ... at any round", when it reads by order;
  - "E4 falls to (e) at B", stated as a reading when it is chance;
  - "refusing only", stated as the whole of "never SHOWN".

## Under the owner's 11:47 and 11:52 laws

- No R4 part presumes a source for the connection: R4's parts read the record's statistics.
- The joint of both places' law-of-the-path refusal agrees with 11:47.
- The parse presumes a joining meeting next to the outcomes within the run (B1).
- The test writers connect the places by a click within the run (MINOR 4).

## Questions for the Boss

1. Does the record name each join, with the parse refusing an unnamed or doubled join?
2. Under 11:52, does the far-outcome sum become a rule?
3. Does D4 allow a leading docstring and annotations?
4. Are the test writers named stand-ins, with E1 and E2 written in the restated form?

## Solution24 (the reader's line)

R4 now reads both sides and both places at once, and its cuts and gates are right. But its pair parse joins by order, so one pair's end can be read as the next pair's start, against the owner's law that a connection comes from the start and the end. The record must name its joins.
