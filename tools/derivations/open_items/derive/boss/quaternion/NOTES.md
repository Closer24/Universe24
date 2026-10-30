# quaternion: working notes (saved as I go; the derivation goes to ONE_ALGEBRA.md)

## Read (t24b main 9067de20d)
- engine/step.py: gear (q, kept = carry(w (a - b) + push, w, r); a+ = a + q; b+ = a), drive (carry(J, T_d, rd)),
  sources (F = pull; gradient; readings = (a, grad, F, unit); J = contract(plan, ...)), driven (s (F + T_k q)),
  weight (W = rest + read(clock, a)), tick, mirror ((b, a, flip(r, W(b)), flip(rd, T_d))), untick = mirror tick mirror.
- engine/contract.py: pushes (each monomial pushes each leg by -f times the other three), contract, read (linear read).
- engine/mesh.py: seen (a[:, nb]), gripped (the ii slots at both ends), pull (sum over 6 Spokes of grip (nb - own)).
- engine/kinds.py: the 24 as signed permutation matrices of det 1 (rows three Spokes), kinds A1, A2, E, T1, T2.
- engine/state.py: State(a, b, r, rd); Layout(nb, spokes, meshes, grip, gearing, plan, clock, stretch).
- algebra/carry.py: carry(n, d, r) = divmod(n + r, d); flip(r, w) = w - 1 - r; lit.
- runner/load.py: W rest = 6 den Gamma^2; every row reads the square's 00 slot at 1; grips den Gamma^2 + ii slots;
  s = T_k = T_d = 1; J's plan empty until G3.
- runner/board.py: 6 neighbours per site, wrapped by carry.
- examples/tensor24: shape 4x4x4; trains light (A1, part 2) and metric (A1, T1, A1, E, T2 = the square, 10 rows);
  den = 15162856759112389, full_rate = 1000.

