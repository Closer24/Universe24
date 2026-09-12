"""Headless replay verifies recorded values before a separate GIF export."""

import argparse
import hashlib
import json
from pathlib import Path

from observe import measure

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_recording(path):
    html = path.read_text(encoding="utf-8")
    marker = '<script id="recording" type="application/json">'
    data = json.loads(html.split(marker, 1)[1].split("</script>", 1)[0])
    if data["metadata"]["status"] != "completed":
        raise ValueError("this comparison requires completed recordings")
    return data


def verify(path):
    from event_universe.reference_api import ReferenceSimulation as Simulation
    from event_universe.reference_api import parse_reference_json as parse_initial_json
    from event_universe.runner import source_fingerprint

    data = load_recording(path)
    initial = path.parent / "initialization.json"
    if digest(initial) != data["metadata"]["initialization_sha256"]:
        raise ValueError("recording input hash mismatch")
    if source_fingerprint() != data["metadata"]["source_sha256"]:
        raise ValueError("recording simulator source mismatch")
    definition = json.loads((HERE / "definition.json").read_text(encoding="utf-8"))
    world = Simulation(parse_initial_json(initial.read_bytes()))
    expected = measure(world.snapshot(), definition["channels"])
    frames = {frame["tick"]: frame for frame in data["frames"]}
    if len(frames) != len(data["frames"]) or 0 not in frames:
        raise ValueError("recording ticks must be unique and include the initial state")
    for tick in range(data["metadata"]["completed_ticks"] + 1):
        if tick:
            world.step()
        state = world.snapshot()
        observed = measure(state, definition["channels"])
        if (observed["energy"], observed["momentum"]) != (expected["energy"], expected["momentum"]):
            raise ValueError("candidate energy or momentum changed during replay")
        if tick in frames and json.loads(json.dumps(state)) != frames[tick]:
            raise ValueError(f"recorded physical state differs at tick {tick}")
    if max(frames) != world.tick:
        raise ValueError("recording does not end at the completed tick")
    proof = {
        "html_sha256": digest(path),
        "initialization_sha256": digest(initial),
        "definition_sha256": digest(HERE / "definition.json"),
        "source_sha256": source_fingerprint(),
        "ticks": world.tick,
        "frames": len(frames),
        "energy": expected["energy"],
        "momentum": expected["momentum"],
        "energy_error_max": 0,
        "momentum_error_max": 0,
        "every_recorded_state_matches": True,
    }
    (path.parent / "recording-proof.json").write_text(
        json.dumps(proof, indent=2) + "\n", encoding="utf-8"
    )
    return proof


def checked_proof(path):
    proof = json.loads((path.parent / "recording-proof.json").read_text(encoding="utf-8"))
    if (
        proof["html_sha256"] != digest(path)
        or proof["initialization_sha256"] != digest(path.parent / "initialization.json")
        or proof["definition_sha256"] != digest(HERE / "definition.json")
        or proof["every_recorded_state_matches"] is not True
    ):
        raise ValueError("recording proof is missing, changed or stale")
    return proof


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recording", type=Path, required=True)
    print(json.dumps(verify(parser.parse_args().recording), indent=2))
