"""Tensor24's decoder, the measurement's rules (D6 to D8) on records built in memory (N5): the cone check by click,
proper time read twice, the twin reading and no duration read from the board's tick; each failing on its mutant."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tensor24.decoder import measure, records

TOOL = Path(__file__).resolve().parent.parent / "tools" / "tensor24_decode.py"
HEAD = {"kind": "header", "record": "tensor24", "major": 1, "minor": 1, "engine": "built in memory"}
BOARD = {**HEAD, "sides": [1, 1, 256]}
Z, X = {"rho": 1, "spin": [0, 0, 1]}, {"rho": 1, "spin": [1, 0, 0]}
PLUS, MINUS, REFUSED, ELSEWHERE = "+", "-", "refused", "taken at site 152"


def built(lines, head=BOARD):
    """A record of the lines in the schema's order, its end after the last round."""
    events = sorted(lines, key=records.place)
    return records.Record(head, events, {"kind": "end", "rounds": events[-1]["round"] if events else 1})


def take(round_, site, lay, frame, outcome):
    """A take naming its lay: the frame its setting set, and its line written, + along it or - against it."""
    written = frame if outcome == PLUS else {**frame, "spin": [-s for s in frame["spin"]]}
    line = {"kind": "whole", "round": round_, "site": site, "count": round_, "train": 0, "q": 1}
    return line | {"birth": lay, "detector": frame, "written": written}


def setting(round_, site, lay, drawn, axes=(Z, X)):
    """A setting naming its lay's part 0: the frames it draws among and the one drawn."""
    line = {"kind": "split", "round": round_, "site": site, "count": round_, "train": 0}
    return line | {"members": [[*lay, 0]], "axes": list(axes), "drawn": drawn}


def pairs(rows, far=100, unset=()):
    """One pair laid at site 50 per row, rows apart: the near setting at +4 (site 45) drawing the row's frame, the near
    take at +5, the far setting at +99 (site 150; none for the rows unset) and the far click at +far there (or at site
    152), the row's outcome."""
    lines = []
    for n, (frame, outcome) in enumerate(rows):
        lay = [1 + 300 * n, 50]
        lines += [{"kind": "whole", "round": lay[0], "site": 50, "count": lay[0], "train": 0, "q": 1}]
        lines += [setting(lay[0] + 4, 45, lay, frame), take(lay[0] + 5, 45, lay, (Z, X)[frame], PLUS)]
        lines += [] if n in unset else [setting(lay[0] + 99, 150, lay, 0)]
        books = {
            "kind": "books",
            "round": lay[0] + far,
            "site": 150,
            "train": 0,
            "kept": 1,
            "birth": lay,
        }
        far_take = take(lay[0] + far, 152 if outcome == ELSEWHERE else 150, lay, Z, outcome)
        lines.append(books if outcome == REFUSED else far_take)
    return lines


LAWFUL = [(0, PLUS), (0, MINUS), (1, PLUS), (1, MINUS)]
SIGNALLING = [(0, PLUS), (0, PLUS), (1, PLUS), (1, MINUS)]


@pytest.mark.parametrize(
    ("rows", "far", "kind", "named"),
    [
        (LAWFUL, 100, "SHOWN", "every click's law is the same"),
        (LAWFUL + [(0, PLUS), (0, MINUS)], (100, (4, 5)), "SHOWN", "the lays: 6"),
        (SIGNALLING, 100, "NOT SHOWN", "at round +100, site 150 reads 0 of 2"),
        (
            [(0, REFUSED), (0, PLUS), (1, PLUS), (1, REFUSED)],
            100,
            "SHOWN",
            "compared: 1; the lays: 4",
        ),
        ([(0, REFUSED), (0, REFUSED), (1, PLUS), (1, PLUS)], 100, "NOT SHOWN", "('refused',)"),
        (
            [(0, ELSEWHERE), (0, PLUS), (1, PLUS), (1, ELSEWHERE)],
            100,
            "SHOWN",
            "compared: 2; the lays: 4",
        ),
        ([(0, PLUS), (0, PLUS), (1, PLUS), (1, ELSEWHERE)], 100, "NOT SHOWN", "('none',)"),
        (LAWFUL + [(1, PLUS), (1, MINUS)], 100, "SHOWN", "the lays: 6"),
        (SIGNALLING, 200, "NOT READ", "no setting outside a click's past cone drew two frames"),
    ],
)
def test_the_cone_check_bins_each_click_by_the_frames_drawn_outside_its_past_cone(
    rows, far, kind, named
):
    far, unset = far if isinstance(far, tuple) else (far, ())
    found = measure.cone_check(built(pairs(rows, far, unset)))
    assert (found["kind"], named in found["cause"]) == (kind, True), found


