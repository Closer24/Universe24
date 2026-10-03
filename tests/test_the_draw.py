"""The draw's experiments in the engine (the owner's word of 2026-10-03, 01:52 UTC: experiments that test that it works in the engine, and derivations for everything, the draw included; the advisor's matrix, #1563 comment 5964151108): T1 Born's rule as the proportionality to whole shares, the realised clicks per region against the window's shares on the two slits' world over four seeds, chi-square about 11 on 11 degrees; T2 the which-way world, the experiment of the heart, read beside its blind (examples/events/which_way); T3 the front's ball, every erased Node's remainder below one read coefficient and constant; T6 one act at three storeys, Rule3, the hold's write and the credit's count calling the one division act; T7 the clicks causally continuous on the telegraph's lines, the next click inside the previous one's cone."""

import ast
import json
import math
from pathlib import Path

import numpy as np

from event_universe import node
from event_universe.core.rule3 import division_forward, rule3
from event_universe.features.hold import hold
from event_universe.features.write import carried
from event_universe.game_board import GameBoard
from event_universe.share import quanta_of
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, RUN, load_file

SLITS, WAY = (load_file(f"{n}_build", EVENTS / n / "build_world.py") for n in ("two_slits", "which_way"))
SRC = ROOT / "src" / "event_universe"


def clicks_and_shares(output: Path) -> tuple[dict[str, int], dict[str, int], int]:
    """A run's clicks per region (its credit lines) and its window shares per region (the click lines' inflows summed, floored at 0), and the quanta credited."""
    lines = json.loads(output.read_text(encoding="utf-8"))["lines"]
    clicks: dict[str, int] = {}
    shares: dict[str, int] = {}
    for line in lines:
        if line["event"] == "credit":
            clicks[line["detector"]] = clicks.get(line["detector"], 0) + 1
        if line["event"] == "click":
            shares[line["detector"]] = shares.get(line["detector"], 0) + int(line["inflow"])
    shares = {name: max(value, 0) for name, value in shares.items()}
    return clicks, shares, sum(clicks.values())


def chi_square(clicks: dict[str, int], shares: dict[str, int], names: list[str]) -> float:
    """Pearson's chi-square of the realised clicks against the shares' expectation, N share_r / SUM share, over the named regions."""
    total, quanta = sum(shares[n] for n in names), sum(clicks.get(n, 0) for n in names)
    expected = {n: quanta * shares[n] / total for n in names}
    return sum((clicks.get(n, 0) - expected[n]) ** 2 / expected[n] for n in names)


def test_borns_rule_is_the_proportionality_to_whole_shares_over_four_seeds(tmp_path):
    """T1 (the law's line, the count is the record's share; the mathematician's 201 A1; the advisor's matrix row 7): the two slits' world laid at four seeds, the realised clicks per screen region (the credit lines, the clicks) against the window's shares (the click lines' inflows floored at 0, the GameBoard's reading the draw reads): Pearson's chi-square on 11 degrees inside the 1 percent band (2.6 to 26.8) at every seed and about 11 on average (the advisor's run 8.9, 10.5, 9.5, 12.1 at the seeds 24 to 27; the seed 24 the gate's own, N = 278 and the row bit for bit); the draw's weights are the shares and nothing else."""
    design, worlds = json.loads((EVENTS / "two_slits" / "design.json").read_text(encoding="utf-8")), []
    for seed in (24, 25, 26, 27):
        folder = tmp_path / f"seed_{seed}"
        folder.mkdir()
        seeded = {**design, "seed": seed, "instrument": {**design["instrument"], "seed": seed}}
        (folder / "design.json").write_text(json.dumps(seeded), encoding="utf-8")
        SLITS.main(["--design", str(folder / "design.json"), "--folder", str(folder)])
        worlds.append(folder / "two_slits.json")
    found = []
    for world in worlds:
        assert RUN.run_input(str(world), str(world.parent))["verdict"] == "LAWFUL"
        clicks, shares, quanta = clicks_and_shares(world.parent / "two_slits.output.json")
        names = [f"screen_{k}" for k in range(12)]
        found.append(chi_square(clicks, shares, names))
        assert quanta == sum(clicks[n] for n in names) and clicks.get("gap", 0) == 0
        if world.parent.name == "seed_24":  # the gate's own numbers, bit for bit
            assert quanta == 278 and [clicks[n] for n in names] == [
                23,
                18,
                34,
                13,
                5,
                35,
                52,
                19,
                9,
                27,
                22,
                21,
            ]
    assert all(2.6 < chi < 26.8 for chi in found) and 7 < sum(found) / 4 < 16, found
    assert [round(chi, 1) for chi in found] == [8.9, 10.5, 9.5, 12.1]  # the advisor's run reproduced


