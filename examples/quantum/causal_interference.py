"""Two-arm interference and which-path decoherence with a classical field source.

This is an experiment harness, not another evolution engine. Every measured
number comes from the canonical runner under ``causal-contact-fields-v1``:
capture weights from the quantum owner's records, and classical field emission
from the recorded ``spatial_envelope_source`` events. Analytic targets are
computed here with exact rational complex arithmetic, independently of the
update code, before the runs are read.

Layout: three Nodes on one line, S=(1,1,1), M=(2,1,1) and D=(3,1,1), which are
registers 0, 1 and 2 of one domain. A configured 3:4 mixer splits the wave
between S and M, a one-mode phase gate acts on M, the inverse mixer recombines,
and a SWAP moves the M port to D where a held detector attempts capture. The
which-path variant adds a second held detector at M, on the arm itself.
"""

import argparse
import json
import platform
import shutil
from fractions import Fraction
from pathlib import Path

from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import run_initialization, source_fingerprint

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "causal_charge.json"
ROTATION = [[5, 0, 0, 0], [0, 3, -4, 0], [0, 4, 3, 0], [0, 0, 0, 5]]
INVERSE = [[5, 0, 0, 0], [0, 3, 4, 0], [0, -4, 3, 0], [0, 0, 0, 5]]
SWAP = [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
# Phase gate coefficient on the occupied M mode: exp(i*phi) as an exact Gaussian integer.
PHASES = {"0": (1, 0), "pi/2": (0, 1), "pi": (-1, 0), "3pi/2": (0, -1)}
FULL_EMISSION = 25
TICKS = 14
RECOMBINED_TICKS = range(8, TICKS)
SOURCE, MIDDLE, DETECTOR = 1, 2, 3
NULL_TICKETS = [0, 0, 0]
CAPTURE_TICKET_AT_OUTPUT = [600]
CAPTURE_TICKET_ON_ARM = [9, 0, 0]


def analytic(phase):
    """Exact port weights after mixer, phase and inverse mixer, scaled to 625."""
    re, im = PHASES[phase]
    # Ports after the 3:4 mixer are (3/5, 4/5); the phase multiplies the M port.
    # The inverse mixer gives S = (9 + 16 e^{i phi}) / 25 and M = (-12 + 12 e^{i phi}) / 25.
    s_re, s_im = 9 + 16 * re, 16 * im
    m_re, m_im = -12 + 12 * re, 12 * im
    weight_s = s_re * s_re + s_im * s_im
    weight_m = m_re * m_re + m_im * m_im
    assert weight_s + weight_m == 625
    return {
        "output_port_weights": [weight_s, weight_m],
        "capture_probability": str(Fraction(weight_m, 625)),
        "source_emission_after_recombination": str(Fraction(FULL_EMISSION * weight_s, 625)),
    }


def configuration(phase, *, which_path, tickets):
    raw = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    raw["ticks"] = TICKS
    for emission in raw["emissions"]:
        emission["budget"] = 1000
    program = raw["event_program"]
    program["tickets"] = list(tickets)
    domain = program["domains"][0]
    re, im = PHASES[phase]
    coefficient = re if im == 0 else [re, im]
    domain["phases"] = [
        [{"register_indices": [0, 1], "matrix": ROTATION}],
        [{"register_indices": [1], "matrix": [[1, 0], [0, coefficient]]}],
        [{"register_indices": [0, 1], "matrix": INVERSE}],
        [{"register_indices": [1, 2], "matrix": SWAP}],
        *([[]] * 12),
    ]
    if which_path:
        domain["capture"]["register_indices"] = [1, 2]
        raw["seeds"].append({"position": [2, 1, 1], "type": "contact_probe"})
    return raw


def emission_by_tick(events_path):
    table = {}
    for line in events_path.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event["event"] == "spatial_envelope_source":
            amount = event["source_delta"].get("electric_signal", [0])[0]
            table.setdefault(event["tick"], {})[event["position"][0]] = -amount
    return table


def run_case(name, raw, output):
    case_dir = output / name
    if case_dir.exists():
        shutil.rmtree(case_dir)
    output.mkdir(parents=True, exist_ok=True)
    initialization = output / (name + ".json")
    initialization.write_text(json.dumps(raw, indent=1) + "\n", encoding="utf-8")
    run_initialization(initialization, case_dir)
    report = json.loads((case_dir / "run.json").read_text(encoding="utf-8"))
    assert report["status"] == "completed", report["error"]
    assert report["accounting_balanced_at_every_completed_tick"]
    assert report["conserved_at_every_completed_tick"]
    resolver = report["computation"]["resolver"]
    decisions = [
        {
            "tick": record["decision"]["tick"],
            "register": record["decision"]["register_index"],
            "weights": record["decision"]["weights"],
            "outcome": record["outcome"],
        }
        for record in resolver["records"]
        if record["decision"]["weights"][1] != 0
    ]
    emission = emission_by_tick(case_dir / "events.jsonl")
    return {
        "name": name,
        "uncertain_decisions": decisions,
        "captures": [
            {"tick": t["tick"], "x": t["address"][0]}
            for t in resolver["contact_transfers"]
            if t["direction"] == "to_localized"
        ],
        "emission_by_tick": {str(tick): emission[tick] for tick in sorted(emission)},
        "source_emission_total": -report["source_totals"]["electric_signal"][0],
        "random_draws": resolver["random_draws"],
    }


def steady_source_emission(case):
    """Mean classical emission at S per tick after recombination, as a string."""
    total = sum(case["emission_by_tick"].get(str(t), {}).get(SOURCE, 0) for t in RECOMBINED_TICKS)
    return str(Fraction(total, len(RECOMBINED_TICKS)))


def run_experiment(output):
    interference = []
    for phase in PHASES:
        case = run_case(
            "interference_" + phase.replace("/", "_"),
            configuration(phase, which_path=False, tickets=NULL_TICKETS),
            output,
        )
        expected = analytic(phase)
        output_decisions = [d for d in case["uncertain_decisions"] if d["register"] == 2]
        measured = output_decisions[0]["weights"] if output_decisions else [1, 0]
        if expected["output_port_weights"][1] == 0:
            assert not output_decisions, "no uncertain output decision when interference is complete"
        else:
            assert len(output_decisions) == 1 and measured == expected["output_port_weights"]
        steady = Fraction(steady_source_emission(case))
        predicted = Fraction(expected["source_emission_after_recombination"])
        assert abs(steady - predicted) * len(RECOMBINED_TICKS) < 1, (steady, predicted)
        assert case["captures"] == [] and case["random_draws"] == (1 if output_decisions else 0)
        interference.append(
            {
                "phase": phase,
                "analytic": expected,
                "measured_output_weights": measured,
                "output_decision_tick": output_decisions[0]["tick"] if output_decisions else None,
                "measured_source_emission_after_recombination": str(steady),
                "case": case,
            }
        )

    localized = run_case(
        "interference_pi_capture",
        configuration("pi", which_path=False, tickets=CAPTURE_TICKET_AT_OUTPUT),
        output,
    )
    assert localized["captures"] == [{"tick": 7, "x": DETECTOR}]
    after = {int(t): row for t, row in localized["emission_by_tick"].items() if int(t) > 7}
    assert all(row.get(MIDDLE, 0) == 0 and row.get(DETECTOR, 0) == 0 for row in after.values())
    cancellation_ticks = sorted(t for t, row in after.items() if row.get(SOURCE, 0))
    assert cancellation_ticks == [8], cancellation_ticks

    which_path = []
    for phase in PHASES:
        for label, tickets in (("null", NULL_TICKETS), ("capture", CAPTURE_TICKET_ON_ARM)):
            case = run_case(
                "which_path_" + phase.replace("/", "_") + "_" + label,
                configuration(phase, which_path=True, tickets=tickets),
                output,
            )
            arm = [d for d in case["uncertain_decisions"] if d["register"] == 1]
            assert arm and arm[0]["tick"] == 1 and arm[0]["weights"] == [9, 16]
            assert not [d for d in case["uncertain_decisions"] if d["register"] == 2]
            if label == "capture":
                assert case["captures"] == [{"tick": 1, "x": MIDDLE}]
            else:
                assert case["captures"] == []
                retarded = case["emission_by_tick"]["2"]
                assert retarded == {SOURCE: 9, MIDDLE: 0}, retarded
            which_path.append(
                {
                    "phase": phase,
                    "arm_ticket": label,
                    "arm_decision_weights": arm[0]["weights"],
                    "later_arm_decisions": [d["weights"] for d in arm[1:]],
                    "captures": case["captures"],
                    "source_emission_after_arm_null": (
                        case["emission_by_tick"]["2"][SOURCE] if label == "null" else None
                    ),
                    "case": case,
                }
            )

    return {
        "status": "pass",
        "python": platform.python_version(),
        "source_sha256": source_fingerprint(),
        "profile": "causal-contact-fields-v1",
        "template": TEMPLATE.name,
        "ticks": TICKS,
        "interference": interference,
        "localized_capture_at_output": localized,
        "which_path": which_path,
        "retarded_source_fraction_after_arm_null": str(Fraction(9, FULL_EMISSION)),
        "limits": [
            "Integer 3:4 mixer, not a balanced beam splitter; visibility follows from 9/25 and 16/25.",
            "Source weights after a null result are retarded and unnormalized: S keeps emitting 9 of 25.",
            "One configured domain and one conserved inventory; no field back-action on amplitudes.",
            "Finite range of ticks and one Link per tick; no continuum limit is measured.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    validate_output_path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("use a new or empty output directory")
    out.mkdir(parents=True, exist_ok=True)
    summary = out / "summary.json"
    summary.touch()
    with ArtifactLease(out, [summary]):
        result = run_experiment(out)
        summary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": result["status"],
                "output": str(out),
                "interference_weights": {
                    row["phase"]: row["measured_output_weights"] for row in result["interference"]
                },
                "source_sha256": result["source_sha256"],
            }
        )
    )


if __name__ == "__main__":
    main()
