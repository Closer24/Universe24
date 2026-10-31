"""Tensor24's decoder, its click-board file: the click board read as the clocks' meetings (FRAMES.md 13b), the meetings,
each clock's line of meetings and light's echo, and the fourth code reader's fold of the click world's four readings,
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
NONE = {
    "kind": "NO CLICK",
    "cause": "the record holds no click line: not in the click world",
}  # the owner's phrase
ECHO = (
    "light's echo is not read: no rule yet tells light's click lines from the others (reading 7, owed)"
)
REFUSAL = "the record holds no click line, so no claim"  # the tool's refusal line, its opening
# a whole click of train 1 at round 1, three windings and one kept laid as four of train 0, and no click line
WHOLE = {"kind": "whole", "round": 1, "site": 0, "count": 1, "train": 1, "ends": []}
WHOLE |= {"taken": [{"train": 1, "windings": [7, 4], "kept": [3, 2]}]}
WHOLE |= {"laid": [{"train": 0, "windings": [0, 4], "kept": [0, 0]}]}


def head(sides=(5, 1, 1), gears=((0, 0, 0, 1, 0, 0),), text=None, name="setting.json"):
    """A 1.3 header: its board's sides, three train cards, and its setting file, laying the gears, by its name."""
    lay = (
        json.dumps({"version": 1, "ticks": 9, "gears": [list(g) for g in gears]})
        if text is None
        else text
    )
    board = {"sides": list(sides)} if sides else {}
    cards = {"kinds": [KIND], "trains": CARDS, "files": [{"name": name, "text": lay}]}
    return {"kind": "header", "record": "tensor24", "major": 1, "minor": schema.MINOR} | board | cards


def click(round_, site, train, q):
    """A click line: at a round and a Node-clock, a train's q, its click tooth before and after within the key."""
    return {"kind": "click", "round": round_, "site": site, "train": train, "q": q, "tooth": [3, 3]}


def read(tmp_path, *lines, header=None):
    """The record of the header (a ring of five, one gear laid at site 0, unless given) and the lines, written and read."""
    path = tmp_path / "record.jsonl"
    path.write_text(
        "".join(json.dumps(e) + "\n" for e in [header or head(), *lines, END]), encoding="utf-8"
    )
    return records.read(str(path))[0]


def tool(tmp_path):
    """The tool's printout of the record written last."""
    run = [sys.executable, "-I", str(TOOL), str(tmp_path / "record.jsonl")]
    return subprocess.run(run, capture_output=True, text=True, check=True).stdout


def test_the_meetings_are_one_give_and_one_take_at_a_place_and_light_is_not_read_by_echo(tmp_path):
    """Yes: a give and a take at each of two places, the meetings SHOWN, light's echo NOT READ. No: q -2 and +2 at a place,
    and +1, +1 and -2, each NOT SHOWN though the books close (the sum alone shows both); a record of no click line
    NO CLICK in each of the seven readings called alone, the owner's phrase whole (echo NO CLICK on lines fails)."""
    yes = read(tmp_path, click(1, 0, 0, -1), click(1, 0, 1, 1), click(2, 0, 1, 1), click(2, 0, 2, -1))
    met = "one give and one take of one quantum at 2 of 2 places: 1 from train 0 to train 1, 1 from train 2 to train 1"
    assert shadow.meetings(yes)["kind"] == "SHOWN" and shadow.meetings(yes)["cause"] == met
    assert shadow.echo(yes) == {"kind": "NOT READ", "cause": ECHO}
    three = [click(1, 0, 0, 1), click(1, 0, 1, 1), click(1, 0, 2, -2)]
    for lines, held in (
        ([click(1, 0, 0, -2), click(1, 0, 1, 2)], "q [-2, 2] of the trains [0, 1]"),
        (three, "q [1, 1, -2] of the trains [0, 1, 2]"),
    ):
        no = read(tmp_path, *lines)
        odd = f"the click lines at round 1, site 0 hold {held}: not one give and one take of one quantum at 1 of 1 places"
        assert shadow.books(no)["kind"] == "SHOWN"
        assert (shadow.meetings(no)["kind"], shadow.meetings(no)["cause"]) == ("NOT SHOWN", odd)
    empty = read(tmp_path)
    readings = [shadow.books, shadow.duration, shadow.twins, shadow.cone]
    for reading in [*readings, shadow.meetings, shadow.clock_lines, shadow.echo]:
        assert reading(empty) == NONE


