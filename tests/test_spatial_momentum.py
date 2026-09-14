"""Independent finite lattice expectations from actual evolved quantum states."""

from fractions import Fraction

import pytest

from event_universe.core.event_space import CausalEventSpace
from event_universe.quantum import DeferredQuantum, EventNetworkConfig, LocalUnitary
from event_universe.quantum.operations import dephasing, integer_matrix, permutation
from event_universe.quantum.state import Amplitude
from examples.quantum.spatial_momentum import local_position_moments, spatial_moments

SQUARE = ((0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0))
RING = ((0, 1), (1, 2), (2, 3), (3, 0))
CHAIN = ((0, 1), (1, 2))
SWAP = permutation((0, 2, 1, 3))
# Equal coherent splitting needs a common squared norm 2 also on vacuum and
# double occupation. Gaussian integer 1+i supplies it without square roots.
SPLIT = LocalUnitary(
    tuple(
        tuple(Amplitude(real, imag) for real, imag in row)
        for row in (
            ((1, 1), (0, 0), (0, 0), (0, 0)),
            ((0, 0), (1, 0), (1, 0), (0, 0)),
            ((0, 0), (1, 0), (-1, 0), (0, 0)),
            ((0, 0), (0, 0), (0, 0), (1, 1)),
        )
    )
)


def network(addresses=SQUARE, occupied=(0,)):
    return DeferredQuantum().bind_event_network(EventNetworkConfig(addresses, occupied))


def phase(real, imag):
    zero = Amplitude(0, 0)
    return LocalUnitary(((Amplitude(1, 0), zero), (zero, Amplitude(real, imag))))


def uniform_ring():
    graph = network()
    graph.step(((SPLIT, (0, 1)),))
    graph.step(((SPLIT, (0, 3)), (SPLIT, (1, 2))))
    return graph


def assert_moments(graph, registers, edges, mean, second, variance):
    before = graph.tick, graph.events, graph.records, graph.heads
    result = spatial_moments(graph, registers, edges)
    assert result == {
        "status": "single_excitation",
        "occupation_probability": Fraction(1),
        "mean_momentum": mean,
        "second_moment": second,
        "variance": variance,
    }
    assert (graph.tick, graph.events, graph.records, graph.heads) == before
    return result


@pytest.mark.parametrize("sign", [-1, 1])
def test_oriented_ring_phase_gradient_has_sharp_nonzero_momentum(sign):
    graph = uniform_ring()
    graph.step(((phase(0, sign), (1,)), (phase(-1, 0), (2,)), (phase(0, -sign), (3,))))
    assert_moments(graph, (0, 1, 2, 3), RING, 2 * sign, 4, 0)
    reversed_edges = tuple((b, a) for a, b in RING)
    assert_moments(graph, (0, 1, 2, 3), reversed_edges, -2 * sign, 4, 0)


def test_equal_position_probabilities_do_not_determine_momentum_variance():
    graph = uniform_ring()
    weights = [graph.query(index).weights for index in range(4)]
    assert_moments(graph, (0, 1, 2, 3), RING, 0, 0, 0)
    graph.step(tuple((dephasing(2), (index,)) for index in range(4)))
    assert [graph.query(index).weights for index in range(4)] == weights
    assert_moments(graph, (0, 1, 2, 3), RING, 0, 2, 2)


@pytest.mark.parametrize("register", range(4))
def test_ring_position_state_matches_local_row_reencoding(register):
    result = assert_moments(network(occupied=(register,)), (0, 1, 2, 3), RING, 0, 2, 2)
    local = local_position_moments((-1, 1))
    assert all(type(value) is int for value in local.values())
    assert local == {key: result[key] for key in local}


@pytest.mark.parametrize("register,second", [(0, 1), (1, 2), (2, 1)])
def test_open_chain_localization_depends_on_its_actual_boundary_row(register, second):
    graph = network(tuple((i, 0, 0) for i in range(3)), (register,))
    assert_moments(graph, (0, 1, 2), CHAIN, 0, second, second)
    row = {0: (-1,), 1: (1, -1), 2: (1,)}[register]
    assert local_position_moments(row) == {
        "mean_momentum": 0,
        "second_moment": second,
        "variance": second,
    }


@pytest.mark.parametrize("sign,second", [(1, 0), (-1, 2)])
def test_open_chain_endpoint_phase_changes_second_moment(sign, second):
    graph = network(tuple((i, 0, 0) for i in range(3)), (1,))
    graph.step(((SPLIT, (1, 0)),))
    graph.step(((SWAP, (1, 2)),))
    graph.step(((phase(sign, 0), (2,)),))
    assert_moments(graph, (0, 1, 2), CHAIN, 0, second, second)


