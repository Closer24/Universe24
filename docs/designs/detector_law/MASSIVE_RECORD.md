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
- (13:05Z, to the chief physicist) On the choice the first draft of section 8
  put to him: "there is something we do need to take from the algebra, and
  it derives itself, and I do not need to decide." Sections 4, 7, 8 and 9
  below are re-formed on it: the motion is derived, not decided.
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

**In ALGEBRA.md's terms** (the Boss's order of 12:48Z: chapter 1's
objects, the dictionary's row for the self pair, chapter 2's maps), one
line per sentence of this design:

| Sentence | ALGEBRA.md object or map | The dictionary's row |
| --- | --- | --- |
| the self term -(p / q) a_now | chapter 2.1, (T) the translation of the row's accumulator by a rate linear in the row, the pair [p, q] a declared rate; then 2.6 (D) the division by 3 q with the remainder kept | NEW ROW: **mass of a foreign object**: the pair [p, q] of the self term on its record's own row; the rest frequency omega_0 = arccos(1 - p / (2 q)) on the circle; the rest energy h omega_0 (de Broglie's clock); the content M = E'_0 / (Q S) of the existing row read from it, not declared beside it |
| the block R | chapter 1, the translation group of the torus acting on Nodes; R a finite G_48-set, its shape group the stabiliser | shape: a declaration (kind 1), as a detector set |
| the block's clock | chapter 1, the phase circle Z_N and its group ring Z[Z_N]: one element carried by the cells of R in step; the bound eigenvector of the interval's map on R; a character of the time translation at k = 0 | time, a clock: the block's own count of its mode's cycles (replaces "a body's count of self-creations") |
| the motion | the characters (omega, **k**) of the time-and-space translations on the surface of section 2; the boost a relation on the characters, not among the 48 | Lorentz: reached as a relation on the characters (the dictionary's line kept: no boost among the 48) |
| the momentum and the step | chapter 2.1, (T) the drive: **p** in Z^3 as the character's **k**; the accumulator per axis against 3 Q S M x 56 d, the remainder kept | momentum of a body: **p** in Z^3, moved by the push and read by the drive (unchanged) |
| the push | chapter 2.2, (B) the bilinear form: the stress T_ii = 3 (motion)^2 + (strain)^2 at the outer Ports, a quadratic form of the state with the declared matrix diag(3, 1) | force, the push: the stress at the Ports (replaces the coupling matrix times the flow vector for the massless kind) |
| the click | chapter 2.5, (E) the evaluation of the block's element of Z[Z_N] and the norm, across R; the wheel W declared | a measurement: a click at a detector; the block's count between clicks |
| the coupling to light | chapter 2.2, (B): light's pair at a cell a bilinear reading of the block's E_m there, one declared kappa | gravity's column and the index: the crowd's E_m sets light's pace (rows 12 and 13) |
| the conserved form E_m | chapter 4's identities: the leapfrog's quadratic form with the mass term, an integer times q | energy: E_m the record's, E'_0 = Q S M the block's rest energy read from omega_0 |

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

## 4. The foreign object as a block: the shape's symmetry a declaration, its extent and clock a derivation

The object is a block of side s (a square on a layer, a cube on the board),
every cell carrying the same self pair `[p, q]`. What confines the record to
the block is the one thing the algebra must supply, and the owner's word of
13:05Z fixes how: nothing about the block's extent is DECLARED IN MOTION; the
extent is what a BOUND STATE gives, so that the block's boost is the boost of
a solution (section 8). Three forms, with their standing:

- **(I) The block's faces as mirrors for its own record** (a declared
  cavity): outside the block the object's record is held at 0. The modes
  are the standing waves of a box of s cells with Dirichlet faces, k_i =
  pi / (s + 1) per axis; the lowest mode's frequency from section 2's
  surface:

  | s | a square on a layer: omega, N | a cube: omega, N | the continuum c pi sqrt(dim) / (s + 1) |
  | --- | --- | --- | --- |
  | 3 | 0.6356, 9.9 | 0.7854, 8.0 | 0.6413, 0.7854 |
  | 6 | 0.3654, 17.2 | 0.4488, 14.0 | 0.3664, 0.4488 |
  | 12 | 0.1972, 31.9 | 0.2417, 26.0 | 0.1973, 0.2417 |
  | 24 | 0.1026, 61.3 | 0.1257, 50.0 | 0.1026, 0.1257 |

  with the self pair added, the rest frequency is the quadrature to the
  lattice's residual (s = 12 on a layer with [1, 16]: 0.3195 exact against
  sqrt(0.2507^2 + 0.1972^2) = 0.3189). This form is the ILLUSTRATION of a
  confined record's rest clock (a confined massless record has one too, as
  a photon in a box; the pair raises it): it is NOT the object's
  definition, because a declared wall carried in motion is not covariant
  (section 8).
