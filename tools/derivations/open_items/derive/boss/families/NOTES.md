# families: working notes (saved as I go; the derivation goes to FAMILIES.md)

## Read
- t24b (main 9067de20d): engine/kinds.py, runner/load.py (trains_of, tables, the square flag), runner/files.py
  (held_departures: E only inside the square), engine/step.py, contract.py, mesh.py, state.py, algebra/carry.py, main.py.
- docs/ARCHITECTURE.md whole (Solution24, the thirteen terms, the families and the three hands, term 12's "a full slot
  refuses after the draw, and the quantum returns to its giver").
- docs/ALGEBRA.md by search: Pauli (L346, 458, 559, 1558, 1562, 1907), exclusion, spin, Gaussian, antisym, exchange,
  statistic, double cover, chiral, handed, parity; lines 35, 94, 100, 102, 1556, 1696.
- scratchpad: sym24_v2/SYM24.md (the 48 hold at standing W; no kind carries a parity label; the epsilon table the one
  door), term11_v2/TERM11.md (tau the cross of the two parts with the kick through the A1 table; the count climbs 0..7),
  click25/NOTES.md (notes only; no CLICK25.md stands).
- tools/derivations/open_items: DAVID-TENSOR24-PAULI.md (2026-10-28: "a family pairs as its kind pairs", the sign the
  Frobenius-Schur indicator, +1 on the 24's five kinds, -1 on the 48's three spinor kinds; Pauli at the click by the
  draw against the occupant's phase reversal; on the old engine's twins), SOFER-PAULI-PHASE-REVERSAL-1.md (Kramers,
  T T = -1 on the twins), DAVID-PAULI-DYNAMICS.md (the field gathers 11.8 quanta at one clock: no exclusion in Rule3's
  step), ANIMATE-PROBES-3/ladder_pauli.py (Sym^2 / Alt^2 by the FS sign).

## The owner's words that bind
- 2026-10-27 (L1562): matter antisymmetric, non-matter (light) symmetric, "they can be in the same state in the clicks";
  "matter is symmetric and force carriers are not ... on the board it is something else, with the phase, and in the
  clicks something else"; "is a hand in this actually a complex number?".
- 2026-10-28 (David's page): "Pauli never as a postulate ... derived from the phase reversal of a family on the board".
- today: "a rule on the families, something algebraic, or a symmetry ... maybe only one family is not symmetric";
  and through the coordinator: "In the clicks, think clocks, do not think quantum: clocks, hands, chains ... clocks
  connect and come apart, and the aim of the system is that clocks connect; that is what clicks show."

## The line of the derivation (to check in probes)
1. Algebra: the exchange sign of a family is the swap sign of its kinds' own pairing into A1, the engine's table
   C[K x K -> A1]; equal to the Frobenius-Schur indicator SUM_g chi(g^2) / 24; +1 on all five kinds and on the square.
   Antisymmetric channels of the 24: T1 x T1 -> T1 (epsilon), T2 x T2 -> T1, E x E -> A2; none into A1.
2. Part: the 24 act on the kind alone; part 2 adds the plane's two forms, dot (sym) and wedge (antisym); the wedge is the
   click's own pairing (tau, the area moved: what one gives the other takes, TERM11), not an exchange sign.
3. Double cover: the spinor kinds have FS -1 (Kramers); none has a whole basis under the 24 (the quarter turn's trace
   +-sqrt 2); Q8 on four gears is the whole lift of the three half-turns alone (law L346). Check in Z[sqrt 2] pairs.
4. Board: one amplitude per train per Node-clock; v (x) v is symmetric; two clocks of one family in one mode are one
   clock of a bigger swing (the act is linear). Mirror: T T = +1 on every family (the swap of now and before twice).
5. Clicks: measure on the act that every kind's taker crowds (count >= 2 in one mode), the "no" mutant a declared
   refusal (a fake, to show the measure sees exclusion) and, if time allows, the blockade by an own four-leg term.
6. Handed: no kind carries a parity label (SYM24); A2 the one odd character (12/12); the epsilon table the one door.

## Widened (the coordinator, three words mid-task)
- The owner: "In the clicks, think clocks, do not think quantum: clocks, hands, chains ... clocks connect and come apart."
- Big Pic (6525978806 item 3): line 90 makes every family a tensor of the five kinds (bosons); the candidate rule is the
  48's kinds: five single-valued (bosons) and three double-valued (E1/2, E5/2, G3/2: fermions, Pauli theirs); the handed
  family a spinor whose click reads one helicity (re x im) . p; the first question: can a spinor stand in whole numbers.
- The owner (6526201692): line 90's five kinds may be widened to the double cover where needed. Big Pic's correction
  (6526070842 item 5): in Z[zeta_8], sqrt 2 = zeta - zeta^3 is whole and every ideal is principal; four whole numbers per
  part. Piece 1: the half-speed gear on the act (the three kinds whole; the 48 bit for bit; the run back; a full turn
  -1, two +1). Piece 2: Pauli in the clicks in clocks (the swap one full turn, Dirac's belt; the pair's joint hand with
  the swap's sign; bunching; the half-speed pair in one state never clicked; opposite senses; no room for a third).

## Results so far
- probe_kinds: all five kinds FS +1; the A1 pairing symmetric for every kind; antisymmetric channels E x E -> A2,
  T1 x T1 -> T1, T2 x T2 -> T1; the loader's square flag is Sym^2 of the four-vector; A2 the one odd character (12/12);
  a Gaussian hand under its own turn keeps two pairings, the dot (+) and the wedge (-, the click's area).
- probe_48: the 48 closed in Z[sqrt 2] from two of the engine's turns, covering the 24 two to one; the quarter turns'
  lifts have trace +-sqrt 2 (no whole matrix on 2n gears); the spinor FS -1; the Hurwitz lift whole in a mixing basis
  (no signed permutation has (trace, order) = (2, 6) or (-2, 3) on four gears); the signed-permutation double cover of
  the even 12 is a complex kind (FS 0); on the act the Hurwitz lift departs on 22 of 22 mixing matrices at W = 9, 0 at
  W = 1; the signed-permutation lift holds 24 of 24.
- probe_act: every kind's taker crowds (count 0 to 7, identical rows for A1, A2, T1, T2); two keys laid land in one
  hand; mirror twice = identity; the declared refusal holds the count at 1 (a fake outside the act); the blockade by a
  four-leg own term caps the count 7, 5, 3, 2, 1, 0 as lambda rises, kind-blind.

## Closed (the derivation in FAMILIES.md; the five probes and their outputs beside it)
- probe_spinor: Lambda = Z[sqrt 2] 2O rank 8; the 48 whole unimodular 8 x 8, a representation, -1 = -I; the quarter
  lift^4 = -I, ^8 = I; SUM trace(M M) = -192; (4, 6) and (-4, 3) in no cycle type of eight gears; Lambda = Z[zeta_8] +
  w Z[zeta_8] (four whole numbers per part); the Gaussian basis (1, j) Z[zeta_8]: the x axis's 16 lifts signed
  permutations; G3/2 on 16 gears; on the act W = 1 all hold, W = 9 the 46 mixing depart, +-I and the Gaussian 16 hold,
  the run back exact, four quarter turns -I.
- probe_pair: the belt picks e = +1 for the five kinds and -1 for the eight-gear kind; the spinor's two pairings from
  conj(x) y = <x, y> + j det(x, y); det(phi, phi) = 0; the partner T (Kramers, opposite sense, det = N); no room for a
  third; on the act: whole-speed copies bunch (J_+), half-speed copies alike with J_- = 0 while their windings climb
  (the books break); the partner pair keeps its hand 600 of 600 with the flipped teeth.
- probe_kinds 7: the winding even under all 48, the helicity (re x im) . p odd under the 24 reflections.

## The square (Big Pic 6527540022 item 5.2; the coordinator after the first report)
Paper first (step 1, does it follow): v(psi) = (psi1^2 - psi2^2, i (psi1^2 + psi2^2), -2 psi1 psi2) is Cartan's square:
v . v = 0 (re . im = 0, |re| = |im|), |re|^2 = |psi|^4, re x im = |psi|^2 s(psi) with s = (2 Re conj(psi1) psi2,
2 Im conj(psi1) psi2, |psi1|^2 - |psi2|^2); Sym^2 E1/2 = T1, so the 48 turn v by the 24's T1 signed permutations;
v(-psi) = v(psi); v(psi) . v(chi) = -2 det(psi, chi)^2; v(T psi) = (-re, im) (the partner: the spin reversed).
The act is linear and the same real operator on all six gears, so V(t) = SUM_y L(t) V(y, 0) + L'(t) V'(y, 0) and
V . V stays 0 at every site for all t iff every pair of the lay's complex vectors (now and before, every site) is
null-orthogonal: all roots parallel (one spin direction) with any complex amplitudes. Two roots in one lay break
the square where they meet: (v + v') . (v + v') = -4 det^2. A square taker fed by a parallel root stays a square and
grows (one root, bigger); fed by another root it leaves the squares (a pair, det not 0). The sign of psi is lost by
the square; det^2 is kept, det's sign is not; a full turn is +1 on the square (T1). A null hand is also circular
light's: the gears cannot tell a square-carried root from a circularly polarized whole-speed hand; the kind must.
Questions on the act: 1 nullness kept, for which lays (one root; mutants: two roots, a line, linear polarization,
a giver of the same root against one of another); 2 the pair reading v . v' at one Node-clock (two copies alike: 0
for ever while the size climbs; the partner pair: -2 |re|^2); 3 the helicity H = SUM (re x im) . (re D im - im D re)
on a line of Meshes, its sign under the x reflection with the g lift, the 48 holding (J = 0).

## After the hostile mathematician (fam_math/REPORT.md, NOT PASSED): the second text FAMILIES2.md
- probe_induced: G3/2 by cosets of C6 with the sign: 48 signed permutations of 8 gears, -1 = -I, FS -96, 1 + 3
  pairings, the commutant of rank 4 with T T = -I a signed permutation; the 24-gear train (pairs +-g with the sign)
  2 E1/2 + 2 E5/2 + 4 G3/2, FS -384; tables C[K x K -> T1] by the group sum, equivariant 48/48; on the act with J
  through them: true 48/48, random 0/48, mutant 4/48 (G3/2) and 2/48 (24 gears) at W = 9, 10, 1.
- probe_pauli2: the kind's I-bilinear epsilon and Hermitian pairings; two quanta laid apart: free act, one state 10
  thousandths of a pair (rounding), partner 921; generic table 144 / 634, w_I 12000 -> 28664; I-averaged table
  44 / 825, w_I kept within 13003; the gears add as waves; the books of keys undefined for v . C(h, h); the
  pair-creation vertex (light at charge 2) named Open.
- The square lead stays on paper (above), unprobed, behind this on the coordinator's word.

## The third round (fam_math/REPORT2 N1-N5; fam_phys/REPORT 1-11; qa_phys 4; qa_math 1; the owner's words of 17:2x and 17:3x)
- probe_pauli3: the whole wedge D = |phi|^2|chi|^2 - <phi,chi>_I^2, 0 iff rank(phi, I phi, chi, I chi) = 2; the reader's chi:
  epsilon 0, D 622 thousandths, rank 4; of 292 chi with epsilon = 0 none has D = 0. G3/2 two lays (W 10^6, light 1000,
  30 rounds): free 21 / 974 / 644 (one state / partner / reader's chi); generic table 537 / 838 / 839; I-averaged 395 /
  771 / 701. Spin 1/2 inside the 24-gear train: the right 48 signed permutations, I = right i, T = right j, the whole
  projector rank 8; free act 0 / 999 / 443 with leak 0; the train's table 613 / 875 / 124 with the leak out of spin 1/2
  998 / 737 / 898 (the doublers mixed by light: qa_phys 4, fam_phys 2 confirmed).
- probe_quaternion: the eight kinds from the 48 units (A2 = sigma(g)/g on 48/48, T2 = sigma(g) v conj(g) 48/48, |T1| =
  1 + chi_E 48/48); per kind on the act with a kind-specific vertex: A1 48/16/16, A2 48/24/16, T1 48/0/16, T2 48/0/16,
  A1+E 48/8/16; the norm vertex a1 (k . k) is kept by every signed permutation (random 48/48): the anchor's tie tells no
  kind; the two tables one product (dot = -Re, eps = the vector part, 20/20); N(conj(b) a) = N(b) N(a) 20/20.
- probe_click (the owner's word: Pauli in the click, the board stacks): TERM11's world, G3/2 taker fed on its own line:
  term 11's count 0..7 (stacks), the pair's size S_- at every later key 0 thousandths, books taken 2 / returned 7; light
  (A1 part 2): count 0..7, S_+ 2000 at every key, all taken. No sine or cosine anywhere in the folder.
