"""The click's read of the board (ALGEBRA.md, The click's read of the board; the owner's words: the board is deterministic and the click is the only instrument that reads it, the new draw built from the remainders and Rule3 only): the digits' number and the one division act per draw (`features/click.read_number`, `drawn_from`), the residue's and the quotient's independence, the digits' lattice at the exact vacuum paces and at the shipped content, the loader's refusal of a generator's keys and the read's refusals by name (`digits.read_of`), and the read at work on three shipped worlds re-declared beside tmp_path (`tests.laws.world_beside`): the singlet's two sides (the first side blind to the later side's basis bit for bit, the read writing nothing), the one photon's two bodies (the arriving record's digits and the body's own in the mixed radix of their walls) and the two slits' many-draw close (the digits spent by name at the shipped window, the close run at a shorter one)."""

import math
import random
from collections import Counter
from dataclasses import fields

import numpy as np
import pytest

from event_universe import digits, node, node_detector, world_files
from event_universe.core import paces
from event_universe.core.rule3 import rule_integers, wall_of
from event_universe.credit import Books
from event_universe.features.click import drawn_from, read_number
from event_universe.lattice import Lattice
from event_universe.loader.draw import DIGIT_ORDER, Draw, body_draw_of, draw_of, windowless_of
from event_universe.meeting_back import first_difference, snapshot
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, family, refused, world_beside
from tests.laws_read import load_shipped

GAMMA, UNIT = 6000, 16  # the shipped universes' Gamma and Link unit G
LIGHT, ATOM = wall_of(6000, GAMMA, UNIT), wall_of(1299, GAMMA, UNIT)  # the walls w = 6 den Gamma^2 G^2


def placed(residue: int, weights: list[int]) -> int:
    """The residue placed on the cumulative weights, the first index whose cumulative weight exceeds it."""
    return next(i for i in range(len(weights)) if residue < sum(weights[: i + 1]))


