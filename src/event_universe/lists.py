"""The lists of the click from the declaration (ALGEBRA.md, The click writes on the lattice, the table of the one act's lists: the five rows with the probe's close and the record of several parts beside them; the owner's word: every kind of click a declaration and one generic act): one table, one row per kind, each row the alternatives of one draw (`act.Alternative`: the weight, the list built where it is drawn, the click's line), read from the declaration and the books, and the kinds named here and nowhere else. The region NodeDetectors' credit (`region`: the window's whole quanta in the record's own unit, (SUM s + W_rec G^2 div 2) div W_rec G^2 capped by the count, each drawn to a region by the shares and to the boundary Node it entered through by the inflows per Node, the record at -1 there, one credit line per quantum with the piece's source drawn and named, `credited_node`; a record of several parts one combination of the sides' ports drawn through the root by the joint shares, the record at -1 at one Node per side; the window's quanta one list, so that the record's front begins from every Node of the window where its count reaches 0); the absorption (`absorption`: per arriving family one draw over the closing records' transitions reading it, each at its own transfer share brought to one denominator, the norms' least common multiple, and the rest of the record's unabsorbed share as nothing, booked where it is drawn, `credit.Books.unabsorbed_in`; the list `exchange`: the drive at -1 at the hole's Node where the transition climbs and +1, given back, where it descends, the part entered +1 in the leaving part's direction turned by the arrival and carrying the piece's momentum, the part left -1); the emission (`emission`: one alternative per direction the board holds at the hazard's weight, span x p_0 x unit div Gamma, and nothing at the lifetime's rest, `hazard_weights`; the list the part left -1, the lower +1, light +1 at the Node drawn by the record's share, as a source in time or a packet along the direction, the two parts' directions read before the lay for the born phase); the probe's close (`probe`: the transitions out of the part whose drive's count stands, each at its transfer share, the probe's own re-laying the body whole in its part, and the null window as the rest); the null window (`null_window`: the part at 0 at its Nodes, one alternative, no draw); the conversion (`conversion`: the record whole at -1 at its Nodes and each family out at +1 at the Node drawn by the record's share, by the count at its massless pair with the table's sense, at the weights [the window, the rate's rest]). A row draws the place inside the list it builds, with the reader's own generator, after the click's draw and before its write; the act writes and lines (`act.click`)."""

from __future__ import annotations

from dataclasses import replace
from functools import partial
from typing import TYPE_CHECKING

from event_universe import credit, reports
from event_universe.act import Alternative, Line
from event_universe.core.rule3 import division_forward
from event_universe.loader.derived import count_wall
from event_universe.loader.keys import Node
from event_universe.loader.node_detector_declaration import Conversion, Rate, Transition
from event_universe.node_detector import (
    NodeBooks,
    credit_draw,
    drawn_node,
    drawn_weights,
    hole_node,
    own_clock,
    piece_momentum,
    share_weights,
)
from event_universe.resonance import arrival_of
from event_universe.twist import Item, fan_momentum, levels_at, unpaid

if TYPE_CHECKING:
    from event_universe.lattice import Lattice


def nothing() -> list[Item]:
    """The list of the outcome that none takes: no Item, no write."""
    return []


def part_at(books: NodeBooks, part: int, delta: int) -> list[Item]:
    """The list of a body's one part at the change `delta` over its Nodes: the null window's and the probe's own re-lay at 0, the record converted whole at -1."""
    return [Item(books.index, books.number, part, delta, books.nodes)]


