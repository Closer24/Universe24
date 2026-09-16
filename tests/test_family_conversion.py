"""Energy-dependent family conversion on the generic N-to-M contract.

The configurations in examples/family-conversion/build.py are supplied discrete
kinematics declared between catalog families through ``participants`` and
``outputs`` and decided by the participants' energies. Passing these checks
shows exact integer accounting of the declared laws, not quantum
electrodynamics. Expected values were written in expectations.json before the
first run. The generic arity, Port, capacity and invariant cases use the
stock/momentum probe world so no physical name is involved.
"""

import importlib.util
import json
from fractions import Fraction
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.configuration_validation import validate_configuration
from event_universe.core.disturbance_state import MAX_VALUE
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "examples" / "family-conversion"
SPEC = importlib.util.spec_from_file_location("family_conversion_build", HERE / "build.py")
build = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(build)
EXPECTED = json.loads((HERE / "expectations.json").read_text(encoding="utf-8"))
PROBE = ROOT / "examples/known-entities/conversion.json"
NODE = [8, 3, 3]
UNITS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]


def records(world):
    """Every owned record: (position or 'link', type name, values)."""
    names = [kind.name for kind in world.initial.disturbances]
    found = [
        (position, names[r.type_index], world.record_values(r))
        for position, node in world.nodes.items()
        for r in node.records
        if r is not None
    ]
    found += [
        ("link", names[p.record.type_index], world.record_values(p.record))
        for packets in world.links.values()
        for p in packets
        if p is not None
    ]
    return sorted(found, key=repr)


def run(document, ticks=None):
    """Step a world, checking closed accounting (totals plus escaped) at every tick."""
    events = []
    world = Simulation(parse_initial_state(document), observer=events.append)
    initial = world.totals()
    for _ in range(document["ticks"] if ticks is None else ticks):
        world.step()
        totals, escaped = world.totals(), world.escaped_totals()
        assert all(
            tuple(a + b for a, b in zip(totals[name], escaped[name], strict=True)) == initial[name]
            for name in initial
        )
        assert world.source_totals() == {name: (0,) * len(v) for name, v in initial.items()}
    if "conservation" in document:
        assert world.conservation_report()["status"] == "passed"
    return world, events


def sent(events, tick, position=NODE):
    return [
        (
            e["disturbance"],
            e["values"]["energy"][0],
            list(e["values"]["momentum"]),
            e["values"]["charge"][0],
            e["port"],
        )
        for e in events
        if e["event"] == "sent"
        and e["tick"] == tick
        and (position is None or tuple(e["position"]) == tuple(position))
    ]


def escapes(events):
    return sorted(
        (e["tick"], e["disturbance"], e["values"]["energy"][0])
        for e in events
        if e["event"] == "escaped"
    )


def cycle_at(events, tick, position=NODE):
    return next(
        e
        for e in events
        if e["event"] == "cycle_started"
        and e["tick"] == tick
        and tuple(e["position"]) == tuple(position)
    )


def co_resident(law, *seeds, ticks=1, slots=4):
    """Seeds placed on one Node; the rule is decided in the first cycle."""
    return build.configuration(law, list(seeds), ticks=ticks, slots=slots)


def rejected_atomically(document, match):
    world = Simulation(parse_initial_state(document))
    before = world.snapshot()
    with pytest.raises(ValueError, match=match):
        world.step()
    assert world.snapshot() == before
    assert all(node.pending is None for node in world.nodes.values())


# --- fixtures, bindings and the four physical laws -------------------------------


@pytest.mark.parametrize("name", sorted(build.FIXTURES))
def test_checked_in_fixture_matches_the_builder_and_validates(name):
    path = HERE / f"{name}.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    assert document == build.FIXTURES[name]()
    assert document["model_id"] == EXPECTED["fixtures"][name]["model_id"]
    assert validate_configuration(path.read_bytes()).valid
    rule = document["interactions"][0]
    assert set(rule) >= {"participants", "outputs", "assignments", "invariants", "when"}
    assert "output_types" not in rule and "left_type" not in rule


