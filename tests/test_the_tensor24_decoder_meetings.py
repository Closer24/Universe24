"""Tensor24's decoder, its click-board file: the click board read as the clocks' meetings (FRAMES.md 13b), the meetings,
and each clock's line of meetings, and the fourth code reader's fold of the click world's readings,
each with its yes, its no and the mutant it catches."""

import json
import subprocess
import sys
from pathlib import Path

from tensor24.decoder import clicks, records, shadow
from tensor24.record import schema

TOOL = Path(__file__).resolve().parent.parent / "tools" / "tensor24_decode.py"
KIND = {"index": 0, "label": "A1", "dimension": 1, "characters": [1] * 24}  # its trace on each of the 24
CARD = {"kinds": [0], "part": 1, "winding": 1, "key": 7, "square": 0}
CARDS = [{"index": t, "label": label, **CARD} for t, label in enumerate("abc")]
END = {"kind": "end", "rounds": 9, "undone": 0, "exact": 1}
# the owner's phrase
NONE = {"kind": "NO CLICK", "cause": "the record holds no click line: not in the click world"}
REFUSAL = "the record holds no click line, so no claim"  # the tool's refusal line, its opening


def head(sides=(5, 1, 1), gears=((0, 0, 0, 1, 0, 0),), text=None, name="setting.json"):
    """A header: its board's sides, three train cards at the key 7, and its setting file, laying the gears, by its name."""
    held = {"version": 1, "ticks": 9, "gears": [list(g) for g in gears]}
    lay = json.dumps(held) if text is None else text
    board = {"sides": list(sides)} if sides else {}
    cards = {"kinds": [KIND], "trains": CARDS, "files": [{"name": name, "text": lay}]}
    return {"kind": "header", "record": "tensor24", "version": schema.VERSION} | board | cards


def edges(round_, site, *passed):
    """The click lines of a place whose edges passed quanta, (giver, taker, quanta) each: every train's line a side per
    edge it stands on, [the other train, its q, tooth before, after], its q their sum, every tooth 3 at the key 7."""
    at: dict[int, list[list[int]]] = {}
    for giver, taker, n in passed:
        at.setdefault(giver, []).append([taker, -n, 3, 3])
        at.setdefault(taker, []).append([giver, n, 3, 3])
    line = dict(kind="click", round=round_, site=site)
    return [dict(line, train=t, q=sum(s[1] for s in z), sides=sorted(z)) for t, z in sorted(at.items())]


def across(round_, give, take):
    """A quantum passed across a Mesh at a round, from a clock (site, train) to another, each line its side across."""
    (s, t), (z, u) = give, take
    line = dict(kind="click", round=round_, site=s, train=t, q=-1, sides=[], across=[[u, z, -1, 3, 3]])
    far = {**line, "site": z, "train": u, "q": 1, "across": [[t, s, 1, 3, 3]]}
    return sorted([line, far], key=lambda e: e["site"])


# every guard but the sides' (sides.paired, last), which refuses a side with no partner
LOOSE = records.GUARDS[:-1]


def read(tmp_path, *lines, header=None, guards=records.GUARDS):
    """The record of the header (a ring of five, one gear laid at site 0, unless given) and the lines, written and read."""
    path = tmp_path / "record.jsonl"
    path.write_text(
        "".join(json.dumps(e) + "\n" for e in [header or head(), *lines, END]), encoding="utf-8"
    )
    return records.read(str(path), guards)[0]


def tool(tmp_path):
    """The tool's printout of the record written last."""
    run = [sys.executable, "-I", str(TOOL), str(tmp_path / "record.jsonl")]
    return subprocess.run(run, capture_output=True, text=True, check=True).stdout


def test_the_meetings_are_one_give_and_one_take_at_a_place(tmp_path):
    """Yes: a give and a take at each of two places, the meetings SHOWN. No: q -2 and +2 at a place, and +1, +1 and -2,
    each NOT SHOWN though the books close (the sum alone shows both); a record of no click line NO CLICK in each of the
    four readings called alone, the owner's phrase whole."""
    yes = read(tmp_path, *edges(1, 0, (0, 1, 1)), *edges(1 + 1, 0, (1 + 1, 1, 1)))
    met = "one give and one take of one quantum at 2 of 2 places: 1 from train 0 to train 1, 1 from train 2 to train 1"
    assert shadow.meetings(yes)["kind"] == "SHOWN" and shadow.meetings(yes)["cause"] == met
    three = edges(1, 0, (1 + 1, 0, 1), (1 + 1, 1, 1))
    for lines, held in (
        (edges(1, 0, (0, 1, 1 + 1)), "q [-2, 2] of the trains [0, 1]"),
        (three, "q [1, 1, -2] of the trains [0, 1, 2]"),
    ):
        no = read(tmp_path, *lines)
        odd = f"the click lines at round 1, site 0 hold {held}: not one give and one take of one quantum at 1 of 1 places"
        assert shadow.books(no)["kind"] == "SHOWN"
        assert (shadow.meetings(no)["kind"], shadow.meetings(no)["cause"]) == ("NOT SHOWN", odd)
    empty = read(tmp_path)
    for reading in (shadow.books, shadow.cone, shadow.meetings, shadow.clock_lines):
        assert reading(empty) == NONE


