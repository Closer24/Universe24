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
  everything", item (2); BEAM_LAW note 36 (ii)): an integer c, a pair
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
  and, for a measured event of a paid family, its `lamp` (`wheel` `[r, W]`, the
  birth wheel's rate, required: u = ordinal x r mod W the record's coordinate on
  the ladder, [1, N] the count of births mod N, BEAM_LAW note 46; `rate` `[n, d]` units
  per self-creation per direction, `directions` the directions it releases
  on, the six headings by default, and optionally its `phase_window`); and,
  since 2026-09-20 (the weak force, `weak-v1`: the model owner's "go on
  everything", item (1), the transformation `become`; the physicist's
  design, WEAK.md section 2; BEAM_LAW note 36 (iii)), its `become`, the
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
  BEAM_LAW note 36) its width `phase_width`, an integer w from 1 through N,
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
along the unit vector of its direction at the flight's scale, the
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

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass, replace
from functools import cached_property

from event_universe.core.game_board import MAX_VALUE, PORT_HEADINGS, Address3
from event_universe.core.integer import (
    MAX_WORK_INT,
    bounded_gcd,
    by_clock,
    integer_root,
    rational_sum,
)
from event_universe.core.phase import MAX_PHASE_STEPS

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
# external thing). Since clock-age-v1 (the model owner's word of
# 2026-09-21, record 394) the clock counts the age moment by default on
# every entry; the word `presence` selects the presence for the clock (its
# record then carries the presence, the zeroth moment, as `scalar` does).
AGE_READS = "age"
PRESENCE_WORD = "presence"
READS = ("scalar", "outside", "here", "vector", "tensor", AGE_READS, PRESENCE_WORD)
# The one scale Q of the law (BEAM_LAW sections 2 and 3): the time resolution
# of the flight, where the turn of a direction is T_d = isqrt(3 |v|^2
# Q^2) and a ray makes S_1 Manhattan steps per T_d / Q intervals in the mean,
# and the length of the momentum label, `LABEL_SCALE` below.
Q = 64
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
    "meeting",
    "massive_rows",
    # The covariant readings (`covariant-readings-v1`, 2026-09-21): one
    # object, absent by default (`COVARIANT_KEYS`).
    "covariant_readings",
    # optical-v1 (2026-09-21): the world's post-Newtonian parameter gamma,
    # a non-negative integer, absent by default (`OPTICAL_RULE`).
    "optical",
    # drive-b-v1 (2026-09-22): the directional drive of a body, a boolean,
    # false by default (`DRIVE_B_RULE`).
    "drive_b",
    "atom_level",
    # centred-step-v1 (2026-09-22): the body's step at half the wall, a
    # boolean, false by default (`CENTRED_STEP_RULE`).
    "centred_step",
    "directions",
    "direction_bound",
    "families",
    "measured",
    "in_transit",
    "detectors",
}
# The identity of the amplitude law (`amplitude-v1`; the model owner,
# 2026-09-20, Highlights 5.4, "DECIDED: `amplitude-v1` is built"; the
# physicist's and the mathematician's design, docs/designs/amplitude-v1/DESIGN.md;
# docs/BEAM_LAW.md note 37): in a recorded world (a lamp declared) an event in
# transit is a record with rows (the store's columns `record`, `branch` and
# `multiplicity`), a re-emission may split a row by integer weights, rows of
# one record in antiphase cancel at the merge, and the click's reading `sum`
# accumulates one record's rows at a set for the ladder of the apparatus's
# layer. Absent (false by default), no row carries a record and every world
# reads as it did, byte for byte.
AMPLITUDE_RULE = "amplitude-v1"
# The world key `amplitude` of stages (i) to (vii-3), deleted at stage
# (vii) step 4 (the one click): the record form is the law; a world that
# declares it is refused naming MIGRATION.
DELETED_AMPLITUDE_KEY = "amplitude"
# The circle must hold the quarter turn of a reflection in a recorded world
# (`phase` + N / 4 exact on the tables): N below 4 is refused with it.
AMPLITUDE_LEAST_STEPS = 4
# The world key `doppler` of the reading's weight at the relative speed
# (`doppler-v1`, 2026-09-20, BEAM_LAW note 38 as it was), deleted on
# 2026-09-21 with the crossing rule (the model owner's record 158 of
# 2026-09-20; note 48): a moving body's Doppler is the count of the rows
# it crosses, no weight. A world that declares the key is refused as an
# unknown key (MIGRATION).


def step_divisor(momentum: int, content: int, width: int, cap: bool = True) -> int:
    """D_a = Q x S x M + |p_a|, the divisor of the step rule on one axis
    (BEAM_LAW section 3 step 5 and note 17: one Link per D_a / |p_a|
    self-creations; `engine.step_axis` reads it), the denominator of the
    body's speed |p_a| / D_a in Links per interval: M the content, S the
    world's `width`, Q the label's scale. Under `covariant-readings-v1`
    (`cap` false; DERIVATIONS_BEAM 17.6 M1 and M8) the wall's second term
    |p_a| is keyed off and the divisor is Q x S x M alone: the drive's rate
    per self-creation is Newton's p_a / (Q S M), and with the self-creations
    gated by the proper-time count the pace per lattice interval is
    p / E' (the one primitive with one term selected off, not a copy)."""
    return LABEL_SCALE * width * content + (abs(momentum) if cap else 0)


# The flight table's resolution on a heading, T_h = isqrt(3 Q^2) = 110: the one
# root of `drive-b-v1`, formed at load as the flight table's is, never at run
# time (docs/designs/drive_b/DESIGN.md section 2).
T_HEADING = integer_root(3 * LABEL_SCALE * LABEL_SCALE)
# The identity of the directional drive (the model owner's approval of form B,
# 2026-09-22, record 652 of the log of 2026-09-20; docs/designs/drive_b/DESIGN.md;
# light_speed/FORM.md section 3.1 (c)): under the world key `drive_b` a body's
# three drive accumulators gain p_a Q each against ONE wall, Q^2 S M + |p|_1 T_h,
# and the axis furthest over the wall steps (`core.integer.by_line`), the
# Bresenham line of the momentum with no coincident fire lost. Absent, the
# per-axis drive of BEAM_LAW note 17 runs unchanged, byte for byte.
DRIVE_B_RULE = "drive-b-v1"
# The identity of the centred step (the model owner's word through the Boss,
# 2026-09-22, record 953 of the log of 2026-09-20; the cause of the atom's
# widening, docs/designs/atom_give/CAUSE.md section 2 (v); the design
# docs/designs/atom_give/CENTRED_STEP.md): under the world key `centred_step`
# the count of a body's step is the NEAREST whole number of its accumulator in
# units of the wall, on both drives (`core.integer.by_drive` and `by_line`,
# `centred`), so a step fires when the accumulated motion passes half a Link
# beyond the Node and the whole wall is subtracted: the body's Node the
# nearest to its accumulated motion, the lag of the Node behind the motion
# (half a Link per axis in the mean, which turns the push read at the Node
# along the motion) zero in the mean. Every other count keeps the whole
# part. Absent, every registered world replays byte for byte.
CENTRED_STEP_RULE = "centred-step-v1"
# The identity of the atom's levels (`atom-level-v1`, 2026-09-22; the model
# owner's word of record 973 through the Boss; docs/designs/atom_levels/
# LEVELS.md section 2 (b), the virial form on the physics-rule reviewer's
# recommendation): under the world key `atom_level` a body that declares
# `level` carries, beside its action rows, the action gained on each axis
# since its last return (DESIGN.md's give rows without the modulus), the
# count of its self-creations since that return and the level at its last
# release; at a return (the momentum's declared component crossing zero in
# the declared sense) its level is the whole part of n_l x (the action
# gained) over 2 h d_l x (the count), and the rise of that level above the
# last released one is released as one row per declared direction of the
# declared paid family, content h_q x (the rise), the row's phase turning
# that many steps per interval of its age (the Planck identity as a rule of
# the row). Absent by default: every registered world byte for byte.
ATOM_LEVEL_RULE = "atom-level-v1"


def drive_wall(momentum: Sequence[int], content: int, width: int, cap: bool = True) -> int:
    """W = Q^2 x S x M + |p|_1 x T_h, the one wall of the directional drive
    (`drive-b-v1`, docs/designs/drive_b/DESIGN.md section 2; light_speed/FORM.md
    3.1 (c)): M the content, S the world's `width`, Q the label's scale,
    |p|_1 the Manhattan norm of the momentum and T_h = isqrt(3 Q^2) = 110
    the flight table's heading resolution; the rate per axis is p_a Q, so
    the Manhattan pace is |p|_1 Q / W Links per interval (on a heading form
    B's |p| x 64 / (Q S M x 64 + 110 |p|); at a small momentum Newton's
    |p|_2 / (Q S M); never above the rows' 64 / 110). Under
    `covariant-readings-v1` (`cap` false) the cap term is keyed off and the
    wall is Q^2 S M alone, the pace p_a / (Q S M) per self-creation (the one
    primitive with one term selected off, as `step_divisor`). The two
    products are tested by division against the integer bound before they
    are formed; a wall past it refuses the run naming the rule."""
    manhattan = sum(abs(component) for component in momentum)
    scale = LABEL_SCALE * LABEL_SCALE * width
    if content > MOMENTUM_BOUND // scale:
        raise OverflowError(
            f"{BEAM_LAW}: {DRIVE_B_RULE}: the wall's rest term Q^2 S M = {scale} x {content} exceeds "
            f"the integer bound {MOMENTUM_BOUND}"
        )
    rest = scale * content
    if not cap:
        return rest
    if manhattan > MOMENTUM_BOUND // T_HEADING or rest > MOMENTUM_BOUND - manhattan * T_HEADING:
        raise OverflowError(
            f"{BEAM_LAW}: {DRIVE_B_RULE}: the wall Q^2 S M + |p|_1 T_h = {rest} + {manhattan} x "
            f"{T_HEADING} exceeds the integer bound {MOMENTUM_BOUND}"
        )
    return rest + manhattan * T_HEADING