def test_bindings_derive_every_family_value_from_the_catalog():
    bindings = json.loads((HERE / "bindings.json").read_text(encoding="utf-8"))
    assert bindings == build.bindings()
    catalog = json.loads((ROOT / bindings["catalog"]).read_text(encoding="utf-8"))
    families = {row["id"] for row in catalog["interaction_families"]}
    channels = {row["id"]: row for row in catalog["representative_channels"]}
    entities = bindings["entities"]
    assert {e["catalog_id"] for e in entities.values()} == {"electron", "positron", "photon", "muon"}
    assert entities["muon"]["rest_energy_keV"] == 105658 and entities["muon"]["charge"] == -3
    assert entities["electron"]["rest_energy_keV"] == 511 == entities["positron"]["rest_energy_keV"]
    assert entities["photon"]["rest_energy_keV"] == 0 and entities["photon"]["charge"] == 0
    assert (entities["electron"]["charge"], entities["positron"]["charge"]) == (-3, 3)
    assert entities["electron"]["mass_encoding"]["rounding"] == "nearest_ties_away_from_zero"
    assert abs(Fraction(entities["electron"]["mass_encoding"]["errors_source_units"][0])) < Fraction(
        5, 10000
    )
    assert entities["positron"]["mass_reference"]["resolved_from"] == "electron"
    for law, rule in bindings["rules"].items():
        assert rule["interaction_family"] in families
        if rule["representative_channel"] is not None:
            channel = channels[rule["representative_channel"]]
            assert sorted(channel["incoming_ids"]) == sorted(rule["participants"])
            assert sorted(channel["outgoing_ids"]) == sorted(rule["outputs"])
        built = build.RULES[law]()
        assert [p["type"] for p in built["participants"]] == rule["participants"]
        assert [o["type"] for o in built["outputs"]] == rule["outputs"]
    assert bindings["conversion_contract"] == "family-conversion-n-to-m-v1"


def test_annihilation_meets_at_tick_6_and_emits_two_on_shell_photons():
    expected = EXPECTED["fixtures"]["annihilation"]
    world, events = run(build.annihilation_fixture())
    assert cycle_at(events, expected["conversion_tick"])["ready_tick"] == expected["conversion_tick"]
    assert sorted(sent(events, expected["conversion_tick"])) == sorted(
        ("photon", o["energy"], o["momentum"], o["charge"], o["port"]) for o in expected["outputs"]
    )
    assert escapes(events) == [(15, "photon", 1825), (15, "photon", 1825)]
    assert world.totals() == {"energy": (0,), "momentum": (0, 0, 0), "charge": (0,)}
    assert world.escaped_totals() == {"energy": (3650,), "momentum": (0, 0, 0), "charge": (0,)}
    assert records(world) == []


@pytest.mark.parametrize(
    ("electron", "positron", "outputs"),
    [
        ((1825, [1752, 0, 0]), (511, [0, 0, 0]), [(2044, [2044, 0, 0]), (292, [-292, 0, 0])]),
        # E + P.u odd: photon b owns the indivisible keV as energy above |p_b|.
        ((1825, [1752, 0, 0]), (512, [0, 0, 0]), [(2044, [2044, 0, 0]), (293, [-292, 0, 0])]),
        ((1825, [-1752, 0, 0]), (512, [0, 0, 0]), [(2044, [-2044, 0, 0]), (293, [292, 0, 0])]),
        ((511, [0, 0, 0]), (511, [0, 0, 0]), [(511, [511, 0, 0]), (511, [-511, 0, 0])]),
        ((700, [0, 0, 400]), (511, [0, 0, 0]), [(805, [0, 0, 805]), (406, [0, 0, -405])]),
    ],
)
def test_annihilation_kinematics_are_exact_with_owned_odd_remainder(electron, positron, outputs):
    document = co_resident(
        "annihilation",
        build.seed("electron", NODE, electron[0], electron[1]),
        build.seed("positron", NODE, positron[0], positron[1]),
    )
    world, _ = run(document)
    found = records(world)
    assert sorted((kind, v["energy"][0], list(v["momentum"])) for _, kind, v in found) == sorted(
        ("photon", e, p) for e, p in outputs
    )
    assert all(v["charge"] == (0,) for _, _, v in found)
    assert sum(v["energy"][0] for _, _, v in found) == electron[0] + positron[0]
    assert all(v["energy"][0] - sum(map(abs, v["momentum"])) in (0, 1) for _, _, v in found)


def test_annihilation_requires_momenta_on_one_common_axis():
    document = co_resident(
        "annihilation",
        build.seed("electron", NODE, 1825, [1752, 0, 0]),
        build.seed("positron", NODE, 1825, [0, -1752, 0]),
    )
    world, _ = run(document)
    assert sorted(kind for _, kind, _ in records(world)) == ["electron", "positron"]


def test_pair_production_at_threshold_leaves_a_resting_pair_and_no_transfer():
    expected = EXPECTED["fixtures"]["pair-production"]
    world, events = run(build.pair_production_fixture())
    assert cycle_at(events, 6)["ready_tick"] == 6
    assert sum(e["event"] == "sent" for e in events) == expected["sent_events_total"]
    assert records(world) == [
        (tuple(NODE), "electron", {"energy": (511,), "momentum": (0, 0, 0), "charge": (-3,)}),
        (tuple(NODE), "positron", {"energy": (511,), "momentum": (0, 0, 0), "charge": (3,)}),
    ]
    assert world.totals() == {"energy": (1022,), "momentum": (0, 0, 0), "charge": (0,)}
    assert world.escaped_totals()["energy"] == (0,)


