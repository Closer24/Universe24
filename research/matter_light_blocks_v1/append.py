"""Append-only update of the published blocks: new entries are added, existing ones never change.

    python -m research.matter_light_blocks_v1.append PROPOSAL.json --check   # every step, nothing written
    python -m research.matter_light_blocks_v1.append PROPOSAL.json           # write files and the catalog

A proposal is ``{"entries": [...]}``. Each entry gives ``name``, ``group``, ``file`` (a source init file in the
official format, repository-relative), ``steps``, ``what``, ``limits``, ``status``, ``source``, ``origin``,
``added`` and optionally ``signature``, ``box_checks``, ``controls``, ``tags``, ``composable``, ``heavy``.
For every entry the tool:

1. refuses a published name, a repeated name, an unknown group, and an initial state identical to a published
   block (a repeated preparation is not republished);
2. writes the official init file compactly to ``blocks/<group>/<name>.json`` (never overwrites; reload-checked);
3. replays it with ``verify.replay`` (native Engine, exact inverse at every update) and requires
   ``verify.check`` to report no failure;
4. records ``file_sha256``, ``final_state_sha256`` and the measured click totals.

Only if every entry passes does it copy the files in and append the entries to ``catalog.json``: the existing
entries stay byte-identical (checked before writing). The 8301320 build tool ``build_from_library.py`` is not
used: the program's source library has changed since, so a rebuild would not reproduce the published entries.
Needs only ``universe24`` and the standard library.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import shutil
import sys
import tempfile

from universe24.experiments import from_dict

from . import verify as V

ROOT = V.HERE.parents[1]
SLUG = {"light": "light", "matter at rest": "matter_at_rest", "moving matter": "moving_matter",
        "atoms": "atoms", "spin": "spin", "charge": "charge", "clocks and gravity": "clocks_and_gravity",
        "interaction and detectors": "interaction_and_detectors", "media": "media",
        "seeds (big bang)": "seeds_big_bang"}
REQUIRED = ("name", "group", "file", "steps", "what", "limits", "status", "source", "origin", "added")
OPTIONAL = {"signature": {}, "box_checks": [], "controls": [], "tags": [], "composable": False, "heavy": False}


def compact(data: dict) -> str:
    """The published file layout: one key per line, one seed change per line."""
    head = [f' {json.dumps(k)}: {json.dumps(v, separators=(",", ":"))}' for k, v in data.items() if k != "seed_changes"]
    body = ",\n".join("  " + json.dumps(c, separators=(",", ":")) for c in data["seed_changes"])
    text = "{\n" + ",\n".join(head) + ',\n "seed_changes": [\n' + body + "\n ]\n}\n"
    if json.loads(text) != data:
        raise AssertionError("compact writer changed the data")
    return text


def _official(path: Path, steps: int):
    data = json.loads(path.read_text(encoding="utf-8"))
    exp = from_dict(data)
    if exp.steps != steps:
        raise ValueError(f"{path}: file horizon {exp.steps} differs from the declared steps {steps}")
    return {"side": exp.initial.cube.side, "coupling_signs": list(exp.engine.coupling.body_signs),
            "background": list(exp.initial.background), "steps": steps,
            "seed_changes": [{"position": list(a[:3]), "channel": a[3], "state": list(s)}
                             for a, s in sorted(exp.initial.cells.items())]}, exp


def prepare(proposal: dict, catalog: dict, stage: Path) -> list[dict]:
    """Build and check every new entry inside ``stage`` (a copy of the package layout); raise on any failure."""
    published = {e["name"] for e in catalog["entries"]}
    initial = {}
    for e in catalog["entries"]:
        exp = from_dict(json.loads((V.HERE / e["file"]).read_text(encoding="utf-8")))
        initial.setdefault((exp.engine.coupling.body_signs, V.state_hash(exp.initial)), e["name"])
    names = Counter(p["name"] for p in proposal["entries"])
    out = []
    for p in proposal["entries"]:
        missing = [k for k in REQUIRED if k not in p]
        if missing:
            raise ValueError(f"{p.get('name')}: missing {missing}")
        if p["name"] in published or names[p["name"]] > 1:
            raise ValueError(f"{p['name']}: name already published or repeated")
        if p["group"] not in SLUG:
            raise ValueError(f"{p['name']}: unknown group {p['group']}")
        data, exp = _official(ROOT / p["file"], p["steps"])
        same = initial.get((exp.engine.coupling.body_signs, V.state_hash(exp.initial)))
        if same:
            raise ValueError(f"{p['name']}: same complete initial state as the published block {same}")
        rel = Path("blocks") / SLUG[p["group"]] / f"{p['name']}.json"
        target = stage / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8") as handle:
            handle.write(compact(data))
        if from_dict(json.loads(target.read_text(encoding="utf-8"))).initial != exp.initial:
            raise AssertionError(f"{p['name']}: written file does not reproduce the preparation")
        entry = {"name": p["name"], "group": p["group"], "what": p["what"], "source": p["source"],
                 "origin": p["origin"], "status": p["status"], "signs": data["coupling_signs"],
                 "background": data["background"], "side": data["side"], "steps": p["steps"],
                 "cells": len(data["seed_changes"])}
        for key, default in OPTIONAL.items():
            entry[key] = p.get(key, default)
        entry.update({"limits": p["limits"], "file": rel.as_posix(), "file_sha256": V.file_sha256(target),
                      "library_verified": False, "added": p["added"]})
        saved = V.HERE
        try:
            V.HERE = stage
            measured = V.replay(entry)
        finally:
            V.HERE = saved
        entry["final_state_sha256"] = V.state_hash(measured["final"])
        entry["measured"] = {"first_return": measured["first_return"], "clicks_total": sum(measured["per_step"]),
                             "kinds_total": dict(sum(measured["kinds_per_step"], Counter()))}
        fails = V.check(entry, measured)
        if fails:
            raise ValueError(f"{p['name']}: {'; '.join(fails)}")
        out.append(entry)
    return out


def append(proposal_path: Path, check_only: bool = False) -> dict:
    text = V.CATALOG.read_text(encoding="utf-8")
    catalog = json.loads(text)
    if json.dumps(catalog, indent=1) + "\n" != text:
        raise ValueError("catalog.json does not round-trip; refusing to rewrite it")
    proposal = json.loads(Path(proposal_path).read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp)
        entries = prepare(proposal, catalog, stage)
        if not check_only:
            for e in entries:
                target = V.HERE / e["file"]
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("x", encoding="utf-8") as handle:
                    handle.write((stage / e["file"]).read_text(encoding="utf-8"))
            new = dict(catalog, entries=catalog["entries"] + entries)
            blob = json.dumps(new, indent=1) + "\n"
            if not blob.startswith(text[:text.index('"entries": [') + len('"entries": [')]):
                raise AssertionError("catalog header changed")
            if json.loads(blob)["entries"][:len(catalog["entries"])] != catalog["entries"]:
                raise AssertionError("an existing entry would change")
            V.CATALOG.write_text(blob, encoding="utf-8")
    return {"appended": [e["name"] for e in entries], "written": not check_only,
            "catalog_entries": len(catalog["entries"]) + (0 if check_only else len(entries))}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    paths = [a for a in argv if not a.startswith("--")]
    if len(paths) != 1:
        raise SystemExit(__doc__)
    print(json.dumps(append(Path(paths[0]), check_only="--check" in argv), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
