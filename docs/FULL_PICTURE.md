# The full picture: the choices, the inputs, the derived laws, what we measure, and what can be achieved now

The model owner, 2026-09-21 (translated, record 238): "check how one can
choose the groups, because here a group of 48 was chosen and mass was
added to it; what has to be written down is what the input parameters of
our universe are, and whether they are derived from the expansion or from
what happens now; give a full picture of what happens, with formulas: the
input parameters, what we measure, and what can be achieved now."

This document is the map. It links to the owning documents and copies no
rule: one canonical copy per rule, in [HIGHLIGHTS.md](HIGHLIGHTS.md)
(5.4 the decisions, 5.7 the conversions and the inputs),
[BEAM_LAW.md](BEAM_LAW.md) (the law as built), the vector form
[designs/vector_form/LAW.md](designs/vector_form/LAW.md) (every rule as a
vector operation), [DERIVATIONS_BEAM.md](DERIVATIONS_BEAM.md) (what
follows from the rules), [PREDICTIONS.md](PREDICTIONS.md) (what the law
says against nature), [EXPERIMENTS.md](EXPERIMENTS.md) (the register),
[THREE_WORLDS.md](THREE_WORLDS.md) (every thing in the vector world, the
software world and our world) and [CODE_TO_FORMULAS.md](CODE_TO_FORMULAS.md)
(how the work got here). Notation per record 184: a scalar plain, a
vector bold lowercase, a matrix or an operator bold uppercase, every
symbol named at its first use, Greek letters as words; rows and bodies,
not light and matter. Written by the mathematician on the Boss's order;
nothing here is a new rule.

**The one-line answer to the owner's question.** Today no input parameter
is derived from the expansion or from the present state: the masses,
charges and lifetimes are free ([PREDICTIONS.md](PREDICTIONS.md) entry
26), the grain of the computation is free of the constant K
([DERIVATIONS_BEAM.md](DERIVATIONS_BEAM.md) section 13), and the
expansion's rate H is itself a declared input, absent by default
(section 15).

## 1. The choices, and what follows from them

**What is chosen.** Three things, and every symmetry of the system is a
consequence of them, not a fourth choice:

1. **The dimension d = 3 and the six Ports.** A Node has six neighbours,
   one per signed axis, the L1 neighbourhood of the cubic lattice
   ([HIGHLIGHTS.md](HIGHLIGHTS.md) 3.1; `core/game_board.py`, the Port
   order [+X, -X, +Y, -Y, +Z, -Z]). This is the choice.
2. **The phase circle Z_N**, N chosen per world (64 on the register; 1024
   and 4096 on the Bell worlds at larger N): the cyclic group of the phase
   (`core/phase.py`, `PhaseCircle`), and with it the tables C and S at
   the scale 256, a declared rounding.
3. **The translation group of the torus**: the GameBoard's extents per
   axis, and per axis whether the axis is periodic (a circle) or open (a
   segment whose faces are the border, a click): `Z_X x Z_Y x Z_Z` with
   each factor a circle or a segment, chosen per world.

**What is not chosen: the group of 48.** The cube's group (the signed
permutations of the three axes, 3! x 2^3 = 48; `cube_symmetries` in
`core/game_board.py`; the 24 of hand +1 the rotations, the 24 of hand -1
the reflections, told apart by the hand as a pseudoscalar, BEAM_LAW note
39) is the symmetry of choice 1: every map that preserves the six Ports as
a set and the lattice's Links is one of the 48, and every one of the 48
does. Nothing was added to it; the mass, the charge and the other
contents of the family table live on the amounts, on which the 48 act
trivially (the 48 permute directions and Nodes; a content is a scalar).
And it is the largest point group any three-dimensional lattice can have:
every Bravais lattice's point group is a subgroup of the full octahedral
group O_h of order 48 (the crystallographic restriction), so no other
lattice gains symmetry over the cubic one; a lattice can only keep the 48
(the face-centred and body-centred cubic lattices keep O_h) or lose part
of it (the tetragonal, orthorhombic and lower systems). What the choice
of lattice DOES change is the neighbourhood, and with it the causal front,
c and the collision table:

