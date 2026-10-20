"""The lists of the click from the declaration (ALGEBRA.md, The click writes on the lattice, the table of the one act's lists: the five rows with the probe's close and the record of several parts beside them; the owner's word: every kind of click a declaration and one generic act): one table, one row per kind, each row the alternatives of one draw (`act.Alternative`: the weight, the list built where it is drawn, the click's line), read from the declaration and the books, and the kinds named here and nowhere else. The region NodeDetectors' credit (`region`: the window's whole quanta in the record's own unit, (SUM s + W_rec G^2 div 2) div W_rec G^2 capped by the count, each drawn to a region by the shares and to the boundary Node it entered through by the inflows per Node, the record at -1 there, one credit line per quantum with the piece's source drawn and named, `credited_node`; a record of several parts read at its sides in the order of their closes, each side's port drawn on its own second moments with the write at the record's birth (`readings`, `meeting_back`), the record at -1 at one Node per side once every side has drawn; the window's quanta one list, so that the record's front begins from every Node of the window where its count reaches 0); the absorption (`absorption`: per arriving family one draw over the closing records' transitions reading it, each at its own transfer share brought to one denominator, the norms' least common multiple, and the rest of the record's unabsorbed share as nothing, booked where it is drawn, `credit.Books.unabsorbed_in`; the list `exchange`: the drive at -1 at the hole's Node where the transition climbs and +1, given back, where it descends, the part entered +1 in the leaving part's direction turned by the arrival and carrying the piece's momentum, the part left -1); the emission (`emission`: one alternative per direction the board holds at the hazard's weight, span x p_0 x unit div Gamma, and nothing at the lifetime's rest, `hazard_weights`; the list the part left -1, the lower +1, light +1 at the Node drawn by the record's share, as a source in time or a packet along the direction, the two parts' directions read before the lay for the born phase); the probe's close (`probe`: the transitions out of the part whose drive's count stands, each at its transfer share, the probe's own re-laying the body whole in its part, and the null window as the rest); the null window (`null_window`: the part at 0 at its Nodes, one alternative, no draw); the conversion (`conversion`: the record whole at -1 at its Nodes and each family out at +1 at the Node drawn by the record's share, by the count at its massless pair with the table's sense, at the weights [the window, the rate's rest]). A row draws the place inside the list it builds, with the reader's own generator, after the click's draw and before its write; the act writes and lines (`act.click`)."""

from __future__ import annotations

from dataclasses import replace
from functools import partial
from typing import TYPE_CHECKING

