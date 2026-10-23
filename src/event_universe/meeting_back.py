"""The meeting that runs back, the click that writes (ALGEBRA.md, The click is the meeting of the future with the past: backward, to the past, the click runs back along the record to its birth and writes there, the realised term's integers into the record's parts, and the board runs forward again by Rule3, so that every later side reads the realised term where it stands, which gives Bell at a distance; The meeting's reading; The births' book; the owner's words of 2026-10-19 and 2026-10-20, the click writes and nothing is in the books but the draw at the click): for every record of several parts read at N declared sides, each side draws at its own place with its own state in the order of the closes, equal closes in the declared order (`lists.readings`), on its own region's second moments with the Gram of the sides after it (`moments_booked`, `gram_of`, `coefficients_of`, `side_weights`, the Gram theorem); its realised port runs back along the record to its birth, the board stepped back by Rule3 at -1 to the birth's interval from the births' book (`run_back`, `birth_of`, `credit.Books.births`), every act from outside the Node re-presented on the way, the faces from the books' log (`take.faces_presented`) and the lays undone from the books' log of the lay lines (`logged`, `crossed`; `credit.Books.lays`, written by `lay.written`); at the birth the port's integer coefficients are written into the record's parts through the one lay act (`realised`, `lay.laid`, exact in the integers); then the board runs forward again to the close by the step at the Nodes alone (`run_forward`, `Lattice.step` with no act, the lays re-applied by their changes, the record's own later lays scaled), the sides' books taken again on the way (`booked_moments`), and the close asserted: outside the record's cone bit for bit the board the run back left, the parts written 0 at zero, the parts written alike equal (`copied`, `snapshot`, `first_difference`); N runs for N sides, the credit lines carrying the side's order and the record's scale; in the cone's reach, the default, the cone stepped alone (the owner's word of 2026-10-20, only the cone moves and the whole board steps as ever): the run back and the run forward step the record's light cone and nothing else, the ball with one ring of Nodes read from the board and asserted at frame 0, the rest of the board neither read nor written (`cone.stepped_alone`, `credit.Books.reach`); the antisymmetric sign read at other than two sides refused by name at load. The host tool's crossing of the acts from the LATTICE lines (tools/back_in_time.py: `faces_from`, `crossed` from the `face` and `lay` lines) lives here and the tool imports it; the observers' frames of the run back and forward are the lattice's (`Lattice.observers`)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import cone, credit, growth, reports
from event_universe.features import phase
from event_universe.features.click import Face
from event_universe.features.front import ball
from event_universe.front import on_board
from event_universe.lay import laid
from event_universe.loader.derived import FamilyRule
from event_universe.loader.draw import CONE, Gauss, Pattern, Ports, times
from event_universe.records import NodeState, Record, largest

if TYPE_CHECKING:
    from event_universe.lattice import Lattice

Snapshot = list[tuple[str, np.ndarray]]  # every array of one family's NodeState with its name, copied
Lines = list[dict[str, object]]  # output lines, as the lattice's output receives them (`reports.py`)
Kept = tuple[
    list[NodeState], list[growth.Growth]
]  # the close as the run back took it: every array copied, the growths standing


def named(name: str, state: NodeState) -> list[tuple[str, np.ndarray]]:
    """Every array of a family's NodeState with its name, the array itself (no copy): every line's levels now and before and its remainder, every held line's write remainder."""
    found: list[tuple[str, np.ndarray]] = []
    for index, record in enumerate(state.lines):
        found.append((f"{name}.lines[{index}].now", record.now))
        found.append((f"{name}.lines[{index}].before", record.before))
        found.append((f"{name}.lines[{index}].remainder", record.remainder))
    found += [
        (f"{name}.write_remainders[{index}]", value)
        for index, value in enumerate(state.write_remainders)
    ]
    return found


def arrays_of(name: str, state: NodeState) -> Snapshot:
    """Every array of a family's NodeState with its name, copied (`named`)."""
    return [(label, np.asarray(value).copy()) for label, value in named(name, state)]


