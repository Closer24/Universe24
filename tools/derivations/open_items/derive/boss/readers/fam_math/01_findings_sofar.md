# Findings so far (16:20), to survive an interruption

## Confirmed (my own construction, p1_cover.txt, p2_induced.txt)
- The 48 closed from two lifts; cover the 24 two to one; -1 among them; spinor characters whole on 36, +-sqrt 2 on 12;
  SUM tr(q q) = -48; SUM tr^2 = 48. Orders: 1:1, 2:1, 3:8, 4:18, 6:8, 8:12.
- Lambda rank 8, the 48 as whole 8x8 of det 1, a representation (2304/2304), -1 = -I; (trace, order) table exactly as
  the text; SUM tr(MM) = -192; invariant forms 8 = 2 sym + 6 anti (null space and characters agree); 2 signed perms in
  the lattice basis; (-4,3) and (4,6) in no cycle type of 8 gears -> E1/2+E5/2 monomial in no basis of 8 gears.
- Hurwitz/2T: rank 4, 24 whole 4x4 det 1, FS -48, forms 1 + 3, (-2,3),(2,6) missing from 4-gear cycle types.
- The five kinds of the 24: FS +1 each; Alt^2 E = A2, Alt^2 T1 = Alt^2 T2 = T1.
- FS sign = full-turn sign on all 8 irreps of the 48 (a fact of 2O, not a theorem: D4 counterexample).
- All five of their probes rerun byte-identical.

## REFUTED (BLOCKING): "a half-speed kind is monomial in no basis beyond one axis" / "no half-speed family rides the act"
- Ind_{C6}^{2O}(lambda), lambda(w) = -1 (w the order-6 lift of a third turn): 8 gears, ALL 48 signed permutations,
  -1 = -I, faithful, = 2 G3/2 over C (G3/2's least whole form, the text's own Open item 3), FS sum -96 (Kramers -1),
  End of rank 4 (a quaternion order), 1 symmetric + 3 antisymmetric forms, quarter lift^4 = -I, 2 Kramers partners
  T (signed permutations in the commutant with TT = -I). By the carry's own lemma it rides the act at every W.
- The 24-gear form Ind_{+-1}(sgn) carries 2 E1/2 + 2 E5/2 + 4 G3/2, all signed permutations, -1 = -I: spin 1/2 DOES
  ride signed permutations (on 24 gears, never alone). Law line 346's "no train of gears turning by signed permutations
  carries spin 1/2" is false as written; true only as "not alone, not on fewer than 24".
- Complete list of transitive signed-permutation trains of the 48 with a half-speed constituent: 8 (C6; 2 G3/2; -I),
  16 (C3; 2 G3/2 + whole-speed; -1 a derangement), 24 ({+-1}; -I), 48 (trivial H; derangement).

## PROVED: the wall for Lambda and for Hurwitz
- Fixed-class theorem: for gcd(W, 6) > 1 no remainder map rho: Lambda -> Lambda with rho(x) = x mod W Lambda and
  rho(g x) = g rho(x) (all 48) exists; the obstruction: order-3 lifts fix nonzero classes when 3 | W (Smith diagonal of
  M-I is (1,1,1,1,3,3,3,3), det 81), -1 and the order-4, order-8 lifts when 2 | W; no g != 1 fixes a nonzero vector.
  Explicit at W = 9: x = 3(1 - g^-1) e_1 = [3,0,6,0,-6,0,9,0]. Affine relabelings (the flip trick) cannot help: an
  order-6 lift has det(1 - M) = 1, so every cocycle is (1-g)v with v in Lambda (H^1 = 0), a translate of the linear
  action. For gcd(W,6) = 1 the 48 act freely on nonzero classes (48 | W^8 - 1), so a G-stable domain exists set-wise.
- Same on Hurwitz/2T: Smith (1,1,3,3) order 3; (2,2,2,2) for -1; (1,1,2,2) order 4; det(1-w) = 1 order 6.

## MINOR so far
- "G3/2 ... sixteen gears (four copies of its least whole form of eight)": 16 = 2 x 8; it is four copies of G3/2 over C.
- "the nearest point of W Lambda": no one metric; the invariant positive forms are a 2-parameter family a N0 + b N1.
- The carry lemma's proof covers only rows with two +1 entries; the general proof (any whole P, any relabeling) in p4.
- The belt law S = R is the one declaration; "the sign is derived, not declared" overstates.
- "no room for a third" is dim 2 (also true of E, whole-speed); G3/2 (dim 4) admits 4.

## p3_act.txt (16:35): the 8-gear G3/2 form on the real act (SYM24's harness)
- J = 0, W = 9, 10 (even!), 1; 6 rounds; teeth drawn in [0, W): the 48 lifts hold with the flip 48 of 48; run back exact.
- CONTROL: 48 random signed permutations (not a homomorphism) ALSO hold 48 of 48 at J = 0: at J = 0 the act knows no
  kind (SYM24 said it); the families' act probes (all at J = 0) measured the carry lemma alone, never the kind.
- J laid through the kind's own table C[G3/2 x G3/2 -> T1] (group sum over the 48 from the seed (0,0,0), 24 entries in
  {-2..2}, 24 monomials, J not 0 at 265 of 567 gears, counts within 35 bits over 4 rounds at W = 9): the true 48 hold
  48 of 48; the random control 0 of 48; the mutant (one table entry + 1) 2 of 48; the table kept by all 48: True.
=> A half-speed (Kramers, full turn -1) kind rides Tensor24's act as built, bit for bit, with all 48, at any W, coupled
   to the vector train through its own table. The text's Open item 1 ("the carry for a half-speed train") is not a
   wall for G3/2; the wall is for spin 1/2 on fewer than 24 gears.
## p4_lemma.txt: the lemma is tight: 2 gears, W = 2: of 625 whole P x 24 bijections of the box, exactly the 8 signed
   permutations commute, each with the forced flip; W = 3 affine: the same 8 with c = W - 1 on negated rows; W = 1: all.

## p5_more.txt (16:50)
- Spin 1/2 on the act: the 24-gear form, J laid through its own table (24 x 24 -> T1, 24 monomials, J not 0 at 602
  of 999 gears, 24 bits over 4 rounds, W = 9): true 48 hold 48/48, random control 0/48, mutant 2/48.
- The text's 16-gear G3/2: a representation, -192, End dim 16, forms 6 + 10 (as the text), but it is TWO copies of
  the 8-gear least whole form (4 G3/2 over C), not four (the text's arithmetic slip).
- Lambda's positive invariant forms a N0 + b N1 (a > |b| sqrt 2): Gram(2N0) +- Gram(2N1) has det 1 and an even
  diagonal [4,4,2,2,10,2,4,4]: Lambda with Tr(((2 +- sqrt 2)/2) N(x)) is the even unimodular E8. Tr N alone: det 16.
  So "the nearest point of W Lambda" under its canonical metric is E8 decoding (Conway-Sloane: round in two cosets
  of D8 and compare) - comparisons, not one division; and impossible anyway at gcd(W,6) > 1 (fixed classes).
- Probe hygiene: object arrays keyed by tobytes() compare pointers (equal values, different bytes shown); the
  families' probes do this throughout (probe_48, probe_kinds, probe_spinor); it held by the small-int cache; no
  result affected (re-verified by value here), but latent.