- **The causal front** is the unit ball of the lattice's step norm, the
  set of Nodes reachable in one interval: the octahedron (the L1 ball,
  six vertices) for the six Ports; the cuboctahedron (twelve vertices,
  the face diagonals (+-1, +-1, 0)) for the face-centred lattice with 12
  neighbours; the cube (eight vertices, the body diagonals (+-1, +-1,
  +-1)) for the body-centred lattice with 8 neighbours; the tetrahedron
  alternating with its mirror for the diamond lattice with 4.
- **c** is the operator norm of the flight ([designs/vector_form/LAW.md](designs/vector_form/LAW.md)
  section 3; [designs/light_speed/FORM.md](designs/light_speed/FORM.md)
  section 1): the largest isotropic Euclidean speed at which no primitive
  direction makes two steps in one interval, `c = min over unit vectors u
  of 1 / (the lattice norm of u)`, the inradius of the front's dual. For
  the six Ports the lattice norm is L1 and `c = 1 / sqrt 3` Links per
  interval, the cube diagonal the bound (`1 / sqrt d` in d dimensions).
  For the face-centred lattice the worst direction is an axis (two
  diagonal steps per two Links) and `c = 1` Link per interval; for the
  body-centred lattice likewise `c = 1`; so a richer neighbourhood raises
  c toward the step length at the cost of more Ports per Node, and the
  L1 lattice is the one whose front is the least computation per
  Euclidean progress (section 13.2 (a)).
- **The collision table** permutes the single units in the Ports' slots
  plus the two rest slots: with six Ports, 8 slots, `3^8 = 6561` joint
  states in 5440 classes (BEAM_LAW section 4; the map
  [designs/masses/ladder.out](designs/masses/ladder.out) A); with twelve
  Ports 14 slots and `3^14 = 4 782 969` states, with eight Ports 10 slots
  and `3^10 = 59 049`: the table's size is `3^(Ports + 2)`.