## Sibling folders (not to redo)
- families/NOTES.md: the half-speed gear, Pauli, FS indicator; the spinor kinds need sqrt 2 (quarter turn's trace).
- click25/NOTES.md: the moving-clock defect, the half-tooth, the wind's click; their piece.
- edge/, g3_blind/: the moving-clock mend and the anchor; theirs.

## The key fact for task 1 (seen at once)
The act is LINEAR in the gear rows (a, b, r) at fixed W and fixed push, componentwise: every gear row is carried by
the same whole number W (per row, per site: W = rest + the 00 slot's count at that site). So three gear rows
(x, y, z) of a T1 train at one site form a pure whole quaternion x i + y j + z k, and the act on it is the
componentwise act. The quaternion product never enters the tick as built: only the quaternion SUM, the whole-number
scalar product by W and s, and the componentwise carry. The 24 enter only as the symmetry of the act (the turn
commutes with the tick), not as an operation the tick performs.

## Plan of the probes (decided before coding)
- q_lib.py: whole quaternions as 4-tuples of Python ints; add, scale, Hamilton product, conj, norm, componentwise carry.
- probe.py (task 1): the engine's own load on trains hand [A1, T1] (a whole quaternion), vec [T1] (a pure one), metric
  (the square: rows 0..3 a four-vector, rows 4..9 a symmetric 3x3 S); a plan through the 24's tables (spring f N(h),
  vertex g Re(h m-bar), triple product c3 eps(vec, h, m_0i)), s = 2, T_k = 3, T_d = 5, the 00 slot moving at some
  sites. tick_Q written on quaternions, compared with step.tick bit for bit over 6 rounds; mirror_Q vs step.mirror;
  untick_Q vs step.untick; the 24 as sandwiches g v g-bar / N(g) at standing W (24 of 24 expected).
- probe_units.py (task 2): each of the 24 turns = a Lipschitz g of norm 1 (12, Hurwitz units, A2 = +1) or norm 2 (12,
  A2 = -1: 1 +- e_a quarter turns, e_a +- e_b edge half-turns), the sandwich divided by N(g) with remainder 0; the
  tables C[T1 T1 -> A1] = -Re(vw) and C[T1 T1 -> T1] = Im(vw) up to measured signs; the four-vector product's five
  channels; Euler's identity; the Gaussian rule as the plane Z + Z e_a; the E and T2 slots outside Hamilton's product
  (det of a 10x10 whole matrix).
- probe_ring.py (task 3c): Lipschitz (deep hole (1,1,1,1)/2 ratio 1: no), Hurwitz (ratio 1/2), the octahedral order
  O_48 = {(1/2) SUM (u_m + v_m sqrt2) e_m : u all one parity, SUM v even} over Z[sqrt 2]: closure, the 48 units,
  sampled Euclidean steps against a central divisor d in Z[sqrt 2] (Nm N(y - q d) < Nm(d)^2).
- probe_time.py (task 3a): the lone swing J = -k v at W | k: k = W, 2W, 3W give whole time-turns of orders 6, 4, 3
  (k = 2W: (v, u) -> (-u, v), the Gaussian i); k = W + 1: the tooth moves, no ring.
- probe_square.py (task 3b): the metric's 10 slots = 1 trace + 9 two-sided sandwiches e_a h e_b; the change of basis
  needs quarters (det); the act reads 00 and ii as whole scalar weights only.

## Key algebra (derived while planning)
- The sandwich by g of norm 2 on a whole pure v is 2 (m v): the carry at 2 has remainder 0. So no whole-speed turn
  needs the root of 2; the root is needed only to make g a unit (norm 1), which the one-sided (half-speed) action
  needs. Check: (1 + i) v (1 - i) = 2 (x i - z j + y k) for v = x i + y j + z k.
- O_48 = H + (1/sqrt2) P with P = (1 + i) H = the Lipschitz quaternions of even norm; [O_48 : Z[sqrt2] (x) H] = 4;
  Z[zeta_8] = Z[sqrt2][i] sits in O_48 as the lifts of one axis's quarter turns.
- The time plane: v+ = 2 v - u - (k / W) v exactly where W | k; k = 2W is the Gaussian i on v + i u.
- Hamilton's words of degree 2 in one four-vector h reach a^2 +- |v|^2 and a v (five of the square's ten slots);
  the E and T2 slots (traceless symmetric) are outside: kinds A1 + T1 against E + T2.

