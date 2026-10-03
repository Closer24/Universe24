"""The draw's experiments in the engine (the owner's word of 2026-10-03, 01:52 UTC: experiments that test that it works in the engine, and derivations for everything, the draw included; the advisor's matrix, #1563 comment 5964151108): T1 Born's rule as the proportionality to whole shares, the realised clicks per region against the window's shares on the two slits' world over four seeds, chi-square about 11 on 11 degrees; T2 the which-way world, the experiment of the heart, read beside its blind (examples/events/which_way); T3 the front's ball, every erased Node's remainder below one read coefficient and constant; T6 one act at three storeys, Rule3, the hold's write and the credit's count calling the one division act; T7 the clicks causally continuous on the telegraph's lines, the next click inside the previous one's cone."""

import ast
import json
import math
from pathlib import Path

import numpy as np

from event_universe import node
from event_universe.core.rule3 import division_fixed_point, division_forward, rule3
from event_universe.credit import record_unit
from event_universe.features.hold import hold
from event_universe.features.write import carried
from event_universe.game_board import GameBoard
from event_universe.giving import born_unit
from event_universe.loader.derived import count_wall
from event_universe.loader.instrument import pair_of
from event_universe.loader.universe import universe_of
from event_universe.loader.world import bodies_of, detectors_of, regions_of_the_law
from event_universe.meeting import hazard_weights
from event_universe.share import quanta_of
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, RUN, TOOL, TOP, load_file, refused

SLITS, WAY, RESONANCE = (
    load_file(f"{n}_build", EVENTS / n / "build_world.py")
    for n in ("two_slits", "which_way", "resonance")
)
SRC = ROOT / "src" / "event_universe"
GATE_ROW = [16, 17, 33, 12, 13, 42, 44, 10, 11, 21, 32, 27]  # the two slits' gate, N = 278, at the seed 24, the half-up rule's own


def clicks_and_shares(output: Path) -> tuple[dict[str, int], dict[str, int], int]:
    """A run's clicks per region (its credit lines) and its window shares per region (the click lines' inflows summed, floored at 0), and the quanta credited."""
    lines = json.loads(output.read_text(encoding="utf-8"))["lines"]
    clicks: dict[str, int] = {}
    shares: dict[str, int] = {}
    for line in lines:
        kind, at = line["event"], line["detector"]
        if kind in ("credit", "click"):
            book, gain = (clicks, 1) if kind == "credit" else (shares, int(line["inflow"]))
            book[at] = book.get(at, 0) + gain
    return clicks, {name: max(value, 0) for name, value in shares.items()}, sum(clicks.values())


def chi_square(clicks: dict[str, int], shares: dict[str, int], names: list[str]) -> float:
    """Pearson's chi-square of the realised clicks against the shares' expectation, N share_r / SUM share, over the named regions."""
    total, quanta = sum(shares[n] for n in names), sum(clicks.get(n, 0) for n in names)
    expected = {n: quanta * shares[n] / total for n in names}
    return sum((clicks.get(n, 0) - expected[n]) ** 2 / expected[n] for n in names)


