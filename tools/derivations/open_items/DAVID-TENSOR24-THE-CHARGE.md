# The charge the one formula keeps: Q*, its two breaks, and what they leave

David, 2026-10-28, 14:1x UTC, for the Boss (Sofer and Animate copied). This page answers the Boss's findings of 6468334029, from draft A's verifier: the step keeps a charge Q*, the sweep weighed by the pawl's sign and the mesh rate, and two breaks stand. The first break is the triple turn summed with no pawl; the second is the turnover flipping the pawl while it keeps the stored sweep. It is the board's item I as well, which the Boss's helper took. This page can serve as I's second hand, or the reverse.

A helper drafted it, and I reran its eighteen probe runs; the outputs are identical, byte for byte. They are in DAVID-TENSOR24-THE-CHARGE_CHECKS.txt, with the draft's proofs in full. The probes import the head read-only and patch it in memory, on toys-5's src (engine-5.0-test's, last changed at 834cfd72e). Sizes are in VSU, in which a fitted hand at the vacuum carries e = 18,000. The charge's rewrites are named QR1 to QR4, so that the fakes' R1 to R14 keep their labels. This page covers protocol steps 1 to 4. A second hand follows, then Sofer's check and my sign-off. No src is pushed.

## 1. In the clock: what the charge is

1. **A hand's charge is its turning sense:** the area its hand sweeps from before to now, read through the pawl (which way the ratchet faces), weighed by the tick's own stretch and Mesh rate.
2. **The clock keeps it for a reason:** the pull is unchanged when every hand is turned by one angle in its own pawl's sense (Noether). So what one Node-clock loses, its Meshes carry to its neighbours, if every Mesh couples its two ends alike.
3. **The head breaks it in two places:**
   - on a pawl wall, the triple turn is summed with no pawl, so the Mesh's two ends see different turns;
   - at a turnover, the pawl flips while the stored sweep is kept, so a turned clock's charge reverses.

## 2. The formula and its proofs

1. **The density.** With a the hand now, a- before, P = W (a - a-) + rho the step's own stride, and eps = 1 - 2b the pawl's sign:
   - d = -eps Im(conj(a + a-) P), the stride crossed with its midpoint.
   - Of the three densities tried, its integer remainder term is the smallest, and it is odd under the exchange of the two slots.
2. **Its step is an exact integer identity at every Node-clock:**
   - dd = -eps (X Im(conj a F) + X Im(conj a F)) - eps (tau + tau+), with tau = Im(conj(v) rho) Rule3's torque.
   - PROVED. CHECKED: 60,000 random states (both teeth parities, to 200 bits), and every live clock of 2,016 hand-ticks over 14 engine runs. Dropping the torque fails 138 of 180 hand-ticks on the hole.
3. **The Meshes carry the whole flux:**
   - X Im(conj a F) = X p^2 SUM_j S_j Im(conj(a) m_j), with S_j = 2 Q_j pinion read the same from both ends (456 of 456).
   - The flux J_j = eps S_j Im(conj(a) U K^f a_y) is antisymmetric if and only if Re U_yx = Re U_xy and Im U_yx = -f Im U_xy. PROVED.
   - The offset's pair meets the condition on every Mesh (40,000 Meshes). The head's triple meets it only off the pawl walls.
   - On a wall the defect is exactly 2 eps_x S Im(t) Re(o conj(a_x a_y)): 19,952 of 19,952 walls, and 456 of 456 hand-ticks of the engine's own transport.
4. **Noether's pairing and the charge.** With lam = 1 / (X p^2):
   - SUM eps lam X Im(conj(a) F) = 0 exactly when the condition holds (24 of 24 tori with the rewrite; nonzero on 24 of 24 with the head).
   - So Q*_t = SUM_x lam d / 2 obeys dQ* = -SUM_Meshes T - SUM_x lam eps (tau + tau+) / 2, bit for bit at every hand-tick of every run (exact rationals).
   - In the exact rational toy it is kept to the last digit at 84 of 84 ticks with QR1. With the head's triple it moves at 84 of 84.
5. **The law's weight:** at rates fixed in time, Q* = T SUM eps S / p^2. That is the law's 1/p^2 on the sweep (ALGEBRA.md line 721 on scribe-5), with the pawl's sign the clause lacks.

## 3. The two breaks, and their rewrites

1. **The triple turn summed with no pawl.** It moves Q* by up to 18,460 VSU a tick on the hole, 6,773 on polarization and 62 on nature.
   - **QR1:** sum the odd gear and the skew through the pawl, as the count already is: odd_xy = side (A_x + f A_y) and m_xy = 3 K side (V_x + f V_y).
   - This meets the condition on every Mesh (PROVED; 40,000 of 40,000). On the engine the transport's defect is 0 at every Mesh-tick.
   - It reads the start's gears alone, so the rewind is kept: 30 ticks there and back, bit for bit on the hole and nature.
2. **The turnover reverses the turned clock's charge.** It moves Q* by up to 1,370,210 VSU a tick on the hole (76 e), at 6,534 turned clock-ticks.
   - **QR2:** the turnover exchanges a hand's two slots with no conjugation (hands.signs [1, 1] at clock.reverse), each fine tooth mirrored once. Then eps' S' = eps S and d' = d, and the turned clock's stored sweep turns with its pawl. PROVED; CHECKED (60,000 draws, and every turned clock-tick of every QR2 run).
   - It is an involution, so the rewind is kept (60,000 draws; 30 ticks bit for bit; QR2 spelt with no involution fails).
   - **In the birth frame, QR2 is the antiunitary K on the hand,** which keeps the charge, as nature's time reversal does. The head's turnover is there the plain exchange, which reverses every charge. That is the law's own clause, "every charge conjugated" (line 1602), so QR2 changes the law: the owner's, through section 30, item 11.
   - **It moves the clicks:** on nature, births go from 3 to 20 and unspringings from 0 to 17 in 60 ticks, so the click must read the framed charge.

## 4. What QR1 and QR2 leave (each exact)

1. **The step a split top discards** is the flux out of the turned region: up to 133,926 VSU a tick on the hole.
   - **QR4, a candidate:** the turned clocks' Meshes held at the teeth for the tick of their turnover.
   - The turned set is known before the hands' carry (420 of 420 hand-ticks). The rewind is kept, and kept at 32 of 32 split tops in the toy.
2. **The weights' move:** lam belongs to the tick, and X p^2 / Gamma^3 runs from 0.034 to 1.058 on the hole. It moves Q* by up to 931,360 VSU a tick there.
   - **QR3, a proposal:** the Mesh's coupling read the same from both ends with the stretch inside, G_j = Q_j pinion (X_x p_x^2 + X_y p_y^2). The charge's weight is then 1, and the charge is the run's, not the tick's (toy: 84 of 84; engine: every book closes bit for bit).
3. **Rule3's torque and the turn's rounding** remain. With QR1 to QR4, the step and the turnover move Q* by them alone: at most 13,696 VSU a tick on the hole (0.76 e), 2,242 on polarization and 361 on nature.
   - The torque is intrinsic: no quadratic charge of one state escapes it. A free hand keeps its plain sweep bit for bit (60,000 ticks); a lone sprung hand does not.
   - The rounding, at most 613 VSU a tick, goes with an exact transport: U a as one Gaussian product over the Mesh's denominator.

## 5. The clicks: the book can fail, and does

1. **Takes** (the chimes, which unwind the light) keep Q* at 4,201 of 4,201: the light carries no Q*.
2. **Fittings** keep it at 64 of 89: all 64 on the uniform bang, 0 of 22 on the hole and 0 of 3 on nature. There are two exact causes:
   - F1's senses keep the plain sweep, not the framed one, so a pair born on a wall carries about 2 e (10 of 22 on the hole). The fix: sigma_y = -f sigma_x (toy: 20,000 draws);
   - the fitted hand's A B is one number at every clock, while Q* weighs it by lam W, about X / Gamma. So a pair across a stretch gradient is born charged, up to 603,228 VSU on the hole even with the senses fixed. **OPEN, and a contradiction with nature:** the charge's quantum would depend on the clock's stretch.
3. **Unspringings** keep it at 0 of 8. The sense is read on the start's plain sweeps while the pair is unwound after the turnover (3 of 6 on the hole unwind two charges of one framed sign), and evolved pairs do not cancel.

## 6. A big law missing above? (the owner's 13:21 and 13:26 words)

1. **For the charge: every Mesh couples its two ends alike.** That is one coupling read from both ends, and a turn that is antisymmetric through the pawl. With it the force is self-adjoint, Noether's pairing holds, and the charge is kept by the clock's own symmetry (QR1 with QR3). It contradicts two small laws of the head: the triple summed without the pawl, and the per-end weights in X F.
2. **For the turnover, three drafts point one way:**
   - **draft E:** the head's K on the twin hands breaks the 24 at every turnover. The twins need T = i sigma_y K (E's e5);
   - **my triggers helper:** the regulator's three flow gears are odd under T, but the turnover mirrors them as even. Corrected, T S T = S^-1 holds to the last integer;
   - **this page:** the turnover reverses every charge, where an antiunitary T in the birth frame keeps it (QR2).

   **One sentence covers all three: the turnover is the kind's own phase reversal T on every gear.** That is i sigma_y K on the twins and K on a hand in its birth frame, with each gear even or odd as T makes it. It is generic, it is a row of the kind table, and it commutes with the 24. It contradicts law 4's mirror and line 1602's "every charge conjugated", so it goes to the owner.

## 7. What it replaces, and what stays OPEN

1. **Replaces:**
   - the plan's "the charge's conservation derived from the one formula" (section 19). It becomes: "The one formula keeps Q*_t = SUM eps Im(conj(P)(a + a-)) / (2 X p^2), tick by tick, to Rule3's torque and the turn's rounding, where QR1 to QR4 hold; the clicks keep it only where the lay's two ends share one frame and one weight (OPEN)";
   - R1 of the fakes (click.py:95). The merger's sense is to be read in the pawl frame on the board it unwinds, and the lay's senses as sigma_y = -f sigma_x;
   - the law's clause at line 721 (and lines 799 and 803). It holds for a free hand. On the coupled lattice it keeps SUM eps (W/X) S / p^2 only with QR1, and its current is the pawl-framed I_ij, not G_ij.
2. **OPEN:**
   - the clicks' quantum of charge against the weight;
   - the torque, booked as a remainder or bounded;
   - an exact transport for the rounding;
   - QR2's consequences for the click's senses, for the retrace through a top, and on the twin hands;
   - the dynamical cost of QR3 and QR4;
   - the stopped clocks, whose weight is 0;
   - the frame the odd gears hold.
