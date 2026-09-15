"""Host optimizations retain exact quantities, fresh observations and integer errors."""

from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE, decode, encode, pack, unpack
from event_universe.initialization import load_initial_state

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("size", [0, 1, 2, 3, 4, 16, 32])
def test_payload_shapes_keep_component_order_and_exact_round_trip(size):
    values = tuple((-1 if index % 2 else 1) * index for index in range(size))
    expected = tuple(encode(value) for value in values)
    assert pack(values) == expected
    assert unpack(expected) == tuple(decode(value) for value in expected) == values


@pytest.mark.parametrize("size", [1, 3, 32])
@pytest.mark.parametrize("bad", [True, 1.0, MAX_VALUE + 1, -MAX_VALUE - 1])
def test_packing_does_not_remove_any_integer_bound_check(size, bad):
    for position in range(size):
        values = [0] * size
        values[position] = bad
        with pytest.raises(ValueError, match="disturbance integer bound"):
            pack(tuple(values))


@pytest.mark.parametrize("size", [1, 3, 32])
@pytest.mark.parametrize("bad", [True, 1.0, 0, -1, 2 * MAX_VALUE + 2])
def test_unpacking_does_not_remove_any_code_check(size, bad):
    for position in range(size):
        values = [1] * size
        values[position] = bad
        with pytest.raises(ValueError, match="positive integer component code"):
            unpack(tuple(values))


def test_payload_integer_endpoints_are_unchanged():
    assert pack((-MAX_VALUE, 0, MAX_VALUE)) == (2 * MAX_VALUE, 1, 2 * MAX_VALUE + 1)
    assert unpack((2 * MAX_VALUE, 1, 2 * MAX_VALUE + 1)) == (-MAX_VALUE, 0, MAX_VALUE)


@pytest.mark.parametrize(
    "example",
    [
        "basic.json",
        "moving_source.json",
        "finite_fields.json",
        "local_field_rules.json",
        "open_world.json",
    ],
)
def test_one_fresh_accounting_read_matches_the_independent_existing_interfaces(example, monkeypatch):
    initial = load_initial_state(ROOT / "examples" / example)
    with Simulation(initial) as world:
        for _ in range(6):
            expected = world.totals(), world.spatial_accounting()
            if world._spatial is None:
                assert world.accounting_snapshot() == expected
            else:
                spatial = world._spatial
                original = spatial.totals
                calls = []

                def counted(calls=calls, original=original):
                    calls.append(1)
                    return original()

                with monkeypatch.context() as patch:
                    patch.setattr(spatial, "totals", counted)
                    captured = world.accounting_snapshot()
                assert len(calls) == 1
                assert captured == expected
                # A returned report must not be aliased to a later calculation.
                world.totals()
                assert captured == expected
            world.step()


def test_focused_totals_do_not_enumerate_empty_carrier_history():
    from event_universe.initialization import parse_initial_state

    from .test_local_focus import moving_document

    raw = moving_document()
    raw.update(boundary="open", focus=True)
    with Simulation(parse_initial_state(raw)) as world:
        for _ in range(10):
            world.step()
        expected = world.totals()

        class NoScan(dict):
            def __iter__(self):
                pytest.fail("totals scanned empty carrier history")

            def values(self):
                pytest.fail("totals scanned empty carrier history")

        world._nodes = NoScan(world._nodes)
        assert world.totals() == expected


def test_explicit_focus_opt_out_is_preserved():
    initial = load_initial_state(ROOT / "examples/basic.json")
    assert initial.focus is True
    with Simulation(replace(initial, focus=False)) as world:
        assert world.execution_report()["focus_enabled"] is False
