"""Independent finite expectations for local coherent scattering and readout."""

import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path

import pytest

from event_universe.core.event_space import CausalEventSpace
from event_universe.integration.quantum_experiment import QuantumExperiment, run_experiment
from event_universe.integration.quantum_initialization import parse_quantum_initialization
from event_universe.integration.quantum_observations import reduced_state
from event_universe.quantum import Amplitude, DeferredQuantum, EventNetworkConfig, LocalUnitary
from event_universe.quantum.mode_rules import occupation_totals

EXAMPLES = Path(__file__).parents[1] / "examples" / "quantum"


def document(name="photon-return-erasure.json"):
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def fraction(value):
    return Fraction(value["numerator"], value["denominator"])


def coherence(world):
    state = reduced_state(world.network.joint_state(), (0, 1))
    return next(
        (fraction(e["real"]) for e in state["elements"] if (e["row"], e["column"]) == (1, 2)),
        Fraction(0),
    )


def run(raw):
    world = QuantumExperiment(parse_quantum_initialization(raw))
    for _ in range(world.initial.ticks):
        world.step()
    return world


def test_return_keeps_which_path_information_until_the_local_inverse():
    world = QuantumExperiment(parse_quantum_initialization(document()))
    assert coherence(world) == Fraction(1, 2)
    expected_x = [0, 0, 1, 2, 3, 0, 0]
    for tick, x in enumerate(expected_x, 1):
        world.step()
        assert world.network.addresses[2:] == ((x, 0, 0),) * 2
        assert coherence(world) == (Fraction(1, 2) if tick in (1, 7) else 0)
        assert not world.network.records
        assert {
            occupation_totals(bits, tuple(m.quantities for m in world.initial.modes))
            for bits, _ in world.network.joint_state()
        } == {(1, 1, 18, 6, 0, 0)}
    assert coherence(run(document("photon-return.json"))) == 0


def test_three_fresh_photons_reduce_coherence_by_their_state_overlap():
    world = QuantumExperiment(parse_quantum_initialization(document("three-photon-decoherence.json")))
    expected = {2: Fraction(3, 10), 5: Fraction(9, 50), 8: Fraction(27, 250)}
    for tick in range(1, 10):
        world.step()
        if tick in expected:
            assert coherence(world) == expected[tick]
    assert fraction(world.snapshot()["groups"]["target"]["purity"]) == Fraction(8177, 15625)
    assert world.network.successful_queries == 0


def test_phase_and_full_checkpoint_preserve_the_returning_environment():
    worlds = [QuantumExperiment(parse_quantum_initialization(document())) for _ in range(2)]
    for tick in range(7):
        for world in worlds:
            world.step()
        if tick == 3:
            worlds[1].network.checkpoint(0)
        assert worlds[0].snapshot() == worlds[1].snapshot()
    variant = document()
    variant["rules"]["phase"] = {"matrix": [[1, 0], [0, -1]]}
    # One cell-local phase while the marked probe waits away from the target.
    for action in variant["actions"]:
        if action["tick"] >= 3:
            action["tick"] += 1
    variant["ticks"] += 1
    variant["actions"].append(
        {"tick": 3, "kind": "local", "modes": ["probe 0 polarization 1"], "rule": "phase", "cost": 1}
    )
    assert coherence(run(variant)) == Fraction(-1, 2)
    variant["rules"]["phase"]["matrix"][1][1] = [0, 1]
    elements = run(variant).snapshot()["groups"]["target"]["elements"]
    cross = next(e for e in elements if (e["row"], e["column"]) == (1, 2))
    assert fraction(cross["real"]) == 0 and fraction(cross["imaginary"]) == Fraction(1, 2)


def test_observed_records_condition_paths_but_unread_outcomes_do_not_signal():
    raw = document("conditioned-target-path.json")
    snapshots = []
    for ticket in (0, 1):
        variant = deepcopy(raw)
        next(a for a in variant["actions"] if a["kind"] == "observe")["ticket"] = ticket
        world = run(variant)
        assert world.network.records[0].decision.weights == (1, 1)
        assert world.network.records[0].outcome == ticket
        final = world.snapshot()
        snapshots.append(final)
        assert fraction(final["modes"][ticket]["probability"]) == 1
        assert final["modes"][ticket]["position"] == (3, ticket, 0)
        assert coherence(world) == 0
    # Summing the two equally weighted records leaves the original marginal.
    for site in (0, 1):
        assert sum(fraction(s["modes"][site]["probability"]) for s in snapshots) / 2 == Fraction(1, 2)
    unobserved = deepcopy(raw)
    unobserved["actions"] = [a for a in unobserved["actions"] if a["kind"] != "observe"]
    assert all(
        fraction(m["probability"]) == Fraction(1, 2) for m in run(unobserved).snapshot()["modes"][:2]
    )