def body_weight(momentum: Sequence[int], content: int, width: int, gamma: int) -> tuple[int, int]:
    """The gravity charge of a moving body under `optical` and `drive_b`
    together (every family under one wall, step 3, 2026-09-22;
    docs/designs/one_wall/BODY_DRIVE.md): the pair (w, Q S) with w = (E'^2
    + 3 gamma p . p) // E' and E' = isqrt((Q S M)^2 + 3 p . p), the rows'
    weight per unit (`nature_beam.unit_weights`) on the body's own
    momentum, over the label scale Q S at which the body's rest energy is
    Q S M: at rest the pair is (Q S M, Q S), the content M over 1 exactly
    (today's push, integer for integer); moving, gamma_L (1 + gamma v^2)
    times it, with gamma_L = E' / (Q S M) the Lorentz factor and v^2 =
    3 p . p / E'^2 (the one-wall note's section 4, the drive's integer
    form). The square is tested against the working bound by division
    before its terms are formed (the wall's square of `momentum_pair`)
    and refused naming the rule; a body of no content weighs (0, 1)."""
    if content <= 0:
        return 0, 1
    scale = LABEL_SCALE * width
    rest = scale * content
    if rest > MAX_WORK_INT // rest:
        raise OverflowError(
            f"{BEAM_LAW}: {OPTICAL_RULE}: the body's rest energy Q S M = {rest} squared exceeds "
            f"the working bound {MAX_WORK_INT} (the weight of a moving body under optical)"
        )
    square = rest * rest
    for component in momentum:
        c = abs(int(component))
        if c and c > ((MAX_WORK_INT - square) // 3) // c:
            raise OverflowError(
                f"{BEAM_LAW}: {OPTICAL_RULE}: the body's energy square (Q S M)^2 + 3 p . p with "
                f"p = {list(momentum)} exceeds the working bound {MAX_WORK_INT}"
            )
        square += 3 * c * c
    energy = integer_root(square)
    pushed = 3 * gamma * sum(int(c) * int(c) for c in momentum)
    return (energy * energy + pushed) // energy, scale


# The identity of the covariant readings, a hypothesis beside the law (the
# model owner's decision of 2026-09-21, record 270 of the log of 2026-09-20;
# DERIVATIONS_BEAM section 17 as amended in 17.6 per the physics-rule
# reviews, records 297 and 314): under the world key `covariant_readings`
# every measured event carries its energy readings (the exact square
# W = E'_0^2 + d p . p at the declared c^2 = [1, d], E'_0 = Q S M, and E'
# the largest integer with E'^2 <= W, kept by comparisons), its
# self-creations are gated by a second owed count (one self-creation per
# E' / E'_0 intervals in the mean), the drive's wall loses its cap term and
# the release runs per lattice interval. Absent, nothing of it is computed
# and every world reads as it did, byte for byte.
COVARIANT_READINGS_RULE = "covariant-readings-v1"
COVARIANT_KEYS = {"c2", "grain", "books"}


@dataclass(frozen=True)
class CovariantDeclaration:
    """The world key `covariant_readings` as declared (`covariant-readings-v1`,
    DERIVATIONS_BEAM 17.6): `c2` the pair of c^2, [1, d] (the design's
    [1, 3]: c = 1 / sqrt 3 Links per interval in the limit), so that the
    exact square is `W = E'_0^2 + d p . p` with `E'_0 = Q S M` whole;
    `grain` g, a power of two dividing Q S, the unit the readings are
    carried in (`E'_0 / g`, the momentum's whole part over g, `W / g^2`:
    the bits of the momentum below g do not enter E', the drive keeps the
    full momentum); `books` whether the world declares the exchange's
    accounting, under which a paid family off the identity `d h n = Q S d_K`
    (h the family's quantum, [n, d_K] the clock's rate) is refused at load
    (17.6 N5); and `off_identity`, the paid families off it with their gap
    `d h n - Q S d_K`, a diagnostic line of the record."""

    c2: tuple[int, int]
    grain: int
    books: bool
    off_identity: tuple[tuple[str, int], ...]

    @property
    def square_factor(self) -> int:
        """d of the pair [1, d]: the factor of p . p in W."""
        return self.c2[1]


def scaled_label(vector: Vector, scale: int) -> Vector:
    """The integer vector nearest `scale x D / |D|`, in integers only: the
    physics-rule reviewer's exact rule of 2026-09-19 for the unit vector at
    the scale Q (`nature_beam.unit_label`, this function at the scale Q),
    with n = |D|^2, each component |a| rounded as k(|a|) = (isqrt((2 scale
    |a|)^2 // n) + 1) // 2 and the sign restored, so that the label of -D
    is minus the label of D exactly and the 48 signed axis permutations
    carry over (k depends on |a| and n alone). The zero vector gives the
    zero vector. The massive rows (`massive-rows-v1`) form their momentum
    label p_D per direction here at the scale p (the lamp's
    `momentum_magnitude`), one load-time rounding per direction in the
    class of u_D's; a scale of 0 gives the zero vector on every direction
    (a row at rest, the primitive's p = 0 case)."""
    n = sum(c * c for c in vector)
    if n == 0 or scale == 0:
        return (0, 0, 0)
    found = []
    for a in vector:
        t = 2 * scale * abs(a)
        k = (integer_root(t * t // n) + 1) // 2
        found.append(k if a >= 0 else -k)
    return found[0], found[1], found[2]


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
# The identity of the meeting (the model owner, 2026-09-20, "DECIDED: the
# meeting, M-R": an event in transit reads the crowd as a body does, a
# report; `events/meeting.py`): the record carries it when the world
# declares `meeting: true`; absent, no paid unit reads the crowd and every
# world reads as it did, byte for byte.
MEETING_RULE = "meeting-v1"
# The identity of the rows' rule at a Node for general relativity's formulas
# (the model owner's "go" of 2026-09-21, record 303, in its generic form,
# records 421 to 428 and REVIEW_3; docs/designs/one_wall/NOTE.md): under the
# world key `optical: gamma` (gamma the post-Newtonian parameter, a
# non-negative integer, nature's 1) the row's flight joins the age wall's
# declared set at the coefficient f = 1 + gamma (`measured.age_wall_set`),
# and every row of content in free space is pushed by the crowd's flow with
# the weight (1 + gamma) x content x e_D and turns to the fan's direction
# nearest its whole momentum (`nature_beam.optical_turn`). Absent, nothing
# of it exists and every world reads as it did, byte for byte.
OPTICAL_RULE = "optical-v1"
# The identity of the hand (`hand-v1`; the model owner, 2026-09-20, record
# 128 of docs/LOG_2026-09-20.md, "the hand's three choices confirmed"; the
# physicist's design hand/DESIGN.md with the mathematician's FORM.md; BEAM_LAW
# note 39): the record carries it when a family, a lamp, a transit row or a
# table entry declares `hand`, a lamp's `branches` name the hands of their
# labels, or a measured event declares an `axis`. Absent, no row carries a
# hand and every world reads as it did, byte for byte.
HAND_RULE = "hand-v1"
# The two hands of a row, its helicity relative to its own direction: +1 a
# right-handed screw along u_d, -1 a left-handed one; 0 no hand, every row
# of every world without a declaration.
HANDS = (-1, 1)
NO_HAND = 0
# The identity of the binding that costs content (`binding-v1`, the model
# owner's record 115 of 2026-09-20, the physicist's design
# docs/designs/binding_v1/DESIGN.md; BEAM_LAW note 40): at a contact under
# `measure` the refused body gives the paid content it carries (`held` of a
# paid family other than its own) to the flight on the heading opposite to
# the refused step (`engine._give`). The record carries it when a measured
# event holds a paid family at load, or from the first give of a run (the
# engine's fact); no registered world does either, and every world without
# one reads as it did, byte for byte.
BINDING_RULE = "binding-v1"
# The identity of the massive rows (`massive-rows-v1`; the model owner's yes
# of 2026-09-21, record 332 of docs/LOG_2026-09-20.md; the mathematician's
# design docs/designs/massive_rows/DESIGN.md, the physics-rule review's
# three rounds): under the world key `massive_rows` a paid family may be
# declared `massive`, its rows flying at the pace |p| / E' of the rest
# energy E'_0 = Q S M (M the family's `quantum`, S the world's `width`)
# and the momentum label p_D per direction at the scale p (the lamp's
# `momentum_magnitude`), turning de Broglie's |p_a| N / h at every axis
# Link over the world's `action` h, and completing by handing ONE quantum
# (M and the one label) to the chosen set at the record's completion (the
# placed fraction f_F = 0, the completion's quantum q_F = M). Every family
# carries the same tables by value (a family without the flag Flight's
# numbers, (phase_per_link, 1) and the pair (1, 0)), so a world without the
# key reads as it did, byte for byte. Absent (false by default), no family
# may be declared massive.
MASSIVE_ROWS_RULE = "massive-rows-v1"
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
FAMILY_KEYS = {
    "name",
    "quantum",
    "charge",
    "columns",
    "lifetime",
    "phase",
    "phase_per_link",
    "hand",
    "massive",
}
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
    "level",
    "directions",
    "table",
    "lamp",
    "become",
    # The axial record (`hand-v1`): one of the six headings, the axis the
    # right-hand rule reads at every product of the event's `become`.
    "axis",
    # The energy E' a thrown body declares under `covariant_readings`
    # (`covariant-readings-v1`; refused without the world key).
    "E",
}
LAMP_KEYS = {
    "rate",
    "wheel",
    "directions",
    "phase_window",
    "phase_width",
    "turns",
    "branches",
    "arms",
    "hand",
    "momentum_magnitude",
}
# A table entry's object form: the rule, a window on any rule but `pass`
# with its width, the reading's component the record carries, on a
# `become` entry the transformation's `into` and `products`, and the parity
# filter `hand` (`hand-v1`: the entry's rule applies to arrivals of that
# hand only; refused on `pass`).
TABLE_ENTRY_KEYS = {
    "rule",
    "phase_window",
    "phase_width",
    "reads",
    "into",
    "products",
    "inputs",
    "weights",
    "turn",
    "rotate",
    "gate",
    "turns",
    "hand",
}
# The split (the amplitude law, 2026-09-20, the owner's unification (2):
# the split is `rerelease` with a vector of integer weights and the
# multiplicity, one rule): on a `rerelease` entry, `weights`
# (one integer from 0 per declared direction of the measured event, at
# least one positive) and `turns` (a phase step per direction, 0 by
# default): an arriving row (w, m, p) is re-emitted as the rows (w a_i,
# m x A, p + t_i) with A = sum a_i^2; without `weights` every weight is 1,
# the equal k-way split. Refused on a rule other than
# `rerelease` and on a free family's entry (free families never branch).
SPLIT_KEYS = ("inputs", "weights", "turns")
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
TRANSIT_KEYS = {"position", "family", "number", "direction", "amount", "phase", "age", "hand"}
DETECTOR_KEYS = {"name", "positions", "threshold", "reading"}
# The readings a detector may declare; the first is the default: `wave`
# since 2026-09-20 (the model owner: "on the GameBoard a ray, in the world a
# wave"; `beam` was the default from 2026-09-19 to 2026-09-20).
DETECTOR_READINGS = ("wave", "beam")
# The third reading, of a record's rows (the design, section
# 0): the set reads the sum of the rows of one record and one label that
# arrived at its Nodes, squared, accumulated over the record's lifetime;
# the crowd's pointer gives the set's phase as under `wave`, and a window
# on its entry is the rotation of the record's labels, not a gate.
SUM_READING = "sum"
# The keys of the deleted `reversible-detector-v1`, refused by name.
REVERSIBLE_KEYS = ("port_map", "output", "capacity", "groups", "reference_phase")
# The face detectors, one per open face of the GameBoard, named by the face in
# Port order (an open face is a detector, the model owner, 2026-09-19); a
# declared detector may not take one of these names.
FACE_NAMES = ("face:+x", "face:-x", "face:+y", "face:-y", "face:+z", "face:-z")
# The layer's name of a measured event's set outside every declared
# detector, `measured:<number>`; a declared detector's name may not use
# the prefix, so that no name collides.
RESERVED_SET_PREFIX = "measured:"
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
    # The pair form of `phase_per_link` (the amplitude law, 2026-09-20, the
    # owner's unification (1): the design's frequency is `phase_per_link`
    # with a rational pair [n, d]): the phase steps a row of the family
    # turns per interval of its age, `by_clock(age, n, d)` at every walk
    # that advances its age, carried through a re-emission; None without.
    # The integer form turns per Link crossed, as it did.
    phase_per_age: tuple[int, int] | None = None
    # The hand of the family (`hand-v1`, 2026-09-20; BEAM_LAW note 39): -1
    # or +1 for a chiral family, whose every row (a lamp's, a free
    # release's, a product's, a home's, a declared transit row's) carries
    # it, the helicity relative to the row's direction (the neutrino -1);
    # 0 for a family without one, every family until then. Declared on the
    # family as `charge` is: the neutrino is left-handed once, not per
    # world.
    hand: int = NO_HAND
    # The massive rows (`massive-rows-v1`, 2026-09-21; the family key
    # `massive`, admitted under the world key `massive_rows` alone): a paid
    # family whose rows are records of massive rows, flying at the pace
    # |p| / E' with the rest energy E'_0 = Q S M (M the `quantum`) and the
    # momentum label p_D at the scale `momentum_magnitude` (the lamp's key,
    # one value per family, resolved by the parser from the family's lamps),
    # turning de Broglie's |p_a| N / h per axis Link; its click hands one
    # quantum at the record's completion. False for every family until then.
    massive: bool = False
    momentum_magnitude: int = 0

    @property
    def declared_phase_per_link(self) -> int | list[int]:
        """The key as the record carries it: the integer, or the pair."""
        return list(self.phase_per_age) if self.phase_per_age is not None else self.phase_per_link

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
    # The birth wheel (`wheel`, [r, W]; the model owner's decision of
    # 2026-09-21, record 180 of the log of 2026-09-20; BEAM_LAW note 46):
    # the rate of one row of the lamp's counts table, advanced by r over W
    # at every birth, whose accumulator before the advance is the record's
    # coordinate u on the ladder, u = ordinal x r mod W; the rungs of the
    # click are on W. [1, N] is the lamp's count of births mod N as built;
    # declared on every lamp, no default.
    wheel: tuple[int, int]
    directions: tuple[int, ...]
    window: int | None
    # The window's width in steps (`phase_width`), None for the default
    # N / 2, the half circle.
    width: int | None = None
    # The phase step each direction's row is born with beyond the clock's
    # phase (`turns`, the amplitude law: the reflection's quarter turn at
    # the source's splitter), 0 each by default.
    turns: tuple[int, ...] = ()
    # The joint labels of a birth with their integer weights (`branches`,
    # the amplitude law's pair: [[0, 1], [3, 1]] the Bell pair on two
    # arms, the bit k of a label the label on arm k) and `arms`, the count
    # of directions that are separate quanta (1 by default: the directions
    # are paths of one quantum; the directions are shared equally by the
    # arms, in order).
    branches: tuple[tuple[int, int], ...] = ((0, 1),)
    arms: int = 1
    # The hand of the lamp's rows (`hand-v1`): a circularly polarised lamp
    # of a family without a hand, -1 or +1; a lamp of a chiral family may
    # repeat the family's value only; 0 means the family's (none, or its
    # own). `label_hands`, the meaning of a label bit on a branched family
    # (the third entry of each branch): the hand of the bit value 0 and of
    # the bit value 1, opposite; None where the branches name none. A row of
    # such a record carries its hand in its label, not in the `hand`
    # column, and its family may declare one or the other, never both.
    hand: int = NO_HAND
    label_hands: tuple[int, int] | None = None
    # The magnitude p of the momentum label of a massive family's rows
    # (`massive-rows-v1`; a scalar in label units, named by its kind:
    # `momentum` on a measured event is a vector): required on a lamp of a
    # massive family, refused on any other lamp; None without.
    momentum_magnitude: int | None = None


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
class LevelDeclaration:
    """A body's `level` under `atom-level-v1` (docs/designs/atom_levels/
    LEVELS.md section 2 (c)): `family` the paid family of the released
    rows (its quantum h_q the content per step), `pair` the rule's grain
    [n_l, d_l] (the released family's Planck constant in units of the
    world's action, h d_l / (N n_l) per phase step; [1, 1] the
    dictionary's own), `axis` the axis of the return and `sign` the sign
    the momentum's component crosses TO at a return (DESIGN.md section 1
    (b): once per loop on any loop that circles a centre, never on a
    straight flight)."""

    family: int
    pair: tuple[int, int]
    axis: int
    sign: int


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
    # The split per family (the amplitude law, `Split`): None where the
    # entry declares none (an equal split of a record's row, the apportioning
    # without it).
    splits: tuple[Split | None, ...] = ()
    # The turn of each entry's rotation on a `sum` set (`turn`, the label
    # click; 0 where none is declared), per family.
    label_turns: tuple[int, ...] = ()
    # The label rotation and the gate of a `rerelease` entry per family
    # (`Rotation`, `Gate`; None where none is declared).
    rotations: tuple[Rotation | None, ...] = ()
    gates: tuple[Gate | None, ...] = ()
    # The axial record (`hand-v1`, 2026-09-20; BEAM_LAW note 39): the index
    # in the world's table of one of the six headings, the body's axis,
    # read by the right-hand rule at every product of its `become` (None
    # without: an isotropic parent); and per family the parity filter of
    # the entry (`hand`: -1 or +1 admits that hand only, 0 admits every
    # hand as before).
    axis: int | None = None
    hands: tuple[int, ...] = ()
    # The energy E' declared under `covariant_readings` (`E`, whole units of
    # the identity), None for the load-time root `isqrt(E'_0^2 + d p . p)`.
    energy: int | None = None
    # The body's `level` under `atom_level` (`LevelDeclaration`), None without.
    level: LevelDeclaration | None = None

    def __post_init__(self) -> None:
        if not self.hands:
            object.__setattr__(self, "hands", (NO_HAND,) * len(self.table))
        if not self.splits:
            object.__setattr__(self, "splits", (None,) * len(self.table))
        if not self.label_turns:
            object.__setattr__(self, "label_turns", (0,) * len(self.table))
        if not self.rotations:
            object.__setattr__(self, "rotations", (None,) * len(self.table))
        if not self.gates:
            object.__setattr__(self, "gates", (None,) * len(self.table))
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
    # The row's hand (`hand-v1`): the family's, or the one declared on a
    # row of a family without one.
    hand: int = NO_HAND


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
    # The meeting (the world key `meeting`, false by default): a paid unit in
    # transit reads the free crowd at every free-space Node after the
    # collision and turns toward it by its phase register (`events/meeting.py`).
    meeting: bool = False
    # The massive rows (the world key `massive_rows`, false by default): a
    # paid family may then be declared `massive` (`massive-rows-v1`); the
    # record carries the identity under `hypotheses`, the books the
    # `waiting` lines and the rows' record `acc_turn`.
    massive_rows: bool = False
    # The covariant readings (the world key `covariant_readings`, absent by
    # default): the declaration, or None (`covariant-readings-v1`).
    covariant: CovariantDeclaration | None = None
    # The row's flight in the age wall's set (optical-v1, 2026-09-21; the
    # law's own since 2026-09-22, the generic entry of the bending): gamma,
    # the declared post-Newtonian parameter of the world key `optical`, 0
    # by default; the flight's coefficient is `flight_coefficient`, 1 + gamma.
    optical: int = 0
    # drive-b-v1 (the world key `drive_b`, false by default): the
    # directional drive of a body (`drive_wall`, `core.integer.by_line`).
    drive_b: bool = False
    # centred-step-v1 (the world key `centred_step`, false by default): the
    # body's step at half the wall on both drives (`CENTRED_STEP_RULE`).
    centred_step: bool = False
    # atom-level-v1 (the world key `atom_level`, false by default): the
    # release at a closure of the difference of two closures' levels
    # (`ATOM_LEVEL_RULE`; a body's `level` declaration).
    atom_level: bool = False

    @property
    def flight_coefficient(self) -> int:
        """The age wall's coefficient of the row's flight, f = 1 + gamma
        (the time part 1 and the space part gamma of the weak-field index
        1 + (1 + gamma) k); 1 by default, gamma the world's `optical`."""
        return 1 + self.optical

    @property
    def recorded(self) -> bool:
        """Whether a row of this world can carry a record: a lamp is
        declared (a record is born by a lamp, a rebirth follows a lamp's
        record; the amplitude law, the one click of stage (vii)). The
        record's columns, the books' `cancelled` and `remainder` lines and
        the identity `amplitude-v1` belong to a recorded world alone, so
        that a world without a lamp reads as it did before the law."""
        return any(entry.lamp is not None for entry in self.measured)

    @property
    def phase_mask(self) -> int:
        """The mask of the phase circle, N - 1."""
        return self.phase_steps - 1

    def turn(self, age: int, content: int) -> int:
        """The turn of a measured event's phase at the self-creation from
        `age` at a CONSTANT content from age 0: `by_clock(age, content x
        n, d)` phase steps at the clock's rate `turn_rate` = (n, d), the
        free release's own form at the rate [1, K] (the four unifications
        (2), BEAM_LAW note 33). The frame reads the turn as the count the
        body's turn accumulator gains, `by_drive(acc_turn, content x n,
        d)` (the fraction-free law, note 41), of which this is the
        constant-rate identity; the readings tools derive a lamp's turn by
        it. The frame refuses a turn of half the circle or more."""
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
    def column_scales(self) -> tuple[int, ...]:
        """Per column the common denominator of its values over the
        families, Lambda_c = lcm of the d_f^c (the fraction-free push,
        2026-09-20, BEAM_LAW note 41): every reader's charge in the
        column, the reduced sum of n_f^c M_f / d_f^c over what it holds,
        has a denominator dividing it, and so has every arriving value,
        so the push's rate V x E_c n_c / (D_c d_c) is a whole numerator
        over the one denominator Lambda_c^2 of the column's accumulator
        (`nature_beam.push_form`). 1 on gravity and on every column whose
        values are whole, where the push was exact already. Lambda_c^2,
        the denominator of the column's rows in every body's table of
        counts (`measured.counts_table`), is tested by division here,
        where Lambda_c is formed: a column whose square leaves the
        register is refused naming the column and the bound, at load
        (`parse_nature_beam_world` reads the scales once) and not at the
        first push (the physics-rule review of the branch,
        `docs/designs/fraction_free/REVIEW.md` section 4; the run's
        refusal of the lifted product, `nature_beam.column_bound_error`,
        stands beside it)."""
        found = []
        for column in range(len(self.families[0].columns)):
            scale = 1
            if column == 0 and self.drive_b:
                # Every family under one wall, step 3 (the law's own since
                # the generic entry of 2026-09-22): under `drive_b` a moving
                # body's gravity charge is the pair (w, Q S) (`body_weight`),
                # so gravity's Lambda is Q S.
                scale = LABEL_SCALE * self.width
            for family in self.families:
                denominator = family.columns[column].value[1]
                scale = scale * denominator // bounded_gcd(scale, denominator)
            if scale > MOMENTUM_BOUND // scale:
                name = self.families[0].columns[column].name
                raise ValueError(
                    f"{BEAM_LAW}: the column {name!r}: Lambda_c = {scale}, the least common "
                    "multiple of the families' value denominators in the column, has a square "
                    f"beyond the integer bound {MOMENTUM_BOUND}, the ceiling of the push's "
                    "accumulator over Lambda_c^2 (BEAM_LAW note 41 (iv)); the column's value "
                    f"denominators must have a least common multiple of at most "
                    f"{integer_root(MOMENTUM_BOUND)}"
                )
            found.append(scale)
        return tuple(found)

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

    @cached_property
    def handed(self) -> bool:
        """Whether the world declares a hand anywhere (`hand-v1`): a
        family's, a lamp's or a transit row's `hand`, a table entry's
        parity filter, a lamp's label hands, or a measured event's `axis`.
        Without one no row carries a hand, no line of the record names one
        and every world reads as it did, byte for byte. Read once per
        world (a cached property: the world is frozen)."""
        return (
            any(family.hand for family in self.families)
            or any(item.hand for item in self.in_transit)
            or any(
                entry.axis is not None
                or any(entry.hands)
                or (entry.lamp is not None and (entry.lamp.hand or entry.lamp.label_hands is not None))
                for entry in self.measured
            )
        )

    @property
    def hypotheses(self) -> list[str]:
        """The identities of the physical hypotheses the world declares
        beside the law, in a fixed order: `bohr-v1` for the turn by momentum
        (`action`), `columns-v1` for the one mechanism of the columns (a
        column beyond `charge`, or a lifetime: a force of nature in this
        law is a column with a sign and a range), `weak-v1` for the
        transformation `become` (the weak force in the world's terms),
        `meeting-v1` and `amplitude-v1` for their keys, `massive-rows-v1`
        for the world key `massive_rows` (the massive rows beside the law),
        `hand-v1` when the world declares a hand or an axis,
        `covariant-readings-v1` when the world declares `covariant_readings`,
        `optical-v1` for the world key `optical`, `drive-b-v1` for the world
        key `drive_b` (the directional drive of a body), `centred-step-v1`
        for the world key `centred_step` (the body's step at half the wall)
        and, last,
        `binding-v1` when a measured event holds a paid family (`binding`;
        the engine appends it at the same place from the first give of a
        run, `NatureBeamSimulation.hypotheses`)."""
        found = []
        if self.action is not None:
            found.append(BOHR_RULE)
        if self.declared_columns or self.lifetimes:
            found.append(COLUMNS_RULE)
        if self.transformations:
            found.append(WEAK_RULE)
        if self.meeting:
            found.append(MEETING_RULE)
        if self.recorded:
            found.append(AMPLITUDE_RULE)
        if self.massive_rows:
            found.append(MASSIVE_ROWS_RULE)
        if self.handed:
            found.append(HAND_RULE)
        if self.covariant is not None:
            found.append(COVARIANT_READINGS_RULE)
        # The row's flight in the age wall's set is the law's own since
        # 2026-09-22 (the generic entry of the bending): `optical-v1` names
        # no hypothesis any more; the runs that carried it keep it in their
        # records as history.
        if self.drive_b:
            found.append(DRIVE_B_RULE)
        if self.centred_step:
            found.append(CENTRED_STEP_RULE)
        if self.atom_level:
            found.append(ATOM_LEVEL_RULE)
        if self.binding:
            found.append(BINDING_RULE)
        return found

    @property
    def binding(self) -> bool:
        """Whether a measured event holds content of a paid family other
        than its own at the start (`held`): the content a body carries,
        which the binding that costs content (`binding-v1`) gives to the
        flight at the body's contact under `measure`. A lamp's own paid
        content is not carried content and never counts. What is held at
        load only: a body that takes paid content during the run gives it
        at its next contact, and the engine raises the fact then
        (`NatureBeamSimulation.binding`, `hypotheses`)."""
        return any(
            content > 0 and not self.families[family].free and family != entry.family
            for entry in self.measured
            for family, content in enumerate(entry.held)
        )

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
    components: list[int] = []
    for item, extent in zip(value, shape, strict=True):
        if type(item) is not int or item < 0 or item >= extent:
            raise ValueError(
                f"{BEAM_LAW}: {label} components must be integers on the GameBoard, from 0 "
                f"through the extent less one on each axis of the shape {list(shape)}"
            )
        components.append(item)
    return components[0], components[1], components[2]


def _vector(value: object, label: str, bound: int) -> Vector:
    """A primitive integer vector with every component in -bound .. bound."""
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{BEAM_LAW}: {label} must be three integers")
    components: list[int] = []
    for item in value:
        if type(item) is not int or item < -bound or item > bound:
            raise ValueError(
                f"{BEAM_LAW}: {label} components must be integers from {-bound} through {bound}"
            )
        components.append(item)
    found = (components[0], components[1], components[2])
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


def bresenham_line(vector: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    """The S_1 unit steps of one period of the digital line of v: at each
    step the axis whose progress is furthest behind, the lowest axis first
    (the flight's walk, `nature_beam.direction_flight`; the loader's walk of
    a record's paths, `_aperture_load_check`)."""
    s1 = sum(abs(c) for c in vector)
    line: list[tuple[int, int, int]] = []
    position = [0, 0, 0]
    for j in range(s1):
        best = max(range(3), key=lambda i: (abs(vector[i]) * (j + 1) - s1 * abs(position[i]), -i))
        step = [0, 0, 0]
        step[best] = 1 if vector[best] > 0 else -1
        position[best] += step[best]
        line.append((step[0], step[1], step[2]))
    return line


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
            f"{BEAM_LAW}: {label} must be one integer (a scalar): the flight gives every "
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
    value: object,
    phase_steps: int,
    age_bound: int = AMOUNT_BOUND,
    massive_rows: bool = False,
    action: int | None = None,
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
        turn_key = f"families[{index}].phase_per_link"
        declared_turn = obj.get("phase_per_link", 0)
        per_age: tuple[int, int] | None = None
        if isinstance(declared_turn, list):
            # The pair form: the phase per interval of age (the amplitude
            # law's frequency; an integer turns per Link crossed).
            per_age = _ratio(declared_turn, turn_key, zero=True)
            # The walk forms (age + 1) x n whole (`by_clock_rows`): bounded
            # here, before it is formed, by the world's largest age.
            if per_age[0] > AMOUNT_BOUND // (age_bound + 1):
                raise ValueError(
                    f"{BEAM_LAW}: {turn_key} [{per_age[0]}, {per_age[1]}]: (age_bound + 1) x n "
                    f"= {age_bound + 1} x {per_age[0]} exceeds the integer bound {AMOUNT_BOUND}"
                )
            per_link = 0
        else:
            per_link = _integer(declared_turn, turn_key, 0, phase_steps - 1)
        if (per_link or per_age is not None) and not phase:
            raise ValueError(f"{BEAM_LAW}: {turn_key} is refused for a family without a phase circle")
        lifetime = _lifetime(obj.get("lifetime"), f"families[{index}].lifetime", age_bound)
        hand = _hand(obj["hand"], f"families[{index}].hand") if "hand" in obj else NO_HAND
        massive = _massive(obj, f"families[{index}]", massive_rows, action, quantum, phase, name)
        found.append(
            FamilyDefinition(
                name,
                quantum,
                charge,
                phase,
                per_link,
                lifetime=lifetime,
                phase_per_age=per_age,
                hand=hand,
                massive=massive,
            )
        )
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
            family.phase_per_age,
            family.hand,
            family.massive,
        )
        for family, columns in zip(found, declared, strict=True)
    )


def _massive(
    obj: dict[str, object],
    label: str,
    massive_rows: bool,
    action: int | None,
    quantum: int,
    phase: bool,
    name: str,
) -> bool:
    """The family key `massive` (`massive-rows-v1`): true or false, false
    by default. Refused, naming the key: without the world key
    `massive_rows`; with `phase_per_link` in either form (a massive row
    turns per axis Link by de Broglie's rule, never per Link count or per
    interval of age); on a free family (a free family's rows are a body's
    field, never massive) or on a family without a phase circle (there is
    no phase to turn); without the world's `action` (the turn's h)."""
    if "massive" not in obj:
        return False
    massive = obj["massive"]
    if type(massive) is not bool:
        raise ValueError(f"{BEAM_LAW}: {label}.massive must be true or false")
    if not massive:
        return False
    if not massive_rows:
        raise ValueError(
            f"{BEAM_LAW}: {label}.massive is refused without the world key `massive_rows` "
            f"(the identity {MASSIVE_ROWS_RULE} beside the law, absent by default)"
        )
    if "phase_per_link" in obj:
        raise ValueError(
            f"{BEAM_LAW}: {label}.massive is refused with phase_per_link (the integer or the "
            f"pair): a massive row turns |p_a| x N / h at every axis Link it crosses, by "
            "de Broglie, never per Link count and never per interval of age"
        )
    if quantum == FREE_QUANTUM:
        raise ValueError(
            f"{BEAM_LAW}: {label}.massive is refused on the free family {name!r} (quantum 0): a "
            "free family's rows are a body's field; a massive family is paid, its quantum the "
            "content M of one row"
        )
    if not phase:
        raise ValueError(
            f"{BEAM_LAW}: {label}.massive is refused on the family {name!r} without a phase "
            "circle: a massive row turns its phase by its momentum at every axis Link"
        )
    if action is None:
        raise ValueError(
            f"{BEAM_LAW}: {label}.massive needs the world's `action` (the quantum h of the "
            "turn, |p_a| x N over h per axis Link), which the world does not declare"
        )
    return True


def _window(value: object, label: str, phase_steps: int) -> int:
    """A phase window's setting: a step of the circle, 0 through N - 1."""
    return _integer(value, label, 0, phase_steps - 1)


def _hand(value: object, label: str) -> int:
    """A declared hand: -1 (left) or +1 (right), nothing else (0 is no
    hand and is not declared; a hand is one of the two)."""
    if type(value) is not int or value not in HANDS:
        raise ValueError(f"{BEAM_LAW}: {label} must be -1 or 1 (the two hands; a row without one has 0)")
    return value


def _axis(value: object, label: str) -> int:
    """The axial record of a measured event: one of the six headings in
    Port order, declared as its vector ([1, 0, 0] .. [0, 0, -1]); the
    index of the heading in the world's direction table."""
    if not isinstance(value, list) or len(value) != 3 or any(type(v) is not int for v in value):
        raise ValueError(
            f"{BEAM_LAW}: {label} must be one of the six headings as a vector, [1, 0, 0] .. [0, 0, -1]"
        )
    vector = (value[0], value[1], value[2])
    if vector not in PORT_HEADINGS:
        raise ValueError(
            f"{BEAM_LAW}: {label} {list(vector)} is not one of the six headings (an axis is a "
            "heading in Port order, [1, 0, 0] .. [0, 0, -1])"
        )
    return HEADING_OFFSET + PORT_HEADINGS.index(vector)


def axis_sign(axis: Vector, direction: Vector) -> int:
    """The sign of the inner product of an axis (a heading) with a direction
    vector, in {-1, 0, +1}: the right-hand rule's one integer (BEAM_LAW
    note 39). An axis is a heading, so the product is one component of the
    direction with a sign, within P; the sign is the same on the direction's
    unit label u_d, whose components carry the direction's signs."""
    product = sum(int(a) * int(d) for a, d in zip(axis, direction, strict=True))
    return (product > 0) - (product < 0)


def _handed_products(
    rules: list[tuple[str, Transformation]],
    families: tuple[FamilyDefinition, ...],
    axis: int | None,
    directions: tuple[int, ...],
    table: tuple[Vector, ...],
) -> None:
    """The right-hand rule's refusal at load: on a parent with an `axis` a
    product of a family with a hand h is born only on the parent's
    directions d with sign(A . u_d) = h (a left-handed product leaves
    against the axis), so a product with none such has nowhere to leave:
    refused naming the event's rule, the product and the axis (a declared
    transformation that cannot leave is a defect of the world, loud)."""
    if axis is None:
        return
    heading = table[axis]
    for label, rule in rules:
        for k, (family, _, _) in enumerate(rule.products):
            hand = families[family].hand
            if not hand:
                continue
            if not any(axis_sign(heading, table[d]) == hand for d in directions):
                raise ValueError(
                    f"{BEAM_LAW}: {label}.products[{k}] ({families[family].name!r}, hand {hand:+d}) "
                    f"has no direction to leave on: none of the event's directions "
                    f"{[list(table[d]) for d in directions]} has sign(A . u_d) = {hand:+d} against "
                    f"the axis {list(heading)} (a left-handed product leaves against the axis, a "
                    "right-handed one along it)"
                )


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
    amount: int,
    content: int,
    table: tuple[Vector, ...],
    directions: tuple[int, ...],
    label: str,
    scale: int = LABEL_SCALE,
) -> None:
    """The momentum label of a release or a declared ray, `content x amount x
    u_d` with u_d the unit vector of the direction at the scale Q (no
    component beyond Q), must fit the bound on every component: Q x content
    x amount within 2^62 - 1, that is content x amount below 2^56; a
    massive family's rows at their scale p where it is the larger."""
    for direction in directions:
        if scale * content * amount > MOMENTUM_BOUND:
            raise ValueError(
                f"{BEAM_LAW}: {label}: the momentum label {scale} x {content} x {amount} = "
                f"{scale * content * amount} along {list(table[direction])} exceeds the "
                f"integer bound {MOMENTUM_BOUND} (content x amount at most {MOMENTUM_BOUND // scale})"
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
    family_hand: int = NO_HAND,
    massive: bool = False,
) -> LampDefinition:
    obj = _object(value, label, LAMP_KEYS, {"rate", "wheel"})
    rate = _ratio(obj["rate"], f"{label}.rate", zero=True)
    if not isinstance(obj["wheel"], list):
        raise ValueError(
            f"{BEAM_LAW}: {label}.wheel must be [r, W], the rate of the birth wheel (the record's "
            "coordinate u on the ladder advances by r over W at every birth; [1, N] the count of "
            "births mod N)"
        )
    wheel = _ratio(obj["wheel"], f"{label}.wheel", zero=False)
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
    turns = (0,) * len(directions)
    if "turns" in obj:
        turns = _split_rows(obj["turns"], f"{label}.turns", len(directions), None, 0, phase_steps - 1)[0]
    arms = 1
    if "arms" in obj:
        arms = _integer(obj["arms"], f"{label}.arms", 1, len(directions))
        if len(directions) % arms:
            raise ValueError(
                f"{BEAM_LAW}: {label}.arms {arms} does not divide the {len(directions)} directions "
                "(every arm takes the same number of directions, in order)"
            )
    branches: tuple[tuple[int, int], ...] = ((0, 1),)
    label_hands: tuple[int, int] | None = None
    if "branches" in obj:
        branches, label_hands = _branches(obj["branches"], f"{label}.branches", arms)
    # The lamp's hand (`hand-v1`): declared on a lamp of a family without a
    # hand, or the family's own value repeated; a lamp of a branched family
    # whose labels carry the hands declares neither, and a family with a
    # hand cannot birth a record whose labels name hands (one or the other
    # per family, so that a row's hand is defined once).
    hand = NO_HAND
    if "hand" in obj:
        hand = _hand(obj["hand"], f"{label}.hand")
        if family_hand and hand != family_hand:
            raise ValueError(
                f"{BEAM_LAW}: {label}.hand {hand:+d} differs from the family's hand {family_hand:+d}: "
                "a lamp of a chiral family releases the family's hand"
            )
    if label_hands is not None and (hand or family_hand):
        raise ValueError(
            f"{BEAM_LAW}: {label}.branches name the hands of their labels and the "
            f"{'lamp' if hand else 'family'} declares a hand: a family carries its hand as the "
            "row's column or as the meaning of a label bit, never both"
        )
    # The momentum label's magnitude p of a massive family's rows
    # (`massive-rows-v1`): required on the lamp of a massive family (its
    # rows' label p_D per direction is formed at the scale p), refused on
    # any other lamp, an integer from 1 (a row at rest is not a massive
    # row's birth).
    momentum_magnitude: int | None = None
    if "momentum_magnitude" in obj:
        if not massive:
            raise ValueError(
                f"{BEAM_LAW}: {label}.momentum_magnitude belongs to the lamp of a massive family "
                "(the family key `massive` under the world key `massive_rows`); this family is "
                "not massive"
            )
        momentum_magnitude = _integer(obj["momentum_magnitude"], f"{label}.momentum_magnitude", 1)
    elif massive:
        raise ValueError(
            f"{BEAM_LAW}: {label} lacks keys: momentum_magnitude (the lamp of a massive family "
            "declares the magnitude p of its rows' momentum label, in label units)"
        )
    # The largest label a release can carry: the rate's numerator units at
    # the largest turn the content allows (the whole part of amount x n / d
    # at the clock's rate [n, d]); for a record the largest weight of a
    # branch is the amount of a row; a massive family's label at the scale
    # p in place of Q where p is the larger.
    largest_turn = max(1, amount * turn_rate[0] // turn_rate[1])
    largest_weight = max(weight for _, weight in branches)
    _label_bound(
        max(1, rate[0], largest_weight),
        quantum * largest_turn,
        table,
        directions,
        f"{label} (the release)",
        scale=max(LABEL_SCALE, momentum_magnitude or 0),
    )
    return LampDefinition(
        rate,
        wheel,
        directions,
        window,
        width,
        turns,
        branches,
        arms,
        hand=hand,
        label_hands=label_hands,
        momentum_magnitude=momentum_magnitude,
    )


def _branches(
    value: object, label: str, arms: int
) -> tuple[tuple[tuple[int, int], ...], tuple[int, int] | None]:
    """The joint labels of a birth: [[label, weight], ...], the labels
    distinct integers below 2^arms (the bit k of a label is its value on
    arm k), the weights integers from 1; since `hand-v1` each may carry a
    third entry, the hand of the label (-1 or +1), every branch or none:
    the hand is what a label bit means, the bit k of a label the hand of
    the row on arm k, so the branches must give each value of a bit one
    hand and the two values opposite hands (the hand of the other value
    follows when only one is named). Returns the branches and the hands of
    the bit values 0 and 1, or None where none is named."""
    if not isinstance(value, list) or not value:
        raise ValueError(f"{BEAM_LAW}: {label} must be a list of [label, weight] pairs")
    found: list[tuple[int, int]] = []
    hands: list[int | None] = []
    for index, item in enumerate(value):
        if not isinstance(item, list) or len(item) not in (2, 3):
            raise ValueError(
                f"{BEAM_LAW}: {label}[{index}] must be a [label, weight] pair, or [label, weight, hand]"
            )
        joint = _integer(item[0], f"{label}[{index}].label", 0, (1 << arms) - 1)
        weight = _integer(item[1], f"{label}[{index}].weight", 1, AMOUNT_BOUND)
        if any(joint == other for other, _ in found):
            raise ValueError(f"{BEAM_LAW}: {label} names the label {joint} twice")
        found.append((joint, weight))
        hands.append(_hand(item[2], f"{label}[{index}].hand") if len(item) == 3 else None)
    norm = sum(weight * weight for _, weight in found)
    if norm > MOMENTUM_BOUND:
        raise ValueError(f"{BEAM_LAW}: {label}: the norm {norm} exceeds the integer bound")
    if all(hand is None for hand in hands):
        return tuple(found), None
    if any(hand is None for hand in hands):
        raise ValueError(f"{BEAM_LAW}: {label} names a hand on some labels and not on others")
    meaning: list[int | None] = [None, None]
    for (joint, _), hand in zip(found, hands, strict=True):
        assert hand is not None
        for arm in range(arms):
            bit = (joint >> arm) & 1
            if meaning[bit] is None:
                meaning[bit] = hand
            elif meaning[bit] != hand:
                raise ValueError(
                    f"{BEAM_LAW}: {label} gives the bit value {bit} two hands: a hand is a label "
                    "bit named, one hand per value of the bit"
                )
    if meaning[0] is not None and meaning[1] is not None and meaning[0] == meaning[1]:
        raise ValueError(
            f"{BEAM_LAW}: {label} gives both values of a label bit the hand {meaning[0]:+d}: the two "
            "values of a bit are the two hands"
        )
    zero = meaning[0] if meaning[0] is not None else -int(meaning[1] or 0)
    one = meaning[1] if meaning[1] is not None else -zero
    return tuple(found), (zero, one)


def _label_turn(value: object, label: str, rule: str, phase_steps: int) -> int:
    """The entry's `turn` (the amplitude law's rotation at a `sum` set: the
    phase step on label 1 of the setting's rotation, 0 by default), refused
    on `pass`."""
    if not isinstance(value, dict) or "turn" not in value:
        return 0
    if rule == "pass":
        raise ValueError(f"{BEAM_LAW}: {label}.turn is refused on pass, which reads nothing")
    return _integer(value["turn"], f"{label}.turn", 0, phase_steps - 1)


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


@dataclass(frozen=True)
class Split:
    """The split of a `rerelease` entry as declared (the amplitude law, the
    owner's unification (2): the split is `rerelease` with a vector of
    integer weights and the multiplicity, one rule): per row of the table
    one weight per declared direction of the measured event (`weights`,
    integers from 0, at least one positive per row) and one phase step
    per direction (`turns`, 0 by default); `inputs`, when declared, the
    arrival directions that select the row (a beam splitter transmits and
    reflects by the side the row comes from; the design's Mach-Zehnder,
    section 3.4), and None for one row on every arrival (a mirror, an
    opening's fan)."""

    weights: tuple[tuple[int, ...], ...]
    turns: tuple[tuple[int, ...], ...]
    inputs: tuple[int, ...] | None = None

    def row(self, arrival: int) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
        """The weights and turns for a row that arrived on `arrival`; None
        where the entry declares inputs and the arrival is not among them."""
        if self.inputs is None:
            return self.weights[0], self.turns[0]
        if arrival not in self.inputs:
            return None
        k = self.inputs.index(arrival)
        return self.weights[k], self.turns[k]


@dataclass(frozen=True)
class Rotation:
    """A `rerelease` entry's rotation of one label bit on the GameBoard (the
    design's 2.2, a single-label gate): the rows of every record at the
    entry, per label, become two rows on the label's bit `bit` cleared and
    set, `(w C'[s], m 65536, p)` and `(w S'[s], m 65536, p + t)` from a
    clear bit, `(w S'[s], m 65536, p + N/2)` and `(w C'[s], m 65536,
    p + t)` from a set bit, on the half-angle tables of 2N (the setting s,
    the turn t on the set bit): U_s = [[C', S' v(t)], [-S', C' v(t)]].
    Not a click: invertible on the tables, the rows kept."""

    setting: int
    bit: int = 0
    turn: int = 0


@dataclass(frozen=True)
class Gate:
    """A `rerelease` entry's gate between records (the design's section 10):
    `cnot`, the permutation of the joint labels of the records whose rows
    are pending at the entry, (l_c, l_t) -> (l_c, l_t xor l_c) from the
    control (the record whose rows arrive on the declared `control`
    direction, which survives; the review of (v), S1: a circuit does not
    change with the order of the `measured` list) to every other record's
    first label bit; the records join into one (the joint labels the
    product of their label sets, every row replicated over the other
    records' labels with its multiplicity times the copies, the copies
    booked on the layer's live count). `hold`: the entry holds the rows
    pending until rows of `parties` distinct emitters are pending at it
    (the design's local hold, read from the rows alone; the review's B3);
    without `hold` the rows of an entry short of that pass as a plain
    re-emission. A record that reaches a gate with units elsewhere or
    with an offer already made is refused by the layer (the lazy
    relabelling of the design's section 10 is not built; the review's
    B2). `control` is the index of the direction in the world's table,
    required for two parties or more, none for a gate of one party."""

    kind: str = "cnot"
    hold: bool = True
    parties: int = 2
    control: int | None = None


GATE_KINDS = ("cnot",)
LABEL_BITS_BOUND = 32


def _rotation(value: object, label: str, rule: str, phase_steps: int) -> Rotation | None:
    """The entry's `rotate` (`Rotation`): refused on a rule other than
    `rerelease`; None where none is declared."""
    if not isinstance(value, dict) or "rotate" not in value:
        return None
    if rule != "rerelease":
        raise ValueError(f"{BEAM_LAW}: {label}.rotate belongs to a `rerelease` entry, not to {rule}")
    obj = _object(value["rotate"], f"{label}.rotate", {"setting", "bit", "turn"}, {"setting"})
    return Rotation(
        _integer(obj["setting"], f"{label}.rotate.setting", 0, 2 * phase_steps - 1),
        _integer(obj.get("bit", 0), f"{label}.rotate.bit", 0, LABEL_BITS_BOUND - 1),
        _integer(obj.get("turn", 0), f"{label}.rotate.turn", 0, phase_steps - 1),
    )


def _gate(value: object, label: str, rule: str, table: tuple[Vector, ...]) -> Gate | None:
    """The entry's `gate` (`Gate`): refused on a rule other than
    `rerelease`; None where none is declared. `control`, the direction the
    control's rows arrive on, is required for two parties or more and
    refused for one (the review of (v), S1)."""
    if not isinstance(value, dict) or "gate" not in value:
        return None
    if rule != "rerelease":
        raise ValueError(f"{BEAM_LAW}: {label}.gate belongs to a `rerelease` entry, not to {rule}")
    obj = _object(value["gate"], f"{label}.gate", {"kind", "hold", "parties", "control"}, {"kind"})
    kind = obj["kind"]
    if kind not in GATE_KINDS:
        raise ValueError(f"{BEAM_LAW}: {label}.gate.kind must be one of {list(GATE_KINDS)}")
    hold = obj.get("hold", True)
    if type(hold) is not bool:
        raise ValueError(f"{BEAM_LAW}: {label}.gate.hold must be true or false")
    parties = _integer(obj.get("parties", 2), f"{label}.gate.parties", 1, LABEL_BITS_BOUND)
    control: int | None = None
    if "control" in obj:
        if parties == 1:
            raise ValueError(f"{BEAM_LAW}: {label}.gate.control: a gate of one party has no control")
        control = _direction(obj["control"], f"{label}.gate.control", table)
    elif parties > 1:
        raise ValueError(
            f"{BEAM_LAW}: {label}.gate of {parties} parties declares its control: `control`, the "
            "direction the control record's rows arrive on (a circuit does not depend on the "
            "order of the measured list)"
        )
    return Gate(str(kind), hold, parties, control)


def _split_rows(
    value: object, label: str, ways: int, rows: int | None, least: int, top: int
) -> tuple[tuple[int, ...], ...]:
    """Lists of `ways` integers in `least` .. `top`: one list where `rows`
    is None (no `inputs` declared), a list of `rows` lists otherwise (one
    per declared input)."""
    listed = value if rows is not None else [value]
    count = 1 if rows is None else rows
    if not isinstance(listed, list) or len(listed) != count:
        raise ValueError(f"{BEAM_LAW}: {label} must list one row per declared input ({count})")
    found = []
    for k, row in enumerate(listed):
        if not isinstance(row, list) or len(row) != ways:
            raise ValueError(
                f"{BEAM_LAW}: {label} must list one integer per declared direction ({ways})"
                + (f" in row {k}" if rows is not None else "")
            )
        found.append(tuple(_integer(item, label, least, top) for item in row))
    return tuple(found)


def _split(
    value: object,
    label: str,
    rule: str,
    ways: int,
    phase_steps: int,
    free: bool,
    table: tuple[Vector, ...],
) -> Split | None:
    """The split of a table entry (`Split`): refused on a rule other than
    `rerelease` and on a free family's entry; None where the entry
    declares none of its keys."""
    if not isinstance(value, dict) or not any(key in value for key in SPLIT_KEYS):
        return None
    named = ", ".join(key for key in SPLIT_KEYS if key in value)
    if rule != "rerelease":
        raise ValueError(
            f"{BEAM_LAW}: {label} declares {named} on the rule {rule!r}: the split is a "
            "`rerelease` with weights (one rule)"
        )
    if free:
        raise ValueError(
            f"{BEAM_LAW}: {label} declares {named} on a free family's entry: free families never branch"
        )
    inputs: tuple[int, ...] | None = None
    if "inputs" in value:
        inputs = _directions(value["inputs"], f"{label}.inputs", table)
    rows = None if inputs is None else len(inputs)
    if "weights" in value:
        weights = _split_rows(value["weights"], f"{label}.weights", ways, rows, 0, AMOUNT_BOUND)
        for row in weights:
            if not any(row):
                raise ValueError(
                    f"{BEAM_LAW}: {label}.weights must have at least one positive weight per row"
                )
    else:
        weights = ((1,) * ways,) * (rows or 1)
    if "turns" in value:
        turns = _split_rows(value["turns"], f"{label}.turns", ways, rows, 0, phase_steps - 1)
    else:
        turns = ((0,) * ways,) * (rows or 1)
    return Split(weights, turns, inputs)


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
) -> tuple[str, int | WindowReading | None, str, int | None, Transformation | None, int]:
    """One table entry: a rule string, or `{"rule": ..., "phase_window": s,
    "phase_width": w, "reads": key}` (the rule the family's default when the
    object omits it, so a window alone is a lawful entry; a window and its
    width refused on `pass`, which responds to nothing, and for a family
    without a phase circle, whose rays carry no phase; the width refused
    without the window's setting; the reading's component `vector` by
    default on `read`, `scalar` otherwise), or a `become` entry, the click
    trigger of the transformation, with its `into` and `products` (refused
    on any other rule; `at` and `crowd` refused: the window is the gate);
    and since `hand-v1` the parity filter `hand` (-1 or +1: the entry's
    rule applies to arrivals of that hand only, the rest passed as an
    arrival outside a window is; refused on `pass`).
    Returns the rule, the window's setting (a number, or a `WindowReading`
    where the entry reads its centre from a reading, issue #363), the
    component, the window's width (None: N / 2), the transformation
    (None but on `become`) and the hand the entry admits (0: every hand)."""
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
    hand = NO_HAND
    if "hand" in obj:
        if rule == "pass":
            raise ValueError(
                f"{BEAM_LAW}: {label}.hand is refused on pass: a hand filter admits arrivals of one "
                "hand to a rule, and pass responds to nothing"
            )
        hand = _hand(obj["hand"], f"{label}.hand")
    return str(rule), window, str(reads), width, transformation, hand


