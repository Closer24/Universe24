# AGREE_H — Study 7, U7 "the hands of nature" (+ ADDENDUM 2, the ±): twin agreement HAND-M1 × HAND-M2
- Skeleton, H1 column and proposed verdicts: HAND-M1, 11:20–11:4x UTC 2026-11-10 (`date -u` in HAND-M1_NOTES.md).
- Sources:
  - H1 = s7/HAND-M1_FINDINGS.md + HAND-M1_work/*.json;
  - H2 = s7/HAND-M2_FINDINGS.md (draft v1 + §0b, 11:10–11:14) + HAND-M2_work/*.json.
- Independence ended at the manager's relay (11:14). HAND-M1's draft v1 was on disk at 11:10, before HAND-M1 read H2.
- Verdicts: AGREED / AGREED-WITH-QUALIFIER (AwQ) / DISAGREE (both positions + a decisive check in BOTH codes) / AGREED-OPEN.
- Labels: THEOREM / NUMERIC (file) / DERIVED / OPEN / FAILS; NEW LAW = owner decision.
- H2 column filled by HAND-M1 from HAND-M2_FINDINGS.md §0b/§8/§10 (11:14–11:21) and the manager's relay (11:21).
  **HAND-M2: please confirm each "H2 mark" (or edit), then sign.**

## A. Algebra of the hands (matter block)
| # | claim | H1 | H2 | proposed verdict | evidence | H2 mark |
|---|---|---|---|---|---|---|
| A1 | γ5 = 1⊗σz = −P_xP_yP_z (an integer diagonal ±1 matrix: the orientation of the three transports). It commutes with P_d, J, J′, V, P_dJ′, K, C, T1..T3 and anticommutes only with W0. So mass, Wilson (and the parity matrix W0) are the only chirality-flipping entries; EM and pair isospin are vector-like | THEOREM + NUMERIC exact (h1_algebra.json) | THEOREM + NUMERIC 36/36 (hm2_algebra.json) | AGREED | both codes; = ONE-P2 N1 | ACCEPT |
| A2 | "Which side": left multiplication (spin/frame) and right multiplication (isospin) applied uniformly both commute with γ5, so every gauge action from either side is vector-like. The γ5 = +1 half is transported by L_d; the γ5 = −1 half by −L_d, which becomes right multiplication after q → q̄ | THEOREM: Γ5 commutes with L_H⊗1, R_H⊗1, L_H⊗σz | THEOREM: "chirality = which side the transport multiplies from (relative to the complex structure)"; frame-rotation couplings vector-like | AwQ: both true. "Which side" separates the hands only in the TRANSPORT (boost) term; no gauge or frame action can, because uniform left/right actions commute with γ5 | h1 A; hm2 §1 | ACCEPT |
| A3 | Massless pair commutant = u(2)_L ⊕ u(2)_R (dim 16); massive = u(2) = J ⊕ su(2)_pair; integer chiral rotations only Z4 = ⟨Jγ5⟩ | NUMERIC exact (nullspaces) | Z4 = ⟨Jγ5⟩ exact; U(1)_A linear-level only | AGREED | h1 B; hm2 §1 | ACCEPT |
| A4 | The 5th Clifford element is integer and on-site: α4 = J·Γ5·W0 (symmetric, Hamiltonian form) / P_s = 1⊗ε′ = −J·Γ5 (antisymmetric transport form, unique). A domain wall along an internal index binds Γ5-chiral modes, but uniform gauge fields couple both walls (vector-like) | NUMERIC + DERIVED | THEOREM (uniqueness) + DERIVED | AGREED | h1 C; hm2 §1, §6 | ACCEPT (+ hm2_domain_wall.json: the β = 0 modes have γ5 = +1 at s = 0 and −1 at s = N−1, slope 0.5998 = 2hop·k; J− shows the same γ5 at the same wall) |
| A5 | The pair isospin contains C (C = −T3·J; C acts on (T1,T2,T3) by an inner automorphism). A chiral block on the PAIR isospin (Γ5 alone) is C-even, CP-odd and CPT-odd: anti-nature, and it breaks R* | NUMERIC: h1 D (C on isospin: A,A,C); h3 L-variant R* FAIL (strong + quiet) | THEOREM (C = −T3·J); s4 A13 (Pauli–Gürsey) | AGREED | h1, h3_chiral_board_L_*.json; hm2_algebra.json | ACCEPT |

## B. Nielsen–Ninomiya, Rule3 and the time doubler
| # | claim | H1 | H2 | proposed verdict | evidence | H2 mark |
|---|---|---|---|---|---|---|
| B1 | Rule3 obeys NN. The linear step is S(k) = function of ONE Hermitian B(k): quasi-energies ε = arcsin(β/D) (J+) and π − arcsin(β/D) (J−); det T ≡ 1, no winding, gaps at ω = 0 and π. A Weyl node cannot sit at ω ∈ {0, π} (|β| = D: linear crossing ⇒ instability). So the anomalous-Floquet escape is impossible | THEOREM (step = f(B)) | THEOREM (T-NN2: no winding, homotopic to constant) + NUMERIC | AGREED (two independent proofs) | h1/§4; hm2 §2 | ACCEPT (+ hm2_nn_census.json: integer L = 4 transfer matrix, |λ| = 1 to 3e−14, ω = ±arccos(β/D) to 1e−14, det T = 1) |
| B2 | The time doubler is forced: a b-only self-block has the palindromic polynomial z² − (2β/D)z + 1; a temporal Wilson term would need own-a reads, which break bijectivity; the spatial Wilson term cannot lift J− | THEOREM | THEOREM ("Wilson cannot touch the time doubler") | AGREED | §4 both | ACCEPT |
| B3 | J− is the C-type (conjugate) mirror of J+: the same profile in the other J-sense carries ALL J-commuting Noether charges negated. Same helicity, opposite charge: (χ, q) ↔ (χ, −q) ≅ (−χ, q) | NUMERIC-float h10_doubler.json (velocity ±0.0809; charge, spin, J-number ∓7.7e5, conserved) + DERIVED (ρ_X = σ D sinω bᵀJXb) | THEOREM + NUMERIC census (hm2_nn_census*.json) | AGREED | h10; hm2 §2 | ACCEPT |
| B4 | J± are separated exactly by the J-number Noether charge N_J = ΣD aᵀJb (J commutes with every block, chiral ones included); only the remainder term mixes them (O(1/A)). S2* has N_J = 0 exactly, so it fills J+ and J− equally | THEOREM (disjoint supports at t = 0) | THEOREM + s6 C7 (E_J = 0) | AGREED | §4 both | ACCEPT |
| B5 | The plain time mirror Mp maps J+ ↔ J− and is an exact reversor of every b-only block, the chiral blocks included: an exact Lee–Yang-type mirror sector built into the clock's two senses | NUMERIC h3_mirror_M.json (W, L PASS) | THEOREM (T-NN4) | AGREED | both | ACCEPT |
| B6 | NN assumptions on the board: integers (no effect on topology); divmod (O(1/A), mixes J± only); second order in time (adds the J− mirror, no escape); not a Hamiltonian flow (symplectic map, no winding); discrete chiral symmetry (a Z2 grading suffices). None evades NN. Interacting Z16 / symmetric mass generation is a quantum many-body route with no classical-board analogue | DERIVED/THEOREM table | same table + Z16/SMG note | AGREED | §4 both | ACCEPT |
| B7 | Ginsparg–Wilson / overlap: not ultralocal (literature: Horváth; Jahn–Pawlowski), irrational: FAILS the six-neighbour integer rules | literature THEOREM | FAILS | AGREED | — | ACCEPT |

## C. The ± (owner's ADDENDUM 2)
| # | claim | H1 | H2 | proposed verdict | evidence | H2 mark |
|---|---|---|---|---|---|---|
| C1 | Two classes. A = {+++, +−−, −++, −−−}: unsigned inversion mirror, max\|λ\| = 6 (light). B = {++−, +−+, −+−, −−+}: only signed mirrors, sign = the A2 character χ, gapped (2+2√3). diag(χ) maps s → (s_x, −s_y, −s_z) exactly; right-Q8 commutes on all 8 boards | NUMERIC exact (h4_signs.json): 8 relabellings per board up to the global sign | NUMERIC: 16 signed relabellings (= 8 × ±1), 16-element signed commutant | AGREED (count convention: ±S) | h4; hm2_signs*.json; = ONE-M1/M2, ONE-P1/P2 | ACCEPT |
| C2 | Mirror on SPIN: on A the unsigned mirror swaps E1/2 ↔ E5/2 (keeps A1, A2, G3/2); on B, P∘χ keeps E1/2, E5/2, G3/2 and swaps A1 ↔ A2 | NUMERIC exact (h5_parity_spin.json, 8/8 each) | consistent: X4 maps T1↔T2 (A), A1↔A2 + E↔E (B) (hm2_x4_exact.json) | AGREED (H1 single code for the spin map; H2's X4 isotypic map agrees on V+) | h5; hm2_x4_exact.json | ACCEPT (H1 single code; consistent with hm2_x4_exact isotypic map) |
| C3 | Spinor sector V− (J = R_i block). A: an isotropic massless 4-component Dirac cone at k = 0, λ = 2 (E1/2 ⊕ E5/2, slope 0.943 on [100], [110], [111]). B: gapped; E1/2 at 2+2√2 and E5/2 at 2−2√2 = a Dirac mass ±2√2 on that 4-dim space, whose sign is the sign choice (++− ↔ +−+ exact). G3/2 levels 2±√2 lie in between, so "massive Dirac" is a k = 0 statement | NUMERIC-float h6_cone.json + exact rest values h9 | B gapped, Kramers-doubled, "spin-½-like" (§0, ONE-P1); cone not computed | AGREED-WITH-QUALIFIER (single code for the cone; the k = 0 rest values are exact algebra) | h6, h9 | ACCEPT (H1 single code) |
| C4 | Kramers on B: an exact antiunitary k-preserving symmetry squares to −1 on V− ⇒ every V− band doubly degenerate ⇒ NO Weyl node anywhere on B. A: no forced doubling | NUMERIC: h7 (200 k, 6e−15), h9 exact (A² = −1 on V− for ++−, +1 only for +++) | NUMERIC: P′² = −1 (Z4); ONE-P1 doublets | AGREED | h7, h9; hm2_signs_c.json | ACCEPT |
| C5 | P′ = P∘χ on B is a Z4 (P′² = global clock flip, or −R_q); B has no involutive parity | consistent (h9: S² ≠ 1) | NUMERIC (all 16 P′) | AGREED | hm2_signs_c.json; h9 | ACCEPT |
| C6 | **What χ is (manager item a) — SETTLED in both codes.** L0 has exactly 4 Board-Noether generators: 3 isospin + X4. X4 is an integer antisymmetric matrix on V+ only, commuting exactly with the six ports and with isospin, a complex structure on its support (X4² = −64 there). χ commutes with J and isospin, and **χX4χ = −X4**. X4 is an AXIAL / duality charge: T1 ↔ T2 on A (vector ↔ pseudovector), A1 ↔ A2 on B (scalar ↔ pseudoscalar); on A it is the helicity-type charge of L0's light. On V− (spinors) χ acts as a γ5-type flip (m → −m), and P∘χ is the Dirac parity β·I with a Z4 phase. **Joint line: χ flips no vector (C-type) charge; it flips exactly one charge, the axial V+ charge X4. So χ is a γ5/duality-type flip, not C. ONE-P1's "C-like" holds only formally (a charge flips). χ does not act on matter** | NUMERIC h11_X4.log (4 generators on +++ and ++−, X4 exact integer, χX4χ = −X4, V− norm 0); h5/h6/h9. H1 corrects its draft "flips no Noether charge" → "flips no vector charge; flips the axial V+ charge X4" | NUMERIC hm2_x4_exact.json (Noether identity 0/40 exact updates on A and B; χX4χ = −X4; isotypic map); proposed the same joint line | AGREED (both codes) | h11_X4.log; hm2_x4_exact.json | ACCEPT (the joint line; settled in both codes) |
| C7 | Click mirror on B: positions mirrored, frames relabelled by π, sizes × χ, kinds C1↔C2 on the 24 odd frames, C0 unchanged; mirror twice swaps all kinds. Kinds are J-signs (overflow direction), not chirality | DERIVED (§2.5) | NUMERIC exact on 68,542 clicks (hm2_signs_dyn.json) | AGREED | hm2; = ONE-P2 N6b | ACCEPT |
| C8 | Bounce on B (one-vacuum embedding, every gear at 3Q−1, odd Q): the Kramers-type R (R² = −1) fixes no seed. Order-8 reversors P∘χ∘T fix a 768-dim space, and an 8-integer seed bounces exactly. "Past = CPT-type mirror of future" survives on B | OPEN in H1 (involutive companion) → ACCEPTS H2's numeric | NUMERIC (hm2_bounce_onevac.json) | AGREED (H2's evidence) | hm2_bounce_onevac.json | ACCEPT |
| C9 | Remainder maps: every forward negation acts as r → c − r with c ∈ {D−2, D−1} (even r), {D−1, D} (odd r); fixes 3Q−1 with R′ for odd Q; fixes 2Q only for Q = 1 | consistent (R′ derivation §5.2) | THEOREM + brute force Q = 1, 3, 5 | AGREED | hm2 §3 S5 | ACCEPT |
| C10 | The ± is a MASS/GAP switch with a lattice-scale hand: B has no continuum sector; its hand is a Z4 intrinsic parity / X4 structure that no universal coupling transmits. The coincidence "short range + P-broken" with the weak force is a coincidence of one Z2 flux, not the weak interaction | DERIVED (§0, §2) | DERIVED (§5 end) | AGREED | both; ONE-P2 N7b | ACCEPT |

## D. Can matter inherit the hand inside the tensor?
| # | claim | H1 | H2 | proposed verdict | evidence | H2 mark |
|---|---|---|---|---|---|---|
| D1 | NO: (i) every matter matrix lies in Q8 ⊂ 2T = ker χ, and a χ-odd 90° spinor turn needs √2 (locked spin–isospin turns are χ-even overall); (ii) universal couplings (lapse 1, shift JP_d, spin L_d⊗1, boosts P_d) commute with γ5, and W0 is L↔R symmetric; (iii) matter-transport signs are a reflection; (iv) a constant axial/torsion background S0·γ5 is CPT-odd, and L0's vacuum is a = b = 0 with no remainder reads | THEOREM (§3) | NUMERIC: lapse (democratic / A2-even) and port-flux link couplings to A and B L0 keep matter EXACTLY mirror-symmetric for 60–80 updates; scalar exchange P-even by reciprocity (THEOREM); link-kernel mechanism OPEN | AGREED (theorem + numeric, complementary) | §3 H1; hm2_couple*.json | ACCEPT (+ hm2_portflux_mech.json: the induced L0 state is not mirror-symmetric; only the projection matter reads is. Link mechanism OPEN) |
| D2 | An on-site axial entry b0·γ5 makes L and R clocks tick at arccos(±b0/D): P-odd but CPT-odd (SME b0, Einstein–Cartan torsion background). Not nature's way | DERIVED | NUMERIC exact (hm2_axial_clock.json: 0.4475 / 0.5525 at b0/D = 1/6) | AGREED | both | ACCEPT |
| D3 | A NEW L0 × matter × matter block (or a coupling to the X4 density, which is a two-time quadratic = rank-4 a-read, forbidden today) could transmit L0's hand only at second order and lattice range (gap 0.426 rad). NEW LAW, not recommended as the weak force | DERIVED | DERIVED (rank-4 a-read) | AGREED | both | ACCEPT |

## E. The chiral weak block — NEW LAW (owner decision)
| # | claim | H1 | H2 | proposed verdict | evidence | H2 mark |
|---|---|---|---|---|---|---|
| E1 | The only CPT-consistent integer chirality is Γ5·V (chirality × charge circulation, V = JJ′): projector (1 ± Γ5V)/2 = (matter, one helicity) ⊕ (antimatter, the other). Pattern: P odd, C odd, CP even, T even, CPT even. Γ5 alone is C-even, CP-odd, CPT-odd. The sign ± is a convention (the P-image) | NUMERIC exact h1 F + h3 (R* PASS/FAIL) | NUMERIC hm2_va_block_diag.json (CP exact), THEOREM (pair isospin ∋ C) | AGREED | both | ACCEPT |
| E2 | It needs SU(2) on a SPECIES doublet (two Dirac pairs, 32 channels per node) commuting with J′ (fermion number); EM = J′ × species charge | NUMERIC (h3 W) | NUMERIC (hm2 §6) | AGREED | both | ACCEPT |
| E3 | Two integral forms of the SAME law (equivalent over Q, not over Z). (i) H1: the design's pair basis. The projector is half-integral, so couplings are even. Local SU(2) is exact as a Noether identity (0/648), and the vacuum is the APPROVED pair bit for bit. (ii) H2: the charge-diagonal basis, V = σz⊗1. The projector is 0/1, local Q8 covariance is bit-exact, and the weak half is a channel set in clicks. It is not unimodularly equivalent to the design's pair (index 256) | NUMERIC h3 (both regimes); h1 E (index 256) | NUMERIC hm2_va_block_diag.json / _design.json ("design basis cannot carry P_W gear-wise") | AwQ: same law; integral form = owner decision | both | ACCEPT AwQ + NEW NUMERIC hm2_va_clicks_design.json: in the PACKAGE basis the uncoupled half Im(1−P_W) is EXACTLY invariant (Vγ5 is a signed permutation and 3Q−1 is R′-fixed), so click-level P violation is exact there too (A = 2^8, 2^12, 2^16: 0 record differences). The charge-diagonal form only adds bit-exact Q8 gauge maps and a coordinate weak channel set |
| E4 | Time reversal: the design's K∘M flips the J′ Wronskian, so it is physically C·T. A charge-preserving T must anticommute with J′: T_phys = C∘K∘M (H1 package basis) = K8∘M′ (H2 charge-diagonal basis), Kramers. R* = W0J′K∘M (+inversion) is CPT | NUMERIC h1 G (J′ under K∘M −1, under CK∘M +1, under R* −1); h3 (CK PASS, R_T FAIL) | THEOREM + NUMERIC hm2_va_T.json (K∘M FAILS, K8∘M′ exact) | AGREED | both | ACCEPT |
| E5 | R* = CPT stays an exact reversor with the Γ5V block, so S2*'s exact bounce survives (the new gears sit at the R′-fixed vacuum 3Q−1). With Γ5 alone R* fails | NUMERIC h3 W PASS, L FAIL (both regimes); S2* fixedness DERIVED | CPT exact (NUMERIC) | AGREED | both | ACCEPT |
| E6 | Masses: the doublet needs a Higgs quaternion (Yukawa rank 3). A plain Wilson term breaks the chiral covariance (W0 maps P_W ↔ 1−P_W). The Higgs-dressed Wilson–Yukawa is covariant: exact Noether 0/648, rewind exact, and in the vacuum (W = φ = 0) bit-identical to the approved Wilson–Dirac pair (wilson = w·v, mass = 2y·v) | NUMERIC h3 (C1–C3, both variants, both regimes) | NUMERIC: plain Wilson breaks covariance and I_s; WY not run | AGREED | h3; hm2_va_block_*.json | ACCEPT (Wilson–Yukawa not rerun by H2) |
| E7 | **One honest NN statement (manager item c):** the chiral LAW is exact (integer, reversible, six-neighbour, rank 3 + OD4). Its SPECTRUM is vector-like: (i) without W0-type terms an exact staggered parity maps the light Weyl field onto its opposite-chirality corner doubler in the same gauged channels (4 L + 4 R per Weyl field); (ii) plain Wilson lifts the doublers but breaks covariance; (iii) Wilson–Yukawa keeps covariance and lifts the doublers to 4wv·n_π in the Higgs vacuum, but the lifted odd-corner doublers still couple with MIRROR chirality (lattice-scale masses); (iv) the J− mirror cannot be lifted. Classically, smooth J+ matter in the Higgs vacuum below the doubler masses feels a chiral force. Exact chirality as in nature (a quantum continuum limit) is NOT reached on an exact local lattice: OPEN (literature: the Wilson–Yukawa failure) | NUMERIC h3 + h8_corners.json (masses 2048/4096/6144; chirality −1 even / +1 odd corners; sum 0) | NUMERIC I_s exact without Wilson; Wilson breaks covariance; DERIVED: WY fails (literature) | AGREED (joint text) | h3, h8; hm2_va_block_*.json | ACCEPT |

## F. CP and the matter excess
| # | claim | H1 | H2 | proposed verdict | evidence | H2 mark |
|---|---|---|---|---|---|---|
| F1 | The current law is exactly P, C, CP and T (T = C∘K∘M): no hand and no CP violation | NUMERIC h1 D | = ONE-P2 N2 | AGREED | both | ACCEPT |
| F2 | No excess under the present law: every species' J′-number is an exact Noether charge (remainder term only). It is R*-odd, and S2* (R*-fixed) has all such charges 0 at the bounce. The visible J′-charge of S2* can drift O(A) through remainders (s6 C4); the mechanism of that drift is OPEN | THEOREM + s6 B5/C4 | agrees; H2's C-fixedness explanation of s6 C4 RETRACTED (relay 11:21), mechanism OPEN | AGREED (drift mechanism AGREED-OPEN) | both | ACCEPT (mechanism AGREED-OPEN; hm2_c4_seeds.json: reproduced without EM; hm2_c4_mech.json: Y(t+1) = S X(t) exactly for both seeds) |
| F3 | CP violation needs a non-removable complex (J-carrying) phase: ≥ 3 weak doublets with Hermitian mixing Re M⊗1 + Im M⊗J (Kobayashi–Maskawa), or a θF∧F block (F∧F is an exact gauge-invariant integer). NEW LAW | DERIVED | DERIVED (≥3 doublets; 2 doublets: removable by linear-level rephasing) | AGREED | both | ACCEPT |
| F4 | An excess needs (Sakharov) number violation (NEW LAW: not bilinear-J′-commuting) + C (Γ5V gives it) + CP + out-of-equilibrium (low-entropy seed). Otherwise it is seed data (≥ 2 species, neutral, not R*-fixed). With R* = CPT exact, a law-made excess is time-antisymmetric about the bounce (CPT-mirror universe) | DERIVED | DERIVED (seed data or O(1/A)) | AGREED | both | ACCEPT |

## G. Clicks and the mirror world (manager item e)
| # | claim | H1 | H2 | proposed verdict | evidence | H2 mark |
|---|---|---|---|---|---|---|
| G1 | Click kinds are J-signs (overflow direction), not chirality; a spatial hand shows only in correlations (spin × momentum, kind tallies of frame classes) or in tick rates | DERIVED | DERIVED + NUMERIC | AGREED | both | ACCEPT |
| G2 | The J− mirror world lives in the SAME official matter channels (it is a time-sense sector, not a channel set). It is separated in CLICK space by the two-time J-Wronskian W_J = Σ ℓ(t+1)ᵀJℓ(t): J+ packet W_J > 0 at 100 % of updates, J− < 0 at 100 % (H2), so a passive J+ readout can hide it. Alternatively it can be left EMPTY by a J-sense-pure seed (N_J ≠ 0; N_J is R*-even, so it is compatible with an exact R* bounce): CONSTRUCTED by H1 (h13_jpure_seed.json: exactly R*-fixed integer seed, J− fraction 1.9e−6 at A = 2^10 and 8.0e−9 at A = 2^14, N_J conserved to 5e−5 / 5e−7 over 40 exact updates; compact minimum OPEN). Either way the separation is exact at the linear level, with O(1/A) remainder mixing | DERIVED + NUMERIC (B4, B5, h10) | NUMERIC hm2_jsense_clicks.json (100 %/100 %, N_J ∓1.736e12 stable to 5e−4; S2*-type point seed N_J = 0, W_J ≈ 0, drift 5e7 on 1e12) | AGREED | both | ACCEPT |
| G3 | Click test T2 (bare V−A vertex, charge-diagonal basis, frozen random integer weak field = MECHANISM for the field): a P_W packet's official record differs from the free run (10,488 entries); its P-image (in 1−P_W) is identical to the free run (0 differences); its CP-image equals the CP-map of the first record (0 differences). So in clicks P is broken and CP is exact | NUMERIC h12_forward_syms.json (11:25): the FULL block (Higgs + Yukawa + Wilson–Yukawa + dynamical links, quiet regime, exact ints, T = 6): CP = inversion∘C·W0 an EXACT forward symmetry of the whole state (so of every click); P and C BROKEN. Γ5-alone variant: C exact, P and CP broken | NUMERIC hm2_va_clicks.json (bare vertex, frozen field) | AGREED (two codes: bare vertex in clicks, full block at state level) | hm2_va_clicks.json; h12_forward_syms.json | ACCEPT |

## OWNER UNIFICATION (joint; HAND-M1 11:2x merged with HAND-M2 §10.2): are decision 2 (handed sign class → a dark, massive Kramers L0) and decision 5 (a chiral weak law) the same thing?
**Joint answer: NOT one thing. They share ONE mirror, not one hand.**

**(U-a) Can ONE sign decide both hands? — NO by derivation; only by declaration (NEW LAW).**
- (i) The matter algebra is χ-blind: its matrices lie in Q8 ⊂ 2T = ker χ [THEOREM, H1 §3].
- (ii) Universal couplings do not transmit the board's hand [NUMERIC hm2_couple*.json; THEOREM for scalar exchange by
  reciprocity, H2 §5].
- (iii) The flux s_y·s_z is P-even (inversion maps ++− to +−+ inside class B). The matter's orientation sign under transport
  signs is s_x·s_y·s_z (a reflection relabels Γ5). These are different Z2's.
- Writing the weak projector as (1 ± s·Γ5V)/2 with a shared sign ties the hands only by fiat (NEW LAW, no physics forces it).
  Their agreement becomes observable only through a new L0 × matter × matter block (second order, lattice range). With the
  L0 vacuum at zero, its exchange kernel is even by reciprocity, so it produces no P-odd matter effect [THEOREM, H2 §5].
- **What IS shared, exactly** [THEOREM-level: spatial inversion acts on all sectors at once]: with a B-class L0 and the Γ5V weak
  block, the whole board has ONE exact mirror, **P∘(χ on L0)∘(C on matter)**. χ (an axial/duality flip of X4 on L0) and C (on
  matter) are the two faces of the board's single "CP". The pattern "P broken, P∘X exact" is the same; the hands are
  independent.

**(U-b) Can the mirror partners hide in the non-clicking part, so that the clicks show one hand while the board stays
balanced? — PARTLY: yes for the time-mirror world, no for the spatial doublers.**
- **The J− mirror world: YES, by a readout or by the seed.**
  - (i) READOUT (an OD1-type observer rule, not a law). The click-space J-Wronskian W_J = Σ ℓ(t+1)ᵀJℓ(t) separates J+ from J−
    at 100 % of updates [NUMERIC hm2_jsense_clicks.json]. An official observer that counts only J+ events sees one world.
    J− is then a DARK mirror world with the opposite weak hand: it still gravitates (gravity is J-even), and it is exactly
    balanced with ours (Mp and R* = CPT exact).
    - Caveat (H1): W_J is a two-time, node-local criterion (ℓ at t and t+1, contracted with J), not a per-click channel
      label like OD1. It is still passive (it reads determined clicks only).
  - (ii) SEED (data). A J-sense-pure seed (N_J ≠ 0; N_J is R*-even, so an exact R* bounce is still possible) leaves J−
    EMPTY. CONSTRUCTED (H1, h13_jpure_seed.json): project an R*-symmetric smooth state exactly onto J+ (the projection
    commutes with R*), round b, and set a = G·b(−x). The seed is exactly R*-fixed; its J− fraction is 1.9e−6 (A = 2^10) and
    8.0e−9 (A = 2^14), ∝ 1/A². After 40 exact updates the leak is 8e−5 / 3e−7. The compact minimum is OPEN.
  - S2* as approved has N_J = 0: it fills both worlds equally.
  - Exactness: the separation is exact at the linear level, because N_J is an exact Noether charge and J-commuting couplings
    never mix J±. Only the remainder mixes them, at O(1/A) (H2: a point seed's N_J drifts 5e7 on a 1e12 scale).
- **The spatial NN doublers: NO by readout; only by ENERGY.**
  - They share gears and J-sector with the light species. Wilson–Yukawa (part of the NEW-LAW block) makes them heavy:
    4wv·n_π (h8).
  - Smooth low-energy data do not excite them, so low-energy clicks show one hand.
  - At lattice energies they return and couple with MIRROR chirality (h8; H2's I_s). Not exact.
- **Click tests:**
  - T2 RUN [H2, hm2_va_clicks.json]: bare V−A vertex, frozen weak field. A P_W packet feels the field (10,488 differing
    entries); its P-image does not (0); its CP-image equals the CP-map of its record (0). **P broken, CP exact, click for
    click.**
  - Still to run:
    - T2 with Wilson–Yukawa and a dynamical field (H1's quiet regime);
    - T1: per-update sign of W_J on mixed seeds (misclassification rate);
    - T3: Fourier-resolved click sizes (odd-corner content at the rounding level for smooth seeds);
    - T4: a β-decay-type P-odd correlation Σ spin_z·velocity_z of weak-scattered packets, of opposite sign in J−.
- **Where each piece lives:**
  - inside the tensor: the signs (mass gap and an axial mirror twist on L0);
  - NEW LAW: the Γ5V chiral block with Higgs and Wilson–Yukawa;
  - observer rule: the J+ readout (or a seed choice: J-pure);
  - exact at the linear level; O(1/A) and lattice-scale leaks remain.
- **One line:** "Symmetric on the board, one-handed in the clicks" is reachable: the law stays mirror- and CPT-balanced
  (Mp, R*), the hand is the chiral law, and the mirror world is made dark by a J+ readout or empty by the seed. But the
  ± signs are not that hand; they are a separate mass/gap switch.

## OWNER DECISIONS (joint recommendation first)
1. **Weak force (NEW LAW).** Adopt the Γ5·V chiral SU(2) block on a species doublet (two Dirac pairs) with a Higgs quaternion,
   Yukawa and Wilson–Yukawa: rank 3 + OD4; vacuum = today's approved matter bit for bit; R* (CPT) kept.
   - **Do NOT use "Γ5 alone":** it is CPT-odd, breaks the bounce, and is maximally CP-violating.
2. **Integral form.** Use the package basis (vacuum bit-identical; local SU(2) Noether-exact) unless the owner wants the hands
   visible as a channel set in clicks. Then use the charge-diagonal basis (bit-exact local Q8; a new integral form, index
   256).
3. **Mirror world.** Choose how the J− mirror world is handled:
   - (a) J+ official readout (OD1-type observer rule): a dark mirror world;
   - (b) a J-pure R*-fixed seed: an empty mirror world (constructed, h13; compact size OPEN).
   - Recommendation: (b), since it is now constructed; (a) as the observer-side fallback. S2* as approved fills both equally.
4. **The ± signs.** Keep +++ for L0: light, and a massless Dirac cone in V−. A B-class L0 is a gapped, Kramers, axially
   twisted sector. It is allowed as a choice of entries, but it gives no hands to matter and has no light.
5. **CP / excess (later, NEW LAW).** ≥ 3 doublets with J-carrying (Kobayashi–Maskawa) mixing, or θF∧F, plus a
   number-violating block if an excess must be grown. Otherwise the excess is seed data (≥ 2 species, neutral, not
   R*-fixed).
6. **Honest status (joint NN statement, E7).** The law is exact; the spectrum is vector-like (heavy mirror doublers + the J−
   mirror). Exact one-handedness holds classically for smooth J+ matter below the doubler masses. The quantum/anomaly status
   is OPEN.

## Six-line plain answer (joint)
1. The ± signs are a mass switch: the handed boards lose light and make the board's own spinors massive and Kramers-paired,
   so no left-only particle can live there. Their "hand" is a lattice-scale twist of an axial (helicity-type) charge.
2. Matter cannot catch that twist by itself: its whole algebra lives where the twist is invisible, and every universal
   coupling treats left and right alike.
3. Nature's hands need one new law: a weak force coupled to chirality × charge (Γ5·V). It is exact in integers, keeps today's
   matter in its vacuum bit for bit, and keeps the seed's bounce, which is exactly CPT.
4. With it, the clicks already show P broken and CP exact, click for click.
5. The lattice still pairs every hand with a mirror partner: heavy corner doublers, and a time-mirror world in the second
   clock sense. The board stays mirror-balanced; our one-handed world is the J+ half, darkened by the readout or emptied by
   the seed.
6. CP violation and a matter excess need further new laws (three families with complex mixing; number violation), or they
   are simply in the seed.

## Signatures
- HAND-M1: skeleton, H1 column, H2 column (from HAND-M2 §0b/§8/§10 + relay 11:21), verdicts, joint OWNER UNIFICATION,
  decisions and six lines, 11:20–11:2x UTC. C6 settled in both codes (h11_X4.log; hm2_x4_exact.json).
  **HAND-M1 SIGNS all rows as written (no DISAGREE): Tue Nov 10 11:24:18 UTC 2026 (`date -u`).**
- HAND-M2: marked every row (ACCEPT, no DISAGREE) and SIGNED; see the section below.


## HAND-M2 marks: details and signature (HAND-M2, 11:26 UTC, `date -u`)
- **All rows marked ACCEPT** (A1–G3; 39 cells). There is no DISAGREE. The extra cell in HAND-M1's interim table
  ('||') has been removed.
- **New evidence since the relay** (all in s7/HAND-M2_work/):
  - **E3 / decision 2.** hm2_va_clicks_design.json: click-level P violation is EXACT in the package basis too. This
    strengthens decision 2 (package basis): the charge-diagonal form is needed only if the owner wants the weak half to
    be a coordinate channel set, or bit-exact Q8 gauge maps.
  - **F2.** hm2_c4_mech.json: for BOTH seeds the Y-block trajectory is an exact image of the X-block trajectory one update
    earlier, Y(t+1) = S X(t) with S = (seed-centred inversion)∘K8W08.
    - So Q′ reduces to −D Σ (S b_X(t−2))·b_X(t). The other term vanishes by antisymmetry of K8W08.
    - This is identically 0 for the node seed and not for S2*. The rest of the mechanism stays OPEN.
  - **G3.** hm2_va_clicks.json: P broken and CP exact in official clicks (bare vertex, frozen field).
- **OWNER UNIFICATION, OWNER DECISIONS and the six lines: ACCEPT as merged by HAND-M1.**
  - Decision 3: I agree with (b) if constructible, else (a). Both keep the law balanced (Mp, R*).
- **HAND-M2 SIGNS all rows, the OWNER UNIFICATION section, the decisions and the six lines as written: Tue Nov 10 11:25:40 UTC 2026.**

## Post-signature addenda (HAND-M1, Tue Nov 10 11:27:26 UTC 2026, `date -u`) — for HAND-M2 to confirm; they strengthen, do not change, any verdict
- **G3 (11:25:29).** h12_forward_syms.json: on the FULL block (Higgs + Yukawa + Wilson–Yukawa + dynamical links, quiet regime,
  exact ints) CP = inversion∘C·W0 is an EXACT forward symmetry of the whole state (hence of every click); P and C are BROKEN.
  The Γ5-alone variant has C exact, and P and CP broken. This complements H2's bare-vertex click test (hm2_va_clicks.json) and
  hm2_va_clicks_design.json.
- **G2 / U-b / Decision 3 (11:27).** The "empty mirror world" seed is now CONSTRUCTED (h13_jpure_seed.json):
  - exactly R*-fixed integer seed (a = G·b(−x), G = W0J′K);
  - J− fraction 1.9e−6 (A = 2^10) and 8.0e−9 (A = 2^14), ∝ 1/A²;
  - N_J conserved to 5e−5 / 5e−7 over 40 exact updates;
  - leak after 40 updates 8e−5 / 3e−7;
  - compact minimum OPEN.
  - Decision 3 therefore reads "(b), since it is now constructed; (a) as the observer-side fallback". This matches HAND-M2's
    signed "(b) if constructible, else (a)".
- No row verdict changed. HAND-M1 re-signs the table with these addenda: Tue Nov 10 11:27:26 UTC 2026.

- **HAND-M2 CONFIRMS both post-signature addenda (Tue Nov 10 11:29:53 UTC 2026, `date -u`), checked independently in my own code (HAND-M2_work/hm2_confirm_addenda.py/.json):**
  - **G3.** On a fuller block in the CHARGE-DIAGONAL basis (V−A vertex + Higgs quaternion + Yukawa + Wilson–Yukawa;
    frozen random integer links and Higgs, exact matter step):
    - local Q8 covariance with Φ → gΦ is EXACT;
    - CP = inversion∘C∘W0 (links reflected + conjugated, Higgs reflected) is an EXACT forward symmetry;
    - P fails in all 4 field-map variants, and C alone fails.
    - This agrees with H1's h12 (dynamical fields, package basis).
  - **Decision 3 (scaling).** My own J+-projected packets (FFT projection then rounding; NOT the R*-fixed construction):
    - J− fraction 6.3e−6 at A = 2^10 and 2.7e−8 at A = 2^14 (ratio 231 ≈ 256: ∝ 1/A²);
    - after 40 exact updates 5.2e−4 and 2.0e−6 (∝ 1/A², the same ratio as H1's 8e−5/3e−7);
    - N_J drift 2.1e−3 and 2.3e−4 (decreasing with A; larger than H1's because the seed and parameters differ).
    - The R*-fixedness of h13 was not re-checked by me.
  - Decision 3 = "(b), constructed; (a) as fallback": AGREED. No verdict changes.
