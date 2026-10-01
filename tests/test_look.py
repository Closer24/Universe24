"""The look's viewer (docs/ENGINE.md #6-how-to-run-a-world): the host reader writes one diagnostic file per world and the page builder one page from it, generic for any world; a smoke test on the chain, and the slit's screen read per region against an expectation in tools/click_counts.py's format."""

from __future__ import annotations

import json

import pytest

from event_universe import world_files
from event_universe.loader.derived import count_wall
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
    {"name": f"screen {y}", "positions": [[20, y + r, 0] for r in range(4 + (y == 4))]} for y in (0, 4)
]
BLIND = {"detector": [d["name"] for d in SCREEN], "family": "charge", "window": [1, 2], "across": "y"}
BLIND.update(pattern=[0, 1], counts=[1.5, 2], through=10, watch={"4": 2, "0": 1.5}, seed=7)
BELL_FILES, BELL_REGIONS = ("bell_0", "bell_1", "expectation"), ("g0", "g4", "screen 0", "screen 4")
SCREEN_PORTS = {"plus": ["screen 0"], "minus": ["screen 4"]}  # the toy right side's ports


def shown(world, monkeypatch, at, blind):
    """The look of `world` over three intervals from a GameBoard that clicks on the detectors `at` names per interval, each click one quantum's inflow, W_c (a click names its region and never a Node; the worlds here do not click by themselves within three intervals), the blind file written beside it, and the page built from both."""

    class Clicking(RECORD.GameBoard):
        def step(self) -> None:
            super().step()
            charge = next(f for f in self.families if f.name == "charge")
            wall = count_wall(charge, self.world.quantum_action)
            for name in at.get(self.tick, []):
                line = {"event": "click", "tick": self.tick, "family": "charge", "detector": name}
                self.observer({**line, "inflow": wall})

    monkeypatch.setattr(RECORD, "GameBoard", Clicking)
    RECORD.main([str(world), "--ticks", "3"])
    world.with_suffix(".blind.json").write_text(json.dumps(blind), encoding="utf-8")
    PAGE.main([str(world.with_suffix(".look.json")), "--blind", str(world.with_suffix(".blind.json"))])
    look = json.loads(world.with_suffix(".look.json").read_text(encoding="utf-8"))
    return look, world.with_suffix(".look.html").read_text(encoding="utf-8")


