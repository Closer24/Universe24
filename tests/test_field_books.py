"""Experiment E11, the field's books (docs/EXPERIMENTS.md): the shell reader of
examples/nature/e11_field_books/profile.py pinned in isolation on a tiny world,
the point source of `make_worlds.profile_world` on a 9^3 open board about
(4, 4, 4) under the dense mode, for two ticks and for four.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("The field's books")
before the first run, from the release and the split table by hand: at tick 1
the six neighbours each hold one ray of 4096 on the outward heading; at tick 2
each of those has been split (2234 forward, 372 on each other heading, the
remainder 22 elevenths, two whole quanta, in the registers) and received the
second release.
"""

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
WORLDS = ROOT / "examples/nature/e11_field_books"
SHAPE = [9, 9, 9]
CENTRE = [4, 4, 4]
RELEASE = 4096
# The shells of the 9^3 box about its centre: 4k^2 + 2 Nodes on the L1 shell k
# (every shell to k = 4 lies inside the box), and the Nodes at rounded distance k.
L1_COUNTS = [1, 6, 18, 38, 66]
EUCLID_COUNTS = [1, 18, 62, 98, 210]
# After tick 2. L1 shell 1: the second release in flight, 6 x 4096, and two
# quanta of registers per Node (7 + 5 x 3 elevenths); shell 2: the six axis
# Nodes with the forward share 2234 and the twelve (1, 1, 0) Nodes with two
# transverse shares, 372 + 372; the radial momentum's integer dot 6 x 2234 x 2
# + 12 x 744 and its real sum 13404 + 8928 / sqrt 2; the flux across level 1
# the whole content of shell 2 (all of it arrived from shell 1), across level 0
# the release less the sink's 6 x 372; the ledger 2 x 24576 = 46908 + 12 + 2232.
FORWARD = RELEASE * 6 // 11
SIDE = RELEASE // 11
SHELL_1_TICK_2 = {
    "flight": 6 * RELEASE,
    "registers": 12,
    "radial_dot": 6 * RELEASE,
    "flux": 6 * FORWARD + 12 * 2 * SIDE,
}
SHELL_2_TICK_2 = {
    "flight": 6 * FORWARD + 12 * 2 * SIDE,
    "registers": 0,
    "radial_dot": 6 * FORWARD * 2 + 12 * 2 * SIDE,
    "radial": 6 * FORWARD + 12 * 2 * SIDE / np.sqrt(2),
    "flux": 0,
}
# The Euclidean shell 1 holds the six axis Nodes and the twelve (1, 1, 0) Nodes,
# shell 2 the six (2, 0, 0) Nodes (the (1, 1, 1) and (2, 1, 0) Nodes are still
# dark); the flux across level 1 is what reached (2, 0, 0) from (1, 0, 0).
EUCLID_1_TICK_2 = {"flight": 6 * RELEASE + 12 * 2 * SIDE, "registers": 12, "flux": 6 * FORWARD}
EUCLID_2_TICK_2 = {"flight": 6 * FORWARD, "registers": 0, "radial_dot": 6 * FORWARD * 2, "flux": 0}
LEDGER_TICK_2 = {
    "sourced": 2 * 6 * RELEASE,
    "flight": 46908,
    "registers": 12,
    "escaped": 0,
    "absorbed": 6 * SIDE,
}
FLUX_0_TICK_2 = 6 * RELEASE - 6 * SIDE


def load_script(name):
    path = WORLDS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"e11_field_books_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def tiny_world():
    document = load_script("make_worlds").profile_world()
    document["shape"] = list(SHAPE)
    document["external_bodies"][0]["position"] = list(CENTRE)
    document["ticks"] = 4
    return document


def test_e11_worlds_are_what_the_generator_writes():
    make_worlds = load_script("make_worlds")
    generated = dict(make_worlds.cases())
    assert list(generated) == ["point_source", "books", "books_axis"]
    for name, document in generated.items():
        text = (WORLDS / f"{name}.json").read_text(encoding="utf-8")
        assert text == json.dumps(document, indent=1) + "\n", name
    point = generated["point_source"]
    assert point["shape"] == [49, 49, 49] and point["ticks"] == 192 and point["dense_field"] is True
    assert point["external_bodies"] == [
        {
            "position": [24, 24, 24],
            "family": "proton",
            "amount": 1 << 20,
            "charge": 3,
            "momentum_table": {"light": 1},
        }
    ]
    light = next(f for f in point["spatial_fields"] if f["field"] == "light")
    assert (light["field_of"], light["release"], light["spread"]) == (
        "proton",
        [1, 256],
        [6, 1, 1, 1, 1, 1],
    )
    books = generated["books"]
    assert books["shape"] == [21, 21, 21] and books["ticks"] == 36 and books["dense_field"] is True
    assert books["seeds"] == [{"position": [0, 14, 10], "type": "electron_lamp"}]
    assert books["ray_interactions"][0]["momentum_table"] == {"light": -1}
    assert books["external_bodies"][0]["position"] == [10, 10, 10]
    assert books["external_bodies"][0]["momentum_table"] == {"light": -1}
    assert not any(f.get("field_of") == "electron" for f in books["spatial_fields"])
    axis = generated["books_axis"]
    assert "dense_field" not in axis
    assert "spread" not in next(f for f in axis["spatial_fields"] if f["field"] == "light")
    stripped = {k: v for k, v in books.items() if k not in ("dense_field", "model_id", "spatial_fields")}
    assert stripped == {k: v for k, v in axis.items() if k not in ("model_id", "spatial_fields")}


