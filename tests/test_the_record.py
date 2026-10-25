"""The committed records (examples/records: the hole seed at 60 on the 5-cube, the chiral seed at 60, the bodies' seed at 300 on the 7-cube, regenerated under PM-S1 on 2026-10-25: the era of matter SHOWN on the hole seed, the bodies' credited Nodes receding) read by the decoder's gates, each verdict asserted by name so that a lost or a gained verdict fails by name, den's circle under gate 19 by its count (MS-S2: 26 points at the toy's den, 8 at the middle's, the typed pairs among them); the conservation check over every record's log (the charge, the count taken against booked, the integers' count constant, every integer within the width, the run back exact); the hole record re-run by the engine and compared with the committed one bit for bit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from event_universe.gates import gates
from event_universe.run import record
from tests.laws import ROOT, load_file, world_of

RECORDS = ROOT / "examples" / "records"
WIDTH = 128
BASE = {
    "17 charge conservation": "SHOWN",
    "18 the arrow of time": "SHOWN",
    "the three constants": "SHOWN",
    "the entropy of the clicks": "SHOWN",
    "14 the horizon": "NOT REACHED",
}
CHARGE = (
    "SHOWN: the senses sum to 0; the magnitude SHOWN"  # MS-S1: one |W| where the plane stood at nothing
)
SHOWN = {
    "hole": {**BASE, "4 an era of matter": "SHOWN", "17 charge conservation": CHARGE},
    "chiral": {**BASE, "17 charge conservation": CHARGE},
    "bodies": {
        "18 the arrow of time": "SHOWN",
        "the three constants": "SHOWN",
        "10 gravitational time dilation": "SHOWN in the reader's view",
        "2 the Links lengthening in the clicks": "SHOWN in the reader's view",
        "1 recurring bangs / 3 shortening then lengthening / 6 contraction (board, the reader's view)": "contraction SHOWN",
        "9 collisions / 13 free fall": "NOT SHOWN: the credited Nodes receding",
        "8 families forming (whole view)": "SHOWN in part: every credit within the floor, tracks right 63 of 63",
        "16 uncertainty floor (one click)": "SHOWN as the law's floor",
        "the entropy of the clicks": "NOT READ",
    },
}


def loaded(name: str) -> dict[str, Any]:
    return json.loads((RECORDS / f"{name}.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", sorted(SHOWN))
def test_the_committed_record_shows_the_gates_by_name(name: str) -> None:
    found = gates(loaded(name))
    for gate, verdict in SHOWN[name].items():
        assert found[gate]["verdict"].startswith(verdict), (name, gate, found[gate]["verdict"])
    circle = next(
        v for k, v in found["19 mass ratios (parts per million)"].items() if k.startswith("den's circle")
    )
    assert (len(circle), sum(1 for _ratio, typed in circle if typed)) == {
        "bodies": (8, 2),
        "chiral": (26, 3),
        "hole": (26, 3),
    }[name]


@pytest.mark.parametrize("name", sorted(SHOWN))
def test_the_conservations_hold_on_the_record(name: str) -> None:
    run = loaded(name)
    births = [e for e in run["log"] if e["event"] == "birth"]
    signs = [(w > 0) - (w < 0) for b in births for w in b["W_children"]]
    assert sum(signs) == 0 and 0 not in signs
    assert all(b["taken"] >= b["booked"] for b in births)
    assert len({row["integers"] for row in run["rows"]}) == 1
    assert max(row["max bits"] for row in run["rows"]) <= WIDTH
    assert max(row["max transient bits"] for row in run["rows"]) <= WIDTH
    assert run["run_back"]["exact"] == run["run_back"]["intervals"] == 20
    assert int(run["counts"]["births"]) == len(births)


def test_the_hole_record_is_the_engines_own_bit_for_bit() -> None:
    universe, world = world_of("world_hole.json")
    committed = loaded("hole")
    assert committed["world"] == world and committed["universe"] == universe
    found = json.loads(json.dumps(record(universe, world, 20, lambda line: None)))
    assert found["log"] == committed["log"] and found["counts"] == committed["counts"]
    assert found["turns"] == committed["turns"] and found["run_back"] == {"intervals": 20, "exact": 20}
    timeless = [{k: v for k, v in row.items() if k != "milliseconds"} for row in found["rows"]]
    assert timeless == [{k: v for k, v in r.items() if k != "milliseconds"} for r in committed["rows"]]


def reading_of(name: str) -> list[dict[str, Any]]:
    """The committed reading beside the record, one JSON per line (the gates' output)."""
    lines = (RECORDS / f"{name}.reading.jsonl").read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


@pytest.mark.parametrize("name", sorted(SHOWN))
def test_the_record_carries_a_node_line_per_interval_and_the_reading_its_events(name: str) -> None:
    run = loaded(name)
    count = int(run["cube"]) ** 3
    assert [line["i"] for line in run["nodes"]] == list(range(1, int(run["intervals"]) + 1))
    for line in run["nodes"]:
        assert len(line["X"]) == len(line["content"]) == count
        assert all(
            0 <= i < count for i in line["turned"] + line["frozen"] + [h[0] for h in line["held"]]
        )
        assert all(h[1] in (0, 1, 2) for h in line["held"])
    assert sum(len(line["turned"]) for line in run["nodes"]) == int(run["counts"]["turns"])
    events = next(line["events"] for line in reading_of(name) if "events" in line)
    assert events == gates(run)["events"]
    labels = [e["label"] for e in events]
    assert "the run back exact" in labels
    first = next((e for e in events if e["label"] in ("a pair born", "a body clicks")), None)
    assert first is not None and first["i"] == min(
        e["i"] for e in run["log"] if e["event"] in ("birth", "credit")
    )
    assert all(len(e["label"].split()) <= 6 for e in events)


def test_the_page_is_one_html_from_the_record_and_the_reading_with_nothing_typed(tmp_path: Path) -> None:
    page = load_file("page", ROOT / "tools" / "page.py")
    out = tmp_path / "hole.html"
    page.write_page(RECORDS / "hole.json", RECORDS / "hole.reading.jsonl", out)
    text = out.read_text(encoding="utf-8")
    run = loaded("hole")
    assert text.isascii() and text.count("<canvas") == 1 and "color-scheme: dark" in text
    assert (
        f"den {run['universe']['integers']['den']}" in text and f"shape {run['world']['shape']}" in text
    )
    events = next(line["events"] for line in reading_of("hole") if "events" in line)
    assert all(e["label"] in text for e in events)
    source = (ROOT / "tools" / "page.py").read_text(encoding="utf-8")
    assert str(run["den"]) not in source and "electron" not in source and "light" not in source