def test_below_threshold_photons_cross_without_reacting_and_leave_the_open_boundary():
    expected = EXPECTED["fixtures"]["pair-production-control"]
    world, events = run(build.FIXTURES["pair-production-control"]())
    assert {e["disturbance"] for e in events if e["event"] == "sent"} == {"photon"}
    assert sum(e["event"] == "sent" for e in events) == expected["sent_events_total"]
    assert sorted(sent(events, 6)) == [
        ("photon", 500, [-500, 0, 0], 0, 1),
        ("photon", 500, [500, 0, 0], 0, 0),
    ]
    assert escapes(events) == [(15, "photon", 500), (15, "photon", 500)]
    assert world.totals()["energy"] == (0,) and world.escaped_totals()["energy"] == (1000,)


@pytest.mark.parametrize(
    ("first", "second", "outputs"),
    [
        ((511, [511, 0, 0]), (511, [-511, 0, 0]), [(511, [0, 0, 0]), (511, [0, 0, 0])]),
        ((511, [511, 0, 0]), (510, [-510, 0, 0]), None),
        ((48, [48, 0, 0]), (5329, [-5329, 0, 0]), None),
        ((600, [600, 0, 0]), (600, [-600, 0, 0]), [(600, [0, 0, 0]), (600, [0, 0, 0])]),
        ((600, [600, 0, 0]), (600, [600, 0, 0]), None),
        ((601, [0, 601, 0]), (600, [0, -600, 0]), [(600, [0, 0, 0]), (601, [0, 1, 0])]),
    ],
)
def test_pair_production_threshold_is_exact_at_1022_and_one_unit_below(first, second, outputs):
    document = co_resident(
        "pair_production",
        build.seed("photon", NODE, first[0], first[1]),
        build.seed("photon", NODE, second[0], second[1]),
    )
    world, _ = run(document)
    found = records(world)
    if outputs is None:
        assert [kind for _, kind, _ in found] == ["photon", "photon"]
        return
    assert [(kind, v["energy"][0], list(v["momentum"]), v["charge"][0]) for _, kind, v in found] == [
        ("electron", outputs[0][0], outputs[0][1], -3),
        ("positron", outputs[1][0], outputs[1][1], 3),
    ]


def test_co_moving_pair_on_one_port_is_a_declared_limit_not_a_silent_merge():
    # Product exactly 511^2: on shell, 2689^2 - 2640^2 = 511^2, but both leptons
    # would leave on -X in the same tick, which the one-departure-per-Port rule rejects.
    document = co_resident(
        "pair_production",
        build.seed("photon", NODE, 49, [49, 0, 0]),
        build.seed("photon", NODE, 5329, [-5329, 0, 0]),
    )
    rejected_atomically(document, "distinct Ports")


def test_compton_transfers_the_declared_energy_fraction_in_one_joint_transaction():
    expected = EXPECTED["fixtures"]["compton"]
    world, events = run(build.compton_fixture())
    assert cycle_at(events, 6)["ready_tick"] == 6
    assert sorted(sent(events, 6)) == [
        ("electron", 767, [511, -255, 0], -3, 0),
        ("photon", 255, [0, 255, 0], 0, 2),
    ]
    assert (10, "photon", 255) in escapes(events)
    assert [e for e in escapes(events) if e[1] == "electron"][0][0] <= expected[
        "electron_escaped_by_tick"
    ]
    assert world.escaped_totals() == {"energy": (1022,), "momentum": (511, 0, 0), "charge": (-3,)}
    assert records(world) == []


@pytest.mark.parametrize("energy", [100, 511, 1022, 10_000_000, MAX_VALUE - 1])
def test_compton_fraction_depends_on_energy_through_the_integer_formula(energy):
    table = EXPECTED["fixtures"]["compton"]["energy_dependence_at_cos_0"]
    rest = build.REST_ENERGY
    scattered = energy * rest // (rest + energy)
    if str(energy) in table:
        assert scattered == table[str(energy)]
    document = co_resident(
        "compton",
        build.seed("photon", NODE, energy, [energy, 0, 0]),
        build.seed("electron", NODE, rest, [0, 0, 0]),
    )
    world, _ = run(document)
    values = {kind: v for _, kind, v in records(world)}
    assert values["photon"] == {"energy": (scattered,), "momentum": (0, scattered, 0), "charge": (0,)}
    assert values["electron"]["energy"] == (energy + rest - scattered,)
    assert values["electron"]["momentum"] == (energy, -scattered, 0)


def test_compton_recoil_energy_owns_the_division_remainder():
    # 511 * 511 / 1022 = 255.5: the photon keeps 255, the electron the rest.
    document = co_resident(
        "compton",
        build.seed("photon", NODE, 511, [511, 0, 0]),
        build.seed("electron", NODE, 511, [0, 0, 0]),
    )
    world, _ = run(document)
    electron = {kind: v for _, kind, v in records(world)}["electron"]
    shell = electron["energy"][0] ** 2 - sum(c * c for c in electron["momentum"])
    assert electron["energy"] == (767,) and shell - 511 * 511 == 2 * 511


