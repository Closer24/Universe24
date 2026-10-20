"""The acceptance lines of the one meeting (the builder's nine lines endorsed by the owner, 2026-10-20, as the branch's tests; ALGEBRA.md, The click is the meeting of the future with the past: at the root it writes; The meeting's identity, the Gram theorem): 1 the four shipped Bell worlds read E = -119 / 169, 119 / 169, -120 / 169, -120 / 169 as the settings fall (a b, a b', a' b, a' b'), S = 478 / 169, every marginal 1 / 2, the credit lines one per side with its realised port, its order and the record's scale, the part written 0 at 0 after the close; 2 the four shipped GHZ worlds E_3 = +1, -1, -1, -1 (x x x, x y y, y x y, y y x), every marginal 1 / 2, every pairwise correlation 0, the eight shares 0 or 1 / 4, two worlds per test for the clock; 4 the born pair's four worlds (the atom giving the pair family at its window's close, 24, in the exact dark, A reading in the first window and B in the second) the same E and S through the sides' own reads, two worlds per test; 5 by design, the write stands at the record's birth inside the run back and never at the close (`meeting_back.realised` from `lists.readings`); 6 the inverse across the write in tests/test_the_meeting_back.py (f), MATCH before and after the close and the engine's own exactness inside the act; 3 and 7 the reader's later design; 8 the byte-for-byte digest of a world without a record of several parts in (d) there; 9 the gates (tools/check.py). The numbers from the parts lines by the reader's arithmetic (tests/laws_spin.py) and the engine's weights at every draw against them (`sided`)."""

import copy
from dataclasses import fields
from fractions import Fraction

import numpy as np
import pytest

from event_universe import credit, meeting_back
from event_universe.credit import Books
from event_universe.lattice import Lattice
from event_universe.loader.draw import norm, times
from event_universe.world_files import load_world
from tests.laws import EVENTS, family, world_beside
from tests.laws_spin import PORT, digest, joint_shares, marginal_of, reduced_write, sided

BELL = {  # the four shipped singlet worlds and the blind's E, the settings a b, a b', a' b, a' b'
    "singlet_a_b": Fraction(-119, 169),
    "singlet_a_b_prime": Fraction(119, 169),
    "singlet_a_prime_b": Fraction(-120, 169),
    "singlet_a_prime_b_prime": Fraction(-120, 169),
}
GHZ = {"ghz_x_x_x": 1, "ghz_x_y_y": -1, "ghz_y_x_y": -1, "ghz_y_y_x": -1}  # the four shipped worlds' E_3
CHSH = ("singlet_a_b", "singlet_a_b_prime", "singlet_a_prime_b", "singlet_a_prime_b_prime")


def sums(pairs):  # type: ignore[no-untyped-def]
    """The sum of Gaussian integers, pair by pair."""
    found = (0, 0)
    for pair in pairs:
        found = (found[0] + pair[0], found[1] + pair[1])
    return found


def expected_scales(board: Lattice, index: int, realised: list[int]) -> list[int]:
    """The record's scale after each side's write, the norm's square of the coefficients standing on its parts (`credit.scale_of`): the sides in the declared order, the first side's coefficients the determinant's for an antisymmetric family (`meeting_back.coefficients_of`), each later side's the pattern's own, reduced by their gcd over the surviving parts and multiplied onto them, nothing where they are one value there (`reduced_write`, `credit.reduced`)."""
    family, written, found = board.families[index], [(1, 0)] * board.families[index].parts, []
    for k, ((_name, ports), port) in enumerate(zip(board.credit.sides, realised, strict=True)):
        coefficients = meeting_back.coefficients_of(family, ports, k == 0)[port]
        written = reduced_write(written, list(coefficients))
        found.append(sum(w[0] * w[0] + w[1] * w[1] for w in written))
    return found


def loaded(tmp_path, folder: str, name: str):  # type: ignore[no-untyped-def]
    """A shipped world copied beside tmp_path with the `meeting` key stripped where a file still carries it (the files move to the one meeting), loaded on the lattice with its output lines: the board and the lines."""
    source = EVENTS / folder / f"{name}.json"
    path = world_beside(tmp_path / name, source, lambda world: world["draw"].pop("meeting", None))
    lines: list[dict] = []  # type: ignore[type-arg]
    return Lattice(load_world(path), lines.append), lines


