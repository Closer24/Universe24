"""The look's viewer (docs/ENGINE.md #6-how-to-run-a-world): the host reader writes one diagnostic file per world and the page builder one page from it, generic for any world; a smoke test on the chain, and the slit's screen read per Node against an expectation in tools/click_counts.py's format."""

from __future__ import annotations

import json

import pytest

from event_universe import world_files
from event_universe.world_files import load_world
from tests.laws import CHAIN, ROOT, SLIT, chain_body_world, load_file, slit_world

TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
RECORD = load_file("look_record", ROOT / "tools" / "look" / "record.py")
PAGE = load_file("look_page", ROOT / "tools" / "look" / "page.py")
COUNTS = load_file("click_counts", ROOT / "tools" / "click_counts.py")
BELL = load_file("bell_clicks", ROOT / "tools" / "bell_clicks.py")
BUILD = load_file("bell_build", ROOT / "examples" / "events" / "bell" / "build_world.py")
ROLE_OF = {"sign": "light", "content": "field"}  # a holder of nothing is matter
SCREEN = [
    {"name": f"screen {y}", "positions": [[20, r, 0] for r in range(y, y + 4 + (y == 4))]}
    for y in (0, 4)
]
BLIND = {"detector": [d["name"] for d in SCREEN], "family": "charge", "window": [1, 2], "across": "y"}
BLIND.update(pattern=[0, 1], counts=[1.5, 2], through=10, watch={"4": 2, "0": 1.5}, seed=7)
BELL_FILES, LINKS = ("bell_0", "bell_1", "expectation"), [0, 6, 12, 18, 24]  # the builder's files


def shown(world, monkeypatch, at, blind):
    """The look of `world` over three intervals from a GameBoard that clicks on the detectors `at` names per interval (a click names its region and the Port crossed, never a Node; the worlds here do not click by themselves within three intervals), the blind file written beside it, and the page built from both."""

    class Clicking(RECORD.GameBoard):
        def step(self) -> None:
            super().step()
            for name in at.get(self.tick, []):
                line = {"event": "click", "tick": self.tick, "family": "charge", "detector": name}
                self.observer({**line, "ports": [[0, -1]], "count": 1, "body": None})

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
    look, html = shown(world, monkeypatch, {t: ["taker"] for t in (1, 2, 3)}, blind)
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