def test_moving_electron_crossing_a_photon_strands_nothing_at_any_node():
    """The meeting is one joint transaction at the shared Node; there is no Node-owned stock."""
    document = build.configuration(
        "compton",
        [
            build.seed("photon", [2, 3, 3], 511, [511, 0, 0]),
            build.seed("electron", [14, 3, 3], 1825, [-1752, 0, 0]),
        ],
        ticks=18,
    )
    world = Simulation(parse_initial_state(document))
    initial = world.totals()
    for _ in range(18):
        world.step()
        found = records(world)
        assert {kind for _, kind, _ in found} <= {"photon", "electron"}
        # Every quantity the world still holds sits in a whole record; nothing else owns stock.
        held = {
            name: tuple(sum(v[name][c] for _, _, v in found) for c in range(len(initial[name])))
            for name in initial
        }
        assert world.totals() == held
        escaped = world.escaped_totals()
        assert all(
            tuple(a + b for a, b in zip(held[name], escaped[name], strict=True)) == initial[name]
            for name in initial
        )
    # The rule requires a resting target, so nothing happened and both records left intact.
    assert records(world) == []
    assert world.escaped_totals() == {"energy": (2336,), "momentum": (-1241, 0, 0), "charge": (-3,)}


def test_photon_stream_past_a_resting_electron_scatters_once_and_forwards_the_rest():
    document = build.configuration(
        "compton",
        [
            build.seed("photon", [2, 3, 3], 511, [511, 0, 0]),
            build.seed("photon", [4, 3, 3], 511, [511, 0, 0]),
            build.seed("photon", [6, 3, 3], 511, [511, 0, 0]),
            build.seed("electron", [8, 3, 3], 511, [0, 0, 0]),
        ],
        ticks=20,
    )
    world, events = run(document)
    # The leading photon (x = 6) meets the target at tick 2; the recoil electron then
    # moves one Link per tick like the following photons, which pass the empty Node.
    assert sorted(sent(events, 2)) == [
        ("electron", 767, [511, -255, 0], -3, 0),
        ("photon", 255, [0, 255, 0], 0, 2),
    ]
    assert escapes(events) == [
        (6, "photon", 255),
        (11, "electron", 767),
        (13, "photon", 511),
        (15, "photon", 511),
    ]
    assert records(world) == [] and world.totals()["energy"] == (0,)
    assert world.escaped_totals()["energy"] == (3 * 511 + 511,)


# --- 2 -> 3 and its controls --------------------------------------------------------


def test_three_photon_conversion_leaves_on_three_distinct_ports_with_exact_totals():
    expected = EXPECTED["fixtures"]["three-photon"]
    world, events = run(build.three_photon_fixture())
    assert cycle_at(events, 6)["ready_tick"] == 6
    assert sorted(sent(events, 6)) == sorted(
        ("photon", o["energy"], o["momentum"], o["charge"], o["port"]) for o in expected["outputs"]
    )
    assert escapes(events) == [(10, "photon", 292), (10, "photon", 292), (15, "photon", 1752)]
    assert world.totals() == {"energy": (0,), "momentum": (0, 0, 0), "charge": (0,)}
    assert world.escaped_totals() == {"energy": (2336,), "momentum": (1752, 0, 0), "charge": (0,)}


@pytest.mark.parametrize(
    ("electron", "positron", "outputs"),
    [
        (
            (1825, [1752, 0, 0]),
            (512, [0, 0, 0]),
            [(1752, [1752, 0, 0]), (293, [0, 292, 0]), (292, [0, -292, 0])],
        ),
        ((1825, [1752, 0, 0]), (1825, [-1752, 0, 0]), None),
        (
            (700, [0, 0, 400]),
            (511, [0, 0, 0]),
            [(400, [0, 0, 400]), (406, [405, 0, 0]), (405, [-405, 0, 0])],
        ),
    ],
)
def test_three_photon_odd_unit_and_zero_net_momentum_guard(electron, positron, outputs):
    document = co_resident(
        "three_photon",
        build.seed("electron", NODE, electron[0], electron[1]),
        build.seed("positron", NODE, positron[0], positron[1]),
    )
    world, _ = run(document)
    found = records(world)
    if outputs is None:
        assert sorted(kind for _, kind, _ in found) == ["electron", "positron"]
        return
    assert sorted((v["energy"][0], list(v["momentum"])) for _, _, v in found) == sorted(outputs)
    assert {kind for _, kind, _ in found} == {"photon"}
    assert all(v["energy"][0] - sum(map(abs, v["momentum"])) in (0, 1) for _, _, v in found)