def run(tmp_path, folder: str, name: str, board=None, lines=None):  # type: ignore[no-untyped-def]
    """A shipped world run through its intervals (`loaded`, or the board and lines given): the board, its output lines and its credit lines' realised ports (0 plus, 1 minus)."""
    if board is None:
        board, lines = loaded(tmp_path, folder, name)
    for _ in range(board.world.intervals):
        board.step()
    clicks = [
        c for c in lines if c["event"] == "credit" and c.get("order") is not None
    ]  # the sides' draws
    return board, lines, clicks, [PORT[c["realised"]] for c in clicks]


def test_line_1_the_four_bell_worlds_read_the_blind_through_the_sides_own_draws(tmp_path):
    """Line 1: the four shipped Bell worlds under the one meeting, each run once: the two credit lines, left then right, with the orders 1 and 2, the count 1, nothing left and the record's scale after each write; the engine's weights at each draw the chain rule from the parts lines exactly (`sided`, the first side at (1, 0) or (1, 1), one magnitude); E the blind's fraction, S = 478 / 169 in the CHSH combination, every marginal 1 / 2; the part written 0 by the first side's determinant coefficients at zero levels after the close (the first side at (1, 0)), the surviving part scaled."""
    found = {}
    for name, expected in BELL.items():
        board, lines, clicks, realised = run(tmp_path, "bell_singlet", name)
        spin = family(board, "spin")
        sides = {r.name: (r.axis, [list(p) for p in r.pattern]) for r in board.world.node_detectors}
        shares = joint_shares(lines, sides, -1 if board.families[spin].exchange < 0 else 0)
        total = sum(shares.values())
        sided(board, spin, shares, realised)
        assert [(c["node_detector"], c["order"], c["count"], c["left"]) for c in clicks] == [
            ("left", 1, 1, 0),
            ("right", 2, 1, 0),
        ]
        assert [c["scale"] for c in clicks] == expected_scales(board, spin, realised)
        assert [c["board_count"] for c in clicks] == [1, 1]  # the count on the board at the close
        found[name] = Fraction(shares[0, 0] + shares[1, 1] - shares[0, 1] - shares[1, 0], total)
        assert found[name] == expected, name
        for side in range(2):
            assert Fraction(marginal_of(shares, side)[0], total) == Fraction(1, 2)
        first = meeting_back.coefficients_of(board.families[spin], board.credit.sides[0][1], True)
        width = board.families[spin].width
        for part, c in enumerate(first[realised[0]]):
            if c == (0, 0):  # the part written 0 at the birth stands at 0 after the close
                for line in board.states[spin].lines[part * width : (part + 1) * width]:
                    assert not line.now.any() and not line.before.any()
        print(
            f"{name}: E = {found[name]}, the realised pair {realised}, the scales {[c['scale'] for c in clicks]}"
        )
    a, b, c, d = (found[name] for name in CHSH)
    assert abs(a - b + c + d) == Fraction(478, 169)


def ghz_read(tmp_path, name: str, expected: int) -> None:  # type: ignore[no-untyped-def]
    """One shipped GHZ world under the one meeting (the cone): the three credit lines in the declared order, the engine's weights at each draw the chain rule from the parts lines exactly (every coefficient written 0 or 1 in magnitude), E_3 the gate's sign, every marginal 1 / 2, every pairwise correlation 0, the eight shares 0 or 1 / 4."""
    board, lines, clicks, realised = run(tmp_path, "ghz", name)
    light = family(board, "light_ghz")
    sides = {r.name: (r.basis, [list(p) for p in r.pattern]) for r in board.world.node_detectors}
    shares = joint_shares(lines, sides, 0, board.families[light].width)
    total = sum(shares.values())
    sided(board, light, shares, realised)
    assert [(c["node_detector"], c["order"], c["count"]) for c in clicks] == [
        (n, order, 1) for order, (n, _p) in enumerate(board.credit.sides, 1)
    ]
    assert Fraction(sum(v * (-1) ** sum(k) for k, v in shares.items()), total) == expected
    for side in range(3):
        assert Fraction(marginal_of(shares, side)[0], total) == Fraction(1, 2)
    for pair in ((0, 1), (0, 2), (1, 2)):
        assert sum(v * (-1) ** (k[pair[0]] + k[pair[1]]) for k, v in shares.items()) == 0
    assert all(Fraction(v, total) in (Fraction(0), Fraction(1, 4)) for v in shares.values())
    print(
        f"{name}: E_3 = {expected}, the realised triple {realised}, the scales {[c['scale'] for c in clicks]}"
    )


