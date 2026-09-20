"""The world of the Beam Law (beam-v1): its keys and their refusals.

A world of this law is a JSON object with `"law": "beam"` and nothing of the
earlier engines' schemas (no `contents`, no `initial_shadows`, no
`wait_per_quantum`, no `dynamics`; none of the old engine's keys): the
refusal names the key at fault. `"law": "events"` is refused naming the Beam
Law and docs/MIGRATION.md (the law of events, `events-v1`, was deleted
on 2026-09-19). What a world declares ([the Beam Law](../../../docs/BEAM_LAW.md),
the model owner, 2026-09-19):

- `shape`, three positive extents; `boundary` `"open"` (the default: the edge
  is infinity on every face, what leaves clicks on the face detector) or an
  object with any of the keys `x`, `y`, `z`, each `"open"` or `"periodic"`,
  the missing axes open; `ticks`;
- `K`, the clock's rate, one for the world: an integer K, the content per
  phase step per self-creation, read as the pair `[1, K]`, or (since
  2026-09-20, the four unifications (2), BEAM_LAW note 33) a pair `[n, d]`
  of phase steps per unit of content per self-creation like `release`, the
  turn of a measured event `by_clock(age, content x n, d)`
  (`NatureBeamWorld.turn`), refused at half the circle; the record carries
  the key as declared; `N`,
  the steps of the phase circle (64 by default, a power of two from 2 through
  4096); `release` `[n, d]`, the rays a measured event of a free family
  releases per self-creation per declared direction per unit of content,
  read off its clock; `suspension` `[n, d]`, the rate of the
  clock's count: a measured event owes `by_clock(age, presence x n, d)`
  intervals after its self-creation, the presence being the amount of every
  ray at its Node of every number but its own (an integer w is accepted as
  `[w, 1]`; `[1, 1]` by default; 0 or `[0, d]` for none); `width`, the
  width S of the push (the model owner's D1, 2026-09-19): a free measured
  event of content M with the momentum component p on an axis steps one
  Link per (S x M + p) / p self-creations on that axis, an integer from 1
  (the default: the rule as it was, one Link per (M + p) / p); 0 or a
  negative width is refused; `age_bound`, the largest age a ray may carry
  (an integer from 1; the age is the count of intervals since the measured
  event that created the ray, kept whole on the record since 2026-09-20 so
  that a measured event may read it; BEAM_LAW section 2): on a GameBoard with an
  open axis it is by default twice the flight bound, the age at which every
  straight ray has left a GameBoard of that diameter (`flight_bound`); on a
  GameBoard periodic on every axis, which no ray leaves, it is required and
  refused if absent; a declared ray's `age` must not exceed it, and a run
  in which a ray on the GameBoard carries an age beyond it is refused;
  `action`, optional: h, the quantum of action of the turn by momentum (an
  integer from 1, in label units times Links; the model owner's decision
  of 2026-09-20 on Bohr, "put it as parameters outside the GameBoard like the
  age"; BEAM_LAW section 10, note 30): a measured event that declares
  `phase_by_momentum` turns its phase, at every Link it steps on an axis
  whose momentum component is p, so that after k Links stepped on that
  axis the phase has turned floor(k x |p| x N / h) mod N steps (the count
  k derived from its age by the step rule, the turn at one step the
  difference of two floors, no register anywhere); absent by default, and
  without it nothing turns by momentum;
- `directions`, optional: integer vectors beyond the six headings that a
  lamp, a measured event or a ray in transit may name; the world's direction
  table `D` is the two rest vectors (0, 0, 0) ("here a", "here b"), the six
  headings in Port order and these, in that order; each declared vector is
  primitive with every component in -P .. P, P = `direction_bound` (64 by
  default, at most 4096 entries in the table);
- `families`: each with a `name`, its `quantum` (h, required: the content
  of one unit of it per phase step of its emitter's turn; the kind of the
  family follows from it and is not declared: h = 0 is a free family,
  matter, whose measured events release at the world's rate, whose rays
  carry no content and are read for gravity and electricity, their label
  the amount along the direction; h >= 1 is a paid family, light, released
  only by a lamp that spends its content: a release costs the emitter
  quantum x s per unit at a self-creation whose turn is s steps, the unit
  carries that content and the momentum quantum x s along its direction,
  and a click measures it, E = h f), for a free family its `charge`, the
  charge per unit of content, rho, an integer or a pair `[n, d]` (d from
  1; an integer c is `[c, 1]`; 0 by default; the model owner's decision
  of 2026-09-20, Highlights 5.4: a measured event's charge is rho times
  its content, and the electric push is one product per arriving free
  ray, M_A x (rho_A rho_B - 1) x V_B), for a paid family since the same
  day its `charge` as a whole charge per unit of amount (D-1, the
  physicist's design of the weak force and the owner's "go on
  everything", item (2); BEAM_LAW note 35 (ii)): an integer c, a pair
  with a denominator other than 1 refused, read on the charge line of the
  books only, so that the charge of a measured event is rho times its
  content for a free family and the declared whole charge times the
  amount (the units it clicked) for a paid family; the push is untouched
  (a paid ray pushes by its label, and the paid family's electric column
  value stays 0), and a lamp on a measured event of a charged paid family
  is refused (its releases would create charge from nothing: a charged
  paid family is born by a transformation or declared in transit), and
  since the
  same day the columns (the model owner, Highlights 5.4, "one mechanism
  for all the laws on the GameBoard"; the mathematician's verified form,
  the identity `columns-v1`): the push is a signed inner product over the
  columns a family declares per unit of content, `gravity` the built-in
  first column of every family (the value [1, 1], the sign minus, never
  declared), `charge` the built-in second column (the sign plus; the
  family key `charge` is the shorthand for its value) and, per family,
  `columns`, an object of column name to `{"value": n or [n, d], "sign":
  1 or -1}` for any further column (a name's sign is the column's, one
  per name across the world; a family that does not name a column
  carries [0, 1] there; a paid family's values must be 0; at most
  `COLUMN_LIMIT` columns in all; the world's column order is gravity,
  charge, then the names in the order of their first declaration),
  `lifetime` (L, optional, since 2026-09-20: the model owner's decision
  on the strong force's range, "the lifetime L, counted on the event's own
  age"; an integer from 1 through `age_bound`, a scalar: the flight gives
  every direction one speed, so L intervals of flight are a sphere; an
  event in transit whose age reaches L at the end of the walk makes no
  next event but a click on the border `lifetime`, booked exactly as an
  open face books an escape; absent, the family's events live for ever,
  as every family did),
  `phase` (true by default; false: the family has no phase circle, its rays
  carry phase 0 and never turn, its measured events never turn, no
  `phase_window` is accepted for it) and `phase_per_link` (an integer
  0 .. N - 1, 0 by default: the phase steps a ray of the family turns at
  every Link crossed). The key `kind` of the first NatureBeam worlds is refused
  naming this derivation and docs/MIGRATION.md (one canonical form);
- `measured`: the measured events at the start, one per Node, each with a
  `position`, its `family`, its `amount` (a positive whole number of units,
  below K x N / 2 for a family with a phase circle), optionally `held`
  (since 2026-09-20, the physicist's design of the strong force: an object
  of family name to a positive whole content the measured event holds of
  that family beside its own, so that a nucleon is one measured event
  holding its charged family and one unit of a strong family; the event's
  own family may not be named, an unknown family, a content below 1 or
  not an integer is refused; a free family held is released at the
  world's rate like its own, a paid one is inert; its charge in every
  column is the rational sum over what it holds; the phase-turn bound
  covers the total), and optionally its
  `phase`, its `momentum` (three integers), `fixed` (true: an apparatus held in place, it takes
  pushes into its momentum and never steps), its `span` (three odd
  integers from 1, `[1, 1, 1]` by default: the measured event is a body on
  the set of `span_x x span_y x span_z` Nodes centred on its `position`,
  ONE record on all of them, the model owner's principle of 2026-09-19
  applied to the electron on 2026-09-20, "the electron of width 3", BEAM_LAW
  section 10, note 30: its clock, its threshold and its push read the one
  reading set summed over its Nodes, the step moves the whole set as one
  and is refused onto a Node of another measured event, through an open
  face the whole body clicks on the face detector, on a periodic axis it
  wraps, no collision acts at any of its Nodes, its releases are
  apportioned whole over its Nodes; a span must fit the axis and the body
  must lie inside the GameBoard on an open axis), `phase_by_momentum` (true:
  the body turns its phase by its momentum label at every Link it steps,
  over the world's `action`; false by default; refused without `action`,
  on a `fixed` measured event, which never steps, and on a family without
  a phase circle), its `directions` (the
  directions it releases on and re-emits on, as vectors or indices of the
  world's table; the six headings by default), its `table` (family name to
  `read`, `measure`, `rerelease` or `pass`, or to an object `{"rule": ...,
  "phase_window": s, "reads": key}`; the table is generated from the
  families' keys by `default_table`, a free family read, the push taken and
  the rays going on, a paid family measured, the click, and a world declares
  only the entries that differ: a window, a rule off the default, a `reads`
  component; an entry equal to the default is accepted and changes nothing)
  and, for a measured event of a paid family, its `lamp` (`rate` `[n, d]` units
  per self-creation per direction, `directions` the directions it releases
  on, the six headings by default, and optionally its `phase_window`); and,
  since 2026-09-20 (the weak force, `weak-v1`: the model owner's "go on
  everything", item (1), the transformation `become`; the physicist's
  design, WEAK.md section 2; BEAM_LAW note 35 (iii)), its `become`, the
  clock trigger of the transformation: `{"at": a, "into": family,
  "products": [[family, amount, content per unit], ...], "crowd": c}`:
  at the self-creation whose clock reaches `at` (the event's own age
  against the key, `nature_beam.ages_at_key`, the one `by_clock` the
  lifetime reads: first at `at`, then every `at`) the measured event
  becomes an event of the family `into`, the products are paid from what
  it holds of its own family (their content R = the sum of amount x
  content, at most its declared `amount`), the rest moves to `into`, the
  products are born at that self-creation as pending rows (product k on
  the direction counted from (clock age + k) mod the directions, the
  parent's phase, the recoil over all of them, free and paid), and its
  `become` key and every `become` entry of its table are consumed;
  `crowd`, optional, an integer from 0, the gate: the transformation
  fires only at a self-creation at which the count the clock read is
  below it (the law's form of the condition that keeps a bound neutron
  stable). A free product carries the content 0, a paid one from 1; the
  transformation's charges must balance at load (rho_into x (amount - R)
  plus the paid products' whole charges against rho_from x amount), and
  the run is refused at the trigger if the event holds less than R. The
  click trigger is a table entry whose rule is `become`, `{"rule":
  "become", "phase_window": s, "phase_width": w, "into": ...,
  "products": [...]}`: an arrival that passes the threshold and the
  window is clicked exactly as `measure` clicks it and then the same
  transformation fires, its products born at the reader's next
  self-creation (the same interval if it self-creates in it); no `at`,
  no `crowd` (the window is the gate);
  every measured event is given its number at parsing, 1, 2, ... in
  declaration order;
- `phase_window`, the declared window of a detector and of an emitter: a
  setting `s`, an integer from 0 through N - 1, and since 2026-09-20 (the
  weak force, the neutrino first: the model owner's "go on everything";
  BEAM_LAW note 35) its width `phase_width`, an integer w from 1 through N,
  N / 2 by default: the w consecutive steps of the circle centred on the
  setting, [s - floor(w / 2), s - floor(w / 2) + w), a phase at the distance
  d = (phase - s) mod N inside when (d + floor(w / 2)) mod N < w
  (`nature_beam.window_admits`, the one floor of the window and its width;
  at the default N / 2 it is the half circle as it was, d < N / 4 or
  d >= 3 N / 4, exactly N / 2 steps, for N = 2 the one step d = 0). On a
  table entry (any rule but `pass`) the response is made only to a ray
  whose own phase falls in the window; a ray outside it passes. On a lamp,
  a release only at the self-creations whose clock phase falls in the
  window. A width is refused where a window is (on `pass`, on a family
  without a phase circle), without its window's setting, at 0 and beyond
  N; the admitted fraction of a source's rays is w / N exactly when the
  source's stride over the circle is coprime to N (the register's series
  J2). On a table entry
  the centre may instead be read from a reading (issue #363, 2026-09-20:
  the settings of a Bell run decided by GameBoard events): `{"reads":
  "<family>", "offset": s}` sets the centre to the phase of the coherent
  pointer (`nature_beam.coherent_pointer`, the first moment over the
  circle) of the named family's rows present at the set in the interval
  (the one reading set: every row at the set but the reader's own number)
  plus the offset s in phase steps (0 by default); the width is the law's.
  With no row of the named family at the set (or a zero pointer) the entry
  passes, the `pass` record naming `window` None and `reads`; every `click`
  of such an entry carries the `window` used. Refused: an unknown family,
  a family without a phase circle, the entry's own family, the form on
  `pass` (as any window on `pass`) and on a lamp;
- `reads` on a table entry: the component of the Node's one reading that
  the response's record carries, `scalar` (the presence), `outside`, `here`,
  `vector` (the net flow), `tensor` (the traceless part) or `age` (the age
  moment, sum amount x age over the set: a reading aid of the measured
  event, the external thing, since 2026-09-20; the GameBoard's rules never read
  the age whole); `vector` by default on `read`, `scalar` otherwise. No
  rule of the GameBoard changes with it: every coupling reads the one reading,
  the moments of the arrivals (`nature_beam.read_arrivals`); the one thing
  the key selects beside the record is what the clock counts
  (`measured.count_component`): the age moment on an entry that reads
  `age`, the presence on every other entry;
- `in_transit`, optional: rays at the start, each with a `position`,
  `family`, `number` (the measured event whose continuation it is),
  `direction` (a vector of the world's table or its index), `amount`,
  `phase` and optionally `age` (0 through `age_bound`), booked as initial
  content of the transit line; the default is an empty GameBoard that the
  releases fill;
- `detectors`, optional: named sets of measured events, each with a `name`,
  its `positions` (the `position` of a measured event each, a body on a
  set named by its centre, each in at most one detector),
  its `threshold` (1 by default): the smallest amount of a family arriving
  at the detector's Nodes in one interval, summed over the whole set and
  over every number but each Node's own; a smaller set passes; and its
  `reading`, `"wave"` (the default since 2026-09-20; the model owner: "on
  the GameBoard a ray, in the world a wave") or `"beam"` (the model owner,
  2026-09-19): a detector is a set of Nodes with ONE record (a click says
  "here, in one of these" and not which; the declared width is the
  position's uncertainty). Under `wave` the record is the square of the
  coherent pointer of the rays the set clicked in the interval, the
  window reads the set's phase and the set's phase is returned to its
  measured events; under `beam` the arriving rays are paired by opposite
  phase over the set, a paired couple passes on and the rest click, the
  record is the plain count. A measured event outside every detector is a
  detector of one Node with the default reading.

Refused, naming the key: `kind` on a family (the quantum decides it),
`charge` on a measured event (since 2026-09-20 the charge is the family's
per unit of content, docs/MIGRATION.md), a family `charge` whose
denominator is 0 or whose parts are not integers, a paid family's `charge`
with a denominator other than 1, a lamp on a measured event of a charged
paid family, a `become` without `into` or `products`, `into` naming an
unknown family or the event's own, a product naming an unknown family, a
product's amount below 1, a free product's content other than 0, a paid
product's content below 1, a product's label beyond the bound, `at` below
1 or absent on the clock trigger, `at` or `crowd` on a table entry, `crowd`
negative or not an integer, `into` or `products` on an entry whose rule is
not `become`, a `become` whose products' content exceeds the event's
`amount` or whose charges do not balance, `become` on a family (a key of
the measured event), a detector named as a
face detector is (`face:+x` and the five others), `headings` on a lamp
(`directions` replaces it),
`heading` on a ray in transit (`direction` replaces it), a column named
`gravity` (built in), `charge` declared both as the key and under
`columns`, a column's `sign` other than 1 or -1, a column value with a
denominator of 0 or a part that is not an integer, a column object with
other keys, one name with two signs across the families, a nonzero
column value on a paid family, more than `COLUMN_LIMIT` columns, a
declared reader whose push over a column from the largest release of a
family could pass 2^62 - 1 (the parser's static budget, per reader, per
family and per column, and the sum over the columns), `dynamics`,
`max_active_owners`, `port_map`, `output`, `capacity`, `groups`, a direction
that is not primitive, a component beyond P, a direction the world does not
declare, a label `Q x content x amount` beyond 2^62 - 1 on a declared ray or
a lamp's release (Q = `LABEL_SCALE` = 64: the momentum label of a ray is
along the unit vector of its direction at the flight table's scale, the
model owner's decision of 2026-09-19 on the physics-rule reviewer's
verdict, [BEAM_LAW section 2](../../../docs/BEAM_LAW.md), so every declared
`momentum` and every momentum of the record is in label units, Q per unit
of amount along a heading), `phase_per_link` outside 0 .. N - 1, `age_bound`
below 1 or absent on a GameBoard periodic on every axis, a declared `age`
beyond it, `action` below 1 or not an integer, a `span` that is not three
odd integers from 1 or larger than its axis, a body whose Nodes leave the
GameBoard on an open axis, two measured events sharing a Node, a detector
naming a Node of a body that is not its `position`, `phase_by_momentum`
without `action`, on a `fixed` measured event or on a family without a
phase circle, a turning body whose product `ticks x |p| x N` (the
count of Links stepped within the run is at most `ticks`) exceeds
2^62 - 1 for a declared momentum component p, a `lifetime` that is not
one integer from 1 (a list or a per-axis value, 0, a negative number, a
fraction) or beyond `age_bound`, a `phase_width` outside 1 .. N, on `pass`,
on a family without a phase circle or without a `phase_window`, a declared ray of a family with a
lifetime at an age at or beyond it, a detector named `lifetime` (the
border's name), and `held` naming the event's own family, an unknown
family or a content that is not a positive integer.
"""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.core.game_board import MAX_VALUE, PORT_HEADINGS, Address3
from event_universe.core.integer import bounded_gcd, by_clock, integer_root, rational_sum

