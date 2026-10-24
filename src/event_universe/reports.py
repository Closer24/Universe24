"""The node_detectors' reports and the bodies' Nodes (ALGEBRA.md #the-count-is-the-records-share, #readings-and-measurements, #the-click-is-the-meeting; the owner's words, no click names a Node, the node_detector a declared NodeDetector): a node_detector is a region of Nodes declared in the file, a declared NodeDetector that reads the currents through its boundary; its click is its report of one interval, the net current into the region through the NodeDetector's front boundary Ports, in the current's units, with the region's name and the family and never a Node; the credit of quanta to node_detectors is the host's reading by the shares. For a record of several parts (the pair family) the NodeDetector reports beside it the parts' signed level sums over its region each interval, the read the sides' books take (the parts line, `credit.moments_booked`). A body's Nodes, where its family's share stands about its declared Nodes, are derived when a report needs them and never kept. The credit line is the click proper (features/click; HIGHLIGHTS.md, the owner's decision): the NodeDetector's draw written on the lattice at one Node, the credited quantum's share leaving the record there; its result the window, the node_detector's own proper time at the close and the index of its window, the family, the region, the port realised and the parts kept, the count moved and the record's count left, the count conserved and read by the credit, never a Node (the board's interval beside it a diagnostic). The output's words live here and nowhere else in the engine (ENGINE.md, the output): the click line, the parts line and the credit line, one line kind for every click of every reader (the region's credit, a record's absorption and emission alike, never a Node), labelled the node_detector's, the field line, the erasure line, the lay line and the face line, labelled a lattice reading, and the run's end."""

from __future__ import annotations

from math import gcd
from typing import TYPE_CHECKING, Any

from event_universe.core.rule3 import division_forward

if TYPE_CHECKING:
    pass