def test_e11_shell_reader_on_a_tiny_world():
    profile = load_script("profile")
    document = tiny_world()
    d = profile.offsets(SHAPE, CENTRE)
    assert profile.shell_counts(profile.l1_level(d), 4) == L1_COUNTS
    assert profile.shell_counts(profile.euclid_level(d), 4) == EUCLID_COUNTS
    assert profile.diagonal_node("l1", 3) == (2, 1, 0)
    assert profile.diagonal_node("euclid", 2) == (1, 1, 1)
    assert profile.diagonal_node("euclid", 3) == (2, 2, 0)
    record = profile.run_world(document, ticks=2, kmax=4, log=None, with_mean_field=True)
    assert record["counts"] == {"l1": L1_COUNTS, "euclid": EUCLID_COUNTS}
    assert record["dense_field"] and record["arrays_agree_with_inventory"]
    assert record["balanced_every_tick"] and record["shell_sum_equals_current"]
    ledger = record["ledger"][-1]
    assert {k: ledger[k] for k in LEDGER_TICK_2} == LEDGER_TICK_2
    assert (
        ledger["sourced"]
        == ledger["flight"] + ledger["registers"] + ledger["escaped"] + ledger["absorbed"]
    )
    assert ledger["body_momentum"] == [0, 0, 0] and ledger["momentum_current"] == [0, 0, 0]
    assert record["flux_0"] == FLUX_0_TICK_2
    l1 = record["profiles"]["l1"]["engine"]
    assert {k: l1[0][k] for k in SHELL_1_TICK_2} == SHELL_1_TICK_2
    assert l1[0]["total"] == 6 * RELEASE + 12 and l1[0]["radial"] == 6 * RELEASE
    assert {k: l1[1][k] for k in ("flight", "registers", "radial_dot", "flux")} == {
        k: SHELL_2_TICK_2[k] for k in ("flight", "registers", "radial_dot", "flux")
    }
    assert abs(l1[1]["radial"] - SHELL_2_TICK_2["radial"]) < 1e-6
    assert l1[2]["total"] == 0 and l1[3]["total"] == 0
    assert l1[0]["axis"]["momentum"] == [RELEASE, 0, 0]
    assert l1[1]["axis"]["momentum"] == [FORWARD, 0, 0]
    assert l1[1]["diagonal"] == {
        "node": [1, 1, 0],
        "momentum": [SIDE, SIDE, 0],
        "radial": 2 * SIDE / np.sqrt(2),
        "content": 2 * SIDE,
        "registers": 0,
    }
    euclid = record["profiles"]["euclid"]["engine"]
    assert {k: euclid[0][k] for k in EUCLID_1_TICK_2} == EUCLID_1_TICK_2
    assert {k: euclid[1][k] for k in EUCLID_2_TICK_2} == EUCLID_2_TICK_2
    assert record["shell_totals_l1"] == [
        [0, 6 * RELEASE, 0, 0, 0],
        [0, 6 * RELEASE + 12, SHELL_2_TICK_2["flight"], 0, 0],
    ]
    # The mean field at the same tick: the same shells to the fraction the
    # floors and the registers hold back (the split's mean is exact).
    mean = record["profiles"]["l1"]["mean_field_tick"]
    assert mean[0]["flight"] == 6 * RELEASE
    assert abs(mean[1]["flight"] - (6 * RELEASE * 6 / 11 + 12 * 2 * RELEASE / 11)) < 1e-6
    assert abs(mean[1]["flight"] - (l1[1]["flight"] + l1[0]["registers"])) < 12
    steady = record["profiles"]["l1"]["mean_field_steady"]
    # Gauss on the lattice: the steady flux is the same through every shell
    # inside the box, the effective source.
    source = record["mean_field"]["effective_source"]
    assert all(abs(steady[i]["flux"] - source) < 1e-8 * source for i in range(3))
    slopes = record["profiles"]["l1"]["slopes"]["engine"]
    assert [s["slope"] is None for s in slopes["per_node"]] == [False, True, True]
    # Four ticks: the identity still exact, the shells' sum still the ledger's.
    four = profile.run_world(document, ticks=4, kmax=4, log=None, with_mean_field=False)
    assert four["balanced_every_tick"] and four["shell_sum_equals_current"]
    assert four["ledger"][-1]["sourced"] == 4 * 6 * RELEASE
    assert four["ledger"][-1]["escaped"] == 0
    assert sum(four["shell_totals_l1"][-1]) == four["ledger"][-1]["current"]
    assert four["profiles"]["l1"]["engine"][3]["flux_in"] == 0
    assert (
        four["profiles"]["l1"]["engine"][0]["flux"]
        == four["profiles"]["l1"]["engine"][0]["flux_out"]
        - four["profiles"]["l1"]["engine"][0]["flux_in"]
    )
