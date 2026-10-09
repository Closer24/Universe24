"""Part F, Task 1: the lattice momentum as a reading (features/currents `momentum`, node.momentum_of; the advisor's and the mathematician's lines of 2026-10-09, momentum from Rule3, 6083929632 and 6084001231). The normalisation chosen and stated: P_a = SUM_i (F_(i,i-a) - F_(i,i+a)) in the current's own unit, F_ij = num (now_i before_j - before_i now_j), so P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a)), the mathematician's with the current's weight; a plane wave cos(k x - omega t) has P_a of the sign of +k. (a) On a periodic chain of 24 with a plane wave the rational mirror of the vacuum form conserves P exactly over 200 intervals and the engine's integers drift below the hands' bound per step, 2 num SUM_i |now_(i+a) - now_(i-a)| in this unit (the remainders' walk, |delta_i| < 1 per Node and the two Links each see it); (b) the plane wave's P over the action it holds is the s-integer of the phase pair at the angle k over the amplitude, in T's unit, the cosine read from the record itself and the pair found by bisection on the phase line, no sine on the engine's side; (c) in a static well held by the harness P changes per step by the gradient term exactly as the rational step at the engine's own integers predicts, to the floor, and over the run the packet gains P toward the well, the fall. The measured integers are printed for the Boss."""

import copy
import json
import math
import time
from dataclasses import replace
from fractions import Fraction

import numpy as np

from event_universe import meeting, node, world_files
from event_universe.core.rule3 import division_forward
from event_universe.features import phase
from event_universe.lattice import Lattice
from event_universe.reports import LOST_TO_DECLARATION, LOST_TO_TAKER, NO_BACK_TO_BACK
from event_universe.world_files import input_digest, load_world
from tests import laws
from tests.laws import EVENTS

GAMMA, T, UNIT, CHAIN = 6000, 32768, 16, 24
LIGHT = {"name": "light", "pair": [GAMMA, GAMMA], "reads": {}, "dimension": 1}
GRAVITY = {
    "name": "gravity",
    "pair": [GAMMA, GAMMA],
    "reads": {"gravity": 1},
    "held": {"sources": ["form"], "level_weight": 1000, "write_weight": 1, "rest": 60, "act": "pace"},
}
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
    """(b) The same plane wave: cos k read from the record itself, 2 cos k = SUM now_i (now_(i+1) + now_(i-1)) / SUM now_i^2, the pair at k by bisection on the phase line (n_k acts, c_k, s_k) and the pair at the band's omega(k) from the rule's own line 2 w cos omega = S + 2 R cos k + 4 R (n_omega, s_omega); the record's action in the hands' sense 2 SUM A^2 sin omega is its share over (3 den sin omega / 2) (the engine's share 3 den A^2 sin^2 omega per Node), so sin k in T's unit read from the engine, P_x 3 den s_omega T over (2 num share X), stands against T s_k / X to the lay's rounding; both integers printed, with the engine's count of the record in W_c for the Boss (the engine's W_c = 3 den T on the share 3 den A^2 sin^2 omega differs from the hands' quantum 2 A^2 sin omega = T by 2 / sin omega: a decision the law lines did not fix)."""
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
    hands = int(division_forward(T * s_k, amplitude, division_forward(amplitude, 2, 0)[0])[0])
    engine_wall = 2 * num * share * amplitude
    engine = int(
        division_forward(
            momentum * 3 * den * s_omega * T, engine_wall, division_forward(engine_wall, 2, 0)[0]
        )[0]
    )
    count = Fraction(share, 3 * den * T)
    print(
        f"Part F (b): n_k = {n_k}, s_k / X = {s_k / amplitude:.6f} (sin pi/4 = {math.sin(math.pi / 4):.6f}), n_omega = {n_omega}, "
        f"s_omega / X = {s_omega / amplitude:.6f}; sin k in T's unit: the engine's reading {engine} against T s_k / X = {hands}; "
        f"P_x = {momentum}, share = {share}, the engine's count {float(count):.3f} W_c, P_x / (num count T) = {momentum / (num * count * T):.4f} "
        f"= 2 sin k / sin omega to the lay's rounding"
    )
    assert abs(engine - hands) <= 4  # the lay's rounding at A = 8,000: a few units of T's 23,170


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