## The carry theorem (derived 16:xx, for the coordinator's decisive question)
Setting: a half-speed hand psi in a lattice L (H = Hurwitz, rank 4, turned by G = 2T, the 24 units; or Lambda = O_48,
rank 8, turned by G = 2O, the 48), the turn the LEFT multiplication psi -> g psi. A carry at teeth W: n = W q + r with
r in a set D of coset representatives of L / W L (a fundamental domain; this is what makes (a) the run back exact).
1. The remainder must turn affinely: r -> g r + c_g with c a 1-cocycle (shown: phi_g(r) - g r is independent of r, since
   n + r = W q + r' with n arbitrary). The per-gear flip is the case c_{-1} = (W - 1) 1 on the negated rows.
2. Every integral cocycle is c_g = (g - 1) a with a in the rational algebra A (H^1(G, A) = 0); the class is trivial iff
   a in L (A^G = 0: g y = y forces y = 0 in a division algebra). The lifts of the third turns of order 6, g = (1 + i +
   j + k) / 2 and its conjugates, have g - 1 a UNIT (N(g - 1) = 2 - tr g = 1). So (g - 1) a in L forces a in L:
   H^1(G, L) = 0 for 2T and 2O. No flip-like twist exists; the domain D must be linearly G-invariant (up to a translation).
3. A G-invariant D exists iff every nonzero coset has trivial stabilizer: a coset x + W L fixed by g != 1 would need a
   point fixed by g, which is 0 alone, and 0 is not in a nonzero coset. g != 1 fixes a nonzero coset iff
   gcd(W, [L : (g - 1) L]) > 1. The indices: order 2 (g = -1): 2^rank; order 4 (N(g - 1) = 2): 2-power; order 8
   (N(g - 1) = 2 -+ sqrt 2, absolute norm 2): 2-power; order 3 (N(g - 1) = 3): 3-power; order 6: 1.
   => A carry on the hand turning with the 24's lifts (or the 48) exists IFF gcd(W, 6) = 1; where it exists D is a
   union of free orbits with 0, D = -D, the mirror's flip is r -> -r, and no per-gear form of it exists (families).
4. The load lays rest = 6 den Gamma^2 (the 6 = the Spokes): W = rest + a_00 is divisible by 6 at the vacuum, so on the
   act as built the half-speed carry turns only where the 00 slot's count is coprime to 6. W = 9 (families): 3 | 9, none.
5. Big Pic's division (nearest in each part) is a fundamental domain but (i) at the double farthest points with the
   two offsets orthogonal its remainder has absolute norm exactly Nm(d)^2 (no reduction; example y = 1 + i + sqrt2 j,
   d = 2), another quotient reduces (8 < 16): the Euclidean minimum is < 1 but not by that rule alone; (ii) the
   nearest point has ties even at gcd(W, 6) = 1: W = 5, the coset of (-5/2, 1/2, 1/2, 1/2) ~ (5/2, 1/2, 1/2, 1/2), both
   of norm 7, so "nearest" is no function without a choice, and a lexicographic choice is not equivariant.
6. Whole-speed hands: monomial action, the box [0, W)^n with the flip twist is invariant (sym24); the centred box is
   the nearest-point rule there and equals the built carry with every tooth counted from the middle (odd W).

## Results so far (all probes run; outputs beside them)
- probe.txt: tick_Q == step.tick 6 of 6 rounds on three lays (rising, standing, varying 00 slot), plan through the
  tables (spring, vertex, triple product), s = 2, T_k = 3, T_d = 5; mirror_Q == step.mirror; untick_Q == step.untick;
  6 unticks return the rising lay (promise holds there); W (a+ - 2a + b) = push + r - r+ every round; the 24 as
  sandwiches: 12 Hurwitz units (A2 = +1), 12 Lipschitz g of norm 2 (A2 = -1), carried at N(g) with remainder 0;
  turned run == run turned 24 of 24 at standing W (mutant without the flip 3 of 24); with W moving [24, 3, 3, 3].
- probe_units.txt: tables = Hamilton's product (0 misses of 300 each); Euler 0 misses; the Gaussian rule is the plane
  Z + Z e; Rule3's box remainder has norm >= W^2 in 307 of 500 draws (not Hurwitz's remainder); Hurwitz's remainder is
  not unique (n = 1, W = 2: q = 0 and q = w both reduce).
- probe_carry.txt: fixed nonzero cosets of H / W H and Lambda / W Lambda per lift order: 2 | W: orders 2, 4, 8;
  3 | W: order 3; none at gcd(W, 6) = 1 (W = 1, 5, 7, 11); indices [Lambda : (g - 1) Lambda] = 256, 81, 16, 1, 4 by
  order 2, 3, 4, 6, 8; the orbit domain at W = 5, 7: 0 conflicts, equivariant and symmetric on every coset; at W = 6, 9
  conflicts 97, 64; nearest-point ties: 192 of 625 (W = 5), 576 of 2401 (W = 7); on the act (lone clock, spring):
  orbit domain 24 of 24 lifts at W = 5, 7 with the run back exact; per gear 1 of 24; (rerun with 20 starts pending).
- probe_time.txt: k = W, 2W, 3W return after 6, 4, 3 rounds bit for bit, teeth still, the wind kept; k = 2W is
  (v, u) -> (-u, v); k = W + 2 the teeth move, no return; k = 0, 4W parabolic, no return.
- probe_square.txt: the ten forms' determinant -48 (E and T2 slots outside Hamilton's degree-2 words); the nine
  sandwiches E_ab symmetric and traceless; change of basis determinant -128; the act reads 0i and jk by nothing
  (spring alone: next hands equal), and through the vertex where a plan reads them.