def snapshot(board: Lattice, states: list[NodeState] | None = None) -> list[Snapshot]:
    """Every array of every family of the lattice, copied: the board at its interval (or the `states` given, frame 0 grown to the board's shape, `frame_grown`), compared bit for bit after a run back and forward (`first_difference`)."""
    return [
        arrays_of(family.name, state)
        for family, state in zip(board.families, board.states if states is None else states, strict=True)
    ]


def first_difference(
    before: list[Snapshot], after: list[Snapshot], where: np.ndarray | None = None
) -> tuple[str, list[int]] | None:
    """The first array and the first Node at which two snapshots differ, or None where they agree bit for bit (a shape that differs named with no Node); with `where`, a mask over the board, the Nodes it names alone (the box's Nodes outside the record's cone, `cone.held`)."""
    for family_before, family_after in zip(before, after, strict=True):
        for (label, was), (_label, now) in zip(family_before, family_after, strict=True):
            if was.shape != now.shape:
                return f"{label} (the shape {list(now.shape)} against {list(was.shape)})", []
            differing = np.argwhere((was != now) if where is None else (was != now) & where)
            if len(differing):
                return label, [int(i) for i in differing[0]]
    return None


def frame_of(board: Lattice) -> list[NodeState]:
    """Frame 0, the lay's state: every family's NodeState as the start laid it, its lines, its write remainders and its phase lines (immutable records, so no array is copied), kept once at the books' start as the reference of every record laid at the start (`credit.Books.reference`; the board at the birth for a record born during the run, `credit.born`) for the cone's assertions (`cone.held`, through `frame_grown` and `credit.Books.regrown`): outside the record's light cone the board stands at frame 0 while the laid rest is an exact fixed point of the step."""
    return [
        NodeState(list(state.lines), list(state.write_remainders), [list(row) for row in state.phases])
        for state in board.states
    ]


def grown(board: Lattice, states: list[NodeState], found: growth.Growth, direction: int) -> None:
    """Frame 0 regrown by one growth of the receding faces in `direction` (+1 as the board grew the layers, -1 as the run back takes them off): every family's NodeState resized as the board's is (`growth.resized`), every grown Node at the state of a Node with no level, the massless row's rest and the half wall."""
    _interval, axis, side, layers = found
    seed = phase.seed(board.amplitude, board.world.node_clock)
    for index, (family, state) in enumerate(zip(board.families, states, strict=True)):
        origin, walls, half = board.origins[index], board.walls(index), board.half_wall(index)
        if (
            index in board.fixed_walls
        ):  # the carried factor: a grown Node is born at the rest's wall, as the board's layer is
            walls = tuple(board.vacuum_walls(index))
        growth.resized(
            state, family, axis, side, layers, origin, walls, direction, board.world.kind, half, seed
        )


def frame_grown(board: Lattice, index: int) -> list[NodeState]:
    """The record's reference over the board as grown (ALGEBRA.md, The births' book, the born record's reference, 2026-10-20): the board as it stood at the record's birth (`credit.Books.reference`, frame 0 for a record laid at the start, the board at the birth for a record born during the run, one mechanism for both), grown by every growth standing that served an interval after the birth (`Lattice.growths`, in their order, the layers the receding faces added before the origin and beyond the far face, `grown`); the cone's own copy, kept in the books through the reading and resized with the growths the run back pops and the run forward finds anew (`credit.Books.regrown`, `cone.stepped_alone`, `cone.grown_at`); the board's own states where the books hold no reference."""
    books = board.credit
    found = (
        frame_of(board)
        if index not in books.reference
        else [
            NodeState(list(s.lines), list(s.write_remainders), [list(r) for r in s.phases])
            for s in books.reference[index]
        ]
    )
    birth = books.births[index][0] if index in books.births else 0
    for growth_found in board.growths:
        if growth_found[0] > birth:
            grown(board, found, growth_found, 1)
    return found


def radius(board: Lattice) -> int:
    """The record's light cone's radius at the board's interval t, (t - t_b) + 1 Links about the birth's Nodes, t_b the birth's interval (`credit.Books.birth`, 0 for a record laid at the start; ALGEBRA.md, the run back's reach: the levels within t - t_b and the remainders within t - t_b + 1, a Node with a lit neighbour walking its remainder before its level leaves 0); the frames' `cone_radius`."""
    return board.interval - board.credit.birth + 1


