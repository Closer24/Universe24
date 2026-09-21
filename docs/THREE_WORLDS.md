# The three worlds: every thing of the system in the vector world, the software world and our world

The model owner, 2026-09-21 (translated): "let there be precise definitions
between what a thing is in the vector world, what it is in the software world
and what it is in our world; a click, for us, is a sampling of the game engine
that yields a number, and it does an operation in the engine, a vector
operation, and an operation in our world; do it for all the things in our
system, so that the different transformations are clear." Written by the Boss
from [vector_form/LAW.md](designs/vector_form/LAW.md), [ENGINE.md](ENGINE.md)
and [HIGHLIGHTS.md](HIGHLIGHTS.md) 5.7; the software column is verified against
the code by the architect (record 212). Notation per record 184: a scalar
plain, a vector in bold lowercase, a matrix or an operator in bold uppercase.

## The three worlds and the six transformations

- **The vector world** (the law): integer vectors on tori and the six
  operations of the map **F** (the translation of an accumulator by its rate,
  the bilinear form with a declared matrix, the group-ring addition, the
  permutation, the evaluation, the Euclidean division with the remainder kept);
  space is the translation group of the GameBoard, time the index of **F**'s
  application, the record an element of the group ring Z[Z_N].
- **The software world** (the engine): the host's representation of the same
  objects and operations: int64 columns of the store, the Count rows of a
  body's counts table, the functions that apply an operation, the tables built
  once at load, the run's record (metadata, events, state) and the register
  (`expectations.json`, `gate_set.json`, the READMEs).
- **Our world** (the observer's): what a human names and sees: a particle, a
  source, a screen, a distance, a time, a speed, a mass, a force, a
  probability, an experiment; reached only through a detector's reading.

| From | To | The transformation |
| --- | --- | --- |
| our world | the vector world | the declaration: the world file's families, bodies, apparatus and grain are the inputs of the law (record 189); a physical thing becomes a row of the family table and a placed body |
| the vector world | the software world | the representation: a vector's components are int64 columns, an operation is a function, a declared matrix is a table at load, the map **F** is the engine's interval |
| the software world | the vector world | the reading back: a run is **F** applied t times; the register's integers are the components of the state at the recorded events; nothing in the software adds to the law (the host's costs and readings are labelled host) |
| the software world | our world | the detector's line: the run's record is read by the click lines, the readings and the books, and a page shows them; the register's pins are detector readings |
| the vector world | our world | the derivation's limits (DERIVATIONS_BEAM.md: Newton, Doppler, Born, Young, Bohr, the delay field) and the dictionary of the observed values (5.7: a distance, a time, a speed, a mass, an energy, a force, an angle, a probability, c) |
| our world | the software world | the world file (JSON) and the run command; an experiment's design names the vector it will read before the run (record 205) |

## The things, one row each