def exchange(
    board: Lattice, books: NodeBooks, leaves: int, enters: int, drive: int | None = None
) -> list[Item]:
    """The record's own half of a click's list, one quantum of its count from the part `leaves` to the part `enters` at its Node, and before it, for a transition by a `drive`, the drive's item at the Node the drive's inflow draws (`hole_node`): the drive's quantum taken, -1, where the transition climbs, the part entered above the part left in the body's declared order of parts (the first part the lowest, `loader/node_detector_declaration.parts_of`), and given back, +1, where it descends, stimulated emission, by the count at the drive's own pair where the drive is local and whole at the Node and nothing where it is a beam (`act.written`, `twist.faced`, the undepleted beam; the two hands' line); both items carry the arriving record's phase the close held for the transition, (X, Y') (`resonance.arrival_of`), None for an emission, which names no drive; Part F: the entering item carries the piece's momentum p_a per axis, one count's, read at the close from the drive's momentum terms and share at the body's Nodes (`node_detector.piece_momentum`), and the books take the click's two readings for its credit line, the piece's p_a and the drive's P_a over the board before the erasure starts (`fan_momentum`), the twist's two set by the write (`twist.twisted`)."""
    arrival = arrival_of(books.declared.transitions, books.references, (leaves, enters, drive))
    books.piece = books.fan = books.twist = books.lost = books.source = books.recoil = None
    momentum = None
    if drive is not None:
        books.piece = piece_momentum(board, drive, board.mask(books.nodes))
        books.fan = list(fan_momentum(board, drive))
        momentum = (books.piece[0], books.piece[1], books.piece[2])
    entering = Item(
        books.index,
        books.number,
        enters,
        1,
        books.nodes,
        arrival=arrival,
        momentum=momentum,
        drive=drive,
    )
    parts = [entering, replace(entering, part=leaves, delta=-1, arrival=None, momentum=None, drive=None)]
    if drive is None:
        return parts
    sign = -1 if enters > leaves else 1
    pair = board.families[drive].pair if sign > 0 else None
    return [Item(drive, None, None, sign, (hole_node(board, books, drive),), pair), *parts]


def credited_node(
    board: Lattice,
    index: int,
    name: str,
    book: credit.Intake,
    realised: str | None,
    kept: list[int],
    quantum: int,
    piece: list[int],
    fan: list[int],
) -> list[Node]:
    """The Node of one credited quantum at a region and its credit line: among the region's boundary Nodes the one the quantum entered through, drawn by the window's inflows per Node floored at 0 and over G^2 once by the division act (the booked current in the unit G^2, the plain inflows bit for bit where no tension stood, `node_detector.drawn_weights`; none where nothing entered: no Node, no write); the piece's source drawn among the record's emitters by their outstanding quanta through the credit's generator (Part G; one emitter, no draw), named and not folded, a region taker having no part of its own to twist (Part H, MUST 5: `recoil` the one word `UNPAID_BY_REGION` and `lost` the reading `LOST_TO_REGION`, `twist.unpaid`; the region's +p OPEN by name); one credit line, its result the window, the region's own proper time at the close and the index of the window closed (`credit.clocked_regions`, the region's two clocks beside the board's interval, a diagnostic), the region, the port realised and the parts kept, the count moved 1 and the record's count left after this, the window's `quantum`-th, the piece's p_a per axis in T's unit (`node_detector.piece_momentum`) and the record's P_a over the board at the close (`fan_momentum`), and no Node (the owner's words: the node_detector gives no result for one Node, and the experiment reads the clicks' file alone); the write itself the act's (`act.written`, the face at that Node); returns the Node, none where nothing entered."""
    nodes = list(book)
    weights = drawn_weights(board, (book[at] for at in nodes))
    if sum(weights) <= 0:
        return []
    at = nodes[credit_draw(board, weights)]
    books = board.credit
    left, window = books.counts[index] - quantum, books.window_of(board.interval)
    source, recoil, reading = unpaid(board, index, partial(credit_draw, board))
    if board.output is not None:
        family, proper = board.families[index].name, books.clocks.get((index, name), [0, 0])[0]
        board.output(
            reports.credit(
                board.interval,
                family,
                name,
                window,
                proper,
                books.windows,
                realised,
                kept,
                1,
                left,
                None,
                None,
                None,
                piece,
                fan,
                None,
                [reading],
                source,
                recoil,
            )
        )
    return [at]


