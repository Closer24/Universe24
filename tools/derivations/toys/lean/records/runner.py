"""The toy's compact record for a derivation (the Stern-Gerlach records beside this file): the world and the universe, the counts, the log, the census, the transient, the seconds and the run back, no Node lines. Usage, from the repository's root: `python tools/derivations/toys/lean/records/runner.py <world.json> <out.json> [back N]`."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import time
from pathlib import Path


def main(argv: list[str]) -> None:
    sys.set_int_max_str_digits(0)
    root = Path(__file__).resolve().parents[5]
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location(
        "lean_toy", root / "tools" / "derivations" / "toys" / "lean" / "toy.py"
    )
    assert spec is not None and spec.loader is not None
    toy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(toy)
    from tests.laws import run_back_exact

    universe, world = toy.load_toy_world(argv[1])
    node = toy.Toy(universe, world)
    kept = copy.deepcopy(node)
    started = time.time()
    for _ in range(int(world["intervals"])):
        node.step()
    seconds = round(time.time() - started, 1)
    back = int(argv[3]) if len(argv) > 3 else 0
    exact = run_back_exact(kept, back) if back else None
    out = {
        "world": world,
        "universe": universe,
        "counts": node.counts,
        "log": node.log,
        "census": node.census(),
        "transient": node.max_transient,
        "seconds": seconds,
        "run_back": [exact, back],
    }
    Path(argv[2]).write_text(json.dumps(out), encoding="utf-8")
    print(argv[1], node.counts, node.census(), node.max_transient, seconds, "s", "run back", exact, back)


if __name__ == "__main__":
    main(sys.argv)
