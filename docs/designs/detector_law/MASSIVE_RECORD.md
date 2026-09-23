# The massive record kind and the foreign object as a block: closed from the algebra before the board

The chief physicist's design of 2026-09-23 on the model owner's words, under
the key `massive-record-v1`, OFF by default; docs and pins only; no build.
It stands beside [DESIGN.md](DESIGN.md) (the massless kind, light, unchanged)
and [PINS.md](PINS.md); the algebra of the push and the boost is Reviewer 3's
`PUSH_BALANCE.md` (docs/designs/detector_law/, at d69c87a9 on `push-balance-r3`, PR
#1043; its section 10, the massive record, cited when it lands, not
rewritten). Every number here is a COMPUTATION from the rule, written before
the board runs it; the board, when it runs, checks the algebra bit for bit,
never the reverse.

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
- (12:10Z, to the chief physicist; record 1370) A detector is one cell from
  outside holding many cells inside it, on the board, by locality; the
  cells produce its frequency at rest; there a real clock can be defined;
  its click in the Outside is read across its cells.
- (12:35Z, to the chief physicist) "Derive everything algebraically, then
  implement in the engine to check; a foreign object is a kind of group
  object like the rest": DESIGN.md's placement (section 1 here).

## 1. The one rule, with the self pair

The interval's map at every Node, on a record's row `(a_now, a_before, r)`,
with the record's declared pair `[p, q]` (`[0, 1]` for light):

    3 q a_next + r' = q (a_E + a_W + a_N + a_S + a_U + a_D)
                      - 3 q a_before - 3 p a_now + r,      0 <= r' < 3 q