def region(board: Lattice, index: int) -> Alternative | None:
    """The region NodeDetectors' credit of one family at the window's close, the credit's row (ALGEBRA.md #the-click-is-the-meeting; L759): one alternative, no draw of its own, its list built from the window's books: for a record of several parts one combination of the sides' ports drawn through the root over the joint shares J (as the reader draws its combination), then at each side's region the one Node drawn by the window's inflows per Node with its credit line (`credited_node`, the port realised and the parts it reads with a coefficient other than 0 kept), the record at -1 as one Item over the Nodes drawn, one quantum; for a record of one part the regions' window inflows floored at 0, in the unit G^2 of the booking, give N = (their sum + W_rec G^2 div 2) div W_rec G^2 whole quanta in the record's own unit, one division at the close (`credit.quanta_through`, `credit.record_unit`), at most the count left, each drawn to a region by the shares, the inflows over G^2 once by the division act, the plain inflows bit for bit where no tension stood (`node_detector.drawn_weights`), and to one Node of it with its line, one Item each; the window's Items one list, so that the record's count goes down by one per quantum and its erasing front begins from every Node written where the count reaches 0; None where nothing entered, where the joint shares are 0 or where the record's count stands at 0, uncreditable whatever its levels still show (the empty wave, a diagnostic, until the front reaches it)."""
    books, names = board.credit, [d.name for d in board.node_detectors if d.declared]
    regions = {d.name: d.nodes for d in board.node_detectors if d.declared and d.nodes is not None}
    intake = {name: books.intake.get((index, name), {}) for name in names}
    if board.families[index].parts > 1:
        joint = books.joints.get(index, {})
        if sum(joint.values()) <= 0 or books.counts[index] <= 0 or not books.sides:
            return None

        def sides() -> list[Item]:
            fan, keys = list(fan_momentum(board, index)), sorted(joint)
            combination = keys[credit_draw(board, [joint[key] for key in keys])]
            pieces = [piece_momentum(board, index, regions[name]) for name, _ports in books.sides]
            nodes: list[Node] = []
            for (name, ports), port, piece in zip(books.sides, combination, pieces, strict=True):
                kept = [k for k, coefficient in enumerate(ports[port]) if coefficient != 0]
                port_name = reports.PORT_NAMES[port]
                nodes += credited_node(board, index, name, intake[name], port_name, kept, 1, piece, fan)
            return [Item(index, None, None, -1, tuple(nodes))]

        return Alternative(1, sides)
    inflows = [max(sum(intake[name].values()), 0) for name in names]
    shares = drawn_weights(board, inflows)
    if sum(shares) <= 0:
        return None
    through = credit.quanta_through(books, index, sum(inflows), board.unit)

    def quanta() -> list[Item]:
        fan, items = list(fan_momentum(board, index)), []
        for quantum in range(min(through, books.counts[index])):
            name = names[credit_draw(board, shares)]
            piece = piece_momentum(board, index, regions[name])
            at = credited_node(board, index, name, intake[name], None, [0], quantum + 1, piece, fan)
            items.append(Item(index, None, None, -1, tuple(at)))
        return items

    return Alternative(1, quanta)


def absorption(
    board: Lattice, drive: int, outcomes: list[tuple[NodeBooks, Transition]]
) -> list[Alternative]:
    """The absorption's row, one draw per arriving family over every closing record's outcomes into it (ALGEBRA.md, The click writes on the lattice (f): the credit draws once over all the NodeDetectors that read one record, one quantum one click; the owner's word): `outcomes` the transitions out of the part each record stands in reading the drive, with their records, each weighted by its transition's own transfer share (`meeting.turned_labels`, `NodeBooks.shares`: the two-mode line's share of the record read at the body, nothing of another drive's transfer, never the composed label of a part several drives feed), the weights of the closing bodies brought to one denominator, the least common multiple of their norms, each body's entered label squared scaled by the denominator over its own norm (ALGEBRA.md, The absorption, the draw (b); `credit.Books.unabsorbed_in`), and the outcome that none takes weighted by the rest of the record's unabsorbed share (`credit.Books.unabsorbed`, the one quantity of the record's books the draw reads: the record's count in that denominator at its first draw, read in a later closing set's denominator by the division act, down by the weights of every window drawn null, dropped when a quantum passes into or out of the record, `act.written`; the rest the smaller of the unabsorbed share and the denominator less the weights drawn, floored at 0; where the weights sum above the denominator the rest is 0 and the quantum goes to one of the bodies in the proportion of their weights, (a)), so that where the readers of one record close at different intervals the later reader's share is read conditionally on the earlier windows' nulls, s_B over (1 - the sum of the earlier readers' shares) in the labels' unit, capped at the unit, the realised frequencies the one draw's, P(B) = s_B, and the count conserved; each outcome's list `exchange` (the drive at -1 at that Node where the transition climbs in the declared order of parts and at +1, given back, where it descends, the record's part entered at +1 and left at -1) with its line, the parts and the family taken from or given to; nothing's list books the unabsorbed share down by the weights drawn, as the one draw's rest."""
    norms = [sum(label * label for label in books.labels) for books, _transition in outcomes]
    unit, unabsorbed = board.credit.unabsorbed_in(drive, norms)
    scaled = zip(outcomes, norms, strict=True)
    weights = [b.shares[t] * division_forward(unit, norm, 0)[0] for (b, t), norm in scaled]
    found = []
    for (books, transition), weight in zip(outcomes, weights, strict=True):
        leaves, enters = transition.leaves, transition.enters
        exchanged = (drive, None) if enters > leaves else (None, drive)
        items = partial(exchange, board, books, leaves, enters, drive)
        found.append(Alternative(weight, items, Line((enters, leaves), exchanged), books))

    def rest() -> list[Item]:
        board.credit.unabsorbed[drive] = unabsorbed - sum(weights)
        return []

    return [*found, Alternative(max(min(unabsorbed, unit) - sum(weights), 0), rest)]


