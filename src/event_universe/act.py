"""The one act of the click (ALGEBRA.md, The click writes on the lattice; the owner's word: one generic act at the Node, operated by the NodeDetector): a click is one draw among its alternatives by the reader's read of the board (`click`, `node_detector.picked`, the lower index on a tie, no draw where one alternative stands), the drawn alternative's list built where it is drawn (the place drawn inside it by the same read, the hole's Node by the inflows booked, the lay's Node by the record's share, a region's quantum to its region and boundary Node; the rows of the table, `lists.py`), the Node's act for every Item of the list (`written`: a spread record taken by the face, one value presented at one Port for two intervals so that Rule3 writes the level, or given whole quanta by the lay, `emission.emitted_quantum`; a record declared a NodeDetector laid part by part at its new count, `parted`, the piece's momentum and the source's recoil booked on its line and written nowhere, `take.recoiled`; the erasing front begun where a spread record's count reaches 0) and the click's line after the write (`node_detector.reported`, the one click line kind of every reader, or the conversion line), a list that moves no count writing its line only where its re-lay changed a level (the null window). The Node knows no click and keeps no memory of one; the books are the readers' and stand at no Node."""

from __future__ import annotations

from typing import TYPE_CHECKING

from event_universe import conversion, credit, front
from event_universe.core.rule3 import division_forward
from event_universe.emission import laid_by_count
from event_universe.loader.derived import FamilyRule, count_wall
from event_universe.loader.keys import Node
from event_universe.reports import (
    birth_line,
)
from event_universe.take import (
    Item,
    faced,
)

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


def click(board: Lattice, items: list[Item]) -> None:
    """The one click act: the draw among the alternatives by their weights by the reader's read of the board (`node_detector.picked`: one draw where more than one alternative stands, the lower index on a tie, the number left carried in the reader's books within the interval; none for one alternative, which needs no reader: the lay by the schedule and the regions' credit), then the drawn alternative's list built, written (`written`) and its line after the write (`lined`); returns the index drawn."""
    written(board, items)


def written(board: Lattice, items: list[Item]) -> None:
    """The write step of the act, the one swappable step, item by item (ALGEBRA.md, The click writes on the lattice, the undepleted beam; the two hands' line at the owner's word for the simple solution): a spread record's quantum is taken or given at the Nodes named through one comparison, `faced`, the record's booked share at the Node against its own quantum W_rec; where the record is local and whole there the absorption is the hole to 0 by the face (every line of the record whatever their number) and the emission the lay of one whole quantum (`emitted_quantum`), and where the record is a beam, many quanta per Node, nothing is written on the board: the quantum passes in the books alone, the count moved by the item's change as for every item and the family's deficit, the board's share over the books' count in quanta, moved against it (`credit.Books.deficits`, up by one for an absorption written at no Node named, down by one for an emission not laid, the deficit's condition the complement of the lay's: an emission naming several Nodes with a beam among them lays nothing and moves the deficit, though no shipped list names several Nodes for an emission; printed in the books' line), and a quantum passing into or out of a spread record ends its windows' account, its unabsorbed share and its denominator dropped from the credit's books to begin again at the count left (`credit.Books.account_ended`, `lists.absorption`); a record declared a NodeDetector at one Node laid part by part at its new count (`parted`), the direction and sense of the part its quantum leaves read first and passed to the part it enters (the phase passes with the quantum), its books' part the one carrying the count and its labels' coherence ended; where a spread record's count reaches 0 its erasing front begins from every Node faced, with the Ports faced there (`front.started`), and a record whose count stays at one or more has no front; every lay of the step is the one lay act's, which writes every line a lay changed at a Node, levels or remainder, as one `lay` line with the levels before and after (`lay.written`, `reports.lay`), the diagnostic the host's tool crosses the lay from (the mathematician's hand: the face's part crossed by Rule3's inverse, the lay's part from its line). Part G (both hands' lines of 2026-10-10, the emission's write): the recoil is booked at the act whose draw fixes the direction; a directed packet laid here (`emission.laid_packet`, the direction the emission's own draw) carries its lattice momentum at birth, and the emitting body's books take its negative as the recoil owed, in T's unit (`scaled`), with the two readings for the emission's own credit line, `BOOKED_AT_EMISSION` and `LOST_TO_SOURCE`: booked on this line and written nowhere, the body's part standing as laid (ALGEBRA.md, The click's algebra beyond the law; the recoil of a body held at declared Nodes is the declaration's); the source in time books none here, the whole recoil the click's. The standing origin (C6, 2026-10-19): where the hole's Node is booked and not faced (`NO_SIDE`, a two-sided arrival or a Port set whose read coefficients sum above the wall), its one-Node share stands and spreads behind the front at the count 0, carried by the deficit book and within B1's one half of a quantum, the consequence named."""
    holes: dict[int, list[tuple[Node, tuple[int, ...]]]] = {}
    for item in items:
        whole, was = faced(board, item), board.credit.counts[item.family]
        drawn = list(zip(item.nodes, item.ports or ((),) * len(item.nodes), strict=True))
        unwritten = not whole if item.delta < 0 else len(whole) < len(item.nodes)
        pair = born_pair(board, item, whole) if unwritten and item.delta > 0 else []
        if item.delta > 0 and not unwritten:
            laid_by_count(board, item)
        elif not pair:  # a quantum born into the pair is counted in its children, not in its own family
            board.credit.counts[item.family] += item.delta
        if item.delta > 0 and not unwritten:  # a lay that raised the count: the births' book
            credit.born(board, item.family, was)
        if item.delta < 0:  # the front from every drawn Node, faced or not (C6, the re-fix)
            holes.setdefault(item.family, []).extend(drawn)
        if pair:  # Matter's birth from light: the second quantum of a gapless family meeting the first at a Node lays the conjugate pair there, the two items walking this same step
            items.extend(pair)
            if board.output is not None:
                board.output(
                    birth_line(
                        board.interval,
                        board.families[item.family].name,
                        [board.families[born.family].name for born in pair],
                        [born.sense for born in pair],
                        pair[0].nodes,
                    )
                )
        elif unwritten:  # the undepleted beam, or no Node with a side: the quantum in the books alone
            board.credit.deficits[item.family] = board.credit.deficits.get(item.family, 0) - item.delta
    for family, absorbed in sorted(holes.items()):
        if board.credit.counts[family] <= 0 and absorbed:  # the count at 0: its front from every Node
            front.started(board, family, absorbed)


