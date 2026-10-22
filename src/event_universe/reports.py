"""The node_detectors' reports and the bodies' Nodes (ALGEBRA.md #the-count-is-the-records-share, #readings-and-measurements, #the-click-is-the-meeting; the owner's words, no click names a Node, the node_detector a declared NodeDetector): a node_detector is a region of Nodes declared in the file, a declared NodeDetector that reads the currents through its boundary; its click is its report of one interval, the net current into the region through the NodeDetector's front boundary Ports, in the current's units, with the region's name and the family and never a Node; the credit of quanta to node_detectors is the host's reading by the shares. For a record of several parts (the pair family) the NodeDetector reports beside it the parts' signed level sums over its region each interval, the read the sides' books take (the parts line, `credit.moments_booked`). A body's Nodes, where its family's share stands about its declared Nodes, are derived when a report needs them and never kept. The credit line is the click proper (features/click; HIGHLIGHTS.md, the owner's decision): the NodeDetector's draw written on the lattice at one Node, the credited quantum's share leaving the record there; its result the window, the node_detector's own proper time at the close and the index of its window, the family, the region, the port realised and the parts kept, the count moved and the record's count left, the count conserved and read by the credit, never a Node (the board's interval beside it a diagnostic). The output's words live here and nowhere else in the engine (ENGINE.md, the output): the click line, the parts line and the credit line, one line kind for every click of every reader (the region's credit, a record's absorption and emission alike, never a Node), labelled the node_detector's, the field line, the erasure line, the lay line and the face line, labelled a lattice reading, and the run's end."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import covector, readings
from event_universe.core.ports import PORT_SIDES, PORTS, Wrap, arrival
from event_universe.records import Record

if TYPE_CHECKING:
    from event_universe.lattice import Lattice
    from event_universe.loader.keys import Node
    from event_universe.node_detector import NodeBooks

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
MOMENTUM, FAN, LOST = (
    "momentum",
    "fan",
    "lost",
)  # Part F: the piece's p_a per axis in T's unit, the record's P_a over the board at the click, and what the write books and does not give (None where nothing was lost): the write moves the count and writes nothing for the piece's momentum (ALGEBRA.md, The click's algebra beyond the law)
SOURCE, RECOIL = (
    "source",
    "recoil",
)  # Part G: the piece's source, the emitting body by its number in the world's order or the lay, and the recoil it owes, -p_a per axis as integers, booked and written nowhere (both hands' lines of 2026-10-10, 6091663984 and 6091670073)
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
ORDER, SCALE, BOARD_COUNT = (
    "order",
    "scale",
    "board_count",
)  # the credit line's three words of a record of several parts' click (the owner's word of 2026-10-20, the click writes at the birth): the side's order among the sides' draws, 1 the first to N the last, and the record's scale after the side's write, the norm's square of every coefficient written (`meeting_back.realised`); on no line of a record of one part
CREDIT_KEYS = (
    "window",
    "proper",
    "windows",
    "before",
    "realised",
    "kept",
    "count",
    "left",
    *EXCHANGED,
    MOMENTUM,
    FAN,
    LOST,
    SOURCE,
    RECOIL,
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
END = ("interval", "axis", "side", "largest")  # the keys of the run's lawful end at a receding face
BOOKS = (
    "share",
    "quanta",
    "count",
    "deficit",
    "drift",
    "pace",
    "frozen",
)  # a family's books, a diagnostic


@dataclass(frozen=True)
class NodeDetector:
    """A node_detector: its name, its Nodes (None: the Nodes of the body it names, derived each interval), that body's number, and whether it is a region of the declared NodeDetector (the faces' layer and a body's node_detector are not: each reads its own boundary and takes no field line); it declares no quantum of its own, counting in the record's own unit (`credit.record_unit`)."""

    name: str
    nodes: np.ndarray | None
    body: int | None
    declared: bool


def click(interval: int, family: str, node_detector: str, inflow: int) -> dict[str, object]:
    """The click line, the measurement: the node_detector's report of one interval, the net current into its region through the NodeDetector's front boundary Ports in the current's units (undivided; N over W_c is the host's reading), with the region's name and the family and never a Node, labelled NODEDETECTOR."""
    return dict(
        zip(
            (*REPORT_KEYS, INFLOW),
            (CLICK, MEASUREMENT, interval, family, node_detector, inflow),
            strict=True,
        )
    )


