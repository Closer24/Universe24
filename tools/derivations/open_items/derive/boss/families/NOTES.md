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
