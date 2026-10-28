# Draft D: the closure of the split (Bell)

For the Boss's Tensor24 (TENSOR24.md sections 11 (d), 18 items 2 and 4, 19 law 6 and its owed list, 24 item 3, 25 item 10, 27). Drafted under the derivation protocol (derive/PROTOCOL.md), 2026-10-28. Read on: the t24 worktree (engine-5.0-test 22149d2b2: bobs.py `splits`, draw.py `vernier`, click.py, core/acts.py); David's DAVID-TENSOR24-THE-CLICK.md and its _CHECKS.txt (toys-5 1cadb3931); DAVID-THE-BELL-LOCAL.patch (toys-5, where `bell_turn` stands); probes/fierz24.py; scribe-5's docs/ALGEBRA.md (bcc1f006b), lines 33, 92, 102 and 1169. The probes and their outputs are in this folder (part 6). Every claim is marked PROVED (with its proof), CHECKED (with the probe's count) or OPEN.

## The answer in short

1. **The closure's formula follows from the tensor's algebra and the click in general.** It is one click of a split held at the pair's two ends, with four parts, one per pair of senses: sigma_ab = N(det[phi1^a, phi2^b]), det the A1 part of two twin pairs. Read in two steps, the first click is half and half by Lagrange's identity, and the partner's click is law 6 on the reading (rho1, -a m1): David's closure, exactly. PROVED; CHECKED (part 3).
2. **The "open axis" (S = 0) is no twin pair's reading.** One twin pair has S . S = rho rho, and David's two-time reading has S . S - W W = 4 N(det[now, before]) >= 0. So the fitting cannot set it; the two-step form above does not need it. PROVED; CHECKED.
3. **At the two ends of one Mesh (L = 1) the closure is one act on the Mesh**, local, with no carriage: S = -82/29 = -2.8275 with every draw counted, -2.8270 on 8,000 vernier draws. PROVED and CHECKED, under one premise left OPEN: that the pair's split reads the A1 part of its two fitted hands.
4. **At L >= 2 the one formula cannot carry the closure.** The partner's click must read the first click's taken sense, four integers made at another Node-clock. The one formula is linear in the gears, so whatever arrives is added to the partner's own hand and does not replace it. What a click changes is the taken sense (axis +a m1), the opposite of the closure. Where the closure's own axis does arrive (the remainder alone, at an empty partner), it holds less than one winding and cannot click. On the probe, the one formula's own carriage gives S from -0.96 to +2.80 timelike, never the singlet's -2.83, and it signals: B's marginal moves with A's setting by up to 0.44. So the closure at a distance needs a carriage of its own (part 4.6), which the decision of section 24 item 3 forbids. PROVED; CHECKED.
5. **Bell.** The engine is local (one Mesh a tick) and deterministic (the draw reads the state). For clicks L Meshes apart, with the partner's click fewer than L - 1 ticks after the first, no rule of the engine gives |S| > 2. That covers the one formula, any click, any closure and any carriage. It holds where the settings are free and every pair is counted. Nature gives 2 sqrt 2 there. On the probe, where the first click writes the gears (the one formula's own carriage, M2), B's answer, draw and reading never moved with A's setting there (0 of 40,000 runs per train), and every model gave |S| <= 0.981. Inside the cone, a carriage gives S = -2.769 to -2.876 (exact -2.8275). The contradiction of section 18 item 4 cannot be removed by any derivation while the law's locality stands. PROVED; CHECKED.

## 1. The words, the state, the operations

- **A twin pair** at a Node-clock: psi = (psi1, psi2), the up twin's hand and the down twin's hand, each a Gaussian integer (three + i twelve). **Its reading** (law 6): rho = N(psi1) + N(psi2), S = (2 Re, 2 Im of conj(psi1) psi2, N(psi1) - N(psi2)), with N(x + i y) = x x + y y.
- **A detector:** a second twin pair phi standing at the Node-clock, with reading (rho_d, m). **Its two senses:** phi^+ = phi, and phi^- = phi_perp = (-conj(phi2), conj(phi1)). The perp is an exchange, two conjugations and a sign; it holds no product.
- **The overlap** <phi, psi> = conj(phi1) psi1 + conj(phi2) psi2. **The A1 part of two twin pairs:** det[u, v] = u1 v2 - u2 v1, the product table's A1 row for two spinors (epsilon; P9).
- **The draw** (law 9): its number c in [0, room). **The click of a split** (law 6; section 27): parts of sizes sigma_k. Rule3 gives c (sum of sigma) = t room + r, and the part in whose running sum t falls takes the whole winding.
- **The pair:** two fitted hands of one fitting, set at the two ends of a Mesh. Here they are L Meshes apart along an axis when they click; L = 1 is where they were set. The first click is at A at tick t_A with detector phi1 (rho1, m1) and answer a. The partner's click is at B at tick t_B with phi2 (rho2, m2) and answer b, where a, b are in {+1, -1}. Delta = t_B - t_A.
- **The readings of a run:** E = the mean of a b over the pairs, and S = E(a,b) + E(a,b') + E(a',b) - E(a',b').
- **The settings of the probes:**

  | setting | twin pair | axis | rho |
  | --- | --- | --- | --- |
  | a | (1, 0) | z | 1 |
  | a' | (1, 1) | x | 2 |
  | b | (5, 2) | (20, 0, 21) | 29 |
  | b' | (5, -2) | (-20, 0, 21) | 29 |

  The axes are Pythagorean (20 x 20 + 21 x 21 = 29 x 29), so no root enters. The singlet gives E = -21/29, -21/29, -20/29 and +20/29, so S = -82/29 = -2.8275. Since S S = 6724/841 <= 8 = 6728/841, this is just under Tsirelson's bound. The local value is S = -82/87 = -0.9425 (P10). Bell's bound is |S| <= 2.