def density(
    interval: int, family: str, node_detector: str, reading: int | None, well: int | None = None
) -> dict[str, object]:
    """The density line, a lattice reading labelled so and no measurement: the family's density over the region this interval; None where a Node of the region is frozen, every Link pace 0, the share not read there (ALGEBRA.md #the-count-is-the-records-share, the frozen Node), and then the frozen Nodes' wells D div T summed, their content reading, as `well`."""
    line = dict(zip(REPORT_KEYS, (DENSITY, DIAGNOSTIC, interval, family, node_detector), strict=True))
    line[READING] = reading
    if well is not None:
        line[WELL] = well
    return line


def parts(interval: int, family: str, node_detector: str, levels: list[list[int]]) -> dict[str, object]:
    """The parts line, the NodeDetector's read of a record of several parts (ALGEBRA.md #the-click-is-the-meeting, the pair's form): per part the signed sums of its two levels over the region at the interval's start, [now, before], labelled NODEDETECTOR with the region's name and never a Node; the sides' books take their second moments from them (`credit.moments_booked`) and the reader its shares (`tools/bell_gate.py`), and nothing is handed over."""
    line = dict(zip(REPORT_KEYS, (PARTS, MEASUREMENT, interval, family, node_detector), strict=True))
    line[LEVELS] = levels
    return line


def credit(
    interval: int,
    family: str,
    node_detector: str,
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
    momentum: list[int] | None = None,
    fan: list[int] | None = None,
    lost: list[str] | None = None,
    source: str | None = None,
    recoil: list[int] | str | None = None,
    order: int | None = None,
    scale: int | None = None,
    board_count: int | None = None,
    bias: list[int] | None = None,
) -> dict[str, object]:
    """The credit line, the one click line kind of every reader (ALGEBRA.md, The NodeDetector is one declaration kind for every experiment; features/click), labelled NODEDETECTOR, the experiment's reading and nothing else (the owner's word: we read only the node_detector's content, the clicks it emits to a file, minding its clock against the board's): the result is the family (the record: the region's credited record, or the clicking record's own for a record declared a NodeDetector), the reader credited or clicking by name (a declared region's, or `body n` for a record declared a NodeDetector, by its number in the world's order), the window [first, last] it was drawn over in the board's intervals, `proper`, the reader's own proper time at the close in whole intervals (its clock the carried sum of its Nodes' composed clocks over the board's intervals, `credit.clocked_regions`, `node_detector.clock_advanced`; the board's `interval` beside it is the board's clock, a diagnostic), `windows`, the index of the window closed, the reader's event clock, the part before and after where the record has parts (`before` and `realised` by their declared names for a record's absorption, emission or probe's click; for a region's credit of a record of several parts `realised` is the port realised with the parts `kept`, the others ended; None for one part), the count moved (one quantum; 0 at the null window's re-lay) and the count left in the books of the record moved (the credited record's; the family `absorbed` from or `emitted` to for a record's click; None where none), the count conserved and read by the credit, and the families exchanged, `absorbed` (the arriving family whose quantum was taken, or the probe's at its click) and `emitted` (the light a whole quantum was given to, or the probe's given back), None where none; Part F (the two hands' lines of 2026-10-09, momentum from Rule3): `momentum`, the piece's p_a per axis in T's unit, the momentum one credited count deposits, the record's lattice momentum at the region's Nodes over its share there times W_rec, read at the close (`node_detector.piece_momentum`; Part F2, both hands' correction: no throughput under this name), `fan`, the record's lattice momentum P_a per axis over the board at the click's interval before the erasure starts (`readings.momentum_of`; their difference the erasure's deficit, measured and not hidden), and `lost`, the readings of what the write books and does not give, in order (`LOST_TO_TAKER`; Part G: `LOST_TO_SOURCE`, `LOST_TO_LAY`, `BOOKED_AT_EMISSION`), None where nothing: the write moves the count by one and writes nothing for the piece's momentum, the recoil of a body held at declared Nodes being the declaration's (ALGEBRA.md, The click's algebra beyond the law); Part G (both hands' lines of 2026-10-10): `source`, the piece's source drawn among the emitters by the quanta each still holds in the record, `body n` by its number in the world's order, or `THE_LAY` where no body emitted it, and `recoil`, the recoil the source owes, -p_a per axis as integers (`take.recoiled`), with `BOOKED_AT_EMISSION` where the directed packet's lay booked it already, and on the emission's own line the packet's recoil booked at the lay (`act.written`), and at a region's credit the word `UNPAID_BY_REGION` with `LOST_TO_REGION` in `lost` (Part H, MUST 5: a region takes no +p and books no recoil to the source, the emitter drawn and named all the same); each None where the click has no such reading; no Node (the owner's word: the reader writes at one Node and gives no result for one Node, the uncertainty principle; the Node written stands in the `lay` and `face` lines, the host's tool's). For a side of a record of several parts the line carries three words more (`ORDER`, `SCALE`, `BOARD_COUNT`; `meeting_back`): the side's order among the sides' draws, 1 the first side to N the last, the record's scale after the side's write (the norm's square of the coefficients standing on its parts, `credit.scale_of`) and the record's count read from the board at the close (`Lattice.count`; ALGEBRA.md, The count on the board, 2026-10-20); on no line of a record of one part, so that every line of such a world stands as built. The null window's re-lay that changed a level writes the same line labelled LATTICE (no `quantum` passed, no measurement), the levels laid in the `lay` lines beside it."""
    label = MEASUREMENT if count else DIAGNOSTIC  # the null window's line (count 0) is the board's
    line = dict(zip(REPORT_KEYS, (CREDIT, label, interval, family, node_detector), strict=True))
    own = (window, proper, windows, before, realised, kept, count, left, absorbed, emitted)
    line.update(zip(CREDIT_KEYS, (*own, momentum, fan, lost, source, recoil), strict=True))
    if (
        order is not None
    ):  # a record of several parts' click: the side's order, the record's scale and its count on the board
        line.update(zip((ORDER, SCALE, BOARD_COUNT), (order, scale, board_count), strict=True))
    if (
        bias is not None and bias[0] * bias[1] > 1
    ):  # the draw's bias bound g / T with its two gcds by name
        line[BIAS_BOUND] = {"g": bias[0] * bias[1], "total": bias[2], "sum": bias[0], "last": bias[1]}
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


