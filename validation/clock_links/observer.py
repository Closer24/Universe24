"""Passive trial readout from canonical clicks and a predeclared protocol only.

No state, tensor evaluator, RNG or Engine is accepted by this module. The
protocol is analysis metadata, separate from the runtime arithmetic protocol.
An empty window means no recorded event, not zero hidden field or intensity.
Completeness of the input stream must be established by independent replay.
"""
from __future__ import annotations

from bisect import bisect_left
from collections import Counter
from copy import deepcopy
from hashlib import sha256

from universe24.core import exact_json
from universe24.system.decoder import verify_click_records

PROTOCOL_SCHEMA = "universe24/clock-link-observer-protocol/1"
REPORT_SCHEMA = "universe24/clock-link-observer/1"


def _integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def _text(value, name):
    if type(value) is not str or not value:
        raise ValueError(f"{name} must be nonempty text")


def make_protocol(*, tensor_hash, L, channel_count, expected_steps, detectors,
                  windows=None):
    """Declare every observation window; default is one window per microtick.

    A detector is {id, node, channels}; a window is {id, start, stop}, inclusive.
    Windows partition 1..expected_steps exactly. No class/quotient filtering is
    accepted. A microtick window is not thereby a physical emission trial.
    """
    _integer(expected_steps, "expected_steps", 1)
    protocol = {"schema": PROTOCOL_SCHEMA, "tensor_hash": tensor_hash, "L": L,
                "channel_count": channel_count, "expected_steps": expected_steps,
                "detectors": deepcopy(detectors),
                "windows": deepcopy(windows) if windows is not None else [
                    {"id": f"step-{step}", "start": step, "stop": step}
                    for step in range(1, expected_steps + 1)]}
    validate_protocol(protocol)
    return protocol


def validate_protocol(protocol):
    keys = {"schema", "tensor_hash", "L", "channel_count", "expected_steps",
            "detectors", "windows"}
    if type(protocol) is not dict or set(protocol) != keys:
        raise ValueError("unknown or missing observer protocol fields")
    if protocol["schema"] != PROTOCOL_SCHEMA:
        raise ValueError("unsupported observer protocol")
    fingerprint = protocol["tensor_hash"]
    if (type(fingerprint) is not str or len(fingerprint) != 64
            or any(c not in "0123456789abcdef" for c in fingerprint)):
        raise ValueError("invalid protocol tensor hash")
    _integer(protocol["L"], "L", 3)
    _integer(protocol["channel_count"], "channel_count", 1)
    if protocol["channel_count"] > 48:
        raise ValueError("observer channel budget exceeds 48")
    _integer(protocol["expected_steps"], "expected_steps", 1)
    detectors = protocol["detectors"]
    if type(detectors) is not list or not detectors:
        raise ValueError("at least one declared detector is required")
    ids, occupied = set(), set()
    for detector in detectors:
        if type(detector) is not dict or set(detector) != {"id", "node", "channels"}:
            raise ValueError("detector requires exactly id, node and channels")
        _text(detector["id"], "detector id")
        if detector["id"] in ids:
            raise ValueError("duplicate detector id")
        ids.add(detector["id"])
        _integer(detector["node"], "detector node")
        if detector["node"] >= protocol["L"] ** 3:
            raise ValueError("detector node outside lattice")
        channels = detector["channels"]
        if type(channels) is not list or not channels:
            raise ValueError("detector channels must be a nonempty list")
        for channel in channels:
            _integer(channel, "detector channel")
            if channel >= protocol["channel_count"]:
                raise ValueError("detector channel outside allocation")
            pair = detector["node"], channel
            if pair in occupied:
                raise ValueError("detector ports overlap or repeat")
            occupied.add(pair)
    windows = protocol["windows"]
    if type(windows) is not list or not windows:
        raise ValueError("complete observation windows are required")
    ids, next_step = set(), 1
    for window in windows:
        if type(window) is not dict or set(window) != {"id", "start", "stop"}:
            raise ValueError("window requires exactly id, start and stop")
        _text(window["id"], "window id")
        if window["id"] in ids:
            raise ValueError("duplicate window id")
        ids.add(window["id"])
        _integer(window["start"], "window start", 1)
        _integer(window["stop"], "window stop", 1)
        if window["start"] != next_step or window["stop"] < window["start"]:
            raise ValueError("windows must partition the run without gaps or overlaps")
        next_step = window["stop"] + 1
    if next_step != protocol["expected_steps"] + 1:
        raise ValueError("windows do not cover the complete declared run")


