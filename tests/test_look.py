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
ROLE_OF = {(True, True): "light", (True, False): "field"}  # (held, by the Wronskian), else matter
REFUSED = [([[20, 4, 0]], "never one Node"), ([[20, 4, 0], [20, 5, 0]], "under half the wavelength")]
REFUSED += [([[20, y, 0] for y in (0, 1, 6, 7)], "not one connected region")]  # the size rule's refusals
SCREEN = [
    {"name": f"screen {y}", "positions": [[20, y + r, 0] for r in range(4 + (y == 4))]} for y in (0, 4)
]
BLIND = {"detector": [d["name"] for d in SCREEN], "family": "charge", "window": [1, 2], "across": "y"}
BLIND.update(pattern=[0, 1], counts=[1.5, 2], through=10, watch={"4": 2, "0": 1.5}, seed=7)


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
    declared, read = sum(b["declared"] for b in look["bodies"]), sum(x[0][0] for a in laid for x in a)
    assert ((abs(declared - read) - 1) // 2) ** 2 <= declared and "holds" not in look["bodies"][0]
    assert all(line["tick"] == t for t, frame in enumerate(look["frames"]) for line in frame["lines"])
    wall, frames = next(f["wall"] for f in look["families"] if f["name"] == "charge"), look["frames"]
    own = [[x for x in fr["lines"] if x["detector"] == "taker" and x["inflow"] == wall] for fr in frames]
    assert [len(lines) for lines in own] == [0, 1, 1, 1]  # the test's own clicks, one per interval
    engine = [x for fr in frames for x in fr["lines"] if x not in [y for z in own for y in z]]
    ends = ("left", "right", "taker", "face")  # the engine's reports: a region and an inflow, no Node
    assert engine and all(x["event"] == "click" and x["detector"] in ends for x in engine)
    assert all("node" not in x and x["inflow"] != 0 for x in engine)
    assert set(look["books"]) == {f["name"] for f in look["families"] if f["quanta"]}
    roles = PAGE.roles(look["families"])
    for family, role in zip(universe, roles.values(), strict=True):
        shape = ("held" in family, "wronskian" in family.get("held", {}).get("sources", []))
        assert role["role"] == ROLE_OF.get(shape, "matter")
    dashed = [name for name, role in roles.items() if role["dashed"]]
    assert dashed == [f["name"] for f in universe if "held" not in f][1:]
    assert "GameBoard reading" in html and PAGE.embedded(roles) in html and '"window":[1,2]' in html
    assert '"measurement" type="application/json">null<' in html and "interpolat" not in html.lower()
    assert PAGE.measurement(look, blind) is None and "<title>Chain look</title>" in html
    assert PAGE.packed(look) in html and "DecompressionStream" in html  # the look inflated at load


def test_the_page_draws_the_screen_per_region_with_the_blind_curve_and_the_faces(tmp_path, monkeypatch):
    """The slit world with a screen of two regions at x = 20 (the rows 0 to 3 and 4 to 8, never one Node: a click reports its region, and the loader refuses by name one Node, a region narrower than half the wavelength across the beam and a region in two pieces), three intervals with the test's own click lines of one quantum each (two on the upper region and one on the lower within the window [1, 2], one beyond it): the look holds the faces as declared; the page's measurement holds one bar per region ordered by its first row, what each saw summed exactly as tools/click_counts.py sums it, N over the wall to the nearest whole and the rounded shares, the blind counts, the pattern's range, the totals line and the watch lines naming the coordinate; the page embeds it with the look (the faces' cubes) and names the faces' layer; two further regions of four rows at x = 21 to 22 are each one reporter placed at their first row, on the page and in tools/click_counts.py (named, or every declared region over the whole run where the expectation names none), which reads beside the rounded shares (the expectation) the clicks (one draw by the seed), each row's extrema, visibility and deviation from the blind row's shares, the arrival of the screen's inflow in the engine's labels (the peak, the centroid, the half-maximum span) and a bare region named `aside`; a region's seen inflow is floored at 0 before the shares, the instrument's declaration."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    cells = [(21 + c // 4, c % 4) for c in range(8)]
    groups = [{"name": f"g{y}", "positions": [[x, y + r, 0] for x, r in cells]} for y in (0, 4)]
    world = slit_world(tmp_path, TOOL, detectors=[*SCREEN, *groups])
    pair = slit_world(tmp_path, TOOL, "pair", detectors=groups)
    for nodes, reason in REFUSED:
        with pytest.raises(ValueError, match=reason):
            load_world(slit_world(tmp_path, TOOL, "n", detectors=[{"name": "n", "positions": nodes}]))
    at = {1: ["screen 4", "g4"], 2: ["screen 0", "screen 4", "g0"], 3: ["screen 4", "g4"]}
    look, html = shown(world, monkeypatch, at, BLIND)
    measure = PAGE.measurement(look, BLIND)
    wall = next(f["wall"] for f in look["families"] if f["name"] == "charge")
    assert look["faces"] == SLIT["faces"] and look["verdict"] == "LAWFUL" and measure["quanta"] == 3
    assert measure["at"] == [0, 4] and measure["rounded_shares"] == [1, 2]
    assert measure["seen"] == [wall, 2 * wall] and measure["labels"] == BLIND["detector"]
    flat = [x for fr in look["frames"] for x in fr["lines"]]
    counted = COUNTS.inflows(flat, BLIND["detector"], "charge", (1, 2))
    assert [counted[name] for name in BLIND["detector"]] == measure["seen"]
    assert measure["blind"] == BLIND["counts"] and measure["pattern"] == [0, 1]
    assert measure["totals"] == "N 3 by the shares (the blind 10)"
    watch = [f"y = {y}: {n} by the shares, the blind {b}" for y, n, b in ((4, 2, 2), (0, 1, 1.5))]
    assert measure["watch"] == watch
    assert PAGE.embedded(measure) in html and PAGE.packed(look) in html
    assert "the faces (declared)" in html and "<title>Slit look</title>" in html
    grouped = {**BLIND, "detector": ["g4", "g0"], "counts": [1, 2], "aside": ["screen 0"]}
    grouped.update(maxima=[1], minima=[0], visibility=1)
    measure = PAGE.measurement(look, grouped)
    assert measure["at"] == [0, 4] and measure["labels"] == ["g0", "g4"]
    assert measure["rounded_shares"] == [1, 1]
    output = tmp_path / "slit.output.json"
    output.write_text(json.dumps({"ticks": 3, "lines": flat}))
    (tmp_path / "grouped.json").write_text(json.dumps(grouped))
    read = COUNTS.reading(world, output, tmp_path / "grouped.json")
    assert read["at"] == [0, 4] and read["seen"] == [wall, wall] and read["quanta"] == 2
    shares, clicks = read["rounded_shares"], read["clicks"]
    assert shares["deviation"] == [1, 3] and shares["row"] == [1, 1] and read["seed"] == 7
    assert sum(clicks["row"]) == 2 and shares["maxima"] == [] and shares["visibility"] == [0, 2]
    assert read["arrival"] == {"peak": 1, "centroid": [3, 2], "span": [1, 2]} and not read["floored"]
    assert read["aside"] == {"screen 0": {"seen": wall, "quanta": 1}}
    assert COUNTS.apportioned(10, [3, 1]) == [8, 2] and sum(COUNTS.drawn(10, [3, 1], 7)) == 10
    unnamed = {k: v for k, v in grouped.items() if k not in ("detector", "window", "aside")}
    (tmp_path / "unnamed.json").write_text(json.dumps(unnamed))
    every = COUNTS.reading(pair, output, tmp_path / "unnamed.json")
    assert every["detector"] == ["g0", "g4"] and every["rounded_shares"]["row"] == [1, 2]
    assert every["window"] == [0, 3]
    assert PAGE.measurement(look, unnamed)["rounded_shares"][:2] == [1, 1]  # the screen's regions first
