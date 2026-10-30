# The hostile mathematician's report on FAMILIES.md (the families' exchange rule, the first text)

Reader: a mathematician new to Tensor24, 2026-10-30, for the Boss. Read: FAMILIES.md, NOTES.md, the five probes and
their outputs; the law's lines 90, 94, 100, 102, 344, 346, 458 (docs/ALGEBRA.md at 9067de20d); engine/kinds.py,
step.py, contract.py, algebra/carry.py, runner/files.py, runner/load.py; sym24_v2/SYM24.md and common.py (the harness
the probes use). Everything below was rebuilt independently in whole numbers with Rule3's carry as the one division
(tensor24.algebra.carry.carry), in this folder: `zlin.py` (whole-number linear algebra), `p1_cover.py` (the 48 as
2 x 2 matrices over Z[zeta_8], not the text's Z[sqrt 2] quaternions; Lambda; the fixed-class theorem), `p2_induced.py`
(every signed-permutation form of the 48, by induction), `p3_act.py` (the half-speed kind G3/2 on the real act),
`p4_lemma.py` (the carry's lemma, exhaustive), `p5_more.py` (spin 1/2 on the act, the 16-gear G3/2, Lambda's metrics);
each with its `.txt` beside it. The five probes of the text were rerun (`rerun/`): all five outputs byte-identical.
Nothing was written in any worktree.

## VERDICT on the families' text: NOT PASSED

The whole-number algebra the text states is right wherever I could recompute it (every number in SOUND below). What
is wrong is the text's central negative claim and the project's "wall" built on it: that a half-speed kind rides the
per-gear carry in no basis beyond one axis, so that no half-speed family rides Tensor24's act today. A half-speed,
Kramers kind of the 48 (G3/2, the text's own "least whole form of eight gears, not built") IS a signed permutation of
eight gears in a basis the text did not look for, and on the real act it holds with all 48 at every W, coupled through
its own table. Spin 1/2 itself rides signed permutations too, on 24 gears, in the company of E5/2 and G3/2. The law's
line 346 is false as written. The act probes that the text reads as properties of the kinds measure the carry's lemma
alone (a control the text lacks shows it). The wall that remains is real and is proved below: it stands for spin 1/2
on eight (or four) gears, at every W sharing a factor with 6, for every remainder rule whatever, search or no search.

## Items, most serious first

### 1. BLOCKING. "A half-speed kind is monomial in no basis beyond one axis; no basis mends it; no half-speed family rides the act." Refuted: G3/2's least whole form is 48 signed permutations of eight gears, and it rides the act at every W.

Text's places: lines 26-28 ("the act as built carries them bit for bit only at W = 1, or for one axis's eight turns at
any W"), 56-60, 118-124 ("a half-speed kind is monomial in no basis for more than one axis"), 202-206 (the lemma's
last clause), 255 and 258 (the table: "no basis mends it", "no such family rides Tensor24's act today"), 308-313
(Open, "the carry for a half-speed train"), 317 ("G3/2's least whole form (eight gears) is not built").

Measurement (`p2_induced.txt`, `p3_act.txt`): the text tested one lattice basis of eight gears (E1/2 + E5/2 on Lambda,
2 signed permutations of 48), the Gaussian basis (16 of 48) and one 16-gear basis of G3/2 (2 of 48), then argued by
cycle types that (4, 6) and (-4, 3) are no signed permutation of eight gears. That argument is right and settles
E1/2 + E5/2 on eight gears (confirmed, p1). It says nothing of G3/2, whose traces at the third turns' lifts are
+-1 per copy. The whole list of signed-permutation trains of the 48 is the list of induced representations
Ind_H lambda over the subgroups H and sign characters lambda; by Frobenius reciprocity Ind_H lambda contains a kind K
exactly <lambda, Res_H K> times. Every subgroup (one- or two-generated: all of them) and every sign character were
run. The transitive signed-permutation trains carrying a half-speed kind are exactly: 8 gears (H = C6 = <w>, w the
order-6 lift of a third turn, lambda(w) = -1): 2 G3/2 over C, -1 acting as -I; 16 gears (H = C3, lambda trivial):
2 G3/2 plus whole-speed kinds, -1 a derangement (plain permutations, no sign at all); 24 gears (H = {+-1},
lambda(-1) = -1): 2 E1/2 + 2 E5/2 + 4 G3/2, -1 as -I; 48 gears (H trivial). Built explicitly, the 8-gear one: 48
distinct signed permutations of eight gears, a representation on 2304 of 2304 pairs, -1 = -I, (trace, order) =
{(8,1):1, (-8,2):1, (2,3):8, (0,4):18, (-2,6):8, (0,8):12}, SUM trace(M M) = -96 = -2 x 48 (Kramers, Frobenius-Schur
-1 on each constituent), SUM trace^2 = 192 (End of dimension 4: one kind, its commutant a quaternion order of rank
4), invariant forms 1 symmetric + 3 antisymmetric, the quarter turn's lift to the fourth -I; two signed permutations T
in the commutant with T T = -I (Kramers partners, which commute with the act by the sign law). On the real act, with
SYM24's own harness (the cube of side 3, rows [8-gear hand, t1, the square], teeth drawn in [0, W), the flip on
negated rows): W = 9, W = 10 (even), W = 1, six rounds, the 48 lifts hold 48 of 48, the run back exact. With J laid
through the kind's own table C[G3/2 x G3/2 -> T1] (the group sum over the 48 from one seed, 24 entries in -2..2, no
table typed; J not 0 at 265 of 567 gears, 35 bits over 4 rounds at W = 9): the true 48 hold 48 of 48; 48 random signed
permutations in their place hold 0 of 48; the table with one entry raised by 1 holds 2 of 48.