def digits_now(board: Lattice, families: list[int], at: np.ndarray) -> tuple[list[int], list[int]]:
    """The digits and their bases by the test's own arithmetic of the declared order: the families in their order, every line of each family's record in the declared order, each line's remainder at the Nodes of `at` in the lattice's index order (`np.argwhere`), the digit the remainder's index on the Node's lattice, r // F (`digits.lattice_of` on the rule's integers there), its base w // F + 1."""
    found, bases = [], []
    for index in families:
        family, gamma = board.families[index], board.world.node_clock
        wall = wall_of(family.pair[1], gamma, board.unit)
        lattice = digits.lattice_of(
            node.rule_of(family, gamma, *board.read(index, 1, 0), board.unit), at
        )
        for line in board.lines_of(index, 0):
            for where, step in zip(np.argwhere(at), lattice, strict=True):
                found.append(int(line.remainder[tuple(where)]) // step)
                bases.append(wall // step + 1)
    return found, bases


def spied(monkeypatch, board_of):  # type: ignore[no-untyped-def]
    """Every draw of the run recorded as the engine makes it (`node_detector.drawn_from` spied): the label, the number read or left, the weights, the pick, the number left after, and the test's own digits of the records the label names at the Nodes it names, read from the board at that moment."""
    seen: list[dict] = []  # type: ignore[type-arg]
    real = node_detector.drawn_from

    def spy(number, weights, label):  # type: ignore[no-untyped-def]
        board = board_of()
        words = label.split("'")
        if label.startswith("the side "):
            name, read = words[1], [family(board, words[3])]
            at = next(d.nodes for d in board.node_detectors if d.name == name)
        elif label.startswith("the regions "):
            read = [family(board, words[1])]
            at = node_detector.node_detector_nodes(board)
        else:
            books = board.credit.bodies[int(label.split()[2])]
            drives = list(dict.fromkeys(t.drive for t in books.declared.transitions))
            read, at = [*drives, books.index], board.mask(books.nodes)
        own, walls = digits_now(board, read, at)
        pick, left = real(number, weights, label)
        seen.append(
            dict(
                label=label,
                number=number,
                weights=list(weights),
                pick=pick,
                left=left,
                digits=own,
                walls=walls,
            )
        )
        return pick, left

    monkeypatch.setattr(node_detector, "drawn_from", spy)
    return seen


def test_the_read_is_the_digits_number_and_each_draw_one_division_act():
    """The number is the digits in base w, the first the most significant (`read_number`, multiply and add, equal to the plain sum and to Horner's form with the base reduced); each draw one division act by the weights' total (`drawn_from`): the quotient the number left, the remainder placed on the cumulative weights (the lower index on a tie, a weight of 0 never drawn); the mixed radix of two walls; one weight consumes nothing; a total at or below 0 and a number below the total refused by name, the text apart from the write's bound refusal."""
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
    assert drawn_from(12345, [0, 3, 0], "the test") == (1, 4115)  # a weight of 0 never drawn
    with pytest.raises(ValueError, match="weights whose total is above 0"):
        drawn_from(12345, [0, 0], "the test")
    with pytest.raises(
        RuntimeError, match="at the test has the number 5 left, below the draw's total 7"
    ):
        drawn_from(5, [3, 4], "the test")
    spent = str(pytest.raises(RuntimeError, drawn_from, 5, [3, 4], "the test").value)
    assert spent.startswith("the click's read of the board") and "amplitude bound" not in spent


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


def test_the_loader_refuses_a_generator_and_admits_the_detector_with_no_key(tmp_path):
    """No generator: `seed`, `multiplier` and `increment` are unknown keys of the world's `draw` and of a body's `node_detector`, refused by name as every unknown key is; a body's `node_detector` is `{}` (its window derived or a probe's) or `{"window": n}` (`body_draw_of`, `windowless_of`, `Draw`); a window beside a probe refused; the world's `engine` key refused as unknown, the start file gone; the books keep no state and the number left of the read alone (`credit.Books.left`)."""
    label = "bodies[0].node_detector"
    generator = {"seed": 24, "multiplier": 6364136223846793005, "increment": 1442695040888963407}
    refused("holds the unknown key 'increment'", draw_of, {"window": 40, **generator}, "draw", True)
    refused("holds the unknown key 'seed'", body_draw_of, {"seed": 25}, label)
    refused("holds the unknown key 'multiplier'", windowless_of, {"multiplier": 5}, label)
    refused("declares a window beside a probe", windowless_of, {"window": 3}, label)
    assert body_draw_of({}, label) == windowless_of({}, label) == Draw(None)
    assert body_draw_of({"window": 48}, label) == Draw(48) and draw_of(
        {"window": 40}, "draw", True
    ) == Draw(40)
    assert draw_of({"window": 40, "reach": "board"}, "draw", True) == Draw(40, "board")
    assert not hasattr(Draw(None), "seed")
    source = EVENTS / "bell_singlet" / "singlet_a_b.json"

    def engine(world):  # type: ignore[no-untyped-def]
        world["engine"] = "examples/events/engine_start.json"

    refused(
        "the world holds the unknown key 'engine'", load_world, world_beside(tmp_path, source, engine)
    )
    names = {f.name for f in fields(Books)}
    assert "left" in names and not names & {"state", "states"}


def test_the_read_refuses_by_name_the_untouched_region_and_the_exact_vacuum(tmp_path):
    """The read's two refusals (`digits.read_of`): on the singlet world at its start the left region stands untouched, every digit at the lay's origin w div 2, so a read there is refused by name; on the one photon's world, once the photon reaches the first atom, the photon's digits at the body's Nodes lie on the lattice of the exact vacuum paces (its family reads no content: three values each, in {w / 6, w / 2, 5 w / 6}), so the photon's record alone is refused by name, and the body's read, the arriving record's digits with its own record's (3,897 values each), is admitted; the refusals' texts stand apart from the write's bound refusal."""
    singlet = Lattice(
        load_world(
            world_beside(
                tmp_path / "singlet", EVENTS / "bell_singlet" / "singlet_a_b.json", lambda w: None
            )
        )
    )
    spin, left = (
        family(singlet, "spin"),
        next(d.nodes for d in singlet.node_detectors if d.name == "left"),
    )
    assert {r for r, _f, _w in digits.digits_of(singlet, spin, left)} == {singlet.half_wall(spin)}
    with pytest.raises(RuntimeError, match="at the test finds every digit at the lay's origin w div 2"):
        digits.read_of(singlet, [spin], left, "the test")
    board = Lattice(
        load_world(
            world_beside(
                tmp_path / "photon", EVENTS / "anticoincidence" / "one_photon.json", lambda w: None
            )
        )
    )
    photon, atom = family(board, "photon"), family(board, "atom")
    body = board.credit.bodies[0]
    at = board.mask(body.nodes)
    while {r for r, _f, _w in digits.digits_of(board, photon, at)} == {board.half_wall(photon)}:
        board.step()
    assert {r for r, _f, _w in digits.digits_of(board, photon, at)} <= {
        LIGHT // 6,
        LIGHT // 2,
        5 * LIGHT // 6,
    }
    with pytest.raises(RuntimeError, match="finds every digit on the lattice of the exact vacuum paces"):
        digits.read_of(board, [photon], at, "the test")
    before = snapshot(board)
    number = digits.read_of(board, [photon, atom], at, "the test")
    assert first_difference(before, snapshot(board)) is None  # the read writes nothing
    own, walls = digits_now(board, [photon, atom], at)
    assert (
        number == read_number(own, walls)
        and walls == [4] * 2 + [3898] * 8  # the bases w div F + 1: light's 3 values, the atom's 3,897
        and 90 < number.bit_length() <= 100  # 2 digits of 2 bits and 8 of 11.9: the vacuum's few bits
    )
    for text in ("w div 2", "exact vacuum"):
        assert "amplitude bound" not in text


def test_the_singlets_sides_read_the_board_and_the_first_side_is_blind_to_the_later_basis(
    tmp_path, monkeypatch
):
    """The shipped singlet (a, b) and (a, b') re-declared beside tmp_path, no generator: at the close each side draws its port by one division act on the number read from the record's sixteen digits at its own region (two parts of a plane, two lines each, four Nodes) (the test's own digits in the declared order equal the engine's number), its credited Node on the number left (one Node, nothing consumed) and its source on none (one emitter, no draw); the two credit lines, left then right, the orders 1 and 2, the count 1, nothing left; the left side's number, weights and pick equal bit for bit in (a, b) and (a, b'), no signalling toward the first side; the books hold the number left within the close alone and nothing across."""
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
        for port, place in (seen[0:2], seen[2:4]):
            assert (
                port["number"] == read_number(port["digits"], port["walls"])
                and len(port["digits"]) == 16
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
    assert (first["number"], first["weights"], first["pick"], first["digits"]) == (
        other["number"],
        other["weights"],
        other["pick"],
        other["digits"],
    )
    print(
        f"the singlet's left read: {first['number'].bit_length()} bits, the weights {first['weights']}, the pick {first['pick']}; the right's {runs['singlet_a_b'][2]['weights']} and {runs['singlet_a_b_prime'][2]['weights']}"
    )


def test_the_one_photons_bodies_read_the_board_at_their_nodes(tmp_path, monkeypatch):
    """The anticoincidence world's one photon re-declared beside tmp_path, no generator: a body's first draw of an interval reads the arriving record's digits first and its own after at its two Nodes, in the mixed radix of the two walls (the test's own digits equal the engine's number), the absorption's outcome one division act on it and the hole's Node one more on the number left; one photon, at most one atom takes it and the other stands in its ground part."""
    holder: list[Lattice] = []
    seen = spied(monkeypatch, lambda: holder[0])
    path = world_beside(tmp_path, EVENTS / "anticoincidence" / "one_photon.json", lambda w: None)
    board = Lattice(load_world(path), (lines := []).append)
    holder.append(board)
    for _ in range(board.world.intervals):
        board.step()
    taken = [c for c in lines if c["event"] == "credit" and c["absorbed"]]
    assert len(taken) <= 1 and seen, (taken, len(seen))
    for k, record in enumerate(seen):
        assert record["walls"] == [4] * 2 + [3898] * 8 and record["label"].startswith("the body ")
        earlier = seen[k - 1] if k else None
        if earlier is not None and earlier["label"] == record["label"]:
            assert record["number"] == earlier["left"]  # the same interval: the number left carried
        else:
            assert record["number"] == read_number(record["digits"], record["walls"])
        total = sum(record["weights"])
        assert (record["pick"], record["left"]) == (
            placed(record["number"] % total, record["weights"]),
            record["number"] // total,
        )
    parts = [b.declared.names[b.part] for b in board.credit.bodies]
    assert parts.count("e") == len(taken) and board.credit.counts[family(board, "photon")] == 1 - len(
        taken
    )
    print(
        f"the one photon: {len(seen)} draws, the outcome {[(c['node_detector'], c['interval']) for c in taken]}, the parts {parts}"
    )


def test_the_two_slits_many_draw_close_spends_the_digits_at_the_shipped_window(tmp_path, monkeypatch):
    """The two slits re-declared beside tmp_path, no generator: the record of one part reads its digits at the union of the regions' Nodes once per close (64 digits of 48 bits, 3,072 bits), and every quantum of the close takes two division acts, its region and its Node; at the shipped window of 130 (one close, 660 quanta) the digits are spent and the read is refused by name, the write's bound not blamed; the draws until the refusal and the bits each took are printed."""
    holder: list[Lattice] = []
    seen = spied(monkeypatch, lambda: holder[0])
    path = world_beside(tmp_path, EVENTS / "two_slits" / "two_slits.json", lambda w: None)
    board = Lattice(load_world(path), (lines := []).append)
    holder.append(board)
    with pytest.raises(
        RuntimeError,
        match="the regions of 'charge' at the interval 130 has the number .* left, below the draw's total",
    ) as refusal:
        for _ in range(board.world.intervals):
            board.step()
    assert "digits read are spent at this close" in str(refusal.value) and "amplitude bound" not in str(
        refusal.value
    )
    first = seen[0]
    assert first["label"] == "the regions of 'charge' at the interval 130" and len(first["digits"]) == 64
    assert (
        first["number"] == read_number(first["digits"], first["walls"])
        and len(first["walls"]) == 64
        and set(first["walls"]) == {108_000_001}  # the base at the content 60, one above the 108,000,000
    )
    bits = [math.log2(sum(s["weights"])) for s in seen]
    for earlier, later in zip(seen, seen[1:], strict=False):
        assert later["number"] == earlier["left"]
    print(
        f"the two slits at the window 130: {len(seen)} draws before the refusal ({len(seen) // 2} quanta), the number {first['number'].bit_length()} bits, the totals {min(bits):.1f} to {max(bits):.1f} bits each, the credit lines {sum(1 for c in lines if c['event'] == 'credit')}"
    )


def test_a_sides_two_lines_read_one_index_per_node_equal_before_the_write_and_complementary_after(
    monkeypatch,
):
    """The digits' pair identity (the builder's measurement on the read's second commit, bell a' b: in 474 reads of 237 worlds the two lines' indices equal at every Node in 357 and complementary in 117, none else): on the shipped bell worlds each side reads the record's two lines at its four Nodes at the close 100, w div F = 108,000,000 at F = 3,072,000 on light's wall 331,776,000,000,000. At every Node the second line's index r div F equals the first line's before any write (the left side, the parts laid alike) and after a write of equal coefficients, and is w div F less it after the write of (1, -1), the second part negated (the right side of a' b, the left side's basis [1, 1], read after the left side's write at the birth): a side's eight digits are its four Nodes' digits twice. Where the left side's port zeroes a part (a b, the basis [1, 0]) the right side reads that part's line at the lay's origin, w div 2F at every Node, the third form. The read takes both lines (`digits.read_of`); the identity is pinned and nothing in the read changed; the indices and the coefficients standing at the right side's read printed."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", ROOT)
    whole, found = LIGHT // 3_072_000, {}  # w div F at the shipped content
    for name in ("bell_a_prime_b", "bell_a_b"):
        board, standing = Lattice(load_shipped(EVENTS / "bell" / f"{name}.json")), []
        seen, spy = spied(monkeypatch, lambda board=board: board), node_detector.drawn_from

        def noted(number, weights, label, board=board, standing=standing, spy=spy):  # type: ignore[no-untyped-def]
            standing.append(list(board.credit.written.get(family(board, "light_pair"), [1, 1])))
            return spy(number, weights, label)

        monkeypatch.setattr(node_detector, "drawn_from", noted)
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
        found[name] = sides[0][1], sides[2][1], standing[2]  # each side's first draw reads
    for left, right, written in found.values():
        assert left[4:] == left[:4]  # no write yet: the second line's index the first's at every Node
        if written[0] == written[1]:
            assert right[4:] == right[:4]  # equal coefficients: equal indices
        elif written[0] == -written[1]:
            assert right[4:] == [whole - k for k in right[:4]]  # the sign write: w div F less it
        else:
            zeroed = written.index(0)  # the part the left side's port zeroed reads the lay's origin
            assert right[4 * zeroed : 4 * zeroed + 4] == [whole // 2] * 4
    assert found["bell_a_b"][2].count(0) == 1  # the basis [1, 0] zeroes a part
    print(f"the pair identity: {found}")
