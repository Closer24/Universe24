# RECHECK: the two hostile reports on ONE_ALGEBRA, item by item, re-derived and re-measured

The deriver of the one algebra, 2026-10-30, after qa_math/REPORT.md (one BLOCKING, six minor) and qa_phys/REPORT.md
(four BLOCKING, four minor) came back NOT PASSED. By the owner's rule every refusal goes to Big Pic first; this file
holds my own re-check meanwhile, on paper and in whole numbers, in new files only (ONE_ALGEBRA.md and the probes are
not edited; the root dial's readers read a frozen copy). New probes: probe_recheck_q.py, probe_recheck_train.py,
probe_recheck_doubler.py (outputs beside them). The second text waits for Big Pic's word.

## The law of findings, applied: what each reader found, broken down

### qa_math item 1 (BLOCKING): the wall holds only for a carry with ONE remainder set (one dial for every quotient)

What I claimed: a carry on the half-speed hand that turns with the lifts exists iff gcd(W, 6) = 1; "r in a set D of
coset representatives ... that is what makes the act bijective and the run back a mirror".

What the reader found: the hypothesis "D one fundamental domain for every quotient" is sufficient and NOT necessary
for the bijection and the mirror. A carry u -> (Q(u), u - W Q(u)) with Q ANY function of the dividend, odd
(Q(-u) = -Q(u)), makes the state map (a, b, r) -> (a + Q(u), a, u - W Q(u)) a bijection on the valid states (the tooth
its own velocity's remainder: Q(W v + r) = v) and the mirror (b, a, -r) its inverse through the tick. His
construction: g u the least of the 24 images of u (a unit g != 1 fixes no nonzero point, so g is unique up to the
order's ties, none in practice), m the centred box quotient of g u at W, Q(u) = conj(g) m. Equivariant by construction
(the orbit of h u is the orbit of u), odd (since -1 is a unit), remainder below the divisor's norm, cells of varying
size (no fundamental domain), and the project's own edge draft (edge_lib.split: cells of 2D - 1 and 2D + 1 by the
parity of q) is a carry of this kind in rank 1.

Re-derived on paper. (a) Injectivity on valid states: if W v + r = W v' + r' with both valid, then v = Q(W v + r) =
Q(W v' + r') = v' and r = r'. The image is valid (the new tooth is the remainder of the quotient the new velocity is).
The mirror keeps validity iff Q is odd. untick = mirror o tick o mirror: for the state (a + q, a, r') with u = W q + r':
mirror gives (a, a + q, -r'); the tick's dividend there is W (a - a - q) + push(a) - r' = -W q + push(a) - r' =
-(u - push(a)) = -(W (a - b) + r), whose quotient by oddness is -(a - b) and whose remainder is -r; the state becomes
(b, a + q - ... ) = (b, a, -r); the mirror returns (a, b, r). Nothing needs a fundamental domain: only Q a function,
Q odd, and the push a function of the now slot. My sentence "that is what makes the act bijective" is FALSE as a
necessity. (b) Where my theorem's step (iii) used the fundamental domain: "a coset fixed by g must have ITS
representative fixed by g". With a quotient-dependent remainder a coset has several remainders (one per quotient
cell), and g may send one to another: the obstruction dissolves. The theorem stands for fixed dials exactly as
proved (H^1 = 0, the fixed cosets, the indices), and so does fam_math's Theorem A, which shares the hypothesis
("D = rho(Lambda) a set of representatives": rho a function of the coset).

Re-measured (probe_recheck_q.txt, my own code for his rule): at W = 5, 6, 9: Q(g u) = g Q(u) 0 misses of 1440 each;
Q(-u) = -Q(u) 0 of 60; the largest 4 N(remainder) 80, 168, 252 against 4 N(W) = 100, 144, 324 (below the divisor's
norm at 5 and 9; at 6 above it once, 168 against 144: his bound "below the divisor's norm" held on his draws, mine
found a remainder above it at W = 6 - immaterial to the bijection, which needs no bound); the cell of the quotient 0
holds 97, 145, 1057 dividends of [-W, W]^4 against W^4 = 625, 1296, 6561 (no fundamental domain); on the act (a lone
Node-clock, the spring J = -2 psi, the engine's pushes) the turned run equals the run turned for 240 of 240 lifts x
starts at each of W = 5, 6, 9 and the run back by (b, a, -r) returns the lay 10 of 10. At W = 6 and 9 my theorem says
no ONE dial turns; his carry turns at both.

VERDICT: STANDS, BLOCKING, accepted in full. What falls in my text: "iff" (right only for fixed dials); "that is what
makes the act bijective"; "at such W the hand's teeth cannot be kept in any dial that turns" (right for ONE dial, wrong
for a dial per quotient); "no domain exists" read as "no carry"; the Clicks' trilemma (a fourth way exists: the edge's
kind); the Answer's "none exists at any teeth count divisible by 2 or 3, search or no search" (wrong: his rule is a
search of 24 images and exists at every W). What stands: the fixed-dial theorem with its hypothesis stated; no per-gear
carry in any basis (fam_math); the open condition (c), now at EVERY W: a rule free of a table and of a comparison
(his rule compares 24 images; the orbit domain is a table). A further candidate I thought of and reject: the
group-averaged box quotient Q(u) = SUM_g conj(g) [g u / (24 W)]_centred is whole, equivariant and compare-free up to
the tie rule, but its quotient errs by up to 24 counts a round (the sum of 24 roundings): a carry 24 times coarser
than the per-gear one, no solution.

### qa_math item 2 (MINOR, a false reason): "the group ring has fixed vectors (the orbit sums)"

Re-derived: on the sign-twisted train L(-1) = -I, so SUM_g L(g) = SUM_g L(-g) = -SUM_g L(g) = 0: every orbit sum is 0
and no vector but 0 is fixed by all of G. Re-measured (probe_recheck_train.txt): SUM L(g) is the zero matrix;
|det(L(g) - I)| = 16777216, 0, 4096, 256, 64 for the orders 2, 3, 4, 6, 8: g - 1 is no unit on the train, so my H^1
argument does not run there at all. The true reason the train rides the per-gear carry: every L(g) and R(g) is a
signed permutation, and the box with the flip is each signed permutation's invariant domain (the carry's lemma). My
reason confused the untwisted group ring (where 1 + g + g^2 is fixed by an order-3 g) with the twisted one.
VERDICT: STANDS; my parenthesis was false; the fix is his sentence.

