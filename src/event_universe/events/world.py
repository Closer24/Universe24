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
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import NamedTuple

from event_universe.core.game_board import MAX_VALUE, PORT_HEADINGS, Address3
from event_universe.core.integer import (
    bounded_gcd,
    integer_root,
)
from event_universe.core.phase import MAX_PHASE_STEPS
from event_universe.core.readings import Reading, world_readings
from event_universe.core.register import discover
from event_universe.core.rule3 import rule_total_bound
from event_universe.core.schema import Context
from event_universe.core.step import STEP_FILE, Step
from event_universe.loader import frame
from event_universe.loader.frame import EngineStart

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
# THE WORLD'S KEYS are the frame's schema (loader/frame.py, `WORLD` and `HANDED`)
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
# The circle must hold the quarter turn of a reflection in a recorded world
# (`phase` + N / 4 exact on the tables): N below 4 is refused with it.
AMPLITUDE_LEAST_STEPS = 4
# The world key `doppler` of the reading's weight at the relative speed
# (`doppler-v1`, 2026-09-20, BEAM_LAW note 38 as it was), deleted on
# 2026-09-21 with the crossing rule (the model owner's record 158 of
# 2026-09-20; note 48): a moving body's Doppler is the count of the rows
# it crosses, no weight. A world that declares the key is refused as an
# unknown key (MIGRATION).


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
# A column's declaration on a family: its value per unit of content and
# the column's sign.
# The most columns a world may carry, the built-in two included: the
# per-group work of the push is then fixed (the mathematician's P2).
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
# THE UNIVERSE'S INTEGERS are the frame's schema (loader/frame.py, `INTEGERS`)
# THE TWIST TABLE in the integers block (ALGEBRA.md 9.81 (2) (b), 9.96 (2) (c), (d)):
# {unit, fine, coarse}; `unit` the integer 4 Gamma 2^16 whose inverse is theta_unit in
# radians; `fine` 2^10 triples (c, s, d) for the angles k_0 theta_unit; `coarse` at most
# 2^15 triples for the angles k_1 2^10 theta_unit; every triple c^2 + s^2 = d^2 exactly,
# d at most 10^9, the nearest the generator finds (`twist_triple`); the transport's
# triple for k = k_1 2^10 + k_0 is their exact product.
TWIST_UNIT_SCALE = 1 << 16
TWIST_FINE_BITS = 10
TWIST_COARSE_MOST = 1 << 15
TWIST_TRIPLE_BOUND = 10**9
# THE ENTRY's keys are the folders' cards (loader/frame.py, `entry_kind`; ALGEBRA.md 9.117 item 2)
PARTS_FORMS = ((1,), (1, 3), (1, 3, 6))
HELD_COUNTS = ("content", "sign")
HELD_DIPOLES = ("spin", "moment")
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
        if not isinstance(rows, list | tuple) or not least <= len(rows) <= most:
            raise ValueError(
                f"{label}.{name} must be a list of {least} to {most} triples [c, s, d] "
                "(ALGEBRA.md 9.96 (2) (c))"
            )
        triples: list[tuple[int, int, int]] = []
        for index, row in enumerate(rows):
            where = f"{label}.{name}[{index}]"
            if (
                not isinstance(row, list | tuple)
                or len(row) != 3
                or any(type(item) is not int for item in row)
            ):
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
    """The universe file read through the frame (loader/frame.py: its integers by the
    frame's schema, every family's entry by the folders' cards, a read's weight word
    resolved to the universe's integer) and translated to the families list the parse
    reads (item 51's attributes and the one stroke's, ALGEBRA.md 9.91 (7)), with the
    universe's integers. THE TRANSLATION: `parts` as declared; `phase` to `levels`;
    `pair` [num, den] or "body"; `held` {count, factors, dipole, dipole_div} to `held`
    (the count word), `held_factors`, `held_dipole`, `held_dipole_div` (as written,
    no default: the universe file writes it); `reads` with `by` 1 or "q" to the
    loader's words, `twist` kept; `self_source.unit` to `self_unit`; `clicks` to
    `clicks` with the quantum, `quantum` 1 on a family without clicks (a held family,
    one click one unit); `charge` 0 on every family (a body's charge is the body's
    number, 9.91 (7); the hold writes it, commit 2). A key of a card this translation
    has no word for (`sourced`, the source's, read by no loop yet) is carried as
    written and refused by name in `_families`. The folders' rules the cards do not
    state stay here until the switch: the three forms of `parts`, the self-source's
    unit 0 or at least 24 A, a family held or clicking or both."""
    entries, universe = frame.universe(value, files, discover())
    label = f"the universe file {value!r}"
    translated: list[dict[str, object]] = []
    for index, obj in enumerate(entries):
        where = f"{label}.families[{index}]"
        parts = obj["parts"]
        assert isinstance(parts, tuple)
        if parts not in PARTS_FORMS:
            raise ValueError(
                f"{where}.parts must be one of {[list(form) for form in PARTS_FORMS]}: "
                "the representation as a list of parts, the time part first (ALGEBRA.md 9.86 (2), "
                "9.91 (1))"
            )
        self_source = obj["self_source"]
        assert isinstance(self_source, dict)
        self_unit = self_source["unit"]
        amplitude = universe["amplitude_bound"]
        assert isinstance(self_unit, int) and isinstance(amplitude, int)
        if 0 < self_unit < 24 * amplitude:
            raise ValueError(
                f"{where}.self_source.unit {self_unit} is below 24 A = "
                f"{24 * amplitude}: the self-source's unit P_2 is 0 (off) or "
                "at least 24 A (ALGEBRA.md 9.91 (5))"
            )
        pair_value = obj["pair"]
        if "held" not in obj and "clicks" not in obj:
            raise ValueError(
                f"{where} declares neither held (a field family) nor clicks (a family "
                "of records): a family does one or both (ALGEBRA.md 9.86 (2))"
            )
        legacy: dict[str, object] = {
            "name": obj["name"],
            "charge": 0,
            "pair": list(pair_value) if isinstance(pair_value, tuple) else pair_value,
            "parts": list(parts),
            "levels": obj["phase"],
            "self_unit": self_unit,
        }
        raw_reads = obj["reads"]
        assert isinstance(raw_reads, tuple)
        reads: list[dict[str, object]] = []
        for read in raw_reads:
            assert isinstance(read, dict)
            reads.append(
                {
                    "family": read["family"],
                    "weight": read["weight"],
                    "by": READ_BY_WORDS[read["by"]],
                    "twist": read["twist"],
                }
            )
        legacy["reads"] = reads
        if "held" in obj:
            source = obj["held"]
            assert isinstance(source, dict)
            legacy["held"] = source["count"]
            legacy["held_factors"] = list(source["factors"])
            legacy["held_dipole"] = source["dipole"]
            legacy["held_dipole_div"] = source["dipole_div"]
        if "clicks" in obj:
            clicks = obj["clicks"]
            assert isinstance(clicks, dict)
            legacy["clicks"] = {"gives": clicks["gives"], "takes": clicks["takes"]}
            legacy["quantum"] = clicks["quantum"]
        else:
            legacy["quantum"] = 1
        for key, as_written in obj.items():
            if key not in ("name", "parts", "phase", "pair", "self_source", "reads", "held", "clicks"):
                legacy[key] = as_written
        translated.append(legacy)
    return translated, universe


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
# THE BODY'S KEYS are the frame's schema (loader/frame.py, `BODY`)
# CANCELLED (docs/CANCELLED_WORLDS.md section 9; ALGEBRA.md 9.90 (1)): the ray law's lamp keys (read by the cancelled parse alone)
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
# The keys of the clock trigger that a table entry (the click trigger) may
# not carry: the window is its gate.
CLOCK_ONLY_KEYS = ("at", "crowd")
# A window read from a reading (issue #363, 2026-09-20): the family whose
# rows at the set give the centre, and the offset added to it.
WINDOW_READING_KEYS = {"reads", "offset"}
# THE DETECTOR'S KEYS are the frame's schema (loader/frame.py, `DETECTOR`)
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
    given: None = None  # the ray law's given train, read by the loop as None (its cancelled branch)
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
    span: tuple[int, int, int] = ONE_NODE
    phase_by_momentum: bool = False
    held: tuple[int, ...] = ()
    contact: tuple[str, ...] = ()
    # the ray law's splits and lamp, read by the loop as None (its cancelled branches)
    splits: tuple[None, ...] = ()
    lamp: None = None
    # The block (massive-record-v1): the measured event's Nodes, pair,
    # seed and the rest, or None (a body of one Node or a span as before).
    block: BlockDefinition | None = None


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
    detectors: tuple[DetectorDefinition, ...]
    readings: tuple[Reading, ...]
    step: Step
    # The clock stamp (the world key `clock_stamp`, false by default): every
    # line a measured event writes carries `clock`, its own count of
    # self-creations; a record field, no physics, no hypothesis.
    clock_stamp: bool = False
    # the face receiver's depth at every open border (ALGEBRA.md 9.25 (10)),
    # declared in the file under the detector law (no default, BUILD.md
    # section 26 item 28); 0 on a GameBoard with no open face (no slab)
    face_depth: int = 0
    # massive-record-v1 (2026-09-23): the massive record kind beside light
    # under the local detector law, false by default; under it a family may
    # declare its `pair`; its faces are the world's.
    massive_record: bool = False
    # THE BODY RECORD (ALGEBRA.md 9.46 (1) to (3); BUILD.md section 26 item
    # 37): true holds every seeded block as one rotation on its clock pair
    # (a Node with a shape), its profile read and never stepped; false, the
    # default, the lattice body (its own rows on the GameBoard)
    body_record: bool = False
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

    def detector_of(self, position: Address3) -> int | None:
        """The index of the detector a Node belongs to, if any."""
        for index, detector in enumerate(self.detectors):
            if position in detector.positions:
                return index
        return None