def node_of(board: Lattice, line: dict[str, object]) -> tuple[int, tuple[int, int, int]]:
    """A LATTICE line's family by its position and its Node at the file's coordinates."""
    names = [family.name for family in board.families]
    at = [int(a) for a in line[reports.LAY_KEYS[3]][reports.AT]]  # type: ignore[index]
    return names.index(str(line[reports.REPORT_KEYS[3]])), (at[0], at[1], at[2])


def faces_from(board: Lattice, lines: Lines) -> None:
    """The faces of a run rebuilt from its `face` lines into the books' log, the log emptied first: per line the family, the line, the Node, the Ports, the interval and the value, so the inverse presents what the lines carry (the host tool's way, tools/back_in_time.py; the engine's own run back presents the books' log whole)."""
    board.credit.faces = {}
    event, when = reports.REPORT_KEYS[0], reports.REPORT_KEYS[2]
    for line in [line for line in lines if line[event] == reports.FACE]:
        index, at = node_of(board, line)
        interval, value = (int(str(line[key])) for key in (when, reports.VALUE))
        ports = tuple(int(str(port)) for port in list(line[reports.PORT_SET]))  # type: ignore[call-overload]
        found = Face(index, int(str(line[reports.LINE])), at, ports, interval, value)
        board.credit.faces.setdefault(interval, []).append(found)


def crossed(board: Lattice, lines: Lines, direction: int = -1) -> None:
    """The lays of the lattice's interval crossed from their `lay` lines by their changes (ALGEBRA.md, The click is the meeting of the future with the past: the backward run brings no new number along the realised orbit, the board is reversible, and the lay is not taken back; the mathematician's hand: the face's part of the inverse; the one write site of the engine beside the lay act's write step, Rule3's step and the cone's write-back of Rule3's own results into the board (`cone.written_back`, the fourth site the writers gate admits)): per line of the interval, in the lines' order forward and reversed back, the Node at the file's coordinates, the line's levels now and before changed by the lay's own change, after less before, added forward and subtracted back, and the remainder: a lay without an origin changes no remainder and the inverse recovers it; a lay with an origin sets it forward and restores the history's own backward, the board's remainder before the setting logged into the line's `before` on the way forward, so that the log holds the history it is replayed in and the next run back restores it (the reader's fix of 2026-10-20, the residual's root: the source's increments carried pass 1's remainders into the rewritten history); so a lay the click's write scaled at the birth (`realised`, the log's copies carrying the scaled levels) replays scaled, and every other lay replays as it was, the board's value equal to the line's at the line's turn by the inverse's theorem; a copy of each array written, nothing in place. The host tool reads the lines from the run's output (tools/back_in_time.py), the engine from the books' log (`logged`)."""
    event, when = reports.REPORT_KEYS[0], reports.REPORT_KEYS[2]
    own = [line for line in lines if line[event] == reports.LAY and line[when] == board.interval]
    for line in own if direction > 0 else reversed(own):
        index, at = node_of(board, line)
        here = on_board(board, at)
        number = int(str(line[reports.LINE]))
        record = board.states[index].lines[number]
        was, after = line[reports.BEFORE], line[reports.AFTER]
        arrays = [np.array(a, copy=True) for a in (record.now, record.before, record.remainder)]
        for array, before_value, after_value in zip(arrays[:2], was[:2], after[:2], strict=True):  # type: ignore[index]
            array[here] += direction * (after_value - before_value)
        if was[2] != after[2]:  # type: ignore[index]  # a lay with an origin: set forward, the history's own back
            if direction > 0:
                line[reports.BEFORE] = [was[0], was[1], int(arrays[2][here])]  # type: ignore[index]
            arrays[2][here] = after[2] if direction > 0 else line[reports.BEFORE][2]  # type: ignore[index]
        board.states[index].lines[number] = Record(arrays[0], arrays[1], arrays[2])


def logged(board: Lattice, direction: int) -> None:
    """The lays the books' log holds at the board's interval, crossed in `direction` (`crossed`; `credit.Books.lays`, filled by `lay.written` where the world's draw runs back): the step at the Nodes alone re-applies them after its Rule3 and the inverse undoes them before its own, so the engine's run back and forward re-present every act from outside the Node from the books; nothing where the log is empty, a world with no record of several parts at declared sides, where the host tool crosses from the lines."""
    crossed(board, board.credit.lays.get(board.interval, []), direction)


