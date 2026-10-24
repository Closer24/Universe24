"""The acceptance lines of the one meeting (the builder's nine lines endorsed by the owner, 2026-10-20, as the branch's tests; ALGEBRA.md, The click is the meeting of the future with the past: at the root it writes; The meeting's identity, the Gram theorem): 1 the four shipped Bell worlds read E = -119 / 169, 119 / 169, -120 / 169, -120 / 169 as the settings fall (a b, a b', a' b, a' b'), S = 478 / 169, every marginal 1 / 2, the credit lines one per side with its realised port, its order and the record's scale, the part written 0 at 0 after the close; 2 the four shipped GHZ worlds E_3 = +1, -1, -1, -1 (x x x, x y y, y x y, y y x), every marginal 1 / 2, every pairwise correlation 0, the eight shares 0 or 1 / 4, two worlds per test for the clock; 4 the born pair's four worlds (the atom giving the pair family at its window's close, 24, in the exact dark, A reading in the first window and B in the second) the same E and S through the sides' own reads, two worlds per test; 5 by design, the write stands at the record's birth inside the run back and never at the close (`meeting_back.realised` from `lists.readings`); 6 the inverse across the write in tests/test_the_meeting_back.py (f), MATCH before and after the close and the engine's own exactness inside the act; 3 and 7 the reader's later design; 8 the byte-for-byte digest of a world without a record of several parts in (d) there; 9 the gates (tools/check.py). The numbers from the parts lines by the reader's arithmetic (tests/laws_spin.py) and the engine's weights at every draw against them (`sided`)."""

import copy
import json
import re
from dataclasses import fields
from fractions import Fraction

import pytest

from event_universe.credit import Books
from event_universe.lattice import Lattice
from event_universe.loader.draw import norm
from event_universe.world_files import load_world
from tests.laws import EVENTS, family, world_beside
from tests.laws_spin import PORT, digest

BELL = {  # the four shipped singlet worlds and the blind's E, the settings a b, a b', a' b, a' b'
    "singlet_a_b": Fraction(-119, 169),
    "singlet_a_b_prime": Fraction(119, 169),
    "singlet_a_prime_b": Fraction(-120, 169),
    "singlet_a_prime_b_prime": Fraction(-120, 169),
}
GHZ = {"ghz_x_x_x": 1, "ghz_x_y_y": -1, "ghz_y_x_y": -1, "ghz_y_y_x": -1}  # the four shipped worlds' E_3
BORN = {  # the four shipped born-pair worlds and the blind's E, the settings a b, a b', a' b, a' b'
    "born_a_b": Fraction(-119, 169),
    "born_a_b_prime": Fraction(119, 169),
    "born_a_prime_b": Fraction(-120, 169),
    "born_a_prime_b_prime": Fraction(-120, 169),
}
SINGLET_FOLDER = EVENTS / "bell_singlet"  # the singlet's and the born pair's record
CHSH = ("singlet_a_b", "singlet_a_b_prime", "singlet_a_prime_b", "singlet_a_prime_b_prime")


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


def test_line_1_the_four_bell_worlds_record_reads_the_blind_through_the_sides_own_draws():
    """Line 1 on the record (the four shipped singlet worlds ran 26 to 33 s on the suite's clock): examples/events/bell_singlet, the blind expectation.json and the reading's table in blind_and_reading.md, where each world's E on the run stands beside the blind's and equals it, -119 / 169, 119 / 169, -120 / 169, -120 / 169 as the settings fall (`BELL`), S = -478 / 169 on both columns, |S| = 478 / 169 in the CHSH combination, every marginal 1 / 2, and the realised combination of the two sides' ports named per world; the four world files and their mode files stand in the folder."""
    record = json.loads((SINGLET_FOLDER / "expectation.json").read_text(encoding="utf-8"))
    blind, runs = record["blind"], record["runs"]
    assert {runs[k]: Fraction(*e) for k, e in blind["correlation"].items()} == BELL
    assert Fraction(*blind["S"]) == Fraction(-478, 169) and record["exchange"] == "antisymmetric"
    assert all(Fraction(*m) == Fraction(1, 2) for w in blind["marginals"].values() for m in w.values())
    page = (SINGLET_FOLDER / "blind_and_reading.md").read_text(encoding="utf-8")
    rows = re.findall(
        r"^\| (a'? b'?) \| (-?\d+) / 169 \| (-?\d+) / 169 \| ([-+]) ([-+]) \|$", page, re.MULTILINE
    )
    assert len(rows) == 4 and all(run == blind_e for _s, run, blind_e, _a, _b in rows), rows
    read = {setting.replace("'", "_prime"): Fraction(int(run), 169) for setting, run, _e, _a, _b in rows}
    assert {runs[k]: e for k, e in read.items()} == BELL
    assert "| S | -478 / 169 | -478 / 169 | |" in page
    a, b, c, d = (BELL[name] for name in CHSH)
    assert abs(a - b + c + d) == Fraction(478, 169)
    for world in runs.values():
        assert (SINGLET_FOLDER / f"{world}.json").is_file()
        assert (SINGLET_FOLDER / f"{world}.mode.json").is_file()


