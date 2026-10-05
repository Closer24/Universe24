"""The triage of the long version for the cut (the brief's Step 2, the owner's word of 2026-10-05): every paragraph,
table, figure and equation of main.tex and every derivation of supplement.tex, as they stand at the long version's
marker paper-long-v1.1 (main 441b2399), is tagged CORE (the short main text, with its section), SUPPORT (the linked
supplement, with its provisional new number) or OUT (the technical report in the archive, with its section); every
row of paper/claims.md inherits the tag of its place, the exceptions named by row. The script prints
paper/claims_triage.md from the three maps below and the claims table; it changes no text of the paper and no
number. Run with

    python paper/general_formula/claims_triage.py > paper/claims_triage.md

The budgets it sets the sums against are the owner's: the main text 30 pages in Springer's class in total (about
630 words of running text per page, a reference about one twelfth of a page, the floats apart) and the supplement
at most 40 pages in the same class.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
MAIN_TEX = HERE / "main.tex"
SUPPLEMENT_TEX = HERE / "supplement.tex"
CLAIMS = PAPER / "claims.md"

CORE, SUPPORT, OUT = "CORE", "SUPPORT", "OUT"

# The short version's sections, as the approved outline of Step 1 holds them with the owner's words of the day.
SHORT_SECTIONS = {
    "1": "Introduction (2.5 pages)",
    "1.1": "The question and the claim",
    "1.2": "What the paper adds, and its precursors",
    "1.3": "Why the world is read in clicks",
    "1.4": "How to read the paper: the status words, and Table 1 (the claims)",
    "2": "The model and the rule (5 pages)",
    "2.1": "The lattice and its group of 48 (Fig. 1)",
    "2.2": "Rule3 and the vacuum band (Eq. 1, Fig. 2)",
    "2.3": "The paces and the one assumption (Eqs. 2, 3)",
    "2.4": "The write, the readings, the interval and the postulates",
    "2.5": "The click: the meeting and the NodeDetector (Fig. 3)",
    "2.6": "The implementation and the pins",
    "3": "Exact properties (4 pages)",
    "3.1": "Reversibility (Theorem 1)",
    "3.2": "What the acts can form (Theorem 2)",
    "3.3": "The conserved form (Theorem 3, Eq. 4)",
    "3.4": "The count is the record's share (Theorem 4, Eq. 5)",
    "3.5": "The Wronskian as the charge (Eq. 6)",
    "3.6": "The three exact bands",
    "4": "The families, the bodies and the clusters: what the algebra builds (2.5 pages; the owner's word of 2026-10-05)",
    "4.1": "Families, holders and this world's file (Table 2)",
    "4.2": "The bound body: the fixed point and its stability (Proposition 1), and the atom as a body",
    "4.3": "A body's clicks: the invariant and Planck's relation (Eq. 7), the clock's rate, the resonance, the count",
    "4.4": "Clusters: the three kinds of binding, the click between clusters, the cosmology at small redshift",
    "5": "The formulas: the ones shared with nature and the ones the paper adds (3.5 pages)",
    "5.1": "The formulas shared with nature (Table 3; Eqs. 8 to 11; Fig. 5)",
    "5.2": "The formulas the paper adds, and the criterion of refutation (Table 4)",
    "6": "The two slits: the one run against its blind (4 pages; Fig. 4)",
    "6.1": "The file",
    "6.2": "What the model says it must give, and the run",
    "7": "Bell and GHZ under the declared credit (3 pages; Eqs. 12, 13)",
    "7.1": "The file",
    "7.2": "What the model says it must give",
    "8": "Limits and what fails (1.5 pages)",
    "8.1": "The misses, with their numbers",
    "8.2": "What is put in",
    "8.3": "What a world closer to nature needs",
    "9": "Conclusion, with the outlook (0.5 pages)",
    "S&D": "Statements and Declarations (0.5 pages)",
    "refs": "References (3 pages, about 36 entries)",
}

# The technical report's sections (the OUT material, in the archive beside the paper).
REPORT_SECTIONS = {
    "R1": "The method's layers, the procedure of a file and its commands, the rules taken, the computation's budget",
    "R2": "The literature in full (the four paragraphs of the long version's Section 2)",
    "R3": "The engine's derivation table and the implementation's versions of the click's write (old S.61, S.62)",
    "R4": "The hypotheses under their own names, in full (the conversion click, the carrier, confinement, the nuclear holders, the record's parts as particles, the masses as families, the bodies' criterion, the closure candidate, the frozen Node and the black hole's quanta)",
    "R5": "The gates of the click's write (the anticoincidence, the Zeno effect, the shelved ion's telegraph)",
    "R6": "What can follow from here, and how to compute it (the inspiration section)",
    "R7": "The summaries the short text drops as repetition, and the atoms' table beyond hydrogen",
}

# The map of main.tex (at main 441b2399): (first line, the place, tag, destination, note). A row of claims.md at a
# line belongs to the entry with the greatest first line at or below it.
MAIN_MAP = [
    (1, "the preamble", CORE, "main", "the preamble is rewritten for Springer's class"),
    (
        70,
        "the abstract",
        CORE,
        "main abstract",
        "the abstract of Step 1, amended by the Boss's notes (fixed by two clicks; the predictions' conditions) and the title's three parts",
    ),
    (
        77,
        "Introduction / The question",
        CORE,
        "main 1.1",
        "cut to the thesis, the one claim, the criterion sentence, the declaration sentence and 'one world built by the method'",
    ),
    (
        79,
        "Introduction / The words (the glossary)",
        SUPPORT,
        "supp front",
        "the thirteen lines go to the supplement's front with the old name beside the new; the five kept terms are defined in line at first use",
    ),
    (
        96,
        "Fig. 1, the lattice and the octahedron",
        CORE,
        "main Fig. 1",
        "redrawn at Springer's text width",
    ),
    (
        100,
        "Related work / What this paper adds",
        CORE,
        "main 1.2",
        "the three things, the attributions (the exponential metric, the shadow) and 'the backward reading fixes no number', compressed",
    ),
    (102, "Related work / Why the world is read in clicks", CORE, "main 1.3", "compressed"),
    (
        104,
        "Related work / The rule in one line (Eq. 1)",
        CORE,
        "main 2.2",
        "Eq. 1 and its explanation, as they stand",
    ),
    (
        117,
        "Fig. 2, the method's three layers",
        OUT,
        "report R1",
        "the figure and its script stay in the archive",
    ),
    (
        118,
        "Related work / The three layers of the method",
        OUT,
        "report R1",
        "one sentence of it in 1.2",
    ),
    (
        119,
        "Related work / The formulas derived",
        CORE,
        "main 5.1",
        "the list becomes the rows of Table 3",
    ),
    (
        121,
        "Related work / What stands, and on what",
        CORE,
        "main 1.2",
        "the five things fold into 1.2 and Table 1",
    ),
    (
        123,
        "Related work / What is put in, and the three kinds of claim",
        CORE,
        "main 8.2",
        "the inputs named (the one assumption, the credit, line (1) of the atom, the selective read, the energy line, the file's numbers); the three kinds become Table 1's status words",
    ),
    (
        125,
        "Related work / How a Universe24 file is built and tested",
        SUPPORT,
        "supp S.8 (the procedure of a file, from this paragraph)",
        "the procedure and the [999, 1000] example to the supplement; the commands and the install line to report R1",
    ),
    (
        127,
        "Table 1 of the long version, the results",
        CORE,
        "main Table 1",
        "rebuilt as the claims table with its status column over every claim of the short text",
    ),
    (
        164,
        "Related work / How to read the paper (the key)",
        CORE,
        "main 1.4",
        "the eight marks, the two fences and the tables' words in half a page; the LLM sentence",
    ),
    (
        166,
        "Related work / Nomenclature",
        SUPPORT,
        "supp front",
        "the table whole, at the supplement's front; gate 6 reads it there",
    ),
    (
        252,
        "Related work / Reversible cellular automata and digital physics",
        CORE,
        "main 1.2",
        "one paragraph of precursors from the four, about twenty citations kept; the rest to report R2",
    ),
    (254, "Related work / Time-symmetric accounts of measurement", CORE, "main 1.2", "as above"),
    (
        256,
        "Related work / Bell's theorem and local models",
        CORE,
        "main 7.2",
        "Pearle's road and the loophole-free tests, three sentences",
    ),
    (
        258,
        "Related work / Discrete gravity and its tests",
        CORE,
        "main 1.2",
        "as the precursors' paragraph; Collins and Mattingly with the Link's bound in 5.1",
    ),
    (260, "The model (the section's head)", CORE, "main 2", ""),
    (264, "The model / The lattice", CORE, "main 2.1", "the box, the faces, the receding face"),
    (
        268,
        "The model / The group and its action",
        CORE,
        "main 2.1",
        "the group of 48, the owner's word: kept whole",
    ),
    (271, "The model / The NodeState", CORE, "main 2.1", ""),
    (273, "The model / Families and records", CORE, "main 4.1", "compressed with 6.1 to 6.6"),
    (275, "The model / Rule3", CORE, "main 2.2", ""),
    (
        276,
        "Fig. 3 of the long version, the bands",
        CORE,
        "main Fig. 2",
        "redrawn at Springer's text width",
    ),
    (
        279,
        "The model / the vacuum line and the band",
        CORE,
        "main 2.2",
        "Klein-Gordon, Schroedinger's limit, E = m* c_m^2 = omega_0",
    ),
    (
        284,
        "The model / The paces (Eq. 2)",
        CORE,
        "main 2.3",
        "the roundings of the law to supp S.5 (old S.34)",
    ),
    (
        294,
        "The model / The one assumption of the forms",
        CORE,
        "main 2.3",
        "hN = 1, fixed by two clicks (R424), the exponential metric with its attribution; the shadow's discussion to 5.2",
    ),
    (296, "The model / The band at a pace (Eq. 3)", CORE, "main 2.3", ""),
    (
        303,
        "The model / The guard",
        SUPPORT,
        "supp S.4 (old S.3)",
        "two sentences stay in 2.3: the guard is the Courant-Friedrichs-Lewy condition checked at load; under the composed paces no Link closes",
    ),
    (
        305,
        "The model / The write, the readings and the interval",
        CORE,
        "main 2.4",
        "the one write, the three readings, the four acts, compressed",
    ),
    (
        314,
        "The model / What is conserved, and where",
        SUPPORT,
        "supp S.7 (old S.55)",
        "one sentence stays in 3.3: the conservations are per family, and neither layer keeps a total energy",
    ),
    (316, "The model / The postulates", CORE, "main 2.4", "the seven as one list"),
    (
        320,
        "The model / The implementation",
        CORE,
        "main 2.6",
        "the pins (1fe3790a, 1.1.0), the archive, the gate; the run's numbers move to 6.2; the commands to report R1",
    ),
    (
        322,
        "The model / The rules taken",
        CORE,
        "main 2.6",
        "one sentence: there are many worlds to build under the rule, and this paper builds one; the rest to report R1",
    ),
    (
        324,
        "The model / The computation is elementary",
        OUT,
        "report R1",
        "one sentence stays in 6.2: the lattice's budget (Link / R)^2 and sqrt(n) / A",
    ),
    (326, "Exact properties (the section's head)", CORE, "main 3", ""),
    (
        330,
        "Exact properties / Reversibility (Theorem 1)",
        CORE,
        "main 3.1",
        "the theorem, the gate's MATCH sentence, the condition on the reads",
    ),
    (
        344,
        "Exact properties / What the acts can form (Theorem 2)",
        CORE,
        "main 3.2",
        "the theorem's statement and the three tests of a line, compressed",
    ),
    (
        354,
        "Exact properties / The conserved form (Theorem 3, Eq. 4)",
        CORE,
        "main 3.3",
        "the remainders' term and the weights' change to supp S.15 (old S.5)",
    ),
    (
        367,
        "Exact properties / The momentum flux and the tension",
        SUPPORT,
        "supp S.17 (old S.7)",
        "one sentence stays in 3.3: the momentum flux is the wave's own stress, and light gravitates by its pressure",
    ),
    (
        383,
        "Exact properties / The count is the record's share (Theorem 4, Eq. 5)",
        CORE,
        "main 3.4",
        "the share identity to supp S.15",
    ),
    (
        397,
        "Exact properties / The signed integers",
        SUPPORT,
        "supp S.16 (old S.6)",
        "one sentence stays in 3.4: the total share is non-negative under the two conditions",
    ),
    (
        399,
        "Measurement (the section's head)",
        CORE,
        "main 2.5",
        "the click as the division act on the shares, compressed",
    ),
    (
        403,
        "Measurement / Events, and no waves",
        CORE,
        "main 2.5",
        "compressed to the future, the past and the cancelled future",
    ),
    (
        405,
        "Measurement / The click is the meeting (Assumption 1)",
        CORE,
        "main 2.5",
        "Assumption 1 kept whole; the two kinds of NodeDetector",
    ),
    (
        413,
        "Measurement / The click, algebraically",
        CORE,
        "main 2.5",
        "the state space, the bijection, the click as the pair (R, t) drawn by the shares; the rest to supp S.9 (old S.50)",
    ),
    (
        415,
        "Measurement / One bilinear form for every click, two credit rules",
        CORE,
        "main 7.1",
        "the pairing through the root, the joint share never a local square; the two credit rules in one sentence in 2.5",
    ),
    (
        417,
        "Fig. 4 of the long version, the click at a NodeDetector",
        CORE,
        "main Fig. 3",
        "the caption cut to the five numbered steps",
    ),
    (
        419,
        "Measurement / The NodeDetector's declaration (Assumption 2)",
        CORE,
        "main 2.5",
        "compressed to its six facts: the region of two Nodes or more at half a wavelength; the declared window; the unit W_c; the credit by the shares over every NodeDetector under the world's one draw; one click per quantum; the write at one Node",
    ),
    (
        422,
        "Measurement / what produces a click, the draw, Born's rule as a declaration",
        SUPPORT,
        "supp S.9 (old S.50)",
        "one sentence stays in 2.5: Born's rule is the NodeDetector's declaration and no finding of the model; the generator's uniformity and the scatter to the supplement",
    ),
    (
        425,
        "Measurement / the uncertainty relation, the NodeDetector as a face",
        SUPPORT,
        "supp S.9 (old S.50)",
        "one sentence stays in 2.5: the uncertainty relation is the NodeDetector's three declarations and no rule of its own",
    ),
    (
        427,
        "Measurement / The NodeDetector is one declaration kind",
        SUPPORT,
        "supp S.9 (old S.50)",
        "the record's own unit W_rec, the lifetime's hazard, the own clock",
    ),
    (
        429,
        "Measurement / The click decides in the credit and writes at one Node (Assumption 3)",
        CORE,
        "main 2.5",
        "compressed to the write at the drawn Node, the hole, the front inside the light cone, the backward reading as the one non-local place",
    ),
    (
        432,
        "Measurement / antibunching, no signal, the window, the emission",
        SUPPORT,
        "supp S.9 (old S.50)",
        "two sentences stay in 2.5: one click per record (antibunching) follows from the one draw; the direction of time belongs to the clicks and not to the lattice",
    ),
    (
        439,
        "Measurement / Only a click moves a quantum between families",
        SUPPORT,
        "supp S.9 (old S.50)",
        "the derived statement; the hypothesis gets its one line in the outlook of 9",
    ),
    (
        441,
        "Measurement / The sign is the rotation sense (Eq. 6)",
        CORE,
        "main 3.5",
        "the Wronskian as the charge, its conservation, the dimension decides who reads the sign holder; antimatter and the shears to supp S.40 (old S.33)",
    ),
    (
        451,
        "Measurement / Light is born by the write",
        CORE,
        "main 2.5",
        "three sentences; the star's reading to supp S.12 (old S.42)",
    ),
    (455, "Measurement / The price of locality", CORE, "main 7.2", "the three prices, compressed"),
    (
        457,
        "Measurement / The formulas of clicks (Table 2 of the long version)",
        SUPPORT,
        "supp section: the formulas of clicks",
        "the rows that are formulas shared with nature (the clock's rate, the bending's clicks, the absorption line, emission, no signalling, Bell, GHZ, magnetism, a body's count) fold into Table 3; the two-slit row and the arrival into 5.2; the rest to the supplement",
    ),
    (
        485,
        "The families (the section's head and How a family enters)",
        CORE,
        "main 4.1",
        "compressed; the families are part of the algebra by the owner's word, a section of their own with the bodies and the clusters",
    ),
    (491, "The families / The exact bands", CORE, "main 3.6", "the theorem and its two sentences"),
    (
        497,
        "The families / The rule's own universe (Table 3 of the long version)",
        CORE,
        "main 4.1 and Table 2",
        "the four families' rows compressed to Springer's width; the integers' paragraph",
    ),
    (
        517,
        "Table 4 of the long version, the choices",
        SUPPORT,
        "supp section: the choices of this world",
        "cited from 4.1",
    ),
    (
        537,
        "The families / What each family carries, and how gravity enters",
        CORE,
        "main 2.3",
        "how gravity enters in three steps; the shapes to supp S.9",
    ),
    (
        541,
        "The families / The reach of a holder, and the binding holder",
        CORE,
        "main 4.1",
        "Yukawa's reach from the gap; the binding holder's pair and range as the file's choice; gravity weak by E_g; the rest to supp S.42 (old S.11)",
    ),
    (
        551,
        "The families / The vacuum content",
        CORE,
        "main 4.1",
        "60 declared above two floors that no click reads, in four sentences; GW170817's comparison a row of Table 3; the floors' derivation to supp S.50 (old S.54)",
    ),
    (
        559,
        "The families / The file's numbers, and how the universe was chosen",
        CORE,
        "main 4.1",
        "the principle and the five numbers of physics; the road (i) to (ix) to supp S.50",
    ),
    (565, "Bodies (the section's head)", CORE, "main 4.2", ""),
    (
        569,
        "Bodies / What a body is, and how it is computed",
        CORE,
        "main 4.2",
        "the definition and the four statements, compressed; the iteration to supp S.20 (old S.13)",
    ),
    (
        573,
        "Bodies / Stability (Proposition 1)",
        CORE,
        "main 4.2",
        "the proposition's statement with its mark; the functional and the three consequences to supp S.20",
    ),
    (
        589,
        "Bodies / The two branches, and the status of a standing body",
        CORE,
        "main 4.2",
        "the two branches and the pixel's budget, compressed; no standing body is claimed from a run (also 8.1)",
    ),
    (
        593,
        "Bodies / The atom, known from clicks",
        CORE,
        "main 4.2",
        "the atom as a body of the sign holder with Bohr's form, compressed (the owner's word: the bodies are part of the algebra); the derivation supp S.47 (old S.46); the self-read's 1s a miss of 8.1",
    ),
    (
        595,
        "Bodies / What the atom's clicks give, and what they do not",
        CORE,
        "main 4.3",
        "what a click at the atom gives, in three sentences, and the criterion (what nature splits is a body); the numbers to supp S.48 (old S.60)",
    ),
    (597, "Bodies / A body's clicks (the head)", CORE, "main 5.1", ""),
    (
        599,
        "Bodies / A steady rotation writes no light",
        CORE,
        "main 4.3",
        "compressed; the derivation supp S.12 (old S.42); also a row of Table 3",
    ),
    (
        601,
        "Bodies / The invariant, and the share's drift (Eq. 7)",
        CORE,
        "main 4.3",
        "Planck's relation in the band's form and the drift's one line; the rest to supp S.21 (old S.14)",
    ),
    (607, "Bodies / The clock's click rate", CORE, "main 4.3", "as it stands; also a row of Table 3"),
    (
        609,
        "Bodies / The resonance",
        CORE,
        "main 4.3",
        "compressed to the parametric line and Rabi's rate; the derivations supp S.29 (old S.16) and S.13 (old S.43)",
    ),
    (
        611,
        "Bodies / A body's count in clicks",
        CORE,
        "main 4.3",
        "compressed to the count as the share summed over the Nodes and Millikan's slope T; the rest to supp S.21 (old S.14)",
    ),
    (
        613,
        "Bodies / Clusters: how they enter",
        CORE,
        "main 4.4",
        "as it stands, compressed (the owner's word: the clusters are part of the algebra)",
    ),
    (
        617,
        "Bodies / Dark matter in kind",
        CORE,
        "main 4.4",
        "the derived kind in two sentences; the source's hypothesis one line; the check script named",
    ),
    (619, "Bodies / The clicks between bodies", CORE, "main 4.4", "compressed"),
    (
        621,
        "Bodies / What each thing represents in a cluster",
        CORE,
        "main 4.4",
        "the nesting and the three kinds of binding, as they stand",
    ),
    (
        623,
        "Bodies / The clusters' cosmology",
        CORE,
        "main 4.4",
        "Friedmann's dust equations and Hubble's law at small redshift, compressed; also rows of Table 3; the deceleration's sign a miss of 8.1",
    ),
    (
        625,
        "The forms (the section's head and Two potentials, Eq. 8)",
        CORE,
        "main 5.1",
        "the two potentials and the Kepler map, as they stand",
    ),
    (
        633,
        "The forms / (a) to (p), Eqs. 9 to 11",
        CORE,
        "main 5.1",
        "each form one row of Table 3 with its number at [2, 3], nature's bound and its S.n; the bending's and the lens's equations kept",
    ),
    (
        659,
        "Fig. 6 of the long version, the moving clock",
        CORE,
        "main Fig. 5",
        "redrawn at Springer's text width",
    ),
    (
        663,
        "The forms / What goes in and what comes out",
        CORE,
        "main 5.2",
        "the shadow with the EHT numbers, the metric's second order, 'at the rule's own pair the model does not describe the solar system'; magnetism a row of Table 3",
    ),
    (665, "The two slits and Bell (the section's head)", CORE, "main 6", ""),
    (667, "The two slits / The file", CORE, "main 6.1", "as it stands, compressed"),
    (
        668,
        "Fig. 5 of the long version, the two slits' file and row",
        CORE,
        "main Fig. 4",
        "redrawn at Springer's text width",
    ),
    (
        669,
        "Fig. 7 of the long version, the two slits mid-run",
        SUPPORT,
        "supp section: the two slits",
        "a lattice diagnostic; the supplement's figure",
    ),
    (
        671,
        "The two slits / What the model says it must give",
        CORE,
        "main 6.2",
        "the blind 273, the real line 284.7, the run 285 at both seeds, the walk, the chi-square, the maxima, the arrival, the transmission; the refinement sequence's detail to supp S.51 (old S.23)",
    ),
    (673, "Bell / The file (Eq. 12)", CORE, "main 7.1", ""),
    (
        679,
        "Bell / What the model says it must give (Eq. 13)",
        CORE,
        "main 7.2",
        "the four lines, 478 / 169, Tsirelson, GHZ's -4, no signalling, the gate-joined bodies as the largest miss",
    ),
    (693, "Discussion (the section's head)", CORE, "main 5.1", ""),
    (
        695,
        "Discussion / The constants (Eq. 11)",
        CORE,
        "main 5.1",
        "G as a reading, alpha's form, charge universality, the two forces' ratio, the units and the Link's bound, each a row of Table 3 or Table 4; the energy line and the dithered level to supp S.35 (old S.26)",
    ),
    (702, "Discussion / What the lattice fixes with no number", SUPPORT, "supp S.50 (old S.54)", ""),
    (
        706,
        "Discussion / The calibration series and Table 5 of the long version",
        SUPPORT,
        "supp S.50 (old S.54)",
        "one sentence in 8.2: every coefficient of the file is read from one measurement of nature, none from the lattice",
    ),
    (
        727,
        "Discussion / One prediction untested, one check, one open question",
        CORE,
        "main 5.2",
        "the gravity of light and the two clocks' check are rows of Table 4 and Table 3; Hawking's temperature to report R4",
    ),
    (
        729,
        "Findings (the head) and Lattice readings, not findings",
        SUPPORT,
        "supp S.56 (old S.56)",
        "one sentence in 8.1: nature's mass ratios are not whole, and the [2, 3] values are no finding",
    ),
    (
        733,
        "Findings / The declarations, and the four forces as declared",
        SUPPORT,
        "supp section: the declarations",
        "the nine declarations are Table 1's status words; the four forces as declared to report R4 with one line each in 9's outlook",
    ),
    (
        735,
        "Findings / The model's misses",
        CORE,
        "main 8.1",
        "the list with every number, compressed in words and not in items",
    ),
    (
        737,
        "Findings / The lattice's frame, and its mend as a hypothesis",
        CORE,
        "main 8.1",
        "two sentences; the finding's sentence in 8.1 points to supp S.54 (old S.35) and to report R4, where the five forms tried stand (old S.36)",
    ),
    (
        739,
        "Findings / The strong force, by derivation",
        OUT,
        "report R4",
        "the binding bound's miss one line in 8.1 with supp S.49 (old S.38) behind it",
    ),
    (
        741,
        "Findings / The weak force",
        CORE,
        "main 8.1",
        "the four misses in one sentence; the conversion's mechanics to report R4",
    ),
    (743, "Findings / The gaps in two columns", CORE, "main 8.1", "one sentence"),
    (
        745,
        "Findings / The record's parts are its particles",
        OUT,
        "report R4",
        "one line in 9's outlook",
    ),
    (
        747,
        "Findings / Open",
        SUPPORT,
        "supp S.55 (the open items, from this paragraph)",
        "the Fermi-LAT width finding one line in 8.1; the telegraph to report R5",
    ),
    (
        749,
        "Findings / Where a click happens: declared, and open in its cause",
        CORE,
        "main 8.1",
        "two sentences: the cause of a click is open; the recoil is the NodeDetector's",
    ),
    (
        751,
        "Findings / Also open, and the atom",
        CORE,
        "main 8.1",
        "helium 1.4 percent, positronium 44 percent, no line for Pauli's exclusion; the rest to supp S.57",
    ),
    (
        753,
        "Findings / What building a world closer to nature needs",
        CORE,
        "main 8.3",
        "the eight calculations as one compact list (the owner's standing decision); the box's and Gamma's axes to supp S.57",
    ),
    (755, "Conclusion / The contribution", CORE, "main 9", "compressed"),
    (
        759,
        "Conclusion / The mechanism",
        OUT,
        "report R7",
        "repeats 2; dropped as repetition after moving",
    ),
    (
        761,
        "Table 6 of the long version, the formulas the paper adds",
        CORE,
        "main Table 4",
        "the rows a click reads; the frozen content, the deceleration, the binding bound and the booking identity to the supplement's rows",
    ),
    (784, "Conclusion / What is new", CORE, "main 5.2", "compressed"),
    (786, "Conclusion / The claim, and its limits", CORE, "main 9", "compressed"),
    (788, "Conclusion / Outlook", CORE, "main 9", "with the conjectures at one line each"),
    (790, "Statements and Declarations", CORE, "main S&D", "as the long version has them"),
    (
        796,
        "The bibliography",
        CORE,
        "main refs",
        "the entries a kept sentence cites, about 36; the rest with their sentences to the supplement's list or report R2",
    ),
]

# The map of the supplement's derivations (old S.n at main 441b2399): tag, destination, note. The new numbers are
# provisional, in the order of the short version's sections, and are fixed at Step 3's build.
SUPP_MAP = {
    "front": (
        SUPPORT,
        "supp front",
        "the title, the note, the LLM paragraph; the Nomenclature and the glossary join it",
    ),
    "path": (SUPPORT, "supp front", "the path from Rule3 to each result, renumbered"),
    "S.1": (SUPPORT, "supp S.2", "the band at a pace"),
    "S.2": (SUPPORT, "supp S.3", "light's index"),
    "S.3": (SUPPORT, "supp S.4", "the guard, with the main's paragraph"),
    "S.4": (SUPPORT, "supp S.1", "the cube's group of 48, first by the owner's word"),
    "S.5": (SUPPORT, "supp S.15", "the share's change is the currents"),
    "S.6": (SUPPORT, "supp S.16", "the total share non-negative"),
    "S.7": (SUPPORT, "supp S.17", "the tension of a plane wave, with the momentum flux"),
    "S.8": (SUPPORT, "supp S.10", "the reading factor and the draw's scatter"),
    "S.9": (SUPPORT, "supp S.19", "the Wronskian's conservation"),
    "S.10": (SUPPORT, "supp S.52", "Bell under the declared credit"),
    "S.11": (SUPPORT, "supp S.42", "the reach of a holder"),
    "S.12": (SUPPORT, "supp S.44", "the two speeds"),
    "S.13": (SUPPORT, "supp S.20", "the bound body"),
    "S.14": (SUPPORT, "supp S.21", "the invariant and the drift"),
    "S.15": (SUPPORT, "supp S.28", "the clock's click rate"),
    "S.16": (SUPPORT, "supp S.29", "the resonance"),
    "S.17": (SUPPORT, "supp S.45", "the cross current"),
    "S.18": (SUPPORT, "supp S.23", "the fall"),
    "S.19": (SUPPORT, "supp S.24", "the post-Newtonian parameters"),
    "S.20": (SUPPORT, "supp S.25", "the bending and Shapiro's delay"),
    "S.21": (SUPPORT, "supp S.26", "the moving clock"),
    "S.22": (SUPPORT, "supp S.27", "de Broglie"),
    "S.23": (SUPPORT, "supp S.51", "the fringe, with the refinement sequence"),
    "S.24": (SUPPORT, "supp S.38", "the Link's bound"),
    "S.25": (SUPPORT, "supp S.34", "Newton's constant"),
    "S.26": (SUPPORT, "supp S.35", "the fine-structure constant, the energy line"),
    "S.27": (SUPPORT, "supp S.36", "the units and the gap"),
    "S.28": (SUPPORT, "supp S.30", "the lens"),
    "S.29": (SUPPORT, "supp S.46", "the clusters' cosmology, with the clusters' paragraphs of the main"),
    "S.30": (SUPPORT, "supp S.32", "the shadow"),
    "S.31": (SUPPORT, "supp S.6", "the two clocks"),
    "S.32": (SUPPORT, "supp S.18", "the Link factor's two witnesses"),
    "S.33": (SUPPORT, "supp S.40", "magnetism, with antimatter and the shears"),
    "S.34": (
        SUPPORT,
        "supp S.5",
        "the composed paces and the exponential metric, with the law's roundings",
    ),
    "S.35": (SUPPORT, "supp S.54", "the preferred-frame parameters"),
    "S.36": (
        OUT,
        "report R4",
        "the carrier's five forms tried: the mend of the lattice's frame is a hypothesis, and its five forms a side track; 7.1 keeps the finding's sentence and points to the report",
    ),
    "S.37": (OUT, "report R4", "confinement, a hypothesis under its own name"),
    "S.38": (SUPPORT, "supp S.49", "the mass defect and the binding bound"),
    "S.39": (SUPPORT, "supp S.43", "the gapped holder's kernel"),
    "S.40": (SUPPORT, "supp S.53", "GHZ"),
    "S.41": (
        SUPPORT,
        "supp S.41",
        "the gravity of light and the two-path check; the frozen Node's open question to report R4",
    ),
    "S.42": (SUPPORT, "supp S.12", "what a body writes into the holder of the sign"),
    "S.43": (SUPPORT, "supp S.13", "the two-mode line under the rotation"),
    "S.44": (SUPPORT, "supp S.37", "the two forces' ratio"),
    "S.45": (OUT, "report R4", "the nuclear holder, a hypothesis under its own name"),
    "S.46": (SUPPORT, "supp S.47", "the atom with the nucleus's angle alone"),
    "S.47": (SUPPORT, "supp S.33", "the equivalence principle between families"),
    "S.48": (SUPPORT, "supp S.14", "the proofs of the theorems"),
    "S.49": (
        SUPPORT,
        "supp front",
        "the words, trimmed to the glossary with the old names beside the new",
    ),
    "S.50": (
        SUPPORT,
        "supp S.9",
        "the click and the NodeDetector, with the main's moved paragraphs; trimmed of repetition",
    ),
    "S.51": (SUPPORT, "supp S.11", "why there is entanglement, and its scope"),
    "S.52": (OUT, "report R4", "the bodies' criterion, with the forces as declared"),
    "S.53": (OUT, "report R4", "the masses as families, a hypothesis"),
    "S.54": (
        SUPPORT,
        "supp S.50",
        "the lattice's properties and the calibration series, with Tables 4 and 5 of the long version",
    ),
    "S.55": (SUPPORT, "supp S.7", "the conservation picture"),
    "S.56": (SUPPORT, "supp S.56", "the explicit findings with their numbers, behind 7.1"),
    "S.57": (
        OUT,
        "report R5",
        "the anticoincidence, a gate of the repository; the Nomenclature's rows that exist for it alone leave with it",
    ),
    "S.58": (SUPPORT, "supp S.31", "the push on a moving record"),
    "S.59": (
        OUT,
        "report R5",
        "the Zeno effect, a gate of the repository; the Nomenclature's rows that exist for it alone leave with it",
    ),
    "S.60": (
        SUPPORT,
        "supp S.48",
        "the atom under two lines, with hydrogen's, helium's and positronium's numbers; the atoms' table beyond them to report R7",
    ),
    "S.61": (
        OUT,
        "report R3",
        "the engine's derivation table; every citation of it that survives the cut becomes a pointer to R3 and its row (no number), the two slits' 674 photons keeping its lattice label with the R3 pointer",
    ),
    "S.62": (OUT, "report R3", "the implementation's versions of the click's write"),
    "S.63": (SUPPORT, "supp S.22", "Schroedinger's equation as the slow limit"),
    "S.64": (OUT, "report R4", "the closure candidate, a side track"),
    "S.65": (SUPPORT, "supp S.39", "the lattice's scale"),
    "closing": (OUT, "report R6", "what can follow from here, the inspiration section"),
}

# The tables' rows of claims.md (section D): the table's default and the rows that go elsewhere, keyed by the
# row's opening words.
TABLE_DEFAULT = {
    "tab:results": (CORE, "main Table 1", "the claims table with its status column"),
    "tab:clicks": (SUPPORT, "supp section: the formulas of clicks", ""),
    "tab:adds": (CORE, "main Table 4", "the formulas the paper adds"),
}
TABLE_ROWS = {
    "Born's rule": (CORE, "main 2.5", "one sentence: Born's rule is the NodeDetector's declaration"),
    "The two-slit row": (CORE, "main 6.2", ""),
    "The arrival and its spread": (CORE, "main 6.2", ""),
    "Bell's pairs": (CORE, "main 7.2 and Table 3", ""),
    "GHZ, three quanta": (CORE, "main 7.2 and Table 3", ""),
    "The clock's click rate": (CORE, "main Table 3", "the redshift's factor"),
    "The bending's clicks": (CORE, "main Table 3", ""),
    "The absorption line": (CORE, "main Table 3", "Rabi's rate"),
    "Emission": (CORE, "main Table 3", ""),
    "The which-way sum": (CORE, "main 7.2", "one sentence of the price of locality"),
    "No signalling": (CORE, "main 7.2 and Table 3", ""),
    "A body's count in clicks": (CORE, "main Table 3", "Millikan's slope"),
    "Magnetism": (CORE, "main Table 3", ""),
    "The frozen content": (SUPPORT, "supp S.41", ""),
    "The clusters' deceleration": (
        CORE,
        "main 4.4 and Table 4",
        "stays in the main by the advisor's word: the abstract names the decelerating cosmology among the misses; its derivation supp S.46",
    ),
    "A body's binding per quantum": (SUPPORT, "supp S.49", "its miss one line of 8.1"),
    "The click's booking identity": (SUPPORT, "supp S.9", ""),
}

WORDS_PER_PAGE = 630  # running text in Springer's class, measured on the long version (74 pages of text for 46,430 words)
ENTRIES_PER_PAGE = 12  # references in Springer's class, measured on the long version
MAIN_BUDGET_PAGES = 30
SUPP_BUDGET_PAGES = 40


def words(s: str) -> int:
    s = re.sub(r"\\(cite|ref|label|texttt|url|href)\{[^}]*\}", " ", s)
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    s = re.sub(r"\$[^$]*\$", " X ", s)
    return len(s.split())


def main_entry(line: int) -> tuple:
    chosen = MAIN_MAP[0]
    for entry in MAIN_MAP:
        if entry[0] <= line:
            chosen = entry
    return chosen


def main_words_by_entry() -> dict[int, int]:
    """The words of main.tex between an entry's first line and the next entry's."""
    lines = MAIN_TEX.read_text(encoding="utf-8").split("\n")
    starts = [e[0] for e in MAIN_MAP] + [len(lines) + 1]
    out = {}
    for k, start in enumerate(starts[:-1]):
        out[start] = words("\n".join(lines[start - 1 : starts[k + 1] - 1]))
    return out


def supplement_words() -> dict[str, int]:
    t = SUPPLEMENT_TEX.read_text(encoding="utf-8")
    body = t[t.index(r"\begin{document}") :]
    parts = re.split(r"(\\section\*\{[^}]*\})", body)
    out = {"front": words(parts[0])}
    n = 0
    for i in range(1, len(parts), 2):
        ders = re.split(r"(\\begin\{derivation\}\[[^\]]*\])", parts[i + 1])
        pre = words(ders[0])
        if "path from Rule3" in parts[i]:
            out["path"] = pre
        elif "What can follow" in parts[i]:
            out["closing"] = pre
        for j in range(1, len(ders), 2):
            n += 1
            out[f"S.{n}"] = words(ders[j + 1])
    return out


def claims_rows() -> dict[str, list[list[str]]]:
    rows: dict[str, list[list[str]]] = {}
    sec = None
    for text_line in CLAIMS.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^## ([A-E])\.", text_line)
        if m:
            sec = m.group(1)
            continue
        is_row = text_line.startswith("| ") and not text_line.startswith(("| #", "| S ", "|---"))
        if sec and is_row:
            rows.setdefault(sec, []).append([c.strip() for c in text_line.strip().strip("|").split("|")])
    return rows


def main() -> None:
    out = sys.stdout
    mw = main_words_by_entry()
    sw = supplement_words()
    rows = claims_rows()
    print("# The triage of the long version for the cut (Step 2)", file=out)
    print(file=out)
    print(
        "Built by `paper/general_formula/claims_triage.py` from `main.tex`, `supplement.tex` and `claims.md` at the long "
        "version's marker `paper-long-v1.1` (main 441b2399). Every place of the long version carries one tag: CORE, the short "
        "main text, with its section of the approved outline; SUPPORT, the linked supplement, with its provisional new "
        "derivation number; OUT, the technical report in the archive, with its section. Every row of `claims.md` inherits the "
        "tag of its place, and the exceptions are named by row. The tags move text and never a number: the short version's "
        "every number is the long version's, the checker's rule. The owner's words of 2026-10-05 govern the tags: the main "
        "text 30 pages in Springer's class in total; the heart in five parts (the one line with the click as the meeting, the "
        "known formulas reached from Rule3, the formulas the paper adds, one world built by the method and others to build, "
        "the algebra with the group of 48); the title's three parts as the sentence the paper rides on.",
        file=out,
    )
    print(file=out)
    print(
        "## 1. The short version's sections, the supplement's shape and the report's sections", file=out
    )
    print(file=out)
    print("| Main text | Section |", file=out)
    print("|---|---|", file=out)
    for k, v in SHORT_SECTIONS.items():
        print(f"| {k} | {v} |", file=out)
    print(file=out)
    print(
        "The supplement: a front (the note on the language model, the Nomenclature, the glossary of the long version's coined "
        "words with the standard terms beside them, the path from Rule3 to each result), then the SUPPORT derivations renumbered "
        "in the order of the short version's sections, with the paragraphs and tables the main text sheds standing beside the "
        "derivations they belong to.",
        file=out,
    )
    print(file=out)
    print("| Report | Section |", file=out)
    print("|---|---|", file=out)
    for k, v in REPORT_SECTIONS.items():
        print(f"| {k} | {v} |", file=out)
    print(file=out)
    print(
        "## 2. The map of main.tex: every place, its words at the long version, its tag and its destination",
        file=out,
    )
    print(file=out)
    print(
        "| Line | The place in the long version | Words | Tag | Destination | What stays and what moves |",
        file=out,
    )
    print("|---|---|---|---|---|---|", file=out)
    sums = {CORE: 0, SUPPORT: 0, OUT: 0}
    for start, place, tag, dest, note in MAIN_MAP:
        w = mw[start]
        sums[tag] += w
        print(f"| {start} | {place} | {w} | {tag} | {dest} | {note} |", file=out)
    print(file=out)
    print("| Tag | Words of the long main text | Of its total |", file=out)
    print("|---|---|---|", file=out)
    total = sum(sums.values())
    for tag in (CORE, SUPPORT, OUT):
        print(f"| {tag} | {sums[tag]} | {100 * sums[tag] / total:.0f} percent |", file=out)
    print(f"| total | {total} | 100 percent |", file=out)
    print(file=out)
    print(
        "## 3. The map of supplement.tex: every derivation, its words, its tag and its destination",
        file=out,
    )
    print(file=out)
    print("| Old | Words | Tag | Destination (the new number provisional) | Note |", file=out)
    print("|---|---|---|---|---|", file=out)
    ssums = {CORE: 0, SUPPORT: 0, OUT: 0}
    for key in ["front", "path"] + [f"S.{n}" for n in range(1, 66)] + ["closing"]:
        tag, dest, note = SUPP_MAP[key]
        w = sw.get(key, 0)
        ssums[tag] += w
        print(f"| {key} | {w} | {tag} | {dest} | {note} |", file=out)
    print(file=out)
    print("| Tag | Words of the long supplement | Of its total |", file=out)
    print("|---|---|---|", file=out)
    stotal = sum(ssums.values())
    for tag in (CORE, SUPPORT, OUT):
        print(f"| {tag} | {ssums[tag]} | {100 * ssums[tag] / stotal:.0f} percent |", file=out)
    print(f"| total | {stotal} | 100 percent |", file=out)
    print(file=out)
    print(
        "The new numbers S.8 and S.55 are taken by two sections the main text sheds, so that the numbering runs 1 to 56 "
        "without a hole: S.8 the procedure of a file (the long version's paragraph at line 125) and S.55 the open items (the "
        "long version's paragraph at line 747); the hypotheses' derivations tagged OUT take no number.",
        file=out,
    )
    print(file=out)
    print("## 4. The sums against the budgets", file=out)
    print(file=out)
    bib_words = mw[796]
    core_text = sums[CORE] - bib_words
    core_pages = core_text / WORDS_PER_PAGE
    supp_in = sums[SUPPORT] + ssums[SUPPORT]
    print(
        f"The CORE places of the long main text hold {sums[CORE]} words, of which the bibliography {bib_words}; the rest, "
        f"{core_text} words of text, tables and captions, is {core_pages:.0f} Springer pages as it stands. The budget is "
        f"{MAIN_BUDGET_PAGES} pages in total: about 22 of running text ({22 * WORDS_PER_PAGE} words), 4.5 of floats, 0.5 of "
        f"Statements and 3 of references (about {3 * ENTRIES_PER_PAGE} entries). So the rewrite of Step 3 compresses the CORE "
        f"text to about {100 * (22 * WORDS_PER_PAGE + 2000) / core_text:.0f} percent of its present words (the floats' words "
        f"counted at about 2,000), with no number and no claim dropped: the repetition (the same statement in the introduction, "
        f"the section and the conclusion), the per-sentence marks (Table 1's column), the pointers' sentences and the long "
        f"parentheses leave.",
        file=out,
    )
    print(file=out)
    print(
        f"The SUPPORT material holds {ssums[SUPPORT]} words of the long supplement and {sums[SUPPORT]} words shed by the main "
        f"text, {supp_in} together, {supp_in / WORDS_PER_PAGE:.0f} Springer pages as they stand against the supplement's budget "
        f"of {SUPP_BUDGET_PAGES}; the rewrite compresses it to {100 * SUPP_BUDGET_PAGES * WORDS_PER_PAGE / supp_in:.0f} percent, "
        f"the repetition between the main's moved paragraphs and the derivations they join (the click's passage, the bodies, "
        f"the calibration) being the first to leave; a derivation's steps are kept whole, and a derivation that will not fit is "
        f"moved whole to the report and named here, never shortened in its steps.",
        file=out,
    )
    print(file=out)
    print(
        f"The OUT material holds {sums[OUT]} words of the main text and {ssums[OUT]} of the supplement, "
        f"{sums[OUT] + ssums[OUT]} words for the report; nothing is deleted without being moved.",
        file=out,
    )
    print(file=out)
    print(
        "If the supplement's build at Step 3 exceeds 40 pages after the repetition leaves, the next derivations move whole to "
        "the report, fewest pointers first (the mathematician's order, 5991556261, by the load each carries in the frozen "
        "paper): old S.55 (the conservation picture), old S.51's second half (the scope of entanglement beyond the pair), old "
        "S.42 (c) (the monopole's departure), old S.39's part beyond Yukawa's form, old S.26 (d') (the energy line, a declared "
        "line), and old S.43 (the two-mode line under the rotation) last and only if the five before it do not suffice, its "
        "two table rows then citing the report. The six hold about 3,270 words, about 5 pages. A derivation is never shortened "
        "in its steps.",
        file=out,
    )
    print(file=out)
    print("## 5. The rows of claims.md with their tags", file=out)
    print(file=out)
    print("### A. The marked claims of the main text (200)", file=out)
    print(file=out)
    print("| # | Line | Place | Marks | Tag | Destination | The claim |", file=out)
    print("|---|---|---|---|---|---|---|", file=out)
    counts = {}
    for r in rows["A"]:
        n, line, place, marks = r[0], int(r[1]), r[2], r[3]
        e = main_entry(line)
        counts[e[2]] = counts.get(e[2], 0) + 1
        print(f"| {n} | {line} | {place} | {marks} | {e[2]} | {e[3]} | {r[7][:120]} |", file=out)
    print(file=out)
    print("| Tag | Marked claims |", file=out)
    print("|---|---|", file=out)
    for tag in (CORE, SUPPORT, OUT):
        print(f"| {tag} | {counts.get(tag, 0)} |", file=out)
    print(file=out)
    print("### D. The tables' rows (54)", file=out)
    print(file=out)
    print("| # | Table | Status | Tag | Destination | The row |", file=out)
    print("|---|---|---|---|---|---|", file=out)
    dcounts = {}
    for r in rows["D"]:
        n, table, status, row_text = r[0], r[1], r[2], r[5]
        tag, dest, note = TABLE_DEFAULT[table]
        for key, val in TABLE_ROWS.items():
            if row_text.startswith(key):
                tag, dest, note = val
        dcounts[tag] = dcounts.get(tag, 0) + 1
        print(f"| {n} | {table} | {status} | {tag} | {dest} | {row_text[:110]} |", file=out)
    print(file=out)
    print("| Tag | Table rows |", file=out)
    print("|---|---|", file=out)
    for tag in (CORE, SUPPORT, OUT):
        print(f"| {tag} | {dcounts.get(tag, 0)} |", file=out)
    print(file=out)
    print("### C. The supplement's derivations (65)", file=out)
    print(file=out)
    print("| Old | Status | Tag | Destination | Title |", file=out)
    print("|---|---|---|---|---|", file=out)
    for r in rows["C"]:
        key, title, status = r[0], r[2], r[3]
        tag, dest, note = SUPP_MAP[key]
        print(f"| {key} | {status} | {tag} | {dest} | {title[:100]} |", file=out)
    print(file=out)
    print("### E. The sentences named by hand as claims (3)", file=out)
    print(file=out)
    print("| # | Line | Tag | Destination | The sentence |", file=out)
    print("|---|---|---|---|---|", file=out)
    for r in rows["E"]:
        n, line = r[0], int(r[1])
        e = main_entry(line)
        print(f"| {n} | {line} | {e[2]} | {e[3]} | {r[4][:120]} |", file=out)
    print(file=out)
    print("### B. The unmarked candidate sentences (239), by their paragraphs", file=out)
    print(file=out)
    print(
        "These carry no mark and are no claims of the paper; each follows its paragraph's tag, counted here by tag so that the checker sees none is lost.",
        file=out,
    )
    print(file=out)
    bcounts = {}
    for r in rows["B"]:
        e = main_entry(int(r[1]))
        bcounts[e[2]] = bcounts.get(e[2], 0) + 1
    print("| Tag | Candidate sentences |", file=out)
    print("|---|---|", file=out)
    for tag in (CORE, SUPPORT, OUT):
        print(f"| {tag} | {bcounts.get(tag, 0)} |", file=out)
    print(file=out)
    print("## 6. The exceptions by row", file=out)
    print(file=out)
    print(
        "A row whose tag is not its paragraph's: the rows of Table 2 of the long version listed in section D above with a "
        "destination of their own (the formulas shared with nature go to Table 3, the two-slit row and the arrival to 6.2, "
        "Born's rule, the which-way sum and no signalling to their sentences); the four rows of Table 6 that go to the "
        "supplement (the frozen content, the clusters' deceleration, the binding bound, the booking identity). No marked claim "
        "of section A leaves its paragraph: where a paragraph is SUPPORT or OUT and the note names a sentence that stays, that "
        "sentence is restated in the main text with its mark in Table 1 and its claim row keeps the paragraph's tag here.",
        file=out,
    )
    print(file=out)
    print("## 7. The restatements the main text carries (the advisor's word, 5991473123)", file=out)
    print(file=out)
    print(
        "Six sentences of SUPPORT or OUT paragraphs are restated in the main text with their marks, their rows keeping the "
        "paragraph's tag here: (1) rows 50, 54, 55 and 56 of section A, one quantum and one click per record between far "
        "NodeDetectors, the write is the NodeDetector's act, the direction of time belongs to the clicks and not to the lattice, "
        "only a click moves a quantum between families, each one sentence of 2.5 with its mark and a row of Table 1; (2) row 173, "
        "charge universality by construction, a row of Table 3 with the measurement a comparison; (3) row 25, neither layer keeps "
        "a total energy, one sentence of 8.1 or 8.2; (4) row 164, no number comes from the lattice itself, one sentence of 8.2; "
        "(5) rows 175 to 178, the declarations condensed to one item each with its mark in 8.2; (6) rows 189 to 191, the nuclear "
        "binding's misses with their numbers in 8.1 (the deuteron by 4 above, iron by 6 below, the size law R proportional to 1 / A "
        "against A to the one third) with the pointer to report R4 and to the binding bound's derivation. The clusters' "
        "deceleration (row 52 of section D) stays in the main, in Table 4 or as 4.4's sentence with its number. The citations of "
        "old S.61 that survive the cut become pointers to report R3 and its row, and the Nomenclature's rows that exist for old S.57 "
        "and S.59 alone leave with them (the mathematician's conditions (c) and (d), 5991556261).",
        file=out,
    )


if __name__ == "__main__":
    main()