def test_borns_rule_is_the_proportionality_to_whole_shares_over_four_seeds(tmp_path):
    """T1 (the law's line, the count is the record's share; the mathematician's 201 A1; the advisor's matrix row 7): the two slits' world laid at four seeds, the realised clicks per screen region (the credit lines, the clicks) against the window's shares (the click lines' inflows floored at 0, the GameBoard's reading the draw reads): Pearson's chi-square on 11 degrees inside the 1 percent band (2.6 to 26.8) at every seed and about 10 on average (the half-up rule's own run, every Node's remainder born at the half wall, 14.2, 16.1, 2.9, 6.0 at the seeds 24 to 27; the seed 24 the gate's own, N = 278 and the row bit for bit); the draw's weights are the shares and nothing else."""
    design = json.loads((EVENTS / "two_slits" / "design.json").read_text(encoding="utf-8"))
    names, found = [f"screen_{k}" for k in range(12)], []
    for seed in (24, 25, 26, 27):
        (folder := tmp_path / f"seed_{seed}").mkdir()
        seeded = {**design, "seed": seed, "instrument": {**design["instrument"], "seed": seed}}
        (folder / "design.json").write_text(json.dumps(seeded), encoding="utf-8")
        SLITS.main(["--design", str(folder / "design.json"), "--folder", str(folder)])
        assert RUN.run_input(str(folder / "two_slits.json"), str(folder))["verdict"] == "LAWFUL"
        clicks, shares, quanta = clicks_and_shares(folder / "two_slits.output.json")
        found.append(chi_square(clicks, shares, names))
        assert quanta == sum(clicks[n] for n in names) and clicks.get("gap", 0) == 0
        if seed == 24:  # the gate's own numbers, bit for bit
            assert quanta == 278 and [clicks[n] for n in names] == GATE_ROW
    assert all(2.6 < chi < 26.8 for chi in found) and 7 < sum(found) / 4 < 16, found
    assert [round(chi, 1) for chi in found] == [14.2, 16.1, 2.9, 6.0]  # the half-up rule's own run reproduced


def test_the_one_division_act_serves_rule3_the_hold_and_the_credit():
    """T6 (the mathematician's 189, two hands; the advisor's matrix row 9, one act at three storeys): the hold's write (`features/hold.hold`), the write's carried division (`features/write.carried`) and the credit's count (`share.quanta_of`, the credit's `counted`) compute by Rule3's division act and by nothing else, their modules naming no floor division, remainder or divmod of their own (the engine's gate on hand division beside it) and each equal to `division_forward` on the same integers: the hold (numerator + r) div wall with the remainder kept, the count (share + W_c div 2) div W_c."""
    acts = {"division_forward", "division_back", "rule3", "quanta_of"}
    for name in ("features/hold/__init__.py", "features/write/__init__.py", "share.py", "credit.py"):
        nodes = list(ast.walk(ast.parse((SRC / name).read_text(encoding="utf-8"))))
        hands = [
            n
            for n in nodes
            if isinstance(n, (ast.BinOp, ast.AugAssign)) and isinstance(n.op, (ast.FloorDiv, ast.Mod))
        ]
        names = {getattr(n, "id", None) or getattr(n, "attr", None) for n in nodes}
        assert not hands and "divmod" not in names and names & acts, name
    for numerator, wall, remainder in ((7, 3, 2), (-11, 4, 3), (0, 5, 4), (123456789, 1000, 999)):
        level, kept = hold(10, numerator, wall, remainder)
        act = division_forward(numerator, wall, remainder)
        assert (level - 10, kept) == act == carried(numerator, wall, remainder) and 0 <= kept < wall
        assert hold(level, numerator, wall, kept, -1) == (10, remainder)
    shares, wall = np.array([0, 5, 6, 7, 11, 12, 13, -1, 24], dtype=object), 12
    half = division_forward(wall, 2, 0)[0]
    assert list(quanta_of(shares, wall, object)) == [
        division_forward(int(s) + half, wall, 0)[0] for s in shares
    ]
    assert rule3((0,) * 6, (0,) * 6, 1, wall, 7, 0, 0) == (
        0,
        7,
    )  # the division act is Rule3 with no read