def level_sums(nodes: np.ndarray, lines: Sequence[Record]) -> list[list[int]]:
    """Per line of a record, the signed sums of its two levels over a region's Nodes, [now, before], in Python's integers: the parts' read of the parts line, a reading of the lines that writes nothing."""
    return [
        [int(line.now[nodes].sum(dtype=object)), int(line.before[nodes].sum(dtype=object))]
        for line in lines
    ]


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


def end(interval: int, axis: str, side: str, largest: int) -> dict[str, object]:
    """The lawful end, named: the front stands on the layer before the receding face of an axis grown to its largest size after this interval, and the next interval would reflect it."""
    return dict(zip(END, (interval, axis, side, largest), strict=True))


def standing_nodes(declared: np.ndarray, present: np.ndarray, wrap: Wrap) -> np.ndarray:
    """A body's Nodes as a report needs them (ALGEBRA.md #what-a-body-is (c)): the Nodes where its family's share stands in quanta (`present`), connected through the Links to its declared Nodes; the declared Nodes themselves where it stands on none of them; derived and kept nowhere."""
    region = declared & present
    if not bool(region.any()):
        return declared
    while True:
        grown = region.copy()
        for axis in range(3):
            for side in (1, -1):
                grown |= arrival(region, axis, side, wrap, False)
        grown &= present
        if np.array_equal(grown, region):
            return np.asarray(region, dtype=bool)
        region = grown


def ball(shape: tuple[int, ...], centre: Node, radius: int, wrap: Wrap) -> np.ndarray:
    """The Chebyshev ball of a radius about a Node as a mask of the board, the near zone of a bound body (ALGEBRA.md, The click writes on the lattice (5), the reader's ruling of 2026-10-22; `loader/instrument.near_zone`): every Node whose distance per axis is at most the radius, the distance the shorter way round on a periodic axis; its front (`front`) is the light's front, the shell's Ports that exist."""
    grid, found = np.indices(shape), np.ones(shape, dtype=bool)
    for axis, (extent, at) in enumerate(zip(shape, centre, strict=True)):
        distance = np.abs(grid[axis] - at)
        if wrap[axis]:
            distance = np.minimum(distance, extent - distance)
        found &= distance <= radius
    return found


def front(
    nodes: np.ndarray, wrap: Wrap, reader_nodes: np.ndarray, declared: np.ndarray
) -> list[np.ndarray]:
    """Per Port, the Nodes of the region at which that Port is a front boundary Port of the declared NodeDetectors: it leads in from a Node of the declared board outside them (`declared`, the file's own Nodes; the layers a receding face has grown lie beyond the declared board, and what leaves into them has left the world), so a Port between two regions, a Port toward the grown layers and a Port beyond a face are no front."""
    return [
        nodes
        & ~arrival(reader_nodes, axis, side, wrap, True)
        & arrival(declared, axis, side, wrap, False)
        for axis, side in PORT_SIDES
    ]


