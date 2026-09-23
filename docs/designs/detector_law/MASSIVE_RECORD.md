# The massive record kind and the foreign object as a block: closed from the algebra before the board (the third draft)

The chief physicist's design of 2026-09-23 on the model owner's words, under
the key `massive-record-v1`, OFF by default; docs and printed computations
only; no build. It stands beside [DESIGN.md](DESIGN.md) (the massless kind,
light, unchanged) and [PINS.md](PINS.md). The algebra of the push, the boost
and the gate of this design is Reviewer 3's `PUSH_BALANCE.md`
(docs/designs/detector_law/ on `push-balance-r3`, PR #1043): its sections 10
and 11 at 6d7a03b5, 60509e9a and d9227352, its section 12 at bb43ef41 and
f5752667, its 12.5 at 198a9bfe and its 12.6 at f089736f; cited by those SHAs,
never rewritten. Every number here is a COMPUTATION from the rule, written
before the board runs it, and printed by a script beside this document (the
list in section 12); the board, when it runs, checks the algebra, never the
reverse. The third draft replaces the first two whole: the massive rule is
the stable form (section 1), the pace c is derived (1.1), the object is the
well of the pair on declared cells (4), the coupling is the dielectric
(7), the motion is one statement (8), and the pins are one table (9).

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
compensation is exactly the difference between an index and a mass, and no
third form exists in range 1.

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

The object is a block R of side s (a square on a layer, a cube on the
board), DECLARED as world data like a wall's placement (the owner's cube;
Reviewer 3's C4 and 12.5 (c)), every cell of R carrying a pair `[num',
den']` with `num' / den' > num / den` (the gap lowered inside: a WELL of the
pair; `g = 2 (num' / den' - num / den)` its depth to first order, mu^2 =
omega_0^2 the outside's gap). The object's record is the bound mode of the
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
- **(II) The free massive packet**, no well: covariant, and it SPREADS
  (tau = 6 sigma^2 omega_0: 54 intervals at s = 12 and [1, 16]; 907 at s =
  24 and [1, 1]); named, not carried.
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

## 5. The block's momentum, step and push

One integer per axis for the whole block, **P**, with its remainder (the
owner's "one body"; per block a declared tie, Reviewer 3's C11, since one
integer for many cells is not one cell's reading): the stress of the total
field (DESIGN.md 5.1 (a)) at every outer Port of the block, summed into
**P** (verb G over the block's Ports, then D with the remainder kept: each
face's cell adds its Port's stress to the block's integer as a detector
set's cells add to one pointer today). The step: the accumulator per axis
against 3 Q S M x 56 d with M the block's content, the remainder kept; the
whole block steps one Link together (its cells, its pair region and its
record's rows translate by verb T). The bound |**v**| < c_m on the vector
(the record's own pace, section 2), a crossing the world's stop with a
diagnostic (DESIGN.md 1.2 (c)). What the block feels: light's stress at
its outer Ports; what it does to light: section 7.

## 6. The click of a block: a body's event, in the body's own clock

A click is ALWAYS the body's event, in the body's own clock (the owner's
words: the Outside has no board, only clicks through a foreign object;
every instrument is a foreign object, always self-clicking). Light's
record has no click of its own: nothing is kept at a free Node beyond the
events there, no rung, no wheel; light alone, without a body, produces
nothing Outside. **Light never clicks; light is read: it moves the body's
record, and the body clicks.** The mechanism: light arriving at the block's
cells drives the block's record through the coupling of section 7; the
block's pointer accumulates its own record's motion across all its cells
(the owner's "the click in the Outside is read across its cells"); the
click when that motion crosses the declared rung of the declared wheel W
(the counting form, DESIGN.md section 5); the click line with the block's
own count (its mode's cycles, section 4) and the light record's birth
stamp. The evaluation E of the block's element of Z[Z_N] across R, as every
click. Its completion needs the sink of section 7 (Reviewer 3's MUST 3): the
verbs are lossless, so a reading of light passing and resonating is not
yet POSTULATES 10's action (the record ends at the detector).

## 7. The coupling between the two record kinds: the dielectric, one declared g with G

**The form** (the chief physicist's 14:00Z finding, Reviewer 3's 12.5 (b)
agreed with two precisions; `massive_dielectric_index.py`): at a cell of R
the two records' rows are coupled by one entry of verb B's declared matrix
over the OTHER record's two columns (now, before), the FIRST difference
both ways:

    the massive row gains   g (a_l,now - a_l,before)    (light's field drives the block's record),
    light's row gains      -G (a_m,now - a_m,before)    (the block's current is light's source),

both local to the cell, the order of the two steps within the interval the
engine's. The dispersion `(c^2 k^2 - omega^2) (omega_0^2 - omega^2) = G g
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
drive's own declared count, no root). Two readings, both stated, neither
chosen here: (a) that pair is a DECLARATION boosted (a world key carried
in motion); (b) it is a COMPUTATION from the drive's count K, which the
cell has. The Boss carries it to the owner; the moving block's index
against the resting one is a chain check of a minute, to be made when the
owner's word is given.

**The sink, the OWNER'S WORD** (Reviewer 3's MUST 3): the completion of a
click (the record ends at the detector, POSTULATES 10) needs a loss the
verbs do not have. Two forms, each with its kind: (a) the TAKE, the damping
pair on light's row at the object's cells (DESIGN.md section 5's Port's
take, a DECLARATION of the world: the cells absorb what they read); (b) a
declared DAMPING on the mode (the block's record loses a declared fraction
per interval, the radiative decay above made irreversible: a DECLARATION
of the object). Either is a declaration; the Boss carries the choice to the
owner. Until it is given, the click of section 6 is a reading of light
passing and resonating, and the count of clicks is the count of crossings,
which the pins already compare.

**One coupling, not two** (Reviewer 3's MUST 4): with this linear coupling
present the second draft's pace coupling (the one-wall pair through the
other record's row, kappa) is NOT needed and not covariant (a local pace is
a medium): ONE declared g (with G) per object, kappa withdrawn. The
receiver forms of DESIGN.md section 5 become values of it: the mirror the
strong-coupling limit (the index large, the Fresnel step to 1), the sponge
the declared damping (the sink (b)), the take the sink (a). What light sees
at a crowd (rows 12 and 13) is the index of its massive records by this g:
2.00 and 1 + gamma_PPN a consequence to compute from g, G and the pairs,
not to find.

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
| (d) at rest | N_0 = 2 L / c + 2 tau_g (the modes' response lags, from g) in the lattice's intervals, the register's 206 at L = 60 the stiff-coupling limit; in the block's own count N_0 / N_b(pair, s) | the rung's grain, the lattice's residual |
| (e), (f) in motion at k = 3 | the blocks' own count per cycle in both arms: N_par / N_perp = 1 and 1, within +- 0.03 (Reviewer 3's third line), plus the band's second term eps (gamma_m^2 - 1) / 2 for eps <= 0.1 (at most 0.025 at k = 3); the cycle in the lattice's intervals gamma_m N_0 along and across | +- 0.03 plus eps (gamma_m^2 - 1) / 2; the two-pace prediction 0.2 percent at N_0 = 50 |
| the lab's row | the moving block's clock read by a resting one: 1 / gamma_m in the well regime, to the second term; 1 / gamma_m^2 for form (I) moved (the control) | eps (gamma_m^2 - 1) / 2; the residual |
| 4a | the block's own clock slow by 1 / gamma_m in the lattice's intervals: the muon's row PASS in form, the number gamma_m at the world's beta_c (gamma at beta_m = beta_c c / c_m to second order) | the second term; 0.2 percent at N_0 = 50 |
| 4b | the boosted block's emission read by a block at rest: 1 + z = gamma_m (1 + beta_c) receding, the character's frequency gamma_m omega_0 shifted by the medium's Doppler | the residual |
| (g) the block at rest | its self-click its own mode, N_b(pair, s), no return and no timer; decaying in tau (section 7) unless re-excited; the clock sentence of DESIGN.md section 8 not needed for it | exact to the residual |
| the index block | n from g, G, the pair and omega: n^2 = 1 + G g / (omega_0^2 - omega^2); the Fresnel step ((n - 1) / (n + 1))^2; the chain's 1.034, 1.083, 1.159 against 1.043, 1.104, 1.200 | the chain's 0.8 to 3.4 percent below the closed form at s = 12 (the faces' steps) |
| the rest cavity (form (I)) | section 4's table: 0.2417 at s = 12 on a cube; the quadrature with the pair | the lattice's residual |
| (h), 10, 2a, 2b, 9 | unchanged: light is massless and its pins are DESIGN.md's | as declared |
| 12, 13 | the coefficient at a crowd from its massive records' index by section 7's g; 2.00 and 1 + gamma_PPN to compute from g, G and the pairs | the residual |

## 10. The force between two blocks through light

Reviewer 3's closed form (PUSH_BALANCE.md section 10, the coupled-oscillator
force between two emitters at their own frequency): the force on block 1 is
2 A^2 cos(k L) toward the partner, the equilibria at L = m lambda_0 / 2
alternately stable and unstable by the clocks' relative phase; with the
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
3. The check worlds, in order: (i) ONE BLOCK AT REST, its mode's frequency
   and extent against section 4 (C6's eigenvalue, the threshold table);
   (ii) the block pushed to k = 3, its clock against section 8's one formula
   (the well regime 0.8065, the cavity regime 0.7128 at mu = 0.05); (iii) the
   rest cavity of form (I) against section 4's table, and moved, against
   gamma_m^2 (the control); (iv) the light clock on two blocks at rest (row
   (d): 2 L / c + 2 tau_g) and in motion (rows (e), (f): 1 and 1 with the
   second term), the light emitted through the source term of section 7,
   decaying in tau; (v) the index block (n from g, G). Nothing found,
   everything checked.
4. The key `massive-record-v1` OFF by default; the build only on Reviewer
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
| the sink (7), either form | a DECLARATION, the owner's word | (D) or the take | PASS |
| the motion (8) | a derivation, no sentence added | none needed | none needed |

**The scripts beside this document, each printing its record (`.out`),
COMPUTATION only, no engine run:** `massive_c_derivation.py` (section 1.1),
`massive_corner_stability.py` (sections 2 and 3), `massive_dielectric_index.py`
(section 7), `massive_light_self_trapping.py` (section 4 (III), the
negative result), `massive_cube_threshold.py` (section 4, the exact table,
the window, light's norm bound), `massive_block_clock_motion.py` (section 8).
Run each as its docstring says; the numbers in this document are theirs.

**Not computed here, and said so:** the moving block's index against the
resting one (a chain check of a minute, after the owner's word on the index
in motion); the click's completion under the sink (after his word); the
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
| CLICKS (the reading in the Outside) | (E) the evaluation, chapter 2.5: the object's record is one element of Z[Z_N] across R; the click when the object's own motion, driven by light and summed across its cells into its pointer, crosses the declared rung of the declared wheel W; the click line with the object's own count (its mode's cycles) and the light record's birth stamp; the completion by the sink (the owner's word) | W, the sensitivity; the sink's pair | as DESIGN.md section 5 | the reading, after the last group operation |
| MOVES (the step; the momentum) | (T) the drive with the accumulator and the remainder, chapter 2.1; the momentum changed by the stress of the total field at the object's outer Ports, section 5 | Q S M x 56 d; the tie | as section 5 | yes: the stress the field's own |

Nothing else connects the object to the board: no declared train (derived
as the decaying emission, section 7), no grace, no fan, no one-way take
beyond the sink, no timer, no clock sentence for the object (its clock is
its mode); the receiver forms of DESIGN.md section 5 (the mirror, the
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
  receives at 2 L / c plus the modes' response lags: N_0 = 2 L / c + 2
  tau_g; the register's 206 at L = 60 with the massless lamp's hard onset
  the limit of a stiff coupling.
- The light clock in motion: section 8's one formula, the well regime: 1
  and 1 in the objects' own counts to the second term, gamma_m N_0 in the
  lattice's intervals.
- The polariser and the tables: the second member of the re-emission table
  (a phase on the wheel) is the object's mode's phase relative to the
  arriving light's, set by the mode's response (the resonance's
  quadrature), a COMPUTATION; Malus and Bell as consequences of the
  coupling's phase, to be derived before any run, never found.

**What the engine implements, from this section, in order**: section 11's
order; the board checks, the algebra leads.
