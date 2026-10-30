# The readings, checked against the head: momentum, current, stress, spin, angular momentum and helicity

David, 2026-10-28, 12:0x UTC, for the Boss (Sofer and Animate copied). This confirms the Boss's readings' drafts in TENSOR24.md section 19, mine under its protocol. Each reading is checked three ways:
- its formula against the code;
- its kind under the 48, the 24's turns with the inversion;
- its second reading, from the click record.

A helper drafted four probes, and I reran each; the outputs are identical (DAVID-TENSOR24-THE-READINGS_CHECKS.txt). They are read on toys-5, whose src is engine-5.0-test's (8b657aa57, the same at 987cacf4f). The probes use integers only. Random fields lie on a 5^3 torus (3^3 for the twins). The click record comes from the head's own worlds: nature (20 ticks), hole (23) and polarization (12), with the state captured in memory just before and after every click. No src is pushed.

**The verdict.** One reading holds as drafted: helicity, and that only as a kind. Stress is confirmed with a frame caveat. Momentum, current, spin and angular momentum need corrections. The worst finding is the momentum gate: the pushes the clicks book do not add up to the state's change on 31 of 34 clicks. The cause is fully accounted for.

## Momentum: CORRECTED

1. **The formula:** P_a = sum over the hands of 2 p_h times the sum over x of [Re(conj z_now(x + e_a) z_before(x)) - Re(conj z_now(x) z_before(x + e_a))]. Here p_h is the hand's pinion (unwind.py:42-54), and P is positive along a wave's motion.
2. **The head's flows** compute T_0a = sum over the hands of p_h Re(conj(u_in + u_out) (z(x + e_a) - z(x - e_a))).
   - u is the odd rounding rates.rounded(2P + 1, 2 teeth X) (tick.py:231-234).
   - The gradient reads the neighbours' raw gears (meshes.py:135).
   - Summed over the node-clocks, sum T_0a = -(P(t - 1/2) + P(t + 1/2)) / 2. PROVED; CHECKED on 360 random fields.
3. **The draft's three errors:**
   - its sign: the draft's quantity is -P;
   - it has no pinion weight;
   - it equals -P only where the stretch is held through the tick. On the engine the identity holds at 252 of 252 hand-axis-ticks where u_in = a - a- and u_out = a+ - a, and it fails at 339 of 624 overall.
4. **"Tallied on the regulator's flows" is CONFIRMED,** at times rate^2 (tick.py:256). The odd rounding chooses its fine tooth by a sign comparison (core/rates.py:19).
5. **Kind: T1u.** A bond's momentum reverses when its ends are exchanged. PROVED; CHECKED on all 48.
6. **The second reading, the booked pushes** (run.py:85-87, 95, 135, and the takes' dP_take), fails on 31 of 34 clicks against the state's change across the click: 13 of 14 on nature, 10 of 10 on hole, 8 of 10 on polarization.
   - **The cause, accounted for on 34 of 34:** takes are pushed on the tick's start board (CL-S2, unspring.py:190 and 235), and lays on the live board (unspring.py:42). On those worlds, 141 of 461 start-board pushes differ from the live board's.
   - **With every push read on the live board, the gate is exact on 34 of 34.** That is the cut.
   - **Two pushes are booked nowhere in the log:** the release's (tick.py:312-314, kept only in the rewind note: 33 advances on those runs), and a split's moves (bobs.py:178).
   - **Row 71 is the drive's carry identity.** It cannot fail (1,539 of 1,539). The draft also cites "K5", which nothing in the repository defines.

## Current: CORRECTED

1. **The formula:** J_a = Im(conj z (K z(x + e_a) - K z(x - e_a))), where K conjugates the neighbour by the pawl, without the mesh's turn (hands.py:26, 48-55).
   - It sources the offset as the sum over the hands of the coupling times J (tick.py:153-156), carried into the kick at T (tick.py:221-226). Bit for bit on 55 of 55 ticks.
   - The coupling is min(spring, 1) (meshes.py:23), a clamp already on the fakes' list.
2. **Kind: T1u** (48 of 48). J is covariant when the pawls' frame changes (200 of 200).
3. **The continuity does not close with J.**
   - J_a(x) = B_a(x) + B_a(x - e_a), where B_a(x) = Im(conj z(x) z(x + e_a)) is the flux on one bond. PROVED; CHECKED 600 of 600.
   - The continuity's flux is the bonds' divergence, and J's centred divergence differs from it on 200 of 200 fields.
   - **The head's exact continuity** (PROVED; bit for bit on 208 of 208 hand-ticks) is: w_div W(a+, a) - w_side W(a, a-) = -X Im(conj a F) - Im(conj(r+ - mid) a) + Im(conj(r - mid') a), with F the pull.
4. **The click record books no current: OPEN.** It does book the charge: the change across the click is the sum of the couplings times (W_children - sweep(stood)), less the couplings times sweep(taken_levels). CHECKED on 55 of 55 clicks, 12 of them with a birth and 4 of those changing the charge.
5. **A name collision:** the chart's clock line `current` (run.py:292) is the light's mesh lead, a flux like momentum, not J.

## Stress: CONFIRMED, with the pinion weight and a frame caveat