def test_each_clock_line_counts_its_meetings_with_no_duration_and_its_books_beside_them(tmp_path):
    """Yes: two clocks meeting at rounds 2 and 9, each with its two meetings counted, never the rounds between, two more
    meeting once, the counts from least to most, and the books, in the reading and the tool's line. No: a lone clock of two
    lines, NOT SHOWN, its count 0 (every line counted a meeting shows it, its lines counted as clocks miscount)."""
    lines = [click(2, 0, 0, -1), click(2, 0, 1, 1), click(9, 0, 0, -1), click(9, 0, 1, 1)]
    yes = shadow.clock_lines(read(tmp_path, *lines, click(9, 1, 0, -1), click(9, 1, 1, 1)))
    each = "the 2 of train 0 (a) net -2 to -1 each, the 2 of train 1 (b) net 1 to 2 each"
    shown = f"every click line stands in a meeting: 4 clocks of 1 to 2 meetings each, the order counted, no duration; {each}"
    assert yes["kind"] == "SHOWN" and yes["cause"] == shown
    line = "    clock at site 0, train 1 (b): 2 meetings, the order counted, no duration; given 0, taken 2, net 2"
    assert line in tool(tmp_path).splitlines()
    lone = shadow.clock_lines(read(tmp_path, lines[0], lines[2]))
    one = "the clock at site 0, train 0 clicks at round 2 in no meeting: 1 of 1 clocks click outside one"
    assert (lone["kind"], lone["cause"]) == ("NOT SHOWN", one) and lone["clocks"][(0, 0)][0] == 0


# a ring of seven, gears at sites 2 and 5 (site 5's laid by its tooth alone) and site 6 (all 0, not laid)
SEVEN = head((7, 1, 1), ((0, 0, 2, 1, 0, 0), (1, 0, 5, 0, 0, 3), (0, 0, 6, 0, 0, 0)))


def test_the_cone_reads_the_lines_that_could_stand_outside_it_and_the_setting_by_its_name(tmp_path):
    """No: a ring of seven laid at sites 2 and 5 (site 6's gear all 0), a line one Mesh from site 5 alone and one outside
    both, NOT SHOWN, and a lay of no site; yes, the first line alone, SHOWN; not read: no line could stand outside, at a
    laid site or at or past round 2, the lay's reach, or every site laid; a setting not read, each cause named."""
    far = shadow.cone(read(tmp_path, click(1, 0, 0, -1), click(1, 4, 1, 1), header=SEVEN))
    outside = "the click line at round 1, site 0 stands outside the lay's cone: 1 of the 2 lines that could stand"
    assert (far["kind"], far["cause"]) == ("NOT SHOWN", f"{outside} outside it, of 2 lines")
    near = shadow.cone(read(tmp_path, click(1, 4, 1, 1), header=SEVEN))
    inside = "every click line stands inside the lay's cone, one Mesh a round from the 2 sites laid: 1 of the 1 lines"
    shown = f"{inside} that could stand outside it, of 1 lines"
    assert (near["kind"], near["cause"]) == ("SHOWN", shown)
    bare = shadow.cone(read(tmp_path, click(1, 0, 0, -1), header=head(gears=((0, 0, 0, 0, 0, 0),))))
    alone = "the click line at round 1, site 0 stands outside the lay's cone: 1 of the 1 lines that could stand"
    assert (bare["kind"], bare["cause"]) == ("NOT SHOWN", f"{alone} outside it, of 1 lines")
    one, two = [click(1, 0, 0, -1)], [click(1, 2, 0, -1), click(2, 0, 1, 1)]
    spaced = [click(1, 0, 0, -1), click(2, 1, 1, 1)]
    reach = "round 2, the lay's reach, the most Meshes from a site to its nearest laid site"
    laid = f"every click line stands at a laid site (2 of the board's 7) or at or past {reach}"
    first = "before the first click line at round 1: no line could stand outside it"
    every = f"the lay's cone covers the board's 2 sites from round 0, {first}"
    pair = head((2, 1, 1), ((0, 0, 0, 1, 0, 0), (0, 0, 1, 1, 0, 0)))
    off, below = head(gears=((0, 0, 7, 1, 0, 0),)), head(gears=((0, 0, -3, 1, 0, 0),))
    for header, lines, cause in (
        (SEVEN, two, f"{laid}: no line could stand outside the lay's cone"),
        (pair, spaced, every),
        (head(name="lay.json"), one, "the header holds no setting file setting.json"),
        (head(text="{"), one, "the setting file setting.json is no JSON object"),
        (head(gears=()), one, "the setting file setting.json holds no gears"),
        (off, one, "the setting's gear 1 names site 7, off the board of sides [5, 1, 1]"),
        (below, one, "the setting's gear 1 names site -3, off the board of sides [5, 1, 1]"),
        (head(gears=((0, 0, 0),)), one, "the setting's gear 1 names no site and counts"),
        (head(text="[" * 10**7), one, "the setting file setting.json is no JSON object"),
        (head(sides=()), one, "the header's sides make no board"),
    ):
        verdict = shadow.cone(read(tmp_path, *lines, header=header))
        assert (verdict["kind"], verdict["cause"]) == ("NOT READ", cause)