from event_universe import credit, meeting_back, reports
from event_universe.act import Alternative, Line
from event_universe.core.rule3 import division_forward
from event_universe.loader.derived import count_wall
from event_universe.loader.keys import Node
from event_universe.loader.node_detector_declaration import Conversion, Rate, Transition
from event_universe.node_detector import (
    NodeBooks,
    Passage,
    credit_draw,
    drawn_node,
    drawn_weights,
    face_ports,
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


def full(books: NodeBooks, part: int) -> bool:
    """The exclusion as the declared rule in the detector's lists (the spin branch, 2026-10-19; ALGEBRA.md, Spin, closed for the paper as a route): a part whose declared `capacity` its count has reached is full, and every alternative that moves a quantum into it has the weight 0 in the list it stands in (`absorption` and `probe`, the transitions into it; `emission`, the rate's part entered), so the quantum is refused by the full part and taken by another or by nothing; a part declaring no capacity is never full. The capacity caps the count in the declared part, in the parts' own basis and in no axis, and reads no sense: a part of capacity 1 holds one quantum whatever its planes' state, an orbital holding both senses is a capacity 2 and the pairing of its senses is not read; the refusal gives nothing to any other outcome, the open parts keeping their own shares and the quantum passing where none takes it (the absorption's rest), and the blocked lower part of an emission is the same declaration descending. Under the engine's one-part convention a body of several quanta stands in the part carrying the largest count after an absorption, the first of a tie in the declared order (`act.written`), and its transitions and rates are read from the standing part alone, so a populated part the body does not stand in neither emits nor transitions while it stands elsewhere. A declaration by name (`loader/node_detector_declaration.parts_of`) and not derived, nothing at the Node: the loader admits a transition's own `weight` from 1 only, and the 0 is the list's at a full part, never the file's."""
    capacities = books.declared.capacities
    capacity = capacities[part] if part < len(capacities) else None
    return capacity is not None and books.counts[part] >= capacity


def exchange_factor(board: Lattice, books: NodeBooks, part: int) -> int:
    """The factor a quantum's entry into `part` carries from the record's sign under exchange, the family's declaration and nothing per part (ALGEBRA.md, Spin, closed for the paper as a route, The family's sign under exchange, 2026-10-19; the key `exchange`, `loader/universe.exchange_of`, `FamilyRule.exchange`): for an antisymmetric record the determinant of two quanta in one part is 0, so a populated part takes nothing, the exclusion derived from the sign and declared by no capacity; for a symmetric record the permanent, n + 1 at a part holding n quanta, the piling of like quanta; 1 for a family declaring no sign, the lists as they stand. Read beside `full` in the absorption, the emission and the probe, the same determinant the first side's coefficients carry for the antisymmetric family (`meeting_back.coefficients_of`, `credit.terms_of`); nothing at the Node."""
    sign, held = board.families[books.index].exchange, books.counts[part]
    if sign < 0:
        return 0 if held >= 1 else 1
    return held + 1 if sign > 0 else 1


def exchange(
    board: Lattice, books: NodeBooks, leaves: int, enters: int, drive: int | None = None
) -> list[Item]:
    """The record's own half of a click's list, one quantum of its count from the part `leaves` to the part `enters` at its Node, and before it, for a transition by a `drive`, the drive's item at the Node the drive's inflow draws, with the Ports the quantum entered it by, the hole's face set, and that Node the fold's origin on the part entered (`hole_node`, `Item.ports`, `Item.origin`; the click's plan, C6): the drive's quantum taken, -1, where the transition climbs, the part entered above the part left in the body's declared order of parts (the first part the lowest, `loader/node_detector_declaration.parts_of`), and given back, +1, where it descends, stimulated emission, by the count at the drive's own pair where the drive is local and whole at the Node and nothing where it is a beam (`act.written`, `twist.faced`, the undepleted beam; the two hands' line); both items carry the arriving record's phase the close held for the transition, (X, Y') (`resonance.arrival_of`), None for an emission, which names no drive; Part F: the entering item carries the piece's momentum p_a per axis, one count's, read at the close from the drive's passage through the body's Nodes over the window, its momentum terms over its share (`node_detector.piece_momentum`, `NodeBooks.passages`, C4), and the books take the click's two readings for its credit line, the piece's p_a and the drive's P_a over the board before the erasure starts (`fan_momentum`), the twist's two set by the write (`twist.twisted`)."""
    arrival = arrival_of(books.declared.transitions, books.references, (leaves, enters, drive))
    books.piece = books.fan = books.twist = books.shortfall = books.lost = books.source = (
        books.recoil
    ) = None
    momentum, taken = None, None
    if drive is not None:
        books.piece = piece_momentum(board, drive, books.passages.get(drive, Passage()))
        books.fan = list(fan_momentum(board, drive))
        momentum = (books.piece[0], books.piece[1], books.piece[2])
        at, ports = hole_node(board, books, drive)
        sign = -1 if enters > leaves else 1
        pair = board.families[drive].pair if sign > 0 else None
        taken = Item(drive, None, None, sign, (at,), pair, ports=(ports,))
    entering = Item(
        books.index,
        books.number,
        enters,
        1,
        books.nodes,
        arrival=arrival,
        momentum=momentum,
        drive=drive,
        origin=taken.nodes[0] if taken is not None else None,
    )
    left = replace(entering, part=leaves, delta=-1, arrival=None, momentum=None, drive=None, origin=None)
    return [entering, left] if taken is None else [taken, entering, left]


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
    order: int | None = None,
    scale: int | None = None,
    board_count: int | None = None,
) -> list[tuple[Node, tuple[int, ...]]]:
    """The Node of one credited quantum at a region, the Ports it entered by and its credit line: among the region's boundary Nodes the one the quantum entered through, drawn by the window's inflows per Node, the Ports' sums, floored at 0 and over G^2 once by the division act (the booked current in the unit G^2, the plain inflows bit for bit where no tension stood, `node_detector.drawn_weights`; none where nothing entered: no Node, no write), with the Ports of its face set from the same book (`node_detector.arrival_ports`, the click's plan, C6 (i)); the piece's source drawn among the record's emitters by their outstanding quanta through the credit's generator (Part G; one emitter, no draw), named and not folded, a region taker having no part of its own to twist (Part H, MUST 5: `recoil` the one word `UNPAID_BY_REGION` and `lost` the reading `LOST_TO_REGION`, `twist.unpaid`; the region's +p OPEN by name); one credit line, its result the window, the region's own proper time at the close and the index of the window closed (`credit.clocked_regions`, the region's two clocks beside the board's interval, a diagnostic), the region, the port realised and the parts kept, the count moved 1 and the record's count left after this, the window's `quantum`-th, the piece's p_a per axis in T's unit, the record's passage through the region over the window (`node_detector.piece_momentum`, `credit.Books.passages`, C4) and the record's P_a over the board at the close (`fan_momentum`), and no Node (the owner's words: the node_detector gives no result for one Node, and the experiment reads the clicks' file alone); the write itself the act's (`act.written`, the face at that Node); returns the Node with its Ports, none where nothing entered. For a side of a record of several parts (`order`, the side's order among the sides' draws, 1 the first side to N the last, `scale`, the record's scale after the side's write, and `board_count`, the record's count read from the board at the close; `readings`) the Node and the piece's source are drawn with the side's own state (`credit_draw` with the side) and the line carries the three (`reports.ORDER`, `reports.SCALE`, `reports.BOARD_COUNT`)."""
    nodes, side = list(book), name if order is not None else None
    weights = drawn_weights(board, (sum(book[at]) for at in nodes))
    if sum(weights) <= 0:
        return []
    at = nodes[credit_draw(board, weights, side)]
    ports = face_ports(board, index, at, book[at])  # the face set, empty on the booked path
    books = board.credit
    left, window = books.counts[index] - quantum, books.window_of(board.interval)
    source, recoil, reading = unpaid(board, index, partial(credit_draw, board, side=side))
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
                None,
                [reading, *([reports.NO_SIDE] if not ports else [])],
                source,
                recoil,
                order,
                scale,
                board_count,
            )
        )
    return [(at, ports)]