- probe_ring.txt: Lipschitz fails at (1 + i + j + k) / 2; O_48: Big Pic's rule reduces 129 of 132, the box 132 of 132,
  worst least ratio 1/2; the double farthest point 1 + i + sqrt 2 j at d = 2: the rule gives ratio 1 (no reduction),
  another quotient 1/2; zeta_8 in O_48 with zeta - zeta^3 = sqrt 2.

## Final runs (20 starts) and the hostile self-check
- probe_carry.txt (20 starts): orbit domain 480/480 at W = 5 and 7, run back 20/20; per gear (flip on +-I) 40/480
  at every W; nearest-lexicographic 213, 204, 150, 203 of 480 at W = 5, 6, 7, 9 with the run back 4, 4, 1, 2 of 20.
- probe_carry_big.txt: W = 13..1003: fixed cosets exactly where 2 | W or 3 | W; the load's rest teeth gcd 6 with 6.
- probe_units.txt: i -> j -> k under (1 + i + j + k) / 2; the commutant on T1 in [-1, 1]: 3 matrices, all scalar.
- probe_square.txt fixed: the 5 x 5 minor on (a2, x2, ax, ay, az) is -16 (first version took zero columns).
- probe_ring.txt fixed: the Hurwitz sample now divides by 2d (doubled coordinates): worst 8 / 16 = 1/2.
- Checks done: every probe rerun; the fixed-coset counts recomputed by hand from the indices (15 = 2^4 - 1, 18 = 6 x 3,
  64 = 8 x 8; 255, 270 = 18 x 15, 36 = 12 x 3, 640 = 8 x 80); cases built to pass the rules (W coprime to 6, composite,
  large) and to fail them; the mutants (no flip, lexicographic choice, per-gear act).
- ONE_ALGEBRA.md written: Answer, by Solution24, four layers, Big Pic's items, Measured, the deriver's check, the
  table, Open, Files.