def test_the_page_draws_the_screen_per_region_with_the_blind_curve_and_the_faces(tmp_path, monkeypatch):
    """The slit world with a screen of two regions at x = 20 (the rows 0 to 3 and 4 to 8, never one Node: a click reports its region, and the loader refuses a region narrower than half the wavelength), three intervals with the test's own click lines (two on the upper region and one on the lower within the window [1, 2], one beyond it): the look holds the faces as declared; the page's measurement holds one bar per region ordered by its first row, the entries counted per region exactly as tools/click_counts.py counts them, the blind counts, the pattern's range, the totals line and the watch lines naming the coordinate; the page embeds it with the look (the faces' cubes) and names the faces' layer; two further regions of four rows at x = 21 to 22 are each one reporter placed at their first row, on the page and in tools/click_counts.py (named, or every declared region over the whole run where the expectation names none), which reads beside the entries the summed absolute deviation from the blind row's shares, the credit from what the regions saw (N over the wall, the clicks credited by the shares and one draw by the seed) and a bare region named `aside`; tools/bell_clicks.py reads the runs by the comb per region (the weights, the marginals, E as the product, S, the curve) and Bell's builder writes from its design file one world per angle with the expectation."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    groups = [
        {"name": f"g{y}", "positions": [[x, r, 0] for x in (21, 22) for r in range(y, y + 4)]}
        for y in (0, 4)
    ]
    world = slit_world(tmp_path, TOOL, detectors=[*SCREEN, *groups])
    pair = slit_world(tmp_path, TOOL, "pair", detectors=groups)
    with pytest.raises(ValueError, match="under half the wavelength"):
        load_world(
            slit_world(tmp_path, TOOL, "narrow", detectors=[{"name": "n", "positions": [[20, 4, 0]]}])
        )
    at = {1: ["screen 4", "g4"], 2: ["screen 0", "screen 4", "g0"], 3: ["screen 4", "g4"]}
    look, html = shown(world, monkeypatch, at, BLIND)
    measure = PAGE.measurement(look, BLIND)
    assert look["faces"] == SLIT["faces"] and look["verdict"] == "LAWFUL" and measure["through"] == 3
    assert (
        measure["at"] == [0, 4] and measure["rises"] == [1, 2] and measure["labels"] == BLIND["detector"]
    )
    flat = [x for fr in look["frames"] for x in fr["lines"]]
    counted = COUNTS.rises(flat, BLIND["detector"], "charge", (1, 2))
    assert [counted.get(name, 0) for name in BLIND["detector"]] == measure["rises"]
    assert measure["blind"] == BLIND["counts"] and measure["pattern"] == [0, 1]
    assert measure["totals"] == "through 3 reported (the blind 10)"
    assert measure["watch"] == ["y = 4: 2 reported, the blind 2", "y = 0: 1 reported, the blind 1.5"]
    assert PAGE.embedded(measure) in html and PAGE.packed(look) in html
    assert "the faces (declared)" in html and "<title>Slit look</title>" in html
    grouped = {**BLIND, "detector": ["g4", "g0"], "counts": [1, 2], "aside": ["screen 0"]}
    grouped.update(maxima=[1], minima=[0], visibility=1)
    measure = PAGE.measurement(look, grouped)
    assert measure["at"] == [0, 4] and measure["labels"] == ["g0", "g4"] and measure["rises"] == [1, 1]
    saw = [
        {"event": "seen", "tick": 1, "family": "charge", "detector": d, "inflow": n}
        for d, n in (("g0", 7), ("g4", 7), ("screen 0", 13))
    ]
    (output := tmp_path / "slit.output.json").write_text(
        json.dumps({"ticks": 3, "lines": [*flat, *saw]})
    )
    (tmp_path / "grouped.json").write_text(json.dumps(grouped))
    read = COUNTS.reading(world, output, tmp_path / "grouped.json")
    assert read["at"] == [0, 4] and read["rises"] == [1, 1] and read["through"] == 2
    assert read["deviation"] == [1, 3] and read["seen"] == [7, 7] and read["quanta"] == 0
    assert read["credited"] == [0, 0] and read["drawn"] == [0, 0] and read["seed"] == 7
    assert read["aside"] == {"screen 0": {"seen": 13, "quanta": 0, "entries": 1}}
    assert COUNTS.apportioned(10, [3, 1]) == [8, 2] and sum(COUNTS.drawn(10, [3, 1], 7)) == 10
    unnamed = {k: v for k, v in grouped.items() if k not in ("detector", "window", "aside")}
    (tmp_path / "unnamed.json").write_text(json.dumps(unnamed))
    every = COUNTS.reading(pair, output, tmp_path / "unnamed.json")
    assert every["detector"] == ["g0", "g4"] and every["rises"] == [1, 2] and every["window"] == [0, 3]
    assert PAGE.measurement(look, unnamed)["rises"][:2] == [1, 1]  # the screen's regions first
    bell = {"family": "charge", "sides": {"left": {"g0": [0, 1, 2, 3]}, "right": {"g4": [4, 5, 6, 7]}}}
    bell.update(
        spacing=8, fringe_centre=1, settings={"a": [0, 4], "b": [0, 4]}, curve={"links": [0, 2, 4]}
    )
    bell.update(sign="left", contrast="right")  # A credits by the sign, B by the contrast
    (tmp_path / "bell.json").write_text(json.dumps(bell))
    loaded = BELL.load_world(pair)
    wall = BELL.count_wall(next(f for f in loaded.families if f.name == "charge"), loaded.quantum_action)
    big = [
        {"event": "seen", "tick": 1, "family": "charge", "detector": d, "inflow": n * wall}
        for d, n in (("g0", 3), ("g4", 2))
    ]  # three quanta at A, two at B: the two coincide, the third has no partner
    (bell_out := tmp_path / "bell.output.json").write_text(
        json.dumps({"ticks": 3, "lines": [*flat, *big]})
    )
    runs = BELL.reading(pair, [bell_out], tmp_path / "bell.json")
    run = runs["per_run"][0]  # the comb + on the rows 0 to 3 at the setting 0 and on 4 to 7 at 4
    assert run["outcome"] == {"left": [1, -1], "right": [-1, 1]} and run["side_quanta"] == {
        "left": 3,
        "right": 2,
    }
    assert run["contrast"] == {"left": [[1, 1], [1, 1]], "right": [[1, 1], [1, 1]]}
    assert run["clicks"] == {"left": [[3, 1], [3, 1]], "right": [[2, 1], [2, 1]]}
    assert runs["correlation"] == {"0 0": [-1, 1], "0 4": [1, 1], "4 0": [1, 1], "4 4": [-1, 1]}
    assert (
        runs["S"] == [-2, 1]
        and runs["runs"] == 1
        and runs["by"] == {"left": "sign", "right": "contrast"}
    )
    assert runs["efficiency"] == {"left": [[1, 1], [1, 1]], "right": [[1, 1], [1, 1]]}
    assert runs["curve"] == [[-1, 1], [0, 1], [1, 1]] and runs["curve_at"]["4"] == [1, 1]  # a tie at 2
    assert runs["by_the_shares"] == {
        "correlation": {"0 0": [-1, 1], "0 4": [1, 1], "4 0": [1, 1], "4 4": [-1, 1]},
        "S": [-2, 1],
    }
    assert runs["entries"] == {"left": {"g0": 1}, "right": {"g4": 2}}
    assert runs["patterns"] == {"left": {"g0": 3}, "right": {"g4": 2}}
    with pytest.raises(ValueError, match="declares"):
        (tmp_path / "bad.json").write_text(json.dumps({**bell, "contrast": "left"}))
        BELL.reading(pair, [bell_out], tmp_path / "bad.json")
    BUILD.main(["--folder", str(folder := tmp_path / "bell")])
    built, tilted, blind = (json.loads((folder / f"{n}.json").read_text()) for n in BELL_FILES)
    assert built["shape"] == [360, 96, 1] and built["ticks"] == 520 and len(built["messages"]) == 4
    assert (
        len(built["detectors"]) == 46 and len(blind["runs"]) == 8 and len(blind["sides"]["left"]) == 23
    )
    still = json.loads((folder / "bell_v.json").read_text())  # the visibility world, u = 0
    assert [m.get("phase") for m in still["messages"]] == [None] * 4 and blind[
        "visibility_world"
    ] == "bell_v"
    assert [m.get("phase") for m in built["messages"]] == [
        None,
        [15, 16],
        None,
        [1, 16],
    ]  # the half-offset
    assert [m.get("phase") for m in tilted["messages"]] == [None, [13, 16], None, [3, 16]]  # the mirror
    assert [m["top"]["x"][0] for m in built["messages"]] == [120, 120, 240, 240]
    assert blind["settings"] == {"a": [0, 12], "b": [-6, -18]} and blind["curve"]["links"] == LINKS
    assert blind["sign"] == "left" and blind["contrast"] == "right"
    assert max(max(rows) for rows in blind["sides"]["right"].values()) == 95
    assert [len(rows) for rows in blind["sides"]["right"].values()] == [7] + [4] * 21 + [5]
    assert [len(rows) for rows in blind["sides"]["left"].values()] == [5] + [4] * 21 + [7]
    assert {p[0] for d in built["detectors"] if d["name"] == "right_0" for p in d["positions"]} == set(
        range(348, 360)
    )
