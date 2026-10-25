"""The committed records (examples/records: the hole seed at 60 on the 5-cube, the chiral seed at 60, the bodies' seed at 300 on the 7-cube) read by the decoder's gates, each verdict asserted by name so that a lost or a gained verdict fails by name; the conservation check over every record's log (the charge, the count taken against booked, the integers' count constant, every integer within the width, the run back exact); the hole record re-run by the engine and compared with the committed one bit for bit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from event_universe.gates import gates
from event_universe.run import record
from tests.laws import ROOT, world_of

RECORDS = ROOT / "examples" / "records"
WIDTH = 128
SHOWN = {
    "hole": {
        "17 charge conservation": "SHOWN",
        "18 the arrow of time": "SHOWN",
        "the three constants": "SHOWN",
        "the entropy of the clicks": "SHOWN",
        "14 the horizon": "NOT REACHED",
        "4 an era of matter": "NOT SHOWN",
    },
    "chiral": {
        "17 charge conservation": "SHOWN",
        "18 the arrow of time": "SHOWN",
        "the three constants": "SHOWN",
        "the entropy of the clicks": "SHOWN",
        "14 the horizon": "NOT REACHED",
    },
    "bodies": {
        "18 the arrow of time": "SHOWN",
        "the three constants": "SHOWN",
        "10 gravitational time dilation": "SHOWN in the reader's view",
        "2 the Links lengthening in the clicks": "SHOWN in the reader's view",
        "1 recurring bangs / 3 shortening then lengthening / 6 contraction (board, the reader's view)": "contraction SHOWN",
        "9 collisions / 13 free fall": "read: 26 lines credited at a new Node",
        "8 families forming (whole view)": "NOT SHOWN",
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
    assert (
        found["log"] == committed["log"]
        and found["counts"] == committed["counts"]
        and found["turns"] == committed["turns"]
    )
    timeless = [{k: v for k, v in row.items() if k != "milliseconds"} for row in found["rows"]]
    assert timeless == [
        {k: v for k, v in row.items() if k != "milliseconds"} for row in committed["rows"]
    ]
    assert found["run_back"] == {"intervals": 20, "exact": 20}
    assert Path(RECORDS / "hole.json").stat().st_size < 10**6