def test_recoil_changes_energy_and_momentum_without_a_global_repair():
    world = QuantumExperiment(parse_quantum_initialization(document("photon-recoil.json")))
    totals = []
    for _ in range(4):
        world.step()
        totals.extend(
            occupation_totals(bits, tuple(m.quantities for m in world.initial.modes))
            for bits, _ in world.network.joint_state()
        )
    assert set(totals) == {(1, 1, 18, 6, 0, 0)}
    assert world.network.joint_state() == ((10, Amplitude(1, 0)),)
    assert world.network.addresses[3] == (0, 1, 0)
    # Independent relativistic mass-shell check, c=1, mass 12, photon 6 -> 3.
    assert 15 * 15 - 9 * 9 == 12 * 12
    assert 12 + 6 == 15 + 3 and 0 + 6 == 9 - 3


def test_open_escape_retains_correlations_and_records_exact_exited_quantities():
    world = QuantumExperiment(parse_quantum_initialization(document("photon-open-escape.json")))
    for tick in range(1, 7):
        world.step()
        snapshot = world.snapshot()
        assert fraction(snapshot["escaped"]["radiation_number"]) == (1 if tick >= 5 else 0)
        assert fraction(snapshot["retained"]["energy"]) + fraction(snapshot["escaped"]["energy"]) == 18
    assert coherence(world) == 0
    assert all(m["ownership"] == "escaped" for m in snapshot["modes"][2:])
    assert not world.network.records


@pytest.mark.parametrize("axis", [0, 1, 2])
@pytest.mark.parametrize("sign", [-1, 1])
def test_periodic_return_is_cardinal_on_every_axis_and_orientation(axis, sign):
    raw = document()
    axes = [axis] + [i for i in range(3) if i != axis]
    old_shape = raw["shape"][:]
    for i, j in enumerate(axes):
        raw["shape"][j] = old_shape[i]
    for mode in raw["modes"]:
        old = mode["position"][:]
        for i, j in enumerate(axes):
            mode["position"][j] = old[i]
        mode["position"][axis] = (sign * mode["position"][axis]) % raw["shape"][axis]
    for action in raw["actions"]:
        if action["kind"] == "link":
            action["port"] = 2 * axis + (1 if sign < 0 else 0)
    assert coherence(run(raw)) == Fraction(1, 2)


def test_uniform_local_cost_wait_and_transit_ownership_have_no_debt():
    raw = document()
    raw["actions"] = raw["actions"][:2]
    raw["link_ticks"] = 2
    raw["normal_budget"] = 1
    raw["ticks"] = 8
    # Two simultaneous one-cost local mode departures: extra=(2/1 - 1)*2=2.
    world = QuantumExperiment(parse_quantum_initialization(raw))
    assert [(a.departure, a.end) for a in world.initial.actions] == [(2, 4), (2, 4)]
    for tick in range(5):
        status = world.snapshot()["modes"][2]["ownership"]
        assert status == ("waiting" if tick < 2 else "in_flight" if tick < 4 else "resident")
        if tick < 4:
            assert world.network.addresses[2] == (3, 0, 0)
        world.step()
    # A later one-cost cycle has no residual computation debt.
    raw["actions"].append(
        {"tick": 4, "kind": "link", "modes": ["probe 0 polarization 0"], "port": 0, "cost": 1}
    )
    later = parse_quantum_initialization(raw).actions[-1]
    assert (later.departure, later.end) == (4, 6)