def test_line_2_the_ghz_world_x_x_x_reads_the_gates_sign(tmp_path):
    """Line 2, the first of the four shipped GHZ worlds (the clock gives each world its own test): x x x reads E_3 = +1, marginals 1 / 2, pairwise 0, the eight shares 0 or 1 / 4."""
    ghz_read(tmp_path, "ghz_x_x_x", GHZ["ghz_x_x_x"])


def test_line_2_the_ghz_world_x_y_y_reads_the_gates_sign(tmp_path):
    """Line 2, the second shipped GHZ world: x y y reads E_3 = -1, marginals 1 / 2, pairwise 0, the eight shares 0 or 1 / 4."""
    ghz_read(tmp_path, "ghz_x_y_y", GHZ["ghz_x_y_y"])


def test_line_2_the_ghz_world_y_x_y_reads_the_gates_sign(tmp_path):
    """Line 2, the third shipped GHZ world: y x y reads E_3 = -1, marginals 1 / 2, pairwise 0, the eight shares 0 or 1 / 4."""
    ghz_read(tmp_path, "ghz_y_x_y", GHZ["ghz_y_x_y"])


def test_line_2_the_ghz_world_y_y_x_reads_the_gates_sign(tmp_path):
    """Line 2, the fourth shipped GHZ world: y y x reads E_3 = -1, marginals 1 / 2, pairwise 0, the eight shares 0 or 1 / 4; over the four M = 1 - (-1) - (-1) - (-1) = 4 in magnitude, the gate's signs."""
    ghz_read(tmp_path, "ghz_y_y_x", GHZ["ghz_y_y_x"])


def born_read(tmp_path, name: str) -> Fraction:  # type: ignore[no-untyped-def]
    """One born-pair world (examples/events/bell_singlet, the atom at the Node 12 giving the pair family at its window's close, 24, in the exact dark (no draw), under the board's reach, A's window closing at 62 before B's beam arrives, B's at 124): the two credit lines, left at 62 with the order 1 and right at 124 with the order 2 (the sides drawing in the order of their closes), the record's scale on each; A's weights the parts' shares, 1 / 2 and 1 / 2 (the Gram of B's identity pattern the identity, the parts laid alike); B's weights at the realised port the singlet's amplitude on the record rewritten by A's determinant coefficients, exactly (one magnitude); E read from the two conditionals, -cos(theta_a - theta_b). The finding of 2026-10-20 (Hand E's drafts), fixed the same day (the reader's F3): B's run back once returned, where A's write zeroed a part, the surviving part spread over 21 Nodes with the largest level 9 at the birth, a residual of levels the inverse could not undo, since `meeting_back.crossed` restored a crossed lay's remainder from pass 1's log at each of the source's increments (the Node 12, the intervals 18 to 28) while the run forward from the rewritten birth carried other remainders; the fix: a lay without an origin changes no remainder, a lay with an origin logs the board's remainder into its `before` on the way forward and the inverse restores that; the record at the birth as each run back returns it, (Nodes lit, largest level) per line, is the lay's one Node at the level 11 on every surviving part from both run backs (B's run back finds the part A's determinant coefficient zeroed at 0), pinned here; the E fractions were untouched by the residual (one surviving part, or parts alike)."""
    board, lines = loaded(tmp_path, "bell_singlet", name)
    spin, births = family(board, "spin"), {}

    def at_the_birth(interval: int, direction: int, passes: int) -> None:
        if (
            direction < 0 and interval == board.credit.birth
        ):  # the run back arrived at the birth: the record as the inverse returns it
            levels = [np.asarray(line.now) for line in board.states[spin].lines]
            births[passes] = [(int((a != 0).sum()), int(abs(a).max())) for a in levels]

    board.observers.append(at_the_birth)
    board, lines, clicks, realised = run(tmp_path, "bell_singlet", name, board, lines)
    books = board.credit
    print(
        f"{name}: the record at the birth as the run backs return it, (Nodes lit, largest level) per line: {births}"
    )
    residual = {
        2: [(1, 11), (0, 0), (1, 11), (0, 0)]
    }  # A's run back: the lay's one Node, the level 11 per part
    residual[
        4
    ] = (  # B's run back returns the written birth bit for bit (the reader's fix of 2026-10-20)
        [(1, 11), (0, 0), (0, 0), (0, 0)] if name in ("born_a_b", "born_a_b_prime") else residual[2]
    )
    assert (
        births == residual
    )  # the lay's one Node at the level 11 on the surviving parts, from both run backs
    assert [(c["node_detector"], c["order"], c["interval"], c["count"]) for c in clicks] == [
        ("left", 1, 62, 1),
        ("right", 2, 124, 1),
    ]
    first = books.weights[(spin, "left")]
    assert first[0] == first[1] > 0  # the parts' shares alone, 1 / 2
    (_a, ports_a), (_b, ports_b) = books.sides
    lambdas = meeting_back.coefficients_of(board.families[spin], ports_a, True)  # the determinant's
    conditional = {  # |SUM_k e_k(q) lambda_k|^2 on Gaussian pairs, the reals here
        p: [
            norm(sums(times(e, lam) for e, lam in zip(ports_b[q], lambdas[p], strict=True)))
            for q in range(2)
        ]
        for p in range(2)
    }
    second = books.weights[(spin, "right")]
    p = realised[0]
    assert second[0] * conditional[p][1] == second[1] * conditional[p][0] and sum(second) > 0
    assert [c["scale"] for c in clicks] == expected_scales(board, spin, realised)
    assert [c["board_count"] for c in clicks] == [1, 1]  # the count on the board at the two closes
    found = sum(  # E = SUM_p P(p) s_p (P(+ | p) - P(- | p)), the marginal 1 / 2, s_p the port's sign
        Fraction(1, 2) * (1 - 2 * p) * Fraction(w[0] - w[1], sum(w)) for p, w in conditional.items()
    )
    print(f"{name}: E = {found}, the realised pair {realised}, A's weights {first}, B's {second}")
    return found


