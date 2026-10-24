"""The take, the act's readings and items (the law's word for the act its contents serve, the module so named on 2026-10-21, twist.py until then; the engine V2, Parts F and G; ALGEBRA.md, The click's algebra beyond the law, The lattice momentum, The click's momentum on the board; the owner's rule, at the Nodes Rule3 only): the taker's part re-laid at each Node's own direction (`relaid`, `levels_at`), the click's items (`Item`, `Phase`, `books_named`), the hole's faces (`faced`, `faces_presented`, `faces_reported`), the piece's momentum readings (`fan_momentum`, `scaled`) and the piece's source drawn among the emitters by the quanta each holds and named with the recoil it owes, -p_a as integers on the credit line and written nowhere (`recoiled`, `drawn_emitter`), the loss booked by name (`unpaid`); the write moves the count by one and writes nothing for the piece's momentum, the recoil of a body held at declared Nodes being the declaration's; meeting.py writes the click with them."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from event_universe.loader.keys import Node

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
    record: int = 0  # the record of the family the item is laid on: a born child's position among its family's children in the list the meeting selected (`act.born_items`; ALGEBRA.md, Matter's birth from light, N records of the write step, 2026-10-24), 0 otherwise


def below_quantum(board: Lattice, item: Item) -> list[Node]:
    """The one comparison of the lay at a spread record's Nodes (ALGEBRA.md, The click writes on the lattice (b) and (d), the undepleted beam; the board's own click, 2026-10-24, the one click since the declared taker was struck): at each Node named the record's booked share, the share the credit reads there (`Lattice.share_of`, the conserved form's density at the Node in the current's units, read before any item's write), against its own quantum W_rec (`credit.record_unit`, the books' unit): the Nodes where the share is at most one quantum, where the lay writes; a Node whose share stands above one quantum takes the quantum in the books alone (`act.written`, the deficit path)."""
    unit = board.credit.units[item.family]
    shares = board.share_of(item.family, 1, board.mask(item.nodes))[0]
    nodes = [(int(n[0]), int(n[1]), int(n[2])) for n in item.nodes]
    return [n for n in nodes if int(shares[n]) <= unit]