- **(II) The free massive packet**, no wall: covariant, and it SPREADS
  (the packet's time tau = 2 sigma^2 omega_0 / c^2 = 6 sigma^2 omega_0: 54
  intervals at s = 12 and [1, 16]; 227 at s = 12 and [1, 1]; 907 at s = 24
  and [1, 1]; 15750 at s = 100 and [1, 1]); not an object at the register's
  sizes. Named, not carried.
- **(III) The bound state of the coupled records, CARRIED**: the massive
  record and light coupled MUTUALLY in the one-wall form the law already
  has (section 7): each record's pace at a cell is lowered where the other
  record's amount is high. A region where the massive record sits slows
  light there, which gathers there, which slows the massive record there,
  which stays: a self-consistent bound state of the two records on the
  board, its existence above a threshold in the coupling, its rest
  frequency and extent a COMPUTATION from the pair and the one coupling
  kappa (the self-consistent eigenproblem of the two interval maps on the
  board; Reviewer 3's section 10 and the Algebra Mathematician's chapter,
  cited when they land). Its shape on a cubic lattice has the cube's
  symmetry (the 48), so the owner's square block is its shape by the
  algebra; s is read from the bound state, not declared. Nothing rigid is
  declared: the block IS this solution, and its boost is section 8's.

The owner's "N derives how many cells" holds in (III) as a derivation:
N_rest(p, q, kappa) and s(p, q, kappa) come together from the bound state.
Form (I)'s table remains the check of the rest clock of a confined record
at a given s, a COMPUTATION the board must reproduce when a wall is
declared for a rest world; it is never carried into motion.

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

## 7. The one coupling, in the law's own one-wall form, both ways