def test_third_output_without_a_free_slot_fails_before_commit():
    document = build.FIXTURES["three-photon-capacity-control"]()
    world = Simulation(parse_initial_state(document))
    for _ in range(6):
        world.step()
    before = world.snapshot()
    with pytest.raises(ValueError, match="free resident slots"):
        world.step()
    assert world.snapshot() == before
    assert sorted((kind, v["energy"][0]) for _, kind, v in records(world)) == [
        ("electron", 1825),
        ("positron", 511),
    ]
    assert all(node.pending is None for node in world.nodes.values())


def test_two_products_on_one_port_fail_before_commit():
    # The collinear variant would send photons 1022 and 1022 on +X and 292 on -X.
    document = build.FIXTURES["three-photon-port-control"]()
    world = Simulation(parse_initial_state(document))
    for _ in range(6):
        world.step()
    before = world.snapshot()
    with pytest.raises(ValueError, match="distinct Ports"):
        world.step()
    assert world.snapshot() == before
    assert sorted(kind for _, kind, _ in records(world)) == ["electron", "positron"]
    assert all(node.pending is None for node in world.nodes.values())


def test_spectator_leaving_on_a_product_port_does_not_fail_the_cycle():
    world, events = run(build.three_photon_fixture(spectator=True))
    node = [8, 6, 3]
    assert sorted(sent(events, 6, node)) == [
        ("photon", 100, [0, 100, 0], 0, 2),
        ("photon", 292, [0, -292, 0], 0, 3),
        ("photon", 292, [0, 292, 0], 0, 2),
        ("photon", 1752, [1752, 0, 0], 0, 0),
    ]
    assert world.escaped_totals() == {"energy": (2436,), "momentum": (1752, 100, 0), "charge": (0,)}


# --- 4 -> 4: four rays through four Ports in one joint transaction ----------------------


def test_four_rays_through_four_ports_convert_in_one_joint_transaction():
    expected = EXPECTED["fixtures"]["four-body"]
    world, events = run(build.four_body_fixture())
    node = [8, 6, 3]
    arrivals = [e for e in events if e["event"] == "received" and e["tick"] == 6]
    assert sorted(e["port"] for e in arrivals) == [0, 1, 2, 3]
    assert cycle_at(events, 6, node)["ready_tick"] == 6
    assert sorted(sent(events, 6, node)) == sorted(
        ("photon", o["energy"], o["momentum"], o["charge"], o["port"]) for o in expected["outputs"]
    )
    assert escapes(events) == [
        (13, "photon", 1063),
        (13, "photon", 1063),
        (15, "photon", 1062),
        (15, "photon", 1062),
    ]
    assert world.escaped_totals() == {"energy": (4250,), "momentum": (0, 0, 0), "charge": (0,)}
    assert records(world) == []


@pytest.mark.parametrize(
    ("electron_energy", "photons", "outputs"),
    [
        # Q odd: photon a (+X) owns the unit above |p_a|; every output reads all four energies.
        (
            1826,
            ((300, [0, 300, 0]), (300, [0, -300, 0])),
            [(1063, [1062, 0, 0]), (1062, [-1062, 0, 0]), (1063, [0, 1063, 0]), (1063, [0, -1063, 0])],
        ),
        (1825, ((300, [0, 300, 0]), (301, [0, -301, 0])), None),
        (1825, ((300, [300, 0, 0]), (300, [-300, 0, 0])), None),
        (
            1825,
            ((700, [0, 0, 700]), (700, [0, 0, -700])),
            [(1262, [1262, 0, 0]), (1262, [-1262, 0, 0]), (1263, [0, 0, 1263]), (1263, [0, 0, -1263])],
        ),
    ],
)
def test_four_body_pooled_energy_depends_on_all_four_inputs(electron_energy, photons, outputs):
    node = [8, 6, 3]
    document = build.configuration(
        "four_body",
        [
            build.seed("electron", node, electron_energy, [1752, 0, 0]),
            build.seed("positron", node, 1825, [-1752, 0, 0]),
            build.seed("photon", node, photons[0][0], photons[0][1]),
            build.seed("photon", node, photons[1][0], photons[1][1]),
        ],
        shape=[17, 13, 7],
        ticks=1,
        slots=6,
    )
    world, _ = run(document)
    found = records(world)
    if outputs is None:
        # The joint rule is silent; the pair annihilates through the declared fallback
        # and the spectator photons continue unchanged, even beside a product's Port.
        assert sum(kind == "photon" for _, kind, _ in found) >= 2
        assert sorted(
            v["energy"][0] for _, kind, v in found if kind == "photon" and v["energy"][0] < 1000
        ) == sorted(p[0] for p in photons)
        return
    assert sorted((v["energy"][0], list(v["momentum"])) for _, _, v in found) == sorted(outputs)
    assert {kind for _, kind, _ in found} == {"photon"}
    assert (
        sum(v["energy"][0] for _, _, v in found)
        == electron_energy + 1825 + photons[0][0] + photons[1][0]
    )