def readings(board: Lattice, index: int) -> list[Item]:
    """The click of a record of several parts, the sides' sequence with the write at the birth (ALGEBRA.md, The click is the meeting of the future with the past: at the root it writes; The meeting's reading: the sides draw in the order of their closes, equal closes in the declared order, each alone at its own place with its own state on its own region's read, the quadratic form of its coefficients on its own second moments with the Gram of the sides after it; The meeting's identity, the Gram theorem; the owner's words of 2026-10-20, the click writes and nothing is in the books but the draw at the click): at a window's close every side whose own moments stand and whose port is unrealised for this record (`credit.Books.taken`) draws in the declared order (`credit_draw` with the side's own state, `meeting_back.side_weights`, the weights kept in the books as a diagnostic, `credit.Books.weights`); its credit line carries its order, the record's scale after its write and the record's count read from the board at the close (`credited_node`, `Lattice.count`); the record runs back along its cone to its birth (`meeting_back.run_back`), the realised port's integer coefficients are written there (`meeting_back.realised`, the one lay act) and the record runs forward again to the close, the sides' books taken again from the rewritten record on the way (`meeting_back.run_forward`), so the next side reads the realised term where it stands; every click writes, the last side's read coherent (no side after it); a side whose beam has not reached it draws at a later close; when every side has drawn, one Item at -1 over the drawn Nodes with their face sets, the count's write and the front the act's as built (`act.written`, `front.started`), and the sequence settled (`credit.Books.taken`: the realised port per side stands until the family's next birth; the reader's ruling of 2026-10-20, precision one: a side already realised that clicks again at a later close in the same setting realises the same port with certainty and writes nothing, its credit line carrying the order of the new sequence, and a side whose realised port carries no overlap with the written factor, a changed setting, is refused by name); N runs for N sides, no number at a Node but Rule3's."""
    books, family = board.credit, board.families[index]
    close, fan = board.interval, list(fan_momentum(board, index))
    taken = books.taken.setdefault(index, {})
    for name, ports in books.sides:
        moments, earlier = books.moments.get(index, {}).get(name), taken.get(name)
        if moments is None or not any(map(any, moments)) or (earlier is not None and not earlier[2]):
            continue  # its beam arriving after this close, or realised in the sequence standing: no second click
        unrealised = [
            books.patterns[other] for other, _p in books.sides if other != name and other not in taken
        ]
        first = not taken if earlier is None else next(iter(taken)) == name
        coefficients = meeting_back.coefficients_of(family, ports, first)
        weights = meeting_back.side_weights(
            moments, coefficients, meeting_back.gram_of(unrealised, family.parts)
        )
        books.weights[(index, name)] = weights
        if earlier is None:
            if sum(weights) <= 0:
                continue
            port = credit_draw(board, weights, name)
        elif weights[port := earlier[0]] <= 0:
            raise RuntimeError(
                f"the side {name!r} clicks again on the record of {family.name!r} with its realised port "
                f"{reports.PORT_NAMES[port]!r} carrying no overlap with the written factor (the weight 0): a later "
                "click of a side in a changed setting needs the overlaps with the written factor, which the parts "
                "carry no more; one setting per side on a record (the reader's ruling of 2026-10-20)"
            )
        kept = [k for k, coefficient in enumerate(ports[port]) if coefficient != 0]
        piece = piece_momentum(board, index, books.passages.get((index, name), Passage()))
        written = books.written.get(index, [1] * family.parts)  # the scale after the side's write
        reduced = (
            credit.reduced(board, index, coefficients[port]) if earlier is None else [1] * family.parts
        )
        scale = sum((w * c) ** 2 for w, c in zip(written, reduced, strict=True))
        order = 1 + sum(
            1 for entry in taken.values() if not entry[2]
        )  # the sides clicked in this sequence
        found = credited_node(
            board,
            index,
            name,
            books.intake.get((index, name), {}),
            reports.PORT_NAMES[port],
            kept,
            1,
            piece,
            fan,
            order,
            scale,
            board.count(index),
        )
        taken[name] = (port, found[0] if found else None, False)
        if earlier is None:  # the side's first click on the record: the write at the birth
            left = meeting_back.run_back(board, index)  # the close as the run back left it
            meeting_back.realised(board, index, coefficients[port])
            meeting_back.run_forward(board, index, close, left)
    if len(taken) < len(books.sides) or any(entry[2] for entry in taken.values()):
        return []
    drawn = [entry[1] for entry in taken.values() if entry[1] is not None]
    for name, entry in taken.items():
        taken[name] = (
            entry[0],
            entry[1],
            True,
        )  # settled: the next window's clicks begin a new sequence
    return [Item(index, None, None, -1, tuple(n for n, _p in drawn), ports=tuple(p for _n, p in drawn))]