## 2. The formula (protocol step 1)

### 2.1 The pair's split on its A1 part

The pair's whole is shared among four parts, one for each pair of senses (a, b). With Phi = [phi, phi_perp], the 2 x 2 matrix of a detector's two senses, the four sizes are the norms of the entries of one contraction:

    sigma_ab = N( (Phi1^T epsilon Phi2)_ab ) = N( det[phi1^a, phi2^b] )

The draw c in [0, room) gives Rule3: c (sigma_++ + sigma_+- + sigma_-+ + sigma_--) = t room + r. The pair (a, b) whose running sum first passes t takes the whole. Each comparison is Rule3's quotient (the plan's indicator 1 - 1 div (q + 1)). By P6, 2 sigma_ab = rho1 rho2 - a b m1 . m2, so E = -m1 . m2 / (rho1 rho2): Born's singlet.

### 2.2 The same split in two steps: the first click, then the partner's

By P7 the same odds come from two clicks:

- **the first click, at A:** two parts, each the sum of its row, sigma_a+ + sigma_a- = rho1 rho2 (Lagrange). In law 6's form, up where c (rho1 rho2 + rho1 rho2) < room rho1 rho2: half and half by the sizes themselves;
- **the partner's click, at B:** law 6 on the partner's reading (N(tau), S(tau_perp)) = (rho1, -a m1), with tau = phi1^a the first click's taken sense:

      up where  c (rho1 + rho1) rho2 < room (rho1 rho2 - a m1 . m2)

This is David's closure (11 (d)) letter for letter: the partner's reading becomes (rho1, -a m1). By P5 it is also the axis of the first split's remainder, the part not taken. In this form the "open axis" is no reading that the fitting writes. It is the statement that the A1 part's two rows are equal.

### 2.3 Its count in the three operations

- **The parts.** The perp of each detector costs no product. Each det costs two Gaussian products and one subtraction (8 integer products, 6 additions), and each N costs 2 products and 1 addition. The four parts hold 40 integer products and about 28 additions.
- **The pick.** One Rule3 on c times the parts' sum, then three running sums compared with t, each comparison a quotient.
- **In two steps.** rho1 = N(tau) takes 4 products. m1 . m2 = S(phi1) . S(phi2): each S is one Gaussian product and two norms, and the dot is three products. The partner's law 6 takes 4 more products and one Rule3 comparison.
- **What it holds.** No root, angle, cosine, table or clamp, and no loop that makes a formula (the four parts are one contraction). No number beyond 0 and 1: the senses are +1 and -1. The four parts are the two senses at each end, the twin train's own two hands.

## 3. The proofs (protocol step 2)

Counts are from closure24_algebra.txt unless named.

- **P1, Lagrange: S . S = rho rho.** S . S = 4 N(conj(psi1) psi2) + (N1 - N2)^2 = 4 N1 N2 + (N1 - N2)^2 = (N1 + N2)^2. So S = 0 only where rho = 0. PROVED. CHECKED: 20,625 runs (exhaustive in [-2, 2]^4, then 20,000 random up to 10^6), 0 failures.
- **P2, the two-time reading: S . S - W W = 4 N(det[now, before]) >= 0.**
  - David's reading from the slots: D_ac = i (conj(b_a) n_c - conj(n_a) b_c), W = D_uu + D_dd, S = (2 Re D_ud, -2 Im D_ud, D_uu - D_dd).
  - Write D = i (u v^H - v u^H), with u = conj(before) and v = conj(now). Then det(u v^H - v u^H) = |u|^2 |v|^2 - |u^H v|^2.
  - So S . S - W W = -4 det D = 4 (rho(now) rho(before) - N(<now, before>)) = 4 N(det[now, before]), the last step by Lagrange.
  - Hence S = 0 forces W = 0. PROVED.
  - CHECKED: 26,561 runs, 0 failures. 321 readings with S = 0 met in the exhaustive set, all with W = 0.
  - **Consequence:** "the fitting sets the open axis on both fitted hands (S = 0)" names a reading that no fitted hand's gears hold, in either form. It would be stored state.
