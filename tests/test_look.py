"""The look's viewer (docs/ENGINE.md #6-how-to-run-a-world): the host reader writes one diagnostic file per world and the page builder one page from it, generic for any world; a smoke test on the chain, and the slit's screen read per Node against an expectation in tools/click_counts.py's format."""

from __future__ import annotations

import json

from event_universe import world_files
from tests.laws import CHAIN, ROOT, SLIT, chain_body_world, load_file, slit_world

TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
RECORD = load_file("look_record", ROOT / "tools" / "look" / "record.py")
PAGE = load_file("look_page", ROOT / "tools" / "look" / "page.py")
COUNTS = load_file("click_counts", ROOT / "tools" / "click_counts.py")
TRAIN = load_file("train_clicks", ROOT / "tools" / "train_clicks.py")
BELL = load_file("bell_clicks", ROOT / "tools" / "bell_clicks.py")
BUILD = load_file("bell_build", ROOT / "examples" / "events" / "bell" / "build_world.py")
ROLE_OF = {"sign": "light", "content": "field"}  # a holder of nothing is matter
SCREEN = {"name": "screen", "positions": [[20, y, 0] for y in range(9)]}
BLIND = {"detector": "screen", "family": "charge", "window": [1, 2], "across": "y", "pattern": [1, 7]}
BLIND.update(counts=[0, 1, 2, 4, 2, 1, 0, 0, 0], through=10, watch={"4": 2, "3": 1.5})


