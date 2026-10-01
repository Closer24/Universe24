"""The helpers of the law's tests: a module loaded by its path (a tool; the generator, the back-in-time gate and the runner loaded once for every test), and the generator's bodies of ALGEBRA.md #the-generator laid on a chain of the universe the tests run on (`UNIVERSE`)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "examples" / "events"
UNIVERSE = EVENTS / "rule.json"  # the rule's own universe: Gamma 6000, T = 32768, the law's rows
CHAIN, QUANTA = 48, 50  # a chain of 48 Nodes (x open) and a body of 50 quanta: seven Nodes
CHARGED = {"name": "charged", "pair": [4000, 6000], "dimension": 2}  # matter's pair as a plane


def load_file(name: str, path: Path):  # type: ignore[no-untyped-def]
    """The module at `path` loaded under `name` and registered in sys.modules (a tool or a generator)."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def refused(match: str, call, *args, **keys):  # type: ignore[no-untyped-def]
    """The call on its arguments refused by name: a ValueError whose message matches `match`."""
    with pytest.raises(ValueError, match=match):
        call(*args, **keys)


TOOLS = ("pixel_mode", "back_in_time", "run_inputs")  # the generator, the back-in-time gate, the runner
TOOL, BACK, RUN = (load_file(name, ROOT / "tools" / f"{name}.py") for name in TOOLS)


def universe_beside(tmp_path, drop=(), charged=False, **pairs):  # type: ignore[no-untyped-def]
    """The tests' universe copied beside a world as u.json (the families `drop` names left out, a family's pair replaced where `pairs` names it, the charged matter row, matter's pair as a plane, added where `charged`) with the engine's start file as e.json."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    universe["families"] = [family for family in universe["families"] if family["name"] not in drop]
    universe["families"] += [dict(CHARGED)] if charged else []
    for family in universe["families"]:
        family["pair"] = pairs.get(family["name"], family["pair"])
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    (tmp_path / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())


def chain_body_world(tmp_path, tool, quanta=QUANTA, at=(CHAIN // 2,), senses=(), taker=False, mode=True):  # type: ignore[no-untyped-def]
    """A chain of CHAIN Nodes (x open) with a body of matter declared with `quanta` on each Node of `at` (the last read by the detector `taker` where asked), a body rotating in the `senses` given of the charged family (matter's pair as a plane), laid by the generator: the bodies' Nodes with their counts and the mode file beside them; the detectors `left` and `right`, two Nodes each at the chain's two ends (never one Node), report the light's inflow there."""
    turning = [bool(senses[i]) if i < len(senses) else False for i in range(len(at))]
    universe_beside(tmp_path, charged=any(turning))
    measured: list[dict[str, object]] = [
        dict(family=CHARGED["name"] if turns else "matter", nodes=[dict(node=[x, 0, 0], count=quanta)])
        for x, turns in zip(at, turning, strict=True)
    ]
    detectors: list[dict[str, object]] = [{"name": "left", "positions": [[0, 0, 0], [1, 0, 0]]}]
    detectors += [{"name": "right", "positions": [[CHAIN - 2, 0, 0], [CHAIN - 1, 0, 0]]}]
    detectors += [{"name": "taker", "block": len(at) - 1}] if taker else []
    document = dict(shape=[CHAIN, 1, 1], detectors=detectors)
    document["boundary"] = dict(x="open", y="periodic", z="periodic")
    document.update(ticks=400, face_depth=1, universe="u.json", engine="e.json", measured=measured)
    (world := tmp_path / "chain.json").write_text(json.dumps(document), encoding="utf-8")
    if mode:
        tool.main(["--input", str(world), "--sense", *(str(sense) for sense in senses)])
    return world


SLIT = dict(shape=[24, 9, 1], boundary=dict(x="open", y="open", z="periodic"), face_depth=1, ticks=24)
SLIT.update(universe="u.json", engine="e.json", measured=[], detectors=[])
SLIT["faces"] = [{"axis": "x", "at": 12, "gaps": [{"y": [4, 4], "z": [0, 0]}]}]
PACKET = {"family": "charge", "along": "x", "wave": [1, 4], "amplitude": 1328}
PACKET.update(top={"x": [5, 5], "y": [0, 8], "z": [0, 0]}, edge={"x": 4, "y": 0, "z": 0})


def slit_world(folder: Path, tool, name: str = "slit", **changes: object) -> Path:  # type: ignore[no-untyped-def]
    """The slit world, a wall across x with one gap at y = 4 on a board of 24 x 9 x 1 (z folded), the packet of light laid by the generator `tool`, in the tests' universe; `changes` replace the world's keys."""
    universe_beside(folder)
    path = folder / f"{name}.json"
    path.write_text(json.dumps({**SLIT, "messages": [PACKET], **changes}), encoding="utf-8")
    tool.main(["--input", str(path)])
    return path
