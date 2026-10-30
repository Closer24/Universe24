# The families' exchange rule: symmetric and antisymmetric clocks, and Pauli in the clicks (the first text)

The deriver of the families (the Boss's agent), 2026-10-30, for the Boss and, after him, two hostile readers, a
mathematician and a physicist, each new to it. It answers the owner's question of today ("a rule on the families,
something algebraic, or a symmetry in the families; maybe only one family is not symmetric ... that is what makes
Pauli"), read in clocks as he asked ("In the clicks, think clocks, do not think quantum: clocks, hands, chains ...
clocks connect and come apart, and the aim of the system is that clocks connect; that is what clicks show"), and Big
Pic's two pieces (#2187 6526201692) as candidates to test, under the owner's word that line 90's five kinds may be
widened to the 24's double cover where the derivation needs it ("Expand it if needed, no problem"). Five probes stand
beside it, all in whole numbers with the engine's own carry as their one division, on the engine's own kinds, tables
and act (t24b, main 9067de20d): `probe_kinds.py`, `probe_48.py`, `probe_spinor.py`, `probe_act.py`, `probe_pair.py`,
each with its output beside it (`.txt`). Run each with the worktree's `.venv/bin/python -I`. Every number below is
theirs unless a line of the law or of the code is cited. No engine code and nothing in any worktree was written.

Status on the ladder: DRAFTED. The clock layer, the algebra and the clicks are written and the probes run; no reader
has read it. Where it says what fails, it fails on the act as built, measured.

## The rule, in one sentence

A family's two clocks pair as its kind pairs: the exchange sign of a family is the sign of its kind's own pairing, the
one bilinear pairing of two hands of one sense that every turn keeps, and that sign is the kind's sign under one full
turn of the board, +1 for a whole-speed kind and -1 for a half-speed one, by the belt: swapping two clocks of one family
is one full turn of one of them. On the five kinds of the 24 the sign is +1 on all five, so every family of Tensor24
today is symmetric: its clocks stack and crowd, and no family is antisymmetric and none is handed. The three half-speed
kinds of the 48 (E1/2 and E5/2, one whole kind of eight gears; G3/2) carry -1: two of their clocks in one state have no
pair hand, two at one place turn in opposite senses, and a third has no room: Pauli in clocks. They stand in whole
numbers, as Big Pic said; the act as built carries them bit for bit only at W = 1, or for one axis's eight turns at any
W, by the carry's own lemma (what fails), and a pair click on them does not close the books (what fails too).

## Clock

- A family is a kind of clock. Its kind says how its hands turn with the board (the cube's turns swap them and reverse
  some); its part says how many planes it has (part 2 a Gaussian hand, re and im). A whole-speed clock returns to itself
  under one full turn of the board; a half-speed clock comes back at minus itself and needs two full turns.
- Two clocks of one family at one Node-clock can pair in two ways, and both are whole: in step, the dot of their hands
  through the A1 table, which stacks two swings into one clock (symmetric in the two clocks); and in quadrature, the
  turn of one hand against the other, the wedge of a Gaussian hand's two parts, which is term 11's area moved (what one
  gives the other takes: antisymmetric in the two clocks, the books). The second is the click's pairing and not an
  exchange sign: it pairs a hand with a counter-turning hand (a quantum against its antiquantum, charge 0), and it is odd
  under the conjugation of the hand (the sense of its turn) as well as under the swap.
- The exchange asks how two clocks of one family turning the same way connect at one Node-clock: whether they stack into
  one clock of a bigger swing (symmetric, they connect and crowd) or cannot connect into one state (antisymmetric,
  Pauli). The pairing that decides it is the one of two hands of one sense, the bilinear pairing of the kind (charge 2),
  not the Hermitian one of the click.
- Whole-speed clocks (the five kinds, every family the files hold today): two such clocks of one state are one clock of a
  bigger swing. On the act a taker takes seven keys of area into one hand, one key after another, its energy growing
  with its count; two keys laid in the giver land in the taker's one hand; a vector family's keys all land in the
  giver's own component. This is the same for A1, A2, T1 and T2: the act knows no kind through the dot, and crowding is
  every family's (probe_act 1, 2).
- Half-speed clocks (the double cover's three kinds): one full turn of the board is -1 on the hand, so by the belt the
  pair of two such clocks carries the swap's minus; two of them in one state have no pair hand at all (its size is 0,
  exactly); a clock and its partner, the hand run the other way with its two Gaussian pairs exchanged and one negated,
  turn in opposite senses and have the pair hand N(phi); a third clock is a Z[zeta_8]-combination of those two and has no
  room (probe_pair 1, 2). That is Pauli said in clocks: two half-speed clocks connect at one place only up and down,
  never alike, and never three.
- On the board as built there is no half-speed clock: every kind of line 90 is whole-speed. A half-speed hand of eight
  gears rides the carry for the eight turns about one axis (its Gaussian basis makes those sixteen lifts signed
  permutations of its gears) and departs on the rest at any W of 2 or more; at W = 1, where the carry is linear, it
  rides all 48. The run back is exact on it in every case, and four quarter turns of the board send it to minus itself
  bit for bit, each tooth flipped in its teeth, eight bring it back (probe_spinor 6).
- The metric family (part 1) has no second part and sweeps no area: term 11 never clicks it; its symmetry flag is the
  symmetric square of the four-vector, a symmetry of its ten slots' indices (probe_kinds 4), not of its quanta. Light's
  tensor form, the antisymmetric square T1 + T1 (six slots), the files would accept as kinds [T1, T1] and flag nothing;
  both are whole-speed, both symmetric under exchange.

## Board

- **The kinds' own pairings** (probe_kinds 2, 3). On the engine's own 24, kinds and tables (kinds.turns, kinds.kinds,
  load.tables, nothing typed): the Frobenius-Schur sum SUM_g chi(g g) over the 24 is +24 on each of A1, A2, E, T1, T2,
  so each kind's own pairing is symmetric; the swap sign of every channel K x K -> m of load.tables: the A1 channel (the
  dot) is symmetric for all five; the antisymmetric channels are E x E -> A2, T1 x T1 -> T1 (the epsilon table) and
  T2 x T2 -> T1, and none lands in A1. By characters, Alt^2 E = A2, Alt^2 T1 = Alt^2 T2 = T1, Alt^2 A1 = Alt^2 A2 = 0;
  the four-vector's Sym^2 is 2 A1 + E + T1 + T2 (the loader's square character on all 24 turns, exactly) and its Alt^2
  is 2 T1.