def region_of(node_detector: NodeDetector, body_nodes: Callable[[int], np.ndarray]) -> np.ndarray:
    """A node_detector's Nodes as a report needs them: its declared Nodes, or the Nodes of the body it names derived now (`body_nodes`, the lattice's reading by the share, `standing`)."""
    if node_detector.body is not None:
        return body_nodes(node_detector.body)
    assert node_detector.nodes is not None  # a node_detector declares its Nodes or names a body
    return node_detector.nodes


def entering(facing: Sequence[np.ndarray], through: tuple[Any, ...]) -> np.ndarray:
    """Per Node of a region, the currents through its front boundary Ports (`facing`, the region's front per Port, `front`, read once per node_detector and interval for every family) summed with their signs, inward positive, in the current's units, 0 at every other Node: the node_detector's report per boundary Node, the shares of the NodeDetector's draw of the one Node it writes (features/click)."""
    seen: Any = 0
    for port in range(PORTS):
        seen = seen + np.where(facing[port], np.asarray(through[port]), 0)
    return np.asarray(seen)


def weighted(
    facing: Sequence[np.ndarray], pieces: Sequence[tuple[tuple[Any, ...], tuple[Any, ...], Any]]
) -> list[np.ndarray]:
    """Per Port and per Node of a region, the conserved form's own current through that front boundary Port (`facing`, the region's front per Port as `entering` reads it), inward positive, 0 at every other Node and Port, six arrays in Port order (their sum at a Node its inflow, the draw's weight; the Port's own the hole's set, `node_detector.arrival_ports`; the click's plan, C6 (i)): per record its current through each front Port times that Link's factor Q_ij, summed over the family's records, `pieces` per record its six currents, its six Links' factors in Port order and its share at the readers' Nodes, at the pair the step starts from (`node_detector.weighed_currents`; the share the passage's, `node_detector.Passage`), in the unit G^2 of the Link's factor and in Python's integers at the front Nodes alone; what a NodeDetector books (`credit.booked`, `node_detector.booked_inflow`; ALGEBRA.md #the-click-is-the-meeting, the credit's booking: num (q_ij / Gamma)^2 (now_i before_j - before_i now_j) through each front Port, the Link's factor squared the one weight, no rounding per Link), equal to the plain current times G^2 where no tension stands on the Link; the click line keeps the plain current, `entering`."""
    seen = [np.zeros(facing[0].shape, dtype=object) for _port in range(PORTS)]
    for through, factors, _shares in pieces:
        for port in range(PORTS):
            at = facing[port]
            flow = np.asarray(through[port])[at].astype(object)
            factor = np.broadcast_to(np.asarray(factors[port]), at.shape)[at].astype(object)
            seen[port][at] += flow * factor
    return seen


def booked_light(board: Lattice, books: NodeBooks, wrap: Wrap, own: np.ndarray) -> None:
    """A bound body's book of its own light through its front (ALGEBRA.md, The click writes on the lattice (5), 2026-10-22: the bound body is a region detector of its own light; one new book, no new act): for each holder of the sign the body's family reads, the holder's light, its record's lines as `Lattice.record` gives them (the sum of its rows), read by `readings.currents_of` at the covector's weights (`covector.weights`, (-3, 1, 1, 1) in thirds under the Lorentz form; the plain time line's current alone where the holder declares none) through the body's front Ports with the holder's Link factors in the unit G^2 (`weighted`, the credit's booking of a drive, inward positive), booked per front Node outward positive into `NodeBooks.light`, the window's sum; nothing for a body whose family reads no holder of the sign."""
    if books.zone is None:  # no near zone: a body with no transition into its part, or no bound body
        return
    facing = front(books.zone, wrap, books.zone, own)  # the light's front, the shell's Ports that exist
    for read in board.families[books.index].reads:
        holder = board.families[read.family]
        if not holder.wronskian:
            continue
        _content, factors = board.read(read.family)
        lines = board.record(read.family)
        current = readings.currents_of(holder.pair[0], lines, wrap, covector.weights(holder), None)
        if not books.light:
            books.light = [0] * len(books.shell)  # per shell Node, the light's front (2026-10-22)
        for through in weighted(facing, [(current, factors, None)]):
            at = np.asarray(through, dtype=object)
            for k, node_at in enumerate(books.shell):
                books.light[k] -= int(
                    at[tuple(c + o for c, o in zip(node_at, board.offset, strict=True))]
                )