BEAM_LAW = "beam-v1"
LAW_VALUE = "beam"
# The law's name before 2026-09-20 (rays-v1 is beam-v1, the same law): a world
# that still declares it is refused naming the migration, never read as a default.
OLD_LAW_VALUE = "rays"
TABLES = ("read", "measure", "rerelease", "pass", "become")
# The rule of the transformation (the weak force, 2026-09-20): the click
# and then the change of family with the products released.
BECOME_RULE = "become"
# The rule of a contact where the world declared none: a body that arrives
# at a body is a paid arrival (its momentum is its own label, kappa = 1),
# and the keys' rule for a paid arrival is `measure` (the model owner,
# 2026-09-20; docs/BEAM_LAW.md note 31 (ix)).
CONTACT_DEFAULT = "measure"
# The quantum of a free family: its unit costs nothing and carries no content.
FREE_QUANTUM = 0
# The components of the one reading a table entry may select for its record;
# `age` is the age moment, the reading aid of the measured event (the
# external thing) that also decides what its clock counts.
AGE_READS = "age"
READS = ("scalar", "outside", "here", "vector", "tensor", AGE_READS)
# The one scale Q of the law (BEAM_LAW sections 2 and 3): the time resolution
# of the flight table, where the turn of a direction is T_d = isqrt(3 |v|^2
# Q^2) and a ray makes S_1 Manhattan steps per T_d / Q intervals in the mean,
# and the length of the momentum label, `LABEL_SCALE` below.
Q = 64
MAX_PHASE_STEPS = 4096
# The bound of an amount, a content, a clock and a momentum component of this
# law: the 64-bit work register with a bit to spare for one more sum.
AMOUNT_BOUND = (1 << 62) - 1
MOMENTUM_BOUND = (1 << 62) - 1
# The momentum label's scale is the same Q: the label of a unit is the
# integer vector nearest Q D / |D| (`nature_beam.unit_label`, exactly Q e_d
# on a heading), so a label component is within Q x content x amount per
# row, and the parser's bound is that product (the model owner's decision of
# 2026-09-19, the physics-rule reviewer's correction 3).
LABEL_SCALE = Q
# The direction table: two rest vectors, the six headings, the declared rest.
REST_DIRECTIONS = 2
HEADING_OFFSET = REST_DIRECTIONS
FIXED_DIRECTIONS = REST_DIRECTIONS + 6
DEFAULT_DIRECTION_BOUND = 64
MAX_DIRECTIONS = 4096
Vector = tuple[int, int, int]
# Keys of the earlier engines' worlds, refused by name so that the refusal
# says which law the world belongs to.
OLD_KEYS = (
    "contents",
    "initial_shadows",
    "wait_per_quantum",
    "schema_version",
    "fields",
    "disturbance_types",
    "seeds",
    "spatial_fields",
    "emissions",
    "spatial_seeds",
    "external_bodies",
    "initial_field",
    "ray_interactions",
    "couplings",
    "interactions",
    "dense_field",
    "standing_field",
    "wait_reads",
    "shadow_wait",
    "slots_per_node",
    "link_ticks",
    "normal_budget",
    "operation_costs",
)
# Keys of the law of events (`events-v1`, deleted on 2026-09-19) that the law
# of the ray refuses by name.
EVENTS_KEYS = ("dynamics", "max_active_owners")
WORLD_KEYS = {
    "law",
    "model_id",
    "shape",
    "boundary",
    "ticks",
    "K",
    "N",
    "release",
    "suspension",
    "width",
    "age_bound",
    "action",
    "directions",
    "direction_bound",
    "families",
    "measured",
    "in_transit",
    "detectors",
}
# The identity of the turn by momentum, a physical hypothesis beside the
# law (the model owner's decision of 2026-09-20 on Bohr): the record carries
# it when the world declares `action`.
BOHR_RULE = "bohr-v1"
# The identity of the one mechanism of the columns (the model owner,
# 2026-09-20, "one mechanism for all the laws on the GameBoard"; the
# mathematician's verified form): the record carries it when a world
# declares a column beyond `charge`. The two built-in columns, gravity
# and charge, are the law as it was, integer by integer.
COLUMNS_RULE = "columns-v1"
# The identity of the transformation `become` (the weak force in the
# world's terms, the model owner's "go on everything", 2026-09-20): the
# record carries it when a measured event declares `become` or a table
# entry's rule is `become`.
WEAK_RULE = "weak-v1"
# The two built-in columns of every family: the first, gravity, has the
# value [1, 1] on every unit of content and the sign minus (like contents
# pull together); the second, charge, the family's `charge` per unit of
# content and the sign plus (like charges push apart). Neither is declared
# under `columns`.
GRAVITY_COLUMN = "gravity"
CHARGE_COLUMN = "charge"
GRAVITY_INDEX, CHARGE_INDEX = 0, 1
COLUMN_SIGNS = (1, -1)
# A column's declaration on a family: its value per unit of content and
# the column's sign.
COLUMN_KEYS = {"value", "sign"}
# The most columns a world may carry, the built-in two included: the
# per-group work of the push is then fixed (the mathematician's P2).
COLUMN_LIMIT = 8
# The span of a measured event on one Node (the default): a body of one.
ONE_NODE: tuple[int, int, int] = (1, 1, 1)
FAMILY_KEYS = {"name", "quantum", "charge", "columns", "lifetime", "phase", "phase_per_link"}
# The border every event in transit of a family with a lifetime clicks on
# when its age reaches the lifetime: named like a face detector in the
# records, the books' escaped lines summing it with the faces'; a declared
# detector may not take the name.
LIFETIME_NAME = "lifetime"
# The key of the first NatureBeam worlds that named the kind; the quantum decides it.
KIND_KEY = "kind"
# The key of the NatureBeam worlds before 2026-09-20 that gave a measured event its
# own whole charge; the charge is the family's per unit of content.
CHARGE_KEY = "charge"
# The charge per unit of content of a family with none: 0 as the pair [0, 1].
NO_CHARGE = (0, 1)
MEASURED_KEYS = {
    "position",
    "family",
    "amount",
    "held",
    "phase",
    "momentum",
    "fixed",
    "span",
    "phase_by_momentum",
    "directions",
    "table",
    "lamp",
    "become",
}
LAMP_KEYS = {"rate", "directions", "phase_window", "phase_width"}
# A table entry's object form: the rule, a window on any rule but `pass`
# with its width, the reading's component the record carries and, on a
# `become` entry, the transformation's `into` and `products`.
TABLE_ENTRY_KEYS = {"rule", "phase_window", "phase_width", "reads", "into", "products"}
TRANSFORM_KEYS = {"into", "products"}
# The clock trigger's keys (the measured event's `become`): the age `at`
# which it fires, the family it becomes, its products and the `crowd` gate.
BECOME_KEYS = {"at", "into", "products", "crowd"}
# The keys of the clock trigger that a table entry (the click trigger) may
# not carry: the window is its gate.
CLOCK_ONLY_KEYS = ("at", "crowd")
# A window read from a reading (issue #363, 2026-09-20): the family whose
# rows at the set give the centre, and the offset added to it.
WINDOW_READING_KEYS = {"reads", "offset"}
TRANSIT_KEYS = {"position", "family", "number", "direction", "amount", "phase", "age"}
DETECTOR_KEYS = {"name", "positions", "threshold", "reading"}
# The readings a detector may declare; the first is the default: `wave`
# since 2026-09-20 (the model owner: "on the GameBoard a ray, in the world a
# wave"; `beam` was the default from 2026-09-19 to 2026-09-20).
DETECTOR_READINGS = ("wave", "beam")
# The keys of the deleted `reversible-detector-v1`, refused by name.
REVERSIBLE_KEYS = ("port_map", "output", "capacity", "groups", "reference_phase")
# The face detectors, one per open face of the GameBoard, named by the face in
# Port order (an open face is a detector, the model owner, 2026-09-19); a
# declared detector may not take one of these names.
FACE_NAMES = ("face:+x", "face:-x", "face:+y", "face:-y", "face:+z", "face:-z")
# The GameBoard's faces per axis: open (the default) or periodic (the wrap).
AXES = ("x", "y", "z")
BOUNDARIES = ("open", "periodic")