# THE RETIRED KEY OF THE TAKE (ALGEBRA.md 9.19 (3); BUILD.md section 26 items 14 and 15):
# refused by name on an inline family with what stands in its place (every other retired key
# is no key of the frame's schemas and is refused there as unknown)
RETIRED_KEYS = {
    "take": "the take retired: nothing absorbs, no Port follows a wave (9.19 (3))",
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
    if not isinstance(value, list | tuple) or len(value) != 2:
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
    if not isinstance(value, list | tuple) or len(value) != 3:
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


def _charge_labels(raw: object, families: tuple[FamilyDefinition, ...]) -> None:
    """THE SIGN ON THE QUANTUM (ALGEBRA.md 9.48 (1); BUILD.md section 26 item
    35): under the detector law every family declares its `charge` q, one
    of -1, 0 and +1 per quantum (light 0, a matter family its own), no
    default; the label passes whole in the click, a body's charge Q the
    signed sum of the quanta it holds."""
    if not isinstance(raw, list):
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
        # NO DEFAULT (record 2089; item 57): the pair, the charge and the reads declared
        # (the clock `phase_per_link` on the given family, 9.62 (1)); the ray law's
        # phase, lifetime, hand, columns and massive flag never read, refused
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
        charge = _signed_ratio(obj.get("charge", 0), f"families[{index}].charge")
        if quantum != FREE_QUANTUM and charge[1] != 1:
            raise ValueError(
                f"families[{index}].charge: a paid family's charge is per unit of "
                f"amount and whole (an integer; the pair {list(charge)} is refused on {name!r}; D-1, "
                "2026-09-20)"
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
        # the ray law's lifetime, hand, massive and columns are refused above (no key of the file)
        lifetime = None
        hand = NO_HAND
        massive = False
        declared_pair = _kind_pair(obj, f"families[{index}]", massive_record, amplitude_bound)
        pair = MASSLESS_PAIR if declared_pair is None else declared_pair
        if "phase_per_link" in obj and not isinstance(obj["phase_per_link"], list):
            # under the law a family's clock is the pair form (ALGEBRA.md 9.17 (6));
            # the integer form is the ray law's turn per Link
            raise ValueError(
                f"families[{index}].phase_per_link is an integer: a "
                "family declares the pair form of its clock [p, q] or none, the given record's "
                "clock then its emitter's (ALGEBRA.md 9.17 (6), 9.85 (3))"
            )
        _refuse_family_faces(obj, f"families[{index}]")
        generic.append(_family_generic(obj, f"families[{index}]"))
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
    family_names = [family.name for family in found]
    families = tuple(
        FamilyDefinition(
            family.name,
            family.quantum,
            family.charge,
            family.phase,
            family.phase_per_link,
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
        for index, (family, attributes) in enumerate(zip(found, generic, strict=True))
    )
    _held_family_shapes(families)
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


def _family_generic(obj: dict[str, object], label: str) -> FamilyAttributes:
    """THE FAMILY GENERICITY (the model owner's record 2066; BUILD.md section
    26 item 51) AND THE COMPLETE ATTRIBUTE SET (ALGEBRA.md 9.86 (3), 9.91 (7);
    the one stroke, commit 1): the family's own declaration of what it is,
    `held` (with `held_factors`, `held_dipole`, `held_dipole_div`), `parts`,
    `levels`, `self_unit`, `clicks` and `reads` (the reads by name, resolved
    after every family is read). Every family declares `reads` (a field family with no waves the empty
    list: the plain rule), no default. The booking is derived (item 53):
    exactly a family with clicks; an inline entry without `clicks` is a
    family of records unless held (the tests' small lists)."""
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
    if "reads" not in obj:
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


def _held_family_shapes(families: tuple[FamilyDefinition, ...]) -> None:
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
    for source in HELD_SOURCES:
        holders = [family.name for family in families if family.held == source]
        if len(holders) > 1:
            raise ValueError(
                f"two families hold {source!r}: {holders}; one family holds each "
                "source (the level the others read is one array; BUILD.md section 26 item 51)"
            )


def _window(value: object, label: str, phase_steps: int) -> int:
    """A phase window's setting: a step of the circle, 0 through N - 1."""
    return _integer(value, label, 0, phase_steps - 1)


def axis_sign(axis: Vector, direction: Vector) -> int:
    """The sign of the inner product of an axis (a heading) with a direction
    vector, in {-1, 0, +1}: the right-hand rule's one integer (BEAM_LAW
    note 39). An axis is a heading, so the product is one component of the
    direction with a sign, within P; the sign is the same on the direction's
    unit label u_d, whose components carry the direction's signs."""
    product = sum(int(a) * int(d) for a, d in zip(axis, direction, strict=True))
    return (product > 0) - (product < 0)


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


def _receiver_names(obj: dict[str, object], label: str) -> tuple[str, ...] | None:
    """The lamp's `receiver`, its records' ladder by name: a set's name or a
    list of distinct names; None without the key."""
    if "receiver" not in obj:
        return None
    value = obj["receiver"]
    names = [value] if isinstance(value, str) else list(value) if isinstance(value, tuple) else value
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


GATE_KINDS = ("cnot",)
LABEL_BITS_BOUND = 32


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
        if not isinstance(value, list | tuple) or len(value) != 3:
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
    if not isinstance(value, list | tuple) or len(value) != 2:
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
        if not isinstance(kind_value, list | tuple) or len(kind_value) != 2:
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
    if isinstance(obj["seed"], list | tuple):
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
            not isinstance(value, list | tuple)
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
            not isinstance(value, list | tuple)
            or len(value) != count
            or any(
                not isinstance(item, list | tuple)
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
    _require_under_law(obj, label, {"q", "spin", "moment", "twist"})
    charge = 0 if "q" not in obj else _integer(obj["q"], f"{label}.q", -AMOUNT_BOUND, AMOUNT_BOUND)
    spin = _axes_vector(obj.get("spin", [0, 0, 0]), f"{label}.spin")
    moment = _axes_vector(obj.get("moment", [0, 0, 0]), f"{label}.moment")
    if "margin" not in obj and pair[0] * kind[1] > pair[1] * kind[0]:
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
    if not isinstance(value, list | tuple) or len(value) != 3:
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
    assert isinstance(value, dict)  # the frame's checked emitter (loader/frame.py, `EMITTER`)
    obj = value
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
    receiver = _receiver_names(obj, label)
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
        weight=weight,
        norm_denominator=norm_denominator,
        part=part,
        twist=twist,
    )


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
    momentum_unit: int = 0,
) -> tuple[MeasuredDefinition, ...]:
    assert isinstance(value, tuple)  # the frame's checked bodies (loader/frame.py, `BODY`)
    names = {family.name: index for index, family in enumerate(families)}
    found: list[MeasuredDefinition] = []
    # Every Node of every body so far: two measured events never share one.
    occupied: set[Address3] = set()
    for index, entry in enumerate(value):
        label = f"measured[{index}]"
        assert isinstance(entry, dict)
        obj = entry
        if "nodes" in obj:
            raise ValueError(
                f"{label} is a body in the law's form (its Nodes with their counts): "
                "the loop reads a body by its position until the count's line is bound to it"
            )
        if "side" in obj or "extents" in obj:
            # NO DEFAULT UNDER THE DETECTOR LAW (record 2089; item 57): the drive's ramp and
            # start on every block; the momentum and the stocks are the schema's required keys
            _require_under_law(obj, label, {"ramp", "start"})
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
        declared_held = obj["stocks"]
        assert isinstance(declared_held, dict)
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
        # the ray law's phase, phase_by_momentum, directions, table and become are no keys of
        # the file (the frame refuses them by name); the loop still reads their attributes
        phase = 0
        momentum_value = obj["momentum"]
        assert isinstance(momentum_value, tuple)
        momentum = tuple(_integer(item, f"{label}.momentum", -AMOUNT_BOUND) for item in momentum_value)
        fixed = obj.get("fixed", False)
        assert isinstance(fixed, bool)
        turning = False
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
            list(range(HEADING_OFFSET, FIXED_DIRECTIONS)), f"{label}.directions", table
        )
        # the table's rules of the ray law: every family at its key's rule, no entry declared
        rules: list[str] = []
        windows: list[int | None] = []
        reads: list[str] = []
        for rule, window, component in default_table(families):
            rules.append(rule)
            windows.append(window)
            reads.append(component)
        # The rule of a contact per family: the entry's rule where it
        # differs from the keys' own rule for the family, `measure` (the
        # keys' rule for a paid arrival, the body's momentum its own label)
        # where the entry is the keys' own, declared or not, and under a
        # `become` entry (the click's hand-over; no transformation fires
        # at a contact: a body is not a click of the entry's family).
        contact = [CONTACT_DEFAULT for _ in families]
        for held_family, content in enumerate(held):
            if content and families[held_family].free:
                # The label of a free release: amount x D along a heading,
                # of the event's own family and of every free family held.
                _label_bound(content * release[0] // release[1] or 1, 1, table, directions, label)
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
            False,
            span,
            shape,
            amplitude_bound,
            phase_steps,
            periodic,
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
                span,
                turning,
                tuple(held),
                tuple(contact),
                block=block,
            )
        )
    return tuple(found)


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
) -> tuple[DetectorDefinition, ...]:
    assert isinstance(value, tuple)  # the frame's checked detectors (loader/frame.py, `DETECTOR`)
    at = {entry.position for entry in measured}
    # The other Nodes of the bodies on a set: a body is named by its centre.
    inside: set[Address3] = set()
    for entry in measured:
        inside.update(body_nodes(entry.position, entry.span, shape, periodic) or ())
    taken: set[Address3] = set()
    found: list[DetectorDefinition] = []
    for index, entry in enumerate(value):
        label = f"detectors[{index}]"
        assert isinstance(entry, dict)
        obj = entry
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
            threshold = 1  # the ray law's key is gone; the loop still reads the attribute
            bound_positions: list[Address3] = []
            if "positions" in obj:
                # the receiving set on free Nodes beside the block (the light
                # clock's cube adjacent to A's face, section 10 item 9): free
                # Nodes are admitted here, the set their receiver; the cube of
                # record 1899 as any detector
                positions_value = obj["positions"]
                if not isinstance(positions_value, list | tuple) or not positions_value:
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
        if not isinstance(positions_value, list | tuple) or not positions_value:
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
        threshold = 1  # the ray law's key is gone; the loop still reads the attribute
        if name.startswith(RESERVED_SET_PREFIX) or name in FACE_NAMES or name == LIFETIME_NAME:
            raise ValueError(
                f"{label}.name {name!r} is reserved: the layer names the measured "
                f"events outside every detector `{RESERVED_SET_PREFIX}<number>`, the faces and "
                "the border by their own names"
            )
        reading = DETECTOR_READINGS[0]  # the ray law's key is gone; the loop still reads the attribute
        if reading not in DETECTOR_READINGS and reading != SUM_READING:
            raise ValueError(
                f"{label}.reading must be one of {[*DETECTOR_READINGS, SUM_READING]}, not {reading!r}"
            )
        found.append(DetectorDefinition(name, tuple(positions), threshold, str(reading)))
    return tuple(found)


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
    # THE WORLD'S KEYS through the frame (loader/frame.py, `WORLD`): an unknown key, a missing
    # key and a wrong kind refused by name; the universe, the bodies, the detectors, the
    # readings, the records in transit, the covariant readings and an inline twist table
    # handed on as written to their readers below
    obj = frame.world(document)
    # ONE ENGINE (ALGEBRA.md 9.90 (1); the model owner's record 2103): every world is the
    # engine's; every branch below on the flag's absence (the ray law's parse) is CANCELLED
    # and unreachable
    word = "universe"
    # THE ENGINE START FILE (ALGEBRA.md 9.83 (2) (a)): one canonical copy at
    # examples/events/engine_start.json, named by every world by its repository path
    # (`engine`, a required word of the frame's schema) and read by the frame (`START`)
    engine = obj["engine"]
    assert isinstance(engine, str)
    start = frame.start(engine, files)
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
        families_file = universe
        _refuse_under_law(obj, "the world", set(frame.INTEGERS.keys))
        entries, integers = universe_file_entries(families_file, files)
        obj["families"] = entries
        obj.update(integers)
    else:
        obj["families"] = universe  # the families' list inline (a unit test's world)
    shape_value = obj["shape"]
    assert isinstance(shape_value, tuple)
    extents = tuple(_integer(item, "shape", 1, 4096) for item in shape_value)
    shape: Address3 = (extents[0], extents[1], extents[2])
    boundary, periodic = _boundary(obj["boundary"])
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
    # the ray law's keys suspension, direction_bound, directions, action, meeting and
    # massive_rows are no keys of the file (the frame refuses them by name); the values below
    # and the world's fields carrying them are read by no line of the loop (DEAD, deleted whole)
    suspension = (1, 1)
    width = obj["width"]
    assert isinstance(width, int)
    bound = DEFAULT_DIRECTION_BOUND
    table = _direction_table([], bound)
    massive_rows = False
    age_bound = _age_bound(obj.get("age_bound"), shape, periodic, table)
    clock_stamp = obj["clock_stamp"]
    assert isinstance(clock_stamp, bool)
    # THE FACE SLAB (ALGEBRA.md 9.25 (10), the mathematician's reading: a face
    # one Node deep books 0.15 of a packet and reflects the rest, the slab as
    # deep as the packet books 0.96): the receiver `face` at every open
    # border is the slab of this depth, one detector, last on every ladder;
    # REQUIRED on a GameBoard with an open face under the detector law and
    # refused without that law (the slab is its receiver), NO DEFAULT (the
    # model owner's rule through the Boss, 2026-09-25; BUILD.md section 26
    # item 28); 0 on a GameBoard with no open face (no slab)
    open_axes = [name for axis, name in enumerate(AXES) if not periodic[axis] and not closed[axis]]
    if open_axes and "face_depth" not in obj:
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
    massive_record = obj["massive_record"]
    assert isinstance(massive_record, bool)
    body_record = obj["body_record"]
    assert isinstance(body_record, bool)
    if body_record and not massive_record:
        raise ValueError(
            "body_record needs massive_record: true (a body record is a block held as "
            "one rotation on its clock pair, ALGEBRA.md 9.46 (1))"
        )
    # massive-record-v1: the amplitude bound A, declared per massive world;
    # REQUIRED under the detector law with `massive_record` (no default, the
    # model owner's record 2089; the ceiling 2^28 of item 31 RETIRED, ALGEBRA.md
    # 9.83 (2) (a): A is the one number, the rule's int64 total its bound)
    amplitude_bound = AMPLITUDE_BOUND
    if massive_record and "amplitude_bound" not in obj:
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
    # REQUIRED with no default
    if "node_clock" not in obj:
        raise ValueError(
            "node_clock is required: Gamma, the one integer of "
            "the Node clock (e, f) = (Gamma, Gamma + M) at every Node, no default (ALGEBRA.md "
            "9.35 (3); BUILD.md section 26 item 31)"
        )
    node_clock = _integer(obj["node_clock"], "node_clock", 1, AMOUNT_BOUND)
    # THE MOMENTUM'S UNIT Q (ALGEBRA.md 9.96 (1), 9.89 (2)): the universe's integer
    # `momentum_unit`, REQUIRED with no default (the wall W = 3 Q M of every body)
    if "momentum_unit" not in obj:
        raise ValueError(
            "momentum_unit is required: Q, the momentum's unit "
            "of the universe's integers, the wall W = 3 Q M of every body, no default (ALGEBRA.md "
            "9.96 (1), 9.89 (2); the model owner's record 2089)"
        )
    momentum_unit = _integer(obj["momentum_unit"], "momentum_unit", 1, AMOUNT_BOUND)
    # THE TWIST TABLE (ALGEBRA.md 9.96 (2)): the families file's, checked with Gamma and A;
    # admitted on an inline world; an inline world without it has no transport (the
    # engine refuses a nonzero twist naming the Port)
    twist_table: TwistTable | None = None
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
        mode_axis = AXES.index(str(obj["mode_axis"]))
    probes: tuple[Address3, ...] = ()
    if "probes" in obj:
        if not massive_record:
            raise ValueError("probes is refused without the world key `massive_record`")
        declared_probes = obj["probes"]
        assert isinstance(declared_probes, tuple)
        probes = tuple(_address(item, "probes", shape) for item in declared_probes)
    action = None
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
    )
    _charge_labels(obj["families"], families)
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
    # THE BODIES AND THE DETECTORS through the frame (loader/frame.py, `BODY`, `DETECTOR`):
    # every key checked with the families known, an unknown key refused by name
    bodies = frame.bodies(obj["measured"], Context(tuple(family.name for family in families)))
    measured = _measured(
        bodies,
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
        momentum_unit,
    )
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
    detectors = _detectors(frame.detectors(obj["detectors"]), shape, periodic, measured, body_record)
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
        detectors,
        readings,
        step,
        clock_stamp=clock_stamp,
        face_depth=face_depth,
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
    _detector_law_load_checks(measured, families, table, periodic, phase_steps)
    set_names = {detector.name for detector in detectors}
    for number, entry in enumerate(measured):
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
    _body_fit_check(world)
    # The push's denominator per column, Lambda_c^2 (`measured.counts_table`),
    # tested where Lambda_c is formed (`column_scales`): a world whose column
    # scales leave the register is refused here, at load, not at its first
    # push (the physics-rule review of the branch, REVIEW.md section 4).
    return world