def test_each_clock_line_counts_its_meetings_with_no_duration_and_its_books_beside_them(tmp_path):
    """Yes: two clocks meeting at rounds 2 and 9, each with its two meetings counted, never the rounds between, two more
    meeting once, the counts from least to most, and the books, in the reading and the tool's line. No: two clocks passing
    two quanta at rounds 2 and 9, NOT SHOWN, each count 0 (every line counted a meeting shows it)."""
    lines = [*edges(1 + 1, 0, (0, 1, 1)), *edges(9, 0, (0, 1, 1))]
    yes = shadow.clock_lines(read(tmp_path, *lines, *edges(9, 1, (0, 1, 1))))
    each = "the 2 of train 0 (a) net -2 to -1 each, the 2 of train 1 (b) net 1 to 2 each"
    shown = f"every click line stands in a meeting: 4 clocks of 1 to 2 meetings each, the order counted, no duration; {each}"
    assert yes["kind"] == "SHOWN" and yes["cause"] == shown
    line = "    clock at site 0, train 1 (b): 2 meetings, the order counted, no duration; given 0, taken 2, net 2"
    assert line in tool(tmp_path).splitlines()
    two = [*edges(1 + 1, 0, (0, 1, 1 + 1)), *edges(9, 0, (0, 1, 1 + 1))]
    lone = shadow.clock_lines(read(tmp_path, *two))
    one = "the clock at site 0, train 0 clicks at round 2 in no meeting: 2 of 2 clocks click outside one"
    assert (lone["kind"], lone["cause"]) == ("NOT SHOWN", one) and lone["clocks"][(0, 0)][0] == 0


def test_a_meeting_is_an_edge_side_and_its_mirror_the_silent_clock_aside(tmp_path):
    """Yes: one quantum on the edge 0-1, train 2 listed at q 0: met, each clock's line met, the sides printed. No: a clock
    at q 0 on two edges; q -1 and +1 at two places, each beside sides across a Mesh (the q's alone would meet them)."""
    record = read(tmp_path, *edges(1, 0, (0, 1, 1), (0, 1 + 1, 0), (1, 1 + 1, 0)))
    assert [shadow.meetings(record)[k] for k in ("kind", "ways")] == ["SHOWN", {(0, 1): 1}]
    lines = shadow.clock_lines(record)
    assert lines["kind"] == "SHOWN" and sorted(lines["clocks"]) == [(0, 0), (0, 1)]
    assert "train 2: q 0, sides [[0, 0, 3, 3], [1, 0, 3, 3]], across []" in tool(tmp_path)
    give, take = edges(1, 0, (0, 1, 1 + 1))
    near = [give | {"q": -1, "across": [[0, 1, 1, 3, 3]]}, take | {"q": 1, "across": [[1, 1, -1, 3, 3]]}]
    far = across(1, (1, 0), (0, 0))[1], across(1, (0, 1), (1, 1))[1]  # each pair's line at site 1
    for held, n in (edges(1, 0, (0, 1 + 1, 1), (1 + 1, 1, 1), (0, 1, 0)), 1), ([*near, *far], 1 + 1):
        verdict, lines = shadow.meetings(record := read(tmp_path, *held)), shadow.clock_lines(record)
        assert verdict["cause"].endswith(f"at {n} of {n} places") and len(lines["clocks"]) == len(held)


# a ring of seven, gears at sites 2 and 5 (site 5's laid by its tooth alone) and site 6 (all 0, not laid)
SEVEN = head((7, 1, 1), ((0, 0, 2, 1, 0, 0), (1, 0, 5, 0, 0, 3), (0, 0, 6, 0, 0, 0)))


