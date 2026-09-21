"""The birth wheel at a declared rate (2026-09-21; the model owner's decision,
record 180 of docs/LOG_2026-09-20.md on record 163 (3); the mathematician's
docs/designs/fraction_free/TWO_SLITS.md section 8 with `wheel_map.py`;
BEAM_LAW note 46): the wheel is one `Count` row of the lamp's counts table,
declared on the lamp as `wheel` [r, W]; u = ordinal x r mod W is written on
the record at birth (the accumulator before the birth advances it); the
rungs at the click are (2 W C_k + T) // (2 T) and the cell [u < b_k]. The
expected integers of docs/TEST_EXPECTATIONS.md ("The birth wheel"), written
down before the first run:

(a) the parse: a lamp without `wheel` is refused naming the key; a bare
    integer, [0, 64] and [1, 0] are refused naming `lamp.wheel`; [2531,
    4096] parses to (2531, 4096) and [1, 64] to (1, 64); every world file
    of the register that declares a lamp declares its wheel (the entity
    definitions included);
(b) the case [1, N]: a lamp of [1, 64] on +x to a counter 10 Links away,
    40 intervals: the birth lines' u are 0, 1, 2, ... (the ordinal less
    one), the rows' `birth` column the same, every gather's last rung 64,
    the lamp's `acc` carrying `wheel` = its births mod 64 and the counter's
    `acc` no `wheel`;
(c) the golden rate [2531, 4096] on the same bar: the first ten births' u
    are 0, 2531, 966, 3497, 1932, 367, 2898, 1333, 3864, 2299 ((k x 2531)
    mod 4096, k from 0), the rows' `birth` the same and their phase at the
    birth u mod 64 (0, 35, 6, 41, 12, 47, 18, 53, 24, 59), every gather's
    last rung 4096 and its u the birth's, the `acc` `wheel` = (births x
    2531) mod 4096;
(d) the cell by the wheel: a lamp on +x and -x (one quantum, two paths of
    amount 1) to two counters `a` and `b` 5 Links away, two cells of equal
    weight, the rungs [2048, 4096]: the first ten records click a, b, a, b,
    a, a, b, a, b, b (u < 2048 for the ordinals 0, 2, 4, 5, 7), where the
    same lamp under [1, 64] (the rungs [32, 64]) sends the first 32
    records to a and the next 32 to b;
(e) the replay: `tools/amplitude_path.replay` on the runner's run of (d)
    under [2531, 4096] returns `run.json`'s `world`, the wheel read from
    the world's lamp.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.run import execute_nature_beam_run

ROOT = Path(__file__).resolve().parents[1]
N = 64
K = 1 << 20
GOLDEN = [2531, 4096]
GOLDEN_U = [(k * 2531) % 4096 for k in range(10)]


def world(
    wheel: list[int], directions: list[list[int]], counters: dict[str, list[int]], ticks: int = 40
):
    return {
        "law": "beam",
        "model_id": "beam-birth-wheel-test",
        "shape": [11, 1, 1],
        "boundary": {"y": "periodic", "z": "periodic"},
        "ticks": ticks,
        "K": K,
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "light", "quantum": 1}],
        "measured": [
            {
                "position": [5, 0, 0] if len(directions) == 2 else [0, 0, 0],
                "family": "light",
                "amount": K,
                "fixed": True,
                "lamp": {"rate": [1, 1], "wheel": wheel, "directions": directions},
            },
            *(
                {"position": position, "family": "light", "amount": 1, "fixed": True}
                for position in counters.values()
            ),
        ],
        "detectors": [
            {"name": name, "positions": [position], "reading": "sum"}
            for name, position in counters.items()
        ],
    }


def run(declared: dict[str, object]) -> tuple[NatureBeamSimulation, list[dict[str, object]]]:
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(declared), observer=lines.append)
    for _ in range(int(declared["ticks"])):  # type: ignore[call-overload]
        simulation.step()
    return simulation, lines


def test_the_wheel_is_declared_on_every_lamp():
    """(a)."""
    base = world([1, N], [[1, 0, 0]], {"counter": [10, 0, 0]})
    lamp = base["measured"][0]  # type: ignore[index]
    without = {**lamp, "lamp": {"rate": [1, 1], "directions": [[1, 0, 0]]}}  # type: ignore[dict-item]
    with pytest.raises(ValueError, match=r"lamp lacks keys: wheel"):
        parse_nature_beam_world({**base, "measured": [without, *base["measured"][1:]]})  # type: ignore[index]
    for bad, message in (
        (64, r"lamp\.wheel must be \[r, W\]"),
        ([0, 64], r"lamp\.wheel numerator"),
        ([1, 0], r"lamp\.wheel denominator"),
    ):
        with pytest.raises(ValueError, match=message):
            parse_nature_beam_world(
                {
                    **base,
                    "measured": [
                        {**lamp, "lamp": {**lamp["lamp"], "wheel": bad}},
                        *base["measured"][1:],
                    ],
                }  # type: ignore[index]
            )
    assert parse_nature_beam_world(base).measured[0].lamp.wheel == (1, N)  # type: ignore[union-attr]
    golden = world(GOLDEN, [[1, 0, 0]], {"counter": [10, 0, 0]})
    assert parse_nature_beam_world(golden).measured[0].lamp.wheel == (2531, 4096)  # type: ignore[union-attr]
    missing = []
    for path in sorted((ROOT / "examples" / "events").rglob("*.json")):
        text = path.read_text(encoding="utf-8")
        if '"lamp"' not in text:
            continue
        lamps: list[dict[str, object]] = []
        collect(json.loads(text), lamps)
        if any("wheel" not in lamp for lamp in lamps):
            missing.append(str(path.relative_to(ROOT)))
    assert missing == []


def collect(node: object, lamps: list[dict[str, object]]) -> None:
    """Every `lamp` object of a document, the entity definitions' included."""
    if isinstance(node, dict):
        if "lamp" in node and isinstance(node["lamp"], dict):
            lamps.append(node["lamp"])
        for value in node.values():
            collect(value, lamps)
    elif isinstance(node, list):
        for value in node:
            collect(value, lamps)


