"""Independent, read-only acceptance of recorded nucleus/electron pilot evidence.

Authority: PROTON_NEUTRON_ELECTRON_CANDIDATE.md and
LOCAL_NUCLEUS_ELECTRON_ARCHITECTURE.md at published a0b037dea3e80ffcc399c8fab568b248bac3a446.
Floating-point arithmetic below is diagnostic only. No engine or renderer is imported.
The contact-gap model is a comparison, not the user's later same-coupling trapped-ray target.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from collections.abc import Iterable
from fractions import Fraction
from pathlib import Path
from typing import Any

MODEL = "contact-bound-ray-electron-pilot-v1"
NUCLEON_MASS = 940032
GAP = 669889164
PORTS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


class EvidenceError(ValueError):
    """Required recorded evidence is missing or cannot support the requested claim."""


def result(passed: bool, **details: Any) -> dict[str, Any]:
    return {"status": "pass" if passed else "fail", **details}


def owners(state: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    """Read each actual carrier owner once; an in-flight owner stays at its origin."""
    rows = []
    for node in state["nodes"]:
        for bank in ("disturbances", "held_outputs"):
            for record in node.get(bank, []):
                if record["type"] == kind:
                    rows.append({**record, "position": node["position"], "owner": bank})
    for record in state.get("transfers", []):
        if record["type"] == kind:
            rows.append({**record, "position": record["origin"], "owner": "link"})
    return rows


def one_owner(state: dict[str, Any], kind: str) -> dict[str, Any]:
    rows = owners(state, kind)
    if len(rows) != 1:
        raise EvidenceError(f"tick {state['tick']}: expected one {kind} owner, found {len(rows)}")
    return rows[0]


def trace_checks(
    states: list[dict[str, Any]], run: dict[str, Any], initialization_bytes: bytes
) -> dict[str, Any]:
    expected_ticks = list(range(run["completed_ticks"] + 1))
    sidecar = run.get("state_trace", {})
    sidecar_valid = (
        sidecar.get("path") == "states.jsonl"
        and sidecar.get("content") in ("all", "carriers")
        and sidecar.get("stride") == 1
        and sidecar.get("rows") == len(states)
        and all(
            sidecar.get(key) == run[key]
            for key in ("source_sha256", "initialization_sha256", "requested_ticks", "completed_ticks")
        )
    )
    return result(
        run["status"] == "completed"
        and run["completed_ticks"] == run["requested_ticks"]
        and [state["tick"] for state in states] == expected_ticks
        and run["initialization_sha256"] == hashlib.sha256(initialization_bytes).hexdigest()
        and isinstance(run.get("source_sha256"), str)
        and len(run["source_sha256"]) == 64
        and sidecar_valid,
        source_sha256=run.get("source_sha256"),
        samples=len(states),
        completed_ticks=run["completed_ticks"],
        expected_samples=len(expected_ticks),
    )


def event_checks(events: Iterable[dict[str, Any]], *, link_ticks: int = 1) -> dict[str, Any]:
    """Stream large causal logs; retain bounded failures and small carrier-cycle evidence."""
    sent = 0
    failures = []
    draw_events = 0
    cycles = []
    material_sent = []
    delayed_cycles = []
    escaped_radiation: Counter[int] = Counter()
    for event in events:
        name = event["event"]
        if name in {"sent", "spatial_sent"}:
            sent += 1
            valid = event["arrival_tick"] == event["tick"] + link_ticks
            valid = valid and type(event["port"]) is int and 0 <= event["port"] < 6
            if not valid and len(failures) < 10:
                failures.append(event)
        if name == "sent":
            material_sent.append(event)
        if name == "cycle_committed":
            cycles.append(event)
        if name == "cycle_started" and event["ready_tick"] != event["tick"]:
            delayed_cycles.append(event["tick"])
        if any(word in name.lower() for word in ("sample", "lottery", "draw", "ticket")):
            draw_events += 1
        if name == "spatial_escaped":
            escaped_radiation[event["tick"]] += event["escaped"].get("radiation", [0])[0]
    return {
        "transit": (
            result(not failures, sent=sent, failures=failures)
            if sent
            else {"status": "not_exercised", "sent": 0, "failures": []}
        ),
        "observed_draw_events": draw_events,
        "carrier_cycles": cycles,
        "zero_extra_wait": result(bool(cycles) and not delayed_cycles, delayed_cycles=delayed_cycles),
        "material_sent": material_sent,
        "escaped_radiation_by_tick": dict(escaped_radiation),
    }


def no_sampling(initialization: dict[str, Any], observed_draw_events: int) -> dict[str, Any]:
    """Verify the deterministic profile's admission, not a universal event-name detector."""
    forbidden = bool(initialization.get("event_program"))
    for field in initialization.get("spatial_fields", []):
        forbidden |= "bond" in field or field.get("kerengonen", {}).get("capture") == "lottery"
    return result(
        not forbidden and observed_draw_events == 0,
        observed_draw_events=observed_draw_events,
        forbidden_sampler_configured=forbidden,
        scope="No configured native instrument, bond or lottery and no draw event in this profile.",
    )


