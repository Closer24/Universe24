"""The node_readers' reports and the bodies' Nodes (ALGEBRA.md #the-count-is-the-records-share, #readings-and-measurements, #the-click-is-the-meeting; the owner's words, no click names a Node, the node_reader a declared NodeReader): a node_reader is a region of Nodes declared in the file, a declared NodeReader that reads the currents through its boundary; its click is its report of one interval, the net current into the region through the reader's front boundary Ports, in the current's units, with the region's name and the family and never a Node; the credit of quanta to node_readers is the host's reading by the shares. For a record of several parts (the pair family) the NodeReader reports beside it the parts' signed level sums over its region each interval, the read the credit pairs through the root (the parts line). A body's Nodes, where its family's share stands about its declared Nodes, are derived when a report needs them and never kept. The credit line is the click proper (features/click; HIGHLIGHTS.md, the owner's decision): the NodeReader's draw written on the GameBoard at one Node, the credited quantum's share leaving the record there; its result the window, the node_reader's own proper time at the close and the index of its window, the family, the region, the port realised and the parts kept, the count moved and the record's count left, the count conserved and read by the credit, never a Node (the board's tick beside it a diagnostic). The output's words live here and nowhere else in the engine (ENGINE.md, the output): the click line, the parts line and the credit line, one line kind for every click of every reader (the region's credit, a record's taking and giving alike, never a Node), labelled the node_reader's, the field line, the erasure line, the lay line and the face line, labelled a GameBoard reading, and the run's end."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np

from event_universe.core.ports import PORT_SIDES, PORTS, Wrap, arrival
from event_universe.node import Record

MEASUREMENT, DIAGNOSTIC = (
    "NODEREADER",
    "GAMEBOARD",
)  # the labels of the output's lines (ALGEBRA.md #readings-and-measurements)
CLICK, DENSITY, PARTS, CREDIT, ERASURE, LAY, FACE, CONVERSION = (
    "click",
    "density",
    "parts",
    "credit",
    "erasure",
    "lay",
    "face",
    "conversion",
)  # the output's eight lines: the node_reader's report, the GameBoard reading, the parts' levels, the click written (every reader's, the region's credit and a record's taking and giving alike), the front's shell, one line laid at one Node, one value presented at one Port, a record converted whole at its Node
REPORT_KEYS = ("event", "label", "tick", "family", "node_reader")  # every line's first keys
INFLOW, READING, WELL, LEVELS = ("inflow", "reading", "well", "levels")  # the lines' own keys
EXCHANGED = ("taken", "given")  # the families a record's click exchanged a quantum with, None where none
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
)  # the credit line's own keys, the one click line kind's
ERASURE_KEYS = ("origin", "distance", "nodes", "taken")  # the erasure line's own keys
INTO = "into"  # the conversion line's own key, the families of the records out
CONVERSION_KEYS = ("window", INTO, "node")  # the conversion line's keys
LINE, BEFORE, AFTER, PORT, VALUE = ("line", "before", "after", "port", "value")  # the two acts' words
LAY_KEYS = (
    LINE,
    BEFORE,
    AFTER,
    "node",
)  # the lay line's own keys: the line laid, its levels before and after
FACE_KEYS = (
    LINE,
    PORT,
    VALUE,
    "node",
)  # the face line's own keys: the line, the Port and the value presented
BODY = (
    "body"  # a NodeReader with a record of its own in the output, by its number among the world's bodies
)
AT = "at"  # the one Node written, a GameBoard diagnostic beside the credit's result
OUTPUT = (
    *REPORT_KEYS,
    INFLOW,
    READING,
    WELL,
    LEVELS,
    *CREDIT_KEYS,
    *ERASURE_KEYS,
    *LAY_KEYS[:3],
    PORT,
    VALUE,
    INTO,
)  # the lines' keys
PORT_NAMES = ("plus", "minus")  # the two ports of a side in the credit line, the + port first
END = ("interval", "axis", "side", "largest")  # the keys of the run's lawful end at a receding face
BOOKS = ("share", "quanta", "drift", "pace", "frozen")  # the keys of a family's books, a diagnostic


@dataclass(frozen=True)
class NodeReader:
    """A node_reader: its name, its Nodes (None: the Nodes of the body it names, derived each interval), that body's number, and whether it is a region of the declared NodeReader (the faces' layer and a body's node_reader are not: each reads its own boundary and takes no field line); it declares no quantum of its own, counting in the record's own unit (`credit.record_unit`)."""

    name: str
    nodes: np.ndarray | None
    body: int | None
    declared: bool


def click(tick: int, family: str, node_reader: str, inflow: int) -> dict[str, object]:
    """The click line, the measurement: the node_reader's report of one interval, the net current into its region through the reader's front boundary Ports in the current's units (undivided; N over W_c is the host's reading), with the region's name and the family and never a Node, labelled NODEREADER."""
    return dict(
        zip((*REPORT_KEYS, INFLOW), (CLICK, MEASUREMENT, tick, family, node_reader, inflow), strict=True)
    )