The coupling between the two record kinds is the ONE-WALL FORM the law
already has (DESIGN.md 4.1, MUST E): at a cell, a record's six-neighbour
term carries the pair [d^2, (d + f n A)^2] with A the OTHER record's amount
at the cell (the integer magnitude of its row, a scalar of that record)
and f n the one declared coupling kappa; the compensated form of 5.1 (b).
Both ways: light's pace at a cell is lowered by the massive record's amount
there (what light sees: the index of a block, the reactive relay that
scatters, reflects the Fresnel step and binds two blocks through light,
DESIGN.md 5.1 (b); rows 12 and 13's mechanism, the crowd's A being its
massive records' amounts, MUST E's definition of A under the rule), and the
massive record's pace at a cell is lowered by light's amount there (what
binds the block, section 4 (III)). The three tests: generic (one pair form,
one declared kappa, no family name; the same form for every record kind);
vector (verb T, the rate of a record's row at most bilinear in the state:
a linear function of the other record's amount times the row; then D);
local (the cell's own two records). The coupling reads an amount (a scalar
of the other record), not its energy density, and that is what keeps the
coupled rules covariant in the continuum (the amount of a scalar record
transforms as a scalar); a coupling through E_m, the first draft's, would
not, and is withdrawn.

## 8. The motion: derived, not decided (COMPUTATION)

- **The characters follow the covariant surface.** The free massive
  record's characters lie on section 2's surface to 0.1 percent at k <=
  0.3 per Link ([1, 16]: omega 0.2523, 0.2573, 0.2762, 0.3050 at k = 0.05,
  0.1, 0.2, 0.3 against the continuum 0.2523, 0.2572, 0.2760, 0.3047; the
  group pace 0.067, 0.131, 0.243, 0.328 Links per interval). The boost of
  a rest state at omega_0 to the pace v is the character with the carrier
  k = gamma_m omega_0 v / c^2: on the lattice its frequency is 0.3070,
  0.2782, 0.2618 at k = 3, 4, 6 against gamma_m omega_0 = 0.3062, 0.2774,
  0.2611 (+0.3 percent), and its internal phase advances by omega - k v =
  0.2049, 0.2261, 0.2401 per interval against omega_0 / gamma_m = 0.2041,
  0.2253, 0.2394: THE CLOCK SLOWS BY 1 / gamma_m AND THE PACKET CONTRACTS BY
  1 / gamma_m, on the lattice's own surface, to the residual. Lorentz is
  reached as a relation on the characters (the dictionary's line: no boost
  among the 48), and nothing is declared for it.
- **Every rule of the design is covariant in the continuum**: the massless
  rule, the massive rule with its self pair, and the coupling of section 7
  through the other record's amount (a scalar). Therefore the boost of any
  rest SOLUTION is a solution: the bound state of section 4 (III) at rest,
  boosted, is the contracted and slowed bound state; its own count per
  cycle unchanged; its cycle in the lattice's intervals gamma_m N_0; its
  extent along the motion s / gamma_m. That is the derivation the owner's
  word of 13:05Z names: it derives itself, and no one decides it.
- **The theorem on declared rigid shapes, kept for what it says**: a block
  whose extent is DECLARED and carried unchanged in motion (a rigid cavity
  of form (I), or a rigid pair region) is not a boosted solution, and the
  linear rule gives it the MEDIUM's clock, 2 L c / (c^2 - beta^2) = gamma_m^2
  x 2 L / c along and gamma_m x 2 L / c across (1.500 and 1.225 at k = 3):
  DESIGN.md 8b (iii)'s row. This is why the design declares no extent in
  motion; the first draft's "choice" between a declared contraction
  (`lorentz-shape-v1`) and a cubic self term (a seventh verb) is WITHDRAWN:
  the contraction is what the covariant bound state does, and the coupling
  of section 7 is bilinear, so no verb is added.
- **What remains a derivation to complete** (the one open item): the bound
  state's existence, threshold, rest frequency and extent on the board
  from the pair and kappa (section 4 (III)); Reviewer 3's section 10 and
  the Algebra Mathematician's chapter. Until it is written, the board runs
  nothing of the motion; when it is, the board checks it.

## 9. The light clock on two blocks: the pins as consequences

Two bound blocks (section 4 (III)) at L Links face to face on a layer; a
light record inserted by block A at its own mode's frequency and received
by B and back (the light record massless, DESIGN.md unchanged):

| Row | The consequence of the algebra (COMPUTATION, before any board run) | The band |
| --- | --- | --- |
| (d) at rest | N_0 = 2 L / c less the precursor's lead (207.85 - about 1 at L = 60, at the hard onset and the declared W), in the lattice's intervals; in the block's own count N_0 / N_rest(p, q, kappa) | the rung's grain and the lattice's residual |
| (e), (f) in motion at k = 3 | the bound blocks boosted: L_along = L_0 / gamma_m, L_across = L_0; the cycle gamma_m N_0 in the lattice's intervals along AND across; the blocks' own count per cycle N_0 / N_rest in both arms: N_par / N_perp = 1, five 1 and 1, 5b PASS | the residual, about 0.3 percent at k = 3 |
| 4a | the block's own clock slow by 1 / gamma_m in the lattice's intervals (its internal phase's advance omega_0 / gamma_m): the muon's row PASS in form, the number gamma_m at the world's beta | the residual |
| 4b | the boosted block's emission read by a block at rest: 1 + z = gamma_m (1 + beta_c) receding (the character's frequency gamma_m omega_0 shifted by the Doppler of the medium) | the residual |
| (g) the block at rest | its self-click its own mode, N_rest(p, q, kappa), no return and no timer; the clock sentence of DESIGN.md section 8 not needed for it (it remains the declaration of the one-Node objects of the pilot's worlds on the massless rule) | exact to the residual |
| a declared rigid block (a rest world with form (I)'s walls, moved) | gamma_m^2 and gamma_m: the theorem of section 8, a check the board makes on a declared rigid world, never a pin of the object | the residual |
| (h), 10, 2a, 2b, 9 | unchanged: light is massless and its pins are DESIGN.md's | as declared |
| 12, 13 | the coefficient at a crowd from its massive records' amounts by section 7's coupling; 2.00 and 1 + gamma_PPN the consequence to compute from the coupling, not to find | the residual |

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
2. The coupling of section 7 (one kappa, the one-wall form both ways); the
   block as the bound state of section 4 (III): its cells where its record
   is, one momentum integer per axis with its remainder, the step of the
   whole solution by verb T; one declared receiver form for light at its
   cells; the click of section 6.
3. A rest world with form (I)'s declared walls, for the check of the
   confined record's rest clock against section 4's table only.
4. The worlds: the bound block at rest (its frequency and extent against
   the derivation); the boosted bound block at k = 3 (its frequency
   gamma_m omega_0 and its extent s / gamma_m against section 8); the
   two-block light clock at rest (row (d)) and in motion (rows (e), (f):
   1 and 1); the declared rigid world moved, as the check of section 8's
   theorem; nothing found, everything checked.
5. The key `massive-record-v1` OFF by default; the build only on Reviewer
   3's gate of this design and its section 10, the independent
   mathematician's check the Boss opens, and the owner's second word; the
   engine's numbers reported against the algebra's, never the algebra
   moved to the engine's.

## 12. The three tests, per sentence, and what is not computed

| Sentence | Generic | Vector | Local |
| --- | --- | --- | --- |
| the rule with the self pair (1) | PASS | PASS (T, D) | PASS |
| the block as the bound state (4 (III)) | PASS (a solution of the coupled rules, no declaration) | PASS (T, D on each record) | PASS |
| the faces as the own record's mirror (4 (I), a rest-world check only) | PASS (the mirror form) | PASS | PASS |
| the block's momentum and step (5) | PASS | PASS (G, D, T) | PASS (the block's own Ports) |
| the click across the cells (6) | PASS | PASS (E) | PASS (the block's pointer) |
| the coupling, both ways (7) | PASS (one kappa, the one-wall form) | PASS (bilinear through the amount) | PASS |
| the motion (8) | a derivation, no sentence added | none needed | none needed |

Not computed here, and said so: the bound state's existence, threshold,
rest frequency and extent on the board from the pair and kappa (section 4
(III); Reviewer 3's section 10 and the Algebra Mathematician's chapter, an
algebra script to print them before the build, never after); form (I)'s
exact eigenvalue at general s and pair beyond the quadrature; kappa
against any nature row (rows 12 and 13 need the crowd's amounts, a world
to declare).

## 13. Where the board stopped, and how a foreign object connects to it, in the algebra

The owner's word (13:25Z, to the chief physicist): nothing is run; we
continue from where the board stopped, which is the OUTSIDE, at the foreign
object; check exactly how the foreign object connects to the board,
algebraically, and derive it to the board from there.

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
foreign object is its cells R (section 1) carrying its massive record; a
light record reaching a cell of R meets the object through exactly these:

| What the object does | The verb, in ALGEBRA.md's terms | The declared integer | The three tests | Covariant |
| --- | --- | --- | --- | --- |
| INSERTS light and RECEIVES light (the lamp, the detector: the same thing) | (B) the bilinear form with a declared matrix, chapter 2.2: at a cell the two records' rows are coupled by the matrix **C** = [[0, g], [g, 0]]: light's row gains g times the massive row's amplitude per interval (the insert: the object's own oscillation at omega_0 drives light at its cells, a lamp at the object's rest frequency, no train declared), and the massive row gains g times light's amplitude (the receive: light arriving drives the object's record). One declared pair g, the same both ways (the law's coupling matrix, symmetric). | g = [g_n, g_d] | generic (one matrix form, no family name; light and the object values); vector (B with a declared matrix, linear in the other record's row); local (the cell's own two records) | yes: a linear coupling of two scalar records |
| SCATTERS, REFLECTS, BINDS (the index, the mirror's limit, the wall, the air; the force between two objects) | (T) with the one-wall pair, section 7: light's pace at the cell lowered by the massive record's AMOUNT there, and the massive record's by light's; the pair [d^2, (d + f n A)^2], A the other's amount | kappa = f n | as section 7 | yes: through a scalar amount |
| CLICKS (the reading in the Outside) | (E) the evaluation, chapter 2.5: the object's record is one element of Z[Z_N] across R; the click when the received light's motion, summed across the object's cells into its pointer, crosses the declared rung of the declared wheel W (the counting form, DESIGN.md section 5); the click line with the object's own count (its mode's cycles) and the light record's birth stamp | W, the sensitivity | as DESIGN.md section 5 | the reading, after the last group operation, as the reading rule says |
| MOVES (the step; the momentum) | (T) the drive with the accumulator and the remainder, chapter 2.1; the momentum changed by the stress of the total field at the object's outer Ports, section 5 (the bilinear form of the field's differences, chapter 2.2) | Q S M x 56 d | as section 5 | yes: the stress the field's own |

Nothing else connects the object to the board: no declared train, no
grace, no fan, no one-way take, no timer, no clock sentence for the
object (its clock is its mode, section 4 (III)); the receiver forms of
DESIGN.md section 5 (the mirror, the sponge, the Port's take) become
values of these verbs (the mirror the limit of the index; the sponge the
damping the receive's g gives when the object's mode is broad; the take
not needed), to be shown as such when the engine carries them.

**What the algebra then gives for the Outside's readings, derived before
the board runs** (each a consequence of the four verbs; the closed forms
Reviewer 3's section 10 and 11 where they exceed this document):

- The insert: an object at rest oscillating in its mode at omega_0 drives
  light at its cells at omega_0 with the amplitude g times its mode's;
  light leaves at lambda_0 = 2 pi c / omega_0 (the object's rest
  wavelength; the register's lamp declared no clock: here the clock is
  the mode); the power the coupling's, a COMPUTATION from g and the mode.
- The receive: light of the object's own frequency arriving at its cells
  drives its mode resonantly (the resonance Reviewer 3 asked for, now
  the object's own, not declared); light of another frequency drives it
  off resonance, less, by the mode's response; the click's rate per
  arriving motion is this response, a COMPUTATION from g and omega_0; a
  detector "reads" what resonates with it, and the counting form's rung
  is crossed by the object's received motion across its cells.
- The light clock at rest on two objects: A's mode drives light, light
  reaches B at L / c, B's mode is driven and drives light back, A's mode
  receives at 2 L / c plus the modes' response lags (two lags of the
  order of the mode's own period over the coupling's strength, a
  COMPUTATION from g): N_0 = 2 L / c + 2 tau_g, tau_g from g; the
  register's 206 at L = 60 with the massless lamp's hard onset is the
  limit of a stiff coupling (tau_g small against the period).
- The light clock in motion: section 8, derived: 1 and 1 in the objects'
  own counts, gamma_m N_0 in the lattice's intervals.
- The polariser and the tables: the second member of the re-emission
  table (a phase on the wheel) is now the object's mode's phase relative
  to the arriving light's, set by the mode's response (the resonance's
  quadrature), a COMPUTATION; Malus and Bell as consequences of the
  coupling's phase, to be derived in Reviewer 3's section 11 or a section
  of this document before any run, never found.

**What the engine implements, from this section, in order**: (1) the two
record kinds with the pair (section 1); (2) at the object's cells the
coupling matrix **C** (verb B with g) and the one-wall pair with the
other's amount (verb T with kappa); (3) the click across the cells at W;
(4) the momentum from the stress and the step; (5) the worlds in section
11's order, the two-object light clock at rest first (N_0 = 2 L / c + 2
tau_g against the derivation, the modes' frequencies against section 4);
the board checks, the algebra leads. The bound state of section 4 (III)
that gives the object its extent is the one derivation still to be
written before (5); until it is, (1) to (4) are built against the rest
worlds with form (I)'s declared walls as the check of the confined mode,
never against a moving world.