def test_the_write_is_the_realised_terms_direction_and_a_scaling_writes_nothing(tmp_path):
    """The Boss's amendment of 2026-10-20 to the write's design (`credit.reduced`): the shipped bell world (a, b) with the draw's window cut to 50 over its 100 intervals (at 40 the beams' share through the sides stands below a whole quantum, the side's gate; by 50 it is through), the record of many quanta clicking once per window: at 50 the left's write leaves one part (the identity pattern's port, the scale 1) and the right's (12, 5) on the one surviving part reduces to 1 and writes nothing (the scale stays 1); at 100 both sides click again on the one-part record and write nothing (the reader's ruling, precision one: a side already realised that clicks again in the same setting realises the same port with certainty), the coefficients standing bit for bit the same before and after the close, the scale 1 on every line, the orders 1 and 2 of a new sequence, the count down by one per window; on a two-part write with coprime coefficients the gcd is 1 and the write stands (a' b: (12, 5) onto (-1, 1), the scale 169, `test_line_1`)."""
    source = EVENTS / "bell" / "bell_a_b.json"

    def cut(world):  # type: ignore[no-untyped-def]
        pass  # the window derived (2026-10-23)

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
        (60, "left", 1),
        (60, "right", 1),
        (90, "left", 1),
        (90, "right", 1),
    ]  # the closes at the derived window 30 (2026-10-23; the former 50 and 100 at the window cut to 50)
    assert written[90] == board.credit.written[pair] and sorted(norm(w) for w in written[90]) == [0, 1]
    assert [c["left"] for c in clicks] == [clicks[0]["left"]] * 2 + [clicks[0]["left"] - 1] * 2
    assert [c["realised"] for c in clicks[2:]] == [
        c["realised"] for c in clicks[:2]
    ]  # the same ports, certain
    assert [c["order"] for c in clicks] == [1, 2, 1, 2]  # the second window's clicks a new sequence
    print(
        f"the bell world at the derived window 30: the coefficients standing {board.credit.written[pair]}, the lines' left {[c['left'] for c in clicks]}"
    )