Fix: strike "in no basis" wherever it is not qualified by "of E1/2 + E5/2 on eight gears"; build G3/2's least whole
form as the cosets of C6 with the sign (eight gears), say that it rides the act with all 48 at every W; move "the
carry for a half-speed train" from Open to "open for spin 1/2 alone". Widen line 90 to the kinds whose irreducible
whole form is a signed permutation: A1, A2, T1, T2, G3/2 (E rides inside A1 + E on the square's ii slots; E1/2 + E5/2
rides inside the 24-gear train of item 2, as E rides inside the square).

### 2. BLOCKING. Law line 346, reaffirmed at lines 197-201 and 267-269: "no train of gears turning by signed permutations carries spin 1/2". False as written.

Measurement (`p2_induced.txt` 3, `p5_more.txt` 1): the 48 acting on their own 24 pairs +-g with the sign (Ind from
{+-1} of the sign character) is a train of 24 gears, every lift a signed permutation, -1 = -I, containing E1/2 twice,
E5/2 twice and G3/2 four times (SUM trace(M M) = -384). On the act, J laid through its own table (24 x 24 -> T1, 24
monomials, J not 0 at 602 of 999 gears, 24 bits over 4 rounds, W = 9): the 48 hold 48 of 48, the random control 0 of
48, the mutant 2 of 48. What is true: spin 1/2 rides no signed-permutation train of fewer than 24 gears, and never
alone (every signed-permutation train containing E1/2 contains G3/2 twice as often); the Hurwitz lift on four gears
and the lattice lift on eight are indeed signed permutations in no basis (p1: the cycle types, confirmed).

Fix: line 346 to read "no train of fewer than 24 gears turning by signed permutations carries spin 1/2, and none
carries it alone; the 24-gear train of the 48's own pairs carries 2 E1/2 + 2 E5/2 + 4 G3/2"; the text's lines 199-201
and 267-269 accordingly.

### 3. MINOR (method, but it carries every act result of the text). The act probes at J = 0 cannot see a kind: any assignment of signed permutations to the 48 holds.

Text's places: lines 118-124 (probe_spinor 6, probe_48 4), 132-135 (the partner pair), 255; Measured 2 and 3.

