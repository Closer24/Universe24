# The physicist's review of the paper (2026-09-22)

The paper read: `paper/general_formula/main.pdf` (43 pages) and `main.tex`
on the branch `claude/paper-owner-review-five`, ordered at
6f9539208e47dd44c3d100132cb7fbd6b35a08e4 and read at its head
f0aca5707b4004c0de1b985f23ae0ea3451d10ac; the diff between the two is one
paragraph of Section 9 ("What the law names and has not computed", page 36)
and one line of NUMBERS.md, covered below as findings 24 and 25. Beside the
paper: `paper/general_formula/NUMBERS.md`, `docs/NATURE.md`,
`docs/EXPERIMENTS.md` (series T), `docs/TERMINOLOGY.md` (the readings, Inside
and Outside, a detector's clock), Highlights 5.4 (records 281, 762, 768, 772,
787, 788) and the three tests of every rule (skills/workflow.md).

The order (the model owner's word, record 974): a physicist goes over the
whole paper and gives criticism and what is missing. This file is criticism of
what the paper says and shows; it proposes no physics. Nature's forms appear
only as the thing compared with. The kinds are the paper's own: DETECTOR (a
click), GAMEBOARD (the host's view, a diagnostic), COMPUTATION (the algebra's).
Pages are the PDF's at f0aca570.

Severity: MUST-FIX, wrong or unsupported as written; SHOULD-FIX, unclear or
incomplete; NIT, wording or a reference.

## The findings

