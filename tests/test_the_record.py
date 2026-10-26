"""The committed records (examples/records: the hole seed at 60 on the 5-cube, the chiral seed at 60, the bodies' seed at 300 on the 7-cube, regenerated under PM-S1 on 2026-10-25, again under CK-S1 and the emission's odd rounding the same day, again under the crossing read even and the light no body (the plane at the gap 0 never credited as a body), and again under PL-S1 (the charge read at the kick in its momentum form, the owner's word of 2026-10-25, 22:50 UTC, through the Boss, 6404425423; the bodies bit for bit): the era of matter SHOWN on the hole seed, Coulomb's sign NOT SHOWN there under PL-S1 (SHOWN in part, unlike senses approach, under the former write of 2 W after the step; NOT SHOWN under the crossing odd at a touch of zero) and the collisions NOT SHOWN with it on the hole (SHOWN under the former write; SHOWN on the chiral), the bodies' well SHOWN, the bodies' credited Nodes receding, the bodies' gate 8 NOT SHOWN by two credits at turned Nodes decoding beyond the floor, so the take's event stands for the click; the hole's births 16 and credits 777 under PL-S1 (233 under the former write of 2 W after the step, 20 and 514 before), the chiral's 17 and 2,943 (2,914; 16 and 2,336 before), the bodies' 1,973 against 1,819) read by the decoder's gates, each verdict asserted by name so that a lost or a gained verdict fails by name, den's circle under gate 19 by its count (MS-S2: 26 points at the toy's den, 8 at the middle's, the typed pairs among them); the conservation check over every record's log (the charge, the count taken against booked, the integers' count constant, every integer within the width, the run back exact); the hole record re-run by the engine and compared with the committed one bit for bit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from event_universe.gates import gates, kind_of
from event_universe.run import record
from tests.laws import ROOT, load_file, world_of

RECORDS, WIDTH = ROOT / "examples" / "records", 128
CIRCLES = {"bodies": (8, 2), "chiral": (26, 3), "hole": (26, 3)}  # den's circle: its points, the typed
SHOWN_ROWS = {  # the numbered rows SHOWN (whole or in part) per record, the Boss's count in Universe24
    # the hole under PL-S1; 9 and 22 among them under the former write of 2 W after the step
    "hole": {2, 4, 5, 7, 8, 10, 15, 16, 17, 18, 19, 21, 25, 26, 27, 30, 37, 43, 45},
    "chiral": {2, 4, 5, 7, 8, 9, 10, 15, 16, 17, 18, 19, 21, 22, 25, 26, 27, 30, 37, 43, 45},
    "bodies": {2, 3, 5, 6, 7, 9, 10, 18, 30, 37, 43, 45},
}
VERDICTS = {  # the verdicts' words by name
    "hole": {
        "9 collisions": "NOT SHOWN: the credited Nodes receding",
        "22 Coulomb's sign": "NOT SHOWN: unlike senses do not approach, like senses do not part",
        "45 the bodies' well, binding and collapse": "SHOWN: a body stands in its own well through the run",
    },
    "chiral": {
        "9 collisions": "SHOWN: two bodies' credited Nodes approached and stood one Link apart",
        "1b the board tops, every Node turning at once": "NOT SHOWN: no interval with every Node turned",
        "1c the board returns to Gamma": "NOT SHOWN: no bottom at Gamma at every Node",
    },
    "bodies": {"37 Maxwell's one Link per interval": "SHOWN: the current's reach grows by one Link"},
}


def loaded(name: str) -> dict[str, Any]:
    return json.loads((RECORDS / f"{name}.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", sorted(SHOWN_ROWS))
def test_the_committed_record_shows_the_gates_by_name(name: str) -> None:
    found = gates(loaded(name))
    kinds = {int(k[:2]): kind_of(v["verdict"]) for k, v in found.items() if k[:2].strip().isdigit()}
    assert len(kinds) == 54
    assert {n for n, kind in kinds.items() if kind.startswith("SHOWN")} == SHOWN_ROWS[name]
    assert {n for n, kind in kinds.items() if kind == "NOT REACHED"} == {14, 34}  # the horizon
    for gate, verdict in VERDICTS[name].items():
        assert found[gate]["verdict"].startswith(verdict), (name, gate, found[gate]["verdict"])
    assert found["the three constants"]["verdict"].startswith("SHOWN")
    circle = next(v for k, v in found["19 mass ratios (parts per million)"].items() if "circle" in k)
    assert (len(circle), sum(1 for _ratio, typed in circle if typed)) == CIRCLES[name]


@pytest.mark.parametrize("name", sorted(SHOWN_ROWS))
def test_the_conservations_hold_on_the_record(name: str) -> None:
    run = loaded(name)
    births = [e for e in run["log"] if e["event"] == "birth"]
    signs = [(w > 0) - (w < 0) for b in births for w in b["W_children"]]
    assert sum(signs) == 0 and 0 not in signs
    assert all(b["taken"] >= b["booked"] for b in births)
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
    assert events == gates(run)["events"]
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
