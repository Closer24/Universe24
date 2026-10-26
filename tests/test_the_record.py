"""The committed records (examples/records: the hole seed at 60 on the 5-cube, the chiral seed at 60, the bodies' seed at 300 on the 7-cube, regenerated under PM-S1 on 2026-10-25, again under CK-S1 and the emission's odd rounding the same day, again under the crossing read even and the light no body (the plane at the gap 0 never credited as a body), and again under PL-S1 (the charge read at the kick in its momentum form, the owner's word of 2026-10-25, 22:50 UTC, through the Boss, 6404425423; the bodies bit for bit): the era of matter SHOWN on the hole seed, Coulomb's sign NOT SHOWN there under PL-S1 (SHOWN in part, unlike senses approach, under the former write of 2 W after the step; NOT SHOWN under the crossing odd at a touch of zero) and the collisions NOT SHOWN with it on the hole (SHOWN under the former write; SHOWN on the chiral), the bodies' well SHOWN, the bodies' credited Nodes receding, the bodies' gate 8 NOT SHOWN by two credits at turned Nodes decoding beyond the floor, so the take's event stands for the click; the hole's births 16 and credits 777 under PL-S1 (24 and 1,124 under A48-S1 (05cca50, the read of the remainder in the laid frame, reverted for the tie of the sign row's write remainder and the births' seed); 16 and 233 under the former write of 2 W after the step, 20 and 514 before), the chiral's 17 and 2,943 with the collisions SHOWN (19 and 3,052 with them NOT SHOWN under the reverted read; 2,914; 16 and 2,336 before), the bodies' 1,973 bit for bit (1,819 before CK-S1)) read by the decoder's gates, each verdict asserted by name so that a lost or a gained verdict fails by name, den's circle under gate 19 by its count (MS-S2: 26 points at the toy's den, 8 at the middle's, the typed pairs among them); the conservation check over every record's log (the charge, the count taken against booked, the integers' count constant, every integer within the width, the run back exact); the hole record re-run by the engine and compared with the committed one bit for bit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from event_universe.events import NAMES
from event_universe.gates import gates
from event_universe.run import record
from tests.laws import ROOT, load_file, world_of

RECORDS, WIDTH = ROOT / "examples" / "records", 128
CIRCLES = {"bodies": (8, 2), "chiral": (26, 3), "hole": (26, 3)}  # den's circle: its points, the typed
SHOWN_ROWS = {  # the numbered rows SHOWN (whole or in part) per record, the Boss's count in Universe24
    # on the records of 3dc12e307 (the five sentences built on toys-5, the remainder and the merger among them): the hole loses 2 (the Links lengthening in the clicks, under GP-S1's lay) and gains 47 (the exact take, the excess kept as the remainder, EX-S1); the chiral loses 58 and gains 24 (two pairs into light, MG-S1), 15 kept by the decoder's read of the remainder, 17 lost by the engine's bug at a merger's tie end (H-Children-Charge-Bug-1: the light laid as the charged child's lay, the children's own charges -36,000 over the births; SHOWN again at the fix); the bodies gain 8 and 16 with the credits the remainder pays; the hole under PL-S1 before: 9 and 22 among them under the former write of 2 W after the step
    "hole": {
        4,
        5,
        7,
        8,
        10,
        15,
        16,
        17,
        18,
        19,
        21,
        25,
        26,
        27,
        30,
        37,
        43,
        45,
        47,
        58,
        59,
        60,
        62,
        64,
        65,
        66,
        67,
    },
    "chiral": {
        2,
        4,
        5,
        7,
        8,
        9,
        10,
        15,
        16,
        18,
        19,
        21,
        22,
        24,
        25,
        26,
        27,
        30,
        37,
        43,
        45,
        47,
        59,
        60,
        62,
        64,
        66,
        67,
    },
    "bodies": {2, 3, 5, 6, 7, 8, 9, 10, 16, 18, 30, 37, 43, 45, 59, 60, 64, 66},
}
VERDICTS = {  # the verdicts' words by name
    "hole": {
        "63 the uniformity in the clicks": "NOT SHOWN: 0 regions without a credit, the least 34 against the largest 444",
        "65 the lepton number": "SHOWN: every species' senses sum to 0 over its births, its number conserved at the click",
        "67 CPT in the clicks": "SHOWN: the charge odd under C and under T and even under CPT on 1631 of 1631 frames",
        "9 collisions": "NOT SHOWN: the credited Nodes receding",
        "22 Coulomb's sign": "NOT SHOWN: unlike senses do not approach, like senses do not part",
        "45 the bodies' well, binding and collapse": "SHOWN: a body stands in its own well through the run",
        "56 Bell": "NOT SHOWN as nature: |S| <= 2 at the pairs' clicks, S = 12 / 16",
        "58 the fast expansion after the bang": "SHOWN: the credits' spacing grows fastest in the first eighths",
        "59 the deceleration in the clicks": "SHOWN: an eighth's growth of the spacing smaller than the one before",
        "60 the acceleration in the clicks": "SHOWN: after a slowing, an eighth's growth of the spacing larger",
        "15 conservation at the click": "SHOWN exact: taken + the remainder before - the remainder after = booked on every birth (EX-S1)",
        "47 the exact take": "SHOWN: the take exact on every birth, its excess kept as the remainder at the Node (EX-S1)",
        "62 the arrow of time in the clicks": "SHOWN: the charge odd under the slot exchange, 1631 of 1631 frames",
    },
    "chiral": {
        "64 dark matter in kind": "SHOWN: 98 of 143 bodies credited at a Node where no light was laid",
        "65 the lepton number": "NOT SHOWN: 1 species with a sum not 0",
        "66 the energy in the clicks": "SHOWN in part: on most pairs",
        "24 the merger (a pair into light)": "SHOWN: 2 pairs into light (the gap-0 children born from a gapped record's take)",
        "62 the arrow of time in the clicks": "SHOWN: the charge odd under the slot exchange, 2956 of 2956 frames",
        "17 charge conservation": "NOT SHOWN: the children's own charges sum to -36000 over the births, 2 mergers with a charged child",
        "9 collisions": "SHOWN: two bodies' credited Nodes approached and stood one Link apart",
        "15 conservation at the click": "SHOWN: taken + the remainder before - the remainder after = booked on every birth carrying the remainder (EX-S1), taken >= booked on the rest (the mergers' ends)",
        "47 the exact take": "SHOWN: the take exact on every birth, its excess kept as the remainder at the Node (EX-S1)",
        "1b the board tops, every Node turning at once": "NOT SHOWN: no interval with every Node turned",
        "1c the board returns to Gamma": "NOT SHOWN: no bottom at Gamma at every Node",
        "56 Bell": "NOT SHOWN as nature: |S| <= 2 at the pairs' clicks, S = 2 / 11",
    },
    "bodies": {
        "64 dark matter in kind": "SHOWN: 91 of 91 bodies credited at a Node where no light was laid",
        "67 CPT in the clicks": "NOT READ: no frame carries a charge",
        "37 Maxwell's one Link per interval": "SHOWN: the current's reach grows by one Link",
        "55 the two slits": "NOT READ: no two gap-0 packets at one centre",
        "56 Bell": "NOT READ: 0 births, no born pair clicked at both ends",
        "57 GHZ": "NOT READ: a birth gives two ends at one Link and a shared take four",
        "61 the horizon radiates": "NOT READ: no frozen Node in the record (as gate 14)",
        "62 the arrow of time in the clicks": "NOT READ: no frame carries a charge",
        "58 the fast expansion after the bang": "NOT SHOWN: the first growth of the spacing is not above zero",
        "59 the deceleration in the clicks": "SHOWN: an eighth's growth of the spacing smaller than the one before",
    },
}


def loaded(name: str) -> dict[str, Any]:
    return json.loads((RECORDS / f"{name}.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", sorted(SHOWN_ROWS))
def test_the_committed_record_shows_the_gates_by_name(name: str) -> None:
    found = gates(loaded(name))
    kinds = {int(k[:2]): v["kind"] for k, v in found.items() if k[:2].strip().isdigit()}
    assert set(kinds) == {int(k) for k in NAMES if k.isdigit()}  # the rows named once, in events.NAMES
    assert {n for n, kind in kinds.items() if kind.startswith("SHOWN")} == SHOWN_ROWS[name]
    assert {n for n, kind in kinds.items() if kind == "NOT REACHED"} == {14, 34}  # the horizon
    for gate, verdict in VERDICTS[name].items():
        assert found[gate]["verdict"].startswith(verdict), (name, gate, found[gate]["verdict"])
    assert found["the three constants"]["verdict"].startswith("SHOWN")
    circle = next(v for k, v in found["19 mass ratios (parts per million)"].items() if "circle" in k)
    assert (len(circle), sum(1 for _ratio, typed in circle if typed)) == CIRCLES[name]


@pytest.mark.parametrize("name", sorted(SHOWN_ROWS))
def test_the_conservations_hold_on_the_record(name: str) -> None:
    """The independent check: the conservations recomputed from the record's log alone, beside what rows 15, 17, 18 and the constants read."""
    run = loaded(name)
    births = [e for e in run["log"] if e["event"] == "birth"]
    pairs = [
        b for b in births if "exact_lay" not in b
    ]  # a merger's light children carry no sense (MG-S1)
    signs = [(w > 0) - (w < 0) for b in pairs for w in b["W_children"]]
    assert sum(signs) == 0 and 0 not in signs

    # EX-S1's identity at the gap-0 take; a merger's ends taken whole (MG-S1)
    paid = [b["taken"] + b.get("remainder_was", 0) - b.get("remainder", 0) - b["booked"] for b in births]
    assert all(x == 0 if "remainder" in b else x >= 0 for x, b in zip(paid, births, strict=True))
    assert len({row["integers"] for row in run["rows"]}) == 1
    assert max(max(row["max bits"], row["max transient bits"]) for row in run["rows"]) <= WIDTH
    assert run["run_back"]["exact"] == run["run_back"]["intervals"] == 20
    assert int(run["counts"]["births"]) == len(births)
    assert all("sense" in e for e in run["log"] if e["event"] == "lay")


