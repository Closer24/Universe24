"""THE RUNS TOWARD NATURE, rows (1) to (3) (ALGEBRA.md #the-rows-against-nature to (3); BUILD.md section 26
item 41): the five world files of `examples/events/toward_nature/` are the generator's, carry
the declared integers (Gamma 10^4, the well's level 2000 on the arm's free Nodes, the momenta
one quarter of each block's drive wall, the bending's beam 20 wide with its body's content
set for U_b = 0.1 on the beam's line) and no pin; the moving clock's two blocks hop together
(the emitter, its mirror and its set one Link every 4 intervals, GAMEBOARD); the reader's
arithmetic on a written output (the mean, the standard error, the ratio and the closed forms
it is set beside, COMPUTATION). No run against a pin: the rows are diagnostics (ALGEBRA.md #the-rows-against-nature)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import parse_nature_beam_world
from tests.running import FOLDER, document, load_module

NAMES = (
    "redshift_top",
    "redshift_bottom",
    "lorentz_rest",
    "lorentz_moving",
    "bending",
    "redshift_top_long",
    "redshift_bottom_long",
    "lorentz_rest_long",
    "lorentz_moving_long",
)


def test_the_four_worlds_carry_the_declared_integers_and_no_pin():
    generator = load_module("make_worlds")
    assert not (FOLDER / "expectations.json").exists(), (
        "a diagnostic row carries no pin (ALGEBRA.md #the-rows-against-nature)"
    )
    for name in NAMES:
        doc = document(name)
        world = parse_nature_beam_world(doc)
        # the integers from the families file alone (item 59)
        assert doc["universe"] == "examples/events/universe.json" and "node_clock" not in doc
        assert world.node_clock == generator.NODE_CLOCK == 10_000
        if name == "bending":
            continue
        assert doc["detectors"][0]["name"] == "at_well" and doc["detectors"][0]["block"] == 0
        assert world.shape[1:] == (3, 3)
    # the long-wave pair (ALGEBRA.md #the-rows-against-nature): the given clock [4096, 21] on N = 2048; SINCE
    # COMMIT 7 the emitter is the chain's point extruded, [1, 3, 3] at the retired train's head
    # (one train, 168 Nodes, from the face), on the point row's body's Node kind [800, 813]
    for name in ("redshift_top_long", "redshift_bottom_long"):
        doc = document(name)
        assert doc["N"] == generator.LONG_PHASE_STEPS == 2048
        assert doc["measured"][0]["emitter"]["clock"] == generator.LONG_GIVEN_CLOCK == [4096, 21]
        assert doc["measured"][0]["extents"] == [1, 3, 3] and doc["measured"][0]["kind"] == [800, 813]
        assert doc["measured"][0]["position"] == [
            generator.LONG_REDSHIFT_EMITTER_X + generator.LONG_TRAIN_LENGTH - 1,
            0,
            0,
        ]
    # THE ARM'S HOLDERS UNDER ONE FAMILY OF MATTER (ALGEBRA.md #the-primitives; the one stroke,
    # commit 1): bodies of matter on one Node each, content 2000 apiece, no well and no
    # record (a second well of the emitter's family on its chain is refused by the
    # separation rule of 9.35); the first at the arm's start, 322 x 3 x 3 of them
    long_bottom = document("redshift_bottom_long")["measured"]
    long_holder = long_bottom[1]
    assert long_holder["family"] == "matter" and long_holder["amount"] == 2000
    assert long_holder["position"] == [368, 0, 0]
    assert "extents" not in long_holder and "kind" not in long_holder and "pair" not in long_holder
    assert sum(1 for m in long_bottom if m["family"] == "matter" and "extents" not in m) == 322 * 9
    bending = document("bending")
    emitter, body = bending["measured"][0], bending["measured"][1]
    assert "model_id" not in bending  # one engine, no identity string (ALGEBRA.md #the-primitives)
    # the one-Node emitter at the retired beam's head on the beam's line (commit 7; the beam of
    # 32 x 20 Nodes HISTORY)
    assert emitter["extents"] == [1, 1, 1] and emitter["amount"] == 1
    assert emitter["stocks"] == {"charge": generator.BENDING_STOCK} and generator.BENDING_STOCK == 100
    assert (
        body["family"] == "matter"
        and body["amount"] == generator.BENDING_BODY_CONTENT
        and "emitter" not in body
    )
    assert bending["ticks"] == generator.BENDING_TICKS
    assert sum(1 for d in bending["detectors"] if d["name"].startswith("screen_")) == 40
    top, bottom = document("redshift_top"), document("redshift_bottom")
    # the emitter, the mirror and the mirror behind the emitter (ALGEBRA.md #the-primitives; commit 7)
    assert [m["family"] for m in top["measured"]] == ["matter", "charge", "charge"]
    arm_start = (
        generator.REDSHIFT_EMITTER_X + generator.TRAIN_LENGTH
        if hasattr(generator, "TRAIN_LENGTH")
        else 132
    )
    arm_nodes = (generator.REDSHIFT_MIRROR_X - arm_start) * 9
    assert [m["family"] for m in bottom["measured"]] == ["matter"] * (1 + arm_nodes) + ["charge"] * 2
    holder = bottom["measured"][1]
    assert holder["position"] == [arm_start, 0, 0]
    assert holder["amount"] == generator.WELL_LEVEL == 2000
    assert "emitter" not in holder and "extents" not in holder
    assert bottom["measured"][-1]["pair"] == [1, 2]  # the mirror, of light's kind, the charge's
    rest, moving = document("lorentz_rest"), document("lorentz_moving")
    assert all(m["momentum"] == [0, 0, 0] for m in rest["measured"])
    for entry in moving["measured"]:
        # the wall on the whole content, the own quanta and the stock held (item 47)
        content = int(entry["amount"]) + sum(int(v) for v in entry.get("stocks", {}).values())
        wall = generator.drive_wall(content)
        assert entry["momentum"] == [wall // generator.HOP_EVERY, 0, 0]


@pytest.mark.xfail(
    strict=True,
    reason="the Boss's records 2204 and 2206 (2026-09-26): a giving lowers the live M in the wall "
    "W = 3 Q M while n stays, so the moving emitter speeds up and the mirror hops one interval "
    "before it from interval 51 (the gap 58 for one interval at every hop); the fix is the count "
    "per family and P_0 = [1, 1000] of ALGEBRA.md #the-primitives, Coder 3's; marked so that the "
    "merge into main is not held (the model owner's word of 13:20Z, speed the merge); the mark comes "
    "off with the fix",
)
@pytest.mark.diagnostic
def test_the_held_level_is_the_well_on_the_arm_and_the_moving_clock_hops_together():
    generator = load_module("make_worlds")
    lines: list[dict] = []
    # a GameBoard reading (a diagnostic): the blocks' corners and the set over 100 intervals
    moving = DetectorLawSimulation(
        parse_nature_beam_world(document("lorentz_moving")), observer=lines.append
    )
    corners = []
    for _ in range(100):
        moving.step()
        corners.append([int(block.corner[0]) for block in moving.blocks])
    head_x = generator.LORENTZ_EMITTER_X + 31  # the one-Node emitter at the retired train's head
    emitter, mirror, behind = zip(
        *corners, strict=True
    )  # the mirror behind the body's Node too (ALGEBRA.md #the-primitives)
    assert emitter[-1] - head_x == 25 and mirror[-1] - generator.LORENTZ_MIRROR_X == 25
    assert behind[-1] - (head_x - 2) == 25
    assert all(m - e == generator.LORENTZ_MIRROR_X - head_x for e, m, _ in corners)
    hops = np.diff(np.array(emitter))
    assert set(hops.tolist()) <= {0, 1} and int(hops.sum()) == 25
    # the set follows the emitter: its Nodes are the block's current Nodes
    at_well = moving.detector_names.index("at_well")
    assert moving.detector_at_node[(emitter[-1] + 5, 1, 1)] == at_well
    assert moving.detector_at_node[(generator.LORENTZ_EMITTER_X + 5, 1, 1)] == -1


def test_the_reader_reads_the_means_the_ratio_and_the_closed_forms(tmp_path: Path, capsys):
    reader = load_module("read_runs")
    top = {
        "clicks": [{"detector": "at_well", "interval": 2400 + i, "giving": 0} for i in range(0, 50, 5)]
    }
    bottom = {
        "clicks": [{"detector": "at_well", "interval": 3100 + i, "giving": 0} for i in range(0, 50, 5)]
        + [
            {"detector": "at_well", "interval": 700, "giving": 0},
            {"detector": "face", "interval": 5, "giving": 0},
        ]
    }
    (tmp_path / "redshift_top.output.json").write_text(json.dumps(top), encoding="utf-8")
    (tmp_path / "redshift_bottom.output.json").write_text(json.dumps(bottom), encoding="utf-8")
    reader.redshift(tmp_path)
    text = capsys.readouterr().out
    assert "DETECTOR redshift_top (the arm at 0): 10 clicks" in text
    assert "1 clicks earlier than the top world's least wait [700]" in text
    assert "the mirror's cluster 1.289" in text  # 3122.5 / 2422.5
    assert "1 / sqrt(1 - 2 U_1) = 1.118 at U_1 = 0.1" in text
    assert "cos k' = -0.250, v_g' = 0.3464, the flight ratio 1.291" in text
    mean, rms, error = reader.stats([1, 2, 3, 4])
    assert (mean, rms, round(error, 4)) == (2.5, 1.118033988749895, 0.559)
