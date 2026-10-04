"""The giving lays no uniform mode and the front writes to 0 over L declared shells (ALGEBRA.md, The click writes on the GameBoard (5) and (6); the owner's "yes to everything" of 2026-10-04, #1793 comment 5975629873; the mathematician's hand, #1793 comments 5975866852 and 5975925032, the advisor's seconds 5975890713 and 5975964920): the source in time's increments corrected by the division act in time where the span holds its period, the open board's packet's two levels by the message lay's act, the front's taper with the erasure line's take in quanta; one test each, on the mathematician's branch for the engine's reopening."""

import json

import numpy as np

from event_universe import world_files
from event_universe.features.click import SCALE_OF
from event_universe.game_board import GameBoard
from event_universe.giving import holds_period, increments_of, radiated_total, uniform_removed_in_time
from event_universe.loader.derived import count_wall
from event_universe.world_files import load_world
from tests.laws import BACK, EVENTS, ROOT, TOOL, refused


def test_the_source_in_time_lays_no_uniform_mode_where_its_span_holds_a_period():
    """The giving lays no uniform mode (ALGEBRA.md, The click writes on the GameBoard (5); the mathematician's hand, #1793 comments 5975866852 and 5975925032; `giving.increments_of`, `uniform_removed_in_time`, `holds_period`): the source's increments at [2, 3] over 48 intervals sum to 31 with the moment SUM t delta_t 938 as laid, and corrected by the division act in time to 0 and 0 exactly, the corrections at most 2 levels; the span holds a period where tau Omega >= 2 pi by the rotation act (from 8 at [2, 3], from 15 at [5414, 6000], never at 1 or 2), and a span of 4 is laid as built since the correction would leave [-9, 13, 1, -5] of [73, 49, -8, -60]; on the resonance world the giver gives at 41 and at the interval 96 the light's two sums over the chain of 48 are within one level per Node (3 and 6, against 797 and 765 before the correction) while the share reads the quantum, 0.7518 W_c against sin Omega = 0.745 (0.7582 uncorrected)."""
    scale, total = (3 * 6000 * 32768) ** SCALE_OF, radiated_total(32768, (2, 3))
    raw, amplitudes = increments_of(total, 48, (2, 3), scale)
    fixed = uniform_removed_in_time(raw, amplitudes)
    assert (sum(raw), sum(t * d for t, d in enumerate(raw)), min(amplitudes), max(amplitudes)) == (
        31,
        938,
        21,
        22,
    )
    assert sum(fixed) == 0 and sum(t * d for t, d in enumerate(fixed)) == 0
    assert max(abs(a - b) for a, b in zip(raw, fixed, strict=True)) == 2
    assert [holds_period(t, (2, 3), scale) for t in (1, 2, 7, 8, 48)] == [
        False,
        False,
        False,
        True,
        True,
    ]
    assert [holds_period(t, (5414, 6000), scale) for t in (14, 15)] == [False, True]
    short, amps = increments_of(total, 4, (2, 3), scale)
    assert short == [73, 49, -8, -60] and uniform_removed_in_time(short, amps) == [-9, 13, 1, -5]
    board = GameBoard(load_world(EVENTS / "resonance" / "resonant.json"), (lines := []).append)
    pulse = [f.name for f in board.families].index("pulse")
    for _ in range(96):
        board.step()
    given = [c for c in lines if c["event"] == "credit" and c["given"] == "pulse"]
    line = board.states[pulse].lines[0]
    sums = (int(line.now.sum(dtype=object)), int(line.before.sum(dtype=object)))
    assert len(given) == 1 and given[0]["tick"] == 41 and max(map(abs, sums)) <= 48
    share, wall = board.total_share(pulse)[0], count_wall(board.families[pulse], 32768)
    assert share is not None and 74 * wall <= 100 * share <= 76 * wall  # sin Omega = 0.745, the quantum


