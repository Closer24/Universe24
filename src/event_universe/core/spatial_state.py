"""Fixed local records for optional initialization-defined spatial fields."""

from dataclasses import dataclass, replace
from dataclasses import field as dataclass_field
from functools import lru_cache

from .disturbance_state import (
    MAX_COMPONENTS,
    MAX_RULES,
    MAX_SLOTS,
    MAX_VALUE,
    Address3,
    Assignment,
    CostMeter,
    DisturbanceDefinition,
    DisturbanceRecord,
    Expression,
    FieldDefinition,
    InitialState,
    InteractionDefinition,
    Invariant,
    Payload,
    TransportDefinition,
    Values,
    any_negative,
    bounded,
    pack,
    unpack,
    validate_codes,
)
from .integer import checked_work, reduced_ratio

SpatialPopulations = tuple[Payload, ...]
SpatialOutgoing = tuple[SpatialPopulations, ...]
SpatialBundle = tuple[SpatialPopulations, ...]


DECAY_RESIDUES = ("localize", "dissipate")


@dataclass(frozen=True, slots=True)
class DecayDefinition:
    """Completed-link attenuation ratio and the fate of the removed fraction.

    ``localize`` (default) keeps the removed quantity as stationary stock owned
    by the receiving Node, so total signed inventory is preserved. ``dissipate`` is the
    explicit historical option that records it as loss instead.
    """

    retain_numerator: int
    retain_denominator: int
    residue: str = "localize"

    def __post_init__(self) -> None:
        if self.residue not in DECAY_RESIDUES:
            raise ValueError("decay residue must be dissipate or localize")

    @property
    def localizes(self) -> bool:
        return self.residue == "localize"


Heading = tuple[int, int, int]
MAX_HEADINGS = 65536
MAX_HEADING_COMPONENT = 4096
MAX_RAY_SLOTS = 4096

# Ray-event state (Highlights 3.3, 3.19, 3.20 and 5.1): every ray carries the
# number of Links it has walked since its event and the information of that
# event. The fields are hidden variables in this slice: no rule reads them.
RAY_EVENT_STATE = "ray-event-state-v1"
EventShares = tuple[int, int, int, int, int, int]
NO_EVENT_SHARES: EventShares = (0, 0, 0, 0, 0, 0)
# The law of the bit (Highlights 5.4, model owner 2026-09-18; bit-law-v1,
# feature 15 of issue #169): every ray carries one bit, and the bit says what
# the ray is: BIT_THING, the thing itself, or BIT_SHADOW, its shadow, the
# field. There is no ray without a bit and nothing else distinguishes rays
# (Highlights 3.3: there is no light and no matter). The bit is set at birth:
# what is born from content is a thing (a seeded ray, a ray emitted at an
# event, the pieces of a split, the outputs of every meeting, the
# transmissions of an inverse split, a body's token); what is placed as a
# thing's field (the prefilled field of `initial_field`, the departures of a
# spread, a shadow re-released when it comes home) is a shadow. A thing moves
# whole on its line and turns by the pushes it takes; a shadow spreads by the
# table, has no mass, no clock (its phase never advances, whatever its family's
# rate) and no delay, and moves at the causal speed. A shadow meeting a thing
# under a momentum table gives the thing the push the table declares and turns
# back on its own steps carrying its amount and the opposite momentum, -dp, in
# its momentum, walks home to the thing that released it (its owner, by the
# trace the owner leaves at every Node it departs), and is absorbed back and
# re-released; a shadow meeting the thing that released it is home, never a
# push; a thing meeting a thing is the declared tables; a shadow meeting a
# shadow is the coherent sum of the spread; a marked Node returns a shadow
# without a draw and counts nothing of it, and draws for a thing, absorbing it
# on 1 (or passing it where the mark says pass) and returning it on 0. The
# read-only ray property `detector` is this bit. The old values (0 none, 1 a
# draw of 0, 2 a draw of 1; detector-bit-property-v1) are retired with the
# marks' on_bit couplings, the rules' `bit` key and the detector_pass record.
BIT_LAW = "bit-law-v1"
BIT_SHADOW, BIT_THING = 0, 1
# Every thing has a stable identity (the model owner, 2026-09-18): a small
# integer declared on its source (`thing` on a disturbance type or an external
# body, by default the source's place in the declarations), carried by every ray
# of the thing as `owner`, stamped on the shadows the thing's field is made of and
# kept through their spread, return and re-release; two things of one family are
# told apart by it, and a shadow whose owner is at the Node it reaches is home.
MAX_THING_ID = 1 << 20
# A click is an absorption (Highlights 5.4, model owner 2026-09-18;
# detector-absorb-v1, feature 2c): the thing a marked Node realizes ends there.
# On a draw of 1 the arriving thing is absorbed into the mark's exact counter
# for its family, its momentum onto the mark's momentum, booked on the audit as
# absorbed by marks, and nothing of it is delivered to the Node's rays; the
# draw is the mark's efficiency (bit-law-v1). How a mark meets each family on a
# click is its declared coupling (on_click): absorb, the default for every
# family, or pass, the ray continuing on its line.
DETECTOR_ABSORB = "detector-absorb-v1"
# What a mark does with a ray that draws 1, per spatial field: pass it on its
# line or absorb it; CLICK_DEFAULT reads the default, absorb (bit-law-v1).
CLICK_PASS, CLICK_ABSORB, CLICK_DEFAULT = 0, 1, -1
CLICK_COUPLINGS = ("pass", "absorb")
# Layers of event spacetime (Highlights 5.1): a layer is a set of families that
# couple, and a meeting exists only inside a layer. Layers are derived, never
# declared: the connected components of the ray fields over the participants
# of the declared ray interactions, a field no rule selects being its own layer.
RAY_LAYERS = "ray-layers-v1"
Layers = tuple[tuple[int, ...], ...]
# The meeting of rays with N-to-M outputs (Highlights 3.17, 3.26 and 5.1): a rule
# with declared outputs replaces its participants by new event rays at the
# meeting Node, an amount may be split by a declared table indexed by the phase
# difference of two inputs, and every family's stock is exact across the event.
RAY_MEETING = "ray-meeting-conversion-v1"
# The field as the ray's information (Highlights 3.5, 3.14, 3.15 and 3.28).
# Since bit-law-v1 (2026-09-18) a shadow is a ray of the SAME family as its
# thing with the bit 0 (there is no separate field family: `field_of` collapsed
# into family + bit), and a thing does not emit its field: the family's
# `release` ratio is the declared size of a thing's shadow set (the whole
# quanta of amount x n / d per heading and interval of the prefill, the field
# given with the board by `initial_field`), a thing releases nothing on its
# own, and a shadow that comes home leaves again from where the thing now is.
# A shadow has no shadow.
RELEASED_FIELD = "released-field-v1"
# The field given with the board (bit-law-v1, the model owner's amendment of
# 2026-09-18): `initial_field` declares, per field family, either the steady
# state of the declared things computed by the split table's mean field in
# exact integers (`fill`, the intervals of the transient, from every body and
# every seeded record holding the origin family), or a profile of shadows
# (`rays`), booked as `initial`, the thing's presence and not a source.
INITIAL_FIELD_MODES = ("fill", "rays")
# A Node is its six Ports; everything else is a ray (Highlights 5.4, point 22,
# the model owner, 2026-09-18; node-is-ports-v1, feature 17 of issue #169).
# Every store the model kept on a Node or beside the rays is a ray with a
# property: what a Node holds below one quantum is a parked shadow (`Ray.parked`,
# its amount in units of the family's split denominator), what a Node remembers
# of a departure is a parked shadow of amount zero on the heading the thing
# left by (the trace, read by the shadows coming home), what a mark has
# absorbed is a thing resident at it (`DetectorMark.resident`), a source is a
# thing that spends its content by its emission rule (no sourced line), and the
# apparatus are things with declared tables. A thing's momentum stays what it
# is, a property of the thing; there is no register and no counter.
NODE_IS_PORTS = "node-is-ports-v1"
# The trace a thing leaves at the Node it departs (bit-law-v1, point 3; a
# zero-amount parked shadow since node-is-ports-v1): at most this many owners'
# traces per family at one Node, the lowest owner ids dropped beyond it.
# A Port is two lanes (Highlights 5.4 point 25, the model owner's decision of
# 2026-09-18; lanes-v1, feature 18): a Link carries rays both ways, so every Port
# has an in-lane and an out-lane and a Node has twelve lanes. In one interval a
# lane carries at most one real ray and at most one shadow of each owner, so a
# Node's state is bounded and fixed before the run: six Ports x two lanes x (one
# real slot + one shadow slot per owner), plus the parked shadows and the
# traces of point 22 and the things at rest at the Node. The lane is a
# condition on the step, not a queue: a thing steps into an out-lane only if the
# lane is free in that interval; otherwise it keeps its heading, its momentum
# stays accumulated, and it steps at the next Node.
LANES = "lanes-v1"
LANE_IN, LANE_OUT = 0, 1
LANES_PER_PORT = 2
NODE_LANES = 6 * LANES_PER_PORT
# The 0-meets-1 table (bit-law-v1, point 16, the model owner, 2026-09-18): per
# pair of families one rule for what the thing multiplies the shadows' message
# by, declared as `reads`: "content" (a mass family's shadow, dp = sign x amount
# x heading x the thing's content, the acceleration content-independent) or
# "charge" (a charged family's shadow, dp = sign x amount x heading x the
# shadow's source sign x the thing's charge); no default.
PUSH_READS = ("content", "charge")
# Gravity by delay (ray-binding-v1, the lag of a ray's face clocks by a declared
# table) was deleted in the cleanup of 2026-09-18 (Highlights 5.4, points 16, 21
# and 22): gravity is the push of the shadows read times the content of what is
# pushed, every ray moves one Link per interval, and the word register leaves
# the model with the stores it named.
# Binding as a loop (Highlights 3.4 and 3.28, loop-binding-v1): a ray never
# stops, and a bound group is a periodic orbit of the ordinary meeting rule, a
# set of rays that a ring of Nodes brings back to the same place in the same
# state, whose corner meetings, under an ordinary rule with outputs, reproduce
# the rays that entered them. Nothing in the engine names a group: a rule meets
# only the rays that arrived at the Node, the outputs of a rule wait their
# declared delay at their event Node without meeting anything there and leave,
# and a group is read from the record by a reader (tools/ray_viewer/extract.py).
LOOP_BINDING = "loop-binding-v1"
# The clock is the content, the two readings, the decay table and one Link per
# interval (Highlights 5.4 points 11, 16, 18, 19, 20 and 21 and the settled rule
# (i), the model owner's decisions of 2026-09-18; clock-readings-v1, feature 16b):
# a thing of a family that declares `clock` advances its phase by content / K
# steps per interval, K the world's one integer, the remainder kept exactly on
# the thing (`remainder`); a shadow and a family without a clock (light) never
# advance. A shadow carries its owner's id; its owner's charge is its family's
# (a shadow is a ray of its owner's family) and its owner's content is read by
# the owner's id from the family's owner table. The gravity reading of a push is
# sign x amount x heading x the content of what is pushed; the electricity
# reading is sign x amount x heading x (the owner's charge / the owner's
# content) x the charge of what is pushed, accumulated exactly on the pushed
# thing in units of 1 / D (D the least common multiple of the owners' contents,
# `push_remainder`), the whole units into its momentum. A decay is a declared
# condition on the group's state (`decay` on a rule with outputs: the n-th
# meeting under the rule, or the group's content at most c), never a draw. The
# momentum a thing carries accumulates its pushes and sets its direction only:
# at a departure, the first axis whose component reaches the thing's content
# turns the thing to that axis and drops by the content, which the ledger books
# as spent; every ray moves one Link per interval.
CLOCK_READINGS = "clock-readings-v1"
# A thing turns by momentum (Highlights 3.5, 3.14, 3.16 and 5.4 point 21,
# ray-momentum-turn-v3 under clock-readings-v1): a coupling without outputs
# whose momentum_table names a participant family pushes the one participant it
# does not name by the declared reading of every shadow it meets, as the
# external body's table pushes the body, the shadow returned reversed with -dp;
# the push stamps no event and changes no amount, phase or bit. The momentum is
# a property of the thing beside its amount and its phase, the pushes it has
# taken and not yet spent on a step (`step_thing`); the DDA staircase of v2,
# which walked the register as a line, is retired with the settled rule (i).
RAY_MOMENTUM_TURN = "ray-momentum-turn-v3"
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
PORT_HEADINGS: tuple[Heading, ...] = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)
# Every ray is a wave ray (Highlights 3.3 and 5.1, wave-ray-family-v1): the phase
# every ray carries has the width its family declares, `phase_bits`, and every
# phase advance or difference is a mask over 2^phase_bits, never a division. A
# plain family is the special case with rest rate 0. The width has no bound in
# the model; two host limits follow from what else stores a phase: the coherence
# table of a Kerengonen field has one entry per phase step (at most 4096, twelve
# bits), and a ray interaction view or a self-exclusion row stores the phase as
# a bounded value (MAX_VALUE = 2^30 - 1, thirty bits).
WAVE_RAY_FAMILY = "wave-ray-family-v1"
MAX_TABLE_BITS = 12
MAX_STORED_PHASE_BITS = 30
# The Detector mark (Highlights 3.19, 3.20 and 5.4, detector-mark-v1 under
# bit-law-v1): a Node's bit with its table. A marked Node counts the things that
# arrive and catches the k-th when k mod d < n, reading nothing from the ray but
# its bit, and is otherwise an ordinary Node.
DETECTOR_MARK = "detector-mark-v1"
MAX_DETECTORS = 4096
# A draw of 0 returns the arriving ray on its own line (detector-return-v1): the
# same wave ray reversed, unchanged, walking its steps back to its event Node.
DETECTOR_RETURN = "detector-return-v1"
# At its event Node a returned ray performs the inverse split of its own share
# (inverse-split-v1, Highlights 3.20): it transmits its amount, phase and bit to
# the sibling lines of its event. The return modes straight and annul and the
# annulled sink of the first form were deleted in the cleanup of 2026-09-18
# (Highlights 5.4, point 7: things conserve exactly, nothing leaves for a sink).
INVERSE_SPLIT = "inverse-split-v1"
# The external body (Highlights 3.19, external-body-v1): the second declared
# element of a world beside the Detector mark, a Node declared to hold a family
# with an amount of any width, a charge and a momentum. It radiates the field of
# its family on all six headings once per interval, booked as a source; it never
# spreads; whatever arrives is met by its declared coupling, the sink by default;
# only field rays named by its momentum table move it, one Link per axis when a
# whole amount has accumulated.
EXTERNAL_BODY = "external-body-v1"
MAX_EXTERNAL_BODIES = 4096
BODY_SINK = -1
# The Node mixes the six (Highlights 5.4, point 24, the model owner's decision of
# 2026-09-18; node-mixing-v1): a shadow does not choose its next heading alone
# and not in a pair. At every Node, in every interval, the shadows of one group
# (one owner, source sign and polarization) that arrive through the six Ports
# are six complex amplitudes, A_j = sqrt(amount_j) at the phase phi_j on the
# family's phase circle of N steps (a Port with no arrival is 0), and the six
# leaving amplitudes are B_h = (1/3) sum_j A_j - A_h: a third of the coherent
# sum to every Port, less the arrival that came in through that Port, sent
# back (the transmission-line matrix node, S = J/3 - I). The amounts leaving
# are the total amount arriving, shared among the six Ports in proportion to
# |B_h|^2 in whole quanta, the parts below one quantum parked in the Node's
# remainder registers per heading (Highlights 3.17), and each leaving share
# carries the phase of its B_h, the nearest step of N; a zero B_h sends
# nothing. Nothing is declared: the third and the minus are what six equal
# Ports and exact conservation allow, and N is the family's phase width. This
# supersedes the split table of section 3.5 (field-spreading-v1) and the
# pairwise steering of point 17 (phase-spread-v1) for shadows; the Born split
# of two things that meet (section 5.2, `steering_table`) stands, and the
# return of a shadow after a push stays a walk back on the trace, never mixed.
# The arithmetic is the integers of the phase tables: the amplitude is the
# integer square root of amount x MIXING_AMPLITUDE_SCALE^2, the phase factors
# are the cosine and sine tables at PHASE_COSINE_SCALE, the weights |B_h|^2 are
# the squared lengths of 3 B_h (the same ratios), reduced by a common shift to
# MIXING_WEIGHT_BITS bits so that every product stays in 64-bit work, and the
# total in ninths (MIXING_DENOMINATOR, the third squared) is apportioned by the
# largest-remainder rule, ties to the lower Port, so that whole quanta leave
# and the ninths below one quantum are parked: exact conservation, integers
# only, deterministic. A lone arrival of 9 sends 4 back and 1 through each
# other Port; two equal arrivals head on in phase send a/9 back each way and
# 4a/9 through each transverse Port; two in antiphase are each sent back
# whole.
NODE_MIXING = "node-mixing-v1"
# The return is a field (Highlights 5.4, point 3 as amended by the model owner
# on 2026-09-18; feature 16d): a shadow that pushes a thing turns back with the
# opposite sign, the same shadow reversed with its momentum inverted, and from
# then on it is a field like any other: it mixes at every Node in its own group
# (its owner, its flipped sign, its polarization; the two groups of one owner
# never mix), carries its momentum through the mixing in proportion to the
# shares, pushes whatever other thing it meets with the opposite sign and is
# absorbed wherever it reaches its owner. No step counter, no trace, no chase.
RETURN_FIELD = "return-field-v1"
MIXING_DENOMINATOR = 9
MIXING_AMPLITUDE_SCALE = 32
MIXING_WEIGHT_BITS = 28
# The Node owns the sub-quantum remainder (Highlights 3.5 and 3.17, model owner
# 2026-09-17; field-remainder-v1): the parts the mixing gives a heading below
# one quantum are kept at the Node in a remainder register per family, owner,
# source sign and Port, in ninths (MIXING_DENOMINATOR), with the register's
# phase combined with each share's by the coherence rule; when a register
# reaches nine it releases one whole quantum through its heading in that
# interval, more if it reached 9k, as a fresh eventless shadow. Since the
# apportionment is exact, a Node's registers of one family hold whole quanta
# in total, and the ledger counts them as content.
# Since node-is-ports-v1 the store is a parked shadow per owner, sign and Port
# among the Node's rays (`Ray.parked`), in ninths (`parked_unit`), eighteen at
# most per owner and family.
FIELD_REMAINDER = "field-remainder-v1"
REMAINDER_SIGNS = (-1, 0, 1)
REMAINDER_SLOTS = 18
# The parked block per owner (return-field-v1): the eighteen slots of the
# owner's outgoing shares and the eighteen of its returning shares (outbound 0),
# the two groups of one owner never mixing.
PARKED_SLOTS = 2 * REMAINDER_SLOTS
# The dense mode for boards that a field fills (dense-field-v1; performance,
# 2026-09-17): the shadow-only Nodes of a board, those holding nothing but
# shadows of spreading families (arriving, parked, returning or waiting) and
# their traces, are cycled by the host as one vectorized step over integer
# arrays that applies the same spread and remainder rule to every such Node at
# once. A host scheduling choice, not a physical rule: the law is the one
# above, the integers are the same, and a Node holding anything else (a
# Detector mark, an external body, a record, a thing) is cycled by the engine
# as before. The default wherever a world admits it; the runner records the
# identity when on.
DENSE_FIELD = "dense-field-v1"
# Polarization (Highlights 3.26, feature 11; ray-polarization-v1): a family
# property read only at a meeting, exactly as charge is. A ray carries a
# transverse direction modulo a half turn, an integer from 0 below
# 2^polarization_bits (a line, not an arrow: 2^polarization_bits steps per half
# turn), or POLARIZATION_NONE for an unpolarized ray. 0 is the first transverse
# lattice axis of the ray's heading and half the circle the second, which is the
# two-state reading of 3.26; the general angle is the transverse direction 3.26
# allows for the circular case, without the handedness bit. The electron family's
# spin is the same property at one bit. Part of the merge identity; kept by the
# spread (as the axial mean of the taken content), the return, the inverse split
# and a push; carried by a meeting's output from its source input unless the
# output declares it; read by the polarizer, an external body's coupling. The
# engine reads it nowhere else.
RAY_POLARIZATION_PROPERTY = "ray-polarization-v1"
POLARIZATION_NONE = -1
# The polarizer coupling of an external body (Highlights 3.19; feature 11): the
# body's coupling value below BODY_SINK, declared with an angle, a pass Port and
# a table, its rest ending in the body's sink and the shares below one quantum in
# the body's held shares, six per body (sign-major -1, 0, 1, then pass and sink).
BODY_POLARIZER = -2
POLARIZER_SLOTS = 6


@dataclass(frozen=True, slots=True)
class Resident:
    """The thing resident at a mark (node-is-ports-v1, Highlights 5.4 point 22): what
    the mark has absorbed, a thing like every other with its content per family,
    its momentum and the identities it is made of, and no counter. A click is an
    absorption into it: `things` holds the content absorbed from things per
    spatial field, `shadows` the content absorbed from the shadows that came home
    to it (settled rule (iv): a shadow absorbed at its home mark makes no event
    and is counted on this line, never as a click), `momentum` the momentum of
    both, and `owners` the ids of the things absorbed, sorted: the resident is
    the home of their shadows. Both content tuples are empty until the first
    absorption and then hold one entry per spatial field. Its content has left
    the board (point 11): nothing here is on the current line."""

    things: tuple[int, ...] = ()
    shadows: tuple[int, ...] = ()
    momentum: tuple[int, int, int] = (0, 0, 0)
    owners: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        for line in (self.things, self.shadows):
            if type(line) is not tuple or any(type(v) is not int or v < 0 for v in line):
                raise ValueError("a resident thing's content is nonnegative integers per family")
        if len(self.things) != len(self.shadows):
            raise ValueError("a resident thing's things and shadows lines have one entry per family")
        if type(self.momentum) is not tuple or len(self.momentum) != 3:
            raise ValueError("a resident thing's momentum requires three integers")
        for value in self.momentum:
            checked_work(value)
        if (
            type(self.owners) is not tuple
            or any(type(v) is not int or not 0 <= v < MAX_THING_ID for v in self.owners)
            or tuple(sorted(set(self.owners))) != self.owners
        ):
            raise ValueError("a resident thing's owners are distinct thing ids in ascending order")