def _atom_levels(
    value: object,
    measured: tuple[MeasuredDefinition, ...],
    families: tuple[FamilyDefinition, ...],
    atom_level: bool,
    action: int | None,
    ticks: int,
) -> tuple[MeasuredDefinition, ...]:
    """The bodies' `level` declarations under the world key `atom_level`
    (`atom-level-v1`, docs/designs/atom_levels/LEVELS.md section 2 (c)):
    `{"family": F, "pair": [n_l, d_l], "return": [axis, sign]}` on a
    measured event that turns its phase by its momentum and is not fixed;
    F a paid family with a phase circle (its rows carry the turn); the pair
    two positive integers; the axis 0, 1 or 2 and the sign -1 or +1. Refused
    without the key, and the key's bounds refused at load: the divisor
    `2 h d_l T` for a count T up to the run's ticks within the register."""
    assert isinstance(value, list)
    found = list(measured)
    names = {family.name: index for index, family in enumerate(families)}
    for index, (entry, definition) in enumerate(zip(value, measured, strict=True)):
        assert isinstance(entry, dict)
        if "level" not in entry:
            continue
        label = f"measured[{index}].level"
        if not atom_level:
            raise ValueError(
                f"{BEAM_LAW}: {label} is refused without the world key atom_level "
                "(atom-level-v1, off by default)"
            )
        obj = _object(entry["level"], label, {"family", "pair", "return"}, {"family", "pair", "return"})
        family_name = obj["family"]
        if not isinstance(family_name, str) or family_name not in names:
            raise ValueError(f"{BEAM_LAW}: {label}.family names an unknown family")
        family = names[family_name]
        if families[family].free:
            raise ValueError(
                f"{BEAM_LAW}: {label}.family names the free family {family_name!r}: a released "
                "row carries content h_q x (the rise of the level), so the family is paid"
            )
        if not families[family].phase:
            raise ValueError(
                f"{BEAM_LAW}: {label}.family names the family {family_name!r} without a phase "
                "circle: a released row turns its phase by its content over the quantum"
            )
        pair_value = obj["pair"]
        if not isinstance(pair_value, list) or len(pair_value) != 2:
            raise ValueError(f"{BEAM_LAW}: {label}.pair must be two positive integers [n_l, d_l]")
        pair = (
            _integer(pair_value[0], f"{label}.pair[0]", 1),
            _integer(pair_value[1], f"{label}.pair[1]", 1),
        )
        return_value = obj["return"]
        if not isinstance(return_value, list) or len(return_value) != 2:
            raise ValueError(f"{BEAM_LAW}: {label}.return must be [axis, sign]")
        axis = _integer(return_value[0], f"{label}.return[0]", 0, 2)
        sign = _integer(return_value[1], f"{label}.return[1]", -1, 1)
        if sign == 0:
            raise ValueError(f"{BEAM_LAW}: {label}.return[1] must be -1 or +1, the sign crossed to")
        if definition.fixed or not definition.phase_by_momentum:
            raise ValueError(
                f"{BEAM_LAW}: {label} needs a body that steps and turns its phase by its momentum "
                "(phase_by_momentum, not fixed): the level is read off its action rows"
            )
        assert action is not None
        if 2 * action * pair[1] > MOMENTUM_BOUND // max(ticks, 1):
            raise ValueError(
                f"{BEAM_LAW}: {label}: the level's divisor 2 h d_l x (the count) leaves the "
                f"integer bound {MOMENTUM_BOUND} within the run's ticks"
            )
        found[index] = replace(definition, level=LevelDeclaration(family, pair, axis, sign))
    return tuple(found)


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
        hands: list[int] = [NO_HAND] * len(families)
        window_reads: list[tuple[int, int] | None] = [None] * len(families)
        splits: list[Split | None] = [None] * len(families)
        label_turns: list[int] = [0] * len(families)
        rotations: list[Rotation | None] = [None] * len(families)
        gates: list[Gate | None] = [None] * len(families)
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
            rule, entry_window, component, widths[at], transforms[at], hands[at] = _table_entry(
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
            splits[at] = _split(
                entry_value,
                entry_label,
                rule,
                len(directions),
                phase_steps,
                families[at].free,
                table,
            )
            label_turns[at] = _label_turn(entry_value, entry_label, rule, phase_steps)
            rotations[at] = _rotation(entry_value, entry_label, rule, phase_steps)
            gates[at] = _gate(entry_value, entry_label, rule, table)
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
        # The axial record (`hand-v1`): one of the six headings, or none;
        # a handed product of the event's transformations must have a
        # direction on its side of it.
        axis = _axis(obj["axis"], f"{label}.axis") if "axis" in obj else None
        # The energy declared under `covariant_readings` (checked against
        # the world key and the invariant by `_covariant`).
        energy = _integer(obj["E"], f"{label}.E", 1) if "E" in obj else None
        _handed_products(
            [
                *([(f"{label}.become", become)] if become is not None else []),
                *(
                    (f"{label}.table[{families[f].name!r}]", t)
                    for f, t in enumerate(transforms)
                    if t is not None
                ),
            ],
            families,
            axis,
            directions,
            table,
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
                family_hand=families[family].hand,
                massive=families[family].massive,
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
                tuple(splits),
                tuple(label_turns),
                tuple(rotations),
                tuple(gates),
                axis=axis,
                hands=tuple(hands),
                energy=energy,
            )
        )
    return tuple(found)