def one_photon_board(tmp_path, draw: bool = True):  # type: ignore[no-untyped-def]
    """The anticoincidence world's one photon (examples/events/anticoincidence/one_photon.json) with its committed mode file, its output kept, the repository root the host's; without `draw` the bodies' node_detector keys are dropped (the twin that books nothing), the world copied under tmp_path at its repository paths with its universe, the engine's start and its mode file at the twin's digest."""
    source = EVENTS / "anticoincidence" / "one_photon.json"
    if draw:
        world_files.REPOSITORY_ROOT = EVENTS.parents[1]
        return Lattice(load_world(source), (lines := []).append), lines
    world = json.loads(source.read_text(encoding="utf-8"))
    for body in world["bodies"]:  # the parts alone: no draw, no transition, no rate
        body.pop("node_detector"), body.pop("transitions"), body.pop("rates")
    folder = tmp_path / "examples" / "events" / "anticoincidence"
    folder.mkdir(parents=True)
    (folder / "one_photon.json").write_text(json.dumps(world), encoding="utf-8")
    (folder / "two_atoms.json").write_bytes((EVENTS / "anticoincidence" / "two_atoms.json").read_bytes())
    (folder.parent / "engine_start.json").write_bytes((EVENTS / "engine_start.json").read_bytes())
    mode = json.loads((EVENTS / "anticoincidence" / "one_photon.mode.json").read_text(encoding="utf-8"))
    mode["world_digest"] = input_digest(world)
    (folder / "one_photon.mode.json").write_text(json.dumps(mode), encoding="utf-8")
    world_files.REPOSITORY_ROOT = tmp_path
    return Lattice(load_world(folder / "one_photon.json"), (lines := []).append), lines


