"""Record, index and display clock-selection research without controlling evolution.

The study producer and independent verifier have separate explicit commands.
This driver never chooses a winner, injects a signal, or changes a recording.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

from research.experiments.run import write_json

ROOT = Path(__file__).resolve().parents[2]
FORMAT = "universe24-clock-selection-evidence-index-v1"


def file_identity(path, parent):
    path = Path(path).resolve()
    return {"path": os.path.relpath(path, parent),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def index_studies(studies, output):
    """Pin every submitted record, including failed outcomes, without relabeling it."""
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError("Refusing to overwrite " + str(output))
    if not studies:
        raise ValueError("At least one study is required")
    entries = []
    for identifier, directory in studies.items():
        if not isinstance(identifier, str) or not identifier:
            raise ValueError("A study requires a nonempty identifier")
        directory = Path(directory).resolve()
        paths = [directory / name for name in ("protocol.json", "result.json")]
        if not all(path.is_file() for path in paths):
            raise ValueError("Each study requires its saved protocol and result")
        records = sorted((directory / "records").glob("*.json"))
        records += sorted((directory / "records").glob("*.json.gz"))
        entries.append({"id": identifier,
                        "protocol": file_identity(paths[0], output),
                        "result": file_identity(paths[1], output),
                        "records": [file_identity(path, output) for path in records]})
    result = {"format": FORMAT,
              "base_commit": subprocess.check_output(
                  ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "studies": entries,
              "records": sum(len(entry["records"]) for entry in entries),
              "scientific_acceptance": "Unchanged; see each frozen protocol and result",
              "audit_status": "Not performed by indexing"}
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "index.json", result)
    return result


def verify_index(path):
    """Verify file identity only, independently of a study's behavior claims."""
    path = Path(path).resolve()
    index = json.loads(path.read_text())
    if index.get("format") != FORMAT:
        raise ValueError("Unsupported evidence index")
    checked = 0
    identifiers = set()
    for entry in index["studies"]:
        if entry["id"] in identifiers:
            raise ValueError("Duplicate study identifier")
        identifiers.add(entry["id"])
        for item in (entry["protocol"], entry["result"], *entry["records"]):
            target = (path.parent / item["path"]).resolve()
            if hashlib.sha256(target.read_bytes()).hexdigest() != item["sha256"]:
                raise ValueError("Evidence identity mismatch: " + str(target))
            checked += 1
    if index["records"] != sum(len(e["records"]) for e in index["studies"]):
        raise ValueError("Record count mismatch")
    return {"files_verified": checked, "scientific_acceptance": "Not evaluated"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    record = commands.add_parser("record", help="Run an ordinary frozen native experiment spec")
    record.add_argument("--spec", type=Path, required=True)
    record.add_argument("--output", type=Path, required=True)
    present = commands.add_parser("present", help="Package complete saved states in the unchanged Presenter")
    present.add_argument("--input", type=Path, action="append", required=True)
    present.add_argument("--output", type=Path, required=True)
    collector = commands.add_parser("index", help="Hash-pin all complete submitted records")
    collector.add_argument("--study", action="append", required=True, metavar="ID=DIRECTORY")
    collector.add_argument("--output", type=Path, required=True)
    verify = commands.add_parser("verify-index", help="Check indexed bytes, not scientific claims")
    verify.add_argument("--index", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.command == "record":
        from research.experiments.run import main as record_main
        return record_main(["--spec", str(args.spec), "--output", str(args.output)])
    if args.command == "present":
        from research.staged_blocks.export import export_pages
        result = export_pages(args.input, args.output,
                              title="Clock-mediated response — complete recorded states")
    elif args.command == "verify-index":
        result = verify_index(args.index)
    else:
        studies = {}
        for value in args.study:
            identifier, separator, directory = value.partition("=")
            if not separator or not identifier or not directory or identifier in studies:
                parser.error("--study requires a distinct ID=DIRECTORY")
            studies[identifier] = directory
        result = index_studies(studies, args.output)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