def _quadrant(x: int, y: int) -> int:
    if x > 0 and y >= 0:
        return 0
    if y > 0 and x <= 0:
        return 1
    if x < 0 and y <= 0:
        return 2
    if y < 0 and x >= 0:
        return 3
    raise EvidenceError("A zero projected radius has no oriented section")


def circulation(
    states: list[dict[str, Any]],
    *,
    electron: str = "electron",
    nucleons: tuple[str, str] = ("proton", "neutron"),
    launch_tick: int = 64,
    active_ticks: int = 768,
    plane: tuple[int, int] = (0, 1),
) -> dict[str, Any]:
    """Score E2 only. Launch is t0; three full windings supply three intervals."""
    selected = [s for s in states if launch_tick <= s["tick"] <= launch_tick + active_ticks]
    if [s["tick"] for s in selected] != list(range(launch_tick, launch_tick + active_ticks + 1)):
        return {"status": "incomplete", "reason": "A complete launch-to-horizon state trace is required"}
    radii_squared = []
    crossings = []
    crossing_states = []
    quarters = 0
    last_quadrant = None
    center_coincident = True
    initial_values = None
    try:
        for state in selected:
            material = one_owner(state, electron)
            left, right = (one_owner(state, name) for name in nucleons)
            center_coincident &= left["position"] == right["position"]
            # Twice the physical center-relative coordinate supports a movable two-owner center.
            relative = [
                2 * material["position"][i] - left["position"][i] - right["position"][i]
                for i in range(3)
            ]
            radii_squared.append(sum(v * v for v in relative))
            quadrant = _quadrant(relative[plane[0]], relative[plane[1]])
            if last_quadrant is None:
                if quadrant != 0 or relative[plane[1]] != 0:
                    raise EvidenceError("Launch must be on the positive section of the declared plane")
                initial_values = material["values"]
            else:
                change = (quadrant - last_quadrant) % 4
                if change == 2:
                    raise EvidenceError("A skipped half-plane prevents an unambiguous winding count")
                quarters += -1 if change == 3 else change
                if quadrant == 0 and last_quadrant == 3 and quarters >= 4 * (len(crossings) + 1):
                    crossings.append(state["tick"] - launch_tick)
                    crossing_states.append(
                        {
                            "tick": state["tick"],
                            "momentum": material["values"]["momentum"],
                            "motion_remainder": material["values"]["motion_remainder"],
                            "matches_launch_momentum_and_remainder": all(
                                material["values"][key] == initial_values[key]
                                for key in ("momentum", "motion_remainder")
                            ),
                        }
                    )
            last_quadrant = quadrant
    except (EvidenceError, KeyError) as error:
        return result(False, reason=str(error))
    endpoints = [0, *crossings[:3]]
    periods = [b - a for a, b in zip(endpoints[:-1], endpoints[1:], strict=True)]
    reference = 64 * math.pi
    period_band = len(periods) == 3 and all(0.75 * reference <= t <= 1.25 * reference for t in periods)
    mean = sum(periods) / len(periods) if periods else None
    period_spread = len(periods) == 3 and max(periods) - min(periods) <= 0.2 * mean
    localized = all(4 * 4**2 <= r2 <= 4 * 12**2 for r2 in radii_squared)
    return result(
        center_coincident and localized and period_band and period_spread,
        localized=localized,
        nucleus_coincident=center_coincident,
        min_radius_squared=min(radii_squared) / 4,
        max_radius_squared=max(radii_squared) / 4,
        completed_positive_windings=len(crossings),
        world_tick_periods=periods,
        reference_world_tick_period=reference,
        period_band_passed=period_band,
        period_spread_passed=period_spread,
        measured_recurrence_per_world_tick=None if not periods else 1 / mean,
        crossing_states=crossing_states,
        quantum_phase_frequency="unavailable: this pilot has no coherent phase law",
        scope="Finite classical kinematic target only; field acceptance and full-state recurrence are separate.",
    )


