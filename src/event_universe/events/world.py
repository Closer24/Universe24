"""The world file of the engine: its keys and their refusals (one engine, no law's
name and no version, ALGEBRA.md 9.90 (1); the world keys `law`, `model_id` and
`detector_law` refused by name).

A world is a JSON object with nothing of the earlier engines' schemas (no
`contents`, no `initial_shadows`, no `wait_per_quantum`, no `dynamics`; none of
the old engine's keys): the refusal names the key at fault. What a world declared
under the ray law, cancelled (docs/CANCELLED_WORLDS.md; [the Beam Law](../../../docs/BEAM_LAW.md),
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
  paid family is given by a transformation or declared in transit), and
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
  giving wheel's rate, required: u = ordinal x r mod W the record's coordinate on
  the ladder, [1, N] the count of givings mod N, BEAM_LAW note 46; `rate` `[n, d]` units
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
  products are given at that self-creation as pending rows (product k on
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
  transformation fires, its products given at the reader's next
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
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from functools import cached_property
from typing import NamedTuple

from event_universe.core.game_board import MAX_VALUE, PORT_HEADINGS, Address3
from event_universe.core.integer import (
    MAX_WORK_INT,
    bounded_gcd,
    by_clock,
    integer_root,
    rational_sum,
)
from event_universe.core.phase import MAX_PHASE_STEPS
from event_universe.core.readings import Reading, world_readings
from event_universe.core.rule3 import rule_total_bound
from event_universe.core.step import STEP_FILE, Step

# ONE ENGINE, NO LAW'S NAME AND NO VERSION (ALGEBRA.md 9.90 (1); the model owner's
# records 2103 and 2107; the cancel of docs/CANCELLED_WORLDS.md section 9): the
# constants BEAM_LAW ("beam-v1"), LAW_VALUE ("beam") and OLD_LAW_VALUE ("rays") are
# CANCELLED; the world keys `law` and `model_id` are refused by name (RETIRED_KEYS);
# a refusal names the file and the key, never a law
TABLES = ("read", "measure", "rerelease", "pass", "become")
# The rule of the transformation (the weak force, 2026-09-20): the click
# and then the change of family with the products released.
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
# The emitter's norm T, one period's action P e_c in the flux's units (ALGEBRA.md
# 9.17 (7) (e) and (f), 9.19 (3)), is quadratic in the record's levels times the
# family's wall: at the registered amplitude 50 x 2^20 it passes 2^62. It is
# admitted up to this bound; the engine's form and running total are exact
# Python integers (the object arrays of `form_share`).
NORM_BOUND = (1 << 126) - 1
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
    # THE FILE'S STAMP (the model owner's record 1886; ALGEBRA.md 9.22 (7) (i),
    # 9.90 (3) (c)): the digest of the whole file the generator wrote
    # (`input_stamp`); no law identifier (9.90 (1))
    "stamp",
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
    "clock_stamp",
    # THE FACE SLAB (ALGEBRA.md 9.25 (10); BUILD.md section 26 item 23): the
    # depth of the face receiver at every open border, 1 by default
    "face_depth",
    # detector-law-v1 (2026-09-23): the local detector law, a boolean, false
    # by default (docs/designs/detector_law/DESIGN.md).
    "detector_law",
    # THE ENGINE START FILE (the model owner's record 2089 of 2026-09-25
    # through the Boss, "every flag the engine needs for a run should leave
    # the code"; records 2092 and 2094; ALGEBRA.md 9.83 (2) (a); BUILD.md
    # section 26 item 57): the repository path of the one start file, REQUIRED
    # under `detector_law`, refused without it; the file holds the run's
    # parameters (`mode`), every key required, none defaulted
    "engine",
    # massive-record-v1 (2026-09-23): the massive record kind beside light
    # under the local detector law, a boolean, false by default
    # (docs/designs/detector_law/MASSIVE_RECORD.md,
    # the build's plan BUILD.md).
    "massive_record",
    # THE BODY RECORD (ALGEBRA.md 9.46; BUILD.md section 26 item 37): every
    # seeded block held as one rotation (a, b, r) on its clock pair, its
    # profile stored and never stepped, its own rows off the GameBoard;
    # false by default (the lattice body); a host form under its own
    # identity, gated by the equivalence test of 9.46 (4)
    "body_record",
    # `point_emitter` RETIRED (commit 7): the window is the law's one giving
    # (ALGEBRA.md 9.85 (5), 9.91 (10) 7), the key refused by name (RETIRED_KEYS)
    # massive-record-v1: `probes`, declared Nodes whose light amplitude the
    # record writes per interval (a GAMEBOARD reading of the rows), a list
    # of Nodes, admitted under `massive_record` alone.
    "probes",
    "readings",
    # massive-record-v1: `mode_axis`, the axis ("x", "y" or "z") along which
    # the record writes the `mode` line per interval (the three sums of
    # light's total field over the Nodes of each residue class of that
    # coordinate modulo 3, the content of the mode k = 2 pi / 3, a GAMEBOARD
    # reading of the hop pump's signature, MASSIVE_RECORD.md section 7),
    # absent by default, admitted under `massive_record` alone.
    "mode_axis",
    # massive-record-v1 (DECLARATIONS.md section 15 M1-10; issue #1085): the
    # world key `amplitude_bound`, the amplitude A every row of a massive
    # world stays below, declared per world (no default: a massive world
    # without it is refused); MUST 3's load bound at that A, the seed and a
    # profile's largest magnitude refused above it, the rows asserted below
    # it at every interval.
    "amplitude_bound",
    # THE NODE CLOCK (the model owner's decision (5) of record 1962; ALGEBRA.md
    # 9.35 (2) and (3); BUILD.md section 26 item 31): the world key
    # `node_clock`, Gamma, the one integer of the clock pair (e, f) = (Gamma,
    # Gamma + M) at every Node, M the content held at the Node; required
    # under `detector_law` (no default), refused without it.
    "node_clock",
    # THE MOMENTUM'S UNIT Q (ALGEBRA.md 9.96 (1), 9.89 (2)): the universe's integer
    # `momentum_unit`, the wall W = 3 Q M of every body; required under
    # `detector_law` (no default), refused without it.
    "momentum_unit",
    # THE TWIST TABLE (ALGEBRA.md 9.81 (2) (b), 9.96 (2) (c)): the universe's table of
    # exact triples for the transport's angles, the families file's; admitted as a
    # world key on an inline world alone.
    "twist_table",
    # THE FAMILY GENERICITY (the model owner's record 2066 of 2026-09-25
    # through the Boss; BUILD.md section 26 item 51): the world keys
    # `clock_family`, `charge_family` and `charge_strength` of items 32 and
    # 35 are RETIRED (`RETIRED_KEYS`): what a family is stands in its own
    # entry of `families` (`held`, `reads`, `booked`, `components`), and the
    # engine knows no family's name or role.
    # The covariant readings (`covariant-readings-v1`, 2026-09-21): one
    # object, absent by default (`COVARIANT_KEYS`).
    "covariant_readings",
    # optical-v1 (2026-09-21): the world's post-Newtonian parameter gamma,
    # a non-negative integer, absent by default (`"optical"`).
    "optical",
    # drive-b-v1 (2026-09-22): the directional drive of a body, a boolean,
    # false by default (`"drive-b"`).
    "drive_b",
    # flow-link-v1 (2026-09-22): one arrival counts one Euclidean Link of
    # its line, a boolean, false by default (`"flow-link"`).
    "flow_link",
    "atom_level",
    # centred-step-v1 (2026-09-22): the body's step at half the wall, a
    # boolean, false by default (`"centred-step"`).
    "centred_step",
    "directions",
    "direction_bound",
    # THE UNIVERSE (record 2128 (3)): the universe file's path, or the families'
    # list inline in a unit test's world; the word `families` is the file's own.
    # The ray law's world (a cancelled path, loaded for the record and never run
    # by the gate) keeps its word `families` for its inline list
    "universe",
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
            f"drive-b: the wall's rest term Q^2 S M = {scale} x {content} exceeds "
            f"the integer bound {MOMENTUM_BOUND}"
        )
    rest = scale * content
    if not cap:
        return rest
    if manhattan > MOMENTUM_BOUND // T_HEADING or rest > MOMENTUM_BOUND - manhattan * T_HEADING:
        raise OverflowError(
            f"drive-b: the wall Q^2 S M + |p|_1 T_h = {rest} + {manhattan} x "
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
            f"optical: the body's rest energy Q S M = {rest} squared exceeds "
            f"the working bound {MAX_WORK_INT} (the weight of a moving body under optical)"
        )
    square = rest * rest
    for component in momentum:
        c = abs(int(component))
        if c and c > ((MAX_WORK_INT - square) // 3) // c:
            raise OverflowError(
                f"optical: the body's energy square (Q S M)^2 + 3 p . p with "
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
# The identity of the one mechanism of the columns (the model owner,
# 2026-09-20, "one mechanism for all the laws on the GameBoard"; the
# mathematician's verified form): the record carries it when a world
# declares a column beyond `charge`. The two built-in columns, gravity
# and charge, are the law as it was, integer by integer.
# The identity of the transformation `become` (the weak force in the
# world's terms, the model owner's "go on everything", 2026-09-20): the
# record carries it when a measured event declares `become` or a table
# entry's rule is `become`.
# The identity of the meeting (the model owner, 2026-09-20, "DECIDED: the
# meeting, M-R": an event in transit reads the crowd as a body does, a
# report; `events/meeting.py`): the record carries it when the world
# declares `meeting: true`; absent, no paid unit reads the crowd and every
# world reads as it did, byte for byte.
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
# The identity of the flow label (`flow-link-v1`; the model owner's decision of
# 2026-09-22, record 915 of docs/LOG_2026-09-20.md, on the Flow Weight
# Designer's design docs/designs/flow_weight/DESIGN.md, the physics-rule
# reviewer's ADMISSIBLE of record 902): under the world key `flow_link` (a
# boolean, absent by default) the arrival flow every reader sums counts each
# arriving row of direction D with the flow label f_D, the integer vector
# nearest |p_D| D / S_1 (the label per Euclidean Link of the line, S_1 = |a| +
# |b| + |c| the line's Nodes per period), in place of the unit label u_D, the
# integer vector nearest |p_D| D / |D| (the label per Node); |p_D| is Q for
# the photon and a massive family's `momentum_magnitude`. Formed once at load
# by one Euclidean division per component (`nature_beam.flow_label`), read
# by the flow's sums alone (`nature_beam.CrowdMoments`, a body's push through
# the group moment of a free family's rays); the age moment, the wall, the
# flight, the collision, the phase and the momentum a click moves untouched.
# Absent, the flow labels are the labels and every world reads as it did,
# byte for byte.
# The identity of the hand (`hand-v1`; the model owner, 2026-09-20, record
# 128 of docs/LOG_2026-09-20.md, "the hand's three choices confirmed"; the
# physicist's design hand/DESIGN.md with the mathematician's FORM.md; BEAM_LAW
# note 39): the record carries it when a family, a lamp, a transit row or a
# table entry declares `hand`, a lamp's `branches` name the hands of their
# labels, or a measured event declares an `axis`. Absent, no row carries a
# hand and every world reads as it did, byte for byte.
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
# The identity of the local detector law (the model owner's words of
# 2026-09-23, docs/designs/detector_law/DESIGN.md): the ray splits at every
# free Node inside the board and holds its amplitudes; outside only clicks
# through a detector. The record carries it when the world declares
# `detector_law: true`; absent, the ray law as built runs unchanged.
# The identity of the massive record kind (the chief physicist's design of
# 2026-09-23, docs/designs/detector_law/MASSIVE_RECORD.md, on the model
# owner's words of records 1381 to 1425): a second record kind beside light
# under the local detector law, its rule the same six-neighbour step with
# a declared pair [num, den] on the six-neighbour term (a gap, its rest
# mass); a family declares the kind by the key `pair`; its faces are the
# world's `boundary`, ONE BORDER FOR EVERY FAMILY (the family key `faces`
# refused by name since 2026-09-25, BUILD.md section 26 item 28). The
# record carries the identity when the world declares
# `massive_record: true`; absent, every world reads as it did, byte for
# byte.
# The amplitude bound A of a record's row under the massive record kind
# (Reviewer 3's MUST 3 on step 2; BUILD.md section 3): the rule's total at a
# Node under the Node clock, Gamma x num x 6 x A + 6 x den x M x A + 3 x
# den x (Gamma + M) x (A + 1), must stay below 2^63 for every declared pair
# with the world's Gamma and its whole content M, checked at load; the
# ceiling A = 2^28 (the model owner's decision (5) of record 1962; BUILD.md
# section 26 item 31: at Gamma = 10^6 on the pair [3200, 3236] the total is
# 7.8 x 10^18, below 2^63 = 9.2 x 10^18; the rows' amplitudes stay at the
# seed's order, the pointers alone square them, as Python integers; the
# 2^40 of MUST 3 was the plain rule's ceiling, HISTORY).
AMPLITUDE_BOUND = 1 << 28
TOTAL_BOUND = 1 << 63
# Light's kind: the pair [1, 1] on the six-neighbour term, the value every
# family without a declared pair reads (no branch on a name).
MASSLESS_PAIR = (1, 1)
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
# The two built-in columns of every family: the first, gravity, has the
# value [1, 1] on every unit of content and the sign minus (like contents
# pull together); the second, charge, the family's `charge` per unit of
# content and the sign plus (like charges push apart). Neither is declared
# under `columns`.
# CANCELLED (docs/CANCELLED_WORLDS.md section 9; ALGEBRA.md 9.90 (1)): the ray law's columns, the only family names in the loader (read by the cancelled parse alone)
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
    # massive-record-v1: the kind's pair [num, den] on the six-neighbour
    # term, admitted under the world key `massive_record` alone; `faces`
    # (a kind's own border per axis, HISTORY) is refused by name: one
    # border for every family, the world's `boundary` (BUILD.md section
    # 26 item 28)
    "pair",
    "faces",
    # THE REPRESENTATION AS A LIST OF PARTS and the rest of the complete
    # attribute set (ALGEBRA.md 9.86 (3), 9.91 (7); the one stroke, commit 1):
    # `parts`, `levels`, `self_unit`, `clicks`, and the held source's
    # `held_factors`, `held_dipole`, `held_dipole_div`; the families file's
    # entries translate to these, an inline list may declare them
    "parts",
    "levels",
    "self_unit",
    "clicks",
    "held_factors",
    "held_dipole",
    "held_dipole_div",
    # THE FAMILY GENERICITY (record 2066; BUILD.md section 26 item 51): what
    # a family is, declared on the family and read by the engine as
    # attributes alone, admitted under `detector_law`: `held` (the source a
    # body's record writes at its Nodes: "content" or "sign"), `reads`
    # (the held levels that enter the family's pace, with their weights),
    # and `components` (1 today; 3 and 6 with the vector and tensor
    # families of ALGEBRA.md 9.77); `booked` HISTORY (item 53: derived, a held
    # family is never booked and every other family is)
    "held",
    "reads",
    "components",
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
# CANCELLED (docs/CANCELLED_WORLDS.md section 9; ALGEBRA.md 9.90 (1)): the ray law's legacy charge key (read by the cancelled parse alone)
CHARGE_KEY = "charge"
# The charge per unit of content of a family with none: 0 as the pair [0, 1].
NO_CHARGE = (0, 1)
# The block's keys (massive-record-v1, MASSIVE_RECORD.md sections 4 to 7;
# the build's plan BUILD.md section 3): admitted on a measured event that
# declares `side`, under the world key `massive_record` alone.
# THE OWNER'S CONSTANT: at most twenty families on a GameBoard (the model
# owner's record 2081 of 2026-09-25 through the Boss, "lift the cap, put it at
# 20": every family works in every experiment; record 1875's three, 1982's
# four and 9.48's five HISTORY; BUILD.md section 26 item 54)
MOST_FAMILIES = 20
# THE ONE FAMILIES FILE (ALGEBRA.md 9.83 (2), 9.85 (3), 9.79 (1); the model owner's
# record 2075 through the Boss; BUILD.md section 26 item 59): the universe's
# families as laws and the universe's integers, one canonical copy at
# examples/events/families.json, referenced by every world of the detector law
# as the value of `families` (its repository path); a world may instead list
# its families inline (the unit tests' small lists, the owner's decision 2 of
# record 2081). The file: {"law", "integers": {"node_clock", "amplitude_bound"},
# "families": [entries]}; an entry: name, quantum, charge, pair, reads,
# representation ("scalar"; the vector and tensor parts ride on 9.86), phase
# (2, the two levels), self_unit (0, the self-source off), booked, and either
# held {"count": "content" | "sign", "factor": 1} (a field family) or clicks
# {"gives", "takes"} (a family of records); every key required, refused by
# name when missing; booked must be the derivation's (false for a held
# family, true otherwise). Under the file the world declares no node_clock and
# no amplitude_bound (the universe's integers, one copy) and every emitter
# declares its given clock (a light record's clock is its emitter's, 9.85 (3)).
# THE UNIVERSE FILE (the Boss's record 2128 (3); ALGEBRA.md 9.90 (6) read UNIVERSE): what
# repeats in every experiment, the families and the universe's integers; no `law` key,
# no name and no version (one engine)
FAMILIES_FILE_KEYS = {"integers", "families"}
# THE UNIVERSE'S INTEGERS (ALGEBRA.md 9.83 (2) (a), 9.91 (7)): Gamma, A, Lambda
# (the charge's read weight, the word "Lambda" on a read) and Q (the momentum's
# unit, `momentum_unit`: the wall of every body is W = 3 Q M, ALGEBRA.md 9.96
# (1), 9.89 (2)); the energy unit P_0 and the twist table enter with the
# operations that read them (9.91 (10) commits 4 and 5)
FAMILIES_INTEGERS = {"node_clock", "amplitude_bound", "Lambda", "momentum_unit"}
# THE TWIST TABLE in the integers block (ALGEBRA.md 9.81 (2) (b), 9.96 (2) (c), (d)):
# {unit, fine, coarse}; `unit` the integer 4 Gamma 2^16 whose inverse is theta_unit in
# radians; `fine` 2^10 triples (c, s, d) for the angles k_0 theta_unit; `coarse` at most
# 2^15 triples for the angles k_1 2^10 theta_unit; every triple c^2 + s^2 = d^2 exactly,
# d at most 10^9, the nearest the generator finds (`twist_triple`); the transport's
# triple for k = k_1 2^10 + k_0 is their exact product.
FAMILIES_TABLES = {"twist_table"}
TWIST_UNIT_SCALE = 1 << 16
TWIST_FINE_BITS = 10
TWIST_COARSE_MOST = 1 << 15
TWIST_TRIPLE_BOUND = 10**9
# THE ENTRY, the complete attribute set (ALGEBRA.md 9.79 (1), 9.86 (3), 9.91
# (7)): name; parts (the representation as a list of parts, [1] a scalar, [1,
# 3] a vector with its time part, [1, 3, 6] the symmetric tensor over the
# four directions); phase (1 or 2, the levels at a Node); pair ([num, den], or
# "body" for the family whose pair every body and record declares); held
# {count, factors, dipole, dipole_div} (a field family: the body's writes);
# reads [{family, weight, twist, by}]; self_source {unit}; clicks {gives,
# takes, quantum} (a family of records). `booked` is derived: true exactly
# for a family with clicks (item 53).
FAMILY_ENTRY_KEYS = {"name", "parts", "phase", "pair", "held", "reads", "self_source", "clicks"}
FAMILY_ENTRY_REQUIRED = {"name", "parts", "phase", "pair", "reads", "self_source"}
PARTS_FORMS = ((1,), (1, 3), (1, 3, 6))
HELD_COUNTS = ("content", "sign")
HELD_DIPOLES = ("spin", "moment")
# a read's weight may be the universe's word (the file's integer by name: `Lambda`, the
# charge's read weight, record 2128 (1); `charge_weight` HISTORY)
READ_WEIGHT_WORDS = {"Lambda": "Lambda"}
# a read's twist (ALGEBRA.md 9.81 (2), 9.91 (6), 9.96 (2) (b)): an integer or "own"
# (the reading record's own rotation in the table's unit, round(2^16 omega_0), times
# the read's weight: Lambda_v is Lambda and no separate twist exists)
READ_TWIST_WORDS = ("own",)


@dataclass(frozen=True)
class TwistTable:
    """THE TWIST TABLE as read (ALGEBRA.md 9.81 (2) (b), 9.96 (2) (c)): the unit's
    integer (theta_unit = 1 / unit radians, unit = 4 Gamma 2^16), the fine triples for
    k_0 in [0, 2^10) and the coarse triples for k_1 in [0, bound); the transport's
    triple for |k| = k_1 2^10 + k_0 is their exact product."""

    unit: int
    fine: tuple[tuple[int, int, int], ...]
    coarse: tuple[tuple[int, int, int], ...]


# THE TWIST "OWN" AND THE NEAREST TRIPLE are the generators' numbers since item 73
# (`event_universe.generator_numbers`: round(2^16 omega_0) written under `twist` on
# every body and every emitter, the triples written into the universe file); the
# loader computes no float (the integer rule, record 2071) and reads the integers.


def _twist_table(value: object, label: str, node_clock: int, amplitude_bound: int) -> TwistTable:
    """The twist table read and checked in integers (ALGEBRA.md 9.96 (2) (c), (d)):
    {unit, fine, coarse}; unit = 4 Gamma 2^16; fine 2^10 triples, coarse from 1 to 2^15;
    each triple three integers, c from 1, s from 0, d from 1 to 10^9 with c^2 + s^2 = d^2,
    the first the angle 0's and the angles never falling along the table (the nearest
    triple of each angle is the generator's number, `generator_numbers.twist_triple`,
    checked by its own test); the product of the largest d of each part times 3 A inside
    int64 (the transport's total)."""
    obj = _object(value, label, {"unit", "fine", "coarse"}, {"unit", "fine", "coarse"})
    unit = _integer(obj["unit"], f"{label}.unit", 1)
    if unit != 4 * node_clock * TWIST_UNIT_SCALE:
        raise ValueError(
            f"{label}.unit {unit} is not 4 Gamma 2^16 = {4 * node_clock * TWIST_UNIT_SCALE}: "
            "theta_unit = 1 / (4 Gamma 2^16) radians per unit of k (ALGEBRA.md 9.96 (2) (a))"
        )
    parts: list[tuple[tuple[int, int, int], ...]] = []
    for name, least, most, _step in (
        ("fine", 1 << TWIST_FINE_BITS, 1 << TWIST_FINE_BITS, 1),
        ("coarse", 1, TWIST_COARSE_MOST, 1 << TWIST_FINE_BITS),
    ):
        rows = obj[name]
        if not isinstance(rows, list) or not least <= len(rows) <= most:
            raise ValueError(
                f"{label}.{name} must be a list of {least} to {most} triples [c, s, d] "
                "(ALGEBRA.md 9.96 (2) (c))"
            )
        triples: list[tuple[int, int, int]] = []
        for index, row in enumerate(rows):
            where = f"{label}.{name}[{index}]"
            if not isinstance(row, list) or len(row) != 3 or any(type(item) is not int for item in row):
                raise ValueError(f"{where} must be three integers [c, s, d]")
            c, s, d = (int(item) for item in row)
            if c < 1 or s < 0 or d < 1 or d > TWIST_TRIPLE_BOUND or c * c + s * s != d * d:
                raise ValueError(
                    f"{where} [{c}, {s}, {d}] is no triple of the table: c from 1, s from 0, "
                    f"d from 1 to {TWIST_TRIPLE_BOUND}, c^2 + s^2 = d^2 exactly (ALGEBRA.md 9.81 (2) (b))"
                )
            if index == 0 and (c, s, d) != (1, 0, 1):
                raise ValueError(f"{where} [{c}, {s}, {d}] is not the angle 0's triple [1, 0, 1]")
            if triples and s * triples[-1][0] < triples[-1][1] * c:
                # the angles in order: tan (s / c) never falls from one entry to the next
                # (the nearest-triple property is the generator's, checked by its own test)
                raise ValueError(
                    f"{where} [{c}, {s}, {d}] turns back below the entry before it: the table's "
                    "angles rise with k (ALGEBRA.md 9.96 (2) (c); the generator writes the "
                    "nearest triples, the loader checks the identities, the bound and the order)"
                )
            triples.append((c, s, d))
        parts.append(tuple(triples))
    room = 3 * max(d for _, _, d in parts[0]) * max(d for _, _, d in parts[1]) * (amplitude_bound + 1)
    if room >= TOTAL_BOUND:
        raise ValueError(
            f"{label}: the transport's total at A = {amplitude_bound}, {room}, leaves int64 "
            "(3 d_1 d_0 (A + 1) below 2^63; ALGEBRA.md 9.81 (2) (e))"
        )
    return TwistTable(unit, parts[0], parts[1])


READ_BY_WORDS = {1: "plain", "q": "sign", "plain": "plain", "sign": "sign"}


def universe_file_entries(
    value: str, files: Mapping[str, object]
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """The universe file read and translated to the families list the parse
    reads (item 51's attributes and the one stroke's, ALGEBRA.md 9.91 (7);
    record 2128 (3): the file examples/events/universe.json, the world's key
    `universe`, its integer `Lambda`),
    with the universe's integers; every key required and refused by name.
    THE TRANSLATION: `parts` as declared; `phase` to `levels`; `pair` [num,
    den] or "body"; `held` {count, factors, dipole, dipole_div} to `held`
    (the count word), `held_factors`, `held_dipole`, `held_dipole_div`;
    `reads` with the weight word resolved to the universe's integer, `by` 1
    or "q" to the loader's words, `twist` kept; `self_source.unit` to
    `self_unit`; `clicks` to `clicks` with the quantum, `quantum` 1 on a
    family without clicks (a held family, one click one unit); `charge` 0
    on every family (a body's charge is the body's number, 9.91 (7); the
    hold writes it, commit 2)."""
    if value not in files:
        raise ValueError(f"universe names {value!r}, no file at the repository's root")
    document = files[value]  # read by the host module event_universe.world_files
    label = f"the universe file {value!r}"
    if not isinstance(document, dict):
        raise ValueError(f"{label} must be a JSON object")
    unknown = set(document) - FAMILIES_FILE_KEYS
    if unknown:
        raise ValueError(f"{label} has unknown keys: {', '.join(sorted(unknown))}")
    missing = FAMILIES_FILE_KEYS - set(document)
    if missing:
        raise ValueError(f"{label} lacks keys: {', '.join(sorted(missing))}")
    integers = document["integers"]
    if not isinstance(integers, dict) or set(integers) != FAMILIES_INTEGERS | FAMILIES_TABLES:
        raise ValueError(
            f"{label}.integers must hold exactly "
            f"{sorted(FAMILIES_INTEGERS | FAMILIES_TABLES)} (the universe's integers and its twist "
            "table, ALGEBRA.md 9.83 (2) (a), 9.91 (7), 9.96 (2); no default)"
        )
    universe: dict[str, object] = {
        key: _integer(integers[key], f"{label}.integers.{key}", 1, AMOUNT_BOUND)
        for key in sorted(FAMILIES_INTEGERS)
    }
    # the twist table as written, checked with the world's Gamma and A (`_twist_table`)
    universe["twist_table"] = integers["twist_table"]
    entries = document["families"]
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{label}.families must be a nonempty list")
    translated: list[dict[str, object]] = []
    for index, entry in enumerate(entries):
        where = f"{label}.families[{index}]"
        obj = _object(entry, where, FAMILY_ENTRY_KEYS, FAMILY_ENTRY_REQUIRED)
        parts = obj["parts"]
        if not isinstance(parts, list) or tuple(parts) not in PARTS_FORMS:
            raise ValueError(
                f"{where}.parts must be one of {[list(form) for form in PARTS_FORMS]}: "
                "the representation as a list of parts, the time part first (ALGEBRA.md 9.86 (2), "
                "9.91 (1))"
            )
        if obj["phase"] not in (1, 2):
            raise ValueError(f"{where}.phase must be 1 or 2, the levels at a Node (ALGEBRA.md 9.91 (1))")
        self_source = _object(obj["self_source"], f"{where}.self_source", {"unit"}, {"unit"})
        self_unit = _integer(self_source["unit"], f"{where}.self_source.unit", 0)
        amplitude = universe["amplitude_bound"]
        assert isinstance(amplitude, int)
        if 0 < self_unit < 24 * amplitude:
            raise ValueError(
                f"{where}.self_source.unit {self_unit} is below 24 A = "
                f"{24 * amplitude}: the self-source's unit P_2 is 0 (off) or "
                "at least 24 A (ALGEBRA.md 9.91 (5))"
            )
        pair_value = obj["pair"]
        if pair_value != "body" and not (
            isinstance(pair_value, list)
            and len(pair_value) == 2
            and all(type(item) is int and item >= 1 for item in pair_value)
        ):
            raise ValueError(
                f'{where}.pair must be [num, den] or the word "body" (every body and '
                "record of the family declares its own pair; ALGEBRA.md 9.85 (3), 9.91 (7))"
            )
        if "held" not in obj and "clicks" not in obj:
            raise ValueError(
                f"{where} declares neither held (a field family) nor clicks (a family "
                "of records): a family does one or both (ALGEBRA.md 9.86 (2))"
            )
        legacy: dict[str, object] = {
            "name": obj["name"],
            "charge": 0,
            "pair": pair_value,
            "parts": list(parts),
            "levels": obj["phase"],
            "self_unit": self_unit,
        }
        reads: list[dict[str, object]] = []
        raw_reads = obj["reads"]
        if not isinstance(raw_reads, list):
            raise ValueError(f"{where}.reads must be a list of {{family, weight, twist, by}}")
        for position, item in enumerate(raw_reads):
            read = _object(
                item,
                f"{where}.reads[{position}]",
                {"family", "weight", "twist", "by"},
                {"family", "weight", "twist", "by"},
            )
            weight = read["weight"]
            if isinstance(weight, str):
                if weight not in READ_WEIGHT_WORDS:
                    raise ValueError(
                        f"{where}.reads[{position}].weight {weight!r} names no integer of "
                        f"the universe (the words: {sorted(READ_WEIGHT_WORDS)})"
                    )
                weight = universe[READ_WEIGHT_WORDS[weight]]
            by = read["by"]
            if by not in (1, "q"):
                raise ValueError(
                    f'{where}.reads[{position}].by must be 1 or "q" (the level enters '
                    "the pace plainly, or by the reading record's charge sign; ALGEBRA.md 9.91 (7))"
                )
            reads.append(
                {
                    "family": read["family"],
                    "weight": weight,
                    "by": READ_BY_WORDS[by],
                    "twist": read["twist"],
                }
            )
        legacy["reads"] = reads
        if "held" in obj:
            source = _object(
                obj["held"],
                f"{where}.held",
                {"count", "factors", "dipole", "dipole_div"},
                {"count", "factors", "dipole"},
            )
            legacy["held"] = source["count"]
            legacy["held_factors"] = source["factors"]
            legacy["held_dipole"] = source["dipole"]
            legacy["held_dipole_div"] = source.get("dipole_div", 1)
        if "clicks" in obj:
            clicks = _object(
                obj["clicks"],
                f"{where}.clicks",
                {"gives", "takes", "quantum"},
                {"gives", "takes", "quantum"},
            )
            legacy["clicks"] = {"gives": clicks["gives"], "takes": clicks["takes"]}
            legacy["quantum"] = clicks["quantum"]
        else:
            legacy["quantum"] = 1
        translated.append(legacy)
    return translated, universe


# THE ENGINE START FILE (record 2089; records 2092 and 2094; ALGEBRA.md 9.83 (2)
# (a); BUILD.md section 26 item 57): one canonical copy at
# examples/events/engine_start.json, referenced by every world of the detector
# law by its repository path (`engine`) and read by the runner; it holds the
# run's parameters and no law's number (the law's numbers are the families
# file's and the world's, 9.83 (2) (a)). Its keys, every one required: `law`
# (the law identifier) and `mode`, "check" (every measured event read beside
# its blind expectation, no pin compared; the run's mode until the model
# owner's Go, records 2050 and 2054) or "pin" (the pins compared).
START_KEYS = {"mode"}
START_MODES = ("check", "pin")
# THE REPOSITORY'S ROOT and every file read live in the host module
# event_universe.world_files (the loader reads no file; tests/test_architecture.py)


@dataclass(frozen=True)
class EngineStart:
    """The one engine start file as read: its repository path and its mode."""

    path: str
    mode: str


def _engine_start(value: object, files: Mapping[str, object], detector_law: bool) -> EngineStart | None:
    """The world key `engine`: the repository path of the start file, required
    (the ray law's branch below CANCELLED, 9.90 (1)); the file a JSON object with
    exactly the keys of START_KEYS (`mode`, one of START_MODES; no law's name,
    ALGEBRA.md 9.90 (1)); a missing key refused by name."""
    if not detector_law:
        if value is not None:
            raise ValueError("engine is refused without `detector_law`")
        return None
    if value is None:
        raise ValueError(
            "engine is required: the repository path of the one "
            "engine start file (examples/events/engine_start.json), no default (the model owner's "
            "record 2089; BUILD.md section 26 item 57)"
        )
    if not isinstance(value, str) or not value:
        raise ValueError("engine must be the start file's repository path, a string")
    if value not in files:
        raise ValueError(f"engine names {value!r}, no file at the repository's root")
    start = files[value]  # read by the host module event_universe.world_files
    if not isinstance(start, dict):
        raise ValueError(f"the engine start file {value!r} must be a JSON object")
    unknown = set(start) - START_KEYS
    if unknown:
        raise ValueError(
            f"the engine start file {value!r} has unknown keys: {', '.join(sorted(unknown))}"
        )
    missing = START_KEYS - set(start)
    if missing:
        raise ValueError(
            f"the engine start file {value!r} lacks keys: {', '.join(sorted(missing))} "
            "(every key required, no default; the model owner's record 2089)"
        )
    if start["mode"] not in START_MODES:
        raise ValueError(
            f"the engine start file {value!r} declares mode {start['mode']!r}; one of "
            f"{list(START_MODES)}"
        )
    return EngineStart(value, str(start["mode"]))


def _require_under_law(obj: dict[str, object], label: str, keys: set[str]) -> None:
    """NO DEFAULT (record 2089): every key the engine or
    the loader reads is declared; a missing one is refused by name."""
    missing = keys - set(obj)
    if missing:
        raise ValueError(
            f"{label} lacks keys the engine reads: "
            f"{', '.join(sorted(missing))} (no default; the model owner's record 2089)"
        )


def _refuse_under_law(obj: dict[str, object], label: str, keys: set[str]) -> None:
    """A key the engine never reads is refused by name: a flag the engine does not need is deleted, not defaulted."""
    present = [key for key in sorted(keys) if key in obj]
    if present:
        raise ValueError(
            f"{label} declares {', '.join(present)}, which the engine never reads "
            "(refused by name; the model owner's records 2089 and 2094)"
        )


# THE FILE'S STAMP (record 1886; ALGEBRA.md 9.22 (7) (i); 9.90 (3) (c)): the
# digest of the whole file, written by the generator under the key `stamp` and
# compared at load; the law identifier that stood beside it is CANCELLED (one
# engine, 9.90 (1)); a change of the engine that moves the initial state is read
# in the digest of the regenerated file.
STAMP_KEYS = {"hash"}
BLOCK_KEYS = {
    "side",
    # the box's extents per axis in place of `side` (the slabs of ALGEBRA.md
    # 9.22 (8); BUILD.md section 26 item 23)
    "extents",
    "pair",
    # THE BODY'S KIND (ALGEBRA.md 9.85 (3), 9.91 (7); the one stroke, commit 1):
    # the body's rest pair on a family whose pair is the body's
    "kind",
    # THE BODY'S NUMBERS the holds read (ALGEBRA.md 9.91 (3), (7); commit 2): its
    # charge Q, its spin S and its moment mu (the momentum n is `momentum`)
    "charge",
    "spin",
    "moment",
    # the body's own record's twist "own", the generator's integer (item 73)
    "twist",
    "coupling",
    "seed",
    # the bound mode's clock [a, b] beside a profile (ALGEBRA.md 9.22 (7))
    "clock",
    # the moving body's Node's proper pairs by the momentum's whole part (ALGEBRA.md
    # 9.63 (3); BUILD.md section 26 item 46), beside `clock` on a moving block
    "proper_clock",
    "cavity",
    "ramp",
    "start",
    "margin",
    # the emitter as a clicking body (ALGEBRA.md 9.17 (4); LAB_TOOLS.md A.1):
    # the excited records in turn on the body's Nodes, each clicking at its
    # own rung, the given record written once by E^T at that interval
    "emitter",
    # detector-law-v1, the receiver by name (DECLARATIONS.md section 13 item
    # 7): an emitting block names the detector set whose one detector is its
    # record's ladder; admitted on an emitting block alone
    "receiver",
    # the stock of the body's own family where its emitter gives it (ALGEBRA.md
    # 9.96 (5); commit 6)
    "stock",
}
# The margin rule's two kinds of world (MASSIVE_RECORD.md section 11 item 4,
# Reviewer 3's two lines): a pin world's Nodes two extents from a
# non-periodic face and a periodic side of s + 4 extents; a control world's
# one extent and s + 2 extents.
MARGIN_KINDS = ("pin", "control")
MEASURED_KEYS = {
    "position",
    "family",
    "amount",
    "stocks",  # the body's stocks of other families' quanta (record 2128 (1); `held` HISTORY)
    "kind",
    "q",  # the body's signed number (record 2128 (1); `charge` the family's word alone)
    "spin",
    "moment",
    "twist",  # the body's own record's twist "own", the generator's integer (item 73)
    "phase",
    "momentum",
    "fixed",
    "span",
    "phase_by_momentum",
    "level",
    "directions",
    "table",
    *BLOCK_KEYS,
    "lamp",
    "become",
    # The axial record (`hand-v1`): one of the six headings, the axis the
    # right-hand rule reads at every product of the event's `become`.
    "axis",
    # The energy E' a thrown body declares under `covariant_readings`
    # (`covariant-readings-v1`; refused without the world key).
    "E",
}
# CANCELLED (docs/CANCELLED_WORLDS.md section 9; ALGEBRA.md 9.90 (1)): the ray law's lamp keys (read by the cancelled parse alone)
LAMP_KEYS = {
    "rate",
    "wheel",
    # detector-law-v1, the block's grace for its emitted records: a lamp's `own_grace` (N_s, the intervals after
    # its train during which its own body takes nothing of its own record;
    # DECLARATIONS.md section 15 M1-6: the matter lamp 16700, the hold);
    # without it a lamp's grace is the engine's constant two periods
    "own_grace",
    # detector-law-v1, the order channel's two keys (DECLARATIONS.md section
    # 2 item 8, the model owner's declaration of 2026-09-24; Reviewer 3's
    # line: no default): on a PAIR lamp (a lamp with `arms` above 1) under
    # `detector_law`, `residue_order` is REQUIRED, "ordinal" (the counter
    # form as built, u = (ordinal - 1) r mod W) or "seed" (the seed-set
    # order, u = order[(ordinal - 1) mod W], the order a Fisher-Yates
    # permutation of Z_W driven by the SplitMix64 mixing hash from
    # `residue_seed`, `core.integer.keyed_permutation`; the stride r must be
    # 1); `residue_seed`, an integer in [0, 2^64), an input of kind 1,
    # required under "seed" and refused under "ordinal". Neither key is
    # admitted on a lamp without arms or outside `detector_law`.
    "residue_order",
    "residue_seed",
    # detector-law-v1: the record's train in periods of its clock (the
    # record's coherence), a declaration of the lamp, absent by default.
    "train",
    # detector-law-v1: the lamp record's LADDER BY NAME (SIZING.md, the click
    # line and the receiver by name, DECLARATIONS.md section 13 item 7): the
    # detector sets, by name, among which the giving wheel's u chooses the
    # record's detector; every other set and every face is a SINK for the lamp's
    # records (what it takes is booked to the escaped row, never chosen).
    # Absent, the ladder is every detector as built. A string or a list of
    # strings; refused outside `detector_law` and on a name no set declares.
    "receiver",
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
# CANCELLED (docs/CANCELLED_WORLDS.md section 9; ALGEBRA.md 9.90 (1)): the ray law's table keys (read by the cancelled parse alone)
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
# CANCELLED (docs/CANCELLED_WORLDS.md section 9; ALGEBRA.md 9.90 (1)): the ray law's split, transform, become, clock, window and transit keys (read by the cancelled parse alone)
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
DETECTOR_KEYS = {"name", "positions", "threshold", "reading", "block"}
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
# detector-law-v1 (DECLARATIONS.md section 10, Reviewer 3's line, 2026-09-24):
# a face declared "closed" is a zero face for light WITHOUT the open face's
# take (a mirror: the level 0 beyond it, no face detector, no sponge), per
# axis, admitted under `detector_law` alone (the ray law has no rows).
CLOSED_FACE = "closed"


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
    # The record kind's pair [num, den] on the six-neighbour term of the
    # local detector law's rule (`massive-record-v1`, MASSIVE_RECORD.md
    # section 1): light's kind is the value (1, 1) (every family without
    # the key `pair`); a massive kind declares den > num, its rest
    # frequency cos omega_0 = num / den. Admitted under the world key
    # `massive_record` alone.
    pair: tuple[int, int] = MASSLESS_PAIR
    # THE FAMILY GENERICITY (the model owner's record 2066 of 2026-09-25
    # through the Boss: "the engine does not know the family's name, does not
    # know what the family does; it only supports the family's operations";
    # BUILD.md section 26 item 51). What a family IS is declared here and
    # read by the engine as attributes alone, never by a name or a role:
    # `held`, the source a body's record writes at the body's Nodes at both
    # levels with the remainder 0, "content" (the quanta the body holds, the
    # Node clock's c of ALGEBRA.md 9.45) or "charge" (the signed sum of its
    # quanta, the d of 9.48), None for a family the step alone moves; `reads`,
    # the held families whose levels enter this family's pace at every Node,
    # (family index, weight, by) each, the effective content SUM weight x
    # level for by = "plain" and - q x weight x level for by = "sign" (q the
    # reading family's own charge sign; 9.48 (3): c - q Lambda d), empty for
    # a held family (the plain rule, the pace 1 of its own); `components`,
    # the representation's count (1 a scalar; 3 and 6 the vector and tensor
    # families of 9.77, not yet built). The sources and the read modes are
    # the operations' words, never a family's name (item 53: "sign", the
    # signed sum of the quanta by the families' declared signs). A held
    # family is booked by no detector and every other family is (`booked`,
    # derived, item 53); a family declares nothing about detectors or
    # emitters: those are the bodies' mechanisms.
    held: str | None = None
    reads: tuple[tuple[int, int, str, int | str], ...] = ()
    # THE REPRESENTATION AS A LIST OF PARTS (ALGEBRA.md 9.86 (2), (3); 9.91
    # (1); the one stroke, commit 1): (1,) a scalar, (1, 3) the time part and
    # the vector, (1, 3, 6) the symmetric tensor over the four directions; the
    # component order fixed once, (t), (x, y, z), (xx, yy, zz, xy, xz, yz)
    parts: tuple[int, ...] = (1,)
    # the levels at a Node (9.91 (1)): 1 the pair (a_now, a_before, r); 2 the
    # two levels with their remainders (the second level not yet allocated:
    # it enters with the transport, commit 4)
    levels: int = 2
    # THE HELD SOURCE'S WRITES (9.91 (3), (7)): the factor per part (gravity
    # (1, 4, 2): s, 4 s n div W, 2 s n n div W^2; the charge (1, 1)), the
    # body's dipole number written on the six neighbours ("spin", "moment")
    # and its divisor; read by the hold once the vector parts are written
    # (commit 2); one factor per part, (1,) on a scalar
    held_factors: tuple[int, ...] = (1,)
    held_dipole: str | None = None
    held_dipole_div: int = 1
    # the self-source's unit P_2 (9.78 (3), 9.91 (5)): 0, off
    self_unit: int = 0
    # THE CLICKS (9.79 (1), 9.91 (7)): (gives, takes) for a family of records,
    # None for a field family that is never given or taken
    clicks: tuple[bool, bool] | None = None
    # THE PAIR ON THE BODY (9.85 (3), 9.91 (7)): the family declares no pair
    # of its own; every body and every given record of it declares its own
    # (`kind` on the body, `pair` on the emitter); `pair` then a placeholder
    pair_on_body: bool = False

    @property
    def booked(self) -> bool:
        """The detectors book the family's records at their Ports: exactly a
        family with clicks (derived, item 53; ALGEBRA.md 9.91 (7))."""
        return self.clicks is not None

    @property
    def components(self) -> int:
        """The count of components, the parts summed (9.91 (1))."""
        return sum(self.parts)

    @property
    def massive_kind(self) -> bool:
        """A family of the massive record kind: its pair has den > num (a
        gap), or its bodies declare their pairs; light's kind reads den =
        num."""
        return self.pair_on_body or self.pair[1] > self.pair[0]

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
    # The giving wheel (`wheel`, [r, W]; the model owner's decision of
    # 2026-09-21, record 180 of the log of 2026-09-20; BEAM_LAW note 46):
    # the rate of one row of the lamp's counts table, advanced by r over W
    # at every giving, whose accumulator before the advance is the record's
    # coordinate u on the ladder, u = ordinal x r mod W; the rungs of the
    # click are on W. [1, N] is the lamp's count of givings mod N as built;
    # declared on every lamp, no default.
    wheel: tuple[int, int]
    directions: tuple[int, ...]
    window: int | None
    # The window's width in steps (`phase_width`), None for the default
    # N / 2, the half circle.
    width: int | None = None
    # The phase step each direction's row is given with beyond the clock's
    # phase (`turns`, the amplitude law: the reflection's quarter turn at
    # the source's splitter), 0 each by default.
    turns: tuple[int, ...] = ()
    # The joint labels of a giving with their integer weights (`branches`,
    # the amplitude law's pair: [[0, 1], [3, 1]] the Bell pair on two
    # arms, the bit k of a label the label on arm k) and `arms`, the count
    # of directions that are separate quanta (1 by default: the directions
    # are paths of one quantum; the directions are shared equally by the
    # arms, in order).
    branches: tuple[tuple[int, int], ...] = ((0, 1),)
    arms: int = 1
    # detector-law-v1, the order channel's keys on a pair lamp (DECLARATIONS.md
    # section 2 item 8): "ordinal" or "seed", None on a lamp without arms;
    # the seed of the seed-set order, None under "ordinal".
    residue_order: str | None = None
    residue_seed: int | None = None
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
    # detector-law-v1: the record's train in periods of the family's clock,
    # None without (the law's default then).
    train: int | None = None
    # detector-law-v1, the block's grace for its emitted records: the lamp's declared own_grace (N_s), the
    # intervals after its train during which its own body takes nothing of
    # its own record; None: two periods of its clock (the engine's constant).
    own_grace: int | None = None
    # detector-law-v1: the record's ladder by name (`receiver`), the detector
    # sets among which u chooses the detector, in the world's order; None: every
    # detector as built (the lamp worlds of the tables, untouched).
    receiver: tuple[str, ...] | None = None


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
class EmitterDefinition:
    """The emitter as a clicking body (ALGEBRA.md 9.17 (4), the mathematician's
    integers of 2026-09-24; LAB_TOOLS.md A.1): on a body of a massive kind
    with its seed (the excited record: the body's seed at both levels) and
    its stock THE GIVEN FAMILY'S CONTENT HELD AT THE BODY, `held` naming the
    given family (ALGEBRA.md 9.51 (8); BUILD.md section 26 item 47: a giving
    lowers the given family's content by one; the body's own quanta `amount`
    and its charge stay; the stock as `amount` HISTORY), the key
    `emitter`: {"family": the given family's name (a paid family with the
    pair form of its clock), "branches": the given record's labels (optional,
    [[0, 1]] by the lamp's form), "receiver": the given records' ladder by
    name (optional, a list of set names; the block's own `receiver`, one
    name, is the line at the rung), "period": P, the nearest integer to
    2 pi / omega_b of the body's mode (the generator's integer), "norm":
    T, one period's action P e_c: the share of the body's conserved form
    at its centre Node summed over P intervals advanced alone (the
    generator's integer under the input stamp; ALGEBRA.md 9.17 (7) (e) and
    (f) in the flux's units of 9.19 (3)), "given": the given record's two levels
    over the whole board as material (optional; {"now": [...], "before":
    [...]}, x-major, one per Node; the engine copies them at the click;
    9.17 (5) item 3)}. Without `given` the given record is the pair on every
    Node of the body: now = A C_2N[3 N / 2 + s] on the circle of 2 N steps
    with s = floor(n / d) the given clock's step and before = -now (the
    character half a step either side of its zero, no static part; 9.17
    (6)); an odd s where 2 N exceeds the tables' bound is refused. Excited
    record k clicks at its own rung (E the one-way flux into its centre
    Node, D the rung 2 T u_k + T <= 2 W C with T its norm); at that click
    X ends it and E^T givings the photon (content one quantum, its residue
    the excitation's) and, while the stock lasts, excited record k + 1. No
    rate, no train, no drive, no source term, no grace."""

    family: int
    branches: tuple[tuple[int, int], ...]
    label_hands: tuple[int, int] | None
    receiver: tuple[str, ...] | None
    # THE GIVEN CLOCK (ALGEBRA.md 9.85 (3); item 59): the given record's clock
    # [p, q], the family's own or the emitter's `clock`
    clock: tuple[int, int]
    # THE GIVEN RECORD'S PAIR (ALGEBRA.md 9.85 (3), 9.91 (7); commit 1): the
    # given family's declared pair, or the emitter's own `pair` on a family
    # whose pair is the body's
    pair: tuple[int, int] = MASSLESS_PAIR
    period: int | None = None
    norm: int | None = None
    train: TrainDefinition | None = None
    given: GivenTrain | None = None
    # THE POINT EMITTER'S NORM DENOMINATOR (9.71 (1) (d); item 50): the
    # excitation's action T as the exact rational norm / norm_denominator,
    # in the form's units, which the window's outward norm is read against;
    # required on every emitter (commit 7: the window the one giving)
    norm_denominator: int | None = None
    # THE POINT EMITTER'S WEIGHT g (ALGEBRA.md 9.71 (1) (b); item 50): the
    # body's coupling to the given family, one integer, the body's Node's rotation
    # copied at that weight into the given row at the body's Node every interval of
    # the window; required on every emitter (commit 7: the window the one giving)
    weight: int | None = None
    # THE GIVEN RECORD'S COMPONENT (ALGEBRA.md 9.82 (3) (d), 9.91 (1); commit 4): the
    # index in the given family's parts, 0 on a scalar family, 1 + the axis of the
    # body's moment on a vector family (the component along mu)
    part: int = 0
    # THE GIVEN RECORD'S TWIST "OWN" (ALGEBRA.md 9.96 (2) (a); commit 4): round(2^16
    # omega_0), the record's rest rotation from its pair (a massive kind) or from its
    # wavelength on light's dispersion (a train) or its emitter's rotation (a window)
    twist: int = 0


@dataclass(frozen=True)
class TrainDefinition:
    """THE GIVEN TRAIN'S DECLARATION (ALGEBRA.md 9.17 (6a); BUILD.md section
    26 item 27): the key `train` of an emitter: {"direction": one signed
    unit axis vector, the train's **K** and its way; "periods": n >= 8, the
    train's length in periods}. The given clock is the given family's
    declared clock [p, q] (the world's family column, one clock per row):
    the wave number k = 2 pi p / (2 N q) per Link on the world's circle of
    N steps, the wavelength 2 N q / p a whole number of Links, and the
    body's extent along the direction n wavelengths (32 Nodes for 8
    periods at the wavelength 4 of [512, 1] on N = 1024). DOPPLER (ALGEBRA.md
    9.62 (4), adopted by the model owner, record 2042; BUILD.md section 26
    item 49): the given rows of a MOVING body carry its motion in the given
    family's representation, the wave number boosted, forward k gamma (1 + v
    / c_l), backward k gamma (1 - v / c_l), declared for the declared momentum
    as the train's own clock pair `clock` [p, q] (the generator's, the
    wavelength whole, the body's extent n of them); admitted on a moving body
    alone, at rest the given family's clock."""

    axis: int
    sign: int
    clock: tuple[int, int]
    periods: int
    wavelength: int
    # DOPPLER (item 49): the train declares its own boosted clock (a moving
    # body's); its `given` then carries the rest norm too (ALGEBRA.md 9.74 (3))
    boosted: bool = False

    @property
    def direction(self) -> tuple[int, int, int]:
        vector = [0, 0, 0]
        vector[self.axis] = self.sign
        return (vector[0], vector[1], vector[2])

    @property
    def length(self) -> int:
        """The train's length in Nodes, periods x wavelength."""
        return self.periods * self.wavelength


@dataclass(frozen=True)
class GivenTrain:
    """THE GIVEN TRAIN'S PROFILE (ALGEBRA.md 9.17 (6a)): the key `given` of an
    emitter: {"now": [...], "before": [...]} over the body's Nodes in the
    box's x-major order (`body_node_indices`: the character of the train's
    **K** over its periods under the window across the transverse extents
    and the tapers along **K**, at the two levels t = 0 and t = -1, the
    generator's integers at the amplitude 2^16), and "norm": T, the given
    record's conserved form on the given family's VACUUM in the flux's units
    (9.19 (3)), the generator's integer checked at load (`given_train_norm`):
    the ladder's T. The two-integer pair [now, before] (the one-Node giving,
    a flat pulse of the body's length, broadband) is refused by name. THE
    BOOSTED NORM (ALGEBRA.md 9.74 (3), 9.75 (1); BUILD.md section 26 item 56):
    a moving body's boosted train carries the quantum's energy in the board's
    frame, gamma (1 + beta) T_rest forward and gamma (1 - beta) T_rest
    backward (the rows at the rest amplitude carry it already: the form is
    quadratic in the wave number, the generator's reading), and declares
    "rest_norm": T_rest, the same train's norm at the body's own clock and
    the same amplitude, the ladder's threshold (the record's form at the
    giving times rest_norm / norm);
    REQUIRED on a train with its own `clock`, refused at rest (the rest
    train's norm is `norm` itself); `rest_norm` equals `norm` at rest."""

    now: tuple[int, ...]
    before: tuple[int, ...]
    norm: int
    rest_norm: int


@dataclass(frozen=True)
class BlockDefinition:
    """A block, the foreign object of the massive record kind
    (`massive-record-v1`, MASSIVE_RECORD.md sections 4 to 7): its Nodes R
    the box of `extents` per axis (the cube of `side` the shorthand for
    equal extents; the slabs of ALGEBRA.md 9.22 (8), BUILD.md section 26
    item 23) with its lower corner at the measured event's `position`,
    cut to the board on an open axis and wrapped on a periodic one; its `pair` on the six-neighbour term at its Nodes (a WELL of the
    massive kind's pair, `num' / den' > num / den`; on light's kind a gap,
    the (M) wall); the
    `seed` of its own record on its Nodes at interval 0 (0: silent; declared,
    no default, BUILD.md section 26 item 28); `ramp`
    (the pushing agent's declaration: its momentum reached from 0 over that
    many intervals); `start` (the same agent's: the interval its drive
    begins, 0 by default, the ramp counted from it); `margin` (the margin
    rule's kind of world). The take (`absorbing`, `take`), the cycle
    emitter (`emits`, `own_grace`) and a declared wheel are retired
    (BUILD.md section 26 items 14 and 15)."""

    side: int
    pair: tuple[int, int]
    # THE BODY'S KIND (ALGEBRA.md 9.85 (3), 9.91 (7); the one stroke, commit
    # 1): the rest pair of the body's own record, its family's declared pair
    # or, on a family whose pair is the body's, the body's own `kind`
    kind: tuple[int, int]
    # the well's own record's amplitude on its Nodes at interval 0 (0
    # silent), or its profile's; declared in the file, no default (the
    # model owner's rule through the Boss, 2026-09-25; BUILD.md section 26
    # item 28; the loader's 2^20 of the first builds HISTORY)
    seed: int
    # the box's extents per axis (x, y, z); a cube's are (side, side, side),
    # and `side` is the x extent for the readers of a cube
    extents: tuple[int, int, int] = (1, 1, 1)
    # the bound mode's integer profile over the whole board (x-major, one per
    # Node) when the seed is declared so; None for a flat seed
    profile: tuple[int, ...] | None = None
    # THE MODE'S CLOCK (ALGEBRA.md 9.22 (7); record 1886): 2 cos omega of the
    # body's bound mode as the rational [a, b] the generator wrote, b at
    # least the profile's amplitude; the loader's integer check of the
    # profile against the eigen-equation reads it; None for a flat seed
    clock: tuple[int, int] | None = None
    # THE PROPER PAIR OF A MOVING BODY ON ONE NODE (ALGEBRA.md 9.63 (3); BUILD.md section 26
    # item 46): the pairs [num_m, b] the body's Node rotates at while the drive's
    # momentum is m, indexed by m from 0 (the clock itself) to |P| along the
    # one axis of the declared momentum, the generator's reading of the moving
    # mode at its moving centre, 2 cos(omega_K - K v) at v = m / (3 Q M);
    # None on a body at rest
    proper_clock: tuple[tuple[int, int], ...] | None = None
    ramp: int = 0
    start: int = 0
    # THE BODY'S NUMBERS (ALGEBRA.md 9.91 (3), (7); the one stroke, commit 2): the
    # signed number q (the held sign's count at its Nodes; the world's word `q`,
    # record 2128 (1)), the spin S and the moment mu (the dipoles on its Node's
    # six neighbours); the momentum n is `momentum`
    q: int = 0
    spin: tuple[int, int, int] = (0, 0, 0)
    moment: tuple[int, int, int] = (0, 0, 0)
    # THE BODY'S OWN RECORD'S TWIST "OWN" (ALGEBRA.md 9.96 (2) (a); commit 4): round(2^16
    # omega_0), its rotation from its mode's clock [a, b] (2 cos omega) where it has
    # one, else from its kind's pair
    twist: int = 0
    margin: str = MARGIN_KINDS[0]
    # detector-law-v1, the receiver by name (DECLARATIONS.md section 13 item
    # 7, the click line): the name of the detector set whose one detector is the
    # ladder of every record this block emits (the click line at that detector's
    # first rung after the record's train; the faces and every other set
    # sinks for it); None where the world names none, the ladder then every
    # detector and the line at the close, as before the key.
    receiver: str | None = None
    # the emitter as a clicking body (ALGEBRA.md 9.17 (4)): None on a body
    # that emits nothing by the click
    emitter: EmitterDefinition | None = None
    # THE STOCK OF THE BODY'S OWN FAMILY (ALGEBRA.md 9.96 (5); commit 6): the count of
    # its own quanta set aside for giving where its emitter gives its own family, 0
    # elsewhere (another family's stock is the body's `held` quanta of it)
    stock: int = 0


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
    # The block (massive-record-v1): the measured event's Nodes, pair,
    # seed and the rest, or None (a body of one Node or a span as before).
    block: BlockDefinition | None = None


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
    (`beam` or `wave`): ONE DETECTOR, one cube of side DETECTOR_SIDE or
    more (record 1899), whose click is the detector's and never a Node's;
    under the local detector law a set may instead be BOUND TO A BLOCK
    (`block`, the measured event's number): its Nodes are the block's Nodes
    at every interval (a stepping block's follow it) or a cube of free
    Nodes beside it, its pointer the one-way flux into them; the click
    stamps the block's own count. The rung's wheel is the record's own
    (ALGEBRA.md 9.22 (4)): a set declares none."""

    name: str
    positions: tuple[Address3, ...]
    threshold: int
    reading: str = DETECTOR_READINGS[0]
    block: int | None = None


@dataclass(frozen=True)
class NatureBeamWorld:
    """A parsed world of the engine (no law's name, no `model_id`: ALGEBRA.md
    9.90 (1)). `boundary` is the declared value
    as the record carries it (the string `"open"` or the object per axis);
    `periodic` says per axis (x, y, z) whether the walk wraps; `directions`
    is the table `D`: the two rest vectors, the six headings and the declared
    rest; `action` is h, the quantum of action of the turn by momentum, or
    None when the world declares none."""

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
    readings: tuple[Reading, ...]
    step: Step
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
    # flow-link-v1 (the world key `flow_link`, false by default): the flow
    # label per Euclidean Link in place of the unit label per Node
    # (`nature_beam.flow_label`, formed once at load).
    flow_link: bool = False
    # centred-step-v1 (the world key `centred_step`, false by default): the
    # body's step at half the wall on both drives (`"centred-step"`).
    centred_step: bool = False
    # The clock stamp (the world key `clock_stamp`, false by default): every
    # line a measured event writes carries `clock`, its own count of
    # self-creations; a record field, no physics, no hypothesis.
    clock_stamp: bool = False
    # the face receiver's depth at every open border (ALGEBRA.md 9.25 (10)),
    # declared in the file under the detector law (no default, BUILD.md
    # section 26 item 28); 0 on a GameBoard with no open face (no slab)
    face_depth: int = 0
    # ONE ENGINE (ALGEBRA.md 9.90 (1)): the flag `detector_law` that selected the
    # engine beside the ray law is CANCELLED; every world is the engine's, and the
    # loader refuses a lamp with turns and a measured event with a fan table
    # (instruments of the ray law) and needs the pair form of the clock on every
    # paid family. The attribute stays True for the record (read by nothing).
    detector_law: bool = True
    # massive-record-v1 (2026-09-23): the massive record kind beside light
    # under the local detector law, false by default; under it a family may
    # declare its `pair`; its faces are the world's.
    massive_record: bool = False
    # THE BODY RECORD (ALGEBRA.md 9.46 (1) to (3); BUILD.md section 26 item
    # 37): true holds every seeded block as one rotation on its clock pair
    # (a Node with a shape), its profile read and never stepped; false, the
    # default, the lattice body (its own rows on the GameBoard)
    body_record: bool = False
    # CANCELLED (commit 7): the world key `point_emitter` is retired, the window
    # the law's one giving (ALGEBRA.md 9.85 (5), 9.71 (1); record 2082 (4)); the
    # field stays False and is read nowhere
    point_emitter: bool = False
    # massive-record-v1: the probes, Nodes whose light amplitude is written
    # per interval (GAMEBOARD), empty by default.
    probes: tuple[Address3, ...] = ()
    mode_axis: int | None = None
    # detector-law-v1: per axis, whether the face is declared "closed" (a
    # zero face for light with no take); never on a periodic axis.
    closed: tuple[bool, bool, bool] = (False, False, False)
    # massive-record-v1: the world key `amplitude_bound`, the amplitude A
    # every row stays below (declared on a massive world; the ceiling 2^28
    # under the Node clock, BUILD.md section 26 item 31, on a world without
    # the kind, where no row is bounded so).
    amplitude_bound: int = AMPLITUDE_BOUND
    # THE NODE CLOCK (ALGEBRA.md 9.35 (2), (3); BUILD.md section 26 item 31):
    # Gamma, the world key `node_clock`, the clock pair (Gamma, Gamma + M) at
    # every Node; required under the detector law, 0 on a world without it
    # (the ray law has no rule with a division).
    node_clock: int = 0
    # THE MOMENTUM'S UNIT Q (ALGEBRA.md 9.96 (1), 9.89 (2)): the universe's
    # integer `momentum_unit`; every body's wall is W = 3 Q M with M its quanta,
    # its velocity n / W Links per interval; required under the detector law,
    # 0 on a world without it
    momentum_unit: int = 0
    # THE TWIST TABLE (ALGEBRA.md 9.81 (2) (b), 9.96 (2) (c); commit 4): the exact
    # triples of the transport's angles, None on a world without one (no transport)
    twist_table: TwistTable | None = None
    # THE ENGINE START FILE (record 2089; BUILD.md section 26 item 57): the
    # world's `engine` as read, None on a world without the detector law
    start: EngineStart | None = None
    # THE ONE FAMILIES FILE (item 59): the world's `families` as a repository
    # path, None when the world lists its families inline
    universe_file: str | None = None
    # atom-level-v1 (the world key `atom_level`, false by default): the
    # release at a closure of the difference of two closures' levels
    # (`"atom-level"`; a body's `level` declaration).
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
        declared (a record is given by a lamp, a rebirth follows a lamp's
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
                    f"the column {name!r}: Lambda_c = {scale}, the least common "
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
        """CANCELLED (ALGEBRA.md 9.90 (1)): the identities of the physical hypotheses
        a world of the ray law declared beside it, in a fixed order, now an empty
        list on every world (one engine, no identity); the order as it stood: `bohr-v1` for the turn by momentum
        (`action`), `columns-v1` for the one mechanism of the columns (a
        column beyond `charge`, or a lifetime: a force of nature in this
        law is a column with a sign and a range), `weak-v1` for the
        transformation `become` (the weak force in the world's terms),
        `meeting-v1` and `amplitude-v1` for their keys, `massive-rows-v1`
        for the world key `massive_rows` (the massive rows beside the law),
        `hand-v1` when the world declares a hand or an axis,
        `covariant-readings-v1` when the world declares `covariant_readings`,
        `optical-v1` for the world key `optical`, `drive-b-v1` for the world
        key `drive_b` (the directional drive of a body), `flow-link-v1` for
        the world key `flow_link` (the flow label per Euclidean Link),
        `centred-step-v1` for the world key `centred_step` (the body's step at
        half the wall) and, last,
        `binding-v1` when a measured event holds a paid family (`binding`;
        the engine appends it at the same place from the first give of a
        run, `NatureBeamSimulation.hypotheses`)."""
        # ONE ENGINE (ALGEBRA.md 9.90 (1); docs/CANCELLED_WORLDS.md section 9): no
        # identity stands beside the engine; the ray law's identities this property
        # listed (bohr, columns, weak, meeting, amplitude, massive-rows, hand,
        # covariant-readings, drive-b, flow-link, centred-step, atom-level, binding)
        # are CANCELLED and never appended
        return []

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
    def held_families(self) -> tuple[int, ...]:
        """THE FAMILY GENERICITY (record 2066; item 51): the indices of the
        families with a held source, in the declared order (the engine's one
        list of held records)."""
        return tuple(index for index, family in enumerate(self.families) if family.held is not None)

    def kind_periodic(self, family: int) -> tuple[bool, bool, bool]:
        """The faces a family's rows read, per axis: the world's `boundary`,
        ONE BORDER FOR EVERY FAMILY (the model owner's rule through the Boss,
        2026-09-25; BUILD.md section 26 item 28); a family's own `faces`
        (`massive-record-v1`, HISTORY) is refused at load, so every family
        reads the same border."""
        assert 0 <= family < len(self.families)
        return self.periodic

    @property
    def boundary_per_axis(self) -> dict[str, str]:
        """The GameBoard's faces per axis, `x`, `y`, `z` to `open`, `periodic` or `closed`."""
        return {
            axis: BOUNDARIES[1] if wraps else (CLOSED_FACE if shut else BOUNDARIES[0])
            for axis, wraps, shut in zip(AXES, self.periodic, self.closed, strict=True)
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
    """CANCELLED (ALGEBRA.md 9.90 (1); docs/CANCELLED_WORLDS.md section 9): no world
    declares a law; every JSON object is the engine's world to parse. Kept for the
    cancelled importers; read by nothing living."""
    return isinstance(document, dict)


# THE RETIRED KEYS OF THE TAKE AND THE DECLARED RESIDUE (ALGEBRA.md 9.19 (3),
# 9.22 (4); BUILD.md section 26 items 14 and 15): each refused by name with
# what stands in its place, on the world, a family, a measured event, an
# emitter and a detector set alike.
RETIRED_KEYS = {
    # ONE ENGINE, NO LAW'S NAME AND NO VERSION (ALGEBRA.md 9.90 (1); records 2103, 2107)
    "law": "one engine, no law's name and no version (ALGEBRA.md 9.90 (1)); no world declares a law",
    "model_id": "one engine, no identity string (ALGEBRA.md 9.90 (1)); the file's name is its name",
    "detector_law": "one engine (ALGEBRA.md 9.90 (1), record 2103): the flag was the law's "
    "name; every world is the engine's",
    "input": "the file's stamp is `stamp` {hash}, the digest alone (ALGEBRA.md 9.90 (3) (c)); "
    "no law identifier",
    "absorbing": "the take retired: every detector books the one-way flux into its Nodes (9.19 (3))",
    "take": "the take retired: nothing absorbs, no Port follows a wave (9.19 (3))",
    "emits": "a body emits by its excited records' clicks, the key `emitter` (9.17 (4))",
    "own_grace": "the emitter's grace retired with the take (9.17, 9.19 (3))",
    "wheel": "the rung's wheel is the record's own, W = 3 den / gcd(num, 3 den) at its giving "
    "Node, given with its residue from the law (9.22 (4)); no set, world or emitter declares one",
    "residue_order": "the residue is the law's: the clicking record's rule remainder at the "
    "giving Node (9.22 (4)); no order is declared",
    "residue_seed": "the residue is the law's: the clicking record's rule remainder at the "
    "giving Node (9.22 (4)); no seed is declared",
    # the cavity of form (I) (MASSIVE_RECORD.md section 4, a record held
    # by mirror faces of its own): refused by name since 2026-09-25 (the
    # model owner's rule through the Boss; BUILD.md section 26 item 28)
    "cavity": "the cavity retired: a body's record is held by the law alone, its border the "
    "world's, no mirror faces of its own (BUILD.md section 26 item 28)",
    # the dielectric coupling of MASSIVE_RECORD.md section 7 (the response
    # records, the receive and source terms, the folded denominators):
    # refused by name since 2026-09-25 (the model owner's decision (2) of
    # record 1962; ALGEBRA.md 9.34 (B); BUILD.md section 26 item 30)
    "coupling": "the coupling retired: mass and light meet only at the click, in whole "
    "numbers (ALGEBRA.md 9.34 (B); BUILD.md section 26 item 30)",
    # THE FAMILY GENERICITY (the model owner's record 2066; BUILD.md section
    # 26 item 51): the engine knows no family's role; the family whose level
    # is the Node clock declares `held: "content"`, the family of charge
    # `held: "charge"`, and every family that reads them declares `reads`
    # with the weight Lambda on the charge's line
    "clock_family": "the family genericity: a family's role is its own declaration; the family "
    'of clicks declares `held: "content"` in `families` and the families that read it declare '
    "`reads` (record 2066; BUILD.md section 26 item 51)",
    "charge_family": 'the family genericity: the family of charge declares `held: "sign"` '
    'in `families` and a charged family reads it by `reads` with `by: "sign"` (record '
    "2066; BUILD.md section 26 item 51)",
    "charge_strength": "the family genericity: Lambda is the `weight` of the reading family's "
    "`reads` entry on the family of charge (record 2066; BUILD.md section 26 item 51)",
    # THE WINDOW IS THE ONE GIVING (ALGEBRA.md 9.85 (5), 9.71 (1); record 2082 (4);
    # the one stroke's commit 7): the point emitter is the law, no key; the given
    # train is retired, its paths marked CANCELLED and disconnected (record 2102)
    "point_emitter": "the window is the law's one giving: every emitter gives by its "
    "rotation written into the given row at its Node at its `weight` (ALGEBRA.md 9.85 (5), "
    "9.71 (1); commit 7); no world key",
    "train": "the given train is retired: every giving is the window's, its length, shape "
    "and wave number from the window and the given family's dispersion (ALGEBRA.md 9.85 "
    "(5), 9.71 (1); commit 7)",
    "given": "the given train's profile is retired with the train: the window writes the "
    "given row (ALGEBRA.md 9.85 (5), 9.71 (1); commit 7)",
}


def _refuse_retired(value: object, label: str, keys: tuple[str, ...]) -> None:
    """A retired key on `value` (an object) is refused naming the key and its
    successor; the loader accepts no world written under the retired forms."""
    if not isinstance(value, dict):
        return
    for key in keys:
        if key in value:
            raise ValueError(
                f"{label}.{key} is refused: {RETIRED_KEYS[key]} "
                "(a retired key; BUILD.md section 26 item 15)"
            )


def _object(value: object, label: str, allowed: set[str], required: set[str]) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    retired = [key for key in (*REVERSIBLE_KEYS, "headings", "heading") if key in value]
    if retired:
        raise ValueError(
            f"{label} declares {', '.join(retired)}, a key of the deleted law of "
            "events or its reversible detector (see docs/MIGRATION.md; a lamp and a ray declare "
            "`directions` and `direction`)"
        )
    unknown = set(value) - allowed
    if unknown:
        raise ValueError(f"{label} has unknown keys: {', '.join(sorted(unknown))}")
    missing = required - set(value)
    if missing:
        raise ValueError(f"{label} lacks keys: {', '.join(sorted(missing))}")
    return {str(key): item for key, item in value.items()}


def _integer(value: object, label: str, minimum: int, maximum: int = AMOUNT_BOUND) -> int:
    if type(value) is not int or value < minimum or value > maximum:
        raise ValueError(f"{label} must be an integer from {minimum} through {maximum}")
    return value


def _ratio(value: object, label: str, zero: bool) -> tuple[int, int]:
    """A rate n / d as `[n, d]` (n from 0 with `zero`, d positive) or one integer."""
    if type(value) is int:
        return _integer(value, label, 0 if zero else 1), 1
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{label} must be an integer or [numerator, denominator]")
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
            f"{label} must be an integer or [numerator, denominator], the charge per unit of content"
        )
    numerator = _integer(value[0], f"{label} numerator", -MAX_VALUE, MAX_VALUE)
    denominator = _integer(value[1], f"{label} denominator", 1, MAX_VALUE)
    return numerator, denominator


def _address(value: object, label: str, shape: Address3) -> Address3:
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{label} must be three integers")
    components: list[int] = []
    for item, extent in zip(value, shape, strict=True):
        if type(item) is not int or item < 0 or item >= extent:
            raise ValueError(
                f"{label} components must be integers on the GameBoard, from 0 "
                f"through the extent less one on each axis of the shape {list(shape)}"
            )
        components.append(item)
    return components[0], components[1], components[2]


def _vector(value: object, label: str, bound: int) -> Vector:
    """A primitive integer vector with every component in -bound .. bound."""
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{label} must be three integers")
    components: list[int] = []
    for item in value:
        if type(item) is not int or item < -bound or item > bound:
            raise ValueError(f"{label} components must be integers from {-bound} through {bound}")
        components.append(item)
    found = (components[0], components[1], components[2])
    if found == (0, 0, 0):
        raise ValueError(f"{label} must not be the zero vector (the rest slots are the table's)")
    if bounded_gcd(bounded_gcd(found[0], found[1]), found[2]) != 1:
        raise ValueError(f"{label} must be a primitive vector (its components coprime)")
    return found[0], found[1], found[2]


def _direction_table(value: object, bound: int) -> tuple[Vector, ...]:
    """The table `D`: the two rest vectors, the six headings, the declared."""
    table: list[Vector] = [(0, 0, 0), (0, 0, 0), *PORT_HEADINGS]
    if not isinstance(value, list):
        raise ValueError("directions must be a list of integer vectors")
    for index, item in enumerate(value):
        vector = _vector(item, f"directions[{index}]", bound)
        if vector in table:
            raise ValueError(f"directions[{index}] repeats a direction of the table")
        table.append(vector)
    if len(table) > MAX_DIRECTIONS:
        raise ValueError(f"the direction table holds at most {MAX_DIRECTIONS} entries")
    return tuple(table)


def _direction(value: object, label: str, table: tuple[Vector, ...], *, rest: bool = False) -> int:
    """A direction named by its vector or by its index in the world's table;
    a rest vector only where `rest` allows it (a ray in transit)."""
    if type(value) is int:
        index = _integer(value, label, 0, len(table) - 1)
    else:
        if not isinstance(value, list) or len(value) != 3 or any(type(v) is not int for v in value):
            raise ValueError(f"{label} must be a direction vector or an index of the table")
        vector = (value[0], value[1], value[2])
        if vector not in table:
            raise ValueError(
                f"{label} names a direction the world does not declare {list(vector)} "
                "(the six headings or a vector of `directions`)"
            )
        index = table.index(vector)
    if index < REST_DIRECTIONS and not rest:
        raise ValueError(f"{label} must not be a rest direction")
    return index


def _directions(value: object, label: str, table: tuple[Vector, ...]) -> tuple[int, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a nonempty list of directions")
    found = tuple(_direction(item, label, table) for item in value)
    if len(set(found)) != len(found):
        raise ValueError(f"{label} repeats a direction")
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
        raise ValueError(f"{label} must be three odd integers from 1")
    found = []
    for item, extent in zip(value, shape, strict=True):
        span = _integer(item, label, 1, extent)
        if span % 2 == 0:
            raise ValueError(f"{label} must be three odd integers from 1 (a centred body)")
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
            "age_bound is required on a GameBoard periodic on every axis: no ray "
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
        and all(item in BOUNDARIES or item == CLOSED_FACE for item in value.values())
    ):
        declared = {str(key): str(item) for key, item in value.items()}
        wraps = tuple(declared.get(axis, BOUNDARIES[0]) == BOUNDARIES[1] for axis in AXES)
        return declared, (wraps[0], wraps[1], wraps[2])
    raise ValueError(
        "the GameBoard is open (its edge is infinity) unless an axis is declared "
        'periodic (boundary "open" or an object of "x", "y", "z" to "open" or "periodic", or '
        '"closed" per axis: a zero face without the take); '
        "a closed GameBoard is refused (the string, and any other word)"
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
            f'{label} must be an object of column name to {{"value": n or [n, d], "sign": 1 or -1}}'
        )
    found: dict[str, tuple[tuple[int, int], int]] = {}
    for name, entry in value.items():
        column = f"{label}[{name!r}]"
        if name == GRAVITY_COLUMN:
            raise ValueError(
                f"{column} declares the built-in column {GRAVITY_COLUMN!r} (the value "
                "[1, 1] on every unit of content of every family with the sign minus; never declared)"
            )
        if name == CHARGE_COLUMN and charged:
            raise ValueError(
                f"{column} and the key `charge` declare the column {CHARGE_COLUMN!r} "
                "twice on one family (`charge` is the shorthand for `columns.charge`; declare one)"
            )
        obj = _object(entry, column, COLUMN_KEYS, COLUMN_KEYS)
        sign = obj["sign"]
        if type(sign) is not int or sign not in COLUMN_SIGNS:
            raise ValueError(
                f"{column}.sign must be 1 (like values push apart) or -1 (like values "
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
            f"{label} must be one integer (a scalar): the flight gives every "
            "direction one speed, so L intervals of flight reach a sphere; a per-axis lifetime "
            "is refused"
        )
    lifetime = _integer(value, label, 1)
    if lifetime > age_bound:
        raise ValueError(
            f"{label} {lifetime} is beyond the world's age_bound {age_bound}: an "
            "event at the age L is still on the GameBoard at the end of its walk (declare a "
            "larger age_bound or a shorter lifetime)"
        )
    return lifetime


def _pair_bound(
    numerator: int,
    denominator: int,
    label: str,
    bound: int = AMPLITUDE_BOUND,
    node_clock: int = 1,
    content: int = 0,
) -> None:
    """The load bound of a pair (Reviewer 3's MUST 3) under the Node clock
    (ALGEBRA.md 9.57 (2), 9.61 (3); BUILD.md section 26 items 31, 34 and 44):
    the weak-field rule's total at a Node under the amplitude bound A (the
    world's `amplitude_bound`), 6 A R + A |S| + w (A + 1) with the rule's
    integers (R, S, w) at the vacuum's level and at the content M, below
    2^63, Gamma the world's `node_clock` and M the content at the Node (the
    world's whole content at the second pass, `_node_clock_bound`; the plain
    rule at Gamma = 1 and M = 0, the first pass on the pair alone); refused
    otherwise naming the bound, the clock, the content and the pair."""
    # THE BOUND FROM THE RULE'S OWN INTEGERS (ALGEBRA.md 9.57 (2), 9.61 (3);
    # BUILD.md section 26 item 44): 6 A R + A |S| + w (A + 1) with (R, S, w)
    # the weak-field rule's coefficients at the level 0 and at the level M
    # (the two levels a Node can read: the vacuum's and a body's), the larger;
    # the plain rule's at Gamma = 1 on the first pass over the pair alone
    # the level a Node can read stays below Gamma (the pace positive: the load's guard per
    # body, `_node_clock_bound`, and the run's, `_advance_fields`), so the reach is read there
    weak_field = node_clock > 1
    reach = min(content, node_clock - 1) if weak_field else content
    total = max(
        rule_total_bound(numerator, denominator, node_clock, level, bound, weak_field)
        for level in (0, reach)
    )
    if total >= TOTAL_BOUND:
        raise ValueError(
            f"{label}.pair [{numerator}, {denominator}]"
            + ": the rule's total 6 A R + A |S| + w (A + 1) at the amplitude bound A = "
            f"{bound}, the Node clock Gamma = {node_clock} and the content M = {content} (read at "
            f"the level {reach}) is {total}, not below 2^63 (the bound of the rows' int64; ALGEBRA.md 9.57 (2) and "
            "9.61 (3), BUILD.md section 26 item 44)"
        )


def _held_bodies_checks(
    families: tuple[FamilyDefinition, ...], measured: tuple[MeasuredDefinition, ...]
) -> None:
    """A held family takes and gives nothing (ALGEBRA.md 9.45 (1), 9.48 (2);
    item 51): no measured event is of it, none holds its quanta, and no
    emitter givings into it; its level is written by the engine alone, the
    declared source at every body's Nodes."""
    for index, family in enumerate(families):
        if family.held is None or family.clicks is not None:
            # a family that is held and has clicks (the charge with light as its
            # wave, ALGEBRA.md 9.86 (2) (b)) has bodies of light's kind, a stock
            # and givings; its held part is the engine's write as any held family's
            continue
        name = family.name
        for number, entry in enumerate(measured):
            if entry.family == index:
                raise ValueError(
                    f"measured[{number}] is of the held family {name!r}: no body is of "
                    "it; its level is held at the bodies' Nodes, written by the engine at the "
                    "load and at every click (ALGEBRA.md 9.45 (2))"
                )
            if len(entry.held) > index and entry.held[index]:
                raise ValueError(
                    f"measured[{number}].stocks names the held family {name!r}: nothing "
                    "holds its quanta; its level is held at a body's Nodes (ALGEBRA.md 9.45 (2))"
                )
            if entry.block is not None and entry.block.emitter is not None:
                if entry.block.emitter.family == index:
                    raise ValueError(
                        f"measured[{number}].emitter givings into the held family "
                        f"{name!r}: it takes and gives nothing (ALGEBRA.md 9.45 (1))"
                    )


def _charge_labels(raw: object, families: tuple[FamilyDefinition, ...], detector_law: bool) -> None:
    """THE SIGN ON THE QUANTUM (ALGEBRA.md 9.48 (1); BUILD.md section 26 item
    35): under the detector law every family declares its `charge` q, one
    of -1, 0 and +1 per quantum (light 0, a matter family its own), no
    default; the label passes whole in the click, a body's charge Q the
    signed sum of the quanta it holds."""
    if not detector_law or not isinstance(raw, list):
        return
    for index, (entry, family) in enumerate(zip(raw, families, strict=True)):
        if not isinstance(entry, dict) or "charge" not in entry:
            raise ValueError(
                f"families[{index}] ({family.name!r}) declares no `charge`: under "
                f"every family declares the sign on its quantum, -1, 0 or +1, "
                "no default (ALGEBRA.md 9.48 (1); BUILD.md section 26 item 35)"
            )
        if family.charge[1] != 1 or abs(family.charge[0]) > 1:
            raise ValueError(
                f"families[{index}].charge {list(family.charge)}: under "
                f"the charge is the sign on the quantum, -1, 0 or +1 "
                "(ALGEBRA.md 9.48 (1))"
            )


def _node_clock_bound(
    families: tuple[FamilyDefinition, ...],
    measured: tuple[MeasuredDefinition, ...],
    amplitude_bound: int,
    node_clock: int,
) -> None:
    """THE LOAD BOUND UNDER THE NODE CLOCK (BUILD.md section 26 item 31), the
    second pass once the content is known: every family's pair and every
    block's pair against the rule's int64 total at the amplitude bound with
    the world's Gamma and M twice its whole content (the sum of every
    measured event's held quanta of every family is the most any one Node
    can hold, since the clicks move the quanta between the bodies and the
    givings return them to the board; the family of clicks' level around the
    bodies is bounded by the held content, and a wave of it off a zero face
    doubles, ALGEBRA.md 9.45 (2); BUILD.md section 26 item 32)."""

    # THE READS (ALGEBRA.md 9.45 (3), 9.48 (3); BUILD.md section 26 items 34,
    # 35 and 51): a family reads the pace Gamma - SUM weight x sign x level
    # over its reads; at a body's Nodes a held level is the body's source
    # (its content for "content", its signed charge for "charge"), so the
    # effective content a family reads there in size is at most SUM weight x
    # |source|, positive at the load at every body (the run's guard,
    # `_advance_fields`, holds it everywhere afterwards); the rows' int64
    # bound takes the reach of the effective content, twice the world's
    # sources weighted by the largest reads
    def source_of(family: FamilyDefinition, entry: MeasuredDefinition) -> int:
        quanta = sum(entry.held)
        if family.held == "sign":
            declared = entry.block.q if entry.block is not None else 0
            return abs(
                declared
                + sum(other.charge[0] * held for other, held in zip(families, entry.held, strict=True))
            )
        return quanta

    for number, entry in enumerate(measured):
        for family in families:
            reach = sum(
                weight * source_of(families[other], entry) for other, weight, _, _ in family.reads
            )
            if family.reads and reach >= node_clock:
                raise ValueError(
                    f"measured[{number}]: the pace of {family.name!r} could reach 0 at its "
                    f"Nodes: its reads weigh the body's sources to {reach} in size, not below Gamma = "
                    f"{node_clock} (ALGEBRA.md 9.48 (3): the charge's hill hastens a clock at most to "
                    "the vacuum's; BUILD.md section 26 items 34, 35 and 51)"
                )
    content = 0
    for family in families:
        reach = 2 * sum(
            weight * source_of(families[other], entry)
            for other, weight, _, _ in family.reads
            for entry in measured
        )
        content = max(content, reach)
    for index, family in enumerate(families):
        if family.pair_on_body:
            continue  # the bodies' kinds are read below (ALGEBRA.md 9.91 (7))
        _pair_bound(
            family.pair[0], family.pair[1], f"families[{index}]", amplitude_bound, node_clock, content
        )
    for number, entry in enumerate(measured):
        if entry.block is not None:
            _pair_bound(
                entry.block.pair[0],
                entry.block.pair[1],
                f"measured[{number}]",
                amplitude_bound,
                node_clock,
                content,
            )
            if families[entry.family].pair_on_body:
                _pair_bound(
                    entry.block.kind[0],
                    entry.block.kind[1],
                    f"measured[{number}].kind",
                    amplitude_bound,
                    node_clock,
                    content,
                )


def _kind_pair(
    obj: dict[str, object], label: str, massive_record: bool, amplitude_bound: int = AMPLITUDE_BOUND
) -> tuple[int, int] | None:
    """The family key `pair` (`massive-record-v1`): [num, den], two integers
    from 1 with den >= num (den > num a massive kind, den = num light's
    kind written out); refused without the world key `massive_record`, and
    with the integer `phase_per_link` on a massive kind (its phase per Link
    is its band's at its clock, never a declared turn; the pair form, the
    clock a matter lamp drives, is admitted) or with the massive rows' flag
    `massive` (one massive form per family)."""
    if "pair" not in obj:
        return MASSLESS_PAIR
    if not massive_record:
        raise ValueError(
            f"{label}.pair is refused without the world key `massive_record` "
            f"(the world key `massive_record`, absent by default)"
        )
    value = obj["pair"]
    if value == "body":
        # THE PAIR ON THE BODY (ALGEBRA.md 9.85 (3), 9.91 (7)): the family
        # declares none; every body (`kind`) and every given record (the
        # emitter's `pair`) declares its own; the placeholder here, the flag
        # `pair_on_body` on the family
        return None
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{label}.pair must be [num, den], the kind's pair")
    numerator = _integer(value[0], f"{label}.pair numerator", 1, MAX_VALUE)
    denominator = _integer(value[1], f"{label}.pair denominator", 1, MAX_VALUE)
    _pair_bound(numerator, denominator, label, amplitude_bound)
    if denominator < numerator:
        raise ValueError(
            f"{label}.pair [{numerator}, {denominator}]: a kind's pair has den >= num "
            "(den > num a massive kind, its gap cos omega_0 = num / den; den = num light's kind)"
        )
    if denominator > numerator:
        if "phase_per_link" in obj and not isinstance(obj["phase_per_link"], list):
            # The pair form is the family's clock (a matter lamp's train
            # carries the band, its phase per Link the rule's at that clock,
            # cos k = 3 den cos omega / num - 2 on a chain); the integer
            # form declares a turn per Link, no massive kind's to declare.
            raise ValueError(
                f"{label}.pair with the integer phase_per_link: a massive kind's phase "
                "per Link is its band's at its clock (the pair form), never a declared turn"
            )
        if obj.get("massive"):
            raise ValueError(
                f"{label} declares both `pair` (massive-record-v1) and `massive` "
                "(massive-rows-v1): one massive form per family"
            )
    return numerator, denominator


def _refuse_family_faces(obj: dict[str, object], label: str) -> None:
    """ONE BORDER FOR EVERY FAMILY (the model owner's rule through the Boss,
    2026-09-25; BUILD.md section 26 item 28): the family key `faces` (a
    massive kind's own border per axis, `massive-record-v1`, HISTORY) is
    refused by name; every family's rows read the world's `boundary`."""
    if "faces" in obj:
        raise ValueError(
            f"{label}.faces is refused: one border for every family, the world's "
            "`boundary` (a kind's own faces are HISTORY; BUILD.md section 26 item 28)"
        )


def _families(
    value: object,
    phase_steps: int,
    age_bound: int = AMOUNT_BOUND,
    massive_rows: bool = False,
    action: int | None = None,
    massive_record: bool = False,
    amplitude_bound: int = AMPLITUDE_BOUND,
    detector_law: bool = False,
) -> tuple[FamilyDefinition, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError("families must be a nonempty list")
    if len(value) > MOST_FAMILIES:
        raise ValueError(
            f"families declares {len(value)}; at most {MOST_FAMILIES} families on a "
            "GameBoard (the model owner's record 2081 of 2026-09-25: every family works in every "
            "experiment, the cap 20; record 1875's unification and its counts HISTORY)"
        )
    found: list[FamilyDefinition] = []
    declared: list[dict[str, tuple[tuple[int, int], int]]] = []
    # The world's columns beyond the two built in, in the order of their
    # first declaration, with the sign the first declaration gave; a later
    # family declaring another sign for the name is refused.
    names: list[str] = []
    signs: dict[str, tuple[int, int]] = {}
    # THE FAMILY GENERICITY (item 51): the three attributes per family, the
    # reads resolved by name once every family is read
    generic: list[FamilyAttributes] = []
    for index, entry in enumerate(value):
        if isinstance(entry, dict) and KIND_KEY in entry:
            raise ValueError(
                f"families[{index}] declares {KIND_KEY}, a key removed on 2026-09-19: "
                "the kind of a family follows from its quantum (0 free, 1 or more paid) and is "
                "not declared; see docs/MIGRATION.md"
            )
        _refuse_retired(entry, f"families[{index}]", ("take",))
        obj = _object(entry, f"families[{index}]", FAMILY_KEYS, {"name", "quantum"})
        if detector_law:
            # NO DEFAULT UNDER THE DETECTOR LAW (record 2089; item 57): the pair,
            # the charge and the reads declared (the clock `phase_per_link` on the
            # given family, 9.62 (1)); the ray law's phase, lifetime, hand, columns
            # and massive flag never read, refused
            _require_under_law(
                obj,
                f"families[{index}]",
                {"pair", "charge", "reads"} if massive_record else {"charge", "reads"},
            )
            _refuse_under_law(
                obj,
                f"families[{index}]",
                {"phase", "lifetime", "hand", "columns", "massive"},
            )
        name = obj["name"]
        if not isinstance(name, str) or not name:
            raise ValueError(f"families[{index}].name must be a nonempty string")
        if any(item.name == name for item in found):
            raise ValueError(f"two families named {name!r}")
        quantum = _integer(obj["quantum"], f"families[{index}].quantum", FREE_QUANTUM, MAX_VALUE)
        columns = _declared_columns(
            obj.get("columns", {}), f"families[{index}].columns", "charge" in obj
        )
        charge_value = columns.pop(CHARGE_COLUMN, None)
        if charge_value is not None and charge_value[1] != 1:
            raise ValueError(
                f"families[{index}].columns[{CHARGE_COLUMN!r}].sign must be 1: the "
                "electric column's sign is plus (like charges push apart)"
            )
        charge = (
            charge_value[0]
            if charge_value is not None
            else _signed_ratio(obj.get("charge", 0), f"families[{index}].charge")
        )
        if quantum != FREE_QUANTUM and charge[1] != 1:
            raise ValueError(
                f"families[{index}].charge: a paid family's charge is per unit of "
                f"amount and whole (an integer; the pair {list(charge)} is refused on {name!r}; D-1, "
                "2026-09-20)"
            )
        for column, ((numerator, _), sign) in columns.items():
            if quantum != FREE_QUANTUM and numerator:
                raise ValueError(
                    f"a paid family (quantum {quantum}) carries no column value "
                    f"({name}, the column {column!r}: its rays push by their content)"
                )
            if column not in signs:
                signs[column] = (sign, index)
                names.append(column)
            elif signs[column][0] != sign:
                raise ValueError(
                    f"families[{index}].columns[{column!r}].sign {sign} differs from "
                    f"the sign {signs[column][0]} families[{signs[column][1]}] declared: a column's "
                    "sign is the column's, one per name across the world"
                )
        phase = obj.get("phase", True)
        if type(phase) is not bool:
            raise ValueError(f"families[{index}].phase must be true or false")
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
                    f"{turn_key} [{per_age[0]}, {per_age[1]}]: (age_bound + 1) x n "
                    f"= {age_bound + 1} x {per_age[0]} exceeds the integer bound {AMOUNT_BOUND}"
                )
            per_link = 0
        else:
            per_link = _integer(declared_turn, turn_key, 0, phase_steps - 1)
        if (per_link or per_age is not None) and not phase:
            raise ValueError(f"{turn_key} is refused for a family without a phase circle")
        lifetime = _lifetime(obj.get("lifetime"), f"families[{index}].lifetime", age_bound)
        hand = _hand(obj["hand"], f"families[{index}].hand") if "hand" in obj else NO_HAND
        massive = _massive(obj, f"families[{index}]", massive_rows, action, quantum, phase, name)
        declared_pair = _kind_pair(obj, f"families[{index}]", massive_record, amplitude_bound)
        pair = MASSLESS_PAIR if declared_pair is None else declared_pair
        if detector_law and "phase_per_link" in obj and not isinstance(obj["phase_per_link"], list):
            # under the law a family's clock is the pair form (ALGEBRA.md 9.17 (6));
            # the integer form is the ray law's turn per Link
            raise ValueError(
                f"families[{index}].phase_per_link is an integer: a "
                "family declares the pair form of its clock [p, q] or none, the given record's "
                "clock then its emitter's (ALGEBRA.md 9.17 (6), 9.85 (3))"
            )
        _refuse_family_faces(obj, f"families[{index}]")
        generic.append(_family_generic(obj, f"families[{index}]", detector_law))
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
                pair=pair,
                pair_on_body=declared_pair is None,
            )
        )
        declared.append(columns)
    if 2 + len(names) > COLUMN_LIMIT:
        raise ValueError(
            f"the world declares {len(names)} columns beyond gravity and charge; at most "
            f"{COLUMN_LIMIT} columns in all (the per-group work of the push is fixed)"
        )
    # Every family's columns aligned with the world's: (0, 1) where it
    # names none; the reads resolved by name (item 51)
    family_names = [family.name for family in found]
    families = tuple(
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
            pair=family.pair,
            held=attributes.held,
            reads=_resolve_reads(attributes.reads, family_names, f"families[{index}]"),
            parts=attributes.parts,
            levels=attributes.levels,
            held_factors=attributes.held_factors,
            held_dipole=attributes.held_dipole,
            held_dipole_div=attributes.held_dipole_div,
            self_unit=attributes.self_unit,
            clicks=attributes.clicks,
            pair_on_body=family.pair_on_body,
        )
        for index, (family, columns, attributes) in enumerate(zip(found, declared, generic, strict=True))
    )
    _held_family_shapes(families, detector_law)
    return families


HELD_SOURCES = ("content", "sign")
READ_BY = ("plain", "sign")


class FamilyAttributes(NamedTuple):
    """What a family is, as declared (items 51 and 53; ALGEBRA.md 9.86 (3), 9.91
    (7)): the reads by name, resolved after every family is read."""

    held: str | None
    parts: tuple[int, ...]
    levels: int
    held_factors: tuple[int, ...]
    held_dipole: str | None
    held_dipole_div: int
    self_unit: int
    clicks: tuple[bool, bool] | None
    reads: list[tuple[str, int, str, int | str]]


def _family_generic(obj: dict[str, object], label: str, detector_law: bool) -> FamilyAttributes:
    """THE FAMILY GENERICITY (the model owner's record 2066; BUILD.md section
    26 item 51) AND THE COMPLETE ATTRIBUTE SET (ALGEBRA.md 9.86 (3), 9.91 (7);
    the one stroke, commit 1): the family's own declaration of what it is,
    `held` (with `held_factors`, `held_dipole`, `held_dipole_div`), `parts`,
    `levels`, `self_unit`, `clicks` and `reads` (the reads by name, resolved
    after every family is read). Admitted under `detector_law` alone; under
    it every family declares `reads` (a field family with no waves the empty
    list: the plain rule), no default. The booking is derived (item 53):
    exactly a family with clicks; an inline entry without `clicks` is a
    family of records unless held (the tests' small lists)."""
    keys = [
        key
        for key in (
            "held",
            "reads",
            "parts",
            "levels",
            "self_unit",
            "clicks",
            "held_factors",
            "held_dipole",
            "held_dipole_div",
        )
        if key in obj
    ]
    if keys and not detector_law:
        raise ValueError(
            f"{label} declares {', '.join(keys)}, refused without `detector_law` (a "
            "family's held source, reads and representation are the local detector law's; BUILD.md "
            "section 26 item 51)"
        )
    held: str | None = None
    if "held" in obj:
        held_value = obj["held"]
        if held_value not in HELD_SOURCES:
            raise ValueError(
                f"{label}.held must be one of {list(HELD_SOURCES)}: the source a body's "
                "record writes at its Nodes, its held quanta or their signed sum (ALGEBRA.md 9.45 "
                "(2), 9.48 (1); BUILD.md section 26 item 51)"
            )
        held = str(held_value)
    if "components" in obj:
        raise ValueError(
            f"{label}.components is refused: the representation is `parts`, a list "
            "([1], [1, 3] or [1, 3, 6]; ALGEBRA.md 9.86 (2), 9.91 (1))"
        )
    parts_value = obj.get("parts", [1])
    if not isinstance(parts_value, list) or tuple(parts_value) not in PARTS_FORMS:
        raise ValueError(
            f"{label}.parts must be one of {[list(form) for form in PARTS_FORMS]}: the "
            "representation as a list of parts, the time part first (ALGEBRA.md 9.86 (2), 9.91 (1))"
        )
    parts = tuple(int(part) for part in parts_value)
    levels = obj.get("levels", 2)
    if levels not in (1, 2):
        raise ValueError(f"{label}.levels must be 1 or 2 (ALGEBRA.md 9.91 (1))")
    # THE SELF-SOURCE'S UNIT P_2 (ALGEBRA.md 9.78 (3), 9.91 (5), 9.97; commit 6): 0 turns
    # the line off (every shipped family: 9.97 derives 0 for gravity's t part and a
    # computed P_2 whose term is 0 in integers on every shipped world); above 0 the
    # engine subtracts (the six squared differences summed over the components) div P_2
    # from the step; the bound 24 A is checked on the file's entries with the universe's
    # A (`families_file_entries`)
    self_unit = _integer(obj.get("self_unit", 0), f"{label}.self_unit", 0)
    held_factors: tuple[int, ...] = tuple(1 for _ in parts)
    held_dipole: str | None = None
    held_dipole_div = 1
    for key in ("held_factors", "held_dipole", "held_dipole_div"):
        if key in obj and held is None:
            raise ValueError(f"{label}.{key} is refused on a family that holds nothing")
    if "held_factors" in obj:
        value = obj["held_factors"]
        if (
            not isinstance(value, list)
            or len(value) != len(parts)
            or any(type(item) is not int or item < 1 for item in value)
        ):
            raise ValueError(
                f"{label}.held_factors must be {len(parts)} integers from 1, one per part "
                "(ALGEBRA.md 9.91 (3): the held factors are the families file's numbers)"
            )
        held_factors = tuple(int(item) for item in value)
    if "held_dipole" in obj:
        if obj["held_dipole"] not in HELD_DIPOLES:
            raise ValueError(
                f"{label}.held_dipole must be one of {list(HELD_DIPOLES)}, the body's "
                "number written on its Node's six neighbours (ALGEBRA.md 9.91 (3))"
            )
        held_dipole = str(obj["held_dipole"])
        if len(parts) < 2:
            raise ValueError(
                f"{label}.held_dipole is refused on a scalar family: the dipole is "
                "written into the vector part (ALGEBRA.md 9.91 (3))"
            )
    if "held_dipole_div" in obj:
        held_dipole_div = _integer(obj["held_dipole_div"], f"{label}.held_dipole_div", 1)
    clicks: tuple[bool, bool] | None = None
    if "clicks" in obj:
        value = _object(obj["clicks"], f"{label}.clicks", {"gives", "takes"}, {"gives", "takes"})
        if value["gives"] is not True or value["takes"] is not True:
            raise ValueError(
                f"{label}.clicks.gives and .takes must be true: a family of records is "
                "given and taken at clicks (ALGEBRA.md 9.79 (1))"
            )
        clicks = (True, True)
    elif held is None:
        clicks = (True, True)
    reads: list[tuple[str, int, str, int | str]] = []
    if detector_law and "reads" not in obj:
        raise ValueError(
            f"{label} declares no `reads`: the held families "
            "whose levels enter the family's pace, with their weights (an empty list for a held "
            "family: the plain rule), no default (ALGEBRA.md 9.45 (3), 9.48 (3); BUILD.md section "
            "26 item 51)"
        )
    raw_reads = obj.get("reads", [])
    if not isinstance(raw_reads, list):
        raise ValueError(f"{label}.reads must be a list of {{family, weight, by, twist}}")
    for position, item in enumerate(raw_reads):
        read = _object(
            item,
            f"{label}.reads[{position}]",
            {"family", "weight", "by", "twist"},
            {"family", "weight"},
        )
        name = read["family"]
        if not isinstance(name, str) or not name:
            raise ValueError(f"{label}.reads[{position}].family must name a family")
        weight = _integer(read["weight"], f"{label}.reads[{position}].weight", 1, AMOUNT_BOUND)
        by = read.get("by", "plain")
        if by not in READ_BY:
            raise ValueError(
                f"{label}.reads[{position}].by must be one of {list(READ_BY)}: the level "
                "enters the pace as weight x level (plain) or as - q x weight x level, q the "
                "reading family's own charge sign (sign; ALGEBRA.md 9.48 (3))"
            )
        twist_value = read.get("twist", 0)
        twist: int | str
        if type(twist_value) is int and twist_value >= 0:
            twist = twist_value
        elif isinstance(twist_value, str) and twist_value in READ_TWIST_WORDS:
            twist = twist_value
        else:
            raise ValueError(
                f"{label}.reads[{position}].twist must be an integer from 0 or one of "
                f"{list(READ_TWIST_WORDS)} (the transport's angle per read, ALGEBRA.md 9.81 (2), "
                "9.91 (6))"
            )
        if any(other == name for other, _, _, _ in reads):
            raise ValueError(f"{label}.reads names {name!r} twice")
        reads.append((name, weight, str(by), twist))
    if held is not None and reads and clicks is None:
        raise ValueError(
            f"{label} is held and reads {[name for name, _, _, _ in reads]}: a field "
            "family with no waves steps by the plain rule at the pace 1 of its own and reads no "
            "level (ALGEBRA.md 9.45 (2); BUILD.md section 26 item 51)"
        )
    return FamilyAttributes(
        held, parts, levels, held_factors, held_dipole, held_dipole_div, self_unit, clicks, reads
    )


def _resolve_reads(
    reads: list[tuple[str, int, str, int | str]], names: list[str], label: str
) -> tuple[tuple[int, int, str, int | str], ...]:
    """The reads by name to the families' indices; a read names a declared
    family (the names listed)."""
    out: list[tuple[int, int, str, int | str]] = []
    for name, weight, by, twist in reads:
        if name not in names:
            raise ValueError(
                f"{label}.reads names {name!r}, which no family declares (the families: {names})"
            )
        out.append((names.index(name), weight, by, twist))
    return tuple(out)


def _held_family_shapes(families: tuple[FamilyDefinition, ...], detector_law: bool) -> None:
    """A held family's shape by attribute (ALGEBRA.md 9.41 (3), 9.45 (1),
    9.48 (2); item 51): the pair [1, 1] (massless: the only pair whose
    static solutions reach), the quantum 1 (one click writes one unit), no
    clock of its own (it givings nothing), its own charge 0 (its level is
    the source it holds, it carries none); a read names a held family; under the
    detector law at most one family holds each source (the level every
    other family reads is one array)."""
    for index, family in enumerate(families):
        label = f"families[{index}] ({family.name!r})"
        if family.held is not None:
            if family.pair != MASSLESS_PAIR:
                raise ValueError(
                    f"{label} is held with the pair {list(family.pair)}: a held family "
                    "is massless, its pair [1, 1], the only pair whose static field reaches "
                    "(ALGEBRA.md 9.41 (3), 9.45 (1))"
                )
            if family.quantum != 1:
                raise ValueError(
                    f"{label} is held with the quantum {family.quantum}: a held family "
                    "is counted in quanta, one click one unit (`quantum` 1; ALGEBRA.md 9.45 (1))"
                )
            if family.phase_per_age is not None or family.phase_per_link:
                raise ValueError(
                    f"{label} is held and declares phase_per_link: a held family "
                    "givings nothing and has no clock of its own (ALGEBRA.md 9.45 (1))"
                )
            if family.charge[0] != 0:
                raise ValueError(
                    f"{label} is held and declares the charge {family.charge[0]}: a held "
                    "family carries none, its level is the source it holds (ALGEBRA.md 9.48 (2))"
                )
        for other, _, _, _ in family.reads:
            if families[other].held is None:
                raise ValueError(
                    f"{label}.reads names {families[other].name!r}, which is not held: "
                    "a family's pace reads the held families' levels alone (ALGEBRA.md 9.45 (3), "
                    "9.48 (3); BUILD.md section 26 item 51)"
                )
    if detector_law:
        for source in HELD_SOURCES:
            holders = [family.name for family in families if family.held == source]
            if len(holders) > 1:
                raise ValueError(
                    f"two families hold {source!r}: {holders}; one family holds each "
                    "source (the level the others read is one array; BUILD.md section 26 item 51)"
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
        raise ValueError(f"{label}.massive must be true or false")
    if not massive:
        return False
    if not massive_rows:
        raise ValueError(
            f"{label}.massive is refused without the world key `massive_rows` "
            f"(the identity massive-rows beside the law, absent by default)"
        )
    if "phase_per_link" in obj:
        raise ValueError(
            f"{label}.massive is refused with phase_per_link (the integer or the "
            f"pair): a massive row turns |p_a| x N / h at every axis Link it crosses, by "
            "de Broglie, never per Link count and never per interval of age"
        )
    if quantum == FREE_QUANTUM:
        raise ValueError(
            f"{label}.massive is refused on the free family {name!r} (quantum 0): a "
            "free family's rows are a body's field; a massive family is paid, its quantum the "
            "content M of one row"
        )
    if not phase:
        raise ValueError(
            f"{label}.massive is refused on the family {name!r} without a phase "
            "circle: a massive row turns its phase by its momentum at every axis Link"
        )
    if action is None:
        raise ValueError(
            f"{label}.massive needs the world's `action` (the quantum h of the "
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
        raise ValueError(f"{label} must be -1 or 1 (the two hands; a row without one has 0)")
    return value


def _axis(value: object, label: str) -> int:
    """The axial record of a measured event: one of the six headings in
    Port order, declared as its vector ([1, 0, 0] .. [0, 0, -1]); the
    index of the heading in the world's direction table."""
    if not isinstance(value, list) or len(value) != 3 or any(type(v) is not int for v in value):
        raise ValueError(f"{label} must be one of the six headings as a vector, [1, 0, 0] .. [0, 0, -1]")
    vector = (value[0], value[1], value[2])
    if vector not in PORT_HEADINGS:
        raise ValueError(
            f"{label} {list(vector)} is not one of the six headings (an axis is a "
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
    product of a family with a hand h is given only on the parent's
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
                    f"{label}.products[{k}] ({families[family].name!r}, hand {hand:+d}) "
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
            f"{label}.phase_width is refused on pass: a width is a width of a "
            "response, and pass responds to nothing"
        )
    if not phased:
        raise ValueError(
            f"{label}.phase_width is refused for a family without a phase circle: "
            "its rays carry no phase to read"
        )
    if "phase_window" not in obj:
        raise ValueError(
            f"{label}.phase_width needs the window's setting `phase_window` (a "
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
                f"{label}: the momentum label {scale} x {content} x {amount} = "
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
    detector_law: bool = False,
) -> LampDefinition:
    obj = _object(value, label, LAMP_KEYS, {"rate", "wheel"})
    rate = _ratio(obj["rate"], f"{label}.rate", zero=True)
    if not isinstance(obj["wheel"], list):
        raise ValueError(
            f"{label}.wheel must be [r, W], the rate of the giving wheel (the record's "
            "coordinate u on the ladder advances by r over W at every giving; [1, N] the count of "
            "givings mod N)"
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
                f"{label}.phase_window is refused on a lamp of a family without a "
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
                f"{label}.arms {arms} does not divide the {len(directions)} directions "
                "(every arm takes the same number of directions, in order)"
            )
    # The order channel's two keys (DECLARATIONS.md section 2 item 8): on a
    # pair lamp under the local detector law `residue_order` is required
    # with no default (an implicit default to the open-channel form is
    # against AGENTS.md); on any other lamp the keys are not admitted.
    residue_order: str | None = None
    residue_seed: int | None = None
    if detector_law and arms > 1:
        if "residue_order" not in obj:
            raise ValueError(
                f"{label}.residue_order is required on a pair lamp (a lamp with arms) "
                'under the local detector law, "ordinal" or "seed", with no default '
                "(DECLARATIONS.md section 2 item 8)"
            )
        declared = obj["residue_order"]
        if declared not in ("ordinal", "seed"):
            raise ValueError(
                f'{label}.residue_order must be "ordinal" (the counter form, u = '
                '(ordinal - 1) r mod W) or "seed" (the seed-set order of the residues)'
            )
        residue_order = str(declared)
        if residue_order == "seed":
            if "residue_seed" not in obj:
                raise ValueError(
                    f'{label}.residue_seed is required under residue_order "seed" '
                    "(an integer in [0, 2^64), the key of the givings' order, drawn once per world)"
                )
            residue_seed = _integer(obj["residue_seed"], f"{label}.residue_seed", 0, (1 << 64) - 1)
            if wheel[0] != 1:
                raise ValueError(
                    f"{label}.wheel [{wheel[0]}, {wheel[1]}]: the stride r must be 1 "
                    'under residue_order "seed" (W givings take every residue once by the order)'
                )
        elif "residue_seed" in obj:
            raise ValueError(
                f'{label}.residue_seed is refused under residue_order "ordinal" '
                "(a key that does nothing is refused)"
            )
    else:
        for key in ("residue_order", "residue_seed"):
            if key in obj:
                raise ValueError(
                    f"{label}.{key} is not admitted on a lamp without arms"
                    + ("" if detector_law else " or outside the local detector law")
                    + " (the giving wheel's form as built, no far setting to hide)"
                )
    branches: tuple[tuple[int, int], ...] = ((0, 1),)
    label_hands: tuple[int, int] | None = None
    if "branches" in obj:
        branches, label_hands = _branches(obj["branches"], f"{label}.branches", arms)
    # The lamp's hand (`hand-v1`): declared on a lamp of a family without a
    # hand, or the family's own value repeated; a lamp of a branched family
    # whose labels carry the hands declares neither, and a family with a
    # hand cannot giving a record whose labels name hands (one or the other
    # per family, so that a row's hand is defined once).
    hand = NO_HAND
    if "hand" in obj:
        hand = _hand(obj["hand"], f"{label}.hand")
        if family_hand and hand != family_hand:
            raise ValueError(
                f"{label}.hand {hand:+d} differs from the family's hand {family_hand:+d}: "
                "a lamp of a chiral family releases the family's hand"
            )
    if label_hands is not None and (hand or family_hand):
        raise ValueError(
            f"{label}.branches name the hands of their labels and the "
            f"{'lamp' if hand else 'family'} declares a hand: a family carries its hand as the "
            "row's column or as the meaning of a label bit, never both"
        )
    # The momentum label's magnitude p of a massive family's rows
    # (`massive-rows-v1`): required on the lamp of a massive family (its
    # rows' label p_D per direction is formed at the scale p), refused on
    # any other lamp, an integer from 1 (a row at rest is not a massive
    # row's giving).
    momentum_magnitude: int | None = None
    if "momentum_magnitude" in obj:
        if not massive:
            raise ValueError(
                f"{label}.momentum_magnitude belongs to the lamp of a massive family "
                "(the family key `massive` under the world key `massive_rows`); this family is "
                "not massive"
            )
        momentum_magnitude = _integer(obj["momentum_magnitude"], f"{label}.momentum_magnitude", 1)
    elif massive:
        raise ValueError(
            f"{label} lacks keys: momentum_magnitude (the lamp of a massive family "
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
        residue_order=residue_order,
        residue_seed=residue_seed,
        hand=hand,
        label_hands=label_hands,
        momentum_magnitude=momentum_magnitude,
        train=None if "train" not in obj else _integer(obj["train"], f"{label}.train", 1),
        own_grace=None
        if "own_grace" not in obj
        else _integer(obj["own_grace"], f"{label}.own_grace", 0),
        receiver=_receiver_names(obj, label, detector_law),
    )


def _receiver_names(obj: dict[str, object], label: str, detector_law: bool) -> tuple[str, ...] | None:
    """The lamp's `receiver`, its records' ladder by name: a set's name or a
    list of distinct names; None without the key. Refused outside the local
    detector law (the ladder is that law's form)."""
    if "receiver" not in obj:
        return None
    if not detector_law:
        raise ValueError(
            f"{label}.receiver is admitted (the "
            "record's ladder by name is the local detector law's form)"
        )
    value = obj["receiver"]
    names = [value] if isinstance(value, str) else value
    if (
        not isinstance(names, list)
        or not names
        or any(not isinstance(name, str) or not name for name in names)
    ):
        raise ValueError(
            f"{label}.receiver must be a detector set's name or a nonempty list of "
            "names (the lamp record's ladder, SIZING.md)"
        )
    if len(set(names)) != len(names):
        raise ValueError(f"{label}.receiver names a set twice")
    return tuple(names)


def _branches(
    value: object, label: str, arms: int
) -> tuple[tuple[tuple[int, int], ...], tuple[int, int] | None]:
    """The joint labels of a giving: [[label, weight], ...], the labels
    distinct integers below 2^arms (the bit k of a label is its value on
    arm k), the weights integers from 1; since `hand-v1` each may carry a
    third entry, the hand of the label (-1 or +1), every branch or none:
    the hand is what a label bit means, the bit k of a label the hand of
    the row on arm k, so the branches must give each value of a bit one
    hand and the two values opposite hands (the hand of the other value
    follows when only one is named). Returns the branches and the hands of
    the bit values 0 and 1, or None where none is named."""
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a list of [label, weight] pairs")
    found: list[tuple[int, int]] = []
    hands: list[int | None] = []
    for index, item in enumerate(value):
        if not isinstance(item, list) or len(item) not in (2, 3):
            raise ValueError(
                f"{label}[{index}] must be a [label, weight] pair, or [label, weight, hand]"
            )
        joint = _integer(item[0], f"{label}[{index}].label", 0, (1 << arms) - 1)
        weight = _integer(item[1], f"{label}[{index}].weight", 1, AMOUNT_BOUND)
        if any(joint == other for other, _ in found):
            raise ValueError(f"{label} names the label {joint} twice")
        found.append((joint, weight))
        hands.append(_hand(item[2], f"{label}[{index}].hand") if len(item) == 3 else None)
    norm = sum(weight * weight for _, weight in found)
    if norm > MOMENTUM_BOUND:
        raise ValueError(f"{label}: the norm {norm} exceeds the integer bound")
    if all(hand is None for hand in hands):
        return tuple(found), None
    if any(hand is None for hand in hands):
        raise ValueError(f"{label} names a hand on some labels and not on others")
    meaning: list[int | None] = [None, None]
    for (joint, _), hand in zip(found, hands, strict=True):
        assert hand is not None
        for arm in range(arms):
            bit = (joint >> arm) & 1
            if meaning[bit] is None:
                meaning[bit] = hand
            elif meaning[bit] != hand:
                raise ValueError(
                    f"{label} gives the bit value {bit} two hands: a hand is a label "
                    "bit named, one hand per value of the bit"
                )
    if meaning[0] is not None and meaning[1] is not None and meaning[0] == meaning[1]:
        raise ValueError(
            f"{label} gives both values of a label bit the hand {meaning[0]:+d}: the two "
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
        raise ValueError(f"{label}.turn is refused on pass, which reads nothing")
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
        raise ValueError(f"{label} must be a list of [family, amount, content per unit] products")
    names = {family.name: index for index, family in enumerate(families)}
    found: list[tuple[int, int, int]] = []
    for k, item in enumerate(value):
        entry_label = f"{label}[{k}]"
        if not isinstance(item, list) or len(item) != 3:
            raise ValueError(f"{entry_label} must be [family, amount, content per unit]")
        name, amount_value, content_value = item
        if not isinstance(name, str) or name not in names:
            raise ValueError(f"{entry_label} names an unknown family {name!r}")
        family = names[name]
        amount = _integer(amount_value, f"{entry_label} amount", 1)
        if families[family].free:
            if type(content_value) is not int or content_value != 0:
                raise ValueError(
                    f"{entry_label}: a free family's product carries no content (0; {name!r} is free)"
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
        raise ValueError(f"{label}.into names an unknown family {into_name!r}")
    into = names[into_name]
    if into == family:
        raise ValueError(
            f"{label}.into names the event's own family {into_name!r}: a "
            "transformation is a change of family"
        )
    products = _products(obj["products"], f"{label}.products", families, table, directions)
    at = crowd = None
    if clock:
        if "at" not in obj:
            raise ValueError(
                f"{label} lacks keys: at (the clock trigger fires at the self-creation "
                "whose clock reaches `at`)"
            )
        at = _integer(obj["at"], f"{label}.at", 1)
        if "crowd" in obj:
            crowd = _integer(obj["crowd"], f"{label}.crowd", 0)
    needed = sum(a * c for _, a, c in products)
    if needed > amount:
        raise ValueError(
            f"{label}: the products' content {needed} exceeds the event's amount "
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
            f"{label}: the transformation's charges do not balance: {into_name!r} on "
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
        raise ValueError(f"{label}.rotate belongs to a `rerelease` entry, not to {rule}")
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
        raise ValueError(f"{label}.gate belongs to a `rerelease` entry, not to {rule}")
    obj = _object(value["gate"], f"{label}.gate", {"kind", "hold", "parties", "control"}, {"kind"})
    kind = obj["kind"]
    if kind not in GATE_KINDS:
        raise ValueError(f"{label}.gate.kind must be one of {list(GATE_KINDS)}")
    hold = obj.get("hold", True)
    if type(hold) is not bool:
        raise ValueError(f"{label}.gate.hold must be true or false")
    parties = _integer(obj.get("parties", 2), f"{label}.gate.parties", 1, LABEL_BITS_BOUND)
    control: int | None = None
    if "control" in obj:
        if parties == 1:
            raise ValueError(f"{label}.gate.control: a gate of one party has no control")
        control = _direction(obj["control"], f"{label}.gate.control", table)
    elif parties > 1:
        raise ValueError(
            f"{label}.gate of {parties} parties declares its control: `control`, the "
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
        raise ValueError(f"{label} must list one row per declared input ({count})")
    found = []
    for k, row in enumerate(listed):
        if not isinstance(row, list) or len(row) != ways:
            raise ValueError(
                f"{label} must list one integer per declared direction ({ways})"
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
            f"{label} declares {named} on the rule {rule!r}: the split is a "
            "`rerelease` with weights (one rule)"
        )
    if free:
        raise ValueError(
            f"{label} declares {named} on a free family's entry: free families never branch"
        )
    inputs: tuple[int, ...] | None = None
    if "inputs" in value:
        inputs = _directions(value["inputs"], f"{label}.inputs", table)
    rows = None if inputs is None else len(inputs)
    if "weights" in value:
        weights = _split_rows(value["weights"], f"{label}.weights", ways, rows, 0, AMOUNT_BOUND)
        for row in weights:
            if not any(row):
                raise ValueError(f"{label}.weights must have at least one positive weight per row")
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
        raise ValueError(f"{label}.reads must name a family")
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
                f"{label} declares {', '.join(clock_only)}: a key of the clock trigger "
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
        raise ValueError(f"{label} must be one of {TABLES}")
    if window is not None and rule == "pass":
        raise ValueError(
            f"{label}.phase_window is refused on pass: a window is a width of a "
            "response, and pass responds to nothing"
        )
    if window is not None and not phased:
        raise ValueError(
            f"{label}.phase_window is refused for a family without a phase circle: "
            "its rays carry no phase to read"
        )
    width = _width(obj, label, phase_steps, phased, str(rule))
    transformation = None
    if rule == "become":
        missing = TRANSFORM_KEYS - set(obj)
        if missing:
            raise ValueError(
                f"{label} lacks keys: {', '.join(sorted(missing))} (a `become` entry "
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
            f"{label} declares into or products on the rule {rule!r}: they belong to a `become` entry"
        )
    if reads is None:
        reads = default_reads(str(rule))
    if reads not in READS:
        raise ValueError(f"{label}.reads must be one of {READS}")
    hand = NO_HAND
    if "hand" in obj:
        if rule == "pass":
            raise ValueError(
                f"{label}.hand is refused on pass: a hand filter admits arrivals of one "
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
                f"{label} is refused without the world key atom_level (atom-level-v1, off by default)"
            )
        obj = _object(entry["level"], label, {"family", "pair", "return"}, {"family", "pair", "return"})
        family_name = obj["family"]
        if not isinstance(family_name, str) or family_name not in names:
            raise ValueError(f"{label}.family names an unknown family")
        family = names[family_name]
        if families[family].free:
            raise ValueError(
                f"{label}.family names the free family {family_name!r}: a released "
                "row carries content h_q x (the rise of the level), so the family is paid"
            )
        if not families[family].phase:
            raise ValueError(
                f"{label}.family names the family {family_name!r} without a phase "
                "circle: a released row turns its phase by its content over the quantum"
            )
        pair_value = obj["pair"]
        if not isinstance(pair_value, list) or len(pair_value) != 2:
            raise ValueError(f"{label}.pair must be two positive integers [n_l, d_l]")
        pair = (
            _integer(pair_value[0], f"{label}.pair[0]", 1),
            _integer(pair_value[1], f"{label}.pair[1]", 1),
        )
        return_value = obj["return"]
        if not isinstance(return_value, list) or len(return_value) != 2:
            raise ValueError(f"{label}.return must be [axis, sign]")
        axis = _integer(return_value[0], f"{label}.return[0]", 0, 2)
        sign = _integer(return_value[1], f"{label}.return[1]", -1, 1)
        if sign == 0:
            raise ValueError(f"{label}.return[1] must be -1 or +1, the sign crossed to")
        if definition.fixed or not definition.phase_by_momentum:
            raise ValueError(
                f"{label} needs a body that steps and turns its phase by its momentum "
                "(phase_by_momentum, not fixed): the level is read off its action rows"
            )
        assert action is not None
        if 2 * action * pair[1] > MOMENTUM_BOUND // max(ticks, 1):
            raise ValueError(
                f"{label}: the level's divisor 2 h d_l x (the count) leaves the "
                f"integer bound {MOMENTUM_BOUND} within the run's ticks"
            )
        found[index] = replace(definition, level=LevelDeclaration(family, pair, axis, sign))
    return tuple(found)


def _block(
    obj: dict[str, object],
    label: str,
    family: FamilyDefinition,
    families: tuple[FamilyDefinition, ...],
    names: dict[str, int],
    held: list[int],
    momentum: tuple[int, ...],
    amount: int,
    momentum_unit: int,
    massive_record: bool,
    lamp_declared: bool,
    span: tuple[int, int, int],
    shape: Address3,
    amplitude_bound: int = AMPLITUDE_BOUND,
    phase_steps: int = 64,
    periodic: tuple[bool, bool, bool] = (True, True, True),
    detector_law: bool = False,
) -> BlockDefinition | None:
    """The block's keys on a measured event (`massive-record-v1`), each named
    in its refusal: `side` makes a block; every other block key without
    `side` is refused; a block needs the world key `massive_record`, no lamp
    and no span; its `pair` is a well on the massive kind (num' / den' >
    num / den) or a gap on light's kind (den' > num', the (M) wall, which
    declares no clock, seed or margin); an emitter's
    giving Node carries a rich pair (at least 500 remainder values, ALGEBRA.md
    9.22 (4)); the momentum is bounded by the pace, 3 (P . P) < (3 Q M)^2 (the wall W
    = 3 Q M of ALGEBRA.md 9.96 (1), Q the universe's `momentum_unit`)."""
    declared = [key for key in BLOCK_KEYS if key in obj]
    if "side" not in obj and "extents" not in obj:
        if declared:
            raise ValueError(
                f"{label}.{declared[0]} belongs to a block (a measured event that "
                "declares `side` or `extents`, massive-record-v1)"
            )
        return None
    if "side" in obj and "extents" in obj:
        raise ValueError(
            f"{label} declares both `side` and `extents`: a cube is `side`, a box is "
            "`extents` [x, y, z] (the bodies with extents per axis; BUILD.md section 26 item 23)"
        )
    if not massive_record:
        raise ValueError(
            f"{label}.side is refused without the world key `massive_record` "
            f"(the world key `massive_record`, absent by default)"
        )
    if lamp_declared:
        raise ValueError(f"{label}: a block declares no lamp (its record is its own)")
    if span != ONE_NODE:
        raise ValueError(f"{label}: a block declares `side`, never `span`")
    if "side" in obj:
        side = _integer(obj["side"], f"{label}.side", 1)
        extents = (side, side, side)
    else:
        value = obj["extents"]
        if not isinstance(value, list) or len(value) != 3:
            raise ValueError(
                f"{label}.extents must be [x, y, z], the box's extents per axis, "
                "each from 1 (the bodies with extents per axis; BUILD.md section 26 item 23)"
            )
        extents = (
            _integer(value[0], f"{label}.extents[0]", 1),
            _integer(value[1], f"{label}.extents[1]", 1),
            _integer(value[2], f"{label}.extents[2]", 1),
        )
        side = extents[0]
    if "pair" not in obj:
        raise ValueError(f"{label} lacks keys: pair (the block's pair at its Nodes)")
    value = obj["pair"]
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{label}.pair must be [num, den], the pair at the Nodes")
    pair = (
        _integer(value[0], f"{label}.pair numerator", 1, MAX_VALUE),
        _integer(value[1], f"{label}.pair denominator", 1, MAX_VALUE),
    )
    # THE BODY'S KIND (ALGEBRA.md 9.85 (3), 9.91 (7)): the family's pair, or the
    # body's own `kind` [num, den] on a family whose pair is the body's,
    # required there and refused elsewhere (one copy)
    if family.pair_on_body:
        if "kind" not in obj:
            raise ValueError(
                f"{label}.kind is required: the family {family.name!r} declares no pair, "
                "so every body of it declares its own rest pair [num, den] (ALGEBRA.md 9.85 (3), "
                "9.91 (7))"
            )
        kind_value = obj["kind"]
        if not isinstance(kind_value, list) or len(kind_value) != 2:
            raise ValueError(f"{label}.kind must be [num, den], the body's rest pair")
        kind = (
            _integer(kind_value[0], f"{label}.kind numerator", 1, MAX_VALUE),
            _integer(kind_value[1], f"{label}.kind denominator", 1, MAX_VALUE),
        )
        if kind[1] <= kind[0]:
            raise ValueError(
                f"{label}.kind [{kind[0]}, {kind[1]}] is no massive kind: den > num, "
                "the gap cos omega_0 = num / den (ALGEBRA.md 9.22)"
            )
    elif "kind" in obj:
        raise ValueError(
            f"{label}.kind is refused: the family {family.name!r} declares its pair "
            f"{list(family.pair)}; one copy (ALGEBRA.md 9.85 (3))"
        )
    else:
        kind = family.pair
    if family.massive_kind:
        # A well lowers the pair; a BARRIER raises it (num' / den' below the
        # kind's: the matter wall of DECLARATIONS.md section 15 M1-6, the
        # mirror line of the matter kind), a block with no bound mode, no
        # seed and no clock; the kind's own pair is no body (the cavity of
        # form (I), a record held by mirror faces of its own, is refused by
        # name: BUILD.md section 26 item 28).
        if pair[0] * kind[1] == pair[1] * kind[0]:
            raise ValueError(
                f"{label}.pair [{pair[0]}, {pair[1]}] is the kind's own pair "
                f"[{kind[0]}, {kind[1]}]: a block lowers the pair at its Nodes (a well) or "
                "raises it (a barrier; MASSIVE_RECORD.md section 4, section 15 M1-6)"
            )
        if pair[0] * kind[1] < pair[1] * kind[0]:
            clock_keys = [key for key in ("seed", "margin") if key in obj]
            if clock_keys:
                raise ValueError(
                    f"{label}.{clock_keys[0]} is refused on a barrier (a raised pair "
                    f"[{pair[0]}, {pair[1]}] on the kind [{kind[0]}, {kind[1]}] has no bound mode "
                    "and no clock; DECLARATIONS.md section 15 M1-6)"
                )
            obj = dict(obj, seed=0)
    else:
        if pair[1] <= pair[0]:
            raise ValueError(
                f"{label}.pair [{pair[0]}, {pair[1]}] on light's kind is no gap: the "
                "(M) wall declares den > num (a lump in the massless surround, "
                "MASSIVE_RECORD.md section 4)"
            )
        clock_keys = [key for key in ("seed", "margin") if key in obj]
        if clock_keys:
            raise ValueError(
                f"{label}.{clock_keys[0]} is refused on a block of light's kind (the "
                "(M) wall has no clock)"
            )
        # the mirror line of light's kind (DECLARATIONS.md section 15 L-1):
        # its Nodes carry the gap's pair and nothing else, no own record
        obj = dict(obj, seed=0)
    # the load bound of MUST 3 on the block's own pair at its Nodes (the
    # coupling's folded denominator HISTORY, decision (2) of record 1962)
    _pair_bound(pair[0], pair[1], label, amplitude_bound)
    if "seed" not in obj:
        # NO IMPLICIT SEED (the model owner's rule through the Boss,
        # 2026-09-25; BUILD.md section 26 item 28): a well declares its own
        # record's amplitude or its profile; the loader's 2^20 is HISTORY
        raise ValueError(
            f"{label} lacks keys: seed (a well's own record on its Nodes: its "
            "amplitude at interval 0, 0 silent, or its profile with `margin`; no default, "
            "BUILD.md section 26 item 28)"
        )
    seed: int
    profile: tuple[int, ...] | None = None
    if isinstance(obj["seed"], list):
        # The bound mode's integer profile over the whole board (MASSIVE_RECORD.md
        # section 11 item 7: the pin worlds' seed, the generator's integers, the
        # same at both levels; admitted with `margin` declared): a flat list of
        # integers in x-major order, one per Node.
        if "margin" not in obj:
            raise ValueError(f"{label}.seed as a profile is admitted only with margin declared")
        values = obj["seed"]
        count = int(shape[0]) * int(shape[1]) * int(shape[2])
        if len(values) != count or any(type(value) is not int for value in values):
            raise ValueError(
                f"{label}.seed as a profile must be {count} integers, one per Node of the "
                "board in x-major order"
            )
        profile = tuple(int(value) for value in values)
        if not any(profile):
            raise ValueError(f"{label}.seed as a profile must not be all zero")
        seed = max(abs(value) for value in profile)
    else:
        seed = _integer(obj["seed"], f"{label}.seed", 0)
    # THE MODE'S CLOCK (ALGEBRA.md 9.22 (7); record 1886): a profile carries
    # its mode's 2 cos omega as the rational [a, b] the generator wrote, b at
    # least the amplitude; the world's integer check of the profile against
    # the eigen-equation reads it (`_initial_state_checks`)
    clock: tuple[int, int] | None = None
    if "clock" in obj:
        if profile is None:
            raise ValueError(
                f"{label}.clock is admitted only beside a profile (the mode's 2 cos "
                "omega belongs to the mode's integers, ALGEBRA.md 9.22 (7))"
            )
        value = obj["clock"]
        if (
            not isinstance(value, list)
            or len(value) != 2
            or any(type(item) is not int for item in value)
            or value[0] < 1
            or value[1] < 1
        ):
            raise ValueError(
                f"{label}.clock must be [a, b], two positive integers, the mode's 2 cos "
                "omega as a rational (ALGEBRA.md 9.22 (7))"
            )
        if value[1] < seed:
            raise ValueError(
                f"{label}.clock [{value[0]}, {value[1]}]: b must be at least the "
                f"profile's amplitude {seed} (the rounding of 2 cos omega to 1 / b at most, "
                "ALGEBRA.md 9.22 (7))"
            )
        clock = (int(value[0]), int(value[1]))
    elif profile is not None:
        raise ValueError(
            f"{label}.seed as a profile needs the mode's `clock` [a, b] beside it (the "
            "generator's rational for 2 cos omega, b at least the amplitude; the loader checks "
            "the profile against the eigen-equation in integers, ALGEBRA.md 9.22 (7), record 1886)"
        )
    # THE PROPER PAIR OF A MOVING BODY ON ONE NODE (ALGEBRA.md 9.63 (3); BUILD.md section 26
    # item 46): beside `clock`, on a block whose momentum lies on one axis, the
    # |P| + 1 pairs [num, den] indexed by the momentum's whole part, the first
    # the clock itself (the rest pair at K = 0)
    proper_clock: tuple[tuple[int, int], ...] | None = None
    if "proper_clock" in obj:
        moving_axes = [axis for axis in range(3) if int(momentum[axis]) != 0]
        if clock is None or len(moving_axes) != 1:
            raise ValueError(
                f"{label}.proper_clock is admitted beside `clock` on a block whose "
                "momentum lies on one axis (the moving body's Node's pairs by the momentum's whole part, "
                "ALGEBRA.md 9.63 (3))"
            )
        value = obj["proper_clock"]
        count = abs(int(momentum[moving_axes[0]])) + 1
        if (
            not isinstance(value, list)
            or len(value) != count
            or any(
                not isinstance(item, list)
                or len(item) != 2
                or any(type(part) is not int for part in item)
                or item[0] < 1
                or item[1] < seed
                for item in value
            )
        ):
            raise ValueError(
                f"{label}.proper_clock must be {count} pairs [num, den] of positive "
                f"integers, den at least the profile's amplitude {seed}, one for every whole part "
                f"of the momentum from 0 to {count - 1} (ALGEBRA.md 9.63 (3))"
            )
        if (int(value[0][0]), int(value[0][1])) != clock:
            raise ValueError(
                f"{label}.proper_clock[0] {value[0]} is not the clock {list(clock)}: at "
                "rest the body's Node rotates at the mode's own pair (ALGEBRA.md 9.63 (3))"
            )
        proper_clock = tuple((int(item[0]), int(item[1])) for item in value)
    if seed > amplitude_bound:
        raise ValueError(
            f"{label}.seed {seed} (the scalar seed, or a profile's largest magnitude) "
            f"is above the world's amplitude bound A = {amplitude_bound} on the pair "
            f"[{pair[0]}, {pair[1]}]: every admitted amplitude enters the one declared bound "
            "(issue #1085; MUST 3)"
        )
    ramp = 0 if "ramp" not in obj else _integer(obj["ramp"], f"{label}.ramp", 0)
    start = 0 if "start" not in obj else _integer(obj["start"], f"{label}.start", 0)
    # THE BODY'S NUMBERS (ALGEBRA.md 9.91 (3), (7); commit 2): charge, spin and moment,
    # required under the law (no default), integers on the axes (record 2084)
    if detector_law:
        _require_under_law(obj, label, {"q", "spin", "moment", "twist"})
    charge = 0 if "q" not in obj else _integer(obj["q"], f"{label}.q", -AMOUNT_BOUND, AMOUNT_BOUND)
    spin = _axes_vector(obj.get("spin", [0, 0, 0]), f"{label}.spin")
    moment = _axes_vector(obj.get("moment", [0, 0, 0]), f"{label}.moment")
    if detector_law and "margin" not in obj and pair[0] * kind[1] > pair[1] * kind[0]:
        # NO DEFAULT UNDER THE DETECTOR LAW (record 2089; item 57): a well's
        # margin kind, pin or control, declared (record 2037, per measured
        # event); a barrier or a gap declares none (refused above)
        raise ValueError(
            f"{label}.margin is required on a well: one of "
            f"{list(MARGIN_KINDS)}, no default (the model owner's records 2037 and 2089)"
        )
    margin = obj.get("margin", MARGIN_KINDS[0])
    if margin not in MARGIN_KINDS:
        raise ValueError(f"{label}.margin must be one of {list(MARGIN_KINDS)}")
    # THE WALL W = 3 Q M (ALGEBRA.md 9.96 (1), 9.89 (2)): one wall per body, on its
    # whole content at the load, its own quanta and what it holds (the stock is
    # content, 9.51 (8)); the width S = 1 is gone
    wall = 3 * momentum_unit * sum(held)
    if 3 * sum(component * component for component in momentum) >= wall * wall:
        raise ValueError(
            f"{label}.momentum {list(momentum)}: the pace bound 3 (P . P) < (3 Q M)^2 "
            f"= {wall * wall} fails (the body's velocity v = P / (3 Q M) below c, ALGEBRA.md "
            "9.96 (1); DESIGN.md 5.1 (a))"
        )
    receiver: str | None = None
    if "receiver" in obj:
        if "emitter" not in obj:
            raise ValueError(
                f"{label}.receiver is refused on a block that emits nothing (the "
                "receiver by name is the ladder of the block's emitted records, DECLARATIONS.md "
                "section 13 item 7)"
            )
        value = obj["receiver"]
        if not isinstance(value, str) or not value:
            raise ValueError(
                f"{label}.receiver must be the name of a declared detector set (a nonempty string)"
            )
        receiver = value
    emitter: EmitterDefinition | None = None
    stock = 0
    if "emitter" in obj:
        # the emitter as a clicking body (ALGEBRA.md 9.17 (4)): a body of a
        # massive kind with its seed (the excited record) and its stock
        if not family.massive_kind:
            raise ValueError(
                f"{label}.emitter is refused on a body of light's kind: the emitter "
                "is a body of a massive kind whose excited record (its seed, the bound mode) "
                "clicks at its own rung (ALGEBRA.md 9.17 (4))"
            )
        if seed <= 0:
            raise ValueError(
                f"{label}.emitter needs the body's `seed` (its excited record is the "
                "seed at both levels; a silent body excites nothing)"
            )
        if amount < 1:
            raise ValueError(
                f"{label}.emitter needs `amount` from 1, the body's own quanta (its "
                "stock is the given family's content under `held`, ALGEBRA.md 9.51 (8))"
            )
        # THE RESIDUES OF AN EMITTING BODY spread from the remainder kept at
        # its Nodes (the model owner's decisions (1) and (2) of record 1962;
        # ALGEBRA.md 9.34 (A) and (B)): the coupling of 9.19 (4e) is HISTORY
        emitter = _emitter(
            obj["emitter"],
            f"{label}.emitter",
            family,
            families,
            names,
            shape,
            phase_steps,
            extents=extents,
            periodic=periodic,
            momentum=momentum,
            moment=moment,
            clock_pair=clock,
        )
        # THE STOCK IS GIVEN-FAMILY CONTENT (ALGEBRA.md 9.51 (8); BUILD.md
        # section 26 item 47): the quanta a body gives are the given family's,
        # held at the body under `held`; a giving lowers them and leaves the
        # body's own quanta and its charge (a body spending its own quantum
        # per giving would lose charge by giving light: refused)
        # A BODY GIVING ITS OWN FAMILY (ALGEBRA.md 9.96 (5); commit 6): its stock is `stock`, a
        # count of its own quanta set aside for giving, from 1 to `amount`; each giving lowers
        # M by one; `stock` is refused where the given family is another (its stock is `held`)
        if emitter.family == names[family.name]:
            if "stock" not in obj:
                raise ValueError(
                    f"{label}.stock is required: the emitter gives the body's own family "
                    f"{family.name!r}, so the body declares the count of its own quanta set aside for "
                    "giving, from 1 to `amount` (ALGEBRA.md 9.96 (5))"
                )
            stock = _integer(obj["stock"], f"{label}.stock", 1, amount)
        elif "stock" in obj:
            raise ValueError(
                f"{label}.stock is refused: the emitter gives {families[emitter.family].name!r}, "
                "another family, whose stock is the body's `held` quanta of it (ALGEBRA.md 9.51 (8), "
                "9.96 (5))"
            )
        elif held[emitter.family] < 1:
            raise ValueError(
                f"{label}.emitter needs its stock as the given family's content held "
                f"at the body: `held` naming {families[emitter.family].name!r} from 1 (a world that "
                "needs W givings holds W; ALGEBRA.md 9.51 (8): a giving lowers the given family's "
                "content, the body's own quanta `amount` and its charge stay)"
            )
        # THE RICHNESS OF THE GIVING NODE (ALGEBRA.md 9.22 (4); BUILD.md section
        # 26 item 15): the residue from the law takes 3 den / gcd(num, 3 den)
        # values on the pair at the body's centre Node (its own pair), at
        # least 500 of them ([801, 700] gives 700, [800, 801] 2403; [8, 7]
        # 21 and [800, 800] 3 are refused)
        residues = 3 * pair[1] // math.gcd(pair[0], 3 * pair[1])
        if residues < 500:
            raise ValueError(
                f"{label}.emitter: the body's pair [{pair[0]}, {pair[1]}] gives "
                f"{residues} remainder values at the giving Node (3 den / gcd(num, 3 den)), below "
                "500: the residue from the law needs a rich pair (ALGEBRA.md 9.22 (4); [801, 700] "
                "on the kind [7, 8] gives 700, [800, 801] on [800, 809] gives 2403)"
            )
        if receiver is not None and emitter.receiver is not None:
            raise ValueError(
                f"{label}: one ladder for the given records: the block's `receiver` "
                "(one name, the line at the rung) or the emitter's `receiver` (a list, the "
                "ladder by name), not both"
            )
    return BlockDefinition(
        side,
        pair,
        kind,
        seed,
        extents=extents,
        profile=profile,
        clock=clock,
        proper_clock=proper_clock,
        ramp=ramp,
        start=start,
        q=charge,
        spin=spin,
        moment=moment,
        # THE BODY'S OWN RECORD'S TWIST "OWN" (ALGEBRA.md 9.96 (2) (a); item 73): the
        # generator's integer round(2^16 omega_0) declared under `twist` (its mode's
        # rotation, or its kind's rest rotation on a body without a mode), no default
        twist=_integer(obj["twist"], f"{label}.twist", 0),
        margin=str(margin),
        receiver=receiver,
        emitter=emitter,
        stock=stock,
    )


def _axes_vector(value: object, label: str) -> tuple[int, int, int]:
    """An integer vector on the axes (record 2084: every directed thing an integer
    vector on the axes), three integers."""
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{label} must be three integers, a vector on the axes")
    return (
        _integer(value[0], f"{label}[0]", -AMOUNT_BOUND, AMOUNT_BOUND),
        _integer(value[1], f"{label}[1]", -AMOUNT_BOUND, AMOUNT_BOUND),
        _integer(value[2], f"{label}[2]", -AMOUNT_BOUND, AMOUNT_BOUND),
    )


def _emitter(
    value: object,
    label: str,
    family: FamilyDefinition,
    families: Sequence[FamilyDefinition],
    names: dict[str, int],
    shape: Address3,
    phase_steps: int,
    extents: tuple[int, int, int] = (1, 1, 1),
    periodic: tuple[bool, bool, bool] = (True, True, True),
    momentum: tuple[int, ...] = (0, 0, 0),
    moment: tuple[int, int, int] = (0, 0, 0),
    clock_pair: tuple[int, int] | None = None,
) -> EmitterDefinition:
    """The `emitter` object of a clicking body (ALGEBRA.md 9.17 (4) to (6),
    9.22 (4)): the given family a paid family with the pair form of its
    clock (not the body's own), the given labels, the ladder by name, the
    period and the norm (the generator's integers), the given profile
    (material). No wheel, no residue order and no seed: the residue is the
    law's (the clicking record's remainder at the giving Node, the wheel the
    pair's), and the keys are refused by name."""
    _refuse_retired(value, label, ("wheel", "residue_order", "residue_seed", "train", "given"))
    obj = _object(
        value,
        label,
        {
            "family",
            "branches",
            "receiver",
            "period",
            "norm",
            "train",
            "given",
            "weight",
            "norm_denominator",
            "window_read",
            "clock",
            "pair",
            "twist",
        },
        {"family"},
    )
    name = obj["family"]
    if not isinstance(name, str) or name not in names:
        raise ValueError(f"{label}.family names an unknown family")
    given_family = families[names[name]]
    # a body may give its own family (ALGEBRA.md 9.96 (5); commit 6): the given record
    # carries the emitter's declared pair, the stock is the body's `stock` of its own quanta
    if given_family.free:
        raise ValueError(
            f"{label}.family {name!r}: the given family is a paid family (light's kind, "
            "or a massive kind)"
        )
    # THE GIVEN RECORD'S PAIR (ALGEBRA.md 9.85 (3), 9.91 (7)): the emitter's
    # `pair` [num, den], required when the given family's pair is the body's
    # and refused when the family declares one (one copy)
    given_pair: tuple[int, int]
    if given_family.pair_on_body:
        if "pair" not in obj:
            raise ValueError(
                f"{label}.pair is required: the given family {name!r} declares no pair, "
                "so the emitter declares the given record's pair [num, den] (ALGEBRA.md 9.85 (3), "
                "9.91 (7))"
            )
        given_pair = _ratio(obj["pair"], f"{label}.pair", zero=False)
        if given_pair[1] <= given_pair[0]:
            raise ValueError(
                f"{label}.pair [{given_pair[0]}, {given_pair[1]}] is no massive kind: den "
                "> num (ALGEBRA.md 9.22)"
            )
    elif "pair" in obj:
        raise ValueError(
            f"{label}.pair is refused: the given family {name!r} declares its pair "
            f"{list(given_family.pair)}; one copy (ALGEBRA.md 9.85 (3))"
        )
    else:
        given_pair = given_family.pair
    if given_family.held is not None and given_family.clicks is None:
        raise ValueError(
            f"{label} givings into the held family {name!r}: it takes and gives "
            "nothing (ALGEBRA.md 9.45 (1))"
        )
    # THE GIVEN CLOCK (ALGEBRA.md 9.85 (3); item 59): a light record's clock is its
    # emitter's, `clock` [p, q] on the emitter, REQUIRED when the given family
    # declares none (the families file's light) and refused when it does (one copy)
    if "clock" in obj:
        if given_family.phase_per_age is not None:
            raise ValueError(
                f"{label}.clock is refused: the given family {name!r} declares its own "
                "clock (phase_per_link); one copy (ALGEBRA.md 9.85 (3))"
            )
        clock = _ratio(obj["clock"], f"{label}.clock", zero=False)
    elif given_family.phase_per_age is not None:
        clock = (int(given_family.phase_per_age[0]), int(given_family.phase_per_age[1]))
    else:
        raise ValueError(
            f"{label}.clock is required: the given family {name!r} declares no clock, so "
            "the emitter declares the given record's clock [p, q] (ALGEBRA.md 9.85 (3); BUILD.md "
            "section 26 item 59)"
        )
    step = clock[0] // clock[1]
    if step % 2 == 1 and 2 * phase_steps > MAX_PHASE_STEPS:
        raise ValueError(
            f"{label}.family {name!r}: the given clock's step floor(n / d) = {step} is "
            f"odd and the write's circle of 2 N = {2 * phase_steps} steps exceeds the tables' bound "
            f"{MAX_PHASE_STEPS} (ALGEBRA.md 9.17 (6)); declare an even step or a smaller N"
        )
    branches: tuple[tuple[int, int], ...] = ((0, 1),)
    label_hands: tuple[int, int] | None = None
    if "branches" in obj:
        branches, label_hands = _branches(obj["branches"], f"{label}.branches", 1)
    receiver = _receiver_names(obj, label, True)
    period = None if "period" not in obj else _integer(obj["period"], f"{label}.period", 1)
    # THE POINT EMITTER'S WEIGHT (ALGEBRA.md 9.71 (1); item 50): an integer from
    # 1; the world's `point_emitter` key pairs it with the absence of a train
    weight = None if "weight" not in obj else _integer(obj["weight"], f"{label}.weight", 1)
    norm_denominator = (
        None
        if "norm_denominator" not in obj
        else _integer(obj["norm_denominator"], f"{label}.norm_denominator", 1)
    )
    norm = None if "norm" not in obj else _integer(obj["norm"], f"{label}.norm", 1, NORM_BOUND)
    # CANCELLED (commit 7): the given train's keys are refused by name above; the
    # parse of `train` and `given` below is disconnected, kept as the record
    train: TrainDefinition | None = None
    if "train" in obj:
        train = _train(
            obj["train"], f"{label}.train", given_family, phase_steps, extents, momentum, clock
        )
    given: GivenTrain | None = None
    if "given" in obj:
        # THE GIVEN TRAIN (ALGEBRA.md 9.17 (6a)): the profile of the train's
        # two levels over the body's Nodes and its norm on the vacuum, the
        # generator's integers, checked here in integers; the two-integer pair
        # (the one-Node giving, a flat pulse of the body's length) refused
        value = obj["given"]
        if isinstance(value, list):
            raise ValueError(
                f"{label}.given is the pair [now, before] on every Node: a flat pulse of "
                "the body's length is broadband and its standing components book the ladder by "
                "sloshing, not by a passage (ALGEBRA.md 9.17 (6a), 9.25 (11)); every giving is a "
                'travelling train: `given` {"now": [...], "before": [...], "norm": T} with `train`'
            )
        if train is None:
            raise ValueError(
                f"{label}.given needs the emitter's `train` (the direction and the "
                "periods; ALGEBRA.md 9.17 (6a))"
            )
        wrap = periodic
        given = _given_train(value, f"{label}.given", given_pair, shape, extents, wrap, train)
    # THE GIVEN RECORD'S COMPONENT (ALGEBRA.md 9.82 (3) (d)): on a vector family the
    # component along the body's moment mu, one axis; a scalar family's one component
    part = 0
    if len(given_family.parts) > 1:
        axes = [axis for axis in range(3) if moment[axis] != 0]
        if len(axes) != 1:
            raise ValueError(
                f"{label}: the given family {name!r} is a vector family and the body's "
                f"moment {list(moment)} lies on {len(axes)} axes: the given record is written into the "
                "component along the body's moment, one axis (ALGEBRA.md 9.82 (3) (d); a body with no "
                "moment gives no direction to write)"
            )
        part = 1 + axes[0]
    # THE GIVEN RECORD'S TWIST "OWN" (ALGEBRA.md 9.96 (2) (a); item 73): the generator's
    # integer declared under `twist` (a massive kind's rest rotation from its pair, or
    # the emitting body's own rotation where the window writes it, 9.85 (5)), no default
    _require_under_law(obj, label, {"twist"})
    twist = _integer(obj["twist"], f"{label}.twist", 0)
    return EmitterDefinition(
        names[name],
        branches,
        label_hands,
        receiver,
        clock,
        given_pair,
        period,
        norm,
        train,
        given,
        weight=weight,
        norm_denominator=norm_denominator,
        part=part,
        twist=twist,
    )


def _train(
    value: object,
    label: str,
    given_family: FamilyDefinition,
    phase_steps: int,
    extents: tuple[int, int, int],
    momentum: tuple[int, ...],
    rest_clock: tuple[int, int],
) -> TrainDefinition:
    """The emitter's `train` (ALGEBRA.md 9.17 (6a)): one signed unit axis
    vector and the periods n >= 8; the given clock the given family's
    declared clock [p, q], the wavelength 2 N q / p a whole number of Links
    and the body's extent along the direction n wavelengths. DOPPLER
    (ALGEBRA.md 9.62 (4); BUILD.md section 26 item 49): a moving body's train
    declares its own clock pair `clock`, the wave number boosted by its
    motion in the given family's representation (the generator's); refused
    on a body at rest."""
    obj = _object(value, label, {"direction", "periods", "clock"}, {"direction", "periods"})
    direction = obj["direction"]
    if (
        not isinstance(direction, list)
        or len(direction) != 3
        or any(type(v) is not int for v in direction)
        or sorted(abs(int(v)) for v in direction) != [0, 0, 1]
    ):
        raise ValueError(
            f"{label}.direction must be one signed unit axis vector, the train's way "
            "(ALGEBRA.md 9.17 (6a))"
        )
    axis = next(index for index, v in enumerate(direction) if v != 0)
    sign = 1 if int(direction[axis]) > 0 else -1
    periods = _integer(obj["periods"], f"{label}.periods", 8)
    p, q = rest_clock  # the given clock, the family's or the emitter's (item 59)
    if "clock" in obj:
        # DOPPLER (ALGEBRA.md 9.62 (4); item 49): the moving body's train at its
        # own boosted wave number, declared for the declared momentum
        if all(int(component) == 0 for component in momentum):
            raise ValueError(
                f"{label}.clock is admitted on a moving body alone: at rest the given "
                "rows carry the given family's clock (ALGEBRA.md 9.62 (4), the given rows of a "
                "moving body carry its motion in the given family's representation)"
            )
        pair = obj["clock"]
        if (
            not isinstance(pair, list)
            or len(pair) != 2
            or any(type(item) is not int for item in pair)
            or pair[0] < 1
            or pair[1] < 1
        ):
            raise ValueError(
                f"{label}.clock must be [p, q], two positive integers, the train's "
                "boosted wave number 2 pi p / (2 N q) per Link (ALGEBRA.md 9.62 (4))"
            )
        p, q = int(pair[0]), int(pair[1])
    if (2 * phase_steps * q) % p != 0:
        raise ValueError(
            f"{label}: the given family's clock [{p}, {q}] on N = {phase_steps} gives "
            f"the wavelength 2 N q / p = {2 * phase_steps * q} / {p}, no whole number of Links "
            "(ALGEBRA.md 9.17 (6a))"
        )
    wavelength = (2 * phase_steps * q) // p
    if extents[axis] != periods * wavelength:
        raise ValueError(
            f"{label}: the body's extent {extents[axis]} along the train's axis "
            f"{AXES[axis]} is not the train's length, {periods} periods of the wavelength "
            f"{wavelength} = {periods * wavelength} Nodes (ALGEBRA.md 9.17 (6a))"
        )
    return TrainDefinition(axis, sign, (p, q), periods, wavelength, "clock" in obj)


def _given_train(
    value: object,
    label: str,
    given_pair: tuple[int, int],
    shape: Address3,
    extents: tuple[int, int, int],
    wrap: tuple[bool, bool, bool],
    train: TrainDefinition,
) -> GivenTrain:
    """The emitter's `given` profile (ALGEBRA.md 9.17 (6a)) checked in
    integers: the two levels over the body's Nodes (the box's Node count,
    x-major), a motion, the flux sign along the train's way positive, and
    the norm the conserved form on the given family's vacuum (the box at the
    board's origin: the vacuum is the same wherever the box stands)."""
    obj = _object(value, label, {"now", "before", "norm", "rest_norm"}, {"now", "before", "norm"})
    count = extents[0] * extents[1] * extents[2]
    levels: list[tuple[int, ...]] = []
    for key in ("now", "before"):
        items = obj[key]
        if not isinstance(items, list) or len(items) != count or any(type(v) is not int for v in items):
            raise ValueError(
                f"{label}.{key} must be {count} integers, the train's level on every "
                f"Node of the body's box {list(extents)} in x-major order (ALGEBRA.md 9.17 (6a))"
            )
        levels.append(tuple(int(v) for v in items))
    now, before = levels
    if not any(now) and not any(before):
        raise ValueError(f"{label} writes no motion (every level 0)")
    flux = given_train_flux_sign(now, before, extents, train.axis, train.sign)
    if flux <= 0:
        raise ValueError(
            f"{label}: the flux along the train's way {list(train.direction)} sums to "
            f"{flux}, not positive: the record does not travel as declared (ALGEBRA.md 9.17 (6a))"
        )
    norm = _integer(obj["norm"], f"{label}.norm", 1, NORM_BOUND)
    board = (int(shape[0]), int(shape[1]), int(shape[2]))
    expected = given_train_norm(now, before, board, (0, 0, 0), extents, given_pair, wrap)
    if norm != expected:
        raise ValueError(
            f"{label}.norm {norm} is not the given record's conserved form on the "
            f"vacuum, {expected} (ALGEBRA.md 9.17 (6a), 9.19 (3); the generator's `given_train`)"
        )
    # THE BOOSTED NORM (ALGEBRA.md 9.74 (3); item 56): the rest train's norm,
    # the ladder's threshold, declared with the boosted train alone
    if train.boosted and "rest_norm" not in obj:
        raise ValueError(
            f"{label}.rest_norm is required with the train's own `clock`: the rest "
            "train's norm T_rest, the ladder's threshold under the boosted rows (ALGEBRA.md 9.74 "
            "(3), 9.75 (1); the generator's `given_train`)"
        )
    if not train.boosted and "rest_norm" in obj:
        raise ValueError(
            f"{label}.rest_norm is refused on a train at the given family's clock: the "
            "rest train's norm is `norm` itself (ALGEBRA.md 9.74 (3))"
        )
    rest_norm = (
        _integer(obj["rest_norm"], f"{label}.rest_norm", 1, NORM_BOUND) if train.boosted else norm
    )
    return GivenTrain(now, before, norm, rest_norm)


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
    massive_record: bool = False,
    width: int = 1,
    amplitude_bound: int = AMPLITUDE_BOUND,
    detector_law: bool = False,
    momentum_unit: int = 0,
) -> tuple[MeasuredDefinition, ...]:
    if not isinstance(value, list):
        raise ValueError("measured must be a list")
    names = {family.name: index for index, family in enumerate(families)}
    found: list[MeasuredDefinition] = []
    # Every Node of every body so far: two measured events never share one.
    occupied: set[Address3] = set()
    for index, entry in enumerate(value):
        label = f"measured[{index}]"
        # under the law a body's `charge` is its own number Q (ALGEBRA.md 9.91 (3), (7);
        # commit 2); the ray law's measured charge of 2026-09-20 stays refused without it
        if isinstance(entry, dict) and CHARGE_KEY in entry and not detector_law:
            raise ValueError(
                f"{label} declares {CHARGE_KEY}, a key removed on 2026-09-20: the "
                "charge of a measured event is its family's charge per unit of content times "
                "its content (the family's `charge`, an integer or [n, d]); see docs/MIGRATION.md"
            )
        _refuse_retired(
            entry, label, ("absorbing", "take", "emits", "own_grace", "wheel", "cavity", "coupling")
        )
        obj = _object(entry, label, MEASURED_KEYS, {"position", "family", "amount"})
        if detector_law:
            # NO DEFAULT UNDER THE DETECTOR LAW (record 2089; item 57): the
            # momentum and the held quanta on every measured event, the drive's
            # ramp and start on every block (a `side` or `extents`), the margin
            # kind on every well (`_block`); the ray law's phase, directions,
            # phase_by_momentum, span, books and the lamp's keys never read,
            # refused; `fixed` (an apparatus held in place) is read since the
            # Boss's record 2157 (ALGEBRA.md 9.104 (6) (b)): the feed, when it
            # lands, acts on a body without the word alone
            _require_under_law(obj, label, {"momentum", "stocks"})
            if "side" in obj or "extents" in obj:
                _require_under_law(obj, label, {"ramp", "start"})
            _refuse_under_law(
                obj,
                label,
                {
                    "phase",
                    "directions",
                    "phase_by_momentum",
                    "span",
                    "books",
                    "windows",
                    "splits",
                    "transforms",
                    "become",
                    "rotations",
                    "gates",
                    "contact",
                    "widths",
                    "table",
                },
            )
        position = _address(obj["position"], f"{label}.position", shape)
        if any(item.position == position for item in found):
            raise ValueError(f"two measured events at one Node {list(position)}")
        span = _span(obj.get("span", list(ONE_NODE)), f"{label}.span", shape)
        nodes = body_nodes(position, span, shape, periodic)
        if nodes is None:
            raise ValueError(
                f"{label}: a body of span {list(span)} centred on {list(position)} "
                "leaves the GameBoard through an open face"
            )
        shared = [node for node in nodes if node in occupied]
        if shared:
            raise ValueError(
                f"two measured events share the Node {list(shared[0])} "
                f"({label}, a body of span {list(span)})"
            )
        occupied.update(nodes)
        family_name = obj["family"]
        if not isinstance(family_name, str) or family_name not in names:
            raise ValueError(f"{label}.family names an unknown family")
        family = names[family_name]
        amount = _integer(obj["amount"], f"{label}.amount", 1)
        held = [0] * len(families)
        held[family] = amount
        # THE BODY'S STOCKS of other families' quanta (`stocks`, record 2128 (1); beside
        # 9.96 (5)'s `stock` of its own): the given family's content held at the body
        declared_held = obj.get("stocks", {})
        if not isinstance(declared_held, dict):
            raise ValueError(f"{label}.stocks must map family names to contents")
        for key, content in declared_held.items():
            if key not in names:
                raise ValueError(f"{label}.stocks names an unknown family {key!r}")
            if names[key] == family:
                raise ValueError(
                    f"{label}.stocks names the event's own family {key!r}, whose content is `amount`"
                )
            held[names[key]] = _integer(content, f"{label}.stocks[{key!r}]", 1)
        phased = families[family].phase
        # The turn's static bound: 2 x content x n below d x N at the clock's
        # rate [n, d] (2 x content below K x N for an integer K), the exact
        # refusal of a turn at half the circle staying the frame's.
        if phased and 2 * sum(held) * turn_rate[0] >= turn_rate[1] * phase_steps:
            raise ValueError(
                f"{label}.amount must keep 2 x content below K x N (the phase step "
                "per self-creation below half the circle; the content held of every family counts; "
                "at the clock's rate [n, d], 2 x content x n below d x N)"
            )
        # A measured event of a family without a phase circle has phase 0.
        phase = _integer(obj.get("phase", 0), f"{label}.phase", 0, phase_steps - 1 if phased else 0)
        momentum_value = obj.get("momentum", [0, 0, 0])
        if not isinstance(momentum_value, list) or len(momentum_value) != 3:
            raise ValueError(f"{label}.momentum must be three integers")
        momentum = tuple(_integer(item, f"{label}.momentum", -AMOUNT_BOUND) for item in momentum_value)
        fixed = obj.get("fixed", False)
        if type(fixed) is not bool:
            raise ValueError(f"{label}.fixed must be true or false")
        turning = obj.get("phase_by_momentum", False)
        if type(turning) is not bool:
            raise ValueError(f"{label}.phase_by_momentum must be true or false")
        if turning:
            if action is None:
                raise ValueError(
                    f"{label}.phase_by_momentum needs the world's `action` (the "
                    "quantum h of the turn by momentum), which the world does not declare"
                )
            if fixed:
                raise ValueError(
                    f"{label}.phase_by_momentum is refused on a fixed measured "
                    "event, which never steps a Link"
                )
            if not phased:
                raise ValueError(
                    f"{label}.phase_by_momentum is refused for a family without a "
                    "phase circle: there is no phase to turn"
                )
            # The bound of the turn: a body steps at most one Link per
            # interval, so within the run k <= ticks Links on an axis and
            # the product k x |p| x N of the declared momentum must fit.
            largest = max(abs(component) for component in momentum)
            if ticks * largest * phase_steps > MOMENTUM_BOUND:
                raise ValueError(
                    f"{label}: the turn by momentum forms k x |p| x N up to "
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
            raise ValueError(f"{label}.table must map family names to rules")
        for key, entry_value in declared.items():
            if key not in names:
                raise ValueError(f"{label}.table names an unknown family {key!r}")
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
                        f"{entry_label}.phase_window.reads names an unknown family "
                        f"{entry_window.family!r}"
                    )
                if not families[names[entry_window.family]].phase:
                    raise ValueError(
                        f"{entry_label}.phase_window.reads names the family "
                        f"{entry_window.family!r}, which has no phase circle: its rows carry no "
                        "phase to read a centre from"
                    )
                if entry_window.family == key:
                    raise ValueError(
                        f"{entry_label}.phase_window.reads names the entry's own family "
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
            rule if rule not in (default_rule(family), "become") else CONTACT_DEFAULT
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
                raise ValueError(f"{label}: a lamp is a measured event of a paid family")
            if families[family].charge[0]:
                raise ValueError(
                    f"{label}: a lamp of the charged paid family {family_name!r} is "
                    "refused: its releases would create charge from nothing (a charged paid family "
                    "is given by a transformation or declared in transit; D-1, 2026-09-20)"
                )
            if detector_law:
                # THE LAMP IS RETIRED under the detector law (ALGEBRA.md 9.17,
                # the model owner's word of 2026-09-24, 22:30Z): a giving is the
                # other side of a click that ends a record; a rate with no
                # record behind it and a drive on the Nodes are refused
                raise ValueError(
                    f"{label}.lamp is refused: a giving has a "
                    "clicking record behind it (ALGEBRA.md 9.17); the emitter is a body of a massive "
                    "kind with its seed, its stock and the key `emitter` (BUILD.md section 26)"
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
                detector_law=detector_law,
            )
        block = _block(
            obj,
            label,
            families[family],
            families,
            names,
            held,
            momentum,
            amount,
            momentum_unit,
            massive_record,
            lamp is not None,
            span,
            shape,
            amplitude_bound,
            phase_steps,
            periodic,
            detector_law,
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
                block=block,
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
                f"measured[{declared[0]}].E is refused without the world key "
                "covariant_readings (the energy E' is a reading of covariant-readings-v1)"
            )
        return None
    label = "covariant_readings"
    obj = _object(value, label, COVARIANT_KEYS, {"c2", "grain"})
    if action is not None:
        raise ValueError(
            f"{label} is refused with `action`: the turn by momentum per Link stepped "
            "and the turn per proper time do not compose on one phase until designed "
            "(DERIVATIONS_BEAM 17.6 S4)"
        )
    c2 = _ratio(obj["c2"], f"{label}.c2", zero=False)
    if c2[0] != 1:
        raise ValueError(
            f"{label}.c2 must be the pair [1, d] (c^2 = 1 / d; the design's [1, 3]), "
            f"not {list(c2)}: the exact square is W = E'_0^2 + d p . p with E'_0 = Q S M whole"
        )
    factor = c2[1]
    grain = _integer(obj["grain"], f"{label}.grain", 1)
    if grain & (grain - 1):
        raise ValueError(f"{label}.grain must be a power of two, not {grain}")
    if (LABEL_SCALE * width) % grain:
        raise ValueError(
            f"{label}.grain {grain} must divide Q x S = {LABEL_SCALE * width} so that "
            "E'_0 / g = (Q S / g) x M is whole for every content"
        )
    books = obj.get("books", False)
    if type(books) is not bool:
        raise ValueError(f"{label}.books must be true or false")
    for index, entry in enumerate(measured):
        if entry.fixed:
            # An apparatus held in place carries no readings (its momentum
            # line is the push it took, never a motion): no domain, no `E`.
            if entry.energy is not None:
                raise ValueError(
                    f"measured[{index}].E is refused on a fixed measured event: an "
                    "apparatus held in place carries no readings under covariant_readings"
                )
            continue
        content = sum(entry.held)
        axes = [axis for axis, component in enumerate(entry.momentum) if component]
        if len(axes) > 1 and not drive_b:
            raise ValueError(
                f"measured[{index}]: the momentum {list(entry.momentum)} has components "
                f"on more than one axis; under {label} a body's momentum lies on one axis (the base "
                "is the per-axis drive of BEAM_LAW note 17, `step_axis`, where the pace p / E' holds "
                "on one axis) unless the world declares `drive_b` (form B's directional drive, "
                "drive-b-v1, off by default)"
            )
        manhattan = sum(abs(component) for component in entry.momentum)
        if manhattan > LABEL_SCALE * width * content:
            raise ValueError(
                f"measured[{index}]: |p|_1 = {manhattan} exceeds Q x S x M = "
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
                    f"measured[{index}].E = {entry.energy}: at the grain {grain} "
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
            f"{label}.books declares the exchange's accounting, and the paid family "
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
            f"{label}: (E'_0 / g)^2 = {rest}^2 exceeds the integer bound "
            f"{MOMENTUM_BOUND} at the grain {grain} (a larger grain)"
        )
    square = rest * rest
    for axis, component in enumerate(momentum):
        part = abs(component) // grain
        if part > MOMENTUM_BOUND // max(part, 1) or part * part > MOMENTUM_BOUND // factor:
            raise OverflowError(
                f"{label}: d x (p_{axis} / g)^2 = {factor} x {part}^2 exceeds the "
                f"integer bound {MOMENTUM_BOUND} at the grain {grain} (a larger grain)"
            )
        square += factor * part * part
        if square > MOMENTUM_BOUND:
            raise OverflowError(
                f"{label}: W / g^2 exceeds the integer bound {MOMENTUM_BOUND} at the "
                f"grain {grain} (a larger grain)"
            )
    return square


def _detector_law_load_checks(
    measured: tuple[MeasuredDefinition, ...],
    families: tuple[FamilyDefinition, ...],
    directions: tuple[Vector, ...],
    periodic: tuple[bool, bool, bool],
    phase_steps: int,
) -> None:
    """The instruments of the ray law (cancelled, ALGEBRA.md 9.90 (1))
    are refused, naming the rule: a lamp's `turns` (a fan of directions
    with phases; the lamp inserts at its Nodes by its clock), a measured
    event's fan `table` (an opening is free Nodes); and every paid family
    needs the pair form of `phase_per_link`, its clock."""
    for number, entry in enumerate(measured):
        if entry.lamp is not None and any(entry.lamp.turns):
            raise ValueError(
                f"measured[{number}].lamp.turns is refused "
                "(a lamp inserts at its Nodes by its clock; there is no fan)"
            )
        # A split with `inputs` is the TABLE form's splitter (build 2, component
        # 3: the split's integer matrix on the record's read phase, the outputs
        # re-emitted at the table's output Nodes); a split without inputs is
        # an opening's fan, refused under the rule.
        if any(split is not None and split.inputs is None for split in entry.splits):
            raise ValueError(
                f"measured[{number}] declares a fan (a rerelease split with weights and "
                f"no inputs), refused (an opening is free Nodes; there is "
                "no fan; a splitter declares its inputs)"
            )
        # An arm's half-space is the sign of (node - origin) . vector on the
        # board's raw coordinates: on a periodic axis there is no half-space,
        # so arms whose first direction has a component on a periodic axis
        # are refused (the pair's two arms, component 2).
        if entry.lamp is not None and entry.lamp.arms > 1:
            per_arm = len(entry.lamp.directions) // entry.lamp.arms
            for arm in range(entry.lamp.arms):
                vector = directions[entry.lamp.directions[arm * per_arm]]
                for axis in range(3):
                    if int(vector[axis]) and periodic[axis]:
                        raise ValueError(
                            f"measured[{number}].lamp.arms: the arm {arm}'s first "
                            f"direction {list(int(v) for v in vector)} has a component on the periodic "
                            f"axis {AXES[axis]}, which has no half-space (an arm's row lives on its "
                            "own side of the lamp's Node on an open axis)"
                        )
    # A family of records may declare no clock of its own (ALGEBRA.md 9.85 (3);
    # item 59): its emitters declare the given record's clock (`_emitter`); a
    # held family gives nothing and has no clock (9.45 (1); item 51)
    for number, entry in enumerate(measured):
        # A matter lamp (a lamp on a massive kind): the lamp verb is the same
        # verb, the family's clock the pair form; a massive kind without a
        # clock is a block's kind (its record a block's own or a block's
        # response) and a lamp on it has no clock to drive.
        family = families[entry.family]
        if entry.lamp is not None and family.massive_kind and family.phase_per_age is None:
            raise ValueError(
                f"measured[{number}].lamp on the massive kind {family.name!r} needs the "
                f"pair form of phase_per_link on the family under `massive_record` (the clock "
                "the lamp drives; the train carries the kind's band at it)"
            )


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
                    f"measured[{index}].table[{families[at].name!r}].phase_window is "
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
                    f"the multiplicity through the re-emitters of the world reaches "
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
            f"two paths of one record of {family_name!r} from the lamp "
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
    2^62 - 1 (the per-push bound, tested at every push), and the sum over
    the columns of the whole parts, each at most |E_c n_c| V_g / (D_c d_c)
    + 1, within the same bound (the column-sum bound), so that k terms each inside the
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
                        f"measured[{index}]: the push over the column {column.name!r} "
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
                    f"measured[{index}]: the pushes over the {len(columns)} columns from "
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
    a lamp is refused: nothing else givings its rows), and the ceilings of
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
                f"the massive family {family.name!r} has no lamp: its momentum label's "
                "magnitude p is its lamp's `momentum_magnitude`, one table per family"
            )
        if len(magnitudes) > 1:
            raise ValueError(
                f"the lamps of the massive family {family.name!r} declare two "
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
                f"the massive family {family.name!r}: momentum_magnitude {p} forms "
                f"(2 p |a|)^2 = (2 x {p} x {reach_table})^2 beyond the working bound "
                f"{MAX_WORK_INT} in the label's rounding (p at most {integer_root(MAX_WORK_INT) // (2 * reach_table)})"
            )
        rest = LABEL_SCALE * width * family.quantum
        if rest * rest > MOMENTUM_BOUND:
            raise ValueError(
                f"the massive family {family.name!r}: the rest energy E'_0 = Q S M = "
                f"{LABEL_SCALE} x {width} x {family.quantum} = {rest} has a square beyond the "
                f"integer bound {MOMENTUM_BOUND} (the pace wall E'_D is formed from it)"
            )
        for vector in table:
            label = scaled_label(vector, p)
            square = rest * rest + 3 * sum(c * c for c in label)
            if square > MOMENTUM_BOUND:
                raise ValueError(
                    f"the massive family {family.name!r} on the direction "
                    f"{list(vector)}: E'_D^2 = E'_0^2 + 3 p_D . p_D = {square} exceeds the integer "
                    f"bound {MOMENTUM_BOUND} (a smaller quantum, width or momentum_magnitude)"
                )
            reach = max(abs(c) for c in label)
            if reach * phase_steps > MOMENTUM_BOUND:
                raise ValueError(
                    f"the massive family {family.name!r} on the direction "
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
        raise ValueError("in_transit must be a list")
    names = {family.name: index for index, family in enumerate(families)}
    found: list[TransitDefinition] = []
    for index, entry in enumerate(value):
        label = f"in_transit[{index}]"
        obj = _object(
            entry, label, TRANSIT_KEYS, {"position", "family", "number", "direction", "amount"}
        )
        family_name = obj["family"]
        if not isinstance(family_name, str) or family_name not in names:
            raise ValueError(f"{label}.family names an unknown family")
        family = names[family_name]
        top = phase_steps - 1 if families[family].phase else 0
        direction = _direction(obj["direction"], f"{label}.direction", table, rest=True)
        amount = _integer(obj["amount"], f"{label}.amount", 1)
        age = _integer(obj.get("age", 0), f"{label}.age", 0, age_bound)
        lifetime = families[family].lifetime
        if lifetime is not None and age >= lifetime:
            raise ValueError(
                f"{label}.age {age} is at or beyond the lifetime {lifetime} of the "
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
                    f"{label}.hand {declared_hand:+d} differs from the hand {hand:+d} of "
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


def block_extents(side: int | tuple[int, int, int]) -> tuple[int, int, int]:
    """A block's extents per axis: the cube's side three times, or the box's
    extents as given."""
    if isinstance(side, int):
        return (side, side, side)
    return (int(side[0]), int(side[1]), int(side[2]))


def body_node_indices(
    shape: tuple[int, int, int],
    corner: tuple[int, int, int],
    side: int | tuple[int, int, int],
    wrap: tuple[bool, bool, bool],
) -> list[int]:
    """The block's Nodes as the engine forms them (`_box`): the box of the
    extents per axis (a cube's side for all three) from its lower corner,
    wrapped on a periodic axis of the kind, cut on an open one; the Nodes'
    flat indices in x-major order (x, then y, then z). The one copy of the
    rule in integers; the margin module's array form (`body_node_mask`) is
    built from it."""
    extents = block_extents(side)
    ranges: list[list[int]] = []
    for axis in range(3):
        indices = [corner[axis] + offset for offset in range(extents[axis])]
        if wrap[axis]:
            indices = [index % shape[axis] for index in indices]
        else:
            indices = [index for index in indices if 0 <= index < shape[axis]]
        ranges.append(sorted(set(indices)))
    if not all(ranges):
        return []
    stride_x, stride_y = shape[1] * shape[2], shape[2]
    return [x * stride_x + y * stride_y + z for x in ranges[0] for y in ranges[1] for z in ranges[2]]


def given_train_norm(
    now: Sequence[int],
    before: Sequence[int],
    shape: tuple[int, int, int],
    corner: tuple[int, int, int],
    extents: tuple[int, int, int],
    pair: tuple[int, int],
    wrap: tuple[bool, bool, bool],
) -> int:
    """THE GIVEN RECORD'S NORM ON THE VACUUM (ALGEBRA.md 9.17 (6a), 9.19 (3)):
    the conserved form of the train's two levels written on the body's
    Nodes and zero elsewhere, on the given family's vacuum (its pair [num,
    den] at every Node, the world's faces), in the flux's units of the
    engine's `conserved_form` with the wall num: the sum over the Nodes of
    3 den (now^2 + before^2) - num now (S_6 before); exact integers; the
    one copy the generator writes and the loader checks."""
    num, den = int(pair[0]), int(pair[1])
    count = int(shape[0]) * int(shape[1]) * int(shape[2])
    nodes = body_node_indices(shape, corner, extents, wrap)
    level_before = [0] * count
    for index, value in zip(nodes, before, strict=True):
        level_before[index] = int(value)
    read = six_neighbours_flat(level_before, shape, wrap)
    total = 0
    for index, now_value, before_value in zip(nodes, now, before, strict=True):
        total += 3 * den * (int(now_value) ** 2 + int(before_value) ** 2)
        total -= num * int(now_value) * read[index]
    return total


def given_train_flux_sign(
    now: Sequence[int],
    before: Sequence[int],
    extents: tuple[int, int, int],
    axis: int,
    sign: int,
) -> int:
    """THE FLUX SIGN ALONG THE TRAIN'S **K** (ALGEBRA.md 9.17 (6a), a load
    check): the sum over the body's Links along the axis, from each Node i
    to its neighbour j on the train's way, of the flux into j from i, now_j
    before_i - before_j now_i (the engine's G_ji of 9.19 (3), the flux into
    a Node from its neighbour); positive when the record travels as
    declared (the one-way flux leaves through the head)."""
    strides = (extents[1] * extents[2], extents[2], 1)
    total = 0
    for x in range(extents[0]):
        for y in range(extents[1]):
            for z in range(extents[2]):
                position = [x, y, z]
                if not 0 <= position[axis] + sign < extents[axis]:
                    continue
                i = x * strides[0] + y * strides[1] + z
                j = i + sign * strides[axis]
                total += int(now[j]) * int(before[i]) - int(before[j]) * int(now[i])
    return total


def six_neighbours_flat(
    values: Sequence[int], shape: tuple[int, int, int], wrap: tuple[bool, bool, bool]
) -> list[int]:
    """S_6 of a flat x-major integer array in exact integers: the sum of the
    six neighbours, a periodic axis wrapped (an axis of extent 1 reads the
    Node itself twice), an open axis reading 0 beyond its faces; the read of
    the law's rule and of the generator's iteration (ALGEBRA.md 9.22 (7))."""
    extents = (int(shape[0]), int(shape[1]), int(shape[2]))
    strides = (extents[1] * extents[2], extents[2], 1)
    total = [0] * len(values)
    for axis in range(3):
        extent, stride = extents[axis], strides[axis]
        for index, value in enumerate(values):
            coordinate = (index // stride) % extent
            for step in (1, -1):
                neighbour = coordinate + step
                if wrap[axis]:
                    neighbour %= extent
                elif not 0 <= neighbour < extent:
                    continue
                total[index + (neighbour - coordinate) * stride] += value
    return total


def mode_residual(
    profile: Sequence[int],
    num: Sequence[int],
    den: Sequence[int],
    clock: tuple[int, int],
    shape: tuple[int, int, int],
    wrap: tuple[bool, bool, bool],
    where: Sequence[bool] | None = None,
) -> tuple[int, int, tuple[int, int, int]]:
    """THE EIGEN-EQUATION'S RESIDUAL IN INTEGERS (ALGEBRA.md 9.22 (7) (ii),
    PROVED there as the bound for the rounded profile of an exact mode): at
    every Node i of `where` (every Node by default) the residual
    abs(b num_i (S_6 p)_i - 3 den_i a p_i) against the bound b (3 num_i + 6
    den_i), the clock [a, b] the mode's 2 cos omega as a rational; the
    Node of the largest excess with its residual and its bound (the
    residual at or below the bound everywhere means the profile is the
    operator's mode to within its rounding). Exact Python integers, the
    same on every host; the arrays flat in x-major order."""
    a, b = clock
    read = six_neighbours_flat(profile, shape, wrap)
    worst_index, worst_excess, worst_residual, worst_bound = 0, None, 0, 0
    for index, (p, n, d, s) in enumerate(zip(profile, num, den, read, strict=True)):
        if where is not None and not where[index]:
            continue
        residual = abs(b * n * s - 3 * d * a * p)
        bound = b * (3 * n + 6 * d)
        excess = residual - bound
        if worst_excess is None or excess > worst_excess:
            worst_index, worst_excess, worst_residual, worst_bound = index, excess, residual, bound
    stride_x, stride_y = int(shape[1]) * int(shape[2]), int(shape[2])
    node = (
        worst_index // stride_x,
        (worst_index // stride_y) % int(shape[1]),
        worst_index % int(shape[2]),
    )
    return worst_residual, worst_bound, node


# THE FILE'S DIGEST AND THE STAMP the generator writes (`input_digest`, `input_stamp`)
# live in the host module event_universe.world_files since item 72: the loader
# compares the stamp with the digest handed to it and computes none.


def _input_stamp_check(
    document: dict[str, object], measured: tuple[MeasuredDefinition, ...], digest: str | None
) -> None:
    """THE FILE'S HASH (the model owner's record 1886; ALGEBRA.md 9.22 (7) (i),
    9.90 (3) (c); BUILD.md section 26 item 28): a world with a seeded body
    carries `stamp` {hash}, the digest of the WHOLE document without `stamp`
    (the generator's stamp over every key, the profiles and the clocks among
    them), so that the file loaded is the one the generator wrote and a file
    changed by hand is regenerated, not run; no law identifier stands beside it
    (one engine, 9.90 (1)). A world with no profile needs no stamp."""
    if not any(entry.block is not None and entry.block.profile is not None for entry in measured):
        return
    value = document.get("stamp")
    if value is None:
        raise ValueError(
            "the world declares a seeded body and no `stamp`: the generator writes `stamp` "
            '{"hash": ...}, the digest of the whole file (the model owner\'s record 1886; '
            "ALGEBRA.md 9.22 (7) (i); BUILD.md section 26 item 28)"
        )
    stamp = _object(value, "stamp", STAMP_KEYS, STAMP_KEYS)
    written = stamp["hash"]
    if not isinstance(written, str):
        raise ValueError("stamp.hash must be a string")
    if digest is None:
        raise ValueError(
            "the stamp's check needs the file's digest, computed by the host module "
            "event_universe.world_files (the loader reads no file and hashes nothing)"
        )
    if written != digest:
        raise ValueError(
            f"stamp.hash {written[:12]}... is not the digest of the file "
            f"{digest[:12]}...: the document is not the one the generator stamped (a key changed "
            "after the stamp; the stamp covers the whole file, BUILD.md section 26 item 28; record "
            "1886); regenerate the file"
        )


def _initial_state_checks(
    shape: Address3,
    periodic: tuple[bool, bool, bool],
    families: tuple[FamilyDefinition, ...],
    measured: tuple[MeasuredDefinition, ...],
) -> None:
    """THE INPUT CHECKED LAWFUL OR REFUSED, IN INTEGERS (the model owner's
    record 1886; ALGEBRA.md 9.22 (3) and (7)): the initial state is stored
    once in the file and the loader says at load whether it is lawful, with
    no float. Every block's Nodes disjoint from every other block's (9.9
    (4); a cube beyond a face is the fit check's refusal, naming the axis
    and the vertex); for every body seeded with a profile, its clock a / b
    strictly above its family's band top 2 num / den (a bound mode) and
    below 2 (stable), and the eigen-equation's residual within its proved
    bound at every Node of the board outside the other bodies of its family
    (the body's own mode in place on the composed operator: at another
    body's Nodes the operator carries that body's summand, so those Nodes
    are its check, not this one's; Nature's reading for the mathematician's
    word, BUILD.md section 26 item 20); the tail rule of 9.35 (a body's mode
    0 at every Node of every other body of its family) is RETIRED by ALGEBRA.md
    9.96 (4) (commit 6). The remainders are 0 by
    construction (the profile is written at both levels with none); the
    amplitude's bound and the rich giving Nodes are checked where the block
    is parsed."""
    board = (int(shape[0]), int(shape[1]), int(shape[2]))
    count = board[0] * board[1] * board[2]
    blocks: list[tuple[int, MeasuredDefinition, BlockDefinition, list[int]]] = []
    for number, entry in enumerate(measured):
        block = entry.block
        if block is None:
            continue
        wrap = periodic
        corner = (int(entry.position[0]), int(entry.position[1]), int(entry.position[2]))
        # a cube beyond a face or wrapped onto itself is refused by the fit
        # check on the parsed world (naming the axis and the vertex)
        nodes = body_node_indices(board, corner, block.extents, wrap)
        own = set(nodes)
        for other_number, _, _, other_nodes in blocks:
            if own.intersection(other_nodes):
                raise ValueError(
                    f"measured[{number}] and measured[{other_number}] overlap: two "
                    "bodies' Nodes are disjoint (ALGEBRA.md 9.9 (4), 9.22 (3))"
                )
        blocks.append((number, entry, block, nodes))
    for number, entry, block, _nodes in blocks:
        if block.profile is None or block.clock is None:
            continue
        family = families[entry.family]
        kind = block.kind  # the body's rest pair (ALGEBRA.md 9.91 (7); commit 1)
        wrap = periodic
        a, b = block.clock
        # (iii) the band: a / b above the kind's band top 2 num / den and below 2
        if a * kind[1] <= 2 * kind[0] * b:
            raise ValueError(
                f"measured[{number}].clock [{a}, {b}] is not above the band's top "
                f"2 x {kind[0]} / {kind[1]} of the kind of the family {family.name!r}: the "
                "profile is no bound mode (ALGEBRA.md 9.22 (7) (iii); a well too shallow for its "
                "board, or a mode of the band)"
            )
        if a >= 2 * b:
            raise ValueError(
                f"measured[{number}].clock [{a}, {b}] is at or above 2: the mode is a "
                "runaway (no oscillation, a level growing every interval; ALGEBRA.md 9.19 (2), "
                "9.22 (7) (iii))"
            )
        # (ii) the residual on the composed operator of the family (every
        # body of the family in place), read outside the other bodies' Nodes
        num = [kind[0]] * count
        den = [kind[1]] * count
        where = [True] * count
        for other_number, other, other_block, other_nodes in blocks:
            if other.family != entry.family or other_block.kind != kind:
                continue
            for index in other_nodes:
                num[index] = other_block.pair[0]
                den[index] = other_block.pair[1]
                if other_number != number:
                    where[index] = False
        residual, bound, node = mode_residual(block.profile, num, den, block.clock, board, wrap, where)
        if residual > bound:
            raise ValueError(
                f"measured[{number}].seed is not the mode of its family's operator "
                f"within the rounding bound: at Node {list(node)} the eigen-equation's residual "
                f"{residual} is above the bound {bound} (the clock [{a}, {b}], the amplitude "
                f"{block.seed}); the generator writes the mode's integers and the loader checks "
                "them in integers (ALGEBRA.md 9.22 (7) (ii), the model owner's record 1886)"
            )
        # THE SEPARATION RULE OF 9.35 IS RETIRED (ALGEBRA.md 9.96 (4); the one stroke,
        # commit 6): each body's record is its own array and meets another body only
        # through the held families, so two bodies of one family may stand anywhere;
        # the tail check of item 28 is gone


def _connected_pieces(
    positions: list[Address3], shape: Address3, periodic: tuple[bool, bool, bool]
) -> int:
    """The number of pieces of a set of Nodes under the board's Links: two
    Nodes are linked when they differ by one on one axis (modulo the extent
    on a periodic axis); an axis of extent 1 links nothing."""
    remaining = set(positions)
    pieces = 0
    while remaining:
        pieces += 1
        frontier = [remaining.pop()]
        while frontier:
            node = frontier.pop()
            for axis in range(3):
                extent = int(shape[axis])
                if extent < 2:
                    continue
                for step in (1, -1):
                    coordinate = node[axis] + step
                    if periodic[axis]:
                        coordinate %= extent
                    elif not 0 <= coordinate < extent:
                        continue
                    neighbour = list(node)
                    neighbour[axis] = coordinate
                    candidate = (neighbour[0], neighbour[1], neighbour[2])
                    if candidate in remaining:
                        remaining.remove(candidate)
                        frontier.append(candidate)
    return pieces


# THE DETECTOR CUBE (the model owner's word of 2026-09-25, record 1899;
# ALGEBRA.md 9.25): a detector is one region, a cube of side 3 or more; its
# sensitivity is its whole cube, read by the flux into it through its Ports
# from outside; the click is the detector's, reported by its name and never
# by a Node. The cube is cut by the GameBoard on an axis whose extent is
# below the side (a chain's or a layer's thin axis), as a block's cube is.
DETECTOR_SIDE = 3


def _box_sides(
    positions: list[Address3], shape: Address3, periodic: tuple[bool, bool, bool]
) -> tuple[int, int, int] | None:
    """The sides of the box a set of Nodes fills, or None where it fills no
    box: per axis the distinct coordinates form one run (the shortest arc
    across a periodic seam) and the count of Nodes is the runs' product."""
    sides: list[int] = []
    for axis in range(3):
        coordinates = sorted({node[axis] for node in positions})
        extent = int(shape[axis])
        if periodic[axis]:
            run = min(max((c - start) % extent for c in coordinates) + 1 for start in coordinates)
        else:
            run = coordinates[-1] - coordinates[0] + 1
        if run != len(coordinates):
            return None
        sides.append(run)
    if sides[0] * sides[1] * sides[2] != len(set(positions)):
        return None
    return (sides[0], sides[1], sides[2])


def _detector_region(
    name: str,
    positions: list[Address3],
    shape: Address3,
    periodic: tuple[bool, bool, bool],
    one_node: bool = False,
) -> None:
    """The three refusals on a detector's Nodes: disconnected pieces (ALGEBRA.md
    9.25 (7)), no box, a side below DETECTOR_SIDE where the GameBoard's extent
    allows it (record 1899). THE ONE-NODE DETECTOR (ALGEBRA.md 9.46 (8) (c);
    the model owner's word of 2026-09-25 in Nature24's session, "start";
    BUILD.md section 26 item 40; SINCE COMMIT 7 on every world, ALGEBRA.md
    9.92, record 2109: several bodies on one Node each are several detectors):
    a detector may be ONE Node, a body's Node, its six Links its Ports (the
    cube's fifty-four HISTORY there, the counts rescaled by the Node's share);
    a set of more than one Node keeps the cube rule."""
    if one_node and len(set(positions)) == 1:
        return
    pieces = _connected_pieces(positions, shape, periodic)
    if pieces > 1:
        raise ValueError(
            f"the receiver {name!r} lies on {pieces} disconnected pieces; a detector "
            "is one connected region, and separate places are separate names (ALGEBRA.md "
            "9.25 (7))"
        )
    sides = _box_sides(positions, shape, periodic)
    if sides is None:
        raise ValueError(
            f"the receiver {name!r} on {len(positions)} Nodes fills no box; a "
            f"detector is one cube of side {DETECTOR_SIDE} or more, its Nodes the whole box of "
            f"its sides, cut by the GameBoard on an axis of extent below {DETECTOR_SIDE} (the "
            "model owner's word of 2026-09-25, record 1899)"
        )
    least = [min(DETECTOR_SIDE, int(shape[axis])) for axis in range(3)]
    if any(sides[axis] < least[axis] for axis in range(3)):
        raise ValueError(
            f"the receiver {name!r} is a box of sides {list(sides)}; a detector is "
            f"one cube of side {DETECTOR_SIDE} or more (at least {least} on this GameBoard), its "
            "sensitivity its whole cube and the click the detector's, never a Node's (the model "
            "owner's word of 2026-09-25, record 1899)"
            + (
                "; a detector is one Node (a body's) or a cube of three or more, nothing between "
                "(ALGEBRA.md 9.46 (8) (c), 9.92; BUILD.md section 26 item 40; commit 7)"
                if one_node
                else ""
            )
        )


def _detectors(
    value: object,
    shape: Address3,
    periodic: tuple[bool, bool, bool],
    measured: tuple[MeasuredDefinition, ...],
    body_record: bool,
    detector_law: bool,
) -> tuple[DetectorDefinition, ...]:
    if not isinstance(value, list):
        raise ValueError("detectors must be a list")
    at = {entry.position for entry in measured}
    # The other Nodes of the bodies on a set: a body is named by its centre.
    inside: set[Address3] = set()
    for entry in measured:
        inside.update(body_nodes(entry.position, entry.span, shape, periodic) or ())
    taken: set[Address3] = set()
    found: list[DetectorDefinition] = []
    for index, entry in enumerate(value):
        label = f"detectors[{index}]"
        _refuse_retired(entry, label, ("wheel",))
        obj = _object(entry, label, DETECTOR_KEYS, {"name"})
        if detector_law:
            # the ray law's threshold and reading kind: never read by the
            # detector law (the click is the ladder's), refused (record 2089)
            _refuse_under_law(obj, label, {"threshold", "reading"})
        name = obj["name"]
        if not isinstance(name, str) or not name:
            raise ValueError(f"{label}.name must be a nonempty string")
        if any(item.name == name for item in found):
            raise ValueError(f"two detectors named {name!r}")
        if name in FACE_NAMES:
            raise ValueError(
                f"{label}.name {name!r} is the name of a face detector (an open face "
                "of the GameBoard is a detector of that name; declare another)"
            )
        if name == LIFETIME_NAME:
            raise ValueError(
                f"{label}.name {name!r} is the name of the border every event of a "
                "family with a lifetime clicks on; declare another"
            )
        bound_block: int | None = None
        if "block" in obj:
            bound_block = _integer(obj["block"], f"{label}.block", 0, max(0, len(measured) - 1))
            if measured[bound_block].block is None:
                raise ValueError(
                    f"{label}.block {bound_block} names a measured event that is no "
                    "block; a receiver set on a BODY is `positions` on the body's Node "
                    "(DECLARATIONS.md section 15 M1-4)"
                )
            threshold = _integer(obj.get("threshold", 1), f"{label}.threshold", 1)
            bound_positions: list[Address3] = []
            if "positions" in obj:
                # the receiving set on free Nodes beside the block (the light
                # clock's cube adjacent to A's face, section 10 item 9): free
                # Nodes are admitted here, the set their receiver; the cube of
                # record 1899 as any detector
                positions_value = obj["positions"]
                if not isinstance(positions_value, list) or not positions_value:
                    raise ValueError(
                        f"{label}.positions with `block` must be a nonempty list of "
                        "Nodes, the receiving cube beside the block (DECLARATIONS.md section 10 "
                        "item 9; record 1899)"
                    )
                for item in positions_value:
                    position = _address(item, f"{label}.positions", shape)
                    if position in at or position in inside or position in taken:
                        raise ValueError(
                            f"{label}.positions with `block` names a Node of a measured "
                            f"event or of another set {list(position)}: the receiving set is a cube "
                            "of free Nodes beside the block"
                        )
                    taken.add(position)
                    bound_positions.append(position)
                _detector_region(name, bound_positions, shape, periodic, one_node=True)
            else:
                # A BODY IS ITS OWN DETECTOR, whatever its support (ALGEBRA.md 9.92, the
                # detectors' rule approved by the model owner, record 2109: a body of
                # several Nodes is one detector, a body of one Node its own, its six Links
                # its Ports, 9.46 (8) (c); item 40; commit 7): the cube rule of record
                # 1899 is the free set's, not a body's
                assert measured[bound_block].block is not None
            found.append(DetectorDefinition(name, tuple(bound_positions), threshold, block=bound_block))
            continue
        if "positions" not in obj:
            raise ValueError(f"{label} needs `positions` (or `block`, a set bound to a block)")
        positions_value = obj["positions"]
        if not isinstance(positions_value, list) or not positions_value:
            raise ValueError(f"{label}.positions must be a nonempty list of Nodes")
        positions = []
        for item in positions_value:
            position = _address(item, f"{label}.positions", shape)
            if position not in at:
                if position in inside:
                    raise ValueError(
                        f"{label}.positions names a Node of a body on a set "
                        f"{list(position)} that is not its position (a body is one record, "
                        "named by its centre)"
                    )
                raise ValueError(
                    f"{label}.positions names a Node without a measured event "
                    f"{list(position)} (a receiving set at a free Node beside a block declares "
                    "`block` with that one position, DECLARATIONS.md section 10 item 9)"
                )
            if position in taken:
                raise ValueError(f"a Node in two detectors {list(position)}")
            taken.add(position)
            positions.append(position)
        # THE DETECTOR IS ONE CONNECTED REGION, A CUBE (ALGEBRA.md 9.25 (7);
        # record 1899): its Nodes are connected by Links (across a periodic
        # seam too), fill one box, and the box's sides are DETECTOR_SIDE or
        # more where the GameBoard's extent allows; separate places are
        # separate names
        _detector_region(name, positions, shape, periodic, one_node=True)
        threshold = _integer(obj.get("threshold", 1), f"{label}.threshold", 1)
        if name.startswith(RESERVED_SET_PREFIX) or name in FACE_NAMES or name == LIFETIME_NAME:
            raise ValueError(
                f"{label}.name {name!r} is reserved: the layer names the measured "
                f"events outside every detector `{RESERVED_SET_PREFIX}<number>`, the faces and "
                "the border by their own names"
            )
        reading = obj.get("reading", DETECTOR_READINGS[0])
        if reading not in DETECTOR_READINGS and reading != SUM_READING:
            raise ValueError(
                f"{label}.reading must be one of {[*DETECTOR_READINGS, SUM_READING]}, not {reading!r}"
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
            f"optical must be a non-negative integer, gamma the post-Newtonian "
            f"parameter (nature's 1), not {value!r}"
        )
    return value


def _body_fit_check(world: NatureBeamWorld) -> None:
    """A body's cube whole on the board, never cut (the model owner's word of
    2026-09-24, 16:35Z and 16:48Z, through the Boss: the experimenter places
    the body exactly where he wants it; SIMULATOR_DEFINITIONS.md, the four
    building blocks, the body's condition 1): the Nodes [x0, x0 + s) on each
    axis from the lower vertex `position` with the edge `side` lie on the
    board on every axis the body's kind does not fold. On an open or closed
    axis the far vertex is on the board; on a periodic axis the extent is at
    least the edge (a cube across the seam is whole, a cube wrapped onto
    itself is not); the folded axis of extent 1 (a layer, a chain) is the
    one exception, the stabiliser's square or segment (ALGEBRA.md 8.2 and
    8.3). Refused naming the body, the axis and the extent; the engine's
    `_cube` and the margin module's `body_node_mask` then never cut."""
    shape = world.shape
    for number, entry in enumerate(world.measured):
        block = entry.block
        if block is None:
            continue
        wrap = world.kind_periodic(entry.family)
        for axis, name in enumerate(AXES):
            extent = int(shape[axis])
            corner = int(entry.position[axis])
            if extent == 1:
                continue
            side = block.extents[axis]
            if wrap[axis]:
                if extent < side:
                    raise ValueError(
                        f"measured[{number}]: the body of side {side} wraps onto "
                        f"itself on the periodic axis {name} of extent {extent} (a body is a whole "
                        "cube, square or segment on the board, never cut or folded but on an axis "
                        "of extent 1; the model owner's word of 2026-09-24, 16:35Z)"
                    )
            elif corner < 0 or corner + side > extent:
                raise ValueError(
                    f"measured[{number}]: the body of side {side} at {corner} on "
                    f"the axis {name} reaches {corner + side - 1} beyond the face at "
                    f"{extent - 1}: a body lies whole on the board, exactly where it is declared, "
                    "never cut to fit (the model owner's word of 2026-09-24, 16:35Z; move the "
                    "vertex or the edge, or open the axis as periodic)"
                )


def parse_world_document(
    document: object, files: Mapping[str, object], digest: str | None
) -> NatureBeamWorld:
    """Reject anything but a lawful world: the loader reads no file (the host hands it the documents and the digest) and refuses by name a key it does not read, a value outside its bounds and a stamp that is not the generator's."""
    if not isinstance(document, dict):
        raise ValueError("a world is a JSON object")
    old = [key for key in OLD_KEYS if key in document]
    if old:
        raise ValueError(
            f"a world of the Beam Law declares none of the earlier engines' "
            f"keys ({', '.join(old)}); see docs/MIGRATION.md"
        )
    # ONE ENGINE (ALGEBRA.md 9.90 (1)): the checks of the world key `law` ("beam",
    # "rays", "events") are CANCELLED; the key itself is refused by name below
    events = [key for key in EVENTS_KEYS if key in document]
    if events:
        raise ValueError(
            f"a world of the Beam Law declares none of the law of events' keys "
            f"({', '.join(events)}); see docs/MIGRATION.md"
        )
    if DELETED_AMPLITUDE_KEY in document:
        # The world key `amplitude` is deleted (stage (vii) step 4, the one
        # click): the record form is the law.
        raise ValueError(
            f"the world key {DELETED_AMPLITUDE_KEY!r} is deleted: the record form is "
            "the law and every lamp givings records; remove the key (docs/MIGRATION.md, the "
            "amplitude law (vii-4))"
        )
    _refuse_retired(
        document,
        "the world",
        (
            "law",
            "model_id",
            "detector_law",
            "input",
            "wheel",
            "clock_family",
            "charge_family",
            "charge_strength",
            "point_emitter",
        ),
    )
    # THE WORD (record 2128 (3)): under `detector_law` a world names its universe under
    # `universe` and the word `families` is refused; the ray law's world (a cancelled
    # path, loaded for the record) keeps its word `families` and never carries `universe`
    under_law = True  # one engine (9.90 (1)); the ray law's word `families` CANCELLED
    if under_law and "families" in document:
        raise ValueError(
            "the world.families is refused: a world names its universe under "
            "`universe` (the universe file's path, examples/events/universe.json, or the "
            "families' list inline in a unit test; the Boss's record 2128 (3))"
        )
    if not under_law and "universe" in document:
        raise ValueError(
            "the world.universe is the detector law's word (record 2128 (3)): a "
            "universe file's path is admitted under `detector_law` alone; the ray law's world "
            "names its families under `families`"
        )
    word = "universe" if under_law else "families"
    obj = _object(
        document,
        "the world",
        WORLD_KEYS,
        {"shape", "ticks", "K", "N", "release", word, "measured"},
    )
    # NO DEFAULT UNDER THE DETECTOR LAW (the model owner's record 2089; records
    # 2092 and 2094; BUILD.md section 26 item 57): the law's world declares
    # every key its path reads (the flags written true or false, the start
    # file, the faces, the wall's width, the events and the detectors), and
    # none the law never reads (the ray law's clock rate, release, push,
    # direction table, action and its two hypotheses' switches); a world
    # without `detector_law` is the ray law's until its deletion (record 2095)
    # ONE ENGINE (ALGEBRA.md 9.90 (1); the model owner's record 2103; the cancel of
    # docs/CANCELLED_WORLDS.md): the world key `detector_law` was the law's name and is
    # refused by name; every world is the engine's, and every branch below on the
    # flag's absence (the ray law's parse) is CANCELLED and unreachable
    early_law = True
    if early_law:
        _require_under_law(
            obj,
            "the world",
            {
                "boundary",
                "width",
                "clock_stamp",
                "massive_record",
                "body_record",
                "engine",
                "measured",
                "detectors",
            },
        )
        _refuse_under_law(
            obj,
            "the world",
            {"suspension", "direction_bound", "directions", "action", "meeting", "massive_rows"},
        )
    start = _engine_start(obj["engine"] if "engine" in obj else None, files, early_law)
    step = files.get(STEP_FILE)
    if not isinstance(step, Step):
        raise ValueError(
            f"the step file {STEP_FILE!r} is missing at the repository's root: the interval's order is its"
        )
    families_file: str | None = None
    as_written = obj  # the document as the generator stamped it (the universe's path, item 59)
    universe = obj[word]
    obj = dict(obj)
    del obj[word]
    if isinstance(universe, str):
        # THE ONE UNIVERSE FILE (item 59; record 2128 (3)): the path in place of the
        # list; the universe's integers from the file alone, the world's own refused
        # (the path reaches here under `detector_law` alone: the ray law's word is `families`)
        families_file = universe
        _refuse_under_law(obj, "the world", FAMILIES_INTEGERS | FAMILIES_TABLES)
        entries, integers = universe_file_entries(families_file, files)
        obj["families"] = entries
        obj.update(integers)
    else:
        obj["families"] = universe  # the families' list inline (a unit test's world)
    shape_value = obj["shape"]
    if not isinstance(shape_value, list) or len(shape_value) != 3:
        raise ValueError("shape must be three positive extents")
    extents = tuple(_integer(item, "shape", 1, 4096) for item in shape_value)
    shape: Address3 = (extents[0], extents[1], extents[2])
    boundary, periodic = _boundary(obj.get("boundary", BOUNDARIES[0]))
    closed = tuple(isinstance(boundary, dict) and boundary.get(axis) == CLOSED_FACE for axis in AXES)
    closed = (closed[0], closed[1], closed[2])
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
    # N declared in every file (no default: the model owner's rule through
    # the Boss, 2026-09-25; BUILD.md section 26 item 28; the 64 of the first
    # worlds HISTORY, written in each)
    phase_steps = _integer(obj["N"], "N", 2, MAX_PHASE_STEPS)
    if phase_steps & (phase_steps - 1):
        raise ValueError(f"N must be a power of two from 2 through {MAX_PHASE_STEPS}")
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
        raise ValueError("massive_rows must be true or false")
    if massive_rows and "age_bound" not in obj:
        raise ValueError(
            "age_bound is required with the world key `massive_rows`: a massive "
            "row flies at its family's pace |p| / E', below the flight's, so the default bound "
            "(twice the flight bound) is not its bound; declare the largest age a row may carry"
        )
    age_bound = _age_bound(obj.get("age_bound"), shape, periodic, table)
    # The clock stamp (the moving detector, 2026-09-22, the chief physicist's
    # design docs/designs/moving_detector/DESIGN.md section 7): true or
    # false, false by default; with it every line a measured event writes
    # (its `click`, `read`, `rerelease` and `become` lines and its face
    # click) carries `clock`, the event's own count of self-creations (its
    # `age`). A record field and no physics: it enters neither the model
    # identity nor the hypothesis list, and without it every record is byte
    # identical to what it was.
    clock_stamp = obj.get("clock_stamp", False)
    if type(clock_stamp) is not bool:
        raise ValueError("clock_stamp must be true or false (false by default)")
    detector_law = True  # one engine (9.90 (1)); the ray law's branches below CANCELLED
    # THE FACE SLAB (ALGEBRA.md 9.25 (10), the mathematician's reading: a face
    # one Node deep books 0.15 of a packet and reflects the rest, the slab as
    # deep as the packet books 0.96): the receiver `face` at every open
    # border is the slab of this depth, one detector, last on every ladder;
    # REQUIRED on a GameBoard with an open face under the detector law and
    # refused without that law (the slab is its receiver), NO DEFAULT (the
    # model owner's rule through the Boss, 2026-09-25; BUILD.md section 26
    # item 28); 0 on a GameBoard with no open face (no slab)
    open_axes = [name for axis, name in enumerate(AXES) if not periodic[axis] and not closed[axis]]
    if "face_depth" in obj and not detector_law:
        raise ValueError(
            "face_depth is refused without `detector_law` (the face slab is the local "
            "detector law's receiver; the ray law has no slab)"
        )
    if detector_law and open_axes and "face_depth" not in obj:
        raise ValueError(
            f"face_depth is required on a GameBoard open on {', '.join(open_axes)} "
            "under `detector_law`: the depth of the receiver slab at every open border, no "
            "default (ALGEBRA.md 9.25 (10); BUILD.md section 26 item 28)"
        )
    face_depth = _integer(obj["face_depth"], "face_depth", 1) if "face_depth" in obj else 0
    for axis, name in enumerate(AXES):
        if not periodic[axis] and face_depth > 1 and 2 * face_depth >= int(shape[axis]):
            raise ValueError(
                f"face_depth {face_depth} leaves no interior on the open axis {name} of "
                f"extent {shape[axis]} (two slabs of the depth fill it)"
            )
    # massive-record-v1: true or false, false by default; a kind's pair and
    # faces are admitted under it alone, and it needs the local detector law
    # (the kind's rule is that law's six-neighbour step).
    massive_record = obj.get("massive_record", False)
    if type(massive_record) is not bool:
        raise ValueError("massive_record must be true or false (off by default)")
    # THE BODY RECORD (ALGEBRA.md 9.46; BUILD.md section 26 item 37): true or
    # false, false by default (the lattice body); a body held as one
    # rotation on its clock pair needs the massive record's blocks
    body_record = obj.get("body_record", False)
    if type(body_record) is not bool:
        raise ValueError(
            "body_record must be true or false (ALGEBRA.md 9.46; off by default, the lattice body)"
        )
    if body_record and not massive_record:
        raise ValueError(
            "body_record needs massive_record: true (a body record is a block held as "
            "one rotation on its clock pair, ALGEBRA.md 9.46 (1))"
        )
    if massive_record and not detector_law:
        raise ValueError(
            "massive_record needs detector_law: true (a record "
            "kind of the local detector law; the ray law has no record's rows at Nodes)"
        )
    if any(closed) and not detector_law:
        raise ValueError(
            f"a face declared {CLOSED_FACE!r}: a closed GameBoard is refused without "
            "`detector_law` (a zero face without the take is the local detector law's; the ray law "
            "has no rows)"
        )
    # massive-record-v1: the amplitude bound A, declared per massive world;
    # REQUIRED under the detector law with `massive_record` (no default, the
    # model owner's record 2089; the ceiling 2^28 of item 31 RETIRED, ALGEBRA.md
    # 9.83 (2) (a): A is the one number, the rule's int64 total its bound)
    amplitude_bound = AMPLITUDE_BOUND
    if detector_law and massive_record and "amplitude_bound" not in obj:
        raise ValueError(
            "amplitude_bound is required with `massive_record`: "
            "A, the amplitude every row stays below, no default (the model owner's record 2089; "
            "ALGEBRA.md 9.57 (2), 9.83 (2) (a))"
        )
    if massive_record and "amplitude_bound" in obj:
        amplitude_bound = _integer(obj["amplitude_bound"], "amplitude_bound", 1, AMOUNT_BOUND)
    elif "amplitude_bound" in obj:
        raise ValueError("amplitude_bound is refused without the world key `massive_record`")
    # THE NODE CLOCK (the model owner's decision (5) of record 1962; ALGEBRA.md
    # 9.35 (2) and (3); BUILD.md section 26 item 31): Gamma, one integer from
    # 1, the clock pair (e, f) = (Gamma, Gamma + M) at every Node under the
    # detector law's rule (M the content held at the Node, 0 in the vacuum);
    # REQUIRED under `detector_law` with no default, refused without that law
    node_clock = 0
    if "node_clock" in obj and not detector_law:
        raise ValueError(
            "node_clock is refused without `detector_law` (the Node clock enters the "
            "local detector law's rule, ALGEBRA.md 9.35 (2); the ray law has no rule with a division)"
        )
    if detector_law and "node_clock" not in obj:
        raise ValueError(
            "node_clock is required: Gamma, the one integer of "
            "the Node clock (e, f) = (Gamma, Gamma + M) at every Node, no default (ALGEBRA.md "
            "9.35 (3); BUILD.md section 26 item 31)"
        )
    if detector_law:
        node_clock = _integer(obj["node_clock"], "node_clock", 1, AMOUNT_BOUND)
    # THE MOMENTUM'S UNIT Q (ALGEBRA.md 9.96 (1), 9.89 (2)): the universe's integer
    # `momentum_unit`, REQUIRED under `detector_law` with no default (the wall W = 3 Q
    # M of every body), refused without that law
    momentum_unit = 0
    if "momentum_unit" in obj and not detector_law:
        raise ValueError(
            "momentum_unit is refused without `detector_law` (the momentum's unit "
            "Q enters the wall W = 3 Q M of the detector law's bodies, ALGEBRA.md 9.96 (1))"
        )
    if detector_law and "momentum_unit" not in obj:
        raise ValueError(
            "momentum_unit is required: Q, the momentum's unit "
            "of the universe's integers, the wall W = 3 Q M of every body, no default (ALGEBRA.md "
            "9.96 (1), 9.89 (2); the model owner's record 2089)"
        )
    if detector_law:
        momentum_unit = _integer(obj["momentum_unit"], "momentum_unit", 1, AMOUNT_BOUND)
    # THE TWIST TABLE (ALGEBRA.md 9.96 (2)): the families file's, checked with Gamma and A;
    # admitted on an inline world of the law, refused without the law; an inline world
    # without it has no transport (the engine refuses a nonzero twist naming the Port)
    twist_table: TwistTable | None = None
    if "twist_table" in obj and not detector_law:
        raise ValueError("twist_table is refused without `detector_law` (ALGEBRA.md 9.81 (2))")
    if "twist_table" in obj:
        twist_table = _twist_table(obj["twist_table"], "twist_table", node_clock, amplitude_bound)
    # THE FAMILY GENERICITY (the model owner's record 2066; BUILD.md section 26
    # item 51): the families' roles of items 32 and 35 are their own
    # declarations (`held`, `reads`), read by `_families` below; the world
    # keys clock_family, charge_family and charge_strength are retired
    mode_axis: int | None = None
    if "mode_axis" in obj:
        if not massive_record:
            raise ValueError("mode_axis is refused without the world key `massive_record`")
        if obj["mode_axis"] not in AXES:
            raise ValueError(f"mode_axis must be one of {list(AXES)}")
        mode_axis = AXES.index(obj["mode_axis"])
    probes: tuple[Address3, ...] = ()
    if "probes" in obj:
        if not massive_record:
            raise ValueError("probes is refused without the world key `massive_record`")
        if not isinstance(obj["probes"], list):
            raise ValueError("probes must be a list of Nodes")
        probes = tuple(_address(item, "probes", shape) for item in obj["probes"])
    # The quantum of action of the turn by momentum, h: absent by default
    # (nothing turns by momentum), an integer from 1 when declared.
    action = None if "action" not in obj else _integer(obj["action"], "action", 1)
    declared = obj.get("measured", [])
    if phase_steps < AMPLITUDE_LEAST_STEPS and any(
        isinstance(entry, dict) and "lamp" in entry
        for entry in (declared if isinstance(declared, list) else [])
    ):
        # A record's circle holds the quarter turn of a reflection (the
        # amplitude law; every lamp givings records). Read off the document
        # before the measured events are parsed, so that this refusal
        # precedes theirs (`tests/test_amplitude_record.py` (b)).
        raise ValueError(
            f"a lamp is refused with N {phase_steps}: a record's circle holds the "
            f"quarter turn of a reflection, at least {AMPLITUDE_LEAST_STEPS} steps"
        )
    families = _families(
        obj["families"],
        phase_steps,
        age_bound,
        massive_rows,
        action,
        massive_record,
        amplitude_bound,
        detector_law,
    )
    if detector_law:
        _charge_labels(obj["families"], families, detector_law)
    # The bound is asked of a world with a MASSIVE FAMILY (a pair with den >
    # num; DECLARATIONS.md section 15 M1-10 lists the massive worlds): a
    # light world under `massive_record` (its probes, its mirror blocks of
    # light's kind) loads without it (the Boss's 03:44Z, the gate reviewer's line on the block's grace).
    if massive_record and "amplitude_bound" not in obj and any(f.massive_kind for f in families):
        raise ValueError(
            "a world with a massive family declares `amplitude_bound`, the amplitude "
            "A every row stays below (2^28 in every registered massive world since BUILD.md "
            "section 26 item 31, DECLARATIONS.md section 15 M1-10's 2^32 HISTORY; the load bound "
            "and the rows' run-time assertion use it; no default)"
        )
    # The meeting: true or false (false by default); under it a paid family
    # without a phase circle is refused, the phase being the register the
    # meeting reads the crowd into (there is no other on the record).
    meeting = obj.get("meeting", False)
    if type(meeting) is not bool:
        raise ValueError("meeting must be true or false")
    if meeting:
        for family in families:
            if not family.free and not family.phase:
                raise ValueError(
                    f"meeting is refused with the paid family {family.name!r} without a "
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
        massive_record,
        width,
        amplitude_bound,
        detector_law,
        momentum_unit,
    )
    _column_budget(families, measured, release)
    if detector_law:
        _held_bodies_checks(families, measured)
        _node_clock_bound(families, measured, amplitude_bound, node_clock)
    # THE WINDOW IS THE ONE GIVING (ALGEBRA.md 9.85 (5), 9.71 (1); record 2082 (4);
    # commit 7): every emitter declares its weight g and its rung's action; the world
    # key `point_emitter` and the train are retired (RETIRED_KEYS)
    for number, entry in enumerate(measured):
        block = entry.block
        if block is None or block.emitter is None:
            continue
        if block.emitter.weight is None:
            raise ValueError(
                f"measured[{number}].emitter declares no `weight`: the body's rotation is "
                "copied into the given row at its Node at a declared weight g, one integer from 1 "
                "(ALGEBRA.md 9.71 (1) (b), 9.85 (5); commit 7)"
            )
        if block.emitter.norm is not None and block.emitter.norm_denominator is None:
            raise ValueError(
                f"measured[{number}].emitter declares no `norm_denominator`: the window "
                "closes when the outward norm reaches the excitation's action norm / "
                "norm_denominator, the generator's exact rational (ALGEBRA.md 9.71 (1) (d))"
            )
    if body_record:
        # every seeded block carries its profile and its clock pair (the
        # generator's, under the stamp): the body record's shape and its
        # rotation's rational (ALGEBRA.md 9.46 (1), (9) (a))
        for number, entry in enumerate(measured):
            block = entry.block
            if block is None or block.seed <= 0:
                continue
            if block.profile is None or block.clock is None:
                raise ValueError(
                    f"measured[{number}] under body_record declares no `clock` with its "
                    "profile: a body record is its stored profile and one rotation on its clock pair "
                    "[num_c, den_c], the generator's (ALGEBRA.md 9.46 (1) and (9) (a); "
                    "`seed_on_the_mode`)"
                )
            if block.proper_clock is None and any(int(part) != 0 for part in entry.momentum):
                raise ValueError(
                    f"measured[{number}] under body_record moves and declares no "
                    "`proper_clock`: the body's Node of a moving body rotates at the proper pair of its "
                    "momentum, the moving mode's rotation at its moving centre, the generator's "
                    "(ALGEBRA.md 9.63 (3); `seed_on_the_mode`)"
                )
    _input_stamp_check(as_written, measured, digest)
    _initial_state_checks(shape, periodic, families, measured)
    families = _massive_families(families, measured, table, width, phase_steps, action)
    # The covariant readings (`covariant-readings-v1`): the key as declared,
    # its domain and its integers checked at load, None by default.
    # drive-b-v1 (2026-09-22): the world key `drive_b`, a boolean, false by
    # default; under it every free body's wall is tested at load.
    drive_b = obj.get("drive_b", False)
    if type(drive_b) is not bool:
        raise ValueError("drive_b must be true or false (drive-b-v1, off by default)")
    if drive_b:
        for entry in measured:
            if not entry.fixed:
                drive_wall(entry.momentum, sum(entry.held), width, obj.get("covariant_readings") is None)
    # flow-link-v1 (2026-09-22): the world key `flow_link`, a boolean, false
    # by default; the flow labels it declares are formed once at load by
    # `nature_beam.direction_flight` and `nature_beam.family_flight`, their
    # one product tested by division before it is formed.
    flow_link = obj.get("flow_link", False)
    if type(flow_link) is not bool:
        raise ValueError(
            f"flow_link must be true or false (flow-link, off by default), not {flow_link!r}"
        )
    # centred-step-v1 (2026-09-22): the world key `centred_step`, a boolean,
    # false by default (docs/designs/atom_give/CENTRED_STEP.md section 1).
    centred_step = obj.get("centred_step", False)
    if type(centred_step) is not bool:
        raise ValueError("centred_step must be true or false (centred-step-v1, off by default)")
    # atom-level-v1 (2026-09-22): the world key `atom_level`, a boolean,
    # false by default, and the bodies' `level` declarations under it
    # (docs/designs/atom_levels/LEVELS.md section 2 (b) and (c)).
    atom_level = obj.get("atom_level", False)
    if type(atom_level) is not bool:
        raise ValueError("atom_level must be true or false (atom-level-v1, off by default)")
    measured = _atom_levels(obj["measured"], measured, families, atom_level, action, ticks)
    covariant = _covariant(
        obj.get("covariant_readings"), measured, families, width, turn_rate, action, drive_b
    )
    in_transit = _in_transit(
        obj.get("in_transit", []), shape, families, measured, phase_steps, table, age_bound
    )
    detectors = _detectors(
        obj.get("detectors", []), shape, periodic, measured, body_record, detector_law
    )
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
                f"measured[{index}]: a moving body at gamma {optical} needs the "
                "key drive_b (form B's directional drive, the member of the age wall's set; "
                "the per-axis drive is never a member, docs/designs/one_wall/BODY_DRIVE.md)"
            )
        if drive_b:
            body_weight(entry.momentum, sum(entry.held), width, optical)
    readings = world_readings(obj, shape, detectors, families, measured)
    world = NatureBeamWorld(
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
        readings,
        step,
        action,
        meeting=meeting,
        massive_rows=massive_rows,
        covariant=covariant,
        optical=optical,
        drive_b=drive_b,
        flow_link=flow_link,
        centred_step=centred_step,
        clock_stamp=clock_stamp,
        face_depth=face_depth,
        atom_level=atom_level,
        detector_law=detector_law,
        massive_record=massive_record,
        body_record=body_record,
        probes=probes,
        mode_axis=mode_axis,
        closed=closed,
        amplitude_bound=amplitude_bound,
        node_clock=node_clock,
        momentum_unit=momentum_unit,
        twist_table=twist_table,
        start=start,
        universe_file=families_file,
    )
    if detector_law:
        _detector_law_load_checks(measured, families, table, periodic, phase_steps)
        set_names = {detector.name for detector in detectors}
        for number, entry in enumerate(measured):
            # the lamp record's ladder by name: every name a declared set's
            if entry.lamp is not None and entry.lamp.receiver is not None:
                for name in entry.lamp.receiver:
                    if name not in set_names:
                        raise ValueError(
                            f"measured[{number}].lamp.receiver names {name!r}, which no "
                            "detector set declares (the record's ladder is made of declared sets; "
                            "a face is never on it)"
                        )
            # the emitter body's ladder by name (ALGEBRA.md 9.17): every name a
            # declared set's
            if entry.block is not None and entry.block.emitter is not None:
                for name in entry.block.emitter.receiver or ():
                    if name not in set_names:
                        raise ValueError(
                            f"measured[{number}].emitter.receiver names {name!r}, which no "
                            "detector set declares (the record's ladder is made of declared sets; "
                            "a face is never on it)"
                        )
            # the receiver by name (DECLARATIONS.md section 13 item 7): the
            # set named must be declared; the names are listed in the refusal
            if entry.block is not None and entry.block.receiver is not None:
                names_declared = [detector.name for detector in detectors]
                if entry.block.receiver not in names_declared:
                    raise ValueError(
                        f"measured[{number}].receiver {entry.block.receiver!r} names no "
                        f"declared detector set (the sets declared: {names_declared}); the receiver "
                        "by name is a set's name (DECLARATIONS.md section 13 item 7)"
                    )
    _record_load_checks(measured, detectors, families, phase_steps)
    _aperture_load_check(measured, families, detectors, table, shape, periodic)
    _body_fit_check(world)
    # The push's denominator per column, Lambda_c^2 (`measured.counts_table`),
    # tested where Lambda_c is formed (`column_scales`): a world whose column
    # scales leave the register is refused here, at load, not at its first
    # push (the physics-rule review of the branch, REVIEW.md section 4).
    _ = world.column_scales
    return world