def test_the_clicks_are_causally_continuous_on_the_telegraphs_lines():
    """T7 (the mathematician's 198, the dependency cone, one Link per interval; the advisor's matrix row 11): over 200 intervals of the shelved ion's telegraph (examples/events/shelved_ion/shelved_ion.json, the committed world and its mode file), every click (the records' jump lines, the Node a GAMEBOARD diagnostic beside, and the counter's credit lines, no Node, the hole's Nodes read from the face lines after them) lies inside the cone of the click before it, |dx| + |dy| + |dz| <= dt on the periodic box, and every credit of a given light quantum lies inside the cone of the giving that laid it, the clicks causally continuous and not Node to Node; the box 12 x 12 x 8, the ion at [6, 6, 4]."""
    board = GameBoard(load_world(EVENTS / "shelved_ion" / "shelved_ion.json"), (lines := []).append)
    for _ in range(200):
        board.step()
    shape = board.world.shape

    def nodes_of(
        c: dict,
    ) -> list:  # a jump's one Node; a credit's the hole's Nodes in the face lines after it
        if c["event"] == "jump":
            return [c["node"]["at"]]
        holes = (f for f in lines if f["event"] == "face" and f["tick"] == c["tick"] + 1)
        return [f["node"]["at"] for f in holes if f["family"] == c["family"]]

    def inside(a: dict, b: dict) -> bool:  # the click b inside the cone of the click a
        return all(
            sum(min(abs(x - y), n - abs(x - y)) for x, y, n in zip(p, q, shape, strict=True))
            <= b["tick"] - a["tick"]
            for p in nodes_of(a)
            for q in nodes_of(b)
        )

    clicks = [c for c in lines if c["event"] in ("jump", "credit") and c["label"] == "DETECTOR"]
    clicks.sort(key=lambda c: int(c["tick"]))
    assert len(clicks) > 30 and all(
        nodes_of(c) and ("node" in c) == (c["event"] == "jump") for c in clicks
    )
    assert all(inside(a, b) for a, b in zip(clicks, clicks[1:], strict=False) if b["tick"] > a["tick"])
    givings = [c for c in clicks if c["event"] == "jump" and c["given"] == "fluorescence"]
    credits = [c for c in clicks if c["event"] == "credit" and c["family"] == "fluorescence"]
    assert givings and credits and all(inside(givings[0], c) for c in credits)
    assert all(
        g["tick"] < c["tick"] for g in givings[:1] for c in credits
    )  # the first giving precedes every credit


def test_the_which_way_world_reads_as_the_one_gap_world_and_the_fringes_are_gone(tmp_path):
    """T2, the experiment of the heart (the owner's word of 2026-10-03, 01:52 UTC; the advisor's matrix row 2; examples/events/which_way, the blind written by its builder before any lay): the three worlds of the design built, laid and run; the shadowed regions behind the channel's walls see 0 clicks exactly; the channel's clicks and the screen's sum to the quanta credited and the channel takes about half (the lower gap's quanta, the blind 136.5, within three times the draw's scatter); the decisive comparison, the which-way world's screen row against the one-gap world's, one draw against another at the same shares, within the 1 percent band of chi-square on 7 regions, and both against the two-gaps world's row: the two slits' minimum at the region 8 filled and the visibility about the regions 6 and 8 fallen below half the two slits'; the two-gaps world the shipped gate's numbers bit for bit (N = 278 and the row); one quantum one click per record (every credit's count 1, the count left falling by one per click)."""
    WAY.main(["--folder", str(tmp_path), "--modes"])
    blind = json.loads((tmp_path / "expectation.json").read_text(encoding="utf-8"))
    assert blind == json.loads((EVENTS / "which_way" / "expectation.json").read_text(encoding="utf-8"))
    rows, totals = {}, {}
    for name in ("which_way", "one_gap", "two_gaps"):
        assert RUN.run_input(str(tmp_path / f"{name}.json"), str(tmp_path))["verdict"] == "LAWFUL"
        clicks, _shares, totals[name] = clicks_and_shares(tmp_path / f"{name}.output.json")
        rows[name] = [clicks.get(f"screen_{k}", 0) for k in range(12)]
        lines = json.loads((tmp_path / f"{name}.output.json").read_text(encoding="utf-8"))["lines"]
        credits = [c for c in lines if c["event"] == "credit"]
        assert all(c["count"] == 1 for c in credits) and len({c["left"] for c in credits}) == len(
            credits
        )
        if name != "two_gaps":
            assert [rows[name][k] for k in blind["shadowed_regions"]] == [0] * 4 and rows[name][4] == 0
    way, one, two = rows["which_way"], rows["one_gap"], rows["two_gaps"]
    channel, scatter = totals["which_way"] - sum(way), 3 * math.sqrt(blind["quanta"]["two_gaps"]) / 2
    assert totals["one_gap"] == sum(one) and totals["two_gaps"] == sum(two) == 278 and two == GATE_ROW
    assert abs(channel - blind["quanta"]["which_way"]["channel"]) < scatter, channel
    assert abs(sum(way) - blind["quanta"]["which_way"]["screen"]) < scatter
    pairs = [(way[k], one[k]) for k in range(5, 12)]
    assert sum((a - b) ** 2 / (a + b) for a, b in pairs if a + b) < 18.5, pairs  # chi-square, 7 degrees
    assert way[8] > two[8] + 3 * math.sqrt(two[8] + 1)  # the two slits' minimum filled
    assert (way[6] - way[8]) * (two[6] + two[8]) * 2 < (two[6] - two[8]) * (
        way[6] + way[8]
    )  # the visibility


