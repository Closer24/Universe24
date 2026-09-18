"""Read the records of experiment E12 (docs/EXPERIMENTS.md), the screen without a
draw, and evaluate them against the mean-field prediction of `mean_field.py`
(`predictions.json`): per run the clicks, passes and returns per mark with
their ticks, the tickets each mark consumed (one per drawn arrival: a click or
a return; a pass consumes none), where the returned quanta ended, the marks'
counters when the record carries them (feature 2c, a click is an absorption),
the ledger and the fingerprints; then the comparisons: the counter's counts
against the mean field mark by mark (the ratio and its spread), the drawn marks
against the counter scaled by 1 / d, the determinism of the click order between
a rerun and another ticket seed at setting [1, 1], and the interference counts
in phase against antiphase, with and without the steering coupling. A Renderer
of records in the sense of Highlights 3.29: it reads only what the runner, the
Recorder and the extractor wrote (`run.json`, `events.jsonl`,
`initialization.json`, `ray-recording.json`, `runs.json`) and never the engine.

Run:  python examples/nature/e12_no_draw/analyze.py RUNS_DIR [--record record.json]
where RUNS_DIR holds one directory per case, named as `make_worlds.py` names
the worlds, with the suffixes `_rerun` (the same world run again) and `_e96`
(the same world in the engine for 96 ticks, for the viewer document).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIEWER_TICKS = 96


def load_events(directory: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in (directory / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def digests(directory: Path) -> tuple[str, str]:
    """The events file's digest and the digest of its lines without the host's
    `cost` (the operation count of a cycle)."""
    raw = (directory / "events.jsonl").read_bytes()
    physical = hashlib.sha256()
    for line in raw.splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        event.pop("cost", None)
        physical.update(json.dumps(event, sort_keys=True).encode("utf-8"))
        physical.update(b"\n")
    return hashlib.sha256(raw).hexdigest(), physical.hexdigest()


def components(value):
    return [value] if isinstance(value, int) else list(value)


def ledger_line(ledger: dict, family: str) -> dict:
    entry = ledger["fields"][family]
    return {key: (components(v) if key != "balanced" else v) for key, v in entry.items()}


def in_flight_returns(directory: Path, family: str) -> int | None:
    """The quanta of `family` still walking back (outbound 0) in the last frame of
    the recording, or None without a recording."""
    sidecar = directory / "ray-recording.json"
    if not sidecar.exists():
        return None
    frames = json.loads(sidecar.read_text(encoding="utf-8"))["frames"]
    last = frames[-1]
    return sum(
        item["ray"]["amount"]
        for item in last["rays"]
        if item["field"] == family and not item["ray"]["outbound"]
    )


def viewer_summary(directory: Path) -> dict | None:
    document = directory / "runs.json"
    if not document.exists():
        return None
    runs = json.loads(document.read_text(encoding="utf-8"))["runs"]
    (run,) = runs
    return {
        "event_kinds": run["event_kinds"],
        "rays": len(run["rays"]),
        "ticks": run["ticks"],
        "ticks_capped_from": run["record"].get("ticks_capped_from"),
        "hits": run.get("eye", {}).get("hits"),
    }


def analyze(directory: Path) -> dict:
    metadata = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    world = json.loads((directory / "initialization.json").read_text(encoding="utf-8"))
    events = load_events(directory)
    kinds = Counter(event["event"] for event in events)
    marks = {tuple(mark["position"]): mark for mark in world.get("detectors", [])}
    field_family = next(f["field"] for f in world["spatial_fields"] if f.get("spread"))
    per_mark = {
        position: {
            "setting": mark["setting"],
            "seed": mark["seed"],
            "clicks": 0,
            "quanta": 0,
            "click_ticks": [],
            "passes": 0,
            "pass_quanta": 0,
            "returns": 0,
            "return_quanta": 0,
            "return_ticks": [],
            "tickets_per_tick": Counter(),
        }
        for position, mark in marks.items()
    }
    clicks = []
    other_detector_events = Counter()
    for event in events:
        kind = event["event"]
        if not kind.startswith("detector_"):
            continue
        position = tuple(event["position"])
        row = per_mark.get(position)
        if row is None:
            other_detector_events[kind] += 1
            continue
        if kind == "detector_click":
            row["clicks"] += 1
            row["quanta"] += event["amount"]
            row["click_ticks"].append(event["tick"])
            row["tickets_per_tick"][event["tick"]] += 1
            row["absorbed"] = row.get("absorbed", 0) + int(event.get("absorbed") or 0)
            clicks.append(
                (
                    event["tick"],
                    list(position),
                    event["amount"],
                    event["port"],
                    event.get("bit"),
                    event.get("family"),
                    event.get("absorbed"),
                )
            )
        elif kind == "detector_pass":
            row["passes"] += 1
            row["pass_quanta"] += event["amount"]
        elif kind == "detector_return":
            row["returns"] += 1
            row["return_quanta"] += event["amount"]
            row["return_ticks"].append(event["tick"])
            row["tickets_per_tick"][event["tick"]] += 1
        else:
            other_detector_events[kind] += 1
    counters = {tuple(m["position"]): m for m in metadata.get("detector_marks", [])}
    for position, row in per_mark.items():
        row.setdefault("absorbed", 0)
        mark = counters.get(position)
        row["counter"] = None if mark is None else mark.get("counter")
        row["momentum"] = None if mark is None else mark.get("momentum")
        row["tickets_consumed"] = row["clicks"] + row["returns"]
        row["tickets_per_tick"] = dict(sorted(row["tickets_per_tick"].items()))
        row["first_click"] = row["click_ticks"][0] if row["click_ticks"] else None
        row["last_click"] = row["click_ticks"][-1] if row["click_ticks"] else None
    # Where the returned quanta ended (field_returned: the family that took them,
    # the Node, restored or unbooked); the rest escaped or is still walking.
    ended = defaultdict(int)
    ended_at = defaultdict(int)
    for event in events:
        if event["event"] == "field_returned":
            ended[str(event.get("by"))] += event["amount"]
            ended_at[str(list(event["position"]))] += event["amount"]
    returned_total = sum(row["return_quanta"] for row in per_mark.values())
    flight = in_flight_returns(directory, field_family)
    audit = metadata["audit"]
    last = audit[-1]
    families = [f["name"] for f in world["fields"]]
    lines = {family: ledger_line(last, family) for family in families if family in last["fields"]}
    ledger_at = {
        str(entry["tick"]): {
            family: ledger_line(entry, family) for family in families if family in entry["fields"]
        }
        for entry in audit
        if entry["tick"] in (48, 96, 120, 240)
    }
    # The source line of the field per tick: a negative step is an unbooking (a
    # returned quantum that reached its releaser).
    sourced = [ledger_line(entry, field_family)["sourced"][0] for entry in audit]
    unbooked_ticks = [audit[i]["tick"] for i in range(1, len(sourced)) if sourced[i] < sourced[i - 1]]
    matter = [f["name"] for f in world["fields"] if f["name"] not in (field_family, "momentum")]
    matter_constant = {
        family: all(
            ledger_line(entry, family)["current"] == ledger_line(entry, family)["initial"]
            and not any(
                ledger_line(entry, family)[k][0] for k in ("sourced", "escaped", "annulled", "absorbed")
            )
            for entry in audit
        )
        for family in matter
        if family in last["fields"]
    }
    events_sha, physical_sha = digests(directory)
    identity_keys = [
        k
        for k in metadata
        if k.startswith("detector")
        or "absorb" in k
        or "mark" in k
        or k in ("dense_field", "ray_layer_families", "ray_meeting")
    ]
    return {
        "case": directory.name,
        "model": metadata["model"],
        "status": metadata["status"],
        "error": metadata.get("error"),
        "completed_ticks": metadata["completed_ticks"],
        "requested_ticks": metadata.get("requested_ticks"),
        "elapsed_seconds": metadata["elapsed_seconds"],
        "dense_field": metadata.get("dense_field"),
        "source_sha256": metadata["source_sha256"],
        "initialization_sha256": metadata["initialization_sha256"],
        "events_sha256": events_sha,
        "events_without_cost_sha256": physical_sha,
        "identities": {k: metadata[k] for k in identity_keys},
        "conserved_at_every_completed_tick": metadata["conserved_at_every_completed_tick"],
        "balanced_every_tick": all(entry["balanced"] for entry in audit),
        "event_kinds": dict(sorted(kinds.items())),
        "other_detector_events": dict(other_detector_events),
        "field": field_family,
        "marks": {str(list(p)): row for p, row in per_mark.items()},
        "clicks": clicks,
        "click_count": len(clicks),
        "click_quanta": sum(c[2] for c in clicks),
        "click_absorbed": sum(int(c[6] or 0) for c in clicks),
        "every_click_absorbed": all(c[6] == c[2] for c in clicks),
        "detector_mark_totals": metadata.get("detector_mark_totals"),
        "detector_mark_momentum": metadata.get("detector_mark_momentum"),
        "returned": {
            "quanta": returned_total,
            "ended_by": dict(ended),
            "ended_at": dict(ended_at),
            "in_flight_at_end": flight,
            "escaped_or_in_flight": returned_total - sum(ended.values()),
        },
        "unbooked_at_ticks": unbooked_ticks,
        "ledger_last": lines,
        "ledger_at": ledger_at,
        "matter_constant": matter_constant,
        "final_totals": metadata["final_totals"],
        "escaped_totals": metadata["escaped_totals"],
        "source_totals": metadata.get("source_totals"),
        "external_body_totals": metadata.get("external_body_totals"),
        "external_bodies": [
            {k: v for k, v in body.items() if k != "positions"}
            for body in metadata.get("external_bodies", [])
        ],
        "viewer": viewer_summary(directory),
    }


# ---- comparisons ----------------------------------------------------------


def quanta_by_mark(summary: dict, through: int | None = None) -> dict[str, int]:
    """Quanta clicked per mark, through tick `through` when given."""
    result = {mark: 0 for mark in summary["marks"]}
    for tick, position, amount, *_ in summary["clicks"]:
        if through is None or tick <= through:
            result[str(position)] += amount
    return result


def counts_by_mark(summary: dict, through: int | None = None) -> dict[str, int]:
    result = {mark: 0 for mark in summary["marks"]}
    for tick, position, *_ in summary["clicks"]:
        if through is None or tick <= through:
            result[str(position)] += 1
    return result


def ratios(observed: dict[str, float], predicted: dict[str, float]) -> dict:
    rows = {}
    values = []
    for mark, expected in predicted.items():
        seen = observed.get(mark, 0)
        ratio = seen / expected if expected else None
        rows[mark] = {"observed": seen, "predicted": expected, "ratio": ratio}
        if ratio is not None:
            values.append(ratio)
    return {
        "marks": rows,
        "mean_ratio": statistics.fmean(values) if values else None,
        "min_ratio": min(values) if values else None,
        "max_ratio": max(values) if values else None,
        "stdev_ratio": statistics.pstdev(values) if len(values) > 1 else None,
        "total_observed": sum(observed.get(m, 0) for m in predicted),
        "total_predicted": sum(predicted.values()),
    }


def part1(summaries: dict, prediction: dict) -> dict:
    out = {}
    absorbing = {m: r["integrated"] for m, r in prediction["part1"]["absorbing"]["marks"].items()}
    transparent = {m: r["integrated"] for m, r in prediction["part1"]["transparent"]["marks"].items()}
    counter = summaries.get("screen_d1")
    for case, d in (("screen_d1", 1), ("screen_d2", 2), ("screen_d4", 4)):
        s = summaries.get(case)
        if s is None:
            continue
        quanta = quanta_by_mark(s)
        block = {
            "setting": [1, d],
            "quanta": quanta,
            "clicks": counts_by_mark(s),
            "against_mean_field_absorbing_over_d": ratios(
                quanta, {m: v / d for m, v in absorbing.items()}
            ),
            "against_mean_field_transparent_over_d": ratios(
                quanta, {m: v / d for m, v in transparent.items()}
            ),
            "counters": {m: r["counter"] for m, r in s["marks"].items()},
            "every_click_absorbed": s["every_click_absorbed"],
            "returns": {m: r["return_quanta"] for m, r in s["marks"].items()},
            "passes": {m: r["pass_quanta"] for m, r in s["marks"].items()},
            "tickets_consumed": {m: r["tickets_consumed"] for m, r in s["marks"].items()},
            "returned": s["returned"],
            "unbooked_at_ticks": s["unbooked_at_ticks"],
            "ledger_last": s["ledger_last"],
        }
        if counter is not None and d > 1:
            block["against_counter_over_d"] = ratios(
                quanta, {m: v / d for m, v in quanta_by_mark(counter).items()}
            )
        out[case] = block
    # Determinism: the rerun and the other seed against the counter.
    if counter is not None:
        det = {}
        for other in ("screen_d1_rerun", "screen_d1_seed7"):
            s = summaries.get(other)
            if s is None:
                continue
            det[other] = {
                "clicks_identical": s["clicks"] == counter["clicks"],
                "events_sha256_identical": s["events_sha256"] == counter["events_sha256"],
                "events_without_cost_sha256_identical": s["events_without_cost_sha256"]
                == counter["events_without_cost_sha256"],
                "ledger_identical": s["ledger_last"] == counter["ledger_last"],
                "initialization_sha256_identical": s["initialization_sha256"]
                == counter["initialization_sha256"],
                "tickets_consumed": {m: r["tickets_consumed"] for m, r in s["marks"].items()},
            }
        out["determinism"] = det
        out["tickets"] = {
            "rule": "one ticket per drawn arrival (a click or a return); a pass consumes none",
            "counter_tickets_equal_clicks": all(
                r["tickets_consumed"] == r["clicks"] and r["returns"] == 0
                for r in counter["marks"].values()
            ),
            "counter_tickets_per_tick": {m: r["tickets_per_tick"] for m, r in counter["marks"].items()},
        }
    return out


def mirror(mark: str, width: int) -> str:
    x, y, z = json.loads(mark)
    return str([x, width - y, z])


def alternation(values: list[int]) -> dict:
    """Whether a list alternates along the line: the count of sign changes of the
    first difference and the longest run of one sign."""
    diffs = [b - a for a, b in zip(values[:-1], values[1:], strict=True)]
    signs = [0 if d == 0 else (1 if d > 0 else -1) for d in diffs]
    changes = sum(1 for a, b in zip(signs[:-1], signs[1:], strict=True) if a and b and a != b)
    return {"differences": diffs, "sign_changes": changes}


def part2(summaries: dict, prediction: dict) -> dict:
    predicted = {m: r["integrated"] for m, r in prediction["part2"]["marks"].items()}
    predicted_96 = {
        m: r["integrated_by_tick"][str(VIEWER_TICKS)] for m, r in prediction["part2"]["marks"].items()
    }
    marks = list(predicted)
    width = 16
    out = {"predicted": predicted, "fringe_period_links": prediction["part2"]["fringe_period_links"]}
    plain = {}
    for case in ("two_inphase", "two_antiphase"):
        s = summaries.get(case)
        if s is None:
            continue
        quanta = quanta_by_mark(s)
        plain[case] = {
            "ticks": s["completed_ticks"],
            "dense_field": s["dense_field"],
            "quanta": quanta,
            "clicks": counts_by_mark(s),
            "quanta_through_96": quanta_by_mark(s, VIEWER_TICKS),
            "against_mean_field": ratios(quanta, predicted),
            "against_mean_field_through_96": ratios(quanta_by_mark(s, VIEWER_TICKS), predicted_96),
            "mirror_symmetric": all(quanta[m] == quanta[mirror(m, width)] for m in marks),
            "along_y": alternation([quanta[m] for m in marks]),
            "ledger_last": s["ledger_last"],
            "external_body_totals": s["external_body_totals"],
        }
    out["plain"] = plain
    if "two_inphase" in plain and "two_antiphase" in plain:
        a, b = plain["two_inphase"], plain["two_antiphase"]
        out["inphase_equals_antiphase"] = {
            "quanta_identical": a["quanta"] == b["quanta"],
            "clicks_identical": a["clicks"] == b["clicks"],
            "click_lists_identical": summaries["two_inphase"]["clicks"]
            == summaries["two_antiphase"]["clicks"],
            "ledger_identical": a["ledger_last"] == b["ledger_last"],
            "difference": {m: a["quanta"][m] - b["quanta"][m] for m in marks},
        }
    # The engine's 96-tick records against the dense records through tick 96.
    identity = {}
    for case in ("two_inphase", "two_antiphase"):
        e = summaries.get(case + "_e96")
        d = summaries.get(case)
        if e is None or d is None:
            continue
        identity[case] = {
            "engine_ticks": e["completed_ticks"],
            "clicks_identical_through_96": e["clicks"]
            == [c for c in d["clicks"] if c[0] <= e["completed_ticks"]],
            "ledger_identical_at_96": e["ledger_last"] == d["ledger_at"].get(str(e["completed_ticks"])),
            "viewer": e["viewer"],
        }
    out["engine_against_dense"] = identity
    steer = {}
    for case in ("two_inphase_steer", "two_antiphase_steer"):
        s = summaries.get(case)
        if s is None:
            continue
        base = summaries.get(case.replace("_steer", ""))
        through = s["completed_ticks"]
        quanta = quanta_by_mark(s)
        steer[case] = {
            "ticks": through,
            "layers": s["identities"].get("ray_layer_families"),
            "quanta": quanta,
            "clicks": counts_by_mark(s),
            "mirror_symmetric": all(quanta[m] == quanta[mirror(m, width)] for m in marks),
            "along_y": alternation([quanta[m] for m in marks]),
            "without_coupling_through_same_ticks": None
            if base is None
            else quanta_by_mark(base, through),
            "against_mean_field_through_96": (
                ratios(quanta, predicted_96) if through == VIEWER_TICKS else None
            ),
            "ledger_last": s["ledger_last"],
            "external_body_totals": s["external_body_totals"],
            "viewer": s["viewer"],
        }
    out["steer"] = steer
    if "two_inphase_steer" in steer and "two_antiphase_steer" in steer:
        a, b = steer["two_inphase_steer"], steer["two_antiphase_steer"]
        out["steer_inphase_against_antiphase"] = {
            "quanta_identical": a["quanta"] == b["quanta"],
            "difference": {m: a["quanta"][m] - b["quanta"][m] for m in marks},
            "sum_inphase": sum(a["quanta"].values()),
            "sum_antiphase": sum(b["quanta"].values()),
        }
    return out


# ---- printing -------------------------------------------------------------


def print_part1(block: dict) -> None:
    print("== Part 1: the counter against the drawn marks (quanta clicked per mark over 240 ticks)")
    for case in ("screen_d1", "screen_d2", "screen_d4"):
        b = block.get(case)
        if b is None:
            continue
        r = b["against_mean_field_absorbing_over_d"]
        print(f"   {case} setting {b['setting']}: quanta {b['quanta']}")
        print(f"      clicks {b['clicks']}")
        print(
            f"      against the mean field (marks absorbing) / d: mean ratio"
            f" {r['mean_ratio']:.3f}, min {r['min_ratio']:.3f}, max {r['max_ratio']:.3f},"
            f" total {r['total_observed']} / {r['total_predicted']:.1f}"
        )
        t = b["against_mean_field_transparent_over_d"]
        print(
            f"      against the mean field (marks transparent) / d: mean ratio {t['mean_ratio']:.3f}, total {t['total_observed']} / {t['total_predicted']:.1f}"
        )
        if "against_counter_over_d" in b:
            c = b["against_counter_over_d"]
            print(
                f"      against the counter / d: mean ratio {c['mean_ratio']:.3f}, min {c['min_ratio']:.3f}, max {c['max_ratio']:.3f}"
            )
        print(f"      returns {b['returns']}; passes {b['passes']}; tickets {b['tickets_consumed']}")
        print(
            f"      returned quanta {b['returned']}; unbooked at ticks {b['unbooked_at_ticks'][:12]}{'...' if len(b['unbooked_at_ticks']) > 12 else ''}"
        )
        print(f"      light line {b['ledger_last'].get('light')}")
    if "determinism" in block:
        print(
            "   determinism:",
            json.dumps(
                {
                    k: {kk: vv for kk, vv in v.items() if kk != "tickets_consumed"}
                    for k, v in block["determinism"].items()
                }
            ),
        )
        print(
            "   tickets:",
            block["tickets"]["rule"],
            "; counter tickets = clicks:",
            block["tickets"]["counter_tickets_equal_clicks"],
        )


def print_part2(block: dict) -> None:
    print("\n== Part 2: two sources on fifteen counters (quanta per mark)")
    marks = list(block["predicted"])
    print(
        f"   {'mark':>12} {'mean field':>10} {'inphase':>8} {'antiphase':>9} {'in@96':>6} {'anti@96':>7} {'steer in':>8} {'steer anti':>10}"
    )
    plain, steer = block.get("plain", {}), block.get("steer", {})
    for m in marks:
        row = [
            f"{block['predicted'][m]:>10.2f}",
            f"{plain.get('two_inphase', {}).get('quanta', {}).get(m, '-'):>8}",
            f"{plain.get('two_antiphase', {}).get('quanta', {}).get(m, '-'):>9}",
            f"{plain.get('two_inphase', {}).get('quanta_through_96', {}).get(m, '-'):>6}",
            f"{plain.get('two_antiphase', {}).get('quanta_through_96', {}).get(m, '-'):>7}",
            f"{steer.get('two_inphase_steer', {}).get('quanta', {}).get(m, '-'):>8}",
            f"{steer.get('two_antiphase_steer', {}).get('quanta', {}).get(m, '-'):>10}",
        ]
        print(f"   {m:>12} " + " ".join(row))
    for case, b in plain.items():
        r = b["against_mean_field"]
        print(
            f"   {case}: {b['ticks']} ticks, dense {b['dense_field']}; mean ratio to the mean field {r['mean_ratio']:.3f} (min {r['min_ratio']:.3f}, max {r['max_ratio']:.3f}), total {r['total_observed']} / {r['total_predicted']:.1f}; mirror symmetric {b['mirror_symmetric']}; sign changes along y {b['along_y']['sign_changes']}"
        )
    if "inphase_equals_antiphase" in block:
        print(
            "   in phase against antiphase:",
            json.dumps(
                {k: v for k, v in block["inphase_equals_antiphase"].items() if k != "difference"}
            ),
        )
    for case, b in block.get("engine_against_dense", {}).items():
        print(
            f"   {case}: engine {b['engine_ticks']} ticks against dense through {b['engine_ticks']}: clicks identical {b['clicks_identical_through_96']}; viewer {b['viewer'] and b['viewer']['event_kinds']}"
        )
    for case, b in steer.items():
        print(
            f"   {case}: {b['ticks']} ticks, layers {b['layers']}; mirror symmetric {b['mirror_symmetric']}; sign changes along y {b['along_y']['sign_changes']}; sum {sum(b['quanta'].values())} against {None if b['without_coupling_through_same_ticks'] is None else sum(b['without_coupling_through_same_ticks'].values())} without the coupling; viewer {b['viewer'] and b['viewer']['event_kinds']}"
        )
        print(f"      light line {b['ledger_last'].get('light')}; bodies {b['external_body_totals']}")
    if "steer_inphase_against_antiphase" in block:
        print(
            "   steering, in phase against antiphase:",
            json.dumps(block["steer_inphase_against_antiphase"]),
        )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("runs", type=Path, help="the directory holding one run directory per case")
    parser.add_argument("--predictions", type=Path, default=HERE / "predictions.json")
    parser.add_argument("--record", type=Path, help="write the readings as JSON")
    args = parser.parse_args(argv)
    prediction = json.loads(args.predictions.read_text(encoding="utf-8"))
    summaries = {}
    for directory in sorted(p for p in args.runs.iterdir() if (p / "run.json").exists()):
        summaries[directory.name] = analyze(directory)
        s = summaries[directory.name]
        print(
            f"{directory.name}: {s['model']} {s['status']} {s['completed_ticks']} ticks"
            f" {s['elapsed_seconds']:.1f} s dense={s['dense_field']} clicks {s['click_count']}"
            f" ({s['click_quanta']} quanta) conserved={s['conserved_at_every_completed_tick']}"
            f" kinds={s['event_kinds']}"
        )
    p1 = part1(summaries, prediction)
    p2 = part2(summaries, prediction)
    print_part1(p1)
    print_part2(p2)
    if args.record:
        record = {"runs": summaries, "part1": p1, "part2": p2, "predictions": args.predictions.name}
        args.record.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
        print(f"\nwritten {args.record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
