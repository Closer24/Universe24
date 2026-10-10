"""Part F, Task 1: the lattice momentum as a reading (features/currents `momentum`, node.momentum_of; the advisor's and the mathematician's lines of 2026-10-09, momentum from Rule3, 6083929632 and 6084001231). The normalisation chosen and stated: P_a = SUM_i (F_(i,i-a) - F_(i,i+a)) in the current's own unit, F_ij = num (now_i before_j - before_i now_j), so P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a)), the mathematician's with the current's weight; a plane wave cos(k x - omega t) has P_a of the sign of +k. (a) On a periodic chain of 24 with a plane wave the rational mirror of the vacuum form conserves P exactly over 200 intervals and the engine's integers drift below the hands' bound per step, 2 num SUM_i |now_(i+a) - now_(i-a)| in this unit (the remainders' walk, |delta_i| < 1 per Node and the two Links each see it); (b) the plane wave's P over the action it holds is the s-integer of the phase pair at the angle k over the amplitude, in T's unit, the cosine read from the record itself and the pair found by bisection on the phase line, no sine on the engine's side; (c) in a static well held by the harness P changes per step by the gradient term exactly as the rational step at the engine's own integers predicts, to the floor, and over the run the packet gains P toward the well, the fall. The measured integers are printed for the Boss."""

import copy
import json
import math
import time
from dataclasses import replace
from fractions import Fraction

import numpy as np

from event_universe import node, twist, world_files
from event_universe.core.rule3 import division_forward
from event_universe.features import phase
from event_universe.lattice import Lattice
from event_universe.reports import (
    LOST_TO_DECLARATION,
    LOST_TO_LAY,
    LOST_TO_REGION,
    LOST_TO_TAKER,
)
from event_universe.world_files import load_world
from tests import laws
from tests.laws import EVENTS, GRAVITY, one_photon_board, world_beside

GAMMA, T, UNIT, CHAIN = 6000, 32768, 16, 24
LIGHT = {"name": "light", "pair": [GAMMA, GAMMA], "reads": {}, "dimension": 1}
INTEGERS = {"node_clock": GAMMA, "quantum_action": T, "width": 63, "link_unit": UNIT}


def chain_world(tmp_path, families, chain=CHAIN, boundary="periodic"):  # type: ignore[no-untyped-def]
    """A chain of `chain` Nodes, x `boundary`, y and z folded, no body and no packet: the records laid by hand."""
    (tmp_path / "u.json").write_text(
        json.dumps({"integers": INTEGERS, "families": families}), encoding="utf-8"
    )
    (tmp_path / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())
    world = dict(
        shape=[chain, 1, 1], boundary=dict(x=boundary, y="periodic", z="periodic"), face_depth=1
    )
    world.update(intervals=400, universe="u.json", engine="e.json", bodies=[], node_detectors=[])
    (path := tmp_path / "chain.json").write_text(json.dumps(world), encoding="utf-8")
    return path


def plane_wave(board: Lattice, index: int, amplitude: int, wave: tuple[int, int], envelope=None):  # type: ignore[no-untyped-def]
    """A real plane wave cos(k x) at the wave number pi p / q per Link laid by hand on the family's one line, the level before advanced by the band's own omega(k) at the vacuum's paces (the test's floats lay; the engine reads no sine), under `envelope` where one is given."""
    family, chain = board.families[index], board.shape[0]
    reads, self_coefficient, wall = node.rule_of(family, GAMMA, 0, None, board.unit)
    k = math.pi * wave[0] / wave[1]
    cosine = (
        int(self_coefficient) + 2 * int(reads[0]) * math.cos(k) + sum(int(r) for r in reads[2:])
    ) / (2 * int(wall))
    omega, x = math.acos(cosine), np.arange(chain)
    shape = amplitude * (np.ones(chain) if envelope is None else envelope)
    now = np.rint(shape * np.cos(k * x)).astype(board.kind).reshape(board.shape)
    before = np.rint(shape * np.cos(k * x + omega)).astype(board.kind).reshape(board.shape)
    line = board.states[index].lines[0]
    board.states[index].lines = [node.Record(now, before, line.remainder)]
    return reads, self_coefficient, wall


