"""Run the configuration-only reflection experiment and retain original HTML players."""

import argparse
import base64
import gzip
import hashlib
import html
import io
import json
import math
import platform
import re
from pathlib import Path

from cases import cases
from measurements import analyze

from event_universe.reference_api import parse_reference_state as parse_initial_state
from event_universe.reference_runner import run_reference_initialization as run_initialization
from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import source_fingerprint


def read_recording(directory):
    movie = (directory / "run.html").read_text()
    match = re.search(r'<script id="recording" type="application/json">(.*?)</script>', movie, re.S)
    if match is None:
        raise ValueError("missing canonical recording")
    recording = json.loads(match.group(1))
    if recording["metadata"] != json.loads((directory / "run.json").read_text()):
        raise ValueError("HTML metadata differs from run metadata")
    return movie, recording


def assess(results, recordings):
    for name, result in results.items():
        if result["kind"] == "wave":
            measured = result["frequency"]
            assert measured["status"] == "measured", name
            assert measured["recurrence_residual"] < 1e-8, name
            if name.startswith("axial"):
                assert abs(measured["phase_speed"] - 0.5) < 1e-8, name
            else:
                # Independent matrix predictions supplied before engine execution.
                expected = {9: 0.7672154454689077, 15: 0.4655332934913530}
                assert abs(measured["omega"] - expected[result["shape"][0]]) < 1e-8, name
        if result["kind"] in ("wave", "control"):
            assert result["rows"][0]["magnetic_squared"] == 0
            assert any(row["magnetic_squared"] > 0 for row in result["rows"][1:]), name
        if result["kind"] == "compact":
            center = result["shape"][0] // 2
            for frame in recordings[name]["frames"]:
                assert all(
                    sum(abs(x - center) for x in node["position"]) <= frame["tick"]
                    for node in frame["spatial_fields"]
                    if any(v for field in node["fields"].values() for v in field["value"])
                ), name
    if "oblique-9" in results and "oblique-15" in results:
        assert (
            results["oblique-15"]["frequency"]["relative_error_from_half_link_speed"]
            < results["oblique-9"]["frequency"]["relative_error_from_half_link_speed"]
        )
    if "stream-only-control" in results:
        assert abs(results["stream-only-control"]["frequency"]["phase_speed"] - 1) < 1e-8
    if "longitudinal-control" in results:
        assert all(r["magnetic_squared"] == 0 for r in results["longitudinal-control"]["rows"])
        assert len({r["electric_squared"] for r in results["longitudinal-control"]["rows"]}) == 1
    if "centered-gauss-control" in results:
        rows = results["centered-gauss-control"]["rows"]
        assert rows[0]["centered_div_e_max"] == 0
        assert rows[1]["centered_div_e_max"] != 0  # A measured physical blocker remains visible.
    if "compact-9" in recordings and "compact-15" in recordings:

        def translated(frame, center):
            return sorted(
                (tuple(x - center for x in node["position"]), name, field["value"])
                for node in frame["spatial_fields"]
                for name, field in node["fields"].items()
                if any(field["value"])
            )

        assert [translated(f, 4) for f in recordings["compact-9"]["frames"]] == [
            translated(f, 7) for f in recordings["compact-15"]["frames"]
        ]


def plot(results):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 2, figsize=(11, 3.6), layout="constrained")
    for name in ("axial-15", "stream-only-control"):
        if name not in results:
            continue
        rows = results[name]["rows"]
        initial = rows[0]["polarized_electric_mode"]
        axes[0].plot(
            [r["tick"] for r in rows][::2],
            [r["polarized_electric_mode"] / initial for r in rows][::2],
            "o-",
            label=name,
        )
    times = [i / 10 for i in range(161)]
    axes[0].plot(times, [math.cos(math.pi * t / 15) for t in times], "--", label="Vacuum target, c=0.5")
    axes[0].set(
        xlabel="Tick", ylabel="Normalized electric Fourier mode", title="Electric-only initial wave"
    )
    axes[0].legend(fontsize=8)
    for name in ("axial-9", "oblique-9", "oblique-15"):
        if name in results:
            rows = results[name]["rows"]
            axes[1].plot(
                [r["tick"] for r in rows], [r["macro_energy_fraction"] for r in rows], label=name
            )
    axes[1].axhline(1, linestyle="--", color="black", label="Conserved full population norm")
    axes[1].set(xlabel="Tick", ylabel="Macro EM proxy / total norm", title="Extra kinetic modes remain")
    axes[1].legend(fontsize=8)
    stream = io.StringIO()
    figure.savefig(stream, format="svg")
    plt.close(figure)
    return "<svg" + stream.getvalue().split("<svg", 1)[1]


def report(output, results, movies, provenance):
    rows = []
    for name, result in results.items():
        frequency = result["frequency"]
        speed = f"{frequency['phase_speed']:.9f}" if "phase_speed" in frequency else frequency["status"]
        energy = [r["macro_energy_fraction"] for r in result["rows"]]
        div = [r["centered_div_e_max"] for r in result["rows"]]
        rows.append(
            f"<tr><td>{html.escape(name)}</td><td>{' × '.join(map(str, result['shape']))}</td><td>{speed}</td><td>Exact</td><td>{min(energy):.6f}–{max(energy):.6f}</td><td>{div[0]} → {max(div)}</td></tr>"
        )
    options = "".join(
        f'<option value="{i}">{html.escape(name)}</option>' for i, name in enumerate(movies)
    )
    # Compress complete canonical movies; no recorded frames are removed.
    players = json.dumps(
        [base64.b64encode(gzip.compress(movie.encode(), mtime=0)).decode() for movie in movies.values()]
    )
    document = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Universe24: local reflection and the vacuum Maxwell limit</title>
