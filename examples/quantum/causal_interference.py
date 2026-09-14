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
# A balanced splitter: Hadamard block with vacuum coefficient 1+i, so U*U = 2I exactly.
BALANCED = [[[1, 1], 0, 0, 0], [0, 1, 1, 0], [0, 1, -1, 0], [0, 0, 0, [1, 1]]]
SPLITTERS = {"rotation": (ROTATION, INVERSE), "balanced": (BALANCED, BALANCED)}
# Phase gate coefficient on the occupied M mode: exp(i*phi) as an exact Gaussian integer.
PHASES = {"0": (1, 0), "pi/2": (0, 1), "pi": (-1, 0), "3pi/2": (0, -1)}
FULL_EMISSION = 25
TICKS = 14
RECOMBINED_TICKS = range(8, TICKS)
SOURCE, MIDDLE, DETECTOR = 1, 2, 3
NULL_TICKETS = [0, 0, 0]
CAPTURE_TICKET_AT_OUTPUT = [600]
CAPTURE_TICKET_ON_ARM = [9, 0, 0]


def analytic(phase, splitter="rotation"):
    """Exact port weights after mixer, phase and inverse mixer, scaled to 625 or 4."""
    re, im = PHASES[phase]
    if splitter == "balanced":
        # Ports after the Hadamard are equal; the second Hadamard gives
        # S = (1 + e^{i phi}) / 2 and M = (1 - e^{i phi}) / 2 up to a common phase.
        s_re, s_im = 1 + re, im
        m_re, m_im = 1 - re, -im
        weight_s = s_re * s_re + s_im * s_im
        weight_m = m_re * m_re + m_im * m_im
        assert weight_s + weight_m == 4
        return {
            "output_port_weights": [weight_s, weight_m],
            "capture_probability": str(Fraction(weight_m, 4)),
            "source_emission_after_recombination": str(Fraction(FULL_EMISSION * weight_s, 4)),
        }
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


COIL = [2, 2, 1]
COIL_CONTROL = [1, 2, 1]


def gaussian_power(base, exponent):
    real, imag = 1, 0
    for _ in range(exponent):
        real, imag = real * base[0] - imag * base[1], real * base[1] + imag * base[0]
    return real, imag


def analytic_field_phase(exponent):
    """Port weights after the 3:4 interferometer with M phase ((3+4i)/5)^n, scaled to 625*25^n."""
    a, b = gaussian_power((3, 4), exponent)
    scale = 5**exponent
    total = 625 * scale * scale
    weight_m = 144 * ((a - scale) ** 2 + b * b)
    return {"output_port_weights": [total - weight_m, weight_m], "exponent": exponent}


def field_phase_configuration(coil_amount, *, coil=COIL, divisor=25):
    """The rotation interferometer whose M phase is read from an external coil field."""
    raw = configuration("0", which_path=False, tickets=NULL_TICKETS)
    raw["fields"].append(
        {
            "name": "vector_potential",
            "components": 1,
            "units": "potential unit",
            "signed": True,
            "conserved": True,
        }
    )
    raw["disturbance_types"].append(
        {
            "name": "coil",
            "fields": ["vector_potential"],
            "defaults": {"vector_potential": 0},
            "transport": {"mode": "hold"},
        }
    )
    raw["spatial_fields"].append(
        {
            "field": "vector_potential",
            "baseline": 0,
            "transport": "outward",
            "decay": {"retain_numerator": 1, "retain_denominator": 2},
        }
    )
    raw["emissions"].append(
        {
            "type": "coil",
            "field": "vector_potential",
            "amount": coil_amount,
            "source": True,
            "budget": 100000,
        }
    )
    if coil_amount:
        raw["seeds"].append({"position": list(coil), "type": "coil"})
    raw["event_program"]["domains"][0]["phases"][1] = [
        {
            "register_indices": [1],
            "field_phase": {
                "field": "vector_potential",
                "divisor": divisor,
                "vacuum": 5,
                "unit": [3, 4],
                "max_exponent": 4,
            },
        }
    ]
    return raw


FUNDED_STOCK = 3000
FUNDED_BUDGET = 1000


def funded_configuration(phase, *, tickets):
    """The rotation interferometer whose classical field is paid from the wave's own stock."""
    raw = configuration(phase, which_path=False, tickets=tickets)
    for kind in raw["disturbance_types"]:
        if kind["name"] in ("incoming_charge", "localized_charge"):
            kind["fields"].append("electric_signal")
            kind["defaults"]["electric_signal"] = FUNDED_STOCK
    for emission in raw["emissions"]:
        emission["source"] = False
        emission["budget"] = FUNDED_BUDGET
        emission["amount"] = FULL_EMISSION
    return raw


SCALE_AMOUNTS = (25, 250, 2500, 25000)


def scale_configuration(phase, amount):
    """The plain interferometer with the full source emission raised to `amount` per tick."""
    raw = configuration(phase, which_path=False, tickets=NULL_TICKETS)
    for emission in raw["emissions"]:
        emission["amount"] = -amount
        emission["budget"] = amount * 40
    return raw