def test_the_hole_record_is_the_engines_own_bit_for_bit() -> None:
    universe, world = world_of("world_hole.json")
    committed = loaded("hole")
    assert committed["world"] == world and committed["universe"] == universe
    found = json.loads(json.dumps(record(universe, world, 20, lambda line: None)))
    assert found["log"] == committed["log"] and found["counts"] == committed["counts"]
    assert found["turns"] == committed["turns"] and found["run_back"] == {"intervals": 20, "exact": 20}
    timeless = [{k: v for k, v in row.items() if k != "milliseconds"} for row in found["rows"]]
    assert timeless == [{k: v for k, v in r.items() if k != "milliseconds"} for r in committed["rows"]]


@pytest.mark.parametrize("name", sorted(SHOWN_ROWS))
def test_the_committed_reading_is_the_decoders_own_whole(name: str) -> None:
    """The whole reading beside the record equals a fresh read, line for line after JSON (the one check of every key, number, verdict, field and event)."""
    assert [{k: v} for k, v in json.loads(json.dumps(gates(loaded(name)))).items()] == reading_of(name)


def reading_of(name: str) -> list[dict[str, Any]]:
    """The committed reading beside the record, one JSON per line (the gates' output)."""
    lines = (RECORDS / f"{name}.reading.jsonl").read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


