"""The take, the act's readings and items (the law's word for the act its contents serve, the module so named on 2026-10-21, twist.py until then; the engine V2, Parts F and G; ALGEBRA.md, The click's algebra beyond the law, The lattice momentum, The click's momentum on the board; the owner's rule, at the Nodes Rule3 only): the taker's part re-laid at each Node's own direction (`relaid`, `levels_at`), the click's items (`Item`, `Phase`, `books_named`), the hole's faces (`faced`, `faces_presented`, `faces_reported`), the piece's momentum readings (`fan_momentum`, `scaled`) and the piece's source drawn among the emitters by the quanta each holds and named with the recoil it owes, -p_a as integers on the credit line and written nowhere (`recoiled`, `drawn_emitter`), the loss booked by name (`unpaid`); the write moves the count by one and writes nothing for the piece's momentum, the recoil of a body held at declared Nodes being the declaration's; meeting.py writes the click with them."""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import TYPE_CHECKING

from event_universe.features.click import Face
from event_universe.front import framed_record
from event_universe.loader.keys import Node
from event_universe.plane import Faces
from event_universe.reports import (
    face,
)

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


@dataclass(frozen=True)
class Item:
    """One entry of a click's list (the mathematician's hand with the advisor's second, two hands; the owner's word, one generic implementation the node_detector operates): the record by its family and, for a record declared a NodeDetector at one Node, its number among `bodies` (None for a record spread over the board), the part (None for every line of a spread record, no line alone), the change of its count, +1, -1 or 0 (the null window moves no count), the Nodes written at, the file's coordinates, and for a spread record given whole quanta the form of its lay (`emission.emitted_quantum`): the pair its lay stands at where the list names one (a record laid whole at its declared interval at its family's massless pair [den, den], the lay by the count at one Node, `meeting.laid_whole`; the conversion's records out until 2026-10-20; the two hands) with, for a plane, the sense of its lay (0 for real lines; the conversion's table declared it until 2026-10-20; `emission.laid_by_count`), else the resonance and the span of a source in time (the emission's, the transition's declared resonance and the lifetime, the mathematician's hand with the advisor's second); the absorption's items carry the arriving record's phase at the close, (X, Y'), `arrival`, by which the entered part's direction is turned (`parted`), and the light's item the two parts' (re, im) at the Node, `levels`, the excited and the ground part's, the born source's phase phi_e - phi_g (`emission.start_of`); Part G: the light's item names the body whose click gives it (`emitter`, the emitters' book, `emission.registered`) and the entering item of an absorption names the piece's family (`drive`, the source's draw, `recoiled`); the click's plan, C6: a spread record taken names per Node the Ports the quantum entered it by, the face's set (`ports`, from the window's inflow booked per Port, `node_detector.arrival_ports`)."""

    family: int
    delta: int
    nodes: tuple[Node, ...]
    pair: tuple[int, int] | None = None
    sense: int = 0
    ports: tuple[tuple[int, ...], ...] = ()  # C6 (i): per Node named, the Ports the quantum entered by
    record: int = 0  # the record of the family the item is laid on: a born child's position among its family's children in the list the meeting selected (`act.born_items`; ALGEBRA.md, Matter's birth from light, N records of the write step, 2026-10-24), 0 otherwise


def faced(board: Lattice, item: Item) -> list[tuple[Node, tuple[int, ...]]]:
    """The one comparison of the absorption and the emission at a spread record's Nodes (features/click, `Face`; ALGEBRA.md, The click writes on the lattice (b) and (d), the undepleted beam): at each Node named the record's booked share, the share the credit reads there (`Lattice.share_of`, the conserved form's density at the Node, `share.share`, read at the click from the levels the next step reads), against the record's own quantum W_rec (`credit.Books.units`); the Nodes where it is at most W_rec, the record there local and whole, are returned with their Ports (a Node whose face set is empty, an arrival two-sided on every axis, is not among them: the quantum is taken in the books and the levels stand, the deficit path below, with the reading no side on the credit line; the click's plan, C6, the cold reader's fix of 2026-10-18), the Nodes the click writes, and for an absorption the hole to 0 is booked there: for every line of the record one face at the next two intervals on the Ports the quantum entered the Node by, the item's set for that Node (`Item.ports`; the click's plan, C6 (i)), so that Rule3 writes the level 0 and then the level before 0 with its own remainder (the mathematician's hand; the front erasing what spread beyond the Node where the count reaches 0); at a Node where the share is above W_rec a record of many quanta per Node is a beam, nature's undepleted beam, exact as the count per Node grows: no face, no lay and no front there, the levels standing (a one-Node lay into a beam would be the same point defect the hole of a dense record was), the quantum passing in the books alone (`written`: the count and the deficit); nothing assigned at any Node."""
    lines = range(board.families[item.family].record)
    intervals = (board.interval + 1, board.interval + 2)
    unit = board.credit.units[item.family]
    shares = board.share_of(item.family, 1, board.mask(item.nodes))[0]
    nodes = [(int(n[0]), int(n[1]), int(n[2])) for n in item.nodes]
    named = zip(nodes, item.ports or ((),) * len(nodes), strict=True)
    sided = not item.ports  # no face set named: a lay, or a record taken whole
    whole = [(n, p) for n, p in named if int(shares[n]) <= unit and (sided or p)]
    framed = framed_record(
        board, item.family
    )  # the hole's target the frame's level on a plain massless record
    for (at, ports), line, interval in itertools.product(
        whole if item.delta < 0 else [], lines, intervals
    ):
        face = Face(item.family, line, at, ports, interval, framed=framed)
        board.credit.faces.setdefault(interval, []).append(face)
    return whole


def faces_presented(board: Lattice, index: int) -> dict[int, Faces]:
    """The faces presented to a family's lines at this interval's step, per line, with the board's offset (the layers grown before the origin), forward and back alike (`flux.step_records`)."""
    found: dict[int, Faces] = {}
    for presented in board.credit.faces.get(board.interval, []):
        if presented.family == index:
            found.setdefault(presented.line, []).append(presented)
    return found


def faces_reported(board: Lattice) -> None:
    """The faces presented at this interval's step, one `face` line each (`reports.face`): the family, the line, the Node, the Ports and the value Rule3 read through them, written after the step computed them, for the host's tool, which presents them again on the way back from the lines and not from the books' log (`tools/back_in_time.py`)."""
    if board.output is None:
        return
    for found in board.credit.faces.get(board.interval, []):
        assert found.value is not None  # computed at this interval's step
        name, at = board.families[found.family].name, list(found.at)
        board.output(face(board.interval, name, found.line, at, list(found.ports), found.value))