MEASUREMENT, DIAGNOSTIC = (
    "NODEDETECTOR",
    "LATTICE",
)  # the labels of the output's lines (ALGEBRA.md #readings-and-measurements)
CLICK, DENSITY, PARTS, CREDIT, ERASURE, LAY, FACE = (
    "click",
    "density",
    "parts",
    "credit",
    "erasure",
    "lay",
    "face",
)  # the output's seven lines: the node_detector's report, the lattice reading, the parts' levels, the click written (every reader's, the region's credit and a record's absorption and emission alike), the front's shell, one line laid at one Node, one value presented at one Port
REPORT_KEYS = ("event", "label", "interval", "family", "node_detector")  # every line's first keys
CONVERSION, INTO, SENSES = (
    "conversion",
    "into",
    "senses",
)  # the conversion line: its event and its own keys, the families of the records out and their senses as laid (conversion.py)
MET = " + "  # the conversion line's `family` where several families' quanta met at one Node: their names joined (conversion.line)
INFLOW, READING, WELL, LEVELS = ("inflow", "reading", "well", "levels")  # the lines' own keys
EXCHANGED = (
    "absorbed",
    "emitted",
)  # the families a record's click exchanged a quantum with, None where none
MOMENTUM, LOST = (
    "momentum",
    "lost",
)  # the momentum as the click's view reads it (2026-10-24, meeting_board.readings_at): per axis [sign_a, num_a, den_a], the frame's running cosine along the axis, 2 cos k_a = (a_{+a} + a_{-a}) / a_i, as the reduced pair with the Link current's sign, p_a = T sin k_a per Link (ALGEBRA.md, The lattice momentum, Part F), None at a level now 0; and what the write books and does not give (None where nothing was lost): the write moves the count and writes nothing for the piece's momentum (ALGEBRA.md, The click's algebra beyond the law). The former keys `fan` (the record's P_a over the whole board at the click) and `recoil` (-p_a owed by the source, Part G) struck from the credit line on 2026-10-24: no click reads the board (the click reads the Node and its six neighbours, the owner's rule of the local law), and the recoil is -p, redundant with the momentum
SOURCE = "source"  # Part G: the piece's source, the emitting body by its number in the world's order or the lay (both hands' lines of 2026-10-10, 6091663984 and 6091670073); the recoil it owed had its own key to 2026-10-24 (`MOMENTUM`)
WRITTEN_AS_PHASE = "P written as the part's phase"  # the recoil as the per-Node phase (2026-10-21): the piece's P written into the entered part over a bound record of two Nodes or more standing free in its well as the phase k . (x - c) per Node (`act.parted`, `take.recoil_phases`), the light's piece gone with the hole; a body held at declared Nodes keeps `LOST_TO_TAKER`
LOST_TO_TAKER = "P lost to the taker"  # Part F: the piece's P booked on the credit line and written into no part, the recoil of a body held at declared Nodes the declaration's (the two hands' lines of 2026-10-09); Part F2 dropped the pair's "no back-to-back region", a declared tolerance's miss: the two pieces' p stand in their two credit lines and the test judges their sum against the lays' floor
LOST_TO_SOURCE, LOST_TO_LAY, BOOKED_AT_EMISSION = (
    "recoil lost to the source",
    "recoil lost to the lay",
    "recoil booked at the emission",
)  # Part G: the source's three readings in `lost` (both hands): the recoil owed by a body booked and written into no part, no body emitted the piece (the file's lay, no receiver), or the recoil booked at the lay, the directed packet's emission line (`emission.laid_packet`, the direction drawn there; `act.written`)
THE_LAY = "the lay"  # Part G: the `source` of a piece no body emitted, the file's lay (one_photon, the two slits, bell)
LOST_TO_REGION, UNPAID_BY_REGION = (
    "P lost to the region",
    "unpaid by the region",
)  # Part H, MUST 5 (both hands' lines of 2026-10-10 on the whole trial): a region taker (the two slits' screens, bell's sides) has no part of its own, so it takes no +p and books no recoil to the source: `lost` reads the piece's P lost to the region and `recoil` the one word, unpaid, the emitter still drawn and its outstanding count down by one (`lists.credited_node`, `take.unpaid`); the region's +p OPEN by name
NO_DRAW = "no draw: every digit at the lay's origin, the emission at the window's close"  # the exact dark (the reader's re-ruling of 2026-10-20, (c)): a body whose read finds every digit at the lay's origin at its emission's draw does not draw; its emission falls at its window's close, the detector's declared when, this reading on its credit line
BIAS_BOUND = "bias_bound"  # the click's line: the bound g / T of the read's first draw, the reader's F, 2026-10-20
NO_SIDE = "no side: booked, not faced"  # C6: the hole's Node two-sided on every axis, its face set empty, the quantum taken in the books by the deficit path and the levels standing (`take.faced`, `act.written`)
LARGEST_ENTRY = "the where by the largest raw entry of the shell's book: every shell Node below G^2 while the row fell"  # (5), the reader's word of 04:21: no weight, no draw, the reading named; the first of a tie (max over the range takes the first index; the reachable tie the all-zero book, the where then the shell's first Node by order)
ORDER, SCALE, BOARD_COUNT = (
    "order",
    "scale",
    "board_count",
)  # the credit line's three words of a record of several parts' click (the owner's word of 2026-10-20, the click writes at the birth): the side's order among the sides' draws, 1 the first to N the last, and the record's scale after the side's write, the norm's square of every coefficient written (`meeting_back.realised`); on no line of a record of one part
PROPER, WINDOWS = (
    "proper",
    "windows",
)  # the taker's own clock at the close in whole intervals and its count of its own closes: constants 0 on the board's own click to 2026-10-24, readings since (the click's view, meeting_board.readings_at; ALGEBRA.md, The paces compose, The clock near matter)
CREDIT_KEYS = (
    "window",
    PROPER,
    WINDOWS,
    "before",
    "realised",
    "kept",
    "count",
    "left",
    *EXCHANGED,
    MOMENTUM,
    LOST,
    SOURCE,
)  # the credit line's own keys, the one click line kind's
ERASURE_KEYS = ("origin", "distance", "nodes", "take", "unit")  # the erasure line's own keys
LINE, BEFORE, AFTER, PORT_SET, VALUE = (
    "line",
    "before",
    "after",
    "ports",
    "value",
)  # the two acts' words
LAY_KEYS = (
    LINE,
    BEFORE,
    AFTER,
    "node",
)  # the lay line's own keys: the line laid, its levels before and after
FACE_KEYS = (
    LINE,
    PORT_SET,
    VALUE,
    "node",
)  # the face line's own keys: the line, the Ports and the value presented
BODY = "body"  # a NodeDetector with a record of its own in the output, by its number among the world's bodies
AT = "at"  # the one Node written, a lattice diagnostic beside the credit's result
OUTPUT = (
    *REPORT_KEYS,
    INFLOW,
    READING,
    WELL,
    LEVELS,
    *CREDIT_KEYS,
    *ERASURE_KEYS,
    *LAY_KEYS[:3],
    PORT_SET,
    VALUE,
)  # the lines' keys
PORT_NAMES = ("plus", "minus")  # the two ports of a side in the credit line, the + port first
BOOKS = (
    "share",
    "quanta",
    "count",
    "deficit",
    "drift",
    "pace",
    "frozen",
)  # a family's books, a diagnostic


