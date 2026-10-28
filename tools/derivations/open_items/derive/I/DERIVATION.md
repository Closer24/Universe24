# Draft I: the charge the one formula keeps, and the act that keeps it

For Tensor24's owed list (TENSOR24.md, section 19: "the charge's conservation derived from the one formula"; section 16, the block "Draft A and its verifier": the kept charge Q* and its two breaks). The board: derive/INDEX.md, item I (drafter: the Boss's helper; verifier: to name). Drafted under derive/PROTOCOL.md on derive/TEMPLATE.md. Every claim is marked PROVED (with its proof), CHECKED (with its probe's count) or OPEN (with what blocks it). Read on the head in the scratchpad worktree t24 (009e50f00; the engine as at 526a5666d and 834cfd72e), by runtime monkeypatches alone; no file of the repository or of a worktree is changed. The law is quoted from scribe-5's docs/ALGEBRA.md at f32b67cc3 (copy: ALGEBRA_scribe5.md here), one numbering.

## 0. The answer in short

**The charge.** For each coupled hand train, at the tick's start,

    Q* = - SUM_x e_x lam_x Im(conj(a_x) P_x),   e = 1 - 2 b,   lam = 1 / (X mr^2),   P = w (now - before) + fine - mid(w)

b the pawl bit (the ratchet's fine tooth), X the stretch, mr the mesh rate, w the gear's teeth. It is the law's own Omega(re, im) with the conserved form's weights 1 / p_i^2 (line 803), read in the frame every hand was born in (line 1602's frame clause), with the fine tooth's term kept.

**The act that keeps it: two changes, each one line.**
1. **The Mesh's turn read in the frame.** The odd gear's Mesh sum is read with the far end's pawl, odd = s (o_x + f o_y), as the head already reads the count, n = K_x - f K_y. The flow gears' skew is read with the near end's pawl sign, m = e_x 3 R s (V_x + V_y). Here f = e_x e_y, s is the Spoke's side, and R is the hand's rest rate times its coupling.
2. **The turnover applies the train's phase reversal once.** A hand's two slots are exchanged through K^(1 - c), with c its coupling, the power at which the Meshes read the pawl. So a coupled hand is exchanged with no K, and the pawl's flip carries the conjugation. On the twin hands, T = i sigma_y K is applied once, by the turnover count modulo 4, and the slots are exchanged with no T. The stored sweep then turns exactly where the pawl flips, and the framed charge is kept.

**Status, claim by claim.**
- The Mesh current is antisymmetric across every pawl wall iff theta_yx = -f theta_xy: PROVED. The head's triple breaks it at every pawl wall where the triple is not the identity: PROVED. Change 1 restores it: PROVED.
  - CHECKED on the toy: 0 of 486 Meshes not antisymmetric, against the head's 224 of 224 pawl walls.
  - CHECKED on the head: the summed current A = 0 at 60 of 60 ticks on the hole and on nature, against the head's 47 and 53 of 60 (largest 17,276.1 and 61.6 vacuum sweep units a tick).
- Change 1 is forced by the Z2 and the 24: PROVED. It is the unique pawl-covariant extension of the head's turn at equal pawls, given that the offset is framed (its count's reading says so) and the regulator is not (its own reads see no pawl).
  - CHECKED: the gauge flip commutes with the step at 0 of 81 Node-clocks for this form, and fails at 80 or 81 of 81 for every other framing. The 24 commute with it, 24 of 24.
- Q* is kept to the last digit by the exact step at fixed rates: PROVED; CHECKED (0 of 40 exact ticks moved).
- Change 2 keeps the framed charge through the turnover: PROVED; CHECKED.
  - The toy: Q* kept on the stepped state, 0 of 4 moved.
  - The twin hands: 0 of 30 ticks moved over 93 turnovers. Applying T in both the gears and the count reverses the turned clocks' charge, 8 of 8.
  - The head: the turnover's own term equals its formula at 3,732 and 2,511 Node-clock turnovers.
- **The rounding: Q* is not kept to the last digit by any carry. It is kept only up to the remainders' cross terms, each an exact integer over its Node-clock's own denominator, booked:** PROVED (theorem R2, and the law's line 785 recomputed); CHECKED (section 5).
- **Q* still moves on the head after both changes, by four named local terms.** Each is computed from its own formula and closes the budget to the last digit at 60 of 60 ticks on both worlds (CHECKED).
  1. The roundings.
  2. The turned clocks' inflow: the law's mirror ends a turned Node-clock at its held pre-state, so it misses its own tick. PROVED.
  3. The clock's rates moving between ticks: the weights are read at the tick and not at the time-Mesh. PROVED.
  4. The click: the fitted hands are laid with one shape at two ends of different charge units and frames. PROVED.

  So "the charge's conservation derived from the one formula" holds in the rationals at fixed rates. On the integers it holds up to the booked roundings. Items 2 to 4 above are OPEN (section 8).
- The rewind stays exact with both changes: 20 of 20 ticks on the hole and on nature (CHECKED).

**What it replaces:**
- Break 1 and Break 2 of draft A's verifier.
- Draft A's F4 gate (a rule written for its phenomenon), by the budget identity: a reading that can fail.
- Line 1602's "every charge conjugated (the Wronskian odd under the swap)". This is a change of the law, the owner's.

**What it leaves:** the four named moves above (section 8).

## 1. In the clocks

- **The hand's charge is its sweep.** A hand is a small clock with two notches in time, now and before. The cross of the two, Im(conj(now) before), is its sweep: the sense and the size of its turning. A Mesh passes sweep from one end to the other. The step keeps the sum over the great clock when what leaves one end enters the other, read alike from both ends. Each Node-clock's sweep is weighed by its own clock: the stretch X and the mesh rate squared, the weight 1 / (X mr^2). This is because each end's grip carries its own mesh rate (line 803).
- **The pawl is the Node-clock's count of its own turnovers, modulo two.** A Node-clock that has turned an odd number of times runs its hand mirrored (its twelve gear negated). Its neighbours read it through the mirror (hands.seen), and its count K is read negated (meshes.offsets). Its sweep, read from outside, is its stored sweep times e = 1 - 2 b. The charge is the sum of these read sweeps.
- **The Mesh's turn has three parts:** the count's, the odd gear's (the offset's three T1 gears) and the skew's (the regulator's flows times the hand's own rest rate). The head read the count in the frame and the other two parts without it. So across a pawl wall the odd gear and the skew turned the two ends' readings the same way where they must turn them oppositely. What left one end did not enter the other. In the clocks, change 1:
  - the odd gear, a gear of the same train as the count, is read like the count: the far end's gear negated across a pawl wall;
  - the skew turns a hand by its own rest rate, and a mirrored hand turns backward, so the skew is read with the reading clock's own pawl sign.
- **The turnover is the clock's time gear reaching its top.** The Node-clock runs back: every gear's two notches are exchanged, and every fine tooth is mirrored about its mid tooth. The phase reversal (K on a hand, T on twin hands) may be applied once only. The head applies it twice, in the gears and again in the pawl's flip, and twice is a plain exchange, which reverses the sweep. Change 2 applies it once, in the pawl. The slots are exchanged plainly, so the stored sweep turns, the read sweep stays, and the charge is kept.
- **The carry.** Rule3's carry moves each gear by a whole notch and keeps the remainder in the gear. The hand's move and its remainder are two Gaussian integers. Their cross, Im(conj(move) remainder), is the charge the carry lets through in a tick, at that Node-clock. It is an integer the Node-clock can book. No carry can make it 0 for every hand (section 4, P7).
- **What remains, in the clocks:**
  - A turned clock ends its tick at the state it started from, mirrored. Its neighbours stepped against the hand it held, so the charge that flowed into it in that tick is not taken.
  - The clock's weight is read at the tick, so where the clock's rate moves from one tick to the next, the weight of a held sweep moves with it.
  - The fitting lays one shape at both ends of a Mesh, whatever their clocks and frames.

## 2. The formula, in the three operations

Every term is an integer of the head's state, or a product, sum or Rule3 carry of such integers. Each is named with its clock word.

- **The pawl sign and the Mesh's pawl** (the ratchet's fine tooth b at two teeth): e = 1 - b - b, and f_xy = 1 - p - p with p the parity of b_x + b_y by the carry on 2 (meshes.pawl; f = e_x e_y).
- **The count** (meshes.offsets, unchanged): n_xy = K_x - f K_y, with K = 2 (Phi_now - Phi_before) + c, and its (cos, sin) pair along the circuit.
- **The odd gear's Mesh sum** (change 1): odd_xy = s (o_x + f o_y), where o is the offset's odd gear of the Mesh's axis and s the Spoke's side (+1 or -1).
- **The skew's Mesh sum** (change 1): m_xy = 3 R e_x s (V_x + V_y), where V is the regulator's flow gear of the Mesh's axis, R = c times the rest rate, and 3 is AXES, the piece's count.
- **The triple** (meshes.through_mesh, unchanged): g3 = 4G G^2 - odd m and g12 = 4G m + odd G^2, with 4G = SIDES SIDES Gamma (meshes.mesh_teeth). The turn is the pair (g3 g3 - g12 g12, g3 g12 + g3 g12) over g3 g3 + g12 g12.
- **The turnover's write on a hand** (change 2): now' = K^(1-c) before and before' = K^(1-c) now. The sign of the twelve gear is (-1)^(1-c), with c in {0, 1} the coupling (the same exponent as the head's pawl reading, f**c). Each fine tooth is mirrored once per reversal of its gear (acts.mirror), and the ratchet's pawl is flipped (acts.flip).
- **The twin hands** (change 2, with draft E's item 3):
  - each Node-clock keeps its turnover count c modulo 4;
  - the neighbour's twin pair is read as K^(c_x)(h) T^(c_y - c_x) psi_y;
  - the turnover exchanges the slots and steps c by one.
- **The charge, a reading.** At each Node-clock, e Im(conj(a) P) is an integer and lam = 1 / (X mr^2) is its weight: one integer over the Node-clock's own integer denominator. Q* is their sum. Two readings of it are compared by cross-multiplication. Nothing of it is written into the state.
- **The booked terms:**
  - the carry's term: Rc = -e lam Im(conj(v) rho'), with v = now' - now and rho' = fine' - mid(w');
  - the turns' term: Rt = -e lam X SUM_j g_j Im(conj(a) (m_j - m_j exact)), with m_j exact the turn's Gaussian rational before its two roundings (denominator: the standard length times g3 g3 + g12 g12);
  - the turnover's own term: e lam Im(conj(now - before) (fine - mid)) of the held hand.