def test_the_case_one_over_n_is_the_count_of_births():
    """(b)."""
    simulation, lines = run(world([1, N], [[1, 0, 0]], {"counter": [10, 0, 0]}))
    births = [line for line in lines if line["event"] == "birth"]
    assert len(births) >= 30
    assert [line["u"] for line in births[:70]] == [k % N for k in range(len(births[:70]))]
    gathers = [line for line in lines if line["event"] == "gather"]
    assert len(gathers) >= 10
    assert all(gather["cells"][-1][1] == N for gather in gathers)
    lamp = next(entry for entry in simulation.measured.values() if entry.lamp_wheel is not None)
    counter = next(entry for entry in simulation.measured.values() if entry.lamp_wheel is None)
    assert lamp.counts.one("wheel") == lamp.births % N
    assert lamp.state()["acc"]["wheel"] == lamp.births % N
    assert "wheel" not in counter.state()["acc"]
    rows = [line for line in lines if line["event"] == "click" and "record" in line]
    assert rows and all(line["u"] == ((line["record"] & 0xFFFFFFFF) - 1) % N for line in rows)


def test_the_golden_rate_writes_the_wheel_on_the_record():
    """(c)."""
    simulation, lines = run(world(GOLDEN, [[1, 0, 0]], {"counter": [10, 0, 0]}))
    births = [line for line in lines if line["event"] == "birth"]
    assert (
        [line["u"] for line in births[:10]]
        == GOLDEN_U
        == [
            0,
            2531,
            966,
            3497,
            1932,
            367,
            2898,
            1333,
            3864,
            2299,
        ]
    )
    by_record = {line["record"]: line["u"] for line in births}
    clicks = [line for line in lines if line["event"] == "click" and "record" in line]
    assert clicks and all(line["u"] == by_record[line["record"]] for line in clicks)
    # The row's phase at the birth is u mod N (the path phase 0 at a click
    # 10 Links away with no phase per Link: the click's phase is u mod N).
    first_ten = [line for line in clicks if (line["record"] & 0xFFFFFFFF) <= 10]
    assert sorted({(line["record"] & 0xFFFFFFFF, line["phase"]) for line in first_ten}) == [
        (k + 1, u % N) for k, u in enumerate(GOLDEN_U)
    ]
    assert [u % N for u in GOLDEN_U] == [0, 35, 6, 41, 12, 47, 18, 53, 24, 59]
    gathers = [line for line in lines if line["event"] == "gather"]
    assert len(gathers) >= 10
    assert all(gather["cells"][-1][1] == 4096 for gather in gathers)
    assert all(gather["u"] == by_record[gather["record"]] for gather in gathers)
    lamp = next(entry for entry in simulation.measured.values() if entry.lamp_wheel is not None)
    assert lamp.counts.one("wheel") == (lamp.births * 2531) % 4096 == lamp.state()["acc"]["wheel"]


def chosen_of(lines: list[dict[str, object]], count: int) -> list[str]:
    gathers = sorted(
        (line for line in lines if line["event"] == "gather"), key=lambda line: int(line["record"])
    )
    return [str(gather["chosen"][0][0]) for gather in gathers[:count]]  # type: ignore[index]


def test_the_cell_is_read_on_the_wheel():
    """(d)."""
    two = {"a": [10, 0, 0], "b": [0, 0, 0]}
    _, lines = run(world(GOLDEN, [[1, 0, 0], [-1, 0, 0]], two, ticks=60))
    gathers = [line for line in lines if line["event"] == "gather"]
    assert len(gathers) >= 40
    assert all(gather["cells"][0][1] == 2048 and gather["cells"][1][1] == 4096 for gather in gathers)
    assert chosen_of(lines, 10) == ["a", "b", "a", "b", "a", "a", "b", "a", "b", "b"]
    _, lines = run(world([1, N], [[1, 0, 0], [-1, 0, 0]], two, ticks=100))
    gathers = [line for line in lines if line["event"] == "gather"]
    assert len(gathers) >= 64
    assert all(gather["cells"][0][1] == 32 and gather["cells"][1][1] == 64 for gather in gathers)
    assert chosen_of(lines, 64) == ["a"] * 32 + ["b"] * 32


def test_the_replay_reads_the_wheel_from_the_lamp(tmp_path: Path):
    """(e)."""
    declared = world(GOLDEN, [[1, 0, 0], [-1, 0, 0]], {"a": [10, 0, 0], "b": [0, 0, 0]}, ticks=60)
    source = tmp_path / "wheel.json"
    source.write_text(json.dumps(declared), encoding="utf-8")
    out = tmp_path / "run"
    out.mkdir()
    execute_nature_beam_run(parse_nature_beam_world(declared), source.read_bytes(), out, "test", 60)
    spec = importlib.util.spec_from_file_location("amplitude_path", ROOT / "tools" / "amplitude_path.py")
    assert spec is not None and spec.loader is not None
    tool = importlib.util.module_from_spec(spec)
    sys.modules["amplitude_path"] = tool
    spec.loader.exec_module(tool)
    layer, gathers = tool.replay(out)
    record = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert gathers == record["world"]
    assert len(gathers) >= 40 and all(gather["cells"][-1][1] == 4096 for gather in gathers)