def _covariant(
    value: object,
    measured: tuple[MeasuredDefinition, ...],
    families: tuple[FamilyDefinition, ...],
    width: int,
    turn_rate: tuple[int, int],
    action: int | None,
    drive_b: bool = False,
) -> CovariantDeclaration | None:
    """The world key `covariant_readings` (`covariant-readings-v1`,
    DERIVATIONS_BEAM 17.6): absent, None, and a measured event's `E` is
    refused. Declared: `c2` the pair [1, d] (d from 1; the design's [1, 3]),
    `grain` a power of two dividing Q S, `books` true or false (false by
    default); refused with `action` (17.6 S4: the turn by momentum per Link
    and the proper-time cadence do not compose on one phase until designed).
    Per measured event that is not `fixed` (an apparatus carries no readings
    and may declare no `E`): the momentum on one axis unless the world
    declares `drive_b` (the base is `main`'s per-axis drive, `step_axis`,
    where the pace p / E' holds on one axis; under `drive-b-v1` the drive
    walks the line of the momentum at p_a / (Q S M) per self-creation on
    every axis, and the refusal is lifted), the domain `|p|_1 <= Q S M` (17.6
    N2: above it the drive's one Link per self-creation gives a pace that
    falls with p);
    `W / g^2 = (E'_0 / g)^2 + d (p / g) . (p / g)` within the integer bound,
    tested by division before the product is formed; a declared `E` at or
    above `E'_0` and within one of the load-time root `isqrt(W)` (17.6 M3).
    Every paid family off the identity `d h n = Q S d_K` is listed with its
    gap as a diagnostic (17.6 N5), a refusal only under `books`."""
    declared = [index for index, entry in enumerate(measured) if entry.energy is not None]
    if value is None:
        if declared:
            raise ValueError(
                f"{BEAM_LAW}: measured[{declared[0]}].E is refused without the world key "
                "covariant_readings (the energy E' is a reading of covariant-readings-v1)"
            )
        return None
    label = "covariant_readings"
    obj = _object(value, label, COVARIANT_KEYS, {"c2", "grain"})
    if action is not None:
        raise ValueError(
            f"{BEAM_LAW}: {label} is refused with `action`: the turn by momentum per Link stepped "
            "and the turn per proper time do not compose on one phase until designed "
            "(DERIVATIONS_BEAM 17.6 S4)"
        )
    c2 = _ratio(obj["c2"], f"{label}.c2", zero=False)
    if c2[0] != 1:
        raise ValueError(
            f"{BEAM_LAW}: {label}.c2 must be the pair [1, d] (c^2 = 1 / d; the design's [1, 3]), "
            f"not {list(c2)}: the exact square is W = E'_0^2 + d p . p with E'_0 = Q S M whole"
        )
    factor = c2[1]
    grain = _integer(obj["grain"], f"{label}.grain", 1)
    if grain & (grain - 1):
        raise ValueError(f"{BEAM_LAW}: {label}.grain must be a power of two, not {grain}")
    if (LABEL_SCALE * width) % grain:
        raise ValueError(
            f"{BEAM_LAW}: {label}.grain {grain} must divide Q x S = {LABEL_SCALE * width} so that "
            "E'_0 / g = (Q S / g) x M is whole for every content"
        )
    books = obj.get("books", False)
    if type(books) is not bool:
        raise ValueError(f"{BEAM_LAW}: {label}.books must be true or false")
    for index, entry in enumerate(measured):
        if entry.fixed:
            # An apparatus held in place carries no readings (its momentum
            # line is the push it took, never a motion): no domain, no `E`.
            if entry.energy is not None:
                raise ValueError(
                    f"{BEAM_LAW}: measured[{index}].E is refused on a fixed measured event: an "
                    "apparatus held in place carries no readings under covariant_readings"
                )
            continue
        content = sum(entry.held)
        axes = [axis for axis, component in enumerate(entry.momentum) if component]
        if len(axes) > 1 and not drive_b:
            raise ValueError(
                f"{BEAM_LAW}: measured[{index}]: the momentum {list(entry.momentum)} has components "
                f"on more than one axis; under {label} a body's momentum lies on one axis (the base "
                "is the per-axis drive of BEAM_LAW note 17, `step_axis`, where the pace p / E' holds "
                "on one axis) unless the world declares `drive_b` (form B's directional drive, "
                "drive-b-v1, off by default)"
            )
        manhattan = sum(abs(component) for component in entry.momentum)
        if manhattan > LABEL_SCALE * width * content:
            raise ValueError(
                f"{BEAM_LAW}: measured[{index}]: |p|_1 = {manhattan} exceeds Q x S x M = "
                f"{LABEL_SCALE * width * content}, the domain of the pace p / E' under "
                f"{label} (DERIVATIONS_BEAM 17.6 N2: beyond it the drive gives one Link per "
                "self-creation and the pace falls with p)"
            )
        square = covariant_square(content, entry.momentum, width, factor, grain, f"measured[{index}]")
        root = integer_root(square)
        if entry.energy is not None:
            rest = LABEL_SCALE * width * content // grain
            declared_energy = entry.energy // grain
            if declared_energy < rest or abs(declared_energy - root) > 1:
                raise ValueError(
                    f"{BEAM_LAW}: measured[{index}].E = {entry.energy}: at the grain {grain} "
                    f"E' / g = {declared_energy} must be at or above E'_0 / g = {rest} and within "
                    f"one of the root {root} of W / g^2 = {square} (DERIVATIONS_BEAM 17.6 M3)"
                )
    numerator, denominator = turn_rate
    off: list[tuple[str, int]] = []
    for family in families:
        if family.quantum == FREE_QUANTUM:
            continue
        gap = factor * family.quantum * numerator - LABEL_SCALE * width * denominator
        if gap:
            off.append((family.name, gap))
    if books and off:
        name, gap = off[0]
        raise ValueError(
            f"{BEAM_LAW}: {label}.books declares the exchange's accounting, and the paid family "
            f"{name!r} is off the identity d x h x n = Q x S x d_K by {gap} (DERIVATIONS_BEAM "
            "17.6 M7 and N5: the click's energy per content and the drive's rest energy per "
            "content must be one number)"
        )
    return CovariantDeclaration(c2, grain, books, tuple(off))