def credit(
    interval: int,
    family: str,
    node_detector: object,  # the reader's name, or the Node's x-major index for the board's own report
    window: list[int],
    proper: int,
    windows: int,
    realised: str | None,
    kept: list[int] | None,
    count: int,
    left: int | None,
    before: str | None = None,
    absorbed: str | None = None,
    emitted: str | None = None,
    momentum: object = None,
    lost: list[str] | None = None,
    source: str | None = None,
    order: int | None = None,
    scale: int | None = None,
    board_count: int | None = None,
    bias: list[int] | None = None,
    readings: dict[str, object] | None = None,
) -> dict[str, object]:
    """The credit line, the one click line kind of every reader (ALGEBRA.md, The NodeDetector is one declaration kind for every world; features/click), labelled NODEDETECTOR, the world's reading and nothing else (the owner's word: we read only the node_detector's content, the clicks it emits to a file, minding its clock against the board's): the result is the family (the record: the region's credited record, or the clicking record's own for a record declared a NodeDetector), the reader credited or clicking by name (a declared region's, or `body n` for a record declared a NodeDetector, by its number in the world's order), the window [first, last] it was drawn over in the board's intervals, `proper`, the reader's own proper time at the close in whole intervals (its clock the carried sum of its Nodes' composed clocks over the board's intervals, `credit.clocked_regions`, `node_detector.clock_advanced`; the board's `interval` beside it is the board's clock, a diagnostic), `windows`, the index of the window closed, the reader's event clock, the part before and after where the record has parts (`before` and `realised` by their declared names for a record's absorption, emission or probe's click; for a region's credit of a record of several parts `realised` is the port realised with the parts `kept`, the others ended; None for one part), the count moved (one quantum; 0 at the null window's re-lay) and the count left in the books of the record moved (the credited record's; the family `absorbed` from or `emitted` to for a record's click; None where none), the count conserved and read by the credit, and the families exchanged, `absorbed` (the arriving family whose quantum was taken, or the probe's at its click) and `emitted` (the light a whole quantum was given to, or the probe's given back), None where none; Part F (the two hands' lines of 2026-10-09, momentum from Rule3) as the click's view reads it (2026-10-24, `meeting_board.readings_at`): `momentum`, the frame's running cosine along each axis, 2 cos k_a = (a_{+a} + a_{-a}) / a_i, with the Link current's sign, p_a = T sin k_a per Link, per axis [sign_a, num_a, den_a] (the reduced pair as the point's, den above 0, the lines' pairs in order where they differ), None at a level now 0; `lost`, the readings of what the write books and does not give, in order (`LOST_TO_TAKER`; Part G: `LOST_TO_SOURCE`, `LOST_TO_LAY`, `BOOKED_AT_EMISSION`), None where nothing: the write moves the count by one and writes nothing for the piece's momentum, the recoil of a body held at declared Nodes being the declaration's (ALGEBRA.md, The click's algebra beyond the law); Part G (both hands' lines of 2026-10-10): `source`, the piece's source drawn among the emitters by the quanta each still holds in the record, `body n` by its number in the world's order, or `THE_LAY` where no body emitted it; the former keys `fan` (the record's P_a over the whole board at the close, `readings.momentum_of`) and `recoil` (-p_a owed by the source, `take.recoiled`, with the words `BOOKED_AT_EMISSION` and `UNPAID_BY_REGION`) struck from the line on 2026-10-24: no click reads the board (the click reads the Node and its six neighbours, the owner's rule of the local law), and the recoil is -p, redundant with the momentum; each None where the click has no such reading; no Node (the owner's word: the reader writes at one Node and gives no result for one Node, the uncertainty principle; the Node written stands in the `lay` and `face` lines, the host's tool's). For a side of a record of several parts the line carries three words more (`ORDER`, `SCALE`, `BOARD_COUNT`; `meeting_back`): the side's order among the sides' draws, 1 the first side to N the last, the record's scale after the side's write (the norm's square of the coefficients standing on its parts, `credit.scale_of`) and the record's count read from the board at the close (`Lattice.count`; ALGEBRA.md, The count on the board, 2026-10-20); on no line of a record of one part, so that every line of such a world stands as built. The null window's re-lay that changed a level writes the same line labelled LATTICE (no `quantum` passed, no measurement), the levels laid in the `lay` lines beside it."""
    label = MEASUREMENT if count else DIAGNOSTIC  # the null window's line (count 0) is the board's
    line = dict(zip(REPORT_KEYS, (CREDIT, label, interval, family, node_detector), strict=True))
    own = (window, proper, windows, before, realised, kept, count, left, absorbed, emitted)
    line.update(zip(CREDIT_KEYS, (*own, momentum, lost, source), strict=True))
    if (
        order is not None
    ):  # a record of several parts' click: the side's order, the record's scale and its count on the board
        line.update(zip((ORDER, SCALE, BOARD_COUNT), (order, scale, board_count), strict=True))
    if (
        bias is not None and bias[0] * bias[1] > 1
    ):  # the draw's bias bound g / T with its two gcds by name
        line[BIAS_BOUND] = {"g": bias[0] * bias[1], "total": bias[2], "sum": bias[0], "last": bias[1]}
    if readings is not None:  # the click's view, the six readings (`READINGS`, 2026-10-24)
        line.update(readings)
    return line