@pytest.mark.parametrize(
    ("lines", "head", "cause"),
    [
        (pairs(LAWFUL), HEAD, "the header's sides make no board"),
        ([e for e in pairs(LAWFUL) if "birth" not in e], BOARD, "no click names its lay (G5)"),
        ([e for e in pairs(LAWFUL) if "axes" not in e], BOARD, "no setting names its lay"),
        (pairs(LAWFUL) + [setting(2, 45, [1, 50], 1 + 1)], BOARD, "draws no frame of its axes"),
        (pairs(LAWFUL) + [{**setting(2, 45, [1, 50], 0), "members": [[1]]}], BOARD, "names no lay"),
        (pairs(LAWFUL) + [{**take(3, 45, [1, 50], Z, PLUS), "written": 0}], BOARD, "writes no line"),
    ],
)
def test_the_cone_check_names_what_it_cannot_read(lines, head, cause):
    found = measure.cone_check(built(lines, head))
    assert (found["kind"], cause in found["cause"]) == ("NOT READ", True), found


def test_the_cone_is_one_mesh_a_round_the_shorter_way_round_each_side():
    sides = [3, 4, 5]  # the site (x 4 + y) 5 + z, z the fastest

    def site(x, y, z):
        return (x * 4 + y) * 5 + z

    assert measure.meshes(sides, site(0, 0, 0), site(2, 0, 0)) == 1
    assert measure.meshes(sides, site(0, 0, 0), site(0, 3, 4)) == 1 + 1
    assert measure.meshes(sides, site(1, 1, 1), site(1, 1, 3)) == 1 + 1
    assert measure.past(sides, (1, site(0, 0, 0)), (3, site(0, 3, 4)))  # on the cone: inside
    assert not measure.past(sides, (1, site(0, 0, 0)), (2, site(0, 3, 4)))


def rate(site, ks):
    """A Node-clock beating once a round from round 1: its rate lines, its k at the first beat and at each change."""
    lines = []
    for count, k in enumerate(ks, start=1):
        if not lines or lines[-1]["k"] != k:
            lines.append(
                {"kind": "rate", "round": count, "site": site, "count": count, "dial": 0, "k": k}
            )
    return lines


def tick(clock, round_, site, tooth):
    """A clock's whole click: the lay that made it, and its face's teeth from that lay, before and after."""
    line = {"kind": "whole", "round": round_, "site": site, "count": round_, "train": 0, "q": 1}
    return line | {"clock": list(clock), "tooth": [tooth - 1, tooth]}


A, B = (1, 5), (2, 5)  # two clocks laid at site 5, at rounds 1 and 2
# site 5 ticks at half the full rate, site 9 at the full rate; each clock counts 3 a tick of its Node-clock
GROUND = rate(5, [1, 0] * 50) + rate(9, [1] * 100)
HOME = [tick(A, 10, 5, 15), tick(A, 30, 5, 45), tick(A, 50, 5, 75), tick(A, 90, 5, 135)]
TRIP = [tick(B, 10, 5, 15), tick(B, 20, 9, 30), tick(B, 30, 9, 60), tick(B, 50, 5, 120)]


