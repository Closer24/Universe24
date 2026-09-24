# The group structure of the law: the four group objects, their operations, and how the group of order 24 and the 48 act on each (the index page)

The canonical statement of this algebra is [docs/ALGEBRA.md](ALGEBRA.md), section 1 (its sections 1 to 6 carried over there) and 7; this file is kept as the record of 2026-09-23.

The model owner's word of 2026-09-22 ("how are the groups defined here;
put it in order in the files if it needs ordering") on the Boss's order:
one page that names the four group objects of the law, their definitions in symbols, the dictionary from the algebra to the physics, how the group was reached from the operations, their operations,
and the action of the symmetry group of the cube on each, with links to
the code and the tests. This page is the index and not a copy: every
rule is stated once here in one line and its full statement lives in the
owning document linked beside it (the one-source rule of
[AGENTS.md](../AGENTS.md)). Nothing here is a new rule; no number moves.
Notation per [skills/workflow.md](../skills/workflow.md) ("Notation"): a
scalar plain, a vector bold lowercase (**p**), a matrix or an operator
bold uppercase (**C**), every symbol named in English at its first use.

## 1. The definitions, in symbols

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

## 2. From the algebra to the physics: the dictionary

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
| spin, polarisation | the hand h in {-1, 0, +1}, a pseudoscalar under the 48 (h -> det(g) h); a body's axis an axial vector | `docs/designs/hand/FORM.md` (deleted on 2026-09-22 with the hand worlds, record 894; in the tree at 59c6b811); BEAM_LAW note 39 |
| isotropy, the symmetry of the law | the 48: every operation commutes with G_48 (section 1); the law's constants are invariants of O_h (k^2 the one quadratic invariant; two quartic ones, the anisotropy at order k^4) | [DERIVATIONS.md](DERIVATIONS.md); [designs/fraction_free/FORM.md](designs/fraction_free/FORM.md) |
| Lorentz, Einstein, Newton | not in the group: no boost is among the 48; their forms are reached Outside as relations among counts between clicks (the one-way factors, the round trip, the radar; the ring mean of the push), the algebra first and the comparison after | [designs/click_frame/DERIVATION.md](designs/click_frame/DERIVATION.md); [designs/ring_mean/PROOF.md](designs/ring_mean/PROOF.md); [HIGHLIGHTS.md](HIGHLIGHTS.md) 5.4 |
| a measurement | a click at a detector; a count between clicks on the detector's own record; a ratio of such counts (the reading rule, section 8); a reading of the board a diagnostic | [ENGINE.md](ENGINE.md), the readings by type; record 281 |

## 3. How the group was reached from the operations

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
   c **p** . **p**, and the square m^2 + 3 **p** . **p** follows. "Generic"
   in the three tests of every rule (generic, vector, local) means
   exactly this: commuting with the 48, made of the six operations,
   reading the neighbourhood alone.

In one sentence: the operations did not deduce a group; they were
defined on a Node of six Ports, the 48 are everything that preserves that
Node and its cone, and once every rule is required to commute with them
they choose the admissible forms, the group of order 24 being the part
under which the hand is kept as well.

## 4. The names, fixed by the owner

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

## 5. The phase circle and its group ring

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

## 6. The translation group of the torus

Z_X x Z_Y x Z_Z per world: the GameBoard's extents per axis, each factor
a circle (a periodic axis) or a segment (an open axis whose faces are
the border, a click at the face detector). Chosen per world by `shape`
and `boundary` ([FULL_PICTURE.md](FULL_PICTURE.md) section 1, choice 3;
[ENGINE.md](ENGINE.md), the world file). The translation (T) of
DERIVATIONS_BEAM's list is the action of this group on Nodes, and on the
counts the same division with the remainder kept.

## 7. The collision as a group action