def hazard_weights(span: int, lifetime: int, clock: int, gamma: int, unit: int) -> list[int]:
    """The dark's draw between the emission and nothing over `span` board intervals at the lifetime tau, a proper time (the mathematician's hand with the advisor's second, two hands): the hazard 1 / tau per proper interval, the body's proper intervals per board interval p_0 / Gamma, so the emission's weight is span x p_0 x unit div Gamma by the division act (half up) against the rest of tau x unit, [span x unit, (tau - span) x unit] exactly in the vacuum where p_0 = Gamma, and in a well the body gives slower by p_0 / Gamma."""
    emitted = int(division_forward(span * clock * unit, gamma, division_forward(gamma, 2, 0)[0])[0])
    return [emitted, lifetime * unit - emitted]


def emission(board: Lattice, books: NodeBooks, rate: Rate, span: int) -> list[Alternative]:
    """The emission's row, one draw per rate out of the part the record stands in (ALGEBRA.md, The click writes on the lattice (j), the fifth act, and the emission's clock; the advisor's clause 5; the mathematician's hand with the advisor's seconds, two hands): one alternative per direction the board holds for the lay (`Rate.directions`, the open board's packet; one, the source in time, inside a guide) at the emission's weight, span x p_0 x unit div Gamma, and nothing at the rest of tau x unit (`hazard_weights`; `span` the smaller of the clock's grain and the lifetime, the grain the window's lit intervals at its close or the one interval in the dark, `meeting.jumped`; p_0 the body's own clock, `node_detector.own_clock`), the lifetime's hazard 1 / tau per proper interval (the beat's current of a one-part record at one Node being 0, so the hazard alone is the rate); the list: the part at N - 1 and the lower at N + 1 at its Node (`exchange`), light's record at +1 at the one Node of the body's region drawn by the record's share at the body's Nodes as the board holds it at the close (`share_weights`, `drawn_node`; the file's lay weights enter no draw), laid as a source in time over the lifetime at the transition's declared resonance from the phase phi_e - phi_g, the two parts' (re, im) at the Node read before the lay (`levels_at`, `Item.levels`, `emission.start_of`), or as a packet along the direction where the rate declares a `width` on the open board (`emission.laid_packet`, an assumption by name); its line the part after and before and the light given to."""
    unit = count_wall(board.families[books.index], board.world.quantum_action) ** 2
    clock, directions = own_clock(board, books), rate.directions or (None,)
    given, rest = hazard_weights(span, rate.lifetime, clock, board.world.node_clock, unit)

    def lit(direction: tuple[int, int] | None) -> list[Item]:
        laid_at = drawn_node(board, books, share_weights(board, books))
        e, g = (levels_at(board, books, p)[:2] for p in (rate.leaves, rate.enters))
        light = Item(rate.light, None, None, 1, (laid_at,), None, rate.resonance, rate.lifetime)
        light = replace(
            light, width=rate.width, direction=direction, levels=(e, g), emitter=books.number
        )
        return exchange(board, books, rate.leaves, rate.enters) + [light]

    line = Line((rate.enters, rate.leaves), (None, rate.light))
    found = [Alternative(given, partial(lit, direction), line, books) for direction in directions]
    return [*found, Alternative(len(directions) * rest, nothing)]


