# The physicist's read of the paper: every physical claim CONFIRMED or NOT CONFIRMED against the contracts (the Paper Verifier, physicist, 2026-09-24; docs only, no run, no pin moved)

**The paper read.** `paper/general_formula/main.tex` on the branch
`paper-48` at its head `6473d8f96b658c5ba1bc91aaa50483a91e966e97`
(commit 34, 2026-09-24 02:05Z), with `records.tex` at the same head as
context. **The contracts read**, all on `main` at
`324244f0f19cb4819581e4305b215fa00ba23d7e`: `AGENTS.md`,
`skills/workflow.md`, `docs/TERMINOLOGY.md`, `POSTULATES.md` (sections 10
and 26), `docs/HIGHLIGHTS.md` section 5.4, `docs/ALGEBRA.md` (chapters 1,
3, 4, 5, 8), `docs/designs/fail_rows/STATUS_RULES.md`,
`docs/designs/detector_law/ALGEBRAIC_CLOSURE.md`,
`docs/designs/detector_law/declarations/DECLARATIONS.md`,
`docs/designs/detector_law/SCHEDULE.md`, `docs/designs/detector_law/PINS.md`,
`docs/designs/detector_law/APPROVALS.md`,
`docs/designs/detector_law/EXPLORATION.md`, `docs/NATURE.md`,
`docs/designs/detector_law/SOURCES_VERIFIED.md` (the 58 rows: 48
VERIFIED, 2 CORRECTED, 8 NOT FOUND), `docs/EXPERIMENTS.md` (the Bell
plateau's entries), `docs/DERIVATIONS_BEAM.md` (the table of S(N) against
the measurement) and `docs/designs/detector_law/LIGHT_DISPERSION_BOUND.md`.
**The reader:** the physicist verifier opened by the Boss on the model
owner's word of 2026-09-24 02:02Z; session
`session_01PVKCdcQVGW7uUj8XjQp59o`; branch `paper-verify-physics` from
`origin/main`. **Date:** 2026-09-24.

**What this page is.** One line per physical claim of the paper: every
sentence that says the law gives, predicts, matches, fails, derives or
bounds a physical quantity or an experiment, every number compared with
nature, every kind word (MET, FAIL, EXPLORATORY, COMPUTATION, DERIVED,
CONJECTURED, HYPOTHESIS, K, P, GAMEBOARD, DETECTOR) and every provenance
word. CONFIRMED means: the claim is what the contracts say, its kind is
right, its nature value is the verified one and its source is cited. NOT
CONFIRMED gives the reason in one sentence with the contract's line. This
page is a proposal: it changes nothing in the paper; the writer folds
only on the Boss's word. The mathematician verifier reads the definitions,
theorems and numbers in parallel; the proofs are his and are not judged
here.