### qa_math item 3 (MINOR, scope): "the unit step is the lone clock's or the uniform hand's"

Re-derived: the step is q -> q j wherever the round's push is -2 W now; for an eigen-hand of the pull with F =
-lambda grip now, the spring k and the pull add: k + s lambda grip = 2 W (s = 1). The lone clock and the uniform hand
are lambda = 0; the staggered hand on an even board is lambda = 12 with NO spring when W = 6 grip (the load's rest!):
F = grip (SUM_nb (-a) - 6 a) = -12 grip a = -2 W a. Re-measured (probe_recheck_doubler.txt, the example's own piece
4 x 4 x 4, light with no spring, the square at 0): the staggered hand (-1)^(x+y+z) gives q+ = q j at every site every
round for 12 rounds, the teeth still, the hand back after 4 rounds, F / a = -12 grip exactly; the long wave
(1, 0, -1, 0) along x gives F / a = -2 grip, q j false, the teeth move. VERDICT: STANDS; the scope sentence must be
his ("wherever the push is -2 W now").

### qa_math item 4 (MINOR, weight): the slot quaternion is a reading; only the step and N(q) are the quarter mode's

Re-derived: the phase i q, the swap (i q i^-1) j and the sum/difference q (1 - j) are identities of the READING, true
at every mode and on any state; what depends on the mode is the step being R_j and N(q) being the kept form; and at
every exact mode the carry is inert (the dividend -W (now + before) + r is a multiple of W plus the tooth, the
quotient exact, the tooth still), so the quaternion reading touches none of the act's one non-trivial operation. His
strengthening (t = +-1: the step is a unit quaternion's right multiplication in NO whole basis of the two slots, the
invariant Hermitian form's Gram determinant 3 c^2 / 4 never 1) I accept on his measurement and on paper: the
S_t-invariant form v^2 - t v u + u^2 has discriminant t^2 - 4 = -3 at t = +-1, so its Gram determinant is 3/4 of c^2
for any scaling c, and a right quaternion multiplication needs a form of determinant 1 (the norm). The sign: the j
slot of q (1 - j) is before - now, the velocity NEGATED (the body says so, the Answer did not). VERDICT: STANDS.

### qa_math items 5-7 (MINOR): hygiene, numbers, wording

5. probe_double.py broke when edge/edge_lib.turned_edge gained the argument `wd` four minutes after my run; with the
   one argument added the output is byte-identical (his rerun). A fixed copy is written as a new file,
   probe_double_fixed.py (passing layout.gearing.drive), its output probe_double_fixed.txt, and the edge_lib revision
   it reads named there. STANDS.
6. "determinant -48" and "-128" are not invariant numbers: the invariant content is the rank 5 of Hamilton's five
   forms, the Smith diagonal [1,1,1,1,1,1,2,2,2,6] of the ten (so E and T2 outside), and [1,1,1,1,2,2,2,2,2,4] for the
   sandwich basis (denominators dividing 4). STANDS; the second text states ranks and Smith forms.
7. "(a) a bijective division with remainder": the map (n, r) -> (q, r') is |D| to 1; the bijection is the state
   map. "A determinant W'/W" names the scale of a non-linear map. The theorem's (i) assumes the tooth turns by a map
   of the tooth alone and the quotient linearly. STANDS; wording.

### qa_phys item 1 (BLOCKING): the slot quaternion lives at the lattice's cutoff, not in nature's time

What I claimed: "the double Node-clock IS Hamilton's quaternion of the slots ... at the quarter mode exactly",
measured with a spring k = 2 W on the example's light.

What the reader found: the whole turns exist at k / W = 1, 2, 3 alone (121 springs scanned), the Hamilton unit at
k = 2 W alone; at the load's W that spring is 9 x 10^22 per row, 4 sin^2(omega / 2) = 2, a beat of 90 degrees a round,
the heaviest beats below the band's edge; the example's light has no spring. On the example's own piece the staggered
mode (pi, pi, pi) IS the Hamilton unit with no spring (F = -12 grip a = -2 W a), period 4, the teeth still: the top of
light's band (omega^2 = 2, zero group velocity: nothing travels there); of the 64 Fourier modes 21 are whole turns, 1
the Hamilton unit, 42 move their teeth; every whole one has |k_a| >= pi / 2 on some axis. Nature's hands (long waves,
k / W ~ 0) are never whole.

Re-derived: the exact linear round needs W | k (my own finding 5), and with the pull on an eigen-hand the condition
is k + lambda grip = 2 W with lambda in {0, ..., 12} the lattice Laplacian's eigenvalue (2 SUM (1 - cos k_a)): at
W = 6 grip the Hamilton unit needs k + lambda grip = 12 grip, so with no spring lambda = 12, the staggered mode, the
band's top; a long wave has lambda ~ |k|^2 small and W does not divide k + lambda grip. Re-measured
(probe_recheck_doubler.txt): the staggered hand: q+ = q j at 64 of 64 sites for 12 rounds, teeth still, period 4;
the long wave along x: not a unit, teeth moving. VERDICT: STANDS, BLOCKING, accepted. My "IS" over-claimed; my own
finding 5 ("where W does not divide k the tooth moves and the step is no unit") already said where nature's hands
sit, and the Answer did not carry it. The right statement: the slot quaternion's unit step is the doubler mode (the
law's line 33 puts light's c^2 = 1/6 at the doubler's hold; the quarter mode is that band's top) or a spring of the
cutoff's size; nature's hands have no unit.

### qa_phys item 2 (BLOCKING): the phase and the step generate a commutative algebra, C (+) C

Re-derived on paper: L_i (the phase, left multiplication by i) and R_j (the step, right multiplication by j) commute;
(L_i R_j)^2 = L_i^2 R_j^2 = (-I)(-I) = +I, so e = (I + L_i R_j) / 2 is an idempotent: the algebra generated by L_i and
R_j is C (x) C = C (+) C, commutative, with zero divisors; Hamilton's i j = -j i is between the LEFT i and the LEFT j
(or the right ones), which the act never multiplies together. The identification C^2 = H (q = z_1 + z_2 j) is a
bookkeeping of the two slots as a complex 2-vector; the act's step at a whole mode is an element of SL_2(Z)
commuting with the phase, the quaternion norm equals the kept form v^2 - t v u + u^2 only at t = 0. VERDICT: STANDS,
BLOCKING, accepted: "the double Node-clock IS Hamilton's quaternion" must become "the two slots are a complex
2-vector; at t = 0 the step is also R_j, the quaternion a bookkeeping of that case"; the three rings are the
crystallographic restriction (my own words in finding 5), of no selection content.

### qa_phys item 3 (BLOCKING): the slot's j is not Kramers' j

Re-derived: the mirror S = (i q i^-1) j is the slot swap: S^2 = I and S L_i = L_i S (the swap acts on the slot index,
the phase on the part index): the mirror is LINEAR and COMMUTES with the phase: the classical T of a reversible
second-order board (and the owner's line 154: Rule3 is a wave with no arrow). Kramers' T on a spinor ANTIcommutes
with the phase and squares to -1 (on the families' side: the 48 on the left, the phase R_i on the right, the partner
R_j with R_j R_i = -R_i R_j and R_j^2 = -I; FAMILIES.md's T phi = phi j, fam_math's "T phi = phi j, right
multiplication by j"). Two operations on one symbol j: the slot's step (a quarter period of evolution, commuting with
the phase) and the spinor's reversal (anticommuting). So "the spinors are the same thing" is NOT shown by the slot
quaternion; my own text concluded "two algebras, not one" but the Answer's "IS Hamilton's quaternion" and the owner's
frame invited the identification. VERDICT: STANDS, BLOCKING, accepted; the left i is a charge rotation (the hand's
SO(2), the winding), the mirror the classical T.

### qa_phys item 4 (BLOCKING): the 24-gear train carries the electron's 8 numbers with 40 of doublers

Re-derived: the train's real content per slot is E1/2 (4 real) + E5/2 (4) + two real G3/2 (8 + 8) = 24; with two
slots 48 per Node-clock; Dirac's electron is 8 real (a Pauli 2-spinor in second order); the Galois twin E5/2 and the
two spin-3/2 quartets are 40 numbers nature does not have; under any invariant spring all three kinds beat alike
(degenerate); pi's kernel (rank 16) IS the spin-3/2 part (so the quaternion reading is blind to 2/3 of a click's size
by his count, 675 permille); 1/2 x 3/2 contains 1, so a vector coupling converts the electron into its doublers; a
whole invariant spring splitting them exists (his M = a I + b D + c (6 P_G)) but nothing derives a, b, c (a
declaration by the law's word). I did not measure the splitting; the counts (4 + 4 + 8 + 8 = 24; the kernel 16) are
mine too (probe_double: pi of rank 8, kernel 16). VERDICT: STANDS, BLOCKING, accepted as the carrier's price: "passed
at the price of 40 doublers per Node-clock, degenerate, invisible to the quaternion reading"; the carrier is
fam_math's and the families', the price is to be said where I cite it.

### qa_phys items 5-8 (MINOR)

5. The one algebra of space and time would be Cl(3,1) = M_4(R): two commuting quaternion algebras acting on ONE
   quaternion from both sides (gamma^0 = L_i, gamma^a = L_j R_a, anticommuting with signature (-,+,+,+)); my two
   algebras act on different indices (the slots x the parts; the T1 rows by Ad(g), with Ad(i), Ad(j), Ad(k)
   commuting, the Klein group) and nothing anticommutes: no Clifford structure, no boost, time and space factorize
   (Galilean); the slot pair is Klein-Gordon's (phi, pi) (Feshbach-Villars), not spin. I had this thought and dropped
   it as speculative; he is right that it belongs in the text as what is absent and why. STANDS.
6. The five readings at k = 2 W are one map (z_1, z_2) -> (-z_2, z_1) read five ways; the "product books kept" is no
   new conservation. STANDS.
7. "Exact at the quarter mode" is drawn on the fine teeth: with the spring off by 1 the hand still follows q j while
   the tooth moves (his 12 of 12); what a click sees of the teeth is click25's. STANDS.
8. probe_double.py's breakage: as qa_math 5. STANDS.

## What stands of ONE_ALGEBRA after the re-check (to carry into the second text)

- Finding 2 (the whole-speed act on whole quaternions, bit for bit; the tables as Hamilton's product), finding 3
  (the 24 as 48 units, 12 Hurwitz and 12 of norm 2, whole at whole speed; parity as conjugation), finding 5's pieces
  (the time plane's rings and the parabolic edges; the metric's E and T2 outside Hamilton's words, as ranks and Smith
  forms; O_48 Euclidean with the double farthest point; Rule3's box against Hurwitz's division; the generations):
  both readers list them SOUND.
- Finding 1 restated: the fixed-dial theorem with its hypothesis ("one remainder set for every quotient: the cells
  translates of one tile") - iff gcd(W, 6) = 1, no twist, the orbit domain; and beside it the quotient-dependent
  carries (the edge's kind): bijective on valid states, mirrored by (b, a, -r), equivariant at every W with a
  comparison (the least image); the open item (c) at every W: a rule free of a table and a comparison.
- The double Node-clock restated: the two slots a complex 2-vector; the step at a whole mode an SL_2(Z) unit
  commuting with the phase; at t = 0 also R_j (the band's top, the doubler mode on the example's piece with no
  spring); the quaternion a bookkeeping of that case; the mirror the classical T, commuting with the phase, not
  Kramers'; the slot j and the spinor j two operations: "the spinors are the same thing" is not shown; the one
  algebra of space and time would be Cl(3,1), absent on the board (no anticommutation, no boost).
- The units as gears restated: the true reason (signed permutations, the carry's lemma), the price (40 doublers per
  Node-clock, degenerate, the spin-3/2 part pi's kernel).
- The root dial section: with its own readers; untouched here.

## Solution24, re-read against the reports

- Step 3: my theorem opened without its hypothesis; a derivation must list what it assumes and read it against the
  project's other drafts (the edge's split was in the folder next door and breaks the hypothesis). Accepted.
- Step 7: a regime clause: say where nature's hands sit (k / W, the wavelength against the Mesh) before calling a
  board structure nature's; a structure found only at k / W in {1, 2, 3} or |k| = pi is the lattice's. Accepted.
- Step 8: the probes measured what I had derived and did not try the construction that breaks the hypothesis
  (a quotient-dependent remainder) nor the modes where nature's hands sit (long waves); both are now in the recheck
  probes.
- Step 9: this is what the hostile pair is for; both reports are right where they are blocking.