@pytest.mark.parametrize("name", sorted(SHOWN_ROWS))
def test_the_record_carries_a_node_line_per_interval_and_the_reading_its_events(name: str) -> None:
    run = loaded(name)
    count = int(run["cube"]) ** 3
    assert [line["i"] for line in run["nodes"]] == list(range(1, int(run["intervals"]) + 1))
    for line in run["nodes"]:
        assert len(line["X"]) == len(line["content"]) == count
        sites = line["turned"] + line["frozen"] + [h[0] for h in line["held"]]
        assert all(0 <= i < count for i in sites)
        assert all(h[1] in (0, 1, 2) for h in line["held"])
    assert sum(len(line["turned"]) for line in run["nodes"]) == int(run["counts"]["turns"])
    events = next(line["events"] for line in reading_of(name) if "events" in line)
    labels = [e["label"] for e in events]
    assert "the run back exact" in labels
    clicks = (
        "a pair born",
        "a body clicks",
        "light absorbed at a take",
    )  # gate 7's take is every click's
    first = next((e for e in events if e["label"] in clicks), None)
    assert first is not None and first["i"] == min(
        e["i"] for e in run["log"] if e["event"] in ("birth", "credit")
    )
    assert all(len(e["label"].split()) <= 6 for e in events)
    rows = {k[:2]: v for line in reading_of(name) for k, v in line.items() if k[:2] in ("1b", "1c")}
    eras = next(line["the eras"] for line in reading_of(name) if "the eras" in line)
    returns = int(rows["1c"]["cause"].split()[0]) if rows["1c"]["kind"] == "SHOWN" else 0
    tops = int(rows["1b"]["cause"].split(" tops")[0].split()[-1]) if rows["1b"]["kind"] == "SHOWN" else 0
    assert (
        len(eras["bangs"]) == 1 + returns and len(eras["tops"]) == tops
    )  # every one, beyond the eight listed


