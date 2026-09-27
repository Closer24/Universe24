"""THE CHECK-MODE WORLDS (ALGEBRA.md 9.87 (4), (5); 9.92; 9.98 (3); the Boss's records 2128,
2130 and 2133 (2)): the world files of `examples/events/check_mode/` are the generator's, in
record 2128's words (`universe`, `q`, `stocks`), with no momentum, spin, moment or margin on a
body and none of the world keys 9.90 (3) deletes; a moving body carries its record at both
levels over the whole board; the README's table names every world file and every world file
is in the table; the generator's translation and its screen are checked on small inputs. No
pin: the rows are check-mode rows (9.59 (6)). Every count here is a HOST count."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from tests.worlds import load_file

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "examples" / "events" / "check_mode"
NAMES = (
    "newton_fall",
    "kepler_pair",
    "all_families",
    "coulomb_plus",
    "coulomb_minus",
    "coulomb_neutral",
    "coulomb_neutral_packet",
    "ampere_parallel",
    "ampere_opposite",
    "radiation_pressure",
    "radiation_pressure_beside",
    "train_recoil",
    "point_recoil",
)
MOVING = {
    "kepler_pair": (0, 1),
    "all_families": (0, 1),
    "coulomb_plus": (1,),
    "coulomb_minus": (1,),
    "coulomb_neutral": (1,),
    "coulomb_neutral_packet": (1,),
    "ampere_parallel": (0, 1),
    "ampere_opposite": (0, 1),
}
DELETED_WORLD_KEYS = {
    "law",
    "model_id",
    "K",
    "N",
    "release",
    "width",
    "clock_stamp",
    "detector_law",
    "massive_record",
    "body_record",
    "point_emitter",
    "age_bound",
    "amplitude_bound",
    "node_clock",
    "input",
    "probes",
    "mode_axis",
    "families",
}
DELETED_BLOCK_KEYS = {"momentum", "spin", "moment", "margin", "charge", "held"}


def generator():
    return load_file("check_mode_make_worlds", FOLDER / "make_worlds.py")


def document(name: str) -> dict:
    return json.loads((FOLDER / f"{name}.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", NAMES)
def test_every_world_speaks_record_2128_and_declares_no_momentum_or_spin(name):
    doc = document(name)
    assert doc["universe"] == "examples/events/universe.json"
    assert not DELETED_WORLD_KEYS & set(doc), sorted(DELETED_WORLD_KEYS & set(doc))
    assert set(doc) >= {"shape", "boundary", "ticks", "engine", "measured", "detectors"}
    count = doc["shape"][0] * doc["shape"][1] * doc["shape"][2]
    for number, body in enumerate(doc["measured"]):
        assert not DELETED_BLOCK_KEYS & set(body), (number, sorted(DELETED_BLOCK_KEYS & set(body)))
        assert isinstance(body["q"], int) and "kind" in body and "pair" in body and "clock" in body
        if "emitter" in body:
            assert "stocks" in body and body["stocks"] and "window_read" not in body["emitter"]
            assert "weight" in body["emitter"] or "train" in body["emitter"]
        seed = body["seed"]
        if number in MOVING.get(name, ()):
            # the moving body as its record (9.98 (3)): both levels over the whole board
            assert set(seed) == {"now", "before"} and len(seed["now"]) == len(seed["before"]) == count
            assert seed["now"] != seed["before"]
        else:
            assert isinstance(seed, list) and len(seed) == count  # the standing mode's profile
    if name.startswith(("coulomb", "ampere")):
        names = [d["name"] for d in doc["detectors"]]
        assert len(names) == len(set(names)) == 118 and names[0] == "screen_1"  # pixels, one per Node


def test_the_table_names_every_world_and_every_world_is_in_the_table():
    readme = (FOLDER / "README.md").read_text(encoding="utf-8")
    named = set(re.findall(r"`([a-z_]+)\.json`", readme))
    shipped = {path.stem for path in FOLDER.glob("*.json")}
    assert shipped == set(NAMES)
    assert shipped <= named, sorted(shipped - named)
    assert not (FOLDER / "expectations.json").exists(), "a check-mode row carries no pin (9.59 (6))"


def test_the_heavy_tool_waits_for_the_energy_unit_and_says_why():
    module = generator()
    assert set(module.WAITING) == {"heavy_tool"} and "heavy_tool" not in module.WORLDS
    assert "P_0 = [1, 1000]" in module.WAITING["heavy_tool"][1]
    assert module.HEAVY_QUANTA == 1_000_000 > module.GAMMA


def test_the_translation_writes_the_words_and_drops_the_deleted_keys():
    module = generator()
    today = {
        "law": "beam",
        "model_id": "x",
        "shape": [4, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "ticks": 3,
        "N": 64,
        "engine": "examples/events/engine_start.json",
        "families": [{"name": "matter"}],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "matter",
                "amount": 2,
                "momentum": [1, 0, 0],
                "held": {"charge": 7},
                "charge": -3,
                "spin": [0, 0, 1],
                "moment": [0, 0, 0],
                "margin": "pin",
                "emitter": {"family": "charge", "weight": 4, "window_read": 99},
            }
        ],
        "detectors": [],
    }
    out = module.translate(today)
    assert list(out) == ["shape", "boundary", "ticks", "engine", "universe", "measured", "detectors"]
    assert out["universe"] == "examples/events/universe.json"
    body = out["measured"][0]
    assert body == {
        "position": [0, 0, 0],
        "family": "matter",
        "amount": 2,
        "stocks": {"charge": 7},
        "q": -3,
        "emitter": {"family": "charge", "weight": 4},
    }
    assert module.screen(9, [10, 5, 2]) == [
        {"name": "screen_1", "positions": [[9, 1, 0], [9, 1, 1]]},
        {"name": "screen_2", "positions": [[9, 2, 0], [9, 2, 1]]},
        {"name": "screen_3", "positions": [[9, 3, 0], [9, 3, 1]]},
    ]
    assert (
        module.dumps({"a": [1, -2, 3], "b": {"c": [4]}})
        == '{\n "a": [1, -2, 3],\n "b": {\n  "c": [4]\n }\n}\n'
    )


def test_the_pair_and_the_charges_are_the_all_families_worlds():
    kepler, whole = document("kepler_pair"), document("all_families")
    for doc in (kepler, whole):
        assert doc["shape"] == [48, 48, 48] and doc["boundary"] == {
            "x": "open",
            "y": "open",
            "z": "open",
        }
        a, b = doc["measured"]
        assert a["amount"] == b["amount"] == 2000 and a["extents"] == b["extents"] == [5, 5, 5]
        assert b["position"][0] - a["position"][0] == 10  # 10 Links apart (9.87 (5))
    assert [m["q"] for m in kepler["measured"]] == [0, 0]
    assert [m["q"] for m in whole["measured"]] == [50, 50]  # Lambda Q = 50 at Lambda = 1
    a = whole["measured"][0]
    assert a["stocks"] == {"charge": 200} and a["emitter"]["weight"] == 4 and "train" not in a["emitter"]
    assert whole["detectors"] == []  # the faces are the counters (9.92 (2)); no D
    newton = document("newton_fall")
    a, b = newton["measured"]
    assert b["position"][0] - a["position"][0] == 20  # from rest at 20 Links (9.87 (4))
    assert isinstance(a["seed"], list) and isinstance(b["seed"], list)  # the standing mode