def gram_of(patterns: Sequence[Pattern], parts: int) -> list[list[int]]:
    """The Gram matrix of the record's parts over the sides whose port is unrealised (ALGEBRA.md, The meeting's identity, the Gram theorem): the part k stands at each such side in the state its declared pattern row (alpha_k, beta_k) names, two parts' states there have the inner product alpha_k alpha_l + beta_k beta_l, and G_kl is the product over those sides; no side left gives the matrix of ones, the coherent read of the last side; a side whose rows are orthonormal gives the identity, the parts' shares alone (Bell's identity pattern, 1 / 2 at every setting)."""
    found = [[1] * parts for _k in range(parts)]
    for pattern in patterns:
        for k in range(parts):
            for m in range(parts):
                (a_k, b_k), (a_m, b_m) = pattern[k], pattern[m]
                found[k][m] *= a_k * a_m + b_k * b_m
    return found


def coefficients_of(family: FamilyRule, ports: Ports, first: bool) -> list[list[Gauss]]:
    """A side's coefficients per port, the integers its read and its write carry (ALGEBRA.md, The meeting's reading, the write at the birth): the pattern's integers at the setting, e_k(p) (`loader/draw.ports_of`), and for the antisymmetric record at the first side the determinant's, lambda_l = SUM_k sign(l - k) e_k(p) (`terms_of`, the two sides' form), the later side reading and writing its own e_k(p) over the parts already carrying the sign."""
    if family.exchange >= 0 or not first:
        return [list(port) for port in ports]
    found = []
    for port in ports:
        lambdas: list[Gauss] = [(0, 0)] * family.parts
        for sign, (k, m) in credit.terms_of(family.exchange, family.parts, 2):
            lambdas[m] = (lambdas[m][0] + sign * port[k][0], lambdas[m][1] + sign * port[k][1])
        found.append(lambdas)
    return found


def side_weights(
    moments: Sequence[Sequence[Gauss]],
    coefficients: Sequence[Sequence[Gauss]],
    gram: Sequence[Sequence[int]],
) -> list[int]:
    """A side's weights at the window's close, one per port (ALGEBRA.md, The meeting's identity, the Gram theorem): w(p) = SUM_kl c_k(p) c_l(p) G_kl M_kl with its own coefficients c per port (`coefficients_of`), the Gram G of the sides unrealised (`gram_of`) and its own second moments M (`moments_booked`), the chain rule of the joint share in its local form, exact in the integers and at or above 0 exactly, G a Gram and M a Gram so their entrywise product is one (the Schur product) and the form a sum of squares; a negative total is a defect of a coefficient's conjugation or of a moment's book and is refused by name, as `drawn` and `largest_below` refuse theirs."""
    found = []
    for port in coefficients:
        total = 0
        for k, (a, b) in enumerate(port):
            for m, (c, d) in enumerate(port):
                re, im = moments[k][
                    m
                ]  # Re(conj(c_k) c_m M_km), the integers' product where every im is 0
                total += gram[k][m] * ((a * c + b * d) * re - (a * d - b * c) * im)
        if total < 0:
            raise ValueError(
                f"the side's weight at the port {port} is {total}, below 0: the Gram's form with the "
                "Hermitian moments is a sum of squares (ALGEBRA.md, The meeting's identity), so a "
                "negative total is a defect of a coefficient's conjugation or of a moment's book; refused"
            )
        found.append(int(total))
    return found


def inside(board: Lattice) -> np.ndarray:
    """The record's light cone over the whole board at the board's interval, the ball about the birth's Nodes (`credit.Books.support`) at the cone's radius (`radius`, `features/front.ball`): the close's assertion of the cone's outside (`run_forward`)."""
    origins = [on_board(board, at) for at in board.credit.support]
    return ball(board.shape, origins, radius(board), board.world.periodic)