def test_the_reader_writes_the_look_and_the_page_shows_it_with_the_roles(tmp_path, monkeypatch):
    """(a) The look of the chain over three intervals: the label, the file's families, per frame every array sized to the board, frame 0 the record's share in quanta, the bodies' declared counts in all (the gate admitted them within the share's rounding), each click line in its interval's frame (one per interval from the test's own GameBoard), no inner face, the books; (b) the page: the label, the roles from the file's rows (the holder of the sign light, a holder of the content a field, a holder of nothing matter, a further one dashed), the blind file's window, the per-detector bars of an expectation without an axis, and no interpolation between Nodes."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL, at=(24, 40), taker=True)
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
    declared = sum(b["declared"] for b in look["bodies"])
    assert sum(x[0][0] for a in laid for x in a) == declared and "holds" not in look["bodies"][0]
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
    """The slit world with a screen of two regions at x = 20 (the rows 0 to 3 and 4 to 8, never one Node: a click reports its region, and the loader refuses a region narrower than half the wavelength), three intervals with the test's own click lines of one quantum each (two on the upper region and one on the lower within the window [1, 2], one beyond it): the look holds the faces as declared; the page's measurement holds one bar per region ordered by its first row, what each saw summed exactly as tools/click_counts.py sums it, N over the wall and the clicks credited by the shares, the blind counts, the pattern's range, the totals line and the watch lines naming the coordinate; the page embeds it with the look (the faces' cubes) and names the faces' layer; two further regions of four rows at x = 21 to 22 are each one reporter placed at their first row, on the page and in tools/click_counts.py (named, or every declared region over the whole run where the expectation names none), which reads beside the credit the summed absolute deviation from the blind row's shares, one draw by the seed and a bare region named `aside`; tools/bell_clicks.py reads the runs by the comb per region (the weights, the marginals, E as the product, S, the curve) and Bell's builder writes from its design file one world per angle with the expectation."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    groups = [
        {"name": f"g{y}", "positions": [[x, y + r, 0] for x in (21, 22) for r in range(4)]}
        for y in (0, 4)
    ]
    world = slit_world(tmp_path, TOOL, detectors=[*SCREEN, *groups])
    pair = slit_world(tmp_path, TOOL, "pair", detectors=groups)
    narrow = [{"name": "n", "positions": [[20, 4, 0]]}]
    with pytest.raises(ValueError, match="under half the wavelength"):
        load_world(slit_world(tmp_path, TOOL, "narrow", detectors=narrow))
    at = {1: ["screen 4", "g4"], 2: ["screen 0", "screen 4", "g0"], 3: ["screen 4", "g4"]}
    look, html = shown(world, monkeypatch, at, BLIND)
    measure = PAGE.measurement(look, BLIND)
    wall = next(f["wall"] for f in look["families"] if f["name"] == "charge")
    assert look["faces"] == SLIT["faces"] and look["verdict"] == "LAWFUL" and measure["quanta"] == 3
    assert (
        measure["at"] == [0, 4] and measure["credited"] == [1, 2] and measure["seen"] == [wall, 2 * wall]
    )
    assert measure["labels"] == BLIND["detector"]
    flat = [x for fr in look["frames"] for x in fr["lines"]]
    counted = COUNTS.inflows(flat, BLIND["detector"], "charge", (1, 2))
    assert [counted[name] for name in BLIND["detector"]] == measure["seen"]
    assert measure["blind"] == BLIND["counts"] and measure["pattern"] == [0, 1]
    assert measure["totals"] == "N 3 credited (the blind 10)"
    assert measure["watch"] == ["y = 4: 2 credited, the blind 2", "y = 0: 1 credited, the blind 1.5"]
    assert PAGE.embedded(measure) in html and PAGE.packed(look) in html
    assert "the faces (declared)" in html and "<title>Slit look</title>" in html
    grouped = {**BLIND, "detector": ["g4", "g0"], "counts": [1, 2], "aside": ["screen 0"]}
    grouped.update(maxima=[1], minima=[0], visibility=1)
    measure = PAGE.measurement(look, grouped)
    assert (
        measure["at"] == [0, 4] and measure["labels"] == ["g0", "g4"] and measure["credited"] == [1, 1]
    )
    output = tmp_path / "slit.output.json"
    output.write_text(json.dumps({"ticks": 3, "lines": flat}))
    (tmp_path / "grouped.json").write_text(json.dumps(grouped))
    read = COUNTS.reading(world, output, tmp_path / "grouped.json")
    assert read["at"] == [0, 4] and read["seen"] == [wall, wall] and read["quanta"] == 2
    assert read["deviation"] == [1, 3] and read["credited"] == [1, 1] and read["seed"] == 7
    assert sum(read["drawn"]) == 2 and read["maxima"] == [] and read["visibility"] == [0, 2]
    assert read["aside"] == {"screen 0": {"seen": wall, "quanta": 1}}
    assert COUNTS.apportioned(10, [3, 1]) == [8, 2] and sum(COUNTS.drawn(10, [3, 1], 7)) == 10
    unnamed = {k: v for k, v in grouped.items() if k not in ("detector", "window", "aside")}
    (tmp_path / "unnamed.json").write_text(json.dumps(unnamed))
    every = COUNTS.reading(pair, output, tmp_path / "unnamed.json")
    assert (
        every["detector"] == ["g0", "g4"] and every["credited"] == [1, 2] and every["window"] == [0, 3]
    )
    assert PAGE.measurement(look, unnamed)["credited"][:2] == [1, 1]  # the screen's regions first
    ports = {"plus": ["g0"], "minus": ["g4"]}
    bell = {"family": "charge", "sides": {"left": {"g0": [0, 1, 2, 3], "g4": [4, 5, 6, 7]}}}
    bell["sides"]["right"] = {"screen 0": [0, 1, 2, 3], "screen 4": [4, 5, 6, 7, 8]}
    bell["ports"] = {"left": {"0": ports, "4": ports}, "right": {k: SCREEN_PORTS for k in ("0", "4")}}
    bell.update(sign="left", contrast="right", settings={"left": [0, 4], "right": [0, 4]}, blind={})
    (tmp_path / "bell.json").write_text(json.dumps(bell))
    click = {"event": "click", "tick": 1, "family": "charge"}
    outs = []
    for name, quanta in (
        ("bell_0", (3, 1, 1, 2)),
        ("bell_1", (1, 3, 2, 1)),
    ):  # left +, left -, right +, right -
        big = [
            {**click, "detector": d, "inflow": n * wall}
            for d, n in zip(BELL_REGIONS, quanta, strict=True)
        ]
        outs.append(tmp_path / f"{name}.output.json")
        outs[-1].write_text(json.dumps({"input": f"{name}.json", "ticks": 3, "lines": big}))
    runs = BELL.reading(world, outs, tmp_path / "bell.json")
    run = runs["per_run"][0]  # the left's + port fuller in the first run, the right's - port
    assert run["outcome"] == {"left": {"0": 1, "4": 1}, "right": {"0": -1, "4": -1}}
    assert run["light"]["left"]["0"] == [4, 1] and run["contrast"]["right"]["4"] == [1, 1]
    assert runs["correlation"] == {"0 0": [-1, 1], "0 4": [-1, 1], "4 0": [-1, 1], "4 4": [-1, 1]}
    assert runs["S"] == [-2, 1] and runs["runs"] == ["bell_0", "bell_1"] and runs["visibility"] is None
    assert runs["efficiency"] == {s: {"0": [1, 1], "4": [1, 1]} for s in ("left", "right")}
    assert runs["by_the_shares"]["correlation"]["0 4"] == [-1, 1]
    assert runs["patterns"] == {"left": {"g0": 4, "g4": 4}, "right": {"screen 0": 3, "screen 4": 3}}
    with pytest.raises(ValueError, match="declares"):
        (tmp_path / "bad.json").write_text(json.dumps({**bell, "contrast": "left"}))
        BELL.reading(world, outs, tmp_path / "bad.json")
    BUILD.main(["--folder", str(folder := tmp_path / "bell")])
    built, tilted, blind = (json.loads((folder / f"{n}.json").read_text()) for n in BELL_FILES)
    assert built["shape"] == [343, 48, 1] and built["ticks"] == 400 and len(built["messages"]) == 4
    assert (
        len(built["detectors"]) == 23 and len(blind["runs"]) == 32 and len(blind["sides"]["left"]) == 12
    )
    still = json.loads((folder / "bell_v.json").read_text())  # the visibility world, u = 0
    assert [m.get("phase") for m in still["messages"]] == [None] * 4
    assert [m.get("phase") for m in built["messages"]] == [None, [63, 64], None, [1, 64]]  # the offset
    assert [m.get("phase") for m in tilted["messages"]] == [None, [61, 64], None, [3, 64]]  # the mirror
    assert [m["top"]["x"][0] for m in built["messages"]] == [111, 111, 231, 231]
    assert blind["settings"] == {"left": [-2, -6], "right": [0, 4]} and blind["degrees"]["left"] == [
        -45,
        -135,
    ]
    assert blind["ports"]["right"]["0"] == {"plus": ["right_5"], "minus": ["right_3", "right_7"]}
    assert [len(rows) for rows in blind["sides"]["right"].values()] == [6] + [4] * 9 + [6]
    assert blind["blind"]["minima"] == [16, 31] and 2.7 < blind["blind"]["S_cosines"] < 2.9
    right = next(d for d in built["detectors"] if d["name"] == "right_0")
    assert {p[0] for p in right["positions"]} == set(range(331, 343))
