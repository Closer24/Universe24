"""Provenance tool: materialise the program's blocks as data-only init files.

This is how ``blocks/`` and ``catalog.json`` were produced. It reads the source
library ``research.matter_light_v1.blocks`` (the researchers' constructors and
init files) plus a few newer modules (listed in ``EXTRAS``) and, for every block:

* writes the complete initial state, background, sign triple and horizon in the
  official init format (one seed change per line; reload-checked; never overwrites);
* runs the native Engine for the declared horizon with the exact inverse checked
  at every update, and records the final full-state SHA-256, the first exact
  return and the native click counts;
* re-checks the generic signature fields and the local box checks; a block that
  fails is not published.

It needs the source research folder ``research/matter_light_v1``; ``verify.py``
does not.

    python -m research.matter_light_blocks_v1.build_from_library OUT_DIR [--max-cells N] [NAME ...]
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys
import time

from research.matter_light_v1 import harness as H
from research.matter_light_blocks_v1 import verify as V

SLUG = {"light": "light", "matter at rest": "matter_at_rest", "moving matter": "moving_matter",
        "atoms": "atoms", "spin": "spin", "charge": "charge", "clocks and gravity": "clocks_and_gravity",
        "interaction and detectors": "interaction_and_detectors", "media": "media",
        "seeds (big bang)": "seeds_big_bang"}

PENDING = "SIMULATION (native Engine, exact inverse every update; manager re-check); referee pending"


def _box(xs, y, zs=(3, 4, 5)):
    return [[x, y, z] for x in xs for z in zs]


_RING_D1 = [[14, 140, 3], [14, 140, 4], [14, 140, 5], [14, 140, 6], [14, 140, 7], [15, 140, 3], [15, 140, 7],
            [16, 140, 3], [16, 140, 7], [17, 140, 3], [17, 140, 4], [17, 140, 5], [17, 140, 6], [17, 140, 7]]
_EIN_X = [237, 238, 239, 0, 1, 2, 3, 4, 5]
P = "research/matter_light_v1"

EXTRAS = [
    dict(name="d1_local_atom_L100", group="atoms", source="r11", origin=f"{P}/r11/preparations/d1_main_L100.json",
         steps=140,
         what=("locally created atom candidate (module D1, mixed-class junctions): the seed glider passes a class-2 "
               "junction and emits light; the light crosses a class-0 junction and creates a glider pair (t=29); the "
               "created glider passes a trapped class-2 junction and a packet stays bound between two silent cores "
               "with period 20 = 2d+4 from t_c = 80 while one packet leaves (radiative recombination)"),
         limits=("prepared sparse network and cores; immobile; lifetime set by the board (about L-39); identical "
                 "to the 2L board until the seed's own light wraps (see d1_local_atom_L200)"),
         box_checks=[{"label": "atom", "type": "periodic", "sites": _box(range(10, 19), 12), "period": 20,
                      "from": 80, "to": 140}]),
    dict(name="d1_local_atom_L200", group="atoms", source="r11", origin=f"{P}/r11/preparations/d1_main_L200.json",
         steps=220,
         what="the same module D1 on the periodic 2L extension (every line and both cores tiled, one seed): same birth",
         limits="board-independence companion of d1_local_atom_L100: the trap box is identical at every t <= 140",
         box_checks=[{"label": "atom", "type": "periodic", "sites": _box(range(10, 19), 12), "period": 20,
                      "from": 80, "to": 220}]),
    dict(name="d1_control_no_seed_L100", group="atoms", source="r11",
         origin=f"{P}/r11/preparations/d1_control_no_seed_L100.json", steps=140,
         what="control: module D1 without the seed glider: no click at all; the silent cores tick as dark period-4 clocks",
         limits="control", signature={"silent": True, "period": 4}),
    dict(name="d1_skeleton_atom_spin_clocks_L160", group="seeds (big bang)", source="r11",
         origin=f"{P}/r11/preparations/d1_v3_skeleton_L160.json", steps=225,
         what=("one seed in a sparse prepared network creates light, a glider pair, an atom candidate (period 20) and a "
               "spinor-class light ring (r04's module on the created pair's -y member: the ring equals its 360-degree "
               "image after each 18-update lap, 7 laps checked), while 4 dark clocks on the atom's light line record the "
               "emitted packet without disturbing it"),
         limits="prepared network, cores, ring and clocks; local until the seed's own light wraps (identical on L=320)",
         box_checks=[{"label": "atom", "type": "periodic", "sites": _box(range(10, 19), 12), "period": 20,
                      "from": 80, "to": 200},
                     {"label": "spin ring", "type": "c_image", "sites": _RING_D1, "t0": 97, "lap": 18, "laps": 7}]),
    dict(name="spin_module_pure4pairs_L80", group="spin", source="r04",
         origin=f"{P}/r04/preparations/wave6_pure4pairs_spin_module.json", steps=90,
         what=("created spin: a 14-site light ring with channel holonomy z joined to a matter line by one partner "
               "junction, fed by the first glider that r06's pure4pairs cascade creates; the ring equals its 360-degree "
               "image after 18 updates and returns after 36 (720 degrees); the junction emits a glider pair every 720 "
               "degrees"),
         limits="one clean double lap here (later cascade traffic reaches the junction); the ring is prepared hardware",
         box_checks=None),
    dict(name="einstein_created_instruments_L240", group="clocks and gravity", source="r08",
         origin=f"{P}/r08/preparations/w8_einstein_module_d20_xm32_L240.json", steps=230,
         what=("two atom clocks created after t=0 (A at t=62, B at t=122; prepared traps holding packets the seed "
               "emitted) joined by a light link: A's formation packet passes A's station at t1=66, is reflected at B "
               "at t_B=145 and is back at t2=224, so t_B = (t1+t2)/2 exactly (Einstein synchronisation with created "
               "instruments; station passages are read by r08's script)"),
         limits=("prepared lines, cores and link; one clean round trip; the declared boxes are the trap segments "
                 "(r08's own detector uses a larger signature, hence its longer life windows)"),
         box_checks=[{"label": "atom A", "type": "periodic", "sites": _box(_EIN_X, 0), "period": 20,
                      "from": 63, "to": 203},
                     {"label": "atom B", "type": "periodic", "sites": _box(_EIN_X, 220), "period": 20,
                      "from": 149, "to": 230}]),
]


def write_compact(path: Path, engine, initial, steps: int) -> Path:
    """Official init format, one seed change per line (smaller than indent=1), reload-checked."""
    from universe24.experiments import from_dict
    data = H.config_dict(engine, initial, steps)
    head = [f' {json.dumps(k)}: {json.dumps(v, separators=(",", ":"))}' for k, v in data.items() if k != "seed_changes"]
    body = ",\n".join("  " + json.dumps(c, separators=(",", ":")) for c in data["seed_changes"])
    text = "{\n" + ",\n".join(head) + ',\n "seed_changes": [\n' + body + "\n ]\n}\n"
    if json.loads(text) != json.loads(json.dumps(data)):
        raise AssertionError("compact writer changed the data")
    reloaded = from_dict(json.loads(text))
    if reloaded.initial != initial or reloaded.engine.coupling.fingerprint != engine.coupling.fingerprint:
        raise AssertionError("init file does not reproduce the preparation")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(text)
    return path


def _replay(out: Path, entry: dict) -> dict:
    saved = V.HERE
    try:
        V.HERE = out
        return V.replay(entry)
    finally:
        V.HERE = saved


def _finish(out: Path, entry: dict):
    measured = _replay(out, entry)
    entry["final_state_sha256"] = V.state_hash(measured["final"])
    entry["measured"] = {"first_return": measured["first_return"],
                         "clicks_total": sum(measured["per_step"]),
                         "kinds_total": dict(sum(measured["kinds_per_step"], Counter()))}
    return entry, V.check(entry, measured)


def build_library(out: Path, max_cells: int, only):
    from research.matter_light_v1.blocks import library as LIB
    source = json.loads(Path(f"{P}/blocks/catalog.json").read_text(encoding="utf-8"))
    chosen = [e for e in source["entries"] if e["cells"] <= max_cells and e.get("verified")
              and (not only or e["name"] in only)]
    results = []
    for e in chosen:
        blk = LIB.get(e["name"])
        engine, initial = blk.prepare()
        rel = Path("blocks") / SLUG[e["group"]] / f"{e['name']}.json"
        write_compact(out / rel, engine, initial, blk.steps)
        entry = {
            "name": e["name"], "group": e["group"], "what": e["what"], "source": e["source"],
            "origin": e["source_file"], "status": e["status"], "signs": e["signs"],
            "background": e["background"], "side": e["side"], "steps": blk.steps, "cells": e["cells"],
            "signature": e["signature"], "controls": e.get("controls", []), "limits": e.get("limits", ""),
            "composable": e.get("composable", True), "heavy": e.get("heavy", False), "tags": e.get("tags", []),
            "file": rel.as_posix(), "file_sha256": V.file_sha256(out / rel), "library_verified": True,
        }
        results.append(_finish(out, entry))
    return source["format"], results


def build_extras(out: Path, only):
    results = []
    for spec in EXTRAS:
        if only and spec["name"] not in only:
            continue
        engine, initial, _ = H.load_config(spec["origin"])
        rel = Path("blocks") / SLUG[spec["group"]] / f"{spec['name']}.json"
        write_compact(out / rel, engine, initial, spec["steps"])
        box_checks = spec.get("box_checks")
        if box_checks is None and spec["name"] == "spin_module_pure4pairs_L80":
            frag = json.loads(Path(f"{P}/r04/preparations/wave6_spin_module_fragment.json").read_text())
            sites = sorted({tuple(c["position"]) for c in frag["seed_changes_recommended_at_pure4pairs_J_20_3_3"]})
            box_checks = [{"label": "spin ring", "type": "c_image", "sites": [list(p) for p in sites],
                           "t0": 51, "lap": 18, "laps": 2}]
        entry = {
            "name": spec["name"], "group": spec["group"], "what": spec["what"], "source": spec["source"],
            "origin": spec["origin"], "status": PENDING, "signs": list(engine.coupling.signs)
            if hasattr(engine.coupling, "signs") else json.loads(Path(spec["origin"]).read_text())["coupling_signs"],
            "background": list(initial.background), "side": initial.cube.side, "steps": spec["steps"],
            "cells": len(initial.cells), "signature": spec.get("signature", {}), "box_checks": box_checks or [],
            "controls": [], "limits": spec["limits"], "composable": False, "heavy": False, "tags": ["new"],
            "file": rel.as_posix(), "file_sha256": V.file_sha256(out / rel), "library_verified": False,
        }
        results.append(_finish(out, entry))
    return results


def build(out: Path, max_cells: int = 50_000, only=None):
    fmt, lib = build_library(out, max_cells, only)
    extra = build_extras(out, only)
    published = [e for e, f in lib + extra if not f]
    rejected = [{"name": e["name"], "fails": f} for e, f in lib + extra if f]
    catalog = {"format": "matter_light_blocks_v1-catalog-1",
               "built": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "source_library_format": fmt,
               "entries": published, "rejected": rejected}
    with (out / "catalog.json").open("x", encoding="utf-8") as handle:
        json.dump(catalog, handle, indent=1)
        handle.write("\n")
    return catalog


if __name__ == "__main__":
    args = sys.argv[1:]
    out = Path(args[0])
    mc = int(args[args.index("--max-cells") + 1]) if "--max-cells" in args else 50_000
    names = [a for i, a in enumerate(args[1:], 1) if not a.startswith("--") and args[i - 1] != "--max-cells"]
    cat = build(out, mc, names or None)
    print(len(cat["entries"]), "published;", len(cat["rejected"]), "rejected:", cat["rejected"][:5])
