"""Run acceptance experiments for the opt-in shared interaction, with existing HTML.

Run after installation: python tools/shared_action_evidence.py
Exit 1 means a physical acceptance criterion FAILED. It is intentionally not
converted to success because the software contracts pass. All arithmetic below
is diagnostic and never feeds a value back into the simulated physical state.
"""

import argparse
import html
import json
import re
from dataclasses import asdict, replace
from pathlib import Path

from event_universe import SharedActionConfig
from event_universe.diagnostics.frames import Slice, capture_volume
from event_universe.diagnostics.measurements import audit, total_momentum
from event_universe.diagnostics.recorder import JsonlRecorder
from event_universe.diagnostics.render import render_volume
from event_universe.models.shared_action import MODEL_ID
from event_universe.runner import source_fingerprint
from event_universe.scenarios import Scenario, get_scenario


def cases():
    settings = SharedActionConfig(nx=96, ny=96, nz=96, c_units=60)
    diagonal = (0, 40, 40, 40, 3, 2, 1)
    resting = (0, 40, 40, 40, 0, 0, 0)
    fast = (0, 40, 40, 40, 27, 18, 9)
    for name, seed, coupling, ticks in (
        ("stationary", resting, 64, 120),
        ("free-diagonal", diagonal, 0, 120),
        ("isolated-slow", diagonal, 64, 360),
        ("isolated-fast", fast, 64, 90),
    ):
        selected = replace(settings, coupling=coupling)
        yield Scenario(name, selected.engine_config(), (seed,), ticks, Slice("XY", 40), action=selected)
    yield replace(get_scenario("action-contact"), ticks=48)
    original = get_scenario("action-contact")
    yield replace(
        original,
        name="near-pair-response",
        ticks=24,
        particles=((0, 30, 23, 16, 0, 0, 0), (1, 32, 25, 16, 0, 0, 0)),
    )


def run_case(scenario, directory):
    directory.mkdir(parents=True, exist_ok=True)
    records = []
    with (directory / "events.jsonl").open("w", encoding="utf-8") as stream:
        world = scenario.create(JsonlRecorder(stream))
        initial = {pid: state.momentum for pid, state in world.particles.items()}
        total_initial = total_momentum(world)
        frames = [capture_volume(world)]
        conserved = True
        valid = True
        for step in range(scenario.ticks):
            previous = dict(world.particles)
            world.step()
            audit(world)
            conserved = conserved and total_momentum(world) == total_initial
            for pid, state in world.particles.items():
                old = previous[pid]
                changed = state.momentum != initial[pid]
                residues = (state.force_rx, state.force_ry, state.force_rz)
                shape = (world.config.nx, world.config.ny, world.config.nz)
                hop = sum(
                    min(abs(a - b), extent - abs(a - b))
                    for a, b, extent in zip(state.position, old.position, shape, strict=True)
                )
                valid = valid and hop <= 1
                records.append(
                    {
                        "tick": world.tick,
                        "pid": pid,
                        "position": state.position,
                        "momentum": state.momentum,
                        "remainders": residues,
                        "momentum_changed": changed,
                        "response_detected": changed or any(residues),
                    }
                )
            if (step + 1) % max(1, scenario.ticks // 8) == 0:
                frames.append(capture_volume(world))
        if frames[-1].tick != world.tick:
            frames.append(capture_volume(world))
        if len(initial) == 1:
            accepted = not any(row["response_detected"] for row in records)
            criterion = "No isolated response in momentum OR residual impulse, every completed tick"
        else:
            accepted = any(row["momentum"][1] != initial[row["pid"]][1] for row in records)
            criterion = "Nonzero transverse pair response before the run ends"
        accepted = accepted and conserved and valid
        metadata = {
            "model": MODEL_ID,
            "source_sha256": source_fingerprint(),
            "source_basis": "GitHub main e74f2fdf390b5dc8036b707eefcfc53bc8a82c17",
            "scenario": asdict(scenario),
            "initialization": "empty field, no velocity-matched dressing",
            "physical_acceptance": "PASS" if accepted else "FAIL",
            "acceptance_requires": "criterion AND every-tick bookkeeping AND hop bound AND state audit",
            "criterion": criterion,
            "initial_momenta": initial,
            "final_momenta": {pid: state.momentum for pid, state in world.particles.items()},
            "final_remainders": {
                pid: (s.force_rx, s.force_ry, s.force_rz) for pid, s in world.particles.items()
            },
            "first_response_frame": next(
                (row["tick"] for row in records if row["response_detected"]), None
            ),
            "bookkeeping_momentum_conserved_each_tick": conserved,
            "hop_bound": valid,
            "all_state_audits_passed": True,
            "physical_self_force_solved": False,
            "full_variational_time_integrator": False,
            "field_structure": "unchanged screened relaxation; fixed one-tick causal ports",
        }
        (directory / "run.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        with (directory / "states.jsonl").open("w", encoding="utf-8") as output:
            for row in records:
                output.write(json.dumps(row) + "\n")
        render_volume(frames, directory / "run.html", title=scenario.name, metadata=metadata)
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("artifacts/shared-action"))
    args = parser.parse_args()
    results = []
    sections = []
    for scenario in cases():
        directory = args.output / scenario.name
        result = run_case(scenario, directory)
        results.append(result)
        page = (directory / "run.html").read_text(encoding="utf-8")
        image = re.search(r"<img [^>]+>", page).group(0)
        sections.append(
            f"<section><h2>{html.escape(scenario.name)} — {result['physical_acceptance']}</h2>"
            f"<p>{html.escape(result['criterion'])}</p>{image}"
            f"<pre>{html.escape(json.dumps(result, ensure_ascii=False, indent=2))}</pre></section>"
        )
        print(scenario.name, result["physical_acceptance"], result["final_momenta"], flush=True)
    failed = sum(r["physical_acceptance"] == "FAIL" for r in results)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    page = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    page += "<title>Shared local interaction — acceptance evidence</title><style>body{background:#111827;color:#eee;font-family:system-ui;max-width:1100px;margin:auto;padding:20px}img{width:100%;height:auto}section{padding:18px;margin:18px 0;background:#1f2937}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style></head><body>"
    page += '<h1 dir="rtl">צימוד מקומי משותף — בדיקות קבלה</h1><p dir="rtl">תלת־ממד מלא XYZ; לא חתך. הליבה בשלמים. זה מימוש של איבר האינטראקציה, לא פתרון מלא לכוח העצמי.</p>'
    page += f"<p>{len(results) - failed} acceptance passes / {failed} failures. Source and timestep limitations are shown below. No global momentum repair; recorded field momentum is bookkeeping.</p>"
    page += "".join(sections) + "</body></html>"
    (args.output / "index.html").write_text(page, encoding="utf-8")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
