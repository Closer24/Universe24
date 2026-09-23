# The massive record kind and the foreign object as a block: closed from the algebra before the board (the third draft)

The chief physicist's design of 2026-09-23 on the model owner's words, under
the key `massive-record-v1`, OFF by default; docs and printed computations
only; no build. It stands beside [DESIGN.md](DESIGN.md) (the massless kind,
light, unchanged) and [PINS.md](PINS.md). The algebra of the push, the boost
and the gate of this design is Reviewer 3's `PUSH_BALANCE.md`
(docs/designs/detector_law/ on `push-balance-r3`, PR #1043): its sections 10
and 11 at 6d7a03b5, 60509e9a and d9227352, its section 12 at bb43ef41 and
f5752667, its 12.5 at 198a9bfe and its 12.6 at f089736f, and its 12.7 (his gate of
7022428c, AGREED WITH SIX MUSTS, at 03a2ba665b6df033ee5d14452ff96a4a6bb6b1a8
on `push-balance-r3`, PR #1043); cited by those
SHAs, never rewritten. The six MUSTs are folded below (sections 1, 4, 7, 9,
10, 13 and `massive_c_derivation.py`). Every number here is a COMPUTATION from the rule, written
before the board runs it, and printed by a script beside this document (the
list in section 12); the board, when it runs, checks the algebra, never the
reverse. The third draft replaces the first two whole: the massive rule is
the stable form (section 1), the pace c is derived (1.1), the object is the
well of the pair on declared cells in the massive medium (4), the click is light
passing through a body with a clock (6), the coupling is the dielectric
(7), the motion is one statement (8), the pins are one table (9), and the
board's faces have a margin rule (11).

## 0. The owner's law and words

- (12:50Z, to the chief physicist) "Stop all the runs that try to find all
  sorts of pins; close everything from these algebraic assumptions and
  implement them on the board. The law: **we go from the algebra to the
  computation on the board, and not from the computation on the board to
  the algebra.**"
- (12:28Z, record 1385) One big generic law, physical, algebraic and
  vector; a foreign object a SQUARE block of cells (3 x 3, 12 x 12, always
  square; a cube on the board), easy to place.
- (12:15Z, record 1381) Direction (ii): a second record kind, massive,
  beside the massless kind that light is; to close all its ends, including
  the algebra that follows from our own formulas.
- (12:10Z, record 1370) A detector is one cell from outside holding many
  cells inside it, on the board, by locality; the cells produce its
  frequency at rest; there a real clock can be defined; its click in the
  Outside is read across its cells.
- (13:05Z) "There is something we do need to take from the algebra, and it
  derives itself, and I do not need to decide": the motion is derived, not
  decided (section 8).
- (12:35Z) "Derive everything algebraically, then implement in the engine
  to check; a foreign object is a kind of group object like the rest."
- (about 14:20Z, through the chief physicist) "A foreign object is a CUBE
  in the Inside that produces CLICKS in the Outside."
- (about 13:50Z, his sentence for Highlights, the Boss to enter) "Light
  cannot be a body, but every body reads light." (Section 4: no lump of
  light holds itself, an exact never; section 6: a click is the body's.)
- (about 13:40Z) "Is everything clear from here: to take the algebra to the
  board and to prove that the physics stands in reality?" Yes: this draft,
  then the build on his word, then runs against DETECTOR pins only.
- (14:08Z, record 1414, on the click) "The click is in the Outside, and
  light definitely produces it. The click is the evaluation E of the
  record's time series on the foreign object's cells at the declared wheel
  W. The whole detector law of today is built on this: the two slits,
  Malus, Bell, all clicks of light. And how does light click without being
  bound: through the coupling. Light drives the foreign object's record at
  the cell (the receive, a_m += g a_l), the object's record crosses the
  rung 1 / W in its own clock, and that is the click. Light does not need
  to stay in order to be read. It needs only to pass through a body that
  has a clock." (Sections 6 and 7: the click needs no sink.)
- (14:12Z, on the board's faces) "Check whether I understood that a foreign
  object cannot now be placed at the edge of the board because it will not
  be held there; check only that, and how it is most convenient to solve
  it: a closed board, an open board as we use, or periodic as we do in Z."
  (Section 11: the margin rule.)

## 1. The one rule, in the stable form: the pair on the six-neighbour term

The interval's map at every Node, on a record's row `(a_now, a_before, r)`,
with the record's declared pair `[num, den]` on the six-neighbour term
(`[1, 1]` for light; `den > num` for a massive record):

    3 den a_next + r' = num (a_E + a_W + a_N + a_S + a_U + a_D)
                        - 3 den a_before + r,        0 <= r' < 3 den

(form (B) of Reviewer 3's 12.6 (c), DESIGN.md 4.1's words: the pair on the
six-neighbour term ALONE, uncompensated, no self term). At `[1, 1]` it is
DESIGN.md section 2's rule bit for bit. The three tests: generic (one
primitive, one declared pair, no family name; light is the value `num =
den`); vector (one entry of verb B's declared matrix on the six neighbours,
verb T the translation of the accumulator, verb D the division by `3 den`
with the remainder kept; no root, no float); local (the record's own row
and its six neighbours; nothing kept at a Node). PASS, PASS, PASS.

**What the pair is.** The characters (section 2) have the gap `cos omega_0
= num / den` at k = 0: the mass of the record IS the pair, the rest energy
h omega_0. The second draft's self pair `[p, q]` maps to it as `den / num =
1 + p / (2 q)` (the same gap to second order); the self-term form itself,
`3 q (a_next + a_before) = q SUM6 - 3 p a_now`, is WITHDRAWN for the board
(section 3: it grows at the checkerboard corner in three dimensions).

**The one primitive** (Reviewer 3's 12.6 (c)): light's index form of
DESIGN.md 5.1 (b) is this same pair WITH the compensation `6 (den - num)
a_now`, which restores the zero mode (the same pace, no gap: an index); the
massive record is the same pair WITHOUT it (a gap: a mass). The
compensation is exactly the difference between an index and a mass; (B) is
the ONE-PAIR form (the edge form (C) of section 2 is the two-coefficient
one, named and not carried).

**Three derivations, one rule.** The Algebra Mathematician's chapter,
written from ALGEBRA.md alone (`docs/ALGEBRA_MASSIVE_RECORD.md` on
`algebra-massive-record` at 4d2f7289), finds the compensated self term
unbounded on every three-dimensional periodic world for every p >= 1 (his
4.5) and proposes the self term on the MEAN of the record to come and the
record before, `3 (2 q + p) (a_next + a_before) + r' = 2 q SUM6 + r` (his
4.6, with its energy positive semidefinite for every shape and every
pair): the rule above with `[num, den] = [2 q, 2 q + p]`, Reviewer 3's form
(B), and this design's stable form, reached three ways. (His one-Node
threshold 2 / (3 W_S) = 0.4397 carries a factor 3 from the Green's
function's normalisation; the threshold is 1.319, this design's 1.3206 in
section 4; none of his conclusions moves. His to fix, in his file.)

**The algebraic placement of the Inside** (the owner's 14:30Z question: how
does the algebra see the ray that splits by itself). A record on the board
is one element of the group algebra Z[Z^3] of the torus's translations (a
finite integer combination of Node translations, ALGEBRA.md 1.6); the
interval's map is multiplication by ONE element of that algebra, h = (1 / 3)
SUM over the six Ports [e], the unique 48-invariant element of range 1 with
no self term, in the second-order form `3 (a_next + a_before) = SUM6` (verbs
B, T, D); the split of the ray at every free Node IS this product, the
amplitudes are the coefficients, and the remainder is verb D's. The
characters of Z^3 diagonalise h into the dispersion surface (section 2);
the click is the evaluation E of a body's record at the clock's character
(section 6). The massive record differs from light by the pair on h alone.

**The algebraic placement of a foreign object** (DESIGN.md's dictionary,
GROUP_STRUCTURE.md sections 1 and 8; Reviewer 3's C1 to C4 at bb43ef41
agreed): no new group and no new verb. A foreign object is (i) a finite
set R of Nodes, a G_48-set (its shape group the stabiliser of R; a cube is
the 48's own shape, a square on a layer the stabiliser of the layer's
normal), DECLARED as world data, like a wall's placement; (ii) the same map
on R with the object's pair on the six-neighbour term (a well of the pair,
section 4); (iii) its clock the bound mode of the map, its frequency
omega_b a CHARACTER of the time translation at k = 0, one element of
Z[Z_N] carried by all its cells in step; light has no such character at k =
0 (its zero mode is a level, not a clock): the whole difference between
light and a foreign object in the algebra is a gap; (iv) its motion the
characters (omega, **k**) on the surface of section 2, the rest object at
**k** = 0; (v) its momentum the existing **p** in Z^3, the step the existing
verb T, the push the stress at its Ports; (vi) its click the evaluation E
across R.

**In ALGEBRA.md's terms**, one line per sentence of this design:

