"""The helpers of the law's tests: a module loaded by its path (a tool), and the generator's bodies of ALGEBRA.md #the-generator laid on a chain of the universe the tests run on (`UNIVERSE`)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "examples" / "events"
UNIVERSE = EVENTS / "rule.json"  # the rule's own universe: Gamma 6000, T = 32768, the two rows
CHAIN, QUANTA = 48, 50  # a chain of 48 Nodes (x open) and a body of 50 quanta: seven Nodes


def load_file(name: str, path: Path):  # type: ignore[no-untyped-def]
    """The module at `path` loaded under `name` and registered in sys.modules (a tool or a generator)."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def universe_beside(tmp_path: Path, drop: tuple[str, ...] = (), **pairs: list[int]) -> None:
    """The tests' universe copied beside a world as u.json (the families `drop` names left out, a family's pair replaced where `pairs` names it) with the engine's start file as e.json."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    universe["families"] = [family for family in universe["families"] if family["name"] not in drop]
    for family in universe["families"]:
        family["pair"] = pairs.get(family["name"], family["pair"])
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    (tmp_path / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())


def chain_body_world(
    tmp_path: Path,
    tool,
    quanta: int = QUANTA,
    at: tuple[int, ...] = (CHAIN // 2,),
    holds: dict[str, int] | None = None,
    senses: tuple[int, ...] = (),
    taker: bool = False,
    mode: bool = True,
) -> Path:
    """A chain of CHAIN Nodes (x open) with a body of matter declared with `quanta` on each Node of `at` (the last holding `holds` of other families, read by the detector `taker` where asked), rotating in the `senses` given, laid by the generator: the bodies' Nodes with their counts and the mode file beside them; the detectors `left` and `right` on the chain's two end Nodes read the light's count rise there."""
    universe_beside(tmp_path)
    measured: list[dict[str, object]] = [
        dict(family="matter", nodes=[dict(node=[x, 0, 0], count=quanta)]) for x in at
    ]
    if holds:
        measured[-1]["holds"] = holds
    detectors: list[dict[str, object]] = [{"name": "left", "positions": [[0, 0, 0]]}]
    detectors += [{"name": "right", "positions": [[CHAIN - 1, 0, 0]]}]
    detectors += [{"name": "taker", "block": len(at) - 1}] if taker else []
    document = dict(
        shape=[CHAIN, 1, 1], boundary=dict(x="open", y="periodic", z="periodic"), detectors=detectors
    )
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
    """The slit world, a wall across x with one gap at y = 4 on a board of 24 x 9 x 1 (z folded), the packet of light laid by the generator `tool`, in the tests' universe without its row with a gap; `changes` replace the world's keys."""
    universe_beside(folder, drop=("polarisation",))
    path = folder / f"{name}.json"
    path.write_text(json.dumps({**SLIT, "messages": [PACKET], **changes}), encoding="utf-8")
    tool.main(["--input", str(path)])
    return path