def region(board: Lattice, index: int) -> Alternative | None:
    """The region NodeDetectors' credit of one family at the window's close, the credit's row (ALGEBRA.md #the-click-is-the-meeting; L759): one alternative, no draw of its own, its list built from the window's books: for a record of several parts the sides' sequence (`readings`: every side whose own moments stand and whose port is unrealised, or realised in a sequence the count's write settled, draws at the close, in the declared order, each at its own region the one Node by the window's inflows per Node with its credit line, `credited_node`, the port realised and the parts it reads with a coefficient other than 0 kept, the write at the record's birth between the draws), the record at -1 as one Item over the Nodes drawn once every side has drawn, one quantum; for a record of one part the regions' window inflows floored at 0, in the unit G^2 of the booking, give N = (their sum + W_rec G^2 div 2) div W_rec G^2 whole quanta in the record's own unit, one division at the close (`credit.quanta_through`, `credit.record_unit`; the remainder of C7 moves when this alternative is built, before the one act draws, main's order kept), at most the count left, each drawn to a region by the shares, the inflows over G^2 once by the division act, the plain inflows bit for bit where no tension stood (`node_detector.drawn_weights`), and to one Node of it with its line, one Item each; the window's Items one list, so that the record's count goes down by one per quantum and its erasing front begins from every Node written where the count reaches 0; None where nothing entered, where no side is ready or where the record's count stands at 0, uncreditable whatever its levels still show (the empty wave, a diagnostic, until the front reaches it)."""
    books, names = board.credit, [d.name for d in board.node_detectors if d.declared]
    passages = {name: books.passages.get((index, name), Passage()) for name in names}
    intake = {name: books.intake.get((index, name), {}) for name in names}
    if (
        board.families[index].parts > 1
    ):  # the sides' sequence with the write at the birth, the one meeting
        taken = books.taken.get(index, {})
        moments = books.moments.get(index, {})
        ready = [
            name
            for name, _p in books.sides
            if (name not in taken or taken[name][2]) and any(map(any, moments.get(name, [])))
        ]
        if not ready or books.counts[index] <= 0:
            return None
        return Alternative(1, partial(readings, board, index))
    inflows = [max(sum(sum(through) for through in intake[name].values()), 0) for name in names]
    shares = drawn_weights(board, inflows)
    if sum(shares) <= 0:
        return None
    through = credit.quanta_through(books, index, sum(inflows), board.unit, board.families[index].parts)

    def quanta() -> list[Item]:
        fan, items = list(fan_momentum(board, index)), []
        for quantum in range(min(through, books.counts[index])):
            name = names[credit_draw(board, shares)]
            piece = piece_momentum(board, index, passages[name])
            found = credited_node(board, index, name, intake[name], None, [0], quantum + 1, piece, fan)
            items.append(
                Item(
                    index, None, None, -1, tuple(n for n, _p in found), ports=tuple(p for _n, p in found)
                )
            )
        return items

    return Alternative(1, quanta)


