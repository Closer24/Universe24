# The massive record: the self pair as an element of the algebra (a proposed chapter of ALGEBRA.md; the Algebra Mathematician, 2026-09-23)

**The order and its bound.** The Boss's order on the model owner's word of
2026-09-23, 12:35Z ([record 1386](LOG_2026-09-20.md), the Boss's
translation: "we do not create the laws of physics anew; we derive
everything algebraically and then implement in the engine to test; check
whether a foreign object is a kind of group or something of that kind,
like the rest"): derive, from the structure and the formulas of
[ALGEBRA.md](ALGEBRA.md) alone, what the candidate law of
[record 1385](LOG_2026-09-20.md) is in the algebra. The candidate: at
every Node the rule of `docs/designs/detector_law/DESIGN.md` section 2
(on the branch push-balance-r3, not yet on main; "DESIGN" below) with
the pair [1, 3], and a foreign object a set of Nodes,
declared by shape (a square on a layer or a cube), whose every Node
carries one extra declared pair [p, q] that subtracts that fraction of
its own present record every interval (the self term), in the
physics-rule reviewer's integer form, taken here as the candidate:

    3 q a_next + r' = q S_6 - 3 q a_before - 3 p a_now + r,   0 <= r' < 3 q,

S_6 the six-neighbour sum. This chapter is docs only, proves what it
proves in the chapter's own terms, and edits nothing else; it was
written without reading the reviewer's sections 8 to 10 of
`docs/designs/detector_law/PUSH_BALANCE.md` (the same branch), so that
the Boss can compare the two derivations line by line. Every formula below
names the ALGEBRA.md formula it starts from (its chapter and section, "1.1",
"2.2", "4.8", "5.1" and so on); every number carries its kind
(COMPUTATION: a closed form, no run; DECLARATION: an input of the world
file; CHECK: a pure-Python evaluation of a stated formula or matrix on a
stated board, not the engine and not a run of the register; NATURE:
none is used here; DETECTOR and GAMEBOARD only where ALGEBRA.md's own
lines are quoted). Every result is stated as matching nature, never as
how nature is; nothing here is compared with nature.

**The symbols, named once** (ALGEBRA.md's head for the ones it names).
a_now, a_before, a_next the record's amplitudes at a Node at the present
interval, the one before and the one to come, integers on the record's
wheel; r and r' the row's remainder before and after the division; S_6
the sum of the six neighbours' a_now; [p, q] the self pair, declared per
Node, p >= 0 and q >= 1 whole; B the object, the set of Nodes that carry
the pair; s its side in Nodes; chi_B the indicator of B (1 on B, 0 off
it); N_board the number of Nodes of a periodic board; Lap the lattice
Laplacian, (Lap a)(x) = S_6(x) - 6 a(x); **A** the interval's operator
on the amplitudes, defined in section 0.2; L an eigenvalue of -Lap, in
[0, 12] on a three-dimensional world and [0, 8] on the design's
one-layer world; mu the mass angle per interval, mu^2 = p / q, the
letter m of ALGEBRA.md 5.1 (ii) written mu here because m is taken by
the mass angle of the walk there and M by a body's content; omega a
frequency angle per interval and **k** a wave-number vector, its
components k_a angles per Link (the walk's omega and kappa of 5.1 (ii));
c the pace 1 / sqrt 3 Links per interval (4.2); v a pace in Links per
interval; k the whole number of intervals per Link of a moving record,
v = 1 / k (3.3); z the growth factor per interval of a mode, the root
of its characteristic equation; E the design's conserved energy (DESIGN
2.1), E_q its integer form; gamma the Lorentz factor, as the thing
compared with; D the diagonal matrix of section 4.6; W_S = 1.516386 the
simple cubic lattice's Watson integral (COMPUTATION, a constant of
analysis).

---

## 0. The candidate written in the algebra's symbols

### 0.1 The rule without the self term, in ALGEBRA.md's terms

DESIGN.md section 2 writes the rule at a Node with a row of the record
as 3 a_next + r' = S_6 - 3 a_before + r, and its three tests: the
six-neighbour sum the group-ring addition (G) over the six Ports (2.3),
the division by 3 with the remainder kept on the row the verb (D)
(2.6), the accumulator carrying r the translation (T) (2.1); it reads
the record's own row at the Node and at the six neighbours (2.8, local);
it commutes with the 48 because S_6 is a symmetric function of the six
Ports, which the 48 permute (1.1, "the action of G_48 on the state").
In the leapfrog form DESIGN 2.1 gives, a_next - 2 a_now + a_before =
(1 / 3) (S_6 - 6 a_now) = (1 / 3) (Lap a_now), the middle term 2 - 6 c^2
being exactly zero at c^2 = 1 / 3 (4.2: c the flight operator's norm).

### 0.2 The candidate, in the same form

Divide the candidate by 3 q and move the terms: on a Node of B,

    a_next - 2 a_now + a_before = (1 / 3) (Lap a_now)(x) - (p / q) a_now(x) + (r - r') / (3 q),

and off B the design's line with (r - r') / 3. So the candidate is the
design's leapfrog with one operator in place of (1 / 3)(-Lap):

    a_next - 2 a_now + a_before = -(**A** a_now)(x) + the remainder's grain,   **A** = (1 / 3)(-Lap) + (p / q) chi_B,

**A** a symmetric matrix on the Nodes (the Laplacian is symmetric, the
added term diagonal), with the remainder's grain below one amplitude
unit per Node per interval (0 <= r' < 3 q, as 0 <= r' < 3 off B). On the
design's one-layer world (a_U = a_D = a_now) the same with -Lap the
four-neighbour Laplacian, whose eigenvalues lie in [0, 8]. Everything
below is a statement about **A**: its spectrum (section 4), its
symmetry (section 3), its dispersion (section 5).

### 0.3 The dispersion of the rule, the one formula the rest reads

On an object that fills a periodic board, or far inside a large one, a
plane wave a(x, t) = cos(**k** . x - omega t) solves the rational form of
the candidate (the remainder set aside, as DESIGN 2.1 sets it aside for
E) exactly when

    2 - 2 cos omega = (2 / 3) sum over the three axes a of (1 - cos k_a) + p / q,        (the massive dispersion, COMPUTATION)

since Lap cos(**k** . x) = -2 sum_a (1 - cos k_a) cos(**k** . x). At p = 0
it is the massless rule's, whose small-angle limit omega^2 = (1 / 3)
abs(**k**)^2 is the pace c = 1 / sqrt 3 of 4.2 (rung 2; DESIGN section 6
A's 0.992 to 0.999 of c at lambda >= 12 Links, the lattice's departure
at fourth order). With p > 0 its small-angle limit is

    omega^2 = c^2 abs(**k**)^2 + mu^2,   c^2 = 1 / 3,   mu^2 = p / q,      (rung 2, second order in the angles)

which is the relation ALGEBRA.md 5.3 states for the Dirac walk under
(A1) and (A2), omega^2 - kappa^2 = m^2 in the walk's units, here with
the Beam Law's c^2 = 1 / 3 written out (W = E'_0^2 + 3 **p** . **p**, "the
3 is 1 / c^2"), and the mass angle m^2 of 5.1 (ii) equal to p / q. This
is the dictionary's entry point (section 1).

---

## 1. Is the foreign object a new group object? No: a declared scalar of the Node, and the shape world data

**The four group objects are untouched** (1.1). The symmetry group of
the cube G_48 and the group of order 24 within it act on directions and
Nodes and "trivially on every scalar (a content, an amount, a count, an
age)" (1.1, the action of G_48 on the state); the self pair [p, q] is a
scalar of the Node, so the 48 do nothing to it and it does nothing to
them (section 3 proves the commutation). The phase circle Z_N and its
group ring Z[Z_N] (1.5) are not entered: the self term multiplies an
amplitude by a declared rational and adds, it turns no phase. The
translation group of the torus (1.6) acts on B as on any set of Nodes.
The collision's cyclic group (1.1) is not read. No fifth object is
needed, and none is defined: the candidate adds to the state space
nothing that a group acts on non-trivially, and it adds no new
operation (section 2).

**Which element it names.** The pair [p, q] is a declared rational per
Node, the same kind of element as the world's pair c2 = [1, 3] of
DESIGN section 2, the suspension pair n / d and the charge "as a
rational pair" of 2.10; among the fifteen rows of 2.10 it belongs with
"the family table, the declared input on which no verb acts". Its
physical name, by the dictionary of 1.2 and the dispersion of 0.3: the
square root of p / q is the mass angle m of 5.1 (ii) and 5.3 (E_0 =
hbar m, "the spacing over the reduced Compton wavelength"), so the pair
names a rest frequency, omega_0 = arccos(1 - p / (2 q)) per interval
exactly on the lattice (section 5.1), sqrt(p / q) at second order. It is
therefore the mass row's element, with one difference the dictionary
must carry: the mass row's M is a body's content in units of its
family's quantum, "on Z, the non-compact scale, free" (2.10), carried by
the record that hops; the self pair is the Node's, a constant of a
place, on Q, carried by nothing. In the words of ALGEBRA.md 5.1 (A2),
"the mass the staying share": the self term is the share p / q of its
present record that a Node of B holds back from what the six-neighbour
rule would re-emit, which is (A2)'s definition of the mass read on a
place instead of a packet. Compared with the design's own second rule
of a massive family (the pace abs(**p**) / E' of massive-rows-v1, 5.10),
this one puts the mass on the Node, not on the row: the record on B is
massive because of where it is.

**Law or world data.** The rule is one line for every Node, with the
pair a value: p = 0, q = 1 gives the design's line bit for bit (3 a_next
+ r' = S_6 - 3 a_before + r), so the massless Node is a value of the
same primitive and not a branch ("its special cases are values, not
branches", 2.8). That line is law. The shape B, its side s, its place and
its pair are world data: chosen per world as `shape` and `boundary` are
(1.6, "chosen per world"), a set of Nodes as a detector's is (3.1). Two
shapes are two worlds under one law. Under the three tests of 2.8, in
the algebra's reading: generic PASS (one primitive, the pair a declared
integer per Node, the engine branching on no name); vector PASS (section
2); local PASS on the reading (the own row and the six neighbours), with
one line for the physics-rule reviewer, not the algebra's to decide: the
pair is a constant of the Node's declaration kept at the Node, like the
world's [1, 3] and unlike a remainder or a register (AGENTS.md's "nothing
kept at a Node beyond the events there"); whether a declared constant
per Node is admissible under LOCALITY-1 is the reviewer's line.

**The result (1): DERIVATION.** The foreign object is a name given to an
element of the existing structure: a declared scalar of the Node (a
rational pair) on which the 48 act trivially, named by the mass row of
the dictionary as the mass angle of the record on that place; the shape
is world data; the law is the one rule with the pair as a value.

---

## 2. Is the self term exactly one of the six operations? Yes: (B) then (D), with (T) on the remainder

Write the candidate's right side as one linear form with a declared
integer vector on the eight integers the Node reads:

    q S_6 - 3 q a_before - 3 p a_now = (q, q, q, q, q, q, -3 q, -3 p) . (a_E, a_W, a_N, a_S, a_U, a_D, a_before, a_now),

a signed inner product over declared columns (2.2, "a vector, a declared
diagonal matrix of +1 and -1, a vector"; the coupling **r** = **C** **a** with
**C** declared), the verb (B) with a one-row matrix whose entries are the
world's integers; without the pair it is the six-neighbour sum, which
DESIGN calls (G) and which is the same sum with the weights all one.
Then 3 q a_next + r' = (that form) + r is the division with the
remainder kept (2.6, the verb (D)): the wall 3 q, the whole part a_next,
the remainder r' in [0, 3 q) kept on the record's row at the Node ("the
remainder is the row's, not the Node's", DESIGN section 2), and the
carry of r from one interval to the next the translation (T) of the
row's accumulator by its rate (2.1). The rate is linear in the state
(2.8 allows "at most bilinear"); no root, no float, no rounding at run
time beyond the one division; nothing of 2.7's seventh verb.

**Where the remainder lives, and its grain.** On a Node of B the
remainder is an integer below 3 q where off B it is below 3: the same
verb with a wider wall, and the same grain, below one unit of the
amplitude per Node per interval (r' / (3 q) < 1). Nothing accumulates:
r' is bounded by the wall at every interval (2.6, "bounded below the
wall, its one owner").

**One convention, named.** The candidate's r' in [0, 3 q) with a signed
numerator is the floor (Euclidean) division, the design's own choice
for its r in [0, 3); ALGEBRA.md 2.6 records that the code's `by_drive`
truncates toward zero on a signed accumulator and that the two wordings
agree on a non-negative one. The energy identity of section 4 holds
under either (both are the rational form plus a remainder below one
unit); the 48 commute with either (a remainder is a scalar); the two
differ only in the sign the remainder carries. It is a declaration of
the build, not of the algebra.

**The result (2): DERIVATION.** The self term is exactly expressible:
(B) the linear form with the declared integer row (q six times, -3 q,
-3 p), then (D) the division by 3 q with the remainder r' in [0, 3 q)
kept on the row, with (T) carrying r; nothing is missing.

---

## 3. Does the rule with the self term commute with the 48, and with the 24? Yes, exactly, with the shape carried along

**Statement.** Let g be one of the 48 (1.1: a signed permutation of the
axes, acting on the Nodes about a centre by its matrix **M**_g and on the
Ports by the same map), and let g act on a state s (the amplitudes a_now,
a_before and the remainders r at every Node) by (g . s)(x) = s(g^(-1) x),
and on the world data by g B = { g x : x in B } with the pair carried to
g x. Let V_B be the interval's map of the candidate with the object B.
Then

    V_(g B) (g . s) = g . V_B (s)   for every g of the 48 and every state s,          (COMPUTATION, exact)

and in particular, when g B = B (g in the stabiliser of B), V_B commutes
with g exactly.

**Proof, in the chapter's own terms.** At the Node g x the map V_(g B)
reads the six neighbours of g x, which are the images under g of the six
neighbours of x (g sends Ports to Ports and opposite to opposite, 1.1;
the L1 neighbourhood is carried to itself), so S_6 at g x of g . s is
S_6 at x of s: the sum is a symmetric function of the six Ports and the
48 only permute them (the same fact that makes the design's rule
commute). The own row (a_before, a_now, r) at g x of g . s is the row at
x of s; the pair at g x of g B is the pair at x of B. So the linear form
(B) of section 2 takes the same eight integers in the same declared
order, hence the same value; the division (D) by the same wall 3 q gives
the same a_next and the same r'; and the remainder's floor is a scalar,
on which the 48 act trivially (1.1). No direction, label, hand or phase
enters the candidate (no (P), no (E), nothing of Z_N), so the two
declared ties of 1.1 (the digital line's axis order, the collision's
Port order) are not touched and no new tie is made.

**The 24 within them.** The self term is a scalar times a scalar; it is
even under the determinant (1.1: a pseudoscalar transforms as h ->
det(g) h; a scalar does not), so the rotations and the reflections act
alike and the hand is not read: the candidate commutes with the group of
order 24 exactly as with the 48, and tells the cosets apart no more than
the massless rule does.

**The translation group and the shape.** The rule commutes with a
translation of the torus (1.6) exactly when the translation is applied
to B as well; a fixed B breaks the torus's translations to the
stabiliser of B, as a declared detector's Node set does (3.1). The
stabiliser of B in the 48: for a cube of side s about its own centre
(a Node for odd s, a cube's centre for even s), all 48; for a square on
a layer, the 16 that fix the layer's axis (the eight of the square's
dihedral group times the flip of the layer's axis, which on the
one-layer world is the identity). This is the world's symmetry, not the
law's: the law's is the 48 (2.8, "generic means exactly commuting with
the 48").

**The result (3): DERIVATION.** The rule with the self term commutes
with every one of the 48, and with the 24, exactly, as the rule without
it does, with the object carried along; no tie is added; the hand is
not read.

---

## 4. The conserved energy with the self term: the added term, its conservation, and its boundedness, which fails on a three-dimensional world

### 4.1 The added term

DESIGN 2.1's E = 3 SUM over Nodes (a_now - a_before)^2 + SUM over Links
(a_now(x) - a_now(y)) (a_before(x) - a_before(y)) is, in the symbols of
0.2, 3 [ <d, d> + <a_now, (1 / 3)(-Lap) a_before> ] with d = a_now -
a_before, since <a, (-Lap) b> = SUM over Links (a(x) - a(y)) (b(x) -
b(y)) (the Laplacian's bilinear form, an identity of the lattice). The
candidate replaces (1 / 3)(-Lap) by **A** (0.2), so its energy is

    E = 3 SUM over Nodes (a_now - a_before)^2 + SUM over Links (a_now(x) - a_now(y)) (a_before(x) - a_before(y)) + 3 (p / q) SUM over the Nodes of B of a_now a_before,

the added term 3 (p / q) times the sum over the object of the product of
the record now and the record one interval ago: the self term's own
strain, on the Node instead of the Link. Its integer form is E_q = q E,
an integer at every interval (the design's factor 3 makes the first two
integers; q clears the pair). (COMPUTATION.)

### 4.2 Its conservation

**Theorem (the leapfrog's invariant).** For the rational form a_next -
2 a_now + a_before = -**A** a_now with **A** symmetric, E_t = <d_t, d_t> +
<a_(t+1), **A** a_t>, d_t = a_(t+1) - a_t, satisfies E_t = E_(t-1) for every
t. Proof in three lines: d_t - d_(t-1) = -**A** a_t; <d_t, d_t> - <d_(t-1),
d_(t-1)> = <d_t - d_(t-1), d_t + d_(t-1)> = -<**A** a_t, a_(t+1) -
a_(t-1)> = -<a_(t+1), **A** a_t> + <a_t, **A** a_(t-1)> by the symmetry of
**A**; and this cancels <a_(t+1), **A** a_t> - <a_t, **A** a_(t-1)>. So E of
4.1 is conserved exactly in the rational form, and with the remainders
kept (verb (D)) to their grain, one amplitude unit per Node per interval
at most, as DESIGN 2.1 states for the massless rule (its 2 x 10^-4 over
200 intervals, COMPUTATION there); the object changes the grain nowhere
(section 2). (COMPUTATION, exact.)

### 4.3 Its boundedness: the one condition

**Theorem (the form's sign).** E = 3 [ <d, d> + <a, **A** (a - d)> ] with
a = a_now is a quadratic form in (a, d) with the block matrix
[[**A**, -**A** / 2], [-**A** / 2, **I**]]; it is positive semidefinite exactly
when **A** - **A**^2 / 4 >= 0 (the Schur complement), that is, exactly when
every eigenvalue of **A** lies in [0, 4]. When it is, E >= 0 bounds every
mode of the record for all time (E is conserved and each mode's share
of it is a non-negative quadratic); when an eigenvalue lambda of **A**
exceeds 4, the mode's characteristic equation z^2 - (2 - lambda) z + 1 =
0 has a real root z with abs(z) = (lambda - 2) / 2 + sqrt(((lambda - 2) /
2)^2 - 1) > 1, at least 1 + sqrt(lambda - 4), the mode grows as abs(z)^t,
its E is negative and unbounded below, and the whole form is indefinite.
This is the design's own remark on the massless rule made exact: the
massless **A** = (1 / 3)(-Lap) has its spectrum [0, 4] on a
three-dimensional periodic world (the eigenvalues of -Lap are 2 sum_a (1
- cos k_a), from 0 at **k** = 0 to 12 at the zone's corner, the
checkerboard), so E is positive-semidefinite exactly at the pair [1, 3]
and the checkerboard is the marginal mode with the repeated root (DESIGN
2.1, "positive-semidefinite exactly at the pair [1, 3]: the mode it does
not bound is the checkerboard"). The self term adds (p / q) chi_B >= 0 to
**A**, so it can only raise the top of the spectrum, and the top is already
at the bound. (COMPUTATION, exact.)

### 4.4 On the design's one-layer world: bounded for 3 p <= 4 q

On the one-layer world (a_U = a_D = a_now) -Lap is the four-neighbour
Laplacian with spectrum [0, 8], so **A** = (1 / 3)(-Lap) + (p / q) chi_B has
its spectrum inside [0, 8 / 3 + p / q], which lies in [0, 4] whenever
p / q <= 4 / 3: BOUNDED for every square of every side and every pair with
3 p <= 4 q, on a periodic or an open layer alike (COMPUTATION, exact; the
design's pins are on such worlds). Above it: the checkerboard restricted
to the square (the sign (-1)^(x + y) on B, 0 off it) has the Rayleigh
quotient <v, **A** v> / <v, v> = 8 / 3 - 4 / (3 s) + p / q (each Node of B
has, of its four neighbours, on average 4 / s outside B), so a square of
side s is UNBOUNDED whenever p / q > 4 / 3 + 4 / (3 s) (COMPUTATION,
exact); the threshold lies between the two. The design's 24 x 24 layer
of DESIGN 2.1 at [1, 3] (p / q = 1 / 3) is inside the bound.
CHECK: a square of side 6 at [1, 3] on a periodic layer of 20 x 20,
seeded with one unit of checkerboard sign on the square, keeps its
largest amplitude between 0.15 and 1.45 units over 400 intervals of
the rational rule (the pure-Python iteration of 0.2's line, floats, no
remainder; the script's formula is 0.2's).

### 4.5 On a three-dimensional world: unbounded for every object on a periodic board, and above a threshold on an open one

**(a) A periodic board.** Let v be the global checkerboard, v(x) =
(-1)^(x + y + z) on every Node of the periodic board (the axes' extents
even, as every registered periodic world's are). Then (-Lap) v = 12 v
exactly, and

    <v, **A** v> / <v, v> = 4 + (p / q) abs(B) / N_board > 4   for every p >= 1,

so the top eigenvalue of **A** exceeds 4 and the candidate is UNBOUNDED on
every periodic three-dimensional world for every object of one Node or
more and every pair with p >= 1 (COMPUTATION, exact, the variational
bound with one test vector). The growth: a mode with lambda >= 4 +
delta_1, delta_1 = (p / q) s^3 / N_board for a cube, grows at least as (1
+ sqrt(delta_1))^t, and the remainder's rounding seeds every mode at
about one unit per interval (DESIGN 2.1's own words on the checkerboard,
"fed by the remainder's rounding"), so the record reaches the amplitude
unit 2^20 from one unit within about 13.9 / sqrt(delta_1) intervals at
most, and faster when the block's own mode of (b) is above the bound.
CHECK, the pure-Python iteration of 0.2's rational line on periodic
boards (the seed one unit of checkerboard sign on the cube; the largest
amplitude reported; the growth factor per interval read from the last
50 or 100 intervals): cube of side 3, 4 and 6 at [1, 3] on 20^3: 1.18,
1.37 and 1.54 per interval, 10^29, 10^54 and 10^75 units by the interval
400; side 2 at [1, 2] on 44^3: 1.05 per interval, 10^13 by 600; side 2 at
[1, 3] on 44^3, side 3 at [1, 6] on 44^3, side 4 at [1, 12] on 44^3 and
side 8 at [1, 100] on 48^3: 1.010, 1.013, 1.012 and 1.007 per interval,
a little above the first-order rate 1 + sqrt(delta_1) of the board's own
global mode (1.006, 1.007, 1.008 and 1.007 at delta_1 = 3.1, 5.3, 6.3 and
4.6 x 10^-5, a lower bound) and far below the isolated block's rates
above, so they confirm (a) and decide nothing about (b).

**(b) An open board (the faces detectors, the record ending there).**
The global checkerboard is not a mode; the question is whether the
block alone lifts an eigenvalue above 4, which by the checkerboard's
sign change (x -> (-1)^(x + y + z) x maps -Lap to 12 - (-Lap) exactly on
the bipartite cubic lattice) is the question whether the well
-(1 / 3) Lap - (p / q) chi_B binds a state below 0. Three exact lines and
one estimate: (i) the checkerboard restricted to the cube has the
Rayleigh quotient 4 - 2 / s + p / q (each Node of B has on average 6 / s
of its six neighbours outside B), so a cube of side s is UNBOUNDED
whenever p / q > 2 / s (COMPUTATION, exact); (ii) a single Node (s = 1)
binds exactly when 3 (p / q) G_0 >= 1 with G_0 = W_S / 2 = 0.758193 the
lattice Green's function of -Lap at the origin, so the one-Node object
is BOUNDED for p / q < 2 / (3 W_S) = 0.4397 and UNBOUNDED above it
(COMPUTATION, exact by Watson's integral); at [1, 3] a single Node is
bounded; (iii) in the continuum estimate of the well (a sphere of the
cube's volume, radius 0.620 s; the bound-state condition of the
three-dimensional well with the kinetic coefficient 1 / 3, (p / q) R^2 >
pi^2 / 12) the threshold is (p / q)_c = 2.1 / s^2 (COMPUTATION, rung 2,
the continuum's form on the lattice's numbers); so at the design's own
pair [1, 3] a cube of side 3 or more is unbounded on an open board too
(2.1 / 9 = 0.23 < 1 / 3), a side of 2 is near the threshold (0.53
against 1 / 3 by the estimate; the CHECK at [1, 2], 0.5, is unbounded)
and only the single Node is inside it. CHECK: a single Node at [1, 3] on
44^3 periodic keeps its largest amplitude below 0.08 units over 600
intervals (the global mode's delta_1 = 3.9 x 10^-6 too slow to show),
consistent with (ii).

**(c) The consequence for the candidate as stated.** On a
three-dimensional world at the pair [1, 3] the self term as written
cannot be built: on every periodic board it is unbounded for every
object, and on an open board it is bounded only for a cube with
(p / q) s^2 below about 2.1, that is mu s < 1.46: a cube less than one
and a half of its own Compton lengths across, which by section 5.3 is
below the size at which it can ring even once. The layer is not
affected (4.4). This is not a fault of the integers or the remainder;
it is the sign of a quadratic form, exact in the rational form, and the
massless rule stands exactly at its edge.

### 4.6 The form within the six verbs that is bounded on every world (this chapter's proposal, not the candidate)

The self term is the mass term of the leapfrog placed on the present
record; the algebra has one other place to put it within the same verbs,
the mean of the record to come and the record before (an implicit
mass), and that form is bounded for every shape and every pair:

    3 (2 q + p) a_next + r' = 2 q S_6 - 3 (2 q + p) a_before + r,   0 <= r' < 3 (2 q + p),        (the pair form)

the design's line with the declared integers (2 q, 3 (2 q + p)) in
place of (1, 3): the same verbs (B) then (D), the same reads, the same
commutation (section 3), the massless Node the value p = 0 again. In
words: a massive Node re-emits the share 2 q / (2 q + p) of what its six
neighbours held, less what it held before, keeping back p / (2 q + p) of
the re-emission, which is (A2)'s "staying share" read on the re-emission
instead of the present record. Its leapfrog is a_next - 2 a_now +
a_before = -**A'** a_now with **A'** = **D**^(-1) **A**, **D** = **I** + (p / (2 q))
chi_B diagonal and **A** the candidate's operator; its energy is

    E = 3 SUM over Nodes (1 + (p / (2 q)) chi_B) (a_now - a_before)^2 + SUM over Links (...)(...) + 3 (p / q) SUM over B of a_now a_before,

the same self term with the motion term heavier on B by 1 + p / (2 q)
(the mass as inertia), conserved by the proof of 4.2 in the inner
product <., **D** .>, its integer form 2 q E; and it is positive
semidefinite for every B and every pair, since <a, **A** a> <= 4 <a, a> +
(p / q) <a, chi_B a> = 4 <a, **D** a> - (p / q) <a, chi_B a> <= 4 <a, **D**
a>, so every generalised eigenvalue of **A** against **D** lies in [0, 4]
and the checkerboard itself is strictly inside (the marginal mode of the
massless rule becomes a bounded one on B). (COMPUTATION, exact.) Its
dispersion: (1 + p / (2 q)) cos omega = 1 - L / 6, that is cos omega =
(1 - (1 / 3) sum_a (1 - cos k_a)) / (1 + p / (2 q)); at second order
omega^2 = c_in^2 abs(**k**)^2 + mu_in^2 with c_in^2 = (1 / 3) / (1 + p / (2
q)) and mu_in^2 = 2 p / (2 q + p): the same mass to first order in p / q,
a pace inside the object slower than c by the factor (1 + p / (2 q))^(-1
/ 2). CHECK: a cube of side 4 at [1, 3] on 20^3 periodic under the pair
form keeps its largest amplitude between 0.39 and 0.87 units over 400
intervals, where the candidate's form reaches 10^54. The pair form is
offered under its own identity for the reviewer's read against the
three tests; it is not the candidate, and the owner's word chooses.

**The result (4): DERIVATION.** The added term is 3 (p / q) times the
sum over the object of a_now a_before, integer as q E; E is conserved
exactly in the rational form and to the remainder's grain with it; it is
bounded below exactly when the spectrum of **A** lies in [0, 4], which
holds on the one-layer world for 3 p <= 4 q and FAILS on a
three-dimensional periodic world for every object and every p >= 1
(and on an open board for (p / q) s^2 above about 2.1, exactly above
2 / s and, at s = 1, above 0.4397). The form of 4.6 is bounded on every
world.

---

## 5. A block of side s with the same pair on every cell, in a massless surround

### 5.1 The self frequency and its period: the closed form, the continuum pace, the lattice correction

For the uniform mode (**k** = 0) of 0.3, cos omega_0 = 1 - p / (2 q) exactly
on the lattice (S_6 = 6 a_now, so a_next = (2 - p / q) a_now - a_before,
whose roots are exp(+- i omega_0)):

    omega_0 = arccos(1 - p / (2 q)) = 2 arcsin(sqrt(p / (4 q))) = mu (1 + mu^2 / 24 + 3 mu^4 / 640 + ...),   mu = sqrt(p / q),
    T_0 = 2 pi / omega_0 = 2 pi sqrt(q / p) (1 - p / (24 q) + ...) intervals,          (COMPUTATION, exact and its expansion)

the continuum's omega_0 = mu (5.3's E_0 = hbar m at **k** = 0, the rest
frequency of the walk) with the lattice's own correction + mu^2 / 24 in
the frequency, the third-order term of 2 arcsin; the mode is bounded
for p / q < 4 (omega_0 = pi at p / q = 4, the period two intervals, the
uniform mode's own edge) but the checkerboard's edge of 4.5 comes first
on a three-dimensional world. The uniform mode's energy: E per Node = 3
A^2 sin^2 omega_0 = 3 A^2 (p / q) (1 - p / (4 q)) for the amplitude A
(COMPUTATION, from 4.1 with a_now = A, a_before = A cos omega_0), the
strain zero (no Link carries a difference), the whole of it motion and
self term. Under the pair form of 4.6, cos omega_0 = 2 q / (2 q + p) and
E per Node = 3 A^2 (1 + p / (2 q)) sin^2 omega_0.

The pace c = 1 / sqrt 3 enters the block's modes through c^2 abs(**k**)^2
(0.3), so a mode of wave-number **k** has omega^2 = p / q + (1 / 3)
abs(**k**)^2 at second order; the lattice's exact line is 0.3, and its
departure from the continuum is at fourth order in the angles, the
anisotropy of 4.2 and 5.1 (ii) (the sum of cosines is not a function of
abs(**k**) beyond the second order), with the same numbers for the pace
by direction as the massless rule's (DESIGN section 6 A). (COMPUTATION.)

### 5.2 The lowest mode of the block, and its extent: a leaking mode, not a bound one

In a massless surround the block's mode is not a bound state: outside B
the dispersion is the massless one, and a frequency omega below the
massive edge would need omega^2 = (1 / 3) abs(**k**)^2 with a real
**k** there, an outgoing wave, never a decaying one. So every mode of the
block radiates into the surround, and "the lowest mode" is the one that
radiates least; its frequency and its decay are one complex number
omega, obtained by matching the interior wave to the outgoing exterior
wave. In one dimension (a slab of width s, the interior even mode cos(k_in
x) matched at x = +- s / 2 to an outgoing exp(i k_out abs(x)), k_out =
sqrt 3 omega, k_in^2 = 3 (omega^2 - mu^2), continuity of the amplitude and
its slope) the matching condition is -k_in tan(k_in s / 2) = i k_out, and
its two regimes are (COMPUTATION, rung 2, the continuum's dispersion of
0.3):

- **A block smaller than about one Compton length** (mu s << 2 c =
  1.15): omega = mu - i c / s + ..., the interior uniform, the amplitude
  draining into the surround in s / c = sqrt 3 s intervals, the time
  light takes to cross the block; for mu s < c = 0.58 the drain is faster
  than one radian of the oscillation and the block does not swing even
  once (overdamped).
- **A block many Compton lengths across** (mu s >> 1.15): the interior
  mode tends to the one that vanishes one Link outside the block (the
  massless surround, whose wavelength 2 pi / (sqrt 3 mu) at the block's
  frequency is much shorter than the block, acts as an open end), so the
  lowest mode is the block's first Dirichlet mode,

      omega_1^2 = p / q + pi^2 / s^2   (a cube: c^2 times 3 (pi / s)^2 with c^2 = 1 / 3),
      omega_1^2 = p / q + 2 pi^2 / (3 s^2)   (a square on the one-layer world),
      T_1 = 2 pi / omega_1 intervals,

  and on the lattice exactly (the first sine mode with the zero one
  Link outside, k_a = pi / (s + 1) on each axis, in 0.3):

      cos omega_1 = cos(pi / (s + 1)) - p / (2 q)   (a cube),   cos omega_1 = 1 - (2 / 3) (1 - cos(pi / (s + 1))) - p / (2 q)   (a square on the layer),

  with the leak rate Gamma (the amplitude's decay per interval), per
  axis, Gamma = 2 pi^2 c^3 / (mu^2 s^3) = 2 pi^2 / (3 sqrt 3 mu^2 s^3)
  (the imaginary part of omega from the matching, to first order in
  2 c / (mu s)); the quality
  Q = omega_1 / (2 Gamma) = 0.132 (mu s)^3 per axis, so the block rings
  for about 0.042 (mu s)^3 periods before its amplitude falls by e; a
  cube leaks through six faces and a square through four, three and
  two axes' worth of the slab's rate in the separable estimate.

**Its extent.** The mode's interior is the block (the first sine mode,
its largest amplitude at the centre, its zero one Link outside); its
exterior is the outgoing wave of wavelength 2 pi / (sqrt 3 omega_1) Links
carrying the leak, which has no finite extent: the mode is the block
plus the record it has radiated. On a board of finite extent the
radiated part reaches the faces (an open board: it ends there as a click,
the block's own record read at the face; a periodic board: it returns
and re-enters, and the block is then not alone). (COMPUTATION, rung 2.)

### 5.3 Whether it oscillates by itself: the self-click without a partner

Yes, in form: the uniform mode of 5.1 is an exact solution of the rule
on an object that fills a periodic world, a_now(t) = A cos(omega_0 t) at
every Node up to the remainder's grain, with no incoming row, no partner
and no lamp; its E is the constant of 5.1 and its phase turns omega_0
per interval, a clock of the place; a block of side s in a massless
surround does the same in the leaking mode of 5.2 and loses the record
to the surround at the rate Gamma. But the two results of section 4 and
5.2 close on the candidate as stated on a three-dimensional world: a
cube that is bounded on an open board has mu s < 1.46 (4.5 (b)), which
is inside the regime where the block swings at most about once and
drains in s / c intervals (5.2's first regime), and on a periodic board
no cube is bounded at all; so under the explicit self term no cube
self-clicks, and the design's DESIGN section 6 A pace check at lambda
>= 12 Links has no massive counterpart there. On the one-layer world the
square rings for any pair with 3 p <= 4 q, with Q = 0.13 (mu s)^3 per axis
in the estimate: a square with mu s = 5 rings for about five periods,
with mu s = 10 for about forty. Under the pair form of 4.6 the cube rings
as the square does, for every pair. (COMPUTATION; the self-click's
reading as a detector's own count is a declaration, section 6.)

### 5.4 The member it reads in motion: the clock's ratio at one Link every k intervals, k = 3

**What moves.** The pair is the Node's (section 1); no verb of the six
carries a Node's pair, and no verb of the candidate carries the record's
amplitudes with a shape that hops (a body hops by the drive (T) on its
own place, 2.1; a row flies by the flight (T) on its line; the
amplitudes a_now, a_before are the Node's row). So "in motion" means, in
the structure as given, a record moving through a region of Nodes that
carry the pair, as a wave packet at the group pace of 0.3's dispersion;
an object whose Nodes hop is a declaration (section 6).

**The clock of a moving packet, on the lattice exactly.** Along an axis,
0.3 reads 2 - 2 cos omega = (2 / 3) (1 - cos k) + p / q, the group pace v
= d omega / d k = sin k / (3 sin omega) Links per interval, and the phase
of the packet at its own centre advances at omega - k v per interval (the
phase k x - omega t along the world line x = v t). The clock's ratio,
the moving record's own count per interval against the rest record's
(3.3's r, "to be found or measured, never assumed"), is then

    r = (omega - k v) / omega_0 = (omega - k sin k / (3 sin omega)) / arccos(1 - p / (2 q)),         (COMPUTATION, exact on the lattice's dispersion)

and at second order in the angles, with omega^2 = k^2 / 3 + mu^2 and v =
k / (3 omega),

    r = mu^2 / (omega omega_0) = sqrt(1 - v^2 / c^2) = 1 / gamma,   c^2 = 1 / 3,          (rung 2)

Lorentz's rate as the thing compared with: the invariant of the
dispersion, omega^2 - c^2 k^2 = mu^2, is what 5.1 (ii) calls the
covariance of the walk to second order, and the phase rate at the
packet's centre is its own clock. At v = 1 / 3 (one Link every k = 3
intervals), v^2 / c^2 = 1 / 3 and

    r = sqrt(2 / 3) = 0.8165,   gamma = sqrt(3 / 2) = 1.2247,   k = mu sqrt(3 / 2) per Link, omega = mu sqrt(3 / 2) per interval          (COMPUTATION),

against the law's two rates for one record of 5.6 (c): the clock's 1 in
no crowd and the drive's 1 - v = 0.6667 at k = 3. The self term
supplies, for a record that moves as a wave in the pair's medium, the
one line the click theorem leaves free (5.1: "LORENTZ FROM THE CLICKS
GIVEN the line k_AB = k_BA, which is r^2 = 1 - v^2"), because the self
term is (A2) built (section 1) and 5.1 (ii) is what (A2) gives.

**The caveats, the algebra's own.** (i) No boost is among the 48 (1.3
item 2; 7 (ii)): the operator **A** does not commute with any boost, and
the covariance is of its dispersion at second order in the angles,
failing from the fourth order on with the lattice's anisotropy (5.1
(ii), "beyond second order in the angles the covariance fails"); the
ratio 0.8165 is the small-angle value, and a packet at k = mu sqrt(3 /
2) is in that regime only when mu is small (mu^2 = p / q << 1) and its
wavelength 2 pi / k = 5.13 / mu Links fits inside the object, so a block
that carries a moving massive record is at least that long. (ii) The
ratio is a reading between clicks Outside (3.2): the packet's phase
steps per the detector's own count, mode D's fix of 6.1 ("the row's
phase turning per Link ... and the click reading the phase steps per
its own count"); on the board it is the GAMEBOARD arithmetic above. (iii)
Under the pair form of 4.6 the same holds with c_in in place of c: r =
sqrt(1 - v^2 / c_in^2), a pace inside the object slower than light's by
(1 + p / (2 q))^(-1 / 2), so at k = 3 the ratio is sqrt(1 - (1 + p / (2
q)) / 3), a departure of relative order p / (8 q) from 0.8165 (COMPUTATION).
(iv) The hopping object, its record carried with it, is NOT REACHABLE
from the structure: which verb carries the amplitudes at a hop ((T) on
the rows along the Link, or (P) of the rows onto the next Node) and what
the pair does during the hop are declarations (section 6), and the
ratio they give is not derived here.

**The result (5): DERIVATION** for the frequency, the period, the
extent, the self-oscillation and the moving packet's ratio, each under
the regime named (the lattice exact where stated, the continuum rung 2
where stated); NOT REACHABLE for the hopping object's ratio.

---

## 6. What the structure does not give: the declarations for the object to interact with light

The candidate's rule acts on "the record's own row at the Node" (DESIGN
section 2), and the algebra's rows of two families at one Node are two
elements, not one (2.3: the merge adds identical rows; light's record
and the object's are not identical rows). So the structure with the self
term gives the object its own record, its rest frequency and its
symmetry, and gives it no way to meet light. Each of the following is a
DECLARATION, named and not filled here:

1. **The coupling of the massive record to light's record.** A term
   read by the object's rule from light's row at the Node, or by light's
   rule from the object's, is a bilinear form (B) with a declared
   coupling matrix between the two records' amplitudes (2.2's **r** =
   **C** **a**, the coupling over declared columns), or a declared merge (G)
   if the two are declared one record; which verb, with which declared
   integers, in which direction (light acting on the object, the object
   on light, or both), and whether the object's own rest oscillation
   enters light's rule as a source (a lamp of the object's frequency,
   5.7's E = h f at the release, 4.11) or only as a sink (a click, 3.1).
   The dictionary's "light and matter: rows of a paid family and a free
   family's rows with bodies" (1.2) does not name it.
2. **The push of light's stress on the object's momentum.** The object
   as declared has no momentum: **p** in Z^3 is a body's (1.2, "momentum
   of a body"), moved by the push (B) and read by the drive (T); a set of
   Nodes with a pair has neither. To be pushed the object needs (a) a
   momentum vector of its own, declared, in label units, one for the
   shape (not per Node, since a Node does not move); (b) the push: the
   bilinear form of light's stress at the object (the strain part of E
   of 4.1 on the Links that cross the object's boundary, or the flow
   vector **a** of light's rows arriving at B's Nodes, 2.2) times a
   declared matrix, giving the rate of that momentum; (c) the drive:
   the object's shape hopping by (T) then (D) against a declared wall
   from that momentum, with (d) the carry of the record's amplitudes
   and the pair with the hop (5.4 (iv)). Each of (a) to (d) is a
   declaration; together they make the object a body whose extent is
   the shape, which the structure does not contain.
3. **The shape and the size.** The set B, its side s, its layer or its
   cube, its place on the board, and the pair [p, q] on it: world data
   (section 1), declared per world, and the object's rest frequency and
   its ringing follow from them by section 5 once declared.
4. **The reading.** Which count of the object is its own count for the
   reading rule (3.2): the zero crossings of its record, a rung of its E
   at a face of B, or a detector declared on it; the candidate's
   self-click is a reading only under such a declaration.

**The result (6): DECLARATION**, four items, none filled.

---

## 7. The table: each result, its kind, its ALGEBRA.md formula, and its status

| Result | Kind | The ALGEBRA.md formula it came from | Status |
| --- | --- | --- | --- |
| The candidate is the design's leapfrog with **A** = (1 / 3)(-Lap) + (p / q) chi_B (0.2) | COMPUTATION | 2.1, 2.3, 2.6 (the verbs of the design's line); DESIGN 2.1's leapfrog | derivation |
| The massive dispersion 2 - 2 cos omega = (2 / 3) sum (1 - cos k_a) + p / q; omega^2 = c^2 k^2 + mu^2 at second order (0.3) | COMPUTATION | 4.2 (c = 1 / sqrt 3); 5.3 (omega^2 - kappa^2 = m^2); 5.1 (ii) | derivation |
| (1) Not a new group object: a declared scalar of the Node, the 48 trivial on it; the mass row's element (the mass angle m^2 = p / q) on the place, not the body; the shape world data, the rule law with the pair a value | COMPUTATION | 1.1 (the action on scalars); 1.2 (the mass row); 2.10 (the declared input); 1.6 (chosen per world); 2.8 (values, not branches); 5.1 (A2) | derivation |
| (2) The self term is (B) with the declared row (q x 6, -3 q, -3 p), then (D) by 3 q with r' in [0, 3 q) on the row, (T) carrying r; the floor against the truncation a build's convention | COMPUTATION | 2.2 (B); 2.6 (D); 2.1 (T); 2.7 (nothing of the seventh verb) | derivation |
| (3) V_(g B)(g . s) = g . V_B(s) for all 48; commutes with the 24 alike; no tie; the hand not read; the stabiliser of B the world's symmetry | COMPUTATION | 1.1 (the 48 on Ports, Nodes and scalars; the two ties); 4.5 (Theorem 1); 1.6 (the torus) | derivation |
| (4a) The added energy term 3 (p / q) SUM_B a_now a_before; E_q = q E an integer | COMPUTATION | DESIGN 2.1's E; 2.2 (the bilinear form of the Laplacian) | derivation |
| (4b) E conserved exactly in the rational form, to the remainder's grain with (D) | COMPUTATION | 2.6 (the remainder's bound); DESIGN 2.1 | derivation |
| (4c) E bounded below iff spec(**A**) in [0, 4]; the layer bounded for 3 p <= 4 q, unbounded above 4 / 3 + 4 / (3 s) | COMPUTATION, CHECK | 4.2 (the spectrum of the flight operator's Laplacian); DESIGN 2.1 (the checkerboard at the edge) | derivation |
| (4d) A three-dimensional periodic world: unbounded for every object and every p >= 1, top eigenvalue >= 4 + (p / q) abs(B) / N_board | COMPUTATION, CHECK | the same; 1.6 (the periodic torus) | derivation (refutes the candidate's boundedness there) |
| (4e) An open three-dimensional world: unbounded for p / q > 2 / s exactly; at s = 1 the threshold 0.4397 exactly (Watson); the estimate (p / q)_c = 2.1 / s^2 | COMPUTATION (exact; rung 2 for the estimate), CHECK | the same; 3.1 (the face a detector) | derivation; the estimate rung 2 |
| (4f) The pair form 3 (2 q + p) a_next + r' = 2 q S_6 - 3 (2 q + p) a_before + r, bounded on every world, the same verbs | COMPUTATION, CHECK | 2.2, 2.6; DESIGN section 2's line with declared integers | this chapter's proposal under its own identity, not the candidate |
| (5a) omega_0 = arccos(1 - p / (2 q)) = mu (1 + mu^2 / 24 + ...), T_0 = 2 pi / omega_0; E per Node 3 A^2 sin^2 omega_0 | COMPUTATION | 0.3 from 4.2 and 5.3 | derivation |
| (5b) The block's lowest mode a leaking one; omega_1^2 = p / q + pi^2 / s^2 (cube), p / q + 2 pi^2 / (3 s^2) (square), the lattice's cos omega_1 = cos(pi / (s + 1)) - p / (2 q); the leak 2 pi^2 c^3 / (mu^2 s^3) per axis, Q = 0.132 (mu s)^3; the extent the block plus the radiated wave | COMPUTATION | 0.3; 4.2 (c); 3.1 (the face) | derivation, rung 2 (the matching in one dimension; the lattice line exact for the Dirichlet mode) |
| (5c) It oscillates by itself in form; under the candidate no cube self-clicks on a three-dimensional world (bounded only below mu s = 1.46, the overdamped regime); the square on the layer rings; the pair form's cube rings | COMPUTATION | 4.5, 5.2 above; 5.1 (A2) | derivation |
| (5d) The moving packet's clock r = (omega - k v) / omega_0 exact on the dispersion; r = sqrt(1 - v^2 / c^2) at second order; 0.8165 at k = 3 against the law's 1 and 0.6667 | COMPUTATION | 5.1 (ii) (the walk's covariance to second order); 3.3 (r, k_AB, k_BA); 5.6 (c) (the three rates); 6.1 mode D | derivation, rung 2; the lattice's departure at fourth order stated |
| (5e) A boost is not among the 48; the covariance is the dispersion's, not the operator's | COMPUTATION | 1.3 item 2; 7 (ii); 5.1 (iii) | derivation (the caveat) |
| (5f) The hopping object's clock ratio, its record carried with it | none | 2.1 (T on a body's place; no verb on a Node's pair) | not reachable; a declaration (6.2 (d)) |
| (6.1) The coupling of the massive record to light's record | DECLARATION | 2.2 (B), 2.3 (G); 4.11; 3.1 | declaration, not filled |
| (6.2) The object's momentum, the push of light's stress, the drive of the shape, the carry at the hop | DECLARATION | 1.2 (momentum of a body); 2.2 (the push); 2.1 (the drive) | declaration, not filled |
| (6.3) The shape, the size, the place, the pair | DECLARATION | 1.6; section 1 | declaration, not filled |
| (6.4) The object's own count for the reading rule | DECLARATION | 3.2 | declaration, not filled |

**In one line for the Boss.** The foreign object is not a fifth group
object but a declared scalar of the Node, the mass angle of the record
on that place, exactly (B) then (D), commuting with the 48 and the 24
as the massless rule does; its energy term is 3 (p / q) SUM_B a_now
a_before, conserved; and the candidate as written is unbounded on every
three-dimensional periodic world because the massless rule at [1, 3]
already sits at the edge of its own energy's positivity, so the self
term must sit on the mean of the next and the previous record (the pair
form of 4.6) to be bounded, which the reviewer's read and the owner's
word decide.
