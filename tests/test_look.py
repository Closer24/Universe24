"""The look's viewer (docs/ENGINE.md #6-how-to-run-a-world): the host reader writes one diagnostic file per world and the page builder one page from it, generic for any world; a smoke test on the chain, and the slit's screen read per Node against an expectation in tools/click_counts.py's format."""

from __future__ import annotations

import json

from event_universe import world_files
from tests.laws import CHAIN, ROOT, SLIT, chain_body_world, load_file, slit_world

TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
RECORD = load_file("look_record", ROOT / "tools" / "look" / "record.py")
PAGE = load_file("look_page", ROOT / "tools" / "look" / "page.py")
COUNTS = load_file("click_counts", ROOT / "tools" / "click_counts.py")
ROLE_OF = {"sign": "light", "content": "field"}  # a holder of nothing is matter
SCREEN = {"name": "screen", "positions": [[20, y, 0] for y in range(9)]}
BLIND = {"detector": "screen", "family": "charge", "window": [1, 2], "across": "y", "pattern": [1, 7]}
BLIND.update(counts=[0, 1, 2, 4, 2, 1, 0, 0, 0], through=10, watch={"4": 2, "3": 1.5})


def shown(world, monkeypatch, detector, at, blind):
    """The look of `world` over three intervals from a GameBoard that clicks on `detector` at the Nodes `at` names per interval (the worlds here do not click by themselves in three intervals; the lines' placement and their counting is what is checked), and the page built from it with `blind` as its expectation file, as text."""

    class Clicking(RECORD.GameBoard):
        def step(self) -> None:
            super().step()
            for node in at.get(self.tick, []):
                line = {"event": "click", "tick": self.tick, "family": "charge", "detector": detector}
                self.observer({**line, "node": node, "axis": [0, 1], "count": 1, "body": None})

    monkeypatch.setattr(RECORD, "GameBoard", Clicking)
    RECORD.main([str(world), "--ticks", "3"])
    world.with_suffix(".blind.json").write_text(json.dumps(blind), encoding="utf-8")
    PAGE.main([str(world.with_suffix(".look.json")), "--blind", str(world.with_suffix(".blind.json"))])
    look = json.loads(world.with_suffix(".look.json").read_text(encoding="utf-8"))
    return look, world.with_suffix(".look.html").read_text(encoding="utf-8")


def test_the_reader_writes_the_look_and_the_page_shows_it_with_the_roles(tmp_path, monkeypatch):
    """(a) The look of the chain over three intervals: the label, the file's families, per frame every array sized to the board, frame 0 the declared counts, each click line in its interval's frame (one per interval from the test's own GameBoard), no inner face, the books; (b) the page: the label, the roles from the file's rows (the holder of the sign light, a holder of the content a field, a holder of nothing matter, a further one dashed), the blind file's window, the per-detector bars of an expectation without an axis, and no interpolation between Nodes."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL, at=(24, 40), holds={"charge": 64}, taker=True)
    blind = {"expected": {"taker": 3}, "family": "charge", "window": [1, 2]}
    look, html = shown(world, monkeypatch, "taker", {t: [[24, 0, 0]] for t in (1, 2, 3)}, blind)
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))["families"]
    assert look["label"] == "GameBoard reading" and look["verdict"] == "LAWFUL" and look["ticks"] == 3
    assert [f["name"] for f in look["families"]] == [f["name"] for f in universe] and look["faces"] == []
    assert len(look["frames"]) == 4 and look["shape"] == [CHAIN, 1, 1] and look["arrays"] == "dense"
    rows = [row for fr in look["frames"] for row in fr["families"].values()]
    arrays = [v for row in rows for k, v in row.items() if k != "parts" and isinstance(v, list)]
    assert all(len(a) == CHAIN and all(len(x) == 1 and len(x[0]) == 1 for x in a) for a in arrays)
    laid = [look["frames"][0]["families"][f["name"]]["count"] for f in look["families"] if f["quanta"]]
    declared = sum(b["declared"] + sum(map(sum, b["holds"].values())) for b in look["bodies"])
    assert sum(x[0][0] for a in laid for x in a) == declared
    assert all(line["tick"] == t for t, frame in enumerate(look["frames"]) for line in frame["lines"])
    assert [len(frame["lines"]) for frame in look["frames"]] == [0, 1, 1, 1]
    assert set(look["books"]) == {f["name"] for f in look["families"] if f["quanta"]}
    roles = PAGE.roles(look["families"])
    for family, role in zip(universe, roles.values(), strict=True):
        assert role["role"] == ROLE_OF.get(family.get("held", {}).get("count"), "matter")
    dashed = [name for name, role in roles.items() if role["dashed"]]
    assert dashed == [f["name"] for f in universe if "held" not in f][1:]
    assert "GameBoard reading" in html and PAGE.embedded(roles) in html and '"window":[1,2]' in html
    assert '"measurement" type="application/json">null<' in html and "interpolat" not in html.lower()
    assert PAGE.measurement(look, blind) is None and "<title>Chain look</title>" in html
    assert PAGE.packed(look) in html and "DecompressionStream" in html  # the look inflated at load


def test_the_page_draws_the_screen_per_node_with_the_blind_curve_and_the_faces(tmp_path, monkeypatch):
    """The slit world with a screen of nine detector Nodes at x = 20, three intervals with the test's own click lines (two at y = 4 and one at y = 3 within the window [1, 2], one at y = 5 beyond it): the look holds the faces as declared; the page's measurement holds one row per screen Node ordered by y, the rises summed per Node exactly as tools/click_counts.py counts them, the blind counts, the pattern's range, the totals line and the watch lines naming the coordinate; the page embeds it with the look (the faces' cubes) and names the faces' layer."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = slit_world(tmp_path, TOOL, detectors=[SCREEN])
    at = {1: [[20, 4, 0]], 2: [[20, 3, 0], [20, 4, 0]], 3: [[20, 5, 0]]}
    look, html = shown(world, monkeypatch, "screen", at, BLIND)
    measure = PAGE.measurement(look, BLIND)
    assert look["faces"] == SLIT["faces"] and look["verdict"] == "LAWFUL" and measure["through"] == 3
    assert measure["nodes"] == SCREEN["positions"] and measure["rises"] == [0, 0, 0, 1, 2, 0, 0, 0, 0]
    counted = COUNTS.rises([x for fr in look["frames"] for x in fr["lines"]], "screen", "charge", (1, 2))
    assert [counted.get(tuple(n), 0) for n in measure["nodes"]] == measure["rises"]
    assert measure["blind"] == BLIND["counts"] and measure["pattern"] == [1, 7]
    assert measure["totals"] == "through 3 reported (the blind 10)"
    assert measure["watch"] == ["y = 4: 2 reported, the blind 2", "y = 3: 1 reported, the blind 1.5"]
    assert PAGE.embedded(measure) in html and PAGE.packed(look) in html
    assert "the faces (declared)" in html and "<title>Slit look</title>" in html