def density(
    tick: int, family: str, node_reader: str, reading: int | None, well: int | None = None
) -> dict[str, object]:
    """The field line, a GameBoard reading labelled so and no measurement: the family's density over the region this interval; None where a Node of the region is frozen, every Link pace 0, the share not read there (ALGEBRA.md #the-count-is-the-records-share, the frozen Node), and then the frozen Nodes' wells D div T summed, their content reading, as `well`."""
    line = dict(zip(REPORT_KEYS, (DENSITY, DIAGNOSTIC, tick, family, node_reader), strict=True))
    line[READING] = reading
    if well is not None:
        line[WELL] = well
    return line


def parts(tick: int, family: str, node_reader: str, levels: list[list[int]]) -> dict[str, object]:
    """The parts line, the NodeReader's read of a record of several parts (ALGEBRA.md #the-click-is-the-meeting, the pair's form): per part the signed sums of its two levels over the region at the interval's start, [now, before], labelled NODEREADER with the region's name and never a Node; the credit pairs each part with the same part through the root and squares (the reader, `tools/bell_gate.py`), and nothing is handed over."""
    line = dict(zip(REPORT_KEYS, (PARTS, MEASUREMENT, tick, family, node_reader), strict=True))
    line[LEVELS] = levels
    return line


def credit(
    tick: int,
    family: str,
    node_reader: str,
    window: list[int],
    proper: int,
    windows: int,
    realised: str | None,
    kept: list[int] | None,
    count: int,
    left: int | None,
    before: str | None = None,
    taken: str | None = None,
    given: str | None = None,
) -> dict[str, object]:
    """The credit line, the one click line kind of every reader (ALGEBRA.md, The NodeReader is one declaration kind for every experiment; features/click), labelled NODEREADER, the experiment's reading and nothing else (the owner's word: we read only the node_reader's content, the clicks it emits to a file, minding its clock against the board's): the result is the family (the record: the region's credited record, or the clicking record's own for a record declared a reader), the reader credited or clicking by name (a declared region's, or `body n` for a record declared a reader, by its number in the world's order), the window [first, last] it was drawn over in the board's intervals, `proper`, the reader's own proper time at the close in whole intervals (its clock the carried sum of its Nodes' composed clocks over the board's ticks, `credit.clocked_regions`, `node_reader.clock_advanced`; the board's `tick` beside it is the board's clock, a diagnostic), `windows`, the index of the window closed, the reader's event clock, the part before and after where the record has parts (`before` and `realised` by their declared names for a record's taking, giving or probe's click; for a region's credit of a record of several parts `realised` is the port realised with the parts `kept`, the others ended; None for one part), the count moved (one quantum; 0 at the null window's re-lay) and the count left in the books of the record moved (the credited record's; the family `taken` from or `given` to for a record's click; None where none), the count conserved and read by the credit, and the families exchanged, `taken` (the arriving family whose quantum was taken, or the probe's at its click) and `given` (the light a whole quantum was given to, or the probe's given back), None where none; no Node (the owner's word: the reader writes at one Node and gives no result for one Node, the uncertainty principle; the Node written stands in the `lay` and `face` lines, the host's tool's). The null window's re-lay that changed a level writes the same line labelled GAMEBOARD (no `quantum` passed, no measurement), the levels laid in the `lay` lines beside it."""
    label = MEASUREMENT if count else DIAGNOSTIC  # the null window's line (count 0) is the board's
    line = dict(zip(REPORT_KEYS, (CREDIT, label, tick, family, node_reader), strict=True))
    own = (window, proper, windows, before, realised, kept, count, left, taken, given)
    line.update(zip(CREDIT_KEYS, own, strict=True))
    return line