@dataclass(frozen=True, slots=True)
class DetectorMark:
    """A Node's Detector bit with its setting: bounded Node metadata.

    The setting is the mark's efficiency (bit-law-v1), the declared table "catch
    n things in every d" read by the mark's own count of arrivals, an explicit
    rational with no default; there is no seed (point 14 of the law: there is no
    lottery; the key is rejected since node-is-ports-v1). What the mark does
    with a thing it catches is the declared table of the thing resident at it,
    per spatial field (detector-absorb-v1): `on_click` holds CLICK_PASS,
    CLICK_ABSORB or CLICK_DEFAULT per spatial field index, empty for all
    defaults (absorb), and `click_keys` is 1 when the world file wrote the key.
    A shadow is returned without a draw and never counted, unless the resident
    is its home. `resident` is the thing the mark has absorbed (node-is-ports-v1):
    a click is an absorption into it, and each shadow of an absorbed thing that
    returns is absorbed into it too, on its shadows line (the model owner,
    2026-09-18). Nothing here is a record, stock or a reading of any ray.
    """

    position: Address3
    pass_numerator: int
    pass_denominator: int
    on_click: tuple[int, ...] = ()
    click_keys: int = 0
    resident: Resident = Resident()

    def __post_init__(self) -> None:
        if type(self.position) is not tuple or len(self.position) != 3:
            raise ValueError("a Detector mark requires a three-integer position")
        if any(type(c) is not int or bounded(c) < 0 for c in self.position):
            raise ValueError("a Detector mark position must be nonnegative bounded integers")
        if bounded(self.pass_denominator) < 1:
            raise ValueError("a Detector setting requires a positive denominator")
        if not 0 <= bounded(self.pass_numerator) <= self.pass_denominator:
            raise ValueError("a Detector setting must be a rational from 0 through 1")
        if type(self.on_click) is not tuple or any(
            value not in (CLICK_PASS, CLICK_ABSORB, CLICK_DEFAULT) for value in self.on_click
        ):
            raise ValueError("a Detector mark meets a click by absorb or pass")
        if self.click_keys not in (0, 1):
            raise ValueError("a Detector mark declares its click key as 0 or 1")
        if type(self.resident) is not Resident:
            raise ValueError("a Detector mark holds a resident thing")


@dataclass(frozen=True, slots=True)
class Polarizer:
    """The polarizer declaration of an external body (ray-polarization-v1; Highlights
    3.19, 3.26): the spatial field it polarizes, its angle in steps of that
    family's polarization circle, the heading index of its pass Port, the declared
    table (one entry per step of the circle, each from 0 through the table's
    length D, the pass share in D-ths at the difference angle - ray) and the pass
    share of an unpolarized ray in D-ths. The engine only splits by the table; the
    physics is the declared table.
    """

    family: int
    angle: int
    pass_heading: int
    table: tuple[int, ...]
    unpolarized: int

    def __post_init__(self) -> None:
        if type(self.family) is not int or self.family < 0:
            raise ValueError("a polarizer family must be a spatial field index")
        steps = len(self.table)
        if type(self.table) is not tuple or steps < 1 or steps & (steps - 1):
            raise ValueError("a polarizer table has one entry per step of a power-of-two circle")
        if any(type(entry) is not int or not 0 <= entry <= steps for entry in self.table):
            raise ValueError("a polarizer table entry is an integer from 0 through the table length")
        if type(self.angle) is not int or not 0 <= self.angle < steps:
            raise ValueError("a polarizer angle is an integer step below its polarization circle")
        if type(self.pass_heading) is not int or self.pass_heading < 0:
            raise ValueError("a polarizer pass heading must be a heading index")
        if type(self.unpolarized) is not int or not 0 <= self.unpolarized <= steps:
            raise ValueError("a polarizer unpolarized share is an integer from 0 through the length")

    @property
    def steps(self) -> int:
        return len(self.table)


@dataclass(frozen=True, slots=True)
class ExternalBody:
    """The external body mark of a Node (external-body-v1): bounded Node metadata.

    The declaration (position, family as a spatial field index, amount of any
    width, charge, the coupling as a ray interaction index, BODY_SINK or
    BODY_POLARIZER with its polarizer declaration,
    the released phase, the momentum table as one sign per spatial field), the
    momentum with its three exact accumulators, one exact sink counter per spatial
    field and, for a polarizer, six held shares below one quantum with their phases
    (ray-polarization-v1). The body's identity as a thing, `thing` (bit-law-v1):
    the owner its shadows carry. No rays, no history.
    """

    index: int
    position: Address3
    family: int
    amount: int
    charge: int = 0
    coupling: int = BODY_SINK
    phase: int = 0
    signs: tuple[int, ...] = ()
    momentum: tuple[int, int, int] = (0, 0, 0)
    accumulators: tuple[int, int, int] = (0, 0, 0)
    sink: tuple[int, ...] = ()
    thing: int = 0
    # What the body multiplies the shadows' message by (bit-law-v1, point 16): the
    # index of "content" or "charge" in PUSH_READS, required beside a momentum
    # table; -1 without one.
    reads: int = -1
    # The polarizer (ray-polarization-v1): the declaration, and the held shares that
    # own the shares below one quantum in units of 1/D, D the table's length,
    # sign-major (-1, 0, 1) then pass and sink, with a phase each; () otherwise.
    polarizer: Polarizer | None = None
    held: tuple[int, ...] = ()
    held_phases: tuple[int, ...] = ()
    # The electricity reading's remainder (clock-readings-v1, point 16): per axis
    # in units of 1 / D of the body's family, the sign of the push kept.
    push_remainder: tuple[int, int, int] = (0, 0, 0)

    def __post_init__(self) -> None:
        if type(self.index) is not int or not 0 <= self.index < MAX_EXTERNAL_BODIES:
            raise ValueError("an external body index must stay below the body capacity")
        if type(self.position) is not tuple or len(self.position) != 3:
            raise ValueError("an external body requires a three-integer position")
        if any(type(c) is not int or bounded(c) < 0 for c in self.position):
            raise ValueError("an external body position must be nonnegative bounded integers")
        if type(self.amount) is not int or self.amount < 1:
            raise ValueError("an external body amount must be a positive integer")
        if type(self.family) is not int or self.family < 0:
            raise ValueError("an external body family must be a spatial field index")
        if type(self.coupling) is not int or self.coupling < BODY_POLARIZER:
            raise ValueError("an external body coupling must be a rule index, the sink or a polarizer")
        if (self.coupling == BODY_POLARIZER) != (self.polarizer is not None):
            raise ValueError("an external body polarizer coupling carries its polarizer declaration")
        if self.polarizer is None:
            if self.held or self.held_phases:
                raise ValueError("only a polarizer body holds shares below one quantum")
        else:
            if type(self.polarizer) is not Polarizer:
                raise ValueError("an external body polarizer must be a Polarizer")
            for block in (self.held, self.held_phases):
                if type(block) is not tuple or len(block) != POLARIZER_SLOTS:
                    raise ValueError("a polarizer body holds six shares and six phases")
                if any(type(v) is not int or v < 0 for v in block):
                    raise ValueError("polarizer shares and phases are nonnegative integers")
            if any(v >= self.polarizer.steps for v in self.held):
                raise ValueError("a polarizer share stays below one quantum")
        if type(self.phase) is not int or self.phase < 0:
            raise ValueError("an external body phase must be a nonnegative integer")
        bounded(self.charge)
        for vector in (self.momentum, self.accumulators, self.push_remainder):
            if type(vector) is not tuple or len(vector) != 3:
                raise ValueError("an external body momentum requires three integers")
            for value in vector:
                checked_work(value)
        if any(abs(value) >= self.amount for value in self.accumulators):
            raise ValueError("an external body accumulator stays below its amount")
        if type(self.signs) is not tuple or any(sign not in (-1, 0, 1) for sign in self.signs):
            raise ValueError("an external body momentum table holds signs -1, 0 or 1")
        if any(self.signs) and not 0 <= self.reads < len(PUSH_READS):
            raise ValueError(
                "a momentum table declares what the body multiplies the shadows' message by: "
                "reads content or charge (bit-law-v1, point 16)"
            )
        if not any(self.signs) and self.reads != -1:
            raise ValueError("reads is declared beside a momentum table")
        if type(self.sink) is not tuple or any(type(v) is not int or v < 0 for v in self.sink):
            raise ValueError("an external body sink holds nonnegative counters")
        if type(self.thing) is not int or not 0 <= self.thing < MAX_THING_ID:
            raise ValueError("an external body thing id is an integer below the id bound")


@dataclass(frozen=True, slots=True)
class Ray:
    """One straight-moving share of a ray field: heading index, DDA state and amount.

    The three accumulators travel with the ray, so every unit of one ray follows the
    same lattice line. They are bounded by the heading's Manhattan length.
    """

    heading: int
    accumulators: tuple[int, int, int]
    amount: int
    # Kerengonen fields only: the ray's phase step, advanced on every link, and
    # the ray's own advance per link when nonnegative (-1 uses the field's).
    phase: int = 0
    advance: int = -1
    # Euclidean pace only: how far the ray is toward its next link, below its
    # heading's pace denominator.
    wait: int = 0
    # Generic local coupling residence; independent of the pacing remainder.
    interaction_delay: int = 0
    # Ray-event state, carried and never read by a rule (ray-event-state-v1):
    # Links walked since the ray's event, counted up while outbound and down on
    # the walk back; 1 while the ray travels on its event's heading, 0 once it
    # is reversed on its line; the six-bit mask of the Ports the event sent to
    # and the amount it sent through each (six fixed entries, port order, zero
    # where the mask bit is zero); the bit of the law (bit-law-v1): BIT_THING,
    # the thing itself, or BIT_SHADOW, its shadow, set at birth and read by every
    # step of the Node's law. A shadow has no event, no delay and no clock.
    steps: int = 0
    outbound: int = 1
    event_ports: int = 0
    event_shares: EventShares = NO_EVENT_SHARES
    detector: int = BIT_THING
    # The sign of the source's charge on a field ray (field-spreading-v1;
    # Highlights 3.5, the field is matter's message about itself): -1, 0 or 1,
    # set at the release from the releasing family's charge (a body's from its
    # declared charge), kept through spreading, merging, the return and the
    # inverse split, carried by a meeting's output from the input of its own
    # family; a visible property like the Detector bit, never encoded in the
    # phase, read by no rule of the engine.
    source_sign: int = 0
    # The momentum (clock-readings-v1, Highlights 5.4 point 21 and the settled
    # rule (i)): on a thing, the pushes it has taken and not yet spent on a step,
    # three integers, or None for none; a thing's momentum as the ledger reads it
    # is amount x heading plus this (`ray_momentum_vector`). At a departure the
    # first axis whose component reaches the amount turns the thing to that axis
    # and drops by the amount (`step_thing`). On a shadow walking home, -dp of the
    # push it gave. Extensive, so merging rays adds it as it adds their amounts.
    momentum: tuple[int, int, int] | None = None
    # Polarization (ray-polarization-v1, Highlights 3.26): the transverse direction
    # modulo a half turn in steps of the family's polarization circle
    # (2^polarization_bits steps per half turn), or POLARIZATION_NONE for an
    # unpolarized ray, which every existing world's ray is. Part of the merge
    # identity; read by the polarizer and by a coupling's guard, nowhere else.
    polarization: int = POLARIZATION_NONE
    # The owner (bit-law-v1): the identity of the thing this ray is, or of the
    # thing whose shadow it is; 0 for a thing born of no declared source. Part
    # of the merge identity; a shadow at a Node holding a thing of its owner is
    # home, and a momentum table never pushes a thing with its own shadow.
    owner: int = 0
    # The further owners of a merged thing (lanes-v1, Highlights 5.4 point 25,
    # the model owner's decision of 2026-09-18): two real rays of one family
    # given one lane in one interval are one real ray, whose owners are kept as
    # a set, sorted, without `owner`, so that a returning shadow of either is
    # home at the merged ray. Empty on every other ray. Part of the merge identity.
    owners: tuple[int, ...] = ()
    # The clock's remainder (clock-readings-v1, point 19): a thing of a clock
    # family advances its phase by (remainder + amount) // K steps per interval
    # and keeps the rest here, below K; 0 on a shadow and on a family without a
    # clock. The electricity reading's remainder (point 16), per axis in units
    # of 1 / D (the family's `push_denominator`), the sign of the push kept, so
    # that a push below one quantum accumulates exactly; (0, 0, 0) on a shadow.
    # The passages (point 20): how many meetings under a rule with a `decay`
    # condition this thing has come through without the group breaking, carried
    # by the outputs of the corner table; 0 on a shadow and on a fresh thing.
    remainder: int = 0
    push_remainder: tuple[int, int, int] = (0, 0, 0)
    periods: int = 0
    # The intervals a thing owes for the whole quanta it read (Highlights 5.4
    # point 23, clock-readings-v1): w per whole quantum of push taken, w = n / d
    # the world's `wait_per_quantum`, kept in units of 1 / d and spent one
    # interval at a time, an interval in which the thing neither moves nor steps
    # nor advances its phase; 0 on a shadow, which pays nothing.
    owed: int = 0
    # A parked shadow (node-is-ports-v1, Highlights 5.4 point 22): 1 on a shadow
    # at rest at its Node, never forwarded and outside the slot budget. With an
    # amount it is what the Node holds below one quantum of its owner on the
    # heading it will leave through, the amount in units of the family's split
    # denominator (`parked_unit`), combined with the shares the spread adds and
    # released whole when it reaches one quantum; with amount zero it is the
    # trace, the mark a thing left at the Node it departed, its heading the way
    # the owner went, read by the shadows coming home. Part of the merge identity.
    parked: int = 0


Rays = tuple[Ray, ...]
# One owner's parked shares at a Node, as the spread step reads and writes them
# (field-remainder-v1): eighteen amounts in units of 1/S, sign-major (-1, 0, 1)
# then Port, per owner in the family's owner order, and as many phases.
ParkedBlock = tuple[int, ...]

# Structural non-owning projections used by the ordinary indexed evaluator.
RAY_PROPERTIES = (
    FieldDefinition("amount", 1, "ray amount", False, True),
    FieldDefinition("heading", 3, "integer direction", True, False),
    FieldDefinition("phase", 1, "phase step", False, False),
    FieldDefinition("advance", 1, "phase step per interval", True, False),
    FieldDefinition("delay", 1, "local interval", False, False),
    # wave-ray-family-v1: the ray's family (the index of its spatial field) and
    # that family's charge per quantum, read-only views for a coupling at a meeting.
    FieldDefinition("family", 1, "spatial field index", False, False),
    FieldDefinition("charge", 1, "charge per quantum", True, False),
    # bit-law-v1: the bit the ray carries, 1 a thing and 0 a shadow, a read-only
    # view; a rule meets things alone, so a guard reads 1 here.
    FieldDefinition("detector", 1, "the bit of the law", False, False),
    # ray-polarization-v1: the polarization the ray carries, a step of the family's
    # polarization circle or -1 for none, a read-only view in a guard; a meeting's
    # output declares its own (`polarization` on the output).
    FieldDefinition("polarization", 1, "polarization step", True, False),
)
(
    RAY_AMOUNT,
    RAY_HEADING,
    RAY_PHASE,
    RAY_ADVANCE,
    RAY_DELAY,
    RAY_FAMILY,
    RAY_CHARGE,
    RAY_DETECTOR,
    RAY_POLARIZATION,
) = range(9)
# A ray interaction may assign heading, phase and delay; the rest is read-only.
RAY_WRITABLE = frozenset((RAY_HEADING, RAY_PHASE, RAY_DELAY))
RAY_VIEW_COMPONENTS = sum(field.components for field in RAY_PROPERTIES)
# The view a meeting reads when none of its layer's rules names polarization: the
# view of detector-bit-property-v1, so that a world whose rules do not read the
# property is charged what it was charged before feature 11 (byte-identical).
RAY_VIEW_COMPONENTS_UNPOLARIZED = RAY_VIEW_COMPONENTS - 1
CHARGE_INVARIANT = "charge"


def charge_invariant(participants: int) -> Invariant:
    """The charge readout, charge x amount summed over the participants, declared as an
    invariant of a ray interaction: exact before and after, checked like every
    declared invariant (wave-ray-family-v1)."""
    if type(participants) is not int or not 1 <= participants <= 6:
        raise ValueError("the charge invariant covers one to six participants")
    total: Expression | None = None
    for side in range(participants):
        term = Expression(
            "mul",
            (
                Expression("field", field=RAY_CHARGE, side=side),
                Expression("field", field=RAY_AMOUNT, side=side),
            ),
        )
        total = term if total is None else Expression("add", (total, term))
    assert total is not None
    return Invariant(CHARGE_INVARIANT, total)


def ray_participant_definitions(
    fields: tuple[FieldDefinition, ...], definitions: tuple[SpatialFieldDefinition, ...]
) -> tuple[DisturbanceDefinition, ...]:
    """Describe non-owning ray views; no additional physical records are created."""
    defaults = tuple(pack((0,) * field.components) for field in RAY_PROPERTIES)
    return tuple(
        DisturbanceDefinition(
            fields[definition.field].name,
            tuple(range(len(RAY_PROPERTIES))) if definition.rays else (),
            defaults,
            TransportDefinition("hold"),
        )
        for definition in definitions
    )


def validate_ray_participants(
    definitions: tuple[SpatialFieldDefinition, ...],
    fields: tuple[FieldDefinition, ...],
    rules: tuple[InteractionDefinition, ...],
) -> frozenset[int]:
    """Enforce the same native participant limits for parsed and direct callers."""
    if type(rules) is not tuple or len(rules) > MAX_RULES:
        raise ValueError("ray interaction rules exceed their fixed capacity")
    selected: set[int] = set()
    for rule in rules:
        if not 2 <= len(rule.participants) <= 6 or rule.k or rule.output_types is not None:
            raise ValueError("ray interactions require two to six indexed roles without k or conversion")
        for role in rule.participants:
            if not role or any(
                type(index) is not int or not 0 <= index < len(definitions) for index in role
            ):
                raise ValueError("ray participant role refers to an unavailable spatial field")
            selected.update(role)
        if rule.outputs:
            # A meeting with outputs (ray-meeting-conversion-v1): one to six new event
            # rays of ray fields, assigned from the frozen inputs, in the same layer.
            if not 1 <= len(rule.outputs) <= 6 or any(
                type(kind) is not int or not 0 <= kind < len(definitions) for kind in rule.outputs
            ):
                raise ValueError("ray meeting outputs require one to six ray fields")
            selected.update(rule.outputs)
            if any(
                not 0 <= assignment.side < len(rule.outputs)
                or not 0 <= assignment.field < len(RAY_PROPERTIES)
                for assignment in rule.assignments
            ):
                raise ValueError("ray meeting assignments address its declared outputs")
            if len(rule.output_polarization) not in (0, len(rule.outputs)) or any(
                by_input not in (0, 1)
                or (by_input == 0 and not 0 <= value < len(rule.participants))
                or (by_input == 1 and value < POLARIZATION_NONE)
                for by_input, value in rule.output_polarization
            ):
                raise ValueError(
                    "ray meeting output polarization names an input or a value, one per output"
                )
            if any(
                not 0 <= split.first < len(rule.outputs)
                or not 0 <= split.second < len(rule.outputs)
                or split.first == split.second
                or split.field != 0
                or split.phase_field != 2
                or not 1 <= len(split.table) <= MAX_PHASE_STEPS
                or any(
                    type(weight) is not int or not 0 <= weight <= len(split.table)
                    for weight in split.table
                )
                or any(not 0 <= index < len(rule.participants) for index in split.between)
                or split.between[0] == split.between[1]
                or not -1 <= split.source < len(rule.participants)
                or any(len(split.table) != definitions[kind].phase_modulus for kind in rule.outputs)
                for split in rule.splits
            ):
                raise ValueError("ray meeting table split requires two outputs and the phase modulus")
        elif rule.splits:
            raise ValueError("a table split requires a meeting with outputs")
        elif any(assignment.field not in RAY_WRITABLE for assignment in rule.assignments):
            raise ValueError("ray interaction amount, advance, family and charge are read-only")
        if rule.momentum_table:
            # ray-momentum-turn-v1: a table that names a participant family is a
            # coupling of free rays, assigning nothing, whose one unnamed role is
            # the ray the named field rays push. A table on a rule that assigns was
            # the push of a bound group (bound-group-motion-v1), removed on
            # 2026-09-17 by loop-binding-v1.
            if rule.reads not in PUSH_READS:
                raise ValueError(
                    "a momentum table declares what the thing multiplies the shadows' message "
                    "by: reads content or charge (bit-law-v1, point 16)"
                )
            participants = {kind for role in rule.participants for kind in role}
            if (
                rule.outputs
                or rule.assignments
                or len(rule.momentum_table) != len(definitions)
                or any(sign not in (-1, 0, 1) for sign in rule.momentum_table)
                or not any(rule.momentum_table)
            ):
                raise ValueError(
                    "a momentum table is declared by a coupling of free rays without outputs or assignments"
                )
            names_participant = any(
                sign and kind in participants for kind, sign in enumerate(rule.momentum_table)
            )
            if not names_participant or turn_receiver(rule) in (None, -1):
                raise ValueError(
                    "a momentum table on a coupling of free rays names every role but the one ray it turns"
                )
            selected.update(kind for kind, sign in enumerate(rule.momentum_table) if sign)
        elif rule.reads:
            raise ValueError("reads is declared beside a momentum table")
    for layer in ray_layers(definitions, rules):
        # The indexed selector's capacity bounds one meeting, and a meeting exists
        # only inside a layer: fields of different layers never share it.
        if selected.intersection(layer) and (
            sum(definitions[index].ray_slots for index in layer) > MAX_SLOTS
        ):
            raise ValueError("ray interactions require at most 32 selected ray slots in one layer")
    for index in selected:
        definition = definitions[index]
        field = fields[definition.field]
        if (
            not definition.rays
            or field.signed
            or not field.conserved
            or any(unpack(definition.baseline))
            or definition.euclidean
            or definition.pace_numerator != definition.pace_denominator
            or definition.self_exclusion
            or definition.decay is not None
            or any(sum(abs(component) for component in heading) != 1 for heading in definition.headings)
        ):
            raise ValueError("ray coupling requires positive unit-axial unpaced ray fields")
        if definition.phase_bits > MAX_STORED_PHASE_BITS:
            raise ValueError(
                "ray interactions view the phase as a stored value: they require phase_bits at most 30"
            )
    return frozenset(selected)


