# The system's algebra audit: every engine component, every world, every reading tool against docs/ALGEBRA.md, and the one form for declaring an experiment from today (the System Architect, 2026-09-23, docs only)

The Boss's order of 2026-09-23 on the model owner's word of 15:33Z
(record 1435 of docs/LOG_2026-09-20.md as the Boss quoted it: "an
assessment of the whole system, of every world, that it is algebraic; the
experiments are defined algebraically and from the algebra they descend to
the board; that is the generic form we run experiments in from today").
Docs only: no engine line, no world file, no run, no pin declared or moved.
The one source is [docs/ALGEBRA.md](../../ALGEBRA.md) (the owner's word of
record 1421 as the Boss quoted it: every postulate follows it, never the
reverse); every verdict below cites a file with its lines and the ALGEBRA.md
chapter and object it is read against, and a verdict without a citation is
not written. Read at `origin/main` 05e9f10 (PR #1049); the builder's map at
`origin/detector-law-build` beb2642f
(`docs/designs/detector_law/BUILD.md` on that branch, section 0, "THE ALGEBRAIC MAP") and
the massive record at `origin/detector-law-design` b6131c64
(`docs/designs/detector_law/MASSIVE_RECORD.md` on that branch, sections 0 to 5 and
11) are read as the algebra's descent to the board before any build; the
earlier audit of the documents' LAW rows is
[ALGEBRA_AUDIT.md](../detector_law/ALGEBRA_AUDIT.md), whose method (a
quoted line, a mark, a rewrite, a status) this file follows for code and
worlds. One limit stated first: the records 1421, 1423, 1424, 1425 and
1435 the order cites are not in `docs/LOG_2026-09-20.md` on any fetched
branch (the log on `origin/main` ends at record 1395, on
`detector-law-build` at 1329, on `detector-law-design` at 1314), so their
words are taken from the Boss's order verbatim and from MASSIVE_RECORD.md
section 11 item 4, which quotes record 1421 ("PERIODIC is the algebra's
own; a wall or a sponge at a face is a declared deviation per world").

**The words of this file.** DETECTOR, GAMEBOARD, COMPUTATION, HOST and
CONVERSION are the five kinds of a number (ALGEBRA.md, the head). The six
verbs are ALGEBRA.md chapter 2: (T) the translation of an accumulator by
its rate, (B) the bilinear form with a declared matrix, (G) the group-ring
addition, (P) the permutation, (E) the evaluation, (D) the division with
the remainder kept and the comparison. The identifiers are
[TERMINOLOGY.md](../../TERMINOLOGY.md)'s: Node, NodeState, Link, Port,
Event, LocalRule, GameBoard. "Matches nature", never "is nature". A
FINDING names what a component does beyond the algebra (a branch on a
physical name, an implicit default, a float, a root, a thing kept at a Node
beyond the events there, a global reach beyond the six neighbours) and
proposes no fix.

## 1. THE ENGINE: every component of src/event_universe/ that touches physical state

The physical path is `events/nature_beam.py`, `events/meeting.py`,
`events/engine.py`, `events/world.py`, `events/measured.py`,
`events/amplitude.py` on `core/integer.py`, `core/phase.py` and
`core/game_board.py` (ENGINE.md:19-28; the algebra gate
`tests/test_integer_algebra.py:51-62` lists the same nine modules). Every
row names the component with its lines at `origin/main` 05e9f10, the
ALGEBRA.md object it implements, the declared integers it takes, and the
verdict. The declared integers are the world file's (ENGINE.md, "The
world") and the law's constants (TERMINOLOGY.md, "The widths"): Q = 64 the
label's scale, N the phase circle, S the width, K = [n, d] the clock's
pair, [n, d] the suspension pair, h the family's quantum, gamma the key
`optical`, W the wheel, P the direction bound, the tables C and S at 256.

### 1.1 core/integer.py (the bounded integer primitives)

| Component (file:lines) | The algebraic object (ALGEBRA.md) | The declared integers it takes | Verdict | The finding, or nothing |
| --- | --- | --- | --- | --- |
| `checked_work` `core/integer.py:9-16` | the working bound of the host's integer torus, a comparison (2.6); the bound is HOST, never a register (TERMINOLOGY.md, "Working bound") | 2^63 - 1 | ALGEBRAIC | nothing |
| `bounded_gcd` `core/integer.py:18-25`; `reduced`, `rational_sum` `:44-57` | (D) the Euclidean division repeated on a rational pair; the books' charge line and the columns' rational sums (4.3, GAMEBOARD) | the pairs (n, d) of the family table | ALGEBRAIC | nothing |
| `integer_root` `core/integer.py:28-41` | the root, the seventh verb (2.7): lawful as a declared rounding at load (record 155 (6)), not at run time | a square | ALGEBRAIC at load (`unit_label`, `flight_triple`, `T_HEADING`); its run-time callers are rows 1.5 (the meeting) and 1.7 (the body's weight) | the finding is at its callers, not here |
| `by_clock` `core/integer.py:60-76` | (T) then (D): the constant-rate identity of the accumulator, floor((a + 1) n / d) - floor(a n / d) (2.1; 4.1) | the age, the rate n, the wall d | ALGEBRAIC | nothing |
| `by_drive` `core/integer.py:79-128` | the one central formula (2, the boxed map): (T) s <- s + r, (D) the count with the remainder kept, the cap a comparison; `centred` the declared variant centred-step-v1 (2, "the one declared variant") | the accumulator, the rate, the wall, the cap, the key `centred_step` | ALGEBRAIC | nothing |
| `by_line` `core/integer.py:131-172` | (T) on three accumulators, (D) against one wall, the comparison choosing the axis furthest over it (drive-b-v1, 5.6 (c) form B); the tie "the lowest axis" declared in the docstring | the three drives, the rates p_a Q, the wall | ALGEBRAIC | nothing |
| `age_wall` `core/integer.py:175-209` | (B): the wall stretched by the crowd's age moment, w x (d + c a_tau n) (5.4, the clock in a crowd; TERMINOLOGY.md, "The age wall") | the rate, the wall, the member's coefficient c, the age moment, [n, d] | ALGEBRAIC | nothing |
| `signed_inner` `core/integer.py:212-252` | (B): a vector, a declared diagonal matrix of +1 and -1, a vector (2.2) | the two vectors, the signs, a bound | ALGEBRAIC | nothing |
| `apportion_whole` `core/integer.py:255-271` | (D) the floors, then (P) the units left by the largest remainders, ties by index from `first` (2.4, "the apportioning's tie ... from age mod n") | the total, the weights, the first index | ALGEBRAIC | nothing |

### 1.2 core/phase.py and core/game_board.py (the circle, the tables, the cube's group, the torus)

| Component (file:lines) | The algebraic object (ALGEBRA.md) | The declared integers it takes | Verdict | The finding, or nothing |
| --- | --- | --- | --- | --- |
| `_fixed_cosine`, `_fixed_sine`, `phase_cosines`, `phase_sines` `core/phase.py:30-116` | the tables C and S at the scale 256, the evaluation's declared rounding at load (2.5; the head's "the tables' rounding as the engine's declared constant"); fixed-point series, no float | N, the scale 256 | ALGEBRAIC | nothing |
| `phase_gram` `core/phase.py:61-79` | the Gram matrix **G** = **E**^T **E** of the click's bilinear form (2.2, 2.5, 4.8) | N (stored through 512; beyond it formed where read, `amplitude.py:779-786`) | ALGEBRAIC | nothing |
| `PhaseCircle`, `phase_circle` `core/phase.py:119-161` | the phase circle Z_N: turn, difference, opposite, the unit vectors (1.5) | N | ALGEBRAIC | nothing |
| `cube_symmetries`, `compose_symmetries`, `inverse_symmetry`, `symmetry_hand` `core/game_board.py:37-84` | the symmetry group of the cube G_48, its composition and inverse, the determinant (1.1, 1.4, 4.5) | none (a constant of the law) | ALGEBRAIC | nothing; not on the interval's path (a check the tests use) |
| `adjacent_node` `core/game_board.py:87-124` | the translation group of the torus acting on Nodes (1.6): a periodic axis wraps, an open face is None (the face a declared deviation per world, record 1421 as MASSIVE_RECORD.md section 11 item 4 quotes it) | the shape, the per-axis periodic flags | ALGEBRAIC | nothing |

### 1.3 events/nature_beam.py (the Node's interval)

| Component (file:lines) | The algebraic object (ALGEBRA.md) | The declared integers it takes | Verdict | The finding, or nothing |
| --- | --- | --- | --- | --- |
| `NatureBeam` `nature_beam.py:216-380` | the row, one entry of the state vector: a Node, a direction of the table D, an age, a phase in Z_N, a number, an amount, a content, the record's identity, branch, multiplicity and u (1.1, "The state") | the family table, N, W | ALGEBRAIC | nothing |
| `Moments`, `moment_table`, `reading_of`, `read_groups`, `read_arrivals` `nature_beam.py:381-584` | (B): the one reading, the moments of order 0, 1, 2 and the age moment over a Node's arrivals (2.2; the dictionary's "a measurement") | the direction vectors at the scale Q, the amounts, the ages | ALGEBRAIC | nothing (the sums are per Node key, `np.add.at`, `:582`) |
| `by_clock_rows`, `by_drive_rows` `nature_beam.py:587-637` | (T), (D) over rows: the array form of `by_drive` (2.1, 2.6) | the accumulators, the rates, the walls, the cap | ALGEBRAIC | nothing |
| `exact_phase` `nature_beam.py:639-714` | (D): one floor at the click with the remainder kept, phi = phase - floor(terms n / d) + floor(n made T_D / (d S_1 Q)) (2.6; TERMINOLOGY.md, "Exact phase at the click"); `math.gcd` reduces the remainder's pair (`:700`) | [n, d] the family's turn, T_D, S_1, Q, N | ALGEBRAIC | nothing |
| `birth_coordinate` `nature_beam.py:716-733` | (T), (D): the wheel's accumulator, u = ordinal x r mod W (2.1, "the lamp's wheel"; 2.10 "the wheel's coordinate u on Z_W") | [r, W] | ALGEBRAIC | nothing |
| `window_admits` `nature_beam.py:735-749` | (D) the comparison: a phase against a window, (d + w // 2) mod N < w (2.6) | s, w, N | ALGEBRAIC | nothing (the earlier audit's T12 and T13 retire the window as a gate under the design; on main it is the comparison 2.6 names) |
| `ages_at_key` `nature_beam.py:751-769` | (D) the comparison: an age against a key, age mod L = 0 (2.6; the border `lifetime`) | L, `age_bound` | ALGEBRAIC | nothing |
| `Flight` `nature_beam.py:771-853` (`accumulator`, `walk_step`) | (T), (D): the flight's accumulator, m_D(tau) = floor((2 tau S_1 Q + T_D) / (2 T_D)) (2.1; 4.1); T_D = isqrt(3 abs(D)^2 Q^2) a declared rounding at load (4.2) | D, Q, T_D | ALGEBRAIC | nothing; the digital line's axis order is one of the two declared ties (TERMINOLOGY.md, "The cube group") |
| `unit_label` `nature_beam.py:856-877`; `flow_label` `:879-909` | the label **u**_D nearest Q D / abs(D) and the flow label **f**_D nearest Q D / S_1: roundings at load, exact under the 48 (1.2 the dictionary's "momentum of a row"; 5.9 flow-link-v1) | Q, D, S_1, a massive family's magnitude | ALGEBRAIC | nothing |
| `direction_flight`, `fan_neighbours` `nature_beam.py:911-1005` | the direction table D, a finite G_48-set of primitive vectors (1.1, "The action of G_48 on the state"), with each direction's nearest neighbours by exact cosine comparisons at load (the fan a row turns on, 5.9) | the world's `directions`, P | ALGEBRAIC | nothing on main; the fan of every direction is a declaration ALGEBRA.md 6.2 row 2a counts (mode F), and the detector-law design retires it (ALGEBRA_AUDIT.md rows A5, T8) |
| `FamilyFlight`, `flight_triple`, `family_flight`, `with_weights`, `unit_energies` `nature_beam.py:1007-1247` | the family's triple (rate 2 abs(p_D)_1, wall 2 E'_D, start E'_D) with E'_D = isqrt(E'_0^2 + 3 p_D . p_D), one root per direction at load (5.3, the exact square; 5.10 massive-rows-v1); the placed pair (f_F, q_F) | h, M, p, Q, S, N, `phase_per_link` | ALGEBRAIC | nothing |
| `CollisionTable`, `class_key`, `state_code`, `collision_table` `nature_beam.py:1249-1327` | (P): the cyclic group acting on the 3^8 slot states, the classes its orbits (1.1, "The collision"; 2.4) | none (a constant of the law) | FINDING (low) | the forward map is the cyclic shift on the class's members sorted as 8-tuples (`:1310-1313`): the tie is Port order, which ALGEBRA.md 2.4 itself names "the one undeclared breaking of the 48"; no world key declares it |
| `NatureBeamTables`, `nature_beam_tables` `nature_beam.py:1330-1394` | the tables formed once at load (the circle, the flight, the collision, the arcs): the declared roundings (2.7) | the world's keys | ALGEBRAIC | nothing |
| `_merge_rows`, `NatureBeamStore.merge` `nature_beam.py:1475-1661`, `:2141-2224` | (G): identical rows added, the cancel [p + N / 2] = -[p] on a record's rows (2.3) | N | ALGEBRAIC | nothing |
| `exact_sum`, `exact_column_sums` `nature_beam.py:1663-1682` | (G): the books' exact sums (4.3, GAMEBOARD) | none | ALGEBRAIC | nothing |
| `born_recoil`, `share_of`, `place_over_nodes`, `label_weights`, `momentum_labels` `nature_beam.py:1723-1858` | (G), (D), (B): the recoil, the row's share amount x label // m with the remainder on the row, the placing over a body's Nodes, the momentum labels amount x content x **u**_D (1.2; 2.1) | Q, m the multiplicity | ALGEBRAIC | nothing |
| `circle_vectors`, `coherent_pointer` `nature_beam.py:1860-1906` | (E): the pointer (X, Y) = **E** f on the tables (2.5) | the amounts, the phases, C and S | ALGEBRAIC | nothing |
| `pointer_phases`, `setting_steps` `nature_beam.py:1908-1984` | (D) comparisons: the table step nearest a pointer by the smallest abs(X S[k] - Y C[k]) among X C[k] + Y S[k] > 0; the setting a window reads from a reading (2.6; ENGINE.md, a window read from a reading) | C, S, N | ALGEBRAIC | nothing (comparisons over the N entries, fixed work for a fixed N) |
| `NatureBeamStore` `nature_beam.py:1986-2280` | the host's arrays, one row per record per family, sorted by Node: a report of the host, not a thing of the law (TERMINOLOGY.md, "The store") | none | ALGEBRAIC | nothing kept at a Node: the rows are the events there (ENGINE.md:163-164) |
| `GameBoardDiagnostics` `nature_beam.py:2323-2418` | the per-Node counts, flow, presence and per-Port crossings of the last interval: GAMEBOARD readings, read-only | none | ALGEBRAIC | nothing (a diagnostic, compared with nothing) |
| `transform` `nature_beam.py:2420-2530` | (D) the comparison of a body's clock against the declared key `at`, and the products born as a re-release (2.9, "the transformation"; weak-v1) | `become` {at, into, products, crowd} | ALGEBRAIC | nothing on the algebra as written; ALGEBRA.md 6.1 mode E names the count trigger as the generic thing rows 8a and 7b lack, and the earlier audit's Q2 asks whether it is the one trigger |
| `FamilyPlan`, `gate_ready`, `apply_gate` `nature_beam.py:2662-2868` | (P): the CNOT gate, the joint labels permuted from the control's bit (2.4) | `gate` {kind, hold, parties, control} | ALGEBRAIC | nothing |
| `rotate_rows`, `entry_rotation` `nature_beam.py:2870-2953` | (B): the rotation **U**_s on the half-angle tables of 2N, a declared rounding at load (3.6; 4.6 Theorem 2) | s, N | ALGEBRAIC | nothing |
| `row_hand`, `read_hands`, `group_hand` `nature_beam.py:2973-3035` | the hand h in {-1, 0, +1}, a pseudoscalar under the 48 (1.2, "spin, polarisation"; hand-v1) | `hand`, `axis` | ALGEBRAIC | nothing |
| `push_form` `nature_beam.py:3037-3125` | (B) then (T), (D): the push as one signed inner product over the columns on the reader's accumulators, per column a count with the remainder kept (2.2; 5.6 (b)) | the columns' values and signs, the reader's charges, Lambda_c | ALGEBRAIC | nothing |
| `Interval`, `interval_frame`, `nature_beam` `nature_beam.py:3128-3481` | the verbs at one interval in their order: the walk, the reading, the collision, the meeting, the tables, the self-creations, the merge, the gather (2.11) | the world | ALGEBRAIC | nothing |
| `CrowdMoments` `nature_beam.py:3182-3268` | (B): the age moment and the arrival flow at a row's Node less its own number, segmented sums, nothing kept at a Node (TERMINOLOGY.md, "The crowd at a row's Node") | none | ALGEBRAIC | nothing |
| `_collide` `nature_beam.py:3483-3527` | (P): the collision at every Node of free space (2.4) | none | ALGEBRAIC | nothing |
| `reseed_flight` `nature_beam.py:3529-3552` | (T): a turned row's accumulator re-seeded from the table's count at its age on the new line | T_D, S_1, Q, d | FINDING | "the crowd's carry on the old line dropped with the old line" (the docstring, `:3532-3541`): a remainder discarded at run time, against TERMINOLOGY.md's "Remainder: never discarded at run time" (records 150 and 155 (3)) and the vector test's "no rounding at run time beyond the ones declared at load" (2.8) |
| `square_ladder`, `split_ladder` `nature_beam.py:3643-3701` | comparisons of squares that reach floor(sqrt(X Q^2)) without a root primitive | X, Q | see the next row | the value formed is the root's; whether a root by comparisons is the seventh verb is the owner's line (part 5) |
| `momentum_pair` `nature_beam.py:3716-3787` | the pushed row's pair (S_1(**P**), T(**P**)) with T = isqrt((R^2 + 3 abs(**P**)^2) Q^2), formed per pushed row when **P** changes; `math.gcd` (`:3751`) reduces **P** | Q, d, the content, E'_0 | FINDING | ALGEBRA.md 2.7 names it: "the pushed row's pair under the key `optical` (the two run-time roots COUPLINGS.md section 3 names), each declared by its design and neither a table formed at load"; a root of the state at run time is the seventh verb, not admitted (2.7; 2.8) |
| `unit_weights`, `row_pairs`, `optical_rate_and_wall` `nature_beam.py:3789-3858` | (D), (B): the weight per unit (E'_D^2 + 3 gamma p_D . p_D) // E'_D at load; the wall stretched by the crowd (5.9, the wall's delay) | gamma, [n, d] | ALGEBRAIC | nothing |
| `optical_walk_step`, `optical_last_link` `nature_beam.py:3860-3970` | (T), (D) with the cap 1: the flight under the one wall; the error accumulator **c** += **h** x **P** (B) (5.9, "the walk") | [n, d], gamma | ALGEBRAIC | nothing |
| `optical_turn` `nature_beam.py:3972-4206` | (T): **W** -= n weight **V**; (B), (D): the label by Bresenham, the Link that keeps abs(**c** + **h** x **P**)^2 smallest among **h** . **P** > 0 (5.9, "the push" and "the label"); **P** conserved across the turn | n, gamma, the fan neighbours | FINDING | at every push the residue is rescaled, s' = s S_1(**P**') // S_1(**P**), and "the sub-unit remainder ... is dropped, the one truncation of the flight's time" (the docstring, `:4022-4024`; the code, `:4090`): a remainder discarded at run time, the same rule as `reseed_flight` (2.8; TERMINOLOGY.md, "Remainder") |
| `_walk` `nature_beam.py:4208-4426` | (T): departures become arrivals; the faces' clicks: the face's pointer square (E), (B) and its lines (3.1 the click) | the faces (`boundary`) | FINDING (low) | an open face is a detector with no body and no count of its own (TERMINOLOGY.md, "A detector's clock": "the tick of its click line is the record's ordering, GAMEBOARD"), where ALGEBRA.md 3.1 gives every detector its own count n_D; the face is a declared deviation from the torus (record 1421 as quoted), and the earlier audit's Q1 is open: a face click's time is GAMEBOARD, its Node and face DETECTOR |
| `MeasuredArrays`, `_measured_arrays`, `_family_plan`, `_apply_plan`, `_apply_plans`, `_measure` `nature_beam.py:4428-5735` | the measured event's tables: the threshold and the window (D), the click (the record ended, the content into `held`, the label into **p**: 3.1), the read (B), the re-emission and the split (P, B, D, T), `become` (2.9's 31 couplings by reference) | the table per (body, family), `threshold`, s, w, `weights`, `turns`, `inputs` | ALGEBRAIC | nothing: the rule is selected by the declared entry, never by a family's name (`world.default_rule` `world.py:995-1000` derives it from the quantum); the earlier audit's T13 retires the threshold under the design |
| `covariant_release`, `_release_family`, `_release` `nature_beam.py:5737-6355` | (T), (D): the release by_clock at the turn s, E = h s (4.11); the lamp's births with the wheel; the apportioning whole (P) | K, h, [r, W], the directions | ALGEBRAIC | nothing |
| `_border` `nature_beam.py:6357-6492` | (D): the border `lifetime`, age mod L = 0, booked as a face click (2.6; the dictionary's "column ... lifetime") | L | ALGEBRAIC | nothing |
| `_merge` `nature_beam.py:6494-6561` | (G) with the cancel; the age bound a comparison (2.3) | N, `age_bound` | ALGEBRAIC | nothing |
| `gather_records`, `_place_completion` `nature_beam.py:6563-6734` with `Layer.complete` `amplitude.py:901-1003` | the click of a record: (B) f^T **G** f per set, (D) the ladder's cell 2 T u + T <= 2 W C_k, the Node by the same rungs, one click per record (2.5, 2.6, 4.12); the placement q_F | W, u | FINDING | the completion reads every detector's offer of one record across the whole board and deletes the record's rows everywhere: a global reach beyond the six neighbours, the one the algebra admits as its one non-local operation (3.1: "the one non-local step (the pair's gather, 3.6)"; ALGEBRA_AUDIT.md part 1.2 and Q5: LOCALITY-1 does not name it) |

### 1.4 events/meeting.py (the meeting under its key)

| Component (file:lines) | The algebraic object (ALGEBRA.md) | The declared integers it takes | Verdict | The finding, or nothing |
| --- | --- | --- | --- | --- |
| `frame`, `ArcTable`, `arc_table`, `sectors`, `arc_shift` `meeting.py:110-217` | (P): the arc permutation of the direction table, every sector sorted by the exact angle to the target by cross-multiplication (2.4, "the meeting's turn") | the direction table, the target | ALGEBRAIC | nothing (`integer_root` at `:196` bounds a product, it forms no state) |
| `column_sum`, `crowd_flow` `meeting.py:219-285` | (B): kappa the signed column sum of two families' values; the crowd's label flow at the row's Node less its own number | the columns, the charges | ALGEBRAIC | nothing |
| `register`, `register_inverse` `meeting.py:234-246` | the crowd met in whole units of Q, adv = (abs(**t**) + Q / 2) // Q added to the phase | Q, N | FINDING | ALGEBRA.md 2.7: "the meeting's `adv = (abs(t) + Q/2) // Q` is a rounding at run time each interval, NOT a torus operation in DERIVATIONS_BEAM's inventory (its exact form `acc += abs(t)` on Z_(N Q) stated there)" |
| `meet` `meeting.py:287-417` | the meeting: the target **t** = sum kappa **V**, its norm, the register, the arc shift by k steps | the key `meeting`, the columns | FINDING | `norm[index] = integer_root(t . t)` at `:359-361`: the meeting's norm is the first of the two run-time roots ALGEBRA.md 2.7 names (ENGINE.md:25-27, `meeting.py:359-361`); the seventh verb, not admitted |

### 1.5 events/engine.py (the frame of the interval)

| Component (file:lines) | The algebraic object (ALGEBRA.md) | The declared integers it takes | Verdict | The finding, or nothing |
| --- | --- | --- | --- | --- |
| `step_axis` `engine.py:122-154` | (T), (D) with the cap 1: the drive per axis, p_a against Q S M + abs(p_a) (2.1, "On a body the drive"; 5.6 (c)) | Q, S, M, p_a | ALGEBRAIC | nothing |
| `count_owed` `engine.py:157-182` | (B) the age wall then (T), (D): the owed count (d + a_tau n) - d over d with the remainder kept (5.4, the clock in a crowd) | [n, d], a_tau | ALGEBRAIC | nothing |
| `energy_root` `engine.py:185-215` | (D) comparisons: E' the largest integer with E'^2 <= W, kept on the record and moved by comparisons; the identity covariant-readings-v1 (5.10: "sqrt(W) is never formed, it only names the value the comparison decides") | W | ALGEBRAIC under its identity, beside the law (5.10, "none is the law") | nothing beyond the identity; the same question as `split_ladder` (part 5) |
| `covariant_frame` `engine.py:218-273` | (B): W = E'_0^2 + 3 **p** . **p**; the comparisons of the domain (5.3; 5.10) | c^2 = [1, d], the grain g | ALGEBRAIC under its identity | nothing |
| `NatureBeamSimulation.__init__`, `_measured`, `occupant`, `_place` `engine.py:279-588` | the load: the stores, the bodies' records, the detector sets, the map of Nodes to bodies (the state of 1.1) | the world | ALGEBRAIC | nothing |
| `step` `engine.py:590-647` | the interval's order: the frame, the steps, the law, the turn and the count (2.11) | none | ALGEBRAIC | nothing |
| `inverse_step` `engine.py:649-662` | the bijection of the interval without a click (4.7, Theorem 3) | none | ALGEBRAIC | nothing |
| `_frame_all` `engine.py:664-736` | (T), (D): the turn by_drive at the rate content x n over d; the content read once (2.1, "the phase's turn") | K = [n, d] | see `body_weight` (1.7) | under `drive_b` the frame calls `world.body_weight` every interval for a moving body (`:687-693`): row 1.7's root |
| `_suspend` `engine.py:738-771` | the owed count; under the identity the proper-time count by_drive(acc_tau, E' - E'_0, E'_0) (5.10) | [n, d] | ALGEBRAIC | nothing |
| `_move` `engine.py:773-1052` | (T), (D), (P): the body's step, x before y before z (a declared tie, TERMINOLOGY.md, "The cube group"); the turn by momentum, the action row abs(p_a) N over h (5.8); under `drive_b` the line by `by_line`; the escape a face click; the contact | Q, S, M, **p**, h, N, gamma | FINDING (low) | on the per-axis drive "a later axis whose drive reaches its D in the interval of an earlier axis's step loses that Link, its D subtracted" (`:931-956` with ENGINE.md:258-261): a count consumed and no Link crossed, which ALGEBRA.md 4.7 puts "outside the theorem"; under `drive_b` the coincident fire is deferred and never lost (`by_line`) |
| `_contact` `engine.py:1054-1159` | (D), (T): the hand-over of the momentum's component by the occupant's table entry, apportioned whole over several occupants (2.9, "the contact and the give D, T") | the table entry, the contents | ALGEBRAIC | nothing |
| `_level_gain`, `_level_return`, `_level_release` `engine.py:1161-1297` | atom-level-v1: (D) one Euclidean division of the action gained over 2 h d_l x the count; the return a sign comparison; the rise released as rows (6.2 row 6: a RULE under its own identity, passing the three tests in the mathematician's judgement) | h, [n_l, d_l], the axis, the sign | ALGEBRAIC under its identity, beside the law | nothing beyond the identity |
| `_give` `engine.py:1299-1375` | (D), (T): held // h units given to the flight at a contact, the recoil taken (binding-v1; 2.9) | h | ALGEBRAIC | nothing |
| `books`, `recount`, `transit_momentum` `engine.py:1418-1608` | (G): the ledger's exact sums (4.3, GAMEBOARD) | none | ALGEBRAIC | nothing |
| `detectors`, `face_detectors`, `cube_flux`, `snapshot_stream`, `snapshot`, `_node_entries` `engine.py:1614-1808` | the record's reports and the snapshot (HOST); `cube_flux` a diagnostic of the walk (GAMEBOARD, 4.4) | none | ALGEBRAIC | nothing (read-only) |

### 1.6 events/measured.py and events/amplitude.py (the body's record, the detector's set, the click's ledger)

| Component (file:lines) | The algebraic object (ALGEBRA.md) | The declared integers it takes | Verdict | The finding, or nothing |
| --- | --- | --- | --- | --- |
| `column_charges`, `count_component` `measured.py:100-152` | (B): the reader's rational charge per column over what it holds; the component a table entry reads (`scalar`, `age`, `presence`) selected by the declared key | the family table, `reads` | ALGEBRAIC | nothing |
| `DetectorSet` `measured.py:154-213` | the detector: a set of Nodes with one record and one phase (3.1, "A detector D at a Node has its own count n_D"; the dictionary's "a measurement") | `positions`, `reading`, `threshold` | ALGEBRAIC | nothing on main; ALGEBRA_AUDIT.md rows E10, S2 and T13 retire `threshold` and `reading` under the design |
| `Count`, `CountTable` `measured.py:215-330` | the body's table of counts, one accumulator per count, one loop `advance` by `by_drive` (2.1; TERMINOLOGY.md, "The counts table") | the rows' rates and walls | ALGEBRAIC | nothing |
| `AGE_WALL_SET`, `age_wall_set`, `age_wall_coefficient` `measured.py:340-402` | the age wall's declared set: the clock at 1, the flight at 1 + gamma, the drive at gamma under `drive_b`; never the phase per age (5.4; 5.9) | gamma | ALGEBRAIC | nothing |
| `counts_table`, `CovariantReadings`, `Measured` `measured.py:404-930` | the body's record: its held content per family, **p** in Z^3, its phase, its clock, its counts, its pending rows (what waits to be created again), its set (1.1, "The state") | the world's keys | ALGEBRAIC | nothing kept at a Node beyond the body's own record (the third test, 2.8) |
| `Ledger` `measured.py:932-1118` | the books per family, exact at every tick (4.3, GAMEBOARD) | none | ALGEBRAIC | nothing |
| `cmul`, `add_count`, `add_counts`, `scale_counts`, `ring_product` `amplitude.py:134-174` | (G): the group ring Z[Z_N], its addition and its convolution product (2.3, "two arms' elements multiply by the ring's convolution") | N | ALGEBRAIC | nothing |
| `half_angle` `amplitude.py:191-207` | the half-angle tables of 2N, a declared rounding at load (3.6) | s, N | ALGEBRAIC | nothing |
| `common_denominator` `amplitude.py:223-239` | a perfect-square predicate on two multiplicities (`math.isqrt` as a predicate; no rounded number enters a reading, `tests/test_integer_algebra.py:28-33`) | the multiplicities | ALGEBRAIC | nothing |
| `rungs`, `choose`, `cell_of`, `node_choice`, `node_rung` `amplitude.py:241-329` | (D): the ladder's comparison 2 T u + T <= 2 W C_k, no division at the click (2.6; 4.8) | W, u | ALGEBRAIC | nothing |
| `Offer`, `LiveRecord`, `Layer.birth`, `split`, `cancel`, `rotate`, `join`, `end` `amplitude.py:331-744` | the record's offers per set: its element of Z[Z_N] per label and Node (G); the join at a gate (P); the end of a row at a set with its content and momentum | N, the labels, the arms | ALGEBRAIC | nothing (the offers are the record's own, held by the host until the completion) |
| `Layer.evaluate`, `gram_entry`, `gram_form`, `arm_element`, `cells` `amplitude.py:766-899` | (E) the pointer **E** f as a report; (B) the weight f^T **G** f, the same integer, no pointer formed; the arms' product in the ring (2.5; 4.8, "the built click's f^T **G** f") | N, C, S | ALGEBRAIC | nothing |
| `Layer.complete` `amplitude.py:901-1003` | the one gather (with `gather_records`, row 1.3) | W, u | FINDING | the global reach of row 1.3's last row, counted once |

### 1.7 events/world.py (the world file's parse and the constants formed at load)

| Component (file:lines) | The algebraic object (ALGEBRA.md) | The declared integers it takes | Verdict | The finding, or nothing |
| --- | --- | --- | --- | --- |
| `step_divisor` `world.py:461-473`; `drive_wall` `:517-547`; `T_HEADING` `:478` | the drive's walls Q S M + abs(p_a) and Q^2 S M + abs(**p**)_1 T_h; T_h = isqrt(3 Q^2) at load (5.6 (c); drive-b-v1) | Q, S, M, **p** | ALGEBRAIC | nothing |
| `body_weight` `world.py:549-586` | the gravity charge of a moving body under `optical` with `drive_b`: (w, Q S) with w = (E'^2 + 3 gamma **p** . **p**) // E' | Q, S, M, **p**, gamma | FINDING | `energy = integer_root(square)` at `:581` is taken at run time, every interval, for every moving body under `drive_b` (`engine._frame_all` `:687-693`): a third run-time root beside the two ALGEBRA.md 2.7 names; the same square a table at load cannot hold, since **p** changes under the push |
| `CovariantDeclaration`, `_covariant`, `covariant_square` `world.py:602-625`, `:3143-3293` | the identity's declaration: c^2 = [1, d], the grain, W by (B) (5.10) | c2, grain | ALGEBRAIC under its identity | nothing |
| `FamilyDefinition`, `built_in_columns`, `_families`, `_massive`, `_declared_columns`, `_lifetime` `world.py:881-993`, `:1813-2061` | the family table: h, rho, the columns with their signs (gravity [1, 1] minus, charge plus), L, the phase circle, `phase_per_link`, the hand, `massive` (1.2 the dictionary; 2.10 "the family table the declared input on which no verb acts") | the family keys | ALGEBRAIC | nothing: `kind` is refused, the kind derived from the quantum (ENGINE.md, the refusals) |
| `default_rule`, `default_reads`, `default_table` `world.py:995-1018` | the table from the keys: a free family read, a paid one measured, the component of the rule (the model owner, 2026-09-19) | h | ALGEBRAIC | nothing: a default derived from a declared integer, not a physical name |
| `LampDefinition`, `_lamp`, `_branches`, `_label_turn` `world.py:1042-1091`, `:2189-2372` | the lamp: rate, wheel [r, W], directions, branches (the pair's labels), arms (3.6; 2.1) | [n, d], [r, W] | ALGEBRAIC | nothing |
| `Transformation`, `_products`, `_transformation`, `_handed_products` `world.py:1021-1040`, `:2103-2132`, `:2374-2479` | `become`: at, into, products, crowd (2.9) | `at`, `crowd` | ALGEBRAIC | nothing |
| `Split`, `Rotation`, `Gate`, `_rotation`, `_gate`, `_split_rows`, `_split`, `_window_reading`, `_table_entry` `world.py:2481-2774` | the apparatus's declared tables: the split's integer matrix (4.6 Theorem 2), the rotation's setting, the gate, the window and its width, `reads` | `weights`, `turns`, `inputs`, `setting`, `bit`, `parties`, s, w | ALGEBRAIC | nothing on main; the earlier audit's rows T7, T8, E6, H8 retire the split with weights and the fan under the design |
| `LevelDeclaration`, `_atom_levels` `world.py:1105-1121`, `:2776-2847` | atom-level-v1's declaration (6.2 row 6) | the axis, the sign, [n_l, d_l] | ALGEBRAIC under its identity | nothing |
| `MeasuredDefinition`, `_measured`, `body_nodes`, `_span` `world.py:1123-1224`, `:1729-1770`, `:2849-3141` | the body: position, family, amount, phase, **p**, fixed, span, held, the table (1.1, "The state") | the measured keys | ALGEBRAIC | nothing |
| `TransitDefinition`, `_in_transit` `world.py:1226-1242`, `:3798-3858` | a declared row at a Node at interval 0: the initial state, one of the four inputs (Highlights 5.4, "The declared inputs and the roads", record 189) | position, family, direction, amount, phase, age | ALGEBRAIC | nothing on main; the earlier audit's Q3 (E9) asks whether the design refuses a row inserted by no detector |
| `DetectorDefinition`, `_detectors` `world.py:1244-1253`, `:3860-3928` | the detector set: name, positions, threshold, reading | `threshold` (1 by default, `:3913`), `reading` | ALGEBRAIC | see `DetectorSet` |
| `NatureBeamWorld` `world.py:1255-1551` (`turn` `:1340`, `hypotheses` `:1444`, `boundary_per_axis` `:1513`) | the world: the torus (1.6), the circle, the constants, the identities under `hypotheses` (TERMINOLOGY.md, "The identities") | the world's keys | ALGEBRAIC | nothing |
| `bresenham_line`, `flight_bound`, `_direction_table`, `_direction`, `_directions` `world.py:1646-1727` | the digital line of a direction (the axis furthest behind, the lowest axis first: the declared tie) and the flight bound | D, P | ALGEBRAIC | nothing |
| `_record_load_checks`, `_aperture_load_check`, `_walk_arm`, `_same_class`, `_aperture_of` `world.py:3295-3620` | the loader's walk of a record's paths through the openings per arm, refusing two paths whose multiplicities' ratio is not a square (4.6; ENGINE.md, "two paths of one record ... refused at load") | the openings, the multiplicities | ALGEBRAIC | nothing (a load-time check of the declaration, HOST; it forms no state) |
| `_optical` `world.py:3930-3963` | gamma, the declared post-Newtonian input, 0 by default: the law's own number, nature's 1 a declaration per world and never a default (5.9; Highlights 5.4, "The one wall") | gamma | ALGEBRAIC | nothing |
| `parse_nature_beam_world` `world.py:3965-4214` | the world file's parse and its refusals (ENGINE.md, "The world") | every key | FINDING (low) | the parser supplies a value where the file names none: N 64 (`:4032`), suspension 1 (`:4036`), width 1 (`:4042`), direction_bound 64 (`:4043`), threshold 1 (`:3913`), phase_width N / 2 (`:2134-2138`), phase true (`:1941`); each is named a default in ENGINE.md, and every registered world declares N, so nothing on the register rests on them; they are still values the world file did not declare (AGENTS.md: "do not ... reintroduce an implicit default") |

### 1.8 The host's modules (no physical state)

`runner.py` (the run's entry and the source fingerprint), `events/run.py`
(the artifacts' writer, outside the integer audit, `numeric_audit.py:96-99`),
`snapshot_writer.py`, `trimmed_record.py` (the record's trimming, the
host's default of record 1296), `retention.py`, `world_loading.py` (the
entity definitions merged into one `families` list, ENGINE.md, "Families
from a definitions file"), `register_map.py` (the `replicated` map carried
through a regeneration), `configuration_validation.py`, `json_documents.py`,
`diagnostics/numeric_audit.py` (the static integer audit) and
`diagnostics/shell_readings.py` (the shell means in floating point, a host
diagnostic outside the engine since 2026-09-21, GAMEBOARD, read-only,
ENGINE.md:136-140) touch no physical state; none is a verb and none is a
finding. `shell_readings` is the one floating-point calculation of the
package and lives outside the physical path by design (`shell_readings.py:1-7`).

### 1.9 The count of part 1

| Verdict | Rows | Where |
| --- | --- | --- |
| ALGEBRAIC | 89 | the rows above not listed below, 5 of them under an identity beside the law (`energy_root`, `covariant_frame`, the covariant declaration, the atom levels' two rows) |
| FINDING | 12 rows, 11 findings | the collision's undeclared tie (low); `reseed_flight` and `optical_turn`, a remainder discarded at run time (two rows, one rule each); `momentum_pair` with `split_ladder`, the pushed row's root; `meet`, the meeting's root; `register`, the meeting's run-time rounding; `gather_records` with `Layer.complete`, the global reach of the completion (two rows, one finding); `body_weight`, a third run-time root; `_walk`, the open face without a count (low); `_move`, the per-axis drive's lost Link (low); `parse_nature_beam_world`, the implicit defaults (low) |
| deferred to another row | 2 | `square_ladder` (to `momentum_pair`), `_frame_all` (to `body_weight`) |

103 rows over the nine physical modules; the ranking of the findings is
in part 5.

## 4. THE ONE FORM for declaring an experiment from today

The owner's word (record 1435 as the Boss quoted it): the experiments are
defined algebraically and from the algebra they descend to the board. The
form has four steps in this order; a runner fills the first before touching
a world file, and a number whose kind is not named is not a result (record
281). Nothing below is a rule of the law; it is the order of the work.

### 4.1 The template

**Step 1. The algebraic declaration** (a file `docs/designs/<series>/DECLARATION.md`
or the series README's first section, written before any world file):

1. The objects, each named as an ALGEBRA.md object with its chapter:
   the torus Z_X x Z_Y x Z_Z with its faces per axis (1.6; a periodic axis
   the algebra's own, an open face a declared deviation, record 1421 as
   quoted); the phase circle Z_N (1.5); the family table, one row per
   family with h, rho, the columns, L (1.2, 2.10); the records the lamps
   birth, elements of Z[Z_N] with the wheel [r, W] (1.5, 2.1, 3.6); the
   bodies with M, **p** in Z^3, their tables (1.1); the detectors, each a
   set of Nodes with one record and its own count (3.1); the apparatus's
   declared tables, if any (the split's integer matrix, 4.6; the rotation
   **U**_s, 3.6; the gate, 2.4).
2. Their declared integers, every one with its kind (a declared input of
   kind 2, Highlights 5.4 "The declared inputs and the roads"): Q, N, S,
   K = [n, d], the suspension [n, d], h per family, [r, W] per lamp, gamma
   under `optical`, P for a direction table, and the world's extents.
3. The verbs that act, per object, from the six of chapter 2 and the 31
   couplings of 2.9 by reference: the flight (T, D), the push (B, T, D),
   the merge (G), the collision (P), the click (E, D), the split (P, B, D,
   T), the transformation (D, T).
4. The pins: every expected DETECTOR reading as a closed form of the
   declared integers, written before any run from an identity of chapter
   4 or a line of chapter 5 with its rung (rung 1 exact within the
   remainder, rung 2 a limit), with its bracket; a COMPUTATION named so;
   no pin from a run.
5. The readings by kind, each one named before the run with the line of
   the record it is read from (ENGINE.md, "The detector's readings by
   type"): DETECTOR (a click, a count between clicks on one detector's own
   record, a ratio of such counts; 3.2), GAMEBOARD (a diagnostic, printed
   with its expectation, never pinned, never compared with nature),
   COMPUTATION, HOST, CONVERSION. An experiment with no DETECTOR reading is
   a diagnostic run, and says so.
6. The identity: the law alone (`beam-v1`), or a hypothesis beside it
   under its own key and name (TERMINOLOGY.md, "The identities"), stated
   so that it can fail.

**Step 2. The descent to the board**: the world file, one key per object of
step 1 and nothing in it that step 1 does not name (ENGINE.md, "The
world"): `shape` and `boundary` for the torus and its faces; `N` for the
circle; `families` (or `entity_definitions` with `entities`) for the family
table; `K`, `release`, `suspension`, `width` and `action` for the declared
integers; `measured` for the bodies and their tables; `lamp` with `rate` and
`wheel` for the records; `detectors` with `positions` and `reading` for the
detectors; `clock_stamp` true wherever a reading is a count of a detector's
own record; the identity's key where step 1.6 names one. The generator
`make_worlds.py` writes it and `expectations.json` beside it from step 1.4,
no number typed by hand (TERMINOLOGY.md, "Register"; the loader's refusals
are the check that nothing outside the algebra entered, ENGINE.md, the
refusals).

**Step 3. The run**: once, headless, dated, fingerprinted
(`PYTHONPATH=src python tools/run_series.py --out <dir> <worlds>` or
`python -m event_universe --init <world> --output <dir>`); a research run,
never a test (CONTRIBUTING.md, the rule of 2026-09-17); the per-row click
lines kept only when a reader of step 4 needs them (`--keep-row-clicks`,
ENGINE.md, "The trimmed record").

**Step 4. The reading**: the series' tool under `tools/click_readings/`
reads the record alone (the `gather`, `record`, `click`, `birth` and face
lines), prints every number with its kind, compares each DETECTOR reading
with its pin of step 1.4 and reports a reading outside its bracket with its
numbers, never moved; the run's entry goes beside its worlds in the series
README with its row in docs/EXPERIMENTS.md and its fingerprint in
docs/VALIDATION.md (CONTRIBUTING.md item 8).

### 4.2 The worked example: `amplitude/mz_equal.json` (series L1, the Mach-Zehnder with equal arms)

**Step 1, the algebraic declaration** (as the register already holds it,
`examples/events/amplitude/README.md:51` and `:73`, `expectations.json:5`
under `mz_equal` with its derivation at `:4322`; docs/EXPERIMENTS.md:4015):

1. The objects: the torus 5 x 5 x 1 with z periodic and x, y open (1.6);
   Z_64 (1.5); one paid family `light`, h = 1 (the family table, from
   `entities/families.json`, the entity `photon`); one lamp at (0, 0, 0)
   birthing one record per self-creation on the two arms +x and +y with the
   turns 0 and 16 (a quarter turn on one arm), the wheel [1, 64] (the
   record an element of Z[Z_64] on two arms, 2.1, 3.6); two mirrors at
   (3, 0, 0) and (0, 3, 0), each a body of `light` with the table
   `rerelease` on one direction (the apparatus's declared table, the
   Outside); the splitter at (3, 3, 0), a `rerelease` with the weights
   [21, 20] and [20, 21] selected by the arrival's side and the turns
   [16, 0], [0, 16] (the split's integer matrix, an isometry up to the
   scaling, 4.6 Theorem 2); the two ports D1 at (4, 3, 0) and D2 at
   (3, 4, 0), each a detector set of one Node reading `sum` (the record's
   scope, 3.1).
2. The declared integers, all of kind 2: Q = 64, N = 64, S = 1, K =
   1048576 (the pair [1, 1048576]), the release [0, 1], the suspension 0,
   h = 1, the lamp's amount 1048576 (its reservoir), the wheel [1, 64], 80
   intervals.
3. The verbs: the flight (T, D) on the two arms; the mirrors' re-emission
   (T, P); the split (P, B, D, T); the merge with the cancel at the ports
   (G); the click of the record by the ladder (E, D): the weight f^T **G**
   f per port, the cell 2 T u + T <= 2 W C_k, one click per record (2.5,
   2.6).
4. The pins, COMPUTATION from chapter 4 before the run: the offers 1681 /
   1682 at D1 and 1 / 1682 at D2 for every u (the bilinear form on the
   splitter's rows, 4.8; `expectations.json:4322`); the clicks over 64
   births D1 64 and D2 0 (4.12: "One click per record, never two ... P(D1
   and D2 in one record) = 0 exactly (the cancel exact; mz_equal 64 / 0,
   DETECTOR)").
5. The readings by kind: DETECTOR, the `gather` lines' `chosen` set per
   record, counted per port (the `world` list of `run.json`); GAMEBOARD,
   the `cancel` lines and the books; COMPUTATION, the offers 1681 / 1682
   and 1 / 1682 printed beside the gathers' `weight`; no CONVERSION.
6. The identity: `beam-v1` with `amplitude-v1` under `hypotheses` (a lamp
   is declared; TERMINOLOGY.md, "The identities").

**Step 2, the descent**: `examples/events/amplitude/mz_equal.json` (one
line), key for key: `shape` [5, 5, 1] and `boundary` {"z": "periodic"} for
1; `N` 64 for 1; `entity_definitions` and `entities` [photon] for the
family table; `K`, `release`, `suspension` for 2; `measured` with the
lamp's `lamp` {rate [1, 1], wheel [1, 64], directions, turns [0, 16]}, the
two mirrors' `table` {"light": "rerelease"} with one direction each, the
splitter's `table` with `inputs`, `weights`, `turns`; `detectors` D1 and D2
with `reading` "sum" for 1; `ticks` 80 for 2. Nothing in the file that
step 1 does not name. Written by `amplitude/make_worlds.py`.

**Step 3, the run**: registered in the L entry (docs/EXPERIMENTS.md:3951
and :4433, the re-run at head 4028b020 through `tools/run_series.py`).

**Step 4, the reading**: `tools/amplitude_path.py` (DETECTOR the gathers,
GAMEBOARD the splits and cancels, `--check` against `run.json`'s `world`);
the register's line D1 64, D2 0 (docs/EXPERIMENTS.md:4015).

### 4.3 Which existing worlds fit the form, and which do not

**Fit the form (a declaration with pins before the run, a world file
one-to-one with it, a DETECTOR reading by kind):** the series whose
`expectations.json` was written before the run from the algebra and whose
readings tool labels every number: amplitude (L; 73 worlds), c_measured
(Q), clock_word (T), shell_clock (X), moving_detector, newton_side,
massive_rows (W), optical (the pin worlds and the body worlds),
flow_link, lamp_shell, drive_b, covariant (S, under its identity), weak
(J), quarks (R), the orbit_lamp k17 pair (4 worlds), atoms (its pins in
docs/designs/atoms/PINS.md), hubble_stars (its pins written, its time
base to be re-declared) and bell (A2 and the choosers: the pins the
theorem's, docs/EXPERIMENTS.md:997 and :3187): 205 of the 241 ALGEBRAIC
worlds.

**Do not yet fit the form (the declaration is of algebra objects, but the
pins were not written from the algebra into a register file before the
run, or the reading is not by kind in one):** the two root worlds
`two_slits` and `one_slit`, the detector definition worlds (4),
heisenberg (8), lensing without the meeting (4), nucleus (8), binding (3)
and bohr (7): 36 worlds whose register entry (docs/EXPERIMENTS.md) reads
the pins from the design prose or from a warm run. Their declaration is
one file each under step 1 and no world file change.

**Outside the form by verdict:** the 42 HISTORY worlds (part 2) stay as
the record of their date and are not re-run under it; the 15 RE-DECLARE
worlds are re-declared first (the time base, `clock_stamp`) and then fit.

## Parts 2, 3 and 5

The world table (part 2), the tools (part 3) and the closing table (part 5) land in the next commit on this branch.
