"""Retained dual-rail records on the shared conservative collision tensor.

This is a passive audit, never an evolution callback.  A record is a particle
in the declared two record rails, not a count inferred from arithmetic clicks.
The shared native module owns the tensor and complete prepared-state map.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
from pathlib import Path

import numpy as np

from universe24.system.bundle import pad_tensor
from universe24.core import State, Tensor, exact_json
from universe24.core.lattice import DIRECTIONS, lattice
from universe24.system.bundle import create_bundle, load_bundle, state_from_data
from universe24.system.decoder import default_protocol
from universe24.system.runtime import TRACE_FILE, run_bundle, verify_run


SCHEMA = "universe24/local-unification-records/1"
RAILS = ("record_plus", "record_minus", "carrier_plus", "carrier_minus")


def _direction(direction):
    direction = tuple(direction)
    if (len(direction) != 3 or any(type(v) is not int for v in direction)
            or direction not in DIRECTIONS):
        raise ValueError("direction must be one physical face")
    return direction


def _bits(values):
    values = tuple(values)
    if len(values) != 4 or any(type(v) is not int or v not in (0, 1) for v in values):
        raise ValueError("four exact Boolean rails are required")
    return values


def collision_oracle(values, *, coupled=True):
    """Literal independently stated 1001<->0110 collision, all others fixed."""
    values = _bits(values)
    if type(coupled) is not bool:
        raise ValueError("coupled must be Boolean")
    if coupled and values == (1, 0, 0, 1):
        return (0, 1, 1, 0)
    if coupled and values == (0, 1, 1, 0):
        return (1, 0, 0, 1)
    return values


def outcome(values):
    """Distinguish absence/doubles from the direction of an actual record."""
    rp, rm, cp, cm = _bits(values)
    record = ("absent" if rp + rm == 0 else "double" if rp + rm == 2
              else "ready" if rp else "used")
    carrier = ("absent" if cp + cm == 0 else "double" if cp + cm == 2
               else "plus" if cp else "minus")
    return {"record": record, "carrier": carrier,
            "record_particles": rp + rm, "carrier_particles": cp + cm}


def incoming_direction_from_record(values):
    """Decode a ready/single-carrier trial from its COMPLETE output rails.

    The domain is essential: neither an unmarked zero nor an arbitrary used
    record is evidence that a new detector event occurred.
    """
    values = _bits(values)
    if values == (1, 0, 1, 0):
        return "plus"
    if values == (0, 1, 1, 0):
        return "minus"
    raise ValueError("not an output of a ready-record single-carrier trial")


def record_train(*, L=7, direction=(1, 0, 0)):
    """Complete current eight-rail preparation for four local encounters.

    Two independent retained banks meet at the same detector on updates
    1,2,5,6.  All particles are supplied at preparation.  There is no refill,
    externally triggered collision or hidden record log in the evolution.
    """
    direction = _direction(direction)
    if type(L) is not int or L < 7:
        raise ValueError("the four-encounter no-wrap fixture requires L>=7")
    grid = lattice(L)
    current = np.zeros((8, grid.N), dtype=object)
    def node(distance):
        return grid.index(*(distance * d % L for d in direction))
    for bank, offsets in ((0, (1, 3)), (1, (0, 2))):
        for distance in offsets:
            current[4*bank, node(-distance)] = 1
            current[4*bank+3, node(distance)] = 1
    return current


def scalar_first_order(values, L, *, direction=(1, 0, 0), coupled=True,
                       stream_records=True, inverse=False):
    """Independent collision table/stream oracle for both counted banks."""
    direction = _direction(direction)
    if type(stream_records) is not bool or type(inverse) is not bool:
        raise ValueError("stream_records and inverse must be Boolean")
    grid = lattice(L)
    values = np.asarray(values, dtype=object)
    if values.shape != (8, grid.N):
        raise ValueError("expected both complete four-rail banks")
    if any(type(x) is not int or x not in (0, 1) for x in values.flat):
        raise ValueError("all eight current rails must be exact Boolean integers")
    result = np.zeros_like(values)
    if inverse:
        # F^-1(A,B)=(S^-1 B,G^-1 A); G is the declared transposition.
        for rail in range(4):
            velocity = direction if rail % 2 == 0 else tuple(-d for d in direction)
            if rail < 2 and not stream_records:
                velocity = (0, 0, 0)
            for n in range(grid.N):
                xyz = grid.coords(n)
                source = grid.index(*((xyz[i] + velocity[i]) % L for i in range(3)))
                result[rail, n] = values[4+rail, source]
        for n in range(grid.N):
            result[4:, n] = collision_oracle(tuple(int(v) for v in values[:4, n]), coupled=coupled)
    else:
        for n in range(grid.N):
            result[:4, n] = collision_oracle(tuple(int(v) for v in values[4:, n]), coupled=coupled)
        for rail in range(4):
            velocity = direction if rail % 2 == 0 else tuple(-d for d in direction)
            if rail < 2 and not stream_records:
                velocity = (0, 0, 0)
            for n in range(grid.N):
                xyz = grid.coords(n)
                source = grid.index(*((xyz[i] - velocity[i]) % L for i in range(3)))
                result[4+rail, n] = values[rail, source]
    return result


def _validate_states(states, *, direction, coupled, stream_records):
    if len(states) < 2:
        raise ValueError("a complete seed and at least one transition are required")
    first = states[0]
    for index, state in enumerate(states):
        if not isinstance(state, State) or state.L != first.L or state.b.shape != (8, first.N):
            raise ValueError("mixed lattice or incomplete shared-law state")
        expected_a = scalar_first_order(state.b, state.L, direction=direction,
            coupled=coupled, stream_records=stream_records, inverse=True)
        if not np.array_equal(state.a, expected_a):
            raise ValueError("complete history is outside the prepared invariant sector")
        if index:
            before = states[index-1]
            expected = scalar_first_order(before.b, state.L, direction=direction,
                coupled=coupled, stream_records=stream_records)
            if (not np.array_equal(state.b, expected)
                    or not np.array_equal(state.a, before.b)
                    or not np.array_equal(state.r, before.r)):
                raise ValueError("trace does not follow the shared collision/transport law")


def inspect_states(states, *, direction=(1, 0, 0), coupled=True,
                   stream_records=True, detector=0):
    """Inspect every detector opportunity and actual moving retained records."""
    direction = _direction(direction)
    states = list(states)
    _validate_states(states, direction=direction, coupled=coupled, stream_records=stream_records)
    if type(detector) is not int or not 0 <= detector < states[0].N:
        raise ValueError("invalid detector node")
    rows, emissions = [], []
    for step, (before, after) in enumerate(zip(states, states[1:]), 1):
        incoming = tuple(int(v) for v in before.b[4:, detector])
        outgoing = tuple(int(v) for v in after.b[:4, detector])
        incoming_status, outgoing_status = outcome(incoming), outcome(outgoing)
        ready_single = incoming[:2] == (1, 0) and sum(incoming[2:]) == 1
        decoded = None
        if ready_single and coupled:
            decoded = incoming_direction_from_record(outgoing)
            if decoded != incoming_status["carrier"]:
                raise AssertionError("retained output failed to recover original incoming direction")
        row = {"step": step, "incoming_rails": list(incoming), "outgoing_rails": list(outgoing),
               "incoming": incoming_status, "outgoing": outgoing_status,
               "ready_single_trial": ready_single, "decoded_incoming_direction": decoded,
               "new_inversion_record": coupled and incoming == (1, 0, 0, 1)}
        rows.append(row)
        if row["new_inversion_record"]:
            emissions.append({"step": step, "node": detector})
    lifetimes = []
    L, grid = states[0].L, states[0].lattice
    for emission in emissions:
        start = emission["step"]
        origin = grid.coords(emission["node"])
        visits, stopped = [], "end_of_saved_window"
        for tick in range(start, len(states)):
            age = tick-start
            displacement = (age+1)//2 if stream_records else 0
            xyz = tuple((origin[i]-displacement*direction[i]) % L for i in range(3))
            node = grid.index(*xyz)
            bank = 0 if age % 2 == 0 else 1
            state = states[tick]
            # At each later collision, the strict carrier-free hypothesis is
            # checked from the retained B input, not inferred from the outcome.
            if age > 0 and bank == 0:
                incident = tuple(int(v) for v in states[tick-1].b[4:, node])
                if any(incident[2:]):
                    stopped = "carrier_free_hypothesis_ended"
                    break
            if int(state.b[4*bank+1, node]) != 1:
                raise AssertionError("used record disappeared within its proved empty-carrier corridor")
            visits.append({"step": tick, "bank": bank, "node": node, "xyz": list(xyz)})
        lifetimes.append({**emission, "verified_visits": visits,
                          "last_verified_step": visits[-1]["step"], "stop_reason": stopped})
    return {"schema": SCHEMA, "direction": list(direction), "coupled": coupled,
            "stream_records": stream_records, "steps": len(states)-1, "detector": detector,
            "detector_opportunities": rows, "created_inversion_record_steps": [e["step"] for e in emissions],
            "retained_used_particles_by_step": [sum(int(v) for row in (s.b[1],s.b[5]) for v in row) for s in states],
            "retained_record_particles_by_step": [sum(int(v) for row in (s.b[0],s.b[1],s.b[4],s.b[5]) for v in row) for s in states],
            "record_lifetimes": lifetimes, "independent_full_history_validation": True,
            "record_encoding": "two Boolean particle rails: absent00, ready10, used01, double11",
            "record_domain": "original-direction inference requires a declared ready10 and exactly one incoming carrier",
            "transport_calibration": "one lattice edge per two Engine updates; opposite direction to the selected carrier",
            "proper_time_clock": "not established; no material proper-time calibration follows from the pipeline period",
            "canonical_click_role": "passive arithmetic; neither C2 nor click count identifies these particle records"}


def inspect_saved_run(path, *, direction=(1, 0, 0), coupled=True,
                      stream_records=True, detector=0, allow_native_prefix=False):
    """Verify the complete saved input/history, then apply the fixed reader."""
    from validation.local_unification.native import build_tensor
    path = Path(path)
    verified = verify_run(path)
    bundle = load_bundle(path/"bundle")
    expected = build_tensor(direction=direction, coupled=coupled, stream_records=stream_records)
    if type(allow_native_prefix) is not bool:
        raise ValueError("allow_native_prefix must be Boolean")
    source_channels = bundle.tensor.G
    if bundle.tensor.fingerprint != pad_tensor(expected).fingerprint:
        if (not allow_native_prefix or source_channels <= 8
                or tuple(bundle.tensor.names[:8]) != tuple(expected.names)):
            raise ValueError("saved run is not the exact declared shared tensor")
        terms = tuple(m for m in bundle.tensor.monomials if m.target < 8)
        if any(f.gear >= 8 for m in terms for f in m.factors):
            raise ValueError("native record prefix depends on extra fields")
        prefix = Tensor(list(bundle.tensor.gears[:8]), terms, strict_support=True)
        if prefix.fingerprint != expected.fingerprint:
            raise ValueError("saved run does not contain the exact native record prefix")
    states = [bundle.seed]
    with gzip.open(path/TRACE_FILE, "rt", encoding="utf-8") as stream:
        for line in stream:
            states.append(state_from_data(exact_json.loads(line)["after"]))
    if source_channels > 8:
        # The complete source run was already verified above; this projection
        # certifies only its exact closed native prefix, not the extra fields.
        states = [State(s.L, s.a[:8].copy(), s.b[:8].copy(), s.r[:8].copy()) for s in states]
    report = inspect_states(states, direction=direction, coupled=coupled,
                            stream_records=stream_records, detector=detector)
    report.update({"tensor_hash": bundle.tensor.fingerprint, "bundle_id": bundle.bundle_id,
                   "run_id": verified["run_id"], "saved_runtime_verified": True,
                   "source_channels": source_channels, "inspected_record_channels": 8,
                   "native_prefix_hash": expected.fingerprint,
                   "extra_field_scope": "full runtime verified; physical interpretation of extra fields requires separate acceptance",
                   "maximum_integer_bits_by_step": verified["maximum_integer_bits_by_step"],
                   "canonical_arithmetic_records": verified["click_count"]})
    return report


def _bundle(*, direction, coupled, stream_records, current=None, L=7):
    from validation.local_unification.native import build_tensor, prepare_state
    tensor = build_tensor(direction=direction, coupled=coupled, stream_records=stream_records)
    current = record_train(L=L, direction=direction) if current is None else current
    carries = np.asarray([[(g+n)%6 for n in range(L**3)] for g in range(8)], dtype=object)
    seed = prepare_state(current, L, direction=direction, coupled=coupled,
                         stream_records=stream_records, remainders=carries)
    channels = [{"index": i, "name": gear.name, "label": gear.label,
                 "owner": "shared_conservative_collision",
                 "purpose": "Counted bank/dual rail of the common carrier-record law"}
                for i, gear in enumerate(tensor.gears)]
    return create_bundle(tensor, seed, channels=channels, protocol=default_protocol(), model={
        "id": "local-unification-record-train", "version": SCHEMA,
        "domain": "Prepared Boolean two-bank conservative collision; finite record transport experiment",
        "direction": list(direction), "coupled": coupled, "stream_records": stream_records})


def audit(out):
    """Run one shared-law record experiment plus clearly separate controls."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    reports = []
    for name, coupled, renewal in (("connected", True, True), ("disconnected", False, True),
                                    ("no_record_transport", True, False)):
        bundle = _bundle(direction=DIRECTIONS[0], coupled=coupled, stream_records=renewal)
        run_bundle(bundle, out/name, steps=6)
        report = inspect_saved_run(out/name, direction=DIRECTIONS[0], coupled=coupled,
                                    stream_records=renewal)
        report["name"] = name
        reports.append(report)
    if reports[0]["created_inversion_record_steps"] != [1, 2, 5, 6]:
        raise AssertionError("predeclared four-encounter fixture did not realize all four events")
    if reports[1]["created_inversion_record_steps"]:
        raise AssertionError("disconnected control created a collision record")
    # Every retained outgoing record permits source-direction reconstruction.
    # Empty, double and unprepared memory remain distinct and are not dropped.
    truth_rows = []
    for integer in range(16):
        incoming = tuple((integer >> (3-i)) & 1 for i in range(4))
        outgoing = collision_oracle(incoming)
        truth_rows.append({"incoming": list(incoming), "outgoing": list(outgoing),
                           "incoming_status": outcome(incoming), "outgoing_status": outcome(outgoing)})
    result = {"schema": SCHEMA, "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "runs": reports, "all_local_outcomes": truth_rows,
              "predeclared_encounter_steps": [1,2,5,6], "scope": {
                  "retained_records": "proved on declared dual-rail sector",
                  "repeated_local_selection": "four finite ready-record encounters in connected fixture",
                  "proper_time": "not established", "einstein_source": "requires independent geometry acceptance",
                  "indefinite_growth": "not inferred from four finite encounters"}}
    (out/"records.json").write_text(exact_json.dumps(result, sort_keys=True)+"\n", encoding="utf-8")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/local-unification/records"))
    parser.add_argument("--run", type=Path)
    args = parser.parse_args(argv)
    result = inspect_saved_run(args.run) if args.run else audit(args.out)
    print(exact_json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