def covariant_square(
    content: int, momentum: Sequence[int], width: int, factor: int, grain: int, label: str
) -> int:
    """`W / g^2 = (E'_0 / g)^2 + d (p / g) . (p / g)` (DERIVATIONS_BEAM 17.6
    M3): the exact square of a body's energy in the identity's units at the
    grain g, `E'_0 = Q S M` the rest energy, the momentum's whole part over
    g per component (the bits below g do not enter), d the factor of the
    declared c^2 = [1, d]. Every product is tested by division before it is
    formed and refused beyond the integer bound naming the record."""
    rest = LABEL_SCALE * width * content // grain
    if rest > MOMENTUM_BOUND // max(rest, 1):
        raise OverflowError(
            f"{BEAM_LAW}: {label}: (E'_0 / g)^2 = {rest}^2 exceeds the integer bound "
            f"{MOMENTUM_BOUND} at the grain {grain} (a larger grain)"
        )
    square = rest * rest
    for axis, component in enumerate(momentum):
        part = abs(component) // grain
        if part > MOMENTUM_BOUND // max(part, 1) or part * part > MOMENTUM_BOUND // factor:
            raise OverflowError(
                f"{BEAM_LAW}: {label}: d x (p_{axis} / g)^2 = {factor} x {part}^2 exceeds the "
                f"integer bound {MOMENTUM_BOUND} at the grain {grain} (a larger grain)"
            )
        square += factor * part * part
        if square > MOMENTUM_BOUND:
            raise OverflowError(
                f"{BEAM_LAW}: {label}: W / g^2 exceeds the integer bound {MOMENTUM_BOUND} at the "
                f"grain {grain} (a larger grain)"
            )
    return square


