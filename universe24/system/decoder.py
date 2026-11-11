"""Passive, versioned arithmetic observations of complete Rule3 transitions.

This module does not evolve or repair a state. Its clicks implement the Engine's
official stream convention, including ownership labels; they are not particle
counts, physical detector outcomes, or a derivation of Born probabilities.
Complete transition provenance belongs to replay. Clicks deliberately omit it.
"""
from __future__ import annotations

import hashlib
from collections import Counter
from collections.abc import Iterable

from universe24.core import exact_json as json
from universe24.core.engine import State
from universe24.core.tensor import Tensor

TRANSITION_SCHEMA = "universe24/transition/1"
CLICK_SCHEMA = "universe24/arithmetic-click/1"
_TRANSITION_KEYS = {"schema", "run_id", "tensor_hash", "step", "before", "after"}
_CLICK_KEYS = {"schema", "event_id", "run_id", "tensor_hash", "step", "node",
               "xyz", "channel", "gear", "label", "quotient", "kind", "sign"}


def default_protocol() -> dict:
    """The one supported arithmetic protocol has no calibration or selection."""
    return {"version": CLICK_SCHEMA}


def validate_protocol(protocol: dict) -> None:
    """Reject unknown versions and settings instead of silently ignoring them."""
    if type(protocol) is not dict or protocol != default_protocol():
        raise ValueError("unsupported click protocol, calibration or selection settings")


def _integer(value, name: str, *, minimum: int | None = None) -> int:
    if type(value) is not int or (minimum is not None and value < minimum):
        raise ValueError(f"{name} must be an exact integer" +
                         (f" >= {minimum}" if minimum is not None else ""))
    return value


def _run_id(value) -> str:
    if type(value) is not str or not value:
        raise ValueError("run_id must be a nonempty string")
    return value


def _hash(data: dict) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True).encode("ascii")).hexdigest()


def _state(data, tensor: Tensor) -> State:
    if type(data) is not dict or set(data) != {"L", "a", "b", "r"}:
        raise ValueError("complete state requires exactly L, a, b and r")
    L = _integer(data["L"], "L", minimum=3)
    for field in ("a", "b", "r"):
        rows = data[field]
        if type(rows) is not list or len(rows) != tensor.G:
            raise ValueError(f"{field}: missing or extra channel rows")
        for row in rows:
            if type(row) is not list or len(row) != L ** 3:
                raise ValueError(f"{field}: missing or extra nodes")
            for value in row:
                _integer(value, field)
                if field == "r" and not 0 <= value < 6:
                    raise ValueError("remainders must be in 0..5")
    return State.from_dict(data)


def _serialize_state(state: State, tensor: Tensor) -> dict:
    # State arrays are mutable. Validate their current raw types before to_dict,
    # whose int(...) conversion could otherwise silently truncate injected floats.
    if not isinstance(state, State):
        raise ValueError("expected a complete State")
    try:
        checked = State(state.L, state.a, state.b, state.r)
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid exact-integer state") from exc
    data = checked.to_dict()
    _state(data, tensor)
    return data


def _validated_transition(record, tensor: Tensor, run_id: str | None):
    if type(record) is not dict or set(record) != _TRANSITION_KEYS:
        raise ValueError("transition fields are missing or unsupported")
    if record["schema"] != TRANSITION_SCHEMA:
        raise ValueError("unsupported transition schema")
    actual_run = _run_id(record["run_id"])
    if run_id is not None and actual_run != _run_id(run_id):
        raise ValueError("transition belongs to a different run")
    if record["tensor_hash"] != tensor.fingerprint:
        raise ValueError("transition tensor hash mismatch")
    step = _integer(record["step"], "step", minimum=1)
    before, after = (_state(record[key], tensor) for key in ("before", "after"))
    if before.L != after.L:
        raise ValueError("transition changes lattice size")
    for g in range(tensor.G):
        for n in range(before.N):
            a, b, r = before.gear(g, n)
            ap, bp, rp = after.gear(g, n)
            if ap != b:
                raise ValueError("transition violates a_next=b")
            # K=2*u must be even. Full polynomial equality is replay's job.
            if (6 * (bp + a) + rp - r) % 2:
                raise ValueError("transition is incompatible with even K=2*u")
    return actual_run, step, before, after


def make_transition(tensor: Tensor, before: State, after: State, *,
                    run_id: str, step: int) -> dict:
    """Copy complete snapshots to a JSON record without retaining mutable aliases."""
    record = {"schema": TRANSITION_SCHEMA, "run_id": run_id,
              "tensor_hash": tensor.fingerprint, "step": step,
              "before": _serialize_state(before, tensor),
              "after": _serialize_state(after, tensor)}
    _validated_transition(record, tensor, run_id)
    return record