def test_the_fronts_ball_holds_remainders_below_one_read_coefficient_and_constant():
    """T3 (the mathematician's 193 (2) and 197 precision 3 with the advisor's second; the matrix row 3): on the anticoincidence world's one photon (examples/events/anticoincidence/one_photon.json, the chain of 24 with its receding faces, the committed world and its mode file) one record takes the photon at the interval 40, the photon's count reaches 0 and the front presents its faces shell by shell from the taker's Node; at every interval after, inside the ball of the shells whose two faces are done and whose outer neighbours stand at 0 (the Link-metric distance at most t - 40 - 3), every line of the photon's record stands at (0, 0) with its remainder below one read coefficient R of the photon's rule at the vacuum's paces and unchanged from one interval to the next: the erasure is Rule3's own write and nothing assigned; the erasure lines one per interval from the interval after the click."""
    board = GameBoard(load_world(EVENTS / "anticoincidence" / "one_photon.json"), (lines := []).append)
    for _ in range(40):
        board.step()
    light = next(i for i, f in enumerate(board.families) if f.name == "photon")
    read = node.rule_of(board.families[light], board.world.node_clock, 0, None, board.unit)[0][0]
    jumps = [c for c in lines if c["event"] == "jump" and c["label"] == "DETECTOR"]
    assert len(jumps) == 1 and jumps[0]["tick"] == 40 and board.credit.counts[light] == 0
    since, origin = 40, jumps[0]["node"]["at"]
    assert board.credit.fronts == [(light, tuple(origin), since)]
    checked = 0

    def ball(
        tick: int,
    ) -> tuple[np.ndarray, list]:  # the ball's mask at the board's offset now, the record's lines
        at = np.reshape(np.add(origin, board.offset), (3, 1, 1, 1))
        inside = np.abs(np.indices(board.shape) - at).sum(axis=0) <= tick - since - 3
        return inside, board.states[light].lines[: board.families[light].record]

    for tick in range(since + 4, since + 16):
        while board.tick < tick:
            board.step()
        inside, own = ball(tick)
        kept = [line.remainder[inside].copy() for line in own]
        for line in own:
            assert not line.now[inside].any() and not line.before[inside].any()
            assert (line.remainder[inside] >= 0).all() and (line.remainder[inside] < read).all()
        board.step()  # the board may grow at a receding face: the ball read again at the new offset
        inside, own = ball(tick)
        assert all((a == line.remainder[inside]).all() for a, line in zip(kept, own, strict=True))
        checked += int(inside.sum())
    erased = [e["tick"] - since for e in lines if e["event"] == "erasure"]
    assert (
        checked > 100
        and erased[:3] == [1, 2, 3]
        and [e for e in lines if e["event"] == "erasure"][0]["nodes"] == 2
    )