def momentum_fraction(levels_now, levels_before, num: int) -> Fraction:  # type: ignore[no-untyped-def]
    """The test's own P_x on a periodic chain in exact rationals, the same antisymmetric sum."""
    chain, total = len(levels_now), Fraction(0)
    for i in range(chain):
        behind, ahead = (i - 1) % chain, (i + 1) % chain
        total += num * (levels_now[i] * levels_before[behind] - levels_before[i] * levels_now[behind])
        total -= num * (levels_now[i] * levels_before[ahead] - levels_before[i] * levels_now[ahead])
    return total


def rational_step(now, before, reads, self_coefficient, wall, periodic=True):  # type: ignore[no-untyped-def]
    """One interval of the vacuum form in exact rationals, next = M now - before, M per Node from the rule's integers (a list per Node where the paces vary): the chain's two x Ports and the four folded Ports reading the Node itself."""
    chain, found = len(now), []
    for i in range(chain):
        r, s, w = (
            (reads[i], self_coefficient[i], wall[i])
            if isinstance(reads, list)
            else (reads, self_coefficient, wall)
        )
        behind, ahead = ((i - 1) % chain, (i + 1) % chain) if periodic else (i - 1, i + 1)
        arrived = (now[behind] if periodic or i > 0 else 0) * int(r[1])
        arrived += (now[ahead] if periodic or i < chain - 1 else 0) * int(r[0])
        total = int(s) * now[i] + arrived + sum(int(v) for v in r[2:]) * now[i]
        found.append(total / int(w) - before[i])
    return found


def bound_of(board: Lattice, index: int) -> int:
    """The hands' bound on the integers' drift per step in this unit, 2 num SUM_i |now_(i+a) - now_(i-a)| along x."""
    now = board.states[index].lines[0].now.reshape(-1).astype(object)
    chain = len(now)
    return (
        2
        * board.families[index].pair[0]
        * int(sum(abs(now[(i + 1) % chain] - now[(i - 1) % chain]) for i in range(chain)))
    )


def pair_at_cosine(board: Lattice, numerator: int, denominator: int) -> tuple[int, int, int]:
    """The phase pair at the angle whose cosine is numerator / denominator, found by bisection on the phase line as `paces.rotation_unit` finds the rest rotation: n acts, (c, s) at the amplitude X; no sine."""
    amplitude, gamma = board.amplitude, board.world.node_clock
    low, high, pair = 0, 2 * gamma, phase.seed(board.amplitude, gamma)
    while high - low > 1:
        middle = int(division_forward(low + high, 2, 0)[0])
        probe = phase.iterate(pair, middle - low, gamma)
        if int(phase.read(probe)[0]) * denominator >= amplitude * numerator:
            low, pair = middle, probe
        else:
            high = middle
    c, s = phase.read(pair)
    return low, int(c), int(s)


