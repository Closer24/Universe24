# The plan of docs/ALGEBRA.md, the one canonical statement of the algebra: the table of contents, the source map, the conflicts, the header text, the estimate (the Algebra Unifier, 2026-09-23)

The order (the Boss, 2026-09-23, one bounded task, step 1 of two): the
model owner's word of 2026-09-23 about 00:5xZ ([record 1128](../../LOG_2026-09-20.md),
on `claude/universe24-new-3ytqde` until it merges; the Boss's
translation: "It is simply all the algebra; let us unify it into one
place; no need for several files there, if it works out") and the
Boss's judgement that it works out as ONE canonical document,
`docs/ALGEBRA.md`, in the order the paper will take ([record 1099](../../LOG_2026-09-20.md):
the algebra first, then what follows, the way, how the group was
reached, the comparison), each rule stated ONCE, every existing file
kept as the record and given a short header pointing to the one
document (the one-source rule of [AGENTS.md](../../../AGENTS.md): one
canonical copy; consumers reference it; nothing deleted). This file is
step 1: the table of contents of the one document (section (a)), the
source map (section (b): which paragraph of which file goes where, what
is kept as a record and what the one document now states alone, and
every place two sources state one rule differently), the header text
for each source (section (c)) and the estimate (section (d)). Step 2,
the document itself, waits for the chief physicist's page
`docs/GROUP_STRUCTURE.md` (the branch `group-structure`, head
`e99a1afa`, its PR open; the Boss's addition of 2026-09-23 about
01:30Z) to merge, so that chapter 1 is his page and not a second
definition of the groups.

