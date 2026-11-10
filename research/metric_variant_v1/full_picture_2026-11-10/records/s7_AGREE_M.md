# AGREE_M — Study 7 "ONE PICTURE": twin agreement ONE-M1 x ONE-M2
- Merged by ONE-M1 at Tue Nov 10 11:12:38 UTC 2026 (`date -u`).
- Sources:
  - drafts: s7/ONE-M1_FINDINGS.md and s7/ONE-M2_FINDINGS.md (both read in full after the manager's 11:05 relay);
  - ONE-M2's marks: s7/ONE-M2_AGREE_COLUMN.md (11:09–11:10) on ONE-M1's 27 rows (s7/ONE-M1_AGREE_ROWS.md);
  - ONE-M2's extra rows M2-1…M2-15, marked here by ONE-M1.
  - The earlier ONE-M1 skeleton is kept as ONE-M1_work/AGREE_M_skeleton_1110.md.
- Labels: THEOREM / NUMERIC (exact integers, file) / NUMERIC-float / DERIVED / OPEN / FAILS.
- Verdicts: AGREED / AGREED-WITH-QUALIFIER / DISAGREE. **There is NO DISAGREE row.**
- Work folders: s7/ONE-M1_work/ (m1_*), s7/ONE-M2_work/ (m2_*).

## 1. ONE-M1's rows, marked by ONE-M2
| id | claim | ONE-M1 | ONE-M2 | verdict | evidence |
|---|---|---|---|---|---|
| U1-1 | L0 = R[2O] per node. H(k) = sum_u s_u diag(e^{ik.R(g)u}) rho_R(B_u). At k = 0 the hop is right multiplication by beta = eta = sum_u s_u [B_u] in Z[2O] | THEOREM (exact integer, 3 sign sets) | AGREE: H(0) = R_eta exact (+++); same k=0 table | AGREED (two codes) | m1_algebra.json; m2_l0_spectrum.json |
| U1-2 | The centre z = -1 splits L0 into V+/V- at every k. Right Q8 is the commutant among right multiplications. T_a vanish on V+; right H acts on V-. Right sectors eps, chi_i, chi_j, chi_k (V+) and H (V-) decouple at every k | THEOREM | AGREE (ports commute with every R_q, 4 sign sets) | AGREED | m1_algebra.json; m2_l0_spectrum.json |
| U1-3 | The real linear commutant of L0's ports has dimension 11 (+++) and 10 (1,-1,1) | THEOREM, exact rank (two primes) | AGREE, independently confirmed (primes 10007, 65537) | AGREED (two codes) | m1_commutant.json; m2_commutant_check.json |
| U1-4 | k=0 eigenvalues per irrep (both sign classes); zone edges by sector: trivial 6; chi_i 2sqrt5; chi_j,k 4.857; V- 5.0355 (+++) / 4.8412 (-1 class) | exact algebra + NUMERIC-float | AGREE; frustrated E = 2 +- 2sqrt3 by the same S3 algebra | AGREED | m1_irreps_*.json; m2_l0_spectrum.json, m2_l0_signs.json |
| U1-5 | THEOREM S: \|cos w\| = 1 anywhere iff s_y s_z = +1. The closed skew-hexagon relator (B_{+y}B_{-z})^3 = 1, with zero displacement, has sign holonomy s_y s_z. The -1 class has max \|lambda\| = 2+2sqrt3 | THEOREM (proof, ONE-M1 §1.3) | AGREE ("ONE-M1's proof is stronger than mine"); all 8 triples split by s_y s_z | AGREED | m1_relator.json, m1_frustr.json; m2_l0_signs.json |
| U1-6 | Plaquette signs of the vacuum frame connection: s_y s_z = sign(order-3 plaquettes) = sign(+90) x sign(-90). The -1 class separates the two screw senses | THEOREM (exact enumeration) | AGREE-WITH-QUALIFIER: +1 has 8 UNSIGNED inversion relabellings; -1 has 0 unsigned and 8 SIGNED with sign = A2 exactly. So the -1 vacuum is P-odd but P∘A2-even. Call it "chiral" only if the A2 grading is not itself a symmetry of the physics (HAND) | AGREED-WITH-QUALIFIER (ONE-M1 WITHDRAWS "two hands": (1,-1,1) and (1,1,-1) are related by the A2-sign gauge, ONE class) | m1_plaquette.json; m2_parity_signs.json |
| U1-7 | Q-scaling with ANY remainder offset: L0 at 3Q-1 (offset Q-1) is today's board bit for bit | THEOREM + NUMERIC (Q = 3, 7, 4095) | AGREE, found independently (Q = 1, 7, 51, 2^25+1; 12/12 vs universe24) | AGREED (two codes) | m1_mirror.json; m2_onevac.json |
| U1-8 | Mp (= R') is an exact reversor for every b-only coupling and fixes 3Q-1 iff Q is odd. With L0 at 3Q-1 the Q-lattice rule is unnecessary | THEOREM + NUMERIC (kappa = 1, LAP/HOP; rhoL0 control fails) | AGREE (R' exact 8+8 with fine coupling; rhoL0 fails) | AGREED (two codes) | m1_mirror.json; m2_onevac.json |
| U2-1 | Board->clock: Rule3/D = forced leapfrog, cos w = mu/2 = Hessian/D. Board->click: ell = floor((K+r)/D) = (2u + r - r')/D; kind = a J-sign. Click->clock: ell = 2cos w b | THEOREM (identities) | AGREE; general D: kind = sign of (r' - r) mod D in (-D/2, D/2]; u mod 3 is the D = 6 case | AGREED | ONE-M1 §2.1; ONE-M2 §2.1 |
| U2-2 | View-invariants: frequency ratios, causal order/cone, charges (O(1/A) in clicks), Born weights, the spectral class (massless vs gapped) | DERIVED | AGREE + M2-1 (click charge = 4cos^2 w x board charge) and Wilson loops | AGREED | m2_dictionary.json |
| U3-1 | (T1) Hop-form link weights on the closed flat board: lambda_max >= 6 mean(w); > 6 if mean >= 1 and node sums are uneven | THEOREM + NUMERIC-float | AGREE (multiplicative n = 1.125 on one link: blow-up t = 766) | AGREED | m1_edges.json; m2_lapse_static.json |
| U3-2 | (T2) Laplacian (shift-symmetric) form: lambda_max <= 6 for any w >= 0 | THEOREM + NUMERIC-float | AGREE (top exactly 6.000 for n in [0,1], [0.5,1], [0,1.3]) | AGREED | m1_edges.json; m2_lapse_spectrum.json |
| U3-3 | (T3) Schur: node sums of link norms <= 6 give \|lambda\| <= 6, so unitary holonomy, traceless shear and N <= 1 are safe. The doubler exists iff L is even | THEOREM + NUMERIC-float | AGREE; H_n >= 6 - 12 max n is the Schur case; one link n = 1.125 gives -6.0083 (L = 4) | AGREED | both |
| U3-4 | Dynamic scalar links: +++ HOP fails at every coupling. LAP survives at weak coupling, hits the doubler on even L at 1e-3, and collapses at >= 1 %. The -1 class survives in both forms at 1e-4..1e-3 | NUMERIC exact, 3 seeds | AGREE, independent toy with matching couplings: LAP bounded at g/Q = 5e-4 (2 seeds x 3000); doubler blow-up at 2e-3 (1024/1071); collapse at 3e-2 (273/274); HOP fails at every coupling, both signs (75–2598) | AGREED (two codes) | m1_dyn*.json; m2_metric_dynamic_g*.json |
| U3-5 | Dynamic quaternion c2 on L0 with fine links: the eps-free forms are stable on +++; the forms that carry the trivial character eps fail on +++ and hold on the -1 class | NUMERIC (amended 11:0x, see §3 row S1) | AGREE-WITH-QUALIFIER (refinement): on +++ the forbidden piece is EXACTLY eps, not V+ as a whole. AW (7 gears, chi's + H dynamic, eps ≡ A) is BOUNDED (3 seeds x 5000; seed 8 x 10,000); W8 (8 gears incl. eps, bit-exact local Q8) FAILS (91/139/200); on (1,-1,1) W8 is BOUNDED (3 seeds x 10,000). Coarse A = 63 fails in every form. ADDED 11:15 (30k per-sector run, m2_c2_sectorlog, seed 8): AW +++ blows up at t = 11651, W8 (1,-1,1) at t = 19376 (links). Their FROZEN controls are bounded to 30,000 but grow in EVERY sector ~ sqrt(t) (Rule3 rounding heating of generic data: frustrated triv 338/635/947, V- 667/1317/1919 at 3k/12k/27k); +++ adds the linear zero-mode drift (triv 1.4e6 at 27k). So the LATE failure is common to both classes (the bilinear drive grows with the heated L0 amplitude until it beats the fixed spring); the FAST failure (<= 200 updates) is the +++-only eps effect | AGREED-WITH-QUALIFIER (M2's refinement adopted: "eps is the forbidden piece") | §3 S1 table |
| U3-6 | (dalet) V- = quaternionic massive matter, the same type as compact-SU(2) matter, so gauge sharing is possible. Mixing L0 <-> Dirac pair needs a NEW LAW | THEOREM (algebra) + DERIVED | AGREE + M2-11 (U(1)_{J'}, fermion parity, L0-number rules; not the photon: A1 vs T1) | AGREED | both §3.2 |
| U3-7 | "48 = 48" is a coincidence: commutant 11 < 12; tr z 0 vs -48; second vs first order | THEOREM | AGREE (commutant independently confirmed) | AGREED (two codes) | m1_commutant.json; m2_commutant_check.json |
| U3-8 | Handed board: L0 = a neutral, massive, Kramers-paired species | DERIVED (with ONE-P1's X^2 = -1) | AGREE (same reading: "dark sector") | AGREED | ONE-M2 §3.2.4 |
| U3-9 | B1-EM's link-wave no-go stands within rank <= 4, B3, one divisor. eps of Z[Q8] can be frozen (linear); the radial \|U\|^2 of a simple algebra cannot | DERIVED | AGREE + NUMERIC strengthening (M2-9): even with NO radial mode the compact photon caps at ~0.21 | AGREED | m2_u1_*.json |
| U6-1 | N <= 1 everywhere = time gauge + positive energy + maximum principle + energy conservation: a principle plus one datum | DERIVED | AGREE + bound: max phi <= G E \|min g_L\|, \|min g_L\| ~ 0.064/L (L = 8..64) | AGREED | m2_shift_noether.json |
| U6-2 | The EP fixes the coupling form (LAP). HOP = LAP + a position-dependent mass term, tachyonic where w > 1 | DERIVED (exact identity) | AGREE (same conclusion via M2-8) | AGREED | — |
| U6-3 | Local Lorentz (c1) = rotation (Schur-safe) + scalar length (LAP); the c1 vacuum carries the sign class | DERIVED | AGREE-WITH-QUALIFIER (+ M2-12): in Einstein–Cartan the frame connection is slaved; its integer image rounds to the vacuum below ~45 deg per link. FIXED L0 frame links are the EC-consistent remnant; a propagating c1 is not EC | AGREED-WITH-QUALIFIER (M2's EC slaving adopted) | — |
| U6-4 | Bianchi <-> Board Noether: exact except the Hamiltonian constraint (dressed) | DERIVED | AGREE | AGREED | — |
| U6-5 | Einstein's symmetries do not select the sign class (a topological Z2) | THEOREM S | AGREE (+ the classes differ by P vs P∘A2, M2-4) | AGREED | — |
| D-1 | The reciprocal detector: the quantum = J_X of the joint U(1) iff Sym T_det(X, ., .) = 0; a \|psi\|^2 read records energy; exclusivity cannot come from OD4 | THEOREM (C1) + DERIVED | AGREE-WITH-QUALIFIER: reconciled. OD4 cannot give winner-take-all (c = 2a or 0; needs c > 2a: NEW LAW). Exclusivity = the REMAINDER LOCK (K1 = -K2 keeps r1 + r2 ≡ c exactly, also with reciprocal rank-3 back-action). The charge-flux input would make S = D Noether-exact: proposal, OPEN | AGREED-WITH-QUALIFIER (merged line in §3 S6) | ONE-M2 §6 |
| O-1 | Owner: ONE vacuum number 3Q-1 | APPROVE after re-tests | AGREE | AGREED (§4) | — |
| O-2 | Owner: the sign class | was "do not switch yet; pre-register a test" | PROPOSED JOINT LINE: the test is DONE; present the switch as the algebra side's preferred option, conditional on HAND's reading of P∘A2; otherwise +++ with V--only/AW c2 | AGREED: joint line in §3 S1 and §4 O2 (ONE-M1 joins M2's line after the two-code check). ONE-M2 ADDED 11:15: the 30k runs do not change the line (the class decides the FAST eps failure; the LATE failure at 1-2e4 is common to both classes and is a spring-capacity vs rounding-heating effect, see S1-a last row) | §3 S1 |

## 2. ONE-M2's extra rows, marked by ONE-M1
| id | claim (ONE-M2) | ONE-M2 label | ONE-M1 mark | verdict |
|---|---|---|---|---|
| M2-1 | Click charge = board charge dressed by H^2, per mode 4(mu/D)^2 = 4cos^2 w, parallel for every generator commuting with H: ONE factor (1.0176/1.014909) | DERIVED + NUMERIC (6e-6) | AGREE: the same identity as ONE-M1 §2.1 (W_X = Sum ell ell/(2cos w)^2 = J_X/D), with M2's number | AGREED |
| M2-2 | Board charges are integers: J^_X = J_X/D in Z, changing by integer remainder kicks | THEOREM | AGREE | AGREED |
| M2-3 | L0 (+++) has the exact uniform-shift symmetry; Noether: 6 Delta P = Sum(r - r'), P = Sum(b - a); it protects L0's light | THEOREM + NUMERIC (0/40 on universe24) | AGREE-WITH-QUALIFIER: exists exactly in the flat class (for +-- the shift pattern is chi_A2); the -1 class has no flat section (Theorem S) and no such shift | AGREED-WITH-QUALIFIER |
| M2-4 | Inversion relabellings: 8 unsigned iff s_y s_z = +1, else 8 signed with sign A2 | THEOREM (exhaustive) | AGREE; consistent with ONE-M1's plaquette signs and Theorem S | AGREED |
| M2-5 | AW register (7 gears, eps ≡ A, springs on chi_i, chi_j, chi_k, H): stable on +++; global Q8 bit-exact; local Q8 exact on Phi, not bit-exact | NUMERIC | AGREE. ONE-M1's further reduction (H form on V- only, 4 gears) is also bounded on +++: 15,000 updates at weak drive (m1_c2_weak) | AGREED |
| M2-6 | W8 (8 gears, bit-exact local Q8): fails on +++, bounded on (1,-1,1) at the frozen level | NUMERIC, pre-registered | AGREE, cross-checked twice. (a) ONE-M1 re-ran ONE-M2's own code (copied, pinned imports) to 15,000 updates: (1,-1,1) seeds 8/10/11 bounded (8/8/8 bits; frozen 8/7/7); +++ 91/139/200. (b) In ONE-M1's own code the eps-carrying form fails fast on +++ (t = 204, 164 at weak drive; 44 at strong drive) | AGREED (two codes) |
| M2-7 | EP for L0 is automatic: under the LAP factor n every k=0 level obeys sin(w'/2) = sqrt(n) sin(w/2), i.e. N^2 = n | THEOREM | AGREE (= ONE-M1 §2.1, M -> 2 - N^2(2 - M)) | AGREED |
| M2-8 | Reciprocity strengthens the sourcing term (+c^2 B^2/2(D - c_nu)); HOP pushes the light past the edge for either sign; LAP only softens gradients | DERIVED + NUMERIC | AGREE (it explains ONE-M1's T1 dynamics). Qualifier: under LAP the softening continues to n -> 0 and below at strong coupling (collapse, U3-4) | AGREED-WITH-QUALIFIER |
| M2-9 | Compact U(1) photon cap: 0.19 (both sectors stable), 0.21 (phase sector only) | NUMERIC-float | AGREE (not re-run by ONE-M1); consistent with ONE-M1 §3.3 | AGREED |
| M2-10 | Unit-group principle: Z4, Q8, Delta96 forced once the ring is Z[i]; 2O carried by permutations | THEOREM | AGREE; ONE-M1 withdraws "Z[omega] option" as a recommendation: it would be a second ring | AGREED |
| M2-11 | (dalet) selection rules: seeding needs a term linear in L0; U(1)_{J'} forbids bilinear mixing with charged matter; L0's massless mode is A1, not the photon's T1; Yukawa = NEW LAW + Brans–Dicke (gamma < 1) | THEOREM + DERIVED | AGREE; complementary to ONE-M1's 2O-vs-C4 and commutant arguments | AGREED |
| M2-12 | Einstein–Cartan: the spin connection is slaved; its 2O image rounds to the vacuum below ~45 deg per link; a propagating frame connection is not EC | DERIVED | AGREE | AGREED |
| M2-13 | N <= 1 for all t from ONE k=0 number: max phi <= G E \|min g_L\|, \|min g_L\| ~ 0.064/L; needs rho >= 0 | THEOREM (Newtonian) + NUMERIC | AGREE (= ONE-M1 §4.1, with M2's number) | AGREED |
| M2-14 | Even Q has NO R'-fixed remainder, so the Born router's even Q conflicts with the uniform vacuum; a channel-paired vacuum (R*) works for any Q | THEOREM | AGREE (checked: even-r fixed point needs 3Q-1 even, odd-r needs 3Q odd; both fail for even Q) | AGREED |
| M2-15 | The one-vacuum offset is REQUIRED for L0's EP coupling (lapse coefficients ∝ F/P not ≡ 0 mod Q, so rhoL0 cannot be exact; R' at 3Q-1 is) | THEOREM | AGREE | AGREED |

## 3. The manager's seven must-settle items
| # | item | joint line | evidence | status |
|---|---|---|---|---|
| S1 | **THE SIGN CLASS** (and which c2 form) | see the two tables and the joint line below | below | AGREED (joint line) |

**S1-a. The decisive two-code check** (manager 11:05: "the same c2 form on +++ vs (1,-1,1), long runs, both codes").
- "eps-carrying" means that the trivial right character eps of the link acts on L0's marginal sector: M2's W8 (8 gears,
  bit-exact local Q8) and M1's 'all' mode (the quaternion real part also multiplies the V+ hop).
- "eps-free" means: M2's AW (7 gears, eps ≡ A) and M1's H form on V- only (4 gears).
- Fine links in every run. Every M1 run had exact rewind at t = 100.

| form | code | +++ | (1,-1,1) |
|---|---|---|---|
| eps-carrying, bit-exact W8 | ONE-M2 (m2_c2_signed, m2_c2_headtohead; pre-registered) | blow-up t = 91 / 139 / 200 | BOUNDED, 3 seeds x 10,000, L0 = frozen level (7/8/8 vs 8) |
| eps-carrying, bit-exact W8, re-run to 15,000 by ONE-M1 (copied code, pinned imports; m2copy/) | ONE-M2's code | 91 / 139 / 200 | BOUNDED, seeds 8/10/11 x 15,000 (8/8/8 bits; frozen 8/7/7) |
| eps-carrying 'all' (H + real part on V+), weak drive (amp 3, A = 1093.5) | ONE-M1 (m1_c2_weak) | blow-up t = 204 / 164 | BOUNDED, seeds 8/10 x 15,000 (8 bits = frozen level) |
| eps-free AW | ONE-M2 | BOUNDED, 3 seeds x 5000, seed 8 x 10,000 (9 bits vs frozen 13) | BOUNDED (8 vs 8) |
| eps-free H on V-, weak drive | ONE-M1 (m1_c2_weak) | BOUNDED, seeds 8/10 x 15,000 (13–14 bits, the +++ zero-mode drift; M2's frozen +++ control 13 bits) | BOUNDED, seeds 8/10 x 15,000 (8 bits) |
| either form, STRONG drive (amp 30, amp/A = 0.08) | ONE-M1 (m1_c2_sector*) | eps-carrying: t = 44 (seed 10), 9529; eps-free: bounded to 10,000, blow-up 10,354 | both forms bounded to 10,000; blow-up 10,554 / 10,556 |
| LONG weak-drive runs with per-sector norms, 30,000 updates (seed 8; ONE-M2 m2_c2_sectorlog, pre-registered 11:10) | ONE-M2 | eps-free AW: blow-up t = 11,651 (links). Frozen control bounded, but every sector grows ~sqrt(t) and triv drifts linearly (1.4e6) | bit-exact W8: blow-up t = 19,376 (links), after tracking the frozen sectors to ~18,000 (V- 1916 vs 1632). Frozen control bounded; sectors ~sqrt(t) (V- 1919 at 27k) |

- **Reading (AGREED, two codes).**
  - The FAST failure of L0's internal links comes ONLY from eps acting on the marginal trivial sector of the +++ class.
  - Removing eps (AW, or H on V-) cures it on +++. Changing the class cures it with the bit-exact register.
  - The late failure at strong drive in ONE-M1's toy appears in BOTH classes and BOTH forms. It is a strong-drive effect
    (link norm excursions 0.9–1.2), not a sign-class effect.
  - ONE-M2's 30k runs (last table row) show the same late failure at WEAK drive: AW +++ at 11,651; W8 (1,-1,1) at 19,376.
    - Its source is common to both classes: the frozen boards themselves heat (every sector ~sqrt(t), from Rule3's
      rounding |eps| < 1 acting on generic data), so the link drive (bilinear in L0) grows until it beats the
      fixed spring.
    - It is NOT a sign-class effect.
    - OPEN: a spring/A scaled to the run length, or legal (seed-built, low-noise) data, as the production regime.
    - The zero-mode-free +++ rerun is running (m2_c2_zeromode).

**S1-b. The trade (for the owner).**
| | +++ (today) with an eps-free c2 (AW or H on V-) | the handed class s_y s_z = -1, e.g. (1,-1,1) |
|---|---|---|
| L0's links | metric links in Laplacian form (N <= 1); frame links fixed (EC); c2 stable, but local Q8 is exact only at the Phi level (AW) or only on V- (H) | the same metric/frame closure; c2 stable with BIT-EXACT local Q8 (the package's own 8-gear register) |
| light | L0 keeps a massless SCALAR (A1, one polarisation, not EM, not a graviton), on a cone differing from the field cone by O(1/Q) | ONE light: the field gears only (EM and gravity waves on the one cone c_Q) |
| L0 as a species | a light board with massive bands; its zero mode drifts on generic data (12–14 bits per 3000–15,000 updates) | a NEUTRAL, MASSIVE, KRAMERS species ("dark"): gapped (cos w <= 0.911), every mode ticks, bounded on generic data |
| parity | plain P (8 unsigned relabellings) | P broken, P∘A2 exact (8 signed relabellings, sign = A2) |
| other | — | B1-GRAV's EP mode W is exactly right (manager 11:10) |
| status | NUMERIC (two codes) | NUMERIC (two codes, pre-registered) |

**S1-c. JOINT RECOMMENDATION (ONE-M1 + ONE-M2).**
- The algebra side's PREFERRED option is the handed class (1,-1,1).
- It closes gap (vav) with the board's own bit-exact local symmetry, removes the duplicate light, and makes L0 a clean
  neutral dark species.
- It is a choice of tensor ENTRIES that today's engine already offers (examples/signed_impulse.json). It is not a new
  law, and the vacuum is unchanged.
- Conditions before switching the shipped default:
  - (a) the HAND pair's reading of P∘A2. Is the A2 grading a symmetry of the physics, in which case the "hand" is
    fictitious, though the closure stands?
  - (b) ONE-P's verdict that losing L0's scalar light costs nothing for Einstein or QM;
  - (c) the package's stage-1 run of the 8-gear c2 on (1,-1,1) (>= 2000 updates; Noether/Gauss and local covariance
    exact; L0 at the frozen level).
- FALLBACK if (a) or (b) fails: keep +++ with frame links fixed, metric links in Laplacian form with N <= 1, and an
  eps-free c2 (AW, or H on V-).
- ONE-M1's draft line "do not switch yet" is replaced by this joint line. The "test first" step is done in two codes;
  only (a)–(c) remain.

| # | item | joint line | evidence | status |
|---|---|---|---|---|
| S2 | ONE vacuum (3Q-1) | APPROVE. Re-test conditions: (i) package T0.1 bit for bit vs universe24 with the bridge r -> Qr + Q - 1; (ii) T0.15 with R' on ref.* (joint mirror exact, vacuum fixed); (iii) frozen_equivalence with the new offset; (iv) the seed builders re-check S2* and R* with L0 at 3Q-1. M2: R*'s JM keeps r, so it is offset-independent | U1-7, U1-8, M2-15 (two codes) | AGREED |
| S3 | (dalet) | CLOSED as "separate species, one universal coupling". It rests on: L0's commutant 11/10 < 12 (not colour x Dirac); U(1)_{J'} + fermion parity + L0-number parity forbid mixing and creation; L0's massless mode is A1, not the photon. The EP REQUIRES L0's metric coupling (L0 is gravity-blind today): Laplacian form, constant-free, half-angle law exact. In the handed class L0 is a neutral massive Kramers dark species | U3-6, U3-7, U3-8, M2-11, M2-7 | AGREED |
| S4 | (vav): which link form, on which sector, in which class | METRIC links: Laplacian (shift-symmetric) form, on ALL of L0, either class, N <= 1 (causal gauge). FRAME links: fixed (Einstein–Cartan slaving). INTERNAL (c2) links, optional: on +++ an eps-free form (AW: chi's + H; or H on V-); on the handed class the bit-exact 8-gear Z[Q8]. Always FINE links (S2). The hop form is excluded for metric links (EP) and for eps on +++ (T1). Dynamic status: weak coupling bounded in both codes; strong coupling meets the physical collapse (OD4 strong-field element) | U3-1..U3-5, U6-2, U6-3, S1 | AGREED ("closed in principle; dynamically at weak coupling"; the package L0 <-> h-gear run is OPEN) |
| S5 | The cone no-go | No escape within rank <= 4, B3 and one divisor. P0 != 0 is forced by covariance + the fixed point. The radial mode of a simple link algebra is quadratic (cannot be frozen; eps of Z[Q8] can). Even radial-free, the phase sector caps the photon at ~0.21. Exits (owner): a plaquette cell (third entity), an E1-like stencil, a second divisor. Physical reading: compact links carry the FORCES (exact Gauss, Newton III); light runs on the field gears (two speeds), unless the owner admits a plaquette entity | U3-9, M2-9 | AGREED |
| S6 | The reciprocal detector | (i) CONSERVATION: the quantum is the integer Noether charge J^_X of the joint U(1), exact up to integer remainder kicks iff Sym T_det(X, ., .) = 0. (ii) A reciprocal \|psi\|^2 read conserves psi's charge: it RECORDS, it does not absorb. (iii) OD4 springs cannot give winner-take-all (c > 2a needed; THEOREM): a +\|d1\|^2 \|d2\|^2 term would be a NEW LAW. (iv) EXCLUSIVITY = the REMAINDER LOCK: antitone inputs K1 = -K2 keep r1 + r2 ≡ c (mod D) exactly, also with reciprocal back-action Phi_det = g(d1 - d2) I(psi). It is an exact arithmetic invariant of the ledger, not a Noether charge. (v) ONE quantum <-> ONE click needs S = D: drive I = the flux of J^. OPEN: the exact current with back-action. GAIN if (v) closes: the \|psi\|^2 designations leave the algebra | D-1, ONE-M2 §6, ONE-M1 §6 | AGREED (v OPEN) |
| S7 | One merged U5/U8 list | §4 below | — | AGREED |

## 4. Merged U5 (ranked) and owner decisions
| rank | item | type | status / what closes it |
|---|---|---|---|
| 1 | ONE vacuum number (0,0,3Q-1); bridge r -> Qr + Q - 1; R' the one mirror; retire the Q-lattice rule | OWNER (data): APPROVE | THEOREM + NUMERIC (two codes); package re-tests S2 |
| 2 | The causal gauge N <= 1: the k=0 lapse constant from the conserved positive energy (max phi <= G E \|min g_L\|) | principle -> prepare/ datum | DERIVED + NUMERIC Green function; B1-GRAV testing |
| 3 | L0's universal metric coupling, Laplacian form (EP-REQUIRED; L0 is gravity-blind today) | EP-forced block, OWNER sign-off | build: L0 + h-gears dynamic, n <= 1, R' exact; strong-field end with OD4 |
| 4 | L0's frame links fixed (Einstein–Cartan) | principle | DERIVED; nothing to build; c1 retired |
| 5 | The sign class: the handed class preferred (S1-c) | OWNER + HAND + ONE-P | facts NUMERIC in two codes; conditions (a)–(c) |
| 6 | c2 on L0 (optional): eps-free on +++ (AW / H on V-); bit-exact W8 on the handed class; fine links | OWNER (optional) | NUMERIC, two codes, >= 10,000–15,000 updates at weak drive; strong drive OPEN |
| 7 | Compact U(1) as THE EM (one potential, Z[i]) | approved (zayin) | its build tests |
| 8 | Reciprocal detector pair: flux input + remainder lock | OWNER (S5-O1 revision) | OPEN: exact current with back-action |
| 9 | Proofs: the handed-class zone maximum 2+2sqrt3 for all k; V-'s 5.0355 in closed form | proof | NUMERIC-float now |
| 10 | Dirac matter on a 2O permutation module (one frame algebra; a handedness channel) | research (HAND) | OPEN |
| 11 | BLOCKER: reciprocal compact link forces on the ONE light cone | research / OWNER (two speeds / plaquette entity / E1) | OPEN (S5) |
| 12 | The Hamiltonian constraint exact | OWNER: accept "dressed" (recommended) | dressed identity |

U8 (every special choice): ONE-M2's §7.2 table is the joint table, with three additions from ONE-M1:
- L parity: even L carries the exact doubler k = pi; prefer odd L in dynamic-link tests.
- The spectral class: massless vs gapped, decided by s_y s_z.
- The coupling FORM of link weights: fixed by the EP (Laplacian) for metric links, and eps-free for c2 on +++.
And one agreed change: the SU(3) subgroup is Delta96, FIXED by the unit-group principle with Z[i] (M2-10). ONE-M1
withdraws the Z[omega] option.

| owner decision | joint recommendation |
|---|---|
| O1 one vacuum number 3Q-1 | APPROVE (re-tests S2) |
| O2 sign class | PREFER the handed class, under conditions (a)–(c); fallback +++ with an eps-free c2 (S1-c) |
| O3 L0's metric coupling (EP) | APPROVE for build and test |
| O4 c2 on L0 | optional; its form follows O2 |
| O5 the cone blocker | present the three exits (two speeds / plaquette entity / E1); no recommendation yet from the math pair |

## 5. Withdrawals and amendments recorded
- ONE-M1 withdraws:
  - "(1,-1,1) and (1,1,-1) are the two hands": they are one class, related by the A2-sign gauge;
  - "a parity-odd, torsion-like background": P∘A2 survives, and EC torsion couples to the P-even axial current;
  - the Z[omega] option for SU(3);
  - "do not switch yet": replaced by the joint line S1-c;
  - "V--only fine links close (vav) in the toy" at STRONG drive: they fail at ~10^4 in both classes there. At weak drive
    they are bounded to 15,000 in both classes.
- ONE-M2 revises "(vav) closed" to "closed in principle; dynamically at weak coupling" (manager's relay, 11:10).

## Signatures
- **ONE-M1: merged ONE-M2's column and extra rows, filled the seven must-settle lines and the two-code check table.
  AGREED with every row as written. SIGNED Tue Nov 10 11:13:32 UTC 2026 (`date -u`).**
- **ONE-M2: reviewed the whole merged file: §1 (my cells correctly quoted from ONE-M2_AGREE_COLUMN.md), §2 (ONE-M1's
  marks on M2-1…M2-15; I accept both qualifiers, M2-3 'flat class only' and M2-8 'collapse at strong coupling'), §3
  S1–S7, §4, §5. AGREED with every row as written. Added at 11:15, with no verdict changed: the 30k per-sector results
  in U3-5, O-2 and S1-a (late failure common to both classes = rounding heating vs a fixed spring; the class decides
  only the FAST eps failure). I note the owner's reading of the handed L0 as DARK MATTER with audit-only clicks
  (OD1); it is consistent with U3-8/D6. The zero-mode-free +++ rerun (m2_c2_zeromode) will be appended as a
  note. CO-SIGNED Tue Nov 10 11:15:21 UTC 2026 (`date -u`).**
- ONE-M2 NOTE appended Tue Nov 10 11:16:10 UTC 2026 (`date -u`), verdicts unchanged: the zero-mode-free +++ rerun (m2_c2_zeromode,
  pre-registered 11:14) blew up at 11,828 (vs 11,651). Its FROZEN control, started with zero-mode charges = 0, still
  drifts: trivial sector 23 → 2.0e6 at 24,000.
  - The marginal zero mode is re-fed by Rule3's rounding, i.e. the remainder term of its own Noether identity
    6ΔP = Σ(r − r′). So an excited +++ board drifts without bound whatever its initial data.
  - The handed class has no marginal mode: only the ~sqrt(t) heating common to both classes.
  - This supports S1-c (one more cost of +++), and does not change any verdict.
