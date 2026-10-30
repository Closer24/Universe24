# The law's check by script, and the sweep of the code and the documents (2026-10-30)

The owner's ask of 2026-10-30, 07:5x UTC, directly to Sofer (in Hebrew, in translation): "Check every document, every code that was written, that there is no contradiction to the laws.. and check the laws with a script that there is no contradiction among them."

## A. The script: scribe_law_check.py

tools/derivations/open_items/scribe_law_check.py reads docs/ALGEBRA.md and runs four checks, each by a table it holds; its self-test (`--selftest`) has 42 cases, 0 parted; `--arch ROOT` reads the trace table of docs/ARCHITECTURE.md against a tree (every path and test it names must be there). Usage: `python -I scribe_law_check.py [--all] [--selftest] [--write-known] [--docs]`; exit 0 when nothing stands beyond the known list, 1 when a finding is new; `--docs` reads the nine live documents (README.md, llms.txt and docs/ but the law) by the same table of pairs, each against the law's governing line, with a ceiling per document and pair (scribe_law_check_docs_known.json), and refuses a count above it.

- **STRUCTURE (S1 to S7):** the fixed length of 1,960 lines, the final newline, ASCII, no tab or trailing space; every clause (a paragraph opening with a bold name) closes its bold marks, parentheses (an interval [0, w) spared), brackets and double quotes; no clause name stands twice (the preface: "the body holds every formula once"); a heading stands alone.
- **REFERENCES (R1 to R6):** every line cited exists; a line cited beside a clause name is that clause; every anchor linked is a heading; Postulates 1 to 7 each defined once and no other cited; no decision past 43.
- **IDENTITIES (I1 to I5):** the 24 are the cube's rotations and the 48 those and their 24 mirror images (the owner's definition); the five kinds' sizes square to 24; the star has six Spokes; the metric's square has ten slots.
- **PAIRS (P01 to P17):** a table of contradicting statements, a stale row of the old engine against the law of the new core that forbids it; a row inside a sentence that marks itself as history (cancelled, struck, former, old engine) is spared; a pair whose governing text has gone is reported moot. The table is the audit of 04:0x (SCRIBE-LAW-AUDIT-1.md) made executable, and it grows with every contradiction a reader finds: P14 to P17 (the width derived against line 100; a dial, a beat count or the state 5 G + 3 against line 92 (4); the ruler's table against decision 41; the log's fire as a mask against the law's clause) came from the four readers of 2026-10-30, 08:3x UTC.

**What a script cannot do:** prove that no two sentences of prose disagree. It reads what its tables name; a contradiction no table names is found by a reader, enters a table, and is found at every later run.

## B. The result on the law at scribe-5

**Repaired at once** (three lines, exact old and new text, 1,960 lines kept): line 1165 said "the 48 rotations" and now says the 48 are the 24 rotations and their 24 mirror images; line 1786 linked an anchor no heading gives (the bold name beside it stays); line 187 held a stray closing parenthesis for a semicolon.

**Known, standing until the owner's word** (scribe_law_check_known.json; 32 lines in 8 checks, printed at every run; the old engine is out of the tree and the body re-cut of 2026-10-30 took out the rest of what the script names, so the rows that stand are dated history that the script's window does not reach, or wait for the owner):

| check | what | lines | in the core (1 to 110) |
|---|---|---|---|
| P01 | an integer root named as a code primitive (largest_below and its kin), against line 100 and decision 41 | 8 | |
| P05 | the time gear's exponential memo, against decision 41 | 4 | |
| P07 | a declaration as a status, against line 35 | 2 | |
| P10 | real arithmetic in a reading, against line 100 | 8 | |
| P11 | a special rule for a horizon or a frozen clock, against decision 40 (a) and the owner's 07:1x word | 7 | |
| P13 | the old spring D / W = 2 / Gamma, against decisions 40 (e) and 41 | 1 | 35 |
| P14 | the width derived (the law's older clause), against line 100 | 1 | |
| S6 | a clause name that stands twice (1079) | 1 | |

The lines of each check are in `python -I scribe_law_check.py --all`. **1 of the 32 stands in the law's new core** (line 35, the old spring D / W = 2 / Gamma, P13): it waits on the owner's rule for the head's notch and is never spared by the script. **The body re-cut** (2026-10-30, 10:5x UTC, the old engine being out of the tree by the owner's words of 09:2x and 09:3x to Animate and the Boss, on his words of 07:1x and 09:0x and his standing "Delete"; six read-only readers by line ranges, each edit an exact old and new text counted once in its line, applied by one script with the line count and every untouched line checked): 125 edits on 99 lines, 1,960 lines kept, the law check from 133 rows in 14 checks to 32 in 8 and no new finding. What was taken out, by kind (the former text standing in git at 054cdfe86 and named in the law's closing section): the integer root by search (largest_below) wherever a phrase could go, the exponential memo repeated beside the slot form, real arithmetic in a reading (the float checks), the horizon and the frozen load as a rule (BH-S1's rule, the frozen mask, the release by the turn of its own time), the width derived, a declaration as a status (read as decided on line 35's closing form, as an assumption on line 8's word, or struck), the old engine's acts table. The form defects were mended by the move of a word, the removal of a bold mark from a pointer, or the closing of a parenthesis: S5 three, S7 one, S6 eleven of twelve. The rows that stand, by the readers' judgment each checked here:

**Sixteen rows that wait for the owner** (a row is one line and one check; the recommendation is to strike each to a one-line stub that keeps the name others cite, the text standing in git):

| line | check | what and why |
|---|---|---|
| 1045 | P01 | The window turn's integer form is one chain on roots ('k largest_below(P^2) div (R s_d)', precision (iii) 'once per window was a root ... |
| 1124 | P01 | Step 2's integer form starts the sine recurrence at (0, largest_below(R^2 (den^2 - num^2)) div den) and takes 'one root per window' (not matched by the script), so cutting only the root leaves 'R cos and R sin ... |
| 1886 | P01 | Item 50's two-quadrature turn is written as k times an integer root of P^2 (largest_below in five places) and the item is cited as item 50 at eight lines, so no clean cut exists and the owner says whether the form is struck or re-derived root-free. |
| 336 | P05 | The numbers 0.015, 0.146, 1.09 and 1.5 and the edge (Gamma / 2) ln 2 = 0.3466 Gamma are computed from the exponential memo p_0 = Gamma (1 - 1 / Gamma)^c, so deleting the memo leaves them unsupported and re-deriving them under the slot form is not mine to invent. |
| 352 | P05 | The sentence derives the old spring D / w = 2 / Gamma from the clock's factor per notch of load p_0 = Gamma (1 - 1 / Gamma)^c, the same clause as line 35's P13 that waits on the owner's rule for the head's notch, so deleting the memo alone leaves the spring resting on it. |
| 699 | P05 | The first sentence defines the exponential clock p_0 and derives it by Cauchy's equation, every later result of the clause (the index e^(2 U), the 5.4366 m shadow, beta = gamma = 1) hangs on it, and W = the rest + c is the tick's weight g^00 and not p_0, so no one-phrase rewrite exists; the owner ... |
| 1640 | P05 | Row 3 is the exponential time gear itself (the p_0 formula, its derivation by composition and its status), line 1634's alignment says rows 1 to 4 stand, and the core gives no formula to put in its place, so only striking the row (a change at line 1634) or a new rule conforms it. |
| 1212 | P10 | the clause derives all six variants by the paper's real line (its script two_slits_real_line.py), so variant (E)'s numbers (the grid's step 0.0025, the largest departure 0.0012, the ratio within 0.0018) are real-arithmetic outputs: deleting the phrase 'in real arithmetic with Rule3's coefficients' ... |
| 1417 | P10 | the old generator's route (the before notch set mode by mode in real arithmetic, rounded once), its test against a real-arithmetic oracle and the misplaced-wind numbers measured with it (1.2 x 10^-2 against 1.2 x 10^-4 and the rest) are one story, and deleting it strands 'open by the choice' in the ... |
| 1640 | P10 | 'Rounded once' is the same exponential p_0 of row 3 (see P05), so no phrase mends it alone. |
| 1328 | P11 | the clause name 'A collapse ends in a frozen clock' is cited by name at lines 693 and 1757 (rule 4 bars its deletion) and the body is a result under the exponential composed rates that line 90 and decision 40 (a) now leave to the metric's own gears, so the owner decides whether the clause goes ... |
| 1610 | P11 | The line is the horizon rule itself and the check matches its bold name, which lines 90 and 106 cite, so only striking the whole clause together with those two citations clears it: strike it, or keep it as the record those lines ... |
| 1757 | P11 | Row (q2) is the old engine's black hole as a frozen Node-clock with an entropy against the area law, and it is cited as (q2) at lines 448 and 1832, so no small cut exists and only the owner can strike it or send it to be re-derived. |
| 1909 | P11 | Item (7) is BH-S1's mask for a Mesh at factor 0 (the owner's word of 2026-10-27, built at 87a168c16): cutting it orphans 'Three acts of the same word' and David's harness result 'without acts 7 and 12' (13 against 38 bits), while cutting only the mask's name leaves the act, so the owner picks. |
| 35 | P13 | The clause 'The time gear's spring is the clock's one notch' holds the old spring D / W = 2 / Gamma (with the pair (den - den div Gamma, den) of line 352) and the exponential memo beside it, and what replaces the head's notch waits on the owner's rule, so no edit is proposed. |
| 1079 | S6 | The name heads line 142 (the short pointer to the engine-5.0 draw, which the core's line 92 cites) and this long clause, and 25 lines of the law and 9 other documents (21 mentions, UNIVERSE24.md and FURTHER_RESEARCH.md meaning this one) cite it, so keeping it here changes the core's line 92 and ... |

**Sixteen rows kept** (dated history marked by its own words beyond the script's window of 260 characters, or a false positive; nothing to change):

| line | check | why it stands |
|---|---|---|
| 354 | P01 | The sentence is the builder's dated finding of 2026-10-24 on the old engine's born amplitude, in a clause whose own Alignment of 2026-10-25 reads 'history as written' (and the key amplitude 'struck ... |
| 356 | P01 | The same dated finding of 2026-10-24, in a paragraph whose own Alignment of 2026-10-25 reads 'history as written (the top tier's file); kept by name', a mark the check's window does not reach. |
| 462 | P01 | isqrt(T / 2) only records how that dated finding's pixel was set in the old engine's world; the paragraph is kept by name and dated history is not touched. |
| 1039 | P01 | 'what was: the detector's own quantum W_d ... |
| 1653 | P01 | Row 16 is one of the ledger's lines 11 to 25 that the Alignment of 2026-10-25 at line 1634 strikes and keeps by name, so its largest_below is dated history that the check's 260-character window cannot see. |
| 1618 | P07 | Item 1 opens '(to 2026-10-24, 09:4x UTC, kept by name; since that hour no train ...)', so its status is the dated record of the former declaration. |
| 1623 | P07 | False positive: item 6 is the setting, the seed (the start's forms, the packets, the bobs' counts), for which 'declared' stands (line 35, decision 38: the seed is free; line 8: declared is a scale or a seed alone). |
| 360 | P10 | 'rounded once' stands inside the quoted old text of the note 'CHANGED 2026-10-20 ... |
| 428 | P10 | 'rounded once at the read' belongs to 'the hill's weight in the notch's variable, the two forms', kept by name' (the genericity hand's derivation of 2026-10-22), 425 characters before it, which is dated history marked by its own words. |
| 1263 | P10 | false positive: 'rounded once' here is one integer rounding of an old-engine rate in whole numbers, no real arithmetic (the rounded divisions belong to row 4 as a whole, 4.0's by the Alignment of line 1256). |
| 1562 | P10 | The reading belongs to the 2026-10-19 derivation that the line's own clause 'Spin, reopened' (CHANGED 2026-10-24) says 'stands as the record it was', a marker the script's 260-character window does not reach. |
| 1898 | P10 | The real arithmetic and the single rounding describe 4.0's generator in an item that its own dated Alignment marks as 4.0's declared problem by name with its doors struck, so it is history that the check's window cannot see. |
| 132 | P11 | Row at char 11063: a dated build record (08:42 UTC) of the engine-5.0 line, in the clause that says the release by the turn of its own time is that line's build and that the turnover's clause which read FR-S1 as its law is cancelled (2026-10-29), naming the old test's input and stating no rule. |
| 436 | P11 | Row at char 2659: the sentence sits in the swing pair's hard finding of 2026-10-26 inside the clause 'The width is derived', which says of itself 'Struck from the law as a clause by the owner's ruling of 2026-10-26 ... |
| 1820 | P11 | The bullet stands in the closing section The former clauses, kept by name (From The Node, dated), and names BH-S1's test as 'the records' numbers at the hands' heads, not the law', so it states no rule. |
| 436 | P14 | Row at char 2: the heading of the struck clause, which reads 'Struck from the law as a clause by the owner's ruling of 2026-10-26, 22:1x UTC' and 'kept by name' (as line 100 confirms), a mark the check's window does not reach. |

## C. The recommendation for the re-cut

1. **The core first** (the ten rows): each conformed by its exact old and new text to the decisions the owner has already made (27, 35, 40, 41, 42, and his words of 07:1x), the Boss reading the Node-clock's lines.
2. **The body after**, done on 2026-10-30 (the 125 edits above: a line that no longer holds is not in the body, by the preface's own rule; it stands dated in the closing section The former clauses, and the body holds every formula once); what remains is the 32 rows of section B, 16 for the owner's word.
3. The check runs after every law edit and every hour; the known list only falls, and a finding beyond it refuses.

## D. The code (tools/derivations/open_items/scribe_code_census.py, an AST scan, at tensor24-review 9751f91c1, reader-5 0b4fb6d3e, toys-5 f89b76a33)

It counts per file the float literals, the true divisions (a pathlib join spared), the powers with no integer exponent, the imports of math, random, fractions, decimal and statistics, and the calls of a root, an exponential, a logarithm, a circular function, round, float and pow (law line 100: no float anywhere, the probes too; line 102: no circularity). A count is a finding to read, not a verdict.

| the code | files | with a hit | what the hits are |
|---|---|---|---|
| src/tensor24, the new engine | 27 | **0** | the independent scan and the gate agree: none |
| tests/test_the_tensor24_*.py | 17 | 5 | float literals laid on purpose to be refused (18), round (2), math and fractions imported once each, one division |
| tools/*.py | 12 | 3 | check.py and documents_gates.py (timings and percentages: float, round), engine_gates.py (a power) |
| derive/ (the Boss's drafts A to I and their verifiers) | 249 | 160 | fractions, random, float, math: the drafts of 2026-10-28 and 10-29, before the owner's word of 03:4x on the probes |
| derive/david_open | 36 | 29 | the older ones (course, born, click, ladder, twin: float, exp, sqrt, sin, cos; mass, two_boards, tables, gear: fractions, random); the newest c1, c2 and g3 are clean; **t5_trace.py (new) imports fractions and random** |
| ANIMATE-* | 35 | 16 | older probes of the old line (float, sqrt, math, fractions) |

The whole documents branch (tools, src, tests): 1,345 files, 473 with a hit, most of them the old line's hands (tools/derivations/open_items/H-*) and its first scripts. **The gate (scribe_scan.py) reads src/tensor24 and tools/tensor24_*.py and no probe**, so no gate guards the probes.

**Recommendation:** freeze the old probes as the old era's record; let the gate refuse a new or changed probe under derive/ with a float, a root, a circular call, or (if the owner says a Fraction is no whole number) a Fraction, a random or a math import; convert a probe only when a page cites it as evidence of the new core.

## E. The documents

**Mechanical:** 373 citations of a law line (331 plain, 42 named) in the 130 documents of docs/ and tools/derivations/open_items/ name an existing line, and no named citation points at a line that lacks its name (the six the script flags are phrases quoted, each held by its line). The law check's stale patterns, read on the live documents (a sentence marked as history spared): README.md, the horizon (2 lines); docs/ENGINE.md, a root, a parity, the horizon, the old spring (6); docs/FURTHER_RESEARCH.md, a root, a refusal past a range, real arithmetic, the horizon (6); docs/FOLLOW_UP_PAPERS.md (2); docs/CLOCK_WORDS.md (4); docs/BIG_PICTURE.md and llms.txt none.

**By readers** (four read-only readers, 2026-10-30, 08:0x to 08:3x UTC, each reading its documents against the law's digest; every one of the 74 items they listed was checked by the keeper against the document and the law line it cites): README.md, llms.txt and ENGINE.md 25 items; BIG_PICTURE.md 32 (12 in lines 1 to 700, 20 in lines 701 to 1372); CLOCK_WORDS.md, FURTHER_RESEARCH.md, FOLLOW_UP_PAPERS.md and UNIVERSE24.md 17. **Seventy-three of the 74 were real and are mended by exact text** (scribe-5 3c7c46c33 and 1f74f2495): the plan's stale forms replaced by what the law and the build say (the ruler's table and its clamps, the books, the fire mask, the couplings key, the dial, the beat count and the state 5 G + 3, the turnover, the horizon's rule, the backward key, the second carry, the width derived, the key amplitude, a mass set by a pair); the old era's rows marked as record by one paragraph at the head of ENGINE.md, README.md and FURTHER_RESEARCH.md (items 12 and 22 to 25 of reader 2 and item 17 of reader 4 are mended by it); wrong pointers and citations mended (the postulates stand in the law, the law's preface, clause names, law lines); former names mended (Node, Link). **One was left:** reader 3's item 20, BIG_PICTURE.md's "links" in a dated paraphrase of the Boss (the same words stand in law line 35); and the dated ruling of ENGINE.md that says "the setting, the links, the rows" (the rest of reader 2's item 18 is mended).

**The documents' check by script:** `scribe_law_check.py --docs` finds 67 stale lines in 6 of the 9 live documents and none in README.md, llms.txt or BIG_PICTURE.md; they are the old engine's dated entries and ledger rows (UNIVERSE24.md 42, HIGHLIGHTS.md 8, FURTHER_RESEARCH.md 6, ENGINE.md 6, CLOCK_WORDS.md 3, FOLLOW_UP_PAPERS.md 2) and stand under their ceilings; a new stale statement in any of them refuses. **Open, and not the documents':** the law's own transitional rows (the nine in the core; line 35's spring; K-S2 and K-S3's typed parities); the draw's c (law decision 29 says the Node-clock's beat count, which the build has not held since G1b); and the Boss's plan file (TENSOR24_PLAN.md), which still says "the books" and the ruler's table in places (his text, for his next push).