- **P3, the perp.** N(phi_perp) = N(phi), S(phi_perp) = -S(phi), (phi_perp)_perp = -phi (the half-spin sign), and <phi_perp, phi> = 0, each by expanding. PROVED. CHECKED: 20,000, 0 failures.
- **P4, the A1 part and Fierz.** det[u, v] = <u_perp, v> exactly. By Fierz (fierz24.py: rho rho_d + S . m = 2 N(<phi, psi>)) applied to u_perp: 2 N(det[u, v]) = rho_u rho_v - S_u . S_v. PROVED. CHECKED: 20,000, 0 failures.
- **P5, the split's remainder.** {phi, phi_perp} are orthogonal with equal norms, so N(phi) psi = <phi, psi> phi + <phi_perp, psi> phi_perp exactly.
  - When the answer is a, the taken part is <phi^a, psi> phi^a and the remainder (the part not taken) is <phi^(-a), psi> phi^(-a).
  - Since S(c eta) = N(c) S(eta) and S(phi^(-a)) = -a m, the remainder's axis is -a m, whatever psi was, wherever the remainder is not 0.
  - PROVED. CHECKED: 60,000, 0 failures. The owner's sentence "its remainder ..." is exact for the axis: the closure's reading has the remainder's axis.
- **P6, the joint sizes.** By P3 and P4, 2 sigma_ab = rho1 rho2 - (a m1) . (b m2). Then:
  - the sum over b of sigma_ab is rho1 rho2;
  - the sum of all four sigma is 2 rho1 rho2;
  - the sum of a b sigma_ab is -2 m1 . m2;
  - so E = -m1 . m2 / (rho1 rho2), and every sigma >= 0 since it is a norm.

  PROVED. CHECKED: 20,000 random detector pairs, 0 failures.
- **P7, the two steps.** The first step picks a at rho1 rho2 / (2 rho1 rho2) = 1/2. The partner's law 6 on (rho1, -a m1) against (rho2, m2) has parts (rho1 rho2 -/+ a m1 . m2) / 2 = sigma_a+ and sigma_a-. PROVED. CHECKED: 400 random detector pairs, every draw of both forms counted, 1,600 cells, 0 failures. Control: the partner's reading (rho1, +a m1) fails 788 times.
- **P8, the closure needs no open axis.** If the partner reads (rho1, -a m1), then E = sum over a of P(a) a (-a m1 . m2 / (rho1 rho2)) = -m1 . m2 / (rho1 rho2) for every first-click odds P(a). So the first click may read its own fitted hand, by Born against its own axis n. After averaging over a hidden n in which n and -n come alike (the six Spoke directions sum to 0), the joint odds are the singlet's. PROVED. CHECKED as model M1b in part 5.3: S from -2.876 to -2.769.
- **P9, the A1 part is the singlet: the tensor's algebra.** u (x) v - v (x) u = det[u, v] epsilon, so the antisymmetric part of two twin pairs is the singlet alone. CHECKED: 80,000, 0 failures. Under 2O, the double cover of the 24:
  - its 48 elements are Gaussian-integer matrices M with the scale root 2 to the e, and det M = 2^e;
  - so M epsilon M^T = det(M) epsilon: epsilon is A1;
  - the Reynolds sum of the three symmetric two-spinors is 0, so nothing else is A1 (the symmetric part is T1);
  - one twin pair's axis S moves by the 24 signed permutations of determinant 1, each met twice (as M and -M).

  PROVED by the characters (1/2 x 1/2 = A1 + T1). CHECKED: 1,061 runs, 0 failures (48 elements, 24 rotations).
