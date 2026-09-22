# The mathematician's read of the paper, 2026-09-22

The Paper Mathematician Reviewer's read, a bounded assignment from the Boss
on the model owner's word of 2026-09-22 ("a mathematician and a physicist go
over the whole paper and give criticism and what is missing"). The paper
read: `paper/general_formula/main.tex` and `main.pdf` (43 pages) on the
branch `claude/paper-owner-review-five` at `6f9539208e47dd44c3d100132cb7fbd6b35a08e4`,
and its one commit after, `f0aca570` (the paragraph "What the law names and
has not computed"; the last section below covers it), with `NUMBERS.md` and
`PLAN.md` beside them. The reviewer edits nothing in the paper; the fixes
below are proposed in the paper's own manner, a sentence, a line or a
reference each. Nature's forms (Einstein's, Newton's, Bohr's) appear only as
the thing compared with. Pages are the PDF's; theorem, definition and
equation numbers are the PDF's (Eq. (1) the map, (2) the shell mean, (3)
Newton, (4) Coulomb, (5) the two fields, (6) the wave equation, (7) the
amplitude, (8) the pointer, (9) the rung, (10) the joint weight, (11) the
quadratic read-out, (12) the correlation's bound, (13) the finite-grain
value, (14) the square; Table 1 the ledger, Table 2 the confrontation rows,
Table 3 the conversion, Table 4 the symbols, Table 5 the families, Table 6
the roads).

What was recomputed here, from the paper's own formulas (Definition 3, Eq.
(9), the half-angle tables at 1/256), before the table was written: S(N_phi)
at the CHSH labels, 3 at 16 and 32, 176/64 at 64, 23/8 at 128, 45/16 at
256, 181/64 at every power of two from 512 through 8192, 5793/2048 at
16384; the four correlations at 4096, 725/1024 and 723/1024; 252 of the
512 multiples of 8 up to 4096 above 2 sqrt 2; no rung tie at the CHSH
labels for any multiple of 8 up to 4096; every marginal 32 of 64 in all
4096 setting pairs at N_phi = 64; 4 delta = 0.011079 and 16 delta =
0.044317 at rho = 256 - sqrt 2 / 2; 181/64 - 2 sqrt 2 = -3.02e-4 and 1.05
standard errors from Poh et al.; T_D = 110, 156, 192 and the paces 0.5818,
0.5802, 0.5774 with 1/c_D^2 = 2.954, 2.971, 3.000; the hand-worked update's
eight accumulator values and its Links at the intervals 1, 3, 5, 7, 8; the
table zero at N_phi = 8192 (C[4097] = -256, S[4097] = 0) against the exact
4 sin^2(pi/8192) = 5.9e-7. Every one agrees with the paper and with
NUMBERS.md (rows 33, 44 to 48, 149, 152, 167, 175, 201, 237). These are
COMPUTATION, the algebra's, not runs. The kind of every number named
below is the paper's own kind for it, checked against NUMBERS.md.

## The findings

Severity: MUST-FIX, wrong or unsupported as written; SHOULD-FIX, unclear or
incomplete; NIT. The kind column names the kind of any number the finding
touches (DETECTOR, GAMEBOARD, COMPUTATION, INPUT, or none).