def _record_load_checks(
    measured: tuple[MeasuredDefinition, ...],
    detectors: tuple[DetectorDefinition, ...],
    families: tuple[FamilyDefinition, ...],
    phase_steps: int,
) -> None:
    """The world's checks of the record form that need the measured events and
    the detectors together: a `phase_window` on a `rerelease` entry whose
    Node reads no `sum` set is dead (a split takes no gate; a `sum`
    re-emitter's window is its rotation's setting) and refused; the
    multiplicity a row can reach through every re-emitter of the world
    (each split's norm, each rotation's 65536, each gate's parties as the
    copies) is bounded by 2^62 - 1 in the product, refused at load before
    any row is formed (a sufficient bound: a path meets every re-emitter
    at most once; the run refuses a longer one at the split). Two guards,
    then: this static path ceiling at load, an acyclic count of the
    splits, rotations and gates on a path, and the run-time bound at the
    split (`nature_beam._release_family`, the row's multiplicity times the
    split's norm against the same bound); a cycle among re-emitters (two
    openings feeding each other, as the two slits 6 Links apart under the
    Huygens fan) is outside the acyclic count and is caught by the
    run-time bound alone, so the register's ceiling is a contract on
    acyclic paths (the auditor's round 8, 2026-09-21)."""
    sum_nodes = {
        position
        for detector in detectors
        if detector.reading == SUM_READING
        for position in detector.positions
    }
    product = 1
    for index, entry in enumerate(measured):
        for at, rule in enumerate(entry.table):
            if rule != "rerelease":
                continue
            window_declared = entry.windows[at] is not None or (
                entry.window_reads and entry.window_reads[at] is not None
            )
            if window_declared and entry.position not in sum_nodes:
                raise ValueError(
                    f"{BEAM_LAW}: measured[{index}].table[{families[at].name!r}].phase_window is "
                    f"dead: a split takes no gate, and the Node "
                    f"{list(entry.position)} reads no `sum` set whose window would be the "
                    "rotation's setting"
                )
            split = entry.splits[at] if entry.splits else None
            if split is not None:
                product *= max(sum(a * a for a in row) for row in split.weights)
            # A plain `rerelease` (the equal split by the directions' count)
            # is not in the product: a path's count of re-emissions is not
            # known at load, and the split's own check refuses the
            # multiplicity beyond the bound when it is formed (stage (vii)
            # step 4: the check runs on every world with a lamp).
            if entry.rotations and entry.rotations[at] is not None:
                product *= 256 * 256
            gate = entry.gates[at] if entry.gates else None
            if gate is not None:
                product *= 1 << gate.parties
            if product > MOMENTUM_BOUND:
                raise ValueError(
                    f"{BEAM_LAW}: the multiplicity through the re-emitters of the world reaches "
                    f"{product} at measured[{index}] at {list(entry.position)}, beyond the integer "
                    f"bound {MOMENTUM_BOUND} (the register's ceiling: fewer splits, rotations "
                    "or gates on a path)"
                )


