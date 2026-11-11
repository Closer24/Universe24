"""Exact, optional global resolution lift; construction-time tensor data only.

For a positive integer M, multiply EVERY coefficient and Q by M. If the
explicit initial remainder is also multiplied by M, the complete lifted
trajectory has identical a, b and quotient values, and remainders multiplied
by M. This embeds the original system into an invariant subset of the larger
remainder space. It does not change Rule3, add gears or change any coupling.

Adding unscaled interactions afterwards defines a different candidate law;
the embedding theorem then applies only to its zero-added-coupling baseline.
The larger Q is an optional resolution choice, not a derived physical scale.
"""
from __future__ import annotations

from ..core.tensor import Monomial, Tensor


def _source_parameters(tensor: Tensor, factor: int, Q: int | None) -> int:
    """Validate a source law and return its explicit positive integer Q."""
    if not isinstance(tensor, Tensor):
        raise TypeError("source tensor must be a Tensor")
    if type(factor) is not int or factor < 1:
        raise ValueError("resolution factor must be a positive Python int")
    if Q is not None and (type(Q) is not int or Q < 1):
        raise ValueError("source Q must be a positive Python int")
    if Q is None:
        Q = tensor.Q
    if Q is None:
        raise ValueError("source tensor has no Q; supply its engine Q explicitly")
    if tensor.Q is not None and tensor.Q != Q:
        raise ValueError(f"source tensor was built with Q={tensor.Q}, not Q={Q}")
    return Q


def lift_tensor(tensor: Tensor, factor: int, *, Q: int | None = None) -> Tensor:
    """Return the exact baseline lift of ``tensor`` by ``factor``.

    ``Q`` is needed only when the source tensor does not record its divisor.
    Gear order, labels, link axes, field signs, one-way designations, factors,
    polynomial degree, locality and the old-a dependency DAG are preserved.
    The source is never mutated; factor=1 returns an equal independent tensor
    when the source already records Q (otherwise Q is added as metadata).
    An explicit source state must be lifted with ``prepare.resolution`` rather
    than recreated using a vacuum formula at the new Q.
    """
    source_Q = _source_parameters(tensor, factor, Q)
    monomials = [Monomial(m.target, factor * m.coeff, m.factors)
                 for m in tensor.monomials]
    designations = [(target, factors, why)
                    for (target, factors), why in tensor.designations.items()]
    return Tensor(tensor.gears, monomials, designated_one_way=designations,
                  Q=factor * source_Q)


__all__ = ["lift_tensor"]