def test_the_momentum_is_conserved_exactly_in_the_mirror_and_to_the_floor_on_the_integers(
    tmp_path, monkeypatch
):
    """(a) A plane wave at k = pi / 4 on the periodic chain of 24 at the amplitude 8,000 (the world's bound 9,266): the rational mirror of the vacuum form keeps P_x bit for bit over 200 intervals; the engine's integer P_x moves per step below the hands' bound 2 num SUM |now_(i+1) - now_(i-1)| and the drift over the run is printed; P_y = P_z = 0 on the folded axes."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    started = time.perf_counter()
    board = Lattice(load_world(chain_world(tmp_path, [LIGHT])))
    reads, self_coefficient, wall = plane_wave(board, 0, 8000, (1, 4))
    num = board.families[0].pair[0]
    lines = board.states[0].lines
    now = [Fraction(int(v)) for v in lines[0].now.reshape(-1)]
    before = [Fraction(int(v)) for v in lines[0].before.reshape(-1)]
    mirror, first = momentum_fraction(now, before, num), node.momentum_of(num, lines, board.wrap)
    assert first[0] > 0 and first[1:] == (0, 0) and Fraction(first[0]) == mirror  # +k: P of k's sign
    steps, bounds, last = [], [], first[0]
    for _ in range(200):
        bound = bound_of(board, 0)
        now, before = rational_step(now, before, reads, self_coefficient, wall), now
        assert momentum_fraction(now, before, num) == mirror  # the theorem: exact at uniform paces
        board.step()
        found = node.momentum_of(num, board.states[0].lines, board.wrap)
        steps.append(found[0] - last)
        bounds.append(bound)
        assert abs(found[0] - last) < bound and found[1:] == (0, 0)
        last = found[0]
    drift = last - first[0]
    print(
        f"Part F (a): P_x = {first[0]}, 200 intervals, the mirror exact; the integers' drift {drift} "
        f"({drift / first[0]:.2e} of P), the largest step {max(abs(s) for s in steps)} under the bound "
        f"{min(bounds)}..{max(bounds)}; {time.perf_counter() - started:.1f} s"
    )


def test_the_plane_waves_momentum_over_its_action_is_the_pairs_s_integer(tmp_path, monkeypatch):
    """(b) The same plane wave: cos k read from the record itself, 2 cos k = SUM now_i (now_(i+1) + now_(i-1)) / SUM now_i^2, the pair at k by bisection on the phase line (n_k acts, c_k, s_k) and the pair at the band's omega(k) from the rule's own line 2 w cos omega = S + 2 R cos k + 4 R (n_omega, s_omega); Part F2, both hands' unit (6085442608, 6085486079): one quantum of action is SUM over lines and Nodes of A^2 sin omega = T, and the record's quanta of action are its share over (3 den T sin omega) (the engine's share 3 den A^2 sin^2 omega per Node), so P_x over num and over the quanta, P_x 3 den s_omega T over (num share X), stands against the whole quantum's 2 T s_k / X (T sin k per Link once, each Link twice in the antisymmetric sum) to the lay's rounding; both integers printed, with the engine's count of the record in W_c for the Boss (a W_c count is 1 / sin omega quanta of action and carries 2 T sin k / sin omega)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(chain_world(tmp_path, [LIGHT])))
    reads, self_coefficient, wall = plane_wave(board, 0, 8000, (1, 4))
    family, lines = board.families[0], board.states[0].lines
    num, den = family.pair
    now = lines[0].now.reshape(-1).astype(object)
    chain = len(now)
    numerator = int(sum(now[i] * (now[(i + 1) % chain] + now[(i - 1) % chain]) for i in range(chain)))
    denominator = 2 * int(sum(now[i] * now[i] for i in range(chain)))
    n_k, c_k, s_k = pair_at_cosine(board, numerator, denominator)
    amplitude = board.amplitude
    band_numerator = (
        int(self_coefficient) * amplitude
        + 2 * int(reads[0]) * c_k
        + sum(int(r) for r in reads[2:]) * amplitude
    )
    n_omega, c_omega, s_omega = pair_at_cosine(board, band_numerator, 2 * int(wall) * amplitude)
    momentum = node.momentum_of(num, lines, board.wrap)[0]
    share = board.total_share(0)[0]
    assert share is not None and momentum > 0
    hands = int(division_forward(2 * T * s_k, amplitude, division_forward(amplitude, 2, 0)[0])[0])
    engine_wall = num * share * amplitude
    engine = int(
        division_forward(
            momentum * 3 * den * s_omega * T, engine_wall, division_forward(engine_wall, 2, 0)[0]
        )[0]
    )
    count = Fraction(share, 3 * den * T)
    print(
        f"Part F (b): n_k = {n_k}, s_k / X = {s_k / amplitude:.6f} (sin pi/4 = {math.sin(math.pi / 4):.6f}), n_omega = {n_omega}, "
        f"s_omega / X = {s_omega / amplitude:.6f}; P over the quanta of action: the engine's reading {engine} against 2 T s_k / X = {hands} "
        f"(the difference {engine - hands}); P_x = {momentum}, share = {share}, the engine's count {float(count):.3f} W_c, "
        f"P_x / (num count T) = {momentum / (num * count * T):.4f} = 2 sin k / sin omega to the lay's rounding"
    )
    assert abs(engine - hands) <= 8  # the lay's rounding at A = 8,000: a few units of 2 T's 46,341