@dataclass(frozen=True)
class Column:
    """One column of a family (the model owner, 2026-09-20, "one mechanism
    for all the laws on the GameBoard"): its name, its value per unit of
    content as the pair (n, d) with d from 1, and the column's sign, +1
    (like values push apart) or -1 (like values pull together). The columns
    of every family of a world are aligned by index: the same name at the
    same index with the same sign, [0, 1] where a family does not name it."""

    name: str
    value: tuple[int, int]
    sign: int


def built_in_columns(charge: tuple[int, int]) -> tuple[Column, Column]:
    """The two columns every family carries: gravity, the value (1, 1) on
    every unit of content with the sign minus, and charge, the family's
    charge per unit of content with the sign plus (the law as it was:
    M_A (rho_A rho_B - 1) x V_B is the case of these two columns)."""
    return Column(GRAVITY_COLUMN, (1, 1), -1), Column(CHARGE_COLUMN, charge, 1)


@dataclass(frozen=True)
class FamilyDefinition:
    """One family of the world: its name, the content of one unit of it per
    phase step of its emitter's turn (`quantum`, h; 0 for a free family,
    1 or more for a paid one: the kind is derived, never declared), its
    charge (`charge`: for a free family the charge per unit of content,
    rho, the pair (n, d) with d from 1, a measured event of the family of
    content M carrying rho x M and its rays pushing a charged reader by
    rho; for a paid family, since 2026-09-20 (D-1), the whole charge per
    unit of amount, the pair (c, 1), read on the charge line of the books
    alone: its rays push by their label and its `charge` column value is
    (0, 1)), its columns (`columns`: gravity first, charge second, the
    declared columns after, aligned by index across the families of the
    world; `charge` is the value of the second for a free family), whether
    it has a phase circle, the phase steps its rays
    turn per Link crossed, and its `lifetime` (L, or None for ever: the
    age at which an event in transit of the family clicks on the border
    `lifetime` instead of making its next event, the range of the family's
    force in Links of flight)."""

    name: str
    quantum: int
    charge: tuple[int, int] = NO_CHARGE
    phase: bool = True
    phase_per_link: int = 0
    columns: tuple[Column, ...] = ()
    lifetime: int | None = None

    def __post_init__(self) -> None:
        # A family made without its columns (the tests' bare definitions,
        # the migration tool) carries the two built-in ones; a paid
        # family's electric column is 0 (its charge is per unit of amount,
        # read on the charge line, never by the push).
        if not self.columns:
            object.__setattr__(self, "columns", built_in_columns(self.column_charge))

    @property
    def column_charge(self) -> tuple[int, int]:
        """The value of the family's `charge` column: rho for a free family,
        (0, 1) for a paid one (D-1: a paid family's charge is per unit of
        amount and is read on the charge line only)."""
        return self.charge if self.free else NO_CHARGE

    @property
    def values(self) -> tuple[tuple[int, int], ...]:
        """The family's value per column, aligned with the world's columns."""
        return tuple(column.value for column in self.columns)

    @property
    def free(self) -> bool:
        """A free family (h = 0): its release costs nothing and its rays
        carry no content."""
        return self.quantum == FREE_QUANTUM

    @property
    def unit_label(self) -> int:
        """The content one declared unit of the family carries for its
        momentum label: the quantum (one phase step of content, no emitter
        having declared its turn) for a paid family, the unit for a free
        one, whose label is the amount along the direction."""
        return max(self.quantum, 1)


def default_rule(family: FamilyDefinition) -> str:
    """The rule the family's key gives: a free family (h = 0) is read, the
    push taken and the rays going on; a paid one (h >= 1) is measured, the
    click."""
    return "read" if family.free else "measure"


def default_reads(rule: str) -> str:
    """The component of the one reading a rule's record carries unless the
    entry declares one: the net flow on `read`, the presence otherwise."""
    return "vector" if rule == "read" else "scalar"


def default_table(
    families: tuple[FamilyDefinition, ...],
) -> tuple[tuple[str, int | None, str], ...]:
    """The table generated from the keys (the model owner, 2026-09-19): per
    family in family order its rule, no window and the rule's component. A
    measured event's declared `table` overrides only the entries it names;
    an entry equal to this default is accepted and changes nothing."""
    return tuple(
        (default_rule(family), None, default_reads(default_rule(family))) for family in families
    )


@dataclass(frozen=True)
class Transformation:
    """The transformation `become` as declared (the weak force,
    2026-09-20): the family the measured event becomes (`into`, an index),
    its products as (family index, amount, content per unit) in order,
    and, for the clock trigger, the age `at` at which it fires and the
    optional `crowd` gate (None: no gate); the click trigger (a table
    entry) carries neither."""

    into: int
    products: tuple[tuple[int, int, int], ...]
    at: int | None = None
    crowd: int | None = None

    @property
    def needed(self) -> int:
        """The content the products are paid with, R = sum of amount x
        content per unit."""
        return sum(amount * content for _, amount, content in self.products)


@dataclass(frozen=True)
class LampDefinition:
    """A measured event of a paid family that releases it at a declared rate,
    `rate` = (n, d) units per self-creation on each of its `directions`
    (indices of the world's table), spending its content; with a `window`
    (a phase setting), only at the self-creations whose clock phase falls in
    the half circle centred on it."""

    rate: tuple[int, int]
    directions: tuple[int, ...]
    window: int | None
    # The window's width in steps (`phase_width`), None for the default
    # N / 2, the half circle.
    width: int | None = None


@dataclass(frozen=True)
class WindowReading:
    """A table entry's window read from a reading, as declared: the name
    of the family whose rows present at the set give the centre (the phase
    of their coherent pointer) and the offset added to it in phase steps
    (issue #363, 2026-09-20). The parser resolves the name to the family's
    index in `MeasuredDefinition.window_reads`."""

    family: str
    offset: int


@dataclass(frozen=True)
class MeasuredDefinition:
    """One measured event as declared: its Node, its family, its amount, its
    phase, its momentum, whether it is held in place, the directions it
    releases and re-emits on, its table per family (in family order) with
    the phase window and the reading key of each entry, and its lamp. Its
    charge is its family's charge per unit of content times its content
    and is not declared. `span` is the set of Nodes it is a body on (three
    odd extents centred on `position`, (1, 1, 1) for one Node),
    `phase_by_momentum` whether it turns its phase by its momentum label
    at every Link it steps (over the world's `action`), and `held` the
    content it holds per family in family order at the start: its
    `amount` under its own family and what `held` declared of the others
    (0 elsewhere). `contact` is the rule per family (in family order) by
    which this event reads a body of that family whose step onto it is
    refused (the contact through the table, 2026-09-20): the entry's rule
    where it differs from the keys' own rule for that family
    (`default_rule`: `rerelease`, `pass`, `measure` on a free family,
    `read` on a paid one), and `CONTACT_DEFAULT` (`measure`, the keys' rule
    for a paid arrival: the body's momentum is its own label) where the
    entry is the keys' own, declared or not, so that an entry equal to the
    default changes nothing. The engine reads a missing entry as the
    default. `window_reads` is, per family in family order, the window
    read from a reading (issue #363): the index of the family whose rows
    at the set give the centre and the offset, or None for a declared or
    absent centre (`windows` then holds the number, or None)."""

    position: Address3
    family: int
    amount: int
    phase: int
    momentum: Vector
    fixed: bool
    directions: tuple[int, ...]
    table: tuple[str, ...]
    windows: tuple[int | None, ...]
    reads: tuple[str, ...]
    lamp: LampDefinition | None
    span: tuple[int, int, int] = ONE_NODE
    phase_by_momentum: bool = False
    held: tuple[int, ...] = ()
    contact: tuple[str, ...] = ()
    # The width of each entry's window (`phase_width`, in family order):
    # None where none is declared, the half circle N / 2.
    widths: tuple[int | None, ...] = ()
    # The transformation (the weak force, 2026-09-20): the clock trigger
    # (`become`, None without) and per family the click trigger of the
    # entry whose rule is `become` (None elsewhere).
    become: Transformation | None = None
    transforms: tuple[Transformation | None, ...] = ()
    window_reads: tuple[tuple[int, int] | None, ...] = ()

    def __post_init__(self) -> None:
        # A definition made without `held` (the tests' bare definitions)
        # holds its amount under its own family alone, and without
        # `widths` or `transforms` declares none.
        if not self.held:
            found = [0] * (self.family + 1)
            found[self.family] = self.amount
            object.__setattr__(self, "held", tuple(found))
        if not self.widths:
            object.__setattr__(self, "widths", (None,) * len(self.table))
        if not self.transforms:
            object.__setattr__(self, "transforms", (None,) * len(self.table))
        # A definition made without `window_reads` reads no window.
        if not self.window_reads:
            object.__setattr__(self, "window_reads", (None,) * len(self.table))