def test_the_one_division_act_serves_rule3_the_hold_and_the_credit():
    """T6 (the mathematician's 189, two hands; the advisor's matrix row 9, one act at three storeys): the hold's write (`features/hold.hold`), the write's carried division (`features/write.carried`) and the credit's count (`share.quanta_of`, the credit's `counted`) compute by Rule3's division act and by nothing else, their modules naming no floor division, remainder or divmod of their own (the engine's gate on hand division beside it) and each equal to `division_forward` on the same integers: the hold (numerator + r) div wall with the remainder kept, the count (share + W_c div 2) div W_c."""
    sources = {
        n: (SRC / n).read_text(encoding="utf-8")
        for n in ("features/hold/__init__.py", "features/write/__init__.py", "share.py", "credit.py")
    }
    for name, text in sources.items():
        tree = ast.parse(text)
        hands = [
            n
            for n in ast.walk(tree)
            if isinstance(n, (ast.BinOp, ast.AugAssign)) and isinstance(n.op, (ast.FloorDiv, ast.Mod))
        ]
        names = {getattr(n, "id", None) or getattr(n, "attr", None) for n in ast.walk(tree)}
        assert not hands and "divmod" not in names, name
        assert names & {"division_forward", "division_back", "rule3", "quanta_of"}, name
    for numerator, wall, remainder in ((7, 3, 2), (-11, 4, 3), (0, 5, 4), (123456789, 1000, 999)):
        level, kept = hold(10, numerator, wall, remainder)
        assert (
            (level - 10, kept)
            == division_forward(numerator, wall, remainder)
            == carried(numerator, wall, remainder)
        )
        back, origin = hold(level, numerator, wall, kept, -1)
        assert (back, origin) == (10, remainder) and 0 <= kept < wall
    shares, wall = np.array([0, 5, 6, 7, 11, 12, 13, -1, 24], dtype=object), 12
    assert list(quanta_of(shares, wall, object)) == [
        division_forward(int(s) + wall // 2, wall, 0)[0] for s in shares
    ]
    assert rule3((0,) * 6, (0,) * 6, 1, wall, 7, 0, 0) == (
        0,
        7,
    )  # the division act is Rule3 with no read


def test_the_clicks_are_causally_continuous_on_the_telegraphs_lines():
    """T7 (the mathematician's 198, the dependency cone, one Link per interval; the advisor's matrix row 11): over 200 intervals of the shelved ion's telegraph (examples/events/shelved_ion/shelved_ion.json, the committed world and its mode file), every click that carries a Node (the records' jump lines and the counter's credit lines, labelled DETECTOR, the Node a GAMEBOARD diagnostic beside) lies inside the cone of the click before it, |dx| + |dy| + |dz| <= dt on the periodic box, and every credit of a given light quantum lies inside the cone of the giving that laid it, the clicks causally continuous and not Node to Node; the box 12 x 12 x 8, the ion at [6, 6, 4]."""
    board = GameBoard(load_world(EVENTS / "shelved_ion" / "shelved_ion.json"), (lines := []).append)
    for _ in range(200):
        board.step()
    shape = board.world.shape

    def apart(a: list[int], b: list[int]) -> int:
        return sum(min(abs(x - y), n - abs(x - y)) for x, y, n in zip(a, b, shape, strict=True))

    clicks = [c for c in lines if c["event"] in ("jump", "credit") and c["label"] == "DETECTOR"]
    clicks.sort(key=lambda c: int(c["tick"]))
    assert len(clicks) > 30 and {c["node"]["label"] for c in clicks} == {"GAMEBOARD"}
    for before, after in zip(clicks, clicks[1:], strict=False):
        if after["tick"] > before["tick"]:
            assert apart(before["node"]["at"], after["node"]["at"]) <= after["tick"] - before["tick"], (
                before,
                after,
            )
    givings = [c for c in clicks if c["event"] == "jump" and c["given"] == "fluorescence"]
    credits = [c for c in clicks if c["event"] == "credit" and c["family"] == "fluorescence"]
    assert givings and credits
    for credit in credits:
        born = [g for g in givings if g["tick"] < credit["tick"]]
        assert (
            born
            and apart(born[0]["node"]["at"], credit["node"]["at"]) <= credit["tick"] - born[0]["tick"]
        )


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
    channel = totals["which_way"] - sum(rows["which_way"])
    assert channel + sum(rows["which_way"]) == totals["which_way"] and totals["one_gap"] == sum(
        rows["one_gap"]
    )
    scatter = 3 * math.sqrt(blind["quanta"]["two_gaps"]) / 2
    assert abs(channel - blind["quanta"]["which_way"]["channel"]) < scatter, channel
    assert abs(sum(rows["which_way"]) - blind["quanta"]["which_way"]["screen"]) < scatter
    pairs = [(rows["which_way"][k], rows["one_gap"][k]) for k in range(5, 12)]
    assert sum((a - b) ** 2 / (a + b) for a, b in pairs if a + b) < 18.5, (
        pairs
    )  # chi-square, 7 degrees, 1 percent
    two, way = rows["two_gaps"], rows["which_way"]
    assert totals["two_gaps"] == 278 and two == [23, 18, 34, 13, 5, 35, 52, 19, 9, 27, 22, 21]
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
    for tick in range(since + 4, since + 16):
        while board.tick < tick:
            board.step()
        at = np.reshape(np.add(origin, board.offset), (3, 1, 1, 1))
        inside = np.abs(np.indices(board.shape) - at).sum(axis=0) <= tick - since - 3
        own = board.states[light].lines[: board.families[light].record]
        kept = [line.remainder[inside].copy() for line in own]
        for line in own:
            assert not line.now[inside].any() and not line.before[inside].any()
            assert (line.remainder[inside] >= 0).all() and (line.remainder[inside] < read).all()
        board.step()  # the board may grow at a receding face: the ball read again at the new offset
        at = np.reshape(np.add(origin, board.offset), (3, 1, 1, 1))
        inside = np.abs(np.indices(board.shape) - at).sum(axis=0) <= tick - since - 3
        after = [
            line.remainder[inside] for line in board.states[light].lines[: board.families[light].record]
        ]
        assert all((a == b).all() for a, b in zip(kept, after, strict=True))
        checked += int(inside.sum())
    erased = [e for e in lines if e["event"] == "erasure"]
    assert (
        checked > 100
        and [e["tick"] - since for e in erased][:3] == [1, 2, 3]
        and erased[0]["nodes"] == 2
    )