def absorption(
    board: Lattice, drive: int, outcomes: list[tuple[NodeBooks, Transition]]
) -> list[Alternative]:
    """The absorption's row, one draw per arriving family over every closing record's outcomes into it (ALGEBRA.md, The click writes on the lattice (f): the credit draws once over all the NodeDetectors that read one record, one quantum one click; the owner's word): `outcomes` the transitions out of the part each record stands in reading the drive, with their records, each weighted by its transition's own transfer share (`meeting.turned_labels`, `NodeBooks.shares`: the two-mode line's share of the record read at the body, nothing of another drive's transfer, never the composed label of a part several drives feed), the weights of the closing bodies brought to one denominator, the least common multiple of their norms, each body's entered label squared scaled by the denominator over its own norm (ALGEBRA.md, The absorption, the draw (b); `credit.Books.unabsorbed_in`), and the outcome that none takes weighted by the rest of the record's unabsorbed share (`credit.Books.unabsorbed`, the one quantity of the record's books the draw reads: the record's count in that denominator at its first draw, read in a later closing set's denominator by the division act, down by the weights of every window drawn null, dropped when a quantum passes into or out of the record, `act.written`; the rest the smaller of the unabsorbed share and the denominator less the weights drawn, floored at 0; where the weights sum above the denominator the rest is 0 and the quantum goes to one of the bodies in the proportion of their weights, (a)), so that where the readers of one record close at different intervals the later reader's share is read conditionally on the earlier windows' nulls, s_B over (1 - the sum of the earlier readers' shares) in the labels' unit, capped at the unit, the realised frequencies the one draw's, P(B) = s_B, and the count conserved; each outcome's list `exchange` (the drive at -1 at that Node where the transition climbs in the declared order of parts and at +1, given back, where it descends, the record's part entered at +1 and left at -1) with its line, the parts and the family taken from or given to; nothing's list books the unabsorbed share down by the weights drawn, as the one draw's rest; an outcome into a full part stands at the weight 0, the exclusion (`full`, 2026-10-19), and every outcome's weight carries the record's sign under exchange on the part entered, 0 into a populated part for the antisymmetric record and n + 1 for the symmetric (`exchange_factor`)."""
    norms = [sum(label * label for label in books.labels) for books, _transition in outcomes]
    unit, unabsorbed = board.credit.unabsorbed_in(drive, norms)
    scaled = zip(outcomes, norms, strict=True)
    weights = [
        0
        if full(b, t.enters)
        else exchange_factor(board, b, t.enters) * b.shares[t] * division_forward(unit, norm, 0)[0]
        for (b, t), norm in scaled
    ]  # the exclusion: a transition into a full part at the weight 0 (`full`); the sign's factor on the part entered (`exchange_factor`)
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
    """The emission's row, one draw per rate out of the part the record stands in (ALGEBRA.md, The click writes on the lattice (j), the fifth act, and the emission's clock; the advisor's clause 5; the mathematician's hand with the advisor's seconds, two hands): one alternative per direction the board holds for the lay (`Rate.directions`, the open board's packet; one, the source in time, inside a guide) at the emission's weight, span x p_0 x unit div Gamma, and nothing at the rest of tau x unit (`hazard_weights`; `span` the smaller of the clock's grain and the lifetime, the grain the window's lit intervals at its close or the one interval in the dark, `meeting.jumped`; p_0 the body's own clock, `node_detector.own_clock`), the lifetime's hazard 1 / tau per proper interval (the beat's current of a one-part record at one Node being 0, so the hazard alone is the rate); the list: the part at N - 1 and the lower at N + 1 at its Node (`exchange`), light's record at +1 at the one Node of the body's region drawn by the record's share at the body's Nodes as the board holds it at the close (`share_weights`, `drawn_node`; the file's lay weights enter no draw), laid as a source in time over the lifetime at the transition's declared resonance from the phase phi_e - phi_g, the two parts' (re, im) at the Node read before the lay (`levels_at`, `Item.levels`, `emission.start_of`), or as a packet along the direction where the rate declares a `width` on the open board (`emission.laid_packet`, an assumption by name); its line the part after and before and the light given to; the emission into a full lower part stands at the weight 0 and nothing at the whole hazard, lifetime x unit, so the list's total stands above 0 where the window's lit intervals reach the lifetime (the exclusion, `full`; the cold reader's E1, 2026-10-19); the emission's weight carries the record's sign under exchange on the lower part, the whole hazard to nothing where the factor is 0 (`exchange_factor`)."""
    unit = count_wall(board.families[books.index], board.world.quantum_action) ** 2
    clock, directions = own_clock(board, books), rate.directions or (None,)
    given, rest = hazard_weights(span, rate.lifetime, clock, board.world.node_clock, unit)
    # the exclusion: no emission into a full lower part, nothing the whole hazard (`full`); the sign's
    # factor on the part entered, 0 for the antisymmetric record's populated part (`exchange_factor`)
    given = given * exchange_factor(board, books, rate.enters)
    if full(books, rate.enters) or given == 0:
        given, rest = 0, rate.lifetime * unit

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
    """The probe's close, the body's one draw at the probe's arrival (ALGEBRA.md, The pulsed gate; the two hands): over the transitions out of the part the body stands in whose family's count stands, each at its own transfer share (`meeting.turned_labels`, `NodeBooks.shares`, the record's share at the body) and the probe's own at the part's label squared as the turns left it (the two-mode line's shares, sin^2 and cos^2 of the half window's turn): the probe's own, the transition of the part into itself, re-lays the body whole in that part, its list the part at the change 0 and no write on the probe's record (taken and given back at one interval and one Node, the fluorescence by name the probe's own wave continuing from that Node), its line naming the probe's family as taken and given; a drive's takes the drive's quantum and exchanges the parts as every absorption does (`exchange`, the hole, the count down by one); the rest of the labels' unit is the null window, the body whole in its part (`null_window`), nothing where the record has one part; a drive's transition into a full part stands at the weight 0, the exclusion (`full`, 2026-10-19), and carries the record's sign under exchange on the part entered (`exchange_factor`), the probe's own transition at its share alone."""
    outcomes = [
        t
        for t in books.declared.transitions
        if t.leaves == books.part and board.credit.counts[t.drive] > 0
    ]
    weights = [
        0
        if t.enters != t.leaves and full(books, t.enters)
        else (exchange_factor(board, books, t.enters) if t.enters != t.leaves else 1)
        * books.shares.get(t, books.labels[t.enters] ** 2)
        for t in outcomes
    ]  # the exclusion: a drive's transition into a full part at the weight 0 (`full`) and the sign's factor on the part entered (`exchange_factor`); the probe's own stands
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