def test_line_4_the_born_pair_a_b_and_a_b_prime(tmp_path):
    """Line 4, the first two born-pair worlds: E = -119 / 169 at (a, b) and 119 / 169 at (a, b'), read through the sides' own draws at their own closes, A's at 62 and B's at 124."""
    assert born_read(tmp_path, "born_a_b") == Fraction(-119, 169)
    assert born_read(tmp_path, "born_a_b_prime") == Fraction(119, 169)


def test_line_4_the_born_pair_a_prime_b_and_a_prime_b_prime(tmp_path):
    """Line 4, the other two born-pair worlds: E = -120 / 169 at (a', b) and at (a', b'); with the first test |S| = 478 / 169 through the born pair."""
    assert born_read(tmp_path, "born_a_prime_b") == Fraction(-120, 169)
    assert born_read(tmp_path, "born_a_prime_b_prime") == Fraction(-120, 169)


def test_the_born_pair_runs_under_the_cone_reach_since_the_remainders_fix(tmp_path):
    """The question of 2026-10-20 (the Boss's), answered by this test and closed the same day: the born pair's world run under the cone's reach, the atom body standing on the board. Before the reader's F3 the cone stepped alone refused the run back from A's close at 62 by name at the interval 24 ("the rest at the record's cone's edge moved ... the array spin.lines[0].before at the Node [3, 0, 0]"): `meeting_back.crossed` restored each crossed lay's remainder from pass 1's log, and the source's increments at the Node 12 (the intervals 18 to 28) carried pass 1's remainders into the run back's history, whose walk reached the ring; the board's reach at the same interval held the wave at 0 at the Node 3 (the dynamics were never the fault). Since the fix (a lay without an origin changes no remainder, a lay with an origin logs the board's remainder forward and restores it back) the cone's reach runs the born pair whole: the same two credit lines as the board's reach, the same realised ports, orders, scales and counts on the board, the same weights at both sides and so the same E through the sides' draws."""
    source = EVENTS / "bell_singlet" / "born_a_b.json"
    found = {}
    for reach in ("cone", "board"):

        def edited(world, reach=reach):  # type: ignore[no-untyped-def]
            world["draw"].pop("meeting", None)
            world["draw"]["reach"] = reach

        lines: list[dict] = []  # type: ignore[type-arg]
        board = Lattice(
            load_world(world_beside(tmp_path / f"born_{reach}", source, edited)), lines.append
        )
        for _ in range(board.world.intervals):
            board.step()
        spin = family(board, "spin")
        clicks = [c for c in lines if c["event"] == "credit" and c.get("order")]
        found[reach] = (
            [
                (
                    c["node_detector"],
                    c["order"],
                    c["interval"],
                    c["realised"],
                    c["scale"],
                    c["board_count"],
                )
                for c in clicks
            ],
            board.credit.weights[(spin, "left")],
            board.credit.weights[(spin, "right")],
        )
    print(f"the born pair under the cone's reach and the board's: {found}")
    assert found["cone"] == found["board"] and len(found["cone"][0]) == 2