def booked_moments(board: Lattice, index: int) -> None:
    """One reading added to the run forward (ALGEBRA.md, The meeting's reading: the later sides' books taken again from the rewritten record on the way): the parts' sums of the record at every declared region from the state the step starts from (`reports.level_sums`, the numbers the `parts` lines carry), booked into the sides' own books (`moments_booked`); no output line, no number at a Node."""
    lines = board.states[index].lines
    sums = {
        d.name: reports.level_sums(d.nodes, lines)
        for d in board.node_detectors
        if d.declared and d.nodes is not None
    }
    credit.moments_booked(board, index, sums)


def realised(board: Lattice, index: int, coefficients: Sequence[Gauss]) -> None:
    """The click's write at the record's birth (ALGEBRA.md, The click is the meeting of the future with the past: at the root it writes; The meeting's identity, the write's exactness; the owner's word of 2026-10-20, the click writes): the realised port's integer coefficients c_k (`coefficients_of`, the pattern's integers at the setting, the determinant's for the antisymmetric first side) reduced by their greatest common divisor over the record's surviving parts and conjugated, the coefficient written on the term k being the port's overlap with the term, conj(e_k(p)), the port's own integer where the ports are real and the turned unit's conjugate on a plane side with a quarter turn (the two-term plane GHZ, 2026-10-20: the record after the click carries <e(p)|k> on its term k, the side's port contracted against the shared term: for a record read at several sides the other sides' conditional state, the port's own state where one side reads it) (`credit.reduced`, the Boss's amendment of 2026-10-20: the write is the realised term's direction among the parts and never its magnitude alone; a scaling alone, a global sign included, writes nothing and the port is realised all the same) and scaled into the record's parts wherever the record stands at the birth, every line of the part k multiplied by c_k on its two levels, the remainder as the birth left it, through the one lay act (`lay.laid` with no uniform-mode weights, the change (c_k - 1) times the level, `lay.written` with its `lay` lines, the books' log where the birth is after the start), exact in the integers, no division, no rounding; the amplitude bound read first, the largest level times the largest coefficient against A, refused by name where the write would pass it; the cumulative coefficients per part (`credit.Books.written`, 1 before any write), whether the parts stood alike before the first write (`credit.Books.alike`) and the record's scale (`credit.Books.scale`, the norm's square of the coefficients standing on the parts, `credit.scale_of`) kept in the books; every later lay line of the record's own birth in the books' log (a source in time's increments after the birth's interval) replaced by a copy with its levels before and after scaled by c_k, so that the replay by changes applies it scaled (`crossed`); the write asserted: every part's arrays after it the coefficient times the arrays before, bit for bit, refused by name otherwise."""
    books, family, state = board.credit, board.families[index], board.states[index]
    parts, blocks = family.parts, credit.parts_of(family, len(state.lines))
    positions = credit.positions_of(family, len(state.lines))
    scaled = [
        (a, -b) for a, b in credit.reduced(board, index, coefficients)
    ]  # conj(e_k(p)): the term's overlap
    tallest, biggest = (
        max((largest(line) for line in state.lines), default=0),
        max(abs(a) + abs(b) for a, b in scaled),  # the pair (a, b) on a level L reaches (|a| + |b|) L
    )
    if tallest * biggest > board.world.amplitude_bound:
        raise RuntimeError(
            f"the write at the birth would pass the amplitude bound A = {board.world.amplitude_bound} (the level "
            f"{tallest} times the coefficient {biggest}): lower the lay's amplitude or the setting's integers"
        )
    before, standing = list(state.lines), books.written.get(index, [(1, 0)] * parts)
    if index not in books.written:
        width = family.width
        books.alike[index] = all(
            (np.asarray(before[k * width + i].now) == np.asarray(before[i].now)).all()
            and (np.asarray(before[k * width + i].before) == np.asarray(before[i].before)).all()
            and (np.asarray(before[k * width + i].remainder) == np.asarray(before[i].remainder)).all()
            for k in range(1, parts)
            for i in range(width)
        )
    books.written[index] = [times(w, c) for w, c in zip(standing, scaled, strict=True)]
    books.scale[index] = credit.scale_of(board, index)  # the norm's square of the coefficients standing
    if all(
        c == (1, 0) for c in scaled
    ):  # a scaling alone, a unit included: the port realised, nothing written
        return
    changes: dict[int, tuple[Any, Any]] = {}
    for number, line in enumerate(before):
        (a, b), position = scaled[blocks[number]], positions[number]
        if (a, b) == (1, 0):
            continue
        assert (
            family.plane or b == 0
        )  # a coefficient with an imaginary part is a plane side's (the loader's word)
        partner = before[number + 1 - 2 * position] if family.plane else line  # the plane's other line
        sign = (
            -1 if position == 0 else 1
        )  # re' = a re - b im, im' = a im + b re: the plane's two lines move together
        changes[number] = (
            np.asarray(line.now, dtype=object) * (a - 1)
            + np.asarray(partner.now, dtype=object) * (sign * b),
            np.asarray(line.before, dtype=object) * (a - 1)
            + np.asarray(partner.before, dtype=object) * (sign * b),
        )
    for number, change in changes.items():
        laid(board, index, number, change, None, None)
    for number, (was, now) in enumerate(zip(before, state.lines, strict=True)):
        change = changes.get(number, (0, 0))
        exact = (
            (np.asarray(now.now) == np.asarray(was.now, dtype=object) + change[0]).all()
            and (np.asarray(now.before) == np.asarray(was.before, dtype=object) + change[1]).all()
            and (np.asarray(now.remainder) == np.asarray(was.remainder)).all()
        )
        if not exact:
            raise RuntimeError(
                f"the write at the birth of {family.name!r} is not the coefficient {scaled[blocks[number]]} times the "
                f"line {number} bit for bit: the lay act's write step wrote another number"
            )
    birth, names = books.births[index][0], [f.name for f in board.families]
    for interval, lines in books.lays.items():
        if interval <= birth:
            continue
        for position, entry in enumerate(lines):
            if names.index(str(entry[reports.REPORT_KEYS[3]])) != index:
                continue
            c = scaled[blocks[int(str(entry[reports.LINE]))]]
            if c[1] != 0:
                raise RuntimeError(
                    f"the record of {family.name!r} has lays after its birth and the write carries the imaginary part {c}: a later "
                    "lay of a record so written is a declaration the law has not made (the two lines' entries would move "
                    "together); a record laid whole at its birth is read"
                )
            copy = dict(entry)
            for key in (reports.BEFORE, reports.AFTER):
                values = list(entry[key])  # type: ignore[call-overload]
                copy[key] = [values[0] * c[0], values[1] * c[0], values[2]]
            lines[position] = copy


