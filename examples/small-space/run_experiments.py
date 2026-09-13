"""Run bounded physics comparisons with ordinary HTML playback and no GIF output."""

import argparse
import html
import json
import platform
import re
import subprocess
from pathlib import Path

from experiments import ROOT, candidates

from event_universe.initialization import parse_initial_state
from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import run_initialization, source_fingerprint


def records(frame):
    owned = [(node["position"], row) for node in frame["nodes"] for row in node["disturbances"]]
    owned += [(row["origin"], row) for row in frame["transfers"]]
    return sorted(
        (
            {"position": position, "type": row["type"], "values": row["values"]}
            for position, row in owned
        ),
        key=lambda row: row["type"],
    )


def field_norms(frame):
    result = {}
    for node in frame.get("spatial_fields", []):
        for name, field in node["fields"].items():
            result[name] = result.get(name, 0) + sum(value * value for value in field["value"])
    for packet in frame.get("spatial_transfers", []):
        for name, populations in packet["fields"].items():
            result[name] = result.get(name, 0) + sum(v * v for pop in populations for v in pop)
    return result


def physical_frame(frame, size):
    """Read-only comparison after translating the origin; ignore dormant host nodes."""
    center = size // 2

    def point(position):
        return tuple(v - center for v in position) if position is not None else None

    carriers = sorted((point(row["position"]), row["type"], row["values"]) for row in records(frame))
    fields = sorted(
        (point(node["position"]), name, field["value"], field["populations"])
        for node in frame.get("spatial_fields", [])
        for name, field in node["fields"].items()
        if any(field["value"]) or any(any(pop) for pop in field["populations"])
    )
    packets = sorted(
        (point(packet["origin"]), packet["port"], packet["fields"])
        for packet in frame.get("spatial_transfers", [])
    )
    return carriers, fields, packets


def shell_measurements(frames, size):
    center = size // 2
    rows = []
    for frame in frames:
        shells = {}
        for node in frame.get("spatial_fields", []):
            field = node["fields"].get("radiation")
            if field and field["value"][0]:
                offset = [v - center for v in node["position"]]
                radius = sum(abs(v) for v in offset)
                shell = shells.setdefault(
                    radius, {"stock": 0, "active_nodes": 0, "squared_distances": set()}
                )
                shell["stock"] += field["value"][0]
                shell["active_nodes"] += 1
                shell["squared_distances"].add(sum(v * v for v in offset))
        rows.append(
            {
                "tick": frame["tick"],
                "shells": {
                    radius: {**shell, "squared_distances": sorted(shell["squared_distances"])}
                    for radius, shell in shells.items()
                },
            }
        )
    return rows


def first_signal(frames, position):
    return next(
        (
            frame["tick"]
            for frame in frames
            for node in frame.get("spatial_fields", [])
            if node["position"] == position and any(node["fields"]["radiation"]["value"])
        ),
        None,
    )