def displacement(
    rows: Iterable[dict[str, Any]], *, denominator: int, initial_remainder: tuple[int, ...] = (0, 0, 0)
) -> dict[str, Any]:
    """Audit observed active-cycle records; never evolve or repair a carrier."""
    total = list(initial_remainder)
    hops = [0, 0, 0]
    failures = []
    count = 0
    for row in rows:
        count += 1
        momentum, remainder, hop = row["momentum"], row["remainder"], row["dispatched_hop"]
        valid = sum(abs(v) for v in momentum) <= denominator
        valid &= sum(abs(v) for v in hop) in (0, 1)
        valid &= sum(abs(v) for v in remainder) < 3 * denominator
        valid &= all(abs(v) < 2 * denominator for v in remainder)
        for axis in range(3):
            total[axis] += momentum[axis]
            hops[axis] += hop[axis]
            valid &= denominator * hops[axis] + remainder[axis] == total[axis]
        if not valid:
            failures.append(row["tick"])
    return result(count > 0 and not failures, active_cycles=count, failed_ticks=failures)


def field_cycle(means: dict[tuple[int, int, int], tuple[float, float, float]]) -> dict[str, Any]:
    """Score fixed F8 calibration and independently specified angular/radial probes."""
    required = [
        *(tuple(8 * d for d in port) for port in PORTS),
        (6, 6, 0),
        (4, 4, 4),
        (4, 0, 0),
        (16, 0, 0),
    ]
    if any(point not in means for point in required):
        return {
            "status": "incomplete",
            "reason": "All preregistered complete-cycle mean probes are required",
        }
    f8 = means[(8, 0, 0)][0]
    if f8 <= 0:
        return result(False, reason="Calibration requires a positive outward F8", f8=f8)
    probes = []
    for point in required:
        vector = means[point]
        radius_squared = sum(v * v for v in point)
        radius = math.sqrt(radius_squared)
        radial = sum(a * b for a, b in zip(vector, point, strict=True)) / radius
        tangent_squared = max(0.0, sum(v * v for v in vector) - radial * radial)
        expected = f8 * 64 / radius_squared
        magnitude_error = abs(radial - expected) / expected
        tangent_fraction = math.sqrt(tangent_squared) / abs(radial) if radial else math.inf
        limit = 0.05 if radius_squared == 64 else 0.25
        probes.append(
            {
                "point": point,
                "radial": radial,
                "reference": expected,
                "relative_radial_error": magnitude_error,
                "tangential_fraction": tangent_fraction,
                "passed": radial > 0 and magnitude_error <= limit and tangent_fraction <= 0.25,
            }
        )
    return result(all(p["passed"] for p in probes), f8=f8, coefficient=64 / f8, probes=probes)