def ray_layers(
    definitions: tuple[SpatialFieldDefinition, ...],
    rules: tuple[InteractionDefinition, ...],
) -> Layers:
    """The layers over the ray fields (ray-layers-v1): the connected components of the
    fields that the roles of one rule can select, and one layer for every ray field
    that no rule selects. Each layer lists its spatial-field indices in field order
    and the layers are in the order of their first field. Bounded by the number of
    spatial fields and the fixed rule capacity; nothing is declared."""
    if type(rules) is not tuple or len(rules) > MAX_RULES:
        raise ValueError("ray interaction rules exceed their fixed capacity")
    parent = list(range(len(definitions)))

    def root(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    for rule in rules:
        # The fields a rule's roles select, the fields of its outputs and the
        # families its momentum table names (ray-momentum-turn-v1) couple.
        selected = (
            {kind for role in rule.participants for kind in role}
            | set(rule.outputs)
            | {kind for kind, sign in enumerate(rule.momentum_table) if sign}
        )
        if any(type(kind) is not int or not 0 <= kind < len(definitions) for kind in selected):
            raise ValueError("ray participant role refers to an unavailable spatial field")
        kinds = sorted(selected)
        for kind in kinds[1:]:
            parent[root(kind)] = root(kinds[0])
    members: dict[int, list[int]] = {}
    for index, definition in enumerate(definitions):
        if definition.rays:
            members.setdefault(root(index), []).append(index)
    return tuple(tuple(layer) for layer in sorted(members.values()))


def ray_layer_names(
    fields: tuple[FieldDefinition, ...],
    definitions: tuple[SpatialFieldDefinition, ...],
    rules: tuple[InteractionDefinition, ...],
) -> tuple[tuple[str, ...], ...]:
    """The derived layers as family names for the run record, sorted within each layer
    and between layers."""
    return tuple(
        sorted(
            tuple(sorted(fields[definitions[index].field].name for index in layer))
            for layer in ray_layers(definitions, rules)
        )
    )


def validate_ray_coupling(initial: InitialState) -> None:
    if not initial.ray_interactions:
        return
    if (
        initial.schema_version != 1
        or initial.link_ticks != 1
        or initial.node_execution
        or initial.spatial_computation_delay
        or initial.field_phase_first
        or initial.arrival_port_blind
        or initial.delay_direction is not None
        or initial.field_rules
        or initial.spatial_interactions
    ):
        raise ValueError("ray interactions require the default fixed H=1 spatial clock")
    selected = validate_ray_participants(
        initial.spatial_fields, initial.fields, initial.ray_interactions
    )
    if any(
        rule.field == initial.spatial_fields[index].field
        for index in selected
        for rule in initial.spatial_couplings
    ):
        raise ValueError("ray interactions do not support coupled responses or absorption")


def validate_released_fields(
    definitions: tuple[SpatialFieldDefinition, ...], fields: tuple[FieldDefinition, ...]
) -> None:
    """The admission of a family with a shadow set (released-field-v1 under
    bit-law-v1): a positive, conserved, unpaced unit-axial ray family on the
    links metric with the six Port headings, whose `release` is a rational at
    most 1, the size of its things' shadow sets. A family without a release
    declares the ratio 0 / 1."""
    for definition in definitions:
        numerator, denominator = definition.release_numerator, definition.release_denominator
        if not numerator:
            if denominator != 1:
                raise ValueError("a family without a release declares the ratio 0 / 1")
            continue
        if not 1 <= bounded(numerator) <= bounded(denominator):
            raise ValueError("release must be a rational from 1 / d through 1")
        field = fields[definition.field]
        if (
            not definition.rays
            or field.signed
            or not field.conserved
            or any(unpack(definition.baseline))
            or definition.euclidean
            or definition.pace_numerator != definition.pace_denominator
            or definition.self_exclusion
            or definition.decay is not None
            or any(sum(abs(c) for c in heading) != 1 for heading in definition.headings)
        ):
            raise ValueError("a released field requires positive unit-axial unpaced ray fields")
        if any(heading not in definition.headings for heading in PORT_HEADINGS):
            raise ValueError("a released field requires the six Port headings")


def validate_released_field_admission(initial: InitialState) -> None:
    """A world with a shadow set runs under the shared Detector admission."""
    if not any(definition.release_numerator for definition in initial.spatial_fields):
        return
    if (
        initial.schema_version != 1
        or initial.link_ticks != 1
        or initial.node_execution
        or initial.spatial_computation_delay
        or initial.field_phase_first
        or initial.arrival_port_blind
        or initial.delay_direction is not None
        or initial.field_rules
        or initial.spatial_interactions
    ):
        raise ValueError("a released field requires the default fixed H=1 spatial clock")
    validate_released_fields(initial.spatial_fields, initial.fields)
    involved = {
        definition.field for definition in initial.spatial_fields if definition.release_numerator
    }
    if any(rule.field in involved for rule in initial.spatial_couplings):
        raise ValueError("a released field does not support coupled responses or absorption")


def release_amount(amount: int, definition: SpatialFieldDefinition) -> int:
    """The amount of one released ray: the whole quanta of amount x n / d. The
    fraction the floor leaves is not released: the field is a description booked
    as a source, so nothing owned is lost (Highlights 3.17)."""
    return checked_work(amount * definition.release_numerator) // definition.release_denominator


def charge_sign(charge: int) -> int:
    """The sign a field ray carries for its source's charge: -1, 0 or 1."""
    return -1 if charge < 0 else (1 if charge > 0 else 0)


def _released(
    amount: int,
    phase: int,
    definition: SpatialFieldDefinition,
    skip: Heading | None,
    sign: int = 0,
    owner: int = 0,
) -> Rays:
    """Shadows of one owner, one per Port heading but `skip`, fresh (steps 0)."""
    return tuple(
        Ray(
            definition.headings.index(heading),
            (0, 0, 0),
            amount,
            phase=phase,
            detector=BIT_SHADOW,
            source_sign=sign,
            owner=owner,
        )
        for heading in PORT_HEADINGS
        if heading != skip
    )


def motion_step(
    momentum: tuple[int, int, int], accumulators: tuple[int, int, int], content: int
) -> tuple[int, tuple[int, int, int]]:
    """One interval of motion over a content (external-body-v1): each axis
    accumulator adds the momentum component, and the owner steps one Link through
    the Port of the first axis (x before y before z) whose accumulator has reached
    a whole content, subtracting the content; at most one Link per interval, never
    faster than a ray. Returns the Port, or -1 when it stays, and the new
    accumulators. An accumulator only grows past the content while the owner waits
    its turn on another axis; it is capped so the accumulator stays bounded metadata."""
    advanced = [a + m for a, m in zip(accumulators, momentum, strict=True)]
    port = -1
    for axis in range(3):
        if advanced[axis] >= content:
            advanced[axis] -= content
            port = 2 * axis
            break
        if advanced[axis] <= -content:
            advanced[axis] += content
            port = 2 * axis + 1
            break
    if any(abs(value) > 2 * content for value in advanced):
        raise ValueError("a momentum exceeds its content: faster than a ray")
    return port, (advanced[0], advanced[1], advanced[2])


def release_stock(stock: int, definition: SpatialFieldDefinition, owner: int = 0) -> Rays:
    """The shadows of one interval of the prefill from a thing's stock (bit-law-v1,
    `initial_field`): one per Port heading, all six, the whole quanta of stock x
    n / d, phase 0 (a record has no phase of its own), the sign of the family's
    charge and the owner's id. A thing releases nothing during a run; this is the
    size X of its shadow set per interval of the fill."""
    amount = release_amount(stock, definition)
    return (
        _released(amount, 0, definition, None, charge_sign(definition.charge), owner)
        if amount > 0
        else ()
    )


def family_owners(initial: InitialState, index: int) -> tuple[int, ...]:
    """The things whose shadows a family carries (bit-law-v1): the ids of the
    disturbance types that hold the family's stock, of the external bodies of
    the family and of the owners of its declared profile, sorted."""
    definition = initial.spatial_fields[index]
    owners = {kind.thing for kind in initial.disturbances if definition.field in kind.fields}
    owners |= {body.thing for body in initial.external_bodies if body.family == index}
    entry = initial.initial_field.get(index)
    if entry is not None:
        owners |= {ray.owner for ray in entry.rays}
    return tuple(sorted(owners))


def shadow_family_names(initial: InitialState) -> list[dict[str, object]]:
    """The families with a shadow set for the run record (bit-law-v1): each with
    its release ratio, the width N of the phase circle its shadows mix on
    (node-mixing-v1) and its owners, in field order."""
    return [
        {
            "field": initial.fields[definition.field].name,
            "release": [definition.release_numerator, definition.release_denominator],
            "phase_width": definition.phase_modulus,
            "owners": list(definition.owners),
        }
        for definition in initial.spatial_fields
        if definition.spread
    ]


# The spread of shadows (node-mixing-v1). Every rule here reads the content that
# arrived at one Node and the family's phase width; nothing reads another Node.


@dataclass(frozen=True, slots=True)
class FieldSpread:
    """The record of one spread for the Node to publish (field-spreading-v1): plain
    bounded integers, as the Node state contract requires. The spatial field, the
    amount taken off the Node, the amount that arrived per heading (six entries by
    the heading's Port index), the departure per Port, the remainder quanta placed
    per Port, the combined phase and the reduced coherence of the arrivals."""

    field: int
    amount: int
    arrived: tuple[int, ...]
    amounts: tuple[int, ...]
    # The quanta the remainder registers released per Port, the whole quanta the
    # registers gained net of those releases, and the registers with their phases
    # after the step (field-remainder-v1).
    released: tuple[int, ...]
    stored: int
    registers: tuple[int, ...]
    register_phases: tuple[int, ...]
    phase: int
    coherence: tuple[int, int]
    # The distinct source signs of the content taken, in order (field-spreading-v1).
    signs: tuple[int, ...] = ()
    # The registers' momenta after the step, three per slot (return-field-v1).
    register_momenta: tuple[int, ...] = ()


@dataclass(frozen=True, slots=True)
class ShadowHome:
    """The record of one shadow that came home (bit-law-v1, point 3 of the law and
    the amendment's re-release): plain bounded integers. The spatial field, the
    amount, the owner, the Port index of the heading the shadow walked in on, the
    momentum it delivered (what it carried in flight, return-field-v1: the -dp of
    the pushes it gave shared through the mixing, zero for a share that gave
    none), whom it was absorbed back into (`to`:
    0 a thing ray, 1 a record, 2 an external body) and the Port index it left
    again through (the heading it arrived from, reversed)."""

    field: int
    amount: int
    owner: int
    port: int
    momentum: tuple[int, int, int]
    to: int
    out_port: int
    # 1 when the momentum left the identity the ledger measures (a record without
    # a momentum field), booked on the returned line; 0 when the thing took it.
    outside: int = 0


def steering_table(modulus: int) -> tuple[int, ...]:
    """The steering table of a phase width (Highlights 3.3 and 5.4, point 17:
    computed once from the width, never declared), the Born split of two things
    of one family that meet (section 5.2, a split indexed by the phase
    difference): the share that continues at a difference of d steps is
    cos^2(pi d / N) in N-ths, rounded to the nearest whole, N the modulus, in
    the fixed-point integer arithmetic of the phase tables (N (1 + cos) / 2 with
    cos at nine decimals); the reference table [8, 7, 4, 1, 0, 1, 4, 7] at eight
    steps, (1,) for a family without a phase width. Since node-mixing-v1
    (Highlights 5.4, point 24) it steers no shadow: a shadow spreads by the
    Node's mixing."""
    if type(modulus) is not int or not 1 <= modulus <= MAX_PHASE_STEPS:
        raise ValueError("a steering table is written for a phase width of at most 4096 steps")
    entries = []
    for difference in range(modulus):
        reduced = min(difference, modulus - difference)
        angle = checked_work(2 * _PI_FIXED * reduced) // modulus
        flip = 4 * reduced > modulus
        cosine = _fixed_cosine(_PI_FIXED - angle if flip else angle)
        if flip:
            cosine = -cosine
        entries.append((checked_work(modulus * (_FIXED + cosine)) + _FIXED) // (2 * _FIXED))
    return tuple(entries)


def validate_spread_fields(
    definitions: tuple[SpatialFieldDefinition, ...], fields: tuple[FieldDefinition, ...]
) -> None:
    """The admission of a family whose shadows spread (node-mixing-v1, every
    family with a shadow set): the geometry of a released field (a positive,
    conserved, unpaced unit-axial ray field on the links metric with the six
    Port headings, zero baseline, no decay, no self-exclusion) and a phase width
    of at most twelve bits, since the mixing sums the amplitudes over the
    cosine and sine tables of its modulus."""
    for definition in definitions:
        if not definition.spread:
            continue
        field = fields[definition.field]
        if (
            not definition.rays
            or field.signed
            or not field.conserved
            or any(unpack(definition.baseline))
            or definition.euclidean
            or definition.pace_numerator != definition.pace_denominator
            or definition.self_exclusion
            or definition.decay is not None
            or any(sum(abs(c) for c in heading) != 1 for heading in definition.headings)
        ):
            raise ValueError(
                "a family with a shadow set requires a positive unit-axial unpaced ray field: "
                "its shadows spread by the Node's mixing (node-mixing-v1)"
            )
        if any(heading not in definition.headings for heading in PORT_HEADINGS):
            raise ValueError("a family with a shadow set requires the six Port headings")
        if definition.phase_bits > MAX_TABLE_BITS:
            raise ValueError(
                "a family with a shadow set has a phase width of at most twelve bits: the "
                "Node mixes its shadows over the cosine and sine tables of its modulus"
            )


def validate_spread_admission(initial: InitialState) -> None:
    """A world with a family whose shadows spread runs under the shared Detector
    admission."""
    if not any(definition.spread for definition in initial.spatial_fields):
        return
    if (
        initial.schema_version != 1
        or initial.link_ticks != 1
        or initial.node_execution
        or initial.spatial_computation_delay
        or initial.field_phase_first
        or initial.arrival_port_blind
        or initial.delay_direction is not None
        or initial.field_rules
        or initial.spatial_interactions
    ):
        raise ValueError("a family with a shadow set requires the default fixed H=1 spatial clock")
    validate_spread_fields(initial.spatial_fields, initial.fields)
    spreading = {definition.field for definition in initial.spatial_fields if definition.spread}
    if any(rule.field in spreading for rule in initial.spatial_couplings):
        raise ValueError("a family with a shadow set does not support coupled responses or absorption")


def validate_dense_field_admission(initial: InitialState) -> None:
    """What the dense mode's prototype supports (dense-field-v1): a spreading
    family on a board of ray fields only, no local conservation audit (a dense
    Node publishes no per-Node events for it to read) and no polarization (the
    dense region carries unpolarized content). Since bit-law-v1 the region is
    the board's shadow layer: it holds shadows alone, and a coupling between a
    thing and a shadow fires at the thing's Node, the engine's."""
    if not initial.dense_field:
        return
    spreading = {index for index, definition in enumerate(initial.spatial_fields) if definition.spread}
    if not spreading:
        raise ValueError("dense_field requires a spreading family (field-spreading-v1)")
    if any(not definition.rays for definition in initial.spatial_fields):
        raise ValueError(
            "dense_field requires ray transport on every spatial field: the dense region "
            "carries rays only"
        )
    if initial.conservation is not None:
        raise ValueError(
            "dense_field does not support the local conservation audit (`conservation`): a "
            "dense Node publishes no per-Node events for the audit to read; the world ledger "
            "of ray-event-audit-v1 is kept"
        )
    if polarization_declared(initial):
        raise ValueError(
            "dense_field does not support polarization (ray-polarization-v1): the prototype "
            "carries unpolarized field content only"
        )


def dense_field_admissible(initial: InitialState) -> bool:
    """Whether the dense mode can be the board's shadow layer (bit-law-v1, point
    13): a spreading family on a board of ray fields only, no local conservation
    audit and no polarization; the default wherever it holds."""
    return (
        any(definition.spread for definition in initial.spatial_fields)
        and all(definition.rays for definition in initial.spatial_fields)
        and initial.conservation is None
        and not polarization_declared(initial)
    )


def remainder_slot(sign: int, port: int, rank: int = 0, flow: int = 0) -> int:
    """The slot of one owner (its rank among the family's owners), flow (0 the
    outgoing shares, 1 the returning, return-field-v1), source sign and Port in
    a family's parked block: thirty-six per owner, owner-major (bit-law-v1)."""
    if sign not in REMAINDER_SIGNS or type(port) is not int or not 0 <= port < 6:
        raise ValueError("a parked share is named by a source sign and a Port")
    if type(rank) is not int or rank < 0 or flow not in (0, 1):
        raise ValueError("a parked share is named by an owner's rank and its flow")
    return rank * PARKED_SLOTS + flow * REMAINDER_SLOTS + (sign + 1) * 6 + port


def remainder_block_size(definition: SpatialFieldDefinition) -> int:
    """The parked shares of one spreading family at a Node, as the spread step reads
    them: thirty-six per owner of the family (eighteen outgoing, eighteen
    returning, return-field-v1), thirty-six for a family with no declared owner
    (bit-law-v1)."""
    return PARKED_SLOTS * max(1, len(definition.owners)) if definition.spread else 0


def remainder_stock(block: tuple[int, ...], total: int) -> int:
    """The whole quanta a Node's parked shares of one family hold: their sum over
    the parked unit, exact because the mixing parks a multiple of it (the total
    in ninths is apportioned exactly) and a release takes a multiple of it."""
    held = 0
    for value in block:
        held = checked_work(held + value)
    if held % total:
        raise ValueError("a Node's parked shadows hold whole quanta in total")
    return held // total


# The parked shadow (node-is-ports-v1): the store below one quantum and the trace
# as rays at rest among the Node's rays. Nothing here reads another Node.


def parked_unit(definition: SpatialFieldDefinition) -> int:
    """The unit of a parked shadow's amount, one for every family whose shadows
    spread: ninths, MIXING_DENOMINATOR (node-mixing-v1; a parked amount is in
    ninths of a quantum, below nine), 1 for a family without a shadow set (whose
    parked shadows are traces of amount zero)."""
    return MIXING_DENOMINATOR if definition.spread else 1


def parked_shadow(
    owner: int,
    port: int,
    definition: SpatialFieldDefinition,
    amount: int,
    phase: int = 0,
    sign: int = 0,
    momentum: tuple[int, int, int] | None = None,
    outbound: int = 1,
) -> Ray:
    """A shadow parked at a Node on the heading of `port`: the share of `owner`
    below one quantum (in units of the family's split denominator), with the
    share's phase, sign, flow (outbound 1 outgoing, 0 returning, return-field-v1)
    and the momentum it holds in flight."""
    if not 1 <= amount < parked_unit(definition):
        raise ValueError("a parked shadow's amount stays below one quantum in its unit")
    if momentum is not None and not any(momentum):
        momentum = None
    return Ray(
        definition.headings.index(PORT_HEADINGS[port]),
        (0, 0, 0),
        amount,
        phase=phase,
        outbound=outbound,
        detector=BIT_SHADOW,
        source_sign=sign,
        momentum=momentum,
        owner=owner,
        parked=1,
    )


def parked_shares(
    rays: Rays, definition: SpatialFieldDefinition
) -> tuple[ParkedBlock, ParkedBlock, ParkedBlock]:
    """The parked shares of one family at a Node as the spread step reads them: the
    block of thirty-six amounts per owner (owner-major by the family's owner
    order, flow-major then sign-major then Port), their phases and their
    momenta (three per slot), from the Node's parked shadows."""
    size = remainder_block_size(definition)
    held, phases, momenta = [0] * size, [0] * size, [0] * (3 * size)
    if not size:
        return (), (), ()
    owners = definition.owners or (0,)
    for ray in rays:
        if not ray.parked:
            continue
        if ray.owner not in owners:
            raise ValueError("a parked shadow's owner is one of its family's declared owners")
        port = PORT_HEADINGS.index(definition.headings[ray.heading])
        slot = remainder_slot(ray.source_sign, port, owners.index(ray.owner), 0 if ray.outbound else 1)
        if held[slot]:
            raise ValueError("a Node parks one shadow per owner, flow, sign and Port of a family")
        held[slot], phases[slot] = ray.amount, ray.phase
        if ray.momentum is not None:
            momenta[3 * slot : 3 * slot + 3] = ray.momentum
    return tuple(held), tuple(phases), tuple(momenta)


def park_shares(
    block: ParkedBlock, phases: ParkedBlock, momenta: ParkedBlock, definition: SpatialFieldDefinition
) -> Rays:
    """The parked shadows of one family at a Node from the block the spread step
    wrote: one per nonzero slot, on the slot's Port heading with the slot's phase,
    sign, flow, momentum and owner, in slot order."""
    owners = definition.owners or (0,)
    result = []
    for slot, amount in enumerate(block):
        if not amount:
            continue
        rank, rest = divmod(slot, PARKED_SLOTS)
        flow, rest = divmod(rest, REMAINDER_SLOTS)
        sign, port = divmod(rest, 6)
        momentum = tuple(momenta[3 * slot : 3 * slot + 3]) if momenta else (0, 0, 0)
        result.append(
            parked_shadow(
                owners[rank],
                port,
                definition,
                amount,
                phases[slot],
                sign - 1,
                (momentum[0], momentum[1], momentum[2]),
                0 if flow else 1,
            )
        )
    return tuple(result)


def parked_stock(rays: Rays, definition: SpatialFieldDefinition) -> int:
    """The whole quanta the parked shadows of one family at a Node hold: the sum of
    their amounts over the family's unit, whole exactly (field-remainder-v1)."""
    return remainder_stock(tuple(ray.amount for ray in rays if ray.parked), parked_unit(definition))


def parked_momentum(rays: Rays) -> tuple[int, int, int]:
    """The momentum the parked shadows of a Node hold in flight (return-field-v1)."""
    result = [0, 0, 0]
    for ray in rays:
        if ray.parked and ray.momentum is not None:
            for axis in range(3):
                result[axis] = checked_work(result[axis] + ray.momentum[axis])
    return result[0], result[1], result[2]


def apportion_momentum(
    momentum: tuple[int, int, int], weights: tuple[int, ...], total: int
) -> list[tuple[int, int, int]]:
    """A momentum shared over slots in proportion to their weights (ninths of the
    shares, summing to `total`), exact per axis: the floors, then the units left
    to the largest remainders (ties to the lower slot); a negative component is
    shared as its magnitude and negated (return-field-v1)."""
    shares = [[0, 0, 0] for _ in weights]
    if total <= 0 or not any(momentum):
        return [(0, 0, 0) for _ in weights]
    for axis in range(3):
        value = momentum[axis]
        if not value:
            continue
        magnitude = abs(value)
        quotients, remainders, given = [], [], 0
        for weight in weights:
            quotient, remainder = divmod(checked_work(magnitude * weight), total)
            quotients.append(quotient)
            remainders.append(remainder)
            given = checked_work(given + quotient)
        left = magnitude - given
        for slot in sorted(range(len(weights)), key=lambda s: (-remainders[s], s))[:left]:
            quotients[slot] += 1
        for slot, quotient in enumerate(quotients):
            shares[slot][axis] = quotient if value > 0 else -quotient
    return [(share[0], share[1], share[2]) for share in shares]


def momentum_part(momentum: tuple[int, int, int], part: int, whole: int) -> tuple[int, int, int]:
    """The momentum a part of a parked share takes with it: the share's momentum x
    part / whole per axis, rounded toward zero, the rest staying on the share;
    the whole momentum when the part is the whole share."""
    if part >= whole:
        return momentum
    result = [0, 0, 0]
    for axis in range(3):
        scaled = abs(momentum[axis]) * part // whole
        result[axis] = scaled if momentum[axis] >= 0 else -scaled
    return result[0], result[1], result[2]


def spread_tables(
    definition: SpatialFieldDefinition,
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    """The cosine and sine tables the spread combines phases with: the family's
    declared coherence table, or the table of its phase modulus (at most twelve
    bits); None for a family without a phase width, whose one phase is 0."""
    modulus = definition.phase_modulus
    if modulus < 2:
        return None
    if definition.coherent:
        return definition.cosine_table, definition.sine_table
    return phase_cosines(modulus), phase_sines(modulus)


def spread_phase(rays: Rays, definition: SpatialFieldDefinition) -> int:
    """The one phase of the content a Node spreads: the phase step nearest the
    direction of the coherent sum over every taken ray (the coherence rule of
    Highlights 3.20; a cancelled sum gives step 0), 0 for a family without a
    phase width."""
    tables = spread_tables(definition)
    if tables is None:
        return 0
    terms = tuple((abs(ray.amount), ray.phase) for ray in rays)
    return _phase_of_sum(terms, tables[0], tables[1], definition.phase_modulus)


def spread_coherence(rays: Rays, definition: SpatialFieldDefinition) -> tuple[int, int]:
    """The reduced coherence of the content a Node spreads, over the same table."""
    tables = spread_tables(definition)
    if tables is None or not rays:
        return (1, 1)
    numerator, denominator = _coherence(rays, tables[0], definition.phase_mask)
    return reduced_ratio(numerator, denominator)


def polarization_tables(
    definition: SpatialFieldDefinition,
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    """The cosine and sine tables of the family's polarization circle
    (ray-polarization-v1): a polarization is a line, so its circle of
    2^polarization_bits steps per half turn is the circle of the doubled angle,
    on which lines add as vectors; None for a circle of one step or wider than
    the table limit (twelve bits)."""
    modulus = definition.polarization_modulus
    if modulus < 2 or modulus > MAX_PHASE_STEPS:
        return None
    return phase_cosines(modulus), phase_sines(modulus)


def combined_polarization(terms: tuple[tuple[int, int], ...], definition: SpatialFieldDefinition) -> int:
    """The one polarization of combined content (ray-polarization-v1): the step of
    the family's polarization circle nearest the direction of the sum of amount x
    e^(i 2 pi p / 2^bits) over the polarized terms (the axial mean, the doubled
    angle of each line), the rule by which the spread combines what it takes as
    it combines the phase; unpolarized terms add no direction. None when no term
    is polarized, when the sum cancels (two equal crossed lines are unpolarized
    content) or when the circle has one step."""
    tables = polarization_tables(definition)
    polarized = tuple((abs(amount), step) for amount, step in terms if step != POLARIZATION_NONE)
    if tables is None or not polarized:
        return POLARIZATION_NONE
    modulus = definition.polarization_modulus
    mask = phase_mask(modulus)
    x = y = 0
    for amount, step in polarized:
        x = checked_work(x + amount * tables[0][step & mask])
        y = checked_work(y + amount * tables[1][step & mask])
    if not x and not y:
        return POLARIZATION_NONE
    return _phase_of_sum(polarized, tables[0], tables[1], modulus)


def spread_polarization(rays: Rays, definition: SpatialFieldDefinition) -> int:
    """The polarization every departure of a spread carries: the combined
    polarization of the taken content, as its phase is the phase of the
    coherent sum and its bit the highest (ray-polarization-v1)."""
    return combined_polarization(tuple((ray.amount, ray.polarization) for ray in rays), definition)


MIXING_OPPOSITE = (1, 0, 3, 2, 5, 4)


def mixing_amplitude(amount: int) -> int:
    """The amplitude of an arriving amount (node-mixing-v1): sqrt(amount) in units
    of 1 / MIXING_AMPLITUDE_SCALE, the integer square root."""
    if type(amount) is not int or amount < 0:
        raise ValueError("an amplitude is the square root of a nonnegative amount")
    return integer_sqrt(checked_work(amount * MIXING_AMPLITUDE_SCALE * MIXING_AMPLITUDE_SCALE))


def mixing_tables(definition: SpatialFieldDefinition) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """The cosine and sine tables the mixing sums amplitudes over: the family's
    (`spread_tables`), or the one-step circle (cos 1, sin 0 at the table's
    scale) of a family without a phase width."""
    tables = spread_tables(definition)
    if tables is None:
        return (PHASE_COSINE_SCALE,), (0,)
    return tables


def node_mixing(
    arrivals: tuple[tuple[int, int], ...],
    cosines: tuple[int, ...],
    sines: tuple[int, ...],
) -> tuple[tuple[int, int, int], ...]:
    """The Node's mixing of one group (node-mixing-v1; Highlights 5.4, point 24):
    `arrivals` are six (amount, phase) by travel heading in Port order (the
    content that arrived walking that heading came in through the opposite
    Port; amount 0 is no arrival), the tables are the family's phase circle of
    N steps. Returns, per leaving heading in Port order, the whole quanta that
    leave, the ninths below one quantum parked in that heading's register and
    the phase of the leaving amplitude. The leaving amplitude of heading h is
    B_h = (1/3) sum_j A_j - A_j(h), A_j(h) the arrival that came in through
    Port h (the one walking the opposite heading); computed as 3 B_h, the same
    ratios and the same phase. The total in ninths is shared in proportion to
    |B_h|^2 by the largest-remainder rule, ties to the lower Port, so the
    quanta leaving plus the ninths parked equal what arrived, exactly."""
    if len(arrivals) != 6:
        raise ValueError("the mixing takes one arrival per Port")
    modulus = len(cosines)
    mask = phase_mask(modulus) if modulus > 1 else 0
    total = 0
    xs, ys = [0] * 6, [0] * 6
    for port, (amount, phase) in enumerate(arrivals):
        if type(amount) is not int or amount < 0:
            raise ValueError("an arrival is a nonnegative amount at a phase")
        if not amount:
            continue
        total = checked_work(total + amount)
        amplitude = mixing_amplitude(amount)
        xs[port] = checked_work(amplitude * cosines[phase & mask])
        ys[port] = checked_work(amplitude * sines[phase & mask])
    if not total:
        return tuple((0, 0, 0) for _ in range(6))
    sum_x, sum_y = 0, 0
    for port in range(6):
        sum_x = checked_work(sum_x + xs[port])
        sum_y = checked_work(sum_y + ys[port])
    weights, phases = [0] * 6, [0] * 6
    for heading in range(6):
        entry = MIXING_OPPOSITE[heading]
        cx = checked_work(sum_x - 3 * xs[entry])
        cy = checked_work(sum_y - 3 * ys[entry])
        if abs(cx) >= 1 << 31 or abs(cy) >= 1 << 31:
            raise OverflowError("64-bit intermediate range exceeded")
        weights[heading] = cx * cx + cy * cy
        if weights[heading]:
            best, best_projection = 0, None
            for step in range(modulus):
                projection = checked_work(cx * cosines[step] + cy * sines[step])
                if best_projection is None or projection > best_projection:
                    best, best_projection = step, projection
            phases[heading] = best
    weight_total = sum(weights)
    shift = max(0, weight_total.bit_length() - MIXING_WEIGHT_BITS)
    reduced = [weight >> shift for weight in weights]
    reduced_total = sum(reduced)
    units = checked_work(total * MIXING_DENOMINATOR)
    quotas, remainders = [0] * 6, [0] * 6
    for heading in range(6):
        product = checked_work(units * reduced[heading])
        quotas[heading], remainders[heading] = divmod(product, reduced_total)
    short = units - sum(quotas)
    for heading in sorted(range(6), key=lambda h: (-remainders[h], h))[:short]:
        quotas[heading] += 1
    return tuple(
        (quotas[heading] // MIXING_DENOMINATOR, quotas[heading] % MIXING_DENOMINATOR, phases[heading])
        for heading in range(6)
    )


def spread_content(
    index: int,
    rays: Rays,
    definition: SpatialFieldDefinition,
    registers: tuple[int, ...] = (),
    register_phases: tuple[int, ...] = (),
    register_momenta: tuple[int, ...] = (),
) -> tuple[Rays, FieldSpread, tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    """The spread of one family's shadows at a Node (node-mixing-v1,
    field-remainder-v1, bit-law-v1, return-field-v1): the departures, one fresh
    shadow per owner, Port, source sign, flow, phase and polarization with
    content, the record, and the Node's registers, their phases and their
    momenta after the step. The rays are the shadows that arrived (at least one
    Link walked), outgoing or returning; a thing moves whole and is never here.
    The shares of one group (one owner, source sign, flow and polarization;
    shadows of different owners, of differing polarization, or an owner's
    outgoing and returning shares do not mix) are the Node's mixing
    (`node_mixing`, Highlights 5.4, point 24): per travel heading the shadows of
    the group that arrived on it are one amplitude, their amount at the step
    nearest their coherent sum; the six amplitudes mix, the whole quanta leave
    through each heading at the phase of its leaving amplitude and the ninths
    below one quantum go to the group's register of that flow, sign and Port
    (thirty-six registers per owner, owner-major by the owner's rank among the
    family's declared owners), the register's phase combined with the share's by
    the coherence rule; a register that reaches nine releases the whole quanta
    it holds through its Port, with its phase, and keeps the rest. The momentum
    the group's shadows carry in flight (a returning share's -dp, point 3)
    goes with the shares, over the twelve outputs of the mixing in proportion
    to their ninths (`apportion_momentum`, exact), and a release takes the
    register's momentum in proportion to what it releases (`momentum_part`).
    Each departure carries the Port's heading, accumulators (0, 0, 0), its
    phase, no rate, wait or delay, steps 0, its flow, no event, its sign,
    its owner, its momentum and its group's polarization (a register's release
    the Node's combined polarization). The total is exact: what arrived equals
    what leaves plus the whole quanta the registers gained, and the momentum
    that arrived equals what leaves plus what the registers gained."""
    total = MIXING_DENOMINATOR
    size = remainder_block_size(definition)
    held = list(registers) if registers else [0] * size
    held_phases = list(register_phases) if register_phases else [0] * size
    held_momenta = list(register_momenta) if register_momenta else [0] * (3 * size)
    if len(held) != size or len(held_phases) != size or len(held_momenta) != 3 * size:
        raise ValueError("a remainder block holds thirty-six registers, phases and momenta per owner")
    before = sum(held)
    arrived = [0] * 6
    groups: dict[tuple[int, int, int, int], dict[int, list[tuple[int, int]]]] = {}
    carried: dict[tuple[int, int, int, int], list[int]] = {}
    for ray in rays:
        if ray.steps < 1 or ray.amount <= 0 or ray.parked:
            raise ValueError("a spread takes the content that arrived at the Node")
        if ray.detector != BIT_SHADOW:
            raise ValueError("a spread takes shadows: a thing moves whole on its line (bit-law-v1)")
        heading = definition.headings[ray.heading]
        if heading not in PORT_HEADINGS:
            raise ValueError("a spread requires content on a Port heading")
        port = PORT_HEADINGS.index(heading)
        arrived[port] = checked_work(arrived[port] + ray.amount)
        key = (ray.owner, ray.source_sign, ray.polarization, 0 if ray.outbound else 1)
        groups.setdefault(key, {}).setdefault(port, []).append((ray.amount, ray.phase))
        if ray.momentum is not None:
            momentum = carried.setdefault(key, [0, 0, 0])
            for axis in range(3):
                momentum[axis] = checked_work(momentum[axis] + ray.momentum[axis])
    phase = spread_phase(rays, definition)
    tables = spread_tables(definition)
    cosines, sines = mixing_tables(definition)
    modulus = definition.phase_modulus
    amounts, released = [0] * 6, [0] * 6
    departing: dict[tuple[int, int, int, int, int, int], list[int]] = {}
    ranks: dict[int, int] = {}
    for (owner, sign, polarization, flow), by_port in sorted(groups.items()):
        if owner not in ranks:
            if definition.owners:
                if owner not in definition.owners:
                    raise ValueError(
                        "a shadow's owner is one of its family's declared owners (bit-law-v1)"
                    )
                ranks[owner] = definition.owners.index(owner)
            elif owner == 0:
                ranks[owner] = 0
            else:
                raise ValueError("a shadow's owner is one of its family's declared owners (bit-law-v1)")
        rank = ranks[owner]
        arrivals = []
        group_amount = 0
        for port in range(6):
            terms = tuple(by_port.get(port, ()))
            if not terms:
                arrivals.append((0, 0))
                continue
            amount = 0
            for term_amount, _ in terms:
                amount = checked_work(amount + term_amount)
            group_amount = checked_work(group_amount + amount)
            port_phase = 0 if tables is None else _phase_of_sum(terms, tables[0], tables[1], modulus)
            arrivals.append((amount, port_phase))
        mixed = node_mixing(tuple(arrivals), cosines, sines)
        group_momentum = carried.get((owner, sign, polarization, flow), [0, 0, 0])
        weights = tuple(checked_work(whole * total) for whole, _, _ in mixed) + tuple(
            fraction for _, fraction, _ in mixed
        )
        shares = apportion_momentum(
            (group_momentum[0], group_momentum[1], group_momentum[2]),
            weights,
            checked_work(group_amount * total),
        )
        for target, (whole, fraction, leaving_phase) in enumerate(mixed):
            if whole:
                amounts[target] = checked_work(amounts[target] + whole)
                sent = (owner, target, sign, leaving_phase, polarization, flow)
                entry = departing.setdefault(sent, [0, 0, 0, 0])
                entry[0] = checked_work(entry[0] + whole)
                for axis in range(3):
                    entry[1 + axis] = checked_work(entry[1 + axis] + shares[target][axis])
            if fraction:
                slot = remainder_slot(sign, target, rank, flow)
                if tables is None:
                    held_phases[slot] = 0
                elif held[slot]:
                    held_phases[slot] = _phase_of_sum(
                        ((held[slot], held_phases[slot]), (fraction, leaving_phase)),
                        tables[0],
                        tables[1],
                        modulus,
                    )
                else:
                    held_phases[slot] = leaving_phase
                held[slot] = checked_work(held[slot] + fraction)
                for axis in range(3):
                    held_momenta[3 * slot + axis] = checked_work(
                        held_momenta[3 * slot + axis] + shares[6 + target][axis]
                    )
    owner_of_rank = definition.owners or (0,)
    release_polarization = spread_polarization(rays, definition)
    for rank in range(size // PARKED_SLOTS):
        for flow in (0, 1):
            for sign in REMAINDER_SIGNS:
                for target in range(6):
                    slot = remainder_slot(sign, target, rank, flow)
                    whole, rest = divmod(held[slot], total)
                    if not whole:
                        continue
                    slot_momentum = (
                        held_momenta[3 * slot],
                        held_momenta[3 * slot + 1],
                        held_momenta[3 * slot + 2],
                    )
                    taken = momentum_part(slot_momentum, checked_work(whole * total), held[slot])
                    held[slot] = rest
                    for axis in range(3):
                        held_momenta[3 * slot + axis] = slot_momentum[axis] - taken[axis]
                    amounts[target] = checked_work(amounts[target] + whole)
                    released[target] = checked_work(released[target] + whole)
                    sent = (
                        owner_of_rank[rank],
                        target,
                        sign,
                        held_phases[slot],
                        release_polarization,
                        flow,
                    )
                    entry = departing.setdefault(sent, [0, 0, 0, 0])
                    entry[0] = checked_work(entry[0] + whole)
                    for axis in range(3):
                        entry[1 + axis] = checked_work(entry[1 + axis] + taken[axis])
                    if not rest:
                        held_phases[slot] = 0
    departures = tuple(
        Ray(
            definition.headings.index(PORT_HEADINGS[port]),
            (0, 0, 0),
            bounded(entry[0]),
            phase=departure_phase,
            outbound=0 if flow else 1,
            detector=BIT_SHADOW,
            source_sign=sign,
            momentum=(entry[1], entry[2], entry[3]) if any(entry[1:]) else None,
            polarization=departure_polarization,
            owner=owner,
        )
        for (owner, port, sign, departure_phase, departure_polarization, flow), entry in sorted(
            departing.items()
        )
        if entry[0]
    )
    stored, fraction = divmod(sum(held) - before, total)
    if fraction:
        raise ValueError("a spread stores whole quanta in the Node's registers in total")
    record = FieldSpread(
        index,
        bounded(sum(arrived)),
        tuple(arrived),
        tuple(amounts),
        tuple(released),
        stored,
        tuple(held),
        tuple(held_phases),
        phase,
        spread_coherence(rays, definition),
        tuple(sorted({ray.source_sign for ray in rays})),
        tuple(held_momenta),
    )
    return departures, record, tuple(held), tuple(held_phases), tuple(held_momenta)


def mixing_field_names(
    fields: tuple[FieldDefinition, ...], definitions: tuple[SpatialFieldDefinition, ...]
) -> list[dict[str, object]]:
    """The families whose shadows spread, for the run record: each with the width
    N of its phase circle, the mixing's one input, in field order."""
    return [
        {"field": fields[definition.field].name, "phase_width": definition.phase_modulus}
        for definition in definitions
        if definition.spread
    ]


@dataclass(frozen=True, slots=True)
class SpatialFieldDefinition:
    field: int
    baseline: Payload
    axis_weights: tuple[int, int, int] = (1, 1, 1)
    octant_weights: tuple[int, ...] = (1, 1, 1, 1, 1, 1, 1, 1)
    decay: DecayDefinition | None = None
    transport: str = "outward"
    # Ray transport only: the fixed heading sequence, rays emitted per source per
    # tick, and the resident ray capacity of one Node.
    headings: tuple[Heading, ...] = ()
    rays_per_tick: int = 0
    ray_slots: int = 0
    # Ray transport only: an emitting record that departs subtracts its own rays
    # from the flux it samples at the next Node, using only its own bookkeeping.
    self_exclusion: bool = False
    # Kerengonen (phased rays): the coherence table, one entry per phase step of
    # one turn (2^phase_bits entries, a power of two up to 4096; 0 is no table),
    # and the clock (clock-readings-v1, Highlights 5.4 point 19): K, the world's
    # content per phase step per interval, for a family whose things have a
    # clock (a thing advances its phase by content / K steps per interval, the
    # remainder kept on the thing), 0 for light and for the plain field, whose
    # rays carry the phase of what emitted them. No family declares a rate.
    phase_steps: int = 0
    clock: int = 0
    # Kerengonen only: how an absorber takes a ray. "share" takes the coherent
    # share of its amount; "threshold" takes the whole ray when that share reaches
    # one half and leaves it otherwise. Neither draws: the only draw in the model
    # is at a Node whose Detector bit is set.
    capture: str = "share"
    # Declared carrier-vector association for read-only ray inventory accounting.
    momentum_field: int | None = None
    # Ray transport only: "links" moves every ray one link per tick; "euclidean"
    # paces each heading so that every ray covers the same Euclidean distance
    # per tick, the slowest lattice direction setting the speed.
    metric: str = "links"
    # Ray transport only: the fastest heading hops pace_numerator links every
    # pace_denominator ticks (1 / 1 is link speed); a slower matter wave is
    # never faster than the signals that chase it.
    pace_numerator: int = 1
    pace_denominator: int = 1
    # Scalar response readout: last-hop Port channels or complete resident ray headings.
    flux_projection: str = "ports"
    # Every ray is a wave ray (wave-ray-family-v1): the width of the phase every
    # ray of this family carries, the modulus being 2^phase_bits; 0 (one phase
    # value, the plain field of existing worlds) unless declared, and log2 of
    # phase_steps when a coherence table is declared without a width.
    phase_bits: int = 0
    # The family's charge per quantum, a bounded signed integer read by couplings
    # at a meeting and summed as charge x amount by the charge readout.
    charge: int = 0
    # The shadow set (released-field-v1 under bit-law-v1): the release ratio, the
    # share of a thing's amount each of its shadows carries, 0 / 1 for a family
    # whose things have no shadows; and the owners, the ids of the things whose
    # shadows the family carries (the types holding its stock, the bodies of the
    # family, the owners of its declared profile), sorted, filled in by the
    # world's initial state when left empty; the parked shadows of a
    # spread are per owner in this order.
    release_numerator: int = 0
    release_denominator: int = 1
    owners: tuple[int, ...] = ()
    # The owners' contents and charges (clock-readings-v1, point 18): per owner
    # in the order of `owners`, the stock each was declared with (a type's
    # default of the family's field, a body's amount, 1 for an owner known only
    # from a profile) and its whole charge (the charge per quantum, the family's
    # or the body's declared, times that stock), what a shadow carries as its
    # owner's content and charge, read by the owner's id; and D, the least
    # common multiple of the owners' contents over the world's families, the
    # unit of the electricity reading's remainder.
    owner_contents: tuple[int, ...] = ()
    owner_charges: tuple[int, ...] = ()
    push_denominator: int = 1
    # The wait per whole quantum read (Highlights 5.4 point 23, clock-readings-v1):
    # w = wait_numerator / wait_denominator intervals, the world's one constant
    # (`wait_per_quantum`, 1 by default), on every ray family.
    wait_numerator: int = 1
    wait_denominator: int = 1
    # The family's shadows spread by the Node's mixing (node-mixing-v1): true for
    # every family with a shadow set (a release, or a field given with the
    # board), set by the world's initial state, never declared; a family without
    # shadows has nothing to spread. Nothing else is declared of the spread: the
    # mixing's one input is the family's phase width.
    spread: bool = False
    # Polarization (ray-polarization-v1): the width of the family's polarization
    # circle, 2^polarization_bits steps per half turn; -1 when the world does not
    # declare it, which reads as the family's phase width (`polarization_modulus`).
    polarization_bits: int = -1
    cosine_table: tuple[int, ...] = dataclass_field(default=(), init=False, repr=False)
    sine_table: tuple[int, ...] = dataclass_field(default=(), init=False, repr=False)
    pace_table: tuple[tuple[int, int], ...] = dataclass_field(default=(), init=False, repr=False)

    def __post_init__(self) -> None:
        if self.flux_projection not in ("ports", "carried_heading"):
            raise ValueError("flux_projection must be ports or carried_heading")
        if self.flux_projection == "carried_heading" and not self.rays:
            raise ValueError("carried_heading flux_projection requires ray transport")
        if self.rays:
            object.__setattr__(self, "pace_table", prepare_heading_paces(self))
        if type(self.phase_bits) is not int or self.phase_bits < 0:
            raise ValueError("phase_bits must be a nonnegative integer")
        if self.phase_steps:
            if (
                type(self.phase_steps) is not int
                or not 2 <= self.phase_steps <= MAX_PHASE_STEPS
                or self.phase_steps & (self.phase_steps - 1)
            ):
                raise ValueError("kerengonen phase_steps must be a power of two between 2 and 4096")
            bits = self.phase_steps.bit_length() - 1
            if self.phase_bits == 0:
                object.__setattr__(self, "phase_bits", bits)
            elif self.phase_bits != bits:
                raise ValueError("kerengonen phase_steps must equal 2 to the power phase_bits")
            # Immutable law preparation precedes every physical event.
            object.__setattr__(self, "cosine_table", phase_cosines(self.phase_steps))
            object.__setattr__(self, "sine_table", phase_sines(self.phase_steps))
        bounded(self.charge)
        if type(self.spread) is not bool:
            raise ValueError("a family's shadows spread by the Node's mixing, never by a declared table")
        if self.spread and not self.rays:
            raise ValueError("a shadow set requires ray transport")
        if (
            type(self.owners) is not tuple
            or any(type(v) is not int or not 0 <= v < MAX_THING_ID for v in self.owners)
            or tuple(sorted(set(self.owners))) != self.owners
        ):
            raise ValueError("a family's owners are distinct thing ids in ascending order")
        if type(self.owner_contents) is not tuple or (
            self.owner_contents
            and (
                len(self.owner_contents) != len(self.owners)
                or any(type(v) is not int or v < 1 for v in self.owner_contents)
            )
        ):
            raise ValueError("a family's owner contents are one positive integer per owner")
        if type(self.owner_charges) is not tuple or (
            self.owner_charges
            and (
                len(self.owner_charges) != len(self.owners)
                or any(type(v) is not int for v in self.owner_charges)
            )
        ):
            raise ValueError("a family's owner charges are one integer per owner")
        if type(self.push_denominator) is not int or self.push_denominator < 1:
            raise ValueError("a family's push denominator is a positive integer")
        if (
            type(self.wait_numerator) is not int
            or type(self.wait_denominator) is not int
            or self.wait_numerator < 0
            or self.wait_denominator < 1
        ):
            raise ValueError("the wait per quantum is a rational n / d, n at least 0 and d at least 1")
        if type(self.clock) is not int or self.clock < 0:
            raise ValueError("a family's clock is K, a nonnegative integer (clock-readings-v1)")
        if self.clock and not self.phase_bits:
            raise ValueError("a clock requires a phase width: phase_bits at least 1 (clock-readings-v1)")
        if type(self.polarization_bits) is not int or self.polarization_bits < -1:
            raise ValueError("polarization_bits must be a nonnegative integer")
        if self.polarization_bits >= 0 and not self.rays:
            raise ValueError("polarization_bits requires ray transport")

    @property
    def rays(self) -> bool:
        return self.transport == "ray"

    @property
    def polarization_declared(self) -> bool:
        """The world wrote the family's polarization width (ray-polarization-v1)."""
        return self.polarization_bits >= 0

    @property
    def polarization_modulus(self) -> int:
        """The steps of the family's polarization circle per half turn:
        2^polarization_bits, or 2^phase_bits when the width is not declared."""
        return 1 << (self.phase_bits if self.polarization_bits < 0 else self.polarization_bits)

    @property
    def coherent(self) -> bool:
        """The family declares the Kerengonen coherence table."""
        return self.phase_steps > 0

    @property
    def phase_modulus(self) -> int:
        """The phase turns over at 2^phase_bits; 1 for a family without a declared width."""
        return 1 << self.phase_bits

    @property
    def phase_mask(self) -> int:
        return (1 << self.phase_bits) - 1

    @property
    def euclidean(self) -> bool:
        return self.metric == "euclidean"

    @property
    def kerengonen(self) -> bool:
        """The family declares a phase rule: a coherence table or a clock."""
        return self.phase_steps > 0 or self.clock > 0

    def owner_content(self, owner: int) -> int:
        """The content of one owner of the family (clock-readings-v1, point 18):
        what its shadows carry as their owner's content, read by the owner's id
        from the owner table; a shadow of an owner the table does not hold
        carries no content and is refused by the electricity reading."""
        if owner in self.owners and self.owner_contents:
            return self.owner_contents[self.owners.index(owner)]
        return 0

    def owner_charge(self, owner: int) -> int:
        """The charge of one owner of the family (clock-readings-v1, point 18): its
        whole charge, what its shadows carry as their owner's charge, read by the
        owner's id from the owner table; over the owner's content it is the
        family's charge per quantum for a thing of a type."""
        if owner in self.owners and self.owner_charges:
            return self.owner_charges[self.owners.index(owner)]
        return 0


@dataclass(frozen=True, slots=True)
class FieldGroupDefinition:
    name: str
    fields: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class FieldAssignment:
    field: int
    expression: Expression
    port: int = -1


@dataclass(frozen=True, slots=True)
class NodeFieldRuleDefinition:
    name: str
    assignments: tuple[FieldAssignment, ...]
    invariants: tuple[Invariant, ...]
    when: Expression | None = None
    k: int = 0
    commit_when: Expression | None = None


@dataclass(frozen=True, slots=True)
class FieldRuleGuard:
    rule_index: int
    delta: Values
    outgoing: tuple[Values, ...]


@dataclass(frozen=True, slots=True)
class SpatialInteractionDefinition:
    name: str
    type_index: int
    assignments: tuple[Assignment, ...]
    invariants: tuple[Invariant, ...]
    when: Expression | None = None
    types: tuple[int, ...] = ()
    k: int = 0
    participants: tuple[tuple[int, ...], ...] = ()
    commit_when: Expression | None = None


@dataclass(frozen=True, slots=True)
class FieldInteractionGuard:
    rule_index: int
    slot: int
    before: Values
    after: Values
    delta: Values
    slots: tuple[int, ...] = ()
    participant_before: tuple[Values, ...] = ()
    participant_after: tuple[Values, ...] = ()


@dataclass(frozen=True, slots=True)
class EmissionDefinition:
    type_index: int
    spatial_field: int
    amount: Expression
    denominator: int = 1
    budget: Payload | None = None
    types: tuple[int, ...] = ()
    # Ray fields only: pay the emitted amount from the record's own field of the
    # same name (clipped to its stock) instead of declaring an external source,
    # and subtract the emitted rays' amount x heading from an owned vector field.
    funded: bool = False
    recoil_field: int | None = None
    # Kerengonen fields only: the phase step every emitted ray starts with, or,
    # when carried, the phase of what the record last absorbed plus one advance.
    phase: int = 0
    phase_carried: bool = False
    # Kerengonen fields only: the emitted rays' own advance per link, an owned-field
    # expression over advance_denominator, taken modulo the phase steps.
    advance: Expression | None = None
    advance_denominator: int = 1
    # Kerengonen fields only: re-emit the whole amount along the mirror image of the
    # heading last absorbed: for each output component, the source component and
    # its sign (a mirror across an axis plane or a diagonal plane).
    mirror: tuple[tuple[int, int], tuple[int, int], tuple[int, int]] | None = None
    # Dissolution (funded ray fields only): emit nothing for dissolve_after cycles,
    # then the record's initial stock over dissolve_over cycles, never more than
    # is left. Zero dissolve_over means no dissolution.
    dissolve_after: int = 0
    dissolve_over: int = 0
    # Ray fields only: emit every ray on this one heading of the sequence instead
    # of sweeping the sequence (a directed emitter). None sweeps.
    heading: int | None = None
    # Ray fields only (ray-polarization-v1): the polarization every emitted ray
    # carries, a step of the family's polarization circle, or -1 for none (a lamp
    # declares the polarization of what it emits; unpolarized by default).
    polarization: int = POLARIZATION_NONE


@dataclass(frozen=True, slots=True)
class SpatialCouplingDefinition:
    name: str
    type_index: int
    field: int
    mode: str
    expression: Expression
    denominator: int = 1
    axis_order: tuple[int, int, int] = (0, 1, 2)
    budget: Payload | None = None
    types: tuple[int, ...] = ()
    # Absorb mode only: the owned vector field that receives amount x heading.
    momentum_field: int | None = None
    # Absorb mode only: the share of each arriving ray that is absorbed, as a
    # nonnegative owned-field expression over fraction_denominator; the rest of
    # the ray is forwarded. None absorbs whole rays.
    fraction: Expression | None = None
    fraction_denominator: int = 1


@dataclass(frozen=True, slots=True)
class SpatialCouplingResult:
    records: tuple[DisturbanceRecord | None, ...]
    reaction: Values
    cost: int
    guards: tuple[FieldInteractionGuard, ...] = ()
    interaction_ticks: int = 0


@dataclass(frozen=True, slots=True)
class SpatialSeed:
    position: Address3
    spatial_field: int
    populations: SpatialPopulations


@dataclass(frozen=True, slots=True)
class SpatialState:
    """Eight owned populations, eight allocation phases, and six delivered samples.

    All entries use the ordinary positive payload coding, including phases.
    Delivered samples project already owned inventory and are never extra stock.
    """

    populations: SpatialPopulations
    allocation_phases: SpatialPopulations
    delivered: tuple[Payload, ...]
    received_mask: int = 0

    def validate(self, components: int) -> None:
        if type(components) is not int or not 1 <= components <= MAX_COMPONENTS:
            raise ValueError("spatial fields require one to thirty-two components")
        if type(self.received_mask) is not int or not 0 <= self.received_mask < 64:
            raise ValueError("received mask requires six bounded port bits")
        for values, size in (
            (self.populations, 8),
            (self.allocation_phases, 8),
            (self.delivered, 6),
        ):
            if len(values) != size:
                raise ValueError("spatial state requires eight octants and six delivered channels")
            for value in values:
                if len(value) != components:
                    raise ValueError("spatial state component count differs from the field")
                validate_codes(value)
        if any(any_negative(payload) for payload in self.allocation_phases):
            raise ValueError("spatial allocation phases must be nonnegative")


@dataclass(slots=True)
class SpatialNodeState:
    """Mutable spatial-field state owned by one Node."""

    states: tuple[SpatialState, ...]
    last_cost: int = 0
    received_count: int = 0
    reaction_phases: Values = ()
    sample_values: Values = ()
    sample_fluxes: Values = ()
    last_begin_tick: int = -1
    received_decay_cost: int = 0
    sample_ports: tuple[Values, ...] = ()
    sample_received_masks: tuple[int, ...] = ()
    # Frozen six delivered channels per spatial field, for arrival-port-blind samples.
    sample_delivered: tuple[tuple[Payload, ...], ...] = ()
    # Computation-field stock present at this node before its last forwarding.
    load: int = 0
    # The same stock split by the six travel channels it was delivered through.
    load_channels: tuple[int, ...] = (0, 0, 0, 0, 0, 0)
    # Later arrivals have destination ownership but cannot enter a frozen cycle.
    shared_pending: int = 0
    # Stationary stock per spatial field, deposited by localizing decay. It is
    # owned inventory at a known Node: never transported, decayed or sampled.
    localized: tuple[Payload, ...] = ()
    # Resident rays per spatial field (empty for non-ray fields). They arrived on
    # the previous link and leave on the next cycle along their own lines.
    rays: tuple[Rays, ...] = ()
    incoming: tuple[SpatialState, ...] = ()
    incoming_count: int = 0
    incoming_decay_cost: int = 0
    # The Detector mark of this Node when its bit is set, and the count of the
    # things that arrived at it, read against the mark's table (bit-law-v1, point
    # 14: no seed, no draw).
    detector: DetectorMark | None = None
    arrivals: int = 0
    # The external body this Node holds, whole, when one is declared or has
    # stepped here (external-body-v1); None at every other Node. What the Node
    # holds below one quantum and what it remembers of a departure are parked
    # shadows among `rays` (node-is-ports-v1): a Node is its six Ports.
    body: ExternalBody | None = None


@dataclass(frozen=True, slots=True)
class SpatialPlan:
    states: tuple[SpatialState, ...]
    outgoing: tuple[SpatialBundle, ...]
    emission_records: tuple[DisturbanceRecord | None, ...]
    source_delta: Values
    cost: int
    rule_delta: Values = ()
    interaction_ticks: int = 0
    field_guards: tuple[FieldRuleGuard, ...] = ()
    # Outgoing rays per port, each entry holding one tuple per spatial field.
    rays: tuple[tuple[Rays, ...], ...] = ()
    # Per port, per field, eight carried allocation phases; empty under node-owned phases.
    outgoing_phases: tuple[SpatialBundle, ...] = ()
    # Funded emission minus absorption per field: stock that moved between a
    # record and its field, booked as a reaction, never as a source.
    transfer_delta: Values = ()
    # Rays that stay resident this cycle (Euclidean pace), one tuple per field.
    kept_rays: tuple[Rays, ...] = ()
    # The inverse splits of this cycle, one per returned ray at its event Node
    # (inverse-split-v1).
    inverse_splits: tuple[InverseSplit, ...] = ()
    # The external body after this cycle and the Port it steps through, or -1
    # when it stays (external-body-v1); None at a Node without a body.
    body: ExternalBody | None = None
    body_port: int = -1
    # The spreads of this cycle, one per spreading family whose content arrived
    # (field-spreading-v1), and the shadows that came home here (bit-law-v1).
    spreads: tuple[FieldSpread, ...] = ()
    homecomings: tuple[ShadowHome, ...] = ()
    # What came home this cycle, per field (bit-law-v1): the amounts of the
    # shadows absorbed back, and on the momentum field the momentum delivered
    # to an owner the identity does not measure (a record without a recoil
    # field); the re-release is booked on `source_delta`.
    returned_delta: Values = ()
    # The parked shadows after this cycle, the shares below one quantum and the
    # traces (node-is-ports-v1), are among `kept_rays`.
    # The pushes of free rays this cycle, one per field ray met by a coupling's
    # momentum table (ray-momentum-turn-v1).
    ray_pushes: tuple[RayPush, ...] = ()
    # The momentum the things spent on their steps this cycle, per field
    # (clock-readings-v1, the settled rule (i)): on the momentum field, the
    # content x heading each step dropped from a thing's momentum, booked spent.
    spent_delta: Values = ()
    # The phase steps of the things this cycle (clock-readings-v1, point 11): the
    # world's computation per interval is their sum over its Nodes.
    phase_steps: int = 0


@dataclass(frozen=True, slots=True)
class RayPush:
    """The record of one push of a free ray for the Node to publish
    (ray-momentum-turn-v1): plain bounded integers, as the Node state contract
    requires. The pushed ray's spatial field and amount, its momentum before and
    after, and the field ray that pushed it: its spatial field, amount and heading.
    """

    field: int
    amount: int
    before: tuple[int, int, int]
    after: tuple[int, int, int]
    pusher: int
    pusher_amount: int
    pusher_heading: Heading


@dataclass(frozen=True, slots=True)
class InverseSplit:
    """The record of one inverse split for the Node to publish (inverse-split-v1).

    Plain bounded integers, as the Node state contract requires: the spatial
    field, the Ports transmitted to with the amount per Port, the returned share
    and 1 when the share was first restored to the event's input at the Node. A
    returned ray is a thing (bit-law-v1).
    """

    field: int
    ports: tuple[int, ...]
    amounts: tuple[int, ...]
    amount: int
    restored: int


@dataclass(frozen=True, slots=True)
class SpatialPacket:
    arrival_tick: int
    origin: Address3
    port: int
    fields: SpatialBundle
    rays: tuple[Rays, ...] = ()
    phases: SpatialBundle = ()
    # An external body stepping one Link through this Port (external-body-v1).
    body: ExternalBody | None = None


def zero_spatial_state(components: int) -> SpatialState:
    bounded(components)
    if not 1 <= components <= MAX_COMPONENTS:
        raise ValueError("spatial fields require one to thirty-two components")
    zero = pack((0,) * components)
    return SpatialState((zero,) * 8, (zero,) * 8, (zero,) * 6)


# Ray state rules. A ray carries its heading index and three integer accumulators.
# On every link it steps along the axis that is furthest behind its heading (an
# integer digital differential analyzer), so all rays of one heading and phase
# trace the same lattice line. Nothing here reads another Node or a global value.


def validate_heading(heading: Heading) -> int:
    """Return the Manhattan length of a bounded nonzero integer heading."""
    if type(heading) is not tuple or len(heading) != 3:
        raise ValueError("a ray heading requires three integer components")
    length = 0
    for component in heading:
        if type(component) is not int or abs(component) > MAX_HEADING_COMPONENT:
            raise ValueError("ray heading components must be bounded integers")
        length += abs(component)
    if length == 0:
        raise ValueError("a ray heading must not be the zero vector")
    return length


def validate_rays(rays: Rays, definition: SpatialFieldDefinition, field: FieldDefinition) -> None:
    if type(rays) is not tuple:
        raise ValueError("ray transport requires a tuple of rays")
    if sum(1 for ray in rays if type(ray) is Ray and not ray.parked) > definition.ray_slots:
        raise ValueError("ray slot budget exceeded")
    parked = 0
    for ray in rays:
        if type(ray) is not Ray:
            raise ValueError("ray transport requires immutable Ray entries")
        if type(ray.heading) is not int or not 0 <= ray.heading < len(definition.headings):
            raise ValueError("ray heading index is outside the configured sequence")
        validate_heading(definition.headings[ray.heading])
        if ray.momentum is not None:
            # A momentum is three stored integers (clock-readings-v1: the pushes a
            # thing has not spent, or -dp on a shadow walking home; zero admitted).
            if type(ray.momentum) is not tuple or len(ray.momentum) != 3:
                raise ValueError("a ray momentum requires three integers")
            for value in ray.momentum:
                if type(value) is not int:
                    raise ValueError("a ray momentum requires three integers")
                bounded(value)
        if type(ray.push_remainder) is not tuple or len(ray.push_remainder) != 3:
            raise ValueError("a ray push remainder requires three integers")
        for value in ray.push_remainder:
            if (
                type(value) is not int
                or not -definition.push_denominator < value < definition.push_denominator
            ):
                raise ValueError("a ray push remainder stays below one quantum in units of 1 / D")
        if type(ray.remainder) is not int or type(ray.periods) is not int or ray.periods < 0:
            raise ValueError("a ray clock remainder and its passages are nonnegative integers")
        bounded(ray.periods)
        if type(ray.owed) is not int or ray.owed < 0 or (ray.detector == BIT_SHADOW and ray.owed):
            raise ValueError("the intervals a thing owes are a nonnegative integer; a shadow owes none")
        bounded(ray.owed)
        if ray.detector == BIT_THING and definition.clock:
            # The clock (clock-readings-v1, point 19): the remainder below K, and
            # the content bounded by K and N, content / K below half the circle.
            if not 0 <= ray.remainder < definition.clock:
                raise ValueError("a thing's clock remainder stays below K (clock-readings-v1)")
            if not ray.owners and 2 * abs(ray.amount) >= definition.clock * definition.phase_modulus:
                # A merged thing above the bound (lanes-v1, Highlights 5.4 point
                # 25) is the family's decay table's business (point 20).
                raise ValueError(
                    "a thing's content / K must stay below half the phase circle N / 2: "
                    "K and N bound the content one Node may hold (clock-readings-v1, point 19)"
                )
        elif ray.remainder or (ray.detector == BIT_SHADOW and (ray.periods or any(ray.push_remainder))):
            raise ValueError(
                "a shadow and a family without a clock carry no remainder (clock-readings-v1)"
            )
        length = vector_length(ray_vector(ray, definition))
        if type(ray.accumulators) is not tuple or len(ray.accumulators) != 3:
            raise ValueError("a ray requires three integer accumulators")
        if any(type(a) is not int or not -length < a <= length for a in ray.accumulators):
            raise ValueError("ray accumulators must stay within the heading length")
        if type(ray.parked) is not int or ray.parked not in (0, 1):
            raise ValueError("a ray is parked (1) or on its way (0)")
        if ray.parked:
            # node-is-ports-v1: a parked shadow is at rest, below one quantum in
            # its family's unit, on a Port heading, without a wait or an event,
            # outgoing or returning with the momentum it holds (return-field-v1),
            # and outside the slot budget.
            parked += 1
            if (
                ray.detector != BIT_SHADOW
                or ray.steps
                or ray.wait
                or ray.accumulators != (0, 0, 0)
                or definition.headings[ray.heading] not in PORT_HEADINGS
            ):
                raise ValueError("a parked shadow is a shadow at rest on a Port heading")
            if not 1 <= bounded(ray.amount) < parked_unit(definition):
                raise ValueError("a parked shadow's amount stays below one quantum in its unit")
        elif bounded(ray.amount) == 0:
            raise ValueError("a resident ray must carry a nonzero amount")
        else:
            field.validate(pack((ray.amount,)))
        if type(ray.phase) is not int or not 0 <= ray.phase < definition.phase_modulus:
            raise ValueError("ray phase must be below the field's phase width")
        if type(ray.advance) is not int or not -1 <= ray.advance < definition.phase_modulus:
            raise ValueError("ray advance must be -1 or below the field's phase width")
        pace = heading_pace(definition, ray.heading)
        if type(ray.wait) is not int or not 0 <= bounded(ray.wait) < pace[1]:
            raise ValueError("ray wait must stay below its heading's pace denominator")
        if bounded(ray.interaction_delay) < 0:
            raise ValueError("ray interaction delay must be nonnegative")
        if ray.source_sign not in (-1, 0, 1):
            raise ValueError("ray source_sign must be -1, 0 or 1")
        if type(ray.polarization) is not int or not (
            ray.polarization == POLARIZATION_NONE
            or 0 <= ray.polarization < definition.polarization_modulus
        ):
            raise ValueError(
                "ray polarization must be none (-1) or a step below the family's polarization circle"
            )
        validate_ray_event_state(ray)
    if parked > PARKED_SLOTS * max(1, len(definition.owners)):
        raise ValueError("a Node parks at most thirty-six shares per owner of a family")


def validate_ray_event_state(ray: Ray) -> None:
    """The carried event state is bounded: a count, a bit, a Port mask, six shares, a bit pair."""
    if bounded(ray.steps) < 0:
        raise ValueError("ray steps since its event must be nonnegative")
    if type(ray.outbound) is not int or ray.outbound not in (0, 1):
        raise ValueError("ray outbound must be 1 on the event's heading or 0 reversed")
    if type(ray.event_ports) is not int or not 0 <= ray.event_ports < 64:
        raise ValueError("ray event ports must be a six-bit port mask")
    if type(ray.event_shares) is not tuple or len(ray.event_shares) != 6:
        raise ValueError("ray event shares require one bounded entry per port")
    for port, share in enumerate(ray.event_shares):
        if bounded(share) and not ray.event_ports >> port & 1:
            raise ValueError("ray event shares must be zero where the event sent nothing")
    if ray.detector not in (BIT_SHADOW, BIT_THING):
        raise ValueError("ray detector must be 0 (a shadow) or 1 (a thing), the bit of the law")
    if type(ray.owner) is not int or not 0 <= ray.owner < MAX_THING_ID:
        raise ValueError("ray owner must be a thing id below the id bound")
    if (
        type(ray.owners) is not tuple
        or any(type(o) is not int or not 0 <= o < MAX_THING_ID for o in ray.owners)
        or tuple(sorted(set(ray.owners))) != ray.owners
        or ray.owner in ray.owners
        or (ray.owners and ray.detector != BIT_THING)
    ):
        raise ValueError(
            "a merged thing's further owners are a sorted set of thing ids without its own; "
            "a shadow has none (lanes-v1)"
        )
    if ray.detector == BIT_SHADOW and (ray.event_ports or ray.interaction_delay or ray.advance != -1):
        raise ValueError("a shadow carries no event, no delay and no clock (bit-law-v1)")


@dataclass(frozen=True, slots=True)
class LaneSlots:
    """One family's state at a Node as Highlights 5.4 point 25 bounds it
    (lanes-v1): addressable as [Port][lane][real | shadow(owner)]. `real` holds
    the one real ray of each of the twelve lanes (`lane_index`); `shadow` one
    slot per lane and per owner in the family's owner order (`owner_index`,
    fixed at parsing), the owner's shadows on that lane as one sum, their
    amount and the momentum they carry added, the least steps, the phase of
    their coherent sum (one ray each once the Node's mixing of point 24 lands);
    `parked` the parked shadows and the traces of point 22, outside the lanes;
    `resident` the rays at rest at the Node this interval (a returned thing at
    its event Node, a shadow whose steps are spent, a held ray). The engine
    stores these slots as the Node's ray tuple in merge order and holds their
    bounds as its invariant: one real per lane at every departure
    (`forward_rays`, `validate_plan_rays`) and at every declared board."""

    real: tuple[Ray | None, ...]
    shadow: tuple[tuple[Ray | None, ...], ...]
    parked: Rays = ()
    resident: Rays = ()


def lane_index(port: int, lane: int) -> int:
    """The index of one lane among a Node's twelve: the Port's in-lane (0) or out-lane (1)."""
    if type(port) is not int or not 0 <= port < 6 or lane not in (LANE_IN, LANE_OUT):
        raise ValueError("a lane is one of the six Ports, in (0) or out (1)")
    return LANES_PER_PORT * port + lane


def owner_index(definition: SpatialFieldDefinition, owner: int) -> int:
    """The owner's slot on the shadow axis of a lane (lanes-v1): its rank among the
    family's owners, assigned at parsing to every thing and to every owner of a
    declared profile (`family_owners`); 0 for the one anonymous owner of a family
    that declares none."""
    if definition.owners:
        if owner not in definition.owners:
            raise ValueError("a shadow's owner is one of its family's declared owners (bit-law-v1)")
        return definition.owners.index(owner)
    if owner:
        raise ValueError("a shadow's owner is one of its family's declared owners (bit-law-v1)")
    return 0


def lane_of(ray: Ray, definition: SpatialFieldDefinition) -> int | None:
    """The in-lane a ray on its way occupies at its Node (lanes-v1): the Port it
    entered through, opposite to its heading; None for a parked shadow and for a
    ray at rest (a returned thing at its event Node, a shadow whose steps are
    spent, a ray held by a delay), which is in no lane."""
    if ray.parked or ray.interaction_delay or (not ray.outbound and ray.steps == 0):
        return None
    heading = definition.headings[ray.heading]
    if heading not in PORT_HEADINGS:
        raise ValueError("lanes-v1 addresses the rays of a family on the six Port headings")
    return lane_index(PORT_HEADINGS.index(heading) ^ 1, LANE_IN)


def node_lanes(rays: Rays, definition: SpatialFieldDefinition) -> LaneSlots:
    """The slots of one family at a Node (lanes-v1, Highlights 5.4 point 25):
    twelve lanes, one real slot and one shadow slot per owner on each, the
    parked shadows and the rays at rest beside them. Two real rays on one lane
    are refused: no Port sends two, so none receives two."""
    owners = max(1, len(definition.owners))
    real: list[Ray | None] = [None] * NODE_LANES
    shadow: list[list[list[Ray]]] = [[[] for _ in range(owners)] for _ in range(NODE_LANES)]
    parked: list[Ray] = []
    resident: list[Ray] = []
    for ray in rays:
        if ray.parked:
            parked.append(ray)
            continue
        lane = lane_of(ray, definition)
        if lane is None:
            resident.append(ray)
        elif ray.detector == BIT_THING:
            if real[lane] is not None:
                raise ValueError("two real rays on one lane (Highlights 5.4, point 25)")
            real[lane] = ray
        else:
            shadow[lane][owner_index(definition, ray.owner)].append(ray)
    return LaneSlots(
        tuple(real),
        tuple(tuple(_shadow_sum(group, definition) for group in lane) for lane in shadow),
        tuple(parked),
        tuple(resident),
    )


def _shadow_sum(group: list[Ray], definition: SpatialFieldDefinition) -> Ray | None:
    """One owner's shadows on one lane as one sum (point 24): the first of them
    with the amounts added, the momenta they carry added, the least steps and the
    phase of their coherent sum; None for an empty slot."""
    if not group:
        return None
    first = group[0]
    if len(group) == 1:
        return first
    amount = 0
    momentum = [0, 0, 0]
    carried = False
    for ray in group:
        amount = checked_work(amount + ray.amount)
        if ray.momentum is not None:
            carried = True
            for axis in range(3):
                momentum[axis] = checked_work(momentum[axis] + ray.momentum[axis])
    phase = first.phase
    if definition.coherent and definition.cosine_table:
        phase = phase_of_sum(tuple((ray.amount, ray.phase) for ray in group), definition)
    return replace(
        first,
        amount=bounded(amount),
        momentum=(momentum[0], momentum[1], momentum[2]) if carried else None,
        steps=min(ray.steps for ray in group),
        phase=phase,
    )


def validate_lanes(initial: InitialState) -> None:
    """The lanes of a declared board (lanes-v1, Highlights 5.4 point 25). An
    emission's outputs occupy distinct lanes: a family's sweep of
    `rays_per_tick` consecutive headings of its sequence never repeats a
    heading. No Port sends two reals on one lane, so a declared board with two
    things leaving one Node on one heading is refused: two seeds at one Node
    whose types emit on one ray family with the same declared heading, or both
    sweeping the sequence from its start. A table of section 5.2 is validated
    where it is compiled (`initialization._ray_meeting`)."""
    for definition in initial.spatial_fields:
        if not definition.rays or definition.rays_per_tick <= 1:
            continue
        headings = definition.headings
        count = definition.rays_per_tick
        for start in range(len(headings)):
            window = [headings[(start + offset) % len(headings)] for offset in range(count)]
            if len(set(window)) != len(window):
                raise ValueError(
                    f"an emission's outputs occupy distinct lanes: rays_per_tick {count} of the "
                    f"family {initial.fields[definition.field].name!r} sweeps one heading twice "
                    "(Highlights 5.4, point 25)"
                )
    lamps: dict[int, list[tuple[int, int | None]]] = {}
    for emission in initial.emissions:
        if not initial.spatial_fields[emission.spatial_field].rays:
            continue
        for kind in emission.types or (emission.type_index,):
            lamps.setdefault(kind, []).append((emission.spatial_field, emission.heading))
    # No Port sends two reals on one lane: two seeds at one Node whose types emit
    # on one heading are refused, of one family (the model owner's merge of
    # 2026-09-18 is for a thing born while another passes, not for a declared
    # board) and of two (a meeting the table of the pair decides, which no
    # departure holds).
    taken: dict[tuple[Address3, int | None], tuple[int, int]] = {}
    for seed in initial.seeds:
        for family, heading in lamps.get(seed.record.type_index, ()):
            key = (seed.position, heading)
            if key in taken:
                other_type, other_family = taken[key]
                names = sorted(
                    {
                        initial.fields[initial.spatial_fields[other_family].field].name,
                        initial.fields[initial.spatial_fields[family].field].name,
                    }
                )
                raise ValueError(
                    f"a declared board with two real rays on one lane is refused: the seeds of "
                    f"{initial.disturbances[other_type].name!r} and "
                    f"{initial.disturbances[seed.record.type_index].name!r} at "
                    f"{list(seed.position)} both emit on one heading "
                    f"({' and '.join(repr(name) for name in names)}; two families on one lane "
                    "are a meeting the table of the pair decides) (Highlights 5.4, point 25)"
                )
            taken[key] = (seed.record.type_index, family)


def vector_length(vector: Heading) -> int:
    """The Manhattan length of a nonzero integer vector the DDA walks: a heading of
    the family's table or a ray's momentum (ray-momentum-turn-v1), whose
    components are stored values and may exceed a heading's bound."""
    if type(vector) is not tuple or len(vector) != 3:
        raise ValueError("a ray vector requires three integer components")
    length = 0
    for component in vector:
        if type(component) is not int:
            raise ValueError("ray vector components must be integers")
        length = checked_work(length + abs(bounded(component)))
    if length == 0:
        raise ValueError("a ray vector must not be the zero vector")
    return length


def ray_vector(ray: Ray, definition: SpatialFieldDefinition) -> Heading:
    """The vector a ray walks: the heading of its line, always (clock-readings-v1,
    Highlights 5.4 point 21: every ray moves one Link per interval on its heading;
    a thing's momentum sets the direction it takes next at a departure,
    `step_thing`, never the line it walks now). The DDA walks a heading of the
    table that is not unit-axial as before."""
    return definition.headings[ray.heading]


def ray_line(ray: Ray, definition: SpatialFieldDefinition) -> Heading:
    """The line a ray occupies ahead of it: the heading of its index (the register's
    dominant axis of ray-momentum-turn-v2 is retired with the DDA walk)."""
    return definition.headings[ray.heading]


def ray_momentum_vector(ray: Ray, definition: SpatialFieldDefinition) -> tuple[int, int, int]:
    """One thing's momentum as the ledger reads it (clock-readings-v1): amount x
    heading, its motion, plus the momentum it carries, the pushes not yet spent
    on a step. The sign of a returning thing is the caller's. A shadow's momentum
    is what it carries in flight (return-field-v1): the -dp of the pushes it
    gave, shared through the mixing, zero for a share that gave none."""
    if ray.detector != BIT_THING:
        return ray.momentum if ray.momentum is not None else (0, 0, 0)
    heading = definition.headings[ray.heading]
    carried = ray.momentum if ray.momentum is not None else (0, 0, 0)
    return (
        checked_work(ray.amount * heading[0] + carried[0]),
        checked_work(ray.amount * heading[1] + carried[1]),
        checked_work(ray.amount * heading[2] + carried[2]),
    )


def ledger_momentum(ray: Ray, definition: SpatialFieldDefinition) -> tuple[int, int, int]:
    """One ray's momentum on the ledger's lines, signed (bit-law-v1, Highlights 3.15
    and 5.4 point 7): a thing reads its momentum or amount x heading, negated on
    its walk back (its share on the event's heading, detector-return-v1); a
    shadow is free and reads the momentum it carries in flight, the -dp of the
    pushes it gave (return-field-v1), zero for a share that gave none."""
    vector = ray_momentum_vector(ray, definition)
    if ray.detector == BIT_THING and not ray.outbound:
        return (-vector[0], -vector[1], -vector[2])
    return vector


def ray_momentum_share(ray: Ray, share: int, definition: SpatialFieldDefinition) -> tuple[int, int, int]:
    """The momentum a share of one ray carries away: share x heading on the ray's
    line; a ray with a momentum set by a push is taken whole or not at all."""
    if ray.momentum is None:
        heading = definition.headings[ray.heading]
        return (
            checked_work(share * heading[0]),
            checked_work(share * heading[1]),
            checked_work(share * heading[2]),
        )
    if share != ray.amount:
        raise ValueError("a ray with a momentum set by a push is absorbed whole")
    return ray.momentum


def pushed_ray(ray: Ray, push: tuple[int, int, int], definition: SpatialFieldDefinition) -> Ray:
    """The thing after a push (clock-readings-v1, Highlights 5.4 points 15 and
    23): the push added to the momentum it carries, and the whole quanta it read,
    the push's components in quanta, owed as intervals of wait, w each
    (`owed`, in units of 1 / d); amount, phase, bit, heading, walk and event
    record untouched. A momentum back at zero is cleared, so a thing whose
    pushes cancelled is the thing it was; a push never stops a thing, whose line
    is its heading."""
    carried = ray.momentum if ray.momentum is not None else (0, 0, 0)
    after = (
        bounded(checked_work(carried[0] + push[0])),
        bounded(checked_work(carried[1] + push[1])),
        bounded(checked_work(carried[2] + push[2])),
    )
    quanta = abs(push[0]) + abs(push[1]) + abs(push[2])
    owed = bounded(checked_work(ray.owed + checked_work(quanta * definition.wait_numerator)))
    return replace(ray, momentum=after if any(after) else None, owed=owed)


def step_thing(ray: Ray, definition: SpatialFieldDefinition) -> tuple[Ray, tuple[int, int, int]]:
    """The step of a thing at its departure (clock-readings-v1, Highlights 5.4
    point 21 and the settled rule (i)): the momentum a thing carries sets the
    direction it takes next and never its speed. The first axis (x before y
    before z) whose component has reached the thing's content turns the thing to
    that axis, the sign of the component choosing the sense, and the momentum
    drops by the content on that axis; at most one step per departure. A step
    is a change of heading: a component on the thing's own direction, however
    large, turns it nowhere and drops nothing (the thing is on that axis
    already; the pushes it carries stay its momentum). Returns
    the thing on its new heading, its walk started over when the heading
    changed, and the momentum spent: what the step took off the thing's
    momentum as the ledger reads it (amount x heading plus the pushes carried),
    content x the heading before the step, booked on the momentum field's spent
    line. A thing without a momentum, a shadow and a thing walking back step
    nowhere."""
    if ray.detector != BIT_THING or ray.momentum is None or not ray.outbound:
        return ray, (0, 0, 0)
    content = abs(ray.amount)
    for axis in range(3):
        component = ray.momentum[axis]
        if abs(component) < content:
            continue
        sign = 1 if component > 0 else -1
        target = PORT_HEADINGS[2 * axis + (0 if sign > 0 else 1)]
        if target == definition.headings[ray.heading]:
            continue
        if target not in definition.headings:
            raise ValueError("a step requires the unit-axial heading in the family's sequence")
        momentum = list(ray.momentum)
        momentum[axis] = bounded(checked_work(component - sign * content))
        heading = definition.headings.index(target)
        before = definition.headings[ray.heading]
        spent = (
            checked_work(content * before[0]),
            checked_work(content * before[1]),
            checked_work(content * before[2]),
        )
        stepped = replace(
            ray,
            heading=heading,
            accumulators=ray.accumulators if heading == ray.heading else (0, 0, 0),
            momentum=(momentum[0], momentum[1], momentum[2]) if any(momentum) else None,
        )
        return stepped, spent
    return ray, (0, 0, 0)


def turn_receiver(rule: InteractionDefinition) -> int | None:
    """The role a momentum table on a coupling pushes (ray-momentum-turn-v1 under
    bit-law-v1): the thing met. A table that names a participant family is the
    shadows' table; the one role the table does not name receives every push,
    and when every role's families are named (a thing met by the shadows of its
    own family, [[electron], [electron]] with the table naming electron) the
    first role is the thing and the others its shadows' families. None for a
    rule without a table or a table naming no participant; -1 when the roles
    do not give one receiver."""
    if not rule.momentum_table:
        return None
    named = {kind for kind, sign in enumerate(rule.momentum_table) if sign}
    if not any(kind in named for role in rule.participants for kind in role):
        return None
    receivers = [
        index for index, role in enumerate(rule.participants) if all(kind not in named for kind in role)
    ]
    pushers = [
        index for index, role in enumerate(rule.participants) if all(kind in named for kind in role)
    ]
    if not receivers and len(pushers) == len(rule.participants):
        return 0
    if len(receivers) != 1 or len(receivers) + len(pushers) != len(rule.participants):
        return -1
    return receivers[0]


def dda_step(accumulators: tuple[int, int, int], heading: Heading) -> tuple[int, tuple[int, int, int]]:
    """One Link along the axis furthest behind the heading; ties take the lowest axis.
    The vector is a heading of the table or a ray's momentum."""
    length = vector_length(heading)
    advanced = [a + abs(h) for a, h in zip(accumulators, heading, strict=True)]
    axis = max(range(3), key=lambda i: (advanced[i], -i))
    advanced[axis] -= length
    port = 2 * axis + (0 if heading[axis] > 0 else 1)
    return port, (advanced[0], advanced[1], advanced[2])


def clock_step(ray: Ray, clock: int) -> tuple[int, int]:
    """One interval of a thing's clock (clock-readings-v1, Highlights 5.4 point
    19): the signed phase step and the remainder after it. Forward, the thing
    advances by (remainder + content) // K steps and keeps the rest, below K;
    on the walk back it undoes exactly that interval, floor((remainder - content)
    / K) steps, so a returned thing reaches its event Node with the phase and the
    remainder it left with. A shadow has no clock (bit-law-v1, point 9), nor has
    a family without one (light carries the phase of what emitted it): step 0,
    remainder 0."""
    if ray.detector != BIT_THING or clock <= 0:
        return 0, 0
    total = ray.remainder + ray.amount if ray.outbound else ray.remainder - ray.amount
    step = total // clock
    return step, total - step * clock


def tick_clock(ray: Ray, phase_modulus: int, clock: int) -> Ray:
    """The ray after one interval of its clock: its phase moved by the step,
    masked by the width, and its remainder kept."""
    step, remainder = clock_step(ray, clock)
    if not step and remainder == ray.remainder:
        return ray
    phase = (ray.phase + step) & phase_mask(phase_modulus) if phase_modulus else ray.phase
    return replace(ray, phase=phase, remainder=remainder)


def phase_mask(phase_modulus: int) -> int:
    """The mask of a phase modulus: 2^phase_bits - 1. The modulus is a power of two, so
    every phase advance and difference is a mask, never a division; 0 means that no
    width was given and the phase is left as it is."""
    if type(phase_modulus) is not int or phase_modulus < 0 or phase_modulus & (phase_modulus - 1):
        raise ValueError("the phase modulus must be a power of two")
    return phase_modulus - 1 if phase_modulus else 0


def advance_ray(ray: Ray, heading: Heading, phase_modulus: int = 0, clock: int = 0) -> tuple[int, Ray]:
    """Walk one Link: the DDA port, the step count and the clock.

    An outbound ray counts its steps up and its clock forward, content / K steps
    of phase with the remainder kept (`clock_step`, clock-readings-v1); a
    returning ray counts both down. The phase is masked by the modulus, a power
    of two (2^phase_bits); a family without a clock (K 0) keeps its phase. A
    returning ray with no steps left is at its event Node, and what it does
    there is not defined in this slice, so walking it further is refused.
    """
    port, accumulators = dda_step(ray.accumulators, heading)
    if ray.outbound or ray.detector == BIT_SHADOW:
        # A shadow counts a Link walked whatever its flow (return-field-v1): its
        # steps say only that it arrived.
        steps = bounded(checked_work(ray.steps + 1))
    elif ray.steps > 0:
        steps = ray.steps - 1
    elif not ray.event_ports:
        # A returned field quantum has no event Node to rest at: it walks on with
        # its count at 0 (field-spreading-v1, the proposal of Highlights 5.5).
        steps = 0
    else:
        raise ValueError("a returning ray with no steps left is at its event Node")
    moved = replace(ray, accumulators=accumulators, steps=steps)
    return port, tick_clock(moved, phase_modulus, clock)


def event_stamp(rays: Rays, headings: tuple[Heading, ...]) -> tuple[int, EventShares]:
    """The mask of Ports one event sends to and the amount per Port, read from its rays.

    Each ray leaves through the Port of its first DDA step. Rays on different
    headings that share a first Port are one event on that Port, so their amounts
    add; a share is bounded like any stored value.
    """
    mask, shares = 0, [0] * 6
    for ray, heading in zip(rays, headings, strict=True):
        port, _ = dda_step(ray.accumulators, heading)
        mask |= 1 << port
        shares[port] = checked_work(shares[port] + ray.amount)
    return mask, (
        bounded(shares[0]),
        bounded(shares[1]),
        bounded(shares[2]),
        bounded(shares[3]),
        bounded(shares[4]),
        bounded(shares[5]),
    )


def stamp_event(rays: Rays, headings: tuple[Heading, ...]) -> Rays:
    """Make the given rays the events of one interaction: fresh outbound trajectories
    with no steps walked, each carrying the mask and shares of that interaction.
    What is born at an event is a thing (bit-law-v1, point 1): an emission, the
    outputs of a meeting, the pieces of a split, the transmissions of an inverse
    split; each keeps its owner."""
    mask, shares = event_stamp(rays, headings)
    return tuple(
        replace(
            ray,
            steps=0,
            outbound=1,
            event_ports=mask,
            event_shares=shares,
            detector=BIT_THING,
        )
        for ray in rays
    )


def return_ray(ray: Ray, definition: SpatialFieldDefinition) -> Ray:
    """The same wave ray reversed on its line (detector-return-v1).

    The heading index becomes the index of the negated heading, outbound becomes 0
    and the transport accumulators (DDA, pace wait, interaction delay) are reset;
    amount, phase, steps, event Ports, event shares and Detector bit are exactly
    what arrived. The Detector admission guarantees the negated heading is in the
    sequence; a field where it is not fails closed.
    """
    heading = definition.headings[ray.heading]
    negated = (-heading[0], -heading[1], -heading[2])
    if negated not in definition.headings:
        raise ValueError("a return requires the negated heading in the field's sequence")
    if ray.detector != BIT_THING:
        raise ValueError("a shadow turns back by return_shadow (bit-law-v1)")
    momentum = ray.momentum
    if momentum is not None:
        # ray-momentum-turn-v1: the same ray reversed walks its momentum back.
        momentum = (-momentum[0], -momentum[1], -momentum[2])
    return replace(
        ray,
        heading=definition.headings.index(negated),
        accumulators=(0, 0, 0),
        wait=0,
        interaction_delay=0,
        outbound=0,
        momentum=momentum,
    )


def return_shadow(
    ray: Ray,
    definition: SpatialFieldDefinition,
    momentum: tuple[int, int, int] = (0, 0, 0),
    flip: bool = True,
) -> Ray:
    """A shadow turned back (bit-law-v1, points 3 and 6; return-field-v1): the
    same shadow reversed on the line it arrived by, fresh from this Node (steps
    0, so it leaves reversed and mixes from the next Node), its amount, phase and
    owner what arrived. With `flip`, the turn of a push: its flow inverted
    (outbound 1 to 0, a returning share back to outgoing) and its sign with it,
    and the opposite of the momentum it gave (-dp) added to what it carries.
    Without (a mark, a thing without a table): reversed as it is, nothing
    carried. A shadow walks its heading, never its momentum."""
    if ray.detector != BIT_SHADOW:
        raise ValueError("return_shadow turns back a shadow")
    heading = definition.headings[ray.heading]
    negated = (-heading[0], -heading[1], -heading[2])
    if negated not in definition.headings:
        raise ValueError("a return requires the negated heading in the field's sequence")
    held = ray.momentum if ray.momentum is not None else (0, 0, 0)
    carried = (
        checked_work(held[0] + momentum[0]),
        checked_work(held[1] + momentum[1]),
        checked_work(held[2] + momentum[2]),
    )
    return replace(
        ray,
        heading=definition.headings.index(negated),
        accumulators=(0, 0, 0),
        wait=0,
        steps=0,
        outbound=(ray.outbound ^ 1) if flip else ray.outbound,
        source_sign=-ray.source_sign if flip else ray.source_sign,
        momentum=carried if any(carried) else None,
    )


def rerelease_shadow(ray: Ray, definition: SpatialFieldDefinition) -> Ray:
    """A shadow that came home leaves again from where its thing is (bit-law-v1,
    the amendment's point c): a fresh outgoing shadow on the heading it arrived
    from reversed, back out along its line, with its amount, phase and owner,
    the owner's sign (a returning share's restored), no steps, no momentum (what
    it carried is the owner's now)."""
    heading = definition.headings[ray.heading]
    negated = (-heading[0], -heading[1], -heading[2])
    if negated not in definition.headings:
        raise ValueError("a re-release requires the negated heading in the field's sequence")
    return Ray(
        definition.headings.index(negated),
        (0, 0, 0),
        ray.amount,
        phase=ray.phase,
        detector=BIT_SHADOW,
        source_sign=ray.source_sign if ray.outbound else -ray.source_sign,
        polarization=ray.polarization,
        owner=ray.owner,
    )


def event_port(ray: Ray, definition: SpatialFieldDefinition) -> int:
    """The Port the ray's event sent it through: the first DDA step of its event heading
    from the event Node. A returning ray's event heading is its own heading negated."""
    heading = definition.headings[ray.heading]
    if not ray.outbound:
        heading = (-heading[0], -heading[1], -heading[2])
    port, _ = dda_step((0, 0, 0), heading)
    return port


def port_heading(port: int, definition: SpatialFieldDefinition) -> int:
    """The index of the unit-axial heading that leaves through the given Port; a field
    without that line fails closed."""
    axis, negative = divmod(port, 2)
    unit = tuple(0 if i != axis else (-1 if negative else 1) for i in range(3))
    if unit not in definition.headings:
        raise ValueError("a transmission requires the line of its Port in the field's sequence")
    return definition.headings.index(unit)


def split_ports(ray: Ray, definition: SpatialFieldDefinition) -> tuple[int, ...]:
    """The Ports a returned ray transmits to at its event Node, in Port order: every
    Port of its event's mask except its own."""
    own = event_port(ray, definition)
    return tuple(port for port in range(6) if ray.event_ports >> port & 1 and port != own)


def split_amounts(amount: int, count: int) -> tuple[int, ...]:
    """Share one amount exactly over `count` lines, the remainder to the first lines
    in Port order (Highlights 3.17): nothing is dropped and nothing stays."""
    if count <= 0:
        return ()
    magnitude, sign = abs(bounded(amount)), -1 if amount < 0 else 1
    base, extra = divmod(magnitude, count)
    return tuple(sign * (base + int(offset < extra)) for offset in range(count))


def transmit(ray: Ray, definition: SpatialFieldDefinition) -> tuple[Rays, tuple[int, ...]]:
    """The inverse split of a returned ray at its event Node (inverse-split-v1).

    The ray must be resident at its event Node (`outbound` 0, `steps` 0). The
    transmission is a set of new event rays at this Node: outbound, no steps
    walked, the returned ray's phase, advance and Detector bit, the mask of the
    lines transmitted to and the amount per line as their event record. Returns the
    rays and the Ports, in Port order.
    """
    if ray.outbound or ray.steps:
        raise ValueError("the inverse split requires a returned ray at its event Node")
    ports = split_ports(ray, definition)
    amounts = split_amounts(ray.amount, len(ports))
    rays = tuple(
        Ray(
            port_heading(port, definition),
            (0, 0, 0),
            amount,
            ray.phase,
            ray.advance,
            source_sign=ray.source_sign,
            polarization=ray.polarization,
            owner=ray.owner,
        )
        for port, amount in zip(ports, amounts, strict=True)
        if amount
    )
    stamped = stamp_event(rays, tuple(definition.headings[r.heading] for r in rays))
    return stamped, ports


RayMergeKey = tuple[
    int,
    tuple[int, int, int],
    int,
    int,
    int,
    int,
    int,
    int,
    int,
    EventShares,
    int,
    int,
    tuple[int, int, int] | None,
    int,
    int,
    int,
    tuple[int, int, int],
    int,
    int,
    int,
    tuple[int, ...],
]


def ray_merge_key(ray: Ray) -> RayMergeKey:
    """The identity of a ray's line and event: everything but its amount, in a fixed
    order; the clock's remainder, the push remainder and the passages are part of
    it (clock-readings-v1)."""
    return (
        ray.heading,
        ray.accumulators,
        ray.phase,
        ray.advance,
        ray.wait,
        ray.interaction_delay,
        ray.steps,
        ray.outbound,
        ray.event_ports,
        ray.event_shares,
        ray.detector,
        ray.source_sign,
        ray.momentum,
        ray.polarization,
        ray.owner,
        ray.remainder,
        ray.push_remainder,
        ray.periods,
        ray.owed,
        ray.parked,
        ray.owners,
    )


def merge_rays(rays: Rays) -> Rays:
    """Combine rays that share heading, lattice phase, wave phase and event: one line, so exact.

    Rays of different events never merge, whatever their heading and phase: the
    event state is part of the identity, so each ray keeps the information of
    its own event. Field content of opposite source signs never merges either:
    it stays two rays of the same family (field-spreading-v1). A parked shadow
    of amount zero, a trace, is kept (node-is-ports-v1).
    """
    combined: dict[RayMergeKey, int] = {}
    # ray-momentum-turn-v1: momentum is extensive, so rays of one momentum that
    # merge carry the sum of their momenta, as they carry the sum of their amounts.
    counts: dict[RayMergeKey, int] = {}
    for ray in rays:
        key = ray_merge_key(ray)
        combined[key] = checked_work(combined.get(key, 0) + ray.amount)
        counts[key] = counts.get(key, 0) + 1
    return tuple(
        Ray(
            key[0],
            key[1],
            bounded(amount),
            key[2],
            key[3],
            key[4],
            key[5],
            steps=key[6],
            outbound=key[7],
            event_ports=key[8],
            event_shares=key[9],
            detector=key[10],
            source_sign=key[11],
            momentum=_merged_momentum(key[12], counts[key]),
            polarization=key[13],
            owner=key[14],
            remainder=key[15],
            push_remainder=key[16],
            periods=key[17],
            owed=key[18],
            parked=key[19],
            owners=key[20],
        )
        for key, amount in sorted(combined.items(), key=lambda item: _merge_order(item[0]))
        if amount or key[19]
    )


def _merged_momentum(momentum: tuple[int, int, int] | None, count: int) -> tuple[int, int, int] | None:
    """The momentum of `count` merged rays that share one: its sum, count times it."""
    if momentum is None:
        return None
    return (
        bounded(checked_work(momentum[0] * count)),
        bounded(checked_work(momentum[1] * count)),
        bounded(checked_work(momentum[2] * count)),
    )


def _merge_order(key: RayMergeKey) -> tuple[object, ...]:
    """The fixed order of merged rays: the key with a momentum not set before one set,
    the polarization, the owner and the parked flag last, so that rays without one
    keep the order they had."""
    momentum = key[12]
    return (*key[:12], momentum is not None, momentum or (0, 0, 0), *key[13:])


def ray_stock(rays: Rays) -> int:
    total = 0
    for ray in rays:
        total = checked_work(total + ray.amount)
    return bounded(total)


def ray_momentum(rays: Rays, definition: SpatialFieldDefinition) -> tuple[int, int, int]:
    """Read the candidate's amount-times-heading inventory from actual ray owners.

    A returning ray (outbound 0) reads as its share on the event's heading, its
    own heading negated: the Detector takes no recoil on a return and the audit
    stays exact (detector-return-v1, issue #169).
    """
    result = [0, 0, 0]
    for ray in rays:
        for axis, value in enumerate(ledger_momentum(ray, definition)):
            result[axis] = checked_work(result[axis] + value)
    return result[0], result[1], result[2]


def ray_charge(rays: Rays, definition: SpatialFieldDefinition) -> int:
    """The charge readout of one bundle: the family's charge per quantum times the amount,
    summed over its things as a 64-bit intermediate (wave-ray-family-v1). A shadow
    carries the sign of its owner's charge as a message and no charge (bit-law-v1)."""
    total = 0
    for ray in rays:
        if ray.detector == BIT_THING:
            total = checked_work(total + checked_work(ray.amount * definition.charge))
    return total


def attenuate_rays(rays: Rays, decay: DecayDefinition, meter: CostMeter) -> tuple[Rays, int]:
    """Apply the completed-link ratio to each ray; return survivors and the removed total."""
    numerator, denominator = decay.retain_numerator, decay.retain_denominator
    survivors, removed = [], 0
    for ray in rays:
        meter.charge("read")
        magnitude = checked_work(abs(ray.amount) * numerator) // denominator
        kept = -magnitude if ray.amount < 0 else magnitude
        removed = checked_work(removed + ray.amount - kept)
        meter.charge("update", 3)
        if kept:
            survivors.append(replace(ray, amount=kept))
    return tuple(survivors), bounded(removed)


# Kerengonen rules. A ray carries a phase step; rays that meet at a Node combine
# by phase. Coherence is |sum a e^(i phi)|^2 / (sum |a|)^2 in bounded integers:
# a fixed cosine table over phase differences, scaled by PHASE_COSINE_SCALE, so
# equal phases give exactly one and opposite phases of equal amounts exactly zero.

MAX_PHASE_STEPS = 4096
PHASE_COSINE_SCALE = 256
# pi in fixed point: integer arithmetic only, as every physical module requires.
_PI_FIXED = 3141592654
_FIXED = 1000000000


def _fixed_cosine(angle: int) -> int:
    """cos of a fixed-point angle in [0, pi/2], scaled by _FIXED, by its series."""
    if not 0 <= angle <= _PI_FIXED // 2:
        raise ValueError("phase table angle is outside the first quadrant")
    magnitude, total, sign = _FIXED, 0, 1
    for k in range(2, 66, 2):
        total = checked_work(total + sign * magnitude)
        magnitude = checked_work(magnitude * angle) // _FIXED
        magnitude = checked_work(magnitude * angle) // _FIXED // ((k - 1) * k)
        if not magnitude:
            return total
        sign = -sign
    raise OverflowError("phase table cosine did not converge within its fixed bound")


def _fixed_sine(angle: int) -> int:
    """sin of a fixed-point angle in [0, pi/2], scaled by _FIXED, by its series."""
    if not 0 <= angle <= _PI_FIXED // 2:
        raise ValueError("phase table angle is outside the first quadrant")
    magnitude, total, sign = angle, 0, 1
    for k in range(3, 67, 2):
        total = checked_work(total + sign * magnitude)
        magnitude = checked_work(magnitude * angle) // _FIXED
        magnitude = checked_work(magnitude * angle) // _FIXED // ((k - 1) * k)
        if not magnitude:
            return total
        sign = -sign
    raise OverflowError("phase table sine did not converge within its fixed bound")


@lru_cache(maxsize=16)
def phase_sines(phase_steps: int) -> tuple[int, ...]:
    """Scaled sine of every phase step, the companion of phase_cosines."""
    phase_cosines(phase_steps)
    entries = []
    for step in range(phase_steps):
        reduced = step if 2 * step <= phase_steps else phase_steps - step
        angle = checked_work(2 * _PI_FIXED * reduced) // phase_steps
        if 4 * reduced > phase_steps:
            angle = _PI_FIXED - angle
        scaled = checked_work(_fixed_sine(angle) * PHASE_COSINE_SCALE + _FIXED // 2) // _FIXED
        entries.append(scaled if 2 * step <= phase_steps else -scaled)
    return tuple(entries)


def _phase_of_sum(
    terms: tuple[tuple[int, int], ...],
    cosines: tuple[int, ...],
    sines: tuple[int, ...],
    phase_steps: int,
) -> int:
    """The phase step nearest the direction of sum a e^(i phi) over the given tables."""
    mask = phase_mask(phase_steps)
    x = y = 0
    for amount, phase in terms:
        x = checked_work(x + amount * cosines[phase & mask])
        y = checked_work(y + amount * sines[phase & mask])
    best, best_projection = 0, None
    for step in range(phase_steps):
        projection = checked_work(x * cosines[step] + y * sines[step])
        if best_projection is None or projection > best_projection:
            best, best_projection = step, projection
    return best


def phase_of_sum(terms: tuple[tuple[int, int], ...], definition: SpatialFieldDefinition) -> int:
    """The phase step nearest the direction of sum a e^(i phi): the best projection.

    Ties and an empty or cancelled sum give step zero. Bounded by phase_steps.
    """
    return _phase_of_sum(terms, definition.cosine_table, definition.sine_table, definition.phase_steps)


@lru_cache(maxsize=16)
def phase_cosines(phase_steps: int) -> tuple[int, ...]:
    """Scaled cosine of every phase difference; immutable law data, computed once.

    cos(2 pi d / P) x 256, rounded to the nearest integer. The only rational
    values on that circle are 0, +-1/2 and +-1, so no entry is a half-integer.
    """
    if type(phase_steps) is not int or not 2 <= phase_steps <= MAX_PHASE_STEPS:
        raise ValueError("kerengonen phase_steps must be between 2 and 4096")
    entries = []
    for difference in range(phase_steps):
        reduced = min(difference, phase_steps - difference)
        angle = checked_work(2 * _PI_FIXED * reduced) // phase_steps
        flip = 4 * reduced > phase_steps
        if flip:
            angle = _PI_FIXED - angle
        cosine = _fixed_cosine(angle)
        scaled = checked_work(cosine * PHASE_COSINE_SCALE + _FIXED // 2) // _FIXED
        entries.append(-scaled if flip else scaled)
    return tuple(entries)


def coherence(rays: Rays, definition: SpatialFieldDefinition) -> tuple[int, int]:
    """Numerator and denominator of the coherent fraction of one Node's rays, in [0, 1]."""
    if not definition.coherent or not rays:
        return (1, 1)
    return _coherence(rays, definition.cosine_table, definition.phase_mask)


def _coherence(rays: Rays, cosines: tuple[int, ...], mask: int) -> tuple[int, int]:
    """The coherent fraction over the given cosine table and phase mask."""
    by_phase: dict[int, int] = {}
    magnitude = 0
    for ray in rays:
        by_phase[ray.phase] = checked_work(by_phase.get(ray.phase, 0) + ray.amount)
        magnitude = checked_work(magnitude + abs(ray.amount))
    numerator = 0
    for phase, amount in by_phase.items():
        for other, other_amount in by_phase.items():
            numerator = checked_work(
                numerator + checked_work(amount * other_amount) * cosines[(phase - other) & mask]
            )
    denominator = checked_work(checked_work(magnitude * magnitude) * PHASE_COSINE_SCALE)
    return (min(max(numerator, 0), denominator), denominator)


# The two captures are deterministic; nothing draws (bit-law-v1, point 14). The
# mark's table below is the one counter of the model: the Detector mark counts
# the things that arrive and catches them by its setting.
CAPTURE_MODES = ("share", "threshold")
ARRIVAL_MODULUS = 1073741789  # the largest prime below the field value bound


def table_catch(arrivals: int, numerator: int, denominator: int) -> tuple[int, int]:
    """One step of a mark's table (bit-law-v1, point 14: there is no lottery): the
    next count and whether the arrival is caught, 1 = caught. The k-th arrival, k
    the count before it, is caught when k mod d < n, so the setting [n, d] is a
    declared table, "catch n arrivals in every d" (1 / 1 catches every thing,
    0 / 1 none), like a mirror's or a splitter's; the count wraps at the modulus.
    The step reads nothing from the ray."""
    if not 0 <= arrivals < ARRIVAL_MODULUS:
        raise ValueError("a mark's count of arrivals must stay below the arrival modulus")
    if denominator < 1 or not 0 <= numerator <= denominator:
        raise ValueError("a setting is a rational from 0 through 1")
    caught = arrivals % denominator < numerator
    return (arrivals + 1) % ARRIVAL_MODULUS, int(caught)


def mark_catch(arrivals: int, mark: DetectorMark) -> tuple[int, int]:
    """One step of a marked Node's table: the next count and 1 when the thing is caught."""
    return table_catch(arrivals, mark.pass_numerator, mark.pass_denominator)


def click_coupling(mark: DetectorMark, index: int, definition: SpatialFieldDefinition) -> int:
    """What the mark does with a thing of spatial field `index` that draws 1
    (detector-absorb-v1 under bit-law-v1): its declared `on_click` for that
    family, or the default, CLICK_ABSORB for every family."""
    declared = mark.on_click[index] if index < len(mark.on_click) else CLICK_DEFAULT
    return CLICK_ABSORB if declared == CLICK_DEFAULT else declared


def detector_absorb(
    mark: DetectorMark, index: int, rays: Rays, definition: SpatialFieldDefinition, fields: int
) -> DetectorMark:
    """The click as an absorption into the thing resident at the mark
    (detector-absorb-v1 under node-is-ports-v1): the arriving rays of one family
    that were caught end in the resident, a thing on its things line and a
    shadow home to it on its shadows line (settled rule (iv)), their momentum,
    amount x heading or the momentum a push set, in the resident's momentum; a
    thing absorbed makes the resident the home of its shadows (`owners`), and
    each shadow of it that returns is absorbed into the same resident. `fields`
    sizes the content lines, one entry per spatial field, on the first
    absorption; nothing else of the mark changes."""
    resident = mark.resident
    things = list(resident.things) or [0] * fields
    shadows = list(resident.shadows) or [0] * fields
    momentum = list(resident.momentum)
    owners = set(resident.owners)
    for ray in rays:
        if ray.detector == BIT_THING:
            things[index] = checked_work(things[index] + ray.amount)
            owners.add(ray.owner)
            owners.update(ray.owners)
        else:
            shadows[index] = checked_work(shadows[index] + ray.amount)
        for axis, value in enumerate(ledger_momentum(ray, definition)):
            momentum[axis] = checked_work(momentum[axis] + value)
    return replace(
        mark,
        resident=Resident(
            tuple(things), tuple(shadows), (momentum[0], momentum[1], momentum[2]), tuple(sorted(owners))
        ),
    )


def validate_detector_marks(initial: InitialState) -> None:
    """Marks are admitted under the shared Detector admission, one mark per Node."""
    if type(initial.detectors) is not tuple or len(initial.detectors) > MAX_DETECTORS:
        raise ValueError("detectors exceed their fixed capacity")
    if not initial.detectors:
        return
    positions: set[Address3] = set()
    for mark in initial.detectors:
        if type(mark) is not DetectorMark:
            raise ValueError("detectors require DetectorMark entries")
        if any(c >= length for c, length in zip(mark.position, initial.shape, strict=True)):
            raise ValueError("a Detector mark position must be within shape")
        if mark.position in positions:
            raise ValueError("a Node carries one Detector mark")
        positions.add(mark.position)
        if len(mark.on_click) not in (0, len(initial.spatial_fields)):
            raise ValueError("a Detector mark declares on_click per spatial field")
        if len(mark.resident.things) not in (0, len(initial.spatial_fields)):
            raise ValueError("a resident thing's content has one entry per spatial field")
    ray_fields = [definition for definition in initial.spatial_fields if definition.rays]
    if (
        initial.schema_version != 1
        or initial.link_ticks != 1
        or initial.node_execution
        or initial.spatial_computation_delay
        or not ray_fields
    ):
        raise ValueError(
            "Detector marks require schema 1, link_ticks 1, the default clock and a ray field"
        )
    for definition in ray_fields:
        headings = set(definition.headings)
        if (
            definition.euclidean
            or definition.pace_numerator != definition.pace_denominator
            or definition.decay is not None
            or any(sum(abs(c) for c in heading) != 1 for heading in definition.headings)
            or any(tuple(-c for c in heading) not in headings for heading in definition.headings)
        ):
            raise ValueError(
                "Detector marks require unpaced, undecayed ray fields with unit-axial "
                "headings closed under negation"
            )


def coherent_stock(rays: Rays, definition: SpatialFieldDefinition) -> int:
    """The stock a reader sees: the ray total scaled by the Node's coherence, toward zero."""
    total = ray_stock(rays)
    numerator, denominator = coherence(rays, definition)
    if numerator == denominator:
        return total
    magnitude = checked_work(abs(total) * numerator) // denominator
    return bounded(-magnitude if total < 0 else magnitude)


# Euclidean pace. A heading of Manhattan length L and Euclidean length E covers
# E / L of a Euclidean unit per link. Pacing every ray to the slowest direction
# makes the wave front round: a ray hops when its wait passes its denominator.

PACE_SCALE = 4096


def integer_sqrt(value: int) -> int:
    """The floor of the square root, by Newton's method on integers."""
    if checked_work(value) < 0:
        raise ValueError("square root of a negative integer")
    if value < 2:
        return value
    guess = value
    better = (guess + value // guess) // 2
    for _ in range(64):
        if better >= guess:
            return guess
        guess, better = better, (better + value // better) // 2
    raise OverflowError("integer square root exceeded its fixed iteration bound")


def prepare_heading_paces(definition: SpatialFieldDefinition) -> tuple[tuple[int, int], ...]:
    """(numerator, denominator) hops per tick for every heading.

    (1, 1) for every heading on the links metric at link speed; the configured
    pace scales every heading alike, and the Euclidean metric slows each heading
    to the slowest lattice direction on top of it.
    """
    numerator, denominator = bounded(definition.pace_numerator), bounded(definition.pace_denominator)
    if not 1 <= numerator <= denominator:
        raise ValueError("pace must be positive and not exceed one link per tick")
    if not 1 <= len(definition.headings) <= MAX_HEADINGS:
        raise ValueError("ray transport requires one to 65536 headings")
    if not definition.euclidean:
        return tuple((numerator, denominator) for _ in definition.headings)
    ratios = []
    for heading in definition.headings:
        manhattan = validate_heading(heading)
        squared = sum(c * c for c in heading)
        ratios.append(integer_sqrt(checked_work(squared * PACE_SCALE * PACE_SCALE)) // manhattan)
    slowest = min(ratios)
    table = []
    for ratio in ratios:
        terms = reduced_ratio(checked_work(slowest * numerator), checked_work(ratio * denominator))
        table.append((bounded(terms[0]), bounded(terms[1])))
    return tuple(table)


def heading_paces(definition: SpatialFieldDefinition) -> tuple[tuple[int, int], ...]:
    """Read immutable configured pace data; physical stepping never prepares a table."""
    return definition.pace_table


def heading_pace(definition: SpatialFieldDefinition, heading: int) -> tuple[int, int]:
    return heading_paces(definition)[heading]


# The external body (external-body-v1). Every rule here reads the body's own mark
# and the rays that arrived at its Node; nothing reads another Node.


def body_release(body: ExternalBody, definition: SpatialFieldDefinition, port: int = -1) -> Rays:
    """The shadows of a body for one interval of the prefill (bit-law-v1): one per
    Port heading of its own family, each the whole quanta of amount x n / d by
    the family's release, with the body's declared phase, the sign of its charge
    and its id, no event. A body releases nothing during a run. In an interval
    the body steps through a Port, that heading is its own line ahead of it, and
    it releases nothing there (no self-field, Highlights 3.5). The amount enters
    no sum: the product is a Python integer and only the ray amount is bounded."""
    amount = (body.amount * definition.release_numerator) // definition.release_denominator
    if amount <= 0:
        return ()
    skip = PORT_HEADINGS[port] if port >= 0 else None
    return _released(
        bounded(amount),
        body.phase & definition.phase_mask,
        definition,
        skip,
        charge_sign(body.charge),
        body.thing,
    )


def body_absorb(
    body: ExternalBody, index: int, rays: Rays, definition: SpatialFieldDefinition
) -> ExternalBody:
    """The sink: the arriving things of one family end in the body's exact counter
    for that family. A body is not pushed by matter (Highlights 3.19), and since
    bit-law-v1 a thing is what arrives here; the body's content never changes."""
    sink = list(body.sink)
    for ray in rays:
        sink[index] = checked_work(sink[index] + ray.amount)
    return replace(body, sink=tuple(sink))


def push_of(
    sign: int,
    shadow: Ray,
    definition: SpatialFieldDefinition,
    reads: str,
    content: int,
    charge: int,
    remainder: tuple[int, int, int] = (0, 0, 0),
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """The push one shadow gives a thing, the two readings of point 16 (Highlights
    5.4 points 16 and 18, clock-readings-v1): the whole push and the pushed
    thing's push remainder after it. The gravity reading, `reads` "content": the
    table's sign x the shadow's amount x its heading x the content of what is
    pushed, exact, the remainder untouched. The electricity reading, `reads`
    "charge": the table's sign x the shadow's amount x its heading x (the owner's
    charge / the owner's content) x the charge of what is pushed, the owner's
    charge and content read by the owner's id from the family's owner table (a
    shadow is a ray of its owner's family: the owner's whole charge, its charge
    per quantum times its stock) and the charge of what is pushed being its
    charge per quantum, the family's for a thing and the declared for a body;
    the product is accumulated per axis in units of 1 / D, D the family's
    push denominator (a multiple of every owner's content), on the pushed thing's
    remainder, and the whole units go into the momentum, the rounding toward
    zero so that a push below one quantum of either sign accumulates exactly
    and the remainder keeps its sign. The table's -1 is attraction toward the
    source, which lies opposite the arriving heading, for a positive product."""
    heading = definition.headings[shadow.heading]
    # A returning share pushes with the opposite sign (return-field-v1): the
    # thing reads the signed sum of its owner's outgoing and returning shares.
    if not shadow.outbound:
        sign = -sign
    if reads == "content":
        scale = checked_work(checked_work(sign * shadow.amount) * content)
        return (
            (
                checked_work(scale * heading[0]),
                checked_work(scale * heading[1]),
                checked_work(scale * heading[2]),
            ),
            remainder,
        )
    if reads != "charge":
        raise ValueError("a momentum table reads content or charge (bit-law-v1, point 16)")
    owner_content = definition.owner_content(shadow.owner)
    if owner_content <= 0:
        raise ValueError(
            "the electricity reading needs the shadow's owner's content: the owner is not in "
            "the family's owner table (clock-readings-v1, point 18)"
        )
    denominator = definition.push_denominator
    if denominator % owner_content:
        raise ValueError("the family's push denominator is a multiple of every owner's content")
    scale = checked_work(
        checked_work(
            checked_work(sign * shadow.amount)
            * checked_work(definition.owner_charge(shadow.owner) * charge)
        )
        * (denominator // owner_content)
    )
    whole = [0, 0, 0]
    kept = [0, 0, 0]
    for axis in range(3):
        total = checked_work(remainder[axis] + checked_work(scale * heading[axis]))
        units = abs(total) // denominator
        whole[axis] = units if total >= 0 else -units
        kept[axis] = total - whole[axis] * denominator
    return (whole[0], whole[1], whole[2]), (kept[0], kept[1], kept[2])


def body_pushed(body: ExternalBody, push: tuple[int, int, int]) -> ExternalBody:
    """The body's momentum after a push (bit-law-v1, point 3): sign x amount x
    heading of a shadow of a family its momentum table names, or -dp brought home
    by a shadow it released. Nothing else moves it."""
    momentum = tuple(checked_work(a + b) for a, b in zip(body.momentum, push, strict=True))
    return replace(body, momentum=(momentum[0], momentum[1], momentum[2]))


def body_step(body: ExternalBody) -> tuple[int, ExternalBody]:
    """One interval of the body's motion: each axis accumulator adds the momentum
    component, and the body steps one Link through the Port of the first axis
    (x before y before z) whose accumulator has reached a whole amount, subtracting
    the amount; at most one Link per interval, never faster than a ray. Returns
    the Port, or -1 when it stays, and the body with its new accumulators."""
    try:
        port, accumulators = motion_step(body.momentum, body.accumulators, body.amount)
    except ValueError as error:
        raise ValueError("an external body momentum exceeds its amount: faster than a ray") from error
    return port, replace(body, accumulators=accumulators)


def body_coupled_families(body: ExternalBody, initial: InitialState) -> frozenset[int]:
    """The spatial fields the body's declared coupling rule meets: every role of the
    rule that does not select the body's family; empty for the sink and for the
    polarizer, which is no rule (ray-polarization-v1)."""
    if body.coupling in (BODY_SINK, BODY_POLARIZER):
        return frozenset()
    rule = initial.ray_interactions[body.coupling]
    return frozenset(kind for role in rule.participants for kind in role if kind != body.family)


def body_token(body: ExternalBody) -> Ray:
    """The body as the participant of its coupling rule that never changes: one
    quantum of its family at the Node, heading 0, no event, a thing of the body's
    identity; the Node strips the rule's unchanged output of it before anything
    leaves."""
    return Ray(0, (0, 0, 0), 1, phase=body.phase, owner=body.thing)


@dataclass(frozen=True, slots=True)
class Polarized:
    """The record of one arriving ray met by a polarizer, for the Node to publish
    (ray-polarization-v1): plain bounded integers. The ray's amount, polarization
    (-1 none) and source sign, the difference angle - polarization on the circle
    (-1 for an unpolarized ray), the pass share in D-ths, the whole quanta passed
    and sunk, the shares below one quantum added to the pass and the sink
    held shares, the whole quanta the held shares released to the pass Port and to
    the sink after this ray, and the body's six held shares after it."""

    amount: int
    polarization: int
    sign: int
    difference: int
    share: int
    passed: int
    sunk: int
    held: tuple[int, int]
    released: tuple[int, int]
    held_after: tuple[int, ...]


def polarizer_slot(sign: int, output: int) -> int:
    """The held share of one source sign (-1, 0, 1) and output (0 pass, 1 sink)."""
    if sign not in REMAINDER_SIGNS or output not in (0, 1):
        raise ValueError("a polarizer share is named by a source sign and pass or sink")
    return (sign + 1) * 2 + output


def polarizer_share(polarizer: Polarizer, polarization: int) -> tuple[int, int]:
    """The difference d = (angle - polarization) mod D and the pass share T[d] in
    D-ths of an arriving ray; an unpolarized ray takes the declared unpolarized
    share and has no difference (-1)."""
    if polarization == POLARIZATION_NONE:
        return -1, polarizer.unpolarized
    if type(polarization) is not int or not 0 <= polarization < polarizer.steps:
        raise ValueError("a polarizer reads a polarization step of its own circle")
    difference = (polarizer.angle - polarization) % polarizer.steps
    return difference, polarizer.table[difference]


def held_stock(body: ExternalBody) -> int:
    """The whole quanta a polarizer body's held shares hold in total, exactly
    (ray-polarization-v1): the pass and the sink fraction of one ray sum to a
    whole quantum, so the held shares of one sign always hold whole quanta."""
    if body.polarizer is None or not body.held:
        return 0
    whole, fraction = divmod(sum(body.held), body.polarizer.steps)
    if fraction:
        raise ValueError("a polarizer body holds whole quanta in its held shares in total")
    return whole


def polarize_content(
    body: ExternalBody, index: int, rays: Rays, definition: SpatialFieldDefinition
) -> tuple[ExternalBody, Rays, tuple[Polarized, ...]]:
    """The polarizer (ray-polarization-v1; Highlights 3.19, 3.26): each arriving
    outbound ray of the polarized family, in merge-key order, is split by the
    body's table at the difference between the body's angle and the ray's
    polarization: the whole quanta of amount x T[d] / D leave on the pass Port
    as a fresh event ray with the ray's phase, bit and sign and the body's angle
    as its polarization; the whole quanta of amount x (D - T[d]) / D end in the
    body's sink for the family (moving the body by its momentum table as the
    sink does); and the two shares below one quantum, which sum to one quantum
    or to none, go to the body's pass and sink held shares of the ray's sign, in
    units of 1/D, each held share's phase combined with the share's by the
    coherence rule as a parked shadow's is (field-remainder-v1). A held share
    that reaches D releases the whole quanta it holds, to the pass Port as a
    fresh event ray with the held share's phase, sign and the body's angle and the
    highest bit of this meeting's arrivals, or into the sink, and keeps the rest.
    Returns the body after, the pass rays stamped as events of this Node, and one
    record per arriving ray. The total is exact: what arrived equals what passed
    plus what sank plus the whole quanta the held shares gained."""
    polarizer = body.polarizer
    if polarizer is None or polarizer.family != index:
        raise ValueError("a polarizer meets the family it polarizes")
    steps = polarizer.steps
    if definition.polarization_modulus != steps:
        raise ValueError("a polarizer table has one entry per step of its family's circle")
    heading = definition.headings[polarizer.pass_heading]
    tables = spread_tables(definition)
    held = list(body.held) if body.held else [0] * POLARIZER_SLOTS
    phases = list(body.held_phases) if body.held_phases else [0] * POLARIZER_SLOTS
    sink = list(body.sink)
    passing: list[Ray] = []
    records: list[Polarized] = []
    for ray in sorted(rays, key=ray_merge_key):
        if not ray.outbound or ray.amount <= 0:
            raise ValueError("a polarizer meets the outbound content that arrived")
        difference, share = polarizer_share(polarizer, ray.polarization)
        passed, pass_fraction = divmod(checked_work(ray.amount * share), steps)
        sunk, sink_fraction = divmod(checked_work(ray.amount * (steps - share)), steps)
        if passed:
            passing.append(
                Ray(
                    polarizer.pass_heading,
                    (0, 0, 0),
                    bounded(passed),
                    phase=ray.phase,
                    advance=ray.advance,
                    source_sign=ray.source_sign,
                    polarization=polarizer.angle,
                    owner=ray.owner,
                )
            )
        if sunk:
            sink[index] = checked_work(sink[index] + sunk)
        released = [0, 0]
        for output, fraction in ((0, pass_fraction), (1, sink_fraction)):
            if not fraction:
                continue
            slot = polarizer_slot(ray.source_sign, output)
            if tables is None:
                phases[slot] = 0
            elif held[slot]:
                phases[slot] = _phase_of_sum(
                    ((held[slot], phases[slot]), (fraction, ray.phase)),
                    tables[0],
                    tables[1],
                    definition.phase_modulus,
                )
            else:
                phases[slot] = ray.phase
            held[slot] = checked_work(held[slot] + fraction)
            whole, rest = divmod(held[slot], steps)
            if not whole:
                continue
            held[slot] = rest
            released[output] = whole
            if output == 0:
                passing.append(
                    Ray(
                        polarizer.pass_heading,
                        (0, 0, 0),
                        bounded(whole),
                        phase=phases[slot],
                        source_sign=ray.source_sign,
                        polarization=polarizer.angle,
                        owner=ray.owner,
                    )
                )
            else:
                sink[index] = checked_work(sink[index] + whole)
            if not rest:
                phases[slot] = 0
        records.append(
            Polarized(
                ray.amount,
                ray.polarization,
                ray.source_sign,
                difference,
                share,
                bounded(passed),
                bounded(sunk),
                (pass_fraction, sink_fraction),
                (released[0], released[1]),
                tuple(held),
            )
        )
    after = replace(body, sink=tuple(sink), held=tuple(held), held_phases=tuple(phases))
    stamped = tuple(stamp_event((ray,), (heading,))[0] for ray in merge_rays(tuple(passing)))
    return after, stamped, tuple(records)


def validate_external_bodies(initial: InitialState) -> None:
    """The admission of external bodies (external-body-v1): the shared Detector
    admission, one body per Node, never on a Detector, a unit-axial links-metric
    ray family at pace 1, the family's released field when one is declared, a
    coupling that is the sink or a declared meeting with outputs in which one role
    selects the body's family alone and the body is returned unchanged."""
    if type(initial.external_bodies) is not tuple or len(initial.external_bodies) > MAX_EXTERNAL_BODIES:
        raise ValueError("external bodies exceed their fixed capacity")
    if not initial.external_bodies:
        return
    if (
        initial.schema_version != 1
        or initial.link_ticks != 1
        or initial.node_execution
        or initial.spatial_computation_delay
        or initial.field_phase_first
        or initial.arrival_port_blind
        or initial.delay_direction is not None
        or initial.field_rules
        or initial.spatial_interactions
        or initial.spatial_couplings
    ):
        raise ValueError("an external body requires the default fixed H=1 spatial clock")
    positions = {mark.position for mark in initial.detectors}
    for expected, body in enumerate(initial.external_bodies):
        if type(body) is not ExternalBody:
            raise ValueError("external_bodies require ExternalBody entries")
        if body.index != expected:
            raise ValueError("external bodies are indexed in declaration order")
        if any(c >= length for c, length in zip(body.position, initial.shape, strict=True)):
            raise ValueError("an external body position must be within shape")
        if body.position in positions:
            raise ValueError("a Node carries one external body and no Detector mark beside it")
        positions.add(body.position)
        if body.family >= len(initial.spatial_fields):
            raise ValueError("an external body family must name a ray spatial field")
        family = initial.spatial_fields[body.family]
        if (
            not family.rays
            or family.euclidean
            or family.pace_numerator != family.pace_denominator
            or family.decay is not None
            or any(sum(abs(c) for c in heading) != 1 for heading in family.headings)
            or any(heading not in family.headings for heading in PORT_HEADINGS)
        ):
            raise ValueError("an external body requires a unit-axial unpaced ray family")
        if body.phase >= family.phase_modulus:
            raise ValueError("an external body phase must be below its family's phase width")
        if len(body.signs) != len(initial.spatial_fields) or len(body.sink) != len(
            initial.spatial_fields
        ):
            raise ValueError("an external body holds one sign and one sink counter per spatial field")
        if any(sign and not initial.spatial_fields[i].rays for i, sign in enumerate(body.signs)):
            raise ValueError("an external body momentum table names ray families")
        if body.coupling == BODY_SINK:
            continue
        if body.coupling == BODY_POLARIZER:
            # ray-polarization-v1: the polarizer names a ray family of the world
            # whose polarization circle its table covers, and a pass Port heading
            # of that family.
            polarizer = body.polarizer
            assert polarizer is not None
            if polarizer.family >= len(initial.spatial_fields):
                raise ValueError("a polarizer polarizes a ray spatial field of the world")
            polarized = initial.spatial_fields[polarizer.family]
            if not polarized.rays or polarizer.family == body.family:
                raise ValueError("a polarizer polarizes a ray spatial field other than its own")
            if polarized.polarization_modulus != polarizer.steps:
                raise ValueError(
                    "a polarizer table has one entry per step of its family's polarization circle"
                )
            if polarizer.pass_heading >= len(polarized.headings) or (
                polarized.headings[polarizer.pass_heading] not in PORT_HEADINGS
            ):
                raise ValueError("a polarizer pass Port is a unit-axial heading of its family")
            continue
        if body.coupling >= len(initial.ray_interactions):
            raise ValueError("an external body coupling names a declared ray interaction")
        rule = initial.ray_interactions[body.coupling]
        own = [role for role in rule.participants if role == (body.family,)]
        if (
            not rule.outputs
            or len(own) != 1
            or any(body.family in role for role in rule.participants if role != (body.family,))
        ):
            raise ValueError(
                "an external body coupling is a meeting with outputs in which one role is the body"
            )
        if rule.outputs.count(body.family) != 1:
            raise ValueError("an external body coupling returns the body once, unchanged")


def validate_thing_ids(initial: InitialState) -> None:
    """The identity of things (bit-law-v1): every disturbance type and every
    external body carries a thing id from 1 below MAX_THING_ID, and every family
    with a shadow set lists its owners, the things whose shadows it carries
    (`family_owners`), which the initial state fills in when the declaration
    leaves them empty."""
    for kind in initial.disturbances:
        if type(kind.thing) is not int or not 1 <= kind.thing < MAX_THING_ID:
            raise ValueError("a disturbance type's thing id is an integer from 1 below the id bound")
    for body in initial.external_bodies:
        if not 1 <= body.thing < MAX_THING_ID:
            raise ValueError("an external body's thing id is an integer from 1 below the id bound")
    for index, definition in enumerate(initial.spatial_fields):
        if not definition.rays or not (definition.spread or definition.release_numerator):
            continue
        expected = family_owners(initial, index)
        if definition.owners != expected:
            raise ValueError(
                f"the family {initial.fields[definition.field].name!r} lists its owners, the things "
                f"whose shadows it carries: {list(expected)} (bit-law-v1)"
            )


def validate_initial_field(initial: InitialState) -> None:
    """The field given with the board (bit-law-v1, `initial_field`): each entry names
    a ray family, a `fill` of at least one interval (the family then declares a
    release, the size of its things' shadow sets), or `rays`, a profile of
    shadows on Nodes of the board with Port headings of the family, each of an
    owner the family lists."""
    for index, entry in initial.initial_field.items():
        if not 0 <= index < len(initial.spatial_fields) or not initial.spatial_fields[index].rays:
            raise ValueError("initial_field names a ray spatial field")
        definition = initial.spatial_fields[index]
        if entry.fill:
            if not definition.release_numerator:
                raise ValueError("an initial_field fill requires a family with a release, a shadow set")
            if not 1 <= entry.fill <= MAX_VALUE:
                raise ValueError("an initial_field fill is a positive bounded number of intervals")
        for ray in entry.rays:
            if any(c >= length for c, length in zip(ray.position, initial.shape, strict=True)):
                raise ValueError("an initial_field ray must be within shape")
            if ray.heading not in PORT_HEADINGS or ray.heading not in definition.headings:
                raise ValueError("an initial_field ray walks a Port heading of its family")
            if not 1 <= ray.amount <= MAX_VALUE:
                raise ValueError("an initial_field ray amount is a positive bounded integer")
            if not 0 <= ray.phase < definition.phase_modulus:
                raise ValueError("an initial_field ray phase is below the family's phase width")
            if ray.sign not in (-1, 0, 1):
                raise ValueError("an initial_field ray sign is -1, 0 or 1")
            if not 0 <= ray.owner < MAX_THING_ID:
                raise ValueError("an initial_field ray owner is a thing id below the id bound")
            if definition.owners and ray.owner not in definition.owners:
                raise ValueError("an initial_field ray owner is one of its family's owners")
            if ray.steps not in (-1, 0, 1):
                raise ValueError(
                    "an initial_field ray has walked one Link (1, the default) or none (0); a "
                    "shadow counts no distance from its owner (return-field-v1)"
                )
            if ray.polarization != POLARIZATION_NONE and not (
                definition.polarization_bits >= 0
                and 0 <= ray.polarization < definition.polarization_modulus
            ):
                raise ValueError(
                    "an initial_field ray polarization is a step of its family's polarization circle"
                )


@dataclass(frozen=True, slots=True)
class InitialShadow:
    """One shadow of a declared profile (`initial_field.rays`): placed at its Node
    as content that arrived on its heading, its steps by default (-1) its Link
    distance from its owner's Node, so that its return arrives where the owner
    was (settled rule (ii) of Highlights 5.4, node-is-ports-v1; for a loop, from
    the owner's Node its line crosses; 1 for an owner with no Node on the
    board), or as declared: 1, one Link walked, spreading there at the first
    cycle, or 0, content leaving the Node at the first cycle, a fresh shadow on
    its way."""

    position: Address3
    heading: Heading
    amount: int
    phase: int = 0
    sign: int = 0
    owner: int = 0
    steps: int = -1
    polarization: int = POLARIZATION_NONE


@dataclass(frozen=True, slots=True)
class InitialFieldDefinition:
    """The field of one family given with the board (bit-law-v1): `fill`, the
    intervals of the split table's transient from every thing of the origin family
    at rest (0 for none), and `rays`, a declared profile."""

    fill: int = 0
    rays: tuple[InitialShadow, ...] = ()


def external_body_names(initial: InitialState) -> list[dict[str, object]]:
    """The declared bodies for the run record, in declaration order."""
    return [
        {
            "index": body.index,
            "thing": body.thing,
            "family": initial.fields[initial.spatial_fields[body.family].field].name,
            "amount": body.amount,
            "charge": body.charge,
            **({"reads": PUSH_READS[body.reads]} if body.reads >= 0 else {}),
            "coupling": (
                "sink"
                if body.coupling == BODY_SINK
                else "polarizer"
                if body.coupling == BODY_POLARIZER
                else initial.ray_interactions[body.coupling].name
            ),
            "initial_position": list(body.position),
            "initial_momentum": list(body.momentum),
            # ray-polarization-v1: the polarizer's declaration, on such a body alone.
            **(
                {}
                if body.polarizer is None
                else {
                    "polarizer": {
                        "family": initial.fields[
                            initial.spatial_fields[body.polarizer.family].field
                        ].name,
                        "angle": body.polarizer.angle,
                        "pass": list(
                            initial.spatial_fields[body.polarizer.family].headings[
                                body.polarizer.pass_heading
                            ]
                        ),
                        "steps": body.polarizer.steps,
                        "unpolarized": body.polarizer.unpolarized,
                    }
                }
            ),
        }
        for body in initial.external_bodies
    ]


def polarization_declared(initial: InitialState) -> bool:
    """Whether the world declares the polarization property anywhere
    (ray-polarization-v1): a family's `polarization_bits`, an emission's
    `polarization`, a rule naming it, or a polarizer body; the runner records the
    identity exactly then, and a world that declares none runs byte-identically."""
    return (
        any(definition.polarization_declared for definition in initial.spatial_fields)
        or any(rule.polarization != POLARIZATION_NONE for rule in initial.emissions)
        or any(rule.polarization_declared for rule in initial.ray_interactions)
        or any(body.polarizer is not None for body in initial.external_bodies)
    )
