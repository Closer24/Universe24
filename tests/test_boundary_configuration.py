"""Independent configured boundary and six-face geometry contracts."""

from typing import Any

import pytest

from event_universe.core.disturbance_state import MAX_VALUE, OPERATIONS, Address3
from event_universe.core.topology import neighbor_address
from event_universe.initialization import parse_initial_state


def document(version: int) -> dict[str, Any]:
    return {
        "schema_version": version,
        "model_id": "arbitrary-boundary-contract",
        "shape": [3, 4, 5],
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 10000,
        "ticks": 1,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "inventory", "components": 1, "units": "unit", "signed": True, "conserved": True}
        ],
        "disturbance_types": [
            {"name": "carrier", "fields": ["inventory"], "transport": {"mode": "hold"}}
        ],
        "seeds": [],
    }


@pytest.mark.parametrize("version", [1, 2])
def test_omitted_boundary_retains_periodic_default_in_each_schema(version: int) -> None:
    initial = parse_initial_state(document(version))
    assert initial.boundary == "periodic"
    assert initial.shape == (3, 4, 5)


@pytest.mark.parametrize("version", [1, 2])
@pytest.mark.parametrize("boundary", ["periodic", "open"])
def test_each_boundary_is_independent_of_schema_and_model_name(version: int, boundary: str) -> None:
    raw = document(version)
    raw["boundary"] = boundary
    initial = parse_initial_state(raw)
    assert initial.boundary == boundary
    assert initial.model_id == "arbitrary-boundary-contract"


@pytest.mark.parametrize("version", [1, 2])
@pytest.mark.parametrize(
    "boundary", [None, False, 0, [], {}, "", "closed", "absorbing", "Open", "open "]
)
def test_schema_rejects_unrecognized_or_nontext_boundary(version: int, boundary: object) -> None:
    raw = document(version)
    raw["boundary"] = boundary
    with pytest.raises(ValueError, match="boundary"):
        parse_initial_state(raw)


@pytest.mark.parametrize("boundary", ["periodic", "open"])
@pytest.mark.parametrize(
    ("port", "expected"),
    [
        (0, (2, 2, 3)),
        (1, (0, 2, 3)),
        (2, (1, 3, 3)),
        (3, (1, 1, 3)),
        (4, (1, 2, 4)),
        (5, (1, 2, 2)),
    ],
)
def test_six_interior_steps_have_the_same_geometry(boundary: str, port: int, expected: Address3) -> None:
    assert neighbor_address((1, 2, 3), port, (3, 4, 5), boundary) == expected


@pytest.mark.parametrize(
    ("port", "origin", "wrapped"),
    [
        (0, (2, 1, 1), (0, 1, 1)),
        (1, (0, 1, 1), (2, 1, 1)),
        (2, (1, 3, 1), (1, 0, 1)),
        (3, (1, 0, 1), (1, 3, 1)),
        (4, (1, 1, 4), (1, 1, 0)),
        (5, (1, 1, 0), (1, 1, 4)),
    ],
)
def test_periodic_faces_wrap_opposite_while_open_faces_have_no_destination(
    port: int, origin: Address3, wrapped: Address3
) -> None:
    assert neighbor_address(origin, port, (3, 4, 5), "periodic") == wrapped
    assert neighbor_address(origin, port, (3, 4, 5), "open") is None


@pytest.mark.parametrize("port", range(6))
def test_single_node_periodic_self_neighbor_and_open_escape(port: int) -> None:
    assert neighbor_address((0, 0, 0), port, (1, 1, 1), "periodic") == (0, 0, 0)
    assert neighbor_address((0, 0, 0), port, (1, 1, 1), "open") is None


def test_largest_valid_extent_wraps_without_overflow() -> None:
    shape = (MAX_VALUE, 1, 1)
    assert neighbor_address((MAX_VALUE - 1, 0, 0), 0, shape, "periodic") == (0, 0, 0)
    assert neighbor_address((0, 0, 0), 1, shape, "periodic") == (MAX_VALUE - 1, 0, 0)
    assert neighbor_address((MAX_VALUE - 1, 0, 0), 0, shape, "open") is None


@pytest.mark.parametrize(
    "shape",
    [
        None,
        [3, 4, 5],
        (),
        (3, 4),
        (3, 4, 5, 6),
        (0, 4, 5),
        (-1, 4, 5),
        (MAX_VALUE + 1, 4, 5),
        (True, 4, 5),
        (3, 4.0, 5),
    ],
)
def test_neighbor_rejects_invalid_immutable_bounded_extents(shape: Any) -> None:
    with pytest.raises(ValueError):
        neighbor_address((0, 0, 0), 0, shape, "periodic")


@pytest.mark.parametrize(
    "origin",
    [
        None,
        [1, 1, 1],
        (),
        (1, 1),
        (1, 1, 1, 1),
        (-1, 1, 1),
        (3, 1, 1),
        (1, 4, 1),
        (1, 1, 5),
        (MAX_VALUE + 1, 1, 1),
        (True, 1, 1),
        (1, 1.0, 1),
    ],
)
def test_neighbor_validates_all_origin_coordinates_before_wrapping(origin: Any) -> None:
    with pytest.raises(ValueError):
        neighbor_address(origin, 0, (3, 4, 5), "periodic")


@pytest.mark.parametrize("port", [-1, 6, MAX_VALUE + 1, True, 0.0, None])
def test_neighbor_rejects_invalid_cardinal_port(port: Any) -> None:
    with pytest.raises(ValueError):
        neighbor_address((1, 1, 1), port, (3, 4, 5), "open")


@pytest.mark.parametrize(
    "boundary", [None, False, 0, [], {}, "", "closed", "absorbing", "Periodic", "open "]
)
def test_neighbor_rejects_invalid_boundary_even_for_an_interior_step(boundary: Any) -> None:
    with pytest.raises(ValueError, match="boundary"):
        neighbor_address((1, 1, 1), 0, (3, 4, 5), boundary)