def test_three_of_four_rays_leave_the_joint_rule_silent_and_the_pair_rule_acts():
    world, events = run(build.FIXTURES["four-body-three-arrive-control"]())
    node = [8, 6, 3]
    assert sorted(sent(events, 6, node)) == [
        ("photon", 300, [0, 300, 0], 0, 2),
        ("photon", 1825, [-1825, 0, 0], 0, 1),
        ("photon", 1825, [1825, 0, 0], 0, 0),
    ]
    assert escapes(events) == [(13, "photon", 300), (15, "photon", 1825), (15, "photon", 1825)]
    assert world.escaped_totals() == {"energy": (3950,), "momentum": (0, 300, 0), "charge": (0,)}


def test_four_collinear_products_fail_the_joint_rule_before_commit():
    # The collinear variant would send 1062 + 1063 on +X and 1062 + 1063 on -X.
    world = Simulation(parse_initial_state(build.FIXTURES["four-body-port-control"]()))
    for _ in range(6):
        world.step()
    before = world.snapshot()
    with pytest.raises(ValueError, match="distinct Ports"):
        world.step()
    assert world.snapshot() == before
    assert sorted(kind for _, kind, _ in records(world)) == ["electron", "photon", "photon", "positron"]
    assert all(node.pending is None for node in world.nodes.values())


def test_muon_spectator_beside_a_product_keeps_ordinary_transport():
    world, events = run(build.four_body_fixture(spectator=True))
    node = [8, 6, 3]
    departures = sent(events, 6, node)
    assert ("muon", 105658, [-100, 0, 0], -3, 1) in departures
    assert sorted(d[4] for d in departures) == [0, 1, 1, 2, 3]
    assert world.escaped_totals()["charge"] == (-3,) and world.totals()["energy"] == (0,)


def test_sixteen_quadruples_on_a_48_cubed_board_convert_at_the_same_tick():
    document = build.scale_configuration("four_body", 16, 10_000_000, 48, 22)
    world, events = run(document)
    started = [e for e in events if e["event"] == "cycle_started" and e["tick"] == 21]
    assert len(started) == 16 and all(e["ready_tick"] == 21 for e in started)
    photons = sent(events, 21, position=None)
    assert len(photons) == 64 and {kind for kind, *_ in photons} == {"photon"}
    assert world.totals()["charge"] == (0,) and world.totals()["momentum"] == (0, 0, 0)


# --- generic N-to-M contract on the stock/momentum probe world ----------------------


def probe_rule(inputs, outputs, assignments, invariants=None):
    return {
        "name": "probe",
        "participants": [{"type": "stored A"}] * inputs,
        "outputs": [{"type": "outgoing A"}] * outputs,
        "assignments": assignments,
        "invariants": invariants or [{"name": "stock", "expression": {"field": "stock"}}],
    }


def probe_world(rule, seeds, *, slots=8, conserved_momentum=True):
    raw = json.loads(PROBE.read_text(encoding="utf-8"))
    raw.update(link_ticks=1, slots_per_node=slots, interactions=[rule], seeds=seeds)
    raw["fields"][1]["conserved"] = conserved_momentum
    return raw


def stored(stock):
    return {
        "position": [4, 4, 4],
        "type": "stored A",
        "values": {"stock": stock, "momentum": [0, 0, 0]},
    }


def part(index, name):
    return {"field": name, "participant": index}


def burst(directions):
    """1 -> 6: stock 12 into six records of stock 2 along the given directions."""
    share = {"op": "exact_div", "args": [part(0, "stock"), 6]}
    return probe_rule(
        1,
        6,
        [
            item
            for j in range(6)
            for item in (
                {"output": j, "field": "stock", "expression": share},
                {"output": j, "field": "momentum", "expression": directions[j]},
            )
        ],
    )


def test_one_to_six_leaves_one_record_on_every_port():
    world, events = run(probe_world(burst(UNITS), [stored(12)]), ticks=1)
    assert sorted(e["port"] for e in events if e["event"] == "sent") == [0, 1, 2, 3, 4, 5]
    assert world.totals() == {"stock": (12,), "momentum": (0, 0, 0)}
    assert len(records(world)) == 6 and all(v["stock"] == (2,) for _, _, v in records(world))


def test_six_to_one_consumes_five_slots_and_keeps_the_stock():
    total = {"op": "add", "args": [part(0, "stock"), part(1, "stock")]}
    for index in range(2, 6):
        total = {"op": "add", "args": [total, part(index, "stock")]}
    rule = probe_rule(
        6,
        1,
        [
            {"output": 0, "field": "stock", "expression": total},
            {"output": 0, "field": "momentum", "expression": [1, 0, 0]},
        ],
    )
    world, events = run(
        probe_world(rule, [stored(i + 1) for i in range(6)], conserved_momentum=False), ticks=1
    )
    assert records(world) == [((5, 4, 4), "outgoing A", {"stock": (21,), "momentum": (1, 0, 0)})]
    assert sum(e["event"] == "sent" for e in events) == 1


