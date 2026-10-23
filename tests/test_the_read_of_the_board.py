"""The click's read of the board (ALGEBRA.md, The click's read of the board; the owner's words: the board is deterministic and the click is the only instrument that reads it, the new draw built from the remainders and Rule3 only): the digits' number and the one division act per draw (`features/click.read_number`, `drawn_from`), the residue's and the quotient's independence, the digits' lattice at the exact vacuum paces and at the shipped content, the loader's refusal of a generator's keys and the read's refusals by name (`digits.read_of`), and the read at work on three shipped worlds re-declared beside tmp_path (`tests.laws.world_beside`): the singlet's two sides (the first side blind to the later side's basis bit for bit, the read writing nothing), the one photon's two bodies (the arriving record's digits and the body's own in the mixed radix of their walls) and the two slits' many-draw close (the digits spent by name at the shipped window, the close run at a shorter one)."""

import math
import random
from collections import Counter

import numpy as np
import pytest

from event_universe import digits, node, node_detector, world_files
from event_universe.core import paces
from event_universe.core.rule3 import rule_integers, wall_of
from event_universe.features.click import bias_bound, drawn_from, read_number
from event_universe.features.front import ball
from event_universe.lattice import Lattice
from event_universe.loader.draw import DIGIT_ORDER
from event_universe.meeting_back import first_difference, snapshot
from event_universe.records import Record
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, family, world_beside
from tests.laws_read import load_shipped

GAMMA, UNIT = 6000, 16  # the shipped universes' Gamma and Link unit G
LIGHT, ATOM = wall_of(6000, GAMMA, UNIT), wall_of(1299, GAMMA, UNIT)  # the walls w = 6 den Gamma^2 G^2


def placed(residue: int, weights: list[int]) -> int:
    """The residue placed on the cumulative weights, the first index whose cumulative weight exceeds it."""
    return next(i for i in range(len(weights)) if residue < sum(weights[: i + 1]))


def body_reads(board: Lattice, families: list[int], at: np.ndarray) -> list[tuple[int, np.ndarray]]:
    """What a body reads by the test's own arithmetic (the reader's G2): each family at the body's Nodes `at` and at the Nodes within one Link of them (the ball of radius 1, `features/front.ball`) where a line of its record holds a remainder other than w // 2."""
    centres = [tuple(int(k) for k in where) for where in np.argwhere(at)]
    near = ball(board.shape, centres, 1, board.world.periodic)
    found = []
    for index in families:
        off = np.zeros(board.shape, dtype=bool)
        for line in board.lines_of(index, 0):
            off |= np.asarray(line.remainder) != board.half_wall(index)
        found.append((index, at | (near & off)))
    return found


