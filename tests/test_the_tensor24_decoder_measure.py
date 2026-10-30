"""Tensor24's decoder, the measurement's rules (D6 to D8) on records built in memory (N5): the cone check by click,
a duration as a clock's own count, the twin reading and no duration read from the board's tick; each failing on its mutant."""

import json
import subprocess
import sys
from pathlib import Path

from tensor24.decoder import measure, records
from tests import frame as board

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


CONES = [
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
]


CONES_UNREAD = [
    (pairs(LAWFUL), HEAD, "the header's sides make no board"),
    ([e for e in pairs(LAWFUL) if "birth" not in e], BOARD, "no click names its lay (G5)"),
    ([e for e in pairs(LAWFUL) if "axes" not in e], BOARD, "no setting names its lay"),
    (pairs(LAWFUL) + [setting(2, 45, [1, 50], 1 + 1)], BOARD, "draws no frame of its axes"),
    (pairs(LAWFUL) + [{**setting(2, 45, [1, 50], 0), "members": [[1]]}], BOARD, "names no lay"),
    (pairs(LAWFUL) + [{**take(3, 45, [1, 50], Z, PLUS), "written": 0}], BOARD, "writes no line"),
]


def test_the_cone_check_reads_each_click_against_the_frames_drawn_outside_its_past_cone():
    """The cone check: one Mesh a round the shorter way; each click binned by the frames outside its past cone, or not read, named."""
    for rows, far, kind, named in CONES:
        far, unset = far if isinstance(far, tuple) else (far, ())
        found = measure.cone_check(built(pairs(rows, far, unset)))
        assert (found["kind"], named in found["cause"]) == (kind, True), found
    for lines, head, cause in CONES_UNREAD:
        found = measure.cone_check(built(lines, head))
        assert (found["kind"], cause in found["cause"]) == ("NOT READ", True), found
    sides = [3, 4, 5]  # the site (x 4 + y) 5 + z, z the fastest
    near = board.board(tuple(sides))  # the board's own six neighbours: the second reading
    for a in range(near.shape[1]):
        far, ring, step = {a: 0}, [a], 0
        while ring:  # the Meshes from a, one ring of neighbours a step
            step += 1
            ring = [b for b in {int(b) for s in ring for b in near[:, s]} if b not in far]
            far.update(dict.fromkeys(ring, step))
        for b, meshes in far.items():
            assert measure.meshes(sides, a, b) == meshes
            for lag in (meshes - 1, meshes):  # one round short of the cone, and on it
                assert measure.past(sides, (1, a), (1 + lag, b)) == (lag >= meshes)


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


TWINS = [
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
]


def test_a_duration_is_a_clocks_own_count_and_the_twins_count_apart():
    """A duration is a clock's own count between two of its clicks: the twins apart, a board tick refused."""
    for lines, kind, named in TWINS:
        found = measure.twins(built(lines))
        assert (found["kind"], named in found["cause"]) == (kind, True), found
    clocked, _ = measure.faces(built(GROUND + HOME + TRIP))
    first, later, start = HOME[0], HOME[1 + 1], TRIP[0]
    counted = later["tooth"][1] - first["tooth"][1]  # the clock's own teeth between its two clicks
    here, there = (first["round"], first["site"]), (later["round"], later["site"])
    assert measure.elapsed(clocked, A, here, there) == counted
    elsewhere = (TRIP[1 + 1]["round"], start["site"])  # a place B's clock does not stand at that round
    assert (
        measure.elapsed(clocked, B, (start["round"], start["site"]), elsewhere)
        == measure.NO_READING
        == "compares board ticks, no reading"
    )


def test_the_ledger_and_the_tool_hold_the_measurements_rules(tmp_path):
    """The ledger's lines stand once at each place, and the tool prints the measurements' rules."""
    path = tmp_path / "measure.jsonl"
    record = built(pairs(LAWFUL) + GROUND + HOME + TRIP)
    lines = [record.header, *record.events, record.end]
    path.write_text("".join(json.dumps(e) + "\n" for e in lines), encoding="utf-8")
    found = subprocess.run(
        [sys.executable, "-I", str(TOOL), str(path)], capture_output=True, text=True, check=True
    )
    for rule in ("the cone check (D8)", "the twin reading (D6)"):
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