def test_two_outputs_on_one_port_are_rejected_before_commit():
    directions = [UNITS[0], UNITS[0], UNITS[2], UNITS[3], UNITS[4], UNITS[5]]
    document = probe_world(burst(directions), [stored(12)], conserved_momentum=False)
    rejected_atomically(document, "distinct Ports")


def test_outputs_beyond_the_free_slots_are_rejected_before_commit():
    rejected_atomically(probe_world(burst(UNITS), [stored(12)], slots=4), "free resident slots")


def test_broken_readout_invariant_leaves_every_owner_unchanged():
    rule = burst(UNITS)
    rule["invariants"] = [
        {
            "name": "momentum_l1",
            "expression": {"op": "sum", "args": [{"op": "abs", "args": [{"field": "momentum"}]}]},
        }
    ]
    rejected_atomically(
        probe_world(rule, [stored(12)], conserved_momentum=False), "invariant momentum_l1"
    )


def test_conserved_field_mismatch_leaves_every_owner_unchanged():
    rule = burst(UNITS)
    rule["assignments"][0]["expression"] = 3
    rejected_atomically(probe_world(rule, [stored(12)]), "conservation of stock")


@pytest.mark.parametrize(
    ("inputs", "outputs", "match"),
    [(7, 1, "participants"), (1, 7, "outputs"), (0, 1, "participants"), (1, 0, "outputs")],
)
def test_arity_outside_one_to_six_is_rejected(inputs, outputs, match):
    rule = burst(UNITS)
    rule["participants"] = [{"type": "stored A"}] * inputs
    rule["outputs"] = [{"type": "outgoing A"}] * outputs
    with pytest.raises(ValueError, match=match):
        parse_initial_state(probe_world(rule, []))


def _pair_selector(rule):
    rule["left_type"] = "stored A"


def _pair_outputs(rule):
    rule["output_types"] = {"left": "outgoing A", "right": "outgoing B"}


def _no_participants(rule):
    rule.pop("participants")


def _missing_assignment(rule):
    rule["assignments"].pop()


def _output_out_of_range(rule):
    rule["assignments"].append({"output": 6, "field": "stock", "expression": 1})


def _duplicate_target(rule):
    rule["assignments"].append({"output": 0, "field": "stock", "expression": 1})


def _property_output(rule):
    rule["outputs"][0] = {"requires": ["stock"]}


@pytest.mark.parametrize(
    ("change", "match"),
    [
        (_pair_selector, "participants only"),
        (_pair_outputs, "participants only"),
        (_no_participants, "indexed participants"),
        (_missing_assignment, "every output field"),
        (_output_out_of_range, "exceeds the declared outputs"),
        (_duplicate_target, "duplicate assignment"),
        (_property_output, "unknown keys"),
    ],
)
def test_unsupported_conversion_compositions_are_rejected_at_initialization(change, match):
    rule = burst(UNITS)
    change(rule)
    with pytest.raises(ValueError, match=match):
        parse_initial_state(probe_world(rule, []))


def test_split_families_cannot_convert():
    raw = probe_world(burst(UNITS), [])
    raw["disturbance_types"][2]["transport"] = {"mode": "split", "weights": [1, 1, 1, 1, 1, 1]}
    with pytest.raises(ValueError, match="whole records"):
        parse_initial_state(raw)


def test_property_selected_inputs_convert_and_the_pair_path_is_unchanged():
    rule = burst(UNITS)
    rule["participants"] = [{"requires": ["stock", "momentum"]}]
    # The properties match every family here, so the products would be selected
    # again in the next cycle; one tick shows the selection without that repeat.
    world, _ = run(probe_world(rule, [stored(12)]), ticks=1)
    assert len(records(world)) == 6
    # The existing two-to-two contract keeps its own selectors and semantics.
    world = Simulation(parse_initial_state(json.loads(PROBE.read_text(encoding="utf-8"))))
    world.step()
    assert sorted(kind for _, kind, _ in records(world)) == ["outgoing A", "outgoing B"]


def test_arrivals_during_a_conversion_wait_cannot_take_a_reserved_output_slot():
    """A slow conversion locks the free slots its extra outputs need; arrivals wait elsewhere."""
    raw = probe_world(burst(UNITS), [stored(12)], slots=7)
    raw["normal_budget"] = 1
    raw["seeds"].append(
        {"position": [3, 4, 4], "type": "outgoing A", "values": {"stock": 1, "momentum": [1, 0, 0]}}
    )
    world = Simulation(parse_initial_state(raw))
    world.step()
    node = world.nodes[(4, 4, 4)]
    assert node.pending is not None
    assert {slot for slot, _ in node.pending.plan.replacements} == set(range(6))
    for _ in range(60):
        world.step()
    assert world.totals()["stock"] == (13,)