- **The fan** is the set of primitive directions within the width P,
  `F_P = {D in Z^3 primitive, |D|_1 <= P}`, the same for every cubic
  lattice (the direction table is the lattice's), weighted by the angular
  measure ([designs/fraction_free/TWO_SLITS.md](designs/fraction_free/TWO_SLITS.md)
  sections 7 and 10); on the register F_6 has 290 directions and the half
  of F_12 91, F_48 1423.

So the honest statement of "how one can choose the groups": one chooses
the lattice (the dimension and the neighbourhood), the phase circle and
the torus; the point group is then forced and is already the largest; the
translation group is the board; and the only freedom that changes the
physics is the neighbourhood, through the front, c and the table above.

## 2. The inputs

Every input of the law, INPUT (chosen or declared) or DERIVED (follows
from the inputs), with its registered value and its source. The three
kinds are Highlights 5.7's (record 189): the grain, the family table with
the width, and the state with the apparatus; K is section 13's constant.

| Symbol | Meaning | Registered value | Kind | Source |
| --- | --- | --- | --- | --- |
| d | the dimension; six Ports | 3 | INPUT | section 1 |
| N | the phase circle Z_N | 64 (1024, 4096 on the Bell worlds at larger N) | INPUT (a grain) | [HIGHLIGHTS.md](HIGHLIGHTS.md) 5.7, record 189 |
| Q | the pace's grain, the scale of a direction's unit label | 64 (`LABEL_SCALE`) | INPUT (a grain) | BEAM_LAW section 3 |
| P | the width of a fan, `F_P` its set | 6 (the 290 fan), 12 (the 91 half fan), 48 (the 1423 half fan) | INPUT (a grain; per declaration, the law fixing the set and the weights) | [designs/fraction_free/TWO_SLITS.md](designs/fraction_free/TWO_SLITS.md) sections 7, 9, 10 |
| G | the fan's weights' grain | 2^18 in the plane; 2^24, 2^14, 2^5, 2^15 on the sphere | INPUT (a grain) | TWO_SLITS.md sections 7 and 10 |
| W | the birth wheel `Z_W` at the golden rate | 4096 (decided, in build; today N at rate 1) | INPUT (a grain) | TWO_SLITS.md section 8; Highlights 5.7 |
| K_clock | the clock's grain, the content per turn (`K` in the world files) | 2^20 (the interferometer and Bell worlds), 2^30 (the slits) | INPUT (a grain) | BEAM_LAW step 5; PREDICTIONS 24 and 25 |
| C, S; C', S'; u_d; T_D | the declared roundings at load (the tables at 1 / 256, the half-angle tables of 2N, the unit labels, the flight's resolution by isqrt) | fixed by N and Q | DERIVED from N and Q (roundings, not choices) | [designs/vector_form/LAW.md](designs/vector_form/LAW.md) section 6 |
| c | the pace of the flight, Links per interval | `1 / sqrt 3` (64 / 110 on a heading) | DERIVED from d = 3 and the L1 walk | [designs/light_speed/FORM.md](designs/light_speed/FORM.md) section 1; section 13.2 (a) |
| M | a family's content per unit (the mass number) | the family table: e 1836 on the Bohr worlds, p 1836, the star 4 198 400, ... | INPUT (free) | [ENTITY_CATALOG.md](ENTITY_CATALOG.md); PREDICTIONS 26 |
| h | the cost of a unit released, `E = h f` | the family's `quantum` (1 for light, 0 for a free family) | INPUT | BEAM_LAW step 5; section 6.4 |
| rho | the charge per unit of content | e -15, beta -7344, p [1, 1], q [0, 1], the masses 0 | INPUT (free) | `examples/events/entities/families.json` |
| sigma | the strong column's value and sign | nuclear 10000, sign -1 | INPUT | the same |
| L | a family's lifetime, the border in intervals | nuclear 3, bond 3, w 1; none for the others | INPUT | the same |
| n / d | a family's phase rate, steps per Link or per interval | light [8591334592, 2^30] on the slits (8 per interval); 0, 8, 16 per Link elsewhere | INPUT | the world files |
| the hand | +-1 on a chiral family | nubar +1 | INPUT | BEAM_LAW note 39; [designs/hand/FORM.md](designs/hand/FORM.md) |
| S | the world's width, the push per unit of content per unit of flow (what physics calls Newton's constant, section 3.3) | 1, 8, 32, 512, 45120, 2^20, 2^28 on the register | INPUT | BEAM_LAW step 5 |
| the extents, the boundary per axis | the torus `Z_X x Z_Y x Z_Z`, periodic or open per axis | per world (60 x 121 x 1 with z periodic on the slits; 301^3 open on the stars; 21 x 1 x 1 on the Bell line) | INPUT | the world files |
| the initial state | the bodies' positions, momenta and held contents, the rows placed, the lamps' rates and directions | per world | INPUT | the world files; the register |
| the apparatus | the detectors' sets, thresholds, phase windows, readings; the splitters' matrices; the gates; the openings' fans | per world | INPUT | BEAM_LAW step 4; the world files |
| H | the growing wall's rate, the expansion (`expansion-v1`, absent by default) | 1 / 400 in the section's map; none on the register | INPUT (declared) | section 15 |
| K | the fixed computation per Node per interval, the operations a Node may do | a bound, not a number of the world files (about 16 per row for the walk, 26 per arriving row for the reading, 12 P per release) | a CONSTRAINT on the form, not an operand | section 13 |

Three facts the table rests on. (i) **The widths are free of K** (section
13.6): P is bounded by K / 12 at a source, N and W by the store, Q and
K_clock by the word, and the register's widths sit at several budgets and
none at a bound, so PREDICTIONS 26 stands: the grain quantises what lives
on a compact group and nothing else. (ii) **The fan's grain does not
dilute under the expansion** (section 15.5): the directions are the
table's and the Bresenham lines the same at every scale factor a; only
the pace along each line falls. (iii) **No input is derived from the
expansion**: H is an input; what the growing wall derives is the
redshift and c in original Nodes per interval, `c a = c_0`, not any
number of the table. And from the present state nothing is derived
either: the masses, the charges and the lifetimes are free (PREDICTIONS
26: a linear law is scale-free in its coefficients), the grain is free
(section 13), and the initial state is the initial state.

## 3. The derived laws

Each with its formula in the notation rule and the section that gives it;
the formula's owner is the section, not this table.

| The law | The formula | Where it is derived |
| --- | --- | --- |
| The pace of the flight | `c = 1 / sqrt 3` Links per interval, the operator norm of the flight: `S_1 Q <= T_D` for every direction D, `T_D = isqrt(3 abs(D)^2 Q^2)`, equality on the cube diagonals | [designs/light_speed/FORM.md](designs/light_speed/FORM.md) section 1; [designs/vector_form/LAW.md](designs/vector_form/LAW.md) section 3; section 13.2 (a) |
| The one map and the six verbs | **s** <- **s** + **r**; e <- [s >= d]; **s** <- **s** - e d on every component of the state vector **s** with its rate vector **r** and wall d; the six verbs (T) (B) (G) (P) (E) (D) | section 0; [designs/vector_form/LAW.md](designs/vector_form/LAW.md) sections 2 and 4 |
| The event-driven form and the flight's closed form | between events **s**(t) = **s**(t_0) + (t - t_0) **r**, bit-identical to the interval stepping; the flight `m(tau) = floor((2 tau S_1 Q + T_D) / (2 T_D))` with tau the age | section 11 (11.1, 11.3) |
| Gauss, Newton and Coulomb | Gauss's law exact on the shell mean; `a = -G M_B / r^2` with `G = K_clock (n / d) / (4 pi S)`; Coulomb `a_e = (q_A q_B / M_A) G / r^2` with the same constant, `q = rho M` | sections 3.1, 3.3, 3.4 |
| Doppler | the receiver's `1 +- v / c` on the axis from the crossing rule, exact over whole Links; the transverse exactly 1; the source's `1 / (1 -+ v / c)` | section 2 (2.2, 2.3, 2.5, 2.7) |
| Born's rule | the click's weight the bilinear form **f**^T **G** **f** with **G** = **E**^T **E** the Gram matrix of the tables, **f** the record's integer vector; the cell by the rungs `b_k = floor((2 N C_k + T) / (2 T))` on the wheel; unique by the lattice Gleason | sections 6.5, 6.7; [designs/amplitude-v1/CLICK_SQUARE.md](designs/amplitude-v1/CLICK_SQUARE.md) |
| The information law | a message is a row, created and ended at one event each; a Node transmits and holds nothing; a body receives and emits at its self-creations; a clock's rate is `1 / (1 + k n / d)`; the balance exact at every tick; the click's cost `log2 N - H` bits per record | sections 6.2, 9 |
| The retarded potential | the age moment of a moving source is the Lienard-Wiechert potential `A(x, t) = q dwell / (4 pi c (1 - n_ret . beta) R_ret)`, beta the speed over c, n_ret the retarded direction, R_ret the retarded distance | section 12 (12.1) |
| The magnetic term's number | the moving reader's count as the magnetic term, the rest density times `(1 - n . beta_reader)` per direction, the field short of Maxwell's by 1 / gamma and along n_ret | section 12b (12b.1, 12b.3) |
| The wait as the reading's cost | the owed count one `by_drive` on the body's record proportional to the rows read, the clock's rate `1 / (1 + k n / d)` | section 13.2 (b); section 9.1 (I4) |
| Entropy and the lattice's Liouville theorem | `S = log2` of the state vectors on the torus consistent with the click list; no production between events (the linear block a bijection), production at the click (`log2 N - H` per record), the cancel and the discarded remainders; `bits read + bits erased = log2 N` per record | section 14 |
| The redshift and Milne | `1 + z = a(t_r) / a(t_e)` from the flight's wall growing at H per interval against the turns' constant rate; `1 + z = exp(H d / c_0)` on the light's path; `c a = c_0`; the Milne case `q = 0` with `z = tau / (T - tau)` for the 24 stars at rest | section 15 (15.3, 15.4) |
| The click without amplitudes | the weight `f^T G f` bit-identical to `X^2 + Y^2`; **E** one factorisation of **G**, not a step of the law | section 6.7 |
| Young's spacing and Bohr's levels | the fringes at `L_1 - L_2 = +- j lambda` from the fan's angular measure; the closure `2 pi p r = j h` under `action` | section 7 |
| E = h f | the click's content `h s` with s the whole turn, the two-valued line of a lamp | section 6.4; PREDICTIONS 24, 25 |
| What is quantised and what is free | the compact groups sampled (phase, direction, charge as a winding), the amounts on the scale free: no number of the law selects a mass | PREDICTIONS 26 |

## 4. What we measure

Nobody sees the state. Every observed value is a detector's reading of
its Node's neighbourhood, and there are three readings only (Highlights
5.7, the conversions; [THREE_WORLDS.md](THREE_WORLDS.md), the things):

