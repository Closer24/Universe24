# fam_math: hostile mathematician's working notes (saved as I go)

## Read so far
- FAMILIES.md whole (357 lines), NOTES.md, probe_48.py/.txt, probe_spinor.py/.txt.

## First suspicions to check (from the reading alone, before probing)
1. "no signed permutation of eight gears has (trace, order) = (4, 6) or (-4, 3)". Cycle-type arithmetic: a signed
   permutation of 8 gears with trace 4 and order 6: fixed points contribute +-1 each, cycles of length k>=2 trace 0.
   Trace 4 needs at least 4 fixed +1 (or 5 fixed +1 and 1 fixed -1 etc.). Order 6 needs a 3-cycle (or 6-cycle, or a
   3-cycle and a 2-cycle / negative 1-cycle). 4 fixed (+1) + 3-cycle (+) + 1 fixed(-1): trace 3, order lcm(1,3,2)=6.
   5 fixed(+1) + 3-cycle: trace 5, order 3. 4 fixed + 3-cycle + ... only 8 gears: 4+3=7, one left: +1 -> trace 5 order 3;
   -1 -> trace 3 order 6. 6 fixed(+1) + 2-cycle(-): trace 6, order 4. Hmm: 4 fixed(+1), 2-cycle(+) ... trace 4 order 2.
   What about 5 fixed +1, 1 fixed -1, 2-cycle: trace 4, order 2. 4 fixed+1, 1 fixed -1, 3-cycle: 8 gears, trace 3.
   The claim looks right for signed permutations. BUT the argument "trace must match" assumes the matrix of the lift
   in the new basis has the same trace (true, trace is basis-invariant) and the same order (true). So the cycle-type
   argument is sound for signed permutations. The real question: is "monomial in no basis" the right criterion?
   The carry lemma says the per-gear carry commutes only with signed permutations. Need to check this lemma exactly:
   does carry commute with other maps, e.g. the map x -> -x (yes, sign law with flip), maps that permute AND something?
   What about the per-gear carry commuting with scaling by -1 on the whole and with permutations: group is the
   hyperoctahedral group of signed permutations. Could it commute with anything else linear? A linear map L commuting
   with the per-gear floor-division (W-step) for all inputs... Let's test: carry(n, W, r) per gear is q = floor((n+r)/W),
   r' = (n+r) mod W. For L to commute we need L(floor(x/W)) = floor(L x / W) for all integer vectors x. Taking x = W y
   gives L y = floor(L y) trivially. Taking x with entries in [0,W): floor(x/W)=0 so need floor(L x / W) = 0, i.e.,
   L x in [0, W)^n for all x in [0,W)^n. For L integer and W >= 2, L maps the box [0,W)^n into itself; with x = e_i
   gives columns of L in [0,W)^n so nonnegative entries; x = (W-1)*ones gives (W-1)*L*ones in [0,W)^n so row sums <= 1.
   Nonneg integer with row sums <= 1 and invertible => permutation matrix. With the "tooth flip" (the sign law), the
   negated rows are handled by a separate convention. So the lemma holds for the plain per-gear carry: only
   permutation matrices (and with the flip, signed permutations). OK, but this is on the MAP of a, b, r together.
   Need to check what "the tooth flip" does exactly and whether it is really the carry commuting or a redefinition.