def assess(runs):
    """Evidence and physical gaps remain separate from software check success."""
    results = []

    def row(name, status, evidence, limit):
        results.append(
            {"experiment": name, "physical_status": status, "evidence": evidence, "limit": limit}
        )

    def owned(name, last=True):
        return records(runs[name]["frames"][-1 if last else 0])

    rest = owned("electron-rest")
    assert rest == owned("electron-rest", False)
    row(
        "Isolated rest",
        "restricted agreement",
        "No displacement or momentum drift in four ticks.",
        "Free-space rest only; no field response selected.",
    )
    moving = owned("electron-free")[0]
    double = owned("electron-double-momentum")[0]
    assert moving["values"]["momentum"] == [1, 0, 0] and double["values"]["momentum"] == [2, 0, 0]
    row(
        "Momentum and inertial motion",
        "missing law",
        f"Both momentum 1 and 2 end at {moving['position']}; same trajectory: {moving['position'] == double['position']}.",
        "The catalog supplies a fixed rate; mass-dependent motion has not emerged.",
    )
    row(
        "Photon record",
        "physical mismatch",
        f"Starts at {owned('photon-free', False)[0]['position']}, ends at {owned('photon-free')[0]['position']} after four ticks.",
        "Two hops instead of the four available light-speed links; a record proxy is not a physical photon.",
    )
    assert owned("photon-speed-candidate")[0]["position"] == [6, 4, 4]
    row(
        "Photon-speed parameter candidate",
        "mechanism demonstrated",
        "Changing the explicit transport denominator from 2 to 1 produces four causal hops in four ticks.",
        "A configured light-speed ray proxy; no quantum photon, polarization or emission law is established.",
    )
    charges = owned("charges-in-electric-background")
    assert all(row["values"]["momentum"] == [0, 0, 0] for row in charges)
    row(
        "Positive, negative and neutral charge under E",
        "missing law",
        "All three momentum registers remain zero under nonzero E.",
        "Profiles supply no charge-to-field coupling; holding positions alone does not explain absent momentum response.",
    )
    row(
        "Electric/magnetic propagation",
        "missing law",
        f"Electric-only pulse final squared magnetic register sum: {field_norms(runs['electric-only-pulse']['frames'][-1]).get('B', 0)}.",
        "No E/B mixing or Maxwell constraints. Parallel E/B catalog samples are not vacuum plane waves.",
    )
    equal = owned("equal-contact-9")
    assert [r["values"]["momentum"][0] for r in equal] == [-1, 1]
    row(
        "Equal-mass head-on contact",
        "restricted agreement",
        "The two momenta reverse and their total remains zero.",
        "Explicit selected permutation; no general collision law derived.",
    )
    unequal = owned("unequal-contact-current")
    assert {r["values"]["mass"][0]: r["values"]["momentum"][0] for r in unequal} == {1: 1, 2: -1}
    row(
        "Unequal masses under current pair rule",
        "missing law",
        "Masses 1 and 2 pass through with unchanged momenta because the equal-mass guard rejects the collision.",
        "Adding mass metadata does not extend the contact law.",
    )
    candidate = owned("unequal-zero-total-candidate")
    assert {r["values"]["mass"][0]: r["values"]["momentum"][0] for r in candidate} == {1: -1, 2: 1}
    row(
        "Unequal-mass zero-total candidate",
        "restricted agreement",
        "Masses 1 and 2 reverse opposite momenta using only exchange; each squared momentum and total momentum persist.",
        "Only total momentum zero; rates 1/2 and 1/4 and momentum scale 2 are supplied, not derived inertia or relativistic scattering.",
    )
    pulse = runs["outward-pulse-9"]["frames"]
    arrivals = [first_signal(pulse, p) for p in ([7, 4, 4], [6, 6, 5])]
    assert arrivals == [3, 5]
    row(
        "Equal-distance point-source propagation",
        "microscopic anisotropy",
        f"Squared distance 9 at both probes; arrival ticks {arrivals}.",
        "Manhattan link distance differs. This does not settle the long-wavelength limit or establish gravity.",
    )
    for left, right, until in [
        ("equal-contact-9", "equal-contact-15", 12),
        ("outward-pulse-9", "outward-pulse-15", 4),
        ("source-response-9", "source-response-15", 3),
    ]:
        assert [physical_frame(f, 9) for f in runs[left]["frames"][: until + 1]] == [
            physical_frame(f, 15) for f in runs[right]["frames"][: until + 1]
        ]
    row(
        "9-cubed versus 15-cubed",
        "restricted agreement",
        "Translated contact, outward pulse and source-response trajectories and field stock agree before relevant boundary differences.",
        "Domain independence for these finite trials, not a continuum proof.",
    )
    positive = next(r for r in owned("source-response-9") if r["type"] == "held_receiver")
    negative = next(r for r in owned("source-response-negative") if r["type"] == "held_receiver")
    zero = owned("receiver-without-source")[0]
    assert positive["values"]["momentum"] == [72, 0, 0]
    assert negative["values"]["momentum"] == [-72, 0, 0]
    assert zero["values"]["momentum"] == [0, 0, 0]
    row(
        "Local source-to-receiver exchange",
        "mechanism demonstrated",
        "Final response +72, -72, or zero according to polarity/source; field receives the opposite vector.",
        "Explicit candidate on a held receiver, externally injected scalar field, no energy or Coulomb/gravity law established.",
    )
    closed = runs["closed-reservoir"]
    name = next(iter(closed["metadata"]["initial_totals"]))
    assert closed["metadata"]["initial_totals"][name] == closed["metadata"]["final_totals"][name] == [3]
    assert closed["metadata"]["source_totals"][name] == [0]
    assert owned("closed-reservoir")[0]["values"][name] == [0]
    assert closed["metadata"]["spatial_accounting"][name]["current"] == [3]
    row(
        "Finite owned reservoir solution",
        "mechanism demonstrated",
        "Three units move from carrier to field; source injection zero; reservoir stops at zero.",
        "Exact abstract inventory transfer, not identified physical energy or a computational gravity law.",
    )
    row(
        "Other field families",
        "representation only",
        "Higgs, strong and computational registers propagate with exact configured component accounting.",
        "No Higgs mass mechanism, gauge dynamics, confinement or computation-clock feedback supplied by these profiles.",
    )
    return results


