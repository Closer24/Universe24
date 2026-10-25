"""The legend of kinds and the per-bang ledger on both pages (tools/look/captions.py legend_of, ledger_of, legend_html; the owner's word of 2026-10-24, 08:0x UTC: one sees everything from the run with labels of what one sees, black holes, electrons, protons, bound bodies, everything; in every bang there must be more things): on the record of 2,400 intervals (examples/events/universe24, the three logs) the legend lists every kind the law can show with its count read from the logs alone, zeros with their cause, and the ledger one row per bang; both pages carry the two blocks as HTML rows; a log cut mid-run (its last line half written) is read to the last whole line, the last cycle open. The test runs in 3 s (2026-10-24, the three tests 2.3 s together)."""

import json
from html.parser import HTMLParser
from pathlib import Path

from tests.laws import ROOT, load_file

CAPTIONS = load_file("captions_for_the_legend", ROOT / "tools" / "look" / "captions.py")
ERAS_PAGE = load_file("eras_page_for_the_legend", ROOT / "tools" / "look" / "eras_page.py")
TORUS = load_file("torus_page_for_the_legend", ROOT / "tools" / "look" / "torus_page.py")
RECORD = ROOT / "examples" / "events" / "universe24"


class Tables(HTMLParser):
    """The rows of the page's tables by the table's id, each row its cells' text."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: dict[str, list[list[str]]] = {}
        self.table: str | None = None
        self.cells: list[str] | None = None
        self.cell: str | None = None
        self.finding: str | None = None
        self.in_finding = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        found = dict(attrs)
        if tag == "table":
            self.table = found.get("id")
        if tag == "tr" and self.table:
            self.cells = []
        if tag in ("td", "th") and self.cells is not None:
            self.cell = ""
        if found.get("id") == "ledger-finding":
            self.in_finding, self.finding = True, ""

    def handle_data(self, data: str) -> None:
        if self.cell is not None:
            self.cell += data
        if self.in_finding and self.finding is not None:
            self.finding += data

    def handle_endtag(self, tag: str) -> None:
        if tag in ("td", "th") and self.cells is not None and self.cell is not None:
            self.cells.append(self.cell)
            self.cell = None
        if tag == "tr" and self.cells is not None and self.table:
            self.rows.setdefault(self.table, []).append(self.cells)
            self.cells = None
        if tag == "table":
            self.table = None
        if tag == "p" and self.in_finding:
            self.in_finding = False


def tables_of(html: str) -> Tables:
    parsed = Tables()
    parsed.feed(html)
    return parsed


def logs() -> tuple[list[dict], list[dict], list[dict]]:
    read = lambda kind: CAPTIONS.parse_log((RECORD / f"universe24.{kind}.jsonl").read_text())  # noqa: E731
    return read("eras"), read("nodes"), read("clicks")


def test_the_legend_counts_every_kind_from_the_record_and_the_ledger_shows_nothing_new_after_bang_1():
    """(1) The record's legend: 8 bangs, 8 tops, 0 black holes, 0 turns at the floor, 1,000 Node turns, 125 proton pairs at 29 at 125 Nodes, 0 electron and 0 matter pairs with the cause, 0 conversions, 125 clicks counted whole, 375 lays, the proton standing 4 per Node at 2,400, light 0 from 29, bound bodies not readable; (2) the ledger: 8 rows, 125 proton pairs in the first, 0 births in every row after, the finding sentence."""
    eras, nodes, clicks = logs()
    floor = ERAS_PAGE.least_of(nodes, eras[0]["node_clock"])["floor"]
    legend = CAPTIONS.legend_of(eras, nodes, clicks, floor)
    assert legend["reached"] == 2400 and legend["declared"] == 2400
    rows = {row["kind"]: row for row in legend["rows"]}
    counts = {kind: row["count"] for kind, row in rows.items()}
    assert counts == {
        "bangs": 8,
        "tops": 8,
        "black holes": 0,
        "turns at the floor (the crunch)": 0,
        "Node turns (the swap at the top)": 1000,
        "matter pairs born": 0,
        "proton pairs born": 125,
        "electron pairs born": 0,
        "conversions": 0,
        "clicks": 125,
        "lays (the records laid)": 375,
        "standing matter": 0,
        "standing light (the seed family: light left)": 0,
        "standing proton": 500,
        "standing electron": 0,
        "standing charge (a holder, beside the families of quanta: the held row writes none of it)": 2875,
        "bound bodies": None,
    }
    assert rows["bangs"]["words"] == "at 1, 311, 615, 925, 1,229, 1,539, 1,843, 2,153"
    assert rows["tops"]["words"].startswith("156 at the volume 1,465,500; 463 at the volume 1,382,625")
    assert (
        rows["black holes"]["words"]
        == "0 in this run: the eras log's horizon 0 at every interval to 2,400"
    )
    assert rows["turns at the floor (the crunch)"]["words"] == (
        "0 Node turns at or under the floor 19; the least X over the run 1,003"
    )
    assert rows["proton pairs born"]["words"] == (
        "125 pairs at 29, at 125 Nodes, the senses [-1, 1] (matter and antimatter)"
    )
    assert rows["electron pairs born"]["words"].startswith(
        "none born: every birth line's children are proton and proton, the heaviest pair within the two meeting quanta's energy"
    )
    assert rows["clicks"]["words"].startswith("125 at 29, 125 the board's own")
    assert rows["clicks"]["words"].endswith("every click counted whole, no part drawn")
    assert rows["standing proton"]["words"] == (
        "500 quanta, 4 per Node, at 125 Nodes at 2,400, standing since 29 (carried through every top)"
    )
    assert (
        rows["standing light (the seed family: light left)"]["words"]
        == "0 from 29: standing from 1, spent at the holes"
    )
    assert rows["bound bodies"]["words"].startswith("not readable from the logs")
    assert all(row["law"] for row in legend["rows"])  # every kind named in the law by one clause
    ledger = CAPTIONS.ledger_of(eras, nodes, clicks)
    cycles = ledger["rows"]
    assert [(c["bang"], c["at"], c["to"], c["top"], c["volume"]) for c in cycles[:3]] == [
        (1, 1, 310, 156, 1465500),
        (2, 311, 614, 463, 1382625),
        (3, 615, 924, 770, 1465500),
    ]
    assert len(cycles) == 8 and cycles[-1]["open"] and cycles[-1]["to"] == 2400
    assert cycles[0]["births"] == {"matter": 0, "proton": 125, "electron": 0}
    assert all(sum(c["births"].values()) == 0 for c in cycles[1:])
    assert all(c["light"] == 0 and c["horizon"] == 0 and c["turns"] == 125 for c in cycles)
    assert [c["standing"]["proton"] for c in cycles[:2]] == [
        "1,125 quanta, 9 per Node, at 125 Nodes",
        "1,000 quanta, 8 per Node, at 125 Nodes",
    ]
    assert ledger["finding"].startswith(
        "The logs show nothing new after bang 1: 7 cycles after the first with 0 births each, the first cycle's births 125 proton pairs, the light spent at 29"
    )


