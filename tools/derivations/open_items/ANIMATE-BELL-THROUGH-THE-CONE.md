# Bell at a distance through the cone (Animate's draft, under derive/PROTOCOL.md, steps 1 to 4)

The owner's word to Animate, 2026-10-28, 11:3x UTC (Hebrew, translated): "Try to get Bell at a distance with the cone and the time reversal. There was already a local solution to it because of the time reversal. Reach a solution with the 24 operations, the tensor and the clocks. And the detectors that were already entangled."

It builds on draft D (derive/D/DERIVATION.md: the four parts sigma_ab = N(det[phi_A^a, phi_B^b]), Born's singlet at the two ends of one Mesh, P1 to P12) and on BC-F1 (The-Bell-Bound-Through-The-Cone_COMPARISON.md, 2026-10-26). The probe is ANIMATE-PROBES-1/bell_cone.py, and its output is bell_cone.txt. Every claim is marked PROVED, CHECKED or OPEN.

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
- **Bell's theorem holds, and the control shows where.** Its premise is that the hidden variable's distribution does not depend on the settings (draft D, P11). That premise fails here by design: the pair drawn at the fitting depends on both frames. Where a setting changes after the fitting, outside its cone, the same rule gives S = -82/24389, inside the bound.
- **The time reversal** carries back a setting chosen after the fitting. OPEN (part 3, iii).

## 1. The formula (step 1)

- **At the fitting** (the Mesh where the pair is set; the detectors' frames phi_A at its A end and phi_B at its B end, as the cone brings them):
  - the four parts are sigma_ab = N(det[phi_A^a, phi_B^b]), with phi^+ = phi and phi^- = (-conj(phi_2), conj(phi_1));
  - the draw c in [0, room) by Rule3 picks (a, b) by the running sums (law 6 on four parts, draft D 2.1).
- **The children's lay:** the A child is set to chi_A = k phi_A^a and the B child to chi_B = k phi_B^b, with k the pair's amplitude.
- **The far click** (law 6 at the detector): the two parts are N(<phi_X^+, chi_X>) and N(<phi_X^-, chi_X>). One of them is 0, so it is a click of a whole.
- **What it holds:** Gaussian products, sums and Rule3. No root, angle, table, clamp or number beyond 0 and 1. Draft D 2.3 has the count.

## 2. The proofs (step 2)

- **P-a, the far click is whole.** By draft D's P3, <phi^-, phi^+> = 0. So N(<phi_X^(-x), k phi_X^x>) = 0, and the detector reads x. PROVED. CHECKED: every draw of the four setting pairs.
- **P-b, the joint odds are the singlet's.** Draft D's P6: 2 sigma_ab = rho_A rho_B - a b m_A . m_B, so E = -m_A . m_B / (rho_A rho_B). PROVED. CHECKED: four of four exact.
- **P-c, no signalling.** For every phi_B, sigma_a+ + sigma_a- = rho_A rho_B (Lagrange), so P(a) = 1/2. PROVED. CHECKED: 1/2 at every pair.
- **P-d, locality.** Every act reads one Mesh:
  - the frames come to the fitting inside its past cone;
  - the children go to the detectors inside its future cone, at most one Mesh a tick;
  - the far clicks read their own Node-clock.

  PROVED by construction, given the carriage of OPEN (i).
- **P-e, the 24.** det is the A1 part under 2O, the double cover of the 24 (draft D's P9). So the four sizes are invariant under any element acting on all four spinors, and the setting pair's odds hold in every image. PROVED by P9.
- **P-f, the control.** A frame at the fitting that is not the far detector's (a setting changed after the fitting) leaves the far click a local split by the detector's own sizes. Then each answer is a function of its own end's state, and |S| <= 2 (draft D's P11). PROVED. CHECKED: S = -82/24389.
- **Mutants** (step 3: each must fail):
  - the perp without its sign: S = -18522/35989;
  - the perp without the conjugates, on frames off the real plane: S = -18522/35989 (on real frames the conjugate is invisible);
  - det with the plus sign: S = -2/29.

  All fail. CHECKED.

## 3. Owed, by name (OPEN)

- **(i) The frames' carriage.** Which train carries a detector's frame, two Gaussian integers, to the fitting through the cone, intact? How does each end of the fitting's Mesh read the frame from its own side?
  - The one formula adds what arrives (draft D 4.1). A frame carried as a wave arrives spread and mixed with others.
  - This is the crux.
- **(ii) Line 102** ("a rule that supplies an outcome from a stored answer and a setting is the phenomenon put in"). The frames here are physical state carried by a train, and the outcome comes from law 6's sizes on the composite, the general click of a split. That reading is Sofer's law check to give.
- **(iii) The time reversal** (the owner's word). A frame set after the fitting is carried back to the fitting's Mesh by the reversed run after a turnover, and the next bang's fitting splits against it.
  - It needs the course's recurrence (draft C: the rate chain's zero) and the frames standing across the turnover.
  - Until then, settings chosen outside the fitting's cone stay under Bell's bound (P-f).
- **(iv) The rewind of the fitting's split.** The click of a split is many to one. Where the erased amplitude stays is the physicist's item and draft D's open.
- **(v) Nature.** Experiments choose settings after the emission, at spacelike separation, and from distant sources. A mechanism of the common past alone does not meet them; with (iii) it may. The plan says this plainly.

## 4. What it replaces (step 4)

- Section 18, item 4 and section 30's "Bell at a distance stands as a contradiction" become:
  - Bell at a distance through the cone: shown wherever the detectors' frames stand in the fitting's cone (the owner's entangled detectors);
  - a contradiction only for settings outside that cone, until (iii) is derived.
- Row 56's gate reads three things:
  - where the detectors' frames stood at the fitting;
  - the clicks' separation;
  - S in the band 4 < S^2 <= 8.

---
Animate, reader-5.
