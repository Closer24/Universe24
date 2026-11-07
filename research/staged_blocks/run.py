"""Run gradual research stages without changing the reference engine.

Examples:
  python -m research.staged_blocks.run list
  python -m research.staged_blocks.run demo --output runs/staged-demo
  python -m research.staged_blocks.run study orbit --output runs/staged-orbit
  python -m research.staged_blocks.run collect --study orbit=runs/staged-orbit --output runs/staged-report
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess

from research.experiments.run import write_json

ROOT = Path(__file__).resolve().parents[2]
MODULES = {"orbit": "orbit", "composition": "composition",
           "interaction": "interactions", "synthesis": "synthesis",
           "synthesis-even": "synthesis_even", "phase": "interactions_phase",
           "signed": "interactions_signed", "transmission": "transmission",
           "bridge": "pause_bridge", "recipes": "recipes", "motion": "motion"}
AUDIT_KINDS = frozenset({"orbit", "composition", "interaction", "synthesis", "motion"})


def _file(path, relative_to):
    return {"path": os.path.relpath(path, relative_to),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def collect(studies, output, *, presenter=True):
    """Index complete existing studies for independent audit and generic replay.

    This operation does not run dynamics or convert any study's outcome into a
    success. An empty records directory is valid for a bounded solver exclusion
    or resource outcome, and must be interpreted using its saved result.
    """
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError("Refusing to overwrite " + str(output))
    entries, bundles = [], []
    for label, location in studies.items():
        identifier, separator, kind = label.partition(":")
        if not separator:
            kind = identifier
        if not identifier or not kind:
            raise ValueError("Study labels require ID:KIND or KIND")
        if kind not in AUDIT_KINDS:
            raise ValueError("Unknown study kind: " + kind)
        directory = Path(location).resolve()
        for name in ("protocol.json", "result.json"):
            if not (directory / name).is_file():
                raise ValueError("Missing complete study artifact: " + str(directory / name))
        records = sorted((directory / "records").glob("*.json.gz"))
        records += sorted((directory / "records").glob("*.json"))
        if any(entry["id"] == identifier for entry in entries):
            raise ValueError("Study IDs must be distinct: " + identifier)
        entries.append({"id": identifier, "kind": kind,
                        "protocol": _file(directory / "protocol.json", output),
                        "result": _file(directory / "result.json", output),
                        "records": [_file(path, output) for path in records]})
        if (directory / "experiments.json").is_file():
            bundles.append(directory / "experiments.json")
    if not entries:
        raise ValueError("At least one complete study is required")
    output.mkdir(parents=True, exist_ok=False)
    base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    manifest = {"format": "universe24-staged-independent-audit-manifest-v1",
                "base_commit": base, "studies": entries}
    write_json(output / "audit_manifest.json", manifest)
    result = {"format": "universe24-staged-collection-v1", "base_commit": base,
              "studies": [entry["id"] for entry in entries],
              "complete_records": sum(len(entry["records"]) for entry in entries),
              "audit_manifest": "audit_manifest.json", "audit_status": "not_run",
              "behavioral_acceptance": "See each frozen study result and independent audit"}
    if presenter and bundles:
        from .export import export_pages
        replay = export_pages(bundles, output / "presenter")
        result["presenter"] = "presenter/" + replay["html"]
        result["presenter_index"] = "presenter/" + replay["index"]
        result["presenter_pages"] = replay["pages"]
        result["displayed_experiments"] = replay["experiments"]
    write_json(output / "result.json", result)
    return result


def run_stage(kind, output):
    """Explicitly execute one owner's bounded study; imports do no work."""
    module = importlib.import_module("research.staged_blocks." + MODULES[kind])
    if kind == "composition":
        return module.run(output)
    return module.main(["--output", str(output)])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="Show the stage catalog and evidence gates")
    demo = commands.add_parser("demo", help="Record the four-component assembly and controls")
    demo.add_argument("--output", type=Path, required=True)
    study = commands.add_parser("study", help="Run one explicitly selected bounded study")
    study.add_argument("kind", choices=tuple(MODULES))
    study.add_argument("--output", type=Path, required=True)
    collector = commands.add_parser("collect", help="Index existing evidence and package its native recordings")
    collector.add_argument("--study", action="append", required=True, metavar="[ID:]KIND=DIRECTORY")
    collector.add_argument("--output", type=Path, required=True)
    collector.add_argument("--no-presenter", action="store_true")
    audit = commands.add_parser("audit", help="Independently audit a saved evidence manifest")
    audit.add_argument("--manifest", type=Path, required=True)
    audit.add_argument("--output", type=Path, required=True)
    audit.add_argument("--max-cpu-seconds", type=float, default=600)
    args = parser.parse_args(argv)
    if args.command == "list":
        from .contracts import load_catalog
        print(json.dumps(load_catalog(), indent=2))
    elif args.command == "demo":
        run_stage("composition", args.output)
    elif args.command == "study":
        run_stage(args.kind, args.output)
    elif args.command == "audit":
        from .audit import main as audit_main
        audit_main(["--manifest", str(args.manifest), "--output", str(args.output),
                    "--max-cpu-seconds", str(args.max_cpu_seconds)])
    else:
        studies = {}
        for value in args.study:
            kind, separator, directory = value.partition("=")
            if not separator or not directory or kind in studies:
                parser.error("--study requires a distinct KIND=DIRECTORY")
            studies[kind] = directory
        print(json.dumps(collect(studies, args.output, presenter=not args.no_presenter), indent=2))


if __name__ == "__main__":
    main()