def _aperture_load_check(
    measured: tuple[MeasuredDefinition, ...],
    families: tuple[FamilyDefinition, ...],
    detectors: tuple[DetectorDefinition, ...],
    table: tuple[Vector, ...],
    shape: Address3,
    periodic: tuple[bool, bool, bool],
) -> None:
    """The aperture's multiplicity, refused at load (issue #714). Two rows
    of one record add exactly at a set only when their multiplicities
    differ by a square factor (`amplitude.common_denominator`, the design's
    section 2.5); the run refuses any other meeting at the offer. A row's
    multiplicity is the lamp's (the paths per arm times the branches' norm)
    times the norm of every opening it was re-released at (a `rerelease`
    entry: the sum of its squared weights, the count of its directions
    where none is declared), and which openings a row meets is the
    GameBoard's geometry, known at load: an aperture two Nodes wide whose
    fan holds the direction along the aperture re-releases a row at one
    opening and its sibling at both, the second opening's norm between
    them (the frozen widths 3 and 5 of the batch of issue #661, refused at
    tick 13 with 201 against 201 x 67; the loader and the run agree on the
    meeting, the loader before tick 0). So the loader walks the record's
    paths: per family and per lamp, per arm (an offer is per arm), from
    each of the arm's directions Link by Link along the direction's digital
    line, the flight's own walk (`bresenham_line`; the periodic axes wrapped,
    a `pass` entry stepped through, at most X + Y + Z Links: a crossing of
    the GameBoard on every axis) to the first other measured event on the
    ray; an opening of the family multiplies the path's multiplicity by
    its norm on that arrival and the walk goes on from it over every
    direction its split can send the row on; the entry that emitted the
    row (the lamp, or the last opening) takes it home, no offer; any other
    measured event ends the path at its set (its detector's, else its
    own), the edge loses it.
    Two paths of one arm at one set whose multiplicities' ratio is not a
    square refuse the world, naming the rule, the two multiplicities, the
    openings of both paths, the ratio and the aperture's width (the
    openings that feed one another, counted). The paths are followed by
    the class of their multiplicity (equal classes at an opening are
    walked once), so a cycle of openings (the two slits feeding each other
    under a fan with the direction between them) ends. The run's check at
    the offer remains the guard for what the walk does not model: a world
    with a gate (records of several lamps joined), a rebirth, a body on
    several Nodes, a detector Node without a measured event."""
    if not any(entry.lamp is not None for entry in measured):
        return
    if any(gate is not None for entry in measured for gate in entry.gates):
        return
    at_position = {entry.position: index for index, entry in enumerate(measured)}
    set_of = {position: detector.name for detector in detectors for position in detector.positions}
    extents = (shape[0], shape[1], shape[2])
    reach = sum(extents)

    def ray(start: Address3, vector: Vector, family: int) -> int | None:
        """The index of the first measured event on the ray from `start`
        along the digital line of `vector` (the flight's own unit steps,
        `bresenham_line`) that is not a `pass` for the family, None where
        the ray leaves the GameBoard or `reach` Links pass none."""
        line = bresenham_line((vector[0], vector[1], vector[2]))
        if not line:
            return None
        x, y, z = start
        for j in range(reach):
            step = line[j % len(line)]
            x, y, z = x + step[0], y + step[1], z + step[2]
            if periodic[0]:
                x %= extents[0]
            if periodic[1]:
                y %= extents[1]
            if periodic[2]:
                z %= extents[2]
            if not (0 <= x < extents[0] and 0 <= y < extents[1] and 0 <= z < extents[2]):
                return None
            index = at_position.get((x, y, z))
            if index is not None and not _passes(measured[index], family):
                return index
        return None

    for at, family in enumerate(families):
        openings = {index for index, entry in enumerate(measured) if _re_releases(entry, at)}
        if not openings:
            continue
        feeds: dict[int, set[int]] = {index: set() for index in openings}
        for index in openings:
            for direction in _fed_directions(measured[index], at):
                reached = ray(measured[index].position, table[direction], at)
                if reached is not None and reached in openings and reached != index:
                    feeds[index].add(reached)
                    feeds[reached].add(index)
        for source, entry in enumerate(measured):
            lamp = entry.lamp
            if lamp is None or entry.family != at:
                continue
            ways = len(lamp.directions)
            paths = ways // lamp.arms
            multiplicity = paths * sum(weight * weight for _, weight in lamp.branches)
            for arm in range(lamp.arms):
                _walk_arm(
                    measured,
                    family.name,
                    at,
                    source,
                    lamp.directions[arm * paths : (arm + 1) * paths],
                    multiplicity,
                    openings,
                    feeds,
                    set_of,
                    table,
                    ray,
                )


def _walk_arm(
    measured: tuple[MeasuredDefinition, ...],
    family_name: str,
    family: int,
    source: int,
    directions: tuple[int, ...],
    multiplicity: int,
    openings: set[int],
    feeds: dict[int, set[int]],
    set_of: dict[Address3, str],
    table: tuple[Vector, ...],
    ray: Callable[[Address3, Vector, int], int | None],
) -> None:
    """The paths of one arm of a lamp's record through the openings to the
    sets (`_aperture_load_check`): refuses the world at the first set two
    paths reach with multiplicities whose ratio is not a square."""
    reached_sets: dict[str, tuple[int, tuple[int, ...]]] = {}
    walked: dict[int, list[int]] = {index: [] for index in openings}
    pending: list[tuple[int, int, tuple[int, ...]]] = []

    def arrive(index: int, direction: int, product: int, path: tuple[int, ...]) -> None:
        if index == (path[-1] if path else source):
            # Home: a row back at the entry that emitted it (its number)
            # is taken to be created again, not offered (`plan.home`).
            return
        if index in openings:
            norm = _split_norm(measured[index], family, direction)
            if norm is None:
                return
            product *= norm
            if any(_same_class(held, product) for held in walked[index]):
                return
            walked[index].append(product)
            pending.append((index, product, path + (index,)))
            return
        name = set_of.get(measured[index].position, f"the set of measured[{index}]")
        held = reached_sets.get(name)
        if held is None:
            reached_sets[name] = (product, path)
            return
        if _same_class(held[0], product):
            return
        common = gcd_of(held[0], product)
        aperture = _aperture_of(set(held[1]) | set(path), feeds)
        if any(feeds[index] for index in aperture):
            geometry = (
                f"an aperture {len(aperture)} Nodes wide: the openings at "
                f"{_positions(measured, tuple(sorted(aperture)))} feed one another"
            )
        else:
            geometry = "no opening feeds another: the openings are fed apart"
        raise ValueError(
            f"{BEAM_LAW}: two paths of one record of {family_name!r} from the lamp "
            f"measured[{source}] at {list(measured[source].position)} reach {name} with "
            f"the multiplicities {held[0]} (through the openings at "
            f"{_positions(measured, held[1])}) and {product} (through "
            f"{_positions(measured, path)}), whose ratio {held[0] // common}:{product // common} "
            f"is not a square ({geometry}); two paths of one record add exactly at a set only "
            "when their multiplicities differ by a square factor (amplitude-v1, the design's "
            "section 2.5), so the run would refuse the record at that set: declare weights "
            "whose squares sum to a square, or open the aperture one Node wide"
        )

    position = measured[source].position
    for direction in directions:
        reached = ray(position, table[direction], family)
        if reached is not None:
            arrive(reached, direction, multiplicity, ())
    while pending:
        index, product, path = pending.pop()
        for direction in _fed_directions(measured[index], family):
            reached = ray(measured[index].position, table[direction], family)
            if reached is not None:
                arrive(reached, direction, product, path)


def gcd_of(a: int, b: int) -> int:
    """Euclid on Python integers (the loader's exact products)."""
    while b:
        a, b = b, a % b
    return a


def _same_class(held: int, arriving: int) -> bool:
    """Whether two multiplicities differ by a square factor: their product
    is a square (`amplitude.common_denominator` finds their denominator)."""
    product = held * arriving
    return math.isqrt(product) ** 2 == product


def _positions(measured: tuple[MeasuredDefinition, ...], path: tuple[int, ...]) -> list[list[int]]:
    return [list(measured[index].position) for index in path]


def _aperture_of(openings: set[int], feeds: dict[int, set[int]]) -> set[int]:
    """The openings that feed one another, from `openings` outward (the
    component of the feeding graph): the aperture."""
    found = set(openings)
    pending = list(openings)
    while pending:
        index = pending.pop()
        for other in feeds.get(index, ()):
            if other not in found:
                found.add(other)
                pending.append(other)
    return found


def _re_releases(entry: MeasuredDefinition, family: int) -> bool:
    """Whether the entry re-releases rows of the family (an opening)."""
    return family < len(entry.table) and entry.table[family] == "rerelease"


def _passes(entry: MeasuredDefinition, family: int) -> bool:
    """Whether the entry lets rows of the family pass (`pass`)."""
    return family < len(entry.table) and entry.table[family] == "pass"


def _fed_directions(entry: MeasuredDefinition, family: int) -> tuple[int, ...]:
    """The directions of the table an opening's split can send a row of
    the family on: every declared direction under a plain `rerelease`
    (every weight 1), those with a positive weight in some row of the
    declared split."""
    split = entry.splits[family] if entry.splits else None
    if split is None:
        return entry.directions
    return tuple(
        direction
        for k, direction in enumerate(entry.directions)
        if any(row[k] > 0 for row in split.weights)
    )


def _split_norm(entry: MeasuredDefinition, family: int, arrival: int) -> int | None:
    """The norm an opening multiplies the multiplicity of a row of the
    family arriving on `arrival` by: the sum of its squared weights, the
    count of its directions under a plain `rerelease`; None where the
    split declares `inputs` that do not name the arrival (the run refuses
    that row by its own message)."""
    split = entry.splits[family] if entry.splits else None
    if split is None:
        return len(entry.directions)
    chosen = split.row(arrival)
    if chosen is None:
        return None
    weights, _ = chosen
    return sum(a * a for a in weights)


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
                        "largest label flow of one self-creation's release read over the reader's "
                        "Nodes)"
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


