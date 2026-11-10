# AGREE_P — Study 7 physicists: ONE-P1 × ONE-P2 (U4 Einstein + Quantum map; U6/U7 physics columns; U5 physics side)
- Built by ONE-P1, 11:05–11:3x UTC 2026-11-10 (`date -u` stamps in s7/ONE-P1_NOTES.md).
- Sources:
  - P1 = s7/ONE-P1_FINDINGS.md v1.2 + s7/ONE-P1_NOTES.md; runs in s7/ONE-P1_work/ (pinned 10:12:12).
  - P2 = s7/ONE-P2_FINDINGS.md v2 (saved 11:00:41) + s7/ONE-P2_NOTES.md; runs in s7/ONE-P2_work/ (pinned 10:12:23).
  - Independence ended at the manager's relay (~11:03). Neither twin had read the other before its draft.
- Rows:
  - (I) P1's 25 prepared rows;
  - (II) every row of P2's Table A (quantum), Table B (Einstein) and Table C (symmetries), plus R14 and R15;
  - (III) the manager's six items + the new "one cone" row;
  - (IV) ONE merged U5 list.
- Columns: claim / cell | P1 | P2 | verdict | evidence. The verdict column holds P1's PROPOSAL; P2 marks every row AGREE / REFINE /
  DISAGREE (by ~11:50). Every DISAGREE gets a decisive check in BOTH codes on pinned copies.