def configuration(phase, *, which_path, tickets, splitter="rotation", null_notices=False):
    raw = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    mixer, inverse = SPLITTERS[splitter]
    raw["ticks"] = TICKS
    for emission in raw["emissions"]:
        emission["budget"] = 1000
    program = raw["event_program"]
    program["tickets"] = list(tickets)
    if null_notices:
        program["null_notices"] = True
    domain = program["domains"][0]
    re, im = PHASES[phase]
    coefficient = re if im == 0 else [re, im]
    domain["phases"] = [
        [{"register_indices": [0, 1], "matrix": mixer}],
        [{"register_indices": [1], "matrix": [[1, 0], [0, coefficient]]}],
        [{"register_indices": [0, 1], "matrix": inverse}],
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
    escaped = -report["escaped_totals"]["electric_signal"][0]
    any_escape = any(any(values) for values in report["escaped_totals"].values())
    # The strict flag requires that nothing left the open boundary; escape is
    # accounted separately and does not change any decision or emission.
    assert report["conserved_at_every_completed_tick"] or any_escape
    assert report["final_totals"]["charge"] == [-1] and report["final_totals"]["mass"] == [1]
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
        "escaped_total": escaped,
        "random_draws": resolver["random_draws"],
        "final_weight_scales": {
            str(e["position"][0]): e["weight_scale"] for e in resolver["source_envelopes"]
        },
        "field_phase_choices": resolver.get("field_phase_choices", []),
        "funded_emission": resolver.get("funded_emission", {}),
        "quantum_inventory": resolver.get("quantum_inventory", {}),
        "source_totals": report["source_totals"],
        "final_totals": report["final_totals"],
        "conserved": report["conserved_at_every_completed_tick"],
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

    balanced = []
    for phase in PHASES:
        case = run_case(
            "balanced_" + phase.replace("/", "_"),
            configuration(phase, which_path=False, tickets=NULL_TICKETS, splitter="balanced"),
            output,
        )
        expected = analytic(phase, "balanced")
        output_decisions = [d for d in case["uncertain_decisions"] if d["register"] == 2]
        if expected["output_port_weights"][1] == 0:
            assert not output_decisions
            probability = Fraction(0)
        else:
            assert len(output_decisions) == 1
            weights = output_decisions[0]["weights"]
            probability = Fraction(weights[1], sum(weights))
        assert probability == Fraction(expected["capture_probability"])
        steady = Fraction(steady_source_emission(case))
        predicted = Fraction(expected["source_emission_after_recombination"])
        assert abs(steady - predicted) * len(RECOMBINED_TICKS) < 1, (steady, predicted)
        arms = case["emission_by_tick"]["1"]
        assert arms == {SOURCE: 12, MIDDLE: 12}, arms
        balanced.append(
            {
                "phase": phase,
                "analytic": expected,
                "measured_capture_probability": str(probability),
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

    # Opt-in causal null notices: the same which-path and output-null runs, with
    # the null Node's factor 1/(1-p) carried through Links to the other envelopes.
    notices = []
    for phase in ("0", "pi"):
        case = run_case(
            "notices_which_path_" + phase.replace("/", "_"),
            configuration(phase, which_path=True, tickets=NULL_TICKETS, null_notices=True),
            output,
        )
        arm = [d for d in case["uncertain_decisions"] if d["register"] == 1]
        assert [d["weights"] for d in arm] == [[9, 16], [9, 16]] and [d["tick"] for d in arm] == [1, 5]
        emission = case["emission_by_tick"]
        assert [emission[str(t)][SOURCE] for t in (2, 3, 4)] == [FULL_EMISSION] * 3, emission
        assert emission["5"] == {SOURCE: 9, MIDDLE: 16}, emission["5"]
        assert [emission[str(t)][SOURCE] for t in range(6, TICKS)] == [FULL_EMISSION] * (TICKS - 6)
        assert case["final_weight_scales"] == {"1": [625, 81], "2": [625, 81], "3": [625, 81]}
        notices.append({"phase": phase, "variant": "arm_null", "case": case})
    case = run_case(
        "notices_output_null_pi_2",
        configuration("pi/2", which_path=False, tickets=NULL_TICKETS, null_notices=True),
        output,
    )
    decisions = [d for d in case["uncertain_decisions"] if d["register"] == 2]
    assert len(decisions) == 1 and decisions[0]["weights"] == [337, 288] and decisions[0]["tick"] == 7
    emission = case["emission_by_tick"]
    assert emission["8"][SOURCE] == 13 and all(emission[str(t)][SOURCE] == 25 for t in range(9, TICKS))
    assert case["final_weight_scales"] == {"1": [625, 337], "2": [625, 337], "3": [625, 337]}
    notices.append({"phase": "pi/2", "variant": "output_null", "case": case})

    # Opt-in field-dependent phase: an external coil field on the M arm selects
    # the phase ((3+4i)/5)^n at the gate's schedule tick, n = floor(value / 25).
    back_action = []
    for label, amount, coil in (
        ("no_coil", 0, COIL),
        ("coil_200", 200, COIL),
        ("coil_400", 400, COIL),
        ("coil_800", 800, COIL),
        ("coil_400_control", 400, COIL_CONTROL),
    ):
        case = run_case("field_phase_" + label, field_phase_configuration(amount, coil=coil), output)
        choices = case["field_phase_choices"]
        assert len(choices) == 1 and choices[0]["epoch"] == 1, choices
        exponent = choices[0]["exponent"]
        expected = analytic_field_phase(exponent)
        decisions = [d for d in case["uncertain_decisions"] if d["register"] == 2]
        if expected["output_port_weights"][1] == 0:
            assert not decisions
            measured = expected["output_port_weights"]
        else:
            assert len(decisions) == 1 and decisions[0]["weights"] == expected["output_port_weights"]
            measured = decisions[0]["weights"]
        total = sum(measured)
        steady = Fraction(steady_source_emission(case))
        predicted = Fraction(FULL_EMISSION * measured[0], total)
        assert abs(steady - predicted) * len(RECOMBINED_TICKS) < 1, (steady, predicted)
        back_action.append(
            {
                "label": label,
                "coil_amount": amount,
                "coil": coil,
                "exponent": exponent,
                "analytic": expected,
                "measured_output_weights": measured,
                "capture_probability": str(Fraction(measured[1], total)),
                "measured_source_emission_after_recombination": str(steady),
                "case": case,
            }
        )
    assert [row["exponent"] for row in back_action] == [0, 0, 1, 2, 0]

    # Opt-in funded emission: the wave's own conserved stock pays for the field.
    funded = []
    for label, tickets in (("null", NULL_TICKETS), ("capture", CAPTURE_TICKET_AT_OUTPUT)):
        case = run_case("funded_pi_" + label, funded_configuration("pi", tickets=tickets), output)
        ledger = case["funded_emission"]["charge_mode"]
        paid = ledger["paid"]["electric_signal"][0]
        residual = ledger["after_capture"]["electric_signal"][0]
        assert case["conserved"], case["name"]
        assert case["source_totals"]["electric_signal"] == [residual]
        assert case["final_totals"]["electric_signal"] == [FUNDED_STOCK + residual]
        if label == "null":
            assert residual == 0 and case["captures"] == []
            assert case["quantum_inventory"]["electric_signal"] == [FUNDED_STOCK - paid]
        else:
            assert case["captures"] == [{"tick": 7, "x": DETECTOR}] and residual > 0
            assert case["quantum_inventory"]["electric_signal"] == [0]
        funded.append(
            {
                "variant": label,
                "paid_by_wave": paid,
                "residual_after_capture": residual,
                "final_total": case["final_totals"]["electric_signal"][0],
                "case": case,
            }
        )

    # Emission scale: the classical field follows the local squared weight to within
    # one unit per tick at every scale, so the relative departure falls as 1/amount.
    scale = []
    for phase in ("pi/2", "pi"):
        weights = analytic(phase)["output_port_weights"]
        weight = Fraction(weights[0], sum(weights))
        for amount in SCALE_AMOUNTS:
            case = run_case(
                f"scale_{amount}_" + phase.replace("/", "_"), scale_configuration(phase, amount), output
            )
            per_tick = [
                case["emission_by_tick"].get(str(t), {}).get(SOURCE, 0) for t in RECOMBINED_TICKS
            ]
            exact = amount * weight
            deviation = max(abs(value - exact) for value in per_tick)
            mean = Fraction(sum(per_tick), len(per_tick))
            assert deviation < 1, (amount, phase, per_tick)
            assert abs(mean - exact) * len(RECOMBINED_TICKS) < 1
            scale.append(
                {
                    "phase": phase,
                    "amount": amount,
                    "source_emission_per_tick": per_tick,
                    "exact_source_emission": str(exact),
                    "mean_source_emission": str(mean),
                    "max_deviation_per_tick": str(deviation),
                    "relative_deviation_of_mean": str(abs(mean - exact) / exact),
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
        "balanced": balanced,
        "localized_capture_at_output": localized,
        "which_path": which_path,
        "retarded_source_fraction_after_arm_null": str(Fraction(9, FULL_EMISSION)),
        "null_notices": notices,
        "field_phase": back_action,
        "funded": funded,
        "scale": scale,
        "limits": [
            "The 3:4 mixer gives visibility from 9/25 and 16/25; the balanced Hadamard with vacuum 1+i gives full visibility.",
            "Without null notices the source weights after a null are retarded and unnormalized: S keeps emitting 9 of 25.",
            "With null notices the factor 1/(1-p) reaches the other envelopes after Link transit; exact for one excitation.",
            "One configured domain and one conserved inventory.",
            "Field back-action is a configured local phase on one arm; it transfers no energy or momentum to the field.",
            "With funded emission the field is paid from the wave's stock; emission committed after a remote capture is an explicit external residual.",
            "Raising the emission amount shows the field converging to the exact squared weight within one unit per tick; it does not show the dynamics of the wave becoming classical.",
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