@pytest.mark.parametrize(
    ("lines", "kind", "named"),
    [
        (GROUND + HOME + TRIP, "SHOWN", "(the clocks: 2; the pairs of clicks: 4)"),
        (
            GROUND + HOME[:2] + [tick(A, 50, 5, 70)] + TRIP,
            "NOT SHOWN",
            "30 over 10 ticks between rounds 10 and 30",
        ),
        (
            GROUND + [{k: v for k, v in e.items() if k != "clock"} for e in HOME],
            "NOT READ",
            "names its clock",
        ),
        (
            GROUND + TRIP[1:3] + [tick(A, 20, 5, 9), tick(A, 30, 9, 18)],
            "SHOWN",
            "(the clocks: 1; the pairs of clicks: 1)",
        ),
        (
            GROUND + [tick(A, 10, 5, 15), tick(A, 30, 9, 75)],
            "NOT READ",
            "two sites is not on the record",
        ),
        (rate(9, [1] * 100) + HOME, "NOT READ", "the rate lines of site 5"),
        (GROUND + HOME + [{**TRIP[0], "tooth": 7}], "NOT READ", "reads no clock, face or count"),
        (GROUND + HOME + [{**TRIP[0], "clock": [2, 5, 0]}], "NOT READ", "reads no clock, face or count"),
    ],
)
def test_proper_time_is_read_twice_and_agrees_through_one_beat(lines, kind, named):
    found = measure.proper(built(lines))
    assert (found["kind"], named in found["cause"]) == (kind, True), found


@pytest.mark.parametrize(
    ("lines", "kind", "named"),
    [
        (GROUND + HOME + TRIP, "SHOWN", "count apart (compared: 1)"),
        (GROUND + HOME + TRIP[:-1] + [tick(B, 50, 5, 75)], "NOT SHOWN", "count 60 each"),
        (
            GROUND + HOME + [tick(B, 10, 5, 15), tick(B, 20, 5, 30), tick(B, 50, 5, 75)],
            "NOT READ",
            "two paths",
        ),
        (
            GROUND + [HOME[0], HOME[2]] + TRIP,
            "NOT READ",
            "meet twice by two paths",
        ),  # A's path between unread
    ],
)
def test_the_twins_count_apart_where_their_paths_differ(lines, kind, named):
    found = measure.twins(built(lines))
    assert (found["kind"], named in found["cause"]) == (kind, True), found


def test_a_duration_is_a_clocks_own_count_and_a_board_tick_is_refused_by_name():
    clocked, _ = measure.faces(built(GROUND + HOME + TRIP))
    assert measure.elapsed(clocked, A, (10, 5), (50, 5)) == 60
    assert (
        measure.elapsed(clocked, B, (10, 5), (30, 5))
        == measure.NO_READING
        == "compares board ticks, no reading"
    )


def test_the_tool_prints_the_measurements_rules(tmp_path):
    path = tmp_path / "measure.jsonl"
    record = built(pairs(LAWFUL) + GROUND + HOME + TRIP)
    lines = [record.header, *record.events, record.end]
    path.write_text("".join(json.dumps(e) + "\n" for e in lines), encoding="utf-8")
    found = subprocess.run(
        [sys.executable, "-I", str(TOOL), str(path)], capture_output=True, text=True, check=True
    )
    for rule in ("the cone check (D8)", "proper time (D6)", "the twin reading (D6)"):
        assert f"{rule}: {{'kind': 'SHOWN'" in found.stdout
    broken = tmp_path / "measure.ledger.jsonl"
    broken.write_text("no ledger\n", encoding="utf-8")
    found = subprocess.run(
        [sys.executable, "-I", str(TOOL), str(path), str(broken)], capture_output=True, text=True
    )
    assert (
        "the ledger: the ledger is absent" not in found.stdout
        and "the ledger: the ledger's line 1 " in found.stdout
    )


def test_the_ledgers_count_lines_stand_once_at_each_round_site_and_train(tmp_path):
    count = {"round": 1, "at": "step", "site": 0, "train": 1, "count": [0]}
    for lines, cause in (
        ([count, {**count, "site": 1}], ""),
        ([count, count], "the site and the train of an earlier"),
    ):
        path = tmp_path / "count.ledger.jsonl"
        path.write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
        assert cause in records.read_ledger(str(path))[1] and (
            cause or not records.read_ledger(str(path))[1]
        )