**The rules the paper is held to** (AGENTS.md; HIGHLIGHTS 5.4, the
measurement rule; STATUS_RULES.md steps 1 to 7; SCHEDULE.md's head):
a GameBoard reading is a labelled diagnostic and never a result; only a
detector's click is a measurement; a pin is declared before the run and
never moved; "matches nature", never "is nature"; a hypothesis
(pair-field-v1, covariant-readings-v1, flow-link-v1, centred-step-v1
and the like) is never stated as the law; the count of agreements comes
only from the closed rows; every reading of the engine before 2026-09-23
is HISTORY, labelled so wherever it is cited (HIGHLIGHTS 5.4, the owner's
words of 2026-09-23 about 08:22Z: "every reading not re-read so is
history, and no old reading stands as the law's"; SCHEDULE.md: "never
carried into the paper's table").

**Symbols named once.** S is the CHSH sum (Clauser, Horne, Shimony and
Holt); N_phi is the phase grain, the number of steps of the phase circle;
c is the pace of light on the lattice; gamma is the Lorentz factor;
beta is a speed as a fraction of c; omega_0 is the pitch, the rest
frequency of a massive kind; c_m and c_eff are the massive kind's
second-order and exact cones; gamma_m is the Lorentz factor at c_eff;
gamma_PPN is the parametrized post-Newtonian space-curvature coefficient;
q is the deceleration parameter; W is a detector's rung; u is the birth
wheel's reading; E is the correlation of a pair at two settings.

## The table

The section is the paper's; the line is the paper's line in `main.tex`
at the head above. (K) is a known-formula row, (P) a prediction row, as
SCHEDULE.md and ALGEBRAIC_CLOSURE.md define them.

| Section (line) | The claim, in ten words | Verdict | The reason, with the contract's line |
| --- | --- | --- | --- |
| Abstract (50) | Exact on the lattice: the books, Gauss's law, every direction's pace | CONFIRMED | ALGEBRA.md chapter 4 lists the conservation books, Gauss's law under its world condition and the pace of every direction as exact identities; "What is proved" (390) names the world condition |
| Abstract (50) | The CHSH sum 181/64 exact from N_phi 512 to 8192 | CONFIRMED | HIGHLIGHTS 5.4 (issue 368): "the powers of two from 512 to 8192 give 181/64 exactly"; DERIVATIONS_BEAM.md 7123 to 7135, the same table; a COMPUTATION of the algebra, the pinned column of Table 1 blank |
| Abstract (50) | 181/64 is 1.05 standard errors from the measurement | NOT CONFIRMED | The arithmetic is right (DERIVATIONS_BEAM.md 7123: +1.05 at 512 to 8192), but the measurement, Poh et al. 2015's 2.82759 +- 0.00051, is neither in NATURE.md row 1a (which cites Hensen's 2.42 +- 0.20 and Cirel'son's bound only) nor among the 58 verified values of SOURCES_VERIFIED.md; nature's value is not the verified one |
| Abstract (50) | Recovered in limits: c = 1/sqrt 3 | CONFIRMED | Proposition 1 (421 to 453): the isotropic bound attained on the body diagonals; "claims no novelty for the number" (453); ALGEBRA.md chapter 4, the pace |
| Abstract (50) | Tsirelson's value in the joint limit of grain and tables | CONFIRMED | Theorem 6 and 679: the fixed-table limit 186034/65773, 2 sqrt 2 the joint limit in N_phi and N_t; HIGHLIGHTS 5.4 (issue 368), the same statement |
| Abstract (50) | Under a shell average Newton's inverse square | CONFIRMED | ALGEBRA.md 5.6 (1416 to 1420) accepts this very sentence: "the paper's opening ... already says only that"; hypotheses (A1), (W1) to (W5), (M), no (A2); a reached form, not a reading |
| Abstract (50) | Under two hypotheses Lorentz's factors and Einstein's step reached | CONFIRMED | ALGEBRA.md 5.1 (the click theorem under (A1), (A3), (A2) for the scale) and 5.5 (Einstein's step); "reached", not "derived", the owner's word of 2026-09-22 (HIGHLIGHTS 5.4, the paper opens with the algebraic object) |
| Abstract (50) | The equivalence principle under the first hypothesis alone | NOT CONFIRMED | ALGEBRA.md 5.4 names the hypotheses (W1), (W2), (M), with (A1) and (A3) only for the accelerated detector; the paper's body (72) says "(A1) and five assumptions of the law as built"; the abstract drops the five, a claim stronger than the row |
| Abstract (50) | The law as built meets (A1) only | CONFIRMED | ALGEBRA.md 5.1 and 5.3; HIGHLIGHTS 5.4, "Lorentz, A": the rows hop whole, no staying amplitude; STATUS_RULES row 4a: no verb makes a count depend on the momentum |
| Abstract (50) | Only a detector's counts and ratios compared with nature | CONFIRMED | HIGHLIGHTS 5.4, the measurement rule; POSTULATES.md section 10 (657 to 668); STATUS_RULES step 1 |
| Abstract (50) | Every number computed before its run, pinned readings blank | CONFIRMED | APPROVALS.md section 3: "Check 3: 0 of 19"; SCHEDULE.md: the pin declared before the run and never moved |
| Abstract (50) | A miss written as a miss | CONFIRMED | APPROVALS.md section 0: "written as a miss, in the paper's table, by kind; no pin moves after a reading" |
| Abstract (50) | The bending's 2(1 + gamma) and the 1/j^2 ladder are conjectures | CONFIRMED | Labelled conjecture, not read, throughout (390, 484, 829); ALGEBRA.md 5.9 gives C_ring 3.652 to 3.918 against 4 (1784) and 5.8 the ladder NOT READ (1696); a weaker word than the contracts' COMPUTATION, allowed |
| Abstract (50) | The law as built has no relativistic dynamics | CONFIRMED | STATUS_RULES rows 4a, 4b, 5b: "no verb makes a count depend on the momentum ... nothing contracts"; SCHEDULE.md, PINS.md 4a: FAIL under the declared clock |
| Abstract (50) | The sequential wheel signals in a pair's order, not counts | CONFIRMED | A COMPUTATION from Theorem 5's cells (638) and STATUS_RULES row 1c (the wheel a counter, the order deterministic); the counts blind by Theorem 5 |
| Introduction (57, 61) | c^2 = 1/3 from the six reads, isotropic at leading order | CONFIRMED | ALGEBRA.md 8.1: light's band cos omega_l = (cos k_x + cos k_y + cos k_z)/3, omega^2 = k^2/3 + O(k^4); LIGHT_DISPERSION_BOUND.md 29 to 43 |
| Introduction (61) | The departure from isotropy appears only in the cubic pattern of the 48 | CONFIRMED | LIGHT_DISPERSION_BOUND.md 29 to 43: the coefficient 3 sum n_i^4 - 1, no free coefficient; SCHEDULE.md row A2 |
| Introduction (62) | Every record kind has one pair: light [1, 1], matter [800, 809] | CONFIRMED | ALGEBRA.md 402 and 8.1; BUILD.md 214 to 235 (the kind [800, 809]) |
| Introduction (64) | With the coupling the body emits and absorbs in one division | CONFIRMED | ALGEBRA.md 8.5: the coupling one entry of the declared matrix, one division per row |
| Introduction (67) | The word is matches, never is | CONFIRMED | SCHEDULE.md's head: "matches nature", never "is nature"; used so in the paper |
| Introduction (72) | Newton's inverse square from clicks under a shell average, reached not derived | CONFIRMED | ALGEBRA.md 5.6, hypotheses named; "reached from the algebra, not derived from nothing" is the owner's wording (HIGHLIGHTS 5.4, 2026-09-22) |
| One page (74) | The list closed in the algebra before any run, none read yet | CONFIRMED | ALGEBRAIC_CLOSURE.md section 1 (CLOSED 19 rows); APPROVALS.md section 3 (Check 3: 0 of 19) |
| One page (74) | The hypotheses beside rows 6, 13, 14 change no verdict of the law | CONFIRMED | APPROVALS.md section 2: under pair-field-v1 only, "never in the paper's place"; ALGEBRAIC_CLOSURE.md section 3 item 4 |
| One page (74) | The ring's constant does not close within the grain | CONFIRMED | HIGHLIGHTS 5.4 (2026-09-22, flow-link-v1): "the constant DOES NOT CLOSE within the grain"; ALGEBRA.md 1934 |
| One page (74) | The ladder not read: no lattice holds the atom's scale | CONFIRMED | ALGEBRAIC_CLOSURE.md row 6: "hydrogen's a_B is 527 Links at mu = 0.15"; SCHEDULE.md row 6 |
| One page (74) | 181/64 inside Poh et al. at 1.05 standard errors, a prediction once no-signalling in order is met | NOT CONFIRMED | The same value as the abstract's: Poh's 2.82759 +- 0.00051 is not in NATURE.md row 1a and not among the 58 verified values; the conditional clause itself is right (STATUS_RULES row 1c) |
| General formula (87) | Only a detector's reading is a measurement | CONFIRMED | HIGHLIGHTS 5.4, the measurement rule; POSTULATES.md section 10 |
| Why physics behaves (93) | Nothing measured is a real number; every quantity a count or a ratio | CONFIRMED | ALGEBRA.md 3.4, discreteness Outside; Theorem 3 (373) |
| Why physics behaves (93) | The click families' symmetry is the Lorentz group up to scale | CONFIRMED | ALGEBRA.md 5.1, the click theorem, under (A1) and (A2); the paper names both (378, 380) |
| Why physics behaves (93) | Row 2a's lamp declares 128 periods because nature's visibility is 0.98 | NOT CONFIRMED | The paper's own Table 1 row 2a gives nature 0.94 (Jacques 2005); NATURE.md row 2a says no two-slit figure is at hand, 0.98 is the Mach-Zehnder proxy of row 2b and 0.94 the biprism's; one row with two nature values in one paper, neither verified in SOURCES_VERIFIED.md |
| Why physics behaves (93) | An explicit model with exact and conditional results, and checks after a detector | CONFIRMED | The ledger's framing; APPROVALS.md's three checks |
| Reading rule (97) | A click is an action of the law on the state | CONFIRMED | POSTULATES.md section 10, the addition of record 1421 (657 to 668): "an action of the law on the state"; HIGHLIGHTS 5.4 (2026-09-23, record 1139) |
| Contributions (104) | Not claimed: a unique prediction of 181/64 without a rule fixing the grain | CONFIRMED | Theorem 6's dependence on N_phi and N_t; DERIVATIONS_BEAM.md 7137 to 7143 (the plateau's five grains) |
| Section 1, the objects (158) | At N_phi = 8192 only 1952 table pairs distinct; two rows read (0, 0) at 5.9e-7 | CONFIRMED as COMPUTATION | Labelled a computation from the tables (gleasonbound), not a run; a fact of the tables |
| Section 1, the click (289 to 301) | Born's form recovered to 1/N_phi; the square, the uniform u and the tables put in | CONFIRMED | ALGEBRA.md 4 (the click's weight the one positive quadratic form, P10); the three inputs named as inputs |
| Section 1 (300) | The choosers' periods 3 and 5 against N_phi = 64 make u independent of the settings | CONFIRMED | A fact of the registered world, stated as such; the coprime condition |
| Section 2, the pair per kind (318) | The three tests hold for the massive rule | CONFIRMED | ALGEBRA.md 8.10: the rule with the pair, (B), (T), (D), the band and the two paces proved |
| Section 2, the band (320 to 324) | cos omega = cos omega_0 cos omega_l(k), proved for every grain and periodic board | CONFIRMED | ALGEBRA.md 8.1, the band; the rest energy h omega_0 as the thing compared with |
| Section 2, the cones (326) | c_m^2 = cos omega_0 c^2, 0.39 percent below at N_0 = 50, COMPUTATION | CONFIRMED | ALGEBRA.md 2272: "0.39 percent at N_0 = 50" (COMPUTATION) |
| Section 2, the cones (328 to 330) | c_eff^2/c_m^2 = omega_0/sin omega_0, 1.0037 at mu = 0.15; two gammas | CONFIRMED | ALGEBRA.md 2283: "1.0037" (COMPUTATION); SCHEDULE.md prediction 1's second face |
| Section 2, light against itself (334 to 336) | The dispersion coefficient 0, 1/2, 2, 4/5; a prediction of the form; nature has bounds only | CONFIRMED | LIGHT_DISPERSION_BOUND.md 29 to 46, the same four values and the same falsifier; SCHEDULE.md row A2 (P) |
| Section 2, the block (338) | Two regimes, the well and the cavity; nothing declared in motion | CONFIRMED | ALGEBRA.md 8.3 and 8.4; SCHEDULE.md's cavity note (a rest control only) |
| Section 2, the motion (340 to 344) | The one formula computed not proved: 0.01 percent for s >= 12 on a chain, 0.15 percent on a layer | CONFIRMED | ALGEBRA.md 2505: "to 0.01 percent for s >= 12 and 0.15 percent on the layer" |
| Section 2, the motion (344) | Row 4a's number 0.8116 at the exact cone; 0.8108 and 0.8132 the controls | CONFIRMED | ALGEBRA.md 2848 to 2851; MASSIVE_RECORD.md 1148; EXPLORATION.md 38 (the layer pin world, 0.8116) |
| Section 2, the coupling (346) | The invariant J exact to 1e-12 on a chain; the amplitude form withdrawn as tachyonic | CONFIRMED | ALGEBRA.md 2586 (1e-12, COMPUTATION) and 2549 (tachyonic) |
| Section 2, the coupling (346) | The index n^2 = 1 + Gg/(omega_0^2 - omega^2), the 4 percent open in size | CONFIRMED | ALGEBRAIC_CLOSURE.md row v: "K CONTROL with the 4 percent open in size"; SCHEDULE.md's index note |
| Section 2, the detector (348) | The click the comparison W x pointer >= norm, integers both | CONFIRMED | ALGEBRA.md 8.6, the click of a body at W |
| Section 2, the direction of time (350) | The Inside reversible bit for bit, the click the one deletion; a check never a pin | CONFIRMED | ALGEBRA.md 8.8; SCHEDULE.md prediction 7 with its falsifier |
| Section 2, predictions (352) | The eight predictions of the massive kind, each with its falsifier | CONFIRMED | SCHEDULE.md's list of eight (P) rows; ALGEBRA.md 8.9 (2867); the paper's eight are the same eight |
| Section 3, the steps (363) | The detector's own count under clock_stamp, DETECTOR | CONFIRMED | STATUS_RULES step 1: the line's time is DETECTOR only under clock_stamp |
| Section 3, Theorem 2 (371) | Locality Outside under (A1), the pair's gather the one exception | CONFIRMED | ALGEBRA.md 3.4, two theorems; HIGHLIGHTS 5.4 (2026-09-23, the two theorems beside P11) |
| Section 3, Theorem 3 (374) | Discreteness Outside: every quantity a count or a ratio | CONFIRMED | ALGEBRA.md 3.4; the owner's line that Outside is quantized |
| Section 3, the one fact (378) | The support bound and Weyl's relation are the transform's mathematics, on a hypothesis of the programme | CONFIRMED | Labelled a hypothesis of the identification (607); ALGEBRA.md chapter 5's word |
| Section 3, the one fact (378) | E(a, b) = cos(2 pi (a - b)/N_phi) within rounding; marginals exactly 1/2 | CONFIRMED | Theorem 5 and Theorem 6, Eq. (ebound); ALGEBRA.md 4.9 (no-signalling a theorem of the click's form) |
| Section 3, the one fact (378) | S = 176/64 = 2.75 at N_phi = 64 against 2.42 +- 0.20 (row 1a) | CONFIRMED as HISTORY | NATURE.md row 1a: S = 2.75, within 1.65 standard errors of Hensen (VERIFIED); a reading of the engine before 2026-09-23, cited with "the full record" and history elsewhere (74) |
| Section 3, Inside and Outside (380) | The counter runs at the rest rate at every speed (rows 4a, 4b); the measurable 1 - v^2 | CONFIRMED | STATUS_RULES rows 4a, 4b; ALGEBRA.md 3.3 (the two one-way factors) |
| Section 3, the step above (380) | W shown to second order under (A1), (A2); declared on the rows' dynamics | CONFIRMED | ALGEBRA.md 5.3: the energy-momentum relation and the identity's exact square; "declared" for W on the rows (742) |
| Section 3, the smallest thing (380) | 1/c_D^2 = 2.954, 2.971, 3.000 by direction; 1/sqrt 3 in the limit | CONFIRMED | ALGEBRA.md 5.7 (light Outside); Proposition 1's interval |
| Section 3, Newton (380) | The register's D3, T and X are their confirmation; the inverse square's reading not made | CONFIRMED as the contract's line, HISTORY | ALGEBRA.md 5.4 (1305 to 1309) itself writes "MET: series D3 ... DETECTOR"; these are readings of the engine before 2026-09-23, the paper's "confirmation" carries no HISTORY label here (see the class line below) |
| Section 3, the chains (380) | Young's bands 23.5 pixels apart for 23.3 (L2b, DETECTOR) | NOT CONFIRMED | A reading of the engine before 2026-09-23 cited as DETECTOR with no HISTORY label; SCHEDULE.md row 2a: the old readings HISTORY; HIGHLIGHTS 5.4 (2026-09-23): no old reading stands as the law's |
| Section 3, the chains (380) | The clock's shift ratio 1.907 for the pin 1.909 (series T, DETECTOR) | CONFIRMED as HISTORY | Labelled "read before the generic entry ... not readable under the law as it stands"; NATURE.md row 12: 1.907 under the age word, HISTORY |
| Section 3, the chains (380) | The fall the same Node on 138 of 139 births, four masses (D3, DETECTOR) | NOT CONFIRMED | ALGEBRA.md 5.4 carries it as MET, but the paper cites it as a current DETECTOR reading without the HISTORY label the schedule requires of every reading before 2026-09-23 |
| Section 3, the chains (380) | The pair: S = 2.75 and 32/64 in every bin (series L, DETECTOR) | NOT CONFIRMED | The same class: the engine before 2026-09-23, no HISTORY label at this citation |
| Section 3 (i) (380) | The quantum of the step read in series S's face clicks 369 and 345 (DETECTOR) | NOT CONFIRMED | Series S is read under the key covariant_readings, a hypothesis's reading (STATUS_RULES row 4a: "DETECTOR, a hypothesis's"); the paper names neither the key nor HISTORY at this line |
| Section 3 (ii) (380) | The bound 8/N_phi + 0.0444; S = 3 at 16 and 32; the plateau; 5793/2048 at 16384 | CONFIRMED | HIGHLIGHTS 5.4 (issue 368); DERIVATIONS_BEAM.md 7123 to 7135 |
| Section 3 (ii) (380) | Measured at seven N_phi, the figure of the engine before 2026-09-23, history | CONFIRMED | Labelled history; EXPERIMENTS.md 4222 to 4313 |
| Section 3 (iii) (380) | The perihelion: FAIL on the law, pinned in order and symmetry, the coefficient NOT MADE | NOT CONFIRMED | No detector reading, no register row and no pin before a run stands behind the word FAIL; STATUS_RULES step 5: "a disagrees with no number is not a disagrees"; the Einstein Outside page's algebraic estimate is a COMPUTATION, the right word |
| Section 3 (iv) (380) | The anisotropy of c: series Q, 290 of 290, DETECTOR | NOT CONFIRMED | A reading of the engine before 2026-09-23 with no HISTORY label; SCHEDULE.md row 5a: the old reading HISTORY, the new pin a COMPUTATION on the rule's band |
| Section 3 (v) (380) | The register's clock and crowd worlds declare nS/d = 16 (GAMEBOARD) | NOT CONFIRMED | A declared input of a world file is kind INPUT by STATUS_RULES step 1, not GAMEBOARD; the kind word is wrong |
| Section 3 (v) (380) | The constant's reading NOT MADE | CONFIRMED | ALGEBRA.md 5.4, the clock's constant; no row of NATURE.md reads it |
| Section 3 (vi) (380) | Light's bending at head: -1.993 pixel at gamma_PPN = 0 (DETECTOR, the pin met) | NOT CONFIRMED | NATURE.md row 13 has the reading, but SCHEDULE.md row 13 under the law as it stands is NOT PREDICTED with "-1.993 and -3.989 pixel (HISTORY)"; the paper states it as "the law at head" with no HISTORY label |
| Section 3 (vi) (380) | Series K's 0.000 pixel, history | CONFIRMED | Labelled history; NATURE.md row 13 |
| Section 3 (vi) (380) | The ring under flow_link: the gamma = 1 ring 0.731 against 0.731 +- 0.025 (DETECTOR); the constant outside the one-grain pin by 2.40, 1.07, 1.40 grains | CONFIRMED as a hypothesis's reading | HIGHLIGHTS 5.4 (2026-09-22): flow-link-v1 off by default, "the deciding pin inside, the constant DOES NOT CLOSE"; ALGEBRA.md 1934; named under its key in the paper |
| Section 3 (vi) (380) | The conjecture: the deflection coefficient 2(1 + gamma) on the one constant | CONFIRMED | Labelled conjecture, not read; ALGEBRA.md 5.9's C_ring 3.652 to 3.918 against 4 (1784) |
| Section 3 (vii) (380) | Dark energy's shape: q_eff = -2 g_1/(1 + g_1), an apparent acceleration with nothing accelerating | CONFIRMED | ALGEBRA.md 5.7 and the dark energy page (a derivation, no run); stated as a property of the conversion |
| Section 3 (vii) (380) | Series G read the accelerating form; the coasting q = -0.108 in 0 +- 0.25 (G2); row 3 not predicted | CONFIRMED as HISTORY, the label missing | NATURE.md row 3: q = -0.108 inside the coasting bracket, the row not predicted / disagrees by STATUS_RULES; SCHEDULE.md row 3 NOT PREDICTED, HISTORY; the paper says "not predicted" but not "history" |
| Section 3 (vii) (380) | The supernova diagram stated as a failure, not a resolution | CONFIRMED | HIGHLIGHTS 5.4 (2026-09-21, the far lamp): q_eff = +1 against nature's, a FAIL that stays |
| Section 3 (viii) (380) | The atom's ladder a_j/a_i = (j/i)^2, 27/20, conjectured and not read | CONFIRMED | ALGEBRA.md 5.8 (1696): "NOT READ; Balmer's ratio ... 27/20 = 1.35 NOT" read; ALGEBRAIC_CLOSURE.md row 6 REPLACED |
| Section 3 (viii) (380) | The Bohr radius over the proton's radius about sixty thousand | CONFIRMED | 5.29e-11 m over 0.84e-15 m is 6.3e4; standard constants, not a row of the register |
| Section 3 (viii) (380) | Row 6 stays NOT YET on the line | NOT CONFIRMED | The word is NATURE.md's old cell; under the current contracts row 6 is NOT COMPARED (SCHEDULE.md), REPLACED by the atom's lines (ALGEBRAIC_CLOSURE.md) and not predicted (STATUS_RULES); the paper's own Table 1 carries row 7, the atom's lines, in its place |
| Section 3 (viii) (380) | The hydrogen loop at r = 12 escapes at 3407 intervals (DETECTOR), the law's own FAIL | NOT CONFIRMED | STATUS_RULES row 6b: disagrees, a finite escape against no escape, a reading of the engine before 2026-09-23; the paper carries neither the HISTORY label nor the row's name 6b |
| Section 3 (viii) (380) | Under centred_step the loop stays: C1 PASS, C2 and C3 FAIL as declared (DETECTOR); a hypothesis until the author makes it the law | CONFIRMED as a hypothesis's reading | ALGEBRA.md 1927: the same three words under centred_step; named as a hypothesis under its own name in the paper |
| Section 3, the limits (384) | W = E_0'^2 + 3 p.p compared and never rooted; series S inside its pins | CONFIRMED as a hypothesis's reading | Series S is under covariant_readings (STATUS_RULES row 4a); the paper names the covariant readings and record 270 |
| Section 4, what is proved (390) | Born to 1/N_phi, the rungs to 1/(2 N_phi), Tsirelson to 8/N_phi + 0.0444 | CONFIRMED | Theorem 6; HIGHLIGHTS 5.4 (issue 368) |
| Section 4, what is proved (390) | Coulomb, the retarded potential, Poisson and the clock's 1/r: the engine before 2026-09-23, history | CONFIRMED | Labelled history; records.tex rec:oldreadings |
| Section 4, what is proved (390) | The Lorentz factor decided by the ratio of the two one-way Doppler factors, 1 - v^2 under the law | CONFIRMED | ALGEBRA.md 3.3 and 5.1 |
| Section 4, what is proved (390) | The bending decided against nature's 1.75 arcseconds | CONFIRMED | NATURE.md row 13: 1.75 arcsec at the Sun's limb, 1 + gamma = 2 (the general-relativity value; Dyson 1920's own number NOT FOUND by the Source Verifier, the VLBI gamma VERIFIED) |
| Section 4, what is proved (390) | A CHSH measurement at 1e-4 decides 181/64 against 2 sqrt 2 | CONFIRMED | DERIVATIONS_BEAM.md 7145 to 7150: the deficit 3.0e-4, a measurement at that precision decides |
| Section 4.1 (412) | A boost is not among the 48; Lorentz is the clicks' symmetry under (A2), which the law lacks | CONFIRMED | ALGEBRA.md 1.3 and 5.1; HIGHLIGHTS 5.4, "Lorentz, A" |
| Section 4.1 (415) | Angular momentum conserved only to the grain; no Noether theorem claimed | CONFIRMED | A non-claim |
| Section 4.1 (442 to 453) | c = 1/sqrt 3 rests on locality, straightness and the declared wall T_D; the anisotropy below 1/T_D | CONFIRMED | Proposition 1; ALGEBRA.md chapter 4, the pace; the bound on N_l stated as a bound |
| Section 4.2 (474) | The third law message by message for paid messages; a symmetry of two readers for a free family; the field's momentum not booked | CONFIRMED | The derivation's 9.1 and 12.4 as cited; ALGEBRA.md 8.11 for the blocks |
| Section 4.2 (478) | Gauss's law exact under its conditions; no detector reading registered | CONFIRMED | ALGEBRA.md chapter 4; the surface crossings labelled GAMEBOARD, the border clicks DETECTOR |
| Section 4.3 (484) | The law at head bends by the time part alone, half of nature's, -1.993 pixel (DETECTOR, the pin met) | NOT CONFIRMED | The same as Section 3 (vi): "the law at head" is the engine before 2026-09-23; SCHEDULE.md row 13 NOT PREDICTED, the pixel numbers HISTORY; the paragraph names the generic entry's date but not the HISTORY word |
| Section 4.3 (484) | The step algebra: C_ring = 5.12 at b = 6; under flow-link-v1 3.65, 3.82, 3.92 against 4 (COMPUTATION) | CONFIRMED | ALGEBRA.md 1784: 3.652 / 3.821 / 3.918 at b = 6 / 3 / 8; the flow algebra page as cited |
| Section 4.3 (484) | Series K's 0.000 pixel under the law as built (FAIL) | CONFIRMED as HISTORY | NATURE.md row 13's old cell; labelled history in the same paragraph |
| Section 4.4 (603) | Two offers of equal weight read 4104 and 4088 at N_phi = 8192, a departure of 8/N_phi, a computation not a run | CONFIRMED as COMPUTATION | Labelled a computation from Eqs. (joint) and (rung) |
| Section 4.4 (603) | The Mach-Zehnder bright port 64 of 64, the dark port 0 (row 2b) | CONFIRMED as HISTORY | NATURE.md row 2b: 64 / 0 over 64 births, DETECTOR (the engine before 2026-09-23); Table 1's new pin 1.00 - 0.02 is the current one |
| Section 4.4 (605) | Planck's and de Broglie's relations identities with one input h; no reading registered | CONFIRMED | The forcing ledger as cited; a non-claim |
| Section 4.5, Theorem 5 (617 to 624) | The first party's outcome from u alone; the second's marginal exactly N_phi/2; no tie to 4096 | CONFIRMED | ALGEBRA.md 4.9 (no-signalling a theorem of the click's form); STATUS_RULES row 1d, a consistency check |
| Section 4.5 (638) | The second party's serial correlation 15/16 and -5/16, a computation from the cells | CONFIRMED as COMPUTATION | Labelled a computation, not a run |
| Section 4.5 (638) | Read after a detector: 15/16 under a constant setting, -1/16 under the cycle, 16 of 16, nature's 0: FAIL (row 1c) | NOT CONFIRMED | NATURE.md row 1c reads it so, but the paper's own Table 1 row 1c says "not predicted until the order form is declared" (SCHEDULE.md row 1c: NOT PREDICTED, "disagrees" HISTORY); the FAIL is the old engine's reading and the paper carries both words for one row |
| Section 4.5 (640) | The strict-crossing rung would signal by 1/N_phi in 3944 of 4096 pairs | CONFIRMED as COMPUTATION | The design page as cited; a fact of the rounding |
| Section 4.5, Theorem 6 (657) | Measured after a detector at 512, 1024, 2048, 4096, 8192 and 16384 | NOT CONFIRMED | EXPERIMENTS.md 4222 to 4313 registers the detector runs at 512 and 4096, then 2048, 8192 and 16384; DERIVATIONS_BEAM.md 7141: "1024 by the design's map"; no run at 1024, and the paper's own line 691 lists five grains without 1024 |
| Section 4.5 (679) | The fixed-table limit 186034/65773, 2.1e-6 below 2 sqrt 2; 5793/2048 measured at 16384 | CONFIRMED | DERIVATIONS_BEAM.md 7123 to 7135; EXPERIMENTS.md 4306 to 4313 (DETECTOR, every pin met) |
| Section 4.5, the prediction (683 to 691) | S_U24 = 181/64, Delta S = -3.02e-4; 725/1024 and 723/1024 at 4096; measured at 512, 2048, 4096, 8192, 16384 | CONFIRMED | DERIVATIONS_BEAM.md 7123 to 7135; EXPERIMENTS.md (the five grains, DETECTOR) |
| Section 4.5, the prediction (691 to 694) | Rejected when a measured S differs by more than five standard errors | NOT CONFIRMED | The register's tolerance is two standard errors or the source's own interval (STATUS_RULES step 5); the paper's five is a looser criterion than the contract's and is not the register's |
| Section 4.5 (694) | A prediction only once the wheel meets no-signalling in the order | CONFIRMED | STATUS_RULES row 1c; the paper's Positioning (830) |
| Section 5.1, the one map (702) | The centred step a declared variant, named where used | CONFIRMED | HIGHLIGHTS 5.4: centred-step-v1 off by default, a hypothesis under its own identity |
| Section 5.1, rules (704) | The law of this paper is the runtime at the commit Appendix B names | NOT CONFIRMED | Appendix B (917) names "the runtime before the generic entry", the first-parent line up to 3a9a7109, the engine before 2026-09-23; Section 2 and Table 1 state the massive record kind and the local detector law of 2026-09-23 as the law (ALGEBRA.md chapter 8; SCHEDULE.md's head: "everything changed from the foundation"); the paper names two laws as its law |
| Section 5.1, rules (704) | The rules chosen among few (P9) marked carried, proved, or computed and not proved | CONFIRMED | ALGEBRA.md 8.10, the marks per rule as the paper lists them |
| Section 5.1, the three tests (710) | Each rule of Section 2 passes the three tests with its mark | CONFIRMED | ALGEBRA.md 8.10, rule by rule, the same marks |
| Section 5.1, the read-out (712) | Light never clicks; a body clicks; a take is a declaration of the world | CONFIRMED | ALGEBRA.md 8.6; POSTULATES.md section 10 (a light record ends only where a take is declared) |
| Section 5.1, the code (714) | The design's scripts are gates on the code, not measurements | CONFIRMED | APPROVALS.md section 0; ALGEBRA.md 8.10 |
| Section 6 (734) | The 48 forced, the 24 the rotations, the hand the pseudoscalar | CONFIRMED | ALGEBRA.md 1.3 and chapter 7; HIGHLIGHTS 5.4 (2026-09-22, the group named the group of order 24) |
| Section 6, the platform (740) | Rows 3, 4b, 12 read in the detector's own clock, r = 1.0000, equal to the host's interval, DETECTOR | CONFIRMED as HISTORY | STATUS_RULES step 1 (the re-run at head, count_owed at a zero numerator); readings of the engine before 2026-09-23; the paper names the re-run of 2026-09-22 |
| Section 6, the roads (742) | "derived" stands nowhere; W declared on the rows, E_0 = mc^2 declared | CONFIRMED | ALGEBRA.md 5.3; the roads table as cited |
| Section 7.1 (752) | Seven formulas shown Inside were confirmed by their runs | NOT CONFIRMED | The seven confirmations (records.tex rec:reproduction: series Q, the click's power, Mach-Zehnder, the marginals, GHZ, Malus, light beside a mass) are runs of the engine before 2026-09-23; SCHEDULE.md and HIGHLIGHTS 5.4 (2026-09-23) make every such reading HISTORY, and the sentence carries no HISTORY label |
| Section 7.1, the method (758) | Three checks in order; (K) and (P); a prediction is not a pass | CONFIRMED | APPROVALS.md section 0; SCHEDULE.md's two kinds; ALGEBRAIC_CLOSURE.md section 3 item 2 |
| Section 7.1, the method (758) | Every pinned reading a blank; the old comparison history, never in this table | CONFIRMED | APPROVALS.md section 3; SCHEDULE.md's head |
| Section 7.1, limitations (762) | A moving thing's own count is r = 1 at every speed; nothing contracts | CONFIRMED | STATUS_RULES rows 4a, 4b, 5b |
| Section 7.1, limitations (762) | The comb: the axes 2.8 times denser than the face diagonals | CONFIRMED | HIGHLIGHTS 5.4 (2026-09-23, the comb): the same number |
| Section 7.1, limitations (762) | The weight pair w = gamma_L (1 + gamma_PPN v^2) M at gamma_PPN > 0; M at 0 | CONFIRMED | HIGHLIGHTS 5.4 (2026-09-23, the weight pair, option B of record 1054; decision B, record 1150) |
| Section 7.1, limitations (762) | Row 7a not predicted and row 2a NOT COMPARED, the owner's word; nothing else moved | NOT CONFIRMED in part | The two placements are HIGHLIGHTS 5.4's (2026-09-23, after the kind audit) and STATUS_RULES rows 2a and 7a; but Table 1's row 2a carries nature's 0.94 with a blank pinned cell and no NOT COMPARED word, so the table does not show the placement the paragraph states |
| Table 1, row 1a (777) | (K) S = 181/64 = 2.828 at N_phi = 2048, exact | CONFIRMED | ALGEBRAIC_CLOSURE.md row 1a: "181/64 at N = 2048, exact"; SCHEDULE.md row 1a; DECLARATIONS.md section 1 |
| Table 1, row 1a (777) | Nature 2.42 +- 0.20 (Hensen 2015) | CONFIRMED | SOURCES_VERIFIED.md: VERIFIED; NATURE.md row 1a |
| Table 1, row 1a (777) | Nature 2.82759 +- 0.00051 (Poh 2015) | NOT CONFIRMED | Not in NATURE.md row 1a and not among the 58 verified values; a nature value the register does not carry |
| Table 1, row 1b (778) | (K) 2, a control | CONFIRMED | SCHEDULE.md row 1b: (K) CONTROL: 2; STATUS_RULES row 1b |
| Table 1, row 1c (779) | Not predicted until the order form is declared | CONFIRMED | SCHEDULE.md row 1c: NOT PREDICTED until declared |
| Table 1, row 1d (780) | 0 exactly by the table's symmetry, 32 of 64 at every setting | CONFIRMED | SCHEDULE.md row 1d; STATUS_RULES row 1d (a consistency check) |
| Table 1, row 2a (781) | (K) at or above the train's coherence 0.99 at 128 periods; 0.959, 0.958, 0.958 at 32 periods | CONFIRMED | SCHEDULE.md row 2a and PINS.md row 2a, the same numbers |
| Table 1, row 2a (781) | Nature 0.94 (Jacques 2005) | NOT CONFIRMED | NATURE.md row 2a: no published single-quantum two-slit visibility at hand, the biprism's 0.94 named beside the Mach-Zehnder proxy 0.98; Jacques 2005 is not among the 58 verified values (Bach 2013 is); the row is NOT COMPARED until the source is verified (STATUS_RULES row 2a, the owner's placement of record 1204) |
| Table 1, row 2a (781) | Partial: the slits' exploratory page | CONFIRMED | APPROVALS.md row 2a: partial, the viewer's exploratory page (record 1513) |
| Table 1, row 2b (782) | (K) 1.00 - 0.02, the dark port 0 of 64; nature 0.98 (Grangier 1986) | CONFIRMED | SCHEDULE.md row 2b; SOURCES_VERIFIED.md: VERIFIED, the published figure the lower bound "over 98 percent", the page's 0.98 its floor |
| Table 1, row 2c (783) | (K) the exponent 2 exactly, the sum 0 to the grain; nature 0.0064 +- 0.0119 (Sinha 2010) | CONFIRMED | SCHEDULE.md row 2c; SOURCES_VERIFIED.md: VERIFIED (the heralded single-photon value) |
| Table 1, row 9 (784) | (K) 128 of 256 at 45 degrees, 0 crossed, 64 with a third between; the three settings' counts | CONFIRMED | SCHEDULE.md rows 9 and Malus's three settings; DECLARATIONS.md 306 |
| Table 1, row 10 (785) | (K) 0.842 at w = 2 lambda, F = 0.16; 0.886 far field | CONFIRMED | SCHEDULE.md row 10; ALGEBRAIC_CLOSURE.md row 10; DECLARATIONS.md 877 |
| Table 1, row 7 (786) | (P) the lines at the modes' own frequencies 0.0995 and 0.1432; exploratory 0.09948 within 0.3 percent | CONFIRMED | APPROVALS.md row 7: "V exploratory: the coupled mode 0.09948 read within 0.3 percent"; DECLARATIONS.md 429 to 447 |
| Table 1, row 4a (787) | (K) 0.8116 at the exact cone (mu = 0.15, s = 14); 0.8108 and 0.8132 controls; nature 1/gamma (Bailey 1977) | CONFIRMED | ALGEBRAIC_CLOSURE.md row 4a; MASSIVE_RECORD.md 1148; SOURCES_VERIFIED.md: Bailey's gamma = 29.33 VERIFIED |
| Table 1, row 4a (787) | At rest 42.364 against 42.36, no beat; in motion partial, the ramp redeclared | CONFIRMED | APPROVALS.md row 4a, the same words; EXPLORATION.md 33 to 34 (0.03 and 0.01 percent, DETECTOR) |
| Table 1, row 4b (788) | (K) 1 + z = 1.9889, the free limit 1.9339; nature gamma (1 + beta) (Botermann 2014) | CONFIRMED | DECLARATIONS.md 244 to 257; SCHEDULE.md row 4b; SOURCES_VERIFIED.md: Botermann VERIFIED |
| Table 1, row 4c (789) | (K) 3.732 at k = 3 exactly, the sidebands named; nature the two-way form | CONFIRMED | SCHEDULE.md row 4c (FORM); ALGEBRAIC_CLOSURE.md row 4c |
| Table 1, row 5a (790) | (K) within 0.8, 0.4, 0.2 percent at 12, 16, 24 Links; a bound met at the lattice's grain | CONFIRMED | SCHEDULE.md row 5a and PINS.md row 5a, the same words; STATUS_RULES row 5a's "disagrees at the registered grain" is the old engine's, superseded by the schedule's new pin |
| Table 1, row 5a (790) | Nature below 1e-17 (Nagel 2015) | NOT CONFIRMED | SOURCES_VERIFIED.md: the "below about 1e-17" is Herrmann et al. 2009's; Nagel et al. 2015's is 9.2 +- 10.7 x 1e-19 (delta nu / nu at 95 percent); the citation names the wrong source for the number |
| Table 1, row R2 (791) | (K) beta = 0.5774 at k = 3 exactly, independent of the clock's factor | CONFIRMED | DECLARATIONS.md 680 to 700; SCHEDULE.md row R2 |
| Table 1, row R2 (791) | Nature's coefficient 0.975 +- 0.021 (Michelson, Gale and Pearson 1925, to verify) | NOT CONFIRMED | SOURCES_VERIFIED.md: NOT FOUND as a printed number; it follows from the published 0.230 +- 0.005 fringe against the computed 0.236; the row should say the number is derived, not "to verify" |
| Table 1, row LC (792) | (K, P) N_0 = 218 +- 2 at W = 64, 2L/c = 207.85 beside; (P) the ring-ups | CONFIRMED | DECLARATIONS.md 470 and 500 to 501, the pin 218 +- 2 with 207.85 as the (K) form; SCHEDULE.md prediction 8 |
| Table 1, row v (793) | (K) the closed-form index, a control; the 4 percent open | CONFIRMED | ALGEBRAIC_CLOSURE.md row v; SCHEDULE.md's index note |
| Table 1, row v (793) | Exploratory at rest: 0.01 to 0.03 percent from the closed form | NOT CONFIRMED | EXPLORATION.md 36: the index reads n = 1.0366, 1.0887, 1.1702 against the closed form's 1.0421, 1.1022, 1.1956, "the excess n - 1 at 0.87 of the form's", by a GAMEBOARD probe; the 0.01 to 0.03 percent belongs to the body's clock at rest (EXPLORATION.md 33 to 34), not to the index; a closeness claimed that the exploration page does not read |
| Table 1, row v-m (794) | (P) the scheme's own number; Fizeau's form the declared non-match; head-on 0.498 beside | CONFIRMED | APPROVALS.md row v, v-m; EXPLORATION.md 37; SCHEDULE.md prediction 3 |
| Table 1, row ii (795) | (P) 0.7814 and 0.8032; exploratory 0.7833 and 0.8055, the three gammas indistinguishable | CONFIRMED | APPROVALS.md row ii-a, ii-b; EXPLORATION.md 38 (0.7833 and 0.8055 by the spectral peak, GAMEBOARD; the clicks' 0.7826 and 0.8099 DETECTOR beside) |
| Table 1, row M1 (796) | (K) the side lobe's centroid at y = 64 + 27.79 for lambda_dB = 12 Links; nature's form de Broglie's | CONFIRMED | DECLARATIONS.md 599; SCHEDULE.md row M1; SOURCES_VERIFIED.md: Joensson 1961 and Tonomura 1989 VERIFIED |
| Table 1, row M2 (797) | (K) the first click 169 +- 2, the transit 167.1 beside; m = 1.0417 | CONFIRMED | DECLARATIONS.md 620 to 627; SCHEDULE.md row M2; Bertozzi 1964 VERIFIED |
| Table 1, row A (798) | (P) the deficit omega_0^2/4; one interval at most 3.6e-28 s (the electron's 2e-14), 6.3e-31 s (the Crab bound); a bound, no run | CONFIRMED | SCHEDULE.md row A, the same two bounds; NATURE_SOURCES_MASSIVE.md 88 to 101; Altschul 2006 and Stecker and Glashow 2001 VERIFIED |
| Table 1, row A2 (799) | (P) the coefficient in [0, 2]; the interval at most about 2e-35 s | CONFIRMED | LIGHT_DISPERSION_BOUND.md 66 to 69: 1.2e-35 s on an axis, 2.0e-35 s on the sphere average, 2.5e-35 s on a face diagonal |
| Table 1, row A2 (799) | The published number recalled and not yet verified | NOT CONFIRMED | SOURCES_VERIFIED.md, first row: E_QG,2 > 1.3e11 GeV (Vasileiou et al. 2013) VERIFIED at 95 percent confidence, with the normalisation factor 3/2 NOT FOUND; the paper's phrase is out of date, on the conservative side |
| Table 1, row B (800) | (P) epsilon (gamma_m^2 - 1)/2 below 1/gamma_m; a bound | CONFIRMED | SCHEDULE.md row B and prediction 2 |
| The derivations, final (803) | Born's exponent 2; Tsirelson's value as the limit; c^2 = 1/3; the rest energy h omega_0 with omega_0 = mc^2 at the massive cone | CONFIRMED | ALGEBRAIC_CLOSURE.md rows 2c, 1a, 5a and M2 ("the rest limit omega_0 = m c_eff^2 exactly ... a derivation") |
| Under the hypothesis (805) | Rows 12, the delay and Newton's fall under pair-field-v1 only, never in the list's place | CONFIRMED | APPROVALS.md section 2; ALGEBRAIC_CLOSURE.md rows 12, 13, 14 and section 2 |
| The rows that left (807) | 3, 11a to 11c, 7a, 7b, 8a to 8c, 5b, R5, R6, 6, 13, 14 not predicted or replaced, none removed | CONFIRMED | ALGEBRAIC_CLOSURE.md's DROPPED 7 and REPLACED 3, the same rows; SCHEDULE.md's NOT PREDICTED list |
| The prediction rows (817) | The seven (P) rows named, each with its falsifier; a prediction is not a pass | CONFIRMED | SCHEDULE.md's eight predictions and (P) rows; ALGEBRAIC_CLOSURE.md section 3 item 2 |
| Discussion (829) | (i) the atom's lines need a rule the law lacks; 27/20 conjectured | CONFIRMED | ALGEBRA.md 5.8 (1696); ALGEBRAIC_CLOSURE.md row 6 |
| Discussion (829) | (v) no rotation curve read; unseen content only as an input family | CONFIRMED | HIGHLIGHTS 5.4 (2026-09-21, the dark sector) |
| Discussion (829) | (viii) the inverse square in space pending its run (row 14) | CONFIRMED | SCHEDULE.md row 14 NOT PREDICTED; ALGEBRAIC_CLOSURE.md row 14 REPLACED by Newton's fall as a prediction of the form |
| Positioning (830) | The order of the outcomes signals under the sequential wheel (row 1c, FAIL after a detector) | NOT CONFIRMED | The same as Section 4.5 (638): the FAIL is the old engine's reading; Table 1 and SCHEDULE.md row 1c say not predicted until the order form is declared |
| Positioning (833) | Theorem 6 puts S(N_phi) on both sides of Tsirelson's bound | CONFIRMED | HIGHLIGHTS 5.4 (issue 368): not bounded by 2 sqrt 2, two-sided |
| Declarations (845) | The forms of Newton, Kepler, Einstein, Lorentz, Bohr and Balmer are the things compared with, not inputs | CONFIRMED | HIGHLIGHTS 5.4 (2026-09-22, the declared inputs and the roads) |
| Appendix B (917) | The paper's law is the runtime before the generic entry; the ring's run the one reading under it | NOT CONFIRMED | See Section 5.1 (704): this names the engine before 2026-09-23 as the paper's law while Sections 2, 5 and Table 1 state the law of 2026-09-23 (ALGEBRA.md chapter 8, MASSIVE_RECORD.md); the two statements of the law contradict, and the appendix's law is the one every contract calls HISTORY |

## The counts

| Verdict | Lines |
| --- | --- |
| CONFIRMED (including CONFIRMED as HISTORY, as COMPUTATION or as a hypothesis's reading, where the paper's own label says so) | 139 |
| NOT CONFIRMED | 29 |
| Lines in the table | 168 |

The kinds I changed: none in the paper (docs only). The kind words this
page proposes, for the writer on the Boss's word: HISTORY on every reading
of the engine before 2026-09-23 that the text cites as DETECTOR without
it; COMPUTATION in place of FAIL on the perihelion; INPUT in place of
GAMEBOARD on the declared nS/d = 16; NOT COMPARED in place of NOT YET on
row 6; "not predicted until declared" in place of FAIL on row 1c where
the text keeps the old word; a hypothesis's reading named as such on
series S wherever it is cited.

## The NOT CONFIRMED lines, in the order of severity

A wrong claim of agreement first, a citation form last.

1. **Table 1, row v (793): the index at rest "exploratory at rest: 0.01
   to 0.03 percent from the closed form".** EXPLORATION.md 36 reads the
   index n = 1.0366, 1.0887, 1.1702 against the closed form's 1.0421,
   1.1022, 1.1956, the excess n - 1 at 0.87 of the form's, by a
   GAMEBOARD probe; the 0.01 to 0.03 percent is the body's clock at rest
   (EXPLORATION.md 33 to 34). A closeness to the algebra is claimed that
   the page does not read, and the kind of the reading is not named.
2. **Theorem 6 (657): "measured after a detector at 512, 1024, 2048,
   4096, 8192 and 16384".** EXPERIMENTS.md registers detector runs at 512,
   4096, 2048, 8192 and 16384; DERIVATIONS_BEAM.md 7141 says "1024 by the
   design's map". A measurement is claimed at a grain that has no run;
   the paper's own line 691 lists the five grains rightly.
3. **Abstract (50), one page (74), Table 1 row 1a (777): 181/64 "1.05
   standard errors from the measurement", "inside Poh et al."** The
   arithmetic is DERIVATIONS_BEAM.md 7123's, but Poh et al. 2015's 2.82759
   +- 0.00051 is in neither NATURE.md row 1a nor SOURCES_VERIFIED.md's 58
   values: nature's value is not the verified one, and it carries the
   abstract's one numerical comparison with nature.
4. **Section 5.1 (704) and Appendix B (917): the law of this paper.**
   The appendix names the runtime before the generic entry (the engine
   before 2026-09-23, the first-parent line to 3a9a7109) as the paper's
   law and Section 5.1 points to it, while Section 2, Section 5's
   postulates and Table 1 state the massive record kind and the local
   detector law of 2026-09-23 (ALGEBRA.md chapter 8; SCHEDULE.md:
   "everything changed from the foundation"). Two laws are named as the
   paper's law, and the appendix's is the one every contract calls
   HISTORY.
5. **Section 3 (iii) (380): the perihelion "FAIL on the law, pinned in
   order and symmetry".** No detector reading, no register row and no pin
   declared before a run stand behind the word; STATUS_RULES step 5: "a
   disagrees with no number is not a disagrees". The Einstein Outside
   page's estimate is a COMPUTATION.
6. **Section 3 (vi) (380) and Section 4.3 (484): row 13's -1.993 pixel
   as "the law at head", DETECTOR, the pin met.** NATURE.md row 13 holds
   the reading, but under the law as it stands SCHEDULE.md row 13 is NOT
   PREDICTED with "-1.993 and -3.989 pixel (HISTORY)"; the HISTORY word
   is missing at both citations.
7. **Section 4.5 (638) and Positioning (830): row 1c "FAIL after a
   detector".** Table 1 row 1c and SCHEDULE.md row 1c say "not predicted
   until the order form is declared"; the FAIL is the old engine's word
   (NATURE.md row 1c, HISTORY in the schedule). One row carries two words.
8. **Section 3 (viii) (380): the hydrogen loop's escape at 3407
   intervals, "the law's own FAIL".** STATUS_RULES row 6b: a reading of
   the engine before 2026-09-23; the paper names neither HISTORY nor the
   row 6b.
9. **Section 7.1 (752): "Seven formulas shown Inside ... were confirmed
   by their runs".** The seven confirmations are runs of the engine
   before 2026-09-23 (records.tex rec:reproduction); SCHEDULE.md and
   HIGHLIGHTS 5.4 (2026-09-23) make them HISTORY, and the sentence
   carries no label.
10. **Section 3, the chains (380), the class of old readings cited as
    DETECTOR without HISTORY:** L2b's 23.5 pixels; D3's 138 of 139;
    series L's S = 2.75 and 32/64; series Q's 290 of 290 in (iv); series
    G in (vii). Each is NATURE.md's or EXPERIMENTS.md's number; each is
    HISTORY by SCHEDULE.md's head, and the label is absent at these
    lines while present at others (74, 390, 484).
11. **Section 3 (i) (380): series S's face clicks 369 and 345 as the
    quantum of the step, DETECTOR.** STATUS_RULES row 4a: under
    covariant_readings, "DETECTOR, a hypothesis's"; neither the key nor
    HISTORY is named at this line.
12. **Why physics behaves (93) against Table 1 row 2a (781): nature's
    two-slit visibility 0.98 in one place and 0.94 (Jacques 2005) in the
    other.** NATURE.md row 2a: no verified two-slit figure, 0.98 the
    Mach-Zehnder proxy, 0.94 the biprism's; Jacques 2005 is not among the
    58 verified values (Bach 2013 is). One row, two nature values,
    neither verified.
13. **Limitations (762) against Table 1 row 2a (781): "row 2a to NOT
    COMPARED" is not shown in the table.** The row carries nature's 0.94
    and a blank pinned cell with no NOT COMPARED word (STATUS_RULES row
    2a; HIGHLIGHTS 5.4, the two placements).
14. **Abstract (50): "the equivalence principle under the first alone".**
    ALGEBRA.md 5.4 names (W1), (W2), (M), with (A1) and (A3) only for the
    accelerated detector; the body (72) names the five assumptions, the
    abstract drops them.
15. **Section 3 (viii) (380): "row 6 stays NOT YET".** SCHEDULE.md row 6
    is NOT COMPARED, ALGEBRAIC_CLOSURE.md REPLACED, STATUS_RULES not
    predicted; NOT YET is NATURE.md's old cell.
16. **Section 4.5, the prediction (691 to 694): rejection at five
    standard errors.** STATUS_RULES step 5's tolerance is two standard
    errors or the source's own interval; the paper's criterion is not the
    register's.
17. **Section 3 (v) (380): "nS/d = 16 (GAMEBOARD, the world files)".**
    A declared input is INPUT by STATUS_RULES step 1; the kind word is
    wrong.
18. **Table 1, row R2 (791): nature's 0.975 +- 0.021 "to verify".**
    SOURCES_VERIFIED.md: NOT FOUND as a printed number; it follows from
    the published 0.230 +- 0.005 fringe against the computed 0.236, and
    the row should say so.
19. **Table 1, row 5a (790): "nature below 1e-17 (Nagel 2015)".**
    SOURCES_VERIFIED.md: the 1e-17 bound is Herrmann et al. 2009's; Nagel
    et al. 2015's is 9.2 +- 10.7 x 1e-19; the wrong source for the number.
20. **Table 1, row A2 (799): "the published number recalled and not yet
    verified".** SOURCES_VERIFIED.md now has E_QG,2 > 1.3e11 GeV VERIFIED
    (with the 3/2 normalisation NOT FOUND); the phrase is out of date, on
    the conservative side.

The NOT CONFIRMED table lines number 29; the twenty items above group
the class of old readings (item 10) and pair the lines that state one
thing twice (items 3, 4, 6, 7, 12 and 13).

## What I did not reach

The whole of the abstract, the comparison table (Table 1) and every MET
or FAIL word were read. Not reached in the two hours: the proofs of
Theorems 1, 4, 5 and 6 and the Gleason-like theorem (the mathematician
verifier's); the figures' captions beyond Figure 1; records.tex's own
tables (the full confrontation record, the conversion table, the forcing
ledger and the families table) line by line, read only where the paper
cites them; `NUMBERS.md` on `paper-48`, which maps each number to its
source, against this table; and the Einstein Outside, click frame and
light Outside pages themselves, read through ALGEBRA.md chapter 5's
restatement of them rather than in their own files.