| No. | Page, section | Severity | Finding | Fix proposed, in the paper's manner | Kind |
| --- | --- | --- | --- | --- | --- |
| 1 | p. 1 abstract; p. 35 "What is proved"; p. 26 Table 2's caption | MUST-FIX | The abstract and "What is proved" say "twelve fail and one is not compared"; Table 2's caption says thirteen FAIL (eight in a registered run, 1c among them; four by a pin without its run; one a declared input refuted), two BOUND, one NOT COMPARED, one NOT YET, two PENDING, and NUMBERS.md row 240 counts the same thirteen. The paper's tally of its own failures differs between its head and its table. | In the abstract and in "What is proved": "three readings pass, a fourth under the clock's assumed word, thirteen fail (eight in a registered run, four by a pin without its run, one a declared input refuted), two are bounds, one is not compared, one is not yet on its line and two are pending their run (Table 2)". | DETECTOR (a count of the table's rows) |
| 2 | p. 31 "The step beneath and the step above"; p. 36 Eq. (14) | MUST-FIX | The chain "from the Inside step, Eq. (14) in its frame, the six operations on the record with W its invariant ... Einstein's relation follows from the Inside step under (A1) and (A2)" attributes to Eq. (1) an invariant that Eq. (1) does not carry: the walk's invariant cos omega = cos m cos kappa belongs to a click that splits each interval between staying and hopping (A2), and the paper says three times that the law as built lacks (A2), its rows hopping whole. The Inside step of that chain is the click frame's walk, a different rule from Eq. (1), and the paper's own Table 6 says W is "declared for the rows' dynamics". As written, a reader takes W to be derived from the map of Section 2. | Open the paragraph with one sentence: "The Inside step of this chain is not Eq. (1) but the click frame's walk, one amplitude per record that splits each interval between staying and hopping (A2), whose exact invariant is cos omega = cos m cos kappa; Eq. (1), which hops whole, carries W only as the declared identity of Eq. (14)." Then replace "from the Inside step, Eq. (1) on the record with W its invariant" by "from the walk's step". | none (a formula's ground) |
| 3 | p. 4 "The road from the cells" (E_0 = N_l N_w M); p. 36 Eq. (14) (E_0 = N_l N_w M, c^2 = 1/3); p. 40 Table 4 (E_0 = m c^2, m = N_l N_w M); p. 31 (W = E_0'^2 + 3 p . p) | MUST-FIX | Three statements of the rest energy contradict: E_0 = N_l N_w M (Section 2, Eq. (14)), E_0 = m c^2 with m = N_l N_w M and c^2 = 1/3 (Table 4), and W = E_0'^2 + 3 p . p with E' = E/c^2 (Section 9). With c^2 = 1/3 the first and the second cannot both hold; Eq. (14)'s E_0 is Section 9's E_0' = E_0/c^2, the whole unit. Multiplying Eq. (14) by c^4 gives E^2 = E_0^2 + p^2 c^2 only under that reading. | One symbol: write Eq. (14) as W = E_0'^2 + 3 p . p, E_0' = E_0/c^2 = N_l N_w M, and in Table 4 "E_0' = N_l N_w M, the rest energy in whole units, E_0 = E_0' c^2"; in Section 2 "the rest energy in whole units E_0' = N_l N_w M". | INPUT (the content M and the grains) |
| 4 | p. 13 Eq. (2); p. 14 Eq. (3), Eq. (4) | MUST-FIX | Eq. (2) counts the K beams as crossing the shell "at K of them" and gives the shell mean q N_l / N(r). A digital line of the direction D crosses a shell of unit radial width at S_1/abs(D) of its Nodes (one Link per Node, abs(D)/S_1 of Euclidean advance per Link), and each of those Nodes reads q_D arrivals per interval; so the shell mean of the flow over a fan is q N_l <S_1/abs(D)>_fan / N(r), the Manhattan factor 1 on a heading, sqrt 3 on a body diagonal, 1.287 on the registered fan (the tree's orbit_read note, NUMBERS.md row 153: "a body at rest on a fan reads the fan's Manhattan mean S_1/abs(D) = 1.287 shell means"), 4/pi for a fan uniform in angle on the plane and 3/2 for one uniform in solid angle in space. The factor does not vanish with r or with the fan's grain. Eq. (3)'s G = K eta / (4 pi N_w) and Eq. (4)'s push are short by it; the derivation's series C (six headings, factor 1) does not see it. The presence of Eq. (5) is right, its dwell T_D/(S_1 N_l) per Link cancelling the factor into tau_L. Coulomb's ratio -rho_A rho_B is unaffected. | In Eq. (2) write <a>(r) = q N_l <S_1/abs(D)>_fan / N(r), one sentence after it: "each beam crosses a shell of unit radial width at S_1/abs(D) Nodes, 1.287 in the mean over the registered fan, 4/pi over a fan uniform in angle on the plane and 3/2 over one uniform in solid angle in space (the presence, Eq. (5), carries the dwell that cancels this factor into tau_L)"; in Eq. (3) G = K eta <S_1/abs(D)> / (4 pi N_w); the same factor in Eq. (4). The ledger's Newton row: "the fan's Manhattan factor" among the assumptions added. | COMPUTATION (1.287, 4/pi, 3/2 from the fan's declaration) |
| 5 | p. 17 Definition 2 (R); p. 19 Theorem 2; p. 20 Theorem 4; p. 24 Theorem 6's proof; p. 40 Appendix B | SHOULD-FIX | The half-angle tables C'[s] and S'[s] are used in the rotation, in Theorem 2's n_s, in Theorem 4's factor and in Theorem 6's proof, and defined nowhere: Appendix B defines only C_N[p] = round(256 cos(2 pi p/N)). The exact rationals 181/64 and 5793/2048 depend on C' (its entries 237, 98 and 181, 181 at the CHSH labels, NUMBERS.md row 51) and a reader cannot recompute them from the paper. The proof of Theorem 6 pins C' only as "within 1/2 per component of 256 cos(pi s/N)". | In Appendix B after C_N: "the half-angle tables of the settings are C'[s] = C_{2N}[s] = round(256 cos(pi s/N)) and S'[s] = C'[s - N/2], the same rounding at the doubled circle"; in Definition 2 (R) "C', S' the half-angle tables (Appendix B)". | COMPUTATION (181/64, 5793/2048) |
| 6 | p. 26 Table 2, row 8a | SHOULD-FIX | The row's verdict, "FAIL: a factor 88 in the registered run, 25 to 40 at head", is computed from the widths 0.036 and 0.08 to 0.13, which the same cell names GAMEBOARD, "the lattice's clock, counted in no criterion". The DETECTOR reading is the width 0, a step. A GAMEBOARD number stands in a verdict against the paper's rule (P11; record 281). | The verdict: "FAIL: a step against an exponential, the width 0 in the clicks (DETECTOR); the lattice clock's 0.036 and 0.08 to 0.13 are GAMEBOARD and enter no criterion", the factors 88 and 25 to 40 removed or moved to the criteria file. | DETECTOR (0); GAMEBOARD (0.036, 0.08 to 0.13) |
| 7 | p. 26 "The comparison with nature" | SHOULD-FIX | "Seven rows (4a, 5b, 6, 10, 11a to 11c) rest on a pin whose run is not made": row 6 now carries its run of 2026-09-22 (C1 PASS, C2 and C3 FAIL, DETECTOR), and rows 4a, 5b, 10 and 11a to 11c are not rows of Table 2 at all; the sentence names rows the table does not carry as if it did. | "Six rows of the register (4a, 5b, 10, 11a to 11c) rest on a pin whose run is not made and are not in this table; row 6 carries the run of 2026-09-22." | DETECTOR (row 6's run) |
| 8 | p. 16 "Light: no optical metric"; p. 34 item (vi); p. 26 Table 2 row 13 | SHOULD-FIX | The bending of light carries three statuses: FAIL against 1.75 arcseconds (Section 5, Section 9 (vi), the abstract's "light unbent"), PENDING (row 13's verdict), and "the discussion's NOT COMPARED stands, gamma an input" (row 13's verdict, the same cell). A referee cannot tell whether the law's bending is refuted or not yet compared. | One status, stated once and pointed to: "on the law as built the bending is 0 (series K, DETECTOR), FAIL against 1.75 arcseconds; row 13 is the pending re-run of the rings under the key, whose NOT COMPARED is the key's, not the law's", in row 13's verdict and in Section 5. | DETECTOR (0.000 pixel); INPUT (gamma) |
| 9 | p. 6 to 7 "The map" and "The two blocks" | SHOULD-FIX | "The linear block's closed form floor(s_0 + r t)" lacks the wall: s_0 + r t is an integer for an integer rate, so the floor is empty, and the cumulative event count of Eq. (1) without a cap is floor((s_0 + r t)/d) (the flight's floor((110 + 128 t)/220) reproduces the hand-worked Links at 1, 3, 5, 7, 8). The same form is repeated for "every component of it". | Write floor((s_0 + r t)/d) in both places, with "for a rate given as the pair [n, d] the wall is d and the form is floor((s_0 + n t)/d)". | none |
| 10 | p. 39 Appendix A, the proof of Theorem 2 | SHOULD-FIX | The two-input case of Theorem 2 ("for two inputs at one splitter the cross terms carry phases differing by N/2 and cancel") is proved by three checked instances, (20, 21), (3, 4, 5) and (119, 120, 169), and "the engine's merge reproduces": a computation, not a proof. The identity is one line: the two-input table with the quarter turn on the reflected output is the matrix U = [[a, i b], [i b, a]] over Z[zeta] (i = x^{N/4}), and U* U = (a^2 + b^2) I = A I. | Replace the instances by the line: "for two inputs the table is U = [[a, i b], [i b, a]] over Z[zeta_N], i = x^{N/4}, and U* U = (a^2 + b^2) I = A I, so the conjugate transpose inverts it and the cross terms cancel; the three registered pairs are its instances". | COMPUTATION (the three instances) |
| 11 | p. 13 Eq. (2) and the sentence after it | SHOULD-FIX | The shell is not defined: "a shell at distance r holds N(r) Nodes" (the derivation's 3.2 defines it on the plane as the ring abs(dist - r) < 1/2 and in space as "the shell", no width named); N(r) counted on the exact circle would be r_2(r^2), zero for most r. The ripple exponent theta <= 131/208 is the plane's (Huxley); "in space" is given no exponent. | "A shell at distance r is the set of Nodes with abs(dist - r) < 1/2, N(r) its count; on the plane N(r) = 2 pi r + O(r^theta), theta <= 131/208 (Huxley); in space N(r) = 4 pi r^2 + O(r^{21/16 + epsilon}) (Heath-Brown, the sphere's lattice-point bound), the relative ripple r^{theta - 1} and r^{-11/16 + epsilon}." | COMPUTATION (N(r)) |
| 12 | p. 13 "The inverse square as a shell mean"; p. 15 Eq. (5); p. 32 "Newton from the small step" | SHOULD-FIX | "The limit of every direction" is used as a limit without a measure: with the cube fan the limit has the anisotropy 3^{3/2} (the paper says so), so the limit depends on the fan's weights; Eq. (2)'s 4 pi r^2 and Eq. (5)'s 4 pi presuppose a fan uniform in solid angle, which is nowhere stated as the limit taken. | One sentence at Eq. (2): "the limit of every direction is K -> infinity with the fan's weights the measure of each direction's cell on the sphere (a fan declared within a ball); a fan declared as a cube has a different limit, with the anisotropy 3^{3/2}". The ledger's fan rows: "the fan uniform in solid angle" among the assumptions. | none |
| 13 | p. 9 Table 1, rows citing only the derivation's sections (the entropy identity, 14 and 16.1; Young's spacing, 7.1; the Lienard-Wiechert potential, 12.1; the Doppler by the crossing rule, 2.2 and 2.7; a body's dispersion, 4.3 and 4.4; Newton's cooling, 25.9) | SHOULD-FIX | The caption says "the section is this paper's; the derivation's section is [derivations]'s", and six rows carry no section of this paper. Four of their results are not shown in it at all (the Lienard-Wiechert potential, the Doppler by the crossing rule, Newton's cooling, Boltzmann's S = k log W beyond one clause on p. 22); Young's spacing is shown on p. 21 and a body's per-axis pace on p. 4 without the rows pointing there. A ledger row for a result the paper does not show is a claim by reference. | For the four: one paragraph each in the paper, or the cell "not shown here; the derivation's 12.1" and the caption "a row whose section is the derivation's alone is stated there and not here". For Young's spacing and the dispersion: the paper's section in the cell. | none |
| 14 | p. 9 Table 1, the row "The uncertainty relation's bounds on Z_N" | SHOULD-FIX | The row's assumption column says "a hypothesis" and the caption says "a result resting on a hypothesis beside the law has no row". The row contradicts its table's rule. | Remove the row, or change its assumption cell to "the identification of the circle as position, a definition of the reading" if that is what is meant, and say so in Section 6. | none |
| 15 | p. 20 "The hypotheses" and Theorem 4; p. 21 "What is derived and what is not" | SHOULD-FIX | Hypothesis (b) is the parallelogram law after one substitution (step (ii) of the proof is that substitution), and the parallelogram law with R(0) = 0 makes R a quadratic form by a standard argument; so "the square as the only power" is put in by (b), not forced beside it. The theorem's own content is steps (iv) and (v): the diagonalisation under the phase shift, the odd harmonics, and positivity from the counts. The paragraph's "the multiplicity rule A = sum a_i^2 and the square as the only power are derived" and the name "Gleason-like" overstate what (a) to (e) add to (b). | "Hypothesis (b) is the parallelogram law on Z[zeta_N] up to the quarter turn (step (ii)), so the square is its content; what the theorem adds is that the form is diagonal in the Galois conjugates with odd harmonics only and non-negative coefficients (steps (iv), (v)), and that A = sum a_i^2 is forced." Keep "Gleason-like" only with that sentence beside it. | none |
| 16 | p. 5 (P4), p. 6 "The map" | SHOULD-FIX | P4 says "nothing kept at a Node beyond the events there, no register, remainder or draw", and Eq. (1)'s third step keeps the remainder s - e d in the accumulator; a reader sees a contradiction on facing pages. The remainder lives on the row's or the body's record, not at the Node, but the paper does not say so where P4 is stated. | In P4: "nothing kept at a Node beyond the events there (a row's or a body's accumulator, with its remainder, travels with the row or the body, not the Node)". | none |
| 17 | p. 15 "What is delayed" | SHOULD-FIX | The clock "owes after each self-creation the whole part of a_r n_c/d_c intervals ... so that its rate is 1/(1 + a_r n_c/d_c)": the whole part alone gives the rate 1/(1 + floor(a_r n_c/d_c)), a staircase; the stated rate holds in the mean only if the remainder is carried by Eq. (1)'s division. Which is built is not said. | "the count of rate a_r n_c against the wall d_c with its remainder kept (Eq. (1)), so that its mean rate over many self-creations is exactly 1/(1 + a_r n_c/d_c)". | none |
| 18 | p. 14 "Gauss's law, exact" | SHOULD-FIX | "Once the front has passed, the net amount crossing the surface per interval equals the release inside it, exactly": for a release q(t) that varies, the crossings at the interval t equal the releases at the retarded intervals per direction, not q(t). The exact statement needs a constant release or the retarded sum. | "equals the release inside it at the retarded interval of each direction; for a constant release, the release per interval, exactly". | none |
| 19 | p. 17 Definition 2 (F) | SHOULD-FIX | pos_D(tau), the position on the digital line at the age tau, is used and never defined; the digital line is defined only in words ("after S_1 Links its displacement is D", "three axis deficits choosing the axis of each Link"), and the flight rule F writes both d and D for the direction. | One line: "pos_D(k) is the Node after k Links of the digital line of D: the axis stepped at each Link is the one whose deficit k D_a/S_1 - (steps taken on a) is largest, ties by the axis order x, y, z (the law's declared tie), so pos_D(S_1) = D"; in F write D for d. | none |
| 20 | p. 7 "The two blocks" | SHOULD-FIX | "Their continuum limit is the differential equation ds/dt = r(s)" names a limit without the scaling that takes an integer accumulator with a wall to it (the wall d -> infinity at fixed r/d, or the interval -> 0) and without an error term; the paper's method (Section 1) asks of every limit its rate. | "in the limit of the wall, d -> infinity at fixed rate over wall, the iterated count is the Euler step of ds/dt = r(s) with the error O(1/d) per interval; no bound on the accumulated error is given here". | none |
| 21 | p. 18 Definition 3, Eq. (8); p. 21 "Interference, by the formulas alone" | NIT | The factor 32 in X += 32 w C[p] is unexplained; the two-slit offer 512[...] = 1024(65536 + ...) carries it through. A reader asks why 32. | One clause naming its reason where Eq. (8) is stated ("the factor 32 is the apparatus's scale, so that one row of amount 1 reads 32^2 x 65536 = 2^26"; the reason is the engine's and the reviewer does not guess it). | none |
| 22 | p. 16 Definition 1, Eq. (7) | NIT | The amplitude z = (w/sqrt(m)) (C + i S)/256 carries a root, and abs(z)^2 = (w^2/m) ... writes the multiplicity as plain m, which the symbol table gives to the mass and Section 2 to the mass angle; z itself is never computed by the law, only abs(z)^2. | "z is a name for the reading and is never computed; the law computes abs(z)^2 = (w^2/mathtt m)(C^2 + S^2)/65536 in integers", the multiplicity in its typewriter font. | none |
| 23 | p. 40 Table 4, and throughout | SHOULD-FIX | Against the paper's own rule (every symbol one meaning, its kind shown), the letters clash: m is the mass (Table 4), the mass angle (p. 4) and the multiplicity (Eq. (7)); d is the wall (Eq. (1)), the phase pair's denominator [n, d], the direction in rule F, and the clock's d_c; a is the cap (Eq. (1)), the acceleration (Eq. (3)), the split's weights a_i, a setting, and bold a the label flow; r is the rate (Eq. (1)), the radius (Eq. (2)), a record (Definition 1) and the click frame's scale r; s is an accumulator and a setting; S is the CHSH sum, the table S[p] and S_1 the Manhattan length; R is the reading R(f), the rotation rule R and a cell's weight R(o_A, o_B); K the number of directions and the number of cells; h the quantum flag of a family (0 or 1) and Planck's constant h = h_q N_phi; A the multiplicity factor sum a_i^2 and the first party. Table 4 admits two of these (K, U_s) and not the rest. | Add to Table 4 the clashing letters with their scopes ("m the mass in Section 9 and Table 4, the mass angle in Section 2, the multiplicity is always mathtt m"; "d the wall; the phase pair's denominator is written d_phi"; "r the rate in Eq. (1) only, elsewhere the radius; the click frame's scale is written r_c"; "h the family's quantum flag, Planck's constant h = h_q N_phi"), and rename where a line suffices (the pair's denominator d_phi, the clock's pair [n_c, d_c] as already written, the cell's weight R_k). | none |
| 24 | p. 23 Theorem 5 | SHOULD-FIX | "No tie occurs for any setting pair at the twelve grains from 8 to 1024 of [checks]": the check file states no tie at the CHSH labels for every multiple of 8 up to 4096 and no tie over every setting pair at N_phi = 1024; NUMBERS.md row 48 states no tie over every pair at N_phi = 8 to 512 and at 64, 256, 1024, and at 4096 for a = 0 and 1024. "Twelve grains" matches neither. | "No tie occurs over every setting pair at N_phi = 8, 16, ..., 512 and at 1024 (NUMBERS.md row 48; [checks]), nor at the CHSH labels for any multiple of 8 up to 4096." | COMPUTATION |
| 25 | p. 9 Table 1, the pace row | NIT | The assumptions cell reads "none; the wall T_D a rule chosen among few (P9); N_l free": "none" and then one named. | "the wall T_D a rule chosen among few (P9); N_l free". | none |
| 26 | p. 10 Theorem 1 | NIT | The coset of determinant -1 is called "the reflections"; it holds the central inversion and the rotoreflections too, and the text on the same page says "the improper maps, ... the reflections with the central inversion among them". | In the theorem: "the other coset, the improper maps (the reflections, the rotoreflections and the inversion), has 24 elements too". | none |
| 27 | p. 6 "The map", operation 5; p. 20 "The objects" | NIT | "The evaluation at the N-th root of unity ... and its norm": the norm of Z[zeta_N] to a mathematician is the field norm, the product of all Galois conjugates, which Theorem 4's mixture over sigma_j is close to; the paper means the squared modulus abs(ev(f))^2. | "and its squared modulus (the click's one quadratic step; not the field norm)". | none |
| 28 | p. 15 Eq. (5) | NIT | The age moment is written with the age r/c while a row's age at the Euclidean distance r is r tau_L (tau_L = 1/v_D intervals per unit distance); on a heading tau_L = 1.72 and 1/c = 1.732. The formula mixes the beam's factor and the limit's in one line, which the sentence after it admits. | Write A = q(t - r/c) tau_L^2/(4 pi r) with "tau_L = 1/c in the limit of every direction, where Eq. (6) is taken". | COMPUTATION (1.72) |
| 29 | p. 26 Table 2, row 7a | NIT | The binding fraction's numerator, "the escaped 4 of 3677 (GAMEBOARD, the books)", is a GAMEBOARD count in a verdict; the DETECTOR mass 3673 against the declared 3677 gives the same 4 without the books. | "the mass read 3673 (DETECTOR) against the declared 3677, 4 units, 0.109 percent; the books' escaped 4 (GAMEBOARD) the check". | DETECTOR (3673); GAMEBOARD (4 of 3677) |
| 30 | p. 16 Section 6's first paragraph | NIT | "Every interval applies three of the six operations ... the click is the one place with a fourth operation": the birth wheel, the phase and every count also use the sixth (the division with the comparison), so four act every interval and the click adds the fifth. | "four of the six operations ... the click adds the fifth, the evaluation with its squared modulus". | none |
| 31 | p. 5 "Rules, parameters, initial conditions" (P11, "Nothing outside this list is assumed") | SHOULD-FIX | The list P1 to P11 is closed by that sentence, and the paper then assumes beside it: the axiom (b) of the apparatus (Theorem 4), the calibration a_tau = G M/(r c^2) (p. 16, "an input of the dictionary"), the dictionary h = h_q N_phi = h_A (p. 22), (A1) to (A3) of the frame (p. 29), and the uniform birth phase (p. 21). | "Nothing outside this list is assumed of the law; the frame's (A1) to (A3), the apparatus's axiom (b), the dictionary's h and the calibration a_tau = G M/(r c^2) are the assumptions of the extension and of the comparison, named where they enter." | INPUT |
| 32 | p. 19 Theorem 3 | NIT | The map is stated on the quotient Q that forgets the age while its flight depends on the age through the history; it is a map on pairs (element of Q, history), and the theorem says so only in prose. | "M o R o S o F induces, for each fixed history, an injective Z-linear map of Q into itself". | none |
| 33 | p. 21 "What is derived and what is not"; p. 9 Table 1, the click's row | NIT | The ledger's row "the click's weight a positive quadratic form of power 2 ... exact" and Theorem 4 rest on hypothesis (a), which the built click with the tables meets only to the tables' rounding (p. 21). The built click is exactly a quadratic form (f^T G f, G the tables' Gram matrix) and not exactly shift-invariant; the row does not say which. | In the row's assumptions cell: "(a) holds for the ideal evaluation; the built click is the quadratic form of the tables' Gram matrix, shift-invariant to the rounding". | none |
| 34 | p. 31 "The smallest thing above" | NIT | "The world above the board is quantized, a theorem of (A1), (A3) and the conversion": that ratios of integer counts lie in Q and that the least distance a click reports is one Link are consequences of the definitions (counts are integers); "theorem" overstates a remark. | "a consequence of the definitions (Theorem 3 of [einsteinoutside] states it)". | none |
| 35 | p. 26 Table 2, row 2c | NIT | The window [1.917, 2.012) is labelled "(DETECTOR)" and "(COMPUTATION)" in one cell; it is a computation from DETECTOR counts. | "the window [1.917, 2.012) (COMPUTATION from the (3, 4) split's DETECTOR counts)". | DETECTOR (63/1, 31/1, 125/3); COMPUTATION (the window) |
| 36 | p. 37 to 38 References; p. 41 Appendix C | NIT | Three sources are cited at branch heads not on main (order-channel-run 389dc5d1, atom-give-momentum 686673f7, gleason-bound 1f0ea47b) and the register at a pending PR's head (b12dd253); a reader of the archived version cannot resolve them until the merge SHAs replace them, as the text says. | The writer's next commit swaps the merge SHAs; the tag paper-2026-09-22 must carry every cited tree. | none |
| 37 | p. 36 "What the law names and has not computed", item (vi) (the commit f0aca570 after 6f953920) | NIT | "an input in (vii) above" points to item (vii) of the earlier list ("What the Inside step gives Outside", dark energy's shape) while this paragraph's own (vii) is the detector's constants c_j; the cross-reference is ambiguous inside a paragraph with the same numbering. | "an input in item (vii) of the list above, dark energy's shape". | none |

## What is missing

For a referee mathematician, ordered by weight:

1. **A statement of the click theorem in the paper's notation.** The
   abstract, Section 1 and Section 9 rest the Lorentz group on "the click
   theorem" of [clickframe], and the paper gives neither its objects (a
   click family, the transformations between families, what "preserve (A1)
   and (A2)" means as a condition on a map) nor its statement; and its
   Inside step is not Eq. (1) (finding 2). Either the theorem is stated,
   with its hypotheses and the one-line reason the scale is free, or the
   word "theorem" is replaced by "the click frame's derivation".
2. **A definition of the feedback block's primitives.** Definition 2 defines
   the rows' interval (F, C, S, R, M, B); the bodies' block (the push, the
   drive with its cap and its coincident-fire rule, the owed count, the
   release, the turn) is prose only (pp. 5 to 7, 13). Newton's, the clock's
   and the atom's results start from it. One definition environment with
   each accumulator's (rate, wall, cap) and its reading, or a table of the
   primitives (the component, its r and d, its cap, the operations among
   the six it uses, which block), as the ledger is a table of the results.
3. **The Manhattan factor of the shell mean and the fan's measure**
   (findings 4, 12), and with them a statement of what the D3 reading
   tests: at r = 12 and 24 the ring mean's grain terms are of order one
   (0.90, 0.95, 1.07, 0.97, 1.55, GAMEBOARD by formula), so the 1.997 for
   2.00 +- 0.18 is a lattice-exact reading of the scale symmetry, not of
   the shell-mean form, which the paper says in Section 4 but a referee
   will ask to see as one sentence beside Eq. (3): "no reading tests Eq.
   (3)'s coefficient; the grain terms at the registered radii are of order
   one".
4. **An error term for every limit called a limit.** The method paragraph
   (Section 1) promises each derived formula its rate; the continuum limit
   of the feedback block (finding 20), the limit of every direction
   (finding 12), the 3D ripple (finding 11) and Young's spacing (a ledger
   row, "limit", with no rate in the paper) have none. A mathematician
   accepts "exact" and "bounded by"; "in the limit" without a rate is a
   conjecture.
5. **A table of the primitives against the six operations** (item 2's table
   in another form): which of the six operations each rule uses, so that
   the claim "the rates and walls are made of six operations and nothing
   else" is checkable row by row; today it is asserted for the whole and
   shown for the rows' block only.
6. **A counterexample for the claims the paper refuses.** The paper says a
   dispersive flight passes every requirement (Table 1, "no dispersion") and
   that a detector reading 1 satisfies (a) to (c) (p. 20); the same care is
   owed to "the marginals are exact for equal weights": one worked instance
   of unequal weights where the marginal is off 1/2 would fix the theorem's
   scope better than "open beyond".
7. **The half-angle tables and the digital line as definitions** (findings
   5, 19): the two objects on which every exact rational of Section 7 and
   every pace of Section 3 rest.
8. **A statement of what is not proved, in one place.** The paper says it in
   pieces (P9's four chosen rules; (A2) not met; the c_j; the masses; the
   bending). One paragraph "Not proved" beside "What is proved" (p. 35),
   with the same items in the same font, would let a referee stop reading
   the ledger's assumption column to find them.

## What stands

- Theorems 5 and 6 with the closed form S(N_phi) = 8 (c_1 + c_1')/N_phi - 4:
  the exact marginals, the tie criterion and the exact rationals reproduce
  from Definition 3 and the tables alone (recomputed here: 176/64, 181/64,
  5793/2048, 252 of 512, no tie, every marginal 32 of 64), a claim of
  exactness that is exactly what it says.
- Proposition 1 with the hand-worked update: the pace of every direction as
  an integer identity, the Manhattan bound by Cauchy-Schwarz, the isotropic
  supremum 1/sqrt 3 as the octahedron's inscribed sphere, and the anisotropy
  as a bound on the grain, all correct as written and checkable in a line.
- The carry as a bijection and the books: conservation exact at every
  interval by construction, with Theorem 2's one-input isometry and the
  split's factor A = sum a_i^2 forced by it; the one place the law deletes,
  the click, named as such.

## The commit after 6f953920

The branch's head at the time of writing is `f0aca570` (one commit after
`6f953920`): the paragraph "What the law names and has not computed" in
Section 9 before Positioning (p. 36), the bibitem for the dark sector note
(a host map, no run), and the matching lines in NUMBERS.md (row 242),
PLAN.md and `cut30/corrections.py`; 43 pages unchanged. The paragraph adds
no number (NUMBERS.md row 242, checked: 27/20, g_1 = 0.36 and the row
numbers are rows already in the ledger or Table 2); its items are
consistent with Table 2 (rows 6, 2c, 13, 14) and with Section 9's earlier
list. Two findings touch it: 7 (the rows 4a, 5b, 10 and 11 that it names are
not in Table 2) and 37 (the cross-reference "(vii) above"). Nothing in it
changes a claim, a verdict or a proof.

## Verdict

MUST-FIX 4 (findings 1, 2, 3, 4); SHOULD-FIX 19 (findings 5 to 20, 23, 24,
31); NIT 14 (findings 21, 22, 25 to 30, 32 to 37). The four must-fixes are
a count (1), a ground misattributed (2), a symbol contradicting itself (3)
and a coefficient (4); none touches a theorem of Sections 3, 6 or 7, and
none moves a DETECTOR reading.