def test_the_born_lights_frequency_is_the_declared_resonance_and_a_detector_counts_in_its_own_quantum(
    tmp_path,
):
    """T4, test (vi) (the owner's word of 2026-10-03, 05:00 UTC, "not in the morning, now"; the mathematician's 213 (B), #1572 comment 5965054791, his 214, 5965082449, and 220, 5965303134, with the advisor's seconds, #1563 comment 5965316267 and #1572 comment 5965312353, two hands; examples/events/resonance, the blind written by its builder before any lay): a region's unit of one quantum is its record's own share per quantum read once at the books' origin (`credit.record_unit`, the advisor's line of 2026-10-03 with the mathematician's second, two hands), W_c for a record laid by share with its count and W_c sin Omega = 2.23605 den T for one quantum at [2, 3], and the loader refuses by name a region declaring a `transition`, a one-Node region (a region of a travelling wave), a transition without its resonance and a giving with no transition between its parts; the dark's hazard is per proper interval (`meeting.hazard_weights`): the weights [span x unit, (tau - span) x unit] in the vacuum and half the giving's weight at p_0 = Gamma / 2; on the resonance world the giver gives at the interval 48 with certainty and lays the quantum as a source in time over 48 intervals, one lay line each on the light's first line at the giver's Node, the level now alone, the amplitudes at most 22 (21 on 30 intervals and 22 on 18, the carry); at the span's end the light's share over the board reads sin Omega = 0.745 quanta of the band's top, one quantum by the count's line in the top's unit and in the detector's own unit at [2, 3] alike; the far Node's cosine over the plateau (the intervals 76 to 90, after the front has passed at the group pace 1 / (3 sin Omega) and before the source stops) reads cos Omega within 2 / A_far of 2 / 3 (the design's own window, 62 to 70, lies in the front's transit and misses, a finding named in the folder); light's Links at the instrument's Node open, the cut the atom's own. Under the dark grain (the mathematician's 223 (a), #1572 comment 5965727937, and 224 (2)(a), 5966081562, with the advisor's 5965918924 (a) and his second 5966129376, two hands; `meeting.dark`, `meeting.gave`): the giver is in the dark until it gives, so over the trials' first 25 seeds its giving is drawn once per interval at the hazard 1 / 48 at the now, the generator advanced exactly once per interval and not at the window's close at 48, the givings at distinct intervals and within the lifetime in 8 to 24 of 25 (the blind's 0.636, three deviations), each seed's lay lines the span from its interval cut by the run's end, the far Node's cosine on each seed's plateau [t + 28, t + 42] within the gate and the count at the span's end 1 where the whole span lies in the run; with the light laid on the chain a window stands and the window's draw at 48 stands as it is."""
    universe = json.loads((EVENTS / "zeno" / "zeno_atom.json").read_text(encoding="utf-8"))
    families, action = universe_of(universe)[1], universe["integers"]["quantum_action"]
    light = next(f for f in families if f.name == "pulse")
    wall = count_wall(light, action)
    refused("from -1 through 1", pair_of, [3, 2], "resonance")
    refused("pair", pair_of, [1], "resonance")
    row = {"name": "d", "positions": [[0, 0, 0], [1, 0, 0]]}
    refused(
        "holds the key 'transition'", detectors_of, [{**row, "transition": TOP}], (2, 1, 1), 0, (), ()
    )
    one = [{"name": "d", "positions": [[0, 0, 0]]}]
    refused(
        "a region of a travelling wave",
        regions_of_the_law,
        detectors_of(one, (2, 1, 1), 0, (), ()),
        (),
        (2, 1, 1),
        (False,) * 3,
        (),
    )
    RESONANCE.main(["--folder", str(tmp_path), "--modes"])
    blind = json.loads((tmp_path / "expectation.json").read_text(encoding="utf-8"))
    assert blind == json.loads((EVENTS / "resonance" / "expectation.json").read_text(encoding="utf-8"))
    world = json.loads((tmp_path / "resonant.json").read_text(encoding="utf-8"))
    bare = {k: v for k, v in world["measured"][0]["transitions"][0].items() if k != "resonance"}
    refused(
        "resonance",
        bodies_of,
        [{**world["measured"][0], "transitions": [bare]}],
        None,
        "",
        families,
        (48, 1, 1),
        9000,
        (),
    )
    alone = {**world["measured"][0], "transitions": []}
    refused("no transition between them", bodies_of, [alone], None, "", families, (48, 1, 1), 9000, ())
    path, draw, at = (
        tmp_path / "resonant.json",
        world["measured"][0]["instrument"],
        tuple(blind["cos_omega"]["node"]),
    )
    given_at: list[int] = []
    for seed in range(
        1, 26
    ):  # the trials' seeds, every record's generator at its own state (tools/meeting_trials.py)
        board = GameBoard(load_world(path), (lines := []).append)
        light_at = [f.name for f in board.families].index("pulse")
        gamma, own = (
            board.world.node_clock,
            division_fixed_point(wall * wall * 5) // 3,
        )  # one quantum at [2, 3]
        assert (
            record_unit(board, light_at, 7 * wall, 7) == wall
            and record_unit(board, light_at, own, 1) == own
        )  # W_rec
        assert abs(own / wall - 5**0.5 / 3) < 2 / wall and record_unit(board, light_at, None, 0) == wall
        assert hazard_weights(1, 48, gamma, gamma, 9) == [
            9,
            47 * 9,
        ]  # the vacuum: the hazard per board tick
        assert hazard_weights(2, 48, gamma // 2, gamma, 9) == [
            9,
            47 * 9,
        ]  # a well at p_0 = Gamma / 2: half the rate
        for books in board.credit.bodies:
            books.state = seed * len(board.credit.bodies) + books.number
        pulse = [f.name for f in board.families].index("pulse")
        giver, series, expected = board.credit.bodies[0], {}, board.credit.bodies[0].state
        for _ in range(96):
            board.step()
            series[board.tick] = int(board.states[pulse].lines[0].now[at])
            given = [c for c in lines if c["event"] == "jump" and c["given"] == "pulse"]
            if not given:  # in the dark one draw per interval at the now; the window's close at 48 draws nothing more
                expected = (draw["multiplier"] * expected + draw["increment"]) % (board.world.width + 1)
                assert giver.state == expected
        if not given:
            continue
        t = given[0]["tick"]
        given_at.append(t)
        lays = [c for c in lines if c["event"] == "lay" and c["family"] == "pulse"]
        assert [c["tick"] for c in lays] == list(
            range(t, min(t + 48, 97))
        )  # the span from t, cut by the run's end
        assert all(
            c["node"]["at"] == [0, 0, 0] and c["line"] == 0 and c["after"][1:] == c["before"][1:]
            for c in lays
        )
        taken = [c for c in lines if c["event"] == "jump" and c["taken"]]
        assert max(abs(c["after"][0] - c["before"][0]) for c in lays) <= 22
        assert board.credit.counts[pulse] + len(taken) == 1  # one quantum given, kept or taken
        if (
            t <= 49 and not taken
        ):  # the whole span in the run: one quantum by the count's line, either unit
            total = board.total_share(pulse)[0]
            assert (
                total is not None and 0.7 < total / wall < 0.8
            )  # sin Omega = 0.745 in the band's top's unit
            for unit in (wall, record_unit(board, pulse, total, 1)):  # W_c and the record's own unit
                assert division_forward(total, unit, division_forward(unit, 2, 0)[0])[0] == 1
        if t <= 53:  # the plateau after the front and before the stop, inside the run
            window = range(t + 28, t + 43)
            numerator = sum(series[k] * (series[k + 1] + series[k - 1]) for k in window)
            read = numerator / (2 * sum(series[k] ** 2 for k in window))
            far = max(abs(series[k]) for k in window)
            assert far > 20 and abs(read - 2 / 3) <= 2 / far, (t, read, far)
    by_tau = sum(t <= 48 for t in given_at)  # 25 x 0.636 = 15.9 +/- 2.4: within three deviations
    assert 8 <= by_tau <= 24 and len(set(given_at)) > 1, (
        given_at
    )  # not the degenerate corner's one interval
    lit = {**world, "messages": [{"family": "pulse", "along": "x", "wave": [1, 2], "amplitude": 308}]}
    lit["messages"][0].update(
        top={"x": [0, 47], "y": [0, 0], "z": [0, 0]}, edge={"x": 0, "y": 0, "z": 0}
    )
    (path := tmp_path / "lit.json").write_text(json.dumps(lit), encoding="utf-8")
    TOOL.main(["--input", str(path)])
    for seed in (1, 2, 3):  # the light at its Node: a window stands and its draw at 48 stands as it is
        board = GameBoard(load_world(path), (lines := []).append)
        light_at = [f.name for f in board.families].index("pulse")
        gamma, own = (
            board.world.node_clock,
            division_fixed_point(wall * wall * 5) // 3,
        )  # one quantum at [2, 3]
        assert (
            record_unit(board, light_at, 7 * wall, 7) == wall
            and record_unit(board, light_at, own, 1) == own
        )  # W_rec
        assert abs(own / wall - 5**0.5 / 3) < 2 / wall and record_unit(board, light_at, None, 0) == wall
        assert hazard_weights(1, 48, gamma, gamma, 9) == [
            9,
            47 * 9,
        ]  # the vacuum: the hazard per board tick
        assert hazard_weights(2, 48, gamma // 2, gamma, 9) == [
            9,
            47 * 9,
        ]  # a well at p_0 = Gamma / 2: half the rate
        for books in board.credit.bodies:
            books.state = seed * len(board.credit.bodies) + books.number
        [board.step() for _ in range(48)]
        assert [c["tick"] for c in lines if c["event"] == "jump" and c["given"] == "pulse"] == [48]


