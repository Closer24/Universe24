"""The rename probe of the genericity audit (the architecture cleanup plan,
section 8): every family, detector and column of a world renamed to a
keyword-like token, both worlds run through the runner, and the records
(`events.jsonl`, `state.json`, `run.json`) compared with the names mapped
back. A read-only probe of the engine; it owns no rule.

    python rename_probe.py CHECKOUT OUT PYTHON WORLD[:TICKS] ...

`CHECKOUT` is the repository root (its `src` is the package run), `OUT` a
scratch directory, `PYTHON` the interpreter of the runs, and each `WORLD`
a path under `examples/events` with an optional tick count.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

TOKENS = [
    "measure",
    "__proto__",
    "rule",
    "wave",
    "sum",
    "0",
    "face:+x ",
    "read",
    "constructor",
    "pass",
    "rerelease",
    "beam",
    "K",
    "N",
    "lamp",
    "gate",
    "record",
    "amount",
    "phase",
    "true",
    "null",
    "x",
    "yy",
    "zz1",
    "the light",
    "mass",
    "gravity",
]
VOLATILE = ("elapsed_seconds", "initialization_sha256", "source_sha256")


def rename_world(document: dict) -> tuple[dict, dict, dict, dict]:
    """The world with every family, detector and column name replaced by a
    token; the three maps from the old names to the new."""
    names = [family["name"] for family in document["families"]]
    families = {name: f"{TOKENS[i % len(TOKENS)]}~{i}" for i, name in enumerate(names)}
    detectors = {
        detector["name"]: f"{TOKENS[(i + 7) % len(TOKENS)]}#{i}"
        for i, detector in enumerate(document.get("detectors", []))
    }
    columns: dict[str, str] = {}
    for family in document["families"]:
        for column in family.get("columns", {}):
            columns.setdefault(column, f"col{len(columns)}~{TOKENS[len(columns) % len(TOKENS)]}")
    renamed = json.loads(json.dumps(document))
    for family in renamed["families"]:
        family["name"] = families[family["name"]]
        if "columns" in family:
            family["columns"] = {columns[k]: v for k, v in family["columns"].items()}
    for entry in renamed.get("measured", []):
        entry["family"] = families[entry["family"]]
        if "held" in entry:
            entry["held"] = {families[k]: v for k, v in entry["held"].items()}
        if "table" in entry:
            table = {}
            for key, value in entry["table"].items():
                if isinstance(value, dict):
                    value = dict(value)
                    window = value.get("phase_window")
                    if isinstance(window, dict):
                        value["phase_window"] = {**window, "reads": families[window["reads"]]}
                    if "into" in value:
                        value["into"] = families[value["into"]]
                    if "products" in value:
                        value["products"] = [[families[p[0]], p[1], p[2]] for p in value["products"]]
                table[families[key]] = value
            entry["table"] = table
        if "become" in entry:
            become = dict(entry["become"])
            become["into"] = families[become["into"]]
            become["products"] = [[families[p[0]], p[1], p[2]] for p in become["products"]]
            entry["become"] = become
    for ray in renamed.get("in_transit", []):
        ray["family"] = families[ray["family"]]
    for detector in renamed.get("detectors", []):
        detector["name"] = detectors[detector["name"]]
    return renamed, families, detectors, columns


def run(root: Path, python: str, world: Path, target: Path, ticks: int | None) -> Path:
    """One headless run of the world into `target/run`; its directory."""
    if target.exists():
        shutil.rmtree(target)
    command = [python, "-m", "event_universe", "--init", str(world), "--output", str(target / "run")]
    if ticks:
        command += ["--ticks", str(ticks)]
    environment = {"PYTHONPATH": str(root / "src"), "PATH": "/usr/bin:/bin"}
    subprocess.run(command, check=True, capture_output=True, env=environment)
    return target / "run"


def unmap(text: str, back: dict[str, str]) -> str:
    """The renamed tokens mapped back by their exact JSON string value."""
    for new, old in sorted(back.items(), key=lambda item: -len(item[0])):
        text = text.replace(json.dumps(new), json.dumps(old))
    return text


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def main() -> None:
    root, out, python = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    out.mkdir(parents=True, exist_ok=True)
    for spec in sys.argv[4:]:
        relative, _, tick_text = spec.partition(":")
        ticks = int(tick_text) if tick_text else None
        source = root / "examples/events" / relative
        document = json.load(open(source))
        if "entity_definitions" in document:
            print("skip (entities)", relative)
            continue
        renamed, families, detectors, columns = rename_world(document)
        stem = source.stem
        renamed_path = out / f"{stem}_renamed.json"
        renamed_path.write_text(json.dumps(renamed))
        before = run(root, python, source, out / f"{stem}_a", ticks)
        after = run(root, python, renamed_path, out / f"{stem}_b", ticks)
        back = {new: old for mapping in (families, detectors, columns) for old, new in mapping.items()}
        events_a = (before / "events.jsonl").read_text()
        events_b = unmap((after / "events.jsonl").read_text(), back)
        state_a = json.loads((before / "state.json").read_text())
        state_b = json.loads(unmap((after / "state.json").read_text(), back))
        run_a = json.loads((before / "run.json").read_text())
        run_b = json.loads(unmap((after / "run.json").read_text(), back))
        for key in VOLATILE:
            run_a.pop(key, None)
            run_b.pop(key, None)
        verdict = (
            "events " + ("identical" if events_a == events_b else "DIFFER"),
            "state " + ("identical" if state_a == state_b else "DIFFER"),
            "run.json " + ("identical" if run_a == run_b else "DIFFER"),
            f"{len(events_a.splitlines())} lines, {run_a['completed_ticks']} ticks, "
            f"families {len(families)}, detectors {len(detectors)}",
        )
        print(relative, *verdict)


if __name__ == "__main__":
    main()
