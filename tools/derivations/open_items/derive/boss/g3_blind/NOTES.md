# G3 blind: working notes (the second hand's; David's texts unread)

## What the act is (src/tensor24/engine, main 9067de20d)
- readings flat = [value rows (R), grad x (R), grad y (R), grad z (R), force (R), unit]; the unit is row 5R = index -1.
- contract.pushes(factor, (a,b,c,d)): legs are GEAR rows or -1 (the unit); a leg's index is both the reading gathered
  and the row its push lands on, so the plan's legs are VALUE legs and the unit only (a gradient or force leg would
  land off its row). Each monomial f x_a x_b x_c x_d pushes leg a by -f x_b x_c x_d, etc.
- drive: q_d, r_d+ = carry(J, T_d, r_d); push = s (F + T_k q_d); gear: q, r+ = carry(W(a-b) + push, W, r);
  a+ = a + q; b+ = a.  So u = W(a-b) + r is the velocity in teeth: u+ = u + push; the count moves by floor(u/W).
- W = 6 den Gamma^2 + the square's 00 slot; grip = den Gamma^2; light c^2 = grip/W = 1/6 per round^2.
- load.tables: 43 of the 125 channels stand (the O-group Clebsch-Gordan rows, primitive, whole):
  K x K -> A1 for every K (A1: 1; A2: 1; E: 2,-1,-1,2 = twice the Eisenstein norm; T1, T2: the dot product).
  T1 x T1 -> E (2,-1,-1 | 1,1,-2), -> T1 (cross, antisymmetric), -> T2 (symmetric off-diagonal); T1 x T2 -> A2, E, T1, T2;
  E x E -> A1, A2 (antisymmetric), E; A2 x E -> E; A2 x T1 -> T2; etc.