(Reviewer 3's 8.7 integer form). At `p = 0` it is DESIGN.md section 2's rule
bit for bit (the division by 3 q against 3 with the same remainder's
grain). The self term is the ONE addition: a rate on the record's own row,
linear in the row, with a declared pair. The three tests: generic (one
primitive, one declared pair, no family name; light is the value `p = 0`);
vector (verb T, the translation of the accumulator by a rate at most
bilinear in the state, here linear; verb D, the division with the remainder
kept; no root, no float); local (the record's own row and its six
neighbours; nothing kept at a Node). PASS, PASS, PASS.

**The algebraic placement** (DESIGN.md's dictionary, GROUP_STRUCTURE.md
sections 1 and 8): no new group and no new verb. A foreign object is (i) a
finite set R of Nodes, a G_48-set (its shape group the stabiliser of R; a
cube is the 48's own shape, a square on a layer the stabiliser of the
layer's normal), declared; (ii) the same map on R with the self pair on the
record's own row; (iii) its clock the bound eigenvector of the map on R,
its eigenvalue's argument omega_0 on the circle, a CHARACTER of the time
translation at k = 0, one element of Z[Z_N] carried by all the cells of R in
step (the same object a record's phase is, spread over many cells); light
has no such character at k = 0 (its zero mode is a level, not a clock): the
whole difference between light and a foreign object in the algebra is a
gap; (iv) its motion the characters (omega, **k**) on the surface of
section 2, the rest object at **k** = 0, the moving one the phase wave; (v)
its momentum the existing **p** in Z^3 as the character's **k**, the step
the existing verb T, the push the stress at its Ports (DESIGN.md 5.1 (a));
(vi) its click the evaluation E and the norm read across R.

## 2. The dispersion surface, the gap, the rest frequency (COMPUTATION)

The characters (omega, **k**) of the map:

    3 (2 cos omega - 2) = SUM over i (2 cos k_i - 2) - 3 p / q,

the continuum limit omega^2 = omega_0^2 + c^2 |**k**|^2 with omega_0^2 =
p / q and c^2 = 1 / 3. At **k** = 0 the gap: omega_0 = arccos(1 - p / (2 q)),
the rest period N_0 = 2 pi / omega_0 in intervals:

| [p, q] | omega_0 (lattice) | N_0 intervals | sqrt(p / q) (continuum) |
| --- | --- | --- | --- |
| [1, 64] | 0.1251 | 50.2 | 0.1250 |
| [1, 16] | 0.2507 | 25.1 | 0.2500 |
| [1, 4] | 0.5054 | 12.4 | 0.5000 |
| [1, 1] | 1.0472 | 6.0 | 1.0000 |

The floors of DESIGN.md 1.2 apply to N_0: the band's top at the period 5.10
intervals (N >= 6, so p / q <= 1 at rest), the honest floor N >= 21 (p / q
<= 0.09). The mass of the record IS the pair: the rest energy h omega_0,
de Broglie's internal clock; nothing else names it.

## 3. The conserved form with the mass term

    E_m = 3 SUM over Nodes (a_now - a_before)^2
          + SUM over Links (a_now(x) - a_now(y)) (a_before(x) - a_before(y))
          + 3 (p / q) SUM over Nodes a_now a_before,

in integers times q; conserved to the remainder's grain as DESIGN.md 2.1's
E (the same leapfrog, one more quadratic term); positive-semidefinite on
the board for p / q <= 1 (the checkerboard's double root at p = 0 is lifted
by the mass term: the checkerboard oscillates at the band's top, no secular
growth). The norm the rungs divide is E_m; the Port's factor of 2.1 applies
with the mass term's share named.

## 4. The foreign object as a block: the shape a declaration, the rest clock a computation

The object is a block of side s (a square of s x s cells on a layer; a cube
of s^3 on the board), every cell carrying the same self pair `[p, q]`; the
shape is a declaration (kind 1), as the owner said. What confines the
record to the block is the one thing the algebra must name, and there are
three forms, each with its consequence:

- **(I) The block's faces as mirrors for its own record**: outside the
  block the object's record is held at 0 (the mirror form of DESIGN.md
  section 5, declared on the block's faces for its own record). Then the
  block is a cavity, and its modes are the standing waves of a box of s
  cells with Dirichlet faces, k_i = pi / (s + 1) per axis; the lowest
  mode's frequency from section 2's surface:

  | s | a square on a layer: omega, N | a cube: omega, N | the continuum c pi sqrt(dim) / (s + 1) |
  | --- | --- | --- | --- |
  | 3 | 0.6356, 9.9 | 0.7854, 8.0 | 0.6413, 0.7854 |
  | 6 | 0.3654, 17.2 | 0.4488, 14.0 | 0.3664, 0.4488 |
  | 12 | 0.1972, 31.9 | 0.2417, 26.0 | 0.1973, 0.2417 |
  | 24 | 0.1026, 61.3 | 0.1257, 50.0 | 0.1026, 0.1257 |

  with the self pair added, the rest frequency is the quadrature to the
  lattice's residual (s = 12 on a layer with [1, 16]: 0.3195 exact against
  sqrt(0.2507^2 + 0.1972^2) = 0.3189). So a block of side s has a real
  rest clock even at p = 0 (a confined massless record has a lowest mode,
  as a photon in a box), and the pair raises it. The owner's "N derives how
  many cells": N_rest(s, p, q) ties the three; declare the pair and s, the
  frequency follows; or declare N and the pair, s follows. This is the form
  the design carries.
- **(II) The free massive packet**, no faces: a packet of width s of the
  massive record at **k** = 0 is an exact solution of the covariant
  equation in the continuum, and it SPREADS: the dispersion of a packet of
  width sigma = s / 2 has the time tau = 2 sigma^2 omega_0 / c^2 = 6 sigma^2
  omega_0: 54 intervals (2 rest periods) at s = 12 and [1, 16]; 227 at s = 12
  and [1, 1]; 907 at s = 24 and [1, 1]; 15750 at s = 100 and [1, 1]. A free
  packet at the sizes of the register's worlds is not an object; the form
  is named and not carried.
- **(III) The well of the pair**: a lower pair inside than outside (the
  massive record everywhere, the block the region where its pair is
  smaller). The bound mode exists in one dimension always and on the board
  above a threshold (Reviewer 3's section 10, the closed form and the
  threshold, cited when it lands); its frequency lies between the inner
  and the outer gaps; its extent is a computation from the depth and s.
  Lawful, one declared pair more (the outside's); the design carries (I)
  as the simpler one and names (III) as the second lawful form.

Under (I) and (III) alike, what holds the cells of one object together is
the DECLARATION of the region (the faces, or the pair's region), not a
derivation; the design says so, as the owner's "the shape a declaration".

## 5. The block's momentum, step and push

One integer per axis for the whole block, **P**, with its remainder (the
owner's "one body"): the stress of the total field (DESIGN.md 5.1 (a)) at
every outer Port of the block, summed into **P** (verb G over the block's
Ports, then D with the remainder kept: the sum over the block's own faces is
the block's own record's reading, local to the block's cells; a host
gather is not needed, each face's cell adds its Port's stress to the
block's integer as a detector set's cells add to one pointer today). The
step: the accumulator per axis against 3 Q S M x 56 d with M the block's
content, the remainder kept; the whole block steps one Link together (its
faces, its pair region and its record's rows translate by verb T). The
bound |**v**| < c on the vector (3 (**P** . **P**) < (3 Q S M x 56 d)^2), a
crossing the world's stop with a diagnostic (DESIGN.md 1.2 (c)). The three
tests as in 5.1 (a). What the block feels: light's stress at its outer
Ports; what it does to light: section 7.

## 6. The click of a block, read by light

A light record arriving at the block's cells offers its motion at the
block's Ports as at any receiver (DESIGN.md section 5, the receiver forms;
the block's outer faces one declared form for LIGHT, the sponge or the
Port's take, beside the mirror they are for the block's OWN record); the
block's pointer accumulates across all its cells (the owner's "the click in
the Outside is read across its cells"); the click at the declared rung of
the declared wheel W; the click line with the block's own count (its own
mode's cycles, section 4) and the record's birth stamp. The evaluation E
of the block's element of Z[Z_N] and the norm, as every record's click.

## 7. The one coupling to light

What light sees at the block's cells is the index pair of DESIGN.md 5.1 (b)
declared as the massive record's PRESENCE: at a cell of the block, light's
six-neighbour term carries q_light = [num, den] with den / num = 1 + kappa
E_m(cell) / E_ref, kappa the one declared coupling, E_m the block's own
record's energy density at the cell (section 3), E_ref a declared unit; at
the block's rest mode E_m is stationary and the index is a constant of the
block (the reactive relay of 5.1 (b), which scatters, reflects the Fresnel
step and can bind through light). Generic (one pair, one declared kappa);
vector (the rate of light's row bilinear in the state: the block's E_m
times light's row, allowed as "at most bilinear"); local (the cell's own
two records). This is also MUST E's definition of A under the rule (6.7
form (b)): a crowd is its massive records on the Nodes around it, and
their E_m sets light's pace there, rows 12 and 13's mechanism; the
function, the pair from E_m, is this declaration.

## 8. The motion: what the algebra gives, said plainly (COMPUTATION)

- The free massive record's characters follow the continuum surface to
  0.1 percent at k <= 0.3 per Link ([1, 16]: omega 0.2523, 0.2573, 0.2762,
  0.3050 at k = 0.05, 0.1, 0.2, 0.3 against 0.2523, 0.2572, 0.2760, 0.3047;
  the group pace 0.067, 0.131, 0.243, 0.328 Links per interval): the boost
  of a free rest packet IS the moving packet, its frequency omega_0
  gamma_m, its internal phase advancing at omega_0 / gamma_m per interval
  along its path, its width s / gamma_m: Lorentz REACHED as a relation on
  the characters, not added to the 48. But a free packet spreads (section
  4 (II)).
- A block confined by its declared faces (I) or its declared pair region
  (III) that steps RIGIDLY (its shape carried unchanged, section 5) is a
  moving cavity: its standing-wave cycle in the lattice's intervals is
  2 L c / (c^2 - beta^2) = gamma_m^2 x 2 L / c along the motion and 2 L /
  sqrt(c^2 - beta^2) = gamma_m x 2 L / c across (gamma_m^2 = 1.500, 1.231,
  1.091 at k = 3, 4, 6): the MEDIUM's row (DESIGN.md 8b (iii)), not
  Lorentz; five's ratios 1.50 and 1.22 at k = 3; the lab's dilation
  gamma_m^2 along. This is a theorem of the linear rule with a declared
  rigid shape, and it is what the board will read if the shape is carried
  rigidly.
- Lorentz for a CONFINED object therefore needs one of two things, neither
  in the design as it stands, both named for the owner's word: (a) the
  shape's declaration in motion is the contracted one, s / gamma_m along
  (the region or the faces boosted with the block: `lorentz-shape-v1`, a
  hypothesis under its own identity; with it the moving cavity's cycle is
  gamma_m x 2 L / c along and across, the object's own count N_0 in both
  arms, five 1 and 1, the lab's dilation gamma_m, rows 4a, 4b, 5b PASS by
  the covariance of the field equation with a transformed confinement); or
  (b) the confinement made of the record itself (the pair at a cell a
  function of the record's own E_m there, a cubic rate, a soliton), which
  is a seventh verb (the rate is not bilinear) and enters only if the
  owner admits the verb. The algebra does not choose between them; it says
  that the declared rigid block gives the medium's clock and that Lorentz
  costs one declaration or one verb. Nothing is run to find out what the
  algebra already says.

## 9. The light clock on two blocks: the pins as consequences

Two blocks of side s, pair [p, q], at L Links (face to face) on a layer; a
light record inserted by block A at its own mode's frequency (the block's
clock, section 4) and received by B and back (the light record massless,
DESIGN.md unchanged):

| Row | The consequence of the algebra (COMPUTATION, before any board run) | The band |
| --- | --- | --- |
| (d) at rest | N_0 = 2 L / c less the precursor's lead (207.85 - about 1 at L = 60, at the hard onset and the declared W), in the lattice's intervals; in the block's own count N_0 / N_rest(s, p, q) | the rung's grain and the lattice's residual |
| (e), (f) rigid blocks | N_par / N_0 = gamma_m^2 (1.500 at k = 3), N_perp / N_0 = gamma_m (1.225): five FAIL, 5b FAIL, 4a FAIL, by the theorem of section 8; the block's own count the same ratios | the residual |
| (e), (f) under `lorentz-shape-v1` | N_par / N_0 = N_perp / N_0 = gamma_m in the lattice's intervals, 1 and 1 in the block's own count: five PASS, 5b PASS, 4a PASS (the block's count slow by gamma_m), 4b PASS (gamma (1 + beta)) | the residual |
| (g) the block at rest | its self-click its own mode, N_rest(s, p, q) exactly, no return and no timer; the clock sentence of DESIGN.md section 8 not needed for it (it remains the declaration of the one-Node objects of the pilot's worlds on the massless rule) | exact |
| (h), 10, 2a, 2b, 9 | unchanged: light is massless and its pins are DESIGN.md's | as declared |
| 12, 13 | the coefficient at a crowd from E_m by section 7's coupling; 2.00 and 1 + gamma_PPN as the consequence to compute from the coupling, not to find | the residual |

No pin is found by a run; the board's run checks these numbers.

## 10. The force between two blocks through light

Reviewer 3's closed form (PUSH_BALANCE.md, the coupled-oscillator force
between two emitters at their own frequency; DESIGN.md 5.1 (b)): the force
on block 1 is 2 A^2 cos(k L) toward the partner, the equilibria at L = m
lambda_0 / 2 alternately stable and unstable by the clocks' relative phase.
A consequence of the algebra, written here before any board run; the
board's two-block world reads it.

## 11. What the engine implements, and in what order

1. The rule with the pair per record (one added rate; light `[0, 1]`).
2. The block: a declared square or cube of side s with its pair, its faces
   the mirror for its own record (I), one declared receiver form for
   light, one momentum integer per axis with its remainder, the rigid step.
3. The coupling of section 7 (one kappa), the click of section 6.
4. The worlds: one block at rest (its own mode's frequency against section
   4's table, bit for bit to the residual); the two-block light clock at
   rest (row (d)); in motion at k = 3 (the theorem of section 8: gamma_m^2
   and gamma_m, the board checking the algebra); then, only on the owner's
   word, `lorentz-shape-v1` or the verb.
5. The key `massive-record-v1` OFF by default; the build only on Reviewer
   3's gate of this design and its section 10, the independent
   mathematician's check the Boss opens, and the owner's second word; the
   engine's numbers reported against the algebra's, never the algebra
   moved to the engine's.

## 12. The three tests, per sentence, and what is not computed

| Sentence | Generic | Vector | Local |
| --- | --- | --- | --- |
| the rule with the self pair (1) | PASS | PASS (T, D) | PASS |
| the block's shape (4) | a declaration, kind 1 | a declaration | the block's cells |
| the faces as the own record's mirror (4 (I)) | PASS (the mirror form) | PASS | PASS |
| the block's momentum and step (5) | PASS | PASS (G, D, T) | PASS (the block's own Ports) |
| the click across the cells (6) | PASS | PASS (E) | PASS (the block's pointer) |
| the coupling to light (7) | PASS (one kappa) | PASS (bilinear) | PASS |
| `lorentz-shape-v1` (8 (a)) | a hypothesis under its own identity | a declaration | the block's cells |
| the soliton (8 (b)) | a seventh verb: not in the law | FAIL as written (cubic) | PASS |

Not computed here, and said so: the bound mode's threshold on the board
for form (III) (Reviewer 3's section 10); the block's mode with the mass
term at general s and [p, q] beyond the quadrature (the exact eigenvalue
of the map on R, seconds on the host, to be printed by the algebra script
before the build, never after); the coupling's kappa against any nature
row (rows 12 and 13 need the crowd's E_m, a world to declare).
