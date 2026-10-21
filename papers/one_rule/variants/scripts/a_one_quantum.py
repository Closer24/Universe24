"""A. One quantum at a time on the engine (README.md, section A): the shipped two slits' world with its packet
laid at one quantum, run under the click's read of the board, once at the shipped T (--shipped) and in an
ensemble of worlds (--ensemble N: the lay's amplitude moved by one unit, the source's column moved by one
Node) at a scratch universe whose T is the shipped T times 2^12, so that one quantum lays at the shipped
amplitude and the integer board carries the wave as the shipped run does; the wall's return credited by a
region at the source's receding face so that every exit of the record is a declared detector. The scaled
universe and the worlds are written under a scratch folder at run time (--scratch; the system's temporary
directory by default), nothing of it shipped. Every number printed is the engine's.

    PYTHONPATH=src python papers/one_rule/variants/scripts/a_one_quantum.py --shipped
    PYTHONPATH=src python papers/one_rule/variants/scripts/a_one_quantum.py --ensemble 40
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "src"))

from event_universe import digits, world_files  # noqa: E402
from event_universe.features.click import drawn_from  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.node_detector import node_detector_nodes  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402

OUT = HERE.parent / "out"
SHIPPED = ROOT / "examples" / "events" / "two_slits" / "two_slits.json"
LIGHT = ROOT / "examples" / "events" / "light.json"
INTERVALS = 130  # the shipped run's intervals, the window spanning the passage


def load_tool(name: str):  # type: ignore[no-untyped-def]
    """A tool of tools/ loaded by its path (the generator, tools/pixel_mode.py)."""
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


TOOL = load_tool("pixel_mode")


def universe_beside(scratch: Path, factor: int) -> str:
    """light.json with its quantum action times `factor`, written beside the scratch root at a repository
    path."""
    universe = json.loads(LIGHT.read_text(encoding="utf-8"))
    universe["integers"]["quantum_action"] *= factor
    target = scratch / "examples" / "events" / f"light_x{factor}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(universe, indent=1), encoding="utf-8")
    return f"examples/events/light_x{factor}.json"


def world_of(
    scratch: Path,
    name: str,
    amplitude: int,
    column: int,
    window: int,
    universe: str,
    return_region: bool,
) -> Path:
    """The shipped two slits' world with the packet's amplitude and column changed, the draw's window set,
    the universe named, and, with `return_region`, a region `return` two columns deep at the source's
    receding face (x = 0 and 1 over every row), backed by that face as the screen is backed by its own, so
    that the wall's return is credited there."""
    world = json.loads(SHIPPED.read_text(encoding="utf-8"))
    world.pop("engine", None)
    packet = world["packets"][0]
    packet["amplitude"] = amplitude
    packet["top"]["x"] = [column, column]
    world["draw"] = {"window": window}
    world["universe"] = universe
    if return_region:
        rows = range(world["shape"][1])
        world["node_detectors"].append(
            {"name": "return", "positions": [[x, y, 0] for x in (0, 1) for y in rows]}
        )
    folder = scratch / "examples" / "events" / "one_quantum"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{name}.json"
    path.write_text(json.dumps(world) + "\n", encoding="utf-8")
    return path


def laid_count(path: Path) -> int:
    """The generator's lay (tools/pixel_mode.py) and the mode file's count of the lay."""
    TOOL.main(["--input", str(path)])
    mode = json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))
    return int(mode["packets"][0]["count"])


def one_quantum_amplitude(scratch: Path, universe: str, window: int, column: int, back: bool) -> int:
    """The largest declared amplitude whose lay counts one quantum by the generator (the count rounds the
    share half up, so the count is 1 over a range of amplitudes; the lay at the shipped amplitude 1241
    counts 4197 at the shipped T)."""
    low, high = 1, 1241
    while high - low > 1:
        mid = (low + high) // 2
        count = laid_count(world_of(scratch, "probe", mid, column, window, universe, back))
        if count <= 1:
            low = mid
        else:
            high = mid
    return low


def run(path: Path, intervals: int) -> tuple[Lattice, list[dict]]:  # type: ignore[type-arg]
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_world(path), lines.append)
    for _ in range(intervals):
        board.step()
        if board.ended is not None:
            break
    return board, lines


def summary(board: Lattice, lines: list[dict], unit: int) -> dict:  # type: ignore[type-arg]
    """The run's numbers: the credit lines (the clicks), the regions' inflows from the click lines summed
    over the run in the record's own unit (a lattice reading beside the clicks), the books."""
    credits = [c for c in lines if c["event"] == "credit"]
    inflow: Counter[str] = Counter()
    for c in (line for line in lines if line["event"] == "click"):
        inflow[str(c["node_detector"])] += int(c["inflow"])
    keys = ("interval", "node_detector", "count", "left", "bias_bound", "window")
    return {
        "credits": [{k: c[k] for k in keys} for c in credits],
        "inflow_quanta": {name: value / unit for name, value in sorted(inflow.items())},
        "books": board.books(),
        "ended": board.ended,
        "interval": board.interval,
    }


def window_weights(lines: list[dict], names: list[str], close: int, window: int) -> list[int]:  # type: ignore[type-arg]
    """The regions' window inflows, the draw's weights (lists.region: each region's intake summed over the
    window and floored at 0, over G^2 once; the click lines carry the plain current per interval, equal to
    the booked one over G^2 where no tension stands), from the click lines of the window closing at `close`."""
    first = close - window + 1
    found = []
    for name in names:
        total = sum(
            int(line["inflow"])
            for line in lines
            if line["event"] == "click"
            and line["node_detector"] == name
            and first <= line["interval"] <= close
        )
        found.append(max(total, 0))
    return found