- On main the plan is empty (load.load: "until the coupling family's one plan reads the 24's tables c (G3)");
  s = T_k = T_d = 1 (the force's path).

## Law lines that bear on term 6 (docs/ALGEBRA.md, main 9067de20d)
- 35: Postulate 5 (no if, no floor, no bound); Postulate 6 (linear in c; "no coupling of the time gear with itself and
  no file setting a strength for one"); "The time gear's spring is the clock's one notch": D/W = 2/Gamma, -D a on A1,
  "the term that gives every massive train its mass", derived from den and Gamma, set by no file; decision 35 (no
  particle, mass or coupling declared in any file); decision 37 (masses measured only in clicks; a train's spring is
  never an input); decision 38 (the Node-clock is one generic node; the seed need not be generic); decision 40 (d) one
  drive serves every row, built at G3 with the coupling family; (g) "the coupling family's steady count is one
  quantum per Node-clock, from the law and not from a file"; (h) the odd tooth generic: if the 24 break, by the state,
  "a steady odd count ... whose kind is to derive"; the toy "bounded at lambda = 1/Gamma, lambda the coupling family's
  strength"; decision 41 no root, no table; the principle (1)-(12).
- 84 one act on every train alike; 88 the Node-clock is one act (kinds, tables; "the contraction of two kinds is fixed
  by the group's product table"); 90 the table of the kinds; 92 locality, the Node-clock independent (its rules the
  24's tables derived once from its star); 94 the 24 hold; 96 generic, no if, no number but the files'; 100 no float,
  no number in the code, the teeth counts algebra; 102 no circularity, no root and no table, no books; 104 unify;
  106 clocks always checked, tests one per generic part, everything from the big things, only generic laws, a
  floor or bound is an if, every bound a carry, time a circle.
- 330: the teeth count is one, w = 6 den Gamma^2 for every train; decision 40 (d) under it.
- 1913: the held field of the old engine: "one gear a held field, two a hand, four twin hands": the numbers alone tell
  a held count from a hand (the precedent for the coupling family's character).
- 1556: confinement is the click's (the mass section's citation).

## The idea being probed
- f = W/Gamma = 6 den Gamma: the clock's one notch as the unit of every spring; the time gear's D = 2 f (line 35).
- The held count N: the one-gear A1 train; its own potential the hairspring toward the unit, lambda f (n - 1)^2
  (monomials n n 1 1 at +lambda f, n 1 1 1 at -2 lambda f): the steady count is the unit, one quantum, from the law.
  Alternative to probe: the hat lambda f (nu - 1)^2 over the A1 rows (Goldstone light), fragile in whole numbers?
- The spring: for every hand X (every train but the square and N), through K x K -> A1 of each of its kinds, with
  the held count: monomials (g f C_yz; x_y, x_z, n, 1): J_x = -2 g f n (C x), J_n = -g f x^T C x.
  Beat: 4 sin^2(omega0/2) = 2 g C n / Gamma. At g = n = 1: the notch's beat, period ~ 2 pi sqrt(Gamma/2) rounds.
- Windows to measure: 0 <= 2 g C n / Gamma < 4 (the step); the own potential 2 lambda/Gamma < 4; the back-reaction
  g A^2 < 4 lambda (n_eq = 1 - g <x.x>/(2 lambda) stays above 0); the 24; the run back.

## Words from above (the coordinator, relayed; to test, not to take as truth)
- Big Pic (#2187 6526181441, 6526201692 piece 3): the coupling family is the ANCHOR of every matter clock's escapement.
  A half-speed (spinor) clock has two hands, left and right; without the anchor they run apart at light's speed, no
  beat, no mass. The held hand stands at every Node-clock, one quantum each (decision 40 (g)), and rocks the matter
  clock from its left hand to its right and back; the rocking's rate is the beat, the mass. It carries no turn of
  light's, so light passes it unmeshed.
- The held hand is no standing count: a hand that beats with D = now^2 - next x before = one winding at every
  Node-clock; with two parts turning round, re^2 + im^2 stands still while it beats, read at the now slot alone.
- The ties: whole-speed hands tie through the held hand's square re^2 + im^2 (never negative: no mirror well, no
  pumping, no bound on the strength, no walls; its rests are a ring); half-speed hands tie linearly (the linear tie
  rocks their two hands; its sign is only which hand goes first); the mirror well came from tying whole-speed hands
  linearly (g k x^2); which families tie to k: those whose two hands differ in a turn the held hand carries; light's
  turn is not among them. The half-speed gear is another agent's piece: name the linear tie, build the whole-speed
  part on the act now.
- The owner (15:3x UTC): yes to the completion of line 35 (4)'s carry: the click counts where the two runs part (D
  given or taken), never D held; so the held hand beating steadily at one quantum is lawful and never clicks.

## What this fixes in whole numbers (to probe)
- "re^2 + im^2 stands still while it beats", exactly, for a two-part hand in quadrature: the carry's recurrence
  a+ = c a - b with c whole keeps re^2 + im^2 exactly only at c = 0: the quarter turn, (re, im) -> (-im, re), the
  Gaussian unit i per round. On the act: push = -2 W a, i.e. the held hand's own spring is twice its teeth (the
  monomial W re re 1 1 pushes re by -2 W re): a+ = 2a - b - 2a = -b. D = now^2 - next x before = re^2 + im_... = 1
  at (1, 0): one winding, exactly, forever; |k|^2 = 1: one quantum per Node-clock.
- The whole-speed tie: g f (x.x)(re^2 + im^2), the tables' K x K -> A1 row for x.x and A1 x A1 -> A1 for each part of
  k; J_x = -2 g f |k|^2 (C x): a constant spring while the turn holds; J_k = -2 g f (x.x) k: a push that only
  hastens k's turn, absorbed in k's fine teeth while 2 g f x.x < W/2, i.e. g x.x < Gamma/4 (to measure).
- Beat of a tied hand: 4 sin^2(omega/2) = 2 g |k|^2 f / W = 2 g / Gamma at f = W/Gamma (the notch) and |k|^2 = 1.
- The act's floor makes a small-amplitude swing a relaxation oscillation (stand, fall at 1 count/round, stand): the
  harmonic beat needs omega A >~ 1, i.e. A >~ sqrt(Gamma/2 g): the quantum's amplitude 1/sin omega. Measure P(A).

## Measured laws (p1-p7, all on engine/step.tick; see G3_MEASURES.md)
- The quarter turn is exact at the factor W alone; |k|^2 and D held; the 00 slot bends it only past +-rest/2.
- A tied hand below the quantum's amplitude swings as a relaxation: P = Gamma/(g |k|^2 A) + 4 A rounds, to a round,
  in A (1..15), g (1..15), |k|^2 (1, 2, 4, 9) and Gamma (200..12,800, the root scaling). Its minimum is 4 (Gamma/g|k|^2)^(1/2)
  at A^2 = Gamma/(4 g |k|^2); at the quantum's amplitude A_q^2 = Gamma/(2 g |k|^2) it is 3 (2 Gamma/g|k|^2)^(1/2), 3/pi of
  the harmonic period.
- The room: one round's push on the largest part, 2 g f (x.x) max|k_rho| < W/2, i.e. g (x.x) max|k_rho| < Gamma/4,
  halved for (1,1) whose parts keep their sign two rounds running; a slow walk of the tooth near the edge (p2 B).
  Past the room the turn bends (|k|^2 among 0, 1, 2, ...) and stays bounded to about g x.x = 0.6 Gamma at |k|^2 = 1;
  runaways from 0.78 Gamma, and at once for a hand moving 2 counts a round; the boundary is fuzzy ((1,1): away at
  256, bounded at 400 within 3,000 rounds). A held hand at (q, 0) holds about q quanta of tied matter per Node-clock.
- The step's own window is [0, 4] exactly (p3); g < 0 runs away.
- Linear ties (g k_re x.x; Re(conj(L) k R) on whole-speed hands): no beat, the held hand pushed off, runaways at A 10.
- Light untied leaves |k|^2 at 1 at any energy (p7).
- Board: generic waves of amplitude ~10 bend the turn (|k|^2 to 17) but stay bounded 300 rounds; moving matter
  within 3 runs away in 36 rounds (p4); with another seed |k|^2 stays 1 (p4b).
