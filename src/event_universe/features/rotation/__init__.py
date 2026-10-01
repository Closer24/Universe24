"""The rotation of a two-part record (ALGEBRA.md #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record, the act a holder of the sign declares in the universe file): a plane's pair (re, im) turned by the angle theta with tan(theta / 2) = numerator / wall, in three shears, each x' = x + (a y) div d by Rule3's division act with no remainder kept and no new state; direction -1 subtracts the same three numbers in the reverse order, so the turn is a bijection of the integer pairs, inverted bit for bit (the back-in-time gate). In the rationals the turn is exactly a rotation (sin theta = 2 n w / (w^2 + n^2) and cos theta = (w^2 - n^2) / (w^2 + n^2) at the tangent half-angle n / w) and the integers' floors stand beside it, so a turned level stays within twice the amplitude while the tangent half-angle is at most 1 (`TURNED_REACH`; the loader's bound and the guard at load, `guard`). A positive numerator turns the plane counterclockwise, re + i im times e^(i theta): the Node's step turns the plane by the holder's time level against the sense of the record of positive Wronskian (z_before = z_now e^(i omega), clockwise), so that record rotates faster by theta in a positive level and the record of the opposite sense slower, and turns the pair arriving through the +a Port by the Link's odd level and through the -a Port by its opposite (node.step_plane)."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core.rule3 import division_forward

TURNED_REACH = (
    2  # a turned level within twice the amplitude: the rotation's root of two and the three floors
)


def shear(x: Any, y: Any, numerator: Any, wall: Any, direction: int = 1) -> Any:
    """One shear, x' = x + (numerator x y) div wall by the division act with no remainder kept; direction -1 subtracts the same number (the shear leaves y as it is), the exact inverse."""
    return x + direction * division_forward(numerator * y, wall, 0)[0]


def turned(x: Any, y: Any, numerator: Any, wall: Any, direction: int = 1) -> tuple[Any, Any]:
    """The pair (x, y) turned by the angle theta with tan(theta / 2) = numerator / wall, counterclockwise for a positive numerator: x1 = x - (n y) div w, y1 = y + (2 n w x1) div (w^2 + n^2), x2 = x1 - (n y1) div w, the three shears, (x2, y1) the turned pair; direction -1 undoes the three in the reverse order, (x, y) back from (x2, y1) bit for bit."""
    sine, circle = 2 * numerator * wall, wall * wall + numerator * numerator
    if direction == 1:
        x1 = shear(x, y, -numerator, wall)
        y1 = shear(y, x1, sine, circle)
        return shear(x1, y1, -numerator, wall), y1
    x1 = shear(x, y, -numerator, wall, -1)
    y0 = shear(y, x1, sine, circle, -1)
    return shear(x1, y0, -numerator, wall, -1), y0


def guard(numerator: Any, wall: int, name: str, axis: int | None) -> None:
    """The turn's guard at load (the one place the loader bounds a turn, as it bounds a pace): the tangent half-angle at most 1 at every Node, |numerator| <= wall, a quarter turn per interval (the time angle, `axis` None) or per Link (the odd line of `axis`), within which a turned level stays inside the loader's room (`TURNED_REACH`); refused by name beyond it, naming the Node."""
    size = np.abs(np.asarray(numerator))
    high = int(size.max()) if size.ndim else int(size)
    if high > wall:
        node = np.unravel_index(int(size.argmax()), size.shape) if size.ndim else ()
        raise ValueError(
            f"the turn of {name!r} by {'the time level' if axis is None else f'the odd line of the axis {axis}'} "
            f"is {high} over {wall} at the Node {tuple(int(i) for i in node)} at load, a tangent half-angle "
            "above 1 (more than a quarter turn), beyond the room the amplitude bound derives for a turned level "
            "(ENGINE.md, the amplitude bound); the run is refused: raise the holder's level weight"
        )