def test_the_gates_of_the_phenomena_are_one_table_written_from_the_readings(tmp_path: Path) -> None:
    tool = load_file("phenomena", ROOT / "tools" / "phenomena.py")
    readings = {name: tool.reading_of(RECORDS / f"{name}.reading.jsonl") for name in SHOWN_ROWS}
    whole = {g for rows in readings.values() for g, r in rows.items() if r["kind"] == "SHOWN"}
    table = tool.table_of("test", readings, {})
    rows = [
        line
        for line in table.splitlines()
        if line.startswith("| ") and line.split("|")[2].strip().isdigit()
    ]
    names = {g: r["phenomenon"] for rows in readings.values() for g, r in rows.items()}
    count = len(
        {int(k) for k in NAMES if k.isdigit()}
    )  # the rows named once, the table's count from the readings
    assert len(rows) == tool.rows_in(readings) == count and all(names[k] in rows[k - 1] for k in names)
    assert (
        whole <= set.union(*SHOWN_ROWS.values())
        and f"SHOWN in Universe24: {len(whole)} of {count} on test" in table
    )
    document = tmp_path / "UNIVERSE24.md"
    document.write_text(
        "## 2\n\n### The gates widened to everything derived\n\nrest\n", encoding="utf-8"
    )
    assert tool.write(document, "test", readings) in document.read_text(encoding="utf-8")


def test_the_page_is_one_html_from_the_record_and_the_reading_with_nothing_typed(tmp_path: Path) -> None:
    page = load_file("page", ROOT / "tools" / "page.py")
    out = tmp_path / "hole.html"
    page.write_page(RECORDS / "hole.json", RECORDS / "hole.reading.jsonl", out)
    text = out.read_text(encoding="utf-8")
    run = loaded("hole")
    assert text.isascii() and text.count("<canvas") == 1 and "color-scheme: dark" in text
    assert f"den {run['universe']['integers']['den']}" in text
    assert f"shape {run['world']['shape']}" in text
    events = next(line["events"] for line in reading_of("hole") if "events" in line)
    assert all(e["label"] in text for e in events)
    source = (ROOT / "tools" / "page.py").read_text(encoding="utf-8")
    assert str(run["den"]) not in source and "electron" not in source and "light" not in source
