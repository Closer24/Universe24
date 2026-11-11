"""Passive snapshot observations; never supplies a next state or changes it."""
from fractions import Fraction

import numpy as np

from universe24.layers.transported_probe import COFRAME, CLOCKS


def metric(state, tensor):
    ids = [tensor.gear_index(name) for name in COFRAME]
    e = state.b[ids].astype(object).T.reshape(state.N, 4, 4)
    eta = np.diag(np.array([-1, 1, 1, 1], dtype=object))
    return e, e.transpose(0, 2, 1) @ eta @ e


def sample(state, tensor, step):
    """Locate the packet from actual support, including odd staggered steps."""
    occupied = []
    for bank in ("X", "Y"):
        row = state.b[tensor.gear_index(f"probe.{bank}")]
        occupied += [(bank, int(node), int(row[node])) for node in np.flatnonzero(row)]
    if len(occupied) != 1:
        raise ValueError("Not a single localized marker packet")
    bank, node, amplitude = occupied[0]
    if amplitude <= 0:
        raise ValueError("Nonpositive marker amplitude")
    phases = {}
    for clock in CLOCKS:
        ids = [tensor.gear_index(f"{clock}.{b}{j}") for b in ("X", "Y") for j in (0, 1)]
        values = state.b[ids]
        support = set(map(int, np.flatnonzero(np.any(values != 0, axis=0))))
        if support != {node}:
            raise ValueError("Clock is not carried with the marker")
        other = "Y" if bank == "X" else "X"
        if any(state.b[tensor.gear_index(f"{clock}.{other}{j}"), node] for j in (0, 1)):
            raise ValueError("Clock bank does not match the marker bank")
        phases[clock] = [int(state.b[tensor.gear_index(f"{clock}.{bank}{j}"), node]) for j in (0, 1)]
    _, g = metric(state, tensor)
    xyz = state.lattice.coords(node)
    return dict(step=step, node=node, board_xyz=list(xyz), bank=bank,
                amplitude=amplitude, clock_phases=phases,
                metric=[[int(v) for v in row] for row in g[node]])


def fraction_record(value):
    value = Fraction(value)
    return dict(numerator=value.numerator, denominator=value.denominator)


def assess(state, tensor, samples):
    """Restricted stationary pp-wave diagnostics, not a generic metric solver.

    Use even microsteps (t=2n,z=z0+n). Tick events are actual phase returns;
    the flat unit calibrations are fixed once: control 4 sqrt(3), candidate
    6 sqrt(3). Only complete tick intervals yield a measured rate.
    """
    even = samples[::2]
    origin = even[0]
    steps = [s["step"] for s in even]
    if steps != list(range(0, samples[-1]["step"]+1, 2)):
        raise ValueError("Missing observation slots")
    x, y, z = origin["board_xyz"]
    transport_ok = all(s["board_xyz"] == [x, y, (z+n) % state.L]
                       and s["bank"] == "X" for n, s in enumerate(even))
    e, all_g = metric(state, tensor)
    node = origin["node"]
    g = all_g[node]
    tangent = np.array([2, 0, 0, 1], dtype=object)
    norm = int(tangent @ g @ tangent)
    # For g=eta+2F (dt-dz)^2 and this constant tangent, the only residuals
    # are -F_x and -F_y. Centered differences are exact inside this chart.
    profile = e[:, 0, 3]
    gradients, hessian = [], []
    for direction in ((1, 0, 0), (0, 1, 0)):
        plus = state.lattice.shift_index(direction)[node]
        minus = state.lattice.shift_index(tuple(-v for v in direction))[node]
        gradients.append(Fraction(int(profile[plus]-profile[minus]), 2))
        hessian.append(int(profile[plus]-2*profile[node]+profile[minus]))
    interior = all(0 < v < state.L-1 for v in (x, y))
    residual = [Fraction(0), -gradients[0], -gradients[1], Fraction(0)]
    geodesic_ok = transport_ok and interior and all(v == 0 for v in residual)
    timelike = norm < 0
    expected_rate_squared = Fraction(-norm, 4) if timelike else None
    clock_reports = {}
    for clock, flat_period in (("control", 4), ("candidate", 6)):
        initial = origin["clock_phases"][clock]
        ticks = [s["step"] for s in even if s["clock_phases"][clock] == initial]
        intervals = [b-a for a, b in zip(ticks, ticks[1:])]
        rates = [Fraction(3*flat_period**2, dt**2) for dt in intervals]
        passed = bool(rates) and timelike and all(rate == expected_rate_squared for rate in rates)
        clock_reports[clock] = dict(tick_steps=ticks, intervals=intervals,
            calibration=f"{flat_period}*sqrt(3) proper-time units per full cycle",
            measured_rate_squared=[fraction_record(rate) for rate in rates],
            matches_metric=passed, insufficient_ticks=not bool(rates))
    # Audit the known coframe inverse E^-1=2I-E over the whole board.
    identity = np.eye(4, dtype=object)
    invertible = bool(np.all(e @ (2*identity-e) == identity))
    return dict(actual_board_transport=transport_ok, timelike=timelike,
        metric_norm_per_macrostep=norm,
        predicted_proper_rate_squared=(fraction_record(expected_rate_squared) if timelike else None),
        transverse_geodesic_residual=[fraction_record(v) for v in residual],
        geodesic_matches=geodesic_ok, interior_chart=interior,
        transverse_profile_hessian_diagonal=hessian,
        nonflat_at_probe=any(v != 0 for v in hessian),
        coframe_inverse_certificate=invertible,
        clocks=clock_reports,
        common_metric_passes=geodesic_ok and timelike and invertible
            and all(c["matches_metric"] for c in clock_reports.values()))
