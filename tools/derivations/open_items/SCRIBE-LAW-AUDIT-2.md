# The law's check by script, and the sweep of the code and the documents (2026-10-30)

The owner's ask of 2026-10-30, 07:5x UTC, directly to Sofer (in Hebrew, in translation): "Check every document, every code that was written, that there is no contradiction to the laws.. and check the laws with a script that there is no contradiction among them."

## A. The script: scribe_law_check.py

tools/derivations/open_items/scribe_law_check.py reads docs/ALGEBRA.md and runs four checks, each by a table it holds; its self-test (`--selftest`) has 38 cases, 0 parted. Usage: `python -I scribe_law_check.py [--all] [--selftest] [--write-known] [--docs]`; exit 0 when nothing stands beyond the known list, 1 when a finding is new; `--docs` reads the nine live documents (README.md, llms.txt and docs/ but the law) by the same table of pairs, each against the law's governing line, with a ceiling per document and pair (scribe_law_check_docs_known.json), and refuses a count above it.

- **STRUCTURE (S1 to S7):** the fixed length of 1,960 lines, the final newline, ASCII, no tab or trailing space; every clause (a paragraph opening with a bold name) closes its bold marks, parentheses (an interval [0, w) spared), brackets and double quotes; no clause name stands twice (the preface: "the body holds every formula once"); a heading stands alone.
- **REFERENCES (R1 to R6):** every line cited exists; a line cited beside a clause name is that clause; every anchor linked is a heading; Postulates 1 to 7 each defined once and no other cited; no decision past 43.
- **IDENTITIES (I1 to I5):** the 24 are the cube's rotations and the 48 those and their 24 mirror images (the owner's definition); the five kinds' sizes square to 24; the star has six Spokes; the metric's square has ten slots.
- **PAIRS (P01 to P17):** a table of contradicting statements, a stale row of the old engine against the law of the new core that forbids it; a row inside a sentence that marks itself as history (cancelled, struck, former, old engine) is spared; a pair whose governing text has gone is reported moot. The table is the audit of 04:0x (SCRIBE-LAW-AUDIT-1.md) made executable, and it grows with every contradiction a reader finds: P14 to P17 (the width derived against line 100; a dial, a beat count or the state 5 G + 3 against line 92 (4); the ruler's table against decision 41; the log's fire as a mask against the law's clause) came from the four readers of 2026-10-30, 08:3x UTC.

**What a script cannot do:** prove that no two sentences of prose disagree. It reads what its tables name; a contradiction no table names is found by a reader, enters a table, and is found at every later run.

## B. The result on the law at scribe-5

**Repaired at once** (three lines, exact old and new text, 1,960 lines kept): line 1165 said "the 48 rotations" and now says the 48 are the 24 rotations and their 24 mirror images; line 1786 linked an anchor no heading gives (the bold name beside it stays); line 187 held a stray closing parenthesis for a semicolon.

**Known, standing until the re-cut** (scribe_law_check_known.json; 133 lines in 14 checks, printed at every run; the owner's answer of 04:5x: the old engine is frozen and its rows stand until the re-cut removes them):

| check | what | lines | in the core (1 to 110) |
|---|---|---|---|
| P01 | an integer root named as a code primitive (largest_below and its kin), against line 100 and decision 41 | 35 | |
| P03 | an act from outside the Node-clock, against line 92 (3) | 1 | |
| P04 | the click as an act outside the reversal, against Postulates 2 and 4 | 5 | |
| P05 | the time gear's exponential memo, against decision 41 | 15 | |
| P06 | a refusal past a range, against decision 40 (e) | 3 | |
| P07 | a declaration as a status, against line 35 | 12 | |
| P09 | a parity rule on Gamma, T or den, against K-S2 and decision 40 (h) | 1 | |
| P10 | real arithmetic in a reading, against line 100 | 20 | |
| P11 | a special rule for a horizon or a frozen clock, against decision 40 (a) and the owner's 07:1x word | 20 | |
| P13 | the old spring D / W = 2 / Gamma, against decisions 40 (e) and 41 | 1 | 35 |
| P14 | the width derived (the law's older clause), against line 100 | 4 | |
| S5 | a parenthesis unbalanced (348, 799, 1558) | 3 | |
| S6 | a clause name that stands twice (358, 390, 446, 807, 1079, 1326, 1344, 1576, 1578, 1580, 1596, 1598) | 12 | |
| S7 | a heading that carries a clause (1254) | 1 | |

The lines of each check are in `python -I scribe_law_check.py --all`. **1 of the 133 stands in the law's new core** (line 35, the old spring D / W = 2 / Gamma, P13): the keeper's re-cut of the core, applied on the owner's "Yes." of 09:0x UTC to question a (8 exact edits on lines 80, 92, 96, 98, 100 and 110, 1,960 lines kept, the word diff read), took the law check from 141 rows to 133 and the core from 9 rows to 1. The history window of the script (a sentence marked as history is spared) was narrowed to the sentence's neighbourhood and the root pattern of P01 to a root named, which removed rows that the law itself marks as its record (line 106's list of the departures of the code, P12) and the over-broad reading of line 100's "each is one primitive"; P13 is never spared, since the clause still stands and waits on the owner's rule for the head's notch.

## C. The recommendation for the re-cut

1. **The core first** (the ten rows): each conformed by its exact old and new text to the decisions the owner has already made (27, 35, 40, 41, 42, and his words of 07:1x), the Boss reading the Node-clock's lines.
2. **The body after** (130 rows and the form defects), section by section beside the engine's cleaning, by the preface's own rule (a line that no longer holds is not in the body; it stands dated in the closing section The former clauses, and the body holds every formula once).
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