def read_again(board: Lattice, index: int, weights: list[int]) -> tuple[int, int, list[int]]:
    """The click's read of the board recomputed after the run at the regions' Nodes (digits.read_of, the
    engine's own function) and the first draw's pick on `weights` (features/click.drawn_from): the number's
    bit length, the residue modulo the weights' total, and the pick with the read's two moduli."""
    at = node_detector_nodes(board)
    number, moduli = digits.read_of(board, [(index, at)], "the regions, read again")
    pick, _left = drawn_from(number, weights, "read again", moduli)
    return number.bit_length(), number % sum(weights), [pick, *moduli]


def shipped_run(scratch: Path, window: int) -> dict:  # type: ignore[type-arg]
    """The one-quantum lay at the shipped T in the shipped geometry, no return region."""
    t0 = time.time()
    universe = "examples/events/light.json"
    amplitude = one_quantum_amplitude(scratch, universe, window, 10, False)
    path = world_of(scratch, "shipped_T_one_quantum", amplitude, 10, window, universe, False)
    count = laid_count(path)
    board, lines = run(path, INTERVALS)
    index = [f.name for f in board.families].index("charge")
    unit = board.credit.units[index]
    found = summary(board, lines, unit)
    found.update(amplitude=amplitude, laid=count, unit=unit, seconds=round(time.time() - t0, 1))
    return found


def ensemble_run(scratch: Path, window: int, size: int, factor: int) -> dict:  # type: ignore[type-arg]
    """The ensemble at the scaled universe with the return region: `size` worlds, the amplitude stepped
    down by one unit every three worlds over the columns 10, 9 and 11."""
    universe = universe_beside(scratch, factor)
    a1 = one_quantum_amplitude(scratch, universe, window, 10, True)
    print(json.dumps({"one_quantum_amplitude_at_scaled_T": a1, "factor": factor}))
    columns = (10, 9, 11)
    variants = [(a1 - k // len(columns), columns[k % len(columns)]) for k in range(size)]
    runs = []
    for k, (amplitude, column) in enumerate(variants):
        t0 = time.time()
        path = world_of(scratch, f"ensemble_{k}", amplitude, column, window, universe, True)
        count = laid_count(path)
        try:
            board, lines = run(path, INTERVALS)
        except (ValueError, RuntimeError) as refusal:
            runs.append({"k": k, "amplitude": amplitude, "column": column, "refused": str(refusal)})
            print(json.dumps(runs[-1]))
            continue
        index = [f.name for f in board.families].index("charge")
        unit = board.credit.units[index]
        found = summary(board, lines, unit)
        credits = found["credits"]
        names = [d.name for d in board.node_detectors if d.declared]
        close = credits[0]["interval"] if credits else board.interval
        weights = window_weights(lines, names, close, window)
        again: object = None
        if credits and sum(weights) > 0:
            try:
                again = read_again(board, index, weights)
            except (ValueError, RuntimeError) as refusal:
                again = str(refusal)
        found.update(
            k=k,
            amplitude=amplitude,
            column=column,
            laid=count,
            unit=unit,
            regions=names,
            weights=weights,
            read_again=again,
            seconds=round(time.time() - t0, 1),
        )
        runs.append(found)
        total = max(sum(weights), 1)
        print(
            json.dumps(
                {
                    "k": k,
                    "amplitude": amplitude,
                    "column": column,
                    "laid": count,
                    "credits": [(c["interval"], c["node_detector"]) for c in credits],
                    "left": [c["left"] for c in credits],
                    "shares": [round(w / total, 4) for w in weights],
                    "read_again": again,
                    "seconds": found["seconds"],
                },
                default=str,
            )
        )
    realised = Counter(c["node_detector"] for r in runs for c in r.get("credits", []))
    print(json.dumps({"realised": dict(realised), "runs": len(runs)}))
    return {"factor": factor, "one_quantum_amplitude": a1, "ensemble": runs}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--scratch",
        type=Path,
        default=Path(tempfile.gettempdir()) / "two_slits_variants",
        help="the scratch root for the scaled universe and the worlds (nothing of it is shipped)",
    )
    parser.add_argument("--shipped", action="store_true", help="the one-quantum lay at the shipped T")
    parser.add_argument("--ensemble", type=int, default=0, help="the ensemble's size at the scaled T")
    parser.add_argument("--factor", type=int, default=4096, help="T's factor for the scaled universe")
    parser.add_argument("--window", type=int, default=INTERVALS, help="the draw's window")
    args = parser.parse_args(argv)
    scratch: Path = args.scratch
    (scratch / "examples" / "events").mkdir(parents=True, exist_ok=True)
    shutil.copy(LIGHT, scratch / "examples" / "events" / "light.json")
    world_files.REPOSITORY_ROOT = scratch
    OUT.mkdir(parents=True, exist_ok=True)
    if args.shipped:
        found = shipped_run(scratch, args.window)
        (OUT / "a_shipped_T.json").write_text(json.dumps(found, indent=1, default=str), encoding="utf-8")
        print(json.dumps({"shipped_T": found}, indent=1, default=str))
    if args.ensemble:
        found = ensemble_run(scratch, args.window, args.ensemble, args.factor)
        (OUT / "a_ensemble.json").write_text(json.dumps(found, indent=1, default=str), encoding="utf-8")


if __name__ == "__main__":
    main()