def test_vacuum_is_unavailable_and_partial_occupation_is_explicit():
    graph = network(occupied=())
    assert spatial_moments(graph, (0, 1, 2, 3), RING) == {
        "status": "vacuum",
        "occupation_probability": Fraction(0),
        "mean_momentum": None,
        "second_moment": None,
        "variance": None,
    }
    graph.step(((LocalUnitary(integer_matrix(((1, 1), (1, -1)))), (0,)),))
    assert spatial_moments(graph, (0, 1, 2, 3), RING) == {
        "status": "partial_occupation",
        "occupation_probability": Fraction(1, 2),
        "mean_momentum": Fraction(0),
        "second_moment": Fraction(2),
        "variance": Fraction(2),
    }


def test_register_order_and_unselected_environment_do_not_relabel_spatial_modes():
    graph = uniform_ring()
    graph.step(((phase(0, 1), (1,)), (phase(-1, 0), (2,)), (phase(0, -1), (3,))))
    assert_moments(graph, (2, 0, 3, 1), RING, 2, 4, 0)
    # An independent occupied register is outside the selected spatial sector.
    graph = network((*SQUARE, (2, 1, 0)), (0, 4))
    assert_moments(graph, (0, 1, 2, 3), RING, 0, 2, 2)


def test_periodic_edge_is_valid_only_in_the_declared_event_space_topology():
    addresses = tuple((i, 0, 0) for i in range(4))
    graph = DeferredQuantum().bind_event_network(
        EventNetworkConfig(addresses, (0,)),
        event_space=CausalEventSpace(shape=(4, 1, 1), boundary="periodic"),
    )
    assert_moments(graph, (0, 1, 2, 3), RING, 0, 2, 2)
    with pytest.raises(ValueError, match="neighboring Links"):
        spatial_moments(network(addresses), (0, 1, 2, 3), RING)


def test_entangled_unselected_environment_changes_reduced_spatial_coherence():
    graph = network((*SQUARE, (2, 0, 0)))
    graph.step(((SPLIT, (0, 1)),))
    graph.step(((SPLIT, (0, 3)), (SPLIT, (1, 2))))
    graph.step(((phase(0, 1), (1,)), (phase(-1, 0), (2,)), (phase(0, -1), (3,))))
    # Controlled flip from spatial mode 1 to its adjacent environment register.
    graph.step(((permutation((0, 3, 2, 1)), (1, 4)),))
    assert_moments(graph, (0, 1, 2, 3), RING, 1, 3, 2)
    assert not graph.records


def test_isolated_position_row_has_no_incident_operator_entries():
    assert local_position_moments(()) == {
        "mean_momentum": 0,
        "second_moment": 0,
        "variance": 0,
    }
    assert_moments(network(((0, 0, 0),)), (0,), (), 0, 0, 0)


@pytest.mark.parametrize("row", [[1], (True,), (0,), (2,), (1,) * 7])
def test_local_reencoding_rejects_noninteger_or_unbounded_rows(row):
    with pytest.raises(ValueError, match="fixed local row"):
        local_position_moments(row)


@pytest.mark.parametrize(
    "registers,edges,message",
    [
        ((0, 0), (), "distinct bounded"),
        ((False,), (), "distinct bounded"),
        ((0, 1), ((0, 0),), "two distinct"),
        ((0, 1), ((0, 1), (1, 0)), "duplicate"),
        ((0, 1, 2), ((0, 2),), "neighboring Links"),
        ((0, 1), ((0, 2),), "two distinct"),
    ],
)
def test_invalid_spatial_graph_is_rejected_before_quantum_evaluation(registers, edges, message):
    graph = network()
    before = graph.tick, graph.events, graph.records, graph.heads
    with pytest.raises(ValueError, match=message):
        spatial_moments(graph, registers, edges)
    assert (graph.tick, graph.events, graph.records, graph.heads) == before


def test_multiple_excitations_are_not_silently_projected_into_one_particle():
    graph = network(occupied=(0, 1))
    with pytest.raises(ValueError, match="at most one excitation"):
        spatial_moments(graph, (0, 1, 2, 3), RING)


@pytest.mark.parametrize("invalid", ["dimension", "colocated"])
def test_spatial_modes_cannot_be_arbitrary_internal_registers(invalid):
    config = (
        EventNetworkConfig(((0, 0, 0),), dimensions=(3,), initial_levels=(1,))
        if invalid == "dimension"
        else EventNetworkConfig(((0, 0, 0), (0, 0, 0)), (0,), register_names=("first", "second"))
    )
    graph = DeferredQuantum().bind_event_network(config)
    with pytest.raises(ValueError, match="must be binary|locations must be distinct"):
        spatial_moments(graph, tuple(range(len(config.addresses))), ())