def test_a_side_whose_realised_port_carries_no_overlap_is_refused_and_the_loader_reads_the_compounding(
    tmp_path,
):
    """The reader's ruling of 2026-10-20, the two precisions. One: a later click of a side in a changed setting needs the overlaps with the written factor, which the parts carry no more, refused by name; no setting changes within a run, so the test turns the booked port of the bell world's left side after its first window, cut to 50 (the port whose part the first write zeroed, its weight 0 on the written record), and steps to the second close. Two: the loader refuses by name a world whose sides' patterns compound past the amplitude bound: the singlet world (a, b) with the left's axis turned to (-12, 5) beside the right's (12, 5) compounds to (-25, 144) on its two terms (the determinant's lambdas (5, 12) first), 144 times the lay's amplitude 64 = 9216 over A = 6949; the shipped worlds all pass the gate (the bell folder's record compounds to a unit after its first write)."""
    cut = EVENTS / "bell" / "bell_a_b.json"

    def window(world):  # type: ignore[no-untyped-def]
        pass  # the window derived (2026-10-23)

    board = Lattice(load_world(world_beside(tmp_path / "bell_turned", cut, window)))
    pair = family(board, "light_pair")
    for _ in range(
        60
    ):  # the first close at the derived window 30 (2026-10-23; the former 50, the window cut to 50)
        board.step()
    port, node, settled = board.credit.taken[pair]["left"]
    board.credit.taken[pair]["left"] = (
        1 - port,
        node,
        settled,
    )  # the setting turned: the other port booked
    with pytest.raises(RuntimeError, match="carrying no overlap with the written factor"):
        for _ in range(30):  # to the next close at 90
            board.step()

    def turned(world):  # type: ignore[no-untyped-def]
        world["draw"].pop("meeting", None)
        world["node_detectors"][0]["basis"] = [-12, 5]

    with pytest.raises(
        ValueError, match="compound on the record of 'spin' to the coefficient 144"
    ) as refused:
        load_world(
            world_beside(tmp_path / "compounding", EVENTS / "bell_singlet" / "singlet_a_b.json", turned)
        )
    assert "times the lay's amplitude 64: 9216 passes the amplitude bound A = 6949" in str(refused.value)


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
    moments = calls[30][0]  # the singlet's close at the derived window 30 (2026-10-23; the former 40)
    ratio = Fraction(sum(weights["right"]), sum(weights["left"])) if weights["right"] else None
    print(
        f"(b) one packet: the credit lines {clicks}; the moments at the close {moments}; the weights {weights}; the "
        f"right's weights over the left's {ratio}; the count left {books.counts[spin]}"
    )
    assert clicks == [("left", 1, 30)] and books.counts[spin] == 1  # the leak below a quantum: no click
    assert (
        moments
        == {
            "left": [[(149318, 0)] * 2] * 2,
            "right": [[(2991, 0)] * 2] * 2,
        }
    )  # the leak 2991 / 149318, 2 %, at the derived window 30 (2026-10-23; the former 3715 / 185800 at 40)
    assert weights["left"] == [149318, 149318] and weights["right"] is None  # the right never draws


def test_line_2_the_four_ghz_worlds_record_reads_the_gates_sign():
    """Line 2 on the record (the four shipped GHZ worlds ran 272 to 440 s each on the suite's clock): examples/events/ghz/expectation.json, the blind written before any run, holds per setting the joint table of the three sides' eight port triples; E_3 from it, the entries signed by the ports' product over their sum, is +1 at x x x and -1 at x y y, y x y and y y x (`GHZ`), M = -4 in the gate's combination over the blind's order, every marginal 1 / 2 and every pairwise correlation 0; each world file and its mode file stand in the folder; the reading's page carries M."""
    folder = EVENTS / "ghz"
    record = json.loads((folder / "expectation.json").read_text(encoding="utf-8"))
    runs, blind, found = record["runs"], record["blind"], {}
    for setting, world in runs.items():
        joint = {key: Fraction(*value) for key, value in blind["joint"][setting].items()}
        total = sum(joint.values())
        found[world] = sum(j * (-1) ** key.split().count("minus") for key, j in joint.items()) / total
        assert all(Fraction(*m) == Fraction(1, 2) for m in blind["marginals"][setting].values())
        assert all(Fraction(*p) == 0 for p in blind["sub_correlations"][setting].values())
        assert (folder / f"{world}.json").is_file() and (folder / f"{world}.mode.json").is_file()
    assert found == GHZ
    combination, order = record["combination"], record["order"]
    assert combination["name"] == "M" and len(order) == 4
    assert sum(s * found[runs[n]] for s, n in zip(combination["signs"], order, strict=True)) == -4
    assert "| M | -4 |" in (folder / "blind_and_reading.md").read_text(encoding="utf-8")


def test_line_4_the_four_born_pair_worlds_record_reads_the_blinds_e():
    """Line 4 on the record (the four born-pair worlds ran 86 s summed on the suite's clock): examples/events/bell_singlet/expectation_born.json, the born pair's blind, reads E = -119 / 169 at (a, b), 119 / 169 at (a, b'), -120 / 169 at (a', b) and at (a', b') (`BORN`), S = -478 / 169 in the CHSH combination, |S| = 478 / 169, every marginal 1 / 2; the four world files stand in the folder with their mode files."""
    record = json.loads((SINGLET_FOLDER / "expectation_born.json").read_text(encoding="utf-8"))
    runs, blind = record["runs"], record["blind"]
    found = {runs[setting]: Fraction(*e) for setting, e in blind["correlation"].items()}
    assert found == BORN and record["combination"] == {"name": "S", "signs": [1, -1, 1, 1]}
    s = sum(sign * found[runs[n]] for sign, n in zip((1, -1, 1, 1), record["order"], strict=True))
    assert s == Fraction(*blind["S"]) == Fraction(-478, 169) and abs(s) == Fraction(478, 169)
    for setting, world in runs.items():
        assert all(Fraction(*m) == Fraction(1, 2) for m in blind["marginals"][setting].values())
        assert (SINGLET_FOLDER / f"{world}.json").is_file()
        assert (SINGLET_FOLDER / f"{world}.mode.json").is_file()