def digits_now(
    board: Lattice, reads: list[tuple[int, np.ndarray]], distinct: bool = True
) -> tuple[list[int], list[int]]:
    """The digits and their bases by the test's own arithmetic of the declared order: the families in their order, each at its own Nodes (`reads`, a side's region or a body's `body_reads`), every line of each family's record in the declared order, each line's remainder at the Nodes in the lattice's index order (`np.argwhere`), the digit the remainder's index on the Node's lattice, r // F (`digits.lattice_of` on the rule's integers there), its base w // F + 1; with `distinct` a remainder equal to an earlier line's at the same Node, or w less it, is a copy and left out (the reader's D2), without it every line's digit."""
    found, bases = [], []
    for index, at in reads:
        family, gamma = board.families[index], board.world.node_clock
        wall = wall_of(family.pair[1], gamma, board.unit)
        lattice = digits.lattice_of(
            node.rule_of(family, gamma, *board.read(index, 1, 0), board.unit), at
        )
        earlier: dict[int, list[int]] = {}  # per Node, the earlier lines' remainders
        for line in board.lines_of(index, 0):
            for k, (where, step) in enumerate(zip(np.argwhere(at), lattice, strict=True)):
                remainder, seen = int(line.remainder[tuple(where)]), earlier.setdefault(k, [])
                copied = distinct and any(remainder in (e, wall - e) for e in seen)
                seen.append(remainder)
                if not copied:
                    found.append(remainder // step)
                    bases.append(wall // step + 1)
    return found, bases


def spied(monkeypatch, board_of, distinct=True):  # type: ignore[no-untyped-def]
    """Every draw of the run recorded as the engine makes it (`node_detector.drawn_from` spied): the label, the number read or left, the weights, the pick, the number left after, and the test's own digits of the records the label names at the Nodes it names, read from the board at that moment (each Node's distinct digits, or with `distinct` False every line's)."""
    seen: list[dict] = []  # type: ignore[type-arg]
    real = node_detector.drawn_from

    def spy(number, weights, label, *moduli):  # type: ignore[no-untyped-def]
        board = board_of()
        words = label.split("'")
        if label.startswith("the side "):
            name = words[1]
            reads = [
                (family(board, words[3]), next(d.nodes for d in board.node_detectors if d.name == name))
            ]
        elif label.startswith("the regions "):
            reads = [(family(board, words[1]), node_detector.node_detector_nodes(board))]
        else:
            books = board.credit.bodies[int(label.split()[2])]
            drives = list(dict.fromkeys(t.drive for t in books.declared.transitions))
            reads = body_reads(board, [*drives, books.index], board.mask(books.nodes))
        own, walls = digits_now(board, reads, distinct)
        pick, left = real(number, weights, label, *moduli)
        drawn = dict(label=label, number=number, weights=list(weights), pick=pick, left=left)
        seen.append(dict(drawn, digits=own, walls=walls))
        return pick, left

    monkeypatch.setattr(node_detector, "drawn_from", spy)
    return seen


def test_the_read_is_the_digits_number_and_each_draw_one_division_act():
    """The number is the digits in base w, the first the most significant (`read_number`, multiply and add, equal to the plain sum and to Horner's form with the base reduced); each draw one division act by the weights' total (`drawn_from`): the quotient the number left, the remainder placed on the cumulative weights (the lower index on a tie, a weight of 0 never drawn); the mixed radix of two walls; one weight above 0 is a certain draw and consumes nothing (a weight of 0 never drawn); a total at or below 0 and a number below the total refused by name in the two texts (the number left, a quotient's draw; the number read, the interval's first), the texts apart from the write's bound refusal."""
    chance = random.Random(24)  # the test's own vectors; the engine draws by nothing of the kind
    for _ in range(60):
        count = chance.randint(1, 12)
        found = [chance.randrange(LIGHT) for _ in range(count)]
        x = read_number(found, [LIGHT] * count)
        assert x == sum(d * LIGHT ** (count - 1 - i) for i, d in enumerate(found))
        weights = [chance.randint(0, 10**9) for _ in range(chance.randint(2, 6))]
        weights[0] = max(weights[0], 1)
        total = sum(weights)
        pick, left = drawn_from(x, weights, "the test")
        residue = x % total
        assert (pick, left) == (placed(residue, weights), x // total) and weights[pick] > 0
        horner = 0
        for d in found:
            horner = (horner * (LIGHT % total) + d) % total
        assert horner == residue
    assert read_number([5, 7], [LIGHT, ATOM]) == 5 * ATOM + 7  # the mixed radix: each digit its own base
    assert drawn_from(12345, [9], "the test") == (0, 12345)  # one weight consumes nothing
    assert drawn_from(12345, [0, 3, 0], "the test") == (1, 12345)  # one weight above 0: certain, whole
    assert drawn_from(12345, [0, 3, 4], "the test") == (placed(12345 % 7, [0, 3, 4]), 12345 // 7)
    with pytest.raises(ValueError, match="weights whose total is above 0"):
        drawn_from(12345, [0, 0], "the test")
    with pytest.raises(
        RuntimeError, match="at the test has the number 5 left, below the draw's total 7"
    ):
        drawn_from(5, [3, 4], "the test")
    spent = str(pytest.raises(RuntimeError, drawn_from, 5, [3, 4], "the test").value)
    assert spent.startswith("the click's read of the board") and "amplitude bound" not in spent
    with pytest.raises(RuntimeError, match="has the number 5 read, below the draw's total 7"):
        drawn_from(5, [3, 4], "the test", (1, 2))  # the interval's read itself below the total


def test_the_residue_and_the_quotient_of_one_number_are_independent():
    """Two draws of one close are one division act each on the number left: over a full period of T1 T2 the pairs (the first pick's residue, the second's) are each hit alike (60 pairs of 60 at T1 = 6 and T2 = 10, 7 times each over 7 periods), where the same residue read twice would lock the picks (30 pairs of 60 at gcd 2: the refused form, the test's own arithmetic)."""
    first, second = [2, 4], [7, 3]  # T1 = 6, T2 = 10
    counts: Counter[tuple[int, int]] = Counter()
    base = 7 * 60  # above both totals at every draw: the number left stays above T2
    for x in range(base, base + 7 * 60):
        pick, left = drawn_from(x, first, "the test")
        again, _rest = drawn_from(left, second, "the test")
        counts[(x % 6, left % 10)] += 1
        assert (pick, again) == (placed(x % 6, first), placed(left % 10, second))
    assert len(counts) == 60 and set(counts.values()) == {7}
    assert len({(x % 6, x % 10) for x in range(60)}) == 30  # the same residue twice: locked pairs


def test_a_total_sharing_a_factor_with_the_bases_books_its_bias_bound_and_is_refused_only_as_the_whole_total():
    """The reader's F of 2026-10-20 (`bias_bound`, `drawn_from` with the read's moduli, `digits.read_of`; CHANGED the same day from D's refusal where the product of the two gcds reached the smallest weight, a model's worst case taken for a measure): at the shipped content the base is B = w div F + 1 = 108,000,001 = 31 x 1069 x 3259 and B - 1 = 108,000,000 = 2^8 3^3 5^6, so the residue modulo a factor of B - 1 is the distinct digits' sum and modulo a factor of B the last digit alone, and g / T, g the product of the two gcds, bounds a port's move where the digits cycle: the bound is booked, [g_sum, g_last, T], and the one draw refused is g = T with two weights above 0, the digits' sum modulo the total alone (the conversion's total 30 at the weight 1, and the base's prime 31 at the weight 1), named so; the screens' class (the total 66,120,000 at the smallest weight 24,000, g = 120,000), a small factor (194 = 2 x 97), a total coprime to both (97) are drawn as before, the residue placed on the weights, and a certain draw (one weight above 0, g = T = 5) consumes nothing; the quotient's draws carry no moduli."""
    moduli, number = (108_000_000, 108_000_001), 10**30 + 12345
    assert bias_bound(66_120_000, moduli) == [
        120_000,
        1,
        66_120_000,
    ]  # the two slits' bound 0.18 percent
    assert bias_bound(30, moduli) == [30, 1, 30] and bias_bound(31, moduli) == [1, 31, 31]
    for weights in ([1, 29], [1, 30]):
        with pytest.raises(RuntimeError, match="the draw is the digits' sum modulo the total alone"):
            drawn_from(number, weights, "the test", moduli)
        total = sum(weights)
        assert drawn_from(number, weights, "the test") == (
            placed(number % total, weights),
            number // total,
        )
    for weights in ([24_000, 66_096_000], [97, 97], [48, 49]):
        total = sum(weights)
        found = drawn_from(number, weights, "the test", moduli)
        assert found == (placed(number % total, weights), number // total)
    for weights in ([5, 0], [1, 0]):  # a certain draw: nothing read, nothing consumed, g = T no refusal
        assert drawn_from(number, weights, "the test", moduli) == (0, number)


def test_the_digits_lattice_at_the_exact_vacuum_is_three_valued():
    """The digits' lattice F = gcd(w, D_i, R_ij) (`digits.lattice_of`): at the exact vacuum paces, p_0 = p_i = Gamma with no tension, light's digits lie on w div 2 + (w div 3) Z, three values each (the read refused there), the massive pair [4000, 6000] on nine; at the shipped universes' content 60 (the paces 5940 and 5881) F = 3,072,000 = 2 num G^2 and a digit takes 108,000,000 values; the atom [1, 1299] at the exact vacuum 3,897."""
    at = np.ones((2, 1, 1), dtype=bool)
    light = rule_integers(6000, 6000, GAMMA, GAMMA, GAMMA, None, UNIT)
    found = digits.lattice_of(light, at)
    assert found == [LIGHT // 3] * 2 and all(3 * f >= LIGHT for f in found)
    matter = rule_integers(4000, 6000, GAMMA, GAMMA, GAMMA, None, UNIT)
    assert digits.lattice_of(matter, at) == [LIGHT // 9] * 2
    atom = rule_integers(1, 1299, GAMMA, GAMMA, GAMMA, None, UNIT)
    assert [ATOM // f for f in digits.lattice_of(atom, at)] == [3897] * 2
    clock, pace = paces.node_paces(GAMMA, 60)
    assert (clock, pace) == (5940, 5881)
    content = rule_integers(6000, 6000, GAMMA, clock, pace, None, UNIT)
    lattice = digits.lattice_of(content, at)
    assert lattice == [3_072_000] * 2 and LIGHT // lattice[0] == 108_000_000
    assert lattice[0] == 2 * 6000 * UNIT * UNIT and all(3 * f < LIGHT for f in lattice)
    assert (
        "most significant" in DIGIT_ORDER and "index order" in DIGIT_ORDER and "r div F" in DIGIT_ORDER
    )


def test_a_turned_records_digits_lie_on_the_lattice_of_the_links_pairs(monkeypatch):
    """The digits' lattice of a turned plane (`digits.lattice_of` with the pairs the step reads, `flux.pairs_of`; the reader's ruling of 2026-10-21 on issue #2169, finding 2): on the shipped hydrogen_1s the electron reads its holder's phase pairs at the exact vacuum paces (its content 0, T = p_0^2 = Gamma^2 = 36,000,000), so F = gcd(w, D_i, R_ij, R^c_ij, R^s_ij) is T at the 33 Nodes about the centre over four intervals but at two Node-intervals 2 T (every pair part even there; four digits of 264, the record's two lines at 33 Nodes; one Node-interval and two digits before 2026-10-21, when the pair at -n was defined as the conjugate of the pair at +n and the pairs read through a -a Port moved by one Link unit at some angles), and every kept remainder lies on w div 2 + F Z and off the plain lattice w div 2 + (w div 9) Z after the first step (the builder's finding on 400 intervals: 36,000,000 the gcd of r - w div 2 over 26,466 remainders, 66 on the plain lattice, frame 0's origins); the plain reaches alone read w div 9, nine values, kept by name."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", ROOT)
    board = Lattice(load_shipped(EVENTS / "atom" / "hydrogen_1s.json"))
    electron, gamma = family(board, "electron"), board.world.node_clock
    quantum, half = board.world.quantum_action, board.half_wall(electron)
    assert quantum == gamma * gamma and electron in board.turning  # T = p_0^2 at the vacuum paces
    at = ((np.indices(board.shape) - board.shape[0] // 2) ** 2).sum(axis=0) <= 4  # r^2 <= 4: 33 Nodes
    found: Counter[int] = Counter()
    for _ in range(4):
        board.step()
        read = list(digits.digits_of(board, electron, at))
        assert all((r - half) % f == 0 for r, f, _w, _p in read)  # on w div 2 + F Z, every one
        assert all((r - half) % (2 * half // 9) for r, _f, _w, _p in read)  # off w div 2 + (w div 9) Z
        assert {w for _r, _f, w, _p in read} == {2 * half}
        found.update(f for _r, f, _w, _p in read)
    assert found == Counter({quantum: 260, 2 * quantum: 4}) and sum(found.values()) == 4 * 2 * 33
    rule = node.rule_of(board.families[electron], gamma, *board.read(electron, 1, 0), board.unit)
    assert digits.lattice_of(rule, at) == [2 * half // 9] * 33  # the plain reaches alone: nine values


def test_the_read_refuses_by_name_the_untouched_region_and_the_exact_vacuum(tmp_path, monkeypatch):
    """The read's two refusals (`digits.read_of`): on the singlet world at its start the left region stands untouched, every digit at the lay's origin w div 2, so a read there is refused by name; on the shipped resonance world at the content 0 (examples/events/resonance/resonant.json, two atoms of two Nodes on the periodic chain of 48, the emitter's pulse laid as a source in time from its window's close, 48; re-read 2026-10-20 there by the reader's ruling, the content fixture's pulse reading the content), once the pulse reaches the taker, the pulse's digits at the taker's Nodes lie on the lattice of the exact vacuum paces (its family reads no content: three values each, in {w / 6, w / 2, 5 w / 6}), so the pulse's record alone is refused by name, and the body's read, the arriving record's digits with its own record's (3,897 values each, the lines read once where one is a copy of another or stands at the lay's origin: four of the atom's digits and two of the pulse's at the two Nodes, 51 bits, re-pinned 2026-10-20 on the shipped ring), is admitted; the refusals' texts stand apart from the write's bound refusal."""
    path = world_beside(
        tmp_path / "singlet", EVENTS / "bell_singlet" / "singlet_a_b.json", lambda w: None
    )
    singlet = Lattice(load_world(path))
    spin = family(singlet, "spin")
    left = next(d.nodes for d in singlet.node_detectors if d.name == "left")
    assert {r for r, _f, _w, _p in digits.digits_of(singlet, spin, left)} == {singlet.half_wall(spin)}
    with pytest.raises(RuntimeError, match="at the test finds every digit at the lay's origin w div 2"):
        digits.read_of(singlet, [(spin, left)], "the test")
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", EVENTS.parents[1])
    board = Lattice(load_shipped(EVENTS / "resonance" / "resonant.json"))  # the shipped ring, content 0
    pulse, atom = family(board, "pulse"), family(board, "atom")
    taker = board.credit.bodies[1]
    at = board.mask(taker.nodes)
    while {r for r, _f, _w, _p in digits.digits_of(board, pulse, at)} == {board.half_wall(pulse)}:
        board.step()
    thirds = {LIGHT // 6, LIGHT // 2, 5 * LIGHT // 6}
    assert {r for r, _f, _w, _p in digits.digits_of(board, pulse, at)} <= thirds
    with pytest.raises(RuntimeError, match="finds every digit on the lattice of the exact vacuum paces"):
        digits.read_of(board, [(pulse, at)], "the test")
    before = snapshot(board)
    number, _moduli = digits.read_of(board, [(pulse, at), (atom, at)], "the test")
    assert first_difference(before, snapshot(board)) is None  # the read writes nothing
    own, walls = digits_now(board, [(pulse, at), (atom, at)])
    assert number == read_number(own, walls) and set(walls) == {4, 3898}  # light's 3 values, the atom's
    # three Nodes since 2026-10-21 (the pair re-declared as the chain's; two Nodes, (2, 4, 51), 2026-10-20)
    assert (walls.count(4), walls.count(3898), number.bit_length()) == (3, 6, 77)
    for text in ("w div 2", "exact vacuum"):
        assert "amplitude bound" not in text


def test_the_singlets_sides_read_the_board_and_the_first_side_is_blind_to_the_later_basis(
    tmp_path, monkeypatch
):
    """The shipped singlet (a, b) and (a, b') re-declared beside tmp_path, no generator: at the close each side draws its port by one division act on the number read from the record's distinct digits at its own region (two parts of a plane, two lines each, four Nodes: the left's eight, the second part's lines copies of the first's, laid alike; the right's eight after the left's write zeroed a part, its lines at the lay's origin read once; the reader's D2) (the test's own digits in the declared order equal the engine's number), its credited Node on the number left (one Node, nothing consumed) and its source on none (one emitter, no draw); the two credit lines, left then right, the orders 1 and 2, the count 1, nothing left; the left side's number, weights and pick equal bit for bit in (a, b) and (a, b'), no signalling toward the first side; the books hold the number left within the close alone and nothing across."""
    runs = {}
    for name in ("singlet_a_b", "singlet_a_b_prime"):
        holder: list[Lattice] = []
        seen = spied(monkeypatch, lambda holder=holder: holder[0])
        path = world_beside(tmp_path / name, EVENTS / "bell_singlet" / f"{name}.json", lambda w: None)
        board = Lattice(load_world(path), (lines := []).append)
        holder.append(board)
        for _ in range(board.world.intervals):
            board.step()
        clicks = [c for c in lines if c["event"] == "credit"]
        assert [(c["node_detector"], c["order"], c["count"], c["left"]) for c in clicks] == [
            ("left", 1, 1, 0),
            ("right", 2, 1, 0),
        ]
        assert [s["label"] for s in seen] == [
            f"the side {side!r} of 'spin' at the interval 40"
            for side in ("left", "left", "right", "right")
        ]
        for (port, place), distinct in zip((seen[0:2], seen[2:4]), (8, 8), strict=True):
            assert (
                port["number"] == read_number(port["digits"], port["walls"])
                and len(port["digits"]) == distinct
            )
            total = sum(port["weights"])
            assert (port["pick"], port["left"]) == (
                placed(port["number"] % total, port["weights"]),
                port["number"] // total,
            )
            assert (
                place["number"] == port["left"]
                and len(place["weights"]) == 1
                and place["left"] == place["number"]
            )
        assert [s["pick"] for s in seen[::2]] == [{"plus": 0, "minus": 1}[c["realised"]] for c in clicks]
        assert board.credit.left == {} and all(b.left is None for b in board.credit.bodies)
        runs[name] = seen
    first, other = (runs[n][0] for n in ("singlet_a_b", "singlet_a_b_prime"))
    keys = ("number", "weights", "pick", "digits")
    assert [first[k] for k in keys] == [other[k] for k in keys]
    print(
        f"the singlet's left read: {first['number'].bit_length()} bits, the weights {first['weights']}, the pick {first['pick']}; the right's {runs['singlet_a_b'][2]['weights']} and {runs['singlet_a_b_prime'][2]['weights']}"
    )


def test_the_chains_bodies_read_the_board_at_their_nodes_and_within_one_link(monkeypatch):
    """The shipped chain world chain_x_minus (ALGEBRA.md, What a body reads, the reader's G2 of 2026-10-20): a body's first draw of an interval reads the arriving record's digits first and its own after, at its three Nodes and at the Nodes within one Link where the photon stands off the origin (the test's own digits in the declared order equal the engine's number), the absorption's outcome one division act on it and the hole's Node one more on the number left; the two atoms take and give back along the run (the absorptions at 74, 142 and 307, each body's own read, the emissions at the windows' closes in the exact dark without a draw; the third pair pinned 2026-10-20 under the twist's deletion, (307, 355) with the piece 45,762 and the recoil at 142 reading 44,243, where the fold's quarter turn on body 1's e part had entered the born light's phase at 190 and moved body 0's read to 303: the recoil's imprint on the emitted light's phase is not written on the board, the recoil booked on the credit line alone), the world LAWFUL over its 400 intervals; the draws' count and the reads' Nodes printed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", ROOT)
    holder: list[Lattice] = []
    seen = spied(monkeypatch, lambda: holder[0])
    board = Lattice(load_shipped(EVENTS / "chain" / "chain_x_minus.json"), (lines := []).append)
    holder.append(board)
    for _ in range(board.world.intervals):
        board.step()
    taken = [c for c in lines if c["event"] == "credit" and c["absorbed"]]
    assert [(c["interval"], c["node_detector"]) for c in taken] == [
        (74, "body 0"),
        (142, "body 1"),
        (307, "body 0"),
    ]
    assert seen and all(record["label"].startswith("the body ") for record in seen)
    for k, record in enumerate(seen):
        earlier = seen[k - 1] if k else None
        if earlier is not None and earlier["label"] == record["label"]:
            assert record["number"] == earlier["left"]  # the same interval: the number left carried
        else:
            assert record["number"] == read_number(record["digits"], record["walls"])  # the first read
            assert set(record["walls"]) <= {4, 3898} and record["walls"].count(3898) >= 6
        total = sum(record["weights"])
        assert (record["pick"], record["left"]) == (
            placed(record["number"] % total, record["weights"]),
            record["number"] // total,
        )
    print(
        f"the chain: {len(seen)} body draws, the first {len(seen[0]['digits'])} digits of {seen[0]['walls'][:1]}..."
    )


def test_the_two_slits_many_draw_close_spends_the_digits_at_the_window_130(tmp_path, monkeypatch):
    """The two slits re-declared beside tmp_path with the draw's window 130, one close over the run (the test's own declaration; the shipped world draws at the window 1 since the landing's pass of 2026-10-20): the record of one part reads its digits at the union of the regions' Nodes once per close, the bases 108,000,001 at the content 60, and every quantum of the close takes two division acts, its region and its Node, each on the number left; at one close of 660 quanta the digits are spent and the read is refused by name with the second text, the number left below the total, where the regions' Nodes read fewer digits than the close's draws take (64 digits of 26.7 bits against 47 draws of 33 to 34 bits on the one-column screens; screens two columns deep read 128 and the close may complete), either way every draw before it the one division act; the write's bound refusal apart."""
    holder: list[Lattice] = []
    seen = spied(monkeypatch, lambda: holder[0])
    source = EVENTS / "two_slits" / "two_slits.json"
    path = world_beside(tmp_path, source, lambda world: world["draw"].update(window=130))
    board = Lattice(load_world(path), [].append)
    holder.append(board)
    refusal = None
    try:
        for _ in range(board.world.intervals):
            board.step()
    except RuntimeError as found:
        refusal = str(found)
    first = seen[0]
    digits_read = len(first["digits"])
    assert first["label"] == "the regions of 'charge' at the interval 130" and digits_read % 8 == 0
    assert first["number"] == read_number(first["digits"], first["walls"]) and set(first["walls"]) == {
        108_000_001
    }
    for earlier, later in zip(seen, seen[1:], strict=False):
        assert later["number"] == earlier["left"]  # one division act per draw on the number left
    bits = [math.log2(sum(s["weights"])) for s in seen]
    if refusal is not None:
        assert (
            "at the interval 130 has the number " in refusal
            and " left, below the draw's total" in refusal
        )
        assert "digits read are spent at this interval" in refusal and "amplitude bound" not in refusal
        assert digits_read * 26.7 < sum(bits) + max(bits)  # spent: the digits below the draws' bits
    else:
        assert digits_read * 26 > sum(bits)  # the deeper screens' digits carry the close's draws
    print(
        f"the two slits at the window 130: {digits_read} digits, {len(seen)} draws ({len(seen) // 2} quanta), the totals {min(bits):.1f} to {max(bits):.1f} bits each, "
        + (f"refused: {refusal[:80]}" if refusal else "the close complete")
    )


def test_a_sides_two_lines_read_one_index_per_node_equal_before_the_write_and_complementary_after(
    monkeypatch,
):
    """The digits' pair identity (the builder's measurement on the read's second commit, bell a' b: in 474 reads of 237 worlds the two lines' indices equal at every Node in 357 and complementary in 117, none else) and the read's copy rule on it (the reader's D2 and D5 of 2026-10-20): on the shipped bell worlds a' b, a' b' and a b each side reads the record's two lines at its four Nodes at the close 100, w div F = 108,000,000 at F = 3,072,000 on light's wall 331,776,000,000,000, the moduli of its first draw the base less one and the base. At every Node the second line's index r div F equals the first line's before any write (the left side, the parts laid alike), so the read takes each Node's distinct digits once: the side's eight digits read as four, the number's bits halved (four digits of 26.7 bits); after the left side's write the right side reads equal indices where the coefficients are equal (the basis [1, 1] at its port (1, 1), which writes nothing), w div F less them where the second part is negated, and, where the port zeroes a part (a b, the basis [1, 0]), that part's line at the lay's origin, w div 2F at every Node, no copy, its eight digits kept. The rule's three cases on a' b's left side at 60, its second line set beside the first: equal and w less it read once (four digits), moved by F at two of the four Nodes read at both (six). The indices, the coefficients standing at the right side's read and the numbers printed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", ROOT)
    whole, found = LIGHT // 3_072_000, {}  # w div F at the shipped content
    for name in ("bell_a_prime_b", "bell_a_prime_b_prime", "bell_a_b"):
        board, standing, read = Lattice(load_shipped(EVENTS / "bell" / f"{name}.json")), [], []
        seen, spy = (
            spied(monkeypatch, lambda board=board: board, distinct=False),
            node_detector.drawn_from,
        )

        def noted(number, weights, label, *moduli, board=board, standing=standing, spy=spy):  # type: ignore[no-untyped-def]
            standing.append(list(board.credit.written.get(family(board, "light_pair"), [(1, 0)] * 2)))
            return spy(number, weights, label, *moduli)

        def reading(board, reads, label, read=read):  # type: ignore[no-untyped-def]
            read.append(digits.read_of(board, reads, label))
            return read[-1]

        monkeypatch.setattr(node_detector, "drawn_from", noted)
        monkeypatch.setattr(node_detector, "read_of", reading)
        for _ in range(board.world.intervals):
            board.step()
        sides = [
            (s["label"].split("'")[1], s["digits"], s["walls"])
            for s in seen
            if "the side " in s["label"]
        ]
        assert [side for side, _d, _b in sides] == [
            "left",
            "left",
            "right",
            "right",
        ]  # the port, the Node
        assert all(len(d) == 8 and set(b) == {whole + 1} for _s, d, b in sides) and whole == 108_000_000
        assert [moduli for _n, moduli in read] == [(whole, whole + 1)] * 2  # one read per side
        found[name] = sides[0][1], sides[2][1], standing[2], [number for number, _m in read]
    for left, right, written, (first, second) in found.values():
        assert left[4:] == left[:4] and first == read_number(left[:4], [whole + 1] * 4)  # read once
        assert first.bit_length() <= 4 * 27  # four digits of 26.7 bits: the eight's bits halved
        if written[0] == written[1]:
            assert right[4:] == right[:4]  # equal coefficients: equal indices
        elif written[0] == (-written[1][0], -written[1][1]):
            assert right[4:] == [whole - k for k in right[:4]]  # the sign write: w div F less it
        else:
            zeroed = written.index((0, 0))  # the part the left side's port zeroed reads the lay's origin
            assert right[4 * zeroed : 4 * zeroed + 4] == [whole // 2] * 4
        copies = right[4:] in (right[:4], [whole - k for k in right[:4]])
        assert second == read_number(right[:4] if copies else right, [whole + 1] * (4 if copies else 8))
    assert found["bell_a_b"][2].count((0, 0)) == 1  # the basis [1, 0] zeroes a part
    board = Lattice(load_shipped(EVENTS / "bell" / "bell_a_prime_b.json"))  # the copy rule's three cases
    pair = family(board, "light_pair")
    for _ in range(60):  # the left side's beam through its region, before the close
        board.step()
    at, (first, second) = (
        next(d.nodes for d in board.node_detectors if d.name == "left"),
        board.states[pair].lines[:2],
    )
    kept = np.asarray(first.remainder)
    cases = {
        "equal": kept,
        "w less it": LIGHT - kept,
        "moved": kept + 3_072_000 * (np.arange(kept.size).reshape(kept.shape) % 2),  # F at every other
    }
    for case, remainder in cases.items():  # the second line set beside the first: read once, or both
        board.states[pair].lines[1] = Record(second.now, second.before, remainder.reshape(kept.shape))
        own, walls = digits_now(board, [(pair, at)], distinct=False)
        number, _moduli = digits.read_of(board, [(pair, at)], "the test")
        distinct = own[:4] + [k for j, k in enumerate(own[4:]) if k not in (own[j], whole - own[j])]
        assert number == read_number(distinct, walls[: len(distinct)]), case
        assert len(distinct) == (4 if case != "moved" else 6), case  # two of the four Nodes moved
    print(f"the pair identity: {found}")