<style>body{{font:16px system-ui;color:#17273b;background:#f8fafc;margin:24px}}main{{max-width:1200px;margin:auto}}p{{line-height:1.6;max-width:1050px}}h1{{font-size:28px}}table{{border-collapse:collapse;width:100%;background:white}}th,td{{padding:10px;border-bottom:1px solid #ccd6e1;text-align:left}}.table{{overflow:auto}}.limits{{background:#fff1db;padding:16px;border-left:4px solid #b87b16}}iframe{{width:100%;height:780px;border:1px solid #ccd6e1;margin-top:16px}}select{{font:inherit;padding:10px;max-width:100%}}svg{{max-width:100%;height:auto}}</style><main>
<h1>Local reflection and the vacuum Maxwell limit</h1>
<p>Six transverse vector populations undergo the same local reflection, then cross one nearest-neighbor link. The engine evaluates integer sums, cross products, sign changes and exact halves. Electric and magnetic moments below are read-only sums of those populations. No continuum derivative supplies a physical update.</p>
<p>The selected scattering hypothesis has a conditional long-wavelength vacuum Maxwell limit with speed <b>0.5 link per tick</b>. The causal link speed remains 1. The runs compare two polarizations, an axis rotation, oblique wavelengths, a streaming-only control and compact 9-cubed/15-cubed domains. Thin periodic boxes represent plane waves uniform in their short directions; they are not localized three-dimensional radiation.</p>
{plot(results)}
<div class="limits"><b>Physical limits found:</b> centered discrete electric Gauss conservation fails for the initially divergence-free oblique control. The exact conserved quantity is population norm; the macro electric/magnetic energy proxy exchanges with additional kinetic modes. Integer exact division is guaranteed here only within the fixed 18-step divisibility budget, subject to runtime bounds. This does not establish full Maxwell with charges, physical light speed, Lorentz force, photons or indefinite integer evolution.</div>
<h2>Measured results</h2><div class="table"><table><thead><tr><th>Experiment</th><th>Shape</th><th>Phase speed</th><th>Population norm</th><th>Macro fraction range</th><th>Centered div E, raw max</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<h2>Original recorded runs</h2><p>The canonical player shows the six population fields. E and B are derived measurements, not additional stored field stock.</p><select id="case">{options}</select><iframe id="viewer" title="Original simulator playback" sandbox="allow-scripts"></iframe>
<details><summary>Source and measurement provenance</summary><pre>{html.escape(json.dumps(provenance, indent=2))}</pre></details>
<script id="runs" type="application/json">{players}</script><script>const runs=JSON.parse(document.getElementById('runs').textContent);const choice=document.getElementById('case');let request=0;async function show(){{const current=++request;try{{const bytes=Uint8Array.from(atob(runs[Number(choice.value)]),c=>c.charCodeAt(0));const stream=new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));const movie=await new Response(stream).text();if(current===request)document.getElementById('viewer').srcdoc=movie;}}catch(error){{document.getElementById('viewer').srcdoc='<p>This browser cannot open the recorded player. Open this report in an up-to-date browser.</p>';}}}}choice.addEventListener('change',show);show();</script></main></html>"""
    (output / "report.html").write_text(document)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--resume", action="store_true", help="Reuse exact successful input/source recordings"
    )
    args = parser.parse_args()
    output = args.output.resolve()
    validate_output_path(output)
    if output.exists() and not args.resume:
        raise ValueError("use a new output directory or explicitly resume")
    output.mkdir(parents=True, exist_ok=True)
    (output / "inputs").mkdir(exist_ok=True)
    summary = output / "summary.json"
    report_path = output / "report.html"
    summary.touch(exist_ok=True)
    report_path.touch(exist_ok=True)
    with ArtifactLease(output, [output / "inputs", summary, report_path]):
        execute(output, args.resume)


def execute(output, resume):
    selected = cases()
    for case in selected.values():
        parse_initial_state(case["input"])
    fingerprint = source_fingerprint()
    results, recordings, movies = {}, {}, {}
    for name, case in selected.items():
        source = (json.dumps(case["input"], indent=2) + "\n").encode()
        initial = output / "inputs" / (name + ".json")
        destination = output / "runs" / name
        if not destination.exists():
            initial.write_bytes(source)
            run_initialization(initial, destination, visualize=True)
        elif not resume or initial.read_bytes() != source:
            raise ValueError("existing run differs from selected input")
        movie, recording = read_recording(destination)
        meta = recording["metadata"]
        assert meta["status"] == "completed" and meta["completed_ticks"] == case["input"]["ticks"]
        assert meta["source_sha256"] == fingerprint
        assert meta["initialization_sha256"] == hashlib.sha256(source).hexdigest()
        assert meta["accounting_balanced_at_every_completed_tick"]
        sends = 0
        with (destination / "events.jsonl").open() as stream:
            for line in stream:
                event = json.loads(line)
                if event["event"] == "spatial_sent":
                    assert event["arrival_tick"] - event["tick"] == 1
                    sends += 1
        result = analyze(case, recording)
        result.update(metadata=meta, completed_sends=sends)
        results[name], recordings[name], movies[name] = result, recording, movie
        (output / "summary.json").write_text(json.dumps(results, indent=2) + "\n")
        print(name, json.dumps(result["frequency"]), flush=True)
    assess(results, recordings)
    assert source_fingerprint() == fingerprint
    provenance = {
        "python": platform.python_version(),
        "source_sha256": fingerprint,
        "runs": len(results),
        "fixed_amplitude_scale": 1 << 20,
        "maximum_exact_ticks": 18,
    }
    report(output, results, movies, provenance)
    print(output / "report.html", flush=True)


if __name__ == "__main__":
    main()
