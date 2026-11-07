"""Prospective finite signal/click-correlation audit; no model modifications.

Run with python -m research.light_approval.compute --output PATH.
The protocol is fixed before any recorded evolution. All choices are initial data.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

from research.experiments.run import run_experiment
from research.presenter.build import build
from research.presenter.export import bundle, write_bundle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / "protocol.json"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def cases(protocol):
    for phase, x, y in itertools.product(range(4), range(2), range(2)):
        yield dict(id=f"shared-{phase}-{x}{y}", ensemble="shared_phase", phases=[phase, phase], settings=[x, y], present=True)
    for phase_a, phase_b, x, y in itertools.product(range(4), range(4), range(2), range(2)):
        yield dict(id=f"independent-{phase_a}-{phase_b}-{x}{y}", ensemble="independent_phases", phases=[phase_a, phase_b], settings=[x, y], present=True)
    for x, y in itertools.product(range(2), range(2)):
        yield dict(id=f"null-{x}{y}", ensemble="null", phases=[0, 0], settings=[x, y], present=False)


def spec_for(protocol, case):
    components = []
    for index, name in enumerate(("A", "B")):
        receiver = protocol["apparatus"]["receivers"][name]
        source = [receiver[0] - 8, receiver[1], receiver[2]]
        a, b = protocol["apparatus"]["source_phases"][case["phases"][index]]
        pair = protocol["apparatus"]["local_setting_receiver_remainders"][case["settings"][index]]
        components.extend([
            {"name": f"{name}-guide", "recipe": "GuideSegment", "at": receiver,
             "params": {"start": -8, "stop": 0, "sockets": [-8, 0], "remainder_pair": [4, 0]}},
            {"name": f"{name}-receiver", "recipe": "Receiver", "at": receiver,
             "params": {"remainders": pair}},
            {"name": f"{name}-source", "recipe": "SignalSource", "at": source,
             "params": {"a": a, "b": b, "present": case["present"]}},
        ])
    return {
        "format": "universe24-assembly-experiment-v1", "id": case["id"],
        "title": "Prepared signal approval audit: " + case["id"],
        "description": "Two local initial apparatuses on one unchanged Rule3 board. Settings are prepared receiver remainders, not physical polarization axes. Shared source phases are a designed common cause. Full records include no-click trials.",
        "question": protocol["question"], "board": protocol["board"], "components": components,
        "steps": protocol["steps"], "detectors": ["A-receiver.node", "B-receiver.node"],
        "view": {"port": "A-receiver.memory"},
        "controls": case,
        "provenance": {"protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(), "case": case},
        "budget": {"max_frames": 17, "max_cells": 500000, "max_bytes": 67108864, "max_seconds": 60},
    }


def local_trace(experiment, position):
    background = tuple(map(int, experiment["background"]))
    result = []
    for frame in experiment["frames"]:
        cells = {tuple(row[:4]): tuple(map(int, row[4:])) for row in frame["cells"]}
        result.append([list(cells.get((*position, g), background)) for g in range(48)])
    return result


def observe(trace):
    all_clicks = []
    for step, (old, new) in enumerate(zip(trace, trace[1:]), 1):
        for channel in range(48):
            ell = new[channel][1] + old[channel][0]
            if ell and old[channel] != new[channel]:
                all_clicks.append({"step": step, "channel": channel, "ell": ell})
    primary = [row for row in all_clicks if row["channel"] == 0]
    first = primary[0] if primary else None
    magnitudes = [row[0][0]**2 + row[0][1]**2 for row in trace]
    remainders = [[row[0][2], row[14][2]] for row in trace]
    start = first["step"] if first else None
    return {
        "outcome": (1 if first["ell"] > 0 else -1) if first else 0,
        "first_click": first, "primary_clicks": primary, "all48_clicks": all_clicks,
        "I": magnitudes, "remainder_pairs": remainders,
        "I_constant_after_first": bool(first) and len(set(magnitudes[start:])) == 1,
        "remainder_pair_constant_after_first": bool(first) and len({tuple(v) for v in remainders[start:]}) == 1,
        "later_primary_clicks": len(primary) - bool(primary),
        "detector_trace_sha256": digest(trace),
    }


def rational(numerator, denominator):
    return str(Fraction(numerator, denominator)) if denominator else None


def statistics(rows, name):
    selected = [row for row in rows if row["case"]["ensemble"] == name]
    table, raw_e, conditional_e = {}, {}, {}
    for x, y in itertools.product(range(2), repeat=2):
        sample = [row for row in selected if row["case"]["settings"] == [x, y]]
        values = [(r["A"]["outcome"], r["B"]["outcome"]) for r in sample]
        detected = [(a, b) for a, b in values if a and b]
        key = f"{x}{y}"
        raw_e[key] = Fraction(sum(a*b for a, b in values), len(values))
        conditional_e[key] = Fraction(sum(a*b for a, b in detected), len(detected)) if detected else None
        counts = Counter(values)
        table[key] = {
            "trials": len(values), "E_all": str(raw_e[key]),
            "E_both_clicked": str(conditional_e[key]) if conditional_e[key] is not None else None,
            "detection_A": rational(sum(bool(a) for a, b in values), len(values)),
            "detection_B": rational(sum(bool(b) for a, b in values), len(values)),
            "joint_detection": rational(len(detected), len(values)),
            "joint_outcome_counts": {f"{a},{b}": counts.get((a, b), 0) for a, b in itertools.product((-1, 0, 1), repeat=2)},
            "marginal_A": {str(k): rational(sum(a == k for a, b in values), len(values)) for k in (-1, 0, 1)},
            "marginal_B": {str(k): rational(sum(b == k for a, b in values), len(values)) for k in (-1, 0, 1)},
        }
    signs = {"00": 1, "01": 1, "10": 1, "11": -1}
    s = abs(sum(signs[k]*raw_e[k] for k in signs))
    conditioned = abs(sum(signs[k]*conditional_e[k] for k in signs)) if all(v is not None for v in conditional_e.values()) else None
    return {"setting_pairs": table, "CHSH_all_trials": str(s),
            "CHSH_both_clicked": str(conditioned) if conditioned is not None else None,
            "all_trials_bound_2_satisfied": s <= 2}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    started, cpu = time.monotonic(), time.process_time()
    protocol_bytes = PROTOCOL.read_bytes()
    protocol = json.loads(protocol_bytes)
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "records").mkdir()
    (args.output / "protocol.json").write_bytes(protocol_bytes)
    planned = list(cases(protocol))
    assert len(planned) == protocol["budget"]["max_engine_runs"] == 84
    sources = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
               for folder in (ROOT/"universe24", ROOT/"research/components", ROOT/"research/presenter")
               for p in sorted(folder.glob("**/*.py"))}
    sources[str(Path(__file__).relative_to(ROOT))] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    registration = {"protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
                    "planned_cases": planned, "source_sha256": sources,
                    "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()}
    write_json(args.output / "registration.json", registration)
    rows, display, signatures = [], [], defaultdict(list)
    for number, case in enumerate(planned):
        if time.process_time()-cpu > protocol["budget"]["max_cpu_seconds"] or time.monotonic()-started > protocol["budget"]["max_wall_seconds"]:
            write_json(args.output / "failure.json", {"reason": "Registered study budget exhausted", "completed_runs": len(rows)})
            raise RuntimeError("Registered study budget exhausted")
        spec = spec_for(protocol, case)
        result = run_experiment(spec)
        experiment = result["experiment"]
        traces = {party: local_trace(experiment, protocol["apparatus"]["receivers"][party]) for party in ("A", "B")}
        observations = {party: observe(trace) for party, trace in traces.items()}
        record = {"case": case, "spec": spec, "assembly": result["assembly"],
                  "experiment": experiment, "detector_traces": traces, "observations": observations,
                  "detector_input_traces": {party: [row["next_input"] for row in result["observations"][party + "-receiver.node"]["trace"]] for party in ("A", "B")}}
        path = args.output / "records" / (case["id"] + ".json.gz")
        payload = canonical(record).encode()
        path.write_bytes(gzip.compress(payload, mtime=0))
        row = {"case": case, **observations, "record": str(path.relative_to(args.output)),
               "record_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
               "initial_state_sha256": experiment["frames"][0]["state_sha256"],
               "final_state_sha256": experiment["frames"][-1]["state_sha256"],
               "frames": len(experiment["frames"]), "full_rewind_equal": experiment["provenance"]["full_rewind_equal"]}
        rows.append(row)
        signatures[row["initial_state_sha256"]].append([frame["state_sha256"] for frame in experiment["frames"]])
        if case["id"] in protocol["presenter_cases"]:
            display.append(experiment)
        print(f"{number+1:02d}/84 {case['id']} outcomes={observations['A']['outcome']},{observations['B']['outcome']}", flush=True)
    assert PROTOCOL.read_bytes() == protocol_bytes
    for name, expected in sources.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected
    remote_checks = []
    for party, remote_index, local_index in (("A", 1, 0), ("B", 0, 1)):
        groups = defaultdict(list)
        for row in rows:
            case = row["case"]
            groups[(case["ensemble"], tuple(case["phases"]), case["settings"][local_index], case["present"])].append(row[party]["detector_trace_sha256"])
        remote_checks.extend(len(set(values)) == 1 for values in groups.values())
    clicked = [row[p] for row in rows if row["case"]["ensemble"] != "null" for p in ("A", "B") if row[p]["first_click"]]
    result = {
        "schema": "universe24-light-approval-result-v1", "protocol_sha256": registration["protocol_sha256"],
        "base_commit": registration["base_commit"], "source_sha256": sources,
        "engine_runs": len(rows), "complete_states": sum(row["frames"] for row in rows),
        "forward_inverse_transitions": len(rows)*protocol["steps"],
        "all_full_rewinds_equal": all(row["full_rewind_equal"] for row in rows),
        "duplicate_preparations_exactly_reproduced": all(all(value == values[0] for value in values) for values in signatures.values()),
        "remote_setting_full_detector_trace_invariance": all(remote_checks),
        "remote_setting_comparisons": len(remote_checks),
        "null_receivers_all48_no_C": all(not row[p]["all48_clicks"] for row in rows if row["case"]["ensemble"] == "null" for p in ("A", "B")),
        "source_on_detected_receiver_runs": len(clicked),
        "no_primary_C_before_distance8": all(item["first_click"]["step"] >= 8 for item in clicked),
        "finite_I_record_constant_after_first": sum(item["I_constant_after_first"] for item in clicked),
        "finite_remainder_record_constant_after_first": sum(item["remainder_pair_constant_after_first"] for item in clicked),
        "receiver_runs_with_later_primary_C": sum(item["later_primary_clicks"] > 0 for item in clicked),
        "statistics": {name: statistics(rows, name) for name in ("shared_phase", "independent_phases", "null")},
        "cases": rows, "physical_entanglement_established": False,
        "seconds": time.monotonic()-started, "cpu_seconds": time.process_time()-cpu,
        "limits": ["Prepared finite family only", "Source phases are a designed common cause", "Local settings are not derived polarization analyzers", "First-click sign is not a proven internal persistent signed record", "Conditioned CHSH is a selection diagnostic", "No emergent all-alternatives exploration or quantum measurement derivation"]}
    write_json(args.output / "result.json", result)
    display.sort(key=lambda e: protocol["presenter_cases"].index(e["id"]))
    write_bundle(args.output / "experiments.json", bundle(display, title="Light approval research — prepared correlations"))
    build(args.output / "experiments.json", args.output / "The_Presenter.html")
    print(canonical({k: v for k, v in result.items() if k not in ("cases", "source_sha256", "statistics")}))
    print(canonical({name: {k: v for k, v in data.items() if k != "setting_pairs"} for name, data in result["statistics"].items()}))


if __name__ == "__main__":
    main()