def test_the_write_is_the_realised_terms_direction_and_a_scaling_writes_nothing(tmp_path):
    """The Boss's amendment of 2026-10-20 to the write's design (`credit.reduced`): the shipped bell world (a, b) with the draw's window cut to 50 over its 100 intervals (at 40 the beams' share through the sides stands below a whole quantum, the side's gate; by 50 it is through), the record of many quanta clicking once per window: at 50 the left's write leaves one part (the identity pattern's port, the scale 1) and the right's (12, 5) on the one surviving part reduces to 1 and writes nothing (the scale stays 1); at 100 both sides click again on the one-part record and write nothing (the reader's ruling, precision one: a side already realised that clicks again in the same setting realises the same port with certainty), the coefficients standing bit for bit the same before and after the close, the scale 1 on every line, the orders 1 and 2 of a new sequence, the count down by one per window; on a two-part write with coprime coefficients the gcd is 1 and the write stands (a' b: (12, 5) onto (-1, 1), the scale 169, `test_line_1`)."""
    source = EVENTS / "bell" / "bell_a_b.json"

    def cut(world):  # type: ignore[no-untyped-def]
        world["draw"]["window"] = 50

    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_world(world_beside(tmp_path / "bell_cut", source, cut)), lines.append)
    pair, written = family(board, "light_pair"), {}

    def observer(interval: int, direction: int, _passes: int) -> None:
        if direction > 0 and interval not in written:
            written[interval] = list(board.credit.written.get(pair, []))

    board.observers.append(observer)
    for _ in range(100):
        board.step()
    clicks = [c for c in lines if c["event"] == "credit" and c.get("order")]
    assert [(c["interval"], c["node_detector"], c["scale"]) for c in clicks] == [
        (50, "left", 1),
        (50, "right", 1),
        (100, "left", 1),
        (100, "right", 1),
    ]
    assert written[100] == board.credit.written[pair] and sorted(norm(w) for w in written[100]) == [0, 1]
    assert [c["left"] for c in clicks] == [clicks[0]["left"]] * 2 + [clicks[0]["left"] - 1] * 2
    assert [c["realised"] for c in clicks[2:]] == [
        c["realised"] for c in clicks[:2]
    ]  # the same ports, certain
    assert [c["order"] for c in clicks] == [1, 2, 1, 2]  # the second window's clicks a new sequence
    print(
        f"the bell world cut to 50: the coefficients standing {board.credit.written[pair]}, the lines' left {[c['left'] for c in clicks]}"
    )