def decode_transition(record: dict, tensor: Tensor, *, run_id: str | None = None) -> list[dict]:
    """Decode one complete transition in canonical node/channel order.

    This readout validates the record and arithmetic shift but does not claim to
    verify the tensor polynomial. Independent replay must check that separately.
    """
    actual_run, step, before, after = _validated_transition(record, tensor, run_id)
    clicks = []
    for n in range(before.N):
        xyz = list(before.lattice.coords(n))
        for g, gear in enumerate(tensor.gears):
            old, new = before.gear(g, n), after.gear(g, n)
            quotient = new[1] + old[0]
            if quotient == 0 or old == new:
                continue
            delta = (new[2] - old[2]) % 6
            kind = "C0" if delta in (0, 3) else "C1" if delta in (1, 2) else "C2"
            identity = {"run_id": actual_run, "tensor_hash": record["tensor_hash"],
                        "step": step, "node": n, "channel": g}
            clicks.append({"schema": CLICK_SCHEMA, "event_id": _hash(identity),
                           **identity, "xyz": list(xyz), "gear": gear.name, "label": gear.label,
                           "quotient": quotient, "kind": kind,
                           "sign": 1 if quotient > 0 else -1})
    return clicks


def decode_trace(records: Iterable[dict], tensor: Tensor, *, run_id: str,
                 expected_steps: int, initial_state: State | None = None) -> list[dict]:
    """Decode a complete contiguous trace; reject duplicates, gaps and truncation."""
    _run_id(run_id)
    _integer(expected_steps, "expected_steps", minimum=0)
    previous = _serialize_state(initial_state, tensor) if initial_state is not None else None
    clicks = []
    count = 0
    for count, record in enumerate(records, 1):
        _validated_transition(record, tensor, run_id)
        if count > expected_steps or record["step"] != count:
            raise ValueError("transition step gap, duplicate or extra record")
        if previous is not None and record["before"] != previous:
            raise ValueError("transition chain does not match previous complete state")
        clicks.extend(decode_transition(record, tensor, run_id=run_id))
        previous = record["after"]
    if count != expected_steps:
        raise ValueError("missing transition records or truncated trace")
    return clicks


def verify_click_records(records: Iterable[dict], expected: Iterable[dict]) -> None:
    """Compare a saved stream with independently decoded records, without filtering.

    No-detection steps are established by the complete trace, not fabricated
    zero-click records. Supplying the expected stream is necessary to detect loss.
    """
    actual = list(records)
    seen = set()
    for record in actual:
        if type(record) is not dict or set(record) != _CLICK_KEYS or record["schema"] != CLICK_SCHEMA:
            raise ValueError("malformed or unsupported click record")
        for name in ("step", "node", "channel", "quotient", "sign"):
            _integer(record[name], name)
        _run_id(record["run_id"])
        if (record["step"] < 1 or record["node"] < 0 or record["channel"] < 0
                or record["quotient"] == 0
                or record["sign"] != (1 if record["quotient"] > 0 else -1)):
            raise ValueError("invalid click index, quotient or sign")
        if record["kind"] not in ("C0", "C1", "C2") or record["label"] not in ("official", "audit"):
            raise ValueError("invalid click class or label")
        if type(record["gear"]) is not str or not record["gear"]:
            raise ValueError("invalid click gear name")
        fingerprint = record["tensor_hash"]
        if (type(fingerprint) is not str or len(fingerprint) != 64
                or any(c not in "0123456789abcdef" for c in fingerprint)):
            raise ValueError("invalid click tensor hash")
        if type(record["xyz"]) is not list or len(record["xyz"]) != 3:
            raise ValueError("malformed click coordinates")
        for coordinate in record["xyz"]:
            _integer(coordinate, "coordinate", minimum=0)
        identity = {key: record[key] for key in ("run_id", "tensor_hash", "step", "node", "channel")}
        if type(record["event_id"]) is not str or record["event_id"] != _hash(identity):
            raise ValueError("click event identity mismatch")
        if record["event_id"] in seen:
            raise ValueError("duplicate click event")
        seen.add(record["event_id"])
    if actual != list(expected):
        raise ValueError("click stream missing, reordered, corrupted or contains extra events")


def summarize_clicks(records: Iterable[dict]) -> dict:
    """Arithmetic counts using click records alone; no hidden state or physical units."""
    events = list(records)
    verify_click_records(events, events)
    kinds = Counter(record["kind"] for record in events)
    return {"interpretation": "arithmetic clicks only", "events": len(events),
            "by_kind": {kind: kinds[kind] for kind in ("C0", "C1", "C2")},
            "signed_quotient_sum": sum(record["quotient"] for record in events)}