def node_profile(rule, seeds):
    """The same 1 -> 2 conversion under the integer Node profile."""
    raw = probe_world(rule, seeds, conserved_momentum=False)
    raw["node_execution"] = True
    raw["fields"][0]["aggregation"] = "sum"
    raw["fields"][1]["aggregation"] = "vector_sum"
    raw["conservation_contract"] = {
        "name": "stock readout",
        "quantities": [
            {
                "name": "stock",
                "components": 1,
                "units": "configured inventory unit",
                "carriers": [{"requires": ["stock"], "value": {"field": "stock"}}],
            }
        ],
    }
    return raw


def split_in_two():
    half = {"op": "exact_div", "args": [part(0, "stock"), 2]}
    return probe_rule(
        1,
        2,
        [
            {"output": 0, "field": "stock", "expression": half},
            {"output": 0, "field": "momentum", "expression": UNITS[0]},
            {"output": 1, "field": "stock", "expression": half},
            {"output": 1, "field": "momentum", "expression": UNITS[1]},
        ],
    )


def test_conversion_under_node_execution_takes_k_local_steps():
    rule = split_in_two()
    rule["k"] = 2
    events = []
    world = Simulation(parse_initial_state(node_profile(rule, [stored(12)])), observer=events.append)
    world.step()
    node = world.nodes[(4, 4, 4)]
    assert node.pending is not None and node.pending.ready_tick == 2
    assert not [e for e in events if e["event"] == "sent"]
    world.step()
    world.step()
    assert sorted((e["tick"], e["port"]) for e in events if e["event"] == "sent") == [(2, 0), (2, 1)]
    assert world.totals()["stock"] == (12,)


def test_conversion_under_node_execution_requires_k():
    with pytest.raises(ValueError, match="explicit positive k"):
        parse_initial_state(node_profile(split_in_two(), [stored(12)]))


# --- integer bound --------------------------------------------------------------------


@pytest.mark.parametrize("law", ["annihilation", "pair_production"])
def test_conversion_at_the_integer_bound_stays_within_max_value(law):
    if law == "annihilation":
        first = build.seed("electron", NODE, MAX_VALUE, [MAX_VALUE - 1, 0, 0])
        second = build.seed("positron", NODE, MAX_VALUE, [1 - MAX_VALUE, 0, 0])
    else:
        first = build.seed("photon", NODE, MAX_VALUE, [MAX_VALUE, 0, 0])
        second = build.seed("photon", NODE, MAX_VALUE, [-MAX_VALUE, 0, 0])
    world, _ = run(co_resident(law, first, second))
    found = records(world)
    assert all(abs(c) <= MAX_VALUE for _, _, v in found for values in v.values() for c in values)
    assert sum(v["energy"][0] for _, _, v in found) == 2 * MAX_VALUE
    assert {kind for _, kind, _ in found} == (
        {"photon"} if law == "annihilation" else {"electron", "positron"}
    )


def test_first_thing_beyond_the_bound_is_rejected_explicitly():
    beyond = MAX_VALUE + 1
    with pytest.raises(ValueError, match="through 1073741823"):
        parse_initial_state(
            co_resident(
                "annihilation",
                build.seed("electron", NODE, beyond, [0, 0, 0]),
                build.seed("positron", NODE, 511, [0, 0, 0]),
            )
        )
    # The Compton recoil electron at a MAX_VALUE photon would carry MAX_VALUE + 1 keV.
    rejected_atomically(
        co_resident(
            "compton",
            build.seed("photon", NODE, MAX_VALUE, [MAX_VALUE, 0, 0]),
            build.seed("electron", NODE, 511, [0, 0, 0]),
        ),
        "integer bound",
    )


def test_sixteen_pairs_on_a_48_cubed_board_convert_at_the_same_tick_up_to_10_gev():
    document = build.scale_configuration("annihilation", 16, 10_000_000, 48, 22)
    world, events = run(document)
    started = [e for e in events if e["event"] == "cycle_started" and e["tick"] == 21]
    assert len(started) == 16 and all(e["ready_tick"] == 21 for e in started)
    photons = sent(events, 21, position=None)
    assert len(photons) == 32 and {kind for kind, *_ in photons} == {"photon"}
    assert max(energy for _, energy, *_ in photons) == 10_000_000
    assert world.totals() == {"energy": (170_000_000,), "momentum": (0, 0, 0), "charge": (0,)}
    assert (
        world.execution_report()["focus_enabled"]
        and world.execution_report()["awake_carrier_nodes"] == 32
    )
