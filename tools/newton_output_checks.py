"""Compare saved simulator measurements with Newtonian targets; never run a world.

Only standard-library imports are allowed. Formulas here are external acceptance
criteria, not simulator laws. Coordinates are lattice links and time is run ticks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

Vector = tuple[Fraction, ...]
ZERO = (Fraction(0),) * 3


class NotTestable(ValueError):
    """Required measurements or the supported physical regime are absent."""


def _unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def decode(text: str) -> Any:
    return json.loads(text, object_pairs_hook=_unique)


def rational(value: Any) -> Fraction:
    if type(value) is not int and not isinstance(value, str):
        raise ValueError("Measurements must use integers or exact rational strings")
    return Fraction(value)


def vector(values: Any) -> Vector:
    if not isinstance(values, list) or len(values) != 3:
        raise ValueError("Expected a three-component measured vector")
    return tuple(rational(value) for value in values)


def sub(left: Vector, right: Vector) -> Vector:
    return tuple(a - b for a, b in zip(left, right, strict=True))


def dot(left: Vector, right: Vector) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def norm_max(value: Vector) -> Fraction:
    return max(map(abs, value))


def result(status: str, formula: str, **details: Any) -> dict[str, Any]:
    return {"status": status, "formula": formula, **details}


def measured_check(formula: str, error: Fraction, tolerance: Fraction, **details: Any) -> dict:
    return result(
        "pass" if error <= tolerance else "fail",
        formula,
        max_absolute_error=str(error),
        tolerance=str(tolerance),
        **details,
    )


class RecordingParser(HTMLParser):
    """Read the existing JSON recording without running JavaScript or rendering."""

    def __init__(self) -> None:
        super().__init__()
        self.active = False
        self.parts: list[str] = []
        self.count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "script" and values.get("id") == "recording":
            if values.get("type") != "application/json":
                raise ValueError("The recording must be non-executable JSON")
            self.active = True
            self.count += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self.active = False

    def handle_data(self, data: str) -> None:
        if self.active:
            self.parts.append(data)


def load_run(folder: Path) -> tuple[dict, dict, list[dict], dict]:
    raw = {
        name: (folder / name).read_bytes()
        for name in (
            "run.json",
            "initialization.json",
            "state.json",
            "run.html",
        )
    }
    hashes = {name: hashlib.sha256(content).hexdigest() for name, content in raw.items()}
    meta = decode(raw["run.json"].decode("utf-8"))
    initial = decode(raw["initialization.json"].decode("utf-8"))
    if meta.get("status") != "completed" or meta.get("error") is not None:
        raise ValueError("A failed or incomplete simulator run cannot pass acceptance")
    ticks = meta.get("completed_ticks")
    if type(ticks) is not int or ticks < 1 or ticks != meta.get("requested_ticks"):
        raise ValueError("Requested and completed physical ticks must match")
    if meta.get("initialization_sha256") != hashes["initialization.json"]:
        raise ValueError("Saved initialization fingerprint does not match run metadata")
    if meta.get("model") != initial.get("model_id") or not meta.get("source_sha256"):
        raise ValueError("Missing or inconsistent model/source identity")
    parser = RecordingParser()
    parser.feed(raw["run.html"].decode("utf-8"))
    if parser.count != 1:
        raise NotTestable("Exactly one saved full-world JSON recording is required")
    document = decode("".join(parser.parts))
    if document.get("observation") is not None:
        raise NotTestable("A local observer recording is not a global Newtonian audit")
    if document.get("metadata") != meta:
        raise ValueError("Recording and run metadata disagree")
    frames = document.get("frames")
    if (
        not isinstance(frames, list)
        or any(type(f.get("tick")) is not int for f in frames)
        or [f.get("tick") for f in frames] != list(range(ticks + 1))
    ):
        raise NotTestable("Every physical tick, including tick zero and the endpoint, is required")
    final = decode(raw["state.json"].decode("utf-8"))
    for key in ("cells", "transfers"):
        if frames[-1].get(key) != final.get(key):
            raise ValueError(f"Final recording and state disagree: {key}")
    return meta, initial, frames, hashes


def tracks(initial: dict, frames: list[dict]) -> dict[str, list[dict]]:
    """Narrow first adapter: unique persistent types, unit-link resident snapshots.

    No inferred subcell position, hidden movement credit or momentum-derived
    velocity is used. Ambiguous identity and unobserved transit are blockers.
    """
    if initial.get("link_ticks", 1) != 1 or initial.get("topology"):
        raise NotTestable("This adapter requires the standard unit-link lattice")
    if any(
        initial.get(key)
        for key in (
            "spatial_fields",
            "event_program",
            "emissions",
            "reactions",
            "conversions",
        )
    ):
        raise NotTestable("Field, reaction and native-event ownership need a dedicated audit adapter")
    definitions = {field["name"]: field for field in initial["fields"]}
    if not {"mass", "momentum"} <= definitions.keys():
        raise NotTestable("Measured mass and momentum are required; inventory is not mass")
    scales = {name: rational(definitions[name].get("scale", 1)) for name in ("mass", "momentum")}
    if any(value <= 0 for value in scales.values()):
        raise ValueError("Field scales must be positive")
    shape = initial["shape"]
    if len(shape) != 3 or any(type(size) is not int or size < 3 for size in shape):
        raise ValueError("Three integer lattice sizes of at least three are required")
    periodic = initial.get("boundary", "periodic") == "periodic"
    output: dict[str, list[dict]] = {}
    for frame in frames:
        if frame.get("transfers") or frame.get("spatial_transfers"):
            raise NotTestable("Transit ownership is present; no position will be invented")
        seen = set()
        for cell in frame["cells"]:
            for record in cell["disturbances"]:
                name = record["type"]
                if name in seen:
                    raise NotTestable("Repeated types lack a persistent per-body output identity")
                seen.add(name)
                values = record["values"]
                if not {"mass", "momentum"} <= values.keys():
                    raise NotTestable("Every tracked owner must expose mass and momentum")
                if len(values["mass"]) != 1:
                    raise ValueError("Mass must be scalar")
                mass = rational(values["mass"][0]) / scales["mass"]
                if mass <= 0:
                    raise NotTestable("Newtonian massive-body checks require positive mass")
                momentum = tuple(value / scales["momentum"] for value in vector(values["momentum"]))
                position = vector(cell["position"])
                if any(
                    p.denominator != 1 or p < 0 or p >= size
                    for p, size in zip(position, shape, strict=True)
                ):
                    raise ValueError("Invalid recorded lattice coordinate")
                history = output.setdefault(name, [])
                unwrapped = position
                if history:
                    delta = list(sub(position, history[-1]["position"]))
                    if periodic:
                        for axis, size in enumerate(shape):
                            if 2 * delta[axis] > size:
                                delta[axis] -= size
                            elif 2 * delta[axis] < -size:
                                delta[axis] += size
                    if sum(map(abs, delta)) > 1:
                        raise ValueError("Recorded movement exceeds one nearest-neighbor link per tick")
                    unwrapped = tuple(a + b for a, b in zip(history[-1]["x"], delta, strict=True))
                history.append(
                    {
                        "tick": frame["tick"],
                        "position": position,
                        "x": unwrapped,
                        "mass": mass,
                        "p": momentum,
                    }
                )
        if (
            not seen
            or seen != output.keys()
            or any(len(h) != frame["tick"] + 1 for h in output.values())
        ):
            raise NotTestable(
                "Body creation, loss or identity replacement needs a different acceptance case"
            )
    for history in output.values():
        if any(row["mass"] != history[0]["mass"] for row in history):
            raise NotTestable("This first Newton adapter requires constant body masses")
    return output


def inertia(history: list[dict], window: int) -> dict:
    formula = "x(t) = x(0) + v(0)t; p(t) = p(0) when net force is zero"
    if window < 1 or len(history) <= 3 * window:
        raise NotTestable("Inertia needs a calibration window and at least two held-out windows")
    origin = history[0]
    velocity = tuple(x / window for x in sub(history[window]["x"], origin["x"]))
    if velocity == ZERO and origin["p"] != ZERO:
        raise NotTestable("Nonzero momentum but unresolved displacement; use a longer observation")
    if sum(map(abs, velocity)) > Fraction(1, 10):
        raise NotTestable("This acceptance case is restricted to speeds at most one tenth link/tick")
    error = max(
        norm_max(
            sub(row["x"], tuple(x + v * row["tick"] for x, v in zip(origin["x"], velocity, strict=True)))
        )
        for row in history
    )
    momentum_error = max(norm_max(sub(row["p"], origin["p"])) for row in history)
    tolerance = Fraction(0) if velocity == ZERO else Fraction(1)
    verdict = measured_check(
        formula,
        error,
        tolerance,
        calibration_window_ticks=window,
        measured_velocity=list(map(str, velocity)),
        held_out_ticks=len(history) - 1 - window,
        momentum_error=str(momentum_error),
        position_resolution="one lattice link",
    )
    if momentum_error:
        verdict["status"] = "fail"
    return verdict


def momentum_velocity(body_tracks: dict[str, list[dict]], window: int) -> dict:
    rows = []
    for name, history in body_tracks.items():
        for start in range(0, len(history) - window, window):
            block = history[start : start + window + 1]
            if any(row["p"] != block[0]["p"] for row in block):
                continue  # Impulse windows are not constant-velocity measurements.
            velocity = tuple(value / window for value in sub(block[-1]["x"], block[0]["x"]))
            error = norm_max(sub(block[0]["p"], tuple(block[0]["mass"] * v for v in velocity)))
            tolerance = block[0]["mass"] / window
            rows.append(
                {
                    "body": name,
                    "start_tick": start,
                    "end_tick": start + window,
                    "measured_velocity": list(map(str, velocity)),
                    "error": str(error),
                    "tolerance": str(tolerance),
                    "pass": error <= tolerance,
                }
            )
    if not rows:
        raise NotTestable("No constant-momentum position window is available")
    return result(
        "pass" if all(row["pass"] for row in rows) else "fail",
        "p = m * dx/dt",
        windows=rows,
        scope="Finite-window consistency, not an independently derived mass law",
    )


def contact(body_tracks: dict[str, list[dict]]) -> dict[str, dict]:
    if len(body_tracks) != 2:
        raise NotTestable("A closed two-body direct-contact output is required")
    left, right = body_tracks.values()
    total = tuple(a + b for a, b in zip(left[0]["p"], right[0]["p"], strict=True))
    p_error = Fraction(0)
    energy0 = sum(dot(h[0]["p"], h[0]["p"]) / (2 * h[0]["mass"]) for h in (left, right))
    e_error = Fraction(0)
    impulses = []
    for index, (a, b) in enumerate(zip(left, right, strict=True)):
        p_error = max(
            p_error, norm_max(sub(tuple(x + y for x, y in zip(a["p"], b["p"], strict=True)), total))
        )
        energy = sum(dot(row["p"], row["p"]) / (2 * row["mass"]) for row in (a, b))
        e_error = max(e_error, abs(energy - energy0))
        if index:
            da, db = sub(a["p"], left[index - 1]["p"]), sub(b["p"], right[index - 1]["p"])
            if da != ZERO or db != ZERO:
                impulses.append(
                    {
                        "observed_interval": [index - 1, index],
                        "left": list(map(str, da)),
                        "right": list(map(str, db)),
                        "opposite": da == tuple(-v for v in db),
                        "co_located_before": left[index - 1]["position"] == right[index - 1]["position"],
                    }
                )
    third = result(
        "not_testable", "Delta p_A = -Delta p_B", reason="No nonzero contact impulse was observed"
    )
    if impulses:
        third = result(
            "pass" if all(row["opposite"] and row["co_located_before"] for row in impulses) else "fail",
            "Delta p_A = -Delta p_B",
            impulses=impulses,
            scope="Integrated third law for direct contact, without field momentum",
        )
    return {
        "linear_momentum": measured_check(
            "sum(p) = constant", p_error, Fraction(0), initial_total=list(map(str, total))
        ),
        "elastic_energy": measured_check(
            "sum(p^2 / (2m)) = constant for elastic contact",
            e_error,
            Fraction(0),
            initial_energy=str(energy0),
        ),
        "newton_third": third,
    }


def provenance(document: dict, kind: str, source: str) -> None:
    if document.get("measurement_kind") != kind or document.get("source_sha256") != source:
        raise ValueError("Independent measurement kind/source fingerprint mismatch")
    proof = document.get("provenance", {})
    if (
        proof.get("derived_from_target_kinematics") is not False
        or not proof.get("method")
        or not proof.get("calibration")
    ):
        raise NotTestable("An independently calibrated measurement with explicit provenance is required")


def second_law(history: list[dict], measurement: dict, source: str, window: int) -> dict:
    provenance(measurement, "independent_net_force", source)
    samples = measurement.get("samples", [])
    if [row.get("tick") for row in samples] != [row["tick"] for row in history]:
        raise NotTestable("Force measurements must cover every matching physical tick")
    forces = [vector(row["force"]) for row in samples]
    if not forces or forces[0] == ZERO or any(f != forces[0] for f in forces):
        raise NotTestable(
            "The first force-response check requires a measured nonzero constant net force"
        )
    if window < 1 or len(history) <= 3 * window:
        raise NotTestable("Insufficient measured force/position duration")
    if any(row["mass"] != history[0]["mass"] for row in history):
        raise NotTestable("F = ma in this check requires constant mass")
    error = Fraction(0)
    for center in range(window, len(history) - window, window):
        left, middle, right = (history[i]["x"] for i in (center - window, center, center + window))
        velocity = tuple((b - a) / window for a, b in zip(middle, right, strict=True))
        if sum(map(abs, velocity)) > Fraction(1, 10):
            raise NotTestable("Force-response velocities exceed the declared low-speed regime")
        acceleration = tuple(
            (after - 2 * current + before) / (window * window)
            for before, current, after in zip(left, middle, right, strict=True)
        )
        error = max(
            error,
            norm_max(sub(forces[center], tuple(history[center]["mass"] * a for a in acceleration))),
        )
    # Three cell-position errors have coefficients 1, -2, 1.
    tolerance = 4 * history[0]["mass"] / (window * window)
    if norm_max(forces[0]) <= tolerance:
        raise NotTestable("Force response is below the declared lattice measurement resolution")
    return measured_check(
        "F_independently_measured = m * d^2x/dt^2",
        error,
        tolerance,
        scope="Conditional on independently reviewed calibration; no force is inferred from target acceleration",
    )


def gravity(measurement: dict, source: str) -> dict:
    provenance(measurement, "gravitational_force_sweep", source)
    rows = measurement.get("samples", [])
    if len(rows) < 3:
        raise NotTestable("Gravity needs one calibration and at least two held-out separations")
    constants = []
    separations = set()
    masses = set()
    for row in rows:
        r, force = vector(row["separation"]), vector(row["force"])
        radius2, magnitude2 = dot(r, r), dot(force, force)
        m1, m2 = rational(row["source_mass"]), rational(row["test_mass"])
        if radius2 <= 0 or m1 <= 0 or m2 <= 0:
            raise ValueError("Gravity samples require positive masses and nonzero separation")
        if not magnitude2 or dot(r, force) >= 0 or dot(r, force) ** 2 != radius2 * magnitude2:
            return result(
                "fail", "F = -G m1 m2 r / |r|^3", reason="Force must be nonzero, radial and attractive"
            )
        separations.add(radius2)
        masses.add((m1, m2))
        constants.append(magnitude2 * radius2 * radius2 / (m1 * m2) ** 2)
    if len(masses) != 1:
        raise NotTestable("The first inverse-square sweep requires fixed masses to avoid confounding")
    if len(separations) < 3:
        raise NotTestable("Three distinct separations are needed to check inverse-square falloff")
    baseline = constants[0]
    error = max(abs(value / baseline - 1) for value in constants[1:])
    return measured_check(
        "|F| = G m1 m2 / r^2; G calibrated once, then held fixed",
        error,
        Fraction(1, 100),
        comparison="relative residual of squared force normalization",
        calibration_g_squared=str(baseline),
        held_out_samples=len(rows) - 1,
        mass_scaling_tested=False,
        scope="Inverse-square radial-force test only; mass sweeps and physical G calibration are additional requirements",
    )


def safely(function, *args) -> dict:
    try:
        return function(*args)
    except NotTestable as exc:
        return result("not_testable", function.__name__, reason=str(exc))


def audit(
    folder: Path,
    mode: str,
    window: int,
    force_path: Path | None = None,
    gravity_path: Path | None = None,
) -> dict:
    if type(window) is not int or window <= 0:
        raise ValueError("Measurement window must be a positive integer")
    meta, initial, frames, hashes = load_run(folder)
    body_tracks = tracks(initial, frames)
    checks: dict[str, dict] = {}
    if mode == "inertia":
        if len(body_tracks) != 1 or any(
            initial.get(k)
            for k in ("interactions", "couplings", "spatial_couplings", "spatial_interactions")
        ):
            raise NotTestable(
                "Inertia acceptance requires one isolated body and no configured interaction"
            )
        checks["newton_first"] = safely(inertia, next(iter(body_tracks.values())), window)
    elif mode == "contact":
        if any(initial.get(k) for k in ("couplings", "spatial_couplings", "spatial_interactions")):
            raise NotTestable("Contact acceptance must have no external or field coupling")
        if any(
            any(values)
            for key in ("source_totals", "escaped_totals", "dissipation_totals")
            for values in meta.get(key, {}).values()
        ):
            raise NotTestable("Contact acceptance requires a closed, source-free recorded system")
        checks.update(contact(body_tracks))
    elif mode != "force-response":
        raise ValueError("Unknown acceptance case")
    checks["momentum_velocity"] = safely(momentum_velocity, body_tracks, window)
    checks["newton_second"] = result(
        "not_testable",
        "F = ma",
        reason="No independent force measurement was supplied; F = dp/dt would be circular here",
    )
    if force_path is not None:
        document = decode(force_path.read_text(encoding="utf-8"))
        target = document.get("target_type")
        if target not in body_tracks:
            raise ValueError("Independent force target is absent from saved output")
        checks["newton_second"] = safely(
            second_law, body_tracks[target], document, meta["source_sha256"], window
        )
        hashes["independent_force_measurement"] = hashlib.sha256(force_path.read_bytes()).hexdigest()
    checks["newton_gravity"] = result(
        "not_testable",
        "F = G m1 m2 / r^2",
        reason="No measured gravitational force/separation sweep was supplied",
    )
    if gravity_path is not None:
        checks["newton_gravity"] = safely(
            gravity, decode(gravity_path.read_text(encoding="utf-8")), meta["source_sha256"]
        )
        hashes["gravity_measurement"] = hashlib.sha256(gravity_path.read_bytes()).hexdigest()
    statuses = {value["status"] for value in checks.values()}
    status = "fail" if "fail" in statuses else "partial" if "not_testable" in statuses else "pass"
    return {
        "status": status,
        "mode": mode,
        "window_ticks": window,
        "source_sha256": meta["source_sha256"],
        "model_id": meta["model"],
        "completed_ticks": meta["completed_ticks"],
        "input_hashes": hashes,
        "scope": "Output agreement only. The checker does not certify that the runtime or configuration did not already impose the target law.",
        "formula_location": "External read-only checker; not the engine or runtime initialization",
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_directory", type=Path)
    parser.add_argument("--case", choices=("inertia", "contact", "force-response"), required=True)
    parser.add_argument("--window", type=int, required=True)
    parser.add_argument("--force-measurements", type=Path)
    parser.add_argument("--gravity-measurements", type=Path)
    args = parser.parse_args()
    try:
        report = audit(
            args.run_directory,
            args.case,
            args.window,
            args.force_measurements,
            args.gravity_measurements,
        )
    except NotTestable as exc:
        report = {"status": "not_testable", "reason": str(exc)}
    except (ValueError, KeyError, TypeError, OSError, ZeroDivisionError) as exc:
        report = {"status": "invalid_output", "reason": str(exc)}
    print(json.dumps(report, indent=2))
    raise SystemExit(
        {"pass": 0, "fail": 1, "invalid_output": 2, "partial": 3, "not_testable": 3}[report["status"]]
    )


if __name__ == "__main__":
    main()