1. **The moments** of the arriving rows, one linear reading **R** per
   detector set: order 0 a scalar (the presence, the amount), order 1 a
   vector (the flow, the pointer), order 2 a tensor (the traceless
   second moment), and the age moment (BEAM_LAW step 2; LAW.md 4.3, "the
   readings").
2. **The click**: one bilinear form on the record and one threshold, the
   cell of the wheel value u on the ladder (LAW.md 4.2); its line in the
   run's record is the gather (the Node, the content, the momentum
   brought).
3. **The counts**: a body's turns (its proper time), its owed count (its
   slowing), its clicks and held content, the ledger's lines (released,
   in transit, absorbed, escaped, cancelled), the momentum balance.

The transformation from the GameBoard to our world is Highlights 5.7's
table (a distance is a round-trip flight time or a parallax, never a Link
count; a time is a body's own turn count; a speed what a moving reader
counts; a mass the push a body reads; an energy the phase rate times h; a
probability the Gram weight over the wheel; c a unit conversion). What we
compare with nature, one row each, and its status:

| The quantity | Compared with a formula | Compared with a measurement of nature | Status |
| --- | --- | --- | --- |
| c | yes: `1 / sqrt 3`, the cone of record 144 | c is a unit here and in nature (record 191) | a unit conversion, not a test |
| Doppler, the receiver's and the source's | yes: the crossing rule's counts 45, 58, 19, 38, 183, 311 (record 158); G2's z per star | the receiver's `1 +- v / c` exact, the source's `1 / (1 -+ v / c)`; the transverse 1 against nature's gamma | compared with a formula; different from nature at order `v^2 / c^2` (section 2.7) |
| Newton and Coulomb | yes: series C's nine ring readings; the deuteron's push `310 967 280 640` per interval | the inverse square in the shell mean; one constant for both | compared with a formula; the six-heading shells depart at small r (section 3.5) |
| Born and Bell | yes: `S = 176 / 64` at N = 64, `2896 / 1024`, `11584 / 4096`; the marginals 32 / 64 | `2 sqrt 2` in the limit; the CHSH bound | compared with a formula and with nature's value in the limit |
| Young's fringes | yes: `slits_huygens`, Pearson 0.895 and visibility 0.954 in the weights, every pin reproduced (TWO_SLITS.md section 7) | the Euclidean two-source cosine at the spacing `lambda D / s` | compared with a formula; the clicks wait on the wheel |
| Bohr's radii | yes: r = 8 and 12 closing under the step drive (series H) | the closure `2 pi p r = j h` | compared with a formula |
| E = h f and the lamp's line | yes: the cavity clicks 5 and 6 (PREDICTIONS 24, 25) | nature's line has a width, not two sharp values | compared with nature: a registered limit of the law |
| The masses and charges | no formula selects them (PREDICTIONS 26) | the mass defect absent (issue #369): the deuteron +2.225 MeV, the alpha +28.3 MeV | compared with nature: free, not derived; the same division as nature's |
| A moving clock | the counter's rate 1 at every speed (HYPOTHESES 21); the bond clock 1.383 x rest at 0.43 c (section 10) | nature's gamma 1.107 | different law; the muon of series J4 not yet run (the pins in [designs/light_speed/FORM.md](designs/light_speed/FORM.md) section 4) |
| The redshift and the expansion | the Milne relation on the 24 stars at rest, rms 0.0044 (section 15.4); the register's `q = -0.108` inside the coasting bracket | `1 + z = exp(H d / c_0)`, `q = 0` | compared with a formula; the periodic universe and the rule's entry wait on the owner |
| Entropy | the identity `bits read + bits erased = log2 N` on six registered worlds (section 14) | the second law in the law's terms | compared with a formula; no measurement of nature |
| The lattice's isotropy | the flight Euclidean within 1.35 percent on every direction (record 144; FORM.md section 1) | nature's isotropy | compared with a formula |

## 5. What can be achieved now, and what waits

**Reachable with the law as it stands** (the list of section 3): c; the
one map and the six verbs with the event-driven form; Gauss, Newton and
Coulomb in the shell mean; Doppler (the receiver's under the crossing
rule, the source's today); Born and Bell below Tsirelson at finite N; the
information law and the click's cost; the retarded potential and the
magnetic term's number; the wait as the reading's cost; entropy and the
Liouville theorem; the redshift and the Milne case on paper; Young's
fringes in the weights; Bohr's radii; E = h f; the division of what is
quantised from what is free.

**Waiting on a build** (decided by the owner, Highlights 5.7 "decided and
in build"): the click without amplitudes (item 1b, section 6.7); no tables
and no registers at Nodes; the crossing rule (record 158); form B, the
drive on the momentum's direction ([designs/light_speed/FORM.md](designs/light_speed/FORM.md)
section 3); the exact phase at the click and the golden wheel W = 4096
(TWO_SLITS.md sections 2 and 8): with the wheel, Young's fringes in the
clicks; the fan by angle as a rule of the law with P a width (TWO_SLITS.md
section 9).

**Waiting on a decision of the owner**: Lorentz's routes A, B and C
(record 230: the seventh verb, the root at a declared grain, for gamma on
a body's own counter, [designs/light_speed/FORM.md](designs/light_speed/FORM.md)
section 4; the bond clock of section 10; the aberration of section 12.2);
the periodic universe and `expansion-v1`, the growing wall with H
declared (record 234; section 15); the rewriting of BEAM_LAW from
[designs/vector_form/LAW.md](designs/vector_form/LAW.md).

**Not reachable by the six verbs**: Lorentz's gamma on a body's own
counter and the contraction of a bond by `1 / gamma` (sections 10.4, 12.5,
12b.3: a root of the state, not one of the six); the origin of the masses
and of the charges (PREDICTIONS 26: a linear law selects no scale; a
nonlinear closure on amounts would be a new identity, issue #369); the
origin of the grain (section 13.4: K bounds the widths and fixes none,
the number `1 / sqrt 3` needs isotropy and not K); the transverse Doppler
at order `v^2 / c^2` (section 2.7).
