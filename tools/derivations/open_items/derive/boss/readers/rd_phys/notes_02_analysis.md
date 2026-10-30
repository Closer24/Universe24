# rd_phys notes 02: analysis before the probes

## What the root dial IS (derived, my own reading)
- Static act: omega^2 = D/W, c^2 = grip/W -> the proper rate N = sqrt(rest/W). In GR with zero shift, g_00 = -N^2,
  so W/rest = 1/N^2 = g^00 (the plain inverse metric's time slot, flat slices). The law's "linear in c" makes the
  00 slot the inverse metric's time slot. Consistent.
- A scalar under a lapse N(t), flat slices, fixed spatial metric: d_t((1/N) d_t a) = N (Lap a - V').
  With 1/N = L/L_rest, L = sqrt(W): L d_t (L d_t a) = F. The root dial's equation. DERIVED (standard).
- L = sqrt(W) = L_rest/N = the time leg of the INVERSE tetrad, e_0^t = 1/N. So "L is tetrad-like" is right for the
  time leg alone. The quaternion frame Phi = (L, l) with l_k = -L N^k is ADM's (lapse, shift) packaged as e_0.
- The frame's square M = Phi Phi^T is rank 1 (their own: every 2x2 minor 0). A rank-1 symmetric tensor is no
  metric (3 null directions, no inverse, no cone). The inverse metric is g^{mu nu} = -e_0 e_0 + sum_i e_i e_i:
  the frame gives the FIRST term alone. Its kk slot -l_k^2 is the shift's contribution to g^{kk}, not the spatial
  metric h^{kk} (the grips). So "kk = l_k^2 = the grips" misidentifies the shift squared as the length slots, with
  the wrong sign. Re(Phi^2) = L^2 - |l|^2 is eta(e_0, e_0) with the FLAT eta on the components: a number, not the
  interval (g(e_0, e_0) = -1 by orthonormality; eta(e_0,e_0) is nothing).
- Carrying the frame's four gears: the square train already has kinds [A1, T1, A1, E, T2]; (L, l) is A1 + T1 = its
  first four rows. So "carry the frame" changes no kind; it changes two READS: W = L^2 (the root dial) and
  g^{0k} = L l_k (term 10, OPEN). The six spatial slots (A1 + E + T2) must stay independent gears or there are no
  tensor polarizations (E, T2 are the shears). "Extended to the space legs" (their words) would kill them.

## The dropped remainder (the central price)
- The push enters as q_F = round_odd(F / L(now)), the remainder dropped. A push below L/2 per round does NOTHING,
  for ever: a floor on the force (Postulate 5: "a floor or a bound is an if"; "every bound is a clock's carry"
  with its remainder kept). The as-built act keeps the push's remainder in r and a small push accumulates.
- F_eff = L round(F/L): a staircase. At F = L/2: factor 2. Relative error <= L/(2F).
- The pull of one count of difference is grip = den Gamma^2 = L^2/6: relative error 3/L (1e-11 at the calibre):
  the deriver is right FOR THE PULL.
- The kick K = T_k s q_d with T_k = s = 1 (BUILT at 1): K = 1 per whole turn of the drive: below L/2 for every
  L > 2: the drive's path is DEAD under the root dial at the calibre (and at any L > 2) unless the strengths are
  of order L. probe_root_generic C hid it: L = 6..9, s = 3, T_k = 2 -> K = 6 q_d ~ L. A spring through the drive
  (with_spring: J = -2 f x, T_d = 1): dead for |2 f x| < L/2.
- "1 to 6 permille" is the dropped sum over pushes dominated by pushes ~ grip x 80 x 6 >> L: a sum, not a
  window, and not the floor. Overclaimed as the price's measure.
- No exact bounded-state integer form exists: F/L_now's remainder at dial L_now cannot be carried to dial L_next
  by a bijection (the kept-tooth failure on a falling clock, their 2 of 40). So the floor is intrinsic to "nature's
  form in whole numbers" with a moving L. The owner's condition 1 and nature's form collide here: name it.

## den = 6 k^2
- 6 den a square iff den = 6 k^2: den even and divisible by 3. The example's den 15162856759112389 =
  617 x 196613 x 124992409 (all three odd; den = 1 mod 4) is refused; the law's "den of the hand" 3311818282 =
  2 x 3529 x 469229 is refused (not divisible by 3, odd part not 3 x square). L_rest = 6 k Gamma. c^2 = 1/6 at rest
  unchanged. Lifts (den as a hypotenuse, K-S3's "two lifts at least"): den^2 = x^2 + y^2 has a nontrivial
  solution iff den has a prime = 1 mod 4; den = 6 k^2 has one iff k has: k in {5, 10, 13, 15, 17, ...}. And the
  prime exponents in den are all even (k^2), which changes the lifts' count/angles. A new structural condition on the
  seed (K-S3 says den is "chosen by its structure"; this adds one). Declared, the owner's.

## The cut (OPEN, not mine)
- c_00^2 / c^2 = (grip/L_rest^2)/(grip/L^2) = (L/L_rest)^2 = W/W_rest: the same second cone as before in W.
- The 00 row on the cut keeps the as-built law (v kept) while every other row keeps L v: a uniform clock change
  now also parts the 00 row's velocities from everyone else's by L/L_rest. Neither helps nor hurts the cone; adds
  nothing toward the 00 row's own law (their D: no bijection in either dial).

## Conventions
- probe_root.py (the physics numbers of EDGE2/ROOT) uses tie-even E.split; probe_root_generic uses half-open
  split_up (the owner's). The physics does not depend on it (mc_phys). I will run the owner's half-open.
