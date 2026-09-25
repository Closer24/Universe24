# Audit of the paper draft against the new engine (the one operator)

Read-only audit, 2026-09-25. Nothing was edited, committed or pushed.

## Scope and sources

- Draft: `origin/paper-48:paper/general_formula/main.tex` (head cc8b22b8, 903 lines); line numbers below are paper-48's.
- Appendix: `git diff origin/paper-48 origin/paper-48-appendix` (head 51b88f9c). It changes four places: Theorem 1 and Theorems 4 and 5 now point to a new appendix "Auxiliary proofs"; that appendix adds proofs of Theorems 1 to 5; and the pace proposition's proof is inlined. Rows marked "app." refer to it.
- Figures: the body includes three figures. `groups_to_click.pdf` (groups_figure.py), `lattice.pdf` and `octahedron.pdf` (octahedron.py) are all drawn from the definitions, with no run behind them. The figures that come from old-engine runs, `two_slits`, `mach_zehnder`, `pair_64` and `s_of_n` (figures.py, drawn from series L, `examples/events/amplitude/`, which is now a cancelled world folder), appear only in `records.tex`. `main.tex` does not input that file. So on paper-48 no old-engine figure is left in the body, but the body still cites those figures and their numbers (see F-rows citing "the S(N) figure of the engine before 2026-09-23").
- New engine: HIGHLIGHTS.md 5.4, "What defines the system now" (records 1875 to 1891); LOG records 1852 to 1891; ALGEBRA.md 8, 9.12 to 9.24 and the table in 9.22 (8), plus LAB_TOOLS.md parts A and B, both on `origin/lab-tools-unification` (4b365063); CANCELLED_WORLDS.md and CANCELLED_BRANCHES.md.

The categories are those of the assignment:
- (A) An old-engine number or figure. Re-run it on the new engine.
- (B) A retired or changed mechanism or term.
- (C) A claim that is still right in the one algebra but needs rewording.
- (D) Something missing that the new engine needs.

The primary category comes first; a secondary one is in brackets. The experiment column uses the names of the seventeen:
- X1 two slits (2a)
- X2 pace fans (5a)
- X3 muon's form (4a)
- X4 redshift (4b)
- X5 transponder / round trip (4c)
- X6 Sagnac (R2)
- X7 de Broglie's fringes (M1)
- X8 moving mass (M2)
- X9 bound clock's second term (ii-a, ii-b)
- X10 deep well in motion (and its control)
- X11 light clock
- X12 receding index at k = 3 (v-m)
- X13 Bell (1a to 1d)
- X14 Malus (9)
- X15 receding index at k = 4
- X16 the two-qubit computer
- X17 Mach-Zehnder

"None" marks a general finding. "Out" means the item is no longer in the list.

"DR" marks findings from the coordinator's added check (the detector sees one Node by declaration, so the board's grain is the detector's resolution).

## 1. Findings in paper order