def probe(board: Lattice, books: NodeBooks) -> list[Alternative]:
    """The probe's close, the body's one draw at the probe's arrival (ALGEBRA.md, The pulsed gate; the two hands): over the transitions out of the part the body stands in whose family's count stands, each at its own transfer share (`meeting.turned_labels`, `NodeBooks.shares`, the record's share at the body) and the probe's own at the part's label squared as the turns left it (the two-mode line's shares, sin^2 and cos^2 of the half window's turn): the probe's own, the transition of the part into itself, re-lays the body whole in that part, its list the part at the change 0 and no write on the probe's record (taken and given back at one interval and one Node, the fluorescence by name the probe's own wave continuing from that Node), its line naming the probe's family as taken and given; a drive's takes the drive's quantum and exchanges the parts as every absorption does (`exchange`, the hole, the count down by one); the rest of the labels' unit is the null window, the body whole in its part (`null_window`), nothing where the record has one part."""
    outcomes = [
        t
        for t in books.declared.transitions
        if t.leaves == books.part and board.credit.counts[t.drive] > 0
    ]
    weights = [books.shares.get(t, books.labels[t.enters] ** 2) for t in outcomes]
    found = []
    for transition, weight in zip(outcomes, weights, strict=True):
        leaves, enters, drive = transition.leaves, transition.enters, transition.drive
        traded = (drive if enters >= leaves else None, drive if enters <= leaves else None)
        own = leaves == enters
        items = (
            partial(part_at, books, leaves, 0)
            if own
            else partial(exchange, board, books, leaves, enters, drive)
        )
        found.append(Alternative(weight, items, Line((enters, leaves), traded), books))
    rest = sum(label * label for label in books.labels) - sum(weights)
    quiet = null_window(board, books)[0] if len(books.counts) > 1 else Alternative(0, nothing)
    return [*found, replace(quiet, weight=rest if rest > 0 else 0)]


def null_window(board: Lattice, books: NodeBooks) -> list[Alternative]:
    """The window with no click (the owner's words, "Yes, both of them" and "I approve the four things"; the mathematician's hand; the advisor's clause 8): one alternative and no draw, the record's own reading of itself written at its one Node, the part it stands in at the change 0 (`part_at`): the record laid again in the complement of its outcome set, the part it stands in, at its whole count, in that part's own direction and sense at every Node of the region (the levels of what stands there within the lay's rounding, each Node's own direction kept so that a twist across the region survives, Part H, MUST 1; the remainder at the lay's origin), the parts' counts unchanged, and the labels' coherence ended; its line at the count 0, written where the re-lay changed a level at any Node of the region (Part H: every Node read, the re-lay standing per Node), one click line labelled LATTICE with the `lay` lines beside it for the host's tool (a null window that changes nothing writes none; `act.click`)."""
    line = Line((books.part, books.part), (None, None), 0)
    return [Alternative(1, partial(part_at, books, books.part, 0), line, books)]


def conversion(board: Lattice, books: NodeBooks, table: Conversion, span: int) -> list[Alternative]:
    """The conversion's row, a record converted whole at its one Node (ALGEBRA.md, A family's declaration, item 5, The conversion's table and rate; The click is the meeting, what the click's picture derives of the conversions; the two hands, the advisor's (c), the mathematician's hand, and their agreement on the one-Node lay): one draw between the conversion's list and nothing at the weights [`span`, the rate less it], the span the window capped at the rate (the rate the intervals per expected conversion, the declared floor, as the emission's); the list the record whole at -1 at its Nodes (`part_at`, its hole its lay at the count 0) and each family out at +1 at the one Node of the region drawn by the record's share at the body's Nodes as the board holds it at the close (`share_weights`, `drawn_node`; the file's lay weights enter no draw), one whole quantum laid by the count at its family's massless pair [den, den] on every laid line of its record alike, a plane's two lines per plane with the sense the table declares for it (`emission.emitted_quantum`, `Item.pair`, `Item.sense`; the mathematician's hand); the act writes one lay line per line the write changed, every line of the record in and every laid line of each record out, so that the back-in-time tool crosses the write as it crosses the absorption and the emission, and one conversion line (`act.lined`, `reports.conversion`); the rotations' sum and the sines' difference at the Node are the reader's to book from the levels (the world `examples/events/neutron_conversion/`)."""

    def whole() -> list[Item]:
        items = part_at(books, books.part, -1)
        laid_at = drawn_node(board, books, share_weights(board, books))
        for out, sense in zip(table.outs, table.senses, strict=True):
            den = board.families[out].pair[1]
            items.append(Item(out, None, None, 1, (laid_at,), (den, den), sense=sense))
        return items

    return [
        Alternative(span, whole, Line(into=table.outs), books),
        Alternative(table.rate - span, nothing),
    ]