2. The Frobenius-Schur sum on the lattice rep of rank 8: -192 = -4 x 48. The FS indicator of a rep is (1/|G|) sum
   chi(g^2); for the realification of the rank-8 lattice, chi = 2 Re(trace) of quaternionic... Lambda tensor R =
   H (x) Q(sqrt2) tensor R = H + H (two copies of the real quaternion algebra, by the two embeddings of sqrt 2), as a
   left module over the 48: each H is the realification of the 2-dim complex spinor, which as a real rep is 4-dim
   irreducible of quaternionic type with character 2 chi_2 (real). Sum of chi(g^2) over 48 for realified E1/2 is
   2 * (-48) = -96; two Galois conjugate copies give -192. Fine: -192 = sum. FS "indicator" per irreducible: -1 each.
   "pairings kept 8, symmetric 2, antisymmetric 6": dim Hom_G(V,V) for V = H_1 + H_2 (two non-isomorphic real
   quaternionic irreps): End = H + H, dim 8; the bilinear invariants V x V -> R: V* = V so dim 8; symmetric ones:
   (n + fs)/2 = (8*48*... wait they compute n = SUM trace(M)^2 = 8*48 = 384, (384 - 192)/96 = 2 symmetric, 6 antisym.
   Check: for a quaternionic-type real irrep of dim 4 (H), the invariant bilinear forms: dim Hom_G(V (x) V, R) =
   dim Hom_G(V, V*) = dim Hom_G(V, V) = 4 (= dim H). Symmetric: 1 (the dot), antisymmetric: 3. Two copies: 2 + 6. OK.
3. "E1/2 + E5/2 one whole kind of eight gears": E1/2 (spin 1/2 rep of binary octahedral 2O) and E5/2 (its Galois
   conjugate, sqrt2 -> -sqrt2). The Q-irreducible rep of 2O containing E1/2 has character field Q(sqrt 2), Schur index
   2 (quaternionic), so the minimal Q-rep is of dimension 2 * 2 * 2 = 8. Yes the claim "one whole kind of eight gears"
   is right; it is Q-irreducible (not Z-irreducible necessarily but that's fine). OK.
4. G3/2 = E1/2 x E "on sixteen gears (four copies of its least whole form of eight)". G3/2 is the 4-dim irrep of 2O
   with rational character and Schur index 2 (quaternionic type, FS -1), so its minimal real form is 8-dim. 8 x 2 = 16
   = (E1/2+E5/2 whole, dim 8) (x) E (dim 2) = 16 dims; complexified: (2 E1/2 + 2 E5/2) (x) E = 2 G3/2 + 2 G3/2 = 4 G3/2
   (since E1/2 (x) E = G3/2 and E5/2 (x) E = G3/2). The text says "four copies of G3/2": in complex terms, yes 4 copies
   of the 4-dim complex G3/2 = 16 dims. But its "least whole form of eight" would be the real 8-dim = 2 G3/2 complex.
   So 16 real dims = 2 copies of the least whole form, = 4 copies of the complex G3/2. The text's "four copies of its
   least whole form of eight" is WRONG arithmetic: 4 x 8 = 32 != 16. Check the exact wording: "G3/2 = E1/2 x E stands
   on sixteen gears (four copies of its least whole form of eight)". Yes: that's an arithmetical slip. Probe text says
   "four copies of G3/2 (its least whole form is eight gears, not built here)" - it's 4 copies of complex G3/2 = 2
   copies of the least whole 8. MINOR but a real error. Also "pairings kept 16, symmetric 6, antisymmetric 10": for
   V = 2 copies of a quaternionic real irrep of dim 8 (End = M_2(H), dim 16); bilinear invariants: dim 16; symmetric:
   (16*48 - 192)/96 = (768-192)/96 = 6; antisym 10. For 2 copies of a quaternionic irrep W: Sym^2(W+W) invariants =
   Sym^2 W inv (1) *2 + (W (x) W) inv (4) = 6. Yes. OK.
5. "SUM Tr(M^2) = -192 = -4 x 48" fine.
6. The belt argument: "S J = R J on the pair's hand J_e = phi(x)chi + e chi(x)phi for e the full-turn sign only".
   Note R J_e = sigma J_e where R acts on ONE factor by a full turn (which is sigma * identity on the kind). S J_e =
   e J_e. S = R on J_e iff e = sigma OR J_e = 0. This is a tautology dressed as a law: "the exchange sign is the full
   turn sign" is the spin-statistics theorem's content, but the "derivation" here is: define S = R as a law (the belt
   trick), then e = sigma follows. The belt trick is a POSTULATE (the law "S = R on a pair hand that is not 0"). The
   text says "the sign is now derived, not declared". That is false: the belt law S = R is the declaration. Must flag:
   BLOCKING or MINOR? It is a logic point: the derivation of the exchange sign from the full-turn sign is a
   postulate relabeled. Hmm, but the owner asked for "a rule on the families, something algebraic". The text claims
   "derived". I'd call it MINOR-to-BLOCKING on honesty: the belt law is an assumption. Actually it also claims the FS
   sign equals the full turn sign "so the belt and the pairing give one rule". For 2O: the faithful irreps have -1 at
   -I, and FS indicators: E1/2 -1, E5/2 -1, G3/2 -1. For the 24's kinds (lifted), FS +1 and +1 at -I. So on this group
   the two coincide. Is that a theorem? For general groups, no: a faithful rep of a double cover can have FS 0 or +1
   (e.g. the signed-permutation double cover of the even 12 = 2T, which is the complex 2-dim rep of 2T = SL(2,3): FS 0,
   -1 at -I; the text acknowledges that: "there the belt alone fixes e = -1"). So the coincidence "FS sign = full-turn
   sign" is a fact about 2O alone (and even there "both ways"), not a law. The text says "on these groups". OK.
7. "Pauli's algebra: det(phi,phi)=0, TT=-1, det(phi,Tphi)=N(phi), no room for a third": these are algebra of a rank-2
   module over Z[zeta_8]; the statements are correct in a 2-dim module over a commutative ring (det alternating). But
   "a third clock is a Z[zeta_8]-combination of those two and has no room": N(phi) psi = phi<phi,psi> + Tphi<Tphi,psi>
   requires dividing by N(phi) over Z[zeta_8]; over the FIELD Q(zeta_8), any third vector is a combination; over the
   ring, only when N(phi) divides. The "exclusion" as "no room" is linear dependence in a 2-dim space: that's a
   statement about a 2-dim representation, not about exclusion. Any two-dimensional kind has it. The text says so
   ("three hands of a two-dimensional kind are never independent"). This is NOT Pauli; it is dimension. E (dim 2)
   has the same property, and E is whole-speed. Hmm, the E kind of the 24: a third E-hand is a combination of two
   independent ones, too. So "no room for a third" is NOT a property of half-speed. Flag.
8. "det(phi, phi) = 0 exactly" for the antisymmetric pairing: trivially true for ANY antisymmetric bilinear form.
   And for the whole-speed kinds the "one state" pair hand is J_+(phi,phi) = 2 phi(x)phi which has size 4N^2: also
   trivial. "Two in one state have no pair hand": J_-(phi,phi) = 0 is trivial for every kind; the whole content is in
   choosing e = -1 for half-speed kinds, which comes from the belt postulate. So the "Pauli in clocks" reduces to:
   IF the pair hand is antisymmetrized THEN it vanishes on equal arguments. Tautology.
9. The "mirror T phi = (-conj z2, conj z1)": T T = -1 is Kramers; T is a signed permutation of 8 gears (conjugation in
   Z[zeta_8] in basis 1,zeta,zeta^2,zeta^3: conj(zeta) = zeta^-1 = -zeta^3, conj(zeta^2) = -zeta^2 -> conj is a signed
   permutation of the 4 coefficients: (a,b,c,d) -> (a, -d, -c, -b). Yes signed permutation.) OK. But T is
   ANTILINEAR over Z[zeta_8], right-multiplication... Actually T = left mult by j? j (z1 + j z2) = j z1 + j j z2 =
   j z1 - z2... hmm, j z1 = conj(z1) j for z1 in Z[zeta_8] = Z[i, (1+i)/sqrt2]... j zeta = conj(zeta) j? j i = -i j, and
   j sqrt2 = sqrt2 j, so j zeta = j (1+i)/sqrt2 = (1-i)/sqrt2 j = conj(zeta) j. So j(z1 + j z2) = conj(z1) j - z2 =
   -z2 + j conj(z1). So T phi = (-conj z2, conj z1)... hmm wait: j z2 = conj(z2) j, j(j z2) = j conj(z2) j?? Let me redo:
   j * (j z2) = j^2 z2 = -z2. j * z1 = conj(z1) j = j conj(z1)?? j conj(z1) = conj(conj(z1)) j = z1 j. Hmm: j z1 =
   conj(z1) j. In the form "z1' + j z2'" we need j z1 written as j * something: j z1 = j z1 (already of the form j z2'
   with z2' = z1). So j(z1 + j z2) = -z2 + j z1. So left mult by j is (z1, z2) -> (-z2, z1), which is LINEAR over
   Z[zeta_8] (right scalars). The text's T = (-conj z2, conj z1) is j composed with conjugation: an antilinear map.
   Does T commute with the 48 (left mult)? Left mult by s in 2O on Lambda, T = left-j composed with "conj" where
   conj acts... Conjugation of the Z[zeta_8] coefficients in basis (1, j): x = z1 + j z2 -> conj(z1) + j conj(z2).
   Hmm, is this "coefficient conjugation" the quaternion conjugation composed with something? Quaternion conjugate
   of z1 + j z2 = conj(z1) + conj(j z2) = conj(z1) + conj(z2)(-j) = conj(z1) - conj(z2) j = conj(z1) - j z2 (since
   conj(z2) j = j z2). So coefficient conjugation sends z1 + j z2 -> conj(z1) + j conj(z2); quaternion conj gives
   conj(z1) - j z2. Different. The coefficient conjugation C: is it an automorphism of H? C(z1 + j z2) = conj(z1) +
   j conj(z2). Take x = i: z1 = i, z2 = 0: C(i) = -i. C(j) = j. C(k) = C(i j) = C(-j i)... k = i j = j (-i)?? i j = k,
   j i = -k, so k = i j = -j i = j (-i): z1 = 0, z2 = -i: C(k) = j conj(-i) = j i = -k. So C: i -> -i, j -> j, k -> -k:
   that's the map x -> -j x j^{-1}... conjugation by j: j i j^-1 = j i (-j) = -j i j = -(-k) j... let me: j i = -k,
   -k j = -(k j) = -i. So j i j^{-1} = -i. j j j^-1 = j. j k j^-1 = (j k)(-j) = i(-j) = -k. Yes C = conjugation by j =
   inner automorphism Ad_j. Ad_j is LINEAR (it's a ring automorphism). So T = L_j o Ad_j: x -> j (j x j^-1) =
   j^2 x j^-1 = -x j^-1 = -x (-j) = x j. So T = RIGHT multiplication by j! T phi = phi j. That's right-multiplication by
   j, which commutes with all left multiplications (the 48). T T = x j j = -x. Good: T is right mult by j, a
   Z[zeta_8]-ANTILINEAR map (since j zeta = conj(zeta) j, right-mult by j conjugates the right scalars). Fine: so the
   "partner" is phi j. The Kramers pairing <phi, phi j> = 0 and det(phi, phi j) = N(phi): consistent with conj(x) y
   for y = x j: conj(x) x j = N(x) j => <,> part 0, det part N(x). OK consistent.
   And the "winding" = right mult by zeta^k; T anticommutes with winding in the sense phi zeta j = phi j conj(zeta):
   "the partner's winding minus the hand's". OK.
10. "two half-speed copies' pair hand never clicked while the books of keys break": need to check what they measure.
11. The decisive question: a division with remainder on Lambda (or Hurwitz) equivariant under 48, bijective with a
    mirror, no search/if/comparison, per-gear carry on whole-speed hands. Think: Euclidean division in Hurwitz
    quaternions is NOT unique (nearest-point needs choice; the Hurwitz order is Euclidean but the remainder is not
    canonical). Any G-equivariant remainder map rho: Lambda -> fundamental domain D of W Lambda needs D itself to be
    G-stable, with D a set of coset representatives of Lambda / W Lambda. G = 2O acts on Lambda / W Lambda
    (a finite module of order W^8). A G-equivariant section of Lambda -> Lambda/W Lambda exists iff there is a
    G-stable set of representatives, i.e., a G-equivariant map Lambda / W Lambda -> Lambda splitting the projection.
    Since G acts freely on Lambda \ {0}? -1 acts as -I, so orbits: the fixed points of G on Lambda/WLambda. For a
    set of representatives D to be G-stable, each G-orbit on Lambda/WLambda must lift to a G-orbit in Lambda of the
    same size, i.e., the stabilizer of a class [x] must fix the representative d. Class 0 must be represented by a
    G-fixed element of Lambda, and the only G-fixed element of Lambda is 0 (since -1 in G acts as -I). Fine, 0.
    Class [x] with stabilizer H (containing -1 maybe): if -1 fixes the class, then 2x in W Lambda, and the
    representative must be fixed by -1, so d = 0, contradiction unless x in W Lambda. So: if W is even, the class
    of (W/2) e for e a lattice vector is fixed by -1 but any representative d satisfies -d = d => d = 0, not in the
    class. So for even W NO equivariant remainder exists. For odd W: -1 fixes only class 0. Other stabilizers: an
    element g of order 3 (trace -4 lift... ) fixing a class mod W: need g x = x mod W with x not 0 mod W; then
    representative d must satisfy g d = d, so d in the fixed sublattice of g, which has rank... g of order 3 in 2O
    acting on Lambda = H + H (real), as left mult by a unit quaternion of order 3 (e.g. w = (1+i+j+k)/2 ... actually
    w has order 6, w^2 of order 3), fixed vectors of left mult by a non-real unit: none (q x = x => (q-1) x = 0 =>
    x = 0 since q - 1 is invertible in H). So no nonzero fixed vectors for any g != 1 in Lambda (left mult by a unit
    != 1 has no fixed points in a division algebra). So D must consist of 0 and free orbits, and every class in
    Lambda/WLambda other than 0 must have trivial stabilizer in G. Is that so for odd W? Lambda/WLambda for W odd: as
    G acts... the class [x] fixed by g means (g-1) x in W Lambda. g-1 is an element of the order with norm N(g-1) =
    2 - 2 Re g = 2 - trace. For order-3 elements Re g = -1/2, N(g-1) = 3. So (g-1) x in W Lambda; if 3 and W are
    coprime, g-1 is invertible mod W (in the order), so x in W Lambda, OK. For order 4 elements (quarter turn lift)
    N(g-1) = 2 - sqrt 2... hmm in Z[sqrt2] norm; (g-1) is a unit times something with norm 2-sqrt2 whose Z-norm is
    (2-sqrt2)(2+sqrt2) = 2: so it's a prime above 2 - invertible mod odd W. Order 6: Re g = 1/2, N(g-1) = 1 => unit.
    Order 8: Re g = +-sqrt2/2... = +- 1/sqrt2, N(g-1) = 2 -+ sqrt 2: Z-norm 2. Order 2 (-1): N = 4. Order 3: N = 3.
    So for W coprime to 6 (gcd(W,6)=1), the action of G on (Lambda/WLambda) \ {0} is FREE, and a G-stable set of
    representatives EXISTS set-theoretically (pick one rep per orbit and transport). But for W divisible by 3 (e.g.
    W = 9, the standing W!), the order-3 elements fix nonzero classes mod 3 and hence mod 9 (x = 3 y with y suitable?
    we need (g-1) x in 9 Lambda; (g-1) has norm 3 so (g-1) Lambda contains 3 Lambda (since conj(g-1)(g-1) = 3), so
    x in (g-1)^{-1} 9 Lambda = 3 conj(g-1) Lambda... wait (g-1)^{-1} = conj(g-1)/3, so (g-1)^{-1} 9 Lambda =
    3 conj(g-1) Lambda, which is a sublattice strictly between 9Lambda and 3Lambda... Lambda contains 3 conj(g-1)
    Lambda which contains 9 Lambda. So x = 3 conj(g-1) y is fixed by g mod 9, and is non-zero mod 9 when conj(g-1) y
    not in 3 Lambda, i.e. when y not in (g-1) Lambda / ... fine, such x exist). Then its representative would have to
    be g-fixed, impossible. So for W = 9 (and any W divisible by 2 or 3) NO 48-equivariant remainder map exists at all,
    search or no search. THEOREM. For W coprime to 6, one exists set-theoretically, but "free of search, if and
    comparison" is a different matter: can it be written as a formula? The standard per-gear carry with a fixed box
    is equivariant only under the box's symmetries (signed perms up to the flip). Any equivariant remainder set D
    for Lambda/WLambda, W coprime to 6: is there a "nice" D, e.g. a fundamental domain that is a union of G-orbits?
    For the quaternion side: Hurwitz order with 2T (24 units) or the full 48 (2O acting on Hurwitz? 2O is not in the
    Hurwitz units; but 2O's elements with sqrt2 don't preserve the Hurwitz order... Actually left mult by (1+i)/sqrt2
    doesn't preserve H_Hurwitz. So on Hurwitz quaternions (rank 4) only the 24 units of 2T (the even 12's double
    cover) act; and the quarter turns' lifts don't. Hence "equivariant under the 48" on a 4-gear hand is
    impossible from the start: the 48 do not act on a rank-4 lattice over Z (the trace sqrt 2 argument). Right, the
    text says that.)
    Also need: bijection "with a mirror" = reversibility: the step must be invertible (untick). The per-gear carry
    (n + r = q d + r') is a bijection (n, r) <-> (q, r') given d: yes since 0 <= r' < d. Equivariance under G of
    the REMAINDER map requires the domain D of remainders to be G-stable. For odd W coprime to 3 it's possible
    set-theoretically but requires defining D; a natural candidate: can D be chosen as a "Voronoi-like" region? The
    nearest-point region (Voronoi cell of W Lambda) is G-stable since G acts by isometries fixing W Lambda, but its
    boundary needs tie-breaking: the Voronoi cell has boundary points equidistant to several lattice points; a
    tie-break rule must be G-equivariant too. The boundary classes have nontrivial... hmm, boundary ties: if x is
    equidistant from 0 and W l, then... tie-breaking equivariantly is possible iff the G-action on the tie set is
    free on ... again set-theoretically fine for gcd(W,6)=1 by the freeness argument above. But "free of search":
    nearest-point in an 8-dim lattice is a CVP; for Lambda (= 2 copies of D4-like? Lambda real = H(x)Q(sqrt2)...
    actually Lambda as a Z-lattice with the trace form is E8! The ring Z[sqrt2] 2O... hmm, the icosians give E8 with
    Z[golden]; the Z[sqrt2]-order 2O ... Lambda with the form Tr_{Q(sqrt2)/Q}(N(x) * something) — is it E8? The
    "octahedral" order: 2O over Z[sqrt2] is a maximal order of the quaternion algebra over Q(sqrt2) ramified at the two
    infinite places; its discriminant... the lattice with form Tr((2 - sqrt2) N(x))? gives E8? Not sure. Not needed.)
    CVP in E8 has a fast exact algorithm (Conway-Sloane) but it's a search with comparisons. For a "formula" without
    if/comparison: the per-gear carry itself is floor division = Rule3's carry, which is "one division". A
    G-equivariant division on 8 gears at once can't be coordinate-wise floor since floor's box isn't G-stable.
    Can a bijective equivariant remainder be written as a composition of per-gear carries in several bases? e.g.
    remainder = carry in basis B1 then carry in basis B2... each is equivariant under its own signed-perm group; the
    composition is equivariant under the intersection. No.
    THEOREM candidate (the wall, provable): For W with gcd(W, 6) > 1 (in particular W even or W = 9), there is NO
    map rho: Lambda -> Lambda with rho(x) = x mod W Lambda and rho(g x) = g rho(x) for all g in the 48, period. Proof
    above via fixed classes. For gcd(W,6)=1 such maps exist (choice per orbit) but a canonical one needs a rule.
    Also for W = 1 trivial. And the SAME argument for the per-gear carry with the 24 acting on a whole-speed kind:
    the 24 act on Z^n by signed permutations; does the per-gear box [0,W)^n give an equivariant remainder? Under a
    sign flip x -> -x the box [0,W) is not stable; the "tooth flip" convention r -> W-1-r is how the engine handles
    negated rows (a different remainder convention per sign). So even for whole-speed kinds the carry is equivariant
    only up to the flip, which the text calls "the sign law". With the flip, the remainder domain is [0,W) and the
    map r -> W-1-r is the reflection of the box: that works because for a signed permutation each coordinate is
    independently negated. OK.
    Importantly: the fixed-class obstruction also applies to the 24 acting on whole-speed kinds: e.g. the sign flip
    -1 on a row... but the 24 don't contain -I on all kinds; for E, the 24 contain elements with fixed classes mod W
    and eigenvalue... For a signed permutation g, fixed vectors exist (e.g. for a permutation fixing a coordinate),
    and the box [0,W)^n representative is g-fixed if g permutes coordinates with the same remainders: fine. The
    obstruction bites when g fixes a class but no vector in the class: e.g. g = -1 on a coordinate at W even: the
    class W/2 on that coordinate is fixed by negation but no representative is: the engine's flip handles it by
    changing the remainder convention (r -> W-1-r), i.e. the engine's turned state is NOT the same state but the
    "flipped" one: that is exactly a failure of strict equivariance, repaired by the convention that a negated row
    carries the mirror remainder. So the sign law is itself an admission that the carry is not equivariant under
    negation; it's equivariant under negation composed with the flip of r. For a mixing matrix no such repair
    exists since remainders are per-gear.
    So for the 48 on 8 gears at W=9: impossible, and the reason is not "search" but a fixed-point obstruction. The
    text's "what would carry them is a carry whose remainders fill a domain the 48 keep, on Lambda the nearest
    point of W Lambda, eight gears at once: a search" — the nearest point of 9 Lambda: the Voronoi cell IS 48-stable,
    but the boundary ties kill equivariance at W=9? Not exactly: the Voronoi boundary tie set might be avoided if
    no lattice point of Lambda lies on the boundary of the Voronoi cell of 9 Lambda... Points of Lambda on the
    boundary of Vor(9Lambda) are those equidistant from 0 and some 9 l: |x|^2 = |x - 9l|^2 => 18 <x,l> = 81 |l|^2 =>
    2<x,l> = 9|l|^2 => <x,l> = 9|l|^2/2 which needs |l|^2 even... with the right inner product on Lambda (what IS the
    inner product? The G-invariant ones: 2 symmetric pairings! There are 2 invariant symmetric forms, one per Galois
    copy, so no canonical "nearest". The isometry group is what matters: G keeps both. Choose the sum, the trace
    form.) The fixed-class argument is airtight regardless: a 9-fixed class of an order-3 element exists (because
    N(g-1) = 3 shares a factor with 9) and has no g-fixed representative. So NO equivariant remainder at W = 9 of any
    kind. For the actual standing W: check what W the engine uses (W = 9 in SYM24's probes; the text says "W
    standing at 9").
    Also check the same obstruction for the Hurwitz order and the 24 (2T) acting: the units of order 3 and 6 have
    N(g-1) = 3 and 1; order 4: N(g-1) = 2; -1: 4. So for W divisible by 2 or 3, no 2T-equivariant remainder on
    Hurwitz quaternions. For gcd(W,6)=1, free action on nonzero classes mod W, so exists set-theoretically.
    This is a clean theorem to report. Also: "free of search, if and comparison": a per-gear carry is a formula
    (floor). An equivariant rho for gcd(W,6)=1: could there be a formula? Since G acts freely on (Lambda/W)\0, the
    orbits have 48 elements each, and |Lambda/W| - 1 = W^8 - 1 must be divisible by 48 for a G-stable D to be
    possible — wait, that's automatic given freeness: W^8 - 1 = (W^4-1)(W^4+1); for W coprime to 6, W^2 = 1 mod 24,
    so W^4 - 1 = (W^2-1)(W^2+1) divisible by 24*2 = 48. Good, consistent (W odd: W^2 = 1 mod 8, W coprime to 3:
    W^2 = 1 mod 3, so W^2 = 1 mod 24; W^4 + 1 is even; so 48 | W^8 - 1). Consistent with freeness.
12. The claim "at W = 1 all 48 hold": at W = 1 carry(n, 1, r) = (n + r, 0): q = n + r, r' = 0: linear. Fine.
13. Check "the quarter turn's lift to the fourth is -I": a quarter turn lift q = (1+k)/sqrt2 has order 8 in the
    group; q^4 = -1. Yes.
14. "(trace, order): (0, 4) 18, (0, 8) 12": elements of order 4 in 2O: the lifts of half turns: 6 face half-turns
    (order 2 in O) lift to order 4 (trace 0), 2 lifts each = 12; the 6 edge half-turns lift to order 4 too, 2 each =
    12; total order-4 elements in 2O = 24? Hmm, but they say (0,4) 18 and (0,8) 12. Let's count 2O (order 48):
    classes: 1 (1), -1 (1), order 4 lifting face half-turns: these are +-i, +-j, +-k: 6 elements; order 8 (quarter
    turn lifts): 12 elements (6 quarter turns x 2 lifts); order 3: 8; order 6: 8; order 4 lifting edge half-turns:
    12 elements (6 edge half turns x 2) with trace 0 (they are (i+j)/sqrt2 etc.) Total: 1+1+6+12+8+8+12 = 48. Order
    4 elements: 6 + 12 = 18. Yes (0,4): 18. (0, 8): 12. Good. The quarter-turn lifts have Re q = +-1/sqrt2 so
    trace in E1/2 is +-sqrt2 and in the 8-dim rational rep: 2(sqrt2 + (-sqrt2)) = 0. Good.
15. The 384 signed permutations table and cycle-type table: fine.
16. Check kinds.py to see how the 24 and the kinds are built; check contract.py, step.py for the carry per gear and
    the "tooth flip".

## Files to read next
- probe_kinds.py/.txt, probe_act.py/.txt, probe_pair.py/.txt
- t24b/src/tensor24/engine/kinds.py, step.py, contract.py, algebra/carry.py, runner/files.py, runner/load.py
- t24b/docs/ALGEBRA.md lines 80-110, 340-350, 450-465
- sym24_v2/common.py (the probes' harness) and SYM24.md (the lemma)

## Rerun of the five probes (16:00)
All five rerun with the worktree's .venv/bin/python -I -B into fam_math/rerun/: outputs byte-identical to the
families' .txt files (probe_kinds, probe_48, probe_spinor, probe_act, probe_pair). Reproducible.

## Plan of my own probes (fam_math/)
- zlin.py: whole-number linear algebra (echelon, coordinates, Bareiss, Smith diagonal, nullspace), carry only.
- p1_cover.py: 2O rebuilt as 2x2 matrices over Z[zeta_8] (not their Z[sqrt2] quaternions); covering onto my own 24;
  FS sums; Lambda as a Z-lattice of rank 8 (echelon basis); the 48 as 8x8 whole matrices; traces/orders; FS; the
  invariant forms counted two ways; cycle types of signed permutations of 8 and 4 gears; the fixed-class theorem for
  an equivariant remainder (Smith diagonals of M_g - I, kernel sizes mod W); Hurwitz / 2T the same.
- p2_induced.py: every subgroup H of 2O and sign character; the induced signed-permutation representations; which
  contain E1/2, E5/2, G3/2 with -1 -> -I. EXPECT: Ind_{C6}(lambda) on 8 gears = 2 G3/2 (Kramers, monomial!), and
  Ind_{C2}(sgn) on 24 gears containing E1/2 twice. Build the 8-gear one explicitly, verify, commutant, Kramers T.
- p3_act.py: the 8-gear G3/2 monomial form on the real act (sym24_v2/common harness), W = 9, 10, 1: 48 of 48?
  Plus the control: random signed permutations (no homomorphism) also hold at J = 0 -> the act test is only the
  carry lemma.
- p4_lemma.py: the carry lemma exhaustively for 2 gears, W = 2, 3, every integer P in [-2, 2]^(2x2), every bijection
  of the remainder box: only signed permutations with the flip commute.
