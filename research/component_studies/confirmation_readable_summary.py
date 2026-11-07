"""Add readable metadata sidecars without rewriting frozen study evidence."""
import hashlib
import json
from pathlib import Path

from research.signal_clocks.run import write_json

HERE = Path(__file__).resolve().parent


def main():
    families = [
        ("confirmation_search_evidence_v1", "Two-source guide search", 64,
         "No preparation passed the registered silent waiting and confirmation criterion. Every source-control recording remains available."),
        ("confirmation_buffer_evidence_v1", "Initial matching-buffer search", 81,
         "No matching-buffer preparation passed the same strict criterion. Initial-state assembly was valid; a working waiting device was not established."),
        ("confirmation_packet_evidence_v1", "Prepared guided compact packet", None,
         "The prepared packet translates one X site per update on the declared periodic guide, including every transverse retained remainder. Source-absent controls stay stationary. This is not a free-vacuum light result or a waiting detector."),
    ]
    for name, title, cases, interpretation in families:
        directory = HERE / name
        source = directory / "result.json"
        result = json.loads(source.read_text())
        sidecar = {"format": "universe24-readable-study-summary-v1", "title": title,
            "interpretation": interpretation,
            "original_result": "result.json", "original_result_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "original_protocol": "protocol.frozen.json",
            "original_protocol_sha256": hashlib.sha256((directory / "protocol.frozen.json").read_bytes()).hexdigest(),
            "source_of_truth": "The original protocol, source snapshot and complete traces are unchanged. This sidecar clarifies presentation language only.",
            "execution_status": result["execution_status"], "cpu_seconds": result["cpu_seconds"],
            "scope": "One board, 48 channels per node, six spatial inputs, unchanged Rule3 and the fixed positive reference coupling. All sources are initial conditions. Observations never change the evolution."}
        if cases is not None:
            sidecar.update({"cases_completed": result["cases_completed"], "runs_completed": result["runs_completed"],
                "accepted_cases": len(result["passing_cases"]),
                "boundary_scope": "The initial support is farther from the periodic boundary than the observation horizon."})
        else:
            sidecar.update({"runs_completed": result["runs"], "forward_steps": result["forward_steps"],
                "production_checks_passed": result["passed"],
                "boundary_scope": "This experiment deliberately uses a full periodic guide. Translation and recurrence include wraparound; the result is separate from a no-wrap receiver experiment.",
                "independent_review": "See research/component_review for independently recorded validation; production checks alone are not an independent audit."})
            descriptor = json.loads((directory / "presentation.json").read_text())
            descriptor["title"] = "Prepared guided compact packet: complete-state translation"
            for entry in descriptor["cases"]:
                entry["description"] = interpretation + " " + sidecar["boundary_scope"] + " Every full state is retained; playback does not inject signals or change Rule3."
            write_json(directory / "presentation_readable.json", descriptor)
        write_json(directory / "readable_summary.json", sidecar)
        print(json.dumps({"directory": name, "readable_summary": "readable_summary.json"}), flush=True)


if __name__ == "__main__":
    main()