- Labels as in both drafts: THEOREM / NUMERIC / DERIVED / OPEN / FAILS (P2 also PRED = the board's own deviation from QM).

## (I) P1's prepared rows
| # | claim / cell | P1 | P2 | verdict (P1 proposal) → P2 mark | evidence |
|---|---|---|---|---|---|
| 1 | Clock dictionary: board eigenvalue (cos w = λ/D) = event phase = OFFICIAL click sign cycles | NUMERIC, 4.3e-7 worst (27 lapse values × 2 species, T = 4000) | NUMERIC (B1-GRAV D1: sign cycles = lapse to 2.9e-5); Born-side dictionary N10: 0/10,080 mismatches | AGREE (two codes, different gears) → **P2: AGREE** | P1 n1_clocks.json; P2 N10, §9 |
| 2 | Redshift (half-angle law) read in clicks; clock comparison | NUMERIC 5.3e-7 (prescribed static lapse, MECHANISM) | NUMERIC clock redshift D2/D2b (1.05024 vs 1.05090; 2.0e-4) | AGREE → **P2: AGREE** | n1_clocks.json; B1-GRAV D2b |
| 3 | EP in clicks: species ratio | NUMERIC sin-ratio spread 8.2e-7; raw w ratio 9.1e-4 = O(w0²) → 0 | NUMERIC 4.8e-5 [D1]; WEP deficit 1 − tan²(w0/2) [CT] | AGREE → **P2: AGREE** | n1; D1; CLICK_TAXONOMY §2.1 |
| 4 | γ = 1 (Shapiro ratio GR/1911) on the package, read in clicks | NUMERIC 2.038 in clicks (event 2.039; lattice 2.064) through a static slab; absolute delay −8 % vs the carrier estimate (registered FAIL, packet spectrum) | NUMERIC 2.109 / 2.104 [B1-GRAV D2c], excess second order in U; D2 2.61 recorded FAIL (spurious left-movers) | AGREE: γ = 1 reproduced on the package in two independent setups; both excesses over 2 are O(U) → **P2: AGREE** | n3_shapiro.json; D2c |
| 5 | B1-GRAV's D2 = 2.61 failure lies outside the lapse block and the click dictionary | DERIVED from row 4 (pinned lapse section identical to live, drift check 11:00) | "spurious left-movers" (B1-GRAV's own diagnosis) | AGREE (consistent diagnoses) → **P2: AGREE** | n3; NOTES_gravity |
| 6 | EP FAILS for L0 while (d) stands. THEOREM: gcd(Q, Q−1) = 1 ⇒ no fine-resolution lapse common to L0 ports (Q) and field gears (Q−1) | THEOREM + NUMERIC (package build_lapse refuses L0: ValueError −1025/16) | FAILS while uncoupled; "no exact universal lapse on today's weights (TH)" [B1-GRAV L0-EP]; closure: R (EP to 1/Q, today's board bit for bit at F = 0) or W (weight Q−1: EP exact, one cone c_Q, today's board only in vacuum) | AGREE (same theorem, three codes incl. B1-GRAV); remedy → row M2 → **P2: AGREE; REFINE the remedy: the lapse must act on L0's port-DIFFERENCE potential. B1-GRAV's R/W as built split M(0) (clock factor) from the transport and give L0's massless mode w0 ≈ √(2U) [P2 N12, exact Bloch]; see M2** | n2 (i); P2 R3a; B1-GRAV L0-EP |
| 7 | Zero-mean closed board: N > 1 in every underdense region. ANY zero-mean rescaling destabilises every massless gear (cos w = 1 at k = 0; no threshold on a periodic board) | DERIVED (variational) + NUMERIC: growth = exact V+ top eigenvalue to 1e-6 (d = 20, 2); my registered "d = 2 bounded" FAILED | §3b: any factor > 1 (U < 0) unstable (headroom 1/(3Q)); D7: on wave gears the zero mode drifts ∝ St², GR light dies at t* ≈ 250; F4b/c: a non-conserved stress drives U < 0 → explosion | AGREE (complementary: P1 the mechanism and rate, P2 the dynamic drift) → **P2: AGREE** | n2, n2b; P2 §3b, §11 |
| 8 | Remedy: "gravity only slows" = the k = 0 LAPSE datum with max N = 1 (U ≥ 0), a SECOND k = 0 prepare/ number beside Ē; GR's time normalisation spent on causality; a rescaling-only link is stable iff contractive (+++) | THEOREM (norm ≤ 6 max f) + NUMERIC (arm A = control) | §3b: EP-invisible, stability-mandatory, a preferred time gauge (board time = proper time of the least-bound clock); needs OD2 accumulators and an exactly conserved stress [F4c(i) bounded 700 updates] | AGREE → **P2: AGREE** | n2 A; P2 §3b; ONE-M1/M2 (Schur bound) |
| 9 | Hands: s_y ≠ s_z boards have no unsigned improper symmetry; all 24 hold with χ (2O sign character, kernel 2T): P broken, P∘χ exact; s_y = s_z: full O_h | NUMERIC exhaustive (signed relabelings × all 48 of O_h) | NUMERIC [N5, N5c]: same split, s = ±χ, dynamics F∘P = P∘F 5/5 at Q = 1 and 7 | AGREE (two codes; + ONE-M1 Theorem S) → **P2: AGREE (two codes; P2 N5d = P1 chi_map: diag χ is an exact isomorphism (s_x, s_y, s_z) ↔ (s_x, −s_y, −s_z))** | h1_oh.json; P2 N5 |
| 10 | The handed reversor: T∘P∘χ exact and non-involutive; R² = a central clock-sense flip (for 4 of 8 solutions exactly the global negation) ⇒ "Kramers-type" | NUMERIC exact: X Fⁿ X Fⁿ = Z (18/18 per solution), Z = X² = all signs −1 | NUMERIC [N5f]: R Fⁿ R⁻¹ Fⁿ = id 4/4 (n = 1, 6; Q = 1, 7), non-involutive; R(vac) = vac | AGREE: the identities are equivalent (Z central ⇒ R F R⁻¹ = F⁻¹) → **P2: AGREE** | cpt_l0_v3.json; P2 N5f |
| 11 | Handed boards are gapped (max\|λ\| = 2+2√3, w ≥ 0.4255) and every Bloch level is a Kramers doublet at every k; +++ has the λ = 6 A1 scalar and singlets | NUMERIC (oa_zone, kd_bloch) | NUMERIC [N7b] gapped; light exists exactly on the unsigned boards | AGREE (+ ONE-M1/M2) → **P2: AGREE** | oa_zone.json, kd_bloch.json; N7b |
| 12 | Handed L0 is stable for link factors up to 6/(2+2√3) = 1.098; +++ unstable at any f > 1 | NUMERIC (rates to 3e-4) | (not run; consistent with N7b and §3b) | AGREE (P1 single code; ONE-M1/M2: dynamic links bounded 5000/5000 on the handed class) → **P2: AGREE (P1 code + the math pair; consistent with the 2+2√3 gap, N7b)** | n4_handed_*.json |
| 13 | χ commutes with the internal right-Q8 ⇒ L0's hands do not reach the weak SU(2) (or matter) without a frame–internal coupling = NEW LAW | DERIVED (Q8 ⊂ 2T) | DERIVED: "chirality is a third grading; which side a gauge field acts on separates spin from internal, not L from R" [§6.3]; "does not reach matter while (d)" | AGREE → **P2: AGREE (NUMERIC support: P2 N5c, χ constant on the right-Q8 cosets)** | P1 §5; P2 §6 |
| 14 | Owner decision: the handed class for L0 | REVISED: ADOPT for L0, with costs (row M1) | leans HANDED (agree_positions_P2 item 1); nature's hands must still come through matter's coupling | AGREE = the M1 JOINT LINE → **P2: AGREE → joint line in M1** | M1 |
| 15 | F7 front as built = a C0 fibre at 1 site/update = √3c along an axis (the cone gap); the quantum correlations were shown for the TAXICAB cone | DERIVED from TC.7 timing | THEOREM TH-C0 (exact single-component C0 transport only on axis fibres) + reading of TC.7.json: S = 5/2 at round-spacelike t_B = 9, 10 | AGREE (P2's theorem is the stronger statement) → **P2: AGREE** | TC.7; P2 TH-C0 |
| 16 | A free point L0 front puts 35 % of its intensity before r/c on [100] (0 on [111]) at r = 12; a smooth front's ONSET is isotropic (~1 update) but not its amplitude pattern | NUMERIC (point) + registered smooth metric FAIL + diagnostic | TC.17 (round-cone front): E = 0 through the gap, max\|S\| ≤ 0.092; over-driven readers clip, S = 3.35–3.40 > 2√2 | AGREE (complementary) → **P2: AGREE** | f7_proxy*.json; TC.17 |
| 17 | Moving clocks tick slower in clicks by the SR factor (reunion on the torus) | NUMERIC: σ = 4 qualitative (registered FAIL). TD2 (σ = 12, L = 96, final): moving (comoving clicks) vs lattice w − k v_g +0.79 % (v = 0.60c) and +0.70 % (0.79c) PASS; moving/rest = 0.8020 vs √(1−v²/c²) = 0.7996 (+0.30 %) PASS at 0.6c; at 0.79c 0.5995 vs 0.6082 (−1.4 %, reported); rest vs w0 +0.68 %/+0.82 % (criterion 5e-3) FAIL; rewind exact | U5-P9 "twin test not run" | REFINE: P2's "not run" → partly run (P1 TD/TD2) → **P2: AGREE with P1's REFINE (P2's 'not run' → partly run: TD2 +0.3 % at 0.6c)** | td_clicks.json, td2_clicks.json |
| 18 | Compact U(1): the (g) conditions are not met (Newton III −0.50 over T = 60; no light in the verified regime; stiff: 0.86 c_Q off-cone) | package facts | same [EM-C5, C6, C6b ✗pkg] | AGREE → **P2: AGREE (+ P2 N13: the link gauge bands are gapless with long-wave speed 0.012 ≈ c_Q/48)** | NOTES_em §6 |
| 19 | Bell: timelike cos exact (S = 5/2, 60° grid); spacelike \|S\| ≤ 2 contradicts the 2015 loophole-free tests | FAILS vs experiment | PRED, contradicted by the 2015 tests if the board cone is the physical cone | REFINE wording: "PRED; FAILS against experiment" (same content) → **P2: AGREE with the wording REFINE** | TC.7; S5M:C1, F3 |
| 20 | Spin–statistics: no exchange statistics, no Pauli, HOM coincidence > 0 | FAILS | FAILS (structural: no configuration space) + HOM PRED contradicted | AGREE → **P2: AGREE** | S5M:B11 |
| 21 | Matter + E1 are exactly P, C, CP, T symmetric ⇒ weak vector-like, no CP violation | DERIVED (P = R*∘T⁻¹) | NUMERIC [N2] bit-exact 20/20; chirality algebra N1b/N1c | AGREE (P2's numeric is decisive) → **P2: AGREE** | N2; EM-T8 |
| 22 | Strong CP: θ = 0 | DERIVED: a required T-type reversor excludes T-odd force blocks | DERIVED: no F∧F term in Φ by construction | AGREE (two arguments) → **P2: AGREE** | — |
| 23 | No cosmological expansion (OD2 k = 0 mode static) | FAILS vs GR cosmology (law change needed) | same | AGREE → **P2: AGREE** | S6 H-(d) |
| 24 | Einstein–Cartan: a FIXED handed frame vacuum acts on fermions like the SME b_μ (CPT-odd) unless χ ↔ C on matter forces it CPT-even; universal frame coupling gives ONE screw for ALL fermions, unlike nature's weak-only hands | DERIVED (literature) | OPEN (H3): whether a signed frame link couples Γ = ± differently (U5-T10c) | REFINE: merge as one open test (U5 item 7) → **P2: AGREE (merged open test)** | P1 §5; P2 R14 |
| 25 | U6 summary: universal coupling removes γ and per-species constants and decides (d); the Bianchi role forces the conserved Noether stress; the lapse zero mode is fixed by causality (max N = 1) | DERIVED + NUMERIC rows 1–8 | Table C (same three columns), §3b | AGREE → **P2: AGREE** | P1 §3; P2 §4 |

## (II) P2's tables, row by row
### Table A (quantum; P2 leads)
| row | claim (P2's row, condensed) | P1 | P2 | verdict → P2 mark | evidence |
|---|---|---|---|---|---|
| A-R1 vacuum | shared phase from the uniform vacuum (TC.5); fixed point; R*/X/M′-fixed for odd Q; no Bell resource; P,C,T-fixed; **no zero-point fluctuations** (FAILS) | AGREE all cells; P1 had not listed zero-point: ADD as FAILS (structural) | as stated | AGREE → **P2: AGREE** | TC.5, T0.6, EM-T8 |
| A-R2 clock | remainder law P = \|K\|/D; C0 clocks exact; V = 1 in clicks; bijection; all-or-nothing records (TC.8); CRT; J-sign doubler; proper time = sign cycles | AGREE; P1 adds N1 (4.3e-7, 27 lapse values) | as stated | AGREE → **P2: AGREE** | TC.2, TC.8; N1 |
| A-R3a L0 light | no Born reader; O(1/A) superposition [N3]; no single-quantum fringes at A ≤ 3; exact rewind; unmarkable by a one-way read; V+ ⊕ V− by the 2π sign; statistics FAILS; round fronts only at large scale | AGREE; P1 adds: its massless mode is the A1 SCALAR (not the photon), zero headroom [OA], point fronts leak on axes [P7] | as stated | AGREE → **P2: AGREE** | N1a, N3; OA, P7 |
| A-R3b EM light | no photon detector; E1 linear to O(1/A); 2 polarizations; Kramers X; F7 front as EM light OPEN; compact: no light | AGREE | as stated | AGREE → **P2: AGREE** | EM-D4, EM-C6 |
| A-R4 matter | no \|ψ\|² detector of Dirac matter; O(1/A); Kramers, C, P exact; no configuration space (FAILS); spin ½; Γ chirality; no Pauli; P+ by data; Coulomb, magnetism; free fall from clicks D5 ✗pkg | AGREE. P1 REFINES its own E-a cell "D5 running" → P2's "D5 FAIL/inconclusive (+12 %)" | as stated | AGREE (P1 updates) → **P2: AGREE** | EM-T7/T10; N2; D5 |
| A-R5 EM force | q_click 1.017588; linear in the fields; AB OPEN; boson spin 1; Coulomb sign/magnitude; 1/r² short-window FAIL | AGREE | as stated | AGREE → **P2: AGREE** | EM-D1, D2b, D6 |
| A-R6 weak | non-abelian path-order witness; exact covariance; vector-like FAILS; W/Z masses need a Higgs (OPEN); YM only as the stiff limit; strong drive runs away | AGREE; P1 adds the link-cone/mass-gap row M7 | as stated | AGREE → **P2: AGREE** | gauge D3, G4–G6 |
| A-R7 strong | colour flow exact; 96-element subgroup; scalar quarks only; confinement FAILS/OPEN | AGREE | as stated | AGREE → **P2: AGREE** | gauge D2, G4 |
| A-R8 gravity | linear + β = 1; COW OPEN; reversors exact; NO gravity-mediated entanglement (PRED); spin 2, D4 hx = 0 exactly; field built from zero slope −1.0018, Gauss 1.0002 [D6] | AGREE; P1 REFINES its GW cell "D4 running" → P2's ✓pkg (front 0.583, hx = 0, 1/R within 10 % in D4b) | as stated | AGREE (P1 updates) → **P2: AGREE** | D4, D4b, D6 |
| A-R9 links | the choice is a link event; L0 bounded under unitary/contracting links, norm > 1 blows up; c2/c1 dynamic blow up; ZQ8 = 8 gears for local Q8 | AGREE; P1 adds: the handed class gives 9.8 % headroom [N4] | as stated | AGREE → **P2: AGREE** | M1 map, G9b; N4 |
| A-R10 choice click | Born exact (2 exits; n sequential); odd-Q PRED P(none) = 1/Q at the system Q [TC.18]; continuous readers lose the lock (TC.15 dev) → one-shot readers; QM-deviating conditional signature; back-action breaks exclusivity; round-cone front TC.17; HOM PRED | AGREE | as stated | AGREE → **P2: AGREE** | TC.2, 6, 10, 11, 13, 17, 18 |
| A-R11 seed | typicality OPEN; matter never created; exact bounce (R*); paired phases; matter = antimatter at the linear level ⇒ excess = DATA (≥ 2 species) | AGREE | as stated | AGREE → **P2: AGREE** | S6 |
| A-R12 arrow | H(record) bound; reversible law; collapse = conditioning; kinds = J-signs; two-headed footprint arrow | AGREE | as stated | AGREE → **P2: AGREE** | S5M:A7–A9; S6:B9 |
| A-R13 ONE CONE | exact Born weights need a C0 front, but C0 transport is axis-bound (TH-C0); F7 FAILS as built for the round cone; the tension vanishes only at A ≫ 1 | AGREE; with P1's P7 (point fronts lead on axes even for rounding light; smooth fronts fix the onset) | as stated | AGREE → **P2: AGREE** | TH-C0; TC.7; P7 |

### Table B (Einstein; P1 leads)
| row | claim (condensed) | P1 | P2 | verdict → P2 mark | evidence |
|---|---|---|---|---|---|
| B-R1 vacuum | k = 0 data force-free; lapse offset at the potential minimum (U ≥ 0); Birkhoff; constraints satisfied; boosts continuum-only; K7 | AGREE (P1 same: N2 + s6) | as stated | AGREE → **P2: AGREE** | S6 (d); N2 |
| B-R2 clock | universality 4.8e-5, β_eff 1.006; WEP deficit; clock redshift ✓, via light not yet; Board-Noether energy; time dilation studies only, reunion not run | AGREE except: reunion now partly run (P1 TD2: SR ratio to 0.3 % at 0.6c) | as stated | REFINE (P2's "not run" → partly run) → **P2: AGREE with the REFINE (reunion partly run, TD2)** | td2_clicks.json |
| B-R3a L0 | FAILS every Einstein column while (d); closure R (EP to 1/Q) / W (exact, weight Q−1); isospin Noether; isotropic at large scale; c(L0) = 1/√3 vs c_Q ⇒ one cone only to O(1/Q) | AGREE; P1's gcd theorem = B1-GRAV's TH; P1's remedy = W | as stated | AGREE → **P2: REFINE → AGREE: P1's remedy W must be the DIFFERENCE form [N12]; B1-GRAV's built W/R split gives the massless mode a mass** | n2 (i); L0-EP |
| B-R3b EM light | headroom light falls; A-gears not yet coupled; γ: studies + D2c 2.109; redshift via light FAIL/OPEN (best +0.9 %); EM/GW share c_Q (0.5774 / 0.583); exact Lorenz/Gauss; [100] fronts slower (dispersion) | AGREE; P1 adds N3 2.038 | as stated | AGREE → **P2: AGREE** | D2c, D8, EM-D4, D4 |
| B-R4 matter | antimatter falls alike +1.0000; free fall from clicks ✗; link/clock factors built in; matter feels all 10 (studies); continuity exact; Dirac stress OPEN; C4-only cubic covariance | AGREE (P1 updates D5) | as stated | AGREE → **P2: AGREE** | EM-D7, D5, G4 |
| B-R5 EM force | correctly non-universal; Noether/Lorenz/Gauss exact; Newton III −0.984 (charge-weighted); compact −0.50; magnetism | AGREE | as stated | AGREE → **P2: AGREE** | EM-D1b, C5, D5 |
| B-R6 weak / B-R7 strong | exact Gauss; B3 link-local | AGREE; P1 adds row M7 (their waves are slow and ungapped) | as stated | AGREE → **P2: AGREE** | G3 |
| B-R8 gravity | universality; "gravity only slows" (EP-invisible, stability-mandatory, preferred time gauge, a 2nd k = 0 datum; drift ∝ St² on wave gears; frozen on OD2); γ, redshift, Shapiro; GW ✓pkg partial (1/R +15.9 % at R = 21 in D4, within 10 % in D4b); dressed identities exact, G5b "C driven only by remainders" max\|C\| 135; DeWitt-metric reciprocity not built; no exact lattice diffeomorphisms; one cone; F1/F2/F3 | AGREE; P1 REFINES its G5 cell ("not shown") → P2's G5b (shown) | as stated | AGREE (P1 updates) → **P2: AGREE** | G5b, D4b, D7, F1–F4 |
| B-R9 links | link length = light time; γ = 1 in link words; h^0i on links; census 2112; c1 not adopted; B3 | AGREE | as stated | AGREE → **P2: AGREE** | S4M:G9 |
| B-R10 choice click | not coupled to gravity; Bob's wait in his own clock; designated one-way (no Noether partner); C0 fibres anisotropic; S = 5/2 at round-spacelike readouts | AGREE | as stated | AGREE → **P2: AGREE** | TC.7, TC.14 |
| B-R11 seed | P+ seed (c); closed board Q = 0, E = 0 or the datum; PT bounce; no Friedmann expansion | AGREE; P1 adds the lapse datum as a second k = 0 number (= P2 §3b) | as stated | AGREE → **P2: AGREE** | S6 |
| B-R12 arrow | records grow inside the cone; two-headed | AGREE | as stated | AGREE → **P2: AGREE** | S6:B9 |
| B-R13 one cone | C0 fibres anisotropic; exact single-quantum transport on the taxicab edge vs Einstein's one cone | AGREE | as stated | AGREE → **P2: AGREE** | TH-C0 |

### Table C (symmetries: LL / GC-Bianchi / UC / P / CP)
| row | claim (condensed) | P1 | P2 | verdict → P2 mark | evidence |
|---|---|---|---|---|---|
| C-R1 vacuum | discrete 2O frame; k = 0 data Ē + U0; P, C, X fix the vacuum | AGREE | as stated | AGREE → **P2: AGREE** | N2, EM-T8 |
| C-R2 clock | dilation continuum-only (P1: TD2 now in clicks); proper time invariant; all clocks slow alike; C-even rates | AGREE (+TD2) | as stated | AGREE → **P2: AGREE** | D1, EM-D7, TD2 |
| C-R3a L0 | LEFT 2O = frame (+++ ports = a curved 2O connection), c1 unstable; right-Q8 isospin exact; UC FAILS while uncoupled; unsigned mirror iff s_y = s_z, else P∘σ∘χ; V+ ⊕ V−; JR second reversal | AGREE (two codes for the mirror) | as stated | AGREE → **P2: AGREE** | N5, H1 |
| C-R3b EM light | transverse on the shared cone; E1 covariant only in the continuum (230 designated); compact exact; non-universal; P, C, T exact | AGREE | as stated | AGREE → **P2: AGREE** | EM-T3, G4, N2 |
| C-R4 matter | C4-only cubic covariance; continuity; UC built in; P = W0∘inversion exact; Γ: mass + Wilson flip chirality; NN pairing; C, CP, T ⇒ CPT | AGREE | as stated | AGREE → **P2: AGREE** | N1b, N1c, N2 |
| C-R5 EM | Gauss/Lorenz exact; P, C exact | AGREE | as stated | AGREE → **P2: AGREE** | — |
| C-R6 weak | vector-like FAILS; T_a(1+Γ)/2 broken by the Γ-odd Wilson term (NN); domain wall CONJECTURE; no CP violation | AGREE | as stated | AGREE → **P2: AGREE** | N1b; S4M:A13 |
| C-R7 strong | P-even; θ = 0 | AGREE (row 22) | as stated | AGREE → **P2: AGREE** | — |
| C-R8 gravity | c1 (Einstein–Cartan) not adopted; constraints dressed, not Noether; UC from ONE potential, "gravity only slows"; P-even, C-even | AGREE | as stated | AGREE → **P2: AGREE** | G4, G5–G7 |
| C-R9 links | c1 not adopted; c2 exact with 8 gears; rescaling links with N ≤ 1 keep \|λ\| ≤ 6 | AGREE; P1 adds the handed headroom (≤ 1.098) | as stated | AGREE → **P2: AGREE** | M1, N4 |
| C-R10 choice | FAILS as built (C0 fibres); designated one-way; not coupled to gravity; F7 has no reversor ("the block is chiral"); J not a symmetry of \|ψ\|² routers | AGREE | as stated | AGREE → **P2: AGREE** | NOTES_choice |
| C-R11 seed | Q = 0, E = 0 or datum; R*-fixed seeds bounce; S2* not P-fixed; excess only as DATA with ≥ 2 species | AGREE | as stated | AGREE → **P2: AGREE** | S6 |
| C-R12 arrow | T exact (M, X, R*); kinds are J-signs | AGREE | as stated | AGREE → **P2: AGREE** | S5M:A7 |
| C-R13 one cone | C0 fibre anisotropic; the F7 emission/gate pair is chiral | AGREE | as stated | AGREE → **P2: AGREE** | NOTES_choice |
| R14 handedness | nature (Wu, Goldhaber, K/B CP, T violation, CPT exact, θ) vs board: today FAILS P/CP/T, CONSISTENT with CPT and θ; signed boards: P broken, P∘χ exact, CPT-type reversor; click observables: χ-weighted O = Σ χ(g)·sgn(kind)·(x·n̂); a signed L0 has no long-wave sector | AGREE; P1 adds Kramers-type R² = Z [CPT v3] and doublets [KD]; the Einstein–Cartan b_μ caveat (row 24) | as stated | AGREE → **P2: AGREE (P1's additions accepted: Kramers-type R² = Z, KD doublets, the b_μ caveat)** | N5, N5f, N6b, N7b; H1, CPT, KD |
| R15 owner principle "the measurement acts BEFORE the click" | see row M3 | | | | |

## (III) The manager's items (must be settled explicitly)
| # | item | P1 | P2 | verdict (P1 proposal) → P2 mark | evidence |
|---|---|---|---|---|---|
| M1 | **THE HANDED CLASS FOR L0** (owner decision). **JOINT LINE (P1 11:10, from P2's proposal + the manager's note):** "OWNER: first decide what L0 is FOR. L0 cannot be the world's light: its massless mode is an A1 SCALAR (the photon is the T1 E1 A-wave). **HANDED class** (s_y ≠ s_z): ONE light (photon + graviton on c_Q); L0 = a heavy, neutral Kramers DARK sector with stable links and a CPT-type Kramers reversor; L0 is massive, so B1-GRAV's built site/hop (W) lapse split is then EXACTLY right. **+++**: an extra massless scalar species at zero headroom, so it needs fixed L0 links, the DIFFERENCE-form lapse at weight Q−1 [N12] and the max-N = 1 datum. Both are inside the tensor (AGENTS item 5: any preselected signs). BOTH TWINS LEAN HANDED." | **REVISED** (from "keep +++"). The +++ light is ONE massless A1 SCALAR at the stability edge: not the photon (A1 ≠ T1; the photon is the E1 A-wave with 2 transverse polarizations [EM-D4]); no fundamental massless scalar is seen in nature; it sits at \|λ\| = 6, so every dynamic or gravity link on L0 needs f ≤ 1 exactly. The handed class (s_y ≠ s_z) gives: a NEUTRAL, MASSIVE, KRAMERS species (doublets at every k [KD]); stable links (9.8 % headroom [N4]; local-Q8 links bounded 5000/5000 per ONE-M1/M2); P broken with P∘χ exact and a CPT-type Kramers reversor [H1, CPT]; ONE light (the field light) as in nature. It can gravitate through the universal coupling (EP mode W) and cannot mix with charged matter (U(1)_J′): a stable, gravitating, neutral massive species = a DARK-SECTOR candidate. Costs: (i) excited L0 ≠ today's board (the vacuum stays bit for bit); (ii) its mass is at the lattice scale (w ≥ 0.4255 rad/update), so it decouples in the continuum limit (a cutoff-scale dark sector, not a tunable DM mass); (iii) its hands stay in L0 (row 13): it does not explain nature's weak hands. **P1 proposal: ADOPT the handed class for L0, as the dark/clock sector, with these costs stated; nature's hands must still come through matter's coupling (row 13, U5 item 7).** | P2 leans HANDED (agree_positions_P2 item 1): +++ keeps an extra massless scalar at zero headroom (G9b blow-ups; N > 1 unstable); handed L0 = neutral massive Kramers dark species, stable links (math 5000/5000), CPT-type reversor, hands at the lattice scale where long-wave light and gravity cannot see them; "one light, one cone" fits nature; cost: today's +++ excited dynamics | **AGREE on the JOINT LINE** (both lean HANDED; the owner decides what L0 is for) → **P2: AGREE = THE JOINT LINE. ADOPT the handed class for L0 (owner decision), with P1's three costs. P2 adds: (a) L0 cannot be the world's light in either class: its massless mode is the A1 SCALAR, not the photon; (b) the handed L0 is a neutral massive Kramers dark/clock sector with no continuum modes [N7b], so its hands stay at the lattice scale and light and gravity stay P-blind, as observed; (c) nature's weak hands still need matter's coupling (a NEW LAW, M5). Signed together. ONE REFINE to the joint line's sentence 'L0 is massive, so B1-GRAV's built site/hop (W) lapse split is then EXACTLY right': P2 N12b (exact Bloch, +−+, U = 0.05) shows that in the OFFICIAL raw click reading (proper time = sign cycles of the sizes, carrier 0) the split makes every mode with w0 < π/2 tick FASTER (top band edge 0.426 → 0.525) and modes above π/2 slower: non-universal. It is EP-correct only in B1-GRAV's demodulated π/2-carrier (first-order) reading (their 8.7e-7 test). The DIFFERENCE form slows every mode by the half-angle law sin(w/2) = √f sin(w0/2) (error 1e-16) in the official reading, for both classes. Proposed wording: 'the split is right only if L0's clock is read on the π/2 carrier; with the official sign-cycle clock use the difference form' (U2 must fix L0's clock convention)** | OA, KD, N4, CPT; N5–N7b; ONE-M1/M2 (relayed) |
| M2 | **EP for L0: remedy W vs R** | Physics: Einstein requires the SAME rescaling for every clock and rod. R (today's board bit for bit, rounded lapse) violates the EP at relative 1/Q (6.27e-6 at Q = 8193; 1.9e-9 at the system Q): below every click precision in practice, but a law-level violation that vanishes only as Q → ∞. W (L0 at weight Q−1, difference form, one cone c_Q) is EP-exact and gives L0 the field gears' corner headroom; today's board survives only as the vacuum. **P1: W**, together with the max-N = 1 datum. If M1 = handed, today's board is already changed for excited data, so W costs nothing extra. If +++ is kept, R is an acceptable owner choice labelled "EP to 1/Q" | AGREE with P1 (agree_positions_P2 item 2). **N12 (exact Bloch, pre-registered, pinned) DECIDES the form:** at uniform U = 0.05 the site/hop split gives L0's massless mode a MASS, w0 = 0.3176 ≈ √(2U). It is right only for massive clocks (μ = 4 → 4N, 8/8). The port-DIFFERENCE (Laplacian) form keeps cos w = 1 exactly, with speed × √f. So the lapse must act on L0's difference potential at weight Q−1 (P1's Φ = −((Q−1)/2) Σ (b_p(x+e) − w b_g(x))²) | **AGREE**: for +++ L0 the EP-exact remedy is the difference form at weight Q−1 + the max-N = 1 datum (mode W with the difference split); R = "EP to 1/Q" only. For a HANDED (massive) L0 the built site/hop W split is exact. Joint test: L0 light massless in uniform U (cos w = 1 at k = 0), Shapiro 2 ± 0.1 in clicks, vacuum bit-identical → **P2: REFINE → AGREE: W preferred, in the DIFFERENCE form. N12: the split (B1-GRAV's R/W as built: clock factor on M(0), link factor on the rest) gives the massless mode w0 = 0.3176 ≈ √(2U) at U = 0.05. The difference form keeps cos w = 1 exactly, and every massive mode gets the half-angle law sin(w/2) = √f sin(w0/2) (DER). R is acceptable only as 'EP to 1/Q'. The handed class has no massless L0 mode, but the difference form is still the universal one. B1-GRAV should rebuild W in the difference form** | P2 N12; B1-GRAV L0-EP; P1 n2 (i), FINDINGS §6 #2 |
| M3 | **The owner principle "the detector acts before the click"** (P2 R15/§10, N8) | AGREE with the Rule3 parked-detector LEMMA (a gear at a = b = 0 transmits nothing, so any reciprocal partner acts only after the first overflow) and with P2's route: audit-labelled reciprocal ABSORBERS (U(1)-invariant, Board-Noether-conserved) decohere the ensemble BEFORE any click [N8: V_ens 1.00 → 0.22, single runs ~0.8, rewind exact, no runaway]. Physics caveats: (i) on an exactly reversible board "irreversible" can only mean a sink of many modes (a fibre or a bath) whose recurrence time exceeds the experiment (Poincaré); N8's Rabi revival (0.95 at t = 40) is the one-mode case; (ii) the race (b2) predicts a click DELAY ∝ N²p(1−p), a QM-deviating timing signature to be stated as PRED and compared with time-resolved detection; (iii) exclusivity must come from conservation (absorbing states), not from a kick | as in §10 (lemma TH; N8 exploratory; PC1–PC8 pre-registered). NEW **N11**: absorbers + a C0-fibre sink kill the revival (V_ens 0.23–0.32 to t = 60), charge identity and rewind exact; but the coupled system GROWS (C0 sits on the stability edge) ⇒ the sink must be a HEADROOM carrier | **AGREE**: lemma TH; pre-click erasable decoherence NUMERIC (exploratory, N8); a sink is needed (N11 removes the revival) and must have headroom (N11 growth) = P1 caveat (i) made concrete; caveats (ii) race-delay PRED and (iii) exclusivity by conservation stand; tests PC1–PC8 → **P2: AGREE with caveats i–iii. P2 adds N11 (exploratory): a C0-fibre sink removes the revival (V_ens 0.23–0.32 to t = 60; single runs ~0.8; exact charge identity and rewind), but the coupled system GROWS (max\|b\| → 114/476), because C0 sits on the stability edge (TH-C0). So the sink must be a HEADROOM, many-mode carrier** | P2 §10, N8, N11 |
| M4 | **F7: round cone vs taxicab, with the onset test** | AGREE that F7 as built uses the cone gap. MERGED TEST (P1 F7-ONSET + P2 U5-T1): the front on the round-cone light gear; Bob at equal Euclidean r along [100] AND [111]; PASS iff (a) E = 0 and Bob's statistics unchanged for t_B − t_out < r/c_Q in BOTH directions (incl. the gap window); (b) after arrival \|E − cos\| ≤ c/A and S direction-independent within O(1/A); (c) an amplitude-limited (normalised, one-shot) reader, so that \|front\| ≤ \|clock\| (no clipping, S ≤ 2√2); (d) report the [100]/[111] onset difference for a SMOOTH (σ ≥ 4) and a POINT front (P1 P7: a point front leaks 35 % ahead on [100]) | AGREE (agree_positions_P2 item 4): the C0-fibre F7 runs on the taxicab cone; light-gear fronts remove the gap correlations [TC.17]; the approved form needs a DC-free source and AMPLITUDE-LIMITED one-shot Born readers (clipping 3.35–3.40); tests TC.19 + F7-ONSET | **AGREE** (one merged test) → **P2: AGREE (one merged test)** | TC.7, TC.17, TC.19; P7, P7s |
| M5 | **P/CP/handedness**: L0's hands are lattice-scale; matter cannot inherit them without a NEW LAW | AGREE: χ commutes with right-Q8 (row 13); a signed L0 has no long-wave sector (gapped); a coupling of L0 to the Dirac pair is a mixing block = NEW LAW (s6 (g)); the only in-tensor route to matter's hands is a frame (c1-type) coupling of matter, whose fixed-vacuum version is SME-b_μ-like (row 24) | AGREE (agree_positions_P2 item 5): matter + E1 exactly P, C, CP, T; the ± gives only lattice-scale hands on a gapped L0; χ commutes with right-Q8; V−A for matter needs a NEW block or LAW (frame–internal coupling, chiral gauge block, or domain wall); CKM-type CP violation FAILS; the matter excess = seed data with ≥ 2 species | **AGREE** → **P2: AGREE** | rows 9–13, 24; N2, N5–N7b |
| M6 | ONE merged U5 list | see (IV) | see (IV) | P2 to mark (IV) → **P2: see (IV) below** | — |
| M7 | **NEW (manager 11:0x): one cone for every FREELY PROPAGATING field — Einstein-consistent if the SU(2)/SU(3) link waves are slow?** | Local Lorentz invariance needs ONE limiting speed for ALL fields, massive or not: w² = m² + c²k² with the same c (species-dependent limiting speeds are Lorentz violation; SME-type bounds are very tight). The photon (E1) and the metric share c_Q [EM-D4, D4] ✓. **SU(2)/SU(3) link waves: no mass gap today** (DERIVED): the OD4 spring fixes only \|U\| (the radial mode is massive, cos w_r = 1/3 at λ = 4 [NOTES_gauge S1]); the angular (gauge) modes get a mass only from a Higgs condensate on the links, i.e. a fixed vev entry κv² Re tr U (rank 2, inside the tensor), which is not built. With a cap ≈ 0.2 (ONE-M2) and no gap they are a slow massless species: **FAILS local Lorentz** unless (a) confined/frozen (B1-GAUGE's verified regime: link transfer below integer resolution [EM-C6]), or (b) gapped (then the violation moves to k ≳ m), or (c) the link stiffness reaches c_Q (ONE-M2: needs a plaquette entity, not B3-local = NEW LAW) | **N13** (P2, pre-registered, pinned): the SHIPPED compact links have GAPLESS gauge bands with long-wave speed 0.012 (≈ c_Q/48), isotropic ⇒ our SU(2) has NO mass gap and a second, slower cone. P2 row **R16**: "one cone" holds for the E1 photon + metric only. U5 item: plaquette entity, or Higgs-gapped links with front c_Q | **AGREE** (P1 DERIVED "no gap" = P2 NUMERIC N13). Joint row R16: ONE cone holds for the freely propagating massless fields (E1 photon + metric, c_Q) ✓; the SU(2)/SU(3) link waves are a second, slower, GAPLESS cone ⇒ local Lorentz FAILS for them until (a) frozen/confined, (b) Higgs-gapped (a vev link entry, rank 2, inside the tensor; the limiting-speed mismatch then shows only at k ≳ m), or (c) stiffened to c_Q (plaquette entity = NEW LAW) → **P2: AGREE; REFINE 'no gap today' from DERIVED to NUMERIC: P2 N13 (linear part of the pinned tensor, regime F): u1 has 3 and su2 9 zero modes at k = 0; the gauge bands are gapless with long-wave speed 0.0121–0.0122 ≈ c_Q/48, isotropic; the next modes are at w ≈ 0.585 (radial/2-path). The Higgs-vev test stands (U5 item 12)** | NOTES_gauge S1; EM-C6; P2 N13; ONE-M2 (relayed) |

## (IV) ONE merged U5 list (physics side), ranked by gain. Backbone = P2's 14-item proposal (agree_positions_P2 item 6); P1's items folded in [P1 #n]
1. **"Gravity only slows" as data + its dynamic conditions.**
   - The k = 0 lapse datum with max N = 1, plus a wave margin, on OD2 accumulators, with an EXACTLY conserved first-order
     (Dirac) stress (F4b/c: a non-conserved stress drives U < 0 and explodes).
   - Test: bounded ≥ 1000 updates with U ≥ 0 at every sample; a zero-mean control grows at the top-eigenvalue rate (N2b-type).
   - [P1 #1; P2 §3b]
2. **Round-cone quantum fronts.**
   - Light-gear fronts with a DC-free source and AMPLITUDE-LIMITED one-shot Born readers.
   - Tests: TC.19 + the merged F7-ONSET (M4).
   - [P2 P1; P1 #5]
3. **L0's place.**
   - The sign class (OWNER, joint line M1: both lean HANDED).
   - The universal lapse:
     - HANDED → the built site/hop W split (exact for massive modes);
     - +++ → the difference form at weight Q−1 [N12] + the max-N = 1 datum.
   - Tests: L0 massless (or gapped) as the class requires; Shapiro 2 ± 0.1 in clicks; vacuum bit-identical; links bounded
     (handed: excursions < 9.8 %).
   - [P2 P2; P1 #2]
4. **ONE cone for EVERY freely propagating field (R16 / M7).**
   - The links are slow and gapless [N13].
   - Fix: either a plaquette entity (NEW LAW), or Higgs-gapped links (a vev link entry) with a front on c_Q.
   - Test: link dispersion, gap and k² coefficient vs c_Q².
   - [P2; P1 M7]
5. **All layers coupled at once + light tests on the package.**
   - Dirac stress → h; EM light → h.
   - Shapiro and bending of the EM A-wave in [1.8, 2.2].
   - Redshift via light to 1e-3 (D8 now FAIL/OPEN).
   - Free fall from clicks with the two-size click energy (D5 now ✗ +12 %).
   - [P2 P3; P1 #3, #4]
6. **Odd-Q one-shot readers** (TC.15b). [P2 P4; P1 #12]
7. **The pre-click detector (owner principle).**
   - Absorbers + a HEADROOM sink (N11) + recorders, or the race.
   - Tests: PC1–PC8; the race delay ∝ N²p(1−p) as a PRED.
   - [P2 P5, P11; M3]
8. **Time dilation (reunion) + Dirac clocks under the lapse.**
   - TD2 done at 0.6c (SR ratio to 0.3 %). Next: 1e-3 with σ ≥ 16 or several laps.
   - Dirac clocks: the half-angle law in clicks to 1e-5.
   - [P2 P9; P1 #6, #7]
9. **AB and COW.** [P2 P7]
10. **Hands (HAND leads).**
    - The chirality NEW LAW (frame–internal coupling / chiral gauge block / domain wall).
    - U5-T10 continuum test.
    - The CPT-even check of a frame-vacuum coupling (no SME b_μ).
    - The CPT bounce on a handed sector (R² = Z ⇒ a twisted bounce).
    - [P2 P6, P10; P1 #9, #10, row 24]
11. **P+ leakage / baryogenesis budget.** [P2 P8]
12. **Compact U(1) vs E1 (g).** Keep E1 as the light block until a compact regime passes Newton III within 2.5 % over T ≥ 60 and a [111] link wave within 3 % of c_Q. [P1 #8]
13. **Structural QM limits (OWNER; record, do not fix inside the rules):** statistics/HOM, spacelike Bell (PRED vs 2015), zero-point, loops/confinement. [P2 P12; P1 #11]
14. **Cosmology (law level):** no expansion on OD2. [P1 #13]

**P2 mark on (IV) (Tue Nov 10 11:12:09 UTC 2026):** AGREE with the 14 items and their order (the backbone is my proposal; P1's items are folded in correctly). ONE REFINE, item 3: 'HANDED → the built site/hop W split (exact for massive modes)' should read 'HANDED → the DIFFERENCE-form lapse as well, unless L0's clock is declared to be read on the π/2 carrier'. P2 N12b: in the official sign-cycle reading the split makes modes with w0 < π/2 tick faster (0.426 → 0.525 at U = 0.05) and the others slower. The difference form gives the half-angle law for every mode (error 1e-16).

**P1 response to the N12b REFINE (Tue Nov 10 11:15 UTC; evidence s7/ONE-P1_work/lf_bloch.json, lf2_bloch.json, pre-registered 11:11/11:13):**
- ACCEPTED: the built split is non-universal in the official sign-cycle reading. Both codes agree (P2 N12b; P1 LF form A:
  massive R ∈ [0.935, 1.089] on +++ and [0.938, 1.386] on ++−; the massless mode gets cos w = 0.90).
- ONE PRECISION (P1 REFINE on the REFINE). In the official (raw, second-order) reading, the package's GR factors are clock
  1 − 2U on mass terms and link 1 − 4U on gradients. With those factors the PURE difference form gives every MASSIVE L0 band
  sin(w/2)/sin(w0/2) = √(1−4U), not the EP value √(1−2U) (LF form B: 0.894427 vs 0.948683, every band, both boards).
- P2's N12/N12b use the first-order factors (f = 1 − 2U). That makes the massive bands EP-right, but L0's MASSLESS light then
  has speed ratio √f = 0.948683, which is the 1911 value (γ = 0). This is P2's own N12 number, reproduced by LF2.
- The form that is right for BOTH (LF2 form C, exact to 7e-16, light speed 0.894426 = √(1−4U), massless kept, on +++ and ++−):
  W = the difference form on the transport, ΣW_d(1 − shift_d) with the link factor 1 − 4U, PLUS the clock factor 1 − 2U on
  L0's on-site label MASS MATRIX M0 = 6·1 − ΣW_d.
- On the massless light, M0 = 0 and (C) IS the difference form. (C) differs only on the massive bands, where it supplies the
  clock factor that the EP requires.
- Proposed wording for item 3, M1 and E8, consistent with the owner-approved decision 3 ("W in the difference form"):
  "W = the difference-form lapse on L0's transport (link factor) with the clock factor on L0's on-site mass matrix M0; for the
  +++ light this is exactly the difference form; for the handed (all massive) class the M0 clock factor is what makes every
  band obey the EP in the official reading."

## (V) P2's prepared rows (agree_rows_P2.md), with P1's position
| P2 row | claim (condensed) | P1 | verdict → P2 confirm | evidence / maps to |
|---|---|---|---|---|
| Q1 | Born 2 exits exact in official clicks; three-view 0/10,080; odd quotients official | AGREE | AGREE → **P2: confirmed** | TC.2, N10, TH-off; A-R10 |
| Q2 | n ≥ 3 exits only sequentially; exit delay k−1 (PRED) | AGREE | AGREE → **P2: confirmed** | TC.6, N4b |
| Q3 | odd Q: no efficiency-1 routers; non-detection 1/Q at the system Q (PRED); one-shot readers | AGREE | AGREE → **P2: confirmed** | TC.13, TC.18 |
| Q4 | superposition exact only on C0; O(1/A) elsewhere; classical limit A → ∞ | AGREE (P1 used O(1/A) throughout) | AGREE → **P2: confirmed** | N3 |
| Q5 | single-quantum interference only on C0 carriers | AGREE | AGREE → **P2: confirmed** | S5P:B3; TH-C0 |
| Q6 | unitarity ↔ exact reversibility; collapse = conditioning | AGREE | AGREE → **P2: confirmed** | — |
| Q7 | all-or-nothing; conditional signature (PRED); Englert broken (PRED) | AGREE | AGREE → **P2: confirmed** | TC.8, TC.10 |
| Q8 | post-click reciprocal back-action breaks exclusivity and blows up | AGREE | AGREE → **P2: confirmed** | TC.11, 11b |
| Q9 | parked-detector lemma | AGREE (TH, one line) | AGREE → **P2: confirmed** | M3 |
| Q10 | absorbers decohere the ensemble before any click; revival ⇒ sink | AGREE (+ N11: the sink must have headroom) | AGREE → **P2: confirmed** | N8, N11 |
| Q11 | timelike cos, S = 5/2; spacelike 0; PRED \|S\| ≤ 2 | AGREE (row 19 wording) | AGREE → **P2: confirmed** | TC.7 |
| Q12 | C0-fibre F7 at √3c: S = 5/2 at round-spacelike t_B | AGREE (row 15) | AGREE → **P2: confirmed** | TC.7 |
| Q13 | TH-C0 (+ N9; McKee–Smyth lead) | AGREE (P1 did not prove it; accepts as TH single-component, NUMERIC two-component) | AGREE → **P2: confirmed** | TH-C0, N9 |
| Q14 | Tsirelson only for amplitude-limited readers | AGREE | AGREE → **P2: confirmed** | TC.17 |
| Q15 | spin structure; statistics and entanglement FAIL | AGREE | AGREE → **P2: confirmed** | N1a, EM-T7/T10 |
| Q16 | chirality Γ algebra; NN pairing | AGREE | AGREE → **P2: confirmed** | N1b, N1c |
| Q17 | no zero-point, no loops | AGREE (P1 adds to its table) | AGREE → **P2: confirmed** | — |
| Q18 | no gravity-mediated entanglement (PRED) | AGREE | AGREE → **P2: confirmed** | — |
| E1 | EP: clocks 2.9e-5, universality 4.8e-5, β_eff 1.006; antimatter +1.0000 | AGREE (+ P1 N1 8e-7) | AGREE → **P2: confirmed** | D1, EM-D7, N1 |
| E2 | γ = 1: 2.109/2.104 [D2c] | AGREE (+ P1 N3 2.038) | AGREE → **P2: confirmed** | row 4 |
| E3 | redshift via light FAIL/OPEN (best +0.9 %); clocks pass | AGREE | AGREE → **P2: confirmed**. Update (manager relay 11:1x): D8e gives +0.32 % vs GR first order (a marginal FAIL of the registered 0.3 %, improved from +0.9 %); R-P2's post-hoc L = 18 light redshift matches GR to first order, with Z_click = Z_event to 2e-7 | D8, D8e, D2b |
| E4 | GW: 2 TT polarizations, front 0.583, 1/R within 10 % | AGREE (P1 updates its cell) | AGREE → **P2: confirmed** | D4, D4b |
| E5 | Bianchi ↔ exact conservation (all constraints exact with the remainder) | AGREE | AGREE → **P2: confirmed** | EM-T5, C1, G3–G7 |
| E6 | one cone: EM 0.5774, GW 0.583 on c_Q; L0 at 1/√3 (to O(1/Q); exact in W) | AGREE; plus R16 (links are a second, slower cone) | AGREE → **P2: confirmed** | EM-D4, D4, N13 |
| E7 | "gravity only slows" (EP-invisible, CFL-mandatory, preferred time gauge, 2nd k = 0 datum; t* = 255 on wave gears; OD2 bounded 700) | AGREE (= rows 7–8) | AGREE → **P2: confirmed** | D7, F4 |
| E8 | L0 FAILS while separate; L0-EP R (1/Q) / W (exact) | AGREE + N12 (the W split must be the difference form for a massless L0) | AGREE → **P2: confirmed (+ N12b: for the handed class the split is non-universal in the official sign-cycle reading; use the difference form)** → **P1: accepted, with the M0 precision (LF2 form C; see the P1 response under (IV))** | M2; lf2_bloch.json |
| E9 | free fall from clicks not reproduced (+12 %) | AGREE (P1 updates) | AGREE → **P2: confirmed** | D5, D5c |
| E10 | no Friedmann expansion | AGREE | AGREE → **P2: confirmed** | S6 H-(d) |
| S1 | P, C, CP, T exact for matter + E1 ⇒ CPT; weak FAILS | AGREE | AGREE → **P2: confirmed** | N2 |
| S2 | the excess is seed data, ≥ 2 species | AGREE | AGREE → **P2: confirmed** | S6:A7 |
| S3 | unsigned mirror iff s_y = s_z, else P∘σ∘χ | AGREE (two codes) | AGREE → **P2: confirmed** | N5, H1 |
| S4 | χ-conjugation isomorphism | AGREE (two codes: N5d, chi_map) | AGREE → **P2: confirmed** | N5d, chi_map.json |
| S5 | lattice-scale handedness in one update from a mirror-symmetric start | AGREE (P2 single code) | AGREE → **P2: confirmed** | N6b |
| S6 | massless L0 light iff unsigned; signed gapped | AGREE (two codes) | AGREE → **P2: confirmed** | N7b, OA |
| S7 | θ = 0 by construction | AGREE (+ P1's reversor argument) | AGREE → **P2: confirmed** | row 22 |

## Signatures
- ONE-P1: rows written 11:05–11:15 UTC; P1 column final.
  - ACCEPTS every ONE-P2 REFINE: rows 6, B-R3a and M2 (difference form, N12); M3 (+N11: the sink needs headroom); M7 (+N13:
    "no gap" NUMERIC); (IV) items 3, 6, 12; M1, (IV) item 3 and E8 (N12b).
  - The form-C precision is agreed in BOTH codes: P1 LF/LF2 (lf_bloch.json, lf2_bloch.json) and P2-N12c (n12c_formC.json).
  - M1 joint line: ADOPT the handed class for L0 with the stated costs (owner decides what L0 is for).
  - Evidence folded in after P2's signature (manager relay; no re-marking needed): E3 → D8e +0.32 % (marginal FAIL of 0.3 %)
    and R-P2's L = 18 post-hoc match with Z_click = Z_event to 2e-7. M4 and M3 package facts (TC.19b; running detector clock):
    see the addendum below.
  - **ONE-P1 CO-SIGNS THE WHOLE FILE, Tue Nov 10 11:18:23 UTC 2026 (`date -u`). NO DISAGREE.**

### Addendum after both signatures (evidence only; no verdict changes; manager relay 11:1x)
- M4 (round cone): B1-CHOICE TC.19b (ρ0 = 0.75).
  - Gap: max S ≤ 0.09.
  - NO clipping: max S = 2.668–2.684 < 2√2.
  - E is an exact cosine at every readout, while ρ and θ drift (an A-independent lattice-light transient).
  - So the round-cone front REMOVES the cone-gap failure and RESPECTS Tsirelson. The fixed law cos(a − b − θ0) + O(1/A) still
    needs slow clocks and a long box.
- M3 (pre-click detector): B1-CHOICE proposes a RUNNING detector clock (u = 3Q·b_d + κ\|ψ\|²).
  - The clock part adds K = D·b_d, so the Born arcs are unchanged; this is consistent with P2's parked lemma.
  - Readout caveat: a running C0 detector clicks officially at every update. "One click per quantum" must be defined on the
    deviation δ from the free detector clock, or the detector must be audit-labelled with an official recorder.
- ONE-P2: marked every row of (I)–(III) at 11:09:13 and confirmed every row of (V) at 11:12:09.
  - AGREE everywhere; NO DISAGREE.
  - REFINEs: rows 6, B-R3a and M2 (the difference form, N12); M3 (+N11); M7 (+N13); M1 / (IV) item 3 / (V) E8 (N12b).
  - Tue Nov 10 11:15:24 UTC 2026: ACCEPT P1's precision on the N12b REFINE. Decisive check in my own code, P2-N12c (pre-registered,
    n12c_formC.json): form C = the difference form on L0's transport × (1 − 4U) + the clock factor (1 − 2U) on the mass
    matrix M0 = 6·1 − ΣW_d.
    - It gives every massive k = 0 band the EP half-angle law √(1−2U) (error 1e-15 on +++, 7e-15 on +−+).
    - It keeps the +++ light massless with speed ratio √(1−4U) = 0.8944 on [100] and [111] (γ = 1).
    - The pure difference form at 1 − 4U fails the EP for massive bands (0.054). At 1 − 2U (my N12) it gives light the 1911
      factor 0.9487.
  - P1's wording for item 3, M1 and E8 is ACCEPTED: "W = the difference-form lapse on L0's transport (link factor) with the
    clock factor on L0's on-site mass matrix M0".
  - M1 joint line = ADOPT the handed class for L0, with the stated costs.
  - **ONE-P2 CO-SIGNS THE WHOLE FILE, Tue Nov 10 11:15:24 UTC 2026 (`date -u`).**