| # | Lines | Quote (short) | Cat | Action | Exp. |
| --- | --- | --- | --- | --- | --- |
| F1 | 1-14 | "Every formula is the derivation's (docs/DERIVATIONS_BEAM.md)... every check a detector reading of the experiments register" | C | The header describes the beam-law sources and the old register. Rewrite it when the cut30 pipeline regenerates: the sources are ALGEBRA 9 and LAB_TOOLS, and the input and output files. | none |
| F2 | 60 | "the integer group ring of a cyclic group, the phase in N_phi steps" | B | The object is now one element V (Nodes tensor label module, two levels and a remainder) and one operator S (ALGEBRA 9.19 (1)-(2)). Z[Z_N] survives only in the generator and host readers (record 1878). Rewrite the abstract. | none |
| F3 | 60 | "six local integer operations" | B | Replace with the one operator (verbs B, T, D per family, the coupling, the label matrix), the click (flux, rung, deletion) and the birth (E transposed). The "four building blocks" are retired (record 1877). | none |
| F4 | 60 | "An amplitude is an integer sum of roots of unity, its square at the click Born's form" | B | The click reads the one-way inward flux E against the form I (9.19 (3)), not the norm of ev(f). Rewrite. | X13 X14 X1 |
| F5 | 60 | "the CHSH sum as an exact rational of the declared grain, 181/64 at N_phi = 2048" | B (A) | Retired: no grain, no half-angle tables. The new pin is S = 14/5, with integer axes (1,0),(1,1) / (1,2),(3,1), n = 100 per setting, S in [2.38, 3.22], falsifier S <= 2 (9.19 (4b)). Rewrite after re-derivation. Bell clicks are held (screen rule). | X13 |
| F6 | 60 | "Tsirelson's value in the joint limit of the grain and the tables' scale" | B | The grain and tables limit is gone. State the proved facts: a product state gives S <= 2, and 14/5 on the chosen axes (records 1877, 1880). | X13 |
| F7 | 60 | "the bending's 2(1 + gamma) and the atom's ladder are conjectures" | B | Both are out of the list: the bending rests on flow_link and the age wall, both cancelled. Remove from the abstract. | Out |
| F8 | 60 | "signalled under the counter wheel ... passes in form ... under the declared seed-set order" | B | Record 1872: the residue is the law's own remainder, and the loader refuses residue_seed and any declared wheel. The seed-set argument is void. Re-derive the order channel under the remainder residue; no-signalling is proved by the mathematician (record 1888). | X13 |
| F9 | 63 | Keywords: "cyclic group ring" | B | Replace, e.g. with "one linear operator; entangled pair". | none |
| F10 | 67 | "a body steps by an accumulator against a wall, a phase turns, identical rows merge" | C | This is acceptable as the road of discovery. Mark it as the road, and state that the law now is one operator, with no stepping body and no merge verb. | none |
| F11 | 72 | "two samples of the real part of one character ... wherever the sine table's S[k] is not 0" | B | The engine has no table (record 1878). The two levels stand; the born pair is [now, -now], written by the generator. Remove the S[k] clause. | none |
| F12 | 72 | "the table of families: light [1, 1], matter [800, 809]" | B (D) | A family is its vacuum pair and label module only (9.22). At most three per world: light, matter and holder (record 1875). The holder family is missing. | none |
| F13 | 73 | "The tables, a polariser's and a splitter's, are operations on that circle" | B | The polariser is an integer axis M_u = [[a,b],[-b,a]] (9.14 (b), 9.16 (2)). The splitter is a material region whose shares are one-way flux (9.19 (3)). No tables. Rewrite item (3). | X14 X13 X17 |
| F14 | 74 | "a pair lower than its surroundings: a well ... its action ... through its table" | B (D) | A tool is a region of the operator: a holder-family cube with material integers, K, at most a birth, and a name (record 1875, LAB_TOOLS A). Remove "its table". | none |
| F15 | 74 | "the body emits and absorbs in one and the same division" | B | Emission is the birth (E transposed), triggered by the body's own click, with a stock (9.13, 9.17). Rewrite. | X4 X6 X11 |
| F16 | 75 | "when the record's motion in its cells, squared and summed, crosses W, it counts" | B | The reading is the one-way inward flux C through the set's Ports against T = I, with the rung 2Tu + T <= 2WC (9.19 (3)). Rewrite item (5). | all |
| F17 | 75 | "the record's completion is one gather ...; the two declared non-local objects beside it" | B | Record 1888: the click is the ONLY non-local act, and the completion is retired (9.12). Delete "two other non-local objects". | all |
| F18 | 76 | "counts per Node (the fringes, Malus, Bell)" | D | State that the click rule over a screen's cells (the Node that shouts) is still being derived, so the clicks of the two slits, Malus and Bell are held. | X1 X14 X13 |
| F19 | 77 | "Z_N is seen in Bell's 2 sqrt2 and in Malus's cos^2" | B | Malus is a^2/(a^2+b^2) on an integer axis; Bell is 14/5 on integer axes. No Z_N. Rewrite. | X13 X14 |
| F20 | 80 + groups_figure.py | "the phase circle Z_N its clock ... the record's motion, squared and summed over its cells" | B | Definitional figure, no run, so not (A). Panel 3 (Z_N ring as the block's clock) and panel 4 (the squared motion against the rung) depict retired mechanisms. Redraw panel 4 as the inward flux against I, and relabel panel 3. | none |
| F21 | 82 | "the law is six integer operations on that ring" | B | Same as F2 and F3. | none |
| F22 | 82 | "under (A1) and five assumptions ... the equivalence principle and ... Newton's inverse square" | B | Newton, the crowd and the push chain are out (orbit, newton_side and shell_clock worlds cancelled). Remove or move to a hypothesis note. | Out |
| F23 | 84 | "one map of bounded integers ... its rates and walls made of the six operations" | B | Rates and walls are retired: no rate, train or heading in any experiment (9.21 (1)-(2)). Rewrite as the one operator. | none |
| F24 | 84 | "the hypotheses beside rows 6, 13 and 14 change no verdict" | C | Rows 6, 13 and 14 are out of the list. Delete. | Out |
| F25 | 84 | "Row 1c: under the counter wheel ... declared seed-set order ... PASS in form" | B | As F8. | X13 |
| F26 | 84 | "S = 181/64 at the declared grain ... 1.05 standard errors from Poh et al." | B (A) | As F5. The comparison with Poh is a grain argument that no longer applies. | X13 |
| F27 | 89-97 | Eq. (map): "s <- s + r, e <- sign(s) min(floor(abs(s)/d), a), s <- s - e d" | B | The "general formula" is the old accumulator law. Replace the boxed equation with the one operator: a_next = M_F a_now - a_before with its remainder, plus coupling, plus label matrix; the click (flux, rung, deletion); the birth E transposed (9.19 (2), 9.21 (3)). | all |
| F28 | 94-96 | "capped at a = 1 for the drive ... a phase step taken, a count completed, a birth, a push" | B | The drive is retired (9.21 (3): no `_drive`). The push is outside the one algebra (9.21 (7a)). Delete. | none |
| F29 | 97 | "the sum in the group ring ...; a permutation; the evaluation ... with its norm" | B | (G), (P) and (E) as board verbs are retired; (E) is now the flux bilinear form. Rewrite the verb list. | none |
| F30 | 99 | Fig. 2 caption: "Nothing sits at a Node beyond the rows there" | C | Say instead: each record's two levels and remainder, and a body's material integers. The figure itself is fine. | none |
| F31 | 103 | "cyclic group of the phase, the group ring of the arrivals, ... the evaluation at the roots of unity" | B | Rewrite as the one element and one operator. | none |
| F32 | 103 | "the whole interval is not linear, since it also holds the carry's comparison, the click's threshold and the rates" | B | These are the old "levels". The one operator is linear (9.24 (1)); only the click is not. Rewrite. | none |
| F33 | 103 | "Its couplings are tables: the circle's C and S ... Born's rule is a coupling computed from N_phi" | B | No table and no formula on the board (record 1878). Born's granularity is 1/(2W), with W = 3 den / gcd(num, 3) of the birth cell (9.19 (4a)). Rewrite. | X13 X14 X1 |
| F34 | 103 | "declared a lamp of 128 periods ... the run's 32-period train is set blind" | B | Lamps and trains are retired: an emitter body with a stock (9.21 (2)). Rewrite the calibration example, or drop it. | X1 |
| F35 | 105 | "born at a declared source, a lamp or an emitting body, with its rows and its birth stamp u" | B | The birth is E transposed at the emitter's click; u is the rule's remainder at the birth cell (record 1872). The generator is the only writer, at interval 0 only (record 1879). | all |
| F36 | 105 | "the one non-local step is the choice of the cell, made by the birth's u ... at its completion, the gather" | B | Record 1888: the non-local act is the click (the record ends everywhere). The cell is chosen at the first interval at which a cumulative L_k reaches the rung (9.19 (3b)). There is no completion. | all |
| F37 | 107 | "a click, a record's moments or an external thing's reading, as the world file declares" | C | Align with record 1875: an experiment checks only clicks. | none |
| F38 | 114 | "run from world files with every reading pinned before the run" | D | Add: an experiment is a list of entries (family, amount or material integers, cubes, K, birth, name). The generator computes the initial state, stored once; the loader checks it in integers and says LAWFUL or REFUSED; the runs go in parallel, each writing one output file with its verdict (records 1882, 1886, 1887). | all |
| F39 | 114 | "the CHSH sum as an exact rational of the grain, 181/64 on the registered plateau" | B (A) | As F5. | X13 |
| F40 | 114 | "the law has no field, a body reads only the crowd of rows at its Node" + pair-field-v1 | B | The "crowd of rows" is the beam law. pair-field-v1 is not in the seventeen. Cut to one line, or remove. | Out |
| F41 | 119-126 | Defs (3)-(5): "Z[Z_N] ... (G) ... (E) ev ... the ladder's pointer ev(f) with its norm" | B | Rewrite the five definitions: the board and its group; the one element V; the one operator S; the click (flux E, rung, deletion, the only non-local act); the birth (E transposed, the only write). | all |
| F42 | 128 | P3 "the six operations"; P7 "the declared tables"; P9 "32/55 on a heading" | B | P7 (tables) and P9's row pace (flight table) are retired; P3 is the one operator. Rewrite the postulate list. Keep P1, P2, P4, P5 and P11. | none |
| F43 | 130 | "A row is one message on the board (a Node, a direction, an age, a phase ...)" | B | The row tuple is the beam law. A record is a summand of V. Also: "ladder's rungs over the birth phase", and HOST "the residue on a gather line" (no gather line). | none |
| F44 | 145 | "the rows' pace c sat at that bound ... the flight's declared wall T_D" | B | This is the flight table, history. Replace with the band's pace at k -> 0 (Eq. dispersion). Per the one-version rule (record 1267), do not keep history blocks in the body. | X2 |
| F45 | 159-170 | "The objects ... at N_phi = 8192 only 1952 of the 8192 table pairs are distinct" | B | This concerns the ring and the table click, both retired. Remove. | none |
| F46 | 172-176 | "(a_now S[k+t] - a_before S[t])/S[k] with the sine table S[j] = round(256 sin j theta)" | B | No table on the board. The clocks [2464, 25] and [308, 25] are born clocks, written by the generator. Rewrite "One group, two representations" as the levels only, or remove. | X13 X14 |
| F47 | 178-197 | Def. row: "(x, D, tau, p, e, h, r, l, w, m) ... bounded by 2^62 - 1" | B | Beam-law row and multiplicity. Remove from the body. | none |
| F48 | 199-203 | "The host ... keeps per live record the birth phase u ... a gathered flag" | B | No gather flag and no accumulated pointer. u is the remainder; the offer is the flux. Remove. | none |
| F49 | 205-244 | Def. rules F, C, S, R, M, B; "u the lamp's phase ... (b - 1) mod N_phi" | B | The whole definition is the beam law. Remove; point to ALGEBRA 9.19. | none |
| F50 | 246-255 | "(T) ... the drive, the owed count, the release, the lamp's wheel, the push"; "(E) ... tables at the scale 256" | B | Keep (B), (T) and (D) as the operator's verbs. (E) becomes the flux. (G) and (P) leave the engine; the joint body of X16 is optional (record 1890). | none |
| F51 | 258 | "one set per Node where a screen is read per Node" | C (D) DR | This agrees with the owner's point, but it is not stated as the declaration. Add: a detector is sensitive to one Node by declaration, so the board's grain is the detector's resolution. Add the pending screen rule. | X1 X7 |
| F52 | 258-262 | "the detector's pointer accumulates its own record's motion ... W x (the pointer) >= (the record's norm)" | B | Replace with the flux offer C and T = I; the rung is 2Tu + T <= 2WC (9.19 (3)). | all |
| F53 | 262 | "the gather line ... at the close where it holds several; ... read at the close with the birth's u" | B | The close and the completion are retired. The cumulative ladder is read at every interval; every record clicks, face receivers included (9.19 (3a)-(3b)). | X1 X7 |
| F54 | 262 | "at a massive body's cells light does not click but drives the body's record" | B | Contradicted by the new crystal: the crystal's cells are the arriving record's named receiver (record 1850), and light clicks there. | X13 X16 |
| F55 | 262 | "the arm's label pair is rotated by the integer matrix U_s of the half-angle tables at 1/256" | B | Integer axis (a, b), M_u, with no table (9.14 (b), record 1858). | X13 X14 |
| F56 | 264-267 | "the birth wheel's u in Z_N, the lamp's phase at the birth, selects one cell" | B | u is the law's remainder with W = 3 den / gcd(num, 3), which must be at least 500 (load check); the pins are binomial (9.19 (4)). | X13 X14 X1 |
| F57 | 269-273 | Eq. (rung) with N_phi; "the ladder's order ... fixed at the lamp before either station reads" | B (C) | The rung's form survives with W from the pair. The pair is born by the crystal (click, then E transposed), not by a lamp (record 1879). | X13 |
| F58 | 273 | "the pair's record of tensor rank 2 ... read by one gather at two clicks" | C (D) | Consistent with record 1880. Add that the tensor is born only by the crystal and never written at interval 0, and drop "gather". | X13 X16 |
| F59 | 277-289 | "u = (b - 1) mod N_phi is uniform ... chooser's periods 3 and 5 against N_phi = 64 ... tables at 1/256" | B | Remainder equidistribution is COMPUTED, not proved (9.19 (4)). Tables and choosers are retired. Restate the three put-in items. | X13 X14 X1 |
| F60 | 291 | "the cos^2 correlation of the pair, GHZ's zeros, and the finite-N_phi value of S" | B | GHZ is out of the list; there is no finite-N_phi value. Rewrite. | X13, Out |
| F61 | 292-294 | "the birth is the only step that adds combinations" | C | Consistent ("the birth the only write"). Align the wording. | none |
| F62 | 296 | "the quantum h (1 on a free family ...), the charge per unit ..., the lifetime, whether the phase turns, the hand" | B | A family is its vacuum pair and label module, nothing else (9.22, record 1877). Rewrite; the families table in records.tex is also old. | none |
| F63 | 300 | "lets the same six operations carry mass, a clock and a body" | C | The rule of Eq. (massive) is the one operator's per-family block. Reword "six operations". | none |
| F64 | 314-318 | "c_m^2 = cos omega_0 c^2 ... (0.19 percent at k = 3 on the declared pair ...)" | C | The band identities stand. The use of gamma_m for a moving bound clock must be re-derived (a well cannot move; 9.24 (1)). | X3 X9 X10 |
| F65 | 326 | "its momentum the existing p in Z^3 and its step the existing verb (T) ... its push the stress" | B | No self-bound body and no moving well (9.24 (1)). A moving body is a packet with K at interval 0 (records 1884, 1885). The push is outside the one algebra (9.21 (7a)). Rewrite "The block". | X3 X9 X10 X4 X6 |
| F66 | 326 | "its action is on the phase circle, through its table, a shift t" | B | No table. Remove. | none |
| F67 | 326 | "Nothing is declared in motion" | B | Contradicted: every entry declares its K (record 1885). | X3 X4 X5 X6 X9 X10 X12 X15 |
| F68 | 326 | "every experiment ... is a world file of such blocks, lamps and detectors" | B (D) | As F38. Lamps are retired. | all |
| F69 | 328-332 | Eq. (motion): "The moving block is a resting block of width gamma_m s ... Row 4a's number ... 0.8116" | B (A) | 8.4 is HISTORY for a moving well and DERIVED for a free packet (9.24 (5)). The tick at v = 1/3 is 0.8146 from the dispersion; 0.8116 is CARRIED. Re-derive the pins blind, then re-run with the moving name (record 1889). | X3 X9 X10 |
| F70 | 334 | "The block emits at its mode through the same entry, a lamp at its own rest frequency" | B | As F15. The index formula n^2 = 1 + Gg/(omega_0^2 - omega^2) stays (C); the medium becomes a bound holder-family body (record 1877). | X12 X15 |
| F71 | 336 | "Where a world must absorb it declares a take, a damping pair on light's row" | B | The take is retired (9.12, 9.19 (3)); an open face is a face receiver. Delete, and also "one gather ... the verbs' only non-local step". | all |
| F72 | 338 | "the arrow of time is born at the click, and at a declared take" | B | Delete "and at a declared take". Recast the "train with no detector" check as a planted-board property test (9.20). | none |
| F73 | 340 | "the hop's parametric pump; the two arms held by light alone; the atom's lines ...; the two ring-ups" | B | Four of the "eight predictions" are out of the list. Reduce to the predictions that survive: the two-pace bound, the second term, the index in motion, and the moving light clock closed form (see F161). | Out, X9 X12 |
| F74 | 348 | "the wheel's reading u is fixed here (Definition rules, B)" | B | u = remainder at the birth cell at the birthing click. | all |
| F75 | 349 | "the six operations on Z[Z_N] ... the split and the rotation by the declared tables, the merge in the ring; ... P9 the blind flight" | B | Step (2) becomes the one operator. | all |
| F76 | 350 | "its completion one gather over all its detectors, the law's one non-local step ... roots of unity" | B | As F16 and F17. | all |
| F77 | 351 | "clock_stamp ... this paper's own runs read the interval between clicks as the host's tick (GAMEBOARD)" | B | Under the clicks-only rule a host tick cannot be a reading. State the clicks' stamps as the output file gives them (record 1887). | X3 X4 X9 X10 X11 |
| F78 | 355 | "Einstein's step and, in the limit under a shell average, Newton's form" | B | Newton is out of the list. Remove. | Out |
| F79 | 358-360 + app. | "The exceptions ...: the completion of a record at its click ... and the pair's click, one gather" | B | Rewrite Theorem 2 and its drafted proof to record 1888: the click is the only non-local act, and no signalling through it is proved by the mathematician. | all |
| F80 | 359 | "which cell clicks is decided at the completion, a gather over the record's offers" | B | As F36. | X1 X13 X14 |
| F81 | 362 + app. | "The least separation of two places read is one Link" | C (D) DR | Consistent with the owner's point, but grounded on (A1) only. Add the declaration that the detector's cell is one Node, so one Link is the resolution. | all |
| F82 | 362 | "c Outside is a BOUND ... 1/sqrt3 on the fan" | B | "The fan" is the beam law's. Use the band's pace at k -> 0. | X2 |
| F83 | 366 | "a record is an element f of Z[Z_N] ... the click evaluates f at the N_phi-th roots of unity" | B | Recast the first face on the levels, or drop it. The uncertainty relation is not in the list. | none |
| F84 | 366 | "a lamp releases one record with two arms" | B | The crystal: the click of the arriving record, then the birth of the entangled pair (record 1879). | X13 |
| F85 | 366 | "176/64 = 2.75 at N_phi = 64 (row 1a, against 2.42 +- 0.20), 181/64 on the plateau" | A (B) | Old-engine reading (series L). Remove; the new pin is 14/5, run on the new engine once the Bell clicks are released. | X13 |
| F86 | 366 | "the birth wheel selecting one of four cells through the ladder" | B | As F56. | X13 |
| F87 | 368 | "Young's bands and the Mach-Zehnder's ports are the beam's rows read at the click" | B | Rewrite without rows. Mach-Zehnder is X17, with two large detectors. | X1 X17 |
| F88 | 368 | "under the massive record kind the clock's 1/gamma_m is derived from the band's one formula" | B | Time dilation now comes from the packet's own dispersion, omega(K) - K v: 0.81457 against 1/gamma = 0.81650 at v = 1/3 (record 1889). Rewrite. | X3 X9 X10 |
| F89 | 368, 370-374 | Eq. (square) "W = E_0'^2 + 3 p.p ... every count of the body gated by E_0/E'" | B | A declared identity of beam-law bodies (drive, gated counts). Remove from the body. | Out |
| F90 | 368 | "the least distance a click can report is one Link" | C DR | As F81. | all |
| F91 | 368 | "c_D = N_l abs(D)/T_D ... its anisotropy 1/c_D^2 = 2.954, 2.971, 3.000" | B | Flight table, history. Remove. | X2 |
| F92 | 368 | "Newton from the small step ... (the crowd read as the age moment, ..., the push ...) ... D3, T and X" | B (A) | Out of the list; old series. Remove. | Out |
| F93 | 368 | "R(x) = 1024 (65536 + C[p1]C[p2] + S[p1]S[p2]) ... the birth wheel selects one" | B | The two slits' chain is on rows and tables. Rewrite on the flux and the cumulative ladder. | X1 |
| F94 | 368, 584 | "the bands' centres 23.5 pixels apart for the exact law's 23.3 (L2b ...)" | A (B) DR | Old-engine reading. It also claims agreement at 0.2 Node, which is below one Node. Remove. The new pin is visibility 0.96 +- 0.02 on the grown board (blind, owed). | X1 |
| F95 | 368 | "its drive moves it at the pace abs(p_a)/(N_l N_w M + abs(p_a)) ... the clock ... 1/(1 + a_tau n/d)" | B | Drive, crowd and push are retired. Remove. | Out |
| F96 | 368 | "1.907 for the pin 1.909 (series T ...)", "138 of 139 births ... (D3)" | A | Old-engine readings, out of the list. Remove. | Out |
| F97 | 368 | "the choosers sa and sb ... S = 2.75 at N_phi = 64 and 32/64 in every bin (series L)" | A (B) | Remove; the new pair source is the crystal. | X13 |
| F98 | 368 (i) | "series S's face clicks 369 and 345 (under the hypothesis covariant-readings-v1 ...)" | A | Remove. | Out |
| F99 | 368 (ii) | "the plateau 181/64 from 512 through 8192 ... measured at seven grains" | A (B) | Old-engine S(N) figure. Remove. | X13 |
| F100 | 368 (iv) | "delta k = (nS/d)(gY/c^2), nS/d = 16 a DECLARATION ... series T's 1.907 and series X's k" | B (A) | The equivalence and crowd are out. Remove. | Out |
| F101 | 368 (v) | "-1.993 pixel at gamma_PPN = 0 ... Series K's 0.000 pixel ... C_ring = 5.12" | B (A) DR | Bending is out (flow_link and lensing cancelled). The readings are sub-pixel. Remove. | Out |
| F102 | 370 | "The content and sum w^2/m are conserved exactly, the offered norm only within the tables' rounding" | B | Now conserved: the content between clicks; I per family and J together, with the exact remainder identity (9.21 (6)). Rewrite. | none |
| F103 | 380 | "the books' conservation ...; Gauss's law of a free family's flux; the split's isometry and the injectivity" | B | "What is proved" must become the one algebra's list: content; I and J; the local flux identity; the bijection 8.8; equivariance; locality; the click's no-signalling (record 1888); a product state gives S <= 2. | none |
| F104 | 380 | "Born's rule to 1/N_phi per cell ..., Tsirelson's bound to 8/N_phi plus the tables' 0.0444" | B | Born's granularity is 1/(2W) at the birth cell (9.19 (4a)); there is no tables term. Rewrite. | X13 X14 X1 |
| F105 | 380 | "Newton's inverse square, from the clicks ...; Coulomb's inverse square, the retarded potential, Poisson's equation" | B | Out of the list. Remove. | Out |
| F106 | 380 | "the bending's coefficient 2(1 + gamma) ..., and the atom's ladder ... Balmer's 27/20" | B | Out. Remove. | Out |
| F107 | 380 | "pinned by the two-slit period and Malus at 22.5 degrees" | B | General polariser angles are retired (records 1853, 1858). The Malus axes are (1,1), (5,1), (15,8), (3,2). | X14 |
| F108 | 380 | "a CHSH measurement at about 6 x 10^-5, deciding 181/64 against 2 sqrt2" | B | Void without a grain. Remove. | X13 |
| F109 | 397-400 | "the digital line's axis order and the collision's Port order ... Z_N ... up to the tables' rounding ... columns of the family table" | B | The symmetries of the one operator are the 48 and the translations, away from material (9.19). Rewrite. | none |
| F110 | 401-405 | "Lorentz's symmetry ... of its clicks Outside, under the amplitude split (A2) that the law as built lacks" | C | Reword: the moving clock's slowing is derived from the dispersion (record 1889); there is still no boost among the 48. | X3 |
| F111 | 407 | Fig. 3 caption: "its inscribed sphere ... is the rows' pace c (Proposition pace)" | C | Definitional figure, fine. Reword the caption to the band's pace. | X2 |
| F112 | 409-431 + app. | Proposition pace and "T_D = floor(sqrt(3 abs(D)^2 N_l^2))" (the appendix inlines its proof) | B | Flight table, history. Take it out of the body per records 1267 and 1538, and do not add its proof in the appendix. | X2 |
| F113 | 439-452 | "released equals in transit plus absorbed plus escaped plus cancelled ... a free message ... takes no recoil" | B | "Escaped" is retired (the face receiver's count). Momentum is conserved on the board's own values (record 1856). Rewrite. | none |
| F114 | 454-458 | "The walk is a translation: a free unit released inside a closed surface ..." | B | Re-derive Gauss's and continuity from the flux identity e_i(t) - e_i(t-1) = sum_j G_ij (9.19 (3)). | none |
| F115 | 460-462 | "The law at head bends a light row past a held mass by the time part alone" | B | Out. Remove the subsection. | Out |
| F116 | 466-477 | "the apparatus sums a record's rows through the tables and squares the sum ... threshold to the birth phase u" | B | As F16, F33 and F56. | all |
| F117 | 481-498 + app. | Theorems 4 and 5: "n_s/65536: an isometry only up to the tables' rounding (65705/65536 ...)"; "M o R o S o F" | B | Rows, splitter tables and flight are history. Replace with 8.8's bijection. The splitter's shares are the flux ratio. Do not carry the appendix proofs of 4 and 5 into the paper. | none |
| F118 | 500 | "the same tables act on the record's pair of levels by the linear form" | B | No tables. Remove. | none |
| F119 | 502-506 | "by R and by every read through the tables only within the tables' rounding" | B | Remove. | none |
| F120 | 508-582 | Theorem 6 "The quadratic read-out on the phase lattice", hypotheses (a)-(e) on Z[Z_N] | C (B) | The mathematics holds on the ring, but the engine's reading is the flux of the form I, quadratic by construction. Re-derive the characterization for the flux, or move it out. Row 2c is out. Also "series L's clicks" (old). | Out |
| F121 | 584 | "over N_phi births the count at x is b_x - b_{x-1} ... read 4104 and 4088 for 4096" | B | Beam-law rung and table arithmetic. Rewrite on the flux and remainder; the pins are binomial. | X1 |
| F122 | 584 | "the Mach-Zehnder's two ports ..., the bright port 64 of 64 clicks and the dark port 0 (row 2b)" | A (D) | Old-engine reading. The new X17: two large detectors, one contiguous region each; blind pin 100 bright / 0 dark over 100 records, band 0, with a control (record 1891). | X17 |
| F123 | 586 | "the release's cost rule reads as E = h_q s ... and the turn rule as lambda = h_A/p" | B | Release cost and turn rule are retired. de Broglie is now the band's k (X7); the rest energy is h omega_0 (X8). Rewrite. | X7 X8 |
| F124 | 588 | "bits read plus bits not read of u equal to log2 N_phi per record, is an identity of the wheel" | B | The wheel is W from the pair, the residue the law's remainder. Rewrite or drop. | X13 |
| F125 | 592-596 | "over N_phi births, one per u, ... at the labels (0, N/8, N/4, 3N/8)" | B | Axes (1,0),(1,1) / (1,2),(3,1); n = 100 records per setting; shares 2/5, 1/10, ... (9.19 (4b)). Rewrite Section 5.x Bell. | X13 |
| F126 | 598-619 | Theorem 7 "Exact count marginals ... exactly N_phi/2 ... No tie ... at the twelve grains from 8 to 1024" | B | Re-derive the marginals under W = 3 den / gcd and the remainder residue: now in distribution (binomial) plus the mathematician's no-signalling proof (record 1888). | X13 |
| F127 | 619 | "that interval the host's tick ... clock_stamp in the registered pair worlds of the engine before 2026-09-23" | B | Remove. | X13 |
| F128 | 619 | "The wheel ... runs at the rate 1 against N_phi ... a square wave ... 1 - 4/N_phi" | B | The counter wheel is retired. Remove. | X13 |
| F129 | 619 | "15/16 over 192 births ... -5/16 ... FAIL"; "Fisher-Yates permutation under a 64-bit SplitMix64 mixing hash" | B (A) | Seeds are refused (record 1872). The 1c run readings (15/16, -1/16) are old. Re-derive whether the order of outcomes under the remainder residue carries the far setting, then state 1c anew. | X13 |
| F130 | 621 | "The strict-crossing rung ... would give the second party 33/64 in 3944 of the 4096 setting pairs" | B | Remove or re-derive for W. | X13 |
| F131 | 628-660 | Theorem 8: "rho = N_t - sqrt2/2 ... 181/64 = 2.828125 at every power of two from 512 through 8192" | B (A) | No grain, no tables. Replace with the closed form S = 14/5 on the integer axes and its binomial band. The "measured after a detector" values are old-engine. | X13 |
| F132 | 660 | "S(N_phi) = 8(c_1 + c_1')/N_phi - 4 ... limit ... 186034/65773" | B | Remove. | X13 |
| F133 | 662-675 | Eq. (prediction) "S_U24 = 181/64 ..., Delta S = -3.02 x 10^-4"; "512 and 4096 were re-run by the second runner" | A (B) | Remove. The new pin is S in [2.38, 3.22] at n = 100 per setting, falsifier S <= 2; the criterion is 3 standard deviations. | X13 |
| F134 | 679 | "the six operations as the engine runs them, the read-out, the code and the ledger" | C | Reword the section preface to the one operator, the click and the birth, and the three roles (record 1879). | none |
| F135 | 683 | "the centred step ... the linear block ... the feedback block: the push, the drive, the coupling ... ds/dt = r(s)" | B | Old blocks and levels. The one operator is linear, including the coupling; drive and push are retired or CARRIED. Rewrite. | none |
| F136 | 685 | P1 "the two modes k = 0 ... and (pi, pi, pi) ... are marginal ... no GO world inserts either" | C (D) | Replace with the loader's spectral check: the largest eigenvalue of the composed operator is below 2, otherwise the file is refused (9.19 (2)). | all |
| F137 | 685 | P6 "the click of a pair is one gather ... relaxes P4 at that one step only" | B | Record 1888's wording. | X13 |
| F138 | 685 | P7/P8 "the circle N_phi and its tables at 1/256 ... the take of each absorbing object ... the lamps ... and the seed" | B (D) | The parameters are now: pairs and label modules, material maps, couplings, axes, stocks, occupation, K, and receivers' names. No tables, take, lamps or declared seeds (9.21 (1)-(2)). | all |
| F139 | 685 | P9 "the one formula of a block's motion, carried ...; the stress of light at a block's outer Ports" | B | Moving well retired; the push is CARRIED and outside the algebra. | X3 X9 X10 X6 |
| F140 | 685 | P10 "the click stores one pointer per set, the least-rank member ..." | B | Replace with the flux reading. | all |
| F141 | 685 | "The law of this paper is the runtime at the commit Appendix reproduction names" | D | Name the new engine commit and the law identity that each input file carries (record 1881). | all |
| F142 | 687 | "a body's cells acting as one ... and the record's own ledger (its pointer per cell, its u, its norm)" | B | Record 1888: there is one non-local act. Delete the other two. | all |
| F143 | 687 | "A block carries its cells, its momentum p in Z^3 and its step's accumulator per axis" | B | As F65. | X3 X4 X6 X9 X10 |
| F144 | 691 | "the take, a declaration, no identity; the seed ...; the block's momentum, step and push" | B | Rewrite the rule list per 9.20 (A): rule, coupling, reading, reversibility and locality PROVED; the push CARRIED. | none |
| F145 | 693 | "The click is the evaluation (E) of a body's own record on its cells ... declares a take" | B | As F16 and F71. | all |
| F146 | 695 | "Every registered world is run from its world file with its pin written before the run" | D | As F38: input file, load check, parallel runner, output file with verdict. | all |
| F147 | 713 | "Two more choices, and no fourth: the phase circle Z_N, N_phi per world, and the translation group" | B | Z_N is no longer a law choice; W belongs to the birth cell's pair (9.19 (4)). Rewrite. | none |
| F148 | 717 | "the turn adds modulo N_phi, hence Z_N, and the merge ... Z[Z_N]"; "the square W of Eq. (square)" | C (B) | Acceptable as the road of finding. Mark it so, and drop the Eq. (square) claim. | none |
| F149 | 719 | "The twenty-four dated steps ... 09-22 the detector's clock, the click theorem" | D | Add the steps of 09-23 to 09-25: the massive record kind and detector law; the one element and one operator; the flux; the crystal; E transposed; the input file; the moving body. | none |
| F150 | 721 | "the self-creations' ticks of series S GAMEBOARD; ... (the redshift rows 3, 4b and 12) ... under the age wall (r = 1.0000 ...)" | B (A) | Remove. | X4, Out |
| F151 | 721 | "a world file declares the families, the emitters and the detectors" | D | As F38. | all |
| F152 | 733 | "Seven formulas shown Inside (... Mach-Zehnder, the marginals, GHZ, Malus, light beside a mass) were confirmed by their runs on the engine before 2026-09-23" | A | Old-engine confirmations leave the body (record 1538). Remove; GHZ and light beside a mass are out. | X17 X13 X14 X2, Out |
| F153 | 739 | "An experiment is a world file: ... the blocks ..., the lamps and the detectors" | D (B) | Replace with the list of entries and the generator (records 1875, 1882). | all |
| F154 | 739 | "approved on the GameBoard without pins, an exploratory run reading beside the algebra's number" | C | Keep, but only clicks count. The tools' checks are the property test on planted boards (9.20), not exploratory GameBoard readings. | all |
| F155 | 743 | "the light clock in motion is a predicted FAIL as declared (row LCm)" | B (unsure) | ALGEBRA 9.24 (6)-(7) at 4b365063: the moving clock is a closed form only, never run. The branch head says gamma^2 is "the arithmetic of the push's rigid scaffold; the model has clocks and no rods". HIGHLIGHTS (record 1889) still calls gamma^2 a prediction. Needs the owner's reading before rewriting. | X11 |
| F156 | 743 | "the beam law's bodies that hop had r = 1 at every speed ..., history" | B | Remove (one-version rule). | none |
| F157 | 743 | "A fan of directions bounded in Manhattan length ... rows 6, 10, 13 and 14" | B | Remove. | Out |
| F158 | 743 | "A row whose apparatus table is the declared law (the polariser's and the splitter's tables)" | B | No tables. Remove. | X13 X14 X17 |
| F159 | 743 | "Two placements, row 7a to not predicted and row 2a to NOT COMPARED" | C | Obsolete bookkeeping. Remove. | X1, Out |
| F160 | 747 | Table caption: "every row's algebra number is the law of 2026-09-23, the massive record kind ... a867ab22" | B | The law of 2026-09-25 (the one operator). Re-derive every pin blind before the new runs. | all |
| F161 | 758 | Row 1a: "two polariser tables reading the record's phase ... S = 181/64 ... 1.05 standard errors from Poh"; col. 2 "the phase-reading component and the tables" | B (A) | New: crystal source; expected counts 40/10/10/40, 5/45/45/5, 45/5/5/45, 40/10/10/40; S = 2.80 +- 0.141; pin [2.38, 3.22]. Clicks held (screen rule). | X13 |
| F162 | 759 | Row 1b: "The CHSH sum under the phase-form window ... 2, a control" | B | The phase-form window is retired. The natural control is the proved one: a product state gives S <= 2. Re-derive, or drop the row. | X13 |
| F163 | 760 | Row 1c: "under the counter wheel [1, N] ... seed-set order ... E_N/(W - 1), 3.5 x 10^-4" | B | As F129. | X13 |
| F164 | 761 | Row 1d: "each party's + fraction N/2 of N ..., 1024 of 2048" | B (A) | The marginal is binomial about 1/2 at n records. Re-derive. | X13 |
| F165 | 762 | Row 2a: "(0.959, 0.958, 0.958 at 12, 16, 24 Links for 32 periods); NOT COMPARED" | A (B) | New: 0.96 +- 0.02 on the grown board (x >= 485, margins); trains retired; blind re-derivation owed (LAB B). Clicks held (screen rule). | X1 |
| F166 | 763 | Row 2b: "1.00 - 0.02, the dark port 0 of 64 at 128 periods ... the pair's two arms and the splitter's table" | B (D) | Recast as X17: two large detectors, pin 100/0 over 100 records, band 0, a control, the splitter as a material region; state the neglected air (record 1891). | X17 |
| F167 | 764 | Row 2c: "Born's exponent, the three-opening sum" | C | Out of the list. Remove, or keep as a derivation only. | Out |
| F168 | 765 | Row 9: "Malus at 45 degrees and at 11.25, 28.125, 33.75 degrees ... the table's counts of 256" | B (A) | New: axes (1,1), (5,1), (15,8), (3,2), which are 45, 11.31, 28.07 and 33.69 degrees; pins 128+-24, 246+-9, 199+-20, 177+-22 at 256 records (9.19 (4b)). Clicks held. | X14 |
| F169 | 766 | Row 10: "The single opening's spread, two halves ... 0.842 ... 0.886" | C | Out. Remove. | Out |
| F170 | 767 | Row 7: "The atom's lines at the coupled modes ... exploratory, GAMEBOARD: 0.09948" | C (A) | Out. Remove. | Out |
| F171 | 768 | Row 4a: "0.8116 ... (the pair [800, 809], s = 14) ... at rest: 42.364 against 42.36; in motion partial, the ramp redeclared" | A (B) | The ramp is retired (record 1884). At rest: the well [3200, 3227] on matter [3200, 3236], mode period 42.33 (9.22 (8)); the paper's pair [800, 809] disagrees. In motion: a packet with K = 0.18556; tick 0.8146 (0.8116 CARRIED); needs the moving name. Re-derive blind and re-run. | X3 |
| F172 | 769 | Row 4b: "1 + z = 1.9889 ..., the free limit 1.9339 ..., 1.9355 with the pair [800, 809]" | A (B) | 9.22 (8) and 9.24 (5): 1.935 in the frame form (emitter packet with a moving name; tick 0.8154 on [156, 157]); 1.9889 is CARRIED (pushed well). Re-derive once the moving name and the packet's stock are closed. | X4 |
| F173 | 770 | Row 4c: "(1 + beta_c)/(1 - beta_c) = 3.732 at k = 3 exactly, the hop's sidebands named beside" | A (B) | 3.7373 (frame form, moving name) against 3.7733 (design, CARRIED) and the continuum 3.732. The mirror is material and does not move (9.24 (7)(iv)). "Hop" is retired. | X5 |
| F174 | 771 | Row 5a: "the phase pace by direction (k^2/36 ...) within 0.8, 0.4, 0.2 percent ..., GAMEBOARD" | B (D) DR | 9.22 (8): a diagnostic row with no click pin; closed form k(axis) - k(diagonal) = k^2/48. Under the clicks-only rule it is not a comparison with nature. The pace difference over the 40-Link probes is about 0.1 Link, below one Node's resolution. The k^2/36 against k^2/48 difference is probably a different quantity (phase pace against k); unsure. Restate as a diagnostic and a closed form. | X2 |
| F175 | 772 | Row R2: "two pushed blocks ... 108 at rest, 247 chasing, 72 meeting, each +- 2; raw 175/319" | A (B) | Owed: re-derived blind on the flux form and the wells [800, 801]. Co-moving means two packets with moving names; the push is CARRIED. | X6 |
| F176 | 773 | Row LC: "N_0 = 213 +- 1 in A's own clicks at W = 64 ... 2L/c = 207.85 ... gamma^2/gamma_m = 1.2224 along" | A (B) | Closed form at rest: 212.10 plus the rung's offset; blind pin 214 +- 1 owed on the flux form, the well [800, 801] and the material mirror [1, 2] at [672, 674). Moving: gamma^2 and gamma forms with c_l = 0.57689, never run (9.24 (6)). Replace 1.2224, 0.9981 and 1.0136. | X11 |
| F177 | 774 | Row LCm: "the along arm is a predicted FAIL as declared ... light-held pair ... 0.8127 ... 1.0136" | B (unsure) | As F155. The light-held pair and the push are not in the one algebra. Remove the row, or restate it as the no-rods statement once the owner decides. | X11 |
| F178 | 775 | Row v: "the index of a medium block at rest ... exploratory at rest: n - 1 read at 0.87" | C (A) | Not a separate experiment. It is the rest and reference world of X12 and X15. The medium is now a bound holder-family body, with its pin re-derived blind (record 1877). Merge into X12 and X15; drop the old 0.87. | X12 X15 |
| F179 | 776 | Row v-m: "the scheme's own number ...; Fizeau's form the declared non-match ... head-on 0.498" | A (D) | LAB B pins: phase +1.0144 rad +- 0.04 with drift 1.2e-3 rad per interval (k = 3); +0.6103 rad with 4.3e-4 (k = 4). But "the probe a GAMEBOARD reading" (9.22 (8)) conflicts with the clicks-only rule: a click form of the reading is needed. The k = 4 row is missing. | X12 X15 |
| F180 | 777 | Row ii: "0.7814 and 0.8032 ...; exploratory: 0.7833 and 0.8055 by the peak" | A (B) | The pins are the well form with its residual, CARRIED. In motion, a packet with tick 0.8146 (9.22 (8), row 11). Re-derive; remove the old exploratory numbers. | X9 |
| F181 | 778 | Row M1: "the side lobe's count centroid at y = 64 + 27.79 ..., the band one Node" | A (C) DR | New: 64 + 27.4, band one Node (LAB B, 9.22 (8)). The take lines retire; the face margin is owed. The band of one Node is consistent with the owner's point; quote the pin to that resolution. Whether the M1 screen waits on the screen rule too is unsure. | X7 |
| F182 | 779 | Row M2: "the first click 169 +- 2 ...; the group transit 167.1 ...; m = k/v_g = 1.0417" | A | Owed: re-derived blind on the flux form. The emitter body now has a stock, and the train is retired. | X8 |
| F183 | 780 | Row A: "one interval is at most 3.6 x 10^-28 s ... at most 6.3 x 10^-31 s" | C (D) DR | A bound with no world, not one of the seventeen. It fixes "the one scale" from Lorentz-violation bounds. That must be reconciled with "the grain is the detector's resolution" (see F195). | none |
| F184 | 781 | Row A2: "the bound on the one scale ... about 2 x 10^-35 s" | C (D) DR | As F183. | none |
| F185 | 782 | Row B: "epsilon(gamma_m^2 - 1)/2 below 1/gamma_m, printed on every massive world; a bound, no run" | B | The bound clock's second term is an experiment with worlds (moving_20 and moving_28, rest_20 and rest_28). The moving-well formula is retired. Merge with row ii into X9 and re-derive. | X9 |
| F186 | 758-782 | (table as a whole) | D | Missing rows: X10, the deep well in motion and its control (0.7531 CARRIED, 0.8146 beside); X15, the index at k = 4; X16, the two-qubit computer (Grover 0/0/0/100, Deutsch-Jozsa 100/0, band 0); X17, Mach-Zehnder. Missing columns or notes: "held" for X1, X13 and X14 (screen rule); the medium between the tools that each experiment neglects, and why (record 1891). | X10 X15 X16 X17 |
| F187 | 785 | "Tsirelson's value 2 sqrt2 as the limit of the finite-grain Bell value (row 1a); ... c^2 = 1/3 ... the flight operator" | B | No grain. c^2 = 1/3 is the band's pace at k -> 0 (Eq. dispersion), not the flight operator. Rewrite. | X13 X2 |
| F188 | 787 | "Three rows enter only under the pair-field hypothesis ... row 12 ... row 13's bending ... row 14's orbit" | C | Out of the list. Remove, or keep one line. | Out |
| F189 | 789 | "The rows that left the list ... the far lamp (rows 3 and 11a to 11c) ..." | C | Update to the seventeen. Also gone: 2c, 10, 7, 1b (unless re-derived), LCm, GHZ, the uncertainty relation. | Out |
| F190 | 799 | "the atom's lines ..., the ring-ups of the light clock, ..." | C | Update the prediction rows: the moving light clock, the index in motion, the second term, the two-pace bound and the dispersion. | X9 X11 X12 X15 |
| F191 | 811 | "(i) The lines of the atom ... (iv) The quarks ... (vi) ... g_1 = 0.36 ... (viii) The inverse square" | B | Most items rest on retired rules (crowd, age wall) and are out of the list. Cut to one line, "outside the seventeen". | Out |
| F192 | 812-815 | "the order of the outcomes signals under the sequential wheel (... FAIL BY DERIVATION)"; "the flight table's transport free of dispersion" | B | As F129 and F91. "The uniform u does the work of quantum equilibrium" is C: u is the law's remainder, and its equidistribution is COMPUTED. | X13 |
| F193 | 819 | Conclusion: "six operations ...; the CHSH sum as a rational of the grain" | B | Rewrite after the new runs. | X13 |
| F194 | 826 | "Every world file, every registered run's record ..." | D | Data: the input files (with the law identity and hash), the output files with verdicts, the generator. | all |
| F195 | 258, 368, 584, 762, 778, 780-781 | two-slit wavelength "12, 16, 24 Links"; screen "read per Node"; "one interval ... 3.6 x 10^-28 s" | B (open) DR | The paper nowhere states a Link's physical length. If one Node is a detector's resolution cell, then light of 12 to 24 Links per wavelength means a detector cell of lambda/12 to lambda/24. Real pixels are several micrometres, larger than lambda. And rows A and A2 bound a single universal scale far below any detector. Either the grain is universal (a detector cell is many Nodes, and the one-Node screen is an idealisation), or it is per experiment (then A and A2's "one scale" and the k^2 dispersion must be re-read). This is the owner's decision; flag it. The neglected-medium reasons of record 1891 ("1e-5 per metre") also need a Link length. | X1 X7 X17, none |
| F196 | 834-848 | bibitems paper1, beamlaw, design, derivations, orderchannel, ringrun, stepalgebra, flowalgebra, pairfield, atomalgebra, darksector, disagrees, lightheld | C | Prune the items together with their rows. Point "algebra" at the unification (ALGEBRA 9.18-9.24) instead of a867ab22. Add LAB_TOOLS and CANCELLED_WORLDS. | none |
| F197 | 887-891 | "C_N[p] = round(256 cos(2 pi p/N)) ... the norm ... in [65536 - 351, 65536 + 361]" | B | Tables are host and generator only (record 1878). Remove Appendix "The tables and their rounding". | none |
| F198 | 899 | "The paper's law is the massive record kind ... a867ab22 ...; the ring's run (row 13) is this paper's one reading" | D (B) | Rewrite Reproduction: the new engine commit; the input file per experiment and its load verdict; the one command in parallel; the output files. | all |
| F199 | 899 | "the figures' runs and the seven confirmations" | A | These are series L figures (two_slits, mach_zehnder, pair_64, s_of_n) and the seven confirmations. Delete, or move to the archive. | X1 X17 X13 |
| F200 | app. | Proof of Theorem 3: "(ii) A clock: ... a pulse to its neighbour and its return"; "(i) ... at least one Link apart" | C DR | Consistent. Add the one-Node detector declaration as the ground of (i). Keep "the tick ... GAMEBOARD and never read" (clicks only). | none |
| F201 | app. | Proofs of Theorems 4 and 5 and the pace proposition: "the check with the pairs (20, 21), (3, 4, 5) ... the engine's merge" | B | Old-engine proofs. Do not carry them into the paper (F112, F117). | none |

Still valid as they stand, with no change needed:
- Theorem 1 (the 48 and the 24) and its appendix proof.
- The band (Eq. band), the cone (Eq. cone) and the light dispersion (Eq. dispersion); row A2's form.
- The coupling's Euler-Lagrange invariant J.
- The direction of time's bijection (minus the take).
- The Positioning references on psi-ontic models.
- The Declarations section.

## 2. Summary

**Counts by primary category (201 findings):**
- (A) 20
- (B) 140
- (C) 31
- (D) 10

15 more carry A as a secondary category, and 14 carry D as a secondary. DR (detector resolution) findings: F51, F81, F90, F94, F101, F174, F181, F183, F184, F195, F200.

**Sections most affected, in order:**
1. **Section 4, Bell (lines 590-675) and every Bell mention** (abstract, the "paper in one page", Section 4's "one fact", Table rows 1a to 1d). It rests entirely on the grain N_phi, the half-angle tables, the counter wheel and the seed-set order, all retired. The central number 181/64 is no longer the pin: the new pin is S = 14/5, n = 100 per setting, [2.38, 3.22]. Rewrite the whole subsection from ALGEBRA 9.19 (4b) and record 1888.
2. **Section 2, the algebra (lines 115-296).** Z[Z_N], the six verbs as board operations, the row definition, the update rules, the objects, the table click, the old click definition, and families as "quantum, charge, lifetime". All go; replace them with the one element, one operator, flux click and E-transposed birth.
3. **Section 4, from click to click (lines 342-374).** Most of the giant paragraph at line 368 is old-engine readings and retired chains (Newton, the crowd, the covariant readings, the bending, series D3, K, L, S, T, X).
4. **Section 3, the massive record kind (lines 298-340).** The band, cone and dispersion survive. The moving block, its motion formula, push, take, lamp emission and the "eight predictions" do not.
5. **The comparison table (lines 745-783).** Every pin must be re-derived blind; four experiments are missing; seven rows are out.
6. **The GameBoard section (lines 677-705) and Reproduction.** P6 to P10, the state, the read-out, and the absence of the input file, load check and runner.
7. **The introduction and abstract.** Items (2) to (7), Eq. (map), and the "general formula" itself.

**The seventeen, against the paper's rows:**

| Experiment | Paper row(s) | Status in the paper |
| --- | --- | --- |
| X1 two slits | 2a; the interference paragraph; lines 368, 584 | Old numbers (0.959, 23.5 against 23.3). New pin 0.96 +- 0.02 on the grown board, owed; clicks held. |
| X2 pace fans | 5a; Proposition pace | Now a diagnostic row (k^2/48, no click pin); the flight table is history. |
| X3 muon's form | 4a | 0.8116 CARRIED against the packet's 0.8146; pair [3200, 3227] not [800, 809]; moving name; ramp retired. |
| X4 redshift | 4b | 1.9889 CARRIED against 1.935 in the frame form; moving name owed. |
| X5 transponder | 4c | 3.732 against 3.7373 (frame form) against 3.7733 (CARRIED). |
| X6 Sagnac | R2 | 108/247/72 owed on the flux form and [800, 801]; packets with moving names. |
| X7 de Broglie's fringes | M1 | 27.79 against 27.4. |
| X8 moving mass | M2 | 169 +- 2 owed on the flux form. |
| X9 bound clock's second term | ii and B | Merge; the moving-well form retired. |
| X10 deep well in motion | none | Missing. |
| X11 light clock | LC, LCm | 213 against 214 +- 1 owed. The moving form's status is unsure (F155). |
| X12 receding index k = 3 | v-m, v | Pins exist, but a GameBoard probe (clicks-only conflict). |
| X13 Bell | 1a-1d | Must be rewritten; 181/64 retired. |
| X14 Malus | 9 | New integer axes and binomial pins; clicks held. |
| X15 receding index k = 4 | none | Missing. |
| X16 two-qubit computer | none | Missing. |
| X17 Mach-Zehnder | 2b | Recast with two large detectors, 100/0. |

No longer in the list: 1b (unless re-derived as the product-state control), 2c, 7, 10, LCm, v (becomes a control), A and A2 (bounds, no world), GHZ, the uncertainty relation, Newton, the equivalence, the bending, the delay, the pair-field rows 12 to 14, the atom, the quarks, and the dark sector.

**Unsure points:**
- (F155, F177) Whether the longitudinal light clock's gamma^2 is a prediction. HIGHLIGHTS record 1889 says it is; ALGEBRA 9.24 at the branch head 4b365063 says the model has clocks and no rods.
- (F174) The k^2/36 against k^2/48 coefficient.
- (F181) Whether M1's screen also waits on the screen rule.
- (F195) Whether the grain is universal or set per experiment by the detector's resolution. This is the owner's decision.
- Old-engine figures: the two-slit and Mach-Zehnder figure that record 1891 says "stands in the body" is on paper-48 only in records.tex. The body's three figures are definitional; only Fig. 1's panels 3 and 4 show retired mechanisms (F20).
