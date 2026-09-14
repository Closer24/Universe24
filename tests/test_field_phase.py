"""Opt-in field-dependent phase: local field value selects an exact integer phase gate."""

import json
from copy import deepcopy

import pytest

from event_universe.diagnostics.node_contract import node_state_violations
from event_universe.initialization import parse_initial_state
from event_universe.integration.contact_program import MAX_FIELD_EXPONENT, FieldPhase
from event_universe.quantum import Amplitude, LocalUnitary
from event_universe.runner import run_initialization

from .test_causal_contact_fields import MIDDLE, SOURCE, causal_configuration
from .test_localized_quantum_contact import step, world_for

INVERSE = [[5, 0, 0, 0], [0, 3, 4, 0], [0, -4, 3, 0], [0, 0, 0, 5]]
SWAP = [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
COIL = [2, 2, 1]


def field_phase_configuration(coil_amount=400, *, divisor=25, coil=COIL, max_exponent=4):
    raw = causal_configuration()
    raw["ticks"] = 14
    raw["event_program"]["tickets"] = [0]
    for emission in raw["emissions"]:
        emission["budget"] = 1000
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
    domain = raw["event_program"]["domains"][0]
    domain["phases"] = [
        [{"register_indices": [0, 1], "matrix": domain["phases"][0][0]["matrix"]}],
        [
            {
                "register_indices": [1],
                "field_phase": {
                    "field": "vector_potential",
                    "divisor": divisor,
                    "vacuum": 5,
                    "unit": [3, 4],
                    "max_exponent": max_exponent,
                },
            }
        ],
        [{"register_indices": [0, 1], "matrix": INVERSE}],
        [{"register_indices": [1, 2], "matrix": SWAP}],
        *([[]] * 12),
    ]
    return raw


def output_decisions(resolver):
    return [
        (r.decision.tick, tuple(r.decision.weights))
        for r in resolver.space.records
        if r.decision.register_index == 2 and r.decision.weights[1]
    ]


def test_field_phase_table_is_exact_and_conjugate_for_negative_exponents():
    program = parse_initial_state(field_phase_configuration()).event_program
    assert program is not None
    from event_universe.integration.event_program import parse_event_program

    parsed = parse_event_program(parse_initial_state(field_phase_configuration()))
    assert parsed.contacts is not None
    rule = parsed.contacts.domains[0].phases[1][0][0]
    assert isinstance(rule, FieldPhase)
    assert rule.max_exponent == 4 and len(rule.matrices) == 9
    identity = rule.unitary(0)
    assert identity.matrix == ((Amplitude(1, 0), Amplitude(0, 0)), (Amplitude(0, 0), Amplitude(1, 0)))
    assert rule.unitary(1).matrix[1][1] == Amplitude(3, 4) and rule.unitary(1).matrix[0][0] == Amplitude(
        5, 0
    )
    assert rule.unitary(-1).matrix[1][1] == Amplitude(3, -4)
    assert rule.unitary(2).matrix[1][1] == Amplitude(-7, 24) and rule.unitary(2).matrix[0][
        0
    ] == Amplitude(25, 0)
    assert all(isinstance(m, LocalUnitary) for m in rule.matrices)
    assert rule.exponent(0) == 0 and rule.exponent(24) == 0 and rule.exponent(25) == 1
    assert rule.exponent(-49) == -1 and rule.exponent(100) == 4
    with pytest.raises(ValueError, match="exceeds"):
        rule.exponent(125)


@pytest.mark.parametrize(
    ("change", "match"),
    [
        (lambda fp: fp.update(unit=[3, 5]), "share one nonzero norm"),
        (lambda fp: fp.update(vacuum=0, unit=0), "share one nonzero norm"),
        (lambda fp: fp.update(divisor=0), "divisor"),
        (lambda fp: fp.update(max_exponent=MAX_FIELD_EXPONENT + 1), "limited to twelve"),
        (lambda fp: fp.update(field="charge"), "configured spatial field"),
        (lambda fp: fp.update(component=1), "outside the field"),
    ],
)
def test_invalid_field_phase_definitions_are_rejected(change, match):
    raw = field_phase_configuration()
    change(raw["event_program"]["domains"][0]["phases"][1][0]["field_phase"])
    with pytest.raises(ValueError, match=match):
        parse_initial_state(raw)


def test_field_phase_requires_the_causal_model_one_register_and_no_matrix():
    raw = field_phase_configuration()
    raw["event_program"]["model"] = "localized-contact-quantum-v1"
    with pytest.raises(ValueError, match="causal contact field model"):
        parse_initial_state(raw)
    raw = field_phase_configuration()
    raw["event_program"]["domains"][0]["phases"][1][0]["register_indices"] = [0, 1]
    with pytest.raises(ValueError, match="one register"):
        parse_initial_state(raw)
    raw = field_phase_configuration()
    raw["event_program"]["domains"][0]["phases"][1][0]["matrix"] = [[1, 0], [0, 1]]
    with pytest.raises(ValueError, match="exactly one matrix or field_phase"):
        parse_initial_state(raw)


@pytest.mark.parametrize(
    ("coil_amount", "exponent", "weights"),
    [(0, 0, None), (200, 0, None), (400, 1, (12745, 2880)), (800, 2, (160225, 230400))],
)
def test_local_field_at_the_schedule_tick_selects_the_phase_for_both_owners(
    coil_amount, exponent, weights
):
    world, resolver = world_for(field_phase_configuration(coil_amount))
    step(world, 3)
    choices = resolver.report()["field_phase_choices"]
    assert choices == [{"domain": "charge_mode", "epoch": 1, "register": 1, "exponent": exponent}]
    step(world, 5)
    decisions = output_decisions(resolver)
    if weights is None:
        assert decisions == []
    else:
        assert decisions == [(7, weights)]
    assert all(not node_state_violations(node) for node in resolver.source_nodes().values())
    assert all(value["balanced"] for value in world.spatial_accounting().values())


def test_a_field_on_the_other_side_does_not_reach_the_arm_gate():
    world, resolver = world_for(field_phase_configuration(400, coil=[1, 2, 1]))
    step(world, 8)
    assert resolver.report()["field_phase_choices"][0]["exponent"] == 0
    assert output_decisions(resolver) == []


def test_envelope_emission_follows_the_shifted_recombination():
    world, resolver = world_for(field_phase_configuration(400))
    step(world, 12)
    nodes = resolver.source_nodes()
    # The source port after the shifted recombination has weight 2549/3125.
    amplitude = nodes[SOURCE].amplitude
    weight = (amplitude.real**2 + amplitude.imag**2, amplitude.denominator**2)
    from fractions import Fraction

    assert Fraction(*weight) == Fraction(2549, 3125)
    assert nodes[MIDDLE].amplitude.real == nodes[MIDDLE].amplitude.imag == 0


def test_start_sources_without_field_values_is_rejected_when_a_field_phase_exists():
    world, resolver = world_for(field_phase_configuration(400))
    step(world, 1)
    with pytest.raises(ValueError, match="spatial field owner"):
        resolver.start_sources(2, None)


def test_headless_run_reports_choices_and_default_examples_are_unchanged(tmp_path):
    initial = tmp_path / "field_phase.json"
    initial.write_text(json.dumps(field_phase_configuration(800)), encoding="utf-8")
    run_initialization(initial, tmp_path / "run")
    report = json.loads((tmp_path / "run/run.json").read_text(encoding="utf-8"))
    resolver = report["computation"]["resolver"]
    assert resolver["field_phases"] == 1
    assert resolver["field_phase_choices"] == [
        {"domain": "charge_mode", "epoch": 1, "register": 1, "exponent": 2}
    ]
    assert report["accounting_balanced_at_every_completed_tick"]
    plain = deepcopy(causal_configuration())
    world, resolver = world_for(plain)
    assert resolver.report()["field_phases"] == 0 and resolver.report()["field_phase_choices"] == []
