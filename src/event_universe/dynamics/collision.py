"""Local two-body elastic backscattering with bounded rational momentum.

The relative velocity reverses in the center-of-mass frame. This is an explicit
classical point-contact choice, not a relativistic or finite-radius solver.
"""

from typing import NamedTuple

from event_universe.core.state import Vector, bounded_gcd, checked, checked_work, reduced_vector


class CollisionBody(NamedTuple):
    momentum: Vector
    mass: int
    denominator: int = 1


class CollisionResult(NamedTuple):
    first: CollisionBody
    second: CollisionBody


def elastic_backscatter(first: CollisionBody, second: CollisionBody) -> CollisionResult:
    """Conserve pair momentum and sum(p squared / (2 mass)) without rounding."""
    for body in (first, second):
        if len(body.momentum) != 3:
            raise ValueError("three momentum components required")
        for value in (*body.momentum, body.mass, body.denominator):
            checked(value)
        if body.mass <= 0 or body.denominator <= 0:
            raise ValueError("positive mass and momentum denominator required")
    m1, m2 = first.mass, second.mass
    common = checked_work(
        (first.denominator // bounded_gcd(first.denominator, second.denominator)) * second.denominator
    )
    denominator = checked_work(common * checked_work(m1 + m2))

    def component(axis: int) -> tuple[int, int]:
        p1 = checked_work(first.momentum[axis] * (common // first.denominator))
        p2 = checked_work(second.momentum[axis] * (common // second.denominator))
        a = checked_work(checked_work((m1 - m2) * p1) + checked_work(checked_work(2 * m1) * p2))
        b = checked_work(checked_work(checked_work(2 * m2) * p1) + checked_work((m2 - m1) * p2))
        return a, b

    x, y, z = component(0), component(1), component(2)
    p1_out, d1 = reduced_vector((x[0], y[0], z[0]), denominator)
    p2_out, d2 = reduced_vector((x[1], y[1], z[1]), denominator)
    return CollisionResult(CollisionBody(p1_out, m1, d1), CollisionBody(p2_out, m2, d2))