Measurement (`p3_act.txt` 1): at J = 0, 48 random signed permutations of the eight gears, one per lift, no
homomorphism (checked), hold 48 of 48 at W = 9, 10 and 1, exactly as the true lifts do. SYM24 said it ("at J = 0 the
act knows no kind"). So "the Gaussian basis's 16 hold 16 of 16", "+-I hold", "copy 2 stays T of copy 1 in 600 of 600"
are the carry's lemma (signed permutations commute with the per-gear carry), not facts about the 48 or about
half-speed. The departures of the mixing lifts are the same lemma's converse. The text's conclusions here are right;
its measurements do not bear them.

Fix: lay J through the kind's table before reading an act probe as a statement about the kind (as SYM24's plan.txt
did, and as p3/p5 do here: true 48 of 48, random 0 of 48, mutant 2 of 48); or say plainly that the act probes
measure the lemma.

### 4. MINOR. "Pauli in clocks" is antisymmetrization by definition; the belt law is the one declaration; "the sign is now derived, not declared" (line 280) overstates.

Text's places: lines 20-28, 50-55, 146-153, 175-181 (probe_pair 1), 189-196, 280, 340.

Measurement: J_e = phi x chi + e chi x phi satisfies S J_e = e J_e and R J_e = sigma J_e by definition of e and of
sigma; "the belt holds for e = sigma alone" is the identity e = sigma, and probe_pair 1 measures an identity. The
content is the belt law S = R itself, a postulate (the spin-statistics connection), not a derivation from the act or
the kinds. J_-(phi, phi) = 0 holds for every antisymmetric pairing of every kind (two T1 hands in one state have no
cross product; nobody calls that Pauli). "A third has no room" (N(phi) psi = phi <phi, psi> + T phi <T phi, psi>) is
the completeness relation of a module of rank 2: E (whole-speed, rank 2) has the same; G3/2 (rank 4 over C) admits
four. Over the ring Z[zeta_8] the relation divides by N(phi), so the "combination" is over the field. Fix: name the
belt law a premise; strike "never three" for G3/2; say the exclusion's content is e = -1 and nothing else.

### 5. MINOR. "The books break" on two half-speed copies (probe_pair 3) is built into the definitions.

Text's places: lines 125-131, 154-160, 256, 314-316; Measured 5.

Measurement: the "half-speed" train there is an A1 train at part 8 on one Node-clock with no turn applied; two copies
laid alike and tied alike to one giver stay alike under any deterministic act, so J_- = phi x chi - chi x phi is 0 in
every round by construction, while J_+ is not; the same act gives the same counts (0 to 4 each, the giver -7) for the
"whole-speed" and the "half-speed" trains, which differ only in the label and in which of J_+ or J_- the pair click
is declared to read. The failure measured is the choice of J_-. Fix: say so; a test of the pair click needs copies
laid apart (or a coupling through a half-speed table) and the kind's 48 acting.

### 6. MINOR. "G3/2 = E1/2 x E stands on sixteen gears (four copies of its least whole form of eight)" (lines 105-107; probe_spinor 5): 4 x 8 = 32.

Measurement (`p5_more.txt` 2): the 16-gear form is a representation with SUM trace(M M) = -192 and 16 = 6 + 10 invariant
forms (as the text says), four copies of G3/2 over C and TWO copies of the 8-gear least whole form (End = M_2(D),
dimension 16). Fix: "two copies of its least whole form, four of G3/2 over C".

### 7. MINOR. "The Frobenius-Schur sign is the full turn's sign ... one rule" (lines 182-188, 340) is a fact of this group, not a theorem.

