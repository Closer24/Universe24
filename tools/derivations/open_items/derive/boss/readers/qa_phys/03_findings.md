# Findings on ONE_ALGEBRA.md (hostile physicist), 2026-10-30

Probes (all on step.tick, the act as built on main 9067de20d, or on whole 4 x 4 / 24 x 24 matrices; whole numbers and
tensor24.algebra.carry.carry as the one division; the example's universe read from its file, no train declared):
qa_lib.py, qa_a_doubler.py (.txt), qa_b_modes.py (.txt), qa_c_algebra.py (.txt), qa_d_train.py (.txt), rerun/ (the
draft's nine probes rerun: eight identical, probe_double.py no longer runs, see 02_rerun.md).

## VERDICT: NOT PASSED

## 1. BLOCKING. The quaternion of the slots is the lattice's cutoff, not nature's time.
Place: Answer 0 ("the double Node-clock IS Hamilton's quaternion of the slots ... at the quarter mode exactly"; "MEASURED
on the edge act at W = 6 den Gamma^2 (a lone Node-clock, the example universe's light hand, a spring k = 2 W)"); section
"The double Node-clock", MEASURED; table row "the double Node-clock as one quaternion"; Solution24 step 1 ("it follows
from the one act at W | k, nothing added").
Measured:
- qa_b_modes.txt: a lone clock, W = 60, every spring k = 0..4W (121 springs, 24 rounds): whole turns (teeth still, the
  hand returns) at k/W = 1, 2, 3 alone (periods 6, 4, 3); the Hamilton unit q+ = q j at k = 2W alone; in k <= W/10 none.
  At the load's W the quarter mode is a spring of 90977140554674334000000 per row: 4 sin^2(omega/2) = 2, a beat of 90
  degrees a round (the architecture's mass line): the heaviest beats below the band's edge (180 degrees at k = 4W). The
  example universe's light has no spring; the draft laid a cutoff-scale mass on it and called it light.
- qa_a_doubler.txt: the example's own piece (4 x 4 x 4), light with NO spring, the square at 0: the staggered mode
  (pi, pi, pi) gives q+ = q j at 64 of 64 sites every round, period 4, teeth still, SUM N(q) = 91264 kept; because
  F = grip (SUM_nb e(nb) - 6 e) = -12 grip a = -2 W a. Of the 64 Fourier modes 21 are whole turns (S = 6, 12), 1 the
  Hamilton unit (S = 12), 42 move their teeth (no unit of any ring); every whole one has |k_a| >= pi/2 on some axis. The
  law's line 33 puts light's c^2 = 1/6 "at the doubler's hold": the quarter mode is the TOP of that band (omega^2 = 2),
  zero group velocity: nothing travels there.
- Nature's hands (long waves, k/W ~ 0): the tooth moves and the step is a unit of no ring, as the draft itself says.
Fix: rename and re-scope: "the quarter mode is light's staggered mode at the top of its band, or a spring with
4 sin^2(omega/2) = 2; a structure of the lattice at its cutoff; nature's hands sit where W does not divide k and have no
unit". Strike "IS Hamilton's quaternion" and the word light for a hand with a spring of W. Measure on light's own modes.

## 2. BLOCKING. What acts on the slots is a commutative algebra; "only at the quarter mode" is a coordinate accident.
Place: Answer 0 ("the phase on the left, the time step j on the right, the two commute"); section "The double
Node-clock" DERIVED (i)-(v); Answer 7 ("the clock's own time plane is a second algebra ... one ring per mode").
Measured (qa_c_algebra.txt): [L_i, R_j] = 0; (L_i R_j)^2 = +I; (I + L_i R_j)^2 = 2 (I + L_i R_j): the algebra the phase
and the step generate is C (x) C = C (+) C, commutative, with a zero divisor; i j = -j i is never exercised by the act.
At every whole t in {-2..2} the step V_t = [[t, -1], [1, 0]] commutes with L_i, has det 1 and keeps its own form
v^2 - t v u + u^2 (twice: [[2, -t], [-t, 2]]); N(q) is that form at t = 0; V_t is a right multiplication by a quaternion
for t = 0 alone ((0, 0, 1, 0) in the box [-2, 2]^4). Physics: (now, before) is not a canonical pair; the shadow energy
W (v^2 - t v u + u^2) is the invariant of every stable mode and the step is a rotation in it; the quaternion norm equals
it only at t = 0. Over Z the three whole modes are three rings (orders 6, 4, 3: the crystallographic restriction, which
the law's own line 559 states): right, and of no physical selection content.
Fix: "the two slots of a two-part hand are a complex 2-vector (z_now, z_before); the time step at a whole mode is an
element of SL_2(Z) commuting with the phase; at t = 0 it is also R_j, and the quaternion is a bookkeeping of that
case". Answer "why only at the quarter mode" with the shadow form, not with Hamilton.

## 3. BLOCKING. Two different j's: the slot's time step and Kramers' time reversal; the mirror commutes with the phase.
Place: Answer 0 ("the mirror's swap of the slots is q -> (i q i^-1) j"; the frame "sync with Big Pic ... the spinors are
the same thing"); section "The 24 and the 48 as units" ("the time mirror ... a swap of the two slots with the tooth's
flip"); Answer 7 ("one algebra for space ...").
Measured (qa_c_algebra.txt): S = (i q i^-1) j = the swap, S^2 = I, [L_i, S] = 0: the mirror is LINEAR and commutes with
the hand's phase (S R_j = -R_j S). On the families' side (the 48 on the left, the phase R_i on the right) the Kramers
partner R_j anticommutes with R_i and squares to -I: Wigner's T for spin 1/2, antiunitary, T^2 = -1. The law's line 559
reads a plane's time reversal as anticommuting with J, Kramers needing a doublet. So the draft's j (a quarter-period
evolution, commuting with its phase) and the spinor's j (a reversal, anticommuting with its phase) are two operations
on one symbol. Physics: the draft's left i is the hand's internal SO(2), a charge, under which classical T is linear:
consistent for a classical board, but then it is not the quantum phase, and nothing of Wigner's T is on the board.
Fix: name the left i a charge rotation and the mirror the classical T; say in Answer 0 that the slot j and the Kramers
j are different, so "the spinors are the same thing" is NOT shown by this algebra (the draft's "two algebras" is the
right conclusion, for this reason).

## 4. BLOCKING. The 24-gear train carries spin 1/2 with five species' worth of doublers, degenerate.
Place: Answer 0 "The units as gears" ("this is how the units become gears and how the wall of gcd(W, 6) is passed: not
by a new carry but by a wider train"); section "The double Node-clock", last paragraph; Clicks bullet 2; Open bullet 1.
Measured (qa_d_train.txt, the group built from scratch: 48 elements, orders {1:1, 2:1, 3:8, 4:18, 6:8, 8:12}):
- the train's real content: E1/2 (4 gears) + E5/2 (4) + two real G3/2 (8 + 8); invariant symmetric forms 8,
  antisymmetric 16; the reading pi onto O_48 has rank 8 and kernel rank 16, and the whole projector 6 P_G (entries
  -1, 0, 1, 4; (6 P_G)^2 = 6 (6 P_G); trace 96) satisfies pi (6 P_G) = 0: the kernel IS the spin-3/2 part.
- per Node-clock with two slots: 48 real numbers; nature's electron (a Pauli 2-spinor in second order, Dirac's 8 real)
  is 8 of them; 40 are species nature does not have: the Galois partner E5/2 (sqrt 2 -> -sqrt 2) and two spin-3/2
  quartets. The Hurwitz hand (4 gears) has the right count and the wrong group (2T); the O_48 hand (8) has the electron
  and its Galois twin.
- under any spring f SUM x_p^2 all three kinds have one beat; the click's size SUM f_p^2 of 200 drawn hands is 675
  permille spin-3/2; a vector coupling (fam_math's 24 x 24 -> T1) converts E1/2 into G3/2 (1/2 x 3/2 contains 1).
- a whole invariant spring that splits them exists: M = a I + b D + c (6 P_G), D = (1/2) SUM_(order 8) sgn(Re g) L(g)
  whole with entries -1, 0, 1, D^2 = 18 (I - P_G); beats a +- 3 sqrt 2 b (E1/2, E5/2), a + 6 c (G3/2); the Pell pair
  (17, 4) puts the Galois twin's spring k below 1/1000 of the electron's (its beat about 1/34 of it) or the other way
  round. Nothing derives a, b, c: by the law's word a declaration. The E1/2 x G3/2 -> T1 channel exists (spin 1/2 x 3/2
  contains spin 1); whether fam_math's one seeded table lays it is the seed's.
Fix: state the carrier's price in the Answer: the electron's 8 numbers come with 40 of doublers, degenerate in mass,
the spin-3/2 part invisible to the quaternion reading and 2/3 of the click's size; nature has none; the half-speed hand
on O_48 is still a twin. Keep "rides the act" (fam_math's measurement) and strike "passed" for "passed at the price of".

## 5. MINOR. "Two algebras commute rather than unify": say what the one algebra would be and why it is absent.
Place: section "The double Node-clock" ("they are two algebras, not one"); Answer 7; Open bullet 3.
Measured (qa_c_algebra.txt): gamma^0 = L_i, gamma^a = L_j R_a give {gamma^m, gamma^n} = 2 diag(-1, 1, 1, 1) on R^4:
two commuting quaternion algebras acting on ONE quaternion from the two sides are M_4(R) = Cl(3,1), Dirac's algebra in a
Majorana basis, whose time gamma anticommutes with its space gammas. The draft's two act on different indices (the
slots x parts; the T1 rows, by the adjoint Ad(g), the vector representation, where Ad(i), Ad(j), Ad(k) commute: the
Klein group) and nothing anticommutes: no Clifford structure, no boost; time and space factorize (Galilean). Dirac's
first-order equation has no counterpart in a second-order (now, before) act; the slot pair is Klein-Gordon's (phi, pi)
(Feshbach-Villars' particle/antiparticle), not spin.
Fix: one paragraph saying so; the owner's "one big algebra of space and time" is Cl(3,1), and the board has no boost.

## 6. MINOR. The five quaternion readings are one map; the "product books" conservation is the same map.
Place: section "The double Node-clock" (i)-(v); "The click's product books" ("kept round to round only at the quarter
mode"); Answer 6.
Measured: at t = 0 the step is (z_1, z_2) -> (-z_2, z_1); q (1 - j), N(q), the swap, |before|^2 |now|^2 kept (next =
-before) are restatements of it (qa_c_algebra.txt, probe_books rerun identical). Fix: say "one map, read five ways".

## 7. MINOR. "Exact at the quarter mode" is a statement about the fine teeth, which no click reads.
Place: Answer 0 ("the hand returns after 4 rounds with its tooth still"); "where W does not divide k the tooth moves".
Measured (qa_b_modes.txt): at the load's W with the spring off the quarter mode by 1 or by 1000, the hand follows
q+ = q j in 12 of 12 rounds while the tooth moves in 12 of 12; off by 10^12, 4 of 12; on a clock rising by 1 a round the
hand follows j 6 of 6 while the tooth moves by 2 (n + 1) a. The hand's quotient sees a defect only when its tooth wraps.
Fix: say that the whole/not-whole line is drawn on the teeth; what a click would see of it is click25's.

## 8. MINOR (method). The main probe cannot be rerun.
Place: Files; "probe_double.py"; the deriver's check ("every probe was run at least twice").
Measured (02_rerun.md): eight probes rerun identical; probe_double.py fails at line 103 (edge_lib.turned_edge grew a
positional argument at 16:33:19 UTC, after the draft's run at 16:29:12); the act-as-built lines of the probe come
after the failure. Fix: pin a copy of edge_lib in the folder, or measure on step.tick alone (qa_a, qa_b do).

## SOUND (my numbers, and the draft's reruns)
- The act at a lone clock with W | k is [[2 - k/W, -1], [1, 0]], det 1; whole elliptic at t = 1, 0, -1 (orders 6, 4,
  3), parabolic at +-2; the shadow form kept; the time plane's ring the mode's own (probe_time identical; qa_b).
- The hand's own SO(2) commutes with the act as built with the flip on the negated row: 12 of 12 (qa_a, the 4^3 board).
- The mirror as the swap with the flip and the exact run back: the classical T of a reversible second-order board.
- Hamilton's product as the T1 tables (dot, cross), the 24 as 48 units (12 Hurwitz, 12 of norm 2), parity as
  conjugation, Euler's identity: reruns identical; standard and right.
- The 24-gear train: 48 elements with the right orders; L and R signed permutations, commuting, -1 = -I; SUM tr^2 =
  1152, SUM tr(g^2) = -384; pi onto O_48 with kernel of rank 16, equal to the spin-3/2 part (qa_d).
- The step is a right quaternion multiplication iff t = 0 (qa_c); the draft's algebra (i)-(v) is right as algebra.
- The draft names its limits: the quarter mode alone, a standing clock, a uniform hand, nothing here a click.

## Solution24, one line
Step 7 needs a regime clause: before a board structure is called nature's, name where nature's hands sit (k/W and the
wavelength against the Mesh) and measure there; a structure found only at k/W in {1, 2, 3} or at |k| = pi is the
lattice's.
