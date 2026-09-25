# The algebra of the law, in one place: the objects, the ring and the six operations, the click-to-click algebra, the exact identities, what is reached under named hypotheses, what each FAIL row lacks, and how the group was reached (the canonical statement; the Algebra Unifier, 2026-09-23)

The model owner's word of 2026-09-23 ([record 1128](LOG_2026-09-20.md),
the Boss's translation: "It is simply all the algebra; let us unify it
into one place; no need for several files there, if it works out") and
the Boss's judgement that it works out as one document: this file is
the one canonical statement of the algebra of the law, in the order
the paper takes ([record 1099](LOG_2026-09-20.md): the algebra first,
then what follows from it, the way, how the group was reached, the
comparison). Every rule is stated here once; every other file of the
tree that states a rule of the algebra is kept as the record of its
day and carries a header pointing here (the one-source rule of
[AGENTS.md](../AGENTS.md); nothing deleted). The plan of this file,
its source map (which paragraph is taken from which file and section)
and the list of the places where two sources stated one rule
differently are [docs/designs/algebra_one/PLAN.md](designs/algebra_one/PLAN.md);
this file proves nothing anew: each statement carries the link to its
proof in its owning file, and no formula is stated that a source does
not state. Chapter 8, added on the owner's word of 20:24Z (record
1489), carries the massive record kind from its design pages into this
file and is the one chapter that writes proofs of its own, each marked
PROVED HERE, beside the design's proofs (CARRIED) and computations
(COMPUTED, NOT PROVED).

**The rules this file obeys.** Every symbol is named in English at its
first use; a scalar plain, a vector bold lowercase (**p**), a matrix or
an operator bold uppercase (**F**). Every number carries its kind:
DETECTOR (a click or a count of clicks at a declared detector, the
only kind compared with nature or pinned), GAMEBOARD (the host's view
of the board, a diagnostic, compared with nothing), COMPUTATION (the
algebra's closed form, no run), HOST (a cost or a time of the machine),
CONVERSION (an Outside number made from counts by a named reading).
Every result is stated as matching nature, never as how nature is;
Newton's, Einstein's, Lorentz's, Bohr's and Balmer's forms appear only
as the thing compared with. The group is called the group of order 24
everywhere (the rotation group of the cube, isomorphic to S_4, the
symmetric group on four things; never "S24"; the owner's word of
[record 1114](LOG_2026-09-20.md), Highlights 5.4). Where two sources
worded one rule differently, the wording in force is stated with the
record or the code that decides it, and the superseded wording is
named once with its source, so that the reader finds both.

**The symbols, named once.** N the phase circle's grain (the paper's
N_phi; 64 on the register, 1024 and 4096 on the Bell worlds); Z_N the
integers modulo N, the phase circle; Z[Z_N] its integer group ring; f a
record's rows at a Node as one element of Z[Z_N], f = sum over p of f_p
x^p with x one phase step and f_p the amount at the phase p; zeta_N the
primitive N-th root of unity, exp(2 pi i / N); Z[zeta_N] the cyclotomic
integers; ev the evaluation Z[Z_N] -> Z[zeta_N]; C and S the tables of
the cosine and the sine at the scale 256, **E** the 2 x N integer matrix
whose rows they are, **G** = **E**^T **E** the click's Gram matrix; **F**
the interval's map on the state vector **s** with its rate vector **r**
and wall d per component; Q the label's scale (the paper's N_l, 64);
S_w the push's width (the paper's N_w, the world key `width`); M a
body's content in units of its family's quantum; T_D the flight period
of a direction D and S_1 = abs(D)_1 its Manhattan length; c the pace of
a light row, 1 / sqrt 3 Links per interval in the limit of every
direction, 32 / 55 on a heading; v a pace in Links per interval; k the
whole number of intervals per hop of a moving record, v = 1 / k; r a
detector's own count per interval against the tick, the click theorem's
one free number; k_AB and k_BA the two one-way count ratios of the
click theorem; gamma the Lorentz factor 1 / sqrt(1 - v^2 / c^2), as the
thing compared with; h the action per Link of a row's phase turn (the
world key `action`); n / d the suspension pair (the world key
`suspension`); a_tau the age moment a wall reads; k_crowd = a_tau n / d
the crowd's stretch of a count (the FAIL rows file writes it k; here k
is the hop's whole number, so the crowd's stretch carries its
subscript); gamma_PPN the world key `optical`'s declared strength;
c_f = 1 + gamma_PPN the flight's coefficient in the age wall's set; u
the birth wheel's value written on a record; (A1), (A2), (A3) the
hypotheses of chapter 5, defined at its head. Two letters are reused
and named at each use: lambda (the boost's dilation in 5.1, the radar's
scale in 5.2, the wavelength in 5.7) and K (the kernel K(Delta) of
Theorem 4 in 4.8, the hypothesis (K) of chapter 5, the number of
directions of the fan in 5.6 and 5.7); omega and kappa are the walk's
angles in chapter 5 and, once, a root of unity (4.11) and a force
constant (5.8), named there; and three letters carry a second meaning
beside their first, named there too: a, plain, the acceleration (5.4)
beside **a** the flow vector; K the kinetic reading in E_j = K + q A
(5.8); s the lamp's turn (5.7) beside s the state's component. Chapter 8
names its own symbols at its head (the two levels of a row, the pair
[num, den], the pitch omega_0, the coupling pairs g and G, the block's
Nodes R and the rest), each apart from the head's where a letter is
reused.

---

## 1. The objects: the four group objects, their definitions in symbols, the dictionary, and how the group was reached (the chief physicist's page, carried over)

This chapter is the chief physicist's page
[docs/GROUP_STRUCTURE.md](GROUP_STRUCTURE.md) (merged to main at
`7739bbbe`, PR #968), its sections 1 to 6 carried over verbatim below
with his name and its date (2026-09-23); his sections 7 to 11 (the
collision as a group action, the operations between the objects, how
the 48 act as one table, where each definition lives, every naming of
24 and 48 in the tree) stay in his file as the index and the record
this chapter links to. Nothing here is a second definition.

**The owner's road, first** ([record 1136](LOG_2026-09-20.md), the
page's section 3 in one sentence): the operations came first, as acts
on the board (a row flies one Link per interval, rows meet at a Node, a
body steps by an accumulator against a wall, a phase turns, identical
rows merge, a detector clicks); the 48 are everything that preserves a
Node of six Ports and its cone of one Link per interval; requiring
every rule to commute with them chooses the admissible forms; and the
group of order 24 is the part under which the hand is kept as well.

*(Carried over verbatim from `docs/GROUP_STRUCTURE.md` sections 1 to 6, the chief
physicist, 2026-09-23; the section numbers inside the text, "section 8" and
the like, are that page's own and point into it; the vectors written
bold uppercase in its dictionary's force row, **V** and **W**, are that
page's and stay as the chief physicist's to fix.)*

### 1.1 The definitions, in symbols

The model owner's second word (2026-09-23): the mathematics itself, not
an index; what the group is, what its operations are, what the cube is,
in the definition of the system. Every symbol named at its first use.

- **The object ("the cube").** P = {+X, -X, +Y, -Y, +Z, -Z}, the six
  Ports of a Node, with the involution e -> -e (the opposite Port); the
  lattice Z^3 with the L1 neighbourhood, six neighbours per Node. The six
  Ports are the face centres of a cube (the vertices of an octahedron);
  no solid is meant. This is the one choice of the model.
- **The symmetry group of the cube.** G_48 = { g : P -> P, a bijection
  with g(-e) = -g(e) for every Port e }, the operation the composition
  ("g then h", `compose_symmetries`), the identity the map that fixes
  every Port, the inverse the map that undoes g. Equivalently the signed
  permutation matrices: the 3 x 3 integer matrices **M**_g with one entry
  +1 or -1 in every row and column and 0 elsewhere, under matrix
  multiplication; G_48 = {+1, -1}^3 semidirect S_3 (S_3 the symmetric
  group on the three axes), the hyperoctahedral group B_3, the full
  octahedral group O_h; the order 3! x 2^3 = 48. The determinant det:
  G_48 -> {+1, -1}, det(gh) = det(g) det(h), is a homomorphism
  (`symmetry_hand`: the sign of the axis permutation times the product of
  the axis signs).
- **The group of order 24.** G_24 = ker det = { g : det(g) = +1 }, a
  subgroup of index 2, the rotations. It acts faithfully on the cube's
  four body diagonals, so G_24 is isomorphic to S_4, the symmetric group
  on four things (the paper's Theorem 1). The other coset, det(g) = -1,
  is the 24 reflections; a pseudoscalar h transforms as h -> det(g) h and
  tells the cosets apart. The order 24 is |G_24|; the group is S_4, never
  S_24.
- **The action of G_48 on the state.** On a vector **v** in Z^3 by
  g . **v** = **M**_g **v**; on the direction table D (a finite set of
  primitive integer vectors closed under the 48, a G_48-set); on the
  labels exactly, **u**_{gD} = g **u**_D; on the Nodes about a centre by
  the same matrix; trivially on every scalar (a content, an amount, a
  count, an age); not at all on a phase (a phase is not a direction). The
  law's claim, tested and not counted: every operation V of the law
  commutes with every g, V(g . s) = g . V(s) on the state s, up to the two
  declared ties (the digital line's axis order, the collision's Port
  order).
- **The phase circle and its group ring.** Z_N = Z / N Z, the integers
  modulo N under addition, N per world. Z[Z_N] = { sum over p of a_p [p]
  : a_p in Z }, the integer group ring: addition by components, the
  product [p] [q] = [p + q]. A record's rows at a Node are one element of
  Z[Z_N]; the merge is the addition; the cancel [p + N/2] = -[p] is the
  passage to the quotient ring Z[Z_N] / (x^(N/2) + 1) = Z[zeta_N], the
  cyclotomic integers, zeta_N a primitive N-th root of unity; the click is
  the evaluation ev([p]) = (C[p], S[p]), the tables' integer vector near
  256 zeta_N^p, and the click's weight the norm |z|^2.
- **The translation group.** Z_X x Z_Y x Z_Z, acting on the Nodes by
  addition modulo the extent on a periodic axis and up to the face on an
  open axis (the face a detector).
- **The collision.** A cyclic group Z_m acting on the finite set S of the
  3^8 slot states of a Node by the shift sigma (`CollisionTable.act`); the
  orbits of the action are the classes; the invariants (the crowd mask,
  the number of singles, their headings' sum) are constant on an orbit;
  the period of a state is the size of its orbit.
- **The state and the operator.** A Node's state: its rows (per family
  and direction an element of Z[Z_N] with an amount and a content) and its
  bodies (the content per family in Z^F, F the number of families, the
  momentum **p** in Z^3, the phase in Z_N, the age in Z, the counts as a
  point of Z^n / d Z^n). The law is one operator per interval at every
  Node, composed of the six operations of section 8 alone: (T) the
  translation, (B) the bilinear form, (G) the group-ring addition, (P) a
  permutation of the joint state, (E) the evaluation, (D) the division
  with the remainder kept and the comparison. G_48 acts on the whole
  state space through the directions and the Nodes and commutes with each
  of the six.

### 1.2 From the algebra to the physics: the dictionary

The model owner's third word (2026-09-23): how the algebra enters the
physics, where momentum, mass and the rest come from; what is the
definition of the mathematics and what is the definition of the physics.
The mathematics is section 1: the state space, the six operations and
the groups. The physics is two things and no third: the names given to
the elements of that structure (this table, one line each, the full
statement in the owner document) and the reading rule (section 8). Every
number of nature is reached from the structure under these names or is a
declared input ([FULL_PICTURE.md](FULL_PICTURE.md) section 1;
[HIGHLIGHTS.md](HIGHLIGHTS.md) 5.7, the conversions and the inputs).

| Physical name | The algebraic element it names | Owner document |
| --- | --- | --- |
| mass | a body's content M, in units of its family's `quantum`; the smallest mass one unit, fixed by the grain and not free; a released row has mass only under massive-rows-v1 (the content M per row) | [DERIVATIONS_BEAM.md](DERIVATIONS_BEAM.md) section 13; [PREDICTIONS.md](PREDICTIONS.md) entry 26; [designs/massive_rows/DESIGN.md](designs/massive_rows/DESIGN.md) |
| gravity | the first column of every family, the value [1, 1] per unit of content and the sign minus (like contents pull together); Newton's constant G a reached number of the flux q, the dwell and the width S, not a key | [BEAM_LAW.md](BEAM_LAW.md) section 3 step 4 (the columns); [DERIVATIONS_BEAM.md](DERIVATIONS_BEAM.md) section 3 |
| charge | the second column, the family's `charge` rho per unit of content, the sign plus | [BEAM_LAW note 36](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation) |
| momentum of a row | its label, the integer vector **p**_D = the unit vector of its direction D at the scale p (Q = 64 for light, `momentum_magnitude` for a massive family), `unit_label` | [BEAM_LAW.md](BEAM_LAW.md) section 2, note 23 |
| momentum of a body | **p** in Z^3, label units, moved by the push and read by the drive | [BEAM_LAW.md](BEAM_LAW.md) section 3 steps 4 and 5 |
| force, the push | the bilinear form (B): **r** = **C** **a**, the coupling matrix over the columns times the flow vector of the arriving rows; on a free row **W** -= n (1 + gamma) content e_D **V** (the generic entry) | [DERIVATIONS_BEAM.md](DERIVATIONS_BEAM.md) section 1 (B); [ENGINE.md](ENGINE.md) the `optical` paragraph |
| velocity, the step | the drive: the pace v = p / (Q S M + p) Nodes per self-creation per axis, a division with the remainder kept (T) | [BEAM_LAW note 17](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation); [designs/moving_detector/DESIGN.md](designs/moving_detector/DESIGN.md) section 1 |
| energy | E'_0 = Q S M the rest energy in the identity's units; E' = isqrt(E'_0^2 + 3 **p** . **p**); a massive row's pace \|**p**\| / E'; the 3 the flight's constant, not a key | [designs/massive_rows/DESIGN.md](designs/massive_rows/DESIGN.md); [DERIVATIONS_BEAM.md](DERIVATIONS_BEAM.md) section 23 |
| time, a clock | a body's count of self-creations; the count it owes to the crowd (the age moment, the age word) the potential M / r; the tick a GameBoard count, read by nothing compared with nature | [ENGINE.md](ENGINE.md) "the owed count"; [EXPERIMENTS.md, T](EXPERIMENTS.md#t-the-clocks-word-2026-09-21); [designs/clock_age/NOTE.md](designs/clock_age/NOTE.md) |
| the speed of light c | the flight table's pace: 32 / 55 Links per interval on a heading, 1 / sqrt 3 Euclidean along the walked line, the operator's norm; the postulate P9 | [BEAM_LAW.md](BEAM_LAW.md) section 3 step 1; [DERIVATIONS_BEAM.md](DERIVATIONS_BEAM.md) section 27 |
| space, distance | Nodes and Links; a distance a count of Links, a radius from a click by the flight table (a CONVERSION) | [TERMINOLOGY.md](TERMINOLOGY.md) |
| light and matter | rows of a paid family (quantum at least 1, the content per row quantum x turn) and a free family's rows with bodies (quantum 0); "rows and bodies, not light and matter" | [BEAM_LAW.md](BEAM_LAW.md) section 2 (`families`); [FULL_PICTURE.md](FULL_PICTURE.md) |
| phase, interference, probability | a row's phase in Z_N; a record's element of Z[Z_N]; interference the merge with the cancel; the probability weight of a click the norm \|z\|^2 of the evaluation (E), the amplitude law | [BEAM_LAW note 37](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation); [DERIVATIONS_BEAM.md](DERIVATIONS_BEAM.md) section 1 (G), (E) |
| spin, polarisation | the hand h in {-1, 0, +1}, a pseudoscalar under the 48 (h -> det(g) h); a body's axis an axial vector | [designs/hand/FORM.md](designs/hand/FORM.md); BEAM_LAW note 39 |
| isotropy, the symmetry of the law | the 48: every operation commutes with G_48 (section 1); the law's constants are invariants of O_h (k^2 the one quadratic invariant; two quartic ones, the anisotropy at order k^4) | [DERIVATIONS.md](DERIVATIONS.md); [designs/fraction_free/FORM.md](designs/fraction_free/FORM.md) |
| Lorentz, Einstein, Newton | not in the group: no boost is among the 48; their forms are reached Outside as relations among counts between clicks (the one-way factors, the round trip, the radar; the ring mean of the push), the algebra first and the comparison after | [designs/click_frame/DERIVATION.md](designs/click_frame/DERIVATION.md); [designs/ring_mean/PROOF.md](designs/ring_mean/PROOF.md); [HIGHLIGHTS.md](HIGHLIGHTS.md) 5.4 |
| a measurement | a click at a detector; a count between clicks on the detector's own record; a ratio of such counts (the reading rule, section 8); a reading of the board a diagnostic | [ENGINE.md](ENGINE.md), the readings by type; record 281 |

### 1.3 How the group was reached from the operations

The model owner's fourth word (2026-09-23): we came from the physics to
the algebra, when we saw which operations the GameBoard has to perform;
so what links the physical operations to the group? The order of events
is recorded in
[designs/algebra_transition/HISTORY.md](designs/algebra_transition/HISTORY.md)
section 18 (the vector program, records 180, 183, 186, 191 and 231 of
the log); the link is one requirement, that every rule commute with
every symmetry of the neighbourhood it reads.

1. **The operations came first**, as acts on the board: a row flies one
   Link per interval along its direction (locality and straightness),
   rows meet at a Node (the collision), a body steps by an accumulator
   against a wall, a phase turns, identical rows merge, a detector
   clicks. On 2026-09-21 the owner said "proceed with everything
   represented in vectors and matrices, from group theory" (record 191),
   and each rule was written as one of the six operations of section 8 on
   a state vector.
2. **The group is the answer to "which maps preserve what the operations
   act on".** They act on a Node with six Ports and its Links, and on a
   causal cone of one Link per interval. The bijections of the six Ports
   that keep opposite Ports opposite are the signed permutations of the
   axes, 48 of them; and over the integers the only bijections that
   preserve the cone are these 48 (the click frame,
   [designs/click_frame/DERIVATION.md](designs/click_frame/DERIVATION.md),
   the proof sketch (a)): a boost is not Z-linear, so no boost is among
   them, and Lorentz's form is reached Outside from the clicks, not as a
   symmetry of the lattice.
3. **Where the 48 first appeared in the code, before they were named a
   group: the collision.** The collision table is generated from its rule
   over the classes of slot states, and the test enumerated the 48 maps
   that leave the table as it is; the group was found as the invariance
   of one physical operation and then recognised as the symmetry of all
   of them (BEAM_LAW note 42: "the same 48 maps the collision test
   enumerated"; `tests/test_nature_beam_collision.py` (b)).
4. **The 24 came from the hand.** Carrying spin and polarisation
   (hand-v1, record 128) needed a pseudoscalar, a quantity a reflection
   flips and a rotation keeps; that is det(g), and it splits the 48 into
   the 24 rotations that keep the hand and the 24 reflections that flip
   it. The owner's word on the name (record 231): the 24 are the
   octahedron's 24 rotations, not his numeral.
5. **The other objects the same way.** The step and the flight are
   shifts, hence the translation group of the torus; the turn adds
   modulo N, hence Z_N, and the merge of records is addition in Z[Z_N];
   the collision is a permutation of a finite set generated by a shift,
   hence a cyclic action. And c was not chosen: it is the norm of the
   flight operator, 1 / sqrt 3, from locality and straightness (record
   186).
6. **What the group does back to the physics: it forces forms.** A rule
   that reads only the local state must commute with the 48, and that
   constraint selects the admissible forms. The proven instance
   ([designs/open_problems/lorentz/NOTE.md](designs/open_problems/lorentz/NOTE.md)
   section 4, Theorem 3): an isotropic even reading of a body's momentum
   within the six operations is a bilinear form **p**^T **M** **p** with
   **M** commuting with all 48; the symmetric integer matrices fixed by
   the 48 are the multiples of the identity, so the only such reading is
   c **p** . **p**: the 48 force the form's isotropy, while the 3 and
   E_0'^2 of the square E_0'^2 + 3 **p** . **p** are the band's (4.2 and
   8.1), not the 48's. "Generic"
   in the three tests of every rule (generic, vector, local) means
   exactly this: commuting with the 48, made of the six operations,
   reading the neighbourhood alone.

In one sentence: the operations did not deduce a group; they were
defined on a Node of six Ports, the 48 are everything that preserves that
Node and its cone, and once every rule is required to commute with them
they choose the admissible forms, the group of order 24 being the part
under which the hand is kept as well.

### 1.4 The names, fixed by the owner

The names are the model owner's (2026-09-23,
[record 1114](LOG_2026-09-20.md#1114-the-owner-the-algebraist-should-also-understand-why-the-passed-experiments-passed-and-everywhere-the-group-is-called-the-group-of-order-24-the-definition-too-2026-09-23-0915z-recorded-by-the-boss-at-0915z-the-owner-001xz-in-hebrew-the-bosss-translation-what-will-also-help-the-algebraist-is-to-understand-why-the-experiments-that-passed-passed-and-the-ones-that-failed-failed-and-what-was-missing-in-them-according-to-what-is-derived-from-the-algebra-to-physics-he-understands-it-since-he-derived-the-algebra-and-reached-the-physics-be-strict-about-it-in-item-5-the-opening-everywhere-we-call-it-the-group-of-the-24-that-is-the-correct-thing-to-say-algebraically-so-it-is-needed-in-the-definition-as-well-say-that-it-is-correct-to-say-the-group-of-the-24-the-bosss-answer-yes-the-group-of-order-24-the-rotation-group-of-the-cube-isomorphic-to-s4-theorem-1-is-the-correct-algebraic-name-and-the-models-name-the-48-signed-permutations-of-the-axes-are-the-objects-symmetries-whose-rotations-that-group-is-named-once-where-the-hand-tells-the-cosets-read-acs-line-the-paper-says-the-group-of-order-24-uniformly-in-the-abstract-the-opening-theorem-1s-statement-and-definition-the-families-section-and-the-discussion-the-other-names-in-apposition-once-each-where-the-isomorphism-is-stated-the-writer-ordered-so-with-the-central-ideas-sentence-or-one-more-commit-on-paper-opening-every-occurrence-listed-in-planmd-the-fail-rows-algebraist-ordered-one-more-table-every-pass-measured-partly-and-replicated-row-of-table-2-one-line-each-why-it-passed-by-the-algebra-which-click-counts-or-count-ratios-which-declared-integers-which-theorem-or-identity-of-the-ring-whether-anything-measured-inside-the-board-so-each-fails-lack-is-seen-against-the-passes-chain-with-one-thing-missing-named-the-naming-decision-to-highlights-54-as-one-line),
[Highlights 5.4](HIGHLIGHTS.md)):

- **The symmetry group of the cube**: the 48 signed permutations of the
  three axes (an axis permutation and a sign per axis, 3! x 2^3 = 48), the
  full octahedral group O_h, each element written as its image of the six
  Ports [+X, -X, +Y, -Y, +Z, -Z] and sending opposite Ports to opposite
  Ports. In the code `core.game_board.cube_symmetries`, with the
  composition `compose_symmetries`, the identity `IDENTITY_SYMMETRY` and
  the inverse `inverse_symmetry`; its pseudoscalar `symmetry_hand`, the
  sign of the axis permutation times the product of the axis signs (the
  determinant of the signed permutation matrix), +1 on 24 elements and -1
  on 24.
- **The group of order 24**: the kernel of that determinant, the
  index-2 subgroup of rotations, called everywhere "the group of order
  24" (the rotation group of the cube, isomorphic to the symmetric group
  S_4 on the cube's four body diagonals; the paper's Theorem 1, "the 24 of
  the name", `paper/general_formula/main.tex`). The other coset, the 24
  reflections, is told from it by the hand, an axial vector or any
  pseudoscalar.
- **"S24" is not a name of anything here.** The 24 is the order of the
  group; the symmetric group it is isomorphic to is S_4, of order 24, not
  S_24 (which has order 24!). No file of the repository uses "S24" or
  "S_24" (section 11).
- **The 48 are not chosen.** The one choice is the six Ports of a Node
  (the L1 neighbourhood of the cubic lattice); every map that preserves
  the six Ports as a set and the lattice's Links is one of the 48 and every
  one of the 48 does ([FULL_PICTURE.md](FULL_PICTURE.md) section 1, "What
  is not chosen: the group of 48"; the crystallographic restriction: no
  three-dimensional lattice has a larger point group).

### 1.5 The phase circle and its group ring

- **The phase circle Z_N**: the integers modulo N, the cyclic group of the
  phase, N chosen per world (64 on the register; 1024 and 4096 on the Bell
  worlds). A turn adds, a difference subtracts, the opposite phase is half
  a turn away; with it the unit vectors (C[phase], S[phase]) at the scale
  256, a declared rounding. In the code `core.phase.PhaseCircle` (`turn`,
  `difference`, `opposite`, `vector`); named in
  [BEAM_LAW note 42](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
  the properties in `tests/test_group_structure.py`
  (`test_the_phase_circle_is_the_cyclic_group_with_unit_vectors`).
- **The group ring Z[Z_N]**: the integer group ring of the phase circle;
  a record's rows at a Node are an element of it, one integer weight per
  phase. **The merge** is its addition, with the cancel [p + N/2] = -[p] on
  a record's rows (an antiphase row subtracts), the normal form
  `NatureBeamStore.merge`; the owning statement is
  [DERIVATIONS_BEAM.md](DERIVATIONS_BEAM.md) section 1, operation (G), and
  [BEAM_LAW note 37](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation).

### 1.6 The translation group of the torus

Z_X x Z_Y x Z_Z per world: the GameBoard's extents per axis, each factor
a circle (a periodic axis) or a segment (an open axis whose faces are
the border, a click at the face detector). Chosen per world by `shape`
and `boundary` ([FULL_PICTURE.md](FULL_PICTURE.md) section 1, choice 3;
[ENGINE.md](ENGINE.md), the world file). The translation (T) of
DERIVATIONS_BEAM's list is the action of this group on Nodes, and on the
counts the same division with the remainder kept.

### 1.7 The record of the rule as a pair of levels: how Z_N acts on it, the three pairs, and where a foreign object and a detector sit (the chief physicist, 2026-09-24, on the model owner's word of 00:40Z; not carried over, this file's own)

The four group objects of 1.1 do not change under the rule of chapter
8 (the massive record kind) and of the massless kind under
[designs/detector_law/DESIGN.md](designs/detector_law/DESIGN.md)
section 2; what changes is how a record carries the phase, and this
subsection states it once so that the groups' account is one account.

- **The record of the rule is two samples of the real part of one
  character.** Under the
  rule a record at a Node is not rows with phase labels but two
  integers, its level now and one interval ago, (a_before, a_now), at
  the amplitude unit declared at load (chapter 8's symbols). With the
  kind's clock k whole steps of Z_N per interval (the first difference
  of a floor, `core.integer.by_clock`; k such that the sine table's
  S[k] is large, DECLARATIONS.md section 14) and theta = 2 pi / N one
  step, the pair is (a_before, a_now) = A (cos(phi - k theta), cos phi):
  two samples of the real part of one character of Z_N x (the time
  translation), the plane waves of 8.1, which fix the character (A and
  phi) wherever S[k] is not 0 (Reviewer 3's token). The phase phi and the
  amplitude A are both in the pair and neither is a label; nothing else
  is kept at the Node (the record's remainder r aside, kept on the record
  by verb (D), 8.2).
- **Z_N acts on the pair by the linear form (PROVED HERE).** For every
  t in Z_N, with kappa = k theta and tau = t theta,

      sin(kappa) cos(phi + tau) = cos(phi) sin(kappa + tau) - cos(phi - kappa) sin(tau).

  Proof: sin(kappa + tau) = sin kappa cos tau + cos kappa sin tau and
  cos(phi - kappa) = cos phi cos kappa + sin phi sin kappa; the right
  side is cos phi sin kappa cos tau + cos phi cos kappa sin tau - cos
  phi cos kappa sin tau - sin phi sin kappa sin tau = sin kappa (cos phi
  cos tau - sin phi sin tau) = sin kappa cos(phi + tau). So the record
  turned by t is A cos(phi + tau) = (a_now sin(kappa + tau) - a_before
  sin tau) / sin kappa, a linear map of the pair. With the sine table
  S[j] = round(256 sin(j theta)) (the declared rounding of the circle,
  an input of kind 1, the grain of the computation, Highlights item 5;
  1.5) a table's drive is (a_now S[k + t] - a_before
  S[t]) / S[k]: verb (B), the bilinear form with the declared matrix on
  the record's two columns, then one division with the remainder kept
  (D); no nearest entry, no phase label, no register (DECLARATIONS.md
  section 14, the linear form; the nearest angle of the head of that
  file is a GAMEBOARD diagnostic). In the group's words: the shift by
  [t] of the group ring Z[Z_N] (1.5), which the beam law applies to a
  record's whole weight vector f, is here applied to the two samples of
  one character; the same group, the same characters, a representation
  of dimension 2 in place of the regular one. The merge (G) is the
  rule's own addition (the levels and the reads' sum S_6 add linearly,
  the cancel a sign); the click is 8.6's rung on the pointer against
  the norm in place of the evaluation ev, both one bilinear form and
  then one comparison (D).
- **The three pairs, named once and never confused.** (1) A kind's pair
  [num, den] (8.1): the clock of a record kind, cos omega_0 = num /
  den, declared world data of kind 2, the table of families (Highlights
  item 5; light [1, 1], the matter kind
  [800, 809]). (2) A record's pair (a_before, a_now): the two levels of
  one record at one Node, its state, the phase and the amplitude
  together (this subsection). (3) The pair of records (3.6): one record
  with two arms, of tensor rank 2, the Bell rows. The first is a
  declaration of kind 2, the second a state, the third one record.
- **Where a foreign object and a detector sit.** A foreign object (a
  table, a mirror, a block; 8.3) is no element of any of the four
  groups and no new group object: it is a finite set R of Nodes, a
  G_48-set (the 48 turn it, the translations of 1.6 move it), declared
  world data like a wall's placement (kind 3, the state and the
  apparatus, Highlights item 5), carrying a kind's pair (a well,
  8.3) or a table; a table is a map from Z_N (its setting t) to the
  linear form above, acting on the records' pairs at its Nodes; the
  object's own record, where it has one (a block), is again a pair of
  levels per Node whose phase runs on Z_N like every record's. A
  detector set is a subset of Nodes with a declared wheel W (kind 3), one
  set per Node where a screen is read per Node; its click (8.6) is the one
  output of the board, in the Outside; every other number of the board
  is a GAMEBOARD diagnostic (3.2; record 281). In one sentence: the
  groups act, the objects are sets of Nodes on which they act, and the
  only thing that leaves the board is a click.
- **The course from the one choice to a click, one line.** The six
  Ports force the 48 and the group of order 24 within them (1.3, 7);
  the two chosen groups, Z_N and the torus's translations, carry the
  phase and the place; a record is two samples of the real part of one
  of their
  characters; a foreign object is a set of Nodes with a pair, its table
  acting through Z_N on the records' pairs; a detector set clicks by
  the rung; the click is the only measurement (3.2).

---

## 2. The ring and the six operations as maps, in symbols

**The one central formula.** The law is one map **F** (the interval's
map) applied at every Node of the GameBoard at every interval, per
component s of the state vector **s**, each with its own rate r and wall
d (the paper's equation (map); [DERIVATIONS_BEAM.md](DERIVATIONS_BEAM.md)
section 0, Eq. (1); the code `core.integer.by_drive`):

    +-----------------------------------------------------------------------------------+
    |   s <- s + r;      e <- sign(s) x min(floor(abs(s) / d), a);      s <- s - e d      |
    +-----------------------------------------------------------------------------------+

Each component of the state is a bounded integer accumulator with a
declared rate and a declared wall: it is translated by its rate,
counted in walls (capped at a = 1 for the drive; uncapped elsewhere,
a with no bound and e the whole part floor(abs(s) / d) with the sign,
which the primitive encodes as `at_most = 0`), and reduced by
the walls it holds; every wall counted is an event (a Link crossed, a
phase step taken, a count completed, a birth, a push) and nothing else
happens. The one declared variant of the count is `centred`
(centred-step-v1, the world key `centred_step`, which chapter 6's row 6
cites): the count is the nearest whole number the accumulator holds,
(abs(s) + d // 2) // d with the sign, the accumulator then in
[-(d - d // 2), d // 2). The rates and
walls are made of six integer operations and nothing else, the six
verbs of [Highlights](HIGHLIGHTS.md) section 1 item 3 (record 181) and
5.7 "The six operations", and 5.4's row of record 181: (T) the
translation, (B) the bilinear form with a declared matrix, (G) the
group-ring addition, (P) the permutation, (E) the evaluation, (D) the
division with the remainder kept and the comparison. The letters are
DERIVATIONS_BEAM's and the paper's (the Boss's word of 2026-09-23 on
the plan's K14); [COUPLINGS.md](designs/couplings_algebra/COUPLINGS.md)
writes the group-ring addition as A, the same operation. A matrix is
written bold uppercase (**G** the Gram matrix, **E** the tables'
matrix); a verb's tag is plain in parentheses; the same letter never
means both in one sentence. Where the rate is a constant of the world
(the linear block: the flight, the phase, the age, the merge, the
split, the rotation, the evaluation) every component has the closed
form s(t) = floor(s_0 + r t), r the rate as a fraction of the wall, so a
row's state at any time is a formula of its birth and its age; where
the rate is a function of what arrives (the feedback block: the push,
the owed count, the turn, the release, the drive) the map is iterated
and its continuum limit is the differential equation ds / dt = r(s)
(DERIVATIONS_BEAM section 0, "The two blocks"). The read-out is one
comparison, the click (chapter 3).

### 2.1 (T) The translation of an accumulator by its rate

x -> x + r on Z^k or on a torus; every count of the law is this: the
flight on the digital line, the phase's turn, the age, the drive, the
owed count, the release, the lamp's wheel, the push per column. On a
row the flight's accumulator gains 2 S_1 Q per interval against the
wall 2 T_D, started at T_D (the half-wall start), so the Links a row has
crossed by the age tau are

    m_D(tau) = floor((2 tau S_1 Q + T_D) / (2 T_D)),   the k-th Link at tau_k = ceil((2 k - 1) T_D / (2 S_1 Q)),

the flight table's closed form (DERIVATIONS_BEAM section 11.1; the
pace c = Q abs(D)_2 / T_D, chapter 4.2). On a body the drive per axis
gains p_a, the momentum's component with its sign, against the wall
Q S_w M + abs(p_a), capped at one Link per interval (a = 1). On the phase, a row
turns phi(tau) = floor((tau + 1) n / d) - floor(tau n / d) steps per
interval of age, the pair [n, d] its family's declaration, read modulo
N; under massive-rows-v1 a massive row turns abs(p_a) N / h steps at
every axis Link over the world's action h (`world.py`, the identity's
paragraph). The translation group of the torus (chapter 1.6) is this
verb on Nodes. Source: DERIVATIONS_BEAM section 1 (T), lines 265-273;
section 0.

### 2.2 (B) The bilinear form with a declared matrix

A moment sum over the rows of w x **u**^(x) k of the neighbourhood's
rows (k = 0, 1, 2 and the age: the presence, the flow vector, the
traceless second-moment tensor, the age moment; the one reading a
detector makes), and the coupling **r** = **C** **a** (**C** the coupling
matrix, the reader's charges per column with their declared signs;
**a** the label flow vector of the arriving rows): a signed inner
product over declared columns times the moment (`core.integer.signed_inner`,
"a vector, a declared diagonal matrix of +1 and -1, a vector"). The
push on a body is this form: the rate of its momentum is bilinear in
the state, the reader's content times the flow. The click's weight is
this form on the record's element (2.5): f^T **G** f with **G** =
**E**^T **E**, nothing squared as a step of its own. Source:
DERIVATIONS_BEAM section 1 (B), lines 274-277; section 6.7.

### 2.3 (G) The group-ring addition: the merge and the cancel

A record's rows at one Node and label are one element f of Z[Z_N]; the
merge of identical rows is the ring's addition, f <- f + g, with the
cancel [p + N/2] = -[p] on a record's rows (an antiphase row subtracts;
an equal antipodal pair leaves nothing). The cancel identifies x^(N/2)
with -1, so the rows after the cancel are an element of
Z[x] / (x^(N/2) + 1); for N a power of two (64, 1024, 4096, every
registered N) x^(N/2) + 1 is the cyclotomic polynomial of N and this
quotient is the ring of cyclotomic integers Z[zeta_N] itself, a free
Z-module of rank N / 2 on the basis 1, x, ..., x^(N/2 - 1): the
GameBoard's cancel and the click's zero are one relation, exactly (for
an N with an odd factor they are not). Two arms' elements multiply by
the ring's convolution (the pair's product, Bell and GHZ), the label
sum is the ring's addition. Source: DERIVATIONS_BEAM section 1 (G),
lines 278-279; section 1.2, the merge's row; section 6.5, lines
1575-1583; section 6.7 (2); chapter 1.5 above.

### 2.4 (P) The permutation of the joint state

The collision: per (Node, number, content) class the single units in
the eight slots are permuted, the forward map the cyclic shift on the
sorted 8-tuples, fixed on the class invariants (the amount and the
labels' sum conserved), the orbits the collision classes (chapter 1;
the group page's section 7); its tie, the sorted order being Port
order, is the one undeclared breaking of the 48. The meeting's turn (an
arc permutation of the direction table, built by comparisons); the gate
(CNOT: the joint labels permuted from the control's bit); the
apportioning's tie (the units left to the largest remainders, ties from
`age mod n`, the tie's start a rotation). A permutation of directions,
labels or Nodes, never of contents. Source: DERIVATIONS_BEAM section 1
(P), lines 280-281; section 1.2, the rows of the collision, the
meeting, the gate and the apportioning.

### 2.5 (E) The evaluation at the roots of unity: the click's pointer

The exact evaluation ev: Z[Z_N] -> Z[zeta_N], ev(f) = sum over p of f_p
zeta_N^p, is a surjective ring homomorphism, exactly; its kernel is the
ideal generated by x^(N/2) + 1, which is the merge's cancel of 2.3, so
the first isomorphism theorem holds here exactly: Z[Z_N] / ker(ev) =
Z[zeta_N], the rows modulo the cancel are the cyclotomic integers. It
is also a *-homomorphism for the involution f*(x) = f(x^(-1)) (the
reflection of the phase), carrying f* f, the record's autocorrelation,
to abs(ev f)^2. The built evaluation is the tables C and S at the scale
256 (`core/phase.py`, reduce-and-flip so that C[p + N/2] = -C[p] and
S[p + N/2] = -S[p] exactly): the pointer (X, Y) = **E** f, a Z-linear map
into Z^2 that is NOT a ring homomorphism (at N = 64, **E**(e_1)^2 =
(64400, 12750) against 256 **E**(e_2) = (64256, 12800), COMPUTATION),
whose kernel contains the cancel and is larger than it; the weight is
the norm abs(z)^2 = X^2 + Y^2 = f^T **G** f, one bilinear form (2.2),
and then the ladder on the wheel (2.6). So "one relation, exactly" is
the exact ev, and on the engine it holds within the tables' rounding;
the document states both lines, the exact one as the algebra and the
rounding as the engine's declared constant. Source: DERIVATIONS_BEAM
section 1 (E), lines 282-283; section 6.7, lines 1826-1876;
[the click frame](designs/click_frame/DERIVATION.md) section 9 (2) (a),
lines 1464-1481.

**The two words "pointer" and "weight", one currency (the model owner's
word of 2026-09-24, 05:55Z, on the physicist's recommendation re-verified
twice, record 1679; Reviewer 3's naming of the clash on ONE_ACCOUNT.md
row (2)).** The pointer (X, Y) = **E** f and the weight X^2 + Y^2 of
this subsection are the ray law's click frame, the account of
`nature_beam` (HISTORY under the rule of chapter 8). Under the rule the
pointer of the rung (8.6) is one accumulator per record per receiving
Node that books the MOTION SQUARED, (a_now - a_before)^2 of the
receiver's own record per Node per interval, summed across the Nodes
and over the intervals; the ladder's weights of 2.6 ARE those pointers,
in one currency with the record's norm (the motion its insert booked)
and with the completion (the motion left on the board against what the
Nodes took); never the levels' squares (DESIGN.md section 5: with a^2 no
completion, a static level moving no receiver). The norm X^2 + Y^2 of
the record's pair of levels survives under the rule only as the click's
weight of the Node for the pair of records, Bell's J^2 of 3.6, not as the
pointer of the rung. The motion squared is a positive quadratic form on
the pair (a_before, a_now), so the read-out characterization of the
paper's section 5 stands under it; for a travelling character the two
forms cross the rung at about the same interval, each against its own
norm, the forms themselves differing by the factor kappa^2 per interval
(about 0.14 at 12 Links per period), and they differ on a standing
residual, which the levels' squares count and the motion does not.

### 2.6 (D) The division with the remainder kept, and the comparison

The count primitive: at each self-creation the accumulator gains its
rate, the count is the whole part it then holds in units of the wall,
that much is subtracted and the remainder stays, bounded below the
wall, its one owner; every wall crossed is the event. **The wording in
force is the code's** (`core.integer.by_drive`, read for the plan's K1
on the Boss's word): the count is abs(s) // d with the sign of the
accumulator, so the division is signed and truncating, the remainder
carries the accumulator's sign in (-d, d), and an accumulator at -1
against the wall 2 counts 0 and keeps -1 (a signed rate, the step
drive, first cancels what it had accumulated the other way); on a
non-negative accumulator (every unsigned count: the owed count, the
release, the lamp, the turn, the push per column, `by_clock`'s floors)
it is the Euclidean division, and there the two wordings agree. The
comparison is part of this verb: the ladder's detector 2 T u + T <= 2 N C_k,
an age against a key, a phase against a window, a threshold, itself a
division whose quotient is 0 or 1 and whose remainder is not read
(the paper: "the division with the remainder kept, together with the
comparison that is the event"). The superseded wording: "the Euclidean
division with the remainder kept" without the comparison ([Highlights](HIGHLIGHTS.md)
section 1 item 3, record 181, and 5.7 "The six operations";
[TERMINOLOGY.md](TERMINOLOGY.md)
"The six verbs"), right on every unsigned count and on the signed drive
only where the accumulator does not change sign; the wording that
matches the code is DERIVATIONS_BEAM section 1 (D), lines 266-270 and
284-287, and it is the one in force. No law changes by this: the code
is the law as built. Source: `src/event_universe/core/integer.py`
(`by_drive`, `by_line`, `by_clock`); DERIVATIONS_BEAM section 1 (D);
section 0, "The readout".

### 2.7 What is not one of the six

A root of the state at run time is the seventh verb, not admitted: the
meeting's norm abs(**t**) = isqrt(**t** . **t**) under the key
`meeting`, and the pushed row's pair under the key `optical` (the two
run-time roots [COUPLINGS.md](designs/couplings_algebra/COUPLINGS.md)
section 3 names), each declared by its design and neither a table
formed at load; Lorentz's gamma on a body's own counter and a bond's
contraction by 1 / gamma, which need such a root (DERIVATIONS_BEAM
section 10.4; [FULL_PICTURE.md](FULL_PICTURE.md) "Not reachable by the
six verbs"; Highlights 5.4, the Lorentz A and B line). A rounded
constant multiplying a row in flight (the rotation's tables, the one
place besides the meeting's root) is a declared rounding at load,
lawful under record 155 (6), not a verb; the meeting's `adv = (abs(t) +
Q/2) // Q` is a rounding at run time each interval, NOT a torus
operation in DERIVATIONS_BEAM's inventory (its exact form `acc +=
abs(t)` on Z_(N Q) stated there, section 1.2). No float, no true
division, no draw.

### 2.8 The three tests every rule passes

A rule enters the law only if it is generic (one primitive with
declared integers, no family name or kind, the engine branching on no
name), vector (one of the six verbs on the state vector, its rate at
most bilinear in the state, no root, no float, no rounding at run time
beyond the ones declared at load) and local (its own record and the six
neighbouring Nodes, fixed work and storage for a fixed K, nothing kept
at a Node); "generic" means exactly commuting with the 48, made of the
six operations, reading the neighbourhood alone (chapter 1, the road's
item 6). Source: [skills/workflow.md](../skills/workflow.md) "The three
tests of every rule" (record 202); Highlights section 1 item 4 and
5.4's line of record 202.

### 2.9 The couplings as verbs, by reference

Every rule the atom worlds and the light worlds run is one of the six
verbs on bounded integers or a stated composition of them, with the two
run-time roots of 2.7 as the exceptions: one row per coupling, 31 rows
(the clock's turn T then D; the owed count; the drive T then D with the
cap then P; the turn by momentum; the release; the lamp's birth; the
flight; the one reading B then G; the crossing a comparison; the push
B, T, D, G; the threshold and the window; the click; the face click;
the split P, B, D, T; the collision P; the merge G; the record's gather
G, B, D, E; the contact and the give D, T; the books G), in
[COUPLINGS.md](designs/couplings_algebra/COUPLINGS.md): the 31 names in
section 1, the per-row verbs in section 2's table, its one-line result
in section 3, which names beside the two roots the `wave` record's
square written as a product.

### 2.10 The quantities as algebraic objects, by reference

The table "The physical quantities, when each entered, where it lives,
and which of the six verbs act on it" of
[HISTORY.md](designs/algebra_transition/HISTORY.md), fifteen rows, one
line each: the amount on Z; the content M on Z, the non-compact scale,
free; the phase on Z_N; the multiplicity; the age; the number an
identity label, never arithmetic; the momentum vector **p** in Z^3; the
charge as a rational pair; the label flow **a** and the moments, a
reading; the family table the declared input on which no verb acts;
the couplings as integer matrices **C**; the wheel's coordinate u on
Z_W; the click's weight the bilinear form f^T **G** f on an element of
Z[Z_N], Born's rule the thing recovered (c_1 = 1, chapter 4.8);
the hand and the axis, a pseudoscalar under the 48; the clock's counts.
The dictionary from the algebra to the physics (mass = content,
momentum = the label, and the rest) is chapter 1.2 and is not restated.

### 2.11 The verbs at one interval, in their order

One interval of a record applies, in order, (T) on every accumulator,
(D) whose whole part is the event, (B) at the push and at the click,
(G) and (E) where rows are summed at one Node and where they end, and
(P) at a collision; on a record's state vector (x, D, **p**, tau, f,
acc_drive, acc_push, acc_owed) the lines are the hop, the phase, the
push, the crowd, the split, the sum, the click and the age, each one of
the six on bounded integers; the identity W = E'_0^2 + 3 **p** . **p**
(chapter 5.3) is not a line of the step but the step's invariant under
covariant-readings-v1. Source: the click frame section 9 (I), lines
1261-1290. Under the massive record kind of chapter 8 a record's row at
a Node is its two levels with the remainder, (a_now, a_before, r), and
one interval is 8.1's map with 8.5's coupling and 8.6's click; the
lines of this section are the rows that hop, the engine as built before
2026-09-23, kept as their record.

---

## 3. The click-to-click algebra and the reading rule

### 3.1 The two worlds, and the click as an action

Inside is the GameBoard: Nodes on the cubic lattice, integer rows on
them, and the tick, the interval's count, which no detector ever reads;
where no one measures. Outside is the game above the board: detectors
and their clicks only, which is not reality but is claimed to represent
it, the match shown result by result (Highlights 5.4 item 8, record
762). A detector D at a Node has its own count n_D, its count of
intervals stretched by what arrives at it (the age wall's member at
coefficient 1); it never reads the tick, only n_D. **A click is an
action, not a passive read** (the owner's word of 2026-09-23, record
1139, the Boss's reading; P11): the record ends at the detector, its
content enters the detector's own record, and the detector's count
advances; the click is the event of receiving a packet, stamped with
n_D, a triple (the Node, n_D at the arrival, what arrived); a record is
read once by one comparison and deleted: the only read-out, the one
deletion, and the one non-local step (the pair's gather, 3.6). A
click family F_D is the set of clicks of one detector and its six
neighbours, each with its counts and its contents; the counts of one
detector add, so a click family is a free abelian monoid of counts
whose ratios lie in Q. Source: the click frame section 0
"Definitions", lines 18-39; section 1, lines 244-270; section 9 (1),
lines 1440-1456.

### 3.2 The reading rule, one sentence; the kinds

**A click at a detector, a count between clicks on the detector's own
record, and a ratio of such counts are what is compared with nature;
nothing measured inside the board is compared; a reading of the board
itself is a diagnostic** (the owner's central idea, [record 1104](LOG_2026-09-20.md);
the paper's abstract, record 1115; P11: only a detector's reading is a
measurement, a click, a record's moments or an external thing's reading
as the world file declares). The wordings of the sources agree on this
sentence and add to it in three places, each kept as its record: the
click frame reads "a ratio or a difference of counts at a click, never
the tick" (a difference of counts being a count between clicks);
[Light Outside](designs/light_outside/DERIVATION.md) adds that every
Outside formula carries its own transformation, from the emitter's
clicks at its place to the detector's clicks at its place, and a
reading at another place is a detector at that place (Highlights 5.4,
the owner's word of 2026-09-22); the paper's P11 lists the readings admitted. The
five kinds: DETECTOR, GAMEBOARD, COMPUTATION, HOST, CONVERSION, as the
head of this file defines them ([the FAIL rows file](designs/fail_rows/WHAT_IS_MISSING.md)
and [Newton from the clicks](designs/newton_clicks/NEWTON_FROM_CLICKS.md)
section 6, the same five).

**The kind of a body's own record (the reading in force, pending the
owner's one line; the Boss's reading of 2026-09-23 on records 991, 1046
and 1139).** A body's own record (its momentum, its place, its `become`
at a count of its own clock) is GAMEBOARD and enters no comparison; a
body that carries a detector's count under the world key `clock_stamp`
is DETECTOR for that count alone (the moving detector with mass, chapter
5.6); Highlights 5.4 item 9's "a body's own record" among the DETECTOR
kinds ("DETECTOR: a click, a record's moments, a body's own record, an
external thing's reading") is the earlier wording, refined by record
991 (the reviewer's read J: "the body's own give rows and count are the
host's view of a store, GAMEBOARD by record 281's words; the DETECTOR
level is the faces'") and by record 1046 (no GAMEBOARD reading, a
body's own record among them, is an input to Newton's chain). The
Newton files and the FAIL rows file use the refined wording (a body's
own record under GAMEBOARD); this file follows it, and the Boss puts
the one line to the owner (the plan's K6).

### 3.3 The count ratios: the two one-way factors and the place-to-place factor

Names (the click frame's, the convention of this file; the plan's K7):
A the detector at rest at Node 0, in no crowd, its own count per
interval 1; B the moving record on an axis, v = 1 / k Nodes per interval
(k a whole number of intervals per hop, the hop pattern x_B(t) =
floor(t / k)), its own count per interval r, a rational n_r / d_r kept
by an accumulator with its remainder, to be found or measured, never
assumed; T the number of a detector's own counts between two records
it emits; k_AB is B's own count between two arrivals of A's records,
over T; k_BA is A's own count between two arrivals of B's records, over
T. Every k is a ratio of two counts of one detector, hence DETECTOR;
every tick is GAMEBOARD arithmetic the reader never sees. On the law,
exactly in the mean (rung 1 on the counts, the remainder below one hop
and one count, the accumulator's carry never accumulating),

    k_AB = r / (1 - v),        k_BA = (1 + v) / r,

and their ratio k_BA / k_AB = (1 - v^2) / r^2. ([Light Outside](designs/light_outside/DERIVATION.md)
section 0 defines k_AB the same way, the count B reads between two
arrivals over the count A read between the two births, and writes both
cases under the one letter, A moving away, (r_B / r_A) (1 + v), or B
moving away, (r_B / r_A) / (1 - v); the plan's K7 is no conflict.) The general form, Theorem 1 of
[Einstein Outside](designs/einstein_outside/DERIVATION.md) (the
place-to-place factor), under (A1), (A3) and the reading by clicks: for
X moving at **v**_X and Y at **v**_Y (Nodes per interval, both below c),
**s** the unit vector from X's Node at the emission to Y's Node at the
arrival, r_X and r_Y the two records' own counts per interval,

    k_XY = (r_Y / r_X) x (1 - s . v_X) / (1 - s . v_Y)        (c = 1; in general s . v / c),

exactly in the mean on an axis (rung 1) and as the instantaneous limit
where **s** turns (rung 2). Its corollaries: X at rest and Y receding
gives k = r_Y / (1 - v), Y at rest and X receding gives k = (1 + v) /
r_X; the round trip k_XY k_YX is r-free for every pair of rates; the
transverse factor is 1 / r_X; two records at rest in crowds give k_XY =
(1 + k_crowd,X) / (1 + k_crowd,Y); the composition k_XZ = k_XY k_YZ
exactly, and by (A3) the chain through Y is the only way a packet
reaches Z from X through Y. The one fact the theorems share: a ratio
of two counts of ONE detector is r-free (the round trip, a radar
velocity, a radar angle); a ratio of counts of TWO detectors carries
r_Y / r_X (a one-way Doppler factor, a rate, an energy). Source: the
click frame section 1 and section 2 (a), lines 244-293; Einstein
Outside Theorem 1, lines 355-397, and lines 466-469.

### 3.4 Locality Outside and discreteness Outside, two theorems; the one assumption beyond them

**Locality Outside** (a theorem of (A1) with the definition of Outside,
P6, nothing leaves the board but clicks): every Outside event is a
click, every click moves information one Node at most, so every
Outside passage is a chain of neighbour steps between neighbouring
places, and the Outside inherits the Inside's locality through the
conversion; it forbids a reading that would need a jump, a velocity
above one Node per interval of the tick, which in a detector's own
count is 1 / r_D Nodes per count (so light in a crowd reads its c in
the detector's stretched count and not above it, series T's clocks,
r_D = 1 / 2.65 at 3 Links, DETECTOR), and a detector reading at a
place no chain of clicks reaches; the one exception is the pair's
click, one gather of one record from both settings, the law's one
non-local operation. **Discreteness Outside** (the quantum of the
Outside step, a theorem of (A1) and the conversion; Theorem 3 of
Einstein Outside; M3, the counts' ratios over Q): (i) the least
separation of two places read is one Link; (ii) the least time a
detector times by itself is a pulse to its neighbour and its return,
two intervals Inside, two of its counts at r_D = 1; the tick itself is GAMEBOARD and never read;
(iii) the least step of a moving record is one Node per k counts, so
the Outside velocities are the ratios 1 / k, a ratio of two whole
counts, never a real number, with the velocity quantum

    1 / k - 1 / (k + 1) = 1 / (k (k + 1)),   finest near c and coarsest near rest,

and (iv) c Outside is one Link per the least count, the bound of (iii)
at k = 1, Einstein's second postulate in the click language; the
Outside step of a transponding record in these quanta is place_(j+1) -
place_j = e_j **d**_hat (the unit vector of the direction D) with e_j in {0, 1} and count_(j+1) - count_j = 1
+ owed_j in the detector's own count; read at a distance the count
between two clicks is multiplied by the factors of 3.3, with r the one
quantity of the step above that (A1) leaves free: r = 1 on the law,
sqrt(1 - v^2) up to m^2 v^2 under (A2). The continuum's formulas cannot
say why the world above is quantized; the Inside gives it. **The one
assumption beyond these two theorems**, stated as an assumption and not
a theorem (the owner's word of 2026-09-22, "the basis is Inside, and we
are operated Outside, by emitters and clicks"): its first half, that
every Outside passage is Inside's passage read by clicks, is (A1) with
the definition of Outside; its second half, that we are built of clicks,
that the emitters and the detectors are themselves records of the board
and not a second kind of thing, is MORE than (A1): it is the statement
that the apparatus is inside the law, which the law today does not
carry (a detector, a lamp and an external body are declarations of the
world file, not records that hop), an assumption about the world or a
programme for the law. Source: the click frame section 0, lines 53-95;
section 9 (III), lines 1320-1398, and the closing theorem, lines
1452-1456; Einstein Outside Theorem 3, lines 524-566.

### 3.5 The conversion as a map, in the algebra's own words

The conversion Phi: Inside -> Outside is a composite of four maps, each
with a name in the algebra, the composite with none: on the amplitude,
Outside = rung o (chi_1 of f* f) o ev on the record's element of
Z[Z_N] (a ring homomorphism, 2.5; a pure state's square, the click's
weight R(f) = abs(ev f)^2 = chi_1(f* f), chi_1 the first character of
the commutative *-algebra C[Z_N], a positive quadratic form on the
lattice; a threshold, the rung); on the schedule, Outside = (Nodes
apart) / (counts apart) in Q, on which the Lorentz group up to scale
acts (chapter 5.1); both sides read at the detector's own count. The
names that fit, exactly, in a limit, or not at all (the click frame's
table): a ring homomorphism with a kernel, the first isomorphism
theorem, EXACTLY for ev at the exact root, on the tables within their
rounding; a positive quadratic form on a lattice, EXACTLY (the lattice
Gleason, chapter 4.8: forced in form, free in its Galois constants, c_1
= 1 Born); a state on a *-algebra with the GNS construction, EXACTLY
for Born at one arm at the exact root; a stochastic map (a Markov
kernel), EXACTLY within 1 / N as a frequency law over one deterministic
wheel, not a random draw; a group action of the Lorentz group up to
scale, EXACTLY over Q on the click families and IN THE LIMIT on the
amplitudes; "Outside is Inside modulo a kernel" for the whole
conversion, DOES NOT FIT (the composite is quadratic then thresholded;
what no click reads, the tick, the ordering, the remainders, the scale
r, the phase's origin, is a set of invariances and unread coordinates,
not an ideal); a functor between two categories, DOES NOT FIT. The
conversion table (nine Inside formulas, their Outside readings, the map
and its order, the inverse, the registered reading by kind) is the
click frame's section 7 (3), by reference. Source: the click frame
section 9 (2) to (5), lines 1458-1681; section 7 (3), lines 925-979.

### 3.6 The pair: the record of tensor rank 2, the settings, the one gather

A lamp releases one record with two arms and two joint labels, 00 and
11, of weight 1 each: in the lattice's algebra the record is psi = (00)
+ (11) in Z^2 (x) Z^2 (the arms' label spaces), tensored with its phase
in Z[Z_N]; entangled by construction (the coefficient matrix the
identity, of rank 2; no integer vectors **u**, **v** give **u** (x) **v**
= psi); in flight each arm's row moves on its own line with its phase
turned per Link, the weights carried unchanged, nothing of one arm
written on the other (B1). A detector's setting is the integer s of its
`phase_window`; at the detector the arm's label pair is rotated by the
integer matrix **U**_s = [[C'[s], S'[s]], [-S'[s], C'[s]]], C' and S'
the half-angle tables at 1 / 256, with **U**_s^T **U**_s = n_s **I**
exactly, n_s = C'[s]^2 + S'[s]^2 (B2, rule R, verb (B)). The click of a
pair is one gather of the one record from both settings at the
completion interval (P6): the joint pointer J(o_A, o_B) = sum over the
labels l of U_a[o_A][l] U_b[o_B][l], the Node's weight R = J^2, the
birth wheel's u selecting one of the four Nodes through the rung (B3);
assumed of the world and not supplied by the law: the settings chosen
freely of the record, and the reading the click with c_1 = 1 (B4, P10);
no Hilbert space is assumed. The non-locality sits in one object, the
pair's record of tensor rank 2, carried by local verbs on two arms and
read by one gather at two clicks; the law has the textbook's structure
with Z in place of C, its one departure the rung. What follows exactly
(the marginals, the finite-N Bell value) is chapter 4.9 and 4.10.
Source: the click frame section 10 (1), lines 1713-1739, and lines
1850-1860; [the entanglement page](designs/click_frame/ENTANGLEMENT_PAGE.md)
paragraphs 1 to 3.

---

## 4. The exact identities: one line each, and the link to the proof

Exact on the lattice: each an identity of the ring, the tables and the
declared world conditions, stated in one line with its hypotheses and
the link to its proof; no proof is copied. The kind of every number is
named; "rung 1" is exact on the GameBoard within the accumulators'
remainder, "rung 2" a limit (the continuum, the shell mean, the fan of
every direction).

- **4.1 The accumulator's closed form and the flight's line.** At a
  constant rate every component of the linear block has s(t) =
  floor(s_0 + r t), r the rate as a fraction of the wall (the carries
  made by t, the residual on the torus (s_0 + r t) mod 1); a row's
  Links by its age are m_D(tau) = floor((2 tau S_1 Q + T_D) / (2 T_D))
  and its k-th Link falls at tau_k = ceil((2 k - 1) T_D / (2 S_1 Q)),
  rung 1. [DERIVATIONS_BEAM](DERIVATIONS_BEAM.md) section 0 (the two
  blocks) and section 11.1.
- **4.2 The pace of every direction and its bound.** A row advances
  c_D = Q abs(D)_2 / T_D Links per interval on its direction, T_D =
  isqrt(3 abs(D)_2^2 Q^2); 32 / 55 on a heading (T = isqrt(3 Q^2) = 110
  at Q = 64); S_1 Q <= T_D by Cauchy-Schwarz (the Manhattan bound, at most
  one Link per interval, equality on the body diagonals); an isotropic
  pace under it is at most the slowest line's, 1 / sqrt 3, the flight
  operator's norm (rung 2); on the table c_D = Q abs(D)_2 / T_D lies
  within 1 / T_D above 1 / sqrt 3, equal to it on the body diagonals,
  since the isqrt rounds the wall down (rung 1); read Outside
  as the arrival count over the Euclidean distance, c_D = j abs(D)_2 /
  ceil((2 j S_1 - 1) T_D / (2 S_1 Q)) -> Q abs(D)_2 / T_D as j grows,
  or by a pulse and its return; the anisotropy 1 / c_D^2 = 2.954, 2.971,
  3.000 on the heading, the face diagonal and the body diagonal
  (COMPUTATION), series Q's 290 of 290 face clicks at the derived tick,
  Node and face (DETECTOR). DERIVATIONS_BEAM sections 2.1 and 13.2 (a);
  [Light Outside](designs/light_outside/DERIVATION.md) II.1.
- **4.3 The books and the continuity equation.** Every message
  released is on exactly one line of the books at every interval:
  released = in transit + absorbed + escaped (+ cancelled) per family,
  in amount and in content, exact at every tick (GAMEBOARD, the
  engine's ledger); for paid messages momentum is conserved exactly
  and the third law holds message by message; from the books, n(x, t +
  1) - n(x, t) = - sum over a of [J_a(x, t) - J_a(x - e_a, t)] + b(x, t)
  - q(x, t), the discrete continuity equation, an identity of the
  ledger in integers with no remainder, its continuum form second order
  in the Link over a feature's width (a feature of width ell Links
  carries a relative error of order (1 / ell)^2; DERIVATIONS_BEAM 25.4
  (3) and (5)). DERIVATIONS_BEAM 9.1 (I5) and 25.4; the paper's section
  2, "The GameBoard as a system of information transfer".
- **4.4 Gauss's law of a free family's flux.** A row released inside a
  closed surface crosses it once and never returns (the walk a
  translation, no collision on a fan or a lone beam), so after the
  front has passed the amount crossing any closed surface per interval
  equals the release inside it: sum over the surface's Ports of the
  amount crossed = q, exactly; registered as a GAMEBOARD reading of the
  probes; its click reading (a shell of rest detectors' counts against
  the source's release rate) NOT READ. DERIVATIONS_BEAM 3.1; [Newton
  from the clicks](designs/newton_clicks/NEWTON_FROM_CLICKS.md) 1.4 (c)
  (iii).
- **4.5 Theorem 1 (the 24 of the name).** The maps of the six Ports
  onto themselves that send opposite Ports to opposite Ports form the
  group of the signed permutations of the three axes, of order 2^3 x 3!
  = 48; the determinant is a homomorphism onto {+1, -1}; its kernel, the
  group of order 24 (the rotation group of the cube), has index 2 and is
  the symmetric group S_4 on the cube's four body diagonals; the hand,
  the one pseudoscalar column of a row, sent to det(g) times itself,
  tells the 24 rotations from the 24 reflections, as does an axial
  vector. Chapter 1.1 and 1.4; the paper's Theorem 1.
- **4.6 Theorem 2 (the split is an isometry whose conjugate transpose
  inverts it).** The split (w, m, p) -> ((w a_i, m A, p + t_i))_i
  preserves sum w^2 / m for every nonzero integer vector (a_i) with A =
  sum a_i^2; the conjugate transpose of the table (the same weights with
  the turns reversed) applied to its outputs, followed by the normal
  form, returns the input up to the scaling (k w, k^2 m) with k = A; the
  rotation satisfies **U**_s^T **U**_s = n_s **I** exactly with n_s =
  C'[s]^2 + S'[s]^2 and multiplies a record's norm by n_s / 65536, an
  isometry only up to the tables' rounding (65705 / 65536 at N = 64, s
  = 1, COMPUTATION). The paper's Theorem 2; DERIVATIONS_BEAM 6.1.
- **4.7 Theorem 3 (the interval is injective between clicks).** On the
  quotient of the rows' module that forgets the age, with the record's
  event history fixed, for an interval without a click, an end at a
  face or the border, or a collision, and for splitters whose joint
  table **B** satisfies **B**^H **B** = A **I** (the balanced splitter
  with the turn N / 4 among them), M o R o S o F induces an injective
  Z-linear map of the quotient into itself: no rule of the interval
  deletes a weight, a multiplicity or a phase; the click is the one
  deletion; a collision, where it acts, is a bijection of the
  GameBoard's states that is not linear; a body's drive under the
  engine's rule of a lost coincident fire is outside the theorem. The
  paper's Theorem 3. Beside it, exact: the event-driven form of the
  interval is bit-identical to the interval stepping on every world of
  beam-v1; two events at one t* commute exactly when the Nodes they
  read and write are disjoint; across events the feedback block has no
  closed form. DERIVATIONS_BEAM 11.3 and 11.5.
- **4.8 Theorem 4 (the quadratic read-out on the phase lattice, a
  lattice Gleason).** Under (a) the phase rotation changes no weight,
  R(x f) = R(f); (b) the balanced splitter conserves for every two
  inputs f, g in Z[zeta_N] (the rows after the cancel, 2.3),
  R(x^(N/4) f + g) + R(f + x^(N/4) g) = A_2 (R(f) + R(g)); (c)
  R(f) >= 0; (d) R(0) = 0; (e) R not identically zero; with N a power
  of two, N >= 4: A_2 = 2 and

      R(f) = sum over odd j, 1 <= j < N / 2, of c_j abs(sigma_j(f))^2,   c_j >= 0,   sigma_j(f) = sum over p of f_p zeta_N^(j p),

  the sigma_j the Galois conjugates of ev, sigma_1 = ev; every such R
  is a positive quadratic form on the lattice, homogeneous, R(a f) =
  a^2 R(f); two rows a x^p and b x^(p + Delta) at one Node read R =
  C_Sigma (a^2 + b^2) + 2 a b K(Delta) with C_Sigma = sum over j of c_j,
  K(Delta) = sum over j of c_j cos(2 pi j Delta / N), K(0) = C_Sigma, K(N / 4) = 0,
  K(N / 2) = -C_Sigma; Born's form abs(ev f)^2 is c_1 = 1 and the other
  c_j = 0 (P10, the one imported constant); the built click's f^T **G**
  f with **G** = **E**^T **E** is its fundamental to the tables'
  rounding, and (**E** f)^T (**E** f) = f^T (**E**^T **E**) f bit for bit
  on integers. Not assumed: continuity, a dimension, the form of R on
  one row, or Theorem 2's A. The paper's Theorem 4; DERIVATIONS_BEAM
  6.5 (the hypotheses at :1592-1609; the Gram matrix at :1651-1658)
  and 6.7.
- **4.9 Theorem 5 (exact count marginals).** For a pair with labels
  {0, 1} of equal weight and settings a, b, with J(o_A, o_B) = sum over
  l of U_a[o_A][l] U_b[o_B][l] and R = J^2: the first party's outcome is
  + exactly for u < N / 2 and - for u >= N / 2, for every (a, b) and
  every N; the second party's count of + is exactly N / 2 for every (a,
  b) unless 2 N R(+, +) / C_K, C_K the record's total weight 2 n_a n_b,
  is an odd integer (a tie of the rung), and
  then N / 2 + 1; no tie occurs at the twelve grains from 8 to 1024 nor
  at the CHSH labels for any multiple of 8 up to 4096 (COMPUTATION);
  the marginals are no-signalling exactly, and the order signals
  (chapter 6, row 1c). The paper's Theorem 5; the click frame section
  10 (2).
- **4.10 The finite-N Bell value, and the local bound.** With the
  counts of Theorem 5 and off a tie, E_N(a, b) = 4 c_(++) / N - 1 and
  abs(E_N(a, b) - cos(2 pi (a - b) / N)) <= 2 / N + 4 arcsin(sqrt 2 / (2
  rho)) < 2 / N + 0.0111 with rho = N_t - sqrt 2 / 2 (N_t = 256 the
  tables' scale), so at the labels (0, N / 8, N / 4, 3 N / 8), abs(S(N) -
  2 sqrt 2) <= 8 / N + 0.0444; S(N) = 8 (c_1 + c_1') / N - 4 is an exact
  rational for each N: 11 / 4 at 64, 45 / 16 at 256, 181 / 64 at every
  power of two from 512 through 8192, 5793 / 2048 at 16384 (COMPUTATION, met by series L and
  L6, DETECTOR); Tsirelson's 2 sqrt 2 is the limit, not a bound of the
  construction (S(N) lies on both sides of it); E(a, b) = cos(2 pi (a -
  b) / N) is an identity of the rotation algebra before rounding, and a
  product state (tensor rank 1) gives abs(S) <= 2, Bell's inequality in
  the CHSH form; under the phase-form window (a local deterministic
  response of each party to its own row's phase) S = 2 exactly at any
  count, an identity of the window's form and a theorem of every local
  read-out. The paper's finite-N Bell theorem; the click frame section
  10 (2), lines 1741-1807; DERIVATIONS_BEAM 6.5's cited rows; the FAIL
  rows file, row 1b.
- **4.11 E = h f as an identity of the release; the cost; the entropy
  and the support bound.** A release costs the emitter h s per unit born,
  s its turn on the K pair, so the content of one click is E = h s = (h
  N) f, an identity of the release (declared at the release, recovered
  at the click as the content carried whole; E = h f_flight would need
  the declaration s = n / d, met by no registered world); the cost of a
  record in units of content h s is the sum over the ends of the rows'
  amounts, k times the product over the path's splits of (sum_i a_i),
  and information out <= log2(Nodes) bits (the Holevo bound as the
  ladder's count); the ladder's identity H(K) + H(U | K) = H(U) = log2 N,
  bits read + bits erased = log2 N per record; on the phase circle abs(supp
  f) x abs(supp f_hat) >= N (the Fourier transform's, Donoho and Stark;
  equality at a comb of every eighth phase at N = 64) and the Weyl
  relation **V** **U** = omega **U** **V**, omega here a primitive N-th
  root of unity, **U** the shift by one phase and **V** the multiplication
  by omega^y (operators, bold uppercase). DERIVATIONS_BEAM 6.4, 6.1, 14 and 22.1; Light Outside II.2.
- **4.12 The click's indivisibility, and Malus.** One click per record,
  never two: the ladder chooses one Node and deletes the offers, P(D1
  and D2 in one record) = 0 exactly (the cancel exact; mz_equal 64 / 0,
  DETECTOR); Malus, P(pass) = cos^2 theta, theta the angle between the label and
  the analyser, on the rotated label's Gram
  form within the tables' rounding (+0.0019 at 22.5 degrees, below 1 /
  256; 128 of 256 at 45 degrees, DETECTOR, series A12). Light Outside
  II.7 and II.9.
- **4.13 The theorem of covariant readings; the minimal mass.** Every
  quantity defined by covariant operations on the linear block's limit
  (the retarded potential and its derivatives, the crossings of world
  lines, the proper time along a world line, the sums of the rows'
  energy-momentum vectors) transforms as the block does, so a body all
  of whose rules are such readings inherits the block's symmetry, a
  theorem for the linear block (its rules on the tree are the identity
  covariant-readings-v1 of chapter 5.10); the smallest content of a
  family whose bodies carry a whole charge is its reduced denominator d
  (the law does not impose the whole charge). DERIVATIONS_BEAM 17.1 and
  16.2.
- **4.14 A negative result: the constancy of c is not a theorem of the
  six verbs.** A dispersive flight passes the six verbs, locality, the
  books, both theorems, the isotropy and the generic requirement as
  written, and disperses phases and, in the mean, frequencies; so the
  constancy of c is the declared postulate P9 (the flight table indexed
  by direction and age) and not a theorem of the six verbs with
  locality: REFUTED as a theorem, kept as a declaration. DERIVATIONS_BEAM
  section 27 (Highlights 5.4, "the proof of c").
- **4.15 The derivation map, by reference.** Sixty formulas, one row
  each with the verbs and premises it starts from, its closed form, its
  section, its script, its registered check, its pin before the run, the
  order of the expansion, the error term and its status (R reached, F in
  form, B a bound, D a different law, I an input, X refuted, H a
  hypothesis with pins), and the Einstein map E1 to E19 beside it:
  DERIVATIONS_BEAM 21.2 and 21.4. This file lists no status the map
  does not.

---

## 5. What is reached under named hypotheses, each with its hypotheses and its kind

HISTORY UNDER THE ONE ALGEBRA (the model owner's adoption of record 1875,
"everything is algebra"; the correspondence audit of record 1942): chapters 1
to 7 are the ray law's (beam-v1) algebra and its readings; every SHOWN in
them is a reading of the retired ray law's worlds, not of the one algebra of
chapter 8 and 9.12 to 9.30. In particular the crowd clock and the age wall
(5.4; the wall's standing NOT NOW by record 941, retired here), the shell mean
and the delay field (5.4, 5.6, 5.9) and the cosmology rows of chapter 6 are
not laws of the one algebra: 9.22 (8a), 9.29 and 9.30 state what stands in
their place (the universality of the tick; the fall into a declared well; the
pair-field hypothesis outside the law).

**The hypotheses, named once, verbatim from their owning files.**
(A1) A click is the passage of information from Node to Node, at most
one Node per interval: c is the unit, the same in every family, and
nothing passes faster ([the click frame](designs/click_frame/DERIVATION.md)
section 0; the law as built meets it). (A2) A click's content is an
amplitude with a phase that splits each interval between staying and
hopping, the mass the staying share: the packet that passes is
converted by its amplitudes (the same; the law's rows do not have it:
they hop whole, so the law as built does not meet it). (A3) Locality
Outside: every Outside passage of a body or a signal is a chain of
clicks between neighbouring places, so the Outside inherits the
Inside's locality through the conversion; it forbids a velocity Outside
above one Node per interval, a jump, and a reading at a place no chain
of clicks reaches ([Einstein Outside](designs/einstein_outside/DERIVATION.md)
section I, the owner's named assumption of 2026-09-22; the click frame
states it as a theorem of (A1) with P6, chapter 3.4, and this file
lists it as the paper does, a named hypothesis, with that derivation
beside it). For Newton, the five assumptions of the law as built and
the shell mean: (W1) the age wall, (W2) the push and the drive, (W3)
the flight blind, (W4) the reading by clicks, (W5) the clock as a pulse
and its return; (M) the spreading, arithmetic and not an assumption: K beams over
a shell of N(r) Nodes, N(r) -> 4 pi r^2 (2 pi r on the plane), "the
shell mean" below; (K) the declared inputs the formulas carry as
constants, all of kind 2: the pair [n, d], the width S_w, the release
eta, the fan's count K, Q, N, the lamp's pair [n_K, d_K], the quantum h,
and beside the law under `optical` the coefficient c_f = 1 + gamma_PPN
(Einstein Outside section I, :198-253). For light, (L1) to (L9) (Light
Outside section I, :244-335). Every item below carries its hypotheses, the limit
taken, the order, its error term, its status (SHOWN, exact under the
hypotheses at the rung named; SHOWN IN FORM, the form with a constant
declared; MET, a registered reading inside its pin; FAIL; NOT READ; a
UNIT or an INPUT) and its kind. Every physics name is the thing
compared with.

### 5.1 The click theorem: Lorentz's factors from the clicks

**Hypotheses:** (A1); (A3) and the conversion of chapter 3 for the
r-free lines; (A2) for the scale. **Statement** (the click frame section
0, records 745 and 749): the conversion from the lattice's momentum to
motion read by clicks is Lorentz up to a correction of relative order
m^2 v^2 / 6 in the rate, second order in v at a fixed mass angle m
(the spacing over the reduced Compton wavelength) and vanishing as m ->
0, exact in the continuum limit, with the lattice's own anisotropy
beyond. In the algebra: let G be the transformations between click
families that carry counts to counts and Nodes to Nodes Q-linearly in
the mean and preserve (A1). (i) G is a group, and with (A1) alone it is
the Lorentz group up to scale: in one dimension the maps (u, w) -> (k u,
w / k) (and the reflection u <-> w) on the light-cone coordinates u = t - x, w = t + x, the boosts
with the invariant u w = t^2 - x^2, whose parameter is the one-way
factor k = sqrt(k_AB k_BA) = sqrt((1 + v) / (1 - v)) for every r (the
round trip reads nothing of r) and whose dilation lambda (the boost's
scale) = sqrt(k_AB / k_BA) = r / sqrt(1 - v^2) carries r alone; the axiom that fixes lambda = 1 is the equality of the two one-way factors,
k_AB = k_BA, that is r / (1 - v) = (1 + v) / r, r^2 = 1 - v^2, by one
multiplication (the relativity principle for the two directions); then
v = (k^2 - 1) / (k^2 + 1), gamma = (k + 1 / k) / 2, the boost's own clock
rate 1 / gamma = sqrt(1 - v^2) = r, the boosts composing by k_1 k_2 (a
one-parameter abelian group, SO(1, 1)); in three dimensions the Lorentz
group SO(1, 3) up to scale and translation (Alexandrov and Zeeman: the
bijections of Minkowski space preserving the causal order). Over Z it
would not be a group: the only cone-preserving bijections of the
integer pairs are the reflections, the 48 in three dimensions, and the
inverse of a map such as (2, 1) is not Z-linear; over Q, under the
axiom, G is the boosts with rational k, dense in SO(1, 1), the Lorentz
group up to scale its closure. (ii) With (A2) the group acts on the
amplitudes as the covariance of the discrete-time Dirac walk: the boost
carries the walk's dispersion cos omega = cos m cos kappa (omega the
walk's frequency angle per interval, kappa its wave-number angle per
Node, m the mass angle) to itself to second order (omega^2 - kappa^2 = m^2 + O(4)), so it fixes the
detector's own rate at

    r = m / omega = sqrt(1 - v^2) (1 - kappa^2 / 6 + O(4)),   kappa^2 = m^2 v^2 / (1 - v^2),

from omega^2 = m^2 + kappa^2 - m^2 kappa^2 / 3 + O(6): a correction of
relative order m^2 v^2 / 6 (the three wordings of the sources, m^2 v^2
/ 6, kappa^2 / 6 and "up to m^2 v^2", are one order; the sign depends
on which velocity is named, above sqrt(1 - beta^2) against the
identity's beta (beta = v / c, the pace over c), below sqrt(1 - v_g^2) against the group velocity v_g
the clicks read, the click frame :877-885);
beyond second order in the angles the covariance fails, and in three
dimensions the board differs from the world from the fourth order on
(the walk's kappa^4 anisotropy). (iii) The lattice's own symmetries are
the 48, which contain no boost (finite, where a boost has infinite
order), so the symmetry is Outside and not Inside. **The law as it
stands:** it meets (A1) and does not meet (A2) (its hop a whole-record
schedule, `by_drive` with `at_most` 1, no staying amplitude, no
interference in flight to make the square root), so its clicks carry
the group of (i) and, read by one clock, Lorentz's radar, and lack the
amplitude of (ii) that would fix r at sqrt(1 - v^2): on the law r = 1,
k_AB = 1 / (1 - v), k_BA = 1 + v, a dilation by gamma away from
Lorentz, its round trip Lorentz's and its one-way factors not. **The
verdict in one line:** LORENTZ FROM THE CLICKS GIVEN the line k_AB =
k_BA, which is r^2 = 1 - v^2 for the moving record's own count; NOT
WITHOUT IT; every wall of the law is linear in the Manhattan momentum,
and the square that would give it is a declared identity (5.10). **The
r-free lines, Einstein's exactly from (A1), (A3) and the conversion**
(Einstein Outside II.2, II.3, II.5; Theorems 1 and 2): the round trip
k_GR k_RG = (1 + v) / (1 - v), Einstein's radar Doppler, under every r
(rung 1 within 1 / T; its pins 3, 5/3, 9/7, 17/15 at v = 1/2, 1/4, 1/8,
1/16, NOT READ); the composition of velocities w = (v_R - v) / (1 - v
v_R) and inversely v_R = (w + v) / (1 + w v), a ratio of one detector's
own counts, under every r_D (SHOWN, rung 1; NOT READ, pins 2/5 and
-2/7); the aberration tan theta_D = sin theta / (gamma (cos theta - v))
from the ratio of the transverse and longitudinal radar scales, under
every r_D (SHOWN, rung 1; NOT READ, the pin 120 degrees at v = 1/2).
**The scaled lines, Einstein's if and only if r^2 = 1 - v^2:** time
dilation, r = sqrt((1 - v^2) k_GR / k_RG) from the two one-way factors
read at one ground detector (DETECTOR; SHOWN in r; MET under the
identity, series S; FAIL on the law, row 4a); the one-way Doppler 1 + z
= k_RG = (1 + v) / r, on the law 1 + v, under the identity gamma (1 +
beta) with beta = v / c, under the line sqrt((1 + v) / (1 - v)) (SHOWN in r; FAIL on the
law, row 4b's 0.2636 against 0.315 at beta 0.2674, DETECTOR; MET under
the identity, 0.3674 for 0.369 +- 0.003, series S, DETECTOR); the
transverse factor 1 / r (SHOWN, rung 2; FAIL on the law, 1 against
gamma; NOT READ); length contraction L_G / L_own = (1 - v^2) / r_D and
L_D / L_0 = r_D, both 1 / gamma if and only if r_D^2 = 1 - v^2 (SHOWN in
r; FAIL in form on the law, asymmetric; NOT READ). All kinds DETECTOR
where read; r itself NOT READ. Source: the click frame section 0 and
section 2; Einstein Outside II.1 to II.5 and its verdict table.

### 5.2 The radar reading: Einstein's definition, adopted and named

**Hypotheses:** (A1), (A3), (W5). A detector D emits a pulse at its own
count n_e and receives its return at n_r from a transponding record at
another place; it assigns x_D = (n_r - n_e) / 2 and t_D = (n_r + n_e) / 2
(c = 1; in Links x_D = c (n_r - n_e) / 2), both DETECTOR on D's own
record. The halving is Einstein's 1905 light-signal definition of
distance and simultaneity (Bondi's radar convention), adopted as a
DEFINITION and nothing more; it takes nothing of Lorentz's beyond the
one-way pace being the same both ways, which is (A1) on the lattice.
For D at rest in no crowd the radar is the lattice's own coordinates,
GAMEBOARD numbers made DETECTOR by the pulse; for D moving at v with the
rate r_D, a reflection at the lattice Node X at the tick t_1 reads

    x_D = r_D (X - v t_1) / (1 - v^2),   t_D = r_D (t_1 - v X) / (1 - v^2),   (t_D, x_D) = lambda x Lorentz_v (t_1, X),   lambda = r_D gamma,

the moving detector's radar coordinates Lorentz's up to the one scale
r_D (lambda here the radar's scale) (SHOWN, rung 1; NOT READ: no moving radar detector registered).
The rows that need the definition: the boost's form as a map of
coordinates and the two readings of a length at equal t; the rows that
are convention-free are the round trips and the ratios of half round
trips (5.1's r-free lines). Source: Einstein Outside Theorem 2,
:418-466; the click frame section 2 (b).

### 5.3 The energy-momentum relation, and the identity's exact square

**Hypotheses:** (A1), (A2) and the law's own Planck map (E = hbar omega,
p = hbar kappa, E_0 = hbar m, hbar the reduced action h / 2 pi, omega
and kappa the walk's frequency and wave-number angles in steps of the
circle) for
the relation; on the tree, the identity covariant-readings-v1 for the
square. Under (A1) and (A2) the walk's cos omega = cos m cos kappa gives
omega^2 - kappa^2 = m^2 to second order and, through the Planck map,
E^2 = E_0^2 + c^2 p^2 per Link; in the identity's whole unit E' = E /
c^2, with c^2 = 1 / 3 in the Beam Law's Links,

    W = E'_0^2 + 3 **p** . **p**   (the 3 is 1 / c^2),   E'_0 = Q S_w M,

the exact square kept on the record and its whole root E' = isqrt(W)
kept by comparisons, E'^2 <= W < (E' + 1)^2 at every interval (series
S, 10 827 lines, GAMEBOARD): W is the step's INVARIANT under the
identity and not a line of the step, as omega^2 - kappa^2 = m^2 is the
walk's invariant; the identity's pace p / E' is a result of the
conversion and not an input (the walk's group velocity to leading
order); the derived identity holds up to corrections of relative order
m^2 beta^2 (m^2 beta^2 / 3 on W, m^2 beta^2 / 6 on E' and r), exact in
the continuum limit. Outside, on a ground detector's record, with E =
E_0 / r and p = E v,

    E^2 - p^2 = E_0^2 (1 - v^2) / r^2,

so E^2 = E_0^2 + p^2 holds Outside if and only if r^2 = 1 - v^2, the
click theorem's one line in the energy's words (SHOWN as the line; MET
under the identity; FAIL on the law, where E = E_0 at every speed and
there is no energy of motion). E_0 = h f_0 = hbar m, a body's rest
energy its rest frequency times the family's quantum, is SHOWN by the
conversion (Compton's relation as the thing compared with; a mass
Outside a mass ratio); E_0 = m_i c^2 with m_i = Q S_w M the inertial
mass of the drive is a UNIT, the load-time identity 3 h n_K = Q S_w d_K
of the identity, not derived and not on the law (the content and the
phase rate untied on main). The momentum: on the law p_law = m_i v / (1
- v) per axis, exact by the wall m_i + abs(p_a) (rung 1), and against
nature's gamma m_i v the ratio p_law / p_nat = sqrt(1 - v^2) / (1 - v)
= k: FAIL at second order on the law; FOLLOWS from the declared square
under the identity (the two verdict words of the sources on one
formula, both stated). Source: the click frame section 7 (1) (b) to
(d); Einstein Outside II.6 and II.7; DERIVATIONS_BEAM 17.6 and 4.5.

### 5.4 The equivalence principle; the accelerated detector; the clock's constant

**Hypotheses:** (W1), (W2), (M); (A1) and (A3) for the accelerated
detector. **The fall independent of the content, exact:** the push p_a(t
+ 1) - p_a(t) = -M_A V_a(t) in the gravity column (Lambda = 1, Lambda the column's declared
bound, the drive's coefficient; p = M_A sum V exactly) and the drive dividing by M_A (the step's divisor scales
with M_A, so the same whole parts and remainders at every abs(p), not
only at abs(p) << Q S_w M_A): the equivalence principle is rung 1 for
bodies (SHOWN; MET: series D3, the held mass four times at r = 24, 138
of 139 common birth ticks at the same Node, DETECTOR); it holds for
bodies and not for rows (the flight blind on main, 5.9); for a bound
body it is a hypothesis with pins (DERIVATIONS_BEAM 21.2 row 44). **The
accelerated detector's count ratio** (Einstein Outside II.9; from
Theorem 1 with no crowd, the ceiling Y receding at g Y / c during the
packet's Y / c intervals):

    k_XY = 1 / (1 - g Y / c^2) = 1 + g Y / c^2 + O((g Y / c^2)^2),

Einstein's elevator redshift as the thing compared with, from (A1)
alone, with the constant 1 / c^2 and no input; rung 2 (first order in
g Y / c^2, the geometry taken at the emission and the arrival);
DETECTOR when read, NOT READ. **The clock in a crowd** (the click
frame section 8; the age wall): a body in a crowd of age moment a_tau
owes a_tau n / d intervals per self-creation, so its rate is 1 / (1 +
k_crowd), k_crowd = a_tau n / d (SHOWN, rung 1; series T's age word
2.6517 at 3 and 4.1500 at 6 Links, DETECTOR); about a point source
k_crowd falls as 1 / r in the shell mean (rung 2, with the ripple; the
count ratio of two lamps at two distances k_crowd(r_1) / k_crowd(r_2) =
r_2 / r_1, READ: series T's 1.907 for the pin 1.909 +- 0.05, DETECTOR, the
continuum's 2.00 outside the pin by the grain); the flat interior of a
shell (series X's k_crowd(2) / k_crowd(4) = 1.0029 for 1.003917 +-
0.02, MET,
DETECTOR, a host-tick reading by the owner's convention). **The
equivalence of the clock's slowing and the fall, one field read twice**
(the click frame section 8 (2) (e); Einstein Outside II.10, II.10a;
Newton from the clicks 1.3): in the static shell mean the flow is the
gradient of the age moment, **a** = -(Q c / tau_L) grad A (**a** the
label flow vector of 2.2; tau_L the flight's intervals per Link, 1 / c
exactly), and the acceleration a = -(c^2 / S_w) grad A; between
two heights Y apart the clock's shift is delta k = (n / d) delta A and
the fall's g Y = (c^2 / S_w) delta A, so

    delta k = (n S_w / d) (g Y / c^2):

nature's form g Y / c^2 times the declared n S_w / d, equal to nature's
if and only if n S_w = d, the pin II.10a (the suspension pair the inverse
of the width: the clock's suspension and the push's width one constant;
CONSISTENT, a condition on the declaration and not a theorem; the
registered worlds at n S_w / d = 16, 2, 256, 1/2 and 1, GAMEBOARD,
inputs, Einstein Outside's correction of the click frame's 2^-16); SHOWN IN FORM, the constant a declared input, the one reading
that would close it (delta k as the ratio of two lamps' count ratios at
two heights against g Y as the second difference of a falling lamp's
arrival Nodes over its ordinals times the height, on one crowd) NOT
MADE. The height is written Y here (h being the action; the Newton
files write it h). It holds for a reader AT REST: the clock's wall
reads what is present at the Node (a count with no velocity term) and
a body's push reads what is met at the crossing of the world lines (a
count with the factor 1 + u / c), so for a moving reader the law's one
field is two (Newton from the clicks section 2). The second order of
the clock: 1 - k + k^2 where nature reads 1 - k - k^2 / 2, a different
law in the strong field, no horizon, below reach at the Earth. Source:
the click frame section 8 (2) (c) and (e), and its table; Einstein
Outside II.9, II.10, II.10a; DERIVATIONS_BEAM 3.3, 5.1, 5.2.

### 5.5 Einstein's step, one sentence (this file's proposal, for the reviewer)

The wording in force is one sentence (the plan's K3; the physics-rule
reader's sentence, in place of the unifier's proposal): **The step
above the board is the image of the Inside step under the conversion
(Newton from the clicks 1.3, :206-207); Einstein's step, as physics
writes it, dp / dt = F with p = gamma m v, E^2 = E_0^2 + c^2 p^2, d tau
/ dt = sqrt(1 - v^2) and the geodesic's first terms (Einstein Outside 3
(a), :511-513), is the thing it is compared with: the image's r-free
lines (the round trip, the composition, the aberration) are Einstein's
exactly from (A1), (A3) and the conversion, and its scaled lines (the
rate r, the one-way Doppler, the length, the energy) are Einstein's if
and only if r^2 = 1 - v^2, the one line the click theorem leaves free;
the rate r, the conversion between the mover's own count and the rest
detector's (Newton from the clicks 1.4 (b), :300-302; Newton on the
side :164-165), is the one factor of the image that the scale needs,
and "Einstein is the step in between" (the owner, record 1044) names
that conversion between the clicks and Newton's form.** The sources'
wordings, verbatim: Einstein Outside :511-513, "Einstein's step: dp /
dt = F with p = gamma m v, E^2 = E_0^2 + c^2 p^2, d tau / dt = sqrt(1 -
v^2), and the geodesic's first terms (the equivalence of the fall, the
redshift g Y / c^2, the deflection 4 G M / (c^2 b))"; NEWTON_FROM_CLICKS
:206-207, "Einstein's step is the IMAGE of the Inside step under this
map"; NEWTON_FROM_CLICKS :300-302, "Einstein's step is the conversion
between the mover's count and the rest detector's, the rate r";
NEWTON_ON_THE_SIDE :164-165, "Einstein's step is the conversion of the
mover's own count to the rest detector's, the rate r; for a moving
reader the one field is two". The image's rows for a body
read by a line of detectors at rest (Einstein Outside section 3 (a)):
the Node after the count, x_L(n + 1) - x_L(n) = the whole part gained by
the drive (0 or 1 per axis); the momentum's change p_a(n + 1) - p_a(n) =
-M <V_a>; the pace <dx / dn> = abs(p_a) / (Q S_w M + abs(p_a)) per axis
in the mean; the clock, the count between self-creations 1 + a_tau n /
d in the mean; each DETECTOR (the births' Nodes and the counts between
them) and each the Inside line read through Theorem 1 at r_L = 1 (rung
1 within one Node and one count). Nothing of Einstein's is put in: only
the Inside step and the map; the geodesic's terms follow at Newton's
first order (5.4) with light's terms absent on the law (5.9).

### 5.6 Newton's form, from the clicks: the second law, the inertia in one form, the velocity term, the shell mean

**The wording in force** (the owner's [record 1044](LOG_2026-09-20.md):
"Newton has to come out of clicks in the algebra, not at low velocity,
because Einstein follows from the clicks; Einstein is a step in
between"; the Boss's word of 2026-09-23 on the plan's K2):
Newton's form is reached from the clicks with no expansion in v / c;
the one limit taken is the shell mean (M), the spatial average over
N(r) Nodes, for the 1 / r of the potential and the 1 / r^2 of the fall;
Newton's classical scale is the value r = 1 of the mover's own count
and the value u / c -> 0 of the click count's term, values the side
arranges and not limits taken in the algebra. The earlier wording, "in
the continuum limit of the image (a) (many self-creations, v << c, the
shell mean of (M))" (Einstein Outside Theorem 4, :570-572, RECOVERED),
is superseded on the v << c clause and kept as its record; the shell
mean it names is the one limit both wordings take, and the paper's
opening, "in a limit under a shell average, Newton's inverse square"
(main.tex:51), already says only that. **Hypotheses:** (A1); (W1) to (W5); (M) where named; the world
file's detectors, lamps and declared integers (the fan, S_w, n / d, the
contents, eta the release per unit of content per direction, the ratio
n / d); no (A2). **(a) The clicks, the primitive.** A detector
is a body with its own count n_D, one accumulator advanced by one per
interval and stretched by the age wall at coefficient 1; a click is the
arrival at D of a packet another detector released, the triple (the
Node, n_D at the arrival, what arrived: the packet's ordinal, its
direction, its content); the ordinal a released row carries is the
emitter's own count at the release, so a lamp on a moving body hands
the body's own count to every rest detector it reaches, and "Nodes
apart over the mover's own counts apart" is a ratio of two click
readings, DETECTOR on both sides; the owner's word of record 1043,
"the information that moves on the GameBoard is the moving detector",
in the file's rendering: the packet in flight IS the moving detector. **(b) The second law, from the clicks.** A
lamp on the moving body releases rows toward a set of rest detectors,
read on the ORDINALS (the body's own count) and not on the line's tick
(GAMEBOARD): each click gives the body's place at the release (the
arrival Node and the flight count converted back, CONVERSION) against
the ordinal, a table x(n), DETECTOR; Newton's second law from the
clicks is its second difference,

    x(n + 1) - 2 x(n) + x(n - 1)   (Nodes per own count squared),   the acceleration read after a detector,

and the push rule p_a(t + 1) - p_a(t) = -M_A V_a(t) is the DECLARATION
that maps it to the record; the momentum's value on the record is never
an input (GAMEBOARD); Newton's F = d**p** / dt is the comparison, the
law's the same form with the own count in place of t, its scale
against the tick the rate r; rung 1, no mean. **(c) The inertia in one
form, exact at every speed.** Per axis the drive's accumulator gains
abs(p_a) per self-creation against the wall m_i + abs(p_a), one Link at
most, so the body hops one Node per (m_i + abs(p_a)) / abs(p_a) counts
in the mean, a hop's own count and then m_i / abs(p_a) counts of rest;
read on the clicks,

    abs(p_a) = m_i x (Nodes hopped) / (counts at rest between hops)   (exact in the mean, rung 1),

Newton's **p** = m_i **u** EXACTLY with **u** the Nodes apart over the
counts apart of a count that advances in the resting intervals and not
in the hop's, m_i = Q S_w M the declared content times the width and Q,
and **p** defined from the clicks by this identity; against the rest
detector's count the same identity reads abs(p_a) = m_i v_a / (1 -
v_a), the law's dispersion. So the three forms of the inertia are ONE
form, differing only by the rate r of the mover's own count against the
tick:

| The form | r | abs(p) against the tick's v | Where it stands |
| --- | --- | --- | --- |
| Newton's | 1 | m_i v | the comparison, never an input |
| Einstein's | sqrt(1 - v^2 / c^2) | m_i v gamma | the click theorem's one line k_AB = k_BA; covariant-readings-v1's declared square |
| the drive as built | 1 - v (the count stopping in the hop's interval) | m_i v / (1 - v) | the law, rung 1, exact by the wall m_i + abs(p_a) |

The law carries two rates for one record, the clock's 1 (in no crowd)
and the drive's 1 - v, and it is NOT SHOWN that they are one (the
click frame section 0, part (4): "the cost gives r = 1 - beta or 1";
the plan's K4: r = 1
the clock in no crowd, 1 / (1 + k_crowd) the clock in a crowd, 1 - v
the drive's resident count, three quantities under one letter, named
apart here). Under form B (decided, not built) the same identity holds
with abs(**p**)_1 in place of abs(p_a). **(d) The velocity term (1 + u
/ c) is the clicks' own.** A detector hopping at v toward a stream of
rows at c meets E(tau) = (1 + s v / c) tau + O(1) rows in tau intervals,
the O(1) one boundary row, EXACTLY over whole Links of its path (128 +
55 = 183 toward and 128 - 55 = 73 away in 128 intervals at k = 4,
against 128 at rest, COMPUTATION from (A1) and the flight table;
`tests/test_crossing.py` pins 183 exactly and 74 away, the one extra
the row co-located with the reader, the O(1) named; after a detector
it is the Doppler, row 4b's z); so the term is produced by the click algebra for every count
that is a click and added by no rule; which counts of the law are such
counts is a declaration (BEAM_LAW note 48: the threshold, the window,
the click and the push read the same `met`), so a BODY's push counts
crossings and carries the term, d p_r / dt = -(1 + u / c) A / r in the
ring mean, while a ROW's push and every wall count what is present at
the Node, a count with no term at first order; against nature, Newton's
gravity as written has no term of first order in u / c (the comparison
and nothing more). **(e) The 1 / r and the 1 / r^2 in the shell mean;
G; Kepler.** On one beam the flow is the same at every Node and the age
moment grows with the age r / c the row carries (1 / r^0 on a beam); the
1 / r^2 of the presence and the 1 / r of the age moment exist per Node
only in the mean over a shell of N(r) Nodes, a mean of GAMEBOARD
quantities, NOT FROM THE CLICKS as a mean; its click readings: the count
ratio of two lamps at two distances, k_crowd(r_1) / k_crowd(r_2) = r_2
/ r_1, READ (series T, DETECTOR, 5.4); the second difference of (b) at two
distances, whose ratio is (r_2 / r_1)^2 in space and r_2 / r_1 on the
plane, NOT READ. In the shell mean, marked so,

    a = -G M_B / r^2,   G = K (n / d) / (4 pi S_w)   (space; on the plane a = -G' M_B / r, G' = K (n / d) / (2 pi S_w)),

G the source's release rate per unit of content per direction n / d,
times the number of directions K, over 4 pi and the width (the Newton
files and Einstein Outside write the ratio eta, the same declared
number: G = K eta / (4 pi S_w)); retarded at c; the value of G a
declared input, NEITHER Outside (no detector reading of G is
registered). Kepler on the plane: T = 2 pi r (S_w + n) / n with the
drive's exact pace, T proportional to r the 1 / r force's scale
symmetry (no v << c in the period's form), T(24) / T(12) = 2 (series
D3's 1.997 inside its bracket 2.00 +- 0.18, read as history, DETECTOR
clicks on the host's tick: the registered D3 before the generic entry,
the click frame :1163; after it 1.677 and 1.512, chapter 6 row 14; the
ratio on the line's tick GAMEBOARD, mode A; its click reading the recurrence of the
arrival Nodes on the ORDINALS of the orbiting lamp, NOT READ); in space
T^2 proportional to r^3, the exponent NOT READ. **(f) The third law at
rest.** For a paid message the label leaves its emitter at birth (the
recoil) and enters its reader at the click, so the third law holds
message by message (rung 1); for a free message the release costs no
recoil and the third law is a symmetry between two readers, M_A **a**_B
= M_B **a**_A (**a** the flow each reads), exact only while both read the same number of each
other's messages; at rest the two counts are equal by the crossing
rule; in motion they differ by (1 + u_A / c) against (1 + u_B / c), so
the free force's third law is a rest theorem, NOT SHOWN in motion; the
register's 1.0000 is a GAMEBOARD reading of the sources' own records,
evidence and not an input. **(g) The prescription for the side, by
reference** ([Newton on the side](designs/newton_clicks/NEWTON_ON_THE_SIDE.md)
sections 3 and 4): the moving detector with mass, a massive row on the
whole rung k of the ladder (E'_D = k p exactly; k = 19 with M_row = 21
and p = 71 at S_w = 1: E'_D = isqrt(1344^2 + 3 x 71^2) = 1349 = 19 x 71,
COMPUTATION), so that its pace's reading is exact over any window; the
reading that brings Newton, (T_mass - T_control) / T_control = k_a(b)
(b / L) ln(4 r_1 r_2 / b^2) x [c_f - (1 - v^2 / c^2) (1 + gamma_PPN v^2
/ c^2) (c / v)^2], every factor a ratio of counts, the mark of Newton's
form the (c / v)^2 (60 at k = 19 and c_f = 2, COMPUTATION); Kepler on
the ordinals T_1(24) / T_1(12) = 2.00 +- 0.20; the owner's open line,
whether a read at a body is a click, which record 1139 (c) restates as
the one question left, which count a body's push takes, arrivals or
crossings, the light row's lever-arm pin deciding (chapter 6.4).
Source: [Newton from the clicks](designs/newton_clicks/NEWTON_FROM_CLICKS.md)
sections 1 to 3, 5 and 6; Newton on the side sections 0 to 4; the
click frame section 8; DERIVATIONS_BEAM 3.3, 9.1 (I5), 17.2.

### 5.7 Light Outside, one line per formula

**Hypotheses:** (A1), (A3), (L1) to (L9), the conversion; each row's
own. The pace of light: chapter 4.2 (SHOWN; MET, series Q and T; FAIL
against nature's isotropy bound at the grain, row 5a, a BOUND on Q).
E = h f at a click: the content of one click E_B = h_q s = h f_A (h_q
the family's quantum, the action per unit born; s the lamp's turn),
DECLARED at the release and RECOVERED at the click as the content
carried whole (rung 1); the frequency B counts f_B = f_A k_AB; lambda_B
= c_D N d / n = h / p FOLLOWS under the calibration h_A = h_q N, read
Outside only as a fringe spacing; E = h f_flight would need the
declaration s = n / d, met by no registered world (MET at the emitter
and at Q's clicks; row 11a's chain). The intensity of a source: the sum
over a shell of the click rates is q K per count exactly (every row
leaves the shell once), the mean click rate per detector q K / N(r) ->
q K / (4 pi r^2) in the shell mean (rung 2), 1 / r^0 on a beam (rung 1);
the 1 / r^2 at two radii after a detector NOT MADE. The Doppler: the
moving detector 1 + z = 1 / (1 -+ v), the moving lamp 1 + z = 1 +- v,
the transverse 1 exactly, the round trip (1 + v) / (1 - v) r-free
(SHOWN, rung 1; matches nature at first order; the two one-way forms
differ at second order by 1 - v^2 where nature has one form, FAIL on
the law, row 4b). The aberration of a moving detector tan alpha = v /
c_D (alpha here the aberration angle) by the passage of clicks, 0 by the click's face (SHOWN at first
order; NOT READ). The two-slit fringes: the count at the pixel y over
W births,

    C(y) / W = (2 + 2 cos(2 pi (L_1(y) - L_2(y)) / lambda)) / Z + O(1 / (2 N)) + O(1 / W),   lambda = c N d / n Links,

bright where L_1 - L_2 = +- j lambda (Z the record's total, the
formula's normaliser; lambda here the wavelength in Links), Young's
lambda L_s / s paraxial (L_s the slit-to-screen distance and s the
slit spacing, the letter D being the direction)
(SHOWN, rung 2 on the fan, Born rung 1 within 1 / (2 N); the bands'
centres 23.5 apart for 23.3, MET; the visibility 0.966 against 0.98,
FAIL by the fan's grain, row 2a). The click's indivisibility and Malus:
chapter 4.12. The redshift through a crowd: one count of one detector,
three factors,

    1 + z_d = k_AB = (1 + k_crowd,A) (1 + v / c) r_B = r_B (1 + z),   r_B = 1 / (1 + k_crowd,B);   at rest   1 + z_d = (1 + k_crowd,A) / (1 + k_crowd,B) = 1 + k_crowd,A - k_crowd,B + O(k_crowd^2),

the potential's 1 / r at first order (rung 1 in k, rung 2 in r; MET:
series G, G2, T and X; the second order the law's own, 5.4); the row's
phase is never stretched (a stretched phase per age would redshift
light in transit). Bell at two places: chapter 4.10. Reflection and
refraction: NEITHER (a row meets no surface; a mirror is the
apparatus's declared table; no crowd slows or bends a row on main). The
apparent acceleration (the dark energy note): for a lamp thrown at v
and read after the flight time tau,

    1 + z_d(tau) = r_B (1 + k_crowd,A(tau)) (1 + v(tau) / c) = g(tau) (1 + z_throw(tau)),   g(tau) = (1 + k_crowd,A(tau)) / (1 + k_crowd,B),

and with g(x) = 1 + g_1 x + g_2 x^2 + ..., x = H tau, H the throw's
rate (Hubble's constant as the thing compared with), the deceleration
parameter a reader fits is q_eff = 2 [(1 + g_1 + g_2) / (1 + g_1)^2 - 1],
q_eff = -2 g_1 / (1 + g_1) when g_2 = 0: any stretch of the emitters'
clocks relative to the detector's growing linearly with the flight time
reads as an acceleration, a property of the conversion (SHOWN IN FORM,
rung 2); the size g_1 = 0.36 that nature's -0.53 needs is an INPUT the
law's own crowd does not supply, and its Seeliger history gives the
wrong sign (row 3); by the brightness the law has one factor of 1 + z
where nature's flux has two, d_L = D sqrt(1 + z_d), q_eff (by
brightness) = 2 / (1 + g_1), FAIL for every g_1 (row 11a). The verdict
line: LIGHT OUTSIDE FROM THE BOARD: PARTLY. Source: Light Outside II.1
to II.12 and its verdict table; [the dark energy note](designs/light_outside/DARK_ENERGY.md)
sections 2 to 5.

### 5.8 The atom's congruences

**Hypotheses:** the law's integers alone (the action row per axis, the
push of the charge column, the drive, the turn by momentum under the
world key `action`); the shell mean (M) for the ladder; the
inverse-square limit for the reach theorem. **The closure, exact, no
grain.** The engine keeps one action row per axis, A_a the exact sum of
abs(p_a) N over the Links counted on that axis since the birth, the
phase the sum of the three per-axis whole parts floor(A_a / h) mod N
plus the birth phase; over one return (the body's arrival at a Node it
left one loop earlier with the same momentum vector) the action row of
the axis a gains Delta A_a = N x (the sum over the Links stepped on the
axis a of abs(p_a)) (an integer per axis, GAMEBOARD), and the loop
CLOSES ON ITS OWN PHASE for every starting state exactly when

    Delta A_a = 0 mod h on each axis a,   and   (Delta A_x + Delta A_y + Delta A_z) / h = j N,   j whole

(three congruences and one sum; the closure not a condition on the
Link count L but on the momentum-weighted L1 length sum abs(p_axis)
over those Links). A row's closure (tau n_phi = j d_phi N) is the light
clock of the click frame and not the atom. In the limit of small Links
on a loop where the step follows the momentum the L1 sum is the line
integral of **p** along the loop, so the closure reads the integral of
**p** . d**l** = j h, Bohr's quantization of the action as the thing it
becomes in the limit, compared with and not put in (the digital
circle's sum 2.041, 2.011, 2.003, 2.000 x pi p r at r = 8, 16, 64, 256,
GAMEBOARD). **The ladder, in the shell mean (rung 2).** For any closed
loop of the inverse-square limit the line integral of **p** is 2 pi
sqrt(kappa m_i a), kappa here the force constant of the limit and a
the loop's semi-major axis, so the closure fixes a
and not the shape,

    a_j = j^2 h^2 / (4 pi^2 kappa m_i),   a_j / a_i = (j / i)^2   exactly in the limit;   T_j / T_i = (j / i)^3,

with m_i = Q S_w M and kappa = 16 M Q E_0 / 10 on the register's charges
(DERIVATIONS_BEAM 7.2: r_j = j^2 h^2 / (4 pi^2 Q S_w M x (M k)), reached
in form). **What a detector reads:** with a passive detector at every
Node, three DETECTOR readings at rest in no crowd (r_D = 1): the
circles per return j (the sum over one return of the phase increments
of successive rows at one detector Node, divided by N, a whole number on
a closed loop and a fraction on an open one; series H's fractions 0.234
and 0.188 on the faces' clicks), the period T (the count at the
proton's Node between two clicks of rows from the same axis), and the
loop's Nodes; so a_j / a_i = (j / i)^2 and T_j / T_i = (j / i)^3 are a
ratio of two counts squared and cubed, both r-free, no root and no
float; the cube of the circle ratio against the period ratio the pin a
run would meet or miss. **The lattice's departure, stated:** the
register's fan of 2616 directions has its ring flux falling as r^-1.83
(GAMEBOARD), so the ladder's exponent on the lattice is 2 / (3 - k) =
1.709 at k = 1.83, the fan's table and not (j / i)^2: MET IN FORM in the
shell mean, FAIL IN FORM on the lattice as declared (the fan the
apparatus's declaration); the paper calls the 1 / j^2 ladder a
conjecture: the three status words of the sources are one status
line, the ladder holding in the shell mean, failing on the lattice's
fan, not established against nature. **The click that moves a row
between the two radii, exact in the declared integers:** a paid row of
amount w and content per unit c arriving at the electron's Node under
`measure` ends, its weight the bilinear form once, and p' = p + w c
**u**_d, M' = M + w c (a free row moves no label; the recoil of the
electron's own paid release the same with the sign reversed); the count
between two hops on the axis changes by Delta k = Q S_w M x (1 /
abs(p'_a) - 1 / abs(p_a)), an exact rational of the declared integers
(7.6186 counts per Link at the register's r = 12, COMPUTATION).
**Theorem (the reach of one click), in the inverse-square limit:** a
body on the closed circle j is carried by one click of any label to a
loop of semi-major axis a' >= r_j / 2, so the closed loop i is one click
away from the closed circle j only if 2 i^2 >= j^2; the pairs one click
reaches from a circle j <= 6 are (4, 3), (5, 4), (6, 5) and none
below 3 (from j = 7 on, (7, 5), (7, 6), (8, 6), ... by the same
condition); Balmer's i = 2 from the register's circle r = 12 (j = 4.01; 2 x 2^2 =
8 < 16) and Lyman's i = 1 from any j >= 2 are not reachable by one
click. **A release unbinds:**
dE / dM < 0, losing content raises the loop's constant and the body
unbinds (charge is per unit of content). **What no rule does:** the row
that carries the body between two closed loops is selected by nothing;
the law has one frequency per family (the declared pair) and not one
per transition; the give of a bound set is once per body and declared
(binding-v1). The comparison, afterwards: Bohr's condition MET IN FORM
in the limit; Bohr's radii MET IN FORM in the shell mean, FAIL IN FORM
on the lattice; Kepler's third law on the closed loops MET IN FORM in
the limit, NOT READ; Balmer's ratio nu(H beta) / nu(H alpha) = 27 / 20 = 1.35 NOT
READ, and FAIL IN FORM for a one-click atom; the binding as a
difference of two levels FAIL (series N's 2.0 against 12.72, DETECTOR);
DERIVATIONS_BEAM 7.2: the levels and the lines NOT REACHED (no energy
of a body, no transition; a detector reads the orbital frequency nu_j
proportional to 1 / j^3, Bohr's correspondence limit); 26.5 reads the
level's energy as an identity of readings, E_j = K + q A (K the kinetic
reading, q A the coupling times the age moment), on a circle under the
inverse square E_j = -q A / 2 ~ -1 / j^2 IN FORM with 7.2's r_j ~ j^2,
the energy read and not given by a rule, the transition NOT REACHED,
level-release-v1 the rule it would need (:7906-7925). **The verdict:**
NEEDS A NEW RULE; the atom as a set of levels with one line per pair is
NOT IN THE LAW; the one primitive it would need, `atom-give-v1` (a give
at the closure with its amount read off the action rows), is named and
not written into the law (chapter 6, row 6). Source: [the atom's
algebra](designs/atom_algebra/ALGEBRA.md) sections 1 to 4 and 6;
DERIVATIONS_BEAM 7.2 and 26.5.

### 5.9 The walk past a mass: the step rule, the bending, the delay

**Hypotheses:** the law's flight table, hop rule, one wall function and
count primitive; the world key `optical` (optical-v1: the flight in the
age wall's set at c_f = 1 + gamma_PPN, gamma_PPN an input, 0 by
default) and, under `flow_link` (flow-link-v1), the flow label **f**_D
in place of **u**_D; the shell mean (M) and the straight-path integral
(r_1, r_2 >> b, alpha << 1) for the closed forms; the pin n S_w = d.
**On the law as built** the flight is not in the age wall's set (the
set is the body's clock alone), so a row's path is the Bresenham line of
its direction and its arrival count L tau_L within 1 / T_D whether or
not a crowd lies on the path: the delay 0 and the deflection 0, rung 1,
exact by the declared set (series K: 0.000 pixel, DETECTOR; FAIL by the
whole of both effects against 1.75 arcseconds and the Shapiro delay);
this is the declaration P9, not a theorem of the six verbs (chapter
4.14). **The step rule under the key, three verbs, all integers** (the
state of a row of light: its Node, its direction D, the count `made`,
the residue s of the flight's accumulator, the age; the push
accumulator **w**, the error accumulator **c**; **p** its momentum label
and **a** the arrival flow, all vectors bold lowercase here where the
step algebra writes them uppercase):

    the walk:   A = the crowd's age moment at the row's Node;  (r_0, w_0) = (2 S_1 Q, 2 T_D) on a row never pushed, else (2 S_1(**p**) Q, 2 T(**p**)), the walk's rate and wall;  s += r_0 d;  if s >= w_0 (d + c_f n A): s -= w_0 (d + c_f n A), the Link step **l** = line_D[made mod S_1] (the step algebra writes it h), **c** += **l** x **p** (a pushed row), made += 1, the Node moves by **l**
    the push:   at a free Node, **a** = the arrival flow there;  **w** -= n x weight_D x **a**;  s = s x S_1(**p**') // S_1(**p**)
    the label:  **p** = Q d **u**_D + **w**; among D and its neighbours the next Link **l** = line_D'[made mod S_1(D')] with **l** . **p** > 0 that keeps abs(**c** + **l** x **p**)^2 smallest; if D' differs, **w** += Q d (**u**_D - **u**_D'), D = D'

with the crowd from the same flight rule, A(r) = scale x sum over the
lines D through r of the sum of the ages present and **a**(r) = scale x
sum of **u**_D (the weighted **f**_D under flow-link-v1, the integer
vector nearest Q D / S_1), constant in time once the oldest row that
reaches r has been born; the engine walks it as the algebra does, every
shift within 0.03 pixel of the register (the grain 0.2) and every delay
within 0.2 interval (the step algebra's calibration, section 5). **Two verbs apart:**
the bending is the push's alone, the delay the wall's alone plus the
bent path's Links; the wall bends nothing by itself; their coupling is
the dwell, the deflection carrying the factor (1 + c_f k_crowd) of the
stretched dwell. **The closed forms, SHOWN IN FORM (rung 2):** the
wall's delay, with the flight in the set, delta t_wall = c_f (1 / v) x
sum over the path's Links of k_a(x), and in the shell mean

    delta t = c_f (n S_w / d) (G M_B / (c^2 v)) ln(4 r_1 r_2 / b^2),   the light row's c_f (n S_w / d) (G M_B / c^3) ln(4 r_1 r_2 / b^2) at v = c,

Shapiro's form as the thing compared with, the coefficient c_f (n S_w /
d) in place of nature's 1 + gamma_PPN (Einstein Outside II.11 reaches
the same by the wall's stretch summed along the path); the bending, by
the push on the row,

    alpha = 2 k_a(b) (c^2 / v^2) (1 + gamma_PPN v^2 / c^2) = 2 (n S_w / d) (G M_B / (b v^2)) (1 + gamma_PPN v^2 / c^2),   k_a(b) = (n S_w / d) G M_B / (b c^2)   (alpha here the deflection angle; k_a(b) the crowd's stretch k_crowd read at the impact distance b),

for the light row 2 c_f (n S_w / d) G M_B / (c^2 b), Einstein's 2 (1 +
gamma_PPN) G M / (c^2 b) and 4 G M / (c^2 b) at gamma_PPN = 1 as the
thing compared with (Einstein Outside II.11 reaches the same value by
Fermat's principle on the delay field; the two mechanisms, the push on
the row and the wavefront's differential delay, agree at v = c and c_f
= 1 + gamma_PPN; the meeting-v1 form theta = q delta_theta / (4 N b c)
of DERIVATIONS_BEAM 5.4 is an older key's, reached in form with a
grain constant); for the massive row at v << c, 2 (n S_w / d) G M_B / (b
v^2), Newton's 2 G M / (b v^2) as the thing compared with; the row's
constant of the fall G_row = (n S_w / d) (1 - v^2 / c^2) (1 + gamma_PPN
v^2 / c^2) G, a held body's G at v << c if and only if n S_w = d; the
arrival earlier by the push's advance, so the massive row's count
against the control carries two terms of opposite sign, delta t = (n
S_w / d) G M_B ln(4 r_1 r_2 / b^2) x [c_f / (c^2 v) - (1 - v^2 / c^2)
(1 + gamma_PPN v^2 / c^2) / v^3], Shapiro's delay at v = c and Newton's
advance at v << c as the two things compared with and nothing between
compared. Nothing is derived: the 2 of c_f is an input; the one click
reading every number hangs on is k_a(b), the count ratio of a lamp at
rest at b against a control (DETECTOR when read; the design's 0.0445
from the board's age moment, GAMEBOARD, row 13's audit). **The
numbers, by kind:** on the registered geometry the ring of starts
reads C_ring = alpha b c^2 / (G M) = 3.652 / 3.821 / 3.918 at b = 6 / 3
/ 8 at gamma_PPN = 1 under flow-link-v1 against the continuum's 4, the
expected 2 c_f x 0.990 x L / sqrt(L^2 + b^2) (the shells' 0.990 and the
finite path's factor), within one to three grains of the ring
(COMPUTATION, the step algebra's simulation of the board, not a run;
the law as built 5.12 / 5.44 / 5.86, the push's constant F_L1 = 1.421
times the clock's (F_L1 the fan's L1 factor, the mean of S_1 / abs(D)_2
over its lines), which flow-link-v1 makes one, 0.990 against 0.993);
the in-plane coefficient 11.69 at b = 6 (14.71 as built) is the plane's
comb and no constant; the ring's mean radial shift 0.731 against 0.731
+- 0.025 at gamma_PPN = 1 (DETECTOR, record 995 of the log); the verdicts CANNOT CLOSE on the
registered geometry as built, CLOSES TO 2 c_f on the one constant
under flow-link-v1, and NOT COMPARED with nature (gamma_PPN an input,
row 13). Source: [the step algebra](designs/light_bending/STEP_ALGEBRA.md)
sections 4, 7, 9 and 10; [the flow weight](designs/flow_weight/ALGEBRA.md)
sections 0 to 3; Newton from the clicks section 3; Einstein Outside
II.11; DERIVATIONS_BEAM 5.4.

### 5.10 The relations reached only under an identity beside the law

One line each, under their identities, so that chapter 6 can name
them; none is the law. **covariant-readings-v1** (the world key
`covariant_readings`; DERIVATIONS_BEAM 17.6 and 17.7): the declared
square W = E'_0^2 + 3 **p** . **p** kept on the record, E' its whole
root by comparisons, the rate r = E'_0 / E' exact on the identity's
integers in no crowd, the gate E'_0 / E' = 1 / gamma in its domain gamma
<= 2 (the enumeration's domain abs(**p**)_1 <= E'_0), and the root-free gate the owner named,
the n-th self-creation allowed when t^2 m^2 >= n^2 W, a comparison of
two integer products (verbs (T), (B), (D)), t / n >= sqrt(W) / m =
gamma: gate (A), the owner's as stated, T'_n = ceil(n sqrt(W) / m);
gate (B), the same comparison at the whole-root gate's origin, strict,
T''_n = 1 + floor((n - 1) sqrt(W) / m), which equals the whole-root
gate's T_n = 1 + floor((n - 1) E' / m) unless a multiple of m lies in
between; (B) later than the whole-root gate by 0 or 1 for n <= m + 1,
equal to it when W is a perfect square (p = 0, and gamma = 2 exactly,
where both give T_n = 2 n - 1); (A) later than the whole-root gate by 0
at p = 0, exactly 1 at gamma = 2, at most 3 on the domain (attained at
m = 16, 64, 100 and 128 for n near m); (A) >= (B) always, since
ceil(n x) >= 1 + floor((n - 1) x) for x >= 1, and by the mathematics
reader's enumeration over every W of the domain at m = 16 and 64, n <=
m + 1 (COMPUTATION, his read of 2026-09-23, record 1167 of
docs/LOG_2026-09-20.md), (A) is later than (B) by 0 to 2, exactly 1 at
gamma = 2 where T'_n = 2 n and T''_n = T_n = 2 n - 1; sqrt(W) is never
formed, it only names the value the comparison decides; the exact root-free form with one division is T_n =
min {t : ceil(t m / (n - 1))^2 > W} (DERIVATIONS_BEAM 17.7,
:5196-5204); MET in its
domain (series S: the muon's products' face clicks at 392, 369 and
345, DERIVATIONS_BEAM 18.1, :5379-5380; z = 0.3674 for 0.369 +- 0.003,
EXPERIMENTS.md and chapter 6 row 4b, DETECTOR; the self-creations 70
and 124, GAMEBOARD), beside the law's FAIL rows 4a and 4b; one sixth
of the perihelion's advance FOLLOWS from the declared square, the
field's five sixths NEITHER (Einstein Outside II.12, :1410-1413, and
its verdict table; DERIVATIONS_BEAM 21.4 row E12). **The seventh verb** (lorentz-v1; Highlights 5.4, the
Lorentz A and B line: "a root at a declared grain slowing the counter
by gamma and contracting the bond ... built beside the law under its
own identity as a comparison hypothesis"; not admitted, Highlights
5.4's form B line, the root-free gate checked instead of admitting a
seventh verb): a root of the state at run time slowing a body's own
counter by gamma and contracting its bond by 1 / gamma; fails the
vector test (record 202); the law's own prediction, that a
body's own counter does not slow with speed, stands as a falsifiable
row (4a) and fails against the muon in flight. **optical-v1 and
flow-link-v1:** 5.9. **massive-rows-v1:** a paid family declared
`massive`, its rows flying at the pace abs(**p**) / E' of the rest energy
E'_0 = Q S_w M and turning abs(p_a) N / h phase steps at every axis Link
over the world's action h; the nu family's quantum 1 under it is the
declaration rows 8b and 8c wait on. **atom-give-v1, decay-by-crowd-v1,
expansion-v1:** named rules outside the law, chapter 6.

---

## 6. What each FAIL row lacks, by the algebra

HISTORY UNDER THE ONE ALGEBRA, as chapter 5's note says: the crowd of these
rows is the ray law's; chapter 9 does not restate them.

The FAIL Rows Algebraist's reading ([the FAIL rows file](designs/fail_rows/WHAT_IS_MISSING.md),
merged to main by PR #964, read AE folded; the owner's words of records
1102 to 1104 and 1114: understand why the experiments that passed passed
and what was missing in the ones that failed, by what the algebra
derives to physics; make sure nothing is measured inside the board),
stated here once, one line per row; the per-row sections of that file
are the record.

### 6.1 The four words, and the seven generic modes in the clicks

**The four words** (the Boss's order, verbatim from the file). A
READING: a click not yet made, named, with its side arrangement and its
pins by the algebra before any run. A DECLARATION: a world integer or a
world key, named, with what each option gives. A RULE: nothing in the
six verbs and the declared tables gives the row's number; what a rule
would have to do is stated under its own identity, outside the law,
with the three tests (generic, vector, local) and whether it can pass
them; a RULE that cannot pass the three tests is still written as a
RULE, so that the Boss sees what nature asks of the law, and the row
then stays FAIL under the law as it stands. NOTHING: no reading, no declaration
and no rule of any kind, inside or outside the six verbs, moves the
row: it is the law's own exact result and nature refutes the law there.
The counts: READING 1 (row 14); DECLARATION 6 (rows 2a, 4a, 4b, 8b, 8c,
13); RULE 8 (rows 1c, 3, 5b, 6, 7b, 8a, 11a, 11c); NOTHING 1 (row 1b).
Sixteen rows: the twelve FAIL rows of the paper's confrontation table
and the four that fail by their pins and stand outside the table (4a,
5b, 11a, 11c; record 1102).

**The seven modes** (the owner: "everything is read from clicks, so if
you understood something now, you understood a generic problem in the
clicks"), each one generic thing that goes wrong between a row and its
click and one generic fix in the clicks: **A**, a GameBoard quantity
taken as the reading (a period on the host's tick, a presence mean
over a shell, an arrival tick, a body's own record) where a detector's
own count is the click; the fix the detector's own count under
`clock_stamp` (on main), the count ratio at two distances, the face
click. **B**, a read counted as a click or a click counted as a read
(the push taken at a body; the term 1 + u / c put where a click count
does or does not have it); the fix the owner's word on which count the
push takes, and the body a detector with mass. **C**, one record with
two rates (the drive's 1 - v and the clock's 1 / (1 + k_crowd); the
click theorem's missing line, r = 1 as the mover's own count); the fix
the one rate shown or refuted by clicks on the k-ladder, the pace a
ratio of counts. **D**, the click reads the row's birth content and not
the row's rate at the arrival (E = h f absent at the click: the content
per click fixed in flight); the fix the row's phase turning per Link
(massive-rows-v1's turn, abs(p_a) N / h steps over the action h) and
the click reading the phase steps per its own count. **E**, a
transformation of a body fired at a declared count of its own clock, or
declared once per body, and not at a met row (the `become` at a count,
the give once per body); the fix the body a detector, the transformation
a click of a row met. **F**, the click's grain (the fan's width, the
wheel, the lattice's scale) where the comparison is the continuum's
limit; no fix in the clicks, the grain the declaration's and the limit
computed. **G**, the click's order (the wheel a counter, the outcome
order deterministic); no fix in the clicks (a draw is not a click). F
and G are the residue where the clicks are right and a declaration's
grain or a theorem is what nature refutes.

### 6.2 One line per row: the pinned reading and its kind, what the algebra gives exactly, the one word, the modes, and whether anything was measured inside the board

| Row | The pinned reading, its kind; nature | What the algebra gives exactly | The one word | The modes; inside the board |
| --- | --- | --- | --- | --- |
| 1b the phase-form window | S = 2 exactly (DETECTOR, the counters' clicks); nature 2.42 +- 0.20 | SHOWN: the local bound is an identity of the window's form at any count (chapter 4.10) | NOTHING: Bell's bound is a theorem of every local read-out; the law's answer is row 1a's one gather (2.75, DETECTOR); 1b stays as the control of what a local read gives | none; NO |
| 1c the order channel | 15 / 16 under a = 0 and -1 / 16 under the cycle, the serial correlation at lag 1 (DETECTOR); nature 0 | SHOWN: the click a function of (a, b, u) alone, the wheel a counter; the statistic exact at every start | RULE: a wheel that is not a counter; a draw fails the vector test (no draw at a Node); a declared permutation table of the wheel (verb (P)) passes the three tests but reaches 0 only as a fit at one count and one setting sequence; the claim kept to the counts | G; NO |
| 2a the two-slit visibility | 0.966 in the clicks (DETECTOR); the pin 0.9659 (COMPUTATION, met bit for bit); nature 0.98 (a Mach-Zehnder source), 0.94 (a biprism, unverified) | SHOWN: the counts per Node bit for bit from the fan, the weights and the wheel; the ideal 1 the limit of every direction; the shortfall the digital lines' landings | DECLARATION: the fan's width P and the grain of the slits' world; the options 0.94, 0.97, 0.96 at P = 32, 48, 64 (COMPUTATION) do not reach 0.98; NOT COMPARED against a two-slit source until its figure is verified | F; NO |
| 3 the deceleration | q = -0.108 registered, -0.104 at head (DETECTOR, the pointer's z per tick, that tick GAMEBOARD); nature -0.53 +- 0.01 | SHOWN: the coasting throw gives Milne's q = 0 exactly; SHOWN IN FORM: q_eff = -2 g_1 / (1 + g_1) from any linear stretch of the emitters' clocks (chapter 5.7); NOT SHOWN: the size g_1 = 0.36 and its sign from the law's own crowd | RULE: a term that makes the emitters' count stretch grow with the flight time by the law's own crowd, at the size 0.36 per Hubble length; the law's own crowd history gives the wrong sign; a declared gradient a fit | A and C; YES (the tick of an open-face detector as the time base) |
| 4a the unslowed clock | the muon's `become` at 64 at every speed (GAMEBOARD, a body's own record; the products' face clicks DETECTOR); the ratio 1 against nature's 29.33 | SHOWN: on the law r_D = 1 at every speed, the hop costing the clock nothing; SHOWN IN FORM under covariant-readings-v1: r = 1 / gamma exact on the identity's integers within gamma <= 2; NOT SHOWN: r read at the ground through a mover's own records | DECLARATION: the key `covariant_readings` (one rate for the drive and the clock of one record), and the lifting of its domain cap by form B; off, FAIL by 29.33; on, gamma's form within the domain; the reading that decides from the clicks alone: k_AB, the missing direction | C, audited A; YES (the `become` line, a body's own record) |
| 4b the moving lamp's redshift | z = 0.2636 registered, 0.2647 at head at beta = 0.2674 (DETECTOR; the tick GAMEBOARD; the detector's own pulse-and-return clock NOT READ); nature 0.315; under the key 0.3674 for 0.369 +- 0.003 (DETECTOR, series S) | SHOWN: 1 + z = 1 + v exactly, the count of what a rest detector meets (the click theorem's k_BA at r = 1); the two one-way factors apart by 1 - v^2 on the law; SHOWN IN FORM: gamma (1 + beta) under the identity | DECLARATION: the same key as 4a; off, 1 + v, seventeen grains below; on, the pin met; the rest detector in no crowd has r_B = 1 exactly, so the NOT READ clock adds nothing here | C, audited A; YES (the tick as the time base) |
| 5b the arms' anisotropy | the round trips gamma^2 along and gamma across, 1.375 and 1.140 at beta = 0.4297 on the flight table (COMPUTATION, a pin; not run); nature's null at beta^2 / 2 = 5 x 10^-9 | SHOWN: the one-way pace relative to a mover c -+ v, the bond clock anisotropic under the law and the identity alike; NOT SHOWN: any object that contracts (the bond a whole Link) | RULE: a contraction of a moving body's extent by 1 / gamma along its motion; it needs a root of the state at run time (the seventh verb), so it fails the vector test; not reachable inside the six verbs | A and C; YES, wholly (no detector: the round trips computed on the flight table) |
| 6 the atom's loop opening | the electron escapes at 3407 intervals (DETECTOR, series H); under `centred_step` the loop stays, C1 PASS, C2 and C3 FAIL as declared (DETECTOR); no line read; nature Balmer's 27 / 20 | SHOWN: a closed loop is an integer congruence of the action row; the one-click reach 2 i^2 >= j^2 and that a release unbinds (chapter 5.8); SHOWN IN FORM: the ladder (j / i)^2 and (j / i)^3 in the shell mean, 27 / 20 under the virial form in the limit; NOT SHOWN: the transition, any rule that selects the row | RULE: atom-give-v1 / atom-level-v1, the give at the closure with its amount read off the action rows, under its own identity; generic, vector and local PASS in the mathematician's judgement, the reviewer's read decides; no lattice we can run holds the scale, so the row stays FAIL by any run and the ladder a conjecture | F and E; YES in part (the loop's radius and period off the body's own record; the escape and the quarter crossings clicks) |
| 7b the strong ratio | 2.0, the border's four clicks against two (DETECTOR, series N); nature 12.72 | SHOWN: the give once per body, held // h units at a contact, so the alpha gives 8 against the deuteron's 4 whatever the partners; the ratio a constant of the rule, blind to the give's value | RULE: a give that grows with the bonds a body makes; a bilinear form on the partners' rows passes the three tests in form; per partner 6, per partner squared 18 (COMPUTATION); nature's 12.72 the partners' count to the power 1.68, reachable only by a declared integer per shape, a fit | E; NO (the border clicks; the books a check) |
| 8a the neutron's step | every neutron at its key on its own clock, the width 0 (DETECTOR, 64 clicks of content 3); in the lattice's clock 0.036 registered, 0.08 to 0.13 at head (GAMEBOARD); nature's exponential, width over median ln 9 / ln 2 = 3.17 | SHOWN: the `become` at a declared count is a step in each body's own clock at any count; the spread in the tick is the crowd's spread of 1 + k_crowd over the 64 Nodes, bounded by the crowd's range | RULE: decay-by-crowd-v1, the `become` fired by a met row of a declared family instead of by a count, so the waiting time is the arrivals' inter-arrival distribution, exponential only where the declared bath's arrivals approach a Poisson comb (COMPUTATION from the declaration); generic, vector ((E) and (D)) and local in form; a re-run reads the crowd's spread alone and cannot reach 3.17 | E, audited A; YES for the paper's number (the width over the median in the lattice's clock) |
| 8b the neutrino's passage | 16 of 1024 at the first reader, 0 behind, the far detector 699 of 711 (DETECTOR, series J2, met bit for bit); nature about 1 | SHOWN: a window admits w / N of a stride coprime to N, 1 / 64 exactly, and a reader behind reads the same residue class, empty; the ray's own phase constant in flight in the registered world | DECLARATION: the `nu` family's content and the key `massive_rows` (with 8c); content 0, no turn: 0 behind, as read; content 1 under massive-rows-v1 (the row turning its phase per Link by abs(p_a) N / h steps over the action h): each reader admits a class shifted by the turn per Link and the window empties a class, 16 rows per class over 1024 births, the first reader 16, a second reader at a fresh class 16, the ratio 1.000 exactly (COMPUTATION), the far detector 1024 less 16 per class covered; 0 behind again when the shift per Link is 0 mod N (p = 2^12 with h a power of two dividing p) | D; NO (the readers' own records) |
| 8c the massless neutrino | the `nu` family with no content, an input; nature's heaviest state above 9.8 x 10^-8 of the electron's | SHOWN: a family's content is a declared integer of the family table | DECLARATION: the `nu` family's quantum 1 under `massive_rows`; 0 refuted; 1 puts the electron's declared content at 1.02 x 10^7 units or more (COMPUTATION on the comparison side), inside the working bound at S_w = 1 | D; NO (an input) |
| 11a the far lamp's brightness | the pin q_eff = +1 (COMPUTATION; the run not made, expansion-v1 not built); nature -0.53 | SHOWN IN FORM: the click count falls as 1 / (1 + z) and the content per click stays the birth's, one factor where nature's flux has two (chapter 5.7) | RULE: a click whose read energy follows the row's frequency in flight ("not one of the six"); in form the massive row's phase turn per Link read as h f at the detector (a key and a reading), which gives q_eff = 0, Milne's, and then row 3's RULE remains | D and A; YES (no click made; the chain's inverse square the shell mean) |
| 11c Tolman's test | the pin n = 1 in (1 + z)^-n (COMPUTATION); nature 4 | SHOWN IN FORM: the Nodes and the fan's lines fixed under the wall, a ruler of l Nodes at d subtends l / d; the flux one power of 1 + z | RULE: the same as 11a for one power (n = 2 at most), and for the other two an angular size that grows with the redshift, a board whose Links stretch, no verb on the state vector: it fails the vector test and the local test; not reachable inside the six verbs | D and A; YES (the ruler's size the board's Nodes) |
| 13 light bending | the law as built 0.000 pixel (DETECTOR, series K); under `flow_link` at gamma_PPN = 1 the ring's mean radial shift 0.731 against 0.731 +- 0.025 (DETECTOR); C_ring = 3.652, 3.821, 3.918 at b = 6, 3, 8 (COMPUTATION), the continuum's 4 within 2.4, 1.0, 1.4 grains; nature 1.75 arcseconds, 1 + gamma = 2 | SHOWN: the walk of a light row past a held mass by the law's integer steps, the engine walking it as the algebra does to 0.01; the M / b form; SHOWN IN FORM: 2 c_f (n S_w / d) G M / (c^2 b) in the straight-path limit (chapter 5.9); NOT SHOWN: the 2 of c_f and the value of n S_w / d | DECLARATION: gamma_PPN = 1 (the key `optical`), c_f = 2 with it, and n S_w = d; gamma_PPN = 0 the time part alone, 0.87 arcseconds; gamma_PPN = 1 gives 1.75 in the limit of large b and L, the finite ring's 2.4 grains the lattice's own; the hypothesis that would derive the 2 must add a space part no verb reads: it stays a declaration | A in part; YES in one input (k_a(b) = 0.0445 from the board's age moment, not read by a lamp at b; the ring's click outside) |
| 14 Newton's periods | T(24) / T(12) = 1.677 under the one constant, 1.512 under the line drive (COMPUTATION from two means of unclosed loops, DETECTOR clicks; the escapes face clicks at 1208 and 2452); the pin 2.00 +- 0.18; nature's inverse square 2^(3/2) in space, not compared | SHOWN: the push (1 + u / c) A / r from the click count, the circle unstable at 0.34 c; Newton's form in the algebra of the clicks with Einstein's step between (chapter 5.6); SHOWN IN FORM: the 1 / r and 1 / r^2 in the shell mean, NOT FROM THE CLICKS until read at two distances; NOT SHOWN: nature's velocity-free gravity, the value of G | READING: the moving detector's arrival click (a massive row released past a held mass, its Node against a control), the deciding pin -4.63 pixels under the arrivals count against -5.47 under the crossing count, the bracket 0.5; and the three readings of records 1098 and 1100 (the count ratio at two distances on one crowd, the second difference of arrival Nodes over ordinals at two distances, the recurrence on the ordinals) with the one word, whether a read at a body is a click (chapter 3.2) | A, B and C; YES, three times (the period on the host's tick, the probe's own record, the contacts) |

### 6.3 Why the rows that passed passed, by the algebra (by reference)

What the three passes and the two bounds share (the file's section 0b,
one line per row of the paper's Table 2 that is not a FAIL, by
reference): each reads a count of clicks or a ratio of two counts at a
declared detector, from a formula that is exact on the law's integers
(the rungs, the tables, the flight table, the window) with no shell
mean, no tick and no body's own record in the chain: row 1a's S = 2.75
at N = 64 from the closed form S(N) of chapter 4.10, one gather of one
record from both settings; the marginals 32 of 64 at every setting
(Theorem 5); S at seven grains, the plateau 181 / 64; row 2b's 64 / 0
from the bilinear form's offers and the rungs; row 9's Malus Nodes on
the tables' grain; row 5a's pace from one Link per interval and the
digital line (a BOUND on Q); row 7a's give once per body (a BOUND on
the input); GHZ's three-party sign from the same one gather; and the
four host-tick readings that stand beside them (row 12's 1.907 under
the age word, the equivalence after a detector in series X, the
covariant readings in series S, the Doppler on the axis). The FAIL rows
are the same chain with one thing missing, named in their column: 1b
and 1c read the same gathers as 1a and lack nothing of the counts (a
theorem; the counter); 2a reads the same rungs as 2b and 9 at a fan
whose landings the comparison's limit does not have (F); 3, 4b and 12
read the same count ratio as series T and X on a tick instead of a
detector's own count (A), and 3 lacks besides the emitters' rate (C);
4a and 4b read the same crossing count as the Doppler and lack the
mover's rate r (C); 5b computes the same round trips as 5a's flight
table with no detector at all (A) and lacks the contraction (C's
root); 7b and 8a read the same border and shell clicks as 7a and lack
a transformation fired by a met row (E); 8b and 8c read the same window
as the marginals' gather on a row whose content and phase do not turn
(D); 11a and 11c would read the same count ratio as series T on a flux
whose energy does not follow the rate (D) over a shell mean (A); 13
reads the same walk as light beside a mass with the crowd's stretch
taken from the board (A) and the 2 declared; 14 reads the same lamp
and line as series D3's controls on the host's tick, with the push at
a body counted as a click (A, B and C).

### 6.4 The order to take them in (by reference)

The file's section 2 and the Boss's reading of it ([record 1128](LOG_2026-09-20.md)
(a)): the generic fixes in the clicks that move several rows at once
first (item 1, mode C's one rate, rows 4a and 4b, one decision, no run;
item 2, mode D's turned phase read as a rate, rows 8b and 8c, one
declaration and a run of seconds; item 4, mode B and E's body as a
detector, row 14, the moving detector's click, a world of minutes to an
hour), with item 3 beside them (row 13, the owner's word on gamma_PPN =
1, no run); then 2a, 8a, 7b, 6, 3 and 11a, 11c, 5b, 1c, 1b; yielding to
the owner's orders in force on rows 13 and 14; the items that are the
owner's own decisions (4a and 4b's key, 13's strength, and which count
a body's push takes, arrivals or crossings, the line record 1128 (a)
calls "a read at a body is a click") are put to him one line each.

---

## 7. How the group was reached, from one Node and its six neighbours (one page)

The owner's word of 2026-09-23 ([record 1109](LOG_2026-09-20.md), the
writer's translation): "they will ask how we got to this group. We
reached it from the Nodes, a Node and its neighbours, there we started;
between Nodes, the GameBoard; through the GameBoard we reached this
group; the GameBoard showed us that everything converges to this group,
or matrix, whatever you call it." This page gathers the answer; nothing
here is written anew.

**(i) The one choice, and the seven Nodes.** The one choice of the
model is the six Ports of a Node, P = {+X, -X, +Y, -Y, +Z, -Z} with the
opposite involution, the L1 neighbourhood of the cubic lattice: a Node
and its six neighbours, the seven Nodes of the causal front, one message
per Link per interval in each direction (chapter 1.1, "the cube"; the
paper's section 2). Two more choices, and no fourth: the phase circle
Z_N, N per world, and the translation group of the torus, Z_X x Z_Y x
Z_Z, each factor a circle or a segment ([FULL_PICTURE.md](FULL_PICTURE.md)
section 1, "The choices, and what follows from them": "one chooses the
lattice (the dimension and the neighbourhood), the phase circle and
the torus; the point group is then forced and is already the largest;
the translation group is the board; and the only freedom that changes
the physics is the neighbourhood, through the front, c and the table
above").

**(ii) What the choice forces: the 48, and the 24 within them.** "What
is not chosen: the group of 48. The cube's group (the signed
permutations of the three axes, 3! x 2^3 = 48; `cube_symmetries` in
`core/game_board.py`; the 24 of hand +1 the rotations, the 24 of hand
-1 the reflections, told apart by the hand as a pseudoscalar, BEAM_LAW
note 39) is the symmetry of choice 1: every map that preserves the six
Ports as a set and the lattice's Links is one of the 48, and every one
of the 48 does. Nothing was added to it; the mass, the charge and the
other contents of the family table live on the amounts, on which the
48 act trivially (the 48 permute directions and Nodes; a content is a
scalar)" (FULL_PICTURE section 1, verbatim); no three-dimensional lattice has a point group of order above 48
(the crystallographic restriction: the cubic holohedry O_h, of order 48,
is the largest of the seven holohedries by order; the hexagonal D_6h, of
order 24, is not a subgroup of O_h, so "every Bravais lattice's point
group is a subgroup of O_h" is false, the Paper Verifier's line of
2026-09-24), so a lattice can keep at most the 48, and the cubic lattice
keeps all of them. Over the integers the only
bijections that preserve the cone of one Link per interval are these
48; a boost is not Z-linear, so no boost is among them, and Lorentz's
form is reached Outside from the clicks (chapter 5.1) and not as a
symmetry of the lattice. The determinant splits the 48: the 24
rotations, the group of order 24, isomorphic to S_4 on the cube's four
body diagonals, and the 24 reflections; the hand, needed to carry spin
and polarisation (hand-v1, record 128: the group page's own words,
carried over, chapter 1.3), is the pseudoscalar that tells
them apart, h -> det(g) h (chapter 1.1 and 1.4; Theorem 1). "24 is the
count of the rotations of the six-Port Node, the octahedral rotation
group, 48 with the hand; a boost is not among them" ([HISTORY.md](designs/algebra_transition/HISTORY.md)
entry 18; the owner's word on the name, record 231: the 24 are the
octahedron's 24 rotations, not his numeral).

**(iii) The road back, from the operations to the group** (chapter 1.3,
the chief physicist's six items, by reference): the operations came
first as acts on the board; the group is the answer to "which maps
preserve what the operations act on"; the 48 first appeared in the code
as the collision table's invariance (the test enumerated the 48 maps
that leave the table as it is) and were then recognised as the symmetry
of every operation; the 24 came from the hand; the other objects the
same way (the step and the flight shifts, hence the torus's
translations; the turn adding modulo N, hence Z_N and Z[Z_N]; the
collision a permutation generated by a shift, hence a cyclic action; c
not chosen but the norm of the flight operator, 1 / sqrt 3, from
locality and straightness); and the group does back to the physics
what the physics gave it: it forces forms (the only isotropic even
reading of a body's momentum within the six operations is c **p** .
**p**: the 48 force the form's isotropy, while the 3 and E_0'^2 of the
square E_0'^2 + 3 **p** . **p** are the band's, 4.2 and 8.1, not the
48's). In one sentence: the
operations did not deduce a group; defined on a Node of six Ports, the
48 are everything that preserves that Node and its cone, and once every
rule is required to commute with them they choose the admissible forms,
the group of order 24 being the part under which the hand is kept as
well.

**(iv) The twenty-five dated steps of the transition** (HISTORY.md,
"The entries, in date order", each with what it was as ordinary
physics, what it became in the law, when and by whose word, where it
lives, its reading by kind, what it superseded; one line each here):
1 (09-17) the shared quantum resource deleted, locality without
exception; 2 (09-17) the amplitude a phase and a conserved content,
Born's rule a coupling, a declared table of bounded integer ratios; 3
(09-17) a force a catalog entry read at a meeting, the engine performing
only simple operations; 4 (09-18) the Born table computed from N, a
clock content, a Node its six Ports; 5 (09-19) the law of events,
everything derived from vector operations, a field an event, matter a
measured event; 6 (09-19) the law of the ray, a quantum an integer row
on the record, the collision a permutation, the click the only one-way
border; 7 (09-19) the tables generated from the keys, a detector's one
reading the moments of order 0, 1, 2, the push one bilinear form; 8
(09-19) E = h f, a release costing the emitter by its phase rate; 9
(09-20) one mechanism for all the laws, a force a column with a sign and
a lifetime, the coupling a signed inner product over the columns; 10
(09-20) two kinds of readings, "our laws are on the GameBoard; in the
detector one sees other laws"; 11 (09-20) masses and charges the
initialisation, the law quantising what lives on a compact group and
leaving free what lives on a scale; 12 (09-20) the amplitude law, a
quantum a record, the click choosing one by the wheel, the world the
list of clicks; 13 (09-20) the record's push by share, the step drive
and the fraction-free law, every count an accumulator on the reader's
own record; 14 (09-20/21) Doppler emerging by itself, the key deleted;
15 (09-20) the fan as a width, Huygens on the lattice, the exact phase
at the click, the register's pins detector readings only; 16 (09-21)
the whole law one vector operation on the integer torus, the six verbs,
the main course, the three tests; 17 (09-21) the click without
amplitudes, the record an element of Z[Z_N], the weight one bilinear
form f^T **G** f, Born's rule the unique positive quadratic form, complex
numbers leaving the code; 18 (09-21) the vector program from group
theory, the lattice as the translation group, the 48 with the hand, the
wheel a count on Z_W, c the norm of the flight operator, rows and
bodies; 19 (09-21) the world through a detector in vectors and tensors,
a formula gives and a run proves; 20 (09-21) Lorentz A and B, the
Lorentz factor a root, the seventh verb, not admitted, the covariant
readings keeping the exact square; 21 (09-21/22) the clock's word the
age moment, the one wall function of the crowd, Newton and Poisson
after a detector; 22 (09-22) a detector's clock a member of the age
wall's set at coefficient 1; 23 (09-22) the click theorem, a click the
passage of information Node to Node, a click family's transformations
the Lorentz group up to scale; 24 (09-22) the paper's framing, Inside
and Outside, "matches nature" never "is nature", whatever can be
computed algebraically computed algebraically, the conversion as a map;
25 (09-22) the three formulas, the step beneath the board, the step
above it and the conversion, a transformation for every formula with
the detector at the place, locality Outside.

**(v) The owner's sentence, the chapter's close** (record 1109, the
writer's summary of the owner's sentence): the
GameBoard showed that everything converges to this group and this ring,
and what did not converge was not put in.

---

## 8. The massive record kind: the pair per kind, the block, the coupling, the click, the seed, the direction of time

The model owner's word of 2026-09-23, 20:24Z, through the chief
physicist (record 1489 of [LOG_2026-09-20.md](LOG_2026-09-20.md), the
Boss's line in Highlights 5.4): the project must be rebuildable from
HIGHLIGHTS.md and this file alone; every design page, schedule and
reading is history under them; what is not in one of the two files is
not part of the law or the method. This chapter carries the law of the
massive record kind from its design pages on main (`50d4980a`) into
this file, in this file's own language: the objects, the six verbs, the
identities, each identity with its proof here or the exact place where
the design proves it. The sources, each the record of its day and none
a second statement: the chief physicist's third draft
[designs/detector_law/MASSIVE_RECORD.md](designs/detector_law/MASSIVE_RECORD.md)
(sections 1, 2, 3, 4, 6, 7, 8, 11 item 7 and 14), the schedule
[designs/detector_law/SCHEDULE.md](designs/detector_law/SCHEDULE.md),
the declarations
[designs/detector_law/declarations/DECLARATIONS.md](designs/detector_law/declarations/DECLARATIONS.md),
the massless kind's design
[designs/detector_law/DESIGN.md](designs/detector_law/DESIGN.md)
(sections 2 and 5, the rule and the counting form) and
[POSTULATES.md](../POSTULATES.md) section 10. The rules this chapter
obeys, beside the head's: integers only inside a rule, no root and no
float; a real number appears only as a declared pin or a computed
consequence and is labelled so (COMPUTATION or DECLARATION); no result
of any run enters (the chapter is the algebra before any run, the
exploration page and the build's readings being history beside it);
nothing is stated that a design page on main does not state, and each
statement carries one of three marks: PROVED HERE (a proof for every N
and every board written in this chapter, this chapter's own), CARRIED
(the design's proof, cited by file and section), or COMPUTED, NOT
PROVED (the design's closed form or script, with what a proof for every
N and every board would need). The three tests of every rule (2.8) are
stated per rule in this file's words: generic, vector, local. Every
result matches nature or does not; none is how nature is.

**The symbols of this chapter, named once.** a_now, a_before and a_next
a record's level at a Node now, one interval ago and one interval on,
integers at the amplitude unit declared at load; r and r' the remainder
kept on the row before and after the interval; S_6 = a_E + a_W + a_N +
a_S + a_U + a_D the sum of the six reads of the record's a_now (the
neighbour across a Link; the Node itself on a folded axis of extent 1;
0 beyond an open face); [num, den] a record kind's declared pair, num
and den whole, 0 < num <= den; omega the frequency angle per interval
and **k** the wave vector, angles k_x, k_y, k_z per Link, k its
Euclidean length, a character (omega, **k**) a plane wave of the
torus's translations (1.6) and the time translation; omega_0 the pitch
of a kind, the gap of its band at **k** = 0, cos omega_0 = num / den,
and N_0 = 2 pi / omega_0 its rest period in intervals; omega_l(k)
light's band at the same **k**; c = 1 / sqrt 3 Links per interval the
pace of light (4.2), c_m and c_eff two paces of the massive kind
defined in 8.1, gamma_m = 1 / sqrt(1 - v^2 / c_eff^2) the one formula's
Lorentz factor, beta_c = v / c a pace as a fraction of c, and K the
drive's whole count of intervals per hop, v = 1 / K (K plain, the
drive's count, apart from the row kind (K) in parentheses of 8.9); I
the conserved quadratic form of a kind, **A** the read matrix (six
entries +1 per row, symmetric), **D** the diagonal matrix of the
per-Node weights D_i = den_i / num_i (the design writes it **W**),
**M** = **D**^-1 **A** / 3 the rule's matrix; R a block's Nodes, a
finite G_48-set of Nodes, s its side; mu the medium's pitch (its
omega_0), g_w = 2 (num' / den' - num / den) the well's depth to first
order (the design writes it g, the letter this chapter keeps for the
coupling), omega_b the bound mode's frequency, eps = 1 - omega_b^2 /
mu^2 its binding depth, kappa the mode's tail per Link (kappa here the
tail's decay, apart from the walk's angle of chapter 5); W a click's
declared wheel and 1 / W its first rung; g = [g_n, g_d] and G = [G_n,
G_d] the two coupling pairs at a block's Nodes (G plain the source's
pair, never the Gram matrix **G** of 2.5; the product G g one number
and the ratio G / g another), **P**_R the projector onto the Nodes (1
on R, 0 elsewhere; bold, an operator, apart from the verb (P)), alpha =
g D_in / G with D_in the weight on the Nodes, and J the coupled
scheme's exact invariant (J plain, apart from the joint pointer J(o_A,
o_B) of 3.6); ev the evaluation Z[Z_N] -> Z[zeta_N] of 2.5, used as
named there.

### 8.1 The rule with a pair per record kind; the band; the pitch; the two paces; the one formula's gamma

**The rule** (CARRIED: MASSIVE_RECORD.md section 1, form (B) of
the gate reviewer's 12.6 (c); at [1, 1] DESIGN.md section 2 bit for bit). At
every Node a record's row (a_now, a_before, r) is mapped, once per
interval, by

    3 den a_next + r' = num S_6 - 3 den a_before + r,        0 <= r' < 3 den,

then a_before <- a_now, a_now <- a_next, r <- r'. Light is the value
[1, 1]: 3 a_next + r' = S_6 - 3 a_before + r, 0 <= r' < 3. A massive
kind is a value den > num; nothing else names the mass. The verbs: (B)
one entry, num, of the declared matrix on the six reads and one entry,
-3 den, on the own row's past, the rate a bilinear form of the
neighbourhood's state (2.2); (T) the accumulator translated by that
rate (2.1); (D) the division by the wall 3 den with the remainder kept
on the row (2.6). The compensated form with a self term, `3 q (a_next +
a_before) = q S_6 - 3 p a_now`, is not the law: its checkerboard
character lies below the band's bottom in three dimensions for every p
> 0 (8.1, the band; MASSIVE_RECORD.md section 3, WITHDRAWN); its pair
maps onto this rule's by den / num = 1 + p / (2 q) to second order.
The three tests: generic, one primitive with one declared pair and no
family name, light the value num = den, the engine branching on no
name; vector, (B), (T), (D) on the row, no root, no float, the
amplitude unit declared at load; local, the record's own row and its
six reads, nothing kept at a Node beyond the row and its remainder. All
three held (MASSIVE_RECORD.md section 1 and section 12's table).

**The band, PROVED HERE.** Drop the remainder (its exact accounting is
8.2) and read the rule on a character a(x, t) = cos(omega t - **k** .
**x**) of a periodic board: a_next + a_before = 2 cos omega a_now and
S_6 = 2 (cos k_x + cos k_y + cos k_z) a_now, so the rule holds on the
character exactly when

    2 cos omega = (2 num / (3 den)) (cos k_x + cos k_y + cos k_z),

the design's dispersion surface (MASSIVE_RECORD.md section 2). Since
abs(cos k_x + cos k_y + cos k_z) <= 3, abs(cos omega) <= num / den <=
1: every character has a real omega for every **k** and every pair
with den >= num, the checkerboard corner (**k** = (pi, pi, pi), cos
omega = -num / den) included; the band is [-num / den, num / den] in
cos omega. With light's band cos omega_l(k) = (cos k_x + cos k_y + cos
k_z) / 3 at the same **k**, the same line reads

    cos omega = cos omega_0 cos omega_l(k),        cos omega_0 = num / den,

the massive band as light's band times the pitch's cosine (MASSIVE_RECORD.md
section 8, "the massive band"). At **k** = 0 the gap: cos omega_0 = num /
den, the rest frequency omega_0, the rest period N_0 = 2 pi / omega_0
intervals, the rest energy h omega_0 (h the action, the head; de
Broglie's internal clock as the thing compared with); light has omega_0
= 0, a zero mode that is a level and not a clock. The exact relativistic
form (PROVED HERE, one substitution): with cos k_i = 1 - 2 sin^2(k_i /
2) and 2 - 2 cos omega = 4 sin^2(omega / 2),

    4 sin^2(omega / 2) = 2 (1 - num / den) + (num / den) (4 / 3) (sin^2(k_x / 2) + sin^2(k_y / 2) + sin^2(k_z / 2)),

light's form (num = den) with the pace squared scaled by num / den, the
design's 12.6 (d). The band is an identity of the linear recurrence on
a periodic board for every N and every extent; on a board with an open
face the characters are not eigenvectors and the statement is the
periodic board's.

**The two paces, and the exact cone (PROVED HERE as the expansion at
the band's bottom; the design's section 8, its exact form on Reviewer
3's token).** Near **k** = 0 light's band is cos omega_l = 1 - k^2 / 6
+ O(k^4), so omega_l^2 = k^2 / 3 + O(k^4) = c^2 k^2 + O(k^4), the pace
c = 1 / sqrt 3 of 4.2 reached once more. (i) To second order in omega
and **k** together, 2 - 2 cos omega = 2 (1 - cos omega_0) + cos omega_0
c^2 k^2 + O(4): omega^2 = omega_0'^2 + c_m^2 k^2 with omega_0'^2 = 2 (1
- cos omega_0) and

    c_m^2 = cos omega_0 c^2,        c_m = c sqrt(cos omega_0) = c (1 - omega_0^2 / 4 + O(omega_0^4)),

the Klein-Gordon dispersion whose cone is c_m and not c: a massive
record's limiting pace is below light's by the deficit omega_0^2 / 4 in
c (COMPUTATION: 0.56 percent at the declared pair [800, 809], omega_0 =
0.1493, N_0 = 42.08; the illustrations 0.39 percent at N_0 = 50 and 3.0
percent at N_0 = 18;
MASSIVE_RECORD.md section 2), the same c in the limit num / den -> 1.
(ii) With no truncation in omega_0: write omega = omega_0 + delta at
the band's bottom; cos(omega_0 + delta) = cos omega_0 - sin omega_0
delta + O(delta^2) and cos omega_l = 1 - omega_l^2 / 2 + O(omega_l^4),
so sin omega_0 delta = cos omega_0 omega_l^2 / 2 and omega^2 = omega_0^2
+ 2 omega_0 delta + O(delta^2) gives

    omega^2 = omega_0^2 + c_eff^2 k^2 + O(k^4),        c_eff^2 = cos omega_0 (omega_0 / sin omega_0) c^2,

the exact cone of the band's bottom; c_eff^2 / c_m^2 = omega_0 / sin
omega_0 = 1 + omega_0^2 / 6 + O(omega_0^4) exactly (COMPUTATION: 1.0037
at mu = 0.15). The two agree at leading order in omega_0 and differ at
order omega_0^2; (i) is the second-order expansion in omega and **k**
jointly, (ii) the second-order expansion in **k** alone, and the named
cone of the massive kind is (ii) (MASSIVE_RECORD.md section 8, decided
by derivation before any pinned run; the k^4 terms of light's own band
remain the GameBoard's residual, said once here for the band's k^4 terms). For every 48-invariant rule of range 1
with a gap the design states c_m^2 / c^2 <= cos^2(omega_0 / 2), no such
rule giving a massive record light's c in three dimensions (COMPUTED,
NOT PROVED: `massive_corner_stability.py`; a proof for every rule would
enumerate the two-coefficient family of 1.1's derivation, `a_next +
a_before = w S_6 + s a_now`, and bound its pace at the band's bottom
against its corner's stability). The two-pace world is prediction 1 of
8.9.

**The one formula's gamma (CARRIED: MASSIVE_RECORD.md section 8).** A
block's moving clock is compared with Lorentz's through the factor of
the massive kind's own cone, gamma_m = 1 / sqrt(1 - v^2 / c_eff^2), and
not light's gamma at c: the record in the well obeys the equation of
its own band and no other, and the boost of a resting solution under
the symmetry of that equation is the Lorentz boost at c_eff, in whose
frame the declared Nodes of width s are gamma_m s wide and the phase
turns at omega_b / gamma_m; light enters only through the coupling
(8.5), which does not carry the well. On the GameBoard a block stepped
one Link per K intervals has beta_c = sqrt 3 / K, so light's factor
squared is the rational pair gamma(c)^2 = K^2 / (K^2 - 3) (PROVED HERE:
1 / (1 - 3 / K^2)), the pair [K^2, K^2 - 3] the design carries into the
coupling in motion (8.5; 3 / 2 at K = 3); gamma_m at c_eff is a real
number computed from the pair and K, never formed inside a rule
(COMPUTATION at K = 3, mu = 0.15: gamma(c_eff) = 1.22705, gamma(c_m) =
1.22820, gamma(c) = 1.22474, the last two the CONTROLS the pins carry
beside the named one, 0.09 and 0.19 percent from it; MASSIVE_RECORD.md
section 8). The same gamma_m carries the moving emitter's redshift's 1 + z = gamma_m (1 +
beta_c) (COMPUTATION on the example pair [800, 809]: 1.9355 at k = 3, mu =
0.15; 1.9373 at c_m and 1.9319 at c beside; the moving emitter's redshift's declared world
[156, 157] reads 1.9339, DECLARATIONS.md section 4) and the second term of 8.4.

### 8.2 The conserved form I on any extents, and the remainders' exact identity

**The form, PROVED HERE for every board.** Let **A** be the read matrix
of the board (A_ij the number of reads of j among the six reads of i:
the neighbour across a Link once, the Node itself once per folded
direction, nothing beyond an open face); it is symmetric, because i
reads j in the direction d exactly when j reads i in -d, and every row
sums to at most 6. Let **D** = diag(D_i), D_i = den_i / num_i >= 1 per
Node (one pair on the whole board, or a well of 8.3), and **M** =
**D**^-1 **A** / 3. Without the remainder the rule of 8.1 is a_next +
a_before = **M** a_now, and the form

    I(a_next, a_now) = a_next . **D** a_next + a_now . **D** a_now - a_next . **D** **M** a_now
                     = SUM_i D_i (a_next,i^2 + a_now,i^2) - (1 / 3) SUM_i SUM_d a_next,i a_now,n_d(i)

is conserved, the second sum over the six directed reads n_d(i) of
every Node (the Link sum a_next,i a_now,j + a_next,j a_now,i when every
extent exceeds 2, the self-reads otherwise). Proof: **D** **M** = **A**
/ 3 is symmetric. Let the next level be a' = **M** a_next - a_now. Then
I(a', a_next) - I(a_next, a_now) = a' . **D** a' - a_now . **D** a_now -
a' . **D** **M** a_next + a_next . **D** **M** a_now, and since **D**
**M** a_next = **D** a' + **D** a_now the third term is -a' . **D** a' -
a' . **D** a_now, while the fourth, by the symmetry of **D** **M**, is
(**D** **M** a_next) . a_now = a' . **D** a_now + a_now . **D** a_now;
the sum is 0. Nothing but the symmetry of **D** **M** is used, so the
identity holds on every extent and every face. In the engine's units
(times 3 num for one pair): 3 den (a_next^2 + a_now^2) summed over the
Nodes less num (a_next,i a_now,j + a_next,j a_now,i) summed over the
reads, the design's integer line (MASSIVE_RECORD.md section 3; the
design's one-line form writes the read sum with the weight one where
this chapter writes 1 / 3 beside the Node weight den_i / num_i, and the
design's integer line, 3 den per Node against num per read, is this
chapter's form times 3 num; the integer line is the one in force).

**Positive definite exactly when den > num, PROVED HERE for every
board.** In the basis where **D**^1/2 **M** **D**^-1/2 = **D**^-1/2 **A**
**D**^-1/2 / 3 is symmetric, I is the quadratic form of the block
matrix [[**1**, -**N** / 2], [-**N** / 2, **1**]] on (**D**^1/2 a_next,
**D**^1/2 a_now), **N** that symmetric matrix; on an eigenvector of
**N** with the eigenvalue lambda the block is [[1, -lambda / 2],
[-lambda / 2, 1]], positive definite exactly when abs(lambda) < 2. By
Gershgorin every eigenvalue of **A** has abs(lambda) <= 6 (each row: at
most six entries, each 1), and **D**^-1/2 **A** **D**^-1/2 / 3 has
abs(lambda) <= 6 / (3 min_i D_i) = 2 max_i (num_i / den_i) < 2 whenever every
Node's den_i > num_i; so I is positive definite for every massive pair
on every board, and at light's pair, den = num, it is semidefinite,
the checkerboard and the zero mode its null directions (DESIGN.md 2.1,
the design's own statement of the light case; 12.6 (c) for the massive
one). A well of 8.3 is a per-Node **D**, and the same proof gives the
same verdict while every Node's den'_i > num'_i; the design states the
condition as "positive definite while the mode's 2 cos omega_b < 2",
the same condition read on the mode.

**The remainders' exact identity, PROVED HERE for every board.** In the
engine's integers the level is a_next = **M** a_now - a_before + e with
e_i = (r_i - r'_i) / (3 den_i) (divide the rule of 8.1 by 3 den_i).
Repeat the three lines above with a' = **M** a_next - a_now + e: the
third term gains -a' . **D** e and the fourth gains -e . **D** a_now, so

    I(t) - I(t - 1) = SUM_i D_i e_i (a_next,i - a_before,i) = SUM_i (a_next,i - a_before,i) (r_i - r'_i) / (3 num_i),

and times 3 num for one pair, I(t) - I(t - 1) = SUM_i (a_next,i -
a_before,i) (r_i - r'_i): the design's identity (MASSIVE_RECORD.md
section 3, "EXACT"; its script `massive_conserved_form.py` reads the
residual 0 on a 6 x 6 x 1 periodic board, a chain of 40 and a 6^3 box,
COMPUTATION, which this proof makes a theorem). The remainders' term is
computed from the state the engine holds, so the books assert an
integer identity and no tolerance; it is bounded by 3 den times the
motion, the design's "bounded jitter". The norm the click's rungs
divide is I (8.6): a static level (a_now = a_before everywhere) has I =
0 and clicks nowhere, which the sum of the squares would count
(DESIGN.md 2.1, the reason).

**Lemma (the layer against the 3-D board), PROVED HERE.** In the
physicist's words (the Boss's addition of 20:33Z; the decision the
owner's word of record 1454, [Highlights 5.4](HIGHLIGHTS.md), the pin
worlds on a one-layer board provided the algebra holds there): a layer
is the same rule with an axis of extent 1, on which the Node reads
itself twice (a_U = a_D = a_now, DESIGN.md section 2; the six reads S_4
+ 2 a_now); the conserved form I holds exactly there with the
remainders' term; so a layer and a 3-D board differ only in geometry
(the mode's extent, the band's corner, the cube's threshold, isotropy
under the cube group), never in the rule; hence one 3-D world per pin row at
the end, the layer's reading labelled beside. Proof: on an axis of
extent 1 the read matrix **A** has A_ii = 2 for that axis's two reads
(one per Port, +U and -U both landing on i) beside the other axes'
reads; it is still symmetric (a self-read is its own converse) and its
rows still sum to at most 6, so the two proofs above hold word for
word: I is conserved (only the symmetry of **D** **M** was used),
positive definite for den > num (only the Gershgorin bound was used),
and the remainders' identity is the same three lines. On the layer
the band of 8.1 reads 2 cos omega = (2 num / (3 den)) (cos k_x + cos
k_y + 1), the folded axis contributing its cos 0 = 1, so the corner
sits at 2 cos omega = -2 num / (3 den) and not at -2 num / den, which
is why a layer is blind to the 3-D corner (MASSIVE_RECORD.md section
3); the rule is one and the same. The design's identity for I on any
extents including 1 is its section 3 (the builder's finding, the
directed reads), and its script `massive_conserved_form.py` reads the
residual 0 on a 6 x 6 x 1 periodic board (COMPUTATION), the check of
this proof; a chain is the same lemma with two axes of extent 1 (four
self-reads, the six reads S_2 + 4 a_now).

### 8.3 The block: the well of the pair on declared Nodes, its clock the bound mode

**The object (CARRIED: MASSIVE_RECORD.md sections 1 and 4).** A foreign
object is no new group object and no new verb: (i) a finite set R of
Nodes, a G_48-set (a cube the cube group's own shape; a square on a layer the
stabiliser of the layer's normal), DECLARED as world data like a wall's
placement (kind 3 of Highlights item 5, the apparatus); (ii) the rule
of 8.1 on R with a LOWERED pair
[num', den'], num' / den' > num / den, a well of the pair in the
medium whose pair [num, den] is the kind's own declaration (the
medium's pitch mu); (iii) its clock the bound mode of the map in that
well, omega_b a character of the time translation at **k** = 0, one
element of Z[Z_N] carried by all the Nodes in step (the phase of a row
is carried by its two levels (a_before, a_now) together with its
amplitude, and a table acts on that pair by the linear form of 1.7,
DECLARATIONS.md section 14; the nearest angle on Z_N by the phase table
at load, DECLARATIONS.md's head, is a GAMEBOARD diagnostic and not a
table's input); (iv) its motion
the characters (omega, **k**) of 8.1's surface; (v) its momentum the
existing **p** in Z^3 and its step the existing verb (T), one integer
per axis for the whole block with its remainder, a declared tie, and
its push the stress of light's field at its outer Ports (8.11); (vi)
its click the evaluation across R (8.6). The whole difference between light and a foreign object
in the algebra is a gap. The Nodes' declaration is lawful world data, a
scalar on Nodes on which the cube group acts trivially, carried by the step verb
like a wall's placement; nothing is declared in motion (the mode's
extent, frequency and regime follow from the pair and the side).

**The two regimes (CARRIED: section 4).** By the side s against the
one-Node extent 2 / (3 g_w): the WELL regime, s small, the mode
extending far beyond the Nodes, its frequency near the gap's, eps small,
its clock in motion Lorentz's to first order (8.4); the CAVITY regime,
s comparable or larger, the mode inside the Nodes, its clock in motion
the medium's (8.4). The tail outside the Nodes falls as exp(-kappa x)
with cosh kappa = 3 D_out cos omega_b - 2 on a chain, D_out = 1 + mu^2 /
2, the extent 1 / kappa = c / (mu sqrt eps) Links in the continuum
(COMPUTED, NOT PROVED: `massive_board_margin.py`; a proof would solve
the rule's recurrence outside the well on a chain, where the cosh line
is the character of a decaying exponential in the same substitution as
8.1's band, and bound the three-dimensional tail by it).

**The cube's threshold (COMPUTED, NOT PROVED: `massive_cube_threshold.py`).**
On the infinite board a mode binds in a cube of side s exactly when g_w
exceeds g_c(s) = D_out / Lambda(s), Lambda(s) the largest eigenvalue of
the massless lattice Green's function restricted to the cube, with g_c(s)
s^2 -> 2.190 (converged to 0.1 percent by s = 20; G_0(0) = 0.758193,
Watson's integral, the check); a proof for every s would bound Lambda(s)
s^2 from both sides by the Green's function's asymptotics. The
reversed-mass window and the smallest binding sides per mu are the
design's table (section 4), computed. On a layer a square well binds at
every depth, so eps at the same s and g_w is deeper than the cube's
(section 11 item 7, computed).

**Light cannot be a body (PROVED HERE, the design's norm bound made a
one-line proof).** An index for light is the pair on light's record at
the Nodes, D_i >= 1 inside and 1 outside (the design's (M) form): the
operator **D**^-1/2 (**A** / 3) **D**^-1/2 has norm at most
norm(**D**^-1/2)^2 norm(**A**) / 3 <= 1 x 6 / 3 = 2, so no eigenvalue
lies beyond the massless band's top, no bound mode exists, and no lump
of light holds itself: an exact never in every dimension (MASSIVE_RECORD.md
section 4 (III), "light cannot be a body", the owner's sentence; the
design's self-trapping search on the chain, `massive_light_self_trapping.py`,
a COMPUTATION beside this proof). What holds a block's Nodes together
is the declaration of R or the tie of (v); the massive record's mode
inside R is then a computation.

### 8.4 The motion: one statement, and its two limits

**The one formula (CARRIED: MASSIVE_RECORD.md section 8).** The moving
block is a resting block of width gamma_m s along its motion with the
same well, read at 1 / gamma_m:

    f / f_0 = omega_b(gamma_m s, g_w) / (gamma_m omega_b(s, g_w)),        gamma_m = 1 / sqrt(1 - v^2 / c_eff^2),

f_0 the rest clock's frequency and f the moving one's, both read as a
count between clicks on the block's own record (8.7); omega_b(s, g_w)
the lowest mode of the well of side s and depth g_w on the world's own
board, a COMPUTATION per world before its run. The design derives it as
the boost of the continuum operator of the band's bottom (8.1 (ii)): the
declared Nodes widen in the block's frame and never contract, nothing
is declared in motion, and Lorentz is reached as a relation on the
characters (no boost among the cube group, chapter 1.2's row). On the GameBoard
the formula is COMPUTED, NOT PROVED (`massive_block_clock_motion.py` on
a chain, `massive_layer_pins.py` on a layer, both the design's own
scratch, to 0.01 percent for s >= 12 and 0.15 percent on the layer; the
rest mode stepped at K = 3 after a ramp); a proof for every N and every
board would show that the stepped well's rule, a_next + a_before =
**M**(t) a_now with the Nodes moved one Link every K intervals, has a
quasi-periodic solution whose clock at the co-moving centre is the
boosted mode's to the order of the hop's grain, which no line of the
design writes. Its two limits are identities of the formula itself
(PROVED HERE, given the formula): in the WELL limit omega_b does not
depend on s, so f / f_0 -> 1 / gamma_m, Lorentz's clock as the thing
compared with; in the CAVITY limit omega_b is proportional to 1 / s, so
f / f_0 -> 1 / gamma_m^2, the medium's clock, the earlier theorem for a
rigid region carried, true exactly in this regime. Between them the
first-order deviation in the well regime is eps (gamma_m^2 - 1) / 2
below 1 / gamma_m (CARRIED: the design's closed form (1 / gamma_m)
sqrt((1 - gamma_m^2 eps) / (1 - eps)), whose first order in eps is 1 -
eps (gamma_m^2 - 1) / 2, PROVED HERE by expanding the root): the
carried Nodes' mark on a bound clock, prediction 2 of 8.9; exactly
Lorentz only with the well's strength carried as g_w / gamma_m, a root
the algebra does not have, so the residual stays. The boost of a rest
state at omega_0 to the pace v is the character with the carrier k =
gamma_m omega_0 v / c_eff^2, its frequency gamma_m omega_0 and its
internal phase omega_0 / gamma_m: the free massive packet's clock slows
by 1 / gamma_m and the packet contracts by 1 / gamma_m on the GameBoard's
own surface (CARRIED: section 8, "the characters themselves", to 0.1
percent at k <= 0.3 per Link, COMPUTATION). The three tests: the motion
is a derivation and adds no sentence to the rule; nothing to test
beyond 8.1's (MASSIVE_RECORD.md section 12's table).

### 8.5 The coupling between the two kinds: the Euler-Lagrange scheme of a two-point Lagrangian, its exact invariant J with the cross term, the one division

HISTORY (the model owner's adoption of record 1962, 2026-09-25): the bilinear
coupling of this section is retired from the law; the families are coupled by
the click alone (9.34 (B), 9.36), the residues spread by the remainder kept at
the body's Nodes (9.34 (A)), the index of a medium is a lowered light pair
(9.31 (8)), and the Node clock of 9.35 is what slows one family by another's
content. What follows is the record of the coupling as it was built and
checked.

**The form (CARRIED: MASSIVE_RECORD.md section 7).** At a Node of R the
two records' rows are coupled by one entry of verb (B)'s declared matrix
over the OTHER record's two columns, the first difference both ways:

    the massive row gains    g (a_l,now - a_l,before)      (the receive: light's field drives the block's record),
    light's row gains       -G (a_m,next - a_m,now)        (the source: the block's current is light's source at its Nodes),

both local to the Node, in the engine's columns in this order (the
design's (B)): first the massive step reads its own row and light's
a_now - a_before as they stand before light's step of this interval and
writes a_m,next; then light's step reads its own row and the massive
a_next - a_now just written; then both records shift. The owner's `a_m
+= g a_l` (record 1414) is the receive's meaning; the first-difference
form is its stable writing. The amplitude form (light's row gaining g
a_m) is withdrawn as tachyonic: the coupled mass matrix at **k** = 0,
[[0, -g], [-g, omega_0^2]], has determinant -g^2 < 0 and so one
negative eigenvalue (PROVED HERE, the determinant), and a block of side
s carries a growing mode once s > pi c omega_0 / g (COMPUTATION, the
design's). The block emits at its mode through the same entry, a lamp
at its own rest frequency with no train declared, and its mode radiates
and decays with a lifetime falling as 1 / g^2 (COMPUTED, NOT PROVED:
the gate reviewer's chain, 320 periods at g = 0.002 and 76 at 0.005; a proof
would compute the mode's radiative width from the coupled dispersion
below). The three tests: generic, one matrix entry, no family name, the
same for every pair; vector, (B) linear in the other record's two
columns, no root, no float; local, the Node's own two records. All three
held (section 7).

**The scheme is the Euler-Lagrange scheme of a two-point Lagrangian
(PROVED HERE; the design states it, MASSIVE_RECORD.md section 7, "THE
EXACT INVARIANT").** With **D** the diagonal of den / num and **A** / 3
the six reads over 3, let

    L(t) = -a_m,t . **D** a_m,t+1 + a_m,t . (**A** / 3) a_m,t / 2 + alpha (-a_l,t . a_l,t+1 + a_l,t . (**A** / 3) a_l,t / 2) + g a_m,t+1 . **D** **P**_R (a_l,t+1 - a_l,t),

alpha = g D_in / G, one number because the block declares one pair on
its coupled Nodes (**P**_R **D** = D_in **P**_R). The discrete
Euler-Lagrange equation of a_m,t (the derivative of L(t - 1) + L(t) set
to zero) is -**D** a_m,t-1 + g **D** **P**_R (a_l,t - a_l,t-1) - **D**
a_m,t+1 + (**A** / 3) a_m,t = 0, that is a_m,t+1 + a_m,t-1 = **M** a_m,t
+ g **P**_R (a_l,t - a_l,t-1), the massive step with light's backward
difference; the equation of a_l,t is -alpha a_l,t-1 + g **P**_R **D**
a_m,t - g **P**_R **D** a_m,t+1 - alpha a_l,t+1 + alpha (**A** / 3)
a_l,t = 0, that is a_l,t+1 + a_l,t-1 = (**A** / 3) a_l,t - (g D_in /
alpha) **P**_R (a_m,t+1 - a_m,t) = (**A** / 3) a_l,t - G **P**_R
(a_m,t+1 - a_m,t), light's step with the massive forward difference:
the scheme of the design's (B) line for line. Being variational and
linear it is symplectic, and a symplectic linear map has an exact
quadratic invariant.

**The invariant J, PROVED HERE for every board (the design computes
it exact to 10^-12 on a chain, `massive_conserved_form.py`).** Let I_m
be 8.2's form of the massive record with the weights **D** and I_l
light's with the weight 1, and

    J = I_m + alpha I_l + g SUM over the Nodes i of D_i (a_m,t+1 - a_m,t)_i (a_l,t+1 - a_l,t)_i,

the cross term of the two first differences on the Nodes. Proof: the
massive step is a_next = **M** a_now - a_before + e_m with e_m = g
**P**_R (a_l,now - a_l,before), so by 8.2's identity I_m(t) - I_m(t -
1) = SUM_i D_i e_m,i (a_m,next - a_m,before)_i = g D_in SUM over the
Nodes of (a_l,now - a_l,before)(a_m,next - a_m,before); light's step is
a_next = (**A** / 3) a_now - a_before + e_l with e_l = -G **P**_R
(a_m,next - a_m,now), so alpha (I_l(t) - I_l(t - 1)) = -alpha G SUM
over the Nodes of (a_m,next - a_m,now)(a_l,next - a_l,before) = -g D_in
SUM over the Nodes of (a_m,next - a_m,now)(a_l,next - a_l,before). Write
per Node X = a_m,next - a_m,now, Y = a_m,now - a_m,before, U = a_l,next -
a_l,now, V = a_l,now - a_l,before; the cross term's change is g D_in
(X U - Y V), and the whole change of J per Node is g D_in [V (X + Y) -
X (U + V) + X U - Y V] = 0. So J is conserved exactly, before the
remainders, on every board and every extent, for every pair and every
coupling; it is the invariant of THIS column order and of no other (the
mirror scheme, light's step first with the massive backward difference,
conserves its own J with the cross term on its own columns, by the same
lines). In the design's E units (E = 3 I) J is E_l + (G num_in / (g
den_in)) E_m + 3 G SUM over the Nodes of (a_m,t+1 - a_m,t)(a_l,t+1 -
a_l,t): the continuum's combination E_light + (G / g) I_m PLUS the
cross term of the two first differences on the Nodes, which is what
oscillates (up to 1.4 percent of J at G g = 0.05 on the design's chain,
COMPUTATION) and is a GAMEBOARD reading of the coupling's grain, not
energy lost. A coupling taken along the Node's path on a hop interval
(the co-moving difference) has no conserving pair: every hop-modulated
coupling is pumped parametrically by the hop's pair resonance with
light's band, exact and degenerate at K = 3 (the mode k = 2 pi / 3 at
omega = pi / 3); so the coupling in motion is the same-Node form's and
the hop moves the Nodes' set and the pair region only (CARRIED:
the gate reviewer's sentence in section 7; the pump COMPUTED, NOT PROVED,
`massive_moving_index.py`; a proof would write the hop as a periodic
modulation of the coupled operator at (omega, k) = (2 pi / K, 2 pi / K)
and show the pair condition omega_1 + omega_2 = 2 pi / K, k_1 + k_2 = 2
pi / K mod 2 pi has solutions on light's band for every K >= 4 and a
degenerate one at K = 3; prediction 4 of 8.9).

**The one division (CARRIED: section 7 (A)); its remainder identity
PROVED HERE.** The coupling is folded into the rule's one division, one
(D) per row per interval and no second (D) for g or G: with g = [g_n,
g_d], G = [G_n, G_d] and P = 1 on the Nodes, 0 elsewhere,

    the massive row:   3 den g_d a_next + r' = num g_d S_6 - 3 den g_d a_before + 3 den g_n P (a_l,now - a_l,before) + r,     0 <= r' < 3 den g_d,
    light's row:       3 G_d a_next + r'    = G_d S_6 - 3 G_d a_before - 3 G_n P (a_m,next - a_m,now) + r,                  0 <= r' < 3 G_d,

the walls 3 den g_d and 3 G_d. Dividing, e_m gains (r - r') / (3 den
g_d) per Node and e_l gains (r - r') / (3 G_d), and the three lines of
8.2 give

    J(t) - J(t - 1) = SUM_i (a_m,next - a_m,before)_i (r - r')_i / (3 num_i g_d) + alpha SUM_i (a_l,next - a_l,before)_i (r - r')_i / (3 G_d),

exact in integers on every board (the design checks it in exact
rationals on a chain, residual 0, `massive_conserved_form.py` part 3);
the engine's test asserts this identity, scaled to integers by the
common 3 L g_d G_n (L the least common multiple of the numerators where
the well has its own; G_d cancels against light's wall and is not in
the scale), and no tolerance.

**The index (COMPUTED, NOT PROVED: `massive_dielectric_index.py`).** In
the continuum of the coupled scheme the dispersion is (c^2 k^2 -
omega^2)(omega_0^2 - omega^2) = G g omega^2, both roots real and
non-negative for every k and G g > 0 (stable at every strength), and
the index of the block's Nodes for light is n^2 = 1 + G g / (omega_0^2 -
omega^2), the classical dielectric as the thing compared with (n plain
the index, apart from the suspension pair's n of the head): Maxwell's
dielectric on the potentials, the record the potential, the field its
first time difference, the polarisation's current the massive record's.
A proof on the GameBoard would take the coupled scheme's characters on a
board coupled at every Node and read the product of the two bands; on a
block of s Nodes the response is the block's own mode sum and not the
infinite medium's, the design's CONTROL beside its pin (section 11 item
6, the index row). The mirror is the strong-coupling limit, the Fresnel
step ((n - 1) / (n + 1))^2, the sponge a declared damping; one declared
g with G per object and no second coupling (the pace coupling
withdrawn). In motion the co-moving first difference at a carried Node
is short by 1 / gamma_m^2 unless the product G g is carried as G g x
[K^2, K^2 - 3] (8.1, the rational pair), a COMPUTATION from the drive's
count the stepping Node has and nothing new declared in motion (the
owner's delegation, section 7); its reading is prediction 3 of 8.9,
which the design states is not covariant under either declaration and
not Fizeau's drag. Gravity as an index of the crowd's massive records
is a hypothesis outside the law under its own name,
`gravity-index-hypothesis`, with no number (section 7's last line).

**The one pair the engine forms in motion (the gate reviewer's classification of
the engine audit, 2026-09-24, row (b)-7; a declared rule, not a hidden
formula).** The coupling's second pair in motion, [W_d^2, W_d^2 - 3 **P** .
**P**] from the drive's count W_d and the declared momentum **P** (the same
pair as [K^2, K^2 - 3] at the cadence K; MASSIVE_RECORD.md section 7), is
a rule of this design that the engine forms each interval from declared
integers, with no float and no root, on one Node's own record: the same
standing as the leapfrog's S_6, a formula of the law and not a formula
hidden in the engine. It is the ONE pair the engine forms in motion; every
other pair is read from the table of families (kind 2).

### 8.6 The click of a body at W, and the take

HISTORY IN PART (the correspondence audit of record 1942): the take, the
emitter's own take and the pointer that books the motion squared are retired
by 9.12 and 9.19 (3) (the click is the one reading, the one-way inward flux
per Port; the excited record's rung accrues the centre Node's own share e_c,
9.17 (7) (e)). What stands of this section is the click as the evaluation of
the body's own record against its rung in the body's own clock
(POSTULATES.md section 10).

**The click (CARRIED: MASSIVE_RECORD.md section 6; the owner's word of
record 1414; POSTULATES.md section 10 as settled by record 1421).** The
click is in the Outside, and light produces it, through a body: the
click is the evaluation (E) of the body's own record on its Nodes at
the declared wheel W. Light arriving at the block's Nodes drives the
block's record through the receive of 8.5; the block's pointer
accumulates its own record's motion across all its Nodes, in I's units
(DESIGN.md 2.1, the Port's factor: the pointer books in the units of the
conserved form, the design's counting form); the click is the
comparison W x (the pointer) >= (the record's norm), integers both, the
crossing of the first rung 1 / W of the norm in the block's OWN clock
(the counting form, DESIGN.md section 5; the norm the record's I at the
end of its insert; the pointer books the motion squared, (a_now -
a_before)^2 per Node per interval, never the levels' squares, in one
currency with the ladder's weights of 2.6: the owner's word of
2026-09-24, record 1679, and 2.5's closing paragraph on the two words);
the click line carries the block's own count (its
mode's cycles, 8.3) and the light record's birth stamp. The
receiver-inserter's second face (the model owner's word of 2026-09-24,
06:42Z, record 1694; DECLARATIONS.md section 10 item 10): an emitter takes its own
record's remnant after its train, from the first interval after it (the
owner's word of 07:42Z, record 1711; no timing integer), in the receiver form of the take
and in the record's kind's pair; what it takes never left it and is not
received back (the detector's own count, Highlights item 7), so it is
booked as content taken by the emitter, a host row, never a pointer and
never a click. Light does not
need to stay in order to be read; it needs only to pass through a body
that has a clock. A click is a body's event in the body's clock: light
never clicks; light is read: it moves the body's record, and the body
clicks; a free Node has no rung, no count and no reading; the verbs are
lossless, light passes on, and the click needs no sink. In this file's
words: the body's record across R is one element of Z[Z_N] (8.3 (iii)),
the click is ev of 2.5 applied to it against the declared rung, the
weight the bilinear form (2.2) on that element, the record ending at the
detector and the detector's own record changing (3.1, the click as an
action; POSTULATES.md section 10, the addition of record 1421: a record
is read at a detector by the evaluation in the detector's own clock, the
click stamped with the detector's own count n_D). The three tests:
generic, one primitive, the rung on the pointer's norm, no family name;
vector, (E) the evaluation, the norm a bilinear form, then the
comparison of (D) on the wheel; local, the body's own record across its
own Nodes, with the one non-local step named as before, the completion
of a record (its offer exhausted into receivers or gone off the board)
the host's reading and not a dependency of any Node (DESIGN.md 2.1's
last paragraph; 3.1). All three held (MASSIVE_RECORD.md section 12's
table).

**The take, a separate declaration of the worlds that absorb, not a
condition of the click (CARRIED: section 7, "the sink"; POSTULATES.md
section 10).** Where a world must absorb (a screen that must not
re-emit, a sponge, a wall that eats) it declares a loss the verbs do not
have: the TAKE, a damping pair on light's row at the Nodes of an object
declared ABSORBING, so that the record ends there (POSTULATES.md section
10 as written: a light record ends only where a take is declared), and
NO take for a clock body read many times (a clock body takes nothing;
the record passes on and is read again). The take is a declaration of
the world and a second one-way step beside the click (8.8); it is not
the law's. What is a measurement stays 3.2's sentence: a detector's
click, a count between clicks on the detector's own record, a ratio of
such counts; a reading of the board is a diagnostic.

### 8.7 The seed: the bound mode's integer profile over the whole board, the engine reading integers, the clicks the reader of record

**The declaration (CARRIED: MASSIVE_RECORD.md section 11 item 7;
DECLARATIONS.md, "The reader of record of every clock row"; SCHEDULE.md
the muon's moving clock).** A pin world of a clock row declares its initial state as the
bound mode's integer profile: the mode as the margin module computes
it, rounded to integers at the world's amplitude OVER THE WHOLE BOARD
(no radius: a cut at two extents leaves a step of e^-2 of the tail that
seeds the medium's free modes again, which on a periodic board never
leave), the same profile at both levels, a declaration of kind 2 (the
initial state, one of the four declared inputs of Highlights 5.4). The
standing start is exact (PROVED HERE, one line): the mode's two-column
state is phi (cos(theta - omega_b), cos theta), phi its profile and
theta its phase, and at theta = omega_b / 2 both columns equal phi
cos(omega_b / 2), so the state (phi, phi) is the mode's own at that
phase up to a common factor, and the standing start excites the bound
mode alone, to the integer rounding of the profile and the remainders'
grain. Under a flat seed on the Nodes a WIDE mode's clicks beat, because
the flat seed overlaps the mode poorly and the rest goes to the medium's
free modes (the design's scratch; its numbers exploratory and not
carried here). Reproducibility: a run's record must follow from the
world file and the engine alone, byte for byte, and a float Lanczos at
load is iterative and not bit-identical across hosts; so the GENERATOR
computes the mode and writes the profile's INTEGERS into the world file
(or a sidecar the world file names by blob SHA), the engine reads
integers under `seed`, the value `mode` lives in the generator and not
in the engine, and the profile printed at load from the margin module is
the GAMEBOARD check that the file's integers are the module's mode: the
world file's data, nothing the declaration does not name.

**The reader of record.** The reader of record of every row that reads a
clock is THE CLICKS: the count between clicks at W on the block's own
record over the hold after the ramp (DETECTOR; the click's record the
block's Nodes' sum as built, the centre Node's clicks a diagnostic
beside), its pin the mode's period on the world's own board at rest and
the one formula's number of 8.4 in motion, the count's grain the hold
over the period, the clicks' own spectrum the finer COMPUTATION on the
click times; the spectral peak of the summed record is a GAMEBOARD
diagnostic beside, never the pin. A row whose clicks still beat (the
ramp radiates into the medium in motion) is a diagnostic until they read
the mode; the pin world then takes a longer ramp before its run, and the
spectral peak never stands in for the clicks. The three tests: the seed
is a declaration of the world's initial state and no rule; the reader is
3.2's reading rule and adds nothing to it.

### 8.8 The direction of time: the Inside a bijection, the click the one deletion, the transform ev between the Inside and the click board

**The Inside is a bijection (CARRIED: MASSIVE_RECORD.md section 14 (a)
and (b), the design's three-line proof, written here for the wall d =
3 den, light's d = 3).** Given the neighbours' reads S_6, the step
(a_before, r) -> (a_next, r') of one row is a bijection of Z x {0, ...,
d - 1} onto itself: (a_before, r) -> n = num S_6 - d a_before + r is a
bijection of Z x {0, ..., d - 1} onto Z (each integer once, the Euclidean
division's uniqueness); n -> (floor(n / d), n mod d) = (a_next, r') is a
bijection of Z onto Z x {0, ..., d - 1}; so the step is a bijection and
its inverse is exact: n = d a_next + r', m = num S_6 - n = d a_before -
r has one solution with 0 <= r < d, a_before = ceil(m / d), r = d
a_before - m. Nothing is lost in the remainder: the Inside is reversible
to the bit, for every N and every board, since the neighbours' reads
are the state's own. It is not symmetric in FORM: the inverse rounds up
where the rule rounds down and the remainder lives on the later level,
so the same formula run backward (the swap with the floor kept) is a
different map, off by the remainders' grain (a random walk of one unit
per Node per interval; the design's chain deviates by 29 and 365 of an
amplitude 957234 after 600 intervals, COMPUTATION, `massive_time_reversal.py`);
the rule carries an arrow in its bookkeeping and none in its
information. The exact inverse is verb (D) with the ceiling in place of
the floor, a declared variant of the one division (the remainder's
convention flipped), lawful under that variant and needing no seventh
verb. The coupling in motion (8.5's column order): each half-step is
invertible given the other record's levels (a triangular map), so the
pair of steps is a bijection, the reversed run taking the half-steps in
the opposite order with (g, G) -> (-g, -G), the product G g and the
dielectric unchanged, and the hop schedule reversed with the drive's
accumulator, itself an integer map with an exact inverse: reversible,
not symmetric in order (CARRIED: section 14 (c)). This restates for the
algebraic rule POSTULATES.md's line that the interval is a bijection on
a GameBoard without a measured event and the click the one one-way
border (its head; 4.7, Theorem 3, said it for the rows that hop).

**The click is the one deletion; ev is the transform between the Inside
and the click board.** The click (8.6) removes the record's rows at the
detector's Nodes, hands its content over and advances the detector's
count by one: the one deletion OF THE LAW (3.1); the take (8.6) is the
second one-way step, a declaration and not the law's. The counts form a
free abelian monoid and not a group (3.1), which is an ORDER and not a
loss; no step of the board un-deletes a row (the design's run with a
click reversed by the exact inverse deviates by the deleted rows'
amplitude exactly, COMPUTATION). In this file's map: the transform from
the Inside to the click board is the conversion of 3.5, rung o chi_1 of
f* f o ev, the evaluation ev of 2.5 on the body's element of Z[Z_N]
followed by the quadratic weight and the rung; ev is a ring
homomorphism with a kernel (the cancel), the weight is quadratic and the
rung a threshold, so the transform is many-to-one at every step and has
no inverse, while every Inside step has one. THE ARROW OF TIME IS BORN
AT THE CLICK (and at a declared take) and nowhere in the rule: a bijection
on the Inside, ev and the rung on the way out (MASSIVE_RECORD.md section
14 (d); prediction 7 of 8.9). The world that shows it is a CHECK and
never a pin against nature: a train with no detector declared, N
intervals forward under the engine and N under the exact inverse, back
to its first rows bit for bit with the books' E equal; the same world
with a detector declared, which does not return, by the deleted rows
exactly (section 14 (e)).

### 8.9 The two kinds of rows, (K) a known formula and (P) a prediction; the eight predictions with their falsifiers, declared before any run

HISTORY IN PART (the correspondence audit of record 1942): prediction 2's
second term is re-derived in 9.22 (8a) (the cone's term plus the lattice's);
predictions 3, 4 and 5 rode the moving material and the push, retired by 9.24
(3); predictions 1, 6, 7 and 8 stand as restated in 8.1, 9.22 (8a), 9.26 (3)
and 9.22 (8).

**The two kinds (CARRIED: SCHEDULE.md, "The two kinds of rows"; the
owner's word of about 17:25Z, record 1466).** When the algebra reaches a
KNOWN formula in the clicks, the engine reaching it is the control of
the engine against the algebra; the beautiful thing is to reach what has
NO known formula, predict it from the algebra and then run it; what is
measured in the world is measured in the world of clicks, not on the
board. Every pin row carries (K), a known-formula row (the algebra's
identity a textbook formula as the thing compared with), or (P), a
prediction row (a number the algebra gives and no known formula gives).
Every number below is a COMPUTATION from this chapter's forms, declared
before any run, and no run's reading stands beside it here.

**The (K) rows of the massive kind, one line each** (SCHEDULE.md's
table; the kinematic numbers at K = 3: beta_c = 1 / sqrt 3 = 0.57735,
gamma(c) = sqrt(3 / 2) = 1.22474, COMPUTATION): the muon's moving clock, the muon's
form, the moving block's clock 1 / gamma_m to the band's second term
(8.4), the layer pin world's number 0.8116 by the one formula with
gamma_m at c_eff (the layer mu = 0.15, s = 14, g_w = mu^2 / 4; against
1 / gamma_m = 0.8150 to the residual 0.3 percent; 0.8108 at c_m and
0.8132 at c the CONTROLS beside; nature's form 1 / gamma, Bailey 1977,
matched in form at the world's beta_c); the moving emitter's redshift, the moving lamp's
redshift, 1 + z = gamma_m (1 + beta_c) = 1.9355 at K = 3 receding on
the example pair [800, 809] at mu = 0.15 (the moving emitter's redshift's declared world [156,
157] reads 1.9339, DECLARATIONS.md section 4; 8.1;
nature's form gamma (1 + beta), Ives and Stilwell 1938, Botermann
2014); the round trip off a receding mirror, the round-trip Doppler off a receding transponder, (1 +
beta_c) / (1 - beta_c) = 3.732 at K = 3, r-free (5.1); the anisotropy between moving arms between two arms in motion, N_par / N_perp = 1 and 1 within +-
0.03 plus eps (gamma_m^2 - 1) / 2, (K) in the number and (P) in the
mechanism (the arms held by light's force, no rigid rod); Sagnac's two-way light times, the Sagnac
ratio, beta = v_c / c = 0.5774 at K = 3 exactly, a count between clicks
independent of the clock's factor; the light clock of two bodies, N_0 =
2 L / c + the two ring-ups, (K) in 2 L / c and (P) in the ring-ups. The
index block at rest is a CONTROL of the coupling and no nature row: its
pin the closed form of 8.5, the cavity's own mode sum a labelled control
beside it, never the pin.

**The eight (P) rows, each with its falsifier in one clause (CARRIED:
SCHEDULE.md's list; DECLARATIONS.md):**

1. The two-pace world: a massive record's limiting pace c_m = c
   sqrt(cos omega_0), the deficit omega_0^2 / 4 (8.1 (i)); falsified by
   a massive front faster than c_m on its world beyond the band, or in
   nature by an electron pace bound tighter than the deficit at the
   declared scale (the bound on the interval's length, SCHEDULE.md: a BOUND on the one scale, one
   interval at most 3.6 x 10^-28 s from the published 2 x 10^-14, the
   Planck time admitted sixteen orders below, COMPUTATION on a NATURE
   number, the scale the owner's declaration and no formula). Its second
   face: a bound clock dilates by gamma at the massive kind's own cone
   c_eff (8.1 (ii)), slower than light's gamma by about beta^2 gamma^2
   omega_0^2 / 6 to second order (0.19 percent at K = 3, mu = 0.15, the
   computed 0.188; 1 / 4 is c_m's coefficient, 0.28 percent, the control
   beside; the Paper Verifier's line, 2026-09-24;
   about 10^-14 at nature's omega_0 of row A); falsified on a pin world
   by the one formula reading gamma(c)'s number and not gamma(c_eff)'s
   beyond the 0.3 percent band. The world that separates the two gammas
   (mu = 0.3 at K = 3 on a 128^2 layer, the square well of side 10 at
   g_w = mu^2 / 8: 1 / gamma at c_eff 0.8104 against 0.8165 at c, five
   bands apart, COMPUTATION) is declared and DEFERRED, no run and no pin
   moved, on the owner's word.
2. The bound clock's second term: a bound body's moving clock reads (1 /
   gamma_m)(1 - eps (gamma_m^2 - 1) / 2) and a free packet exactly 1 /
   gamma_m (8.4); falsified by a pin world's ratio off the one formula
   beyond the band, or in nature by a bound clock dilated exactly as a
   free one below the term under the eps mapping (the bound clock's second term, SCHEDULE.md, a
   BOUND: the stored Li+ clock 2.2 x 10^-11 against its bound 2.3 x
   10^-9; the rotor 0.26 sigma; the eps mapping, a real clock's binding
   energy over its rest energy, a named hypothesis and not derived).
3. The index in motion: the moving block's lab delay head-on at K = 3
   is 0.50 of the covariant slab's under the same-Node coupling with the
   drive's pair (8.5; the design's script number +0.5103 rad, the
   falsifier +- 0.04 rad); the receding number is the script's on the
   DECLARED geometry of MASSIVE_RECORD.md section 11 item 6 (the chain
   of 4000 with light's open faces as the engine has them and the
   reading window [3400, 4800], closed before the face's reflection
   reaches the probe), computed at pin time before the run, and not the
   periodic-wrap chain's 6.8 times the covariant value (a number of the
   script's own wrapped geometry, section 7, read against no open
   face); against nature the DECLARED NON-MATCH with Fizeau's drag
   (first order in beta at large K, not computed), a prediction doing
   its job, written before the run.
4. The hop's parametric pump: a block stepping at K = 3 through light
   feeds the mode k = 2 pi / 3 at omega = pi / 3 through its boundary
   Node, 10^-4 of light's energy per interval (8.5); falsified by no
   growth at that mode in the moving worlds' GAMEBOARD readings, or by
   growth of the same size at K = 4 or 5 (then not the degenerate
   resonance).
5. Five's 1 and 1 from arms held by light alone: the force between two
   blocks through light is 2 A^2 cos(k_0 L) toward the partner, its
   equilibria the zeros of cos(k_0 L), L = (2 m + 1) lambda_0 / 4,
   alternately stable and unstable by the clocks' relative phase (8.11,
   the force between two blocks through light; A the emitters'
   amplitude set by g and G, k_0 the mode's wave number, lambda_0 its
   wavelength, m whole); falsified in the two-arm world by
   N_par / N_perp off 1 beyond 0.03 plus the second term.
6. The atom's lines at the modes' own frequencies, not at their
   difference (a linear scalar coupling: an atom a well of the pair, its
   levels the well's bound modes, its lines the modes' frequencies read
   by light through 8.5; the levels of a declared well a PREDICTION, no
   1 / n^2 ladder expected at the affordable depths and grain, the Bohr
   radius at mu = 0.15 being 527 Links, NOT COMPARED; MASSIVE_RECORD.md
   section 9, the atom's row, COMPUTATION, `massive_well_spectrum.py`);
   falsified by a line at the modes' difference in the probe's spectrum,
   which would need a nonlinear coupling outside the design.
7. The click's arrow of time (8.8): the Inside reversible bit for bit,
   the click the one deletion; falsified by an Inside step without an
   exact inverse, or by a click recoverable from the Outside.
8. The light clock of two bodies: N_0 = 2 L / c plus the two ring-ups,
   never the register's 206 in a body's counting form (the register's
   206 the take world's, an (M) mirror and a detector declared absorbing,
   which the design keeps as that world; MASSIVE_RECORD.md section 9 row
   (d), COMPUTATION per declaration); falsified by the two-body world
   reading 206 +- 2 with the body's count.

The rows this kind does not reach are named and not filled: the crowd's
field (the two slits, the boxed clocks, the deep well's clock, the light clock and the receding index at one third: the coupling gives an index at declared
Nodes and nothing about a crowd's field, the ray law's numbers there
history), the nucleus and a decay (the round trip off a receding mirror and Sagnac's two-way light times: the well binds a record,
not a nucleus; no lifetime derived), the polariser (a scalar record has
no polarisation; Malus and Bell stay under light's declared tables), and
a mass ratio between two kinds (each kind's pair declared, none derived
from another) (SCHEDULE.md, NOT PREDICTED and NOT COMPARED).

### 8.10 The three tests per rule, the scripts, and what is computed and not proved

| Rule | Generic | Vector | Local | Its identity's mark |
| --- | --- | --- | --- | --- |
| the rule with the pair on the six reads (8.1) | one primitive, one pair, light a value | (B), (T), (D) | the row and its six reads | the band PROVED HERE; the two paces PROVED HERE at the band's bottom; the range-1 bound COMPUTED, NOT PROVED |
| the conserved form I (8.2) | one form for every pair | a bilinear form of the two levels | the reads' sum | PROVED HERE on every board, with the remainders' identity |
| the well of the pair on declared Nodes (8.3) | a per-Node pair, world data | the same verbs | the same | the threshold and the tail COMPUTED, NOT PROVED; light's norm bound PROVED HERE |
| the motion (8.4) | a derivation, no sentence added | none needed | none needed | the one formula CARRIED (the continuum's boost), on the GameBoard COMPUTED, NOT PROVED; its two limits PROVED HERE |
| the coupling, first difference both ways, in the one division (8.5) | one g with G, no family name | (B) linear in the other's two columns; one (D) per row | the Node's two records | the Euler-Lagrange scheme PROVED HERE; J and its remainder identity PROVED HERE; the index and the pump COMPUTED, NOT PROVED |
| the click across the Nodes at W (8.6) | the rung on the norm | (E), the bilinear form, (D)'s comparison | the body's own record across its Nodes; the completion the host's | the click's definition CARRIED (the owner's word) |
| the take (8.6) | a declaration of the absorbing world | (D) or the take's pair | the object's own Nodes | a declaration, no identity |
| the seed (8.7) | a declaration of the initial state | none | none | the standing start PROVED HERE |
| the direction of time (8.8) | the same rule | (D) with the ceiling, a declared variant | the same reads | the bijection CARRIED (the design's proof), its inverse exact |
| the block's momentum, step and push (8.11) | one primitive, the stress at the outer Ports and one comparison, the declared integers Q, S, M and the take's scale 56 d; the tie declared per block | (G) the stresses summed into the block's vector, (D) with the remainder kept, (T) the step, then comparisons | the block's own outer Ports and the free Nodes beyond them; per block under the declared tie | the cadence and the bound PROVED HERE as identities of the accumulator; the stress as the wave's momentum flux CARRIED, a declaration of the design and not of the law |
| the force between two blocks through light (8.11) | the same push read on two blocks | the same verbs | the same | the closed form CARRIED (the gate reviewer's, the continuum's coupled emitters); on the GameBoard COMPUTED, NOT PROVED |

The design's scripts, each printing its record beside
MASSIVE_RECORD.md and none an engine run: `massive_c_derivation.py`
(the pace from three inputs, 1.1 of the design), `massive_corner_stability.py`
(the band and the corner), `massive_conserved_form.py` (I and J with
their remainders' terms), `massive_cube_threshold.py`, `massive_board_margin.py`,
`massive_dielectric_index.py`, `massive_light_self_trapping.py`,
`massive_block_clock_motion.py`, `massive_layer_pins.py`, `massive_moving_pins.py`,
`massive_light_clock_relay.py`, `massive_moving_index.py`,
`massive_well_spectrum.py`, `massive_time_reversal.py`. What is computed
and not proved is marked so above, each with what a proof for every N
and every board would need; what the design does not compute it says
(section 12 of the design: Fizeau's drag, the click's completion under
the take, the threshold under a light-shaped well, g against any nature
row, form (C) beyond its name), and this chapter does not fill it. The
block's momentum, step and push and the force between two blocks
through light are 8.11. Where this chapter and a design page differ in a letter or a
factor, the design's integer lines are in force and this chapter says
where it differs (8.2, the read sum's weight); no rule, no number and no
reading is new here.

### 8.11 The block's momentum, step and push, and the force between two blocks through light

**Where the momentum lives (CARRIED: MASSIVE_RECORD.md section 5;
DESIGN.md 5.1 (a), a declaration of the design and not of the law).**
One integer per axis for the whole block, **P** = (P_x, P_y, P_z) in Z^3
with a remainder per axis, the existing momentum of a body (chapter
1.2's row, 2.1's drive), on the block and nowhere else; changed by
nothing but light's field at the block's own outer Ports. Per block one
integer for many Nodes is not one Node's reading, so the block's
momentum is a DECLARED TIE (the gate reviewer's C11): per Node the same rule is
local and lawful, one integer per Node pushed by the stress at its own
Ports; the block declares that its Nodes share one. The block's own
massive record is the block: the massive kind's rows do not push (a
self-force excluded), and a massive-to-massive force between blocks is
not in the law; the force between blocks is through light (below).

**The step (CARRIED; the cadence PROVED HERE as an identity of the
accumulator).** Per interval the accumulator of the axis i gains
abs(P_i) against the wall 3 Q S M x 56 d (Q the label's scale, S the
width and M the block's content, the head's letters; 56 d the take's
pair scale, which enters only with light's push, the engine keeping the
wall at 3 Q S M until the push step and rescaling the world files' P in
the same commit, the builder's answer accepted in section 5 (e)); when
the accumulator reaches the wall the block steps one Link along the
axis in the sign of P_i and the wall is subtracted, the remainder kept
on the block as the rule keeps r: verb (T) then (D), the count of 2.6.
The cadence is the accumulator's closed form of 4.1: after t intervals
the Links stepped on the axis are floor((A_0 + t abs(P_i)) / (3 Q S M
x 56 d)), A_0 the accumulator's start, so the pace is v_i = P_i / (3 Q S
M x 56 d) Links per interval exactly in the mean, one Link every K =
(3 Q S M x 56 d) // abs(P_i) intervals with the remainder kept, and the
declared step of a world is its initial P_i = 3 Q S M v_0 x 56 d; the
rest energy E'_0 = Q S M and the momentum 3 Q S M v = E'_0 v / c^2 with
c^2 = 1 / 3, the head's units. What steps: the block's NODES and its
pair region, one Link together by verb (T); the massive record's rows
STAY on their Nodes and follow the moving well by the rule of 8.1 (a
carried record would be a hop of the record, not the design; 8.4's
formula is the stepped well's); the coupling's first differences stay
the same-Node differences of 8.5 on every interval, and G g is carried
as [K^2, K^2 - 3] (8.1, 8.5). The bound (PROVED HERE, one line): abs(**v**)
< c is the integer comparison 3 (**P** . **P**) < (3 Q S M x 56
d)^2, since abs(**v**)^2 = **P** . **P** / (3 Q S M x 56 d)^2 and c^2 =
1 / 3; no root; checked at the initial **P** and at every change, a
change that would cross it the WORLD'S STOP with a diagnostic naming the
click and the block, never a clamp (a per-axis "K >= 2" is its one-axis
shadow and not the bound: three axes at K = 2 give abs(**v**) = 0.866
Links per interval, beta_c = 1.5; DESIGN.md 1.2 (c)); the record's own
bound is c_m (8.1), tighter than c by the deficit, and the pin worlds
step at K = 3 and 4, well inside both. MUST I's floor, lambda_0 (1 -
beta_c) >= 12 Links with beta_c = sqrt 3 abs(**P**) / (3 Q S M x 56 d),
is the second load-time check, at the initial **P** and at every change
(Highlights 5.4, the owner's word of record 1363: not every N may be
declared).

**The push (CARRIED: MASSIVE_RECORD.md section 5 (a) to (d); DESIGN.md
5.1 (a)).** (a) Which records push: the stress of the LIGHT kind's total
field (all light records superposed, the block's own emission included:
its recoil kept, physics and not a defect) at the free Node beyond each
OUTER Port of the block (a Port from a Node of R to a Node not in R; 6
s^2 on a cube). (b) The integer: at the free Node beyond a Port of the
axis i the stress T_ii = 3 (motion)^2 + (the strain along i)^2 in the
rule's own differences, the terms of the conserved form (DESIGN.md 2.1:
the motion a Node's change in one interval, the strain the difference
across the Link), an integer (times 4 as the pins script computes it);
P_i changes by T_ii at the Ports behind less T_ii at the Ports ahead,
summed over the block's outer Ports of the axis i (verb (G) into the
block's vector), then (D) against the wall 3 Q S M x 56 d with the
remainder kept, then the comparisons above: what the wave loses at the
block the block gains; no new integer, no new verb. That T_ii is the
wave's momentum flux is the design's identification, a declaration of
the design (DESIGN.md 5.1 (a): "a declaration of the design, not of
the law"), stated here as such and not proved: a proof would take the
rule's conserved form on a travelling character and show its Port
balance equals the change of **P** per interval to the remainders'
grain. The click form first written, h times the wave number per click,
is withdrawn as the push and kept as the READING: the clicks read the
momentum the block has, they do not make it. (c) The ramp and the push
together: `ramp` stays the pushing agent's declaration for the pin
worlds (the design's chain device); in the two-arm world the momentum
changes by (b) alone, the arms held at the equilibrium below and no
ramp; a world declares one of the two, never both on one block. (d) The
reading: the stress sum per interval per block is a GAMEBOARD reading
(the force, against the closed form below); the block's pace is read by
its clicks (the count between clicks on its own record and the Nodes of
its clicks, DETECTOR; 3.2, 8.7). The three tests: generic, one
primitive, the stress at the six Ports and one comparison, with the
declared integers Q, S, M and the take's scale 56 d, no family name and
no kind; vector, (G) the stresses summed into the block's vector, (D)
the one division with the remainder kept, (T) the step, then
comparisons, no root and no float; local, the block's own outer Ports
and the free Nodes beyond them, nothing further; per block local under
the declared tie, per Node local outright. All three held (DESIGN.md
5.1 (a); MASSIVE_RECORD.md section 12's row "the block's momentum and
step").

**The force between two blocks through light (CARRIED: MASSIVE_RECORD.md
section 10; the gate reviewer's closed form in
[designs/detector_law/PUSH_BALANCE.md](designs/detector_law/PUSH_BALANCE.md)
section 10.1, the coupled-oscillator force between two emitters at
their own frequency, a COMPUTATION on a chain in floats).** Two blocks
of the design at L Links face to face, each emitting at its mode
through 8.5's source term and each pushed by the total field's stress
at its outer Ports: the force on block 1 is 2 A^2 cos(k_0 L) toward
the partner, A the emitters' amplitude set by g and G, k_0 the mode's
wave number and lambda_0 = 2 pi / k_0 its wavelength in Links (with
each block's own recoil beside it, the closed forms F_1 = (k_b^2 -
k_f^2) T_0 + 2 k_b^2 T_0 cos(k_b k_0 L - delta) and F_2 = (k_b^2 -
k_f^2) T_0 - 2 k_f^2 T_0 cos(k_f k_0 L + delta) at the pace beta_c, k_f
= 1 / (1 - beta_c), k_b = 1 / (1 + beta_c), T_0 one emitter's
travelling-wave stress at rest and delta the declared relative phase;
at rest F_2 - F_1 = -4 T_0 cos(k_0 L) cos delta). Its EQUILIBRIA are
the zeros of cos(k_0 L), L = (2 m + 1) lambda_0 / 4, m whole,
alternately stable and unstable by the clocks' relative phase (in phase
stable at (m' + 3 / 4) lambda_0, 88 Links at lambda_0 = 32; antiphase
at (m' + 1 / 4) lambda_0, 72; COMPUTATION), NOT L = m lambda_0 / 2,
which are the force's extrema: L_0 = 80 = 5 lambda_0 / 2 is the
maximal repulsion and never an equilibrium (the gate reviewer's MUST (i)). In
motion the stable point continued from the rest point by a slow ramp
is L* = L_0 (1 - beta_c) for a pair of emitters at the GameBoard's interval
frequency, and L_0 / gamma_m for the covariant pair (PUSH_BALANCE.md
10.2, COMPUTATION); the two-arm world of 8.9's the muon's moving clock holds its arms at
this equilibrium by light's force alone and no rigid rod, prediction 5.
On the GameBoard the closed form is COMPUTED, NOT PROVED (the chain
within 3 percent at rest at every L from 72 to 92 and in sign and
spacing at K = 3, `check_pair_motion.py` in the gate reviewer's scratchpad; a
proof for every N and every board would take the stress of the
superposition of the two blocks' travelling trains at the Ports from
the rule's differences on a character and compute the cross term
exactly, with the counter-propagating pair's cross term vanishing under
c^2 = 1 / 3 as the design states, 3 omega_1 omega_2 - k_1 k_2 = 0). A
consequence of the algebra written before any board run; the board's
two-block world reads it; the force is the push of light at the Ports
and nothing beside it (no 1 / r form: 8.9's rows not reached).

---

## 9. The tools as operations of the group: a body at rest that does one thing (the mathematician, 2026-09-24, on the model owner's words of 19:10Z to 19:35Z through the Boss)

THE OWNER'S WORD (translated): "derive everything that happens in the
body through the group and its operations ... the body does not move but
does something, and each does something different, polar or not polar.
It must come from the group." This chapter derives every lab tool from
chapters 1 to 8 alone. Each statement is marked IN THE ALGEBRA (its
section), DERIVED HERE (the proof is here) or MISSING (what the algebra
lacks). The engine lines, the numbers and the unit tests of each tool are
[the lab tools' specification](designs/lab_tools/LAB_TOOLS.md), which
cites this chapter and copies none of it.

### 9.1 The notion: a tool is a body at rest, and what it does is an equivariant map

**The object (IN THE ALGEBRA, 8.3 and 1.7).** A tool is a finite set R of
Nodes, a G_48-set, with integers written on its Nodes (a pair, a seed;
the take of this first reading is removed, 9.12), declared world data of
kind 3. AT REST: its Nodes do not move and
its integers do not change with the interval, so the tool is a fixed
point of the time translation's action on the apparatus (its momentum 0,
8.3 (v)). Its SHAPE is fixed by its STABILISER H, the subgroup of G_48
(with the translations along any axis on which R is unbounded) that maps
R to itself and its integers to themselves.

**The theorem (DERIVED HERE).** Every operation of the law commutes with
every g of G_48 (1.1, the law's claim) and with the translations (1.6).
The tool's integers are invariant under H by the definition of H. So the
one rule on the board with the tool written on it commutes with every h
in H: THE TOOL'S ACTION A ON THE RECORDS THAT PASS IT IS AN H-EQUIVARIANT
MAP, A(h . s) = h . A(s). Proof: for h in H the board with the tool is
carried to itself by h, and the rule commutes with h, so the map from a
record's state before the tool to after it commutes with h. Consequence
(Schur's lemma on each isotypic part of H's representation): on each
irreducible part the action is fixed up to one number per multiplicity,
and a map between parts of different irreducible types is 0. So what a
tool CAN do is the space of H-equivariant maps, and what is written on
its Nodes chooses one of them; nothing about its action outside that
space can be declared.

**Polar or not polar (DERIVED HERE, the owner's distinction).** H acts on
the label module (the hand, a pseudoscalar, h -> det(g) h, IN THE
ALGEBRA, 1.2's dictionary: "spin, polarisation: the hand"). A tool is NOT
POLAR when its action is the identity on the label module (it acts on
the places and the characters only): the mirror, the splitter, the
receiver, the emitter, the well body. It is POLAR when its action on the
label module is not the identity: the polariser (a rotation of the label
pair) and the crystal (a map from the arriving label into the pair's
label module).

### 9.2 The operations, tool by tool

**The emitter: the orbit of a Port (DERIVED HERE).** A birth at one
Node with nothing declared about a direction is invariant under the
Node's stabiliser, all of G_48; G_48 acts transitively on the six Ports
(1.1), so the only invariant set of headings containing one Port is all
six: the emitter is isotropic, the orbit sum of a Port. A direction can
come only from the SHAPE of its Nodes (a line of Nodes born in phase,
its stabiliser the line's), never from a declared heading. Written on
the board: the clock pair (a character of the time translation), the
amplitude, the train, the label state (IN THE ALGEBRA, 1.7 and 4.11).
Load check: the train ends at the clock's zero, exact. Not polar.
SUPERSEDED by 9.17: the emitter is a clicking body with a stock of
excitations; the drive and the train retire, the born profile of 9.17
(4) in the train's place.

**The receiver: the click (IN THE ALGEBRA, 2.5 and 8.6).** The evaluation
of the record on the body's Nodes (E), the norm (a bilinear form, B), the
rung (D): THE RECEIVER IS WHERE THE CLICK IS. Its TAKE is a declaration of
the world, not an operation of the law (8.6 says so): MISSING as an
operation, IN THE ALGEBRA as a declaration. Written: the take pair and
the wheel W. Load check: W >= 1, the take [n, d] with 0 <= n <= d. Not
polar (it books the sum over the labels). SUPERSEDED: a receiver is its
name on the records' ladders, with no take (9.12) and no wheel (the
rung's wheel is the record's own, from its birth Node's pair, 9.19 (4)).

**The mirror: a reflection (DERIVED HERE).** A slab of Nodes whose pair
opens a gap (8.1's band, cos omega = (num / den) cos omega_l(k), IN THE
ALGEBRA): its stabiliser contains the translations along its plane and
the time translation. So the incoming character's component along the
plane and its clock are kept (the action is equivariant under both);
no clock with cos omega > num / den propagates inside (8.1), so the
outgoing character has the same clock, the same tangential part, and
the other root of the band: k_perp -> -k_perp, THE REFLECTION of the det
= -1 coset through the plane (1.1). The reflection is not written on the
board: it is the only equivariant outcome of a gap. Written: the gap pair
and the depth. Load check: every family clock that reaches it lies below
the gap, C[k] > 256 num / den on the tables (an integer comparison).
Not polar.

**The splitter: a mirror of finite depth (DERIVED HERE).** The same
operation weighted by the layer's reflection r and transmission t; its
stabiliser contains the reflection through its own mid-plane, which
exchanges its two sides, so its scattering matrix on the two paths is
symmetric, [[t, r], [r, t]], and the conserved form I (8.2) makes it
norm-preserving: abs(t)^2 + abs(r)^2 = 1 and t r* + r t* = 0, the
reflected and the transmitted parts a quarter turn apart. So THE
SPLITTER'S FORM FOLLOWS: a thin material layer; a table with declared
outputs cannot be H-equivariant (its outputs are directions it declares,
which its stabiliser does not fix). Written: the layer's pair (its share
computed from the band). Not polar.

**The polariser: a rotation of the label pair (IN THE ALGEBRA, 3.6).**
The rotation **U**_s on the label module with **U**_s^T **U**_s = n_s
**I** exactly, then the receiver's take on one component. It is a
receiver acting in the rotated label basis, not a separate operation
(DERIVED HERE). Its equivariance: a reflection exchanges the two hands,
and exchanging the rows and columns of **U**_s gives **U**_(-s), so the
mirror image of a polariser at s is the polariser at -s (DERIVED HERE, a
one-line check). At a general s the rotation is not an element of the
Nodes' group (the cube group gives only quarter turns); it IS an element of the
wheel's group, the relative translation x^s of the two hands, with no
table (9.14).
Polar. SUPERSEDED: the setting s, **U**_s and "then the receiver's take"
by the integer axis (a, b) and **M**_u = [[a, b], [-b, a]] on the label
rows (9.14 (b), ADOPTED; 9.16 (2)), the click's weights R = J^2 in the
take's place (9.12).

**The well body (IN THE ALGEBRA, 8.3).** A G_48-set with a lowered pair,
its clock the bound mode, its seed computed and checked at load (8.7).
Not polar.

**The crystal: the transpose of the product (DERIVED HERE).** A record is
two samples of one character of the phase circle, the time translation
and the translations (1.7, 8.1); the characters form a group under the
pointwise product, so energy adding and momentum adding are the dual
group's law ([p] [q] = [p + q] on Z_N, 1.1 and 1.5). The transpose of the
product, m^T([p]) = SUM over a + b = p of [a] (x) [b], is a linear map
with the group's own 0 / 1 table (the bilinear form) whose image lies exactly on the
pairs whose product is the arriving character: CONSERVATION IS ITS
SUPPORT, not a check. On the translations the transpose would be the drive at
every Node with the arriving character's phase there; under the rule of
reading (9.7) that phase is not read, the pair is born by the crystal's
click with its own clocks, and the arriving record's momentum is carried
by the board's own values, the crystal's Nodes taking their share as the
law advances them (9.15; record 1856: the first reading's "handed to the
crystal at its click, the receiver's take" is SUPERSEDED), the pair's
birth spreading from the crystal's Nodes with no phase gradient. The degenerate split [p / 2] (x) [p / 2] is exact on the
circle of 2N (3.6's tables). IT TAKES WITHOUT A CLICK: what it takes is
the born record's (m^T conserves the quantum), so it has no rung and
books on no pointer. MISSING: a record on main carries one clock per
family, so the born family's clock is one split of m^T declared as the
crystal's material; the whole sum (all the splits) in one record is not
on main. Polar.

### 9.3 What follows, not chosen (DERIVED HERE)

**The crystal's state.** Let the crystal's stabiliser contain the
reflection sigma_y through the plane of the arriving axis normal to the
layer's in-plane transverse axis (a crystal symmetric about the arriving
axis); sigma_y exchanges the two arms' headings (+theta and -theta) and,
being a reflection, exchanges the two hands (1.2, h -> det(g) h). Write
the crystal's action on an arriving hand H as T(H) = a HH + b VV + c HV +
d VH in the pair's label module (the first letter the arm at +theta).
The layer's own reflection sigma_z (every body on a layer has it)
exchanges the hands and keeps the arms: T(V) = a VV + b HH + c VH + d HV.
sigma_y exchanges the hands AND the arms: HV -> HV, VH -> VH, HH <-> VV;
equivariance gives T(V) = sigma_y T(H) = a VV + b HH + c HV + d VH.
Comparing the two, c = d: THE TWO MIXED CHANNELS CARRY EQUAL WEIGHTS AND
THE SAME PHASE, HV + VH, the owner's channels of record 1821, now a
theorem of the crystal's symmetry and not a declaration. The weights a
and b of the same-hand channels are not fixed by the symmetry: whether
the crystal also converts into HH and VV is its material (a declared
integer, MISSING a derivation). A crystal with c = d and a = b = 0 gives
HV + VH; its Bell counts follow from ALGEBRA 3.6 and 4.10 and the
tables: at the settings (0, 256), (0, 768), (512, 256), (512, 768), the
counts 150, 874, 874, 150 and 874, 150, 150, 874 thrice, S = 181 / 64
with Bob's two settings exchanged (the mirror image of Bob's polariser,
the exchange of the rows of **U**_b, 9.2), 0 in the cancelled roles.
SUPERSEDED: those counts and S = 181 / 64 are the tables'; under the
integer axis the weights are 9.16 (4)'s (S = 14 / 5) and the pins are
distributions (9.19 item (4b)).

**The hands' paces: equal, never birefringence.** A pace per hand inside the
crystal would have to be invariant under the stabiliser; sigma_z
exchanges the hands, so the two hands' indices are EQUAL in every body on
a layer (DERIVED HERE): birefringence between the hands is forbidden by
the crystal's own symmetry. Under the crystal of 9.7 (the click, then a
birth) the pair is born in phase over the crystal's Nodes and no cone
forms; a cone would need the pair's phase to carry the arriving record's
local phase, which needs a read (9.7): the cone is NOT DERIVABLE under
the rule of reading, and an experiment's headings are its placement's
(9.6). THE CONTRADICTION, NAMED: this paragraph contradicted Highlights
5.4's line of record 1829, "The crystal is birefringent; its directions
arise by phase matching". RESOLVED by the model owner (record 1879,
2026-09-25 on the Israel clock): the crystal of 9.7 (b) is APPROVED, a
click then the birth of an entangled pair, not birefringent, its
directions from the receivers' placement; the line of record 1829 is
marked superseded in Highlights.

**The length the experiment needs.** The joint gather reads the pair's
label state and the two receivers' rotations (3.6); the arms' headings
enter only the share of the conversions that reaches the receivers, never
the counts. A crystal of ONE Node (m^T at one point, every heading alike)
performs the whole operation; a length L only narrows the headings (the
sum over L Nodes, its width about the born family's period in Links over
L), which the counts do not read. DERIVED: the Bell experiment needs L =
1; a formed cone is a separate test.

**The splitter's form.** A thin material layer (9.2), its share computed.

### 9.4 The group element of each tool, and whether it has a direction at all (the owner's word of 19:50Z: "this is rotation X of the group, this is rotation Y"; "think whether they have a direction at all; maybe they have none")

**Two facts of the group used below (IN THE ALGEBRA, 1.1; DERIVED HERE in
one line each).** (i) G_48 = G_24 x {I, -I}: the inversion -I commutes with
everything and has det = -1, so EVERY REFLECTION IS THE INVERSION TIMES A
ROTATION of G_24 = S_4: the reflection through a coordinate plane is -I
times the half-turn about that plane's normal, one of the three
double transpositions of S_4 (the Klein four-group V_4, the half-turns
about the three axes); the reflection through a diagonal plane is -I
times a half-turn about a face diagonal, a transposition of S_4. (ii) The
hand is invariant under G_24 and exchanged by the other coset (h ->
det(g) h, 1.2): S_4 acts TRIVIALLY on the hands.

**A tool has a direction exactly when its stabiliser H is smaller than
G_48 in the part that moves directions (DERIVED HERE).** A direction (an
axis, a plane's normal) is fixed by H only if H is not transitive on the
six Ports; a body whose shape is a CUBE and whose written integers are
invariant under the cube group has H = G_48, which is transitive on the Ports
(1.1), so it has NO DIRECTION. A direction enters only through a body's
shape (a slab, a line) or through the record that arrives (its
character). The table:

| Tool | Its operation, as a group element | Its stabiliser on a cube body | A direction? |
| --- | --- | --- | --- |
| The emitter | the orbit sum of a Port, the projector onto the trivial representation of G_48 ((1 / 48) SUM over g of g applied to one Port) | G_48 | NONE: isotropic; a beam's axis only from a line of Nodes (stabiliser the line's, D_4h, of order 16) |
| The receiver | the evaluation (E) then the rung: a scalar, the trivial representation (the click does not move under any g) | G_48 | NONE |
| The mirror | the reflection through the face the record meets: -I times the half-turn of V_4 in S_4 about that face's normal, acting on the arriving character (k_perp -> -k_perp) | G_48 (a cube of gap): the face is chosen by the record, not by the mirror | NONE of its own on a cube; on a slab its normal (stabiliser D_4h), an unoriented axis |
| The splitter | the same reflection weighted by r, the identity weighted by t (9.2) | D_4h for a one-Node layer | its normal only (a layer is a slab) |
| The polariser | the rotation U_s of the label module, in SO(2) of the label plane, NOT an element of G_48 (except s = 0 and s = N / 2, the identity and the quarter turn); it commutes with S_4, which acts trivially on the hands, and a reflection turns it into U_(-s) (9.2) | EXACTLY G_24 = S_4 for s not 0 or N / 2 | NO SPATIAL DIRECTION, but CHIRAL: it tells the two cosets apart (a reflection turns the polariser at s into the one at -s) |
| The crystal | the transpose m^T of the ring's product on the characters (9.2), equivariant under all of G_48 acting on the characters and the hands | G_48 for a crystal of one Node (a cube) | NONE of its own: the cone's axis is the arriving record's character; the mirrors that fix that axis (the layer's and the transverse one) give HV + VH (9.3) |
| The well body | the bound mode of a lowered pair on a G_48-set (8.3), a character of the time translation at **k** = 0 | G_48 (a cube) | NONE at rest; its motion's direction is its momentum, a declared **p** (8.3 (v)), not a tool's |

SUPERSEDED in the polariser's row: **U**_s and the stabiliser G_24 belong
to the setting s; under the adopted axis (9.14 (b)) the polariser is the
rational projector **P**_u of the specification's A.5, chiral as before
(a reflection sends (a, b) to (a, -b)).

So THE OWNER'S GUESS IS RIGHT, derived: no tool on a cube body has a
direction of its own. The mirror and the splitter act by a reflection =
the inversion times a rotation of S_4 (the half-turn about the normal of
the face met); the polariser acts by a rotation of the label module that
S_4 leaves alone and the inversion reverses; the emitter, the receiver,
the crystal and the well body are invariant under all 48. Where a
direction appears in an experiment it comes from the SHAPE of a body (a
slab, a line of Nodes) or from the ARRIVING record, never from a
declaration.

### 9.5 The code is the algebra: the confirmation that gates every tool's merge (the owner's word of 19:50Z)

For every tool, after the physicist writes its code, the mathematician
reads the code against this chapter and confirms, line by line, that
each operation on a Node is one of the six verbs (2.1 to 2.6) applied
with the tool's written integers and performs exactly the group
operation of 9.4, and nothing else. THE RULE OF THE READING (the owner's word of 20:05Z, through the Boss
at 20:20Z: "you cannot ask a Node what is in it; you get it only by a
click from above"): the ONLY lawful read of a Node's value that decides
anything is THE CLICK, the rung of 8.6 and 9.2; a count of a record's or
a body's OWN clock (its accumulator under the translation: an emitter's train
counted on its own clock, a body's age) is not a read of a Node and is
lawful; a check at LOAD (the gap's check, the clocks' sum, the seeds) is
the loader's, not the law's; every other branch on a Node's value, on a
family's name or on a tool's name is a DEFECT (the owner: "every operation
in the Nodes is always an operation of the group, exactly the one"). The confirmation is written
per tool as CONFIRMED (the code is the algebra) or the defect line with
its file and line; it is the gate for the tool's merge.

### 9.6 Cubes and their orientation (the owner's word of 20:05Z: "everything is made of cubes ... check whether the cubes' orientation has a meaning")

**A cube has no orientation of its own (DERIVED HERE).** A body is
declared by a cube's lower vertex and edge (8.3; a square on a layer, a
segment on a chain, the cube's section by the board's folded axes). Its
faces are the lattice's coordinate planes, so every g of G_48 about its
centre maps it onto itself: its stabiliser is the whole G_48, and the
only "orientation" a cube could have is an element of G_48, which leaves
it unchanged. THE CUBES' ORIENTATION HAS NO MEANING. A direction in an
experiment can come from exactly three places (DERIVED HERE, by listing
what can break G_48): (i) THE RELATIVE PLACEMENT of cubes (the vectors
between their centres; the arrangement's stabiliser is the intersection
of the placements' stabilisers); (ii) THE ARRIVING RECORD (its
character's wave vector, 9.4); (iii) THE LABEL AXIS of a polariser's
rotation, which is not a spatial direction (9.4). The board's own shape
(a layer, a chain) is the torus's, not a tool's.

**No tool needs a shape other than a cube (DECIDED HERE, derived).** The
mirror: a cube of gap of side s reflects through whichever face the
record meets (9.4); its transmitted share falls with the depth crossed
(the chain's numbers, the lab tools' specification 3.3), so a cube of
side s >= 2 is a mirror for a beam no wider than s; a wider mirror is a
row of such cubes side by side, a RELATIVE PLACEMENT (i), not a new
shape. The splitter: a row of cubes of side 1 (its plane the row's, a
placement). The polariser, the receiver, the emitter, the crystal and the
well body: one cube each (a beam from an emitter is a row of emitter
cubes born in phase, a placement). So AN EXPERIMENT IS CUBES ON A
BOARD, and every direction it has is a placement of cubes or the
arriving record's.

### 9.7 Nothing asks a Node (the owner's word of 20:05Z: "you cannot ASK a Node what is in it; you can get it only by a click from above")

**The rule of reading (DERIVED HERE from 2.1 to 2.6 and 3.1).** The six
verbs READ amplitudes to COMPUTE (the sum of six reads, a bilinear form,
a division): that is the rule itself, a group-ring and bilinear
operation, and no decision. What the law never does is read a Node to
DECIDE (a branch on a value): the one comparison that decides is the division with the remainder kept's
at the click, the rung, from above (3.1, 8.6). So a tool's definition may
use the six verbs on the amplitudes freely and a comparison only as the
click.

**The places in the tools' definitions that asked a Node, and their
replacements.**

1. THE CRYSTAL'S START "at the arriving amplitude's first rising zero
   after that Node's first rung" (the lab tools' clause on the first rung, LAB_TOOLS.md)
   READS A NODE TO DECIDE: WITHDRAWN. Two replacements were weighed:
   (a) THE BILINEAR COUPLING g a_arriving a_born (the bilinear form, no read): the
   halving would arise by resonance, BUT from a born amplitude of 0 the
   product is 0 (PROVED HERE), so it needs a SEED of the born family at
   interval 0; a seed on the board is a record with no birth, which
   spreads by the split before any arrival and could be booked and click
   with no quantum behind it: it breaks one quantum, one click (8.6) and
   the initial state (9.9). REJECTED. (b) THE CLICK, THEN A BIRTH (the
   Boss's "or the click itself"; the owner's "the receiver gives a
   click"; the physicist's form of 18:05Z): the crystal's Nodes are the
   arriving record's NAMED RECEIVER (its ladder by name, SIMULATOR_DEFINITIONS.md,
   the receiver by name: every other Node a sink), so the arriving record
   clicks at its FIRST RUNG at the crystal (the one comparison 9.5 allows,
   the line at the rung where the ladder holds one Node) and ends there
   (ONE QUANTUM, ONE CLICK; its remaining field is energy the sinks
   absorb, content 0, as main's receiver by name does); at that interval
   the crystal, as an EMITTER, BIRTHS the pair's record on its Nodes by
   its own clocks (the born clocks summing to the arriving one: m^T, 9.2),
   the pair carrying the arriving record's residue u (one quantum, one
   residue). ADOPTED (DERIVED HERE: it reads nothing but the rung and
   keeps one quantum, one click). Consequences, DERIVED HERE: the pair's
   phase cannot inherit the arriving record's local phase (that would be
   a read), so the pair is born in phase over the crystal's Nodes and NO
   CONE forms (the headings come from the placement, 9.6); every arriving
   record that reaches the crystal's rung gives one pair, so W arriving
   births over the wheel give W pairs and the pairs' counts are exact
   (874, 150, 150, 874 up to the settings' order); the "fraction
   converted" becomes the share of the arriving norm the crystal's Nodes
   book, which decides only whether the rung is reached (it must be at
   least 1 / W). SUPERSEDED in its sinks and its numbers: the leftover
   field goes to no sink, the record ends whole at its click (9.12), and
   the exact counts 874 / 150 are distributions (9.19 item (4b)).
2. The train's end at the clock's quarter (the emitter): computed AT
   LOAD from the declared clock, no Node read: LAWFUL. RETIRED with the
   train (9.17).
3. The emitter's take of its own remnant after its train: a comparison
   of the record's AGE with its train, the emitter's own count, not a
   Node's value: LAWFUL (the clock's comparison, the division with the remainder kept on a count).
   RETIRED: there is no own take (9.12); the emitter's own record clicks
   at its rung (9.17).
4. The polariser: a take per label component in the rotated basis (a
   multiplication, B), no branch: LAWFUL; its click's weights are read
   from the record's label state AT THE CLICK, from above: LAWFUL.
5. The record's completion (the pair's gather waiting for every arm): a
   HOST reading of the board's remaining motion, named as the one
   non-local host step (DESIGN.md 2.1): not a Node's decision, but a
   host's; LAWFUL as named, never a physical dependency. RETIRED: no
   completion (9.12 item 4); a record ends at its click (9.19 (3)).
6. The mirror, the splitter, the receiver's take, the well body: no read
   beyond the six verbs: LAWFUL (the receiver's take RETIRED, 9.12).

### 9.8 Outside the cubes: what an experiment defines (the owner's word of 20:05Z)

**DECIDED HERE, derived.** An experiment defines exactly: (1) THE BOARD,
the torus's extents per axis (the translation group, 1.6); (2) THE
FAMILIES, each its clock and its vacuum pair (light's [1, 1], a massive
kind's [num, den]; 8.1); (3) THE CUBES, each with its written integers
(its pair per family, its coupling, its seed, its axis; the take and the
wheel of this first reading are SUPERSEDED, 9.12 and 9.19 (4)); (4)
THE INITIAL STATE (9.9). Nothing else. THE FACES: an open face on main is a sponge whose Nodes are not on the
board (the row beyond read as 0, the boundary Node's outward Port booked
to the face's Node, a sink under the receiver by name); a shell of
receiver cubes of side 1 with the take [1, 1] on a periodic board is the
same held-at-0 boundary with the same booking. DECIDED: the face's Node
is ADMITTED as the shell's shorthand (the two are the same operation; the
shell would add one body per boundary Node, about 830 on the two slits'
layer, for nothing), and the load check counts the face's Nodes as a
declared set. So an experiment is cubes on a board whose faces are
receivers. SUPERSEDED in its form: the sponge and the shell with the take
[1, 1] retire; an open face is the zero row with the receiver `face` at
the border, last on every ladder (9.19 (3) (a), 9.22 (2)). What lies
between the cubes is the vacuum: the families' own pairs, declared once.

### 9.9 The initial state, over the whole board (the owner's word of 20:05Z)

**DERIVED HERE from 8.7.** At interval 0 every Node's state is the SUM
over the bodies of each body's seed: a well body's seed is its bound
mode's integer profile OVER THE WHOLE BOARD at both levels (8.7: the
tail is not cut at the cube, so "zero outside the bodies" would be wrong
for a well); no other record exists but the emitter bodies' own excited
records (a crystal carries no seed, 9.7; an emitter body's record at
interval 0 is its first excitation, 9.17 (4) item 1 and 9.22 (3), and
its births come later); every remainder is 0. THE LOAD-TIME CONDITION: the board's state at interval 0 equals that
sum Node by Node, exactly (integers), each well's profile equal bit for
bit to the generator's (the body check, 8.7), and no Node carries any
other nonzero amplitude; refused at load otherwise.

**THE WELL AND THE OTHER TOOLS (the owner's word through the Boss,
22:10Z: "a well looking at the fields around it must not collide with
the other lab tools; the initial conditions must close that").** A
correction of wording first: each well's seed is written on ITS OWN
RECORD (every record carries its own rows, 8.6), not summed with other
seeds on one Node's state. The condition then follows in four steps
(DERIVED HERE).

1. WHICH TOOLS ENTER A WELL'S RECORD. A record of the family F moves by
   the one rule with each Node's pair FOR F (8.1). A tool enters F's
   operator only through a pair for F, or through a polar matrix that
   acts on F's labels. The mirror, the splitter, the polariser, the
   crystal and the receivers are LIGHT's materials: they carry no pair
   for a massive family, so they are the vacuum for a matter record, and
   a light tool anywhere leaves the well's operator unchanged. So a well
   can collide only with a body that carries a pair of its own family:
   another well of that family, a transponder's massive body, or that
   family's faces (the zero row, already in the module).
2. NO TOOL READS OR CHANGES THE WELL'S RECORD BY AN OPERATION. By 9.7 the
   only read that decides is a click, and a click reads only a record
   that names the clicking Nodes (the ladder by name): a receiver's E and
   a crystal's click read their named records, and the well's record
   names its own block. The take is removed (9.12). So nothing but the
   rule's material acts on the well's record, and step 1 names that
   material.
3. THE SEED IS THE MODE OF THE COMPOSED WORLD. The standing start is
   exact only for an eigenvector of the operator the record actually
   feels (8.7). That is F's operator with EVERY body's pair for F in
   place, not the well's alone. Two cases:
   - (i) The well's mode is separated from every other mode of the
     composed operator by more than 1 / T (T the run's intervals). Then
     the seed is the composed operator's own mode, computed with every
     body of F in place.
   - (ii) Two wells of one family whose modes are nearly degenerate (the
     same pair and side). The composed modes are the even and odd
     hybrids, split by delta omega, and NO LOCALISED EIGENVECTOR EXISTS.
     The seed is then the well-alone mode projected on the composed modes
     within 1 / T of its own frequency; for two wells that is the hybrid
     combination localised on the well. It moves to the other well at the
     rate delta omega / 2, carrying the norm share sin^2(delta omega T /
     2) over the run. THE CONDITION: that share must be below the
     reading's band.

   On main, `bound_mode` computes each well ALONE ("the other blocks'
   wells not carried"): a defect for every world with two wells of one
   family.
4. NO OVERLAP. One Node is one body's: a body is the material of its
   Nodes (9.1), and two bodies on one Node give that Node two materials
   with no rule to choose between them. REFUSED at load.

THE LOAD-TIME CHECK that follows (the body check, extended):
- (a) The Nodes of every two bodies are disjoint; the first shared Node
  is named in the refusal.
- (b) For each well of family F, the composed operator (every body's pair
  for F) is formed. Its modes within 1 / T of the well's are found, and
  the seed is recomputed as in 3 and compared with the file bit for bit
  at both levels.
- (c) In case (ii), sin^2(delta omega T / 2) is printed (COMPUTATION) and
  the world is refused if it exceeds the reading's declared band.

THE EXPECTED VALUES (COMPUTATION: a dense eigen decomposition of the
chain operator D^(-1/2) (S_6 / 3) D^(-1/2), float, on the host):
- `sagnac_rest.json` (two matter wells of side 12 at x = 700 and 772 on
  the open chain of 3000, T = 8450; RECOMPUTED BLIND at the pair [800,
  801] of 9.19 item (4a), the file's [800, 800] being history): the wells are
  case (ii). omega_b = 0.100217 per interval, delta omega = 4.25 x 10^-7
  per interval and sin^2(delta omega T / 2) = 3.2 x 10^-6, far below the
  band of 3 x 10^-3: ACCEPTED on (c). The composed seed differs from the
  well-alone seed at the amplitude 52428800 by at most 639 units, at 89
  Nodes (at the file's [800, 800]: omega_b 0.089258, delta omega 1.96 x
  10^-7, sin^2 6.9 x 10^-7, 244 units at 72 Nodes). So the file's seeds, computed alone, are REFUSED by (b) until
  they are regenerated on the composed world; the reading does not move
  beyond 7 x 10^-7.
- `deep_well_rest_40.json` with a light mirror cube added anywhere off
  the well: the matter operator is unchanged, so the seed is the same
  bit for bit: ACCEPTED.
- The same world with a receiver cube of side 2 at (80, 80, 0), inside
  the well [44, 84): REFUSED by (a) at (80, 80, 0). At (84, 44, 0),
  adjacent to the well: ACCEPTED.
- Every other world of the list has a single well per family (the
  layer, the redshift, the deep well, the boxes, the light clock, the
  receding index): (b) reduces to main's check, with no change.

### 9.10 The gate reviewer's forbidden branches, and the one rule for each group (the Boss's line of 20:20Z)

the gate reviewer's audit of main's physical path named eleven per-Node branches
that are not group operations. Each group has one rule, DERIVED HERE:

1. THE EMITTER'S OWN NODES (the grace window; its exclusion in the Port
   read; the exemption of an emitting block's sets for its own record;
   the own take; the fresh Port's first-interval case): ONE RULE: the
   emitter's Nodes are Nodes like every other; a record's offer at them
   is booked as at any receiver whose take they declare, and they are on
   the record's ladder as every Node is. WHETHER AN EMITTER MAY CLICK ON
   ITS OWN RECORD follows from the algebra and is not decided: a rule that
   treats a record's own emitter's Nodes differently branches on the
   record's identity, which no element of the group sees (9.1: the tool's
   action is equivariant; a record's identity is not a group object); so
   an emitter MAY click on its own record, with the share its Nodes book.
   The driven Nodes' amplitude is imposed by the emitter's own clock
   (the translation); their Ports book the offer that arrives through them from the
   neighbours, as every Node's do. The test value: the share of a record's
   norm booked at a one-Node emitter with the take [1, 1] on a free board
   (a COMPUTATION owed with DESIGN.md section 5's Port form; MEASURED ONLY
   until then), and 0 at an emitter declared with the take [0, 1].
   SUPERSEDED: the take retires (9.12) and the owed share with it; the
   emitter's own record clicks at its own rung by the flux (9.17, 9.19
   (3)).
2. THE TAKE PAIRS (two take pairs chosen per Node by set membership): ONE
   RULE: one take pair per Node, the Node's material (section 9.2's
   receiver), whatever sets name the Node. SUPERSEDED: no take pair
   (9.12); one material per Node stands.
3. THE TABLE FORMS (the splitter's Node that takes and books nothing; the
   table body acting on one family only): RETIRED with the table forms
   (the no-table rule; the material tools of 9.2).
4. THE BODY'S READ (the cavity's record zeroed outside its Nodes every
   interval; two forms of a body's read chosen by absorbing or taking):
   ONE RULE: one read for every body (its pair, rule 2; the take is
   removed, 9.12); the
   cavity's boundary is a DECLARED ZERO FACE made material: a gap pair of
   the record's own kind around the Nodes, whose band admits no clock of
   the mode (8.1), so the mode's amplitude decays outside as exp(-kappa)
   per Link, kappa (the decay constant per Link) given by cosh kappa =
   6 (den / num) cos omega_b - 2 on a chain; the declared zero
   is the limit of a deep gap, and the leak per Node e^(-kappa) is the
   test value (computed per world from the cavity's pair).
5. The arm's half-space cut dies with the two-arm emitter (record 1818).

### 9.11 The first tool through the gate: the polariser's fix (PR 1139, polariser-fix at 32745860), read against this chapter

Read line by line: `TableBody` gains the half-angle pair; `_split_table_offers`
forms the weights from `joint_weights` with one body on the record's
labels and moves J(+)^2 / (J(+)^2 + J(-)^2) of each interval's booked
gain to the + Node with the remainder kept. THE ALGEBRA, for a record of
ONE arm: CONFIRMED (the weights are 3.6's projection of the record's label
state on the body's rotation, the bilinear form then the square; the division verb
D with its remainder; the first rung the click). THE DEFECTS: (a) `if
body.family != live.family: continue` is a branch on a family (Reviewer
3's item 28, 9.10 rule 3); (b) `if norm:` is a dead branch (J(+)^2 +
J(-)^2 = n_s times the state's norm, never 0), to be removed; (c) `if
gain:` is a host skip with no effect (the division of 0 with a remainder
below the wall gives 0): lawful as bookkeeping; (d) FOR A RECORD OF RANK
2 the one-body weights on the JOINT labels are a coherent sum over the
other arm's bit, which is not the arm's reduced state: the lawful weight
is the partial trace, R(o) = SUM over the other arms' bits b of (SUM over
the labels l with that bit b of w_l U_s[o][bit of l on this arm])^2; with
HV + VH at s = 512 the code books all of an arm's offer on the + Node
where the reduced state books half; the Bell counts are not moved (the
joint gather reads the whole offer), but the books are wrong; (e) the
tool is still the table form, which the no-table rule retires (the
absorbing material of the lab tools' specification, section 2). VERDICT:
the fix is the algebra for one-arm records and may merge as the bug's fix
with (a), (b) and (d) corrected; the tool's final form is the material
one.

**CONFIRMED at polariser-fix e99b7091 (2026-09-24, the physicist's
corrected head).** The three corrections read line by line:
- (a) `table_bodies_by_family` is indexed by the record's family as data,
  filled from each body's own declaration, with no branch on a family.
- (b) The guard on the weights' sum is removed.
- (d) `channel_weights` groups the labels by their bits on the other arms
  (the key label & ~(1 << arm)). The pointer is coherent within a group
  (the bilinear form) and the weight is the sum over the groups of the squares: the
  partial trace. An arm of HV + VH gets (65522, 65522) at s = 512,
  (65536, 65536) at s = 0 and (65773, 65773) at s = 256, which is 2 x
  181^2, 2 x 256^2 and 237^2 + 98^2 on the tables.
- `if gain:` remains the lawful host skip.

tests/test_detector_law_tables.py passes on that head (15 passed). The
gate: CONFIRMED as the bug's fix. Under 9.14's adopted axis, the pair
(a, b) enters `channel_weights` in place of (C', S') with no other
change.

### 9.12 The take and the click (the owner's word of 21:30Z through the Boss: "the receiver's take is defined by an operation of the group; we named it E, I think; check it")

**Three operations at a receiver, told apart (DERIVED HERE from 2.5, 3.1,
8.6 and 8.8).** (i) THE EVALUATION E (2.5): ev: Z[Z_N] -> Z[zeta_N], a
ring homomorphism; with the norm (B) and the rung (D) it READS the
record at the receiver's Nodes and changes nothing on the board. (ii) THE
CLICK'S ACTION (3.1; POSTULATES.md section 10): the record ENDS at the
detector, all its rows everywhere, and the detector's own record
changes: the one deletion of the law (8.8). (iii) THE TAKE (8.6's last
paragraph): at every interval the declared Nodes' amplitude of the record
is held at 0 and its motion booked: a projection of the Inside, a
diagonal map with a 0 on those Nodes (the bilinear form with a degenerate matrix),
NOT invertible. THE TAKE IS NOT E: E reads and leaves the Inside a
bijection; the take removes amplitude from the Inside before any click.
And it is not the click: the click deletes a record once and whole; the
take deletes part of every record that passes, every interval. By 8.8
the Inside is a bijection and the click is its one deletion; the take is
the one other loss, which 8.6 already names "a declaration of the world,
not the law's". Under the owner's rule that every operation in the Nodes
is an operation of the group (9.5), a projection that no group element
performs is not admitted into the law.

**The take can be removed, and what replaces it (DERIVED HERE).**

1. A record whose click's weights are COMPUTED from its state, not from
   booked offers (the joint gather's R = J^2; the polariser's
   projection; a ladder of one named receiver), needs no take: its click
   is E then D at the first rung (the line at the rung, the receiver by
   name), and at that interval the click's action DELETES THE RECORD
   WHOLE, its leftover field included. The leftover field does not go to
   sinks; it ends with the record. The crystal's arriving record (9.7
   (b)) and the pair's gather are of this kind.
2. A record whose click chooses among SEVERAL Nodes by their booked offers
   (a screen's pixels: the two slits, de Broglie's fringes) needs the
   offers at a CLOSE. Without a take the lossless field is read by E at
   the screen's Nodes as it passes (a clock body is read and not taken,
   8.6: "light passes on, and the click needs no sink"), and the close is
   a COUNT ON THE RECORD'S OWN CLOCK (its age reaching a declared close,
   lawful by 9.5): the offers booked up to that age form the ladder, the
   residue chooses the Node, and the click deletes the record. The world
   must be large enough that no reflection from a face reaches the screen
   before the close (a timing condition per world, from the distances and
   c, a load check). SUPERSEDED by 9.19 (3) (a): the screen's ladder is
   read cumulatively at every interval by the flux and the record clicks
   at the first crossing; there is no close on a record's age.
3. THE FACES: an open axis's face is the segment's border (1.6); with no
   take, the row beyond read as 0 is a closed face that reflects (the
   delay 3.547 intervals of the lab tools' specification 11.5), and it is
   harmless exactly when every click happens before the first reflection
   reaches its receiver (items 1 and 2). No face and no receiver then
   needs a take pair; the shell of receiver cubes (9.8) needs none.
   SUPERSEDED by 9.19 (3) (a): an open face is the zero row with the
   receiver `face` at the border, last on every ladder (Highlights'
   record 15, kept); nothing reflects at an open face, what leaves clicks
   there.
4. THE COMPLETION (the host's reading of a record's remaining motion,
   DESIGN.md 2.1) RETIRES: a record ends at its click (item 1) or at its
   close (item 2), both lawful. A record that never reaches a rung before
   its close ends at the close with the ladder of the offers it booked;
   with no offer at all it ends unread, which the books count as its own
   row (a record with no click), never as "escaped" into a sink. THE
   CLOSE SUPERSEDED as in item 2: a record ends at its click, at the face
   receiver at the latest (9.19 (3) (a)).

**What changes in the counts and the books (DERIVED HERE).** The Bell
counts: none (the weights are computed; the first rungs unchanged,
because the first rung is reached by the direct front before any
reflection on the Bell layer: the faces are at least 11 Links behind every
receiver along its line, 11.3 of the lab tools' specification). Malus:
none (computed weights). The two slits and de Broglie's fringes: the
screen's offers up to the close equal the offers the sinks' form booked,
provided no reflection arrives before the close; their pins stand on
that condition, which each world's generator checks. The books: the
Inside's content is conserved exactly until the clicks (8.8's bijection);
"absorbed" is the clicked content alone; "escaped" retires, replaced by
"ended unread" for a record that closes with no offer. The one input the
algebra did not produce (the take, 9.16 item 3) is thereby removed.

### 9.13 The emitter as the transpose of the click (the owner's word of 21:40Z: "perhaps the emitter is the reverse: a click produces the emitter")

**DERIVED HERE.** The click's evaluation on the tables is the linear map
**E**: Z[Z_N] -> Z^2, f -> (SUM over p of f_p C[p], SUM over p of f_p S[p])
(2.5). Its transpose for the inner product in which the [p] are
orthonormal is **E**^T: Z^2 -> Z[Z_N], (X, Y) -> SUM over p of (X C[p] + Y
S[p]) [p]: from a number back to a record, the real part of a character
on the phase circle. A lamp's drive is exactly this, sampled by its own
clock: a_now(t) = A C[phase(t)] at its Node is **E**^T applied to (A, 0)
and read at the clock's phase (1.7); spread by the split to the six
neighbours, the birth is invariant under the Node's stabiliser G_48, the
projector onto the trivial representation (9.4). And **E** **E**^T =
[[SUM C^2, SUM C S], [SUM C S, SUM S^2]] = (N / 2) 256^2 **I** up to the
tables' rounding (the characters' orthogonality on Z_N): THE EMITTER IS
THE RECEIVER'S TRANSPOSE, its right inverse up to the scale (N / 2) 256^2
and the rounding. ITS TRIGGER IS A CLICK OF ITS OWN RECORD: an emitting
block births one record per cycle of its own mode, the cycle counted by
its own clock, the evaluation of its own record at its rung (8.6, the
block's clock): exactly "a click produces the emitter". A lamp is the
degenerate case: its own clock is its rate's accumulator (the translation) with no
record behind it; a lamp that must be read so is a block emitter. So THE
RECEIVER IS **E**, THE EMITTER IS **E**^T, AND THE CRYSTAL IS **E**
(the arriving record's click at its Nodes) THEN m^T (the arriving clock
split into the two born clocks, 9.2) THEN **E**^T (the pair's birth): EXACT
as the path of the data a click lets through, namely the clock (the
energy, through m^T) and the residue u (9.7 (b)); the arriving record's
amplitude and phase are not passed (no read), the born amplitude is the
crystal's own declared number and its phase starts at the born clock's
zero. What it changes in the code: nothing for a block emitter (its
births per cycle of its own clock are this); for a lamp, only the naming
(its rate's count is its clock); for the crystal, its births fired by the
arriving record's click, not by its own clock (9.7 (b)); the train, the
wheel and the residue were unchanged in this reading. SUPERSEDED: the
train by the born profile (9.17 (4)), the wheel and the residue by the
law's own remainder (9.19 (4)).

### 9.14 The polariser's angle: an element of the wheel's group, with no table (the owner's word of 21:40Z, and of 2026-09-24 17:27Z through the Boss: "about the general angle of the polariser, perhaps we do not need it at all")

This section replaces the earlier reading, in which the half-angle tables
were kept as a declared rounding. The question: can every polariser
setting the measured experiments need be an operation of the algebra, with
no declared table? Two candidates are tested: (a) the setting as an
element of the wheel's group Z_N; (b) the setting as an element of the
Nodes' group ring. The result: (a) is exact and keeps every pin; (b) is
exact only on the lattice's rational axes, and it never reaches 22.5
degrees.

**The Nodes' own group gives no Bell violation (PROVED HERE).** A
reflection of G_48 that keeps the record's path exchanges the two hands
(the hand is a pseudoscalar, 9.3). The elements that fix the path act on
the plane across it only through quarter turns and the reflections of
that plane. So the polarisers in the group sit at multiples of 45 degrees
(s a multiple of N / 4, with the angle theta = pi s / N). Every
correlation E(a, b) = cos 2 (theta_a - theta_b) is then 1, 0 or -1, and
the four terms of CHSH give abs(S) <= 2. THE STEP WRITTEN OUT (Reviewer
4's line: S = 3 was not excluded by the text): let A, A', B, B' be twice
the four angles, multiples of 90 degrees, so that every term is the
cosine of a multiple of 90 degrees, in {-1, 0, 1}, and note the identity
(A - B) - (A - B') - (A' - B) + (A' - B') = 0. If one term is 0, its
difference is an odd multiple of 90 degrees, so by the identity an odd
number of the four differences are, and at least two terms are 0:
abs(S) <= 2. If no term is 0, every difference is a multiple of 180
degrees and by the identity an even number of them are odd multiples,
so the four signs have the product +1; S = 4 needs the signs (+, -, +,
+), the product -1, and S = 3 needs a 0: both excluded, and S lies in
{-2, 2}. COMPUTED beside it: the 4^4 = 256 settings give max abs(S) = 2.
So S above 2 needs something beyond the Nodes' own group.

**(b) The Nodes' group ring: exact, but only on rational axes (PROVED
HERE).** The group ring Q[G_48] acts on the plane across the path through
the dihedral group of the square, D_4: I, **Z** = diag(1, -1) (the
reflection in the H axis), **X** (the reflection in the diagonal, which
exchanges H and V) and the quarter turn **X** **Z**. Their rational span is
all of M_2(Q), the 2 x 2 rational matrices. Every element of the ring
therefore acts by a RATIONAL matrix, because G_48's characters are
integers and this plane is realised over Q with entries 0 and +-1. A
polariser is an orthogonal rank-one projector. The rational ones are
exactly **P** = **u** **u**^T / abs(**u**)^2 for an integer axis **u** =
(a, b); this is the lattice-axes result of the earlier reading. The
projector at 22.5 degrees has the entries (2 + sqrt 2) / 4 and sqrt 2 /
4, which are irrational, so it is NOT in the ring: "22.5 degrees through
the ring" is impossible exactly. What (b) does give is S = 14 / 5 exactly
on the axes (1, 0) and (1, 1) for Alice and (2, 1) and (1, 3) for Bob,
with R(+, +) = (**u**_A . **u**_B)^2 and R(+, -) = (**u**_A x
**u**_B)^2 (COMPUTATION; the counts at W = 2048 are 819/205 and 102/922,
S = 717 / 256, and S = 14 / 5 exactly at W = 2560). That result stands
as a special case, but it moves Bell's pin, and Malus's angles are not
rational axes.

**(a) The wheel's group: the setting is a translation (DERIVED HERE).**
Read the label pair in the hands (circular) basis, with `label_hands`
declared (LAB_TOOLS.md 11.6). A turn of the polarisation plane by theta
multiplies the two hands by exp(-i theta) and exp(+i theta). Up to a
common phase, which cancels in every weight, that is the RELATIVE
translation by s on the wheel: 2 theta = 2 pi s / N, so the setting s
is the element x^s of Z_N acting on one hand. The group the polarisers
live in is the dihedral group D_N = Z_N x| {hand exchange}: the wheel's
translations together with the Nodes' hand exchange. Both factors are
already in the algebra (the wheel, chapter 2; the exchange, 9.3), so
nothing is declared but the integer s. G_48's quarter turns are the
subgroup s in {0, N / 4, N / 2, 3 N / 4}. THE WHEEL'S GROUP IS WHAT GOES
BEYOND THE NODES.
- The polariser at s is the reflection r_s = (hand exchange) then x^s in
  D_N, and its pass projector is the ring element (1 + r_s) / 2. In the
  hands basis (+, -) the channel rows have ONE GROUP ELEMENT PER ENTRY:
  the pass row (x^0, x^(-s)) and the block row (x^0, x^(N/2 - s)), the
  second because -x^(-s) = x^(N/2 - s) under the cancel (2.3). Each row
  has the norm 2, the same for both channels, and the common factor
  drops out of every ladder as n_s does today. The half angle is gone:
  in the linear basis the angle enters as cos theta and sin theta, while
  in the hands basis it enters only as the full relative phase 2 theta,
  a whole number s of steps.
- The joint pointer is J(o_A, o_B) = SUM over the joint labels of w times
  the product of the two rows' entries: an element of the group ring
  Z[Z_N], formed with the ring's convolution (`ring_product`). The Node's
  weight is R = J J*, with J* the involution x^p -> x^(-p) (the complex
  conjugate under ev). R is a REAL element of Z[zeta_N], and the cancel
  x^(N/2) = -1 reduces it exactly (2.3; for N a power of two, the
  cancel IS ev). For HH + VV = (+-) + (-+) and k = s_A - s_B:
  R(+, +) = R(-, -) = 2 + x^k + x^(-k) and R(+, -) = R(-, +) = 2 - x^k -
  x^(-k). The TOTAL is the integer 8 at every setting, because the
  channel projectors sum to the identity. E(a, b) = ev(x^k + x^(-k)) / 2
  = cos(2 pi k / N), exactly.
- Bell's settings s = 0 and 512 for Alice and s = 256 and 768 for Bob, at
  N = 2048, give k = -256, -768, 256 and -256. In the ring, S = 3 cos(pi
  / 4) + cos(pi / 4) = 2 sqrt 2 = ev(x^(N/8) + x^(-N/8)) EXACTLY: the
  Tsirelson bound as an element of Z[zeta_N]. S ABOVE 2 FOLLOWS WITH NO
  DECLARATION beyond the integers s.

**The click: the one place a weight becomes a count (PROVED HERE).** The
rung compares 2 T u + T <= 2 W C_k (`cell_of`). Here T is an integer and
C_k a real element of Z[zeta_N], so the rung is the NEAREST INTEGER TO AN
IRRATIONAL. That value is unique and never a tie. It is main's own
rounding at the rung, the same one that makes 14 / 5 exact only at W a
multiple of 20; it is not a declared table. The comparison is exact with
integers alone, no root and no float. For N = 2^m, the number c_m = 2
cos(2 pi / 2^m) satisfies c_m^2 = 2 + c_(m-1), with c_2 = 0. An element
p(c_m) splits as a + b c_m, with a and b one level down, and the sign of
a + b c_m follows from sign a, sign b and, where these differ, sign(a^2 -
b^2 (2 + c_(m-1))). The recursion ends at the integers. Its depth is
log2 of the order of the element x^k, minus 2: depth 1 for Bell (the
order 8), where the test is one comparison of squares: (16 u + 8 - 4 W)
<= 0 or (16 u + 8 - 4 W)^2 <= 8 W^2. Malus's settings have the depths 0,
2, 3 and 2. The work is fixed for a fixed wheel but grows exponentially
with the depth: a general s at N = 2048 has a depth of up to 9 (this is
the host's cost, reported separately).

**The pins do not move (COMPUTATION, exact sign recursion against the
current tables, checked against floats on 300 random elements with no
mismatch).**
- Bell at N = W = 2048: the counts are 874, 150, 150, 874 at every pair
  of settings (150, 874, 874, 150 at E = -cos(pi / 4)), the same as the
  half-angle tables give, so S = 181 / 64 on the counts (2 sqrt 2 in the
  ring).
- Malus at N = W = 256 with H arriving and R(+) = 2 + x^s + x^(-s) of
  the total 4: the counts are 128, 246, 199 and 177 at s = 64, 16, 40
  and 48, the same as today.
- So the owner's open choice between the tables (181 / 64) and the
  lattice axes (14 / 5) DISSOLVES: (a) keeps 181 / 64 with no table.

**Which is exact, and the verdict.** Both are exact. (a) is exact in the
ring: every setting s is a group element, the weights are elements of
Z[zeta_N], ev is the cancel, and the only rounding is the rung's. (b) is
exact in the rationals, but only on the rational axes: it gives S = 14 / 5
and reaches neither 22.5 degrees nor Malus's angles. RECOMMENDED: (a).
It needs no new object, keeps every pin, and retires the half-angle
tables from every polariser path. (b) stays admissible for a world that
declares integer axes.

**ADOPTED: (b), the integer axis (the Boss's order of 2026-09-24, 22:10Z,
on the owner's hint "perhaps we do not need the general angle at all").**
A polariser declares its AXIS as an integer vector **u** = (a, b) of the
plane across the path; the setting s and the half-angle tables retire.
The engine's change is one line, because `joint_weights` already takes a
pair (C', S') per body and forms U = [[C', S'], [-S', C']]: it takes
(a, b) in its place. The weights R = J^2 are then exact integers, the rung
is unchanged, the sign recursion of (a) is not needed and no ring weight
enters the ladder. The steps that belong to (a) alone (1, 2 and 3 in the
list below) do not apply. The pins under (b) are in 9.16 (4). (a) stays
derived, for a world that needs an angle that is not a rational axis;
none of the measured experiments needs one.

**What disappears from the code (read at 9b8554e1's base).**
- `amplitude.half_angle` and the tables of 2N behind it, at its four call
  sites: `DetectorLaw.joint_weights` (through `_click_pair`),
  `_table_body` (the pair C'^2, S'^2 and n_s = C'^2 + S'^2 in
  `TableBody`), the amplitude layer's rotation (`amplitude.py`, the
  `half_angle(s, self.steps)` line) and `nature_beam.py`'s rotation.
- The norm n_s and the assertion **U**_s^T **U**_s = n_s **I** (3.6)
  become the fixed row norm 2.
- The polariser keeps no remainder: its rows are group elements, so it
  applies only the ring's verbs (a translation and a sum), with no
  division.
- What STAYED at the time of writing: `phase_cosines` and `phase_sines`
  where ev was still read through the rounded circle (the Z[i] pointers
  and `cmul`, the detector law's cosine and sine arrays, `world.py`'s
  sine table). SUPERSEDED (the owner's word of 23:00Z, "if it is not used,
  throw it out; no formulas on the board"): with the flux as the reading
  (9.19 (3)), the axes as integers and the born pair as the world's
  integers (9.17 (6)), THE ENGINE OF THE FIFTEEN CARRIES NO TABLE; the
  readers that turned levels into phases (`read_phase`, `nearest_phase`)
  are host tools outside the engine, and `core.phase` stays only for them
  and for the generator.

**What Nature24 must change.**
1. `joint_weights`: take the rows (x^0, x^(-s)) and (x^0, x^(N/2 - s))
   per body, form J with `ring_product` in place of the Z[i] product of
   the table rows, and form R = J J* reduced by the cancel.
2. `cell_of` and `rungs`: accept the weights as real elements of the
   ring, with an integer total, and compare them by the sign recursion
   above in place of the integer product.
3. `TableBody` and `_split_table_offers`: the split share becomes the
   ring element (2 +- (x^s + x^(-s))) / 4. An integer count cannot carry
   an irrational share with a kept remainder, so the split moves onto the
   ring pointer (the per-hand amplitude of 9.16 (2)), or the body's books
   are compared with the click only within the rung's margin (LAB_TOOLS.md
   2.3).
4. The world file: the settings stay integers s, and `label_hands` is
   declared wherever a polariser acts.
5. The tests: the pins stay (874/150/150/874 with S = 181 / 64; Malus
   128, 246, 199, 177). Tests that pin the tables' integers C'[s], S'[s]
   or n_s retire with the tables. A new test pins the sign recursion on
   inputs, their expected signs and an edge case: the zero element, and a
   u exactly at a rational rung.
The gate (9.5) reads the new `joint_weights` line by line against this
section.

### 9.15 Momentum on the board's own values (the owner's words of 21:40Z and 22:30Z, record 1856 of 2026-09-25 on the Israel clock; REVISED at 22:30Z: no book at a held body)

THE OWNER'S WORD (22:30Z, translated): "when the photon moves in the
crystal the momentum IS conserved, because the crystal's Nodes change ...
after we put the values into the board, the momentum is conserved." The
earlier reading (a book at a held body) is WITHDRAWN. The reading below
has four parts.

**(i) The theorem on a homogeneous board (PROVED HERE).** Where every
Node carries the same pair, the rule commutes with every translation
(1.6). So the rule maps each character of the torus to itself: the
record's content in each wave vector **k** is advanced by that character's
own clock and never moved to another **k** (8.1's band). The records'
total content in each **k**, and with it the total momentum SUM over **k**
of **k** times that content, is therefore the same at every interval.
Nothing is booked: the values carry it.

**(ii) Where a tool's Nodes carry it (DERIVED HERE, from 8.11 and 8.3
(v)).** A tool's material breaks the translations at its Nodes, and there
the field's momentum changes (a reflection sends k_perp to -k_perp). On
the board the difference is carried by the one value that a body has
besides its material: ITS OWN RECORD'S MOMENTUM VECTOR, advanced by the
push (8.11). The push is the stress of light's field summed at the body's
outer Ports (the merge), divided with the remainder kept (the division with the remainder kept), and it
steps the body's record, by the hop, when the accumulator passes its
wall (the translation). These are the law's own verbs on the body's own values:
NO BOOK. "The crystal's Nodes change" is this: the body's record moves
by the push it received.
- At the crystal: before the click the arriving record's stress at the
  crystal's outer Ports enters the crystal's vector. At the click the
  arriving record ends. The pair is born by **E**^T with no heading, and
  the birth's own push on the crystal is 0 on the average, because the
  six Port vectors of the orbit sum add to 0 (PROVED HERE: SUM over the
  six Ports of the unit vectors is 0). So the board's total before is the
  crystal's vector plus the arriving record's, and after it is the
  crystal's new vector plus the pair's mean of 0: equal.
- At the mirror: the reflected record's stress at the mirror's Ports
  steps the mirror body's vector by twice the normal momentum.

**(iii) What cannot carry it, said plainly.** A body declared `fixed` has
its step suppressed: its vector is held at 0. So a FIXED BODY'S NODES
CANNOT CARRY MOMENTUM UNDER THE LAW, and wherever a fixed body reflects,
converts or absorbs, the board's total changes by the difference.
Momentum is conserved on the board exactly when EVERY TOOL IS A FREE BODY
WITH ITS OWN RECORD (a block of a massive kind carrying the tool's light
material, the transponder's form, section 8 of the specification;
ADOPTED, record 1875, 2026-09-25 on the Israel clock: of the HOLDER
family, BOUND, 9.18 (2)), held
in place only by its mass: its velocity after a push is the push over
its mass. A body of mass M that reflects a photon of momentum k moves
at 2 k / M Links per interval afterwards, so it drifts 2 k T / M Links
over T intervals. A crystal
or mirror of a massive kind that drifts less than one Link over the run
is "at rest" to the board's own grain.

**(iv) Exactness.** The push's accumulator and its step are PROVED as
identities (8.11). That the stress at the Ports equals the field's
momentum flux is CARRIED (8.11: a declaration of the design, not of the
law). So on the GameBoard the total over the records' characters and the
free bodies' vectors is conserved to that declaration. It is exact in
(i), where no body intervenes.

WHAT CHANGES. The tools of the specification become free bodies of a
massive kind carrying their light material. Their `fixed` flag retires
from the tools, and their mass is written so that the drift over the run
is below one Link (the specification's A.3, A.4, A.5 and A.6). Nothing
changes in any count: the counts are computed weights or first rungs, and
a drift below one Link moves no Node. MISSING: a proof that the stress is
the flux on the board, not only in the continuum.

### 9.16 What was missing, closed item by item (the Boss's order of 2026-09-24, 22:10Z: "close, do not bring the owner questions")

**(1) The whole sum m^T on one record: an engine form (DERIVED HERE).**
A record's clock becomes a finite list of COMPONENTS, each with its own
clock pair on its arms and an integer weight: arm 0 at a and arm 1 at p -
a, for a in the crystal's declared WINDOW [a_lo, a_hi] (its material, both
clocks inside their families' propagating bands, 8.1). One component is
main's record, unchanged. The generic step: each component is propagated
by the one rule at its own clock, and the record's offer at a Node is the
sum of the components' offers (linearity; distinct clocks are orthogonal
characters, so the norms add over a full period). The click reads the
record's offer; the joint gather's weights read the label state only
(3.6), so THE COUNTS DO NOT DEPEND ON THE COMPONENTS. The identity behind
it: m(m^T([p])) = N [p] on Z[Z_N], and over a window of w components
m(SUM over the window) = w [p] (PROVED HERE: each term [a] (x) [p - a]
multiplies back to [p]). None of the measured experiments' pins reads it; it is the
form for nature's broad spectrum of the pair. The engine form and its
unit tests: [the lab tools' specification](designs/lab_tools/LAB_TOOLS.md),
section 12.1.

**(2) One amplitude per label on every record: an engine form (DERIVED
HERE).** Every record carries its rows per label value of each arm (two
rows per arm for the label pair). The one rule acts on each label row
alike, because the paces of the two labels are equal in every body
(9.3). A POLAR BODY with the axis **u** = (a, b) applies at its Nodes the
integer matrix **M**_u = [[a, b], [-b, a]] to the pair of label rows
(the bilinear form). There is no division: the common factor abs(**u**)^2 scales the
record's norm, as n_s did, by the identity (a x + b y)^2 + (-b x + a y)^2
= (a^2 + b^2)(x^2 + y^2) (Brahmagupta's, exact on integers). For a record
of rank 2 the arm's weights are the partial trace (9.11 (d)), which the
per-label rows give without a new rule. The unit tests are in the
specification's section 12.2.

**(3) The take: REMOVED (9.12).** CLOSED.

**(4) The polariser's angle: the integer axis, ADOPTED (9.14).** The
setting s and the half-angle tables retire. THE PINS, written before any
run (COMPUTATION: main's `joint_weights` with (a, b) in place of (C', S')
and main's `rungs`):
- BELL. The pair's state is HV + VH, the crystal's (item (5)). Alice's
  axes are (1, 0) and (1, 1). Bob's are (1, 2) and (3, 1): the reflections
  in the diagonal of (2, 1) and (1, 3), because the state HV + VH is HH +
  VV with Bob's labels exchanged. For the lamp's HH + VV on main's files,
  Bob's axes are (2, 1) and (1, 3) and the counts are the same. The
  weights (++, +-, -+, --) are:
  - (1, 0) with (1, 2): 4, 1, 1, 4 of 10, so E = 3 / 5.
  - (1, 0) with (3, 1): 1, 9, 9, 1 of 20, so E = -4 / 5.
  - (1, 1) with (1, 2): 9, 1, 1, 9 of 20, so E = 4 / 5.
  - (1, 1) with (3, 1): 16, 4, 4, 16 of 40, so E = 3 / 5.

  S = 3 / 5 + 4 / 5 + 4 / 5 + 3 / 5 = 14 / 5 EXACTLY at every wheel W that
  is a multiple of 20. THE PIN AT W = 2560 (the wheel [1, 2560], N = 2048
  unchanged): 1024, 256, 256, 1024; 128, 1152, 1152, 128; 1152, 128, 128,
  1152; 1024, 256, 256, 1024. So S = 14 / 5 = 2.8 (DETECTOR), each
  marginal exactly 1280 of 2560, with no band: a differing count is an
  engine defect. RETIRED with the declared wheel (record 1872): the band
  is binomial, 9.19 item (4b). At W = 2048 the same weights give 717 / 256 (the rung's
  rounding), which is why the wheel moves to 2560. Nature's optimum, 2
  sqrt 2 = 2.828, is not a pin.
  THE HOST'S FORM (the physicist's cost of 19:00Z: about 1.7 ms per
  record-interval on the Bell layer, about 6 hours at 2048 records): the
  counts are deterministic over the wheel, so the smallest exact wheel,
  W = 20, gives the SAME S = 14 / 5 with 20 pair records per setting.
  The counts are 8, 2, 2, 8; 1, 9, 9, 1; 9, 1, 1, 9; 8, 2, 2, 8, with
  marginals exactly 10 (COMPUTATION, main's `rungs`), in about 1 / 100 of
  the host time. Any multiple of 20 is the same pin scaled. ADOPTED by
  the Boss at 00:05Z: THE BELL WORLDS ARE PINNED AT W = 20. RETIRED by
  record 1872 (the residue from the law, no declared wheel): the pins are
  distributions, n = 100 pair records per setting, 9.19 item (4b).
- MALUS. H arrives; the + Node is along the axis, with the share a^2 /
  (a^2 + b^2). The axes, chosen as the integer vectors nearest the four
  settings of the list:
  - (1, 1) at 45 degrees: 1 / 2.
  - (5, 1) at 11.31 degrees: 25 / 26.
  - (15, 8) at 28.07 degrees: 225 / 289.
  - (3, 2) at 33.69 degrees: 9 / 13.

  THE PINS AT W = 256 (the wheel [159, 256] as the files stand): 128, 246,
  199 and 177 of 256 on the + Node (DETECTOR). RETIRED as exact counts by
  record 1872: the expected values 128.0, 246.2, 199.3, 177.2 with their
  binomial bands, 9.19 item (4b). These are the rung's
  nearest integers to 128, 246.15, 199.31 and 177.23, none of them a tie,
  and they are the list's numbers, unmoved. Each share is exact at its own
  wheel: W = 2, 26, 289 and 13, or together at W = 7514, with 3757, 7225,
  5850 and 5202.

**(5) The crystal's same-hand weights a and b: the crystal's MATERIAL,
with a = b = 0 (DERIVED HERE).** Beyond c = d (9.3) the symmetry fixes
nothing. The half-turn about the arriving axis exchanges the arms and
changes the sign of both labels, and gives c = d again. The quarter turn
carries the arms out of the placement's plane, so it relates channels of
other headings. So a and b are free. What the algebra does fix is WHICH
STATES ARE MAXIMALLY ENTANGLED: the coefficient matrix [[a, c], [c, b]]
must be a multiple of an orthogonal matrix, and that holds exactly when
b = -a (any c) or when c = 0 and a = b (PROVED HERE: a c + c b = 0 and a^2
+ c^2 = c^2 + b^2). A state outside those two families (for example a =
b = c, the product state (H + V)(H + V)) lowers S. THE VALUE WRITTEN IN
THE CRYSTAL'S WORLD FILE is a = b = 0 and c = 1, the branches [[1, 1],
[2, 1]] (label bit j is the value on arm j). The reasons:
- It is maximally entangled.
- It is the smallest material: one nonzero integer, the channel that
  symmetry already fixes.
- It is the owner's channel of record 1821.
- The Bell pin in (4) is computed for it.

**(6) The cone: ACCEPTED as not derivable (9.3, 9.7).** The pair's
headings are the placement's: the receivers are placed where the pair
goes (LAB_TOOLS.md 11.3).

### 9.17 The only operation is the click, and the emitter clicks (the owner's word of 22:30Z: "in principle we cannot do any operation on the Nodes except to produce a click, which really takes out a record. Verify whether the emitter must also make a click")

**(1) The form of every tool (DERIVED HERE, from 8.8 and 9.12).** The
Inside is a bijection and the click is its one deletion (8.8). So a
tool's action is the law's own advance (the rule **R**, with the tool's
material, and the push of 9.15) PLUS AT MOST A CLICK. The click may have
a birth as its other side (9.13): **E**^T writes the born record's two
levels once, at the click's interval, and from then on only the law
advances it. Read against that form:
- THE RECEIVER: a click. FORM MET.
- THE MIRROR, THE SPLITTER, THE FACES: the law's advance on a gap or on
  the zero row. No click. FORM MET.
- THE POLARISER: the law's advance with **B**_u on the label rows
  (9.16 (2)), then its receivers' clicks. FORM MET once the per-label
  rows are built. The table form (the split of booked offers with a kept
  remainder) is an operation on the books and not the law's advance: it
  RETIRES (9.11 (e)).
- THE CRYSTAL: the arriving record's click, then a birth. FORM MET.
- THE WELL AND THE TRANSPONDER: the law's advance, and its own record's
  clicks. FORM MET.
- THE EMITTER, as main has it: NOT MET, twice over. First, the lamp's
  births come from a rate accumulator with no record behind them, so a
  record begins where none ends. Second, `_drive` writes the cosine value
  at the emitter's Node every interval of the train (the translation on a Node
  that the law does not advance), and it overwrites what arrives there
  (the physicist's observation of 18:50Z).

**(2) The emitter must click (DERIVED HERE).** One quantum, one click
(8.6) and the bijection (8.8) together say that the number of quanta
changes only at a click. A birth adds one, so A BIRTH MUST BE THE OTHER
SIDE OF A CLICK THAT ENDS ONE: the emitter's own excited record ends as
the new record begins. This is the atom's transition: **E** on the
emitter's own record, then **E**^T. Its own clock's rung alone is not
enough, because a count on a clock with no record behind it ends nothing
(it is lawful as a count, 9.5, but it creates a quantum from nothing).
The algebra's form is therefore THE BLOCK EMITTER: a body with its own
record (a well of a massive kind, 8.3) whose record clicks at its own
rung. That click ends the record, and the photon's record is born at the
same interval on the emitter's Nodes.
- THE BORN RECORD'S VALUES are written once, at the click, by **E**^T:
  the born clock's character on the emitter's Nodes at both levels. They
  are never driven afterwards.
- A NARROW TRAIN IS A LENGTH, NOT A DURATION: a record of n periods is
  written over n wavelengths of emitter Nodes in a line (its direction
  the line's, a placement, 9.6). On a single Node the born record is
  broadband.
- The emitter's Nodes are Nodes like any other before and after the
  birth, and an arriving amplitude passes them under the rule. This
  answers 9.10 item 1 and the physicist's question: nothing is
  overwritten.

**(3) What changes in the code.**
- `_drive` retires. The lamp's rate accumulator retires as a source of
  births. `train` becomes the born record's extent on a line of emitter
  Nodes.
- A birth is fired only by a click: the emitter body's own record's rung,
  or an arriving record's rung at a crystal.
- The loader refuses a birth with no clicking record behind it.
- The light clock's A changes too (see (4): main's block does not delete
  its record at its count, and it drives its light record by the source
  term).
- The consequences for the fifteen:
  - Bell and Malus read computed weights and are unchanged.
  - The rows reading a steady field (the two slits, the pace fans, de Broglie's fringes,
    the index probes) take the born packet's spectrum, the extent of
    their emitter line. Their pins are re-derived blind on the
    regenerated worlds.
  - The first-rung rows (the moving mass's energy, Sagnac) re-derive their first rung from the
    packet's front.

**(4) The emitter's integers (the physicist's five questions of 19:45Z;
DERIVED HERE).** First, a CORRECTION of (3): main's block emitter is not
the form either. Its "click" is a count on the sum of its record (a
crossing from at most 0 to above 0) that deletes nothing. Its light
record is born at content 0 and filled at every interval of the cycle by
the coupling's source term (`_source`). So the light clock's A CHANGES
too. The form, with its integers:
1. THE EXCITED RECORDS, IN TURN. The emitter is a body of a massive kind
   with `emits` and a STOCK `amount` = M, the number of its excitations.
   - At interval 0 its first excited record is on the board: the body's
     seed at both levels (9.9), content one quantum, its residue u_1
     (SUPERSEDED by 9.19 (4), ADOPTED: the law's remainder at its centre
     Node, no wheel and no residue order on the body).
   - Excited record k clicks at ITS OWN RUNG on its own Nodes: **E** is
     its own offer booked through its Nodes (read-through, no take), and
     **D** is 2 T u_k + T <= 2 W C with T its norm.
   - At that click **X** ends it, and **E**^T births two records: the
     photon (content one quantum) and, while the stock lasts, excited
     record k + 1 (the seed again, content one quantum, residue u_(k+1)).
   - So quanta are conserved at every click, M in all. The emission
     times are the rungs, spread by the residues over the wheel: the
     spontaneous emission of the algebra. THE RATE KEY RETIRES: the rate
     is the rungs'. There is no source term and no drive.
2. THE BORN VALUES, written once at the click's interval t_0 on the
   emitter's Nodes (N the wheel of phases, [p, q] the born family's
   phase per Link, n / d its clock per interval, phase(age) main's
   `_phase` = (3 N / 4 + floor(age n / d)) mod N):
   - On ONE NODE: now = A C[phase(0)] and before = A C[phase(-1)]. The
     record is broadband.
   - On A LINE of L Nodes from the vertex along +e, at the Node x = 0 ..
     L - 1: now = A C[(phase(0) - floor(x p / q)) mod N] and before = A
     C[(phase(-1) - floor(x p / q)) mod N], a character travelling along
     +e. The line's order from its vertex is its placement (9.6), and its
     heading is the born character's.
   - A narrow packet of n wavelengths has L = round(n N q / p) Links, the
     nearest integer (the loader prints it).
   - The residue u enters only the born record's rung, as today.
3. THE NORM: T = SUM over the emitter's Nodes of (now - before)^2 at the
   birth, the motion the one write inserts. The rung's T is this.
4. THE WHEEL AND THE RATE: the wheel [step, W] and the residue order
   `seed` stayed on the emitter body in this reading; SUPERSEDED by 9.19
   (4), ADOPTED: no wheel and no residue order on any body, u the law's
   remainder and W from the centre Node's pair. The rate keys ([1, 1]
   for Bell, [1, 4] for the two slits) retire: births come at the
   excited records' rungs. A world that needs n births declares the
   stock M = n.
5. THE STEADY-FIELD PINS are re-derived blind by the World Generator's
   map (the physicist's tool) on the born packets. The mathematician
   checks each derivation. The pace fans need no single-Node source: two
   LINE emitters, one along the axis and one along the diagonal, each
   give a travelling character, and k(axis) - k(diagonal) = k^2 / 48 at
   fixed omega is a property of the band that holds per character. So the
   fans' reading is kept with lines, and the pin stands.

**(5) The physicist's two readings and one question on the emitter's
first head (emitter-click 7ce8d66a, 20:45Z; DECIDED HERE).**
1. THE EXCITED RECORD'S NORM T is the offer its own mode books over ONE
   PERIOD of its own clock, T = SUM over the P intervals of a period of
   SUM over its Nodes of (now - before)^2, with P the nearest integer to
   2 pi / omega_b. The generator computes it by advancing the seed alone
   for P intervals, the rule being exact on integers, and writes it as the
   emitter's integer `norm`. The loader recomputes it the same way and
   refuses a mismatch; the count is the loader's, not the law's (9.5).
   - WHY: a bound record books without end, so its only finite measure is
     per cycle. With this T, the excitation of residue u clicks within its
     first period, at about (2 u + 1) / (2 W) of it. The mean wait is half
     a period WHATEVER THE WELL'S DEPTH: W births take about W P / 2
     intervals, and the cadence is not a sizing integer.
   - The seed's squares (the head's T) make the wait scale as 1 / omega^2,
     which is a unit accident.
   - The smoke run's numbers move accordingly. The generator re-derives
     them.
2. THE STATIC LEVEL: the one-Node write carries no zero-frequency part.
   now = A C[(3 N / 4 + floor(s / 2)) mod N], with s = floor(n / d) the
   clock's step, and before = -now EXACTLY. That is the character sampled
   half a step either side of its zero crossing. The norm is then 4 now^2
   per Node.
3. THE LINE'S TRAVELLING CHARACTER: no per-Link pair enters the engine.
   The band's k at a rational omega is not rational, so the born profile
   along a line is MATERIAL: the generator writes the two levels' integers
   over the body's Nodes (the key `born`, a profile at both levels, as the
   well's seed is, 8.7). The engine copies them at the click. The loader
   prints the band check (the profile's k and omega on 3 cos omega = cos
   k + 2), as the seed's check is printed.
   - Default with no `born`: the one-Node pair of item 2 on every Node
     (Nodes in phase).
4. A DEFECT to correct: `_emit` branches on `self.families[family].
   massive_kind` to set the record's `driven` mask. That is a branch on a
   family's kind (9.10; the three tests: no family name or kind). The mask
   belongs to the record's own data, set from the emitter's declaration,
   with no branch at the birth. SUPERSEDED by 9.18 (3): there is no
   `driven` mask at all; nothing drives a record after its birth.
5. CONFIRMED IN FORM on 7ce8d66a:
   - X is `del self.records[...]`, a deletion of the whole record.
   - The rung 2 T u + T <= 2 W C.
   - The offer read through the body's Nodes with no take.
   - One write at the birth, with nothing driven afterwards.
   - The next excitation, while the stock lasts.
   - The content moved from the stock.
   THE GATE (9.5) stays on the whole line, the retirements and the
   regenerated worlds included.

**(6) The write for an odd clock step (the physicist's question (2) of
22:00Z; DECIDED HERE; the table moved out of the engine on the owner's
word of 23:00Z).** The born pair is the character sampled half a step
either side of its zero: now = round(A sin(pi n / (d N))) and before =
-now exactly, n / d the clock's advance per interval in steps of the
circle of N, taken EXACT as the rational, A the amplitude unit
(CORRECTED 2026-09-25 on the physicist's finding: the first draft's
whole step s = floor(n / d) is 0 for a clock below one step per
interval, the index rows' [3565, 10000] on N = 64, and wrote no motion;
the half of the exact advance is never 0: 157930 on [77, 25] at N = 64
for A = 2^20, 18349 on [3565, 10000]). THE ENGINE HOLDS NO TABLE FOR IT: the born pair is TWO INTEGERS
OF THE WORLD, `born: [now, before]` per birth, computed by the generator
(a host tool, as the seed's mode is) and checked at load against the
generator's recompute; a line's born profile is the generator's integers
in the same way. No emitter is refused for any s. THE TWO FORMS OF THE
KEY, stated once (2026-09-25, on the physicist's reading of this
paragraph as "two integers only"): `born` is EITHER two integers [now,
before], the uniform birth on every Node of the body with before = -now
exactly, OR a profile, one integer per Node of the body at each of the
two levels (item (5) 3; the packet's summand of 9.22 (3): a travelling
character has before = the character one interval earlier, not -now),
checked at load for its count and for a motion; both are the world's
integers, the generator's, and neither is a table in the engine.
(6a) THE BORN TRAIN (REVISED at the owner's word of record 1950, 9.35 (10): the envelope is the body's own mode, the window and the tapers below are HISTORY; the load checks stand), THE ONE FORM OF A BIRTH (the physicist's finding on
emitter-click f0d2d745, 2026-09-25: the light clock's file run by the one
command, every record clicking on its outgoing pass, the one-way flux
into the cube beside the emitter 4.65 times the record's norm within 400
intervals and 4.23 at the emitter's own Node; DERIVED HERE, the first
form of the key RETIRED). The uniform birth [now, -now] on every Node of
a body is a flat pulse of the body's length: on twelve Nodes at the
wavelength 20.78 it is 0.58 of a period, broadband, and its standing
components (the band's edges, whose group velocity is about zero) carry
an alternating current at the body's Ports with no transport; the
positive part of an alternating current grows without bound, so the
one-way flux booked by any region beside the emitter exceeds the
record's norm and the ladder is met by sloshing, not by a passage (9.25
(11)). THE LOAD CONDITION (DERIVED): every birth is a TRAVELLING TRAIN,
the character of one **K** over n >= 8 periods under an envelope, written
on the body's Nodes at both levels; `born` has this one form, the
profile, and the two-integer form is refused with this reason. THE
INTEGER FORM: now[x, y, z] = round(A e(x) h(y) h(z) cos(k (x - x0))),
before[x, y, z] = round(A e(x) h(y) h(z) cos(k (x - x0) + omega)), the
character exp(i (k x - omega t)) at t = 0 and t = -1 along **K** = (k,
0, 0), travelling from interval 0 with no ramp (9.24 (2)); 3 cos omega =
(num / den) (cos k + 2) for a profile constant across (the reads on an
axis of extent 1 are the Node itself); the born clock [p, q] gives k = 2
pi p / (2 N q), and [512, 1] on N = 1024 (k = pi / 2, the wavelength 4;
cos omega = 2 / 3 for light, 0.6593 for [800, 809]) is the one clock of
every light emitter, since a longer wavelength fits no train on a body;
h the Hann window across each transverse extent Y, h(y) = sin^2(pi (y -
y0 + 1 / 2) / Y) (1 on a chain); e the taper along **K** over tau = X / 4
Nodes at each end, e(i) = sin^2(pi (i + 1 / 2) / (2 tau)) for i < tau, 1
between, e(X - 1 - i) for the tail (a hard-edged train is broadband at
its ends); X = 32 Nodes, 8 periods (64 for Mach-Zehnder), and the
emitting body's side along **K** is X; A = 2^16 (the rounding below 10^-5
of the norm; the ladder's integers are Python integers in the engine's
flux reading; the back-action 6 g x 1.41 A = 556 against the seed / 1000
= 52429 under (7) (c)). THE NORM T of the born record is the conserved
form of its two levels on the vacuum (9.19 (3)), computed by the
generator in integers, written beside the profile and checked at load:
it is the ladder's T. THE CHECKS: at load, in integers, the FORM (the two
levels on the body's Nodes and zero elsewhere; the hash of 9.22 (7)) and
the FLUX SIGN along **K** (the sum over the body's Links along **K** of
now_i before_j - before_i now_j positive: the record travels as
declared); not a residual of the character (a windowed train is no
solution of the rule, and a bound on its residual would be a number
chosen to pass). Before writing, the generator (float, the writer) runs
the train alone on the vacuum and reads its one-way flux through a plane
40 Links ahead: the norm within 2 x 10^-3 (COMPUTED on a chain of light at
k = pi / 2: 8 periods 0.9987, 16 periods 0.9997; 3 periods 1.0285 and
still growing, refused). The excited record's rung is untouched here
((7) (f), for the owner's word).

**(7) THE EXCITED RECORD'S RUNG, CORRECTED (the physicist's two readings
on emitter-click fd1734c2, 2026-09-25: the births 1 to 10 intervals
apart with the flux into the centre Node front-loaded; the seed-100 test
bodies swamped by the born light; DERIVED HERE, RECOMMENDED for the
model owner's word, since (4) item 1 and (5) item 1 were adopted with
9.17).** (a) THE FINDING'S CAUSE, PROVED: on the lattice the flux G_ij =
(1 / 3) A_ij (now_i before_j - before_i now_j) (9.19 (3)) VANISHES
IDENTICALLY for a bound standing mode: every Node of a real eigenvector
oscillates in phase, a_i(t) = p_i cos(omega t + phi), so now_i before_j
- before_i now_j = p_i p_j [cos(omega t + phi) cos(omega (t - 1) + phi)
- cos(omega (t - 1) + phi) cos(omega t + phi)] = 0 at every Link and
every interval (the Wronskian of proportional functions; the Node's
share e_i = D_i p_i^2 sin^2 omega is constant, so nothing flows). The
seed (p, p) is such a mode with its phase half a step off. So the one-way
inward flux into the centre Node that (4) item 1 and (5) item 1 read is
NOT the mode's sloshing (there is none on this flux form, unlike the
continuum's energy current) but the seed's ROUNDING TRANSIENT (an
integer profile is not an exact eigenvector, and its residual radiates
in the first intervals and settles) plus the back-action; the norm T of
(5) item 1 is that transient's flux over a period, front-loaded, and a
residue near W crosses it within ten intervals: the physicist's cadence,
exactly. His proposed start on the mode's phase (before = the profile one
step back) is the same standing mode and gives the same zero: it changes
the transient, not the reading. (b) THE LAWFUL RUNG: the excited record's
offer accrues at the fixed rate of its own mode, C(t) = T (t - t_0) / P,
with t_0 the interval of its (re)seed and P its period, the generator's
integer pair [p, q] from the composed operator's eigenvalue (2 pi /
omega_b as a rational); the rung 2 T u + T <= 2 W C is then the INTEGER
COMPARISON 2 W q (t - t_0) >= (2 u + 1) p, and T drops out of the
emitter's rung (it stays the born record's, the conserved form). The
click comes at the phase (2 u + 1) / (2 W) of the period: a uniform
waiting time in [0, P) set by the residue, one birth per half period on
average, the cadence (5) item 1 intended ("W births take about W P / 2
intervals"), now independent of the seed's rounding and of the
back-action, which move the remainder and hence the residues alone (the
chi-square of 9.19 item (4e) stands: 6.20 and 11.20 on 9 degrees of freedom
over 100 births, equidistributed). The three tests: generic (the
integers u, W, p, q and the record's own age), vector (one comparison),
local (the record's own age and residue, its named set the centre Node
where the remainder is read). What it is physically: the bound mode's
own oscillation read at its centre, the emission at the phase the law's
remainder sets; the light on the board neither hastens nor delays it
(no stimulated emission in the law; a hypothesis, if ever wanted, under
its own identity). (c) THE BORN AMPLITUDE (his question (ii)): the born
record's amplitude is the amplitude unit A of (6), a convention of the
write, not the excited record's; no law ties the born record's norm to
the excited record's (each record's I is its own conserved form, the
birth is a write E^T and the quantum is counted, not weighed; a relation
between them would be a new hypothesis). What is physical is the
back-action's size against the body's own amplitude: g times the born
light's first differences at the body's Nodes must stay small against
the excited record's amplitude, else the record leaves its mode (his
seed-100 worlds, driven 158 per Node per interval against 100, are
swamped). LOAD CONDITION (DERIVED): 6 g A sin(pi n / (d N)) <= the
body's seed amplitude / 1000, printed at load and refused above; the
registered worlds at 50 x 2^20 meet it by 10^-6, the test worlds at a
seed of 100 do not and are raised to it (their assertions are on the
form). (d) WHAT CHANGES IN THE ENGINE (for the physicist, after the
owner's word): `_excitation_rung` compares the record's age with its
residue on the mode's period instead of booking the flux into the centre
Node; the emitter's `norm` is the born record's and its `period` the
mode's pair; the residue's read point and the coupling of 9.19 item (4e)
stay. (e) THE INTERNAL CLOCK AND THE ONE FORM (the model owner's
questions of 2026-09-25 through the Boss: "so it is a general law? the
clock is the internal clock, and what is the internal clock really?";
and the Boss's two: is the age a counter, and is the age rung one
operation with the flux rung; DERIVED HERE). THE AGE IS NOT A COUNTER.
Let e_i be the Node's share of the record's conserved form (9.19 (3):
e_i = D_i (now_i^2 + before_i^2) - (1 / 3) now_i (**A** before)_i, a
bilinear form of the record's two levels at the Node and its six reads,
the bilinear form, local). For the bound mode a_i(t) = p_i cos(omega t + phi) it
is CONSTANT at every Node, e_i = D_i p_i^2 sin^2 omega (PROVED by the
mode equation (**A** p)_i / 3 = 2 cos omega D_i p_i and cos^2 a + cos^2
b - 2 cos(a - b) cos a cos b = sin^2 (a - b)), positive, and it is what
the standing mode has in place of a flux (its change, SUM of G_ij, is
zero). So THE EXCITED RECORD'S RUNNING TOTAL ACCRUES ITS CENTRE NODE'S
SHARE e_c EVERY INTERVAL, C(t) = C(t - 1) + e_c(t), read from the two
levels on the board and nothing else; its norm is one period's sum, T =
P e_c (the record's ACTION over one cycle, energy times time); the rung
2 T u + T <= 2 W C is unchanged, and for the exact mode it reduces to 2
W (t - t_0) >= (2 u + 1) P, the age rung of (b), the age appearing only
as the number of accruals, which the running total C already is: the
record integer every record carries (9.25 (2)), no clock and no
counter, nothing kept at a Node; for the rounded mode e_c(t) wobbles
with the transient and the sum self-corrects. THE INTERNAL CLOCK is
therefore the mode's own rotation under the law, omega per interval
with 2 cos omega = a / b (the pair the generator writes and the load
check verifies, 9.22 (7)); its tick on the board is e_c per interval,
the same at every interval because the rotation is uniform; and it is
the one clock of the model: the one that slows in a moving packet by
the dispersion (0.8146 at k = 3, 9.24 (2)), so the emitter's cadence,
the muon's tick and the light clock's period are readings of one
rotation. ONE RULE OR TWO: ONE FORM, ONE RUNG, ONE RUNNING TOTAL, TWO
READINGS OF THE FORM, and the two are the two sides of one identity.
The detector reads e's CHANGE within its region, what enters through its
Ports per interval (the one-way flux, 9.25 (2)); the excited record
reads e's VALUE at its centre Node per interval (what stays); e_i(t) -
e_i(t - 1) = SUM over j of G_ij (9.19 (3), PROVED) ties them, the flux
being the change of the share. Why not one reading: a bound record has
no change to read (its energy never crosses a Link, (a)), and a
travelling record's value at a detector would count its residence, not
its passage (the same energy counted once per interval it sits in the
Node, a norm that depends on the set's depth and breaks the one
threshold per record); so each set reads the side of the identity that
is not identically zero for the record it names. Stated as one law: the
click reads the record's conserved form at the named set, and C accrues
per interval the part of it the set acquires, from outside through its
Ports where the record moves, from its own persistence where the record
stands. In the engine the two are one machinery (Nature24's
`conserved_form` is SUM of e_i, the flux its increment), the excited
record's increment e_c at its centre Node in place of the flux there.
The Boss's phrasing "the accumulated phase advance, of which the flux is
the travelling case" is not exact (a passage's flux is the norm, not a
phase) and is replaced by the above. (f) THE RULE IN ONE STATEMENT, in
the model owner's framing of record 1912 ("first we set their clock by
our general rule"; "it is really the rate: the rate of the click with
its own clock"), fit for his yes:

    EVERY RECORD CLICKS ONCE, at the first interval at which its running
    total C reaches its threshold theta = (2 u + 1) T / (2 W), and C
    accrues each interval the record's conserved form e that its named
    set ACQUIRES: through the set's Ports from outside where the record
    moves (the one-way flux, the detector's pace), and at the set's own
    Node where the record stands (its share e_c, the record's own tick,
    the emitter's pace); T is the norm of one whole acquisition, the
    record's energy entering a detector, or one period's action, P e_c,
    at the emitter.

One click, two sources of its pace, exactly as the owner framed it; the
clock of the second source is set by the law alone, the mode's rotation
omega with 2 cos omega = a / b, no declaration. THE THREE TESTS: generic
(the integers u, W, T, the form e and its increments, no family name
and no kind; the same rung for a photon at a screen, an excited atom
and a pair); vector (e is a bilinear form of the record's two levels,
the bilinear form; the accrual a sum, the translation; the click one comparison, the division with the remainder kept; no
root, no float); local (e_i from the Node's two levels and its six
reads; the flux from the two ends of a Link; the running total and the
threshold the record's own integers, nothing kept at a Node; the record
deleted whole at the click, record 1888). WHAT CHANGES IN THE ENGINE
(for the physicist, on the owner's yes): in `_excitation_rung` the
excited record's increment is its centre Node's share of the conserved
form (the per-Node term of `conserved_form`, D_c (now^2 + before^2) -
(1 / 3) now (A before)_c in the flux's units) in place of `inward_flux`
there; the emitter's `norm` is P e_c, the generator's integer from the
mode's period [p, q] and its share, recomputed at load; the residue's
read point and the coupling of 9.19 item (4e) stay; every detector's ladder
is untouched. What it settles: the emitter's cadence is one birth per
half period on average, fixed by the law's remainder, the same for a
one-Node emitter and a slab, on a chain and on a layer.

### 9.18 The unification: one object, one record, one rule; what is generic; what the algebra carries at once (the model owner's words of 2026-09-24 to the mathematician: "write the whole unification, what is generic with us, and whether the algebra supports it in one stroke"; ADOPTED by the model owner, 2026-09-24, 22:39Z (2026-09-25 on the Israel clock) through the Boss, record 1875: "adopt; everything is algebra", with bound tool bodies of a holder family, at most three families, one border for every family)

THE QUESTION. The owner's questions that led here: is every tool a
body of a massive kind; is there any duplication; is a massive family
matter. This section answers them as one statement and marks what the
algebra carries and what it does not. ADOPTED (record 1875): it is the
definitions' form (SIMULATOR_DEFINITIONS.md, "The one operator, the click
and the birth").

**(1) THE ONE OBJECT: THE BODY (DERIVED HERE, from 8.1, 8.3, 9.1, 9.15
and 9.17).**
- A tool acts by the law's own advance on its material, plus at most a
  click whose other side may be a birth (9.17 (1)).
- A tool's material is integers on a set of Nodes whose stabiliser fixes
  its shape (9.1, 9.6), which is exactly 8.3's body: a G_48-set of
  Nodes with a pair per family on its Nodes.
- Light cannot be a body (8.3, PROVED: the norm bound). So a body's own
  family is always a MASSIVE family.
- So the nine tools of the specification's A.10 are ONE OBJECT, the
  body, carrying optional integers. THERE IS NO DUPLICATION: the well
  and the transponder are the same object, the emitter is a well with a
  stock, and the crystal is a body whose birth is triggered by an
  arriving record instead of its own.

| What the body carries on its Nodes, beyond its own pair | The tool it is |
| --- | --- |
| nothing | the well (a clock) |
| a light pair (a gap [1, 2], a layer [91, 107], an index) | the mirror, the splitter, an index slab |
| an axis (a, b) on the label rows | the polariser |
| a coupling (g, G) between two families (8.5) | the medium of the index rows |
| a BIRTH (a born profile and branches) triggered by its own excited record's click, with a stock M | the emitter |
| a BIRTH triggered by the click of an arriving record whose ladder names the body | the crystal |
| its name in records' ladders and a wheel W | the receiver |
| a light pair and a momentum | the transponder |

- THE FACES ARE NOT A BODY: they are the board's border, the row beyond
  read as 0 (1.6).
- A BODY IS BOUND OR SILENT. A BOUND body carries its own record, its
  seed, the mode of the composed world (9.9), and a momentum the push
  moves (9.15). A SILENT body carries no record: its integers act, but
  it cannot carry momentum. Main had the silent body (the receding
  index's medium, "the silent body's exception" in the body's
  conditions). DECIDED (record 1875): TOOL BODIES ARE BOUND, of the holder
  family; the silent body retires, the index rows' medium included (9.22
  (4)).

**(2) THE FAMILIES (DERIVED HERE).** A family is its vacuum pair and its
label module, nothing else; its quantum is the counting unit of its
content, a convention of the reading (9.22 (1)). Its clock
(`phase_per_link`) is a datum of the birth, read by the generator for the
born profiles and the seeds (9.17 (5), 8.7), not by the law.
- LIGHT: the pair [1, 1], with no rest frequency (at **k** = 0, omega =
  0). It is never a body.
- A MASSIVE FAMILY: the pair [num, den] with num < den, whose rest
  frequency omega_0 has cos omega_0 = num / den (8.1). This is MATTER in
  the dictionary: one kind of quantum with one rest mass. The experiment
  declares one where it has matter (the clocks, Sagnac, the redshift,
  the index rows, de Broglie's fringes, the moving mass's energy).
- THE HOLDER FAMILY FOR THE TOOLS' BODIES, needed only where the tools'
  bodies are bound. Its necessity is DERIVED: a Node carries ONE pair per
  family (8.1), so a body whose own family is F cannot carry on the same
  Nodes a tool pair for F, because its F-pair is its well. So a tool's
  body must be of a family OTHER THAN EVERY FAMILY THE TOOL ACTS ON OR
  READS.
  - de Broglie's fringes' barrier (the gap [1, 2] for matter) and its screen cannot be
    bodies of the matter waves' own family.
  - A receiver of a family's records cannot be a well of that family,
    because its well would change the field it reads through.
  - So a world has at most THREE families: light, the experiment's
    matter, and the holder. It has fewer where one is absent: Bell,
    Malus, the two slits and the pace fans have light and, with bound
    tools, the holder.
  - This is not a duplication: the holder is the same KIND as matter
    with its own pair, and it is required by one pair per family per
    Node.
- WHAT RETIRES: `counter` (the table bodies' family); the cart world's
  `post`, `source`, `cart` and `mass` (the table form); the families'
  `take` pairs (9.12).
- DECIDED (record 1875): ONE BORDER FOR EVERY FAMILY (the algebra's one
  board, 1.6); main's faces per family (the light clock's chain periodic
  for matter and closed for light) retire at regeneration.

**(3) THE ONE RECORD.** A record is its family; its rows per label value
per arm at two levels with the remainders; its residue u; its norm T; its
content in quanta; its ladder (the Nodes it names); its branches (the
labels); and its age. A body's own record is a record like any other,
with its offer booked through its own Nodes. NOTHING ELSE is kept:
- no clock on the record (the law does not read one);
- no take and no grace;
- no driven mask;
- no completion (it ends at its click or at its close, 9.12).

**(4) WHAT IS GENERIC WITH US: the primitives, each a composition of the
six verbs of chapter 2 on data alone, with no family name, no tool name
and no kind.**
1. THE RULE (8.1): every record of family F at every Node, with that
   Node's F-pair. It is (B) the pair on the six reads, (T) the levels'
   shift and (D) the one division with the remainder kept (8.10). It is the same rule for
   light and for matter: light is the pair with num = den, and no branch
   on the kind exists.
2. THE COUPLING (8.5): (B) between two records' rows at a body's Nodes,
   with the body's (g, G). It is the law's advance.
3. THE LABEL MATRIX (9.16 (2)): (B) with the body's axis on a record's
   label rows.
4. THE CLICK (3.1, 8.6, 9.12): (E) the record's offer at the Nodes its
   ladder names, read through (the motion booked at their Ports), then
   (D) the rung 2 T u + T <= 2 W C. For a record of rank 2 the joint
   weights are R = J^2 (3.6).
5. THE CLICK'S ACTION (8.8): the record ends with all its rows, the one
   deletion. Its content and its push are handed to the clicking body.
6. THE BIRTH (9.13, 9.17): the body's born profile written once, at both
   levels, at a click's interval. The click is either the body's own
   excited record's (and the next excitation follows while the stock
   lasts) or a named arriving record's.
7. THE PUSH (8.11): (G) the stress, at the body's outer Ports, of the
   records of the families the body declares as pushing it; then (D)
   into the body's vector **p** (the momentum, bold for a vector) with
   the remainder kept; then (T) the step when the accumulator reaches
   its wall. Which families push a body is its declared data, not a
   branch.
8. A COUNT ON A RECORD'S OWN AGE (9.5): the close of a screen's ladder
   (9.12 item 2). RETIRED by 9.19 (3) (a): the ladder is read at every
   interval and the record ends at its click, at the face receiver at
   the latest; no count on an age remains in the law.
9. THE LOADER'S CHECKS (9.5), never the law's:
   - the body whole on the board, and the bodies' Nodes disjoint;
   - the composed seed bit for bit, and the hybrids' share within the
     band (9.9);
   - the excited record's norm per period, and the born profile's band
     check (9.17 (5));
   - the axis with gcd(a, b) = 1 (the wheel as a permutation REFUSED,
     9.19 (4): no wheel is declared);
   - the tool bodies' drift: SUM over the run of abs(p_i) below the
     step's wall (8.11), so that no tool hops; the wall is the push's own
     integer denominator, 3 Q S M d, with Q the label's scale, S the
     width, M the body's content and d the push's declared scale, an
     integer of the world; the take's pair scale (56 d) of the first
     reading is REFUSED with the take (9.12).

**(5) WHAT RETIRES FROM MAIN'S ENGINE (read on main 5b0e8a77,
`detector_law.py` and `world.py`), each replaced by (4):**
- THE LAMP: `_drive`, the rate, the train, and the norm taken from the
  cosine table.
- THE BLOCK AS AN EMITTER: its cycle births and `_source` as the
  emitter's source. The coupling itself stays, as law.
- THE EMITTER'S KNOT: `own_grace`, `_exempt`, `_own_take`, `_in_grace`
  and the driven masks.
- THE TAKE: the take masks, the take pairs, `taken_by_emitter` and
  `escaped`.
- `_complete`.
- THE TABLE FORMS: `TableBody`, `_split_table_offers`, `read_pair`,
  `half_angle`, the `Splitter` with its linear form, and `world.py`'s
  check of S[k] for it.
- THE KIND BRANCHES on `massive_kind` in the law's path of main's
  `detector_law.py`: `_advance` (line 1691), `_complete` (2081) and
  `step` (2435, 2479, 2511 and 2524). The branch in `read_pair` (1910)
  goes with the table form. The reader `read_phase` (2550) keeps its
  own, because a reading writes nothing.

With these go ALL RUN-TIME TABLES. The cosine and sine tables remain only
in the GAMEBOARD readers (`read_phase`, a reading that writes nothing)
and in the generator (the seeds and the born profiles, written into the
world file as integers). THE LAW THEN USES NO TABLE, NO ROOT AND NO FLOAT,
and none of 2.7's exceptions.

**(6) DOES THE ALGEBRA CARRY IT AT ONCE? Item by item.**

| Piece | Status |
| --- | --- |
| the body as the one object, every tool its integers | IN (8.3, 9.1); the nine tools as this object DERIVED HERE |
| light is never a body | PROVED (8.3) |
| one rule for every family, light the pair num = den | IN (8.1) |
| the holder family's necessity | DERIVED HERE (one pair per family per Node) |
| the coupling | its form CARRIED (8.5); its scheme and its invariant J PROVED (8.5) |
| the label matrix | DERIVED (9.16 (2)) |
| the click, its action, the rung | IN (3.1, 8.6, 8.8) |
| the birth at a click | DERIVED (9.13, 9.17) |
| the composed seed and the hybrid condition | DERIVED (9.9): a condition checked per world, not a theorem that it holds |
| the push, and momentum conserved on the board | CARRIED (8.11): the stress as the momentum flux, and the one vector per body (the declared tie), are declarations of the design, not of the law |
| the excited record's norm per period; before = -now; the born profile as material | DECIDED (9.17 (5)), fixed only up to a convention |
| the tool bodies' binding, their mass and the hybrid share | SIZING integers the generator chooses and the loader checks, not values the algebra fixes |
| the material integers, the placement, the cone | declarations of the world by their nature (9.8; 9.16 (6)) |
| the faces per family | DECIDED (record 1875): one border for every family |

THE VERDICT: YES IN ITS OBJECTS AND OPERATIONS, NOT IN EVERYTHING.
- THE ALGEBRA CARRIES THE UNIFICATION AT ONCE WHERE IT MATTERS: one
  object (the body), one record, one rule, the six verbs. Every tool is
  data on that object. No new verb, no new group, no table and no root.
- IT DOES NOT CARRY AT ONCE:
  - (a) momentum's conservation with free bodies, because the push is
    carried (MISSING: a proof on the board that the stress at the Ports
    is the flux);
  - (b) the tool bodies' sizing (binding, mass, hybrid share), which
    consists of conditions and chosen integers;
  - (c) the decided conventions of 9.17 (5).
- THE COUNTS OF THE FIFTEEN DO NOT DEPEND ON THE UNIFICATION:
  - Bell and Malus read computed weights.
  - The first-rung rows read the front.
  - A tool drifting less than one Link moves no Node.
  - The steady-field rows are re-derived blind on their born profiles
    (9.17 (4)).

**(7) WHAT IT ASKS OF THE ENGINE (the physicist's), in addition to what
is owed already (12.1, 12.2, the emitter's line, the crystal's
rework):**
- A body carrying a pair for each of two families on the same Nodes.
- The birth as a body option, with its two triggers.
- The push generic over the families the body declares.
- The seeds computed on the composed operator.
- The retirements of (5).
The gate (9.5) reads each against this section.

### 9.19 The whole board is algebra: one element, one operator, one click (the model owner's words of 2026-09-24, 22:00Z (2026-09-25 on the Israel clock), through the Boss: "the whole board is algebra ... there are no parts"; his questions to the mathematician on the residues and on what the algebra carries; ADOPTED, record 1875)

THE CLAIM. The state of the whole board, every Node, every family and
every label together, is ONE ELEMENT of one module. The law is ONE MAP of
that element, equivariant under the four group objects. The click is the
one act that is not invertible. Everything the specification calls a
body, a tool, a family, a record or a face is a region or a summand of
that one element, or a name the host uses to read it. This section
derives it from chapters 1, 2 and 8, marks each piece, and draws what it
changes. (ADOPTED with the package of record 1875.)

**(1) THE ONE ELEMENT (DERIVED HERE from 1.1, 1.5, 1.6, 3.6 and 8.1).**
Let R be the group ring of the torus's translations extended by the cube group
(the translations act on positions, the cube group on positions and, by the
hand's sign, on the label pair). Let L be the label module (Z^2 per arm;
its tensor powers for a record of rank 2, 3.6). The state space is

    V = SUM over the quanta q of V_q,   V_q = (Z^Nodes (x) L_q)^2 (x) (the remainders),

one summand per quantum: a record is a summand of V, its two levels (now,
before) over the Nodes and its labels, with the remainder of verb (D) per
Node. The state of the world at an interval is one element v of V. Its
family is an index of the summand (the pair the operator uses on it), not
a second object. So THE OWNER'S WORD HOLDS AS WRITTEN: there are no parts,
there is one element with summands and regions.

**(2) THE ONE OPERATOR (IN THE ALGEBRA, 8.2; stated here for the whole
board).** The world declares, once, THE OPERATOR: for each family F a pair
[numerator, denominator] at every Node (the vacuum's pair everywhere, a
body's pair on its Nodes, the zero row at a closed face), the couplings
(g, G) between families on declared Nodes (8.5) and the axes (a, b) on
declared Nodes (9.16 (2)). Write **M**_F = **D**_F^-1 **A** / 3 for 8.2's
matrix of the family F (**A** the read matrix, **D**_F the diagonal of the
pairs). The step **S** of the law (bold, apart from CHSH's S) is:

    **S**: v -> v'  with, per summand of family F,  a_next = M_F a_now - a_before  (with the remainder, 8.1),
                 plus the coupling's bilinear term between summands of coupled families (8.5),
                 plus the label matrix on the axis's Nodes (9.16 (2)),
                 plus the push of the operator's regions (8.11: a body's Nodes step by its vector).

The whole board is one bound system (PROVED HERE, from 8.2): **S** restricted
to one family is a second-order linear recurrence with the symmetric
operator **D**^1/2 **M** **D**^-1/2 = **D**^-1/2 (**A** / 3) **D**^-1/2,
whose eigenvectors are THE MODES of the board and whose eigenvalues are 2
cos omega, omega the mode's clock. On a torus the spectrum is finite, one
mode per Node. A mode is BOUND when its 2 cos omega lies above the vacuum
band's top (omega below the rest frequency omega_0, 8.3), FREE when it
lies inside the band. Each mode is rotated by **S** at its own clock, with the
conserved form I (8.2) as its norm. THE STABILITY CONDITION (PROVED HERE):
the form I is positive definite, and every mode a rotation, exactly when
the largest eigenvalue is below 2; a mode with 2 cos omega >= 2 grows
without bound (the physicist's "runaway well" of 2026-09-24, 22:00Z:
[800, 700] on [800, 809] gives 2.03 on a chain). A pair with numerator at
most denominator at every Node is SUFFICIENT (then abs(2 cos omega) <= 2
by 8.1's band), not necessary (the one-Node well [8, 7] on [7, 8] has
1.90 on a chain, 1.75 on a layer). THE LOADER'S CHECK is the spectral one:
the composed operator's largest eigenvalue below 2, refused otherwise (the
physicist's refusal CONFIRMED). THE LOWER END (the crystal's reviewer's line): the
symmetrised operator D^-1/2 (A / 3) D^-1/2 has nonnegative entries, so by
Perron-Frobenius its largest eigenvalue is the largest in absolute value
and the smallest eigenvalue is at least minus the largest; with the
largest below 2 every eigenvalue lies in (-2, 2), abs(2 cos omega) < 2,
and every mode is a rotation: the one check bounds both ends.

EXACTNESS. The rotation of the modes is exact in the real reading
(Outside, 3.4). On the board the levels are integers and the step keeps
the remainder: the step is a bijection (8.8) and I obeys 8.2's exact
remainder identity. The modes mix by at most one unit per step, and that
unit is the remainder.

**(3) THE ONE READING: THE FLUX (DERIVED HERE from 8.2; the physicist's
question of 22:00Z on the content found on a take Node, and 9.10 item 1
and 9.12 closed by it).** Let e_i be the Node's share of the conserved
form, e_i = D_i (a_next,i^2 + a_now,i^2) - (1 / 3) a_next,i (**A**
a_now)_i, so that I = SUM over i of e_i. Then, PROVED HERE in one line
(substitute the rule D_i (a_next,i + a_before,i) = (**A** a_now)_i / 3
into the difference of e_i between two intervals):

    e_i(t) - e_i(t - 1) = SUM over the reads j of i of G_ij,
    G_ij = (1 / 3) A_ij (now_i x before_j - before_i x now_j),   G_ij = -G_ji.

G_ij is THE FLUX INTO i FROM j: a bilinear form (the bilinear form) of the record's
own two levels at the two ends of a Link, PAIR-FREE (the pairs cancel in
the derivation), antisymmetric, local. For a character moving from j to
i it equals sin omega sin k times the squared amplitude, positive.
COMPUTATION (a chain, light's pair, a packet of 40 Links at k = 0.3024):
the local identity holds to 10^-15; the ONE-WAY inward flux into one
Node, SUM over intervals and Ports of max(G, 0), over the packet's
passage equals the packet's I to six digits (2.135254 both), and the
signed sum is 0.

THE READING E OF EVERY RECEIVER IS THIS: the record's offer C at a set of
Nodes is the one-way inward flux into the set through its Ports, summed
over intervals; the record's norm T is its conserved form I. The rung 2 T
u + T <= 2 W C then reads "the share of the record's energy that has
entered the set reached (2 u + 1) / (2 W)", and C reaches T exactly as the
record passes, at a set of ONE Node as at a screen. The rectification
max(G, 0) is the click's own comparison (the division with the remainder kept at the click, 9.7): a
record's energy is counted when it enters. Consequences, each DERIVED
HERE:
- THE TAKE, THE GRACE, THE EXEMPTION, THE OWN TAKE AND THE DRIVEN MASK
  RETIRE TOGETHER (9.12, 9.17): an outgoing front gives no inward flux at
  its own body's Ports, so a record never clicks on the way out; it
  clicks where its energy enters, and on its own emitter only when it
  returns (the light clock, Sagnac). 9.10 item 1's owed self-click share
  is the returning share, a placement's number, and the computation owed
  there retires.
- A SET AT ITS EMITTER'S NODES (the physicist's finding (3)): the write is
  on the Nodes, not through a Port; it books nothing; the record's
  energy is its I from the birth; nothing vanishes and nothing is booked
  unread.
- THE EXCITED RECORD: SUPERSEDED by 9.17 (7) (a) and (e) (the correspondence
  audit of record 1942): a standing mode's flux through every Port vanishes
  (the Wronskian), so its rung accrues the centre Node's own share e_c and
  its norm is T = P e_c, one period's sum; the earlier reading here (the
  one-way flux into the centre Node fed by the mode's sloshing) is HISTORY.
  The cadence stays half a period per birth.
- THE MIRROR'S AND THE SPLITTER'S SHARES are the one-way flux through a
  Port behind the body over the record's I, the form the physicist
  measured (his window reading of 18:50Z).
- THE NUMBERS: T and C are integers once scaled by 3 (the flux) and by the
  pairs' common wall (I); the first-rung pins of the measured experiments (the moving mass's energy, Sagnac,
  the light clock) are re-derived blind by the generator's map on the
  flux form before any run; Bell and Malus read computed weights and do
  not move.

THE PHYSICIST'S THREE QUESTIONS OF 22:17Z, ANSWERED (DERIVED HERE):
- (a) THE FACES, read against Highlights' record 15 of 2026-09-19 ("the
  GameBoard of a run is open on every face, what leaves clicking on the
  face detector; an axis may be declared periodic; a closed board is
  refused"): THAT DECISION STANDS, with the take replaced by the click.
  An open face is the zero row beyond the border (1.6) AND A RECEIVER
  named `face` at the border Nodes, on every record's ladder as its last
  set, read like any set by the one-way inward flux; what leaves clicks
  there and is deleted whole; the sponge (a take with no click) retires,
  and `escaped` is the face receiver's count. A board with neither a
  periodic axis nor a face receiver stays refused. Before the face's rung
  is reached the zero row reflects, so the steady-field rows keep the
  margin rule of the placed experiments of LAB_TOOLS.md at regeneration. On such a
  board every record's energy is read by some set of its ladder without
  end, so EVERY RECORD CLICKS and the close on a record's own age (9.12
  item 2) RETIRES: the click is the record's one end; a record alive at
  the run's last interval is reported alive, a host reading. (An earlier
  line here, "every board is closed and the open face retires",
  CONTRADICTED record 15 and is withdrawn.)
- (b) THE CLICK'S ACT: the record is deleted WHOLE at the rung, its rows
  everywhere (8.8's one deletion), at that interval; a set's offer is
  read through its Ports only (a Link from a Node outside the set into a
  Node inside it), the Ports of a set at a body's Nodes included. WITH
  SEVERAL SETS ON ONE LADDER (a screen), the ladder is cumulative in its
  declared order and THE CLICK IS THE INCREMENT LADDER OF 9.25 (2): the
  running total C(t) of the record's offers into the ladder's detectors
  crosses theta = (2 u + 1) T / (2 W) at one interval, and the Node is the
  one whose segment of THAT INTERVAL'S increment, laid out in the
  ladder's order, contains theta - C(t - 1); Born's rule is then exact
  (9.25 (3)). (The sentence that stood here, "the click fires at the
  first interval at which some partial sum L_k reaches the threshold, at
  the first such k", read the Node on the partial sums at the crossing
  and put every click at the last Node of the order, as the physicist
  found on 2026-09-25: WITHDRAWN.)
- (c) THE EXCITED RECORD'S SET: one Node always, the body's centre Node
  at the lower vertex plus side // 2 on each axis; for a one-Node body the
  set is the Node. Its reading is NOT a flux through the Node's Links (a
  standing mode has none, 9.17 (7) (a)): the rung accrues the Node's own
  share e_c and T = P e_c (9.17 (7) (e)); the line that stood here, "T =
  the one-way inward flux into it over one period", is HISTORY (the
  correspondence audit of record 1942).

**(4) THE RESIDUE: WHAT IT IS, AND HOW TO STOP DECLARING IT (the owner's
question; DERIVED HERE, with COMPUTATION).** Two things are called a
remainder. THE RULE'S REMAINDER r (the division with the remainder kept, 8.1) is kept per Node per
record and is the law's own. THE WHEEL'S RESIDUE u is one integer per
record on Z_W, read once, at the rung; with the ladder it chooses the
Node in the weights' proportion, which is Born's rule (4.8, c_1 = 1). It
is the model's hidden variable: local (born with the record),
deterministic (no draw, 2.7), and DECLARED (a permutation of Z_W in the
world file, `residue_order` and `residue_seed`). IT CANNOT BE REMOVED:
without it every record clicks at the same Node and there is no
distribution. ITS SOURCE CAN CHANGE: u may be read from the law itself,
as the rule's remainder r at the birth Node at the interval of the click
that births the record (the excited record's remainder at its click; the
arriving record's at the crystal's), with the wheel W = 3 x the pair's
denominator at that Node. Then the world declares no residue.
- THE RANGE OF THE REMAINDER (PROVED HERE, one line): the rule gives r'
  = numerator x S_6 + r (mod 3 x denominator), so from r = 0 every
  remainder is a multiple of gcd(numerator, 3 x denominator) =
  gcd(numerator, 3) with the pair in lowest terms: AT MOST 3 x
  denominator / gcd(numerator, 3) values. THAT EVERY ONE IS REACHED, and
  equidistributed, is COMPUTED, not proved: on a chain the vacuum [800,
  809] gives 2427 values,
  equidistributed over 18000 intervals (chi-square 21 on 19 degrees of
  freedom, the 95 percent bound 30) and equidistributed over 160 births
  read one per birth (11 on 9, the bound 17); [3200, 3227] gives 9681;
  A WELL [800, 800] = [1, 1] AND LIGHT [1, 1] GIVE THREE. The lamps'
  [77, 25] and [2464, 25] are BORN CLOCKS (the phase per Link, 9.17 (4)),
  not pairs: light's pair is [1, 1], so a light birth Node needs an index
  pair (4a). So the residue is read where the pair is rich: a well
  declared [800, 801] (2403 values) rather than [800, 800].
- THE COST: with a declared permutation W records cover the wheel exactly
  once and the pins are exact (8/2/2/8 at W = 20, no band); with the
  law's remainder the residues are equidistributed but not a permutation,
  and the counts are binomial about the weights, as nature's are: every
  pin gains its binomial band. The run stays deterministic and
  reproducible either way.
- ADOPTED (the model owner, 2026-09-24, through the Boss at 22:18Z: "in
  my opinion, without declarations"): THE RESIDUE IS THE LAW'S OWN
  REMAINDER. A record's u is the rule's remainder r at its birth Node at
  the interval of the click that births it (the excited record's
  remainder at the emitter's centre Node; the arriving record's at the
  crystal's centre Node), and its wheel is W = 3 x denominator /
  gcd(numerator, 3) of that Node's pair for the clicking record's family,
  in lowest terms. No `residue_order`, no `residue_seed`, no declared
  wheel anywhere; the loader refuses them. Read against Highlights: the
  remainder read is the RECORD'S ROW'S (8.1: the remainder kept on the
  record's row), not the Node's, so record 155 ("a Node keeps no
  remainder and no draw") holds; and W, listed by record 189 among the
  law's grain constants as the birth wheel, becomes a quantity of the
  world's pair (3 x denominator / gcd(numerator, 3)), no longer a constant
  of the law: a RECLASSIFICATION for the Boss's record, not a change of a
  rule. The first excitation of a
  body, on the board at interval 0 with every remainder 0 (9.9), has u =
  0 and clicks at its earliest rung. What follows, DERIVED HERE, blind:
  - (4a) THE RICHNESS OF THE BIRTH NODE. The granularity of Born's rule
    on a wheel of W values biases each Node's share by at most 1 / (2 W).
    For that bias to stay below a tenth of the smallest binomial band the
    fifteen read (Bell's 0.011 on a share of 0.4 at 100 records), W >=
    500. So EVERY TOOL THAT BIRTHS DECLARES, ON ITS BIRTH NODE, A PAIR FOR
    THE CLICKING RECORD'S FAMILY WITH 3 x denominator / gcd(numerator, 3)
    >= 500, checked at load: an emitter's well [800, 801] (2403) or
    [3200, 3227] (9681), never [800, 800] or [8, 7] (3 and 21); a
    crystal's Nodes carry a LIGHT pair, an index, rich in the same
    sense ([800, 801] on light, 2403), never the vacuum's [1, 1] (3). The
    fifteen's wells [800, 800] (the deep well, the boxes, the light clock,
    Sagnac) become [800, 801]; [314, 315] (945) and [3200, 3227] stand;
    [156, 157] (157) is the vacuum pair of the redshift and the index rows
    and no birth Node carries it (their births are the wells [314, 315],
    945), so it stands (the physicist's question of 2026-09-24, 22:50Z,
    answered; the earlier "changes" withdrawn); the one-Node emitters'
    [8, 7] (21) is too poor and changes: [801, 700] on [7, 8] gives 700
    values, and COMPUTED on the composed operator it is bound and stable
    on a chain (1.90193 against the band top 1.75, the profile halving
    per Link), bound weakly on the layer 30 x 33 (1.75218, the tail 0.30
    five Links out), and on a cube one Node does not bind in the
    large-board limit (1.7512, 1.7506, 1.7504 on 8, 10 and 12, falling to
    1.75): a cube's emitter body is of side 3 (1.8609 on 14^3, the tail
    below 0.13 three Links out), the load check's bound deciding (9.21
    (8b)). The pair's richness is a load check beside the bound and
    the stability (9.19 (2)).
  - (4b) THE PINS AS DISTRIBUTIONS (the exact W = 20 pin RETIRES; every
    counting row reads a count against a binomial band; n the records per
    setting; the band 3 standard deviations). BELL, HV + VH with Alice's
    axes (1, 0), (1, 1) and Bob's (1, 2), (3, 1): the shares (++, +-, -+,
    --) are (2 / 5, 1 / 10, 1 / 10, 2 / 5) at E = 3 / 5, (1 / 20, 9 / 20,
    9 / 20, 1 / 20) at E = -4 / 5, (9 / 20, 1 / 20, 1 / 20, 9 / 20) at E =
    4 / 5; S = 14 / 5 with the variance SUM over the four pairs of (1 -
    E^2) / n = (16 + 9 + 9 + 16) / (25 n) = 2.00 / n (the earlier 2.28
    was an arithmetic slip, the crystal's reviewer). At n = 100 per setting (400 pair
    records): the
    expected counts 40 / 10 / 10 / 40 (standard deviations 4.9, 3.0, 3.0,
    4.9), 5 / 45 / 45 / 5 (2.2, 5.0, 5.0, 2.2), 45 / 5 / 5 / 45 (5.0, 2.2,
    2.2, 5.0), 40 / 10 / 10 / 40; S = 2.80 with the standard deviation
    0.141 (sqrt(2 / 100)), so S above 2 by 5.7 standard deviations. THE
    VERDICT "S above 2 at 5 standard deviations" needs n >= 79 per
    setting (316 pair records: 0.8 >= 5 sqrt(2 / n)); at 3 standard
    deviations n >= 29 (116). THE PIN: n = 100
    per setting, S in [2.38, 3.22] (3 standard deviations), the falsifier S
    <= 2. MALUS at 256 records, H arriving, the + Node: 128 +- 24 at (1,
    1), 246 +- 9 at (5, 1), 199 +- 20 at (15, 8), 177 +- 22 at (3, 2) (3
    standard deviations of sqrt(n p (1 - p))); the expected values are
    the shares' 128.0, 246.2, 199.3, 177.2. THE OTHER COUNTING ROWS: the
    two slits' visibility and de Broglie's fringes' centroid already carry bands (0.96 +-
    0.02; one Node) that the binomial spread at their records (1024 and
    2048 over 201 and 121 pixels) lies inside; the generator's map prints
    the binomial band beside each on regeneration.
  - (4e) THE EMITTER'S RESIDUES (the physicist's two findings on the
    board, 2026-09-25, emitter-click 055de7be; DERIVED HERE). (i) A body
    whose excited record is reseeded identically after every click, with
    no coupling to the light on the board, repeats its remainder at the
    centre Node and births ONE residue every time (his chain: 214, 214,
    214 on W = 700): the algebra's own answer, a deterministic law with
    an identical start gives an identical cycle, a perfectly periodic
    source. (REVISED at the model owner's word of record 1962: the residues spread by the remainder KEPT at the body's Nodes through its reseed, 9.34 (2), computed, with no coupling; the coupling of 8.5 is retired, 9.34 (B); the reading that follows is HISTORY.) THE RESIDUES SPREAD ONLY BY THE BOARD'S OWN BACK-ACTION: the emitting body's COUPLING (g, G) to the family it births (8.5), by
    which the photons already on the board act on the excited record's
    rows (a one-unit change of a row changes the next remainder by
    numerator mod 3 denominator, so any back-action spreads them), and
    which an emitter carries because it radiates (a body that births
    light and is not coupled to light is a write and no source). So
    EVERY EMITTING BODY DECLARES (g, G) FOR ITS BORN FAMILY on its Nodes,
    the one-Node emitters [801, 700] included; the equidistribution of
    the residues so born is COMPUTED on the engine (owed: a chain of 100
    births with the registered G [1, 50], g [1, 1000], the chi-square
    against the wheel). WHAT THE BACK-ACTION CAN SPREAD (DERIVED HERE):
    only what the board holds at the reseed. The state at a reseed is the
    seed, the record just born (the same profile at every birth) and
    whatever earlier records are still on the board; a world whose born
    records all leave (their click at a receiver or the face) before the
    next reseed has the SAME state at every reseed and repeats one
    residue exactly, coupling or not, by the determinism of 2.7. The
    residues spread only where records are still in flight at the
    reseed, and then as a deterministic walk on Z_W whose cycle the
    chi-square measures. So the chi-square is read PER WORLD (the Malus
    bar's 256 births in 3800 ticks are about 15 apart against a transit
    of 7 and more, so they overlap; the Bell layer's likewise), and a
    world whose residues cycle short is cured by memory (a longer board,
    a torus, a denser stock), never by a draw. (ii) The excited record's own residue read at its
    (re)seed is 0 (the seed's remainders are 0), so its rung is T / (2 W)
    and it clicks at the first interval with any flux, one birth per
    interval: WITHDRAWN as a reading point. The excited record's residue
    is read from its own remainder at the centre Node AFTER ITS FIRST
    ADVANCE (the seed's remainders are 0 at the write and nonzero after
    one step of the rule), and the rung compares from that interval on;
    the born photon's residue is the excited record's remainder at the
    click, as built. The first excitation of a run then has the residue
    the generator's seed gives after one step, the same in every run of
    that world (deterministic, 2.7), and every later one differs by the
    back-action of (i).
  - (4c) THE FIRST-RUNG ROWS (the moving mass's energy, Sagnac, the light clock, the redshift)
    DO NOT CHANGE: a first rung is the interval at which 2 W C first
    reaches T, the u = 0 rung, and reads no residue. They move only with
    the flux form of (3), already ordered.
  - (4d) WHAT THE PHYSICIST CHANGES: the birth reads the clicking record's
    remainder at the birth's centre Node and sets u and W from it; the
    loader refuses `residue_order`, `residue_seed` and a declared `wheel`,
    and refuses a birthing Node whose pair is poorer than 500; the wells
    of (4a) regenerated to rich pairs and the crystal's light index
    declared; the Bell worlds at n = 100 per setting, Malus at 256, their
    registers carrying the expected counts and the 3-standard-deviation
    bands of (4b); the readers report a count against its band.

**(5) WHAT IS LEFT OF THE PARTS (DERIVED HERE).**

| The word | What it is in the one element | Declared by the world? |
| --- | --- | --- |
| a family | an index of the summands, and the operator's pair for them | its vacuum pair and quantum: yes |
| a record | a summand of v, one quantum | the seeds at interval 0 and the born profiles: yes; the rest is born by clicks |
| a body | a region of the operator where a family's pair differs from the vacuum's | yes (a cube, a pair) |
| a tool | a region of the operator with its integers, and at most a birth and a name | yes |
| a face | the operator's zero row beyond the border | the board's extents: yes |
| a receiver | a NAME the host gives a set of Nodes, on records' ladders; the rung's wheel is the record's own, born with u (4), not the receiver's | yes (a name) |
| the emitter's stock, the born profile, the crystal's branches | the birth's data | yes |
| the residues | one integer per summand | yes, or the rule's own remainder (4) |
| the click, the birth, the push | the map S and its one deletion | no: the law |
| a lamp, a table, a take, a grace, a completion | nothing: names of retired forms | no |

So THE WORLD FILE DECLARES: the board's extents; the families (a pair and
a quantum each); THE OPERATOR (every region where a pair, a coupling or an
axis differs from the vacuum, as cubes); THE INITIAL ELEMENT (the seeds, one
per bound body, the composed modes of 9.9); THE BIRTHS (a body's stock and
born profile, a crystal's branches and clocks); THE NAMES (the
receivers' sets and the ladders that name them; no wheel: the rung's
wheel is the record's, (4)). Nothing else, the residues included (4). THE GENERIC ENGINE IS: one
step of S on the one element, then the click (E the flux, D the rung, X
the deletion, E^T the birth) on the summands whose ladders name a set.

**(6) EQUIVARIANCE, STATED ONCE (IN THE ALGEBRA, 1.1 and 1.6; the form
here DERIVED).** The map S is a function of the world's declared data w
(the operator, the names) and the state v. For every g in the cube group and every
translation of the torus, S(g . w, g . v) = g . S(w, v): the law is
covariant; a world breaks the symmetry only through w. The click commutes
with g in the same sense (the ladder's detectors move with the world). This
is the statement the property test of 9.20 checks.

**(7) MARKS.**
- PROVED: the one operator and its modes (8.2); the stability condition;
  the flux identity; the remainder's range.
- DERIVED: the one element; the flux as the one reading and what it
  retires; the parts as regions, summands and names; equivariance's form.
- COMPUTATION: the flux check; the remainder's equidistribution.
- CARRIED: the push (8.11): the regions' step and its stress as the flux
  of momentum. With it, momentum between clicks is carried, not proved.
- ADOPTED: the residue from the law (4); bound tool bodies of a holder
  family, at most three families, one border (record 1875).
- WHAT CHANGES FOR THE ENGINE (the physicist), beyond 9.18 (7): E as the
  one-way flux at every set, and T as the record's I (the take, the grace,
  the own take, the exemption and the driven mask retire with them); the
  spectral load check; the born pair as the world's integers (9.17 (6)); the
  residue's source if the owner takes (4).

### 9.20 The property test of the board, as the algebra gives it (the Boss's order of 2026-09-24, 22:00Z (2026-09-25 on the Israel clock); the owner's word of 22:10Z: "he only needs to verify it, because it is an algebraic test of the families he wants, before a code test"; ADOPTED, record 1875)

**(A) THE ALGEBRA'S VERIFICATION FIRST, property by property, per family
and for the families together (the owner's word).** Each property is read
off the one map S of 9.19 before any code; its mark is the mark of the
line of the algebra it follows from.
1. EQUIVARIANCE UNDER THE CUBE GROUP. Per family: the step is (B) the pair on the
   six reads, (T) the shift and (D) the division, and the six reads are
   the orbit of one Port under the cube group (1.1), so the step at g . x on g . w
   is g applied to the step at x on w; the remainder is per Node and moves
   with it. Together: the coupling adds (B) between the two families' rows
   AT THE SAME NODE (8.5), a scalar entry, invariant under every g; the
   axes (a, b) and the hand change sign together under a reflection (9.4);
   the push sums the stress over the outer Ports, an orbit (8.11). PROVED
   for the rule (1.1, 8.1), the coupling (8.5) and the reading (9.19 (3)
   is a bilinear form of the two ends of a Link, carried with the Link);
   CARRIED for the push (8.11).
2. TRANSLATION ON THE TORUS. The same, with the translations (1.6): the
   reads are the same six offsets at every Node. PROVED per family and
   together.
3. CONSERVATION BETWEEN CLICKS. (a) Content: nothing but a click or a
   birth changes the summands (9.17): exact, DERIVED. (b) Per family the
   form I is conserved exactly before the remainders and obeys the exact
   remainder identity with them (8.2, PROVED); together, J = I_m + alpha
   I_l + the cross term is conserved exactly before the remainders (8.5,
   PROVED). (c) Momentum: on a homogeneous board each character is an
   eigenvector of S, so its wave vector is exact (1.6, PROVED); at a
   body the difference goes into the body's vector by the push, CARRIED
   (8.11).
4. REVERSIBILITY EXCEPT THE CLICK. Per family: the step is a bijection
   of (level, remainder) with the exact inverse a_before = ceil(m / (3
   den)), r = 3 den a_before - m (8.8, PROVED). Together: the coupled step
   is two such bijections in a column order, each reading data the other
   leaves in place, so it is inverted in the reverse order (DERIVED HERE,
   one line). The click deletes a summand and has no inverse (8.8).
5. LOCALITY. The step at a Node reads the six neighbours and the Node's
   two families only (8.1, 8.5), so a change at one Node reaches
   Manhattan distance m at interval m and no further; the reading reads a
   Link's two ends (9.19 (3)); the push reads the outer Ports (8.11).
   PROVED per family and together; the click's deletion is the law's one
   non-local act (POSTULATES.md section 10).
6. ONLY THE CLICK READS. The step is one function of the seven inputs at
   every Node (the pair, the row with its remainder, the six reads), with
   no branch on a name or a value (9.5, 9.7); the only comparison on the
   state is the rung. DERIVED (the gate of 9.5 reads the code for it).
   The residue enters the rung alone, so two elements that differ only in
   their residues evolve identically until a click (DERIVED).

**(B) THE PLANTED BOARDS.** Six properties of the one map S of 9.19, each a test on a small world
that is none of the measured experiments, each with its expected value. Every test
runs headless, on integers, and compares arrays bit for bit unless the
expected value says otherwise. The small world: a cube of 12 x 12 x 12
(periodic on every axis), light's family [77, 25] and a massive family
[800, 809]; one well of side 2 at the vertex (3, 4, 5) with the pair
[800, 801] seeded on its composed mode; one light record born at (8, 2,
7) on one Node with the branches [[0, 1], [1, 1]] (both labels), its
residues supplied by the TEST HARNESS (a permutation over W = 8, an
input of the test and not a world key; the engine's u is the law's
remainder, 9.19 (4), and the harness may read it from the law instead,
the six tests holding for either source by 6c); one receiver of one
Node at (9, 9, 2) named on the record's ladder; 60 intervals.

1. EQUIVARIANCE UNDER THE CUBE GROUP. For each of the cube group's 48 elements g: apply g to
   the world (every cube's vertex and orientation, every axis (a, b)
   with the hand's sign, the receiver's Node) and to the initial element
   (every seed's array, the label rows exchanged where det g = -1), run
   60 intervals, and compare with g applied to the reference run's
   state. EXPECTED: identical arrays at every interval, remainders
   included, and the same click at the same interval (48 of 48). The
   rule's remainder is per Node and moves with the Node, so equality is
   exact.
2. TRANSLATION ON THE TORUS. For each of 6 shifts (one Link along each
   axis in each sign) and one diagonal shift (3, 5, 7): shift the world
   and the initial element, run, compare with the shifted reference.
   EXPECTED: identical, bit for bit, 7 of 7.
3. CONSERVATION BETWEEN CLICKS. (a) CONTENT: the sum of the quanta over
   the summands per family is constant at every interval before the
   click, and drops by exactly one quantum of the light family at the
   click. EXPECTED: exact. (b) THE FORM I: per record, I(t) plus 8.2's
   remainder term is the same integer at every interval. EXPECTED: exact
   (the remainder identity). (c) MOMENTUM: on the homogeneous part of the
   run (the well removed, one plane-wave record along x with the phase
   per Link [77, 25]), the record's phase per Link along x, read as the
   character's index by the reader of 4.11, is the same integer at every
   interval. EXPECTED: exact. With the well in place the record's
   momentum changes at the well and the well's vector gains the push:
   the total is CARRIED (8.11), and the test prints both as GAMEBOARD
   with no expected value.
4. REVERSIBILITY EXCEPT THE CLICK. Run 60 intervals with the receiver's
   name removed from the ladder (no click); then run 8.8's inverse map 60
   intervals. EXPECTED: the initial element returns bit for bit,
   remainders included. With the receiver named: the record clicks at
   some interval t_c; the inverse run from 60 returns the state at t_c
   without the deleted summand, and the difference from the forward
   state at t_c is exactly that summand's rows. EXPECTED: exact.
5. LOCALITY. Two runs from initial elements that differ at ONE Node of
   one record by one unit of `now`. EXPECTED: at every interval m the
   difference of the two states is supported inside the Manhattan ball
   of radius m about that Node (a difference outside it is a defect),
   and the difference is nonzero somewhere at every m <= 12.
6. ONLY THE CLICK READS. (a) STATIC: the code gate of 9.5, read by the
   mathematician: the only comparison on a value of the state is the
   rung, the only branch on a name none. (b) DYNAMIC: for 1000 random
   integer states on the small world, evaluate the step at two Nodes
   whose seven inputs (the Node's pair, its record's row and remainder,
   the six neighbours' rows) are equal by construction. EXPECTED: equal
   outputs, 1000 of 1000. (c) THE CLICK'S BLINDNESS: two runs whose
   records differ only in their residues u give identical states until
   the first click. EXPECTED: identical, bit for bit, at every interval
   before the earlier of the two clicks.

Each expected value is DERIVED from 9.19: 1, 2 and 6 from the map's
covariance (9.19 (6)) and its dependence on the seven inputs alone; 3 (a)
and (b) from 8.6 and 8.2; 3 (c) from 1.6 on a homogeneous board; 4 from
8.8; 5 from the six reads (8.1). A failure of any of them is an engine
defect, never a change of the law.

7. NO SIGNALLING (9.25 (6), the model owner's record 1888). Two Bell
   worlds differing only in Bob's axis ((1, 2) against (3, 1)): Alice's
   two receivers give identical counts and identical click intervals,
   record by record, bit for bit, and her shares are abs(v_+)^2 :
   abs(v_-)^2 of her own projection (1 : 1 for HV + VH); the same with
   Bob's polariser moved farther from the crystal. Expected value: no
   difference at Alice at all; the joint counts differ as the joint
   weights say.

**(C) THE PROTOTYPES' READING (COMPUTATION, 2026-09-24, outside the engine:
[docs/designs/lab_tools/board_algebra.py](designs/lab_tools/board_algebra.py),
its record `board_algebra.out` beside it; the model owner's word: "try it in
code and say whether it works").** The one element and the one operator of
9.19 built from scratch on integers, 300 lines: a torus of 8 x 8 x 8, the
rule with a pair per Node and the remainder, the flux reading, the rung,
the deletion, the emitter as a clicking body (its seed the composed
operator's bound mode, its norm one period's one-way flux into its centre)
and the birth with before = -now; W = 8 and the residues a permutation
supplied by the test harness (an input of the prototype, not a world
key). Every expected value of the six tests met:
- THE INITIAL STATE FROM THE OPERATOR: the well [800, 801] of side 2 on
  [800, 809] has the largest eigenvalue 1.978065 (below 2: stable), the
  mode's clock 0.14824 below the vacuum's 0.14930 (bound); seeded on that
  mode, the record rotates (two sign changes per period at the centre) and
  its form I changes by 2.4 x 10^-4 over a period at the amplitude 4096,
  the remainder's grain.
- THE EMITTER AND THE RECEIVER: three excitations click at the intervals
  4, 43 and 72 for the residues 0, 6 and 4 (the expected waits 3, 34 and 24
  of a period of 42); each photon clicks at the one-Node screen 11 Links
  away when its offer C, the one-way inward flux, reaches (2 u + 1) / (2 W)
  of its norm T: C / T = 0.440, 0.211 and 1.015 at the intervals 72, 81
  and 166 for u = 3, 1 and 7 against the rungs 0.4375, 0.1875 and 0.9375
  (the offer is read once per interval and crosses the rung by up to one
  interval's flux). The physicist found a factor of 3 in the prototype's
  flux (2026-09-24, 22:50Z, CONFIRMED): `flux_into` returned 3 L times
  the sum of 3 G_ij and now returns L times that sum, the units of
  `form_I`; before the correction the receiver clicked at 38, 65 and 126,
  the emitter's clicks and the six tests unchanged (its norm and its offer
  scale together).
- (1) 48 of 48 transformed worlds identical bit for bit, remainders and
  clicks included; (2) 7 of 7 shifts identical; (3a) the quanta constant at
  every interval (photons alive, photons clicked, the stock); (3b) the
  form I's drift 9.7 x 10^-4 at the amplitude 4096 and 4.2 x 10^-5 at
  65536, falling with the grain; (3c) a plane wave's wave number constant
  on the homogeneous board; (4) 40 steps and 40 of 8.8's inverse return the
  element bit for bit, and only the clicked summands are not recoverable;
  (5) a one-unit change stays inside the Manhattan ball of radius m at
  interval m, m = 1 to 7; (6b) equal seven inputs give equal outputs, 1000
  of 1000; (6c) two runs differing only in their residues are identical
  until the first click.
The engine's test of 9.20 runs the same six on the engine; this prototype
is the algebra's own reading of them, not a run of the engine.

THE FAMILIES TOGETHER (COMPUTATION,
[docs/designs/lab_tools/board_algebra_coupled.py](designs/lab_tools/board_algebra_coupled.py),
its record beside it): the same torus with the massive kind [800, 809],
its well [800, 801] of side 2 seeded on the composed operator's bound
mode, and light [1, 1] coupled on the well's Nodes with g = 1 / 1000 and G
= 1 / 50 in 8.5's column order, the couplings' denominators folded into
the rows' walls: (1) 48 of 48 transformed boards identical bit for bit
after 40 coupled steps; (2) 7 of 7 shifts identical; (3) J's relative
drift at most 9.1 x 10^-4 over 200 intervals at the amplitude 4096 (the
grain), the well radiating into light (I_l from 0 to 1.4 x 10^4 against I_m
1.8 x 10^8); (4) 40 coupled steps and 40 of the reverse-order inverse
return both families bit for bit, remainders included; (5) a one-unit
change of light at one Node stays inside the Manhattan ball of radius m at
interval m across the coupling. THE ENGINE'S TEST is (B) run on the
engine, per family and together; (A) is its verification in the algebra,
done before it.

### 9.21 The implications of one algebra (the owner's word of 2026-09-24, 22:15Z (2026-09-25 on the Israel clock): "what is certain is that the whole world is one big algebra"), one line each, marked (ADOPTED, record 1875)

1. THE WORLDS. A world is its initial element (integers at interval 0)
   PLUS its operator (the pairs, couplings and axes per region) PLUS the
   births' data PLUS the receivers' names (no wheel): DERIVED (9.19 (5)). Not "the
   initial element alone": the operator is the world's second declaration,
   and it is data, not a rule. A world file may declare exactly those four
   and the board's extents; it may not declare a residue, a wheel, a take,
   a grace, a train, a rate, a heading or a table: DERIVED (9.19 (4)
   ADOPTED; 9.12; 9.17). A tool's test world is a small planted element on
   a small operator: DERIVED (9.20 (B)).
2. THE FIFTEEN. Survive as declared inputs: the extents, the families'
   pairs and quanta, the bodies' cubes and pairs, the couplings, the axes,
   the emitters' stocks and born profiles, the crystal's branches and
   clocks, the receivers' names, the amplitudes. Become DERIVED: the
   wheel (the birth Node's pair),
   the seeds (the composed operator's modes, 9.9), the trains (a born
   profile's length), the residues (the law's remainders), the tools'
   shares (the operator's scattering), the first rungs (the flux), the
   counts' bands (binomial at the records). Retire: the tables, the takes,
   the rates, the grace windows, the headings, the two-arm emitter, the
   sponge faces: DERIVED (9.18 (5), 9.19).
3. THE ENGINE. One step of one operator on the one element (the rule per
   family with the coupling, the axes and the push) plus the click (the
   flux, the rung, the deletion, the birth): DERIVED (9.19 (5)). No place
   in it for: `_drive`, `_source` as a birth, `_block_births`, the grace,
   the exemption, the own take, the take masks, `_complete`, the close,
   `escaped`, `TableBody`, `read_pair`, `half_angle`, `Splitter`, the
   residue orders and seeds, the `massive_kind` branches in the law's
   path: DERIVED (9.18 (5), 9.19 (3) and (4)).
4. THE TESTS. The property test is the test of the one operator: verified
   in the algebra in 9.20 (A) (PROVED for the rule, the coupling, the
   reading, reversibility, locality; DERIVED for content and the blind
   step; CARRIED for the push), then computed on planted boards (9.20
   (C), all met), then built on the engine from that section: the order
   the owner set. AND THE RUN IS COMPARED ONLY THROUGH CLICKS (the
   owner's word of 22:39Z: "check clicks only in the experiment, that's
   it"): an experiment's result is its clicks, the counts and the first
   rungs on the receivers' names; everything else about the run is proved
   in the algebra (9.19, 9.20 (A)), computed on planted boards (9.20
   (C)), and checked at load (9.22 (3)); a GameBoard reading is a
   diagnostic and never a result (Highlights, the readings by type).
5. THE FAMILIES. A family is an index of the summands and the operator's
   pair for them, nothing else: DERIVED (9.19 (1)). The number of families
   is fixed by the world's needs and by one pair per family per Node: the
   families a tool acts on or reads, plus one holder for bound tool bodies:
   at most three: DERIVED (9.18 (2)); DECIDED (record 1875): a holder
   family, distinct from the experiment's matter.
6. THE CONSERVED QUANTITIES. Exactly conserved by the one algebra: the
   content (the quanta) between clicks (DERIVED); per family the form I,
   and together J, before the remainders, with the exact remainder
   identity on integers (PROVED, 8.2, 8.5); a character's wave vector on a
   homogeneous board (PROVED, 1.6); the equivariance itself (PROVED).
   Conserved by declaration, not by the algebra: momentum at a body (the
   push, CARRIED, 8.11). Not conserved: nothing else is claimed.
7. WHAT THE STATEMENT RULES OUT THAT IS STILL CARRIED. (a) The push as a
   separate rule with declared integers (Q, S, M, 56 d, the tie): it moves
   the operator's regions from outside the operator; the one algebra
   would have the regions move by the law's own values, which needs the
   body's own record to carry its momentum and the pairs to follow it: OPEN
   (9.15, a proof owed that the stress is the flux). (b) The per-family
   faces of main: DECIDED, one border (record 1875). (c) The cosine
   tables: DECIDED (the owner, 2026-09-24, 23:00Z (2026-09-25 on the Israel clock): "if it is not used,
   throw it out; no formulas on the board"; superseding his word of
   2026-09-21 that the table stays for the click's Gram matrix, which the
   flux reading has replaced): the engine carries NO TABLE; the generator
   computes the born pairs and profiles and writes integers, and the
   phase readers are host tools outside the engine. (d) The float Lanczos of the
   generator: HOST, outside the law, its integers checked at load. (e)
   The one non-local act, the click's deletion of a summand across the
   board: not ruled out; it is the algebra's one deletion (8.8,
   POSTULATES.md section 10).
8. LARGE BOARDS (the model owner's question of 2026-09-24, 23:10Z (2026-09-25 on the Israel clock),
   through the Boss: "large boards' scalability, in a few marked
   lines"), each line marked.
   - (a) THE STEP: per interval, per alive record, per family, at every
     Node of the record's rows six reads, three multiplications and one
     division with its remainder (8.1); the cost is Nodes x alive records
     x labels per interval, LINEAR in the Nodes, with no global sum
     (PROVED: 8.1 is local); the storage three integers per Node per row
     (now, before, remainder), the same product. The alive records are
     bounded by the world, not by the stock: a clicking body births in
     turn (9.17), so at most (a record's lifetime on the board) / (the
     birth's period) are alive at once (DERIVED: the two slits, 485
     Links at a period of about 42, some 12 photons alive at once
     whatever the stock of 1024, about 4.5 million integers); the run's
     length is the stock times the period, LINEAR in the stock.
   - (b) THE INITIAL STATE: the composed operator's bound mode at each
     occupied body by the generator's Lanczos on the sparse operator
     (seven entries per row), Nodes per iteration and tens of iterations
     (the gap above the band's top sets the count): LINEAR (DERIVED); the
     prototypes' dense eigen-decomposition (Nodes^3) is theirs, not the
     generator's, and stops at some 10^4 Nodes. The bound mode's tail
     falls exponentially away from its body (bound: above the band,
     PROVED 8.3), so at the declared amplitude the integer profile is
     zero beyond a radius the gap fixes: the summand is a window about
     its body; the load check of the profile is the eigen-equation's
     residual, one application of the operator, at most Nodes. The gap
     is the body's, COMPUTED: on a chain every body binds ([801, 700] on
     [7, 8]: 1.90193 against the top 1.75), on a layer weakly (1.75218),
     on a cube a one-Node body does not bind in the large-board limit
     (1.7512, 1.7506, 1.7504 on 8, 10 and 12) and a body of side 3 does
     (1.8609): a cube's emitter body has the extent the load check's
     bound decides, never one Node.
   - (c) THE CLICK: the reading is the flux through the set's Ports, the
     Ports' count per alive record per interval (a screen of 201 Nodes
     on a layer, some 800 Ports); the ladder one integer per record per
     set; the deletion drops the record's rows, at most its window, the
     one non-local act, a host memory operation and never a computation
     across the board (8.8): LINEAR and once per click (DERIVED).
   - (d) THE INTEGERS: the norm T sums a record's squares over its rows,
     amplitude^2 x support, and the rung's 2 W C reaches W x that: at
     the amplitude 4096, 10^6 Nodes and W = 2403 about 2^56, at 65536
     about 2^64 (COMPUTED): the ladder's integers are arbitrary-precision
     or the amplitude is bounded at load, a LOAD CHECK, the one thing
     that would fail silently otherwise.
   - (e) WHAT DOES NOT SCALE: nothing in the law; in the host, (i) a
     board-wide dense vector per record where the record is a window
     (the prototypes' form; the window is exact by locality, 9.20 (5): a
     record born at one Node is zero outside the Manhattan ball of its
     age, and inside it any cut is an approximation the algebra does not
     licence: a host matter, OPEN); (ii) the prototypes' dense
     eigen-decomposition and 48-fold equivariance test, which run on
     planted boards of 8^3 only (9.20 (B)), never on the measured experiments'
     boards; (iii) the tensor's 2^n joint weights of a record of n arms
     (n = 2: four integers, 9.23); (iv) a declared rate of births,
     retired (the emitter births in turn).
9. WHAT IS DROPPED (the model owner's word of 23:10Z: "work only on the
   adopted line; drop anything older not needed, and tell me what you
   drop"). Dropped from the line, kept in this chapter as derivations
   only: 9.14 (a), the angle as the wheel's translation (its one use is
   the retarder's phase in 9.23 (2), as a pair per label, not a wheel);
   the exact pins at W = 20 (Bell 181 of 64, Malus's exact counts), the
   pins being distributions (9.19 item (4b)); 9.10 item 1's owed computation
   of the click's Gram matrix from the table, the flux reading the click
   (9.19 (3)); 9.17 (2)'s emitter with a table, the born pair being two
   integers (9.17 (6)); the specification's sections 0 to 12 and
   CRYSTAL_ALGEBRA.md as history, parts A and B the live specification.
   Not dropped, older and needed: chapter 8 (the rule), 9.1 to 9.13 (each
   tool's operation), 9.14 (b), 9.15 to 9.17; the ramp of
   DECLARATIONS.md section 8 until 8.4 is settled. One stand-in named:
   the prototypes' residue is a declared permutation over W = 8, the
   engine's is the law's remainder (9.19 (4)); the prototypes'
   residue-blindness (6c) holds for either, and no prototype on the
   remainder is owed, the engine's test of 9.20 being the test.

### 9.22 What defines a family and an experiment, and the initial state as a function of it (the model owner's word of 2026-09-24, 22:28Z (2026-09-25 on the Israel clock), through the Boss: "you need to understand what really defines an experiment, and a family, in order to reach a correct algebraic initial state"; ADOPTED with the package of record 1875)

**(1) A FAMILY (DERIVED HERE from 8.1 and 3.6).** The minimal data: its
VACUUM PAIR [numerator, denominator] and its LABEL MODULE (Z^2 per arm
for the hand; Z for a family with no hand). Nothing else. Its quantum is
the unit of its content (the counting unit, a convention of the reading,
not a datum of the law); its clock (`phase_per_link`, the born
character's frequency) is a datum of the BIRTH that makes its records,
not of the family. What follows from the pair alone:
- its rest frequency, cos omega_0 = numerator / denominator (8.1): light
  has none ([1, 1]); a massive family has one, its mass;
- its operator block on an empty board, **M**_F = (numerator / (3
  denominator)) **A** (8.2), whose modes are the characters of the torus
  with the band 3 cos omega = (numerator / denominator) SUM of cos k_i
  (8.1, PROVED);
- its stability on any board: every mode a rotation exactly when the
  composed operator's largest eigenvalue is below 2 (9.19 (2), PROVED);
  numerator <= denominator is sufficient;
- whether it can be a body: only a massive family (8.3, PROVED);
- its remainder's range at a Node with the pair in lowest terms, 3 x
  denominator / gcd(numerator, 3) (9.19 (4), PROVED).
The number of families in a world is fixed by one pair per family per
Node (9.18 (2)): light, the experiment's matter, and the holder of the
tools' bodies; at most three (ADOPTED, record 1875).

**(2) AN EXPERIMENT (DERIVED HERE from 9.19 (5)).** The minimal data,
and nothing else:
- THE BOARD: the torus's extents per axis, and per axis periodic or open
  (an open axis carries the face receiver at its border, 9.19 (3) (a);
  ONE border for every family, ADOPTED).
- THE FAMILIES: at most three, each by (1).
- THE MATERIAL MAP: which Nodes carry which pair per family (the vacuum's
  everywhere else), which carry a coupling (g, G) between two families,
  which carry an axis (a, b); every such region a cube by its vertex and
  edge, the bodies of the tools among them.
- THE OCCUPATION: which bound bodies hold quanta, how many, at which
  amplitude; which packets of a family are on the board, how many quanta,
  at which amplitude and width, where; which bodies carry a stock of
  excitations and birth which family with which clock and which born
  profile; which body births a pair (the crystal's branches and clocks).
- THE MOMENTUM: every entry carries its total momentum as one of its
  integers, the wave vector **K** of its character, 0 at rest (DECIDED,
  the model owner, record 1885, 2026-09-25 on the Israel clock); a packet
  moves by **K** under the law (9.24 (2)); a region of material has
  **K** = 0 in the one algebra (9.24 (3)). There is no acceleration: a
  moving entry is written moving at interval 0 and its energy of motion
  is part of the initial state, conserved; no ramp (DECIDED, record 1884;
  the ramp of DECLARATIONS.md section 8 retires).
- THE NAMES: the receivers' sets, and the ladder of each birth (the sets
  its records name, the face receiver last).
NOT PART OF IT (refused at load): a residue, a wheel, a seed written by
hand, a rate, a train, a heading, a take, a grace, a table, a per-family
border, a ramp.

**(3) THE INITIAL STATE AS A FUNCTION OF (2) (DERIVED HERE from 8.7, 9.9
and 9.19).** The initial element is

    v_0 = SUM over the occupied bound modes of (the quanta) x (the mode's integer profile at the declared amplitude, at both levels), with every remainder 0,

where the modes are the eigenvectors of the COMPOSED operator of the
body's family (every region of that family in place, 9.9), one summand
per occupied body, each the body's first excitation where the body births
(9.17 (4)), plus one summand per PACKET: its profile times the character
of its momentum **K** at the two levels, integers after rounding, an
exact solution of the homogeneous law from interval 0 with no ramp (9.24
(2), DERIVED; the model owner's record 1884). A region of material does
not move (9.24 (3)); the stepped well of 8.4 and its ramp are history.
Nothing else is on the board at interval 0: no light record, no response
record, no remainder (9.9).
- EXACT INTEGERS: the summands as written (the levels and the zero
  remainders), the amplitude, the quanta, the material map; the operator
  itself (integer pairs); the born profiles' integers.
- A HOST COMPUTATION, ROUNDED: the mode's real profile (the generator's
  Lanczos vector, float, unique up to sign and scale), rounded to the
  nearest integer at the amplitude; the character's cosine at each Node
  for a moving body, and the born pairs and profiles (the generator's
  own cosines). Their integers, once written, are the world's data; the
  float that produced them is never read by the law, and the engine
  carries no table (the owner's word of 23:00Z).
- THE LOAD CHECK REFUSES: a body whose Nodes are cut or overlap another's
  (9.9 (4)); a composed operator with a mode at or above 2 (9.19 (2)); a
  body's summand that is not the composed mode's integer profile bit for
  bit at both levels, or with a nonzero remainder (8.7, 9.9); a birth
  Node whose pair gives fewer than 500 remainder values (9.19 item (4a)); two
  near-degenerate wells whose hybrid share exceeds the reading's band
  (9.9 (3)); any key of the refused list of (2); a board with neither a
  periodic axis nor a face receiver on an open axis (record 15); a family
  count above three; a body of a family a tool of that body acts on or
  reads (9.18 (2)).

**(4) THE FIFTEEN, EACH IN THE FORM OF (2), AND ITS FILE ON main 5b0e8a77
AGAINST IT.** "Today declares" lists what (2) does not allow; "lacks"
what (2) needs and the file has not. Every row's regeneration is the
World Generator's, its pin re-derived blind (9.19 item (4b), 9.17 (5)).

In the table a bracket pair is a PAIR [numerator, denominator] of a
family or a body unless it is named a born clock, a wheel, a rate, a
gap, a take or a momentum.

| Row | Its defining data in the form of (2) | Today declares, not allowed | Lacks |
| --- | --- | --- | --- |
| Bell (4 files) | the layer [30, 33, 1], periodic; light [1, 1] with the born clock [2464, 25], a holder family; the emitter body at (2, 16) with a stock of 100 per setting; the crystal body at (13, 15) side 3 with its light index and branches [[1, 1], [2, 1]]; two polariser bodies with the axes (1, 0) or (1, 1) and (1, 2) or (3, 1); their receivers; the ladders | a chain of 21 with an open x face; a lamp with rate, wheel, train, directions, `arms` 2 and `branches`, a residue seed; two table bodies with `phase_window`; the family `counter` | the crystal, the polariser bodies with axes, the emitter body, the holder family, the layer |
| Malus (4 files) | the bar of 8; light [1, 1] with the born clock [308, 25], a holder family; the emitter body at x = 0 with a stock of 256; the polariser body at x = 6 with the axis (1, 1), (5, 1), (15, 8) or (3, 2); its + receiver at x = 7 | a lamp with rate, wheel [159, 256], train 32, directions; a table body with `phase_window`; `counter` | the emitter body, the polariser body with its axis, the holder family |
| The two slits | the layer 160 x 256 grown to x >= 485 (the margin rule); light [1, 1] with the born clock [77, 25], a holder family; the emitter body at (20, 128) with a stock of 1024; the wall of gap cubes [1, 2] with its two openings; the 201 screen receivers; the face receivers; the ladder naming the screen | a lamp with rate [1, 4], wheel [1, 1024], train 32; the screen sets with a wheel 2^20; open sponge faces | the emitter body, the face receivers, the grown board |
| The pace fans | the layer 128 x 128; light [1, 1] with the born clock [77, 25], a holder family; two LINE emitter bodies (one along the axis, one along the diagonal) with born profiles of n wavelengths; the probes as a GAMEBOARD reading | a lamp with rate, wheel, train and four `directions`; open sponge faces | the two line emitters, the face receivers |
| The muon's moving clock | the layer 200 x 200, periodic; matter [3200, 3236]; the well [3200, 3227] of side 14 at (93, 93), one quantum, at rest and with the momentum [64, 0, 0] | nothing outside (2) (the `margin` key is the generator's label) | the moving summand as the boosted mode (the ramp stays until 8.4 is settled) |
| The moving emitter's redshift | the chain 4096 with the face receivers; light [1, 1], matter [156, 157]; the well [314, 315] of side 12 at 2994 with the coupling, a stock, its light birth, the momentum; the receiver at 4094 | `own_grace`, a receiver `wheel` 64, a light lamp with `directions` in the control; open sponge faces; a flat seed (regenerated on the mode since body-check) | the face receivers, the stock in place of `emits` |
| The round trip off a receding mirror | the chain; light [1, 1] with the born clock [2464, 25], a holder family; an emitter body with its receiver; the transponder body with the gap [1, 2] and the momentum k = 3 | the whole table form: the families post, source, cart and mass, `rerelease` and `pass` tables, a lamp with directions | everything: rebuilt as the transponder |
| Sagnac's two-way light times | the chain 3000 with the face receivers; light [1, 1], matter [800, 809]; two wells [800, 801] of side 12 at 700 and 772 with the coupling, a stock each, momenta; the receivers at_a and at_b; the ladders A -> at_b, B -> at_a | wells [800, 800] (3 remainder values); `own_grace`, `wheel`; open sponge x face; seeds computed alone | rich pairs, composed seeds, the face receivers |
| de Broglie's fringes | the layer 128 x 128; matter [800, 809] and a holder family; a matter emitter body with a stock of 2048; the barrier of gap cubes [1, 2] with its openings; the 121 screen receivers; the face receivers | a matter lamp with rate [1, 2], wheel [1, 2048], train 8; the family key `take` [-19, 86]; the take lines (252 cubes of the vacuum pair); the screen sets' wheel 65536; open sponge faces | the emitter body, the face receivers; the barrier and the screen as holder-family bodies, not matter bodies (9.18 (2)) |
| The moving mass's energy | the chain 200 with the face receivers; matter [800, 809]; a matter emitter body with a stock; the receiver at 104 | a matter lamp with rate [1, 8], train 8, directions; the family `take`; open sponge faces | the emitter body, the face receivers |
| The boxes (the boxed clocks) | the cubes 64^3 and 48^3, periodic; matter; one well [800, 801] of side 20 or 28, one quantum, at rest or with the momentum | the well [800, 800]; a flat seed (regenerated on the mode) | the rich pair |
| The deep well | the layer 128 x 128, periodic; matter; one well [800, 801] of side 40 at (44, 44) | the well [800, 800]; a flat seed (regenerated) | the rich pair |
| The light clock | the chain 674 with the face receivers; light [1, 1], matter [800, 809], a holder family; the well A [800, 801] of side 12 at 600 with the coupling and a stock; the mirror body [672, 674) with the gap [1, 2]; the receiver at_a at 612 | the well [800, 800]; `own_grace` 70, `wheel`; per-family faces (periodic for matter, closed for light); a flat seed (regenerated) | the rich pair, one border, the face receivers, the mirror as a holder-family body |
| The receding index (k = 3, k = 4) | the chain 4000 with the face receivers; light [1, 1] with the born clock [3565, 10000] or [1846, 10000], matter [156, 157] and a holder family; a light emitter body at 800 with a stock of 200; the medium body [314, 315] of side 24 at 1500 with the coupling and the momentum; the probe as a GAMEBOARD reading | a lamp with rate, wheel [2531, 4096], train 200, directions; the medium a SILENT body (seed 0) with `start` 3000; open sponge faces | the emitter body; the medium as a BOUND body of the holder family with its own record (ADOPTED: tool bodies bound), the index pin re-derived blind on it (COMPUTATION owed) |

THE THREE THINGS THIS TABLE SETTLES ONCE (DERIVED HERE): every lamp
becomes a body with a stock; every sponge face becomes a face receiver;
every well [800, 800] becomes [800, 801]. THE ONE THING IT OPENS: the
index rows' medium, silent today, becomes bound; its pin moves with it and
is re-derived blind before any run.

**(5) THE THREE ROLES, AND THE SHORT EXPERIMENT FILE (the model owner's
decision, record 1879, 2026-09-25 on the Israel clock; DERIVED HERE
where marked).** Three roles and no fourth. (i) THE BOARD GENERATOR is
the only writer, and it writes at interval 0 only: it reads the short
file of (2), composes the operator (the pairs, couplings and axes per
region, 9.19 (2)) and computes the initial element of (3), the bound
modes' integer profiles and the born pairs and profiles (9.17 (6));
after interval 0 nothing writes but the law. (ii) THE LAW acts at every
Node, at most one Link per interval: the rule per family with the
coupling, the axis and the push, the click and the birth (9.19 (5));
its locality is PROVED (9.20 (5)). (iii) THE CLICK READER is the only
reader: the flux on the named sets, the rung, the deletion and the
counts (9.19 (3)); a GameBoard reading is a diagnostic. THERE IS NO
WORLD WRITER: an experiment is a SHORT FILE of what is on the board, (2)
and nothing else: the extents and per axis periodic or open; the
families (pair and label module); the tools placed with their integers
(vertex, edge, pair, coupling, axis, stock, born clock and profile,
branches); the occupation (quanta, amplitude, momentum); the receivers'
names and the ladders. Everything the measured experiments' files declare beyond it
(the "today declares" column of (4)) is the generator's to derive or the
loader's to refuse; what the short file does not carry is DERIVED: the
initial element, the norms, the residues, the wheels, the pins' bands.

**(6) WHERE A TENSOR ENTERS, AND WHETHER IT MUST (the model owner's
word, record 1880, 2026-09-25 on the Israel clock: "write clearly in
the laws where a tensor computation enters and whether we must have it,
because the world generator gets complicated"; the Boss's lines of
record 1877 CONFIRMED line by line, with one precision).** THE ONE
TENSOR is the pair: a record of fixed rank 2 whose label module is Z^2
(x) Z^2, four integer weights on the joint labels, each arm's rows over
the Nodes as any record's (9.23 (1)); nothing of size Nodes x Nodes
exists, and a body's label matrix acts on one arm's two rows (9.16
(2)). IT IS REQUIRED only where entanglement is measured: Bell (a
product state gives S at most 2, PROVED: CHSH's bound holds for weights
that factor) and the circuits of 9.23; no other row of the measured experiments has
one. IT IS BORN only by the crystal, during the run, at an arriving
record's click (9.7 (b), 9.13); it is never written at interval 0, and
two separately born records are never joined (9.23 (1)). SO THE BOARD
GENERATOR WRITES ONLY VECTORS: each occupied mode's integer profile with
its labels, and the born pairs and profiles; it writes no tensor and
computes none; the crystal's branches are four integers of the short
file. THE TENSOR'S OPERATIONS live in the birth and in the pair's
click: the crystal's birth writes the four weights (**E**^T with the
branches); a body's label matrix acts on one arm (the bilinear form on that arm's
rows); the click of ONE arm alone reads the weights summed over the
other arm's labels, the partial trace (9.11 (d)), computed at that
click from the four weights and kept nowhere (the precision); the
click of both arms reads the joint weights R = J^2 (3.6); a joint body
(9.23 (3), not on main) acts on the four weights with a declared 4 x 4
integer matrix. Each is the bilinear form or P with declared integers, under the
declared contract of docs/ARCHITECTURE.md ("Integers, vectors and
tensors": a fixed rank 2, fixed dimensions 2 x 2, integer components,
no general tensor).

**(7) THE INITIAL STATE: STORED ONCE BESIDE THE SHORT FILE, CHECKED
EXACTLY AT LOAD (the Boss's question of record 1879, "recomputed at
every load, or stored once and checked"; DERIVED HERE).** Recomputation
at every load is NOT reproducible bit for bit across hosts: the
generator's Lanczos vector is a float whose last digits depend on the
host (the order of the sums, the threads, fused multiply-add) and on the
convergence tolerance, about 10^-8 relative; an entry within that of a
half-integer at the amplitude rounds differently on another host, and on
10^5 Nodes at the amplitude 4096 about 8 entries are expected within it
(COMPUTED: the window 2 x 4096 x 10^-8 per unit, times 10^5). Two hosts
would then load two worlds, and their clicks would differ. SO THE FORM:
the generator writes the initial element ONCE, as the world's integers
beside the short file (the profiles at both levels, the born pairs and
profiles, and for each occupied mode its clock as a rational [a, b], the
generator's rounding of 2 cos omega to a denominator b at least the
amplitude), and the loader CHECKS IT EXACTLY, in integers and with no
float: (i) the integers are the ones the generator wrote (the file's
hash in the short file); (ii) the eigen-equation's residual at every
Node of the profile p, abs(b x numerator_i x (S_6 p)_i - 3 x
denominator_i x a x p_i) <= b x (3 x numerator_i + 6 x denominator_i),
PROVED HERE as the bound for the rounded profile of an exact mode (each
entry off by at most 1 / 2, six neighbours, the clock off by at most
1 / b; a profile that is not a mode fails it by a margin of the
amplitude's order), exact in integers and the same on every host; (iii)
a / b above the band's top (bound) and below 2 (stable), rational
comparisons; (iv) the remainders 0, the amplitude's bound, the disjoint
Nodes, the rich birth Nodes, as in (3). What (ii) does not do: single
out the mode among near-degenerate ones (9.9 (3)'s hybrid share stays
the generator's, printed as GAMEBOARD), and check a moving body's
summand (8.4's product, OPEN, the generator's recomputation printed).
Recomputation at load stays a DIAGNOSTIC (the largest deviation
printed), never the check. IN ONE LINE: store once, check exactly in
integers; recompute only to print.

THE GENERATOR IS THE BOARD'S OWN OPERATOR, ITERATED (the model owner's
word, 2026-09-25: "the generator is iterative by nature; it starts from
a state until it reaches the desired one"; DERIVED HERE). The bound mode
is the top eigenvector of the composed operator **M**; the power
iteration v -> (**M** + 2 **I**) v applies the law's own read (the six
neighbours with the pairs at every Node) and nothing else, from any
start, and converges to the mode (PROVED: **M** + 2 **I** has nonnegative
entries, so by Perron-Frobenius its top eigenvector is the mode and the
shift keeps the lowest mode from competing), at the rate 1 - gap / (lambda
+ 2) per iteration, gap the distance of the mode's eigenvalue from the
band's top; Lanczos is the same read with inner products. So the
generator is the same algebra in another mode of use: the law STEPS the
operator (second order, every mode a rotation, reversible), the
generator RELAXES with it (first order, the top mode grows and the rest
decay), the click compares and deletes. Three consequences. (i) The ramp
was the board doing the generator's relaxation; record 1884 puts it
where it belongs, and nothing on the board relaxes. (ii) IN INTEGERS the
iteration is reproducible bit for bit: 3 den v' = num S_6(v) + 6 den v
with the remainder kept, renormalised by an exact shift by a power of
two when the levels pass the amplitude; the float Lanczos above is then
a host shortcut only, the stored state can be re-derived exactly on any
host, and the load check stays (ii) above (the residual). (iii) THE COST
of an experiment is the generator's iterations, each the work of one
board step (linear in the Nodes), about (lambda + 2) / gap of them per
e-fold (COMPUTED: 15700 for the muon's form, whose gap is 0.00025 in
lambda, 450 for the boxes' 0.0089; fourteen e-folds to 10^-6), plus the
run; for the two-qubit computer the generator's iterations are the gates
on 2^n weights, exponential in n, and the board adds the click, not
computing power (9.23 (7)).

**(7a) THE CHECK'S TWO READINGS AT bab3056a (the physicist's, 2026-09-25;
DECIDED HERE).** (i) WHICH OPERATOR A BODY'S SUMMAND IS THE MODE OF: the
top mode of the operator with THAT BODY ALONE among the material regions: every record-free material region (a mirror, a wall, a splitter, a medium, a barrier) in place, and every OTHER RECORD-CARRYING BODY's region replaced by its family's vacuum (the Boss's reading of record 1929, confirmed, record 1947 (C); 9.27 (B) (3) says the same), one summand per
occupied body as (3) says; the composed operator of every body in place
has, for two equal wells, the symmetric hybrid as its top mode, which is
no summand of one body (9.9 (3)), and a body's summand is not its
eigenvector (it tunnels at the hybrid share, 3.2 x 10^-6 over Sagnac's
run, the separate load check of 9.9 (3)). So THE RESIDUAL OF (7) (ii) IS
READ ON THE COMPOSED OPERATOR AT EVERY NODE OUTSIDE THE OTHER BODIES'
NODES, where the two operators agree; at the other bodies' Nodes the
operator carries their summands, and the mode's tunnel tail there
(10^-5 of the amplitude on Sagnac) is not this summand's to satisfy. The
physicist's reading CONFIRMED and this the rule; the two hybrids are not
the summands (they would put half a quantum in each well). (ii) THE
GENERATOR'S MODE: the three-term Lanczos without reorthogonalisation
gave the vector to 3 x 10^-4 and the stored profiles failed the bound by
6 to 860 times (COMPUTED by him); the accurate float mode (ARPACK's
implicitly restarted Lanczos at the machine's tolerance, scipy in the
generator and the diagnostics, never in the engine) passes the bound with margin (the worst residual 0.18 to 0.53 of it), and the integer power iteration of record 1898 is the reproducible form and THE GENERATOR ITSELF (below); the float eigensolver is a diagnostic beside it and the integer residual the gate, as (7) says. A
one-unit change at one Node stays within the bound and is admitted (it
changes the output, 9.20 test 8); a profile off the mode by the
amplitude's order is refused. THE INTEGER ITERATION'S FLOOR (his
computation at de363acb, 2026-09-25): from the Nodes' indicator the
integer power iteration of record 1898 reaches the mode within 78 units
at the amplitude 2^20 (the chain of 80, the gap 0.0105) and stays there
from 4000 to 16000 iterations: each step's rounding, about half a unit
per Node, feeds the next mode and is damped only by gap / (lambda + 2)
per step, so the iterate carries an admixture of the next mode of about
1 / gap units, its residual 0.43 of the bound against the float mode's
0.15, both admitted. DECIDED BY THE MODEL OWNER (2026-09-25, 04:10Z in Nature24's session, closing record 1898: "the iterated operator must become the generator itself, with the stop"; this paragraph's earlier line, the float mode as the writer and the iteration as the check, is withdrawn at his word): THE GENERATOR IS THE OPERATOR ITERATED WITH ITS STOP, from the Nodes' indicator, the clock the operator's quotient over the board in exact integers, the stop the residual bound of (7) (ii), the working amplitude at least 2^20 (built at a9ab486f, `iterated_mode`, read line by line and confirmed by the mathematician at 05:50Z); the float eigensolver is a diagnostic and never the writer; the stored integers with their stamp (9.22 (7) (i),
built at de363acb: the law identifier and the SHA-256 of the shape and
every seeded body's profile, clock and born pair, refused missing, of
another law or mismatched) are the world, and a regeneration that
differs by units within the bound is another lawful world with another
hash, never the same one silently. (iii) THE ONE-NODE EMITTER ON A LAYER (his
reading): the well [801, 700] on the holder's [7, 8] binds on a chain
(2 cos omega = 1.897 against the band's top 1.75) but on a layer only by
1.1 x 10^-3 (1.751147), its mode spread over 4200 Nodes: a source forty
Links wide. On the layer rows (Bell, the computer) the one-Node emitter
is therefore [699, 700] (2 cos omega = 1.9011, 69 Nodes above one
percent of its peak; W = 3 x 700 / gcd(1201, 2100) = 2100, above the 500
of 9.19 item (4a); [1001, 700] binds at 1.7946 but has W = 300 and is
refused); the chain rows keep [801, 700] (W = 700). The table of (8)
carries it. (iv) TRANSPARENCY, a load condition (DERIVED with 9.25
(11) (d)): every body whose Nodes a born record must ENTER to be read (an
emitter whose light returns to it, the other well of Sagnac, a moving
name's receiver, a medium) is transparent to that family at the born
**K**: the generator runs a train through the body alone on the vacuum
and reads its one-way flux 40 Links beyond against the norm, 0.99 or
above, refused below. Below it the coupling's scale is wrong, not the
placement: the physicist's reading at f0d2d745 that a body's coupling
reflects foreign light entirely contradicts g G = 2 x 10^-5 per Node
(while the source term -G delta(massive) is a CW radiation at omega_b
into light's family, about 10^5 per interval at the seed 50 x 2^20, which
swamps any reading sharing its record); it is re-measured on the train's
own record, OWED from him before the chain rows' files.
(v) TWO WELLS ON ONE BOARD, THE EXACT SPLIT (the physicist's two-well
statement for the model owner, 2026-09-25, given by him as an
approximation; DERIVED HERE and COMPUTED). The composed board is one
linear operator: the mode equation is (1 / 3) (**A** p)_i = lambda D_i
p_i with lambda = 2 cos omega and D_i = den_i / num_i, and a well lowers
D on its Nodes by Delta D = den_vac / num_vac - den_well / num_well (0.01
for [800, 801] on [800, 809]). Let p_A and p_B be the modes of each well
alone on the same board, lambda_0 their common rate for equal wells. On
the span of p_A and p_B (the two-level reduction, Rayleigh-Ritz on the
generalized problem) the composed board's two rates are lambda_+- =
lambda_0 (M_11 + t_11 +- (M_12 + t_12)) / (M_11 +- M_12) with M_11 =
sum_i D_i p_A_i^2 (the mode's D-norm), M_12 = sum_i D_i p_A_i p_B_i (the
D-weighted overlap of the two modes), t_12 = sum over A's Nodes of Delta D
p_A_i p_B_i (THE OVERLAP THAT SPLITS: the well's weight difference times
the two modes, summed over ONE well's Nodes) and t_11 = sum over B's
Nodes of Delta D p_A_i^2 (A's tail's weight in B's well, a shift common to
both). THE SPLIT to leading order in the tails is lambda_+ - lambda_- = 2
lambda_0 t_12 / M_11, the M_12 and t_11 terms entering at second order;
the modes are near p_A + p_B and p_A - p_B; a record seeded on p_A alone
is their half sum and beats between the wells with the period 2 pi / (omega_-
- omega_+) = 4 pi sin omega_0 / (lambda_+ - lambda_-). In the law's
integers Delta D_i = (den_vac num_well - den_well num_vac) / (num_vac
num_well), so t_12 multiplied by num_vac num_well is an integer sum. THE
CORRECTION BEYOND TWO LEVELS is the coupling of the pair to the band's
modes, of relative order (the tail / the gap), and it is what the exact
eigenproblem adds to the Ritz values. COMPUTED on a chain of [800, 809]
with two wells [800, 801] of side 12 (omega_0 = 0.10022, kappa = 0.1922
per Link), by the gap between their faces: gap 2, the exact split 5.917
x 10^-3 against the leading form 5.902 x 10^-3 (the Ritz pair 6.108 x
10^-3), the beat 213 intervals; gap 4, 4.042 x 10^-3 against 4.017 x
10^-3, the beat 311; gap 8, 1.872 x 10^-3 against 1.862 x 10^-3, the beat
672; gap 16, 4.005 x 10^-4 against 4.001 x 10^-4, the beat 3.1 x 10^3;
gap 32, 1.848 x 10^-5, the forms equal to four figures, the beat 6.8 x
10^4; gap 60 (Sagnac's wells of side 12), 8.5 x 10^-8, the beat 1.5 x 10^7
intervals; gap 80, 1.8 x 10^-9. THE LAWFUL DECLARATION (the physicist's
question (2)): two near wells are ONE body, the composed operator, and a
record on it is one composed mode with one clock (the sum or the
difference, each its own record if wanted); a record seeded on p_A is a
superposition of two rates, has no one clock a / b, and the clock check
of (7) refuses it. "Two bodies, two records" is lawful exactly when each
body's own mode is a mode of the composed board within the rounding,
which is the loader's residual check outside the other bodies' Nodes
((7a) (i)): the tail of one at the other's Nodes below one unit (on the stored integers: the profile 0 at every Node of every other body of its family AND at every Node of a zero face of the board on an open or closed axis, a load check that names the two bodies or the body and the face, the Node and the value when it refuses; a zero face is a boundary of the operator, so a profile that is not 0 there is the mode of the well and the wall together, a different body with its own clock; the well [800, 801] of side 32 in [800, 809] decays by 0.79337 per Link outside and needs 56 Links to a zero face at the amplitude 2^20, 73 at 50 x 2^20, COMPUTED, scratchpad tail_decay.py; the condition is on the body's own family alone, a body or a material region of another family being transparent to it by 9.34 (B)). The tail
scales with the amplitude and the bound does not, so the check reads the
seed: Sagnac's wells at the gap 60 carry A's tail at B's centre at 1.7 x
10^-6 of the peak, 1.8 units at 2^20 and 91 units at 50 x 2^20 (the three
times the bound the physicist read); at the gap 80 it is 0.04 and 1.9
units. So Sagnac's two wells are two bodies at the seed 2^20 with their
faces 80 Links apart, or one composed body otherwise; the table's row
takes the gap 80 (the wells at [700, 732) and [812, 844)). THE READING
the physicist proposes (two equal wells at the gaps 2, 4, 8 and 16 on a
chain, the split read from the generator's clocks of the sum and the
difference and the beat from a record seeded on one well, a GameBoard
diagnostic with no pin) is CONFIRMED, with the numbers above as its
expectation: the two-level form within 0.3 percent at the gap 2 and
within 10^-4 from the gap 16 on.

**(8) THE MEASURED EXPERIMENTS, EACH COMPLETE FOR ITS INPUT FILE (the model owner's
words of 2026-09-25 through the Boss, records 1901 and 1902: "try to
reach a state where all 17 experiments run correctly"; "all the inputs
for the 17 experiments must be ready, everything algebraic and
translated to the board for running"; the earlier form of this table,
"the sixteen, each represented algebraically?", is folded into the last
two columns).** One row per experiment, in the form of (2), so that the
physicist writes its file through the generator without asking: the
board; the families; the entries (the bodies by vertex and side with
their pairs, the emitters with their coupling and stock, the momentum
**K** of every entry); the births (the born clock and profile, the
crystal's branches); the detectors as cubes of side 3 or more in the
ladder's declared order, the face last where the board has one (9.25
(10)); the neglected medium and its reason against the band (the
specification's the placed experiments); the board size and its reason; the blind pin
in clicks with its band; what is CARRIED or OPEN. Conventions (RESTATED 2026-09-25 on the physicist's finding at
f0d2d745, 9.17 (6a) and 9.25 (11)): light's vacuum pair is [1, 1]; a born clock [p, q] is the phase advance per Link k = pi p / (N q) on the world's circle of N = 1024 (the same statement as 9.17 (6a)'s 2 pi p / (2 N q); [512, 1] is k = pi / 2, the wavelength 4; the earlier "p / q of the circle per Link" doubled it, corrected at Nature24's reading); EVERY BIRTH IS THE BODY'S OWN MODE TIMES THE CHARACTER OF ONE **K** (9.35 (10), the model owner's record 1962; the earlier train under the Hann window and the tapers HISTORY), its length the body's extent along **K** (32 Nodes, 64 for Mach-Zehnder), at the born clock [512, 1] (k = pi / 2, the wavelength 4, cos
omega = 2 / 3) for every light emitter, so light's pace on every row is
v_g = 0.44721 Links per interval (the wavelength 20.78 of the earlier
rows, [2464, 25], is HISTORY: it fits no train on a body, and a body's
flat pulse is the broadband birth of 9.17 (6a)); every emitting body's
extent along **K** is the train's 32 Nodes; the holder family's vacuum
pair is [7, 8] and its emitting bodies are wells [801, 700] on a chain
and [699, 700] on a layer, of side 32 along **K** ((7a) (iii)); matter's
emitting bodies are [800, 801] on [800, 809] (the train at **K** = pi / 2
in the matter family, cos omega = 0.6593, v_g = 0.4384) or [314, 315] on
[156, 157]; every emitting body declares its coupling (g, G) to its born
family (9.19 item (4e)) and is TRANSPARENT to it ((7a) (iv)); every face is a
receiver slab as deep as the train, one train's length from every
emitter and receiver, and a fringe row's transverse axis carries slabs,
not a period (9.25 (11)); where the light returns to its source the
detector is the source's own Nodes; a pin on a passage is the MEAN click
interval over the stock with its band 3 rms / sqrt(n) (9.25 (11) (d)).
The rows' earlier placements and pins (the first draft's, at the
wavelength 20.78 or with a one-Node birth) are HISTORY where a row says
so.

| The experiment | The board | The entries and the births | The detectors, in the ladder's order | The neglected medium | The blind pin in clicks, with its band | CARRIED or OPEN |
| --- | --- | --- | --- | --- | --- | --- |
| Bell's four settings | the layer [96, 128, 1], periodic on both axes (no face: the record circulates until it is caught; RE-PLACED for the train, the 30 x 33 layer HISTORY) | light [1, 1], born clock [512, 1]; the holder [7, 8]. The emitter: a holder slab [699, 700] from (8, 60, 0) with the extents 32 x 8 x 1, its train along +x (the pump), the coupling to light, a stock of 100 per setting. The crystal (A.11): a holder body 3 x 32 x 1 from (56, 48, 0) with its light index and the branches [[1, 1], [2, 1]] (HV + VH), the born clocks p_1 + p_2 = p, the pair born as two trains on its Nodes, one with **K** = +y and one with **K** = -y (its long axis). Alice's polariser (A.5): a holder body of side 3 at (56, 100, 0) with the axis (1, 0) or (1, 1); Bob's at (56, 25, 0) with (1, 2) or (3, 1) | per arm its + cube then its - cube, 3 x 3 each beside its polariser (the placement per A.5); no face | air or fibre common to both arms: cancels | n = 100 pairs per setting: 40 / 10 / 10 / 40, 5 / 45 / 45 / 5, 45 / 5 / 5 / 45, 40 / 10 / 10 / 40 (standard deviations 4.9, 3.0, 3.0, 4.9 and 2.2, 5.0, 5.0, 2.2); S = 2.80 +- 0.14 (the pin [2.38, 3.22], the falsifier S <= 2); the controls: Bell's no-signalling control, Alice's counts identical bit for bit under Bob's two axes (9.25 (6)); Bell's product-state control, the product state HV (the branches [[1, 1]] alone) gives 80 / 20 / 0 / 0, 10 / 90 / 0 / 0, 40 / 10 / 40 / 10, 5 / 45 / 5 / 45 and S = 1.40 +- 0.52; the pins are the projections' shares and do not move with the placement | the crystal's pair birth as two trains (the crystal's build) |
| Malus's four axes | the chain [192, 1, 1] with the face slabs 32 deep at both ends (the bar of 11 HISTORY) | light [1, 1], born clock [512, 1]; the holder [7, 8]. The emitter: a holder well [801, 700] of side 32 at [40, 72), its train along +x (the hand H), the coupling, a stock of 256. The polariser (A.5): a holder body of side 3 at [104, 107) with the axis (1, 1), (5, 1), (15, 8) or (3, 2) | the + cube [112, 115), then the faces (the far slab from 160) | none between the tools | at 256 records on the + cube: 128 +- 24, 246 +- 9, 199 +- 20, 177 +- 22 (3 standard deviations; the expected 128.0, 246.2, 199.3, 177.2; the projections' shares) | none |
| The two slits | the layer [305, 320, 1], every face a receiver slab of depth 32, one train's length from the emitter and the screen (9.25 (11); the [241, 320] placement with the slab at the screen's back HISTORY: it halved the count) | light [1, 1], born clock [512, 1] (the wavelength 4); the holder [7, 8]. The emitter: a holder slab [699, 700] from (64, 128, 0) with the extents 32 x 64 x 1, **K** = 0, the coupling, a stock of 4096, its train along +x over 8 periods with the Hann window across y and the tapers of 8 (9.17 (6a)). The wall: a slab of the gap [1, 2] of depth 4 at x = 116 to 119 for y = 32 to 287 except the two openings of width 5 centred at y = 154 and y = 167 (d = 13), cut through its depth (a gap one deep transmits 0.2 at the wavelength 4, A.3). No polariser | the screen: 67 cubes of side 3 at x = 230 to 232, y = 60 to 260, in the order of y (the fringe spacing on the lattice 2 pi L / (d sin k) = 53.2 Nodes, 9.25 (10), not the continuum's 33.8); then the faces (the slabs x = 0 to 31, x = 273 to 304, y = 0 to 31, y = 288 to 319) | air: the index 2.7 x 10^-4 common to both paths, the Rayleigh loss below 10^-4 | COMPUTED by the generator's run of the placement: the screen's share 0.341 on the ladder, the visibility 0.945 at the lattice spacing 53.2 (read 52.5), the centroid 160.1, on the body's mode envelope (record 1962; the train under the window read 0.406 and 1662 +- 94, HISTORY, as the 1076 +- 84 of the slab at the screen's back); THE PIN at a stock of 4096: the screen 1396 +- 91, the visibility 0.95 +- 0.11 at 53.2, the spacing 53 +- 2, the centroid 160 +- 4; the control, the two slits with one opening closed: one opening closed (the opening at 167 filled by the wall's slab), no fringe, the component at 53.2 below 0.2 (computed 0.01, the best component 0.10) at 735 +- 74 screen clicks, the centroid 154 +- 4 (the 1052 +- 84 under the window HISTORY) | none |
| The pace fans | the layer [256, 256, 1] with the face slabs 32 deep (RE-PLACED at the wavelength 4; the 128 layer at [77, 25] HISTORY) | light [1, 1], born clock [512, 1]; the holder [7, 8]. ONE emitter: a holder slab [699, 700] from (64, 124, 0) with the extents 32 x 8 x 1, its train along +x with the Hann window of 8 across y (a narrow train diffracts into a fan of every direction at one omega), **K** = 0, the coupling, a stock of 1 | none: the fronts are read as a GAMEBOARD probe at 40 Links along the axis and along the diagonal from the emitter's head, a diagnostic and not a result (9.21 (4)) | none | at one omega = 0.8411 (k = pi / 2 on the axis) the diagonal's wave number is 1.4810 per Link (2 cos(k / sqrt 2) + 1 = 2) and its group velocity 0.5477 against the axis's 0.4472, the ratio sqrt(3 / 2) = 1.2247 (COMPUTED from the dispersion): the diagonal front at 40 Links 73 intervals, the axis's 89; the small-k forms (k^2 / 48 between the axis and the diagonal, k^2 / 36 against the continuum) are the same anisotropy at long wavelengths; no click pin | a diagnostic row |
| The muon's moving clock | the layer [200, 200, 1], periodic | matter [3200, 3236]. At rest: the well [3200, 3227] of side 14 at the vertex (93, 93), a clock body: a stock of 64 at the amplitude 2^20 on its composed mode, the coupling to light, its born trains circulating on the periodic layer (their return spreads its residues), **K** = 0. In motion: a packet of the matter family about 100 Links wide with **K** = 0.18556 per Link (v = 1 / 3), written moving at interval 0 (no ramp, record 1884) | the well's own Nodes (side 14) at rest; in motion a co-moving name of side 3 or more translating with the packet (A.14); no face | nature's muons slow in air over the hold: the one declared idealisation (the row reads the tick at one fixed **K**) | at rest the mode's period 42.33 intervals (omega_b = 0.14845) read from its own clicks, each click's interval t since the reseed and its residue u giving P = 2 W t / (2 u + 1) within the interval's grain (9.31 (13)), averaged over the stock; in motion the tick ratio 0.8146 of the rest (1 / gamma = 0.8165), band 0.3 percent | the push CARRIED, retiring; 8.4's well form HISTORY |
| The moving emitter's redshift | the chain [4096, 1, 1] with the face slabs 32 deep at both ends | light [1, 1], born clock [512, 1]; matter [156, 157]. At rest: the well [314, 315] of side 32 at [2944, 2976), the coupling (g, G) to light, a stock of 256, its train along +x written on its Nodes at each of its rungs (its cadence the internal clock, 9.17 (7)), **K** = 0. In motion: the emitter a packet of [156, 157] of side 32 with **K** = 0.13946 per Link (v = 1 / 3) receding from the receiver (moving -x), and a co-moving name with its stock | the receiver the cube [4000, 4003) (one train's length before the far slab), then the faces; the emitter's own Nodes for its births | none | 1 + z = (1 + v / c_l) / (the tick ratio) = (1 + 0.33333 / 0.44721) / 0.8154 = 2.141 at v = 1 / 3, band 0.3 percent, as the ratio of the receiver's click cadence to the emitter's birth cadence (the 1.935 at c_l = 0.57689 HISTORY); the control the rest world, the ratio 1 | the moving name ADOPTED (1889); the push CARRIED |
| The round trip off a receding mirror | the chain [1600, 1, 1] with the face slabs 32 deep at both ends (the 1000 chain with the name receding toward x = 0 HISTORY: it left the board) | light [1, 1], born clock [512, 1]; the holder [7, 8]. The mirror (A.3): the gap [1, 2] of depth 4 at [40, 44), at rest, at the low end. The emitter and its receiver ONE co-moving name: a holder well [801, 700] of side 32 on a holder packet with **K** for v = 1 / 3, from [300, 332) moving +x, receding from the mirror, its train along -x toward the mirror, the coupling, a stock of 32 | the receiver the name's own Nodes (the return enters them; 9.25 (11) (d)), then the faces | none | (1 + beta) / (1 - beta) = 6.856 at beta = v / c_l = 0.7454, band 0.3 percent, as the sent over the received click cadence at the moving name (the 3.7373 at c_l = 0.57689 HISTORY; the continuum's two-way Doppler is the same form at that beta) | the moving name ADOPTED; `cart_k3.json` REBUILT in this form |
| Sagnac's two-way light times | the chain [3000, 1, 1] with the face slabs 32 deep at both ends | light [1, 1], born clock [512, 1]; matter [800, 809]. At rest: two wells [800, 801] of side 32 at [700, 732) (A) and [812, 844) (B), their faces 80 Links apart so that each is a mode of the composed board within the rounding at the seed 2^20 ((7a) (v)), each with the coupling and a stock of 64, A's train along +x and B's along -x, **K** = 0; co-moving at v = 1 / 3: two packets of [800, 809] of side 32 with **K** = 0.18556 and two co-moving names with their stocks | at_a and at_b the wells' own Nodes (A's train enters B's Nodes and B's enters A's; 9.25 (11) (d)); the ladders A -> at_b, B -> at_a; then the faces | Fizeau's drag cancels on a closed loop | at rest the passage's mean click interval at the other well (80 + 16 + 2) / 0.44721 = 219 +- 6 at 64 records each way (the head's 80 Links from A's far face to B's near face; the rms 25), the same both ways; in motion the passages scaled by c_l / (c_l -+ v) = 3.927 with the motion and 0.573 against it (860 and 125), their ratio (c_l - v) / (c_l + v) = 0.146 +- 0.01 (the 108 +- 2 and 0.5774 at c_l = 0.57689 HISTORY) | the moving names ADOPTED; the push CARRIED; the hybrid share 3.2 x 10^-6 a load check |
| De Broglie's fringes | the two slits' layer [305, 320, 1] with the face slabs 32 deep on both axes (the y-periodic layer of 128 HISTORY: the pattern wraps at 2.41 spacings and its visibility falls to 0.43, 9.25 (11) (c)) | matter [800, 809]; the holder [7, 8]. The emitter: a holder body [699, 700] on the holder's [7, 8] from (64, 128, 0) with the extents 32 x 64 x 1, coupled to the matter family (g, G) (a body births a family other than its own, 9.17 (4); the earlier "matter slab" corrected at Nature24's reading), its train the character of the matter family at **K** = pi / 2 over 8 periods with the Hann window across y and the tapers of 8 (cos omega = 0.6593, v_g = 0.4384), the coupling, a stock of 2048. The barrier: holder bodies carrying the matter pair [1, 2] as a slab of depth 4 at x = 116 to 119 for y = 32 to 287 except two openings of width 5 centred at y = 154 and y = 167 (d = 13, as the two slits) | the screen: 67 cubes of side 3 at x = 230 to 232, y = 60 to 260, in the order of y (the fringe spacing on the lattice 2 pi L / (d sin K) = 53.2 Nodes); then the faces as the two slits | a vacuum chamber in nature: nothing | COMPUTED by the generator's run of the placement: the screen's share 0.337 on the ladder, the visibility 0.949 at 53.2 (read 52.5), the centroid 160.1, the lobes' centroids 159.9, 107.8 and 213.3, on the body's mode envelope (record 1962; the train under the window read 0.410 and 840 +- 67, HISTORY); THE PIN at a stock of 2048: the screen 690 +- 64, the visibility 0.95 +- 0.16 at 53.2, the centroid 160 +- 5, the lobes 160, 108 and 213 each +- 3 (the 515 +- 58 on the 128 layer HISTORY) | none |
| The moving mass's energy | the chain [224, 1, 1] with the face slabs 32 deep at both ends | matter [800, 809]; the holder [7, 8]. The emitter: a holder body [699, 700] on the holder's [7, 8] of side 32 at [64, 96), coupled to the matter family (g, G), with a stock of 400 (9.17 (4); the earlier "matter well" corrected at Nature24's reading); its births trains of the matter family at **K** = pi / 2 (v_g = 0.4384, omega = 0.8503), written on its Nodes, travelling +x | the receiver the cube [136, 139), then the faces (the far slab from 192) | none | the passage's mean click interval (41 + 16 + 2) / 0.4384 = 135 +- 5 at 400 records (the head's 41 Links from the well's far face to the cube; the 169 +- 2 HISTORY); the pace v_g(**K**) and the energy omega(**K**) closed forms beside (8.4, 9.24 (2)) | none |
| The boxed clocks, the box of side 20 and the box of side 28 | the cubes [64, 64, 64] and [48, 48, 48], periodic | matter [800, 809]; one well [800, 801] of side 20 or 28, a clock body with a stock of 64 at rest on its mode and the coupling to light, its born trains circulating on the periodic cube; the box of side 28 in motion a packet with **K** (v = 1 / 3) | the well's own Nodes; in motion a co-moving name | none | at rest omega_b from the clock body's own clicks, P = 2 W t / (2 u + 1) per click averaged over the stock (0.11929 and 0.09885, the periods 52.67 and 63.56 intervals); in motion the tick 0.8146 from the dispersion (the design's 0.7814 and 0.8032 HISTORY) | the push CARRIED |
| The deep well's clock | the layer [128, 128, 1], periodic | matter [800, 809]; the well [800, 801] of side 40 at (44, 44), a clock body with a stock of 64 at rest and the coupling to light; in motion (the control) a packet with **K** | the well's own Nodes; in motion a co-moving name | none | at rest omega_b = 0.07285 (the period 86.25 intervals) from the clock body's own clicks, P = 2 W t / (2 u + 1) per click over the stock; in motion the tick 0.8146 (the design's 0.7531 HISTORY) | as the boxed clocks |
| The light clock | the chain [760, 1, 1] with the face slabs 32 deep at both ends (the chain of 674 with at_a the cube beside A HISTORY: a cube beside the emitter books the outgoing pass, the physicist's finding at f0d2d745) | light [1, 1], born clock [512, 1]; matter [800, 809]; the holder [7, 8]. The well A [800, 801] of side 32 at [600, 632) with the coupling and a stock of 64, its train along +x, **K** = 0; the mirror (A.3): the gap [1, 2] of depth 4 at [690, 694) | at_a IS A'S OWN NODES (the set bound to the block, 9.25 (10) and (11) (d)): the outgoing train leaves them through the Port (negative, not booked) and the return enters them (0.998 of T booked, COMPUTED); then the faces | none | at rest THE MEAN click interval after the birth 300 +- 9 at 64 records (the passage's mean 299.7 = (2 x 58 + 16 + 2) / 0.44721, its rms 24.8, COMPUTED by the generator's run of the placement; the first click of the stock 250 +- 8); the 214 +- 1 HISTORY; in motion a closed form only, never a run (the longitudinal gamma squared WITHDRAWN as a prediction, record 1895) | the transparency of A to its return, (7a) (iv) |
| The receding index at one third of a Link per interval | the chain [4000, 1, 1] with the face slabs 32 deep | light [1, 1]; matter [156, 157]; the holder [7, 8]. The medium: a BOUND body [314, 315] of side 24 at 1500 with the coupling to light, at rest (material does not move); the emitter a holder well [801, 700] of side 32 and the receiver a holder body of side 32, ONE co-moving name on holder packets with **K** for v = 1 / 3 receding from the medium, the emitter's train through the medium toward the receiver | the receiver the name's own Nodes, then the faces | none | OPEN ON THE TRAIN'S WAVELENGTH: the index n = 1.2519 of the design was the bound medium's response BELOW its mode (omega_b = 0.092) at the light of omega' = 0.0181; at the train's omega = 0.841 (the wavelength 4, above every matter body's mode) the coupled index lies below 1 and its delay below the band of one interval (the resonance form n^2 - 1 = f / (omega_b^2 - omega^2)), and a train of 8 periods at the design's wavelength (200 Nodes a period) fits no body; the row is re-derived on a medium whose mode lies ABOVE the train's omega (the holder family's bodies, omega_b in 0.3 to 0.5, with a train at [2464, 25], the wavelength 20.78, 166 Nodes on a body of side 166; or a shorter train under the generator's check of 9.17 (6a)); the design's +1.0144 rad and 10.5 intervals HISTORY | the moving name ADOPTED; the push CARRIED; the medium's index at the train's omega OWED |
| The receding index at one quarter of a Link per interval | as the receding index at one third | as the receding index at one third with **K** for v = 1 / 4 (beta = v / c_l = 0.559 at c_l = 0.44721) | as the receding index at one third | none | as the receding index at one third, OPEN with it (the design's omega' = 0.02202 and n = 1.2577 HISTORY) | as the receding index at one third |
| The two-qubit computer | the layer [96, 128, 1], periodic, as Bell's four settings | as Bell's four settings: the emitter slab, the crystal with the branches of the prepared state (Grover: the uniform superposition [[0, 1], [1, 1], [2, 1], [3, 1]] with the circuit folded in by the generator; Deutsch-Jozsa: the state |+>|-> [[0, 1], [1, -1], [2, 1], [3, -1]] with the oracle folded in), two readout polarisers whose axes carry the last gates; the joint body OPTIONAL (record 1890) | per arm its + then its - cube, 3 x 3 | as Bell's four settings | Grover on four items: 0 / 0 / 0 / 100 at 100 records, the band 0 on the first three; Deutsch-Jozsa: 100 / 0 per oracle, the band 0; Bell as Bell's four settings | the joint body optional; complex joint weights OPEN, not needed |
| Mach-Zehnder | the layer [576, 576, 1], every face a receiver slab of depth 64 (the train's 16 periods), the emitter 32 Links from the x = 0 slab and the far slabs 100 Links behind the receivers (9.25 (11) (b); the 416 layer with the emitter at the slab HISTORY) | light [1, 1], born clock [512, 1]; the holder [7, 8]. The emitter: a holder slab [699, 700] from (96, 164, 0) with the extents 64 x 64 x 1, the coupling, a stock of 100, its train along +x over 16 periods with the Hann window across y and the tapers of 16; the splitters (A.4): light's pair [2, 3] on the line x = y from (158, 158) to (234, 234) and from (254, 254) to (330, 330); the mirrors (A.3): the gap [1, 2] of depth 4 on x - y = 96 to 99 for y = 158 to 234 and on x - y = -96 to -99 for x = 158 to 234 | the bright, from (412, 236, 0) with the extents 5 x 113 x 1; the dark, from (236, 412, 0) with the extents 81 x 5 x 1; then the faces | air or fibre common to both arms: cancels | at 100 records: the bright 97 +- 5 (share 0.973), the dark 0 or 1 (share 0.0079; two at the 20 percent level, three at the 5 percent level, four a defect), the faces 2 (0 to 6; share 0.019), COMPUTED by the generator's run of the placement on the body's mode envelope (record 1962; the window's shares 0.968 / 0.0054 / 0.027 HISTORY, the pins unchanged) (the placed experiments of LAB_TOOLS.md) | none |
| Mach-Zehnder with one arm blocked | as Mach-Zehnder | as Mach-Zehnder with a gap slab [1, 2] of depth 4 across the +y arm, its normal along y, at y = 244 to 247 for x = 158 to 234 (a receiver cannot block an arm: it books flux and leaves the amplitude; a mirror is the board's beam block) | as Mach-Zehnder | as Mach-Zehnder | at 100 records: the bright 25 +- 13 (share 0.248), the dark 22 +- 12 (0.219), the faces 53 +- 15 (0.534): the open arm's half splits at the second splitter and the blocked arm's half returns through the first splitter to the near slabs, COMPUTED as Mach-Zehnder's (the 47 / 39 / 14 of one-Node faces, which reflected the blocked arm back into the interferometer, HISTORY) | none |
| Sorkin's three openings (the model owner's record 1911 of 2026-09-25: its seven worlds on the two slits' placement, nothing new in the engine) | the two slits' layer [305, 320, 1], every face a receiver slab of depth 32 | light [1, 1], born clock [512, 1]; the holder [7, 8]. The emitter: a holder slab [699, 700] from (64, 96, 0) with the extents 32 x 128 x 1 (128 wide, centred on y = 160), **K** = 0, the coupling, a stock of 16384 per world, its train along +x over 8 periods with the Hann window across y. The wall: a slab of the gap [1, 2] of depth 4 at x = 116 to 119 for y = 32 to 287 with THREE openings of width 5 centred at y = 121, 160 and 199 (d = 39, 9.75 wavelengths), cut through its depth; SEVEN WORLDS by the openings left open, A, B, C, AB, AC, BC, ABC, the closed ones filled by the wall's slab | the screen: 67 cubes of side 3 at x = 230 to 232, y = 60 to 260, in the order of y; then the faces | air: the index 2.7 x 10^-4 common to every path | THE SORKIN SUM OF THE SCREEN'S CLICK TOTALS S = N_ABC - N_AB - N_AC - N_BC + N_A + N_B + N_C. COMPUTED by the generator's runs of the seven placements on the ladder's shares: A 0.0333, B 0.0957, C 0.0279, AB 0.1286, AC 0.0558, BC 0.1219, ABC 0.1527, on the body's mode envelope (record 1962; the window's shares HISTORY), the sum +0.0033 per record on the ladder's shares (+0.0041 on the flux), 0.02 of ABC's screen; ABC's visibility 0.59 at the spacing 17.7. THE PIN at 16384 records per world: S = 0 +- 284 (3 standard deviations of the seven binomial totals; the computed +55 inside it), and the seven screen counts A 545 +- 69, B 1568 +- 113, C 457 +- 63, AB 2107 +- 129, AC 914 +- 88, BC 1998 +- 126, ABC 2502 +- 138. THE CLICK'S OWN TERM (the rectification max(G, 0) of 9.19 (3), a positive grain term of the order (lambda / the fringe spacing)^2, 10^-6 in nature's regime; Sinha 2010: 0.006 +- 0.003 of the central count on a bound of 10^-2) reads +0.02 of ABC's screen on the mode envelope (the board's lambda over the spacing is 0.23 where nature's is 10^-3), inside the pin's band; the earlier +0.0049 per record was read on a flux that counted the slab's return (HISTORY) | none |

IN ONE LINE: every row is on the board with nothing outside (2) declared;
the pins that are counts or shares are closed forms with their bands
(Bell's four settings, Malus's four axes, the two-qubit computer,
Mach-Zehnder and its control, and Bell's two controls); the first rungs and
the fringe rows are the generator's runs of their placements, owed on
the flux form (the two slits, Sagnac's two-way light times, de Broglie's fringes, the moving mass's energy, the light clock, the receding index at one third and the receding index at one quarter), the two slits' and de Broglie's fringes' runs
today; the moving halves stand on the moving name (ADOPTED, record
1889) and the packet with **K** (record 1885), the push carried and
retiring; the pace fans are a diagnostic. WHAT THE PAPER LISTS BEYOND
THE MEASURED EXPERIMENTS (the Boss's audit, 2026-09-25): Bell's
product-state control, Bell's no-signalling control, the medium's index at
rest and the two slits with one opening closed enter as the controls inside
Bell's four settings, the receding index at one third and the two slits
above; Sorkin's three openings is prepared as an eighteenth in the placed experiments of LAB_TOOLS.md (its
first runs at d = 13 read a Sorkin sum of +0.11 of the three-opening
share, the openings coupling through the wall at 3.25 wavelengths apart:
re-placed at d = 39 with a three-source variant on the one wall to
isolate the click's own term: the seven walls +0.011 of the
three-opening screen flux, the three sources +0.022 at d = 39 and +0.005
at d = 13, the click's rectification a positive grain term of the order
(lambda / the fringe spacing)^2, 10^-6 in nature's regime; the pin
within +- 0.05 at 16384 records per world, the specification's Sorkin's three openings);
the atom's lines (at the coupled modes) waits on the owner; the moving
light clock stays out, the model having clocks and no rods
(record 1895); the bound on the interval's length, light's dispersion and the bound
clock's second term have no world.

THE PINS' FILE FORM (for the one command's `--pins`, 9.22 (7)): every
reading is of clicks. {detector, count, band} the count of clicks;
{detector, first_click, band} the interval of the detector's first
click; {detector, mean_interval, band} the mean over the detector's
clicks of the interval since the record's birth (the passage rows: 8,
10, 13); {detector, cadence, band} the mean spacing of successive clicks
at a detector, or of the births at an emitter (its own line); {ratio:
[reading_a, reading_b], value, band} of two readings of these forms (6,
7, 8); {sum: [{world, detector, weight}], value, band} (18; Bell's S from
the sixteen counts of Bell's four settings); {fringe: {detectors: [...], spacing,
centre, width}, visibility, band} twice the Fourier component at the
spacing over the ordered cubes under a Gaussian window of the width,
divided by the windowed total (3, 9); {centroid: {detectors: [...]},
value, band} (3, 9). Nothing else is compared.

**THE SIMPLEST FAITHFUL PLACEMENT OF EVERY MEASURED EXPERIMENT, ONE TABLE
(the model owner's rule of record 1944: "meet the experiment's conditions in
the simplest way; if it is with cubes, with cubes; if it means putting the
cubes in the middle of the big cube, we put them in the middle"; the Boss's
order of 06:21Z; PROVED and placed here).** THE EXTRUSION RULE (PROVED): a
chain [N, 1, 1] becomes [N, 3, 3] periodic on y and z and a layer [N, M, 1]
becomes [N, M, 3] periodic on z, every tool extruded across the added axes
and every seed uniform across them. On a state uniform across an added
axis the six-neighbour sum reads 2 a from that axis, exactly what the
extent-1 self-read gave; the operator commutes with the translation along
the axis; so the run is the extent-1 run copied identically on each slice,
bit for bit, remainders included. Every Port across an added axis carries
zero flux (its two ends are equal), and the tally and the norm scale
together by the number of slices, so EVERY PIN IS UNCHANGED TO THE BIT,
while every detector is a whole cube of side 3 and no cube is cut: the
owner's condition met at 9 times a chain's Nodes and 3 times a layer's. A
CUBE BOARD is needed exactly where a condition of the real experiment is
three-dimensional: (i) the isotropy under the 48 read as a fan of
directions (the body diagonals exist only in three dimensions): the pace
fans; (ii) a pin that counts clicks over a distance (the inverse-square
dilution of a spreading record): none of the eighteen, every pin being a
ratio, a count through a set, or a pattern along one transverse axis; (iii)
a bound body whose own three-dimensional mode is pinned: the boxes (already
cubes); the deep well's own clock is a model number, its pin the dilation
ratio, so the layer stands and a cube is the owner's choice. Polarisation
needs no third dimension: the polariser is an element of the wheel's group
on the label rows (9.14), not a transverse vector. The tools stand in the
middle of the board, one train's length from every slab's front (9.25
(11)), extruded across the added axes; the Nodes named are the host cost
per record per interval.

| The experiment | The simplest faithful board | Why | The host cost (Nodes) |
| --- | --- | --- | --- |
| Bell's four settings; the two-qubit computer | [96, 128, 3], periodic on all axes | the pins are counts through the polarisers' sets, no length; the 3 keeps every detector a whole cube | 36,864 |
| Malus's four axes | [192, 3, 3], the face slabs 32 deep on x | a count ratio along one axis | 1,728 |
| The two slits; de Broglie's fringes; Sorkin's three openings (seven worlds) | [305, 320, 3], every x and y face a receiver slab 32 deep, periodic on z | a real slit is uniform along its length: the pattern lives on one transverse axis; a cube of 305 x 320 x 305 would add 30 million Nodes and no condition | 292,800 (per world) |
| The pace fans | the cube [192, 192, 192], the face slabs 32 deep, the emitter cube at the centre, the 26 detector cubes at 48 Links on the axes, the face diagonals and the body diagonals | the one row that reads the isotropy under the 48; the body diagonals need three dimensions | 7,077,888 |
| The muon's moving clock | [200, 200, 3], periodic | the tick ratio depends on the dispersion along **K** alone; the layer keeps the light clock across the arm | 120,000 |
| The moving emitter's redshift | [4096, 3, 3], the face slabs 32 deep on x | a ratio of click intervals along one axis | 36,864 |
| The round trip off a receding mirror | [1600, 3, 3], the face slabs 32 deep on x | as the redshift | 14,400 |
| Sagnac's two-way light times | [3000, 3, 3], the face slabs 32 deep on x | two passages along one axis | 27,000 |
| The moving mass's energy | [224, 3, 3], the face slabs 32 deep on x | a first-click interval along one axis | 2,016 |
| The boxed clocks | the cubes [64, 64, 64] and [48, 48, 48], periodic, the box at the centre | already cubes; a box's mode is three-dimensional | 262,144; 110,592 |
| The deep well's clock | [128, 128, 3], periodic, the well at the centre; the cube [128, 128, 128] if the owner wants the atom's own clock three-dimensional | the pin is the dilation ratio, unchanged by the dimension; the well's own frequency is a model number | 49,152 (the cube 2,097,152) |
| The light clock | [760, 3, 3], the face slabs 32 deep on x, the detector the emitter's own Nodes | a passage and its return along one axis | 6,840 |
| The receding index, at one third and at one quarter | [4000, 3, 3], the face slabs 32 deep on x | a ratio of delays along one axis | 36,000 |
| Mach-Zehnder; with one arm blocked | [576, 576, 3], every x and y face a receiver slab 64 deep, periodic on z | the real interferometer is planar; a cube of 576 would cost 191 million Nodes and add no condition | 995,328 |

**(8a) THE COMPUTED EXPERIMENTS (the model owner's decision of 2026-09-25 through
the Boss, record 1915, Highlights 5.4: twenty-four experiments, the eighteen measured experiments of (8), run and read in clicks against
blind pins, and six computed experiments, whose result is the algebra's, stated in the paper with
how to compute it, the model's number beside nature's, agree or not,
labelled COMPUTATION and never a measurement; the atom algebraic only).**
The Boss's list of six computed experiments, confirmed on five and
replaced on one: gravity's
forms are NOT the algebra's (the coupling (g, G) acts at a body's Nodes,
9.19 item (4e), and nothing of it spreads outward: no field stands in the
vacuum around a body, so an inverse square or Poisson's equation would
need the pair-field hypothesis, which spreads a body's pair into its
neighbourhood, a hypothesis under its own identity and no computation of
the algebra); in its place the UNIVERSALITY OF THE TICK, which the
algebra computes and nature bounds. The in-motion halves on heavy boards
keep their closed forms inside their measured rows. Every number below
is a COMPUTATION on the law's forms (8.1, 9.24 (2), 9.19 (3), A.5,
A.11); the numbers of nature are cited with their source; a bound on
the one scale is a bound and not a measurement of it (the scale is the
owner's declaration and no formula, 8.9).

| The computation | Step by step | The model's number | Nature's number and its source | The verdict |
| --- | --- | --- | --- | --- |
| The atom's lines | (i) A well is a body whose pair raises 2 cos omega above the vacuum's band top 2 num / den; its bound modes are the eigenvectors of the composed operator above the top (9.22 (3)), one rotation each, omega_n = arccos(lambda_n / 2), all BELOW the rest frequency omega_0 = arccos(num / den). (ii) The emitter's excited record is seeded on the highest mode and rotates at omega_1, its internal clock (9.17 (7) (e)); its births come one per half period on average at the residue's phase. (iii) The born light's own clock is the world's declared born clock ((6a): [512, 1]); the law ties no frequency of the born light to the mode. (iv) Under the one identification the model could make, the born clock the mode's clock (the moving emitter's redshift's first design), the line sits at the mode's OWN frequency omega_1, and a second mode gives a second line at omega_2, never at the difference: the law is linear on one record and a record on one mode stays on it (no transition between modes is a term of the rule). COMPUTED on a chain of [800, 809], the well [800, 801] of side 32: omega_0 = 0.14930; the modes omega_1 = 0.06718, omega_2 = 0.10174, omega_3 = 0.13771 (the binding 0.08212, 0.04756, 0.01159 below the top); of side 12: one mode, 0.10022 | the lines at 0.06718 and 0.10174 per interval (the modes' own); the difference 0.03456 is no line; the ratio of a difference to an own frequency 0.514 | the lines are differences of two levels: hydrogen's Lyman-alpha 121.6 nm is (E_2 - E_1) / h = 2.47 x 10^15 Hz against the ground level's own E_1 / h = 3.29 x 10^15 Hz, the ratio 3 / 4 exactly (Bohr; Rydberg's constant) | DISAGREE, stated: the algebra's atom emits at its modes' own rotations, nature's at their differences; the paper says so, and how to compute the modes |
| Light's dispersion by direction and wavelength | (i) Light's band cos omega = (cos k_x + cos k_y + cos k_z) / 3 (4.2, 8.1). (ii) With **k** = k **n**, expand: cos omega = 1 - k^2 / 6 + k^4 sum n_i^4 / 72 + O(k^6); with omega^2 = 2 (1 - cos omega) + (1 - cos omega)^2 / 3 + O(6), omega^2 = (k^2 / 3) (1 - (k^2 / 36) (3 sum n_i^4 - 1)) + O(k^6), so omega = (k / sqrt 3) (1 - (k^2 / 72) (3 sum n_i^4 - 1)) and the group pace d omega / dk = (1 / sqrt 3) (1 - (k^2 / 24) (3 sum n_i^4 - 1)). (iii) 3 sum n_i^4 - 1 is 2 along an axis, 1 / 2 along a face diagonal and 0 along the body diagonal (1, 1, 1) / sqrt 3: the pace falls with the wave number (subluminal), most along an axis and not at all along the body diagonal (COMPUTED against the exact band at k = 0.2: the form and the band agree to 2 x 10^-7). (iv) In nature k a = E a / (hbar c) for the Link a, so the pace deficit is (E a / hbar c)^2 (3 sum n^4 - 1) / 24, a quadratic term in the energy | the deficit of the group pace (k a)^2 / 12 along an axis, 0 along the body diagonal; between the axis and the body diagonal at one wave number (k a)^2 / 12 | the quadratic energy dependence of the photon's pace from the gamma-ray burst GRB 090510: E_QG,2 > 1.3 x 10^11 GeV (Vasileiou et al. 2013), so a < sqrt 12 hbar c / E_QG,2 = 5.3 x 10^-27 m for a burst along an axis (the Planck length 1.6 x 10^-35 m admitted eight orders below); the direction dependence of c at one wavelength below 10^-18 (Nagel et al. 2015), a < 2.8 x 10^-16 m at 500 nm, weaker | AGREE as a bound: no number of nature is contradicted; the Link a lies below 5 x 10^-27 m |
| The bound on the interval's length, from the two paces | (i) A massive kind's band cos omega = (num / den) (sum cos K_i) / 3 has its bottom at omega_0 = arccos(num / den) (8.1). (ii) Its cone: omega^2 = omega_0^2 + c_eff^2 K^2 + O(K^4) with c_eff^2 = cos omega_0 (omega_0 / sin omega_0) c^2 (8.1 (ii), PROVED), c = 1 / sqrt 3 Links per interval light's pace; c_eff = c (1 - omega_0^2 / 6 + O(omega_0^4)); the joint second-order form gives c_m = c sqrt(cos omega_0) = c (1 - omega_0^2 / 4) (8.1 (i)). (iii) So a massive record's limiting pace lies below light's by the deficit omega_0^2 / 6 (the exact cone) to omega_0^2 / 4, with omega_0 = m c^2 tau / hbar the rest rotation per interval of length tau. (iv) A bound on (c - v_max) / c for a massive kind bounds omega_0 and so tau; and a = sqrt 3 c tau | for the declared pair [800, 809], omega_0 = 0.1493: the deficit 0.37 percent (c_eff) to 0.56 percent (c_m), COMPUTED; on a nature number: tau below 3.6 x 10^-28 s (the deficit omega_0^2 / 4 below 2 x 10^-14 for the electron), a below 1.9 x 10^-19 m; with the Link a below 5.3 x 10^-27 m of light's dispersion above, tau below 1.0 x 10^-35 s | the electron's pace against light's within 2 x 10^-14 (the published bound cited in SCHEDULE.md row A); the Planck time 5.4 x 10^-44 s | AGREE as a bound: one interval at most 3.6 x 10^-28 s from the electron and at most 1.0 x 10^-35 s from the burst, the Planck time admitted below both; a massive front faster than c_eff on a world beyond the band would falsify the model, and a tighter electron bound tightens tau |
| The bound clock's second term | (i) A moving bound record is a packet of its kind at **K** (9.24 (2)); its internal clock is the phase rate along its own centre, omega(**K**) - **K** . grad omega (the rotation seen where the packet is), and the tick ratio is that over omega_0. (ii) On the exact cone omega^2 = omega_0^2 + c_eff^2 K^2 this is omega_0^2 / omega = omega_0 / gamma_eff with gamma_eff = 1 / sqrt(1 - v^2 / c_eff^2): a bound clock dilates by Lorentz's gamma AT ITS OWN CONE c_eff, not at light's c (8.9, prediction 1's second face). (iii) The lattice's own term beyond the cone: the exact band against the cone, COMPUTED for [800, 809] at v = 1 / 3 along an axis (K = 0.18556): the tick ratio 0.81457 against 1 / gamma_eff = 0.81496, the ratio 1 - 0.41 K^4 (the same coefficient at K = 0.05, 0.1 and 0.2: a K^4 term, not K^2); for [156, 157] at v = 1 / 3 (K = 0.13946): 0.81541 against 0.81563, 1 - 0.72 K^4. (iv) Against light's gamma the clock is slower by about beta^2 gamma^2 omega_0^2 / 6 (0.19 percent at v = 1 / 3, omega_0 = 0.1493) | two terms beyond Lorentz's at light's c: the cone's, beta^2 gamma^2 omega_0^2 / 6, and the lattice's, 0.41 (K a)^4; in nature's regime for the electron with tau below 3.6 x 10^-28 s: omega_0 below 2.8 x 10^-7, the cone's term below 10^-14 at beta = 0.34, the lattice's term below 10^-40 | the time dilation of a bound clock (the Li+ ion's transition) at beta = 0.338 agrees with Lorentz's gamma to 2.3 x 10^-9 (Botermann et al. 2014); the muon's lifetime at gamma = 29.3 to 2 x 10^-3 (Bailey et al. 1977) | AGREE: both terms lie below nature's bands by five orders and more; the model's clock is Lorentz's at c_eff, and c_eff differs from c below the bands |
| Born's exponent and Tsirelson's limit | (i) The rule conserves one bilinear form of a record's two levels, I = sum_i D_i (now_i^2 + before_i^2) - (1 / 3) now_i (**A** before)_i (9.19 (3)), quadratic in the levels; a detector's share is its region's part of I acquired through its Ports (9.25 (2), (3)), so the click's probability is a quadratic form of the amplitudes: the exponent is 2 because the conserved form is of degree 2, and no other degree is conserved by the rule (an identity of the law, not a postulate). (ii) A crystal births a record of two branches (A.11); a polariser's body with the axis (a, b) passes the component along the axis (A.5), its + cube's share cos^2 of the angle between the record's hand and the axis, Malus's law as the same quadratic form; for the pair with the branches [[1, 1], [2, 1]] the correlation of the two + cubes is E(alpha, beta) = cos 2 (alpha - beta) (the two branches' quadratic form). (iii) S = E(a, b) - E(a, b') + E(a', b) + E(a', b') is a sum of four cosines of the four differences of two pairs of axes; its maximum over all axes is 2 sqrt 2 at the differences 45 degrees apart, Tsirelson's bound, an identity of the cosine form (the four vectors' Gram determinant); with integer axes the angles are rational tangents, and the settings (1, 0), (1, 1) for Alice and (1, 2), (3, 1) for Bob give the differences of the 3-4-5 triangle, E = 0.6, -0.8, 0.8, 0.6 | the exponent 2 exactly; S = 2.80 at the integer settings of Bell's four settings, 2.83 the bound approached by rational axes nearer 22.5 degrees | Born's exponent: the three-slit sum within 10^-2 of 0 (Sinha et al. 2010); Bell: S = 2.697 +- 0.015 (Aspect et al. 1982), 2.73 +- 0.02 (Weihs et al. 1998), 2.42 +- 0.20 loophole-free (Hensen et al. 2015); the bound 2 sqrt 2 = 2.828 never exceeded | AGREE: the exponent and the bound are identities of the one quadratic form; the measured S of Bell's four settings (2.80 +- 0.14) is the same form's number at the row's axes |
| The universality of the tick (in gravity's place) | (i) By the bound clock's second term above, every bound clock of a kind dilates by gamma at its own cone c_eff(omega_0), and the kinds differ in omega_0: two clocks of different constitution at one pace v differ in their tick ratios by about beta^2 gamma^2 (omega_0a^2 - omega_0b^2) / 6, plus the lattice's K^4 terms. (ii) The same clock along an axis and along the body diagonal at one pace differs by the band's anisotropy (light's dispersion above, 3 sum n^4 - 1). COMPUTED: [800, 809] and [156, 157] at v = 1 / 3, the tick ratios 0.81457 and 0.81541 (the difference 8.4 x 10^-4 on the board); [800, 809] at v = 1 / 3 along the axis and along the body diagonal, 0.81457 and 0.81496 (3.9 x 10^-4) | a constitution term (omega_0a^2 - omega_0b^2) beta^2 gamma^2 / 6 and a direction term of order (K a)^4; in nature's regime (tau below 3.6 x 10^-28 s) the constitution term between an electron clock and a muon clock at gamma = 29.3 is below 5 x 10^-7 and the direction term below 10^-40 | the muon's dilation agrees with the atomic clocks' Lorentz factor to 2 x 10^-3 (Bailey et al. 1977 against Botermann et al. 2014); the direction dependence of a clock's rate below 10^-18 (the anisotropy tests of Nagel et al. 2015 and the Hughes-Drever type bounds far below) | AGREE: nature's clocks are universal to the bands, and the model's non-universality lies below them by three orders (the constitution) and twenty (the direction); a clock-comparison in motion at 10^-7 between a lepton's decay and an atomic transition would reach the model's constitution term |

GRAVITY, for the record: the algebra has no gravitational field. A body's
coupling (g, G) acts at its own Nodes on the families it is coupled to
(the index of a medium, the back-action of an emitter, 9.19 item (4e)); the
vacuum around a body carries the vacuum's pair; light passing beside a
body is not bent and a second body is not drawn. Newton's inverse square
under a shell average and Poisson's equation are therefore not limits of
the algebra; a rule that spreads a body's pair into the vacuum with a
tail (the pair-field hypothesis) is a hypothesis under its own identity,
to be stated as such if the owner wants it, with its own expectations.

**(9) THE BOARD SIZE PER WELL (the Boss's item of 2026-09-25; COMPUTED by
Lanczos on the symmetrised operator of each well's own geometry; the
decay constant kappa along an axis from cosh kappa = 3 (denominator /
numerator) cos omega_b - 2 with the vacuum's pair, PROVED from 8.1 for a
tail at an imaginary wave number; the smallest torus the one whose
wrapped tail stays below half a unit at the amplitude A, N >= side + 2
ln(2 A) / kappa).**

| The well | omega_b, omega_0, the gap | kappa per Link, the decay length | The smallest torus at A = 4096 and 2^20 |
| --- | --- | --- | --- |
| the muon's moving clock: [3200, 3227] of side 14 on [3200, 3236], the layer 200^2 | 0.14845, 0.14930, 0.00085 | 0.0277, 36 Links | 665 and 1066 (the 200-layer holds it only with the wrapped tail: a weakly bound, wide mode) |
| the box of side 20: [800, 801] of side 20 on [800, 809], 64^3 | 0.11929, 0.14930, 0.0300 | 0.156, 6.4 | 136 and 207 (64^3 wraps the tail at 2^20; at 4096 within 0.03 units) |
| the box of side 28: side 28 on 48^3 | 0.09885, 0.14930, 0.0504 | 0.194, 5.1 | 121 and 178 |
| the deep well: side 40 on the layer 128^2 | 0.07285, 0.14930, 0.0765 | 0.226, 4.4 | 120 and 169 |
| Sagnac, the light clock: [800, 801] of side 12 on the chains | 0.10022, 0.14930, 0.0491 | 0.192, 5.2 | 106 and 163 |
| the redshift: [314, 315] of side 12 on [156, 157] | 0.10175, 0.11293, 0.0112 | 0.085, 11.8 | 224 and 355 |
| the receding index: [314, 315] of side 24 on [156, 157] | 0.09203, 0.11293, 0.0209 | 0.114, 8.8 | 183 and 280 |
| the emitter body of 9.19 item (4a): [801, 700] of side 3 on [7, 8] | 0.3753, 0.5054, 0.130 | 0.607, 1.6 | 33 and 51 |

THE SMALLEST CUBE OF [800, 801] ON [800, 809] THAT BINDS IN THREE
DIMENSIONS (COMPUTED, Lanczos at 100 steps on 40^3 and 56^3): a side of
16 is bound (4.99 x 10^-3 above the band's top on 40^3), a side of 12 is
marginal (1.6 x 10^-3 on 40^3, 1.0 x 10^-3 on 56^3, still falling with
the board), and sides 2 to 10 are not bound in the large-board limit
(their excess over the top falls toward 0 as the torus grows); the
estimate from the band's curvature and the well's depth, side^2 >= 3 pi^2
/ (8 m V) with m = 3 denominator / (2 numerator) and V = 2 (800 / 801 -
800 / 809) = 0.0198, gives a side of about 11. So the property test's
well of side 2 on 12^3 (9.20 (B)) binds only by its small torus, which is
enough for the test (any mode of the composed operator is a valid seed),
and a moving-clock well on a cube is of side 16 or more, or a packet
(9.24).


### 9.23 A two-qubit quantum computer on the board (the model owner's word of 2026-09-24, 22:46Z (2026-09-25 on the Israel clock), through the Boss: "in our world the Outside sees only the click; lab equipment simulates on the board what we built from the algebra; check whether a quantum computer of two qubits can be simulated this way"), marked, before any code

**(1) THE QUBIT (DERIVED HERE from 3.6, 9.16 (2) and 9.19 (1)).** A qubit
is the label module Z^2 of ONE ARM of a record, carried by that arm's two
label rows (9.16 (2)): the two rows' amplitudes are the qubit's two
weights and their relative phase is the qubit's phase (the rows share the
clock; the phase is read between the two rows at the same Node). Its
normalisation is never written: the rung divides by the record's own norm
T, so the weights are integers up to a common scale. TWO QUBITS are one
record of rank 2, the tensor Z^2 (x) Z^2 of the two arms' label modules
(3.6), born together by the crystal (9.13) with its branches as the
tensor's INTEGER coefficients and the per-arm phases on the rows. Two
separately born records are two summands of the direct sum (9.19 (1));
nothing in the six verbs joins two summands into one tensor (that would be
an operation bilinear in two summands acting on a third, a cubic term the
three tests exclude, 2.8), so THEY ARE NEVER ENTANGLED: a two-qubit
register is one record of rank 2, DERIVED. What the tensor carries: real
integer coefficients on the four joint labels plus one phase per arm, so
every reachable two-qubit state has a phase matrix theta_ij = alpha_i +
beta_j (no "phase interaction", theta_00 + theta_11 - theta_01 - theta_10
= 0). Bell's states and every REAL circuit (Deutsch-Jozsa, Grover) lie in
it; a state such as (|00> + |01> + i|10> + |11>) / 2 does not: OPEN (a
second, quarter-turned row per joint label, the ring Z[i] on the tensor,
would carry it; not needed below).

**(2) THE ONE-QUBIT GATES AS TOOLS (DERIVED HERE).** Three bodies, each a
region of the operator with integers, each already in the tool table:
- THE ROTATOR R_(a, b): a body with an axis (a, b) and NO receivers, the
  label matrix **M**_u = [[a, b], [-b, a]] on the arm's rows (9.16 (2)):
  the rotation by the angle with tangent b / a, integer, the scale a^2 +
  b^2 absorbed by the rung. The rational axes are dense in the circle
  (PROVED: tan of a dense set of angles is rational).
- THE MIRROR: a mirror body (the gap [1, 2]) acts on the arm's label rows
  as the reflection of the label plane its own plane induces (9.14 (b)'s
  D_4): Z = diag(1, -1) for a mirror plane containing the H axis, X =
  [[0, 1], [1, 0]] for one containing the diagonal (CORRECTED on
  2026-09-25: the first draft wrote X for every mirror; in the hands
  basis every reflection is the exchange, in the label rows it is Z or X
  by the orientation).
- THE RETARDER Z_s: the relative phase of the two hands, the wheel's
  translation x^s on one row (9.14 (a)): a chiral body with a pair PER
  LABEL (one label's rows paced differently from the other's over its L
  Nodes, the crystal's own index-per-label form, the lab tools'
  specification 1.9 test 1). It is EXACT when L times the two paces'
  difference is a whole number of the clock's steps (a Diophantine
  condition the generator solves for the world's clock); otherwise it is
  the phase to the clock's grain, COMPUTED per world. Z = Z_(N/2), S =
  Z_(N/4), T = Z_(N/8) on the wheel of N.
THE HADAMARD: **H** = [[1, 1], [1, -1]] = **M**_(1, 1) X = **M**_(1, -1) Z
(the matrix products, up to the overall sign), its 1 / sqrt 2 absorbed by
the rung: EXACT in integers (DERIVED); and X = **M**_(0, 1) Z up to the
sign, so one mirror of either orientation with the quarter turn gives the
other. THE GATE SET {R_(a, b), X, Z_s}: for a fixed wheel N
it generates a FINITE group up to the rung's scale; as N grows and the
axes range over the rationals it is DENSE in the one-qubit gates
(rotations of every rational tangent times phases in steps of 2 pi / N):
DERIVED. The norm scale grows by a^2 + b^2 per rotator (by 2 per H); a
circuit of depth d multiplies it by up to 2^d against the host's integer
bound, a load check.

**(3) THE TWO-QUBIT GATE (DERIVED HERE; NEW for the engine).** A
controlled gate acts on the joint label module Z^2 (x) Z^2: CNOT is a
permutation of the four joint labels (|a b> -> |a, b + a mod 2>), verb (P)
of 2.4 on the joint state; CZ is the diagonal matrix (1, 1, 1, -1) on the
joint weights, verb (B) with a declared matrix. Both are operations of
the algebra as written. THE JOINT BODY IS THE CRYSTAL'S FORM WITH A
MATRIX (DERIVED HERE, replacing the first draft's per-Node action and
its equal-time condition, both withdrawn on 2026-09-25): the four joint
weights are the record's own data, not a value at a Node, so no per-Node
verb reaches them; the one act of the law on a record's own data is the
click, and the one act that writes a record is the birth (9.17). So the
joint body is a region named on the pair's ladder for BOTH arms: the pair
clicks there at its rung (**E**, **D**, **X**, the pair's offer being its
rows' flux into the body's Nodes) and the body BIRTHS a pair on its Nodes
with the weights c' = **G** c, **G** its declared 4 x 4 integer matrix
(the bilinear form) or permutation (the permutation) on Z^2 (x) Z^2, the residue the law's
remainder at its centre Node (9.19 (4)), the born rows written once at
both levels (9.17 (6)): exactly the crystal (9.7 (b), 9.13) with a
matrix on the arriving weights in place of fixed branches. Nothing waits
for the two arms to arrive together: the ladder sums both arms' offers
and the rung fires once. The born pair spreads from the body's Nodes as
the crystal's does, and the readouts are placed where it goes (9.6). In
nature it is a nonlinear medium; here it is a declared matrix, a material
like the crystal's branches. Within the three tests: generic (the
crystal's primitives with declared integers, no family name), vector
(**G** on the weights, no root), local (the body's Nodes). NOT ON MAIN:
the engine's crystal births fixed branches, never a matrix applied to
the arriving pair's weights. WHAT THE CRYSTAL'S
BIRTH REPLACES: any entangling gate that comes first in a circuit is a
prepared state, the crystal's declared branches (the four Bell states,
the uniform superposition, any real tensor with integer weights); an
entangling gate in the MIDDLE of a circuit needs the joint body.

**(4) THE READOUT (DERIVED, 9.19 (3) and (4)).** Clicks only: each arm
ends at a polariser body with the axis (1, 0) (the computational basis)
and its two receivers; the pair clicks once, on the joint Nodes, with the
weights R = J^2 of the joint state (3.6); the residue is the law's (the
arriving record's remainder at the crystal's centre, 9.19 (4)); the
counts are distributions, binomial about the joint weights' shares, and
a share of 0 has the band 0 (one click there is a defect).

**(5) ONE CONCRETE CIRCUIT, as placed tools (DERIVED HERE, blind).**
- THE BELL STATE AND ITS FOUR MEASUREMENTS: the Bell row of the
  specification's the placed experiments as it stands (the crystal's branches [[1, 1],
  [2, 1]], Alice's rotators are her polarisers' axes (1, 0) and (1, 1),
  Bob's (1, 2) and (3, 1)); 100 pair records per setting: 40 / 10 / 10 /
  40, 5 / 45 / 45 / 5, 45 / 5 / 5 / 45, 40 / 10 / 10 / 40 with the bands of
  9.19 item (4b), S = 2.80 +- 0.14.
- GROVER'S SEARCH ON FOUR ITEMS, the marked item |11>: (i) the crystal
  births the uniform superposition, the branches [[0, 1], [1, 1], [2, 1],
  [3, 1]] (H (x) H on |00> as a prepared state); (ii) the oracle: a joint
  body with the diagonal (1, 1, 1, -1); (iii) the diffusion: on each arm
  X then R_(1, 1) (the Hadamard), then a joint body with the diagonal
  (1, -1, -1, -1) (2 |00><00| - I up to the overall sign), then X and
  R_(1, 1) on each arm again; (iv) the readout with the axis (1, 0) on
  both arms. THE ALGEBRA'S COUNT (PROVED, the standard one-iteration
  Grover on 4 items; here on the integer weights: (1, 1, 1, 1) -> the
  oracle (1, 1, 1, -1) -> H (x) H (2, 2, 2, -2) -> the joint (1, -1, -1,
  -1) gives (2, -2, -2, 2) -> H (x) H (0, 0, 0, 8), the rung's scale
  absorbing the 8): every record clicks at (-, -), the labels (1, 1); with n = 100
  records the expected counts are 0, 0, 0, 100 with the band 0 on the
  first three: a single click elsewhere is an engine defect. The joint
  bodies need both arms at one region: the two arms are folded by two
  mirrors onto one Node line at equal times (the mirror theorem, a
  placement of the specification's 11.3 with the polarisers replaced by
  the mirrors), then separated again to the two readout polarisers.
- DEUTSCH-JOZSA ON TWO QUBITS (the query qubit and the ancilla): the
  crystal births |+>|->, the branches [[0, 1], [1, -1], [2, 1], [3, -1]]
  (negative integer weights allowed); the oracle of a constant function is
  the identity (no body) or the joint (-1, -1, -1, -1) (a sign), of a
  balanced one the joint (1, 1, -1, -1) or (-1, -1, 1, 1) (the phase
  kick-back of f(x) = x or 1 - x on the ancilla |->); then X and
  R_(1, 1) on the query arm and its readout with the axis (1, 0): the
  query arm clicks + for a constant function and - for a balanced one,
  every record; n = 100: 100 / 0 with the band 0.
- THE RECORDS EACH NEEDS: Bell 400 (the distributions); Grover 100 and
  Deutsch-Jozsa 100 per oracle (deterministic outcomes, the band 0).
- AS PLACED ON A LAYER (DERIVED HERE; the sixteenth row of the
  specification's the placed experiments): a gate that stands between a birth and a
  readout with nothing between is composed into them exactly, since the
  algebra composes matrices (a one-qubit gate before the joint body into
  the crystal's branches, one after it into the readout polariser's
  axis); on a layer the rows spread from a birth in every direction and
  a separate gate body would catch a part of an arm only, so the placed
  form is: the crystal births the state the circuit has reached at its
  first entangling gate; ONE joint body carries that gate; the readout
  polarisers' axes carry the last one-qubit gates. Grover: the crystal
  births (1, 1, 1, -1) (the uniform state after the oracle, the branches
  [[0, 1], [1, 1], [2, 1], [3, -1]]); the joint body **G** = diag(1, -1,
  -1, -1) gives (1, -1, -1, 1) = (1, -1) (x) (1, -1); both readout
  polarisers with the axis (1, 1) (the Hadamard then the axis (1, 0)):
  every record clicks (-, -), 0 / 0 / 0 / 100. Deutsch-Jozsa: the crystal
  births |+> |-> = (1, 1, -1, -1) (the query arm 0, the label index a +
  2 b); the joint body is the identity or -I (constant) or diag(1, -1, 1,
  -1) or its negative (balanced); the query arm's polariser with the axis
  (1, 1) clicks + for constant and - for balanced, 100 of 100; the
  ancilla's polariser with the axis (1, 0) clicks - always (a check).
  The gate bodies themselves (the rotator, the mirror, the retarder) are
  tested on a bar with single records (the specification's A.5 and
  A.13), not in the sixteenth's layer.

**(6) THE VERDICT.**
- THE BOARD CARRIES NOW (once 12.2's per-label rows and the crystal are
  built): one qubit per arm; the rotator, the mirror and the retarder as
  one-qubit gates (the retarder exact under its Diophantine condition);
  the Bell states and any real prepared two-qubit state from the crystal;
  the readout by clicks with distributions. All DERIVED, within the three
  tests.
- IT WOULD NEED: the JOINT BODY (a declared integer matrix or permutation
  on Z^2 (x) Z^2 at a region both arms cross), the one new engine form;
  the routing of both arms to it by mirrors at equal times; and, for
  states with a phase interaction, complex joint weights (OPEN, not
  needed for Bell, Grover or Deutsch-Jozsa).
- WITHIN THE THREE TESTS: yes for every piece above (verbs B and P with
  declared integers, no root, local at the body's Nodes).
- PLAINLY: the board simulates a two-qubit computer as a classical
  machine would, with the tensor's 2^n integer weights for n qubits; the
  cost is exponential in the qubits, as for any board simulation of a
  quantum computer, and the Outside sees only the clicks.

**(7) THE MODEL OWNER'S READING (2026-09-25 on the Israel clock, to the
mathematician, translated: "the computation is in the generator, not on
the board; the board cannot compute like that, it is local; reaching the
quantum state required the computation; the quantum state computes
nothing, the entanglement is already on the board; creating that
entanglement is the cost; the generator, if it works right, computes it
in iterations"): CONFIRMED, and it sharpens (6).** THE BOARD COMPUTES
NOTHING: the law spreads the rows locally (the split) and the click reads
(9.19); no verb of the law reaches a record's joint weights but the click
and the birth. So the whole unitary part of a circuit is a computation
OUTSIDE the law: the board generator iterates the circuit's gates on the
weights (each gate one product of a 2^n x 2^n integer matrix with the
weight vector, 2^n = 4 here) and writes the result as the crystal's
branches, with the readout axes carrying the last one-qubit gates; THAT
IS THE COST, exponential in the qubits, and it sits in the generator,
not on the board. The joint body of (3) is the crystal's own act (a birth
with a matrix on the weights) placed in the middle of the run: it
computes nothing the generator could not have folded into the branches,
so it is OPTIONAL, wanted only to test a gate as a body of the engine.
WHAT THE BOARD ADDS, which no generator can: the ENTANGLEMENT AS A THING
ON THE BOARD, one record of rank 2 carried by the local law to two
separated readouts, and THE CLICKS: Born's rule by the residue and the
rung (9.19 (4)), the two arms' clicks with no signal between them (the
pair's one gather), and the distributions of the counts. So the
sixteenth tests the measurement law on a prepared entangled state, as
Bell does with its own branches; the unitary circuit is the generator's
iteration, and the board's cost stays linear (the transport and the
clicks, 9.21 (8)). The verdict of (6) reads so: "the board simulates a
two-qubit computer" means the generator computes the state and the board
carries and measures it.

### 9.24 The moving body under the one operator (the model owner's question of 2026-09-25 on the Israel clock, through the Boss: "how is a moving body represented algebraically? that is the question"; his lead: "it is a large bound body with momentum"; his decisions of records 1884 and 1885: no acceleration, and the momentum an integer of every entry), marked, before any code

**(1) THE THEOREM THAT DECIDES THE FORM (PROVED HERE).** The one
operator is LINEAR in the state (8.1's rule, 8.5's coupling, 9.16 (2)'s
label matrix, each a linear map of the element; the pairs, couplings and
axes are data) and, away from the regions of material, it commutes with
every translation (1.6). A linear translation-invariant map has the
characters as its modes and nothing else that is stationary: a localised
stationary state needs a region of material that breaks the translations
(a well, 8.3). So there is NO SELF-BOUND LOCALISED BODY in the one algebra:
a body's own quanta do not bind each other (that would be a term of degree
two or more in one family's amplitude, which the three tests exclude,
2.8), and a family's "binding" is only its rest frequency, the pair's
omega_0 (8.1), which is the same at every Node. What a moving body can be
is therefore one of two things, and no third: A PACKET of a family
carried by the character of its momentum (item 2), or A REGION OF
MATERIAL, which does not move (item 3). The owner's lead is read against
this: "a large bound body with momentum" is a LARGE PACKET of the massive
family, bound in the sense of its mass (its rest frequency, its internal
clock), not by a potential, large so that it barely spreads.

**(2) THE FREE MOVING QUANTUM, AND THE LARGE PACKET (PROVED and
COMPUTED).**
- EXACT SOLUTION (PROVED, 1.6 and 8.1): on a homogeneous board every
  character exp(i(**k** . **x** - omega(**k**) t)) is a mode of the rule
  with 3 cos omega = (numerator / denominator) SUM of cos k_i, and a
  packet SUM over **k** of c_**k** times the character is an exact
  solution, each mode advanced by its own clock; the written initial
  state (the profile times the character of **K** at the two levels,
  integers after rounding) is such a packet to the remainder's grain, and
  it moves from interval 0 with no ramp: the model owner's record 1884 is
  the algebra's own statement (DERIVED).
- THE PACE AND THE ENERGY (PROVED): the group velocity per axis v_i =
  (numerator / denominator) sin k_i / (3 sin omega), the energy the clock
  omega(**K**) at one quantum of content. At small **K** and omega, omega^2
  = omega_0^2 + k^2 / 3 with omega_0^2 = 2 (1 - numerator / denominator):
  the relativistic band with c = 1 / sqrt 3 and the mass omega_0 (PROVED
  by expanding 8.1). The effective mass 1 / omega'' at rest is 3 sin
  omega_0 (denominator / numerator): 0.4513 for [800, 809] and [3200,
  3236], 0.3402 for [156, 157], 0.2396 for [314, 315] (COMPUTED).
- THE INTERNAL CLOCK OF A MOVING PACKET (PROVED from the dispersion): at
  the packet's centre, which moves at v = v_g(**K**), the phase advances by
  omega(**K**) - **K** . **v** per interval, so the packet's own tick is
  slower than the rest tick by (omega(**K**) - **K** . **v**) / omega_0.
  TIME DILATION ARISES FROM THE DISPERSION, from no rule, as the owner's
  lead says: for the relativistic band that ratio is exactly 1 / gamma.
  COMPUTED on the lattice band along an axis, for [800, 809] and [3200,
  3236]: at v = 0.1 the tick ratio 0.98477 against 1 / gamma = 0.98489;
  at v = 0.2 (**K** = 0.09637) 0.93757 against 0.93808; at v = 1 / 3, the
  fifteen's k = 3 (**K** = 0.18556 per Link), 0.81457 against 0.81650;
  for [156, 157] at v = 1 / 3 (**K** = 0.13946) 0.81540; for [314, 315]
  (**K** = 0.09802) 0.81595. THE LATTICE'S ANISOTROPY: along the diagonal
  at the same speed the ratio differs from the axis's by less than 0.1
  percent up to v = 0.35 and by 0.2 percent at v = 0.43 (COMPUTED, 9.24's
  script beside this chapter's prototypes).
- THE SPREADING (PROVED and COMPUTED): a packet of width sigma spreads on
  the time t_s = 2 sigma^2 / omega'' (the dispersion's curvature); for
  [800, 809] t_s = 130 intervals at sigma = 12, 1444 at 40 and 9025 at
  100 Links; for [314, 315] 69, 767 and 4792. So a moving CLOCK of the
  fifteen's length (a hold of 8000 intervals) is a packet about 100 Links
  wide, and a well of side 12 or 14 set free is not a clock: it spreads
  in a hundred intervals. The muon's form, the boxes and the deep well
  in motion are LARGE PACKETS, of the width their hold demands; on the
  200 x 200 layer and the 64^3 cubes that width fits.
- THE CONTRACTION: none on the board's own surface; the profile is as
  written (8.4's "the characters themselves" is history, and its 0.1
  percent carried value is replaced by the dispersion's exact one).
- WHAT THIS SERVES AS IS: the moving mass (the moving mass's energy) is a free packet born by
  its emitter body and read by a static receiver: DERIVED, nothing
  changes. The packet as a CLOCK read by clicks needs item 4.

**(3) THE REGION OF MATERIAL DOES NOT MOVE (PROVED), and the four forms
weighed.**
- (a) THE WELL'S MATERIAL CARRIED BY A RECORD OF THE HOLDER FAMILY:
  REFUSED by the three tests (PROVED). A pair at a Node is data; for it to
  follow a record, the pair for F at a Node would have to be a function
  of the holder record's amplitude there, a term of degree two in the
  holder's amplitude times F's amplitude (a cubic term, not bilinear), or
  a threshold on the holder's amplitude (a read of a Node to decide, 9.7).
  The bilinear coupling of 8.5 (F's row gains g times the holder's
  difference) is linear in the holder and binds nothing.
- (b) THE PUSH (8.11, 9.21 (7a)): moves the regions from outside the
  operator by a declared rule; not in the one algebra; CARRIED on main
  and RETIRING with the moving wells (item 5).
- (c) THE REST MODE TIMES THE CHARACTER (8.4), dragged by the hops:
  COMPUTED here on the chain of 1500, the well [800, 801] of side 12 on
  [800, 809], the seed the rest mode times the character at **K** =
  0.18556 (v = 1 / 3), the well hopping one Link every 3 intervals from
  interval 0 with no ramp: the share of the form I within 10 Links of the
  well falls to 0.869 at 300 intervals, 0.798 at 600 and 0.740 at 900
  (the rest mode alone dragged: 0.603, 0.580, 0.606; at v = 0.1: 0.939,
  0.889, 0.848; at rest: 0.996 constant). So the boosted rest mode is NOT
  a mode of the hopping well: it sheds about 4 x 10^-4 of its norm per
  interval at k = 3 into the vacuum's characters, which is the "relaxation
  the ramp absorbs" of 8.4; the ramp only lets the record shed it before
  the reading. CARRIED where the push stays; history where it goes.
- (d) THE FRAME FORM: run the experiment with the material at rest and
  read the Outside's clicks in the moving frame by the click theorem's
  symmetry (Highlights 5.4; the dispersion's Lorentz form to the order of
  item 2). ITS SCOPE (DERIVED): it removes the motion of ONE thing; an
  experiment whose two sides both need material (a moving mirror and a
  resting emitter, the transponder; the moving light clock, whose mirror
  and receiver move together) cannot be run in any frame with the
  material at rest on both sides; those are CLOSED FORMS (item 6), the
  runs at rest confirming their ingredients by clicks.

**(4) THE MOVING NAME (DERIVED HERE as lawful; ADOPTED by the model
owner, record 1889, 2026-09-25 on the Israel clock: "yes, approve the
moving name"; the specification's card A.14).** The Boss's question: can a receiver or an emitter be named by
the record rather than by fixed Nodes? A receiver is a name (9.19 (5)),
no material: a set of Nodes that the click reads (the flux into it) and
the birth writes on. A NAME MAY TRANSLATE: the set S(t) = S(0) + (the
accumulator's steps), the accumulator advanced by the rate of **K**'s
group velocity in integers (one Link per [intervals] with the remainder
kept, the translation), the same stepping the push uses, applied to a NAME and
not to material. Then: the operator is unchanged (no material moves), so
equivariance, locality, conservation and reversibility hold as proved
(9.20 (A)); the click reads the flux into S(t) and the birth writes on
S(t), the crystal's and the emitter's forms unchanged; a packet with a
co-moving name is the moving clock (its own record clicks at its rung on
S(t) as the well's does at its block, the norm one period's one-way flux
into the moving centre Node, 9.17 (5)), the moving emitter (a stock
births at S(t) at the packet's own tick rate, which item 2 dilates), and
the moving receiver. The three tests: generic (the name's rate is derived
from **K** by the generator, an integer pair per axis, not a declared
heading; the translation), vector (no root), local (the set's Nodes). WHAT IT IS
NOT: a mirror, a well, a medium (material), which stay at rest. ADOPTED
(record 1889): a name may move; its rate is **K**'s own, computed by the
generator, and no rate or heading is declared beyond the body's **K**.

**(5) WHAT EACH MOVING ROW DECLARES NOW (DERIVED, on items 2 to 4), and
the ramp.** THE RAMP IS NOT NEEDED (DECIDED, record 1884; DERIVED, item 2:
a packet is born moving, the character times the profile is an exact
solution); DECLARATIONS.md section 8 retires; no `ramp` key; a world
with one is refused (9.22 (2)). 8.4 moves from CARRIED to DERIVED for a
free packet (the dispersion's exact clock) and to HISTORY for a moving
well. The rows:
- THE MOVING MASS (the moving mass's energy): as is; a packet from the emitter body, the first
  rung at the static receiver.
- THE MUON'S FORM (4a), THE BOX OF SIDE 28, THE DEEP WELL IN MOTION: at
  rest the well and its clicks as today; in motion a LARGE PACKET of the
  matter family with **K** written at interval 0 (no well, no push), its
  tick the closed form of item 2 (0.8146 of the rest tick at v = 1 / 3,
  against the design's well form 0.8116, CARRIED); read by clicks only
  with a moving name (item 4), else a closed form beside the rest run.
- THE REDSHIFT (4b): the emitter a packet with **K** and a moving name
  with its stock; its births come at the packet's own tick (dilated by
  item 2) from positions that recede, so the receiver's click intervals
  are stretched by 1 + v / c_l: 1 + z = (1 + v / c_l) / (the tick ratio)
  = 1.935 at v = 1 / 3 with c_l = 0.57689 (the chain's light at k = 2 pi
  / 64) and the tick ratio 0.8154 of [156, 157] (COMPUTED; the
  relativistic (1 + beta) gamma gives 1.9332; the design's 1.9889 on the
  pushed well with the coupling's emission is CARRIED and differs: the
  emission mechanism of a packet, its stock at a moving name, is the
  open point of item 4).
- THE ROUND TRIP (4c): the mirror at rest (material), the emitter and
  receiver one moving name on a holder packet: (1 + beta) / (1 - beta) =
  3.7373 at beta = v / c_l = 0.5778 (the design's 3.7733 on the band at
  [2464, 25], CARRIED; the continuum 3.732).
- SAGNAC (Sagnac's two-way light times) co-moving: two packets with **K**, two moving names with
  stocks; the first rungs D / (c_l - v) and D / (c_l + v) plus the
  emission's dilation, COMPUTATION owed on the flux form.
- THE RECEDING INDEX (k = 3, 4): the medium at rest (material, bound, of
  the holder family), the light emitter and the probe moving names; the
  probe stays a GAMEBOARD reading; the pin re-derived blind on the bound
  medium (owed).
Every one of these runs with the moving name (ADOPTED, record 1889),
after the physicist's cleanup; until built, its moving form on main is
the push's, CARRIED and named so.

**(6) THE MOMENTUM AS A TOOL'S INTEGER, AND THE LIGHT CLOCK IN CLOSED
FORM (the model owner's record 1885).** Every entry of an experiment's
list carries **K**, the integer wave vector of its character, 0 at rest
(9.22 (2); the tool cards of LAB_TOOLS.md, each card). THE LIGHT CLOCK
(DERIVED HERE from the dispersion; the chain of 674, the receiver at 612,
the mirror at [672, 674), D = 60 Links, the light of the chains at k = 2
pi / 64, v_g = c_l = 0.57689):
- AT REST: the tick is 2 D / c_l + the mirror's delay = 208.01 + 3.973 =
  211.98 intervals (the gap [1, 2] of depth 2 at the chains' light, its
  group delay referred to the last free Node, COMPUTED at the true
  clock on 2026-09-25; the first draft's 4.085 was the old reading's),
  plus the rung's own offset (the design's blind pin
  214 +- 1; OWED on the flux form and [800, 801]). The run at rest
  confirms exactly these ingredients by clicks: c_l on the board's band
  and the material mirror's delay.
- MOVING WITH **K** ALONG ITS ARM (the longitudinal clock, mirror and
  receiver together at v): the tick is D / (c_l - v) + D / (c_l + v) +
  the delay = gamma^2 (2 D / c_l) + the delay with gamma = 1 / sqrt(1 -
  v^2 / c_l^2): 218.43 at v = 0.1, 240.40 at v = 0.2, 316.22 at v = 1 /
  3 (gamma = 1.2252).
- MOVING ACROSS ITS ARM (the transverse clock): 2 D / sqrt(c_l^2 - v^2)
  + the delay = gamma (2 D / c_l) + the delay: 215.18, 225.73, 258.83.
- THE LATTICE'S ANISOTROPY enters through c_l alone, the light's group
  velocity at its k along the arm's axis (0.57689 on an axis at k = 2 pi
  / 64, 0.57735 in the limit); the mirror's delay is the material's.
- THE PIN IS BLIND, and THE MOVING CLOCK IS NOT RUN: its mirror is
  material and does not move (item 3), and no frame puts both its mirror
  and its receiver at rest while the rest of the world moves. The
  transverse form gamma is Lorentz's clock; the longitudinal form
  gamma^2 is the board's own statement that its material does not
  contract (8.4's "declared Nodes widen and never contract"), a
  PREDICTION of the model against nature's gamma, to be stated as such
  and not hidden. The run only confirms by clicks what the closed form
  uses.

**(7) WHAT STAYS OPEN FOR THE OWNER.** (i) The moving name: ADOPTED
(record 1889); its pins re-derived blind in the placed experiments of LAB_TOOLS.md. (ii) With it, the emission of a moving packet (a stock at a moving
name) as the redshift's and Sagnac's mechanism, and its blind pins
re-derived. (iii) Rods: the model has clocks and no rods (item 6), so a moving rigid
arm, and with it the longitudinal light clock and Michelson-Morley, are not
yet in it; whether a rod arises from packets is a question for the owner. (iv) The rows whose material must move (the transponder's
mirror, the index's medium) stay closed forms in the frame form; if the
owner wants them RUN with moving material, that is the push, outside the
one algebra, and is to be said so.

### 9.25 The click over a set of Nodes: which record, when, at which Node (the model owner's question of 2026-09-25 on the Israel clock, through the Boss: "what does the algebra say about the way to catch a click on the board?"; his form, "a Node can shout it and that's it"; his word, "in a detector all the Nodes are armed as long as they are together"; his decision of record 1888: the deletion at once, the one non-local act, and no information through it), marked, before any code

**(1) THE PHYSICIST'S FINDING, CONFIRMED (COMPUTED).** The rule as it
stood in 9.19 (3) (b), "the click fires at the first interval at which
some partial sum L_k reaches (2 u + 1) T / (2 W), at the first such k",
reads the interval by the total's crossing and the Node by the partial
sums at that interval; since each Node's cumulative offer exceeds one
interval's increment, at the crossing every partial sum but the total is
still below the threshold, and the click falls at the LAST Node of the
order for every residue: eight of eight on his layer. On a planted profile
of three Nodes over five intervals whose proportions change in time (the
final shares 0.352, 0.366, 0.282) it gives 0.225, 0.352, 0.423. The
sentence was mine and it conflated the interval with the Node; the
derivation behind it ("the crossing Node is the final ladder's") was
right and its local-in-time form was not written. WITHDRAWN there; the
rule below replaces it.

**(2) THE RULE (DERIVED HERE): THE INCREMENT LADDER.** The data: the
record's residue u (the law's remainder at its birth Node, 9.19 (4)), its
norm T, its wheel W, hence its threshold theta = (2 u + 1) T / (2 W),
fixed at the birth; its ladder, the named DETECTORS in their declared
order with the face last. A DETECTOR OF THE LADDER IS ONE DETECTOR, a cube
of side 3 or more (the model owner's record 1899 of 2026-09-25, (10)
below; the first draft's Nodes within a set are HISTORY). At every
interval t each Node i of the ladder receives the one-way inward flux
f_i(t) >= 0 of the record's rows through ITS PORTS: the Links from a
Node outside the detector into a Node of it (9.19 (3)); a Link between
two Nodes of one detector is not a Port and carries no offer (else the
energy that entered at one Node would be offered again at its
neighbour, and the detector's total would exceed the record's I per
passage); the flux is read from the two
levels after the interval's step, now = a(t) and before = a(t - 1), as
the identity of 9.19 (3) and the prototypes read it; the record's
running total is C(t) = C(t - 1) + SUM over the ladder's detectors of
f_i(t). THE CLICK: at the first interval t* with C(t*)
>= theta, at the Node whose segment of THAT INTERVAL'S increment, laid
out in the ladder's order, contains theta - C(t* - 1); there the record
ends, whole, at that interval (record 1888). WHICH RECORD: the one whose
ladder names the Node. WHEN: t*. WHERE: that Node. ONE QUANTUM, ONE CLICK
(PROVED): C is non-decreasing and theta < T <= the total offered with the
face last (what leaves offers everything at the face), so theta is
crossed exactly once, and the deletion at once leaves nothing to cross it
again. The three tests: generic (the integers u, T, W and the fluxes, no
family name), vector (sums and one comparison per Node, the division with the remainder kept, no root),
local (each Node's flux is its own six Ports'; the two record integers
theta and C(t - 1) travel with the record as its residue does).

**(3) BORN'S RULE (PROVED HERE).** Let u be spread evenly over {0, ...,
W - 1} (the law's remainder, 9.19 (4), COMPUTED equidistributed); then
theta is spread evenly over a grid of W points in [0, T). The segments
[C(t - 1) + SUM over j before i of f_j(t), C(t - 1) + SUM over j up to i
of f_j(t)), one per (interval, Node), partition [0, C(infinity)) and have
the lengths f_i(t). So P(the click at interval t, at Node i) = f_i(t) / T
to the grain 1 / W, and summing over t, P(Node i) = C_i(infinity) / T:
THE DETECTOR'S SHARE OF THE RECORD'S TOTAL INWARD FLUX, whatever the
time profile (the sum over its boundary Nodes of their inward flux from
outside the cube, (10)); over every detector of the ladder the shares
sum to one with the face. COMPUTED on the planted profile: 0.3521, 0.3662, 0.2817 exactly, in
either order of the Nodes. The grain: a count is the number of u whose
theta falls in the Node's segments, within 1 / W of the share; with the
law's remainder the residues are equidistributed and not a permutation,
so the counts are binomial about the shares (9.19 item (4b)).

**(4) THE ORDER WITHIN AN INTERVAL (DERIVED).** The distribution does not
depend on it: the total length of a Node's segments is SUM over t of
f_i(t) for every order. A single record's Node at a given u does depend
on it, so for equivariance bit for bit (9.20 (1)) the order must be data
of the world that transforms with it: the detectors' declared order (a
list's order; inside a detector there is no order, its cube being one
Node, record 1899), never the host's lexicographic order of the lattice,
which a rotation of the cube group does not preserve. Any deterministic declared
order passes the three tests: it is a name's data.

**(5) THE TWO OTHER FORMS, AND WHY NOT (COMPUTED on the planted
profile).**
- (a) THE PHYSICIST'S TWO COMPARISONS (the interval by the total, the
  Node by the cumulative proportions at that interval): exact only when
  the proportions are constant in time; on the profile 0.550, 0.239, 0.211
  against Born's 0.352, 0.366, 0.282, the Nodes that receive early
  overcounted (a screen's centre against its fringes). Malus's two Nodes
  receive in a constant proportion, so his form is exact there; the two
  slits are not.
- (b) THE NODE THAT SHOUTS ALONE (the owner's form): each Node with its
  own threshold from its own remainder and its own accumulator, the first
  to pass shouting. With thresholds spread evenly over [0, T) the race is
  not Born's rule: two Nodes receiving in the constant shares 0.9 and 0.1
  give 17 / 18 = 0.944 to the first (PROVED: P(theta_1 / 0.9 < theta_2 /
  0.1) = 1 - 1 / 18), and on the profile 0.317, 0.248, 0.140 with 30
  percent of the quanta never clicking at the set. With MEMORYLESS
  thresholds (a chance f_i(t) / T at each Node at each interval, the
  Node's own remainder as its die) the race gives the shares exactly for
  a constant proportion among those that click, but only 1 - e^-1 = 63
  percent click and 37 percent pass on to the face, and for a changing
  profile the early flux is overweighted (0.454, 0.344, 0.202).
  EXACTNESS NEEDS THE CHANCE NORMALISED BY THE RECORD'S REMAINING NORM,
  f_i(t) / (T - C(t - 1)): then the survival to t is (T - C(t)) / T and
  P(t, i) = f_i(t) / T exactly (PROVED, the product telescopes), and T -
  C(t - 1) is the ladder's running total, a record integer. So THE NODE
  SHOUTS EXACTLY WHEN IT HOLDS THE RECORD'S TWO INTEGERS, theta and C(t -
  1): its test is whether theta - C(t - 1) - (the increments of the Nodes
  before it in the order) falls within its own increment f_i(t); that is
  the increment ladder read Node by Node, and no other race is exact.
  RECOMMENDED: the increment ladder, read as each Node's own test with
  the record's two integers (the owner's "a Node shouts", in its exact
  form), with the deletion at once (record 1888); the hidden variable
  stays one per record, u, and no Node throws a die (2.7).

**(6) THE PAIR, AND NO SIGNALLING (PROVED HERE; record 1888).** A pair
record (rank 2) has one residue u, its norm T, and per arm its rows and
its named sets (arm 0 the first polariser's Nodes, arm 1 the second's).
ITS CLICK: each arm's TIME by its own increment ladder over its own Nodes
(the arm's rows' flux; the crossing of theta by that arm's running
total); its OUTCOME on the JOINT LADDER of the four outcomes (o_A, o_B)
with the weights R(o_A, o_B) = J^2 (3.6), laid out with o_A outer and o_B
inner in the sets' declared order, the point (u + 1 / 2) / W of the total
SUM of R choosing the outcome for both arms at once: the one gather at
two clicks (record 1141), the one non-local act. THEOREM (no signalling):
the share of records clicking + at Alice is SUM over b of R(+, b) / SUM
of R, and SUM over b of R(o_A, b) = (a_B^2 + b_B^2) abs(v_(o_A))^2 with
v_(o_A) = SUM over a of w_(a b) M_A[o_A][a] the arm's projected label
state, by Brahmagupta's identity (9.16 (2)); the scale a_B^2 + b_B^2 is
common to both o_A and cancels in the share; so Alice's marginal share is
abs(v_+)^2 / (abs(v_+)^2 + abs(v_-)^2), independent of Bob's axis EXACTLY
in integers (her two segments' union is [0, SUM over b of R(+, b))
whatever Bob's axis, the joint ladder being o_A-outer), and independent
of anything beyond her light cone: her click's time is her own arm's
flux (her rows and her Nodes) and her outcome's boundary her own
projection; nothing of Bob's setting, placement or distance enters
either. The same for Bob. The counts are binomial about shares that do
not depend on the far setting: NO INFORMATION MOVES, at any speed. What
is non-local is Bob's outcome GIVEN Alice's (the inner segments), decided
by the same u and the joint weights: the correlation S = 14 / 5 (9.16
(4)), which is not a signal. COMPUTED: for HV + VH the marginal is 1 : 1
at every axis, the maximally entangled pair's.
A DELETION FRONT (the owner's "not all at once"; analysis only, the
reason for record 1888): if the record's end spread from Alice's click
at one Link per interval, Bob's arm would click before the front arrived
on the data at Bob alone (his rows, his axis, u): a local rule at each
arm; by Bell's theorem, and by 9.14's result for the Nodes' group, every
such rule gives S at most 2, against nature's loophole-free 2.4 to 2.7
and the model's 2.8; and a second crossing at Bob before the front would
be two clicks of one quantum. So a front cannot reproduce S above 2; the
deletion at once is the algebra's one non-local act, carrying the pair's
one outcome to both arms, and no information passes through it, by the
theorem.

**(7) THE DETECTOR AS ONE REGION (the owner's word; DERIVED).** For the
rule of (2) and Born's rule, contiguity is not needed: the increment
ladder runs over any named set. It IS needed for the detector as a BODY,
whose own record changes at the click (POSTULATES.md section 10: the
content and the push handed to it), a body being one connected G_48-set
of cubes (8.3, 9.6); and for the NAME: Nodes in separate places are
separate detectors with separate names (Bell's two arms), else one name
would read two places as one and its clicks could not be placed. LOAD
CHECK: a receiver's name on two pieces not connected by Links (the
six-neighbour adjacency on the torus) is refused with the sentence "the
receiver `name` lies on n disconnected pieces; a detector is one
connected region, and separate places are separate names". UNIT TEST
(restated on the cube of (10), 2026-09-25): two 3 x 3 cubes three Links
apart under one name are refused naming 2 pieces; one 3 x 3 cube is
admitted, also across a periodic seam (connected through the seam); the
3 x 3 cube less its centre is refused as filling no box; a box of sides
[2, 2, 1] on a layer is refused naming its sides.

**(8) UNIT TESTS WITH EXPECTED VALUES (for the engine; restated PER
DETECTOR on record 1899, 2026-09-25: every set below is a cube of side 3
or more, cut by the board on a thin axis).**
- The physicist's layer (24 x 9 closed, the emitter at (2, 4), three 3 x
  3 cubes at x = 17 to 19, s1 centred on the emitter's row, s0 and s2
  its images across the periodic seam; the residues u = 0 to 7 on W =
  8): the counts under the order [s0, s1, s2] and under [s2, s1, s0] are
  EQUAL IN DISTRIBUTION (the theorem of (3)), not residue by residue: on
  eight residues of the first draft's one-Node sets he read (4, 2, 2)
  under the one order and (2, 2, 4) under the other, since reversing the
  detectors within an interval's increment moves where the eight
  thresholds fall (a finite wheel is a sample; CORRECTED on his finding,
  2026-09-25); each count is the number of u whose theta falls in the
  detector's segments of the final increment ladder, which the harness
  computes from the same fluxes before the run and the engine gives bit
  for bit; on 128 planted residues the two orders agree within 12 on the
  cubes (the engine's own count, emitter-click 55830eec). (The first
  draft's "the middle Node most" assumed a free layer; on his closed
  layer the mirrors' returns put s0 and s2 ahead of s1: the harness's
  shares decide, not a guess.)
- Malus's four worlds: the shares a^2 / (a^2 + b^2) on the + cube (the
  cube [7, 9] of the bar grown to 11), the expected 128.0, 246.2, 199.3,
  177.2 at 256 records with their bands (9.19 item (4b)).
- The two slits: the screen's counts binomial about the 67 pixels'
  shares (cubes of side 3) of the record's total flux over its passage;
  the visibility 0.96 +- 0.02 re-derived on the grown board (owed); the
  pixel of 3 against the fringe spacing 90 Nodes scales it by 0.998.
- NO SIGNALLING (9.20 (B)'s seventh test): two Bell worlds differing only
  in Bob's axis, (1, 2) against (3, 1), give at Alice's two receivers
  identical counts and identical click intervals, record by record, bit
  for bit; and her counts' shares are abs(v_+)^2 : abs(v_-)^2 of her own
  projection (1 : 1 for HV + VH).
- ONE QUANTUM, ONE CLICK: with the face last on every ladder, every record
  clicks exactly once (the content's count).

**(9) THE MAPPING TO NATURE BY RATIOS (record 1894 of 2026-09-25 on the
Israel clock, whose first sentence, "the detector is sensitive to a
single Node by declaration", is SUPERSEDED by record 1899 and (10): a
detector's sensitivity is its whole cube, of side 3 or more, and a Node
is the grain of the board; his second sentence stands: "a wave spreads
over several Nodes; that does not contradict the detector's
sensitivity").** A Node is the grain and a detector's cube is the
smallest thing a detector tells apart: a click names the detector, and
nothing below a detector is observable or claimed. THE MAPPING TO NATURE
(DERIVED): on the board a wavelength spans several Nodes and one or a
few detector cubes (the born light's 20.78 Links at [2464, 25], 64 at
the chains' [1, 1], 4 at the Mach-Zehnder's [512, 1]), while a real
pixel is larger than a real wavelength; so an
experiment is compared by the RATIOS it measures, and each pinned ratio
is checked to be free of that scaling: the counts and their shares
(Bell's S, Malus's shares, Grover's and Deutsch-Jozsa's counts) are
numbers of clicks and carry no length; a fringe spacing or a centroid in
Nodes (the two slits, de Broglie's fringes) is compared as spacing over wavelength, L / d
on the board as in nature; a first rung or a tick is compared as a ratio
of intervals (the clocks, the redshift, the round trip, Sagnac, the
light clock); an index as a ratio of delays. WHERE A PIN DOES DEPEND ON
THE GRAIN: the pace fans read k^2 / 48, the lattice's own anisotropy,
a diagnostic by construction; and the moving rows' ticks carry the
dispersion's lattice term (0.8146 against 1 / gamma = 0.8165 at K =
0.18556 per Link, 0.2 percent, inside their 0.3 percent bands, 9.24
(2)); no other pin depends on the wavelength's size in Nodes.

**(10) THE DETECTOR CUBE (the model owner's decisions of 2026-09-25 on
the Israel clock, record 1899, through the Boss: "the detector can
define a sensitivity, say a cube 3 by 3: when there is a click the whole
cube shouts; the detector does not know which Node shouted in the cube;
the detector's sensitivity is its size; there is a minimal size of 3 by
3"; "cubes smaller than side 3 must be refused"; ADOPTED with the
increment ladder at the detector level).** WHAT THE MATHEMATICIAN
CORRECTED WITH THE OWNER, in his words: the cube does not shout by a
count of Nodes shouting; its one reading is the FLUX INTO THE CUBE
through its Ports from outside (9.19 (3)), and the click is the
detector's when the record's running total crosses its threshold in the
cube's segment of the interval's increment (2); so the cube's share is
its share of the record's inward flux, Born's rule per detector (3).
THE PER-DETECTOR FORM (DERIVED): the operation of the click is the
projection onto the detector's region: the flux through the region's
Ports is the SUM over its boundary Nodes of their inward flux from
outside the region (the Links between two Nodes of the region carry no
offer, (2)), so a detector's segment of an interval is the sum of its
Nodes' segments and its share is the sum of its Nodes' shares; the order
inside a detector no longer exists (one segment), and only the declared
order of the detectors decides within an interval (4). The record is
deleted whole at the click (record 1888) and the line names the
detector, never a Node. THE MINIMUM SIDE 3, ITS REASON (DERIVED; the
Boss's reading confirmed): a box of side 3 is the smallest with an
INTERIOR Node, a Node all of whose six neighbours lie in the region (its
centre), so it is the smallest region with Ports on its boundary and a
Node with none; a box of side 2 has no interior (every Node touches the
outside) and no centre Node; the engine reads a body's centre Node as
the excited record's named set (9.19 (3)); and the sensitivity is then
strictly coarser than the grain: 3 Nodes on a chain, 9 on a layer, 27
in a cube. THE CUT CUBE (the physicist's reading, CONFIRMED; the Boss's
"at least 3 along every axis of the board" is the same statement): on
an axis whose extent is below 3 (a chain's y and z, a layer's z) the
cube is cut by the GameBoard as a block's cube is, so the side required
per axis is min(3, the extent): three Nodes in a row on a chain, a 3 x
3 box one deep on a layer. THE LOAD CHECK (55830eec): a detector's
Nodes are one connected piece (7), fill one box (per axis one run of
coordinates, across a periodic seam the shortest arc, the count the
runs' product), and every side is 3 or more where the board's extent
allows; a set bound to a block is the block's Nodes (side 3 or more,
refused below) or a cube of free Nodes beside it, checked as any
detector; the one-Node receiver is retired. WHAT CHANGES IN THE ROWS
(the placed experiments of LAB_TOOLS.md, each restated blind before any run): every
receiver becomes a cube of side 3 (the two slits' screen 67 pixels of 3
over y = 28 to 228, x = 153 to 155; de Broglie's fringes' 41 pixels; the chains'
receivers three Nodes in a row: the redshift's [4092, 4094], the light
clock's [612, 614], the moving mass's energy's receiver [104, 106]; Malus's + receiver [7, 9] on the bar
grown to 11; Bell's four receivers 3 x 3 cubes beside the polarisers;
Sagnac's wells' own Nodes of side 12; the Mach-Zehnder's regions 5 x 113
and 81 x 5 already so); THE PINS: a count or a share does not move (Bell,
Malus, the computer, Mach-Zehnder); a fringe pattern read on pixels of 3
is the pattern's box average over 3 Nodes, which scales the visibility by
sin(3 pi / L) / (3 pi / L) for the fringe spacing L in Nodes: 0.998 on
the two slits (L = 20.78 x 113 / 26 = 90), inside the band; a centroid
read on binned counts keeps its band of one Node while the lobe spans
several pixels (de Broglie's fringes: the generator's map states it); a first rung is read
at the cube's NEAR FACE, so it holds where the cube begins at the old
Node (the light clock's 612, the moving mass's energy's receiver at 104) and moves by the offset over v_g
where it does not (the redshift's, a ratio of intervals that cancels);
the first-rung pins are owed on the flux form in any case. THE FACE
RECEIVER IS A SLAB AS DEEP AS THE RECORD IS LONG (DERIVED and COMPUTED
2026-09-25 on the generator's run of the two slits' placement): the
zero row beyond an open face is a hard wall, so a face receiver one Node
deep books only the one-way flux of the packet's head before its own
reflection cancels the net flux at the Port, 0.15 of the packet (a
packet of 8 periods at the wavelength 4 on a chain: a slab of depth D
books 0.15 at D = 1, 0.29 at 4, 0.52 at 8, 0.83 at 16, 0.96 at 32 and
0.995 at 64; the same shares for 16 periods at D scaled by two), and the
rest returns into the board; then "what leaves offers everything at the
face" (2) fails, the records whose threshold the direct passage did not
cross click later on REFLECTED light (on the two slits' first placement
half of them, and the pattern read on the screen was the reflections'),
and 9.19 (3)'s proof of one click per passage needs the face to book
what reaches it. THE RULE: every open face is a receiver slab of depth
at least the record's length at the face (the born packet's length, or
the generator's map of a pulse's spread), so that a record's first
passage over the detectors and the faces books its whole norm and every
record clicks on the direct light; the box of side 3 is its lower bound
and this its working depth (32 for the 8-period packets of the two slits,
de Broglie's fringes and the pace fans, 64 for Mach-Zehnder's 16 periods). The rows'
boards carry the slabs' depth; the tools stand clear of them. THE
FRINGE SPACING ON THE LATTICE (PROVED 2026-09-25 on the two slits' run,
which read lobes 52 to 54 Nodes apart where the continuum's lambda L / d
gives 33.8): a ray's direction is its group velocity's, tan theta = sin
k_y / sin k_x from 3 cos omega = cos k_x + cos k_y + 1, so a screen point
at the small angle y / L receives the wave with k_y = (y / L) sin k_x,
and the two openings' phase difference k_y d steps by 2 pi every DELTA y
= 2 pi L / (d sin k_x): at k = pi / 2 that is (pi / 2) times lambda L /
d, 1.571 times, 53.2 Nodes for L = 110 and d = 13; at the first draft's
k = 0.30 the factor k / sin k is 1.015. So a fringe spacing compared
with nature by "spacing over wavelength" (9) carries the factor k / sin
k, a grain term named beside the pace fans' and the moving rows'; the
VISIBILITY and Born's rule are what the row compares.

**(11) THE ONE-WAY FLUX READS A PASSAGE; THE BORN TRAIN AS THE LOAD
CONDITION; WHERE THE FACE SLAB STANDS (the physicist's finding on
emitter-click f0d2d745, 2026-09-25: the light clock's file run by the
one command, MISS, every record clicking on its outgoing pass; and the
Boss's question: can a lawful state make the one-way inward flux exceed
the record's norm, and is the click then Born's rule; DERIVED and
COMPUTED).** (a) The one-way inward flux per Port (9.19 (3): the positive
part per Link, booked after the step) equals the conserved form passing
when the current through the Port keeps one sign, which a travelling
record does: COMPUTED on a chain of light [1, 1], a train of 8 periods at
k = pi / 2 under the tapers books 0.9987 of its norm T through a Port 40
Links ahead and 16 periods 0.9997 (the physicist's smooth packet 1.0017).
A lawful state CAN make it exceed T: a record that STANDS at the Port.
Its standing components (the band's edges, whose group velocity is
about zero) carry an alternating current with no transport, and the
positive part of an alternating current grows without bound: the
uniform birth of 9.17 (6) on twelve Nodes (0.58 of a period at the
wavelength 20.78) booked 4.65 T into the cube beside its emitter within
400 intervals and 4.23 T at the emitter's own Node, so every record
clicked on its outgoing pass; a train of 3 periods books 1.0285 T at 40
Links and keeps growing. So the click of (2) is Born's rule for a record
that PASSES its detectors, and only for it: this is 9.17 (7) (e) made a
condition (a standing record's acquisition is its own Node's share e_c,
a moving record's the flux through its Ports; a broadband pulse at the
emitter's face is both at once and is read wrongly by either). The
SIGNED flux is not the reading: through a thin receiver the net during a
passage is about zero (in at the front, out at the back), so it would not
count what passes, and the ladder cannot carry a negative increment.
THE LOAD CONDITION (DERIVED): every birth is a travelling train (9.17
(6a)); the generator refuses a profile whose one-way flux through a plane
40 Links ahead, run alone on the vacuum, is not T within 2 x 10^-3. (b)
THE FACE SLAB RETURNS WHAT IT BOOKS: the reflection off the zero row
comes back out of the slab, so a slab beside a tool books the tool's own
light, and the light a receiver passes is booked by two regions at once
when the slab stands at its back. THE PLACEMENT RULE (COMPUTED on the
generator's runs): every emitter's tail and every receiver stands at
least one train's length from every slab's front. Mach-Zehnder's emitter
ADJACENT to the x = 0 slab put 0.2078 of T into that face, 32 Links away
0.0079; its far slab 23 Links behind the bright receiver took 0.156 of
the ladder from the receiver (the bright 0.8365), 100 Links behind 0.027
(the bright 0.968); the two slits' slab at the screen's back halved the
screen's count (the share 0.263 against 0.406 with the slab 40 Links
behind), the fringe the same (0.950 against 0.945). (c) A FRINGE ROW'S
TRANSVERSE AXIS CARRIES SLABS, NOT A PERIOD: on a y-periodic layer of 128
the two openings' pattern wraps at 2.41 spacings and adds itself
shifted, and the visibility on the ladder falls to 0.43 (light and matter
alike, COMPUTED); on the layer of 320 with y slabs it is 0.95 for both.
(d) WHERE THE LIGHT RETURNS TO ITS SOURCE, THE DETECTOR IS THE SOURCE'S
OWN NODES (the set bound to the block, (10)): the outgoing train leaves
the body through its Ports (negative, not booked) and the return enters
them (0.998 of T booked, COMPUTED on the light clock's chain); a cube
beside the emitter books the outgoing pass (the physicist's finding:
HISTORY for the light clock's [612, 614]); this asks that the body be
transparent to its born family at the born **K** (9.22 (7a) (iv)). THE
PIN OF A PASSAGE: a record's click interval at a detector is spread over
the passage (a train of 32 Nodes passes a Port in 72 intervals at v_g =
0.44721; the rms of the click intervals 24.8), so the pin is the MEAN
click interval over the stock, (the head's path + X / 2 + 2) / v_g
(COMPUTED 299.7 against the form's 299.6 on the light clock), with the
band 3 rms / sqrt(n), and the stock's first click beside it. What changes
in the rows is in 9.22 (8) (every row but the muon's moving clock, the boxed clocks and the deep
well's clock restated).

**(12) WHAT A CLICK IS, GENERICALLY, AND THE TOOL THAT DRAWS IT WITHOUT
COUNTING THE NODES (the model owner's big question, records 1933 and
1934: "what is a click, really? how do we know a click is produced
without counting all the Nodes? if a click is a change, one turn, how do
we reach the generic rule?"; "the generic rule to draw a detector's
click, and make it a kind of local"; the Boss's reading PROVED and
corrected in two places).** (a) A CLICK IS AN EVENT OF ONE RECORD AND ONE
OBJECT: the record's one quantum, its norm T fixed at birth and conserved,
handed over to an object; the click falls when the handed-over share
reaches the record's drawn share (2 u + 1) / (2 W), the residue u the
law's own remainder at the birth Node ((2), 9.19 (4)); no Node clicks,
the object clicks as a whole (10). (b) WITHOUT COUNTING THE NODES, THE
EXACT BOUNDARY STATEMENT. The form is conserved and moves only across
Links: for any region R the change of its share over one interval is the
SIGNED sum of the fluxes through its Ports, E_R(t) - E_R(t - 1) = sum
over R's Ports of G_ij (9.19 (3), the discrete Gauss law, exact). The
tally reads the POSITIVE PART of each Port's flux, sum over R's Ports of
max(G_ij, 0): a boundary quantity too, read at the same Ports, but not
the net: the net is what the region HOLDS, the one-way sum is what has
ENTERED, and the two agree exactly for a passage (a travelling record's
current through a Port keeps one sign, (11) (a)) and differ where the
record stands at a Port or returns through it. So the tool reads the
boundary, never the volume (a cube of side s has 6 s^2 Ports, not s^3
Nodes), and a large system needs one tally per record, not a count of
its Nodes; the tally is exactly "what has crossed in", the Boss's
statement with the positive part in place of Gauss's net. (c) ONE TURN,
AND WHETHER THE STANDING AND THE TRAVELLING CASES ARE ONE BOUNDARY
STATEMENT: they are NOT one boundary statement but one FORM read two
ways. For a standing record the flux through every Port is zero (the
Wronskian of a mode vanishes, 9.17 (7) (a)), so the boundary reads
nothing and the tally accrues the Node's own share e_c, a VOLUME reading
of the same form, one period's sum being one whole quantum, T = P e_c
(9.17 (7) (e)): its click falls at a drawn phase within ONE TURN of its
own clock, exactly; for a travelling record the turn is its passage into
the object. The identity that joins them is the one of (b): the change
of the share equals the net flux, so where nothing crosses the share
itself is the tick; the standing Node is not a degenerate boundary but
the other side of Gauss's law. (d) THE GENERIC LAW IN ONE LINE: every
record clicks once, when the share of its one quantum acquired by an
object reaches its drawn share; the acquisition is read on the object's
boundary as what has crossed in where the record moves, and as the
object's own held share where the record stands. (e) THE TOOL, THREE
STEPS PER INTERVAL, AND WHAT IN IT IS LOCAL: (1) each object sums, over
its own Ports, the positive part of each record's flux through the Port
(local: a Port's flux is the two ends of one Link, and the sum is the
object's own gather); (2) each record carries three integers of its own,
its norm T, its residue u with its wheel W, and its tally C; (3) the
objects' increments for that record are added to its tally in the
declared order, and at the first interval at which 2 W C reaches (2 u +
1) T the object whose piece holds the crossing clicks and the record is
deleted whole. THE COST is the Ports the record currently touches, not
the board: a record's rows are zero where it has not yet reached (one
Link per interval), so nothing is added before it arrives. WHAT IS LOCAL:
every gather is local; the addition across the objects one record touches
and the deletion of that record's rows everywhere are the click's one
non-local act (record 1888), and Bell's theorem forces it ((6): a click
that is fully local gives S at most 2). THE BOSS'S "WHOLLY LOCAL WHEN ONLY
ONE OBJECT IS REACHED", CORRECTED: when a record's form reaches one
object only, the DECISION is local (the tally is that object's own sum,
compared with the record's own integers at the object), but the DELETION
is not: the record's rows elsewhere (its tail, its part not yet arrived,
its reflection) vanish at once; the click is wholly local only for a
record wholly inside the object. THE DECLARED ORDER: it decides only how
one interval's increments are split among objects reached at once, and
the counts are equal in distribution under every fixed order ((8), the
physicist's correction), so any declared order serves Born's rule; what
cannot be replaced is the SUM across objects: separate tallies racing per
object lose Born's rule (the race, 17 against 18 on the Born share), so
the one addition is the price of the quantum case, one quantum shared
among several objects (the two slits, Bell), and it is the only price.
(f) THE UNIVERSE: it has no boundary and no Port, so it cannot click by
crossing; a standing record named on the whole of it clicks once by its
own turn and leaves it empty (9.26 (4a)).

### 9.26 A body's frequency, energy and momentum, and the whole's; the clock of a whole; time's reversal; the recurrence of the board (the model owner's four questions of 2026-09-25 through the Boss; DERIVED and PROVED here, for the paper in plain words)

**(1) FREQUENCY, MOMENTUM AND ENERGY OF A BODY (the Boss's reading,
confirmed on frequency and momentum, corrected on energy).** FREQUENCY
is the rotation of a shape per interval: the law is the same at every
interval, so its solutions of one shape are the modes, each turning
uniformly, 2 cos omega = a / b (1.1, 8.1, 9.22 (7)); a body's frequency
is its bound mode's own rotation, set by the body's pair and extents
and by nothing outside it, and seen from outside only as a rate of
clicks (its births come at the residue's phase of that rotation, 9.17
(7) (b) and (e)). MOMENTUM **K** is the advance of the phase per Link
along the axes: the law is the same at every Node, so its solutions of
one shape along space are the characters and the packets built of them
(9.24 (2)); **K** is zero for a shape at rest, is carried by a packet as
its own integer, and is tied to the frequency by the body's band
omega(**K**): what frequency is for the intervals, momentum is for the
Links. ENERGY is two things the algebra keeps apart. (a) THE FORM I of
a record (9.19 (3)): the one bilinear invariant of the rule, what the
law keeps step by step, what the flux moves through Ports and what a
click's ladder partitions (Born's rule, 9.25 (3)); for a mode every
Node's share is e_i = D_i p_i^2 sin^2 omega, so I scales with the
amplitude squared and with sin^2 omega and not with omega; and a
record's amplitude is a convention of its write (9.17 (7) (c)), so the
form is the measure of a wave and no energy per quantum. (b) THE
QUANTUM: one record, counted once at its click, whatever its form: the
same rotation at twice the amplitude is one record still, with four
times the form. The algebra has no E = h f: nothing in the law ties a
record's form to its rotation. The paper may DEFINE the energy of a
quantum as its rotation, hbar omega, to speak nature's language; that is
an identification the algebra neither derives nor contradicts (the
form's scale being free), and the CONSERVED quantities of the law are I
step by step and the count at every click. THE MOVING BODY (the Boss's
question): the phase phi = **K** . x - omega t of a packet turns at
omega(**K**), above omega_0, when read at a fixed Node, and at omega -
**K** . grad omega = omega_0 / gamma_eff, below omega_0, when read along
the packet's own centre (9.24 (2); the bound clock's second term, 9.22 (8a)): one phase, two
readers. The body's clicks come at its own centre's rotation, so its
tick slows as it moves while its frequency at a Node rises; both hold
at once because omega - K d omega / d K = omega_0^2 / omega on the cone,
the identity of the dispersion.

**(1a) THE OWNER'S CANDIDATE LAW, "every body has its own click by its
frequency, and if it has no frequency it has no click" (2026-09-25,
through the Boss; TESTED against the algebra).** (a) NO FREQUENCY, NO
FORM, NO CLICK, a THEOREM: for a mode every Node's share of the
conserved form is e_i = D_i p_i^2 sin^2 omega (9.17 (7) (e), PROVED), so
a record of zero frequency carries zero form identically, and its
threshold cannot be reached by an acquisition that has nothing to
acquire (a record of zero norm is no record: the loader refuses it,
9.17 (6a)). Zero frequency IS a lawful state of light's family, the
static level (now = before = p, 2 cos omega = 2 at **k** = 0, the band's
top), whose form is 0 exactly; and its mirror at omega = pi (now =
-before, the alternating level, the band's other edge) carries zero form
as well, sin pi = 0: the two states that are their own reverse in time
carry nothing and click nowhere. A massive kind has NO zero-frequency
mode at all: its band's bottom is omega_0 = arccos(num / den) > 0 (8.1),
and no well raises 2 cos omega to 2 short of light's own pair. What is
NOT the algebra's in the sentence is "energy per quantum proportional to
frequency": the form goes as the amplitude squared times sin^2 omega
((1) above), so it vanishes with the frequency quadratically and is not
the frequency times the quanta. (b) A STANDING RECORD clicks by its own
frequency EXACTLY: the excited record's running total accrues e_c per
interval, the same every interval, and its rung fires at the phase (2 u
+ 1) / (2 W) of its own period, a uniform waiting time in [0, P), one
birth per half period on average (9.17 (7) (b), (e) and (f); COMPUTED in
the engine at 294a7c80: the six waits within two intervals of (2 u + 1)
P / (2 W)); so "every body has its own click by its frequency" is the
emitter's rule of 9.17 (7) (f) at the set's own Node, word for word, the
body's click being its birth. (c) A TRAVELLING RECORD clicks by the
ARRIVAL of its form at a detector, through the detector's Ports (9.25
(2), (11)), and a detector has no frequency of its own (it is a set of
Nodes, not a body): its pace is the record's group velocity, from the
band, not a rotation. THE ONE LAW that holds both is the click rule as
adopted: EVERY RECORD CLICKS WHEN ITS NAMED SET HAS ACQUIRED THE
RESIDUE'S SHARE (2 u + 1) / (2 W) OF ITS CONSERVED FORM, the acquisition
running at the record's own tick where it stands (its frequency, through
e_c) and at the arrival of its form where it moves (its pace, through the
flux); the owner's law is that law read at a body, and "no frequency, no
click" is its theorem (a); it does not hold as "the frequency times the
quanta", which the algebra does not carry.

**(2) THE CLOCK OF A WHOLE (the owner's "the rate of what contains
everything, the sum of all, like gears").** The state is always a sum:
the law is linear. (a) TWO RECORDS SIDE BY SIDE are the direct sum:
each keeps its own rotation, and there are NO BEATS between them: the
rows are each record's own, the flux and the ladder are read per record
(9.25 (2)), so nothing on the board and nothing in a click reads the
difference of two records' clocks (the Boss's "beats in clicks"
corrected: a click's quadratic form is one record's). Beats appear only
within ONE record that carries two components (a train of two wave
numbers): its own form has the cross term. (b) ONE WHOLE OF TWO
ENTANGLED PARTS, the pair of rank 2 (A.11, 9.23): the joint weight
multiplies the two branches' amplitudes, each branch turning at its own
omega_1 and omega_2, and the product of two uniform rotations is one
uniform rotation at omega_1 + omega_2: the whole turns at the SUM of its
parts' clocks, EXACTLY when each part is one shape (one mode, or one
monochromatic train), and over the sum of their bands otherwise; the
sum is that of the complex rotations the two levels encode (a record's
now and before fix its phase; in real parts a product carries the sum
and the difference alike, and the click reads the quadratic form, not
the phase). THE CLAUSE FOR THE PAPER: two things side by side keep their
own clocks and never beat; one whole of entangled parts turns at the
sum of their clocks, exactly for parts of one shape, as energies of a
composite add. A board contained in a larger board keeps its own
frequencies, forms and momenta while it is not coupled to the rest (the
direct sum), and once coupled or entangled they are the larger whole's
(the sum of its parts', I and **K** conserved by the one law).

**(3) TIME'S REVERSAL (the owner: "whether things are reversible in
time except the clicks, or whether the clicks also come out reversible;
the whole big cube should work in both directions").** (a) THE INSIDE
IS EXACTLY REVERSIBLE (PROVED): the step 3 den a_next + r' = num S_6(a)
- 3 den a_before + r with 0 <= r' < 3 den is a bijection of the
states (a_before, a_now, r) -> (a_now, a_next, r'): given a_now, a_next
and r', the integer M = num S_6(a_now) - 3 den a_next - r' equals 3 den
a_before - r with 0 <= r < 3 den, so a_before = ceil(M / (3 den)) and r
= 3 den a_before - M, uniquely. The reversed motion obeys the SAME
recurrence with next and before exchanged and the remainder's sign
mirrored (the floor become the ceiling): the law is symmetric under t
-> -t up to the side of its rounding, which is a convention of the unit
and not a law (8.8; the property test's digests are the check). (b) THE
CLICK is the one deletion: X ends the record's rows at once and the
detector's own record changes (the click line: the detector, the
interval, the record's residue; POSTULATES.md section 10, record 1139).
The record's shape, its two levels on every Node, is kept nowhere, so
THE BOARD WITH ITS DETECTORS IS NOT A BIJECTION: what a click loses is
the record's two levels on all its Nodes less the few integers of the
line, its shape and its phase; the line keeps the count and the
residue, enough to say which record clicked where and when, not enough
to write it back. THE CLICK AS THE ONE EXCHANGE BETWEEN SYSTEMS, AND THE
WHOLE'S FREQUENCY (the owner's line, "the click is a way for systems to
communicate; when the click is not reversible, there is no frequency,
really"; CONFIRMED with one precision): the click is the one exchange of
the model, a record born at one body ending at another whose own record
changes, the exchange travelling between them locally as flux and the
click itself carrying no signal (9.25 (6)); and with the click
irreversible the whole, the board with its detectors, is no bijection,
so the exact recurrence of (4) (b) fails for it: the whole has no period
and hence no frequency of its own, while every body keeps its own clock
between clicks and every record its own rotation; were the click made
reversible by keeping the record at the detector, the whole would be a
bijection again and would recur exactly, with a period, under the one
condition of (4) (b) that its orbit stays bounded. So the owner's
decision on the click's reversibility decides whether the universe of
the model has a frequency; the algebra gives both answers and chooses
neither. (c) A FULLY REVERSIBLE CLICK would keep the whole
record at the detector, a register at its Nodes: it contradicts no
proof (Born's rule, no signalling and one quantum one click are
statements about the forward click and stand whatever the detector
stores), and it contradicts the owner's decision that the deletion is
at once and carries no information (record 1888) and that nothing is
kept at a Node beyond the events there. The birth is the click's mirror
in form (E^T against X, 9.13): the reversed film shows every click as a
birth from the detector's stock and every birth as a click at the
emitter, and it runs exactly where the content the click lost is
supplied. So the GameBoard works in both directions as a LAW, and its
one arrow is the click's deletion: a decision, not a theorem, and the
falsifiable line of 8.9 item 7 stands as the Boss told it.

**(4) THE RECURRENCE OF THE BOARD (the owner: "the frequency of a body
is within how many turns it returns to its initial state; said of the
whole universe, it is cyclic").** (a) A BOUND SHAPE returns to itself
after its period 2 pi / omega in the real recurrence. In integers it
never returns exactly: 2 cos omega = a / b is rational, and by Niven's
theorem the cosine of a rational multiple of pi is rational only at 0,
+-1 / 2 and +-1, so for every clock of the generator omega is no
rational multiple of pi, the rotation is dense on the circle, and the
shape comes back within the rounding and never to the bit. (b) THE
WHOLE BOARD (PROVED, with one condition): by (3) (a) the Inside step is
a bijection of the integer states; on the set of states whose levels
stay within the amplitude bound A, a finite set, a bijection that keeps
the set is a permutation, and every state of a bounded orbit RECURS
EXACTLY after a finite number of intervals and then repeats the SAME
cycle (a deterministic law repeats its process, not another one): the
recurrence in integers, with a period at most the set's size, (2 A +
1)^(2 N) for N Nodes, astronomical. THE CONDITION is that the orbit
stays bounded. The real recurrence keeps I exactly and I is positive
on the band (the form bounds every level by sqrt(I / the least
eigenvalue of **D** - **A** / 6)), so a real orbit is bounded for ever;
the integer recurrence keeps I within the remainder's effect, at most
one unit's worth per Node per step, so I drifts by at most the order of
A per step at worst and of A sqrt(t) at random over t steps; whether
the drift stays below the bound for ever is OPEN as a proof and
COMPUTED as far as the runs go (the property test's digests and the
light clock's 2600 intervals show no drift beyond the rounding). THE
INTEGERS STAY BOUNDED BY REFUSAL, NEVER BY OVERFLOW: the engine refuses
a run whose level exceeds A (world.py, MUST 3's bound) rather than
wrapping it, so a drifting orbit is refused and no false cycle is ever
read. (c) WITH CLICKS THE WHOLE IS NOT CYCLIC: a click deletes and a
stock is finite, so a world of emitters and detectors ends with its
stock spent and its records clicked, the board empty of them (the arrow
of (3)); the recurrence is the Inside's, and a universe that is one
Inside with no click is cyclic in the sense of (b), returning through
the same process.

**(4a) THE THREE-CUBE UNIVERSE AS A DETECTOR, AND THE SPECIAL NUMBERS
(the model owner's question, record 1932: "the universe for us is also a
detector, and a detector alone has a click, no? a three-by-three universe
forces something so that it is periodic and has a click: the numbers we
must choose for it are special numbers so that it turns"; the Boss's
reading PROVED and made exact).** (i) THE CLICK. A detector's running
total accrues the flux entering through its Ports FROM OUTSIDE (9.25
(2)); a universe that is the whole detector has no outside and no Port,
so it never clicks by flux. A standing record named on the whole set
clicks by its own tick ((1a) (b), the emitter's rule), ONCE: then it is
deleted and the universe is empty of it. A click is an exchange between
two systems ((3) (b)); a universe alone has no one to exchange with, and
its only click is its own ending. (ii) THE SPECIAL NUMBERS, EXACT. On
the torus of three Nodes per axis the six-neighbour sum's eigenvalues
are 6, 3, 0 and -3 (each axis contributing 2 cos(2 pi j / 3), that is 2
or -1), and a mode's multiplier is m = 2 cos omega = num lambda / (3
den). The step 3 den a_next + r' = num S_6(a) - 3 den a_before + r on an
eigenvector p with num lambda = 3 den m, m an integer, is a_next = m
a_now - a_before EXACTLY, the remainder 0 for ever (PROVED: the total is
an exact multiple of 3 den); the recurrence a_next = m a - a_before is
periodic for |m| < 2 and unbounded for |m| > 2 (its characteristic roots
lie on the unit circle only there), and by Niven's theorem 2 cos of a
rational multiple of pi is rational only at 0, +-1 and +-2, so THE ONLY
MODES THAT RETURN TO THE BIT ON ANY BOARD have m in {-1, 0, 1}: THE
PERIODS 3, 4 AND 6 (m = -1: a_next = -a - a_before, period 3, omega = 2
pi / 3; m = 0: period 4, omega = pi / 2; m = 1: period 6, omega = pi /
3), while m = 2 (static) and m = -2 (alternating) carry zero form ((1a)
(a)). For light [1, 1] the three-cube realises all three: lambda = 3
(one axis at 2 pi / 3), 0 (two axes), -3 (three axes); COMPUTED on the
integer step with the eigenvector seeds (the profile 2, -1, -1 along each
turned axis, scaled even so that the level one step back is an integer):
the period 6 at lambda = 3 and 4 at lambda = 0 with the remainder 0 and
the form 1458 and 972 in the flux's units; lambda = -3 the period 3 by the
recurrence. A general pair [num, den] reaches them only where num lambda
/ (3 den) is an integer: lambda = 0 (the period 4) for every pair; the
others for num = den, and the gap [1, 2] at lambda = 6 (m = 1, the
period 6): so the special numbers are the periods 3, 4 and 6, and a
three-cube universe that is exactly periodic and carries form turns
with one of them. THE SMALLEST DETECTOR AND THE SMALLEST SUCH UNIVERSE
COINCIDE AT SIDE 3 for one reason: three Nodes on an axis are the least
at which a Node's two neighbours are distinct from it and from each
other (a detector's interior Node, 9.25 (10); a torus whose reads are
not its own Node), the grain of the geometry and nothing more. THE EXACT-RETURN THEOREM, checked at the owner's word ("that is the
theorem we were missing"; PROVED and COMPUTED): A RECORD OF ONE SHAPE
RETURNS TO THE BIT AFTER ITS OWN PERIOD IF AND ONLY IF ITS MULTIPLIER m =
2 cos omega IS AN INTEGER WITH |m| <= 1 AND ITS PROFILE AN INTEGER
EIGENVECTOR (the level one step back an integer); THEN THE REMAINDER IS
0 AT EVERY INTERVAL AND THE PERIOD IS 3, 4 OR 6. Proof: if the two
levels return exactly after P intervals, the shape's rotation satisfies
P omega in 2 pi Z, so omega is a rational multiple of pi and by Niven 2
cos omega is in {0, +-1, +-2}; +-2 carry no form ((1a) (a)), and for m in
{-1, 0, 1} the recurrence a_next = m a - a_before on integers has the
period 3, 4 or 6 with no rounding, since num S_6 p = 3 den m p exactly.
A state of several such shapes returns after the least common multiple
of their periods (1, 2, 3, 4, 6 or 12); every other integer state
returns only by the recurrence of the whole ((4) (b)), never by its
rotation. COMPUTED on light's tori with even eigenvector seeds: the
three-cube carries all three exact returns (the periods 6, 4 and 3 at
lambda = 3, 0, -3, the remainder 0, the forms nonzero); the four-cube
carries the period 4 alone (its other integer multipliers are +-2, the
static and the alternating levels); the six-cube carries all three
again; so THE THREE-CUBE IS THE SMALLEST UNIVERSE THAT TURNS EXACTLY IN
EVERY WAY THE LAW ALLOWS, and its side is the detector's least side for
the one reason above. THE SAME THEOREM IN SPACE (the owner's "everything
is Rubik's cubes", 2026-09-25): the cube group's elements have the orders
1, 2, 3, 4 and 6 and no other, by the crystallographic restriction (a
turn that maps the integer lattice to itself has an integer 2 cos theta,
hence 2 cos theta in {0, +-1, +-2}), which is the exact-return theorem's
own argument read on the lattice's axes instead of on the intervals: on
the one integer lattice of the GameBoard the turns that return exactly
in space and the turns that return exactly in time are the same orders,
1, 2, 3, 4, 6, for the same reason; a body is a sub-cube with its own
turn, the law is the turn, the click is the one cut, and the remainder
is where chance lives (the exact worlds have none). (iii)
PERIODIC AND CLICKING AT ONCE: with the click irreversible one click ends
the periodicity ((3) (b), (4) (c)); a universe cannot be both exactly
periodic and clicking unless its click is made reversible, the owner's
decision of (3) (c); with a finite stock the cycle of births and clicks
ends when the stock is spent.

### 9.27 The coherence of the model owner's decisions with the algebra; the generic way to build a board; the quarks (the model owner's order of 2026-09-25 through the Boss, record 1930: "take my decisions to the mathematician, so he sees that they really are laws that can be used ... see that all the laws are coherent"; "what is the generic way we build a board"; "how do the quarks connect here")

**(A) THE COHERENCE TABLE.** Every decision row of docs/HIGHLIGHTS.md 5.4
from the one algebra on (records 1852 to 1929), each as the owner said
it, the law as a usable statement in the algebra's terms, and the
verdict: CONSISTENT, or DIFFERS with the exact difference and the wording
proposed for his yes. "Consistent" means the algebra proves or contains
the decision as stated; "differs" names where my derivation says
something other than his words.

| The decision (the owner's words, short; the record) | The law as a usable statement | The verdict |
| --- | --- | --- |
| Momentum is conserved on the board; no operation on Nodes but the click; each tool the law's advance on its material plus at most a click (1856) | The rule conserves the board's total momentum and the record's form (8.1, 9.19 (3)); the only acts outside the advance are the click X and its other side the birth E^T (9.13); a tool is a region of pairs and does nothing else | CONSISTENT (the birth counted as the click's other side, as record 1879 says) |
| The residue from the law, never declared (1872) | The residue u = r / g and the wheel W = wall / g from the record's own remainder at the centre Node after its first advance (9.19 (4), (4e)); the loader refuses a declared residue | CONSISTENT |
| An experiment is an algebraic experiment: the world says what is on the board, the engine does the algebra, the outcome derived before the run (1873) | The table of 9.22 (8): every row a list of regions and a blind pin computed from the algebra; the run checks in clicks | CONSISTENT |
| The one algebra: one element, one operator, covariant under the cube group and the translations; the click deletes, the birth writes; at most three families; one border (1875) | 9.20 (the one operator), 9.21, 9.22 (2); the loader's three-family bound | CONSISTENT |
| How an experiment is built: a list of what is on the board; never a residue, a wheel, a take, a grace, a TRAIN, a rate, a heading or a table (1875) | The list of 9.22 (2); the born profile of 9.17 (6a) is the GENERATOR'S integers on the emitting body's Nodes, its length the body's extent along its momentum, its wavelength the family's born clock: the experimenter declares the body and its clock, never a train | DIFFERS IN A WORD: "never a train" stands for the lamp's declared count of periods (retired); the birth's shape is a travelling train the generator writes from the body's extent. Proposed wording: "no train is declared; the born profile's length is the emitting body's extent along its momentum" |
| What a lab tool is: a region of the operator, a cube of the holder family with its material integers, its momentum, at most a birth and a name (1875) | The tool cards of LAB_TOOLS.md; the bodies with extents per axis (a slab, a line, a cube) since 9.22 (8) | CONSISTENT (a cube become a box of extents, record 1929's bodies with extents) |
| The initial state: the sum over the occupied modes of the composed operator of the quanta times the profile, the momentum's character for a moving body, every remainder 0, checked at load bit for bit (1875) | 9.22 (3) and (7); the remainders 0 at the write and nonzero after one step, where the residue is read | CONSISTENT |
| An experiment checks only clicks (1875) | 9.21; the pins' file form of 9.22 (8): every reading a click's count, interval, cadence, ratio, sum, fringe or centroid | CONSISTENT |
| No table and no formula on the GameBoard; a birth's born PAIR the world's integers (1878) | No table (9.17 (6)); the birth's integers are the born TRAIN, a profile at both levels on the body's Nodes (9.17 (6a)); the two-integer pair on every Node is a flat pulse, broadband, whose one-way flux exceeds the norm 4.65 times beside its emitter (the physicist's finding at f0d2d745) and it is refused | DIFFERS: the born pair of record 1878 is replaced by the born train, a derivation from the physicist's finding, NOT YET THE OWNER'S DECISION. Proposed wording for his yes: "the birth is a travelling train of the generator's integers on the body's Nodes, at least eight periods under an envelope; a flat pulse is refused" |
| The crystal: the click of the arriving record then the birth of an entangled pair; the pair's directions set by where the receivers are placed (1879) | A.11; the pair's two records are two trains on the crystal's Nodes with their momenta along the crystal's long axis, toward the polarisers (9.22 (8), Bell's four settings) | CONSISTENT (the crystal a body of extents 3 x 32 so that each train fits) |
| Three roles on the board: the generator the only writer at interval 0, the law at every Node, the click reader the only reader; no world writer (1879) | 9.22 (7) with the stamp; the generator the operator iterated with its stop ((7a) (ii)) | CONSISTENT |
| Where a tensor enters: the pair of rank 2 only, born by the crystal, never written at interval 0 (1880) | 9.23; the pair's clock the sum of its parts' (9.26 (2)) | CONSISTENT |
| The input file and its check in integers; a failing file refused; recomputation at load a diagnostic (1886) | 9.22 (7); the born train's checks the form, the flux sign along the momentum and the hash (9.17 (6a)); the transparency condition (7a) (iv) | CONSISTENT, with two checks added for his yes (the train's, the transparency's) |
| One command, one output file per experiment, in parallel (1887) | tools/run_inputs.py; the pins' readers of 9.22 (8) | CONSISTENT |
| The click the one non-local act; no information through it; the click what the Outside sees (1888) | 9.25 (6) no signalling; 9.26 (3) (b): the click deletes the record's shape at once and keeps the line only | CONSISTENT |
| Mach-Zehnder: the dark port has no inward flux and never clicks (1891) | The dark port's share is the splitters' imbalance over the train's band plus the lattice's diffracted wing, 0.0079 on the body's mode envelope at 16 periods (0.0054 under the window, HISTORY; 9.22 (8)): one dark click in 100 within the algebra, two at the 10 percent level, three a defect | DIFFERS IN THE NUMBER: not exactly zero on a lattice at one wavelength's band. Proposed wording: "the dark port's share is below one click in a hundred, the band's residual; the bright port takes the rest" |
| What lies between the tools is neglected with a stated reason (1891) | The placed experiments of LAB_TOOLS.md, one clause per row | CONSISTENT |
| A moving body: a packet carried by its momentum's character, its clock slowed by its own dispersion, no acceleration; a light clock across its arm reads gamma; along the arm withdrawn (1895) | 9.24 (2); 9.26 (1): one phase, two readers; 9.22 (8a): gamma at the kind's own cone c_eff with a lattice term of order K^4 | CONSISTENT, with one precision for his yes: the dilation is Lorentz's at the kind's OWN cone c_eff, below light's c by omega_0^2 / 6 (8.1 (ii)), and light's gamma to the bands' precision |
| A detector's sensitivity is its cube of side at least 3; the click the detector's, never a Node's; the increment ladder at the detector level (1899) | 9.25 (10); the one-Node line of record 1894 superseded (9.25 (9) HISTORY) | CONSISTENT; two additions for his yes: the face is a slab as deep as the train, standing a train's length from every tool, and where the light returns to its source the detector is the source's own Nodes (9.25 (11)) |
| The paper on the new engine (1899) | 9.22 (8) and (8a) the paper's sources; the names of record 1925 | CONSISTENT |
| Sorkin's three openings: the algebra gives exactly zero for a fixed operator, the board a small term from the openings coupling through the wall (1911) | 9.22 (8): the sum +0.02 of ABC's screen on the mode envelope, the click's own term at the board's grain; the pin S = 0 +- 284 at 16384 records per world (the +80 +- 400 of the slab at the screen's back HISTORY) | CONSISTENT |
| Twenty-four experiments: eighteen measured, six algebraic, the sixth gravity's forms under a shell average (1915) | 9.22 (8) and (8a) | DIFFERS ON THE SIXTH: gravity's forms are not the algebra's (no field around a body; the pair-field a hypothesis under its own identity); replaced by the universality of the tick. Proposed wording: "the sixth computed experiment is the universality of the tick; gravity waits on a hypothesis outside the law" |
| The click rule in one statement; the emitter's pace its own clock (1918) | 9.17 (7) (f); built at 294a7c80, the waits within two intervals of the rule | CONSISTENT |
| The convergence to the freeze; no run against a pin before the engine is stable (1918, 1924) | The table's pins registered before any run; the placements re-derived blind | CONSISTENT |
| Names with meaning (1924) | Applied in chapters 8 and 9, the tool cards and the placed experiments, the definitions and the postulates (record 1925) | CONSISTENT |
| The generator is the operator iterated, with its stop; the state only turning by its own clock (1924) | 9.22 (7a) (ii) as aligned at 86e1df43: the stop the first iterate that passes the loader's residual bound (the built stop, a9ab486f, confirmed), the clock the operator's quotient in exact integers; the one-unit stop that stood in this row is withdrawn | CONSISTENT |
| Building a world: each body generated alone on the final board; composing is placing; two bodies two only while each tail at the other's Nodes is below the rounding floor, nearer one body with one mode; the margin the decay length (1929) | 9.22 (7a) (v) the exact split and the declaration rule; (B) below | CONSISTENT, with one precision: the margin is the distance at which the mode's tail falls below ONE UNIT AT THE SEED'S AMPLITUDE, ln(A) over the decay constant kappa (Sagnac's wells 80 Links apart at 2^20), since the tail scales with the seed and the bound does not |
| Energy and momentum on the board; the frequency a return; the universe cyclic, reaching its initial point though perhaps not through the same process (1922) | 9.26 (1) and (4): frequency the shape's rotation, momentum its twist, energy the conserved form and the counted quantum; a shape returns within the rounding, never to the bit; the Inside on a bounded orbit returns EXACTLY and through the SAME process; with clicks the whole is not cyclic | DIFFERS IN THREE PLACES: (i) energy is the form, quadratic in the amplitude and in sin omega, not the frequency times the quanta (no E = h f in the law); (ii) the return is through the same process, a deterministic law repeating its cycle; (iii) cyclic only for the Inside with no click and on a bounded orbit. Proposed wording: "the law's Inside is cyclic, returning exactly through the same process on a bounded board; the world with clicks is not, and its arrow is the click's" |
| Every body has its own click by its frequency; no frequency, no click (1926) | 9.26 (1a): a theorem for "no frequency, no click" (the form vanishes with sin^2 omega); the emitter's rule for a standing record; the arrival's rule for a moving one; the click rule of 1918 the one law | CONSISTENT as a law read at a body; DIFFERS if read as "the frequency times the quanta", which the algebra does not carry |
| The click the systems' way of communicating; an irreversible click leaves no frequency of the whole (1927) | 9.26 (3) (b): the click the one exchange, carrying no signal; with the click irreversible the whole has no period and no frequency of its own, every body keeping its clock | CONSISTENT, with one precision: reversibility once the detectors' records are counted would need the detector to keep the record's whole shape, the register of record 1888's deletion; the line keeps the count, the interval and the residue only |

TWO DECISIONS THAT PULL AGAINST EACH OTHER, for the owner: (i) "a
birth's born pair" (1878) and "never a train" (1875) against the born
train of 9.17 (6a), which the physicist's run forced: his yes on the train
retires the pair and reads "never a train" as "never a declared one".
(ii) "The universe is cyclic" (1922) against "the click is the one
non-local act, the record ends at once" (1888): a deleted record cannot
return, so the world with clicks has no period; the two hold together
only as "the Inside is cyclic, the click is the arrow" (9.26 (4) (c)),
which is what the algebra proves. No other pair conflicts; every other
difference above is a precision the owner can adopt in one word.

**(B) THE GENERIC WAY TO BUILD A BOARD (from record 1929, the physicist's
answer, made one statement and one ordered procedure).** THE STATEMENT:
A WORLD IS ONE BOARD, ONE OPERATOR AND A LIST OF REGIONS; EVERY REGION IS
GENERATED ALONE ON THE FINAL BOARD AND PLACED, NEVER REGENERATED; THE
OPERATOR IS THE SUM OF THE REGIONS' PAIRS; TWO REGIONS WITH RECORDS ARE
TWO BODIES ONLY WHILE EACH ONE'S MODE IS A MODE OF THE COMPOSED BOARD
WITHIN ONE UNIT, ELSE THEY ARE ONE BODY WITH ONE MODE; THE INITIAL STATE
IS THE SUM OF THE SEEDED MODES, EACH RECORD ONE MODE WITH ONE CLOCK; AND
THE BOARD IS AS LARGE AS THE MARGINS AND THE PATHS ASK. THE PROCEDURE, in
order, the same for a small world and a large one: (1) THE BOARD AND
THE FAMILIES: the extents per axis, periodic or open per axis, the
families (at most three: light, the experiment's matter, the holder of
the tools' bodies) with their vacuum pairs and, for an emitting family,
its born clock. (2) THE MATERIAL REGIONS, which carry no record: mirrors
and walls (the gap [1, 2] of depth 4), splitters (the diagonal line of
[2, 3]), polarisers (a holder body with its axis), a medium (a bound
body with the coupling), each a box of extents per axis; they are placed
first because every body's mode is generated with them in place. (3)
THE BODIES WITH RECORDS: emitters (a well of the holder or the matter
family, its extent along its momentum the train's length, its coupling
(g, G), its stock), wells with a quantum at rest (the clocks), the
crystal (a holder body of extents 3 x 32 with its branches); EACH IS
GENERATED ALONE ON THE FINAL BOARD with every record-free material region in place and every other record-carrying body's region replaced by its family's vacuum (the same statement as 9.22 (7a) (i); record 1947 (C)):
the operator iterated in integers until the shape only turns, its clock
read by the Rayleigh quotient, its residual checked ((7a) (ii)). (4) THE
COMPOSITION CHECK: with every body placed, each body's own mode is
checked on the composed operator outside the other bodies' Nodes; it
passes when its tail at every other body's Nodes is below one unit at
its seed's amplitude, the distance ln(A) / kappa from each (kappa from
cosh kappa = 3 (den / num) cos omega_b - 2, 9.22 (9)); where it fails the
two are one body with one mode, generated as one region ((7a) (v)); a
moving body is its packet with its momentum's character and its moving
name (9.24). (5) THE DETECTORS AND THE FACES: every detector a cube of
free Nodes of side 3 or more (or a body's own Nodes where the light
returns to it), every open border a face slab as deep as the train, every
detector and every emitter one train's length from every slab (9.25 (10)
and (11)); the ladder's order declared. (6) THE BIRTHS: the born train on
each emitting body's Nodes along its momentum (9.17 (6a)), the emitter
transparent to it ((7a) (iv)). (7) THE BOARD'S SIZE, checked last: every
body a decay length from every face and from every other body, every
path (the passage times, the round trips) inside the run's intervals,
the fringe geometry as the row states it. (8) THE STAMP AND THE PINS:
the generator writes the file with its stamp {law, hash}; the algebra's
pin with its band is registered before any run. COMPOSED STRUCTURES: a
structure is a set of regions placed by the same procedure; AN ATOM in
this algebra is a nucleus, a deep well of a heavy family, and an
electron, a bound mode of a second family in a well declared at the same
Nodes (two regions, two families, two records with two clocks), and its
"stability without the electron" has no counterpart in the law: a body
is where its pair is declared and its mode exists whether or not another
record is present; the law has no force of one body on another (the
coupling of 9.19 (4e) is a body's to light alone), so the atom's stability
as a consequence of the electron's presence is outside the law, under
its own identity, as record 881 left it. Small and large worlds differ
only in the extents and the margins: the procedure is one.

**(C) THE QUARKS.** HOW GROUPING WOULD APPEAR: a composite body is one
declared well whose composed operator has several bound modes (9.22 (9)
shows a well of side 32 with three), and a group is several records on
those modes, or several quanta on one mode; the group's clock is each
record's own, and its total form and momentum are the sums (9.26 (2)).
WHAT THE LAW AS BUILT ALLOWS: at most three families on a board, so a
proton of three quark families cannot be declared beside light and a
holder; three records of ONE matter family in one declared well can be;
their masses are their modes' rotations, set by the well's pair and
extents that the experimenter declares (9.22 (9)), not by any binding
among them. WHAT IT LACKS: (i) a colour-like label (light's records
carry the two polarisation labels; a matter record carries none); (ii)
any interaction between records (the law is linear: two records on one
board never act on each other, the only nonlinearity being the click),
so no binding of one record to another and no confinement: a record is
bound by a declared well, never by other records; (iii) a mass from
binding (a mode's rotation comes from the declared pair, not from the
group). THE VERDICT: quark groups are representable now only as several
records on the modes of one well declared by hand, a bag with no colour,
no confinement and no mass of its own; the earlier quark worlds (the
series of examples/events/quarks, the quarks as rows of the family table
with the binding through the table) are HISTORY with the tables and the
take. THE MINIMAL ADDITION, stated as a hypothesis outside the law under
its own identity, never in it: a record-record coupling, one record's
form lowering the weight D at its own Nodes for a second family (the
pair-field hypothesis, a body's pair spread by its record's form: the same
addition gravity would need, (8a)), together with a third label module,
a colour with three values on the matter family's records, and a closure
condition on the bound mode (only the colour-neutral combination of three
records has a mode below the band: confinement as a closure, the
hypothesis of POSTULATES.md on colour); each with its own tests and its
own expectations, and none of it a computation of the algebra as it
stands.

**(D) THE EXCHANGE HYPOTHESIS, UNDER ITS OWN IDENTITY, OUTSIDE THE LAW
(the model owner's idea in the mathematician's session, 2026-09-25: "the
click spreads between the systems and that is how they talk, and that is
also their forces"; his word: "we are closed; pass the idea on so that
they implement it and write it"; STATED here, not adopted into the law
until its gate).** THE STATEMENT: at a record's click at a body (a
detector bound to the block, or any body the record ends at) the
record's momentum integer is ADDED to the receiving body's momentum
accumulator (the drive of the moving name, 9.24), and at a birth the born
record's momentum is SUBTRACTED from the emitting body's; nothing else in
the law changes. WHAT IT IS: the exchange of quanta (birth, passage,
click) made a transfer of momentum, which the owner's decision that
momentum is conserved on the board (record 1856) demands once a record
with momentum is deleted at a body: without it the board's total
momentum drops by the record's at every click. WHAT IT GIVES: pressure
and recoil (a body pushed by the trains it absorbs, an emitter pushed the
other way), the first force of the model, mediated by records; WHAT IT
DOES NOT GIVE: attraction, gravity or binding (an exchange of light
pushes; an attraction would need a record-record coupling, (C)). ITS
IDENTITY: the world key `hypotheses: {"exchange": true}`, off by default,
refused absent, named in the run's record; nothing of the twenty-four
experiments touched, no pin moved. ITS TEST WORLD, `exchange_recoil`: a
chain with the face slabs, an emitter of trains with momentum K along +x
(the born clock [512, 1], the train 32 Nodes, a stock of 64) and a
receiving body of the matter family whose own Nodes are the detector,
both at rest at interval 0; THE BLIND EXPECTATION, a GameBoard diagnostic
and no click count: after the 64 clicks the receiving body has hopped
floor(64 K / W_body) Links along +x and the emitter floor(64 K /
W_emitter) along -x, K the train's momentum integer in the drive's units
and W each body's wall, and the board's total momentum the same at every
interval; a hop count off by more than one Link falsifies the form.
THE THREE TESTS: generic (one integer moved between a record and a body,
no family name), vector (the translation verb on the accumulator, 1.5),
local (at the click's body alone); what it adds beyond the law is a
second act at the click besides the deletion, which is why it stands
outside the law under its own name until the owner's gate.

### 9.28 The central theorem closed with the model owner on 2026-09-25, and the theorems around it, gathered for the record (the Boss's request of 05:52Z: "get from the mathematician all the theorems and the central theorem we closed"; the model owner's words in the mathematician's session, 2026-09-25, 05:30Z to 05:50Z on the Israel clock: "that is the theorem we were missing, check it"; "a click is made when there is no remainder, no?"; "everything is Rubik's cubes, connect it all into one simple thing"; "we are closed, pass it on")

This section adds no statement to 9.25, 9.26 and 9.27; it gathers, one
place and one line each, what the model owner closed with the
mathematician in that exchange, so that the log and Highlights 5.4 can
cite it. Each line points to where it is proved or computed.

**(1) THE CENTRAL THEOREM: THE EXACT-RETURN THEOREM (PROVED and
COMPUTED, 9.26 (4a); the model owner's word, 2026-09-25: "that is the
theorem we were missing").** THE SETTING. The law's step at a Node is 3
den a_next + r' = num S_6(a) - 3 den a_before + r with 0 <= r' < 3 den
(8.1): num and den the clock pair of the family, S_6 the six-neighbour
sum, r the rule's own remainder kept per Node per record. A shape p is
an eigenvector of the six-neighbour sum on the GameBoard with the
eigenvalue lambda; its multiplier is m = 2 cos omega = num lambda / (3
den), omega its rotation per interval. THE HYPOTHESES. One record of one
shape p with integer levels; the board's rule as above; nothing else
(no family name, no click, no boundary: the theorem is about the Inside's
rotation). THE ROLE OF THE REMAINDER. On the shape p the step reads 3 den
a_next + r' = 3 den m a_now - 3 den a_before + r, so the remainder is 0
at every interval IF AND ONLY IF m is an integer (then the total is an
exact multiple of 3 den and the step is a_next = m a_now - a_before
exactly, with no rounding for ever); for every other multiplier the
remainder is nonzero somewhere and the rotation is dense on the circle,
never returning to the bit (Niven's theorem, 9.26 (4) (a)). THE
CONCLUSION. A record of one shape returns to the bit after its own
period if and only if its multiplier m = 2 cos omega is an integer with
|m| <= 1 and its profile an integer eigenvector (the level one step back
an integer); then the remainder is 0 at every interval and the period
is 3 (m = -1, omega = 2 pi / 3), 4 (m = 0, omega = pi / 2) or 6 (m = 1,
omega = pi / 3); m = +-2 carry zero form ((1a) (a) of 9.26). THE PROOF'S
LINE. If the two levels return exactly after P intervals then P omega
lies in 2 pi Z, so omega is a rational multiple of pi and by Niven 2 cos
omega lies in {0, +-1, +-2}; +-2 carry no form; for m in {-1, 0, 1} the
recurrence a_next = m a - a_before on integers has the period 3, 4 or 6
with no rounding, since num S_6 p = 3 den m p exactly; conversely such a
shape returns by that recurrence. Several such shapes return after the
least common multiple of their periods (1, 2, 3, 4, 6 or 12). THE
COMPUTATION (9.26 (4a)): on light's tori with even eigenvector seeds the
three-cube carries all three exact returns (the periods 6, 4 and 3 at
lambda = 3, 0, -3, the remainder 0, the forms nonzero), the four-cube the
period 4 alone, the six-cube all three again; so the three-cube is the
smallest universe that turns exactly in every way the law allows, and
its side is the detector's least side (9.25 (10)) for the one reason
that three Nodes on an axis are the least at which a Node's two
neighbours are distinct from it and from each other. WHAT THE THEOREM IS
NOT ABOUT: it does not say that a click happens when the remainder is 0
(the model owner's question, answered in (2) (e) below), and it does not
change what is local and what is not in a click ((3) (a) below).

**(2) THE OTHER THEOREMS AND FINDINGS OF THE SAME EXCHANGE, one line
each.**
- (a) THE SAME THEOREM IN SPACE (PROVED, 9.26 (4a); the owner's
  "everything is Rubik's cubes"): the cube group's elements have the
  orders 1, 2, 3, 4, 6 and no other, by the crystallographic restriction
  (a turn keeping the integer lattice has an integer 2 cos theta); the
  exact-return theorem is the same argument read on the intervals instead
  of the axes; on the one integer lattice of the GameBoard the turns that
  return exactly in space and in time have the same orders for the same
  reason.
- (b) THE RECURRENCE OF THE WHOLE (PROVED with one condition, 9.26 (4)
  (b)): the Inside step is a bijection of the integer states, so on a
  bounded orbit every state recurs exactly through the same process, with
  a period at most (2 A + 1)^(2 N); that the orbit stays bounded for
  ever is OPEN as a proof and COMPUTED as far as the runs go; the engine
  bounds the integers by refusal, never by overflow.
- (c) THE INSIDE IS EXACTLY REVERSIBLE (PROVED, 9.26 (3) (a)): a_before
  = ceil(M / (3 den)) with M = num S_6(a_now) - 3 den a_next - r', so the
  law runs in both directions up to the side of its rounding.
- (d) THE CLICK LOSES THE SHAPE (PROVED, 9.26 (3) (b)): the click keeps
  the count and the residue and nothing of the record's two levels, so
  the board with its detectors is not a bijection; with the click
  irreversible the whole has no period and no frequency of its own,
  while every body keeps its clock and every record its rotation; a
  reversible click would restore the whole's period, a decision of the
  owner and not a theorem (9.26 (3) (c)).
- (e) THE REMAINDER IS WHERE CHANCE LIVES (DERIVED, from 9.19 (4)
  ADOPTED and (1) above; the owner's "a click is made when there is no
  remainder?" answered the other way round): a record's residue u is the
  rule's remainder at its birth Node at the interval of the click that
  births it, and u fixes where within the acquisition the click falls,
  the drawn share (2 u + 1) / (2 W); in the exact worlds of (1) the
  remainder is 0 at every Node and interval, so every record is born with
  u = 0 and every click falls at the first rung, the same for all: a
  world without a remainder is a world without chance, every click
  predictable, and Born's rule needs the remainder's spread (9.25 (3)); so
  the click is not made by the absence of a remainder; the remainder
  gives the click its place.
- (f) THE PROPAGATION AND THE CLICK ARE TWO WORDS (DERIVED, the owner's
  "a Node clicks to its neighbours and they to theirs"): what passes from
  a Node to its six neighbours every interval is the wave under the one
  operator, local and reversible; the click is the record's end, at once,
  the one act that is not local (record 1888); the conversation between
  two bodies is a birth, a passage and a click, and calling every local
  step a click would erase the owner's own distinction.
- (g) THE UNIVERSE WITHOUT A BOUNDARY CANNOT CLICK BY CROSSING (DERIVED,
  9.25 (12) (f), 9.26 (4a) (i)): it has no Port; a standing record named
  on the whole of it clicks once by its own turn and leaves it empty.
- (h) WHAT A CLICK IS, AND THE TOOL (PROVED, 9.25 (12), the answers to
  records 1933 and 1934, pushed at d2f6e0cc): a click is an event of one
  record and one object; the tally is the positive part of the flux per
  Port, a boundary reading, exactly what has crossed in for a passage,
  the object's own held share for a standing record; the tool is three
  steps per interval at the cost of the Ports the record touches; any
  declared order serves Born's rule, the sum across objects cannot be
  replaced.
- (i) NO FORCE IN THE LAW (DERIVED, 9.27 (C), 9.22 (8a)): the law is
  linear, no record acts on a record, a body is bound to a declared well;
  there is no gravity in the algebra, and "gravity as computation" means
  only that the paper states what would be required and that it is
  outside the law.
- (j) THE EXCHANGE HYPOTHESIS (OPEN, under its own identity, 9.27 (D)):
  at a click the record's momentum integer passes to the receiving body's
  accumulator, at a birth it leaves the emitter's; it gives pressure and
  recoil, the model's first force, not attraction; one test world with a
  blind expectation; nothing of the twenty-four touched.
- (k) THE TWO LEVELS (a reading, not a theorem; the owner's word): the
  algebra is the level that produces clicks, bodies placed on the
  GameBoard and their clicks counted, and there Born, Bell, interference
  and the clocks are theorems; the theory of clicks, bodies as sources
  and sinks of clicks that push, attract or bind, is one level above,
  derivable in principle from ours, and it begins only over the one
  bridge of (j).

**(3) HOW IT SITS WITH WHAT IS WRITTEN.** (a) THE CLICK THE ONE
NON-LOCAL ACT (record 1888): untouched. The theorem is about the Inside's
rotation and its remainder; a click in an exact world is still a
deletion at once (and the addition across objects, 9.25 (12) (e)); the
owner's words to the Boss, "in the systems we build the click is really
non-local, with a theorem and the remainder", are to be recorded as: the
click's deletion is the one non-local act by his decision of record
1888; the theorem is the exact-return theorem, which says where the
remainder vanishes and hence where chance is absent; the theorem neither
adds to nor removes from the click's non-locality. (b) NO SIGNALLING
(9.25 (6)): untouched; it is a statement about the joint ladder of a
pair and holds for every residue, so also at u = 0. (c) THE INCREMENT
LADDER AND BORN'S RULE (9.25 (2), (3)): Born's rule is proved for u
spread evenly over the wheel; in an exact world u is 0 for every record
and the ladder has one rung, so THE EXACT WORLDS ARE PROPERTY TESTS OF
THE ENGINE AND NOT EXPERIMENTS: a Born row (the two slits, Bell) cannot
be run on them, and the measured experiments live on clocks with a
remainder, where the theorem says the record never returns to the bit.
(d) THE CLICK'S REVERSIBILITY AS A DECISION (9.26 (3) (c)): untouched;
the theorem's periodicity is the Inside's, and (2) (d) says what each
decision gives. (e) THE OWNER'S "what is a click" AND "the click as a
tool" (records 1933 and 1934): answered in 9.25 (12), the wording in (2)
(h); nothing of them is owed.

**(4) WHAT THE MODEL OWNER MUST DECIDE (nothing else in this section
waits on him).** (a) Whether the exact-return theorem enters Highlights
5.4 as adopted, with its consequence for the engine: the exact worlds
(the three-cube at lambda = 3, 0, -3 with even eigenvector seeds, the
four-cube at lambda = 0) as property tests that the engine must return
to the bit with the remainder 0, before any experiment (sent to Nature24
as an order to build after his current line). (b) The gate of the
exchange hypothesis (2) (j), once its test world has numbers. (c) The
click's reversibility (9.26 (3) (c)), which decides whether the whole
has a frequency. (d) The born train in place of the born pair (9.17
(6a); the coherence table's first difference, 9.27 (A)), and the five
other differences of that table. (e) The wording of his own summary to
the Boss, per (3) (a): "the click's deletion is non-local by decision;
the theorem is about the remainder and exact return".

### 9.29 Gravity as the clock shift of the pair: what the GameBoard has today, checked at the model owner's word (2026-09-25, in the mathematician's session: "in our Nodes there is a clock shift; place a body and there is a clock shift, and that makes couplings; it is not gravity, it is the clock shift that makes gravity; a body with mass should have gravity there; check me")

**(1) THE CLAIM, CHECKED: CONFIRMED FOR THE MASSIVE FAMILY, with what is
missing named.** The mathematician's earlier line ("today the board has
gravity's effect on clocks, not attraction") was too narrow. A declared
well is a clock shift, and a clock shift attracts: the two are one field
read twice, inside the one operator, with no force term and no new
rule. What the board does NOT have is the well's source (a body does not
make the well around itself) and light's fall.

**(2) THE THEOREM, ONE FIELD READ TWICE (PROVED and COMPUTED here).**
THE FIELD: a family's pair p = num / den per Node, declared per region
(8.1); a well is a region whose pair is closer to 1 than the medium's
(8.3, "a lowered pair, num' / den' > num / den"). THE DISPERSION under
the one operator: cos omega = p (cos K_x + cos K_y + cos K_z) / 3, so
the rest frequency is cos omega_0 = p, and for small K and small
omega_0, omega = omega_0 + p K^2 / (6 omega_0): the inertial mass is m*
= 3 omega_0 / p, that is omega_0 = m* c^2 with c^2 = 1 / 3 (8.1), the
rest frequency the rest energy. THE FIRST READING, THE CLOCK: where p
is closer to 1 the rest frequency is lower, so a body held there ticks
slower (the well [800, 801] on [800, 809]: omega_0 0.04997 against
0.14930; the deep well's bound clock 0.0729 between them, 9.22 (8)):
the gravitational redshift of the rows. THE SECOND READING, THE FALL:
the operator is linear, so a packet's centre follows the ray equations
of its dispersion (the eikonal, Ehrenfest's theorem on the lattice):
d**x** / dt = grad_K omega and d**K** / dt = - grad_x omega = + (lambda(K)
/ (3 sin omega)) grad p, lambda(K) the six-neighbour eigenvalue of the
packet's character; a packet accelerates TOWARD THE LARGER PAIR, that
is toward the lower rest frequency, the slower clock, with no force
term: the same p that slows the clock bends the path. IN NEWTON'S FORM
(small K): the potential is the rest frequency itself, U(**x**) =
omega_0(**x**), and the acceleration is **a** = - grad omega_0 / m* =
- c^2 grad ln omega_0, so between two places the clock's shift and the
fall's work are one number, delta omega_0 / omega_0 = delta Phi / c^2
with Phi = c^2 ln omega_0: Einstein's II.10a with no declared constant
(chapter 5.4 wrote the same sentence under the suspension hypothesis,
a host field with a pin n S_w = d; here it is a theorem of the
operator, the pin automatic). COMPUTED on the law (real-valued levels,
the integer step differing by the carried remainder only): a 400 x 200
layer, a Gaussian well of width 30 at (200, 70), a packet 12 wide at K
= 0.5 passing 45 Nodes above its centre over 500 intervals, and the ray
of the same dispersion beside it, the transverse shift of the packet's
centre in Nodes (toward the centre negative):

| the region on the medium [800, 809] | the packet's centre (the law) | the ray (the eikonal) |
| --- | --- | --- |
| the well [800, 801] | -14.8 | -17.2 |
| the hill [800, 817] (a higher rest clock) | +13.1 | +15.6 |
| the well [1, 1] | -16.6 | -19.4 |
| light [1, 1] through a region [99, 100] (K = pi / 2) | +1.9 | +2.0 |

The sign and the size agree; the packet, 12 wide against the well's 30,
averages the gradient, the difference. So THE EQUIVALENCE OF THE CLOCK'S
SLOWING AND THE FALL is a theorem of the law for a massive family, and
the atom's binding is this fall: the bound mode of 8.3 is a record held
by the same gradient.

**(3) UNIVERSALITY: WITHIN A FAMILY YES, ACROSS FAMILIES NO.** Within a
family the fall is the same for every record and every amplitude (the
operator is linear; the field is the region's). Across families it is
NOT: (a) a well is declared for one family's pair, and another family
in the same region keeps its own pair; (b) LIGHT HAS NO WELL: a family's
pair cannot exceed 1 (at p > 1 the uniform character has cos omega > 1,
an unbounded level, refused by the bound), so a massless family (p =
1) can only have its pair LOWERED by a region, which gives it a rest
frequency and REPELS its ray (the last row of the table: +1.9 away);
a material region slows light's passage (the group index, the index
rows) and bends its phase away. So today's board has gravity for
matter and none for light; nature's light falls (Eddington 1919, and
the Shapiro delay). A clock shift that every family feels would have
to be a shift OF THE NODE (its rotation slowed for all families), not
of a family's pair; the pair cannot express it.

**(4) WHAT IS MISSING FOR GRAVITY PROPER, exactly.** (a) THE SOURCE: the
well is declared in the world file; no body raises the pair around
itself; two bodies in the vacuum are the sum of each alone (linearity),
so neither bends the other: no two-body attraction, no 1 / r. The one
law that would make the well from the body is a Poisson law of the
pair: the pair at a Node raised toward 1 by the form held nearby and
relaxed through the six neighbours (the discrete Laplacian's Green's
function gives 1 / r at long range on the lattice). It is local (six
neighbours) and integer, but QUADRATIC in the levels (the form is the
source, the level is not): a record acting on a record, outside the
linear law; it is stated only under its own identity, a hypothesis
beside the exchange (9.27 (D)), with one test world reading one field
twice: a bound clock beside a heavy body reads its redshift, and a
packet passing the body falls toward it by the same field, with no
declared well. (b) LIGHT'S FALL: a shift of the Node's clock for all
families, (3) (b); not expressible by the pair; a second hypothesis if
the owner wants it. (c) The coupling between families of 8.5 (light's
row gains g times the holder's difference, and back with G) is
additive, linear in each, and shifts no clock: it is not the clock
shift the owner names; the force between two blocks through light of
8.11 rode the push, which is retired (9.24 (b)).

**(5) COHERENCE WITH THE DECISIONS.** Record 1884 (no acceleration, no
ramp) retired the push, a ramp from outside the operator; the fall of
(2) is the operator's own, and the rows are untouched: every row's
well is a uniform block and every moving body of the rows moves in the
vacuum, where p is constant and **K** is conserved; a graded well is a
placement no row uses. Record 1885 (the momentum an integer of every
entry) stands: **K** is written at birth and changes inside a material
by the operator, as it does at every index boundary. The click's rules
(9.25) are untouched: the fall is the Inside's. THE OWNER'S SENTENCE,
made exact: "it is not gravity, it is the clock shift that makes
gravity" is a theorem of the law for the family whose pair is shifted;
"a body with mass should have gravity there" holds for a body placed
IN a declared well and fails for a body placed in the vacuum, whose
mass shifts no clock: that step, mass makes the well, is the one law
the board lacks.

**(6) FOR THE OWNER TO DECIDE.** Whether the Poisson law of the pair
(4) (a) is written as a hypothesis under its own identity with its test
world, and whether a Node's clock shift for all families (4) (b) is
wanted beside it; nothing of the law changes before his word.

### 9.30 The correspondence audit's algebra rows (the Boss's two orders of 06:17Z and 06:21Z on records 1937, 1942, 1943 and 1944): the stale lines, the mechanisms to state or retire, the differences judged, mass and time, and the laws at every Node

**(1) THE STALE LINES, CORRECTED IN PLACE (this head).** Chapters 1 to 7
carry the HISTORY note at chapter 5's and chapter 6's heads (the crowd
clock, the age wall, the shell mean, the delay field and the cosmology rows
are the ray law's readings, not the one algebra's). 8.6 carries its note
(the take, the emitter's own take and the motion-squared pointer retired by
9.12 and 9.19 (3)). 8.9 carries its note (predictions 2, 3, 4 and 5). 9.19
(3)'s bullet on the excited record and its (c) are superseded by 9.17 (7)
(a) and (e): the standing mode's rung accrues e_c and T = P e_c. 9.22 (7a)
(ii) was aligned at 86e1df43 (the generator is the operator iterated with
its stop, the model owner's decision). 9.27 (A)'s generator row now names
the built stop (the loader's residual bound), the one-unit stop withdrawn.

**(2) THE ENGINE'S MECHANISMS THAT THE ALGEBRA DID NOT NAME, NOW STATED
OR RETIRED EXPLICITLY.** (a) THE RAY-LAW PATH (the flights, the digital
line, the collision and meeting tables, the crowd, the drive, the pointers
on the tables) and ITS AGE WALL: RETIRED. The one algebra has one path,
the operator of 8.1 with the click of 9.17 (7) (f) and the birth of 9.17
(6a); the ray law (beam-v1, record 15 of 2026-09-19) was replaced by the
model owner's adoption of record 1875; the age wall's standing was NOT NOW
by record 941 and is retired by 9.22 (8a) and 9.29 (4): no clock on the
board runs slow by a crowd. The engine's default path must be the one
operator's (a world without the key is refused, never run on the ray law):
Nature24's cleanup, 9.21 (3). (b) THE REMAINDER RESCALED WHEN A RAMP CHANGES
THE WALL: RETIRED with the ramp (record 1884). The wall 3 den of a row
never changes during a run; a rescaled remainder is a floor that breaks
the bijection of 8.8 and is refused. (c) A BLOCK'S NODES BOOKED TO ITS OWN
NODE: STATED as host bookkeeping. A body's Nodes form no receiver unless
declared (the source's own Nodes as a detector where the row says so, 9.25
(11) (d)); an outgoing front gives no inward flux at its own body's Ports
(9.19 (3)); what the engine books at a body's Nodes outside a declared set
is a host row and no click. (d) THE BLOCK CLOCK's sign-crossing count named
"click": RETIRED. The clock of a body is its own record's click at its rung
(9.17 (7) (f), 9.26 (1a) (b)); a clock body is an emitting body with a
stock, its ticks its births; a sign crossing is no event of the law, and a
line named "click" that deletes nothing must not stamp a set. (e) THE
CAVITY's per-interval zeroing: RETIRED (9.10 item 4, 9.12): a projection is
not the law; the cavity is a gap pair on declared Nodes. (f) FACES PER
FAMILY and CLOSED BOARDS: RETIRED (one border for every family, record
1875; a board with neither a periodic axis nor a face receiver refused,
9.19 (3) (a)). (g) THE `massive_kind` BRANCHES in the law's path: RETIRED
(9.18 (5), 9.21 (3)): what a record books and which ladder it stands on is
decided by its named sets and its rung, never by its family's kind.

**(3) THE THREE DIFFERENCES, JUDGED.** (a) MIRRORS AS SILENT BLOCKS OF
LIGHT'S FAMILY against BOUND HOLDER BODIES: the operator is the same (a
region where light's pair is the gap [1, 2]); the ALGEBRA IS RIGHT on the
form, ADOPTED by record 1875: a tool is a body of the holder family
carrying the material pairs on its Nodes, with its cube, its orientation
and its momentum 0, so that a tool's card is the body's; the code's silent
light-family block is that body under a wrong name, to be declared as the
holder body at the worlds' rebuild (the cleanup's step 6); no number moves.
(b) A BODY'S RESPONSE SPLIT PER LIGHT RECORD: the split by origin is
LAWFUL and is the algebra's own necessity, stated here: a body's massive
record has a MODE PART (its excited profile, seeded from the stock, which
sources no light, its emission being the birth, 9.17 (2) to (4)) and a
DRIVEN PART per light record at its Nodes (the dielectric response, which
receives that record's difference with g and sources light with G, the
Euler-Lagrange pair of 8.5 with its invariant J); the superposition
principle lets the driven part be kept per light record, equal in total.
WHERE THE CODE DIFFERS AND THE ALGEBRA IS RIGHT: the mode part's receive is
the entry of 8.5 over EVERY light record's columns at its Nodes (the
returning light, another body's light, its own born train), not its own
born light alone; that is what spreads the residues (9.19 (4e) (i)). (c)
THE EMITTER'S BACK-ACTION THROUGH g ONLY, NO G TERM: the CODE IS RIGHT, and
8.5's J is restated: the mode part sources no light (a G source on the
excited mode would be a second, unquantised emission at the body's rest
clock beside the births, which 9.17 forbids), so J holds for each driven
pair (the response record with its light record) and is not claimed for
the mode part, whose form is reset at every birth; 9.19 (4e) (i)'s "(g, G)
for its born family" reads: g on the mode part for the back-action, (g, G)
on the driven part for the medium's index.

**(4) MASS AND TIME, CONFIRMED EXACTLY.** In the one algebra a Node's pair
sets the local pace (the massive group velocity, a body's own rotation,
the index at a coupled body's Nodes, the dilation of motion) and NO CLOCK
RUNS SLOW NEAR A MASS: the vacuum around a body keeps the vacuum's pair
(9.22 (8a)), the old age wall is retired ((2) (a)), and a body's form,
quanta or content changes nothing in any Node's step (the law is linear).
What the board has is 9.29: a DECLARED well is a clock shift, and it bends
and holds its family's records (one field read twice), without a source.
THE MINIMAL ADDITION, in one clause: THE PAIR-FIELD HYPOTHESIS, "the pair at
every Node is raised toward 1 by the form held at it and its six
neighbours and relaxed through them, with one declared integer
coefficient" (a Poisson law of the pair, the algebraic successor of the
physics' delay field of DERIVATIONS_BEAM.md 5.1, where the age moment
obeyed Poisson's equation and slowed the clock by 1 / (1 + k)). THE THREE
TESTS: generic PASS (one primitive, one declared integer, no family name);
local PASS (a Node, its six neighbours, nothing kept beyond the pair);
vector FAIL (the form is quadratic in the levels, not one of the six verbs
on the state vector: a record acting on a record). So it enters only under
its own identity, `hypotheses: {"pair_field": true}`, off by default, with
9.29 (4) (a)'s test world (one field read twice with no declared well), and
the gravitational clock STAYS OUT of the law until the owner's word. Light's
fall needs a second clause (a shift of the Node's rotation for all
families, 9.29 (3) (b)), which the pair cannot express.

**(5) THE LAWS AT EVERY NODE (the model owner's rule of record 1944:
"in the physics we reached laws at every Node; we must use that for the
algebra"), CONFIRMED and LISTED.** THE ALGEBRA STATES, PER NODE AND NOTHING
ELSE AS LAW: (i) the rule at a Node from its own two levels, its remainder
and its six neighbours, 3 den a_next + r' = num S_6 - 3 den a_before + r
(8.1, 8.2); (ii) the pair per Node per family, declared per region, a well
a region of a raised pair (8.1, 8.3, 9.19 (2), 9.29); (iii) the coupling
between two families at a Node, the first difference both ways, the mode
part receiving only ((3) (b), (c); 8.5); (iv) the border: the zero row
beyond an open face, the wrap on a periodic axis, the face slab a receiver
(1.6, 9.19 (3) (a), 9.25 (10)); (v) the flux per Port from the two levels at
the Link's ends, and each object's gather of its positive part (9.19 (3),
9.25 (12) (e)); (vi) the residue read from the remainder at the birth Node
(9.19 (4)); (vii) the birth written on the body's Nodes as the train (9.17
(6a)); (viii) the click: the deletion of one record whole, the one non-local
act (record 1888). EVERYTHING ELSE IS DERIVED: the band and the paces
(8.1), gamma and the tick (9.24, 9.22 (8a)), the redshift and the fall in a
well (9.29), Born's rule and no signalling (9.25), the exact returns (9.26
(4a)), the split at a splitter and the fringe spacing (A.4, 9.25 (10)). THE
PER-NODE LAWS OF THE PHYSICS' WORK THAT THE ALGEBRA DOES NOT STATE, EACH
WITH ITS STANDING: the ray law's walk on the digital line, its collision
slots and its meeting (beam-v1, record 15; retired by record 1875); the
crowd and the age wall, the clock at 1 / (1 + k) (record 941 NOT NOW;
retired, (2) (a)); the delay field and the retarded potential
(DERIVATIONS_BEAM.md 5.1 to 5.3; moved to history by record 1580; its
successor the pair-field hypothesis of (4)); the optical turn of a row in a
crowd (optical-v1, 2026-09-21, a hypothesis under its identity; retired
with the crowd); the push, the drive and the contact (8.11; retired by
9.24 (3), record 1884); the give at the return (atom-give-v1, record 881,
outside the law under its identity, standing); the transformations
("become", a family change at a click; not in the one algebra, the quarks'
verdict 9.27 (C)); the pointers on the cosine and sine tables and the
half-angle rotations (amplitude-v1; retired by 9.14 and 9.18 (5)); the
cavity's projection (retired, (2) (e)); DESIGN.md 4.1's crowded-Node pair
(never built; named now as the pair-field hypothesis's ancestor); the
Hubble rows' crowd (chapter 6, HISTORY). None of these is a law of the one
algebra; two stand beside it under their own identities (the atom's give,
the pair field when the owner says so).

**(6) UNDER RECORD 1940, WHERE THE MATHEMATICIAN AND NATURE24 DISAGREE.**
On the algebra's side nothing is open between us after 86e1df43 (the
generator, the loader's exclusion, the tail check). What this section
sends him to build or to confirm, each a code matter: the mode part's
receive over every light record ((3) (b)); the block clock's "click" line
retired ((2) (d)); the ray-law default, the cavity, the faces per family,
the closed boards and the kind branches ((2) (a), (e), (f), (g)), all in
the cleanup order of 9.21 (3); the holder body's name for the mirror ((3)
(a), step 6). Where he reads the code otherwise, the Boss hears it from
both of us.

### 9.31 The coherence agenda, closed item by item (the model owner's word through Nature24, 07:50Z on his clock: "you, the Boss and the mathematician decide among yourselves on the coherence of the laws, and then we go to the experiments"; Nature24's thirteen items, records 1946 and 1947; the Boss's positions; each item closes by the rule of three, record 1940)

**(1) WHO BIRTHS WHAT: 9.17 (4) STANDS.** A body births a family other than
its own (the born record's rows at the body's Nodes carry the born
family's pair, the vacuum's unless a material is declared; a body's own
well is no vacuum for its own family, so a train of the body's own family
born inside it would be no character). The emitter of a matter train is a
HOLDER BODY coupled to the matter family, as the emitter of a light train
is a body coupled to light: the two rows that said otherwise (de Broglie's
fringes, the moving mass's energy) are corrected in 9.22 (8): a holder
body [699, 700] on the holder's [7, 8] (W = 2100, rich), coupled to
matter with (g, G). Nothing in the law changes (the Boss's position
AGREED).

**(2) THE GENERATOR:** aligned at 86e1df43 (9.22 (7a) (ii), 9.27 (A)'s
row); the operator iterated with its stop at the loader's residual bound,
the owner's word of records 1920 and 1924. CLOSED.

**(3) TWO BODIES:** the stored integer profile of each body is 0 at every
Node of every other body of its family (an integer below one unit is 0),
the loader refusing otherwise with the two bodies, the Node and the value;
Sagnac's wells re-placed 80 Links apart at 2^20 (9.22 (7a) (v)). CLOSED.

**(4) THE BORN CLOCK:** one statement, k = pi p / (N q) with N = 1024:
[512, 1] is k = pi / 2, the wavelength 4; the conventions line of 9.22 (8)
that read "p / q of the circle per Link" (the wavelength 2) is corrected
to it at this head. CLOSED.

**(5) THE COUPLING'S LOAD CONDITION, 9.17 (7) (c):** a REFUSAL AT LOAD, as
written there ("printed at load and refused above"): 6 g A sin(pi n / (d
N)) at most the body's seed amplitude / 1000; an input is LAWFUL or
REFUSED at the load and nowhere else (the Boss's position AGREED); the
registered seeds at 2^20 meet it, a seed of 100 is refused. CLOSED.

**(6) THE EXCITED RECORD'S RUNG, 9.17 (7) (f), UNDER THE TRAIN:** untouched
by 9.17 (6a); the train is the born record's profile, the rung accrues
e_c and T = P e_c. CONFIRMED as built. CLOSED.

**(7) THE INTEGER FORMS, for the loader and the generator (the Boss's
position (7)):**
- (a) THE PACKET (a moving body, 9.24 (2)): the key `packet: {profile,
  momentum, amplitude}`; `profile` the body's rest profile p_i on its Nodes
  (the generator's integers); `momentum` a born clock per axis [[p_x, q_x],
  [p_y, q_y], [p_z, q_z]], K_i = pi p_i / (N q_i) on N = 1024; the seed
  now_i = round(A p_i cos(**K** . (**x**_i - **x**_c))), before_i = round(A
  p_i cos(**K** . (**x**_i - **x**_c) + omega(**K**))) with cos omega(**K**)
  = (num / den) (cos K_x + cos K_y + cos K_z) / 3 of the family's VACUUM (a
  packet moves in the vacuum, no well): the same write as the born train
  of 9.17 (6a) with the profile in place of the window and the tapers; at
  load the conserved form, the flux sign along **K** and the hash, as for
  the train. When the packet is an emitter or a clock, it is the body's
  excited record: its rung on e_c at the name's current centre Node; the
  reseed writes the same packet centred at the name's current centre.
- (b) THE MOVING NAME (9.24 (4), A.14, record 1889): the key `name:
  {Nodes, pace, phase}`; `Nodes` at interval 0; `pace` a pair per axis
  [[vn_x, vd_x], [vn_y, vd_y], [vn_z, vd_z]] declaring the packet's group
  velocity as a rational (v = 1 / 3 is [1, 3]); `phase` the accumulators at
  0 (default 0). Per interval on each axis a_i += vn_i, and while a_i >=
  vd_i the set translates one Link along i and a_i -= vd_i (the drive of
  `by_drive`); the set at interval t is the Nodes at 0 translated by
  floor((t vn_i + a_i(0)) / vd_i). The loader refuses a name whose declared
  pace leaves the packet: with v_g,i = (num / den) sin K_i / (3 sin omega)
  (a host float of the generator) and T the run's declared length,
  abs(T v_g,i - floor(T vn_i / vd_i)) must be at most 1. A name reads the
  flux through the Ports of its current Nodes like any set; a name carried
  on a packet reads that packet's own record (an emitter's rung, a light
  clock's return) at its current centre.
- (c) THE POLARISER'S AXIS (9.14 (b), 9.16 (2), A.5): a receiver set of a
  holder body (its Nodes transparent to light, the vacuum's pair) with the
  key `axis: [a, b]`, integers with gcd 1, the wheel's group element of the
  angle atan2(b, a), (1, 0) the H axis. A record carries `labels: [w_H,
  w_V]`, integers (a pair record a 2 x 2 integer matrix w_ab). At the
  polariser the record's increment f of one interval (the one-way flux into
  the set's Nodes) is laid on TWO OUTCOME NODES, "+" and "-", with the
  weights v_+^2 and v_-^2, v_+ = a w_H + b w_V and v_- = -b w_H + a w_V,
  v_+^2 + v_-^2 = (a^2 + b^2)(w_H^2 + w_V^2) = S by Brahmagupta; the
  increment ladder of 9.25 (2) runs in the units f x S: the click at the
  first interval with 2 W (sum over the ladder's detectors of f_k v_k^2) >= (2
  u + 1) T S, the Node reached by that interval's increments in the
  ladder's order. Malus's share is a^2 / (a^2 + b^2) for w = (1, 0),
  exactly in integers (9.14 (b)). A polariser that ends the record is this
  and nothing more; no rebirth.
- (d) THE CRYSTAL (9.13, 9.16 (5), 9.19 (4a), A.6, A.11): a holder body, a
  well of the holder family with a RICH light pair at its Nodes (9.19 (4a),
  at least 500 remainder values), with the key `crystal: {arms, labels,
  amplitude, coupling}`: `arms` two entries, each {momentum (a born clock
  per axis), Nodes (the arm's birth Nodes)}; `labels` the 2 x 2 integer
  matrix (HV + VH: [[0, 1], [1, 0]]). An arriving pump record clicks at
  the crystal's Nodes (its receiver set; the one-way flux; the record's
  rung), the crystal's own record changes (the count), and the click
  births ONE PAIR RECORD of rank 2 (E^T): arm 0 the train of 9.17 (6a) on
  arm 0's Nodes with its **K** and arm 1 on arm 1's, in the born family's
  rows, the labels the declared matrix, ONE residue u and wheel W read from
  the crystal's remainder at the birth Node, the norm per arm T_a its
  train's conserved form. THE PAIR'S CLICK (9.25 (6)): each arm's TIME by
  its own ladder over its own rows, 2 T_a u + T_a <= 2 W C_a, its rows
  deleted at its own click; the OUTCOME for both arms fixed at the first
  arm's click on the joint ladder R(o_A, o_B) = (sum over a, b of w_ab
  M_A[o_A][a] M_B[o_B][b])^2, M_X = [[a_X, b_X], [-b_X, a_X]] the axes of
  the receivers the arms are aimed at (declared), laid out arm-0-outer,
  chosen by the point (2 u + 1) / (2 W) of the total sum of R; the second
  arm's click, at its own time, names the outcome already fixed. The pair
  record's integers: `rank 2, arms [rows_0, rows_1], labels, u, W, T:
  [T_0, T_1], outcome` (none until the first click).
- (e) THE TOOL BODY (item 12 below): the key set `body: {family, Nodes,
  pair, material, seed, coupling, receiver}`.

**(8) THE RECEDING INDEX, ITS MEDIUM (DERIVED):** neither a holder body
with omega_b above the train's omega nor a longer train. A COUPLED body's
index n^2 = 1 + G g / (omega_0^2 - omega^2) (8.5) lies below 1 at the
train's omega = 0.841 for every bound body of the rows (omega_0 <= 0.15)
and is not used. THE MEDIUM IS A REGION OF LIGHT'S PAIR: a holder body
carrying light's lowered pair [p, q], p < q, on a slab (item 12), with no
coupling. At fixed omega the medium's character has cos K_in = 3 cos
omega / (p / q) - 2 (8.1), so its PHASE index K_in / K is below 1 and its
GROUP index is n_g = v_g(vacuum) / v_g(medium) = sin K / ((p / q) sin
K_in) above 1: at the train's K = pi / 2 (cos omega = 2 / 3), [4, 5] gives
cos K_in = 1 / 2 and n_g = 1.44, [79, 100] gives n_g = 1.55, the gap [1,
2] gives cos K_in = 2, an evanescent character (the mirror, A.3), one
family of numbers. The delay of a passage through a slab of depth d is
d (n_g - 1) / v_g(vacuum) beyond the vacuum's, the generator's run of the
placed slab giving the pin blind; the RECEDING part is the frame form of
9.24 (d): the medium at rest, the emitter and the receiver moving names
((7) (b)), the pin the delay's ratio between the moving pair and the pair
at rest. Fizeau's first-order drag then follows from the medium's own
dispersion read in the moving frame, a number of the model with the
model's phase index (below 1), possibly not nature's (1 - 1 / n^2): stated
when computed, never pinned to nature's before. The row's pin is
recomputed on this medium before its file.

**(9) THE PLACEMENT RULE AND THE TRANSPARENCY:** the placement rule of 9.25
(11) (b) is a LOADER REFUSAL, in integers (every emitter's tail Node and
every receiver's Node at least X Links, the train's length, from every
slab's front along the slab's normal; the condition decides whether a
tally reads a passage, that is whether a reading is lawful); the
transparency of 9.22 (7a) (iv) is a GENERATOR CHECK (a host run of the
train alone against the body) whose number is stamped in the world and
READ AT LOAD: a stamp below 0.99 or absent is refused (the Boss's split
AGREED).

**(10) THE COUPLING TO A MASSIVE BORN FAMILY:** the same form. A body's
`coupling` names the family it couples to; the step applies 8.5's bilinear
form to every record of THAT family whatever its kind: the driven rows
gain g times the record's first difference, the record's rows gain -G
times the driven rows' forward difference, in the one division with the
born family's own wall 3 den (the engine's light scale generalised to the
coupled family's denominators). No branch on the kind; the kind branches
go (9.30 (2) (g)).

**(11) RECORD 1929 AGAINST 9.22 (7a) (i):** they agree, in the Boss's
reading (record 1947 (C)), now written in both places the same way: each
body's mode is generated with every record-free material region (a
mirror, a wall, a splitter, a medium, a barrier) in place and every other
record-carrying body's region replaced by its family's vacuum. The reason:
a material region is part of the body's operator (a barrier beside a well
shapes its mode), while another body's well of the same family would give
the composed operator a hybrid top mode that is no body's summand (9.9
(3)); the "two bodies, two records" check ((3)) then guards the
composition. Nature24 builds (7a) (i) as read here.

**(12) THE TOOL BODY'S INTEGER FORM (9.18 (1) and (2), A.3, A.10, A.12):**
`body: {family: H, Nodes, pair: [num, den], material: {L: [a, b], ...},
seed, coupling: {L: [g, G]}, receiver: {axis: [a, b]}}`. `pair` is H's own
pair at the body's Nodes (default the family's vacuum; a well for a body
with a seed). `material` names the pairs the body IMPOSES on OTHER
families at its Nodes: a record of L reads L's rule there with the pair
[a, b]; a family absent from `material` keeps its vacuum's pair; H's own
record, if any, reads H's rule with `pair`. `seed` is optional: present
for a body that clicks or emits (the crystal, an emitter, a clock body),
absent for a mirror, a splitter, a wall, a medium (a body with no record
has no rung and no click, and is no "silent light block": it is a holder
body). So: the mirror `material: {light: [1, 2]}` on its slab; the
splitter `material: {light: [2, 3]}` on a one-Node diagonal layer (A.4,
the exact half at k = pi / 2); the medium `material: {light: [p, q]}` on
its slab ((8)); the barrier of de Broglie's fringes `material: {matter:
[1, 2]}`; the polariser `receiver: {axis}` on Nodes transparent to light;
the crystal `seed` and `crystal` ((7) (d)); an emitter `seed`, `coupling`
and `born`. One key set for every tool; the loader refuses a light-family
body (8.3: light cannot be a body).

**(13) THE CLOCK BODY, AND HOW ITS TICK IS A MEASUREMENT:** the block
clock's sign-crossing count is retired (9.30 (2) (d)); a non-emitting well
has no click in the engine and none in the algebra. A CLOCK BODY IS AN
EMITTING BODY: a stock (64 in the rows), the coupling to its born family,
its born trains leaving to a face slab or circulating on a periodic board
(where their return spreads its residues); its ticks are the clicks of
its own record at its rung on e_c (9.17 (7) (f)), one per birth. THE
PERIOD IS READ FROM EACH CLICK'S LINE, a measurement: for a standing mode
e_c is constant, so the rung's running total is t e_c and the click falls
at the first interval t since the reseed with 2 W t >= (2 u + 1) P; the
click line carries t and the record's residue u (record 1139's line), so
P = 2 W t / (2 u + 1) within the interval's grain (2 W / (2 u + 1) at
most), averaged over the stock; the mean click interval alone is P / 2
(9.17 (7) (b)) and would need a stock of 8 x 10^4 for the rows' 0.3
percent bands, which the residue in the line makes unnecessary. A moving
clock reads the same at its co-moving name ((7) (a), (b)): the mode's tick
at the moving centre, slower by its own dispersion (9.24 (2)). The rows'
"one quantum" is corrected to "a stock of 64" in 9.22 (8) at this head;
the pin of every clock row is a detector's line, never a GameBoard
reading.

**THE TEXT ITEMS Nature24 and the reviews named:** 9.19 (3) (c), 8.6, 8.9
and 9.27 (A)'s stop were corrected at 9ffc0fb2 (9.30 (1)). **THE GATE:**
2c9690cb through 952f745a CONFIRMED (sent at 05:50Z and 06:45Z on the
mathematician's clock); the norm's bound 2^126 the host's guard, the units
the flux's (3 G times the wall); the stop the loader's residual bound.

**(14) THE MODEL OWNER'S WORD ON THE ENGINE, 2026-09-25 in the
mathematician's session (translated: "there are bugs in the engine today,
they must be cleaned; on the board of Nodes there is no ray; an event
duplicates and splits at the Node, and when it does there is a clock
shift, because it is a mass: a mass is coupled to a clock, and light too
is coupled to a clock on the board; check it with the Boss"), CHECKED
AGAINST THE ALGEBRA: his picture is the rule of 8.1 exactly, and nothing
beside it. (a) NO RAY: a record is two levels at every Node it touches,
and every interval the Node's level goes to its six neighbours with the
weight num / (3 den) and turns against its own past, 3 den a_next + r' =
num S_6 - 3 den a_before + r; the "event that duplicates" is this split,
the ray law's walk on a line (beam-v1) is retired (record 1875; 9.30 (2)
(a)). (b) THE CLOCK IS THE SPLIT: the one pair [num, den] sets both the
split's weight and the rotation per interval, cos omega = (num / den)
(cos K_x + cos K_y + cos K_z) / 3; a mass is a pair with num < den, whose
rest rotation cos omega_0 = num / den is its clock (8.1, 9.26 (1)); light
is the pair [1, 1], whose rotation is set by its born **K** alone (cos
omega = 2 / 3 at [512, 1]): mass and light are coupled to the clock by
the same rule, one with a rest clock and one without; a declared well
shifts that clock and bends the family's records toward it (9.29). (c)
THE BUGS ARE THE MECHANISMS BESIDE THE RULE, named in the correspondence
audit (record 1942) and in 9.30 (2): the ray-law path still the engine's
default (a world without the key runs on rays); the `massive_kind`
branches in the law's path; the cavity's per-interval zeroing; moving
material with a ramp and the remainder rescaled under it; faces per
family and closed boards admitted; the block clock's sign-crossing count
named "click"; the mode part's back-action from its own born light alone;
the born pair in place of the train (9.17 (6a)); the placement rule and
the tail check not yet refused at load. Each is a code matter of
Nature24's under the cleanup order of 9.21 (3), gated line by line, and
none is a law change: the law is (a) and (b) and the click.

### 9.32 The one law at the single Node (the model owner's word, 2026-09-25, in the mathematician's session: "look at the small things, at the level of the single Node: the single Node produces a click; and many Nodes, if all the Nodes together produce a click, then you know you have a body that is not connected to another body; something with the remainder you said; connect everything into one law that solves everything for us"; PROVED and COMPUTED here)

**THE FRAME (the model owner's sentence, adopted as the frame of everything,
record 1967 through the Boss, 2026-09-25): "The click is the moment the
fraction becomes whole, at the level of the record and not at each Node
alone. The record gathers part after part. When the gathering completes
the share the remainder set, one whole quantum leaves. The click takes
out the whole, and the remainder stays behind at the Node." It adds no
rule: it is 9.17 (7) (f), this section and 9.33 to 9.35 in one sentence,
and 9.38 reads it on the body's shell. With it the owner withdrew his
old rule that a Node keeps no remainder (record 1966): a Node keeps its
remainder, 9.34 (A).**

**THE ONE LAW, AT A NODE, IN FIVE LINES.** (1) THE STATE: a Node holds,
per record, two levels and a remainder, and nothing else (record 155;
8.1). (2) THE STEP (the Inside): every interval the Node's level goes to
its six neighbours with the pair's weight and turns against its own past,
the remainder kept, 3 den a_next + r' = num S_6 - 3 den a_before + r
(8.1); the pair per Node is the clock, a mass a pair with a rest
rotation, light the pair [1, 1] (9.31 (14)). (3) THE SHARE, derived and
never stored: a record's form at a Node, e_i = D_i (now_i^2 + before_i^2)
- (1 / 3) now_i (**A** before)_i; its change per interval is the net flux
through the Node's six Links (the discrete Gauss law, 9.19 (3)); the
record's whole is I = sum over its Nodes of e_i, conserved. (4) THE CLICK:
a record ends at every Node at once at the first interval at which the
share of it gathered by one object reaches (2 u + 1) / (2 W) of its
whole; the gather is the Node's own share where the record stands and
the positive flux through the object's Ports where it passes (9.25 (12));
u is the record's remainder at its birth Node on the wheel W = 3 den /
gcd(num, 3 den) (9.19 (4)); the object's own record changes at the click
(a count; a birth if it emits). (5) THE BIRTH: at a body's click the
train is written on its Nodes (9.17 (6a)). Nothing else is law; every
detector, emitter, mirror, clock and body of the rows is Nodes under
these five lines with the pairs declared per region, and Born's rule,
Bell, the clocks, the fall in a well and the exact returns are their
theorems (9.25, 9.26, 9.29).

**THE OWNER'S TWO STATEMENTS ARE THEOREMS OF (4).** (a) THE SINGLE NODE
CLICKS: a record confined to one Node (the one-Node emitter [801, 700])
clicks by (4) with the Node's own share; the click is that Node's event.
(b) ALL THE NODES TOGETHER CLICK THE SAME CLICK (PROVED): for a standing
record the flux through every Link vanishes (the Wronskian of a mode,
9.17 (7) (a)), so by (3) the share at EVERY Node is constant in time,
e_i = D_i p_i^2 sin^2 omega; the gather over one Node is t e_c against
T = P e_c and over all the Nodes t I against P I, the same ratio t / P;
so the rung is reached at the same interval t = ceil((2 u + 1) P / (2 W))
whether the click is read at one Node, at some Nodes or at all of them:
ONE CLICK, READ ANYWHERE ON THE BODY. COMPUTED (the float law, a well
[800, 801] of side 32 on the chain [800, 809], the mode at 2^20, 400
intervals): the share at the centre Node, at an edge Node and at a Node
outside the well constant to 10^-13, the whole I constant to 10^-14; the
click interval at the centre Node and over all the Nodes identical at
every residue tried (u = 0, 600, 1201, 2402: t = 1, 24, 47, 94, the
period 93.53). THAT IS WHAT MAKES THE NODES ONE BODY: A BODY IS THE SET
OF NODES OF ONE STANDING RECORD, the Nodes that click together, and no
declaration. (c) NOT CONNECTED TO ANOTHER BODY: two standing records with
no Node in common are two bodies with two clicks, each at its own u; two
wells so near that the composed operator's mode lies on both are ONE
standing record on both and ONE click on all their Nodes, one body with
one mode (9.22 (7a) (v)); so the loader's "two bodies, two records" check
(the stored profile 0 at every Node of the other body, 9.31 (3)) is
exactly the click's own criterion, and not a rule beside it. A passing
record shares a body's Nodes while it crosses and is no part of the
body: its share there is not constant, and its click is the gather at
the object's boundary, (4). (d) THE REMAINDER: the one thing at a Node
beyond the two levels; it carries the phase below one unit, is kept
exactly (the step a bijection, 9.26 (3) (a)), makes the integer step
exact, and at a birth Node gives the born record its residue u, the
place of its click within the acquisition; where the remainder is 0 for
ever (the exact returns, 9.26 (4a)) every click falls at the first rung
and there is no chance (9.28 (2) (e)): the remainder is where chance
lives, and it lives at the Node.

**WHAT THE ONE LAW SOLVES, AND HOW IT SITS WITH WHAT IS WRITTEN.** The
Inside (2), the click (4), the body (b), two bodies (c), chance (d) and
the birth (5) are one statement at the Node; 9.18 ("one object, one
record, one rule") and 9.25 (12) (d) (the generic click in one line) are
this statement read at the object; (b) adds the theorem that a body's
click is the same at each of its Nodes, which is why the emitter's rung
may read one Node (9.17 (7) (e)) and the clock body's period may be read
at its centre (9.31 (13)); (c) adds that the body is the record's
support and the "two bodies" check the click's own. The cleanup of 9.30
(2) is the removal of everything the engine does beside these five
lines. Proposed for Highlights 5.4, at the owner's word: "The law is five
lines at a Node: two levels and a remainder; the split to the six
neighbours and the turn against the past by the pair; the share, derived;
the click, one record ending on all its Nodes at once at its drawn share,
the residue from the remainder at its birth Node; the birth, the train on
the body's Nodes. A body is the Nodes of one standing record, which click
together; two bodies share no Node; the remainder is where chance lives
(2026-09-25)".

### 9.33 The remainder and the click: what nature keeps whole (the model owner's word, 2026-09-25, in the mathematician's session: "think: mass and light should perhaps be coupled to the click, and the click is a kind of remainder in the Node, so they are coupled to the remainder in the Node; nature does not want a remainder, nature wants a click; so it tends to things without a remainder, to periodic things, by coupling everything to the click; the click is the amplitude; nature does not want a remainder in charge, so it couples charge to the click; connect everything now"; CHECKED: three theorems of the law as written, and one decision)

**(1) THE REMAINDER LIVES ONLY INSIDE A RECORD'S LIFE, AND LEAVES AS A CLICK
(PROVED from the law as written).** A record is born with the remainder 0
at every Node (the seed's and the train's write, 9.17 (6a), 9.19 (4e));
between its birth and its click its remainders move exactly with it (the
step a bijection, 9.26 (3) (a)); at its click its rows AND its remainders
are deleted at every Node at once (record 1888); and the one thing of them
that survives is the remainder at the birth Node at that interval, which
becomes the born record's residue u, the place of its click (9.19 (4)). So
the board never keeps a remainder beyond the life of the record that made
it: the remainder is turned into a click's place and erased. That is the
owner's sentence, "nature does not want a remainder, nature wants a click",
as the law stands; and mass and light are coupled to the click by the same
rule, the standing record by its own tick and the passing one by its
arrival (9.26 (1a), one law), each with its residue from the remainder at
its birth Node: "coupled to the remainder in the Node".

**(2) WHAT IS WHOLE MOVES ONLY AT THE CLICK; WHAT MOVES AT THE STEP CARRIES
THE REMAINDER (PROVED).** The levels move every interval by the division
with the remainder kept (8.1). The quantum, the content, the labels and
every conserved integer of the law (a charge, if a family declares one;
the momentum of the exchange hypothesis, 9.27 (D)) move at the click alone,
in whole units, with no division and no remainder (9.17 (7) (c), "the
quantum is counted, not weighed"; the click line's handover, 9.18 (4)).
That is why charge has no remainder: it is coupled to the click, as the
owner says, and to nothing that moves at the step. "The click is the
amplitude" holds in this form: the click carries the record's whole, its
form and its one quantum, never a part; the amplitude itself is a
convention of the write and the click is scale-free.

**(3) PERIODICITY TO THE BIT COMES FROM THE CLICK, NOT FROM THE INSIDE
(PROVED; HISTORY since 9.43: the reseed is retired, a body's own record is
never rewritten and is one rotation carried for ever).** The Inside alone never returns a shape to the bit (Niven, 9.26
(4) (a)) except the exact modes of 9.26 (4a). A body that clicks does: at
each click its excited record is reseeded from the stock as the same
integers with the remainder 0 (9.17 (4)), so every cycle starts bit for bit
where the last did and differs only in its length, (2 u + 1) P / (2 W),
and in light's back-action within it. So "nature tends to periodic things
by coupling everything to the click" is the law's own: a body's exact
periodicity is the click's reseed; a body with no click drifts within the
rounding for ever; the clock rows read this (9.31 (13)). A body whose
stock is spent stands and clicks no more: the model's ground state, the
stability the atom's rule of record 881 was to give, is here the stock,
one integer, and no rule beside the five lines of 9.32.

**(4) THE ONE DECISION, WHERE THE OWNER'S READING GOES BEYOND THE LAW: THE
EXACT RECORD.** The law as written makes a record with the residue u = 0
click at the FIRST rung, at once (9.28 (2) (e)): on an exact board (the
remainder 0 for ever, the periods 3, 4, 6) every record is born with u =
0 and the three-cube universe clicks once and empties itself (9.26 (4a)
(i)). The owner's reading, "nature tends to what has no remainder", would
make the exact record the one that does NOT click: what has no remainder
has nothing to release, and stays periodic for ever. The two agree on
every measured row (no real clock is exact, by Niven) and differ on the
exact test worlds alone. It is a decision of the owner and not a theorem,
stated under its own identity until his word: THE REMAINDER RULE, "a
record clicks only from a remainder: a residue 0 read from an exact
record is no rung, and the record stands", the key `hypotheses:
{"remainder_rule": true}`, off by default; its one test the three-cube
universe, eternal under the rule and emptied at once without it; the
three tests: generic (no family name), vector (a comparison on the
residue, verb (D)), local (the birth Node's own remainder); no pin of the
eighteen moves either way.

**(5) THE ONE SENTENCE.** The remainder is where chance lives and it lives
at the Node (9.32); the click is where the remainder leaves, carrying the
whole and the place of the next click; what is whole moves at the click
and what moves at the step carries the remainder; a body is periodic to
the bit by its clicks and drifts without them. Nothing of the five lines
of 9.32 changes; (4) waits on the owner. (Revised by 9.34, ADOPTED by the model owner, record 1962: the remainder is the Node's, kept through the click and the reseed; (1) and (3) above are restated there.)

### 9.34 The remainder is the Node's; the families coupled by the click alone (the model owner's word, 2026-09-25, in the mathematician's session: "if you think it explains everything, then yes; but note that in a single Node you have to couple the families, you couple them to the click; and there is a remainder in the Node, and by it the click is measured; and with no remainder the click is only the speed of light passing from Node to Node"; CHECKED and COMPUTED; three decisions named)

**(1) WHAT THE REMAINDER RULE EXPLAINS, HONESTLY.** The rule of 9.33 (4)
by itself explains one thing: an exact record (the remainder 0 for ever)
does not click but only turns and splits, one Link per interval, the
owner's "at the speed of light from Node to Node"; the exact worlds are
eternal instead of emptying at once. It moves no measured number. What
DOES reach further is the owner's other sentence, "there is a remainder in
the Node, and by it the click is measured", once it is taken literally,
below.

**(2) THE REMAINDER IS THE NODE'S (COMPUTED; the correction of 9.33 (1) and
(3)).** The law as written owns the remainder by the RECORD: born 0,
deleted at the click, reset to 0 at an emitter's reseed. Taken so, an
emitter reseeded identically with no coupling to light births ONE residue
for ever (Nature24's finding, 9.19 (4e) (i)), and the spread of the
residues, on which Born's rule rests (9.25 (3)), had to come from light's
back-action on the body (the coupling g of record 1414). COMPUTED on the
INTEGER law, an emitter [800, 801] of side 32 on the chain [800, 809] (W
= 2403), the mode at 2^20, no coupling at all, 600 cycles, the residue
read after the first advance and the click by the standing record's rung:
with the remainder RESET at every reseed, one residue (337) in 600 cycles
and a mean cycle of 14 intervals, not P / 2; with the remainder KEPT AT
THE NODES through the click and the reseed (the levels rewritten, the
remainders left where they are), 532 distinct residues in 600 cycles,
equidistributed over the wheel (chi-square 26.1 on 20 bins, the 95 percent
bound 30.1), and the mean cycle 46.8 = P / 2 exactly as 9.17 (7) (b)
says. So THE NODE'S REMAINDER ALONE SPREADS THE RESIDUES, deterministically
and locally, with no coupling and no draw: the remainder is where chance
lives, and it lives AT THE NODE, as the owner said, not in the record.
THE FORM: at a body's reseed the levels are rewritten as the profile and
the remainders at the body's Nodes are KEPT; a record born elsewhere is
still written with the remainder 0 and its remainders end with it (there
they carry nothing across). The step stays the bijection of (levels,
remainders) (9.26 (3) (a)); the click deletes the levels; the form's
accounting per record moves by less than a unit per Node (8.2). Taken to
the letter, "one remainder per Node per family" shared by every record of
the family at the Node, stepping in their declared order, is the same idea
with one integer fewer per record and a coupling of records below one
unit; the body's form above is the least change and is what was computed.
The three tests: generic (one integer per Node, no family name), vector
(verb (D) with the remainder kept, as now), local (the Node's own).

**(3) THE FAMILIES ARE COUPLED BY THE CLICK ALONE.** With (2) the bilinear
coupling of 8.5 (record 1414, "a_m += g a_l") has no role left in the law:
the index of a medium is the pair's (9.31 (8)); the residues' spread is
the Node's remainder ((2)); the emitter's transparency to its born family
is then exact (no coupling, no index at its Nodes, 9.22 (7a) (iv) empty);
the load condition of 9.17 (7) (c) has nothing to bound; the response
records, the invariant J and the kind branches of the coupling (9.30 (3))
go with it. What couples mass and light is the CLICK, at a Node, and it
hands over whole integers only: the quantum, the content, the labels, the
residue (the place of the next click, read from the Node's remainder at
the birth Node), and the momentum if the exchange hypothesis is adopted
(9.27 (D)); the click is measured by the Node's remainder, as the owner
says. The Inside is then one operator per family with no cross term at
all, and 9.32's five lines lose nothing.

**(4) NO REMAINDER, NO CLICK.** An exact record, the remainder 0 at every
Node for ever, has no residue to draw and does not click: it splits and
turns at one Link per interval, the owner's "the click is only the speed
of light from Node to Node"; every other record clicks from its remainder
(9.33 (4), the remainder rule, now with (2) as its reason: the click IS
the remainder leaving the Node).

**(5) THE THREE DECISIONS FOR THE MODEL OWNER, each a law change stated
for his word under record 1940 (the algebra: this section; the code:
Nature24 after his word; the Boss records):** (A) THE REMAINDER IS THE
NODE'S: kept at a body's Nodes through its clicks and reseeds ((2)); it
replaces "reset to 0 at the reseed" and revises 9.33 (1) and (3) (a body
is periodic to the bit in its LEVELS at each reseed, its remainders its
memory). (B) THE COUPLING IS THE CLICK ALONE: the bilinear term of record
1414 retired from the law, the click's handover the one exchange ((3)).
(C) THE REMAINDER RULE: an exact record never clicks ((4), 9.33 (4)). What
moves if he says yes to all three: no measured pin (the pins are binomial
about the ladder's shares, which need only the residues' spread, given by
(A)); the exact worlds become eternal (C); the engine loses the coupling,
the response records, J, the transparency and the back-action checks (B)
and keeps the remainders at a body's Nodes (A). The mathematician's
recommendation: yes to all three; they are one thing, the owner's "the
click is a kind of remainder in the Node".

### 9.35 The clock's slowing as law: the Node clock, the form that passes the three tests (the model owner's decisions of 2026-09-25 through the Boss: record 1948, "a clock should slow toward a mass; mass slows a clock; the Node multiplies itself, which causes a clock's slowing"; record 1949, "THE CLOCK'S SLOWING IS LAW: the pace at a Node stretched by what is at the Node, generic for every family, light included; it is not exactly gravity, it is a clock's slowing"; record 1951, "in a single Node, its internal clock is the click"; record 1954, the coupling at a Node is to the click; record 1955, "close everything by the law of the click and the remainder, at the Node, at the body and at the whole"); with the answers to records 1950, 1952 and 1953 and Nature24's findings; PROVED and COMPUTED)

**(1) THE DIVISION'S CARRY IS NOT A CLOCK (the Boss's computation of
record 1955 CONFIRMED, with its reason).** The remainder r at a Node is
equidistributed on [0, wall) whatever the levels there (9.19 (4)'s
computation), so a carry (the floor raised by the carried remainder)
happens with the probability (1 - 1 / W) / 2 per occupied Node per interval, W the wheel (the residue classes, 3 den / gcd(num, 3 den); Nature24's correction of the Boss's wall, COMPUTED on the engine: 0.3229 inside a well [800, 800], whose wheel is 3, against 0.49 in its vacuum [800, 809], whose wheel is 2427), independent of the content, the mass, the rotation, the momentum and the amplitude: the Boss's 0.329 for light (W = 3), 0.499 for [800, 809] (W = 2427), 0.477 for the holder (W = 24) are this number. The carry is the rounding's own statistics, not a clock of what
is there; it is not a click in the sense of 9.17 (7) (f) and needs no
name; the Inside stays exactly reversible with it. The link between the
remainder and the click that the owner named is 9.32 to 9.34: the
click's place is the remainder at the birth Node (the residue), the
remainder kept at the Node spreads the residues with no coupling, the
click carries whole numbers and leaves the remainder behind, and a body
is the Nodes that click together.

**(2) THE NODE CLOCK, THE FORM THAT PASSES THE THREE TESTS (PROVED and
COMPUTED).** At every Node i a clock pair (e_i, f_i), e_i <= f_i, THE
SAME FOR EVERY FAMILY, enters the rule as a positive self term:

    3 den f_i a_next + r' = e_i num S_6 + 6 den (f_i - e_i) a_now - 3 den f_i a_before + r,    0 <= r' < 3 den f_i;

e_i = f_i is the plain rule of 8.1, e_i -> 0 a frozen Node. On a
character, cos omega' = 1 - (e / f)(1 - cos omega): the whole dispersion
of every family is slowed alike (a mass's rest rotation, light's pace,
a body's bound mode, all by the same factor), light keeps cos omega' = 1
at **k** = 0 (no mass gap, unlike a lowered pair, 9.29 (3)), and cos
omega' >= 1 - 2 e / f >= -1 (no instability: the positive self term is
the mirror of the compensated form 8.1 withdrew, whose self term was
negative). THE CONSERVED FORM: the leapfrog invariant with the weights
D_i f_i / e_i, I' = sum over i of (D_i f_i / e_i) (now_i^2 + before_i^2)
- (D_i f_i / e_i) now_i ((2 - 2 e_i / f_i) before_i + (e_i / f_i)
(num / (3 den)) S_6(before)_i): COMPUTED exact to 10^-16 over 300 steps
on a random state with a random clock field. THE BIJECTION: the step
has the same shape with the wall 3 den f_i, so the Inside stays
reversible bit for bit. THE ROTATION: a rest mode [800, 809] at e / f =
0.8 turns with 2 cos omega' = 1.982200 against the predicted 1.982200
(the period 47.06 intervals for 42.08), at 0.5 with 1.988875 (59.54
intervals). THE BENDING: light [1, 1] at K = pi / 2 and matter [800,
809] at K = 0.5 passing 45 Nodes beside a Gaussian slow region (e / f =
0.7 at its centre, width 30) bend TOWARD it, 30.0 and 24.4 Nodes over
500 intervals: a slow region is a lens for every family. THE THREE
TESTS: generic (one pair per Node, no family name), vector (the same
three verbs with integer entries, no root, no float), local (the Node's
own pair). This is the shift of the Node's rotation for all families that 9.29 (3) (b) said the family's pair cannot express: the pair cannot, the Node clock can. THE SHARE AND THE CURRENT UNDER THE NODE CLOCK (Nature24's question, PROVED and COMPUTED): with (e, f) = (Gamma, Gamma + M_i) and in the integer units 3 num Gamma e_i, the Node's own share is E_i = 3 den (Gamma + M_i)(now_i^2 + before_i^2) - num Gamma now_i (**A** before)_i - 6 den M_i now_i before_i (**A** the six reads with the self reads of a folded axis), the record's norm T = sum over its Nodes of E_i, and its change per interval is the sum over the Node's six Links of num Gamma (now_i before_j - before_i now_j) read on the levels before the step: THE LINK'S CURRENT IS THE SAME BILINEAR FORM AS WITHOUT THE CLOCK, only the Node's own term changes; the one-way flux per Port for the click's tally is num Gamma max(now_i before_j - before_i now_j, 0) in these units (the identity computed exact to 5 x 10^-15 on a random clock field, the sum of E_i the invariant above).

**(3) WHAT IS AT THE NODE: THE CONTENT, CHANGING ONLY AT EVENTS (since
record 1982 the content is the level of the family of clicks held at the
body's Nodes, and the clock its amplitude: 9.45, the one statement) (the
Boss's question (a) of record 1949, answered yes).** The Node's clock is
set by the content at the Node,

    (e_i, f_i) = (Gamma, Gamma + M_i),

M_i the content (the quanta: the stock and the held quanta) of the bodies
whose Nodes include Node i, 0 in the vacuum, and Gamma one declared
integer of the world (the old wall's gamma = 1 / Gamma; the law's one
constant beside the pairs, required in every world file, refused absent).
M_i changes only at births and clicks, the law's integer events, so
BETWEEN EVENTS THE STEP IS LINEAR, CONSERVATIVE AND REVERSIBLE EXACTLY,
and at an event the clock changes with the content, where the click
already breaks the bijection. AT A MASS: every clock at the mass's own
Nodes, of every family, light included, runs slow by e / f = Gamma /
(Gamma + M), and light passing through the mass's Nodes is delayed and
bent into it: the owner's law. AROUND A MASS: only where the body's Nodes
are; a slowing in the vacuum around a body needs a field kept at the
Nodes, the pair-field hypothesis of 9.29 (4) (a) rewritten for the Node
clock (the content spread to the neighbourhood by a Poisson law), which
fails the vector test and stays outside the law until his word. LIGHT
WITH LIGHT: if M_i also counts the quanta of every record present at
the Node (presence a nonzero level), records slow each other where they
overlap, the same rule; but presence changes inside the Inside (the
tails), so exactness between events is lost there: a second decision,
not recommended before the first is run. THE NUMBER (the Boss's (d)):
Gamma is declared per world like the pairs; the eighteen declare Gamma
= 10^6: the clock bodies (M = 64) and the wells (M = 1) slow by 6 x
10^-5 and 10^-6, the emitters by their stock (the two slits' 4096: 0.4
percent of the emitter's own cadence, which no pin reads), so NO PIN OF
THE EIGHTEEN MOVES beyond its band. THE SIXTH COMPUTED ROW (gravity):
the algebra now carries a clock's slowing at a mass, universal, of size
M / (Gamma + M), and light's delay and bending into the mass: THE FORM
IS NATURE'S AND THE NUMBER IS DECLARED (Gamma, as G is measured in
nature); 9.22 (8a)'s "no clock runs slow near a mass" and 9.27 (A)'s
replacement of gravity by the universality of the tick are REVISED
here: the universality of the tick stays a theorem, and beside it the
Node clock is the slowing. The pins' file carries Gamma with the pairs.

**(4) THE OWNER'S TWO FINDINGS, PLAINLY (record 1948).** (i) WHEN A CLICK
IS REVERSIBLE: the Inside is reversible bit for bit (9.26 (3) (a)); a
click is reversible only if the detector keeps the record's whole shape,
the register that his decision of record 1888 deletes; as the law
stands no click is reversible, the line keeps the count, the interval
and the residue, and the whole has no period (9.26 (3) (b), (c)). (ii)
THE REMAINDER AND THE CLICK: the click's place is the remainder at the
birth Node; the remainder kept at the Node spreads the residues with no
coupling (9.34, computed: 532 residues in 600 cycles); the click carries
whole numbers and leaves the remainder behind (9.33); a body is the
Nodes that click together (9.32).

**(5) THE TWO ITEMS (record 1948):** the exact-return theorem into
Highlights 5.4 with the exact worlds as property tests: YES. The
coherence table's differences: YES to all, the gravity row no longer
held but REPLACED by (3).

**(6) EVERY WRITE COMPLETE (record 1952).** Per Node per family: the
value now, the value before, the pair (declared per region) and the
division's remainder; per Node for all families: the clock pair (e, f)
from the content; nothing else. At a born Node the born family's
remainder is the Node's (kept, 9.34 (A)), or 0 where the family had no
record there; either keeps the Inside reversible between clicks. A birth
touches only the born family's levels at the body's Nodes and the body's
content (M - 1, one count of the Node clock at its Nodes). AGENTS.md's
"nothing kept at a Node beyond the events there (no register, remainder
or draw)" and the one algebra read the same as: nothing at a Node beyond
the law's own numbers, the two levels and the division's remainder of
each record there, the declared pairs and the clock from the content; no
register beside them and no draw; the remainder is the law's own, and
record 155's "no remainder" was the ray law's rows, which had no
division.

**(7) THE PER-NODE STATE (record 1955 (2)).** Per record: the two levels
and the remainder, over the record's Nodes; per family per Node: the
pair; per Node: the clock. The remainder of a sum is not the sum of the
remainders, so the remainder is the record's, as the engine keeps it;
9.34 (A)'s "the Node's remainder" is the body's own record's remainder
kept at its Nodes through its reseed, per record.

**(8) THE LADDER, ONCE (record 1953 (A)).** THE NODE: two levels and a
remainder per record, the pair per family, the clock from its content.
THE BODY: the Nodes of one standing record, which click together (9.32);
its clock its rung; its content its quanta. A BODY IN A BODY: a record
standing on Nodes inside another body's Nodes: its clock slowed by the
outer body's content through the Node clock ((3)), its coupling to the
outer body the click alone (9.34): a clock in a mass, an atom in a
lattice. THE EXPERIMENT: bodies placed in the GameBoard, the faces its
border (9.27 (B)), every write at the load and at every birth writing
all families' values at the Nodes touched ((6)), every reading a click.
Each rung is written by one act, content into Nodes, and read by one
act, the click.

**(9) THE BRICKS (record 1953 (B)).** The cube of side 3 is the least
detector, whole and never cut (the extrusion rule, 9.22 (8)), and the
least universe that turns exactly (9.28); but an EXACT brick holds only
the exact modes (an integer eigenvector with the multiplier in {-1, 0,
1}, the remainder 0 for ever), which have no chance: an experiment built
of exact bricks alone would put every click at the first rung and show
no Born's rule, no fringe statistics and no Bell (9.28 (2) (e)). THE
SMALLEST DEPARTURE THAT BRINGS CHANCE BACK IS ONE RICH NODE: the
emitter's birth Node with a pair whose wheel carries at least 500
remainder values (9.19 (4a)), whose remainder draws every residue;
everything else may be whole cubes. The eighteen, in one line each: the
detectors are cubes of side 3 in every row; the emitters bodies of 32
Nodes along **K** (a train's length) with one rich Node; the wells sides
12 to 40 (a bound mode needs its side, 8.3); the mirrors, splitters and
media slabs of depth 1 to 4; the boards as 9.22 (8)'s table; no row is
built of exact bricks, and the exact bricks are the property tests.

**(10) THE BORN RECORD IS THE BODY'S OWN MODE (record 1950, the owner:
"the born train is not generic enough; a world is content written into
the Nodes at once"; the Boss's proposal CONFIRMED and adopted).** A birth
writes, at both levels on the body's Nodes, the born family's LOWEST
MODE ON THE BODY'S NODES WITH THE ZERO ROW BEYOND (the generator's
iteration on those Nodes alone; a half sine along each extent; uniform
across an extent the body spans on a periodic axis, Nature24's line)
times the character of its momentum **K**: no Hann window, no tapers, no
period count chosen for the birth; the length along **K** is the body's
extent. COMPUTED, the generator's flux check of 9.17 (6a) on the chain
(light, K = pi / 2, 32 Nodes, the one-way flux 40 Links ahead over the
passage against the norm): the body's mode 0.9997, the Hann window with
the tapers 0.9987, the flat pulse 0.9818: the body's own mode passes
9.25 (11) better than the window. The pins: the passage pins (the mean
click interval, the head's path + X / 2 + 2) do not move; the fringe
pins are recomputed by the generator on the mode envelope before their
files (the band is narrower; the visibilities are expected within their
bands). 9.17 (6a)'s window and tapers are HISTORY; its load checks (the form, the flux sign along **K**, the hash) and the born clock stand. TWO READINGS OF "THE BODY'S OWN MODE", ONE CHOSEN (Nature24's measurement on the engine, the light clock's A [800, 801] of [32, 3, 3] on [760, 3, 3]): the EMITTER'S OWN massive mode has tails beyond the body (11 percent of its magnitude outside A's Nodes at 2^20); clipped to the body it fails the check (1.0047, a hard edge), written over its tails (72 Nodes) it passes (1.00002), but then the birth writes outside the body's Nodes and the born record's shape depends on a foreign family's well. THE FORM ADOPTED IS THE OTHER: the BORN FAMILY'S lowest mode on the body's Nodes with the zero row beyond (the half sine of the flux check above, which vanishes at the body's edge), written on the body's Nodes alone, as long as the body's extent along **K**: the passage's mean click interval stays the head's path + X / 2 + 2 and its rms as before (9.25 (11) (d)).

**(11) THE HOLDER EMITTERS' PAIR (Nature24's finding of 07:20Z on his
clock, CONFIRMED by 9.29 (3) (b)):** a pair above 1 over 32 Nodes runs
away ([801, 700] on [7, 8] reads 2 cos omega = 2.285 over 32 Nodes; a
pair above 1 is bounded only on a tiny region); the holder's emitting
bodies of side 32 are wells BELOW 1 and near it, [699, 700] on [7, 8]
(2 cos omega = 1.994, above the band top 1.75, bound; W = 700, rich);
the rows' [1201, 700] are corrected to [699, 700] at this head; the
one-Node [801, 700] stays. With 9.34 (B) the holder emitter's
transparency to its born family is exact.

**(12) THE THREE LEVELS IN ONE LINE EACH (record 1955 (3)).** The Node:
its records' two levels and remainders, its families' pairs, its clock
from its content; it splits and turns, and it clicks when a record's
share at it reaches the record's drawn share. The body: the Nodes of one
standing record, which click together, its clock its rung slowed by the
content at its Nodes, its coupling to everything the click. The whole:
the GameBoard with its faces, exact and reversible between clicks,
whose only events are the clicks and the births, and whose remainders
live at the Nodes.

### 9.36 The Node's law with its couplings, closed in one circle (the model owner's word, 2026-09-25, in the mathematician's session: "yes" to the remainder rule of 9.33 (4) and 9.34 (C), "a click when there is a remainder"; and "it has to enter the Node's law and the Node's couplings: how do we couple the mass and the click at the Node?")

**THE STATE AT A NODE.** Per record of each family: two levels and a
remainder, kept at the Node (9.34 (A)). Per family: the pair [num, den],
which is the family's mass (its rest rotation cos omega_0 = num / den,
8.1). Per Node: the CONTENT M, the quanta of the body whose Node it is
(0 in the vacuum), and from it the NODE CLOCK (e, f) = (Gamma, Gamma +
M), one for every family (9.35 (3)).

**THE STEP (the Inside),** for every record of every family at the Node:
3 den f a_next + r' = e num S_6 + 6 den (f - e) a_now - 3 den f
a_before + r, the remainder kept at the Node. The mass enters here
twice: the family's pair (its own rest rotation) and the Node's content
through the clock (which slows every family alike, light included). No
continuous term couples one family to another (9.34 (B)).

**THE GATHER.** Each object sums at its Ports the positive current of
each record, num Gamma (now_i before_j - before_i now_j), and a standing
record its own share at the Node (9.32 (4), 9.35 (2)).

**THE CLICK, WHICH IS THE WHOLE COUPLING.** A record clicks when the
share of it gathered by one object reaches (2 u + 1) / (2 W) of its
whole, u the remainder at its birth Node; A RECORD WITH NO REMAINDER
NEVER CLICKS (the remainder rule, ADOPTED by the model owner,
2026-09-25: it splits and turns at one Link per interval and stays). At
the click, in whole numbers only: the record ends on all its Nodes (1888);
THE RECEIVING BODY'S CONTENT M RISES BY ONE, and at a birth the emitter's
falls by one: THIS IS THE COUPLING OF MASS TO THE CLICK. The content
changes the Node clock at the body's Nodes, which slows the rotation of
its own mode and of every record passing through it; a quantum of light
becomes content, content becomes clock, clock becomes rotation. A body
heavier at its Nodes turns slower and so CLICKS slower (its rung T = P
e_c grows with its period). The labels, a charge and the momentum (if
the exchange hypothesis is adopted, 9.27 (D)) pass in the same click,
whole. The born record starts from the remainder at its birth Node,
which sets the place of its own click.

**THE CIRCLE AT THE NODE.** The remainder gives the click its place; the
click moves the content; the content sets the clock of every family at
the Node; the clock sets the rotation; the rotation leaves the
remainder. Mass and light are coupled by nothing else: the pair gives
each family its pace and its rest mass, the click moves the whole
numbers between them, and the Node clock is how what is at a Node slows
what passes through it. 9.32's five lines, 9.34's three decisions and
9.35's Node clock are this one circle; nothing is kept at a Node beyond
the law's own numbers.

### 9.37 One gives the click, one receives it: the birth is the click read at its giving end, and no wave is written (the model owner's words of 2026-09-25 through the Boss: record 1963, "we do not write a wave; everything happens by itself in the Nodes; the opposite of a click is an emitter"; record 1964, "a click is a kind of emission, and a birth is what receives the click; one gives the click and one receives the click"; the Boss's five questions; PROVED)

**(1) A CHANGE OF THE BODY'S INTEGERS ALONE SHEDS NOTHING OF THE BORN
FAMILY (PROVED, one line).** The step is linear and separate per family
(9.36: no term couples one family's rows to another's). The born family's
rows at an emitter's Nodes are 0 before its click; a change of the body's
content M, of its Node clock (Gamma, Gamma + M) or of its pair changes
the OPERATOR at those Nodes, and the operator maps zero rows to zero
rows. So light does not leave a body by the step alone: no light exists
to leave. What such a change does shed is of the BODY'S OWN family: its
standing mode is no longer an exact mode of the changed operator and
sheds the difference as a travelling record of the massive family, in
every direction, of the order of the change squared: for M -> M - 1 at
Gamma = 10^6 about 10^-12 of the body's form, nothing; for a pair moved
by one unit of its denominator about (the mode's overlap defect)^2, small
and of the wrong family. The three tests do not help here: the obstacle
is linearity, which the owner's own law keeps.

**(2) ONE QUANTUM PER CLICK: THE GIVING END SETS THE BORN FAMILY'S LEVELS
ON THE BODY'S NODES, AT THE CLICK, AND THAT IS NOT A WRITTEN WAVE.** The
click at the receiving end deletes a record's two levels on all its Nodes
at once and raises the detector's count (record 1888, 9.32 (4)); its
mirror at the giving end SETS a record's two levels on the body's Nodes
at once, the body's own mode of the born family times the character of
its momentum (9.35 (10)), and lowers the stock. Nothing is written but
the state of the body's own Nodes at the instant of its click, exactly
as the deletion changes nothing but the state of the record's Nodes;
the WAVE is not written: from that instant the record moves by the step
alone, Node to Node, one Link per interval, as the owner says. One
click, one quantum out; the record ends at one detector's click and at
no other (9.25 (12)): one detector click at most, the quantum counted
once. The owner's two words are one statement: the click is one rule
read at its two ends, the levels set and the stock down at the giver,
the levels cleared and the count up at the taker, the sign of the
body's change the only difference, and between the two the Nodes carry
the quantum by the step alone, two events at two times. "BIRTH" LEAVES
THE LAW'S VOCABULARY AS A SEPARATE ACT: it is the click at its giving
end (9.13, the emitter as the transpose of the click, was this sentence
before its time).

**(3) THE THREE TESTS:** generic (one rule, the click, read at two ends;
the born family's mode on the body's Nodes with no family name); vector
(the deletion and the setting of two levels on a declared set of Nodes,
the same verb as the load's write, no root, no float); local (the body's
own Nodes at the giving end, the record's own Nodes at the taking end;
the one non-local act per record, its Nodes at once, as before).

**(4) THE EMITTING ROWS AND THEIR PINS:** unchanged. The birth of record
1962 (the body's own mode times the character, set on the body's Nodes
at its click) is this giving end already; the pins of 9.22 (8) stand as
recomputed on the mode envelope.

**(5) IF NOTHING MAY BE SET AT THE GIVING END:** there is no smaller change
that lets the Nodes emit light by themselves. The only way the step alone
makes rows of one family from another's is a source term between them,
which is the retired coupling of 8.5 (record 1962): it emits
continuously and unquantised at the body's own rotation, one quantum per
click lost. So the law keeps the click's two ends and drops the word
"birth"; the light on the board is never written as a wave, only set on
a body's Nodes as the state of its Nodes at its click, and then left to
the step.

### 9.38 The surface rule: every click is read at the body's outer shell, at both ends (the model owner's word of 2026-09-25 in the mathematician's session: "there are still bugs in the code, in the births; we need one generic thing that solves everything with the remainder and the click, when the remainder is and how the click is measured, with no remainder or with a remainder; connect it all into one generic law in the engine; maybe on the boundary of the body we are looking for something: the whole outer boundary of our body gives the click"; PROVED and COMPUTED)

**(1) THE SHELL.** A body is the Nodes of one standing record (9.32
(b)). Its OUTER SHELL is the set of its Nodes that have a Port: a Link to
a Node that is no Node of the body (9.19 (3)); the shell's Ports are the
body's SURFACE. On a chain the shell is two Nodes; a cube of side n has
n^3 - (n - 2)^3 shell Nodes (side 3: 26 of 27; side 32: 5768 of 32768);
on the extruded boards [N, 3, 3] of 9.22 (8) every Node is a shell Node.
A body of one Node is its own shell, its surface its six Ports. THE
INTERIOR IS NEVER READ: the owner's sentence, "the whole outer boundary
of the body gives the click", is the rule below, and it is one rule at a
Node and at a body.

**(2) THE RULE: ONE GATHER, ONE THRESHOLD, ONE LADDER, AT BOTH ENDS.**
Every interval the body's shell gathers, per record: THROUGH ITS PORTS,
the positive inward current of a record that passes, num Gamma (now_i
before_j - before_i now_j) read on the levels before the step (9.35 (2),
9.25 (2)); AT ITS NODES, the share e_i (9.32 (3)) of the body's OWN
record, the record whose Nodes they are (its tick, 9.17 (7) (f)). The
record's running total C is compared with theta = (2 u + 1) T / (2 W), T
the whole the shell gathers in one acquisition: a passing record's whole
I (what crosses the surface once), the own record's P times the shell's
share (one period of its rotation). THE WALK over the shell Nodes in
their declared order (the box's x-major order, the loader's one
convention, 9.17 (6a)) lands the click at one shell Node, the Node whose
segment of that interval's gather holds theta - C(t - 1); THE RESIDUE OF
WHAT THE CLICK BIRTHS IS THE REMAINDER AT THAT NODE, on its wheel W
(9.19 (4)); no centre Node, which a body of even side does not have. The
two ends are this one landing read with the sign of the body's change
(9.37 (2)): a passing record that lands is cleared on all its Nodes and
the body's content rises by one; the body's own record that lands sets
the born family's levels on the body's Nodes with the character of the
declared **K** and lowers the stock; the body's own levels, phase and
remainders are LEFT AS THEY ARE (no reseed, 9.43; the rewrite as the
profile is history). Nothing else is read
and nothing else is written; the record then moves by the step alone
(9.37).

**(3) PROVED.** (a) THE TICK IS THE SAME AT THE SHELL, AT ONE NODE AND
AT ALL THE NODES: for a standing record the current through every Link
vanishes (the Wronskian, 9.17 (7) (a)), so e_i is constant at every Node
and the ratio C / T = t / P is the same over any set of its Nodes (9.32
(b)); the shell is such a set. (b) THE BODY'S GAUSS LAW: E_S(t) - E_S(t
- 1) = the sum over the body's surface Ports of the current into it,
because the per-Node identity of 9.19 (3) summed over the body's Nodes
cancels every interior Link pairwise (G_ij = - G_ji), and only the
surface remains; so what the shell gathers of a passing record IS the
change of the body's share of it: the surface reads the body's whole,
never less and never twice (the Port rule of 9.25 (2), a Link inside the
body no Port, is this cancellation). (c) THE ONE RULE AT A NODE AND AT A
BODY: a one-Node body's shell is its Node and its six Ports, so (2) at
one Node is 9.32 (a) and at a body 9.32 (b), one sentence.

**(4) COMPUTED on the integer law with the remainders kept at the Nodes
and no coupling** (scratchpad surface_click.py and surface_tick.py; the
well [800, 801] of side 32 on the chain [800, 809], W = 2403, the mode
at 2^20, the period 93.53, 600 cycles): the tick read at the shell (the
two outermost Nodes of the well) fires at the same interval as the tick
read over all the Nodes in EVERY one of the 600 cycles; the centre
Node's reading differs from all the Nodes' in 2 cycles by one interval
(the rounding at one Node; the shell's share per interval varies by 3.8
x 10^-4 of itself and the shell reads two Nodes); the born residue read
at the shell Node where the walk lands: 531 distinct residues in 600
cycles, the chi-square over 20 bins of the wheel 15.6 (the centre
Node's 26.1; the 95 percent bound 30.1); the mean cycle 46.8 = P / 2;
the walk lands 293 times on the first shell Node and 307 on the last.
The body's Gauss law on the integer law, a travelling record of 32
Nodes crossing the well over 260 intervals: the defect of E_S(t) - E_S(t
- 1) against the surface currents is at most 8.8 x 10^-7 of the
record's whole per interval, the rounding of the levels alone (the
float law's identity is exact, node_clock_flux.py, 9.35 (2)).

**(5) WHEN THE REMAINDER, AND WHEN NO REMAINDER (the owner's question,
answered once more in the surface's words).** The click is MEASURED BY
the remainder: u, the remainder at the shell Node where the walk lands,
sets the place of the next click, (2 u + 1) / (2 W) of the whole; the
click HAPPENS when there is a remainder to read. A record with no
remainder (an exact record, 9.26 (4a); the periods 3, 4 and 6) has
nothing to draw: it crosses the surface and is not gathered, one Link
per interval, Node to Node (9.34 (4), the remainder rule, adopted). So
the two sentences the owner keeps asking about are one: the remainder
is the measure, and a record clicks when it has one.

**(6) WHAT THE ENGINE CARRIES BESIDE THIS RULE (read at Nature24's head
b8faee40 on emitter-click; the list for his order after the owner's
word; the owner's "bugs in the births").** (a) Two click readings
instead of one: the emitter's tick at the CENTRE Node (`_excitation_rung`
over `centre_mask` and `form_share`) and the detectors' ladder over the
Ports (`_ladder_click`); under (2) one ladder over the shell at both
ends. (b) The residue read at the centre Node (`residue_of`) instead of
at the click's Node. (c) The coupling still in the step: `_receive`,
`_source`, `_coupled_term`, the response records and the `extra` of the
block's emitted light, retired by record 1962 (9.34 (B)). (d) The
remainder reset at every reseed (a fresh record with zero remainders at
each `_excite`) against 9.34 (A); with it the emitter births one residue
for ever (9.34 (2)). (e) The cavity's zeroing of the levels and the
remainders outside the body's mask, an act beside the law. (f) No Node
clock: no Gamma and no content in the step (9.35 (3)). (a), (b), (d)
and (e) are the births' bugs in the owner's sense: the emitter reads an
interior Node the rule does not name, resets what the Node keeps, and
zeroes what the step made; (c) and (f) are the two law changes of 1962
not yet built.

**(7) THE THREE TESTS AND THE ROWS.** Generic: the shell is defined by
the Ports alone (a Node with a Link to a non-Node), no family name, no
shape counted beyond "has a Port" (record 1934). Vector: sums over
declared Nodes and Ports, one comparison, the division with the
remainder kept, no root, no float. Local: a shell Node reads its own
Ports and its own share; the two record integers C and theta travel
with the record (9.25 (2)). The rows and their pins: UNCHANGED (the
tick's interval the same by (3) (a) and (4); the detectors' Nodes were
already read at their Ports; the born residues' spread the same
statistics by (4)); the host cost of a click falls from the body's Nodes
to its shell (side 32: 5768 Nodes of 32768).

**(8) THE BOSS'S FACE CONDITION AND HIS CURRENT (record 1965, answered).**
(a) "A taker clicks when what entered through its faces reaches the
drawn share; a giver when what left through its faces reaches it": the
first half is (2); the second cannot be, because a standing record's
current through every Link is 0 (9.17 (7) (a), 9.32 (b)) and 9.37 (1)
proves that no change of the body's integers makes it leak by the step:
NOTHING LEAVES A BODY AT REST BEFORE ITS CLICK. The giver's term on the
shell is therefore not an outflow but the TICK, the share of its own
standing record at the shell's Nodes gathered per interval ((2)); the
one rule for both ends is the one gather on the shell, the passing
record through the Ports and the own record at the Nodes, with one
threshold. What leaves the body is the born record, set on the body's
Nodes at the click (9.37 (2)) and carried out through the faces by the
step alone afterwards; the quantum stays one per click (9.37 (2), 9.25
(2)). (b) THE BOSS'S CURRENT, (1/2)[a_j(now)(a_i(next) - a_i(before)) -
a_i(now)(a_j(next) - a_j(before))], CHECKED (scratchpad boss_current2.py,
the chain with a pair boundary and a Node clock field): per Link it is
exactly the mean of the one-sided current now_i before_j - before_i now_j
at two successive readings (before -> now and now -> next; to 1.6 x
10^-14), and num Gamma times its six values at a Node is the mean of two
successive intervals' changes of the form E_i of 9.35 (2) (to 3.7 x
10^-15), carrying no pair weight and no clock weight, as he says. It is
the same line centred in time, and right as a diagnostic; THE CLICK'S
GATHER STAYS THE ONE-SIDED CURRENT read on the two levels before the
step (9.35 (2), 9.25 (2)): it needs no next level (which the gather does
not yet have), and it gives each interval its own flux whole, where the
centred one hands half of it to the neighbouring interval.
(c) THE SAME ANSWER IN THE FRAME OF RECORD 1967. A taker completes the
share the remainder set by what enters through its faces, part after
part. A giver completes it by its own rotation, gathered part after part
at its shell's Nodes: one period is the whole, and the remainder set the
fraction of it at which the gathering is complete. At that moment one
whole quantum leaves: the born record, set on the body's Nodes at the
click and carried out through the faces by the step alone; nothing is
written, and the remainder stays behind at the Node.

**(9) THE BIGGER RULE: THE BODY IS ONE NODE (the model owner's word,
2026-09-25, in the mathematician's session: "this feels to me like a
complication of a bigger rule that we need, out of clicks, a sum of
remainders and the order of the small Node"; CHECKED and COMPUTED).**
The owner is right that (2) can be said without the walk. THE RULE: a
body is one Node. Its levels are its profile on its Nodes; its Ports are
its surface ((1)); its share is its whole; and ITS REMAINDER IS THE SUM
OF ITS NODES' REMAINDERS, read on the wheel: u = (sum over the body's
Nodes of r_i, mod wall) / g, with g = gcd(num, wall) and W = wall / g as
for one Node (9.19 (4); each r_i moves on the multiples of g, so the sum
does). Then the order of the small Node applies to the body verbatim:
the step at every Node; the gather, the inward current of a passing
record through the Ports and the body's own share; the click at the
threshold (2 u + 1) / (2 W) of the whole set by the remainder; at the
click the whole out (a passing record cleared and the content up one;
the own record's click the born family's levels set and the stock down
one), the remainders staying behind at the Nodes. No Node is chosen and
no order is declared inside a body: the landing Node and the walk of
(2) are needed only between bodies (the ladder of detectors, 9.25 (2),
where a detector of the ladder is a whole body) and never inside one. This
is the frame of record 1967 read on a body as on a Node, and it is what
the owner asked for.

COMPUTED on the integer law with the remainders kept and no coupling
(scratchpad sum_remainders.py, sum_remainders2.py, sum_remainders3.py;
the well [800, 801] of side 32 on the chain, W = 2403): the born residue
as the sum over all the body's Nodes: 4000 cycles, 1949 distinct values
where a uniform draw expects 1948, the chi-square over 20 bins 30.3 on
all 4000 (33.5 and 21.3 on the two halves; the 95 percent bound 30.1),
the mean cycle 48.1 +- 0.4 against P / 2 = 46.8; the sum over the shell
Nodes alone: 1944 distinct, the chi-square 52.2 on 4000 (25.3 and 38.2),
the mean cycle 46.8 +- 0.4; the remainder at one Node (the centre, the
engine's reading today): 1325 distinct of 2000 where uniform expects
1357, the chi-square 50.3 on 2000. THE HONEST READING: every reading of
a reseeded body's remainder is a deterministic map on the wheel (the
levels are the same profile at every reseed, so the next residue is a
fixed function of the last), and none is exactly uniform over thousands
of cycles; the sum over the body's Nodes covers the wheel exactly as a
uniform draw does and shows the mildest structure of the three, a few
percent in 20 bins, which no pin sees (the pins are binomial shares with
bands of 5 to 10 percent, 9.22 (8)). RECOMMENDED: the owner's form, the
sum over the body's Nodes, as the body's remainder; the landing Node of
(2) withdrawn inside a body.

### 9.39 The cube's click with everything in, and what must be declared (the model owner's words of 2026-09-25 through the Boss: record 1970, only the name Node, a body a number of Nodes; record 1971, "we do not need a well and a wave height; everything converges from the click once the laws are at the Node; check the algebra with everything in; run a world with a cube and see its click by the faces or by the sum of the remainders"; the Boss's host run; DERIVED and COMPUTED; written with the name Node alone)

**(1) THE CUBE'S CLICK, DERIVED WITH EVERYTHING IN.** The state at a Node:
per record two levels and a remainder, kept at the Node (9.34 (A)); per
family a pair; per Node the content M of the body it belongs to and the
Node clock (Gamma, Gamma + M) (9.35 (3)). The step at every Node: 3 den
f a_next + r' = e num S_6 + 6 den (f - e) a_now - 3 den f a_before + r,
with (e, f) the Node's clock. A cube of side 3 is a body of 27 Nodes; its
faces are its 54 outward Ports (9.38 (1)); it holds no standing record
(a detector), or it holds one (an emitter, a holder). THE TAKING END: a
record passing the cube offers, every interval, the positive current
through its faces, num Gamma (now_i before_j - before_i now_j), read on
the two levels before the step; by the body's Gauss law (9.38 (3) (b))
the net current through the faces is the change of the record's share
inside, so the faces read the body's whole of the record and nothing
twice. The record's running total C is compared with (2 u + 1) T / (2
W): T its whole; u and W its residue and wheel, INHERITED AT ITS BIRTH
from the body that gave the click (9.19 (4); a record of light [1, 1]
born of a body [800, 801] carries W = 2403, not light's own wheel of 3,
which would quantise every share to sixths). The click at the first
interval at which C reaches the threshold: the record is cleared on all
its Nodes, the cube's content rises by one, its clock at its 27 Nodes
slows by 1 / (Gamma + M), and the remainders stay where they are. THE
GIVING END, if the cube holds a standing record: its own share at its
Nodes, gathered every interval (constant; the tick), against P times
that share; the click at (2 u + 1) P / (2 W) with u the sum of the
body's remainders on its wheel (9.38 (9)); the born family's levels set
on the 27 Nodes with the character, the stock down one, the remainders
kept. THE REMAINDER RULE: a record whose remainders are 0 for ever (an
exact one, 9.26 (4a)) has no residue and never clicks; a residue that
happens to read 0 on a body that is not exact is a rung at 1 / (2 W),
the first place on the wheel, and clicks (9.33 (4) and 9.34 (4) agree on
this: the rule is about the exact record, not about the digit 0). NO
PART FAILS WITH THE OTHERS IN: the clock changes the operator at the
body's Nodes at each click by 1 / (Gamma + M) and sheds nothing of the
born family (9.37 (1)); the remainders kept through the click and the
reseed spread the residues with no coupling (9.34 (2), 9.38 (9)); the
click hands over whole numbers only; the faces are read on the levels
before the step, which the Node has; the exact record passes the faces
and is not gathered. THE BOSS'S HOST RUN, CONFIRMED: a half-sine record
of 32 Nodes through a cube of side 3 across a section of 9 x 9 offers
the cube 0.1107 of its whole, which is the geometric share 9 / 81 = 1 /
9 of the section (the record's form is uniform across it); the net
inflow equals the change of the share inside, in integers, which is the
body's Gauss law; and THE SUM OF THE CUBE'S REMAINDERS STAYS IN [0, 54]
(27 Nodes on light's wall 3) AND DOES NOT FOLLOW THE PASSAGE, which is
right: the remainder is not the measure of what passes, the faces are;
the remainder is the measure of WHERE in the share the click falls, read
once at a birth on the giving body's wheel. So the cube's click reads
the faces, and the remainder sets its place: the Boss's sentence,
derived.

**(2) THE WAVE HEIGHT IS NOT PHYSICS (CONFIRMED, with its two bounds).**
The click is scale-free: the threshold is a fraction of the record's
whole, and scaling every level by a factor scales every share and the
whole by its square, the ratio unchanged; one record is one quantum
whatever its height (9.33 (2), "the quantum is counted, not weighed").
The height is a convention of the write, with two bounds that are the
integers' and not nature's: below, the rounding (the accounting error
under one unit per Node per interval, 8.2; a body whose remainders take
fewer than 500 values is refused, 9.19 (4a); a tail must reach 0 before
the next body or a face, 9.22 (7a) (i)); above, the working amplitude
2^28 under int64 (9.35 (3)). Between them no pin depends on it.

**(3) THE WELL: WHAT THE OWNER'S CLAIM GETS RIGHT, AND THE LEAST THAT MUST
BE DECLARED (COMPUTED).** (a) A TAKING BODY NEEDS NO WELL: a detector is
a declared number of Nodes with its Ports and a place on a ladder; the
Boss's cube is 27 Nodes of the vacuum and reads 1 / 9 of the record;
nothing at its Nodes is lowered. Every detector of the rows is such a
body. (b) A GIVING BODY NEEDS A STANDING RECORD, and a standing record
needs a bound mode of the operator; in a uniform vacuum the operator has
none (every mode is a plane wave; a written packet disperses). CAN THE
NODE CLOCK BIND IT, so that the content makes its own well and nothing is
declared? For a family of pair p the clock at a body of content M raises
the local band top by 2 (1 - p) M / (Gamma + M), the same as a lowered
pair of relative depth (1 - p) M / (p (Gamma + M)); FOR LIGHT (p = 1) IT
RAISES NOTHING: the clock never binds light, at any Gamma (9.29, light
has no well). For matter [800, 809] the critical depth of a cube on the
three-dimensional lattice (scratchpad cube_bind_np.py, the top mode by
iteration on a periodic box, bound when it lies above the vacuum's band
top and on few Nodes): side 3 between 0.10 and 0.15; side 8 between
0.010 and 0.020; side 32 between 0.002 and 0.003 (the declared well
[800, 801] in [800, 809] is 0.010, bound on about 20800 Nodes). The
clock's depth at Gamma = 10^6: 1.1 x 10^-8 for M = 1, 7.2 x 10^-7 for M =
64, 1.1 x 10^-4 for M = 10^4, below every threshold; to bind a cube of
side 32 by its own content the clock needs Gamma of the order of M
(Gamma = 300 at M = 64 gives 2.0 x 10^-3, just short; Gamma = M gives 5.6
x 10^-3, bound), and then the clock at the body runs at 0.5 to 0.8 of
the vacuum's, which moves every clock row of 9.22 (8) by tens of percent
against bands of 0.3 percent. So THE LEAST THAT MUST BE DECLARED for a
body that gives is ONE LOWERED PAIR PER REGION PER FAMILY, the well,
which stands in for the binding the algebra does not yet have (a charge
law would be its own identity, 9.27 (D)); the alternative, Gamma of the
order of the content under its own identity, is the content as its own
well and is refused by the clock rows as they stand. The owner's
sentence holds for everything that takes and for the height; for what
gives, the well is the one declaration left.

### 9.40 The body, the click and a mere number of Nodes, in algebraic sentences alone (the model owner's word of 2026-09-25 in the mathematician's session: "check it purely algebraically; a body is not just a number of Nodes, a body for us is a number of Nodes that click together; derive from there the big law on a body that keeps it a body with the remainders; what is a click, what is a body, what is a mere number of Nodes; put the Node's remainder and the click's action on the clock into the algebra and then derive"; DEFINITIONS AND THEOREMS, no run on the board)

**D1 (the state).** The GameBoard is a finite set of Nodes with six
Links each. A record of a family is a triple (a, b, r) of integer
vectors over the Nodes: the level now a, the level before b, the
remainder r with 0 <= r_i < wall_i, wall_i = 3 den_i, [num_i, den_i] the
family's pair at Node i. A Node also carries an integer content M_i >= 0
and from it its clock (e_i, f_i) = (Gamma, Gamma + M_i), Gamma an
integer of the world, the same for every family.

**D2 (the step).** One interval maps every record (a, b, r) to (a', a,
r') by, at every Node, 3 den_i f_i a'_i + r'_i = e_i num_i (S_6 a)_i + 6
den_i (f_i - e_i) a_i - 3 den_i f_i b_i + r_i, with 0 <= r'_i < wall_i
f_i, S_6 the sum over the six neighbours. The step is linear in (a, b)
apart from the floor, is a bijection of (a, b, r) (9.26 (3) (a)), acts
separately on every family (no cross term, 9.34 (B)) and touches M and
Gamma not at all.

**D3 (the share, the current, a number of Nodes).** For a record, the
share at Node i is E_i = 3 den_i f_i (a_i^2 + b_i^2) - num_i Gamma a_i
(S_6 b)_i - 6 den_i M_i a_i b_i and the current from j to i is J_ij =
num Gamma (a_i b_j - b_i a_j) (9.35 (2)). For ANY set S of Nodes, its
Ports are the Links (i, j) with i in S and j not in S, its share is E_S
= the sum of E_i over S, and its whole is I = E over all Nodes.
THEOREM T1 (Gauss on any set): E_S after the step minus E_S before the
step equals the sum of J_ij over the Ports of S, exactly in the real
law and up to the remainders' rounding in the integer law; the sum over
all Nodes is invariant. Proof: the identity at one Node (9.19 (3), 9.35
(2)) summed over S; J_ij = - J_ji cancels every Link inside S. So a mere
number of Nodes has Ports, a share of every record and a Gauss law, and
nothing else.

**D4 (a standing record; a body).** A record is STANDING on the set S
if (a, b) = (phi cos(omega t), phi cos(omega (t - 1))) for an integer
profile phi supported on S and a rotation omega: an eigenvector of the
family's operator on the board, phi's support S. A BODY is the support
of a standing record. THEOREM T2 (what makes a body a body): for a
standing record every current J_ij is 0 (a_i b_j - b_i a_j = phi_i phi_j
[cos(omega t) cos(omega (t - 1)) - cos(omega (t - 1)) cos(omega t)] =
0), hence by T1 the share E_i is constant in time at EVERY Node of S,
and the gather of the record over any subset of S is t times a constant
against P times the same constant: the ratio t / P is the same at one
Node, at the shell, at all of S. THAT IS THE ALGEBRAIC SENTENCE "THE
NODES OF A BODY CLICK TOGETHER": they carry one eigenvector, so they
carry one time. A set that carries no eigenvector has no constant share
and no common time: it is a mere number of Nodes; it can take (its
Ports gather a passing record) and cannot give. THEOREM T3 (a body
needs a well): the operator with one pair everywhere has no eigenvector
of finite support (every eigenvector is a plane wave); an eigenvector
of finite support exists iff the pair is lowered on a region deep
enough (9.39 (3), the thresholds), and the clock (Gamma, Gamma + M)
lowers nothing for light and 10^-8 to 10^-4 for matter at Gamma = 10^6.
So a body is the eigenvector of a declared well, and "a body is
something special in the algebra of the big cube" is this: it is an
eigenvector, a mere number of Nodes is not.

**D5 (the click, as an operator on the state).** Let a record have the
residue u on the wheel W (D6) and the threshold theta = (2 u + 1) T / (2
W), T its whole gathered per acquisition. The TAKING END at the set S:
at the first interval at which the running sum of the positive Port
currents of S reaches theta, the map X_S: (a, b, r, M) -> (a with the
record's rows set to 0 on its support, b likewise, r UNCHANGED, M_i + 1
for every i in S). The GIVING END at a body S with a standing record
(phi, omega) and a stock: at the first interval at which t E_S reaches
theta with T = P E_S (equivalently t >= (2 u + 1) P / (2 W)), the map
X_S^T: (a, b, r, M, stock) -> (the born family's rows set to psi_S chi_K
on S, psi_S the born family's eigenvector on S with the zero row beyond,
chi_K the character of the declared momentum; the own record's rows
left as they are, with their phase (no reseed, 9.43); r UNCHANGED; M_i - 1 for every i in S
by the stock's quantum leaving; stock - 1). A CLICK IS ONE OF THESE TWO
MAPS, applied once, at one interval, on all the Nodes of one set at
once, and nothing else is a click. THEOREM T4 (the clock under a
click): X_S and X_S^T change no r, no pair and no Gamma; they change M
on S by +-1, hence the clock at every Node of S from (Gamma, Gamma + M)
to (Gamma, Gamma + M +- 1). For every family at those Nodes the
rotation goes from omega to omega' with 1 - cos omega' = (Gamma / (Gamma
+ M)) (1 - cos omega) (9.35 (2)); so one taken quantum slows every clock
on S by (1 - cos omega') / (1 - cos omega) = (Gamma + M) / (Gamma + M +
1), a period longer by 1 / (2 (Gamma + M)) for small omega, and one
given quantum hastens it by the same; a standing record's next tick
(2 u + 1) P' / (2 W) is longer by that factor, and every record passing
S is bent toward it by the same clock (9.35 (5)). THIS IS THE WHOLE
ACTION OF A CLICK ON A CLOCK: through M and through nothing else. A
click also sheds nothing: X_S^T sets the born rows, and the step alone
carries them out (9.37).

**D6 (the remainder, and the law that keeps a body a body).** The
remainder r_i belongs to the Node: D2 moves it, D5 leaves it. THEOREM
T5 (a body is one rotation carried for ever, and remembers in its
remainders): X_S^T leaves the own record's levels, phase and remainders
as they are, so the body is the same eigenvector on the same Nodes,
carried by the step alone between its clicks (the rounding's drift below
one unit per Node per interval, 8.2); its remainders after a cycle are
r_i(t) = (c_i(t, phase) + r_i(0) + the carries) mod wall_i with c_i the
rounding sequence of the profile at Node i AT THE PHASE THE RECORD HAS,
which advances by the cycle's length modulo the period, an irrational
number of intervals; hence the next residue is a function of the last
and of the phase (a map on the wheel whose shift does not repeat, 9.43),
and the body's REMAINDER is the sum of its Nodes' remainders on its
wheel, u = (sum over S of r_i mod wall) / g, g = gcd(num, wall), W =
wall / g (9.38 (9)). The law that keeps a
body a body across its clicks is therefore: THE CLICK LEAVES THE BODY'S
OWN RECORD, LEVELS AND REMAINDERS, AS IT IS; the eigenvector
makes the Nodes one body (T2), the remainders make its next click's
place (D5), and the content it gave or took sets its clock (T4). Nothing
is kept at a Node beyond a, b, r and M. THEOREM T6 (the remainder
rule): a record with r = 0 at every Node for ever (an exact one, 2 cos
omega in {-1, 0, 1}, 9.26 (4a)) has no residue to read and is never
gathered: it crosses every set's Ports and no X_S applies; every other
record has a residue and clicks once, at the first set whose gather
reaches its threshold (9.25 (2), one quantum one click).

**THE SENTENCES, GATHERED.** A click is X_S or X_S^T at one interval on
one set. A body is the support of an eigenvector of the operator with
its declared well; its Nodes share one time, so they click together,
and their remainders' sum is its residue. A mere number of Nodes has
Ports and a Gauss law, takes and never gives. The remainder is the
Node's, moved by the step and left by the click. A click acts on the
clock through the content alone, by (Gamma + M) / (Gamma + M +- 1). No
run on the board is needed for any line above; the runs of 9.38 and
9.39 are illustrations of T2, T5 and T3 and add no rule.

### 9.41 A fourth family, of clicks: the clock field (the model owner's question of 2026-09-25 through the Boss, record 1972, "perhaps we need a fourth family, of clicks?"; the Boss's reading; CHECKED against the three tests and COMPUTED on the algebra; ADOPTED by the model owner as the fourth family, record 1982, "close everything together, the family of clicks included, the clock inside it as its amplitude"; the one statement in 9.45)

**(1) WHAT IT IS.** A family whose level c_i at a Node is what the Node
clock reads: (e_i, f_i) = (Gamma, Gamma + c_i). It has a declared pair,
two levels and a remainder per Node like every family, and it moves by
the step (D2). The clock term of the step at every other family, 6 den
(f - e) a_i = 6 den c_i a_i, becomes a product of two families' levels
at one Node.

**(2) THE THREE TESTS: IT PASSES, AS A MODULATION AND NOT AS A SOURCE.**
Generic: one primitive, a family named by its role (as the born family
is), with declared integers and no family name in the rule. Vector: the
term c_i a_i is a product of two levels at one Node, the share's own
verb (E_i has a_i b_i), no root, no float; it is NOT the retired
coupling of 8.5, which made rows of one family out of another's (a
source term, 9.37 (5)): here the family's own row is multiplied by an
integer that happens to be another family's level, and by 9.37 (1) it
sheds nothing of any family. Local: c_i at the Node. Exact and
reversible between clicks: at each interval the wall 3 den (Gamma +
c_i) is an integer at the Node, the step of every family given c(t) is
the bijection of D2, the remainder is formed again below the new wall,
and c's own step does not read the other families, so the joint step
inverts; the one bound is |c_i| < Gamma, the loader's.

**(3) ITS PAIR AND ITS SOURCE (DERIVED).** A lasting field around a mass
is a STATIC solution of the step, a_next = a_before = a_now, that is 2
a_i = (p / 3) (S_6 a)_i. With p = 1 (light's pair) this is the discrete
Laplace equation, whose solutions outside a source fall as 1 / r; with
p < 1 every static solution is screened, falling as exp(- kappa r) / r
with kappa^2 = 6 (1 / p - 1) (for [800, 809], kappa = 0.26 per Link, a
range of four Links). So THE CLOCK FIELD IS MASSLESS, ITS PAIR [1, 1].
Its source: a click alone, a pulse of c born whole and left to the step,
spreads outward at one Link per interval and leaves no lasting field;
the field lasts only if THE CONTENT IS HELD at the body's Nodes as a
boundary value, c_i = M there, written whole at each click and kept,
which is exactly 9.35 (3) as it stands (M changes only at births and
clicks). Around it the step's static part is the discrete Coulomb
potential (COMPUTED, scratchpad side3_window.py (b): a content M held on
a cube of side 3, the far border 0: the level times the distance is
constant, 1350 to 1420 for M = 1000 over 2 to 6 Links, the cube acting
as a sphere of radius about 1.4 Links; it falls only where the far
border is felt), and the transients are outgoing waves at light's pace,
booked by the face slabs of an open board; on a periodic board they
never leave, so the field settles only where the faces take. The one
thing beside the step is the held level at the body's Nodes, and it is
already in the law.

**(4) WHAT IT GIVES.** (a) THE SLOWING AROUND A MASS: c_i = M R / r
(R the source's radius in Links) puts the clock (Gamma, Gamma + M R /
r) at every Node around the body: 1 - cos omega' = (Gamma / (Gamma +
c)) (1 - cos omega), a period longer by c / (2 Gamma) = M R / (2 Gamma
r): NEWTON'S POTENTIAL IN THE CLOCK, the weak-field redshift form with
R / (2 Gamma) in the place of G / c^2 in the board's units; linear in M,
so it escapes the quadratic source of 9.29 (4) (a); every family
including light bends toward the slow region (9.35 (5)). (b) A BODY ITS
OWN WELL: NO. At its own Nodes c_i = M, the same depth as 9.39 (3),
(1 - p) M / (p (Gamma + M)), 10^-8 to 10^-4 at Gamma = 10^6 against
thresholds of 10^-3 to 10^-1; light is never bound by a clock. The
fourth family moves the field's FORM outside the body, not the binding
question. (c) LIGHT WITH LIGHT: only if a light record's presence counts
as content and is held, which light, moving, cannot be: a light record
would source a moving pulse and no lasting field; so no, by the same
rule, unless the owner declares light's content otherwise.

**(5) THE PINS AND THE COST.** At Gamma = 10^6 with M at most 100 the
field is at most 100 x 1.4 / r, the slowing at most 1.4 x 10^-4 at one
Link and 10^-5 at ten: NO PIN OF THE EIGHTEEN MOVES; the gravity row
(9.22 (8a)) changes its form from the declared well's profile to the 1 /
r potential, a computed row. The cost: two levels and a remainder per
Node more, and the owner's constant of three families becomes four.
VERDICT: it passes the three tests as a modulation; its pair is [1, 1]
and its source the held content; it gives the slowing around a mass in
Newton's form and does not give a body its own well; it is a hypothesis
under its own identity (the key `clock_family`), built after the Node
clock (decision (5)) and only on the owner's word.

### 9.42 A detector is a body (the model owner's decision of 2026-09-25 through the Boss, record 1974: "a body has an algebraic definition; just Nodes are not a body; a number of Nodes must click for them to be a body"; the Boss's four questions and record 1975; COMPUTED)

**(1) THE DETECTOR BODY'S STANDING RECORD.** Its family: a matter family,
the screen's matter, declared per detector region; its pair: the
family's pair lowered on the region (a well) inside the window of (2);
its standing record: the well's bound mode, generated as every body's
(9.22 (7a)); its content M: the quanta it holds, rising by one at each
of its clicks; its own remainders: kept, and never read while it only
takes (the threshold of a taking is the PASSING record's residue, D5).

**(2) THE LEAST BODY OF SIDE 3 (COMPUTED, scratchpad side3_window.py
(a)).** In the vacuum [800, 809] a cube of side 3 binds a mode from the
relative depth 0.135 and runs away (2 cos omega > 2, no rotation) from
0.185: THE WINDOW IS THE PAIR INSIDE FROM ABOUT [800, 713] TO [800, 686]
(2 cos omega from 1.980 to 1.999, the mode on 2000 to 160 Nodes). A pair
above 1 inside is lawful there because the confinement of three Nodes
keeps 2 cos omega below 2; the same pair over 32 Nodes runs away (the
holder's [699, 700], 9.31). A SLAB, the receiver at a face [N, M, d],
binds at ANY positive depth (a well binds in one dimension however
shallow), so the face slabs are bodies with a shallow pair such as
[800, 808]. DOES THE DETECTOR NEED ONE RICH NODE? No: a taking body's
own remainders are never read; an exact brick (2 cos omega in {-1, 0,
1}) takes as well as any body; the detector's residue matters only if it
gives (a screen that re-emits), and then 9.38 (9) reads its sum.

**(3) THE TAKING AT ITS FACES, AND ITS OWN RECORD AT THE CLICK.** The
passing record is gathered through the body's Ports (9.38 (2), D5 X_S)
and nowhere else; at the click the record is cleared on all its Nodes,
the detector's M rises by one on all its Nodes, its clock goes to
(Gamma, Gamma + M + 1), and so ITS OWN STANDING RECORD'S ROTATION SLOWS
by (Gamma + M) / (Gamma + M + 1) (T4), its levels untouched (no reseed
at a taking). That is record 1139's "the detector's own record changes
at the click", in its exact form.

**(4) THE EIGHTEEN.** Every detector region of the rows (a screen's
pixels, the receivers, the face slabs) is declared a body: a matter well
inside its side's window with its mode generated (one small mode per
detector; a screen of forty pixels of side 3 is forty modes of 27 Nodes;
a slab one mode); the ladder's places are bodies. The passing light is
unaffected by a matter well (no coupling, 9.34 (B)) and by the
detector's clock beyond M / Gamma, at most 10^-4 after thousands of
clicks: NO PIN MOVES IN FORM. ONE PLACEMENT CHANGE: two wells whose
modes overlap are ONE body with one click (9.32 (c)), so adjacent pixels
would merge into one place; at the depth 0.18 the side-3 mode lies on
about 160 Nodes, a tail of two Links, so PIXELS STAND FOUR LINKS APART
(a pixel every seven Links), the light between them going to the slab
behind; the fringe spacing 53 of the two slits is resolved by pixels
every seven Links as before, and the counts per pixel scale by 3 / 7,
the pins recomputed under the same rule. The bricks of side 3 (9.35
(8)) are these bodies.

**(5) THE WHEEL UNDER THE NODE CLOCK, AND THE CURRENT'S BOOKING (record
1975 (3) and (4); Nature24's question).** The wheel is THE RULE'S AT THE
NODE: the remainder moves on the multiples of gcd(e num, 6 den M, 3 den
f) below the wall 3 den f, so W = 3 den f over that gcd; at M = 0 every
coefficient carries Gamma and W is the pair's own 3 den / gcd(num, 3
den), and at M > 0 it is finer (18,774,639 at M = 64 on the light
clock's A against 2403). u and W are read together at the birth and
travel with the record as the fraction (2 u + 1) / (2 W) (9.25 (2)); all
the Nodes of one body share M, so the sum of 9.38 (9) is on one wheel;
the click's statistics are the same on a finer wheel. THE BOOKING: the
current through a Link stays num Gamma (now_i before_j - before_i
now_j), read on the two levels before the step, with no weight f / e or
1 / e (9.35 (2), 9.38 (8)); the weights f / e enter the SHARE and the
WHOLE (E_i and I), which the tick and the threshold T use; the ladder's
increments are the currents as booked today times the wall's integer
factor. The order (2) then (5) is right: without the coupling's scale
the wall 3 den (Gamma + M) times the amplitude 2^28 is below 2^63 at the
muon's pair (7.8 x 10^18).

### 9.43 The countdown of the residues, and the reseed retired (Nature24's finding of 2026-09-25 on the tree with decisions (1) and (2): under the kept remainder and no coupling, the light clock's births came in runs of one per interval, twenty-six in a row; the mechanism on the engine's integers; CHECKED on the algebra; the ruling, for the model owner's word under record 1940)

**(1) THE FINDING (Nature24, GAMEBOARD readings, no verdict).** With the
remainder kept through the reseed and the coupling retired, the excited
record reseeded at each birth as the profile at phase 0 reads, after its
first advance, the residue u - 1 where u was the born record's: the
profile's first-step rounding at the read Node is exactly one unit. A
residue below W / P (25.6 on the light clock's body) crosses its rung in
one interval, so the next is u - 1, and the countdown runs to 0: u + 1
births at one per interval; thirty-two of the sixty-four births of the
light clock came in two such runs, the mean click interval 270.5 against
302.2 with the coupling.

**(2) THE MECHANISM, ON THE ALGEBRA.** With the reseed, the residues'
order is the map u -> u + S(t(u)) mod W, where t(u) = ceil((2 u + 1) P /
(2 W)) is the cycle's length and S(t) is the rounding accumulated at the
read Node over t steps FROM PHASE 0, a fixed sequence of the profile. For
t = 1, S(1) is the profile's first-step rounding at the read Node: a HOST
CONSTANT, set by the generator's precision and not by the law: -1 unit
for the generator's profile at its stop (Nature24), -1147 units for a
float eigenvector rounded at 2^28 and +337 at 2^20 (scratchpad
countdown2.py). At -1 the map counts down; at -1147 or +337 it does not
run but turns the wheel by a constant, and the residues fall on a
lattice (the chi-square 79 and 71 on 20 bins against the bound 30.1).
Either way the birth statistics of a closed body would depend on the
profile's rounding, which the law forbids (9.39 (2): the height and the
precision are not physics). The reseed is the cause: it resets the
phase to 0 at every birth, so the rounding sequence is the same every
cycle and the shift is a constant.

**(3) THE RULING: THE RESEED IS RETIRED; A BODY'S OWN RECORD IS NEVER
REWRITTEN.** The giving end of the click sets the born family's rows on
the body's Nodes, lowers the stock and the content, and LEAVES THE
BODY'S OWN LEVELS, PHASE AND REMAINDERS AS THEY ARE; the step alone
carries the standing record between its clicks. Then the rounding
sequence runs at the phase the record has, which advances by the
cycle's length modulo the period, an irrational number of intervals, so
the shift takes a different value at every cycle and no countdown can
form. COMPUTED (countdown2.py, the well of side 32, 3000 cycles in
order, the residue read after the first advance as the engine reads it):
with the reseed, the centre Node's shift over a one-interval cycle is
one constant (-1147 at 2^28, +337 at 2^20) and the chi-square 79 and 71;
the body's sum with the reseed one constant (931, -901), chi-square 19
and 24; WITHOUT the reseed the shift takes many values (11, 177, 214,
405, ... at the centre; 136, 158, 217, ... for the sum), the longest run
of one-interval cycles is 1 or 2 as a fair draw gives, the mean cycle
46.9 to 47.8 against P / 2 = 46.8, the chi-square 14 to 27 on 20 bins.
The read point stays as built (the next tick's residue after the first
advance; the born record's residue at the click), moving to the body's
sum on the owner's word (9.38 (9)). NEITHER (a) NOR (b) of Nature24's
question: (a) would pin a host precision as physics; (b), a read after
a full period, is the same constant map with S(P) in place of S(1).

**(4) WHAT CHANGES IN THE TEXTS.** 9.17 (4) item 1 and 9.33 (3) ("a body
is periodic to the bit by its clicks; its excited record reseeded from
the stock as the same integers") are HISTORY: a body is one rotation
carried for ever within the rounding (Niven, 9.26 (4)), its levels never
rewritten, its remainders its memory (9.34 (A) unchanged); 9.37 (2), 9.38
(2) and 9.40 (D5, T5) are corrected in place; the load's seed is the one
write of a body's record. The three tests: generic (one write fewer);
vector (nothing new); local (nothing new). No pin moves in form; the
light clock's mean interval and first click are recomputed by Nature24
on the engine without the reseed, and I expect 302 +- 9 and 250 +- 8 as
pinned (the mean cycle P / 2 and no run). In the engine: the emitter's
click creates no fresh excited record; the block's own record continues;
the next residue is read after the first advance as now; the stock and M
move.

### 9.44 The click known at each Node of a body's boundary (the model owner's word of 2026-09-25 through the Boss, record 1981: "a click is a connected body all of which passed one phase; you want to know it from each Node on its boundary; perhaps a family of clicks that spreads, and that is the flux; with a constant flux you recognise the body at each Node of its boundary; the fourth family gathers everyone's remainders and knows whether you are on a body's boundary; if you are, and the body passed a phase, you get the click"; the Boss's four questions; DERIVED, and one recommendation of 9.38 (9) withdrawn)

**(1) THE PHASE IS ALREADY LOCAL AT EVERY NODE OF A BODY.** For a
standing record (D4) every Node carries the same rotation: the
eigen-relation a_next + a_before = 2 cos omega a_now holds at each Node
by itself, so a Node reads 2 cos omega, hence the period P, from its own
three levels; its share E_i is constant in time (T2), so "the body passed
the fraction t / P of a phase" is the same count at every Node; and the
content M, which changes at the click, is on every Node of the body, so
each Node counts from the last click. THE MARK OF A BODY AT A NODE IS A
CONSTANT FLUX, AND THE CONSTANT IS ZERO: for a standing record the
current through every Link is exactly 0 (T2) and the share is constant;
a passing record gives a changing share and currents through the Links.
A Node knows it is on a body by that mark, and on the body's BOUNDARY by
a neighbour whose row of the record is 0, all from itself and its six
neighbours. So the owner's sentence, "with a constant flux you recognise
the body at each Node of its boundary", holds in the law as it stands,
with the fourth family not needed for it: the constant flux is the
standing record's own zero current, and the phase is its own rotation.

**(2) THE ONE BODY-WIDE INTEGER IS THE RESIDUE, AND A SPREADING FIELD
CANNOT MAKE IT LOCAL.** What the shell's gather of 9.38 (2) sums across
the body is not the phase but the residue u, the place on the wheel at
which the count is complete. A family sourced by the Nodes' remainders
and spread by the step delivers at each Node the static part of its
step, a sum of the remainders weighted by the lattice's Green function
(about 1 / distance, 9.41 (3)): a real number, different at every Node,
never the integer sum modulo the wall; so the boundary Nodes would read
different residues and click at different intervals, and the body would
not click together (T2). Nor can the remainders be its source (9.41 (5)
and the owner's question in the mathematician's session): the remainder
is where chance lives and the click reads it (9.32 (d)); a field fed by
remainders would count occupied Nodes at wall / 2 each, whatever their
energy (9.35 (1)), so a photon would source it like an atom; and a
record that gives its remainder away loses the bijection of its step.
The family of 9.41 is sourced by the CONTENT, whole at each click; it
passes the three tests as a modulation; the remainder-sourced family
passes them in form (one primitive, sums, local) and fails in what it
sources. The two local ways to a common residue: (a) THE REMAINDER AT
ONE NODE OF THE BODY, the first shell Node in the declared order, where
the walk of 9.38 (2) lands for the tick (the shares being constant, it
lands there every time): one integer at one Node, read after the first
advance, and by 9.43 a fair draw once the reseed is retired (COMPUTED,
countdown2.py (iii): the chi-square 16.5 and 13.7 on 20 bins, no run,
the mean cycle P / 2); (b) a tally passed along the body's Links at one
Link per interval, which reaches every Node after the body's diameter
and is a register in transit, which the law does not keep at a Node.
RECOMMENDATION, REVISED: 9.38 (9)'s sum was my answer to the lattice of
residues under the one-Node read, and 9.43 has traced that lattice to
the reseed, not to the read; with the reseed retired the one-Node read
is fair and LOCAL, so I withdraw the sum in favour of (a): the body's
residue is the remainder at its first shell Node, read after the first
advance; the born record's residue the same Node's remainder at the
click. This is the owner's wish for a click known at a Node, met inside
the law.

**(3) WHAT THE FOURTH FAMILY DOES, AND DOES NOT.** It does not mark the
body (the eigenvector does) and does not carry the residue (nothing
spreading can). It carries the CLICK OUTWARD: at the click c rises by one
on the taker's Nodes or falls by one on the giver's, and the step spreads
the change from the body's surface at one Link per interval as a shell
with the sign, behind it the static part higher by one (9.41 (3)); a far
Node learns that a click happened, where and in which direction, when the
shell arrives, and the far clock changes then and not before: the one
non-local act stays the record's ending, and the knowledge of the click
travels at light's pace. That is the owner's "a family of clicks that
spreads, and that is the flux", exactly as 9.41 has it, with the content
as its source. One integer caution: a write of one unit per Node falls
below one unit within about sqrt(N_surface / (4 pi)) Links (22 for a body
of side 32, 2 for side 3) and the rounding takes it; so the fourth
family's quantum, how many units one click writes, is a declared number,
like every write's height, and sets how far in integers a click is seen.

**(4) THE CONSTANT FLUX, TWICE.** For the body's own standing record the
constant flux is 0 through every Link with a constant share: the mark of
a body at each of its Nodes, local, (1). For the fourth family around a
held content the steady state is the discrete Coulomb field, and by Gauss
on the lattice (T1) the outward flux through the body's surface is
constant in time and equal to its source: a Node with a steady nonzero
flux of that family through its Links is at a source, and the body's
surface is where the flux is constant and equal to M; that is the owner's
"constant flux" for the fourth family, the steady state that marks a
source's boundary from outside. Both are true; the first needs no new
family.

### 9.45 The Node clock is the family of clicks: the one statement (the model owner's decision of 2026-09-25 through the Boss, record 1982: "close everything together, the family of clicks included, the clock inside it as its amplitude"; 9.35 (3) and 9.41 read here as one; the owner's constant now at most four families)

**(1) THE FAMILY.** The fourth family is THE FAMILY OF CLICKS. Its pair
is [1, 1] (9.41 (3): the only pair whose static solutions reach). Its
level c_i at a Node is the Node clock: (e_i, f_i) = (Gamma, Gamma + c_i),
read by the step of every other family (D2). Its unit is the quantum:
one click writes one unit; its levels are counted in quanta and not in
the write-height of the other families, so THE CLOCK IS ITS AMPLITUDE,
as the owner says. It carries no residue, no ladder and no click of its
own: it takes and gives nothing; every family's clock reads it. The
static content M of 9.35 (3) and 9.36 is this family's level held at a
body's Nodes: the same integer under a family's name.

**(2) ITS SOURCE AND ITS STEP.** At the Nodes of a body the level is
HELD: c_i = the body's content, written whole at each click (up by one
at a taking, down by one at a giving, 9.40 D5) and kept between clicks;
that hold is the one place where a family's level is not the step's
own, and it is the same write as the load's (the vector test's verb).
At every other Node the family moves by the step of D2 with its own
pair, like every family, and reads the world's one border (record 1970).
Around a held body the step's static part is the discrete Coulomb
potential, about M R / r with R the body's radius in Links (COMPUTED,
9.41 (3)); a change of the held level at a click spreads outward from
the body's surface at one Link per interval with its sign (9.44 (3));
in integers a change of one unit per Node falls below one unit within
about sqrt(N_surface / (4 pi)) Links and the rounding takes it, and the
static level M R / r is below one unit beyond M R Links, so the field
in integers is the held content, its potential to M R Links, and
nothing farther; on the eighteen at Gamma = 10^6 no pin sees it.

**(3) WHAT IT CHANGES IN THE STEP, THE SHARE AND THE WHEEL.** Nothing in
form: the step at every Node is 3 den f a_next + r' = e num S_6 + 6 den
(f - e) a_now - 3 den f a_before + r with f = Gamma + c_i (9.35 (2)); the
share E_i = 3 den f (now^2 + before^2) - num Gamma now (A before)_i - 6
den c_i now before and the current num Gamma (now_i before_j - before_i
now_j), no weight in the current (9.38 (8), 9.42 (5)); the wheel at a
Node the rule's, 3 den f over the gcd of the step's coefficients, the
pair's own where c_i = 0 (9.42 (5)); the bounds: c_i < Gamma everywhere
(f > 0; Gamma above the world's whole stock) and the amplitude ceiling
2^28 with the wall 3 den (Gamma + c). WHERE THE FIELD IS STATIC the
per-Node identity and the invariant of 9.35 (2) hold exactly (computed
to 10^-15); WHERE IT CHANGES, a transient passing a Node, the identity
gains the term 3 den (f' - f)(now^2 + before^2) of the record there, the
clock's change working on the record: an exchange between the family of
clicks and the others, whose one conserved total, the field's own form
included, is OWED as algebra; at Gamma = 10^6 the term is 10^-6 of the
share per unit of the field and below every pin.

**(4) THE CIRCLE, CLOSED.** The remainder at a Node gives the place of
the click (9.44 (2), at one Node of the body); the click moves the whole,
one unit of the family of clicks at the body's Nodes; the family's level
is the clock at those Nodes and, by the step, the clock around them
(Newton's potential in the clock, 9.41 (4)); the clock sets every
family's rotation; the rotation leaves the remainder. 9.36's circle with
its one integer named as a family; 9.32's five lines, 9.34's decisions,
9.35's clock, 9.37's two ends, 9.38's shell, 9.40's sentences, 9.43's
retired reseed and 9.44's local reading are this one law, and the
owner's constant is four families: light, the matter families, and the
family of clicks.

**(5) THE EXCHANGE WITH A MOVING CLOCK, WRITTEN (the owed line of (3),
on the owner's word of 2026-09-25 in the mathematician's session).**
Let the clock at Node i change from f to f' (c to c') between one
interval and the next, by the family of clicks' own step or by a click.
The share of a record there, E_i of (3), changes by 3 den (f' - f)
(now^2 + before^2) - 6 den (c' - c) now before beyond the currents
through its Links: the clock's change works on the record. THERE IS NO
CONSERVED TOTAL OF THE FAMILIES TOGETHER BETWEEN CLICKS, and that is
the law's own choice, not an omission: the family of clicks reads no
other family (its source is the content, whole, at clicks; 9.34 (B)), so
it acts on every record's rotation and is acted upon by nothing but the
click; between clicks the exchange runs one way, from the clock to the
records, like a parametric drive whose own energy is not booked. What
IS conserved: each family's whole where the clock is static (9.35 (2),
exact to 10^-15); the count of quanta, the content, at every click; and
the family of clicks' own form under its own step away from the held
Nodes. The size: for a change of one unit of the clock at a Node the
record's share there moves by 1 / (Gamma + c) of itself, 10^-6 at Gamma
= 10^6, below every pin of the eighteen; a static field moves nothing.
A law in which the records' energy sources the clock (gravity by energy
and not by counted quanta alone) would need the field to read the
families, a coupling beyond the click, and stands outside the adopted
law under its own identity if ever wanted.

**(5) THE SHELL READS THE BODY AND THE CLICK THROUGH THE FAMILY OF
CLICKS (the model owner's record 1984 through the Boss; his aim: at each
Node of a body's shell, to know whether this is a body and whether it
clicked, through the family of clicks).** (a) WHETHER THIS IS A BODY,
through the family: a body's Nodes hold the family's level at the
content M and outside it falls as about M R / r (9.45 (2)); the mark at
a shell Node is the LEVEL STEP across its outward Links, its own level
held and not moving against a neighbour's lower and moving level, not a
current (a static field has no current: now = before at every Node, so
the Wronskian is 0). It is a local reading, right, for a body whose
content is not 0; a body with no content (a detector before its first
click, an emitter whose stock is spent) is marked only by its
eigenvector, (1). (b) WHETHER IT CLICKED: at a click the held level
steps by one on all the body's Nodes in that interval, so every Node of
the body, the shell included, sees the step at once, and the Nodes
outside see it arrive a Link per interval later; right, local. (c) WHEN
IT CLICKS, the trigger. THE GIVING END CAN BE LOCAL AT EVERY NODE: the
tick's count is the same at every Node (T2); the period each Node reads
from its own levels; and the one body-wide number, the residue, can ride
the click's own write: at the click the body's Nodes receive, in the one
act that already writes M on all of them, the residue u read at that
interval at the first shell Node (the first shell Node's remainder at
the click, on the body's wheel). Then every Node of the body holds (M,
u), counts its own intervals against (2 u + 1) P / (2 W) with its own P,
and all reach the rung at the same interval by construction; no sum, no
tally, and no fraction moved (the remainders stay where they are; u is
a reading of one of them, whole). The born record's residue is the same
u. THE TAKING END CANNOT: the passing record's chance to click at this
body is its share of the record's whole gathered through ALL the body's
Ports (Born's rule, 9.25 (3)); a threshold at each shell Node on its own
Ports' inflow would make the body click on the largest single Node's
share and not on the body's, and Born's rule would fail at every body of
more than one Node; so the taking end's gather stays one sum over the
body's Ports per interval, the body's one act at its own scale, as the
deletion is; a tally passed along the Links would give the same sum
after the diameter's delay and is a register in transit. (d) "THE
FAMILY RECEIVES THEM, MAYBE", of the remainders: the reading that moves
no fraction between families (records 1962 (2) and 1983) is (c): what
the family's write at the click carries to the body's Nodes is the
residue, a whole reading of one remainder, and never a remainder itself;
the remainders stay at their Nodes and the step alone moves them. With
(c) the reading of (2) above changes in one word: the residue is read at
the click, not after the first advance, and written with the content on
the body's Nodes.
Two readings of Nature24's build of the Node clock (head e84ddba4), for
the record: (a) the declared norm T of a body's own record is one
period's action at its initial content; after births at a lower content
its share is smaller by about (M_0 - M) times the kinetic part over
Gamma T, 10^-5 on the light clock, the rung's crossing moving by a
hundredth of an interval at most; an exact T per excitation would be a
register the law does not keep, so the declared T stands. (b) After a
birth the wall at the body's Nodes falls from 3 den (Gamma + M) to 3 den
(Gamma + M - 1), and a kept remainder at or above the new wall (the
chance about 1 / Gamma per Node) is absorbed by the next division, the
invariant restored after one advance: lawful, the remainder re-formed
below the wall it has. And the generator's mode is the mode of the
operator the body sees (9.22 (7a)), so the generator carries the Node
clock at the body's declared initial content on its Nodes; without it
the body's record starts off the clocked mode by about M / Gamma of its
amplitude (6 x 10^-5 at M = 64), a transient below every pin.

### 9.46 The body record: a body held as one Node in the engine, its parameters, its step and its equivalence test (the model owner's word of 2026-09-25 in the mathematician's session: "already now, because it is generic; a body holds real parameters, and then it is a special Node in the simulator; it can be checked that it is equivalent"; DERIVED; a host form under its own identity, its gate the equivalence below)

**(1) WHAT A BODY IS, AS DATA.** A body's own standing record is phi_i
cos(omega t): a fixed integer profile times ONE rotation (D4, T2). So a
body is one Node's worth of state and a stored shape. THE BODY RECORD
holds: its family and its pair on its Nodes; its Nodes S (the declared
region) and its profile phi on them, the generator's integers, read and
never stepped; its clock pair [num_c, den_c] with 2 cos omega = num_c /
den_c, the generator's; its norm T (one period's action, 9.17 (7) (e));
its stock; its content M; its residue u; and ITS ROTATION (a, b, r): two
levels and one remainder. Nothing else. It is a special Node: a Node
with a shape.

**(2) ITS STEP.** The rotation moves by the two-term rule with the clock
of its content: den_c (Gamma + M) a' + r' = (num_c Gamma + 2 den_c M) a
- den_c (Gamma + M) b + r, 0 <= r' < den_c (Gamma + M) (the form of the
wall 3 den (Gamma + M); under the constant wall ruled in 9.50 (8) it is
den_c Gamma a' + r' = (num_c (Gamma - M) + 2 den_c M) a - den_c Gamma b
+ r, 0 <= r' < den_c Gamma, the same wall at every content and the
record's own backward run exact through its clicks); this is 2 cos
omega' = (Gamma / (Gamma + M)) 2 cos omega + 2 M / (Gamma + M), which is
1 - cos omega' = (Gamma / (Gamma + M))(1 - cos omega), the Node clock's
rotation of 9.35 (2) in one coordinate; all integers, one division, the
remainder kept. Its wheel is den_c (Gamma + M) over the gcd of the
step's coefficients, the pair's own at M = 0. Its share per interval is
the invariant of the two-term rule, e = D (a^2 + b^2) - (num_c / den_c)
a b in the rule's units, constant in time; its tick is the count t
against T: the click at the first t with 2 W t e >= (2 u + 1) T, the
same interval as the lattice body's at every Node (9.32 (b)). Its
residue u is its own remainder r on its wheel, read at the click and
carried (9.44 (5) (c)); the born record's residue the same u.

**(3) ITS INTERFACES TO THE GameBoard, unchanged in form.** (a) THE GIVING
END: at its tick the born family's eigenvector on S times the character
is set on the GameBoard's Nodes of S (9.37 (2)), the stock and M fall by
one; the body's own rotation continues (9.43, no reseed). (b) THE TAKING
END: a passing record's inflow through the Ports of S is gathered on
the GameBoard as now; at its click M rises by one and the body record's
clock changes with it (T4). (c) THE FAMILY OF CLICKS: the level held at
M on the Nodes of S, as 9.45 (2). (d) THE PAIR REGION on S stays on the
GameBoard, so every passing record of every family, the body's own
family included, moves through S by the lattice step with the well in
place; the body's own rows are NOT on the GameBoard, and by the
linearity of the step per family (D2) no passing record ever needed
them: a record's motion through S does not read the standing record
there, and a click counts per record. (e) The tail rule (9.22 (7a) (i))
and the two-bodies check are read on the stored profile as now.

**(4) WHAT IS NOT BIT-EQUAL, AND THE EQUIVALENCE TEST (THE GATE).** The
body record's rotation and its remainder run on the two-term rule with
the wall den_c (Gamma + M), the lattice body's on the six-neighbour
rule with the wall 3 den (Gamma + M) at every Node: the rotations agree
as rationals (the same clock pair), the remainders are different
integers on different wheels, so the residues' ORDER differs and the
drift within the rounding differs (Niven, 9.26 (4)). The law's claim is
statistical there (9.43), so the equivalence to require is: (i) THE
TICKS: the distribution of the body's cycle lengths, the mean P / 2, no
runs of one-interval cycles beyond a fair draw's, the residues spread on
the wheel (the chi-square within its bound), read on both forms over the
same number of births; (ii) THE ROTATION: 2 cos omega' equal as
rationals at every content M, bit for bit; (iii) THE BORN RECORDS: the
same rows set on S at each tick (the same eigenvector, the same
character), so every pin of the eighteen that reads the born light
(the light clock's 300 +- 9 and 250 +- 8 first) unchanged to its band;
(iv) THE TAKING END identical by construction (the GameBoard's own
gather); (v) THE FAMILY OF CLICKS' field identical (the same held M).
A body record that passes (i) to (v) replaces the lattice body under the
world key `body_record`, off by default; one that fails is refused
naming the test.

**(5) THE HOST COST AND THE THREE TESTS.** The step of the body's own
family over the N Nodes of S is gone; the rest of the GameBoard's cost
is unchanged; in a world of many bodies (a crystal of atoms, 9.31) the
cost is linear in the bodies and not in their Nodes. Generic: one
primitive, a Node with a shape, declared integers, no family name.
Vector: the two-term rule is verb (D) with the remainder kept, no root,
no float. Local: the body record reads its own state and its Ports on
S; its one non-local act is the click's, as before. It is the owner's
"the body is one Node" (9.38 (9), 9.40 T2) made an engine form, and it
is what the owner asked to build now.

**(6) WHAT BODIES DO TO EACH OTHER, AND WHAT THEY DO NOT (the model owner's
observation of 2026-09-25 in the mathematician's session: "our simulator
declares that everything is bodies; there is no resistance between
bodies").** Right, and it is the law's own content, not the body
record's. Two bodies act on each other in four ways and no other: (a) BY
CLICKS: a record born of one and taken by the other moves one quantum,
whole, with its labels (9.37, 9.40 D5); this is the only collision the
law has, an absorption, at the taker's share by Born's rule. (b) BY THE
FAMILY OF CLICKS: each body's content slows every clock around it and
bends every record toward it (9.41 (4), 9.45), an attraction and never
a repulsion. (c) BY PASSAGE: a moving record of one body's family
crosses another body's well transparent and lensed (9.29), never
stopped. (d) BY OVERLAP: two bodies whose modes overlap are one
eigenvector, one body with one click (9.32 (c)); they merge, they do not
push. THERE IS NO CONTACT, NO REPULSION AND NO EXCLUSION in the law:
nothing keeps two bodies apart, and two bodies at one place superpose.
A repulsion needs a label with a sign and a rule that reads it, a
charge, which the algebra does not have (the exchange hypothesis of 9.27
(D) is the place it would enter, under its own identity); a contact
force is that or nothing. None of the eighteen rows has two bodies
meeting (the mirrors and slabs are regions, the wells declared apart),
so no pin asks for it; the crystal rows (9.31) hold their bodies apart
by declaration. The body record changes none of this: it holds the four
ways as the lattice body does, and has no fifth.

**(7) A COMPOSITE BODY RECORD ON THE GameBoard: ITS MASS, ITS MOMENTUM, ITS
PLACE (the model owner's question of 2026-09-25 in the mathematician's
session: "for such a special Node, its mass as the mass of all its parts
and its momentum as the momentum of all its parts; how would we put such
a Node into our board naturally?").** (a) MASS, TWICE. The law has two
things called mass. THE CONTENT M, the quanta held, is ADDITIVE: a body
made of parts holds the sum of its parts' contents, and that sum is what
the family of clicks reads, so the gravitational mass of the composite
is the sum of its parts', exactly. THE REST ROTATION omega, the pair's
and the well's, is NOT a sum: a composite is one eigenvector on the union
of its parts' Nodes (9.32 (c), two wells whose modes overlap are one
body), and its rotation is the composed operator's top eigenvalue, which
the generator computes once; parts that do not overlap are not one body
at all but several, each with its own record. So a composite body record
carries one M (the sum) and one clock pair (the union's eigenvalue).
(b) MOMENTUM. A moving body is its eigenvector times the character of one
**K** (9.17 (6a), 9.31 the moving name): all its Nodes share the one
**K**, so the composite's momentum is the one **K** with the content M
behind it, M **K** in the exchange hypothesis's units (9.27 (D)),
additive over parts that share the character and undefined for parts
that do not (they would not be one record). Its pace is the dispersion's
at that **K** under its clock, dω/dK, carried as the pace pair per axis on
an accumulator (9.31 (2)), the hop of p Links every q intervals. (c) THE
INSERTION, NATURALLY: a body record is placed on the GameBoard by its
corner and its extents, its pair region written on S there, its profile
phi on S, its clock pair the generator's for that well AT THAT **K** (the
moving mode's clock), its T, stock, M, u, its rotation (a, b, r) at phase
0 and remainder 0 (the load's one write), its **K** and its accumulators;
each interval its rotation steps by (2) and its accumulators by the pace;
when an accumulator carries, S and its pair region hop one Link on that
axis (the moving name), its held M with them (the family of clicks'
source moves, and the field follows at one Link per interval, a retarded
potential); its Ports are those of S where it stands, its born rows go
on S where it stands. Nothing else is declared: a composite is the same
body record with the union's Nodes, the sum's content and one **K**; the
tail rule and the two-bodies check hold on its profile as on any
body's. What the law does not give a composite is what it gives no
body: binding between its parts other than the declared well (9.39
(3)), contact and repulsion ((6)).

### 9.47 The law, derived: the chain of the adopted statements, each marked (the model owner's word of 2026-09-25 through the Boss, record 1987: "everything we do must be backed by the algebra and follow from it, the family of clicks, the clock and a body represented by something smaller included"; every statement marked PROVED, DERIVED, COMPUTED, ADOPTED or OPEN, with its section; Nature24 names the section each commit implements)

**(1) THE NODE AND ITS NUMBERS.** A Node carries, per record of each
family, two integer levels a_i and b_i and one remainder r_i, kept at
the Node through every click (D1; the remainder the Node's: ADOPTED,
records 1962 (1) and 1966); per family a pair [num, den] per declared
region, the family's rest rotation cos omega_0 = num / den (8.1,
DEFINITION); and the level c_i of the family of clicks, which is its
clock (e_i, f_i) = (Gamma, Gamma + c_i), Gamma one integer of the world
(9.45 (1), ADOPTED, record 1982). The remainder moves on the multiples
of the gcd of the step's coefficients below the wall 3 den f_i, so the
wheel at the Node is W = 3 den f_i over that gcd, the pair's own where
c_i = 0 (9.19 (4), 9.42 (5): DERIVED). Nothing else is at a Node (9.40
D6: ADOPTED as the frame, record 1967).

**(2) THE FOUR FAMILIES.** Light, pair [1, 1]; the matter families, each
with its declared pair; and the family of clicks, pair [1, 1], whose
level is the clock (9.45; ADOPTED, record 1982; the owner's constant at
most four). Every family is one primitive under the same step; no
family name enters any rule (the generic test, skills/workflow.md).

**(3) THE STEP.** At every Node, per record, 3 den f a' + r' = e num S_6
(a) + 6 den (f - e) a - 3 den f b + r, 0 <= r' < 3 den f (D2). It is a
bijection of (a, b, r) (9.26 (3) (a): PROVED); separate per family, no
cross term (9.34 (B): ADOPTED). The share E_i = 3 den f (a^2 + b^2) -
num Gamma a (S_6 b)_i - 6 den c_i a b and the current J_ij = num Gamma
(a_i b_j - b_i a_j) satisfy, at every Node and on every set of Nodes,
E after minus E before equals the sum of the currents through the Ports
(T1, 9.35 (2), 9.38 (3) (b): PROVED; exact to 10^-15 on the float law
and to the rounding on the integer law: COMPUTED). Where the clock is
static the whole I is invariant (PROVED); where the clock changes, the
record's share changes by 3 den (f' - f)(a^2 + b^2) - 6 den (c' - c) a b,
a one-way exchange with no conserved total of the families together, by
the law's choice (9.45 (5): DERIVED). The clock's rotation: 1 - cos
omega' = (Gamma / (Gamma + c))(1 - cos omega) (9.35 (2): PROVED;
COMPUTED on the engine to 10^-5, 9.45 (5)). The family of clicks' own
step runs plain, e = f for itself (DERIVED, 9.45 (2)); at a body's
Nodes its level is held at the content and elsewhere it moves by the
plain step (9.45 (2): ADOPTED); its static part around a held content
is the discrete Coulomb potential (9.41 (3): COMPUTED), so around a mass
every clock reads Newton's potential (9.41 (4): DERIVED); a pair below
[1, 1] would screen it (DERIVED), which is why its pair is [1, 1].

**(4) A BODY.** A body is the support of an eigenvector of the family's
operator with its declared well, a standing record (D4: DEFINITION).
Its Nodes carry one time: every current of a standing record is 0 and
its share is constant at every Node, so the count t / P is the same at
one Node, at the shell and at all (T2, 9.32 (b): PROVED; COMPUTED 600
of 600 cycles, 9.38 (4)). The mark of a body at a Node is zero current
with a constant share, local (9.44 (1): PROVED). Two bodies whose modes
overlap are one eigenvector and one body (9.32 (c): PROVED). A body
needs a declared well: the uniform operator has no eigenvector of
finite support, and the clock lowers nothing for light and 10^-8 to
10^-4 for matter at Gamma = 10^6 against thresholds of 10^-3 to 10^-1
(T3, 9.39 (3): COMPUTED). A body's content is the sum of its parts'
and its rotation the union's eigenvalue (9.46 (7): DERIVED).

**(5) THE SMALLER REPRESENTATION, AND THE PROOF THAT IT GIVES THE SAME
CLICKS.** A body is represented by its content M, its residue u read at
its first shell Node in the declared order, and one rotation (a, b, r)
with its stored profile (9.44, 9.46). THE PROOF, in four parts. (i) THE
GIVING CLICK'S INTERVAL: for a standing record the share is constant
at every Node and the count against T = P times the share is the same
count, so for a given u the click falls at the interval ceil((2 u + 1) P
/ (2 W)) whether it is read at one Node, at the shell, at all the Nodes,
or on the one rotation of 9.46 (2), which has the same P as a rational
(T2: PROVED; 9.38 (4) and 9.46 (4) (ii): COMPUTED). (ii) THE RESIDUE:
with the reseed retired, the remainder at any one Node of the body is a
fair draw on the wheel in the sense the pins need, the residues spread
with no run beyond a fair draw's and the mean cycle P / 2 (9.43 (3):
COMPUTED, 3000 cycles); the pins are marginal shares (9.22 (8)), so
which Node is read is a convention; the ORDER of the residues is a
deterministic map that differs between any two representations (T5:
DERIVED), so the equivalence is in distribution and not bit for bit,
which is all the law claims (9.43 (2)). (iii) THE TAKING CLICK: gathered
through the body's Ports on the GameBoard in every representation, the
same integers (9.38 (2), 9.46 (3) (b): identical by construction). (iv)
THE BORN ROWS: the born family's eigenvector on the body's Nodes times
the character, set at the tick, the same in every representation (9.37
(2), 9.46 (3) (a): identical by construction). Hence the same clicks:
the same intervals for the same residues, the same residue statistics,
the same takings and the same births. OPEN: the equivalence test of
9.46 (4) on the engine, body record against lattice body on one world,
not yet run because the body record is not yet built; until it passes
the body record is a host form under its key and the lattice body the
reference.

**(6) THE TWO ENDS OF THE CLICK.** A click is X_S (the taking end: the
record's rows to 0 on its support, M + 1 on S, r unchanged) or X_S^T
(the giving end: the born family's eigenvector on S times the character
set, the stock and M down one, the body's own levels, phase and
remainders left as they are), applied once at one interval on all the
Nodes of one set, and nothing else (D5: DEFINITION; ADOPTED, records
1962 (4), 1963, 1964, 1982). A change of a body's integers alone sheds
nothing of the born family (9.37 (1): PROVED), so the giving end must
set the rows and no wave is written (9.37 (2): DERIVED; the born mode's
flux check 0.9997 on the algebra and 1.00023 on the engine: COMPUTED).
The clock under a click changes through the content alone, by (Gamma +
M) / (Gamma + M +- 1) (T4: PROVED). The giving trigger is local at
every Node, the residue riding the click's write to all the body's
Nodes (9.44 (5) (c): DERIVED); the taking trigger is one gather over the
body's Ports, by Born's rule (9.25 (3): PROVED; a per-Node threshold
would break it: DERIVED). One quantum, one click (9.25 (2): PROVED).
The record's ending on all its Nodes at once is the one non-local act
(ADOPTED, record 1888) and is required by Bell's row: a spreading
ending would let two far bodies take one quantum or bound the
correlations at the local value (DERIVED, in the mathematician's
session). The remainder rule: an exact record never clicks (T6: ADOPTED,
record 1962 (3)).

**(7) THE SURFACE RULE.** The shell of a body is its Nodes with a Port;
every click is read there, the passing record through the Ports and the
own record at the shell's Nodes, one threshold (9.38 (2): DERIVED;
ADOPTED, record 1982); the body's Gauss law makes the shell read the
body's whole and nothing twice (9.38 (3) (b): PROVED); the tick at the
shell equals the tick at all the Nodes (9.38 (4): COMPUTED, 600 of 600).

**(8) A DETECTOR IS A BODY.** A detector is a matter well's bound mode
with its held quanta as content (9.42 (1); ADOPTED, record 1974). The
least body of side 3 in [800, 809] has its pair inside from about [800,
713] to [800, 686] (9.42 (2): COMPUTED); a slab binds at any depth
(DERIVED); no rich Node is needed, the taking reads the passing record's
residue (DERIVED). Its own record changes at a click by (Gamma + M) /
(Gamma + M + 1) (T4: PROVED). Pixels stand four Links apart so that no
two merge (9.42 (4): DERIVED from 9.32 (c)). OPEN: the eighteen's files
with their detectors as bodies and their pins recomputed under the same
rule, on the new engine.

**(9) THE RESEED RETIRED.** Under a reseed the residues' order is u -> u
+ S(t(u)) with S(1) the profile's first-step rounding at the read Node,
a host constant (9.43 (2): DERIVED; -1 on the engine, -1147 and +337 in
two roundings: COMPUTED), which would make a closed body's births depend
on the profile's precision; with the body's own record left as it is,
the phase carries and no run forms (9.43 (3): COMPUTED; ADOPTED, record
1982). The light clock's interval pins are expected unchanged: OPEN
until read on the engine without the reseed.

**(10) WHAT STANDS OUTSIDE THE LAW.** A well from the law itself: no
(9.39 (3): COMPUTED). A conserved total of the families under a moving
clock: none, by choice (9.45 (5): DERIVED). Contact, repulsion,
exclusion, charge: none (9.46 (6): DERIVED); the exchange hypothesis
(9.27 (D)) is where a charge would enter, under its own identity. Dark
matter: not given, the field is Newton's exactly (9.41 (4): DERIVED).
Light with light: not given (9.41 (4) (c): DERIVED). The family of
clicks carries no quantum, no residue and no click of its own (9.45 (1):
ADOPTED); its unit is the quantum and its reach in integers M R Links
(9.45 (2): DERIVED), a declared resolution. The body record (9.46) is a
host form under its key, its gate the equivalence test: OPEN. The
generator's mode under the clock at the body's initial content: a build
item (9.45 (5)): OPEN on the engine. Every statement above not marked
OPEN follows from (1) to (3) and the adopted definitions; the runs of
9.38, 9.39 and 9.43 are computations of the algebra and add no rule.

**(8) A BODY SEATED AT ONE NODE OF THE GameBoard (the model owner's
question of 2026-09-25 in the mathematician's session: "then it can be
put in as one small Node that stays a Node on the board, and from that
Node we read its clicks, instead of three by three by three; will it
work?").** Yes for three of its four offices, no for the fourth, and the
fourth has a form. Let the body record of (1) be SEATED at one Node of
the GameBoard, its seat: its rotation, its content, its residue and its
stock live there. (a) AS A HOLDER OF CONTENT, the source of the family of
clicks: the level held at the seat, a point source; the field beyond a
few Links is the same 1 / r (9.41 (3)), the near field that of a radius
of one Node instead of the cube's 1.4; no pin reads the near field.
WORKS. (b) AS ITS OWN CLOCK, the tick: the rotation of (2) at the seat,
the residue its own remainder, the count the same interval as any
representation ((5) of 9.47). WORKS. (c) AS A TAKER: the seat's six
Links are its Ports; a passing record offers it the inflow through six
Ports instead of the cube's fifty-four, about one twenty-seventh of the
cube's share, so a seated detector takes fewer records by that factor
and the rest go on to the slab; the PATTERN across a screen of seated
pixels is unchanged (each pixel's share is the local intensity, the
ratios between pixels the same), the COUNTS are rescaled, so the pins'
counts are recomputed and their form is not. WORKS, with its pins
recomputed. (d) AS A GIVER: the born record's band is set by the extent
it is written on, delta k about 2 pi / L (9.17 (6a), the train); a
record born on one Node is broadband, every wavelength at once, which
is the one-Node birth retired at 8f224288 and would move every pin that
reads a wavelength (the two slits' spacing, Mach-Zehnder's dark port,
the light clock's interval). So a seated emitter WRITES ITS BORN ROWS ON
A DECLARED EXTENT around its seat, the born family's eigenvector on
those Nodes times the character, as now; its own rotation sits at the
seat and its births use the extent. That is the form: A SEAT AND A
BIRTH EXTENT; a detector, a holder and a clock body need the seat alone,
an emitter the seat and the extent. The pair region on the GameBoard is
needed only where a record of the body's OWN family must pass through
it (lensed, transparent); the eighteen's passing records are of other
families, so a seated body carries no pair region there. Under these
two caveats it works, and (4)'s equivalence test decides the numbers.

### 9.48 The charge: a sign on the quantum and a signed field, so that bodies repel as well as attract (the model owner's decision of 2026-09-25 in the mathematician's session: "I want to add this feature; it seems important to me"; DERIVED from 9.45 by one sign; the three tests; the numbers; supersedes the "no charge" line of 9.46 (6) and 9.47 (10); for the Boss's record and Nature24's build after the family of clicks and the body record)

**(1) THE SIGN ON THE QUANTUM.** Every family declares a charge q in {-1,
0, +1} per quantum: light 0, each matter family its own (an electron
family -1, a proton family +1, a neutral family 0). The label passes in
the click, whole, as every label does (9.36, 9.40 D5): at a taking the
taker's charge Q rises by the quantum's q, at a giving the giver's Q
falls by the born family's q (a body giving light, q = 0, keeps its Q).
A body's charge Q is the sum of the signs of the quanta it holds, an
integer of either sign, held at its Nodes as its content M is.

**(2) THE FAMILY OF CHARGE.** A fifth family, the family of charge: pair
[1, 1]; two levels and a remainder per Node; its level d_i held at a
body's Nodes at Q (signed) and moved elsewhere by the plain step with
the world's one border; its own step plain (e = f for itself); no
residue, no ladder, no click and no quantum of its own; its unit the
charge quantum; its transients unbooked, reflecting and dying in the
rounding; its static part around a held Q the discrete Coulomb potential
Q R / r (9.41 (3)), of either sign. Everything of 9.45 (1) and (2) with
Q for M, and one thing more, the strength: a declared integer Lambda of
the world, the charge's weight in the clock, below.

**(3) THE READING, ONE SIGN.** The clock a record of charge q reads at a
Node is (e_i, f_i) = (Gamma, Gamma + c_i - q Lambda d_i): the family of
clicks' level as before, and the family of charge's level times the
strength, WITH THE SIGN OPPOSITE TO THE READER'S OWN. Then: a record
near a body of its own sign sees q Lambda d > 0, f below Gamma + c, a
FASTER clock, a hill, and is bent away (9.29: a hill repels, +13.1
Nodes computed); a record near a body of the opposite sign sees a
slower clock, a well, and is bent toward it (9.29: a well attracts,
-14.8 Nodes); light, q = 0, reads no charge at all and is bent by the
content alone, as in nature. The step at the Node is D2 with this f,
one more product of integers in the self term; the share, the current
and Gauss (T1) hold with this f as with any clock field; the wheel at
the Node is the rule's with this f. The three tests: generic (one
primitive, a signed label and a field, no family name in the rule);
vector (a product q Lambda d_i a_i at the Node, the share's own verb;
sums; one division with the remainder kept); local (d_i at the Node).
The loader's bound: f_i > 0 everywhere, so Lambda |d_i| < Gamma + c_i:
the charge's hill can hasten a clock at most to the vacuum's, never
stop it.

**(4) WHAT IT GIVES, AND THE NUMBERS.** Coulomb's form: the field Q R /
r, the bending as its gradient, the force falling as 1 / r^2, like signs
repelling and unlike attracting, light untouched: DERIVED from (2) and
(3) by the same steps as Newton's potential in the clock (9.41 (4)).
THE STRENGTH AGAINST GRAVITY: per quantum, Lambda times the content's
effect; with Gamma = 10^6 and f > 0, Lambda at most about 10^6 / |d| at
the body's Nodes, so the ratio of the charge's pull to the content's is
at most of the order of 10^5 to 10^6 on the eighteen's integers, not
nature's 10^40; a larger ratio needs a larger Gamma and a smaller
amplitude under int64 (the wall 3 den (Gamma + c) times the amplitude
below 2^63), a declared trade, and no pin of the eighteen asks for it.
THE WELL FROM THE LAW, for the first time: a charge of the opposite
sign makes a well of relative depth about (1 - p) Lambda |d| / (p
(Gamma + c)) for a matter record (9.39 (3), 9.41 (4) (b)); against the
computed thresholds (side 32: 0.002 to 0.003; side 8: 0.010 to 0.020;
side 3: 0.10 to 0.15) a body of side 32 is bound by an opposite charge
at Lambda |d| about 0.25 Gamma, a body of side 8 at about 1.5 Gamma,
which the bound f > 0 forbids, and a body of side 3 never; so under
this law an electron-like record binds to a proton-like body as a mode
of the charge's own well of side 32 or more, and the declared well of
[800, 801] in [800, 809], depth 0.010, is matched by Lambda |d| about
0.9 Gamma: a computed row, the atom, once the family is built; the
declared wells of the eighteen stand as they are.

**(5) THE PINS AND THE ENGINE.** Every family of the eighteen declares q
= 0, so the family of charge is 0 everywhere and the engine is bit for
bit as without it: no pin moves. The cost: two levels and a remainder
per Node more, one product more in every record's self term. In the
engine: the charge label per family; Q per body, moved at clicks with
the label; the fifth family on the scaffold of the family of clicks
with Q for M and the sign in the reading; Lambda a world key; the f > 0
bound at load; a seated body record in motion needs one rule more, its
pace changed by the field's gradient at its seat (9.29's ray equation
as a line; a record on the lattice needs none, the step refracts it).
The owner's constant of four families becomes five. What stays open:
the atom as a computed row; the strength's scale as a declared trade.

**(6) THE FAMILY OF CLICKS AS BUILT (Nature24's head 1b3c7b0f): FOUR
RULINGS.** (A) THE INVERSE WHERE THE CLOCK FALLS. The step is a bijection
of (a, b, r) for a fixed wall (9.26 (3) (a)); under the Node clock the
wall at a Node is 3 den (Gamma + c) and moves with c. Where c does not
fall the joint step still inverts bit for bit. Where c falls between
two intervals, a remainder at or above the new wall and one below it
give one total, and the inverse cannot tell them apart: about (c - c')
/ (Gamma + c) of the states per unit of fall, 10^-6 at Gamma = 10^6
(COMPUTED by Nature24: exact return before the first fall, a return
within 16 units of 2^20 after it). THE RULING: THE LEVEL MAY FALL, and
the law keeps conservation over bit-exact reversibility there, by its
own structure: the content must sit in f (the self term and the wall)
and not in e, because a per-Node e makes the neighbour coupling
asymmetric and the conserved form of T1 is lost, so the wall must move
with the content; a clock read from a level that never falls (a running
total of clicks, a monotone rule) would keep the giver's clock slow for
ever after each birth, a physical change the owner has not made. The
property (4) of 9.20 (B) is restated: the joint step inverts exactly
wherever the clock has not fallen at a Node with a record, and loses at
most one remainder's worth of state per unit of fall where it has; the
tests assert that. [SUPERSEDED by 9.50 on the owner's requirement of
2026-09-25: the wall is the constant 3 den Gamma and the clock enters
the numerator, (e, f) = (Gamma - c, Gamma), and the inverse is exact
where the level falls too; the reason given here, that a per-Node e
loses T1's conserved form, was WRONG: the form exists with the Node
terms weighted by 1 / e_i and the Link current unweighted, 9.50 (9).]
(B) THE FIELD AT UNIT LEVELS. With one unit per
quantum (9.45 (1), the owner's "the clock as its amplitude") a body of
1 to 64 quanta makes a field that is the rounding's walk within a few
Links and nothing beyond (13 units at most on the small world, 9 in the
emitter chain's vacuum: COMPUTED by Nature24), not a resolved
potential; this is what the clock's own resolution allows, since a
clock (Gamma, Gamma + c) reads shifts of 1 / Gamma and the potential M
R / r is below one quantum beyond M R Links (9.45 (2)); the walk's
jitter is at most 13 / Gamma of the clock, below every pin. THE
RULING: the step at unit levels is the law's and one click writes one
unit; a resolved potential comes from a heavy body (a content of 10^4
quanta resolves the 1 / r to 10^4 R Links), which is how the gravity
row (9.22 (8a)) is to be read, and not from a finer unit, because a
unit U per quantum multiplies the wall (Gamma U + c) against the
amplitude under int64 (at 2^28 and Gamma = 10^6 there is no room for U
above 3). (C) THE CLICKS REACH THE BIRTHS. A click's content spreads
from the taker as the field, reaches an emitter's Nodes at one Link per
interval, moves its rounding, and so moves the residues of its later
births with where the click landed (COMPUTED by Nature24: the residues
agree bit for bit until the field arrives, and differ after). THE
RULING: THIS IS THE LAW: the field is the memory of every click,
causal, at light's pace, and it is the back-action of the board on a
body's residues that 9.19 (4e) once assigned to the retired coupling,
now lawful and one-way; the residues' statistics are unchanged, their
order is not, which is all the law claims (9.43). The asymmetry Nature24
read (the content held at a set's first body, row 0 against row 6) is
the set's write for a set of several bodies, and goes with (v), one
body per detector. (D) e = f FOR THE FAMILY'S OWN STEP: confirmed, the
plain step, the field linear. THE GATE on 1b3c7b0f, with the rename
601a3741 (names only): CONFIRMED as 9.45 with these four rulings; the
three pieces no section stated are now stated: the load bound's factor
2 on the world's content is host arithmetic; the click's content held
at a set's first body goes with (v); the kept remainder above a shrunk
wall is 9.45 (5).

**(9) TWO CONVENTIONS FOR THE BUILD (Nature24's plan, the Boss's record
1992).** (a) THE CLOCK PAIR: the nearest pair [num_c, den_c] to the
iterated mode's 2 cos omega at a declared denominator of the world (the
generator's, under the stamp); the equality of (4) (ii) is read as: the
lattice body's rotation, (a_next + a_before) / a_now at any of its
Nodes, agrees with num_c / den_c within the loader's residual bound at
every content M, the clock's transform applied to both; a bit-equal
rational does not exist for a lattice body, whose rotation is the
integer profile's to the rounding. (b) THE SHARE AND THE NORM: e = den_c
(a^2 + b^2) - num_c a b is the invariant of the two-term rule (a' =
(num_c / den_c) a - b leaves it fixed: PROVED in one line); T is the
generator's declared norm at the body's initial content, one period's
action, an integer, unchanged with M as 9.45 (5) rules (the drift 10^-5,
no register); the rung is the first t with 2 W t e >= (2 u + 1) T. (c)
THE ORDER, confirmed: (iii) the reseed retired on the lattice body, so
the reference is right; the body record under its key with the
equivalence test; (v) the detectors as seated body records with their
pins recomputed blind; then the special paths; (iv) folded into the body
record, its taking end being the engine's one gather over the Ports
already and its giving end at the seat equal to the shell's by T2.

### 9.49 The build, all together, and the test of each piece (the model owner's word of 2026-09-25 in the mathematician's session: "go for everything together, with tests that it works"; the order of records 1992 and 1985; each piece with the test that gates it; for Nature24's build and the Boss's record)

**(1) THE RESEED RETIRED (9.43), on the lattice body.** Build: at a birth
the body's own record is left as it is; the residue read at the click
at the first shell Node in the declared order, written with the content
on the body's Nodes; the born record's residue the same u. TEST: 3000
births of the emitter chain, the cycle lengths in order: no run of
one-interval cycles beyond a fair draw's (the longest at most 3), the
mean cycle P / 2 within 3 percent, the residues' chi-square on 20 bins of
the wheel below 30.1; the light clock without pins: the mean interval
and the least wait inside 300 +- 9 and 250 +- 8, as readings.

**(2) THE GENERATOR UNDER THE CLOCK (9.45 (5)).** Build: the mode of the
operator with the Node clock at the body's declared initial content on
its Nodes. TEST: the body's record on the engine starts within the
loader's residual bound of the clocked mode (no transient above 10^-5
of the amplitude); the excitation norm read on the engine equal to the
declared T within 10^-5.

**(3) THE BODY RECORD (9.46), under `body_record`.** Build: (1) to (3) of
9.46 with the conventions of 9.46 (9). TEST, the equivalence of 9.46 (4)
on three worlds: (i) the emitter chain, 3000 births on both forms, the
cycle lengths equal in distribution (the mean within 3 percent, the
chi-square of the residues on both below 30.1, the longest run at most
3 on both); (ii) the clocked rotation of the body record equal to the
lattice body's read from its levels within the loader's bound at every
content; (iii) the light clock, the same born rows on the body's Nodes
at each tick bit for bit, 300 +- 9 and 250 +- 8 on both forms as
readings; (iv) the boxed clock of side 20, the block's count over 3000
intervals equal on both forms, the host time beside; (v) the family of
clicks' field identical on all three. A form that fails any one is
refused naming the test.

**(4) THE DETECTORS AS SEATED BODIES (9.42, 9.46 (8)), the eighteen's
files.** Build: every detector a seated body record with its six Ports
and its held content; every emitter a seat with its declared birth
extent; the tests' wells 56 Links from a face. TEST: the pins recomputed
blind on the new files by the generator's runs, then the eighteen run
against them; the screens' patterns unchanged in form (the two slits'
visibility 0.95 within its band, the spacing 53.2 within 2 percent), the
counts rescaled by the seat's share; Bell's S above 2.5; Mach-Zehnder's
dark port at most 1 in 100.

**(5) THE CHARGE (9.48).** Build: the charge label per family, Q per
body moved at clicks, the family of charge on the family of clicks'
form with Q for M, the reading with the sign opposite to the reader's,
Lambda a world key, the bound f > 0 at load. TEST: (i) every registered
file at q = 0 for every family: the engine bit for bit as without the
family (the chain digests unchanged); (ii) a charged world: two seated
bodies of like sign 40 Links apart, a record of one family with q = +1
sent between them, bent away from the like body by the ray equation's
sign (the centroid moves away, computed against 9.29's hill, +13 Nodes
at the declared Lambda scaled); a body of the opposite sign, bent
toward; light between them untouched to 10^-6; (iii) the Coulomb form:
the field's level around a seated body of charge Q at 2, 4, 8 Links in
the ratio 4 : 2 : 1 within the rounding.

**(6) THE EIGHTEEN, RUN.** After (1) to (5): every row of 9.22 (8)
against its pins on the new engine, the pins recomputed blind where (4)
moved the counts. This is the cracking; a row outside its band is a
finding for the mathematician before anything else changes.

**(7) WHAT IS NOT BUILT, by the owner's earlier words.** The clock
sourced by energy (9.45 (5)); the wall that never shrinks (9.45 (6) (A),
not needed since 9.50 keeps the inverse with the wall on the edge);
magnetism, spin, exclusion, the short-range forces (9.48's neighbours).
Each waits on its own row and its own word.

### 9.50 The backward run exact where the clock falls: two exact forms, the wall on the edge between two intervals (2) and the constant wall with the clock in the numerator (8), the constant wall ruled the law's form (the model owner's requirement of 2026-09-25 through the Boss: "the backward run must be solved; we need to find the right way to solve it", and his word "always look in the algebra for the generic solution"; Nature24's proposal and the Boss's check, records 1994 to 1997; PROVED and COMPUTED; supersedes the ruling (A) of 9.45 (6) and corrects its reason; for Nature24's build before 9.49 (2))

**(1) WHERE THE INVERSE IS LOST, EXACTLY.** The step at a Node under the
Node clock (9.45 (3)): 3 den f a_next + r' = e num S_6(a_now) + 6 den
(f - e) a_now - 3 den f a_before + r, with (e, f) = (Gamma, Gamma + c),
c the family of clicks' level at the Node, the wall W = 3 den f and 0
<= r' < W. The remainder r on the right was written by the previous
step under ITS wall, W_prev = 3 den (Gamma + c_prev): 0 <= r < W_prev.
The inverse (9.26 (3) (a)) reads K = e num S_6(a_now) + 6 den (f - e)
a_now - W a_next - r' = W a_before - r and takes a_before = ceil(K / W),
r = W a_before - K. This is one pair only when r < W, that is when
W_prev <= W. Where the level fell between the two intervals, c_prev >
c, the remainders r in [W, W_prev), 3 den (c_prev - c) of the 3 den
(Gamma + c_prev), satisfy W a_before - r = W (a_before + 1) - (r + W):
the states (a_before, r) and (a_before + 1, r + W) give one K and the
inverse cannot tell them apart. The integers: the two coefficients of
one step, of a_next and of a_before, are one wall, W(t); the remainder
crosses from the step at t - 1 to the step at t; where W(t - 1) > W(t)
it does not fit under the wall that consumes it. The fraction lost is
(c_prev - c) / (Gamma + c_prev) per unit of fall, 10^-6 at Gamma =
10^6, the number of 9.45 (6) (A). COMPUTED (the scratch script
`edge_wall.py`): a ring of 48 Nodes with S_6 read as the two ring
neighbours (the same algebra), Gamma = 50 so that the loss shows,
levels walking by 0 or +-1 per interval at every Node; 400 of 400
backward steps wrong, the first already (about 1 / 53 of the remainders
merge at each unit of fall on 48 Nodes); for one unit of fall at Gamma
+ c = 53, 1503 of 79659 remainders merge, 0.0189 = 1 / 53.

**(2) THE FIX: THE WALL ON THE EDGE.** Attach the wall to the edge
between two intervals and not to the interval: the edge (t, t + 1)
carries the level c(t + 1), the family of clicks' own value after its
step of interval t. Its own wall is constant, 3 den Gamma, by (D) of
9.45 (6) (e = f for its own step), so its a_next at the Node is known
from its own record and the six neighbours at t before any other family
divides: the family of clicks steps first in the sweep. The rule at a
Node, for every other family, with f_- = Gamma + c(t) and f_+ = Gamma +
c(t + 1), W_- = 3 den f_-, W_+ = 3 den f_+:

  W_+ a_next + r' = e num S_6(a_now) + [3 den (f_- + f_+) - 6 den e]
  a_now - W_- a_before + r,  0 <= r' < W_+,  0 <= r < W_-.

The produced value stands under the wall of the edge it enters; the
before term stands under the wall of the edge it came from; the middle
is the mean of the two walls, an integer since 6 den (f - e) = 3 den
(f_- + f_+) - 6 den e when f_- = f_+ = f. PROVED, THE INVERSE: K = e num
S_6(a_now) + [3 den (f_- + f_+) - 6 den e] a_now - W_+ a_next - r' = W_-
a_before - r with 0 <= r < W_-, so a_before = ceil(K / W_-) and r = W_-
a_before - K, one pair, for every sequence of walls, rising or falling.
THE REVERSED MOTION obeys the same rule with the two edges exchanged
(the value it produces under the earlier edge's wall, its before term
under the later edge's) and the remainder's sign mirrored, exactly as in
9.26 (3) (a); the middle is symmetric in f_- and f_+, so it reads the
same both ways. REDUCTIONS: at a constant level, f_- = f_+, the rule is
9.45 (3) term for term (COMPUTED: 400 steps on the ring, bit-identical);
at c = 0 everywhere it is the eighteen's rule. COMPUTED on the ring with
the levels rising and falling (4426 falls at the Nodes over 400
intervals): 0 of 400 backward steps wrong; the state returns bit for bit
to the first interval. The clock of a mode at a static level is
unchanged, 1 - cos omega' = (Gamma / (Gamma + c))(1 - cos omega); on an
edge where the level moves the step reads both walls, and that two-wall
form is the one that admits the inverse.

**(3) THE THREE TESTS.** Generic: one primitive with declared integers
(num, den, Gamma, the two levels at the Node), no family name, every
family reading the two edge levels the same way; with the charge (9.48)
each edge level is c - q Lambda d read on that edge. Vector: multiply
by an integer, add, one division with a remainder; no root, no float.
Local: the two levels are the family of clicks' own record at the Node
at t and at t + 1, the second its own a_next from its record and the six
neighbours; nothing else is kept at the Node, the state per family
stays (a_before, a_now, r). It is the same law with its wall read at the
right moment, not a new coupling.

**(4) THE IDEAS TO JUDGE, JUDGED (the Boss's three, and one more).**
(i) The family of clicks conserved, what enters a Node leaves it: a
conserved field still has a level that falls at a Node when the flow
leaves it; conservation does not keep the wall from shrinking; not a
fix. (ii) The wall never shrinks inside a step, only at a click: at a
body's Node the level is held and moves only at clicks, but at every
other Node the field's own step moves it every interval, far from any
click; and a wall that never falls keeps the giver's clock slow for ever
(9.45 (6) (A)), a physical change; not a fix. (iii) The merged remainder
kept as part of the Node's own numbers: a count that grows with every
fall, a register of the Node's history beyond the events there; fails
the local test. (iv) The level in e with f fixed, a constant wall:
reversible, but the coefficient of a Link's current, e num, then differs
at its two ends and T1's conserved form is lost; the reason of 9.45 (6)
(A) stands. The edge wall keeps e = Gamma on the Links, the content in
the wall, and the inverse: (A) chose conservation over reversibility,
and the choice is no longer made.

**(5) THE SHARE AND THE WORK TERM ON THE EDGE (the conservation answer
of 9.45 (5), restated).** The share on the edge (t, t + 1) over a set:
Q(t + 1/2) = sum over the Nodes of [3 den f_+ (a_{t+1}^2 + a_t^2) - e num
a_{t+1} S_6(a_t) - (3 den (f_- + f_+) - 6 den e) a_{t+1} a_t]. At a
static clock it is conserved exactly (T1; COMPUTED in exact rationals
on the ring). Where the clock moves, per Node, Q(t + 1/2) - Q(t - 1/2)
= 3 den (f(t + 1) - f(t)) (a_t^2 + a_{t+1} a_{t-1}) - 3 den (f(t + 1) -
f(t - 1)) a_t a_{t-1}, with f(t) the wall of the edge (t - 1, t)
(PROVED: the two products a_{t+1} W_- a_{t-1} and a_{t-1} W_+ a_{t+1}
differ by (W_+ - W_-) a_{t+1} a_{t-1}, and the two middles by 3 den
(f(t - 1) - f(t + 1)); COMPUTED exactly, the scratch script
`edge_share.py`). This is the work term of 9.45 (5) on the edge; the
answer there stands: no conserved total of the families under a moving
clock, by the law's choice, the exchange the clock's work on the
records; the remainders add their walk under rounding as always. What
changes is one word of 9.45 (6) (A): the law no longer keeps
conservation OVER reversibility; it keeps both.

**(6) THE PINS AND THE BODY RECORD.** Every world with a static clock
(the eighteen today: c = 0 everywhere, or the Node clock off) runs bit
for bit as before; no pin moves. Where the clock moves, the pins are
the ones 9.49 (4) and (6) recompute blind in any case. The body record
(9.46 (2)): its content M moves only at its clicks, so between clicks its
step is unchanged; at the interval of a click, with M_- the content
before and M_+ after, its step is den_c (Gamma + M_+) a' + r' = (num_c
Gamma + den_c (M_- + M_+)) a - den_c (Gamma + M_-) b + r, 0 <= r' < den_c
(Gamma + M_+), the two-term form of (2) (the middle num_c Gamma + 2 den_c
M when M_- = M_+); the record's own backward run is then exact, and the
equivalence test of 9.46 (4) is unchanged.

**(7) THE REQUIREMENT AS READ, AND ITS TEST.** The backward run is
exact at every Node between clicks, whatever the level does, by (2). A
click stays the one deletion (9.26 (3) (b), the owner's record 1139):
the record ends at the detector and the detector's record changes;
across a click the GameBoard is not a bijection, by the law. The owner's
words are read as the first, the run between clicks; if he means the
second as well, that is a change of POSTULATES.md section 10 and needs
his own word. For the build (9.49): this section goes before 9.49 (2).
The rule with the two walls, the family of clicks first in the sweep,
the body record's click step of (6). The test: (a) a world where the
level falls at Nodes with records (a body's field with its transients,
or the countdown world under the Node clock), run forward T intervals
and backward T, the state bit-equal to the start, T at least the
world's longest cycle; (b) the static-clock worlds bit-identical to
today's digests; (c) the assertion of 9.45 (6) (A), "loses at most one
remainder's worth per unit of fall", retired for "returns bit for bit".

**(8) THE CONSTANT WALL, AND THE RULING (Nature24's proposal and the
Boss's check of 2026-09-25, records 1996 and 1997; the owner: "always
look in the algebra for the generic solution").** The second exact
form: the wall the constant 3 den Gamma and the clock in the numerator,
the pair (e, f) = (Gamma - c, Gamma):

  3 den Gamma a_next + r' = (Gamma - c) num S_6(a_now) + 6 den c a_now
  - 3 den Gamma a_before + r,  0 <= r' < 3 den Gamma.

It is the one primitive of 9.45 (3) with another pair; 6 den (f - e) =
6 den c; nothing new enters the law. The remainder's range is the same
at every interval, so the split of the inverse is unique whatever the
level does, with no order in the sweep and no second level read
(COMPUTED, the scratch script `fixed_wall.py`: the ring of 48 Nodes at
Gamma = 50 with 4299 falls, 0 of 400 backward steps wrong; the Boss on
the host: 0 failures in 20000 against 1065 with the wall 3 den (Gamma +
c)). At c = 0 it is the vacuum's rule term for term: every static
world, the eighteen today, bit for bit. The rotation: 1 - cos omega' =
((Gamma - c) / Gamma)(1 - cos omega) in place of (Gamma / (Gamma +
c))(1 - cos omega); the two agree to first order in c / Gamma, the
Newton limit and every reading of 9.45 (2) unchanged, and differ at
second order by (c / Gamma)^2: 10^-12 at c = 1, 4 x 10^-9 at c = 64,
10^-6 at c = 1000 (COMPUTED); no pin of the eighteen reads the second
order, and nature's second order (the metric's) is neither of these
two, so the choice is the law's. THE RULING: THE CONSTANT WALL IS THE
LAW'S FORM. The reasons, one each: (i) it is the generic statement,
every family's wall the constant of its declared pair, everything that
moves in time in the numerator, as the owner asked; (ii) the inverse
needs no order and no lookahead, the edge wall of (2) needs the family
of clicks first in the sweep and the level of the next interval; (iii)
the load bound loses the factor (Gamma + M) and the guard becomes c <
Gamma, e > 0, so the amplitude bound 2^28 stands with more room (the
numerator at most Gamma num times 6 times 2^28, the vacuum's own bound;
under int64 as today); (iv) the reason that put the content in the wall
was wrong, (9). The edge wall of (2) stays recorded as the exact form
of the pair (Gamma, Gamma + c), not adopted. WHAT CHANGES WHERE: 9.41
and 9.45 (1) to (3) read (Gamma - c, Gamma) for (Gamma, Gamma + c) with
this ruling, the wheel W = 3 den Gamma / gcd((Gamma - c) num, 6 den c,
3 den Gamma), the pair's own at c = 0; the body record (9.46 (2)) den_c
Gamma a' + r' = (num_c (Gamma - M) + 2 den_c M) a - den_c Gamma b + r;
the charge (9.48) the pair (Gamma - c + q Lambda d, Gamma) with the
bound e > 0; the family of clicks' own step unchanged (e = f = Gamma).
ONE PHYSICAL DIFFERENCE, at the extreme only: at c = Gamma the numerator
is 0 and a record's rotation stops, a horizon at a content of Gamma
quanta at one Node; under the wall 3 den (Gamma + c) the clock never
stops. It is far outside every world of the eighteen and is stated, not
used. The test of (7) stands, with (a) on the constant wall.

**(9) THE REASON OF 9.45 (6) (A), CORRECTED (PROVED and COMPUTED).**
(A) said that a per-Node e makes the neighbour coupling asymmetric and
loses T1's conserved form, so the content had to sit in the wall. That
was wrong. Write the static linear step as a_next + a_before = B a_now
with B_ij = e_i num / W_i on the Links and B_ii = 6 den (f_i - e_i) /
W_i; B is not symmetric when e_i or W_i differs by Node, but D B is
symmetric for the diagonal weight D_ii = W_i / e_i, since (D B)_ij =
num on every Link; and for any such D the form Q = a_next . D a_next +
a_now . D a_now - a_next . D B a_now is conserved exactly (the
difference of two consecutive Q is a_next . D a_before - a_before . D
a_next = 0, D symmetric). So the conserved form on a set is the sum
over its Nodes of [3 den f_i (now^2 + before^2) - 6 den (f_i - e_i) now
before] / e_i less num (now . S_6 before) over its Links, with the Link
current num (now_i before_j - before_i now_j) UNWEIGHTED and the same
in both forms; T1 holds with the Node terms weighted. In the pair
(Gamma, Gamma + c) the weight is 1 / Gamma, uniform, so the form is the
integer E_i of 9.45 (3) with the content in the wall; in the pair (Gamma
- c, Gamma) the weight is 1 / (Gamma - c_i), a rational per Node, the
same integer form within a body at one level. COMPUTED in exact
rationals on the ring at a static level walking by Node: both forms
conserved exactly, the unweighted sum under (Gamma - c, Gamma) not.
The share is a GameBoard reading (a diagnostic); the click's taking end
reads the current, which is the same integer in both forms.

**(10) CONSERVATION, ON THE OWNER'S TWO WORDS (records 1997 and
Nature24's question: "why did you think another family, gravity or
energy, is needed for conservation?").** The owner: "the conservation
must follow from local laws at the Node; these conservations must not
be laws that we put in so that it comes out that way." The answers, one
each. (a) No family was ever meant for conservation: 9.45 (5) speaks of
a COUPLING, the family of clicks reading the records' shares at the
Node as its source in place of the counted content; the fifth family
of 9.48 is the charge, another matter. (b) What follows by itself from
the rule at the Node, with nothing put in: each family's weighted
share (9) where the clock stands, exactly, from the step's symmetric
form (D B symmetric); the count of quanta at every click; the exact
backward run, which is the rule at every Node one to one, (8). (c)
What does not follow and is not declared: a conserved total of the
families under a moving clock; the records' share changes by the
clock's work (5) and nothing balances it, because the family of clicks
reads no family; 9.45 (5) says so and 9.47 (10) marks it "none, by
choice"; no rule is written to make a total come out. (d) Is there a
generic local form in which the family of clicks and the records
balance with no rule added for it: YES, in principle, and it is
gravity by energy: one joint local rule from one form at the Node,
the records stepped with the clock as their index and the clock
stepped from the records' shares, the same form read both ways (a
variational step of one local quadratic); then a conserved total
follows from the form's symmetry under a shift of the interval (the
discrete Noether identity), not from a rule written for it; its
integer form and its exact backward run (the source read one edge
behind, so that the inverse has what it needs) are not derived here
and stand OPEN under their own identity, as 9.45 (5) placed them. (e)
Needed or wanted: no pin of the eighteen needs a conserved total with
gravity; it is wanted for light as a source of the field, the mass
defect of a bound body and the moving body's weight, none of them a
row today. (f) The exact backward run is not that conservation: it is
the rule's one-to-one form, a different property, and it is now exact
by (8) with nothing added.

**(11) THREE CONVENTIONS OF THE BUILD, STATED (Nature24's head 3715fcb0,
the reseed retired; the pieces he listed as stated nowhere).** (i) The
first residue after the load is read after the body's first advance,
because the seed's remainders are 0 at the write (9.43 (4), 9.19 (4e)):
a convention of the load, one line. (ii) The shell on a folded axis of
extent 1 carries no Port, as the flux reading's Ports (the Node reads
itself there, the read matrix of the chain lemma): a convention of the
GameBoard's folding, stated. (iii) The count's P is the emitter's
declared integer, the mode's period at the initial content under the
clock (9.45 (5)); the clocked period exceeds the plain mode's by about
M / (2 Gamma) intervals, below one interval at every content of the
eighteen, so the integer is the same; when it is not, the generator's
integer under the clock is the one declared.