- **P10, the local value.** Summed over the six Spoke directions, n n^T = 2 I. Fitted hands set with opposite senses chi(n) and chi(-n), n over the six, each clicking alone by Born, then give E = -m1 . m2 / (3 rho1 rho2), so S = -82/87. PROVED. CHECKED: 15 runs, 0 failures.
- **P11, CHSH.** Take answers that are functions a(phi1, lambda) and b(phi2, lambda). For each lambda, a(phi1) [b(phi2) + b(phi2')] + a(phi1') [b(phi2) - b(phi2')] is +2 or -2. So |S| <= 2 for every distribution of lambda that does not depend on the settings. PROVED. CHECKED: the 16 deterministic strategies reach 2 and no more. The singlet's -82/29 is exact.
- **P12, the rewind.** The one formula runs back exactly (law 3): p+ = W (a+ - a) + r+ - mid, p = p+ - s F(a), and (a - a-, r) = carry(p, W, mid). The remainder's write (part 4.3) comes off from its note. PROVED. CHECKED (closure24_lattice.txt): 40 trials on the ring (14, 1, 1) for 12 ticks each way, and 8 on the torus (14, 3, 3) for 8 ticks, 0 failures.

## 4. Can the one formula carry the closure? (the owner's condition)

The decision of section 24 item 3 reads: "the click of a split leaves its quotient, and its remainder is carried one Mesh a tick by the one formula itself, with no carriage of its own".

**The one formula's own act, in the three operations.** Take the remainder's write (model M2 of part 5).

- With eta = phi1^(-a), form c = <eta, psi_A> (8 products, 6 additions), then the part not taken, (c eta1, c eta2) (8 products, 4 additions).
- Each of its four integer coefficients goes by Rule3 on N(eta) = rho1: the quotient goes to the gear and the remainder is booked. This is done at both slots, now and before.
- Then law 2 carries it: p = W (a - a-) + (r - mid W), F = sum over the six Spokes of g (a_j - a) - D a, p+ = p + s F, and (a+ - a, r+) = carry(p+, W, mid W). The probe uses the head's own carry and mid.

### 4.1 The one formula is linear in the gears, up to its carries

Take a flat clock (W and s constant), U_j the identity and J = 0. Then law 2 is the same integer recursion at every gear of the twin pair.

- The momentum steps exactly linearly: p+ = p + s F.
- The notch steps by (p+ + mid) div W, which differs from p+ / W by at most one half.
- So two runs that differ by a write delta at A differ at B by G delta, plus at most half a notch of rounding per gear per tick. Here G is the step's propagator.
- G is real: it is the same on the three and twelve gears, so it multiplies a Gaussian by a real factor. It is blind to the spin, being the same on both twins. It is zero outside the cone, by the stencil of seven.

PROVED. With the offset's spin term in J, G also turns the spin by the field the offset holds. It is still linear in the twin gears, so parts 4.2 to 4.4 hold to first order in that coupling (OPEN 4).

### 4.2 What arrives is added; it does not replace

The partner's twin pair at its click is psi_B = beta + G delta, plus the rounding, where beta is what it would hold with no first click. The closure asks the partner's axis to be -a m1 for every setting m1 and both answers.

- If beta is not 0, as the partner's click of a split needs, the partner holding its own whole winding, this asks G delta = lambda chi(-a m1) - beta for each (a, m1).
- Then delta would have to depend on beta, which the first click does not read (locality, line 92). Or it would need the propagator from A to B written into the click, which is a rule written for the phenomenon (line 102).

PROVED: no click that reads its own Node-clock gives the partner the closure's reading while the partner holds its own hand.

### 4.3 What a click sends is the taken sense

Suppose the split's quotient leaves A and its remainder stays (P5). Then the click's change is delta = (remainder) - (whole) = -(the taken part), and its axis is +a m1, since S(-x) = S(x). That is the opposite of the closure's axis.

- Where that change dominates the partner's reading, the partner lines up with the first answer, and E tends to +m1 . m2.
- PROVED. CHECKED: exact odds, light train, ring: S = +2.7992 at Delta = 36 (E(a,b) = +0.7170). That is past Bell's bound with the sign opposite to the singlet's, inside the cone, by a signal. E near +m1 . m2 for every pair of axes is a correlation that no state of two twin pairs gives: such a state with E = +k m1^ . m2^ needs k <= 1/3. PROVED: its weight on the singlet is (1 - 3k)/4, since the singlet's sigma . sigma is -3 and the one-sided terms vanish on it.
- The head's write (bobs.splits: the picked twin set to the whole wind, the other zeroed) leaves the taken sense at A. Whatever leaves A after it carries +a m1 likewise.

### 4.4 Where the one formula carries the closure's axis, it holds less than a winding

Suppose the partner holds nothing (beta = 0) and the first click comes before any of its fitted hand's field has left A. Then what arrives is the remainder alone. Its axis is -a m1 (P5), and the spin-blind propagator keeps it.

- CHECKED (model M2e: light train, A's remainder left at its fitting):

  | Delta | ring: along -a m1 | ring: rho at B / a fitted hand's | torus (14, 3, 3): along -a m1 | torus: rho at B / a fitted hand's |
  | --- | --- | --- | --- | --- |
  | 6 | 1.0000 | 0.0000 | 1.0000 | 0.0000 |
  | 8 | 1.0000 | 0.0009 | 1.0000 | 0.0000 |
  | 12 | 0.9999 | 0.0132 | 1.0000 | 0.0000 |
  | 20 | 1.0000 | 0.0344 | 0.9999 | 0.0193 |
  | 36 | 0.9999 | 0.0297 | 0.9999 | 0.0008 |

- Where something arrived, the correlation is the singlet's. S = -1.8850 = (2/3)(-82/29), because in 8 of 48 cases the first answer was sure and left no remainder, and those count 0.
- But the remainder is a part not taken. By the click of a split's premise, each part holds less than a whole winding, and the step's conserved wind spreads it.
- So at B, within 36 ticks:
  - on the ring, rho reached at most 0.0344 of one fitted hand's;
  - on the torus, at most 0.0193;
  - with the heavy train, nothing reached B (48 of 48 cases).
- The partner then holds no whole winding, and its click of a split cannot fire. PROVED (the premise, and the books); CHECKED.

### 4.5 The one formula's carriage signals

The first click's write depends on its setting, and the step carries it. So the partner's own statistics move with the first setting.

- In exact odds, B's marginal under a against a' differed by up to 0.1947 on the ring and 0.4380 on the torus (Delta = 20).
- In the many-draw runs, B's answer moved with A's setting in 19,466 of 56,000 timelike runs (light train).
- Nature's singlet never signals: B's marginal is one half at any separation.

So the one formula's own carriage is no closure. If it were taken as one, it would bring two new contradictions inside the cone: the taken sense's correlation, and the signal. CHECKED.

For comparison, the carriage models do not signal. M1a's partner marginal is exactly 0 per pair, since P(a) = 1/2. M1b's is -(m1^ . n^)(m1^ . m2^) per hidden n, with the hats the unit axes (m / rho), and 0 over the six n. PROVED. The measured gaps were 0.005 to 0.096 on 2,000-run cells, within the noise.

### 4.6 So the closure at a distance is a carriage of its own

What it must hold, named. These are taken from David's form and from DAVID-THE-BELL-LOCAL.patch's "flying" closures, which his TENSOR24 form keeps in substance:

1. **The message:** the first click's taken sense tau = phi1^a (two Gaussian integers), or (rho1, m1, a) (five integers).
2. **Its way:** the fitting's Spoke toward the partner, or the pair's name, so that it reaches the partner and no other twin pair. David: "the closure follows the partner's hand".
3. **Its step:** a shift of one Mesh a tick, first order and along a Spoke. That is not the one formula's step, which is second order with grips, and disperses.
4. **The write at the partner:** its reading replaced by (N(tau), S(tau_perp)), which is a branch on whether a message stands there. The replaced reading is booked for the rewind (postulate 4).
5. **For David's first click:** the open reading (rho, 0) stored at both fitted hands (P1, P2). This item goes if the two-step form of 2.2 is taken.

Under Sofer's scan (scribe_scan.py, scribe-5), items 1 to 3 held off the gears are "state outside a Node-clock". Held on the gears, they are a train of its own written for the closure. Either way the carriage is put in.

PROVED, by 4.2 to 4.4: nothing less carries the closure. **So the condition "with no carriage of its own" cannot be met at L >= 2.** CHECKED, as M1: the carriage gives S = -2.769 to -2.876 inside the cone, against the exact -2.8275 (part 5.3).

## 5. Bell: the engine is local and deterministic

### 5.1 The cone, exactly

A click at A at tick t_A writes A's gears and nothing else. By law 2's stencil, the state at t_A + k depends on that write only within k Meshes (the graph distance). The partner's click at t_B reads its own Node-clock (the reading) and its six neighbours (the draw). So it can depend on the first click's setting and answer only where Delta >= L - 1 (through the draw) or Delta >= L (through the reading). PROVED.

CHECKED (L = 6, with A's other setting):

- Delta <= 4, M2, whose first click writes the gears: B's answer, draw and reading moved in 0 of 40,000 runs, for both trains. For M0 and M1, whose first click writes no gear, the same holds by construction, and the carried message had not yet arrived (B's answer moved in 0 of 40,000).
- Delta = 5: the draw moved in 7,285 of 8,000 runs (light, M2), and the reading in 0.

### 5.2 The theorem

Take Delta <= L - 2. Let the detectors' settings be set at their own Node-clocks, each outside the other click's cone and independently of the pair, and let every pair be counted. Then b is a function of (the state outside A's cone, phi2), and a of (the state, phi1). Both are deterministic, since the draw is a function of the state. So |S| <= 2 (P11). PROVED.

This holds for every rule of the engine: the one formula, any click, any closure, and any carriage of at most one Mesh a tick. It is Bell's theorem in CHSH's form, for a local deterministic machine.

### 5.3 The numbers

Model by model (closure24_lattice.txt):

- **M0, local:** each fitted hand clicks on its own twin pair.
- **M1a, David's closure, carried:** the stored open reading, then the message moving one Mesh a tick, the partner reading (rho1, -a m1) once it has arrived.
- **M1b:** the same, with each fitted hand's own reading before the message arrives.
- **M2, the one formula's own carriage:** part 4.3.
- **M3, the Mesh's one act at L = 1:** part 2.1.

The many-draw cells hold 2,000 runs per setting pair, each with its hidden n and fine teeth from an integer LCG. One standard error of S is about 0.03 to 0.045.

| model | spacelike, Delta 0 to 4: S | edge, Delta 5: S | timelike, Delta 6 to 12: S | exact |
| --- | --- | --- | --- | --- |
| M0 local | -0.981 to -0.828 | -0.956 (light), -0.885 (heavy) | light -0.996 to +0.992; heavy -0.955 to -0.840 | -0.9425 while the bobs stay (P10) |
| M1a closure, carried | -0.062 to +0.060 | +0.029, -0.001 | -2.869 to -2.775 | 0 outside the cone, -2.8275 inside (P6, P7) |
| M1b carried, own readings | -0.981 to -0.828 | -0.956, -0.885 | -2.876 to -2.769 | -0.9425 outside (P10), -2.8275 inside (P8) |
| M2 one formula | -0.981 to -0.828 | -0.920, -0.885 | light -0.955 to +1.674; heavy -0.955 to -0.840 | every draw counted, to Delta 36: light ring -0.94 to +2.80; light torus -0.94 to +1.50; heavy -0.9425 at every Delta |
| M3 the Mesh's act, L = 1 | | | | -2.8275 exact; -2.8270 on 8,000 vernier draws |

Notes:

- **Every run counted.** Both clicks fired in every run, with no refused draw.
- **The light train's drift.** Its bobs do not stay put: by Delta 7 each fitted hand's Node-clock holds both bobs' waves, so M0's local value drifts (|S| <= 0.996). The heavy train's bobs stay.
- **The heavy train carries nothing.** In 56,000 timelike runs, B's answer moved with A's setting in 119, almost all through the draw: the reading moved in 1.

### 5.4 Where the singlet holds, and where it cannot

- **It holds exactly in two places.**
  - (a) At the two ends of one Mesh, in one act (M3), given the A1 premise (OPEN 1).
  - (b) At L >= 2, where the partner clicks at least L ticks after the first click and the first click's taken sense is carried to it and read in place of its own reading (M1). That is a carriage of its own.
- **It cannot hold where the partner clicks fewer than L - 1 ticks after the first click,** outside the cone. There every rule gives |S| <= 2 (5.2), and nature gives 2 sqrt 2: Aspect, Dalibard and Roger 1982; Weihs et al. 1998; the loophole-free test of Hensen et al. 2015 at Delft, S = 2.42 +/- 0.20. No derivation removes this while a Node-clock reads one Mesh a tick, its draw reads its state, and the settings are free of the pair (5.5).
- **Inside the cone, the singlet by a carriage is no Bell test in nature's sense.** It is a hidden influence from the first click to the partner. It is unseen in the partner's own statistics (4.5), but it is causal, and it has a finite speed in the lattice's frame.
  - The cone is wider than light's. The causal speed is one Mesh a tick, and light's is 1/sqrt 3 (postulate 3; the clock words' c). So along an axis the carriage outruns light by sqrt 3 (section 18 item 2).
  - Where it does, the engine shows S > 2 between clicks that nature calls spacelike.
  - Measurement in nature bounds the speed of such an influence below by about 10^4 c in frames near the Earth's (Salart et al. 2008). Influences of finite speed that reproduce quantum correlations also allow signalling among more parties (Bancal et al. 2012).
- **The one formula's own carriage (M2) does not give the singlet even inside the cone.** It gives the taken sense's correlation and a signal (4.3, 4.5).

### 5.5 What row 56's gate must hold, so that it cannot overclaim

1. **Every fitted pair is counted.** A pair whose click did not fire (a refused draw, a split not due) is counted, not dropped. Selecting the pairs "clicked at both ends", as predicates.bell does, lets a local rule pass 2 (the detection loophole: Pearle 1970; Garg and Mermin 1987).
2. **The settings are free.** Each is set at its detector's Node-clock from its own history, independent of the pair, and outside the other click's cone. The one seed makes every setting a function of the state, so this independence is read from the record, not assumed. A seed tuned so that settings and pair agree, which is superdeterminism, would be a result typed in, and the one formula provides none.
3. **The two clicks' separation is read from the record,** their ticks and their Node-clocks. The row reports S outside the cone and inside it, each against 2. A gate of this form can fail both ways. This is section 18 item 13's way out for row 56, in place of "nature's band 4 < S^2 <= 8" (A9).

## 6. The probes and their outputs (protocol step 3)

**How to run.** Both probes run with `python3 -I -B` and use integers only: no float and no Fraction. Ratios are compared by cross-multiplication, and decimals are printed by integer division.

**closure24_algebra.py**, output in closure24_algebra.txt:

- P1 to P11, with exhaustive and random property tests: 0 failures.
- Two controls, each a wrong form that must fail: 788 and 391 mismatches.

**closure24_lattice.py**, output in closure24_lattice.txt:

- **The head's code.** It imports only the head's core/acts.py `carry` and `mid`, so law 2's Rule3 is the head's bit for bit. The head holds no closure to compare with: bobs.splits says "the pair's one pick across a fitting that Bell's 2.828 needs, wait on the owner's word". The head's split against law 6 was checked by David (30,388 draws).
- **The world's integers:** W = 3 x 2^19 and s = 1. The light twin train has g = W/3 (light's own grip ratio) and D = W/24. The heavy one has g = W/96 and D = W/6. The bobs are 4,096 notches, the room is 5,800, L = 6 and t_A = 2.
- **What it holds:**
  - [rewind]: P12;
  - [A] and [A summary]: the many-draw runs, light and heavy, M0, M1a, M1b and M2, at every Delta from 0 to 12, with the locality counts and the signalling gaps;
  - [B]: M2's exact odds on the ring (14, 1, 1) and the torus (14, 3, 3), light and heavy, to Delta 36;
  - [B']: M2e;
  - [D]: M3.
- **What it simplifies:**
  - the vernier's digits are the raw fine teeth, without the pitches and frames;
  - the clock is flat, with no offset (spin term 0), and the twin train stands alone;
  - the detectors are integer twin pairs written at their clicks, not trains that move;
  - the fitted hands are set L apart at the start, not set one Mesh apart and moved.

## 7. What it replaces and what it changes (protocol step 4)

- **11 (d), the open axis.** "The fitting sets the open axis on both fitted hands (S = 0)" names a reading that no twin pair holds (P1, P2). It is replaced by the pair's split on its A1 part (2.1, 2.2): the first click is half and half by Lagrange. The closure's formula stands as David wrote it (P7), now derived as that split's second step.
- **bell_turn.** It goes, as already decided. It is the quaternion turn by a declared setting in DAVID-THE-BELL-LOCAL.patch, which the scan names a "tuple of bilinear sums", with module tables keyed by id(), which the scan names "state outside a Node-clock". The formula here holds no turn.
- **The carriage at L >= 2.** It is not removed: it is named (4.6) and marked as put in. Its label is Sofer's to give: state outside a Node-clock, or a train written for one phenomenon.
- **Row 56.**
  - SHOWN at L = 1 (the Mesh's act, under OPEN 1), and inside the cone with the carriage. Neither is a Bell test in nature's sense (5.4).
  - NOT SHOWN outside the cone, for good, with the cause named: Bell's theorem.
  - Its criterion, nature's band (A9; section 18 item 13), is replaced by 5.5 (3).
- **Row 57 (GHZ).** The same premise excludes GHZ's correlations outside the cone (Mermin's form). Not probed here (OPEN 3).
- **The law's line 1169** (scribe-5, "Tsirelson's bound is a theorem of the credit's form", A9). Its alignment asks for the correlation "in the reckoner's whole view and no act between the two Node-clocks". A reckoner reads the record and makes nothing. So with no act between the Node-clocks, the record's S is at most 2 outside the cone (5.2). The clause cannot be re-derived under the generic Node-clock as worded.
- **The contradictions with nature left.**
  - Section 18 item 4, which is permanent under locality.
  - Section 18 item 2, for any carriage of one Mesh a tick.
  - If the one formula's own carriage were taken as the closure, two more: the taken sense's correlation and the signal inside the cone (4.3, 4.5).

## 8. The law's lines 33, 92 and 102

**Where the lines are.** In the worktree's docs/ALGEBRA.md (S/t24, engine-5.0-test), lines 33, 92 and 102 hold other clauses: postulate 4, no float, and MS-S2. The clauses the plan cites are scribe-5's (bcc1f006b). In the t24 file, postulate 3 stands at line 31 and locality at line 86, and there is no circularity clause.

**Line 33 (postulate 3).** It says that "every act travels one Mesh per tick at most ... a bare word crosses a Mesh in one tick, sqrt 3 times light's straight-line speed; no hand carries it and no click of nature's measures it, and what a bob measures of another by clicks never exceeds c".

- The carriage is a bare word of one Mesh a tick that the partner's click measures, and along an axis it exceeds c.
- The L = 1 act stays within one Mesh and one tick, and so within the line.

**Line 92 (locality is never broken).** It says that a Node-clock reads itself and its six Meshes, and, for "the correlation of two clicks (Bell, GHZ), ... the correlation in the reckoner's whole view and no act between the two Node-clocks".

- The carriage is an act between the two Node-clocks. So is the L = 1 act, though it reads only one Mesh.
- Under the line's last clause as written, Bell's S stays at most 2 everywhere (5.2). The line must choose between that and the closure.

**Line 102 (no circularity).** It says that "a rule that supplies an outcome from a stored answer and a setting is the phenomenon put in", and that "a correlation lives in the state of the hands that hold it and is read across the Mesh".

- The carriage supplies the partner's reading from a stored answer (a) and a setting (m1). By the line's own words it is put in.
- The L = 1 act reads across the Mesh: the pair's A1 part and the two detectors. It is within the line's last sentence if the A1 premise is granted (OPEN 1).

## 9. The plan's text, proposed for the Boss

**Section 18, item 4 (Bell at a distance).**

> A Node-clock reads one Mesh a tick and its draw is a function of its state, so the engine is a local deterministic machine. Take two clicks L Meshes apart, the second fewer than L - 1 ticks after the first, with the detectors' settings set independently of the pair and every pair counted. For them, every rule of the engine keeps |S| <= 2 (Bell's theorem, CHSH's form), any closure and any carriage included. Nature reaches 2 sqrt 2 there (Aspect 1982, Weihs 1998, Hensen 2015). No derivation removes this while the law's locality stands. Inside the cone, the singlet's correlation is reached exactly only by carrying the first click's taken sense, four integers, to the partner and reading it in place of the partner's own reading. That is a carriage of its own, not the one formula (draft D, part 4), and along an axis it moves sqrt 3 times light's speed (item 2). At the two ends of one Mesh it is one act, exact and local (draft D, 2.1).

**Section 18, item 2.** Add: "a closure carried one Mesh a tick moves at sqrt 3 c along an axis; at L = 1 it is one act within one tick".

**11 (d) and section 27, the closure paragraph.**

- "The fitting sets the open axis on both fitted hands (S = 0)" becomes: "the pair's split on the A1 part of its two twin pairs, sigma_ab = N(det[phi1^a, phi2^b]); its first click is half and half by Lagrange".
- "Carried one Mesh a tick to the partner by the one formula, with no carriage of its own" is struck (4.2 to 4.5).
- "The one thing put in" becomes: the carriage at L >= 2 (4.6), and the A1 premise at L = 1 (OPEN 1).

**Section 24, item 3.** The decision holds for the formula (2.1, 2.2) and for the two ends of one Mesh. It cannot hold for a distance of two Meshes or more, where the closure needs the carriage of 4.6. The owner's word is asked again: allow the carriage, with items 2 and 4 of section 18 standing, or keep the closure to the two ends of one Mesh.

**Section 25, item 10.** "... so this stands as a contradiction until David's derivation answers it" becomes "... so this stands as a contradiction of the local engine with nature, which no derivation answers while a Node-clock reads one Mesh a tick".

**Section 19, the owed list, "the closure of the split".** Its formula stands (2.1, 2.2). Its carrier at L >= 2 is the owner's ruling.

## 10. Open, and owed

- **OPEN 1, the A1 premise.** That the pair's split reads the A1 part of its two fitted hands, and not their product with its T1 part.
  - It follows if the fitting, whose source is the light's wind (A1), sets the pair as one A1 tensor.
  - The head's fitting sets two twins with opposite senses. Their product holds a T1 part, and Born on the whole product gives the local value (-0.9425 over the six n), not the singlet.
  - This is draft A's (what a click writes) and David's.
- **OPEN 2.** The owner's ruling on section 24 item 3 at L >= 2.
- **OPEN 3.** GHZ (row 57) by the same theorem; a probe is owed.
- **OPEN 4.** The offset's spin term in J: parts 4.1 to 4.4 hold to first order in that coupling. Not probed. With the metric's half on (the regulator driven by the twin hands' stress), the step is no longer linear in the twin gears, and 4.2 then rests on line 102 alone: an overwrite of the partner's axis by those terms would be a rule written for the phenomenon. That route is not probed. Whatever it carries still obeys part 5's cone, so part 5 does not depend on it.
- **OPEN 5.** Whether a carriage at light's speed c should be preferred to one Mesh a tick. It removes item 2's excess, not item 4.
- **Owed, protocol step 5:** a second hand, a verifier who did not write this, re-derives parts 2 to 5, attacks them (the zero detector, the sure first answer, the largest integers, the rewind), runs both probes, and reports CONFIRMED or REFUTED.
- **Owed, protocol step 6:** Sofer's law check, then David's sign-off.
