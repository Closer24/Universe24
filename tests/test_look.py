"""The look's viewer (docs/ENGINE.md #6-how-to-run-a-world): the host reader writes one diagnostic file per world and the page builder one page from it, generic for any world; a smoke test on the chain, and the slit's screen read per region against an expectation in tools/click_counts.py's format."""

import json

from event_universe import world_files
from event_universe.loader.derived import count_wall
from event_universe.world_files import load_world
from tests.laws import CHAIN, RECORD, ROOT, SLIT, TOOL, chain_body_world, load_file, refused, slit_world

PAGE = load_file("look_page", ROOT / "tools" / "look" / "page.py")
COUNTS = load_file("click_counts", ROOT / "tools" / "click_counts.py")
NARROW = [[[20, 4, 0]], [[20, 4, 0], [20, 5, 0]], [[20, y, 0] for y in (0, 1, 6, 7)]]  # the size rule
REASONS = ("never one Node", "under half the wavelength", "not one connected region")
REFUSED = [([{"name": "n", "positions": at}], why) for at, why in zip(NARROW, REASONS, strict=True)]
SCREEN = [{"name": f"s{y}", "positions": [[20, y + r, 0] for r in range(4 + (y == 4))]} for y in (0, 4)]
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
    """(a) The look of the chain over three intervals (one body of 50 quanta at the Node 36: under the top mode on the board as declared a lone body spans 10 Nodes carrying a quantum, and two such bodies on this chain of 48 stand apart at no separation, the first's share sliding into the second's well round by round, its Nodes 14..18 then 16..26 then 17..26 about the declared 16 at 20 Links, until their regions share a Node and the generator refuses the pair by name as one body; a GameBoard finding of the generator's lay, the two-body chain of 12 Links having stood only under the cut mode): the label, the file's families, per frame every array sized to the board, frame 0 the record's share in quanta, the bodies' declared counts in all (the gate admitted them within the share's rounding), each click line in its interval's frame (one per interval from the test's own GameBoard), no inner face, the books; (b) the page: the label, the roles from the file's rows (the holder of the sign light, a holder of the content a field, a holder of nothing matter, a further one dashed), the blind file's window, the per-detector bars of an expectation without an axis, and no interpolation between Nodes. The slit world with a screen of two regions at x = 20 (the rows 0 to 3 and 4 to 8, never one Node: a click reports its region, and the loader refuses by name one Node, a region narrower than half the wavelength across the beam and a region in two pieces), three intervals with the test's own click lines of one quantum each (two on the upper region and one on the lower within the window [1, 2], one beyond it): the look holds the faces as declared; the page's measurement holds one bar per region ordered by its first row, what each saw summed exactly as tools/click_counts.py sums it, N over the wall to the nearest whole and the rounded shares, the blind counts, the pattern's range, the totals line and the watch lines naming the coordinate; the page embeds it with the look (the faces' cubes) and names the faces' layer; two further regions of four rows at x = 21 to 22 are each one reporter placed at their first row, on the page and in tools/click_counts.py (named, or every declared region over the whole run where the expectation names none), which reads beside the rounded shares (the expectation) the clicks (one draw by the seed), each row's extrema (the one rule of the builder and the reader: above the left neighbour and at or above the right a maximum, below and at or below a minimum, the row's ends neither), visibility at the blind `central` (the middle blind maximum where it names none) and deviation from the blind row's shares, the arrival of the screen's inflow in the engine's labels over every interval of the window, the negative ones included (the peak, the centroid, the half-maximum span), and a bare region named `aside`; a region's seen inflow is floored at 0 before the shares, the instrument's declaration. (c) A gate's page: with the joint-share reader's file over the gate's worlds (the look's world among them) and a blind of the gate's form, the page embeds the reading, another gate's blind beside it and the gate panels' script; without a reading no panel and no marker remains, the page as before; a reading without the look's world is refused by name."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL, at=(36,), taker=True)  # one body: a pair slides into one
    blind = {"expected": {"taker": 3}, "family": "charge", "window": [1, 2]}
    gate = {**blind, "sides": {"a": "left"}, "order": ["a"], "runs": {"a": "chain"}}
    gate.update(blind={"S": [1, 1]}, combination={"name": "S", "signs": [1]})
    look, html = shown(world, monkeypatch, {t: ["taker"] for t in (1, 2, 3)}, gate)
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
    roles, held = PAGE.roles(look["families"]), [f.get("held", {}).get("sources") for f in universe]
    expected = ["matter" if s is None else "light" if "wronskian" in s else "field" for s in held]
    assert [role["role"] for role in roles.values()] == expected
    dashed = [name for name, role in roles.items() if role["dashed"]]
    assert dashed == [f["name"] for f in universe if "held" not in f][1:]
    assert "GameBoard reading" in html and PAGE.embedded(roles) in html and '"window":[1,2]' in html
    assert '"measurement" type="application/json">null<' in html and "interpolat" not in html.lower()
    assert PAGE.measurement(look, blind) is None and "<title>Chain look</title>" in html
    assert PAGE.packed(look) in html and "DecompressionStream" in html  # the look inflated at load
    reading = {"worlds": {"chain": {}}, "S": [1, 1]}
    gated = PAGE.page(look, gate, reading, other := PAGE.beside(world.with_suffix(".blind.json")))
    assert PAGE.embedded(PAGE.gate(look, gate, reading)) in gated and PAGE.embedded(other) in gated
    assert "drawGate();" in gated and "gate-reading" not in html and "{{" not in html
    refused("not among the reading's worlds", PAGE.page, look, gate, {"worlds": {}})
    cells = [(21 + c // 4, c % 4) for c in range(8)]
    groups = [{"name": f"g{y}", "positions": [[x, y + r, 0] for x, r in cells]} for y in (0, 4)]
    world = slit_world(tmp_path, TOOL, detectors=[*SCREEN, *groups])
    pair = slit_world(tmp_path, TOOL, "pair", detectors=groups)
    for detectors, reason in REFUSED:
        refused(reason, load_world, slit_world(tmp_path, TOOL, "n", detectors=detectors))
    at = {1: ["s4", "g4"], 2: ["s0", "s4", "g0"], 3: ["s4", "g4"]}
    look, html = shown(world, monkeypatch, at, BLIND)
    measure = PAGE.measurement(look, BLIND)
    wall = next(f["wall"] for f in look["families"] if f["name"] == "charge")
    assert look["faces"] == SLIT["faces"] and look["verdict"] == "LAWFUL" and measure["quanta"] == 3
    assert measure["at"] == [0, 4] and measure["rounded_shares"] == [1, 2]
    assert measure["seen"] == [wall, 2 * wall] and measure["labels"] == BLIND["detector"]
    flat = [x for fr in look["frames"] for x in fr["lines"]]
    assert list(COUNTS.inflows(flat, BLIND["detector"], "charge", (1, 2)).values()) == measure["seen"]
    assert measure["totals"] == "N 3 by the shares (the blind 10)" and measure["pattern"] == [0, 1]
    watch = [f"y = {y}: {n} by the shares, the blind {b}" for y, n, b in ((4, 2, 2), (0, 1, 1.5))]
    assert measure["watch"] == watch and measure["blind"] == BLIND["counts"]
    assert PAGE.embedded(measure) in html and "the faces (declared)" in html
    grouped = {**BLIND, "detector": ["g4", "g0"], "counts": [1, 2], "aside": ["s0"]}
    grouped.update(maxima=[1], minima=[0], visibility=1)
    measure = PAGE.measurement(look, grouped)
    assert [measure[k] for k in ("at", "labels", "rounded_shares")] == [[0, 4], ["g0", "g4"], [1, 1]]
    (output := tmp_path / "slit.output.json").write_text(json.dumps({"ticks": 3, "lines": flat}))
    (tmp_path / "grouped.json").write_text(json.dumps(grouped))
    read = COUNTS.reading(world, output, tmp_path / "grouped.json")
    assert read["at"] == [0, 4] and read["seen"] == [wall, wall] and read["quanta"] == 2
    shares, clicks = read["rounded_shares"], read["clicks"]
    assert shares["deviation"] == [1, 3] and shares["row"] == [1, 1] and read["seed"] == 7
    assert sum(clicks["row"]) == 2 and shares["maxima"] == [] and shares["visibility"] == [0, 2]
    assert read["arrival"] == {"peak": 1, "centroid": [3, 2], "span": [1, 2]} and not read["floored"]
    assert read["aside"] == {"s0": {"seen": wall, "quanta": 1}}
    assert COUNTS.apportioned(10, [3, 1]) == [8, 2] and sum(COUNTS.drawn(10, [3, 1], 7)) == 10
    blind = {"pattern": [0, 3], "maxima": [0, 2, 3], "minima": [1], "counts": [1, 1, 1, 1]}
    rows = [COUNTS.read_row([5, 1, 4, 2], b) for b in ({**blind, "central": 0}, blind)]
    assert [(r["maxima"], r["minima"]) for r in rows] == [([2], [1])] * 2  # the ends 0 and 3 are neither
    assert [r["visibility"] for r in rows] == [[4, 6], [3, 5]]  # `central` read; else the middle maximum
    assert COUNTS.arrival({1: 3, 2: -1, 3: 2}) == {"peak": 1, "centroid": [7, 4], "span": [1, 3]}
    unnamed = {k: v for k, v in grouped.items() if k not in ("detector", "window", "aside")}
    (tmp_path / "unnamed.json").write_text(json.dumps(unnamed))
    every = COUNTS.reading(pair, output, tmp_path / "unnamed.json")
    assert every["detector"] == ["g0", "g4"] and every["rounded_shares"]["row"] == [1, 2]
    assert every["window"] == [0, 3] and PAGE.measurement(look, unnamed)["rounded_shares"][:2] == [1, 1]