def test_a_side_whose_realised_port_carries_no_overlap_is_refused_and_the_loader_reads_the_compounding(
    tmp_path,
):
    """The reader's ruling of 2026-10-20, the two precisions. One: a later click of a side in a changed setting needs the overlaps with the written factor, which the parts carry no more, refused by name; no setting changes within a run, so the test turns the booked port of the bell world's left side after its first window, cut to 50 (the port whose part the first write zeroed, its weight 0 on the written record), and steps to the second close. Two: the loader refuses by name a world whose sides' patterns compound past the amplitude bound: the singlet world (a, b) with the left's axis turned to (-12, 5) beside the right's (12, 5) compounds to (-25, 144) on its two terms (the determinant's lambdas (5, 12) first), 144 times the lay's amplitude 64 = 9216 over A = 6949; the shipped worlds all pass the gate (the bell folder's record compounds to a unit after its first write)."""
    cut = EVENTS / "bell" / "bell_a_b.json"

    def window(world):  # type: ignore[no-untyped-def]
        world["draw"]["window"] = 50  # the beams' share through the sides by the first close

    board = Lattice(load_world(world_beside(tmp_path / "bell_turned", cut, window)))
    pair = family(board, "light_pair")
    for _ in range(50):
        board.step()
    port, node, settled = board.credit.taken[pair]["left"]
    board.credit.taken[pair]["left"] = (
        1 - port,
        node,
        settled,
    )  # the setting turned: the other port booked
    with pytest.raises(RuntimeError, match="carrying no overlap with the written factor"):
        for _ in range(50):
            board.step()

    def turned(world):  # type: ignore[no-untyped-def]
        world["draw"].pop("meeting", None)
        world["node_detectors"][0]["axis"] = [-12, 5]

    with pytest.raises(
        ValueError, match="compound on the record of 'spin' to the coefficient 144"
    ) as refused:
        load_world(
            world_beside(tmp_path / "compounding", EVENTS / "bell_singlet" / "singlet_a_b.json", turned)
        )
    assert "times the lay's amplitude 64: 9216 passes the amplitude bound A = 6949" in str(refused.value)


def test_line_7_the_count_on_the_board_reads_the_books_count_at_every_close(tmp_path):
    """Line 7, the count on the board (ALGEBRA.md, The count on the board, the owner's word of 2026-10-20; the builder's line read on the branch's form): `Lattice.count`, (n S + scale W div 2) div (scale W), read at every interval of the singlet world (a, b) and of the born pair's world: 1 at every interval from the lay (the singlet) or from the birth (the born pair, 0 before it) through the last close, the writes at the birth moving the share by the scale over n and the count by nothing; the credit lines' `board_count` 1 at both sides; equal to the books' count at every close by the engine's own check before the acts (`meeting.closed`, refused by name otherwise); after the close where every side has drawn the books' count is 0 and the board's follows the erasing front."""
    found = {}
    for name, birth in (("singlet_a_b", 0), ("born_a_b", 24)):
        board, lines, spin, calls = stepped(tmp_path, "bell_singlet", name)
        counts = [calls[t][3] for t in range(1, board.world.intervals + 1)]
        clicks = [c for c in lines if c["event"] == "credit" and c.get("order")]
        one = next(
            t for t, count in enumerate(counts, 1) if count == 1
        )  # the source's increments past half
        assert (
            all(count == 0 for count in counts[: one - 1]) and birth <= one <= clicks[0]["interval"]
        ), name
        assert all(count == 1 for count in counts[one - 1 : clicks[-1]["interval"]]), name
        assert [c["board_count"] for c in clicks] == [1, 1] and board.credit.counts[spin] == 0, name
        found[name] = (one, counts[clicks[-1]["interval"] - 1], board.count(spin))
    print(
        f"(7) the count on the board (the first interval reading 1, at the last close, at the end): {found}"
    )
    assert found == {
        "singlet_a_b": (1, 1, 1),
        "born_a_b": (36, 1, 1),
    }  # the born increments past half at 36, from the birth at the atom's close, 24


# The clicks in sequence (the owner's word of 2026-10-20, through the builder: "Clicks are discrete, but no click
# jumps from nowhere; they happen in sequence."): four verifications of the one meeting, (a) to (d).


def stepped(tmp_path, folder: str, name: str, edit=None):  # type: ignore[no-untyped-def]
    """A shipped world beside tmp_path, the `meeting` key stripped and `edit` applied, run through its intervals with an observer recording at the first call of every interval (the step's own after its acts, or at a close with a reading the run back's, the board as Rule3 left it before any write) the sides' moments, the frame's digest, the Books' fields holding data, the record's count on the board (`Lattice.count`) and, at the first side's run forward's arrival (pass 3), the moments re-booked from the rewritten record; returns the board, its lines, the spin family and the record per interval."""
    source = EVENTS / folder / f"{name}.json"

    def edited(world):  # type: ignore[no-untyped-def]
        world["draw"].pop("meeting", None)
        if edit is not None:
            edit(world)

    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_world(world_beside(tmp_path / name, source, edited)), lines.append)
    spin, calls = family(board, "spin"), {}

    def observer(interval: int, direction: int, passes: int) -> None:
        if direction < 0:
            return
        books = board.credit
        if interval not in calls:  # at a close the run back's call, before any write
            calls[interval] = (
                copy.deepcopy(books.moments.get(spin, {})),
                digest(board),
                {f.name for f in fields(Books) if bool(getattr(books, f.name))},
                board.count(spin),
                None,
            )
        if passes == 3 and calls[interval][4] is None:  # the first side's run forward arrived: re-booked
            calls[interval] = (*calls[interval][:4], copy.deepcopy(books.moments.get(spin, {})))

    board.observers.append(observer)
    for _ in range(board.world.intervals):
        board.step()
    return board, lines, spin, calls


