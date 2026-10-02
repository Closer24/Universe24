"""The helpers of the law's tests: a module loaded by its path (a tool; the generator, the back-in-time gate and the runner loaded once for every test), and the generator's bodies of ALGEBRA.md #the-generator laid on a chain of the universe the tests run on (`UNIVERSE`); the chain is the shortest that holds the body of 50 quanta (about eleven Nodes about its centre) and the end detectors with their regions apart, since the lay's cost is the start's relaxation over the chain's length squared, and every bound the tests put on the chain is per Node, the same on any length."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from event_universe.loader.derived import Row

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "examples" / "events"
UNIVERSE = EVENTS / "rule.json"  # the rule's own universe: Gamma 6000, T = 32768, the law's rows
CHAIN, QUANTA = 24, 50  # the shortest chain (x open) holding the body of 50 and the end detectors apart
CHARGED = {"name": "charged", "pair": [4000, 6000], "dimension": 2}  # matter's pair as a plane
CHARGED["reads"] = {"gravity": 1, "binding": 1, "charge": 1}  # every holder, the sign's among them


def real_rows(*rows: tuple[str, tuple[int, int], int, int | None]) -> list[Row]:
    """Rows of real lines as the loader reads them (loader.derived.Row), each (name, pair, lines, level weight): one part, no plane, sourced by the form where it is held at the write weight 1, acting on the pace, and every row reading every held row among them at the weight 1 (the tests' declaration)."""
    held = tuple((name, 1) for name, _pair, _lines, weight in rows if weight is not None)
    return [Row(n, p, k, 1, False, False, False, w, w and 1, 0, held) for n, p, k, w in rows]


def load_file(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    sys.modules[name] = module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def refused(match: str, call, *args, **keys):
    with pytest.raises(ValueError, match=match) as refusal:
        call(*args, **keys)
    return refusal.value


TOOLS = ("pixel_mode", "back_in_time", "run_inputs")  # the generator, the back-in-time gate, the runner
TOOL, BACK, RUN = (load_file(name, ROOT / "tools" / f"{name}.py") for name in TOOLS)
RECORD = load_file("look_record", ROOT / "tools" / "look" / "record.py")  # the look's reader


def universe_beside(tmp_path, drop=(), charged=False, **pairs):  # type: ignore[no-untyped-def]
    """The tests' universe copied beside a world as u.json (the families `drop` names left out, of every family's reads too, a family's pair replaced where `pairs` names it, the charged matter row, matter's pair as a plane, added where `charged`) with the engine's start file as e.json."""
    universe = json.loads(UNIVERSE.read_text(encoding="utf-8"))
    universe["families"] = [family for family in universe["families"] if family["name"] not in drop]
    universe["families"] += [json.loads(json.dumps(CHARGED))] if charged else []
    for family in universe["families"]:
        family["pair"] = pairs.get(family["name"], family["pair"])
        family["reads"] = {name: w for name, w in family["reads"].items() if name not in drop}
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    (tmp_path / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())


def chain_body_world(folder, tool, quanta=QUANTA, at=(), senses=(), taker=False, mode=True, chain=CHAIN):  # type: ignore[no-untyped-def]
    """A chain of `chain` Nodes (x open) with a body of matter declared with `quanta` on each Node of `at` (the chain's centre where empty; the last read by the detector `taker` where asked), a body rotating in the `senses` given of the charged family (matter's pair as a plane), laid by the generator: the bodies' Nodes with their counts and the mode file beside them; the detectors `left` and `right`, two Nodes each at the chain's two ends (never one Node), report the light's inflow there."""
    at = at or (chain // 2,)  # the chain's centre where no Node is named
    families = [CHARGED["name"] if i < len(senses) and senses[i] else "matter" for i in range(len(at))]
    universe_beside(folder, charged=CHARGED["name"] in families)
    nodes = [[dict(node=[x, 0, 0], count=quanta)] for x in at]
    measured = [dict(family=f, nodes=n) for f, n in zip(families, nodes, strict=True)]
    ends = [{"name": "left", "positions": [[0, 0, 0], [1, 0, 0]]}]
    ends += [{"name": "right", "positions": [[chain - 2, 0, 0], [chain - 1, 0, 0]]}]
    detectors = ends + ([{"name": "taker", "block": len(at) - 1}] if taker else [])
    world = dict(shape=[chain, 1, 1], detectors=detectors, measured=measured, ticks=400, face_depth=1)
    world.update(boundary=dict(x="open", y="periodic", z="periodic"), universe="u.json", engine="e.json")
    (path := folder / "chain.json").write_text(json.dumps(world), encoding="utf-8")
    if mode:
        tool.main(["--input", str(path), "--sense", *(str(sense) for sense in senses)])
    return path


SLIT = dict(shape=[24, 9, 1], boundary=dict(x="open", y="open", z="periodic"), face_depth=1, ticks=24)
SLIT.update(universe="u.json", engine="e.json", measured=[], detectors=[])
SLIT["faces"] = [{"axis": "x", "at": 12, "gaps": [{"y": [4, 4], "z": [0, 0]}]}]
PACKET = {"family": "charge", "along": "x", "wave": [1, 4], "amplitude": 1328}
PACKET.update(top={"x": [5, 5], "y": [0, 8], "z": [0, 0]}, edge={"x": 4, "y": 0, "z": 0})


def slit_world(folder: Path, tool, name: str = "slit", **changes: object) -> Path:  # type: ignore[no-untyped-def]
    universe_beside(folder)
    path = folder / f"{name}.json"
    path.write_text(json.dumps({**SLIT, "messages": [PACKET], **changes}), encoding="utf-8")
    tool.main(["--input", str(path)])
    return path
