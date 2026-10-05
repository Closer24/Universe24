# The triage of the long version for the cut (Step 2)

Built by `paper/general_formula/claims_triage.py` from `main.tex`, `supplement.tex` and `claims.md` at the long version's marker `paper-long-v1.1` (main 441b2399). Every place of the long version carries one tag: CORE, the short main text, with its section of the approved outline; SUPPORT, the linked supplement, with its provisional new derivation number; OUT, the technical report in the archive, with its section. Every row of `claims.md` inherits the tag of its place, and the exceptions are named by row. The tags move text and never a number: the short version's every number is the long version's, the checker's rule. The owner's words of 2026-10-05 govern the tags: the main text 30 pages in Springer's class in total; the heart in five parts (the one line with the click as the meeting, the known formulas reached from Rule3, the formulas the paper adds, one world built by the method and others to build, the algebra with the group of 48); the title's three parts as the sentence the paper rides on.

## 1. The short version's sections, the supplement's shape and the report's sections

| Main text | Section |
|---|---|
| 1 | Introduction (2.5 pages) |
| 1.1 | The question and the claim |
| 1.2 | What the paper adds, and its precursors |
| 1.3 | Why the world is read in clicks |
| 1.4 | How to read the paper: the status words, and Table 1 (the claims) |
| 2 | The model and the rule (5 pages) |
| 2.1 | The lattice and its group of 48 (Fig. 1) |
| 2.2 | Rule3 and the vacuum band (Eq. 1, Fig. 2) |
| 2.3 | The paces and the one assumption (Eqs. 2, 3) |
| 2.4 | The write, the readings, the interval and the postulates |
| 2.5 | The click: the meeting and the NodeDetector (Fig. 3) |
| 2.6 | The implementation and the pins |
| 3 | Exact properties (4 pages) |
| 3.1 | Reversibility (Theorem 1) |
| 3.2 | What the acts can form (Theorem 2) |
| 3.3 | The conserved form (Theorem 3, Eq. 4) |
| 3.4 | The count is the record's share (Theorem 4, Eq. 5) |
| 3.5 | The Wronskian as the charge (Eq. 6) |
| 3.6 | The three exact bands |
| 4 | The families, the bodies and the clusters: what the algebra builds (2.5 pages; the owner's word of 2026-10-05) |
| 4.1 | Families, holders and this world's file (Table 2) |
| 4.2 | The bound body: the fixed point and its stability (Proposition 1), and the atom as a body |
| 4.3 | A body's clicks: the invariant and Planck's relation (Eq. 7), the clock's rate, the resonance, the count |
| 4.4 | Clusters: the three kinds of binding, the click between clusters, the cosmology at small redshift |
| 5 | The formulas: the ones shared with nature and the ones the paper adds (3.5 pages) |
| 5.1 | The formulas shared with nature (Table 3; Eqs. 8 to 11; Fig. 5) |
| 5.2 | The formulas the paper adds, and the criterion of refutation (Table 4) |
| 6 | The two slits: the one run against its blind (4 pages; Fig. 4) |
| 6.1 | The file |
| 6.2 | What the model says it must give, and the run |
| 7 | Bell and GHZ under the declared credit (3 pages; Eqs. 12, 13) |
| 7.1 | The file |
| 7.2 | What the model says it must give |
| 8 | Limits and what fails (1.5 pages) |
| 8.1 | The misses, with their numbers |
| 8.2 | What is put in |
| 8.3 | What a world closer to nature needs |
| 9 | Conclusion, with the outlook (0.5 pages) |
| S&D | Statements and Declarations (0.5 pages) |
| refs | References (3 pages, about 36 entries) |

The supplement: a front (the note on the language model, the Nomenclature, the glossary of the long version's coined words with the standard terms beside them, the path from Rule3 to each result), then the SUPPORT derivations renumbered in the order of the short version's sections, with the paragraphs and tables the main text sheds standing beside the derivations they belong to.

| Report | Section |
|---|---|
| R1 | The method's layers, the procedure of a file and its commands, the rules taken, the computation's budget |
| R2 | The literature in full (the four paragraphs of the long version's Section 2) |
| R3 | The engine's derivation table and the implementation's versions of the click's write (old S.61, S.62) |
| R4 | The hypotheses under their own names, in full (the conversion click, the carrier, confinement, the nuclear holders, the record's parts as particles, the masses as families, the bodies' criterion, the closure candidate, the frozen Node and the black hole's quanta) |
| R5 | The gates of the click's write (the anticoincidence, the Zeno effect, the shelved ion's telegraph) |
| R6 | What can follow from here, and how to compute it (the inspiration section) |
| R7 | The summaries the short text drops as repetition, and the atoms' table beyond hydrogen |

## 2. The map of main.tex: every place, its words at the long version, its tag and its destination

| Line | The place in the long version | Words | Tag | Destination | What stays and what moves |
|---|---|---|---|---|---|
| 1 | the preamble | 276 | CORE | main | the preamble is rewritten for Springer's class |
| 70 | the abstract | 255 | CORE | main abstract | the abstract of Step 1, amended by the Boss's notes (fixed by two clicks; the predictions' conditions) and the title's three parts |
| 77 | Introduction / The question | 964 | CORE | main 1.1 | cut to the thesis, the one claim, the criterion sentence, the declaration sentence and 'one world built by the method' |
| 79 | Introduction / The words (the glossary) | 519 | SUPPORT | supp front | the thirteen lines go to the supplement's front with the old name beside the new; the five kept terms are defined in line at first use |
| 96 | Fig. 1, the lattice and the octahedron | 158 | CORE | main Fig. 1 | redrawn at Springer's text width |
| 100 | Related work / What this paper adds | 430 | CORE | main 1.2 | the three things, the attributions (the exponential metric, the shadow) and 'the backward reading fixes no number', compressed |
| 102 | Related work / Why the world is read in clicks | 309 | CORE | main 1.3 | compressed |
| 104 | Related work / The rule in one line (Eq. 1) | 512 | CORE | main 2.2 | Eq. 1 and its explanation, as they stand |
| 117 | Fig. 2, the method's three layers | 155 | OUT | report R1 | the figure and its script stay in the archive |
| 118 | Related work / The three layers of the method | 239 | OUT | report R1 | one sentence of it in 1.2 |
| 119 | Related work / The formulas derived | 295 | CORE | main 5.1 | the list becomes the rows of Table 3 |
| 121 | Related work / What stands, and on what | 333 | CORE | main 1.2 | the five things fold into 1.2 and Table 1 |
| 123 | Related work / What is put in, and the three kinds of claim | 573 | CORE | main 8.2 | the inputs named (the one assumption, the credit, line (1) of the atom, the selective read, the energy line, the file's numbers); the three kinds become Table 1's status words |
| 125 | Related work / How a Universe24 file is built and tested | 523 | SUPPORT | supp section: the procedure of a file | the procedure and the [999, 1000] example to the supplement; the commands and the install line to report R1 |
| 127 | Table 1 of the long version, the results | 1041 | CORE | main Table 1 | rebuilt as the claims table with its status column over every claim of the short text |
| 164 | Related work / How to read the paper (the key) | 489 | CORE | main 1.4 | the eight marks, the two fences and the tables' words in half a page; the LLM sentence |
| 166 | Related work / Nomenclature | 2290 | SUPPORT | supp front | the table whole, at the supplement's front; gate 6 reads it there |
| 252 | Related work / Reversible cellular automata and digital physics | 223 | CORE | main 1.2 | one paragraph of precursors from the four, about twenty citations kept; the rest to report R2 |
| 254 | Related work / Time-symmetric accounts of measurement | 179 | CORE | main 1.2 | as above |
| 256 | Related work / Bell's theorem and local models | 94 | CORE | main 7.2 | Pearle's road and the loophole-free tests, three sentences |
| 258 | Related work / Discrete gravity and its tests | 137 | CORE | main 1.2 | as the precursors' paragraph; Collins and Mattingly with the Link's bound in 5.1 |
| 260 | The model (the section's head) | 35 | CORE | main 2 |  |
| 264 | The model / The lattice | 167 | CORE | main 2.1 | the box, the faces, the receding face |
| 268 | The model / The group and its action | 240 | CORE | main 2.1 | the group of 48, the owner's word: kept whole |
| 271 | The model / The NodeState | 66 | CORE | main 2.1 |  |
| 273 | The model / Families and records | 252 | CORE | main 4.1 | compressed with 6.1 to 6.6 |
| 275 | The model / Rule3 | 179 | CORE | main 2.2 |  |
| 276 | Fig. 3 of the long version, the bands | 212 | CORE | main Fig. 2 | redrawn at Springer's text width |
| 279 | The model / the vacuum line and the band | 354 | CORE | main 2.2 | Klein-Gordon, Schroedinger's limit, E = m* c_m^2 = omega_0 |
| 284 | The model / The paces (Eq. 2) | 489 | CORE | main 2.3 | the roundings of the law to supp S.5 (old S.34) |
| 294 | The model / The one assumption of the forms | 662 | CORE | main 2.3 | hN = 1, fixed by two clicks (R424), the exponential metric with its attribution; the shadow's discussion to 5.2 |
| 296 | The model / The band at a pace (Eq. 3) | 220 | CORE | main 2.3 |  |
| 303 | The model / The guard | 469 | SUPPORT | supp S.4 (old S.3) | two sentences stay in 2.3: the guard is the Courant-Friedrichs-Lewy condition checked at load; under the composed paces no Link closes |
| 305 | The model / The write, the readings and the interval | 428 | CORE | main 2.4 | the one write, the three readings, the four acts, compressed |
| 314 | The model / What is conserved, and where | 341 | SUPPORT | supp S.7 (old S.55) | one sentence stays in 3.3: the conservations are per family, and neither layer keeps a total energy |
| 316 | The model / The postulates | 314 | CORE | main 2.4 | the seven as one list |
| 320 | The model / The implementation | 580 | CORE | main 2.6 | the pins (1fe3790a, 1.1.0), the archive, the gate; the run's numbers move to 6.2; the commands to report R1 |
| 322 | The model / The rules taken | 183 | CORE | main 2.6 | one sentence: there are many worlds to build under the rule, and this paper builds one; the rest to report R1 |
| 324 | The model / The computation is elementary | 166 | OUT | report R1 | one sentence stays in 6.2: the lattice's budget (Link / R)^2 and sqrt(n) / A |
| 326 | Exact properties (the section's head) | 50 | CORE | main 3 |  |
| 330 | Exact properties / Reversibility (Theorem 1) | 455 | CORE | main 3.1 | the theorem, the gate's MATCH sentence, the condition on the reads |
| 344 | Exact properties / What the acts can form (Theorem 2) | 389 | CORE | main 3.2 | the theorem's statement and the three tests of a line, compressed |
| 354 | Exact properties / The conserved form (Theorem 3, Eq. 4) | 480 | CORE | main 3.3 | the remainders' term and the weights' change to supp S.15 (old S.5) |
| 367 | Exact properties / The momentum flux and the tension | 573 | SUPPORT | supp S.17 (old S.7) | one sentence stays in 3.3: the momentum flux is the wave's own stress, and light gravitates by its pressure |
| 383 | Exact properties / The count is the record's share (Theorem 4, Eq. 5) | 471 | CORE | main 3.4 | the share identity to supp S.15 |
| 397 | Exact properties / The signed integers | 250 | SUPPORT | supp S.16 (old S.6) | one sentence stays in 3.4: the total share is non-negative under the two conditions |
| 399 | Measurement (the section's head) | 514 | CORE | main 2.5 | the click as the division act on the shares, compressed |
| 403 | Measurement / Events, and no waves | 256 | CORE | main 2.5 | compressed to the future, the past and the cancelled future |
| 405 | Measurement / The click is the meeting (Assumption 1) | 260 | CORE | main 2.5 | Assumption 1 kept whole; the two kinds of NodeDetector |
| 413 | Measurement / The click, algebraically | 268 | CORE | main 2.5 | the state space, the bijection, the click as the pair (R, t) drawn by the shares; the rest to supp S.9 (old S.50) |
| 415 | Measurement / One bilinear form for every click, two credit rules | 267 | CORE | main 7.1 | the pairing through the root, the joint share never a local square; the two credit rules in one sentence in 2.5 |
| 417 | Fig. 4 of the long version, the click at a NodeDetector | 527 | CORE | main Fig. 3 | the caption cut to the five numbered steps |
| 419 | Measurement / The NodeDetector's declaration (Assumption 2) | 9 | CORE | main 2.5 | compressed to its six facts: the region of two Nodes or more at half a wavelength; the declared window; the unit W_c; the credit by the shares over every NodeDetector under the world's one draw; one click per quantum; the write at one Node |
| 422 | Measurement / what produces a click, the draw, Born's rule as a declaration | 559 | SUPPORT | supp S.9 (old S.50) | one sentence stays in 2.5: Born's rule is the NodeDetector's declaration and no finding of the model; the generator's uniformity and the scatter to the supplement |
| 425 | Measurement / the uncertainty relation, the NodeDetector as a face | 795 | SUPPORT | supp S.9 (old S.50) | one sentence stays in 2.5: the uncertainty relation is the NodeDetector's three declarations and no rule of its own |
| 427 | Measurement / The NodeDetector is one declaration kind | 517 | SUPPORT | supp S.9 (old S.50) | the record's own unit W_rec, the lifetime's hazard, the own clock |
| 429 | Measurement / The click decides in the credit and writes at one Node (Assumption 3) | 17 | CORE | main 2.5 | compressed to the write at the drawn Node, the hole, the front inside the light cone, the backward reading as the one non-local place |
| 432 | Measurement / antibunching, no signal, the window, the emission | 1845 | SUPPORT | supp S.9 (old S.50) | two sentences stay in 2.5: one click per record (antibunching) follows from the one draw; the direction of time belongs to the clicks and not to the lattice |
| 439 | Measurement / Only a click moves a quantum between families | 409 | SUPPORT | supp S.9 (old S.50) | the derived statement; the hypothesis gets its one line in the outlook of 9 |
| 441 | Measurement / The sign is the rotation sense (Eq. 6) | 718 | CORE | main 3.5 | the Wronskian as the charge, its conservation, the dimension decides who reads the sign holder; antimatter and the shears to supp S.40 (old S.33) |
| 451 | Measurement / Light is born by the write | 323 | CORE | main 2.5 | three sentences; the star's reading to supp S.12 (old S.42) |
| 455 | Measurement / The price of locality | 183 | CORE | main 7.2 | the three prices, compressed |
| 457 | Measurement / The formulas of clicks (Table 2 of the long version) | 821 | SUPPORT | supp section: the formulas of clicks | the rows that are formulas shared with nature (the clock's rate, the bending's clicks, the absorption line, emission, no signalling, Bell, GHZ, magnetism, a body's count) fold into Table 3; the two-slit row and the arrival into 5.2; the rest to the supplement |
| 485 | The families (the section's head and How a family enters) | 357 | CORE | main 4.1 | compressed; the families are part of the algebra by the owner's word, a section of their own with the bodies and the clusters |
| 491 | The families / The exact bands | 203 | CORE | main 3.6 | the theorem and its two sentences |
| 497 | The families / The rule's own universe (Table 3 of the long version) | 675 | CORE | main 4.1 and Table 2 | the four families' rows compressed to Springer's width; the integers' paragraph |
| 517 | Table 4 of the long version, the choices | 423 | SUPPORT | supp section: the choices of this world | cited from 4.1 |
| 537 | The families / What each family carries, and how gravity enters | 529 | CORE | main 2.3 | how gravity enters in three steps; the shapes to supp S.9 |
| 541 | The families / The reach of a holder, and the binding holder | 530 | CORE | main 4.1 | Yukawa's reach from the gap; the binding holder's pair and range as the file's choice; gravity weak by E_g; the rest to supp S.42 (old S.11) |
| 551 | The families / The vacuum content | 453 | CORE | main 4.1 | 60 declared above two floors that no click reads, in four sentences; GW170817's comparison a row of Table 3; the floors' derivation to supp S.50 (old S.54) |
| 559 | The families / The file's numbers, and how the universe was chosen | 615 | CORE | main 4.1 | the principle and the five numbers of physics; the road (i) to (ix) to supp S.50 |
| 565 | Bodies (the section's head) | 132 | CORE | main 4.2 |  |
| 569 | Bodies / What a body is, and how it is computed | 460 | CORE | main 4.2 | the definition and the four statements, compressed; the iteration to supp S.20 (old S.13) |
| 573 | Bodies / Stability (Proposition 1) | 713 | CORE | main 4.2 | the proposition's statement with its mark; the functional and the three consequences to supp S.20 |
| 589 | Bodies / The two branches, and the status of a standing body | 194 | CORE | main 4.2 | the two branches and the pixel's budget, compressed; no standing body is claimed from a run (also 8.1) |
| 593 | Bodies / The atom, known from clicks | 313 | CORE | main 4.2 | the atom as a body of the sign holder with Bohr's form, compressed (the owner's word: the bodies are part of the algebra); the derivation supp S.47 (old S.46); the self-read's 1s a miss of 8.1 |
| 595 | Bodies / What the atom's clicks give, and what they do not | 433 | CORE | main 4.3 | what a click at the atom gives, in three sentences, and the criterion (what nature splits is a body); the numbers to supp S.48 (old S.60) |
| 597 | Bodies / A body's clicks (the head) | 66 | CORE | main 5.1 |  |
| 599 | Bodies / A steady rotation writes no light | 308 | CORE | main 4.3 | compressed; the derivation supp S.12 (old S.42); also a row of Table 3 |
| 601 | Bodies / The invariant, and the share's drift (Eq. 7) | 193 | CORE | main 4.3 | Planck's relation in the band's form and the drift's one line; the rest to supp S.21 (old S.14) |
| 607 | Bodies / The clock's click rate | 80 | CORE | main 4.3 | as it stands; also a row of Table 3 |
| 609 | Bodies / The resonance | 224 | CORE | main 4.3 | compressed to the parametric line and Rabi's rate; the derivations supp S.29 (old S.16) and S.13 (old S.43) |
| 611 | Bodies / A body's count in clicks | 355 | CORE | main 4.3 | compressed to the count as the share summed over the Nodes and Millikan's slope T; the rest to supp S.21 (old S.14) |
| 613 | Bodies / Clusters: how they enter | 126 | CORE | main 4.4 | as it stands, compressed (the owner's word: the clusters are part of the algebra) |
| 617 | Bodies / Dark matter in kind | 259 | CORE | main 4.4 | the derived kind in two sentences; the source's hypothesis one line; the check script named |
| 619 | Bodies / The clicks between bodies | 208 | CORE | main 4.4 | compressed |
| 621 | Bodies / What each thing represents in a cluster | 106 | CORE | main 4.4 | the nesting and the three kinds of binding, as they stand |
| 623 | Bodies / The clusters' cosmology | 172 | CORE | main 4.4 | Friedmann's dust equations and Hubble's law at small redshift, compressed; also rows of Table 3; the deceleration's sign a miss of 8.1 |
| 625 | The forms (the section's head and Two potentials, Eq. 8) | 238 | CORE | main 5.1 | the two potentials and the Kepler map, as they stand |
| 633 | The forms / (a) to (p), Eqs. 9 to 11 | 2168 | CORE | main 5.1 | each form one row of Table 3 with its number at [2, 3], nature's bound and its S.n; the bending's and the lens's equations kept |
| 659 | Fig. 6 of the long version, the moving clock | 152 | CORE | main Fig. 5 | redrawn at Springer's text width |
| 663 | The forms / What goes in and what comes out | 521 | CORE | main 5.2 | the shadow with the EHT numbers, the metric's second order, 'at the rule's own pair the model does not describe the solar system'; magnetism a row of Table 3 |
| 665 | The two slits and Bell (the section's head) | 130 | CORE | main 6 |  |
| 667 | The two slits / The file | 406 | CORE | main 6.1 | as it stands, compressed |
| 668 | Fig. 5 of the long version, the two slits' file and row | 238 | CORE | main Fig. 4 | redrawn at Springer's text width |
| 669 | Fig. 7 of the long version, the two slits mid-run | 161 | SUPPORT | supp section: the two slits | a lattice diagnostic; the supplement's figure |
| 671 | The two slits / What the model says it must give | 949 | CORE | main 6.2 | the blind 273, the real line 284.7, the run 285 at both seeds, the walk, the chi-square, the maxima, the arrival, the transmission; the refinement sequence's detail to supp S.51 (old S.23) |
| 673 | Bell / The file (Eq. 12) | 382 | CORE | main 7.1 |  |
| 679 | Bell / What the model says it must give (Eq. 13) | 760 | CORE | main 7.2 | the four lines, 478 / 169, Tsirelson, GHZ's -4, no signalling, the gate-joined bodies as the largest miss |
| 693 | Discussion (the section's head) | 8 | CORE | main 5.1 |  |
| 695 | Discussion / The constants (Eq. 11) | 1387 | CORE | main 5.1 | G as a reading, alpha's form, charge universality, the two forces' ratio, the units and the Link's bound, each a row of Table 3 or Table 4; the energy line and the dithered level to supp S.35 (old S.26) |
| 702 | Discussion / What the lattice fixes with no number | 200 | SUPPORT | supp S.50 (old S.54) |  |
| 706 | Discussion / The calibration series and Table 5 of the long version | 534 | SUPPORT | supp S.50 (old S.54) | one sentence in 8.2: every coefficient of the file is read from one measurement of nature, none from the lattice |
| 727 | Discussion / One prediction untested, one check, one open question | 231 | CORE | main 5.2 | the gravity of light and the two clocks' check are rows of Table 4 and Table 3; Hawking's temperature to report R4 |
| 729 | Findings (the head) and Lattice readings, not findings | 254 | SUPPORT | supp S.56 (old S.56) | one sentence in 8.1: nature's mass ratios are not whole, and the [2, 3] values are no finding |
| 733 | Findings / The declarations, and the four forces as declared | 860 | SUPPORT | supp section: the declarations | the nine declarations are Table 1's status words; the four forces as declared to report R4 with one line each in 9's outlook |
| 735 | Findings / The model's misses | 442 | CORE | main 8.1 | the list with every number, compressed in words and not in items |
| 737 | Findings / The lattice's frame, and its mend as a hypothesis | 175 | CORE | main 8.1 | two sentences; the five forms tried to supp S.55 (old S.36) |
| 739 | Findings / The strong force, by derivation | 389 | OUT | report R4 | the binding bound's miss one line in 8.1 with supp S.49 (old S.38) behind it |
| 741 | Findings / The weak force | 243 | CORE | main 8.1 | the four misses in one sentence; the conversion's mechanics to report R4 |
| 743 | Findings / The gaps in two columns | 112 | CORE | main 8.1 | one sentence |
| 745 | Findings / The record's parts are its particles | 175 | OUT | report R4 | one line in 9's outlook |
| 747 | Findings / Open | 581 | SUPPORT | supp S.57 (the open items) | the Fermi-LAT width finding one line in 8.1; the telegraph to report R5 |
| 749 | Findings / Where a click happens: declared, and open in its cause | 314 | CORE | main 8.1 | two sentences: the cause of a click is open; the recoil is the NodeDetector's |
| 751 | Findings / Also open, and the atom | 224 | CORE | main 8.1 | helium 1.4 percent, positronium 44 percent, no line for Pauli's exclusion; the rest to supp S.57 |
| 753 | Findings / What building a world closer to nature needs | 759 | CORE | main 8.3 | the eight calculations as one compact list (the owner's standing decision); the box's and Gamma's axes to supp S.57 |
| 755 | Conclusion / The contribution | 361 | CORE | main 9 | compressed |
| 759 | Conclusion / The mechanism | 236 | OUT | report R7 | repeats 2; dropped as repetition after moving |
| 761 | Table 6 of the long version, the formulas the paper adds | 779 | CORE | main Table 4 | the rows a click reads; the frozen content, the deceleration, the binding bound and the booking identity to the supplement's rows |
| 784 | Conclusion / What is new | 173 | CORE | main 5.2 | compressed |
| 786 | Conclusion / The claim, and its limits | 331 | CORE | main 9 | compressed |
| 788 | Conclusion / Outlook | 104 | CORE | main 9 | with the conjectures at one line each |
| 790 | Statements and Declarations | 162 | CORE | main S&D | as the long version has them |
| 796 | The bibliography | 2566 | CORE | main refs | the entries a kept sentence cites, about 36; the rest with their sentences to the supplement's list or report R2 |

| Tag | Words of the long main text | Of its total |
|---|---|---|
| CORE | 37855 | 73 percent |
| SUPPORT | 12924 | 25 percent |
| OUT | 1360 | 3 percent |
| total | 52139 | 100 percent |

## 3. The map of supplement.tex: every derivation, its words, its tag and its destination

| Old | Words | Tag | Destination (the new number provisional) | Note |
|---|---|---|---|---|
| front | 405 | SUPPORT | supp front | the title, the note, the LLM paragraph; the Nomenclature and the glossary join it |
| path | 441 | SUPPORT | supp front | the path from Rule3 to each result, renumbered |
| S.1 | 204 | SUPPORT | supp S.2 | the band at a pace |
| S.2 | 86 | SUPPORT | supp S.3 | light's index |
| S.3 | 317 | SUPPORT | supp S.4 | the guard, with the main's paragraph |
| S.4 | 532 | SUPPORT | supp S.1 | the cube's group of 48, first by the owner's word |
| S.5 | 331 | SUPPORT | supp S.15 | the share's change is the currents |
| S.6 | 252 | SUPPORT | supp S.16 | the total share non-negative |
| S.7 | 81 | SUPPORT | supp S.17 | the tension of a plane wave, with the momentum flux |
| S.8 | 101 | SUPPORT | supp S.10 | the reading factor and the draw's scatter |
| S.9 | 272 | SUPPORT | supp S.19 | the Wronskian's conservation |
| S.10 | 329 | SUPPORT | supp S.52 | Bell under the declared credit |
| S.11 | 160 | SUPPORT | supp S.42 | the reach of a holder |
| S.12 | 112 | SUPPORT | supp S.44 | the two speeds |
| S.13 | 689 | SUPPORT | supp S.20 | the bound body |
| S.14 | 329 | SUPPORT | supp S.21 | the invariant and the drift |
| S.15 | 118 | SUPPORT | supp S.28 | the clock's click rate |
| S.16 | 357 | SUPPORT | supp S.29 | the resonance |
| S.17 | 120 | SUPPORT | supp S.45 | the cross current |
| S.18 | 139 | SUPPORT | supp S.23 | the fall |
| S.19 | 432 | SUPPORT | supp S.24 | the post-Newtonian parameters |
| S.20 | 121 | SUPPORT | supp S.25 | the bending and Shapiro's delay |
| S.21 | 409 | SUPPORT | supp S.26 | the moving clock |
| S.22 | 50 | SUPPORT | supp S.27 | de Broglie |
| S.23 | 77 | SUPPORT | supp S.51 | the fringe, with the refinement sequence |
| S.24 | 235 | SUPPORT | supp S.38 | the Link's bound |
| S.25 | 62 | SUPPORT | supp S.34 | Newton's constant |
| S.26 | 1249 | SUPPORT | supp S.35 | the fine-structure constant, the energy line |
| S.27 | 388 | SUPPORT | supp S.36 | the units and the gap |
| S.28 | 256 | SUPPORT | supp S.30 | the lens |
| S.29 | 324 | SUPPORT | supp S.46 | the clusters' cosmology, with the clusters' paragraphs of the main |
| S.30 | 113 | SUPPORT | supp S.32 | the shadow |
| S.31 | 316 | SUPPORT | supp S.6 | the two clocks |
| S.32 | 199 | SUPPORT | supp S.18 | the Link factor's two witnesses |
| S.33 | 886 | SUPPORT | supp S.40 | magnetism, with antimatter and the shears |
| S.34 | 468 | SUPPORT | supp S.5 | the composed paces and the exponential metric, with the law's roundings |
| S.35 | 514 | SUPPORT | supp S.54 | the preferred-frame parameters |
| S.36 | 603 | OUT | report R4 | the carrier's five forms tried: the mend of the lattice's frame is a hypothesis, and its five forms a side track; 7.1 keeps the finding's sentence and points to the report |
| S.37 | 703 | OUT | report R4 | confinement, a hypothesis under its own name |
| S.38 | 794 | SUPPORT | supp S.49 | the mass defect and the binding bound |
| S.39 | 606 | SUPPORT | supp S.43 | the gapped holder's kernel |
| S.40 | 452 | SUPPORT | supp S.53 | GHZ |
| S.41 | 803 | SUPPORT | supp S.41 | the gravity of light and the two-path check; the frozen Node's open question to report R4 |
| S.42 | 819 | SUPPORT | supp S.12 | what a body writes into the holder of the sign |
| S.43 | 910 | SUPPORT | supp S.13 | the two-mode line under the rotation |
| S.44 | 411 | SUPPORT | supp S.37 | the two forces' ratio |
| S.45 | 817 | OUT | report R4 | the nuclear holder, a hypothesis under its own name |
| S.46 | 684 | SUPPORT | supp S.47 | the atom with the nucleus's angle alone |
| S.47 | 224 | SUPPORT | supp S.33 | the equivalence principle between families |
| S.48 | 606 | SUPPORT | supp S.14 | the proofs of the theorems |
| S.49 | 2226 | SUPPORT | supp front | the words, trimmed to the glossary with the old names beside the new |
| S.50 | 2812 | SUPPORT | supp S.9 | the click and the NodeDetector, with the main's moved paragraphs; trimmed of repetition |
| S.51 | 1078 | SUPPORT | supp S.11 | why there is entanglement, and its scope |
| S.52 | 632 | OUT | report R4 | the bodies' criterion, with the forces as declared |
| S.53 | 461 | OUT | report R4 | the masses as families, a hypothesis |
| S.54 | 626 | SUPPORT | supp S.50 | the lattice's properties and the calibration series, with Tables 4 and 5 of the long version |
| S.55 | 647 | SUPPORT | supp S.7 | the conservation picture |
| S.56 | 1073 | SUPPORT | supp S.56 | the explicit findings with their numbers, behind 7.1 |
| S.57 | 442 | OUT | report R5 | the anticoincidence, a gate of the repository |
| S.58 | 354 | SUPPORT | supp S.31 | the push on a moving record |
| S.59 | 693 | OUT | report R5 | the Zeno effect, a gate of the repository |
| S.60 | 1577 | SUPPORT | supp S.48 | the atom under two lines, with hydrogen's, helium's and positronium's numbers; the atoms' table beyond them to report R7 |
| S.61 | 3424 | OUT | report R3 | the engine's derivation table |
| S.62 | 114 | OUT | report R3 | the implementation's versions of the click's write |
| S.63 | 393 | SUPPORT | supp S.22 | Schroedinger's equation as the slow limit |
| S.64 | 475 | OUT | report R4 | the closure candidate, a side track |
| S.65 | 290 | SUPPORT | supp S.39 | the lattice's scale |
| closing | 1629 | OUT | report R6 | what can follow from here, the inspiration section |

| Tag | Words of the long supplement | Of its total |
|---|---|---|
| CORE | 0 | 0 percent |
| SUPPORT | 28859 | 74 percent |
| OUT | 9993 | 26 percent |
| total | 38852 | 100 percent |

## 4. The sums against the budgets

The CORE places of the long main text hold 37855 words, of which the bibliography 2566; the rest, 35289 words of text, tables and captions, is 56 Springer pages as it stands. The budget is 30 pages in total: about 22 of running text (13860 words), 4.5 of floats, 0.5 of Statements and 3 of references (about 36 entries). So the rewrite of Step 3 compresses the CORE text to about 45 percent of its present words (the floats' words counted at about 2,000), with no number and no claim dropped: the repetition (the same statement in the introduction, the section and the conclusion), the per-sentence marks (Table 1's column), the pointers' sentences and the long parentheses leave.

The SUPPORT material holds 28859 words of the long supplement and 12924 words shed by the main text, 41783 together, 66 Springer pages as they stand against the supplement's budget of 40; the rewrite compresses it to 60 percent, the repetition between the main's moved paragraphs and the derivations they join (the click's passage, the bodies, the calibration) being the first to leave; a derivation's steps are kept whole, and a derivation that will not fit is moved whole to the report and named here, never shortened in its steps.

The OUT material holds 1360 words of the main text and 9993 of the supplement, 11353 words for the report; nothing is deleted without being moved.

If the supplement's build at Step 3 exceeds 40 pages after the repetition leaves, the next derivations move whole to the report, in this order, each named in the pass's map: old S.43 (the two-mode line under the rotation, its result kept as a row of Table 3 with the report cited), old S.42 (c) (the monopole's departure), old S.51's second half (the scope of entanglement beyond the pair), old S.26 (d') (the energy line, a declared line), old S.39 (the gapped holder's kernel beyond Yukawa's form), old S.55 (the conservation picture). A derivation is never shortened in its steps.

## 5. The rows of claims.md with their tags

### A. The marked claims of the main text (200)

| # | Line | Place | Marks | Tag | Destination | The claim |
|---|---|---|---|---|---|---|
| 1 | 77 | sec:intro / The question. | assumption | CORE | main 1.1 | The paper starts from one statement and never contradicts it ([assumption]): Universe24 is the meeting of the past with  |
| 2 | 102 | sec:related / Why the world is read in clicks, and never on the | assumption | CORE | main 1.3 | This is why the paper sets beside nature only what the clicks give: a lattice reading, a level, a support, a count at a  |
| 3 | 123 | sec:related / What is put in, and the three kinds of claim. | assumption,fitted | CORE | main 8.2 | Three choices were made with a known result in view, and the paper states them as inputs, not predictions: the one assum |
| 4 | 128 | sec:related / How a Universe24 file is built and tested. | experiment | CORE | main Table 1 | A calibration is a number taken from nature; [experiment] a number the model does not fix} |
| 5 | 266 | sec:objects | assumption | CORE | main 2.1 | A face may also be declared receding ([assumption]). |
| 6 | 268 | sec:objects / The group and its action. | theorem | CORE | main 2.1 | So Lorentz's group and the continuum's rotations are no symmetries of the lattice, and what the paper finds of the movin |
| 7 | 273 | sec:records | hypothesis | CORE | main 4.1 | It enters only as an explicitly named hypothesis of Section~\ref{sec:open} ([hypothesis]). |
| 8 | 276 | sec:line | derived | CORE | main Fig. 2 | \begin{figure}[!tb]\centering\includegraphics[width=0.66\textwidth]{figures/bands.pdf}\caption{\label{fig:bands}The band |
| 9 | 282 | sec:line | derived | CORE | main 2.2 | Along the cube's diagonal $\cos\omega = \cos k$ exactly, with no dispersion ([derived], <lattice>; S.1, S.65; bands.py). |
| 10 | 282 | sec:line | derived | CORE | main 2.2 | The three are one as the gap closes.) Its slow limit at small wave number is Schr\"odinger's equation with the inertia $ |
| 11 | 282 | sec:line | derived | CORE | main 2.2 | The departure is $\omega_0 / \tan\omega_0$, which is $1 - \omega_0^2 / 3$ to the order $\omega_0^2$ ([derived], <clicks> |
| 12 | 282 | sec:line | derived | CORE | main 2.2 | What the law adds is one rational $[\num, \den]$ that fixes mass and speed together, an equation that is exact, departur |
| 13 | 294 | sec:paces / The one assumption of the forms: a Link is clocked | assumption,fitted | CORE | main 2.3 | Beside the line, the model holds that a level is a count of units and that every act is measured in the Node's own units |
| 14 | 294 | sec:paces / The one assumption of the forms: a Link is clocked | derived | CORE | main 2.3 | The clock composes, $p_0 = \Gamma(1 - 1 / \Gamma)^c$: each unit slows the clock as it stands by the same fraction, since |
| 15 | 294 | sec:paces / The one assumption of the forms: a Link is clocked | derived | CORE | main 2.3 | The write carries $p_x p_y p_z / (p_0\Gamma^2)$ on the form and $p_x p_y p_z / (p_0^2\Gamma)$ on the Wronskian, and the  |
| 16 | 294 | sec:paces / The one assumption of the forms: a Link is clocked | assumption,fitted | CORE | main 2.3 | One sentence is not in Rule3. It is the model's one assumption of the forms, and it is named as the credit is (Section~\ |
| 17 | 294 | sec:paces / The one assumption of the forms: a Link is clocked | assumption,fitted | CORE | main 2.3 | This is where Einstein's $\gamma = 1$ enters the model by hand ([assumption], [fitted]: the one assumption of the forms, |
| 18 | 294 | sec:paces / The one assumption of the forms: a Link is clocked | derived | CORE | main 2.3 | The metric is stated in the variable in which it is exact ([derived]; S.31; <lattice>; paces.py). |
| 19 | 296 | sec:paces / The band at a pace. | derived | CORE | main 2.3 | \paragraph{The band at a pace.} From the coefficients, the rotation of a record at a Node with clock pace $p_0$ and Link |
| 20 | 300 | sec:paces / The band at a pace. | derived | CORE | main 2.3 | So light's speed is $N^2 = e^{-2x}$ times its vacuum speed, to the unit: an index $n = e^{2x}$, which is $1 / (1 - 2x)$  |
| 21 | 300 | sec:paces / The band at a pace. | derived | CORE | main 2.3 | Light meets a total mirror where $p_a < \Gamma \sin(k / 2)$ ([derived], <lattice>; paces.py). |
| 22 | 303 | sec:paces / The guard. | theorem | SUPPORT | supp S.4 (old S.3) | Beyond $P$ the extreme mode grows without bound, the mode at wave number $\pi$ on every axis for a numerator at or above |
| 23 | 303 | sec:paces / The guard. | derived | SUPPORT | supp S.4 (old S.3) | So a deep well freezes a clock and closes nothing, and the horizon of the quadratic form at $\Gamma / 2$ is a feature of |
| 24 | 303 | sec:paces / The guard. | assumption | SUPPORT | supp S.4 (old S.3) | It has no share, by the law's declaration by name (the frozen Node has no share): Eq.~\eqref{eq:share}'s weight $1 / p_i |
| 25 | 314 | sec:interval / What is conserved, and where. | theorem,assumption | SUPPORT | supp S.7 (old S.55) | In the clicks there are conservations other than the lattice's, and neither layer keeps a total energy ([theorem] for th |
| 26 | 318 | sec:postulates | assumption | CORE | main 2.4 | The line and its clock are fixed: every mend of the model is a family, a holder, a declaration or a read, never a change |
| 27 | 320 | sec:engine | computed | CORE | main 2.6 | The one run this paper reports is the two slits': the Huygens prediction $273$, written before the run; the run $N = 285 |
| 28 | 342 | sec:direction | theorem,assumption | CORE | main 3.1 | The back-in-time gate is exact between clicks, and runs across a click and the erasure intervals that follow it, treatin |
| 29 | 342 | sec:direction | theorem | CORE | main 3.1 | The whole run therefore goes back: $N$ intervals forward and $N$ back return every array of every family bit for bit, pr |
| 30 | 342 | sec:direction | computed | CORE | main 3.1 | The implementation checks this as a test: it runs a file forward and back and compares every array at every interval; on |
| 31 | 365 | sec:form | theorem | CORE | main 3.3 | \noindent (Proved in S.48.) With the rounding, each Node's remainder adds the term $(r - r')(\mathrm{next} - \mathrm{bef |
| 32 | 365 | sec:form | theorem,computed | CORE | main 3.3 | The change is $0$ at paces fixed in time, uniform or not, for the weighted form (for the plain form at fixed uniform pac |
| 33 | 367 | sec:form / The momentum flux is the wave's own stress. | theorem | SUPPORT | supp S.17 (old S.7) | The integer step subtracts the remainder term $\delta_i\,\Delta_a(\mathrm{now})_i - \mathrm{now}_i\,\Delta_a(\delta)_i$, |
| 34 | 381 | sec:form / The momentum flux is the wave's own stress. | derived | SUPPORT | supp S.17 (old S.7) | A narrow-band packet of count $n$ and velocity $\mathbf v$, its components' cross terms averaging out, has $2n\,v_a v_b$ |
| 35 | 381 | sec:form / The momentum flux is the wave's own stress. | derived | SUPPORT | supp S.17 (old S.7) | With the sign as written a wave's stress is written into the axis parts of the content, which enter the Link's factor an |
| 36 | 389 | sec:share | theorem | CORE | main 3.4 | Over one step of Rule3 the share's rational value, before its floor, changes by exactly the six currents into the Node,  |
| 37 | 395 | sec:share | theorem | CORE | main 3.4 | So over any region the total share changes only by the weighted currents through the region's boundary, the remainder te |
| 38 | 395 | sec:share | assumption | CORE | main 3.4 | The law does not carry it ([assumption]). |
| 39 | 397 | sec:share / The signed integers. | theorem | SUPPORT | supp S.16 (old S.6) | The total share of any lattice whose Links read the same from both ends and whose every beyond reads $0$ (a closed, a pe |
| 40 | 397 | sec:share / The signed integers. | assumption | SUPPORT | supp S.16 (old S.6) | Where a window is cut inside a passage, the NodeDetector credits $\max(s_R, 0)$, the floor at $0$ the credit's declared  |
| 41 | 401 | sec:click | assumption | CORE | main 2.5 | The credit and the write in this paragraph are the NodeDetector's declaration ([assumption]; <clicks>). |
| 42 | 403 | sec:nowaves | assumption | CORE | main 2.5 | On the lattice, the absorbed record is erased from the click's Node outward at the causal bound, one Link distance per i |
| 43 | 413 | sec:meeting / The click, algebraically. | assumption | CORE | main 2.5 | Its write is one act on $X$, at the one Node of the region that the draw picks by the share (Section~\ref{sec:nothing}): |
| 44 | 413 | sec:meeting / The click, algebraically. | assumption,derived | CORE | main 2.5 | A frozen Node stands in no NodeDetector's front and is never clicked ([assumption] for the definition, [derived] for the |
| 45 | 415 | sec:meeting / One bilinear form for every click, two credit rule | assumption,derived | CORE | main 7.1 | The meeting is the law's reading of the click, laid over a credit that computes the forward record's share; the NodeDete |
| 46 | 417 | sec:meeting / One bilinear form for every click, two credit rule | assumption,derived | CORE | main Fig. 3 | \begin{figure}[!tb]\centering\includegraphics{figures/click_body.pdf}\caption{\label{fig:meeting}The click at a NodeDete |
| 47 | 425 | sec:node-reader | assumption | SUPPORT | supp S.9 (old S.50) | The NodeDetector is defined by its three resolutions, the region's, the window's and the draw's, which are that relation |
| 48 | 425 | sec:node-reader | derived | SUPPORT | supp S.9 (old S.50) | What each declaration costs is derived in S.8 and S.50: a pattern in the histogram and never in one click ([derived], <c |
| 49 | 427 | sec:node-reader / The NodeDetector is one declaration kind. | derived | SUPPORT | supp S.9 (old S.50) | Its own clock, the carried sum of $p_0$ over $\Gamma$ at its Nodes, and its event clock, the windows closed, stand in th |
| 50 | 435 | sec:nothing | assumption,derived | SUPPORT | supp S.9 (old S.50) | This gives antibunching, and one quantum, one click per record between far NodeDetectors \cite{grangier}, from the credi |
| 51 | 435 | sec:nothing | derived | SUPPORT | supp S.9 (old S.50) | A bound body clicks when quanta from outside meet its own transition, never by clicks from outside; the meeting is the r |
| 52 | 435 | sec:nothing | derived | SUPPORT | supp S.9 (old S.50) | A bound body has no window of its own, and the now reaches it only through a NodeDetector's click; its own period as its |
| 53 | 435 | sec:nothing | assumption | SUPPORT | supp S.9 (old S.50) | The arrival-window rule enters no archived file; the window is declared ([assumption], <clicks>). |
| 54 | 435 | sec:nothing | assumption,derived | SUPPORT | supp S.9 (old S.50) | The write is the NodeDetector's act ([assumption], the NodeDetector's declaration; the form of the decision is [derived] |
| 55 | 435 | sec:nothing | theorem | SUPPORT | supp S.9 (old S.50) | The direction of time belongs to the clicks and not to the lattice ([theorem] for the step; the clicks' arrow is the Nod |
| 56 | 439 | sec:nothing / Only a click moves a quantum between families: a d | derived | SUPPORT | supp S.9 (old S.50) | Nothing writes a record's lines but Rule3, the lay and the face, and the credit's counts move in the click's acts alone  |
| 57 | 439 | sec:nothing / Only a click moves a quantum between families: a d | hypothesis | SUPPORT | supp S.9 (old S.50) | Its gate is named in Section~\ref{sec:open} ([hypothesis]; Section~\ref{sec:open}). |
| 58 | 447 | sec:sign | theorem | CORE | main 3.5 | The line without its division conserves it exactly, with the weights of the conserved form, under the condition of Theor |
| 59 | 447 | sec:sign | computed | CORE | main 3.5 | So the integer $W$ changes at a Node by $\epsilon_{\mathrm{re}}\,\mathrm{im}_{\mathrm{now}} - \epsilon_{\mathrm{im}}\,\m |
| 60 | 447 | sec:sign | theorem | CORE | main 3.5 | Its total over the lattice is invariant under any change of the paces that keeps them uniform over the lattice, and the  |
| 61 | 447 | sec:sign | derived,assumption | CORE | main 3.5 | Antimatter, in the model's words, is the record of the opposite sense: the same family, the same gap and the same inerti |
| 62 | 449 | sec:sign | assumption | CORE | main 3.5 | Who reads the holder of the sign is decided by the family's dimension and by no name ([assumption], <lattice>): a family |
| 63 | 449 | sec:sign | theorem,assumption | CORE | main 3.5 | The exact angle of the shears is $2\arctan(L p_0 / (2\Gamma^2))$, which is $(L / \Gamma)(p_0 / \Gamma)$ at small angles, |
| 64 | 453 | sec:light | derived | CORE | main 2.5 | A uniformly moving body writes no travelling light in the long-wavelength band (S.42 (b)) ([derived], <clicks>; body\_cl |
| 65 | 453 | sec:light | hypothesis | CORE | main 2.5 | In this reading a star shines by the write of its charges, continuous and clickless, emits whole quanta at its declared  |
| 66 | 455 | sec:price | theorem,assumption,fitted | CORE | main 7.2 | And a pair is one laid record, its phase a shared classical variable inside Bell's hidden variable \cite{bell}, so every |
| 67 | 455 | sec:price | derived | CORE | main 7.2 | The model's opaque NodeDetector in one gap loses the fringes and reads one gap's envelope, as nature's absorbing which-w |
| 68 | 493 | sec:exact | theorem | CORE | main 3.6 | So the rule carries exactly three exact massive rotations: $2\cos\omega_0 = 1$, $0$ and $-1$, with the periods $6$, $4$  |
| 69 | 502 | sec:universe | derived | CORE | main 4.1 and Table 2 | \caption{\label{tab:universe}The rule's own universe, its four families as the file examples/events/rule.json holds them |
| 70 | 515 | sec:universe | assumption | CORE | main 4.1 and Table 2 | A file's starting rest is the fixed point of the division act, computed once before the first interval ([assumption]). |
| 71 | 537 | sec:shapes | derived | CORE | main 2.3 | \subsection{What each family carries, and how gravity enters as a clock}\label{sec:shapes} What a family carries is set  |
| 72 | 539 | sec:shapes / How gravity enters: a slowed clock, and no curved | derived | CORE | main 2.3 | Around a static source it therefore rests at Poisson's solution, $3\,G_0(r)\,s$, with $s$ the body's write per interval  |
| 73 | 539 | sec:shapes / How gravity enters: a slowed clock, and no curved | derived | CORE | main 2.3 | What general relativity calls curved space stands here as the Link's pace, light's index $n = e^{2x}$ ([derived], <latti |
| 74 | 543 | sec:reach | derived | CORE | main 4.1 | So the gap is one number that is both the mass of the holder's quanta and the inverse reach of the holder ([derived], <l |
| 75 | 546 | sec:reach | assumption,fitted | CORE | main 4.1 | It binds the bodies and is not the strong force (Section~\ref{sec:open}); its pair is a declared row's, chosen where nat |
| 76 | 546 | sec:reach | assumption | CORE | main 4.1 | The nuclear holders of Section~\ref{sec:open} are read by the nucleon families alone (the law's line, Section~\ref{sec:p |
| 77 | 549 | sec:reach | assumption,fitted | CORE | main 4.1 | The binding holder is a declared row $[2400, 2401]$, its pair chosen at nature's scale ([assumption], [fitted]; the rese |
| 78 | 557 | sec:vacuum | derived | CORE | main 4.1 | So the massless holder's own travelling events have light's paces identically in every level: gravity's events and light |
| 79 | 557 | sec:vacuum | derived | CORE | main 4.1 | Inside matter the source is read through the pace: gravity gravitates ([derived], <lattice>; weak\_field.py). |
| 80 | 557 | sec:vacuum | assumption | CORE | main 4.1 | Since the two speeds are one speed, the measurement bounds no rest, and the vacuum content stays a declaration, $60$ in  |
| 81 | 559 | sec:choice | assumption | CORE | main 4.1 | The universe is chosen by one principle, stated before any row: one rule closes everything; the families are its inputs, |
| 82 | 559 | sec:choice | hypothesis | CORE | main 4.1 | Whether the free rest is computable is a hypothesis under its own name and no claim of this paper ([hypothesis]): a comp |
| 83 | 561 | sec:choice | theorem,assumption,assumption,fitted | CORE | main 4.1 | (i) a family is a band of the rule, and its row holds only its two keys; (ii) there are three exact massive rotations, t |
| 84 | 564 | sec:choice | assumption | CORE | main 4.1 | That this universe is the universe is a decision and not a theorem ([assumption]). |
| 85 | 569 | sec:whatbody | derived | CORE | main 4.2 | Four statements make a body ([derived] from the line, with the decisions named; <lattice>). |
| 86 | 579 | sec:stable | theorem | CORE | main 4.2 | The record is the top mode of Rule3's symmetric form at the paces, and $dF / d\phi = 2\lambda\phi$ on the sphere is the  |
| 87 | 585 | sec:stable | derived | CORE | main 4.2 | \noindent (Derived in S.48, by Derrick's scaling \cite{derrick} and Pohozaev's identity \cite{pohozaev} on the lattice.) |
| 88 | 587 | sec:stable | derived | CORE | main 4.2 | Beside it, a hollow beyond its reach adds a barrier: $F = a / R^2 - b / R^3 - c / R$ on a Gaussian body, where the wide  |
| 89 | 587 | sec:stable | derived | CORE | main 4.2 | (c) A collapse ends in a frozen clock ([derived] under the one assumption; <lattice>; S.41; paces.py). |
| 90 | 591 | sec:branches | theorem,computed | CORE | main 4.2 | The binding holder's fixed point has two branches, a wide cloud and a compact pixel, and the start's width alone chooses |
| 91 | 593 | sec:branches / The atom: known from clicks, laid on the lattice. | derived | CORE | main 4.2 | With the nucleus's angle alone, the levels have Bohr's form, $E_n \propto 1 / n^2$ with $a_0 = \sqrt 3 / (m^* Z\alpha)$  |
| 92 | 593 | sec:branches / The atom: known from clicks, laid on the lattice. | assumption,fitted,assumption | CORE | main 4.2 | Under line (1) of S.60 ([assumption], [fitted]) a record reads every sign field but its own, and hydrogen's lines are th |
| 93 | 595 | sec:branches / What the atom's clicks give, and what they do not. | derived | CORE | main 4.3 | The orbital Zeeman splitting has Land\'e's $g_L = 1$ ([derived]; supporting findings with their numbers in S.46; <clicks |
| 94 | 595 | sec:branches / What the atom's clicks give, and what they do not. | derived | CORE | main 4.3 | In the model, mass is the family's gap, $T\sin\omega_s$ ($s$ the family), bound or free; what decays is a body, from whi |
| 95 | 595 | sec:branches / What the atom's clicks give, and what they do not. | assumption | CORE | main 4.3 | A nucleus of several nucleons, the atom and the molecule are bodies by the one mechanism the law has for a body, a recor |
| 96 | 595 | sec:branches / What the atom's clicks give, and what they do not. | derived | CORE | main 4.3 | A nuclear holder that the electron reads is set against hydrogen's $1s$ and muonic hydrogen, a comparison that supports  |
| 97 | 599 | sec:bodyclicks / A steady rotation writes no light. | derived | CORE | main 4.3 | A body is seen by what it absorbs and by what it writes when it breathes or moves ([derived]; the Wronskian and the sour |
| 98 | 601 | sec:bodyclicks / The invariant, and the share's drift. | computed | CORE | main 4.3 | The form $D = A^2\sin^2\omega_b$ and the share are not invariant; the recurrence stepped over $20{,}000$ intervals with  |
| 99 | 605 | sec:bodyclicks / The invariant, and the share's drift. | derived | CORE | main 4.3 | The first factor is the rotation's own change under the clock's pace; the second is the Node's weight in the share ([der |
| 100 | 605 | sec:bodyclicks / The invariant, and the share's drift. | derived | CORE | main 4.3 | So $E = \hbar\omega$ holds, with $T$ for $\hbar$ and $\sin\omega$ in place of $\omega$ ([derived]; <clicks>; body\_click |
| 101 | 607 | sec:bodyclicks / The clock's click rate. | derived | CORE | main 4.3 | A light clock between two faces falls by $2U$, the Link's pace read twice (Section~\ref{sec:calibration}; S.15) ([derive |
| 102 | 609 | sec:bodyclicks / The resonance. | derived | CORE | main 4.3 | A body with two bound modes $\omega_i < \omega_j$ transfers between them at the difference $\omega_j - \omega_i$, at Rab |
| 103 | 609 | sec:bodyclicks / The resonance. | derived | CORE | main 4.3 | The one-mode line at $2\omega_b$ has no analogue there ([derived]; S.43; <clicks>; body\_clicks.py). |
| 104 | 611 | sec:bodyclicks / A body's count in clicks. | derived | CORE | main 4.3 | Under a moving well it drifts by Eq.~\eqref{eq:drift} ([derived], <lattice> for the drift; body\_clicks.py). |
| 105 | 611 | sec:bodyclicks / A body's count in clicks. | assumption | CORE | main 4.3 | This is the NodeDetector's own declaration, its record's parts, beside its Nodes, its own seed and the file's draw windo |
| 106 | 611 | sec:bodyclicks / A body's count in clicks. | derived | CORE | main 4.3 | So a body counts photons and reads $\hbar\omega$ per click, Millikan's slope $T$ ([derived]; S.14; <clicks>; body\_click |
| 107 | 611 | sec:bodyclicks / A body's count in clicks. | derived | CORE | main 4.3 | The share with the paces' weights stays the conserved form; the credit's reading at the vacuum's coefficients is the dra |
| 108 | 617 | sec:clusters / Dark matter in kind. | derived,hypothesis | CORE | main 4.4 | The paper claims no identification with nature's dark matter: this is a supporting statement of what the model holds and |
| 109 | 619 | sec:clusters / The clicks between bodies are clicks in the one se | derived | CORE | main 4.4 | It moves only by the clicks at its front, up to the drift of Eq.~\eqref{eq:drift} ([derived] from the definitions; <clic |
| 110 | 621 | sec:clusters / What each thing represents in a cluster. | derived | CORE | main 4.4 | These are three kinds of binding by rank: quanta into a body, bodies into a charged cluster, charged clusters into a gra |
| 111 | 621 | sec:clusters / What each thing represents in a cluster. | assumption | CORE | main 4.4 | The couplings are at the edge: every divisor is $1$ but gravity's $E_g$, and the universe of clusters carries $\Gamma$,  |
| 112 | 623 | sec:clusters / The clusters' cosmology. | derived | CORE | main 4.4 | The two derivations, the Doppler period of Section~\ref{sec:forms}'s row (m) times the moving clock of its row (e), agre |
| 113 | 633 | sec:forms / Two potentials. | derived | CORE | main 5.1 | The two columns are one algebra, and nature's tests read the second ([derived] for the formulas, <clicks>; S.18, S.19; w |
| 114 | 636 | sec:forms / Two potentials. | derived | CORE | main 5.1 | \item[(a)] The redshift ([derived], <clicks>; weak\_field.py). |
| 115 | 637 | sec:forms / Two potentials. | derived | CORE | main 5.1 | \item[(b)] The bending of light ([derived], <clicks>; weak\_field.py). |
| 116 | 645 | sec:forms / Two potentials. | derived | CORE | main 5.1 | Its bending is exact in the gap, while the orbit's second order at the computed pair carries the band's $k^4$ term (S.19 |
| 117 | 646 | sec:forms / Two potentials. | derived | CORE | main 5.1 | \item[(c)] The delay of light ([derived], <clicks>; S.20; weak\_field.py). |
| 118 | 647 | sec:forms / Two potentials. | derived | CORE | main 5.1 | \item[(d)] The perihelion ([derived] under the one assumption, whose end this click selected, the calibration and no tes |
| 119 | 647 | sec:forms / Two potentials. | derived,assumption | CORE | main 5.1 | At the computed pair the band's $k^4$ term, of the same order as the relativistic one, adds of the order of ten percent  |
| 120 | 648 | sec:forms / Two potentials. | derived | CORE | main 5.1 | \item[(e)] The moving clock: the band's kinetic scale and the fourth order ([derived], <clicks>; S.21; moving\_clock.py) |
| 121 | 649 | sec:forms / Two potentials. | derived | CORE | main 5.1 | \item[(h)] De Broglie's relation ([derived]; <lattice> for the band, <clicks> for the fringe spacing that reads it; S.22 |
| 122 | 650 | sec:forms / Two potentials. | derived | CORE | main 5.1 | \item[(i)] The fall ([derived], <clicks>; weak\_field.py). |
| 123 | 650 | sec:forms / Two potentials. | derived | CORE | main 5.1 | The seat of the electromagnetic binding energy is open ([derived]; <clicks>; S.56 (12), S.38). |
| 124 | 650 | sec:forms / Two potentials. | derived | CORE | main 5.1 | That, a free-packet estimate (S.47), is under nature's $10^{-13}$ for that pair \cite{will} and $10^{-15}$ for titanium  |
| 125 | 651 | sec:forms / Two potentials. | derived | CORE | main 5.1 | \item[(j)] Newton's pull and orbits ([derived], <clicks>; weak\_field.py). |
| 126 | 652 | sec:forms / Two potentials. | theorem | CORE | main 5.1 | \item[(m)] A free record keeps its wave number ([theorem]: Rule3 is invariant under the lattice's translations, the next |
| 127 | 653 | sec:forms / Two potentials. | derived | CORE | main 5.1 | \item[(p)] The lens: a content bends light and matter alike, by one formula ([derived], two derivations; <lattice> for t |
| 128 | 659 | sec:forms / Two potentials. | derived | CORE | main Fig. 5 | \begin{figure}[!tb]\centering\includegraphics[width=0.66\textwidth]{figures/moving_clock.pdf}\caption{\label{fig:clock}T |
| 129 | 663 | sec:forms / What goes in and what comes out. | derived | CORE | main 5.2 | Read as a metric, the composed clock gives $N^2 = e^{-2U}$ and the ruler $h^2 = e^{2U}$, against the isotropic Schwarzsc |
| 130 | 663 | sec:forms / What goes in and what comes out. | derived | CORE | main 5.2 | Light's index $e^{2U}$ places the photon sphere at $r = 2m$ with $U = m / r$, $m = GM / c^2$ in Links (S.30), so the cap |
| 131 | 663 | sec:forms / What goes in and what comes out. | theorem,derived | CORE | main 5.2 | So the odd lines are sourced by the halved current over the same wall as the time level, with no number matched, and a c |
| 132 | 663 | sec:forms / What goes in and what comes out. | derived | CORE | main 5.2 | In the model a source and a reader of one family see one light speed; at nature's bounds the difference is below $10^{-2 |
| 133 | 667 | sec:slits-world | derived | CORE | main 6.1 | A record uniform along the folded axis has the three-dimensional band at $k_z = 0$, so the flat lattice carries the file |
| 134 | 667 | sec:slits-world | computed | CORE | main 6.1 | The peak of the screen's inflow is at the interval $69.0$, against $62.0$ on the same file with the lattice refined four |
| 135 | 668 | sec:slits-world | computed | CORE | main Fig. 4 | \begin{figure}[!tb]\centering\includegraphics{figures/two_slits_rows.pdf}\caption{\label{fig:slits}The two slits, the on |
| 136 | 671 | sec:slits-blind | derived | CORE | main 6.2 | At $L = 2d$ the fringe is the near field's, with the minima near the lines $y = 15.3$ and $32.7$, in the regions $3$ and |
| 137 | 671 | sec:slits-blind | computed | CORE | main 6.2 | Light's line at the vacuum's paces, stepped in real arithmetic on the declared file at its own lay, gives $284.7$ units  |
| 138 | 671 | sec:slits-blind | computed | CORE | main 6.2 | The draw against its shares, a check of the generator (Born's rule being put in, Section~\ref{sec:conclusion}): the chi- |
| 139 | 671 | sec:slits-blind | computed | CORE | main 6.2 | On the Huygens row at $N = 273$ the central maximum stands above its two minima by $5.7$ times its scatter ([computed],  |
| 140 | 671 | sec:slits-blind | computed,computed | CORE | main 6.2 | (c) The lattice's own number is the inflow peak's $69.0$ against $62.0$ (Section~\ref{sec:slits-world}), a shift the law |
| 141 | 677 | sec:bell | assumption | CORE | main 7.1 | It is the NodeDetectors' draw with the declared seed, and the lattice draws nothing: the first side is drawn from its ma |
| 142 | 681 | sec:bell-blind | theorem | CORE | main 7.2 | The two parts of one beam, laid equal, are two records of one family stepped by the same line along the same path, and t |
| 143 | 681 | sec:bell-blind | derived | CORE | main 7.2 | The root sums the two branches: $\sum_k c_k\,e_k(a)\,e_k(b) = \cos(a - b)$ for the normalised vectors $e(a)$ and $e(b)$, |
| 144 | 681 | sec:bell-blind | assumption,fitted | CORE | main 7.2 | Everything after it, the fractions, $S$ and GHZ's $M$, is derived in the algebra ([assumption], [fitted]; <clicks>). |
| 145 | 690 | sec:bell-blind | derived | CORE | main 7.2 | The second, third and fourth lines follow by averaging over the pair's phase $\theta$ ([derived], <clicks>; S.10; bell.p |
| 146 | 690 | sec:bell-blind | computed | CORE | main 7.2 | The efficiency is $1$ by construction, and the marginal is one half on each side whatever the partner's setting ([comput |
| 147 | 690 | sec:bell-blind | derived | CORE | main 7.2 | For unequal parts, with $r$ the ratio of their products at the ports, the same credit gives $E = \cos 2a\cos 2b + \rho\s |
| 148 | 690 | sec:bell-blind | derived | CORE | main 7.2 | The declared pairs' $478 / 169$ sits below $2\sqrt 2$ because the angles are rational ([derived], <clicks>; bell.py). |
| 149 | 692 | sec:bell-blind | derived | CORE | main 7.2 | Without the declaration the lattice gives the second and third lines of Eq.~\eqref{eq:bell}, two results on local credit |
| 150 | 692 | sec:bell-blind | derived | CORE | main 7.2 | The same credit on four lines gives the three-quantum GHZ correlation \cite{ghz}, $E_3 = \cos 2(a + b + c)$, with every  |
| 151 | 692 | sec:bell-blind | derived | CORE | main 7.2 | Nature's gate-joined ions \cite{rowe} and transmons with a transferred photon \cite{storz} exceed it: the largest discre |
| 152 | 695 | sec:constants-law | derived | CORE | main 5.1 | The level slows the clock by Newton's potential $\Phi = -c^2 U = -c^2\ell / \Gamma$, with Newton's sign, so ([derived],  |
| 153 | 699 | sec:constants-law | derived | CORE | main 5.1 | Kepler's $G$, read from the orbits of matter as clicks, is $[2\cos\omega_0 / (1 + \cos\omega_0)]\,G_{\mathrm{clock}}$ by |
| 154 | 700 | sec:constants-law / The fine-structure constant, a coefficient of the | derived | CORE | main 5.1 | Charge universality follows from these two definitions, the quantum one unit of the invariant and the sign holder's sour |
| 155 | 700 | sec:constants-law / The fine-structure constant, a coefficient of the | derived,assumption | CORE | main 5.1 | The law's coupling between two quanta is then $\alpha_{\mathrm{law}} = (3\sqrt 3 / 8\pi)\,k / (\Gamma E_s)$, independent |
| 156 | 700 | sec:constants-law / The fine-structure constant, a coefficient of the | derived | CORE | main 5.1 | The reader sources the holder it reads, so the pair is reciprocal ([derived]; S.26 (c); <clicks>; constants.py). |
| 157 | 700 | sec:constants-law / The fine-structure constant, a coefficient of the | derived,assumption | CORE | main 5.1 | A charged body and its light read one energy by a line of the law, $E_s T\cos\omega_s = k_w\Gamma$: the energy its click |
| 158 | 700 | sec:constants-law / The fine-structure constant, a coefficient of the | derived | CORE | main 5.1 | Under the law's line a record of a family that reads a holder of the sign has the count $1$, so that many quanta of char |
| 159 | 700 | sec:constants-law / The fine-structure constant, a coefficient of the | derived | CORE | main 5.1 | This is an identity in the small-gap limit (the gap factors $\cos\omega_s$ and $2\cos\omega_s / (1 + \cos\omega_s)$, $1$ |
| 160 | 700 | sec:constants-law / The fine-structure constant, a coefficient of the | derived | CORE | main 5.1 | The Link's bound of Section~\ref{sec:calibration}, from MAGIC's subluminal dispersion limit \cite{magic}, the one the su |
| 161 | 700 | sec:constants-law / The fine-structure constant, a coefficient of the | derived | CORE | main 5.1 | $\Gamma$ reads nothing of $\omega_e$ or of $\alpha$, and nothing of the clocks bounds it ([derived], <lattice>; constant |
| 162 | 704 | sec:calibration / What the lattice fixes with no number. | derived | SUPPORT | supp S.50 (old S.54) | \paragraph{What the lattice fixes with no number.} Before any file, the lattice fixes the following, each [derived] with |
| 163 | 706 | sec:calibration / The calibration series. | derived | SUPPORT | supp S.50 (old S.54) | The two ratios the model fixes without it are light's speed of $1 / \sqrt 3$ Link per interval, from Rule3's vacuum band |
| 164 | 706 | sec:calibration / The calibration series. | hypothesis | SUPPORT | supp S.50 (old S.54) | No number comes from the lattice itself ([hypothesis] for any such number, S.54). |
| 165 | 706 | sec:calibration / The calibration series. | derived | SUPPORT | supp S.50 (old S.54) | A cavity of bodies and an atom's beat shift alike by $N$ at long wavelength, as nature's clocks do, atom against atom an |
| 166 | 709 | sec:calibration / The calibration series. | derived | SUPPORT | supp S.50 (old S.54) | \caption{\label{tab:calibration}The calibration series: each coefficient of the universe's file, the click that reads it |
| 167 | 717 | sec:calibration / The calibration series. | hypothesis | SUPPORT | supp S.50 (old S.54) | The gaps, one per family & the masses: $\omega_e$ by the electron's mass, the rest terms' coefficients $g = 1 - \cos\ome |
| 168 | 721 | sec:calibration / The calibration series. | hypothesis | SUPPORT | supp S.50 (old S.54) | The nuclear holders' ranges and weights & the nuclear binding and the nuclei's sizes, if the holders are admitted (Secti |
| 169 | 727 | sec:calibration / One prediction of the model, untested, one check a | derived | CORE | main 5.2 | It is derived from the law's lines and entered under its own name as untested, no measurement having read it ([derived]  |
| 170 | 727 | sec:calibration / One prediction of the model, untested, one check a | derived | CORE | main 5.2 | This is $0.989$ for a strontium clock at one metre for one second, the magnitude of the semiclassical expectation \cite{ |
| 171 | 731 | sec:open / Lattice readings, not findings. | assumption | SUPPORT | supp S.56 (old S.56) | The proton is one quantum of its own family, and hydrogen's clicks read it as one unit of $W$ over $0.84$ fm \cite{pdg}  |
| 172 | 731 | sec:open / Lattice readings, not findings. | derived | SUPPORT | supp S.56 (old S.56) | What the click's structure derives of the masses is in S.53: the rest energy $m^* c_m^2$ exactly, the ratio of two decla |
| 173 | 731 | sec:open / Lattice readings, not findings. | derived | SUPPORT | supp S.56 (old S.56) | Charge universality follows from the writes exactly, and the equivalence between families as the gaps close, the free pa |
| 174 | 731 | sec:open / Lattice readings, not findings. | hypothesis | SUPPORT | supp S.56 (old S.56) | If the families share one denominator, the masses are the square roots of the gaps ([hypothesis]). |
| 175 | 733 | sec:open / The declarations. | assumption | SUPPORT | supp section: the declarations | This is the law's own list, and each item carries what is derived once it is declared ([assumption] for every declaratio |
| 176 | 733 | sec:open / The declarations. | hypothesis | SUPPORT | supp section: the declarations | The weak force is the conversion click ([hypothesis] under its own name): a click that absorbs a quantum of one family a |
| 177 | 733 | sec:open / The declarations. | derived | SUPPORT | supp section: the declarations | Confinement is the record's indivisibility under the click ([derived] from its declared row; S.37; <clicks>). |
| 178 | 733 | sec:open / The declarations. | assumption,fitted | SUPPORT | supp section: the declarations | The binding holder is a declared row $[2400, 2401]$, its pair chosen at nature's scale ([assumption], [fitted]; the rese |
| 179 | 735 | sec:open / Findings against nature: the model's misses. | derived | CORE | main 8.1 | That is derived under the static read ([derived]; <clicks>; S.35, S.36) and is a finding: nature's gravitational waves a |
| 180 | 735 | sec:open / Findings against nature: the model's misses. | derived | CORE | main 8.1 | Gravity's readers are real records with no read of a current, so in the model a gyroscope precesses by $0$ from the moti |
| 181 | 735 | sec:open / Findings against nature: the model's misses. | derived | CORE | main 8.1 | A metric with no $g_{0i}$ in its preferred frame has $4\gamma + 4 + \alpha_1 = 0$, so $\alpha_1 = -8$ at $\gamma = 1$ ([ |
| 182 | 735 | sec:open / Findings against nature: the model's misses. | derived | CORE | main 8.1 | Like $\alpha_1$, this is conditional on the metric read for a static source ([derived] under the static read, named and  |
| 183 | 735 | sec:open / Findings against nature: the model's misses. | derived | CORE | main 8.1 | At the second order in $z$ the model's finite ball of bodies decelerates, bound or free, $q_0 = \Omega_m / 2 > 0$ ([deri |
| 184 | 737 | sec:open / The lattice's frame, and its mend as a hypothesis. | derived | CORE | main 8.1 | \paragraph{The lattice's frame, and its mend as a hypothesis.} At long wavelength and small gap every record's band is a |
| 185 | 737 | sec:open / The lattice's frame, and its mend as a hypothesis. | derived | CORE | main 8.1 | So the moving clock's $\gamma$ follows, and no Michelson-Morley shift appears at nature's pair beyond $c_m$'s own differ |
| 186 | 737 | sec:open / The lattice's frame, and its mend as a hypothesis. | derived | CORE | main 8.1 | But the content's Poisson rest in the lattice's frame gives a moving mass no $g_{0a}$ and no velocity-dependent $g_{ab}$ |
| 187 | 737 | sec:open / The lattice's frame, and its mend as a hypothesis. | hypothesis | CORE | main 8.1 | The mend is an explicitly named hypothesis with no line written ([hypothesis]): a carrier on a pair of Links, sourced by |
| 188 | 737 | sec:open / The lattice's frame, and its mend as a hypothesis. | derived | CORE | main 8.1 | Against it stands this: among the five forms tried, no real, local, explicit, bijective lattice line on Rule3's clock ca |
| 189 | 739 | sec:open / The strong force, by derivation. | derived | OUT | report R4 | A body's binding per quantum is bounded by $0.76\,CW / (\Gamma E)$ at one Node, and is about $0.29\,CW / (\Gamma E r)$ f |
| 190 | 739 | sec:open / The strong force, by derivation. | hypothesis | OUT | report R4 | The nucleus is therefore a hypothesis under its own name: a bound body of nucleon quanta in the well of a nuclear holder |
| 191 | 739 | sec:open / The strong force, by derivation. | derived | OUT | report R4 | The findings are these, each [derived] under the hypothesis and set beside nature (<clicks>; S.45; nuclear.py). |
| 192 | 741 | sec:open / The weak force. | derived | CORE | main 8.1 | Every rotation holder, massive or not, couples at $\alpha$ at the Link; its gap is its range and never its strength ([de |
| 193 | 741 | sec:open / The weak force. | assumption | CORE | main 8.1 | The table and the rate are nature's numbers, and nothing of the neutron's mass or its excess is claimed ([assumption] fo |
| 194 | 745 | sec:open / The record's parts are its particles. | hypothesis | OUT | report R4 | \paragraph{The record's parts are its particles.} An explicitly named hypothesis beside the families' reading (S.56 (7)) |
| 195 | 747 | sec:open / Open. | hypothesis | SUPPORT | supp S.57 (the open items) | \paragraph{Open.} The hypothesis that only a click moves a quantum between families (Section~\ref{sec:nothing}; [hypothe |
| 196 | 747 | sec:open / Open. | derived | SUPPORT | supp S.57 (the open items) | The lattice's scale: the massless band's quartic term $-(3\sum_a n_a^4 - 1)\,k^4 / 108$ ($-1 / 54$ on an axis, $0$ on th |
| 197 | 747 | sec:open / Open. | derived,hypothesis | SUPPORT | supp S.57 (the open items) | The shape of the statistics is derived from the known form of the rate equations \cite{cook} ([derived] under a declarat |
| 198 | 749 | sec:open / Where a click happens: declared, and open in its c | assumption | CORE | main 8.1 | The law's one principle for every write from outside Rule3 into a massless record, that it wakes no zero mode of the mas |
| 199 | 751 | sec:open / Also open, and the atom. | assumption | CORE | main 8.1 | The relations among the file's integers are the programme of future work, each an explicitly named hypothesis tested by  |
| 200 | 751 | sec:open / Also open, and the atom. | computed | CORE | main 8.1 | The many-body correlation is not reproduced by a product of records (helium $1.4$ percent, positronium $44$ percent of n |

| Tag | Marked claims |
|---|---|
| CORE | 158 |
| SUPPORT | 38 |
| OUT | 4 |

### D. The tables' rows (54)

| # | Table | Status | Tag | Destination | The row |
|---|---|---|---|---|---|
| 1 | tab:results | theorem | CORE | main Table 1 | Rule3's step is reversible to the bit; the interval under the condition of Section~\ref{sec:direction} |
| 2 | tab:results | computed, a run | CORE | main Table 1 | The back-in-time gate says match on the two slits' file over $40$ intervals at both seeds; the two slits' Node |
| 3 | tab:results | theorem | CORE | main Table 1 | The rule's acts form no product of levels, on the infinite lattice for one family at fixed coefficients; it co |
| 4 | tab:results | theorem at static paces, weighted | CORE | main Table 1 | A conserved form at static paces with the weights $1 / p_i^2$, its current, and the momentum flux at uniform c |
| 5 | tab:results | theorem under the two conditions | CORE | main Table 1 | The count is the record's share; the rational total share is never negative on any lattice whose Links read th |
| 6 | tab:results | theorem | CORE | main Table 1 | Three exact massive rotations |
| 7 | tab:results | derived | CORE | main Table 1 | Light's speed $1 / \sqrt 3$ Link per interval, its dispersion, and no dispersion along the cube's diagonal |
| 8 | tab:results | assumption, derived | CORE | main Table 1 | A click is the meeting of two quanta, decided in the credit, written at one Node; no signal |
| 9 | tab:results | derived | CORE | main Table 1 | A holder's reach from its gap, Yukawa's form |
| 10 | tab:results | derived (the continuous functional, the dilation continuous; the integer step's version op... | CORE | main Table 1 | The stability of a body under the dilation, to first order in the well |
| 11 | tab:results | derived | CORE | main Table 1 | A body's clicks: no light from a steady rotation, light at a breathing body's beat, the resonance at $2\omega_ |
| 12 | tab:results | definition, derived | CORE | main Table 1 | A cluster: the three levels at a Node as the nesting, three kinds of binding, the click the only thing between |
| 13 | tab:results | derived | CORE | main Table 1 | The gravitational redshift, $z = f(\omega_0)\,U$ |
| 14 | tab:results | derived under the one assumption (assumption, fitted), fixed by the two clicks | CORE | main Table 1 | The bending and the perihelion, which fixed the one assumption's two halves (`twice' and whose clock); the del |
| 15 | tab:results | derived (the formulas) | CORE | main Table 1 | The same forms against Kepler's potential: $\gamma_K$, $\beta_K$ and $\alpha_K$ from the pair alone for $0 < \ |
| 16 | tab:results | derived | CORE | main Table 1 | The moving clock: its fourth order and its kinetic scale $c_m$, Lorentz's as the gap closes |
| 17 | tab:results | derived | CORE | main Table 1 | The force between moving charges, Coulomb's over $\gamma$ |
| 18 | tab:results | derived | CORE | main Table 1 | De Broglie, the fall, Newton's pull; the content's index for every family, the lens |
| 19 | tab:results | derived | CORE | main Table 1 | Newton's pull, the clock's $G$ and Kepler's $G$ |
| 20 | tab:results | derived; $k$ declared; charge universality and the forces' ratio in the small-gap limit, b... | CORE | main Table 1 | $\alpha_{\mathrm{law}} = (3\sqrt 3 / 8\pi)\,k / (\Gamma E_s)$ between two quanta, $k$ the sign holder's declar |
| 21 | tab:results | computed | CORE | main Table 1 | The two-slit fringe row and the lattice's arrival interval |
| 22 | tab:results | fitted (the credit); derived (the forms); computed (the numbers) | CORE | main Table 1 | Bell's $E = \cos 2(a - b)$, $S = 2\sqrt 2$, $S(\rho)$ and Tsirelson's $2\sqrt{1 + \rho^2}$; every local credit |
| 23 | tab:results | declaration (the content, above its floors); derived from the law's line (the events' spee... | CORE | main Table 1 | The vacuum content $60$ at $\Gamma = 6{,}000$, bounded below by the lattice's own floor and the swing read on  |
| 24 | tab:results | declaration | CORE | main Table 1 | The binding range, $20$ Links |
| 25 | tab:results | calibration, experiment | CORE | main Table 1 | Gravity's weight $E_g$ and the sign holder's $k$, the matter pair's gap, the Link's length |
| 26 | tab:results | derived; the comparisons supporting findings | CORE | main Table 1 | The two clocks shift alike; the findings against nature of Section~\ref{sec:open} |
| 27 | tab:clicks | declaration; $N_R$ and the scatter derived under it | CORE | main 2.5 | Born's rule, the count at a region |
| 28 | tab:clicks | declaration | SUPPORT | supp section: the formulas of clicks | The dead time |
| 29 | tab:clicks | derived; computed by two\_slits\_real\_line.py | CORE | main 6.2 | The two-slit row |
| 30 | tab:clicks | derived; computed by two\_slits\_real\_line.py | CORE | main 6.2 | The arrival and its spread |
| 31 | tab:clicks | the credit declared (Born's rule for a pair); $E$ and $S$ derived under it | CORE | main 7.2 and Table 3 | Bell's pairs |
| 32 | tab:clicks | derived under the declared credit (S.40) | CORE | main 7.2 and Table 3 | GHZ, three quanta |
| 33 | tab:clicks | derived | CORE | main Table 3 | The clock's click rate |
| 34 | tab:clicks | derived under the one assumption, which this click fixed (the calibration, no test); in $U... | CORE | main Table 3 | The bending's clicks |
| 35 | tab:clicks | derived (S.16, S.43); the one-mode line under the pace read alone | CORE | main Table 3 | The absorption line |
| 36 | tab:clicks | derived | CORE | main Table 3 | Emission |
| 37 | tab:clicks | derived | CORE | main 7.2 | The which-way sum |
| 38 | tab:clicks | declaration, with its inequalities | SUPPORT | supp section: the formulas of clicks | The uncertainty relation |
| 39 | tab:clicks | derived | CORE | main 7.2 and Table 3 | No signalling |
| 40 | tab:clicks | derived; the unit the record's own, built; the drift a lattice reading | CORE | main Table 3 | A body's count in clicks |
| 41 | tab:clicks | derived under the holder's rotation (S.33); not under the plain read | CORE | main Table 3 | Magnetism |
| 42 | tab:adds | derived; lattice for the band, clicks for the clock | CORE | main Table 4 | The band's inertia and kinetic scale, $m^* = 3\tan\omega_0$, $c_m^2 = \omega_0 / (3\tan\omega_0)$, $E = m^* c_ |
| 43 | tab:adds | derived under the one assumption; clicks | CORE | main Table 4 | The post-Newtonian parameters with the gap, for $0 < \num \le \den$, $\gamma_K = \den / \num$, $\beta_K = (\de |
| 44 | tab:adds | derived under the one assumption; lattice, the second order clicks | CORE | main Table 4 | Yilmaz's exponential metric, $N^2 = e^{-2U}$, $h^2 = e^{2U}$, $\gamma = \beta = 1$ identically in $U$ in the e |
| 45 | tab:adds | derived under the one assumption, bounded by measurement and not confirmed; clicks | CORE | main Table 4 | The shadow's capture radius $b = 2e\,m$, the exponential metric's own form \cite[Section 7]{boonserm}, against |
| 46 | tab:adds | derived under the static kernel (an assumption named), the packet's field open; untested; ... | CORE | main Table 4 | The gravity of light: a light packet's integrated write at $1 \times E / c^2$ (static kernel; the packet's fie |
| 47 | tab:adds | derived, two derivations; lattice for the index, clicks for the focus | CORE | main Table 4 | The lens, Eq.~\eqref{eq:lens}: one formula for light and matter, for light exact as $\sin(k_{\mathrm{in}} / 2) |
| 48 | tab:adds | derived form, the weight declared; clicks | CORE | main Table 4 | The fine-structure constant's form, $\alpha = (3\sqrt 3 / 8\pi)\,k / (\Gamma E_s)$, $k$ the declared write wei |
| 49 | tab:adds | derived; clicks | CORE | main Table 4 | The moving clock's fourth order, $\omega_0\,[(\sum_a n_a^4)\tan\omega_0 + \cot\omega_0]$, anisotropic by $\sum |
| 50 | tab:adds | an evaluation of the declared credit, fitted, no prediction; clicks | CORE | main Table 4 | Bell's and GHZ's values at rational settings, $S = 478 / 169$ and $M = -4$ |
| 51 | tab:adds | derived under the one assumption; lattice | SUPPORT | supp S.41 | The frozen content, $U_f = \tfrac12\ln(2\Gamma)$, $(\Gamma / 2)\ln 2\Gamma$ levels |
| 52 | tab:adds | derived at $z \ll 1$; clicks | SUPPORT | supp S.46 | The clusters' deceleration, $q_0 = \Omega_m / 2 > 0$ at $z \ll 1$, bound or free |
| 53 | tab:adds | derived, a bound under the declared $W$; lattice for the well, clicks for the defect it bo... | SUPPORT | supp S.49 | A body's binding per quantum, bounded by $0.76\,CW / (\Gamma E)$ at one Node and about $0.29\,CW / (\Gamma E r |
| 54 | tab:adds | derived; clicks | SUPPORT | supp S.9 | The click's booking identity, $\Delta(wQ) = w\,(x - v)(x - b)$, with the record's own quantum $W_{\mathrm{rec} |

| Tag | Table rows |
|---|---|
| CORE | 48 |
| SUPPORT | 6 |
| OUT | 0 |

### C. The supplement's derivations (65)

| Old | Status | Tag | Destination | Title |
|---|---|---|---|---|
| S.1 | derived; lattice. | SUPPORT | supp S.2 | the band at a pace, Eq.~(4) of the paper |
| S.2 | derived; lattice. | SUPPORT | supp S.3 | light's index at a content, Section 3.4 |
| S.3 | theorem for the edge and the extreme mode; derived for the horizon of the quadratic form, a feature of the truncation; lattice. | SUPPORT | supp S.4 | the guard's edge and the horizon, Section 3.4 |
| S.4 | theorem; lattice. | SUPPORT | supp S.1 | the cube's group of 48 and its action, Section 3.1 |
| S.5 | two derivations; theorem; lattice. | SUPPORT | supp S.15 | the share's change is the currents, Eq.~(10) |
| S.6 | theorem; lattice. | SUPPORT | supp S.16 | the total share is non-negative, Section 4.4 |
| S.7 | derived; lattice. | SUPPORT | supp S.17 | the tension of a plane wave, Section 4.3 |
| S.8 | derived; clicks. | SUPPORT | supp S.10 | the region's reading factor and the draw's scatter, Section 5.3 |
| S.9 | theorem, its witnesses computed; lattice. | SUPPORT | supp S.19 | the Wronskian's conservation and its current, Section 5.5 |
| S.10 | derived under the declared credit; clicks. | SUPPORT | supp S.52 | Bell's correlation under the declared credit, Section 5.7 and Section 9.4 |
| S.11 | derived; lattice. | SUPPORT | supp S.42 | the reach of a holder with a gap, Section 6.4 |
| S.12 | derived; clicks. | SUPPORT | supp S.44 | the two speeds, Section 6.5 |
| S.13 | theorem for the critical point, the fixed point computed and the continuum constants; the stability along the dilation derived; lattice. | SUPPORT | supp S.20 | the bound body: the fixed point and the functional, Section 7.2 |
| S.14 | derived to the first order in the slow variation, the drift computed; lattice and clicks. | SUPPORT | supp S.21 | the invariant and the count's drift, Eq.~(13) |
| S.15 | derived; clicks. | SUPPORT | supp S.28 | the clock's click rate, Section 7.4 |
| S.16 | two derivations; derived; clicks. | SUPPORT | supp S.29 | the resonance at twice the rotation, Section 7.4 |
| S.17 | derived; lattice. | SUPPORT | supp S.45 | the cross current of two standing records, Section 7.5 |
| S.18 | derived; clicks. | SUPPORT | supp S.23 | the fall and the Newtonian potential the orbits measure, Eq.~(14) |
| S.19 | derived under the one assumption; clicks. | SUPPORT | supp S.24 | the post-Newtonian parameters against the Newtonian potential the orbits measure, Section ... |
| S.20 | derived; clicks. | SUPPORT | supp S.25 | the bending of light and Shapiro's delay, Section 8 (b) and (c) |
| S.21 | derived; lattice and clicks. | SUPPORT | supp S.26 | the moving clock to the second order, Section 8 (e) |
| S.22 | derived; lattice and clicks. | SUPPORT | supp S.27 | de Broglie's relation, Section 8 (h) |
| S.23 | derived; clicks. | SUPPORT | supp S.51 | the fringe's spacing and the near-field minima, Section 9.2 |
| S.24 | derived; lattice and clicks. | SUPPORT | supp S.38 | the Link's bound from light's dispersion, Section 10.2 |
| S.25 | derived; lattice. | SUPPORT | supp S.34 | Newton's constant as a reading, Eq.~(20) |
| S.26 | derived under the declared weights; lattice and clicks. | SUPPORT | supp S.35 | the fine-structure constant as a coefficient of the file, Section 10.1 |
| S.27 | derived; lattice and clicks. | SUPPORT | supp S.36 | the units, the share's ceiling and the matter pair's gap, Section 10.1 |
| S.28 | two derivations; derived; lattice and clicks. | SUPPORT | supp S.30 | the content's index for every family, Section 8 (p) |
| S.29 | two derivations; derived; clicks. | SUPPORT | supp S.46 | the clusters' cosmology: the ball of dust, Section 7.5 |
| S.30 | derived; clicks. | SUPPORT | supp S.32 | the shadow's capture radius from light's index, Section 8 |
| S.31 | derived under the one assumption; lattice and clicks. | SUPPORT | supp S.6 | the two clocks under the one assumption of Section 3.4, Section 10.2 |
| S.32 | corollary of Theorem 3, with two witnesses; lattice. | SUPPORT | supp S.18 | the conserved form's Link factor, two witnesses, Theorem 3 |
| S.33 | theorem for (a) and (b), the conservation; derived at long wavelength for (c) to (e), the force's form, Peierls' coupling; lattice for the identity, clicks for the force. | SUPPORT | supp S.40 | magnetism: the continuity identity and the covector, Section 8 |
| S.34 | derived under the one assumption; lattice. | SUPPORT | supp S.5 | the composed paces, the acts' factors and the exponential metric, Section 3.4 |
| S.35 | derived, the frame's finding; clicks. | SUPPORT | supp S.54 | the preferred-frame parameter of a diagonal metric, Section 10.3 |
| S.36 | assumption (no carrier) for the general claim; derived for the five forms tried, one derivation; clicks. | OUT | report R4 | the carrier: the five forms tried, Section 10.3 |
| S.37 | derived from the click's one form under the dimension-$3$ family, an explicitly named hypothesis, two independent derivations; clicks (no free quark, the partons' fractions); the scaling uncomputed, t... | OUT | report R4 | confinement as the indivisibility of a record, Section 10.3 |
| S.38 | derived, a bound conditional on the declared $W$, which no click bounds, and a labelled diagnostic in (b); the size law kept; lattice for the well, clicks for the defect. | SUPPORT | supp S.49 | the mass defect at a kept count and the binding bound, Section 10.3 |
| S.39 | derived, one derivation, the comparisons with nature's numbers supporting findings; lattice for the kernel, clicks for the comparisons, supporting findings. | SUPPORT | supp S.43 | the gapped holder's kernel, Section 10.3 |
| S.40 | derived under the declared credit, the credit the one assumption (Section 9.4); clicks. | SUPPORT | supp S.53 | the Greenberger-Horne-Zeilinger (GHZ) correlation under the declared credit, Section 9.4 |
| S.41 | (1) derived; clicks. (2) derived, the integrated write, the coefficient under the static far kernel, the moving packet's field open; clicks, untested. (3) derived under the one assumption, what it mea... | SUPPORT | supp S.41 | the prediction, the check and the open question, Section 10.2 |
| S.42 | derived, (b) by two derivations as stated; clicks. | SUPPORT | supp S.12 | what a body writes into the holder of the sign, Section 7.4 |
| S.43 | derived, one derivation, the sum and difference assignment of (c) and (d) checked by two; the pace read's one-mode line (S.16) has no analogue under the rotation; clicks. | SUPPORT | supp S.13 | the two-mode line under the rotation, Section 7.4 |
| S.44 | derived from the definitions, an identity and no test (Section 10.1's mark); clicks. | SUPPORT | supp S.37 | the two forces between quanta and their ratio between families, Section 10.1 |
| S.45 | one derivation under the hypothesis, the normalisation of the radiated share for a second; nothing run; clicks. | OUT | report R4 | the nuclear holder's well: the threshold, the binding at a size, the capture and its rever... |
| S.46 | (a) and (b) derived in form, two derivations; (c) the finding and its numbers two derivations; (d) derived, one derivation. Under the two lines of S.60 the self-term of (c) is absent and (a) is the la... | SUPPORT | supp S.47 | the atom with the nucleus's angle alone, the record's own level, and the holders the elect... |
| S.47 | derived in form, two derivations, the number an upper estimate; clicks. | SUPPORT | supp S.33 | the equivalence principle between families, Section 8 (i) |
| S.48 | Theorems 1 to 3 proved for every lattice; the stable body's proposition derived for the continuous functional, the integer step's version open; lattice. | SUPPORT | supp S.14 | the proofs of the theorems of Sections 4 and 7.2 |
| S.49 | the law's words; the paper's Sections 1, 3, 5 and 7. | SUPPORT | supp front | the words of the method, as the paper uses them, Sections 1, 3, 5 and 7 |
| S.50 | the click's algebraic definition and the NodeDetector's declarations the law's; the credit a declaration; lattice for the record, clicks for every number of nature. | SUPPORT | supp S.9 | the click and the NodeDetector: the passage from the lattice to the clicks, Section 5 |
| S.51 | the joint share a declaration; the correlations under it derived, two derivations; the swap's joint share [hypothesis], with the criterion that separates a transferred quantum from a coupling, the cre... | SUPPORT | supp S.11 | why there is entanglement, and its scope, Sections 5.2 and 9 |
| S.52 | the body's definition and its computation the law's; the criterion the model's decision; the atom's state as marked; lattice and clicks. | OUT | report R4 | bodies, the atom and the nucleus as bodies, and the criterion, Sections 7 and 10.3 |
| S.53 | the mass ratios' reading derived under the hypothesis of Section 10.3; the families declared; clicks. | OUT | report R4 | the masses as families, Section 10.3 |
| S.54 | each item as marked; lattice for the forms, clicks where a number of nature is named. | SUPPORT | supp S.50 | the properties of the lattice and the calibration series, in full, Section 10.2 |
| S.55 | the lattice's conservations theorems; the credit's bookkeeping a declaration; the energy line the law's line, two derivations. | SUPPORT | supp S.7 | the conservation picture and the credit's bookkeeping, Section 3.5 |
| S.56 | explicit findings; clicks where a number of nature is named. | SUPPORT | supp S.56 | the explicit findings, with their numbers, Section 10.3 |
| S.57 | derived from the credit's declaration, as Born's rule is, two derivations; clicks. Nothing of the click's write enters it: the anticoincidence rests on the one draw under the law as it stands; its rea... | OUT | report R5 | one photon on two bodies: the anticoincidence, Sections 5.4 and 10.3 |
| S.58 | derived from Eqs.~(3) and (4) under the one assumption (assumption, fitted), two derivations; as physics the standard post-Newtonian factor $1 + \gamma\beta^2$, where $\gamma = 1$ follows from $hN = 1... | SUPPORT | supp S.31 | the push on a moving record, Section 8 (b), Eq.~(16) |
| S.59 | derived under the law's line of the click's write with the window's outcome written, two derivations and the model's decision on the Zeno window; the archive's Zeno file is a gate and no claim of this... | OUT | report R5 | the quantum Zeno effect: the click writes the body, Section 5.4 |
| S.60 | derived under the two lines, the model's decision (line (1) [assumption], [fitted]; line (2) [assumption]); two derivations, with two costs named: under (1) the fields at a Node number the file's char... | SUPPORT | supp S.48 | Sections 7.3 and 10.3: the atom under two lines: no record reads its own write of the sign... |
| S.61 | a table of the engine's acts with their statuses D, W, L, A, H, O, F and X, each line the law's or a declaration; lattice. | OUT | report R3 | the engine's derivation table, Section 3.7 |
| S.62 | a record of the implementation's versions; lattice. | OUT | report R3 | the implementation's versions of the click's write and their readings, Sections 5.3, 5.4, ... |
| S.63 | derived, the slow limit with its three conditions named, three independent derivations; lattice. | SUPPORT | supp S.22 | Schr\"odinger's equation as the slow limit of the line, Section 3.3 |
| S.64 | derived; the closure candidate refuted as a selection of nature's electron; the coefficients stay free and the exact band's family stays a hypothesis under its own name; lattice. | OUT | report R4 | the closure candidate of the free coefficients: the pairs whose record closes at its rotat... |
| S.65 | derived, a constraint on any world file meant for nature and a constraint on the implementation's integer width (its $2^{63}$ cannot hold $\den \ge 2^{94}$), the law fixing no number; the anisotropy o... | SUPPORT | supp S.39 | the lattice's scale from light's anisotropy and nature's photon bounds, Section 10.3 |

### E. The sentences named by hand as claims (3)

| # | Line | Tag | Destination | The sentence |
|---|---|---|---|---|
| 1 | 125 | SUPPORT | supp section: the procedure of a file | The engine holds no number, no formula, no family name and no flag, and every primitive is one folder found by its name. |
| 2 | 320 | CORE | main 2.6 | Each act is a call of Rule3 on whole-lattice arrays of integers at a declared width, every neighbour read through a Port |
| 3 | 320 | CORE | main 2.6 | It holds no number of physics, no formula, no family's name and no flag; every physical value comes from the run's files |

### B. The unmarked candidate sentences (239), by their paragraphs

These carry no mark and are no claims of the paper; each follows its paragraph's tag, counted here by tag so that the checker sees none is lost.

| Tag | Candidate sentences |
|---|---|
| CORE | 175 |
| SUPPORT | 60 |
| OUT | 4 |

## 6. The exceptions by row

A row whose tag is not its paragraph's: the rows of Table 2 of the long version listed in section D above with a destination of their own (the formulas shared with nature go to Table 3, the two-slit row and the arrival to 6.2, Born's rule, the which-way sum and no signalling to their sentences); the four rows of Table 6 that go to the supplement (the frozen content, the clusters' deceleration, the binding bound, the booking identity). No marked claim of section A leaves its paragraph: where a paragraph is SUPPORT or OUT and the note names a sentence that stays, that sentence is restated in the main text with its mark in Table 1 and its claim row keeps the paragraph's tag here.