Measurement (`p2_induced.txt` 4): on the 48 the two signs agree on all eight kinds (FS +1 and chi(-1) = dim on the
five; FS -1 and chi(-1) = -dim on E1/2, E5/2, G3/2), confirmed. But a double cover D4 -> V4 has a real kind of two rows
with the covering involution -I and Frobenius-Schur +1 (half-speed, symmetric pairing), and the 4-gear complex spinor
of 2T (the text's own probe_48 3) has FS 0 with a full turn -1. Fix: state the coincidence as the 48's, and say which
sign the physics uses (the pairing's); the belt alone decides nothing where they differ.

### 8. MINOR. The carry's lemma (lines 202-206; SYM24 Algebra) is proved only for a row summing two entries with coefficient +1.

Measurement (`p4_lemma.txt`): the complete statement and proof. Let the turn act by any whole matrix P on the counts
and by ANY bijection rho of the remainder box [0, W)^n. From n + r = q W + r' and P n + rho(r) = P q W + rho(r')
follows rho(r') - P r' = rho(r) - P r for all r, r' (any r' is reached from any r by a suitable n), so rho(r) =
P r + c; then P r + c in the box for every r in the box forces every row of P to one entry +-1 at W >= 2 (two
entries in a row, of either signs, overflow the box at r = (W - 1) e_i + (W - 1) e_k or at (W - 1) e_i), c = 0 on a
+ row and W - 1 on a - row: the flip, forced. Exhaustive: two gears, W = 2, 625 whole P times all 24 bijections of
the box: exactly the 8 signed permutations commute, each with its flip; W = 3 (affine rho): the same 8; W = 1: all
625. So "signed permutations alone" is exactly right, including against non-linear relabelings of the teeth. Fix:
cite the general proof.

### 9. MINOR. "The nearest point of W Lambda" (lines 309-310; probe_spinor 7) names no metric, and the reason it cannot be the carry is deeper than "a search".

Measurement (`p1_cover.txt` 5, `p5_more.txt` 3): Lambda keeps two symmetric forms, the two rational coordinates N_0, N_1
of the reduced norm N(x) = N_0 + N_1 sqrt 2; the positive invariant forms are a N_0 + b N_1 with a > |b| sqrt 2, a
two-parameter family; Tr N (a = 2, b = 0 in Gram(2 N_0)) has determinant 16, while Gram(2 N_0) +- Gram(2 N_1) (the
form Tr(((2 +- sqrt 2) / 2) N(x))) has determinant 1 and an even diagonal [4, 4, 2, 2, 10, 2, 4, 4]: Lambda with its
canonical invariant metric is the even unimodular lattice E8. The nearest point of W E8 is E8 decoding (round in two
cosets of D8, compare), comparisons by nature. And by the theorem below no equivariant remainder exists at W = 9 at
all. Fix: name the metric, and replace "a search, which the gate refuses" by the obstruction.

### 10. MINOR. runner/files.py note (lines 303-304): "a half-speed kind has none [whole basis], so the files refuse it as they refuse a lone E".

Measurement: the files' criterion (`vocabulary`'s `wholes`: every matrix of the kind a signed permutation) ACCEPTS
G3/2's 8-gear form, since all 48 are signed permutations in it; it refuses E1/2 + E5/2 on eight gears as it refuses a
lone E, and both ride inside a larger whole train (A1 + E on 3 gears; the 24-gear train of item 2). Fix: the parallel.

### 11. MINOR. Probe hygiene: object arrays keyed by `tobytes()` compare pointers, not values.

Measurement (`p5_more.py` comment; the debug run): `np.array(..., dtype=object).tobytes()` serialises the addresses
of the int objects; two equal matrices computed by different paths gave different bytes here (and a KeyError), while
the probes' comparisons held only because every entry lies in CPython's small-int cache. probe_48 (lines 119-133,
215-216, 250-271, 305-313), probe_kinds (49-50), probe_spinor (217, 315-330, 360, 382) do this. No result of the text
is affected (all re-verified by value here), but any probe comparing larger integers this way fails silently. Fix:
key by `tuple(map(tuple, m.tolist()))`.

## The wall: the carry for a half-speed train, what is proved

