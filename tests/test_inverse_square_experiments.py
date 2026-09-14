"""Host-side shell-stock probe and anisotropic node values."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "inverse_square_experiments", ROOT / "examples/inverse-square/run_experiments.py"
)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def test_every_manhattan_shell_carries_exactly_one_tick_of_emission():
    PROBE.configure(size=15, ticks=7, strength=8 * 3**5)
    world = PROBE.run(PROBE.conservative_document(with_receivers=False))
    shells = PROBE.shell_table(world, 6)
    assert [row["shell_nodes"] for row in shells] == [6, 18, 38, 66, 102, 146]
    assert all(row["shell_stock"] == PROBE.STRENGTH for row in shells)
    # The shell mean is therefore emission / (4R^2 + 2): inverse square in the mean.
    assert all(row["mean_times_4R2_plus_2_over_emission"] == 1.0 for row in shells)


def test_node_values_are_anisotropic_geometric_on_axes_and_slow_on_body_diagonal():
    PROBE.configure(size=15, ticks=7, strength=8 * 3**5)
    world = PROBE.run(PROBE.conservative_document(with_receivers=False))
    rays = {(row["direction"], row["steps"]): row for row in PROBE.direction_table(world, 6)}
    strength = PROBE.STRENGTH
    # Four octants share each axis node, each forwarding one third per link.
    assert [rays[("axis", k)]["value"] for k in range(1, 6)] == [
        strength // 6 // 3 ** (k - 1) for k in range(1, 6)
    ]
    # Same Manhattan radius 6: the body diagonal node holds far more than the axis node.
    assert rays[("body_diagonal", 2)]["manhattan_radius"] == rays[("axis", 6)]["manhattan_radius"]
    assert rays[("body_diagonal", 2)]["value"] > 10 * rays[("axis", 6)]["value"]
    # Edge case: the host flux projection has a positive outward component.
    for row in rays.values():
        if row["value"]:
            assert row["radial_flux"] > 0


def test_in_world_receiver_momentum_matches_host_flux_reading():
    PROBE.configure(size=15, ticks=7, strength=8 * 3**5)
    world = PROBE.run(PROBE.conservative_document(with_receivers=True))
    rows = {(row["direction"], row["steps"]): row for row in PROBE.receiver_table(world)}
    axis = rows[("axis", 1)]
    # Steady flux from tick 2 onward: six ticks of the same host-read flux.
    assert axis["momentum"] == (6 * axis["host_flux_now"][0], 0, 0)
    assert rows[("axis", 3)]["momentum"][0] < axis["momentum"][0]