def test_the_clicks_in_sequence_a_the_far_side_books_nothing_before_its_beam_arrives(tmp_path):
    """(a) On the born pair's world (the atom at the Node 12 of the chain of 61, the left region x 0..3 near it, the right x 57..60 far; the draw's window 62, A's close at 62 and B's at 124): the right side's own second moments are 0 at every interval before the beam's first level stands in its region, its first parts line and its first booking are at the interval after the arrival (the step reads the state it starts from), and its credit line's interval is after it; the left's books begin when its beam arrives. The fifth world's lay is centred (the packets' top at x 16 of the chain of 33, the regions at 0..3 and 29..32), both beams arriving together, so the sequence there is the declared order's at the one close."""
    lines: list[dict] = []  # type: ignore[type-arg]
    source = EVENTS / "bell_singlet" / "born_a_b.json"
    path = world_beside(tmp_path / "born", source, lambda world: world["draw"].pop("meeting", None))
    board = Lattice(load_world(path), lines.append)
    spin, arrival, standing = family(board, "spin"), {}, {}
    for _ in range(board.world.intervals):
        board.step()
        for side in ("left", "right"):
            region = next(d.nodes for d in board.node_detectors if d.name == side)
            lit = any(
                bool(np.asarray(line.now)[region].any() or np.asarray(line.before)[region].any())
                for line in board.states[spin].lines
            )
            if lit:
                arrival.setdefault(side, board.interval)
            moments = board.credit.moments.get(spin, {}).get(side)
            if moments is not None and credit.standing(moments):
                standing.setdefault(side, board.interval)
    parts = {
        side: min(
            line["interval"]
            for line in lines
            if line["event"] == "parts" and line["node_detector"] == side
        )
        for side in ("left", "right")
    }
    clicks = {
        c["node_detector"]: c["interval"] for c in lines if c["event"] == "credit" and c.get("order")
    }
    print(
        f"(a) the born pair: the beam's first level at the left {arrival['left']}, at the right {arrival['right']}; "
        f"the moments first standing at the left {standing['left']}, at the right {standing['right']}; the first "
        f"parts lines at {parts}; the credit lines at {clicks}; the fifth world's lay is centred"
    )
    for side in ("left", "right"):  # the parts line and the book read the state the step starts from
        assert standing[side] == parts[side] == arrival[side] + 1 and clicks[side] > arrival[side]
    assert arrival["left"] < arrival["right"] and clicks == {"left": 62, "right": 124}