def field_cycle_samples(
    samples: dict[tuple[int, int, int], list[dict[str, Any]]], *, period: int = 10
) -> dict[str, Any]:
    """Average one complete recorded source cycle, preserving its exact calibration ratio."""
    means = {}
    for point, rows in samples.items():
        ticks = [row["tick"] for row in rows]
        if len(rows) != period or ticks != list(range(ticks[0], ticks[0] + period)):
            return {"status": "incomplete", "reason": "A complete consecutive source cycle is required"}
        means[point] = tuple(Fraction(sum(row["flux"][i] for row in rows), period) for i in range(3))
    scored = field_cycle({point: tuple(float(v) for v in vector) for point, vector in means.items()})
    if (8, 0, 0) in means:
        f8 = means[(8, 0, 0)][0]
        scored["f8_exact"] = [f8.numerator, f8.denominator]
        if f8 > 0:
            coefficient = 64 / f8
            scored["coefficient_exact"] = [coefficient.numerator, coefficient.denominator]
    return scored


def nuclear_control(
    states: list[dict[str, Any]],
    case: str,
    *,
    nucleons: tuple[str, str] = ("proton", "neutron"),
    initialization: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Check N0-N3 from actual carrier owners and complete canonical inventory aggregates."""
    energies = []
    momenta = []
    pairs = []
    seen_outgoing = False
    lifecycle_valid = True
    properties_retained = True
    initial_properties = None
    try:
        for state in states:
            pair = [one_owner(state, name) for name in nucleons]
            values = [record["values"] for record in pair]
            properties = [[v[field] for field in ("mass", "charge", "baryon", "gap")] for v in values]
            if initial_properties is None:
                initial_properties = properties
            properties_retained &= properties == initial_properties
            sectors = [v["sector"][0] for v in values]
            if seen_outgoing:
                lifecycle_valid &= sectors == [2, 2]
            seen_outgoing |= 2 in sectors
            accounting = state["accounting"]
            nuclear_energy = 0
            for v in values:
                mass = v["mass"][0]
                numerator = sum(p * p for p in v["momentum"])
                if mass != NUCLEON_MASS or numerator % (2 * mass):
                    raise EvidenceError("The fixed nuclear kinetic code is not exactly represented")
                nuclear_energy += (
                    numerator // (2 * mass)
                    + v["radiation"][0]
                    + v["excitation"][0]
                    - v["gap"][0] * v["bound"][0]
                )
            radiation = accounting["spatial_accounting"].get("radiation")
            if radiation is None:
                absent_by_definition = initialization is not None and not any(
                    field["field"] == "radiation" for field in initialization.get("spatial_fields", [])
                )
                if not absent_by_definition:
                    raise EvidenceError(
                        "Spatial radiation inventory is unavailable; do not substitute zero"
                    )
            else:
                nuclear_energy += sum(
                    radiation[bank][0] for bank in ("current", "escaped", "dissipated")
                )
            energies.append(nuclear_energy)
            momenta.append(
                [
                    sum(
                        accounting[bank]["momentum"][i]
                        for bank in ("totals", "escaped_totals", "dissipation_totals")
                    )
                    for i in range(3)
                ]
            )
            pairs.append(pair)
    except (EvidenceError, KeyError) as error:
        return {"status": "incomplete", "reason": str(error)}
    if not pairs:
        return {"status": "incomplete", "reason": "No nuclear states"}
    conserved = len(set(energies)) == 1 and all(p == momenta[0] for p in momenta)
    first_bound = next((pair for pair in pairs if all(r["values"]["bound"] == [1] for r in pair)), None)
    final_values = [r["values"] for r in pairs[-1]]
    separated = pairs[-1][0]["position"] != pairs[-1][1]["position"]
    checks: dict[str, bool] = {}
    if case in ("nuclear_capture", "nuclear_boost"):
        expected_p = [0, 0, 0] if case == "nuclear_capture" else [NUCLEON_MASS, 0, 0]
        checks["capture"] = first_bound is not None and all(
            r["values"]["momentum"] == expected_p and r["values"]["radiation"] == [335414598]
            for r in first_bound
        )
        checks["initial_energy"] = energies[0] == (
            NUCLEON_MASS if case == "nuclear_capture" else 2 * NUCLEON_MASS
        )
        checks["retained_pair"] = all(pair[0]["position"] == pair[1]["position"] for pair in pairs)
        if case == "nuclear_boost":
            checks["translated"] = pairs[-1][0]["position"] != pairs[0][0]["position"]
    elif case == "nuclear_disabled":
        checks["separated"] = separated
        checks["never_bound"] = all(r["values"]["bound"] == [0] for pair in pairs for r in pair)
        checks["no_capture_radiation"] = all(
            state["accounting"]["spatial_accounting"].get("radiation", {}).get(bank, [0]) == [0]
            for state in states
            for bank in ("current", "escaped", "dissipated")
        )
        checks["no_retained_radiation"] = all(
            r["values"]["radiation"] == [0] for pair in pairs for r in pair
        )
    elif case == "nuclear_subthreshold":
        checks["valid_odd_deficit"] = [r["values"]["excitation"][0] for r in pairs[0]] == [
            GAP // 2 - 1,
            GAP // 2,
        ]
        checks["no_change"] = all(
            [r["values"] for r in pair] == [r["values"] for r in pairs[0]] for pair in pairs
        )
    elif case in ("nuclear_threshold_zero_kick", "nuclear_dissociation"):
        checks["outgoing"] = all(v["sector"] == [2] and v["bound"] == [0] for v in final_values)
        q = 0 if case == "nuclear_threshold_zero_kick" else NUCLEON_MASS
        checks["paid_relative_kick"] = [v["momentum"] for v in final_values] == [[q, 0, 0], [-q, 0, 0]]
        checks["excitation_debited"] = all(v["excitation"] == [0] for v in final_values)
        if q:
            checks["separated"] = separated
    else:
        raise EvidenceError(f"Unknown preregistered nuclear control: {case}")
    return result(
        conserved and lifecycle_valid and properties_retained and all(checks.values()),
        case=case,
        scope="Contact-gap comparison only; this does not test same-coupling trapped-ray binding.",
        initial_energy=energies[0],
        final_energy=energies[-1],
        energy_and_momentum_conserved=conserved,
        constituent_properties_retained=properties_retained,
        no_recapture_after_outgoing=lifecycle_valid,
        checks=checks,
    )


def score_run(directory: Path, *, electron: str = "electron") -> dict[str, Any]:
    """Read canonical metadata/events plus complete raw carrier states exported by the run owner."""
    run = json.loads((directory / "run.json").read_text())
    source = (directory / "initialization.json").read_bytes()
    initialization = json.loads(source)
    states_path = directory / "states.jsonl"
    if not states_path.exists():
        raise EvidenceError(
            "Missing complete raw states.jsonl; rendered output is not acceptance evidence"
        )
    states = [json.loads(line) for line in states_path.read_text().splitlines()]
    with (directory / "events.jsonl").open() as stream:
        events = event_checks((json.loads(line) for line in stream), link_ticks=run["link_ticks"])
    final = json.loads((directory / "state.json").read_text())
    final_agrees = bool(states) and all(
        states[-1].get(key) == final.get(key)
        for key in ("tick", "nodes", "transfers", "boundary", "escaped_totals")
    )
    return {
        "model": run["model"],
        "scope": "Earlier contact-gap pilot comparison; not the same-coupling trapped-ray target.",
        "model_identity": result(run["model"] == MODEL and initialization["model_id"] == MODEL),
        "trace": trace_checks(states, run, source),
        "final_state_agrees": result(final_agrees),
        "transit": events["transit"],
        "zero_extra_wait": events["zero_extra_wait"],
        "no_draws": no_sampling(initialization, events["observed_draw_events"]),
        "circulation": circulation(states, electron=electron),
        "field_acceptance": {"status": "incomplete", "reason": "Supply independent source-cycle probes"},
        "nuclear_acceptance": {"status": "incomplete", "reason": "Supply N0-N4 control evidence"},
        "physical_atomic_frequency": "unavailable",
    }