def test_a_record_empty_at_the_origin_takes_its_unit_from_its_first_lay(tmp_path):
    """The unit of a record empty at the books' origin (the advisor's word of 2026-10-03, #1572 comment 5967247080, on the generic detector's entry; `giving.born_unit`, `credit.Books.empty`): the resonance world's giver alone with its transition at [9, 10], sin Omega = 0.436 below 1 / 2, its window 240 so that it takes nothing back before the run's end, over 240 intervals. Light's record holds nothing at the origin, so its unit stands at W_c and it is named empty; at the giving's first lay the unit becomes the giving's own W_c sin Omega, 0.436 W_c within the root's rounding, the record leaves the empty set and the unit is held. The books' count after the giving 1, kept or taken back at the window's close, a click's number. The finding by name beside it, a GameBoard reading recorded in ENGINE.md and not pinned here (2026-10-03): at the span's end, before any taking, the born quantum's share over the board reads about W_c at [9, 10] (1.06 at the seed 1; 0.84 at [4, 5], 0.75 at [2, 3]: the count's line's W_c sin Omega holds near the band's top alone), so the credit in W_c reads 1 already and the credit in the record's own unit would read 2; the premise that a born quantum below the half-top energy is credited 0 is not what the engine reads on the chain, left to the hands (the mathematician's 245 answers it: the source in time's energy on the chain)."""
    world = json.loads((EVENTS / "resonance" / "resonant.json").read_text(encoding="utf-8"))
    giver = {**world["measured"][0], "transitions": [{**world["measured"][0]["transitions"][0]}]}
    giver["transitions"][0]["resonance"], giver["instrument"] = (
        [9, 10],
        {**giver["instrument"], "window": 240},
    )
    (path := tmp_path / "low.json").write_text(json.dumps({**world, "measured": [giver], "ticks": 240}))
    TOOL.main(["--input", str(path)])
    for seed in (1, 2, 3, 4):  # the first trial whose giving leaves the whole span inside the run
        board, series = GameBoard(load_world(path), (lines := []).append), {}
        pulse = [f.name for f in board.families].index("pulse")
        wall, books = count_wall(board.families[pulse], board.world.quantum_action), board.credit
        assert books.units[pulse] == wall and pulse in books.empty and books.counts[pulse] == 0
        board.credit.bodies[0].state = seed
        for _ in range(240):
            board.step()
            series[board.tick] = board.total_share(pulse)[0]
        jumps = [
            (c["tick"], c["given"]) for c in lines if c["event"] == "jump" and c["label"] == "DETECTOR"
        ]
        if jumps and jumps[0][1] == "pulse" and jumps[0][0] <= 192:
            break
    assert jumps and jumps[0][1] == "pulse" and jumps[0][0] <= 192 and pulse not in books.empty
    assert (
        books.units[pulse] == born_unit(board, pulse, (9, 10))
        and abs(books.units[pulse] / wall - 0.436) < 0.002
    )
    taken = sum(given is None for _t, given in jumps[1:])  # the window's close at 240 may take it back
    assert books.counts[pulse] + taken == 1  # one quantum given, kept or taken back, the books' number
