"""Read-only timing and ownership checks against predeclared fixture results."""

from __future__ import annotations

from configuration import DIRECTIONS, RECEIVER, SOURCE, expectations


def at(event: dict, position: tuple[int, int, int]) -> bool:
    return tuple(event.get("position", ())) == position


def selected(events: list[dict], name: str, position: tuple[int, int, int]) -> list[dict]:
    return [event for event in events if event.get("event") == name and at(event, position)]


def source_states(frames: list[dict]) -> list[dict]:
    states = []
    for frame in frames:
        for node in frame["nodes"]:
            if tuple(node["position"]) != SOURCE:
                continue
            for record in node["disturbances"]:
                if record["type"] == "held_source":
                    states.append({"tick": frame["tick"], **record["values"]})
    return states


def clock_at(frames: list[dict], position: tuple[int, int, int], sample_tick: int) -> dict | None:
    for frame in frames:
        for node in frame.get("spatial_fields", []):
            clock = node.get("output_clock", {})
            if tuple(node["position"]) == position and clock.get("sample_tick") == sample_tick:
                return clock
    return None


def assess(case: dict, name: str) -> dict:
    """Return explicit failed assertions without changing or rerunning a world."""
    expected = expectations()["cases"][name]
    events, frames, metadata = case["events"], case["frames"], case["metadata"]
    checks: dict[str, bool] = {
        "run_completed": metadata["status"] == "completed" and case["error"] is None,
        "requested_duration_completed": metadata["completed_ticks"] == metadata["requested_ticks"],
        "declared_token_accounting": metadata["accounting_balanced_at_every_completed_tick"],
        "source_identity": metadata["source_sha256"] == case["source_sha256"],
        "input_identity": metadata["initialization_sha256"] == case["initialization_sha256"],
    }
    sent = [event for event in events if event.get("event") in {"sent", "spatial_sent"}]
    checks["fixed_link_transit"] = all(event["arrival_tick"] - event["tick"] == 1 for event in sent)
    states = source_states(frames)
    checks["source_retained"] = len(states) == len(frames)
    checks["source_mass_unchanged"] = all(state["mass"] == [expected["mass"]] for state in states)
    reserve = states[-1]["computation"][0] if states else None
    departures = [event["tick"] for event in selected(events, "spatial_sent", SOURCE)]
    arrivals = [
        [event["tick"] for event in selected(events, "spatial_received", (SOURCE[0] + hop, *SOURCE[1:]))]
        for hop in (1, 2)
    ]
    observations = {
        "source_departures": departures,
        "first_two_arrivals": [values[0] for values in arrivals if values],
        "final_reserve": reserve,
        "host_elapsed_seconds": metadata["elapsed_seconds"],
        "visualization": case["visualization"],
    }
    if "source_departures" in expected:
        checks["source_departure_ticks"] = departures == expected["source_departures"]
    if "first_two_arrivals" in expected:
        checks["causal_arrival_ticks"] = (
            observations["first_two_arrivals"] == expected["first_two_arrivals"]
        )
    if "emitted_tokens" in expected:
        checks["exact_funded_source_debit"] = reserve == expected["reserve"] - expected["emitted_tokens"]
    source_clock = clock_at(frames, SOURCE, 0)
    checks["source_uses_actual_local_emission"] = (
        source_clock is not None and source_clock["sample"] == expected["mass"]
    )
    if expected["mass"] > 0 and arrivals[0]:
        receiver_clock = clock_at(frames, RECEIVER, arrivals[0][0])
        checks["equal_local_field_same_response"] = (
            receiver_clock is not None
            and source_clock is not None
            and receiver_clock["sample"] == source_clock["sample"]
            and receiver_clock["delays"] == source_clock["delays"]
        )
        before_arrival = [
            node.get("output_clock", {})
            for frame in frames
            if frame["tick"] < arrivals[0][0]
            for node in frame.get("spatial_fields", [])
            if tuple(node["position"]) == RECEIVER
        ]
        checks["no_remote_clock_effect_before_arrival"] = all(
            clock.get("sample", 0) == 0 for clock in before_arrival
        )
    if expected["mass"] * expected["coupling"] > 1:
        next_clock = clock_at(frames, SOURCE, 1)
        checks["held_packet_not_resampled"] = next_clock is not None and next_clock["sample"] == 0
    if name in {"C1", "C2"}:
        received = [
            event for event in selected(events, "received", RECEIVER) if event["disturbance"] == "probe"
        ]
        emitted = [
            event for event in selected(events, "sent", RECEIVER) if event["disturbance"] == "probe"
        ]
        target = (RECEIVER[0], RECEIVER[1] - 1, RECEIVER[2])
        delivered = [
            event for event in selected(events, "received", target) if event["disturbance"] == "probe"
        ]
        checks["probe_input_not_delayed"] = [event["tick"] for event in received] == [
            expected["probe_ready_tick"]
        ]
        checks["probe_output_departure"] = [event["tick"] for event in emitted] == [
            expected["probe_departure_tick"]
        ]
        checks["probe_adjacent_arrival"] = [event["tick"] for event in delivered] == [
            expected["probe_arrival_tick"]
        ]
        observations["probe_departure_ticks"] = [event["tick"] for event in emitted]
    if name in {"P6", "P2"}:
        ports = range(6) if name == "P6" else (2, 3)
        emitted = [
            event for event in selected(events, "sent", SOURCE) if event["disturbance"] == "probe"
        ]
        by_port = {event["port"]: event for event in emitted}
        observed_departures = [by_port[port]["tick"] for port in ports if port in by_port]
        observed_arrivals = []
        for port in ports:
            target = tuple(value + delta for value, delta in zip(SOURCE, DIRECTIONS[port], strict=True))
            observed_arrivals.extend(
                event["tick"]
                for event in selected(events, "received", target)
                if event["disturbance"] == "probe" and event["port"] == port ^ 1
            )
        checks["independent_face_departures"] = observed_departures == expected["probe_departure_ticks"]
        checks["independent_face_arrivals"] = observed_arrivals == expected["probe_arrival_ticks"]
        observations["probe_departure_ticks"] = observed_departures
        observations["probe_arrival_ticks"] = observed_arrivals
        if name == "P2":
            incoming = [
                event["tick"]
                for event in selected(events, "received", SOURCE)
                if event["disturbance"] == "probe"
            ]
            checks["input_received_while_other_face_held"] = incoming == [1]
    if name == "L1":
        changes = [
            (current["tick"] - 1, current["computation"][0])
            for previous, current in zip(states, states[1:], strict=False)
            if previous["computation"] != current["computation"]
        ]
        checks["held_source_emission_ticks"] = [tick for tick, _ in changes] == expected[
            "emission_ticks"
        ]
        checks["held_source_reserve_steps"] = [value for _, value in changes] == expected[
            "reserves_after_emission"
        ]
        observations["reserve_changes"] = changes
    return {"name": name, "passed": all(checks.values()), "checks": checks, "observed": observations}