def lay(
    interval: int, family: str, line: int, node: list[int], before: list[int], after: list[int]
) -> dict[str, object]:
    """The lay line, one line of a record laid at one Node by an act from outside the Node (src/event_universe/act.py, `written`: the absorption's and the emission's lays of the record's parts, the emitted quantum's lay on light's record, the null window's re-lay; the mathematician's hand, the lay's part crossed from its line), labelled LATTICE, a diagnostic for the host's tool and no result: the interval, the record's family, no node_detector, the line's number among the family's lines, its levels [now, before, remainder] at the Node before the lay and after it, and the one Node under `node`; written where the lay changed one of the three, so that `tools/back_in_time.py` sets the line back before its step back and Rule3's inverse crosses the lay."""
    found: dict[str, object] = dict(
        zip(REPORT_KEYS, (LAY, DIAGNOSTIC, interval, family, None), strict=True)
    )
    written: dict[str, object] = {OUTPUT[1]: DIAGNOSTIC, AT: node}
    found.update(zip(LAY_KEYS, (line, before, after, written), strict=True))
    return found


def face(
    interval: int, family: str, line: int, node: list[int], ports: list[int], value: int
) -> dict[str, object]:
    """The face line, one value presented at the Ports of one Node's set for one interval's step (features/click, `Face`; the mathematician's hand with the advisor's second, the face value logged per line per interval; the click's plan, C6: the set in place of one Port), labelled LATTICE, a diagnostic for the host's tool and no result: the interval at whose step it is presented, the record's family, no node_detector, the line, the Ports, the set in Port order, and the value Rule3 read through each of them in the place of the neighbour's level (the click's hole and the front's shells alike), the one Node under `node`; the inverse presents the same value at the same Ports, so the tool crosses the click from the lines and not from the books' log."""
    found: dict[str, object] = dict(
        zip(REPORT_KEYS, (FACE, DIAGNOSTIC, interval, family, None), strict=True)
    )
    found.update(zip(FACE_KEYS, (line, ports, value, {OUTPUT[1]: DIAGNOSTIC, AT: node}), strict=True))
    return found


def erasure(
    interval: int, family: str, origin: list[int], distance: int, nodes: int, take: int, unit: int
) -> dict[str, object]:
    """The erasure line, the front's shell of one interval (src/event_universe/front.py; the owner's word, the past going out at the speed of light), labelled LATTICE, a diagnostic beside the click line for the host's tool and no result: the interval, the clicked record's family, the click's Node at the file's coordinates (`origin`), the shell's Link-metric distance from it, the shell's Nodes, the record's share standing on the shell as the front reaches it in the current's units (`take`, what the shell's faces book for removal) and the record's quantum W_rec (`unit`), so that take over unit is the faces' take in quanta."""
    line: dict[str, object] = dict(
        zip(REPORT_KEYS, (ERASURE, DIAGNOSTIC, interval, family, None), strict=True)
    )
    for key, value in zip(ERASURE_KEYS, (origin, distance, nodes, take, unit), strict=True):
        line[key] = value
    return line