def birth_of(board: Lattice, index: int) -> int:
    """The interval a family's record standing in the books was born at, the root the run back reaches (ALGEBRA.md, The births' book, 2026-10-20): the births' book's interval (`credit.Books.births`, written by the write step for every kind of lay alike, `credit.born`), 0 for a record laid at the start; the run back stops at the state right after the birth's lays, since the inverse undoes an interval's lays before its own step."""
    assert (
        board.credit.counts[index] > 0 and index in board.credit.births
    )  # a record standing, born once
    return board.credit.births[index][0]


def run_back(board: Lattice, index: int) -> Kept:
    """The run back from the close to the birth of the record of the family `index` (ALGEBRA.md, The click is the meeting of the future with the past: the backward run from the first click reaches the root; The births' book: the birth's interval and Nodes from the births' book, `birth_of`, the cone's root the birth's Nodes): the observers called first with the board at the close as Rule3 left it (the frame of the forward run at the close, before any step back; `Lattice.observers`), the board's every array copied with the growths standing (`cone.copied`, `Lattice.growths`; the inverse's exactness asserted on the return, `run_forward`), then `Lattice.step_inverse` interval by interval down to `to`, each step undoing the acts' lays of its interval from the books' log and presenting the faces from it, every array returning bit for bit (the inverse's theorem), and in the cone's reach the cone stepped alone, the ball with its ring and nothing else, shrinking by one Link to the lay's Nodes at the birth (`cone.stepped_alone`; the record's reference regrown kept in the books for the reading, `frame_grown`); the Node-steps counted in the books either way (`cone.counted`); returns the copy."""
    board.passes, board.heading = board.passes + (board.heading < 0), 1
    for observer in board.observers:
        observer(board.interval, 1, board.passes)
    kept, books = (cone.copied(board), list(board.growths)), board.credit
    (books.birth, books.support), to = books.births[index], birth_of(board, index)
    if books.reach == CONE:
        books.regrown = frame_grown(board, index)
    while board.interval > to:
        if books.reach == CONE:
            cone.stepped_alone(board, -1)
        else:
            volume = int(np.prod(board.shape))
            board.step_inverse()
            cone.counted(board, volume)
    return kept