Docs only: no code, no run, no law changed, no number moved, nothing
deleted. Base commit `e404baa` (`origin/main`, "Merge pull request
#965"). Sources read on `origin/main` unless a branch is named: record
1128 and its Highlights line on `claude/universe24-new-3ytqde`
(`01161389`); `docs/GROUP_STRUCTURE.md` on `group-structure`
(`e99a1afa`, sections 1 to 11); `docs/designs/fail_rows/WHAT_IS_MISSING.md` on `fail-rows`
(`2252bbdf`, read AE folded; its last lines are being folded now, and
step 2 takes the merge SHA). Every symbol below is named in English at
its first use; a scalar plain, a vector bold lowercase (**p**), an
operator bold uppercase (**F**). Every number carries its kind:
DETECTOR (a click or a count of clicks at a declared detector, the
only kind compared with nature), GAMEBOARD (the host's view of the
board, a diagnostic), COMPUTATION (the algebra's closed form, no run),
HOST (a cost or a time of the machine), CONVERSION (an Outside number
made from counts by a named reading). Every result is stated as
matching nature, never as how nature is; Newton's, Einstein's,
Lorentz's, Bohr's and Balmer's forms appear only as the thing compared
with. The group is called the group of order 24 everywhere (the
rotation group of the cube, isomorphic to S_4, the symmetric group on
four things; never "S24"; the owner's word of [record 1114](../../LOG_2026-09-20.md),
Highlights 5.4).

**The six lines, first.** (1) The information: the document moves no
row and no count; it moves statements between files: every rule of the
algebra from its scattered sources (seventeen files, about 1.7 MB of
prose, of which the algebra proper is about a tenth) into one file, and
a one-sentence header the other way, into each source. (2) The generic
solution: one document in the paper's order, one statement per rule,
every other file a record with a pointer; no rule restated twice, so
that a later change is made in one place. (3) Why it will work: every
rule of the algebra already has one owning statement in the tree (the
source map names it for each paragraph), and the paper's abstract and
theorems already agree with those statements; the document is a
gathering with links to the proofs, not a derivation. The reading that
would refute it: a conflict of section (b.6), where two sources give
one rule two forms that cannot both stand; fourteen are listed, and
none is decided here. (4) Why do this at all: a reader of the paper, a
reviewer, a new session and the owner's own batches today find the
algebra in seventeen files and the same rule in two to four wordings;
the paper's Part 1 has no mirror in the tree. (5) The Highlights: kept,
every line of 5.4 on the six verbs (records 181, 202), the three tests
(record 202), the reading rule (records 205, 210, 281, 1104), the kinds
(record 281), "matches nature" (record 762), the group's name (record
1114), the unification (record 1128); none needs to change; a conflict
of section (b.6) that the owner decides would be a new line beside the
one it refines, on his word. (6) The implementation: documents only:
one new file `docs/ALGEBRA.md` (step 2), one header line in each of
the seventeen source files, one row in `docs/README.md`; no engine, no
register, no identity; the time is in section (d) (HOST); not
dangerous: no key, no run, no number moves, and `tools/check.py`
guards the links and the language.

**The symbols, named once.** N the phase circle's grain (the paper's
N_phi; 64 on the register); Z_N the integers modulo N, the phase
circle; Z[Z_N] its integer group ring, a record's rows at a Node one
element f of it; zeta_N the primitive N-th root of unity; Z[zeta_N] the
cyclotomic integers, the ring the rows live in after the cancel; ev the
evaluation Z[Z_N] -> Z[zeta_N]; **G** the click's Gram matrix; **E**
the 2 x N matrix of the tables C and S at the scale 256; **F** the
interval's map on the state vector **s** with its rate vector **r** and
wall d; Q the label's scale (the paper's N_l, 64); S_w the push's width
(the paper's N_w); T_D the flight period of a direction D; c the pace
of a light row, 1 / sqrt 3 Links per interval in the limit of every
direction, 32 / 55 on a heading; v a pace in Links per interval; r a
detector's own count per interval against the tick, the click
theorem's one free number; k_AB and k_BA the two one-way count ratios
of the click theorem; gamma the Lorentz factor 1 / sqrt(1 - v^2 / c^2),
as the thing compared with; h the action per Link of a row's phase
turn; M a body's content in units; n / d the suspension pair; k =
a_tau n / d the crowd's stretch of a count with a_tau the age moment;
gamma_PPN the world key `optical`'s declared strength; c_f = 1 +
gamma_PPN the flight's coefficient; (A1), (A2), (A3) the click frame's
hypotheses (defined in section (a), chapter 5).

---

## (a) The table of contents of docs/ALGEBRA.md, in the paper's order

The paper's order (record 1099, the plan of `paper-algebra-first`): the
algebra first (the group, the ring, the six operations), then what
follows from it (exact; under hypotheses), the way (the click), how the
group was reached, the comparison (what each FAIL row lacks). The one
document has seven chapters and nothing else; each rule appears in one
chapter and is linked from every other place it is needed. Every
paragraph carries its source in a bracket (the file and section of
section (b)), so that the proof is one link away and the document
itself proves nothing anew.

### Chapter 1. The objects: the four group objects (by reference until the group page lands)

Chapter 1 is the chief physicist's page `docs/GROUP_STRUCTURE.md`
(`group-structure` at `e99a1afa`), by reference: its sections 1 to 3
in full (1 the definitions in symbols: the six Ports with the opposite
involution as the cube; G_48 the signed permutation matrices, B_3 =
O_h; G_24 = ker det, isomorphic to S_4, "the group of order 24"; the
action on Z^3, the labels and the Nodes; Z_N and Z[Z_N] with the merge
and the cancel; the translations; the cyclic action on the 3^8 slot
states; the state of a Node and the one operator per interval; 2 the
dictionary from the algebra to the physics, seventeen rows, mass =
content, momentum = the label, energy = Q S M and the exact square,
time = counts, c = the flight operator's norm, a measurement = a click,
each with its owner document; 3 how the group was reached from the
operations, six items), his sections 4 to 11 (the names, the objects,
the action table, where each definition lives, every naming of 24 and
48 verbatim) the index the chapter links to. The page itself is kept as
the record with the header of section (c). The unifier writes no
second definition of any group and no second dictionary: chapter 1 of
the document is one paragraph naming the four objects in this order,
each with the link to his section:

1. The symmetry group of the cube: the 48 signed permutations of the
   three axes, with the hand as its pseudoscalar; the group of order
   24 its kernel under the determinant, the rotations (the paper's
   Theorem 1, "the 24 of the name"). The 48 are not chosen: they are
   forced by the one choice, the six Ports of a Node.
2. The phase circle Z_N and its group ring Z[Z_N]; a record's rows at a
   Node one element; the merge its addition with the cancel
   [p + N/2] = -[p].
3. The translation group of the torus, Z_X x Z_Y x Z_Z per world.
4. The collision as the cyclic group's action on the 3^8 slot states of
   a Node, its orbits the collision classes.

How his page enters (the Boss's word of 2026-09-23, about 01:30Z):
by reference, sections 1 to 3 in full, not a second statement; the page
kept as the record with the header. Chapter 7 of the document (how the
group was reached) is then his section 3 by reference too, with the
twenty-five dated steps of HISTORY.md and record 1109 beside it, so
that the answer to "how did you reach this group" is stated once.

### Chapter 2. The ring and the six operations as maps, in symbols

The one central formula, boxed, the interval's map per component of the
state (the paper's equation (map), DERIVATIONS_BEAM's Eq. (1)):

    s <- s + r;   e <- sign(s) min(floor(abs(s) / d), a);   s <- s - e d

every rate r and every wall d of it made of the six operations and
nothing else. Then the six, each as a map on the ring and on the
lattice, one paragraph each, in the one fixed order and with the one
fixed letter (the conflict K1 of section (b.6) decides the wording, the
Boss and the owner decide it):

- 2.1 (T) the translation of an accumulator by its rate: x -> x + r on
  Z^k or on a torus; the flight on the digital line (the closed form
  m_D(tau) = floor((2 tau S_1 Q + T_D) / (2 T_D))), the phase's turn,
  the age, every count.
- 2.2 (B) the bilinear form with a declared matrix: the moments of
  order 0, 1, 2 of the arrivals; the coupling **r** = **C** **a**; the
  click's weight f^T **G** f with **G** = **E**^T **E**.
- 2.3 (G) the group-ring addition in Z[Z_N]: the merge of identical
  rows; the cancel [p + N/2] = -[p]; the normal form in
  Z[x] / (x^(N/2) + 1) = Z[zeta_N] for N a power of two.
- 2.4 (P) the permutation of the joint state: the collision's cyclic
  shift, the meeting's arc, the gate (CNOT), the apportioning's tie; a
  permutation of directions or Nodes, never of contents.
- 2.5 (E) the evaluation ev: Z[Z_N] -> Z[zeta_N], ev(f) = sum_p f_p
  zeta_N^p, a surjective ring homomorphism with kernel (x^(N/2) + 1),
  the merge's cancel; then the norm abs(ev f)^2 and the ladder on the
  wheel; the built tables C and S at 256 a Z-linear map into Z^2 that is
  not a ring homomorphism (the rounding, stated as its own line).
- 2.6 (D) the division with the remainder kept and the comparison: the
  carry that is the event, the ladder's cell 2 T u + T <= 2 N C_k, an
  age against a key, a phase against a window.
- 2.7 What is not one of the six: a root of the state at run time (the
  seventh verb; the meeting's norm and the pushed row's pair under
  `optical`, the two run-time roots named in COUPLINGS section 3);
  Lorentz's gamma on a body's own counter and a bond's contraction.
- 2.8 The three tests every rule passes (generic, vector, local), one
  line each, by reference to skills/workflow.md.
- 2.9 The couplings as verbs: the one table of COUPLINGS.md section 1,
  by reference (31 rows), with its one-line result: every rule the atom
  and light worlds run is one of the six or a stated composition, with
  the two run-time roots as the exceptions.
- 2.10 The quantities as algebraic objects: the table of HISTORY.md
  ("The physical quantities, when each entered, where it lives, and
  which of the six verbs act on it"), by reference, its fifteen rows
  named in one line each (the amount on Z; the content on Z, the
  non-compact scale; the phase on Z_N; the multiplicity; the age; the
  momentum vector; the charge as a rational pair; the label flow and
  the moments; the family table as the declared input; the couplings as
  integer matrices; the wheel's coordinate on Z_W; Born's rule as the
  bilinear form; the hand and the axis under the 48; the clock's
  counts).

### Chapter 3. The click-to-click algebra and the reading rule

- 3.1 The two worlds: Inside (the Nodes, the integer rows, the tick,
  where no one measures) and Outside (the detectors and their clicks
  only). The click: the event of receiving a packet at a detector's
  Node, stamped with the detector's own count; the one comparison, the
  one deletion, the one non-local step.
- 3.2 The reading rule, one sentence (the owner's central idea, record
  1104; the paper's abstract, record 1115): a click at a detector, a
  count between clicks on the detector's own record, and a ratio of
  such counts are what is compared with nature; nothing measured inside
  the board is compared; a GameBoard reading is a diagnostic. The five
  kinds of a number, one line each.
- 3.3 The count ratios: k_AB (B's own count between two arrivals of A's
  records, over T) and k_BA; on the law k_AB = r / (1 - v) and k_BA =
  (1 + v) / r exactly in the mean; a ratio of two counts of ONE detector
  is r-free, a ratio of counts of TWO detectors carries r_Y / r_X; the
  place-to-place factor k_XY = (r_Y / r_X) (1 - s . v_X) / (1 - s . v_Y).
- 3.4 The k-ladder: the Outside velocities are the ratios 1 / k with
  the quantum 1 / (k (k + 1)), finest near c and coarsest near rest; c
  Outside one Link per the least count; the place quantum one Link, the
  time quantum one count, a pulse and its return two (the Outside
  quantum, a theorem of (A1), (A3) and the conversion).
- 3.5 The conversion as a map, in the algebra's own words: Outside =
  rung o (chi_1 of f* f) o ev on the record's element (a ring
  homomorphism, a pure state's square, a threshold, a count ratio); the
  table of names that fit and do not (a ring homomorphism with a
  kernel; a positive quadratic form on a lattice; a state on a
  *-algebra; a group action of the Lorentz group up to scale; not a
  functor, not "Inside modulo a kernel").
- 3.6 The pair: an element of Z[Z_N] (x) Z^2 (x) Z^2 of tensor rank 2;
  the settings as integer matrices U_s with U_s^T U_s = n_s I; the click
  of a pair one gather from both settings, the one non-local operation.

### Chapter 4. The exact identities: one line each and the link to the proof

Exact on the lattice, each stated in one line with its hypotheses (the
declared tables and world conditions) and the link to its proof; no
proof is copied.

- 4.1 The accumulator's closed form at a constant rate, s(t) = floor(s_0
  + r t); the flight's line and period; the k-th Link at tau_k =
  ceil((2 k - 1) T_D / (2 S_1 Q)).
- 4.2 The pace of every direction, c_D = Q abs(D) / T_D, with c <= 1 /
  sqrt 3 (Cauchy-Schwarz, equality on the diagonals; c the operator
  norm of the flight) and the Manhattan bound; 32 / 55 on a heading.
- 4.3 The books: released = in transit + absorbed + escaped (+
  cancelled) per family, in amount and in content, at every interval;
  the continuity equation from the books with its error term.
- 4.4 Gauss's law of a free family's flux: the amount crossed over a
  closed surface's Ports equals the charge enclosed (GAMEBOARD, the
  probes' reading).
- 4.5 Theorem 1 (the 24 of the name): by reference to chapter 1.
- 4.6 Theorem 2 (the split is an isometry): sum w_i^2 / m_i = w^2 / m for
  every integer table; the conjugate transpose inverts it up to the
  scaling by A; the rotation U_s^T U_s = n_s I exactly, an isometry up
  to the tables' rounding.
- 4.7 Theorem 3 (the interval is injective between clicks): M o R o S o
  F induces an injective Z-linear map of the quotient that forgets the
  age; the click the one deletion; a collision a non-linear bijection.
- 4.8 Theorem 4 (the quadratic read-out, a lattice Gleason): under (a)
  to (e), N a power of two, A_2 = 2, R(f) = sum over odd j of c_j
  abs(sigma_j(f))^2, c_j >= 0; the built f^T **G** f is its fundamental
  to the tables' rounding; the bit-identity of (E f)^T (E f) and f^T
  (E^T E) f.
- 4.9 Theorem 5 (exact count marginals): the first party's outcome is a
  function of u alone; the second's count of + is N / 2 exactly off a
  tie; no tie at the twelve grains.
- 4.10 The finite-N Bell value: S(N) = 8 (c_1 + c_1') / N - 4, an exact
  rational; abs(S(N) - 2 sqrt 2) <= 8 / N + 0.0444; 11 / 4 at 64, 181 /
  64 from 512 to 8192; the local bound S <= 2 an identity of every local
  read-out (the phase-form window).
- 4.11 E = h f as an identity of the release (E = h s = (h N) f); the
  cost of a record; the entropy identity bits read + bits erased = log2
  N per record; the support bound abs(supp f) abs(supp f_hat) >= N and
  the Weyl relation V U = omega U V.
- 4.12 The event-driven form bit-identical to the interval stepping;
  two events at one t* commute exactly when their Nodes are disjoint;
  the feedback block has no closed form across events.
- 4.13 The theorem of covariant readings for the linear block; the
  minimal-mass theorem (the smallest whole-charge content is the reduced
  denominator d).
- 4.14 The negative result: the constancy of c is not a theorem of the
  six verbs with locality; it is the declared postulate P9 (DERIVATIONS_BEAM
  section 27).

### Chapter 5. What is reached under named hypotheses, each with its hypotheses and its kind

The hypotheses named once at the head of the chapter, verbatim from
their owning files: (A1) a click is the passage of information from
Node to Node, at most one Node per interval, c the unit, the same in
every family; (A2) a click's content is an amplitude with a phase that
splits each interval between staying and hopping, the mass the staying
share (the law's rows do not have it: they hop whole); (A3) locality
Outside: every Outside passage is a chain of clicks between
neighbouring places (the owner's named assumption; the click frame
states it as a theorem of (A1) with P6: conflict K10). Then the five
assumptions of the law as built for Newton (W1) to (W5) and the shell
mean (M), by reference. Each result below carries: its hypotheses, the
limit taken, the order of the expansion, its error term, its status
(SHOWN / SHOWN IN FORM / MET / FAIL / NOT READ) and its kind.

- 5.1 The click theorem (Lorentz's factors): the transformations that
  keep (A1) form the Lorentz group up to scale; the r-free lines (the
  round trip (1 + v) / (1 - v), the composition w = (v_R - v) / (1 - v
  v_R), the aberration) exact from (A1), (A3) and the conversion; the
  scaled lines Einstein's if and only if r^2 = 1 - v^2 (the one line
  k_AB = k_BA), which (A2) gives up to a correction of relative order
  m^2 v^2 / 6 and the law as built, at r = 1, does not; the 48 contain
  no boost, so the symmetry is Outside and not Inside.
- 5.2 The radar and Einstein's definition (adopted, named): x_D = (n_r -
  n_e) / 2, t_D = (n_r + n_e) / 2; (t_D, x_D) = lambda Lorentz_v (t_1,
  X) with lambda = r_D gamma.
- 5.3 The energy-momentum relation and the identity W = E'_0^2 + 3 **p**
  . **p** (the step's invariant, not the step); E^2 - p^2 = E_0^2 (1 -
  v^2) / r^2; E_0 = m_i c^2 a unit, a declaration; the momentum's
  second-order FAIL on the law (conflict K8).
- 5.4 The equivalence principle: exact in the gravity column and the
  drive (p = M_A sum V, Lambda = 1) for bodies; not for rows; a
  hypothesis for a bound body; the accelerated detector's count ratio
  k_XY = 1 / (1 - g Y / c^2) to first order; the equivalence constant
  delta k = (n S_w / d) (g Y / c^2), nature's if and only if n S_w = d
  (the pin II.10a), at rest only.
- 5.5 Einstein's step, one definition (conflict K3 decides which): the
  image of the Inside step under the conversion, the most general form
  the Outside step takes (dp / dt = F with p = gamma m v; E^2 = E_0^2 +
  c^2 p^2; d tau / dt = sqrt(1 - v^2); the geodesic's first terms).
- 5.6 Newton's form (conflict K2 decides the wording of the limit): the
  second law as the second difference of arrival Nodes over the
  detector's ordinals; the inertia in one form abs(p_a) = m_i (Nodes
  hopped) / (counts at rest between hops) with r = 1 Newton's, r =
  sqrt(1 - v^2) Einstein's, r = 1 - v the drive's as built; the
  velocity term (1 + u / c) produced for every count that is a click;
  the 1 / r of the potential and the 1 / r^2 of the push in the shell
  mean, a = -G M_B / r^2 with G = K (n / d) / (4 pi S_w) (conflict K11
  on the letter), retarded at c; the third law at rest; Kepler's period
  T = 2 pi r (S_w + n) / n; the value of G a declared input.
- 5.7 Light Outside: the pace of light c_D = Q abs(D) / T_D read by the
  arrival count over the Euclidean distance; E = h f declared at the
  release and recovered at the click; the intensity 1 / r^2 in the shell
  mean; the Doppler of a moving detector 1 / (1 -+ v) and of a moving
  lamp 1 +- v, exact at first order, FAIL at second; the aberration tan
  alpha = v / c_D; the fringes C(y) / W = (2 + 2 cos(2 pi (L_1 - L_2) /
  lambda)) / Z + O(1 / 2N) + O(1 / W); Malus P(pass) = cos^2 theta
  within the tables' rounding; the redshift through a crowd 1 + z_d =
  (1 + k_A) / (1 + k_B), rung 1, and its second order 1 - k + k^2
  against nature's 1 - k - k^2 / 2; the apparent acceleration q_eff =
  -2 g_1 / (1 + g_1) a property of the conversion, its size an input.
- 5.8 The atom's congruences: a loop closes exactly when Delta A_a = 0
  mod h on each axis and (Delta A_x + Delta A_y + Delta A_z) / h = j N,
  j whole (three congruences and one sum, no grain); Bohr's action
  quantization the thing it becomes in the limit; the ladder a_j / a_i =
  (j / i)^2 and T_j / T_i = (j / i)^3 in the shell mean, read as two
  circle counts and two periods at a detector; on the lattice the
  exponent 2 / (3 - k) = 1.709 at k = 1.83; the reach of one click 2 i^2
  >= j^2 (Balmer's i = 2 not reachable from j = 4 by one click); a
  release unbinds; the transition NOT IN THE LAW (`atom-give-v1` a
  named rule outside it); Balmer's 27 / 20 the thing compared with,
  NOT READ.
- 5.9 The walk past a mass: the step rule as three verbs (the walk s +=
  r_0 d against the wall w_0 (d + c_f n A); the push **W** -= n weight_D
  **V**; the label by comparison), the crowd A(r) and the flow **V**(r)
  from the arrivals' ages and directions; the bending the push's alone,
  the delay the wall's alone; the deflection alpha = 2 c_f (n S_w / d) G
  M_B / (c^2 b) in the straight-path limit (SHOWN IN FORM, the 2 of c_f
  an input; conflict K9 on the two mechanisms); the Shapiro delay c_f (n
  S_w / d) (G M_B / c^3) ln(4 r_1 r_2 / b^2); on the registered geometry
  C_ring = 3.65 / 3.82 / 3.92 at b = 6 / 3 / 8 under `flow_link` at
  gamma_PPN = 1 against the continuum's 4 (COMPUTATION), the law as
  built 0.000 pixel (DETECTOR, series K).
- 5.10 The relations reached only under an identity beside the law
  (covariant-readings-v1: r = E'_0 / E' exact on the identity's
  integers, the gate t^2 m^2 >= n^2 W with no root; the seventh verb's
  gamma and contraction, not admitted): one line each, under their
  identities, so that chapter 6 can name them.

### Chapter 6. What each FAIL row lacks, by the algebra

- 6.1 The four words (READING, DECLARATION, RULE, NOTHING), verbatim
  from WHAT_IS_MISSING.md's definition; the seven generic modes in the
  clicks (A: a GameBoard quantity taken as the reading; B: a read
  counted as a click or a click as a read; C: one record with two
  rates; D: the click reads the birth content and not the rate at the
  arrival; E: a transformation fired at a declared count and not at a
  met row; F: the click's grain; G: the click's order), one line each.
- 6.2 One line per FAIL row, sixteen rows, in the file's order, each
  with the pinned reading and its kind, what the algebra gives exactly,
  the one word and the modes, and the inside-the-board line:

| Row | The word | The modes; inside the board |
| --- | --- | --- |
| 1b the phase-form window | NOTHING | none; NO |
| 1c the order channel | RULE (a wheel that is not a counter) | G; NO |
| 2a the two-slit visibility | DECLARATION (the fan's width and the grain) | F; NO |
| 3 the deceleration | RULE (the emitters' stretch growing with the flight time, the law's crowd of the wrong sign) | A and C; YES (the tick) |
| 4a the unslowed clock | DECLARATION (the key `covariant_readings`) | C, audited A; YES (a body's own record) |
| 4b the moving lamp's redshift | DECLARATION (the same key) | C, audited A; YES (the tick) |
| 5b the arms' anisotropy | RULE (a contraction, the seventh verb) | A and C; YES, wholly |
| 6 the atom's loop opening | RULE (the give at the closure, `atom-give-v1`) | F and E; YES in part |
| 7b the strong ratio | RULE (a give that grows with the bonds) | E; NO |
| 8a the neutron's step | RULE (`decay-by-crowd-v1`) | E, audited A; YES for the paper's number |
| 8b the neutrino's passage | DECLARATION (the `nu` family's content under `massive_rows`) | D; NO |
| 8c the massless neutrino | DECLARATION (the `nu` quantum 1) | D; NO |
| 11a the far lamp's brightness | RULE (a click whose read energy follows the row's frequency in flight) | D and A; YES |
| 11c Tolman's test | RULE (an angular size growing with the redshift, beyond the verbs) | D and A; YES |
| 13 light bending | DECLARATION (gamma_PPN = 1) | A in part; YES in one input (k_a(b)) |
| 14 Newton's periods | READING (the moving detector's arrival click) | A, B and C; YES, three times |

- 6.3 Why the rows that passed passed, by the algebra (WHAT_IS_MISSING
  section 0b): one sentence: each reads a count of clicks or a ratio
  of two counts at a declared detector from a formula exact on the
  law's integers (the rungs, the tables, the flight table, the window)
  with no shell mean, no tick and no body's own record in the chain;
  the FAIL rows are the same chain with one thing missing. The table
  by reference.
- 6.4 The order to take them in (WHAT_IS_MISSING section 2, the Boss's
  order of record 1128 (a)), by reference: one line.

### Chapter 7. How the group was reached, from one Node and its six neighbours (one page)

Gathered, not written anew (record 1109: "we reached it from the
Nodes, a Node and its neighbours; between Nodes, the GameBoard; through
the GameBoard we reached this group; the GameBoard showed us that
everything converges to this group"): (i) the one choice, the six
Ports of a Node, the L1 neighbourhood of the cubic lattice, and the
seven Nodes of the causal front; (ii) what is forced by it: every map
that preserves the six Ports as a set and the lattice's Links is one
of the 48, and every one of the 48 does; no three-dimensional lattice
has a larger point group; the determinant splits them, 24 rotations
and 24 reflections, the hand telling them apart; (iii) the other two
choices, the phase circle and the torus, and that nothing was added to
the 48 (the mass lives on the amounts, on which the 48 act trivially);
(iv) the twenty-five dated steps of the transition (HISTORY.md, 09-17
to 09-22), named in one line each: the shared quantum resource deleted;
the amplitude a phase and a content; a force a catalog entry; the Born
table computed from N; the law of events; the law of the ray; the
moments as the one reading; E = h f; one mechanism, a column with a
sign; two kinds of readings; masses and charges the initialisation;
the amplitude law; the fraction-free law; Doppler by itself; the fan
and the exact phase; the whole law one vector operation, the six
verbs; the click without amplitudes, the record in Z[Z_N]; the vector
program from group theory; the world through a detector; Lorentz A and
B, the seventh verb refused; the clock's word the age moment; the
detector's clock in the age wall's set; the click theorem; the paper's
framing; the three formulas; (v) the owner's sentence, that what did
not converge to the group and the ring was not put in.

---

## (b) The source map

One row per paragraph or theorem of the one document: the chapter and
paragraph; the source file and section with its lines on `origin/main`
(a branch named where not); whether the source is kept as the record
with the header of section (c) (KEPT), or whether the one document is
now the only statement of that paragraph (ONLY: a gathering or a
sentence no source states as such). Every source in this map is KEPT;
nothing is deleted; ONLY marks the paragraphs the document adds as the
join between sources, each made of the sources' own sentences.

### (b.1) Chapter 1, the objects

| Paragraph | Source | Kept / only |
| --- | --- | --- |
| 1 the definitions in symbols (the cube, G_48, G_24, the action on the state, Z_N and Z[Z_N], the translations, the collision, the state and the operator) | `docs/GROUP_STRUCTURE.md` section 1 (branch `group-structure`, `e99a1afa`, lines 15-83) | KEPT (by reference, in full; the Boss's word) |
| 1 the dictionary from the algebra to the physics (seventeen rows) | `docs/GROUP_STRUCTURE.md` section 2, lines 84-116 | KEPT (by reference, in full; the document adds no row) |
| 1 how the group was reached from the operations (six items) | `docs/GROUP_STRUCTURE.md` section 3, lines 117-184 | KEPT (by reference, in full; chapter 7 links here) |
| 1 the names fixed by the owner; the four objects; the operations between them; the action of the 48, one table; where each definition lives; every 24/48 wording | `docs/GROUP_STRUCTURE.md` sections 4 to 11, lines 185-361 | KEPT (the index the chapter links to) |
| 1.1 Theorem 1, the 24 of the name | `paper/general_formula/main.tex` lines 309-317 (`th:group`) | KEPT (the paper is the mirror, not a source with a header) |
| 1.1 the 48 not chosen; the crystallographic restriction | `docs/FULL_PICTURE.md` section 1, lines 36-110 ("The choices, and what follows from them"; "What is not chosen: the group of 48", lines 54-66) | KEPT |
| 1.1 the hand as the pseudoscalar, h -> det(g) h; the axial record a -> det(g) g a | `docs/designs/hand/FORM.md` sections 1 and 2, lines 16-76; the verdict line 192 | KEPT |
| 1.2 the ring Z[Z_N], the record as an element f | `docs/DERIVATIONS_BEAM.md` symbol table line 78; section 0 lines 148-160; section 6.5 lines 1570-1588 | KEPT |
| 1.4 the collision as the cyclic action | `docs/DERIVATIONS_BEAM.md` section 1.2 line 342; `GROUP_STRUCTURE.md` sections 1 and 7 | KEPT |

### (b.2) Chapter 2, the ring and the six operations

| Paragraph | Source | Kept / only |
| --- | --- | --- |
| 2.0 the central formula, boxed | `paper/general_formula/main.tex` equation `eq:map` (lines 56-66); `DERIVATIONS_BEAM.md` Eq. (1) line 108; `FULL_PICTURE.md` section 3 table line 168 | KEPT |
| 2.0 the six, the list in one sentence | `docs/HIGHLIGHTS.md` 5.4 item 3 (line 19) and "The six operations" (line 877); `docs/TERMINOLOGY.md` "The six verbs" (lines 157-162); `skills/workflow.md` "The three tests", test 2 | KEPT (Highlights and Terminology carry no header: they are the law's and the glossary's; they link to the document instead) |
| 2.1 (T) | `DERIVATIONS_BEAM.md` section 1 lines 265-273; the closed form line 157; the flight 11.1 lines 2495-2510 | KEPT |
| 2.2 (B) | `DERIVATIONS_BEAM.md` section 1 lines 274-277; 6.7 lines 1813-1865 (the Gram form) | KEPT |
| 2.3 (G) | `DERIVATIONS_BEAM.md` section 1 lines 278-279; 1.2 line 402 (the merge); 6.5 lines 1575-1583 (the cancel as the quotient); 6.7 lines 1850-1854 (the antipodal pair killed exactly) | KEPT |
| 2.4 (P) | `DERIVATIONS_BEAM.md` section 1 lines 280-281; 1.2 lines 342 (the collision), 347 (the meeting's arc), 381 (the gate), 382 (the apportioning) | KEPT |
| 2.5 (E) the exact evaluation and the built tables | `DERIVATIONS_BEAM.md` section 1 lines 282-283; 6.7 lines 1872-1876; `click_frame/DERIVATION.md` section 9 (2) (a), lines 1464-1481 | KEPT |
| 2.6 (D) and the comparison | `DERIVATIONS_BEAM.md` section 1 lines 284-287; section 0 lines 169-172 (the ladder's cell) | KEPT |
| 2.7 what is not one of the six | `DERIVATIONS_BEAM.md` 10.4 lines 2428-2436; `FULL_PICTURE.md` line 278; `couplings_algebra/COUPLINGS.md` section 3 lines 241-251 (the two run-time roots) | KEPT |
| 2.8 the three tests | `skills/workflow.md` "The three tests of every rule"; `HIGHLIGHTS.md` 5.4 item 4 | KEPT (by reference; no header on a skill) |
| 2.9 the couplings as verbs | `couplings_algebra/COUPLINGS.md` section 1 lines 154-194 (31 rows), section 3 | KEPT (the table by reference, not copied) |
| 2.10 the quantities as objects | `algebra_transition/HISTORY.md` "The physical quantities ..." lines 1516-1548 (15 rows) | KEPT (by reference) |
| 2.x the verbs in step order at one interval (1, 6, 2, 3 and 5, 4) | `click_frame/DERIVATION.md` section 9 (I), lines 1266-1284 | KEPT |
| 2.x the split as an integer matrix, A = sum a_i^2 | `DERIVATIONS_BEAM.md` 1.2 line 379; 6.1 line 1354 | KEPT |
| 2.x the pair's arms in Z^2 (x) Z^2 | `click_frame/DERIVATION.md` lines 1437-1438; `ENTANGLEMENT_PAGE.md` lines 15-16 | KEPT |

### (b.3) Chapter 3, the click-to-click algebra and the reading rule

| Paragraph | Source | Kept / only |
| --- | --- | --- |
| 3.1 the two worlds, the click | `click_frame/DERIVATION.md` section 0 "Definitions" lines 18-39; section 1 lines 244-270; section 8 lines 990-994 | KEPT |
| 3.2 the reading rule, one sentence | `HIGHLIGHTS.md` 5.4 items 8 and 9 (lines 24-25), the lines of records 1104 and 1115; the paper's abstract (line 46) and opening (line 51); `GROUP_STRUCTURE.md` section 5, "The reading rule"; `WHAT_IS_MISSING.md` lines 26-37 (the kinds) | ONLY as one sentence in the document (the sources state it in five wordings, conflict K5); each source KEPT |
| 3.2 the five kinds | `WHAT_IS_MISSING.md` lines 26-37; `NEWTON_FROM_CLICKS.md` lines 27-38; `NEWTON_ON_THE_SIDE.md` lines 19-28 | KEPT (conflict K6 on the kind of a body's own record) |
| 3.3 k_AB, k_BA, the two factors exact in the mean | `click_frame/DERIVATION.md` section 1 lines 261-266; section 2 (a) lines 274-293; the table 3 lines 352-361 | KEPT |
| 3.3 the place-to-place factor k_XY and its five corollaries | `einstein_outside/DERIVATION.md` Theorem 1, lines 355-397; the r-free fact lines 466-469 | KEPT (conflict K7 on the subscript convention against `light_outside`) |
| 3.4 the k-ladder and the Outside quantum | `click_frame/DERIVATION.md` section 9 (III) lines 1320-1398; `einstein_outside/DERIVATION.md` Theorem 3 lines 524-566; `NEWTON_ON_THE_SIDE.md` lines 116-117, 290-300 (the whole-rung condition E'_D = k p) | KEPT |
| 3.5 the conversion as a map; the names that fit | `click_frame/DERIVATION.md` section 9 (2) lines 1458-1546, (3) lines 1548-1558, (4) and (5) lines 1560-1673; lines 1676-1681 | KEPT |
| 3.5 the conversion table (Inside, Outside, the map, the inverse) | `click_frame/DERIVATION.md` section 7 (3) lines 925-979 | KEPT (by reference) |
| 3.6 the pair, the settings, the one gather | `click_frame/DERIVATION.md` section 10 (1) lines 1713-1739, lines 1850-1860; `ENTANGLEMENT_PAGE.md` paragraphs 1 to 3 | KEPT |

### (b.4) Chapter 4, the exact identities

| Paragraph | Source | Kept / only |
| --- | --- | --- |
| 4.1 the closed forms | `DERIVATIONS_BEAM.md` section 0 line 157; 11.1 lines 2495-2510 | KEPT |
| 4.2 the pace, the bound c <= 1 / sqrt 3 | `DERIVATIONS_BEAM.md` 2.1 lines 634-640; 13.2 (a) lines 3590-3605; `light_outside/DERIVATION.md` II.1 lines 383-501 | KEPT |
| 4.3 the books; the continuity equation | `DERIVATIONS_BEAM.md` 9.1 lines 2145-2147; 25.4 lines 7318-7350; the paper's section 2 paragraph "The GameBoard as a system of information transfer" (line 88) | KEPT |
| 4.4 Gauss's law | `DERIVATIONS_BEAM.md` 3.1 lines 858-867 | KEPT |
| 4.6 Theorem 2 | `paper/general_formula/main.tex` lines 672-680 (`th:isometry`); `DERIVATIONS_BEAM.md` 6.1 line 1354 | KEPT |
| 4.7 Theorem 3 | `paper/general_formula/main.tex` lines 682-690 (`th:bijection`); `DERIVATIONS_BEAM.md` 11.3 lines 2594-2603, 11.5 lines 2719, 2733 | KEPT |
| 4.8 Theorem 4 | `paper/general_formula/main.tex` lines 736-744 (`th:gleason`); `DERIVATIONS_BEAM.md` 6.5 lines 1556-1660 (the hypotheses (a) to (e) lines 1590-1608; the Gram matrix lines 1651-1658); 6.7 lines 1831-1833, 1922-1924 | KEPT |
| 4.9 Theorem 5 | `paper/general_formula/main.tex` lines 798-806 (`th:marginals`); `click_frame/DERIVATION.md` section 10 (2) lines 1741-1807 | KEPT |
| 4.10 the finite-N Bell value; the local bound | `paper/general_formula/main.tex` lines 828-836 (`th:bell`); `click_frame/DERIVATION.md` lines 1770-1803, the table row line 1833; `WHAT_IS_MISSING.md` row 1b | KEPT |
| 4.11 E = h f; the cost; the entropy identity; the support bound | `DERIVATIONS_BEAM.md` 6.4 line 1508; 6.1 line 1389; 14 lines 3847, 3880; 22.1 lines 6583-6591 | KEPT |
| 4.12 the event-driven form | `DERIVATIONS_BEAM.md` 11.3 and 11.5 | KEPT |
| 4.13 covariant readings; the minimal mass | `DERIVATIONS_BEAM.md` 17.1 lines 4607-4631; 16.2 line 4321 | KEPT |
| 4.14 the constancy of c refuted as a theorem | `DERIVATIONS_BEAM.md` 27 lines 7948-8121 | KEPT |
| 4.x the derivation map, one row per formula with status | `DERIVATIONS_BEAM.md` 21.2 lines 6122-6202 (60 rows); 21.4 the Einstein map (E1 to E17) | KEPT (by reference; the document lists no status the map does not) |

### (b.5) Chapter 5, what is reached under named hypotheses

| Paragraph | Source | Kept / only |
| --- | --- | --- |
| 5.0 (A1), (A2) verbatim | `click_frame/DERIVATION.md` lines 42-54; `einstein_outside/DERIVATION.md` lines 160-171; `light_outside/DERIVATION.md` lines 334-339 | KEPT |
| 5.0 (A3) verbatim | `einstein_outside/DERIVATION.md` lines 177-195; `light_outside/DERIVATION.md` lines 346-356 | KEPT (conflict K10) |
| 5.0 (W1) to (W5), (M), (K); (L1) to (L9) | `einstein_outside/DERIVATION.md` lines 196-251; `light_outside/DERIVATION.md` lines 242-333 | KEPT (by reference) |
| 5.1 the click theorem | `click_frame/DERIVATION.md` section 0 lines 96-133 (the statement), 135-197 (the proof sketch), 199-205, 225-228 (the verdict); section 2 (b) lines 295-326 | KEPT |
| 5.1 the r-free lines: the round trip, the composition, the aberration | `einstein_outside/DERIVATION.md` II.2 lines 689-726, II.3 lines 728-769, II.5 lines 823-871 | KEPT |
| 5.1 the correction m^2 v^2 / 6 | `click_frame/DERIVATION.md` lines 116-121, 183-184, 859-903 | KEPT |
| 5.2 the radar | `einstein_outside/DERIVATION.md` Theorem 2 lines 416-464; `click_frame/DERIVATION.md` lines 312-321 | KEPT |
| 5.3 the energy-momentum relation, W | `einstein_outside/DERIVATION.md` II.6 lines 873-953, II.7 lines 955-1002; `click_frame/DERIVATION.md` section 7 (1) lines 832-838; `DERIVATIONS_BEAM.md` 17.7 line 5179 | KEPT (conflict K8) |
| 5.4 the equivalence principle | `DERIVATIONS_BEAM.md` 3.3 lines 949-951, 5.4 line 1257; `click_frame/DERIVATION.md` section 8 (2) (c) lines 1099-1103, (e) lines 1119-1144; `einstein_outside/DERIVATION.md` II.9 lines 1040-1084, II.10a lines 1172-1264; `NEWTON_FROM_CLICKS.md` 1.3 lines 195-232 | KEPT (conflict K12 on the height's letter and the rest-only qualifier) |
| 5.5 Einstein's step | `einstein_outside/DERIVATION.md` section 3 (a) lines 495-522; `NEWTON_FROM_CLICKS.md` lines 204-205, 298-303; `NEWTON_ON_THE_SIDE.md` lines 162-164 | KEPT (conflict K3) |
| 5.6 Newton's form: the second law, the inertia, the velocity term | `NEWTON_FROM_CLICKS.md` 1.4 (a) lines 245-265, (b) lines 267-307, section 2 lines 397-520; `NEWTON_ON_THE_SIDE.md` section 1 lines 106-189 | KEPT (conflict K2 on the limit, K4 on the law's r) |
| 5.6 the 1 / r and 1 / r^2 in the shell mean; G; Kepler | `DERIVATIONS_BEAM.md` 3.3 lines 938-951; `NEWTON_FROM_CLICKS.md` 1.4 (c) lines 309-343; `einstein_outside/DERIVATION.md` Theorem 4 lines 568-583; `click_frame/DERIVATION.md` section 8 (2) (c) line 1094, (d) lines 1105-1117 | KEPT (conflict K11) |
| 5.6 the prescription for the side (the rung k, the reading, the pins) | `NEWTON_ON_THE_SIDE.md` sections 3 and 4 lines 218-564 | KEPT (by reference; the document states the reading and the pins' kinds, not the change list) |
| 5.7 light Outside, one line per formula | `light_outside/DERIVATION.md` II.1 to II.10 lines 383-1352; the verdict table lines 1455-1510 | KEPT |
| 5.7 the apparent acceleration | `light_outside/DARK_ENERGY.md` section 2 lines 98-166, section 4 lines 225-258 | KEPT |
| 5.8 the atom's congruences | `atom_algebra/ALGEBRA.md` section 1 lines 132-214 (the closure), section 2 lines 206-294 (the ladder and the reading), section 3 lines 296-399 (the click, the reach theorem, the release unbinds), section 4 lines 401-414 (the comparison), section 6 lines 457-533 (the verdict) | KEPT |
| 5.8 Bohr's levels in DERIVATIONS_BEAM | `DERIVATIONS_BEAM.md` 7.2 lines 2003-2072; 26.5 lines 7904-7913 | KEPT (conflict K13 on the ladder's status against the atom file) |
| 5.9 the step rule of the walk; the crowd and the flow | `light_bending/STEP_ALGEBRA.md` section 4 lines 163-227 (the rule lines 174-188, the crowd lines 196-201), section 8 (the comb), section 9 (the ring); `flow_weight/ALGEBRA.md` sections 1 to 3 lines 61-160 (the flow label f_D line 35) | KEPT |
| 5.9 the deflection and the delay in form | `NEWTON_FROM_CLICKS.md` section 3 lines 522-741 (lines 615, 643-647, 701, 715); `einstein_outside/DERIVATION.md` II.11 lines 1266-1360 (lines 1320-1328) | KEPT (conflict K9) |
| 5.9 the bending's numbers by kind | `WHAT_IS_MISSING.md` row 13; `flow_weight/ALGEBRA.md` lines 43-44; `STEP_ALGEBRA.md` section 0 | KEPT |
| 5.10 covariant-readings-v1; the seventh verb | `DERIVATIONS_BEAM.md` 17.6, 17.7 lines 5168-5191; 4.3 lines 1083-1094; `HIGHLIGHTS.md` 5.4 the Lorentz A and B line (line 356) | KEPT |

### (b.6) Chapters 6 and 7

| Paragraph | Source | Kept / only |
| --- | --- | --- |
| 6.1 the four words; the seven modes | `WHAT_IS_MISSING.md` (branch `fail-rows`) lines 38-50 (the words), section 0 lines 80-116 (the modes) | KEPT |
| 6.2 the sixteen rows, one line each | `WHAT_IS_MISSING.md` section 0's table lines 122-139; the per-row sections 1.1 to 1.13 lines 207-843 (the audit lines) | KEPT (the document's lines are the table's cells, shortened; the sections are the record) |
| 6.3 why the passed rows passed | `WHAT_IS_MISSING.md` section 0b lines 141-197 | KEPT (by reference) |
| 6.4 the order | `WHAT_IS_MISSING.md` section 2 lines 845-898; record 1128 (a) | KEPT |
| 7 (i) to (iii) the one choice and what it forces | `GROUP_STRUCTURE.md` section 3 (by reference, in full); `FULL_PICTURE.md` section 1 lines 36-110; `HISTORY.md` entry 18 lines 920-981 (line 947: "24 is the count of the rotations of the six-Port Node, the octahedral rotation group, 48 with the hand; a boost is not among them") | KEPT |
| 7 (iv) the twenty-five dated steps | `HISTORY.md` "The entries, in date order" lines 58-1515 (the entries 1 to 25 at lines 60, 103, 142, 171, 233, 265, 324, 378, 419, 481, 524, 565, 631, 689, 729, 774, 845, 920, 992, 1059, 1125, 1198, 1235, 1326, 1444); "The argument in order" lines 1550-1620 | KEPT (one line per entry in the document; the entries are the record) |
| 7 (v) the owner's sentence | record 1109 (the log) | ONLY as the chapter's closing line; the record is the record |

The count: 75 rows above; seventeen source files and the group page
under the header of section (c); the paper, Highlights, Terminology, the workflow skill and the log
referenced without a header (they are the mirror, the law, the glossary,
the skill and the record).

### (b.7) The conflicts: every place two sources state one rule differently (decided by nobody here)

Both wordings verbatim; the file and lines; what the difference is.
The Boss and the owner decide; the document's step 2 takes each
decision as one line. The sharpest is K6.

**K1. The sixth verb: "Euclidean" against "signed, truncating, not Euclidean on a negative accumulator"; and the comparison in or out of the six.**
- `HIGHLIGHTS.md` 5.4 item 3 (line 19), `TERMINOLOGY.md` lines 157-162, `HISTORY.md` line 1527, `COUPLINGS.md` line 159, `einstein_outside/DERIVATION.md` line 264: "the Euclidean division with the remainder kept".
- `DERIVATIONS_BEAM.md` lines 266-270: "is the division with the remainder kept, signed and truncating (Eq. (1): the count `sign(s) floor(abs(s) / d)`, the remainder with the accumulator's sign in `(-d, d)`, so an accumulator at -1 against the wall 2 counts 0 and keeps -1, where the Euclidean division would count -1 and keep 1"; and lines 284-287: "**(D) the signed truncating division with the remainder kept** (the same as (T)'s carry; Euclidean on a non-negative accumulator) and **the comparison** (the ladder's cell `2 T u + T <= 2 N C_k`, an age against a key, a phase against a window, a threshold), itself a division whose quotient is 0 or 1 and whose remainder is not read."
- The paper, line 66: "the division with the remainder kept, together with the comparison that is the event".
- The difference: the law's word (record 202) says Euclidean; the derivation says the engine's division is truncating and Euclidean only on a non-negative accumulator; and the comparison is part of the sixth verb in the derivation and the paper, and absent from the Highlights' list. The document must state the sixth verb once.

**K2. Newton's form: "in a limit" against "no low-velocity limit is taken".**
- `einstein_outside/DERIVATION.md` lines 568-572: "**(c) Theorem 4 (Newton's step as the limit of the small step).** In the continuum limit of the image (a) (many self-creations, `v << c`, the shell mean of (M)) the small step of (b) becomes Newton's step". The paper's opening, line 51: "under (A1) and five assumptions of the law as built, with no (A2), the equivalence principle and, in a limit under a shell average, Newton's inverse square".
- `NEWTON_FROM_CLICKS.md` title (line 1): "nothing taken as a low-velocity limit"; lines 298-303: "Einstein is the step in between because Einstein's step is the conversion between the mover's count and the rest detector's, the rate r; no low-velocity limit is taken, Newton's classical form being the value r = 1 of the same identity, the value the law's CLOCK has in no crowd (4.3) while its DRIVE has 1 - v". `NEWTON_ON_THE_SIDE.md` lines 185-187: "neither is a low-velocity limit taken in the algebra, both are values the side must arrange."
- The difference: two limits are in play, the shell mean (rung 2, both files take it for the 1 / r^2) and v << c (taken by Einstein Outside and the paper, refused by the Newton files on the owner's word of record 1044). The document must say which limit Newton's form needs and which it does not.

**K3. "Einstein's step", three definitions.**
- `einstein_outside/DERIVATION.md` line 511: "Einstein's step: dp / dt = F with p = gamma m v, E^2 = E_0^2 + c^2 p^2, d tau / dt = sqrt(1 - v^2), and the geodesic's first terms".
- `NEWTON_FROM_CLICKS.md` lines 204-205: "Einstein's step is the IMAGE of the Inside step under this map (section 3 (a))."
- `NEWTON_FROM_CLICKS.md` lines 299-300 and `NEWTON_ON_THE_SIDE.md` lines 162-164: "Einstein's step is the conversion between the mover's count and the rest detector's, the rate r".
- The difference: a form, a map's image, and one factor of that image. The document uses the phrase once with one meaning.

**K4. The law's own rate r of a mover's count: four values.**
- `einstein_outside/DERIVATION.md` lines 405-406: "The law fixes `r = 1 / (1 + k)` at every speed"; lines 518-519: "the law as built does not give (r = 1)"; lines 666-667: "under the loop's resident count `r = 1 - v`".
- `NEWTON_FROM_CLICKS.md` lines 301-303: "the value the law's CLOCK has in no crowd (4.3) while its DRIVE has 1 - v ... That the law carries two rates for one record is the click frame's ... it is NOT SHOWN that they are one." `NEWTON_ON_THE_SIDE.md` line 135: "the law as built has r = 1 [D, the whole-record hop]".
- The difference: r = 1 (the clock in no crowd), 1 / (1 + k) (the clock in a crowd), 1 - v (the drive's resident count): three quantities under one letter; mode C of the FAIL rows. The document names them apart.

**K5. The reading rule, five wordings.**
- `HIGHLIGHTS.md` 5.4 (records 1104, 1115) and the paper's abstract, line 46: "Everything the paper compares with nature is a count between clicks at a detector, or a ratio of such counts; nothing measured inside the board is compared".
- The paper, line 80 (P11): "Only a detector's reading is a measurement (the frame's assumption, P11): a click, a record's moments or an external thing's reading, as the world file declares."
- `click_frame/DERIVATION.md` lines 967-968: "every Outside formula is a ratio or a difference of counts at a click, never the tick".
- `light_outside/DERIVATION.md` lines 55-58: "Every Outside formula carries its own transformation: it is written as the map from the emitter's clicks at its place to the detector's clicks at its place, and nothing else. A reading at another place is a detector at that place".
- `GROUP_STRUCTURE.md` section 8 (at `e99a1afa`): "a click at a detector, a count between clicks on the detector's own record, and a ratio of such counts are what is compared with nature; nothing measured inside the board is compared (a GameBoard reading is a diagnostic)".
- The difference: "a ratio" (the abstract) against "a ratio or a difference" (the click frame); "a click" against "a click, a record's moments or an external thing's reading" (P11). The document states the rule in one sentence and lists the readings it admits.

**K6. The kind of a body's own record: DETECTOR in Highlights, GAMEBOARD in the Newton files and the FAIL rows (the sharpest).**
- `HIGHLIGHTS.md` 5.4 item 9 (line 25): "DETECTOR: a click, a record's moments, a body's own record, an external thing's reading, as declared in the world file, the only kind reality has and the only kind compared with nature or pinned".
- `NEWTON_FROM_CLICKS.md` lines 28-31: "DETECTOR, a click or a detector's own record, the only kind compared with nature or pinned; GAMEBOARD, the host's view of the board (a tick, a body's own record, a body's steps, a presence, a shell mean, ...)". `WHAT_IS_MISSING.md` lines 27-29: "GAMEBOARD, the host's view of the board (a tick, a body's own record, a presence, a shell mean, the books)"; its row 4a: "the muon's `become` at 64 at every speed (GAMEBOARD, a body's own record ...)".
- The difference: the same words, "a body's own record", on both sides of the one line that decides what is compared with nature; it decides row 4a's kind and row 14's push count, and it is the word "a read at a body is a click" (records 1044, 1053) that record 1128 (a) puts to the owner. The document cannot state the kinds until it is decided.

**K7. The one-way factors' subscripts: two conventions.**
- `click_frame/DERIVATION.md` lines 263-266 and `NEWTON_FROM_CLICKS.md` line 176: "`k_AB`: B's own count between two arrivals of A's records, over T. `k_BA`: A's own count between two arrivals of B's records, over T"; on the law k_AB = 1 / (1 - v / c), k_BA = 1 + v / c (A at rest, B receding).
- `light_outside/DERIVATION.md` lines 222-223: "k_AB = (r_B / r_A) x (1 + v)      (A moving away, B at rest ...), k_AB = (r_B / r_A) / (1 - v)      (B moving away, A at rest ...)".
- The difference: the same symbol k_AB names the reverse ratio in the light file (emitter to detector) and in the click frame (the counter's own count of the other's records). One convention in the document, the other named once as the record's.

**K8. The law's momentum p = m_i v / (1 - v): "exact, rung 1" against "FAIL at second order".**
- `NEWTON_FROM_CLICKS.md` line 294: "| the drive as built | 1 - v ... | m_i v / (1 - v) | the law, rung 1, exact by the wall m_i + abs(p_a) |".
- `einstein_outside/DERIVATION.md` line 980: "p_law / p_nat = sqrt(1 - v^2) / (1 - v) = sqrt((1 + v) / (1 - v)) = k," with the verdict "FAIL at second order".
- The difference: not a contradiction (exact on the law, failing against nature) but two verdict words on one formula; the document gives it one status line with both.

**K9. The bending's coefficient: two mechanisms, one value; and a third form under `meeting-v1`.**
- `einstein_outside/DERIVATION.md` line 1328 (Fermat on the delay field): "alpha = c_f (n / d) (c tau_L) x integral of (dA / db) ds = 2 c_f (n S / d) G M_B / (c^2 b)".
- `NEWTON_FROM_CLICKS.md` lines 643-647 (the push on the row): "alpha = 2 k_a(b) x (c^2 / v^2) x (1 + gamma_PPN v^2 / c^2) ... = 2 (n S / d) (G M_B / (b v^2)) (1 + gamma_PPN v^2 / c^2)".
- `DERIVATIONS_BEAM.md` 5.4 line 1270 (under the key `meeting-v1`): "theta = ... = q delta_theta / (4 N b c)", "reached in form for the bending with a grain constant".
- `STEP_ALGEBRA.md` line 305: "the bending is the push's alone, the delay the wall's alone; the wall bends nothing by itself".
- The difference: Einstein Outside bends by the delay field, the Newton file and the step algebra by the push; the values agree at v = c and c_f = 1 + gamma_PPN; the meeting-v1 form is an older key's. The document states the walk once (the push bends, the wall delays) and the delay-field form as the continuum's check.

**K10. (A3): a theorem of (A1) or the owner's assumption.**
- `click_frame/DERIVATION.md` lines 55-73: "LOCALITY OUTSIDE ... FOLLOWS FROM A1 ALONE".
- `einstein_outside/DERIVATION.md` lines 192-195: "The click frame at 1dd81fe (:52-68) states the same as a theorem of (A1) with P6, the pair's click the one exception; this file keeps it as the owner's named assumption and uses nothing beyond that theorem." The paper, line 51: "under (A1) with (A3)".
- The difference: whether the document lists two hypotheses or three. It lists (A3) as the paper does and says in one line that the click frame derives it from (A1) with P6.

**K11. Newton's constant G: two letters for the suspension.**
- `DERIVATIONS_BEAM.md` line 945: "a = - G M_B / r^2,     G = K (n / d) / (4 pi S)".
- `NEWTON_FROM_CLICKS.md` lines 335-336, `NEWTON_ON_THE_SIDE.md` line 54, `einstein_outside/DERIVATION.md` line 1318: "G = K eta / (4 pi S)".
- The difference: eta against n / d for the same declared ratio; the document uses one and names the other once.

**K12. The equivalence constant: the height's letter, and "at rest only".**
- `NEWTON_FROM_CLICKS.md` line 217 and `NEWTON_ON_THE_SIDE.md` line 160: "delta k = (n S / d) (g h / c^2)" with h the height; lines 227-232 add "it holds for a reader AT REST ... For a moving reader the law's "one field" is two."
- `einstein_outside/DERIVATION.md` line 1122: "delta k = (n S tau_L / (d c)) g Y = (n S / d) (g Y / c^2)   in the limit of every direction (tau_L c = 1)", with Y the height and h kept for Planck's constant; no rest-only qualifier.
- The difference: h is Planck's constant everywhere else in the tree (the notation rule: one symbol, one quantity); and the qualifier is in one file only. The document uses Y and carries the qualifier.

**K13. The atom's ladder: "reached in form" against "FAIL IN FORM on the lattice as declared", and the paper's "conjecture".**
- `DERIVATIONS_BEAM.md` 7.2 line 2035: "r_j = j^2 h^2 / (4 pi^2 Q S M x (M k)),   r_j ~ j^2" (reached in form under the inverse square with a circular orbit); lines 2061-2072: the energies and the lines "**Not reached**".
- `atom_algebra/ALGEBRA.md` lines 281-294: the lattice's exponent "2 / (3 - k) = 1.709 at k = 1.83"; section 4: Bohr's radii "MET IN FORM in the shell mean; ... FAIL IN FORM on the lattice as declared"; the verdict line 26 "NEEDS A NEW RULE".
- The paper's abstract, line 46: "Two relations, the bending's coefficient 2(1 + gamma) and the atom's 1/j^2 ladder, are conjectures, not established."
- The difference: three status words for one ladder (in form in the shell mean; FAIL on the lattice; a conjecture). The document gives the ladder one status line naming the mean it holds in and the lattice it fails on.

**K14. The letters G, P, E: verbs in one place, matrices in another.**
- `DERIVATIONS_BEAM.md` section 1 lines 278-283: "(G) the group-ring addition", "(P) a permutation of the joint state", "(E) the evaluation".
- `DERIVATIONS_BEAM.md` symbol table line 49: "| **G**, **P**, **E** | matrix, matrix, matrix | the click's Gram matrix (`G = E^T E` in 6.7), the rotation of the phase as a signed permutation (section 6.5), the `2 x N` matrix of the tables C and S |". `COUPLINGS.md` line 158 writes the group-ring addition as "A", `FULL_PICTURE.md` line 168 as "(G)".
- The difference: one letter, two objects, in one file; and two letters for one verb across files. The notation rule (a matrix bold uppercase, a verb's tag plain in parentheses) separates them typographically; the document must still fix the verb letters once: (T) (B) (G) (P) (E) (D) as DERIVATIONS_BEAM, GROUP_STRUCTURE and FULL_PICTURE have them, or T B A P E D as COUPLINGS has them.

**Agreements worth one line each (no conflict, listed so that the reader does not look for one):** the group's objects agree in every file (GROUP_STRUCTURE section 8); the cancel as the quotient by x^(N/2) + 1 and Z[zeta_N] for N a power of two agree (DERIVATIONS_BEAM 6.5, the click frame section 9, HISTORY entry 17); the built tables' rounding as "not a ring homomorphism" agrees (DERIVATIONS_BEAM 6.7, the click frame lines 1471-1481); the (A2) correction's three forms (m^2 v^2 / 6; kappa^2 / 6 with kappa^2 = m^2 v^2 / (1 - v^2); "up to m^2 v^2") agree to the order stated; the FAIL count (twelve in the table and four by a pin, sixteen) agrees between the paper's opening and WHAT_IS_MISSING; the redshift's second order 1 - k + k^2 agrees (Einstein Outside II.10, Light Outside II.8); Newton's G = K eta / (4 pi S_w) agrees in value across the three Outside files (K11 is the letter only).

### (b.8) Decisions the plan needs before step 2 (the Boss and the owner)

- D1. Chapter 1: decided by the Boss's addition of 2026-09-23 (by
  reference, sections 1 to 3 in full, the page kept as the record); what
  remains is the merge SHA of `group-structure` (PR open at `e99a1afa`),
  so that the header of section (c) lands on the merged file.
- D2. The merge SHA of `fail-rows` (PR #964's fold of read AE), so that
  chapter 6's sixteen lines are taken from the merged file.
- D3. K6 (the kind of a body's own record; "a read at a body is a
  click"): the owner's word, already put to him by record 1128 (a).
- D4. K1 (the sixth verb's one wording) and K14 (the verb letters):
  the Boss's word; the derivation mathematician owns DERIVATIONS_BEAM
  and the architect BEAM_LAW, so the wording chosen is theirs to keep.
- D5. K2 and K3 (Newton's limit; Einstein's step): the owner's word
  of record 1044 read against Einstein Outside's Theorem 4; the Boss
  decides which file's sentence the document carries.
- D6. K7, K11, K12 (notation): the Boss's word; the document proposes
  the click frame's subscripts, n / d, and Y.

---

## (c) The header text for each source file

One sentence at the top of each source, under its title, nothing else
changed in the file; N the chapter of `docs/ALGEBRA.md` the file's
algebra is stated in; the date the file's own (its title's, or its
first commit's where the title has none):

> The canonical statement of this algebra is `docs/ALGEBRA.md` (a relative link to it), section N; this file is kept as the record of <date>.

| File | Section N | The date |
| --- | --- | --- |
| `docs/DERIVATIONS_BEAM.md` | 2 (the operations), 4 (the identities), 5 (the map's rows) | 2026-09-22 |
| `docs/designs/click_frame/DERIVATION.md` | 3 (the click algebra), 5.1 (the click theorem) | 2026-09-22 |
| `docs/designs/click_frame/ENTANGLEMENT_PAGE.md` | 3.6 | 2026-09-22 |
| `docs/designs/newton_clicks/NEWTON_FROM_CLICKS.md` | 5.6 | 2026-09-22 |
| `docs/designs/newton_clicks/NEWTON_ON_THE_SIDE.md` | 5.6 | 2026-09-22 |
| `docs/designs/newton_clicks/MASSIVE_RELEASE_INVENTORY.md` | 5.6 (an inventory beside the chain; the header names it as such) | 2026-09-22 |
| `docs/designs/einstein_outside/DERIVATION.md` | 5.1 to 5.5 | 2026-09-22 |
| `docs/designs/light_outside/DERIVATION.md` | 5.7 | 2026-09-22 |
| `docs/designs/light_outside/DARK_ENERGY.md` | 5.7 | 2026-09-22 |
| `docs/designs/atom_algebra/ALGEBRA.md` | 5.8 | 2026-09-22 |
| `docs/designs/light_bending/STEP_ALGEBRA.md` | 5.9 | 2026-09-22 |
| `docs/designs/flow_weight/ALGEBRA.md` | 5.9 | 2026-09-22 |
| `docs/designs/algebra_transition/HISTORY.md` | 7 (the steps), 2.10 (the quantities) | 2026-09-22 |
| `docs/designs/couplings_algebra/COUPLINGS.md` | 2.9 | 2026-09-22 |
| `docs/designs/hand/FORM.md` | 1.1 (the hand as the pseudoscalar) | 2026-09-20 |
| `docs/FULL_PICTURE.md` | 1 and 7 (section 1 of the file only; the rest of the file is the physicist's picture and is not the algebra) | 2026-09-22 |
| `docs/designs/fail_rows/WHAT_IS_MISSING.md` | 6 | 2026-09-22 |
| `docs/GROUP_STRUCTURE.md` | 1 (and 7 through its section 3) | 2026-09-23 (after its merge) |

Not given a header: the paper (its Part 1 is the document's mirror,
and the paper never changes the tree), `docs/HIGHLIGHTS.md` (the law's
decisions; its "The six operations" paragraph gets a link to the
document's chapter 2, not a header), `docs/TERMINOLOGY.md` (the
glossary; its "The six verbs" entry gets the same link),
`skills/workflow.md` (a skill), the log (the record). The
README's rows of the seventeen files are not changed; the document's
own row is added.

---

## (d) The estimate

**The document's length.** By chapter, from the sources' rows above
(HOST estimates; a page is about 3 KB of this prose): chapter 1 one
page plus the group page's six sections carried over (about 12 KB);
chapter 2 five pages (the boxed formula, six paragraphs, the two tables
by reference); chapter 3 four pages; chapter 4 three pages (fourteen
one-line identities with links); chapter 5 eight pages (ten items,
each with its hypotheses, order, error term, status and kind); chapter
6 three pages (the words, the modes, sixteen lines, two references);
chapter 7 one page; the symbols named once and the links one page. In
sum about 26 to 30 pages, 75 to 90 KB of markdown; every sentence
traceable to a row of section (b); no formula stated that a source
does not state.

**Step 2's time (HOST).** The document: five to seven hours of writing
in the paper's order, chapters 2 to 5 the bulk, chapter 1 the carry
over, chapters 6 and 7 the shortest; the seventeen headers and the two
links (Highlights, Terminology): one hour; the README row and the
check (`tools/check.py --base origin/main`: the language, the hygiene
and the links): half an hour; in two to four commits on the branch
`algebra-one` (chapter 1 with the headers first, so that the pointers
land with the page they point to; chapters 2 to 4; chapters 5 to 7).
Then the physics-rule reviewer's read of the whole (the three tests,
the reading rule, the kinds, the group's name in every line) and the
derivation mathematician's check (every formula against its source
line): two to three hours each, in parallel; their must-fixes one more
bounded commit. End to end about two days of the tree's clock, one
working day of the unifier's.

**What step 2 waits on.** D1 (the group page's merge SHA; its content
is read at `e99a1afa` already), D2 (the fail-rows merge SHA), D3 (K6,
the owner's word); D4 to D6 can be taken as the plan proposes and
corrected by one line if the word differs.

## Links

- The order: [record 1128](../../LOG_2026-09-20.md) (on
  `claude/universe24-new-3ytqde`), [record 1099](../../LOG_2026-09-20.md),
  [record 1104](../../LOG_2026-09-20.md), [record 1109](../../LOG_2026-09-20.md),
  [record 1114](../../LOG_2026-09-20.md); [Highlights 5.4](../../HIGHLIGHTS.md).
- The sources: [DERIVATIONS_BEAM](../../DERIVATIONS_BEAM.md); the click
  frame [DERIVATION](../click_frame/DERIVATION.md) and the
  [entanglement page](../click_frame/ENTANGLEMENT_PAGE.md); [Newton from
  the clicks](../newton_clicks/NEWTON_FROM_CLICKS.md), [Newton on the
  side](../newton_clicks/NEWTON_ON_THE_SIDE.md), [the massive release
  inventory](../newton_clicks/MASSIVE_RELEASE_INVENTORY.md); [Einstein
  Outside](../einstein_outside/DERIVATION.md); [Light
  Outside](../light_outside/DERIVATION.md) and [dark
  energy](../light_outside/DARK_ENERGY.md); [the atom's
  algebra](../atom_algebra/ALGEBRA.md); [the step
  algebra](../light_bending/STEP_ALGEBRA.md) and [the flow
  weight](../flow_weight/ALGEBRA.md); [the transition's
  history](../algebra_transition/HISTORY.md); [the
  couplings](../couplings_algebra/COUPLINGS.md); [the hand](../hand/FORM.md);
  [the full picture](../../FULL_PICTURE.md); the FAIL rows
  (`docs/designs/fail_rows/WHAT_IS_MISSING.md` on `fail-rows`); the group
  page (`docs/GROUP_STRUCTURE.md` on `group-structure` at `e99a1afa`).
- The mirror: [the paper](../../../paper/general_formula/main.tex)
  (the abstract, Theorems 1 to 5 and the finite-N Bell value).
- The rules: [AGENTS.md](../../../AGENTS.md) (the one-source rule);
  [skills/workflow.md](../../../skills/workflow.md) (the notation, the
  three tests, the six lines); [TERMINOLOGY](../../TERMINOLOGY.md).