## Last piece (the coordinator's refocus, Big Pic 6527540022 item 4)
- Big Pic's own "no" on the two decisive questions checked against the theorem and probes: agrees on all four points.
- probe_books.txt: conj(before) now = real + turn, real^2 + |turn|^2 = N(before) N(now): 0 misses of 500; real = the two
  A1 channels, turn = the two T1 channels with the cross: 0 misses; the Gaussian two-square 0 misses; kept round to
  round 12/12 at k = 2W (the real part negated, the turn kept), 0/12 at k = W, 3W; the edge: w p_out = w' (p_in + push
  + r - r+) 0 misses over 6 rounds (the momentum rescaled by W'/W: the determinant on the edge).
- ONE_ALGEBRA.md updated: Answer item 6 (Big Pic's no, the books, the edge), the edge paragraph, the books section,
  Measured 8, the table rows, Files.

## The double Node-clock and the quaternion (the owner's question of 16:3x; derived before the probe)
- A two-part hand (re, im) with its two slots (now, before) is four whole numbers; read as q = z_now + z_before j
  (Cayley-Dickson: q = re_1 + im_1 i + re_2 j + im_2 k), the hand's own phase (the winding, (re, im) -> (-im, re) on
  both slots) is the LEFT multiplication by i; the slot swap is q -> (i q i^-1) j; the time step at the quarter mode
  (k = 2 W), (v, u) -> (-u, v), is the RIGHT multiplication by j; left and right commute. Only at t = 2 - k/W = 0 is the
  step [[t, -1], [1, 0]] of the form [[c, -conj d], [d, conj c]] (a right multiplication by a quaternion); at other
  modes it is a split quaternion (M_2(Z), norm det = 1) acting on the (now, before) pair, outside H.
- The forward-backward differences: q (1 - j) = (now + before) + (before - now) j: the velocity is the j slot of the
  right multiplication by the norm-2 element 1 - j (a quarter turn's lift); the edge's dial D = W(b) + W(a) is the sum.
- The wind now^2 - next x before = (1/W)(W v^2 - (2W - k) v u + W u^2); at the quarter mode it is N(q) = |now|^2 +
  |before|^2 summed over the parts: the quaternion norm, kept because the step is a unit.
- The edge form (edge_lib): the tooth between the slots in the dial W(b) + W(a), centred, the mirror negating it:
  exactly the D = -D the orbit domain needs; the edge act at W | k is the same whole time-turn.
- fam_math's 24-gear train (the 48 on their 24 pairs +-g with the sign) is the group ring Z[2O] / (-1 = -1) of rank
  24; left AND right multiplication by units are signed permutations there (Cayley), so the per-gear carry turns with
  both sides; pi: f -> SUM f_p g_p maps it ONTO O_48 (the eight basis elements are units), equivariantly, with kernel
  the G3/2 part (rank 16); the carry does not descend through pi (a sum of carries is no carry of a sum), so the
  quaternion hand is a reading of the 24-gear train, not a carried gear: this is how the units become gears and the
  wall of gcd(W, 6) is bypassed (the group ring has fixed vectors, the orbit sums; the division algebra has none).

## probe_double.txt (the owner's double Node-clock; the edge act at W = 6 den Gamma^2, a lone clock)
- k = 2W: q+ = q j every round, the hand returns after 4 rounds with its tooth still, N(q) and the wind kept; the
  phase (i on the left) commutes 12/12; the mirror's swap is (i q i^-1) j with the tooth negated; 12 edge unticks
  return; q (1 - j) holds the sum and the negated velocity; the act as built gives q+ = q j too.
- k = W, 3W: the hand returns after 6, 3 rounds, the wind kept, q j false, N(q) not kept. k = 2W + 2: the tooth moves.
- the 24-gear train (fam_math): L and R all signed permutations, L a representation, R an anti-representation, they
  commute, -1 = -I, SUM tr^2 = 1152 = 48 (4 + 4 + 16), SUM tr(LL) = -384; pi onto O_48, equivariant both sides (0 of
  1600 twice); the per-gear carry does not descend through pi (100 of 100 at W = 7).
- Bugs of mine caught in the check: the period read on the whole state (the free square rows drift) -> on the hand;
  the trace label (384 was Lambda's number; the 24-gear train's is 1152).
- ONE_ALGEBRA.md: Answer item 0, the section "The double Node-clock", Measured 9, table rows, Open narrowed, Files.

## The root dial (the owner's 17:2x word; derived before the probe)
- The frame as a whole quaternion Phi = L + l_x i + l_y j + l_z k (an A1 + T1 train, a whole basis the 24 permute);
  its components along the Spokes Phi_mu = Re(Phi conj(e_mu)); the metric's ten slots are the symmetric square
  M_mu,nu = Phi_mu Phi_nu: 00 = L^2 = W (the time leg's square), 0k = L l_k (the tilt), kk = l_k^2 (the grips), jk =
  l_j l_k. N(Phi) = L^2 + |l|^2 = the metric's trace; Re(Phi^2) = L^2 - |l|^2 the Lorentz interval of the frame.
  W = L^2 = N(Phi) iff the space legs vanish (a pure-time frame); in general W = (Re Phi)^2.
- The root dial reads the frame's COMPONENT L at the first power (the dial L(b) + L(a), the push divided by L at the
  pivot and by L again at the dial: F / (L L) = F / N(L)); the W dial reads the norm. On the edge the (now, before)
  step has determinant D_in / D_out: the root dial's is the ratio of leg sums (nature's redshift v ~ 1/L = N), the
  W dial's the ratio of norm sums (~ the square). Neither is a unit on a moving clock; both are the unit [[2 - k/W,
  -1], [1, 0]] standing (the quarter mode q -> q j holds on the root dial too); both are shears (det 1) in (a, P).
