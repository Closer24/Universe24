# The claims map

Every theorem, lemma, identity and quantitative claim of the law (docs/ALGEBRA.md), the paper and its supplement, as the proofs' inventory quotes them at the heads its header names (the law at 3a334eeb and its lines of 2026-10-17 at b254f4d2, the paper and the supplement at d7e97674, the long version), stands here as one row, generated from tools/derivations/proofs_inventory.json by tools/claims_map.py, so the two cannot drift apart (tests/test_claims_map.py). Each row names where the claim stands, its exact statement, the ground its check stands on, its kind and its verdict, and the function that checks it; tests/test_proofs_check_the_law.py runs every check and asserts every verdict, so a green run of `python -m pytest tests/test_proofs_check_the_law.py -q` runs every check of the map to its verdict; the rows with no check stand as statements only, and a witness is not a proof.

**The kinds and the verdicts.** The kinds, in the words of tools/derivations/README.md: (A) an exact identity, checked in Python's integers, `fractions.Fraction` and Gaussian rationals at random integer witnesses with the symmetric cases forced; (B) a series expansion with its order, checked by the residual against the exact function at two step sizes, the ratio 2^order the test of the order; (C) a hand proof with a numerical witness only, the witness recomputed where a script exists and the row counted as unchecked; (D) a statement of the engine's structure that only a test of the engine shows, the engine's tests named and no check here. The verdicts: "holds" (the check returns true), "witness only" (a hand proof with a numerical witness, the check a witness and not a proof), "finding" (the statement as printed at the place named is false and the check reproduces the mismatch; the commits, what was found and what was done about it stand in docs/ERRATA.md), "none" (no check, the row stands as a statement only).

| id | name | place | kind | verdict |
| --- | --- | --- | --- | --- |
| A01 | Theorem 4's Yukawa exponent | Universe24_Paper.tex 7.2, Theorem 4; S.13; the writer's (1), the advisor's (1) | B | holds |
| A02 | The time-Link recurrence's Wronskian | Universe24_Paper.tex 5.5, S.9, S.33 and ALGEBRA.md row 9 of The conventions and the units, the two-angle form at every place since d7e97674; the writer's (2), the advisor's (2) | A | holds |
| A03 | S.42's monopole | S.42, inputs and (c); the writer's (3), the advisor's (3) | A | holds |
| A04 | S.39 (b)'s band is real for every pair | S.39 (b); the writer's (4), the advisor's (4) | A | holds |
| A05 | S.43 (e)'s Stark sentence | S.43 (e); the writer's (5), the advisor's (5) | A | holds |
| A06 | S.17's beat | S.17; Universe24_Paper.tex 7.5; the writer's (6), the advisor's (6) | C | witness only |
| A07 | S.24's orientation | S.24 and Universe24_Paper.tex 10.2; the writer's (7), the advisor's (7) | B | holds |
| A08 | S.57's wall | S.57 (a); the writer's (8), the advisor's (8) | A | holds |
| A09 | 10.2's 'hence' | Universe24_Paper.tex 10.2; the writer's (9), the advisor's (9) | C | none |
| A10 | S.26 (d')'s balance at every step | S.26 (d'); the writer's (10), the advisor's (10) | B | holds |
| L01 | The line's band identity | ALGEBRA.md, The line; row 3 of The conventions and the units; S.1 | A | holds |
| L02 | The band at a pace, the Lorentz form | ALGEBRA.md, The line (The clock once and the Link twice), The band at a pace; the paper's Eq. (4); S.1 | A | holds |
| L03 | The vacuum's band and light's dispersion | row 3 of The conventions and the units; S.1; Universe24_Paper.tex 3.3 | A | holds |
| L04 | The clocks shift alike | ALGEBRA.md, The line (i) | A | holds |
| L05 | The guard's edge | ALGEBRA.md, The guard; S.3; S.61 row 4; Universe24_Paper.tex 3.4 | A | holds |
| L06 | The total mirror of light | ALGEBRA.md, The band at a pace; the derivation script paces.py | A | holds |
| L07 | The three exact bands | ALGEBRA.md, The exact bands; Universe24_Paper.tex 6.1 | A | holds |
| L08 | The band's top on the diagonal and the axis | S.27 | A | holds |
| L09 | The largest group speed | S.21 | A | holds |
| L10 | The content's index for every family | S.28; Universe24_Paper.tex 8 (p); The paces compose | A | holds |
| L11 | The slow matter's index limit | S.28's check | B | holds |
| L12 | The reach of a holder with a gap | ALGEBRA.md, The well; S.11; S.39's check | A | holds |
| L13 | The group velocity | ALGEBRA.md, The band at a pace; S.1; rule3.group_velocity | A | holds |
| L14 | Light's speed and dispersion | S.1; ALGEBRA.md, The lattice constants; Universe24_Paper.tex 10.2 | B | holds |
| L15 | The fourth order of light's band | S.24; ALGEBRA.md, The law's own formulas B (11) | B | holds |
| L16 | Rule3's coefficients are the read's own without tension | ALGEBRA.md, The paces (The clock is the Node's, the tension is the Link's); rule3.coefficients | A | holds |
| L17 | Theorem 3, the conserved form | ALGEBRA.md, The conserved form; the paper's Theorem 3; S.48 | A | holds |
| L18 | The plain form fails under a tension, S.32's two witnesses | S.32; ALGEBRA.md, The conserved form | A | holds |
| L19 | The remainders' walk of the form | ALGEBRA.md, The conserved form (the proof's last sentence), row 7 of The conventions and the units; the paper's 4.3 | A | holds |
| L20 | The three-level form equals the two-level form | row 7 of The conventions and the units; Universe24_Paper.tex 4.3 | A | holds |
| L21 | The form's change under moving paces | Universe24_Paper.tex 4.3 | A | holds |
| L22 | Theorem 1, the direction | ALGEBRA.md, The direction; the paper's Theorem 1; S.48 | A | holds |
| L23 | The cube's symmetry: the complement identity | ALGEBRA.md, The direction (The cube's symmetry), the proof's act (1) | A | holds |
| L24 | The cube's symmetry act by act | ALGEBRA.md, The direction (The cube's symmetry), the proof's acts (2) to (6) | D | none |
| L25 | The Wronskian with the form's weights | ALGEBRA.md, The paces (The sign is the rotation sense); S.9 | A | holds |
| L26 | The sign current's flux over density | S.33 (b); S.61 row 8 | A | holds |
| L27 | The velocity invariant of the massless row | ALGEBRA.md at 915c6a7b, The click writes on the lattice (the restoring front's third test; the front is history at 3a334eeb under the dense record's clause, the identity of the line standing); ENGINE.md, the face's kicks | A | holds |
| L28 | The write's total is exact over any window | ALGEBRA.md, The integer-exact constructions (4); The integer budget of a derived row | A | holds |
| L29 | The booking identity of the hole | S.50 (R289); ALGEBRA.md, The click is the meeting | A | holds |
| L30 | The share identity at any paces | ALGEBRA.md, The share's change is the currents; the paper's Eq. (10); S.5 | A | holds |
| L31 | The share is conserved at standing paces | ALGEBRA.md, The count is the record's share (Theorem); Universe24_Paper.tex 4.4 | A | holds |
| L32 | The vacuum's share | ALGEBRA.md, The count is the record's share; Universe24_Paper.tex Eq. (9) | A | holds |
| L33 | The plane wave's current and form | ALGEBRA.md, The booking; The velocity | A | holds |
| L34 | The momentum flux identity with the remainders | ALGEBRA.md, The tension; the paper's Eq. (7); row 5 of The conventions and the units; S.48 | A | holds |
| L35 | The tension of a plane wave | S.7; row 6 of The conventions and the units | A | holds |
| L36 | The two share forms summed over the board | row 14 of The conventions and the units | A | holds |
| L37 | The exact lay's operator line | ALGEBRA.md, The packet lay (The generator) | A | holds |
| L38 | The paces compose | ALGEBRA.md, The paces compose; S.34 (a) | A | holds |
| L39 | The clock's exponential and its readings | ALGEBRA.md, The paces compose; S.34 (a), (e); The paces | B | holds |
| L40 | The acts' factors | ALGEBRA.md, The write per proper volume and per proper interval; S.34 (d) | A | holds |
| L41 | The exponential metric's post-Newtonian orders | S.34 (c); S.19; Universe24_Paper.tex 3.4 and 8 | B | holds |
| L42 | The clock's click rate | S.15; Universe24_Paper.tex 7.4 and 8 (a); The method of derivation, step 3 | B | holds |
| L43 | The fall and Kepler's potential | S.18; the paper's Eq. (14); ALGEBRA.md, The method of derivation | A | holds |
| L44 | The post-Newtonian parameters of the Kepler column | S.19; ALGEBRA.md, The rows against nature (a) | A | holds |
| L45 | The moving clock to the fourth order | S.21; Universe24_Paper.tex 8 (e); ALGEBRA.md, The rows against nature (e) | B | holds |
| L46 | De Broglie and the three speeds | S.22; S.53; Universe24_Paper.tex 3.3 | A | holds |
| L47 | The push on a moving record | S.58; ALGEBRA.md, The push on a moving record; the paper's Eq. (16) | A | holds |
| L48 | The shadow's capture radius | S.30; ALGEBRA.md, The paces compose | A | holds |
| L49 | The two clocks under the principle | S.31; Universe24_Paper.tex Table 4 and 3.4; ALGEBRA.md, The same clock and the same ruler for every act | B | holds |
| L50 | Light's index to first order | S.2; S.12; Universe24_Paper.tex 8 (p) | B | holds |
| L51 | The mass defect's first order | S.38 (b); ALGEBRA.md, The mass defect is the form's fall at a kept count | B | holds |
| L52 | The preferred-frame parameter of a diagonal metric | S.35; Universe24_Paper.tex 10.3 | A | holds |
| L53 | The staggered clock's redshift | S.36 (v) | B | holds |
| L54 | The frozen content | S.41 (3); ALGEBRA.md, The paces compose; row 4 of The conventions and the units | A | holds |
| L55 | The bounds from the photon and the dispersion | S.27; S.24; Universe24_Paper.tex 10.1 and 10.2 | A | holds |
| L56 | The bending of light and Shapiro's delay | S.20; the paper's Eq. (15); ALGEBRA.md, The rows against nature (b), (c) | A | holds |
| L57 | The rest rotation at a content to first order | S.63's input; S.15 | B | holds |
| L58 | Bell's correlation under the declared credit | S.10; S.51; ALGEBRA.md, The pair family and Bell's gate; Universe24_Paper.tex 9.3 and 9.4 | A | holds |
| L59 | The two local credits and the sawtooth | S.10; S.51b; Universe24_Paper.tex 9.4; ALGEBRA.md (h) | A | holds |
| L60 | The contrast credit | S.10's check | A | holds |
| L61 | The GHZ correlation under the declared credit | S.40; ALGEBRA.md, The GHZ gate; Universe24_Paper.tex 9.4 | A | holds |
| L62 | The instruments' rational angles and the turn's three shears | ALGEBRA.md, The integer-exact constructions (3), row 9; S.61 row 9 | A | holds |
| L63 | The units of one quantum | rows 12, 13, 17 and 18 of The conventions and the units; S.49 (4), (5); S.26 (a) | A | holds |
| L64 | The region's reading factor | S.8; Universe24_Paper.tex 5.3 | A | holds |
| L65 | The Zeno formula | S.59 | A | holds |
| L66 | Theorem 4, the stable body | the paper's Theorem 4; ALGEBRA.md, The functional and the dilation; S.48 | A | holds |
| L67 | The hollow's barrier | ALGEBRA.md 7.2 (b); S.13; Universe24_Paper.tex 7.2 | A | holds |
| L68 | The functional's gradient is the fixed point's equation | S.13; ALGEBRA.md, The functional (Proof); the paper's Eq. (12) | A | holds |
| L69 | The adiabatic invariant and the count's drift | S.14; the paper's Eq. (13); invariant_check.py | A | holds |
| L70 | The body's click share | S.14, the body's click; Universe24_Paper.tex 5.4 and 7.4 | A | holds |
| L71 | Schroedinger's equation as the slow limit | S.63; Universe24_Paper.tex 3.3 | A | holds |
| L72 | The resonance's exponents | S.16; ALGEBRA.md, The law's own formulas A (6) | A | holds |
| L73 | The resonant growth rate | S.16's check | C | witness only |
| L74 | The cross current of two standing records | S.17; Universe24_Paper.tex 7.5 | A | holds |
| L75 | The integer budget's walk | ALGEBRA.md, The integer budget of a derived row; Universe24_Paper.tex 9.2 | A | holds |
| L76 | The guide's lay | S.48; row 18 of The conventions and the units | A | holds |
| L77 | What a body writes into the holder of the sign | S.42; Universe24_Paper.tex 7.4 | A | holds |
| L78 | The two-mode line under the rotation | S.43; Universe24_Paper.tex 7.4 | A | holds |
| L79 | The two forces between quanta | S.44; Universe24_Paper.tex 10.1 | A | holds |
| L80 | The nuclear holder's threshold | S.45 (a), (b) | A | holds |
| L81 | The atom's self-term | S.46 (c); Universe24_Paper.tex 7.3 | A | holds |
| L82 | The equivalence principle between families | S.47; Universe24_Paper.tex 8 (i) | A | holds |
| L83 | The quanta a cloud gives to settle | ALGEBRA.md, The surplus leaves | A | holds |
| L84 | The total share is non-negative | S.6; ALGEBRA.md, The share's sign and the credit's floor (a), at the vacuum's coefficients since 3a334eeb, the bound in a well the hands' to state; Universe24_Paper.tex 4.4 | A | holds |
| L85 | Theorem 2, what the acts can form | ALGEBRA.md, The four acts; the paper's Theorem 2; S.48 | C | none |
| L86 | The bilinears of one pair | ALGEBRA.md at b254f4d2, The conserved form (The bilinears of one pair) | A | holds |
| L87 | The Gram determinant of the planes | ALGEBRA.md at b254f4d2, The count is the record's share (The Gram determinant of the planes) | A | holds |
| L88 | The charge of a plane is bounded by its share | ALGEBRA.md at b254f4d2, The paces (The charge of a plane is bounded by its share); The third and the colours, closed as absent | A | holds |
| L89 | The Ports' three readings | ALGEBRA.md at b254f4d2, The click is the meeting (The Ports' three readings) | A | holds |
| L90 | The staggering is exact | ALGEBRA.md at b254f4d2, A family's declaration (The staggering is exact) | A | holds |
| L91 | The quarter turn of a two-plane record | ALGEBRA.md at b254f4d2, The direction (The quarter turn of a two-plane record) | A | holds |
| L92 | The exact bands: the integer rotations | ALGEBRA.md at b254f4d2, A family's declaration (The exact bands) | A | holds |
| L93 | The nucleon is a compact body of its family: the Hartree-Fock identity | ALGEBRA.md at b254f4d2, The hypotheses under their own names (The nucleon is a compact body of its family) | A | holds |
| R01 | The computed pair's limits | Universe24_Paper.tex, Introduction | A | holds |
| R02 | The clock's rate is exact in 2 sin(omega / 2) | Universe24_Paper.tex 3.4; S.31 | A | holds |
| R03 | The cut region's uniform mode | Universe24_Paper.tex 5.3 | A | holds |
| R04 | The folded axis carries the band | Universe24_Paper.tex 9.1 | A | holds |
| R05 | Friedmann's dust equations and the redshift | Universe24_Paper.tex 7.5; S.29 | A | holds |
| R06 | The content to first order in the clock | Universe24_Paper.tex 8 (a); ALGEBRA.md, The ledger of exactness | B | holds |
| R07 | The two readings of beta | Universe24_Paper.tex 8 (b) | B | holds |
| R08 | gamma_K - 1 is half the gap squared | Universe24_Paper.tex 10.1; S.27 | B | holds |
| R09 | The lattice's half-sine variable | S.31 | B | holds |
| R10 | The ports are exactly orthogonal | Universe24_Paper.tex 9.3; S.51; Universe24_Paper.tex 10.1 | A | holds |
| R11 | The fringe's spacing and the near-field minima | S.23 | A | holds |
| R12 | Newton's constant and alpha_law's numbers | S.25, Eq. (20); S.26 (b) | A | holds |
| R13 | The rule's total at the width | ALGEBRA.md, The bound | A | holds |
| R14 | A body stands, in integers | ALGEBRA.md, The integer budget of a derived row; Universe24_Paper.tex 9.2 | A | holds |
| R15 | The one-sided mixed term's dispersion | S.36 (i) | A | holds |
| F01 | The law's weighted form change as printed | ALGEBRA.md at 3a334eeb, The mass defect is the form's fall at a kept count (The surplus leaves) | A | finding |
| F02 | Row 14's unweighted sum as printed | row 14 of The conventions and the units | A | finding |
| F03 | The quadratic reading at Gamma = 2,400 as printed | ALGEBRA.md, The paces compose (R169 (h)) | A | finding |
| F04 | S.14's plain phase fails at the first order | S.14 (since d7e97674) | B | holds |
| F05 | The plain monopole is the uniform-pace case | S.42, inputs (since 9775922e) | A | holds |
| F06 | The momentum identity at non-uniform paces as printed | Universe24_Paper.tex 4.3 | A | finding |
| F07 | S.42 (b)'s Fourier weight for every body | S.42 (b) | B | finding |
| F08 | Light's stress at the band's top as printed | Universe24_Paper.tex 4.3 (since 5f5df82b) | A | finding |
| R16 | The massless row's two double roots and the staggered mode | ALGEBRA.md at 3a334eeb, No write from outside Rule3 wakes either double root of the massless row (the generator; the shelved ion's remedy) | A | holds |
| R17 | Light's written stress over its written energy at finite k | Universe24_Paper.tex 4.3 (since 5f5df82b) | A | holds |
| R18 | The division act's stop is the integer square root | Universe24_Paper.tex, the one root (since 5f5df82b); ALGEBRA.md, The six verbs | A | holds |
| R19 | The shears' exact angle at small angles | Universe24_Paper.tex 5.5 (since d7e97674); S.61 row 9 | B | holds |
| N01 | S.4, the cube's group of 48 | S.4 | D | none |
| N02 | S.37, confinement | S.37 | D | none |
| N03 | S.38 (c), the binding bound | S.38 (c), (d) | C | none |
| N04 | S.39 (a), the gapped kernel | S.39 (a) | C | none |
| N05 | S.41 (1), (2), the prediction and the gravity of light | S.41 | C | none |
| N06 | S.45 (b) to (e), the nuclear well's binding, capture and size law | S.45 | C | none |
| N07 | S.46 (a), (b), (d), the atom's levels and the holders the electron does not read | S.46 | C | none |
| N08 | S.60, the atom under the two lines | S.60 | C | none |
| N09 | S.61, the engine's derivation ledger | S.61 | D | none |
| N10 | S.62, the implementation's versions of the click's write | S.62 | D | none |
| N11 | S.49, S.52 to S.56, the words, the bodies, the masses, the lattice's properties, the conservation picture, the findings | S.49, S.52, S.53, S.54, S.55, S.56 | D | none |
| N12 | S.19's orbit step and S.21's orbit on the exact band | S.19; ALGEBRA.md, The push on a moving record | C | none |
| N13 | The lattice constants | ALGEBRA.md, The lattice constants; S.38's check | C | none |
| N14 | The draw's share to within s_k / 2^63 | ALGEBRA.md at 3a334eeb, The click's algebraic definition (the draw) | D | none |

