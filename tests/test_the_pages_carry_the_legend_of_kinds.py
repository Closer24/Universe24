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
    """(1) The record's legend at the enlarged den on the merged engine (2026-10-24; the former dens' numbers in the folder's notes): 7 bangs, 6 tops, 0 black holes, 0 turns at the floor, 750 Node turns, 125 proton births at 30 at 125 Nodes, 0 electron births with the cause (matter's row gone), 0 conversions, 125 clicks counted whole, 375 lays, the proton standing 4 per Node at 2,400, light 0 from 29, bound bodies not readable; (2) the ledger: 8 rows, 125 proton pairs in the first, 0 births in every row after, the finding sentence."""
    eras, nodes, clicks = logs()
    floor = ERAS_PAGE.least_of(nodes, eras[0]["node_clock"])["floor"]
    legend = CAPTIONS.legend_of(eras, nodes, clicks, floor)
    assert legend["reached"] == 2400 and legend["declared"] == 2400
    rows = {row["kind"]: row for row in legend["rows"]}
    counts = {kind: row["count"] for kind, row in rows.items()}
    assert counts == {
        "bangs": 7,
        "tops": 6,
        "black holes": 0,
        "turns at the floor (the crunch)": 0,
        "Node turns (the swap at the top)": 750,
        "proton births": 125,
        "electron births": 0,
        "conversions": 0,
        "clicks": 125,
        "lays (the records laid)": 625,
        "standing light (the seed family: light left)": 0,
        "standing proton": 4250,
        "standing electron": 0,
        "standing charge (a holder, beside the families of quanta: the held row writes none of it)": 0,
        "bound bodies": None,
    }
    assert rows["bangs"]["words"] == "at 1, 390, 764, 1,136, 1,510, 1,882, 2,256"
    assert rows["tops"]["words"].startswith("204 at the volume 3,978,250; 577 at the volume 4,133,375")
    assert (
        rows["black holes"]["words"]
        == "0 in this run: the eras log's horizon 0 at every interval to 2,400"
    )
    assert rows["turns at the floor (the crunch)"]["words"] == (
        "0 Node turns at or under the floor 19; the least X over the run 1,003"
    )
    assert rows["proton births"]["words"] == (
        "125 births at 30, at 125 Nodes, the senses [-1, 1] (matter and antimatter)"
    )
    assert rows["electron births"]["words"].startswith(
        "none born: every birth line's children are proton and proton, the heaviest list within the two meeting quanta's energy"
    )
    assert rows["clicks"]["words"].startswith("125 at 30, 125 the board's own")
    assert rows["clicks"]["words"].endswith("every click counted whole, no part drawn")
    assert rows["standing proton"]["words"] == (
        "4,250 quanta, 34 per Node, at 125 Nodes at 2,400, standing since 30 (carried through every top)"
    )
    assert (
        rows["standing light (the seed family: light left)"]["words"]
        == "0 from 30: standing from 1, spent at the holes"
    )
    assert rows["bound bodies"]["words"].startswith("not readable from the logs")
    assert all(row["law"] for row in legend["rows"])  # every kind named in the law by one clause
    ledger = CAPTIONS.ledger_of(eras, nodes, clicks)
    cycles = ledger["rows"]
    assert [(c["bang"], c["at"], c["to"], c["top"], c["volume"]) for c in cycles[:3]] == [
        (1, 1, 389, 204, 3978250),
        (2, 390, 763, 577, 4133375),
        (3, 764, 1135, 950, 3978250),
    ]
    assert len(cycles) == 7 and cycles[-1]["open"] and cycles[-1]["to"] == 2400
    assert cycles[0]["births"] == {"proton": 125, "electron": 0}  # matter's row left the file 2026-10-24
    assert all(sum(c["births"].values()) == 0 for c in cycles[1:])
    assert all(c["light"] == 0 and c["horizon"] == 0 for c in cycles)
    assert [c["turns"] for c in cycles] == [125] * 6 + [0]  # the seventh cycle open before its top
    assert [c["standing"]["proton"] for c in cycles[:2]] == [
        "4,625 quanta, 37 per Node, at 125 Nodes",
        "4,750 quanta, 38 per Node, at 125 Nodes",
    ]
    assert ledger["finding"].startswith(
        "The logs show nothing new after bang 1: 6 cycles after the first with 0 births each, the first cycle's births 125 proton pairs, the light spent at 30"
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
        assert len(cycles) == 8 and cycles[1][:5] == [
            "1",
            "1",
            "389",
            "204 at the volume 3,978,250",
            "125 proton pairs; 0 electron pairs",
        ]
        assert (
            cycles[7][2] == "2,400 (the log's last interval)"
            and cycles[7][4] == "0 proton pairs; 0 electron pairs"
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
        assert kinds["bangs"][2:] == ["2", "at 1, 390"]
        assert kinds["tops"][2] == "1" and kinds["standing proton"][3].endswith(
            "at 400, standing since 30 (carried through every top)"
        )
        cycles = parsed.rows["ledger"]
        assert len(cycles) == 3 and cycles[2][1:4] == [
            "390",
            "400 (the log's last interval)",
            "none reached",
        ]
        assert cycles[2][8] == "0" and cycles[1][8] == "125"
        assert "to the interval 400 of 2,400 declared" in (tmp_path / name).read_text()


def test_the_captions_name_the_three_prime_lifts_by_rising_sine_at_every_den() -> None:
    """The pages' captions are a look and no law (the owner's word of 2026-10-24 on the born-amplitude hand's reading): among the lifts of den's primes, the vectors with one entry twice the prime's exponent, by rising sine the electron, the proton and the neutron's candidate, the top point and the composite points their label alone; at den 1,021 the one lift is the electron, the least leg as before; at the top tier the former rule's names stand, point 0 2 0 electron and point 0 0 2 proton, with point 2 0 0 the neutron's; at the PeV tier point 0 0 2 electron, point 2 0 0 proton and point 0 2 0 neutron, where the former rule, the heaviest prime's point proton, named the least leg."""
    from event_universe.loader.circle import circle_points, factors, label_of

    def header(den: int) -> dict:  # type: ignore[type-arg]
        points = {label_of(v): [n, s] for v, n, s in circle_points(den)}
        return {"seed": "massless", "primes": sorted(factors(den).items()), "points": points}

    assert CAPTIONS.captions_for(header(1021)) == {"massless": "light", "point 2": "electron"}
    top = CAPTIONS.captions_for(header(1_166_991_900_949_580_266_237))
    assert top == {
        "massless": "light",
        "point 0 2 0": "electron",
        "point 0 0 2": "proton",
        "point 2 0 0": "neutron",
    }
    # the PeV den's captions stand in tests/test_the_loader.py::test_dens_circle_is_read_from_its_integers_alone, the one test that factors it (2026-10-24)
    assert CAPTIONS.captions_for(None) == {} and CAPTIONS.captions_for({"seed": "light"}) == {
        "light": "light"
    }