@dataclass(frozen=True)
class TransitDefinition:
    """A ray at the start: at its Node, of its family and number, on its
    direction (an index of the world's table), its amount, its phase and its
    age."""

    position: Address3
    family: int
    number: int
    direction: int
    amount: int
    phase: int
    age: int


@dataclass(frozen=True)
class DetectorDefinition:
    """A named set of measured events, its threshold and its reading
    (`beam` or `wave`)."""

    name: str
    positions: tuple[Address3, ...]
    threshold: int
    reading: str = DETECTOR_READINGS[0]


@dataclass(frozen=True)
class NatureBeamWorld:
    """A parsed world of the Beam Law. `boundary` is the declared value
    as the record carries it (the string `"open"` or the object per axis);
    `periodic` says per axis (x, y, z) whether the walk wraps; `directions`
    is the table `D`: the two rest vectors, the six headings and the declared
    rest; `action` is h, the quantum of action of the turn by momentum, or
    None when the world declares none."""

    model_id: str
    shape: Address3
    boundary: str | dict[str, str]
    periodic: tuple[bool, bool, bool]
    ticks: int
    K: int | tuple[int, int]
    turn_rate: tuple[int, int]
    phase_steps: int
    release: tuple[int, int]
    suspension: tuple[int, int]
    width: int
    age_bound: int
    directions: tuple[Vector, ...]
    direction_bound: int
    families: tuple[FamilyDefinition, ...]
    measured: tuple[MeasuredDefinition, ...]
    in_transit: tuple[TransitDefinition, ...]
    detectors: tuple[DetectorDefinition, ...]
    action: int | None = None

    @property
    def phase_mask(self) -> int:
        return self.phase_steps - 1

    def turn(self, age: int, content: int) -> int:
        """The turn of a measured event's phase at the self-creation from
        `age`: `by_clock(age, content x n, d)` phase steps at the clock's
        rate `turn_rate` = (n, d), the free release's own form at the rate
        [1, K] (the four unifications (2), BEAM_LAW note 33); the frame
        refuses a turn of half the circle or more."""
        numerator, denominator = self.turn_rate
        return by_clock(age, content * numerator, denominator)

    @property
    def columns(self) -> tuple[tuple[str, int], ...]:
        """The world's columns in order, (name, sign): gravity, charge, then
        the declared names; every family's `columns` is aligned with it."""
        return tuple((column.name, column.sign) for column in self.families[0].columns)

    @property
    def declared_columns(self) -> tuple[str, ...]:
        """The names of the columns beyond the two built in."""
        return tuple(name for name, _ in self.columns[CHARGE_INDEX + 1 :])

    @property
    def lifetimes(self) -> bool:
        """Whether any family declares a lifetime (the border `lifetime` is
        then a detector of the record, and the inverse interval is refused)."""
        return any(family.lifetime is not None for family in self.families)

    @property
    def transformations(self) -> bool:
        """Whether any measured event declares a transformation: the clock
        trigger `become` or a table entry whose rule is `become`."""
        return any(
            entry.become is not None or any(t is not None for t in entry.transforms)
            for entry in self.measured
        )

    @property
    def hypotheses(self) -> list[str]:
        """The identities of the physical hypotheses the world declares
        beside the law, in a fixed order: `bohr-v1` for the turn by momentum
        (`action`), `columns-v1` for the one mechanism of the columns (a
        column beyond `charge`, or a lifetime: a force of nature in this
        law is a column with a sign and a range), `weak-v1` for the
        transformation `become` (the weak force in the world's terms)."""
        found = []
        if self.action is not None:
            found.append(BOHR_RULE)
        if self.declared_columns or self.lifetimes:
            found.append(COLUMNS_RULE)
        if self.transformations:
            found.append(WEAK_RULE)
        return found

    @property
    def boundary_per_axis(self) -> dict[str, str]:
        """The GameBoard's faces per axis, `x`, `y`, `z` to `open` or `periodic`."""
        return {
            axis: BOUNDARIES[1] if wraps else BOUNDARIES[0]
            for axis, wraps in zip(AXES, self.periodic, strict=True)
        }

    def owners(self, family: int) -> tuple[int, ...]:
        """The numbers whose rays of a family can exist: the measured events
        that hold the family and are free (they release it), the lamps of it,
        the measured events whose table re-releases it (their number is
        stamped on what leaves them) and the numbers of the rays in transit
        at the start."""
        found = []
        for index, entry in enumerate(self.measured):
            number = index + 1
            definition = self.families[family]
            holds = family < len(entry.held) and entry.held[family] > 0
            rules = [t for t in (entry.become, *entry.transforms) if t is not None]
            transforms_into = any(
                (t.into == family and definition.free) or any(p[0] == family for p in t.products)
                for t in rules
            )
            if (
                (holds and (definition.free or (entry.family == family and entry.lamp is not None)))
                or entry.table[family] == "rerelease"
                or transforms_into
                or any(item.number == number and item.family == family for item in self.in_transit)
            ):
                found.append(number)
        return tuple(found)

    def detector_of(self, position: Address3) -> int | None:
        """The index of the detector a Node belongs to, if any."""
        for index, detector in enumerate(self.detectors):
            if position in detector.positions:
                return index
        return None


def is_nature_beam_world(document: object) -> bool:
    """Whether a document declares the Beam Law (`"law": "beam"`)."""
    return isinstance(document, dict) and document.get("law") == LAW_VALUE


def _object(value: object, label: str, allowed: set[str], required: set[str]) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{BEAM_LAW}: {label} must be a JSON object")
    retired = [key for key in (*REVERSIBLE_KEYS, "headings", "heading") if key in value]
    if retired:
        raise ValueError(
            f"{BEAM_LAW}: {label} declares {', '.join(retired)}, a key of the deleted law of "
            "events or its reversible detector (see docs/MIGRATION.md; a lamp and a ray declare "
            "`directions` and `direction`)"
        )
    unknown = set(value) - allowed
    if unknown:
        raise ValueError(f"{BEAM_LAW}: {label} has unknown keys: {', '.join(sorted(unknown))}")
    missing = required - set(value)
    if missing:
        raise ValueError(f"{BEAM_LAW}: {label} lacks keys: {', '.join(sorted(missing))}")
    return {str(key): item for key, item in value.items()}


def _integer(value: object, label: str, minimum: int, maximum: int = AMOUNT_BOUND) -> int:
    if type(value) is not int or value < minimum or value > maximum:
        raise ValueError(f"{BEAM_LAW}: {label} must be an integer from {minimum} through {maximum}")
    return value


def _ratio(value: object, label: str, zero: bool) -> tuple[int, int]:
    """A rate n / d as `[n, d]` (n from 0 with `zero`, d positive) or one integer."""
    if type(value) is int:
        return _integer(value, label, 0 if zero else 1), 1
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{BEAM_LAW}: {label} must be an integer or [numerator, denominator]")
    numerator = _integer(value[0], f"{label} numerator", 0 if zero else 1)
    denominator = _integer(value[1], f"{label} denominator", 1)
    return numerator, denominator


def _signed_ratio(value: object, label: str) -> tuple[int, int]:
    """A charge per unit of content n / d as an integer c (the pair (c, 1))
    or as `[n, d]`, n an integer of either sign and d an integer from 1,
    each within the bound of a declared charge; a denominator of 0 and a
    part that is not an integer are refused naming the key."""
    if type(value) is int:
        return _integer(value, label, -MAX_VALUE, MAX_VALUE), 1
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(
            f"{BEAM_LAW}: {label} must be an integer or [numerator, denominator], the charge "
            "per unit of content"
        )
    numerator = _integer(value[0], f"{label} numerator", -MAX_VALUE, MAX_VALUE)
    denominator = _integer(value[1], f"{label} denominator", 1, MAX_VALUE)
    return numerator, denominator


def _address(value: object, label: str, shape: Address3) -> Address3:
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{BEAM_LAW}: {label} must be three integers")
    found = tuple(
        _integer(item, label, 0, extent - 1) for item, extent in zip(value, shape, strict=True)
    )
    return found[0], found[1], found[2]


def _vector(value: object, label: str, bound: int) -> Vector:
    """A primitive integer vector with every component in -bound .. bound."""
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{BEAM_LAW}: {label} must be three integers")
    found = tuple(_integer(item, label, -bound, bound) for item in value)
    if found == (0, 0, 0):
        raise ValueError(
            f"{BEAM_LAW}: {label} must not be the zero vector (the rest slots are the table's)"
        )
    if bounded_gcd(bounded_gcd(found[0], found[1]), found[2]) != 1:
        raise ValueError(f"{BEAM_LAW}: {label} must be a primitive vector (its components coprime)")
    return found[0], found[1], found[2]


def _direction_table(value: object, bound: int) -> tuple[Vector, ...]:
    """The table `D`: the two rest vectors, the six headings, the declared."""
    table: list[Vector] = [(0, 0, 0), (0, 0, 0), *PORT_HEADINGS]
    if not isinstance(value, list):
        raise ValueError(f"{BEAM_LAW}: directions must be a list of integer vectors")
    for index, item in enumerate(value):
        vector = _vector(item, f"directions[{index}]", bound)
        if vector in table:
            raise ValueError(f"{BEAM_LAW}: directions[{index}] repeats a direction of the table")
        table.append(vector)
    if len(table) > MAX_DIRECTIONS:
        raise ValueError(f"{BEAM_LAW}: the direction table holds at most {MAX_DIRECTIONS} entries")
    return tuple(table)


def _direction(value: object, label: str, table: tuple[Vector, ...], *, rest: bool = False) -> int:
    """A direction named by its vector or by its index in the world's table;
    a rest vector only where `rest` allows it (a ray in transit)."""
    if type(value) is int:
        index = _integer(value, label, 0, len(table) - 1)
    else:
        if not isinstance(value, list) or len(value) != 3 or any(type(v) is not int for v in value):
            raise ValueError(f"{BEAM_LAW}: {label} must be a direction vector or an index of the table")
        vector = (value[0], value[1], value[2])
        if vector not in table:
            raise ValueError(
                f"{BEAM_LAW}: {label} names a direction the world does not declare {list(vector)} "
                "(the six headings or a vector of `directions`)"
            )
        index = table.index(vector)
    if index < REST_DIRECTIONS and not rest:
        raise ValueError(f"{BEAM_LAW}: {label} must not be a rest direction")
    return index