def report(output, runs, result):
    summaries = "".join(
        f"<tr><td>{html.escape(row['experiment'])}</td><td>{html.escape(row['physical_status'])}</td><td>{html.escape(row['evidence'])}</td><td>{html.escape(row['limit'])}</td></tr>"
        for row in result["comparisons"]
    )
    options = "".join(
        f'<option value="{index}">{html.escape(name)}</option>' for index, name in enumerate(runs)
    )
    payload = json.dumps([r["html"] for r in runs.values()]).replace("<", "\\u003c")
    document = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Universe24 small-space physics experiments</title>
<style>body{{font:16px system-ui;margin:24px;background:#f6f8fb;color:#182336}}h1{{font-size:28px}}table{{border-collapse:collapse;width:100%;background:white}}th,td{{text-align:left;vertical-align:top;border-bottom:1px solid #ccd4dd;padding:12px}}th{{background:#e8edf4}}select{{font:inherit;padding:10px;max-width:100%}}iframe{{width:100%;height:780px;border:1px solid #ccd4dd;margin-top:16px;background:white}}.note{{max-width:1000px;line-height:1.6}}</style>
<h1>Small-space physics experiments</h1><p class="note">{len(runs)} recorded experiments, 9×9×9 and 15×15×15. Exact configured accounting is checked separately from resemblance to real physics. No GIFs. Missing laws remain visible below. The player shows the existing simulator's recorded HTML without modifying trajectories.</p>
<table><thead><tr><th>Question</th><th>Finding</th><th>Observed evidence</th><th>Scope</th></tr></thead><tbody>{summaries}</tbody></table>
<h2>Recorded runs</h2><select id="case">{options}</select><iframe id="viewer" title="Original simulation playback" sandbox="allow-scripts"></iframe>
<p class="note">Runtime source: {html.escape(result["source_sha256"])}. Python {html.escape(result["python"])}. Full physical particle/field laws and emergent annihilation remain unestablished.</p>
<script id="runs" type="application/json">{payload}</script><script>const runs=JSON.parse(document.getElementById('runs').textContent);const select=document.getElementById('case');function show(){{document.getElementById('viewer').srcdoc=runs[Number(select.value)];}}select.addEventListener('change',show);show();</script></html>"""
    (output / "report.html").write_text(document, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    validate_output_path(output)
    if output.exists():
        raise ValueError("use a new output directory")
    cases = candidates()
    for raw in cases.values():
        parse_initial_state(raw)
    output.mkdir(parents=True)
    (output / "inputs").mkdir()
    (output / "summary.json").touch()
    (output / "report.html").touch()
    with ArtifactLease(output, [output / "inputs", output / "summary.json", output / "report.html"]):
        runs = {}
        fingerprint = source_fingerprint()
        for name, raw in cases.items():
            initial = output / "inputs" / (name + ".json")
            initial.write_text(json.dumps(raw, indent=2) + "\n")
            destination = output / "runs" / name
            run_initialization(initial, destination, visualize=True)
            movie = (destination / "run.html").read_text()
            recorded = json.loads(
                re.search(
                    r'<script id="recording" type="application/json">(.*?)</script>', movie, re.S
                ).group(1)
            )
            meta = recorded["metadata"]
            assert meta["status"] == "completed" and meta["source_sha256"] == fingerprint
            assert meta["accounting_balanced_at_every_completed_tick"]
            events = [
                json.loads(line) for line in (destination / "events.jsonl").read_text().splitlines()
            ]
            assert all(
                e["arrival_tick"] - e["tick"] == raw["link_ticks"]
                for e in events
                if e["event"] in ("sent", "spatial_sent")
            )
            runs[name] = {
                **recorded,
                "html": movie,
                "recorded_output": str(destination.relative_to(output)),
            }
            print(name, "completed", flush=True)
        result = {
            "python": platform.python_version(),
            "source_sha256": fingerprint,
            "git_head": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "run_count": len(runs),
            "comparisons": assess(runs),
            "pulse_shells": shell_measurements(runs["outward-pulse-9"]["frames"], 9),
            "runs": {
                name: {
                    "recorded_output": r["recorded_output"],
                    "metadata": r["metadata"],
                    "initial_records": records(r["frames"][0]),
                    "final_records": records(r["frames"][-1]),
                    "final_squared_register_sum": field_norms(r["frames"][-1]),
                }
                for name, r in runs.items()
            },
        }
        assert source_fingerprint() == fingerprint
        (output / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
        report(output, runs, result)
        print(output / "report.html")


if __name__ == "__main__":
    main()
