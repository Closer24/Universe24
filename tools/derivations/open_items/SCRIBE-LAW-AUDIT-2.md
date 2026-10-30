# The law's check by script, and the sweep of the code and the documents (2026-10-30)

The owner's ask of 2026-10-30, 07:5x UTC, directly to Sofer (in Hebrew, in translation): "Check every document, every code that was written, that there is no contradiction to the laws.. and check the laws with a script that there is no contradiction among them."

## A. The script: scribe_law_check.py

tools/derivations/open_items/scribe_law_check.py reads docs/ALGEBRA.md and runs four checks, each by a table it holds; its self-test (`--selftest`) has 34 cases, 0 parted. Usage: `python -I scribe_law_check.py [--all] [--selftest] [--write-known]`; exit 0 when nothing stands beyond the known list, 1 when a finding is new.

- **STRUCTURE (S1 to S7):** the fixed length of 1,960 lines, the final newline, ASCII, no tab or trailing space; every clause (a paragraph opening with a bold name) closes its bold marks, parentheses (an interval [0, w) spared), brackets and double quotes; no clause name stands twice (the preface: "the body holds every formula once"); a heading stands alone.
- **REFERENCES (R1 to R6):** every line cited exists; a line cited beside a clause name is that clause; every anchor linked is a heading; Postulates 1 to 7 each defined once and no other cited; no decision past 43.
- **IDENTITIES (I1 to I5):** the 24 are the cube's rotations and the 48 those and their 24 mirror images (the owner's definition); the five kinds' sizes square to 24; the star has six Spokes; the metric's square has ten slots.
- **PAIRS (P01 to P13):** a table of contradicting statements, a stale row of the old engine against the law of the new core that forbids it; a row inside a sentence that marks itself as history (cancelled, struck, former, old engine) is spared; a pair whose governing text has gone is reported moot. The table is the audit of 04:0x (SCRIBE-LAW-AUDIT-1.md) made executable, and it grows with every contradiction a reader finds.

**What a script cannot do:** prove that no two sentences of prose disagree. It reads what its tables name; a contradiction no table names is found by a reader, enters a table, and is found at every later run.

## B. The result on the law at scribe-5

**Repaired at once** (three lines, exact old and new text, 1,960 lines kept): line 1165 said "the 48 rotations" and now says the 48 are the 24 rotations and their 24 mirror images; line 1786 linked an anchor no heading gives (the bold name beside it stays); line 187 held a stray closing parenthesis for a semicolon.

**Known, standing until the re-cut** (scribe_law_check_known.json; 140 lines in 15 checks, printed at every run; the owner's answer of 04:5x: the old engine is frozen and its rows stand until the re-cut removes them):

| check | what | lines | in the core (1 to 110) |
|---|---|---|---|
| P01 | an integer root named as a code primitive (largest_below and its kin), against line 100 and decision 41 | 38 | 96, 100 |
| P03 | an act from outside the Node-clock, against line 92 (3) | 1 | |
| P04 | the click as an act outside the reversal, against Postulates 2 and 4 | 5 | |
| P05 | the time gear's exponential memo, against decision 41 | 15 | |
| P06 | a refusal past a range, against decision 40 (e) | 3 | |
| P07 | a declaration as a status, against line 35 | 12 | |
| P08 | the swap at the top, against decision 27 (cancelled) | 3 | 80, 92, 98 |
| P09 | a parity rule on Gamma, T or den, against K-S2 and decision 40 (h) | 3 | 100, 110 |
| P10 | real arithmetic in a reading, against line 100 | 21 | |
| P11 | a special rule for a horizon or a frozen clock, against decision 40 (a) and the owner's 07:1x word | 21 | 92 |
| P12 | a bound read as a clamp, against line 106 and decision 40 (e) | 1 | 106 |
| P13 | the old spring D / W = 2 / Gamma, against decisions 40 (e) and 41 | 1 | 35 |
| S5 | a parenthesis unbalanced (348, 799, 1558) | 3 | |
| S6 | a clause name that stands twice (358, 390, 446, 807, 1079, 1326, 1344, 1576, 1578, 1580, 1596, 1598) | 12 | |
| S7 | a heading that carries a clause (1254) | 1 | |

The lines of each check are in `python -I scribe_law_check.py --all`. **Ten of the 140 stand in the law's new core** (lines 1 to 110: 35, 80, 92, 96, 98, 100, 106, 110): they are the rows of the old engine that the new core's own lines still carry.

## C. The recommendation for the re-cut

1. **The core first** (the ten rows): each conformed by its exact old and new text to the decisions the owner has already made (27, 35, 40, 41, 42, and his words of 07:1x), the Boss reading the Node-clock's lines.
2. **The body after** (130 rows and the form defects), section by section beside the engine's cleaning, by the preface's own rule (a line that no longer holds is not in the body; it stands dated in the closing section The former clauses, and the body holds every formula once).
3. The check runs after every law edit and every hour; the known list only falls, and a finding beyond it refuses.

## D. The code and the documents

The sweep of the code and of the documents follows in section E and F of this file as each part closes.
