# Bell at a distance through the cone (Animate's draft, under derive/PROTOCOL.md, steps 1 to 4)

The owner's word to Animate, 2026-10-28, 11:3x UTC (Hebrew, translated): "Try to get Bell at a distance with the cone and the time reversal. There was already a local solution to it because of the time reversal. Reach a solution with the 24 operations, the tensor and the clocks. And the detectors that were already entangled."

It builds on draft D (derive/D/DERIVATION.md: the four parts sigma_ab = N(det[phi_A^a, phi_B^b]), Born's singlet at the two ends of one Mesh, P1 to P12) and on BC-F1 (The-Bell-Bound-Through-The-Cone_COMPARISON.md, 2026-10-26). The probe is ANIMATE-PROBES-1/bell_cone.py, and its output is bell_cone.txt. Every claim is marked PROVED, CHECKED or OPEN.

Part 1a answers line 102: Sofer's law check of draft D at L = 1 (6467734998, item 3) and D's verifier (TENSOR24.md, 11 d: "REFUTED"). Both found the four parts a function of the two settings alone, the singlet put in.

## 0. The answer

- **Locally, by the one route Bell's theorem leaves open.** The detectors' frames are not free of the pair: they stand in the fitting's past cone. The owner calls these detectors already entangled: every Node-clock shares the one seed with every other, and the exact rewind keeps that shared root bit for bit (BC-F1).
  - So the pair's one click of a split happens at the fitting, at the two ends of one Mesh, against both detectors' frames. Draft D proved that act local (its part 3, L = 1).
  - Each child carries its taken sense to its detector, one Mesh a tick.
  - Each far detector's click is then a click of a whole: it reads the answer the fitting drew, at any tick, however far apart the two clicks are.
- **CHECKED exactly, every draw number counted** (bell_cone.txt, at draft D's settings: a = (1, 0), a' = (1, 1), b = (5, 2), b' = (5, -2)):
  - E is the singlet's at all four setting pairs: -21/29, -21/29, -20/29 and +20/29;
  - S = -82/29, with S^2 = 6724/841: above 4 and at most 8, Tsirelson's band;
  - every far click is a click of a whole: 58 of 58 and 116 of 116 draws;
  - no signalling: A's odds are 1/2 at every setting pair;
  - frames off the real plane (y and z axes) give S = -82/29 too.
- **Line 102 is answered by law 6 itself** (part 1a). The four parts are law 6 on the pair's composite state laid at the fitting: the same overlap law 6 takes on one hand, with nothing typed for Bell.
  - The 24 fix k epsilon alone among the two-spinors. So a lay that keeps the kind of an A1 parent lays the singlet with no declaration.
  - The rule reads the state, so its -82/29 can fail. With a T1 state laid, the same frames give 2/29, 82/29 and -2/29. With any product state laid, |S| <= 2. The owner's "from the twins' state", read as two product states, gives D's -82/87.
- **Bell's theorem holds, and the control shows where.** Its premise is that the hidden variable's distribution does not depend on the settings (draft D, P11). That premise fails here by design: the pair drawn at the fitting depends on both frames. Where a setting changes after the fitting, outside its cone, the same rule gives S = -82/24389, inside the bound.
- **The time reversal** carries back a setting chosen after the fitting. OPEN (part 3, iii).

## 1. The formula (step 1)

- **At the fitting** (the Mesh where the pair is set; the detectors' frames phi_A at its A end and phi_B at its B end, as the cone brings them):
  - the four parts are sigma_ab = N(<phi_A^a (x) phi_B^b, Psi>), with phi^+ = phi and phi^- = (-conj(phi_2), conj(phi_1)), and Psi the pair's composite state laid at the fitting (part 1a);
  - where Psi = k epsilon, the A1 state, this is draft D's sigma_ab = N(k) N(det[phi_A^a, phi_B^b]);
  - the draw c in [0, room) by Rule3 picks (a, b) by the running sums (law 6 on four parts, draft D 2.1).
- **The children's lay:** the A child is set to chi_A = k phi_A^a and the B child to chi_B = k phi_B^b, with k the pair's amplitude.
- **The far click** (law 6 at the detector): the two parts are N(<phi_X^+, chi_X>) and N(<phi_X^-, chi_X>). One of them is 0, so it is a click of a whole.
- **What it holds:** Gaussian products, sums and Rule3. No root, angle, table, clamp or number beyond 0 and 1. Draft D 2.3 has the count.

### 1a. The four parts as law 6 on the composite (line 102)

- **Law 6 on one hand** (the plan's K6, "up where c (rho + rho) rho_d < room (rho rho_d + S . m)") is the overlap's size. Its two parts are N(<phi_d^+, psi>) = (rho_d rho + m . S) / 2 and N(<phi_d^-, psi>) = (rho_d rho - m . S) / 2 (Fierz; draft D's P3 and P4). CHECKED: 389,376 of 389,376 pairs (6a).
- **On two hands it is the same law.**
  - The state is a two-index Gaussian tensor Psi_ij, and the frame is the product frame phi_A^a (x) phi_B^b.
  - The four parts are sigma_ab = N(sum_ij conj(phi_A^a_i) conj(phi_B^b_j) Psi_ij): the same overlap and the same Rule3 pick.
  - The four joint senses are orthogonal, so the parts sum to rho_A rho_B |Psi|^2 (Lagrange).
- **The state laid is the parent's, through the 24.** The 24, lifted to 2O, turn two spinor indices as Psi to M Psi M^T.
  - Under the three generators, the two-spinors with M Psi M^T = det(M) Psi have real dimension 2: they are k epsilon alone (exact elimination, 6b). The symmetric part, T1, holds none. This is Schur's lemma, draft D's P9.
  - So a lay that keeps the 24 (the one formula's acts commute with them) takes an A1 parent to k epsilon, with k the parent's amplitude. On k epsilon the rule is the closure's det form part for part: CHECKED, 32 of 32 (6c).
  - A T1 parent of polarization n lays k (n . sigma) epsilon. A lay that does not keep the kind lays a mixture.
- **The rule reads the state.** Sofer's "a function of the two settings alone" holds for the A1 state: it has no direction to hold, so only the frames vary, as in nature's singlet. The function itself reads Psi, and with another state laid the same frames give other numbers (6d):

  | the state laid at the fitting | S at draft D's settings |
  |---|---|
  | A1, k = 1 and k = 2 + i (the singlet) | -82/29 |
  | T1 along x | 2/29 |
  | T1 along y (E = +m_A . m_B on these frames) | 82/29 |
  | T1 along z (the closure's plus-sign mutant) | -2/29 |
  | the product z+ (x) z- (equal to A1 beside T1 z) | -42/29 |
  | the product x+ (x) x- | -40/29 |
  | the product y+ (x) y- | 0 |
  | chi(n) (x) chi(-n) over the six Spoke directions, each a sixth | -82/87 (draft D's P10) |

  So the -82/29 is no closed form put in: law 6 reads it only where an A1 state was laid. Every product reads |S| <= 2, as P11 requires.
- **Where the correlation lives** (line 102's last sentence, the owner's "from the twins' state").
  - The click writes the taken joint sense phi_A^a (x) phi_B^b, a product, so each child holds its own hand at its own Node-clock.
  - The correlation lives in those two hands, and the far clicks of a whole read it across the Meshes.
  - No answer is stored as a bit, and no setting is read by any rule but law 6.
- **Where the state is held during the fitting:** the parent's amplitude k, at the fitting's Mesh. The act reads k and the two frames at the Mesh's two ends: one act on one Mesh (L = 1).
- **What stays owed:** the lay itself, that the fitting takes an A1 parent to k epsilon by the one formula. That is draft E's check (the Boss's item 0 of 6467729194: "a fitting that keeps the kind lays the A1 part"), and open item 11 e (no twin train in the one big bang's calibre).

## 2. The proofs (step 2)

- **P-a, the far click is whole.** By draft D's P3, <phi^-, phi^+> = 0. So N(<phi_X^(-x), k phi_X^x>) = 0, and the detector reads x. PROVED. CHECKED: every draw of the four setting pairs.
- **P-b, the joint odds are the singlet's.** Draft D's P6: 2 sigma_ab = rho_A rho_B - a b m_A . m_B, so E = -m_A . m_B / (rho_A rho_B). PROVED. CHECKED: four of four exact.
- **P-c, no signalling.** For every phi_B, sigma_a+ + sigma_a- = rho_A rho_B (Lagrange), so P(a) = 1/2. PROVED. CHECKED: 1/2 at every pair.
- **P-d, locality.** Every act reads one Mesh:
  - the frames come to the fitting inside its past cone;
  - the children go to the detectors inside its future cone, at most one Mesh a tick;
  - the far clicks read their own Node-clock.

  PROVED by construction, given the carriage of OPEN (i).
- **P-e, the 24.** det is the A1 part under 2O, the double cover of the 24 (draft D's P9). So the four sizes are invariant under any element acting on all four spinors, and the setting pair's odds hold in every image. PROVED by P9. CHECKED on the composite (6f): the A1 state's four odds stand with both frames turned by each generator, 12 of 12. A T1 state's odds stand when the state turns too, 36 of 36, and move when it does not, 16 of 36.
- **P-f, the control.** A frame at the fitting that is not the far detector's (a setting changed after the fitting) leaves the far click a local split by the detector's own sizes. Then each answer is a function of its own end's state, and |S| <= 2 (draft D's P11). PROVED. CHECKED: S = -82/24389.
- **P-g, line 102: the rule reads the state.** Each piece is PROVED:
  - one hand: Fierz, so law 6 is the overlap's size;
  - the A1 part: Schur, so the 24 fix k epsilon alone;
  - no signalling for every state laid: the sum over b of sigma_ab is rho_B times the sum over j of N(<phi_A^a, Psi_.j>), Psi's columns, whatever B's frame (Parseval);
  - every product: its parts factor, so its answers are local and |S| <= 2 (P11).

  CHECKED (6a to 6e):
  - 389,376 one-hand pairs;
  - the fixed space of real dimension 2;
  - 32 of 32 parts equal to the det form;
  - the table above;
  - A's odds move with B's frame in 0 of 3,885 cases: 1,295 states with entries in {0, 1, -1, i, 1 + i, 2 - i}, three A frames, four B frames.
- **Mutants** (step 3: each must fail):
  - the perp without its sign: S = -18522/35989;
  - the perp without the conjugates, on frames off the real plane: S = -18522/35989 (on real frames the conjugate is invisible);
  - det with the plus sign: S = -2/29. It is the T1 state along z, laid in place of A1;
  - the second index turned as a conjugate spinor (M Psi M^dagger): the 24 then fix the identity in place of epsilon, and laid at the fitting it gives S = 82/29 (6g).

  All fail. CHECKED.

## 3. Owed, by name (OPEN)

- **(i) The frames' carriage.** Which train carries a detector's frame, two Gaussian integers, to the fitting through the cone, intact? How does each end of the fitting's Mesh read the frame from its own side?
  - The one formula adds what arrives (draft D 4.1). A frame carried as a wave arrives spread and mixed with others.
  - This is the crux.
- **(ii) Line 102.** Answered in part 1a and P-g, for Sofer's law check. What it leaves owed:
  - the lay (draft E): that the fitting takes an A1 parent to k epsilon by the one formula;
  - that law 6 on two hands is the law's own click of a split and no new act, which is the law's word to give.
- **(iii) The time reversal** (the owner's word). A frame set after the fitting is carried back to the fitting's Mesh by the reversed run after a turnover, and the next bang's fitting splits against it.
  - It needs the course's recurrence (draft C: the rate chain's zero) and the frames standing across the turnover.
  - Until then, settings chosen outside the fitting's cone stay under Bell's bound (P-f).
- **(iv) The rewind of the fitting's split.** The click of a split is many to one. Where the erased amplitude stays is the physicist's item and draft D's open.
- **(v) Nature.** Nature's Bell tests choose settings after the emission, at spacelike separation, and from distant sources. A mechanism of the common past alone does not meet them; with (iii) it may. The plan says this plainly.

## 4. What it replaces (step 4)

- Section 18, item 4 and section 30's "Bell at a distance stands as a contradiction" become:
  - Bell at a distance through the cone: shown wherever the detectors' frames stand in the fitting's cone (the owner's entangled detectors);
  - a contradiction only for settings outside that cone, until (iii) is derived.
- Section 11 d's "Derived: REFUTED" at L = 1 (the verifier, on line 102) becomes: law 6 on the composite state laid at the fitting, with the A1 state from the 24 for an A1 parent (part 1a). The lay itself stays owed to draft E.
- Row 56's gate reads four things:
  - where the detectors' frames stood at the fitting;
  - the clicks' separation;
  - the state laid at the fitting, by its kind;
  - S in the band 4 < S^2 <= 8.

---
Animate, reader-5.