| The thing | In the vector world | In the software world | In our world |
| --- | --- | --- | --- |
| the GameBoard | the translation group Z_X x Z_Y x Z_Z (a circle per periodic axis, a segment with faces per open one) | `GameBoard` (`core/game_board.py`); the extent and boundaries of the world file | space; the volume the experiment fills |
| a Node | an element of the group, an index; it holds nothing | the position columns of a row (x, y, z); no object of its own | a place, a point of space |
| a Link | a generator of the group (a unit step on one axis) | a row's position moved by one axis unit | the smallest distance; nothing lies between two Nodes |
| an interval | one application of the map **F**, the time index t | one step of the engine (`engine.py`, `nature_beam.py`) | the tick of time, the smallest duration; a clock counts them as turns |
| a row (a message in flight) | a point of Node x D x Z_N x Z x Z^+ (position, direction, phase, age, amount, number) | one row of the store (`NatureBeamStore`, int64 columns) | a quantum on its way, unseen until a click |
| a record | the vector **f** in Z[Z_N] per (end Node, label), the rows of one number | `LiveRecord` and the layer's ledger (`amplitude.py`) | the one message an apparatus sent: "one photon", "one electron"; the thing that clicks once |
| a body (a measured event) | held contents, the momentum vector **p**, a phase, an age, the counts table (one accumulator per count) | `Measured` with `counts` (`measured.py`) | a particle with mass, a star, a planet, a detector's plate |
| a family | a row of the family table: content unit, cost h, charge rho, the strong column sigma, lifetime L, phase rate n / d, hand | the world file's `families` parsed by `world.py` | a kind of particle: free (photon-like) or paid (electron-like); physics' particle table |
| the amount | an integer, the units in a row or record | the `amount` column | the intensity, how many quanta |
| the content | an integer M in the family's units | `content` on a body or a paid row | mass (the mass number) |
| the phase | an element of the circle Z_N | the `phase` column | the wave's phase; interference |
| the age | an integer, the intervals since the event | the `age` column | the time since emission |
| the momentum vector **p** | an integer 3-vector at the grain Q | `momentum` on a body, the label on a row | momentum: the direction and pace of a particle |
| a direction D | an element of the fan F_P, a primitive integer vector | the direction index; the flight's accumulator | the direction of propagation |
| the flight | the translation of the Manhattan accumulator (rate 2 S_1 Q, wall 2 T_D) with the three deficits on the digital line | the walk step (`nature_beam.py`; the accumulator on the no-tables branch) | propagation at c; light travel |
| the drive | the translation of a body's accumulator (per axis today; on the momentum's direction under form B) | `by_drive` in the engine's step | a particle's motion, its velocity |
| the push (the coupling) | the bilinear form **C a**, the reader's charges times the arriving flow, added to **p** | `push_form` and the push Count rows | force: gravity, electricity, the strong column |
| the reading | the moments of order 0, 1, 2 of the arriving rows at a Node, and the age moment | `read_arrivals`, `Reading` | what a detector feels: density, current, stress (**T**) |
| the merge | the addition in Z[Z_N] of identical rows at one Node (an antiphase pair cancels) | the merge (`nature_beam.py`) | interference at a point; cancellation |
| the split | the multiplication by the apparatus's integer matrix (w a_i, m A, phase + t_i) | the split entries (`world.py`, `nature_beam.py`) | a beam splitter, a slit, a mirror |
| the fan | the split whose matrix is the angular measure over F_P | the fan's weights built at load | Huygens' re-emission, diffraction |
| the collision | a permutation of the eight slots, the table's group action | `collide` with the cached table | scattering at a free Node |
| the rotation, the gate | a linear map with the half-angle entries; a permutation of the labels | the rotations and the gate (`amplitude.py`) | a polariser, a wave plate; a CNOT gate |
| the lamp | the birth of a record with its amount, family and wheel value | `_lamp` (`world.py`) and the birth | a source: a laser, a lamp, an emitter |
| the wheel value u | a scalar on Z_W, an accumulator on the lamp's record | the `u` field of the record; a Count row under the golden wheel | the source's phase at emission, the deterministic stand-in for a draw |
| the detector | a set of Nodes with a table entry naming the family it reads and a threshold T | the detector entries of the world file; the ladder (`amplitude.py`) | a plate, a photomultiplier, a screen, a counter |
| the click | Threshold_u( Rungs_T( Gram_G( Reading_R( record ) ) ) ), one cell, then a translation of the state | the click line of the events record (`clicks`), `complete` | a detection: a dot on the screen; the sampling of the engine that yields a number; the observed event |
| the threshold T | the divisor of the rungs b_k = (2 W C_k + T) // (2 T) | `threshold` on the entry | the detector's sensitivity |
| the turn | the accumulator of a body's phase at the rate content x n / d | `acc_turn` (the branch), `by_clock` (main) | a clock's tick, proper time |
| the owed count | the accumulator at the presence times the rate | `acc_owed` | a clock's slowing in a crowd, the gravitational slowing |
| the release | the accumulator of a body's emission, held x n / d per direction | the release (`nature_beam.py`) | emission: radiation, the field's source |
| the meeting (meeting-v1) | the crowd's flow and the arc permutation toward the target | `meeting.py` | the deflection of light near a mass (lensing) |
| the hand | a pseudoscalar bit; the hemisphere rule | the `hand` column (int8) | chirality, parity |
| the crossing rule | a comparison on the last two Links of a body and a row | `met` (the crossing branch) | a moving observer meets a ray once: Doppler's cause |
| the books | the ledger's sums per family, exact at every tick | `engine.books`, `Ledger` | the conservation laws: energy, momentum, charge |
| the register | the recorded components of the state at the recorded events | `expectations.json`, `gate_set.json`, the READMEs | the lab notebook; the numbers compared with nature |
| a run | **F** applied t times to the initial state | `execute_run` and the run's record (metadata, events, state) | an experiment performed; time passing |
| an experiment | a world file, a detector, a derived expectation and a run that compares | the world JSON, the series' tools and pages | a laboratory measurement |
| the grain (N, P, Q, W, K) | the sizes of the tori and the declared roundings at load | the world keys and the tables | the resolution of nature, finite by the law's claim |
| c | the norm of the flight operator, 1 / sqrt 3 Links per interval | the table constants T_D and S_1 Q | the speed of light: a unit conversion |
| gamma (the Lorentz factor) | the limit of the pair-in-motion's computed clock (section 12) or lorentz-v1's imposed root | not built | time dilation |

A thing missing from this table is missing from the law's vocabulary: add its
row before adding its rule.