- **The one odd character** (probe_kinds 5): A2, +1 on the tetrahedron's 12 (closed under products) and -1 on the
  other 12; A2 x T1 = T2, A2 x E = E, A2 x A1 = A2. It is odd under the cube's own quarter turns and edge half turns,
  not under a reflection: under the 24 no kind carries a parity label (SYM24). A family of kind A2 or T2 is not handed.
- **The Gaussian hand's two pairings** (probe_kinds 6): a kind at part 2 keeps four pairings under the 24 (three
  symmetric, one antisymmetric), and under its own quarter turn (re, im) -> (-im, re) two: the dot (symmetric, even
  under conjugation) and the wedge (antisymmetric, odd under conjugation). The wedge of a hand with its kick is term 11's
  tau, with tau_M = -tau_L (TERM11, the common turn). The part changes no exchange sign.
- **The helicity** (probe_kinds 7, Big Pic's handed click): a vector hand at part 2 affords two whole readings with a
  gradient p: the winding w = SUM_i (re_i p'_im,i - im_i p'_re,i), kept by all 48 (even under every reflection), and
  h = (re x im) . p through the epsilon table, kept by the 24 turns and negated by all 24 reflections (the parts polar).
  A click that reads the winding (term 11) is achiral; a click that read one helicity would be handed on an achiral
  board; which sign a reflection gives depends on the lift (polar or axial) that no kind carries, the plan's at G3.
  Named as a candidate for G5, not derived; h is 0 wherever re and im are parallel (a hand on a line, or turning in
  one component alone, as every lay in probe_act does).
- **The half-speed gear in whole numbers** (probe_48, probe_spinor; Big Pic's piece 1):
  - the 48 turns of spin, closed in Z[sqrt 2] (integer pairs p + q sqrt 2) from the lifts of two of the engine's own
    turns, cover the engine's 24 two to one, -1 among them; the spinor's character 2 Re q is whole on the 24 lifts of
    the even 12 and 0 or +-sqrt 2 on the 24 lifts of the odd 12: the twelve lifts of the six quarter turns have an
    irrational trace, so on two gears, on four, or on any 2 n with the character alone, the quarter turns have no whole
    spinor; SUM chi(g g) = -48, Frobenius-Schur -1 (Kramers): the own pairing antisymmetric (probe_48 1);
  - the order Lambda = Z[sqrt 2] 2O, the 48's own ring, is a lattice of rank 8 (a Hermite basis in integers), and the
    48 act on it by left multiplication as whole 8 x 8 matrices of determinant 1, M(s) M(t) = M(s t) on 2,304 of 2,304
    pairs, -1 the matrix -I; the quarter turn's lift to the fourth is -I and to the eighth I, the third turn's lift
    cubed -I; SUM trace(M M) = -192 = -4 x 48; the lattice keeps 8 pairings, 2 symmetric and 6 antisymmetric
    (probe_spinor 1, 2);
  - Lambda is Z[zeta_8] + w Z[zeta_8] on the right, w = (1 + i + j + k) / 2, each contains the other's spanning set: a
    hand of Lambda is a pair of Z[zeta_8] numbers, four whole numbers each, a + c i + zeta (b + d i), a pair of Gaussian
    pairs, exactly as Big Pic said; the hand's own phase, its winding, is right multiplication by zeta^k, which
    commutes with the 48 on the left; the 48 are 2 x 2 matrices over Z[zeta_8] there, every entry whole, monomial on
    4 of 48 (probe_spinor 3);
  - E1/2 and E5/2 are one whole kind of eight gears (the quarter turns' lifts trace 0 = sqrt 2 - sqrt 2; the
    complexification 2 E1/2 + 2 E5/2); G3/2 = E1/2 x E stands on sixteen gears (four copies of its least whole form of
    eight), a representation with -1 at -I, every trace whole, SUM trace(M M) = -192 (probe_spinor 5);
  - the Gaussian basis (1, j) Z[zeta_8], the hand z1 + j z2: sixteen lifts map it to itself, all signed permutations of
    the eight gears, covering the eight turns that fix the x axis up to sign (zeta = (1 + i) / sqrt 2 is the quarter
    turn about x); the other 32 send such a hand to halves. Each axis has such a basis; no basis serves two axes
    (probe_spinor 4);
  - by cycle types, no signed permutation of eight gears has (trace, order) = (4, 6) or (-4, 3), the third turns'
    lifts; and no signed permutation of four gears has (2, 6) or (-2, 3), the Hurwitz lift's: the Kramers lift of the
    even 12 is whole in a mixing basis (the Hurwitz units on 1, i, j, w: 24 whole matrices of determinant 1) and a
    signed permutation in none (probe_48 2, probe_spinor 2). The one double cover of the even 12 by signed permutations
    of four gears (Q8 and the cyclic turn of i, j, k) is a complex kind, Frobenius-Schur 0, with one dot and one winding
    like a Gaussian hand and no pairing of its own (probe_48 3).
- **On the act as built** (SYM24's cube of side 3, the eight gears a train of kind A1 at part 8 beside the square, W
  standing; probe_spinor 6; probe_48 4): at W = 1 every lift holds (the carry is linear, q = n); at W = 9 the 46 mixing
  lifts of the lattice basis depart on 46 of 46 over 6 rounds, +-I hold with the tooth flip, the Gaussian basis's 16
  hold on 16 of 16, the run back by the act alone returns the start bit for bit. The same at W = 9 for the Hurwitz lift
  on four gears: 22 of 22 mixing depart, +-1 hold. The reason is SYM24's lemma for E, which these probes extend: the
  per-gear carry commutes with signed permutations alone (SYM24, the sign law), and a half-speed kind is monomial in no
  basis for more than one axis.
- **Two copies at one Node-clock** (probe_pair 3; TERM11's world, the vertex g = f / 10 through the dot, both copies
  tied alike to the giver): whole-speed, the copies' gears stay alike in 3,001 of 3,001 states, the symmetric pair hand
  J_+ is not 0 in 3,000 of 3,000 rounds and J_- is 0 in all: the pair bunches, one state, one hand of double size, each
  copy's count by term 11 from 0 to 4 and the giver's from 0 to -7. Half-speed (eight gears each): the copies alike in
  3,001 of 3,001, J_- and det(copy 1, copy 2) 0 in every state, so a pair click reading the pair's hand counts 0 for
  ever, yet each copy's own winding climbs from 0 to 4 keys while the giver gives 7: on the act as built the gears
  gather what the pair's hand does not hold, and the books of keys between the giver and the pair do not close. The
  partner pair (phi, T phi) run free, copy 2's teeth laid at W - 1 on the four rows T negates (the sign law): copy 2
  stays T of copy 1 in both slots in 600 of 600 rounds, <copy 1, copy 2> = 0 in 600, det not 0 in 600, the windings
  opposite in 600: two at one place in opposite senses keep their pair's hand, since the act commutes with T, a signed
  permutation of the gears.

## Clicks

- **What a click of a whole-speed family shows** (term 11 as drafted, TERM11): one key of area taken (+1) or given back
  (-1), the net winding of the train's two parts, the books closing between a giver and a taker in every round. Of two
  clocks of one family at one Node-clock it shows crowding: the count climbs 0, 1, 2, ... 7 with no refusal, in the same
  numbers for A1, A2, T1 and T2 (probe_act 1); the taker's energy at its second click is 2,948 thousandths of its
  energy at the first (the births at half a key: the areas 1/2 and 3/2 of a key, one clock of a bigger swing). Light's
  clicks bunch, as nature's do; the metric family never clicks by term 11 (no second part); no click of any family
  today reads an exclusion, and none should: the act has none (what the law says of Rule3's step at line 458 stands).
- **What a click of a half-speed family would show** (the candidate, in clocks): the family's click reads two of its
  clocks at one Node-clock as one joint hand, J = phi x chi - chi x phi, the two orders entering with the swap's sign,
  which the belt fixes at -1 for a hand that one full turn negates. In one state (one place, one sense of turn) the
  joint hand is 0 exactly and nothing is ever clicked; a clock and its partner (opposite senses) have the joint hand
  N(phi) and click; a third clock has no state and no click. Nothing is banned in the click: the sign is the family's,
  read off its full turn. This is David's law of the pair (DAVID-TENSOR24-PAULI.md, 2026-10-28, on the old engine's
  twins) derived again on Tensor24's own 48 in whole numbers, with the belt in place of the pairing's computation: the
  two agree, since the pairing's sign is the Frobenius-Schur sign and that is the full turn's.
- **What fails in the clicks on the act as built** (probe_pair 3): the pair click and term 11's click disagree on the
  half-speed pair in one state. The pair's hand is empty in every round (never clicked) while each copy's winding fills
  (clicked by term 11), and the giver's seven keys are then counted by no pair click: the books of keys break. Pauli on
  the act needs the act itself to move area only into a pair hand that is not 0, which the linear act with the vertex
  through the dot does not do; the law's line 458 ("the step excludes nothing and must not, Rule3 being linear") holds
  on Tensor24's act as on the old one, and David's finding that "the step does not keep the cap" (his section The bound
  between clicks) holds here too.
- **The handed click**: the one reflection-odd whole reading a family of the five kinds affords is the helicity of a
  vector hand, (re x im) . p (probe_kinds 7), odd under all 24 reflections with the parts polar; term 11 reads the
  winding, which is even. A click reading one helicity would make the clicks handed on an achiral board (SYM24: the 48
  hold at standing W), which is where nature's parity breaks (Wu 1957; the law's line 344). It is a candidate for G5,
  not derived; which lift the plan fixes at G3 decides whether the helicity is odd at all (SYM24, Board, the one door).
- **The blockade, a strength and not a rule** (probe_act 5): a hairspring that stiffens with the swing, the taker's own
  four-leg term lambda (T . T)^2 (a monomial the plan allows), caps the taker's count 7, 7, 5, 3, 2, 1, 0 as lambda runs
  0, 10^3, 10^4, 3 x 10^4, 10^5, 3 x 10^5, 10^6, 10^7, with the same rows for A1 and T1: a clock that holds one key beats
  off the giver's beat and the second key does not connect. It is a window of lambda, CHOSEN, blind to the kind, and
  never exact: not Pauli. The declared refusal (the vertex cut outside the act wherever the taker holds one key) holds
  the count at 1 trivially (probe_act 4) and is the fake the owner forbade (line 35, 2026-10-29).

## Algebra

- **The joint hand and the belt** (probe_pair 1). For hands phi, chi of one kind let J_e = phi x chi + e chi x phi. The
  swap S J = J^T gives S J_e = e J_e for either e. One full turn of one clock gives R J_e = sigma J_e, sigma the kind's
  sign under a full turn (+1 on the 24's kinds, since their turns are the 24 themselves and a full turn is the identity;
  -1 on a half-speed kind, where (the quarter turn's lift)^4 = -I). The belt law, S = R on a pair hand that is not 0,
  holds for e = sigma and for no other: measured on every kind with whole hands, [1] for A1, A2, E, T1, T2 and [-1] for
  the eight-gear kind (a kind of one row has J_- = 0 identically, so its pair hand is J_+ alone). The pair in one state
  J_sigma(phi, phi) has size 4 N(phi)^2 for sigma = +1 (bunching) and 0 for sigma = -1 (no hand).
- **The sign is the kind's own pairing's** (probe_kinds 2, 3; probe_48 1; probe_spinor 2). For a real kind the
  invariant bilinear pairing into A1 is unique (Schur) and its swap sign is the Frobenius-Schur sum SUM_g chi(g g) / |G|,
  +1 on the five kinds of the 24 (the A1 tables of load.tables are symmetric on all five) and -1 on the 48's three
  half-speed kinds (-48 on the spinor, -192 = -4 x 48 on the eight-gear lattice and on the sixteen-gear G3/2). The
  Frobenius-Schur sign is the full turn's sign on these groups (a true kind of the 24 is +1 both ways; a faithful kind of
  the 48 is quaternionic, -1 both ways), so the belt and the pairing give one rule. A complex kind (Frobenius-Schur 0,
  the signed-permutation double cover of the even 12) has no pairing of its own; there the belt alone fixes e = -1.
- **The two pairings of a half-speed hand, in whole numbers** (probe_pair 2). On Lambda in the Gaussian basis, for
  x = z1 + j z2 and y, conj(x) y = <x, y> + j det(x, y): <,> the Hermitian pairing (<chi, phi> = conj <phi, chi>, kept
  when both hands turn by their own i: charge 0), det the determinant (det(chi, phi) = -det(phi, chi), times i^2 = -1
  when both turn by i: charge 2). det(phi, phi) = 0 and <phi, phi> = N(phi) > 0 on 20 of 20 hands. The partner
  T phi = (-conj z2, conj z1), a signed permutation of the eight gears: T T = -1, <phi, T phi> = 0 (Kramers),
  det(phi, T phi) = N(phi), the partner's winding minus the hand's, on 20 of 20. A third hand:
  phi det(chi, psi) + chi det(psi, phi) + psi det(phi, chi) = 0 and N(phi) psi = phi <phi, psi> + T phi <T phi, psi>
  on 20 of 20: three hands of a two-dimensional kind are never independent.
- **Whole numbers hold the half-speed gear** (probe_spinor 1 to 5): sqrt 2 = zeta - zeta^3 is whole in Z[zeta_8],
  Lambda is a free Z[zeta_8]-module of rank 2 (every ideal principal), and the 48 are whole and unimodular on it. Big
  Pic's correction stands and the law's line 346 ("the spinor's character is irrational, and no train of gears turning
  by signed permutations carries spin 1/2, only Q8 lifting in integers") stands with it: whole, but not by signed
  permutations.
- **The carry's lemma** (SYM24, Algebra, E has no whole basis; here measured on eight and on four gears). If a row of the
  turned train sums two rows, lay n1 + r1 = n2 + r2 = W - 1 with r1 = r2 = 0: the needed quotient is 0 and the turned
  carry gives at least 1 for every tooth in [0, W); so at W >= 2 the act turns only with signed permutations (with the
  tooth flip on a negated row, the sign law), and a half-speed kind is a signed permutation in no basis for more than one
  axis's eight turns (the cycle types). At W = 1 the carry is linear and every whole matrix commutes with it.
- **Crowding** (probe_act): the act is linear in its gears through the vertex, so two hands of one family driven alike
  stay alike, and a hand's area grows with the square of its swing; n keys fit in one hand for every n the giver holds
  (7 of 7), the quotient of the click tooth counting them one by one with |q_c| <= 1 a round at this key.

## Measured

1. `probe_kinds.py`: 216 candidates, the 24 kept, 576 of 576 products among them; Frobenius-Schur +1 on all five kinds
   (+5 on the square); the swap signs of all channels (A1 + for all five; E x E -> A2 -, T1 x T1 -> T1 -, T2 x T2 -> T1
   -); the squares by characters; the loader's square character = the four-vector's Sym^2 on all 24; A2 12/12, the +1
   half closed; a Gaussian hand of A1 and of T1: 4 pairings under the 24 (3 + 1), 2 under its own turn (the dot +, the
   wedge -; the wedge odd under conjugation); the winding kept by 48 of 48 signed permutations, the helicity kept by the
   24 turns and negated by the 24 reflections.
2. `probe_48.py`: the 48 closed from two lifts, 24 turns covered two to one, -1 among them; the spinor characters whole
   on the even lifts and 0 or +-sqrt 2 on the odd ones, 12 irrational; SUM chi(g g) = -48, SUM chi^2 = 48; on four real
   gears 4 pairings, 1 symmetric and 3 antisymmetric; the Hurwitz units as 24 whole 4 x 4 matrices of determinant 1,
   closed, 2 signed permutations, SUM trace(M M) = -48, (trace, order) in {(-4, 2), (-2, 3), (0, 4), (2, 6), (4, 1)}
   against the 384 signed permutations' table, (-2, 3) and (2, 6) missing; the signed-permutation double cover of the
   even 12: 24 elements, -1 among them, the map to the even 12 one-valued with kernel +-1, SUM trace(M M) = 0, 2
   pairings (1 + 1); on the act at W = 1 and 9 the 24 signed permutations hold 24 of 24; the Hurwitz lift's 22 mixing
   matrices depart 0 of 22 at W = 1 and 22 of 22 at W = 9, +-1 hold 2 of 2.
3. `probe_spinor.py`: Lambda rank 8, the 48 in it, a ring; the 48 as whole 8 x 8 matrices of determinant 1, a
   representation on 2,304 of 2,304 pairs, -1 = -I; (trace, order): (8, 1) 1, (-8, 2) 1, (0, 4) 18, (0, 8) 12, (4, 6) 8,
   (-4, 3) 8; the quarter lift^4 = -I, ^8 = I, the third lift^3 = -I; SUM trace(M M) = -192, 8 pairings (2 + 6); 2
   signed permutations; (4, 6) and (-4, 3) in no cycle type of eight gears; Lambda = Z[zeta_8] + w Z[zeta_8]; the 48 as
   2 x 2 over Z[zeta_8], monomial on 4; the Gaussian basis: 16 lifts whole, all signed permutations, the x axis's
   dihedral eight; G3/2 on sixteen gears, traces in {-16, -4, 0, 4, 16}, SUM trace(M M) = -192, 16 pairings (6 + 10); on
   the act: W = 1 all hold, the run back exact; W = 9 the 46 mixing depart 46 of 46, +-I hold 2 of 2, the Gaussian 16
   hold 16 of 16, the run back exact; four quarter turns -I, eight +I.
4. `probe_act.py`: a giver and a taker of A1, A2, T1, T2 at part 2, the key a seventh of the giver's area made odd
   (714285714285714285714285714285), 3,000 rounds: the count 0 to 7 (1 at round 218, 2 at round 385), the area at its
   most 7,004 thousandths of a key, the books miss 0 of 3,000, no |q_c| >= 2, the energy ratio 2,948 thousandths, every
   key in the giver's component (T1, T2); two keys laid (the key 2500000000000000000000000000001): the count 0 to 2, 2
   at round 838; mirror twice the identity on all four kinds; the declared refusal: the count 0 to 1, the vertex cut in
   2,782 of 3,000 rounds; the blockade rows above, A1 and T1 alike.
5. `probe_pair.py`: the belt picks [1] for the five kinds and [-1] for the eight-gear kind and the complex spinor; the
   pair in one state 4 N^2 (5,184; 8,100; 63,504) or 0; the spinor's pairings on 20 hands and pairs as in Algebra; on
   the act: the whole-speed copies alike 3,001 of 3,001, J_+ not 0 in 3,000, counts 0 to 4 each, the giver -7; the
   half-speed copies alike 3,001 of 3,001, J_- and det 0 in all, counts 0 to 4 each, the giver -7; the partner pair 600
   of 600 in both slots, Kramers 600, det not 0 600, windings opposite 600.

## Where it stands

| claim | holds | fails |
| --- | --- | --- |
| one algebraic rule: the exchange sign is the kind's own pairing's sign, the full turn's sign, the belt | on the engine's kinds and tables and on the 48 in whole numbers | nothing |
| every family of the five kinds symmetric; none antisymmetric; none handed | yes (probe_kinds, probe_act) | the owner's "maybe only one family is not symmetric": none among the five; the odd character A2 is not a parity |
| the Gaussian hand's i gives an exchange sign | no: it gives the winding, the click's pairing (charge 0) | |
| whole numbers hold the half-speed gear (Big Pic's correction) | Lambda, the 48 whole and unimodular, Z[zeta_8]^2, four whole numbers per part | the law's line 346 is right that no signed permutations do |
| the 24 as the 48, bit for bit, on the act | at W = 1; one axis's eight turns at any W; the run back exact; a full turn -1, two +1 | at W >= 2 the other 40 lifts depart, by the carry's lemma; no basis mends it |
| Pauli in the clicks by the pair's hand | the algebra, exactly, in whole numbers (one state 0, partners N, no third) | on the act the pair's hand stays empty while the copies fill: the books of keys break |
| the handed family | a candidate click, (re x im) . p, odd under reflections | no family is handed on the board; the lift is the plan's |
| the owner's "that is what makes Pauli" | yes: the one family kind that is antisymmetric is the half-speed one, and Pauli is its pair's | no such family rides Tensor24's act today |

## The law's lines it touches, quoted

- Line 90: "a train is a tensor whose kind is a way the cube's 24 turns exchange and reflect its dials (five kinds, the
  scalar, the pseudoscalar, E, the vector and the shear, derived from the lattice's axes), and the contraction of two
  kinds is fixed by the group's product table". This is the line Big Pic names, and the one the owner may widen: the 24
  to the 48 of spin, the five kinds to eight, three of them half-speed. The same line's "one division with a carried
  remainder over one integer contraction" is the wall: the per-gear carry turns with signed permutations alone.
- Line 346: "the spinor's character is irrational, and no train of gears turning by signed permutations carries spin
  1/2, only Q8 lifting in integers" and SP-S2 "struck ... the owner's word 'close it'": stands, read exactly: whole in
  a mixing basis (probe_spinor), by signed permutations never beyond one axis.
- Line 458: "Pauli's exclusion has no line of Rule3's step ... the step excludes nothing and must not, Rule3 being
  linear and D even in a gear's sign; no key, no weight, no act": stands on Tensor24's act (probe_act 1, probe_pair 3).
- Line 559: "Pauli by The click law, a premise by name (the exchange key a departure)" and "the cube's whole double
  cover needs eight gears, the struck train; one level up, the exchange sign and spin one half as one declaration,
  matter carried as doublets and light a plane": the eight gears confirmed; the one declaration replaced by the belt
  law, one sentence for every family, the sign read off the kind.
- Line 1562: the owner's words of 2026-10-27 ("the matter family is antisymmetric, and all the non-matter families, like
  light, are symmetric; they can be in the same state in the clicks"; "matter is symmetric and force carriers are not,
  and that brings Pauli; on the board it is something else, with the phase, and in the clicks something else"), "Rule3's
  one line carries no spin one half of its own, derived", "under the 48 real gears carry integer spin alone (spinor
  multiplicity 0)" and "the train's sign under exchange declared": the sign is now derived, not declared; the board's
  "something else, with the phase" is the half-speed hand's -1 under a full turn and its partner's opposite sense; the
  clicks' is the pair's hand.
- Line 1558: "saturation in nature being Pauli's exclusion and the hard core, which the law lacks": the lack stands on
  the act; the blockade (probe_act 5) is a hard core by a strength, not a law.
- Line 94: "The reflections are not asked, so the great clock may be chiral."; line 344: "it conserves parity, since
  Rule3 commutes with the cube's 48, the reflections included, so no hand of the law has a handedness, where nature
  violates it maximally (Wu 1957, the V minus A structure)"; line 1696: "the 48 symmetries with the reflections, so
  parity is kept, no handedness, a finding by name against nature (Wu 1957)": SYM24's disagreement between 94 and the
  other two stands; this text adds that the only reflection-odd whole reading of a vector hand is its helicity, and
  the winding term 11 reads is even.
- Line 100: "a gear's teeth count may be even or odd, and no act and no line of this law may lean on its parity": the
  key's oddness (TERM11) and the centred tooth (SYM24) lean on it; nothing here does.
- Line 102: "no rotation by a setting applied outside Rule3 (a quaternion or a Gaussian turn chosen by a detector's
  setting)": the 48 here are the board's own turns, derived from the star, chosen by no setting.
- Line 35, the owner's words of 2026-10-29: "all the exclusions and restrictions ruin it for us, because then the generic
  law cannot be reached ... The node is a generic and simple node": the declared refusal of probe_act 4 is such a fake;
  the belt law is one sentence for every family alike.
- docs/ARCHITECTURE.md, term 12's Board cell: "a full slot refuses after the draw, and the quantum returns to its
  giver": a slot's fullness is an exclusion by another name; nothing in the act, in David's draw draft
  (DAVID-TENSOR24-G5-DRAW.md names the metric's slots and holds no "full slot", "occupation" or "capacity") or here
  derives a slot's capacity for a whole-speed family, whose clocks crowd. It should be marked OPEN or struck until the
  half-speed kinds stand.
- runner/files.py, held_departures: a kind "has no whole basis the 24 permute, so it stands only in the four-vector's
  square": a half-speed kind has none, so the files refuse it as they refuse a lone E; the line to widen with line 90.

## Open, so no code starts

- **The carry for a half-speed train.** The per-gear carry turns with signed permutations alone; the 48 are monomial in
  no basis beyond one axis. What would carry them is a carry whose remainders fill a domain the 48 keep, on Lambda the
  nearest point of W Lambda, eight gears at once: a search, which the gate refuses in the act (Solution24 step 3; the
  laws in code). Whether one contraction writes it, or whether the owner's click as one more operation beside the 24
  (click25, notes only, nothing stands) is that operation, is the owner's and the Boss's. Until then a half-speed family
  rides the act for one axis's eight turns, or at W = 1.
- **The pair click and the books.** On the act as built the pair's hand stays empty while the copies fill. Pauli on the
  act needs the act to move area into a half-speed family only through a pair hand that is not 0 (each quantum its own
  hand, the overlaps kept: David's cut (d), his open item on the carries against the overlaps). Not derived here.
- **G3/2's least whole form** (eight gears) is not built; sixteen stand.
- **The handed click** (the helicity) and the lift the plan fixes at G3 (SYM24's one door).
- **Term 11 on the metric family** (no second part, no click) and on a half-speed family (the pair's winding against
  each hand's) are not written.
- **Term 12's "full slot"** in the document: OPEN by name until a half-speed kind stands.

## Method: addressed

- **Does it follow by itself** (step 1): the symmetric rule follows from the one act and the 24 (every kind's own
  pairing symmetric, measured on the engine's tables); the antisymmetric families do not follow from the 24 at all;
  what does not follow is named: the half-speed kinds of the 48, which line 90 lacks and the owner may add.
- **The big things only** (step 3): the kinds, the 24 and the 48 derived from the star, the carry, the Gaussian hand; no
  table typed (the 48 closed from two of the engine's own lifts, Lambda by a Hermite basis in integers); the blockade's
  lambda is CHOSEN and said so; the declared refusal is named a fake.
- **Four layers** (step 4): above, forward, clock first.
- **The clicks and the books** (steps 5, 6): term 11's winding counts crowding for every family; the pair's hand would
  count Pauli; the books close for the first and break for the second on the act as built: a conservation lost in the
  clicks is no solution, said.
- **Both ways** (step 7): forward from the clocks (the belt, the pairings) and backward from nature (bunching light,
  Pauli's matter, Wu's handedness): where it does not match (no half-speed clock on the act) is named, not hidden.
- **Run locally** (step 8): five probes on the engine's own kinds, tables and act, one Node-clock and a cube of side 3,
  with their mutants (the declared refusal, the blockade; the Hurwitz and lattice lifts against the Gaussian 16; the
  wrong sign of the belt refused by the pair hand being 0 or by S and R disagreeing).
- **Unify** (step 10): one rule for every family, the kind's full turn; the pairing's sign and the belt's sign are one.
- **Say what was addressed** (step 12): the clocks that make it are the kinds' own turns and the Gaussian hand; what the
  clicks show is crowding for every family on the act today; what does not follow and is asked of the clicks is the
  half-speed clock and its carry.

## Ready for a hostile pair?

The rule and the whole-number results (the pairings, the 48 on Lambda, the belt) are exact and exhaustive at their
sizes and are ready to be read. The act's part is a measured failure, clear and reproducible, ready to be read as such.
The pair click as a law of the clicks is a candidate with its algebra done and its books open: not ready as DERIVED;
ready to be refused or taken as the question for the owner (the carry of eight gears at once).

## On Solution24

Add to step 3's big things "the 48 turns of spin, where a family's hand needs them", once the owner widens line 90; and
to step 5 that a click may read a pair of clocks as one hand with the swap's sign, the sign the family's full turn, so
that a count of the books is asked of it (step 6). Nothing else to add.