def run_forward(board: Lattice, index: int, to: int, kept: Kept) -> None:
    """The run forward from the birth to the close again (ALGEBRA.md, The click is the meeting of the future with the past: the board runs forward from the rewritten birth by Rule3 at one Link per interval, so that every later side reads the realised term where it stands): `Lattice.step` with no act, interval by interval up to `to`, the step at the Nodes alone with the faces from the books' log and the acts' lays re-applied from it by their changes (`crossed`, the record's own later lays scaled by the write), a computation by Rule3 and no re-presentation of kept frames; in the cone's reach the cone stepped alone as it grows by one Link, the growths of the receding faces replayed from the record's own history (`cone.stepped_alone`); the sides' own books of the record `index` taken again on the way from the rewritten record over the window closing at `to` (`booked_moments`, the books emptied first); then the close's three assertions, refused by name where one fails: outside the record's cone the board equal bit for bit to the copy the run back took, that copy resized as the board was by the growths the run back popped and the run forward found anew (`kept`, `grown`; the rewritten record may reach a receding face at another interval, the grown layers the state of a Node with no level either way, `growth.resized`; `first_difference`; the reading touched nothing outside), every part written 0 at zero levels bit for bit (a zeroed part is Rule3's fixed point), and the parts written alike equal bit for bit where they stood alike at the birth (identical arrays step identically); the shares' deviation from the rationals where the written coefficients differ in magnitude is the law's regime of the remainders' walk, a diagnostic of the tests and no refusal."""
    books, family = board.credit, board.families[index]
    books.moments[index], first = {}, books.window_of(to)[0]
    while board.interval < to:
        if board.interval + 1 >= first:
            booked_moments(board, index)
        if books.reach == CONE:
            cone.stepped_alone(board, 1)
        else:
            board.step(False)
            cone.counted(board, int(np.prod(board.shape)))
    states, growths = kept
    shared = 0
    while shared < min(len(growths), len(board.growths)) and growths[shared] == board.growths[shared]:
        shared += 1
    for popped in reversed(growths[shared:]):
        grown(board, states, popped, -1)
    for added in board.growths[shared:]:
        grown(board, states, added, 1)
    found = first_difference(snapshot(board, states), snapshot(board), ~inside(board))
    if found is not None:
        raise RuntimeError(
            f"the run back and forward of the meeting returned to the interval {board.interval} with the array "
            f"{found[0]} differing at the Node {found[1]} outside the record's cone: the inverse is exact or the "
            "meeting is not read"
        )
    written, state = books.written.get(index, [(1, 0)] * family.parts), board.states[index]
    for number, (part, line) in enumerate(
        zip(credit.parts_of(family, len(state.lines)), state.lines, strict=True)
    ):
        if written[part] == (0, 0) and (np.asarray(line.now).any() or np.asarray(line.before).any()):
            raise RuntimeError(
                f"the part {part} of {family.name!r} written 0 at the birth did not stay at 0 to the close (the line "
                f"{number}): a zeroed part is Rule3's fixed point, or the meeting is not read"
            )
    if books.alike.get(index):
        width = family.width
        for k in range(1, family.parts):
            if written[k] != written[0]:
                continue
            for i in range(width):
                one, other = state.lines[i], state.lines[k * width + i]
                alike = (
                    (np.asarray(one.now) == np.asarray(other.now)).all()
                    and (np.asarray(one.before) == np.asarray(other.before)).all()
                    and (np.asarray(one.remainder) == np.asarray(other.remainder)).all()
                )
                if not alike:
                    raise RuntimeError(
                        f"the parts 0 and {k} of {family.name!r}, written alike at the birth, parted by the close "
                        f"(the line {k * width + i}): parts alike step alike by one rule, or the meeting is not read"
                    )