def test_the_clicks_in_sequence_b_one_packet_removed_the_far_side_reads_the_lays_leak(tmp_path):
    """(b) The singlet's chain with the packet toward +x removed, declared here: the right side receives no beam by the lay's word, and what the engine gives is measured, not presumed. The short packet (edge 6 at the wave 1 / 4) is laid at the even phase at its top (cos(4 pi) = 1 at x = 16), so its levels sum to 1.017 b over the row and the massless correction takes 0.17 b e_i out of each level (`lay.corrected`): a standing hump of 5.8 percent of the form, half of it moving +x on the massless row, the lay's own backward root 3e-4 beside it (ALGEBRA.md, The packet lay; the exact lay is on shell per component), so the right side reads the hump's part, measured here at 2 percent of the moments; the remedy an edge of one wavelength or the odd phase; the builder's third of 2026-10-20 was his build's: the right's moments, its weights against the left's and whether a credit line appears are pinned as the engine gives them; the left draws first at its own place on its full marginal, 1 / 2 and 1 / 2, since its parts stand alike; the owner's line, nothing clicks where nothing arrived, is what the test states, and here the leak arrives below one whole quantum through the right side's window, so the side's gate keeps it from drawing (the reader's F4 of 2026-10-20, `lists.readings`): the left side clicks alone, the right's moments booked and its weights never drawn, the record's count standing at 1."""

    def one_beam(world):  # type: ignore[no-untyped-def]
        world["packets"] = [
            p for p in world["packets"] if p["wave"][0] < 0
        ]  # the packet toward -x alone

    board, lines, spin, calls = stepped(tmp_path, "bell_singlet", "singlet_a_b", one_beam)
    books = board.credit
    clicks = [
        (c["node_detector"], c["order"], c["interval"])
        for c in lines
        if c["event"] == "credit" and c.get("order")
    ]
    weights = {side: books.weights.get((spin, side)) for side in ("left", "right")}
    moments = calls[40][0]
    ratio = Fraction(sum(weights["right"]), sum(weights["left"])) if weights["right"] else None
    print(
        f"(b) one packet: the credit lines {clicks}; the moments at the close {moments}; the weights {weights}; the "
        f"right's weights over the left's {ratio}; the count left {books.counts[spin]}"
    )
    assert clicks == [("left", 1, 40)] and books.counts[spin] == 1  # the leak below a quantum: no click
    assert moments == {
        "left": [[(185800, 0)] * 2] * 2,
        "right": [[(3715, 0)] * 2] * 2,
    }  # the leak 3715 / 185800, 2 %
    assert weights["left"] == [185800, 185800] and weights["right"] is None  # the right never draws


def test_the_clicks_in_sequence_d_the_books_hold_nothing_joint(tmp_path):
    """(d) The Books at every close, on the born pair's world (two closes) and on the singlet (one): the fields holding data are among the declaration, the read's number left, the per-side moments and the patterns, the counts, the inflows and passages the credit always had, the sides' order, the births, the lays' and faces' logs, the write's coefficients and scale and the reading's own (the realised ports, the likeness, the weights kept as a diagnostic, the record run, the Node-steps); the born pair's world runs under the cone's reach, whose books are these: at A's close the reference (the board at the born record's birth), at B's close the birth, the reference, the cone's volumes, the regrown close and the Node-steps beside the write's; nothing joint: no joints, no J, no conditioning, no levels of one side in another's book; the set pinned per close."""
    names = {f.name for f in fields(Books)}
    assert not names & {"joints", "levels", "conditioning", "joined", "popped", "reweighted"}
    always = {
        "declaration",
        "elapsed",
        "counts",
        "intake",
        "sides",
        "bodies",
        "fronts",
        "faces",
        "sources",
        "units",
        "empty",
        "clocks",
        "windows",
        "deficits",
        "unabsorbed",
        "unabsorbed_units",
        "emitters",
        "remainders",
        "passages",
        "left",
        "patterns",
    }
    own = {
        "births",
        "birth",
        "support",
        "reference",
        "cone",
        "regrown",
        "stepped",
        "lays",
        "moments",
        "written",
        "scale",
        "taken",
        "alike",
        "weights",
    }
    assert names == always | own
    held = {}
    for name in ("born_a_b", "singlet_a_b"):
        _board, lines, _spin, calls = stepped(tmp_path, "bell_singlet", name)
        closes = sorted({c["interval"] for c in lines if c["event"] == "credit" and c.get("order")})
        held[name] = {interval: sorted(calls[interval][2]) for interval in closes}
    print(f"(d) the fields holding data at the closes: {held}")
    credit = [
        "clocks",
        "counts",
        "declaration",
        "emitters",
        "empty",
        "intake",
        "passages",
        "units",
        "windows",
    ]
    read = ["births", "left", "moments", "patterns", "sides", "support", "taken", "weights"]
    cone = ["birth", "reference", "cone", "regrown", "stepped"]  # the cone's reach books these
    assert held == {
        "born_a_b": {
            62: sorted(
                credit + read + ["bodies", "lays", "reference"]
            ),  # A's draw, the record born at 24
            124: sorted(
                credit
                + read
                + cone
                + ["bodies", "lays", "alike", "scale", "written"]
                + ["unabsorbed", "unabsorbed_units"]
            ),  # B's draw after A's write, under the cone
        },
        "singlet_a_b": {40: sorted(credit + read + ["reference"])},  # the record laid at the start
    }
    for name, closes in held.items():
        for interval, holding in closes.items():
            assert set(holding) <= always | own, (name, interval, holding)