- **No other number appears.** There is no number beyond 0 and 1 but the lattice's counts 2 (the sides) and 3 (the axes), no float and no clamp. There is no branch on a train: c is the train's integer, read as a power.

## 3. In the tensors

- **The hand** is the A1 kind of the 24 times one Gaussian integer.
  - Its charge density is Im(conj(a) P), the antisymmetric part of its two notch pairs' bilinear: an A1 of the 24, even under the time reversal T (z to conj z, time run back) and odd under the unitary run back (CT).
  - The current through Spoke j is J_j(x) = e_x 2 pinion Q_j Im(conj(a_x) U_j a_j): the Spoke's component of a T1 current, odd under the exchange of the ends.
- **The pawl's Z2.** The gauge flip G_x conjugates the hand at x, flips its pawl, and negates the gears at x that carry the hand's charge sign: the offset's count and its three odd gears (the scalar and vector potential, one train). It leaves the regulator, whose kinds (2 A1 + E + T1, the metric) carry no charge. The pawls are a pure gauge: f is the product e_x e_y on every Mesh, its plaquettes are +1 (draft E, e5), and every Mesh read must commute with G.
- **The Mesh's turn U_j** is a product of three phases:
  - from the count (A1, framed);
  - from the Spoke's component of the odd gear (T1, framed);
  - from the Spoke's component of the flow (T1, unframed) times the hand's rest rate, which carries the hand's own rotation sense (odd under G).

  The 24 allow only the Spoke's component of a T1 gear in a Mesh's turn: a transverse component breaks 21 of 24 rotations (CHECKED, i1 mutant `transverse`).
