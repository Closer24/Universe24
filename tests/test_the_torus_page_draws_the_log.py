"""The torus view (tools/look/torus_page.py) draws the Nodes' log and nothing else (the owner's word of 2026-10-23: every Node in three dimensions, the Link's length between them, the time's direction by colour, the content; the owner's rule: every test of the law's course on a structured board): on the universe test's small structured board, the 3-cube torus with one clump of matter, light and one instrument body of its own beat (tests/test_universe24_runs_its_cycle.py's world), tools/eras.py's run writes the eras log, the clicks log and the Nodes' log over 32 intervals (two windows of the beat 15), the page tool writes one page from them, and the page's embedded data equals the log line for line: every Node's Link length e^U = (X / Gamma)^(1 / 4) and every Node's direction of time at every interval, the Nodes turned, the quanta per Node, the clicks written at the instrument's Node and its chart's 1 / e^U and light's quanta the log's own; the page's script holds no number that is not the log's."""

import json
import re
from pathlib import Path

import pytest

from event_universe import world_files
from tests.laws import ROOT, load_file
from tests.laws_universe import GAMMA, small_universe

ERAS = load_file("eras_for_the_torus", ROOT / "tools" / "eras.py")
TORUS = load_file("torus_page", ROOT / "tools" / "look" / "torus_page.py")
INTERVALS = 12


def embedded(html: str, name: str) -> object:
    found = re.search(rf'<script id="{name}" type="application/json">(.*?)</script>', html, re.S)
    assert found is not None, name
    return json.loads(found.group(1).replace("<\\/", "</"))


def test_the_torus_page_holds_every_nodes_length_direction_and_content_from_the_log(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    small_universe(tmp_path)  # the tests' small universe on a bare 3-cube
    world = tmp_path / "small.json"
    world.write_text(json.dumps({"shape": [3, 3, 3], "intervals": INTERVALS, "universe": "u.json"}))
    eras, clicks, nodes = (tmp_path / f"small.{kind}.jsonl" for kind in ("eras", "clicks", "nodes"))
    ERAS.run(world, eras, 100, INTERVALS, clicks, nodes)
    logged = TORUS.read_log(nodes)
    assert [line["interval"] for line in logged] == list(range(1, INTERVALS + 1))
    for line in (
        logged
    ):  # the log's own consistency: the length is the level's fourth root, the direction a sign
        assert len(line["X"]) == len(line["length"]) == len(line["direction"]) == 27
        assert all(
            abs(length - (x / GAMMA) ** 0.25) < 1e-5
            for x, length in zip(line["X"], line["length"], strict=True)
        )
        assert set(line["direction"]) <= {1, -1}
    html = TORUS.page(
        logged, TORUS.read_log(eras), TORUS.read_log(clicks), json.loads(world.read_text()), None
    )
    drawn = embedded(html, "nodes")
    assert drawn == json.loads(
        json.dumps(logged)
    )  # (1) every Node's length, direction, turned list and quanta, line for line
    course = embedded(html, "course")
    assert course["shape"] == [3, 3, 3] and course["gamma"] == GAMMA and len(course["rows"]) == INTERVALS
    assert embedded(html, "charts") == []  # no instrument body: the board reads itself (2026-10-24)
    assert "cdn" not in html.lower() and "<script src" not in html  # plain HTML, no library
