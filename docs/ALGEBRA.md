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
not state.

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
constant (5.8), named there.

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
   c **p** . **p**, and the square m^2 + 3 **p** . **p** follows. "Generic"
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
where the cap a is absent and e is the whole part floor(abs(s) / d)
with the sign; the code's `at_most = 0` means no cap), and reduced by
the walls it holds; every wall counted is an event (a Link crossed, a
phase step taken, a count completed, a birth, a push) and nothing else
happens. The one declared variant of the count is `centred`
(centred-step-v1, the world key `centred_step`, which chapter 6's row 6
cites): the count is the nearest whole number the accumulator holds,
(abs(s) + d // 2) // d with the sign, the accumulator then in
[-(d - d // 2), d // 2). The rates and
walls are made of six integer operations and nothing else, the six
verbs of [Highlights 5.4](HIGHLIGHTS.md) (records 181 and 202): (T) the
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
gains abs(p_a), the momentum's component, against the wall Q S_w M +
abs(p_a), capped at one Link per interval (a = 1). On the phase, a row
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
comparison is part of this verb: the ladder's cell 2 T u + T <= 2 N C_k,
an age against a key, a phase against a window, a threshold, itself a
division whose quotient is 0 or 1 and whose remainder is not read
(the paper: "the division with the remainder kept, together with the
comparison that is the event"). The superseded wording: "the Euclidean
division with the remainder kept" without the comparison ([Highlights
5.4](HIGHLIGHTS.md) item 3, record 202; [TERMINOLOGY.md](TERMINOLOGY.md)
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
constant multiplying a row in flight (the rotation's tables, the
meeting's `adv`) is a declared rounding at load or a stated limit, not
a verb. No float, no true division, no draw.

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
tests of every rule" (record 202); Highlights 5.4 item 4.

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
[COUPLINGS.md](designs/couplings_algebra/COUPLINGS.md) section 1, its
one-line result in section 3.

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
Z_W; Born's rule the bilinear form f^T **G** f on an element of Z[Z_N];
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
1261-1290.

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
section 0 writes the same two factors with the subscripts in the
emitter-to-detector order, so that its k_AB is this file's k_BA; the
record's convention, named once here.) The general form, Theorem 1 of
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
two intervals Inside, two of its counts at r_D = 1 (2 r_D in general,
which is how r shows); the tick itself is GAMEBOARD and never read;
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
labels l of U_a[o_A][l] U_b[o_B][l], the cell's weight R = J^2, the
birth wheel's u selecting one of the four cells through the rung (B3);
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
  in the Link over the coarse cell (DERIVATIONS_BEAM 25.4 (3)). DERIVATIONS_BEAM 9.1 (I5) and 25.4; the paper's section
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
  6.5 (the hypotheses at lines 1590-1608; the Gram matrix at
  1651-1658) and 6.7.
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
  rational for each N: 11 / 4 at 64, 45 / 16 at 256, 181 / 64 from 512
  through 8192, 5793 / 2048 at 16384 (COMPUTATION, met by series L and
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
  and information out <= log2(cells) bits (the Holevo bound as the
  ladder's count); the ladder's identity H(K) + H(U | K) = H(U) = log2 N,
  bits read + bits erased = log2 N per record; on the phase circle abs(supp
  f) x abs(supp f_hat) >= N (the Fourier transform's, Donoho and Stark;
  equality at a comb of every eighth phase at N = 64) and the Weyl
  relation V U = omega U V, omega here a primitive N-th root of unity,
  for the shift U by one phase and the multiplication V by omega^y. DERIVATIONS_BEAM 6.4, 6.1, 14 and 22.1; Light Outside II.2.
- **4.12 The click's indivisibility, and Malus.** One click per record,
  never two: the ladder chooses one cell and deletes the offers, P(D1
  and D2 in one record) = 0 exactly (the cancel exact; mz_equal 64 / 0,
  DETECTOR); Malus, P(pass) = cos^2 theta, theta the polariser's angle against
  the label, on the rotated label's Gram
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
  hypothesis with pins), and the Einstein map E1 to E17 beside it:
  DERIVATIONS_BEAM 21.2 and 21.4. This file lists no status the map
  does not.

---

## 5. What is reached under named hypotheses, each with its hypotheses and its kind

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
and its return; (M) the shell mean over N(r) Nodes, N(r) -> 4 pi r^2
(2 pi r on the plane); (K) the one constant (Einstein Outside section
I, lines 196-251). For light, (L1) to (L9) (Light Outside section I,
lines 242-333). Every item below carries its hypotheses, the limit
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
w / k) on the light-cone coordinates u = t - x, w = t + x, the boosts
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
/ 6, kappa^2 / 6 and "up to m^2 v^2", are one statement to this order);
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
transverse factor 1 / r_X (SHOWN, rung 2; FAIL on the law, 1 against
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
trips (5.1's r-free lines). Source: Einstein Outside Theorem 2, lines
416-464; the click frame section 2 (b).

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
count ratio of two lamps at two distances k(r_1) / k(r_2) = r_2 / r_1,
READ: series T's 1.907 for the pin 1.909 +- 0.05, DETECTOR, the
continuum's 2.00 outside the pin by the grain); the flat interior of a
shell (series X's k(2) / k(4) = 1.0029 for 1.003917 +- 0.02, MET,
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
inputs); SHOWN IN FORM, the constant a declared input, the one reading
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

The wording in force is one sentence (the plan's K3, the Boss's word:
stated as the unifier's proposal, the reviewer decides): **Einstein's
step is the image of the Inside step under the conversion, a step
above the board whose r-free lines (the round trip, the composition,
the aberration) are Einstein's exactly from (A1), (A3) and the
conversion, and whose scaled lines (the rate r, the one-way Doppler,
the length, the energy) are Einstein's if and only if r^2 = 1 - v^2,
the one line the click theorem leaves free** (the click frame section
9 (II); Einstein Outside section 3 (a); Newton from the clicks 1.3).
The three wordings of the sources say one thing from three sides:
Einstein Outside writes the image's most general form (dp / dt = F with
p = gamma m v; E^2 = E_0^2 + c^2 p^2; d tau / dt = sqrt(1 - v^2); the
geodesic's first terms, the equivalence of the fall, the redshift g Y /
c^2, the deflection 4 G M / (c^2 b)); Newton from the clicks 1.3 writes
"the IMAGE of the Inside step under this map"; Newton from the clicks
1.4 (b) and Newton on the side write "the conversion between the
mover's count and the rest detector's, the rate r", which is the one
factor of that image that the scale needs. The image's rows for a body
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
Newton out of the clicks in the algebra, not at low velocity, Einstein a
step in between; the Boss's word of 2026-09-23 on the plan's K2):
Newton's form is reached from the clicks with no expansion in v / c;
the one limit taken is the shell mean (M), the spatial average over
N(r) Nodes, for the 1 / r of the potential and the 1 / r^2 of the fall;
Newton's classical scale is the value r = 1 of the mover's own count
and the value u / c -> 0 of the click count's term, values the side
arranges and not limits taken in the algebra. The earlier wording, "in
the continuum limit ... many self-creations, v << c, the shell mean"
(Einstein Outside Theorem 4, RECOVERED; the paper's opening "in a limit
under a shell average"), is superseded on the v << c clause and kept as
its record; the shell mean it names is the one limit both wordings
take. **Hypotheses:** (A1); (W1) to (W5); (M) where named; the world
file's detectors, lamps and declared integers (the fan, S_w, n / d, the
contents, eta the suspension ratio n / d); no (A2). **(a) The clicks, the primitive.** A detector
is a body with its own count n_D, one accumulator advanced by one per
interval and stretched by the age wall at coefficient 1; a click is the
arrival at D of a packet another detector released, the triple (the
Node, n_D at the arrival, what arrived: the packet's ordinal, its
direction, its content); the ordinal a released row carries is the
emitter's own count at the release, so a lamp on a moving body hands
the body's own count to every rest detector it reaches, and "Nodes
apart over the mover's own counts apart" is a ratio of two click
readings, DETECTOR on both sides; the packet in flight IS the moving
detector (record 1043). **(b) The second law, from the clicks.** A
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
click frame's "the cost gives r = 1 - beta or 1"; the plan's K4: r = 1
the clock in no crowd, 1 / (1 + k_crowd) the clock in a crowd, 1 - v
the drive's resident count, three quantities under one letter, named
apart here). Under form B (decided, not built) the same identity holds
with abs(**p**)_1 in place of abs(p_a). **(d) The velocity term (1 + u
/ c) is the clicks' own.** A detector hopping at v toward a stream of
rows at c meets E(tau) = (1 + s v / c) tau + O(1) rows in tau intervals,
the O(1) one boundary row, EXACTLY over whole Links of its path (128 +
55 = 183 toward and 128 - 55 = 73 away in 128 intervals at k = 4,
against 128 at rest; COMPUTATION from (A1) and the flight table, met
by `tests/test_crossing.py`; after a detector it is the Doppler, row
4b's z); so the term is produced by the click algebra for every count
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
ratio of two lamps at two distances, k(r_1) / k(r_2) = r_2 / r_1, READ
(series T, DETECTOR, 5.4); the second difference of (b) at two
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
clicks on the host's tick; its click reading the recurrence of the
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
the ordinals T_1(24) / T_1(12) = 2.00 +- 0.20; the owner's word "a read
at a body is a click" the one line the push count needs (chapter 3.2).
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
c_D by the passage of clicks, 0 by the click's face (SHOWN at first
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

    1 + z_d = k_AB = (1 + k_A) (1 + v / c) r_B = r_B (1 + z),   r_B = 1 / (1 + k_B);   at rest   1 + z_d = (1 + k_A) / (1 + k_B) = 1 + k_A - k_B + O(k^2),

the potential's 1 / r at first order (rung 1 in k, rung 2 in r; MET:
series G, G2, T and X; the second order the law's own, 5.4); the row's
phase is never stretched (a stretched phase per age would redshift
light in transit). Bell at two places: chapter 4.10. Reflection and
refraction: NEITHER (a row meets no surface; a mirror is the
apparatus's declared table; no crowd slows or bends a row on main). The
apparent acceleration (the dark energy note): for a lamp thrown at v
and read after the flight time tau,

    1 + z_d(tau) = r_B (1 + k_A(tau)) (1 + v(tau) / c) = g(tau) (1 + z_throw(tau)),   g(tau) = (1 + k_A(tau)) / (1 + k_B),

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
sections 2 and 4.

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
reaches from a circle j <= 6 are (4, 3), (5, 4), (6, 5) and from j = 3
none below (from j = 7 on, (7, 5), (7, 6), (8, 6), ... by the same
condition); Balmer's i = 2 from j = 4 (2 x 2^2 = 8 < 16) and Lyman's i = 1
from any j >= 2 are not reachable by one click. **A release unbinds:**
dE / dM < 0, losing content raises the loop's constant and the body
unbinds (charge is per unit of content). **What no rule does:** the row
that carries the body between two closed loops is selected by nothing;
the law has one frequency per family (the declared pair) and not one
per transition; the give of a bound set is once per body and declared
(binding-v1). The comparison, afterwards: Bohr's condition MET IN FORM
in the limit; Bohr's radii MET IN FORM in the shell mean, FAIL IN FORM
on the lattice; Kepler's third law on the closed loops MET IN FORM, NOT
READ; Balmer's ratio nu(H beta) / nu(H alpha) = 27 / 20 = 1.35 NOT
READ, and FAIL IN FORM for a one-click atom; the binding as a
difference of two levels FAIL (series N's 2.0 against 12.72, DETECTOR);
DERIVATIONS_BEAM 7.2: the levels and the lines NOT REACHED (no energy
of a body, no transition; a detector reads the orbital frequency nu_j
proportional to 1 / j^3, Bohr's correspondence limit). **The verdict:**
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

    the walk:   A = the crowd's age moment at the row's Node;  (r_0, w_0) = (2 S_1 Q, 2 T_D) on a row never pushed, else (2 S_1(**p**) Q, 2 T(**p**)), the walk's rate and wall;  s += r_0 d;  if s >= w_0 (d + c_f n A): s -= w_0 (d + c_f n A), the Link h = line_D[made mod S_1], made += 1, the Node moves by h
    the push:   at a free Node, **a** = the arrival flow there;  **w** -= n x weight_D x **a**;  s = s x S_1(**p**') // S_1(**p**)
    the label:  **p** = Q d **u**_D + **w**; among D and its neighbours the h with h . **p** > 0 that keeps abs(**c** + h x **p**)^2 smallest; if D' differs, **w** += Q d (**u**_D - **u**_D'), D = D'

with the crowd from the same flight rule, A(r) = scale x sum over the
lines D through r of the sum of the ages present and **a**(r) = scale x
sum of **u**_D (the weighted **f**_D under flow-link-v1, the integer
vector nearest Q D / S_1), constant in time once the oldest row that
reaches r has been born; the engine walks it as the algebra does to
0.01 (the calibration on the registered worlds). **Two verbs apart:**
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

    alpha = 2 k_a(b) (c^2 / v^2) (1 + gamma_PPN v^2 / c^2) = 2 (n S_w / d) (G M_B / (b v^2)) (1 + gamma_PPN v^2 / c^2),   k_a(b) = (n S_w / d) G M_B / (b c^2),

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
+- 0.025 at gamma_PPN = 1 (DETECTOR); the verdicts CANNOT CLOSE on the
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
gamma, T'_n = ceil(n sqrt(W) / m), later than the whole-root gate's
T_n = 1 + floor((n - 1) E' / m) by 0 to 3 intervals on the domain
(exactly 1 at gamma = 2); the exact root-free form with one division
is T_n = min {t : ceil(t m / (n - 1))^2 > W} (DERIVATIONS_BEAM 17.7);
MET in its
domain (series S: the muon's products' face clicks at 369 and 345, z =
0.3674 for 0.369 +- 0.003, DETECTOR; the self-creations 70 and 124,
GAMEBOARD), beside the law's FAIL rows 4a and 4b; one sixth of the
perihelion's advance FOLLOWS from the declared square, the field's
five sixths NEITHER. **The seventh verb** (lorentz-v1, not admitted;
Highlights 5.4, the Lorentz A and B line): a root of the state at run
time slowing a body's own counter by gamma and contracting its bond by
1 / gamma; fails the vector test; the law's own prediction, that a
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
with the three tests and whether it can pass them; a RULE that cannot
pass the three tests is still written as a RULE, and the row then stays
FAIL under the law as it stands. NOTHING: no reading, no declaration
and no rule of any kind, inside or outside the six verbs, moves the
row: it is the law's own exact result and nature refutes the law there.
The counts: READING 1 (row 14); DECLARATION 6 (rows 2a, 4a, 4b, 8b, 8c,
13); RULE 8 (rows 1c, 3, 5b, 6, 7b, 8a, 11a, 11c); NOTHING 1 (row 1b).
Sixteen rows: the twelve FAIL rows of the paper's confrontation table
and the four that fail by a pin whose run is not made (4a, 5b, 11a,
11c).

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
| 2a the two-slit visibility | 0.966 in the clicks (DETECTOR); the pin 0.9659 (COMPUTATION, met bit for bit); nature 0.98 (a Mach-Zehnder source), 0.94 (a biprism, unverified) | SHOWN: the counts per cell bit for bit from the fan, the weights and the wheel; the ideal 1 the limit of every direction; the shortfall the digital lines' landings | DECLARATION: the fan's width P and the grain of the slits' world; the options 0.94, 0.97, 0.96 at P = 32, 48, 64 (COMPUTATION) do not reach 0.98; NOT COMPARED against a two-slit source until its figure is verified | F; NO |
| 3 the deceleration | q = -0.108 registered, -0.104 at head (DETECTOR, the pointer's z per tick, that tick GAMEBOARD); nature -0.53 +- 0.01 | SHOWN: the coasting throw gives Milne's q = 0 exactly; SHOWN IN FORM: q_eff = -2 g_1 / (1 + g_1) from any linear stretch of the emitters' clocks (chapter 5.7); NOT SHOWN: the size g_1 = 0.36 and its sign from the law's own crowd | RULE: a term that makes the emitters' count stretch grow with the flight time by the law's own crowd, at the size 0.36 per Hubble length; the law's own crowd history gives the wrong sign; a declared gradient a fit | A and C; YES (the tick of an open-face detector as the time base) |
| 4a the unslowed clock | the muon's `become` at 64 at every speed (GAMEBOARD, a body's own record; the products' face clicks DETECTOR); the ratio 1 against nature's 29.33 | SHOWN: on the law r_D = 1 at every speed, the hop costing the clock nothing; SHOWN IN FORM under covariant-readings-v1: r = 1 / gamma exact on the identity's integers within gamma <= 2; NOT SHOWN: r read at the ground through a mover's own records | DECLARATION: the key `covariant_readings` (one rate for the drive and the clock of one record), and the lifting of its domain cap by form B; off, FAIL by 29.33; on, gamma's form within the domain; the reading that decides from the clicks alone: k_AB, the missing direction | C, audited A; YES (the `become` line, a body's own record) |
| 4b the moving lamp's redshift | z = 0.2636 registered, 0.2647 at head at beta = 0.2674 (DETECTOR; the tick GAMEBOARD); nature 0.315; under the key 0.3674 for 0.369 +- 0.003 (DETECTOR, series S) | SHOWN: 1 + z = 1 + v exactly, the count of what a rest detector meets (the click theorem's k_BA at r = 1); the two one-way factors apart by 1 - v^2 on the law; SHOWN IN FORM: gamma (1 + beta) under the identity | DECLARATION: the same key as 4a; off, 1 + v, seventeen grains below; on, the pin met; the rest detector in no crowd has r_B = 1 exactly, so the NOT READ clock adds nothing here | C, audited A; YES (the tick as the time base) |
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
from the bilinear form's offers and the rungs; row 9's Malus cells on
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
first (mode C's one rate, rows 4a and 4b, one decision, no run; mode
D's turned phase read as a rate, rows 8b and 8c, one declaration and a
run of seconds; row 13, the owner's word on gamma_PPN = 1; row 14, the
moving detector's click, a world of minutes to an hour; then 2a, 8a,
7b, 6, 3 and 11a, 11c, 5b, 1c, 1b), yielding to the owner's orders in
force on rows 13 and 14; the items that are the owner's own decisions
(4a and 4b's key, 13's strength, "a read at a body is a click") are put
to him one line each.

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
the physics is the neighbourhood, through the front, c and the table").

**(ii) What the choice forces: the 48, and the 24 within them.** "What
is not chosen: the group of 48. The cube's group (the signed
permutations of the three axes, 3! x 2^3 = 48; the 24 of hand +1 the
rotations, the 24 of hand -1 the reflections, told apart by the hand as
a pseudoscalar) is the symmetry of choice 1: every map that preserves
the six Ports as a set and the lattice's Links is one of the 48, and
every one of the 48 does. Nothing was added to it; the mass ... lives
on the amounts, on which the 48 act trivially" (FULL_PICTURE section 1,
verbatim); every Bravais lattice's point group is a subgroup of the
full octahedral group O_h of order 48, the crystallographic restriction,
so a lattice can only keep the 48. Over the integers the only
bijections that preserve the cone of one Link per interval are these
48; a boost is not Z-linear, so no boost is among them, and Lorentz's
form is reached Outside from the clicks (chapter 5.1) and not as a
symmetry of the lattice. The determinant splits the 48: the 24
rotations, the group of order 24, isomorphic to S_4 on the cube's four
body diagonals, and the 24 reflections; the hand, needed to carry spin
and polarisation (hand-v1, record 128), is the pseudoscalar that tells
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
**p**, so the square m^2 + 3 **p** . **p** follows). In one sentence: the
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

**(v) The owner's sentence, the chapter's close** (record 1109): the
GameBoard showed that everything converges to this group and this ring,
and what did not converge was not put in.