- **T** is K on a hand and i sigma_y K on the twin hands, with T T = -1 (Kramers; draft E, P4 and P5). The frame of a twin pair is T^c with c modulo 4, since T^2 = -1 is a sign that the pawl's two teeth cannot hold.
- **The contraction used** is the A1 part of A1 times A1 (conj(a) times P), antisymmetrised. The 24 allows it at every Node-clock, and it is the one A1 the hand's own U(1) leaves.

## 4. The proofs

**P1. The condition for an antisymmetric Mesh current.** PROVED.
- Let x read y as u_xy K^((1-f)/2) a_y, where u_xy is the head's phase.
- At f = 1, J_xy + J_yx = e S Im(conj(a_x) (u_xy - conj(u_yx)) a_y). This is 0 for every hand iff u_yx = conj(u_xy).
- At f = -1, Im(conj(a_x) u conj(a_y)) = Im(u conj(a_x a_y)), so J_xy + J_yx = e_x S Im((u_xy - u_yx) conj(a_x a_y)). This is 0 iff u_yx = u_xy.
- So, with theta the phase's angle, the condition is theta_yx = -f theta_xy.
- The count satisfies it: n_yx = K_y - f K_x = -f n_xy, and the circuit's pair is odd in n (readings.standard_angle).

**P2. The head's triple breaks it at every pawl wall where the triple is not the identity.** PROVED.
- odd_yx = -s (o_y + o_x) = -odd_xy, and m_yx = -m_xy. So g_yx = conj(g_xy) and theta_tri(y,x) = -theta_tri(x,y) at every f, where f = -1 needs +.
- CHECKED: 224 of 224 pawl-wall Meshes with a nonzero triple, 0 of 260 one-frame Meshes (i1, C1).

