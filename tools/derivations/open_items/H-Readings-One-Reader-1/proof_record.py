"""The record module's proof: the hole 60 with back 20 run through record_module.record (its own writer, census and hashes) with close.refused, close.children and bodies.credit rebound to the module's spellings through `entry`; every key compared with the committed record (the rows without milliseconds). Usage: proof_record.py <world.json> <committed.json> <out.json>."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import record_module as rm  # noqa: E402
from event_universe import bodies, close, run  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402

sys.set_int_max_str_digits(0)


def rebind(mod, fname, mine):
    orig = getattr(mod, fname)
    for name, m in list(sys.modules.items()):
        if name.startswith("event_universe"):
            for attr, val in list(vars(m).items()):
                if val is orig:
                    setattr(m, attr, mine)


def main(world_path, committed_path, out_path):
    rebind(close, "refused", rm.refused)
    rebind(close, "children", rm.children)
    rebind(bodies, "credit", rm.credit)
    universe, world = load_world(world_path)
    found = rm.record(run.Node, universe, world, 20, lambda s: None)
    committed = json.loads(Path(committed_path).read_text())
    verdict = {}
    for key in committed:
        a, b = committed[key], found.get(key)
        if key == "rows":
            a = [{k: v for k, v in r.items() if k != "milliseconds"} for r in a]
            b = [{k: v for k, v in r.items() if k != "milliseconds"} for r in b]
        if key == "turns":
            b = [list(t) for t in b]
        if key == "gapped":
            b = [list(t) for t in b]
        if key == "log":
            apart = sum(1 for x, y in zip(a, b, strict=False) if x != y) + abs(len(a) - len(b))
            verdict[key] = {"committed": len(a), "module": len(b), "apart": apart}
            continue
        verdict[key] = "EQUAL" if json.loads(json.dumps(a)) == json.loads(json.dumps(b)) else "APART"
    Path(out_path).write_text(json.dumps(verdict, indent=1))
    print(json.dumps(verdict))


if __name__ == "__main__":
    main(*sys.argv[1:4])
