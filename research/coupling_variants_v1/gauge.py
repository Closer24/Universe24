"""Data-only transport of a preparation between gauge-equivalent couplings.

``J(a, b, r) = (-a, -b, 4 - r + 2*(r mod 2))`` satisfies
``forward(J(s), -u) = J(forward(s, u))`` (r05, T3). Applying J to every channel
outside 2T (``character(g) == -1``) therefore conjugates the dynamics of a
coupling with body weights ``w_u`` to that of ``VariantCoupling.chi_gauged``
(body weights ``character(B_u) * w_u``), because ``character(g) *
character(g*B_u) = character(B_u)``. The map is global (a group character), so
it needs no region or parity condition; it needs a J-invariant background,
i.e. ``r`` in {2, 3}. For the reference tables it sends the signs
``(sx, sy, sz)`` to ``(sx, -sy, -sz)``, the chi-gauge r03 and r05 used.

On an even side, J on every channel of the sites with odd ``x+y+z`` likewise
conjugates body weights ``w_u`` to ``-w_u`` (``staggered_state``); on an odd side
the wrap-around bonds join equal parities and the map fails.

These are preparation steps (data generators), not evolution stages.
"""
from __future__ import annotations

from universe24.core.state import Channel, State

from .coupling import character


def flip(triple) -> Channel:
    """J: negate both counters and reflect the remainder within its parity class."""
    a, b, r = triple
    return Channel(-a, -b, 4 - r + 2 * (r % 2))


def chi_gauge_state(state: State) -> State:
    """J on the 24 channels outside 2T, every site; an involution."""
    if flip(state.background) != state.background:
        raise ValueError("chi gauge needs a J-invariant background: (0, 0, 2) or (0, 0, 3)")
    return State(state.cube, state.background,
                 {address: flip(value) if character(address[3]) < 0 else value
                  for address, value in state.cells.items()})


def staggered_state(state: State) -> State:
    """J on every channel of the odd-parity sites; needs an even side. An involution."""
    if flip(state.background) != state.background:
        raise ValueError("staggered gauge needs a J-invariant background: (0, 0, 2) or (0, 0, 3)")
    if state.cube.side % 2:
        raise ValueError("staggered gauge needs an even side")
    return State(state.cube, state.background,
                 {address: flip(value) if sum(address[:3]) % 2 else value
                  for address, value in state.cells.items()})
