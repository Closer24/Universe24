"""The helpers of the law's tests: a module loaded by its path (a tool), and the generator's body of ALGEBRA.md #the-generator laid by the pixel tool on the rule's own universe (examples/events/planck.json)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_file(name: str, path: Path):  # type: ignore[no-untyped-def]
    """The module at `path` loaded under `name` and registered in sys.modules (a tool or a generator)."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


BODY_24 = 24  # a body of the generator at Gamma 24: bound above the band's top, below its collapse at 48 where the Link's pace Gamma - 2 c reaches 0 (tests/test_pixel_mode.py)


def body_at_24(tmp_path: Path, tool, quanta: int = BODY_24, centre=(6, 6, 6), mode: bool = True) -> Path:
    """The rule's own universe (examples/events/planck.json: T = 64, binding [23, 24] at 2, gravity at 10) copied beside a world of one body declared on one Node with `quanta` at `centre` on an open box of 13; the generator lays the body over its Nodes and writes its mode file when asked."""
    events = ROOT / "examples" / "events"
    (tmp_path / "u.json").write_bytes((events / "planck.json").read_bytes())
    (tmp_path / "e.json").write_bytes((events / "engine_start.json").read_bytes())
    body = dict(family="matter", nodes=[dict(node=list(centre), count=quanta)], momentum=[0, 0, 0])
    body.update(momentum_before=[0, 0, 0], phase_denominator=1024)
    document = dict(shape=[13, 13, 13], boundary=dict(x="open", y="open", z="open"), detectors=[])
    document.update(ticks=64, N=1024, face_depth=1, universe="u.json", engine="e.json", measured=[body])
    (world := tmp_path / "body.json").write_text(json.dumps(document), encoding="utf-8")
    if mode:
        tool.main(["--input", str(world)])  # the body's Nodes and the record Rule3 makes of them
    return world