def test_invalid_remote_gate_noncausal_reuse_and_sector_violation_fail_loading():
    bad = document()
    next(a for a in bad["actions"] if a["kind"] == "local")["tick"] = 0
    with pytest.raises(ValueError, match="same cell"):
        parse_quantum_initialization(bad)
    bad = document()
    bad["actions"].append(deepcopy(bad["actions"][0]))
    with pytest.raises(ValueError, match="reserved"):
        parse_quantum_initialization(bad)
    bad = document("photon-recoil.json")
    bad["modes"][1]["quantities"]["px"] = 8
    with pytest.raises(ValueError, match="sector"):
        parse_quantum_initialization(bad)
    bad = document("photon-open-escape.json")
    bad["actions"].append(
        {
            "tick": 5,
            "kind": "observe",
            "modes": ["probe 0 polarization 0"],
            "rule": "position observation",
            "ticket": 0,
            "cost": 1,
        }
    )
    with pytest.raises(ValueError, match="escaped"):
        parse_quantum_initialization(bad)


def test_remote_work_never_changes_the_source_departure():
    raw = document()
    raw["normal_budget"] = 1
    raw["rules"]["phase"] = {"matrix": [[1, 0], [0, -1]]}
    raw["actions"] = [
        raw["actions"][0],
        {"tick": 0, "kind": "local", "modes": ["target A"], "rule": "phase", "cost": 4},
    ]
    initial = parse_quantum_initialization(raw)
    assert (initial.actions[0].departure, initial.actions[0].end) == (0, 1)
    assert (initial.actions[1].departure, initial.actions[1].end) == (3, 4)
    assert run(raw).network.addresses[2] == (0, 0, 0)


def test_invalid_ticket_and_arrival_capacity_are_atomic_failures():
    raw = document("conditioned-target-path.json")
    next(a for a in raw["actions"] if a["kind"] == "observe")["ticket"] = 2
    world = QuantumExperiment(parse_quantum_initialization(raw))
    for _ in range(3):
        world.step()
    shared = world.event_space
    history = shared.events
    before = (world.network.events, world.network.heads, world.network.addresses, world.snapshot())
    with pytest.raises(ValueError, match="ticket"):
        world.step()
    assert (
        world.network.events,
        world.network.heads,
        world.network.addresses,
        world.snapshot(),
    ) == before
    assert shared is world.network.event_space and shared.events == history
    assert world.tick == 3 and world.network.successful_queries == 0
    from event_universe.quantum import DeferredQuantum

    net = DeferredQuantum().bind_event_network(EventNetworkConfig(((0, 0, 0), (1, 0, 0)), (0,)))
    with pytest.raises(OverflowError, match="capacity"):
        net.advance((), transfers=((0, (1, 0, 0)),))
    assert net.tick == 0 and net.addresses == net.config.addresses


def test_shared_provenance_tracks_completed_arrivals_across_host_checkpoints():
    events = CausalEventSpace(shape=(4, 1, 1), boundary="periodic", link_ticks=2)
    root = events.append(tick=0, addresses=((0, 0, 0),), owner="other", kind="source")
    # The joint source also supports the destination; that must not waive transit.
    config = EventNetworkConfig(
        ((3, 0, 0), (0, 0, 0)),
        modes_per_cell=2,
        shape=(4, 1, 1),
        boundary="periodic",
        initial_state=((1, Amplitude(1, 0)), (2, Amplitude(1, 0))),
    )
    net = DeferredQuantum().bind_event_network(config, event_space=events)
    source = net.heads[0]
    before = events.events
    with pytest.raises(ValueError, match="completed local link"):
        net.advance((), transfers=((0, (0, 0, 0)),))
    assert net.tick == 0 and events.events == before
    net.advance(())
    checkpoint = net.checkpoint(0)
    net.advance((), transfers=((0, (0, 0, 0)),))
    arrival = events.event(net.heads[0])
    assert arrival.tick == 2 and arrival.addresses == ((0, 0, 0),)
    assert arrival.physical_parents == (source,) and checkpoint in arrival.parents
    assert net.event_space is events and events.event(root.id) is root
    assert net.joint_state() == config.initial_state
    with pytest.raises(ValueError, match="completed local link"):
        net.advance((), transfers=((0, (1, 0, 0)),))
    assert net.tick == 2