def test_both_pages_carry_the_legend_and_the_ledger_as_rows():
    """The eras page and the torus page of the record hold the legend's table (one row per kind, the count and the reading in its cells) and the ledger's table (one row per bang) with the finding sentence; the HTML parses."""
    eras, nodes, clicks = logs()
    floor = ERAS_PAGE.least_of(nodes, eras[0]["node_clock"])["floor"]
    legend, ledger = (
        CAPTIONS.legend_of(eras, nodes, clicks, floor),
        CAPTIONS.ledger_of(eras, nodes, clicks),
    )
    block = CAPTIONS.legend_html(legend, ledger)
    pages = [
        ERAS_PAGE.page(
            eras,
            None,
            None,
            50,
            "",
            clicks,
            ERAS_PAGE.least_of(nodes, eras[0]["node_clock"]),
            None,
            block,
        ),
        TORUS.page(nodes, eras, clicks, json.loads((RECORD / "universe24.json").read_text()), None),
    ]
    for html in pages:
        parsed = tables_of(html)
        kinds = parsed.rows["kinds"]
        assert kinds[0] == ["kind (the viewer's name)", "in the law", "count", "read from the logs"]
        assert [row[0] for row in kinds[1:]] == [row["kind"] for row in legend["rows"]]
        assert [row[2] for row in kinds[1:]] == [
            "not readable" if row["count"] is None else f"{row['count']:,}" for row in legend["rows"]
        ]
        assert [row[3] for row in kinds[1:]] == [row["words"] for row in legend["rows"]]
        cycles = parsed.rows["ledger"]
        assert len(cycles) == 9 and cycles[1][:5] == [
            "1",
            "1",
            "310",
            "156 at the volume 1,465,500",
            "0 matter pairs; 125 proton pairs; 0 electron pairs",
        ]
        assert (
            cycles[8][2] == "2,400 (the log's last interval)"
            and cycles[8][4] == "0 matter pairs; 0 proton pairs; 0 electron pairs"
        )
        assert parsed.finding == ledger["finding"]
        assert "to the interval 2,400 of 2,400 declared" in html


def test_a_log_cut_mid_run_is_read_to_its_last_whole_line(tmp_path: Path) -> None:
    """The record's logs cut after the interval 400 with the next line half written (a run in progress read at the moment of the cut): both tools build their pages, the legend reads to 400 of 2,400 declared, the ledger two rows, bang 2 at 311 open to the log's last interval with no top reached."""
    for kind, keep in (("eras", 401), ("nodes", 400)):
        lines = (RECORD / f"universe24.{kind}.jsonl").read_text().splitlines()
        (tmp_path / f"cut.{kind}.jsonl").write_text(
            "\n".join(lines[:keep]) + "\n" + lines[keep][: len(lines[keep]) // 2]
        )
    (tmp_path / "cut.clicks.jsonl").write_bytes((RECORD / "universe24.clicks.jsonl").read_bytes())
    (tmp_path / "cut.json").write_bytes((RECORD / "universe24.json").read_bytes())
    eras, nodes, clicks = (tmp_path / f"cut.{kind}.jsonl" for kind in ("eras", "nodes", "clicks"))
    ERAS_PAGE.main(
        [str(eras), "--clicks", str(clicks), "--nodes", str(nodes), "--out", str(tmp_path / "cut.html")]
    )
    TORUS.main(
        [
            str(nodes),
            "--eras",
            str(eras),
            "--clicks",
            str(clicks),
            "--world",
            str(tmp_path / "cut.json"),
            "--out",
            str(tmp_path / "cut.torus.html"),
        ]
    )
    for name in ("cut.html", "cut.torus.html"):
        parsed = tables_of((tmp_path / name).read_text())
        kinds = {row[0]: row for row in parsed.rows["kinds"][1:]}
        assert kinds["bangs"][2:] == ["2", "at 1, 311"]
        assert kinds["tops"][2] == "1" and kinds["standing proton"][3].endswith(
            "at 400, standing since 29 (carried through every top)"
        )
        cycles = parsed.rows["ledger"]
        assert len(cycles) == 3 and cycles[2][1:4] == [
            "311",
            "400 (the log's last interval)",
            "none reached",
        ]
        assert cycles[2][8] == "0" and cycles[1][8] == "125"
        assert "to the interval 400 of 2,400 declared" in (tmp_path / name).read_text()