def test_in_a_held_well_the_momentum_changes_by_the_gradient_term_and_falls_toward_the_well(
    tmp_path, monkeypatch
):
    """(c) A packet (the plane wave at k = pi / 4 under a raised-cosine envelope over 12 Nodes) on an open chain of 48 beside a well of the content, the gravity row's level raised by a bump of 400 over 9 Nodes at the far side and held static by the harness each interval (the hands' non-uniform static paces): per step the engine's integer Delta P_x equals the rational step's at the engine's own integers per Node (the gradient term; 0 at uniform paces) to the floor 2 num SUM |now_(i+1) - now_(i-1)|, and over 30 intervals P_x grows toward the well, the fall; the integers printed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    light = dict(LIGHT, reads={"gravity": 1})
    board = Lattice(load_world(chain_world(tmp_path, [GRAVITY, light], 48, "open")))
    gravity, index = 0, 1
    x = np.arange(48)
    envelope = np.where((x >= 4) & (x < 16), np.sin(np.pi * (x - 3) / 13) ** 2, 0.0)
    plane_wave(board, index, 6000, (1, 4), envelope)
    well = np.where(abs(x - 36) <= 4, np.rint(400 * np.cos(np.pi * (x - 36) / 10) ** 2), 0).astype(
        board.kind
    )
    row = board.states[gravity].lines[0]
    level = (row.now + well.reshape(board.shape)).astype(board.kind)
    board.states[gravity].lines[0] = node.Record(level, level.copy(), row.remainder)
    kept = (
        list(board.states[gravity].lines),
        [r.copy() for r in board.states[gravity].write_remainders],
    )
    num = board.families[index].pair[0]
    first = node.momentum_of(num, board.states[index].lines, board.wrap)[0]
    last, misses = first, []
    for _ in range(30):
        content = board.read(index, 1, 0)[0]
        rules = [
            node.rule_of(
                board.families[index], GAMMA, int(np.asarray(content).reshape(-1)[i]), None, board.unit
            )
            for i in range(48)
        ]
        reads, self_coefficient, wall = ([r[k] for r in rules] for k in range(3))
        lines = board.states[index].lines
        now = [Fraction(int(v)) for v in lines[0].now.reshape(-1)]
        before = [Fraction(int(v)) for v in lines[0].before.reshape(-1)]
        predicted = momentum_fraction(
            rational_step(now, before, reads, self_coefficient, wall, False), now, num
        ) - Fraction(last)
        bound = bound_of(board, index)
        board.step()
        board.states[gravity].lines = list(kept[0])
        board.states[gravity].write_remainders = [r.copy() for r in kept[1]]
        found = node.momentum_of(num, board.states[index].lines, board.wrap)[0]
        misses.append(abs(Fraction(found - last) - predicted))
        assert abs(Fraction(found - last) - predicted) < bound
        last = found
    assert last > first  # the packet moves toward +x where the well stands: P_x grows, the fall
    print(
        f"Part F (c): P_x {first} -> {last} over 30 intervals toward the well (+{last - first}); the integer step against the "
        f"rational step's gradient term: the largest miss {float(max(misses)):.0f} under the floor"
    )


def test_the_piece_is_booked_at_the_detector_with_its_momentum_and_the_fans(tmp_path, monkeypatch):
    """Tasks 2 and 5, rebooked in Part F2 (both hands' correction, 6085442608 and 6085486079): one_photon to the click of 48 at body 0, the piece arriving from the right: the credit line carries `momentum` [p_x, 0, 0], one credited count's momentum, the photon's momentum terms at the atom's two Nodes over its share there times W_rec, read at the close (`node_detector.piece_momentum`), p_x below 0, the sign of travel; it stands within ten percent of the whole left packet's own P W_rec / (W num) read at 47 (the region's two Nodes read the packet's local wave number at its edge), and against 2 T sin(pi / 4) = 46,341, one quantum of action's p, it carries W_rec's worth: on one_photon one count is the two packets' lay, W_rec = 0.956 W_c = 2.2 quanta of action (the mathematician's "W_rec count 100,289"), so the booked p is about twice 46,341 and not 46,341 itself (the Boss's number presumed a one-quantum count: a decision reported, not hidden); `fan` the photon's P over the board at the click in the same unit (688, a true P, the two packets near cancelling), and the deficit fan minus the piece, the three integers printed; the twin without the draw books nothing: no books, no credit line."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board, lines = one_photon_board(tmp_path)
    light = next(i for i, f in enumerate(board.families) if f.name == "photon")
    num = board.families[light].pair[0]
    for _ in range(47):
        board.step()
    left = (np.arange(board.shape[0]) < 48).reshape(board.shape)
    packet_momentum = node.momentum_of(num, board.lines_of(light, 0), board.wrap, left)[0]
    packet_share = int(board.share_of(light, 1, left)[0][left].sum(dtype=object))
    per_count = packet_momentum * board.credit.units[light] / (packet_share * num)
    board.step()
    credits = [line for line in lines if line["event"] == "credit"]
    assert len(credits) == 1 and credits[0]["interval"] == 48 and credits[0]["absorbed"] == "photon"
    piece, fan = credits[0]["momentum"], credits[0]["fan"]
    assert piece[0] < 0 and piece[1:] == [0, 0] and fan[1:] == [0, 0]
    assert abs(piece[0] - per_count) * 10 < abs(per_count)  # the region reads the packet's own ratio
    deficit = [a - b for a, b in zip(fan, piece, strict=True)]
    assert deficit[0] > 0 and abs(deficit[0] + piece[0]) < abs(piece[0])  # the fan near symmetric
    quantum = 2 * T * math.sin(math.pi / 4)
    print(
        f"Part F2 (Tasks 1, 5): the piece's p = {piece}, the fan's P = {fan}, the deficit {deficit}; "
        f"the whole left packet's P W_rec / (W num) at 47 = {per_count:.0f} (P / num = {packet_momentum / num:.0f}, "
        f"W = {packet_share / 589824000:.3f} W_c), W_rec = {board.credit.units[light] / 589824000:.3f} W_c; "
        f"|p_x| against 2 T sin(pi / 4) = {quantum:.0f}: {abs(piece[0]) / quantum:.3f} of it"
    )
    twin, twin_lines = one_photon_board(tmp_path, draw=False)
    for _ in range(48):
        twin.step()
    assert not twin.credit.bodies
    assert not [line for line in twin_lines if line["event"] == "credit"]
    assert board.credit.counts[light] == 0 and twin.credit.counts[light] == 1


def test_the_write_twists_the_taker_to_the_pieces_momentum_or_books_the_loss(tmp_path, monkeypatch):
    """Task 3: (a) on one_photon at the click of 48 the atom (two Nodes along x) is folded: its P_x after the write less before has the piece's sign and the credit line carries the twist n_x; the piece's |p_x| exceeds what the two-Node atom at its lay amplitude (A = 90 per Node, 2 T rho sin delta at most T) can carry, so `lost` reads "P lost to the taker" (Part G: with "recoil lost to the lay" after it, the file's packets having no emitting body) and n_x is the quarter turn, the most the taker takes (printed: the taker's P before and after, n_x, |p_x|); (b') the reachable case, `twist.twisted` on the second atom's ground part at a p_x within its reach: the part's P_x grows by exactly p_x to the floor (two units per Node of the fold's roundings) with nothing lost; (c) the twist is a rotation: the taker's count is unchanged by the fold and the share's change is printed; (b) a one-Node taker books "P lost to the declaration", nothing folded and its lines unchanged."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board, lines = one_photon_board(tmp_path)
    atom = next(i for i, f in enumerate(board.families) if f.name == "atom")
    for _ in range(47):
        board.step()
    before = twist.fan_momentum(board, atom)
    board.step()
    after = twist.fan_momentum(board, atom)
    credits = [line for line in lines if line["event"] == "credit"]
    piece, turned, lost = credits[0]["momentum"], credits[0]["twist"], credits[0]["lost"]
    quarter = twist.quarter_turn(board)
    assert before == (0, 0, 0) and after[0] < 0 and after[0] * piece[0] > 0
    assert lost == [LOST_TO_TAKER, LOST_TO_LAY] and turned == [-quarter, 0, 0]  # Part G: the lay's case
    assert abs(after[0]) < abs(piece[0])
    print(
        f"Part F (Task 3a): the taker's P_x before {before[0]} and after {after[0]}, n_x = {turned[0]} "
        f"(the quarter turn {quarter}), the piece's p_x = {piece[0]}: {lost}, the loss {abs(piece[0]) - abs(after[0])} "
        f"(the two-Node atom's reach 4 SUM A^2 = {4 * 2 * 90 * 90} at most; no taker of this lay carries one count of one_photon's photon)"
    )
    # (b') the reachable case on the second atom, standing in its ground part at 48
    books = board.credit.bodies[1]
    wanted = 10000
    shares_before = board.share_of(atom, 1, board.mask(books.nodes))[0]
    count_before = board.quanta(atom, board.mask(books.nodes))[0]
    standing = twist.fan_momentum(board, atom)[0]
    found, nothing = twist.twisted(board, books, books.part, (wanted, 0, 0))
    gained = twist.fan_momentum(board, atom)[0] - standing
    assert nothing is None and found[1:] == [0, 0] and 0 < found[0] < quarter
    at = board.mask(books.nodes)
    floor = 2 * sum(int(np.abs(r.now.astype(object))[at].sum()) for r in board.states[atom].lines)
    assert abs(gained - wanted) <= floor, (
        gained,
        wanted,
        floor,
    )  # one level unit per rounding, the neighbour's level each
    shares_after = board.share_of(atom, 1, board.mask(books.nodes))[0]
    count_after = board.quanta(atom, board.mask(books.nodes))[0]
    assert np.array_equal(count_before, count_after)
    moved = int((shares_after - shares_before)[board.mask(books.nodes)].sum(dtype=object))
    held = int(shares_before[board.mask(books.nodes)].sum(dtype=object))
    print(
        f"Part F (Task 3b', 3c): p_x = {wanted} asked, {gained} given by n_x = {found[0]} acts (the floor {floor}); the share "
        f"over the taker's Nodes {held} moved by {moved} ({moved / held:.2e}), the count unchanged"
    )
    # (b) the one-Node taker: the second atom's books on its first Node alone
    single = replace(books, nodes=books.nodes[:1], weights=books.weights[:1])
    kept = [(r.now.copy(), r.before.copy(), r.remainder.copy()) for r in board.states[atom].lines]
    found, lost = twist.twisted(board, single, single.part, (wanted, 0, 0))
    assert found == [0, 0, 0] and lost == LOST_TO_DECLARATION and len(single.nodes) == 1
    assert all(
        np.array_equal(a, b)
        for r, k in zip(board.states[atom].lines, kept, strict=True)
        for a, b in zip((r.now, r.before, r.remainder), k, strict=True)
    )


def test_the_reversal_through_the_click_is_bit_for_bit_with_the_twist(tmp_path, monkeypatch):
    """Task 4: one_photon 100 intervals forward through the click of 48 and back to the lay with the books, the faces from the `face` lines and every lay, the twist's among them, crossed from the `lay` lines as the BACK gate does: MATCH, every array of every family at every interval."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    started = time.perf_counter()
    board, _lines = one_photon_board(tmp_path)
    verdict = laws.BACK.verdict(board, 100)
    assert verdict["verdict"] == "MATCH", verdict
    print(
        f"Part F (Task 4): one_photon 100 forward and back through the click of 48: MATCH; {time.perf_counter() - started:.1f} s"
    )


def rounding_floor(board: Lattice, index: int, at: np.ndarray) -> float:
    """The floor of a piece's p from the lay's roundings in p's own unit (the two hands' lines of 2026-10-09, Part F2 Task 3: one level unit per Node per rounding times the neighbours' levels, as Task 3b's floor was computed): P's floor 2 num SUM over the record's lines and the region's Nodes of (|now| + |before|), each level's unit of rounding meeting the neighbour's level on two Links, scaled as the piece is, by W_rec over the region's share and over num, and one more for the piece's own rounding half up."""
    lines = board.lines_of(index, 0)
    levels = sum(
        int(np.abs(r.now.astype(object))[at].sum()) + int(np.abs(r.before.astype(object))[at].sum())
        for r in lines
    )
    share = int(board.share_of(index, 1, at)[0][at].sum(dtype=object))
    return 2 * levels * board.credit.units[index] / share + 1


def test_the_pairs_two_pieces_are_back_to_back_over_twenty_seeds(tmp_path, monkeypatch):
    """Part F2, Task 3 (both hands' lines of 2026-10-09: the tolerance 1 in src was a declared number; the pieces' p are booked as integers and the test judges): Bell's shipped world a b (two packets of the pair, back to back from the centre, one region per side) over 20 seeds of the draw, the board stepped once to 99 and copied per seed with the generator at the seed for the window's close at 100: the two credited pieces' p_x are opposite in sign and their sum, reported, stands below the computed floor of the two lays' roundings (`rounding_floor`, read at the close on the twin whose levels still stand); `lost` carries nothing but Part G's "recoil lost to the lay" on every pair line (the pair is the file's lay), nothing booked under a tolerance; the realised port combinations over the seeds printed with the pieces' sums (the J statistics of the draw, left to the seed)."""
    world_files.REPOSITORY_ROOT = EVENTS.parents[1]
    board = Lattice(load_world(EVENTS / "bell" / "bell_a_b.json"), [].append)
    pair = next(i for i, f in enumerate(board.families) if f.name == "light_pair")
    for _ in range(99):
        board.step()
    sums, realised, lost, size, floors = [], [], [], 0, []
    for seed in range(20):
        twin = copy.deepcopy(board)
        twin.output, twin.credit.state = (lines := []).append, seed + 1
        twin.step()
        credits = [line for line in lines if line["event"] == "credit"]
        assert len(credits) == 2 and {c["node_detector"] for c in credits} == {"left", "right"}
        left, right = sorted(credits, key=lambda c: str(c["node_detector"]))
        sums.append([a + b for a, b in zip(left["momentum"], right["momentum"], strict=True)])
        realised.append(f"{left['realised']} {right['realised']}")
        lost += [
            r for c in credits if c["lost"] for r in c["lost"] if r != LOST_TO_REGION
        ]  # Part H, MUST 5: a region taker books the piece's P lost to the region (no +p of its own); Part G's "recoil lost to the lay" is a body's reading
        size = abs(left["momentum"][0])
        floors.append(
            sum(
                rounding_floor(twin, pair, d.nodes)
                for d in twin.node_detectors
                if d.declared and d.nodes is not None
            )
        )
        assert left["momentum"][0] * right["momentum"][0] < 0  # opposite signs along x
    largest = max(abs(s[0]) for s in sums)
    counted = {key: realised.count(key) for key in sorted(set(realised))}
    print(
        f"Part F2 (Task 3): Bell a b over 20 seeds, the pieces' p_x sums {sorted({s[0] for s in sums})} "
        f"against |p_x| = {size}, the largest |sum| {largest} ({largest / size:.2e}) under the lays' floor {min(floors):.0f}; "
        f"the realised ports {counted}; `lost` booked {len(lost)} times of 40 pair lines"
    )
    assert all(s[1:] == [0, 0] for s in sums) and largest <= min(floors) and lost == []


def test_a_taker_across_the_periodic_wrap_folds_by_consecutive_offsets(tmp_path, monkeypatch):
    """Part F2, Task 4 (the mathematician's line of 2026-10-09: twist.twisted's offsets failed across a periodic wrap): one_photon's world made a periodic chain of 96 with no packet and no receding face, the first atom at the Nodes (95, 0) across the wrap and the second at (40, 41) in the middle; `twist.twisted` asked the same p_x of each ground part gives the same n_x and the same deposit, the taker across the wrap folded by the offsets 0, 1 (`core/ports.run_offsets`) and not 95, 0; the integers printed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)

    def edit(world):  # type: ignore[no-untyped-def]
        world["boundary"]["x"], world["packets"] = "periodic", []
        world.pop("receding", None)
        world["bodies"][0]["nodes"] = [
            {"node": [95, 0, 0], "weight": 1},
            {"node": [0, 0, 0], "weight": 1},
        ]
        world["bodies"][1]["nodes"] = [
            {"node": [40, 0, 0], "weight": 1},
            {"node": [41, 0, 0], "weight": 1},
        ]

    board = Lattice(
        load_world(world_beside(tmp_path, EVENTS / "anticoincidence" / "one_photon.json", edit))
    )
    atom = next(i for i, f in enumerate(board.families) if f.name == "atom")
    assert board.wrap.x and [b.nodes for b in board.credit.bodies] == [
        ((95, 0, 0), (0, 0, 0)),
        ((40, 0, 0), (41, 0, 0)),
    ]
    wanted, deposits, twists = 10000, [], []
    for books in board.credit.bodies:
        standing = twist.fan_momentum(board, atom)[0]
        found, lost = twist.twisted(board, books, books.part, (wanted, 0, 0))
        deposits.append(twist.fan_momentum(board, atom)[0] - standing)
        twists.append(found[0])
        assert lost is None and found[1:] == [0, 0]
    print(
        f"Part F2 (Task 4): p_x = {wanted} asked of the taker across the wrap (95, 0) and of the taker (40, 41): "
        f"the deposits {deposits}, n_x {twists}"
    )
    assert deposits[0] == deposits[1] and twists[0] == twists[1] and 0 < deposits[0] <= wanted