def born_table(
    families: tuple[FamilyRule, ...], parent: int, action: int, energy: int, over: int
) -> conversion.Table | None:
    """The pair two quanta of a gapless family make at one Node under the law's sentence of 2026-10-24 (ALGEBRA.md, Matter's birth from light, the owner's word, 05:2x UTC: the heaviest conjugate pair of a plane family the universe declares whose two walls fit within the two meeting quanta's own energy as read from the Node's own levels; the former clause, the lightest within the threshold 2 x 3 den T, two quanta at the top of the band, from 2026-10-23 to 2026-10-24, kept by name): among `conversion.birth_of`'s tables, the lightest first, the heaviest whose two walls, 2 x count_wall(child) = 2 x 3 T sqrt(den^2 - num^2) (`loader/derived.count_wall`), are at or below the two quanta's energy `energy` / `over`, the fraction the caller reads at the Node (the board's two n-ths of the Node's share where n whole quanta stand, `meeting_board.child_of`; the act's standing n-th with the arriving quantum's own unit, `born_pair`), the comparison cross-multiplied, 2 x count_wall(child) x over <= energy, exact in the integers with no division and no rounding; None where no pair fits, nothing then born."""
    fitting = [
        table
        for table in conversion.birth_of(families, parent)
        if 2 * count_wall(families[table[0][0]], action) * over <= energy
    ]
    return fitting[-1] if fitting else None


def born_pair(board: Lattice, item: Item, whole: list[tuple[Node, tuple[int, ...]]]) -> list[Item]:
    """Matter's birth from light, the gapless meeting's own clause (ALGEBRA.md, the law's sentence on the owner's word of 2026-10-23, the heaviest within the two quanta's own energy on his word of 2026-10-24; `conversion.birth_of`, `born_table`): a quantum of a gapless family [den, den] given at a Node where its family's quantum already stands is not written there, and in place of the books' deficit the two quanta make the heaviest conjugate pair of a plane family the universe declares whose two walls fit within their own energy, laid at that Node as two items of this write step at the senses -1 and 1 (the senses summing to 0, the charge kept); the energy read at the Node by the law's own acts: the standing light's share there (`Lattice.share_of`, the count is the record's share, the Node's two levels and its six Links, the read `take.faced` took), n W_c sin omega(k) for the n whole quanta standing at the wave number k, n the floor of the share over the record's unit (one division act, the floor `meeting_board.meetings` takes), the standing quantum's n-th of it, and the arriving quantum's own W_c sin Omega at its resonance (`emission.born_unit`, the act that gives a record its unit at its first lay; W_c for a lay by the count, a one-Node lay carrying no wave number), the two together (share + n x arriving) / n; [] where the family has a gap, where the universe declares no such pair, or where no pair's walls fit, the deficit then booked as before (the former clause's lightest pair within 2 x 3 den T was born at every meeting whatever the light's frequency, the threshold a tautology). The items walk the same write step as a conversion's records out (`laid_by_count` at the pair [den, den] of the child, the births' book by `credit.born`), so the lay is logged at its interval and undone by the run back as every lay is (The lay's inverse)."""
    family = board.families[item.family]
    if family.pair[0] != family.pair[1] or family.held:
        return []
    action = board.world.quantum_action
    nodes = (
        tuple(node for node in item.nodes if node not in {at for at, _ports in whole}) or item.nodes[:1]
    )
    at = nodes[0]
    shares, frozen = board.share_of(item.family, 1, board.mask(nodes[:1]))
    if bool(frozen[at]):
        return []  # a frozen Node births nothing: its share is not read there
    share = int(shares[at])  # the standing light's energy
    standing = max(
        int(division_forward(share, board.credit.units[item.family], 0)[0]), 1
    )  # the whole quanta standing there
    wall = count_wall(family, action)
    arriving = wall  # the arriving quantum, one wall: W_c sin Omega
    table = born_table(board.families, item.family, action, share + standing * arriving, standing)
    if table is None:
        return []
    den = board.families[table[0][0]].pair[1]
    return [Item(out, 1, nodes, (den, den), sense=sense) for out, sense in table]