| Sentence | ALGEBRA.md object or map | The dictionary's row |
| --- | --- | --- |
| the pair [num, den] on the six-neighbour term | chapter 2.2, (B) one entry of the declared matrix on the six neighbours' present records; 2.1 (T); 2.6 (D) the division by 3 den with the remainder kept | NEW ROW: **mass of a foreign object**: the pair [num, den] of its record's rule; the rest frequency omega_0 = arccos(num / den) on the circle; the rest energy h omega_0; the content M = E'_0 / (Q S) of the existing row read from it, not declared beside it |
| the pace c | chapter 7 (iii) and the row "the speed of light c", extended by section 1.1: c^2 = 1 / 3 also from the rule's second moment | c: forced by the absent self term in the 48-invariant family; the Manhattan road the same count; the value in m/s a CONVERSION |
| the block R | chapter 1, the translation group of the torus acting on Nodes; R a finite G_48-set | shape: a declaration (kind 1), as a wall's placement |
| the block's clock | chapter 1, the phase circle Z_N and its group ring Z[Z_N]: one element carried by the cells of R in step; the bound mode of the interval's map; a character of the time translation at k = 0 | time, a clock: the block's own count of its mode's cycles |
| the motion | the characters (omega, **k**) on the surface of section 2; the boost a relation on the characters, not among the 48 | Lorentz: reached as a relation on the characters (no boost among the 48) |
| the momentum and the step | chapter 2.1, (T) the drive: **p** in Z^3; the accumulator per axis against 3 Q S M x 56 d, the remainder kept; per block one integer, a declared tie (Reviewer 3's C11) | momentum of a body (unchanged) |
| the push | chapter 2.2, (B): the stress T_ii = 3 (motion)^2 + (strain)^2 at the outer Ports | force, the push: the stress at the Ports |
| the click | chapter 2.5, (E) the evaluation of the block's element of Z[Z_N] across R; the wheel W declared | a measurement: a click at a body |
| the coupling to light | chapter 2.2, (B): an entry over the other record's two columns (now, before) at the same cell, one declared g with G (section 7) | the dielectric: the index and the source of a body's light |
| the conserved form I | chapter 4's identities: the leapfrog's quadratic form, positive definite for den > num (section 3) | energy: I the record's; E'_0 = Q S M read from omega_0 |

### 1.1 Where c comes from: derived, not declared (COMPUTATION, `massive_c_derivation.py`)

The 48-invariant local rules of range 1, second order and reversible in
time, are `a_next + a_before = w SUM6 + s a_now`: two numbers, w on the six
neighbours and s on the Node itself. Their characters are `2 cos omega = s
+ 2 w SUM cos k_i`. Three inputs, and no more:

1. **Locality with the 48.** The six neighbours enter with one weight
   (the 48 leave one element of range 1 on them), and their second moment
   is a multiple of the identity (SUM **e** **e**^T = 2 **I**), so near k =
   0 the pace is ONE number in every direction: c^2 = w (checked on five
   directions, 0.57735 each at w = 1 / 3).
2. **The zero mode.** The uniform record is a solution (light is massless:
   the definition of light's record, not a law) iff s = 2 - 6 w: a
   one-parameter family with c^2 = w in (0, 1 / 3], stable while w <= 1 /
   3 (the corner 2 - 12 w >= -2).
3. **The absent self term.** s = 0 picks w = 1 / 3 in that family ("the
   rule has no coefficient but 3", DESIGN.md section 2: the design's own
   declaration), and it is the same point as the stability edge (the
   maximal pace) and the corner's double root.

So c^2 = 2 / 6 = the two time Ports over the six space Ports, c = 1 / sqrt
3 Links per interval; the world's pair `c2 = [1, 3]` is that consequence,
not a free constant. NOT circular: no input uses c. Not two inputs but
three (Reviewer 3's 12.6 (a)): without the third, c^2 = w < 1 / 3 with a
positive self term is a lawful massless record too, an index. The Manhattan
road (P9, the flight operator's norm: one Link per interval spread over
three axes, ALGEBRA.md 4.2 and chapter 7 (iii)) is the SAME COUNT (in d axes
both give 1 / sqrt d), a check of the counting and not an independent
derivation. Light's group pace over the whole zone never exceeds c (the
maximum 0.577350 on a 61^3 grid, at k -> 0). The value in metres per second
is a CONVERSION (the Link's length, the interval's duration). The index of
a foreign object is the one departure the family allows for light: w = num
/ (3 den) with s = 2 - 6 w, the pace c / n, n^2 = den / num (checked at [2,
3] and [1, 2]).

## 2. The dispersion surface, the gap, the pace of a massive record (COMPUTATION, `massive_corner_stability.py`)

The characters (omega, **k**) of the rule of section 1:

    2 cos omega = (2 num / (3 den)) (cos k_x + cos k_y + cos k_z),

within [-2 num / den, 2 num / den] for every **k**: stable for every pair.
In the lattice's own variables it is exactly relativistic (Reviewer 3's
12.6 (d)): `4 sin^2(omega / 2) = 2 (1 - num / den) + (num / den) (4 / 3) SUM
sin^2(k_i / 2)`, light's form with the pace `c_m^2 = (num / den) c^2 = cos
omega_0 c^2`. At **k** = 0 the gap `cos omega_0 = num / den`, the rest
period N_0 = 2 pi / omega_0 in intervals:

| the second draft's [p, q] | [num, den] (den / num = 1 + p / 2 q) | omega_0 (lattice) | N_0 intervals | c_m / c = sqrt(num / den) |
| --- | --- | --- | --- | --- |
| [1, 64] | [128, 129] | 0.1246 | 50.4 | 0.9961 |
| [1, 16] | [32, 33] | 0.2468 | 25.5 | 0.9847 |
| [1, 4] | [8, 9] | 0.4759 | 13.2 | 0.9428 |
| [1, 1] | [2, 3] | 0.8411 | 7.5 | 0.8165 |

**The pace of a massive record is below c on the lattice, by order
omega_0^2**: c_m = c sqrt(cos omega_0), 0.39 percent below c at N_0 = 50,
3.0 percent at N_0 = 18, the same c in the limit num / den -> 1. This is
range 1's, not form (B)'s (Reviewer 3's 12.6 (d)): for every 48-invariant
rule of range 1 with a gap, c_m^2 / c^2 <= cos^2(omega_0 / 2); NO such rule
gives a massive record light's c in three dimensions; the least deficit,
omega_0^2 / 8 in c, is the edge form (C), `12 q (a_next + a_before) = (4 q -
p) SUM6 - 6 p a_now`, marginal at the corner as light is, named for the
record and not carried. (B) is the one-pair form, strictly inside, and the
design. What the deficit touches: the massive record's characters are
Lorentz's with c_m and light's with c, so a well's mode boosted reads 1 /
gamma at beta_m = beta_c c / c_m: at k = 3 and N_0 = 50, 0.8149 against
0.8165, 0.2 percent, inside five's band and under the pins' grain (one
interval on 206). A TWO-PACE WORLD at second order in omega_0 is a
PREDICTION of the model, stated here as such, no pin moved (section 9).

The floors of DESIGN.md 1.2 apply to N_0: the band's top (N >= 6), the
honest floor N >= 21 (den / num <= 1.047). Nothing else names the mass.

## 3. The conserved form, the corner, and why the chains were blind (COMPUTATION, `massive_corner_stability.py`)

For `a_next + a_before = M a_now` with **M** symmetric the form

    I = a_next . a_next + a_now . a_now - a_next . M a_now

is conserved, and positive definite exactly when **M**'s eigenvalues lie
strictly inside (-2, 2), which the rule of section 1 satisfies for every den
> num (Reviewer 3's 12.6 (c); light itself, den = num, sits at both ends,
semidefinite, its corner and its zero mode the null directions, DESIGN.md
2.1). In the engine's units: `3 den (a_next^2 + a_now^2)` summed over the
Nodes less `num (a_next,i a_now,j + a_next,j a_now,i)` summed over the Links,
conserved up to the remainders' bounded jitter. With a well (a per-Node pair
`[num_i, den_i]`, section 4) the same identity holds with `den_i / num_i` per
Node, positive definite while the mode's `2 cos omega_b < 2`. The norm the
rungs divide is I; the Port's factor of DESIGN.md 2.1 applies with the
pair's share named. The second draft's E_m is replaced by I.

**The contradiction the second draft carried, and its correction.** The
self-term form (A), `3 q (a_next + a_before) = q SUM6 - 3 p a_now` (the
second draft's section 1, Reviewer 3's 8.7, 11.1 and C2), has at the
checkerboard corner `2 cos omega = -2 - p / q`, below -2 for every p > 0: a
growing checkerboard, acosh(1 + p / 2 q) per interval, 0.125 at [1, 64]
(a one-unit seed on a 2^20 record reaches 3.8 x 10^10 in 200 intervals on a
6^3 periodic box) and 0.352 at [1, 8]. The second draft's section 3 said
the opposite ("the checkerboard oscillates at the band's top"), wrong in
sign: the mass term lifts the whole band, so the corner leaves it. The
reason is the edge: light at w = 1 / 3 already has its corner at -2, and
any self term of the mass's sign pushes it over. WITHDRAWN for the board
(Reviewer 3's 12.6 (b)). In one and two dimensions the corner sits at 2 / 3
- p / q and -2 / 3 - p / q, inside the band: every chain and layer reading
of this design and of PUSH_BALANCE.md sections 8, 10, 11 and 12 stands, and
the map `g = 2 (num' / den' - num / den)` carries them into form (B) to
1.5 percent in the binding depth at s = 1 and better for a block (his 12.6
(e): eps 0.0983 against 0.0998 at s = 1, 0.0575 against 0.0573 at s = 12).

## 4. The foreign object as a block: the well of the pair on declared cells

The massive record kind's rule runs at EVERY Node its rows reach (rows
created as the record spreads, as light's), with the background pair
`[num, den]` the KIND's declaration in the world file (its rest mass, the
medium's gap mu, as light's family has its clock). The object is a block R
of side s (a square on a layer, a cube on the board), DECLARED as world
data like a wall's placement (the owner's cube; Reviewer 3's C4 and 12.5
(c)), every cell of R carrying a LOWERED pair `[num', den']` with `num' /
den' > num / den` (a WELL of the pair in that medium; `g = 2 (num' / den' -
num / den)` its depth to first order, mu^2 = omega_0^2 the outside's gap). The object's record is the bound mode of the
map in that well; ITS CLOCK IS THE MODE (omega_b, a character at k = 0;
the owner's 12:10Z); its extent is the mode's, a COMPUTATION from the
pair and the side, never a declaration in motion (the owner's 13:05Z).

**The two regimes** (Reviewer 3's C6 at bb43ef41; the chain's H, the
continuum's finite well `k_in tan(k_in s / 2) = kappa`, agreeing to 0.1
percent), by the side against the one-Node extent 2 / (3 g):

- the WELL regime, s small against 2 / (3 g): the mode extends far beyond
  the cells, its frequency near the gap's, the binding depth eps = 1 -
  omega_b^2 / mu^2 small; its clock in motion is Lorentz's to first order
  (section 8), and eps <= 0.1 keeps it inside five's band;
- the CAVITY regime, s comparable or larger: the mode sits inside the
  cells, its frequency the block's own standing wave; its clock in motion
  is the medium's (section 8).

**The cube's exact threshold on the infinite board** (COMPUTATION,
`massive_cube_threshold.py`; no box): at the band's top the bound mode obeys
`(2 - L / 3) a = (g / D_out) a` on the cube, so a mode binds iff g exceeds
`g_c(s) = D_out / Lambda(s)`, with Lambda(s) the largest eigenvalue of the
massless lattice Green's function `G_0 = (2 - L / 3)^-1` restricted to the
s-cube (the Bessel form `G_0(r) = INT PROD ive(r_i, 2 t / 3) dt`; `G_0(0) =
W_3 / 2 = 0.758193`, Watson's integral, met to 6 digits) and D_out = 1 +
mu^2 / 2:

| side s | g_c(s) at mu = 0.05 | g_c(s) s^2 | Reviewer 3's sphere with R = s / 2, g R^2 >= 0.822 |
| --- | --- | --- | --- |
| 1 | 1.3206 | 1.32 | (his one-Node 1.319: met) |
| 3 | 0.2245 | 2.02 | 3.29 |
| 12 | 0.01513 | 2.18 | 3.29 |
| 24 | 0.00380 | 2.19 | 3.29 |
| 36 | 0.00169 | 2.19 | 3.29 |
| 60 | 0.00061 | 2.19 | 3.29 |

The cube's constant is `g_c(s) s^2 -> 2.190` (converged to 0.1 percent by s
= 20): the sphere's bound is 20 percent too demanding in the side. The
smallest side that binds, the inside's gap reduced and not reversed (g <=
mu^2): mu = 0.05: s = 30 at g = mu^2, s = 42 at g = mu^2 / 2; mu = 0.15: s =
10 at g = mu^2, s = 14 at g = mu^2 / 2. (A scratch box scaling with zero
faces to 96^3 read "side 36 at the threshold": the box's confinement hid a
weakly bound mode, HISTORY, superseded by the exact table.)

**The reversed-mass window** (the owner's allowance, if wanted): a small
block binds only with the inside's gap reversed (num' > den'), and then
inside a window: for a 12-cube at mu = 0.05, bound for g > g_c(12) =
0.01513 (mu_in^2 = -0.0126) and GROWING for g > g_tach(12) = mu^2 + 1 /
Lambda(12) = 0.01761 (the mode's omega_b reaches 0; by the checkerboard
symmetry S L S = -L the spectrum of form (B) is symmetric, so the corner
mode leaves the band at exactly the same g: one ceiling); the window's
width `mu^2 (1 - 1 / (2 Lambda))` = 0.00248, about mu^2, narrow. Lawful
inside the window in form (B); the design's default is the reduced gap and
a side above the threshold.

**The three forms of the earlier drafts, with their standing now:**

- **(I) The block's faces as mirrors for its own record** (a declared
  cavity): the modes of a box of s cells with Dirichlet faces, k_i = pi /
  (s + 1); the lowest mode's frequency at [1, 1] on the massless surface:

  | s | a square on a layer: omega, N | a cube: omega, N | the continuum c pi sqrt(dim) / (s + 1) |
  | --- | --- | --- | --- |
  | 3 | 0.6356, 9.9 | 0.7854, 8.0 | 0.6413, 0.7854 |
  | 6 | 0.3654, 17.2 | 0.4488, 14.0 | 0.3664, 0.4488 |
  | 12 | 0.1972, 31.9 | 0.2417, 26.0 | 0.1973, 0.2417 |
  | 24 | 0.1026, 61.3 | 0.1257, 50.0 | 0.1026, 0.1257 |

  with the pair added, the rest frequency the quadrature to the lattice's
  residual (s = 12 on a layer with [1, 16]: 0.3195 exact against 0.3189).
  Form (I) is the CONTROL: a rest world's check of a confined record's
  clock, and, moved, the world that reads gamma_m^2 (the cavity regime's
  limit, section 8). It is never the object's definition.
- **(II) The free massive packet**, no well: a PHYSICAL THING of the
  design, the medium's free massive quantum, a matter wave at group pace
  below c_m with its own clock omega_0, covariant, and it SPREADS (tau = 6
  sigma^2 omega_0: 54 intervals at s = 12 and [1, 16]; 907 at s = 24 and
  [1, 1]); carried by the rule wherever its rows reach; it clicks only by
  reaching a body's cells (verb G, the same kind); not an object, and no
  world of section 11 is built on it.
- **(III) The bound state of the coupled records** (the second draft's
  self-consistent pair): DROPPED. Light has no gap, so an index lump binds
  no light: with D >= 1 inside and D = 1 outside the operator's norm is
  bounded by the continuum's top, `||D^-1/2 (L / 3) D^-1/2|| <= 2`, an exact
  never in every dimension (checked once: 1.9780 < 2 for n^2 = 2 in a
  12-cube on a 32^3 box; on a chain the fixed-point iteration of the pace form finds no
  self-trapped pair at kappa = 0.3, 1, 3, `massive_light_self_trapping.py`;
  Reviewer 3's 12.5 (c) agreed). So the light half of a self-consistent
  state does not exist: **light cannot be a body** (the owner's sentence).
  What holds the object's cells together is the declaration of R, or the
  tie of Reviewer 3's C11; the massive record's mode inside R is then a
  computation (the threshold above).

The owner's "N derives how many cells" holds as: the side is declared, and
the mode's extent, frequency and regime follow from the pair and the side.

**The medium: what the design carries, and the alternative, with the price
of each** (the Boss's structural question of 14:15Z; the owner to be told).
This design carries the massive record kind as a RULE ON EVERY NODE of the
board: the world declares the background pair `[num, den]` (the medium's
gap mu, world data like the phase circle's N), the object's cells carry the
LOWERED pair (the well) as one extra declaration at the cells (the owner's
record 1385 met: the object's Nodes carry one extra declared pair, on top
of the world's), and the coupling g, G of section 7 lives on the object's
cells only, so the medium away from objects is invisible to light. Then
the object's mode is BOUND below the medium's gap with its tail in the
medium, the well regime exists, and the clock in motion is section 8's.
What it costs: (i) a background pair declared per world; (ii) a free
massive packet away from any object exists as the medium's own free record
(form (II): a physical thing of the design, a free massive quantum,
covariant, spreading, its pace c_m; it clicks only by reaching a body's
cells, where it merges with the body's record by verb G, the same kind); (iii) a two-pace world (section 2). In the pins: five's 1 and 1
to the band's second term; the lifetime the radiative tau of section 7;
the index from g, G. THE ALTERNATIVE (the Algebra Mathematician's chapter,
section 5): the pair only at the object's cells, a MASSLESS SURROUND. Then
no mode is bound: a frequency below the massive edge is an outgoing wave
outside, so the lowest mode LEAKS into light's band, `omega_1^2 = p / q +
pi^2 / s^2` (a cube, the first Dirichlet mode, the zero one Link outside),
with the quality `Q = 0.13 (mu s)^3` per axis: a 12-cube at mu = 0.05 rings
0.03 of a period (no clock), a 30-cube at mu = 0.15 about twelve periods;
no well regime exists (there is no medium to hold a tail), and the clock in
motion is the cavity's, the medium's 1 / gamma_m^2, so five's 1 and 1 is
lost in form and the lifetime is Q periods. The alternative keeps the
world free of a background pair and of free massive packets; it gives no
Lorentz clock to any object. The design takes the first; the Boss carries
the difference to the owner with these four answers. In Reviewer 3's
letters (his line of 14:08Z through the Boss): (W), the pair uncompensated
on the SECOND record kind, whose rule runs at every Node its rows reach
(rows created as the record spreads, as light's), its background pair the
kind's own declaration in the world file (its rest mass, as light's family
has its clock), the object a region of lowered pair at declared cells, a
clock that persists, a free massive packet a matter wave at group pace
below c with its own clock; and (M), the pair at the cells on LIGHT's
record in a massless surround: no bound mode and no clock (the resonance
above), but a MIRROR for light below mu, evanescent inside: the WALL the
design wanted, derived from the pair. CONFIRMED here as the design's
reading: the owner's cube that produces clicks is (W); (M) is the wall for
light (DESIGN.md section 5's mirror, now a value of the pair); the margin
rule of section 11 reads under (W).

## 5. The block's momentum, step and push

One integer per axis for the whole block, **P**, with its remainder (the
owner's "one body"; per block a declared tie, Reviewer 3's C11, since one
integer for many cells is not one cell's reading): the stress of the total
field (DESIGN.md 5.1 (a)) at every outer Port of the block, summed into
**P** (verb G over the block's Ports, then D with the remainder kept: each
face's cell adds its Port's stress to the block's integer as a detector
set's cells add to one pointer today). The step: the accumulator per axis
against 3 Q S M x 56 d with M the block's content, the remainder kept; the
block's CELLS and its pair region step one Link together by verb T; the
massive record's rows STAY on their Nodes and follow the moving well by the
rule (Reviewer 3's line on 7a82c155, record 1431: a carried record would be a
hop of the record, the mathematician's 5.4 (iv), not the design; section 8's
own script reproduces Lorentz by stepping the well only); the coupling's
first difference of section 7 stays the SAME-NODE difference on every
interval (a difference along the cell's path on a hop interval was tried
and is unstable, section 7), and G g is carried as [K^2, K^2 - 3] (section
7). The bound |**v**| < c_m on the vector
(the record's own pace, section 2), a crossing the world's stop with a
diagnostic (DESIGN.md 1.2 (c)). What the block feels: light's stress at
its outer Ports; what it does to light: section 7.

## 6. The click of a block: light passing through a body that has a clock (the owner's word, record 1414)

The click is in the Outside, and light produces it, through a body: the
click is the evaluation E of the object's own record on its cells at the
declared wheel W (the owner's 14:08Z). Light arriving at the block's cells
drives the block's record through the receive of section 7 (the owner's
`a_m += g a_l`, in the stable form the first difference of light's row);
the block's pointer accumulates its own record's motion across all its
cells (the owner's "the click in the Outside is read across its cells");
the click when that motion crosses the declared rung of the declared wheel
W in the block's OWN clock (the counting form, DESIGN.md section 5); the
click line with the block's own count (its mode's cycles, section 4) and
the light record's birth stamp. **Light does not need to stay in order to
be read; it needs only to pass through a body that has a clock.** A click
is therefore always a body's event in the body's clock: light never
clicks; light is read: it moves the body's record, and the body clicks
(the same statement said from the free Node's side, which has no rung, no
count and no reading; the owner's sentence of record 1414 above is the one
written for the record and the algebra file), and it needs NO SINK: the verbs are lossless, light
passes on, and the click is the crossing. The whole detector law of today
(the two slits, Malus, Bell) reads so.

**POSTULATES.md section 10, settled by the owner's word** (14:33Z, record
1421: "all the postulates must be changed so that they agree with the
algebra; what does not agree there is settled by the algebra"). The
postulate follows the algebra: a record is READ at a detector by E in the
detector's own clock (the click), and a light record ENDS only where a take
is declared (the absorbing worlds of section 7; a clock body takes nothing).
POSTULATES.md section 10 is being rewritten to this on the branch
`postulates-by-algebra` (the whole file brought to ALGEBRA.md, Reviewer 3
gating); this design cites the record and does not edit the postulate.

## 7. The coupling between the two record kinds: the dielectric, one declared g with G

**The form** (the chief physicist's 14:00Z finding, Reviewer 3's 12.5 (b)
agreed with two precisions; `massive_dielectric_index.py`): at a cell of R
the two records' rows are coupled by one entry of verb B's declared matrix
over the OTHER record's two columns (now, before), the FIRST difference
both ways:

    the massive row gains   g (a_l,now - a_l,before)    (light's field drives the block's record),
    light's row gains      -G (a_m,now - a_m,before)    (the block's current is light's source),

both local to the cell, the order of the two steps within the interval the
engine's. The owner's `a_m += g a_l` (record 1414) is the receive's
MEANING, light drives the object's record; the first-difference form is
its stable writing, since the amplitude form is the tachyon of Reviewer
3's 12.5 (a) (below). The dispersion `(c^2 k^2 - omega^2) (omega_0^2 - omega^2) = G g
omega^2`: both roots real and non-negative for every k and G g > 0, stable
at every strength; the index `n^2 = 1 + G g / (omega_0^2 - omega^2)`, the
classical dielectric (the chain read 1.034, 1.083, 1.159 against the
closed form 1.043, 1.104, 1.200 at G g = 0.02, 0.05, 0.10, omega_0 = 1 / 2,
omega = 0.15; the second-difference form of the script has the same
dispersion). With the first difference both ways `E_light + (G / g) I_m` is
conserved and the coupling moves nothing into it (gyroscopic): a local
conserved energy, which the second-difference-one-way form lacks. This is
Maxwell's dielectric written on the potentials: the record is the
potential, the field its first time difference, the polarization's current
the massive record's. The three tests: generic (one matrix entry, no family
name, the same for every pair); vector (B, linear in the other record's two
columns); local (the cell's own two records). PASS, PASS, PASS.

**The source term** (Reviewer 3's line of 12.4, answered): the block EMITS
at its mode through this same entry, `-G (a_m,now - a_m,before)`: the
block's oscillating record is light's source at its cells, a lamp at the
object's rest frequency, no train declared. Not a third thing (his 12.6
(e)). The amplitude coupling of the second draft's section 13 (light gains
g a_m) is WITHDRAWN: tachyonic (the coupled mass matrix [[0, -g], [-g,
omega_0^2]] has a negative eigenvalue; a block of side s carries the
growing k = 0 mode once s > pi c omega_0 / g, four Links at g = 0.02), his
C10 (a) with it.

**Radiation, and the register's train derived** (Reviewer 3's MUST 1 at
198a9bfe, his chain): under the coupling the block's mode RADIATES and
decays, the lifetime tau falling as 1 / g^2 (320 periods at g = 0.002, 76 at
g = 0.005, his COMPUTATION): an object's light is a decaying train of its
own frequency, the register's declared train DERIVED. And a condition: a
lone object's clock stops in tau, so a world's readings sit inside tau, or
the receive re-excites the mode (a detector driven by light of its
frequency rings again). g and tau are declared and computed per world.

**The index in motion, the OWNER'S WORD** (Reviewer 3's precision (2)): in
motion the co-moving first difference at a carried cell is (u . d) /
gamma_m, so the moving block reads in its own frame `n^2 - 1 = (G g /
gamma_m^2) / (omega_0^2 - omega'^2)`, short by 1 - beta_c^2 (a third at k =
3), UNLESS the declared product G g is carried as `G g x [K^2, K^2 - 3]`
(gamma_m^2 = K^2 / (K^2 - 3) at the drive's k = K, a rational pair from the
drive's own declared count, no root). Two readings: (a) that pair is a
DECLARATION boosted (a world key carried in motion); (b) it is a
COMPUTATION from the drive's count K, which the stepping cell has. TAKEN
BY DELEGATION (the owner's word of about 13:55Z, "close it among
yourselves, and let me know", read by the Boss at 14:25Z as a delegation,
reversible on his word): (b), the pair `[K^2, K^2 - 3]` formed by verb D on
integers the stepping cell has, nothing new declared in motion. THE CHAIN
CHECK, made in the design's reading (COMPUTATION, `massive_moving_index.py`
with its printed record, both forms of the coupling on a hop; Reviewer 3's
MUST on 7a82c155, record 1431: the step translates the cells and the pair
region only, the massive rows stay on their Nodes and follow by the rule; a
first version that carried the rows with the cells is superseded, a hop of
the record and not the design): a block of 24 cells, the medium's pair
[156, 157], the well mu^2 / 2, G g = 0.005 (n = 1.236 at rest); light at
omega = 0.035 through the block stepped at K = 3; the lab phase delay at a
probe against the same train without the block; the covariant expectation
from the phase's invariance, (n(omega') - 1) omega' gamma_m s / c, with
n(omega') the RESTING block's own reading at the block-frame frequency; the
energy account printed (light's E on the chain beyond the source's feed,
the massive E, and their conserved combination E_light + (G / g) E_m).
FIRST FINDING: the coupling's first difference taken ALONG THE CELL'S PATH
on a hop interval (Reviewer 3's (b), the backward difference in both rows)
is UNSTABLE, and so is the ADJOINT PAIR he then prescribed (his line on
4f74bf2a through the Boss, 15:39Z: light's step first, the source the
backward difference of the massive levels along the path on the hop
interval, the receive the forward difference of light along the path on
the interval before the hop), implemented as stated in the script and
printed beside the same-Node form: it pumps more slowly than the
both-backward form (light's E +17 to +9 x 10^4 per interval in the 4400-step
windows, unbounded on the longer chain, the amplitude 7 x 10^4 by 3000
intervals of motion) and its head-on readings before the pump dominates
are 0.79 and 1.07, the both-backward form's; the same-Node pair conserves.
The both-backward form light's E grows by 2 x
10^11 per interval in the head-on window and without bound on a longer
chain (the transmitted amplitude 5 x 10^10 by 3000 intervals of motion),
while the hopping well alone, without light, is bounded (a scratch check
of both the (B) form and the chain H form); the SAME-NODE first difference
on every interval (the hop changing only the cells' set and the pair
region) conserves the combination to 10^-5 per interval, as at rest. So the
path forms as tried are conservation breaches and are withdrawn; the
same-Node form is the coupling in motion in this design until Reviewer 3
names a conserving path form and it is checked the same way. SECOND FINDING, in the stable form: HEAD-ON the lab
delay is 0.40 of the covariant value with G g unchanged and 0.50 with G g x
[K^2, K^2 - 3]; FROM BEHIND (the longer chain, the window after the
block-frame period settles) 4.3 and 6.8 times the covariant value (the
transmitted amplitude 1.2 to 1.3 there, the energy conserved). NEITHER
declaration makes the stepped well a covariant dielectric, and the drive's
pair moves the head-on reading toward and the receding reading away from
it: the index in motion is a COMPUTATION of the stepped rule per world and
a PREDICTION of the model as built (the stepped cells' mark, far from the
covariant slab, beside the clock's residual of section 8, which is small
because the clock is the field's mode and the index is the cells'); the
delegated (b) of the index in motion stands as the drive's pair carried,
with these numbers as its reading and no claim of covariance; nature's row
is Fizeau's drag (light in a moving medium, first order in beta at large
K), NOT computed here (section 12).

**The sink, a SEPARATE declaration of the worlds that absorb, not a
condition of the click** (Reviewer 3's MUST 3, answered by the owner's word
of 14:08Z: the click is the crossing, light passes on). Where a world must
absorb (a screen that must not re-emit, a sponge, a wall that eats), it
declares a loss the verbs do not have, with its kind: (a) the TAKE, the
damping pair on light's row at the object's cells (DESIGN.md section 5's
Port's take; a DECLARATION of the world: the cells absorb what they read),
or (b) a declared DAMPING on the mode (the block's record loses a declared
fraction per interval; a DECLARATION of the object, which also stops its
clock). TAKEN BY DELEGATION (the same word of the owner, the Boss's reading of
14:25Z, reversible on his word): the TAKE (a) on light's row at the cells
of the objects declared ABSORBING (a screen, a sponge: the record ends
there, POSTULATES 10 as written), and NO take for a clock body read many
times (the owner's 14:08Z: light need not stay); not a damping on the mode.
The two readings of POSTULATES 10 in section 6 stay stated for the record.

**One coupling, not two** (Reviewer 3's MUST 4): with this linear coupling
present the second draft's pace coupling (the one-wall pair through the
other record's row, kappa) is NOT needed and not covariant (a local pace is
a medium): ONE declared g (with G) per object, kappa withdrawn. The
receiver forms of DESIGN.md section 5 become values of it: the mirror the
strong-coupling limit (the index large, the Fresnel step to 1), the sponge
the declared damping (the sink (b)), the take the sink (a). What light sees
at a crowd (rows 12 and 13, the deflection and the delay) is NOT derived in
this design: the coupling gives an index at declared cells and nothing
about a crowd's field; the rows keep the ray law's history (2.00 and 1 +
gamma_PPN there). "Gravity as an index of the crowd's massive records" is
a hypothesis outside the law, under its own name `gravity-index-hypothesis`,
with no number here (Reviewer 3's MUST (iii)).

## 8. The motion: one statement (COMPUTATION, `massive_block_clock_motion.py`)

The theorem of the second draft (a declared rigid region carried in
motion reads the medium's clock, 1 / gamma_m^2) and Reviewer 3's C8 (the
well-regime block reads Lorentz to first order with its cells declared)
are ONE statement:

    f / f_0 = omega_b(gamma_m s, g) / (gamma_m omega_b(s, g)),

the moving block a RESTING block of width gamma_m s with the same g, read
at 1 / gamma_m (the boost of the continuum's operator: the declared cells
widen in the block's frame and never contract), omega_b the lowest mode of
the pair and the side (section 4). Checked on an independent chain (the
rest mode stepped by an accumulator to k = 3 after a ramp of 1500
intervals, 8000 intervals held, the clock read at the co-moving centre by
the spectral peak), mu = 0.05:

| s | g | eps at rest | f / f_0 read | the one formula | Reviewer 3's C8 reading | 1 / gamma_m | 1 / gamma_m^2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.0183 | 0.100 | 0.7936 | 0.7852 (the one-Node needs his strength form gamma_m g: 0.7934) | 0.7949 | 0.8165 | 0.6667 |
| 12 | mu^2 / 2 | 0.057 | 0.8065 | 0.8065 | 0.8060 | 0.8165 | 0.6667 |
| 12 | mu^2 | 0.201 | 0.7811 | 0.7812 | 0.7796 | 0.8165 | 0.6667 |
| 24 | mu^2 | 0.471 | 0.7448 | 0.7450 | 0.7461 | 0.8165 | 0.6667 |
| 48 | mu^2 | 0.748 | 0.7128 | 0.7129 | 0.7107 | 0.8165 | 0.6667 |

The formula gives every reading to 0.01 percent for s >= 12, and his to
0.3 percent. Its two limits:

- the WELL limit, omega_b independent of s (the mode's support far beyond
  the cells): f / f_0 -> 1 / gamma_m, Lorentz's clock, with the first-order
  deviation `eps (gamma_m^2 - 1) / 2` (his closed form `(1 / gamma_m)
  sqrt((1 - gamma_m^2 eps) / (1 - eps))`; his chain 0.8073, 0.7947, 0.7452
  against 0.8079, 0.7935, 0.7454 at eps = 0.04, 0.10, 0.25): the carried
  cells' mark on the clock, the block form's own prediction, the band's
  second term (section 9). Exactly Lorentz only with the well's strength
  carried as g / gamma_m, a root the algebra does not have (the strength
  form of the withdrawn `lorentz-shape-v1`): nothing is declared in motion,
  and the residual stays;
- the CAVITY limit, omega_b proportional to 1 / s (the mode's support the
  declared region): f / f_0 -> 1 / gamma_m^2, the medium's clock, the
  second draft's theorem, true exactly in this regime (form (I) moved is
  its control world).

**The theorem's scope, restated:** a declared region reads the medium's
clock exactly when the mode's support IS the region; when the region only
sets the well and the field's own bound mode extends beyond it, the clock is
the covariant field's. In the algebra's terms the cells' declaration is
lawful world data, a scalar on Nodes on which the 48 act trivially, carried
by the step verb like a wall's placement; what the theorem forbade was
declaring the MODE's extent, not the well's cells. Nothing is declared in
motion; the first draft's choice (a declared contraction or a seventh
verb) stays withdrawn; Lorentz is reached as a relation on the characters,
with c_m for the massive record and c for light (section 2's two-pace
prediction: the boosted well's mode reads 1 / gamma at beta_m = beta_c c /
c_m, 0.8149 against 0.8165 at k = 3 and N_0 = 50).

**The characters themselves** (the second draft's check, kept): the free
massive record's characters lie on section 2's surface to 0.1 percent at k
<= 0.3 per Link; the boost of a rest state at omega_0 to the pace v is the
character with the carrier k = gamma_m omega_0 v / c_m^2, its frequency
gamma_m omega_0 (+0.3 percent on the lattice at k = 3) and its internal
phase omega_0 / gamma_m: the clock slows by 1 / gamma_m and the packet
contracts by 1 / gamma_m on the lattice's own surface.

## 9. The pins as consequences: one table

Two blocks of the design at L Links face to face on a layer, in the well
regime with eps <= 0.1; light inserted by block A at its mode through the
coupling of section 7 and received by B and back (light massless,
DESIGN.md unchanged). Every row a COMPUTATION before any board run; the
band's terms named; no pin found by a run; the two-pace world a
prediction:

| Row | The consequence of the algebra | The band |
| --- | --- | --- |
| (d) at rest | COMPUTED (`massive_light_clock_relay.py`, a chain: the medium's pair [156, 157], lambda_0 = 32, two objects of 12 cells with the well mu^2 / 2, L = 60 between the facing cells, A_0 = 2^20, W = 64, G = 1): the receiver's driven record crosses the rung 1 / W of the train's norm delta_rung = 46, 25, 22, 20 intervals after the front at g = 0.02, 0.05, 0.1, 0.2 (the ring-up), and the emitter's RECEIVED part (its record with the partner less its record alone) crosses at N_0 = 527, 324, 305, 258 intervals against 2 L / c = 207.85; with the partner an (M) MIRROR (the pair on light's record at its cells, the gap 0.3) N_0 = 238 and 236 at g = 0.05 and 0.2. The register's 206 +- 2 is NOT MET by any of these declarations: the register's 206 was the Port's take on the ARRIVING light (an immediate rung), the design's counting form is the object's OWN record's motion, which builds over its ring-up; so the light clock of two bodies reads N_0 = 2 L / c + the two ring-ups, a COMPUTATION per declaration (its cycle set by the coupling, as the relay of DESIGN.md 8's record), never 206; the register's numbers belong to the world of an (M) mirror and a detector declared ABSORBING with the take on the arriving light (section 7), which the design keeps as that world. The emitter's own mode e-folds in 0.8 to 3.0 periods at these couplings (G g = 0.02 to 0.2): a clock body wants a weak coupling, which lengthens the ring-up as g^(-2/3): the trade-off is the design's, printed per world | the rung's grain; N_0 the script's number per declaration; 206 the take-world's |
| (e), (f) in motion at k = 3 | the blocks' own count per cycle in both arms: N_par / N_perp = 1 and 1, within +- 0.03 (Reviewer 3's third line), plus the band's second term eps (gamma_m^2 - 1) / 2 for eps <= 0.1 (at most 0.025 at k = 3); the cycle in the lattice's intervals gamma_m N_0 along and across | +- 0.03 plus eps (gamma_m^2 - 1) / 2; the two-pace prediction 0.2 percent at N_0 = 50 |
| the lab's row | the moving block's clock read by a resting one: 1 / gamma_m in the well regime, to the second term; 1 / gamma_m^2 for form (I) moved (the control) | eps (gamma_m^2 - 1) / 2; the residual |
| 4a | the block's own clock slow by 1 / gamma_m in the lattice's intervals: the muon's row PASS in form, the number gamma_m at the world's beta_c (gamma at beta_m = beta_c c / c_m to second order) | the second term; 0.2 percent at N_0 = 50 |
| 4b | the boosted block's emission read by a block at rest: 1 + z = gamma_m (1 + beta_c) receding, the character's frequency gamma_m omega_0 shifted by the medium's Doppler | the residual |
| (g) the block at rest | its self-click its own mode, N_b(pair, s), no return and no timer; decaying in tau (section 7) unless re-excited; the clock sentence of DESIGN.md section 8 not needed for it | exact to the residual |
| the index block | n from g, G, the pair and omega: n^2 = 1 + G g / (omega_0^2 - omega^2); the Fresnel step ((n - 1) / (n + 1))^2; the chain's 1.034, 1.083, 1.159 against 1.043, 1.104, 1.200 | the chain's 0.8 to 3.4 percent below the closed form at s = 12 (the faces' steps) |
| the index block IN MOTION (a prediction of the model as built) | in the design's reading with the stable same-Node coupling (section 7, `massive_moving_index.py`): the stepped block's lab phase delay at K = 3 is 0.40 (G g unchanged) and 0.50 (the drive's pair) of the covariant slab's head-on, and 4.3 and 6.8 times it from behind; the path-difference coupling on hops unstable and withdrawn; not covariant under either declaration; nature's row Fizeau's drag at first order in beta, not computed | the chain's +- 0.001 rad head-on; Fizeau pending |
| the rest cavity (form (I)) | section 4's table: 0.2417 at s = 12 on a cube; the quadrature with the pair | the lattice's residual |
| NATURE, the two-pace world (the owner's word of about 14:50Z, "verify before implementing", record 1424; the sources resolved by the Source Verifier, `docs/designs/detector_law/NATURE_SOURCES_MASSIVE.md` on `nature-sources-massive` at c396a65b, every published number a search excerpt, "(snippet)", to be read once in the paper before final) | the design predicts a massive record's limiting pace c_m = c sqrt(cos omega_0), the deficit omega_0^2 / 4 in c: 3.9 x 10^-3 at N_0 = 50 (COMPUTATION). Nature, the SUBLUMINAL side (the design's): the electron's maximal pace below light's by less than 6 x 10^-20 on the Crab-to-Earth combination and 2 x 10^-14 on every coefficient (Altschul 2006, the Crab's synchrotron; NATURE (snippet)); the 1.3 x 10^-15 recalled earlier is the superluminal side (Stecker and Glashow 2001) and not this row's; the proton's 10^-23 NOT FOUND as published, dropped; Coleman and Glashow 1999 resolved, its own numbers not reached. So the law in this form REQUIRES omega_0 <= 2.8 x 10^-7, N_0 >= 2.2 x 10^7 intervals (COMPUTATION): NOT COMPARED until the conversion between the board's interval and nature's electron rest period is written (STATUS_RULES step 2); a CONSISTENCY REQUIREMENT on that conversion, never a pin at N_0 = 50, whose 0.4 percent is the lattice's | NOT COMPARED (a consistency requirement on the conversion) |
| NATURE, the band's second term (the same word; the same page at c396a65b) | the design predicts a BOUND object's clock in motion reads (1 / gamma_m)(1 - eps (gamma_m^2 - 1) / 2), eps its binding depth; a free massive packet has eps = 0 (the muon, row 4a, exactly 1 / gamma_m). Under the NAMED HYPOTHESIS that a real clock's eps is its binding energy over its rest energy (not derived in this design, whose objects are declared cubes): (B) the stored Li+ clock, Botermann and others 2014: beta = 0.338 and the bound +-2.3 x 10^-9 on gamma sqrt(1 - beta^2) = 1, SAME (NATURE (snippet)); eps = 2.2604 eV / 6534.9 MeV = 3.46 x 10^-10 (COMPUTATION from the 548.5 nm line and the 7Li mass; the 10^-9 recalled earlier DIFFERS by a factor 2.9); the second term 2.2 x 10^-11, one hundredth of the bound: BELOW MEASURABILITY, a BOUND row, consistent. (C) the Moessbauer rotor, Kuendig 1963: the ratio to Einstein's shift 1.0065 +- 0.011, SAME (NATURE (snippet)); Fe-57's binding 8.8 MeV per nucleon over the nucleon's rest energy, eps about 0.94 percent (RECALLED, not reached from the page; a standard table to cite before final); the design's 1 + eps = 1.0094, at 0.26 sigma: a BOUND, not a test; the later rotor re-analyses (Kholmetskii and Yarman 2008 to 2016, an excess k = 0.60 to 0.69; Corda 2015; Friedman 2016) CONTESTED, none decided: the design's 0.94 percent is 9 to 15 sigma below their excess, a fact and no verdict | BOUND rows: (B) 2.2 x 10^-11 against 2.3 x 10^-9; (C) 0.26 sigma against 1.1 percent; the eps mapping a named hypothesis |
| the atom's levels (the owner's question of record 1430: what is an atom, what is an electron, in the algebra) | an ELECTRON is the free massive quantum of the design (form (II), section 4): a free packet of the massive kind, its rest mass the kind's pair, its clock omega_0, exactly 1 / gamma_m in motion to second order, clicking only at a body's cells. An ATOM is a well of the pair (the nucleus: declared cells with the lowered pair) with the massive record bound in it; its levels the well's bound modes; its lines the modes' frequency differences read by light through the coupling of section 7. COMPUTED (`massive_well_spectrum.py`, a 64^3 periodic box, mu = 0.15, the inside's gap reduced and never reversed): a cube of side 20 at full depth holds one deep mode (eps 0.45) and a pair at the threshold; a sphere of radius 10 one mode; a Coulomb-like profile g(r) = mu^2 min(1, r_0 / r) holds six bound modes at r_0 = 6 with eps ratios 1, 0.40, 0.32 (x2), 0.155 (x2) and eight at r_0 = 12 with 1, 0.64 (x2), 0.51, 0.42, 0.32, 0.25, 0.21: no 1 / n^2 ladder (Balmer's 1, 0.250, 0.111) and not the old 27 / 20, because the well is capped at the medium's gap, the binding is deep (eps 0.4 to 0.7, far from the weak-binding ladder) and the grain is coarse (c / omega_0 = 3.85 Links); THE SCALE CONDITION: nature's hydrogen has the Bohr radius 137 c / omega_0 = 527 Links at this mu, a board of thousands a side, not affordable, as the old atom design said. NOT COMPARED; the ladder a PREDICTION of the model as built for a declared well shape; no Balmer ladder is EXPECTED at these depths (eps_1 = 0.39 to 0.69, r_0 = 6 to 12 Links against c / omega_0 = 3.85: the 1 / n^2 ladder needs eps_1 << 1 and r_0 >> c / omega_0, the scale condition itself), so "no ladder at this scale" is not a finding against the design (Reviewer 3's line on b977743c); the old atom algebra (docs/designs/atom_algebra, atom_levels) history under the new kind | NOT COMPARED (the scale condition); the well's shape a DECLARATION |
| the board's faces | an object nearer a non-periodic face than its mode's extent reads a raised clock (the tail cut, the cavity's creeping in); the margin rule of section 11 a load-time check, the faces periodic by default for the massive record; no pin of the object | the extent from the pair and the side (COMPUTATION); the faces a DECLARATION |
| (h), 10, 2a, 2b, 9 | unchanged: light is massless and its pins are DESIGN.md's | as declared |
| 12, 13 | not derived in this design (the coupling gives an index at declared cells, nothing about a crowd's field); 2.00 and 1 + gamma_PPN stay under the ray law's history | as registered |
| Malus, Bell | outside this design: a scalar record has no polarisation; the polariser needs a Vector record or two records | as DESIGN.md's declared tables |

## 10. The force between two blocks through light

Reviewer 3's closed form (PUSH_BALANCE.md section 10, the coupled-oscillator
force between two emitters at their own frequency): the force on block 1 is
2 A^2 cos(k_0 L) toward the partner; its EQUILIBRIA are the
zeros of cos(k_0 L), L = (2 m + 1) lambda_0 / 4, alternately stable and
unstable by the clocks' relative phase (in phase stable at (m' + 3 / 4)
lambda_0, 88 Links at lambda_0 = 32; antiphase at (m' + 1 / 4) lambda_0,
72), NOT L = m lambda_0 / 2, which are the force's extrema: L_0 = 80 = 5
lambda_0 / 2 is the maximal repulsion and never an equilibrium (Reviewer
3's sections 1 and 10, his MUST (i)); with the
coupling of section 7 the emitters are the blocks' modes and A is set by g
and G. A consequence of the algebra, written before any board run; the
board's two-block world reads it.

## 11. What the engine implements, and in what order

1. The rule with the pair per record on the six-neighbour term (section 1;
   light `[1, 1]`); the conserved form I read by the books (section 3).
2. The block: its cells R declared with the inside pair (the well of the
   pair); one momentum integer per axis with its remainder (a declared tie);
   the step of the whole block by verb T; the coupling of section 7 at its
   cells, one g with G; the click of section 6 at W; the sink as the owner
   words it.
3. The check worlds, in order (which is which per item 4: a CONTROL world
   at one extent of margin, a PIN world of five at two, a PREDICTION world
   the block form's residual): (i) ONE BLOCK AT REST, its mode's frequency
   and extent against section 4 (C6's eigenvalue, the threshold table): a
   control; (ii) the block pushed to k = 3, its clock against section 8's
   one formula: at the four smallest binding sides a PIN world of five (1
   and 1 to the residual under one percent), at s = 20 and 28, mu = 0.15,
   the PREDICTION world (the residual 11 and 5.5 percent); (iii) the
   rest cavity of form (I) against section 4's table, and moved, against
   gamma_m^2 (the control); (iv) the light clock on two blocks at rest (row
   (d): N_0 = 2 L / c + the two ring-ups, the script's number for the
   world's declaration: with the exact mode as the seed 258 at G g = 0.2
   on the chain; with the ENGINE'S seed, a declared flat amplitude A_0 on
   the emitter's cells at both levels, the same script reads N_0 = 235 at
   G g = 0.2 and 310 at 0.05 (the receiver's rung crossed 11 and 13
   intervals after the front), and with an (M) mirror partner 247; the
   world's pin is the script's number under the seed the world declares,
   the builder's question (h)) and in motion (rows
   (e), (f): 1 and 1 with the second term), the light emitted through the
   source term of section 7, decaying in tau; and the TAKE WORLD beside it
   (an (M) mirror and a detector declared absorbing, the take on the
   arriving light) as the register's 206 +- 2 reproduced; the TWO-ARM RELAY
   in motion (rows (e), (f)) as two worlds, which is which declared
   (Reviewer 3's line through the Boss, 15:39Z, on the arms' lengths): (a)
   the CONTROL, declared rigid arms (cells at L along and across the
   motion) at k = 3, expected the theorem's gamma_m ratio between the arms
   times the ring-ups' ratio (the cavity's reading, section 8); (b) five's
   PIN, the arms held by light's force at section 10's equilibrium ((2 m +
   1) lambda_0 / 4) and pushed by the stress of section 5, at k = 4 (v =
   0.25, under the free pair's break at about 0.27 in the morning's chain
   run, which was the ramp's adiabaticity plus the recoil, PUSH_BALANCE.md
   10.7) with that run's ramp; at k = 3 only with the ramp lengthened per
   10.7; expected 1 and 1 to the band's second term; (v) the index block (n from g, G). Nothing found,
   everything checked.
4. **The board's faces and the margin rule** (the owner's question of
   14:12Z; COMPUTATION for the extents, `massive_board_margin.py`;
   DECLARATION for the faces). The object's mode extends beyond its cells
   into the medium with the tail exp(-kappa x), cosh kappa = 3 D_out cos
   omega_b - 2, the extent 1 / kappa = c / (mu sqrt(eps)) Links in the
   continuum (eps the binding depth): a face nearer than the extent
   changes the clock. A ZERO face (a declared wall for the massive record)
   cuts the tail and raises the mode toward the cavity's (the medium's
   clock creeps in); a PERIODIC face wraps the tail onto the object's
   other side (a periodic image, small once the board exceeds a few
   extents); an OPEN board does not exist on the lattice (every world has
   faces: declared walls, sponges or periodic); PERIODIC is the algebra's
   own (the torus of ALGEBRA.md 1.6), and a wall or a sponge at a face is a
   declared deviation per world (the owner's word of record 1421). So the owner's reading is
   right: an object at the edge is not held as itself. THE MARGIN RULE, a
   load-time check like MUST I's floor (Reviewer 3's two lines of his gate
   of 643a1c93, 14:31Z, carried into the build's world section): a hard
   face at distance d shifts the bound mode by about eps e^(-2 kappa d), so
   ONE extent (e^-2, 13 percent of eps, a third of five's band at eps =
   0.1) is enough for a CONTROL world and a PIN world needs TWO extents
   from any non-periodic face; the board's side per axis at least the
   object's side plus two extents (a control) or four extents (a pin) when
   that axis is periodic; the extent printed from the pair and the side
   before the world runs.
   The massive record kind's faces PERIODIC by default (the medium
   continuous, nothing to declare) with the margin; light's faces per the
   experiment as today (the sponge for the detector worlds, periodic where
   the clock's light must not be eaten); the background pair's faces the
   same periodic ones. The numbers (a periodic box of 96^3 for mu = 0.15,
   128^3 for mu = 0.05):

   | mu | s | g | omega_b | eps | the extent 1 / kappa (Links) | the side by the rule s + 2 / kappa |
   | --- | --- | --- | --- | --- | --- | --- |
   | 0.15 | 10 | mu^2 | 0.1488 | 0.007 | 45 (weakly bound, the extent beyond the box; the smallest binding side, g above g_c by 2 percent) | a PIN world of five at s + 4 / kappa, about 190 |
   | 0.15 | 14 | mu^2 / 2 | 0.1488 | 0.006 | 48 (the same, g above g_c by 0.1 percent) | a PIN world of five, about 205 |
   | 0.15 | 20 | mu^2 | 0.1107 | 0.451 | 5.7 | 31 |
   | 0.15 | 28 | mu^2 / 2 | 0.1318 | 0.220 | 8.2 | 44 |
   | 0.05 | 30 | mu^2 | 0.0491 | 0.036 | 61 (weakly bound, the extent beyond the box; g above g_c by 3 percent) | a PIN world of five, about 275 |
   | 0.05 | 42 | mu^2 / 2 | 0.0491 | 0.035 | 62 (the same, g above g_c by 1 percent) | a PIN world of five, about 290 |
   | 0.05 | 60 | mu^2 | 0.0368 | 0.458 | 17 | 94 |

   WHICH WORLD IS WHICH (Reviewer 3's line): the four smallest binding
   sides are the DEEPEST well-regime clocks (eps 0.006 to 0.036, the
   residual eps (gamma_m^2 - 1) / 2 under one percent at k = 3) and so the
   best PIN worlds of five's 1 and 1, if a board of s + 4 / kappa is
   afforded (about 200 a side at mu = 0.15, s = 14: 8 million Nodes, HOST
   about 0.3 s per interval, a moving world under an hour); the s = 20 and
   s = 28 worlds at mu = 0.15 (eps 0.45 and 0.22: the residual 11 and 5.5
   percent at k = 3) are the worlds of the PREDICTION (the block form's
   residual, section 8's second term), not of five's pin, on a periodic
   48^3 board (110,592 Nodes; HOST 0.005 s per interval, a rest world of
   three periods a second, the moving world two minutes); the rest cube at
   mu = 0.15, s = 20 at full depth is also the cavity-leaning CONTROL. A
   well-regime clock at eps about 0.1 has the extent c / (mu sqrt 0.1) =
   1.83 / mu: 12 Links at mu = 0.15 (a side between 14 and 20 at full
   depth; a pin board of 64^3 at two extents, HOST 0.010 s per interval,
   the moving cube at k = 3 over its ramp and hold, 9500 intervals, 2
   minutes) and 37 Links at mu = 0.05 (s about 36 to 40 at full depth; the
   board 128^3 at two extents, HOST 0.079 s per interval, the moving world
   12 minutes); the moving cube's axis periodic, the travel wraps. The
   HOST figures are numpy on this machine; the engine's integer form is
   its own cost.
5. The key `massive-record-v1` OFF by default; the build only on Reviewer
   3's gate of this draft's SHA, the Algebra Mathematician's chapter, and
   the owner's second word through the Boss (with his two words of section
   7: the index in motion, the sink); the engine's numbers reported against
   the algebra's, never the algebra moved to the engine's.

## 12. The three tests per sentence; the scripts; what is not computed

| Sentence | Generic | Vector | Local |
| --- | --- | --- | --- |
| the rule with the pair on the six-neighbour term (1) | PASS | PASS (B, T, D) | PASS |
| the well of the pair on declared cells (4) | PASS (a per-Node pair, world data) | PASS (the same verbs) | PASS |
| the faces as the own record's mirror (4 (I), the control) | PASS (the mirror form) | PASS | PASS |
| the block's momentum and step (5) | PASS (the tie declared) | PASS (G, D, T) | PASS (the block's own Ports) |
| the click across the cells (6) | PASS | PASS (E) | PASS (the block's pointer) |
| the dielectric coupling, first difference both ways (7) | PASS (one g with G) | PASS (B, linear in the other's two columns) | PASS |
| the sink (7), either form, only where a world absorbs | a DECLARATION of that world | (D) or the take | PASS |
| the motion (8) | a derivation, no sentence added | none needed | none needed |

**The scripts beside this document, each printing its record (`.out`),
COMPUTATION only, no engine run:** `massive_c_derivation.py` (section 1.1),
`massive_corner_stability.py` (sections 2 and 3), `massive_dielectric_index.py`
(section 7), `massive_light_self_trapping.py` (section 4 (III), the
negative result), `massive_cube_threshold.py` (section 4, the exact table,
the window, light's norm bound), `massive_block_clock_motion.py` (section 8),
`massive_board_margin.py` (section 11, the mode's extent in the medium and
the margin rule's numbers, with the HOST cost), `massive_light_clock_relay.py`
(section 9 row (d), the two-object light clock on a chain: the rung-crossing
time, N_0 against 2 L / c, the mirror variant), `massive_moving_index.py`
(section 7, the moving block's index against the resting one), and
`massive_well_spectrum.py` (section 9: the atom's levels as the well's bound modes, three shapes, against Balmer),
`massive_time_reversal.py` (section 14: the rules' exact inverse in integers, the same formula backward, the click).
Run each as its docstring says; the numbers in this document are theirs.

**Not computed here, and said so:** Fizeau's drag (the stepped block's
index at first order in beta, large K, against nature's 1 - 1 / n^2; the
chain at K = 3 is far from that regime); the click's completion under the
take where a world declares it; the
cube's threshold under a light-shaped well (the peak capped at mu^2, the
mean depth mu^2 / 8: none found to side 44, the side needed about 100, a
scratch box, HISTORY); g against any nature row (rows 12 and 13 need a
crowd's pairs, a world to declare); form (C) beyond its name.

## 13. Where the board stopped, and how a foreign object connects to it, in the algebra

The owner's word (13:25Z): nothing is run; we continue from where the
board stopped, which is the OUTSIDE, at the foreign object; check exactly
how the foreign object connects to the board, algebraically, and derive it
to the board from there.

**Where the board stopped.** The Inside is built and checked: the
six-neighbour rule on the free Nodes (the splitting ray, the amplitudes
held, the pace c, the bells and the two slits by the pins script; the
chain's click in the build at f4a3971a). The Outside is where it stopped:
the foreign object (the lamp that inserts, the receiver that clicks, the
wall, the polariser) was carried in the build by declared forms (the
lamp's train, the Port's take, the grace) and not by the law. This
document replaces those forms by the massive record kind; this section
states the connection itself, verb by verb, so that the engine derives it
and does not declare it.

**The connection: four verbs at the object's cells, and no other.** A
foreign object is its cells R (section 4) carrying its massive record; a
light record reaching a cell of R meets the object through exactly these:

| What the object does | The verb, in ALGEBRA.md's terms | The declared integers | The three tests | Covariant |
| --- | --- | --- | --- | --- |
| INSERTS light and RECEIVES light (the lamp, the detector: the same thing) | (B) the bilinear form with a declared matrix, chapter 2.2: at a cell the massive row gains g (a_l,now - a_l,before) and light's row gains -G (a_m,now - a_m,before), the first difference both ways (section 7): the insert is the block's current as light's source at its own mode, no train declared; the receive is light's field driving the block's record | g, G (one product G g sets the index; one ratio G / g the conserved energy's weight) | generic, vector, local (section 7) | at rest yes; in motion the owner's word (the drive's pair [K^2, K^2 - 3] or a declaration) |
| SCATTERS, REFLECTS, BINDS (the index, the mirror's limit, the wall, the air; the force between two objects) | the same entry: the index n^2 = 1 + G g / (omega_0^2 - omega^2) from the coupling's dispersion; the mirror the strong-coupling limit; the force of section 10 | none beyond g, G (kappa withdrawn, MUST 4) | as section 7 | as above |
| CLICKS (the reading in the Outside) | (E) the evaluation, chapter 2.5: the object's record is one element of Z[Z_N] across R; the click when the object's own motion, driven by light and summed across its cells into its pointer, crosses the declared rung of the declared wheel W in the object's own clock; light passes on, no sink needed (the owner's word, record 1414); the click line with the object's own count (its mode's cycles) and the light record's birth stamp | W, the sensitivity | as DESIGN.md section 5 | the reading, after the last group operation |
| MOVES (the step; the momentum) | (T) the drive with the accumulator and the remainder, chapter 2.1; the momentum changed by the stress of the total field at the object's outer Ports, section 5 | Q S M x 56 d; the tie | as section 5 | yes: the stress the field's own |

Nothing else connects the object to the board: no declared train (derived
as the decaying emission, section 7), no grace, no fan, no one-way take
(the sink a separate declaration of the worlds that absorb, section 7),
no timer, no clock sentence for the object (its clock is its mode); the receiver forms of DESIGN.md section 5 (the mirror, the
sponge, the Port's take) are values of these verbs (section 7).

**What the algebra then gives for the Outside's readings, derived before
the board runs** (each a consequence of the four verbs; the closed forms
Reviewer 3's sections 10, 11 and 12 where they exceed this document):

- The insert: an object at rest oscillating in its mode at omega_b drives
  light at its cells through -G times its current, at omega_b; light leaves
  at lambda_b = 2 pi c / omega_b (the object's rest wavelength; the
  register's lamp declared no clock: here the clock is the mode); the
  power the coupling's and the train's decay tau from g, G (section 7).
- The receive: light of the object's own frequency arriving at its cells
  drives its mode resonantly (the resonance Reviewer 3 asked for, now the
  object's own); light of another frequency drives it off resonance, less,
  by the mode's response; the click's rate per arriving field is this
  response, a COMPUTATION from g, G and omega_b; a detector reads what
  resonates with it, and the counting form's rung is crossed by the
  object's own motion across its cells.
- The light clock at rest on two objects: A's mode drives light, light
  reaches B at L / c, B's mode is driven and drives light back, A's mode
  receives at 2 L / c plus the two ring-ups: N_0 = 258 to 527 intervals on
  the chain at G g = 0.2 to 0.02 against 2 L / c = 207.85 (row (d) of
  section 9, computed); the register's 206 is the take-world's (an (M)
  mirror and an absorbing detector), not two bodies'.
- The light clock in motion: section 8's one formula, the well regime: 1
  and 1 in the objects' own counts to the second term, gamma_m N_0 in the
  lattice's intervals.
- The polariser and the tables: OUTSIDE THIS DESIGN. A scalar record has
  no polarisation; a polariser needs a Vector record or two records, which
  this design does not have; Malus and Bell stay under DESIGN.md's declared
  tables (Reviewer 3's MUST (iv)). What the coupling does give is the mode's
  phase relative to the arriving light's (the resonance's quadrature), a
  COMPUTATION, and no table.

**What the engine implements, from this section, in order**: section 11's
order; the board checks, the algebra leads.

## 14. The direction of time: in the Inside and at the click (the owner's question of record 1439; COMPUTATION, `massive_time_reversal.py`)

- **(a) The light rule** `3 a_next + r' = S_6 - 3 a_before + r`, `0 <= r' < 3`.
  Under the swap `(a_next, r') <-> (a_before, r)` the EQUATION is unchanged.
  The RECURRENCE is a bijection of the row's state given the neighbours, in
  three lines: `(a_before, r) -> N = S_6 - 3 a_before + r` is a bijection of
  `Z x {0, 1, 2}` onto `Z` (each integer once); `N -> (floor(N / 3), N mod
  3)` is a bijection of `Z` onto `Z x {0, 1, 2}`; so the step is a
  bijection, and its inverse is exact: `N = 3 a_next + r'` is exact, `M =
  S_6 - N = 3 a_before - r` has one solution with `0 <= r < 3`, `a_before =
  ceil(M / 3)`, `r = 3 a_before - M`. Nothing is lost: the Inside is
  REVERSIBLE to the bit (600 intervals forward and back on a chain of
  integers: the deviation 0 of the amplitude 957234). But it is NOT
  SYMMETRIC in form: the inverse rounds UP where the rule rounds DOWN, and
  the remainder always lives on the later level; the SAME formula run
  backward (the swap with the floor kept) is a different map and deviates
  by the remainders' grain (29 of 957234 after 600 intervals, a random walk
  of one unit per Node per interval). So the rule carries an arrow in its
  bookkeeping (which level owns the remainder) and none in its information.
- **(b) The massive kind** `3 den (a_next + a_before) + r' = num S_6 + r`:
  the same three lines with `3 den` in place of 3; the exact inverse returns
  to the bit (0 at [128, 129] and at [2, 3]); the same formula backward
  deviates by 365 and 29.
- **(c) The coupling in motion** (the same-Node pair, light's step first,
  section 7): each half-step is invertible given the other record's levels
  (a triangular map), so the pair of steps is a bijection; the reversed run
  takes the half-steps in the opposite order (the massive first), and the
  hop schedule is reversed with the drive's accumulator, itself an integer
  map with an exact inverse. Reversible; not symmetric in order.
- **(d) The click** is the one deletion (ALGEBRA.md 3.1): the record's rows
  are removed at the detector's cells, its content handed over, the
  detector's count advanced by one; the counts form a free abelian monoid,
  not a group, and no step of the board un-deletes a row: the run with a
  click at interval 300 reversed by the exact inverse deviates by 40092,
  the deleted rows' amplitude. THE ARROW OF TIME IS BORN AT THE CLICK and
  nowhere in the rule: (a) to (c) hold.
- **(e) The world that shows it** (a CHECK, never a pin against nature): a
  train on a chain or a layer with no detector declared, N intervals
  forward under the engine, N intervals under the exact inverse (a host
  step, the ceiling division), the board back to its first rows bit for
  bit and the books' E equal; the same world with a detector declared,
  which does not return, by the deleted rows exactly; and the same world
  reversed by the engine's own formula, which returns only to the
  remainders' grain.