**P3. Change 1 is forced, and it is antisymmetric.** PROVED.
- Antisymmetry:
  - odd_yx = -s (o_y + f o_x) = -f s (o_x + f o_y) = -f odd_xy, since f f = 1;
  - m_yx = e_y 3 R (-s) (V_y + V_x) = -f m_xy;
  - so g_yx = (4G - i f odd_xy)(G^2 - i f m_xy), and theta_yx = -f theta_xy.
- Forced:
  - Write the turn at equal pawls (the head's, the 24's) as h_xy = phi(K~_x - K~_y) psi(s (o~_x + o~_y), 3 R s (V_x + V_y)), in the physical gears K~ = e K and o~ = e o (framed) and V (unframed), with phi and psi odd.
  - The pure-gauge Z2 fixes the stored frame's turn as u_xy = K^(b_x)(h_xy), whose angle is e_x times the physical one.
  - Then e_x phi(e_x K_x - e_y K_y) = phi(K_x - f K_y), which is the head's count, and e_x psi(s (e_x o_x + e_y o_y), m) = psi(s (o_x + f o_y), e_x m), which is change 1.
  - No other placement of the pawl commutes with G under these frames (CHECKED, i1 C3):
    - change 1: 0 of 81 Node-clocks differ;
    - both T1 gears framed (fixA): 81 of 81;
    - neither framed (fixB): 81 of 81;
    - the head: 81 of 81.
  - fixA and fixB are antisymmetric too (C1), but each needs a framing the head's trains do not have:
    - fixA needs the regulator framed, which its own pulls refuse;
    - fixB needs the odd gears unframed, which the count's reading refuses (the offset is one train, acted on alike, and the odd gear's source is the sign's current read in the frame: line 1539, line 1602's frame clause).

