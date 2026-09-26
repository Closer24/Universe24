"""THE RUNS TOWARD NATURE, rows (1) to (3) (ALGEBRA.md 9.59 (0) to (3); BUILD.md section 26
item 41): the five world files of `examples/events/toward_nature/` are the generator's, carry
the declared integers (Gamma 10^4, the well's level 2000 on the arm's free Nodes, the momenta
one quarter of each block's drive wall, the bending's beam 20 wide with its body's content
set for U_b = 0.1 on the beam's line) and no pin; the moving clock's two blocks hop together
(the emitter, its mirror and its set one Link every 4 intervals, GAMEBOARD); the reader's
arithmetic on a written output (the mean, the standard error, the ratio and the closed forms
it is set beside, COMPUTATION). No run against a pin: the rows are diagnostics (9.59 (6))."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.world import parse_nature_beam_world

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "examples" / "events" / "toward_nature"
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


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(f"toward_nature_{name}", FOLDER / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"toward_nature_{name}"] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def document(name: str) -> dict:
    return json.loads((FOLDER / f"{name}.json").read_text(encoding="utf-8"))


def test_the_four_worlds_carry_the_declared_integers_and_no_pin():
    generator = load_module("make_worlds")
    assert not (FOLDER / "expectations.json").exists(), "a diagnostic row carries no pin (9.59 (6))"
    for name in NAMES:
        doc = document(name)
        world = parse_nature_beam_world(doc)
        # the integers from the families file alone (item 59)
        assert doc["families"] == "examples/events/families.json" and "node_clock" not in doc
        assert world.node_clock == generator.NODE_CLOCK == 10_000
        if name == "bending":
            continue
        assert doc["detectors"][0]["name"] == "at_well" and doc["detectors"][0]["block"] == 0
        assert world.shape[1:] == (3, 3)
    # the long-wave pair (ALGEBRA.md 9.62 (1)): the given clock [4096, 21] on N = 2048, the
    # wavelength 21 Links (k = 0.299), the train 168 Nodes, the emitter one train from the face
    for name in ("redshift_top_long", "redshift_bottom_long"):
        doc = document(name)
        assert doc["N"] == generator.LONG_PHASE_STEPS == 2048
        assert doc["measured"][0]["emitter"]["clock"] == generator.LONG_GIVEN_CLOCK == [4096, 21]
        assert doc["measured"][0]["extents"] == [generator.LONG_TRAIN_LENGTH, 3, 3] == [168, 3, 3]
        assert doc["measured"][0]["position"] == [generator.LONG_REDSHIFT_EMITTER_X, 0, 0]
    long_holder = document("redshift_bottom_long")["measured"][1]
    assert long_holder["family"] == "well" and long_holder["amount"] == 2000
    assert long_holder["position"] == [368, 0, 0] and long_holder["extents"] == [322, 3, 3]
    bending = document("bending")
    emitter, body = bending["measured"][0], bending["measured"][1]
    assert bending["model_id"] == "beam-toward-nature-bending-v1"
    assert emitter["extents"] == [32, 20, 1] and emitter["amount"] == 1
    assert emitter["held"] == {"light": generator.BENDING_STOCK} and generator.BENDING_STOCK == 100
    assert (
        body["family"] == "dark"
        and body["amount"] == generator.BENDING_BODY_CONTENT
        and "emitter" not in body
    )
    assert bending["ticks"] == generator.BENDING_TICKS
    assert sum(1 for d in bending["detectors"] if d["name"].startswith("screen_")) == 40
    top, bottom = document("redshift_top"), document("redshift_bottom")
    assert [m["family"] for m in top["measured"]] == ["matter", "light"]
    assert [m["family"] for m in bottom["measured"]] == ["matter", "well", "light"]
    holder = bottom["measured"][1]
    arm_start = (
        generator.REDSHIFT_EMITTER_X + generator.TRAIN_LENGTH
        if hasattr(generator, "TRAIN_LENGTH")
        else 132
    )
    assert holder["position"] == [arm_start, 0, 0]
    assert holder["extents"] == [generator.REDSHIFT_MIRROR_X - arm_start, 3, 3]
    assert holder["amount"] == generator.WELL_LEVEL == 2000
    assert "emitter" not in holder
    rest, moving = document("lorentz_rest"), document("lorentz_moving")
    assert all(m["momentum"] == [0, 0, 0] for m in rest["measured"])
    for entry in moving["measured"]:
        # the wall on the whole content, the own quanta and the stock held (item 47)
        content = int(entry["amount"]) + sum(int(v) for v in entry.get("held", {}).values())
        wall = generator.drive_wall(content)
        assert entry["momentum"] == [wall // generator.HOP_EVERY, 0, 0]


def test_the_held_level_is_the_well_on_the_arm_and_the_moving_clock_hops_together():
    generator = load_module("make_worlds")
    lines: list[dict] = []
    bottom = DetectorLawSimulation(
        parse_nature_beam_world(document("redshift_bottom")), observer=lines.append
    )
    level = bottom.level_of("content")
    arm_start = generator.REDSHIFT_EMITTER_X + 32
    assert (
        int(level[arm_start, 1, 1]) == 2000 and int(level[generator.REDSHIFT_MIRROR_X - 1, 1, 1]) == 2000
    )
    # the emitter's one own quantum beside its stock of 64 at its Nodes (item 47)
    assert int(level[generator.REDSHIFT_EMITTER_X + 10, 1, 1]) == 65
    assert int(level[generator.REDSHIFT_MIRROR_X + 10, 1, 1]) == 0  # beyond the mirror, free
    moving = DetectorLawSimulation(
        parse_nature_beam_world(document("lorentz_moving")), observer=lines.append
    )
    corners = []
    for _ in range(100):
        moving.step()
        corners.append([int(block.corner[0]) for block in moving.blocks])
    emitter, mirror = zip(*corners, strict=True)
    assert (
        emitter[-1] - generator.LORENTZ_EMITTER_X == 25 and mirror[-1] - generator.LORENTZ_MIRROR_X == 25
    )
    assert all(m - e == generator.LORENTZ_MIRROR_X - generator.LORENTZ_EMITTER_X for e, m in corners)
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
