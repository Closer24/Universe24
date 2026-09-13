"""Record existing reference controls for subsequent, separate output-only analysis.

No Newtonian formula is added to a runtime law. The collision is the unchanged
configured reference, not an emergence experiment. Controls only remove contact
and select initial conditions, duration and existing scale parameters.
"""

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from event_universe.runner import source_fingerprint

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "examples/04-unequal-mass-collision.json"
WINDOWS = {"collision-reference": 120, "free": 60, "rest": 30, "slow": 1000}


def controls(reference: dict) -> dict:
    result = {}
    for name in ("free", "rest", "slow"):
        document = copy.deepcopy(reference)
        document["interactions"] = []
        document["seeds"] = document["seeds"][:1]
        document["disturbance_types"] = document["disturbance_types"][:1]
        document["model_id"] = "newton-output-" + name + "-control-v1"
        document["ticks"] = {"free": 240, "rest": 120, "slow": 4000}[name]
        if name == "rest":
            document["disturbance_types"][0]["defaults"]["momentum"] = [0, 0, 0]
        if name == "slow":
            document["fields"][1]["scale"] = 1000
            document["fields"][1]["units"] = "mass unit times c / 1000"
            document["disturbance_types"][0]["defaults"]["momentum"] = [2, 0, 0]
            document["disturbance_types"][0]["transport"]["rate_denominator"] = 1000
        result[name] = document
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise ValueError("Use a new evidence directory; preserve earlier measurements")
    output.mkdir(parents=True)
    before = source_fingerprint()
    raw = REFERENCE.read_bytes()
    cases = {"collision-reference": REFERENCE}
    for name, document in controls(json.loads(raw)).items():
        path = output / (name + ".json")
        path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
        cases[name] = path
    contract = {
        "source_sha256": before,
        "reference_sha256": hashlib.sha256(raw).hexdigest(),
        "windows_ticks": WINDOWS,
        "scope": "Reference agreement, not emergence. Existing collision and p/m transport are configured laws.",
        "checks": "External Newtonian formulas are applied after each simulation process exits.",
    }
    # Measurement windows are recorded before execution, never fitted to a failed result.
    (output / "acceptance-contract.json").write_text(json.dumps(contract, indent=2) + "\n")
    for name, path in cases.items():
        subprocess.run(
            [
                sys.executable,
                "-m",
                "event_universe",
                "--init",
                str(path),
                "--output",
                str(output / name),
                "--visualize",
                "--frame-stride",
                "1",
            ],
            cwd=ROOT,
            check=True,
        )
    if source_fingerprint() != before or REFERENCE.read_bytes() != raw:
        raise RuntimeError("Runtime or canonical reference changed during evidence capture")
    print(output)


if __name__ == "__main__":
    main()