def test_the_piece_is_booked_at_the_detector_with_its_momentum_and_the_fans(tmp_path, monkeypatch):
    """Tasks 2 and 5: one_photon to the click of 48 at body 0, the piece arriving from the right: the credit line carries `momentum` [p_x, 0, 0] with p_x below 0, the sign of travel, `fan` the photon's P over the board at the click in the same unit, and their difference the erasure's deficit, minus the piece's p where the fan is symmetric (the two packets back to back); |p_x| against T s_k / X at k = pi / 4 printed (the engine's count convention gives 2 / sin omega of the hands' T sin k on a whole packet, tests (b); the packet here half entered and coarse at the amplitude 116); the twin without the draw books nothing: no momentum in the credit's books, no credit line."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board, lines = one_photon_board(tmp_path)
    light = next(i for i, f in enumerate(board.families) if f.name == "photon")
    for _ in range(48):
        board.step()
    credits = [line for line in lines if line["event"] == "credit"]
    assert len(credits) == 1 and credits[0]["interval"] == 48 and credits[0]["absorbed"] == "photon"
    piece, fan = credits[0]["momentum"], credits[0]["fan"]
    assert piece[0] < 0 and piece[1:] == [0, 0] and fan[1:] == [0, 0]
    deficit = [a - b for a, b in zip(fan, piece, strict=True)]
    assert deficit[0] > 0 and abs(deficit[0] + piece[0]) < abs(piece[0])  # the fan near symmetric
    print(
        f"Part F (Tasks 2, 5): the piece's p = {piece}, the fan's P = {fan}, the deficit {deficit}; "
        f"|p_x| = {abs(piece[0])} against T sin(pi / 4) = {T * math.sin(math.pi / 4):.0f}: {abs(piece[0]) / (T * math.sin(math.pi / 4)):.3f} of it"
    )
    twin, twin_lines = one_photon_board(tmp_path, draw=False)
    for _ in range(48):
        twin.step()
    assert twin.credit.momenta == {} and not twin.credit.bodies
    assert not [line for line in twin_lines if line["event"] == "credit"]
    assert board.credit.counts[light] == 0 and twin.credit.counts[light] == 1


def test_the_write_twists_the_taker_to_the_pieces_momentum_or_books_the_loss(tmp_path, monkeypatch):
    """Task 3: (a) on one_photon at the click of 48 the atom (two Nodes along x) is folded: its P_x after the write less before has the piece's sign and the credit line carries the twist n_x; the piece's |p_x| exceeds what the two-Node atom at its lay amplitude (A = 90 per Node, 2 T rho sin delta at most T) can carry, so `lost` is "P lost to the taker" and n_x is the quarter turn, the most the taker takes (printed: the taker's P before and after, n_x, |p_x|); (b') the reachable case, `meeting.twisted` on the second atom's ground part at a p_x within its reach: the part's P_x grows by exactly p_x to the floor (two units per Node of the fold's roundings) with nothing lost; (c) the twist is a rotation: the taker's count is unchanged by the fold and the share's change is printed; (b) a one-Node taker books "P lost to the declaration", nothing folded and its lines unchanged."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board, lines = one_photon_board(tmp_path)
    atom = next(i for i, f in enumerate(board.families) if f.name == "atom")
    for _ in range(47):
        board.step()
    before = meeting.fan_momentum(board, atom)
    board.step()
    after = meeting.fan_momentum(board, atom)
    credits = [line for line in lines if line["event"] == "credit"]
    piece, twist, lost = credits[0]["momentum"], credits[0]["twist"], credits[0]["lost"]
    quarter = meeting.quarter_turn(board)
    assert before == (0, 0, 0) and after[0] < 0 and after[0] * piece[0] > 0
    assert lost == LOST_TO_TAKER and twist == [-quarter, 0, 0] and abs(after[0]) < abs(piece[0])
    print(
        f"Part F (Task 3a): the taker's P_x before {before[0]} and after {after[0]}, n_x = {twist[0]} "
        f"(the quarter turn {quarter}), the piece's p_x = {piece[0]}: {lost}"
    )
    # (b') the reachable case on the second atom, standing in its ground part at 48
    books = board.credit.bodies[1]
    wanted = 10000
    shares_before = board.share_of(atom, 1, board.mask(books.nodes))[0]
    count_before = board.quanta(atom, board.mask(books.nodes))[0]
    standing = meeting.fan_momentum(board, atom)[0]
    found, nothing = meeting.twisted(board, books, books.part, (wanted, 0, 0))
    gained = meeting.fan_momentum(board, atom)[0] - standing
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
    found, lost = meeting.twisted(board, single, single.part, (wanted, 0, 0))
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


def world_beside(tmp_path, source, edit):  # type: ignore[no-untyped-def]
    """A shipped world copied under tmp_path at its repository paths with its universe, the engine's start and its mode file at the edited world's digest, `edit` applied to the document; the repository root moved there."""
    world = json.loads(source.read_text(encoding="utf-8"))
    edit(world)
    folder = tmp_path / source.parent.relative_to(EVENTS.parents[1])
    folder.mkdir(parents=True, exist_ok=True)
    (folder / source.name).write_text(json.dumps(world), encoding="utf-8")
    for key in ("universe", "engine"):
        target = tmp_path / world[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((EVENTS.parents[1] / world[key]).read_bytes())
    mode = json.loads(source.with_suffix(".mode.json").read_text(encoding="utf-8"))
    mode["world_digest"] = input_digest(world)
    (folder / source.with_suffix(".mode.json").name).write_text(json.dumps(mode), encoding="utf-8")
    world_files.REPOSITORY_ROOT = tmp_path
    return folder / source.name


def test_the_pairs_two_pieces_are_back_to_back_over_twenty_seeds(tmp_path, monkeypatch):
    """Task 6: Bell's shipped world a b (two packets of the pair, back to back from the centre, one region per side) over 20 seeds of the draw, the board stepped once to 99 and copied per seed with the generator at the seed for the window's close at 100: the two credited pieces' p_x are opposite in sign and sum to 0 within the lay's rounding (under one percent of |p_x|; the two packets are laid at their own roundings) but not to one unit of T, so every click books "no back-to-back region" (each side being one declared region there is no draw among regions to filter; the reading is booked where it fails, the open corner measured); the realised port combinations over the seeds printed with the pieces' sums (the J statistics of the draw, which the filter leaves to the seed)."""
    world_files.REPOSITORY_ROOT = EVENTS.parents[1]
    board = Lattice(load_world(EVENTS / "bell" / "bell_a_b.json"), [].append)
    for _ in range(99):
        board.step()
    sums, realised, lost, size = [], [], [], 0
    for seed in range(20):
        twin = copy.deepcopy(board)
        twin.output, twin.credit.state = (lines := []).append, seed + 1
        twin.step()
        credits = [line for line in lines if line["event"] == "credit"]
        assert len(credits) == 2 and {c["node_detector"] for c in credits} == {"left", "right"}
        left, right = sorted(credits, key=lambda c: str(c["node_detector"]))
        sums.append([a + b for a, b in zip(left["momentum"], right["momentum"], strict=True)])
        realised.append(f"{left['realised']} {right['realised']}")
        lost += [c["lost"] for c in credits if c["lost"] is not None]
        size = abs(left["momentum"][0])
        assert left["momentum"][0] * right["momentum"][0] < 0  # opposite signs along x
    largest = max(abs(s[0]) for s in sums)
    counted = {key: realised.count(key) for key in sorted(set(realised))}
    print(
        f"Part F (Task 6): Bell a b over 20 seeds, the pieces' p_x sums {sorted({s[0] for s in sums})} "
        f"against |p_x| = {size}, the largest |sum| {largest} ({largest / size:.2e}); the realised ports {counted}; "
        f"{NO_BACK_TO_BACK!r} booked {len(lost)} times of 40 credit lines"
    )
    assert all(s[1:] == [0, 0] for s in sums) and largest * 100 < size
    assert lost == [NO_BACK_TO_BACK] * 40 if largest > 1 else lost == []