def shown(world, monkeypatch, detector, at, blind):
    """The look of `world` over three intervals from a GameBoard that clicks on `detector` at the Nodes `at` names per interval (a Node, or a tuple of a detector's name, a Node and optionally the whole the line names; the worlds here do not click by themselves in three intervals; the lines' placement and their counting is what is checked), and the page built from it with `blind` as its expectation file, as text."""

    class Clicking(RECORD.GameBoard):
        def step(self) -> None:
            super().step()
            for entry in at.get(self.tick, []):
                name, node, *whole = entry if isinstance(entry, tuple) else (detector, entry)
                line = {"event": "click", "tick": self.tick, "family": "charge", "detector": name}
                line.update(node=node, count=1, body=None, **({"whole": whole[0]} if whole else {}))
                self.observer(line)

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
    """The slit world with a screen of nine detector Nodes at x = 20, three intervals with the test's own click lines (two at y = 4 and one at y = 3 within the window [1, 2], one at y = 5 beyond it): the look holds the faces as declared; the page's measurement holds one row per screen Node ordered by y, the rises summed per Node exactly as tools/click_counts.py counts them, the blind counts, the pattern's range, the totals line and the watch lines naming the coordinate; the page embeds it with the look (the faces' cubes) and names the faces' layer; two detectors of two Nodes each sharing a y are each one reporter placed at it, on the page, in tools/click_counts.py (named, or every placed group over the whole run where the expectation names none) and in tools/train_clicks.py, whose reading gives each of two quanta the rises nearest its peak (the pace one Link an interval), the halves that rose and the rates, and in tools/bell_clicks.py, whose reading by the comb pairs the landings by the whole each click line names (the left packet's whole n with the right packet's whole n), gives each pair the outcomes of its landings at the settings, the correlation at the settings, S, the coincidences, E as a curve in a + b over every position and the coincidence map's ridge; tools/click_counts.py reads beside the rises the summed absolute deviation from the blind row's shares over the total and the wholes named on the lines (each one's first entry alone, none twice, none in two groups); Bell's first world's builder writes from its design file the world (400 x 48, 400 intervals, the two packets at x = 140 and 260) and the expectation (the mirrors, the settings and the curve's sums in Links)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    groups = [{"name": f"g{y}", "positions": [[21, y, 0], [22, y, 0]]} for y in (3, 4)]
    world = slit_world(tmp_path, TOOL, detectors=[SCREEN, *groups])
    at = {1: [[20, 4, 0], ("g4", [21, 4, 0], [1, 0])]}
    at[2] = [[20, 3, 0], [20, 4, 0], ("g3", [22, 3, 0], [0, 0])]
    at[3] = [[20, 5, 0], ("g4", [21, 4, 0], [1, 1])]
    look, html = shown(world, monkeypatch, "screen", at, BLIND)
    measure = PAGE.measurement(look, BLIND)
    assert look["faces"] == SLIT["faces"] and look["verdict"] == "LAWFUL" and measure["through"] == 3
    assert measure["nodes"] == SCREEN["positions"] and measure["rises"] == [0, 0, 0, 1, 2, 0, 0, 0, 0]
    flat = [x for fr in look["frames"] for x in fr["lines"]]
    counted = COUNTS.rises(flat, ["screen"], "charge", (1, 2))
    assert [counted.get(("screen", tuple(n)), 0) for n in measure["nodes"]] == measure["rises"]
    assert measure["blind"] == BLIND["counts"] and measure["pattern"] == [1, 7]
    assert measure["totals"] == "through 3 reported (the blind 10)"
    assert measure["watch"] == ["y = 4: 2 reported, the blind 2", "y = 3: 1 reported, the blind 1.5"]
    assert PAGE.embedded(measure) in html and PAGE.packed(look) in html
    assert "the faces (declared)" in html and "<title>Slit look</title>" in html
    grouped = {**BLIND, "detector": ["g4", "g3"], "counts": [1, 2], "pattern": [0, 1]}
    grouped.update(maxima=[1], minima=[0], visibility=1)
    measure = PAGE.measurement(look, grouped)
    assert measure["at"] == [3, 4] and measure["labels"] == ["g3", "g4"] and measure["rises"] == [1, 1]
    output = tmp_path / "slit.output.json"
    output.write_text(json.dumps({"ticks": 3, "lines": flat}))
    (tmp_path / "grouped.json").write_text(json.dumps(grouped))
    read = COUNTS.reading(world, output, tmp_path / "grouped.json")
    assert read["at"] == [3, 4] and read["rises"] == [1, 1] and read["through"] == 2
    assert read["deviation"] == [1, 3] and read["wholes"] == {"wholes": 3, "twice": 0, "two_groups": 0}
    unnamed = {k: v for k, v in grouped.items() if k not in ("detector", "window")}
    (tmp_path / "unnamed.json").write_text(json.dumps(unnamed))
    whole = COUNTS.reading(world, output, tmp_path / "unnamed.json")
    assert whole["detector"] == ["g3", "g4"] and whole["rises"] == [1, 2] and whole["window"] == [0, 3]
    assert PAGE.measurement(look, unnamed)["rises"] == [1, 2]
    train = {"family": "charge", "across": "y", "along": "x", "pace": [1, 1]}
    train.update(halves={"left": [0, 3], "right": [4, 8]})
    train["quanta"] = [{"peak": 1, "window": [1, 2]}, {"peak": 3, "window": [3, 4]}]
    (tmp_path / "train.json").write_text(json.dumps(train))
    rows = TRAIN.reading(world, output, tmp_path / "train.json")
    assert [q["rises"] for q in rows["quanta"]] == [2, 1] and rows["groups"] == [3, 4]
    assert [q["halves"] for q in rows["quanta"]] == [["left", "right"], ["right"]]
    assert rows["both"] == [1, 2] and rows["one"] == [1, 2] and rows["neither"] == [0, 2]
    assert rows["rises_per_quantum"] == [3, 2] and rows["per_group"] == [1, 2]
    bell = {**train, "sides": {"left": "g3", "right": "g4"}, "mirrors": [[0, 1]], "spacing": 4}
    bell.update(fringe_centre=3, settings={"a": [0, 2], "b": [1, 3]}, bins=4, curve={"links": [0, 1, 2]})
    (tmp_path / "bell.json").write_text(json.dumps(bell))
    pairs = BELL.reading(world, output, tmp_path / "bell.json")
    assert pairs["pairs"][0]["outcomes"] == {"left": [1, -1], "right": [1, -1]}
    assert pairs["pairs"][1]["outcomes"] == {"right": [1, -1]} and pairs["coincidences"] == 1
    assert pairs["correlation"] == {"0 1": [1, 1], "0 3": [-1, 1], "2 1": [-1, 1], "2 3": [1, 1]}
    assert pairs["S"] == [2, 1] and pairs["landings"] == {"left": 1, "right": 2}
    assert pairs["curve"] == [[0, 1], [1, 1], [0, 1], [0, 1]] and pairs["ridge"] == [0, 1, 0, 0]
    BUILD.main(["--folder", str(tmp_path / "bell")])
    built = json.loads((tmp_path / "bell" / "bell.json").read_text())
    blind = json.loads((tmp_path / "bell" / "expectation.json").read_text())
    assert built["shape"] == [400, 48, 1] and built["ticks"] == 400 and len(built["messages"]) == 2
    assert [m["top"]["x"][0] for m in built["messages"]] == [140, 260]
    assert blind["settings"] == {"a": [0, 4], "b": [-2, -6]} and blind["mirrors"] == [[0, 1]]
    assert blind["curve"]["links"] == [0, 2, 4, 6, 8] and blind["wholes"] == 3000