def _directions(value: object, label: str, table: tuple[Vector, ...]) -> tuple[int, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{BEAM_LAW}: {label} must be a nonempty list of directions")
    found = tuple(_direction(item, label, table) for item in value)
    if len(set(found)) != len(found):
        raise ValueError(f"{BEAM_LAW}: {label} repeats a direction")
    return found


def flight_bound(shape: Address3, table: tuple[Vector, ...]) -> int:
    """The age at which every straight ray has left an open GameBoard of this
    shape: the longest Manhattan flight on the GameBoard is D = X + Y + Z - 2
    Links (inside and out), a ray of direction v makes S_1 = |a| + |b| + |c|
    steps per period of its line and the least tau with m(tau) >= M steps
    is at most ceil(M x T_d / (S_1 Q)) (BEAM_LAW section 3), so the exiting
    walk of a ray of direction v is at age at most ceil(ceil(D / S_1) x
    T_d / Q); the largest over the table's moving directions. A rest
    direction never moves and a collision or a periodic axis may keep a ray
    longer: the bound is exact for the straight flight alone."""
    diameter = shape[0] + shape[1] + shape[2] - 2
    largest = 1
    for vector in table:
        manhattan = sum(abs(component) for component in vector)
        if manhattan == 0:
            continue
        turn = integer_root(3 * sum(component * component for component in vector) * Q * Q)
        periods = -(-diameter // manhattan)
        largest = max(largest, -(-(periods * turn) // Q))
    return largest


def body_nodes(
    position: Address3,
    span: tuple[int, int, int],
    shape: Address3,
    periodic: tuple[bool, bool, bool],
) -> tuple[Address3, ...] | None:
    """The set of Nodes a measured event of `span` is a body on: the block
    of span_x x span_y x span_z Nodes centred on `position` (each span odd,
    the offsets -(s - 1) / 2 .. (s - 1) / 2 per axis), in the fixed order
    of the offsets (x, then y, then z, ascending; the order the releases
    are apportioned in). On a periodic axis an offset wraps; on an open
    axis a Node beyond the face means the body has left the GameBoard and the
    result is None (the whole body clicks on the face detector). A span
    of (1, 1, 1) is the one Node `position`."""
    axes: list[list[int]] = []
    for axis in range(3):
        half = (span[axis] - 1) // 2
        coordinates = []
        for offset in range(-half, half + 1):
            coordinate = position[axis] + offset
            if periodic[axis]:
                coordinate %= shape[axis]
            elif not 0 <= coordinate < shape[axis]:
                return None
            coordinates.append(coordinate)
        axes.append(coordinates)
    return tuple((x, y, z) for x in axes[0] for y in axes[1] for z in axes[2])


def _span(value: object, label: str, shape: Address3) -> tuple[int, int, int]:
    """The span of a body: three odd integers from 1, each at most its
    axis's extent (so that the body's Nodes are distinct)."""
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{BEAM_LAW}: {label} must be three odd integers from 1")
    found = []
    for item, extent in zip(value, shape, strict=True):
        span = _integer(item, label, 1, extent)
        if span % 2 == 0:
            raise ValueError(f"{BEAM_LAW}: {label} must be three odd integers from 1 (a centred body)")
        found.append(span)
    return found[0], found[1], found[2]


def _age_bound(
    value: object, shape: Address3, periodic: tuple[bool, bool, bool], table: tuple[Vector, ...]
) -> int:
    """The largest age a ray may carry: declared, or twice the flight bound
    on a GameBoard with an open axis (the slack of one collision or one wrap of
    a periodic axis), required on a GameBoard periodic on every axis, which no
    ray leaves."""
    if value is not None:
        return _integer(value, "age_bound", 1)
    if all(periodic):
        raise ValueError(
            f"{BEAM_LAW}: age_bound is required on a GameBoard periodic on every axis: no ray "
            "leaves it, so the largest age a ray may carry (the bound of the store) must be "
            "declared"
        )
    return 2 * flight_bound(shape, table)


def _boundary(value: object) -> tuple[str | dict[str, str], tuple[bool, bool, bool]]:
    """The GameBoard's faces: `"open"` on every face, or an object with any of
    the keys `x`, `y`, `z`, each `"open"` or `"periodic"`, the missing axes
    open. Returns the value as declared (what the record carries) and, per
    axis, whether the walk wraps. A closed GameBoard and every other word are
    refused."""
    if value == BOUNDARIES[0]:
        return BOUNDARIES[0], (False, False, False)
    if (
        isinstance(value, dict)
        and set(value) <= set(AXES)
        and all(item in BOUNDARIES for item in value.values())
    ):
        declared = {str(key): str(item) for key, item in value.items()}
        wraps = tuple(declared.get(axis, BOUNDARIES[0]) == BOUNDARIES[1] for axis in AXES)
        return declared, (wraps[0], wraps[1], wraps[2])
    raise ValueError(
        f"{BEAM_LAW}: the GameBoard is open (its edge is infinity) unless an axis is declared "
        'periodic (boundary "open" or an object of "x", "y", "z" to "open" or "periodic"); '
        "a closed GameBoard is refused"
    )


def _declared_columns(
    value: object, label: str, charged: bool
) -> dict[str, tuple[tuple[int, int], int]]:
    """A family's `columns`: an object of column name to `{"value": n or
    [n, d], "sign": 1 or -1}`. The built-in `gravity` is refused (one
    owner); `charge` under `columns` is refused when the family also
    declares the key `charge` (one owner of a value); a sign other than 1
    or -1, a value with a denominator of 0 or a part that is not an
    integer, and an object with other keys are refused naming the key."""
    if not isinstance(value, dict):
        raise ValueError(
            f"{BEAM_LAW}: {label} must be an object of column name to "
            '{"value": n or [n, d], "sign": 1 or -1}'
        )
    found: dict[str, tuple[tuple[int, int], int]] = {}
    for name, entry in value.items():
        column = f"{label}[{name!r}]"
        if name == GRAVITY_COLUMN:
            raise ValueError(
                f"{BEAM_LAW}: {column} declares the built-in column {GRAVITY_COLUMN!r} (the value "
                "[1, 1] on every unit of content of every family with the sign minus; never declared)"
            )
        if name == CHARGE_COLUMN and charged:
            raise ValueError(
                f"{BEAM_LAW}: {column} and the key `charge` declare the column {CHARGE_COLUMN!r} "
                "twice on one family (`charge` is the shorthand for `columns.charge`; declare one)"
            )
        obj = _object(entry, column, COLUMN_KEYS, COLUMN_KEYS)
        sign = obj["sign"]
        if type(sign) is not int or sign not in COLUMN_SIGNS:
            raise ValueError(
                f"{BEAM_LAW}: {column}.sign must be 1 (like values push apart) or -1 (like values "
                "pull together); a column's sign is a key, not a formula"
            )
        found[str(name)] = (_signed_ratio(obj["value"], f"{column}.value"), sign)
    return found


def _lifetime(value: object, label: str, age_bound: int) -> int | None:
    """A family's lifetime: one integer from 1 through the world's
    `age_bound` (an event at age L is still on the GameBoard when the walk
    ends, so the store's bound must hold it); a list or a per-axis value is
    refused (the flight gives every direction one speed, so a scalar L is
    a sphere and a vector would be a box), as are 0, a negative number and
    a fraction."""
    if value is None:
        return None
    if isinstance(value, list):
        raise ValueError(
            f"{BEAM_LAW}: {label} must be one integer (a scalar): the flight table gives every "
            "direction one speed, so L intervals of flight reach a sphere; a per-axis lifetime "
            "is refused"
        )
    lifetime = _integer(value, label, 1)
    if lifetime > age_bound:
        raise ValueError(
            f"{BEAM_LAW}: {label} {lifetime} is beyond the world's age_bound {age_bound}: an "
            "event at the age L is still on the GameBoard at the end of its walk (declare a "
            "larger age_bound or a shorter lifetime)"
        )
    return lifetime


def _families(
    value: object, phase_steps: int, age_bound: int = AMOUNT_BOUND
) -> tuple[FamilyDefinition, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{BEAM_LAW}: families must be a nonempty list")
    found: list[FamilyDefinition] = []
    declared: list[dict[str, tuple[tuple[int, int], int]]] = []
    # The world's columns beyond the two built in, in the order of their
    # first declaration, with the sign the first declaration gave; a later
    # family declaring another sign for the name is refused.
    names: list[str] = []
    signs: dict[str, tuple[int, int]] = {}
    for index, entry in enumerate(value):
        if isinstance(entry, dict) and KIND_KEY in entry:
            raise ValueError(
                f"{BEAM_LAW}: families[{index}] declares {KIND_KEY}, a key removed on 2026-09-19: "
                "the kind of a family follows from its quantum (0 free, 1 or more paid) and is "
                "not declared; see docs/MIGRATION.md"
            )
        obj = _object(entry, f"families[{index}]", FAMILY_KEYS, {"name", "quantum"})
        name = obj["name"]
        if not isinstance(name, str) or not name:
            raise ValueError(f"{BEAM_LAW}: families[{index}].name must be a nonempty string")
        if any(item.name == name for item in found):
            raise ValueError(f"{BEAM_LAW}: two families named {name!r}")
        quantum = _integer(obj["quantum"], f"families[{index}].quantum", FREE_QUANTUM, MAX_VALUE)
        columns = _declared_columns(
            obj.get("columns", {}), f"families[{index}].columns", "charge" in obj
        )
        charge_value = columns.pop(CHARGE_COLUMN, None)
        if charge_value is not None and charge_value[1] != 1:
            raise ValueError(
                f"{BEAM_LAW}: families[{index}].columns[{CHARGE_COLUMN!r}].sign must be 1: the "
                "electric column's sign is plus (like charges push apart)"
            )
        charge = (
            charge_value[0]
            if charge_value is not None
            else _signed_ratio(obj.get("charge", 0), f"families[{index}].charge")
        )
        if quantum != FREE_QUANTUM and charge[1] != 1:
            raise ValueError(
                f"{BEAM_LAW}: families[{index}].charge: a paid family's charge is per unit of "
                f"amount and whole (an integer; the pair {list(charge)} is refused on {name!r}; D-1, "
                "2026-09-20)"
            )
        for column, ((numerator, _), sign) in columns.items():
            if quantum != FREE_QUANTUM and numerator:
                raise ValueError(
                    f"{BEAM_LAW}: a paid family (quantum {quantum}) carries no column value "
                    f"({name}, the column {column!r}: its rays push by their content)"
                )
            if column not in signs:
                signs[column] = (sign, index)
                names.append(column)
            elif signs[column][0] != sign:
                raise ValueError(
                    f"{BEAM_LAW}: families[{index}].columns[{column!r}].sign {sign} differs from "
                    f"the sign {signs[column][0]} families[{signs[column][1]}] declared: a column's "
                    "sign is the column's, one per name across the world"
                )
        phase = obj.get("phase", True)
        if type(phase) is not bool:
            raise ValueError(f"{BEAM_LAW}: families[{index}].phase must be true or false")
        per_link = _integer(
            obj.get("phase_per_link", 0), f"families[{index}].phase_per_link", 0, phase_steps - 1
        )
        if per_link and not phase:
            raise ValueError(
                f"{BEAM_LAW}: families[{index}].phase_per_link is refused for a family without a "
                "phase circle"
            )
        lifetime = _lifetime(obj.get("lifetime"), f"families[{index}].lifetime", age_bound)
        found.append(FamilyDefinition(name, quantum, charge, phase, per_link, lifetime=lifetime))
        declared.append(columns)
    if 2 + len(names) > COLUMN_LIMIT:
        raise ValueError(
            f"{BEAM_LAW}: the world declares {len(names)} columns beyond gravity and charge; at most "
            f"{COLUMN_LIMIT} columns in all (the per-group work of the push is fixed)"
        )
    # Every family's columns aligned with the world's: (0, 1) where it
    # names none.
    return tuple(
        FamilyDefinition(
            family.name,
            family.quantum,
            family.charge,
            family.phase,
            family.phase_per_link,
            (
                *built_in_columns(family.column_charge),
                *(
                    Column(column, columns.get(column, (NO_CHARGE, 0))[0], signs[column][0])
                    for column in names
                ),
            ),
            family.lifetime,
        )
        for family, columns in zip(found, declared, strict=True)
    )


def _window(value: object, label: str, phase_steps: int) -> int:
    """A phase window's setting: a step of the circle, 0 through N - 1."""
    return _integer(value, label, 0, phase_steps - 1)


def default_width(phase_steps: int) -> int:
    """The width of a window that declares none: the half circle, N / 2
    steps (for N = 2 the one step), the window as it was until 2026-09-20."""
    return phase_steps // 2


def _width(obj: dict[str, object], label: str, phase_steps: int, phased: bool, rule: str) -> int | None:
    """A window's width (`phase_width`): an integer w from 1 through N, the
    w consecutive steps centred on the window's setting; None where none is
    declared (the half circle). Refused where a window is (on `pass`, which
    responds to nothing, and for a family without a phase circle, whose rays
    carry no phase) and without a `phase_window` (a width is the width of a
    window, and the window's setting says where it is centred)."""
    if "phase_width" not in obj:
        return None
    if rule == "pass":
        raise ValueError(
            f"{BEAM_LAW}: {label}.phase_width is refused on pass: a width is a width of a "
            "response, and pass responds to nothing"
        )
    if not phased:
        raise ValueError(
            f"{BEAM_LAW}: {label}.phase_width is refused for a family without a phase circle: "
            "its rays carry no phase to read"
        )
    if "phase_window" not in obj:
        raise ValueError(
            f"{BEAM_LAW}: {label}.phase_width needs the window's setting `phase_window` (a "
            "width is the width of a window centred on its setting)"
        )
    return _integer(obj["phase_width"], f"{label}.phase_width", 1, phase_steps)


def _label_bound(
    amount: int, content: int, table: tuple[Vector, ...], directions: tuple[int, ...], label: str
) -> None:
    """The momentum label of a release or a declared ray, `content x amount x
    u_d` with u_d the unit vector of the direction at the scale Q (no
    component beyond Q), must fit the bound on every component: Q x content
    x amount within 2^62 - 1, that is content x amount below 2^56."""
    for direction in directions:
        if LABEL_SCALE * content * amount > MOMENTUM_BOUND:
            raise ValueError(
                f"{BEAM_LAW}: {label}: the momentum label {LABEL_SCALE} x {content} x {amount} = "
                f"{LABEL_SCALE * content * amount} along {list(table[direction])} exceeds the "
                f"integer bound {MOMENTUM_BOUND} (content x amount at most {MOMENTUM_BOUND // LABEL_SCALE})"
            )


def _lamp(
    value: object,
    label: str,
    phase_steps: int,
    phased: bool,
    table: tuple[Vector, ...],
    quantum: int,
    amount: int,
    turn_rate: tuple[int, int],
) -> LampDefinition:
    obj = _object(value, label, LAMP_KEYS, {"rate"})
    rate = _ratio(obj["rate"], f"{label}.rate", zero=True)
    directions = _directions(
        obj.get("directions", list(range(HEADING_OFFSET, FIXED_DIRECTIONS))),
        f"{label}.directions",
        table,
    )
    window = None
    if "phase_window" in obj:
        if not phased:
            raise ValueError(
                f"{BEAM_LAW}: {label}.phase_window is refused on a lamp of a family without a "
                "phase circle (a window is a width on the circle, and the family has none)"
            )
        window = _window(obj["phase_window"], f"{label}.phase_window", phase_steps)
    width = _width(obj, label, phase_steps, phased, "measure")
    # The largest label a release can carry: the rate's numerator units at
    # the largest turn the content allows (the whole part of amount x n / d
    # at the clock's rate [n, d]).
    largest_turn = max(1, amount * turn_rate[0] // turn_rate[1])
    _label_bound(max(1, rate[0]), quantum * largest_turn, table, directions, f"{label} (the release)")
    return LampDefinition(rate, directions, window, width)


def _products(
    value: object,
    label: str,
    families: tuple[FamilyDefinition, ...],
    table: tuple[Vector, ...],
    directions: tuple[int, ...],
) -> tuple[tuple[int, int, int], ...]:
    """The products of a transformation: a list of `[family, amount,
    content per unit]`, the amount an integer from 1, the content 0 for a
    free family (its unit carries none) and from 1 for a paid one, each
    product's label bounded on the event's directions as a release is."""
    if not isinstance(value, list):
        raise ValueError(
            f"{BEAM_LAW}: {label} must be a list of [family, amount, content per unit] products"
        )
    names = {family.name: index for index, family in enumerate(families)}
    found: list[tuple[int, int, int]] = []
    for k, item in enumerate(value):
        entry_label = f"{label}[{k}]"
        if not isinstance(item, list) or len(item) != 3:
            raise ValueError(f"{BEAM_LAW}: {entry_label} must be [family, amount, content per unit]")
        name, amount_value, content_value = item
        if not isinstance(name, str) or name not in names:
            raise ValueError(f"{BEAM_LAW}: {entry_label} names an unknown family {name!r}")
        family = names[name]
        amount = _integer(amount_value, f"{entry_label} amount", 1)
        if families[family].free:
            if type(content_value) is not int or content_value != 0:
                raise ValueError(
                    f"{BEAM_LAW}: {entry_label}: a free family's product carries no content (0; "
                    f"{name!r} is free)"
                )
            content = 0
        else:
            content = _integer(content_value, f"{entry_label} content", 1)
        _label_bound(amount, content if content else 1, table, directions, entry_label)
        found.append((family, amount, content))
    return tuple(found)


def _transformation(
    value: object,
    label: str,
    families: tuple[FamilyDefinition, ...],
    family: int,
    amount: int,
    table: tuple[Vector, ...],
    directions: tuple[int, ...],
    clock: bool,
) -> Transformation:
    """A transformation as declared: the clock trigger (`become` on the
    measured event: `at`, `into`, `products`, `crowd`) or the click
    trigger (`into` and `products` of a `become` table entry). `into` a
    known family other than the event's own; the products' content at most
    the event's `amount`; the charges balanced: rho_into x (amount - R)
    plus the paid products' whole charges per unit of amount equal to
    rho_from x amount (charge conservation is a refusal of the parser)."""
    obj = _object(value, label, BECOME_KEYS if clock else TRANSFORM_KEYS, {"into", "products"})
    names = {definition.name: index for index, definition in enumerate(families)}
    into_name = obj["into"]
    if not isinstance(into_name, str) or into_name not in names:
        raise ValueError(f"{BEAM_LAW}: {label}.into names an unknown family {into_name!r}")
    into = names[into_name]
    if into == family:
        raise ValueError(
            f"{BEAM_LAW}: {label}.into names the event's own family {into_name!r}: a "
            "transformation is a change of family"
        )
    products = _products(obj["products"], f"{label}.products", families, table, directions)
    at = crowd = None
    if clock:
        if "at" not in obj:
            raise ValueError(
                f"{BEAM_LAW}: {label} lacks keys: at (the clock trigger fires at the self-creation "
                "whose clock reaches `at`)"
            )
        at = _integer(obj["at"], f"{label}.at", 1)
        if "crowd" in obj:
            crowd = _integer(obj["crowd"], f"{label}.crowd", 0)
    needed = sum(a * c for _, a, c in products)
    if needed > amount:
        raise ValueError(
            f"{BEAM_LAW}: {label}: the products' content {needed} exceeds the event's amount "
            f"{amount} (a transformation is paid from what the event holds of its own family)"
        )
    before = rational_sum(
        [(families[family].column_charge[0] * amount, families[family].column_charge[1])]
    )
    after_terms = [
        (families[into].column_charge[0] * (amount - needed), families[into].column_charge[1])
    ]
    after_terms.extend(
        (families[f].charge[0] * a, families[f].charge[1])
        for f, a, _ in products
        if not families[f].free
    )
    after = rational_sum(after_terms)
    if before != after:
        raise ValueError(
            f"{BEAM_LAW}: {label}: the transformation's charges do not balance: {into_name!r} on "
            f"{amount - needed} with the paid products carries {list(after)} against "
            f"{list(before)} on {families[family].name!r} (charge conservation is a refusal at load)"
        )
    return Transformation(into, products, at, crowd)


def _window_reading(value: object, label: str, phase_steps: int) -> WindowReading:
    """A window read from a reading, `{"reads": "<family>", "offset": s}`
    (issue #363): the family's name (resolved and refused by `_measured`,
    which knows the families) and the offset, a step of the circle, 0 by
    default."""
    obj = _object(value, label, WINDOW_READING_KEYS, {"reads"})
    family = obj["reads"]
    if not isinstance(family, str) or not family:
        raise ValueError(f"{BEAM_LAW}: {label}.reads must name a family")
    return WindowReading(family, _window(obj.get("offset", 0), f"{label}.offset", phase_steps))


def _table_entry(
    value: object,
    label: str,
    phase_steps: int,
    phased: bool,
    default: str,
    families: tuple[FamilyDefinition, ...],
    family: int,
    amount: int,
    table: tuple[Vector, ...],
    directions: tuple[int, ...],
) -> tuple[str, int | WindowReading | None, str, int | None, Transformation | None]:
    """One table entry: a rule string, or `{"rule": ..., "phase_window": s,
    "phase_width": w, "reads": key}` (the rule the family's default when the
    object omits it, so a window alone is a lawful entry; a window and its
    width refused on `pass`, which responds to nothing, and for a family
    without a phase circle, whose rays carry no phase; the width refused
    without the window's setting; the reading's component `vector` by
    default on `read`, `scalar` otherwise), or a `become` entry, the click
    trigger of the transformation, with its `into` and `products` (refused
    on any other rule; `at` and `crowd` refused: the window is the gate).
    Returns the rule, the window's setting (a number, or a `WindowReading`
    where the entry reads its centre from a reading, issue #363), the
    component, the window's width (None: N / 2) and the transformation
    (None but on `become`)."""
    reads: object = None
    obj: dict[str, object] = {}
    if isinstance(value, dict):
        clock_only = [key for key in CLOCK_ONLY_KEYS if key in value]
        if clock_only:
            raise ValueError(
                f"{BEAM_LAW}: {label} declares {', '.join(clock_only)}: a key of the clock trigger "
                "(the measured event's `become`), not of a table entry, whose gate is its window"
            )
        obj = _object(value, label, TABLE_ENTRY_KEYS, set())
        rule = obj.get("rule", default)
        window: int | WindowReading | None = None
        if isinstance(obj.get("phase_window"), dict):
            window = _window_reading(obj["phase_window"], f"{label}.phase_window", phase_steps)
        elif "phase_window" in obj:
            window = _window(obj["phase_window"], f"{label}.phase_window", phase_steps)
        reads = obj.get("reads")
    else:
        rule, window = value, None
    if rule not in TABLES:
        raise ValueError(f"{BEAM_LAW}: {label} must be one of {TABLES}")
    if window is not None and rule == "pass":
        raise ValueError(
            f"{BEAM_LAW}: {label}.phase_window is refused on pass: a window is a width of a "
            "response, and pass responds to nothing"
        )
    if window is not None and not phased:
        raise ValueError(
            f"{BEAM_LAW}: {label}.phase_window is refused for a family without a phase circle: "
            "its rays carry no phase to read"
        )
    width = _width(obj, label, phase_steps, phased, str(rule))
    transformation = None
    if rule == BECOME_RULE:
        missing = TRANSFORM_KEYS - set(obj)
        if missing:
            raise ValueError(
                f"{BEAM_LAW}: {label} lacks keys: {', '.join(sorted(missing))} (a `become` entry "
                "names the family the reader becomes and its products)"
            )
        transformation = _transformation(
            {key: obj[key] for key in TRANSFORM_KEYS},
            label,
            families,
            family,
            amount,
            table,
            directions,
            clock=False,
        )
    elif TRANSFORM_KEYS & set(obj):
        raise ValueError(
            f"{BEAM_LAW}: {label} declares into or products on the rule {rule!r}: they belong to a "
            "`become` entry"
        )
    if reads is None:
        reads = default_reads(str(rule))
    if reads not in READS:
        raise ValueError(f"{BEAM_LAW}: {label}.reads must be one of {READS}")
    return str(rule), window, str(reads), width, transformation


def _measured(
    value: object,
    shape: Address3,
    periodic: tuple[bool, bool, bool],
    families: tuple[FamilyDefinition, ...],
    turn_rate: tuple[int, int],
    phase_steps: int,
    release: tuple[int, int],
    table: tuple[Vector, ...],
    ticks: int,
    action: int | None,
) -> tuple[MeasuredDefinition, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{BEAM_LAW}: measured must be a list")
    names = {family.name: index for index, family in enumerate(families)}
    found: list[MeasuredDefinition] = []
    # Every Node of every body so far: two measured events never share one.
    occupied: set[Address3] = set()
    for index, entry in enumerate(value):
        label = f"measured[{index}]"
        if isinstance(entry, dict) and CHARGE_KEY in entry:
            raise ValueError(
                f"{BEAM_LAW}: {label} declares {CHARGE_KEY}, a key removed on 2026-09-20: the "
                "charge of a measured event is its family's charge per unit of content times "
                "its content (the family's `charge`, an integer or [n, d]); see docs/MIGRATION.md"
            )
        obj = _object(entry, label, MEASURED_KEYS, {"position", "family", "amount"})
        position = _address(obj["position"], f"{label}.position", shape)
        if any(item.position == position for item in found):
            raise ValueError(f"{BEAM_LAW}: two measured events at one Node {list(position)}")
        span = _span(obj.get("span", list(ONE_NODE)), f"{label}.span", shape)
        nodes = body_nodes(position, span, shape, periodic)
        if nodes is None:
            raise ValueError(
                f"{BEAM_LAW}: {label}: a body of span {list(span)} centred on {list(position)} "
                "leaves the GameBoard through an open face"
            )
        shared = [node for node in nodes if node in occupied]
        if shared:
            raise ValueError(
                f"{BEAM_LAW}: two measured events share the Node {list(shared[0])} "
                f"({label}, a body of span {list(span)})"
            )
        occupied.update(nodes)
        family_name = obj["family"]
        if not isinstance(family_name, str) or family_name not in names:
            raise ValueError(f"{BEAM_LAW}: {label}.family names an unknown family")
        family = names[family_name]
        amount = _integer(obj["amount"], f"{label}.amount", 1)
        held = [0] * len(families)
        held[family] = amount
        declared_held = obj.get("held", {})
        if not isinstance(declared_held, dict):
            raise ValueError(f"{BEAM_LAW}: {label}.held must map family names to contents")
        for key, content in declared_held.items():
            if key not in names:
                raise ValueError(f"{BEAM_LAW}: {label}.held names an unknown family {key!r}")
            if names[key] == family:
                raise ValueError(
                    f"{BEAM_LAW}: {label}.held names the event's own family {key!r}, whose "
                    "content is `amount`"
                )
            held[names[key]] = _integer(content, f"{label}.held[{key!r}]", 1)
        phased = families[family].phase
        # The turn's static bound: 2 x content x n below d x N at the clock's
        # rate [n, d] (2 x content below K x N for an integer K), the exact
        # refusal of a turn at half the circle staying the frame's.
        if phased and 2 * sum(held) * turn_rate[0] >= turn_rate[1] * phase_steps:
            raise ValueError(
                f"{BEAM_LAW}: {label}.amount must keep 2 x content below K x N (the phase step "
                "per self-creation below half the circle; the content held of every family counts; "
                "at the clock's rate [n, d], 2 x content x n below d x N)"
            )
        # A measured event of a family without a phase circle has phase 0.
        phase = _integer(obj.get("phase", 0), f"{label}.phase", 0, phase_steps - 1 if phased else 0)
        momentum_value = obj.get("momentum", [0, 0, 0])
        if not isinstance(momentum_value, list) or len(momentum_value) != 3:
            raise ValueError(f"{BEAM_LAW}: {label}.momentum must be three integers")
        momentum = tuple(_integer(item, f"{label}.momentum", -AMOUNT_BOUND) for item in momentum_value)
        fixed = obj.get("fixed", False)
        if type(fixed) is not bool:
            raise ValueError(f"{BEAM_LAW}: {label}.fixed must be true or false")
        turning = obj.get("phase_by_momentum", False)
        if type(turning) is not bool:
            raise ValueError(f"{BEAM_LAW}: {label}.phase_by_momentum must be true or false")
        if turning:
            if action is None:
                raise ValueError(
                    f"{BEAM_LAW}: {label}.phase_by_momentum needs the world's `action` (the "
                    "quantum h of the turn by momentum), which the world does not declare"
                )
            if fixed:
                raise ValueError(
                    f"{BEAM_LAW}: {label}.phase_by_momentum is refused on a fixed measured "
                    "event, which never steps a Link"
                )
            if not phased:
                raise ValueError(
                    f"{BEAM_LAW}: {label}.phase_by_momentum is refused for a family without a "
                    "phase circle: there is no phase to turn"
                )
            # The bound of the turn: a body steps at most one Link per
            # interval, so within the run k <= ticks Links on an axis and
            # the product k x |p| x N of the declared momentum must fit.
            largest = max(abs(component) for component in momentum)
            if ticks * largest * phase_steps > MOMENTUM_BOUND:
                raise ValueError(
                    f"{BEAM_LAW}: {label}: the turn by momentum forms k x |p| x N up to "
                    f"{ticks} x {largest} x {phase_steps} = {ticks * largest * phase_steps} "
                    f"within the run, beyond the integer bound {MOMENTUM_BOUND} (a smaller "
                    "momentum, N or run)"
                )
        directions = _directions(
            obj.get("directions", list(range(HEADING_OFFSET, FIXED_DIRECTIONS))),
            f"{label}.directions",
            table,
        )
        # The table the keys give; the declared entries override what they name.
        rules: list[str] = []
        windows: list[int | None] = []
        reads: list[str] = []
        widths: list[int | None] = []
        transforms: list[Transformation | None] = []
        window_reads: list[tuple[int, int] | None] = [None] * len(families)
        for rule, window, component in default_table(families):
            rules.append(rule)
            windows.append(window)
            reads.append(component)
            widths.append(None)
            transforms.append(None)
        declared = obj.get("table", {})
        if not isinstance(declared, dict):
            raise ValueError(f"{BEAM_LAW}: {label}.table must map family names to rules")
        for key, entry_value in declared.items():
            if key not in names:
                raise ValueError(f"{BEAM_LAW}: {label}.table names an unknown family {key!r}")
            at = names[key]
            entry_label = f"{label}.table[{key!r}]"
            rule, entry_window, component, widths[at], transforms[at] = _table_entry(
                entry_value,
                entry_label,
                phase_steps,
                families[at].phase,
                rules[at],
                families,
                family,
                amount,
                table,
                directions,
            )
            if isinstance(entry_window, WindowReading):
                # The window read from a reading (issue #363): the named
                # family must exist, carry a phase circle and differ from
                # the entry's own family (its rows are what the window gates).
                if entry_window.family not in names:
                    raise ValueError(
                        f"{BEAM_LAW}: {entry_label}.phase_window.reads names an unknown family "
                        f"{entry_window.family!r}"
                    )
                if not families[names[entry_window.family]].phase:
                    raise ValueError(
                        f"{BEAM_LAW}: {entry_label}.phase_window.reads names the family "
                        f"{entry_window.family!r}, which has no phase circle: its rows carry no "
                        "phase to read a centre from"
                    )
                if entry_window.family == key:
                    raise ValueError(
                        f"{BEAM_LAW}: {entry_label}.phase_window.reads names the entry's own family "
                        f"{key!r}: the window gates those rows and cannot be read from them"
                    )
                window_reads[names[key]] = (names[entry_window.family], entry_window.offset)
            rules[names[key]], reads[names[key]] = rule, component
            windows[names[key]] = entry_window if isinstance(entry_window, int) else None
        # The clock trigger of the transformation (`become` on the event).
        become = None
        if "become" in obj:
            become = _transformation(
                obj["become"],
                f"{label}.become",
                families,
                family,
                amount,
                table,
                directions,
                clock=True,
            )
        # The rule of a contact per family: the entry's rule where it
        # differs from the keys' own rule for the family, `measure` (the
        # keys' rule for a paid arrival, the body's momentum its own label)
        # where the entry is the keys' own, declared or not, and under a
        # `become` entry (the click's hand-over; no transformation fires
        # at a contact: a body is not a click of the entry's family).
        contact = [
            rule if rule not in (default_rule(family), BECOME_RULE) else CONTACT_DEFAULT
            for rule, family in zip(rules, families, strict=True)
        ]
        for held_family, content in enumerate(held):
            if content and families[held_family].free:
                # The label of a free release: amount x D along a heading,
                # of the event's own family and of every free family held.
                _label_bound(content * release[0] // release[1] or 1, 1, table, directions, label)
        lamp = None
        if "lamp" in obj:
            if families[family].free:
                raise ValueError(f"{BEAM_LAW}: {label}: a lamp is a measured event of a paid family")
            if families[family].charge[0]:
                raise ValueError(
                    f"{BEAM_LAW}: {label}: a lamp of the charged paid family {family_name!r} is "
                    "refused: its releases would create charge from nothing (a charged paid family "
                    "is born by a transformation or declared in transit; D-1, 2026-09-20)"
                )
            lamp = _lamp(
                obj["lamp"],
                f"{label}.lamp",
                phase_steps,
                phased,
                table,
                families[family].quantum,
                amount,
                turn_rate,
            )
        found.append(
            MeasuredDefinition(
                position,
                family,
                amount,
                phase,
                (momentum[0], momentum[1], momentum[2]),
                fixed,
                directions,
                tuple(rules),
                tuple(windows),
                tuple(reads),
                lamp,
                span,
                turning,
                tuple(held),
                tuple(contact),
                tuple(widths),
                become,
                tuple(transforms),
                tuple(window_reads),
            )
        )
    return tuple(found)


def event_charges(families: tuple[FamilyDefinition, ...], held: dict[int, int]) -> list[tuple[int, int]]:
    """A declared measured event's charge in every column from what it
    holds at the start (family index to content): per column the exact
    rational sum of the held families' values times their contents, the
    reduced pair (the parser's copy of the engine's reading of the same,
    `measured.column_charges`, for the static budget below)."""
    return [
        rational_sum(
            [
                (families[family].values[column][0] * content, families[family].values[column][1])
                for family, content in held.items()
                if content and families[family].values[column][0]
            ]
        )
        for column in range(len(families[0].columns))
    ]


def _column_budget(
    families: tuple[FamilyDefinition, ...],
    measured: tuple[MeasuredDefinition, ...],
    release: tuple[int, int],
) -> None:
    """The parser's static budget of the push over the columns (the
    mathematician's rule P3 of 2026-09-20 in the form the physicist's
    design states for the load-time check): for every declared measured
    event A, every free family g and every column c, the product of the
    reader's charge in the column with the family's value, |E_c n_c|,
    times the largest label flow per axis A can meet from one number's
    rays of g in one interval, V_g = Q x w_A x (the largest release of one
    self-creation of g by any event over its directions), must stay within
    2^62 - 1 (the run-time rule R1 tested at every push), and the sum over
    the columns of the whole parts, each at most |E_c n_c| V_g / (D_c d_c)
    + 1, within the same bound (R2), so that k terms each inside the
    budget sum inside it in any order. Static and conservative on the
    declared keys: a declared ray in transit, a merged or re-emitted row
    and a content grown by clicks are beyond it and are refused at the
    push they would overflow (`nature_beam.push_form`). Refused naming the
    measured event, the family, the column and the numbers."""
    numerator, denominator = release
    count = len(families)
    # Per family and per measured event, the largest release of one
    # self-creation over its directions (a reader never reads its own
    # rays: the largest over the other events).
    releases: list[list[int]] = [[0] * len(measured) for _ in range(count)]
    for index, entry in enumerate(measured):
        for family, content in _held_of(entry).items():
            if not families[family].free or not content:
                continue
            product = content * numerator
            per_direction = product // denominator + (1 if product % denominator else 0)
            releases[family][index] = per_direction * len(entry.directions)
    columns = families[0].columns
    for index, entry in enumerate(measured):
        width = entry.span[0] * entry.span[1] * entry.span[2]
        charges = event_charges(families, _held_of(entry))
        for family in range(count):
            largest = max((r for k, r in enumerate(releases[family]) if k != index), default=0)
            if not families[family].free or not largest:
                continue
            moment = LABEL_SCALE * width * largest
            total = 0
            for c, (column, (charge, charge_denominator)) in enumerate(
                zip(columns, charges, strict=True)
            ):
                value, value_denominator = families[family].values[c]
                if not charge or not value:
                    continue
                if abs(value) * moment > MOMENTUM_BOUND or abs(charge) > MOMENTUM_BOUND // (
                    abs(value) * moment
                ):
                    raise ValueError(
                        f"{BEAM_LAW}: measured[{index}]: the push over the column {column.name!r} "
                        f"from the rays of the family {families[family].name!r} could reach "
                        f"|E n| x V = |{charge} x {value}| x {moment} beyond the integer bound "
                        f"{MOMENTUM_BOUND} (E/D the reader's charge in the column, n/d the family's "
                        f"value per unit of content, V = {LABEL_SCALE} x {width} x {largest} the "
                        "largest label flow of one self-creation's release read over the "
                        "reader's Nodes)"
                    )
                total += (
                    abs(charge) * abs(value) * moment // (charge_denominator * value_denominator) + 1
                )
            if total > MOMENTUM_BOUND:
                raise ValueError(
                    f"{BEAM_LAW}: measured[{index}]: the pushes over the {len(columns)} columns from "
                    f"the rays of the family {families[family].name!r} could sum to {total} beyond "
                    f"the integer bound {MOMENTUM_BOUND} (each column's whole part within the bound, "
                    "their sum not)"
                )


def _held_of(entry: MeasuredDefinition) -> dict[int, int]:
    """The content a declared measured event holds per family at the start."""
    return {family: content for family, content in enumerate(entry.held) if content}


def _in_transit(
    value: object,
    shape: Address3,
    families: tuple[FamilyDefinition, ...],
    measured: tuple[MeasuredDefinition, ...],
    phase_steps: int,
    table: tuple[Vector, ...],
    age_bound: int,
) -> tuple[TransitDefinition, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{BEAM_LAW}: in_transit must be a list")
    names = {family.name: index for index, family in enumerate(families)}
    found: list[TransitDefinition] = []
    for index, entry in enumerate(value):
        label = f"in_transit[{index}]"
        obj = _object(
            entry, label, TRANSIT_KEYS, {"position", "family", "number", "direction", "amount"}
        )
        family_name = obj["family"]
        if not isinstance(family_name, str) or family_name not in names:
            raise ValueError(f"{BEAM_LAW}: {label}.family names an unknown family")
        family = names[family_name]
        top = phase_steps - 1 if families[family].phase else 0
        direction = _direction(obj["direction"], f"{label}.direction", table, rest=True)
        amount = _integer(obj["amount"], f"{label}.amount", 1)
        age = _integer(obj.get("age", 0), f"{label}.age", 0, age_bound)
        lifetime = families[family].lifetime
        if lifetime is not None and age >= lifetime:
            raise ValueError(
                f"{BEAM_LAW}: {label}.age {age} is at or beyond the lifetime {lifetime} of the "
                f"family {family_name!r}: the event would have clicked on the border already"
            )
        # A declared ray of a paid family carries one phase step of content
        # per unit, quantum x 1 (no emitter declared its turn); a free one
        # carries none and its label is the amount along the direction.
        _label_bound(amount, families[family].unit_label, table, (direction,), label)
        found.append(
            TransitDefinition(
                _address(obj["position"], f"{label}.position", shape),
                family,
                _integer(obj["number"], f"{label}.number", 1, max(1, len(measured))),
                direction,
                amount,
                _integer(obj.get("phase", 0), f"{label}.phase", 0, top),
                age,
            )
        )
    return tuple(found)


def _detectors(
    value: object,
    shape: Address3,
    periodic: tuple[bool, bool, bool],
    measured: tuple[MeasuredDefinition, ...],
) -> tuple[DetectorDefinition, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{BEAM_LAW}: detectors must be a list")
    at = {entry.position for entry in measured}
    # The other Nodes of the bodies on a set: a body is named by its centre.
    inside: set[Address3] = set()
    for entry in measured:
        inside.update(body_nodes(entry.position, entry.span, shape, periodic) or ())
    taken: set[Address3] = set()
    found: list[DetectorDefinition] = []
    for index, entry in enumerate(value):
        label = f"detectors[{index}]"
        obj = _object(entry, label, DETECTOR_KEYS, {"name", "positions"})
        name = obj["name"]
        if not isinstance(name, str) or not name:
            raise ValueError(f"{BEAM_LAW}: {label}.name must be a nonempty string")
        if any(item.name == name for item in found):
            raise ValueError(f"{BEAM_LAW}: two detectors named {name!r}")
        if name in FACE_NAMES:
            raise ValueError(
                f"{BEAM_LAW}: {label}.name {name!r} is the name of a face detector (an open face "
                "of the GameBoard is a detector of that name; declare another)"
            )
        if name == LIFETIME_NAME:
            raise ValueError(
                f"{BEAM_LAW}: {label}.name {name!r} is the name of the border every event of a "
                "family with a lifetime clicks on; declare another"
            )
        positions_value = obj["positions"]
        if not isinstance(positions_value, list) or not positions_value:
            raise ValueError(f"{BEAM_LAW}: {label}.positions must be a nonempty list of Nodes")
        positions = []
        for item in positions_value:
            position = _address(item, f"{label}.positions", shape)
            if position not in at:
                if position in inside:
                    raise ValueError(
                        f"{BEAM_LAW}: {label}.positions names a Node of a body on a set "
                        f"{list(position)} that is not its position (a body is one record, "
                        "named by its centre)"
                    )
                raise ValueError(
                    f"{BEAM_LAW}: {label}.positions names a Node without a measured event {list(position)}"
                )
            if position in taken:
                raise ValueError(f"{BEAM_LAW}: a Node in two detectors {list(position)}")
            taken.add(position)
            positions.append(position)
        threshold = _integer(obj.get("threshold", 1), f"{label}.threshold", 1)
        reading = obj.get("reading", DETECTOR_READINGS[0])
        if reading not in DETECTOR_READINGS:
            raise ValueError(
                f"{BEAM_LAW}: {label}.reading must be one of {list(DETECTOR_READINGS)}, not {reading!r}"
            )
        found.append(DetectorDefinition(name, tuple(positions), threshold, str(reading)))
    return tuple(found)


def parse_nature_beam_world(document: object) -> NatureBeamWorld:
    """Reject anything but a lawful world of the Beam Law."""
    if not isinstance(document, dict):
        raise ValueError(f"{BEAM_LAW}: a world is a JSON object")
    old = [key for key in OLD_KEYS if key in document]
    if old:
        raise ValueError(
            f"{BEAM_LAW}: a world of the Beam Law declares none of the earlier engines' "
            f"keys ({', '.join(old)}); see docs/MIGRATION.md"
        )
    if document.get("law") == "events":
        raise ValueError(
            f'{BEAM_LAW}: "law": "events" names the law of events (events-v1), deleted on '
            '2026-09-19; a world of the Beam Law declares "law": "beam" (docs/MIGRATION.md)'
        )
    if document.get("law") == OLD_LAW_VALUE:
        raise ValueError(
            f'{BEAM_LAW}: "law": "rays" is the Beam Law\'s name before 2026-09-20 (rays-v1 is '
            'beam-v1, the same law); a world declares "law": "beam": rewrite it with '
            'tools/migrate_nature_beam_worlds.py (docs/MIGRATION.md, "The names NatureBeam and '
            "GameBoard and the glossary's single names, on 2026-09-20\")"
        )
    if document.get("law") != LAW_VALUE:
        raise ValueError(f'{BEAM_LAW}: a world of the Beam Law declares "law": "beam"')
    events = [key for key in EVENTS_KEYS if key in document]
    if events:
        raise ValueError(
            f"{BEAM_LAW}: a world of the Beam Law declares none of the law of events' keys "
            f"({', '.join(events)}); see docs/MIGRATION.md"
        )
    obj = _object(
        document,
        "the world",
        WORLD_KEYS,
        {"law", "model_id", "shape", "ticks", "K", "release", "families", "measured"},
    )
    model_id = obj["model_id"]
    if not isinstance(model_id, str) or not model_id:
        raise ValueError(f"{BEAM_LAW}: model_id must be a nonempty string")
    shape_value = obj["shape"]
    if not isinstance(shape_value, list) or len(shape_value) != 3:
        raise ValueError(f"{BEAM_LAW}: shape must be three positive extents")
    extents = tuple(_integer(item, "shape", 1, 4096) for item in shape_value)
    shape: Address3 = (extents[0], extents[1], extents[2])
    boundary, periodic = _boundary(obj.get("boundary", BOUNDARIES[0]))
    ticks = _integer(obj["ticks"], "ticks", 0)
    # The clock's rate: an integer K is the pair [1, K] (one phase step per
    # K units of content per self-creation), a pair [n, d] is n phase steps
    # per d units of content per self-creation, like `release`; the record
    # carries the key as declared.
    declared_clock = obj["K"]
    K: int | tuple[int, int]
    if type(declared_clock) is int:
        K = _integer(declared_clock, "K", 1)
        turn_rate = (1, K)
    else:
        turn_rate = _ratio(declared_clock, "K", zero=False)
        K = turn_rate
    phase_steps = _integer(obj.get("N", 64), "N", 2, MAX_PHASE_STEPS)
    if phase_steps & (phase_steps - 1):
        raise ValueError(f"{BEAM_LAW}: N must be a power of two from 2 through {MAX_PHASE_STEPS}")
    release = _ratio(obj["release"], "release", zero=True)
    suspension = _ratio(obj.get("suspension", 1), "suspension", zero=True)
    if suspension[0] == 0:
        # Off: 0 and [0, d] alike, recorded as [0, 1].
        suspension = (0, 1)
    # The width S of the push: one Link per (S x M + p) / p self-creations;
    # 1 (the rule as it was) unless the world declares it, never below 1.
    width = _integer(obj.get("width", 1), "width", 1)
    bound = _integer(obj.get("direction_bound", DEFAULT_DIRECTION_BOUND), "direction_bound", 1, 4096)
    table = _direction_table(obj.get("directions", []), bound)
    age_bound = _age_bound(obj.get("age_bound"), shape, periodic, table)
    # The quantum of action of the turn by momentum, h: absent by default
    # (nothing turns by momentum), an integer from 1 when declared.
    action = None if "action" not in obj else _integer(obj["action"], "action", 1)
    families = _families(obj["families"], phase_steps, age_bound)
    measured = _measured(
        obj["measured"],
        shape,
        periodic,
        families,
        turn_rate,
        phase_steps,
        release,
        table,
        ticks,
        action,
    )
    _column_budget(families, measured, release)
    in_transit = _in_transit(
        obj.get("in_transit", []), shape, families, measured, phase_steps, table, age_bound
    )
    detectors = _detectors(obj.get("detectors", []), shape, periodic, measured)
    world = NatureBeamWorld(
        model_id,
        shape,
        boundary,
        periodic,
        ticks,
        K,
        turn_rate,
        phase_steps,
        release,
        suspension,
        width,
        age_bound,
        table,
        bound,
        families,
        measured,
        in_transit,
        detectors,
        action,
    )
    return world
