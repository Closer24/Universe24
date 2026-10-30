# Reading notes (hostile mathematician), 2026-10-30

Read: ONE_ALGEBRA.md, NOTES.md, q_lib.py, the nine probes and their .txt; engine step.py, state.py, kinds.py,
mesh.py, contract.py, carry.py, runner/load.py, board.py, files.py, main.py; examples/tensor24/*.json;
fam_math/REPORT.md; edge/EDGE.md, edge_lib.py; docs/ARCHITECTURE.md (Solution24).

## Engine facts confirmed from the code
- gear: q, r+ = carry(W (a - b) + push, W, r); a+ = a + q; b+ = a. drive: carry(J, T_d, rd). push = s (F + T_k q_d).
- W = rest + read(clock, a) with rest = 6 den Gamma^2 (len(spokes) * grip), every row reading the square's 00 slot at 1.
- grip of a Mesh = den Gamma^2 + ii slot at both ends (gripped). pull F = sum_k grip_k (nb_k - own).
- mirror: (b, a, flip(r, W(b)), flip(rd, T_d)); untick = mirror o tick o mirror.
- Gearing arrays are (rows, 1): per-row s, T_k, T_d are possible in the data structure (the probes set them so);
  the load lays them alike. So "one scalar on the quaternion" is a property of the load, as the text says.
- The 24 = signed permutation matrices of det 1 with rows Spokes; A2 = det of the permutation part (sign of the axis
  permutation); square(held) = beside(beside(a1, t1), beside(t1*t1, t2)): slots 00, 0i, ii (permutation), jk (T2).

## Paper check of the carry theorem (finding 1)
- (i) affine remainder: proof OK given that the tooth's turn is a map of the tooth alone (hypothesis implicit).
- (ii) H^1 = 0: c_g = (g-1) a, a = -(1/|G|) sum c_h in L (x) Q; coboundary iff a in L since A^G = 0; order-6 lift has
  N(g-1) = 1 so g-1 a unit of H (and of O_48): a in L. OK.
- (iii)-(iv) fixed cosets iff gcd(W, [L:(g-1)L]) > 1; indices N(g-1)^2 (H) and Nm(N(g-1))^2 (Lambda): 16, 4, 9, 1 on H;
  256, 16, 81, 1, 4 on Lambda. OK. Primes 2 and 3 only (|2O| = 48 anyway: Maschke mod p for p not dividing 48).
- BUT the framework is "r in a set D of coset representatives, the same D for every quotient". The text says this
  "is what makes the act bijective and the run back a mirror". That is sufficient, not necessary: the project's own
  edge form (EDGE.md, the tie-even split) uses a remainder set that depends on the quotient's parity, is bijective
  and mirrored (s -> -s) and lives on an EVEN dial 2D where -1 fixes the class D: exactly what the theorem's
  framework forbids in rank 1. Hypothesis to test: on H under 2T, left multiplication by g != 1 fixes no nonzero
  lattice point, so a G-equivariant quotient map Q: H -> H with bounded cells exists at EVERY W (transport orbit
  representatives of G on H \ 0); with states valid iff Q(W(a-b) + r) = a - b, the state map is a bijection, the
  mirror (b, a, -r) inverts it, and equivariance holds for every lift. If so, the "iff" is an artifact of the
  fixed-domain framework. -> probe qa3.

## Paper check of the double Node-clock (finding 0)
- q = z1 + z2 j, i q = phase on both slots; q j = -z2 + z1 j = the step at t = 0; (i q i^-1) j = z2 + z1 j = swap;
  q (1 - j) = (z1 + z2) + (z2 - z1) j. All trivial identities. Right multiplication by a unit quaternion = SU(2) on
  (z1, z2); [[t, -1], [1, 0]] is unitary iff t = 0. Stronger: for t = +-1 the invariant Hermitian form has Gram
  [[1, -t/2], [-t/2, 1]] of determinant 3/4, not a square of a rational times a unimodular one, so in NO whole basis
  of Z[i]^2 is the step a right multiplication by a unit quaternion. The text's "at no other mode" is right and
  can be strengthened.
- At W | k with a spring alone, the dividend is W(a - b) - k a + r: the carry is inert (q exact, r still). The whole
  quaternion reading lives where the carry does nothing.
- Scope claim "the unit step is the lone clock's or the uniform hand's" (probe_double): suspect. The step is q j
  wherever the round's total push is -2 W now; on a board, eigen-hands of the pull with k + s lambda G = 2 W do
  it with F != 0; on an even board the checkerboard hand at k = 0 (no spring) does it. -> probe qa4.

## The units as gears (Answer 0, second paragraph)
- "the group ring escapes the gcd(W, 6) wall (it has fixed vectors, the orbit sums...)": with -1 = -1 imposed,
  L(-1) = -I, so the 24-gear train has NO nonzero fixed vector and every orbit sum vanishes. The real reason it
  escapes: the lifts are monomial in that basis and the flip twist c_g = (W-1) on negated rows is a cocycle that is
  NOT a coboundary at even W (a = -(W-1)/2 (1,...,1) not whole); the H^1 argument fails because g - 1 is not a unit
  on Z^24 (expected det(L(g) - I) = 2^8 = 256 for order 6: eight 3-cycles of pairs with sign product -1). -> qa5.

## Smaller points
- Determinants -48, -16, -128 (probe_square) depend on the normalization of the forms (Im(h h) = 2 a v carries a 2);
  the invariant content is rank 5 and the elementary divisors of the change of basis. -> qa6.
- "the velocity is the j slot of q (1 - j)" (Answer) vs "the velocity, negated" (body): the j slot is before - now.
- "the edge's determinant W'/W" is an identity of a non-linear map; wording.
- fam_math REPORT's phrase "the carry n + r = qW + r' is a bijection (n, r) <-> (q, r')" is false as a map on pairs
  (it is |D| to 1); the bijection is the state map. ONE_ALGEBRA says "bijective division" loosely; same remark.