| No. | Page, section | Severity | Finding | Fix, in the paper's own manner | Kind of the number |
| --- | --- | --- | --- | --- | --- |
| 1 | p1 abstract; p26 Table 2 caption; p29 "The prediction, and the failures" | MUST-FIX | The three counts of the verdicts disagree: the abstract says three pass, a fourth under the clock's word, twelve fail, one not compared; the caption says thirteen FAIL (eight in a run, four by a pin without a run, one input refuted), two BOUND, one NOT COMPARED, one NOT YET, two PENDING; the failures paragraph lists eight failures and omits 1c (the order channel) and 8b (the neutrino's passage). | One count, computed from the table's rows, written once in the caption and repeated verbatim in the abstract and the failures paragraph; the failures paragraph lists every FAIL row by its number. | a count of rows |
| 2 | p29 row 12; p1 abstract; p15 Section 5 | MUST-FIX | Row 12 is counted as a pass ("a fourth under the clock's assumed word") though the row itself says the reading is "not readable under the law as it stands" and the four worlds are being redeclared. The PASS is against the lattice pin 1.909 +- 0.05, a gate on the code; against nature's 2.00 the reading 1.907 is 4.6 percent off with no uncertainty stated on either side, so the row meets the caption's own PASS criterion ("within the stated uncertainty") nowhere. | Verdict "HISTORY: the lattice pin met (DETECTOR, the law before the entry); against nature 4.6 percent off, PENDING the weak-field re-read"; the abstract's "a fourth" struck; the pass count of finding 1 without it. | DETECTOR (historical) |
| 3 | p28 rows 7a and 8a | MUST-FIX | A GAMEBOARD number is used as a result. Row 7a's 0.109 percent is "the escaped 4 of 3677 (GAMEBOARD, the books)" over "the mass read 3673" (its kind not named). Row 8a's verdict "a factor 88 in the registered run, 25 to 40 at head" is nature's 3.17 over the lattice clock's widths 0.036 and 0.08 to 0.13, which the same row labels GAMEBOARD and "counted in no criterion". The paper's rule (record 281, P11): only a detector reading is compared with nature. | 7a: the binding fraction from the border clicks alone, or the row moved out of Table 2 as a GAMEBOARD diagnostic with its BOUND withdrawn. 8a: the verdict "a step, width 0 against nature's 3.17 (DETECTOR): FAIL"; the factors 88 and 25 to 40 struck or moved to a labelled GAMEBOARD aside. | GAMEBOARD used as DETECTOR |
| 4 | p29 row 13; p16 Section 5 "Light: no optical metric" | MUST-FIX | Section 5 says light beside a mass is FAIL against 1.75 arcseconds "(Table 2)", but Table 2 has no row carrying series K's FAIL; row 13 is PENDING a run under the key `flow_link` "with the root replaced", a rule under its own identity (a root is not one of the six verbs), and the caption's rule is that a hypothesis's PASS never changes the law's FAIL. As written the law's one reading of bending (0.000 pixel, DETECTOR) is in no row. | Row 13 carries the law's verdict now: deflection 0.000 pixel, delay 0.00 interval (series K, DETECTOR), FAIL against 1.75 arcseconds and against the Shapiro delay (finding 21); the `flow_link` run stands beside it under its identity with its pin 0.731 +- 0.025, PENDING. | DETECTOR |
| 5 | p27-28 row 6; p36 (i) | MUST-FIX | The C1 PASS ("the loop stays") is under the key `centred_step`, off by default, a hypothesis; the law as built reads "the electron escapes at 3407". The row's verdict for the law is therefore FAIL, and the hypothesis's C1 PASS and C2, C3 FAIL stand beside it. Further, the electron family carries no circle (h = 0, "no circle", page 34), so no rule of the law as built quantises the loop: Bohr's 27/20 is not NOT YET, it is not reachable by any run without a new rule, and the paper should say which. | Row 6: "the law as built: the electron escapes at 3407 (DETECTOR), FAIL; under `centred_step` (a key, off by default): C1 PASS, C2 and C3 FAIL; the lines: no rule of the six quantises a body's loop, so 27/20 is NOT COMPUTABLE under the law as built". Section 9 (i) the same. | DETECTOR |
| 6 | p31 "The step beneath and the step above"; p29-30 the quoted frame | MUST-FIX | Two sentences a page apart contradict: "In one chain, with nothing of Einstein's put in ... the symmetry of that conversion, the Lorentz group up to scale" against the frame's own words "Lorentz of the world is assumed, and what is shown is that this conversion brings it", and Highlights (record 772): "it does not prove Lorentz". A referee reads the first as a derivation claim and the second as its retraction. | Strike "with nothing of Einstein's put in". Say once: Outside is assumed Lorentz through (A1) and the relativity of the two directions (k_AB = k_BA); the click theorem shows the conversion consistent with that assumption to order m^2 v^2 under (A2), which the law as built lacks; nothing here derives the Lorentz group from the six verbs. | COMPUTATION |
| 7 | p26-29 rows 3, 4b, 12; p29 "Inside and Outside"; p15 Section 5 | MUST-FIX | The denominator of every 1 + z is "the click's tick" at a fixed open-face detector (series G2 and T, `docs/EXPERIMENTS.md`: "the inverse slope of the birth ordinal against the click's tick"). By the paper's own words on page 29 ("an open face without a body having none") and record 768 (TERMINOLOGY: the tick of a bodiless detector's click line is the record's ordering, GAMEBOARD), that tick is the host's interval. So the three redshift rows are a DETECTOR count over a GAMEBOARD clock, and the kind in the rows is wrong as written. | In each of rows 3, 4b and 12 name the time base: "births (DETECTOR) per host interval (GAMEBOARD, the open face's tick; the detector's own pulse-and-return clock NOT READ)"; or re-read with a detector that carries a body and its own clock (record 768) and keep DETECTOR. The platform paragraph's "every reading named here is DETECTOR" qualified the same way. | DETECTOR over GAMEBOARD |
| 8 | p26 row 1a; p29 the prediction paragraph | SHOULD-FIX | The PASS against Hensen's 2.42 +- 0.20 at N_phi = 64 has no power: any S in [2.02, 2.82] passes within two standard errors; and the same grain N_phi = 64 (S = 2.75) is excluded by Poh's 2.82759 +- 0.00051 three pages later. A row cannot pass at a grain the paper itself excludes without saying so in the row. | Row 1a: add "the window that would fail: S < 2.02 or S > 2.82; N_phi = 64 is excluded by row 1a's companion (Poh, page 29), the PASS is of the loophole-free source's precision, not of the grain". | DETECTOR |
| 9 | p27 row 2b | SHOULD-FIX | "visibility 1.000 above the apparatus-limited 0.98" rests on 64 births: the click resolves 1/64 = 0.016, and the dark port's offer 1/1682 makes a rung of width 64/1682 = 0.038 < 1, so zero clicks is the resolution's artefact and cannot be told from 0.98. The law's ideal, 0.9988, is the offers' (GAMEBOARD). | Verdict: "a bound met at the click's resolution 1/64, which does not resolve 1.00 from 0.98; the law's ideal visibility 0.9988 from the tables' rounding (GAMEBOARD, a diagnostic)". | DETECTOR; GAMEBOARD labelled |
| 10 | p28 row 9 | SHOULD-FIX | Malus's law has no published source in the row (the register's rule: one source per value). And 219/256 = 0.8555 at 22.5 degrees is off cos^2 = 0.8536 by 1.9 x 10^-3, the tables' rounding at N_t = 256: a precise Malus measurement bounds N_t exactly as row 5a bounds N_l, and the row should carry that bound, not a bare PASS. | Cite a measured Malus law with its precision; verdict "PASS at 45 and 90 degrees (exact); BOUND on N_t at 22.5 degrees: the tables' rounding 1/512 per component against the measurement's precision". | DETECTOR; the bound COMPUTATION |
| 11 | p26-27 row 2a | SHOULD-FIX | One row carries two verdicts (FAIL against a Mach-Zehnder reading; NOT COMPARED against the two-slit source "its figure to be verified against the source"). A submitted table cannot carry "to be verified". | Verify Jacques et al. 2005 (the biprism's 0.94) before submission; one verdict, bound against bound, with the fan's discreteness named as the cause of the 0.966. | DETECTOR |
| 12 | p27 row 2c; p19-21 Theorem 3 | SHOULD-FIX | "kappa not computed" understates the algebra: Theorem 3 forces every admissible click to be a quadratic form, and a quadratic form has no third-order term, so Sorkin's kappa is 0 exactly for the law, a consequence the paper already owns. Row 2c compares nothing where the paper's strongest theorem gives a number. | Row 2c: "kappa = 0 exactly, an identity of Theorem 3 (COMPUTATION), consistent with 0.0064 +- 0.0119; NOT COMPARED after a detector until a three-opening world is run"; Section 9 (ii) the same. | COMPUTATION |
| 13 | p29 row 14; p14 "The ground of these derivations" | SHOULD-FIX | Nature has no 1/r gravity on a plane: the pins 384 and 768 and the ratio 2.00 check the scale symmetry of a 1/r force (the period of a 1/r push grows as r), an analytic form, and the row's "nature's value" is that form's. The workflow's method: an analytic check is an empirical comparison only against sourced data. The confrontation with nature is Kepler's third law in space, 2^(3/2) = 2.83, with a source. | Label row 14 "analytic check: the 1/r form's scale symmetry on the plane, 2.00"; add the row that is nature's: the period ratio in space against Kepler's third law (2^(3/2), a sourced value), NOT MADE. | DETECTOR against an analytic form |
| 14 | p13-14 Section 4; p16 Section 5 | SHOULD-FIX | "the equivalence principle is exact" is the weak principle (universality of free fall, M_A cancelling) only. The flight reads nothing of the crowd, so light and clocks share no metric: Einstein's equivalence principle (the same local physics for light and clocks in a field) fails in the law as built, and a referee will read "exact" as the strong claim. | Write "the weak equivalence principle is exact"; add one sentence that the Einstein form is not met, light being blind to the crowd (row 13). | COMPUTATION |
| 15 | p13 Section 4 "Newton's law"; p5 P9; Table 2 | SHOULD-FIX | The drive saturates at one Link per interval, above c = 1/sqrt(3): "a body can outrun its own field's rows". So the law as built predicts massive bodies at up to sqrt(3) c, a detector-readable velocity (Nodes apart over counts apart, D3's controls) that nature never shows. The paper says the fact and does not name it as a prediction or a FAIL; Table 2 has no row. | A row: "the pace of a body against c: the law's cap 1 Link per interval = sqrt(3) c; nature: no massive body at c; the reading a body at high momentum through a line of detectors (D3's kind), pinned by the drive's formula; FAIL as declared" or NOT MADE with the pin. | DETECTOR (pin) |
| 16 | p13-16 Sections 4 and 5; p27-28 row 6 | SHOULD-FIX | The field is purely retarded at c with no velocity-dependent term (the flow the push reads is the arrivals' first moment, nothing of the reader's motion). Laplace's argument for a retarded central force gives a secular drift of a bound orbit's radius and angular momentum of order v/c per turn; the paper does not name it, though row 6's tightening from 12 to 7 Links over five turns with the period falling 1431 to 1040 looks like it. This is the first thing a physicist asks of a retarded inverse square. | Derive the per-turn drift from the retarded push at the loop's pace (a COMPUTATION), pin it, and read it on the D3 or the atom loop as a control (finding 22); state the comparison with the solar system's bound on such a drift (Laplace; the speed-of-gravity bound) and its verdict, or name it NOT MADE with the pin. | COMPUTATION; DETECTOR (pin) |
| 17 | p27 row 5a; p18 P1's bound | SHOULD-FIX | The bound N_l >= 5.8 x 10^17 with the registered fan (|D| <= 6) gives the flight's wall 2 T_D = 2 sqrt(3) |D| N_l of about 1.2 x 10^19, above the working bound 2^63 - 1 = 9.2 x 10^18 the paper names on page 18; the law refuses such a run. The BOUND is not reachable inside P1's declared integers with the registered fan. | Add to row 5a: "reachable only with a wider integer or a fan of |D| <= 4; the working bound is the host's (record 558)". | COMPUTATION |
| 18 | p26 Table 2, every row | SHOULD-FIX | The law's side has no uncertainty column: the grain (1/N_phi per cell, the tables' rounding 1/512 per component, the fan's L1 factor 1.07/0.97, the drive's anisotropy 0.069, the digital line's landings) appears in prose in some rows (3, 2a) and nowhere in others (9, 2b, 1a). The PASS criterion "within the stated uncertainty" is then one-sided. | One column "the law's grain" per row with its source (the ledger's caption names the three grounds; the rows name none), and the criterion applied to both sides. | COMPUTATION |
| 19 | p32 "The smallest thing above" | SHOULD-FIX | "why the world above the board is quantized, a theorem of (A1)" conflates the integer read-out (counts and Nodes) with nature's quantisation (levels, spin, h). The paper's h is an input (Table 1), its levels NOT YET (row 6) and its velocity quantum "not read as such". | "integer-valued" for what the click reads; "quantised" kept for what is not derived; one sentence that the levels are not reached. | COMPUTATION |
| 20 | p23-24 Section 7, "No-signalling in the times" | SHOULD-FIX | The second party's outcome "is fixed at the completion from the joint weights", and the completion is the later of the two arrivals, so the interval at which the second party's outcome exists depends on the first arm's length. The paper calls this bookkeeping; a physicist reads that a detector at B that must record at its own tick has no outcome then, which nature's detectors do not show. The arrival's independence is stated; the outcome's is not, and is false. | State it: "the second party's outcome is not defined before the first arm's rows end; a detector recording at its own tick reads nothing of the law's outcome until the completion; the times' no-signalling is of the arrivals alone". | COMPUTATION |
| 21 | p16 Section 5; p26 Table 2 | SHOULD-FIX | Series K reads the delay beside a mass as 0.00 interval (DETECTOR). Nature's Shapiro delay (Cassini: gamma - 1 = (2.1 +- 2.3) x 10^-5; Shapiro 1964) is a second dimensionless FAIL of the same run, and it is in no row. | A row 13b: the delay, 0.00 against the Shapiro form's (1 + gamma), FAIL as declared, with the source. | DETECTOR |
| 22 | p14-16 Sections 4 and 5; p41 Appendix C | SHOULD-FIX | No control world is named for the forces and the clock: a Newton world with the push off (does the drive alone hold the D3 loop?), a clock world with no crowd (the tick's baseline, record 569 is cited in the register but not in the paper), a pair world with the chooser's period not coprime to N_phi (the marginal's failure the paper computes and does not run). The two-slit's one-slit control and the presence-word clock are the only controls named. | One line per Section 4 to 7 naming the control world, its reading and its kind, or NOT MADE. | DETECTOR |
| 23 | p15-16 "The clock's redshift" | SHOULD-FIX | "the calibration a_tau = GM/rc^2 ... is a constraint on the inputs" is asserted; the constraint is not written. A reader cannot check that the calibration is not a free fit once G = K eta / (4 pi N_w) is fixed. | Write the one equation: the clock's constant C_a (the pair [n_c, d_c] times tau_L / (4 pi c)) against G / c^2, the ratio a declared number of the world; say which inputs it ties. | COMPUTATION |
| 24 | p36 "What the law names and has not computed" (the commit f0aca570 after the ordered SHA) | SHOULD-FIX | The new paragraph is right to exist and its items are honest; but (v) says "the field at a galaxy's edge is Newton's in the shell mean and the detector adds nothing there" while row 14 says the inverse square in space is NOT MADE: the paragraph claims the shell-mean form at a scale where no reading exists. And item (vi) "an input in (vii) above" points to nothing above. | (v): "Newton's in the shell mean by Section 4's derivation, at no scale read after a detector"; (vi): fix the cross-reference. | COMPUTATION |
| 25 | p1-2 abstract; p26 caption (the same commit) | SHOULD-FIX | The rebuilt PDF of f0aca570 keeps the abstract's counts of finding 1 unchanged while adding the paragraph; NUMBERS.md's new line says the paragraph "adds no number", which is true, but the count mismatch of finding 1 is now the one number of the abstract with no row in NUMBERS.md. | With finding 1: one line in NUMBERS.md for the verdict counts, kind "a count of the table's rows", and the abstract read from it. | a count of rows |
| 26 | p10-12 Section 3 "What a detector measures" | SHOULD-FIX | Series Q's pace 0.5718 to 0.5893 at finite ages against the table's 0.5774 to 0.5818: the finite-age band exceeds the asymptotic band by 0.0075 above and the ages are not given, so a reader cannot apply the 1/T_D bound of Proposition 1 and the paragraph has no verdict word. | Give the ages, the per-direction bound 1/T_D at those ages, and the verdict (every click inside the bound, PASS as a gate on the code). | DETECTOR |
| 27 | p22 "Planck and de Broglie, as identities"; p5-6 P7, P8; p13 N_w; p15 the calibration; p20 the tables; p6 the wheel 2531/4096 | SHOULD-FIX | The inputs are scattered over Sections 2, 4, 5, 6 and 9 with no one table (record 817): h = h_q N_phi = h_A, N_w (Newton's constant), rho (the hierarchy 1.1 x 10^18), the masses M, the clock's pair, the calibration a_tau, N_phi, the tables at 1/256, the wheel's rate 2531/4096, the mass angle m, gamma = 1 for the bending. The ledger's third column names some per result; the reader who asks "which recoveries are identities of the definitions" must assemble the answer. | One inputs table: the input, where declared, its kind (grain, dictionary, family table, world), and the results that are identities of it (Planck, de Broglie, E_0 = N_l N_w M and W, the clock's 1/r calibration, G, k_C = G, rho_p). Every "recovered" in the abstract then points to a row. | inputs |
| 28 | p28 row 8a | NIT | "the registered J1 run predates the one flight wall ... kept as history, J1's redeclaration in the weak field after the paper" softens a FAIL by promising a re-read. | The verdict is the law's at the named commit; the redeclaration, if wanted, is its own NOT YET line. | DETECTOR |
| 29 | p29-30 the quoted frame | NIT | kappa, omega and m stand alone as letters in the quotation ("(1 - kappa^2/6)", "cos omega = cos m cos kappa") against the notation rule (every symbol named at first use, record 184). | Name them once before the quotation: omega (the walk's frequency), kappa (the momentum per Link), m (the mass angle). | none |
| 30 | p37-39 bibliography | NIT | Three references are branch heads "pending merge" (the order channel at 389dc5d1, the atom's centred step at 686673f7, the register's PR #860 at b12dd253). A submitted paper cannot cite an unmerged branch. | Replace each with its merge commit before submission, as the text already promises. | none |
| 31 | p1 abstract | NIT | "a fourth under the clock's assumed word (read under the law before the generic entry of 2026-09-22)" names a dated repository event a reader cannot see; "181/64 from 512 to 8192" appears before S is defined. | Say "under a historical form of the clock" or drop (finding 2); define S in the sentence. | none |
| 32 | p19 Theorem 3, hypothesis (b) | NIT | The balanced splitter's conservation is called "an axiom of the apparatus" here and "a hypothesis on the reading" two lines later, and the ledger calls it an axiom. | One word; "axiom" if the paper means it is put in, and the ledger's row unchanged. | none |

## What is missing

Ordered by weight, the heaviest first.

1. **The inputs table** (finding 27; record 817). Without it a referee cannot
   separate the recoveries that are identities of the dictionary (Planck, de
   Broglie, the energy relation W, the clock's calibration) from the results
   the six verbs force (Gauss, the marginals, the quadratic form, S(N_phi)).
   The paper knows the difference row by row; it does not show it in one
   place.
2. **An error budget on the law's side, and a systematics list** (finding 18).
   The grains (1/N_phi, 1/512, the fan's L1 factor, the drive's anisotropy
   0.069, the axis-order tie x before y before z, the digital line's
   landings) are named in prose across the paper; no row of Table 2 carries
   them as its uncertainty, so every PASS and FAIL is one-sided.
3. **The time base of every detector** (finding 7). Record 768 decided what a
   detector's clock is; the redshift rows read against the host's interval
   and do not say so. This is where a locality referee will look first.
4. **Falsifiable predictions the paper has and does not name**: a massive
   body at up to sqrt(3) c (finding 15); the secular drift of a bound orbit
   under the retarded push (finding 16); Sorkin's kappa = 0 exactly (finding
   12). The paper names three others honestly (the moving clock's rate 1,
   the strong-field clock's 1 - a + a^2, the second party's serial
   correlation); these three belong beside them.
5. **Comparisons the paper avoids**: the Shapiro delay from the same series
   K run (finding 21); Kepler's third law in space against the plane's 1/r
   check (finding 13); the solar system's bound on a retarded force
   (finding 16). Each is a row the register can carry now.
6. **Control worlds** (finding 22): the push off, the crowd absent, the
   chooser not coprime to the wheel. A referee asks for the null before the
   effect.
7. **A figure that shows a mechanism** the text only describes: the drive's
   per-axis staircase for a diagonal body (the coincident fire lost, the
   anisotropy 0.069); the comb of beams at one Node against the shell mean
   (Section 4's "on one Node the inverse square exists only in the limit");
   the pair's ladder of four cells with the coarse rung at N_phi/2 and the
   fine rung within it (Section 7). Figures 1 and 2 draw the board and the
   click; no figure draws a force or a pair.
8. **A column for the identity a row runs under** (findings 4, 5): rows 6 and
   13 read under keys off by default; the caption's rule that a hypothesis's
   PASS never changes the law's FAIL needs the key visible in the row.
9. **Which rule would give the atom its lines** (finding 5): the electron
   family has no circle; the paper should say that no run of the law as
   built can reach Bohr's 27/20, not that it has not been made.

## What stands

1. Theorem 3 (page 19): the click's reading forced to a positive quadratic
   form on the phase lattice from the balanced splitter's conservation, the
   rotation and the counts, with the two extra hypotheses (d) and (e) named
   and the unforced harmonic constants c_j stated as not derived. This is a
   real result, honestly bounded.
2. Section 7 with row 1c: the exact marginals, S(N_phi) an exact rational with
   181/64 read after a detector at six grains, and the order channel's FAIL
   found by the paper's own reading and written as the law's determinism
   showing in the order. A referee trusts a paper that reports its own
   signalling.
3. Section 2: one map with a rate and a wall, six verbs, the hand-worked
   update, no floating point, every world run from its file with its pin
   before the run; every FAIL in Table 2 carried as the law's own with the
   number. The law is specified well enough to be refuted, which most
   discrete proposals are not.

## Verdict

MUST-FIX 7 (findings 1 to 7); SHOULD-FIX 20 (findings 8 to 27); NIT 5
(findings 28 to 32). The diff of the branch head f0aca570 against the ordered
6f953920 (one paragraph of Section 9, one line of NUMBERS.md) is covered by
findings 24 and 25 and adds no MUST-FIX.