def conversion(
    tick: int, family: str, body: int, window: list[int], into: list[str], node: list[int]
) -> dict[str, object]:
    """The conversion line, the click of a record converted whole at its one Node (the fifth list of the act, ALGEBRA.md, A family's declaration, item 5; the two hands on the table, the rate and the lay; src/event_universe/conversion.py), labelled NODEREADER: the interval, the record's family (the record in, its count down by one), the reader by its number among the world's `bodies`, the window [first, last] drawn over and `into`, the families of the records out in the table's order, each up by one whole quantum laid at the Node by the count; beside the result, under `node` and labelled GAMEBOARD, the one Node written at the file's coordinates, a diagnostic for the host's tool; the lay lines of the write beside it."""
    line = dict(zip(REPORT_KEYS, (CONVERSION, MEASUREMENT, tick, family, f"{BODY} {body}"), strict=True))
    written = {OUTPUT[1]: DIAGNOSTIC, AT: node}
    line.update(zip(CONVERSION_KEYS, (window, into, written), strict=True))
    return line


def lay(
    tick: int, family: str, line: int, node: list[int], before: list[int], after: list[int]
) -> dict[str, object]:
    """The lay line, one line of a record laid at one Node by an act from outside the Node (src/event_universe/meeting.py, `written`: the taking's and the giving's lays of the record's parts, the given quantum's lay on light's record, the null window's re-lay; the mathematician's hand, the lay's part crossed from its line), labelled GAMEBOARD, a diagnostic for the host's tool and no result: the interval, the record's family, no node_reader, the line's number among the family's lines, its levels [now, before, remainder] at the Node before the lay and after it, and the one Node under `node`; written where the lay changed one of the three, so that `tools/back_in_time.py` sets the line back before its step back and Rule3's inverse crosses the lay."""
    found: dict[str, object] = dict(zip(REPORT_KEYS, (LAY, DIAGNOSTIC, tick, family, None), strict=True))
    written: dict[str, object] = {OUTPUT[1]: DIAGNOSTIC, AT: node}
    found.update(zip(LAY_KEYS, (line, before, after, written), strict=True))
    return found


def face(tick: int, family: str, line: int, node: list[int], port: int, value: int) -> dict[str, object]:
    """The face line, one value presented at one Port of one Node for one interval's step (features/click, `Face`; the mathematician's hand with the advisor's second, the face value logged per line per interval), labelled GAMEBOARD, a diagnostic for the host's tool and no result: the interval at whose step it is presented, the record's family, no node_reader, the line, the Port in Port order and the value Rule3 read there in the place of the neighbour's level (the click's hole and the front's shells alike), the one Node under `node`; the inverse presents the same value, so the tool crosses the click from the lines and not from the books' log."""
    found: dict[str, object] = dict(
        zip(REPORT_KEYS, (FACE, DIAGNOSTIC, tick, family, None), strict=True)
    )
    found.update(zip(FACE_KEYS, (line, port, value, {OUTPUT[1]: DIAGNOSTIC, AT: node}), strict=True))
    return found


def erasure(
    tick: int, family: str, origin: list[int], distance: int, nodes: int, taken: int
) -> dict[str, object]:
    """The erasure line, the front's shell of one interval (src/event_universe/front.py; the owner's word, the past going out at the speed of light), labelled GAMEBOARD, a diagnostic beside the click line for the host's tool and no result: the interval, the clicked record's family, the click's Node at the file's coordinates (`origin`), the shell's Link-metric distance from it, the shell's Nodes and the levels taken there, the sum of the sizes of the record's two levels over the shell."""
    line: dict[str, object] = dict(
        zip(REPORT_KEYS, (ERASURE, DIAGNOSTIC, tick, family, None), strict=True)
    )
    for key, value in zip(ERASURE_KEYS, (origin, distance, nodes, taken), strict=True):
        line[key] = value
    return line


