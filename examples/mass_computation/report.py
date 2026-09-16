"""Package saved acceptance evidence without running or changing a simulation."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import shutil
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def write_report(run_root: Path, output: Path, source_commit: str | None = None) -> Path:
    if output.exists() and any(output.iterdir()):
        raise ValueError("use a new or empty report directory")
    output.mkdir(parents=True, exist_ok=True)
    summary = json.loads((run_root / "summary.json").read_text(encoding="utf-8"))
    expected = json.loads((HERE / "expectations.json").read_text(encoding="utf-8"))
    runs = {item["name"]: item for item in summary["runs"]}
    rows = []
    provenance = {
        "candidate": expected["model_id"],
        "frozen_design_commit": expected["design_commit"],
        "tested_source_commit": source_commit,
        "evidence_kind": expected["evidence_kind"],
        "sources": sorted({item["source_sha256"] for item in summary["runs"]}),
        "renderers": sorted({item["renderer_sha256"] for item in summary["runs"]}),
        "python_versions": sorted({item["python_version"] for item in summary["runs"]}),
        "physical_gravity_calibration": "not established",
        "files": {},
    }
    for audit in summary["acceptance"]:
        name = audit["name"]
        filename = f"universe24-mass-clock-{name}.html"
        shutil.copyfile(run_root / name / "run.html", output / filename)
        target = output / "cases" / name
        target.mkdir(parents=True)
        for artifact in ("initialization.json", "events.jsonl", "state.json", "run.json"):
            shutil.copyfile(run_root / name / artifact, target / artifact)
        observed = audit["observed"]
        items = [
            f"<a href='{filename}'>{html.escape(name)} playback</a>",
            html.escape(
                str({key: expected["cases"][name][key] for key in ("mass", "coupling", "reserve")})
            ),
            html.escape(str(observed.get("first_two_arrivals", []))),
            html.escape(str(observed.get("probe_departure_ticks", observed["source_departures"]))),
            f"{sum(audit['checks'].values())}/{len(audit['checks'])} checks",
            "PASS" if audit["passed"] else "FAIL",
        ]
        rows.append("<tr>" + "".join(f"<td>{item}</td>" for item in items) + "</tr>")
    passed = sum(audit["passed"] for audit in summary["acceptance"])
    details = "".join(
        f"<details><summary>{html.escape(audit['name'])}: exact checks</summary>"
        f"<pre>{html.escape(json.dumps(audit, indent=2))}</pre></details>"
        for audit in summary["acceptance"]
    )
    display_path = run_root / "display-checks.json"
    display_report = (
        json.loads(display_path.read_text(encoding="utf-8")) if display_path.exists() else None
    )
    display_note = (
        "Headless JavaScript checks verified six held probes at their owning Node, a single owned "
        "held field, release labels and unchanged snapshots in P6/P2. Browser visual inspection was "
        "not performed: the Cloud browser URL policy blocked the local page."
        if display_report is not None
        else "No separate browser visual-inspection evidence is included."
    )
    report = (
        "<!doctype html><html lang='en'><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Universe24: mass and computation-field timing</title>"
        "<style>body{max-width:1100px;margin:32px auto;padding:0 18px;font:16px system-ui;"
        "color:#183c31;background:#f1f6f2}h1{font-size:28px}p{line-height:1.5}"
        "table{width:100%;border-collapse:collapse;font-size:14px}td,th{padding:10px;text-align:left;"
        "border-bottom:1px solid #b6cdbd}a{color:#135e44}pre{white-space:pre-wrap;overflow-wrap:anywhere;"
        "background:white;padding:14px}details{margin:14px 0}summary{cursor:pointer}"
        ".scroll{overflow:auto}.status{background:#d6eedb;padding:18px;border-radius:10px}</style>"
        "<h1>Mass → computation rays → output delay</h1>"
        f"<p class='status'><b>{passed}/{len(summary['acceptance'])} configured fixtures passed.</b> "
        "This is a test of the named integer candidate, not empirical validation of gravity.</p>"
        "<p>The source is held in place and emits funded computation tokens. Each Node responds only "
        "to actual local emission or reception. Six output clocks delay departure; input receipt "
        "and the fixed one-tick Link transit remain separate. Nonemitting probes test the timing. "
        "The existing free-emitter self-field rules are outside this candidate's admitted composition.</p>"
        "<p>The playback shows recorded states only. Dashed shapes remain owned by their Node until "
        "the displayed release tick. Rings and diamonds denote actual Link transfers. "
        "The exact clock/ownership table is available in each playback.</p>"
        f"<p>{html.escape(display_note)}</p>"
        "<div class='scroll'><table><thead><tr><th>Fixture</th><th>Frozen parameters</th>"
        "<th>First two field arrivals</th><th>Selected departures</th><th>Checks</th><th>Result</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
        "<p>M1–M3 vary mass; Z1 disables clock coupling while still emitting; Z2 emits no field. "
        "G2 doubles clock coupling. C1/C2 test reception and an already departed probe. "
        "P6 releases six outputs together; P2 admits new input while another face is held. "
        "L1 retains the source and emits at ticks 0, 8 and 16 from a finite reserve.</p>"
        "<p>Token accounting is not a physical energy assignment. Proper-time calibration, "
        "gravitational redshift, nuclear binding, arbitrary moving emitters and unrestricted "
        "same-Port collisions are not established by these fixtures.</p>"
        f"<p>Source fingerprint: <code>{html.escape(next(iter(runs.values()))['source_sha256'])}</code></p>"
        "<p><a href='universe24-mass-clock-summary.json'>Structured results</a> · "
        "<a href='universe24-mass-clock-expectations.json'>Frozen expectations</a> · "
        "<a href='universe24-mass-clock-provenance.json'>Source and file fingerprints</a></p>"
        + details
        + "</html>"
    )
    path = output / "universe24-mass-clock-report.html"
    path.write_text(report, encoding="utf-8")
    shutil.copyfile(run_root / "summary.json", output / "universe24-mass-clock-summary.json")
    shutil.copyfile(HERE / "expectations.json", output / "universe24-mass-clock-expectations.json")
    if display_report is not None:
        shutil.copyfile(display_path, output / "universe24-mass-clock-display-checks.json")
    for artifact in sorted(output.rglob("*")):
        if artifact.is_file():
            provenance["files"][artifact.relative_to(output).as_posix()] = hashlib.sha256(
                artifact.read_bytes()
            ).hexdigest()
    (output / "universe24-mass-clock-provenance.json").write_text(
        json.dumps(provenance, indent=2) + "\n", encoding="utf-8"
    )
    archive = output / "universe24-mass-clock-evidence.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for artifact in sorted(output.rglob("*")):
            if artifact.is_file() and artifact != archive:
                bundle.write(artifact, artifact.relative_to(output))
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_root", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-commit")
    args = parser.parse_args()
    print(write_report(args.run_root, args.output, args.source_commit))