The question: is there a division with remainder on a whole hand of four or eight numbers at once (the Hurwitz
quaternions under the even 12's cover 2T; Lambda under the 48) that is a bijection with a mirror, equivariant under
the group, free of search, if and comparison, and the per-gear carry on whole-speed hands?

**Theorem A (no equivariant remainder at gcd(W, 6) > 1; `p1_cover.txt` 3 and 4).** Let G be the 48 on Lambda (or 2T
on the Hurwitz order), W >= 2. A remainder rule is a map rho: Lambda -> Lambda with rho(x) = x mod W Lambda; its
domain D = rho(Lambda) is a set of representatives of Lambda / W Lambda, and the carry n + r = q W + r' is then a
bijection (n, r) <-> (q, r') on Lambda x D. Equivariance rho(g x) = g rho(x) makes D G-stable. If a class [x] is fixed
by g (that is (g - 1) x in W Lambda), its representative d satisfies g d = d; but left multiplication by a unit g != 1
of a division algebra fixes no vector but 0. So every class fixed by some g != 1 must be the class 0. The classes
fixed by g are the kernel of M_g - I on (Z / W)^8, of size the product of gcd(d_i, W) over the Smith diagonal of
M_g - I, computed: order 2 (-1): (2, 2, 2, 2, 2, 2, 2, 2), det 256; order 3: (1, 1, 1, 1, 3, 3, 3, 3), det 81; order 4:
(1, 1, 1, 1, 2, 2, 2, 2), det 16; order 8: (1, 1, 1, 1, 1, 1, 2, 2), det 4; order 6: (1, ..., 1), det 1. Hence at every
even W and every W divisible by 3 some g != 1 fixes a nonzero class, and NO equivariant remainder rule exists, by any
method, search or formula. Witness at W = 9: x = 3 (1 - g^-1) e_1 = (3, 0, 6, 0, -6, 0, 9, 0) for a third turn's lift g:
(g - 1) x = 0 mod 9, x != 0 mod 9. The Hurwitz order under 2T: Smith (1, 1, 3, 3) for order 3, (2, 2, 2, 2) for -1,
(1, 1, 2, 2) for order 4, (1, 1, 1, 1) for order 6: the same conclusion for every W sharing a factor with 6. The
engine's standing W = 9 is such a W; so is every even W.

**The flip does not help.** The engine escapes the same obstruction for one negated gear (W even: the class W / 2 is
fixed by -1 with no fixed representative) by relabeling the remainder, r -> W - 1 - r: an affine map whose centre
(W - 1) / 2 is not a lattice point. On Lambda every such relabeling is x -> g x + c_g with c a 1-cocycle; over Q,
c_g = (1 - g) v for one v; the order-6 lift w has det(1 - M_w) = 1 (1 - w is a unit of the order), so c_w in Lambda
forces v in Lambda, and the relabeled action is the linear one translated by a lattice vector: H^1(48, Lambda) = 0,
and Theorem A applies to every relabeling. (The same for 2T on Hurwitz: w is in 2T.)

**Theorem B (gcd(W, 6) = 1: it exists, but is never the per-gear carry).** The Smith entries are 1, 2, 3 only, so for
W prime to 6 every g != 1 acts without fixed nonzero classes: the 48 act freely on the W^8 - 1 nonzero classes
(48 divides W^8 - 1, checked for W = 5, 7, 11, 13), and a G-stable D exists: 0 and one lattice point per orbit, its
orbit carried along, (W^8 - 1) / 48 choices (8138 at W = 5; 120100 at W = 7), each with infinitely many lattice
points to choose from. Such a D is a box [0, W)^8 in no basis, since the per-gear box is stable under signed
permutations alone (item 8) and the 48 are signed permutations in no basis of Lambda (the cycle types): so no
equivariant rule on Lambda is a per-gear carry, in any basis. The mirror is free: D = -D for every G-stable D since
-1 is in the group. What a choice would cost: a metric a N_0 + b N_1 (the canonical one makes Lambda E8) and the
nearest point of W Lambda, ties broken orbit by orbit, which is E8 decoding with comparisons; or a table of
(W^8 - 1) / 48 orbit representatives: what lines 35 and 100 forbid. Whether a comparison-free formula exists for some
W prime to 6 I cannot prove impossible; I can prove it is not a carry per gear in any basis, and not any rule at all
at the standing W = 9 or at any even W.

**Theorem C (the per-gear carry is exactly the signed permutations' own; item 8).** With any relabeling of the teeth.

**The positive side, measured (`p3_act.txt`, `p5_more.txt`).** The wall is for spin 1/2 on eight or four gears. The
half-speed kind G3/2 (full turn -1, Kramers) rides the per-gear carry with all 48 on eight gears at every W, coupled
to the vector train through its own invariant table (48 of 48; the random control 0 of 48; the mutant 2 of 48); spin
1/2 rides it on 24 gears in the company of E5/2 and four G3/2 (48 of 48; control 0; mutant 2). So "one division with a
carried remainder" (line 90) already carries a half-speed family; what it does not carry is E1/2 + E5/2 alone, and
the eight-gear hand of Lambda should be given up as a carrier, not the half-speed kinds.

## SOUND, with numbers (my own construction, p1, p2, p5; the text's probes rerun)

- The 48: closed from two lifts (2 x 2 over Z[zeta_8] here), 48 elements, -1 among them, covering the 24 signed
  permutations of det 1 two to one; orders 1:1, 2:1, 3:8, 4:18, 6:8, 8:12; tr(q) whole on 36, +-sqrt 2 on 12 (the six
  quarter turns' lifts); SUM tr(q q) = -48 (FS -1), SUM tr(q)^2 = 48.
- Lambda = Z[sqrt 2] 2O: rank 8, a ring; the 48 as whole 8 x 8 matrices of determinant 1, M(x) M(y) = M(x y) on 2304
  of 2304, -1 = -I; (trace, order) {(8,1):1, (-8,2):1, (-4,3):8, (0,4):18, (4,6):8, (0,8):12}; SUM trace(M M) = -192;
  SUM trace^2 = 384; invariant forms 8 = 2 symmetric + 6 antisymmetric (null space and characters agree); 2 signed
  permutations in the lattice basis; (-4, 3) and (4, 6) in no cycle type of eight gears: E1/2 + E5/2 is monomial in no
  basis of eight gears (the text's cycle-type argument is sound); it is one kind over Q (End of dimension 8).
- Hurwitz under 2T: rank 4, 24 whole 4 x 4 of det 1, SUM trace(M M) = -48, forms 1 + 3, (trace, order) {(4,1), (-4,2),
  (-2,3):8, (0,4):6, (2,6):8}, (-2, 3) and (2, 6) in no cycle type of four gears.
- The five kinds of the 24 from my own matrices: FS +1 on each; Alt^2 E = A2, Alt^2 T1 = Alt^2 T2 = T1, Alt^2 A1 =
  Alt^2 A2 = 0; so the antisymmetric channels are E x E -> A2, T1 x T1 -> T1, T2 x T2 -> T1 and none into A1 (the
  engine's tables' swap signs, probe_kinds 3, agree with this by characters).
- FS sign = full-turn sign on all eight kinds of the 48 (as a fact of this group).
- The 16-gear G3/2: a representation, -192, 16 = 6 + 10 forms (but two copies of the least form, not four).
- The pairing algebra of the Gaussian basis (probe_pair 2): det alternating, T T = -1, <phi, T phi> = 0,
  det(phi, T phi) = N(phi): right, and clearer once T is named: T phi = phi j, right multiplication by j, which
  commutes with the 48 on the left for that reason; the winding is right multiplication by zeta^k.
- The Gaussian basis's 16 lifts (probe_spinor 4): the stabilizer of Z[zeta_8] + j Z[zeta_8] is the binary dihedral
  group of order 16 covering the x axis's dihedral eight; the structure is right (their measurement reproduced).
- The carry's lemma's conclusion (signed permutations with the flip, W >= 2; all whole matrices at W = 1): right and
  tight (item 8).
- The five probes: outputs byte-identical on rerun.

## On Solution24 (one line)

Step 8 ("run locally, with mutants") failed here for want of the control that distinguishes a measurement from a
tautology: an act probe at J = 0 must be run against random signed permutations, and a "no basis" claim against
every whole form (the induced ones), before it enters the ladder as measured.