def test_the_books_read_in_row_15_order_and_the_tool_refuses_only_a_record_of_no_click(tmp_path):
    """No: a give at round 1, its take at round 2, NOT SHOWN at round 1, the trains' tallies (one of no line) in the reading
    and the tool, no refusal line; a lone give before a line with no q and a take, NOT SHOWN with the gap beside it, the
    meetings so; a line with no train first, NOT READ, the tool too. Yes: a whole click, no click line, no refusal line."""
    held = shadow.books(read(tmp_path, click(1, 0, 0, -1), click(2, 0, 1, 1)))
    opened = "the sum of q over the trains is -1 at round 1, site 0: not 0 at 2 of 2 places"
    assert (held["kind"], held["cause"]) == ("NOT SHOWN", opened)
    out = tool(tmp_path)
    assert held["trains"][0] == clicks.Tally(1, 1, 0, -1) and REFUSAL not in out
    assert "    train 0 (a): 1 lines, given 1, taken 0, net -1" in out.splitlines()
    assert "    train 2 (c): 0 lines, given 0, taken 0, net 0" in out.splitlines()
    gap = {key: value for key, value in click(3, 0, 0, -1).items() if key != "q"}
    closed = [click(1, 0, 0, -1), click(1, 0, 1, 1)]
    record = read(tmp_path, *closed, click(2, 0, 0, -1), gap, click(3, 0, 1, 1))
    lacks = "the click line at round 3, site 0 holds no q, which its"
    books = f"the sum of q over the trains is -1 at round 2, site 0: not 0 at 1 of 2 places; {lacks} books are read from"
    assert shadow.books(record)["cause"] == books
    assert shadow.meetings(record)["cause"].endswith(f"at 1 of 2 places; {lacks} meeting is read from")
    trainless = {key: value for key, value in click(1, 0, 0, 1).items() if key != "train"}
    record = read(tmp_path, trainless, click(1, 0, 1, -1), gap)
    unread = (
        "NOT READ",
        "the click line at round 1, site 0 holds no train, which its meeting is read from",
    )
    for reading in (shadow.meetings, shadow.clock_lines):
        assert (reading(record)["kind"], reading(record)["cause"]) == unread
    assert f"  the meetings: {unread[0]}: {unread[1]}" in tool(tmp_path).splitlines()
    assert read(tmp_path, WHOLE, header=head() | {"minor": 1}).of("whole") == [WHOLE]
    out = tool(tmp_path)
    assert "  the books at each click: NO CLICK" in out and REFUSAL not in out