def _massive_families(
    families: tuple[FamilyDefinition, ...],
    measured: tuple[MeasuredDefinition, ...],
    table: tuple[Vector, ...],
    width: int,
    phase_steps: int,
    action: int | None,
) -> tuple[FamilyDefinition, ...]:
    """The magnitude p of every massive family's momentum label, resolved
    from its lamps (`momentum_magnitude`; one table per family, so every
    lamp of the family declares the one value, and a massive family without
    a lamp is refused: nothing else births its rows), and the ceilings of
    its tables at load (`massive-rows-v1`, the design's section 1): the
    rest energy E'_0 = Q S M and, on every direction D of the world's table
    with the label p_D at the scale p (`scaled_label`), the square E'_D^2 =
    E'_0^2 + 3 p_D . p_D and the turn's rate |p_{D,a}| x N per axis, each
    within 2^62 - 1, refused naming the family and the direction. Returns
    the families with the magnitude on each massive one."""
    found = list(families)
    for index, family in enumerate(families):
        if not family.massive:
            continue
        magnitudes = sorted(
            {
                entry.lamp.momentum_magnitude
                for entry in measured
                if entry.family == index
                and entry.lamp is not None
                and entry.lamp.momentum_magnitude is not None
            }
        )
        if not magnitudes:
            raise ValueError(
                f"{BEAM_LAW}: the massive family {family.name!r} has no lamp: its momentum label's "
                "magnitude p is its lamp's `momentum_magnitude`, one table per family"
            )
        if len(magnitudes) > 1:
            raise ValueError(
                f"{BEAM_LAW}: the lamps of the massive family {family.name!r} declare two "
                f"momentum_magnitude values {magnitudes}: one table per family, one p"
            )
        p = magnitudes[0]
        assert action is not None
        # The label's rounding forms (2 p |a|)^2 within the working bound
        # (`scaled_label`, one integer root per direction): bounded here
        # before it is formed, naming the key.
        reach_table = max((abs(c) for vector in table for c in vector), default=1)
        if (2 * p * reach_table) ** 2 > MAX_WORK_INT:
            raise ValueError(
                f"{BEAM_LAW}: the massive family {family.name!r}: momentum_magnitude {p} forms "
                f"(2 p |a|)^2 = (2 x {p} x {reach_table})^2 beyond the working bound "
                f"{MAX_WORK_INT} in the label's rounding (p at most {integer_root(MAX_WORK_INT) // (2 * reach_table)})"
            )
        rest = LABEL_SCALE * width * family.quantum
        if rest * rest > MOMENTUM_BOUND:
            raise ValueError(
                f"{BEAM_LAW}: the massive family {family.name!r}: the rest energy E'_0 = Q S M = "
                f"{LABEL_SCALE} x {width} x {family.quantum} = {rest} has a square beyond the "
                f"integer bound {MOMENTUM_BOUND} (the pace wall E'_D is formed from it)"
            )
        for vector in table:
            label = scaled_label(vector, p)
            square = rest * rest + 3 * sum(c * c for c in label)
            if square > MOMENTUM_BOUND:
                raise ValueError(
                    f"{BEAM_LAW}: the massive family {family.name!r} on the direction "
                    f"{list(vector)}: E'_D^2 = E'_0^2 + 3 p_D . p_D = {square} exceeds the integer "
                    f"bound {MOMENTUM_BOUND} (a smaller quantum, width or momentum_magnitude)"
                )
            reach = max(abs(c) for c in label)
            if reach * phase_steps > MOMENTUM_BOUND:
                raise ValueError(
                    f"{BEAM_LAW}: the massive family {family.name!r} on the direction "
                    f"{list(vector)}: the turn's rate |p_a| x N = {reach} x {phase_steps} exceeds "
                    f"the integer bound {MOMENTUM_BOUND} (a smaller momentum_magnitude or N)"
                )
        found[index] = replace(family, momentum_magnitude=p)
    return tuple(found)


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
        # The row's hand (`hand-v1`): the family's, or declared on a row of
        # a family without one; a chiral family's row takes the family's.
        hand = families[family].hand
        if "hand" in obj:
            declared_hand = _hand(obj["hand"], f"{label}.hand")
            if hand and declared_hand != hand:
                raise ValueError(
                    f"{BEAM_LAW}: {label}.hand {declared_hand:+d} differs from the hand {hand:+d} of "
                    f"the family {family_name!r}: a chiral family's row carries the family's hand"
                )
            hand = declared_hand
        found.append(
            TransitDefinition(
                _address(obj["position"], f"{label}.position", shape),
                family,
                _integer(obj["number"], f"{label}.number", 1, max(1, len(measured))),
                direction,
                amount,
                _integer(obj.get("phase", 0), f"{label}.phase", 0, top),
                age,
                hand=hand,
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
        if name.startswith(RESERVED_SET_PREFIX) or name in FACE_NAMES or name == LIFETIME_NAME:
            raise ValueError(
                f"{BEAM_LAW}: {label}.name {name!r} is reserved: the layer names the measured "
                f"events outside every detector `{RESERVED_SET_PREFIX}<number>`, the faces and "
                "the border by their own names"
            )
        reading = obj.get("reading", DETECTOR_READINGS[0])
        if reading not in DETECTOR_READINGS and reading != SUM_READING:
            raise ValueError(
                f"{BEAM_LAW}: {label}.reading must be one of "
                f"{[*DETECTOR_READINGS, SUM_READING]}, not {reading!r}"
            )
        found.append(DetectorDefinition(name, tuple(positions), threshold, str(reading)))
    return tuple(found)


def _optical(
    value: object,
    suspension: tuple[int, int],
    meeting: bool,
    table: tuple[Vector, ...],
    massive_rows: bool = False,
) -> int:
    """The world key `optical`: gamma, the declared post-Newtonian
    parameter of the row's flight in the age wall's set (the generic entry
    of the bending, the model owner's word of 2026-09-22, record 847;
    docs/designs/one_wall/EVERY_FAMILY.md section 6, step 5): a
    non-negative integer (a boolean, a float, a string or a negative
    integer refused), 0 when absent (the time part alone, the law's own
    number; nature's 1 is a declaration per world and never a default,
    record 817). The coupling is the law's for every world: since the
    stretch is n / d times the crowd's age moment and the push is n times
    the crowd's flow, a world at `suspension` [0, d] or with no crowd walks
    integer for integer as before (the refusals of optical-v1 at
    suspension 0, with `meeting` and for a heading without a neighbour are
    lifted: under `meeting` the meeting's turn keeps the heading and the
    stretch stays, one turn verb per row; a heading without a neighbour
    turns to nothing, `nature_beam.optical_turn`). The other refusals of
    the note (a wall, a weight or a momentum beyond the register) are the
    run's, tested by division before the product is formed."""
    del suspension, meeting, table, massive_rows
    if value is None:
        return 0
    if type(value) is not int or value < 0:
        raise ValueError(
            f"{BEAM_LAW}: optical must be a non-negative integer, gamma the post-Newtonian "
            f"parameter (nature's 1), not {value!r}"
        )
    return value


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
            "tools/migrate_nature_beam_worlds.py of git before e4b649a0, deleted on 2026-09-20 "
            "(docs/MIGRATION.md, \"The names NatureBeam and GameBoard and the glossary's single "
            'names, on 2026-09-20")'
        )
    if document.get("law") != LAW_VALUE:
        raise ValueError(f'{BEAM_LAW}: a world of the Beam Law declares "law": "beam"')
    events = [key for key in EVENTS_KEYS if key in document]
    if events:
        raise ValueError(
            f"{BEAM_LAW}: a world of the Beam Law declares none of the law of events' keys "
            f"({', '.join(events)}); see docs/MIGRATION.md"
        )
    if DELETED_AMPLITUDE_KEY in document:
        # The world key `amplitude` is deleted (stage (vii) step 4, the one
        # click): the record form is the law.
        raise ValueError(
            f"{BEAM_LAW}: the world key {DELETED_AMPLITUDE_KEY!r} is deleted: the record form is "
            "the law and every lamp births records; remove the key (docs/MIGRATION.md, the "
            "amplitude law (vii-4))"
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
    # The massive rows (`massive-rows-v1`): true or false, false by default;
    # with it the world declares its `age_bound` (a massive row's pace is
    # its family's, |p| / E', not the flight's, so the flight bound is not
    # its bound).
    massive_rows = obj.get("massive_rows", False)
    if type(massive_rows) is not bool:
        raise ValueError(f"{BEAM_LAW}: massive_rows must be true or false")
    if massive_rows and "age_bound" not in obj:
        raise ValueError(
            f"{BEAM_LAW}: age_bound is required with the world key `massive_rows`: a massive "
            "row flies at its family's pace |p| / E', below the flight's, so the default bound "
            "(twice the flight bound) is not its bound; declare the largest age a row may carry"
        )
    age_bound = _age_bound(obj.get("age_bound"), shape, periodic, table)
    # The quantum of action of the turn by momentum, h: absent by default
    # (nothing turns by momentum), an integer from 1 when declared.
    action = None if "action" not in obj else _integer(obj["action"], "action", 1)
    declared = obj.get("measured", [])
    if phase_steps < AMPLITUDE_LEAST_STEPS and any(
        isinstance(entry, dict) and "lamp" in entry
        for entry in (declared if isinstance(declared, list) else [])
    ):
        # A record's circle holds the quarter turn of a reflection (the
        # amplitude law; every lamp births records). Read off the document
        # before the measured events are parsed, so that this refusal
        # precedes theirs (`tests/test_amplitude_record.py` (b)).
        raise ValueError(
            f"{BEAM_LAW}: a lamp is refused with N {phase_steps}: a record's circle holds the "
            f"quarter turn of a reflection, at least {AMPLITUDE_LEAST_STEPS} steps"
        )
    families = _families(obj["families"], phase_steps, age_bound, massive_rows, action)
    # The meeting: true or false (false by default); under it a paid family
    # without a phase circle is refused, the phase being the register the
    # meeting reads the crowd into (there is no other on the record).
    meeting = obj.get("meeting", False)
    if type(meeting) is not bool:
        raise ValueError(f"{BEAM_LAW}: meeting must be true or false")
    if meeting:
        for family in families:
            if not family.free and not family.phase:
                raise ValueError(
                    f"{BEAM_LAW}: meeting is refused with the paid family {family.name!r} without a "
                    "phase circle: the meeting turns a unit in transit by its phase register (the "
                    "crowd met is added to the phase, one grain step per wrap of the circle), and "
                    "a phase-less family has no register to read the crowd into"
                )
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
    families = _massive_families(families, measured, table, width, phase_steps, action)
    # The covariant readings (`covariant-readings-v1`): the key as declared,
    # its domain and its integers checked at load, None by default.
    # drive-b-v1 (2026-09-22): the world key `drive_b`, a boolean, false by
    # default; under it every free body's wall is tested at load.
    drive_b = obj.get("drive_b", False)
    if type(drive_b) is not bool:
        raise ValueError(f"{BEAM_LAW}: drive_b must be true or false (drive-b-v1, off by default)")
    if drive_b:
        for entry in measured:
            if not entry.fixed:
                drive_wall(entry.momentum, sum(entry.held), width, obj.get("covariant_readings") is None)
    # centred-step-v1 (2026-09-22): the world key `centred_step`, a boolean,
    # false by default (docs/designs/atom_give/CENTRED_STEP.md section 1).
    centred_step = obj.get("centred_step", False)
    if type(centred_step) is not bool:
        raise ValueError(
            f"{BEAM_LAW}: centred_step must be true or false (centred-step-v1, off by default)"
        )
    # atom-level-v1 (2026-09-22): the world key `atom_level`, a boolean,
    # false by default, and the bodies' `level` declarations under it
    # (docs/designs/atom_levels/LEVELS.md section 2 (b) and (c)).
    atom_level = obj.get("atom_level", False)
    if type(atom_level) is not bool:
        raise ValueError(f"{BEAM_LAW}: atom_level must be true or false (atom-level-v1, off by default)")
    measured = _atom_levels(obj["measured"], measured, families, atom_level, action, ticks)
    covariant = _covariant(
        obj.get("covariant_readings"), measured, families, width, turn_rate, action, drive_b
    )
    in_transit = _in_transit(
        obj.get("in_transit", []), shape, families, measured, phase_steps, table, age_bound
    )
    detectors = _detectors(obj.get("detectors", []), shape, periodic, measured)
    optical = _optical(obj.get("optical"), suspension, meeting, table, massive_rows)
    # Every family under one wall, step 3: a moving body under the wall
    # (the law's own since the generic entry of 2026-09-22).
    for index, entry in enumerate(measured):
        if entry.fixed or not any(entry.momentum):
            continue
        if optical > 0 and not drive_b:
            # Every family under one wall, step 3 (2026-09-22): a moving
            # body at gamma > 0 walks by form B's directional drive, the
            # member of the age wall's set at gamma; the per-axis drive of
            # note 17 is never a member (REVIEW_3 must-fix 2 and 3). At
            # gamma 0 the member is declared at 0 and nothing is stretched.
            raise ValueError(
                f"{BEAM_LAW}: measured[{index}]: a moving body at gamma {optical} needs the "
                "key drive_b (form B's directional drive, the member of the age wall's set; "
                "the per-axis drive is never a member, docs/designs/one_wall/BODY_DRIVE.md)"
            )
        if drive_b:
            body_weight(entry.momentum, sum(entry.held), width, optical)
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
        meeting=meeting,
        massive_rows=massive_rows,
        covariant=covariant,
        optical=optical,
        drive_b=drive_b,
        centred_step=centred_step,
        atom_level=atom_level,
    )
    _record_load_checks(measured, detectors, families, phase_steps)
    _aperture_load_check(measured, families, detectors, table, shape, periodic)
    # The push's denominator per column, Lambda_c^2 (`measured.counts_table`),
    # tested where Lambda_c is formed (`column_scales`): a world whose column
    # scales leave the register is refused here, at load, not at its first
    # push (the physics-rule review of the branch, REVIEW.md section 4).
    _ = world.column_scales
    return world