class ClickObserver:
    """Incremental passive reader with bounded per-window summaries.

    No reference to mutable caller data is retained. Event identities are
    checked; missing well-formed records remain unobservable without replay.
    """

    def __init__(self, protocol, *, run_id):
        validate_protocol(protocol)
        _text(run_id, "run_id")
        self._protocol = deepcopy(protocol)
        self._run_id = run_id
        self._last_order = None
        self._digest = sha256()
        self._record_count = 0
        self._selected_count = 0
        self._ends = [w["stop"] for w in protocol["windows"]]
        self._ports = {(d["node"], c): i for i, d in enumerate(protocol["detectors"])
                       for c in d["channels"]}
        self._bins = [[{"event_count": 0, "signed_quotient_sum": 0,
                        "absolute_quotient_sum": 0, "by_kind": Counter(),
                        "by_channel": Counter()}
                       for _ in protocol["detectors"]] for _ in protocol["windows"]]

    def consume(self, records):
        for record in records:
            # This validates exact types and canonical identity, without any
            # retained state. Comparing a record with itself does not certify
            # truth or completeness; the report expressly records that limit.
            verify_click_records([record], [record])
            p = self._protocol
            if record["run_id"] != self._run_id or record["tensor_hash"] != p["tensor_hash"]:
                raise ValueError("click belongs to a different run or tensor")
            if not 1 <= record["step"] <= p["expected_steps"]:
                raise ValueError("click step outside declared run")
            if record["node"] >= p["L"] ** 3 or record["channel"] >= p["channel_count"]:
                raise ValueError("click port outside declared allocation")
            n, side = record["node"], p["L"]
            if record["xyz"] != [n // (side * side), (n // side) % side, n % side]:
                raise ValueError("click coordinates disagree with node index")
            order = record["step"], n, record["channel"]
            if self._last_order is not None and order <= self._last_order:
                raise ValueError("duplicate or reordered click record")
            self._last_order = order
            self._digest.update(exact_json.dumps(record, sort_keys=True,
                                                separators=(",", ":")).encode())
            self._digest.update(b"\n")
            self._record_count += 1
            detector = self._ports.get((n, record["channel"]))
            if detector is None:
                continue
            self._selected_count += 1
            index = bisect_left(self._ends, record["step"])
            bucket = self._bins[index][detector]
            bucket["event_count"] += 1
            bucket["signed_quotient_sum"] += record["quotient"]
            bucket["absolute_quotient_sum"] += abs(record["quotient"])
            bucket["by_kind"][record["kind"]] += 1
            bucket["by_channel"][record["channel"]] += 1
        return self

    def report(self):
        rows, totals = [], Counter()
        for window, bins in zip(self._protocol["windows"], self._bins):
            for detector, bucket in zip(self._protocol["detectors"], bins):
                count = bucket["event_count"]
                outcome = "none" if count == 0 else "single" if count == 1 else "multiple"
                totals[outcome] += 1
                rows.append({"window": deepcopy(window), "detector": detector["id"],
                             "outcome": outcome, "event_count": count,
                             "signed_quotient_sum": bucket["signed_quotient_sum"],
                             "absolute_quotient_sum": bucket["absolute_quotient_sum"],
                             "by_kind": {k: bucket["by_kind"][k] for k in ("C0", "C1", "C2")},
                             "by_channel": {str(c): bucket["by_channel"][c]
                                            for c in detector["channels"]}})
        return {"schema": REPORT_SCHEMA, "run_id": self._run_id,
                "protocol": deepcopy(self._protocol), "trials": rows,
                "outcome_counts": {name: totals[name] for name in ("none", "single", "multiple")},
                "input_records": self._record_count,
                "declared_detector_records": self._selected_count,
                "input_record_sha256": self._digest.hexdigest(),
                "stream_completeness": "requires independent complete-run replay",
                "interpretation": "Arithmetic record windows, not physical emission trials. Empty means no recorded event; nonzero stationary intensity can be invisible. Quotient sums cover recorded events only; no Born sampler or intensity reconstruction is applied."}


def observe_clicks(records, protocol, *, run_id):
    """Read an iterable once; requires no hidden states or expected outcomes."""
    return ClickObserver(protocol, run_id=run_id).consume(records).report()