def test_staged_metadata_cannot_overwrite_another_owners_append():
    events = CausalEventSpace()
    staged = events.stage()
    staged.append(tick=0, addresses=((0, 0, 0),), owner="quantum", kind="operation", model_cost=3)
    external = events.append(tick=0, addresses=((0, 0, 0),), owner="other", kind="source")
    with pytest.raises(ValueError, match="stale"):
        events.adopt(staged)
    assert events.events == (external,) and events.model_cost == 0
    staged = events.stage()
    saved = staged.append(
        tick=1, addresses=((0, 0, 0),), owner="quantum", kind="operation", model_cost=3
    )
    events.adopt(staged)
    assert events.events == (external, saved) and events.model_cost == 3
    staged.append(tick=2, addresses=((0, 0, 0),), owner="quantum", kind="later")
    assert events.events == (external, saved)


def test_initial_and_matrix_bounds_and_local_arity_are_enforced():
    with pytest.raises(ValueError, match="duplicate"):
        EventNetworkConfig(((0, 0, 0),), initial_state=((1, Amplitude(1, 0)), (1, Amplitude(1, 0))))
    with pytest.raises(OverflowError):
        EventNetworkConfig(((0, 0, 0),), initial_state=((1, Amplitude(1 << 30, 0)),))
    with pytest.raises(ValueError):
        LocalUnitary(tuple(tuple(Amplitude(int(i == j), 0) for j in range(32)) for i in range(32)))
    bad = document()
    bad["budgets"] = {"max_nodes": 4}
    world = QuantumExperiment(parse_quantum_initialization(bad))
    world.step()
    world.step()
    before = world.network.events
    with pytest.raises(OverflowError, match="node budget"):
        world.step()
    assert world.network.events == before and world.tick == 2


def test_labels_and_declaration_order_do_not_change_physical_results():
    raw = document("three-photon-decoherence.json")
    baseline = run(raw)
    rename = {
        m["name"]: n
        for m, n in zip(
            raw["modes"],
            ["constructor", "__proto__", "local", "observe", "rule", "tick", "port", "target"],
            strict=True,
        )
    }
    for mode in raw["modes"]:
        mode["name"] = rename[mode["name"]]
    for term in raw["state"]:
        term["occupied"] = [rename[n] for n in term["occupied"]]
    for action in raw["actions"]:
        action["modes"] = [rename[n] for n in action["modes"]]
    raw["groups"] = {n: [rename[q] for q in qs] for n, qs in raw["groups"].items()}
    raw["modes"].reverse()
    raw["quantities"].reverse()
    renamed = run(raw)
    assert baseline.snapshot()["groups"] == renamed.snapshot()["groups"]
    assert baseline.snapshot()["retained"] == renamed.snapshot()["retained"]
    assert renamed.tick == 9 and renamed.network.events != ()
    assert [a.cost for a in baseline.initial.actions] == [a.cost for a in renamed.initial.actions]


def test_headless_cli_retains_source_input_trace_and_failure(tmp_path):
    output = tmp_path / "complete"
    result = run_experiment(EXAMPLES / "photon-return-erasure.json", output, checkpoint_every=3)
    assert result["status"] == "completed" and result["source_sha256"]
    assert result["visualization"] is False
    assert {p.name for p in output.iterdir()} == {
        "initialization.json",
        "observations.jsonl",
        "events.jsonl",
        "causal-events.jsonl",
        "result.json",
    }
    assert len((output / "observations.jsonl").read_text().splitlines()) == 8
    invalid = tmp_path / "invalid.json"
    raw = document("conditioned-target-path.json")
    next(a for a in raw["actions"] if a["kind"] == "observe")["ticket"] = 10
    invalid.write_text(json.dumps(raw))
    with pytest.raises(ValueError):
        run_experiment(invalid, tmp_path / "failed")
    assert json.loads((tmp_path / "failed" / "failure.json").read_text())["last_committed_tick"] == 3
    code = "from pathlib import Path; from event_universe.runner import run_initialization; import sys; run_initialization(Path(sys.argv[1]), Path(sys.argv[2])); assert not any(n.split('.')[0] in {'matplotlib', 'numpy', 'PIL'} for n in sys.modules)"
    child = subprocess.run(
        [
            sys.executable,
            "-B",
            "-c",
            code,
            str(EXAMPLES / "photon-recoil.json"),
            str(tmp_path / "standard-cli"),
        ],
        text=True,
        capture_output=True,
    )
    assert child.returncode == 0, child.stderr