**P4. Q* is kept by the exact step at fixed rates.** PROVED (the law's line 803 in the frame).
- The kick: SUM_x e lam X Im(conj(a) F) = SUM_x e SUM_j 2 pinion Q_j Im(conj(a_x) U_j a_j), since lam X g_j = 2 pinion Q_j is the Mesh's own and the same from both ends. This is SUM over the Meshes of (J_xy + J_yx), which is 0 by P3. The spring's and the self terms are real: Im(conj(a) a) = 0.
- The drift: Im(conj(a + P'/w) P') = Im(conj(a) P').
- CHECKED: 0 of 40 exact ticks moved, random pawls (i1 C2); the head's triple moves 40 of 40.

**P5. The turnover keeps the framed charge iff the phase reversal is applied once.** PROVED.
- In the frame Z = K^b a:
  - The head's write (K in the gears, the pawl flipped) gives Z' = K^(b+1) K a_before = K^b a_before = Z_before: a plain exchange. Then W_Z' = Im(conj(Z_before) Z_now) = -W_Z.
  - Change 2 (no K in a coupled hand's gears, the pawl flipped) gives Z' = K^(b+1) a_before = K Z_before: T. Then W_Z' = Im(conj(K Z_before) K Z_now) = W_Z.
  - In P terms: P goes to -conj(P) on the head and to -P under change 2. So the framed density -e lam Im(conj(a) P) is reversed on the head and kept under change 2, up to the mirror's remainder term (P6).
- On the twin hands: T^(c+1) psi_before = T Z_before (once: kept), and T^(c+1) T psi_before = -Z_before (twice: reversed).
- CHECKED:
  - i1 C6a and C6c;
  - i2 D3: kept 8 of 8 in the count and 8 of 8 in the gears; reversed 8 of 8 in both;
  - the head: the turnover's own term equals e lam E_held at 3,732 (hole) and 2,511 (nature) turnovers, and equals -2 q_held - e lam E_held on the head.
- **The twin frames need the count modulo 4.** Reading T^-1 as T (the pawl alone) leaves 242 of 486 Meshes not antisymmetric (i2, mutant `z2_frames`).

**P6. The turned clock's inflow, a theorem of the law's mirror.** PROVED.
- The law's turnover ends a turned Node-clock "at the state it started from ... the step's output discarded" (line 1602).
- Its neighbours stepped against its held hand, and they cannot know that it turns. The trigger reads its stepped time gear, which depends on its six neighbours, two Meshes from theirs (line 92).
- So at a turnover, Q*' - Q*_mid = SUM_turned [ e lam E_held(x) - (I + Rt + Rc)(x) ]: the turned clocks lose their own tick, and only the mirror's remainder term is their own.
- The mirror of the stepped state would keep Q* exactly (i1 C6c: 0 of 4 moved), but it turns again at every following tick (i1 C7: ticks 9 to 19, against one turnover at tick 9 for the held mirror). This is line 1602's own finding: "the swap of the post-state in place of the pre-state locks the great clock in a two-cycle at its top, refuted and shown".
- CHECKED: the turnover identity at 60 of 60 ticks on both worlds.

**P7. The rounding: no carry keeps Q* exactly, and the book is exact.** PROVED.
- (a) The step's identity: D' - D = X Im(conj(a) pull) + Im(conj(v) rho'), and Im(conj(v) rho') = Im(conj(v) P'), since Im(conj(v) w' v) = 0. CHECKED: 0 of 20,000 random steps to 2^200, both signs, with the edges 0 and teeth 2 among them (i3 R1).
- (b) **Theorem.** Let P' be a Gaussian integer with gcd(P'_3, P'_12) = 1 and max |P'_k| >= w'. Then no quotient v in Z[i] whose remainders satisfy |P'_k - w' v_k| < w' gives Im(conj(v) P') = 0.
  - Proof: Im(conj(v) P') = 0 forces v = k P' with k an integer, since P' is primitive.
  - If k = 0, the remainder is P' itself, outside the teeth.
  - If |k| >= 1, the larger remainder is at least (w' - 1) |P'_k| >= w'.
  - CHECKED exhaustively (i3 R2): 95,560 primitive momenta, w' from 2 to 12, |P'_k| <= 60, with 0 charge-keeping quotients. Among the 63,192 non-primitive momenta, 16,272 have one.
- So the carry that keeps the remainder in its gear, as Rule3 does with one pair (q, r') (law 1), passes charge at a Node-clock whenever the hand moves along a primitive direction. Rule3's quotient and remainder are unique, so the step has no freedom to avoid it.
- (c) **No quadratic form of one Node-clock's six integers (two notch pairs and two remainders) is kept by the integer step but the constants.** The null space over Q has dimension 1 over the 28 monomials of degree at most 2. The exact rational step's null space holds the charge (dimension 5 over 15) (i3 R3). This is the law's line 785, recomputed independently.
- (d) The turns' two roundings (rates.rounded, odd) leave the current not antisymmetric at 5,000 of 5,000 random Meshes, and the exact turn at 0 (i3 R4). Only the four Gaussian units turn Z[i] into itself exactly.
- So **Q* is kept only up to the remainders' cross terms**, Rc and Rt, each booked exactly at its Node-clock.
- CHECKED on the head: the step identity Q*_mid - Q*_start = SUM (I + Rt + Rc) at 60 of 60 ticks on both worlds, in every variant.

**P8. The rates' motion.** PROVED.
- A site-weighted charge SUM mu Im(conj(a) P) is kept by the kick only if mu X g_j is the same from both ends, which forces mu proportional to 1 / (X mr^2) at that tick.
- Between ticks the weights move: B = -SUM e (lam' - lam) Im(conj(a) P), which is not 0 where the rates move unevenly.
- The charge is kept exactly if the momentum is carried into the next tick's charge unit, P'' = (lam / lam') P'. Then lam' P'' = lam P', and the kick and the drift are as in P4.
- In the clocks, the conserved form's time part is the time-Mesh's: read from the tick's two ends alike, as the tension is the Mesh's. The head reads s and mr at the Node-clock's tick.
- CHECKED: the identity 0 failures of 24 with Q* moved at 12 of 12 ticks, and the rescaled form kept at 12 of 12 (i1 C5); on the head, B's formula at 60 of 60 ticks on both worlds.
- On the integers, the rescale is a second division, with its own remainder in each gear (OPEN 2).

**P9. Locality.** PROVED.
- The charge's flow is the Mesh current, read from the two ends' gears and the two pawls alone.
- Every booked term is a Node-clock's own integers: Rc, the turnover's term and B at the Node-clock; Rt at the Node-clock and its six Meshes.
- The budget holds tick by tick, so nothing is read beyond one Mesh (line 92).

**P10. The click's books.** PROVED.
- A fitting lays (sigma A, 0 | 0, B) at both ends, with F1's senses sigma_x = -sigma_y.
  - The framed sweep of the pair is e_x sigma_x AB + e_y sigma_y AB, which is 0 iff e_x = e_y.
  - Laid in the end's frame (the twelve gear read through the pawl, as `seen` reads it), it is 0 at every Mesh.
  - Its Q* is sigma AB (u_x - u_y), with u = lam w the end's charge unit. This is 0 only where the two ends' clocks agree.
  - CHECKED (i1 C9): of 400 random pairs, 197 across a pawl wall, the framed sweep is 0 at 400 when laid in the frame and at 203 when laid as the head lays; the Q* is 0 at 0.
- An unspringing removes both ends' charges, and keeps Q* only if they cancel in the unit.
- So with one fitted shape for every Node-clock, no click keeps Q* exactly where the clocks differ. Draft A's gate F4 (write only where the charge moved is 0) would refuse almost every lay and every evolved pair.
- What replaces it here is the budget identity. The click moves Q* by exactly the charge of its writes, booked, and the board's Q* is compared with the books tick by tick: a reading that can fail. The write in the charge's unit is OPEN 3.

**P11. The 24.** PROVED: every term is the Spoke's component of a T1 gear or an A1. CHECKED: 24 of 24 rotations commute with the step under change 1 (i1 C4).

**P12. The rewind.** PROVED: change 1 is a pure function of the tick's start board, read alike at -1, and change 2 is an involution (two exchanges and two mirrors). CHECKED: 20 ticks forward and back, the state equal to the forward run's at 20 of 20 ticks and the start bit for bit, on the hole and on nature, with both changes (i4_rewind.txt).

**P13. The run back at a uniform top.** PROVED in a static background. With change 2, the run back is the stored frame's plain exchange under the same Mesh pairs. So at the turnover the count must be kept, which needs the ratchet's slots negated as well as exchanged, and the regulator's flows must be negated: the train's T parity times its C parity. With the head's signs it does not retrace.
- CHECKED (i1 C8), on a static background:
  - change 1 with change 2, count kept and flows negated: retraces exactly, Q* kept;
  - with the head's background signs: no retrace;
  - the head's turnover retraces only with both T1 gears unframed (fixB), and then Q* is reversed.

## 5. The probes

All of them run with `python3 -I` (the toys) or with `/home/user/Universe24/venv314/bin/python -I` with sys.path set to S/t24/src (the head). Each prints PASS or FAIL per check, and each mutant's failing output is kept beside it.

| probe | what it checks | pass criterion | count | mutants (each must fail), file |
| --- | --- | --- | --- | --- |
| i1_toy.py | the exact toy on a 3^3 torus: C1 the antisymmetry by variant, C2 Q* over 40 ticks, C3 the gauge, C4 the 24, C5 the rates, C6 the turnover, C7 the top, C8 the run back, C9 the fitting | every check as stated | 32 of 32 PASS (i1_toy.txt) | `nopawl_seen`, `count_plain`, `transverse` (the 24, 21 of 24), `skew_far`, `no_rescale`, `sweep_not_turned`: i1_toy_mutants.txt |
| i2_twins.py | the twin hands with T = i sigma_y K: D1 the antisymmetry, D2 Q* over 30 ticks with 93 turnovers, D3 T once against twice, D4 the stored and physical dynamics | 0 Meshes off, 0 ticks moved, D3's three cases, 0 ticks differ | 4 of 4 PASS (i2_twins.txt) | `z2_frames` (242 of 486), `twice` (28 of 30 ticks moved), `no_frame_advance_fix`: i2_twins_mutants.txt |
| i3_rounding.py | R1 the step's charge identity to 2^200, R2 the theorem exhaustively, R3 the null space, R4 the turns' rounding | 0 failures; no charge-keeping quotient on primitive momenta; constants alone; exact turn antisymmetric | 6 of 6 PASS (i3_rounding.txt) | `no_rho` (19,966 of 20,000), `wrong_mid` (19,928), `even_round`: i3_rounding_mutants.txt |
| i4_head.py | the head with monkeypatches, 60 ticks: the budget step + turnover + click + rates, each term from its formula; A = 0; the turnover's term against its formula; the rewind | the budget closes at every tick, A = 0 at every tick, the turnover's term on its formula | fix12 PASS on the hole and on nature (i4_hole_fix12.txt, i4_nature_fix12.txt); the rewind 20 of 20 on both (i4_rewind.txt) | `fix1` (the sweep not turned), `fix2` (the pawl dropped from the triple), and the head: i4_head_mutants.txt |

**The head's budget, 60 ticks, vacuum sweep units** (both changes in place; fix12):

| term | hole, summed | hole, largest in a tick | nature, summed | nature, largest |
| --- | --- | --- | --- | --- |
| the Mesh currents A | 0 | 0 | 0 | 0 |
| the turns' rounding Rt | 1,357.6 | 327.6 | 2,867.9 | 476.7 |
| the carry's rounding Rc | 19,481.8 | 32,594.1 | 12,342.2 | 2,358.7 |
| the turnover's own term | -3,105.2 | 3,442.8 | 253.1 | 786.9 |
| the turned clocks' inflow not taken | -52,036.1 | 16,642.5 | 233,678.0 | 44,542.0 |
| the click (29 and 19 births) | -2,883,720.8 | 2,159,281.0 | -25,764.5 | 19,966.5 |
| the rates B | 149,703.2 | 878,450.9 | 3,132.1 | 2,409.8 |
| Q* moved | -2,768,319.5 | | 226,508.7 | |

The turnovers number 3,732 on the hole and 2,511 on nature.

**The mutants on the head** (i4_head_mutants.txt):

| variant | A = 0 at every tick | the turnover's term on change 2's formula | verdict |
| --- | --- | --- | --- |
| the head | no: 47 of 60 (hole, largest 17,276.1), 53 of 60 (nature, largest 61.6) | no: its term is the reversal, largest 2,674,429.1 (hole) and 87,055.3 (nature) in a tick | FAIL |
| fix1 (the sweep not turned) | yes | no: largest 7,529,985.9 (hole) and 87,587.9 (nature) | FAIL |
| fix2 (the pawl dropped from the triple) | no: 47 of 60 (largest 26,333.1), 53 of 60 (largest 238.5) | yes | FAIL |

**The edges:**
- 0: the zero hand, the first ticks, and P' = 0 in R1.
- The sign: R1's both signs and the odd rounding.
- The largest integers: to 2^200 in R1.
- The rewind: P12.
- Both teeth parities: R1 at random teeth. The mirror's even-teeth edge, a fine tooth at 0 under even teeth, is counted in i4 and met 0 times on the charts.

## 6. The law's lines (scribe-5, docs/ALGEBRA.md at f32b67cc3)

- **Line 92, Locality is never broken:** "a Node-clock reads itself and its six Meshes and nothing else, forward and backward". (P6, P9)
- **Line 94, The cube's 24 turns hold:** "the step commutes with each of the cube's 24 turns, bit for bit, the click included". (P11)
- **Line 721, The sign is the rotation sense:** "the charge density at a Node-clock is the booking W_i = re_now x im_before - im_now x re_before, the Wronskian of the two pairs, which Rule3's line conserves exactly with the conserved form's weights 1 / p_i^2 ... its weighted total SUM_i W_i / p_i^2 exactly invariant in the rationals at rates fixed in time". (Q*; P4, P8)
- **Line 785, the conserved form's proof:** "no quadratic form of the notches and the remainders is conserved exactly by the integer step, the Wronskian included ... the exact invariant of the integer step being the state itself through the back step". (P7c)
- **Line 803, The bilinears of one pair:** "two solutions u, v of one line conserve Omega(u, v) = SUM_i (u_now v_before - v_now u_before) / p_i^2 ... exactly in the rationals at fixed rates, in integers to the carried remainders, as W = Omega(re, im)". (Q* is this, framed.)
- **Line 805:** "no rounding with one integer of memory per Node-clock conserves the form ... Rule3 unchanged, no second carried integer". (OPEN 2)
- **Line 1539, The odd gear's source is the sign's own current:** "the odd gear on the axis a is sourced by J_a, the sign's own current". (P3: the odd gear framed with its source)
- **Line 1602, The turnover**, which says:
  - the frame clause: "where they differ the neighbour's plane value is read conjugated and its K negated ... and every reading of a plane across a Mesh, the sign current's and the tension's ... and the Lorentz form's flux ... : the Wronskian's flux through a Mesh is one number read from both ends in the frame every hand was born in". Change 1 restores this for the odd gear and the skew, which the head reads outside it. The same line records that "the flux cancels there to 39 to 75 notches ... owed by name": Break 1's ancestor;
  - "every charge conjugated (the Wronskian odd under the swap)": this is Break 2 as law, and change 2 changes it;
  - "the step's output discarded": P6;
  - "the swap of the post-state in place of the pre-state locks the great clock in a two-cycle at its top, refuted and shown": P6 and C7.

## 7. What it replaces and what moves

**The fakes, by label:**
- Draft A's verifier's Break 1, the triple turn summed with no pawl (meshes.meshes_of's odd_sum and meshes.skewed): replaced by change 1.
- Break 2, the turnover keeping the stored sweep while flipping the pawl (hands.signs [1, -1] in Clock.reverse for a coupled hand): replaced by change 2.
- Draft A's F4, written for its phenomenon: replaced by the budget identity, a second reading that can fail.
- On the twin hands, draft E's turnover (T in the gears with the pawl): T is moved into the count, applied once.

**The law's text that changes (Sofer's sentences, on the owner's word):**
- Line 1602's "every charge conjugated (the Wronskian odd under the swap)" becomes "every charge kept".
- Its run back "(M z)* = M* z*" becomes the plain exchange under the same pairs. This brings the background's signs at the turnover: the count kept (the ratchet negated as well as exchanged), the offset's time gear and the regulator's flows negated (P13).

**The rows that move:**
- The charge's rows: 17, 65 and 70, which read the typed senses (section 16), and 67 (CPT).
- Every chart moves at every pawl wall with an odd gear or a flow, and at every turnover of a coupled hand.

**The contradictions with nature.** Charge conservation, exact in nature, is still not exact on the board after these two changes. The inflow, the rates and the click's units (section 8) stand under section 18's root I (the head's fakes) and root VI (the course).

## 8. OPEN

1. **The turned clocks' inflow** (P6). It is up to 44,542 vacuum sweep units in a tick on nature, 233,678 summed over 60 ticks. It is blocked by law 4's mirror of the held pre-state: the top must be passed once, and the stepped mirror locks a two-cycle. A turnover that keeps the tick's inflow needs a trigger or a mirror on the time-Mesh that passes the top once. That is R9, the turnover as the time gear's own carry: David's.
2. **The rates' motion** (P8). It is up to 878,451 in a tick on the hole. The momentum's carry into the next tick's charge unit is a second division with its own remainder per gear. It is blocked by the owner's decision of 2026-10-19 (line 805: "no second carried integer"). The owner's.
3. **The click in the charge's unit** (P10).
   - The fitted hand needs a shape whose sweep is one quantum in each end's unit, laid in its end's frame. With one shape for every Node-clock the pair's Q* is sigma AB (u_x - u_y).
   - The unspringing needs a write that leaves the pair's net charge in place, the quotient leaving as light and the remainder staying (law 11's form).
   - This ties to draft A's OPEN 8 (the fitted hand's shape): David's.
4. **The background at the turnover on the head's dynamic trains** (P13). The offset's own pulls and the stress's centred gradient read their neighbours with no pawl, so the head's whole step is not covariant under the Z2 beyond the hand's transport. The count's and the flows' signs at the turnover are proved on a static background only: the Boss's and David's.
5. **The twin hands' count modulo 4 on the board.** It needs the pawl and one more tooth (draft E's item 3); the head reads the twins per gear with K. Draft E's.
6. **The turns' rounding.** It is exact only for the four Gaussian units, so no continuous Mesh phase is exactly unitary on Z[i]. It stays booked (P7d).
7. **The protocol's steps 5 and 6.** The verifier is to be named on the board. Sofer's law check and David's sign-off are owed.

## A big law above?

**The law above:**

> The one act is the stationary act of one action of the clocks. Every weight is a Mesh's, in space and in time. Every frame is a gauge of that action. The turnover is the action's own time reversal.

**What it does:**
- Change 1 follows in one line: a real action has a Hermitian Mesh term, and a gauge-invariant one reads every gear in one frame.
- The weights' break goes: the kinetic term lives on the time-Mesh, read from the tick's two ends alike, as the tension lives on the Mesh.
- Change 2 follows: the action's T is applied once, and the charge is T-even.
- Every charge and current of a symmetry is then conserved at once by Noether's theorem, exactly in the rationals: the hand's U(1), the torus's translations as momentum, the 24.
- On the integers each is conserved up to its carried remainders, booked: law 11 at the carry, line 785.

**The small laws it cancels or rewrites:**
- the separately written weights of the conserved form, the charge and the bilinears (lines 773, 721, 803): one weight per Mesh;
- "the clock is the Node-clock's" for the time part of law 2, so s and mr are read at the time-Mesh;
- line 1602's "every charge conjugated", and the head's per-reading frame rules (`seen`, the count, the triple), which become one rule;
- draft A's F4 gate.

**The small law it contradicts:** the owner's decision of 2026-10-19, "Rule3 unchanged, no second carried integer" (line 805). The time-Mesh weight carries the momentum into the next tick's unit, which is one more carry per gear. This goes to the owner for approval, as the owner's word of 13:21 UTC asks.