The cyclic group acts on the 3^8 slot states of a Node by the shift
`forward` (its inverse `inverse`); the orbits of the action are the
collision classes of [BEAM_LAW section 4](BEAM_LAW.md), each with its
invariants (the crowd mask, the number of singles, their headings' sum);
a code's period is its class's size, one cycle per class. In the code
`nature_beam.CollisionTable` (`act`, `orbit`, `period`); named in BEAM_LAW
note 42; the properties in `tests/test_group_structure.py`
(`test_the_collision_action_is_one_cycle_per_class`) and the orbits under
the 48 in `tests/test_nature_beam_collision.py` (b).

## 8. The operations between them, from the algebra

[DERIVATIONS_BEAM.md](DERIVATIONS_BEAM.md) section 1 lists the six
operations of every interval at every Node, and this page names where
each group sits in them (the full statement is there, not here):

| Operation | On what | The group object |
| --- | --- | --- |
| (T) the translation | Nodes and counts | the translation group of section 6; on a count the division with the remainder kept |
| (B) the bilinear form | the neighbourhood's rows, the coupling **C** **a** | the moments over directions; covariant under the 48 (section 9) |
| (G) the group-ring addition | a record's rows at a Node | Z[Z_N], the merge with the cancel (section 6) |
| (P) a permutation of the joint state | the collision, the meeting's turn, the gate, the apportioning's tie | the collision's cyclic action (section 7); the meeting's arc permutation of the direction table (`tests/test_meeting.py`, `test_the_arc_permutation_on_the_table_of_series_k`); a permutation of directions or Nodes, never of contents |
| (E) the evaluation | Z[Z_N] -> Z[zeta_N] through the tables C and S and the norm \|z\|^2, then the ladder on the wheel | the click: zeta_N a primitive N-th root of unity, Z[zeta_N] the cyclotomic integers, the quotient of the group ring by x^(N/2) + 1 where opposite phases cancel |
| (D) the division and the comparison | a count against a wall, an age against a key, a phase against a window | the counts' primitive; no group |

**The reading rule** (the model owner, records 1104 and 1115): a
click at a detector, a count between clicks on the detector's own
record, and a ratio of such counts are what is compared with nature;
nothing measured inside the board is compared (a GameBoard reading is a
diagnostic). The evaluation (E) is the last group operation before a
number leaves the board; every comparison is made on counts after it.

**Under the rule of the massive record kind and the massless kind
beside it** (`massive-record-v1`, `detector-law-v1`, hypotheses beside
the law; 2026-09-24): a record is a pair of levels (a_before, a_now), two
samples of one character of Z_N, and a table acts on that pair by the
linear form, the shift of Z[Z_N] read on two samples; the click is the
rung on the pointer against the norm in place of the evaluation. The one
statement is [ALGEBRA.md](ALGEBRA.md) 1.7 (the identity proved there)
and 8.6; the objects of the board (a foreign object, a detector set) are
sets of Nodes on which the groups act, elements of none, ALGEBRA.md 1.7.

## 9. How the 48 act: one table

The 48 act on directions and Nodes and commute with every verb of the
law up to the two declared ties (the digital line's axis order and the
collision's Port order, [TERMINOLOGY.md](TERMINOLOGY.md) "The cube
group"; [designs/fraction_free/FORM.md](designs/fraction_free/FORM.md)
"Covariance under the 48"); they act trivially on every content (a
content is a scalar); on the hand they act by the determinant alone
(`docs/designs/hand/FORM.md` (deleted on 2026-09-22 with the hand worlds, record 894; in the tree at 59c6b811)). The group of order 24 is
the subgroup that fixes every pseudoscalar.

| Object | Operation | What the 48 do | What the group of order 24 does |
| --- | --- | --- | --- |
| a direction D of the table; its label **u**_D, its flow label **f**_D | the flight, the label, the push | permute the table: **u**_{gD} = g **u**_D exactly (`unit_label`, BEAM_LAW note 23) | the same, by the rotations alone |
| a Node, the six Ports | the translation, the step, the face click | permute the Ports and the Nodes about a Node; the two ties named above | the same |
| a content, an amount, a count, an age | (T), (D), the books | fixed (scalars) | fixed |
| a row's phase in Z_N and a record's element of Z[Z_N] | the turn, the merge (G), the click (E) | fixed: the phase is not a direction; (E) commutes with the 48 through the directions' moments alone | fixed |
| the collision's slot states | (P), the cyclic action | permute the classes among themselves (the orbits of the six-heading patterns, `test_nature_beam_collision.py` (b)) | the same |
| the hand h in {-1, 0, +1} of a row; a body's axis | `become`'s right-hand rule, the merge's identity field | h -> det(g) h: kept by the 24 rotations, negated by the 24 reflections; an axial vector a -> det(g) g a | fixed (det = +1) |
| the moments of order 0, 1, 2 of the arrivals (the one reading) | (B) | rotate the flow vector and the tensor, fix the scalars (`tests/test_nature_beam_readings.py`) | the same |

## 10. Where each definition lives today

| Definition | Owner document (the full statement) | Code | Test |
| --- | --- | --- | --- |
| the symmetry group of the cube, the 48; the group of order 24; the hand as the pseudoscalar | [FULL_PICTURE.md](FULL_PICTURE.md) section 1; [BEAM_LAW note 42](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation) and [note 39](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation); [TERMINOLOGY.md](TERMINOLOGY.md) "The cube group"; the paper's Theorem 1 | `core/game_board.py` (`cube_symmetries`, `compose_symmetries`, `inverse_symmetry`, `symmetry_hand`) | `tests/test_group_structure.py` (a); `tests/test_hand.py` |
| the phase circle Z_N and its unit vectors | [BEAM_LAW section 5](BEAM_LAW.md) and note 42 | `core/phase.py` (`PhaseCircle`) | `tests/test_group_structure.py` (b) |
| the group ring Z[Z_N], the merge, the cancel | [DERIVATIONS_BEAM.md](DERIVATIONS_BEAM.md) section 1 (G); [BEAM_LAW note 37](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation) | `nature_beam.py` (`NatureBeamStore.merge`) | `tests/test_amplitude_click.py` |
| the translation group of the torus | [FULL_PICTURE.md](FULL_PICTURE.md) section 1, choice 3; [ENGINE.md](ENGINE.md) | `core/game_board.py` (the GameBoard's shape and boundary) | `tests/test_locality.py` |
| the collision as a group action | BEAM_LAW section 4 and note 42 | `nature_beam.py` (`CollisionTable`) | `tests/test_group_structure.py` (c); `tests/test_nature_beam_collision.py` (b) |
| the six operations and the evaluation at the click | [DERIVATIONS_BEAM.md](DERIVATIONS_BEAM.md) section 1; [designs/vector_form/LAW.md](designs/vector_form/LAW.md) | `nature_beam.py`, `measured.py`, `core/integer.py` | `tests/test_fraction_free.py`, `tests/test_amplitude_click.py` |
| the action of the 48 on the hand | `docs/designs/hand/FORM.md` (deleted on 2026-09-22 with the hand worlds, record 894; in the tree at 59c6b811) sections 2 and 3 (`hand_map.out`) | `nature_beam.py` (`become`'s right-hand rule) | `tests/test_hand.py` |
| the covariance of every rule under the 48, the two ties | [TERMINOLOGY.md](TERMINOLOGY.md) "The cube group"; [designs/fraction_free/FORM.md](designs/fraction_free/FORM.md) | the flight table (`direction_flight`), `unit_label` | `tests/test_nature_beam_label.py` (a), `tests/test_nature_beam_readings.py` |

## 11. Every file in which 24 or 48 names a group: the wording found, and whether it agrees

The fixed names: "the symmetry group of the cube" (the 48 signed
permutations of the axes, O_h) and "the group of order 24" (its
rotations, isomorphic to S_4). Nothing below is renamed; a wording that
uses another name for the same object is listed for the owner's word.
"S24" and "S_24" appear in no file. Hits where 24 or 48 is a count and
not a group (the 24 thrown sources and Hubble stars, the 48 in-plane
lines of the fan in `designs/light_bending/STEP_ALGEBRA.md` and
`designs/flow_weight/ALGEBRA.md`, the 48 capture seeds of VALIDATION.md,
the 48 orientations of a nucleus in ENTITY_CATALOG.md) are left out.

| File | The wording found (verbatim) | Against the fixed names |
| --- | --- | --- |
| `paper/general_formula/main.tex`, Theorem 1 and its proof | "the group of the signed permutations of the three axes, of order 2^3 . 3! = 48"; "its kernel, the group of order 24 (the rotation group of the cube), has index 2 and is the group of the permutations of the cube's four body diagonals, the symmetric group S_4"; the proof and the symbols table: "the hyperoctahedral group B_3" | agrees; B_3 a second standard name of the 48 (B_3 = O_h), used in the proof and the table |
| `docs/HIGHLIGHTS.md` 5.4 | "the rotation group of order 24"; "the group is called the group of order 24 everywhere ... the 48 signed permutations of the axes are the object's symmetries, whose rotations that group is" | agrees (the fixing lines) |
| `docs/FULL_PICTURE.md` section 1 | "What is not chosen: the group of 48. The cube's group (the signed permutations of the three axes, 3! x 2^3 = 48 ...; the 24 of hand +1 the rotations, the 24 of hand -1 the reflections ...)"; "the full octahedral group O_h of order 48" | agrees in substance; says "the cube's group" and "the 24 of hand +1 the rotations", not "the group of order 24" |
| `docs/TERMINOLOGY.md`, "The cube group" | "the 48 signed axis permutations about a Node, 24 rotations and 24 reflections, under which every rule is covariant up to the two declared ties ...; its hand is its pseudoscalar, +1 on a rotation and -1 on a reflection" | agrees in substance; the term entry is "The cube group", the rotations named by count |
| `docs/BEAM_LAW.md` note 42 | "the 48 signed axis permutations are the cube's group with its hand as the pseudoscalar" | agrees in substance ("the cube's group") |
| `docs/BEAM_LAW.md` note 39 and its tests' lines | "kept by the 24 proper rotations and negated by the 24 improper ones"; "differs under exactly the 24 improper elements and under none of the 24 proper ones" | agrees in substance ("proper" and "improper" for the two cosets) |
| `docs/DERIVATIONS_BEAM.md` section 16.3's table | "the group of the Ports of order 48 = 2^3 x 3! (the signed permutations of the axes), its 24 rotations and 24 reflections (the determinant the hand)"; elsewhere "the cubic 48", "commutes with the 48 signed axis permutations" | agrees in substance |
| `docs/DERIVATIONS.md` | "the group O_h requires (k^2 is its only quadratic invariant)"; "O_h has two quartic invariants" | agrees (O_h the 48) |
| `docs/designs/paper_families/FAMILY_TABLE_AUDIT.md` and `family_table.py` | "the 48 signed permutations of the axes, 3! x 2^3, the hyperoctahedral group B_3, its 24 rotations and 24 reflections told apart by the hand"; "the hand (Z_2, the pseudoscalar of the 48)"; "the permutation (the 48)" | agrees in substance; B_3 as in the paper |
| `docs/designs/hand/FORM.md`, `REVIEW.md`, `hand_map.py` | "the 48 symmetries", "the 48 signed axis permutations: proper (det +1)", "kept under the 24 proper rotations, negated under the 24 improper" | agrees in substance |
| `docs/designs/click_frame/DERIVATION.md` | "are the 48 (the 24 rotations of the six Ports with the hand)"; "the reflections, the 48 in three dimensions" | agrees in substance |
| `docs/designs/algebra_transition/HISTORY.md` | "24 is the count of the rotations of the six-Port Node, the octahedral ..."; "the cube group of 48"; "a group of 48 signed axis permutations under which ... contains no boost" | agrees in substance (history) |
| `docs/designs/highlights_now/AUDIT.md`; `docs/designs/highlights_prune/CONTRADICTIONS.md` | "Universe24 is the universe of the 24 rotations"; "a Lorentz boost is not among the 24, which is why Lorentz's symmetry belongs to the limit and not to the group" | agrees |
| `docs/designs/open_problems/lorentz/NOTE.md` | "a rule of the law commutes with the cube's group of 48 signed axis permutations (..., the law's only symmetry at finite Q)" | agrees in substance |
| `docs/designs/quarks/QUARKS.md`, `quark_numbers.py` | "the cube's group of 48 on a line (the stabiliser 16 of 48)"; "The cube's group of 48: a permutation of the axes and a sign per axis" | agrees in substance |
| `docs/designs/fraction_free/FORM.md`, `TWO_SLITS.md`, `fan_sphere_map.py` | "Covariance under the 48"; "O_h-equivariant"; "the 48 symmetries, checked on all 290" | agrees |
| `docs/designs/massive_rows/DESIGN.md`; `docs/designs/light_outside/DERIVATION.md` | "the 48 signed axis permutations"; "pseudoscalar of the 48" | agrees in substance |
| `docs/EXPERIMENTS.md` (the gallery's frames) | "the 48 signed axis permutations ... (24 rotations, then 24 improper ones ...)" | agrees in substance |
| `docs/ENTITY_CATALOG.md` | "that family restricted to the 24 proper rotations of the GameBoard" | agrees in substance |
| `docs/TEST_EXPECTATIONS.md`, `docs/VALIDATION.md`, `docs/MIGRATION.md` | "the cube's group of 48"; "the 48 signed axis permutations"; "the 48 GameBoard symmetries"; "the 24 improper" | agrees in substance |
| `src/event_universe/core/game_board.py` | "The cube's group of 48 (the signed axis permutations, ...). The 24 of hand +1 are the rotations, the 24 of hand -1 the reflections (`symmetry_hand`, the pseudoscalar of the group ...)" | agrees in substance |
| `src/event_universe/events/nature_beam.py`, `world.py` | "kept by the 24 proper rotations of the cube and negated by the 24 improper"; "the 48 signed axis permutations" | agrees in substance |
| `tests/test_group_structure.py`, `test_nature_beam_collision.py`, `test_nature_beam_readings.py`, `test_nature_beam_label.py`, `test_hand.py`, `test_gallery_pages.py` | "the cube's group of 48"; "the six-heading patterns under the cube's group of 48"; "the 48 signed axis permutations R"; "the octahedron's rotations: 1 + 3 + 6 + 6 + 8) then the 24 of determinant -1" | agrees in substance |

In sum: no file disagrees with the fixed names on the objects (the 48
and their rotations, told apart by the determinant); the phrase "the
group of order 24" is used by the paper and Highlights 5.4, while the
older documents and the code name the same subgroup "the 24 rotations",
"the 24 proper rotations" or "the 24 of hand +1", and name the 48 "the
cube's group", "the cube group", "O_h" or "B_3". Whether those wordings
are aligned to "the group of order 24" and "the symmetry group of the
cube" is the owner's word; this page renames nothing.