1. **The formula:** T_aa = sum over the hands of p_h |z(x + e_a) - z(x - e_a)|^2 (regulation.py:15-19, tick.py:237-238).
   - Its trace feeds the time gear's drive. That drive is clamped at plus and minus the hold (tick.py:255); the clamp lies in the use, not in the stress.
   - The traceless 3 T_aa - tr drives the tension gears (regulation.py:22-25).
   - The shears are struck.
2. **The frame caveat.** The gradient reads raw neighbours, while the sprung hands' pull reads them through the pawl (tick.py:142, clock.py:135).
   - The two differ at 2,375 node-clocks in 51 of 208 hand-ticks.
   - The stress is not covariant when the pawls' frame changes (fails 200 of 200). It should read through the pawl, as the pull does.
3. **The kinds:** trace A1g; diagonal A1g + Eg; traceless Eg; shears T2g. CHECKED on all 48.
4. **The second reading is OPEN, and mine:** an exact relation between the stress and the regulator's response in the log.

## Spin: CORRECTED (the draft must say which bilinear it means)

1. **The head computes no S.** The split reads |W_up| and |W_down| (bobs.py:161-170): the z part of the sweep bilinear W = 2 Im(n^dagger b), S_k = 2 Im(n^dagger sigma_k b), with W_up = (W + S_z) / 4 (4,000 of 4,000).
2. **The draft's one-slot S = psi^dagger sigma psi:** S . S = rho^2 by Lagrange's identity (PROVED; CHECKED 4,000 of 4,000). Its sigma matches the Pauli gearing at tick.py:193-196 (1,500 of 1,500).
3. **The sweep bilinear has S . S = W W only for a pair turning rigidly** (4,000 of 4,000), and not on a general pair (4,000 of 4,000). DAVID-TENSOR24-PAULI.md gives the exact form: W W - S . S = -4 N(det[now, before]).
4. **My own convention,** in DAVID-TENSOR24-THE-CLICK.md, has the opposite sign on S_y. Every share reads only S . m, so nothing there moves, but the plan should name one convention.
5. **Kind: T1g, only when 2O acts on the twins through a Gaussian matrix M(R).** Then S goes to lam det(R) R S (48 of 48). Under the head's images, which move only node-clocks, every component is a scalar (48 of 48).
   - lam = 1, exact on the gears up to a global phase, on 8 rotations: the identity, the three half turns, the two quarter turns about z and the two half turns about x + y and x - y. That is D4, the rotations about the twins' axis.
   - lam = 2 on the other 16.
   - This corrects DAVID-TENSOR24-THE-CLICK.md's check 10, which said the quarter turn about z doubles the reading. That page takes the correction at its next edit.
6. **The second reading** is the split's fields (bobs.py:188-198). The up fraction should match the sum of |W_up| over the sum of |W_up| + |W_down|. The test is statistical and can fail. OPEN: no test universe holds twin hands.

## Angular momentum: CORRECTED

1. **The head has L only from the clicks:** row 72's walk, the sum of moment(arm, dP). The moment is arm times push (symmetries.py:259-261), with arm = 2x - (cube - 1) measured from the great clock's centre (symmetries.py:271). There is no window and no S term.
2. **The state formula that matches it** is L = the sum over the bonds of arm times (p_a e_a). A one-site advance changes L by exactly moment(arm, push). PROVED; CHECKED 300 of 300.
   - It is not covariant under a translation on the torus (fails 40 of 40); off the wrap it is (40 of 40). So the draft's origin and window are needed.
3. **Kind: T1g** (48 of 48).
4. **The second reading,** the walk against the state's change in L, fails on 31 of 34 clicks, for momentum's cause. Row 72's "closed" is identically 0 by row 71's identity: PROVED, and it cannot fail.
5. **The "+ S" term is OPEN:** the head has no S, and S scales by lam where L does not.

## Helicity: CONFIRMED as a kind only

1. **S . P is A1u when 2O acts on the twins** (48 of 48). Under the head's images it is not kept (fails 47 of 48).
2. **The head's stand-in is the twist** (meshes.py:150-158): A1u summed, A1u + Eu per axis (48 of 48), in integers. It is the lead field's helicity, not S . P.
3. **The second reading:** a moving birth's logged node, minus and plus record the signs of both the lead and the twist exactly.
   - The node is the end the lead flows into (17 of 17).
   - plus equals node exactly when the twist is right-handed (17 of 17).
   - PROVED from click.py:88-101; predicates.twist_of_fitting counts it correctly.
4. **The gate of S . P against the twist is OPEN.**

## For the Boss

1. **Cuts:**
   - every push read on the live board, which makes the momentum and angular momentum gates exact (34 of 34);
   - the release's pushes and the split's moves booked in the log;
   - the stress read through the pawl's frame;
   - one sign convention for S, named;
   - the readings' drafts corrected as above: momentum's sign and pinion weight, the current's bond flux, spin's bilinear and its kind through M(R), the origin of L.
2. **OPEN, mine:**
   - the stress's second reading;
   - the current in the click record;
   - spin's statistical gate on a twin universe;
   - the "+ S" of angular momentum;
   - the S . P gate against the twist.
