"""Optional reciprocal clock/record coupling; fixed tensor data only.

The caller supplies three distinct scalar node gears with field sign +1. The
potential Phi = -kappa * clock * (positive + negative) gives equal forces on the
recording pair and makes its sum, rather than only its difference, observable to
an evolving clock. No click callback, state comparison or extra update is used.

This is a new coupling hypothesis. It preserves the matched-pair difference
identity under its stated conditions, but modifies each individual quotient
ledger. It does not derive collapse, a Born rule, complexity selection or GR.
"""
from __future__ import annotations

from ..core.tensor import Block

ZERO = (0, 0, 0)


def build_clock_record_bridge(*, Q: int, clock: str, positive: str, negative: str,
                              kappa: int, include_free_clock: bool = False) -> Block:
    """Return an additive block; gears must already be declared by the caller.

    Names are global (normally qualified, e.g. ``clock.local``, ``cosmic.dp``).
    The three gears must be scalar node gears with field sign +1 for the stated
    reciprocity and strict on-site support. Composition with strict_support=True validates geometric support;
    the reciprocity checker validates the signs of the composed tensor.

    With ``include_free_clock=True``, also add u_clock=(D/2)*b_clock, an isolated
    period-six clock when uncoupled. Do not add that inertia twice. The isolated
    clock/pair linear block has all eigenvalues strictly inside (-D,D) when
    0 <= kappa < D/2. This linear band condition is not a bound for an arbitrary
    composed nonlinear system or a proof of bounded integer trajectories.
    """
    if type(Q) is not int or Q <= 0:
        raise ValueError('Q must be a positive integer')
    if type(kappa) is not int or kappa < 0:
        raise ValueError('kappa must be a non-negative integer')
    if type(include_free_clock) is not bool:
        raise TypeError('include_free_clock must be a bool')
    names = (clock, positive, negative)
    if any(type(name) is not str or not name.strip() for name in names):
        raise ValueError('clock and record names must be non-empty strings')
    if len(set(names)) != 3:
        raise ValueError('clock and record gears must be distinct')
    f = lambda gear: (gear, ZERO, 'b')
    terms = []
    if kappa:
        terms.extend([
            (clock, -kappa, (f(positive),)),
            (clock, -kappa, (f(negative),)),
            (positive, -kappa, (f(clock),)),
            (negative, -kappa, (f(clock),)),
        ])
    D = 6 * Q
    if include_free_clock:
        terms.append((clock, D // 2, (f(clock),)))
    return Block((), tuple(terms), name=None, Q=Q,
        params=dict(clock=clock,positive=positive,negative=negative,kappa=kappa,
                    include_free_clock=include_free_clock,
                    isolated_remainder_free_band=2*kappa < D,
                    required_field_signs=[1,1,1],required_link_axes=[None,None,None]),
        doc='optional reciprocal scalar clock / recording-sum bridge; no new forward primitive')
