# ALG1: the clocks' coupling complex, the algebra in which each object has its own size (node-all 4ce1aa9d7)

ALG1, for the Boss, 2026-10-31, 07:32 to 08:3x UTC. Read only: nothing in /home/user/Universe24 was checked out,
edited, committed or pushed. node-all 4ce1aa9d7's src and examples were extracted by git archive into S/alg1/all. S is
S.

**What was read.**
- Whole: BRIEF_PAIRS.md, with the rulings of 07:5x.
- Whole: MIN1.md, MATH1.md, both VARY3 reports with the Boss's answers, THIRD7.md (sections 0 to 6 and 8 to 12) and
  its mathematician's report.
- Whole: PICTURE.md at ed6a1f225. Its section 10 at 9a31b22b8 (Big Pic's weighing of this direction, relayed at 07:5x).
- The code: node-all's state.py, step.py, contract.py, mesh.py and carry.py; plans.py; run.py's record functions;
  load.py's assembly of the plans; main.layout.
- MIN1's two readers' reports, for the 24 and the pruning only.

**Probes.** S/alg1/probes/cochain.py (modes compare, books, coneback, turn), unitlay.py, twinD.py and twinD_back.py.
Their outputs are in S/alg1/out/.
- Whole numbers only, with Rule3's carry the one division.
- Run with python -I, the extracted tree's src first on sys.path, one process at a time under nice 19.
- The load was read before each run: 6.2 to 7.7, never above 8.
- Two outputs were rerun and are byte-identical: compare_click_100 and books_vary3_L1_200.

Every claim is marked DERIVED (proved here, or in the text named), MEASURED (the probe and its count) or OPEN.

## The answer to the owner

The algebra that orders the world of clocks is the clocks' coupling complex, with whole-number cochains on it, augmented
by the place: Z^F --C--> Z^E --B--> Z^V --eps--> Z.

**Its cells.**
- A clock (a train at a Node-clock) is a 0-cell.
- A meeting (two clocks a coupling joins, at one place or across one Mesh) is a 1-cell.
- Three clocks pairwise joined are a 2-cell.

**Its teeth.** Every tooth is a cochain: one whole number per oriented cell.
- It is born at the middle, which is the cell's zero.
- Read from the cell's other end it is its negation. In the engine's digits that is key - 1 - k.
- A passing is a 1-chain, and a clock's line is its boundary.
- The cells are laid from the structure alone.

**The doubles and the costs.** MIN1's doubles cannot be written in this algebra. node-all's runs come back byte for byte
on all five shipped worlds. On the click world one Node-clock holds 97 entries instead of 279 and does about 1,900
products a round instead of 145,000.

**What closes by construction.** Every case in the project is one face of d d = 0:
- the place's books are eps B = 0;
- the third click is never seen in a clock's line because B C = 0.

**The three clicks** are what a record of lines and sides can show:
- an edge's quanta are seen in lines and in sides;
- a triangle's quanta are seen in sides alone;
- the split click is the boundary map between the two;
- a 3-cell's quanta would be seen nowhere, so a 3-cell holds no tooth.

**The one reading that can fail** is the class of the clocks' own work in H_0. The augmentation reads it as the place's
total coupling work. No edge, triangle or other cell between clocks can carry it; this is a theorem, and Big Pic
reaches the same.

**The two-leg couplings.** For a two-leg coupling this work is exactly minus the change of the coupling's own staggered energy,
f (x y' + x' y). That is a function of the board's two slots, so each clock's books close exactly once it is read, with
no new element.

**The four-leg tie.** No polynomial of any number of slots can hold the tie's work. The residual is the board's own
step failing to keep the quartic's energy. A tooth on the tie's own cell can name it in the record, but it cannot close
it. Only a step that makes the quartic's work an exact difference closes it: the miracle's road is the board's, not the
record's.

## 0. The standings

| claim | standing | section |
|---|---|---|
| the coupling complex and its augmented chain complex; one number per oriented cell | DERIVED | 1 |
| D1, D2 by structure, D3, S1 and the work dead by structure cannot arise | DERIVED; MEASURED byte for byte | 1.4, 5.1 |
| node-all byte for byte (board, every tooth, every click, the click lines, the end teeth and digest read back); the run back exact from the end alone | MEASURED: five worlds and the mesh world at file key 7 | 5.1 |
| state per Node-clock 76 -> 40, 279 -> 97, 103 -> 33, 115 -> 43; products 23,616 -> 447, 144,984 -> 1,899, 19,080 -> 420, 30,008 -> 483 | MEASURED | 5.2 |
| on the click world MIN1's D2 holds 12 cells (24 sides) per Node-clock dead only by mesh = 0, the ruling's (c) | MEASURED | 1.4, 5.2 |
| the mirror keeps every cochain; a turn is a cellular map with the orientation sign (MIN1's flip) | DERIVED; MEASURED on two turns that reverse the Mesh's axis | 2.1, 2.2 |
| no 1-chain and no 2-chain books the place's coupling work (the H_0 theorem) | DERIVED | 3.2 |
| a two-leg coupling's work is minus the change of its staggered energy, exactly | DERIVED; MEASURED 0 off at every place and round | 3.3 |
| for degree 3 or more, no polynomial of a finite window of counts telescopes the work form | DERIVED | 3.4 |
| the tie's residual: VARY3's 82 keys reproduced; Big Pic's two numbers reproduced; 95 or 54 keys left after the two-slot forms tried | MEASURED | 3.4 |
| the tie's own cell: each clock within its teeth by construction; its run back exact | DERIVED; MEASURED | 3.5 |
| the triangle's twin needs only the dial D, not 3D | DERIVED; MEASURED on toy dials against Big Pic's Stepper, run back included | 4.3 |
| a 3-cell holds no tooth; its boundary is THIRD7's kept direction | DERIVED | 4.4 |
| the generations | OPEN | 4.2 |

## 1. The algebra

### 1.1 The complex, laid from the structure

The cells are laid once at the initialization, from the three files' structure. No strength is read.

**The clocks, X_0.** Every train t at every Node-clock x is a clock (x, t).

**The couplings.** A coupling is a monomial f x_1 ... x_d of J's potential whose factor is not 0 when every CHOSEN
strength is 1. The trains' characters, the 24's tables and the board's shape decide it: this is the 07:5x ruling's (b).
- A coupling is held as a multiset of legs, a polynomial's own form, so equal multisets are one coupling with their
  factors summed.
- Its clocks S_m are the trains of its value legs.
- Its degree d is its count of value positions, a squared leg counting twice.

**The meetings, X_1.**
- Own edges: every pair of clocks at one Node-clock that a coupling with two clocks or more joins.
- Mesh edges: every pair (x, t), (x + s, u) that the gradient vertex couples across a Spoke s.
- Each edge is held once, oriented from its lower train, or from its + Spoke's end.

**The triangles, X_2.** Three clocks of one Node-clock, pairwise joined.

**The place, X_-1.** One per connected part of the coupling graph. On the click world, with its Mesh cells idle, that is
each Node-clock's held, giver and taker.

**The boundaries.**
- B = d_1 is +1 at an edge's first clock and -1 at its second.
- C = d_2 is PICTURE.md section 7's.
- eps = d_0 is 1 on every clock of a part.
- So eps B = 0 and B C = 0: d d = 0 at both joints (DERIVED; L0 is the second).

**Read on the shipped worlds** (MEASURED, cochain.py's COMPLEX line):
- **click:** own edges (held, giver), (held, taker) and (giver, taker), and one triangle (held, giver, taker). Mesh edges
  wave to giver and wave to taker across each + Spoke, both ways round: 12 per Node-clock. The structure lays them; the
  file's mesh 0 leaves them idle.
- **mesh:** own edge (held, tied); Mesh edges wave to tied across +x, both ways round, 2 per Node-clock. The y and z
  sides are 1, so their Spokes close on the Node-clock itself and couple nothing: that is the board's shape.
- **bang, live and well:** no edge, since no train is held or tied. Their couplings are one-clock monomials (the notch);
  the metric's push is a plan of its own.

### 1.2 The state as cochains

- **On a 0-cell:** its gears (a, b, r) on every row, with its train's kinds as the coefficients (the module its kinds'
  matrices turn).
  - rd is a cochain with values in Z/T_d, held only on the rows where T_d > 1. Z/1 is a point.
- **On a 1-cell:** one element of Z/K, K the edge key (odd).
  - It is held as the balanced number c in [-(K - 1)/2, (K - 1)/2].
  - The engine's birth (K - 1) div 2 is c = 0, so "born at the middle" is the zero cochain.
  - Read from its other end the cell is -e and its tooth -c. In the engine's digits that is K - 1 - k. The owner's
    "one pair of teeth, born complementary" is one cochain value.
- **On a 2-cell** (on the bench, THIRD7's member): its pair (tau, eta), a module of rank 2 (section 4.3).
- **On a coupling's own cell:** its stored energy, when it has one (section 3).

### 1.3 The act on the complex

**The board.** node-all's four shears on the 0-cells, unchanged. They run on the structural plans: only the terms of
the structural couplings, with the pushes onto the unit row dropped and like monomials combined.

**The passing, Phi, a 1-chain.** Take a coupling m on two clocks t and u:
- l_t and l_u its legs on each, L = l_t + l_u (a held hand's two positions one leg, as edging counts them);
- W_t its works on t's legs over the window (b, a, a+).

edging's weight kappa (L - l) / L gives

    Phi_m(t, u) = kappa (l_u W_t - l_t W_u) / L = (kappa l_t l_u / L) (W_t / l_t - W_u / l_u).

That is the coboundary of the per-leg mean work, weighed by kappa l_t l_u / L (DERIVED from plans.edging). On three
clocks it is the coboundary of (kappa / L)(L - l_t) W_t on the triangle's edges. A Mesh coupling's passing is step.crossing's
c (a_p (a+_r - b_r) - a_r (a+_p - b_p)). It is held at the + end and read by the far end across one Mesh.

**The teeth.** n + c = q K + c', with c' in the window: the balanced carry. That is Rule3's carry(n, K, c + B), with
c' = r' - B and B the middle. In the engine's digits it is carry(n, K, k) itself, so the act needs no B (DERIVED).

**The lines.** B q: each clock's line is the boundary of the clicks.

### 1.4 Why the doubles cannot arise (DERIVED unless marked)

**D1.** A cochain has one value per cell; the reversed cell is not a second cell.
- MIN1's pair law, k(u, t) = K - 1 - k(t, u), is the cochain's own antisymmetry c(-e) = -c(e) in the balanced digits.
- The carry is odd there: n + c = q K + c' gives -n - c = -q K - c'. The window is symmetric because K is odd.
- So no lay can break the law either. A hidden unit laid in a tooth moves its complement with it, by construction
  (MIN1 2.1's remark).

**D2.** A 1-cell joins two distinct clocks that a structural coupling joins.
- The diagonal (t, t) is no cell.
- A pair no coupling joins is no cell.
- A reach with no structural Mesh coupling is no cell.
- The complex is the coupling's own support, read from the structure. The act never tests a value.

**D3.** rd's coefficient group on a row is Z/T_d. Where T_d = 1 the group is a point and holds nothing.

**S1.** A coupling is a multiset of legs, so h c_ii c_jj and h c_jj c_ii are one cell, with factor 2h. That is the
polynomial's own representation, the ruling's "combine like monomials at the load". MEASURED: bang, live and well each
lay 10 notch monomials, which combine to 7; the well's run is byte for byte (5.1).

**The factor-0 work** splits by its cause, as the 07:5x ruling splits it.

- **Dead by structure.** A train that is not held, tied or a square; a table entry 0; a push onto the unit row. These
  give no cell, so no work. MEASURED on the click world, node-all's terms against the complex's:

  | terms | node-all | the complex |
  |---|---|---|
  | J | 9,664 | 126 |
  | Mesh plan | 4,056 | 12 |
  | push | 910 | 178 |
  | clock | 130 | 25 |
  | passing | 9,664 | 108 |
  | crossing pairs | 4,056 | 12 |

- **Dead only by a strength the file chose as 0** (the ruling's (c)). These cells are laid and stay idle: the world's
  lay, as a row at rest is. On the click world they are:
  - the notch's 7 couplings (notch 0);
  - term 5's 178 terms (push 0);
  - the gradient vertex's 12 Mesh cells and their 12 terms (mesh 0).

  Together they are about 650 of the complex's 1,899 products and 12 of its 97 entries (MEASURED).

- **MIN1's D2.** MIN1's 85 entries drop these 12 Mesh cells by the strength's value: 24 of the sides MIN1 counts as
  never carrying are dead only because mesh = 0. MIN1's physicist found the same 24. The structural 97 is the count that
  is lawful now; the ruling's (c) decides the rest (MEASURED).

## 2. The laws

### 2.1 The run back

**The mirror on cochains.**
- The 0-cells' gears go as in step.mirror: slots swapped, r -> -1 - r, rd flipped on its T_d > 1 rows, the odd rows
  negated.
- Every 1-cochain is kept.
- On the bench, a 2-cell's tau is kept and its eta flipped.

**Why the act runs back (DERIVED).** The passing is odd under the window's reversal, since each term's work is. The
balanced carry is odd. So carry(-Phi, K, c') returns (-q, c): the run back is the same act on the mirrored state. This
is COUNT5 M1's law, in one line.

**MEASURED.** From the cochain end alone, with nothing saved, the run back reaches the start exactly:
- on every world (bang 10 rounds, click 100 and 300, live 20, mesh 125, well 10, the mesh world at file key 7 60);
- with the tie's cell teeth added (VARY3's L1 and node-all's L0, 200 rounds each; section 3.5).

### 2.2 The 24

**A turn g is a cellular automorphism.**
- It sends (x, t) to (g x, t): it moves Node-clocks, never trains.
- An own edge goes to the same edge at g x; a Mesh edge across Spoke s goes to the edge across g s.
- The 0-cells' modules turn by the kinds' matrices.

**On a cochain**, (g c)(g e) = sign(g, e) c(e). The sign is -1 exactly where g sends the cell's + end to its - end.
- So the held tooth goes to the far end and is read there negated. MIN1's flip is the orientation sign of a cellular
  map; in the engine's digits it is K - 1 - k.
- It is not the mirror's: the mirror keeps every tooth (MIN1's physicist, m1).
- The passing is an A1 scalar (MATH1 5.1), so the board's equivariance carries over to the cochain act (DERIVED).

**MEASURED** (turn mode, the mesh world at file key 7, 60 rounds, the Mesh teeth off their birth in 2,366 cell-rounds).
The turns diag(-1, -1, 1) and diag(-1, 1, -1) each reverse the Mesh's axis. For each of them, in 60 of 60 rounds:
- the engine's act(g s) equals g act(s);
- the cellular map with its sign equals the engine's turn read back;
- act(g c) equals g act(c) on the complex.

Also: MIN1's mathematician read 24 of 24 on a cube at key 1,000,003 (S/min1_math/REPORT.md, item 2). On the 2-cells,
THIRD7 reads 24 of 24 (lines, sides and landings).

### 2.3 Locality

- An own edge reads its two clocks at one Node-clock.
- A Mesh edge is held at its + end and reads its partner's counts (b, a, a+) across one Mesh, as step.crossing does.
- Its far end reads the held tooth across the same Mesh.

So a Node-clock reads its own cells and those across its six Meshes (DERIVED from the probe's act, which makes
step.crossing's reads and no other).

### 2.4 Integers, one division, no if

- **The act** has additions, products and Rule3's carry, and writes no number beyond 0 and 1 (the flip's 1). B is a
  layout number, like the key, and the act needs none (1.3).
- **No if, mask or bound in the act.** The cells are laid once, and the act runs on every cell alike.
- **The load reads the support:** the couplings whose factor is not 0 at unit strengths.
  - That is a count from the structure (the ruling's (b)), not a test of a strength. The strengths are the cochains'
    coefficients.
  - The probe reads this support by laying the files at unit strengths.
  - A writer lays the cells straight from the characters and tables, for instance a held hand times a tied train's A1
    form. For a kind whose matrices are signed permutations (A1, A2, T1, T2), Schur's lemma makes that form a multiple
    of the identity, so its support is its diagonal (MIN1: the tie's live entries are y = z). E's basis
    (e1 - e2, e2 - e3) is not orthonormal, so its form has entries off the diagonal. Either way the support is the
    table's own, a count from the structure. No plan is laid and then pruned (DERIVED).
- **Every dial must be odd.** The balanced window is symmetric only on an odd dial, so only there is a cell's reversal
  a negation.
  - K = 2 middle + 1 (KEY3's ruling) is odd by its form, and so are D = 3K and 3D = 9K.
  - A coupling counting four legs would make kappa 8 or 24 (MIN1's mathematician): it must be refused by name (KEY3's
    ruling) or have its weights read anew (OPEN).

## 3. The books

### 3.1 What closes by construction: checks, named so

- **Each edge:** q at one end and -q at the other. This is the orientation.
- **Each place:** eps B q = 0, d d = 0 at the bottom joint. It is the 07:5x ruling's place identity.
- **Each clock's line is unmoved by the third click:** B C W = 0, d d = 0 at the top joint.
- **David's identity:** K x (each clock's booked total) - (its swept passing) = B (c_0 - c_N). It stays within the
  clock's degree times B. MEASURED: 150,089,166 on L0, against 2B = 152,434,286.

None of these can fail on the act. Each reads the record's faithfulness, as the ruling names it.

### 3.2 The reading that can fail, and the theorem

The ruling's reading compares each clock's own work omega_v with its swept passing (B Phi)_v. Here omega_v is kappa
times the works of the edged terms on its legs.

**Theorem (DERIVED).**
- Take any 1-chain Phi: any edge form, split, weight or turn on edges.
- Add any 2-chain: any third-click form's C W.
- Then over the clocks of one connected part, SUM (omega - B (Phi + C W)) = eps(omega) = kappa SUM_m R_m.
- Here R_m = SUM_i J_i(a)(a+_i - b_i), over the coupling's legs, is its total work.
- Proof: eps B = 0 and B C = 0.

**What it means.**
- Each clock's books can hold within its teeth only if eps(omega), summed over the rounds, stays within the part's
  teeth.
- The obstruction is omega's class in H_0 = coker B. No cell of a complex whose vertices are clocks carries it.
- Big Pic's section 10 (9a31b22b8) states the same and reads it on the click world. This settles VARY3's B1 road by
  proof, not only by measurement: neither the split nor any triangle form can book the residual.

For a coupling on two clocks, each clock is left its leg share: omega_t - (B Phi_m)_t = kappa (l_t / L) R_m (DERIVED
from 1.3). These are VARY3's 1/3 and 2/3.

### 3.3 The two-leg couplings: the coupling's own energy is a function of the board

**The identity (DERIVED).** For d = 2, f x y,

    R = -f [(x' y + x y') - (x y_ + x_ y)] = -(E(after) - E(before)),   E(a, b) = f (x_a y_b + x_b y_a),

where ' is the next count, _ the count before, and E is the coupling's staggered energy over the two slots. A squared
leg f x^2 gives E = 2 f x_a x_b. So a two-leg coupling's stored energy is a function of the board's state.

**The books close exactly**, with no tooth and no new element:

    omega_t = (B Phi)_t - kappa (l_t / L) (E(after) - E(before)),   l_t / L = 1/2 on two legs.

**Why it is energy (DERIVED, in the continuum shadow: rationals, constant teeth).** push (a+ - b) is twice the row's
kinetic-energy change under the leapfrog, W (v+^2 - v^2) / 2 = push (a+ - b) / 2, from MATH1 2.1's recurrence
(in whole numbers up to the edge tooth's term, (r+ - r) (a+ - b) / 8). The work
form J_i (a+ - b) is the coupling's share of that. So this is energy kept between the clocks and their coupling.

**MEASURED** (books mode, L0, 200 rounds):
- kappa (SUM R + the change of E) = 0 at every place and round, on the two-leg terms (the hands' tie).
- Their stored energy alone reaches 17 edge keys at one place.
- So the ruling's reading fails even on a two-leg coupling until the coupling's energy is read; once read, the books
  hold exactly.
- Big Pic's tieresid.py reads the same at 27 of 27 Node-clocks.

### 3.4 Couplings of degree three or more: no polynomial of the slots

**Theorem (DERIVED).** The work form's R_m telescopes through a polynomial of a finite window of counts only if d <= 2.

**Proof.**
1. Suppose F(a_(n+1), ..., a_(n+1-w)) - F(a_n, ..., a_(n-w)) = R(a_(n-1), a_n, a_(n+1)) as polynomials.
2. The left side reads a_(n-w) only through its second F, so F does not depend on its last slot. By induction F is a
   function F(u, v) of two slots.
3. Setting a_(n-1) = a_(n+1) makes R = 0, so F is symmetric.
4. Varying a_(n+1) gives F(v, u) = -f SUM_i v_i PROD_(j != i) u_j + G(u), linear in v.
5. Symmetry then equates a part of bidegree (1 in v, d - 1 in u) with one of bidegree (d - 1, 1). With f != 0 that is
   impossible for d >= 3. For d = 2 the two coincide, and E of 3.3 is the solution.

**What it says of the tie** (d = 4: x_y x_z k_rho k_rho).
- No stored energy of the board's slots holds it, whatever their number.
- Its residual is the leapfrog's failure to keep the quartic's energy: MIRACLE_A's Theorem A, seen on one coupling.
  This is DERIVED for polynomials of the counts; a function of the teeth is Theorem A's case, which is drafted.
- A third slot added to the present step cannot hold it either: the theorem covers any finite window. What HAT3 or HAT4
  would change is the step itself, and that is where the road lies.
- Only a change of the push makes R an exact difference: a discrete gradient whose push reads the next count (HAT4,
  the miracle's roads).

**On the shipped worlds the tie is the only coupling with d >= 3.** The notch (c00 c00, c_ii c_jj), the held spring
(rho rho), the hands' tie (x_y y_z) and the gradient vertex (M D L) are all d = 2 (DERIVED from plans.py).

**Named beside it.** The metric's push J5, which step.py says "enters no side's passing", is a coupling between the
metric and the sourcing clocks with no edge. It is idle on the click world (push 0) and live only on the well world,
which has no click. OPEN.

**MEASURED** (books mode, 200 rounds; one edge key K = 152,434,287):

| reading | L1, VARY3's varied lay | L0, node-all's own |
|---|---|---|
| own - swept at a clock, largest | -12,527,520,000, 82 keys (giver, site 17, round 170): VARY3's number | 2,957,760,000, 19 keys (taker, round 155): VARY3's |
| the place's kappa SUM R, four-leg | -18,791,280,000, 123 keys (site 17, round 170) | -5,459,040,000, 35 keys |
| after adding the change of V(a) + V(b) | 14,521,320,000, 95 keys | 8,139,960,000, 53 keys |
| after adding the change of the full polarization E4 | 8,340,480,000, 54 keys | 1,800,840,000, 11 keys |
| two-leg: kappa (SUM R + the change of E) | 0 everywhere (the taker's counts stay 0) | 0 at every place and round |

- E4 = (f / 3) SUM over the six ways to put two of the four positions at each slot, so that E4(a, a) = 2 V(a), as
  E(a, a) = 2 V(a).
- At site 0, round 200 of L0, SUM R four-leg = -909,840,000, against V(a)'s change of 313,740,000. These are Big Pic's
  two numbers to the unit.

### 3.5 The tie's own cell: what can be built, and what it is

**The cell.** A 0-cell of a new kind: the coupling's own, the barycentre of the tie's simplex, joined to each clock that
carries a tie leg.
- It is the one cell the theorem allows, since it is not a clock.
- With it, the clocks' bookings no longer sum to 0; the difference is what the tie's cell takes.

**Its teeth.**
- One tooth per clock carrying a tie leg: on the click world held, giver and taker, so 3 per Node-clock.
- The dial is the edge key K, and each is born at the middle (balanced 0).
- Each turns by its clock's leftover, kappa (l_t / L) R_m.
- The two-leg leftovers can ride on it too, or be read off E with no tooth.

**MEASURED** (L1 and L0, 200 rounds).
- With it, each clock's K x (booked + its cell's quanta) - own work stays within its teeth: at most 151,714,287 on L1
  and 180,617,139 on L0, against (degree + 1) B = 228,651,429.
- Its run back by the same act on the mirrored state is exact (L1 and L0, 200 rounds each). The leftover is odd under
  the window's reversal.
- The cell's quanta at round 200, summed over the sites: held 83 and giver 170 on L1; held -324, giver 324 and
  taker -486 on L0.

**What it is.** It closes the books by construction. It names where the tie's work goes and makes every clock's books
close, but the reading that can fail moves onto the tie's cell: its booked quanta against any stored energy of the
board. There it fails, by 54 keys on L1 with the best form tried.
- So it does not close the residual. By the Boss's answer 1 of 07:5x on VARY3, it counts as "the residual booked" only
  if a named cell that is not a clock may hold it.
- For the owner's batch, if he wants the residual named in the record: one tooth per clock carrying a tie leg, record
  only (the board reads no tooth), dial K, born at the middle. I do not propose it as a closure.

**What closes it.** A step whose quartic work is an exact difference. By the theorem of 3.4, no record-side form and no
extra slot of the present step can do this. With such a step, the tie's own energy, a function of the board, books the
residual as a two-leg coupling's energy does, with no tooth. This agrees with Big Pic's section 10.

## 4. How it orders the world of clocks

### 4.1 Clocks, meetings and clicks, by dimension

| dimension | cell | holds | its quanta seen in | the click |
|---|---|---|---|---|
| -1 | the place | nothing: its books close, eps B = 0 | the place identity | none |
| 0 | a clock (a train at a Node-clock) | its gears: the board | its line, B q | none |
| 0, a new kind | a coupling's own cell | its stored energy: E when d = 2; nothing exact when d >= 3 | nowhere, unless a tooth is laid | none |
| 1 | a meeting (two clocks a coupling joins) | one tooth in Z/K | lines and sides | the first click |
| between 2 and 1 | the boundary map C: the Hodge split 3 x = (3 x - C C^T x) + C C^T x | none | none | the split click |
| 2 | a triangle | (tau, eta) | sides alone, since B C = 0 | the third click |
| 3 | a tetrahedron | nothing (4.4) | nowhere, since C d_3 = 0 | none |

- A meeting is a 1-cell. An event is one wrap of its tooth: one quantum given at one end and taken at the other, the
  ruling's one give and one take on a side.
- The record has two levels: lines on 0-cells and sides on 1-cells.
  - A 1-cell's quanta reach the sides directly.
  - A 2-cell's reach them through C.
  - A 3-cell's would reach them through C d_3 = 0, which is never.
  - So a record of lines and sides can show exactly three: the first click, the split and the third click. The count
    three follows from the record's two levels (DERIVED, given the record's form; a record with a level for triangles
    would change it).

### 4.2 The third click, "never seen alone", and the generations

- "Never seen alone" is d_1 d_2 = 0 (L4). The place's books closing is eps d_1 = 0. It is one law at two joints
  (DERIVED).
- The owner's word ties the third generation to the third click: never seen alone. In the algebra that property has
  one exact place, the top joint. Nothing above dimension 2 can be shown by a record of lines and sides, so no fourth
  click can be shown there (DERIVED, under that form).
- That the three kinds of click are the three generations is the owner's word, to be read only in the click world
  through the decoder: OPEN. Big Pic's three heights and Koide's 2/3 are not derived here: OPEN.

### 4.3 The twin's own size (Big Pic's first word)

**A 2-cell's module has rank 2:** the tooth tau, kept by the mirror, and the twin eta, flipped by it. "One number per
cell" is the 1-cells' rule. On a 2-cell it is one gear's two entries:
- with a gear's mirror: in ((tau + eta) / 2, (tau - eta) / 2) the mirror is the slot swap;
- but not a gear's law: the turn gives b' = 27 a - 14 b, not b' = a (THIRD7's mathematician, MINOR 2; MIN1 2.7).

So Big Pic's "one gear per cell, with its now and its before" holds for its size and its mirror, not for its step
(DERIVED). THIRD8's two entries per triangle are this module.

**Its own size is smaller.** Every shear that moves tau adds 3 eta, and 3 (eta + D) = 3 eta mod 3D, so eta enters the
act only mod D (MATH1 3.4). The round therefore runs on (tau mod 3D, eta mod D):
- eta += 3 tau descends to the dial D;
- the birth (3D - 1) / 2 is (D - 1) / 2 mod D, the middle of D;
- the flip 3D - 1 - eta descends to D - 1 - eta.

So the twin's dial is D, and the Z/3 that no landing reads drops by construction (DERIVED). The pair then has
3D x D states: on 3D = 63 that is 1,323, the count at which MATH1's F4 found the landing words saturate (3,969 / 3).

MEASURED (probes/twinD.py and twinD_back.py; one triangle; tau on 3D and the twin on D):
- Against Big Pic's mode 11 Stepper (circ.py, run read only), the landings, tau and the twin's class mod D are 0 off.
  This held for every pair of the dials 3D = 15, 63 and 255 (225, 3,969 and 65,025 pairs), for 30 rounds, under a steady
  passing of 7, a steady passing of 2D + 3, and a walk.
- The run back from the end alone, by the same round on the mirrored pair (tau kept, the twin flipped on D) with the
  passings negated and in reverse order, reached the start for every pair of 3D = 63 and 255 (1,323 and 21,675 pairs,
  30 rounds), with the forward landings negated and reversed.
- On the file's dial this is a third of the twin's states, log2(3) bits per triangle, with the same two entries. A change
  of the twin's dial goes to the owner by Sofer's rule.

### 4.4 A 3-cell (Big Pic's second word)

**Where it arises.** Four clocks pairwise joined carry four triangles whose boundaries are dependent.
- C has the kernel k = (-1, 1, -1, 1): the 2-cycle of the tetrahedron's surface, Z_2 = ker C (THIRD7's
  mathematician, OPEN-1).
- If the 3-cell is filled, d_3 is that cycle (up to sign), and C d_3 = 0.

**It holds no tooth.** Given a tooth, a 3-cell's quanta would land on the four triangles as k W. Their edges' net is
C k W = 0, so no side and no line would ever show them (DERIVED). Only a record level for the triangles' landings could;
the record has none (PICTURE.md section 5 names a circulation quantum's side OPEN).

**Its role is the opposite: it removes a direction.**
- The triangles' hidden pairs on such a place should live on C_2 / Z_2, of rank 3, not on C_2, of rank 4.
- The kept direction OPEN-1 measured (k.tau and k.eta constant over 20,000 rounds) is the part that quotient removes:
  a double by MIN1's rule.
- A carrier with no pick is the circulation lattice im C in C_1, which needs no basis of triangles. Its dial, turn and
  run back are OPEN.

**A coupling of four distinct trains is no new click either.**
- Its passing is a 1-chain on its six edges, and its circulations land on its triangles.
- Its own work (d >= 4) is an H_0 leftover, like the tie's (DERIVED from 3.2 to 3.4).
- No shipped plan lays one.

### 4.5 The families

- **The 24's five kinds** are the 0-cells' coefficient modules. A passing is an A1 scalar on a 1-cell (MATH1 5.1), so
  no kind reaches the record except through the A1 work: a click names a meeting, never a kind (DERIVED).
- **The half-speed trains** (2O's spinorial kinds) are 0-cells with no coupling cell in this build: no plan couples
  them (load.trains_of; plans.py). They are isolated vertices of X, meet no clock and never click (DERIVED; no shipped
  world lays one).
- **The coupling family, ordered by its cell** (DERIVED):
  - one clock, d = 2 (the held spring, the notch): the energy stays inside the clock, booked on no edge, as edging
    weighs it 0;
  - two clocks, d = 2 (the hands' tie; the gradient vertex across a Mesh): the energy E is the board's, and the books
    are exact;
  - two clocks, d = 4 (the tie): the residual. It is the only one on the shipped worlds.

### 4.6 What the algebra carries and what it does not (Big Pic's item 4)

**It carries:**
- the record's structure: cells, orientation, one number each;
- the books: d d = 0 and the H_0 class;
- the laws' form: the mirror on cochains, the 24 as cellular maps, locality;
- the removal of the doubles;
- the residual's exact place, and the theorem that no cell closes it.

**It does not carry** (each OPEN, by name):
- the square-2 stop (STOP1) and the runaway: the board's step;
- the key's value (KEY3): the algebra asks only that every dial be odd;
- the third click's memory (THIRD8): the turn L's orbit on the 2-cell's module;
- the term that parts the doublets: a coupling cell the plan does not lay;
- the strengths chosen in the files (AUDIT2 A1): they are the cochains' coefficients;
- light's lines (LIGHT2). On the board the Mesh edges are couplings of the board's wave, and nothing here names light.

It is the books' algebra, not the dynamics'.

## 5. MEASURED

### 5.1 Byte for byte (compare mode)

The cochain act runs beside step.act. Every round compares a, b, r, rd, every tooth read back, every click and the
record's click lines (run.clicked's JSON text). At the end it compares the end line's teeth and the digest of the state
read back. Then it runs back from the cochain end alone, with nothing saved.

| world (rounds) | entries off: a, b, r, rd, k, clicks, lines | click entries not 0 | click lines | end teeth, end digest | run back |
|---|---|---|---|---|---|
| bang, tensor24 (10, all its ticks) | 0, 0, 0, 0, 0, 0, 0 | 0 | 0 | equal, equal | exact |
| click (100 of 5,000) | 0, 0, 0, 0, 0, 0, 0 | 4,050 | 5,508 | equal, equal | exact |
| click (300 of 5,000) | 0, 0, 0, 0, 0, 0, 0 | 22,950 | 19,521 | equal, equal | exact |
| live (20 of 100) | 0, 0, 0, 0, 0, 0, 0 | 0 | 0 | equal, equal | exact |
| mesh (125, all its ticks) | 0, 0, 0, 0, 0, 0, 0 | 36,192 | 21,589 | equal, equal | exact |
| well (10 of 128; the notch combined, 10 -> 7) | 0, 0, 0, 0, 0, 0, 0 | 0 | 0 | equal, equal | exact |
| mesh at file key 7, MIN1's variant (60; 138 cell-places off the birth at the end) | 0, 0, 0, 0, 0, 0, 0 | 6,824 | 4,204 | equal, equal | exact |

- The click run was made twice, with byte-identical outputs.
- The header is the files' and the layout's, which the state's form does not touch; it was not compared.
- The digest is taken on the state read back, as the 07:5x ruling has it.

### 5.2 State and work per Node-clock per round

| world | state, node-all -> cochain | what the cochain holds | products, node-all -> cochain |
|---|---|---|---|
| bang, live | 76 -> 40 | a, b, r 12 each; rd 4 | 23,616 -> 447 |
| click | 279 -> 97 | a, b, r 26 each; rd 4; own teeth 3; Mesh cells 12 (idle: mesh 0) | 144,984 -> 1,899 (about 650 of them on strength-0 cells) |
| mesh | 103 -> 33 | a, b, r 10 each; rd 0; own teeth 1; Mesh teeth 2 | 19,080 -> 420 |
| well | 115 -> 43 | a, b, r 13 each; rd 4 | 30,008 -> 483 |

- Products are counted as MIN1 counts them: 3 per contract term; the clock plan read 5 times; 4 per passing term plus
  its weights; 3 per Mesh coupling (node-all's at both ends, the complex's at the + end only).
- The 144,984 agrees, within the counting, with MIN1's about 144,800 and its physicist's 143,684.
- The click world's couplings: 2,416 laid, 42 structural, 32 live, and 39 once like monomials are combined.
- Its teeth carries fall from 175 to 15, of which 3 are live.

### 5.3 The books

As in the table of 3.4 and the counts of 3.5 (books and coneback modes).

### 5.4 The 24

As in 2.2 (turn mode).

## 6. OPEN

1. The ruling's (c): the click world's 12 Mesh cells per Node-clock (mesh 0), and the push's and the notch's
   strength-0 terms.
2. The twin on the dial D (4.3): measured on toy dials only, not on the board or at the file's dial.
3. The hidden pairs on a place of four pairwise-joined clocks, on C_2 / Z_2 with no pick, through im C (4.4).
4. A dial that comes out even (a coupling counting four legs): refused by name, or its weights read anew.
5. The tie's residual. Only a step closes it (3.4); the tie's cell only names it (3.5).
6. The metric's push J5, a coupling with no edge (3.4).
7. Harmonic cycles of the board-level complex (own edges and Mesh edges round the torus), which would be carried as
   first clicks on a world with mesh != 0: not read.
8. The generations, Koide's 2/3 and the three heights (4.2).
9. The dynamics (4.6).

## 7. DERIVED, MEASURED, and where my measurement overturned my derivation

**DERIVED:**
- the complex and its boundaries; the balanced cochain and its odd carry;
- the passing as a weighted coboundary;
- D1, D2 by structure, D3 and S1 by construction;
- the mirror on cochains, the 24 as cellular maps with the orientation sign, locality, and the odd dials;
- the H_0 theorem; the two-leg identity R = -(the change of E); the degree theorem (no polynomial telescoping for
  d >= 3);
- the tie's cell; the twin on D; the 3-cell holding no tooth; three clicks for a record of two levels.

**MEASURED:**
- byte for byte with the run back on five worlds and one variant;
- the state and the work;
- the books on L0 and L1, with VARY3's 82 keys and Big Pic's two numbers reproduced;
- the twin on the dial D against Big Pic's Stepper, with its run back, on three toy dials;
- the two-leg identity at 0 off;
- the tie's cell within its teeth, and its run back;
- two axis-reversing turns of the 24 on moving Mesh teeth.

**Where my measurement overturned my derivation:**
1. I expected the tie's residual to be mostly its potential's change over the two slots, so that its cell would need
   no tooth. V(a) + V(b) leaves 95 of the 123 keys at L1's peak, and the full polarization still leaves 54: a defect.
   Section 3.4's theorem, derived after the measurement, explains why.
2. I expected the structural complex to hold MIN1's 85 entries on the click world. It holds 97: 12 Mesh cells are
   dead only by mesh = 0.
3. I expected each clock's books to hold within its teeth wherever every coupling is two-leg. On L0 the hands' tie's
   own energy reaches 17 keys at one place, so the reading holds only once the coupling's energy E is read.

## 8. Files (all under S/alg1/)

- ALG1.md: this text.
- probes/cochain.py: the cochain act and its four modes. probes/unitlay.py: writes a world's files with every CHOSEN
  strength at 1 (into unit/), the key the world's own. probes/twinD.py and twinD_back.py: the twin on the dial D.
- The outputs, in out/:
  - compare_tensor24_10.txt, compare_click_100.txt and its _run2, compare_click_300.txt, compare_tensor24-live_20.txt,
    compare_tensor24-mesh_125.txt, compare_tensor24-well_10.txt, compare_mesh_key7_60.txt;
  - books_vary3_L1_200.txt and its _run2, books_click_L0_200.txt;
  - coneback_vary3_L1_200.txt and coneback_click_L0_200.txt;
  - twinD_30.txt and twinD_back_30.txt;
  - turn_mesh_key7_60.txt.
- worlds/vary3_L0/: VARY3's shipped setting beside its universe and piece (byte for byte node-all's click world).
- all/: node-all 4ce1aa9d7's src and examples, extracted by git archive.
- PICTURE_ed6a1f225.md: Big Pic's text, as read by git show.