## A01. Theorem 4's Yukawa exponent

**Place.** Universe24_Paper.tex 7.2, Theorem 4; S.13; the writer's (1), the advisor's (1)

**Statement.** A Yukawa kernel's log-derivative at one separation is 1 + kappa R; a body's integrated well energy has the running exponent s(R) = 1 + kappa R <u^2> / <u> in the body's own weights, 1.0176, 2.130, 2.971, 2.9997 at kappa R = 0.01, 1, 10, 100, from 1 at kappa R << 1 to the contact kernel's 3 at kappa R >> 1 through 2 at 0.821; the virial and the second variation stand with s the integrated exponent, and R^2 F'' carries R s'(R) W.

**Ground.** the Gaussian body's well moments in closed form through erfc (I = 2 - 2 sqrt pi z erfcx z, J = -4 z + (2 + 4 z^2) sqrt pi erfcx z), the asymptotes by the residual's order

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_audit.py, `check_theorem_4s_integrated_exponent`

**Note.** The paper's sentence at 2836519e, 's(R) = 1 + kappa R ... holds in the two asymptotic regimes', held at kappa R << 1 and failed at kappa R >> 1 (the audit's item 1); main 7.2 and S.13 since 9775922e print the integrated exponent, 2.130 at kappa R = 1, 2.971 at 10 and the crossing of 2 at 0.82, recomputed.

**Far-regime witness.** kappa R = 100: the integrated exponent 2.9997 against the printed large end 3 (3 - 3 / z^2 + O(z^-4)) and against 1 + kappa R = 101 of the sentence at 2836519e; the small end 1 + sqrt pi kappa R + O(z^2) to its order

## A02. The time-Link recurrence's Wronskian

**Place.** Universe24_Paper.tex 5.5, S.9, S.33 and ALGEBRA.md row 9 of The conventions and the units, the two-angle form at every place since d7e97674; the writer's (2), the advisor's (2)

**Statement.** The law's step e^(i theta_t) z_next + e^(-i theta_(t-1)) z_before = M z_now / w conserves W_i = Im(conj(z_now) e^(-i theta_(t-1)) z_before) under the per-Node continuity identity for any paces, Link phases and time angles, and the weighted total SUM W_i / p_i^2 exactly; the one-theta form of 5.5 conserves W at a static angle only, |z_2| = 1.93 against the law's 1.00 at the audit's one-Node witness.

**Ground.** exact Gaussian rationals on four periodic boards with Link factors; the audit's witness in floats

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_form.py, `check_the_wronskian_under_the_time_link_turn_for_any_angle_in_time`

**Note.** The slip was the paper's 5.5 sentence at 2836519e (one theta on both levels); since d7e97674 main 5.5, S.9 and S.33 print the two-angle step with the Wronskian booked from the turned levels and conserved exactly for any level in time, as the law's row 9 and the engine's rotation act have it; the one-theta witness is kept as the contrast.

## A03. S.42's monopole

**Place.** S.42, inputs and (c); the writer's (3), the advisor's (3)