def book(
    share: int | None,
    quanta: int | None,
    count: int,
    deficit: int,
    drift: int | None,
    pace: int,
    frozen: int,
) -> dict[str, int | None]:
    """A family's books, a lattice diagnostic: its share summed over the lattice in the current's units, the same in quanta over W_c, its count in the credit's books, its deficit, the quanta taken from the record and written nowhere (the undepleted beam, `take.faced`, the absorptions' count times one quantum: the board's share in quanta stands above the books' count by it, the three compared at every reading), the share's drift from the one the world started with (share, quanta and drift None where a Node is frozen: the share is not read there and no number is invented), the least Node pace Gamma - 2 c_i of the final state and the count of the frozen Nodes."""
    return dict(zip(BOOKS, (share, quanta, count, deficit, drift, pace, frozen), strict=True))


BORN_KEYS = (
    "records",
    "points",
)  # the birth line's children's records and points, the click's view of the birth (2026-10-24)
READINGS = (
    "point",
    "kind",
    "sense",
    "support",
    "beat",
    "identity",
)  # the click's view, the six new readings on the credit line (2026-10-24, the owner's frame: the Nodes are the event space, the clicks are what is seen from the hidden layer, all measurements go to the clicks; the builder's six, accepted as readings and no act): the point the credited record's cosine at the credited Node read from its three levels around the step, the kind the rank of the lines credited, the sense the Wronskian's sign there, the support the shell Node the credit left through, the beat W_rec of the point read (3 T den sin omega, the quantum's own wall), the identity the record's family and index; with them the credit line's former keys read and no longer constants on the board's own click: MOMENTUM (the frame's running cosine along each axis, 2 cos k_a = (a_{+a} + a_{-a}) / a_i, with the Link current's sign, p_a = T sin k_a per Link, Part F, per axis [sign_a, num_a, den_a], meeting_board.readings_at; the same day's former form, the law's region formula at the one Node, P_a(region) x W_rec div (num x W(region)), a one-Node ratio bounded by nothing, struck on 2026-10-24 with the fan, the record's P_a over the whole board, which no click reads, and the recoil, -p, redundant) and PROPER (the taker's own clock at the close in whole intervals, with WINDOWS its count of its own closes), eight readings beyond the labels (meeting_board.readings_at)


def point_of(before: int, now: int, after: int) -> tuple[int, int] | None:
    """The point a line's three levels around one step read at a Node, as the reduced pair (num, den) of the cosine of its rotation: Rule3's line at a mode of frequency omega has a_next + a_before = 2 cos omega a_now, so 2 cos omega = (after + before) / now and the pair is (after + before, 2 now) over their greatest common divisor, den above 0 (the massless uniform mode's double root (1, 1); a mode above the band or below it num beyond den); None where the level now is 0, the cosine not read there. One of the six readings of the click's view (`READINGS`), the point of the family's quantum as the click sees it, beside the family's label."""
    if now == 0:
        return None
    num, den = after + before, 2 * now
    if den < 0:
        num, den = -num, -den
    common = gcd(abs(num), den)
    return int(division_forward(num, common, 0)[0]), int(division_forward(den, common, 0)[0])


def birth_line(
    interval: int,
    family: str,
    children: list[str],
    senses: list[int],
    nodes: tuple[Any, ...],
    records: list[int] | None = None,
    points: list[list[int]] | None = None,
) -> dict[str, object]:
    """The birth line, the reading of the sentence's act beside the credit's (ALGEBRA.md, Matter's birth from light; act.py): the interval, the gapless family met, the children's families and senses and the Nodes, never a rate."""
    line = {"event": "birth", "label": "NODEDETECTOR", "interval": interval, "family": family}
    found = {**line, "children": children, "senses": senses, "nodes": [list(node) for node in nodes]}
    if (
        records is not None
    ):  # the children's records and points, the click's view of the birth (2026-10-24)
        found.update(zip(BORN_KEYS, (records, points), strict=True))
    return found