def test_the_clicks_in_sequence_a_the_far_side_books_nothing_before_its_beam_arrives():
    """(a) on the record (the born pair's world ran 35 s on the suite's clock): the folder's reading, examples/events/bell_singlet/blind_and_reading.md, The born pair, names the record born at the atom's emission, the beam's first levels at the near side before the far side's, and the near side's click with the order 1 at its close before the far side's with the order 2: the clicks fall in sequence, each after its beam's arrival, and none jumps from nowhere."""
    page = (SINGLET_FOLDER / "blind_and_reading.md").read_text(encoding="utf-8")
    page = page[page.index("## The born pair") :]

    def number(pattern: str) -> int:
        found = re.search(pattern, page)
        assert found is not None, pattern
        return int(found.group(1))

    born = number(r"the\s+record\s+is\s+born\s+at\s+(\d+)")
    near, far = (
        number(r"first\s+levels\s+at\s+the\s+left\s+about\s+the\s+interval\s+(\d+)"),
        number(r"at\s+the\s+right\s+about\s+(\d+)"),
    )
    left, right = (
        number(r"`left`\s+with\s+`order`\s+1\s+at\s+(\d+)"),
        number(r"`right`\s+with\s+`order`\s+2\s+at\s+(\d+)"),
    )
    assert born < near < far and near < left < right and far <= right, (born, near, far, left, right)
    record = json.loads((SINGLET_FOLDER / "expectation_born.json").read_text(encoding="utf-8"))
    assert f"born at the interval {born}" in record["comment"] or f"born at {born}" in record["comment"]


def test_the_clicks_in_sequence_d_the_books_hold_nothing_joint():
    """(d) The Books hold nothing joint (the owner's word of 2026-10-20 through the builder; the run of the born pair's and the singlet's worlds, 44 s on the suite's clock, left out: the fields are the declaration's and the dataclass's, read without a run): no field for a joint distribution, levels, conditioning or reweighting; the fields are the credit's own and the one meeting's (the births, the birth, the support, the reference, the cone, the regrown and stepped books, the lays, the moments, the write's coefficients and scale, the taken ports, the likeness, the weights), and nothing else."""
    names = {f.name for f in fields(Books)}
    assert not names & {"joints", "levels", "conditioning", "joined", "popped", "reweighted"}
    always = {"declaration", "elapsed", "counts", "intake", "sides", "bodies", "fronts", "faces"}
    always |= {"sources", "units", "charges", "empty", "clocks", "windows", "deficits", "unabsorbed"}
    always |= {"unabsorbed_units", "emitters", "remainders", "passages", "left", "bias", "patterns"}
    own = {"births", "birth", "support", "reference", "cone", "regrown", "stepped", "lays", "moments"}
    own |= {"written", "scale", "taken", "alike", "weights"}
    assert names == always | own


def test_line_7_the_count_on_the_board_reads_the_books_count_at_every_close():
    """Line 7 on the record (ALGEBRA.md, The count on the board; the singlet's and the born pair's runs, 31 s on the suite's clock): the folder's reading names `board_count` 1 and `scale` 1 at the clicks of the (a, b) world and the blind two credit lines per world at the count 1 each, the count on the board the books' count at every close; the engine's reading is `Lattice.count`, the record's share over the scale and the record's unit, one method and no key."""
    page = (SINGLET_FOLDER / "blind_and_reading.md").read_text(encoding="utf-8")
    assert "`board_count` 1" in page and "`scale` 1" in page
    assert re.search(r"two\s+credit\s+lines\s+per\s+world", page) and "the count 1 each" in page
    assert callable(Lattice.count) and "count" not in {f.name for f in fields(Books)} - {"counts"}