def test_the_open_boards_packet_lays_no_uniform_mode(tmp_path):
    """The packet's two levels take the message lay's division act over the packet's Nodes where the span holds a period (ALGEBRA.md, The click writes on the GameBoard (5) and The message lay; `giving.laid_packet`, `holds_period`, `features/start.uniform_removed`): on an open board of 160 by 5 by 5 a giver of the lifetime 8 lays its packet of 3 across along a drawn sense of x, and the light record's levels now and before each sum to 0 over the board exactly after the lay (the energy-form envelope under the carrier sums to other than 0: the shipped packet world's before summed to -80 over 4,992 Nodes, the two slits' bump of +24,442 the same defect), the top's level standing above 20 of the envelope's 24, the count 1 in the books; the lifetime-2 toy of the test above is laid as built, below its period."""
    world = json.loads((EVENTS / "packet_giving" / "packet_giving.json").read_text(encoding="utf-8"))
    giver = world["bodies"][0]
    rate = {**giver["rates"][0], "width": 3, "lifetime": 8}
    nodes = [{"node": [80, 2, 2], "weight": 1}, {"node": [81, 2, 2], "weight": 1}]
    small = {**world, "shape": [160, 5, 5], "ticks": 60, "node_readers": []}
    small["bodies"] = [{**giver, "nodes": nodes, "rates": [rate]}]
    small["bodies"][0]["node_reader"] = {**giver["node_reader"], "window": 2}
    del small["draw"]
    (path := tmp_path / "small.json").write_text(json.dumps(small) + "\n", encoding="utf-8")
    TOOL.main(["--input", str(path)])
    board = GameBoard(load_world(path), (lines := []).append)
    pulse = [f.name for f in board.families].index("pulse")
    while board.tick < 60 and not any(c["event"] == "credit" and c["given"] == "pulse" for c in lines):
        board.step()
    lays = [c for c in lines if c["event"] == "lay" and c["family"] == "pulse"]
    assert len(lays) > 500 and board.credit.counts[pulse] == 1  # the train of 69 slices by 9 across
    sums = [sum(c["after"][k] - c["before"][k] for c in lays) for k in (0, 1)]
    assert sums == [0, 0] and max(abs(c["after"][0]) for c in lays) > 20  # each level's lay sums to 0


def test_the_front_writes_to_zero_over_the_declared_shells_and_the_board_ends_dark(
    tmp_path, monkeypatch
):
    """The front's taper (ALGEBRA.md, The click writes on the GameBoard (6), the front writes to 0 over L shells, L declared; the owner's word of 2026-10-04; `src/event_universe/front.py`, `Face.fraction`, the world's `erasure`): the one-photon world with `erasure` 8, its mode file regenerated, takes at 48 as the shipped one does; from then every Node at Link distance at most d - 9 from the hole, d the intervals since the click, holds the photon's record at (0, 0) exactly while the last eight shells before the reach carry falling levels (a shell within them nonzero at some interval), the erasure lines carry the shell's share `take` and the record's `unit`, the share over the board never rises above the lay's by more than one part in seven and is 0 exactly at 230, once the band of eight shells has left the grown board, the board dark; the back-in-time gate reads MATCH over 170 intervals across the tapered faces; `erasure` 0 is refused by name and the shipped world loads at 1."""
    folder = EVENTS / "anticoincidence"
    world = json.loads((folder / "one_photon.json").read_text(encoding="utf-8"))
    (tmp_path / "u.json").write_bytes((ROOT / world["universe"]).read_bytes())
    (tmp_path / "e.json").write_bytes((ROOT / world["engine"]).read_bytes())
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world.update(universe="u.json", engine="e.json", erasure=8)
    (path := tmp_path / "tapered.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(path)])
    (bad := tmp_path / "bad.json").write_text(json.dumps({**world, "erasure": 0}), encoding="utf-8")
    refused("erasure", load_world, bad)
    board = GameBoard(load_world(path), (lines := []).append)
    assert board.world.erasure == 8
    photon, shares = [f.name for f in board.families].index("photon"), []
    laid = board.books()["photon"]["share"]
    for _ in range(48):
        board.step()
    credits = [c for c in lines if c["event"] == "credit" and c["label"] == "NODEREADER" and c["taken"]]
    assert len(credits) == 1 and credits[0]["tick"] == 48 and board.credit.counts[photon] == 0
    origin = next(f.at for f in board.credit.faces[49] if f.family == photon)
    tapered = 0
    for tick in range(49, 231):  # the band of eight shells leaves the grown board by about 210
        board.step()
        shares.append(board.books()["photon"]["share"])
        at = np.reshape(np.add(origin, board.offset), (3, 1, 1, 1))
        distance = np.abs(np.indices(board.shape) - at).sum(axis=0)
        inside, taper = distance <= tick - 48 - 9, (distance > tick - 48 - 9) & (distance <= tick - 48)
        for line in board.states[photon].lines[: board.families[photon].record]:
            assert not line.now[inside].any() and not line.before[inside].any()
            tapered += int(np.abs(line.now[taper]).sum(dtype=object) > 0)
    erased = [e for e in lines if e["event"] == "erasure"]
    assert tapered > 20 and erased and all(e["unit"] == board.credit.units[photon] for e in erased)
    assert all(e["take"] >= 0 for e in erased) and max(e["take"] for e in erased) > 0
    assert laid > 0 and max(shares) * 7 <= laid * 8 and shares[-1] == 0
    assert BACK.verdict(GameBoard(load_world(path)), 170)["verdict"] == "MATCH"