**Statement.** At static non-uniform paces the conserved monopole is the weighted sum SUM_i W_i / p_i^2 (S.33 (a), S.9's D M symmetric), the plain sum its uniform-pace case; at the audit's two-Node witness, paces squared (1, 2) and couplings (a, 2 a), the weighted sum stands exactly while the plain sum moves.

**Ground.** exact Gaussian rationals at random levels and self coefficients

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_audit.py, `check_the_weighted_monopole_at_the_two_node_witness`

**Note.** S.42's input at 2836519e, the plain sum 'exactly conserved for a static self-level', was the audit's finding; since 9775922e S.42 prints the weighted sum with 'the plain sum its uniform-pace case', row `F05`'s check.

## A04. S.39 (b)'s band is real for every pair

**Place.** S.39 (b); the writer's (4), the advisor's (4)

**Statement.** kappa is the static kernel's fall per Link, cosh kappa = 3 den / num - 2; with S = 0 at the vacuum's paces 2 cos omega = (2 num / 3 den) SUM_a cos k_a runs from 2 num / den to -2 num / den, within [-2, 2] for every pair with num <= den, so no quantum stands 'above the band's top' and the clause does not follow from kappa > 1; [1, 2] has cosh kappa = 4 and the band from 60 to 120 degrees.

**Ground.** exact rationals at the zone's corners and random cosines for every pair to den = 39

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_audit.py, `check_s39s_band_is_real_for_every_pair`

**Note.** S.39 (b)'s clause at 2836519e, 'a range below one Link, whose quanta would be above the band's top', reads since 5f5df82b 'where the kernel's lattice sum departs from its continuum integral'; the band's reality for every pair stands as the check.

## A05. S.43 (e)'s Stark sentence

**Place.** S.43 (e); the writer's (5), the advisor's (5)

**Statement.** A uniform static Link phase is a gauge on an open domain (the step with the phases is conjugate to the plain one by the diagonal e^(i theta x), the modes unchanged) and a holonomy on the periodic board (the conjugation fails at the wrap unless N theta is a multiple of 2 pi; it shifts the allowed k and mixes no mode of a body); Stark's shift needs a holder level with a gradient across the body at omega_L = 0.

**Ground.** exact Gaussian rationals on an open and a periodic chain of six

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_audit.py, `check_a_uniform_link_phase_is_a_gauge`

**Note.** S.43 (e) since 9775922e: 'a static holder level with a gradient across the body (omega_L = 0, grad b_L not 0) mixes the modes without a transition, Stark's shift; a uniform static phase is a gauge', the check's content.

## A06. S.17's beat

**Place.** S.17; Universe24_Paper.tex 7.5; the writer's (6), the advisor's (6)

**Statement.** The finite window's mean of the cross current of two standing records is the sum-frequency term's, bounded by 2 / ((omega_1 + omega_2) n T_b) for n beats of length T_b: 0.0083 over one beat at A = B = num = 1, omega_1 = 0.4, omega_2 = 0.4 + 2 pi / 20, and 1.1 x 10^-4 over 100 beats (the bounds 0.09 and 0.0009), falling as 1 / n and never 0 at a finite window.

**Ground.** a hand bound on the oscillating sum; the means and the bounds recomputed, the inequality at random phases

**Kind and verdict.** C, witness only.

**Check.** tools/derivations/proofs_audit.py, `check_s17s_beat_mean_bound`

**Note.** S.17 at 2836519e printed 'its mean over the beat is 0'; since 9775922e 'its mean over n beats is 0 to the order of the fast term over the window, 1 / ((omega_1 + omega_2) n T_b) with T_b the beat's length', the bound the witness recomputes.

## A07. S.24's orientation

**Place.** S.24 and Universe24_Paper.tex 10.2; the writer's (7), the advisor's (7)

**Statement.** The directional k^4 coefficient C(n) = (3 SUM_a n_a^4 - 1) / 24 is 1 / 12 on an axis, 1 / 48 on a face diagonal and 0 on the body diagonal, continuous toward it (C / C_axis = 4.4 x 10^-11 at n proportional to (1.00001, 1, 1), the Link bound weakening by 1.5 x 10^5 there); the mean over directions, <SUM n_a^4> = 3 / 5, gives C_mean / C_axis = 2 / 5; the bound weakens tenfold only within about 4 degrees of a body diagonal, one percent of the sky, and a hundredfold within 0.4 degrees.

**Ground.** C(n) as the band's own fourth order (proofs_band), the caps by bisection over the azimuths

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_audit.py, `check_the_orientation_coefficient`

**Note.** S.24 since 9775922e prints 'The orientation', C(n), the mean's 2 / 5 and the caps of 4 and 0.4 degrees, and main 10.2 the sentence on the bounds' comparison; recomputed.

**Far-regime witness.** the eight body diagonals, where the bound is void: the caps of 4.1 and 0.41 degrees, 1.0 and 0.01 percent of the sky

## A08. S.57's wall

**Place.** S.57 (a); the writer's (8), the advisor's (8)

**Statement.** One quantum's inflow is Phi_A + Phi_B <= W_c sin Omega, the born unit, and s_X = eta Phi_X / (W_c sin Omega), so complete equal absorption gives s = eta / 2 and P(neither) = 1 - eta, where the rule at 2836519e, s_X = eta Phi_X / W_c, would leave 1 - eta sin Omega (S.57 since 9775922e prints the born unit W_c sin Omega in the wall and in the transfer); alpha = 0 for one quantum under the one draw, and for two quanta 1 / 2 by the mean counts and 2 / (2 - s)^2 per trial, 8 / 9 at s = 1 / 2.

**Ground.** exact rationals

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_credit.py, `check_the_anticoincidences_algebra_and_s57s_wall`

## A09. 10.2's 'hence'

**Place.** Universe24_Paper.tex 10.2; the writer's (9), the advisor's (9)

**Statement.** Reversibility to the bit with no loops does not by itself give no running of alpha and no Lamb shift; the ground is S.37's 'no pair is created and no coupling runs' from the count's conservation between clicks, the writer's word 'and, with no pair created between clicks (S.37),'.

**Ground.** a sentence's ground; no quantity to compute

**Kind and verdict.** C, none.

**Check.** none.

**Note.** No machine check applies to a sentence's logical ground; main 10.2 since 9775922e carries the premise, 'with no pair created between clicks (S.37)'.

## A10. S.26 (d')'s balance at every step

**Place.** S.26 (d'); the writer's (10), the advisor's (10)

**Statement.** The gain side is exact: the discrete form H_t = (1 / 2) |l_(t+1) - l_t|^2 - (1 / 2) l_(t+1) . L l_t of the holder's line with L symmetric changes per step by exactly (1 / 2) s_t . (l_(t+1) - l_(t-1)); the loss side is the finite sine difference T [sin omega - sin(omega - Delta theta)] = 2 T cos(omega - Delta theta / 2) sin(Delta theta / 2); their ratio is kappa (1 + (Delta theta / 2) tan omega_s + O(Delta theta^2)), so the balance closes to first order in the turn with the remainder (Delta theta / 2) tan omega_s, below 10^-18 at nature's turn and not 0.

**Ground.** the gain identity exact with a random symmetric L, the sine difference exact at rational half-angles, the remainder by the residual's order

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_audit.py, `check_s26_d_primes_finite_step_remainder`

**Far-regime witness.** the largest turn the law allows (the tangent half-angle at most 1, Delta theta = pi / 2): the exact ratio at [2, 3] is 1.348 against the first order's 1.878, so 'at every step and for every motion' is first order in the turn, as S.26 (d') since 9775922e says, 'to first order in the turn at every step and for every motion', the remainder (Delta theta / 2) tan omega_s printed

## L01. The line's band identity

**Place.** ALGEBRA.md, The line; row 3 of The conventions and the units; S.1

**Statement.** A plane wave A cos(k . x - omega t) in the line without its remainder leaves the residual a_now [2 w cos omega - S - 2 SUM_a R_a cos k_a], so it solves the line iff 2 w cos omega = S + 2 SUM_a R_a cos k_a.

**Ground.** rule3.coefficients and rule3.numerator at random integer paces, exact at rational angles

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_band.py, `check_band_identity_of_a_plane_wave`

## L02. The band at a pace, the Lorentz form

**Place.** ALGEBRA.md, The line (The clock once and the Link twice), The band at a pace; the paper's Eq. (4); S.1

**Statement.** cos omega = 1 - (1 - num / den) (p_0 / Gamma)^2 - (num / (3 den)) SUM_a (p_a / Gamma)^2 (1 - cos k_a) equals (S + 2 SUM_a R_a cos k_a) / (2 w) with the law's coefficients.

**Ground.** a polynomial identity in the paces and the cosines, exact

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_band.py, `check_band_at_a_pace_is_the_lorentz_form`

## L03. The vacuum's band and light's dispersion

**Place.** row 3 of The conventions and the units; S.1; Universe24_Paper.tex 3.3

**Statement.** At the vacuum's paces S = 12 num Gamma^2 - 6 R = 0 and cos omega = (num / (3 den)) SUM_a cos k_a, the gap cos omega_0 = num / den; light has cos omega = (2 + cos k) / 3 along an axis; rule3.plane_wave_dispersion is the same number.

**Ground.** exact rationals; the derivations' rule3 in floats

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_band.py, `check_vacuum_band_and_lights_dispersion`

## L04. The clocks shift alike

**Place.** ALGEBRA.md, The line (i)

**Statement.** At k = 0 every massive band's rest rotation obeys 1 - cos omega_b = (p_0 / Gamma)^2 (1 - cos omega_0), one factor for every family.

**Ground.** exact rationals from the band at a pace

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_band.py, `check_the_clocks_shift_alike`

## L05. The guard's edge

**Place.** ALGEBRA.md, The guard; S.3; S.61 row 4; Universe24_Paper.tex 3.4

**Statement.** The mode at wave number pi on every axis has the factor (S - 2 SUM_a R_a) / w = 2 - 2 (1 - num / den) (p_0 / Gamma)^2 - 4 (num / den) (p_a / Gamma)^2, -2 num / den in the vacuum, at or above -2 exactly when p^2 (den + |num|) <= 2 den Gamma^2 (the k = 0 mode for a negative numerator), the edge P^2 = 2 den Gamma^2 div (den + |num|), Gamma^2 for light.

**Ground.** exact rationals over every pace to 2 Gamma; rule3.guard_edge_squared

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_band.py, `check_the_guards_edge`

## L06. The total mirror of light

**Place.** ALGEBRA.md, The band at a pace; the derivation script paces.py

**Statement.** Light's record is evanescent where cosh kappa = (Gamma / p_a)^2 (1 - cos k) - 1 > 1, that is p_a < Gamma sin(k / 2), e^(-2 U) below sin(k / 2) under the composed paces: c above 1,733 at lambda = 4 Links and 2,464 at 4.78 at Gamma = 10^4.

**Ground.** the half-angle identity exact at Pythagorean angles; the thresholds by the exact power

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_band.py, `check_the_total_mirror_of_light`

## L07. The three exact bands

**Place.** ALGEBRA.md, The exact bands; Universe24_Paper.tex 6.1

**Statement.** The one-Node line at rest is exact in integers only where 2 cos omega_0 is an integer, so the rule carries exactly three exact rotations, 2 cos omega_0 = 1, 0 and -1, the periods 6, 4 and 3, the pairs [1, 2], [0, 1] and [-1, 2].

**Ground.** the integer matrix [[m, -1], [1, 0]] and its orders

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_band.py, `check_the_three_exact_bands`

## L08. The band's top on the diagonal and the axis

**Place.** S.27

**Statement.** Along the body diagonal light's band is omega = q exactly, no dispersion; along an axis the top at k = pi has cos omega = 1 / 3, omega = 1.231, sin omega = 0.943.

**Ground.** exact at rational cosines; the axis's numbers in floats

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_band.py, `check_the_band_top_along_the_diagonal_and_the_axis`

## L09. The largest group speed

**Place.** S.21

**Statement.** On the full band v_g is largest at k = (pi / 2, pi / 2, pi / 2), (num / den) / sqrt 3 = c cos omega_0, 0.3849 at [2, 3].

**Ground.** the value exact; the maximum over a grid of the zone a witness

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_band.py, `check_the_largest_group_speed`

## L10. The content's index for every family

**Place.** S.28; Universe24_Paper.tex 8 (p); The paces compose

**Statement.** A stationary boundary conserving omega gives 1 - cos k_in = [1 - cos k + 3 (den - num) (1 - N^2) / num] / N^4 exactly; for light sin(k_in / 2) = sin(k / 2) / s with s = N^2; the phase index (2 / k) arcsin(sin(k / 2) / s) = 1 / s + k^2 (1 / s^3 - 1 / s) / 24 + O(k^4), to first order in U 1 + [4 tan(k / 2) / k] U, 1.380 at k = pi / 2 and s = 0.8.

**Ground.** the exact lines in Fractions; the expansions by the residual's orders 4 and 2

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_band.py, `check_the_contents_index`

**Far-regime witness.** k = pi / 2 at s = 0.8: the exact ratio 1.380 against the ray limit's 1 / s = 1.25, the chromatic dispersion the ray limit lacks

## L11. The slow matter's index limit

**Place.** S.28's check

**Statement.** The 1 / k^2 term of the slow index, 12 (den - num) U / (num m*^2 v^2) = [4 (1 - cos omega_0) / (3 cos omega_0 tan^2 omega_0)] U / v^2, tends to (2 / 3) U / v^2 = 2 Phi / v^2 as omega_0 -> 0, nature's index for a slow body.

**Ground.** the identity in floats to 10^-9, the limit by the residual's order 2

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_band.py, `check_the_slow_matters_index_limit`

**Far-regime witness.** the coefficient 0.533 at [2, 3] against the small-gap 2 / 3

## L12. The reach of a holder with a gap

**Place.** ALGEBRA.md, The well; S.11; S.39's check

**Statement.** cosh kappa = 3 den / num - 2 from 6 den = num (2 cosh kappa + 4); kappa^2 = 6 den / num - 6 to the second order in the gap; [1, 2] has cosh kappa = 4, e^(-kappa) = 0.127; R = sqrt(num / (6 (den - num))) = 20.00 at [2400, 2401]; inside a thick body the rest is 3 den sigma / (num kappa^2); Yukawa's identity c / omega_g = R sqrt(den / num) to the gap's first order.

**Ground.** exact rationals; the two expansions by the residual's orders 2 and 1

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_band.py, `check_the_reach_of_a_holder`

## L13. The group velocity

**Place.** ALGEBRA.md, The band at a pace; S.1; rule3.group_velocity

**Statement.** d omega / dk = (R_a / w) sin k / sin omega = (num / (3 den)) (p_a / Gamma)^2 sin k / sin omega along an axis, the vacuum's (num / (3 den)) sin k / sin omega.

**Ground.** the centred difference quotient of the band's omega(k), order 2 at halving

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_band.py, `check_the_group_velocity`

## L14. Light's speed and dispersion

**Place.** S.1; ALGEBRA.md, The lattice constants; Universe24_Paper.tex 10.2

**Statement.** For [1, 1] along an axis cos omega = 1 - k^2 / 6 + k^4 / 72 + O(k^6), omega = (k / sqrt 3) (1 - k^2 / 36 + O(k^4)) and d omega / dk = (1 / sqrt 3) (1 - k^2 / 12 + O(k^4)): the speed 1 / sqrt 3 at long wavelength and the group speed falling as 1 - 0.083 k^2; S.1's check -0.0833, -0.0834, -0.0835 at k = 0.05, 0.1, 0.2.

**Ground.** the residuals' orders 6, 5 and 4; the numbers recomputed

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_band.py, `check_lights_speed_and_dispersion_series`

## L15. The fourth order of light's band

**Place.** S.24; ALGEBRA.md, The law's own formulas B (11)

**Statement.** The k^4 coefficient of omega^2 along n is 1 / 108 - SUM_a n_a^4 / 36: -1 / 54 on an axis, 0 on the body diagonal, -1 / 135 on the directional mean (<n_a^4> = 1 / 5); the anisotropies, an axis against the face diagonal k^2 / 48 in phase and k^2 / 16 in group, against the body diagonal k^2 / 36 and k^2 / 12.

**Ground.** each coefficient by the residual's order 6 along its direction, the mean exact

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_band.py, `check_the_fourth_order_of_lights_band`

## L16. Rule3's coefficients are the read's own without tension

**Place.** ALGEBRA.md, The paces (The clock is the Node's, the tension is the Link's); rule3.coefficients

**Statement.** At q_ij = Gamma the Link's read coefficient 2 num p_i^2 q_ij^2 / Gamma^2 is rule3's R_a = 2 num p_a^2 at p_a = p_i = p_0^2 / Gamma and the self coefficient 12 den Gamma^2 - 12 (den - num) p_0^2 - SUM over the six Ports of R_ij is rule3's S: the general read and the derivations' Rule3 are one line where no tension stands.

**Ground.** exact rationals on four periodic boards

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_form.py, `check_rule3s_coefficients_are_the_reads_own_without_tension`

## L17. Theorem 3, the conserved form

**Place.** ALGEBRA.md, The conserved form; the paper's Theorem 3; S.48

**Statement.** With D = diag(1 / p_i^2), p_i = p_0(i)^2 / Gamma, D M is symmetric under R_a(i -> j) = 2 num p_i^2 q_ij^2 / Gamma^2 with q_ij = q_ji, and Q(x, y) = x . D x + y . D y - x . D M y satisfies Q(a_next, a_now) = Q(a_now, a_before); E = w Q is exact for any field and any tensions before the integer remainders.

**Ground.** exact fractions on four periodic boards over several intervals, the vacuum's paces and the no-tension cases forced

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_form.py, `check_theorem_3_the_weighted_form_is_exact_in_the_line`

## L18. The plain form fails under a tension, S.32's two witnesses

**Place.** S.32; ALGEBRA.md, The conserved form

**Statement.** Three Nodes at [1, 1], Gamma = 4, q = 2 (R = 8, w = 96, S = 144), now = (1, 0, 0): next = (11 / 6, 1 / 12, 1 / 12), the plain form from 6 to -21 / 4 and Eq. (6) 6; 3^3 Nodes at [2, 3], Gamma = 10, q = 5 (R = 100, w = 1,800, S = 1,800), a uniform 3 over 0: next = 4 with the remainder 0, the plain form per Node 162 to -54 and Eq. (6) 162 (4,374 over the board); at q = Gamma the two forms coincide.

**Ground.** exact fractions and integers

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_form.py, `check_the_plain_form_fails_under_a_tension_the_two_witnesses_of_s32`

## L19. The remainders' walk of the form

**Place.** ALGEBRA.md, The conserved form (the proof's last sentence), row 7 of The conventions and the units; the paper's 4.3

**Statement.** The integer step's next = next* + (r - r') / w adds to Q the walk SUM_i epsilon_i (next_i - before_i), epsilon_i = (r_i - r_i') / w, so E walks by SUM_i (r_i - r_i') (next_i - before_i) / p_i^2 (rule3.form_walk), each term below one unit of the level's change; E_3 walks by SUM_i [epsilon_i(t) next_i - epsilon_i(t + 1) now_i] / p_i^2.

**Ground.** exact integers on four boards with tensions, 40 intervals each

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_form.py, `check_the_remainders_walk_of_the_form`

## L20. The three-level form equals the two-level form

**Place.** row 7 of The conventions and the units; Universe24_Paper.tex 4.3

**Statement.** Q = SUM_i (now_i^2 + before_i^2) / p_i^2 - (1 / w) SUM_i (SUM_j R_ij now_j + S_i now_i) before_i / p_i^2 equals E_3 = SUM_i (now_i^2 - next_i before_i) / p_i^2 exactly under the line, and D_i = b^2 sin^2 omega on a plane wave.

**Ground.** exact fractions on four boards with tensions and at rational angles

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_form.py, `check_the_three_level_form_equals_the_two_level_form`

## L21. The form's change under moving paces

**Place.** Universe24_Paper.tex 4.3

**Statement.** Where the paces move, D = |a_now|^2 - <a_next, a_before> changes exactly by D(t + 1) - D(t) = <a_next, (M(t) - M(t + 1)^T) a_now>, and the weighted E with the weights of the paces at t + 1 by a_next^T D (M(t) - M(t + 1)) a_now.

**Ground.** exact fractions, two reads with different contents on three boards

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_form.py, `check_the_forms_change_under_moving_paces`

## L22. Theorem 1, the direction

**Place.** ALGEBRA.md, The direction; the paper's Theorem 1; S.48

**Statement.** The forward call (a_now, a_before, r) gives (a_next, r') and the backward call (a_now, a_next, r') gives (a_before, r) bit for bit; the proof's identities -floor(u / w) = ceil(-u / w) and ceil((w a - r) / w) = a for 0 <= r < w.

**Ground.** the identities over every residue at every wall to 40 (both sides shift by one with u + w); rule3.step and rule3.step_backward round trips at random integers

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_form.py, `check_theorem_1_the_direction`

## L23. The cube's symmetry: the complement identity

**Place.** ALGEBRA.md, The direction (The cube's symmetry), the proof's act (1)

**Statement.** floor((w - 1 - u) / w) = -floor(u / w) for every integer u, the ones' complement commuting with the floor division by a positive wall, its remainder w - 1 - r'; the zero-remainder lay's floor(-u / w) = -ceil(u / w) differs wherever w does not divide u.

**Ground.** every residue at every wall to 60

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_form.py, `check_the_complement_identity_of_the_cubes_symmetry`

## L24. The cube's symmetry act by act

**Place.** ALGEBRA.md, The direction (The cube's symmetry), the proof's acts (2) to (6)

**Statement.** A lay invariant under one of the cube's 48 with the complement remainders is invariant to the bit under every act of the step, so one fundamental domain steps the whole.

**Ground.** the engine's acts (the write, the reads, the time and Link turns); the integer identity of act (1) is row `L23`

**Kind and verdict.** D, none.

**Check.** none.

**Note.** A statement of the engine's acts; tests/test_the_node.py and the symmetric lay's runs show it.

## L25. The Wronskian with the form's weights

**Place.** ALGEBRA.md, The paces (The sign is the rotation sense); S.9

**Statement.** W = re_now^T D im_before - im_now^T D re_before is invariant under the line with D M symmetric; per Node W_i / p_i^2 changes by (2 num / w) (q_ij^2 / Gamma^2) (im_i re_j - re_i im_j) over the six Ports, (num / (3 den)) per Port for the integer W_i at the vacuum; S.9's chain of three at Gamma = 2 (W_0 from 0 to 3, the current 3 / 4) and the integer counterexample at [2, 3], (1, 3) over zeros to (1, 4), W from 0 to -1.

**Ground.** exact fractions on four boards with tensions; rule3.step for the witnesses

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_form.py, `check_the_wronskian_is_conserved_with_the_forms_weights`

## L26. The sign current's flux over density

**Place.** S.33 (b); S.61 row 8

**Statement.** For the plane record the density is w A^2 sin omega and the flux through a Link R_a A^2 sin k_a, so flux over density is (R_a / w) sin k_a / sin omega = d omega / dk_a, the current rho v exactly; J_a = g_(i, i+a) + g_(i-a, i) = 2 A^2 sin k_a = (6 den / num) W v at the vacuum's paces.

**Ground.** exact Gaussian rationals at rational angles

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_form.py, `check_the_sign_currents_flux_over_density`

## L27. The velocity invariant of the massless row

**Place.** ALGEBRA.md at 915c6a7b, The click writes on the lattice (the restoring front's third test; the front is history at 3a334eeb under the dense record's clause, the identity of the line standing); ENGINE.md, the face's kicks

**Statement.** For a record at uniform paces with S + SUM R = 2 w the velocity sum SUM now - SUM before is kept by the line and the integer V = w (SUM now - SUM before) + SUM r is exactly invariant on a periodic board; for a gapped pair it moves by -12 (den - num) Gamma^2 SUM now per interval.

**Ground.** exact integers by rule3.step on four periodic boards, 100 intervals

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_form.py, `check_the_velocity_invariant_of_the_massless_row`

## L28. The write's total is exact over any window

**Place.** ALGEBRA.md, The integer-exact constructions (4); The integer budget of a derived row

**Statement.** The sum over n intervals of the written q_t is (the sum of the numerators + r_0 - r_n) / w exactly, in (-1, 1) of the line's sum; the remainders' terms telescope to (r_0 - r_n) / w.

**Ground.** exact integers at random numerators and walls

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_form.py, `check_the_writes_total_is_exact_over_any_window`

## L29. The booking identity of the hole

**Place.** S.50 (R289); ALGEBRA.md, The click is the meeting

**Statement.** Q(p, q) = SUM_i [w p_i^2 + w q_i^2 - p_i (S q_i + SUM_j R_ij q_j)] at uniform coefficients satisfies Q(next, now) = Q(now, before) and Q(now, before) = w SUM_i D_i; a face writing x for the level v the step would write changes Q by (x - v) [w (x + v) - (S now_i + SUM_j R_ij now_j)] = w (x - v) (x - b), at most w (v - b)^2 / 4 removed at the midpoint.

**Ground.** exact fractions on three periodic boards

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_booking.py, `check_the_booking_identity_of_the_hole`

## L30. The share identity at any paces

**Place.** ALGEBRA.md, The share's change is the currents; the paper's Eq. (10); S.5

**Statement.** e_i(next*, now) - e_i(now, before) = SUM_j (q_ij^2 / Gamma^2) F_ij, since R_ij / (2 p_i^2) = num q_ij^2 / Gamma^2 is the same from both ends; the integer step adds -(next_i - before_i) (r'_i - r_i) / (2 p_i^2); S.5's witnesses, the chain of five at [2, 3] and the uniform 3 over 0 reading 81 where the mean-of-paces form read 324.

**Ground.** exact fractions and integers with Link factors

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_booking.py, `check_the_share_identity_at_any_paces`

## L31. The share is conserved at standing paces

**Place.** ALGEBRA.md, The count is the record's share (Theorem); Universe24_Paper.tex 4.4

**Statement.** Over any region whose paces stand, SUM e_i changes in one step by the weighted currents through the region's boundary Links and the remainder terms alone, the interior Links cancelling by F_ji = -F_ij and q_ji = q_ij.

**Ground.** exact fractions on a chain of five with a region of two and the whole board

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_booking.py, `check_the_share_is_conserved_over_a_region`

## L32. The vacuum's share

**Place.** ALGEBRA.md, The count is the record's share; Universe24_Paper.tex Eq. (9)

**Statement.** At the vacuum's paces the share is exactly 3 den (now_i^2 + before_i^2) - num now_i S_6(before)_i.

**Ground.** exact integers on a chain and a box

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_booking.py, `check_the_vacuum_share`

## L33. The plane wave's current and form

**Place.** ALGEBRA.md, The booking; The velocity

**Statement.** A plane record travelling from i to j has F_ij = -2 num |psi|^2 sin omega sin k summed over its two lines; one real line has F = -num A^2 sin omega sin k exactly at every Node with no oscillating part, and D = A^2 sin^2 omega.

**Ground.** exact at rational angles

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_booking.py, `check_the_plane_waves_current_and_form`

## L34. The momentum flux identity with the remainders

**Place.** ALGEBRA.md, The tension; the paper's Eq. (7); row 5 of The conventions and the units; S.48

**Statement.** At uniform coefficients w [P_a(t + 1) - P_a(t)] = SUM_b R_b [G_ab(i) - G_ab(i - b)] with G_ab(i) = now_i (now_(i+a+b) - now_(i-a+b)) - now_(i+b) (now_(i+a) - now_(i-a)); with the rounding the identity holds up to -[delta_i Delta_a now_i - now_i Delta_a delta_i], delta = r - r', exactly; and G_aa(i) = h_a(i) + h_a(i + a).

**Ground.** exact integers on a periodic 5-box at every Node and axis by rule3.step, anisotropic uniform paces included

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_booking.py, `check_the_momentum_flux_identity_with_the_remainders`

## L35. The tension of a plane wave

**Place.** S.7; row 6 of The conventions and the units

**Statement.** For now_i = b cos(k x_i + phi) along the axis G_aa = -2 b^2 sin^2 k at every Node, the Link's booking 2 num b^2 sin^2 k and the Node's tension T_aa = -num h_a = num b^2 sin^2 k; the cross reading G_ab = -2 b^2 sin k_a sin k_b.

**Ground.** exact at rational angles

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_booking.py, `check_the_plane_waves_stress`

## L36. The two share forms summed over the board

**Place.** row 14 of The conventions and the units

**Statement.** The share's one-sided form and the hole's symmetric form agree summed over the board with the share's weight 1 / p_i^2 inside, SUM_i a_i SUM_j R_ij b_j / p_i^2 = SUM_i b_i SUM_j R_ij a_j / p_i^2, and differ at a Node; without the weight they agree at uniform paces.

**Ground.** exact fractions on three boards with tensions

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_booking.py, `check_the_two_share_forms_summed_over_the_board`

## L37. The exact lay's operator line

**Place.** ALGEBRA.md, The packet lay (The generator)

**Statement.** With L the line's own read, (L f)_i = (S f_i + SUM over the six Ports of R f_j) / (2 w), of eigenvalue cos omega(q) on e^(i q x), the record one interval earlier is z_(-1) = (L + i sqrt(1 - L^2)) z, so before = L a - sqrt(1 - L^2) s exactly with the backward root 0; the expansion about c = cos omega_k, before_i = (c a_i - s_k s_i) + [(L a)_i - c a_i] + (c / s_k) [(L s)_i - c s_i] + O((L - c)^2), its remainder (1 / 2) f'' (L - c)^2 with f = sqrt(1 - L^2), f'' = -1 / s_k^3 and L - c = -s_k v_g delta, -v_g^2 delta^2 / (2 s_k); the plain lay's backward root 0.02991 at delta = 0.05 and 0.05662 at 0.10 against the first order 0.03173 and 0.06345.

**Ground.** the eigenvalue and the addition formula exact at rational angles; the expansion by the residual's order 2 and its coefficient; the roots recomputed

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_booking.py, `check_the_exact_lays_operator_line`

## L38. The paces compose

**Place.** ALGEBRA.md, The paces compose; S.34 (a)

**Statement.** p_0(c + 1) = p_0(c) (1 - 1 / Gamma), so p_0 = Gamma (1 - 1 / Gamma)^c and P(U + l) = P(U) P(l) exactly; p_i = p_0^2 / Gamma.

**Ground.** exact fractions by rule3.clock_pace and rule3.node_pace

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_paces_compose_exactly`

## L39. The clock's exponential and its readings

**Place.** ALGEBRA.md, The paces compose; S.34 (a), (e); The paces

**Statement.** p_0 is Gamma e^(-U) to O(1 / Gamma), the relative departure U / (2 Gamma) (0.951225 against 0.951229 at Gamma = 6,000, c = 300); its square is Gamma^2 - 2 Gamma c + 2 c^2 to the second order, the composition differing at -4 U^3 / 3 (0.905000 against 0.904837 at U = 0.05) while the Link's (Gamma - 2 c)^2 is e^(-4 U) to the first order only (0.8100 against 0.8187); the quadratic reading Gamma - c + c^2 div 2 Gamma within Gamma U^3 / 6 of a unit (1.02 at Gamma = 6,000 and 2.0 at 12,000 at U = 0.10) and the cubic within Gamma U^4 / 24 of a unit (0.05 and 0.13 at U = 0.15).

**Ground.** the orders by the residual at two step sizes, the numbers exact

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_clocks_exponential_and_its_readings`

**Note.** The printed 0.41 at Gamma = 2,400 is row `F03`.

## L40. The acts' factors

**Place.** ALGEBRA.md, The write per proper volume and per proper interval; S.34 (d)

**Statement.** With N = p_0 / Gamma and h = p_0 / p_a = 1 / N under p_a = p_0^2 / Gamma, a count source carries N^2 / (h_x h_y h_z) = N^5 = p_x p_y p_z / (p_0 Gamma^2) and the Wronskian N / (h_x h_y h_z) = N^4 = p_x p_y p_z / (p_0^2 Gamma); with a tension the rulers differ and the volume is h_x h_y h_z.

**Ground.** exact fractions

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_acts_factors`

## L41. The exponential metric's post-Newtonian orders

**Place.** S.34 (c); S.19; Universe24_Paper.tex 3.4 and 8

**Statement.** g_00 = -e^(-2 U) = -(1 - 2 U + 2 U^2) + O(U^3) and g_ij = e^(2 U) delta_ij = (1 + 2 U + 2 U^2) delta_ij + O(U^3): gamma = 1 exactly and beta = 1 in U; the remainders -4 U^3 / 3 and 4 U^3 / 3.

**Ground.** the residuals' order 3 and their coefficients

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_exponential_metrics_post_newtonian_orders`

**Far-regime witness.** U = 0.5: e^-1 = 0.368 against the truncation's 0.500 and e^1 = 2.718 against 2.500, the orders holding and the values parting

## L42. The clock's click rate

**Place.** S.15; Universe24_Paper.tex 7.4 and 8 (a); The method of derivation, step 3

**Statement.** cos omega(U) = cos omega_0 + 2 g U - 2 g U^2 exactly at the quadratic clock; d omega / omega_0 = -f(omega_0) dU with f = 2 (1 - cos omega_0) / (omega_0 sin omega_0), 1.063 at [2, 3]; f = 1 + omega_0^2 / 12 + O(omega_0^4), 5.9 percent at the computed pair (6.3 exactly), 1 as the gap closes.

**Ground.** exact fractions for the quadratic clock; the residual's orders 2 in U and 4 in omega_0

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_clocks_click_rate`

**Far-regime witness.** num / den = 0.01: f = 1.269 against the series' 1.203; [999999, 1000000]: f = 1.0000002

## L43. The fall and Kepler's potential

**Place.** S.18; the paper's Eq. (14); ALGEBRA.md, The method of derivation

**Statement.** m* = 3 den sin omega_0 / num = 3 tan omega_0; a = [num / (3 den sin omega_0)] [2 g / sin omega_0] |grad U| = 2 cos omega_0 / (3 (1 + cos omega_0)) |grad U| = [(1 - epsilon) / (3 (1 - epsilon / 2))] |grad U| in the gap epsilon, 4 / 15 at [2, 3] and 1 / 3 as the gap closes; U_K = [2 cos omega_0 / (1 + cos omega_0)] U, 4 / 5 at [2, 3] and 1 as the gap closes.

**Ground.** exact rationals in cos omega_0 = num / den

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_fall_and_keplers_potential`

**Far-regime witness.** [999999, 1000000]: 0.3333332 and 0.9999995; num / den = 0.01: 0.0066 and 0.0198

## L44. The post-Newtonian parameters of the Kepler column

**Place.** S.19; ALGEBRA.md, The rows against nature (a)

**Statement.** lambda = (den + num) / (2 num); gamma_K = den / num from the bending 4 lambda U_K = (1 + gamma) 2 U_K; beta_K = 2 + 2 den / num - 3 lambda = (den + num) / (2 num) from the periapsis; 1 + alpha_K = f lambda = tan omega_0 / omega_0 from the redshift; 1.5, 1.25 and 1.329 at [2, 3], 1 as the gap closes.

**Ground.** exact rationals; f lambda = tan omega_0 / omega_0 exact in (cos, sin) at rational points

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_post_newtonian_parameters`

**Far-regime witness.** [999999, 1000000]: 1.000001, 1.0000005, 1.0000007; num / den = 0.01: 100, 50.5, 64.1

## L45. The moving clock to the fourth order

**Place.** S.21; Universe24_Paper.tex 8 (e); ALGEBRA.md, The rows against nature (e)

**Statement.** omega(k) = omega_0 + alpha k^2 - beta k^4 + O(k^6) with alpha = c_0 / (2 s) and beta = c_0 / (24 s) + c c_0^2 / (8 s^3); Omega / omega_0 = 1 - v^2 / (2 c_m^2) - (2 omega_0 / sin 2 omega_0) v^4 / (8 c_m^4) + O(v^6), c_m^2 = omega_0 / (3 tan omega_0): Lorentz's factor at c_m to the second order exactly, the fourth order's factor 2 omega_0 / sin 2 omega_0 = 1.6926 at [2, 3], along n omega_0 [(SUM n_a^4) tan omega_0 + cot omega_0], 1.2224 on a face diagonal, 1.0657 on the body diagonal, 1 as the gap closes; S.21's check -3.37 and -2.12 against -3.365 and -2.119.

**Ground.** the band's series by the residual's order 6, the interval's by its order 6; the numbers recomputed

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_moving_clock_to_the_fourth_order`

**Far-regime witness.** the factor at num / den = 0.01 is 156 on an axis and 1.0000003 at [999999, 1000000]

## L46. De Broglie and the three speeds

**Place.** S.22; S.53; Universe24_Paper.tex 3.3

**Statement.** k = m* v with m* = 3 tan omega_0, c_m^2 = omega_0 / (3 tan omega_0) = 0.2508 at [2, 3], and m* c_m^2 = omega_0 exactly for every pair; c_s^2 = num / (3 den), c_m^2 and light's 1 / 3 are one as the gap closes, c_m / c = 0.867 at [2, 3] and 0.9997 at [999, 1000].

**Ground.** exact identity in floats to 10^-12 relative, the limits recomputed

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_paces.py, `check_de_broglie_and_the_three_speeds`

**Far-regime witness.** num / den = 0.01: c_s^2 = 0.0033, c_m^2 = 0.0052 against light's 1 / 3

## L47. The push on a moving record

**Place.** S.58; ALGEBRA.md, The push on a moving record; the paper's Eq. (16)

**Statement.** With E^2 = m^2 + P^2, m = N omega_0, P = c N^2 k, -(d omega / dU)_k = (E^2 + P^2) / E = E (1 + beta^2); the exact line F_perp = grad U [2 (1 - nu) e^(-2 U) + (4 nu / 3) e^(-4 U) SUM_a (1 - cos k_a)] / sin omega; at [2, 3] the rest push over E is f(omega_0) = 1.0634 and the coefficient of beta^2 over it 1.3354 = gamma_K - alpha_K / 2; at [999, 1000] 1.00017 and 1.00067.

**Ground.** the derivative identities by the centred difference's order 2; the numbers recomputed

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_push_on_a_moving_record`

## L48. The shadow's capture radius

**Place.** S.30; ALGEBRA.md, The paces compose

**Statement.** In the index n = e^(2 m / r) a circular ray stands where d(n r) / dr = e^(2 m / r) (1 - 2 m / r) = 0, r = 2 m, and b = 2 e m = 5.437 m, 0.046 above Schwarzschild's 3 sqrt 3 m; the quadratic index 1 / (1 - 2 U) gives r = 4 m and b = 8 m.

**Ground.** the derivative by the centred difference, the roots and numbers recomputed

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_shadows_capture_radius`

## L49. The two clocks under the principle

**Place.** S.31; Universe24_Paper.tex Table 4 and 3.4; ALGEBRA.md, The same clock and the same ruler for every act

**Statement.** omega' = 2 arcsin(N sin(omega / 2)) = N omega [1 - (1 - N^2) omega^2 / 24 + O(omega^4)]; the beat Delta' = N Delta [1 - (1 - N^2) (omega_1^2 + omega_1 omega_2 + omega_2^2) / 24 + O(omega^4)], (1 - N^2) omega^2 / 8 at equal rotations: 0.3916 against 0.4 and 0.3920 at N = 0.8, omega = 0.4, 0.9; 2.5 x 10^-38 at nature's gap; the rest line's rate in omega -2 tan(omega_0 / 2) / omega_0 = -f(omega_0); a cavity of bodies intervals at N exactly.

**Ground.** the series by the residual's order 5, the half-angle identity exact, the numbers recomputed

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_two_clocks_under_the_principle`

**Far-regime witness.** omega = 2 and 3 at N = 0.8: the exact beat 0.372 against N Delta = 0.8 and the series 0.572, outside the small-rotation domain

## L50. Light's index to first order

**Place.** S.2; S.12; Universe24_Paper.tex 8 (p)

**Statement.** n = e^(2 x) = 1 / (1 - 2 x) + O(x^2) and n - 1 = 2 x + O(x^2); two events over L Links arrive L sqrt 3 [1 / (1 - 2 x) - 1] = 2 x L sqrt 3 + O(x^2) intervals apart.

**Ground.** the residuals' order 2

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_paces.py, `check_lights_index_to_first_order`

**Far-regime witness.** x = 0.4: e^0.8 = 2.23 against 5.0 and 1.8; x = 0.5: the quadratic form's 1 / (1 - 2 x) diverges where e^1 = 2.72, the truncation's horizon (S.3)

## L51. The mass defect's first order

**Place.** S.38 (b); ALGEBRA.md, The mass defect is the form's fall at a kept count

**Statement.** M sin(N omega_0) = M sin omega_0 - M omega_0 x cos omega_0 + O(x^2) with N = e^(-x).

**Ground.** the residual's order 2

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_mass_defects_first_order`

**Far-regime witness.** x = 1 at [2, 3]: 0.304 against the first order's 0.185

## L52. The preferred-frame parameter of a diagonal metric

**Place.** S.35; Universe24_Paper.tex 10.3

**Statement.** 4 gamma + 4 + alpha_1 = 0, alpha_1 = -4 (1 + gamma) = -8 at gamma = 1; the drag (4 gamma + 4 + alpha_1) / 8 of Lense-Thirring's is 0; a covariant boost would give g_0i = gamma_L^2 v (N^2 - h^2) = -4 U v to first order.

**Ground.** exact arithmetic; the cross term's residual order 3

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_preferred_frame_parameter`

## L53. The staggered clock's redshift

**Place.** S.36 (v)

**Statement.** omega / omega_0 = N sqrt(3 / (4 - N^4)) = N (1 - 2 U / 3 + O(U^2)), a redshift 5 / 3 of general relativity's; sqrt(3 / (4 - 0.9^4)) = 0.9472; P_0 (4 - nu) = N^2 (4 - nu P_a) for all nu forces P_0 = N^2 and P_a = 1.

**Ground.** the residual's order 2, the forcing exact

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_staggered_clocks_redshift`

## L54. The frozen content

**Place.** S.41 (3); ALGEBRA.md, The paces compose; row 4 of The conventions and the units

**Statement.** p_i = p_0^2 / Gamma rounds to 0 where Gamma e^(-2 U) < 1 / 2, U > (1 / 2) ln(2 Gamma), the frozen content (Gamma / 2) ln(2 Gamma), 4.70 Gamma, 28,206 at Gamma = 6,000 with p_0 rounded before squaring (paces.frozen_content) against the formula's 28,178.

**Ground.** the inequality exact, the numbers by the derivation script

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_frozen_content`

## L55. The bounds from the photon and the dispersion

**Place.** S.27; S.24; Universe24_Paper.tex 10.1 and 10.2

**Statement.** One interval is omega_0 x 1.288 x 10^-21 s and one Link omega_0 x 6.69 x 10^-13 m; a photon of 1.4 PeV gives sin omega_0 <= 3.65 x 10^-10 (3.44 x 10^-10 on an axis), den > 1.5 x 10^19 and gamma_K - 1 < 6.7 x 10^-20; MAGIC's 3.8 x 10^-16 gives k < 6.7 x 10^-8 per Link, the Link below 1.3 x 10^-26 m on an axis and 2.1 x 10^-26 m on the mean, omega_e < 2.0 x 10^-14 (3.1 x 10^-14) and gamma_K - 1 < 2.0 x 10^-28.

**Ground.** every number recomputed from the constants

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_bounds_from_the_photon_and_the_dispersion`

## L56. The bending of light and Shapiro's delay

**Place.** S.20; the paper's Eq. (15); ALGEBRA.md, The rows against nature (b), (c)

**Statement.** The delay along a straight path is 2 sqrt 3 mu [arsinh(x_2 / b) + arsinh(x_1 / b)], 2 sqrt 3 mu ln(4 x_1 x_2 / b^2) far away; the bending's transverse integral is integral b dl / (b^2 + l^2)^(3 / 2) = 2 / b, so with n - 1 = 2 U the turn is 4 U_b, twice the Newtonian 2 U_b.

**Ground.** the antiderivative at its limits exact, the quadratures against the closed forms, the logarithm's remainder of order 2

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_bending_and_shapiros_integrals`

## L57. The rest rotation at a content to first order

**Place.** S.63's input; S.15

**Statement.** omega_0(U) = omega_0 - omega_0 f(omega_0) U + O(U^2).

**Ground.** the residual's order 2 at [2, 3] with the composed clock

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_paces.py, `check_the_slow_limits_rest_rotation`

**Far-regime witness.** U = 0.5 at [2, 3]: 0.500 exact against the first order's 0.394

## L58. Bell's correlation under the declared credit

**Place.** S.10; S.51; ALGEBRA.md, The pair family and Bell's gate; Universe24_Paper.tex 9.3 and 9.4

**Statement.** The four sums' squares add to M_1^2 + M_2^2 (Lagrange's identity); E(a, b) = cos 2a cos 2b + rho sin 2a sin 2b with rho = 2 M_1 M_2 / (M_1^2 + M_2^2); P(A+) = (M_1^2 c_a^2 + M_2^2 s_a^2) / (M_1^2 + M_2^2) independent of b; equal parts give cos 2(a - b); at (1, 0), (1, 1), (12, 5), (5, 12): 119 / 169, -119 / 169, 120 / 169, 120 / 169, S = 478 / 169 = 2.8284 below 2 sqrt 2, and S = (238 + 240 rho) / 169 at unequal parts.

**Ground.** exact rationals at random angles and parts, the integer settings exact

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_credit.py, `check_bells_correlation_under_the_declared_credit`

## L59. The two local credits and the sawtooth

**Place.** S.10; S.51b; Universe24_Paper.tex 9.4; ALGEBRA.md (h)

**Statement.** A credit by the shares gives E = (1 / 2) cos 2(a - b) and S = sqrt 2 at the ideal angles; a credit by the sign of the larger port gives the sawtooth E = 1 - 4 |a - b| / pi, whose sum at four settings ordered a < b < a' < b' within a quarter turn is exactly 2, Bell's bound, at the ideal and at the file's integer settings alike.

**Ground.** the product-to-sum identity exact, the means by the discrete average over 64 phases (exact for the shares), the sawtooth's measure exact

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_credit.py, `check_the_local_credits_and_the_sawtooth`

## L60. The contrast credit

**Place.** S.10's check

**Statement.** <cos x sgn cos(x - 2 delta)> = (2 / pi) cos 2 delta, so the contrast credit gives E = cos 2(a - b) exactly at one side's efficiency 2 / pi; the symmetric |cos| reading gives E(pi / 8) = 0.88 and S = 3.52.

**Ground.** the integral in closed form against a quadrature, the symmetric numbers by quadrature

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_credit.py, `check_the_contrast_credit`

## L61. The GHZ correlation under the declared credit

**Place.** S.40; ALGEBRA.md, The GHZ gate; Universe24_Paper.tex 9.4

**Statement.** With the patterns A (p, p, q, q), B (p, q, p, q), C (p, -q, -q, -p) the + ports' sum is cos(a + b + c), a - port -sin(a + b + c); the eight shares sum to 4, E_3 = cos 2(a + b + c), every pairwise E is 0 and every marginal 1 / 2; Mermin's M = -4 exactly at the integer settings (1, 0) and (1, 1).

**Ground.** exact Gaussian rationals at random angles

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_credit.py, `check_the_ghz_correlation`

## L62. The instruments' rational angles and the turn's three shears

**Place.** ALGEBRA.md, The integer-exact constructions (3), row 9; S.61 row 9

**Statement.** sin theta = 2 p q / (p^2 + q^2) and cos theta = (p^2 - q^2) / (p^2 + q^2) exactly on the circle; R(theta) = S_x S_y S_x with t = tan(theta / 2) and sin theta = 2 t / (1 + t^2), an identity of 2 x 2 matrices.

**Ground.** exact fractions at random pairs

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_credit.py, `check_the_instruments_rational_angles_and_the_three_shears`

## L63. The units of one quantum

**Place.** rows 12, 13, 17 and 18 of The conventions and the units; S.49 (4), (5); S.26 (a)

**Statement.** (W_c sin omega_0)^2 = 9 T^2 (den^2 - num^2), the count wall; A^2 = count T den / (2 laid sqrt(den^2 - num^2)) gives 2 A^2 sin omega = (count / laid) T; one quantum's share 6 den A^2 sin^2 omega = W_c sin omega; the Wronskian |W| = A^2 sin omega = T / 2 for a charged circular quantum (0 for a real record, S.49 (4) since d7e97674), so one quantum writes 1 / (2 E_s) and |q_p| = |q_e|; |W| / (count T) = 1 / (2 sin omega_0) = 0.6708 for a record laid by share at [2, 3] and 1 / 2 for a record of count 1.

**Ground.** exact rationals in the squares, rule3's isqrt

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_credit.py, `check_the_units_of_one_quantum`

## L64. The region's reading factor

**Place.** S.8; Universe24_Paper.tex 5.3

**Statement.** |SUM_(y = 0)^(n - 1) e^(2 pi i y / Lambda)| = sin(pi n / Lambda) / sin(pi / Lambda), the factor sin(pi n / Lambda) / (n sin(pi / Lambda)), 0.91 at n = 4, Lambda = 16, and 0 at Lambda = n.

**Ground.** the geometric sum's modulus exact at rational unit angles; the number recomputed

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_credit.py, `check_the_regions_reading_factor`

## L65. The Zeno formula

**Place.** S.59

**Statement.** P(e at T_pi) = (1 - cos^n(pi / n)) / 2: 1, 0.500, 0.375, 0.235, 0.133, 0.072 and 0.037 at n = 1, 2, 4, 8, 16, 32 and 64.

**Ground.** the recurrence and the numbers recomputed

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_credit.py, `check_the_zeno_formula`

## L66. Theorem 4, the stable body

**Place.** the paper's Theorem 4; ALGEBRA.md, The functional and the dilation; S.48

**Statement.** F(R) = K / R^2 - SUM_r sigma_r W_r R^(-s_r): F'(1) = 0 is the virial 2 K = SUM sigma s W and F''(1) = SUM sigma s (2 - s) W under it; s (2 - s) = +1, 0, -3 at s = 1, 2, 3; Pekar's F = a / R^2 - c / R has one critical point 2 a / c, a minimum for every mass.

**Ground.** the Taylor remainder's order 3 with K set by the virial, F'' exact, Pekar's exact

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_stable_body_theorem`

**Note.** The theorem's domain is power-law kernels; the Yukawa kernel's integrated exponent is row `A01`.

## L67. The hollow's barrier

**Place.** ALGEBRA.md 7.2 (b); S.13; Universe24_Paper.tex 7.2

**Statement.** F = a / R^2 - b / R^3 - c / R has F' = (c R^2 - 2 a R + 3 b) / R^4, the roots R_+- = (a +- sqrt(a^2 - 3 b c)) / c, none where 3 b c > a^2; F'' = 2 (a R - 3 b) / R^5 at a root, the wide point the minimum and the narrow the saddle.

**Ground.** exact rationals at (5, 1, 3) and the derivative identity at random points

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_hollows_barrier`

## L68. The functional's gradient is the fixed point's equation

**Place.** S.13; ALGEBRA.md, The functional (Proof); the paper's Eq. (12)

**Statement.** dF / dphi_i = (2 num / (3 den)) (-Delta^2 phi)_i - (8 g / Gamma) Phi_i phi_i with Phi the wells of the record's own counts, so dF / dphi = -2 (M(Phi) phi - 2 cos omega_0 phi) and dF / dphi = 2 lambda phi on the sphere is the fixed point's equation with lambda = 2 cos omega_0 - 2 cos omega_b.

**Ground.** exact rationals on a periodic chain of five with two symmetric kernels, the derivative by exact interpolation of the quartic

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_functionals_gradient_is_the_fixed_points_equation`

## L69. The adiabatic invariant and the count's drift

**Place.** S.14; the paper's Eq. (13); invariant_check.py

**Statement.** At fixed omega D_t = a_t^2 - a_(t+1) a_(t-1) = a_t^2 + a_(t-1)^2 - 2 cos omega a_t a_(t-1) is conserved and equals A^2 sin^2 omega; the orbits are ellipses of area pi D / sin omega, so D / sin omega = A^2 sin omega is the adiabatic invariant, the slowly varying ansatz with the midpoint phase satisfying the line to the first order in the ramp; the recurrence stepped 20,000 intervals from 0.841 to 0.600 keeps D / sin omega within 4 x 10^-5 while D falls by a quarter; N(t_2) / N(t_1) = [sin omega_b(t_2) / sin omega_b(t_1)] [p_i^2(t_1) / p_i^2(t_2)].

**Ground.** exact rationals; the ansatz by the residual's order 2; the stepped recurrence a witness

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_adiabatic_invariant_and_the_drift`

**Note.** The ansatz's phase as printed is row `F04`.

## L70. The body's click share

**Place.** S.14, the body's click; Universe24_Paper.tex 5.4 and 7.4

**Statement.** sin omega_j - sin omega_i = 2 cos((omega_i + omega_j) / 2) sin((omega_j - omega_i) / 2) = sin(omega_j - omega_i) [1 - omega_i omega_j / 2 + O(omega^4)]: one photon's share T sin omega_L at the line, to a relative omega_0^2 / 2 at nature's gap.

**Ground.** the identity exact at rational half-angles, the expansion by the residual's order 5

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_bodys_click_share`

**Far-regime witness.** omega = 1 and 2: the exact share difference 0.068 against the first order's 0

## L71. Schroedinger's equation as the slow limit

**Place.** S.63; Universe24_Paper.tex 3.3

**Statement.** Re[e^(-i omega_0 (t + 1)) (psi + psi' + psi'' / 2) + e^(-i omega_0 (t - 1)) (psi - psi' + psi'' / 2)] = Re[e^(-i omega_0 t) (2 cos omega_0 psi - 2 i sin omega_0 psi' + cos omega_0 psi'')] exactly; (num / (3 den)) 6 = 2 cos omega_0; i psi' = -Delta psi / (2 m*) with m* = 3 den sin omega_0 / num = 3 tan omega_0; the three conditions, the band's k^4 term of relative size k^2 / 12 and psi'' against 2 sin omega_0 psi' of relative size (omega - omega_0) / (2 tan omega_0).

**Ground.** the expansion exact in Gaussian rationals; the orders by the residual

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_schroedingers_slow_limit`

## L72. The resonance's exponents

**Place.** S.16; ALGEBRA.md, The law's own formulas A (6)

**Statement.** zeta' = -i (Delta / 2) zeta - i mu e^(i theta) conj(zeta) has the exponents +- sqrt(mu^2 - Delta^2 / 4): growth for |Delta| < 2 mu, a full width epsilon / sin omega_b with mu = epsilon / (4 sin omega_b).

**Ground.** the real 2 x 2 generator squares to (mu^2 - Delta^2 / 4) times the identity, exact

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_resonances_exponents`

## L73. The resonant growth rate

**Place.** S.16's check

**Statement.** The recurrence stepped 20,000 intervals at 2 cos omega_b = 1.4317 and epsilon = 0.013 grows at 0.004653 to 0.004656 per interval, the first-order mu = epsilon / (4 sin omega_b) = 0.004654 to four digits.

**Ground.** the slowly varying method a hand derivation; the stepped recurrence a witness

**Kind and verdict.** C, witness only.

**Check.** tools/derivations/proofs_bodies.py, `check_the_resonant_growth_witness`

## L74. The cross current of two standing records

**Place.** S.17; Universe24_Paper.tex 7.5

**Statement.** num (a_t b_(t-1) - a_(t-1) b_t) for A cos(omega_1 t + alpha), B cos(omega_2 t + beta) is a sum of cosines of (omega_1 - omega_2) t and (omega_1 + omega_2) t with constant parts only when omega_1 = omega_2.

**Ground.** exact at rational angles

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_cross_current_of_two_standing_records`

**Note.** The finite window's mean is row `A06`.

## L75. The integer budget's walk

**Place.** ALGEBRA.md, The integer budget of a derived row; Universe24_Paper.tex 9.2

**Statement.** The response kernel G_m - G_(m-1) = cos(omega (m + 1 / 2)) / cos(omega / 2) with G_m = sin(omega (m + 1)) / sin omega, of mean square 1 / (1 + cos omega), so the walk is sqrt(n / (12 (1 + cos omega_k))): 0.224 sqrt n at [2, 3]'s rest, 0.209 at light's k = pi / 4, 0.289 at a band's centre; G_(t-1) = t at the uniform mode and (-1)^t t at the checkerboard; the zone means 0.354, 0.259, 0.226 and 0.302 sqrt n.

**Ground.** the kernel identity exact at rational half-angles, the double roots exact in integers, the numbers recomputed, the zone means by quadrature

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_budgets_walk`

**Note.** The walk is statistics under the model of independent uniform remainders, named so in the law.

## L76. The guide's lay

**Place.** S.48; row 18 of The conventions and the units

**Statement.** |C| = 3 den s / (2 num sin k) for the source at one Node of a width-one guide; the two trains' form (3 / 2) (SUM_t A_t^2) sin Omega / sin k from B = 3 A / (2 sin k), D = B^2 sin^2 Omega and v_g = sin k / (3 sin Omega); one quantum is laid at SUM_t A_t^2 = (2 / 3) T sin k, the increments' own squares summing to half of it.

**Ground.** exact at rational angles; the half by the discrete sum over a period

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_guides_lay`

## L77. What a body writes into the holder of the sign

**Place.** S.42; Universe24_Paper.tex 7.4

**Statement.** z_(t+1) + z_(t-1) = 2 cos omega_t z_t with any real omega_t keeps W = Im(conj(z_t) z_(t-1)) exactly; a steady rotation has W_i = phi_i^2 sin omega_b constant and g_ij = 0, writing nothing travelling; the quanta radiated through a far sphere are (3 sqrt 3 / 4 pi) s^2 sin^2 Omega / T, the coefficient 0.4135.

**Ground.** exact Gaussian rationals, the number recomputed; the retarded multipole expansion a hand derivation

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_what_a_body_writes_into_the_holder_of_the_sign`

## L78. The two-mode line under the rotation

**Place.** S.43; Universe24_Paper.tex 7.4

**Statement.** (a) a uniform time turn is a gauge, z_t = e^(-i Phi_t) u_t with u on the plain line for any theta_t; (b) a constant turn shifts both senses by theta; (c) K_jm antisymmetric, K_mm = 0; (d) the transfer generator squares to -(g^2 + Delta^2 / 4), P(t) = [g^2 / (g^2 + Delta^2 / 4)] sin^2(sqrt(g^2 + Delta^2 / 4) t), the full width 4 Omega_R; (e) SUM_i x_i [phi_j (M phi_m) - (M phi_j) phi_m]_i = -K_jm on an open chain, so K_jm = 2 w (cos omega_j - cos omega_m) d_jm = -4 w sin((omega_j + omega_m) / 2) sin((omega_j - omega_m) / 2) d_jm and Omega_R = theta_L omega_L |d_jm| / 2 for a small line.

**Ground.** exact Gaussian rationals and Fractions, the small line by the residual's order 2

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_two_mode_line_under_the_rotation`

## L79. The two forces between quanta

**Place.** S.44; Universe24_Paper.tex 10.1

**Statement.** F_e / F_g = k E_g / (2 E_s sin^2 omega_s) at one family and (F_e / F_g)_e / (F_e / F_g)_p = sin^2 omega_p / sin^2 omega_e = (m_p / m_e)^2 between two; nature's 4.17 x 10^42 and 1.24 x 10^36, the ratio 3.37 x 10^6 = 1836.15^2.

**Ground.** exact rationals, the numbers recomputed

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_two_forces_between_quanta`

## L80. The nuclear holder's threshold

**Place.** S.45 (a), (b)

**Statement.** 2 mu g^2 / kappa >= 1.6798 is W >= 1.17 Gamma kappa / omega_p^3 (1.6798 x 4 pi / 18 = 1.173): 591 at [2, 3] (502 at the exact inertia), doubling under the pair hypothesis to 1,183 and 1,004 (1.6798 x 4 pi / 9 = 2.345); lambda_p = 0.210 fm and the binding fractions 3.1 x 10^-2, 4.9 x 10^-3, 1.6 x 10^-3 at 0.84, 2.13, 3.75 fm.

**Ground.** the numbers recomputed

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_nuclear_holders_threshold`

**Note.** The threshold 1.6798 of Yukawa's well is a known number of that equation, taken as input.

## L81. The atom's self-term

**Place.** S.46 (c); Universe24_Paper.tex 7.3

**Statement.** epsilon = x^2 - 2 x + (1.25 / Z) x; Hartree's fixed point is the minimum of E_tot = x^2 - 2 x + (0.625 / Z) x at x = 1 - 0.3125 / Z, E_tot = -(1 - 0.3125 / Z)^2 and epsilon = E_tot + 0.625 (1 - 0.3125 / Z) / Z: (-0.473, -0.043, 1.45), (-0.712, -0.448, 1.19), (-0.938, -0.878, 1.03), (-0.979, -0.959, 1.01) at Z = 1, 2, 10, 30; the Rydberg ratios 1 - 1.25 / Z, 95.9 percent at Z = 30.

**Ground.** exact rationals

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_atoms_self_term`

## L82. The equivalence principle between families

**Place.** S.47; Universe24_Paper.tex 8 (i)

**Statement.** 2 nu / (1 + nu) = 1 - tan^2(omega_s / 2) exactly with nu = cos omega_s; two families fall apart by tan^2(omega_n / 2) - tan^2(omega_p / 2), (omega_n^2 - omega_p^2) / 4 at small gaps; 0.0139 x 9,297 / 4 = 32.3, eta = 32.3 omega_e^2 below 4.4 x 10^-18.

**Ground.** the identity exact at rational points, the small-gap difference by the residual's order 4, the numbers recomputed

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_equivalence_principle_between_families`

## L83. The quanta a cloud gives to settle

**Place.** ALGEBRA.md, The surplus leaves

**Statement.** f = (4 f / (1 + 4 f^2))^3 in a box (23 percent leaving), f = 4 f^(1 / 3) / (4 f^(2 / 3) + 1) on a chain (17.1 percent), f = 16 f / (4 f + 1)^2 on a plane with the root f = 3 / 4 exactly (25.0 percent); the brackets 1 - (4 / 5)^d, 20, 36 and 49 percent.

**Ground.** the plane's root exact, the others by bisection

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_quanta_a_cloud_gives_to_settle`

## L84. The total share is non-negative

**Place.** S.6; ALGEBRA.md, The share's sign and the credit's floor (a), at the vacuum's coefficients since 3a334eeb, the bound in a well the hands' to state; Universe24_Paper.tex 4.4

**Statement.** At the vacuum's coefficients SUM_i e_i = 3 den (|n|^2 + |b|^2) - num n . S_6 b >= 3 (den - |num|) (|n|^2 + |b|^2) >= 0 on a closed or periodic board for |num| <= den, with equality at the static uniform level of light and the even board's checkerboard with before = -now; a Node's share has the minimum 3 den before_i^2 - num^2 s^2 / (12 den), negative iff |s| > 6 (den / num) |before_i|.

**Ground.** Gershgorin's theorem on the form's symmetric integer matrix [[3 den I, -(num / 2) S_6], [-(num / 2) S_6^T, 3 den I]], every row's disc in [3 den - 3 |num|, 3 den + 3 |num|] since every row carries six neighbours with multiplicity, exact on four boards; the random boards witnesses; the equality cases and the minimum exact

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_the_total_share_is_non_negative`

## L85. Theorem 2, what the acts can form

**Place.** ALGEBRA.md, The four acts; the paper's Theorem 2; S.48

**Statement.** Every fixed finite composition of the four acts is an affine form of the levels plus a term bounded by a constant of the composition, so no product of two levels is written by the step on the whole lattice.

**Ground.** a hand proof by the growth of a floor of an affine form against a product's

**Kind and verdict.** C, none.

**Check.** none.

**Note.** No numerical witness is printed; a machine check would be a proof assistant's.

## L86. The bilinears of one pair

**Place.** ALGEBRA.md at b254f4d2, The conserved form (The bilinears of one pair)

**Statement.** Two solutions u, v of one line conserve Omega(u, v) = SUM_i (u_now v_before - v_now u_before) / p_i^2 and E polarised over them, exactly in the rationals at fixed paces, in integers to the carried remainders, as W = Omega(re, im); n lines carry n^2 such numbers, the dimension declaring the record's; a line of another pair conserves none with them; three planes of one pair carry u(3), the trace the record's W, eight traceless numbers no holder reads.

**Ground.** D M symmetric at the law's weights 1 / p_i^2: Omega and the polarised form exact in Fractions on four boards at random clocks and Link factors read the same from both ends, six lines (the zero line among them), the 36 bilinears, five pairs with the symmetric ones forced; the integer step's walk of Omega the remainders' term SUM_i (epsilon_u v_now - epsilon_v u_now) / p_i^2 exactly; a line stepped by [3, 4] beside the record's pair moving every cross number; the Hermitian 3 x 3 of three planes conserved, its trace the weighted W; the contrast, the clock's weight 1 / p_0^2 moving the cross Omega

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_lines_2026_10_17.py, `check_the_bilinears_of_one_pair`

**Note.** The law's own witness run of 2026-10-17 (a periodic chain of 40 at [2, 3], 200 rational and 2,000 integer intervals) is not repeated; the identity is checked exactly at random witnesses, the integer clause as the exact walk.

## L87. The Gram determinant of the planes

**Place.** ALGEBRA.md at b254f4d2, The count is the record's share (The Gram determinant of the planes)

**Statement.** For n planes of one pair K_ab, E polarised over the planes a and b, is their Gram matrix, positive definite for a gapped family: its trace the record's share, its rank the independent planes' number, det K 0 exactly when they are dependent. Identical planes step bit-identically, det K = 0 exactly in integers; a plane laid as two others' sum departs by its remainders, its eigenvalue 10^-3 to 10^-5 of the trace. Neither the step nor the credit reads it.

**Ground.** the real polarisation of E over the planes' two lines at the vacuum's coefficients, anchored to rule3.conserved_form; Sylvester's minors and the rank by elimination in Fractions on four boards and five pairs, the dependent lays (identical planes, a sum, a rational combination) before and after the step, and the massless contrast (light's static uniform plane, E = 0, det K = 0 with independent planes); rule3.step on the chain of 221 at [4000, 6000], two bit-identical planes and the plane laid as two overlapping packets' sum, the smallest eigenvalue over the trace after five intervals at the lay amplitudes 30 and 100 (6.5 x 10^-4 and 7.4 x 10^-5)

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_lines_2026_10_17.py, `check_the_gram_determinant_of_the_planes`

**Note.** The credit's count of a coincident pair as two quanta and the inflow matrix at the close are the engine's readings of 2026-10-17 (the chain of 221), not checked here; the eigenvalue's range 10^-3 to 10^-5 is recomputed on the law's step at the amplitudes named and falls inside it.

## L88. The charge of a plane is bounded by its share

**Place.** ALGEBRA.md at b254f4d2, The paces (The charge of a plane is bounded by its share); The third and the colours, closed as absent

**Statement.** A plane at fixed paces has |W| <= I / 2, I the invariant: D M is self-adjoint in the D metric, form and Wronskian split over its eigenmodes, each mode a 2 x 2 Cauchy-Schwarz of determinant sin^2 omega_k; exact at fixed paces (the vacuum by Parseval, a static well by its modes), a reading under moving paces, in integers to the remainders' walk. A record has |W| <= count x T / 2, with the count read at the record's own rotation (in a well the vacuum's unit reads the factor sin omega_0 / sin omega_b, the two units of a quantum, The click writes on the lattice), equality iff every plane is circular and of one sense: |q_p| = |q_e| is the one-sense case (16,384 = T / 2 per quantum on the engine), the fractions (2, 2, -1) / 3 give 3 / 5 of the unit at count 1 or count 5 / 3 at the unit.

**Ground.** Lagrange's identity W_k^2 sin^2 omega_k = q_k(re) q_k(im) - <re, im>_k^2 per mode with the arithmetic mean's bound, exact in Fractions: the one-Node line at the Pythagorean pairs [3, 5] to [24, 25], its rotation from rule3.coefficients, circular planes of either sense built at rational angles (equality), elliptical, real and zero planes (strict), records of several planes (equality iff all circular and of one sense); the Fourier modes of the vacuum's boxes of extents 1, 2 and 4 (Parseval) and the two-Node well at Gamma = 3, [5, 9], the clocks 1 and 2, with rational D-orthogonal modes, the split and the per-mode identity exact and the summed bound in floats; the fractions' arithmetic and T / 2 at T = 32,768

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_lines_2026_10_17.py, `check_the_charge_of_a_plane_is_bounded_by_its_share`

**Note.** The integer clause, the Wronskian's walk by the remainders, is row `L25` and not restated; the reading under moving paces is a reading, not a check; 16,384 = T / 2 per quantum is the engine's reading of 2026-10-17 on the one-Node ring (the one-sense lay, W per piece 16,384 at every read; the charged lay 9,713 = 0.5928 T / 2), not this check's arithmetic; the record clause |W| <= count x T / 2 is covered as several planes at one Node (the records of two planes, equality iff both circular and of one sense) plus the arithmetic 16,384 = 32,768 / 2.

## L89. The Ports' three readings

**Place.** ALGEBRA.md at b254f4d2, The click is the meeting (The Ports' three readings)

**Statement.** Under the 48 a Node's six arrivals split into their sum, the quadrupole pair and the three signed differences along the axes; Rule3's numerator SUM_a R_a (arr(+a) + arr(-a)) is even in every axis, so the step reads the sum alone at uniform paces, the sum and the pair where the Link paces differ by axis, the differences never (2,000 trials per pair on the law's step); the click's inflow is the sum over the region's front Ports and the lattice momentum the differences; the quadrupole pair no line reads. A traceless symmetric tensor splits into its diagonal pair and its three off-diagonal parts, and the law's tensions and paces are diagonal: the static read's + and no x.

**Ground.** the 48 signed permutations on the six Ports in integers, the three pieces orthogonal, invariant under the 48 and rebuilding the arrivals, 1 + 2 + 3 = 6; rule3.numerator and rule3.step at random arrivals, 2,000 trials per pair at eight pairs, at uniform and at by-axis Link paces, the pair's read (R_x - R_y) delta; the inflow and the momentum density from rule3.link_current at random neighbours; the tensor's count 5 = 2 + 3 and the read's one coefficient per axis

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_lines_2026_10_17.py, `check_the_ports_three_readings`

**Note.** The engine's 300 trials and the two slits' 159 click lines and 1,120 readings are runs of the engine, not repeated here.

## L90. The staggering is exact

**Place.** ALGEBRA.md at b254f4d2, A family's declaration (The staggering is exact)

**Statement.** b = (-1)^(x + y + z) a signs every arrival against its Node, so b obeys the line with R_a -> -R_a and S unchanged, [-num, den]'s line at the vacuum's S = 0; with the odd Nodes' levels negated and remainders complemented, w - 1 - r, the floor commutes exactly, so in the vacuum a record of [1, 2] and one of [-1, 2] are one record read on the two sublattices with opposite signs, bit for bit (4 x 4 x 4, 60 intervals; 18 of 64 Nodes break without the complement, 63 of 64 in a content with S / w = 0.02). The space-time (-1)^(t + x + y + z) maps a pair's line to itself with S -> -S, exact in the rationals, not in integers (no remainder alternates its sign with the interval).

**Ground.** the signed line exact in Fractions at random clocks and Link factors on boxes of even extents, four pairs; rule3.coefficients at [num, den] and [-num, den], equal but for the sign of R at the vacuum and apart by 24 num (p_a^2 - p_0^2) in S in a content; rule3.step on the 4 x 4 x 4 box over 60 intervals at random levels and remainders, with the complement (0 Nodes broken), without it (27 of 64 at the first interval) and in the content c = 20 of Gamma = 6,000 with S / w = 0.0199 (64 of 64); the space-time sign in Fractions, and in integers the Nodes departing by the second interval with and without the complement

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_lines_2026_10_17.py, `check_the_staggering_is_exact`

**Note.** The counts 18 of 64 and 63 of 64 are the law's lay's; this lay's counts stand in the computed object, 27 and 64.

## L91. The quarter turn of a two-plane record

**Place.** ALGEBRA.md at b254f4d2, The direction (The quarter turn of a two-plane record)

**Statement.** A two-plane record whose axis vector turns as a vector needs its planes mixed: the quarter turn about z is diag(1, i) up to the common phase e^(-i pi / 4), plane 2's (re, im) -> (-im, re), exact to the bit with the negated line's remainder complemented (40 intervals); the turn about x needs a halving, exact in the rationals alone (210 of 500 Node-lines off). Up to a common phase 8 lifts are exact in integers (one axis's dihedral group), 16 need a halving, none 1 / sqrt 2.

**Ground.** the 48 unit quaternions of the cube's rotations as Pauli matrices in Gaussian integers over the scales 1, sqrt 2 and 2, each turning the three Pauli axes as a signed permutation of determinant 1 exactly, classified by its entries' moduli and ratios (8, 16, 0); rule3.step on the 4 x 4 x 2 box over 40 intervals at [2, 3] and [4000, 6000] with the z turn's Node map and the complement, bit for bit; the x turn on the 5 x 5 x 5 box in Fractions, exact, its half-integer Node-lines counted (228 of 500)

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_lines_2026_10_17.py, `check_the_quarter_turn_of_a_two_plane_record`

**Note.** Whether the common phase is a ray's freedom or a line of the lay is the law's open decision, not a check; the 210 of 500 is the law's lay's count, this lay's 228 in the computed object.

## L92. The exact bands: the integer rotations

**Place.** ALGEBRA.md at b254f4d2, A family's declaration (The exact bands)

**Statement.** Three lines of [-1, 2] laid as the third's phases (1000, -500, -500) turn by the 3-cycle (L_0, L_1, L_2) -> (L_2, L_0, L_1) with remainder 0, three lines of [1, 2] by the signed 3-cycle (-L_2, L_0, L_1), a plane of [0, 1] by (re, im) -> (-im, re), to the bit (30 intervals); the lines' 3-cycle is the uniform lay's identity and no act of the step (a random lay differs from it at 374 of 375 Node-lines), the cube's C3 commuting with the step on every lay: one group of order 3, two actions, the lines' cycle a Cartan element of SU(3) and not its centre.

**Ground.** rule3.step at the vacuum on the 2 x 2 x 2 box over 30 intervals for the three exact pairs, the lines laid as s(t - m) on the period's phases, the remainders 0 throughout; a random lay of three lines on the 5 x 5 x 5 box against the cycle (375 of 375 Node-lines off); the body diagonal's C3 on the 5 x 5 x 5 box against rule3.step with random levels and remainders at [-1, 2] and [2, 3], its order 3; the cycle's matrix in integers, P^3 = I, det P = 1, the characteristic polynomial x^3 - 1, no scalar

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_lines_2026_10_17.py, `check_the_exact_bands_integer_rotations`

**Note.** The three exact rotations themselves are row `L07`; the 374 of 375 is the law's lay's count, this lay's 375 in the computed object.

## L93. The nucleon is a compact body of its family: the Hartree-Fock identity

**Place.** ALGEBRA.md at b254f4d2, The hypotheses under their own names (The nucleon is a compact body of its family)

**Statement.** Helium in the mean field without exchange -2.8617 against -2.9037 hartree (1.4 percent), the Hartree-Fock number itself: in the 1s^2 singlet the opposite-spin exchange vanishes and the self-exchange cancels the self-Hartree that No record reads its own write of the sign removes, so the 1.4 percent is the correlation alone, the two-position amplitude no board of one-position records holds.

**Ground.** the two-electron determinant's expectation of a symmetric interaction summed over positions and spins exactly in Fractions at random orbitals and kernels, twelve cases: J / N^2 for the singlet of one orbital, equal to (2 J - K) / N^2 with K = J and to the mean field in which each electron reads the other's cloud alone, apart from the self-read mean field 2 J / N^2 by J / N^2; two orbitals of parallel spin carrying -K_ab and of opposite spin none, the same-orbital parallel pair the zero state; the percent from the two printed energies

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_lines_2026_10_17.py, `check_the_hartree_fock_identity_of_the_closed_shell`

**Note.** The two energies are the quantum-chemical calculations' numbers, taken as input; the percent is recomputed, 1.45.

## R01. The computed pair's limits

**Place.** Universe24_Paper.tex, Introduction

**Statement.** Replacing [2, 3] by [999, 1000] moves c_m / c from 0.867 to 0.9997 and gamma_K, beta_K from 1.5, 1.25 to 1.001, 1.0005, approaching 1 as the gap closes.

**Ground.** the numbers recomputed

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_computed_pairs_limits`

**Far-regime witness.** num / den = 0.01: c_m / c = 0.125, gamma_K = 100, beta_K = 50.5

## R02. The clock's rate is exact in 2 sin(omega / 2)

**Place.** Universe24_Paper.tex 3.4; S.31

**Statement.** 2 sin(omega(U) / 2) = N 2 sin(omega_0 / 2) exactly for every N, from 1 - cos omega(U) = (1 - nu) N^2; in omega up to the finite-rotation correction omega_0^2 / 12, 5.9 percent at the computed pair.

**Ground.** exact rationals in the half-sines squared

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_clocks_rate_is_exact_in_the_half_sine`

**Far-regime witness.** U = 4.7, the frozen content: omega(U) / omega_0 = 0.0091 against N = 0.0091, exact in the half sine

## R03. The cut region's uniform mode

**Place.** Universe24_Paper.tex 5.3

**Statement.** A region with its outer Links cut and its inner Links open has its uniform mode at cos omega_0 = num / den exactly whatever the region's size, (S_i + SUM over the open Ports of R_ij) / w = 2 num / den.

**Ground.** exact rationals on chains of one to five Nodes

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_cut_regions_uniform_mode`

## R04. The folded axis carries the band

**Place.** Universe24_Paper.tex 9.1

**Statement.** A record uniform along the folded axis has the three-dimensional band at k_z = 0, so the flat lattice carries the file's band exactly.

**Ground.** exact at rational angles on the folded chain by rule3.numerator

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_folded_axis_carries_the_band`

## R05. Friedmann's dust equations and the redshift

**Place.** Universe24_Paper.tex 7.5; S.29

**Statement.** a'' = -(4 pi G_K / 3) rho a with rho a^3 constant integrates exactly to a'^2 / a^2 = (8 pi G_K / 3) rho - kappa / a^2, q_0 = Omega_m / 2 positive for every rho > 0; 1 + z = (1 + beta) / sqrt(1 - beta^2) = 1 + beta + beta^2 / 2 + O(beta^3), the classical 1 / (1 - beta) differing at the second order.

**Ground.** the invariant's derivative exact and a fourth-order integration to 10^-12; the series by the residual's order 3

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_friedmanns_dust_equations_and_the_redshift`

**Far-regime witness.** beta = 0.9: 4.36 exact against the second order's 2.31 and the classical 10

## R06. The content to first order in the clock

**Place.** Universe24_Paper.tex 8 (a); ALGEBRA.md, The ledger of exactness

**Statement.** p_0 / Gamma = (1 - 1 / Gamma)^l = e^(-U) exactly with U = -l ln(1 - 1 / Gamma), which is l / Gamma to the first order in 1 / Gamma, U - l / Gamma = l / (2 Gamma^2) + ...

**Ground.** the residual's order 2 in 1 / Gamma

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_contents_first_order_in_the_clock`

**Far-regime witness.** Gamma = 2: U = 0.693 l against l / 2

## R07. The two readings of beta

**Place.** Universe24_Paper.tex 8 (b)

**Statement.** P / E with p = E v and v / c_local agree as the gap closes: on the exact band P / E = c k / omega(k) and v / c = (d omega / dk) / c read 0.203 and 0.151 at [2, 3] and k = 0.3, and agree to 10^-6 at [999999, 1000000].

**Ground.** the readings recomputed

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_two_readings_of_beta`

**Far-regime witness.** [999, 1000] at k = 0.3: 0.971 against 0.960

## R08. gamma_K - 1 is half the gap squared

**Place.** Universe24_Paper.tex 10.1; S.27

**Statement.** den / num - 1 = 1 / cos omega_0 - 1 = omega_0^2 / 2 + 5 omega_0^4 / 24 + O(omega_0^6), below 6.7 x 10^-20 at omega_e < 3.7 x 10^-10.

**Ground.** the residual's order 4 and its coefficient

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_gamma_k_minus_one_is_half_the_gap_squared`

**Far-regime witness.** [1, 2], omega_0 = pi / 3: 1 against omega_0^2 / 2 = 0.548

## R09. The lattice's half-sine variable

**Place.** S.31

**Statement.** s(k)^2 = (2 sin(k / 2))^2 = k^2 [1 - k^2 / 12 + O(k^4)], every mode scaling by N in s(omega) exactly at long wavelength and to the lattice's k^2 / 12 at finite k.

**Ground.** the residual's order 6

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_lattices_half_sine_variable`

**Far-regime witness.** k = pi: s^2 = 4 against the truncation's 1.75

## R10. The ports are exactly orthogonal

**Place.** Universe24_Paper.tex 9.3; S.51; Universe24_Paper.tex 10.1

**Statement.** e(+) = (p, q) and e(-) = (-q, p) are exactly orthogonal with equal norms, so each side's marginal is one half for any setting; in nature cos omega differs from 1 by under 10^-18 for every family (6.8 x 10^-20 at omega_e = 3.7 x 10^-10).

**Ground.** exact integers, the number recomputed

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_ports_are_exactly_orthogonal`

## R11. The fringe's spacing and the near-field minima

**Place.** S.23

**Statement.** The far-field spacing is lambda L / d = 16 Links; the near-field minima solve sqrt(L^2 + (y - 18)^2) - sqrt(L^2 + (y - 30)^2) = +- 4 at y = 15.28 and 32.72, the rows 15 and 33.

**Ground.** the roots by bisection

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_fringes_near_field_minima`

## R12. Newton's constant and alpha_law's numbers

**Place.** S.25, Eq. (20); S.26 (b)

**Statement.** G_clock = 1 / (4 pi Gamma E_g) from U = 3 s / (4 pi r Gamma E_g) against G M / (c^2 r) with c^2 = 1 / 3; alpha_law = (3 sqrt 3 / 8 pi) k / (Gamma E_s) = 0.20675 k / (Gamma E_s), 137.036 x 0.20675 = 28.33, 28 giving 1 / 135.43 and 29 giving 1 / 140.27.

**Ground.** the algebra exact with pi cancelled, the numbers recomputed

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_newtons_constant_and_alpha_laws_numbers`

## R13. The rule's total at the width

**Place.** ALGEBRA.md, The bound

**Statement.** 6 A |R| + A |S| + w (A + 1) is 4.4 x 10^15 at [2, 3] and 8.8 x 10^18 at [4000, 6000] with Gamma = 10^4 and A = 2^20, 0.96 of 2^63 (0.955 exactly).

**Ground.** exact integers by rule3.rule_total

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_rules_total_at_the_width`

## R14. A body stands, in integers

**Place.** ALGEBRA.md, The integer budget of a derived row; Universe24_Paper.tex 9.2

**Statement.** A = sqrt(T c_i / (2 sin omega_s)) is 852 at T = 2^15 and 3,407 at 2^19 for c_i = 33 at [2, 3]; the deviation 2 sqrt 8 sigma sqrt n / A is 4.7 percent per mode at n = 10^3; at the two slits over 130 intervals the walk is 2.4 levels per mode, 3.0 per Node over the plane's zone and 4.0 over a cube's.

**Ground.** the numbers recomputed

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_a_body_stands_in_integers`

## R15. The one-sided mixed term's dispersion

**Place.** S.36 (i)

**Statement.** C_a (2 i sin k_a) (1 - e^(i omega)) = 2 C_a sin k_a sin omega + 4 i C_a sin k_a sin^2(omega / 2), by 1 - e^(i omega) = -2 i sin(omega / 2) e^(i omega / 2): a g_0a part beside an imaginary part.

**Ground.** exact Gaussian rationals at rational half-angles

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_one_sided_mixed_terms_dispersion`

## F01. The law's weighted form change as printed

**Place.** ALGEBRA.md at 3a334eeb, The mass defect is the form's fall at a kept count (The surplus leaves)

**Statement.** As printed: the line a_next = M(t) a_now - a_before with the paces changing in time changes the weighted total form E = <a_now, D a_now> + <a_before, D a_before> - <a_next, D a_before>, D = diag(1 / p_i^2), by exactly E(t + 1) - E(t) = <a_next, D (M(t) - M(t + 1)) a_now>, 0 at fixed paces. As printed E carries <a_before, D a_before> once too often: Theorem 3's form over w, SUM_i [w (now_i^2 + before_i^2) - S_i now_i before_i] / p_i^2 - SUM_ij (R_ij / p_i^2) now_i before_j, is <a_now, D a_now> - <a_next, D a_before> by the line itself, and the printed E changes by the claimed term plus <a_now, D a_now> - <a_before, D a_before>, not 0 at fixed paces; the two-level weighted form satisfies the identity exactly at any paces (row `L21`) and the plain form at uniform paces, as the paragraph also says.

**Ground.** exact fractions on three boards, two reads with different contents and tensions, the weights of the paces at t + 1

**Kind and verdict.** A, finding.

**Check.** tools/derivations/proofs_form.py, `check_the_laws_weighted_form_change_as_printed`

**Note.** At 915c6a7b the paragraph printed the plain form D = |a_now|^2 - <a_next, a_before> without the transpose, exact at uniform paces only, this inventory's finding then; 3a334eeb (fill 17, push eight) moved to the weighted form and carries one Node term too many: the line to read E = <a_now, D a_now> - <a_next, D a_before>, Theorem 3's E over w, with which the identity is exact at any paces.

**Finding.** See docs/ERRATA.md.

## F02. Row 14's unweighted sum as printed

**Place.** row 14 of The conventions and the units

**Statement.** As printed: SUM_i a_i SUM_j R_ij b_j = SUM_i b_i SUM_j R_ij a_j by R's symmetry from both ends. R_ij carries the reading Node's p_i^2 and is not symmetric where the paces differ; the equality holds with the share's weight 1 / p_i^2 inside (row `L36`).

**Ground.** exact fractions

**Kind and verdict.** A, finding.

**Check.** tools/derivations/proofs_booking.py, `check_row_14s_unweighted_sum_as_printed`

**Note.** A wording finding: the row's equality is the weighted one, the share's own.

**Finding.** See docs/ERRATA.md.

## F03. The quadratic reading at Gamma = 2,400 as printed

**Place.** ALGEBRA.md, The paces compose (R169 (h))

**Statement.** As printed: the quadratic reading is within Gamma U^3 / 6 of a unit of the composition, 1.02 units at c = 600 and Gamma = 6,000, 0.41 at Gamma = 2,400 and 2.0 at 12,000. The exact power gives 0.44 at 2,400 (0.436), the 1.02 and 2.0 recomputed.

**Ground.** exact fractions by rule3.clock_pace

**Kind and verdict.** A, finding.

**Check.** tools/derivations/proofs_paces.py, `check_the_quadratic_reading_at_gamma_2400_as_printed`

**Note.** A numeric finding on one printed digit: 0.41 against 0.44.

**Finding.** See docs/ERRATA.md.

## F04. S.14's plain phase fails at the first order

**Place.** S.14 (since d7e97674)

**Statement.** The ansatz a_t = C cos(theta_t + phi) / sqrt(sin omega_t) with the midpoint phase theta_t = SUM_(s <= t) (omega_s + omega_(s+1)) / 2 satisfies the line to the second order in omega_(t+1) - omega_t, and the phase SUM_(s <= t) omega_s fails at the first order: the residual with the plain phase, the increment omega_(t+1), is of the first order in the ramp and with the midpoint increment of the second.

**Ground.** the residual's order at two step sizes, for both phases

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_bodies.py, `check_s14s_plain_phase_fails_at_the_first_order`

**Note.** At 2836519e S.14 printed the plain phase with the first order, this inventory's finding then; d7e97674 (R165's midpoint phase) prints the midpoint phase and the plain phase's failure, which the check confirms.

## F05. The plain monopole is the uniform-pace case

**Place.** S.42, inputs (since 9775922e)

**Statement.** The weighted sum SUM_i W_i / p_i^2 over a body is exactly conserved for a static self-level, the plain sum its uniform-pace case: at the two-Node witness the plain sum moves at the paces squared (1, 2) and stands with the weighted one at the paces squared (1, 1).

**Ground.** exact Gaussian rationals at the two-Node witness at two pairs of paces

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_audit.py, `check_the_plain_monopole_is_the_uniform_pace_case`

**Note.** At 2836519e S.42 printed the plain sum as the conserved one, the audit's item 3 and this inventory's finding then; the hands' line of 5977935062 (3) is printed since 9775922e, and the check holds it.

## F06. The momentum identity at non-uniform paces as printed

**Place.** Universe24_Paper.tex 4.3

**Statement.** As printed: at non-uniform static paces Eq. (7) gains the Link-wise differences of the coefficients, [R_b(i) - R_b(i - b)] times the stress readings. Computed, the clause's residual on a 5-box is of the size of the identity's terms; the exact identity is w [P_a(t + 1) - P_a(t)] = -Y_i Delta_a now_i + now_i Delta_a Y_i, whose extra terms against Eq. (7) are, times the levels' products, the differences [S_(i + a) - S_i] along the momentum's axis and, for every Link direction b, [R_b(i + a) - R_b(i +- e_b)], along the axis for b = a and between the axis neighbour and the transverse neighbours for b != a, the transverse part of the size of the axial one; the share's identity gains nothing (row `L30`).

**Ground.** exact fractions on a periodic 5-box with per-Node coefficients

**Kind and verdict.** A, finding.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_momentum_identity_at_non_uniform_paces_as_printed`

**Note.** A finding of the far-regime sweep on the paper's Section 4.3 sentence.

**Finding.** See docs/ERRATA.md.

## F07. S.42 (b)'s Fourier weight for every body

**Place.** S.42 (b)

**Statement.** As printed: a body smooth over many Links sources zone-edge light only by its Fourier weight there, below e^-100 for every body of the paper. A Gaussian body of rms width R has the weight e^(-pi^2 R^2 / 2) at k = pi, below e^-100 for R above 4.5 Links; the paper's bodies on the chain are 2.1 to 3.4 Links wide (e^-22 to e^-57), and an exponential tail's weight falls as a power of k.

**Ground.** the weights computed

**Kind and verdict.** B, finding.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_fourier_weight_of_a_smooth_body`

**Note.** A finding of the far-regime sweep on 'for every body of the paper'.

**Finding.** See docs/ERRATA.md.

## F08. Light's stress at the band's top as printed

**Place.** Universe24_Paper.tex 4.3 (since 5f5df82b)

**Statement.** As printed: on light's wave the written stress over the written energy, (num / 3 den) sin^2 k / sin^2 omega, is '3 / 5 at the band's top along an axis'. At the band's top along an axis, k = pi with cos omega = 1 / 3 for light, sin k = 0 and the ratio is 0; 3 / 5 is the ratio at k = pi / 2, where sin k = 1 and the group speed along the axis is largest.

**Ground.** exact rationals at k = pi / 2 and k = pi

**Kind and verdict.** A, finding.

**Check.** tools/derivations/proofs_far_regime.py, `check_lights_stress_at_the_band_top_as_printed`

**Note.** A finding of the sweep at d7e97674 on the number's place: 3 / 5 is right at k = pi / 2, and 'the band's top' names k = pi, where the written stress is 0.

**Finding.** See docs/ERRATA.md.

## R16. The massless row's two double roots and the staggered mode

**Place.** ALGEBRA.md at 3a334eeb, No write from outside Rule3 wakes either double root of the massless row (the generator; the shelved ion's remedy)

**Statement.** cos omega_k = (1 / 3) SUM_a cos k_a has two double roots, the uniform mode at k = 0, omega = 0, and the staggered mode (-1)^(x + y + z + t) at k = (pi, pi, pi), omega = pi; each carries neither form nor share, 3 den (a^2 + b^2) - den a SUM_j b_j = 0 for a = b uniform and for the staggered pair b = -a; each is an exact mode of a board periodic on three axes of even extent; in either a level stands and a velocity impulse is a slope that grows as tau + 1 for ever; a gapped row has no double root.

**Ground.** the band's line and its omega-derivative at the two roots exact in rationals; the two modes stepped by the vacuum's massless line a_next = (1 / 3) SUM_j a_j - a_before on the periodic boxes (2, 2, 2) and (4, 2, 2) in exact fractions, the share and the form 0 at every Node, the impulse's slope over ten intervals, the odd box (3, 2, 2) the contrast

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_massless_rows_two_double_roots`

**Far-regime witness.** the staggered root, the band's top omega = pi at k = (pi, pi, pi): the mode steps exactly with 0 share and 0 form on the even boxes and is no mode of the odd box

## R17. Light's written stress over its written energy at finite k

**Place.** Universe24_Paper.tex 4.3 (since 5f5df82b)

**Statement.** On light's wave the written stress over the written energy is (num / 3 den) sin^2 k / sin^2 omega, 1 at long wavelength (nature's T_xx = T_00), 0.90 at k = pi / 4 and 3 / 5 where sin k = 1, at k = pi / 2; at the band's top k = pi it is 0.

**Ground.** the long-wavelength limit by the residual's order 2, 0.897 at pi / 4, the values at k = pi / 2 and pi exact in rationals

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_lights_written_stress_over_energy_at_finite_k`

**Far-regime witness.** k = pi, the band's top along an axis: the ratio 0 (sin k = 0) against the long-wavelength 1; 3 / 5 is the ratio at k = pi / 2 (row `F08`)

## R18. The division act's stop is the integer square root

**Place.** Universe24_Paper.tex, the one root (since 5f5df82b); ALGEBRA.md, The six verbs

**Statement.** The integer square root at a lay is the stop of the division act x <- (x + n div x) div 2, the law's fixed point, where the iterate stops falling (at n = 3 the iterates 2, 1, 2 alternate and the stop is 1).

**Ground.** exact integers, the stop from x_0 = n against isqrt(n) for every n to 5,000

**Kind and verdict.** A, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_division_acts_stop`

## R19. The shears' exact angle at small angles

**Place.** Universe24_Paper.tex 5.5 (since d7e97674); S.61 row 9

**Statement.** The exact angle of the three shears is 2 arctan(L p_0 / (2 Gamma^2)), which is (L / Gamma)(p_0 / Gamma) at small angles.

**Ground.** the remainder 2 arctan(x / 2) - x of the order 3 with the coefficient -1 / 12, and the exact angle's sine x / (1 + x^2 / 4) at rational x, the Pythagorean point of tan(theta / 2) = x / 2

**Kind and verdict.** B, holds.

**Check.** tools/derivations/proofs_far_regime.py, `check_the_shears_exact_angle_at_small_angles`

**Far-regime witness.** x = L p_0 / Gamma^2 = 2, the largest turn the law allows (tan(theta / 2) = 1): the exact angle pi / 2 = 1.571 against the small-angle 2

## N01. S.4, the cube's group of 48

**Place.** S.4

**Statement.** The 48 signed permutations of the three axes commute with the step, R_a being even in the axis's sign; D, F and W are a scalar, a Link quantity and a scalar; the time reversal carries the step to its inverse; a boost is not in the group.

**Ground.** the engine's acts and the cube's group

**Kind and verdict.** D, none.

**Check.** none.

**Note.** The integer identity of the complement is row `L23`; the commutation act by act is the engine's, tests/test_the_node.py.

## N02. S.37, confinement

**Place.** S.37

**Statement.** A record of dimension 3 clicks whole or not at all; the partons' three fractions; Bjorken scaling exact in the declared row.

**Ground.** the click's one form under the dimension-3 hypothesis

**Kind and verdict.** D, none.

**Check.** none.

## N03. S.38 (c), the binding bound

**Place.** S.38 (c), (d)

**Statement.** defect / rest <= 0.76 C W / (Gamma E) per quantum at one Node from Watson's 3 G(0) = 0.7582.

**Ground.** the lattice Green's function's value, the derivation script greens_function.py

**Kind and verdict.** C, none.

**Check.** none.

**Note.** The number 0.7582 is the output of tools/derivations/greens_function.py three_g, held by the documents gate.

## N04. S.39 (a), the gapped kernel

**Place.** S.39 (a)

**Statement.** G_kappa(1) = G_0(1) (1 - 0.92 kappa + O(kappa^2)), the ratio 0.9546 at R = 20.

**Ground.** the exact lattice Yukawa integral

**Kind and verdict.** C, none.

**Check.** none.

**Note.** A quadrature of the three-dimensional lattice integral; no script here.

## N05. S.41 (1), (2), the prediction and the gravity of light

**Place.** S.41

**Statement.** The strontium clock's visibility 0.989 at one metre and one second; a light packet's active mass 1 x E / c^2 against general relativity's 2.

**Ground.** arithmetic on nature's constants and the one write

**Kind and verdict.** C, none.

**Check.** none.

## N06. S.45 (b) to (e), the nuclear well's binding, capture and size law

**Place.** S.45

**Statement.** b = (lambda_s / R)^2 / 2 by the virial of the slow limit; the capture at the beat; Bethe and Peierls's shape; R* proportional to 1 / n.

**Ground.** hand derivations of the slow limit's equation

**Kind and verdict.** C, none.

**Check.** none.

**Note.** The threshold's numbers are row `L80`.

## N07. S.46 (a), (b), (d), the atom's levels and the holders the electron does not read

**Place.** S.46

**Statement.** E_n = -m* (Z alpha)^2 / (6 n^2) and a_0 = sqrt 3 / (m* Z alpha); the orbital g = 1; the finite-size shift and the muonic radii.

**Ground.** the slow limit's hydrogen-like problem, standard mathematics

**Kind and verdict.** C, none.

**Check.** none.

## N08. S.60, the atom under the two lines

**Place.** S.60

**Statement.** The pinned nucleus reproduces -1 / (2 n^2) to 10^-4 on a grid of 2,000 points; helium -2.8617 Ha; positronium -0.110 Ha.

**Ground.** a radial grid solve and a two-record Hartree iteration

**Kind and verdict.** C, none.

**Check.** none.

**Note.** Computed by the paper's hand; no script in the tree.

## N09. S.61, the engine's derivation ledger

**Place.** S.61

**Statement.** Every act of the engine with its derivation or its stated reason.

**Ground.** the engine's acts

**Kind and verdict.** D, none.

**Check.** none.

**Note.** The engine's tests show the acts; the rows of the ledger with an identity are carried above (rows 1, 2, 4, 7, 8, 9, 11, 12, 17).

## N10. S.62, the implementation's versions of the click's write

**Place.** S.62

**Statement.** The paper reports no reading of the implementation but the two slits'.

**Ground.** a statement of the paper's scope

**Kind and verdict.** D, none.

**Check.** none.

## N11. S.49, S.52 to S.56, the words, the bodies, the masses, the lattice's properties, the conservation picture, the findings

**Place.** S.49, S.52, S.53, S.54, S.55, S.56

**Statement.** Definitions and the tables of the paper's statements with their marks.

**Ground.** no quantity beyond the rows above

**Kind and verdict.** D, none.

**Check.** none.

**Note.** m* c_m^2 = omega_0 (S.53) is row `L46`; the conservation table's theorems are rows `L17`, `L25`, `L27`.

## N12. S.19's orbit step and S.21's orbit on the exact band

**Place.** S.19; ALGEBRA.md, The push on a moving record

**Statement.** The periapsis on the exact band at [2, 3] is 13 to 15 percent above 6 pi U_p in a coordinate plane and 8 to 10 percent in the (111) plane, vanishing as tan^2 omega_0.

**Ground.** the rays of the exact band on the orbit, computed twice by the hands

**Kind and verdict.** C, none.

**Check.** none.

**Note.** A computed row of the paper; the geometric-optics integration is not reproduced here.

## N13. The lattice constants

**Place.** ALGEBRA.md, The lattice constants; S.38's check

**Statement.** 3 G(0) = 0.7582 at the Node and 0.2582, 0.1287, 0.0826, 0.0609, 0.0483 at 1 to 5 Links; 4 pi r G(r) toward 1.

**Ground.** the lattice Green's function by quadrature, tools/derivations/greens_function.py

**Kind and verdict.** C, none.

**Check.** none.

**Note.** Held by the documents gate (3) through tools/numbers.json.

## N14. The draw's share to within s_k / 2^63

**Place.** ALGEBRA.md at 3a334eeb, The click's algebraic definition (the draw)

**Statement.** P(region k) = s_k / SUM s to within s_k / 2^63 over the generator's full period whatever the seed, exact where SUM s divides 2^63.

**Ground.** the engine's generator (the full period of the linear congruential generator); tests/test_the_draw.py

**Kind and verdict.** D, none.

**Check.** none.

**Note.** A statement of the engine's draw; the engine's tests show it.