def test_the_cone_reads_the_lines_that_could_stand_outside_it_and_the_setting_by_its_place(tmp_path):
    """No: a ring of seven laid at sites 2 and 5 (site 6's gear all 0), a line one Mesh from site 5 alone and one outside
    both, NOT SHOWN, and a lay of no site; yes, the first line alone, SHOWN, the setting read by its place whatever its
    name (AUDIT2's A8); not read: no line could stand outside, at a laid site, past the lay's reach or every site laid."""
    apart, files = across(1, (0, 0), (4, 1)), [{**SEVEN["files"][0], "name": "w.1.json"}]  # another name
    far = shadow.cone(read(tmp_path, *apart, header=SEVEN))
    assert shadow.cone(read(tmp_path, *apart, header={**SEVEN, "files": files})) == far
    outside = "the click line at round 1, site 0 stands outside the lay's cone: 1 of the 2 lines that could stand"
    assert (far["kind"], far["cause"]) == ("NOT SHOWN", f"{outside} outside it, of 2 lines")
    near = shadow.cone(read(tmp_path, *edges(1, 4, (0, 1, 1)), header=SEVEN))
    shown = "every click line stands inside the lay's cone, one Mesh a round from the 2 sites laid: 2 of the 2 lines that could stand outside it, of 2 lines"
    assert (near["kind"], near["cause"]) == ("SHOWN", shown)
    bare = shadow.cone(read(tmp_path, *edges(1, 0, (0, 1, 1)), header=head(gears=((0, 0, 0, 0, 0, 0),))))
    alone = "the click line at round 1, site 0 stands outside the lay's cone: 2 of the 2 lines that could stand"
    assert (bare["kind"], bare["cause"]) == ("NOT SHOWN", f"{alone} outside it, of 2 lines")
    one, two = edges(1, 0, (0, 1, 1)), [*edges(1, 1 + 1, (0, 1, 1)), *edges(1 + 1, 0, (0, 1, 1))]
    spaced = [*edges(1, 0, (0, 1, 1)), *edges(1 + 1, 1, (0, 1, 1))]
    laid = "every click line stands at a laid site (2 of the board's 7) or at or past round 2, the lay's reach, the most Meshes from a site to its nearest laid site"
    every = "the lay's cone covers the board's 2 sites from round 0, before the first click line at round 1: no line could stand outside it"
    pair = head((2, 1, 1), ((0, 0, 0, 1, 0, 0), (0, 0, 1, 1, 0, 0)))
    off, below = head(gears=((0, 0, 7, 1, 0, 0),)), head(gears=((0, 0, -3, 1, 0, 0),))
    for header, lines, cause in (
        (SEVEN, two, f"{laid}: no line could stand outside the lay's cone"),
        (pair, spaced, every),
        ({**head(), "files": []}, one, "the header holds no files"),
        (head(text="{"), one, "the setting file is no JSON object"),
        (head(gears=()), one, "the setting file holds no gears"),
        (off, one, "the setting's gear 1 names site 7, off the board of sides [5, 1, 1]"),
        (below, one, "the setting's gear 1 names site -3, off the board of sides [5, 1, 1]"),
        (head(gears=((0, 0, 0),)), one, "the setting's gear 1 names no site and counts"),
        (head(text="[" * 10**7), one, "the setting file is no JSON object"),
        (head(sides=()), one, "the header's sides make no board"),
    ):
        verdict = shadow.cone(read(tmp_path, *lines, header=header))
        assert (verdict["kind"], verdict["cause"]) == ("NOT READ", cause)


def test_the_books_read_in_row_15_order_and_the_tool_refuses_only_a_record_of_no_click(tmp_path):
    """Yes: a meeting, the books SHOWN, the trains' tallies (one of no line) in the reading and the tool, no refusal line.
    No: a give at round 1 and its take at round 2, refused at read for the absent partner and, read without the sides'
    guard, NOT SHOWN at round 1, row 15's first, the gap of no q beside it, the meetings so; no train first, NOT READ."""
    shown = shadow.books(read(tmp_path, *edges(1, 0, (0, 1, 1))))
    out = tool(tmp_path)
    assert shown["kind"] == "SHOWN" and shown["trains"][0] == clicks.Tally(1, 1, 0, -1)
    assert REFUSAL not in out
    assert "    train 0 (a): 1 lines, given 1, taken 0, net -1" in out.splitlines()
    assert "    train 2 (c): 0 lines, given 0, taken 0, net 0" in out.splitlines()
    apart = [edges(1, 0, (0, 1, 1))[0], edges(1 + 1, 0, (0, 1, 1))[1]]  # a give, its take a round later
    assert read(tmp_path, *apart) is None and REFUSAL not in tool(tmp_path)
    held = shadow.books(read(tmp_path, *apart, guards=LOOSE))
    opened = "the sum of q over the trains is -1 at round 1, site 0: not 0 at 2 of 2 places"
    assert (held["kind"], held["cause"]) == ("NOT SHOWN", opened)
    gap = {key: value for key, value in edges(3, 0, (0, 1, 1))[0].items() if key != "q"}
    lone = edges(1 + 1, 0, (0, 1, 1))[0]
    record = read(tmp_path, *edges(1, 0, (0, 1, 1)), lone, gap, edges(3, 0, (0, 1, 1))[1], guards=LOOSE)
    lacks = "the click line at round 3, site 0 holds no q, which its"
    books = f"the sum of q over the trains is -1 at round 2, site 0: not 0 at 1 of 2 places; {lacks} books are read from"
    assert shadow.books(record)["cause"] == books
    assert shadow.meetings(record)["cause"].endswith(f"at 1 of 2 places; {lacks} meeting is read from")
    bare = {"kind": "click", "round": 1, "site": 0, "q": 1}  # lines of no side, which no guard pairs
    gap = {"kind": "click", "round": 3, "site": 0, "train": 0}
    record = read(tmp_path, bare, {**bare, "train": 1, "q": -1}, gap)
    trainless = "the click line at round 1, site 0 holds no train, which its meeting is read from"
    unread = "NOT READ", trainless
    for reading in (shadow.meetings, shadow.clock_lines):
        assert (reading(record)["kind"], reading(record)["cause"]) == unread
    assert f"  the meetings: {unread[0]}: {unread[1]}" in tool(tmp_path).splitlines()
