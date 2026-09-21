# Canonical simulation terminology

The paper's glossary and its symbols table are taken from this file at one
named commit: the paper cites the commit it copied, and a later edit here is
a later commit the paper takes or not (the model owner, 2026-09-21: "make
sure we have a glossary and definitions, everything ordered, exactly what we
defined, no old words there; and that the paper has it too").

This file is the one glossary of the Beam Law (`beam-v1`, [BEAM_LAW.md](BEAM_LAW.md)):
every canonical term defined once, in one or two sentences in the law's own
words, with the note, section or record that owns it. The rules themselves
live in the owning documents (the table in [AGENTS.md](../AGENTS.md)); this
file names, it does not legislate. It is ordered by kind, not alphabetically,
so that it reads as the law's vocabulary: the location, the state, the rule,
the readings, the widths, the identities, the symbols, the retired words.
Every symbol follows the notation rule ([skills/workflow.md, "Notation"](../skills/workflow.md#notation-every-symbol-named-its-kind-shown-the-model-owner-2026-09-21-record-184)):
named in English at its first use, a scalar plain, a vector in bold
lowercase (**p**), a tensor, a matrix or an operator in bold uppercase (**C**).
The engine's data and the human names of the same things, one row each, are
in [THREE_WORLDS.md](THREE_WORLDS.md); the records' fields by type in
[ENGINE.md, "The detector's readings by type"](ENGINE.md#the-detectors-readings-by-type).

## The location

- **Node**: one local location of the GameBoard. Between intervals it holds
  nothing but the rows present at it and the body there; nothing else is
  kept at a Node (BEAM_LAW section 3; the third test of every rule, local).
- **NodeState**: all local information one Node owns at an interval, the
  records of its rows and of its body; not a second physical object
  (AGENTS.md, the canonical terminology).
- **Scalar**, **Vector**: a one-component and a three-component local value;
  input and output are roles of them, not further kinds (AGENTS.md).
- **Port**: one of the six directional connection endpoints of a Node, in
  Port order +x, -x, +y, -y, +z, -z (`PORT_HEADINGS`, `core/game_board.py`).
- **Link**: the causal connection between two neighbouring Nodes, one unit
  step on one axis. A row crosses at most one Link per interval, the causal
  bound (LOCALITY-1 in [SIMULATOR_DEFINITIONS.md](../SIMULATOR_DEFINITIONS.md#locality-1-end-to-end-local-physics)).
- **GameBoard**: the cubic lattice of Nodes with six Ports each and the faces
  per axis, open or periodic (the world keys `shape` and `boundary`);
  `GameBoard` in code, `game_board` in module and function names; the only
  noun for it (the model owner, 2026-09-20, [Highlights 5.4](HIGHLIGHTS.md#54-the-detector),
  "DECIDED: the name of the board is GameBoard"). In the vector form, the
  translation group Z_X x Z_Y x Z_Z acting by shift operators (record 191).
- **Face, face detector**: an open face of the GameBoard is a detector,
  named `face:+x` .. `face:-z`, with the threshold 1: every row or body that
  leaves through it clicks on it, the escape a measurement at the border and
  not a loss; a periodic axis has no faces (the model owner, 2026-09-19;
  [ENGINE.md, GameBoard topology](ENGINE.md#per-axis-gameboard-topology-2026-09-19-implementation-amendment)).
- **Event**: a local state transition at a Node or a completed transfer on a
  Link. On the GameBoard there are only events: a row is an event in
  transit, a body an event created here without end (the model owner,
  2026-09-20, "there is no ray, there is only an event").
- **LocalRule**: configured local logic that reads only the NodeState and the
  values that arrived through Links, then proposes the next local state and
  the outgoing transfers (AGENTS.md).
- **Interval (tick)**: the step t -> t + 1 of the whole GameBoard, one
  application of the interval's map **F**; `tick` in every record key and
  identifier, "interval" the prose noun (Highlights 5.6, item 9).
- **The cube group**: the 48 signed axis permutations about a Node, 24
  rotations and 24 reflections, under which every rule is covariant up to
  the two declared ties, the digital line's axis order (x before y before z,
  which moves the Nodes crossed and the exit face of a tied direction under
  the 40 axis permutations; the label, the momentum and the hand covariant)
  and the collision's Port order (`core.game_board.cube_symmetries`; records
  191 and 349 of [the log](LOG_2026-09-20.md)); its hand is its pseudoscalar,
  +1 on a rotation and -1 on a reflection.
- **The phase circle**: the world's one circle of N steps, the cyclic group
  Z_N of the phase, with its unit vectors at the scale 256 (`core.phase.PhaseCircle`,
  the tables C and S).

## The state

- **Row**: the record of an event in transit, `NatureBeam` in the code: a
  Node, a direction, an age, a phase, a number, an amount and a content per
  unit, moving along the digital line of its direction at one pace for every
  direction; identical rows at one Node are one row with the amounts added
  ([BEAM_LAW section 2](BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file)).
  The system has rows and bodies (the model owner, record 183, 2026-09-21);
  a row is a body of no content (the first test of every rule, generic).
- **Body (a measured event)**: an event created here without end, at one
  Node or on a set of Nodes (`span`), with one record: its held content per
  family, its momentum vector **p**, its phase, its clock and its counts
  table; it meets what arrives by its table and releases off its clock
  ([BEAM_LAW section 5](BEAM_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors)).
- **Record (of a quantum)**: in a recorded world (one with a lamp,
  `amplitude-v1`), the identity a lamp's self-creation gives every row it
  births, the lamp's number x 2^32 + the birth's ordinal, carried through
  every split, re-emission, rotation and gate; one record is one quantum of
  the world's list of clicks, its rows are its paths, its click is one
  (BEAM_LAW note 37). In the vector form the record is the phase-count
  vector **f** of Z^N, an element of the group ring Z[Z_N] (record 188).
- **Family**: one row of the family table, the world's `families`: its
  quantum h (0 a free family, 1 or more a paid one), its charge per unit of
  content rho, its columns, its lifetime L, its phase (a circle or none),
  its phase per Link and its hand; its kind is derived from its quantum and
  never declared (the model owner, 2026-09-19, the table from the keys).
- **Content**: the integer M a body holds, or a paid row carries per unit,
  in the family's units: the mass; `content` on a body or a row
  (BEAM_LAW section 2). A free row carries no content.
- **Amount**: the whole units in a row or a record, the intensity;
  `amount`. **Carried** is amount x content, the content a row carries, the
  content line of the books (Highlights 5.6, item 13).
- **The momentum label**: the momentum of a row is not stored, it is its
  label, content x **u**_d per unit for a paid family and amount x **u**_d
  for a free one, **u**_d the unit vector of its direction at the scale
  Q = 64; every momentum the law reads or moves (the push, the click, the
  recoil, the books' lines) is this label, in label units, Q per unit of
  amount along a heading (BEAM_LAW section 2, notes 18 and 23).
- **Phase**: a step of the circle of N: on a row, stamped by the emitter's
  clock at birth and turned by the family's `phase_per_link` at every Link
  crossed; on a body, the turns of its clock (BEAM_LAW section 2). A record
  row's rules read its path phase, the phase less its birth phase u
  (note 37); at its end the row is read at the exact phase (below).
- **Age**: on a row, the count of intervals since the event that created it,
  a birth or a re-emission, kept whole on the record; the flight reads it
  modulo the direction's period, a body reads it whole as the age moment
  (note 25). On a body, its clock.
- **Number**: the last emitter's number on a row, a body's number; a reader
  reads everything at its Node but its own number (the one reading set).
- **Direction**: an index into the world's direction table: 0 and 1 the two
  rest directions, 2 .. 7 the six headings in Port order, 8 .. the declared
  primitive vectors **D** with components in -P .. P (BEAM_LAW section 2).
  The **unit vector of a direction** **u**_d is the integer vector nearest
  Q **D** / |**D**|, one constant per direction computed once at load,
  of length Q within 1.35 percent (note 23).
- **Hand**: the row's column `hand` in {-1, 0, +1}, the sense in which the
  event in transit turns about its own direction, a pseudoscalar under the
  48 symmetries, carried unchanged through every re-creation and an
  identity field of the merge (`hand-v1`, note 39). The **axis** of a body
  is its declared axial heading, read by the right-hand rule at the birth of
  a transformation's products (the same note).
- **Held content**: what a body holds of every family (`held`), its own
  amount under its own family; its content is the sum, its charge in every
  column the rational sum over what it holds (note 31 (viii)).
- **Charge**: of a family, rho, the charge per unit of content, an integer
  or a pair [n, d]; of a body, rho times its content, and per column the
  rational sum of the column's value times the content held; of a paid
  family, a whole charge per unit of amount read on the charge line of the
  books alone (the model owner, 2026-09-20; note 36 (ii)).
- **Column**: a value per unit of content a family declares under a name
  with a sign, +1 like values push apart, -1 like values pull together;
  every family carries `gravity` first and `charge` second. A force of nature
  is a column with a sign and a lifetime on its family, never a code path
  (the model owner, 2026-09-20, note 31; `columns-v1`).
- **Clock**: the count of a body's self-creations, its age; every rate of the
  body, the turn, the release, the owed count, is read off it.
- **The counts table**: the rows of a body's record that own its counts,
  one accumulator each: the owed count, the release per family, the lamp,
  the turn, the push per column and axis, the drive, the action and the
  place rows (`Measured.counts`, note 41).
- **The store**: the host's arrays, one row per record per family, sorted by
  Node at every interval; a report of the host, not a thing of the law
  (BEAM_LAW section 3).

## The rule

- **The six verbs**: the only operations of the law on the state vector
  (the model owner, records 181 and 202): the translation of an accumulator
  by its rate; the bilinear form with a declared matrix; the group-ring
  addition; the permutation; the evaluation; the Euclidean division with the
  remainder kept. A rule that needs a seventh verb (a root) is stated under
  its own identity outside the law.
- **The three tests**: generic, vector, local; a rule enters the law only if
  it passes all three ([skills/workflow.md](../skills/workflow.md#the-three-tests-of-every-rule-generic-vector-local-the-model-owner-2026-09-21-record-202), record 202).
- **Accumulator**: the one bounded integer on a body's record that owns a
  count: it gains the count's rate at each self-creation, the count is the
  whole part it then holds in units of the wall, and the remainder stays in
  it (`core.integer.by_drive`; the fraction-free law, note 41).
- **Rate**: what an accumulator gains per interval, at most bilinear in the
  state (record 202): the flight's 2 S_1 Q, the drive's |p_a|, the turn's
  content x n, the owed count's k x n; the rate vector **r** of the state.
- **Wall**: the denominator of an accumulator, the value at which its count
  fires and the accumulator is reduced: the flight's 2 T_D, the drive's
  Q S M + |p_a| per axis, the turn's d; the map is linear between walls and
  jumps at a wall (DERIVATIONS_BEAM section 0).
- **Remainder**: what an accumulator keeps below its wall after a count,
  never discarded at run time; the phase of the count within its cycle
  (the model owner, records 150 and 155 (3)).
- **Count**: the whole part an accumulator yields at a self-creation, the
  sixth verb; a clock's count of self-creations; the owed count.
- **Drive**: the body's accumulator of its step, per axis the rate p_a
  against the wall Q S M + |p_a|, at most one Link per self-creation, the
  remainder on the body's record (note 17 as amended; the step drive of
  2026-09-20). Under form B, decided and not built, the flight of the
  momentum's direction at the fraction the momentum earns (record 301).
- **Flight**: the row's position accumulator on the digital line of its
  direction: it starts at T_D, gains 2 S_1 Q per interval against the wall
  2 T_D, and its count picks the unit step of the line; a rest direction
  never moves (BEAM_LAW section 3, the flight rule; the flight table is
  retired, MIGRATION 2026-09-20). The step's count is `by_drive_rows`, the
  array form of `core.integer.by_drive` over the rows (2026-09-21); nothing
  written by hand, no field on the row.
- **Walk**: step 1 of the interval, departures become arrivals: every row
  whose flight counts a Link crosses it whole, its record unchanged
  ([BEAM_LAW section 3](BEAM_LAW.md#3-the-nodes-interval-nature_beam)).
- **Crossing**: the one meeting of a row and a body, where their world lines
  cross, read once: a body reads every arrival at its Nodes, and in the
  interval of a step the rows that crossed its Link the other way and the
  resident rows moving against it, never a row behind it; a moving reader's
  Doppler is the count of the rows it crosses, 1 +- v / c on an axis
  (record 158; note 48; [MIGRATION](MIGRATION.md#the-crossing-rule-on-2026-09-21-the-step-before-the-law-a-row-and-a-body-met-once-the-key-doppler-and-the-grain-deleted)).
- **Meeting**: under the world key `meeting` (`meeting-v1`), at a Node of
  free space after the collision, a paid unit's reading of the free crowd
  and its turn toward the target kappa **V** by k steps of the arc
  permutation, k read off its phase; the crowd is untouched, a report and
  not a balance (the model owner, 2026-09-20, note 35).
- **Collision**: at a Node of free space, one that holds no body, the
  permutation of the directions of the single rows of one (Node, number,
  content) group by the eight-slot table, a bijection whose class (the crowd
  mask, the number of singles, their headings' sum) is invariant
  ([BEAM_LAW section 4](BEAM_LAW.md#4-the-collision-table)).
- **Push (the coupling)**: what a body takes from the rows arriving at its
  Node, the signed inner product over the columns, per column the whole part
  off the reader's clock of **V** times the reader's charge in the column
  times the arriving family's value: gravity -M_A **V**_B, the electric part
  rho_A rho_B M_A **V**_B; for a paid family's rows the label itself; the
  bilinear form **C a** (note 31; DERIVATIONS_BEAM).
- **Table**: a body's rule per family, generated from the families' keys: a
  free family read (`read`, the push taken, the rows go on), a paid one
  measured (`measure`, the click); a world declares only what differs, a
  window, `rerelease`, `pass`, `become` or a `reads` component (the model
  owner, 2026-09-19). Not a table at a Node.
- **Click (measurement)**: a paid row's units merged into a body's record by
  the rule `measure`: the content joins, the label enters the momentum, the
  phase is read, one click per unit; the click is the only one-way border of
  the law (BEAM_LAW section 5). **Gather** is the click of a record: when
  its live units are 0 the layer reads its ladder at u and the record clicks
  at the chosen set, arm, channel and Node, with the content and the momentum
  the chosen rows carried; each Node's weight is the bilinear form
  **f**^T **G** **f** of its own phase-count vector, no pointer formed,
  coherent within one Node only (record 188; note 37 (xii); on main at
  7e523c55).
- **Exact phase at the click**: the phase a record's row is read at when it
  ends (a click, a `sum` re-emitter, an open face, the border), the phase at
  the exact time of its last Link, phi = phase - floor(terms n / d) +
  floor(n made T_D / (d S_1 Q)) mod N from the row's two counts, the phase
  per interval of age n / d and the Links made on its direction, one floor
  at the click with the remainder kept (`nature_beam.exact_phase`; the click
  line's `exact` and `remainder`); the row's `phase` column stays the
  walk's (the model owner, record 163 (2); note 45).
- **Offer, ladder**: what a record's rows put at a `sum` set's Node when the
  set ends them, the phase-count vector per label and Node (`Offer.counts`),
  the residual units, the content and the momentum they carried; a set's
  weight in the cells is the sum over its Nodes of the bilinear form of the
  sum over the labels. The ladder is the record's cells in the order of its
  offers, each cell's rung b_k = (2 W C_k + Total) // (2 Total) on the
  record's wheel W, and u falls in the cell whose rung it is below: Born's
  rule read as a count over the wheel (note 37 (iii) and (xii); note 46).
- **Release**: what a body's self-creation creates: at a turn s each unit a
  lamp releases costs it h x s content, carries that content and the
  momentum h x s **u**_d along its direction, E = h f; a free family's
  release costs nothing; a body releases every free family it holds at the
  world's `release` rate ([ENGINE.md](ENGINE.md#a-release-costs-the-emitter-by-its-phase-rate)).
- **Turn**: the phase steps s a body's clock gains at a self-creation, the
  whole part of age x content x n / d gained at the clock's pair K = [n, d],
  0 for a family without a phase circle; a release is priced by it (the
  model owner, 2026-09-19). The **turn by momentum**, under `action`
  (`bohr-v1`), adds |p_a| x N over h at every Link stepped on the axis.
- **Wheel (the birth wheel)**: a lamp's declared rate `wheel` [r, W], no
  default: one `Count` row of the lamp's counts table advanced by r over W
  at every birth, its accumulator before the advance the record's
  coordinate u = ordinal x r mod W on the ladder, written on the record and
  its rows at birth, the rows' birth phase u mod N; [1, N] the count of
  births mod N as built before, [2531, 4096] the golden rate of
  `slits_huygens` (the model owner, record 180; note 46; on main at
  7e523c55). A rebirth at a re-emitter that is no lamp keeps u = its count
  of births less one mod N.
- **Lifetime**: the family key `lifetime`, an integer L from 1: a row of the
  family whose whole age reaches L clicks on the border `lifetime`, a
  detector without Nodes booked as an open face books an escape; the range
  of a column is its family's lifetime (the model owner, 2026-09-20,
  note 31 (vii)).
- **Suspension pair**: the world key `suspension` [n, d]: a body that read
  the presence k after its self-creation owes the count k x n / d before its
  next one, the **owed count** on its accumulator, on average one
  self-creation per 1 + k n / d intervals; a row in transit never waits
  (the model owner, 2026-09-19; the fraction-free law).
- **Merge**: identical rows at one Node become one row with the amounts
  added; in a recorded world rows of one record in antiphase cancel, the
  group-ring addition (BEAM_LAW section 3 step 6).
- **Split**: a `rerelease` entry with `weights`: an arriving row leaves as the
  rows w a_i with the multiplicity m x A and the phase + t_i, the
  multiplication by the apparatus's integer matrix (note 37 (ii)).
- **Fan**: every re-emitter emits on all primitive directions within P, each
  weighted by the angle it covers, Huygens on the lattice; decided, not
  built (the model owner, record 160 and 163 (1)).
- **Re-emission**: a `rerelease` entry: the rows it takes are created again at
  the Node's next self-creation on the body's `directions`, apportioned
  whole, with the arriving phase and content, the re-emitter's number, age 0
  and the recoil taken (BEAM_LAW section 5). **Home** is a row of the body's
  own number arriving at it, created again the same way, pushing nothing.
- **Transformation (`become`, `weak-v1`)**: the fifth table rule: a body
  becomes an event of another family and releases the rest as products, born
  as a re-release with the recoil over all of them; a clock trigger (`at`,
  gated by `crowd`) and a click trigger (note 36 (iii)). The W is a paid
  family with a whole charge and the lifetime 1, no key of its own (note 36 (iv)).
- **Contact**: a body's step refused because the destination holds another
  body, read through the occupant's table entry for the body's family:
  `measure` hands the momentum component over, `rerelease` returns it,
  `read` and `pass` leave it (note 31 (ix)). **Give** (`binding-v1`): at a
  contact under `measure` a body that holds paid content of another family
  gives it to the flight as content in flight, the binding that costs
  content (note 40).
- **Window**: a table entry's or a lamp's setting `phase_window` s and width
  `phase_width` w, the w consecutive steps of the circle about s a phase
  must be in to be admitted, N / 2 by default; a window may be read from a
  reading (note 36 (i)).
- **Threshold**: a detector set's `threshold`, the amount summed over the set
  in one interval below which every row passes with a `pass` record; the
  sensitivity; at a record's click the divisor of the rungs (BEAM_LAW
  section 5).
- **Lamp**: a body's declared source: at its self-creations it births rows
  of its family with its amount, phase and wheel value, in a recorded world
  one record per birth, at its declared `rate` and `wheel` (the world's
  `lamp` key; BEAM_LAW section 5, note 46).
- **Detector**: a declared set of measured events (`detectors[].positions`)
  with one record; a click says "here, in one of these", the set's extent
  the position's uncertainty; a measured event outside every declared
  detector is a detector of one Node (the model owner, 2026-09-19).
- **Self-creation**: a body created at the next interval, at its Node or
  where it steps, one tick of its clock; a row's transfer is not one.
- **Step**: the Link a body's drive counts on an axis; refused onto a Node
  that holds a body (a contact); a body on a set moves as one; before the
  law in the interval's order (the frame, the steps, the law, the clocks'
  turn and count; MIGRATION 2026-09-21).
- **Frame**: the engine's bookkeeping of an interval, the tick, the steps,
  the books and the record; it computes no physics of the row
  ([ENGINE.md](ENGINE.md#the-beam-law-beam-v1)).
- **Bijection**: the walk, the collision, the meeting and the merge have
  inverses (`NatureBeamSimulation.inverse_step`); the click is the only
  one-way border.

## The readings

- **Detector reading**: the record of a detector's set or of a measured
  event, a click, a record's moments, a pointer, an owed count, an external
  thing's reading, as declared in the world file; the only kind reality
  has; only a detector reading is compared with nature or pinned (the model
  owner, record 281; AGENTS.md).
- **GameBoard reading**: the host's view of the deterministic GameBoard, a
  row's position, the count or flow at a Node, a body's steps, the shell
  means, the books; a diagnostic, labelled GAMEBOARD wherever it appears and
  never compared with nature (records 163 (5) and 281).
- **The crowd (the one reading set)**: everything present at the Node but
  the reader's own number, here included: the arrivals of every family and
  number and, here, the content of the body at the Node under its number;
  every coupling, the presence, the push, the threshold, the window and the
  meeting, reads it (the model owner, 2026-09-19; note 47, the crowd audit).
- **The reading (the moments)**: the amount-weighted moments of order 0, 1
  and 2 of the unit vectors of a Node's arrivals over the one reading set:
  order 0 the count, split outside and here; order 1 the net flow **f**;
  order 2 the traceless tensor **T**; and the age moment; a table entry
  selects its component by `reads` (`read_arrivals`; the model owner,
  2026-09-19). The **presence** is the order-0 reading, the count k the
  owed count reads; the **flow** **V** is the order-1 reading with the
  labels as weights, what the push reads.
- **Record (of a detector)**: per interval, per set and family, under the
  reading `wave` the pointer (X, Y) over the clicked rows' amplitudes,
  32 x amount at the row's phase over the 1/256 tables, and its square
  X^2 + Y^2; under `beam` the count clicked after the pairing by opposite
  phase; the `record` line and the run's cumulative `record`; the set's
  phase is returned to every body of the set (BEAM_LAW section 5). The
  reading `sum` accumulates one record's rows for the record's click.
- **Pointer**: (X, Y), the coherent sum over the clicked rows, the
  evaluation **E** **f** of a phase-count vector at the circle; the `wave`
  record of a detector set is its square, while the click of a record forms
  no pointer, its weight being the Gram form (`Layer.evaluate`, a report;
  record 188; note 37 (xii)).
- **Books**: the ledger per family, exact at every interval: the measured,
  transit, content and charge lines and the momentum on the bodies, in
  transit, escaped and turned; a GameBoard reading (ENGINE.md).
- **Register**: the recorded detector readings of the worlds of a series,
  `expectations.json`, `gate_set.json` and the READMEs, one source per
  number, which a test reads and never copies (TEST_EXPECTATIONS.md).
- **Pin**: a detector reading's expected value written before the run,
  derived from the law's operations where a formula exists; a formula
  gives, a run proves, and nothing is tuned backward (records 205 and 305).
- **Registered run**: a research run made once, on a stated date, at one
  runtime source fingerprint, its expectation written before it and its
  result recorded with the fingerprint in VALIDATION.md (EXPERIMENTS.md).
- **Series**: the worlds of one question (D, G2, J, R, ...) registered under
  `examples/events/<series>/` with their `expectations.json`, README,
  readings tool and comparing test (TEST_EXPECTATIONS.md).
- **Gate set**: `examples/events/gate_set.json`, the digests of the
  registered lamp-free worlds replayed for bit-identity; the replay
  mechanism, never a pin.
- **Experiment**: a world file, a detector, a derived expectation and a run
  that compares; a run without a derived expectation is a research run and
  says so (record 205).

## The widths (the grain)

The constants of the law, not of a world: resolutions whose limit reaches
the known formulas (Highlights 5.7).

- **Q = 64**: the label's scale and the flight's grain, the length of every
  unit vector **u**_d; the only knob of the pace (record 191).
- **S**: the width of the push, the world key `width`, 1 by default: a body
  of content M with the momentum component p steps one Link per
  (S M + p) / p self-creations on that axis (note 17).
- **N**: the steps of the phase circle, the world key `N`.
- **The circle's rounding, 1 / 256**: the scale of the circle's tables of
  cos and sin (`core.phase.phase_cosines`, `phase_sines`), computed once
  at load from N by integer series and read only at the click through the
  Gram matrix; a declared input of the law beside Q, S and N, kept as the
  fixed-point transforms of signal processing keep theirs (the model
  owner, record 328).
- **P**: the direction bound, the world key `direction_bound`: every
  declared direction has its components in -P .. P.
- **K = [n, d]**: the clock's pair, the world key `K`: the turn per
  self-creation is content x n / d; an integer K is [1, K].
- **W**: the circle of a lamp's birth wheel, the lamp key `wheel` [r, W],
  the click's own grain beside N: 4096 under the golden rate, N under [1, N]
  (record 180; note 46).
- **c**: the pace of a row, Q / T_D = 32 / 55 Links per interval on an axis
  and 1 / sqrt 3 in the limit of the grain; derived from locality and
  straightness, the norm of the flight operator, never declared (record 191).

## The identities

An identity is the name a world's record carries for a law or for a
hypothesis beside it (`run.json`: `law` and `hypotheses`); a hypothesis is
stated so that it can fail and never enters the law by its list.

| Identity | What it names | Status |
| --- | --- | --- |
| `beam-v1` | the Beam Law, `"law": "beam"` | the law |
| `amplitude-v1` | the record: rows of one quantum, the split, the cancellation at the merge, the one click at the ladder (note 37) | built; under `hypotheses` when a lamp is declared |
| `meeting-v1` | the meeting, the world key `meeting` (note 35) | built; under `hypotheses` when the key is declared |
| `binding-v1` | the give at the contact, a body holding paid content of another family (note 40) | built; under `hypotheses` from the first held paid content |
| `hand-v1` | the hand of a row and the axis of a body (note 39) | built; under `hypotheses` when a hand or an axis is declared |
| `weak-v1` | the transformation `become` (note 36) | built; under `hypotheses` when a `become` is declared |
| `columns-v1` | a column beyond `charge` or a lifetime (note 31) | built; under `hypotheses` when declared |
| `bohr-v1` | the turn by momentum, the world key `action` (note 30) | built; under `hypotheses` when declared |
| `massive-rows-v1` | the free particle as a record of massive rows: the world key `massive_rows`, the family key `massive`, the lamp key `momentum_magnitude` ([the design](designs/massive_rows/DESIGN.md)) | built (2026-09-21); under `hypotheses` when the key is declared |
| form B | one motion primitive: a body's drive as the flight of its momentum's direction at a fraction | decided (records 183, 191, 301), not built |
| `covariant-readings-v1` | the four covariant readings of DERIVATIONS_BEAM section 17, in place of `lorentz-v1` | decided (record 270), not built |
| `optical-v1` | the rows' rule at a Node for the bending, the Shapiro delay, the second-order redshift and Snell ([the design](designs/gr_rows/DESIGN.md)) | decided as a hypothesis, not built |
| `colour-v1` | a Z_3 label on the quarks ([the design](designs/quarks/QUARKS.md)) | decided (record 270), not built |
| `expansion-v1` | the growing wall of the flight with the rate H declared, absent by default | a declared assumption (record 279), not built |
| the click without amplitudes; the birth wheel at a declared rate; the exact phase at the click | the Gram form on the phase-count vector (record 188, note 37 (xii)); the lamp key `wheel` (record 180, note 46); phi at the row's end (record 163 (2), note 45) | built, on main at 7e523c55 (PR #457); rules of `beam-v1`, no identity of their own |
| the scheduler | the GameBoard as one vector map between events, the jump to the next carry (record 191 (3)) | decided, in build |

## The symbols

Every symbol the documents use, its English name, its kind, its unit in the
law and where it is defined. In a code span every letter is plain; its kind
is the one stated here. Under record 369 (the notation decision of
2026-09-21) the table carries the letters the paper, HIGHLIGHTS 5.7 and the
page use, with the spelling the law's documents still use in parentheses
until their writers' next pass; code identifiers and world keys keep their
names everywhere.

| Symbol | Name | Kind | Unit | Defined in |
| --- | --- | --- | --- | --- |
| N_l (Q in the law's documents until their next pass) | the label's scale, the flight's grain, 64 | scalar | label units per unit of amount | BEAM_LAW section 2; record 369 |
| N_w (S in the law's documents until their next pass) | the width of the push (`width`) | scalar | dimensionless | BEAM_LAW note 17; record 369 |
| N_phi (N in the law's documents until their next pass) | the steps of the phase circle (`N`) | scalar | phase steps per turn | BEAM_LAW section 2; record 369 |
| N_D (P in the law's documents until their next pass) | the direction bound (`direction_bound`) | scalar | Links (a component) | BEAM_LAW section 2; record 369 |
| K, n / d | the clock's pair (`K`), the turn per unit of content per self-creation | scalar, a pair | phase steps per unit of content per interval | ENGINE, a release costs the emitter |
| N_u, r (W in the law's documents until their next pass) | the circle of a lamp's birth wheel and its rate, the lamp key `wheel` [r, W] | scalars | wheel steps, wheel steps per birth | BEAM_LAW note 46; record 369 |
| c, c_h | c the limit pace of the law, 1 / sqrt 3 Links per interval (c^2 = 1 / 3), the pace of a row on the diagonals; c_h = S_1 Q / T_D the Manhattan pace of a direction (64 / 110 on a heading; the paper's and DERIVATIONS_BEAM 18.6's letter; c_1 is Born's harmonic constant in the paper, so record 369's c_1 is withdrawn) | scalars | Links per interval | record 191; DERIVATIONS_BEAM 2.4; records 369 and 379 |
| T_D | the direction's period constant, isqrt(3 abs(**D**)^2 Q^2), the flight's wall over 2 | scalar | label units x Links | BEAM_LAW section 3 |
| S_1 | the Manhattan length of a direction, abs(a) + abs(b) + abs(c) | scalar | Links | BEAM_LAW section 3 |
| L_d | the period of a direction's line | scalar | intervals | BEAM_LAW section 3 |
| **D** | a direction of the world's table, a primitive integer vector | vector | Links | BEAM_LAW section 2 |
| **u**_d | the unit vector of a direction at the scale Q | vector | label units | BEAM_LAW section 2, note 23 |
| tau | the age of a row | scalar | intervals | BEAM_LAW section 2 |
| `m(tau)` (a row's field) | the flight's count at the age, the row's place on its line, in code font, never in a formula beside the mass m | scalar | unit steps of the line | BEAM_LAW section 3; record 369 |
| **p**, p_x | a body's momentum vector and its component on an axis | vector, scalar | label units | BEAM_LAW section 2 |
| abs(**p**)_1 | the Manhattan norm of the momentum | scalar | label units | designs/light_speed/FORM.md, form B |
| M | a body's content, a count of units | scalar | units of content | BEAM_LAW section 2 |
| m | the mass in label units, m = N_l N_w M (Q S M in the law's documents), the rest energy E_0 = m c^2 | scalar | label units | DERIVATIONS_BEAM 17.6; record 369 |
| h | a family's quantum (`quantum`), the content of one unit per phase step of the emitter's turn | scalar | units of content per phase step | ENGINE, a release costs the emitter |
| h (under `action`) | the quantum of action, the world key `action` | scalar | label units x Links | BEAM_LAW note 30 |
| f (in E = h f) | the frequency, the turn per self-creation | scalar | phase steps per interval | ENGINE, a release costs the emitter |
| E, E_0 | a body's energy as an accumulator of the work, its rest value E_0 = m c^2; the paper's E^2 = E_0^2 + p^2 c^2 with the exact square (E / c^2)^2 = m^2 + 3 p . p kept as an integer and never rooted (`energy_square`); no prime on E | scalar | units of content x c^2 | DERIVATIONS_BEAM section 17 (`covariant-readings-v1`); record 369 |
| s | the turn of a clock at a self-creation | scalar | phase steps | BEAM_LAW section 3 step 5 |
| a_r (k in the law's documents until their next pass) | the presence a body read, the count the owed count reads | scalar | units of amount | BEAM_LAW section 3 step 2; record 369 |
| a_tau (k_a in the law's documents until their next pass) | the age moment a body read, the sum over the rows dwelling at its Node of amount x age, the count on a table entry that reads `age` | scalar | units of amount x intervals | BEAM_LAW section 3 step 5; record 379 |
| n, d | the suspension pair (`suspension`) | scalars | dimensionless | ENGINE, the world |
| rho | the charge per unit of content of a family (`charge`) | scalar, rational | charge per unit of content | BEAM_LAW section 2 |
| L | the lifetime of a family (`lifetime`) | scalar | intervals | BEAM_LAW note 31 (vii) |
| kappa | the meeting's column sum of a family against the crowd's | scalar | dimensionless | BEAM_LAW note 35 |
| **a** (**V** in the law's documents until their next pass) | the label flow at a Node, the order-1 reading with the labels as weights | vector | label units | BEAM_LAW section 3 step 2; record 369 |
| **f** | the net flow, the order-1 reading on the unit vectors | vector | Q per unit of amount along a heading | ENGINE, the readings by type |
| **f** (of a record) | the phase-count vector of a record's rows at one end Node and label, f_p the amount at the phase p at the amplitude scale 32 (`amplitude.Counts`), the record's element of Z[Z_N] | vector | 32 per unit of amount, per phase step | record 188; BEAM_LAW note 37 (xii) |
| **T** | the traceless second moment, 3 sum amount **u**_d **u**_d^T less its trace | tensor, 3 x 3 symmetric | Q^2 per unit of amount | ENGINE, the readings by type |
| **C** | the coupling matrix, the reader's charges per column | matrix | charge per unit of content | DERIVATIONS_BEAM section 0 |
| **G** | the click's Gram matrix, **E**^T **E**, G_jk = C_j C_k + S_j S_k over the rounded tables (`core.phase.phase_gram`); the weight of a cell **f**^T **G** **f** | matrix | 256^2 | record 188; BEAM_LAW note 37 (xii) |
| **E** | the 2 x N matrix whose rows are the tables C and S; the pointer **E** **f** its evaluation at the circle (`Layer.evaluate`, a report) | matrix | 256 per unit | BEAM_LAW note 37 (xii); DERIVATIONS_BEAM section 6 |
| N_t | the cosine tables' scale, 256, the unit of the tables C and S of **E** (the paper's letter, needed for S(N, Q)) | scalar | table units per unit | BEAM_LAW note 37 (xii); record 379 |
| **Phi** (**F** in the law's documents until their next pass) | the interval's map, one piecewise-linear map of the state | operator | none | DERIVATIONS_BEAM section 0; record 369 |
| **s**, **r**, d | the state vector on the torus, its rate vector, its wall per component | vector, vector, scalar | mixed, per row of the counts table | designs/vector_form/LAW.md |
| (X, Y) | the pointer, the coherent sum of a set's clicked rows | a vector of the phase plane Z^2 | 32 x 256 per unit of amount | BEAM_LAW section 5 |
| u | the record's coordinate on the ladder, the birth wheel's value ordinal x r mod W; the rows' birth phase u mod N | scalar on Z_W | wheel steps | BEAM_LAW notes 37 (ix) and 46 |
| phi, terms, made | the exact phase at the click and the row's two counts it is read from, the intervals the phase holds and the Links made on its direction | scalars | phase steps; intervals; Links | BEAM_LAW note 45 |
| `m` (a row's field) | the multiplicity of a record's row, in code font, never in a formula beside the mass m | scalar | dimensionless | BEAM_LAW note 37 (i); record 369 |
| (the norm of a split) | the sum of the squares of a split's weights, written out; its shares' letter BEAM_LAW's writer's (A until its next pass; not a) | scalar | dimensionless | BEAM_LAW note 37 (ii); record 369 |
| **e**_A (**A** in the law's documents until their next pass) | the axis of a body (`axis`), a unit vector | vector | one heading | BEAM_LAW note 39; record 369 |
| b_k, C_k, C_K (T in the law's documents until their next pass) | a rung of the ladder on the record's wheel N_u, a cell's cumulative weight, the total (the last cumulative weight) | scalars | wheel steps; the unit 2^58 | BEAM_LAW notes 37 (iii) and 46; record 369 |
| w | the width of a window (`phase_width`) | scalar | phase steps | BEAM_LAW note 36 (i) |
| **v**, v | a body's velocity and its speed | vector, scalar | Links per interval | DERIVATIONS_BEAM |
| beta | the speed over the pace of a row, v / c | scalar | dimensionless | DERIVATIONS_BEAM section 12 |
| gamma | the Lorentz factor, 1 / sqrt(1 - beta^2) | scalar | dimensionless | DERIVATIONS_BEAM; HYPOTHESES 21 |
| z | the redshift a detector reads | scalar | dimensionless | DERIVATIONS_BEAM section 15; series G |
| H, a | the growing wall's rate per interval and growth factor (`expansion-v1`) | scalars | dimensionless | DERIVATIONS_BEAM section 15 |
| lambda, theta | the wavelength, an angle | scalars | Links, radians | DERIVATIONS_BEAM |
| zeta_N | the primitive N-th root of unity | scalar | none | DERIVATIONS_BEAM 6.5 |
| N_theta (G in the law's documents until their next pass) | the fan's angular grain, the grain of the fan's angular weights: each direction of the fan within P carries the angle it covers, half the gap to each Farey neighbour, gap(D, D') = 3 Q^2 / (T_D T_D'), as the integer a_D = floor(G x (gap(D^-, D) + gap(D, D^+)) / 2), G = 2^18 in the plane (2^24, 2^14 and 2^5 in the sphere's form); a constant of the law beside N, Q, P, W and K; a different constant from the retired grain of `doppler-v1` below, kept | scalar | dimensionless, a resolution of the angle | [TWO_SLITS.md](designs/fraction_free/TWO_SLITS.md) sections 7 and 10; [LAW.md](designs/vector_form/LAW.md); Highlights 5.7; the fan of record 160 decided and not built, so BEAM_LAW has no owning note yet |
| G (the grain of `doppler-v1`) | the deleted grain of the reading's weight at the relative speed | retired | none | MIGRATION 2026-09-21 |
| R(f) | the click's reading, the weight of a cell **f**^T **G** **f** (W in DERIVATIONS_BEAM 6.5 to 6.7 until its next pass; code `gram_form`) | scalar | the unit of **G** times the unit of **f** squared | DERIVATIONS_BEAM 6.5; record 369 |
| d_p | the drive's wall, the wall of the momentum's accumulator (W in designs/light_speed/FORM.md 3 until its next pass; code `wall`) | scalar | as FORM.md 3 states | designs/light_speed/FORM.md 3; record 369 |
| sigma_s | the strong coupling per unit of content, the strong column (G in BEAM_LAW note 40 until its next pass; the column key keeps its name) | scalar | per unit of content, as the column declares | BEAM_LAW note 40; record 369 |
| **D**_diff | the diffusion tensor of the crowd (written D_diff in prose; distinct from a direction **D**) | tensor, 3 x 3 | as DERIVATIONS_BEAM 25.6 states | DERIVATIONS_BEAM 25.6; record 369 |

## Retired words

A word below is no longer used for an active thing. It may appear in a
quoted decision, a MIGRATION entry, a LOG record or a historical section,
which say so; nowhere else.

| Retired | Named | Now | Retired by |
| --- | --- | --- | --- |
| board, the game board, lattice (as the noun), grid | the GameBoard | GameBoard | the model owner, 2026-09-20; [MIGRATION](MIGRATION.md#the-names-naturebeam-and-gameboard-and-the-glossarys-single-names-on-2026-09-20). "Lattice" stays as the mathematical term (the translation group of the lattice, a lattice gas) |
| site, Site | a Node | Node, `node`, NodeState | AGENTS.md, no second physical-location noun |
| ray, rays (the noun); "the law of the ray" | a row; the Beam Law | row, rows, `NatureBeam`; the Beam Law | rows and bodies, record 183 (2026-09-21); the name, record 37 of 2026-09-20; ray stays only in a quoted decision |
| `rays-v1` | the identity of the law | `beam-v1`, the same law | MIGRATION, the names; a historical identity name only |
| light and matter (as the two things) | rows and bodies | rows (of any family) and bodies (measured events) | record 183 |
| wave, wave function (a thing on the GameBoard) | nothing: the Node holds no wave | the reading key `wave` (the pointer's square over the crowd) is a key name; a record's vector is **f** in Z^N | record 15 of 2026-09-19; record 188 |
| the flight table, `FlightTable`, `flight_table` | the per-direction step table | the flight, the row's position accumulator (`Flight`, `direction_flight`) | [MIGRATION](MIGRATION.md#no-registers-at-nodes-no-tables-on-2026-09-20-the-last-counts-join-the-table-the-flight-as-the-positions-accumulator-no-remainder-discarded) |
| the key `doppler`, `doppler-v1`, the grain G, `quantised_speed` | the reading's weight at the relative speed | the crossing: the Doppler is the count of the rows a moving reader crosses; the fan's grain G (the angular weights of record 160, the symbols table) is a different constant, kept | [MIGRATION](MIGRATION.md#the-crossing-rule-on-2026-09-21-the-step-before-the-law-a-row-and-a-body-met-once-the-key-doppler-and-the-grain-deleted) |
| `weighted_flow`, `flux_pair`, `frame_momentum`, `acc.flow` | the weighted flow of `doppler-v1` and the frame's copy of the momentum | the label flow **V** read at the crossing; `Measured.momentum` | the same entry |
| a register or a table at a Node; a remainder discarded | counts kept at Nodes | nothing at a Node: every count an accumulator on the body's record, the remainder kept | record 155; MIGRATION, no registers at Nodes, no tables; the third test |
| `lorentz-v1` | the seventh verb, a root at a declared grain | `covariant-readings-v1`, decided and not built; a historical identity name | Highlights 5.4, "Lorentz, B replaced" (record 270) |
| the law of events, `events-v1`; the sides, the shares, the placement, the tie order, the scatter, the coherent sum at a Node, the seventh exit | the model of the evening of 2026-09-19 | the Beam Law | [MIGRATION](MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1) |
| the ray-event model, the law of the bit, the law of the shadow, `bit-law-v1`, `field-only-v1`, `ray-event-state-v1` | the engines before the Beam Law | none; in git before their deletion | [MIGRATION](MIGRATION.md#one-engine-on-2026-09-19-the-old-engine-deleted) |
| `reversible-detector-v1`, `dynamics`, `transduce`, `port_map` | the reversible detector | the detector's record and the re-emission | BEAM_LAW section 1 |
| `kind` (a family key) | the kind of a family | derived from `quantum` | [MIGRATION](MIGRATION.md#the-table-from-the-keys-and-the-moments-on-2026-09-19-the-night) |
| `phase_turn` | a row's turn in flight | `phase_per_link` | MIGRATION, the law of the ray |
| the key `amplitude`; the threshold under `wave` on the pointer's square, `pointer_units`; `RECORD_AMOUNT_BOUND`, the affordable amount | the first stages of the amplitude law | a lamp makes a recorded world; the threshold is the amount summed over the set; the record is exact, never refused | [MIGRATION](MIGRATION.md#the-amplitude-law-on-2026-09-20-vii-4-the-one-click-the-record-form-the-law); [MIGRATION](MIGRATION.md#the-push-as-one-form-the-one-label-and-the-affordable-amount-on-2026-09-19-the-night) |
| `charge` on a measured event; the row's `charge` and `mass` columns | the emitter's charge and content on the record | the family's charge per unit of content rho; nothing on the row but its number | [MIGRATION](MIGRATION.md#charge-per-unit-of-content-on-2026-09-20-the-familys-charge-a-pair-no-charge-on-a-measured-event-the-records-two-columns-gone) |
| a momentum read off a Port; the label along **D** | the momentum before the one label | the momentum label along **u**_d | [MIGRATION](MIGRATION.md#the-label-along-the-unit-vector-of-the-direction-on-2026-09-19-the-momentum-units-change-by-q--64) |
| the whole part off the clock (`by_clock`) as a count of its own | the count before the fraction-free law | the accumulator's count; `by_clock` its constant-rate identity | [MIGRATION](MIGRATION.md#the-fraction-free-law-on-2026-09-20-every-count-an-accumulator-on-the-bodys-record) |

## Naming rule

A name identifies a component's actual responsibility in simple English:
portable ASCII file names, `snake_case` modules and functions, explicit
class names; one canonical copy of each nonempty file; no historical model
called "current" (AGENTS.md). The one exception recorded: the law's record
is `NatureBeam` and its one function `nature_beam`, the model owner's own
names (BEAM_LAW, "The owner's name"). Every new symbol enters this file with
its name, kind, unit and owner before a document uses it alone.