- Not natural as built: the ten slots are ten independent gears, and the act's linear pull does not keep a square a
  square (to measure); the frame reading wants the frame's four gears carried and the square read, as the root dial
  does for L; the law's W = 6 den Gamma^2 + c is a square only if 6 den is (to test for the example's den).
- The two divisions by L are the two factors of N(L) = L conj(L): with space legs the natural division of a push by
  the frame is F conj(Phi) carried at N(Phi) = the metric's trace: the first place a quaternion divisor would enter
  the act (OPEN, the owner's).

## probe_rootdial.txt (the root dial in the algebra)
- the frame's square along the Spokes: 0 misses of 300 (slots, trace = N(Phi), 00 - sum ii = Re(Phi^2)); W = N(Phi)
  for the pure-time frame 300/300.
- the act as built on a metric laid as a frame's square: 27 -> 0 -> 0 squares (frame by site), 27 -> 27 -> 27 (uniform).
- the root dial standing (L = 60): k = 2 L^2 q+ = q j 12/12, period 4; k = L^2 period 6; k = 3 L^2 period 3.
- the free gear on the rising course: books exact 2000/2000; the norms 200/201 (root) vs 20000/20201 (W), the W dial's
  the root dial's square to the next order (808040000 vs 808020000).
- 6 den = 90977140554674334 is no square (between 301624171^2 and 301624172^2).
- Self-check: the component sign Re(Phi conj e_k) = +l_k re-derived (conj e_k = -e_k, Re(l (-e_k)) = l_k); the
  quarter mode on the root dial derived (q_F = -(k/L) a exact at L | k, the split at 4L exact at L^2 | k) and measured;
  the floor root checked by the neighbour square. The answer: YES it fits naturally (the first power of the frame's
  time component, the norm's two factors), and what does not fit is the act as built (ten slots as gears).
- ONE_ALGEBRA.md: Answer item R, the section "The root dial", Measured 10, a table row, Open (the frame train), Files.

## The two hostile reports (qa_math, qa_phys) and my re-check (RECHECK.md; nothing edited in place)
- qa_math 1 (BLOCKING) STANDS: the wall is for ONE dial; a quotient-dependent carry (the least of 24 images, centred
  box, conj(g) back) is equivariant, odd, bijective on valid states with the mirror (b, a, -r), at every W: my own
  rebuild (probe_recheck_q): 0 misses, 240/240 on the act at W = 5, 6, 9, run back 10/10; its remainder set is no
  fundamental domain (cell 0 holds 97, 145, 1057 of W^4). The theorem stands for fixed dials with its hypothesis.
- qa_math 2 STANDS: the twisted train has no fixed vectors (SUM L(g) = 0), det(L(g) - I) = 256 at order 6; the true
  reason is the carry's lemma (signed permutations).
- qa_math 3, 4, 5, 6, 7 STAND (scope: wherever the push is -2 W now; the reading vs the act; probe_double broke on
  edge_lib's new argument, fixed copy probe_double_fixed.py; ranks and Smith forms; wording).
- qa_phys 1 (BLOCKING) STANDS: the unit step is the doubler (the staggered mode on the example's piece, no spring,
  F = -12 grip a = -2 W a: probe_recheck_doubler 64/64, period 4; the long wave moves its teeth).
- qa_phys 2 (BLOCKING) STANDS: L_i and R_j commute, (L_i R_j)^2 = +I: C (+) C, not H in action.
- qa_phys 3 (BLOCKING) STANDS: the mirror is linear and commutes with the phase (classical T); Kramers' j
  anticommutes: two operations on one symbol; "the spinors are the same thing" is not shown.
- qa_phys 4 (BLOCKING) STANDS: the 24-gear carrier's price, 40 doublers per Node-clock, degenerate, pi's kernel.
- qa_phys 5-8 STAND (Cl(3,1) as the absent one algebra; one map read five ways; the line drawn on the teeth; hygiene).
- Waiting for Big Pic's word before the second text.