def level_sums(nodes: np.ndarray, lines: Sequence[Record]) -> list[list[int]]:
    """Per line of a record, the signed sums of its two levels over a region's Nodes, [now, before], in Python's integers: the parts' read of the parts line, a reading of the lines that writes nothing."""
    return [
        [int(line.now[nodes].sum(dtype=object)), int(line.before[nodes].sum(dtype=object))]
        for line in lines
    ]


def book(
    share: int | None, quanta: int | None, drift: int | None, pace: int, frozen: int
) -> dict[str, int | None]:
    """A family's books, a GameBoard diagnostic: its share summed over the GameBoard in the current's units, the same in quanta over W_c, the share's drift from the one the world started with (the three None where a Node is frozen: the share is not read there and no number is invented), the least Node pace Gamma - 2 c_i of the final state and the count of the frozen Nodes."""
    return dict(zip(BOOKS, (share, quanta, drift, pace, frozen), strict=True))


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


def front(
    nodes: np.ndarray, wrap: Wrap, reader_nodes: np.ndarray, declared: np.ndarray
) -> list[np.ndarray]:
    """Per Port, the Nodes of the region at which that Port is a front boundary Port of the declared NodeReaders: it leads in from a Node of the declared board outside them (`declared`, the file's own Nodes; the layers a receding face has grown lie beyond the declared board, and what leaves into them has left the world), so a Port between two regions, a Port toward the grown layers and a Port beyond a face are no front."""
    return [
        nodes
        & ~arrival(reader_nodes, axis, side, wrap, True)
        & arrival(declared, axis, side, wrap, False)
        for axis, side in PORT_SIDES
    ]


def region_of(node_reader: NodeReader, body_nodes: Callable[[int], np.ndarray]) -> np.ndarray:
    """A node_reader's Nodes as a report needs them: its declared Nodes, or the Nodes of the body it names derived now (`body_nodes`, the GameBoard's reading by the share, `standing`)."""
    if node_reader.body is not None:
        return body_nodes(node_reader.body)
    assert node_reader.nodes is not None  # a node_reader declares its Nodes or names a body
    return node_reader.nodes


def entering(facing: Sequence[np.ndarray], through: tuple[Any, ...]) -> np.ndarray:
    """Per Node of a region, the currents through its front boundary Ports (`facing`, the region's front per Port, `front`, read once per node_reader and interval for every family) summed with their signs, inward positive, in the current's units, 0 at every other Node: the node_reader's report per boundary Node, the shares of the NodeReader's draw of the one Node it writes (features/click)."""
    seen: Any = 0
    for port in range(PORTS):
        seen = seen + np.where(facing[port], np.asarray(through[port]), 0)
    return np.asarray(seen)


def inflow(
    nodes: np.ndarray,
    through: tuple[Any, ...],
    wrap: Wrap,
    reader_nodes: np.ndarray,
    declared: np.ndarray,
) -> int:
    """A node_reader's report of one interval, its click (ALGEBRA.md #the-count-is-the-records-share; the owner's words, no click names a Node, the node_reader a declared NodeReader): the currents through the reader's front boundary Ports at the region's Nodes (`entering`), inward positive, summed in integers with their signs, the density that entered the region from the declared board (the advisor's correction: the front Links only, net; the transverse Links inside the declared NodeReader and the Links toward a receding face's grown layers not counted); the host's reading for the credit by the shares. `reader_nodes` is the union of the declared regions (a body's node_reader and the faces' layer their own Nodes), so that what passes between the regions of one screen is not seen twice; nothing is handed over and no line names a Node."""
    return int(entering(front(nodes, wrap, reader_nodes, declared), through).sum(dtype=object))
